"""Tests for Grad-CAM functionality."""

from __future__ import annotations

import numpy as np
import torch

from cardioretina.evaluation.gradcam import GradCAM
from cardioretina.models.hybrid_model import CardioRetinaModel


def test_gradcam_generate():
    """Test Grad-CAM generates heatmap of correct shape."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    target_layer = model.cnn.backbone.conv_head
    gradcam = GradCAM(model, target_layer)

    image = torch.randn(1, 3, 224, 224)
    clinical = torch.randn(1, 8)
    heatmap = gradcam.generate(image, clinical)

    assert isinstance(heatmap, np.ndarray)
    assert heatmap.shape == (224, 224)
    assert heatmap.min() >= 0
    assert heatmap.max() <= 1


def test_gradcam_without_clinical():
    """Test Grad-CAM works without clinical data."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    target_layer = model.cnn.backbone.conv_head
    gradcam = GradCAM(model, target_layer)

    image = torch.randn(1, 3, 224, 224)
    heatmap = gradcam.generate(image, None)

    assert isinstance(heatmap, np.ndarray)
    assert heatmap.shape == (224, 224)


def test_gradcam_visualize():
    """Test Grad-CAM visualization creates figure."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    target_layer = model.cnn.backbone.conv_head
    gradcam = GradCAM(model, target_layer)

    image = torch.randn(1, 3, 224, 224)
    heatmap = gradcam.generate(image, None)

    original = np.random.rand(224, 224, 3)
    fig = gradcam.visualize(original, heatmap)
    assert fig is not None
