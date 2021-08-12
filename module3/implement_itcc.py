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

#%%
df.to_csv("/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/itcc_dense_artifact.csv")
df.head()
#%%
%time
# running EBC algorithm R times
ebc_output = i.run_R_times(R=3)

#%%
import numpy as np

N = df.shape[0]
# initialize coocurrance matrix
matrix = np.full((N, N), 0)

cooccurance_matrix = i.get_cooccurance(ebc_output = ebc_output, matrix = matrix)

#%%

print(str(cooccurance_matrix))

#%%
df["DrugBank"].value_counts()

# %%
# Distribution of ground truth labels
# df["DrugBank"].value_counts()
# %%

#%%


#%%


# %%
artifact = i.get_drugbank_artifact()
artifact["Drug-Gene Pair Cluster"].sort_values()


# %%


# %%
