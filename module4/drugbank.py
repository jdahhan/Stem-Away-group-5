"""
Goal: Generate seed and test sets
"""


def ingest_drugbank(path):
    """Creating a function to ingest the Drugbank XML files"""
    drugbank = []
    with open(path, "r") as f:
        for line in f:
            drugbank.append(line)
    return drugbank
