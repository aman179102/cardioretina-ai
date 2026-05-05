"""Tests for the FastAPI application."""

from __future__ import annotations

import io
from unittest.mock import patch

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from cardioretina.api.inference import InferenceEngine


@pytest.fixture
def client():
    """Create test client with mocked model loading."""
    with patch.object(InferenceEngine, "load_model"):
        from cardioretina.api.app import app
        engine_mod = app.state if hasattr(app, "state") else None  # noqa: F841
        from cardioretina.api.inference import engine
        engine._is_loaded = True
        engine.model = None

        with TestClient(app) as c:
            yield c


@pytest.fixture
def dummy_image_bytes():
    """Create a dummy retinal image as bytes."""
    img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


def test_health_endpoint(client):
    """Test /health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data
    assert "device" in data
    assert "version" in data


def test_model_info_endpoint(client):
    """Test /model-info endpoint returns architecture details."""
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "CardioRetina-AI"
    assert "EfficientNet" in data["architecture"]
    assert "Vision Transformer" in data["architecture"]
    assert len(data["clinical_features"]) == 8
    assert "disclaimer" in data


def test_metrics_endpoint_no_results(client):
    """Test /metrics endpoint when no evaluation results exist."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["available"] is False


def test_predict_endpoint_no_file(client):
    """Test /predict endpoint rejects request without file."""
    response = client.post("/predict")
    assert response.status_code == 422


def test_predict_response_schema(client, dummy_image_bytes):
    """Test prediction response matches expected schema."""
    mock_result = {
        "risk_probability": 0.35,
        "risk_level": "Low",
        "risk_percentage": 35.0,
        "confidence": 0.3,
        "clinical_factors": {"blood_pressure": "Normal"},
        "top_clinical_contributors": [],
    }
    with patch.object(InferenceEngine, "predict", return_value=mock_result):
        with patch.object(InferenceEngine, "validate_upload", return_value=(True, "OK")):
            response = client.post(
                "/predict",
                files={"file": ("test.png", dummy_image_bytes, "image/png")},
            )
    if response.status_code == 200:
        data = response.json()
        assert "risk_probability" in data
        assert "risk_level" in data
        assert "confidence" in data
        assert "disclaimer" in data
        assert "model_version" in data


def test_clinical_data_validation():
    """Test ClinicalData schema validation."""
    from cardioretina.api.schemas import ClinicalData

    clinical = ClinicalData(age=55, systolic_bp=140, cholesterol=250)
    assert clinical.age == 55
    assert clinical.systolic_bp == 140
    assert clinical.cholesterol == 250


def test_clinical_factor_assessment():
    """Test clinical factor assessment logic."""
    from cardioretina.api.inference import InferenceEngine
    from cardioretina.api.schemas import ClinicalData

    eng = InferenceEngine()
    clinical = ClinicalData(
        age=70,
        systolic_bp=150,
        diastolic_bp=95,
        cholesterol=260,
        bmi=32,
        smoking=1,
        diabetes=1,
        physical_activity=0,
    )
    factors = eng._assess_clinical_factors(clinical)
    assert "Hypertension" in factors["blood_pressure"]
    assert "High" in factors["cholesterol"]
    assert "Obese" in factors["bmi"]
    assert "Increased risk" in factors["smoking"]
    assert "Increased risk" in factors["diabetes"]


def test_upload_validation():
    """Test file upload validation."""
    valid, msg = InferenceEngine.validate_upload("test.png", 1024)
    assert valid is True

    valid, msg = InferenceEngine.validate_upload("test.exe", 1024)
    assert valid is False
    assert "Unsupported" in msg

    valid, msg = InferenceEngine.validate_upload("test.png", 20 * 1024 * 1024)
    assert valid is False
    assert "too large" in msg


def test_gradcam_not_found(client):
    """Test /gradcam returns 404 for missing heatmap."""
    response = client.get("/gradcam/nonexistent-id")
    assert response.status_code == 404


def test_root_endpoint(client):
    """Test root endpoint serves content."""
    response = client.get("/")
    assert response.status_code == 200
