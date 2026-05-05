"""Pydantic schemas for API request/response validation."""

from __future__ import annotations

from pydantic import BaseModel, Field

MEDICAL_DISCLAIMER = (
    "This project is a research prototype for educational and experimental use only. "
    "It is not intended for clinical diagnosis, treatment decisions, or as a substitute "
    "for professional medical advice. Always consult a qualified healthcare professional."
)

MODEL_VERSION = "1.0.0"


class ClinicalData(BaseModel):
    """Clinical health metrics for multimodal prediction."""

    age: float = Field(default=50.0, ge=0, le=120, description="Patient age in years")
    systolic_bp: float = Field(default=120.0, ge=50, le=300, description="Systolic blood pressure (mmHg)")
    diastolic_bp: float = Field(default=80.0, ge=30, le=200, description="Diastolic blood pressure (mmHg)")
    cholesterol: float = Field(default=200.0, ge=50, le=600, description="Total cholesterol (mg/dL)")
    bmi: float = Field(default=25.0, ge=10, le=70, description="Body Mass Index (kg/m^2)")
    smoking: float = Field(default=0.0, ge=0, le=1, description="Smoking status (0=No, 1=Yes)")
    diabetes: float = Field(default=0.0, ge=0, le=1, description="Diabetes status (0=No, 1=Yes)")
    physical_activity: float = Field(default=1.0, ge=0, le=1, description="Physical activity (0=Sedentary, 1=Active)")


class PredictionResponse(BaseModel):
    """Response schema for prediction endpoint."""

    risk_probability: float = Field(description="Heart disease risk probability [0, 1]")
    risk_level: str = Field(description="Risk category: Low / Moderate / High")
    risk_percentage: float = Field(description="Risk as percentage")
    confidence: float = Field(description="Model confidence in the prediction [0, 1]")
    model_version: str = Field(default=MODEL_VERSION, description="Model version identifier")
    clinical_factors: dict[str, str] = Field(default_factory=dict, description="Clinical factor assessments")
    gradcam_url: str | None = Field(default=None, description="URL to Grad-CAM heatmap image")
    top_clinical_contributors: list[str] = Field(
        default_factory=list,
        description="Top contributing clinical factors"
    )
    disclaimer: str = Field(default=MEDICAL_DISCLAIMER, description="Medical disclaimer")


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: str
    model_loaded: bool
    device: str
    version: str


class ModelInfoResponse(BaseModel):
    """Response schema for model information endpoint."""

    model_name: str = "CardioRetina-AI"
    version: str = MODEL_VERSION
    architecture: str = "Hybrid EfficientNet-B3 + Vision Transformer + Clinical Data Fusion"
    input_size: str = "224x224 RGB"
    clinical_features: list[str] = Field(default_factory=lambda: [
        "age", "systolic_bp", "diastolic_bp", "cholesterol",
        "bmi", "smoking", "diabetes", "physical_activity",
    ])
    output: str = "Binary classification - heart disease risk probability [0, 1]"
    backbone: str = "EfficientNet-B3 (ImageNet pretrained)"
    vit_module: str = "ViT-Base-Patch16-224"
    explainability: list[str] = Field(default_factory=lambda: [
        "Grad-CAM heatmap visualization",
        "Clinical feature importance analysis",
    ])
    disclaimer: str = MEDICAL_DISCLAIMER


class MetricsResponse(BaseModel):
    """Response schema for evaluation metrics endpoint."""

    available: bool
    metrics: dict | None = None
    message: str = ""
