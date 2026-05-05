"""Train/val/test splitting script with class imbalance handling."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def split_dataset(
    csv_path: str | Path,
    output_dir: str | Path,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> dict[str, int]:
    """Split dataset CSV into train/val/test with stratification.

    Returns dict with split sizes.
    """
    df = pd.read_csv(csv_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if "label" not in df.columns:
        raise ValueError("CSV must contain a 'label' column")

    train_df, temp_df = train_test_split(
        df, test_size=(1 - train_ratio), random_state=seed, stratify=df["label"]
    )

    relative_val = val_ratio / (1 - train_ratio)
    val_df, test_df = train_test_split(
        temp_df, test_size=(1 - relative_val), random_state=seed, stratify=temp_df["label"]
    )

    train_df.to_csv(output_dir / "train.csv", index=False)
    val_df.to_csv(output_dir / "val.csv", index=False)
    test_df.to_csv(output_dir / "test.csv", index=False)

    sizes = {
        "train": len(train_df),
        "val": len(val_df),
        "test": len(test_df),
    }

    print("Split complete:")
    for name, size in sizes.items():
        pct = size / len(df) * 100
        print(f"  {name}: {size} samples ({pct:.1f}%)")
    print(f"Saved to {output_dir}/")

    return sizes


def compute_class_weights(csv_path: str | Path) -> dict[int, float]:
    """Compute inverse-frequency class weights for imbalanced datasets.

    Returns dict mapping class label to weight.
    """
    df = pd.read_csv(csv_path)
    counts = df["label"].value_counts()
    total = len(df)
    weights = {}
    for label, count in counts.items():
        weights[int(label)] = total / (len(counts) * count)
    return weights


def main() -> None:
    """CLI entry point for dataset splitting."""
    parser = argparse.ArgumentParser(description="Split CardioRetina-AI dataset")
    parser.add_argument("csv_path", type=str, help="Path to dataset CSV")
    parser.add_argument("--output-dir", type=str, default="data/splits", help="Output directory")
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    split_dataset(
        args.csv_path,
        args.output_dir,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )

    weights = compute_class_weights(args.csv_path)
    print(f"\nClass weights (for handling imbalance): {weights}")

    sys.exit(0)


if __name__ == "__main__":
    main()
