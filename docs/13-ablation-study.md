# Ablation Study Explanation

## What is Ablation Study?

An **ablation study** systematically removes or modifies components of a system to measure their individual contributions to overall performance.

### Purpose

1. **Understand component importance**: Which parts matter most?
2. **Identify redundancy**: Are some components unnecessary?
3. **Validate design decisions**: Do architectural choices help?
4. **Optimize efficiency**: Can we simplify without losing performance?

## Ablation Study in CardioRetina-AI

### Architectural Components

The full model combines three inputs:

```
Full Model = CNN (EfficientNet) + ViT + Clinical Network
```

We test these configurations:

| Configuration | Components | Purpose |
|---------------|------------|---------|
| **CNN Only** | EfficientNet | Baseline local feature extraction |
| **ViT Only** | Vision Transformer | Global context baseline |
| **CNN + ViT** | Both image encoders | Combined visual features |
| **Full Model** | All three | Complete multimodal approach |

### Running Ablation Study

```bash
python -m cardioretina.evaluation.ablation \
    --test-csv data/splits/test.csv \
    --image-dir data/images/ \
    --checkpoint-dir checkpoints/ \
    --output-dir ablation_results/
```

### Prerequisites

Ensure all model variants are trained:

```bash
# Train each configuration
cardioretina-train --config config/cnn_only.yaml
cardioretina-train --config config/vit_only.yaml
cardioretina-train --config config/cnn_vit.yaml
cardioretina-train --config config/full.yaml
```

## Expected Results

### Performance Table

| Configuration | Accuracy | AUC-ROC | F1 | Params | Inference Time |
|-------------|----------|---------|-----|--------|----------------|
| CNN Only | ~0.78 | ~0.84 | ~0.79 | 10M | 50ms |
| ViT Only | ~0.75 | ~0.82 | ~0.76 | 86M | 80ms |
| CNN + ViT | ~0.80 | ~0.87 | ~0.81 | 96M | 120ms |
| Full Model | ~0.82 | ~0.89 | ~0.83 | 97M | 125ms |

### Interpretation

#### CNN Only vs ViT Only
- CNN: Better local pattern detection (vessel details)
- ViT: Better global structure understanding (overall layout)
- Both have complementary strengths

#### CNN + ViT vs Single Encoder
- Combined visual features improve over individual encoders
- Demonstrates value of hybrid approach
- Small increase in parameters but significant gain in performance

#### Full Model vs CNN + ViT
- Clinical data provides additional improvement
- Shows value of multimodal learning
- Marginal parameter increase for meaningful gain

## Analysis Dimensions

### 1. Performance Impact

Measure contribution of each component:

```
CNN Contribution = (CNN+ViT) - ViT Only ≈ +0.05 AUC
ViT Contribution = (CNN+ViT) - CNN Only ≈ +0.03 AUC
Clinical Contribution = Full - (CNN+ViT) ≈ +0.02 AUC
```

### 2. Computational Cost

Compare efficiency metrics:

| Metric | CNN Only | ViT Only | Full |
|--------|----------|----------|------|
| Parameters | 10M | 86M | 97M |
| FLOPs | 1.8B | 17.6B | 19.8B |
| Memory | 150MB | 350MB | 400MB |
| Inference | 50ms | 80ms | 125ms |

### 3. Feature Redundancy

Check if components learn redundant features:
- Analyze feature correlations
- Check if removing one hurts more than expected
- Look for complementary patterns in Grad-CAM

### 4. Failure Modes

Compare error patterns:
- Cases where CNN succeeds but ViT fails
- Cases where clinical data makes the difference
- Hard examples that require all components

## Ablation Results Output

### Markdown Report

```markdown
# Ablation Study Results

## Configuration Comparison

| Model | Accuracy | AUC-ROC | Params (M) |
|-------|----------|---------|------------|
| CNN Only | 0.7823 | 0.8412 | 10.8 |
| ViT Only | 0.7534 | 0.8234 | 86.4 |
| CNN + ViT | 0.8012 | 0.8723 | 96.2 |
| Full (CNN+ViT+Clinical) | 0.8234 | 0.8912 | 97.1 |

## Key Findings

1. **CNN provides strongest baseline** for retinal features
2. **ViT adds complementary global context** (+0.03 AUC)
3. **Clinical data provides meaningful improvement** (+0.02 AUC)
4. **Hybrid approach is justified** by performance gains
```

### JSON Output

```json
{
  "configurations": {
    "cnn_only": {
      "accuracy": 0.7823,
      "auc_roc": 0.8412,
      "parameters": 10800000
    },
    "vit_only": {
      "accuracy": 0.7534,
      "auc_roc": 0.8234,
      "parameters": 86400000
    },
    "cnn_vit": {
      "accuracy": 0.8012,
      "auc_roc": 0.8723,
      "parameters": 96200000
    },
    "full": {
      "accuracy": 0.8234,
      "auc_roc": 0.8912,
      "parameters": 97100000
    }
  },
  "relative_improvements": {
    "vit_over_cnn": -0.0289,
    "cnn_vit_over_cnn_only": 0.0189,
    "cnn_vit_over_vit_only": 0.0478,
    "full_over_cnn_vit": 0.0222
  }
}
```

## Advanced Ablations

### Component-Level Ablation

Test removing specific parts:

| Ablation | Modification | Purpose |
|----------|--------------|---------|
| No BatchNorm | Remove normalization | Test stability contribution |
| No Dropout | Remove regularization | Test overfitting prevention |
| No Pretraining | Random initialization | Test transfer learning value |
| Smaller Clinical | 8→16→8 instead of 8→64→32 | Test clinical network size |

### Feature-Level Ablation

Test removing specific clinical features:

```
Ablation: Remove Age
Result: AUC drops by 0.015
Conclusion: Age is important predictor

Ablation: Remove Smoking
Result: AUC drops by 0.008
Conclusion: Moderate contribution
```

## Best Practices

1. **Test each component independently**
   - Ensure fair comparison (same training data, epochs, etc.)
   - Use same random seeds where possible

2. **Report all metrics**
   - Don't cherry-pick favorable results
   - Include accuracy, AUC, precision, recall, F1

3. **Consider computational cost**
   - Performance gains should justify added complexity
   - Report parameter counts and inference times

4. **Visualize results**
   - Bar charts for metric comparisons
   - Radar charts for multi-dimensional comparison

## Limitations

- **Interaction effects**: Components may interact non-linearly
- **Optimization variance**: Different configs may need different tuning
- **Dataset dependency**: Results may vary with different data

## Next Steps

After ablation study:
1. Select optimal configuration based on performance/cost trade-off
2. Document findings in MODEL_CARD.md
3. Use insights for future architecture improvements

---

*Ablation studies provide empirical evidence for architectural decisions and help optimize the performance-efficiency trade-off.*
