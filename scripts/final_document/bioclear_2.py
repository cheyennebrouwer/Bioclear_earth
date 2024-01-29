import pandas as pd
import panel as pn
import numpy as np
import matplotlib.pyplot as plt
from bokeh.transform import factor_cmap, factor_mark, cumsum
from bokeh.layouts import gridplot
from bokeh.plotting import figure
import plotly.graph_objects as go
import plotly.express as px
from bokeh.models import Dropdown, Select, Legend, LegendItem, ColumnDataSource
from bokeh.plotting import show
from bokeh.layouts import column
from math import pi
from bokeh.palettes import Category20c

# pnextension
pn.extension()

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

# load in the data
taxonomy_data = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/" \
                "ASV_taxonomy_small.txt"
df_taxonomy = pd.read_table(taxonomy_data,
                            sep="	",
                            header=None,
                            index_col=0)

counts_file = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/ASV_counts_small.txt"
df_counts = pd.read_table(counts_file,
                          delimiter='\t',
                          index_col=0)

mapping = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/" \
          "wetransfer_ngs-data_2023-11-14_1231/Mapping.txt"
mapping_df = pd.read_table(mapping,
                           index_col=0)

# get the counts and zotu's from the chosen sample
column_names = list(df_counts)
samples = pn.widgets.MenuButton(name='Select Sample',
                                items=column_names[1:])


def menu_callback(event):
    selected_column = samples.value
    print(f"Selected column: {selected_column}")


zotu_count_list = {}
zotu_list = []

if samples.clicked:
    default_sample = samples.clicked
else:
    default_sample = ['S001P8292']

sample_one = default_sample[0]

sample_one = df_counts[(df_counts[default_sample[0]]) != 0]
zotu_list = sample_one[default_sample[0]].index.tolist()
zotu_count_list = sample_one[default_sample[0]].tolist()

# create nodes
taxonomy_levels = dict(
    zip(["d", "p", "c", "o", "f", "g", "s"],
        ["domain", "phylum", "class", "order", "family", "genus", "species"]))


class Node():
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


class SampleCounts():
    """data class to store sample counts for taxonomic levels"""

    def __init__(self, sample):
        self.sample = sample
        self.counts = dict()

    def __repr__(self):
        return f'sample {self.sample}: counts={self.counts}'


class Tree():
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


if __name__ == "__main__":
    tree = Tree()
    tree.add_lineages_file("/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/"
                           "ASV_taxonomy_small.txt")

my_data = tree.get_nodes_as_string()

# Writing the data to a .txt file
with open("/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/output.txt", 'w') as file:
    file.write(str(my_data))

# # Reading the data back from the .txt file
with open('/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/output.txt', 'r') as file:
    content = file.read()

# # Using eval() to convert the string back to a list
my_data_read = eval(content)

# # Display the read data
print(my_data_read)

# create plot
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

# fig = go.Figure(go.Treemap(
#     labels=children,
#     parents=parents,
#     root_color="lightgrey"
# ))

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


blast_results = pd.read_csv("/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/"
                            "wetransfer_ngs-data_2023-11-14_1231/NGS data/blast_results.txt", sep=",", header=0)
# print(blast_results)

blast_resultsies = pd.DataFrame(blast_results)
# print(blast_resultsies)
blast_10 = blast_resultsies.head(11)

# Create a search bar
search_bar_data = pn.widgets.TextInput(placeholder='Enter Query id...')


# Create a function to filter data based on the query id
def filter_data(query_id):
    if query_id:
        filtered_data = blast_resultsies[blast_resultsies['Query id'].str.contains(query_id, case=False)].head(1)
    else:
        filtered_data = blast_resultsies.head(11)
    return filtered_data


# Create a function to update the displayed information based on the query id
def update_display(event):
    query_id = search_bar_data.value
    filtered_data = filter_data(query_id)
    display_table.object = filtered_data


# Create a panel widget for displaying information
display_table = pn.pane.DataFrame(blast_10)

# Set up the callback to update the display when the query id changes
search_bar_data.param.watch(update_display, 'value')

# Create the layout
layout = pn.Column(
    "## Query Data Search",
    search_bar_data,
    display_table
)

# make multiple pages
homepage_content = pn.Row(homepage_text)
page1_content = pn.Row(samples, fig)
page2_content = pn.Row(layout)
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
