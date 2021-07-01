'''
This script is to take the input of biomedical sentences and parse 
them in a format that is readable for the Java Stanford Parser
implementation (as a text file).
'''

#%%
import pandas as pd


# ingesting from CSV

biomedical = pd.read_csv("./data/biomedical_sentences.csv")
biomedical_data = ""
for i in biomedical['Text']:
    biomedical_data+= '\n'+i

# getting a sample
sample = biomedical.sample(100)
sample_data = ""
for i in sample['Text']:
    sample_data += '\n'+i

# Converting the input to txt
# %%
with open("biomedical_output.txt", "w") as text_file:
    text_file.write(biomedical_data)

# %%
with open("sample_data.txt", "w") as text_file:
    text_file.write(sample_data)
