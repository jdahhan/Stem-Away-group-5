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
        dependency paths, path cluster, drug_gene pairs, and pair_clusters

        NOTE: Sourav implemented a pipeline to generate this artifact. This particular function is 90% of the way there, but
        it is discontinued in favor of what Sourav created.
        """

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

    def get_drugbank_artifact(
        self,
        drugbank_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/module4/drugbank_pairs.tsv",
        pairpath_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/module3/Pair_Path_Mapping.csv",
    ) -> pd.DataFrame:
        """This function uses the drugbank and pairpath CSV file to create a
        consolidated dataframe with the drugbank ground truth column"""

        # Get drugbank
        drugbank = pd.read_csv(drugbank_path, delimiter="\t", header=None)
        drugbank.columns = ["Drug", "Gene"]
        # parsing to appropriate format
        text_parse = [
            f"({str(drug).lower()}/{str(gene).lower()})"
            for drug, gene in zip(drugbank["Drug"], drugbank["Gene"])
        ]

        pair_paths = pd.read_csv(
            pairpath_path,
            index_col=0,
        )

        # checking for matches in the drug gene column and the drugbank genes
        exists_mask = [i in text_parse for i in pair_paths["drug-gene"]]

        pair_paths["DrugBank"] = exists_mask  # adding ground truth column

        return pair_paths

    def run_ITCC(self):
        """Runs the ITCC algorithm one time"""
        pass

    def cooccurance() -> pd.DataFrame:
        """This function is meant to create a dataframe with the cooccurance
        matrix"""
        df = pd.DataFrame()

    def run_N_times(self):
        """Runs the ITCC algorithm N times to get the cooccurance matrix"""
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
