# Security and Upload Safety Notes

## Overview

This document outlines security considerations for handling image uploads and clinical data in the CardioRetina-AI system.

## Upload Security

### File Upload Validation

| Check | Purpose | Implementation |
|-------|---------|----------------|
| **File type** | Prevent malicious uploads | Whitelist: jpg, jpeg, png, bmp, tif |
| **File size** | Prevent resource exhaustion | Max 10MB |
| **Magic numbers** | Verify actual file type | Check file headers |
| **Image dimensions** | Prevent processing issues | Verify min/max dimensions |
| **Content scan** | Detect embedded malware | Basic sanitization |

### Validation Implementation

```python
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_upload(file):
    # Check extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type: {ext}")
    
    # Check size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")
    
    # Verify image can be opened
    try:
        img = Image.open(file.file)
        img.verify()
    except Exception as e:
        raise ValueError(f"Invalid image: {e}")
```

## Data Handling Security

### Input Validation

| Field | Validation | Sanitization |
|-------|-----------|--------------|
| **Age** | 0-120 range | Float conversion |
| **BP values** | 50-300 (sys), 30-200 (dia) | Float conversion |
| **Cholesterol** | 50-600 | Float conversion |
| **BMI** | 10-70 | Float conversion |
| **Binary fields** | 0 or 1 only | Integer conversion |

### Example Validation

```python
VALIDATION_RANGES = {
    'age': (0, 120),
    'systolic_bp': (50, 300),
    'diastolic_bp': (30, 200),
    'cholesterol': (50, 600),
    'bmi': (10, 70),
    'smoking': (0, 1),
    'diabetes': (0, 1),
    'physical_activity': (0, 1)
}

def validate_clinical_data(data):
    for field, (min_val, max_val) in VALIDATION_RANGES.items():
        value = data.get(field)
        if value is None:
            raise ValueError(f"Missing field: {field}")
        if not (min_val <= value <= max_val):
            raise ValueError(f"{field} must be between {min_val} and {max_val}")
```

## API Security

### Current Limitations

**Note**: This research prototype has minimal security:
- No authentication required
- No rate limiting
- No HTTPS enforcement
- No audit logging

### Development-Only Security

For development/testing:

```python
# Add basic rate limiting (if needed)
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("10/minute")  # Limit requests per IP
def predict(...):
    ...
```

### Production Considerations

If deploying beyond research (not recommended for clinical use):

1. **Add authentication**
   - API keys or OAuth
   - Role-based access control

2. **Enable HTTPS**
   - TLS 1.2 or higher
   - Valid SSL certificates

3. **Implement rate limiting**
   - Per-user limits
   - Per-IP limits
   - Burst allowances

4. **Add audit logging**
   - Log all predictions
   - Store timestamps and metadata
   - Retain for compliance

5. **Input sanitization**
   - SQL injection prevention (if using database)
   - XSS prevention in output
   - CSRF protection for web forms

## Privacy Considerations

### Data Minimization

**What we collect:**
- Retinal image (temporary, in-memory)
- 8 clinical features (numeric only)
- Processing timestamp

**What we DON'T collect:**
- Patient names or IDs
- Contact information
- Medical record numbers
- Geolocation data
- Device identifiers

### Data Retention

| Data Type | Retention | Purpose |
|-----------|-----------|---------|
| Uploaded images | Session only | Immediate processing |
- Prediction results | Not stored | Stateless design |
| Grad-CAM outputs | Session only | Immediate display |
| Logs | No logging | Minimal data collection |

### Temporary File Handling

```python
import tempfile
import os

# Use temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    temp_path = os.path.join(tmpdir, "upload.jpg")
    
    # Save uploaded file
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    
    # Process...
    
# Automatic cleanup when context exits
```

## Threat Model

### Potential Threats

| Threat | Risk | Mitigation |
|--------|------|------------|
| **Malicious uploads** | Medium | File validation, type checking |
| **DoS via large files** | Low | Size limits, timeouts |
| **Data exfiltration** | Low | Stateless design, no data storage |
| **Model extraction** | Low | Not a production-grade API |
| **Prompt injection** | N/A | Not applicable (not LLM-based) |

### Risk Assessment

Given this is a **research prototype**:
- **Acceptable risk** for local development
- **Not suitable** for production without hardening
- **Not appropriate** for processing real patient data

## Best Practices for Users

### Running Locally

```bash
# Run on localhost only (not exposed to network)
uvicorn cardioretina.api.app:app --host 127.0.0.1 --port 8000

# Use firewall to block external access
sudo ufw deny 8000  # Block external access to port 8000
```

### Testing with Synthetic Data

```python
# Use synthetic images for testing
from PIL import Image
import numpy as np

# Create dummy image
dummy = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
img = Image.fromarray(dummy)
img.save("test_image.jpg")
```

### Docker Security

```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Read-only filesystem
--read-only --tmpfs /tmp

# Drop capabilities
--cap-drop=ALL
```

## Incident Response

### If Security Issue Discovered

1. **Document the issue**
   - What was found
   - Potential impact
   - Steps to reproduce

2. **Assess severity**
   - Critical: Immediate fix needed
   - High: Fix within 24 hours
   - Medium: Fix within week
   - Low: Address in next update

3. **Fix and test**
   - Implement fix
   - Verify fix works
   - Test for regressions

4. **Document resolution**
   - What was fixed
   - Version containing fix
   - Any breaking changes

## Security Checklist

### Before Running API

- [ ] Running on localhost only
- [ ] No sensitive data in test images
- [ ] Environment properly isolated
- [ ] No real patient data being processed

### For Development

- [ ] File upload validation enabled
- [ ] Input sanitization in place
- [ ] Size limits configured
- [ ] Error messages don't leak information

### Documentation

- [ ] Security limitations documented
- [ ] No-production-use disclaimer clear
- [ ] Privacy practices explained

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

---

*Security is a continuous process. This research prototype prioritizes simplicity over security hardening - use appropriate precautions.*
