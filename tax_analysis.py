import pandas as pd
from model import Tree

def load_count_data(counts_file):
    counts = pd.read_table(counts_file, index_col=0)
    return counts

def normalize_counts(counts_df):
    counts_columns = counts_df.columns.difference(['OTUID'])
    normalized_counts = counts_df.copy()

    for count_column in counts_columns:
        normalized_counts[count_column] = normalized_counts[count_column] / normalized_counts[count_column].sum() * 100

    return normalized_counts


if __name__ == "__main__":
    tree = Tree()
    tree.add_lineages_file('ASV_taxonomy_extra_small.txt')
    #print(str(tree))

    counts_file = "ASV_counts_extra_small.tsv"
    counts_df = load_count_data(counts_file)
    normalized_counts = normalize_counts(counts_df)
    print(normalized_counts)