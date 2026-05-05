# Official Project Overview

## CardioRetina-AI

**CardioRetina-AI** is a research-to-production deep learning system designed to predict cardiovascular disease risk using retinal fundus images combined with clinical health metrics.

### Project Vision

This project bridges the gap between cutting-edge medical AI research and practical implementation, providing a complete pipeline from data preprocessing to deployment-ready inference API.

### Core Capabilities

1. **Multimodal Analysis**: Combines retinal image features with clinical data (blood pressure, cholesterol, BMI, etc.)
2. **Explainable AI**: Provides Grad-CAM visualizations and SHAP feature importance for transparency
3. **Production Ready**: Includes FastAPI server, Docker containers, and comprehensive testing
4. **Research Focused**: Ablation studies, evaluation metrics, and reproducibility tools

### Target Audience

- **Researchers**: Studying retinal-cardiovascular associations
- **Developers**: Building medical AI applications
- **Students**: Learning deep learning in healthcare contexts
- **Educators**: Teaching medical AI concepts

### Project Status

This is a research prototype for educational and experimental purposes. It demonstrates:
- Hybrid CNN + Transformer architectures
- Clinical data fusion techniques
- Explainable AI methods
- Production deployment patterns

### Repository Structure

```
cardioretina-ai/
├── cardioretina/      # Core Python package
├── docs/              # Documentation files
├── frontend/          # Web dashboard
├── tests/             # Test suite
├── docker/            # Container configurations
└── config/            # Training configurations
```

### Quick Links

- [README](../README.md) - Main documentation
- [MODEL_CARD](../MODEL_CARD.md) - Model documentation
- [DATASET](../DATASET.md) - Dataset specifications
- [REPRODUCIBILITY](../REPRODUCIBILITY.md) - Reproduction guide

---

*Last updated: Documentation polish phase*
