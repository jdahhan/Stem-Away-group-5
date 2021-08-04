"""
This script is to execute and consolidate the ITCC implementations into one clear interactive shell script.


[Useful article to overcome module import issues](https://towardsdatascience.com/how-to-fix-modulenotfounderror-and-importerror-248ce5b69b1c)
"""


#%%
import pandas as pd
from module3.itcc import ITCC

i = ITCC()
df = i.get_drugbank_artifact()

#%%
df

# %%
# Distribution of ground truth labels
df["DrugBank"].value_counts()
# %%
from module3.ebc.ebc import EBC
from module3.ebc.matrix import SparseMatrix


def get_data(
    resource_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/ebc/resources/matrix-ebc-paper-sparse.tsv",
):
    """Outputs a list in the form:
    ['(rc-160,igf-i)', '[nsubj, reduced, dobj]', 1.0]
    """
    with open(resource_path, "r") as f:
        data = []
        for line in f:
            sl = line.split("\t")
            if len(sl) < 5:  # Skipping less than 5 length tokens
                continue
            data.append([sl[0], sl[2], float(sl[4])])

    return data


data = get_data()

matrix = SparseMatrix(
    [14052, 7272]
)  # want to compress this to 30 and 125 dimensions, whilst preserving as much information as possible
matrix.read_data(data)
matrix.normalize()

#%%
data[0]


#     ebc = EBC(matrix, [30, 125], 10, 1e-10, 0.01)
#     (
#         cXY,
#         objective,
#         it,
#     ) = (
#         ebc.run()

# EBC()


# %%
artifact = i.get_drugbank_artifact()
# %%
artifact["Drug-Gene Pair Cluster"].sort_values()
