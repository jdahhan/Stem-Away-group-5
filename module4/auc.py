"""
This is where I generate the AUC metrics for a given dataset.
"""

from module4.ebc_scoring import EBCScoring


class AUC:
    def __init__(self):
        self.ebc = EBCScoring()
