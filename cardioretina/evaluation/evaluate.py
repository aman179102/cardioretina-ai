"""Complete evaluation pipeline for CardioRetina-AI model."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from cardioretina.data.augmentation import get_val_transforms
from cardioretina.data.dataset import RetinaDataset
from cardioretina.evaluation.metrics import EvaluationResults, compute_metrics
from cardioretina.evaluation.visualization import (
    plot_confusion_matrix,
    plot_precision_recall_curve,
    plot_roc_curve,
)
from cardioretina.models.hybrid_model import CardioRetinaModel
from cardioretina.utils.config import Config, get_default_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def load_model(
    checkpoint_path: str | Path,
    config: Config,
    device: torch.device,
) -> CardioRetinaModel:
    """Load a trained model from checkpoint."""
    cfg = config.model
    model = CardioRetinaModel(
        backbone=cfg.backbone,
        pretrained=False,
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

    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)
    model.eval()
    return model


@torch.no_grad()
def evaluate_model(
    model: CardioRetinaModel,
    dataloader: DataLoader,
    device: torch.device,
) -> tuple[EvaluationResults, np.ndarray, np.ndarray]:
    """Run evaluation on a dataset and compute all metrics.

    Returns (results, y_true, y_prob) for further plotting.
    """
    model.eval()
    all_labels: list[float] = []
    all_probs: list[float] = []

    for batch in tqdm(dataloader, desc="Evaluating"):
        images = batch["image"].to(device)
        labels = batch["label"]
        clinical = batch.get("clinical")
        if clinical is not None:
            clinical = clinical.to(device)

        outputs = model(images, clinical).squeeze(1)
        all_probs.extend(outputs.cpu().numpy().tolist())
        all_labels.extend(labels.numpy().tolist())

    y_true = np.array(all_labels)
    y_prob = np.array(all_probs)
    y_pred = (y_prob >= 0.5).astype(int)

    results = compute_metrics(y_true, y_pred, y_prob)
    return results, y_true, y_prob


def main() -> None:
    """Entry point for evaluation script."""
    parser = argparse.ArgumentParser(description="Evaluate CardioRetina-AI model")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to model checkpoint")
    parser.add_argument("--config", type=str, help="Path to config YAML file")
    parser.add_argument("--test-csv", type=str, required=True, help="Path to test dataset CSV")
    parser.add_argument("--image-dir", type=str, required=True, help="Path to image directory")
    parser.add_argument("--output-dir", type=str, default="evaluation_results")
    args = parser.parse_args()

    config = Config.from_yaml(args.config) if args.config else get_default_config()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Loading model from: %s", args.checkpoint)
    model = load_model(args.checkpoint, config, device)

    val_transforms = get_val_transforms()
    test_dataset = RetinaDataset(
        args.test_csv,
        image_dir=args.image_dir,
        transform=val_transforms,
        target_size=config.data.image_size,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.training.batch_size,
        shuffle=False,
        num_workers=config.data.num_workers,
    )

    logger.info("Running evaluation...")
    results, y_true, y_prob = evaluate_model(model, test_loader, device)

    logger.info("\n%s", results.summary())
    logger.info("\nClassification Report:\n%s", results.classification_report_str)

    plot_confusion_matrix(results, save_path=output_dir / "confusion_matrix.png")
    plot_roc_curve(results, save_path=output_dir / "roc_curve.png")
    plot_precision_recall_curve(y_true, y_prob, save_path=output_dir / "precision_recall_curve.png")

    results_dict = {
        "accuracy": results.accuracy,
        "precision": results.precision,
        "recall": results.recall,
        "specificity": results.specificity,
        "f1": results.f1,
        "auc_roc": results.auc_roc,
        "classification_report": results.classification_report_str,
    }

    with open(output_dir / "results.json", "w") as f:
        json.dump(results_dict, f, indent=2)

    with open(output_dir / "results.txt", "w") as f:
        f.write(results.summary())
        f.write(f"\n{results.classification_report_str}")

    logger.info("Results saved to: %s", output_dir)


if __name__ == "__main__":
    main()
