# Model Card Usage Notes

## Overview

This document explains how to read, use, and contribute to the CardioRetina-AI Model Card.

## What is a Model Card?

A **Model Card** is a documentation standard (introduced by Google) that provides structured transparency about machine learning models, including:
- Model architecture and training
- Intended and out-of-scope uses
- Performance characteristics
- Ethical considerations and limitations

## Location

The main model card is located at: `MODEL_CARD.md` in the repository root.

## Model Card Sections Explained

### 1. Model Details

| Field | What It Tells You |
|-------|-----------------|
| **Model Name** | Unique identifier |
| **Version** | Current release |
| **Type** | Task type (classification, regression, etc.) |
| **Architecture** | Technical implementation |
| **Framework** | Software libraries used |
| **License** | Usage rights |

**How to Use**: Verify you have the right model version and understand its basic characteristics.

### 2. Purpose

**What It Tells You**:
- What the model is designed to do
- High-level goal and approach
- Target setting (research vs. production)

**How to Use**: Confirm alignment with your intended application.

### 3. Intended Use

| Aspect | Details |
|--------|---------|
| **Primary** | Main intended application |
| **Secondary** | Other acceptable uses |
| **Population** | Who it's designed for |
| **Users** | Who should use it |

**How to Use**: Verify your use case is within intended scope.

### 4. Out-of-Scope Use

**Critical Section**: Lists prohibited uses.

For CardioRetina-AI:
- ❌ Clinical diagnosis
- ❌ Treatment decisions
- ❌ Replacing medical advice

**How to Use**: Ensure your application doesn't fall into prohibited categories.

### 5. Input Format

**What It Describes**:
- Required input data format
- Image specifications
- Clinical feature requirements
- Preprocessing steps

**How to Use**: Prepare your data to match these specifications exactly.

### 6. Output

**What It Describes**:
- Prediction format
- Probability scales
- Confidence levels
- Additional outputs (Grad-CAM, etc.)

**How to Use**: Interpret predictions correctly based on documented output format.

### 7. Training Data

**What It Describes**:
- Dataset characteristics
- Size and composition
- Preprocessing applied
- Data quality considerations

**How to Use**: Assess applicability to your data distribution.

### 8. Evaluation Metrics

| Metric | Interpretation |
|--------|----------------|
| **Accuracy** | Overall correctness |
| **Precision** | Positive predictive value |
| **Recall** | Sensitivity |
| **AUC-ROC** | Ranking ability |

**How to Use**: Understand expected performance levels and limitations.

### 9. Limitations

**Critical Section**: Known constraints and failure modes.

**How to Use**: Design your application around these limitations.

### 10. Ethical Considerations

**What It Covers**:
- Privacy concerns
- Fairness issues
- Transparency measures
- Autonomy considerations

**How to Use**: Ensure your application respects these ethical dimensions.

## Using the Model Card

### For Researchers

1. **Before using the model**:
   - Read Purpose and Intended Use
   - Verify Out-of-Scope Use doesn't apply
   - Check Limitations section

2. **When citing the model**:
   - Reference the Model Card
   - Include version number
   - Quote relevant sections

3. **When extending the model**:
   - Document changes
   - Update the Model Card
   - Maintain transparency

### For Developers

1. **When integrating**:
   - Follow Input Format specifications
   - Handle Output as documented
   - Respect Out-of-Scope Use restrictions

2. **When deploying**:
   - Include disclaimer in UI
   - Document your deployment context
   - Monitor for issues not in Model Card

### For Reviewers

1. **When evaluating**:
   - Check completeness of Model Card
   - Verify claims match documentation
   - Assess limitation disclosure

2. **When providing feedback**:
   - Suggest missing information
   - Point out inconsistencies
   - Recommend improvements

## Updating the Model Card

### When to Update

Update the Model Card when:
- Model architecture changes
- New evaluation results available
- Additional limitations discovered
- Ethical considerations change
- Intended use cases expand

### How to Update

1. **Make changes**:
   ```bash
   nano MODEL_CARD.md
   ```

2. **Follow format**:
   - Keep table structures intact
   - Maintain consistent formatting
   - Add version history for changes

3. **Commit with clear message**:
   ```bash
   git add MODEL_CARD.md
   git commit -m "docs: update model card with new evaluation results"
   ```

### Version History

Maintain a version history at the end:

```markdown
## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-15 | Initial release |
| 1.0.1 | 2024-02-01 | Updated evaluation metrics |
```

## Model Card Limitations

### What Model Cards Don't Cover

- Detailed API documentation (see API docs)
- Installation instructions (see README)
- Training code details (see source code)
- Real-time performance metrics

### Complementary Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | General project overview |
| **MODEL_CARD.md** | Model-specific information |
| **docs/** | Detailed guides |
| **API docs** | Usage instructions |

## Model Card Best Practices

### For Model Creators

1. **Be honest**: Don't hide limitations
2. **Be specific**: Include concrete numbers
3. **Be current**: Update as model evolves
4. **Be clear**: Use accessible language
5. **Be complete**: Cover all sections

### For Model Users

1. **Read thoroughly**: Don't skip sections
2. **Verify fit**: Check alignment with your use case
3. **Respect limits**: Stay within intended use
4. **Provide feedback**: Report issues or gaps
5. **Stay updated**: Check for new versions

## Creating Model Cards for Variants

If you create a variant of CardioRetina-AI:

1. **Copy the template**:
   ```bash
   cp MODEL_CARD.md MODEL_CARD_VARIANT.md
   ```

2. **Update relevant sections**:
   - Model Name and Version
   - Architecture (if changed)
   - Training Data (if different)
   - Evaluation Metrics (re-run evaluation)
   - Limitations (may differ)

3. **Document lineage**:
   ```markdown
   ## Model Lineage
   Based on: CardioRetina-AI v1.0.0
   Modified: [description of changes]
   ```

## Resources

- [Model Cards for Model Reporting (Google)](https://arxiv.org/abs/1810.03993)
- [Model Cards Toolkit](https://modelcards.withgoogle.com/)
- [About ML Documentation](https://www.partnershiponai.org/aboutml/)

---

*Model Cards are essential tools for responsible AI development and deployment. Use them, contribute to them, and help improve transparency in machine learning.*
