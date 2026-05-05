# Grad-CAM Explainability Flow

## What is Grad-CAM?

**Gradient-weighted Class Activation Mapping (Grad-CAM)** is a technique that visualizes which regions of an input image contribute most to the model's prediction.

### Why Explainability Matters

In medical AI, **transparency is crucial**:
- **Trust**: Users need to understand why a prediction was made
- **Debugging**: Developers can identify model biases
- **Validation**: Experts can verify if reasoning aligns with medical knowledge
- **Regulatory**: Future approval processes require explainability

### How Grad-CAM Works

```
┌──────────────────────────────────────────────────────────────┐
│                    GRAD-CAM PROCESS                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. FORWARD PASS                                              │
│     ┌───────────┐    ┌───────────┐    ┌───────────┐          │
│     │   Input   │───▶│   CNN     │───▶│  Output   │          │
│     │  Image    │    │  Layers   │    │  Class    │          │
│     └───────────┘    └─────┬─────┘    └───────────┘          │
│                            │                                  │
│  2. CAPTURE ACTIVATIONS    │                                  │
│     Save feature maps from the final convolutional layer       │
│                                                               │
│  3. BACKWARD PASS          │                                  │
│     ┌───────────┐    ┌───────────┐                           │
│     │   Gradients│◀───│   Loss    │                           │
│     │  (w.r.t.  │    │  w.r.t.   │                           │
│     │  features)│    │  class)   │                           │
│     └─────┬─────┘    └───────────┘                           │
│           │                                                   │
│  4. WEIGHT CALCULATION                                        │
│     Global Average Pooling of gradients → weights            │
│                                                               │
│  5. WEIGHTED COMBINATION                                      │
│     ┌─────────────┐                                           │
│     │  CAM = Σ(wᵢ│  ×  Aᵢ)                                   │
│     │  activation │                                           │
│     │   weighted  │                                           │
│     │   by grads  │                                           │
│     └──────┬──────┘                                           │
│            │                                                   │
│  6. POST-PROCESSING                                           │
│            ▼                                                   │
│     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│     │   ReLU     │───▶│  Normalize  │───▶│   Resize    │     │
│     │(only pos)  │    │   0 to 1    │    │ to img size │     │
│     └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                               │
│  7. OVERLAY                                                   │
│     Heatmap + Original Image = Interpretable Visualization     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Implementation Details

#### Target Layer Selection
- **EfficientNet-B3**: `features[-1]` or `conv_head`
- **Why last conv layer?**: Captures high-level semantic features
- **Spatial resolution**: Typically 7×7 or 14×14 before pooling

#### Gradient Flow
```python
# Pseudo-code
features = model.forward_to_target_layer(image)
output = model.classifier(features)
output[target_class].backward()

gradients = features.grad  # [batch, channels, h, w]
weights = gradients.mean(dim=(2,3))  # GAP per channel

cam = (weights * features).sum(dim=1)  # Weighted sum
cam = F.relu(cam)  # Only positive contributions
cam = normalize(cam)
```

### Visualization Output

The Grad-CAM heatmap shows:
- **Red/Yellow areas**: High importance (contribute to risk prediction)
- **Blue/Dark areas**: Low importance (not significant for prediction)
- **Overlay**: Heatmap superimposed on original retinal image

### Retinal-Specific Insights

Typical highlighted regions:
- **Optic disc**: Often important, contains vessel origins
- **Macula**: Central vision area, microvasculature patterns
- **Vessel crossings**: Arteriovenous nicking indicators
- **Peripheral vessels**: Tortuosity and branching patterns

### API Integration

```python
# Endpoint: GET /gradcam/{prediction_id}
{
  "gradcam_url": "/static/gradcam_abc123.png",
  "highlights": [
    "optic_disc_region",
    "superior_vessel_arcade",
    "macular_area"
  ],
  "confidence": "high"
}
```

### Limitations

1. **Spatial resolution**: Limited to conv layer resolution
2. **Class-specific**: Only explains one class at a time
3. **Not causal**: Shows correlation, not causation
4. **Human interpretation**: Still requires expert validation

### Best Practices

- **Multiple samples**: Review across diverse cases
- **Expert validation**: Have ophthalmologists review
- **Comparison**: Compare with known pathological features
- **Documentation**: Record which regions are typically highlighted

---

*Grad-CAM transforms black-box predictions into interpretable visualizations, crucial for medical AI trust and validation.*
