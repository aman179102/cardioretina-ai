# SHAP and Clinical Feature Importance

## Understanding SHAP Values

**SHAP (SHapley Additive exPlanations)** is a game-theoretic approach to explain individual predictions by attributing importance to each input feature.

### Why SHAP for Clinical Data?

While Grad-CAM explains **image regions**, SHAP explains **numerical features**:
- Age, blood pressure, cholesterol values
- Binary indicators (smoking, diabetes)
- Quantitative contribution to each prediction

### Core Concept

SHAP values answer: **"How much does each feature contribute to pushing the prediction away from the baseline?"**

```
Baseline (average prediction) + Σ(SHAP values) = Final Prediction
```

### SHAP Properties

| Property | Description |
|----------|-------------|
| **Efficiency** | Sum of SHAP values equals prediction minus baseline |
| **Symmetry** | Identical features get identical importance |
| **Dummy** | Features that don't change output have zero SHAP |
| **Additivity** | SHAP values sum for combined models |

### Clinical Feature SHAP Analysis

#### Features Analyzed

| Feature | SHAP Interpretation |
|---------|---------------------|
| **Age** | Each year adds/subtracts from risk baseline |
| **Systolic BP** | mmHg above/below normal changes risk |
| **Cholesterol** | mg/dL deviation from healthy range matters |
| **BMI** | Weight status contribution to prediction |
| **Smoking** | Binary impact (smoker vs. non-smoker) |
| **Diabetes** | Condition presence/absence effect |
| **Physical Activity** | Active lifestyle protective factor |

### Visualization Types

#### 1. Summary Plot
```
Feature Importance (across all predictions)

Age          ████████████████████
Systolic BP  ██████████████
Cholesterol  ████████████
Smoking      ████████
Diabetes     ██████
BMI          ████
Diastolic BP ██
Activity     █
```

#### 2. Individual Force Plot
```
Base value: 0.45 (average risk)

Age (65)         +0.12 ████████
BP (145/95)      +0.08 █████
Cholesterol (240)+0.07 ████
Smoking (1)      +0.05 ███
Diabetes (0)     -0.03 ██
BMI (26)         +0.02 █

Final: 0.76 → High Risk
```

#### 3. Waterfall Plot (per prediction)
```
Risk Probability: 0.76

Base        0.45
+ Age       0.57  (+0.12)
+ BP        0.65  (+0.08)
+ Chol      0.72  (+0.07)
+ Smoking   0.77  (+0.05)
- Diabetes  0.74  (-0.03)
+ BMI       0.76  (+0.02)
─────────────────────────
Final       0.76
```

### Implementation Approach

#### For This Project
```python
# Using SHAP library
import shap

explainer = shap.TreeExplainer(model)  # Or KernelExplainer for neural nets
shap_values = explainer.shap_values(clinical_features)

# Visualize
shap.summary_plot(shap_values, clinical_features)
shap.force_plot(explainer.expected_value, shap_values[0], clinical_features[0])
```

#### Neural Network SHAP
For deep learning models, we use:
- **DeepExplainer**: Background samples for baseline
- **GradientExplainer**: Gradient-based approximations
- **KernelExplainer**: Model-agnostic but slower

### Clinical Interpretation

#### High SHAP Values (Increase Risk)
- Age > 60
- Systolic BP > 140
- Total cholesterol > 200
- Smoking = 1
- Diabetes = 1
- Sedentary lifestyle

#### Negative SHAP Values (Decrease Risk)
- Younger age
- Normal blood pressure
- Healthy cholesterol
- Non-smoker
- No diabetes
- Active lifestyle

### Practical Use Cases

#### 1. Patient Explanation
"Your high blood pressure contributed most to this risk assessment, followed by your age."

#### 2. Model Debugging
"Why does the model predict high risk for young, healthy patients?" → Check feature interactions

#### 3. Bias Detection
"Are predictions equally fair across demographic groups?" → Analyze SHAP distributions

### Combining with Grad-CAM

| Aspect | Grad-CAM | SHAP |
|--------|----------|------|
| **Input** | Retinal image | Clinical features |
| **Output** | Spatial heatmap | Feature importance |
| **Use** | "Where does the model look?" | "Which factors matter most?" |
| **Type** | Visual explanation | Numerical explanation |

**Combined insight**: "The model focused on your vessel patterns [Grad-CAM] and your elevated blood pressure was the strongest clinical factor [SHAP]."

### Limitations

1. **Computational cost**: SHAP calculations can be slow for complex models
2. **Approximation**: Some SHAP methods are approximations
3. **Correlation**: Correlated features share importance
4. **Baseline choice**: Different baselines yield different explanations

### Best Practices

- **Consistent baseline**: Use dataset mean or zero
- **Multiple samples**: Don't rely on single SHAP values
- **Feature scaling**: Normalized features for fair comparison
- **Expert review**: Have clinicians validate explanations

---

*SHAP provides mathematical rigor to clinical feature importance, complementing Grad-CAM's visual explanations for complete model transparency.*
