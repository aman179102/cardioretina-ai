"""Visualization tools for model evaluation and interpretability."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import precision_recall_curve

from cardioretina.evaluation.metrics import EvaluationResults


def plot_confusion_matrix(
    results: EvaluationResults,
    save_path: str | Path | None = None,
) -> plt.Figure:
    """Plot confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        results.confusion_mat,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Low Risk", "High Risk"],
        yticklabels=["Low Risk", "High Risk"],
        ax=ax,
    )
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig


def plot_roc_curve(
    results: EvaluationResults,
    save_path: str | Path | None = None,
) -> plt.Figure:
    """Plot ROC curve with AUC score."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(
        results.fpr,
        results.tpr,
        color="darkorange",
        lw=2,
        label=f"ROC curve (AUC = {results.auc_roc:.4f})",
    )
    ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Random")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver Operating Characteristic (ROC) Curve")
    ax.legend(loc="lower right")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig


def plot_precision_recall_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    save_path: str | Path | None = None,
) -> plt.Figure:
    """Plot Precision-Recall curve."""
    precision, recall, _ = precision_recall_curve(y_true, y_prob)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(recall, precision, color="steelblue", lw=2, label="Precision-Recall")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve")
    ax.legend(loc="lower left")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig


def plot_training_history(
    history: dict[str, list[float]],
    save_dir: str | Path | None = None,
) -> tuple[plt.Figure, plt.Figure]:
    """Plot training/validation accuracy and loss curves as separate figures."""
    epochs = range(1, len(history["train_loss"]) + 1)

    fig_acc, ax_acc = plt.subplots(figsize=(8, 5))
    ax_acc.plot(epochs, history["train_acc"], "b-o", markersize=3, label="Training Accuracy")
    ax_acc.plot(epochs, history["val_acc"], "r-o", markersize=3, label="Validation Accuracy")
    ax_acc.set_xlabel("Epoch")
    ax_acc.set_ylabel("Accuracy")
    ax_acc.set_title("Training vs Validation Accuracy")
    ax_acc.legend()
    ax_acc.grid(True, alpha=0.3)
    plt.tight_layout()

    fig_loss, ax_loss = plt.subplots(figsize=(8, 5))
    ax_loss.plot(epochs, history["train_loss"], "b-o", markersize=3, label="Training Loss")
    ax_loss.plot(epochs, history["val_loss"], "r-o", markersize=3, label="Validation Loss")
    ax_loss.set_xlabel("Epoch")
    ax_loss.set_ylabel("Loss")
    ax_loss.set_title("Training vs Validation Loss")
    ax_loss.legend()
    ax_loss.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig_acc.savefig(save_dir / "training_accuracy.png", dpi=150, bbox_inches="tight")
        fig_loss.savefig(save_dir / "training_loss.png", dpi=150, bbox_inches="tight")

    plt.close(fig_acc)
    plt.close(fig_loss)
    return fig_acc, fig_loss


def plot_metrics_comparison(
    model_names: list[str],
    accuracies: list[float],
    auc_scores: list[float],
    save_path: str | Path | None = None,
) -> plt.Figure:
    """Plot performance comparison between different models."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    x = np.arange(len(model_names))
    width = 0.35

    axes[0].bar(x, accuracies, width, color="steelblue")
    axes[0].set_xlabel("Model")
    axes[0].set_ylabel("Accuracy (%)")
    axes[0].set_title("Model Accuracy Comparison")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(model_names, rotation=45, ha="right")

    axes[1].bar(x, auc_scores, width, color="coral")
    axes[1].set_xlabel("Model")
    axes[1].set_ylabel("AUC-ROC")
    axes[1].set_title("Model AUC-ROC Comparison")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(model_names, rotation=45, ha="right")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig
