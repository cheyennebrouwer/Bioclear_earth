import pandas as pd
import config


def load_taxonomy():
    file_path = config.read_config()['Paths']['taxonomy']
    return pd.read_table(file_path, sep="	",
                         header=None,
                         index_col=0)


def load_counts():
    file_path = config.read_config()['Paths']['counts']
    return pd.read_table(file_path,
                         delimiter='\t',
                         index_col=0)


def load_mapping():
    file_path = config.read_config()['Paths']['mapping']
    return pd.read_table(file_path,
                         index_col=0)


def load_blast_results():
    file_path = config.read_config()['Paths']['blast_results']
    return pd.read_csv(file_path,
                       sep=",",
                       header=0)


def save_output(data):
    file_path = config.read_config()['Paths']['output']
    data.to_csv(file_path,
                index=False)

# load in the data
# taxonomy_data = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/" \
#                 "ASV_taxonomy_small.txt"
# df_taxonomy = pd.read_table(taxonomy_data,
#                             sep="	",
#                             header=None,
#                             index_col=0)
#
# counts_file = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear_earth/ASV_counts_small.txt"
# df_counts = pd.read_table(counts_file,
#                           delimiter='\t',
#                           index_col=0)
#
# mapping = "/Users/cheyennebrouwer/Documents/23-24/Kwartaal_2/Data_Dashboards/Bioclear/" \
#           "wetransfer_ngs-data_2023-11-14_1231/Mapping.txt"
# mapping_df = pd.read_table(mapping,
#                            index_col=0)


    def load_blast_results():
        return None