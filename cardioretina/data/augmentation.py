"""Data augmentation transforms for retinal fundus images."""

from __future__ import annotations

import random

import cv2
import numpy as np
import torch
from torchvision import transforms

from cardioretina.data.preprocessing import apply_clahe, apply_gamma_correction


class RetinalAugmentation:
    """Custom augmentation pipeline for retinal fundus images.

    Applies rotation, flipping, gamma correction, and CLAHE
    as described in the research methodology.
    """

    def __init__(
        self,
        rotation_limit: int = 15,
        horizontal_flip: bool = True,
        vertical_flip: bool = True,
        gamma_range: tuple[float, float] = (0.8, 1.2),
        apply_clahe_aug: bool = True,
        clahe_clip_limit: float = 2.0,
        brightness_limit: float = 0.2,
    ) -> None:
        self.rotation_limit = rotation_limit
        self.horizontal_flip = horizontal_flip
        self.vertical_flip = vertical_flip
        self.gamma_range = gamma_range
        self.apply_clahe_aug = apply_clahe_aug
        self.clahe_clip_limit = clahe_clip_limit
        self.brightness_limit = brightness_limit

    def __call__(self, image: np.ndarray) -> np.ndarray:
        """Apply augmentation to a single image (expected as float32 in [0,1])."""
        img = (image * 255).astype(np.uint8) if image.max() <= 1.0 else image.copy()

        if random.random() < 0.5:
            angle = random.uniform(-self.rotation_limit, self.rotation_limit)
            h, w = img.shape[:2]
            matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
            img = cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

        if self.horizontal_flip and random.random() < 0.5:
            img = cv2.flip(img, 1)

        if self.vertical_flip and random.random() < 0.5:
            img = cv2.flip(img, 0)

        if random.random() < 0.3:
            gamma = random.uniform(*self.gamma_range)
            img = apply_gamma_correction(img, gamma)

        if self.apply_clahe_aug and random.random() < 0.3:
            img = apply_clahe(img, clip_limit=self.clahe_clip_limit)

        if random.random() < 0.3:
            factor = 1.0 + random.uniform(-self.brightness_limit, self.brightness_limit)
            img = np.clip(img.astype(np.float32) * factor, 0, 255).astype(np.uint8)

        return img.astype(np.float32) / 255.0


def get_train_transforms(config: dict | None = None) -> transforms.Compose:
    """Get training transforms: augmentation + tensor conversion."""
    cfg = config or {}
    augmenter = RetinalAugmentation(
        rotation_limit=cfg.get("rotation_limit", 15),
        horizontal_flip=cfg.get("horizontal_flip", True),
        vertical_flip=cfg.get("vertical_flip", True),
        gamma_range=cfg.get("gamma_limit", (0.8, 1.2)),
        apply_clahe_aug=cfg.get("apply_clahe", True),
        clahe_clip_limit=cfg.get("clahe_clip_limit", 2.0),
        brightness_limit=cfg.get("brightness_limit", 0.2),
    )

    return transforms.Compose([
        transforms.Lambda(lambda img: augmenter(np.array(img) if not isinstance(img, np.ndarray) else img)),
        transforms.Lambda(lambda img: torch.from_numpy(img).permute(2, 0, 1).float()),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


def get_val_transforms() -> transforms.Compose:
    """Get validation/test transforms: normalization + tensor conversion."""
    return transforms.Compose([
        transforms.Lambda(
            lambda img: (np.array(img).astype(np.float32) / 255.0)
            if not isinstance(img, np.ndarray)
            else img
        ),
        transforms.Lambda(lambda img: torch.from_numpy(img).permute(2, 0, 1).float()),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
