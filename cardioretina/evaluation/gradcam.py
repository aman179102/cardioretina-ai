"""Grad-CAM visualization for model interpretability.

Generates heatmaps highlighting retinal regions that contribute
most to the heart disease risk prediction.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn import functional as func


class GradCAM:
    """Gradient-weighted Class Activation Mapping for the CNN backbone.

    Highlights important retinal regions (vascular structures, optic disc,
    microvascular damage areas) that influence prediction.
    """

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module) -> None:
        self.model = model
        self.target_layer = target_layer

        self.gradients: torch.Tensor | None = None
        self.activations: torch.Tensor | None = None

        self._register_hooks()

    def _register_hooks(self) -> None:
        def forward_hook(module: torch.nn.Module, input: tuple, output: torch.Tensor) -> None:
            self.activations = output.detach()

        def backward_hook(module: torch.nn.Module, grad_input: tuple, grad_output: tuple) -> None:
            self.gradients = grad_output[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate(
        self,
        image: torch.Tensor,
        clinical: torch.Tensor | None = None,
    ) -> np.ndarray:
        """Generate Grad-CAM heatmap for an input image.

        Args:
            image: Preprocessed image tensor (1, 3, H, W)
            clinical: Clinical features tensor (1, num_features)

        Returns:
            Heatmap array of shape (H, W) in [0, 1]
        """
        self.model.eval()
        image.requires_grad_(True)

        output = self.model(image, clinical)
        self.model.zero_grad()
        output.backward()

        if self.gradients is None or self.activations is None:
            raise RuntimeError("Hooks did not capture gradients/activations")

        weights = self.gradients.mean(dim=[2, 3], keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = func.relu(cam)

        cam = func.interpolate(cam, size=image.shape[2:], mode="bilinear", align_corners=False)
        cam = cam.squeeze().cpu().numpy()

        cam_min = cam.min()
        cam_max = cam.max()
        if cam_max - cam_min > 0:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = np.zeros_like(cam)

        return cam

    def visualize(
        self,
        image: np.ndarray,
        heatmap: np.ndarray,
        alpha: float = 0.4,
        save_path: str | Path | None = None,
    ) -> plt.Figure:
        """Overlay Grad-CAM heatmap on original image.

        Args:
            image: Original image as numpy array (H, W, 3) in [0, 1]
            heatmap: Grad-CAM heatmap (H, W) in [0, 1]
            alpha: Overlay opacity
            save_path: Optional path to save the visualization
        """
        heatmap_colored = cv2.applyColorMap(
            (heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET
        )
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB) / 255.0

        if image.max() > 1.0:
            image = image / 255.0

        overlay = alpha * heatmap_colored + (1 - alpha) * image

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        axes[0].imshow(image)
        axes[0].set_title("Original Retinal Image")
        axes[0].axis("off")

        axes[1].imshow(heatmap, cmap="jet")
        axes[1].set_title("Grad-CAM Heatmap")
        axes[1].axis("off")

        axes[2].imshow(np.clip(overlay, 0, 1))
        axes[2].set_title("Grad-CAM Overlay")
        axes[2].axis("off")

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig
