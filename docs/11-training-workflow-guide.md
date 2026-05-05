# Training Workflow Guide

## Overview

This guide explains the complete training workflow for CardioRetina-AI, from data preparation to model checkpointing.

## Prerequisites

Before starting training, ensure:
1. Dataset prepared (see [Dataset Format Guide](09-dataset-format-guide.md))
2. Environment configured (Python 3.10+, PyTorch installed)
3. GPU available (optional but recommended)
4. Sufficient disk space for checkpoints and logs

## Training Pipeline

### Step 1: Validate Data

```bash
python -m cardioretina.data.validate \
    data/dataset.csv \
    --image-dir data/images/
```

**Purpose**: Ensure data integrity before training
**Expected output**: Validation report with any issues found

### Step 2: Split Dataset

```bash
python -m cardioretina.data.split \
    data/dataset.csv \
    --output-dir data/splits/ \
    --train-ratio 0.7 \
    --val-ratio 0.15
```

**Creates**:
- `train.csv` (70%): For model training
- `val.csv` (15%): For validation and early stopping
- `test.csv` (15%): For final evaluation (held out)

### Step 3: Configure Training

Edit `config/default.yaml` or create custom config:

```yaml
training:
  epochs: 100
  batch_size: 32
  learning_rate: 0.001
  weight_decay: 0.0001
  early_stopping_patience: 10

model:
  architecture: "cnn_vit_clinical"  # Options: cnn, vit, cnn_vit, cnn_vit_clinical
  efficientnet_version: "b3"
  vit_model: "vit_base_patch16_224"
  dropout: 0.3

data:
  image_size: 224
  augmentation: true
  num_workers: 4
```

### Step 4: Start Training

#### Basic Training

```bash
python -m cardioretina.training.train \
    --data-csv data/splits/train.csv \
    --image-dir data/images/ \
    --val-csv data/splits/val.csv
```

#### Training with Custom Config

```bash
python -m cardioretina.training.train \
    --config config/custom.yaml \
    --data-csv data/splits/train.csv \
    --image-dir data/images/
```

#### Training with Hyperparameter Overrides

```bash
python -m cardioretina.training.train \
    --data-csv data/splits/train.csv \
    --image-dir data/images/ \
    --epochs 150 \
    --batch-size 64 \
    --lr 0.0005
```

## Training Process

### What Happens During Training

```
Epoch 1/100
├── Batch 1/50: Forward pass, compute loss, backward pass, update weights
├── Batch 2/50: ...
├── ...
├── Validation: Compute metrics on val set
├── Check early stopping criteria
├── Save checkpoint if best model
└── Log metrics

Epoch 2/100
└── ... (repeat)
```

### Training Outputs

The training script creates the following outputs:

```
outputs/
├── training_history.json       # Metrics per epoch (JSON)
├── training_history.csv        # Metrics per epoch (CSV)
├── experiment_log.json         # Experiment metadata
└── config_snapshot.yaml        # Config used for this run

checkpoints/
├── best_model.pt              # Best model (lowest val loss)
├── epoch_10.pt                # Intermediate checkpoints (optional)
└── final_model.pt             # Final model after training
```

### Monitored Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Loss** | Binary cross-entropy | Decreasing |
| **Accuracy** | Classification accuracy | Increasing |
| **AUC-ROC** | Area under ROC curve | Increasing |
| **Precision** | True positives / predicted positives | Balanced |
| **Recall** | True positives / actual positives | Balanced |
| **F1-Score** | Harmonic mean of precision/recall | Balanced |

## Training Best Practices

### Data Considerations

1. **Class Balance**
   - If classes are imbalanced (>2:1 ratio), use class weights
   - Or apply oversampling/undersampling techniques
   - Monitor per-class metrics

2. **Data Augmentation**
   - Always enabled for training (prevents overfitting)
   - Disabled for validation (consistent evaluation)
   - See `cardioretina/data/augmentation.py` for details

3. **Batch Size**
   - Larger batches (32-64): More stable gradients, need more memory
   - Smaller batches (8-16): Noisier gradients, less memory
   - Adjust based on available GPU memory

### Model Configuration

1. **Architecture Selection**
   - Start with full model (CNN + ViT + Clinical)
   - Use ablation study to compare simpler variants
   - Choose based on validation performance

2. **Transfer Learning**
   - Pre-trained ImageNet weights used by default
   - Early layers frozen (feature extractors)
   - Later layers trainable (task-specific)

3. **Regularization**
   - Dropout: 0.3 is a good starting point
   - Weight decay: 1e-4 helps prevent overfitting
   - Early stopping: Prevents unnecessary training

### Hyperparameter Tuning

Key hyperparameters to experiment with:

| Parameter | Default | Range to Try |
|-----------|---------|--------------|
| Learning rate | 0.001 | 0.0001 - 0.01 |
| Batch size | 32 | 16 - 64 |
| Dropout | 0.3 | 0.1 - 0.5 |
| Weight decay | 1e-4 | 1e-5 - 1e-3 |
| Epochs | 100 | 50 - 200 |

## Monitoring Training

### Console Output

Training progress displayed in console:
```
Epoch 25/100
├── Train Loss: 0.4234, Acc: 0.8234, AUC: 0.8912
└── Val Loss: 0.4532, Acc: 0.8123, AUC: 0.8823 ← Best: saved checkpoint
```

### TensorBoard (Optional)

If configured, metrics are logged to TensorBoard:
```bash
tensorboard --logdir outputs/logs/
```

### Early Stopping

Training stops automatically when:
- Validation loss doesn't improve for `patience` epochs (default: 10)
- Best model is always preserved
- Prevents overfitting to training data

## Troubleshooting

### Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Training loss not decreasing | Learning rate too high | Reduce to 0.0001 |
| Validation loss increases | Overfitting | Increase dropout, add augmentation |
| Out of memory | Batch size too large | Reduce batch size |
| Slow training | Too many workers or I/O bound | Reduce num_workers, check disk speed |
| NaN loss | Learning rate too high, bad data | Check data, reduce LR |

### GPU Utilization

Monitor GPU usage:
```bash
watch -n 1 nvidia-smi
```

- Low utilization: Increase batch size or num_workers
- Out of memory: Reduce batch size

## Next Steps

After training completes:
1. Run evaluation on test set (see [Evaluation Guide](12-evaluation-workflow-guide.md))
2. Export model to ONNX for deployment
3. Start API server for inference
4. Document results in experiment log

---

*Consistent training workflows ensure reproducible and comparable results.*
