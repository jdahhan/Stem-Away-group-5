'''
Goal: Generate seed set
'''
filepath = "full database.xml"
file = open(filepath, 'r', encoding = "UTF-8")
allpairs = []

for line in file:
    line = line.strip()
    if line.find("<drug type=") != -1:
        newpairs = [f"{currdrug}\t{gene}" for gene in currgenes]
        currdrug = ""
        currgenes = []
        allpairs += newpairs
    if line.find("<name>") != -1 and currdrug == "":
        currdrug = line[6:-7]
    if line.find("<gene-name>") != -1:
        currgenes.append(line[11:-12])
file.close()

outfile = "drugbank_pairs.tsv"
file = open(outfile, "w", encoding='utf-8')
file.write("\n".join(allpairs))
file.close()