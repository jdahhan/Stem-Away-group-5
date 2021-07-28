#%%
import os
import nltk
from nltk.parse import stanford
#%%
java_path = r'C:\ProgramData\Oracle\Java\javapath\java.exe'
os.environ['JAVAHOME'] = java_path
os.environ['STANFORD_PARSER'] = r'C:\Users\jdahh\Documents\STEMAWAY\project\Stem-Away-group-5\stanford-parser-full-2014-10-31\stanfordparser.jar'
os.environ['STANFORD_MODELS'] = r'C:\Users\jdahh\Documents\STEMAWAY\project\Stem-Away-group-5\stanford-parser-full-2014-10-31\stanfordparser-3.5.0-models.jar'
#%%
dependency_parser = stanford.StanfordDependencyParser(path_to_jar=r'C:\Users\jdahh\Documents\STEMAWAY\project\Stem-Away-group-5\stanford-parser-full-2014-10-31\stanford-parser.jar', path_to_models_jar=r'C:\Users\jdahh\Documents\STEMAWAY\project\Stem-Away-group-5\stanford-parser-full-2014-10-31\stanford-parser-3.5.0-models.jar')
#%%
sentence = "CYP3A4 mRNA expression was significantly increased by rifampicin exposure in human hepatocytes."
result = dependency_parser.raw_parse(sentence)
#%%
dep = next(result)
print(list(dep.triples()))
print(type(result))
# %%
def find_path(sentence, drug, gene):
    result = dependency_parser.raw_parse(sentence)
    currnode = #find(drug)
    queue = [currnode]
    path = []
    while queue:
        currnode = queue.pop(0)[0]
        for #child in currnode.children:
            if child == gene:
                return path
            else:
                queue.append((child, path + [child]))