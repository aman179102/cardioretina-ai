"""Image preprocessing utilities for retinal fundus images."""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).

    Enhances local contrast in retinal images to improve visibility
    of vascular structures.
    """
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l_channel = lab[:, :, 0]
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        lab[:, :, 0] = clahe.apply(l_channel)
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)


def apply_gamma_correction(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """Apply gamma correction to simulate different lighting conditions."""
    inv_gamma = 1.0 / gamma
    table = np.array(
        [(i / 255.0) ** inv_gamma * 255 for i in range(256)]
    ).astype(np.uint8)
    return cv2.LUT(image, table)


def remove_noise(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Remove noise using Gaussian blur."""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Min-max normalize pixel values to [0, 1] range."""
    img_float = image.astype(np.float32)
    x_min = img_float.min()
    x_max = img_float.max()
    if x_max - x_min == 0:
        return np.zeros_like(img_float)
    return (img_float - x_min) / (x_max - x_min)


def preprocess_image(
    image: Image.Image | np.ndarray,
    target_size: int = 224,
    apply_clahe_enhancement: bool = True,
    clahe_clip_limit: float = 2.0,
    denoise: bool = True,
) -> np.ndarray:
    """Full preprocessing pipeline for a retinal fundus image.

    Steps:
    1. Convert to numpy RGB array
    2. Resize to target_size x target_size
    3. Denoise with Gaussian blur
    4. Apply CLAHE for contrast enhancement
    5. Normalize to [0, 1]
    """
    if isinstance(image, Image.Image):
        image = np.array(image.convert("RGB"))

    image = cv2.resize(image, (target_size, target_size), interpolation=cv2.INTER_LANCZOS4)

    if denoise:
        image = remove_noise(image)

    if apply_clahe_enhancement:
        image = apply_clahe(image, clip_limit=clahe_clip_limit)

    image = normalize_image(image)
    return image
