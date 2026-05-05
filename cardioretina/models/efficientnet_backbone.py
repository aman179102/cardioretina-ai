"""EfficientNet-B3 backbone for retinal image feature extraction."""

from __future__ import annotations

import timm
import torch
import torch.nn as nn


class EfficientNetBackbone(nn.Module):
    """EfficientNet-B3 feature extractor for retinal fundus images.

    Uses pretrained ImageNet weights with fine-tuning strategy:
    - Early layers (low-level features like edges/textures) are frozen
    - Deeper layers are trainable for domain-specific pattern learning
    - Global Average Pooling reduces feature maps to 1D vector
    """

    def __init__(
        self,
        model_name: str = "efficientnet_b3",
        pretrained: bool = True,
        freeze_early_layers: bool = True,
        dropout_rate: float = 0.3,
    ) -> None:
        super().__init__()

        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,
            global_pool="avg",
        )
        self.feature_dim = self.backbone.num_features

        if freeze_early_layers:
            self._freeze_early_layers()

        self.dropout = nn.Dropout(p=dropout_rate)
        self.batch_norm = nn.BatchNorm1d(self.feature_dim)

    def _freeze_early_layers(self) -> None:
        """Freeze the first ~60% of backbone parameters (early conv layers)."""
        all_params = list(self.backbone.parameters())
        freeze_count = int(len(all_params) * 0.6)
        for param in all_params[:freeze_count]:
            param.requires_grad = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Extract features from retinal image.

        Args:
            x: Input tensor of shape (batch, 3, 224, 224)

        Returns:
            Feature vector of shape (batch, feature_dim)
        """
        features = self.backbone(x)
        features = self.batch_norm(features)
        features = self.dropout(features)
        return features
