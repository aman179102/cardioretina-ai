# Research References Notes

## Overview

Key research papers and resources that inform the CardioRetina-AI project.

## Foundational Papers

### Retinal-Cardiovascular Connection

**1. Poplin et al. (2018)** - *Prediction of cardiovascular risk factors from retinal fundus photographs via deep learning*
- **Journal**: Nature Biomedical Engineering
- **Key Finding**: Deep learning can predict cardiovascular risk factors from retinal images with accuracy comparable to traditional risk calculators
- **Significance**: Demonstrated feasibility of retinal-based cardiovascular prediction
- **Citation**: Poplin, R., et al. (2018). "Prediction of cardiovascular risk factors from retinal fundus photographs via deep learning." *Nature Biomedical Engineering*, 2(3), 158-164.

**2. Wong & Mitchell (2004)** - *Hypertensive retinopathy*
- **Journal**: New England Journal of Medicine
- **Key Finding**: Established connection between retinal vascular changes and systemic hypertension
- **Significance**: Clinical foundation for retinal-cardiovascular associations
- **Citation**: Wong, T. Y., & Mitchell, P. (2004). "Hypertensive retinopathy." *New England Journal of Medicine*, 351(22), 2310-2317.

### Deep Learning Architectures

**3. Tan & Le (2019)** - *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*
- **Conference**: ICML 2019
- **Key Finding**: Compound scaling (depth, width, resolution) achieves better efficiency
- **Significance**: Basis for EfficientNet backbone selection
- **Citation**: Tan, M., & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks." *ICML 2019*.

**4. Dosovitskiy et al. (2021)** - *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*
- **Conference**: ICLR 2021
- **Key Finding**: Vision Transformers can achieve competitive performance without convolution
- **Significance**: Foundation for ViT module implementation
- **Citation**: Dosovitskiy, A., et al. (2021). "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale." *ICLR 2021*.

## Explainability Methods

**5. Selvaraju et al. (2017)** - *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization*
- **Conference**: ICCV 2017
- **Key Finding**: Gradient-weighted class activation mapping for visual explanations
- **Significance**: Core explainability method for retinal visualization
- **Citation**: Selvaraju, R. R., et al. (2017). "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization." *ICCV 2017*.

**6. Lundberg & Lee (2017)** - *A Unified Approach to Interpreting Model Predictions*
- **Conference**: NeurIPS 2017
- **Key Finding**: SHAP values provide consistent feature attribution
- **Significance**: Method for clinical feature importance analysis
- **Citation**: Lundberg, S. M., & Lee, S. I. (2017). "A Unified Approach to Interpreting Model Predictions." *NeurIPS 2017*.

## Medical AI Ethics

**7. Price & Cohen (2019)** - *Privacy in the Age of Medical Big Data*
- **Journal**: Nature Medicine
- **Key Finding**: Discusses privacy challenges in medical AI
- **Significance**: Informs privacy considerations in the project

**8. Amann et al. (2020)** - *Explainability for artificial intelligence in healthcare*
- **Journal**: BMC Medical Informatics and Decision Making
- **Key Finding**: Comprehensive review of explainability methods in healthcare
- **Significance**: Guides explainability implementation choices

## Related Work in Medical Imaging

### Retinal Image Analysis

**9. Abramoff et al. (2016)** - *Improved Automated Detection of Diabetic Retinopathy*
- **Key Finding**: FDA-approved AI system for diabetic retinopathy detection
- **Significance**: Demonstrates regulatory pathway for retinal AI

**10. Gulshan et al. (2016)** - *Development and Validation of a Deep Learning Algorithm*
- **Journal**: JAMA
- **Key Finding**: Deep learning for diabetic retinopathy detection
- **Significance**: Validation methodology reference

### Multimodal Learning

**11. Huang et al. (2020)** - *Fusion of medical imaging and clinical data*
- **Key Finding**: Methods for combining imaging and structured clinical data
- **Significance**: Informs fusion strategy decisions

## Technical Resources

### PyTorch and Deep Learning

**12. Paszke et al. (2019)** - *PyTorch: An Imperative Style, High-Performance Deep Learning Library*
- **Conference**: NeurIPS 2019
- **Key Finding**: PyTorch framework design and capabilities
- **Significance**: Technical foundation for implementation

### Vision Transformers

**13. Touvron et al. (2021)** - *Training data-efficient image transformers*
- **Key Finding**: Data-efficient training strategies for ViTs
- **Significance**: Training methodology for limited medical data

## Fairness and Bias

**14. Buolamwini & Gebru (2018)** - *Gender Shades*
- **Conference**: FAccT 2018
- **Key Finding**: Demonstrated racial and gender bias in facial recognition
- **Significance**: Motivation for bias analysis in medical AI

**15. Obermeyer et al. (2019)** - *Dissecting racial bias in an algorithm*
- **Journal**: Science
- **Key Finding**: Algorithmic bias in healthcare allocation
- **Significance**: Important cautionary tale for medical AI fairness

## MLOps and Engineering

**16. Huyen (2022)** - *Designing Machine Learning Systems*
- **Book**: O'Reilly
- **Key Finding**: Comprehensive guide to production ML systems
- **Significance**: Engineering best practices reference

## Citation Format

### For Papers

```bibtex
@article{poplin2018prediction,
  title={Prediction of cardiovascular risk factors from retinal fundus photographs via deep learning},
  author={Poplin, Ryan and Varadarajan, Avinash V and Blumer, Katy and Liu, Yun and McConnell, Michael V and Corrado, Greg S and Peng, Lily and Webster, Dale R},
  journal={Nature Biomedical Engineering},
  volume={2},
  number={3},
  pages={158--164},
  year={2018},
  publisher={Nature Publishing Group}
}

@inproceedings{tan2019efficientnet,
  title={Efficientnet: Rethinking model scaling for convolutional neural networks},
  author={Tan, Mingxing and Le, Quoc},
  booktitle={International Conference on Machine Learning},
  pages={6105--6114},
  year={2019},
  organization={PMLR}
}

@inproceedings{dosovitskiy2021image,
  title={An image is worth 16x16 words: Transformers for image recognition at scale},
  author={Dosovitskiy, Alexey and Beyer, Lucas and Kolesnikov, Alexander and Weissenborn, Dirk and Zhai, Xiaohua and Unterthiner, Thomas and Dehghani, Mostafa and Minderer, Matthias and Heigold, Georg and Gelly, Sylvain and others},
  booktitle={International Conference on Learning Representations},
  year={2021}
}

@inproceedings{selvaraju2017grad,
  title={Grad-cam: Visual explanations from deep networks via gradient-based localization},
  author={Selvaraju, Ramprasaath R and Cogswell, Michael and Das, Abhishek and Vedantam, Ramakrishna and Parikh, Devi and Batra, Dhruv},
  booktitle={Proceedings of the IEEE International Conference on Computer Vision},
  pages={618--626},
  year={2017}
}
```

## Reading Recommendations

### For Understanding Medical Context

1. Start with: Wong & Mitchell (2004) - Hypertensive retinopathy
2. Then: Poplin et al. (2018) - Deep learning for cardiovascular risk

### For Technical Implementation

1. Start with: Tan & Le (2019) - EfficientNet
2. Then: Dosovitskiy et al. (2021) - Vision Transformers
3. Finally: Selvaraju et al. (2017) - Grad-CAM

### For Ethical Considerations

1. Start with: Buolamwini & Gebru (2018) - Gender Shades
2. Then: Obermeyer et al. (2019) - Racial bias in healthcare algorithms

## Online Resources

### Datasets

- **UK Biobank Retinal Imaging**: Large-scale population study
- **EyePACS**: Diabetic retinopathy dataset
- **AREDS**: Age-Related Eye Disease Study

### Tools and Libraries

- **torchvision**: PyTorch computer vision library
- **timm**: PyTorch Image Models library
- **captum**: PyTorch model interpretability
- **grad-cam**: Grad-CAM implementation

### Community

- **Medical Imaging with Deep Learning (MIDL)**: Conference
- **MICCAI**: Medical image computing conference
- **arXiv cs.CV**: Computer vision preprints

## Notes for Future Research

### Gaps in Literature

1. **Longitudinal studies**: Most work is cross-sectional
2. **External validation**: Limited multi-center validation
3. **Fairness analysis**: Few studies analyze demographic performance
4. **Cost-effectiveness**: Economic analyses lacking

### Promising Directions

1. **Self-supervised learning**: For limited labeled data
2. **Federated learning**: Multi-center training without data sharing
3. **Uncertainty quantification**: Confidence in predictions
4. **Multi-task learning**: Joint prediction of multiple conditions

---

*Understanding the research foundation is essential for contextualizing contributions and identifying opportunities for advancement.*
