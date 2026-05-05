# Web Dashboard Usage Guide

## Overview

The CardioRetina-AI web dashboard provides an interactive browser interface for making predictions and visualizing results.

## Accessing the Dashboard

### Start the Server

```bash
uvicorn cardioretina.api.app:app --host 0.0.0.0 --port 8000
```

### Open Dashboard

Navigate to: `http://localhost:8000/`

## Dashboard Interface

### Layout Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CardioRetina-AI Dashboard                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────────────────────┐   │
│  │   Image Upload  │  │     Prediction Results        │   │
│  │                 │  │                                 │   │
│  │  [Drag & Drop]  │  │  ┌──────────────────────────┐   │   │
│  │  [Click to      │  │  │    Risk Gauge           │   │   │
│  │   Browse]       │  │  │    [0-100%]            │   │   │
│  │                 │  │  └──────────────────────────┘   │   │
│  │  Preview:       │  │                                 │   │
│  │  [Image]        │  │  Risk Level: [Low/Med/High]     │   │
│  │                 │  │  Probability: 0.XX              │   │
│  └─────────────────┘  │                                 │   │
│                      │  Clinical Factors Analysis      │   │
│  ┌─────────────────┐  │  ┌──────────────────────────┐   │   │
│  │ Clinical Data   │  │  │  • Age: +XX%            │   │   │
│  │                 │  │  │  • BP: +XX%             │   │   │
│  │  [Form Fields]  │  │  │  • Cholesterol: +XX%    │   │   │
│  │                 │  │  │  • BMI: +XX%            │   │   │
│  │  Age: [___]     │  │  │  • Smoking: +XX%        │   │   │
│  │  Systolic BP:   │  │  │  • ...                  │   │   │
│  │  [___]          │  │  └──────────────────────────┘   │   │
│  │  ...            │  │                                 │   │
│  │                 │  │  Grad-CAM Visualization       │   │
│  │  [Submit]       │  │  [Heatmap Overlay]            │   │
│  │                 │  │                                 │   │
│  └─────────────────┘  └─────────────────────────────────┘   │
│                                                             │
│  ⚠️ Disclaimer: Research prototype only. Not for clinical   │
│     use. Always consult healthcare professionals.           │
└─────────────────────────────────────────────────────────────┘
```

## Step-by-Step Usage

### Step 1: Upload Retinal Image

**Drag and Drop Method**:
1. Drag a retinal fundus image from your file explorer
2. Drop onto the "Image Upload" area
3. Preview appears automatically

**Click to Browse**:
1. Click the upload area
2. Select image from file dialog
3. Supported formats: JPEG, PNG, BMP, TIFF

**Image Requirements**:
- Color fundus photograph (not OCT, not fluorescein)
- Clear, in-focus image
- Standard 45° field of view preferred
- Minimum 512×512 resolution

### Step 2: Enter Clinical Data

Fill in all 8 clinical fields:

| Field | Input Type | Valid Range | Example |
|-------|-----------|-------------|---------|
| **Age** | Number | 0-120 | 55 |
| **Systolic BP** | Number | 50-300 | 140 |
| **Diastolic BP** | Number | 30-200 | 90 |
| **Cholesterol** | Number | 50-600 | 240 |
| **BMI** | Number | 10-70 | 28.5 |
| **Smoking** | Dropdown | Yes/No | No |
| **Diabetes** | Dropdown | Yes/No | No |
| **Physical Activity** | Dropdown | Active/Sedentary | Active |

**Tips**:
- Use most recent clinical values
- Blood pressure in mmHg
- Cholesterol in mg/dL
- BMI = weight(kg) / height(m)²

### Step 3: Submit for Analysis

1. Click the **"Analyze Risk"** button
2. Wait for processing (typically 1-3 seconds)
3. Results display automatically

### Step 4: Review Results

#### Risk Gauge
- **Green (0-40%)**: Low risk
- **Yellow (40-70%)**: Moderate risk
- **Red (70-100%)**: High risk

#### Clinical Factors
Shows contribution of each factor:
- **Positive (+)**: Increases risk
- **Negative (-)**: Decreases risk
- **Magnitude**: Size of contribution

#### Grad-CAM Visualization
- Original image with heatmap overlay
- **Red/Yellow areas**: Regions contributing to prediction
- Helps understand which retinal areas influenced the result

## Example Workflow

### Scenario 1: Low Risk Patient

```
Patient Profile:
- Age: 35
- BP: 120/80
- Cholesterol: 180
- BMI: 22
- Non-smoker, no diabetes, active

Expected Result:
Risk: Low (15-25%)
Gauge: Green zone
Key factors: Young age, normal vitals
```

### Scenario 2: High Risk Patient

```
Patient Profile:
- Age: 68
- BP: 160/100
- Cholesterol: 280
- BMI: 32
- Smoker, diabetic, sedentary

Expected Result:
Risk: High (75-85%)
Gauge: Red zone
Key factors: Age, BP, smoking, diabetes
Grad-CAM: Likely highlights vessel abnormalities
```

## Advanced Features

### Result Download

Export prediction results:
```
[Download Report] button → PDF/JSON report
```

### History (Future Feature)

Planned enhancement:
- Save predictions locally
- Compare over time
- Track changes

### Comparison Mode (Future Feature)

Planned enhancement:
- Compare two patients side-by-side
- See relative risk factors

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Image not loading | Wrong format | Use JPEG, PNG, BMP, or TIFF |
| Form won't submit | Missing fields | Fill all 8 clinical fields |
| Slow response | Server load | Wait or check server status |
| No Grad-CAM | API error | Check server logs |
| Incorrect values | Unit confusion | Verify BP in mmHg, cholesterol in mg/dL |

## Browser Compatibility

Supported browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Required features:
- JavaScript enabled
- Modern CSS support
- File API support

## Mobile Usage

The dashboard is responsive and works on mobile devices:
- Touch-friendly interface
- Responsive layout
- Image upload via camera (if supported)

Note: For best experience, use desktop/tablet for detailed analysis.

## Privacy Notice

Data handling:
- Images processed on your local server
- No data sent to external services
- No persistent storage of predictions
- Refresh page clears current session

## Next Steps

After using dashboard:
1. Review Grad-CAM explanations
2. Understand clinical factor contributions
3. Refer to documentation for API access
4. See [Troubleshooting Guide](34-troubleshooting-guide.md) if issues

---

*The web dashboard provides the easiest way to interact with the model through a visual interface.*
