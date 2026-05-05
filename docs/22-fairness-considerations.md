# Fairness Considerations

## Overview

Fairness in medical AI ensures that models perform equitably across different demographic groups and don't perpetuate or amplify existing healthcare disparities.

## Why Fairness Matters in Medical AI

### Healthcare Disparities

- **Existing inequities**: Healthcare access and outcomes vary by demographics
- **AI amplification**: Models can perpetuate or worsen these disparities
- **Trust erosion**: Unfair models undermine trust in AI-assisted care
- **Ethical obligations**: Obligation to do no harm and ensure equitable benefit

### Potential Harms

| Harm Type | Description | Example |
|-----------|-------------|---------|
| **Allocation harm** | Unequal resource distribution | Screening access denied to certain groups |
| **Representation harm** | Stereotyping or demeaning | Assuming higher risk based on demographics |
| **Quality of service** | Different accuracy across groups | Better performance for majority population |
| **Stereotyping** | Reinforcing negative stereotypes | Associating certain groups with disease |

## Fairness Definitions

### 1. Demographic Parity

**Definition**: Equal positive prediction rates across groups

```
P(Ŷ = 1 | A = 0) = P(Ŷ = 1 | A = 1)
```

**When to use**: When positive predictions should be equally distributed

**Limitation**: May be impossible when base rates differ

### 2. Equalized Odds

**Definition**: Equal true positive and false positive rates across groups

```
P(Ŷ = 1 | Y = y, A = 0) = P(Ŷ = 1 | Y = y, A = 1)  for y ∈ {0, 1}
```

**When to use**: When model errors should be similar across groups

**Trade-off**: May conflict with overall accuracy optimization

### 3. Calibration (Predictive Parity)

**Definition**: Predicted probabilities reflect true probabilities equally across groups

```
P(Y = 1 | Ŷ = p, A = 0) = P(Y = 1 | Ŷ = p, A = 1) = p
```

**When to use**: When probability outputs should be equally reliable

**Note**: Can conflict with equalized odds when base rates differ

## Fairness in CardioRetina-AI Context

### Protected Attributes

| Attribute | Consideration | Sensitivity |
|-----------|----------------|-------------|
| **Age** | Cardiovascular risk varies by age | Age-adjusted evaluation needed |
| **Gender** | Different baseline risk profiles | Separate calibration may help |
| **Ethnicity** | Disease prevalence varies | Critical for fairness assessment |
| **Geography** | Healthcare access differences | Important for deployment equity |

### Model-Specific Considerations

1. **Age bias**: Model trained primarily on elderly may perform poorly on young adults
2. **Camera bias**: Different devices may produce systematically different images
3. **Clinical context**: Normal ranges vary by demographics (BP, cholesterol)

## Assessment Methods

### Subgroup Analysis

```python
def evaluate_by_subgroup(y_true, y_pred, subgroup_labels):
    results = {}
    for subgroup in np.unique(subgroup_labels):
        mask = subgroup_labels == subgroup
        results[subgroup] = {
            'accuracy': accuracy_score(y_true[mask], y_pred[mask]),
            'precision': precision_score(y_true[mask], y_pred[mask]),
            'recall': recall_score(y_true[mask], y_pred[mask]),
            'auc': roc_auc_score(y_true[mask], y_pred[mask])
        }
    return results
```

### Fairness Auditing

| Audit Type | Purpose | Method |
|------------|---------|--------|
| **Pre-training** | Check dataset balance | Demographic analysis |
| **In-training** | Monitor fairness metrics | Regular fairness evaluation |
| **Post-training** | Validate fairness claims | Subgroup testing |
| **Deployment** | Detect drift in fairness | Continuous monitoring |

## Mitigation Approaches

### 1. Pre-processing

**Data-level interventions:**
- Reweighting samples by group
- Synthetic data generation for underrepresented groups
- Adversarial removal of protected attribute signals

### 2. In-processing

**Algorithm-level interventions:**
- Fairness constraints in optimization
- Adversarial debiasing
- Multi-task learning with fairness objectives

### 3. Post-processing

**Prediction-level interventions:**
- Threshold adjustment by group
- Calibration by group
- Reject option classification

## Implementation Guidelines

### For This Project

Given this is a research prototype:

1. **Measure disparities**
   - Report metrics by demographic group
   - Identify performance gaps
   - Document in model card

2. **Be transparent**
   - Acknowledge dataset limitations
   - State known biases
   - Declare intended use cases

3. **Set expectations**
   - Not for clinical deployment
   - Requires validation on target population
   - Fairness audit needed before real use

### Fairness Checklist

- [ ] Analyzed dataset demographic composition
- [ ] Identified potential bias sources
- [ ] Measured performance by subgroup
- [ ] Reported fairness metrics
- [ ] Documented limitations
- [ ] Considered intersectional fairness
- [ ] Planned mitigation strategies

## Trade-offs and Tensions

### Fairness vs. Accuracy

- Optimizing for overall accuracy may harm minority groups
- Fairness constraints may reduce overall performance
- Need to balance based on application context

### Different Fairness Definitions

**Impossibility theorem**: Generally impossible to satisfy multiple fairness definitions simultaneously when base rates differ.

| Fairness Type | Trade-off |
|---------------|-----------|
| Demographic parity | May require different thresholds |
| Equalized odds | May reduce calibration |
| Calibration | May conflict with equalized odds |

### Recommendation

- Choose fairness definition based on application context
- Be transparent about chosen definition and trade-offs
- Engage stakeholders in decision-making

## Stakeholder Engagement

### Who to Consult

- **Clinicians**: Understand clinical fairness requirements
- **Patients/Affected communities**: Understand lived experience
- **Ethicists**: Navigate ethical trade-offs
- **Regulators**: Ensure compliance requirements

### Questions to Ask

1. What does fairness mean in this clinical context?
2. Which errors are more harmful (false positives vs. false negatives)?
3. How do different groups experience the healthcare system?
4. What are the consequences of algorithmic errors?

## Documentation

### Model Card Fairness Section

```markdown
## Fairness

### Intended Use
This model is for research and educational purposes only.

### Factors
- Age
- Gender (if available in dataset)

### Evaluation Data
Limited demographic information available.

### Metrics
- Overall AUC-ROC: 0.89
- Performance by demographic group: Not evaluated (insufficient data)

### Ethical Considerations
- Dataset primarily from [specific population]
- May not generalize to other populations
- Not validated for clinical use in any population

### Caveats and Recommendations
- Fairness audit needed before deployment
- External validation on target population required
- Continuous monitoring for performance disparities
```

## Resources

- [Fairness in Machine Learning](https://fairmlbook.org/)
- [Google AI Principles](https://ai.google/principles/)
- [Microsoft Responsible AI](https://www.microsoft.com/en-us/ai/responsible-ai)
- [ACM Code of Ethics](https://www.acm.org/code-of-ethics)

---

*Fairness is not just a technical problem but a socio-technical challenge requiring diverse perspectives and ongoing attention.*
