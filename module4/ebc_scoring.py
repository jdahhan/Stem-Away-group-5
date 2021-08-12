import pandas as pd
import math
import numpy as np


class EBCScoring:
    def __init__(self, itcc, seed_set_size: int = 10):
        self.seed_set_size = seed_set_size
        self.itcc = itcc  # ITCC object from module 3

    def get_seed_and_test_sets(self, artifact: pd.DataFrame, sample_size: int):
        """Samples the seed set, then the test set. Finally returns both."""
        filtered = artifact[artifact["DrugBank"] == True]

        seed_set_sample = filtered.sample(n=sample_size)

        artifact_without_seedset = artifact.drop(labels=seed_set_sample.index, axis=0)

        # We are not allowed to get the same seed set pairs that we just sampled
        # twice, so I feed in the artifact without that seed set here
        test_set_sample = self.get_testset(
            artifact=artifact_without_seedset, half_size=math.floor(sample_size / 2)
        )

        return seed_set_sample, test_set_sample

    def get_drugbank(self):
        artifact = self.get_dense_itcc_artifact()
        return artifact[artifact["DrugBank"] == True]

    def get_testset(self, artifact, half_size: int):
        """These sets have a 50-50 split of sets in drugbank and not in drugbank.
        Half size represents the size of 50 percent of the sample which is either
        all in drugbank or all non-drugbank pairs."""
        in_drugbank = self.get_drugbank()
        not_in_drugbank = artifact[artifact["DrugBank"] == False]
        drugbank_sample = in_drugbank.sample(n=half_size)
        not_in_drugbank_sample = not_in_drugbank.sample(n=half_size)
        return drugbank_sample.append(not_in_drugbank_sample)

    def get_N_data(self, low=5, high=12, N=1000):
        """Get N seed sets"""
        artifact = self.get_dense_itcc_artifact()
        lengths = np.random.randint(low, high, N)

        seedsets = []
        testsets = []
        # Get seedsets and test sets
        for l in lengths:
            seed_set, test_set = self.get_seed_and_test_sets(artifact, l)
            seedsets.append(seed_set)
            testsets.append(test_set)

        return seedsets, testsets

    def generate_filtered_matrix(self, test_set_pairs: pd.Series):
        """Generates the test set coocurance matrix
        Inputs:
            test_set_pairs: pd.Series of the test set drug-gene pairs
        Outputs:
            Coocurance matrix with just the test set
        """
        # converting to the correct data format and string formatting
        test_pairs = list(test_set_pairs.apply(lambda x: x.replace("/", ",")))

        matrix = self.get_cooccurance()
        # drugbank_pairs = artifact[artifact["DrugBank"] == True]["Drug-Gene"]

        mask = [i in test_pairs for i in matrix.index]

        return matrix[mask]

    def generate_ebc_scoring_artifact(self, filtered_matrix, seed_pairs):
        """Adding seed set indicators to the artifact.

        Be cautious of the format of the seed pairs (if it uses a ',' or a '/' delimiter respectively),
        otherwise the matching will not work.
        """
        matrix = filtered_matrix.T
        seed_pairs = list(seed_pairs.apply(lambda x: x.replace("/", ",")))
        matrix["SeedSet"] = [i in seed_pairs for i in matrix.index]
        return matrix

    def score(self, ebc_scoring_artifact, drugbank_pairs):
        """This is where I generate a score for each test set and seed set pair.

        Paper description of process:

        For each test set Ti, rank all n rows of the data matrix based on how often they co-cluster with Ti.
        This produces a ranking Ri of length in in which pairs that
        frequently co-cluster with Ti are assigned high ranks
        and those that seldom cluster get low ranks. The score for Ti is the ranksum
        of the member sof the seed set, S, within this list
        """
        for i, j in ebc_scoring_artifact.to_dict("list").items():
            

    def get_cooccurance(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/module3/Co-occurrency Matrix/Co-occurrency_Matrix.csv",
    ):
        return pd.read_csv(path, index_col=0)

    def get_itcc_artifact(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/itcc_artifact.csv",
    ):
        return pd.read_csv(
            path,
            index_col=0,
        )

    def get_dense_itcc_artifact(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/itcc_dense_artifact.csv",
    ):
        return pd.read_csv(
            path,
            index_col=0,
        )

    def main(self):
        """Runthrough of intended usage"""
        pass
