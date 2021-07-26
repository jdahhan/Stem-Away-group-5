'''
EBC Application

Goal: To generate the Co-occurance statistics



'''

import pandas as pd
import plotly.express as px
from visualize import Visualize


class EDA:
    def ingest_biomedical_data(self):
        # finding distribution of sentence counts
        with open('../data/biomedical_output.txt') as f:
            file = [i.split(" ") for i in f.readlines()]

    def visualize_biomedical_lengths(self, file) -> None:
        lengths = [len(i) for i in file]
        v = Visualize()
        v.onedim_distplot(data = lengths, title = "Distribution of Token Lengths in Biomedical Data")

    def ITCC_densities(self):
        v = Visualize()
        data = pd.read_csv('/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/cXY_output.csv', index_col = 0)
        data = data.T
        data.columns = ["Drug-Gene","Dependency Path"]
        print(data.head())

        print(max(data['Dependency Path']))

        # v.onedim_distplot(data = data['Drug-Gene'], title = 'Drug-Genes Distribution')
        v.onedim_distplot(data = data['Dependency Path'].dropna(), title = 'Dependency Paths Distribution')
        


class ITCC:

    def get_matrix(self, path = "/matrix-ebc-paper-sparse.tsv"):
        pd.read_csv(path,delimiter="\t")

    def run_N_times(self):
        pass
