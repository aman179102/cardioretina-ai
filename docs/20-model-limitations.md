# Model Limitations

## Overview

Understanding the limitations of CardioRetina-AI is essential for appropriate use and interpretation.

## Research Prototype Status

### Not Clinically Validated

**This model has NOT been:**
- Tested in clinical settings
- Validated on diverse patient populations
- Approved by any regulatory body (FDA, CE, etc.)
- Subject to clinical trials
- Peer-reviewed by medical professionals

### Appropriate Use Only

**This model IS intended for:**
- Research and experimentation
- Educational purposes
- Methodology development
- Algorithm comparison

**This model is NOT intended for:**
- Clinical diagnosis
- Patient care decisions
- Health screening programs
- Insurance or employment decisions

## Dataset Limitations

### Training Data Dependency

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Size** | Small datasets lead to poor generalization | Use larger, diverse datasets |
| **Quality** | Low-quality images reduce accuracy | Strict quality control |
| **Diversity** | Homogeneous populations limit applicability | Collect diverse data |
| **Bias** | Dataset bias leads to model bias | Audit and address biases |

### Potential Dataset Biases

1. **Demographic Bias**
   - Underrepresentation of certain age groups
   - Limited ethnic diversity
   - Geographic concentration

2. **Equipment Bias**
   - Single camera type in training data
   - Specific imaging protocols
   - Particular clinic settings

3. **Selection Bias**
   - Referral population characteristics
   - Severity spectrum limitations
   - Comorbidity patterns

## Technical Limitations

### Image Quality Requirements

| Factor | Requirement | Consequence if Not Met |
|--------|-------------|----------------------|
| Resolution | Minimum 512×512 | Poor vessel detection |
| Focus | Sharp images | Blur reduces accuracy |
| Field of View | Standard 45° | Non-standard angles may fail |
| Color | True color fundus | OCT or angiography not supported |
| Artifacts | Minimal | Glare/blur affects predictions |

### Input Constraints

**Supported:**
- Color fundus photographs
- Standard clinical metrics (age, BP, cholesterol, etc.)
- Binary risk classification

**Not Supported:**
- OCT images
- Fluorescein angiography
- Pediatric patients (trained on adults)
- Longitudinal analysis (single-image only)

### Output Limitations

| Output | Interpretation | Limitation |
|--------|----------------|------------|
| **Risk Probability** | 0-1 scale | Not calibrated to actual risk rates |
| **Risk Level** | Low/Mod/High | Arbitrary thresholds (0.4, 0.7) |
| **Grad-CAM** | Highlighted regions | Correlation, not causation |
| **SHAP Values** | Feature importance | Approximate explanations |

## Performance Limitations

### Accuracy Constraints

- **Not 100% accurate**: Will make incorrect predictions
- **Threshold dependent**: Performance varies by classification threshold
- **Class imbalance sensitive**: May favor majority class

### Generalization Limits

| Scenario | Expected Performance |
|----------|---------------------|
| Similar to training data | Good |
| Different camera type | Degraded |
| Different population | Unknown/Degraded |
| Unusual presentations | Potentially poor |
| Edge cases | Unpredictable |

### Failure Modes

**Cases where model may fail:**
1. Severe image artifacts
2. Unusual anatomy (post-surgical, congenital)
3. Co-existing eye diseases (cataracts, glaucoma)
4. Very young or very old patients
5. Unusual clinical presentations

## Explainability Limitations

### Grad-CAM Constraints

- **Spatial resolution**: Limited to conv layer resolution
- **Class-specific**: Only explains one class at a time
- **Correlation not causation**: Highlights correlated regions, not necessarily causal
- **Human interpretation**: Requires expert knowledge to interpret

### SHAP Limitations

- **Approximation**: Some SHAP methods are approximations
- **Correlated features**: Shared importance among correlated features
- **Computational cost**: Can be slow for large models
- **Baseline sensitivity**: Results depend on baseline choice

## Ethical and Legal Limitations

### Privacy Concerns

- **Biometric data**: Retinal images can identify individuals
- **Protected health information**: Subject to HIPAA/GDPR
- **Consent requirements**: Proper consent needed for any real data

### Liability

- **No warranty**: Provided as-is without guarantees
- **No liability**: Authors not responsible for misuse
- **Not a medical device**: Not subject to medical device regulations

### Fairness Concerns

- **Demographic disparities**: May perform differently across populations
- **Access inequities**: Technology may not be equally accessible
- **Confirmation bias**: Risk of confirming existing biases

## Environmental Limitations

### Computational Requirements

| Resource | Minimum | Limitation |
|----------|---------|------------|
| GPU | Optional | Slow without GPU |
| RAM | 8GB | Large datasets need more |
| Storage | 10GB | Checkpoints and data use space |

### Deployment Constraints

- **Model size**: ~100MB for full model
- **Inference time**: ~100-200ms per image (GPU)
- **Batch processing**: Limited by available memory

## Interpretation Guidelines

### Do

✅ Use as a research and educational tool
✅ Compare with other methods
✅ Generate hypotheses for further study
✅ Teach medical AI concepts
✅ Understand model behavior

### Don't

❌ Use for actual patient diagnosis
❌ Make treatment decisions based on output
❌ Replace professional medical advice
❌ Use without understanding limitations
❌ Deploy in clinical settings

## Future Improvements Needed

### Technical

- [ ] Larger and more diverse training datasets
- [ ] Multi-center validation studies
- [ ] Calibration of probability outputs
- [ ] Longitudinal analysis capabilities
- [ ] Uncertainty quantification

### Clinical

- [ ] External validation cohorts
- [ ] Prospective clinical studies
- [ ] Regulatory approval pathway
- [ ] Clinical workflow integration
- [ ] Physician training materials

### Ethical

- [ ] Fairness audits across demographics
- [ ] Bias detection and mitigation
- [ ] Explainability improvements
- [ ] Stakeholder engagement
- [ ] Impact assessment

---

*Understanding limitations is as important as understanding capabilities. Always use this tool responsibly and within its intended scope.*
