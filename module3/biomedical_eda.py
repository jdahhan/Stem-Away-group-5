""" This module is used for the brief Exploratory Data Analysis of medical data.
The outputs I have extracted as plotly plots.
"""
import plotly.express as px
from visualize import Visualize


class _EDA:
    """This class is a utility class used for an initial EDA of the biomedical
    abstracts."""

    def _ingest_biomedical_data(self):
        """finding distribution of sentence counts"""
        with open("../data/biomedical_output.txt") as f:
            file = [i.split(" ") for i in f.readlines()]

        return file

    def _visualize_biomedical_lengths(self, file) -> None:
        """Finding sequence lengths in a file"""
        lengths = [len(i) for i in file]
        v = Visualize()
        v.onedim_distplot(
            data=lengths, title="Distribution of Token Lengths in Biomedical Data"
        )

    def ITCC_densities(self):
        v = Visualize()
        data = pd.read_csv(
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/cXY_output.csv",
            index_col=0,
        )
        data = data.T
        data.columns = ["Drug-Gene", "Dependency Path"]
        print(data.head())

        print(max(data["Dependency Path"]))
        # v.onedim_distplot(data = data['Drug-Gene'], title = 'Drug-Genes Distribution')
        v.onedim_distplot(
            data=data["Dependency Path"].dropna(), title="Dependency Paths Distribution"
        )
