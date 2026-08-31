---
license: mit
license_name: deepseek
license_link: LICENSE
pipeline_tag: any-to-any
library_name: transformers
tags:
- muiltimodal
- text-to-image
- unified-model
---

## 0. Update
**2024.10.20**: We have uploaded the correct `tokenizer_config.json`. The previous file was missing the `pad_token`, which caused poor visual generation results.


## 1. Introduction

Janus is a novel autoregressive framework that unifies multimodal understanding and generation. 
It addresses the limitations of previous approaches by decoupling visual encoding into separate pathways, while still utilizing a single, unified transformer architecture for processing. The decoupling not only alleviates the conflict between the visual encoder’s roles in understanding and generation, but also enhances the framework’s flexibility. 
Janus surpasses previous unified model and matches or exceeds the performance of task-specific models. 
The simplicity, high flexibility, and effectiveness of Janus make it a strong candidate for next-generation unified multimodal models.

[Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation](https://arxiv.org/abs/2410.13848)

[**Github Repository**](https://github.com/deepseek-ai/Janus)

<div align="center">
<img alt="image" src="teaser.png" style="width:90%;">
</div>


### 2. Model Summary

Janus is a unified understanding and generation MLLM, which decouples visual encoding for multimodal understanding and generation. 
Janus is constructed based on the DeepSeek-LLM-1.3b-base which is trained on an approximate corpus of 500B text tokens.
For multimodal understanding, it uses the [SigLIP-L](https://huggingface.co/timm/ViT-L-16-SigLIP-384) as the vision encoder, which supports 384 x 384 image input. For image generation, Janus uses the tokenizer from [here](https://github.com/FoundationVision/LlamaGen) with a downsample rate of 16.

<div align="center">
<img alt="image" src="arch.jpg" style="width:90%;">
</div>

## 3. Quick Start

Please refer to [**Github Repository**](https://github.com/deepseek-ai/Janus)


## 4. License

This code repository is licensed under [the MIT License](https://github.com/deepseek-ai/DeepSeek-LLM/blob/HEAD/LICENSE-CODE). The use of Janus models is subject to [DeepSeek Model License](https://github.com/deepseek-ai/DeepSeek-LLM/blob/HEAD/LICENSE-MODEL).
## 5. Citation

```
@misc{wu2024janus,
      title={Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation}, 
      author={Chengyue Wu and Xiaokang Chen and Zhiyu Wu and Yiyang Ma and Xingchao Liu and Zizheng Pan and Wen Liu and Zhenda Xie and Xingkai Yu and Chong Ruan and Ping Luo},
      year={2024},
      eprint={2410.13848},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2410.13848}, 
}
```

## 6. Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](mailto:service@deepseek.com).