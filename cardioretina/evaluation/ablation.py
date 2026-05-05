"""Ablation study comparing model configurations.

Compares: CNN-only, ViT-only, CNN+ViT, CNN+ViT+Clinical
Outputs markdown table and JSON results.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from cardioretina.data.augmentation import get_val_transforms
from cardioretina.data.dataset import RetinaDataset
from cardioretina.evaluation.metrics import EvaluationResults, compute_metrics
from cardioretina.models.hybrid_model import CardioRetinaModel
from cardioretina.utils.config import Config, get_default_config

logger = logging.getLogger(__name__)

ABLATION_CONFIGS = {
    "CNN Only (EfficientNet-B3)": {
        "use_vit": False,
        "use_clinical": False,
    },
    "ViT Only": {
        "use_vit": True,
        "use_clinical": False,
        "use_cnn": False,
    },
    "CNN + ViT": {
        "use_vit": True,
        "use_clinical": False,
    },
    "CNN + ViT + Clinical": {
        "use_vit": True,
        "use_clinical": True,
    },
}


def build_model_for_ablation(
    config: Config,
    ablation_name: str,
    ablation_cfg: dict,
) -> CardioRetinaModel:
    """Build model with specific ablation configuration."""
    cfg = config.model
    use_vit = ablation_cfg.get("use_vit", True)
    num_clinical = cfg.num_clinical_features if ablation_cfg.get("use_clinical", True) else 0

    model = CardioRetinaModel(
        backbone=cfg.backbone,
        pretrained=cfg.pretrained,
        use_vit=use_vit,
        vit_model=cfg.vit_model,
        vit_embed_dim=cfg.vit_embed_dim,
        num_clinical_features=max(num_clinical, 1),
        clinical_hidden_dims=cfg.clinical_hidden_dims,
        fusion_dims=cfg.fusion_dims,
        dropout_rate=cfg.dropout_rate,
        fusion_dropout_rate=cfg.fusion_dropout_rate,
        freeze_backbone=cfg.freeze_backbone_layers,
    )
    return model


@torch.no_grad()
def evaluate_ablation(
    model: CardioRetinaModel,
    dataloader: DataLoader,
    device: torch.device,
    use_clinical: bool = True,
) -> EvaluationResults:
    """Evaluate a model variant on the test set."""
    model.eval()
    all_labels: list[float] = []
    all_probs: list[float] = []

    for batch in dataloader:
        images = batch["image"].to(device)
        labels = batch["label"]
        clinical = batch.get("clinical")

        if not use_clinical:
            clinical = None
        elif clinical is not None:
            clinical = clinical.to(device)

        outputs = model(images, clinical).squeeze(1)
        all_probs.extend(outputs.cpu().numpy().tolist())
        all_labels.extend(labels.numpy().tolist())

    y_true = np.array(all_labels)
    y_prob = np.array(all_probs)
    y_pred = (y_prob >= 0.5).astype(int)

    return compute_metrics(y_true, y_pred, y_prob)


def generate_ablation_table(results: dict[str, dict]) -> str:
    """Generate a markdown table of ablation results."""
    header = "| Model Configuration | Accuracy | Precision | Recall | F1-Score | AUC-ROC |"
    sep = "|---|---|---|---|---|---|"
    rows = [header, sep]

    for name, metrics in results.items():
        row = (
            f"| {name} | "
            f"{metrics['accuracy']:.4f} | "
            f"{metrics['precision']:.4f} | "
            f"{metrics['recall']:.4f} | "
            f"{metrics['f1']:.4f} | "
            f"{metrics['auc_roc']:.4f} |"
        )
        rows.append(row)

    return "\n".join(rows)


def run_ablation_study(
    test_csv: str | Path,
    image_dir: str | Path,
    checkpoint_dir: str | Path | None = None,
    config: Config | None = None,
    output_dir: str | Path = "ablation_results",
) -> dict[str, dict]:
    """Run complete ablation study.

    If checkpoint_dir contains checkpoints for each variant, loads them.
    Otherwise, evaluates with pretrained-only weights (for pipeline validation).
    """
    config = config or get_default_config()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    val_transforms = get_val_transforms()
    test_dataset = RetinaDataset(
        test_csv,
        image_dir=str(image_dir),
        transform=val_transforms,
        target_size=config.data.image_size,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.training.batch_size,
        shuffle=False,
        num_workers=0,
    )

    all_results: dict[str, dict] = {}

    for name, ablation_cfg in ABLATION_CONFIGS.items():
        logger.info("Evaluating: %s", name)

        model = build_model_for_ablation(config, name, ablation_cfg)

        if checkpoint_dir:
            ckpt_name = name.lower().replace(" ", "_").replace("+", "_")
            ckpt_path = Path(checkpoint_dir) / f"{ckpt_name}_best.pt"
            if ckpt_path.exists():
                checkpoint = torch.load(ckpt_path, map_location=device, weights_only=False)
                model.load_state_dict(checkpoint["model_state_dict"])

        model = model.to(device)
        use_clinical = ablation_cfg.get("use_clinical", True)
        results = evaluate_ablation(model, test_loader, device, use_clinical)

        all_results[name] = {
            "accuracy": results.accuracy,
            "precision": results.precision,
            "recall": results.recall,
            "specificity": results.specificity,
            "f1": results.f1,
            "auc_roc": results.auc_roc,
        }

    table = generate_ablation_table(all_results)
    print("\n" + table)

    with open(output_dir / "ablation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    with open(output_dir / "ablation_results.md", "w") as f:
        f.write("# Ablation Study Results\n\n")
        f.write(table)
        f.write("\n")

    logger.info("Ablation results saved to %s", output_dir)
    return all_results


def main() -> None:
    """CLI entry point for ablation study."""
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Run ablation study")
    parser.add_argument("--test-csv", type=str, required=True)
    parser.add_argument("--image-dir", type=str, required=True)
    parser.add_argument("--checkpoint-dir", type=str, default=None)
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default="ablation_results")
    args = parser.parse_args()

    config = Config.from_yaml(args.config) if args.config else get_default_config()
    run_ablation_study(
        args.test_csv, args.image_dir, args.checkpoint_dir, config, args.output_dir
    )


if __name__ == "__main__":
    main()
