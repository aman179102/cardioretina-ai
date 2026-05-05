"""Dataset validation and statistics for CardioRetina-AI."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["image_path", "label"]
CLINICAL_COLUMNS = [
    "age", "systolic_bp", "diastolic_bp", "cholesterol",
    "bmi", "smoking", "diabetes", "physical_activity",
]


def validate_dataset(csv_path: str | Path, image_dir: str | Path | None = None) -> dict:
    """Validate dataset CSV and return statistics.

    Checks for:
    - Required columns (image_path, label)
    - Label values (binary 0/1)
    - Missing values per column
    - Image file existence (if image_dir provided)
    - Clinical column availability and ranges

    Returns dict with validation results and statistics.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    results: dict = {"valid": True, "errors": [], "warnings": [], "stats": {}}

    results["stats"]["total_samples"] = len(df)
    results["stats"]["columns"] = list(df.columns)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            results["valid"] = False
            results["errors"].append(f"Missing required column: '{col}'")

    if not results["valid"]:
        return results

    unique_labels = df["label"].dropna().unique()
    invalid_labels = [v for v in unique_labels if v not in [0, 1, 0.0, 1.0]]
    if invalid_labels:
        results["valid"] = False
        results["errors"].append(
            f"Invalid label values found: {invalid_labels}. Expected 0 or 1."
        )

    label_counts = df["label"].value_counts().to_dict()
    results["stats"]["label_distribution"] = {str(int(k)): int(v) for k, v in label_counts.items()}

    total = len(df)
    pos = int(df["label"].sum())
    neg = total - pos
    if total > 0:
        ratio = max(pos, neg) / max(min(pos, neg), 1)
        results["stats"]["class_imbalance_ratio"] = round(ratio, 2)
        if ratio > 3.0:
            results["warnings"].append(
                f"Class imbalance detected (ratio {ratio:.1f}:1). "
                "Consider using class weights or oversampling."
            )

    missing = df.isnull().sum().to_dict()
    results["stats"]["missing_values"] = {k: int(v) for k, v in missing.items() if v > 0}

    available_clinical = [c for c in CLINICAL_COLUMNS if c in df.columns]
    results["stats"]["available_clinical_features"] = available_clinical
    results["stats"]["missing_clinical_features"] = [
        c for c in CLINICAL_COLUMNS if c not in df.columns
    ]

    if available_clinical:
        clinical_stats = {}
        for col in available_clinical:
            s = df[col].describe()
            clinical_stats[col] = {
                "mean": round(float(s["mean"]), 2),
                "std": round(float(s["std"]), 2),
                "min": round(float(s["min"]), 2),
                "max": round(float(s["max"]), 2),
                "missing": int(df[col].isnull().sum()),
            }
        results["stats"]["clinical_summary"] = clinical_stats

    if image_dir:
        image_dir = Path(image_dir)
        missing_images = []
        for _, row in df.iterrows():
            img_path = image_dir / row["image_path"]
            if not img_path.exists():
                missing_images.append(str(row["image_path"]))
        if missing_images:
            results["warnings"].append(
                f"{len(missing_images)} image(s) not found in {image_dir}"
            )
            results["stats"]["missing_images_count"] = len(missing_images)
            results["stats"]["missing_images_sample"] = missing_images[:5]

    return results


def print_report(results: dict) -> None:
    """Print a formatted validation report."""
    print("\n" + "=" * 60)
    print("  CardioRetina-AI Dataset Validation Report")
    print("=" * 60)

    status = "PASSED" if results["valid"] else "FAILED"
    print(f"\nStatus: {status}")

    stats = results["stats"]
    print(f"\nTotal samples: {stats['total_samples']}")
    print(f"Columns: {', '.join(stats['columns'])}")

    if "label_distribution" in stats:
        print("\nLabel distribution:")
        for label, count in stats["label_distribution"].items():
            pct = count / stats["total_samples"] * 100
            print(f"  Class {label}: {count} ({pct:.1f}%)")

    if "class_imbalance_ratio" in stats:
        print(f"  Imbalance ratio: {stats['class_imbalance_ratio']}:1")

    if "available_clinical_features" in stats:
        print(f"\nClinical features available: {len(stats['available_clinical_features'])}")
        for feat in stats["available_clinical_features"]:
            print(f"  - {feat}")
        if stats["missing_clinical_features"]:
            print(f"Missing clinical features: {', '.join(stats['missing_clinical_features'])}")

    if results["errors"]:
        print("\nErrors:")
        for err in results["errors"]:
            print(f"  [ERROR] {err}")

    if results["warnings"]:
        print("\nWarnings:")
        for warn in results["warnings"]:
            print(f"  [WARN] {warn}")

    print("=" * 60)


def main() -> None:
    """CLI entry point for dataset validation."""
    parser = argparse.ArgumentParser(description="Validate CardioRetina-AI dataset")
    parser.add_argument("csv_path", type=str, help="Path to dataset CSV")
    parser.add_argument("--image-dir", type=str, help="Path to image directory")
    parser.add_argument("--output-json", type=str, help="Save results as JSON")
    args = parser.parse_args()

    results = validate_dataset(args.csv_path, args.image_dir)
    print_report(results)

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output_json}")

    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()
