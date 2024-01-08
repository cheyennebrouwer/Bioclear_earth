import pandas as pd
import panel as pn
import RUST
import taxonomy
from taxonomy.taxonomy import Taxonomy

tax_file = pd.read_csv("/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/"
                       "wetransfer_ngs-data_2023-11-14_1231/NGS data/ASV_taxonomy.txt", sep="	", header=0,
                       index_col=0)
# one_zotu = tax_file.loc["Zotu1"]
# print(one_zotu)

Taxonomy.from_newick(variable that contains zotu)

