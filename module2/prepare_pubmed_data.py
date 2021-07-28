"""
Preparing the data for both the stanford parser
Java implementations and the Jython implementations.

"""
import pandas as pd


class PrepareStanfordParser:
    """Useful functions for pipeline to iterate towards the use of the
    Stanford parser"""

    def __init__(self):
        self.genes = self.get_genes()
        self.drugs = self.get_drugs()

    def get_genes(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/genes/genes.tsv",
    ):
        return list(pd.read_csv(path, delimiter="\t")["Name"])

    def get_drugs(
        self,
        path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/drugs/drugs.tsv",
    ):
        return list(pd.read_csv(path, delimiter="\t")["Name"])

    def tag_drug_gene(self, sent: str) -> tuple:
        """
        Parameters
        =====
        str: biomedical sentence

        Returns
        ========
        (sent, i, j) where i is the set of drug indices and j is the set of gene indices
        """

        tokenized = sent.split(" ")

        drug_indices = []
        gene_indices = []

        for i, token in enumerate(tokenized):
            if token in self.drugs:
                drug_indices.append(i)
            if token in self.genes:
                gene_indices.append(i)

        return (sent, drug_indices, gene_indices)

    def apply_to_all_sentences(self, biomedical_sentences: list) -> list:
        """Getting all the drug indices and tag indices of each of the pubmed sentences"""
        return [self.tag_drug_gene(sent) for sent in biomedical_sentences]

    def parse_to_stanford(self) -> None:
        """Take the input of biomedical sentences CSV and parse
        them in a format that is readable for the Java Stanford Parser
        implementation (as a text file).
        """
        biomedical = pd.read_csv("./data/biomedical_sentences.csv")
        biomedical_data = ""
        for i in biomedical["Text"]:
            biomedical_data += "\n" + i

        # getting a sample
        sample = biomedical.sample(100)
        sample_data = ""
        for i in sample["Text"]:
            sample_data += "\n" + i

        # Converting the input to txt
        with open("biomedical_output.txt", "w") as text_file:
            text_file.write(biomedical_data)

        with open("sample_data.txt", "w") as text_file:
            text_file.write(sample_data)
