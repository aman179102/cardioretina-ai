"""Tests for configuration management."""

from __future__ import annotations

import tempfile
from pathlib import Path

from cardioretina.utils.config import Config, get_default_config


def test_default_config():
    """Test default configuration values."""
    config = get_default_config()
    assert config.data.image_size == 224
    assert config.model.backbone == "efficientnet_b3"
    assert config.model.use_vit is True
    assert config.model.use_clinical is True
    assert config.training.batch_size == 16
    assert config.training.epochs == 50
    assert config.training.seed == 42


def test_config_yaml_roundtrip():
    """Test saving and loading config from YAML preserves values."""
    config = get_default_config()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yaml"
        config.to_yaml(path)
        loaded = Config.from_yaml(path)
    assert loaded.data.image_size == config.data.image_size
    assert loaded.model.backbone == config.model.backbone
    assert loaded.training.learning_rate == config.training.learning_rate


def test_model_config_ablation_flags():
    """Test model config supports ablation flags."""
    config = get_default_config()
    assert hasattr(config.model, "use_vit")
    assert hasattr(config.model, "use_clinical")
    config.model.use_vit = False
    config.model.use_clinical = False
    assert config.model.use_vit is False
    assert config.model.use_clinical is False


def test_training_config_class_weights():
    """Test training config has class weights option."""
    config = get_default_config()
    assert hasattr(config.training, "use_class_weights")
    assert config.training.use_class_weights is False
