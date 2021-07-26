'''
Note: This code is still incomplete and the logic needs to still be modified to meet the 
replication requirements of the paper. 

Namely, the dependency path is not represented properly yet. 

'''

#%%
import pandas as pd
import numpy as np

drugs = []
genes = []
parsename = 'sample_dependency_output.txt'

df_drug = pd.read_csv('./drugs/drugs.tsv', sep='\t')
df_genes = pd.read_csv('./genes/genes.tsv', sep='\t')

drugs.extend(df_drug["Name"])
genes.extend(df_genes["Name"])
set_drug = set(drugs)
set_gene = set(genes)
# %%
dependencies = []
infile = open(parsename, 'r')
for line in infile:
    if line[0].islower() and line.find('(') != -1:
        stripline = line[line.find('(') + 1 : line.find(')')]
        stripline = stripline.split(', ')
        for i in range(2):
            stripline[i] = stripline[i][:stripline[i].rfind('-')]
        drug, gene = '', ''
        for word in stripline:
            if word in set_drug:
                drug = word
            elif word in set_gene:
                gene = word
        if drug and gene:
            dependencies.append((line[:line.find('(')], (drug, gene)))

# %%
setrelations = set()
setpairs = set()
for dependency in dependencies:
    setrelations.add(dependency[0])
    setpairs.add(dependency[1])

relations = list(setrelations)
pairs = list(setpairs)

zeroes = np.zeros(shape=(len(pairs), len(relations)))
matrix = pd.DataFrame(zeroes, index = pairs, columns = relations)
# %%
for dependency in dependencies:
    matrix.at[dependency[1], dependency[0]] += 1
# %%
