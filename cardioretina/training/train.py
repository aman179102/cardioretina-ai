"""Training pipeline for CardioRetina-AI model."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
import torch.nn as nn
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader
from tqdm import tqdm

from cardioretina.data.augmentation import get_train_transforms, get_val_transforms
from cardioretina.data.dataset import RetinaDataset, create_data_splits
from cardioretina.models.hybrid_model import CardioRetinaModel
from cardioretina.utils.config import Config, get_default_config
from cardioretina.utils.seed import set_seed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class EarlyStopping:
    """Early stopping to terminate training when validation loss stops improving."""

    def __init__(self, patience: int = 10, min_delta: float = 1e-4) -> None:
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss: float | None = None
        self.should_stop = False

    def __call__(self, val_loss: float) -> bool:
        if self.best_loss is None:
            self.best_loss = val_loss
            return False

        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
                return True
        return False


class Trainer:
    """Training manager for the CardioRetina-AI model."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info("Using device: %s", self.device)

        set_seed(config.training.seed)

        self.model = self._build_model()
        self.criterion = nn.BCELoss()
        self.optimizer = self._build_optimizer()
        self.scheduler = self._build_scheduler()
        self.early_stopping = EarlyStopping(
            patience=config.training.early_stopping_patience
        )
        self.scaler = GradScaler(enabled=config.training.mixed_precision)

        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.history: dict[str, list[float]] = {
            "train_loss": [],
            "val_loss": [],
            "train_acc": [],
            "val_acc": [],
            "learning_rate": [],
        }

    def _build_model(self) -> CardioRetinaModel:
        cfg = self.config.model
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
            freeze_backbone=cfg.freeze_backbone_layers,
        )
        return model.to(self.device)

    def _build_optimizer(self) -> torch.optim.Optimizer:
        cfg = self.config.training
        trainable_params = filter(lambda p: p.requires_grad, self.model.parameters())

        if cfg.optimizer == "adam":
            return torch.optim.Adam(
                trainable_params, lr=cfg.learning_rate, weight_decay=cfg.weight_decay
            )
        elif cfg.optimizer == "adamw":
            return torch.optim.AdamW(
                trainable_params, lr=cfg.learning_rate, weight_decay=cfg.weight_decay
            )
        elif cfg.optimizer == "sgd":
            return torch.optim.SGD(
                trainable_params,
                lr=cfg.learning_rate,
                momentum=0.9,
                weight_decay=cfg.weight_decay,
            )
        else:
            raise ValueError(f"Unsupported optimizer: {cfg.optimizer}")

    def _build_scheduler(self) -> torch.optim.lr_scheduler.LRScheduler:
        cfg = self.config.training
        if cfg.scheduler == "reduce_on_plateau":
            return torch.optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer,
                mode="min",
                factor=cfg.scheduler_factor,
                patience=cfg.scheduler_patience,
            )
        elif cfg.scheduler == "cosine":
            return torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=cfg.epochs
            )
        else:
            return torch.optim.lr_scheduler.StepLR(
                self.optimizer, step_size=10, gamma=0.5
            )

    def train_epoch(self, dataloader: DataLoader) -> tuple[float, float]:
        """Run one training epoch."""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for batch in tqdm(dataloader, desc="Training", leave=False):
            images = batch["image"].to(self.device)
            labels = batch["label"].to(self.device)
            clinical = batch.get("clinical")
            if clinical is not None:
                clinical = clinical.to(self.device)

            self.optimizer.zero_grad()

            with autocast(enabled=self.config.training.mixed_precision):
                outputs = self.model(images, clinical).squeeze(1)
                loss = self.criterion(outputs, labels)

            self.scaler.scale(loss).backward()

            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                self.config.training.gradient_clip_max_norm,
            )

            self.scaler.step(self.optimizer)
            self.scaler.update()

            total_loss += loss.item() * images.size(0)
            predictions = (outputs >= 0.5).float()
            correct += (predictions == labels).sum().item()
            total += labels.size(0)

        avg_loss = total_loss / total
        accuracy = correct / total
        return avg_loss, accuracy

    @torch.no_grad()
    def validate(self, dataloader: DataLoader) -> tuple[float, float]:
        """Run validation."""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        for batch in tqdm(dataloader, desc="Validating", leave=False):
            images = batch["image"].to(self.device)
            labels = batch["label"].to(self.device)
            clinical = batch.get("clinical")
            if clinical is not None:
                clinical = clinical.to(self.device)

            outputs = self.model(images, clinical).squeeze(1)
            loss = self.criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)
            predictions = (outputs >= 0.5).float()
            correct += (predictions == labels).sum().item()
            total += labels.size(0)

        avg_loss = total_loss / total
        accuracy = correct / total
        return avg_loss, accuracy

    def save_checkpoint(self, epoch: int, val_loss: float, is_best: bool = False) -> None:
        """Save model checkpoint."""
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "val_loss": val_loss,
            "config": self.config.model_dump(),
        }

        path = self.checkpoint_dir / f"checkpoint_epoch_{epoch}.pt"
        torch.save(checkpoint, path)

        if is_best:
            best_path = self.checkpoint_dir / "best_model.pt"
            torch.save(checkpoint, best_path)
            logger.info("Saved best model (val_loss=%.4f)", val_loss)

    def _save_history(self) -> None:
        """Save training history as JSON and CSV."""
        json_path = self.output_dir / "training_history.json"
        with open(json_path, "w") as f:
            json.dump(self.history, f, indent=2)

        csv_path = self.output_dir / "training_history.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["epoch", "train_loss", "val_loss", "train_acc", "val_acc", "learning_rate"])
            for i in range(len(self.history["train_loss"])):
                writer.writerow([
                    i + 1,
                    self.history["train_loss"][i],
                    self.history["val_loss"][i],
                    self.history["train_acc"][i],
                    self.history["val_acc"][i],
                    self.history["learning_rate"][i] if i < len(self.history["learning_rate"]) else "",
                ])

    def _save_experiment_log(self, elapsed: float, best_val_loss: float) -> None:
        """Save experiment metadata for reproducibility."""
        log = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "config": self.config.model_dump(),
            "device": str(self.device),
            "total_epochs": len(self.history["train_loss"]),
            "best_val_loss": best_val_loss,
            "final_train_loss": self.history["train_loss"][-1] if self.history["train_loss"] else None,
            "final_val_acc": self.history["val_acc"][-1] if self.history["val_acc"] else None,
            "training_time_seconds": round(elapsed, 2),
            "pytorch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
        }
        log_path = self.output_dir / "experiment_log.json"
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)

    def train(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
    ) -> dict[str, list[float]]:
        """Full training loop with history export."""
        best_val_loss = float("inf")

        self.config.to_yaml(self.output_dir / "config_snapshot.yaml")

        logger.info("Starting training for %d epochs", self.config.training.epochs)
        start_time = time.time()

        for epoch in range(1, self.config.training.epochs + 1):
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate(val_loader)

            current_lr = self.optimizer.param_groups[0]["lr"]

            self.history["train_loss"].append(train_loss)
            self.history["val_loss"].append(val_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_acc"].append(val_acc)
            self.history["learning_rate"].append(current_lr)

            is_best = val_loss < best_val_loss
            if is_best:
                best_val_loss = val_loss

            self.save_checkpoint(epoch, val_loss, is_best=is_best)

            if isinstance(
                self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau
            ):
                self.scheduler.step(val_loss)
            else:
                self.scheduler.step()

            logger.info(
                "Epoch %d/%d - Train Loss: %.4f, Train Acc: %.4f, "
                "Val Loss: %.4f, Val Acc: %.4f, LR: %.6f",
                epoch,
                self.config.training.epochs,
                train_loss,
                train_acc,
                val_loss,
                val_acc,
                current_lr,
            )

            if self.early_stopping(val_loss):
                logger.info("Early stopping triggered at epoch %d", epoch)
                break

        elapsed = time.time() - start_time
        logger.info("Training completed in %.1f seconds", elapsed)
        logger.info("Best validation loss: %.4f", best_val_loss)

        self._save_history()
        self._save_experiment_log(elapsed, best_val_loss)

        return self.history


def main() -> None:
    """Entry point for training script."""
    parser = argparse.ArgumentParser(description="Train CardioRetina-AI model")
    parser.add_argument("--config", type=str, help="Path to config YAML file")
    parser.add_argument("--data-csv", type=str, required=True, help="Path to dataset CSV")
    parser.add_argument("--image-dir", type=str, required=True, help="Path to image directory")
    parser.add_argument("--epochs", type=int, default=None, help="Override number of epochs")
    parser.add_argument("--batch-size", type=int, default=None, help="Override batch size")
    parser.add_argument("--lr", type=float, default=None, help="Override learning rate")
    args = parser.parse_args()

    config = Config.from_yaml(args.config) if args.config else get_default_config()

    if args.epochs:
        config.training.epochs = args.epochs
    if args.batch_size:
        config.training.batch_size = args.batch_size
    if args.lr:
        config.training.learning_rate = args.lr

    config.to_yaml(Path(config.output_dir) / "config.yaml")

    logger.info("Splitting dataset...")
    train_df, val_df, test_df = create_data_splits(
        args.data_csv,
        train_ratio=config.data.train_ratio,
        val_ratio=config.data.val_ratio,
        seed=config.training.seed,
    )

    split_dir = Path(config.output_dir) / "splits"
    split_dir.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(split_dir / "train.csv", index=False)
    val_df.to_csv(split_dir / "val.csv", index=False)
    test_df.to_csv(split_dir / "test.csv", index=False)

    aug_config = config.augmentation.model_dump()
    train_transforms = get_train_transforms(aug_config)
    val_transforms = get_val_transforms()

    train_dataset = RetinaDataset(
        split_dir / "train.csv",
        image_dir=args.image_dir,
        transform=train_transforms,
        target_size=config.data.image_size,
    )
    val_dataset = RetinaDataset(
        split_dir / "val.csv",
        image_dir=args.image_dir,
        transform=val_transforms,
        target_size=config.data.image_size,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.training.batch_size,
        shuffle=True,
        num_workers=config.data.num_workers,
        pin_memory=config.data.pin_memory,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.training.batch_size,
        shuffle=False,
        num_workers=config.data.num_workers,
        pin_memory=config.data.pin_memory,
    )

    trainer = Trainer(config)
    trainer.train(train_loader, val_loader)

    logger.info("Training complete. Checkpoints saved to: %s", config.checkpoint_dir)


if __name__ == "__main__":
    main()
