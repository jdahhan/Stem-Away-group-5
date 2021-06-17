#%% imports & initialization
import requests
import pubmed_parser as pp
import pandas as pd
from gzip import decompress
import nltk
nltk.download()

SIZE = 2 # how many files are we bothering with
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
pubmed_df = pd.concat(parsed_files, ignore_index=True)
#%% isolate sentences
#pull abstracts <= 2015
abstracts = [pubmed_df['abstract'][i] for i in pubmed_df.index if int(pubmed_df['pubdate'][i]) <= 2015]
sentences = []
for abstract in abstracts:
    sentences += nltk.tokenize.sent_tokenize(abstract)
#%% narrow sentences down to only those with drug-gene relationships
usable_sentences = []

#NO IDEA WHERE TO GET THESE
drugs = []
genes = []

for sentence in sentences:
    token_sentence = set(nltk.tokenize.word_tokenize(sentence))
    for drug in drugs:
        if drug in sentence:
            for gene in genes:
                if gene in sentence:
                    usable_sentences.append(sentence)

sentences = usable_sentences
#%% writing final sentences
file = open("usable_sentences.tsv", "w")
file.write('\t'.join(sentences))
file.close()
print('done')