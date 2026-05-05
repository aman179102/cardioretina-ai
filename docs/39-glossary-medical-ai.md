# Glossary of Medical AI Terms

## Overview

Definitions of key terms used in medical artificial intelligence, specifically relevant to the CardioRetina-AI project.

## A

**Ablation Study**
Systematic removal of components to measure their contribution. In our project, we test CNN-only, ViT-only, and hybrid configurations to validate the architecture.

**AUC-ROC (Area Under the Receiver Operating Characteristic Curve)**
Metric measuring the model's ability to distinguish between classes across all thresholds. AUC of 0.5 = random, 1.0 = perfect. Our target is >0.85.

**AUC-PR (Area Under the Precision-Recall Curve)**
Similar to AUC-ROC but focuses on precision-recall trade-off, more informative for imbalanced datasets.

## B

**Binary Classification**
Predicting between two classes (e.g., low risk vs. high risk). Our model outputs probabilities that are thresholded to binary predictions.

**Biomarker**
A measurable indicator of a biological state or condition. Retinal vessel patterns serve as biomarkers for cardiovascular health.

**BMI (Body Mass Index)**
Clinical feature used by our model: weight(kg) / height(m)². Normal range: 18.5-24.9.

## C

**Cardiovascular Disease (CVD)**
Class of diseases involving the heart or blood vessels. The target condition our model predicts risk for.

**CLAHE (Contrast Limited Adaptive Histogram Equalization)**
Image enhancement technique used in preprocessing to improve vessel visibility in retinal images.

**Clinical Data**
Structured health information (age, blood pressure, cholesterol, etc.) used alongside images in our multimodal model.

**Confusion Matrix**
Table showing true positives, false positives, true negatives, and false negatives. Helps identify specific error patterns.

## D

**Data Augmentation**
Techniques to artificially increase training data variety (rotation, flipping, color jitter) to improve generalization.

**Demographic Parity**
Fairness metric requiring equal positive prediction rates across demographic groups.

**Diastolic BP**
Lower blood pressure value (when heart rests). Clinical feature: normal <80 mmHg.

**Dropout**
Regularization technique randomly disabling neurons during training to prevent overfitting. We use 0.3 dropout rate.

## E

**Early Stopping**
Training termination when validation performance stops improving. We use patience=10 epochs.

**EfficientNet**
CNN architecture using compound scaling. Our model uses EfficientNet-B3 as the CNN backbone.

**Embryological Origin**
Developmental source. Retinal and coronary vessels share embryological origins, explaining their correlation.

**Epoch**
One complete pass through the training dataset. Typical training uses 50-100 epochs.

**Ethics Approval (IRB)**
Institutional Review Board approval required for research using human data. Essential for medical AI projects.

**Explainable AI (XAI)**
Methods making AI decisions interpretable. We use Grad-CAM and SHAP for explaining predictions.

## F

**False Negative**
Case incorrectly predicted as negative (low risk) when actually positive (high risk). Critical error in screening.

**False Positive**
Case incorrectly predicted as positive (high risk) when actually negative (low risk).

**FastAPI**
Modern Python web framework for building APIs. Used for our inference server.

**F1-Score**
Harmonic mean of precision and recall: 2 × (precision × recall) / (precision + recall). Balances both metrics.

**Fairness**
Ensuring equitable model performance across demographic groups. Important ethical consideration.

**Feature Fusion**
Combining features from different sources (images + clinical data). Our model uses late fusion.

**Federated Learning**
Training across decentralized data sources without sharing raw data. Future research direction.

**Fundus Photography**
Photographic technique for capturing retinal images. Our model's input data type.

## G

**Generalization**
Model's ability to perform well on unseen data. Key goal of proper training and regularization.

**Grad-CAM (Gradient-weighted Class Activation Mapping)**
Visualization technique showing which image regions influenced predictions. Our primary explainability method.

**Ground Truth**
Actual correct labels for training and evaluation. In our case, verified cardiovascular risk status.

**GPU (Graphics Processing Unit)**
Hardware accelerator for deep learning training and inference. Enables faster processing.

## H

**Healthcare Disparity**
Differences in healthcare access or outcomes between populations. Medical AI must avoid exacerbating these.

**Held-out Test Set**
Data completely separate from training/validation, used only for final evaluation to prevent overfitting.

**HIPAA**
US Health Insurance Portability and Accountability Act. Governs health data privacy and security.

**Hybrid Architecture**
Combining multiple model types (CNN + ViT in our case) to leverage complementary strengths.

**Hyperparameter**
Configuration value set before training (learning rate, batch size, etc.). Requires tuning.

## I

**ImageNet**
Large-scale image dataset used for pre-training. We use ImageNet weights for transfer learning.

**Inference**
Making predictions with a trained model. Our API performs inference on uploaded images.

**Informed Consent**
Process ensuring participants understand and agree to research use of their data. Ethical requirement.

**IRB (Institutional Review Board)**
Committee reviewing research ethics. Approval required for using patient data.

## L

**Label**
The correct answer for training data (0=low risk, 1=high risk in our binary classification).

**Late Fusion**
Combining modalities at the classification stage (vs. early in the pipeline). Our chosen approach.

**Learning Rate**
Step size for gradient descent optimization. Critical hyperparameter affecting convergence.

**Loss Function**
Measure of prediction error. We use Binary Cross-Entropy for classification.

## M

**Medical AI**
Artificial intelligence applications in healthcare. Our project demonstrates research in this field.

**Metrics**
Quantitative measures of model performance (accuracy, AUC, precision, recall, etc.).

**Microvasculature**
Small blood vessels, including those in the retina that provide cardiovascular insights.

**Mixed Precision Training**
Using both 16-bit and 32-bit floats to accelerate training and reduce memory usage.

**Model Card**
Documentation standard describing model characteristics, limitations, and intended use. We include one in the project.

**Multimodal Learning**
Combining multiple data types (images + clinical features). Core aspect of our architecture.

## N

**NaN (Not a Number)**
Error value often indicating numerical instability in training (e.g., exploding gradients).

**Normalization**
Scaling data to standard range. Images normalized using ImageNet statistics.

## O

**ONNX**
Open Neural Network Exchange format for model portability. Optional export format.

**Overfitting**
Model memorizing training data instead of learning generalizable patterns. Addressed via regularization.

## P

**Patch (ViT)**
Small image region (16×16 pixels) processed by Vision Transformer. ViT-Base uses 196 patches for 224×224 images.

**Precision**
True positives / (true positives + false positives). Measures reliability of positive predictions.

**Pre-training**
Training on large dataset (ImageNet) before task-specific fine-tuning. Improves performance with limited medical data.

**Protected Health Information (PHI)**
Individually identifiable health information. Subject to strict privacy regulations.

## R

**Recall (Sensitivity)**
True positives / (true positives + false negatives). Measures coverage of actual positives.

**Receiver Operating Characteristic (ROC)**
Curve plotting true positive rate vs. false positive rate at various thresholds.

**Regularization**
Techniques preventing overfitting (dropout, weight decay, data augmentation).

**Reproducibility**
Ability to obtain same results given same code, data, and configuration. Core scientific principle.

**Retinal Fundus**
Interior surface of the eye opposite the lens, including retina, optic disc, macula, and blood vessels.

**Risk Factor**
Attribute increasing probability of disease. Age, BP, cholesterol are cardiovascular risk factors.

## S

**Self-Attention (ViT)**
Mechanism allowing each patch to attend to all other patches, capturing global context.

**Sensitivity**
Same as Recall. Proportion of actual positives correctly identified.

**SHAP (SHapley Additive exPlanations)**
Feature attribution method based on game theory. Used for explaining clinical feature importance.

**Specificity**
True negatives / (true negatives + false positives). Measures coverage of actual negatives.

**Stratified Sampling**
Maintaining class proportions in train/val/test splits. Ensures representative evaluation.

**Systolic BP**
Higher blood pressure value (when heart contracts). Clinical feature: normal <120 mmHg.

## T

**Test Set**
Data used only for final evaluation, never during training or hyperparameter tuning.

**Threshold**
Value converting probabilities to class predictions. Default is 0.5 but can be adjusted.

**Torch (PyTorch)**
Deep learning framework used for model implementation.

**Tortuosity**
Twisting or winding of blood vessels. Retinal vessel tortuosity correlates with cardiovascular risk.

**Training Set**
Data used to train model parameters via gradient descent.

**Transfer Learning**
Leveraging pre-trained model weights for new task. Our approach with ImageNet weights.

**True Negative**
Correctly predicted negative case (correctly identified low risk).

**True Positive**
Correctly predicted positive case (correctly identified high risk).

## U

**Underfitting**
Model too simple to capture patterns in data. Opposite of overfitting.

**U-Net**
Popular CNN architecture for medical image segmentation. Not used in our classification task but relevant to the field.

## V

**Validation Set**
Data used for hyperparameter tuning and early stopping during training.

**Vessel Caliber**
Width of blood vessels. Narrowing of retinal arterioles indicates hypertension.

**ViT (Vision Transformer)**
Transformer architecture adapted for images. Our model uses ViT-Base for global feature extraction.

**Virtual Environment**
Isolated Python environment for project dependencies. Essential for reproducibility.

## W

**Weight Decay**
L2 regularization penalizing large weights. Helps prevent overfitting. We use 1e-4.

**Workflow**
Sequence of steps in a process. Our project includes training, evaluation, and inference workflows.

---

*Understanding terminology is essential for effective communication in interdisciplinary medical AI teams.*
