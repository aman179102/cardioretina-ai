"""Configuration management for CardioRetina-AI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class DataConfig(BaseModel):
    """Data pipeline configuration."""

    image_size: int = 224
    train_ratio: float = 0.70
    val_ratio: float = 0.15
    test_ratio: float = 0.15
    num_workers: int = 4
    pin_memory: bool = True


class AugmentationConfig(BaseModel):
    """Data augmentation configuration."""

    rotation_limit: int = 15
    horizontal_flip: bool = True
    vertical_flip: bool = True
    brightness_limit: float = 0.2
    contrast_limit: float = 0.2
    gamma_limit: list[float] = Field(default_factory=lambda: [0.8, 1.2])
    apply_clahe: bool = True
    clahe_clip_limit: float = 2.0


class ModelConfig(BaseModel):
    """Model architecture configuration."""

    backbone: str = "efficientnet_b3"
    pretrained: bool = True
    num_clinical_features: int = 8
    clinical_hidden_dims: list[int] = Field(default_factory=lambda: [64, 32])
    fusion_dims: list[int] = Field(default_factory=lambda: [128, 64, 32])
    dropout_rate: float = 0.3
    fusion_dropout_rate: float = 0.4
    use_vit: bool = True
    vit_model: str = "vit_base_patch16_224"
    vit_embed_dim: int = 768
    freeze_backbone_layers: bool = True
    use_clinical: bool = True


class TrainingConfig(BaseModel):
    """Training configuration."""

    batch_size: int = 16
    epochs: int = 50
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    optimizer: str = "adam"
    scheduler: str = "reduce_on_plateau"
    scheduler_patience: int = 5
    scheduler_factor: float = 0.5
    early_stopping_patience: int = 10
    gradient_clip_max_norm: float = 1.0
    mixed_precision: bool = True
    seed: int = 42
    use_class_weights: bool = False


class Config(BaseModel):
    """Root configuration for CardioRetina-AI."""

    data: DataConfig = Field(default_factory=DataConfig)
    augmentation: AugmentationConfig = Field(default_factory=AugmentationConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    output_dir: str = "outputs"
    log_dir: str = "logs"
    checkpoint_dir: str = "checkpoints"

    @classmethod
    def from_yaml(cls, path: str | Path) -> Config:
        """Load configuration from a YAML file."""
        with open(path) as f:
            data: dict[str, Any] = yaml.safe_load(f)
        return cls(**data)

    def to_yaml(self, path: str | Path) -> None:
        """Save configuration to a YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False, sort_keys=False)


def get_default_config() -> Config:
    """Return the default configuration."""
    return Config()
