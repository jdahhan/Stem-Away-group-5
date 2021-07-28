import unittest
from itcc import ITCC
import pandas as pd


class TestITCC(unittest.TestCase):
    def test_itcc_ingest(self):
        i = ITCC()
        df = i.get_path_matrix()
        self.assertEqual(type(df), pd.DataFrame)
        df.describe()

    def test_getCXY(self):
        i = ITCC()
        df = i.getCXY()
        print(df.head())
        print(f"Shape: {df.shape}")

    def test_generate_artifact(self):
        i = ITCC()
        druggene_mappings = pd.read_csv(
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/druggene_mappings.csv",
            index_col=0,
        )
        path_mappings = pd.read_csv(
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/path_mappings.csv",
            index_col=0,
        )

        df = i.generate_artifact(
            druggene_mappings=druggene_mappings, path_mappings=path_mappings
        )
        print(df.head())

        df.to_csv(
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/ebc_artifact.csv"
        )


unittest.main()
