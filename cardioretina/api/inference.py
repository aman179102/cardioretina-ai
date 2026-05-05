"""Inference engine for CardioRetina-AI predictions."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from cardioretina.api.schemas import ClinicalData
from cardioretina.data.preprocessing import preprocess_image
from cardioretina.models.hybrid_model import CardioRetinaModel
from cardioretina.utils.config import Config

logger = logging.getLogger(__name__)

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
MAX_UPLOAD_SIZE_MB = 10


class InferenceEngine:
    """Handles model loading and prediction for the API."""

    def __init__(self) -> None:
        self.model: CardioRetinaModel | None = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.config: Config | None = None
        self._is_loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load_model(
        self,
        checkpoint_path: str | Path | None = None,
        config: Config | None = None,
    ) -> None:
        """Load model from checkpoint or create with default weights."""
        self.config = config or Config()
        cfg = self.config.model

        self.model = CardioRetinaModel(
            backbone=cfg.backbone,
            pretrained=cfg.pretrained,
            use_vit=cfg.use_vit,
            vit_model=cfg.vit_model,
            vit_embed_dim=cfg.vit_embed_dim,
            num_clinical_features=cfg.num_clinical_features,
            clinical_hidden_dims=cfg.clinical_hidden_dims,
            fusion_dims=cfg.fusion_dims,
            dropout_rate=cfg.dropout_rate,
            fusion_dropout_rate=cfg.fusion_dropout_rate,
            freeze_backbone=False,
        )

        if checkpoint_path and Path(checkpoint_path).exists():
            checkpoint = torch.load(
                checkpoint_path, map_location=self.device, weights_only=False
            )
            self.model.load_state_dict(checkpoint["model_state_dict"])
            logger.info("Loaded model from checkpoint: %s", checkpoint_path)
        else:
            logger.info("Using model with pretrained backbone weights (no fine-tuned checkpoint)")

        self.model = self.model.to(self.device)
        self.model.eval()
        self._is_loaded = True

    def _prepare_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess image for model input."""
        img_array = preprocess_image(
            image,
            target_size=224,
            apply_clahe_enhancement=True,
        )

        tensor = torch.from_numpy(img_array).permute(2, 0, 1).float()

        for c in range(3):
            tensor[c] = (tensor[c] - IMAGENET_MEAN[c]) / IMAGENET_STD[c]

        return tensor.unsqueeze(0)

    def _prepare_clinical(self, clinical: ClinicalData) -> torch.Tensor:
        """Normalize clinical data for model input."""
        ranges = {
            "age": (0, 120),
            "systolic_bp": (50, 300),
            "diastolic_bp": (30, 200),
            "cholesterol": (50, 600),
            "bmi": (10, 70),
            "smoking": (0, 1),
            "diabetes": (0, 1),
            "physical_activity": (0, 1),
        }

        values = []
        for field_name in [
            "age", "systolic_bp", "diastolic_bp", "cholesterol",
            "bmi", "smoking", "diabetes", "physical_activity",
        ]:
            val = getattr(clinical, field_name)
            lo, hi = ranges[field_name]
            normalized = (val - lo) / (hi - lo) if hi > lo else 0.0
            values.append(normalized)

        return torch.tensor([values], dtype=torch.float32)

    def _assess_clinical_factors(self, clinical: ClinicalData) -> dict[str, str]:
        """Assess individual clinical risk factors based on medical thresholds."""
        factors: dict[str, str] = {}

        if clinical.systolic_bp >= 140 or clinical.diastolic_bp >= 90:
            factors["blood_pressure"] = "High - Hypertension detected"
        elif clinical.systolic_bp >= 120 or clinical.diastolic_bp >= 80:
            factors["blood_pressure"] = "Elevated - Pre-hypertension"
        else:
            factors["blood_pressure"] = "Normal"

        if clinical.cholesterol >= 240:
            factors["cholesterol"] = "High - Hypercholesterolemia"
        elif clinical.cholesterol >= 200:
            factors["cholesterol"] = "Borderline High"
        else:
            factors["cholesterol"] = "Normal"

        if clinical.bmi >= 30:
            factors["bmi"] = "Obese"
        elif clinical.bmi >= 25:
            factors["bmi"] = "Overweight"
        elif clinical.bmi >= 18.5:
            factors["bmi"] = "Normal"
        else:
            factors["bmi"] = "Underweight"

        factors["diabetes"] = "Yes - Increased risk" if clinical.diabetes > 0.5 else "No"
        factors["smoking"] = "Yes - Increased risk" if clinical.smoking > 0.5 else "No"

        if clinical.age >= 65:
            factors["age"] = "Elderly - Higher baseline risk"
        elif clinical.age >= 45:
            factors["age"] = "Middle-aged - Moderate baseline risk"
        else:
            factors["age"] = "Young - Lower baseline risk"

        factors["physical_activity"] = "Active" if clinical.physical_activity > 0.5 else "Sedentary - Increased risk"

        return factors

    def _get_top_contributors(self, factors: dict[str, str]) -> list[str]:
        """Identify top contributing clinical risk factors."""
        risk_keywords = ["High", "Hypertension", "Obese", "Increased risk", "Sedentary", "Elderly"]
        contributors = []
        for name, status in factors.items():
            if any(kw in status for kw in risk_keywords):
                contributors.append(f"{name}: {status}")
        return contributors

    @torch.no_grad()
    def predict(
        self,
        image: Image.Image,
        clinical: ClinicalData | None = None,
    ) -> dict:
        """Run prediction on a retinal image with optional clinical data."""
        if not self._is_loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        img_tensor = self._prepare_image(image).to(self.device)

        clinical_data = clinical or ClinicalData()
        clinical_tensor = self._prepare_clinical(clinical_data).to(self.device)

        output = self.model(img_tensor, clinical_tensor)
        probability = output.item()

        confidence = abs(probability - 0.5) * 2.0

        if probability >= 0.7:
            risk_level = "High"
        elif probability >= 0.4:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        factors = self._assess_clinical_factors(clinical_data)

        return {
            "risk_probability": round(probability, 4),
            "risk_level": risk_level,
            "risk_percentage": round(probability * 100, 2),
            "confidence": round(confidence, 4),
            "clinical_factors": factors,
            "top_clinical_contributors": self._get_top_contributors(factors),
        }

    def generate_gradcam(
        self,
        image: Image.Image,
        clinical: ClinicalData | None = None,
        save_path: str | Path | None = None,
    ) -> np.ndarray | None:
        """Generate Grad-CAM heatmap for the prediction."""
        if not self._is_loaded or self.model is None:
            return None

        from cardioretina.evaluation.gradcam import GradCAM

        target_layer = self.model.cnn.backbone.conv_head
        gradcam = GradCAM(self.model, target_layer)

        img_tensor = self._prepare_image(image).to(self.device)
        clinical_data = clinical or ClinicalData()
        clinical_tensor = self._prepare_clinical(clinical_data).to(self.device)

        heatmap = gradcam.generate(img_tensor, clinical_tensor)

        if save_path:
            original = np.array(image.resize((224, 224))) / 255.0
            gradcam.visualize(original, heatmap, save_path=save_path)

        return heatmap

    @staticmethod
    def validate_upload(filename: str, file_size: int) -> tuple[bool, str]:
        """Validate uploaded file type and size."""
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        if file_size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            return False, f"File too large. Maximum size: {MAX_UPLOAD_SIZE_MB}MB"
        return True, "OK"


engine = InferenceEngine()
