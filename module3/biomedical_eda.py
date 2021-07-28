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


#%%
import pandas as pd

df = pd.read_csv(
    "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/matrix.csv",
    index_col=0,
)

df["druggene"] = df["druggene"].astype(str)
df["path"] = df["path"].astype(str)

df.drop_duplicates(subset=["druggene"], keep="first", inplace=True)
df.head()
# %%
df.info()
# %%
df.shape

#%%

artifact_path = "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/"
# %%
df.to_csv(
    "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/filtered_matrix.csv"
)
df[["path", "column_indice"]].to_csv(artifact_path + "path_mappings.csv")

# %%
druggene_df = df.copy()

druggene_df.sort_values("row_indice", ascending=True, inplace=True)

druggene_df[["druggene", "row_indice"]].to_csv(artifact_path + "druggene_mappings.csv")
# %%
druggene_mappings = pd.read_csv(
    "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/druggene_mappings.csv",
    index_col=0,
)
path_mappings = pd.read_csv(
    "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/path_mappings.csv",
    index_col=0,
)


#%%
path_mappings.head()

# %%
druggene_mappings.head()

# %%

make_hashtable = lambda df, col1, col2: dict(zip(df[col1], df[col2]))

make_hashtable(druggene_mappings, "druggene", "row_indice")

# %%
make_hashtable(path_mappings, "path", "column_indice")
# %%
ebc_df = pd.read_csv("/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/ebc_artifact.csv", index_col=0)

ebc_df
# %%