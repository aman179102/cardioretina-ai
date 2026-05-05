"""SHAP analysis for feature importance in clinical data."""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import shap
import torch

logger = logging.getLogger(__name__)


class SHAPAnalyzer:
    """SHAP-based feature importance analysis for clinical features.

    Analyzes which clinical features (BMI, blood pressure, cholesterol, etc.)
    contribute most to the heart disease risk prediction.
    """

    def __init__(
        self,
        model: torch.nn.Module,
        feature_names: list[str] | None = None,
    ) -> None:
        self.model = model
        self.feature_names = feature_names or [
            "Age",
            "Systolic BP",
            "Diastolic BP",
            "Cholesterol",
            "BMI",
            "Smoking",
            "Diabetes",
            "Physical Activity",
        ]

    def _predict_fn(
        self,
        clinical_data: np.ndarray,
        dummy_image: torch.Tensor,
    ) -> np.ndarray:
        """Wrapper for SHAP that predicts using clinical data with a fixed image."""
        self.model.eval()
        device = next(self.model.parameters()).device

        with torch.no_grad():
            clinical_tensor = torch.tensor(clinical_data, dtype=torch.float32).to(device)
            batch_image = dummy_image.repeat(clinical_data.shape[0], 1, 1, 1).to(device)
            outputs = self.model(batch_image, clinical_tensor)

        return outputs.cpu().numpy().squeeze(-1)

    def analyze(
        self,
        clinical_data: np.ndarray,
        background_data: np.ndarray,
        dummy_image: torch.Tensor,
        max_samples: int = 100,
    ) -> shap.Explanation:
        """Run SHAP analysis on clinical features.

        Args:
            clinical_data: Clinical features to explain (n_samples, n_features)
            background_data: Background dataset for SHAP (n_background, n_features)
            dummy_image: A representative image tensor (1, 3, 224, 224)
            max_samples: Maximum samples to use for explanation
        """
        def predict_fn(x: np.ndarray) -> np.ndarray:
            return self._predict_fn(x, dummy_image)

        background = background_data[:min(50, len(background_data))]
        explainer = shap.KernelExplainer(predict_fn, background)

        data_to_explain = clinical_data[:max_samples]
        shap_values = explainer.shap_values(data_to_explain)

        return shap.Explanation(
            values=shap_values,
            base_values=explainer.expected_value,
            data=data_to_explain,
            feature_names=self.feature_names[: clinical_data.shape[1]],
        )

    def plot_summary(
        self,
        shap_values: shap.Explanation,
        save_path: str | Path | None = None,
    ) -> plt.Figure:
        """Create SHAP summary plot showing feature importance."""
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.summary_plot(
            shap_values.values,
            shap_values.data,
            feature_names=shap_values.feature_names,
            show=False,
        )
        plt.title("Clinical Feature Importance (SHAP Values)")
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig

    def plot_bar(
        self,
        shap_values: shap.Explanation,
        save_path: str | Path | None = None,
    ) -> plt.Figure:
        """Create SHAP bar plot of mean absolute feature importance."""
        fig, ax = plt.subplots(figsize=(10, 6))
        mean_abs = np.abs(shap_values.values).mean(axis=0)
        sorted_idx = np.argsort(mean_abs)

        feature_names = shap_values.feature_names or self.feature_names
        ax.barh(
            range(len(sorted_idx)),
            mean_abs[sorted_idx],
            color="steelblue",
        )
        ax.set_yticks(range(len(sorted_idx)))
        ax.set_yticklabels([feature_names[i] for i in sorted_idx])
        ax.set_xlabel("Mean |SHAP Value|")
        ax.set_title("Clinical Feature Importance")
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig
