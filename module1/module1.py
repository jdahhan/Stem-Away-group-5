#%% imports & initialization
import requests
import pubmed_parser as pp
import pandas as pd
from gzip import decompress
import nltk

nltk.download("punkt")

SIZE = 5 # how many files are we bothering with
parsed_files = []
fnames = ["pubmed21n" + str(num).zfill(4) + ".xml" for num in range(1,1 + SIZE)]
#%% getting + processing files
ftp_url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
for fname in fnames:
    r = requests.get(ftp_url + fname + '.gz')
    print('yoinked')
    data = decompress(r.content)
    print('decompressed')
    medline_data = pd.DataFrame.from_dict(pp.parse_medline_xml(data))
    print('parsed')
    medline_data = medline_data[['abstract', 'pubdate']]
    parsed_files.append(medline_data)
    print('appended')

#%% create dataframe of parsed files
drugs = []
genes = []

df_drug = pd.read_csv('./drugs/drugs.tsv', sep='\t')
df_genes = pd.read_csv('./genes/genes.tsv', sep='\t')

drugs.extend(df_drug["Name"])
genes.extend(df_genes["Name"])

#drug names from DrugBank
drugbank_drug= pd.read_csv('./drugs/drugbank vocabulary.csv')
drugs.extend(drugbank_drug["Common name"])

#%%
pubmed_df = pd.concat(parsed_files, ignore_index=True)
#%% isolate sentences
#pull abstracts <= 2015
abstracts = [pubmed_df['abstract'][i] for i in pubmed_df.index if int(pubmed_df['pubdate'][i]) <= 2015]
sentences = []
for abstract in abstracts:
    sentences += nltk.tokenize.sent_tokenize(abstract)

#%% narrow sentences down to only those with drug-gene relationships
usable_sentences = []
set_drugs = set(drugs)
set_genes = set(genes)

for sentence in sentences:
    drug, gene = False, False
    token_sentence = nltk.tokenize.word_tokenize(sentence)
    for token in token_sentence:
        if token in set_drugs:
            drug = True
        elif token in set_genes:
            gene = True
        if drug and gene:
            usable_sentences.append(sentence)
            break

#%% writing final sentences
file = open("usable_sentences.tsv", "w", encoding='utf-8')
file.write('\t'.join(usable_sentences))
file.close()
print('done')
# %%
# %%
