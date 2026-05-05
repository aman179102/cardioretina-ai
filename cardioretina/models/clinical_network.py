"""Fully connected network for processing structured clinical data."""

from __future__ import annotations

import torch
import torch.nn as nn


class ClinicalNetwork(nn.Module):
    """Neural network for processing structured clinical health data.

    Processes clinical features (blood pressure, cholesterol, BMI, etc.)
    through dense layers with batch normalization and dropout.

    Architecture: input -> Dense(64, ReLU) -> BN -> Dense(32, ReLU) -> BN -> Dropout(0.3)
    """

    def __init__(
        self,
        num_features: int = 8,
        hidden_dims: list[int] | None = None,
        dropout_rate: float = 0.3,
    ) -> None:
        super().__init__()
        hidden_dims = hidden_dims or [64, 32]

        layers: list[nn.Module] = []
        in_dim = num_features
        for dim in hidden_dims:
            layers.extend([
                nn.Linear(in_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(inplace=True),
            ])
            in_dim = dim

        layers.append(nn.Dropout(p=dropout_rate))
        self.network = nn.Sequential(*layers)
        self.output_dim = hidden_dims[-1]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Process clinical features.

        Args:
            x: Clinical feature tensor of shape (batch, num_features)

        Returns:
            Processed features of shape (batch, output_dim)
        """
        return self.network(x)
