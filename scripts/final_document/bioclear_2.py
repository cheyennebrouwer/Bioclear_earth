import configparser
import pandas as pd
import panel as pn
import plotly.graph_objects as go

pn.extension()

config = configparser.ConfigParser()
config.read('config.ini')


def load_taxonomy():
    file_path = config['Paths']['taxonomy']
    return pd.read_table(file_path, sep="\t", header=None, index_col=0)


def load_counts():
    file_path = config['Paths']['counts']
    return pd.read_table(file_path, delimiter='\t', index_col=0)


def load_mapping():
    file_path = config['Paths']['mapping']
    return pd.read_table(file_path, index_col=0)


def load_blast_results():
    file_path = config['Paths']['blast_results']
    return pd.read_csv(file_path, sep=",", header=0)


def save_output(data):
    file_path = config['Paths']['output']
    data.to_csv(file_path, index=False)


homepage_text = pn.widgets.StaticText(name="Home Page",
                                      value="This project was made with data obtained from Bioclear Earth. This data is"
                                            "represented on the website as a couple of things. The first tab, called "
                                            "Tree, contains a taxonomic tree. This is made in a tree plot, which is"
                                            " clickable and colourcoded on the amount of counts. On the third page, "
                                            "Charts, there are multiple plots. These range fom a search bar that gives "
                                            "information about the zotu that you look for, to an alignment plot and a"
                                            " plot that shows the distribution of different variables per sample. "
                                            "If a sample is required, fill in a sample with a coding that looks like"
                                            "this: Example: S002P8292. If a query id is requested, a zotu with a number"
                                            " ranging from 1 to 44000 can be entered. Example: Zotu44")

Reference_page = pn.widgets.StaticText(name="References",
                                       value="The data that is used for the plots on this website was obtained from"
                                             " Bioclear Earth. Website: https://bioclearearth.nl/")


class Node:
    def __init__(self, name, tax_level=None, count=None):
        self.name = name
        self.level = tax_level
        self.children = []
        self.parent = None
        self.counts = dict()
        self.zotus = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def set_count(self, count):
        self.count = count

    def __repr__(self):
        parent_name = "None" if self.parent is None else self.parent.name
        zotus = '' if len(self.zotus) == 0 else f'; zotus={len(self.zotus)}:{self.zotus}'
        children = '' if len(self.children) == 0 else f'; children={len(self.children)}'
        return f"Node name={self.name}; parent={parent_name}{children}{zotus}{self.children}; zotus={len(self.zotus)}; {self.zotus}"


class SampleCounts:
    """data class to store sample counts for taxonomic levels"""

    def __init__(self, sample):
        self.sample = sample
        self.counts = dict()

    def __repr__(self):
        return f'sample {self.sample}: counts={self.counts}'


class Tree:
    def __init__(self):
        self.root = Node("root", tax_level="root")
        self.nodes = dict()
        self.zotus = dict()
        self.nodes["root"] = self.root

    def add_lineages_file(self, file):
        with open(file) as lin_file:
            for line in lin_file:
                try:
                    self.add_lineage_str(line.strip())
                except Exception as ex:
                    print(ex, '\n', line)

    def add_lineage_str(self, lineage_str):
        # Zotu1  d:Bacteria,p:Actinobacteriota,c:Actinobacteria,o:Micrococcales,f:Micrococcaceae
        zotu, lineage = lineage_str.split("\t")
        lineage = lineage.split(",")
        parent = self.root
        for node_str in lineage:
            level, name = node_str.split(":")
            if 'uncultured' in name:
                name = name + ' ' + parent.name

            if zotu in zotu_list:
                if name not in self.nodes:
                    node = Node(name, taxonomy_levels[level])
                    parent.add_child(node)
                    node.parent = parent
                    parent = node
                    self.nodes[name] = node
                else:
                    parent = self.nodes[name]
            else:
                continue
        # last node gets zotu annotated
        self.nodes[name].zotus.append(zotu)
        self.zotus[zotu] = node

    def get_counts(self, tax_level, samples):
        # iterate tree
        # find nodes with correct level
        counts = list()
        for sample in samples:
            counts.append(SampleCounts(sample))
        # print(counts)
        # return counts
        for node in self.nodes:
            if node.level == tax_level:
                # fetch counts for requested samples
                for sample in samples:
                    if sample in node.counts:
                        counts[sample] = node.counts[sample]

    def get_nodes_as_string(self):
        return [n.__repr__().replace('\n', '') for n in self.nodes.values()]

    def __str__(self):
        newick = self._newick(self.root)
        newick.extend(';')
        return ''.join(newick)

    def print_nodes(self):
        for name in self.nodes:
            print(name, ':', self.nodes[name])


# Load data
taxonomy_data = load_taxonomy()
df_counts = load_counts()
mapping_df = load_mapping()
blast_results = load_blast_results()

# Set up the zotu list and counts
zotu_count_list = {}
zotu_list = []

samples = pn.widgets.MenuButton(name='Select Sample', items=list(df_counts.columns)[1:])
if samples.clicked:
    default_sample = samples.clicked
else:
    default_sample = ['S001P8292']

sample_one = default_sample[0]
sample_one = df_counts[(df_counts[default_sample[0]]) != 0]
zotu_list = sample_one[default_sample[0]].index.tolist()
zotu_count_list = sample_one[default_sample[0]].tolist()

taxonomy_levels = dict(
    zip(["d", "p", "c", "o", "f", "g", "s"],
        ["domain", "phylum", "class", "order", "family", "genus", "species"]))

# Create Tree instance
tree = Tree()
tree.add_lineages_file(config['Paths']['taxonomy'])

my_data = tree.get_nodes_as_string()

# Plotting
data = my_data
children = []
parents = []
counts = zotu_count_list

for entry in data:
    parts = entry.split(';')
    if len(parts) >= 2:
        node_name = parts[0].split('=')[1].strip()
        parent = parts[1].split('=')[1].strip() if parts[1].split('=')[1].strip() != 'None' else ''
        children.append(node_name)
        parents.append(parent)

fig = go.Figure(go.Treemap(
    labels=children,
    parents=parents,
    values=counts,
    marker=dict(
        colors=counts,
        colorscale='ylorbr',
        colorbar=dict(title='Counts')
    ),
    root_color="lightgrey"
))

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25),
                  width=1250,
                  height=700)


class Plots:
    def __init__(self):
        self.blast_results = pd.read_csv(config['Paths']['blast_results'], sep=",", header=0)
        self.search_bar_data = pn.widgets.TextInput(placeholder='Enter Query id...')
        self.display_table = pn.pane.DataFrame(self.blast_results.head(11))

        self.search_bar_data.param.watch(self.update_display, 'value')

    def filter_data(self, query_id):
        if query_id:
            filtered_data = self.blast_results[self.blast_results['Query id'].str.contains(query_id, case=False)].head(1)
        else:
            filtered_data = self.blast_results.head(11)
        return filtered_data

    def update_display(self, event):
        query_id = self.search_bar_data.value
        filtered_data = self.filter_data(query_id)
        self.display_table.object = filtered_data

    def layout(self):
        return pn.Column(
            "## Query Data Search",
            self.search_bar_data,
            self.display_table
        )


# Create Plots instance
plots = Plots()

# make multiple pages
homepage_content = pn.Row(homepage_text)
page1_content = pn.Row(samples, fig)
page2_content = plots.layout()
page3_content = pn.Row(Reference_page)
tabs = pn.Tabs(("Home", homepage_content),
               ("Tree", page1_content),
               ("Charts", page2_content),
               ("References", page3_content))

# place it in a dashboard
dashboard = pn.template.BootstrapTemplate(title='Bioclear Earth')
dashboard.header_background = '#AC3E31'
dashboard.main.append(tabs)
dashboard.show()
