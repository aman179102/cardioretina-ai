# Reproducibility Guide: CardioRetina-AI

## Deterministic Training

CardioRetina-AI supports deterministic training through seed control.

### Seed Configuration

Default seed: `42` (configurable in `config/default.yaml` or via CLI)

```yaml
training:
  seed: 42
```

The seed controls:
- Python `random` module
- NumPy random state
- PyTorch random state (CPU and CUDA)
- CUDA deterministic algorithms (when available)

### Deterministic Settings

```python
# Applied automatically when seed is set
import torch
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
```

> Note: Full determinism is hardware-dependent. Results may vary slightly between different GPUs or CPU architectures.

## Environment

### Software Requirements

| Package | Version |
|---------|---------|
| Python | 3.10+ |
| PyTorch | 2.0+ |
| torchvision | 0.15+ |
| timm | 0.9+ |
| FastAPI | 0.100+ |
| Pillow | 10.0+ |
| scikit-learn | 1.3+ |
| numpy | 1.24+ |
| pandas | 2.0+ |
| matplotlib | 3.7+ |
| pydantic | 2.0+ |

### Installation

```bash
git clone https://github.com/aarohidev91/cardioretina-ai.git
cd cardioretina-ai
pip install -e ".[dev]"
```

### GPU Support

- CUDA 11.8+ recommended for GPU training
- CUDA is optional; CPU training is fully supported
- The system auto-detects available hardware

## Reproducing Training

### Step 1: Prepare Dataset

```bash
# Validate dataset
python -m cardioretina.data.validate path/to/dataset.csv --image-dir path/to/images/

# Create train/val/test splits
python -m cardioretina.data.split path/to/dataset.csv --output-dir data/splits/ --seed 42
```

### Step 2: Train Model

```bash
python -m cardioretina.training.train \
    --data-csv data/splits/train.csv \
    --image-dir data/images/ \
    --config config/default.yaml
```

### Step 3: Evaluate Model

```bash
python -m cardioretina.evaluation.evaluate \
    --checkpoint checkpoints/best_model.pt \
    --test-csv data/splits/test.csv \
    --image-dir data/images/ \
    --output-dir evaluation_results/
```

### Step 4: Run Ablation Study

```bash
python -m cardioretina.evaluation.ablation \
    --test-csv data/splits/test.csv \
    --image-dir data/images/ \
    --checkpoint-dir checkpoints/ \
    --output-dir ablation_results/
```

## Expected Outputs

### Training Outputs

```
outputs/
├── training_history.json      # Epoch-by-epoch metrics
├── training_history.csv       # Same metrics in CSV format
├── experiment_log.json        # Experiment metadata
└── config_snapshot.yaml       # Configuration snapshot

checkpoints/
├── best_model.pt              # Best validation loss checkpoint
└── checkpoint_epoch_N.pt      # Periodic checkpoints
```

### Evaluation Outputs

```
evaluation_results/
├── results.json               # Numeric metrics
├── results.txt                # Formatted report
├── confusion_matrix.png       # Confusion matrix plot
├── roc_curve.png              # ROC curve with AUC
└── precision_recall_curve.png # Precision-recall curve
```

### Ablation Study Outputs

```
ablation_results/
├── ablation_results.json      # Per-configuration metrics
└── ablation_table.md          # Markdown comparison table
```

## Experiment Tracking

Each training run automatically logs:
- Timestamp (UTC)
- Full configuration snapshot
- Device information
- PyTorch and CUDA versions
- Training duration
- Best validation loss
- Final metrics

Logs are saved to `outputs/experiment_log.json`.

### Example Experiment Log

```json
{
  "timestamp": "2024-01-15T10:30:00+00:00",
  "config": { ... },
  "device": "cuda",
  "total_epochs": 50,
  "best_val_loss": 0.3456,
  "final_train_loss": 0.2100,
  "final_val_acc": 0.8500,
  "training_time_seconds": 3600.0,
  "pytorch_version": "2.1.0",
  "cuda_available": true
}
```

## Verifying Setup

```bash
# Run test suite
pytest tests/ -v

# Lint check
ruff check cardioretina/ tests/

# Import verification
python -c "from cardioretina.models.hybrid_model import CardioRetinaModel; print('OK')"

# Model forward pass
python -c "
import torch
from cardioretina.models.hybrid_model import CardioRetinaModel
model = CardioRetinaModel(pretrained=False, use_vit=False)
model.eval()
out = model(torch.randn(1, 3, 224, 224), torch.randn(1, 8))
print(f'Output: {out.item():.4f}')
"
```
