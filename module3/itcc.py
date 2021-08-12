"""
EBC Application

Goal: To generate the Co-occurance statistics

"""

from os import pathconf
import pandas as pd
from module3.ebc.ebc import EBC
from module3.ebc.matrix import SparseMatrix
import numpy as np


class ITCC:
    """This class gives you ways of getting useful data artifacts and
    actually runs the ITCC algorithm appropriately in conjuction with
    help from the official EBC implementation which is in the ebc directory
    to create a co-occurance matrix of drug-gene pairs (we do not need
    path co-occurance"""

    def __init__(self, runs=10):
        self.artifact_path = (
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts"
        )
        self.runs = runs
        self.matrix = SparseMatrix(
            [14052, 7272]
        )  # want to compress this to 30 and 125 dimensions, whilst preserving as much information as possible

    def get_data(
        self,
        resource_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/ebc/resources/matrix-ebc-paper-sparse.tsv",
    ):
        """Outputs a list in the form:
        ['(rc-160,igf-i)', '[nsubj, reduced, dobj]', 1.0]

        This is the format that the EBC implementation wants it in.
        """
        with open(resource_path, "r") as f:
            data = []
            for line in f:
                sl = line.split("\t")
                if len(sl) < 5:  # Skipping less than 5 length tokens
                    continue
                data.append([sl[0], sl[2], float(sl[4])])

        return data

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
        pairpath_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/module3/Pair_Path_Mapping_Dense.csv",
    ) -> pd.DataFrame:
        """This function uses the drugbank and pairpath CSV file to create a
        consolidated dataframe with the drugbank ground truth column.

        NOTE: Example usage is shown in the implement_itcc.py script
        """

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
        exists_mask = [i in text_parse for i in pair_paths["Drug-Gene"]]

        pair_paths["DrugBank"] = exists_mask  # adding ground truth column

        return pair_paths

    def run_ITCC(self):
        """Runs the ITCC algorithm one time"""
        data = self.get_data()
        self.matrix.read_data(data)
        self.matrix.normalize()

        ebc = EBC(self.matrix, [30, 125], 10, 1e-10, 0.01)
        (
            cXY,
            objective,
            it,
        ) = ebc.run()

        # Transposing the list
        map(list, map(None, *cXY))

        return cXY[0]
        # import csv
        # write to file
        # with open("Co-occurency.csv", "a") as f:
        #     writer = csv.writer(f)
        #     writer.writerows(cluster)

    def run_R_times(self, R: int = 1):
        """Runs the ITCC algorithm N times to get the cooccurance matrix.
        Input:
            R is the number of runs.
        Output:
            EBC Output Artifact
        """
        return [self.run_ITCC() for i in range(R)]

    def get_cooccurance(self, ebc_output: list, matrix: np.array) -> pd.DataFrame:
        """This function is meant to create a dataframe with the cooccurance
        matrix"""

        for i, row in enumerate(ebc_output):
            temp = row[0]
            for j, col in enumerate(row):
                if col == temp:
                    matrix[i][j] += 1

        return matrix

    def get_dense_artifact(self, full_artifact: pd.DataFrame, dense_path: str):
        pass

    # Helper methods
    def _peek_matrix(self):
        print(str(matrix))  # QUESTION: what does this sparse matrix represent?

    def _list_diagnostics(self, l):
        print(f"Length of list is: \n{len(l)}")
        print("Lengths of the list:")
        print([len(i) for i in l])

    def _output_list_of_lists(self, l, path_to="cXY_output.csv"):
        df = pd.DataFrame.from_records(l)
        df.to_csv(path_to)


# Using the EBC to generate the artifacts
if __name__ == "__main__":
    i = ITCC()
    i.main()
