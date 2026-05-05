# Demo Video Script

## Overview

This script provides a guide for creating a demonstration video of CardioRetina-AI.

## Video Specifications

| Property | Specification |
|----------|---------------|
| **Duration** | 3-5 minutes |
| **Resolution** | 1920×1080 (1080p) |
| **Frame rate** | 30 FPS |
| **Audio** | Voiceover + optional background music |
| **Format** | MP4 (H.264 encoding) |

## Scene Breakdown

### Scene 1: Introduction (30 seconds)

**Visual**:
- Title card: "CardioRetina-AI: AI for Cardiovascular Risk Screening"
- Project logo
- Subtitle: "Research Prototype Demo"

**Voiceover**:
> "CardioRetina-AI is a research project exploring how artificial intelligence can predict cardiovascular disease risk from retinal fundus images. This demonstration shows the web interface and prediction capabilities."

**On-screen text**:
- Research prototype only
- Not for clinical use

---

### Scene 2: System Overview (45 seconds)

**Visual**:
- Split screen or carousel showing:
  - Dashboard interface
  - Model architecture diagram
  - Grad-CAM visualization

**Voiceover**:
> "The system combines deep learning models including EfficientNet and Vision Transformers to analyze retinal images. It also incorporates clinical data like blood pressure and cholesterol levels for multimodal prediction."

**On-screen text**:
- Hybrid CNN + ViT architecture
- Clinical data fusion
- Explainable AI with Grad-CAM

---

### Scene 3: Uploading an Image (45 seconds)

**Visual**:
- Screen recording of dashboard
- Drag-and-drop image upload
- Image preview appearing

**Voiceover**:
> "To begin, upload a retinal fundus image. The system accepts standard image formats and automatically preprocesses the image for analysis."

**On-screen text**:
- Supported formats: JPEG, PNG, BMP, TIFF
- Recommended: 45° field of view fundus photo

**Action**:
1. Show empty upload area
2. Drag test image onto area
3. Preview appears
4. Brief pause to show result

---

### Scene 4: Entering Clinical Data (60 seconds)

**Visual**:
- Clinical data form being filled
- Each field highlighted as entered

**Voiceover**:
> "Next, enter the patient's clinical information. The model uses eight features including age, blood pressure, cholesterol levels, body mass index, and lifestyle factors like smoking and physical activity."

**On-screen text** (as fields are filled):
- Age: 55 years
- Blood Pressure: 140/90 mmHg
- Cholesterol: 240 mg/dL
- BMI: 28.5
- Non-smoker, no diabetes, sedentary

**Action**:
1. Cursor moves to first field
2. Values entered one by one
3. Brief pause on completed form

---

### Scene 5: Submitting and Processing (30 seconds)

**Visual**:
- Submit button click
- Loading animation
- Progress indicator (if available)

**Voiceover**:
> "Clicking analyze sends the data to the model. Processing typically takes one to two seconds on GPU-enabled systems."

**Action**:
1. Click "Analyze Risk" button
2. Show loading spinner
3. Brief wait
4. Results appear

---

### Scene 6: Viewing Results (60 seconds)

**Visual**:
- Full results panel
- Risk gauge animation
- Probability value displayed

**Voiceover**:
> "The results show a risk probability between zero and one, categorized as low, moderate, or high risk. This example shows a high-risk prediction of seventy-six percent, based on the elevated blood pressure and other clinical factors."

**On-screen text**:
- Risk Probability: 0.76
- Risk Level: High
- Confidence: 0.89

**Action**:
1. Results panel fully visible
2. Risk gauge fills to show value
3. Clinical factors breakdown visible

---

### Scene 7: Explainability - Grad-CAM (45 seconds)

**Visual**:
- Grad-CAM heatmap overlay
- Side-by-side original and highlighted
- Hotspots clearly visible

**Voiceover**:
> "Grad-CAM visualization highlights the regions of the retinal image that contributed most to the prediction. In this case, the model focused on the optic disc area and surrounding vessels. This explainability helps researchers understand model behavior."

**On-screen text**:
- Red/Yellow: High importance regions
- Blue: Low importance regions

**Action**:
1. Show original image
2. Fade to Grad-CAM overlay
3. Highlight key areas

---

### Scene 8: API Usage (30 seconds)

**Visual**:
- Code editor or terminal
- cURL command execution
- JSON response displayed

**Voiceover**:
> "For programmatic access, a REST API is available. This example shows a prediction request using cURL with the returned JSON response."

**On-screen text** (code snippet):
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@image.jpg" \
  -F "age=55" ...
```

---

### Scene 9: Key Features Summary (30 seconds)

**Visual**:
- Bullet point list with icons
- Key features displayed

**Voiceover**:
> "CardioRetina-AI demonstrates several important capabilities: multimodal learning combining images and clinical data, explainable AI for transparency, a production-ready API, and comprehensive evaluation tools."

**On-screen text**:
- Hybrid CNN + ViT architecture
- Multimodal clinical data fusion
- Grad-CAM explainability
- FastAPI inference server
- Docker deployment support

---

### Scene 10: Disclaimer and Closing (30 seconds)

**Visual**:
- Important disclaimer text
- GitHub repository link
- Contact information

**Voiceover**:
> "Important: CardioRetina-AI is a research prototype for educational purposes only. It is not intended for clinical diagnosis or treatment decisions. Always consult healthcare professionals for medical advice."

**On-screen text**:
- Research prototype only
- Not for clinical use
- Not FDA approved
- Always consult healthcare professionals

**Ending screen**:
- GitHub: github.com/aarohidev91/cardioretina-ai
- Documentation: [link to docs]

---

## Recording Tips

### Software

| Platform | Recommended Tools |
|----------|-----------------|
| **macOS** | ScreenFlow, Camtasia, OBS Studio |
| **Windows** | Camtasia, OBS Studio, Xbox Game Bar |
| **Linux** | OBS Studio, SimpleScreenRecorder |

### Settings

- **Resolution**: Match screen resolution
- **Audio**: Record system audio + microphone
- **Mouse**: Highlight clicks (software cursor)
- **Zoom**: Use smooth zoom for details

### Best Practices

1. **Prepare environment**:
   - Clean desktop
   - Close notifications
   - Set appropriate browser zoom

2. **Practice the script**:
   - Rehearse before recording
   - Time each section
   - Prepare for mistakes

3. **Recording**:
   - Pause between sections
   - Record audio separately if needed
   - Leave buffer time for editing

4. **Post-production**:
   - Trim unnecessary pauses
   - Add transitions between scenes
   - Include captions for accessibility
   - Add background music (optional, low volume)

## Voiceover Script (Full Text)

```
[Scene 1]
CardioRetina-AI is a research project exploring how artificial intelligence 
can predict cardiovascular disease risk from retinal fundus images. This 
demonstration shows the web interface and prediction capabilities.

[Scene 2]
The system combines deep learning models including EfficientNet and Vision 
Transformers to analyze retinal images. It also incorporates clinical data like 
blood pressure and cholesterol levels for multimodal prediction.

[Scene 3]
To begin, upload a retinal fundus image. The system accepts standard image 
formats and automatically preprocesses the image for analysis.

[Scene 4]
Next, enter the patient's clinical information. The model uses eight features 
including age, blood pressure, cholesterol levels, body mass index, and 
lifestyle factors like smoking and physical activity.

[Scene 5]
Clicking analyze sends the data to the model. Processing typically takes one to 
two seconds on GPU-enabled systems.

[Scene 6]
The results show a risk probability between zero and one, categorized as low, 
moderate, or high risk. This example shows a high-risk prediction of seventy-six 
percent, based on the elevated blood pressure and other clinical factors.

[Scene 7]
Grad-CAM visualization highlights the regions of the retinal image that 
contributed most to the prediction. In this case, the model focused on the 
optic disc area and surrounding vessels. This explainability helps researchers 
understand model behavior.

[Scene 8]
For programmatic access, a REST API is available. This example shows a prediction 
request using cURL with the returned JSON response.

[Scene 9]
CardioRetina-AI demonstrates several important capabilities: multimodal learning 
combining images and clinical data, explainable AI for transparency, a 
production-ready API, and comprehensive evaluation tools.

[Scene 10]
Important: CardioRetina-AI is a research prototype for educational purposes only. 
It is not intended for clinical diagnosis or treatment decisions. Always consult 
healthcare professionals for medical advice.
```

## Alternative: Text-Only Demo

For silent demos or text overlays:

Replace voiceover with on-screen text synchronized with actions. Use larger font and ensure sufficient display time for reading.

---

*A well-produced demo video effectively communicates the project's capabilities and intended use.*
