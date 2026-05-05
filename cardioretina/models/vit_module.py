"""Vision Transformer module for global context learning from retinal images."""

from __future__ import annotations

import timm
import torch
import torch.nn as nn


class ViTModule(nn.Module):
    """Vision Transformer module for capturing global spatial relationships.

    Complements the CNN backbone by analyzing long-range dependencies
    and global structural patterns in retinal images using self-attention.

    The image is divided into patches, each converted to embeddings,
    and the self-attention mechanism learns relationships between patches.
    """

    def __init__(
        self,
        model_name: str = "vit_base_patch16_224",
        pretrained: bool = True,
        dropout_rate: float = 0.3,
        embed_dim: int = 768,
    ) -> None:
        super().__init__()

        self.vit = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,
            global_pool="avg",
        )
        self.feature_dim = embed_dim

        self.projection = nn.Sequential(
            nn.Linear(self.vit.num_features, embed_dim),
            nn.BatchNorm1d(embed_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Extract global features using Vision Transformer.

        Args:
            x: Input tensor of shape (batch, 3, 224, 224)

        Returns:
            Feature vector of shape (batch, embed_dim)
        """
        features = self.vit(x)
        features = self.projection(features)
        return features
