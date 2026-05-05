# Evaluation Workflow Guide

## Overview

This guide describes how to evaluate trained CardioRetina-AI models using the comprehensive evaluation pipeline.

## When to Evaluate

1. **After Training**: Assess final model performance on held-out test set
2. **During Training**: Monitor validation metrics for early stopping
3. **Before Deployment**: Confirm model meets quality thresholds
4. **Model Comparison**: Compare different architectures or checkpoints

## Evaluation Pipeline

### Step 1: Prepare Test Data

Ensure test data is:
- Held out from training (no data leakage)
- Representative of real-world distribution
- Properly formatted (see [Dataset Format Guide](09-dataset-format-guide.md))

### Step 2: Run Evaluation

```bash
python -m cardioretina.evaluation.evaluate \
    --checkpoint checkpoints/best_model.pt \
    --test-csv data/splits/test.csv \
    --image-dir data/images/ \
    --output-dir evaluation_results/
```

### Evaluation Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `--checkpoint` | Path to model checkpoint | Yes |
| `--test-csv` | Path to test dataset CSV | Yes |
| `--image-dir` | Directory containing images | Yes |
| `--output-dir` | Directory for results | Yes |
| `--batch-size` | Inference batch size (default: 32) | No |
| `--device` | Device: cuda/cpu (default: auto) | No |

## Evaluation Outputs

### Generated Files

```
evaluation_results/
├── results.json              # Numerical metrics (JSON)
├── results.txt               # Human-readable report
├── confusion_matrix.png        # Confusion matrix visualization
├── roc_curve.png               # ROC curve plot
├── precision_recall_curve.png  # PR curve plot
└── per_class_metrics.csv       # Metrics per class
```

### Metrics Computed

#### Classification Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correctness |
| **Precision** | TP/(TP+FP) | Reliability of positive predictions |
| **Recall** | TP/(TP+FN) | Coverage of actual positives |
| **Specificity** | TN/(TN+FP) | Coverage of actual negatives |
| **F1-Score** | 2×(Precision×Recall)/(Precision+Recall) | Balanced measure |

#### Probability Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **AUC-ROC** | Area under ROC curve | > 0.8 good, > 0.9 excellent |
| **AUC-PR** | Area under Precision-Recall curve | Useful for imbalanced data |
| **Calibration** | Predicted vs actual probabilities | Well-calibrated preferred |

#### Per-Class Metrics

Computed separately for each class:
- True Positives, False Positives
- True Negatives, False Negatives
- Precision, Recall, F1 for each class

## Understanding Results

### results.json Structure

```json
{
  "accuracy": 0.8234,
  "precision": 0.8123,
  "recall": 0.8456,
  "specificity": 0.8012,
  "f1_score": 0.8287,
  "auc_roc": 0.8912,
  "auc_pr": 0.8567,
  "confusion_matrix": {
    "true_negatives": 450,
    "false_positives": 50,
    "false_negatives": 40,
    "true_positives": 210
  },
  "class_metrics": {
    "low_risk": {"precision": 0.85, "recall": 0.90, "f1": 0.87},
    "high_risk": {"precision": 0.81, "recall": 0.84, "f1": 0.82}
  }
}
```

### results.txt Example

```
========================================
EVALUATION RESULTS
========================================
Model: checkpoints/best_model.pt
Test samples: 750

Classification Metrics:
  Accuracy:    0.8234
  Precision:   0.8123
  Recall:      0.8456
  Specificity: 0.8012
  F1-Score:    0.8287

Probability Metrics:
  AUC-ROC:     0.8912
  AUC-PR:      0.8567

Confusion Matrix:
                 Predicted
               Low    High
  Actual Low   450    50
  Actual High  40     210

Generated at: 2024-01-15 14:30:22
```

## Interpreting Visualizations

### Confusion Matrix

Shows prediction accuracy per class:
- **Diagonal**: Correct predictions
- **Off-diagonal**: Misclassifications
- Use to identify class-specific issues

### ROC Curve

Plots True Positive Rate vs False Positive Rate:
- **Curve closer to top-left**: Better performance
- **AUC interpretation**:
  - 0.5: Random guessing
  - 0.7-0.8: Acceptable
  - 0.8-0.9: Good
  - >0.9: Excellent

### Precision-Recall Curve

Useful for imbalanced datasets:
- Shows trade-off between precision and recall
- High PR-AUC indicates good performance on minority class

## Evaluation Best Practices

### Data Considerations

1. **Test Set Integrity**
   - Never use test data during training
   - No hyperparameter tuning on test set
   - Evaluate once, or use nested cross-validation

2. **Sample Size**
   - Minimum 100 samples per class for reliable metrics
   - More samples = more reliable estimates
   - Report confidence intervals if possible

3. **Class Distribution**
   - If imbalanced, focus on AUC-ROC and AUC-PR
   - Accuracy can be misleading for imbalanced data

### Model Interpretation

1. **Threshold Selection**
   - Default threshold: 0.5
   - Adjust based on use case:
     - Screening (catch all cases): Lower threshold, higher recall
     - Diagnosis (avoid false alarms): Higher threshold, higher precision

2. **Calibration**
   - Check if predicted probabilities match actual outcomes
   - Well-calibrated: Predicted 0.8 ≈ 80% actual positive rate
   - Use calibration plots if needed

3. **Error Analysis**
   - Review false positives: What patterns lead to over-prediction?
   - Review false negatives: What cases are missed?
   - Consider Grad-CAM for understanding mistakes

## Comparing Models

### Multiple Model Evaluation

Run evaluation for different checkpoints:

```bash
# Model A (CNN only)
python -m cardioretina.evaluation.evaluate \
    --checkpoint checkpoints/cnn_only.pt \
    --test-csv data/splits/test.csv \
    --image-dir data/images/ \
    --output-dir results/cnn_only/

# Model B (Full hybrid)
python -m cardioretina.evaluation.evaluate \
    --checkpoint checkpoints/hybrid.pt \
    --test-csv data/splits/test.csv \
    --image-dir data/images/ \
    --output-dir results/hybrid/
```

### Comparison Table

| Model | Accuracy | AUC-ROC | F1-Score | Params |
|-------|----------|---------|----------|--------|
| CNN Only | 0.78 | 0.84 | 0.79 | 10M |
| ViT Only | 0.75 | 0.82 | 0.76 | 86M |
| Hybrid | 0.82 | 0.89 | 0.83 | 96M |

## Reporting Results

### For Research Papers

Include:
- Dataset size and split ratios
- All relevant metrics (not just best ones)
- Statistical significance tests
- Comparison with baselines
- Ablation study results

### For Documentation

Include:
- Evaluation command used
- Model checkpoint version
- Date of evaluation
- Any special conditions or notes

## Next Steps

After evaluation:
1. **Ablation Study**: Compare architectural components (see [Ablation Guide](13-ablation-study.md))
2. **Export Model**: Convert to ONNX for deployment
3. **API Setup**: Start inference server
4. **Documentation**: Record results in model card

---

*Thorough evaluation ensures reliable understanding of model performance and limitations.*
