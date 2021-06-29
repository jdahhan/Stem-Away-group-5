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
print(dependencies)
# %%
setrelations = set()
setpairs = set()
for dependency in dependencies:
    setrelations.add(dependency[0])
    setpairs.add(dependency[1])

relations = list(setrelations)
pairs = list(setpairs)

zeroes = np.zeros(shape=(len(pairs), len(relations)))
matrix = pd.DataFrame(zeroes, index=list(pairs.keys()), columns = list(relations.keys()))
# %%
for dependency in dependencies:
    matrix.at[dependency[1], dependency[0]] += 1
print(matrix)
# %%
