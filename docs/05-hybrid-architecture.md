# Hybrid CNN + ViT Architecture

## Architecture Philosophy

CardioRetina-AI uses a **hybrid approach** combining the strengths of Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs) for comprehensive retinal image analysis.

### Why Hybrid?

#### CNN Strengths
- **Local feature extraction**: Excellent at detecting edges, textures, and small patterns
- **Translation invariance**: Recognizes features regardless of position
- **Hierarchical representation**: Builds from simple to complex features
- **Computational efficiency**: Well-optimized for image tasks

#### ViT Strengths
- **Global context**: Captures long-range dependencies across the image
- **Attention mechanism**: Focuses on relevant regions adaptively
- **Patch-based processing**: Handles large images effectively
- **Transfer learning**: Benefits from pre-trained weights

### Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT (224×224 RGB)                       │
└──────────────────┬───────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────┐      ┌─────────────────┐
│ EfficientNet │      │   Vision Transformer   │
│    B3        │      │   (ViT-Base-16)        │
└──────┬───────┘      └────────┬────────┘
       │                       │
       │ Local Features        │ Global Context
       │ (geometric patterns)  │ (spatial relationships)
       │                       │
       └──────────┬────────────┘
                  │
                  ▼
       ┌────────────────────┐
       │  Feature Fusion    │
       │  (Concatenation)   │
       └────────┬───────────┘
                │
                ▼
       ┌────────────────────┐
       │  Clinical Network  │
       │  (8 → 64 → 32)     │
       └────────┬───────────┘
                │
                ▼
       ┌────────────────────┐
       │  Classifier Head   │
       │  (128 → 64 → 32 → 1)│
       └────────┬───────────┘
                │
                ▼
       ┌────────────────────┐
       │   Sigmoid Output   │
       │  Risk Probability  │
       └────────────────────┘
```

### Component Details

#### 1. EfficientNet-B3 Backbone
- **Pre-trained**: ImageNet weights for feature initialization
- **Compound scaling**: Balanced depth, width, and resolution
- **Frozen early layers**: First 100 layers frozen for transfer learning
- **Output**: 1536-dimensional feature vector

#### 2. Vision Transformer Module
- **Model**: ViT-Base-Patch16-224
- **Patch size**: 16×16 pixels
- **Embedding dimension**: 768
- **Projection**: Maps to 512-dimensional space
- **Attention heads**: 12, capturing multi-scale relationships

#### 3. Clinical Data Network
- **Input**: 8 clinical features (age, BP, cholesterol, etc.)
- **Architecture**: Dense layers (64 → 32)
- **Activation**: ReLU with BatchNorm
- **Dropout**: 0.3 for regularization

#### 4. Fusion Layer
- **Concatenation**: EfficientNet features + ViT features + Clinical features
- **Total dimensions**: 1536 + 512 + 32 = 2080 (compressed to 128)
- **Processing**: 128 → 64 → 32 with BatchNorm

#### 5. Classification Head
- **Layers**: 128 → 64 → 32 → 1
- **Activation**: ReLU (hidden), Sigmoid (output)
- **Output**: Risk probability [0, 1]

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| EfficientNet-B3 | Good balance of accuracy and efficiency |
| ViT-Base | Strong global context without excessive parameters |
| Concatenation fusion | Preserves all feature information |
| BatchNorm | Stabilizes training, reduces internal covariate shift |
| Dropout 0.3 | Prevents overfitting without hurting convergence |

### Training Configuration

- **Loss**: Binary Cross-Entropy
- **Optimizer**: Adam (lr=0.001, weight_decay=1e-4)
- **Scheduler**: ReduceLROnPlateau (patience=5, factor=0.5)
- **Early stopping**: Patience=10 epochs

### Ablation Support

The architecture supports modular configurations:
- **CNN-only**: Remove ViT and Clinical branches
- **ViT-only**: Remove CNN and Clinical branches
- **CNN+ViT**: Remove Clinical branch
- **Full**: All three components active

---

*This hybrid design maximizes information extraction from both local patterns and global retinal structures.*
