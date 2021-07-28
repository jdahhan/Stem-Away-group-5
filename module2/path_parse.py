''' This code is the code from Quan's team in an effort
to help our team create the appropriate dependency matrix.
'''

def get_dependency_path(sentence, drug, gene):
    """
    Input: sentence, drug, gene
    Output: dependency path
    """

    import os

    java_path = r'C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe'
    os.environ['JAVAHOME'] = java_path
    os.environ['STANFORD_PARSER'] = r'/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/stanford-parser-full-2014-10-31/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = r'Users/mtaruno/Documents/DevZone/Stem-Away-group-5/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar'
    dependency_parser = stanford.StanfordDependencyParser(path_to_jar=r'Users/mtaruno/Documents/DevZone/Stem-Away-group-5/stanford-parser-full-2014-10-31/stanford-parser.jar', path_to_models_jar=r'Users/mtaruno/Documents/DevZone/Stem-Away-group-5/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar')

    # cover edge case where [] and {} cannot be parsed
    sentence = sentence.replace('[','(').replace(']',')').replace('{','(').replace('}',')')

    try:
        result = dependency_parser.raw_parse(sentence)
        dep = next(result)

    except:
        print(f"Error parsing the following sentence:\n {sentence} \n------------------")
        result = []

    if result == []:
        return []
        
    # make dependency tuple into list
    try:
        dependency_list = []
        for relation in dep.triples():
            temp_list=[]
            for item in relation:
                if type(item).__name__ == 'tuple':
                    temp_list.append(str(item[0]))
                else:
                    temp_list.append(str(item))
            dependency_list.append(temp_list)
    except:
        return []

    # Obtain drug and gene path
    drug_path = []
    gene_path = []
    drug_path_search = []
    gene_path_search = []

    restart_loop = True
    loop_counter = 0
    while restart_loop == True:
        loop_counter += 1
        
        # specific cases where code keeps running while dependency_list is empty
        if len(dependency_list)==0 and loop_counter > 200:
            drug_path = []
            gene_path = []
            break
        
        for i in range(len(dependency_list)):
            relation = dependency_list[i]
            if relation[2] == drug:
                drug_path.append(relation[2])
                drug_path.append(relation[1])
                    drug_path.append(relation[0])
                    drug_path_search = relation[0]
                    dependency_list.pop(i)
                    loop_counter = 0
                    break
                elif relation[2] == drug_path_search:
                    drug_path.append(relation[1])
                    drug_path.append(relation[0])
                    drug_path_search = relation[0]
                    dependency_list.pop(i)
                    loop_counter = 0
                    break
                elif relation[2] == gene:
                    gene_path.append(relation[2])
                    gene_path.append(relation[1])
                    gene_path.append(relation[0])
                    gene_path_search = relation[0]
                    dependency_list.pop(i)
                    loop_counter = 0
                    break
                elif relation[2] == gene_path_search:
                    gene_path.append(relation[1])
                    gene_path.append(relation[0])
                    gene_path_search = relation[0]
                    dependency_list.pop(i)
                    loop_counter = 0
                    break
                elif i == (len(dependency_list)-1):
                    restart_loop = False
                    break

        # Combine drug and gene path into dependency path
        if drug in gene_path:
            ind = gene_path.index(drug)
            dependency_path = gene_path[1:ind]
        elif gene in drug_path:
            ind = drug_path.index(gene)
            dependency_path = drug_path[1:ind][::-1]
        else:
            dependency_path = gene_path[1:] + drug_path[::-1][1:-1]

        return dependency_path


def get_dependency_matrix(abs_filt):
    """
    Input: Dataframe of filtered abstract with columns of abstract, sentence, drug, and gene
    Output: Dependency matrix in the form: dependency_paths, drug_gene_pairs, relation (always 1)
    """

    dependency_matrix = pd.DataFrame(columns = ['dependency_paths','drug_gene_pairs','relation'])
    for i, sentence in enumerate(abs_filt["sentence"]):
        print('-------------------------')
        print(sentence)
        drug = abs_filt["drug"].iloc[i]
        gene = abs_filt["gene"].iloc[i]
        dependency_path = get_dependency_path(sentence, drug, gene)
    #     print(drug)
    #     print(gene)
    #     print('----dependency path----')
    #     print(dependency_path)
    #     print('-----------------------')
        if len(dependency_path) > 0 and dependency_path[0]!='conj':
            drug_gene_pair = drug+'/'+gene
            to_append = [dependency_path,drug_gene_pair,1]
            dependency_matrix = dependency_matrix.append(pd.DataFrame([to_append],columns = ['dependency_paths','drug_gene_pairs','relation']),ignore_index=True)
            print('append to matrix')
    
    print('done')
    return dependency_matrix