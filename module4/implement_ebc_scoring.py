#%%
import pandas as pd
from module4.ebc_scoring import EBCScoring
from module3.itcc import ITCC


e = EBCScoring(seed_set_size=10, itcc=ITCC())
artifact = e.get_dense_itcc_artifact()
# seedsets, testsets = e.get_N_data(N=10)

seed, test = e.get_seed_and_test_sets(
    artifact=e.get_dense_itcc_artifact(), sample_size=10
)

df = e.generate_filtered_matrix(test["Drug-Gene"])

print(seed)

scoring = e.generate_ebc_scoring_artifact(
    filtered_matrix=df, seed_pairs=seed["Drug-Gene"]
)

sum(scoring["SeedSet"])


# h = df.T.to_dict("list")

# h.keys()


#%%

df.sort_values()
#%%
test_pairs = list(test["Drug-Gene"].apply(lambda x: x.replace("/", ",")))
matrix = e.get_cooccurance()
mask = [i in test_pairs for i in matrix.index]
matrix[mask]


#%%
sum(mask)
#%%
# Checking to see if the seedsets and testsets produced have the correct drugbank relationships
[(i["DrugBank"].sum(), i.shape[0]) for i in seedsets]


#%%
[(i["DrugBank"].sum(), i.shape[0]) for i in testsets]


#%%
testsets[0]["drug-gene"]
#%%
matrix = e.get_cooccurance()


# %%
e.generate_filtered_matrix(test_set_pairs=list(test["Drug-Gene"]))

#%%
test

#%%

a = e.get_dense_itcc_artifact()
m = e.get_cooccurance()

#%%
a["Drug-Gene"]

#%%

mask = [*map(lambda x: x.replace(",", "/"), m.index)]


#%%
coocurance_pairs = list(e.get_cooccurance().index)
# %%
coocurance_pairs
# %%
test["Drug-Gene"]

# %%
