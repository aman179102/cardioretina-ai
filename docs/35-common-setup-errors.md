# Common Setup Errors Guide

## Overview

A quick reference for the most common setup errors and their immediate solutions.

## Error 1: `ModuleNotFoundError: No module named 'cardioretina'`

### Symptom
```python
>>> import cardioretina
ModuleNotFoundError: No module named 'cardioretina'
```

### Quick Fix
```bash
# Make sure you're in the project root
cd /path/to/cardioretina-ai

# Install in editable mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

### Root Cause
Package not installed or virtual environment not activated.

---

## Error 2: `RuntimeError: CUDA error: out of memory`

### Symptom
```
RuntimeError: CUDA out of memory. Tried to allocate 256.00 MiB
```

### Quick Fix
```bash
# Option 1: Reduce batch size
python -m cardioretina.training.train --batch-size 16

# Option 2: Use CPU
export CUDA_VISIBLE_DEVICES=""
python -m cardioretina.training.train

# Option 3: Clear cache (in Python)
import torch
torch.cuda.empty_cache()
```

### Prevention
Monitor GPU memory: `watch -n 1 nvidia-smi`

---

## Error 3: `FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'`

### Symptom
```
FileNotFoundError: data.csv not found
```

### Quick Fix
```bash
# Check if file exists
ls -la data.csv

# Use absolute path
python -m cardioretina.training.train --data-csv /full/path/to/data.csv

# Or check current directory
pwd
```

### Root Cause
Wrong working directory or incorrect file path.

---

## Error 4: `ImportError: cannot import name 'RetinalDataset'`

### Symptom
```python
from cardioretina.data.dataset import RetinalDataset
ImportError: cannot import name 'RetinalDataset'
```

### Quick Fix
```bash
# Reinstall package
pip uninstall cardioretina-ai -y
pip install -e ".[dev]"

# Check if files exist
ls cardioretina/data/
```

### Root Cause
Corrupted installation or missing files.

---

## Error 5: `Permission denied` when saving checkpoints

### Symptom
```
PermissionError: [Errno 13] Permission denied: 'checkpoints/best_model.pt'
```

### Quick Fix
```bash
# Create directory with correct permissions
mkdir -p checkpoints
chmod 755 checkpoints

# Or use different directory
python -m cardioretina.training.train --checkpoint-dir /tmp/checkpoints
```

### Root Cause
Directory doesn't exist or incorrect permissions.

---

## Error 6: `Connection refused` when calling API

### Symptom
```
curl: (7) Failed to connect to localhost port 8000
```

### Quick Fix
```bash
# Check if server is running
ps aux | grep uvicorn

# Start server
uvicorn cardioretina.api.app:app --host 0.0.0.0 --port 8000

# Try different port
uvicorn cardioretina.api.app:app --port 8001
```

### Root Cause
Server not started or port conflict.

---

## Error 7: `ValueError: Invalid image format`

### Symptom
```
ValueError: Invalid image format: .webp
```

### Quick Fix
```bash
# Convert image to supported format
convert image.webp image.jpg

# Or use Python
from PIL import Image
img = Image.open('image.webp')
img.save('image.jpg')
```

### Supported Formats
JPEG, PNG, BMP, TIFF only.

---

## Error 8: `KeyError: 'systolic_bp'` in clinical data

### Symptom
```
KeyError: 'systolic_bp' not found in data
```

### Quick Fix
```bash
# Check CSV columns
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(df.columns.tolist())"

# Fix column names in CSV
# Should be: image_path,label,age,systolic_bp,diastolic_bp,cholesterol,bmi,smoking,diabetes,physical_activity
```

### Root Cause
Missing or misspelled column names.

---

## Error 9: `AssertionError: Torch not compiled with CUDA enabled`

### Symptom
```
AssertionError: Torch not compiled with CUDA enabled
```

### Quick Fix
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 --force-reinstall

# For CPU only (no GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Verify
python -c "import torch; print(torch.cuda.is_available())"
```

### Root Cause
PyTorch CPU version installed but CUDA requested.

---

## Error 10: Docker `executor failed running`

### Symptom
```
executor failed running [/bin/sh -c pip install ...]
```

### Quick Fix
```bash
# Clear Docker cache
docker system prune -a

# Build without cache
docker build --no-cache -f docker/Dockerfile -t cardioretina-ai .

# Check disk space
df -h
```

### Root Cause
Corrupted Docker cache or insufficient disk space.

---

## Error 11: `RuntimeError: Expected all tensors to be on the same device`

### Symptom
```
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu
```

### Quick Fix
```python
# In code, ensure model and data on same device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
images = images.to(device)
clinical = clinical.to(device)
```

### Root Cause
Model on GPU but data on CPU, or vice versa.

---

## Error 12: `OSError: [Errno 24] Too many open files`

### Symptom
```
OSError: [Errno 24] Too many open files
```

### Quick Fix
```bash
# Increase file descriptor limit
ulimit -n 4096

# Or reduce number of workers
python -m cardioretina.training.train --num-workers 2
```

### Root Cause
Too many file descriptors open (common with high num_workers).

---

## Quick Diagnostic Commands

### Check Python Environment
```bash
# Python version
python --version  # Should be 3.10+

# Installed packages
pip list | grep -E "(torch|fastapi|cardioretina)"

# Virtual environment
which python  # Should point to venv
```

### Check GPU Status
```bash
# NVIDIA GPU
nvidia-smi

# PyTorch CUDA
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

### Check Data
```bash
# CSV validation
python -m cardioretina.data.validate data.csv --image-dir images/

# Image count
ls images/ | wc -l

# CSV row count
wc -l data.csv
```

### Check Installation
```bash
# Import test
python -c "import cardioretina; print('OK')"

# Model test
python -c "from cardioretina.models.hybrid_model import HybridModel; print('OK')"

# Run quick test
pytest tests/test_imports.py -v
```

## Prevention Tips

### Always Do

1. **Use virtual environments**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install in editable mode**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Validate data before training**
   ```bash
   python -m cardioretina.data.validate data.csv --image-dir images/
   ```

4. **Check GPU availability before CUDA training**
   ```python
   import torch
   assert torch.cuda.is_available(), "CUDA not available"
   ```

5. **Use absolute paths in scripts**
   ```bash
   python -m cardioretina.training.train \
       --data-csv $(pwd)/data.csv \
       --image-dir $(pwd)/images/
   ```

---

*Most setup errors stem from environment configuration. Following the installation guide carefully prevents most issues.*
