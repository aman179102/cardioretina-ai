# Troubleshooting Guide

## Overview

Common issues and their solutions when working with CardioRetina-AI.

## Installation Issues

### Issue: `pip install` fails with dependency conflicts

**Symptoms**:
```
ERROR: Cannot install package because these packages have conflicting dependencies.
```

**Solutions**:

1. **Create fresh virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

2. **Upgrade pip**:
```bash
pip install --upgrade pip
```

3. **Install with no cache**:
```bash
pip install -e ".[dev]" --no-cache-dir
```

4. **Install dependencies individually**:
```bash
pip install torch torchvision
pip install fastapi uvicorn
pip install -e .
```

### Issue: CUDA not available after installation

**Symptoms**:
```python
import torch
print(torch.cuda.is_available())  # False
```

**Solutions**:

1. **Check CUDA version**:
```bash
nvidia-smi
```

2. **Install PyTorch with matching CUDA**:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# CPU only
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

3. **Verify installation**:
```python
import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())
```

## Training Issues

### Issue: Out of memory during training

**Symptoms**:
```
RuntimeError: CUDA out of memory. Tried to allocate X MB
```

**Solutions**:

1. **Reduce batch size**:
```bash
python -m cardioretina.training.train --batch-size 16  # Instead of 32
```

2. **Enable gradient accumulation** (if implemented):
```bash
python -m cardioretina.training.train --batch-size 8 --accumulation-steps 4
```

3. **Use mixed precision training**:
```bash
python -m cardioretina.training.train --mixed-precision
```

4. **Clear CUDA cache** (in code):
```python
import torch
torch.cuda.empty_cache()
```

5. **Monitor GPU memory**:
```bash
watch -n 1 nvidia-smi
```

### Issue: Training loss not decreasing

**Symptoms**:
- Loss stays constant or increases
- Validation metrics don't improve

**Solutions**:

1. **Check learning rate**:
```bash
# Try lower learning rate
python -m cardioretina.training.train --lr 0.0001
```

2. **Verify data loading**:
```python
# Check if data is being loaded correctly
from cardioretina.data.dataset import RetinalDataset
dataset = RetinalDataset(...)
print(len(dataset))
sample = dataset[0]
print(sample['image'].shape, sample['label'])
```

3. **Check label distribution**:
```bash
python -m cardioretina.data.validate data.csv --image-dir images/
```

4. **Enable debug logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Issue: NaN loss during training

**Symptoms**:
```
Epoch 5: loss = nan
```

**Solutions**:

1. **Lower learning rate**:
```bash
python -m cardioretina.training.train --lr 0.00001
```

2. **Check for invalid data**:
```bash
python -m cardioretina.data.validate data.csv --image-dir images/
```

3. **Add gradient clipping**:
```python
# In training code
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

4. **Check for inf/nan in data**:
```python
import numpy as np
print(np.isnan(image).any())
print(np.isinf(image).any())
```

## API Issues

### Issue: Cannot connect to API server

**Symptoms**:
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Solutions**:

1. **Verify server is running**:
```bash
ps aux | grep uvicorn
```

2. **Check port availability**:
```bash
lsof -i :8000  # Check if port is in use
```

3. **Try different port**:
```bash
uvicorn cardioretina.api.app:app --port 8001
```

4. **Check firewall settings**:
```bash
sudo ufw status
sudo ufw allow 8000
```

### Issue: Model not loading in API

**Symptoms**:
```
Error: Model checkpoint not found at checkpoints/best_model.pt
```

**Solutions**:

1. **Verify checkpoint exists**:
```bash
ls -la checkpoints/
```

2. **Set correct path**:
```bash
export MODEL_CHECKPOINT=/absolute/path/to/checkpoints/best_model.pt
uvicorn cardioretina.api.app:app
```

3. **Check file permissions**:
```bash
chmod 644 checkpoints/best_model.pt
```

### Issue: File upload fails

**Symptoms**:
```
Error: File too large or invalid format
```

**Solutions**:

1. **Check file size**:
```bash
ls -lh image.jpg  # Should be < 10MB
```

2. **Verify file format**:
```bash
file image.jpg  # Should show JPEG/PNG
```

3. **Use supported format**:
```bash
# Convert if needed
convert image.tiff image.jpg
```

## Data Issues

### Issue: Dataset validation fails

**Symptoms**:
```
ValidationError: Missing required column: systolic_bp
```

**Solutions**:

1. **Check CSV format**:
```bash
head -n 5 data.csv
```

2. **Verify column names**:
```bash
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(df.columns.tolist())"
```

3. **Check for missing values**:
```bash
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(df.isnull().sum())"
```

### Issue: Images not found

**Symptoms**:
```
FileNotFoundError: Image not found at images/patient_001.jpg
```

**Solutions**:

1. **Verify image path**:
```bash
ls images/patient_001.jpg
```

2. **Check relative path**:
```bash
# CSV should have relative paths from image_dir
head -n 5 data.csv | cut -d',' -f1
```

3. **Verify image directory**:
```bash
python -m cardioretina.data.validate data.csv --image-dir ./images/
```

## Docker Issues

### Issue: Docker build fails

**Symptoms**:
```
ERROR: failed to solve: executor failed running
```

**Solutions**:

1. **Check Dockerfile syntax**:
```bash
docker build -f docker/Dockerfile -t cardioretina-ai . 2>&1 | head -50
```

2. **Clear Docker cache**:
```bash
docker build --no-cache -f docker/Dockerfile -t cardioretina-ai .
```

3. **Check available disk space**:
```bash
df -h
```

### Issue: Container exits immediately

**Symptoms**:
```
Container started and exited with code 1
```

**Solutions**:

1. **Check logs**:
```bash
docker logs <container_id>
```

2. **Run interactively**:
```bash
docker run -it cardioretina-ai /bin/bash
```

3. **Check entrypoint**:
```bash
docker run --entrypoint /bin/bash cardioretina-ai
```

## Evaluation Issues

### Issue: Evaluation produces empty results

**Symptoms**:
```
Results file is empty or missing
```

**Solutions**:

1. **Check output directory permissions**:
```bash
ls -la evaluation_results/
```

2. **Verify test data**:
```bash
python -m cardioretina.data.validate test.csv --image-dir images/
```

3. **Check model checkpoint**:
```bash
python -c "import torch; model = torch.load('checkpoints/best_model.pt'); print(model.keys())"
```

## Performance Issues

### Issue: Slow inference

**Symptoms**:
- API responses take > 5 seconds
- Batch processing is slow

**Solutions**:

1. **Use GPU**:
```bash
export DEVICE=cuda
uvicorn cardioretina.api.app:app
```

2. **Increase batch size**:
```bash
python -m cardioretina.evaluation.evaluate --batch-size 64
```

3. **Use ONNX optimization**:
```bash
python -m cardioretina.export.onnx_export --checkpoint checkpoints/best_model.pt
```

4. **Profile code**:
```python
import cProfile
cProfile.run('make_prediction()', 'profile.stats')
```

## Getting Help

### Before Asking for Help

1. **Check logs**:
```bash
# Training logs
tail -n 100 outputs/training_history.json

# API logs
uvicorn cardioretina.api.app:app --log-level debug
```

2. **Verify environment**:
```bash
python --version
pip list | grep torch
nvidia-smi
```

3. **Check documentation**:
- README.md
- docs/ folder
- MODEL_CARD.md

### Reporting Issues

When reporting issues, include:
1. Full error message
2. Command that caused the error
3. Environment info (OS, Python version, GPU)
4. Steps to reproduce

## Quick Fixes Checklist

| Issue | Quick Fix |
|-------|-----------|
| Import errors | `pip install -e ".[dev]"` |
| CUDA OOM | Reduce `--batch-size` |
| API won't start | Check port with `lsof -i :8000` |
| Data not loading | Run validation script |
| NaN loss | Lower learning rate |
| Slow training | Check GPU utilization |
| Docker fails | Clear cache: `docker system prune` |

---

*Most issues have straightforward solutions. Start with the simplest fix and work toward more complex solutions.*
