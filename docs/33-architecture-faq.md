# Architecture FAQ

## Overview

Frequently asked questions about the CardioRetina-AI architecture and design decisions.

## Hybrid Architecture Questions

### Q: Why combine CNN and Vision Transformer instead of using just one?

**A:** CNNs and ViTs have complementary strengths:

| Aspect | CNN (EfficientNet) | Vision Transformer |
|--------|-------------------|-------------------|
| **Strength** | Local pattern detection | Global context understanding |
| **Feature focus** | Edges, textures, small details | Overall structure, relationships |
| **Inductive bias** | Translation invariance | Positional encoding |
| **Computational** | Efficient, optimized | More flexible, scalable |

**Ablation study results**:
- CNN-only: 0.84 AUC
- ViT-only: 0.82 AUC
- CNN + ViT: 0.87 AUC

The combination outperforms either alone by capturing both local and global features.

### Q: Why EfficientNet-B3 specifically?

**A:** EfficientNet-B3 offers a good balance:
- **Accuracy**: Strong performance on ImageNet (81.6% top-1)
- **Efficiency**: Compound scaling optimizes depth, width, and resolution
- **Size**: 12M parameters (manageable for training)
- **Pre-training**: Widely available ImageNet weights

**Why not B0 or B7?**
- B0: Too small, might underfit complex patterns
- B7: Too large (66M params), diminishing returns for this task
- B3: Sweet spot for performance/efficiency trade-off

### Q: Why not use a newer architecture like ConvNeXt or Swin Transformer?

**A:** Design choices considered:

| Model | Pros | Cons | Decision |
|-------|------|------|----------|
| **ConvNeXt** | Modern, pure ConvNet | Less established, fewer pre-trained weights | Future exploration |
| **Swin Transformer** | Hierarchical ViT | More complex, longer training | Future exploration |
| **EfficientNet** | Proven, efficient, good pre-training | Older architecture | **Chosen** |
| **ViT** | Simple, scalable, global attention | Needs more data, no inductive bias | **Combined with CNN** |

For a research prototype, proven architectures reduce variables and ensure stability.

## Fusion Strategy Questions

### Q: Why late fusion (concatenation) instead of early fusion?

**A:** Late fusion preserves modality-specific features:

**Early fusion** (alternative):
```
Image + Clinical → Joint encoder → Prediction
```
- Problem: Forces encoders to adapt to each other too early
- Risk: Loses modality-specific representations

**Late fusion** (chosen):
```
Image → CNN → Features ─┐
Image → ViT → Features ─┼→ Concatenate → Classifier
Clinical → Dense → Features ─┘
```
- Benefit: Each encoder learns optimal representation for its modality
- Cross-modal interactions learned only at final layers
- Ablation showed better performance than early fusion

### Q: How were the clinical network dimensions chosen (8→64→32)?

**A:** Empirical testing with constraints:

| Configuration | Val AUC | Params | Notes |
|--------------|---------|--------|-------|
| 8→16→8 | 0.88 | Small | Underfitting |
| 8→32→16 | 0.885 | Medium | Good |
| **8→64→32** | **0.89** | Medium | **Best** |
| 8→128→64 | 0.888 | Large | Overfitting risk |

64→32 provides sufficient capacity without overfitting on 8 input features.

### Q: Why concatenate instead of attention-based fusion?

**A:** Simplicity and effectiveness:

**Concatenation** (chosen):
- Simple, fast, effective
- Proven in many multimodal papers
- Easy to interpret and debug

**Attention fusion** (alternative):
- Cross-modal attention between features
- More complex, harder to train
- Marginal gains for this task size

For research prototypes, simple effective methods are preferred over complex ones unless complexity is justified by significant gains.

## Training Questions

### Q: Why use transfer learning? Wouldn't training from scratch be more domain-specific?

**A:** Trade-offs favor transfer learning:

| Approach | Data needed | Training time | Performance |
|----------|-------------|---------------|-------------|
| From scratch | 100K+ images | Weeks | Potentially better |
| Transfer learning | 1K-10K images | Hours | Very good |

Medical datasets are typically small. Transfer learning:
- Leverages learned visual features from ImageNet
- Requires less medical data
- Faster training and experimentation
- Better generalization with limited data

### Q: Why freeze early layers of EfficientNet?

**A:** Early layers learn generic features:

**Frozen (first 100 layers)**:
- Edge detectors, color blobs, simple textures
- Transfer well across domains
- Prevents overfitting to small dataset

**Trainable (later layers)**:
- Complex patterns, domain-specific features
- Adapt to retinal images
- Classification head learns task-specific features

This is standard practice in transfer learning for computer vision.

### Q: Why Binary Cross-Entropy loss instead of Focal Loss?

**A:** BCE is simpler and sufficient:

**BCE** (chosen):
```python
loss = -[y*log(p) + (1-y)*log(1-p)]
```
- Standard for binary classification
- Well-understood optimization
- No hyperparameters to tune

**Focal Loss** (alternative):
- Addresses class imbalance by down-weighting easy examples
- Requires tuning γ parameter
- Benefits more for extreme imbalance

Our dataset had moderate balance, so BCE performed adequately. Focal Loss could be explored if class imbalance becomes problematic.

## Inference Questions

### Q: Why FastAPI instead of Flask or Django?

**A:** FastAPI is optimal for ML APIs:

| Framework | Async | Auto-docs | Performance | ML Ecosystem |
|-----------|-------|-----------|-------------|--------------|
| **FastAPI** | ✅ Native | ✅ OpenAPI | ⭐⭐⭐ Excellent | ⭐⭐⭐ Strong |
| Flask | ❌ WSGI | ❌ Manual | ⭐⭐ Good | ⭐⭐ Good |
| Django | ❌ WSGI | ❌ Manual | ⭐⭐ Good | ⭐ Good |

FastAPI's async support is crucial for I/O-bound ML inference, and automatic API documentation is essential for usability.

### Q: Why 224×224 input size?

**A:** Standard size with good trade-offs:

- **Pre-trained models**: EfficientNet-B3 and ViT-Base expect 224×224
- **Memory**: Manageable for batch processing
- **Detail**: Sufficient for retinal vessel patterns
- **Speed**: Fast preprocessing and inference

Larger sizes (512×512) could capture more detail but:
- Require more memory
- Slower training/inference
- Diminishing returns for this task

### Q: Why include both probability and risk level in output?

**A:** Different use cases need different information:

| Output | Use case | Example |
|--------|----------|---------|
| **Probability (0.76)** | Fine-grained decisions, ranking | Comparing patients |
| **Risk Level (High)** | Quick categorization, thresholds | Triage decisions |

Probability provides continuous information; risk level simplifies communication.

## Explainability Questions

### Q: Why Grad-CAM and not other explanation methods?

**A:** Grad-CAM is established and effective:

| Method | Pros | Cons | Use in Project |
|--------|------|------|----------------|
| **Grad-CAM** | Class-discriminative, localization | Lower resolution | **Primary method** |
| Guided Backprop | Fine-grained | Not class-discriminative | Not used |
| LIME | Model-agnostic | Slow, approximations | Not used |
| Integrated Gradients | Axiomatic | Computationally expensive | Not used |

Grad-CAM provides a good balance of effectiveness and computational efficiency for this use case.

### Q: Why SHAP for clinical features?

**A:** SHAP provides rigorous feature attribution:

- **Game-theoretic foundation**: Mathematically grounded
- **Local explanations**: Per-patient feature importance
- **Consistency**: Satisfies desirable properties
- **Implementation**: Well-supported shap library

SHAP answers: "How much does each feature contribute to this specific prediction?"

## Future Architecture Questions

### Q: What would you change in the next version?

**A:** Potential improvements:

1. **Attention fusion**: Replace concatenation with cross-modal attention
2. **Larger ViT**: Try ViT-Large for better global features
3. **Longitudinal analysis**: Process multiple timepoints
4. **Multi-task learning**: Predict additional cardiovascular metrics
5. **Uncertainty quantification**: Add confidence intervals to predictions

### Q: How would you scale this to millions of images?

**A:** Architecture changes for scale:

1. **Model optimization**: Convert to ONNX/TensorRT for faster inference
2. **Batch inference**: Process multiple images simultaneously
3. **Model distillation**: Train smaller student model
4. **Caching**: Cache embeddings for repeated images
5. **Distributed serving**: Multiple model instances behind load balancer

---

*Architecture decisions should always be justified by empirical results and appropriate for the project's scope and constraints.*
