"""Tests for model components and forward pass."""

from __future__ import annotations

import torch

from cardioretina.models.clinical_network import ClinicalNetwork
from cardioretina.models.efficientnet_backbone import EfficientNetBackbone
from cardioretina.models.hybrid_model import CardioRetinaModel, FeatureFusionLayer


def test_clinical_network_forward():
    """Test clinical network produces correct output shape."""
    net = ClinicalNetwork(num_features=8, hidden_dims=[64, 32])
    x = torch.randn(4, 8)
    out = net(x)
    assert out.shape == (4, 32)


def test_clinical_network_single_sample():
    """Test clinical network with single sample."""
    net = ClinicalNetwork(num_features=8, hidden_dims=[64, 32])
    net.eval()
    x = torch.randn(1, 8)
    out = net(x)
    assert out.shape == (1, 32)


def test_fusion_layer():
    """Test feature fusion layer concatenates and processes features."""
    fusion = FeatureFusionLayer(cnn_dim=128, vit_dim=64, clinical_dim=32)
    fusion.eval()
    cnn = torch.randn(2, 128)
    vit = torch.randn(2, 64)
    clinical = torch.randn(2, 32)
    out = fusion(cnn, vit, clinical)
    assert out.shape == (2, fusion.output_dim)


def test_cardioretina_model_with_vit():
    """Test full model with ViT enabled."""
    model = CardioRetinaModel(pretrained=False, use_vit=True)
    model.eval()
    x = torch.randn(1, 3, 224, 224)
    c = torch.randn(1, 8)
    out = model(x, c)
    assert out.shape == (1, 1)
    assert 0 <= out.item() <= 1


def test_cardioretina_model_no_vit():
    """Test model without ViT (CNN-only mode)."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    x = torch.randn(1, 3, 224, 224)
    c = torch.randn(1, 8)
    out = model(x, c)
    assert out.shape == (1, 1)
    assert 0 <= out.item() <= 1


def test_cardioretina_model_no_clinical():
    """Test model without clinical data."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    x = torch.randn(1, 3, 224, 224)
    out = model(x, None)
    assert out.shape == (1, 1)
    assert 0 <= out.item() <= 1


def test_model_output_range():
    """Test model output is always in [0, 1] range (sigmoid)."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    for _ in range(5):
        x = torch.randn(1, 3, 224, 224)
        c = torch.randn(1, 8)
        out = model(x, c)
        assert 0 <= out.item() <= 1


def test_model_batch_forward():
    """Test model with batch of samples."""
    model = CardioRetinaModel(pretrained=False, use_vit=False)
    model.eval()
    x = torch.randn(4, 3, 224, 224)
    c = torch.randn(4, 8)
    out = model(x, c)
    assert out.shape == (4, 1)


def test_efficientnet_backbone_feature_dim():
    """Test EfficientNet backbone reports correct feature dimension."""
    backbone = EfficientNetBackbone(pretrained=False)
    assert backbone.feature_dim > 0
    backbone.eval()
    x = torch.randn(1, 3, 224, 224)
    out = backbone(x)
    assert out.shape == (1, backbone.feature_dim)
