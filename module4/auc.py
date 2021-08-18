"""
This is where I generate the AUC metrics for a given dataset.

Helpful Resource: https://towardsdatascience.com/understanding-the-roc-curve-and-auc-dd4f9a192ecb
"""

from os import setgroups
from module4.ebc_scoring import EBCScoring
from sklearn.metrics import roc_auc_score
import pickle


class AUC:
    def __init__(
        self,
        trials_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/scores/test_sets_2021-08-16,21:27.txt",
        seed_test_sets_path="/Users/mtaruno/Documents/DevZone/Stem-Away-group-5/data/artifacts/scores/seed_test_sets_2021-08-16,21:27.txt",
    ):
        self.ebc = EBCScoring()
        self.trials_path = trials_path
        self.seed_test_sets_path = seed_test_sets_path

    def calculate_TPR(self, TP, FN):
        """Calculates True Positive Rate/Recall/Sensitivity"""
        return (TP) / (TP + FN)

    def calculate_FPR(self, FP, TN):
        """Calculates False Positive Rate"""
        return (FP) / (FP + TN)

    def calculate_TP_FP_rate(self, y_true, y_pred):
        # Instantiate Counters
        TP, FP, TN, FN = 0, 0, 0, 0

        # Calculate TP, FP, TN, FN
        for i in range(len(y_true)):
            if y_true[i] == y_pred[i] == 1:
                TP += 1
            if y_pred[i] == 1 and y_true[i] != y_pred[i]:
                FP += 1
            if y_true[i] == y_pred[i] == 0:
                TN += 1
            if y_pred[i] == 0 and y_true[i] != y_pred[i]:
                FN += 1

        # Calculate TPR and FPR
        tpr = self.calculate_TPR(TP, FN)
        fpr = self.calculate_FPR(FP, TN)

        return tpr, fpr

    def ingest_data(
        self,
        trials_path=None,
        seed_test_sets_path=None,
    ):
        if trials_path is None:
            trials_path = self.trials_path
        if seed_test_sets_path is None:
            seed_test_sets_path = self.seed_test_sets_path

        with open(trials_path, "rb") as fp:  # Unpickling
            trials = pickle.load(fp)
        with open(seed_test_sets_path, "rb") as fp:  # Unpickling
            seed_test_sets = pickle.load(fp)

        return trials, seed_test_sets

    def process_trial_roc(self, trial, test_set):
        """Creates ROC plot for one trial given a trial and a test set."""
        ground_truth = dict(zip(test_set["Drug-Gene"], test_set["DrugBank"]))
        in_drugbank = {i.replace("/", ","): j for i, j in ground_truth.items() if j}

        # Getting lowest and highest scores for the particular run
        start = min(trial.values())
        end = max(trial.values())

        tp_rates = []
        fp_rates = []

        # We are saying for a particular boundary value, if the value is higher,
        for boundary in range(start, end, 1):
            # Split the current testset on the boundary
            y_pred = [1 if j >= boundary else 0 for i, j in trial.items()]
            y_true = [1 if i in in_drugbank else 0 for i, j in trial.items()]
            tpr, fpr = self.calculate_TP_FP_rate(y_true, y_pred)
            tp_rates.append(tpr)
            fp_rates.append(fpr)

        auc = self.calculate_auc_score(fp_rates, tp_rates)

        return tp_rates, fp_rates, auc

    def plot_roc(self, tp_rates, fp_rates, auc, test_set_size: str, trial_number: str):
        import matplotlib.pyplot as plt

        plt.style.use("seaborn")
        lw = 2

        # Plotting the ROC curve
        plt.figure()
        plt.plot(
            fp_rates,
            tp_rates,
            color="darkorange",
            lw=lw,
            label=f"Trial: AUC Score is {round(auc, 3)}",
        )
        plt.plot(
            [0, 1], [0, 1], color="navy", lw=lw, linestyle="--", label="Random Guessing"
        )
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"Trial {trial_number}, Test Set Size: {test_set_size}")
        plt.legend(loc="lower right")
        plt.show()

    def calculate_auc_score(self, fp_rates, tp_rates):
        from sklearn.metrics import auc

        return auc(fp_rates, tp_rates)

    def main(self):
        """Entire walkthrough"""
        trials, seed_test_sets = self.ingest_data()
        test_sets = [i[1] for i in seed_test_sets]  # Getting just the test sets
        seed_sets = [i[0] for i in seed_test_sets]
        auc_scores = []

        for trial_num, (trial, test_set) in enumerate(zip(trials, test_sets), start=1):
            print("Test Set Size: %d" % (len(test_set)))
            tp_rates, fp_rates, auc = self.process_trial_roc(trial, test_set)
            self.plot_roc(
                tp_rates,
                fp_rates,
                auc,
                test_set_size=str(len(test_set)),
                trial_number=str(trial_num),
            )

            auc_scores.append(auc)

        standard = [1 if i > 0.7 else 0 for i in auc_scores]
        proportion = sum(standard) / len(auc_scores)

        print("REPORT")
        print(f"Proportion of trials with AUC > 0.7: {proportion}")

        return [len(i) for i in test_sets], [len(i) for i in seed_sets], auc_scores

    def plot_seed_test_set_sizes(self, seed_set_sizes, test_set_sizes):

        import plotly.figure_factory as ff
        import numpy as np

        group_labels = ["Seed", "Test"]
        colors = ["rgb(0, 0, 100)", "rgb(0, 200, 200)"]

        # Create distplot with custom bin_size
        fig = ff.create_distplot(
            [seed_set_sizes, test_set_sizes], group_labels, colors=colors
        )

        fig.update_layout(
            title_text="Distribution of Seed Sets and Test Sets After 100 EBC Trial Runs"
        )
        fig.show()
