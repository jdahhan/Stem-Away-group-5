'''
Implementation of EBC Algorithm


Case 1:
-------
Format we need: (from matrix-ebc-paper-sparse.tsv)
(rc-160,igf-i)	0	[nsubj, reduced, dobj]	1861	1.0


Case 2:
-------

data: each element of the data list should be a list, 
    and should have the following form:
            [feature1, feature2, ..., feature dim, value]

'''

#%%
# with open('../dependency_matrix.txt') as f:
#     matrix = f.readlines()

import pandas as pd

matrix = pd.read_csv('../dependency_matrix.txt', sep = '\t')
matrix.head()


#%%
matrix

#%%
from matrix import SparseMatrix as sm

sm.read_data()
#%%
# input sparse matrix
ebc = EBC(sparse_matrix, n_clusters=[30, 125], max_iterations=10)
cXY, objective, iter = ebc.run()

# output coclusterings

