import unittest
from module4.ebc_scoring import EBCScoring
from module3.itcc import ITCC

ebc = EBCScoring(itcc=ITCC())


class TestEbcScoring(unittest.TestCase):
    def test_get_testset(self):
        artifact = ebc.get_itcc_artifact()
        test_set1 = ebc.get_testset(artifact=artifact, half_size=10)
        print(test_set1)
        assert test_set1.shape[0] == 20

    def test_get_seed_and_test_set(self):
        artifact = ebc.get_dense_itcc_artifact()
        seed, test = ebc.get_seed_and_test_sets(artifact=artifact, sample_size=10)

        print(test.head())
        print(seed.head())

    def test_seed_and_test_set_intersection(self):
        artifact = ebc.get_dense_itcc_artifact()
        seed, test = ebc.get_seed_and_test_sets(artifact=artifact, sample_size=10)
        assert len(set(seed["Drug-Gene"]).intersection(set(test["Drug-Gene"]))) != 0

    def test_generate_filtered_matrix(self):
        artifact = ebc.get_dense_itcc_artifact()
        seed, test = ebc.get_seed_and_test_sets(artifact=artifact, sample_size=10)
        test_pairs = list(test["Drug-Gene"].apply(lambda x: x.replace("/", ",")))
        matrix = ebc.generate_filtered_matrix(test_pairs)
        print(matrix.head())
        assert matrix.shape[0] > 0


unittest.main()
