taxonomy_levels = dict(
    zip(["d", "p", "c", "o", "f", "g", "s"], ["domain", "phylum", "class", "order", "family", "genus", "species"]))


class Node():
    def __init__(self, name, zotu=None, tax_level=None, counts={}):  # counts is dict van sample en percentage
        self.name = name
        self.level = tax_level
        self.children = []
        self.parent = None
        self.zotus = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __repr__(self):
        parent_name = "None" if self.parent is None else self.parent.name
        zotus = '' if len(self.zotus) == 0 else f'; zotus={len(self.zotus)}:{self.zotus}'
        children = '' if len(self.children) == 0 else f'; children={len(self.children)}'
        return f"Node name={self.name}; parent={parent_name}{children}{zotus}"


class SampleCounts():
    '''data class to store sample counts for taxonomic levels'''

    def __init__(self, sample):
        self.sample = sample
        self.counts = dict()

    def __repr__(self):
        return f'sample {self.sample}: counts={self.counts}'


class Tree():
    def __init__(self):
        self.root = Node("root", "root")
        self.nodes = dict()
        self.zotus = dict()
        self.nodes["root"] = self.root

    def add_lineages_file(self, file):
        with open(file) as lin_file:
            for line in lin_file:
                self.add_lineage_str(line.strip())

    def add_lineage_str(self, lineage_str):
        # Zotu1	d:Bacteria,p:Actinobacteriota,c:Actinobacteria,o:Micrococcales,f:Micrococcaceae
        zotu, lineage = lineage_str.split("\t")
        lineage = lineage.split(",")
        parent = self.root
        for node_str in lineage:
            level, name = node_str.split(":")
            if 'uncultured' in name:
                name = name + ' ' + parent.name

            if name not in self.nodes:
                node = Node(name, taxonomy_levels[level])
                parent.add_child(node)
                node.parent = parent
                parent = node
                self.nodes[name] = node
            else:
                parent = self.nodes[name]
        # last node gets zotu annotated
        self.nodes[name].zotus.append(zotu)

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

    def __repr__(self):
        return f"Tree: {''.join([n.__repr__() for n in self.nodes.values()])}"

    def __str__(self):
        newick = self._newick(self.root)
        newick.extend(';')
        return ''.join(newick)

    def print_nodes(self):
        for name in self.nodes:
            print(name, ':', self.nodes[name])

    def _newick(self, node, newick=[]):
        if len(node.children) > 0:
            newick.extend('(')
            for child in node.children:
                newick = self._newick(child, newick)
            if newick[-1] == ',':
                newick = newick[:-1]
            newick.extend(')')
        else:
            newick.extend(node.name)
            newick.extend(',')
        return newick


if __name__ == "__main__":
    tree = Tree()
    tree.add_lineages_file('ASV_taxonomy_extra_small.txt')
    tree.print_nodes()