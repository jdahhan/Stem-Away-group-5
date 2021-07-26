import unittest
from itcc import EDA, ITCC



class TestITCC(unittest.TestCase):
    def test_ITCC_densities(self):
        eda = EDA()
        eda.ITCC_densities()


unittest.main()
        