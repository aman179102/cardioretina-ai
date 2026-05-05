"""FastAPI application for CardioRetina-AI inference service."""

from __future__ import annotations

import json
import logging
import os
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from cardioretina.api.inference import engine
from cardioretina.api.schemas import (
    ClinicalData,
    HealthResponse,
    MetricsResponse,
    ModelInfoResponse,
    PredictionResponse,
)
from cardioretina.utils.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
GRADCAM_DIR = Path("gradcam_outputs")
GRADCAM_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Load model on startup."""
    checkpoint_path = os.environ.get("MODEL_CHECKPOINT", None)
    config_path = os.environ.get("MODEL_CONFIG", None)
    config = Config.from_yaml(config_path) if config_path else Config()
    try:
        engine.load_model(checkpoint_path=checkpoint_path, config=config)
        logger.info("Model loaded successfully on %s", engine.device)
    except Exception as e:
        logger.error("Failed to load model: %s", e)
        logger.info("Server starting without model - predictions will use pretrained backbone")
        engine.load_model(config=config)
    yield


app = FastAPI(
    title="CardioRetina-AI",
    description=(
        "Deep learning system for non-invasive heart disease risk prediction "
        "using retinal fundus images with CNN and Vision Transformer analysis. "
        "DISCLAIMER: This is a research prototype for educational use only. "
        "Not intended for clinical diagnosis."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

cors_origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Serve the frontend application."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text())
    return HTMLResponse(
        content="<h1>CardioRetina-AI API</h1><p>Visit <a href='/docs'>/docs</a> for API documentation.</p>"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=engine.is_loaded,
        device=str(engine.device),
        version="1.0.0",
    )


@app.get("/model-info", response_model=ModelInfoResponse)
async def model_info() -> ModelInfoResponse:
    """Return model architecture and configuration details."""
    return ModelInfoResponse()


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics() -> MetricsResponse:
    """Return evaluation metrics if available."""
    results_path = Path("evaluation_results/results.json")
    if results_path.exists():
        with open(results_path) as f:
            metrics = json.load(f)
        return MetricsResponse(
            available=True,
            metrics=metrics,
            message="Evaluation results from the most recent evaluation run.",
        )
    return MetricsResponse(
        available=False,
        message="No evaluation results available. Run evaluation pipeline first.",
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(..., description="Retinal fundus image (JPEG/PNG)"),
    age: float = Form(default=50.0),
    systolic_bp: float = Form(default=120.0),
    diastolic_bp: float = Form(default=80.0),
    cholesterol: float = Form(default=200.0),
    bmi: float = Form(default=25.0),
    smoking: float = Form(default=0.0),
    diabetes: float = Form(default=0.0),
    physical_activity: float = Form(default=1.0),
    generate_gradcam: bool = Form(default=False),
) -> PredictionResponse:
    """Predict heart disease risk from retinal fundus image."""
    file_content = await file.read()

    valid, msg = engine.validate_upload(file.filename or "", len(file_content))
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    import io
    image = Image.open(io.BytesIO(file_content)).convert("RGB")

    clinical = ClinicalData(
        age=age,
        systolic_bp=systolic_bp,
        diastolic_bp=diastolic_bp,
        cholesterol=cholesterol,
        bmi=bmi,
        smoking=smoking,
        diabetes=diabetes,
        physical_activity=physical_activity,
    )

    result = engine.predict(image, clinical)

    gradcam_url = None
    if generate_gradcam:
        gradcam_id = str(uuid.uuid4())
        gradcam_path = GRADCAM_DIR / f"{gradcam_id}.png"
        try:
            engine.generate_gradcam(image, clinical, save_path=gradcam_path)
            gradcam_url = f"/gradcam/{gradcam_id}"
        except Exception as e:
            logger.warning("Grad-CAM generation failed: %s", e)

    return PredictionResponse(
        risk_probability=result["risk_probability"],
        risk_level=result["risk_level"],
        risk_percentage=result["risk_percentage"],
        confidence=result["confidence"],
        clinical_factors=result["clinical_factors"],
        top_clinical_contributors=result["top_clinical_contributors"],
        gradcam_url=gradcam_url,
    )


@app.get("/gradcam/{gradcam_id}")
async def get_gradcam(gradcam_id: str) -> FileResponse:
    """Retrieve a generated Grad-CAM visualization."""
    safe_id = gradcam_id.replace("/", "").replace("\\", "").replace("..", "")
    path = GRADCAM_DIR / f"{safe_id}.png"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Grad-CAM not found")
    return FileResponse(path, media_type="image/png")


def start() -> None:
    """Start the API server."""
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    uvicorn.run(
        "cardioretina.api.app:app",
        host=host,
        port=port,
        reload=os.environ.get("ENVIRONMENT", "development") == "development",
    )


if __name__ == "__main__":
    start()
