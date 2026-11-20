---
license: other
license_name: nvidia-open-model-license
license_link: https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf
base_model: nvidia/C-RADIOv4-H
---

# Model Overview

### Description or Model Summary with Description and License:
C-RADIOv4-H-AV generates embeddings for images and text in a shared space, used for text-to-image and image-to-image retrieval over autonomous vehicle (AV) driving data. C-RADIOv4-H-AV was developed by NVIDIA as a fine-tune of C-RADIOv4-H (SigLIP2-g adaptor), a contrastive CLIP-style model that outputs embeddings and similarity scores; it does not generate images or text. Only the SigLIP2-g adaptor head was trained; the image backbone and the text encoder are unchanged from the base model.<br>

This model is ready for commercial or non-commercial use. <br>

### License/Terms of Use:
GOVERNING TERMS: Use of this model is governed by the [NVIDIA Open Model License Agreement](https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf). <br>

The base model, C-RADIOv4-H, is governed by the [NVIDIA Open Model License Agreement](https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf). <br>

### Deployment Geography:
Global <br>

### Use Case: <br>
AV data engineers and developers searching large driving-data collections with text or image queries, for example finding traffic signs, traffic lights, road markings, intersections and other driving scenes. <br>

### Release Date:
Hugging Face 11/20/2026 via [https://huggingface.co/nvidia/C-RADIOv4-H-AV](https://huggingface.co/nvidia/C-RADIOv4-H-AV) <br>

## References(s):
* [C-RADIOv4 paper](https://arxiv.org/abs/2601.17237) <br>
* [RADIO on GitHub](https://github.com/NVlabs/RADIO) <br>
* [C-RADIOv4-H on Hugging Face](https://huggingface.co/nvidia/C-RADIOv4-H) <br>

## Model Architecture:
**Architecture Type:** Transformer <br>

**Network Architecture:** Other: Vision Transformer (ViT-H) image encoder with an MLP adaptor head (SigLIP2-g adaptor) and a text encoder <br>

**This model was developed based on C-RADIOv4-H** <br>

** Number of model parameters: C-RADIOv4-H (base) 653M. Only the SigLIP2-g adaptor head (8.9M parameters) was trained. <br>

## Input(s): <br>
**Input Type(s):** Image, Text <br>

**Input Format(s):** <br>
- Image: Red, Green, Blue (RGB) <br>
- Text: String <br>

**Input Parameters:** <br>
- Image: Two-Dimensional (2D) <br>
- Text: One-Dimensional (1D) <br>

**Other Properties Related to Input:** Images are resized to 384x384 without preserving the aspect ratio.  <br>

## Output(s)

**Output Type(s):** Other: Embeddings <br>

**Output Format(s):** Other: Tensor (embedding vectors) <br>

**Output Parameters:** One-Dimensional (1D) <br>

**Other Properties Related to Output:** 512-dimensional vectors (first 512 PCA components of the 1536-dimensional adaptor output). The PCA eigenvalues are near zero beyond about 500 components, so the reduction shows a negligible drop on the AV and generalization benchmarks. Image and text embeddings share one space and are compared with a dot product or cosine similarity. The model outputs embeddings only; it does not generate images or text. A downstream application can use the cosine similarity between a query (text or image) embedding and image embeddings to rank multiple images by relevance.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Usage:

The model is loaded with the RADIO PyTorch code through `torch.hub`, using the checkpoint downloaded from this repository. The 512-dimensional output is obtained by multiplying the eigenvectors (`c-radio_v4-h_half_av-eigenvectors.npy`) into the SigLIP2-g adaptor head weights and keeping the first 512 output dimensions. For both images and text, the adaptor returns a vector (`summary`) of shape (B, 1536) before truncation to (B, 512).

```python
import numpy as np
import torch
from huggingface_hub import hf_hub_download
from PIL import Image
from torchvision.transforms.functional import to_tensor

repo = "nvidia/C-RADIOv4-H-AV"

ckpt = hf_hub_download(repo, "c-radio_v4-h_half_av.pth.tar")
eigenvectors = hf_hub_download(repo, "c-radio_v4-h_half_av-eigenvectors.npy")

model = torch.hub.load("NVlabs/RADIO", "radio_model", version=ckpt,
                       adaptor_names=["siglip2-g"], progress=True)

# Absorb the PCA eigenvectors into the image and text heads of the SigLIP2-g adaptor.
E = torch.from_numpy(np.load(eigenvectors).astype(np.float32))
adaptor = model.adaptors["siglip2-g"]
for layer in (adaptor.head_mlp.final[2], adaptor.text_model.head):
    layer.weight.data = (E.T @ layer.weight.data.float()).to(layer.weight.dtype)
    layer.bias.data = (E.T @ layer.bias.data.float()).to(layer.bias.dtype)
model.eval().cuda()

# Image embedding.
image = Image.open("image.jpg").convert("RGB").resize((384, 384), Image.BICUBIC)
x = to_tensor(image).unsqueeze(0).cuda()
with torch.no_grad():
    summary, _ = model(x)["siglip2-g"]
image_embedding = summary[:, :512].float()

# Text embedding.
tokens = adaptor.tokenizer(["a traffic light"]).to("cuda")
with torch.no_grad():
    text_embedding = adaptor.encode_text(tokens)[:, :512].float()

# Cosine similarity can be used to rank images for a text or image query.
score = torch.nn.functional.cosine_similarity(image_embedding, text_embedding)
```

## Software Integration:
**Runtime Engine(s):**
* Not Applicable (N/A) - PyTorch <br>

**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Ampere <br>

**Supported Operating System(s):**
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment. <br>

## Model Version(s):
V1. The model can be integrated into an AI system by loading it with the RADIO PyTorch code (`torch.hub`) and calling it to embed images and text for retrieval. <br>

## Training, Testing, and Evaluation Datasets:

### Dataset Overview
** Total Size: 3,747,347 image-caption pairs (3,369,193 unique images) <br>
** Total Number of Datasets: 1 (MB AV Data, made of AV data and NVClip data) <br>

** A general description of the data processing involved in transforming the acquired data into the training data for the model: AV images from NVIDIA AV data are paired with captions generated by Kimi K3 and caption templates. NVClip image-caption pairs from NV-CC-Img-Text-Dataset are used with the captions provided. Image paths and captions are stored in a CSV of `image_path,caption` pairs. <br>

## Private Datasets
* List of parties providing datasets: NVIDIA (AV data and NV-CC-Img-Text-Dataset) <br>
* Number of data points: 3,747,347 image-caption pairs (about 1.8M AV and 1.8M NVClip) <br>
* Overall size per modality: about 274 GB of images <br>
* Nature of content: AV images (road-scene data that may contain personal data), synthetic captions <br>

## Self-Sourced Synthetic Data
* Number of data points: 1,850,979 AV captions <br>
* Overall size per modality: <br>
* A description of the methods used to synthetically generate training data: AV captions are generated with Kimi K3 and caption templates. <br>
* The name(s) of any AI model(s) used: Kimi K3 <br>

## Training Dataset:

### Data Modality:
* Image <br>
* Text <br>

### Training Data Size:

** Image Training Data Size
* 1 Million to 1 Billion Images <br>

** Text Training Data Size
* Less than a Billion Tokens <br>

** Data Collection Method by dataset
* Hybrid: Automatic/Sensors (AV data), Automated (NVClip data) <br>

** Labeling Method by dataset
* Hybrid: Synthetic (AV captions), Automated (NVClip captions) <br>

**Properties:** 3,747,347 image-caption pairs (1,850,979 AV, 1,896,368 NVClip) over 3,369,193 unique images, about 274 GB. The AV images come from a 120° field of view (FOV) car camera and cover road markings, lane markings, traffic signs, traffic lights, intersections and full driving scenes; they may contain personal data from real-world driving scenes. The captions are in English. <br>

### Testing Dataset:

Data Collection Method by dataset: <br>
* AV validation data: Automatic/Sensors <br>
* NVClip validation data: Automated <br>

Labeling Method by dataset: <br>
* AV validation data: Synthetic <br>
* NVClip validation data: Automated <br>

**Properties** The testing data is the validation set used to select the training epoch: 131,604 image-caption pairs (116,221 AV, 15,383 NVClip), image and text modalities, English captions. The AV images are road scenes from a 120° FOV car camera and may contain personal data from real-world driving scenes; the NVClip images are web images. For the AV data, the training, validation and evaluation sets share no H3 cell for a class. <br>

### Evaluation Dataset:

**Benchmark Score <br>

Data Collection Method by dataset: <br>
* AVObjects: Automatic/Sensors <br>
* NVImageNet: Automated <br>

Labeling Method by dataset: <br>
* AVObjects: Synthetic (text queries generated with Kimi K3) <br>
* NVImageNet: Automated (class label taken from the ImageNet category each image was collected for) <br>

**Properties** AVObjects has 73,961 gallery images (Intersection 5,466; Road Markings 10,162; Traffic Light 7,209; Traffic Sign 51,124), 843 query images and 93 text queries, all in English; the images are road scenes from a 120° FOV car camera and may contain personal data from real-world driving scenes. NVImageNet (NV-CC-Img-Text-Dataset, default version) is evaluated on 1,000 ImageNet classes with up to 100 images per class; the images are natural photos and the class names are in English. Evaluation covers AVObjects (image-to-image and text-to-image retrieval; Intersection, Road Markings, Traffic Light, Traffic Sign) and NVImageNet (Top-1 and Top-5 accuracy, to check that generalization is retained). The splits share no H3 cell per class with the training data. <br>

Higher is better for all metrics. <br>

NVImageNet:

| Model                              | Top-1 (%) | Top-5 (%) |
|------------------------------------|-----------|-----------|
| C-RADIOv4-H (base, no fine-tuning) | 60.8      | 84.5      |
| C-RADIOv4-H-AV                     | 57.6      | 82.2      |

AVObjects image-to-image retrieval:

| Dataset       | Model              | Pr@100 | Recall@100 | AUROC | PR_AUC |
|---------------|--------------------|--------|------------|-------|--------|
| Intersection  | C-RADIOv4-H (base) | 0.875  | 0.081      | 0.790 | 0.619  |
|               | C-RADIOv4-H-AV     | 0.902  | 0.083      | 0.880 | 0.736  |
| Road Markings | C-RADIOv4-H (base) | 0.437  | 0.035      | 0.584 | 0.236  |
|               | C-RADIOv4-H-AV     | 0.696  | 0.055      | 0.774 | 0.480  |
| Traffic Light | C-RADIOv4-H (base) | 0.632  | 0.036      | 0.594 | 0.356  |
|               | C-RADIOv4-H-AV     | 0.951  | 0.057      | 0.840 | 0.703  |
| Traffic Sign  | C-RADIOv4-H (base) | 0.574  | 0.119      | 0.855 | 0.304  |
|               | C-RADIOv4-H-AV     | 0.762  | 0.169      | 0.973 | 0.623  |

AVObjects text-to-image retrieval:

| Dataset       | Model              | Pr@100 | Recall@100 | AUROC | PR_AUC |
|---------------|--------------------|--------|------------|-------|--------|
| Intersection  | C-RADIOv4-H (base) | 0.926  | 0.086      | 0.881 | 0.749  |
|               | C-RADIOv4-H-AV     | 0.944  | 0.087      | 0.937 | 0.834  |
| Road Markings | C-RADIOv4-H (base) | 0.469  | 0.036      | 0.603 | 0.274  |
|               | C-RADIOv4-H-AV     | 0.577  | 0.046      | 0.772 | 0.464  |
| Traffic Light | C-RADIOv4-H (base) | 0.968  | 0.058      | 0.842 | 0.702  |
|               | C-RADIOv4-H-AV     | 0.943  | 0.056      | 0.875 | 0.726  |
| Traffic Sign  | C-RADIOv4-H (base) | 0.650  | 0.145      | 0.913 | 0.433  |
|               | C-RADIOv4-H-AV     | 0.762  | 0.175      | 0.977 | 0.624  |

## Inference:
**Acceleration (Engine used to optimize the runtime if applicable) Engine:** PyTorch <br>
**Test Hardware Set-Up (GPU Architecture, Model):** <br>
* NVIDIA Ampere A100 <br>

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse. <br>

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included. <br>

For more detailed information on ethical considerations for this model, please see the Model Card++ Bias, Explainability, Safety & Security, and Privacy Subcards below. <br>

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).  <br>

# Model Card++ Subcards

## Bias

Field                                                                                               |  Response
:---------------------------------------------------------------------------------------------------|:---------------
Participation considerations from adversely impacted groups [protected classes](https://calcivilrights.ca.gov/disputeresolution/protected-characteristics/) in model design and testing:  |  None
Measures taken to mitigate against unwanted bias:                                                   |  None
Bias Metric (If Measured):                                                   |  Not Applicable

## Explainability

Field                                                                                                  |  Response
:------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------
Intended Task/Domain:                                                                   |  Text-to-image and image-to-image retrieval over driving data
Model Type:                                                                                            |  Transformer
Intended Users:  |  AV data engineers and developers use this model to search large driving-data collections with text or image queries, for example to find traffic signs, traffic lights, road markings and intersections for data curation.
Output:                                                                                                |  512-dimensional image and text embeddings
Describe how the model works:                                                                          |  The image is resized and passed through a Vision Transformer and the SigLIP2-g adaptor head to give an embedding. The text is passed through the text encoder to give an embedding in the same space. A dot product or cosine similarity between the two gives the match score.
List the groups (or group characteristics) for which this was tested to produce comparable outcomes:  |  Not Applicable
Technical Limitations & Mitigation:                                                                    |  Fine-tuned on driving data from a 120° FOV car camera and evaluated on AVObjects and NVImageNet. Other camera setups and domains have not been evaluated; domain-specific evaluation is recommended for the target application.
Verified to have met prescribed NVIDIA quality standards:  |  Yes
Performance Metrics:                                                                                   |  Precision@100, Recall@100, AUROC, PR-AUC (AVObjects); Top-1 and Top-5 accuracy (NVImageNet)
Potential Known Risks:                                                                                 |  The model only computes similarity scores between the input images and text; it does not generate images or text. Rankings may place irrelevant items high, or miss relevant ones, for rare or unseen categories.
Licensing:                                                                                             |  [NVIDIA Open Model License](https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf)

## Privacy

The datasets used to train C-RADIOv4-H-AV included data from real-world road driving scenes. NVIDIA collected and used this data in compliance with applicable data protection and privacy laws. The datasets used to train this model were reviewed before release. Please review NVIDIA’s Privacy Policy (https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information. <br>

## Safety & Security

Field                                               |  Response
:---------------------------------------------------|:----------------------------------
Model Application Field(s):                               |  Autonomous Vehicles
Describe the life critical impact (if present).   |  Not applicable. This model computes similarity scores between the input images and text; it does not generate images or text. Rankings may place irrelevant items high, or miss relevant ones, for rare or unseen categories.
Use Case Restrictions:                              |  Abide by NVIDIA Open Model License Agreement
Model and dataset restrictions:            |  The Principle of least privilege (PoLP) is applied limiting access for dataset generation and model development.  Restrictions enforce dataset access during training, and dataset license constraints adhered to.
