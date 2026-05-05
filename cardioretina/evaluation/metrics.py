"""Evaluation metrics for CardioRetina-AI model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


@dataclass
class EvaluationResults:
    """Container for model evaluation results."""

    accuracy: float
    precision: float
    recall: float
    specificity: float
    f1: float
    auc_roc: float
    confusion_mat: np.ndarray
    fpr: np.ndarray
    tpr: np.ndarray
    roc_thresholds: np.ndarray
    classification_report_str: str

    def summary(self) -> str:
        """Return a formatted summary of results."""
        return (
            f"Accuracy:    {self.accuracy:.4f}\n"
            f"Precision:   {self.precision:.4f}\n"
            f"Recall:      {self.recall:.4f}\n"
            f"Specificity: {self.specificity:.4f}\n"
            f"F1-Score:    {self.f1:.4f}\n"
            f"AUC-ROC:     {self.auc_roc:.4f}\n"
        )


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
) -> EvaluationResults:
    """Compute comprehensive evaluation metrics.

    Args:
        y_true: Ground truth labels (0 or 1)
        y_pred: Predicted labels (0 or 1)
        y_prob: Predicted probabilities [0, 1]
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    try:
        auc_val = roc_auc_score(y_true, y_prob)
    except ValueError:
        auc_val = 0.0

    fpr, tpr, thresholds = roc_curve(y_true, y_prob)

    report = classification_report(y_true, y_pred, target_names=["Low Risk", "High Risk"])

    return EvaluationResults(
        accuracy=acc,
        precision=prec,
        recall=rec,
        specificity=specificity,
        f1=f1,
        auc_roc=auc_val,
        confusion_mat=cm,
        fpr=fpr,
        tpr=tpr,
        roc_thresholds=thresholds,
        classification_report_str=report,
    )
