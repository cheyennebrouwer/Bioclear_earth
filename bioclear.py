import pandas as pd


def read_fasta(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            print(line)


file_path_fasta = "/Bioclear/wetransfer_ngs-data_2023-11-14_1231/NGS data/ASV.fa"

read_fasta(file_path_fasta)



