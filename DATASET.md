# Dataset Specification: CardioRetina-AI

## Expected Format

The dataset should be provided as a CSV file with corresponding retinal fundus images in a directory.

### CSV Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `image_path` | string | Yes | Relative path to the retinal fundus image file |
| `label` | integer | Yes | Binary label: 0 = low risk, 1 = high risk |
| `age` | float | Yes | Patient age in years (0-120) |
| `systolic_bp` | float | Yes | Systolic blood pressure in mmHg (50-300) |
| `diastolic_bp` | float | Yes | Diastolic blood pressure in mmHg (30-200) |
| `cholesterol` | float | Yes | Total cholesterol in mg/dL (50-600) |
| `bmi` | float | Yes | Body Mass Index in kg/m² (10-70) |
| `smoking` | integer | Yes | Smoking status: 0 = No, 1 = Yes |
| `diabetes` | integer | Yes | Diabetes status: 0 = No, 1 = Yes |
| `physical_activity` | integer | Yes | 0 = Sedentary, 1 = Active |

### Example CSV

```csv
image_path,label,age,systolic_bp,diastolic_bp,cholesterol,bmi,smoking,diabetes,physical_activity
patient_001/fundus_left.jpg,0,55,120,80,190,24.5,0,0,1
patient_002/fundus_right.jpg,1,68,155,95,260,31.2,1,1,0
patient_003/fundus_left.jpg,0,42,110,70,180,22.0,0,0,1
```

### Image Requirements

- **Format**: JPEG, PNG, BMP, or TIFF
- **Content**: Color retinal fundus photographs
- **Resolution**: Any resolution (automatically resized to 224x224)
- **Color**: RGB (grayscale images will be converted)
- **Quality**: Clinical-grade preferred; avoid severely blurred or occluded images

## Preprocessing Pipeline

1. **Resize** to 224x224 pixels
2. **CLAHE** (Contrast Limited Adaptive Histogram Equalization) on L-channel
3. **Optional denoising** using bilateral filter
4. **Normalization** to [0, 1] range
5. **ImageNet standardization** (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

## Augmentation (Training Only)

- Random rotation (±15°)
- Horizontal flip (p=0.5)
- Vertical flip (p=0.5)
- Random gamma correction (0.8-1.2)
- Color jitter (brightness=0.2, contrast=0.2)

## Label Requirements

- Binary labels only: 0 or 1
- Label 0: Low cardiovascular risk
- Label 1: High cardiovascular risk
- Labels should be determined by clinical assessment (not self-reported)

## Data Splitting

The split script (`cardioretina.data.split`) creates stratified train/val/test splits:
- **Default**: 70% train / 15% validation / 15% test
- **Stratification**: Preserves label distribution across splits
- **Output**: `train.csv`, `val.csv`, `test.csv` in the specified output directory

```bash
python -m cardioretina.data.split path/to/dataset.csv --output-dir data/splits/ --train-ratio 0.7 --val-ratio 0.15
```

## Validation

Run the validation script to check dataset integrity:

```bash
python -m cardioretina.data.validate path/to/dataset.csv --image-dir path/to/images/
```

This checks:
- Required columns exist
- Labels are binary (0 or 1)
- No missing values in required columns
- Image files exist on disk
- Clinical values are within expected ranges
- Class distribution and imbalance warnings

## Bias Risks

- **Demographic bias**: Retinal datasets may underrepresent certain age groups, ethnicities, or genders
- **Camera bias**: Different fundus cameras produce varying image characteristics
- **Geographic bias**: Training data from specific regions may not generalize globally
- **Selection bias**: Hospital-based datasets may overrepresent severe cases
- **Label bias**: Clinical diagnosis criteria may vary across institutions

## Privacy Considerations

- Retinal images are **biometric identifiers** — treat as sensitive personal data
- Do not include patient-identifiable information in file names or metadata
- Follow applicable data protection regulations (GDPR, HIPAA, etc.)
- Consider de-identification procedures before sharing datasets
- Store and transmit data using appropriate security measures

## Recommended Datasets for Research

While this project does not include a dataset, the following public datasets may be suitable for adaptation:
- **ODIR-5K**: Ocular Disease Intelligent Recognition
- **EyePACS**: Diabetic retinopathy detection
- **DRIVE / STARE**: Retinal vessel segmentation
- **UK Biobank**: Large-scale retinal imaging cohort (requires application)

> Note: These datasets may require label engineering to create cardiovascular risk labels.
