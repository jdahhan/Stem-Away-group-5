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
            "num",
            "path",
            "num2",
            "num3",
        ]  # I am not sure what column 2, 4, 5 is
        print(df.head())
        print(f"Shape: {df.shape}")
        return df

    def generate_artifact(self):
        """This function is supposed to create a data artifact with
        dependency paths, path cluster, drug_gene pairs, and pair_clusters"""

        artifact = self.get_path_matrix()
        paths = artifact["path"].tolist()
        drug_gene = artifact["druggene"].tolist()

        df = pd.DataFrame({"dependency_paths": paths, "drug_gene_pairs": drug_gene})

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
