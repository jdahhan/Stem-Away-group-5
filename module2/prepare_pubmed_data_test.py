import unittest
from prepare_pubmed_data import PrepareStanfordParser
import pandas as pd


class Test(unittest.TestCase):
    def test_get_gene(self):
        p = PrepareStanfordParser()
        genes = p.get_genes()

        print(genes[:5])

        self.assertIsInstance(genes, list)

    def test_get_drug(self):
        p = PrepareStanfordParser()
        drugs = p.get_drugs()

        print(drugs[:5])

        self.assertIsInstance(drugs, list)

    def test_tag_drug_gene(self):
        p = PrepareStanfordParser()
        example_sent = "The concentration of immunoreactive secretin in portal blood and the secretion from the exocrine pancreas were measured during intraduodenal infusion of isotonic or hypertonic saline, isotonic or hypertonic glucose, aminoacids, fat emulsion, or 0.1 mol X 1(-1) hydrochloric acid in 7 anaesthetized pigs."
        tagged = p.tag_drug_gene(example_sent)

        print(f"Tagged: {tagged}")

    def test_str_contains(self):
        """[Testing Potential Concern in tag_drug_gene function] This test shows that it is okay for the gene representations to
        have spaces even though the tokens that are being compared to are split
        by spaces."""

        s = "actin gamma 1"
        self.assertTrue("actin" in s)

    def test_apply_to_all_sentences(self):
        p = PrepareStanfordParser()

        biomedical_sentences = pd.read_csv(
            "/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/usable_sentences.tsv",
            delimiter="\t",
        ).columns.tolist()

        parsed = p.apply_to_all_sentences(biomedical_sentences)
        print(parsed[:10])


unittest.main()
