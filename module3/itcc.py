"""
EBC Application

Goal: To generate the Co-occurance statistics

"""

from os import pathconf
import pandas as pd


class ITCC:
    """This class is meant to be used in conjunction with the
    EBC.py implementation repo"""

    def __init__(self):
        self.artifact_path = (
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts"
        )

    def get_path_matrix(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/matrix-ebc-paper-sparse.tsv",
    ) -> list:
        """Getting a list of all the dependency paths from the EBC dependency matrix data
        artifact as given from the EBC repository.
        """
        df = pd.read_csv(path, delimiter="\t")
        df.columns = [
            "druggene",
            "row_indice",
            "path",
            "column_indice",
            "certainty_value",
        ]

        print(df.info())

        df = df.sort_values(by=["column_indice"])

        print(df.head())
        print(f"Shape: {df.shape}")

        df.to_csv(
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/matrix.csv"
        )

        return df

    def getCXY(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/cXY_output.csv",
    ):
        df = pd.read_csv(path)
        df = df.T
        df.columns = ["pair_cluster", "path_cluster"]
        df = df.iloc[1:, :]  # getting rid of first row

        return df["pair_cluster"].dropna(), df["path_cluster"].dropna()

    def generate_artifact(self, druggene_mappings, path_mappings) -> pd.DataFrame:
        """This function is supposed to create a data artifact with
        dependency paths, path cluster, drug_gene pairs, and pair_clusters"""

        def make_hashtable(df, col1, col2) -> dict:
            """Creating a function to create a hashtable or dictionary from the respective mappings dataframes"""
            return dict(zip(df[col1], df[col2]))

        path_hash = make_hashtable(path_mappings, "column_indice", "path")
        druggene_hash = make_hashtable(druggene_mappings, "row_indice", "druggene")

        pair_cluster, path_cluster = self.getCXY()

        druggene = pair_cluster.apply(lambda x: druggene_hash[int(x) + 1])
        paths = [
            path_hash.get(int(i) + 1, None) for i in path_cluster
        ]  # NOTE: Incomplete mappings

        # Diagnostics
        print(
            f"Pair Cluster Shape: {pair_cluster.shape}, Path Cluster Shape: {path_cluster.shape}"
        )

        # Making a column for drug gene names and dependency paths

        df = pd.DataFrame()

        df["pair_cluster"] = pair_cluster
        df["druggene_pair"] = druggene
        df["path_cluster"] = path_cluster
        df["path"] = paths + [None] * (df.shape[0] - len(paths))

        # save artifact
        # df.to_csv(self.artifact_path + "/ebc_artifact.csv")

        return df

    def get_drugbank(path: str):
        """Getting all the drug gene pairs in drugbank (ground truth)"""
        pd.read_csv()

    def run_N_times(self):
        pass

    def _list_diagnostics(self, l):
        print(f"Length of list is: \n{len(l)}")
        print("Lengths of the list:")
        print([len(i) for i in l])

    def _output_list_of_lists(self, l, path_to="cXY_output.csv"):
        df = pd.DataFrame.from_records(l)
        df.to_csv(path_to)


# Using the EBC to generate the artifacts
itcc = ITCC()
