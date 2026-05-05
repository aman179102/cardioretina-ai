# Inference API Usage Examples

## API Overview

The CardioRetina-AI inference API provides RESTful endpoints for making predictions using trained models.

## Starting the API Server

### Basic Startup

```bash
uvicorn cardioretina.api.app:app --host 0.0.0.0 --port 8000
```

### With Model Checkpoint

```bash
MODEL_CHECKPOINT=checkpoints/best_model.pt uvicorn cardioretina.api.app:app
```

### Production Mode

```bash
uvicorn cardioretina.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Purpose**: Verify API is running and model is loaded

**Example Request**:
```bash
curl http://localhost:8000/health
```

**Example Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "device": "cuda",
  "timestamp": "2024-01-15T14:30:22Z"
}
```

### 2. Model Information

**Endpoint**: `GET /model-info`

**Purpose**: Get model architecture and configuration details

**Example Request**:
```bash
curl http://localhost:8000/model-info
```

**Example Response**:
```json
{
  "model_name": "CardioRetina-AI",
  "version": "1.0.0",
  "architecture": "hybrid_cnn_vit_clinical",
  "backbone": "efficientnet-b3",
  "vit_model": "vit_base_patch16_224",
  "clinical_features": 8,
  "input_size": [224, 224],
  "output": "binary_classification",
  "parameters": 97100000
}
```

### 3. Make Prediction

**Endpoint**: `POST /predict`

**Purpose**: Get cardiovascular risk prediction for a patient

#### Request Format

Content-Type: `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | Retinal fundus image |
| `age` | Float | Yes | Age in years |
| `systolic_bp` | Float | Yes | Systolic BP in mmHg |
| `diastolic_bp` | Float | Yes | Diastolic BP in mmHg |
| `cholesterol` | Float | Yes | Total cholesterol in mg/dL |
| `bmi` | Float | Yes | Body Mass Index |
| `smoking` | Integer | Yes | 0=No, 1=Yes |
| `diabetes` | Integer | Yes | 0=No, 1=Yes |
| `physical_activity` | Integer | Yes | 0=Sedentary, 1=Active |
| `generate_gradcam` | Boolean | No | Generate explanation heatmap |

#### Example cURL Request

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@retinal_image.jpg" \
  -F "age=55" \
  -F "systolic_bp=140" \
  -F "diastolic_bp=90" \
  -F "cholesterol=240" \
  -F "bmi=28.5" \
  -F "smoking=0" \
  -F "diabetes=0" \
  -F "physical_activity=1" \
  -F "generate_gradcam=true"
```

#### Example Response

```json
{
  "prediction_id": "pred_abc123def456",
  "risk_probability": 0.7634,
  "risk_level": "High",
  "confidence": 0.89,
  "clinical_factors": {
    "age": {"value": 55, "contribution": "moderate_increase"},
    "systolic_bp": {"value": 140, "contribution": "significant_increase"},
    "cholesterol": {"value": 240, "contribution": "moderate_increase"},
    "bmi": {"value": 28.5, "contribution": "slight_increase"}
  },
  "gradcam_url": "/gradcam/pred_abc123def456",
  "processing_time_ms": 125,
  "model_version": "1.0.0",
  "disclaimer": "This is a research prototype. Not for clinical use."
}
```

### 4. Get Grad-CAM

**Endpoint**: `GET /gradcam/{prediction_id}`

**Purpose**: Retrieve Grad-CAM explanation for a prediction

**Example Request**:
```bash
curl http://localhost:8000/gradcam/pred_abc123def456
```

**Response**: PNG image with Grad-CAM overlay

### 5. Get Metrics

**Endpoint**: `GET /metrics`

**Purpose**: Retrieve evaluation metrics if available

**Example Request**:
```bash
curl http://localhost:8000/metrics
```

**Example Response**:
```json
{
  "metrics_available": true,
  "accuracy": 0.8234,
  "precision": 0.8123,
  "recall": 0.8456,
  "auc_roc": 0.8912,
  "f1_score": 0.8287,
  "last_evaluated": "2024-01-10T09:00:00Z"
}
```

### 6. Web Dashboard

**Endpoint**: `GET /`

**Purpose**: Access the web interface for interactive predictions

Simply open `http://localhost:8000/` in a browser.

## Python Client Example

```python
import requests

# API endpoint
url = "http://localhost:8000/predict"

# Prepare data
files = {
    'file': open('retinal_image.jpg', 'rb')
}
data = {
    'age': 55,
    'systolic_bp': 140,
    'diastolic_bp': 90,
    'cholesterol': 240,
    'bmi': 28.5,
    'smoking': 0,
    'diabetes': 0,
    'physical_activity': 1,
    'generate_gradcam': 'true'
}

# Make request
response = requests.post(url, files=files, data=data)
result = response.json()

# Parse result
risk_level = result['risk_level']
probability = result['risk_probability']
print(f"Risk Level: {risk_level} ({probability:.2%})")

# Download Grad-CAM
if result.get('gradcam_url'):
    gradcam_response = requests.get(f"http://localhost:8000{result['gradcam_url']}")
    with open('gradcam.png', 'wb') as f:
        f.write(gradcam_response.content)
```

## JavaScript/Frontend Example

```javascript
async function predictRisk(imageFile, clinicalData) {
    const formData = new FormData();
    formData.append('file', imageFile);
    formData.append('age', clinicalData.age);
    formData.append('systolic_bp', clinicalData.systolic_bp);
    formData.append('diastolic_bp', clinicalData.diastolic_bp);
    formData.append('cholesterol', clinicalData.cholesterol);
    formData.append('bmi', clinicalData.bmi);
    formData.append('smoking', clinicalData.smoking);
    formData.append('diabetes', clinicalData.diabetes);
    formData.append('physical_activity', clinicalData.physical_activity);
    formData.append('generate_gradcam', 'true');

    const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    return result;
}

// Usage
const imageInput = document.getElementById('imageInput');
const file = imageInput.files[0];
const clinicalData = {
    age: 55,
    systolic_bp: 140,
    // ... other fields
};

predictRisk(file, clinicalData)
    .then(result => {
        console.log('Risk:', result.risk_level);
        console.log('Probability:', result.risk_probability);
    });
```

## Error Handling

### Common Error Responses

| Status | Code | Description | Solution |
|--------|------|-------------|----------|
| 400 | invalid_image | Image format not supported | Use JPEG, PNG, BMP, or TIFF |
| 400 | missing_field | Required field missing | Check all 8 clinical fields |
| 400 | invalid_value | Value out of expected range | Check data ranges |
| 422 | model_error | Model inference failed | Check model checkpoint |
| 500 | internal_error | Server error | Check logs |

### Error Response Format

```json
{
  "detail": {
    "error_code": "missing_field",
    "message": "Required field 'systolic_bp' is missing",
    "field": "systolic_bp"
  }
}
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Security Notes

- **No authentication**: Development/testing only
- **No rate limiting**: Single-user scenario
- **File upload limits**: 10MB max image size
- **Research disclaimer**: Always included in responses

---

*The API provides programmatic access to model predictions for integration with other applications.*
