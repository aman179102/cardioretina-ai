# Changelog

## Overview

All notable changes to the CardioRetina-AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Additional documentation files in docs/ folder
- Expanded troubleshooting guide
- Common setup errors guide
- Future work roadmap
- Publication readiness checklist

## [1.0.0] - 2024-01-15

### Added - Core Features

#### Model Architecture
- Hybrid CNN + ViT + Clinical fusion architecture
- EfficientNet-B3 backbone for local feature extraction
- ViT-Base-Patch16-224 for global context
- Clinical data network (8 → 64 → 32 features)
- Late fusion strategy with concatenation
- Classification head with dropout regularization

#### Training Pipeline
- Complete training script with CLI interface
- Support for custom configuration files (YAML)
- Transfer learning from ImageNet weights
- Early stopping with patience configuration
- Learning rate scheduling (ReduceLROnPlateau)
- Mixed precision training support
- Training history logging (JSON and CSV)
- Model checkpointing (best and periodic)

#### Evaluation Tools
- Comprehensive evaluation script
- Metrics: accuracy, precision, recall, specificity, F1, AUC-ROC, AUC-PR
- Confusion matrix generation
- ROC and PR curve plotting
- Ablation study framework
- Per-class metrics breakdown

#### Data Pipeline
- CSV-based dataset loading
- Automatic data validation
- Train/validation/test splitting
- CLAHE image enhancement
- Data augmentation (flip, rotation, color jitter)
- Custom dataset class for PyTorch

#### Inference API
- FastAPI-based REST API
- Endpoints:
  - `/` - Web dashboard
  - `/health` - Health check
  - `/predict` - Risk prediction
  - `/gradcam/{id}` - Grad-CAM visualization
  - `/model-info` - Model metadata
  - `/docs` - Swagger documentation
- Multipart form data support
- Async request handling

#### Web Dashboard
- Interactive HTML interface
- Drag-and-drop image upload
- Clinical data form (8 features)
- Real-time risk prediction display
- Risk gauge visualization
- Grad-CAM heatmap display
- Responsive design

#### Explainability
- Grad-CAM implementation for CNN
- SHAP integration for clinical features
- Feature importance visualization
- Risk factor breakdown
- Confidence indicators

#### Deployment
- Docker support with Dockerfile
- Docker Compose configuration
- GPU support (NVIDIA Docker)
- Health checks
- Environment variable configuration

#### Documentation
- Comprehensive README.md
- Model Card (MODEL_CARD.md)
- Dataset documentation (DATASET.md)
- Reproducibility guide (REPRODUCIBILITY.md)
- 40+ additional documentation files in docs/
- Architecture diagrams
- Usage guides
- API documentation (auto-generated)

#### Development Tools
- GitHub Actions CI/CD pipeline
- pytest test suite
- ruff linting
- mypy type checking
- Pre-commit hooks configuration

#### Export
- ONNX export functionality
- Model serialization utilities

### Technical Details

#### Dependencies
- PyTorch 2.0+
- torchvision 0.15+
- timm 0.9+
- FastAPI 0.100+
- grad-cam 1.4.8
- shap 0.42.0
- Standard scientific Python stack (numpy, pandas, scikit-learn)

#### Project Structure
```
cardioretina-ai/
├── cardioretina/          # Main package
│   ├── api/              # FastAPI application
│   ├── data/             # Data pipeline
│   ├── evaluation/       # Evaluation tools
│   ├── models/           # Neural network modules
│   ├── training/         # Training scripts
│   └── utils/            # Utilities
├── docs/                 # Documentation
├── frontend/             # Web dashboard assets
├── tests/                # Test suite
├── docker/               # Docker files
└── config/               # Configuration templates
```

### Documentation Highlights

#### User Guides
- Installation guide
- Training workflow guide
- Evaluation workflow guide
- Inference API usage
- Web dashboard guide
- Docker deployment guide

#### Technical Documentation
- Architecture FAQ
- Hybrid architecture explanation
- Clinical data fusion details
- Grad-CAM explainability flow
- SHAP analysis guide

#### Research Documentation
- Problem statement for cardiovascular screening
- Retinal fundus imaging motivation
- Ablation study methodology
- Reproducibility checklist
- Experiment tracking notes

#### Ethics and Safety
- Research prototype disclaimer
- Medical AI ethics
- Dataset privacy and ethics notes
- Security and upload safety
- Fairness considerations
- Dataset bias discussion

#### Presentation Materials
- Screenshots placeholder guide
- Demo video script
- LinkedIn launch post draft
- GitHub presentation guide
- Resume bullet points
- Interview explanation notes

#### Reference Materials
- Troubleshooting guide
- Common setup errors guide
- Future work roadmap
- Publication readiness checklist
- Research references notes
- Glossary of medical AI terms
- Glossary of deep learning terms

### Known Limitations

- No clinical validation performed
- Not FDA approved or CE marked
- Performance depends on dataset quality
- Single-image analysis only
- May not generalize across all populations
- Requires GPU for efficient training

### Research Status

This release represents a complete research prototype demonstrating:
- Multimodal deep learning architecture
- Medical AI development practices
- MLOps and deployment patterns
- Explainable AI implementation
- Comprehensive documentation standards

**Not intended for clinical use.**

## Future Releases

### Planned for [1.1.0]
- Increased test coverage
- Additional evaluation metrics
- Performance benchmarks
- More example notebooks
- Extended documentation

### Under Consideration [2.0.0]
- Additional model architectures
- Longitudinal analysis support
- External validation framework
- Multi-center study tools
- Enhanced fairness analysis

---

## Release Notes Format

### Categories

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

### Version Numbering

- **MAJOR** (X.0.0): Breaking changes, significant architecture changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

---

*For detailed technical information about specific versions, see git tags and commit history.*
