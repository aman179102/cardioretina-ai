"""Dataset classes for retinal fundus images with clinical data."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset

from cardioretina.data.preprocessing import preprocess_image

CLINICAL_FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "cholesterol",
    "bmi",
    "smoking",
    "diabetes",
    "physical_activity",
]


class RetinaDataset(Dataset):
    """Dataset for retinal fundus images with optional clinical metadata.

    Expects a CSV file with columns:
        - image_path: relative or absolute path to retinal image
        - label: 0 (low risk) or 1 (high risk)
        - Optional clinical columns matching CLINICAL_FEATURES
    """

    def __init__(
        self,
        csv_path: str | Path,
        image_dir: str | Path | None = None,
        transform: Callable | None = None,
        target_size: int = 224,
        apply_clahe_enhancement: bool = True,
        clinical_features: list[str] | None = None,
    ) -> None:
        self.df = pd.read_csv(csv_path)
        self.image_dir = Path(image_dir) if image_dir else None
        self.transform = transform
        self.target_size = target_size
        self.apply_clahe = apply_clahe_enhancement
        self.clinical_features = clinical_features or CLINICAL_FEATURES

        self._available_clinical = [
            col for col in self.clinical_features if col in self.df.columns
        ]
        if self._available_clinical:
            self._impute_clinical_data()

    def _impute_clinical_data(self) -> None:
        """Handle missing values in clinical data.

        Continuous variables: median imputation
        Categorical variables: mode imputation
        """
        continuous_cols = ["age", "systolic_bp", "diastolic_bp", "cholesterol", "bmi"]
        categorical_cols = ["smoking", "diabetes", "physical_activity"]

        for col in self._available_clinical:
            if col in continuous_cols:
                self.df[col] = self.df[col].fillna(self.df[col].median())
            elif col in categorical_cols:
                mode_val = self.df[col].mode()
                self.df[col] = self.df[col].fillna(mode_val.iloc[0] if len(mode_val) > 0 else 0)

        for col in self._available_clinical:
            if col in continuous_cols:
                col_min = self.df[col].min()
                col_max = self.df[col].max()
                if col_max - col_min > 0:
                    self.df[col] = (self.df[col] - col_min) / (col_max - col_min)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        row = self.df.iloc[idx]

        img_path = row["image_path"]
        if self.image_dir:
            img_path = self.image_dir / img_path

        image = Image.open(img_path).convert("RGB")
        image = preprocess_image(
            image,
            target_size=self.target_size,
            apply_clahe_enhancement=self.apply_clahe,
        )

        if self.transform:
            image = self.transform(image)
        else:
            image = torch.from_numpy(image).permute(2, 0, 1).float()

        label = torch.tensor(float(row["label"]), dtype=torch.float32)

        result: dict[str, Any] = {"image": image, "label": label}

        if self._available_clinical:
            clinical = torch.tensor(
                row[self._available_clinical].values.astype(np.float32),
                dtype=torch.float32,
            )
            result["clinical"] = clinical

        return result


def create_data_splits(
    csv_path: str | Path,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split dataset into train/validation/test sets with stratification."""
    df = pd.read_csv(csv_path)
    from sklearn.model_selection import train_test_split

    train_df, temp_df = train_test_split(
        df, test_size=(1 - train_ratio), random_state=seed, stratify=df["label"]
    )

    relative_val = val_ratio / (1 - train_ratio)
    val_df, test_df = train_test_split(
        temp_df, test_size=(1 - relative_val), random_state=seed, stratify=temp_df["label"]
    )

    return train_df, val_df, test_df
