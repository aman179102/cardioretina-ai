# Glossary of Deep Learning Terms

## Overview

Definitions of key deep learning terms used throughout the CardioRetina-AI project.

## A

**Ablation Study**
Systematic process of removing components from a model to understand their individual contributions. We use this to validate our hybrid architecture.

**Activation Function**
Non-linear function applied to neuron outputs. ReLU (Rectified Linear Unit) is most common: f(x) = max(0, x).

**Adam Optimizer**
Adaptive moment estimation optimizer combining momentum and RMSprop. We use it with learning rate 0.001.

**Attention Mechanism**
Neural network component allowing model to focus on relevant parts of input. ViT uses self-attention across image patches.

**Autoencoder**
Neural network learning to compress and reconstruct input. Not used in our project but relevant for representation learning.

## B

**Backpropagation**
Algorithm computing gradients of loss with respect to weights by applying chain rule backward through the network.

**Batch**
Subset of training data processed together. We use batch size 32 for training.

**Batch Normalization**
Technique normalizing layer inputs to stabilize and accelerate training. Applied after convolutional and linear layers.

**Bias (Neural Network)**
Additional learnable parameter allowing activation shift. Present in all linear layers.

**Binary Cross-Entropy**
Loss function for binary classification: -[y·log(p) + (1-y)·log(1-p)]. Our training loss.

**Bounding Box**
Rectangle enclosing an object in image. Not directly used in our classification task.

## C

**Checkpoint**
Saved model state (weights, optimizer state) during training. We save best model based on validation performance.

**Classification**
Predicting discrete class labels. Our task: binary classification (low vs. high cardiovascular risk).

**CNN (Convolutional Neural Network)**
Neural network using convolution operations. EfficientNet-B3 is our CNN backbone.

**Compound Scaling**
EfficientNet's approach scaling depth, width, and resolution together rather than independently.

**Concatenation**
Joining tensors along a dimension. We concatenate CNN, ViT, and clinical features before classification.

**Convergence**
State where training loss stops decreasing significantly. We use early stopping to detect convergence.

**Convolution**
Operation sliding filter over input to detect local patterns. Core of CNN architecture.

## D

**Dense Layer (Fully Connected)**
Layer where every input connects to every output. Used in clinical network and classifier head.

**Depth (Network)**
Number of layers in network. Deeper networks can learn more complex features.

**Dropout**
Regularization technique randomly setting fraction of inputs to zero during training. We use rate 0.3.

## E

**Early Stopping**
Training termination when validation metric stops improving. Prevents overfitting. Our patience: 10 epochs.

**Embedding**
Learned representation mapping discrete or high-dimensional data to lower-dimensional space.

**Epoch**
Complete pass through entire training dataset. Typical training: 50-100 epochs.

**Exploding Gradients**
Problem where gradients become extremely large during backpropagation. Solved by gradient clipping.

**Extracted Features**
Representations learned by network layers. CNN outputs 1536-dim features, ViT outputs 512-dim.

## F

**Feature Map**
Output of convolutional layer representing detected patterns at different locations.

**Feature Vector**
One-dimensional representation of input. Our fusion layer combines feature vectors from multiple sources.

**Filter (Kernel)**
Small matrix slid over input during convolution to detect specific patterns.

**Fine-tuning**
Adapting pre-trained model to specific task. We fine-tune ImageNet weights on retinal images.

**Forward Pass**
Computing network output from input through sequential layer operations.

**Fully Connected Layer**
See Dense Layer.

## G

**GAP (Global Average Pooling)**
Averaging spatial dimensions to produce fixed-size output regardless of input size.

**Gradient**
Vector of partial derivatives indicating direction of steepest loss increase. Used to update weights.

**Gradient Clipping**
Limiting gradient magnitude to prevent exploding gradients. Optional technique.

**Gradient Descent**
Optimization algorithm updating weights in direction of negative gradient to minimize loss.

## H

**Hidden Layer**
Layer between input and output. Our fusion and classification layers are hidden.

**Hidden Units**
Neurons in hidden layers. Clinical network has 64 then 32 hidden units.

**Hyperparameter**
Configuration set before training (learning rate, batch size, architecture choices). Requires tuning.

## I

**ImageNet**
Large-scale dataset (1.28M images, 1000 classes) commonly used for pre-training. Source of our transfer learning weights.

**Inference**
Forward pass to generate predictions from trained model. Our API performs inference.

**Input Layer**
First layer receiving raw data (224×224×3 images or 8 clinical features).

## K

**Kernel (Filter)**
See Filter.

**Kernel Size**
Dimensions of convolution filter (e.g., 3×3, 16×16 for ViT patches).

## L

**Label**
Ground truth target for supervised learning. Our labels: 0 (low risk), 1 (high risk).

**Late Fusion**
Combining features at later stage (before classifier) vs. early fusion (at input).

**Layer**
Collection of neurons processing data. Networks stack multiple layers.

**Learning Rate**
Step size for gradient descent. Critical hyperparameter: too high = unstable, too low = slow.

**Linear Layer**
Layer computing weighted sum of inputs plus bias: y = Wx + b.

**Loss Function**
Measure of prediction error to minimize during training. Ours: Binary Cross-Entropy.

## M

**Mini-batch**
Small subset of data processed together. See Batch.

**Mixed Precision**
Using 16-bit and 32-bit floats to accelerate training. Optional optimization.

**Model Capacity**
Ability to fit complex functions. Determined by architecture (depth, width).

**Momentum**
Optimization technique accelerating gradient descent by adding fraction of previous update.

**Multi-task Learning**
Training single model on multiple related tasks. Not used in our project but relevant technique.

**Multimodal Learning**
Combining multiple data modalities (images + clinical data). Core of our architecture.

## N

**Neuron**
Basic computational unit receiving inputs, applying weights, adding bias, passing through activation.

**Normalization**
Scaling data to standard range or distribution. Essential for stable training.

## O

**One-hot Encoding**
Representing categorical variables as binary vectors. Not needed for our numerical features.

**Optimizer**
Algorithm updating weights based on gradients. We use Adam.

**Output Layer**
Final layer producing predictions. Ours: single unit with sigmoid activation.

**Overfitting**
Model memorizing training data rather than learning generalizable patterns. Addressed via regularization.

## P

**Padding**
Adding border pixels to maintain spatial dimensions after convolution.

**Parameter**
Learnable value (weight or bias) updated during training. Model size measured by parameter count.

**Patch (ViT)**
Small image region (16×16 pixels) treated as token in Vision Transformer.

**Pooling**
Downsampling operation reducing spatial dimensions (max pooling, average pooling).

**Precision (Metric)**
True positives / (true positives + false positives). Measures reliability of positive predictions.

**Pre-training**
Training on large dataset before task-specific fine-tuning. We use ImageNet pre-training.

## R

**Random Seed**
Value initializing random number generator for reproducibility. We set seed for all libraries.

**Recall (Metric)**
True positives / (true positives + false negatives). Measures coverage of actual positives.

**Receptive Field**
Region of input affecting a particular neuron. Larger in deeper layers.

**Regularization**
Techniques preventing overfitting: dropout, weight decay, data augmentation, early stopping.

**ReLU (Rectified Linear Unit)**
Activation function: f(x) = max(0, x). Default choice for hidden layers.

**Residual Connection**
Skip connection adding input to output: output = F(x) + x. Enables training very deep networks.

**RGB**
Color space with Red, Green, Blue channels. Our input images are RGB.

## S

**Self-Attention**
Attention mechanism relating different positions within same sequence. Core of ViT.

**Semantic Segmentation**
Classifying every pixel in image. Not our task but related computer vision task.

**Sigmoid**
Activation function mapping to (0, 1): σ(x) = 1 / (1 + e^(-x)). Our output activation for probabilities.

**Skip Connection**
See Residual Connection.

**Softmax**
Activation function for multi-class classification converting logits to probabilities summing to 1.

**Spatial Dimensions**
Height and width of feature maps. Decrease through pooling, increase through upsampling.

**Stride**
Step size for sliding convolution filter. Stride > 1 reduces spatial dimensions.

**Supervised Learning**
Learning from labeled examples (input, target) pairs. Our training approach.

## T

**Target**
Desired output for given input. Same as Label.

**Test Set**
Data held out for final evaluation only. Never used during training or validation.

**Token (ViT)**
Embedding of image patch plus position information. Input to transformer encoder.

**Transfer Learning**
Applying knowledge from one task to another. We transfer ImageNet features to retinal images.

**Transformer**
Architecture using self-attention mechanisms. ViT applies to images.

**True Negative**
Correctly predicted negative class.

**True Positive**
Correctly predicted positive class.

## U

**Underfitting**
Model too simple to capture data patterns. Opposite of overfitting.

**Unit (Neural Network)**
See Neuron.

**Unsupervised Learning**
Learning without labels. Not used in our supervised classification task.

**Upsampling**
Increasing spatial dimensions. Opposite of pooling.

## V

**Validation Set**
Data used for hyperparameter tuning and early stopping during training.

**Vanishing Gradients**
Problem where gradients become extremely small in deep networks. Addressed by residual connections.

**ViT (Vision Transformer)**
Transformer architecture adapted for images by treating patches as tokens.

**Vocabulary (ViT)**
Set of possible tokens. For images, vocabulary is learned patch embeddings.

## W

**Weight**
Learnable parameter multiplying input in linear layer. Updated during training.

**Weight Decay**
L2 regularization adding penalty proportional to squared weights. We use 1e-4.

**Weight Initialization**
Strategy for setting initial weight values. Critical for training stability.

**Width (Network)**
Number of units in a layer. Wider networks have more parameters.

---

*Understanding deep learning terminology enables effective communication about model architecture, training, and behavior.*
