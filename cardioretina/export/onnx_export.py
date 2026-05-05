"""Export CardioRetina-AI model to ONNX format.

Usage:
    python -m cardioretina.export.onnx_export --checkpoint checkpoints/best_model.pt --output model.onnx
    python -m cardioretina.export.onnx_export --no-checkpoint --output model_pretrained.onnx
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import torch

from cardioretina.models.hybrid_model import CardioRetinaModel
from cardioretina.utils.config import Config, get_default_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_to_onnx(
    checkpoint_path: str | Path | None = None,
    output_path: str | Path = "cardioretina_model.onnx",
    config: Config | None = None,
    opset_version: int = 14,
) -> Path:
    """Export model to ONNX format.

    Args:
        checkpoint_path: Path to model checkpoint (.pt file)
        output_path: Output path for ONNX model
        config: Model configuration
        opset_version: ONNX opset version

    Returns:
        Path to exported ONNX file
    """
    config = config or get_default_config()
    cfg = config.model

    model = CardioRetinaModel(
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
        checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
        model.load_state_dict(checkpoint["model_state_dict"])
        logger.info("Loaded checkpoint: %s", checkpoint_path)

    model.eval()

    dummy_image = torch.randn(1, 3, 224, 224)
    dummy_clinical = torch.randn(1, cfg.num_clinical_features)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    torch.onnx.export(
        model,
        (dummy_image, dummy_clinical),
        str(output_path),
        opset_version=opset_version,
        input_names=["image", "clinical_data"],
        output_names=["risk_probability"],
        dynamic_axes={
            "image": {0: "batch_size"},
            "clinical_data": {0: "batch_size"},
            "risk_probability": {0: "batch_size"},
        },
    )

    logger.info("Model exported to: %s (%.2f MB)", output_path, output_path.stat().st_size / 1e6)
    return output_path


def main() -> None:
    """CLI entry point for ONNX export."""
    parser = argparse.ArgumentParser(description="Export CardioRetina-AI to ONNX")
    parser.add_argument("--checkpoint", type=str, default=None, help="Path to model checkpoint")
    parser.add_argument("--no-checkpoint", action="store_true", help="Export with pretrained backbone only")
    parser.add_argument("--output", type=str, default="cardioretina_model.onnx", help="Output ONNX path")
    parser.add_argument("--config", type=str, default=None, help="Config YAML path")
    parser.add_argument("--opset", type=int, default=14, help="ONNX opset version")
    args = parser.parse_args()

    config = Config.from_yaml(args.config) if args.config else get_default_config()

    checkpoint = None if args.no_checkpoint else args.checkpoint
    export_to_onnx(checkpoint, args.output, config, args.opset)


if __name__ == "__main__":
    main()
