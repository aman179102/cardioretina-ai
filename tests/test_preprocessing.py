"""Tests for image preprocessing pipeline."""

from __future__ import annotations

import numpy as np
from PIL import Image

from cardioretina.data.preprocessing import (
    apply_clahe,
    normalize_image,
    preprocess_image,
    remove_noise,
)


def test_preprocess_image_from_pil():
    """Test full preprocessing pipeline with PIL image."""
    img = Image.fromarray(np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8))
    result = preprocess_image(img, target_size=224)
    assert result.shape == (224, 224, 3)
    assert result.dtype == np.float32
    assert result.min() >= 0.0
    assert result.max() <= 1.0


def test_preprocess_image_from_numpy():
    """Test preprocessing with numpy array input."""
    img = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    result = preprocess_image(img, target_size=224)
    assert result.shape == (224, 224, 3)
    assert result.dtype == np.float32


def test_clahe_preserves_shape():
    """Test CLAHE preserves image dimensions."""
    img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    result = apply_clahe(img)
    assert result.shape == img.shape


def test_normalize_range():
    """Test normalization produces [0, 1] range."""
    img = np.random.randint(50, 200, (100, 100, 3), dtype=np.uint8)
    result = normalize_image(img)
    assert result.min() >= 0.0
    assert result.max() <= 1.0


def test_normalize_constant_image():
    """Test normalization handles constant-value images."""
    img = np.full((100, 100, 3), 128, dtype=np.uint8)
    result = normalize_image(img)
    assert np.allclose(result, 0.0)


def test_remove_noise():
    """Test noise removal preserves shape."""
    img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    result = remove_noise(img)
    assert result.shape == img.shape
