# Expected Evaluation Outputs

## Overview

This document describes the evaluation outputs generated after training and testing the CardioRetina-AI model.

## Output Files

After running evaluation, the following files are created in the output directory:

```
evaluation_results/
├── results.json                 # Structured metrics (JSON)
├── results.txt                  # Human-readable report
├── confusion_matrix.png         # Confusion matrix visualization
├── roc_curve.png                # ROC curve plot
├── precision_recall_curve.png   # Precision-Recall curve
└── per_class_metrics.csv        # Class-specific metrics
```

## Detailed Output Descriptions

### 1. results.json

**Format**: JSON
**Purpose**: Machine-readable metrics for programmatic analysis

**Structure**:
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
    "low_risk": {
      "precision": 0.8529,
      "recall": 0.9000,
      "f1": 0.8759
    },
    "high_risk": {
      "precision": 0.8077,
      "recall": 0.8400,
      "f1": 0.8235
    }
  },
  "evaluation_timestamp": "2024-01-15T14:30:22Z",
  "model_checkpoint": "checkpoints/best_model.pt",
  "test_samples": 750
}
```

### 2. results.txt

**Format**: Plain text
**Purpose**: Human-readable summary report

**Sample Content**:
```
========================================
EVALUATION RESULTS
========================================

Model: checkpoints/best_model.pt
Evaluation Date: 2024-01-15 14:30:22
Test Samples: 750

CLASSIFICATION METRICS
----------------------
Accuracy:      0.8234
Precision:     0.8123
Recall:        0.8456
Specificity:   0.8012
F1-Score:      0.8287

PROBABILITY METRICS
-------------------
AUC-ROC:       0.8912
AUC-PR:        0.8567

CONFUSION MATRIX
----------------
                    Predicted
               Low Risk    High Risk
Actual Low       450          50
Actual High       40         210

CLASS-SPECIFIC METRICS
----------------------
Low Risk:
  - Precision: 0.8529
  - Recall:    0.9000
  - F1-Score:  0.8759

High Risk:
  - Precision: 0.8077
  - Recall:    0.8400
  - F1-Score:  0.8235

========================================
```

### 3. confusion_matrix.png

**Format**: PNG image
**Purpose**: Visual representation of prediction accuracy

**Contents**:
- 2×2 grid showing:
  - True Negatives (top-left)
  - False Positives (top-right)
  - False Negatives (bottom-left)
  - True Positives (bottom-right)
- Color-coded heatmap
- Raw counts and percentages

**Interpretation**:
- Diagonal elements (TN, TP): Correct predictions
- Off-diagonal elements (FP, FN): Errors
- Ideal: High values on diagonal, low on off-diagonal

### 4. roc_curve.png

**Format**: PNG image
**Purpose**: Visualize true positive vs. false positive trade-off

**Contents**:
- X-axis: False Positive Rate (0 to 1)
- Y-axis: True Positive Rate (0 to 1)
- ROC curve (model performance)
- Diagonal reference line (random guessing)
- AUC score annotation

**Interpretation**:
- Curve closer to top-left: Better performance
- AUC = 0.5: Random guessing
- AUC > 0.8: Good performance
- AUC > 0.9: Excellent performance

### 5. precision_recall_curve.png

**Format**: PNG image
**Purpose**: Precision-recall trade-off visualization

**Contents**:
- X-axis: Recall (0 to 1)
- Y-axis: Precision (0 to 1)
- PR curve
- Baseline (random classifier performance)
- AUC-PR annotation

**Interpretation**:
- Important for imbalanced datasets
- High area under curve: Good performance
- Baseline depends on class distribution

### 6. per_class_metrics.csv

**Format**: CSV
**Purpose**: Detailed per-class breakdown

**Sample Content**:
```csv
class,precision,recall,f1_score,support
low_risk,0.8529,0.9000,0.8759,500
high_risk,0.8077,0.8400,0.8235,250
```

## Expected Value Ranges

### Reasonable Performance Targets

| Metric | Acceptable | Good | Excellent |
|--------|-----------|------|-----------|
| **Accuracy** | 0.70-0.80 | 0.80-0.85 | >0.85 |
| **AUC-ROC** | 0.75-0.85 | 0.85-0.90 | >0.90 |
| **F1-Score** | 0.70-0.80 | 0.80-0.85 | >0.85 |
| **Precision** | 0.70-0.80 | 0.80-0.85 | >0.85 |
| **Recall** | 0.70-0.80 | 0.80-0.90 | >0.90 |

### Note on Metrics

> **Important**: These ranges are approximate and depend on:
> - Dataset quality and size
> - Task difficulty
> - Clinical context
> - Class balance

### Factors Affecting Performance

1. **Dataset Size**: Larger datasets generally yield better results
2. **Data Quality**: Clear images, accurate labels
3. **Class Balance**: Balanced datasets give more reliable metrics
4. **Data Diversity**: Varied populations improve generalization

## Using Evaluation Outputs

### For Model Selection

Compare multiple models:

```python
import json

models = {
    'baseline': json.load(open('exp_001/results.json')),
    'tuned': json.load(open('exp_002/results.json'))
}

for name, results in models.items():
    print(f"{name}: AUC = {results['auc_roc']:.4f}")
```

### For Reporting

Include in documentation:
- Key metrics from results.txt
- Visualizations from PNG files
- Comparison with baseline

### For Debugging

Analyze poor performance:
1. Check confusion matrix for class-specific issues
2. Review ROC curve for threshold sensitivity
3. Examine per-class metrics for imbalance

## Output Verification

### Checklist

After evaluation, verify:
- [ ] All expected files created
- [ ] results.json contains all required fields
- [ ] Visualizations are readable
- [ ] Metrics are in reasonable ranges
- [ ] Class distribution is as expected

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Missing files | Permission error | Check directory permissions |
| NaN values | Data issues | Check input data quality |
| Very low metrics | Training issue | Review training logs |
| Empty plots | No predictions | Verify model checkpoint |

## Archiving Results

### Recommended Practice

Organize evaluation results:

```
experiments/
├── exp_001_baseline/
│   ├── training_history.csv
│   ├── best_model.pt
│   └── evaluation_results/        # <- Evaluation outputs here
│       ├── results.json
│       ├── results.txt
│       ├── confusion_matrix.png
│       ├── roc_curve.png
│       └── precision_recall_curve.png
└── summary.md  # Summary of all experiments
```

### Long-term Storage

- Keep JSON and CSV files (small, useful)
- Keep PNG files for reports
- Archive with experiment metadata
- Document which checkpoint was evaluated

---

*Comprehensive evaluation outputs enable thorough model assessment and informed decision-making.*
