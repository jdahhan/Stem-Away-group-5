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

        # Schema validation
        # df["pair_cluster"] = df["pair_cluster"].astype(int)
        # df["path_cluster"] = df["path_cluster"].astype(int)

        return df

    def generate_artifact(self, druggene_mappings, path_mappings) -> pd.DataFrame:
        """This function is supposed to create a data artifact with
        dependency paths, path cluster, drug_gene pairs, and pair_clusters"""

        def make_hashtable(df, col1, col2) -> dict:
            """Creating a function to create a hashtable or dictionary from the respective mappings dataframes"""
            hash = dict(zip(df[col1], df[col2]))
            # switch = lambda my_dict: {
            #     y: x for x, y in my_dict.items()
            # }  # utility function to switch keys and values
            return hash

        path_hash = make_hashtable(path_mappings, "column_indice", "path")
        druggene_hash = make_hashtable(druggene_mappings, "row_indice", "druggene")

        df = self.getCXY()

        # Making a column for drug gene names and dependency paths
        try:
            df["path"] = df["path_cluster"].apply(lambda x: path_hash[int(x)])
            df["druggene_pair"] = df["pair_cluster"].apply(
                lambda x: druggene_hash[int(x)]
            )
        except KeyError as e:
            print(e)

        # save artifact
        df.to_csv(self.artifact_path + "/ebc_artifact.csv")

        return df

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
