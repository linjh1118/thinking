---
license: other
license_name: openmdw-1.1
license_link: https://openmdw.ai/license/1-1/
base_model: nvidia/Nemotron-3.5-Embed-1B-BF16
tags:
  - multimodal-embedding
  - image-embeddings
  - text-embeddings
  - retrieval
  - rag
  - semantic-search
  - transformers
  - vllm
language:
  - multilingual
library_name: vllm
pipeline_tag: visual-document-retrieval
---

<div align="center">

**NVIDIA Nemotron 3.5 Embed**

<a href="https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16">
  <img alt="Nemotron 3.5 Embed 1B BF16" src="https://img.shields.io/badge/1B-BF16-76B900?style=for-the-badge&logo=nvidia&logoColor=white">
</a>
&nbsp;
<a href="https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-NVFP4">
  <img alt="Nemotron 3.5 Embed 1B NVFP4" src="https://img.shields.io/badge/1B-NVFP4-76B900?style=for-the-badge&logo=nvidia&logoColor=white">
</a>
&nbsp;
<a href="https://huggingface.co/nvidia/Nemotron-3.5-Embed-8B-BF16">
  <img alt="Nemotron 3.5 Embed 8B BF16" src="https://img.shields.io/badge/8B-BF16-76B900?style=for-the-badge&logo=nvidia&logoColor=white">
</a>

</div>

# Nemotron-3.5-Embed-1B-NVFP4 Overview

## Description:  

**Nemotron-3.5-Embed-1B-NVFP4** is the quantized version of the [Nemotron-3.5-Embed-1B-BF16](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16) model, developed for multimodal and multilingual question-answering retrieval. The model can embed document pages in the form of image, text, or combined image–text inputs. Documents can be retrieved given a user query in text form. The model supports page images containing text, tables, charts, and infographics. The model is quantized with NVIDIA Model Optimizer, using nvidia-modelopt v0.47.0.
For text retrieval, the model was evaluated across 34 languages: English, Arabic, Assamese, Bengali, Bulgarian, Chinese, Danish, Dutch, Finnish, French, German, Hindi, Hinglish, Indonesian, Italian, Japanese, Korean, Malay, Marathi, Nepali, Norwegian, Persian, Portuguese, Romanian, Russian, Spanish, Swahili, Swedish, Tamil, Telugu, Thai, Ukrainian, Urdu, and Vietnamese. For image retrieval, it was evaluated across 18 languages: Arabic, Bengali, Chinese, English, Persian, Finnish, French, German, Hindi, Indonesian, Japanese, Korean, Russian, Spanish, Swahili, Telugu, Thai, and Yoruba. The model may support additional languages beyond these evaluation sets.

This model is ready for commercial or non-commercial use.


### License/Terms of Use:

**Governing Download Terms:** Use of the model is governed by the [OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1/). <br>
**Additional Information:** The [Ministral-3-3B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512-BF16) and [Ministral-3-8B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-BF16) base models are governed by the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).


### Deployment Geography:
Global

### Use Case:  
The **Nemotron-3.5-Embed-1B-NVFP4** is suitable for users who want to build a multimodal question-and-answer application over a large corpus, leveraging the latest dense retrieval technology. For more details refer to [here](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16).

Generally **Nemotron-3.5-Embed-1B-BF16** and **Nemotron-3.5-Embed-1B-NVFP4** models share the embedding space and can be used interchangeably, but we recommend validating retrieval quality on a representative sample before switching the models.

### Release Date:

Hugging Face 10/20/2026 via https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-NVFP4

## Model Architecture:
**Architecture Type:** Transformer <br>
**Network Architecture:** [Ministral-3-8B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-BF16)-based distilled vision encoder, and a language model initialized from [nvidia/Nemotron-3-Embed-1B-BF16](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16). <br>
**Number of model parameters:** 1.55B

The `Nemotron-3.5-Embed-1B-NVFP4` is the quantized version of the `Nemotron-3.5-Embed-1B-BF16`, which is a transformer-based multimodal embedding model distilled from a fine-tuned `Nemotron-3.5-Embed-8B-BF16` teacher model. 

For distribution, the NVFP4 checkpoint was converted to the compressed-tensors format. NVFP4 quantization is applied to eligible linear layers in both the language model and the vision encoder. The final embedding vector is obtained by applying average pooling to the transformer’s token-level representations. It encodes each input (image, text, or image + text) into a dense embedding vector of dimension 2048.

#### Post-Training Quantization and Quantization-Aware Distillation
This model is a post-training quantized variant of `Nemotron-3.5-Embed-1B-BF16`. Quantization was applied to the weights and activations of linear layers only, targeting the NVFP4 data type for efficient inference. Quantization-Aware Distillation (QAD) was applied primarily to recover accuracy for long input sequences.

## Input:  
**Input Type(s):** Text, Image <br>
**Input Format(s):** Text: String; Image: Red, Green, Blue (RGB) <br>
**Input Parameters:** Text: One-Dimensional (1D), Image: Two-Dimensional (2D) <br>
**Other Properties Related to Input:** The model supports image and/or text inputs. For queries, the model accepts text input only. For documents, it accepts an image, text, or a combination of image + text. The default image longest_edge is 1,120 pixels, and it can be increased up to 1,540 pixels. The model’s max context length is 32,768 pixels.

## Output:  
**Output Type(s):** Embeddings  
**Output Format:** Vector <br>
**Output Parameters:** One-Dimensional (1D) per input <br>
**Other Properties Related to Output:** Token-level hidden states are mean-pooled and then L2-normalized to produce one 2048-dimensional embedding vector for each input. The model also supports dynamic embedding sizes by truncating the vector from the end (e.g., retaining the first 1024 or 512 dimensions). The truncated embeddings remain effective for retrieval, provided they are L2-normalized after truncation.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.


## vLLM Usage

This NVFP4 checkpoint is intended for vLLM. This checkpoint requires hardware with NVFP4 support, such as NVIDIA Blackwell GPUs. The examples below show offline Python use and online serving. Use `nvidia/Nemotron-3.5-Embed-1B-BF16` if you need Transformers or Sentence Transformers.

### Dependencies

Create a Python environment and install the dependencies. Set `MODEL_PATH` to the Hugging Face model ID by default. If you are working from a local checkpoint, replace `MODEL_PATH` with that path:

```bash
uv venv --python 3.12 .venv-vllm
source .venv-vllm/bin/activate
uv pip install "vllm==0.32.0" "transformers==5.19.0" pillow httpx numpy
export MODEL_PATH="nvidia/Nemotron-3.5-Embed-1B-NVFP4"
```

This checkpoint requires Transformers 5.17.0 or later for its Pixtral rotary embedding configuration. vLLM 0.32.0 requires `transformers>=5.16.1,<5.20.0`. The versions above were tested together with this checkpoint.

**Tested vLLM Versions:**
This checkpoint has been explicitly tested with the following vLLM distributions:

| Distribution | Tested version |
| --- | --- |
| Python package | `vllm==0.32.0` |
| Upstream container | `vllm/vllm-openai:v0.32.0` |

The examples enable `compile_mm_encoder` to compile the Pixtral image encoder.

### vLLM Offline Python

Use `query:` for text queries and `passage:` for documents. Format each input
with the model's chat template and pass images through `multi_modal_data`:

```python
import os

import numpy as np
from transformers import AutoProcessor
from transformers.image_utils import load_image
from vllm import LLM
from vllm.config import PoolerConfig

MODEL_PATH = os.environ["MODEL_PATH"]
DOCUMENT_NAMES = ["nemo_image_text", "nemo_text", "nemo_image", "biology_text"]
IMAGE_URL = "https://docs.nvidia.com/nemo-framework/user-guide/24.07/_images/nemo-llm-mm-stack.png"
MAX_MODEL_LEN = 32768


def main() -> None:
    processor = AutoProcessor.from_pretrained(MODEL_PATH)
    model = LLM(
        model=MODEL_PATH,
        compilation_config={"compile_mm_encoder": True},
        pooler_config=PoolerConfig(
            task="embed",
            pooling_type="MEAN",
            use_activation=True,
        ),
        max_model_len=MAX_MODEL_LEN,
    )
    image = load_image(IMAGE_URL)
    nemo_text = "NeMo Framework offers comprehensive functionalities for developing both LLMs and Multimodal Models."
    biology_text = "A biological foundation model designed to analyze and generate DNA, RNA, and protein sequences."
    samples = [
        ("query:", "What is NVIDIA NeMo Framework?", None),
        ("passage:", nemo_text, image),
        ("passage:", nemo_text, None),
        ("passage:", None, image),
        ("passage:", biology_text, None),
    ]
    prompts = []
    for prefix, text, image in samples:
        content = [] if image is None else [{"type": "image", "image": image}]
        if text is not None:
            content.append({"type": "text", "text": text})
        conversation = [
            {"role": "system", "content": prefix},
            {"role": "user", "content": content},
        ]
        prompt = {"prompt": processor.apply_chat_template(conversation, tokenize=False)}
        if image is not None:
            prompt["multi_modal_data"] = {"image": image}
        prompts.append(prompt)

    # Preserve the template output without adding BOS/EOS tokens.
    outputs = model.embed(prompts, tokenization_kwargs={"add_special_tokens": False})
    embeddings = np.asarray([result.outputs.embedding for result in outputs], dtype=np.float32)
    query_embedding, document_embeddings = embeddings[:1], embeddings[1:]
    scores = query_embedding @ document_embeddings.T
    print(f"query_embedding.shape={query_embedding.shape}")
    print(f"document_embeddings.shape={document_embeddings.shape}")
    for name, score in zip(DOCUMENT_NAMES, scores[0]):
        print(f"{name}_similarity={score:.6f}")


if __name__ == "__main__":
    main()
```

Example output (scores can vary with hardware and runtime):
```text
query_embedding.shape=(1, 2048)
document_embeddings.shape=(4, 2048)
nemo_image_text_similarity=0.518269
nemo_text_similarity=0.466552
nemo_image_similarity=0.497254
biology_text_similarity=0.104270
```

### vLLM Online Serving

vLLM reads the checkpoint’s NVFP4 metadata automatically.

Start a local embedding server with persistent caching and a sparse CUDA graph profile using Bash or Zsh. Set `VLLM_CACHE_ROOT` to a writable directory that persists across restarts so vLLM can reuse compatible compilation and FP4 GEMM autotuning artifacts:

```bash
export VLLM_CACHE_ROOT=/mnt/vllm-cache
mkdir -p "$VLLM_CACHE_ROOT"

vllm serve "$MODEL_PATH" \
    --served-model-name "nvidia/Nemotron-3.5-Embed-1B-NVFP4" \
    --max-model-len 32768 \
    --compilation-config '{"compile_mm_encoder":true}' \
    --host 127.0.0.1 \
    --port 8000 \
    --chat-template-content-format openai \
    --cudagraph-capture-sizes \
        1 2 4 {8..248..8} {256..4096..16} \
        {4224..8192..128} {8448..16384..256} \
        {16896..32768..512}
```

The example uses `/mnt/vllm-cache`, but you can use any writable directory that persists across restarts. For container deployments, mount persistent storage at the directory you choose. Bash and Zsh expand the capture-size ranges before vLLM starts. For other launchers, pass the expanded integer list to `--cudagraph-capture-sizes`.

The sparse CUDA graph profile is a practical starting point. Benchmark representative traffic before changing it or increasing `--api-server-count`. For other cache or tuning configurations, refer to the vLLM [VLLM_CACHE_ROOT reference](https://docs.vllm.ai/en/v0.32.0/usage/security/#cache-directory-configuration), [--cudagraph-capture-sizes reference](https://docs.vllm.ai/en/v0.32.0/configuration/engine_args/#-cudagraph-capture-sizes), and [Parallel Processing guide](https://docs.vllm.ai/en/v0.32.0/configuration/optimization/#parallel-processing).

Expect the first startup to take several minutes while vLLM tunes FP4 GEMMs and captures CUDA graphs. vLLM recaptures CUDA graphs on every launch. Startup time varies by hardware and deployment configuration.

Change `--host` or `--port` if you need different network settings.

After the server is ready, open another terminal in the same directory and activate the vLLM environment:

```bash
source .venv-vllm/bin/activate
```

Run the following Python client to send the query and a batch of four documents to `/v2/embed`. `input_type` selects the query or document prefix from the checkpoint. The client sets `truncate="END"` to truncate text from the end. If image tokens alone exceed the context limit, reduce the image resolution.

```python
import httpx
import numpy as np

MODEL_ID = "nvidia/Nemotron-3.5-Embed-1B-NVFP4"
ENDPOINT = "http://127.0.0.1:8000/v2/embed"
IMAGE_URL = "https://docs.nvidia.com/nemo-framework/user-guide/24.07/_images/nemo-llm-mm-stack.png"
DOCUMENT_NAMES = ["nemo_image_text", "nemo_text", "nemo_image", "biology_text"]


def embed(client: httpx.Client, input_type: str, inputs: list[dict]) -> np.ndarray:
    response = client.post(
        ENDPOINT,
        json={
            "model": MODEL_ID,
            "input_type": input_type,
            "inputs": inputs,
            "embedding_types": ["float"],
            "truncate": "END",
        },
    )
    response.raise_for_status()
    return np.asarray(response.json()["embeddings"]["float"], dtype=np.float32)


def main() -> None:
    query = "What is NVIDIA NeMo Framework?"
    nemo_text = "NeMo Framework offers comprehensive functionalities for developing both LLMs and Multimodal Models."
    biology_text = "A biological foundation model designed to analyze and generate DNA, RNA, and protein sequences."
    image_block = {"type": "image_url", "image_url": {"url": IMAGE_URL}}
    documents = [
        {"content": [image_block, {"type": "text", "text": nemo_text}]},
        {"content": [{"type": "text", "text": nemo_text}]},
        {"content": [image_block]},
        {"content": [{"type": "text", "text": biology_text}]},
    ]
    with httpx.Client(timeout=120.0) as client:
        query_embedding = embed(client, "query", [{"content": [{"type": "text", "text": query}]}])[0]
        document_embeddings = embed(client, "document", documents)

    for name, score in zip(DOCUMENT_NAMES, query_embedding @ document_embeddings.T):
        print(f"{name}_similarity={score:.6f}")


if __name__ == "__main__":
    main()
```

Example output (scores can vary with hardware and runtime):

```text
nemo_image_text_similarity=0.518269
nemo_text_similarity=0.466552
nemo_image_similarity=0.497254
biology_text_similarity=0.104270
```

### Expected Configuration Warning

When loading this checkpoint, Transformers can emit the following warning:

```text
[transformers] Unrecognized keys in `rope_parameters` for 'rope_type'='yarn': {'apply_yarn_scaling'}
```

This warning does not prevent model loading or inference. No checkpoint configuration edit is required.

## Software Integration:
**Runtime Engine(s):**
* vLLM


**Supported Hardware Microarchitecture Compatibility:**
* NVIDIA Blackwell

**Supported Operating System(s):** Linux  

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.  


## Model Version(s):
**Nemotron-3.5-Embed-1B-NVFP4**


## Training, Testing, and Evaluation Datasets:


### Training Dataset:

**Data Modality:**
* Image  
* Text  


**Image Training Data Size:** 49k samples <br>
**Text Training Data Size:** 49k samples <br>
**Data Collection Method by dataset:** Automated, Manually-Labeled, Synthetic <br>
**Labeling Method by dataset:** Automated, Manually-Labeled, Synthetic <br>
**Properties:** This checkpoint is an NVFP4 post-training-quantized derivative of [nvidia/Nemotron-3.5-Embed-1B-BF16](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16). NVFP4 quantization and Quantization-Aware Distillation (QAD) used a 49k-sample subset of the training data, selected to cover typical cases and tail cases, and containing both images and text. Of these samples, initial post-training quantization calibration used 384 samples: 128 images, 128 short texts, and 128 long texts. Initial QAD of the vision encoder used 5,120 randomly sampled images. Later text and image+text QAD stages used the full 49k-sample subset, with 5% held out for validation.

`Nemotron-3.5-Embed-1B-BF16's` training was conducted using publicly available, commercially permissible datasets and synthetically generated datasets. For more detail about the text and image datasets used for training please refer to the [BF16 model card](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16).


### Testing Dataset:

**Data Collection Method by dataset:** Not Applicable <br>
**Labeling Method by dataset:** Not Applicable <br>
**Properties:** Not Applicable. Model quality was assessed using the evaluation benchmark datasets described in the Evaluation Dataset subsection.

### Evaluation Dataset:
**Benchmark**:
- [ViDoRe V3](https://huggingface.co/blog/QuentinJG/introducing-vidore-v3) <br>

**Benchmark Score:** NDCG@10 <br>

Both **Nemotron-3.5-Embed-1B-BF16** and **Nemotron-3.5-Embed-1B-NVFP4** were evaluated with the models' default image `longest_edge` of 1,120 pixels.

<table>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Precision</th>
    <th colspan="3" style="text-align: center;">ViDoRe V3</th>
  </tr>
  <tr>
    <th>image</th>
    <th>text</th>
    <th>image + text</th>
  </tr>
  <tr>
    <td>Nemotron-3.5-Embed-1B-BF16</td>
    <td>BF16</td>
    <td>58.02</td>
    <td>57.80</td>
    <td>58.82</td>
  </tr>
  <tr>
    <td>Nemotron-3.5-Embed-1B-NVFP4</td>
    <td>NVFP4</td>
    <td>57.82</td>
    <td>57.53</td>
    <td>58.71</td>
  </tr>
</table>



**Data Collection Method by dataset:** Automated, Manually-Labeled, Synthetic 
**Labeling Method by dataset:** Automated, Manually-Labeled, Synthetic  
**Properties:** `ViDoRe V3` is a visual document retrieval benchmark covering 8 public and 2 private datasets across professional domains.


## Inference:
**Acceleration Engine:** vLLM <br>
**Hardware Requirements (GPU Architecture, Model):**
* NVIDIA Blackwell (GB200 186GB)

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.  
Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.  
For more detailed information on ethical considerations for this model, please see the [Bias](#bias), [Explainability](#explainability), [Privacy](#privacy), and [Safety & Security](#safety) Subcards.  
Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Bias

| Field | Response |
| ----- | ----- |
| Participation considerations from adversely impacted groups [protected classes](https://calcivilrights.ca.gov/disputeresolution/protected-characteristics/) in model design and testing: | None |
| Measures taken to mitigate against unwanted bias: | None |
| Bias Metric (If Measured): | Not Applicable |

## Explainability

| Field | Response |
| ----- | ----- |
| Intended Task/Domain: | Document and query embedding for question and answer retrieval. |
| Model Type: | Transformer encoder |
| Intended Users: | Generative AI creators working with conversational AI models - users who want to build a multilingual and multimodal question and answer application over a large document corpus, leveraging the latest dense retrieval technologies. |
| Output: | Array of float numbers (Dense Vector Representation for the input text or image) |
| Describe how the model works: | Model transforms the tokenized input into a dense vector representation. |
| List the groups (or group characteristics) for which this was tested to produce comparable outcomes: | Not Applicable |
| Technical Limitations & Mitigation: | The model’s max sequence length is 32768. Therefore, the longer inputs should be truncated. |
| Verified to have met prescribed NVIDIA quality standards: | Yes |
| Performance Metrics: | Accuracy, Latency and Throughput|
| Potential Known Risks: | This model does not always guarantee to retrieve the correct document(s) for a given query. |
| Licensing: | Use of the model is governed by the [OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1/). Additional Information: The [Ministral-3-3B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512-BF16) and [Ministral-3-8B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-BF16) base models are governed by the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt). |

## Privacy

The datasets used to train this model were reviewed before release. Please review NVIDIA’s Privacy Policy (https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

## Safety

| Field | Response |
| ----- | ----- |
| Model Application Field(s): | Document Embedding for Retrieval. User queries can be text and documents can be text, document page images, charts, tables, and infographics. |
| Describe the life critical impact (if present). | Not Applicable |
| Use Case Restrictions: | Use of the model is governed by the [OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1/). Additional Information: The [Ministral-3-3B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512-BF16) and [Ministral-3-8B-Instruct-2512-BF16](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-BF16) base models are governed by the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).|
| Model and dataset restrictions: | The Principle of least privilege (PoLP) is applied limiting access for dataset generation and model development. Restrictions enforce dataset access during training, and dataset license constraints adhered to. |
