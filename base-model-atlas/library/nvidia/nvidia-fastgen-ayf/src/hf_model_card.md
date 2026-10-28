---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
language:
- en
base_model:
- black-forest-labs/FLUX.1-dev
- Qwen/Qwen-Image
pipeline_tag: text-to-image
tags:
- nvidia
- distillation
- few-step-generation
- text-to-image
- image-generation
- fastgen
---


# **Align Your Flow: Scaling Continuous-Time Flow Map Distillation**
**[Paper](https://arxiv.org/abs/2506.14603)** | **[Code](https://github.com/NVlabs/fastgen)** | **[Project Page](https://research.nvidia.com/labs/toronto-ai/AlignYourFlow/)**

![](assets/banner.jpg)

# Introduction

Align Your Flow (AYF) distills pretrained diffusion or flow-matching models into few-step flow map generators that can map between arbitrary noise levels in a single step, enabling fast high-quality image synthesis across different step counts. 
AYF models are trained as LoRAs applied to existing text-to-image models. We leveraged [FLUX.1 [dev]](https://huggingface.co/black-forest-labs/FLUX.1-dev) and [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) as base models and performed fine-tuning using lightweight LoRA adapters. This release comprises the LoRA adapters only.

This model is ready for commercial/non-commercial use. <br>

**Model Developer:** NVIDIA

### Model Versions

- AYF-FLUX (`flux.1-dev/model.pth`): LoRA adapter over [FLUX.1 [dev]](https://huggingface.co/black-forest-labs/FLUX.1-dev) for few-step (4-8) text-to-image generation.
- AYF-Qwen-Image (`qwen-image/model.pth`): LoRA adapter over [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) for few-step (4-8) text-to-image generation.

## Quickstart

Install [FastGen](https://github.com/NVlabs/fastgen) and run its inference script with a checkpoint from this repository:

```bash
# FLUX.1 [dev]
torchrun --standalone --nproc_per_node=1 \
    scripts/inference/image_model_inference.py \
    --config fastgen/configs/experiments/Flux/config_ayf.py \
    --ckpt_path FastGen-AYF/flux.1-dev/model.pth \
    --do_student_sampling True \
    --prompt_file scripts/inference/prompts/image_prompts.txt

# Qwen-Image
torchrun --standalone --nproc_per_node=1 \
    scripts/inference/image_model_inference.py \
    --config fastgen/configs/experiments/QwenImage/config_ayf.py \
    --ckpt_path FastGen-AYF/qwen-image/model.pth \
    --do_student_sampling True \
    --prompt_file scripts/inference/prompts/image_prompts.txt
```

### License/Terms of Use

GOVERNING TERMS: Use of the Align Your Flow model is governed by the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).<br>

Use of the software components is governed by [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).<br>

Use of third-party models with Align Your Flow is subject to third party model terms and conditions. You are responsible for reviewing and complying with applicable-third party model terms.

### Deployment Geography

Global

### Use Case

This model is intended for users interested in fast, high-quality text-to-image generation. It enables few-step sampling for interactive creative workflows and low-latency deployment, where users iterate quickly on prompts while retaining strong image quality. <br>

### Release Date

Hugging Face [27/08/2026] via [https://huggingface.co/nvidia/FastGen-AYF](https://huggingface.co/nvidia/FastGen-AYF)

## Model Architecture

**Architecture Type:** Transformer <br>
**Network Architecture:** Multimodal Diffusion Transformer (MMDiT) <br>

**This model was developed based on [FLUX.1 [dev]](https://huggingface.co/black-forest-labs/FLUX.1-dev) and [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) <br> 

**Number of Model Parameters:** 357M (FLUX), 445M (Qwen-Image) <br>

## Input(s)

**Input Type(s):** Text <br>

**Input Format(s):** Text: String <br>

**Input Parameters:** Text: One-dimensional (1D) <br>

**Other Properties Related to Input**: The FLUX-based model uses CLIP and T5 text encoders which can handle up to 512 tokens. The Qwen-Image-based model uses a Qwen2.5-VL text encoder that can handle arbitrarily long inputs.

## Output(s)

**Output Type(s):** Image <br>

**Output Format(s):** Image: Red, Green, Blue (RGB) <br>

**Output Parameters:** Image: Two-Dimensional (2D), with 3 channel (Red, Green, Blue) <br>

**Other Properties Related to Output:** The model was primarily fine-tuned at 256x256, 512×512, and 1024×1024 resolutions, where it performs best, though other resolutions may also work. 

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems **A100**. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration

**Runtime Engine(s):** 
* PyTorch, FastGen <br>

**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Ampere <br>
* NVIDIA Blackwell <br>
* NVIDIA Hopper <br>

**Supported Operating System(s):**
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment. <br>

## Model Version(s)

- V1.0

## Training, Testing, and Evaluation Datasets

### Training Dataset:

We use the public [text-to-image-2M](https://huggingface.co/datasets/jackyhate/text-to-image-2M) for training. 

- **Data Modality:** Image, Text <br>

- **Image Training Data Size:** Approximately 2 Million Images <br>

- **Text Training Data Size:** Less than a Billion Tokens <br>

- **Data Collection Method by dataset:** Hybrid: Automated, Automatic/Sensors, Synthetic, Human <br>

- **Labeling Method by dataset:** Hybrid: Automated, Automatic/Sensors, Synthetic, Human  <br>

- **Properties:** The dataset consists of approximately 2M image-text pairs which are a mixture of synthetically generated images and real images with synthetic captions. <br>

- **Preprocessing:** Images were cropped and resized to the target training resolutions of 256×256, 512×512, and 1024×1024.

### Testing Dataset: 

We used a subset of the training data for testing and validation.

- **Data Collection Method by dataset:** Hybrid: Automated, Automatic/Sensors, Synthetic, Human <br>

- **Labeling Method by dataset:** Hybrid: Automated, Automatic/Sensors, Synthetic, Human  <br>

- **Properties:** The testing dataset is approximately a 10% split of the training dataset. <br>


## Key Considerations

AYF models are trained as LoRA (Low-Rank Adaptation) extensions applied to existing text-to-image architectures. For this release, we fine-tuned [FLUX.1 \[dev\]](https://huggingface.co/black-forest-labs/FLUX.1-dev)  and [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) using lightweight LoRA adapters. This release includes only the LoRA adapters, not the underlying base models.

Please note that the base models, when used independently, can generate synthetic images and may produce content that is inaccurate, offensive, or otherwise inappropriate. Users should implement robust safety guardrails—including content filtering, abuse monitoring, and access controls—to reduce the risk of harmful outputs. Users are responsible for ensuring that their use of the model complies with all applicable laws and regulations, and for reviewing and updating their guardrails as risks evolve.

## Inference

**Acceleration Engine:** N/A <br>
**Test Hardware:** NVIDIA A100 GPUs <br>

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse. <br> 

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included. <br> 

For more detailed information on ethical considerations for this model, please see the Model Card++ Bias, Explainability, Safety & Security, and Privacy Subcards.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment. <br> 

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

---

# Model Card++ Subcards

### Bias

Field                                                                                               |  Response
:---------------------------------------------------------------------------------------------------|:---------------
Participation considerations from adversely impacted groups [protected classes](https://www.senate.ca.gov/content/protected-classes) in model design and testing:  |  None
Measures taken to mitigate against unwanted bias:                                                   |  None


### Explainability

Field                                                                                                  |  Response
:------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------
Intended Task/Domain:                                                                   |  Text-to-Image Generation
Model Type:                                                                                            |  Multimodal Diffusion Transformer (MMDiT)
Intended Users:                                                                                        |  Generative AI creators working with image content.
Output:                                                                                                |  Images
Describe how the model works:                                                                          |  The text input is encoded into tokens and is concatenated with random Gaussian noise before being passed into the transformer-based diffusion model that gradually denoises it into a clean image in 2-4 steps.
Name the adversely impacted groups this has been tested to deliver comparable outcomes regardless of:  |  Not Applicable
Technical Limitations & Mitigation:                                                                    |  While the model is trained to perform well for standard text inputs given 2-4 steps, it may not work well with out-of-distribution text prompts and may generate blurry outputs if used with only a single step.
Verified to have met prescribed NVIDIA quality standards:  |  Yes
Performance Metrics:                                                                                   |  Prompt Adherence (Compositional Image Generation), Image Quality, Latency, Visual Inspection
Potential Known Risks:                                                                                 |  The generated image may appear blurred and may contain unrealistic artifacts. The generated image may not fully adhere to the given prompt. <br> This model can generate synthetic images and may produce content that is inaccurate, offensive, or otherwise inappropriate. Users should implement robust safety guardrails—including content filtering, abuse monitoring, and access controls—to reduce the risk of harmful outputs. Users are responsible for ensuring that their use of the model complies with all applicable laws and regulations, and for reviewing and updating their guardrails as risks evolve.
Licensing:                                                                                             |  GOVERNING TERMS: Use of the Align Your Flow model is governed by the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/). Use of the software components is governed by [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Use of third-party models with Align Your Flow is subject to third party model terms and conditions. You are responsible for reviewing and complying with applicable-third party model terms.


### Privacy

Field                                                                                                                              |  Response
:----------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------
Generatable or reverse engineerable personal data?                                                                                 |  Yes
Personal data used to create this model?                                                                                           |  Yes
Was consent obtained for any personal data used?                                                                                   |  Unknown (Externally-Sourced Data)
Is a mechanism in place to honor data subject right of access or deletion of personal data?                                        |  Unknown (Externally-Sourced Data)
If personal data was collected for the development of the model, was it collected directly by NVIDIA?                              |  No
If personal data was collected for the development of the model by NVIDIA, do you maintain or have access to disclosures made to data subjects?  |  Not Applicable
If personal data was collected for the development of this AI model, was it minimized to only what was required?                   |  Yes
How often is dataset reviewed?                                                                                                     |  Before Release
Was data from user interactions with the AI model (e.g. user input and prompts) used to train the model?                           |  No
Is there provenance for all datasets used in training?                                                                             |  Yes
Does data labeling (annotation, metadata) comply with privacy laws?                                                                |  Yes
Is data compliant with data subject requests for data correction or removal, if such a request was made?                           |  No, not possible with externally sourced data
Applicable Privacy Policy        | https://www.nvidia.com/en-us/about-nvidia/privacy-policy/ 



### Safety & Security

Field                                               |  Response
:---------------------------------------------------|:----------------------------------
Model Application Field(s):                               |  Media & Entertainment
Describe the life critical impact (if present).   |  Not Applicable 
Use Case Restrictions:                              |  Abide by [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/). Use of the software components is governed by [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Use of third-party models with Align Your Flow is subject to third party model terms and conditions. You are responsible for reviewing and complying with applicable-third party model terms.
Model and dataset restrictions:            |  The Principle of least privilege (PoLP) is applied limiting access for dataset generation and model development.  Restrictions enforce dataset access during training, and dataset license constraints adhered to.
