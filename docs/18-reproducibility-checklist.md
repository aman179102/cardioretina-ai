# Reproducibility Checklist

## Overview

This checklist ensures experiments with CardioRetina-AI can be reproduced by yourself and others.

## Environment Reproducibility

### Python Environment

- [ ] Python version specified (3.10+ required)
- [ ] Virtual environment used (venv/conda)
- [ ] All dependencies installed from `pyproject.toml`
- [ ] Exact dependency versions recorded

### Record Environment

```bash
# Save exact versions
pip freeze > requirements.lock.txt

# Or use pip-tools
pip-compile pyproject.toml
```

### CUDA/GPU (if applicable)

- [ ] CUDA version documented
- [ ] GPU model specified
- [ ] Driver version noted

```bash
# Record CUDA info
nvidia-smi > cuda_info.txt
```

## Code Reproducibility

### Version Control

- [ ] All code committed to git
- [ ] Git commit hash recorded
- [ ] No uncommitted changes during experiment

```bash
# Record git state
git rev-parse HEAD > git_commit.txt
git status > git_status.txt
git diff > git_diff.txt  # If any uncommitted changes
```

### Code State

- [ ] Specific branch used for experiment
- [ ] Tag created for milestone results
- [ ] Code reviewed before experiment

## Data Reproducibility

### Dataset Documentation

- [ ] Dataset source documented
- [ ] Dataset version recorded
- [ ] Preprocessing steps documented
- [ ] Data split random seed fixed

### Data Splits

```python
# Fix random seed for splits
from cardioretina.utils.seed import set_seed
set_seed(42)
```

### Data Validation

- [ ] Dataset validation run passed
- [ ] Data checksums recorded (optional)
- [ ] Data split files saved

## Model Reproducibility

### Random Seeds

- [ ] PyTorch random seed set
- [ ] NumPy random seed set
- [ ] Python random seed set
- [ ] CUDA deterministic mode enabled (if needed)

```python
from cardioretina.utils.seed import set_seed
set_seed(42, deterministic=True)
```

### Model Configuration

- [ ] Configuration file saved
- [ ] All hyperparameters documented
- [ ] Architecture details recorded

```bash
# Save config with experiment
cp config/experiment.yaml outputs/experiment_001/config.yaml
```

### Training Process

- [ ] Number of epochs specified
- [ ] Batch size documented
- [ ] Learning rate schedule recorded
- [ ] Optimizer settings saved
- [ ] Early stopping criteria noted

## Experiment Tracking

### Output Organization

Recommended structure:
```
experiments/
├── exp_001_baseline/
│   ├── config.yaml
│   ├── training_history.csv
│   ├── training_history.json
│   ├── experiment_log.json
│   ├── best_model.pt
│   └── evaluation_results/
├── exp_002_higher_lr/
│   └── ...
```

### Metrics Logging

- [ ] All metrics logged per epoch
- [ ] Training and validation loss recorded
- [ ] Best checkpoint saved with metric value
- [ ] Final metrics documented

### Artifacts

- [ ] Model checkpoint saved
- [ ] Training curves plotted
- [ ] Evaluation metrics saved
- [ ] Grad-CAM examples generated

## Documentation Checklist

### Experiment Documentation

- [ ] Experiment purpose described
- [ ] Hypothesis stated
- [ ] Methodology explained
- [ ] Results summarized

### README Update

- [ ] Experiment added to experiment log
- [ ] Key findings documented
- [ ] Unexpected observations noted

### Model Card Update

- [ ] Training data description
- [ ] Performance metrics filled
- [ ] Limitations documented
- [ ] Ethical considerations noted

## Reproduction Steps

### Step-by-Step Commands

Document exact commands used:

```bash
# 1. Prepare data
python -m cardioretina.data.split data/dataset.csv --output-dir splits/

# 2. Train model
python -m cardioretina.training.train \
    --config config/experiment.yaml \
    --data-csv splits/train.csv \
    --val-csv splits/val.csv

# 3. Evaluate
python -m cardioretina.evaluation.evaluate \
    --checkpoint outputs/exp_001/best_model.pt \
    --test-csv splits/test.csv
```

### Expected Results

Document expected outcomes:

| Metric | Expected Range |
|--------|----------------|
| Accuracy | 0.80 - 0.85 |
| AUC-ROC | 0.87 - 0.92 |
| Training Time | 2-4 hours |

## Verification

### Self-Verification

- [ ] Can you reproduce your own results?
- [ ] Results consistent across multiple runs?
- [ ] Sensitivity to seed tested?

### External Verification

- [ ] Colleague can reproduce results
- [ ] Results consistent on different hardware
- [ ] Results consistent with similar methods

## Common Pitfalls to Avoid

### ❌ Non-Reproducible Practices

- Using different data splits between runs
- Modifying code during experiment
- Not saving model checkpoints
- Relying on global state
- Using non-deterministic operations

### ✅ Reproducible Practices

- Fixed random seeds
- Version-controlled code
- Documented dependencies
- Saved configurations
- Automated logging

## Tools for Reproducibility

### Recommended Tools

| Tool | Purpose |
|------|---------|
| Git | Version control |
| DVC | Data version control |
| MLflow | Experiment tracking |
| Weights & Biases | Experiment logging |
| Docker | Environment reproducibility |

### Simple Logging Template

```python
import json
from datetime import datetime

experiment_info = {
    "timestamp": datetime.now().isoformat(),
    "git_commit": get_git_commit(),
    "config": config,
    "seed": 42,
    "hardware": {
        "gpu": torch.cuda.get_device_name(0),
        "cuda_version": torch.version.cuda
    }
}

with open('experiment_log.json', 'w') as f:
    json.dump(experiment_info, f, indent=2)
```

## Quick Reproducibility Check

Before starting any experiment, verify:

```bash
# 1. Clean working directory
git status  # Should show no uncommitted changes

# 2. Record environment
pip freeze > requirements.lock.txt

# 3. Set seed in code
# (set_seed(42) called in training script)

# 4. Create experiment directory
mkdir -p experiments/exp_$(date +%Y%m%d_%H%M%S)

# 5. Start experiment with logging
python -m cardioretina.training.train --config config.yaml 2>&1 | tee experiments/exp_*/train.log
```

---

*Reproducibility is the foundation of scientific research and engineering reliability.*
