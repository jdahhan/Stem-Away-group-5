


#%%
import pandas as pd
import plotly.express as px

# finding distribution of sentence counts

with open('../data/biomedical_output.txt') as f:
    file = [i.split(" ") for i in f.readlines()]
# %%
lengths = [len(i) for i in file]
# %%
lengths
# %%
# visualizing
import plotly.figure_factory as ff

def distplot(lengths, title = "Distplot", 
    color = 'rgb(0, 200, 200)'):
    hist_data = [lengths]
    group_labels = ['distplot'] # name of the dataset
    fig = ff.create_distplot(hist_data, 
    group_labels, colors = [color])
    fig.update_layout(title_text=title)
    fig.show()

distplot(lengths = lengths, title = "Distribution of Token Lengths in Biomedical Data")
# %%
