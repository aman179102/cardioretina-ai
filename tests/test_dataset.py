"""Tests for dataset validation and loading."""

from __future__ import annotations

import pandas as pd
import pytest

from cardioretina.data.validate import validate_dataset


@pytest.fixture
def valid_csv(tmp_path):
    """Create a valid dataset CSV for testing."""
    df = pd.DataFrame({
        "image_path": ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"],
        "label": [0, 1, 0, 1],
        "age": [55, 62, 45, 70],
        "systolic_bp": [120, 150, 110, 140],
        "diastolic_bp": [80, 95, 70, 90],
        "cholesterol": [200, 260, 180, 240],
        "bmi": [25, 32, 22, 28],
        "smoking": [0, 1, 0, 1],
        "diabetes": [0, 1, 0, 0],
        "physical_activity": [1, 0, 1, 0],
    })
    csv_path = tmp_path / "dataset.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def invalid_csv(tmp_path):
    """Create a CSV missing required columns."""
    df = pd.DataFrame({"some_column": [1, 2, 3]})
    csv_path = tmp_path / "invalid.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


def test_validate_valid_dataset(valid_csv):
    """Test validation passes for a correct dataset."""
    results = validate_dataset(valid_csv)
    assert results["valid"] is True
    assert results["stats"]["total_samples"] == 4
    assert len(results["stats"]["available_clinical_features"]) == 8


def test_validate_invalid_dataset(invalid_csv):
    """Test validation fails for dataset missing required columns."""
    results = validate_dataset(invalid_csv)
    assert results["valid"] is False
    assert any("image_path" in err for err in results["errors"])


def test_validate_label_distribution(valid_csv):
    """Test label distribution is computed correctly."""
    results = validate_dataset(valid_csv)
    dist = results["stats"]["label_distribution"]
    assert dist["0"] == 2
    assert dist["1"] == 2


def test_validate_nonexistent_file():
    """Test validation raises error for missing file."""
    with pytest.raises(FileNotFoundError):
        validate_dataset("/nonexistent/path.csv")


def test_validate_clinical_summary(valid_csv):
    """Test clinical summary statistics are computed."""
    results = validate_dataset(valid_csv)
    summary = results["stats"]["clinical_summary"]
    assert "age" in summary
    assert "mean" in summary["age"]
    assert "std" in summary["age"]
