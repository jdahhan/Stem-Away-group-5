import unittest
from itcc import ITCC
import pandas as pd


class TestITCC(unittest.TestCase):
    def test_itcc_ingest(self):
        i = ITCC()
        df = i.get_path_matrix()
        self.assertEqual(type(df), pd.DataFrame)


unittest.main()
