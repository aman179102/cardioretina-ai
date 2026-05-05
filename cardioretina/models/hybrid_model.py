"""Hybrid CNN + ViT model with clinical data fusion for heart disease prediction."""

from __future__ import annotations

import torch
import torch.nn as nn

from cardioretina.models.clinical_network import ClinicalNetwork
from cardioretina.models.efficientnet_backbone import EfficientNetBackbone
from cardioretina.models.vit_module import ViTModule


class FeatureFusionLayer(nn.Module):
    """Fuses features from CNN, ViT, and clinical data streams.

    Concatenates feature vectors from all modalities and processes
    through classification layers with progressive dimensionality reduction.
    """

    def __init__(
        self,
        cnn_dim: int,
        vit_dim: int,
        clinical_dim: int,
        fusion_dims: list[int] | None = None,
        dropout_rates: list[float] | None = None,
    ) -> None:
        super().__init__()
        fusion_dims = fusion_dims or [128, 64, 32]
        dropout_rates = dropout_rates or [0.4, 0.3, 0.3]

        total_dim = cnn_dim + vit_dim + clinical_dim

        layers: list[nn.Module] = []
        in_dim = total_dim
        for i, dim in enumerate(fusion_dims):
            layers.extend([
                nn.Linear(in_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(inplace=True),
                nn.Dropout(p=dropout_rates[i] if i < len(dropout_rates) else 0.3),
            ])
            in_dim = dim

        self.fusion_network = nn.Sequential(*layers)
        self.output_dim = fusion_dims[-1]

    def forward(
        self,
        cnn_features: torch.Tensor,
        vit_features: torch.Tensor,
        clinical_features: torch.Tensor,
    ) -> torch.Tensor:
        """Fuse multi-modal features via concatenation.

        Args:
            cnn_features: CNN output (batch, cnn_dim)
            vit_features: ViT output (batch, vit_dim)
            clinical_features: Clinical network output (batch, clinical_dim)

        Returns:
            Fused features of shape (batch, output_dim)
        """
        fused = torch.cat([cnn_features, vit_features, clinical_features], dim=1)
        return self.fusion_network(fused)


class CardioRetinaModel(nn.Module):
    """Complete hybrid model for heart disease risk prediction.

    Architecture:
        Retinal Image -> [EfficientNet-B3 (CNN)] -> local features
        Retinal Image -> [ViT] -> global features
        Clinical Data  -> [Dense Network] -> clinical features
        [Feature Fusion] -> concatenation -> classification layers
        -> Sigmoid -> probability score [0, 1]
    """

    def __init__(
        self,
        backbone: str = "efficientnet_b3",
        pretrained: bool = True,
        use_vit: bool = True,
        vit_model: str = "vit_base_patch16_224",
        vit_embed_dim: int = 768,
        num_clinical_features: int = 8,
        clinical_hidden_dims: list[int] | None = None,
        fusion_dims: list[int] | None = None,
        dropout_rate: float = 0.3,
        fusion_dropout_rate: float = 0.4,
        freeze_backbone: bool = True,
    ) -> None:
        super().__init__()
        self.use_vit = use_vit

        self.cnn = EfficientNetBackbone(
            model_name=backbone,
            pretrained=pretrained,
            freeze_early_layers=freeze_backbone,
            dropout_rate=dropout_rate,
        )

        if use_vit:
            self.vit = ViTModule(
                model_name=vit_model,
                pretrained=pretrained,
                dropout_rate=dropout_rate,
                embed_dim=vit_embed_dim,
            )
            vit_dim = vit_embed_dim
        else:
            self.vit = None
            vit_dim = 0

        self.clinical_net = ClinicalNetwork(
            num_features=num_clinical_features,
            hidden_dims=clinical_hidden_dims or [64, 32],
            dropout_rate=dropout_rate,
        )

        self.fusion = FeatureFusionLayer(
            cnn_dim=self.cnn.feature_dim,
            vit_dim=vit_dim,
            clinical_dim=self.clinical_net.output_dim,
            fusion_dims=fusion_dims or [128, 64, 32],
            dropout_rates=[fusion_dropout_rate, dropout_rate, dropout_rate],
        )

        self.classifier = nn.Linear(self.fusion.output_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(
        self,
        image: torch.Tensor,
        clinical: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Forward pass for heart disease risk prediction.

        Args:
            image: Retinal fundus image tensor (batch, 3, 224, 224)
            clinical: Clinical features tensor (batch, num_features).
                      If None, zeros are used.

        Returns:
            Risk probability tensor of shape (batch, 1) in [0, 1]
        """
        cnn_features = self.cnn(image)

        if self.use_vit and self.vit is not None:
            vit_features = self.vit(image)
        else:
            vit_features = torch.zeros(
                image.size(0), 0, device=image.device, dtype=image.dtype
            )

        if clinical is None:
            clinical = torch.zeros(
                image.size(0),
                self.clinical_net.network[0].in_features,
                device=image.device,
                dtype=image.dtype,
            )

        clinical_features = self.clinical_net(clinical)

        fused = self.fusion(cnn_features, vit_features, clinical_features)

        logits = self.classifier(fused)
        return self.sigmoid(logits)

    def get_cnn_features(self, image: torch.Tensor) -> torch.Tensor:
        """Extract CNN features only (for Grad-CAM)."""
        return self.cnn(image)
