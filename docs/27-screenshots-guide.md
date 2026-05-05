# Screenshots Placeholder Guide

## Overview

This guide documents where screenshots should be placed and what they should demonstrate.

## Required Screenshots

### 1. Dashboard Overview

**Location**: `docs/screenshots/dashboard_overview.png`

**Contents**:
- Full web dashboard interface
- Image upload area visible
- Clinical data form visible
- Results panel visible

**Purpose**: Give users a preview of the interface

### 2. Upload Process

**Location**: `docs/screenshots/upload_process.png`

**Contents**:
- Drag-and-drop in progress
- Image preview displayed
- Upload area highlighted

**Purpose**: Show how to upload images

### 3. Clinical Data Entry

**Location**: `docs/screenshots/clinical_form.png`

**Contents**:
- All 8 fields filled in
- Form validation visible (if applicable)
- Submit button highlighted

**Purpose**: Demonstrate data entry workflow

### 4. Prediction Results

**Location**: `docs/screenshots/prediction_results.png`

**Contents**:
- Risk gauge displayed
- Probability value shown
- Risk level indicated (Low/Moderate/High)
- Clinical factors breakdown visible

**Purpose**: Show what users see after analysis

### 5. Grad-CAM Visualization

**Location**: `docs/screenshots/gradcam_result.png`

**Contents**:
- Original retinal image
- Grad-CAM heatmap overlay
- Highlighted regions visible
- Color legend if applicable

**Purpose**: Demonstrate explainability feature

### 6. API Documentation

**Location**: `docs/screenshots/api_docs.png`

**Contents**:
- Swagger UI at `/docs`
- Endpoint list visible
- Example request/response shown

**Purpose**: Show API documentation interface

### 7. Training Progress

**Location**: `docs/screenshots/training_progress.png`

**Contents**:
- Console output during training
- Epoch progress visible
- Loss/metrics displayed
- ETA or timing information

**Purpose**: Show what training looks like

### 8. Evaluation Results

**Location**: `docs/screenshots/evaluation_results.png`

**Contents**:
- Confusion matrix plot
- ROC curve
- Metrics table or output
- Results summary

**Purpose**: Show evaluation output

## Screenshot Specifications

### Technical Requirements

| Property | Specification |
|----------|---------------|
| **Format** | PNG (preferred) or JPEG |
| **Resolution** | 1920×1080 minimum |
| **DPI** | 72 or 96 (web), 300 (print) |
| **Color space** | sRGB |
| **File size** | Under 500KB each |

### Styling Guidelines

1. **Clean desktop**: No personal files visible
2. **Consistent browser**: Use same browser for all screenshots
3. **Appropriate zoom**: 100% zoom level
4. **No notifications**: Hide system notifications
5. **Professional appearance**: Use realistic data (synthetic)

## Generating Screenshots

### Dashboard Screenshots

```bash
# Start the server
uvicorn cardioretina.api.app:app --host 127.0.0.1 --port 8000

# Open browser to http://localhost:8000/
# Use synthetic data for all screenshots
```

### Using Synthetic Data

```python
# Generate test image
from PIL import Image
import numpy as np

# Create synthetic fundus-like image
def generate_synthetic_fundus():
    # Dark background
    img = np.zeros((224, 224, 3), dtype=np.uint8)
    
    # Add circular fundus shape
    center = (112, 112)
    radius = 100
    y, x = np.ogrid[:224, :224]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2
    img[mask] = [80, 50, 40]  # Reddish-brown fundus color
    
    # Add vessel-like lines (simplified)
    for i in range(224):
        if abs(i - 112) < 2:
            img[i, :] = [150, 30, 30]  # Dark red vessels
        if abs(i - 112) < 80 and abs(i - 112) > 75:
            img[:, i] = [150, 30, 30]
    
    return Image.fromarray(img)

# Save for testing
img = generate_synthetic_fundus()
img.save("docs/screenshots/test_fundus.jpg")
```

### Using Demo Mode

For screenshots, use these representative clinical values:

| Screenshot | Age | BP | Cholesterol | BMI | Smoking | Diabetes | Activity |
|------------|-----|-----|-------------|-----|---------|----------|----------|
| Low Risk | 35 | 120/80 | 180 | 22 | No | No | Active |
| Moderate Risk | 55 | 140/90 | 220 | 27 | No | No | Sedentary |
| High Risk | 68 | 160/100 | 280 | 32 | Yes | Yes | Sedentary |

## Screenshot Checklist

### Before Capturing

- [ ] Clean browser cache/cookies
- [ ] Close unnecessary tabs
- [ ] Use consistent window size
- [ ] Set appropriate zoom level
- [ ] Hide bookmarks bar
- [ ] Disable browser extensions that modify page

### During Capture

- [ ] Use screenshot tool (not phone camera)
- [ ] Capture full window or relevant area
- [ ] Ensure text is readable
- [ ] Check for sensitive information
- [ ] Verify content is appropriate

### After Capture

- [ ] Check file size (compress if needed)
- [ ] Verify image quality
- [ ] Crop if necessary
- [ ] Add annotations if helpful
- [ ] Save with descriptive filename

## Using Screenshots

### In Documentation

```markdown
![Dashboard Overview](screenshots/dashboard_overview.png)
*Figure 1: CardioRetina-AI web dashboard interface*
```

### In README

```markdown
## Demo

![Dashboard](docs/screenshots/dashboard_overview.png)
```

### In Presentations

- Use high-resolution versions
- Add annotations to highlight features
- Include context in slide notes

## Screenshots Directory Structure

```
docs/
├── screenshots/
│   ├── README.md                 # This guide
│   ├── dashboard_overview.png
│   ├── upload_process.png
│   ├── clinical_form.png
│   ├── prediction_results.png
│   ├── gradcam_result.png
│   ├── api_docs.png
│   ├── training_progress.png
│   └── evaluation_results.png
└── ...
```

## Animated GIFs (Optional)

For demonstrating workflows:

```bash
# Tools for creating GIFs
# macOS: LICEcap, GIPHY Capture
# Windows: ScreenToGif
# Linux: Peek, silentcast

# Recommended settings:
# - 15-30 FPS
# - 800x600 resolution
# - 5-10 seconds duration
# - Loop once or forever
```

## Maintenance

### When to Update Screenshots

Update when:
- UI design changes significantly
- New features are added
- Old screenshots become outdated
- Quality improvements are made

### Version Control

```bash
# Add screenshots to git
git add docs/screenshots/*.png
git commit -m "docs: update screenshots for v1.1.0"

# Use LFS for large images (optional)
git lfs track "docs/screenshots/*.png"
```

## Privacy Note

**Important**: Use only synthetic or anonymized data in screenshots:
- No real patient information
- No actual retinal images of real people
- No identifying details in the background
- Use placeholder data for all fields

---

*Screenshots help users understand the interface and capabilities before installing or using the software.*
