# Local Development Guide

## Overview

This guide explains how to set up the CardioRetina-AI development environment on your local machine.

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Linux, macOS, Windows (WSL) | Linux (Ubuntu 20.04+) |
| **Python** | 3.10 | 3.10-3.11 |
| **RAM** | 8GB | 16GB+ |
| **Storage** | 10GB | 50GB+ (for datasets) |
| **GPU** | Optional | NVIDIA GPU with 8GB+ VRAM |

### Required Software

- Python 3.10 or higher
- pip (Python package manager)
- Git
- (Optional) CUDA 11.8+ for GPU support

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/aarohidev91/cardioretina-ai.git
cd cardioretina-ai
```

### Step 2: Create Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows
```

**Using conda:**
```bash
conda create -n cardioretina python=3.10
conda activate cardioretina
```

### Step 3: Install Dependencies

**Development Install (includes all dev tools):**
```bash
pip install -e ".[dev]"
```

**Production Install (minimal dependencies):**
```bash
pip install -e .
```

**Install Specific Extras:**
```bash
# For training only
pip install -e ".[train]"

# For API only
pip install -e ".[api]"
```

### Step 4: Verify Installation

```bash
# Check Python packages
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import cardioretina; print('CardioRetina installed')"

# Run tests
pytest tests/ -v --tb=short

# Check linting
ruff check cardioretina/ tests/
```

### Step 5: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env  # or your preferred editor
```

Example `.env`:
```env
MODEL_CHECKPOINT=checkpoints/best_model.pt
LOG_LEVEL=info
DEVICE=auto
```

## Development Workflow

### Project Structure

```
cardioretina-ai/
├── cardioretina/           # Main package
│   ├── api/               # FastAPI application
│   ├── data/              # Data pipeline
│   ├── evaluation/        # Evaluation tools
│   ├── models/          # Neural network modules
│   ├── training/        # Training scripts
│   └── utils/           # Utilities
├── tests/                 # Test suite
├── docs/                  # Documentation
├── frontend/              # Web dashboard
├── config/                # Configuration files
├── docker/                # Docker files
└── scripts/               # Utility scripts
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=cardioretina

# Run specific test file
pytest tests/test_models.py -v

# Run specific test
pytest tests/test_models.py::test_hybrid_model -v
```

### Code Quality

```bash
# Linting
ruff check cardioretina/ tests/

# Auto-fix linting issues
ruff check --fix cardioretina/ tests/

# Type checking
mypy cardioretina/
```

### Making Changes

1. **Create a branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes** to relevant files

3. **Test your changes:**
   ```bash
   pytest tests/ -v
   ```

4. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

## GPU Setup (Optional)

### NVIDIA GPU

1. **Install CUDA:**
   Follow [NVIDIA CUDA installation guide](https://developer.nvidia.com/cuda-downloads)

2. **Install PyTorch with CUDA:**
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Verify GPU:**
   ```bash
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
   python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0)}')"
   ```

### MPS (Apple Silicon)

For Macs with Apple Silicon:

```bash
# PyTorch automatically uses MPS
python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
```

## IDE Setup

### VS Code

Recommended extensions:
- Python (Microsoft)
- Pylance
- Ruff
- Python Docstring Generator
- Markdown Preview Enhanced

Settings:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "ruff.importStrategy": "fromEnvironment"
}
```

### PyCharm

1. Open project in PyCharm
2. Set Python interpreter to virtual environment
3. Enable pytest as test runner
4. Configure run configurations for training/API

## Common Development Tasks

### Training a Model

```bash
python -m cardioretina.training.train \
    --data-csv data/train.csv \
    --image-dir data/images/ \
    --val-csv data/val.csv
```

### Running API Locally

```bash
uvicorn cardioretina.api.app:app --reload
```

### Evaluating a Model

```bash
python -m cardioretina.evaluation.evaluate \
    --checkpoint checkpoints/best_model.pt \
    --test-csv data/test.csv \
    --image-dir data/images/
```

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### VS Code Debugging

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Train",
            "type": "python",
            "request": "launch",
            "module": "cardioretina.training.train",
            "args": ["--data-csv", "data/train.csv", "--image-dir", "data/images/"]
        }
    ]
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure virtual environment is activated |
| `CUDA out of memory` | Reduce batch size, close other GPU programs |
| `Import errors` | Reinstall: `pip install -e ".[dev]"` |
| `Permission denied` | Use `sudo` or check file permissions |
| `Slow training` | Check GPU usage, enable mixed precision |

## Updating Dependencies

```bash
# Update all packages
pip install -e ".[dev]" --upgrade

# Update specific package
pip install torch --upgrade

# Regenerate lock file (if using)
pip freeze > requirements.lock.txt
```

## Useful Aliases

Add to `.bashrc` or `.zshrc`:

```bash
alias crtrain='python -m cardioretina.training.train'
alias creval='python -m cardioretina.evaluation.evaluate'
alias crapi='uvicorn cardioretina.api.app:app --reload'
alias crtest='pytest tests/ -v'
alias crlint='ruff check cardioretina/ tests/'
```

---

*A properly configured development environment ensures productive and reproducible work.*
