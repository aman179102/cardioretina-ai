# Experiment Tracking Notes

## Overview

Effective experiment tracking helps compare results, reproduce findings, and identify optimal configurations.

## What to Track

### Essential Information

| Category | Details to Record |
|----------|-----------------|
| **When** | Timestamp, duration |
| **What** | Model architecture, hyperparameters |
| **Where** | Hardware, environment |
| **How** | Code version, data version |
| **Results** | Metrics, artifacts, observations |

### Metrics to Log

**Training Metrics (per epoch):**
- Training loss
- Validation loss
- Training accuracy
- Validation accuracy
- Learning rate

**Final Metrics:**
- Test accuracy
- AUC-ROC
- Precision, Recall, F1
- Confusion matrix
- Per-class metrics

**System Metrics:**
- Training time
- GPU memory usage
- CPU utilization
- Disk I/O

## Tracking Methods

### 1. JSON Logging (Built-in)

The training pipeline automatically creates:

```json
{
  "experiment_id": "exp_20240115_143022",
  "timestamp": "2024-01-15T14:30:22Z",
  "git_commit": "a1b2c3d4",
  "config": {
    "model": "hybrid_cnn_vit_clinical",
    "epochs": 100,
    "batch_size": 32,
    "learning_rate": 0.001
  },
  "hardware": {
    "gpu": "NVIDIA RTX 3090",
    "cuda_version": "11.8"
  },
  "epochs": [
    {"epoch": 1, "train_loss": 0.6932, "val_loss": 0.6821, "val_auc": 0.6234},
    {"epoch": 2, "train_loss": 0.6523, "val_loss": 0.6432, "val_auc": 0.6721}
  ],
  "best_epoch": 45,
  "best_val_auc": 0.8912
}
```

Located at: `outputs/experiment_log.json`

### 2. CSV Training History

For easy analysis in spreadsheet tools:

```csv
epoch,train_loss,train_acc,val_loss,val_acc,val_auc,learning_rate
1,0.6932,0.5234,0.6821,0.5432,0.6234,0.001
2,0.6523,0.6123,0.6432,0.6234,0.6721,0.001
...
```

Located at: `outputs/training_history.csv`

### 3. Manual Experiment Log

Maintain a manual log for observations:

```markdown
# Experiment Log

## Experiment 001: Baseline

**Date:** 2024-01-15
**Purpose:** Establish baseline with default config
**Hypothesis:** Hybrid model should achieve >0.85 AUC

### Configuration
- Model: Hybrid (CNN+ViT+Clinical)
- Epochs: 100
- Batch size: 32
- LR: 0.001

### Results
- Best epoch: 45
- Val AUC: 0.8912
- Test AUC: 0.8823

### Observations
- Training was stable
- Validation loss plateaued around epoch 40
- No signs of overfitting

### Next Steps
- Try learning rate 0.0005
- Test with different batch sizes
```

## Experiment Comparison

### Comparison Table

Maintain a table comparing experiments:

| Exp | Config | Val AUC | Test AUC | Epochs | Notes |
|-----|--------|---------|----------|--------|-------|
| 001 | Baseline | 0.8912 | 0.8823 | 45 | Stable |
| 002 | LR=0.0005 | 0.8934 | 0.8856 | 52 | Slight improvement |
| 003 | BS=64 | 0.8891 | 0.8812 | 38 | Faster convergence |

### Visualization

Plot comparison charts:

```python
import matplotlib.pyplot as plt
import pandas as pd

# Load multiple experiments
exp1 = pd.read_csv('exp_001/training_history.csv')
exp2 = pd.read_csv('exp_002/training_history.csv')

plt.plot(exp1['epoch'], exp1['val_auc'], label='Baseline')
plt.plot(exp2['epoch'], exp2['val_auc'], label='Lower LR')
plt.legend()
plt.savefig('comparison.png')
```

## Organizing Experiments

### Directory Structure

```
experiments/
├── 001_baseline_20240115/
│   ├── experiment_log.json
│   ├── training_history.csv
│   ├── config_snapshot.yaml
│   ├── best_model.pt
│   ├── evaluation_results/
│   └── NOTES.md
├── 002_lower_lr_20240116/
│   └── ...
└── summary.xlsx  # Comparison spreadsheet
```

### Naming Convention

Format: `XXX_description_YYYYMMDD`

Examples:
- `001_baseline_20240115`
- `002_lr_0.0005_20240116`
- `003_cnn_only_20240117`

## Advanced Tracking

### MLflow Integration (Optional)

```python
import mlflow

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("epochs", 100)
    mlflow.log_param("batch_size", 32)
    
    # Log metrics per epoch
    for epoch in range(epochs):
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_auc", val_auc, step=epoch)
    
    # Log artifacts
    mlflow.log_artifact("outputs/training_history.csv")
    mlflow.log_artifact("checkpoints/best_model.pt")
```

### Weights & Biases (Optional)

```python
import wandb

wandb.init(project="cardioretina-ai")

# Log config
wandb.config.update(config)

# Log metrics
wandb.log({"train_loss": loss, "val_auc": auc})

# Log model
wandb.save("checkpoints/best_model.pt")
```

## Best Practices

### 1. One Change at a Time

Compare experiments with single variable changes:
- ✅ Change LR from 0.001 to 0.0005 (keep everything else same)
- ❌ Change LR and batch size and model architecture simultaneously

### 2. Run Multiple Seeds

For critical comparisons, run with different seeds:
- Seed 42, 123, 456
- Report mean ± std

### 3. Document Everything

Write notes immediately after experiment:
- What worked
- What didn't
- Unexpected observations
- Ideas for next experiments

### 4. Version Control

- Commit code before starting experiment
- Tag important milestones
- Note commit hash in experiment log

### 5. Regular Cleanup

- Delete failed/poor experiments after analysis
- Keep only best models
- Archive old experiments to cold storage

## Analysis Tools

### Command Line

```bash
# Compare multiple experiments
python scripts/compare_experiments.py \
    experiments/001_baseline/ \
    experiments/002_lower_lr/ \
    experiments/003_higher_bs/

# Generate summary report
python scripts/generate_report.py --experiments experiments/
```

### Jupyter Notebook

```python
# Load and compare experiments
import pandas as pd
import matplotlib.pyplot as plt

exps = {
    'Baseline': pd.read_csv('experiments/001/training_history.csv'),
    'Lower LR': pd.read_csv('experiments/002/training_history.csv'),
}

for name, df in exps.items():
    plt.plot(df['epoch'], df['val_auc'], label=name)
plt.legend()
```

## Troubleshooting Tracking Issues

| Issue | Solution |
|-------|----------|
| Missing experiment logs | Check `outputs/` directory permissions |
| Incomplete metrics | Ensure training completed successfully |
| Wrong experiment comparison | Verify experiment IDs and timestamps |
| Large model artifacts | Use model checkpointing, not full saves |

---

*Systematic experiment tracking transforms random exploration into systematic progress.*
