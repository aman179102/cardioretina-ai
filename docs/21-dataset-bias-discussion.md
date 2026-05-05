# Dataset Bias Discussion

## Overview

Dataset bias is a critical concern in medical AI that can lead to unfair and inaccurate predictions for underrepresented populations.

## Types of Bias in Retinal Datasets

### 1. Demographic Bias

| Bias Type | Example | Impact |
|-----------|---------|--------|
| **Age bias** | Overrepresentation of elderly patients | Poor performance on young adults |
| **Gender bias** | Skewed gender distribution | Different accuracy across genders |
| **Ethnic bias** | Limited ethnic diversity | Poor generalization to other populations |
| **Geographic bias** | Single location/center | Regional variations not captured |

### 2. Socioeconomic Bias

- **Healthcare access**: Different populations have different screening rates
- **Camera quality**: Resource-limited settings may have lower-quality images
- **Referral patterns**: Tertiary centers see more severe cases

### 3. Disease Spectrum Bias

| Aspect | Potential Bias | Effect |
|--------|----------------|--------|
| **Severity** | Only severe cases included | Poor detection of early disease |
| **Comorbidities** | Specific comorbidity patterns | Fails on atypical presentations |
| **Progression stage** | Single time point | No longitudinal understanding |

### 4. Technical Bias

- **Camera types**: Different fundus cameras produce different image characteristics
- **Imaging protocols**: Variations in lighting, focus, field of view
- **Image quality**: Higher-quality images from better-resourced settings

## Detecting Bias

### Statistical Methods

```python
# Check demographic distribution
df['age_group'].value_counts(normalize=True)
df['ethnicity'].value_counts(normalize=True)
df['gender'].value_counts(normalize=True)

# Compare with population statistics
population_age_dist = [...]
dataset_age_dist = df['age_group'].value_counts(normalize=True)

# Statistical test for difference
from scipy.stats import chisquare
chi2, p = chisquare(dataset_age_dist, population_age_dist)
```

### Performance Disparities

```python
# Evaluate by subgroup
for group in df['ethnicity'].unique():
    mask = df['ethnicity'] == group
    group_auc = roc_auc_score(y_true[mask], y_pred[mask])
    print(f"{group}: AUC = {group_auc:.3f}")
```

## Mitigation Strategies

### 1. Data Collection

| Strategy | Implementation |
|----------|----------------|
| **Stratified sampling** | Ensure proportional representation |
| **Multi-center data** | Collect from diverse locations |
| **Broad inclusion criteria** | Minimize exclusion of edge cases |
| **Community partnerships** | Engage underrepresented communities |

### 2. Data Augmentation

```python
# Synthetic data generation (with caution)
# Domain randomization for camera types
# Demographic-preserving transformations
```

### 3. Algorithmic Approaches

| Method | Description |
|--------|-------------|
| **Reweighting** | Adjust sample weights by group |
| **Adversarial debiasing** | Train to be invariant to protected attributes |
| **Fairness constraints** | Add fairness regularization to loss |
| **Post-processing** | Adjust thresholds by group |

### 4. Evaluation Practices

- Report metrics by demographic subgroup
- Use fairness metrics (equalized odds, demographic parity)
- Test on external validation sets from different populations
- Conduct regular bias audits

## Fairness Metrics

### Key Metrics to Track

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Demographic Parity** | P(Ŷ=1\|A=0) = P(Ŷ=1\|A=1) | Equal positive prediction rates |
| **Equalized Odds** | P(Ŷ=1\|Y=y,A=0) = P(Ŷ=1\|Y=y,A=1) | Equal TPR and FPR across groups |
| **Calibration** | P(Y=1\|Ŷ=p,A=0) = P(Y=1\|Ŷ=p,A=1) | Predicted probabilities accurate for all groups |

### Implementation

```python
from sklearn.metrics import confusion_matrix

def equalized_odds_difference(y_true, y_pred, sensitive_attr):
    groups = sensitive_attr.unique()
    tpr_by_group = {}
    fpr_by_group = {}
    
    for group in groups:
        mask = sensitive_attr == group
        tn, fp, fn, tp = confusion_matrix(y_true[mask], y_pred[mask]).ravel()
        tpr_by_group[group] = tp / (tp + fn)
        fpr_by_group[group] = fp / (fp + tn)
    
    tpr_diff = max(tpr_by_group.values()) - min(tpr_by_group.values())
    fpr_diff = max(fpr_by_group.values()) - min(fpr_by_group.values())
    
    return tpr_diff, fpr_diff
```

## Ethical Considerations

### Protected Attributes

Attributes requiring special consideration:
- Race/ethnicity
- Gender
- Age
- Socioeconomic status
- Geographic location
- Insurance status

### Disclosure Requirements

Document in MODEL_CARD.md:
- Dataset demographic composition
- Known biases and limitations
- Performance by subgroup (if available)
- Mitigation strategies employed

## Case Study: Retinal Imaging

### Known Issues in Literature

1. **Population differences**: Retinal vessel patterns vary by ethnicity
2. **Camera variations**: Different devices produce systematically different images
3. **Disease prevalence**: Cardiovascular disease rates vary by demographics

### Recommendations

1. **Collect diverse data**: Prioritize underrepresented populations
2. **Validate externally**: Test on completely independent cohorts
3. **Monitor continuously**: Track performance metrics post-deployment (for research)
4. **Engage stakeholders**: Include affected communities in development
5. **Be transparent**: Clearly document limitations and intended use

## Checklist for Bias Awareness

### Before Training

- [ ] Analyzed dataset demographic distribution
- [ ] Compared to target population demographics
- [ ] Identified potential bias sources
- [ ] Planned mitigation strategies

### During Training

- [ ] Used appropriate sampling/weighting
- [ ] Monitored per-group metrics
- [ ] Tested fairness interventions

### After Training

- [ ] Evaluated on diverse test sets
- [ ] Reported subgroup performance
- [ ] Documented limitations clearly
- [ ] Made model card transparent

## Resources

- [Fairness Indicators (TensorFlow)](https://www.tensorflow.org/responsible_ai/fairness_indicators)
- [AI Fairness 360 (IBM)](https://aif360.res.ibm.com/)
- [Partnership on AI](https://www.partnershiponai.org/)
- [Equality of Opportunity in Supervised Learning](https://arxiv.org/abs/1610.02413)

---

*Addressing dataset bias is essential for developing fair and trustworthy medical AI systems.*
