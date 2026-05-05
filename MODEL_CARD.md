# Model Card: CardioRetina-AI

## Model Details

| Field | Value |
|-------|-------|
| **Model Name** | CardioRetina-AI |
| **Version** | 1.0.0 |
| **Type** | Binary Classification (Heart Disease Risk) |
| **Architecture** | Hybrid EfficientNet-B3 + Vision Transformer + Clinical Data Fusion |
| **Framework** | PyTorch |
| **License** | MIT |

## Purpose

CardioRetina-AI predicts cardiovascular disease risk from retinal fundus photographs combined with clinical health metrics. It aims to support non-invasive cardiovascular screening in research and educational settings.

## Intended Use

- **Primary**: Research prototype for studying retinal-cardiovascular associations
- **Secondary**: Educational tool for deep learning in healthcare
- **Population**: General adult population with available retinal fundus images
- **Users**: Researchers, students, and developers working on medical AI

## Out-of-Scope Use

- **Clinical diagnosis or treatment decisions**
- **Replacing professional medical advice**
- **Screening without medical professional oversight**
- **Use with non-fundus images (OCT, fluorescein angiography, etc.)**
- **Pediatric patients (model trained on adult populations)**

## Input Format

### Retinal Image
- Format: JPEG, PNG, BMP, or TIFF
- Size: Automatically resized to 224x224 RGB
- Type: Retinal fundus photograph (color)
- Preprocessing: CLAHE enhancement, normalization, optional denoising

### Clinical Features (8 numeric values)
| Feature | Range | Unit |
|---------|-------|------|
| Age | 0-120 | years |
| Systolic BP | 50-300 | mmHg |
| Diastolic BP | 30-200 | mmHg |
| Cholesterol | 50-600 | mg/dL |
| BMI | 10-70 | kg/m² |
| Smoking | 0 or 1 | binary |
| Diabetes | 0 or 1 | binary |
| Physical Activity | 0 or 1 | binary |

## Output

- **risk_probability**: Float [0, 1] indicating heart disease risk
- **risk_level**: "Low" (<0.4), "Moderate" (0.4-0.7), "High" (>0.7)
- **confidence**: Model confidence in the prediction
- **clinical_factors**: Individual factor assessments
- **gradcam_url**: Optional Grad-CAM heatmap showing contributing retinal regions

## Training Data Requirements

- Labeled retinal fundus images with binary heart disease risk labels
- Associated clinical metadata (8 features listed above)
- Minimum recommended: 1,000+ images per class
- Expected class distribution: ~50/50 or with class weight adjustment

## Evaluation Metrics

Metrics are generated after training on a labeled dataset:
- Accuracy, Precision, Recall, Specificity
- F1-Score, AUC-ROC
- Confusion Matrix
- Precision-Recall Curve
- Per-class classification report

> No fake metrics are reported. Results will be available after training.

## Limitations

1. **Not clinically validated** — no regulatory approval
2. **Dataset bias** — performance depends on training data diversity
3. **Single-image analysis** — does not consider longitudinal changes
4. **Camera variability** — may not generalize across different fundus cameras
5. **Demographic bias** — may underperform on underrepresented populations
6. **Interpretability** — Grad-CAM highlights are informational, not diagnostic

## Ethical Considerations

- **Privacy**: Retinal images are biometric data; handle with appropriate security
- **Fairness**: Model should be validated across demographic groups before any deployment
- **Transparency**: Grad-CAM and SHAP provide explanation, but these are not clinical evidence
- **Autonomy**: This tool should augment, never replace, clinical judgment
- **Access**: Designed to potentially improve healthcare access in resource-limited settings

## Medical Disclaimer

This project is a research prototype for educational and experimental use only. It is not intended for clinical diagnosis, treatment decisions, or as a substitute for professional medical advice. Always consult a qualified healthcare professional. The model has not been evaluated or approved by any regulatory body (FDA, CE, etc.).

## References

1. Poplin et al. (2018). Nature Biomedical Engineering, 2(3), 158-164.
2. Wong & Mitchell (2004). NEJM, 351(22), 2310-2317.
3. Tan & Le (2019). EfficientNet. ICML 2019.
4. Dosovitskiy et al. (2021). ViT. ICLR 2021.
5. Selvaraju et al. (2017). Grad-CAM. ICCV 2017.
