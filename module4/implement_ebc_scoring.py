#%%
import pandas as pd
from module4.ebc_scoring import EBCScoring
from module3.itcc import ITCC


e = EBCScoring(seed_set_size=10, itcc=ITCC())
e.get_itcc_artifact()


#%%
seedsets, testsets = e.get_N_data(N=10)


#%%
# Checking to see if the seedsets and testsets produced have the correct drugbank relationships
[(i["DrugBank"].sum(), i.shape[0]) for i in seedsets]
#%%
[(i["DrugBank"].sum(), i.shape[0]) for i in testsets]


#%%
testsets[0]["drug-gene"]
#%%
matrix = e.get_cooccurance()

matrix.shape
