import panel as pn
import pandas as pd
import numpy as np
pd.options.plotting.backend = 'holoviews'
from bokeh.transform import factor_cmap, factor_mark
from bokeh.layouts import gridplot
from bokeh.plotting import figure
import plotly.graph_objects as go
import plotly.express as px

pn.extension()

taxonomy_levels = dict(zip(["d", "p", "c", "o", "f", "g", "s"], ["domain", "phylum", "class", "order", "family", "genus", "species"]))


class Node:
    def __init__(self, name, tax_level=None, count=None):
        self.name = name
        self.level = tax_level
        self.children = []
        self.parent = None
        self.zotus = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def set_count(self, count):
        self.count = count

    def __repr__(self):
        first_zotu = "None" if len(self.zotus) == 0 else self.zotus[0]
        parent_name = "None" if self.parent is None else self.parent.name
        return f"\nNode name={self.name}; parent={parent_name}; children={len(self.children)}; zotus={len(self.zotus)}; {self.zotus}"


class Tree:
    def __init__(self):
        self.root = Node("root", "root")
        self.nodes = dict()
        self.nodes["root"] = self.root

    def add_lineages_file(self, file):
        with open(file) as lin_file:
            for line in lin_file:
                self.add_lineage_str(line.strip())

    def add_lineage_str(self, lineage_str):
        # Zotu1  d:Bacteria,p:Actinobacteriota,c:Actinobacteria,o:Micrococcales,f:Micrococcaceae
        zotu, lineage = lineage_str.split("\t")
        lineage = lineage.split(",")
        parent = self.root
        for node_str in lineage:
            level, name = node_str.split(":")
            if name not in self.nodes:
                node = Node(name, taxonomy_levels[level])
                parent.add_child(node)
                node.parent = parent
                parent = node
                self.nodes[name] = node
            else:
                parent = self.nodes[name]
        #last node gets zotu annotated
        self.nodes[name].zotus.append(zotu)

    def get_nodes_as_string(self):
        return [n.__repr__().replace('\n','') for n in self.nodes.values()]

    # def __repr__(self):
    #     return f"Tree: {''.join([n.__repr__() for n in self.nodes.values()])}"


if __name__ == "__main__":
    tree = Tree()
    tree.add_lineages_file('/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/ASV_taxonomy_small.txt')

    print (tree.get_nodes_as_string())

my_data = tree.get_nodes_as_string()

# Writing the data to a .txt file
with open('/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/output.txt', 'w') as file:
    file.write(str(my_data))

# Reading the data back from the .txt file
with open('/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/output.txt', 'r') as file:
    content = file.read()

# Using eval() to convert the string back to a list (caution: potential security risk)
my_data_read = eval(content)

# Display the read data
print(my_data_read)

data = my_data_read

children = []
parents = []

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
    root_color="lightgrey"
))

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig.show()

gridspec = pn.GridSpec(sizing_mode='stretch_both', min_height=600)
gridspec[1:3,1:3] = fig
gridspec

blast_results = pd.read_csv("/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/wetransfer_ngs-data_2023-11-14_1231/NGS data/blast_results.txt", sep=",", header=0)
# print(blast_results)

blast_resultsies = pd.DataFrame(blast_results)
# print(blast_resultsies)
blast_10 = blast_resultsies.head(11)
print(blast_10)

# Create a search bar
search_bar_data = pn.widgets.TextInput(placeholder='Enter Query id...')


# Create a function to filter data based on the query id
def filter_data(query_id):
    if query_id:
        filtered_data = blast_resultsies[blast_resultsies['Query id'].str.contains(query_id, case=False)]
    else:
        filtered_data = blast_resultsies
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

# Serve the app
pn.serve(layout)
