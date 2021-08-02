"""
This script is to execute and consolidate the ITCC implementations into one clear interactive shell script.
"""


#%%
import pandas as pd
import importlib

importlib.reload(module3.itcc)
from module3.itcc import ITCC

i = ITCC()
path_matrix = i.get_path_matrix()
pair_cluster, path_cluster = i.getCXY()

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


#%%

drugbank = pd.read_csv(
    "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/module4/drugbank_pairs.tsv",
    delimiter="\t",
    header=None,
)
drugbank.columns = ["Drug", "Gene"]
# parsing to appropriate format
text_parse = [
    f"({drug},{gene})" for drug, gene in zip(drugbank["Drug"], drugbank["Gene"])
]
# %%
text_parse
# %%
df
# %%
exists = [i in text_parse for i in df["druggene_pair"]]
# %%
sum(exists)
# %%
df["druggene_pair"]
# %%
