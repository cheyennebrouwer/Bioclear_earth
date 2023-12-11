import pandas as pd
import panel as pn
import RUST as rust
import taxonomy


# def read_fasta(file_path):
#     with open(file_path, "r") as file:
#         for line in file:
#             line = line.strip()
#             print(line)
#
# # take one zotu and put in variable
#
# file_path_tax = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/wetransfer_ngs-data_2023-11-14_1231/NGS data/ASV_taxonomy.txt"
#
# df_tax_file = pd.DataFrame()
# read_fasta(file_path_tax)

# Taxonomy.from_newick(variable that contains zotu)

tax_file = pd.read_csv("/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/wetransfer_ngs-data_2023-11-14_1231/NGS data/ASV_taxonomy.txt")
one_zotu = tax_file.loc["Zotu1"]

