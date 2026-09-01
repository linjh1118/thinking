#!/usr/bin/env python3
"""Build the BrainHao base-model atlas and sync publishable notes/posters.

The atlas is intentionally data-driven: curated family timelines establish the
editorial scope, while existing BrainHao notes and posters are discovered and
linked automatically. Generated BrainHao additions are limited to teams that
were missing entirely (plus current flagship gaps) and never overwrite files.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote


THINKING = Path(__file__).resolve().parents[1]
BRAINHAO = Path("/Users/omegalin/Documents/github/BrainHao")
SOURCE = BRAINHAO / "Topics/13_base_model"
ATLAS = THINKING / "base-model-atlas"
LIBRARY = ATLAS / "library"


TEAMS = [
    {"id":"openai","dir":"OpenAI","name":"OpenAI · GPT","region":"海外","color":"#7cf2c8","thesis":"从通用 next-token scaling 走向统一 reasoning、工具调用与专业工作基座。","models":[
        ["1806","GPT-1","生成式预训练证明统一语言建模可迁移。","https://openai.com/index/language-unsupervised/"],
        ["1902","GPT-2","规模、WebText 与 zero-shot 能力开始联动。","https://openai.com/index/better-language-models/"],
        ["2005","GPT-3","few-shot prompting 成为通用接口。","https://arxiv.org/abs/2005.14165"],
        ["2211","GPT-3.5","指令对齐与对话产品化形成规模效应。","https://openai.com/index/chatgpt/"],
        ["2303","GPT-4","多模态与高可靠复杂任务能力跃迁。","https://openai.com/research/gpt-4"],
        ["2311","GPT-4 Turbo","128K context、更新知识截止时间与更低 API 成本。","https://openai.com/index/new-models-and-developer-products-announced-at-devday/"],
        ["2405","GPT-4o","原生 omni 交互与低时延统一。","https://openai.com/index/hello-gpt-4o/"],
        ["2502","GPT-4.5","以更大规模预训练提升世界知识、模式识别与自然交互。","https://openai.com/index/introducing-gpt-4-5/"],
        ["2504","GPT-4.1","1M context，并强化 coding、instruction following 与长上下文。","https://openai.com/index/gpt-4-1/"],
        ["2508","GPT-5","reasoning、fast path 与工具能力统一。","https://developers.openai.com/api/docs/models/gpt-5"],
        ["2511","GPT-5.1","强化 coding 与 agentic task。","https://developers.openai.com/api/docs/models/gpt-5.1"],
        ["2512","GPT-5.2","面向专业工作的可配置推理旗舰。","https://developers.openai.com/api/docs/models/gpt-5.2"],
        ["2603","GPT-5.4","统一 reasoning、coding、工具与专业工作流。","https://developers.openai.com/api/docs/models/gpt-5.4"],
        ["2603","GPT-5.3","ChatGPT Instant 正代更新，强化日常问答、搜索与对话质量。","https://developers.openai.com/api/docs/models/gpt-5.3-chat-latest"],
        ["2604","GPT-5.5","复杂 coding 与专业工作质量上移。","https://developers.openai.com/api/docs/models/gpt-5.5"],
        ["2608","GPT-5.6","Sol / Terra / Luna 分层，正代统一到 1.05M context。","https://developers.openai.com/api/docs/models/gpt-5.6-sol"]]},
    {"id":"anthropic","dir":"Anthropic","name":"Anthropic · Claude","region":"海外","color":"#ffb36b","thesis":"以 Constitutional AI、安全评估和长时程 agentic coding 为主轴。","models":[
        ["2303","Claude 1","Constitutional AI 路线首次产品化。","https://www.anthropic.com/news/introducing-claude"],
        ["2307","Claude 2","长上下文与 coding 能力增强。","https://www.anthropic.com/news/claude-2"],
        ["2311","Claude 2.1","200K context，并降低长文档任务中的错误率。","https://www.anthropic.com/news/claude-2-1"],
        ["2403","Claude 3","Haiku / Sonnet / Opus 能力—成本分层。","https://www.anthropic.com/news/claude-3-family"],
        ["2406","Claude 3.5 Sonnet","coding 与 computer use 成为核心优势。","https://www.anthropic.com/news/claude-3-5-sonnet"],
        ["2502","Claude 3.7 Sonnet","hybrid reasoning 统一快答与 extended thinking。","https://www.anthropic.com/news/claude-3-7-sonnet"],
        ["2505","Claude 4","Opus / Sonnet 进入 agent 与长任务阶段。","https://www.anthropic.com/news/claude-4"],
        ["2508","Claude Opus 4.1","在 agentic tasks、真实 coding 与 reasoning 上更新 Opus 4。","https://www.anthropic.com/system-cards"],
        ["2509","Claude Sonnet 4.5","coding、computer use 与长时程 agent 能力成为 Sonnet 主力。","https://www.anthropic.com/news/claude-sonnet-4-5"],
        ["2511","Claude Opus 4.5","coding、computer use 与自主工作增强。","https://www.anthropic.com/news/claude-opus-4-5"],
        ["2602","Claude Sonnet 4.6","coding、computer use、长上下文与 agent planning 的 Sonnet 升级。","https://www.anthropic.com/news/claude-sonnet-4-6"],
        ["2602","Claude Opus 4.6","1M context 与 agent planning 持续增强。","https://www.anthropic.com/news/claude-opus-4-6"],
        ["2604","Claude Opus 4.7","长时程软件工程与自验证进一步提升。","https://www.anthropic.com/news/claude-opus-4-7"],
        ["2605","Claude Opus 4.8","更可靠的判断、工具效率与诚实性。","https://www.anthropic.com/news/claude-opus-4-8"],
        ["2606","Claude Sonnet 5","把高阶 agent 能力下放到 Sonnet 成本层。","https://www.anthropic.com/news/claude-sonnet-5"],
        ["2607","Claude Opus 5","面向长时程 agents 的 Opus 代际跃迁。","https://www.anthropic.com/news/claude-opus-5"]]},
    {"id":"google","dir":"Google_DeepMind","name":"Google DeepMind · Gemini","region":"海外","color":"#78a8ff","thesis":"原生多模态、超长上下文与推理/工具生态合流。","models":[
        ["2312","Gemini 1.0","Ultra / Pro / Nano 原生多模态分层。","https://deepmind.google/technologies/gemini/"],
        ["2402","Gemini 1.5 Pro","MoE 与百万 token context。","https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/"],
        ["2412","Gemini 2.0","agentic era、原生工具与实时交互。","https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/"],
        ["2503","Gemini 2.5 Pro","thinking model 成为主线。","https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/"],
        ["2511","Gemini 3 Pro","多模态 reasoning 与 agent 工具链升级。","https://deepmind.google/models/gemini/"],
        ["2602","Gemini 3.1 Pro","面向复杂专业任务与长时程 agents。","https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/"],
        ["2605","Gemini 3.5 Flash","3.x 正代在速度、成本与多模态 agent 之间继续扩展。","https://ai.google.dev/gemini-api/docs/models"],
        ["2607","Gemini 3.6 Flash","面向通用 agentic 与多模态任务的 3.x 升级。","https://ai.google.dev/gemini-api/docs/models"],
        ["2608","Gemini 3.7 Flash","当前 3.x 正代，强化 coding、agentic workflow 与可靠多步执行。","https://ai.google.dev/gemini-api/docs/latest-model"]]},
    {"id":"meta","dir":"Meta_Llama","name":"Meta · Llama","region":"海外","color":"#63d5ff","thesis":"开放权重生态从 dense LLM 演进到原生多模态 MoE。","models":[
        ["2302","Llama 1","高质量开放基础模型开启生态。","https://ai.meta.com/blog/large-language-model-llama-meta-ai/"],
        ["2307","Llama 2","开放权重与商业许可扩大采用。","https://ai.meta.com/llama/"],
        ["2404","Llama 3","数据与训练规模显著扩展。","https://ai.meta.com/blog/meta-llama-3/"],
        ["2407","Llama 3.1","405B、长上下文与开放旗舰。","https://ai.meta.com/blog/meta-llama-3-1/"],
        ["2409","Llama 3.2","轻量端侧与视觉模型支线。","https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/"],
        ["2504","Llama 4","Scout / Maverick 原生多模态 MoE。","https://ai.meta.com/blog/llama-4-multimodal-intelligence/"]]},
    {"id":"xai","dir":"xAI_Grok","name":"xAI · Grok","region":"海外","color":"#f2f5ff","thesis":"以超大规模训练、实时搜索和 agentic RL 推动闭源旗舰快速迭代。","models":[
        ["2311","Grok-1","实时 X 数据与通用 reasoning 起点。","https://x.ai/news/grok"],
        ["2403","Grok-1.5","128K context 与 reasoning 增强。","https://x.ai/news/grok-1.5"],
        ["2408","Grok-2","能力、速度与多语言产品化升级。","https://x.ai/news/grok-2"],
        ["2502","Grok-3","大规模预训练叠加 reasoning agents。","https://x.ai/news/grok-3"],
        ["2507","Grok-4","200K GPU 级 RL、原生工具和实时搜索。","https://x.ai/news/grok-4"],
        ["2509","Grok-4 Fast","2M context 与统一 reasoning/non-reasoning。","https://x.ai/news/grok-4-fast"],
        ["2511","Grok-4.1","对话质量与 reasoning 继续上移。","https://x.ai/news/grok-4-1"],
        ["2604","Grok-4.20","高风险能力进入正式 system-card 评估。","https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf"],
        ["2607","Grok-4.5","coding、agentic tasks 与知识工作。","https://x.ai/news/grok-4-5"],
        ["2608","Grok-4.6","长时程 agent 与交互式视觉工作增强。","https://x.ai/news/grok-4-6"]]},
    {"id":"mistral","dir":"Mistral_AI","name":"Mistral AI","region":"海外","color":"#ff7e65","thesis":"欧洲开放模型路线：稀疏 MoE、轻量部署、multimodal 与 agentic coding。","models":[
        ["2309","Mistral 7B","小尺寸开放模型的效率标杆。","https://mistral.ai/news/announcing-mistral-7b"],
        ["2312","Mixtral 8x7B","稀疏 MoE 以较低激活参数提升能力。","https://mistral.ai/news/mixtral-of-experts"],
        ["2402","Mistral Large","首代闭源旗舰进入复杂任务。","https://mistral.ai/news/mistral-large"],
        ["2407","Mistral Large 2","128K、多语言与 function calling。","https://mistral.ai/news/mistral-large-2407"],
        ["2505","Mistral Medium 3","multimodal 与 enterprise cost/performance。","https://mistral.ai/news/mistral-medium-3"],
        ["2508","Mistral Medium 3.1","长任务、同步 tool calling 与 agentic coding。","https://mistral.ai/models/"],
        ["2512","Mistral Large 3","开放权重通用多模态旗舰。","https://mistral.ai/models/"],
        ["2603","Mistral Small 4","统一 reasoning、multimodal 与 agentic coding。","https://mistral.ai/news/mistral-small-4/"]]},
    {"id":"microsoft","dir":"Microsoft","name":"Microsoft · Phi","region":"海外","color":"#5fd6b5","thesis":"用高质量合成数据把复杂 reasoning 压进小模型。","models":[
        ["2306","Phi-1","textbook-quality data 验证小模型 scaling。","https://www.microsoft.com/en-us/research/publication/textbooks-are-all-you-need/"],
        ["2312","Phi-2","2.7B 小模型的数据质量路线。","https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/"],
        ["2404","Phi-3","端侧可部署的小语言模型 family。","https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/"],
        ["2412","Phi-4","14B 模型在 STEM reasoning 超越 teacher。","https://www.microsoft.com/en-us/research/publication/phi-4-technical-report/"],
        ["2507","Phi-4 Reasoning","SFT + RL 的高效复杂推理。","https://www.microsoft.com/en-us/research/articles/phi-reasoning-once-again-redefining-what-is-possible-with-small-and-efficient-ai/"],
        ["2603","Phi-4 Reasoning Vision","15B 混合 reasoning/non-reasoning 多模态模型。","https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/"]]},
    {"id":"amazon","dir":"Amazon_Nova","name":"Amazon · Nova","region":"海外","color":"#ffca63","thesis":"面向 Bedrock 的多尺寸、多模态、企业可部署模型家族。","models":[
        ["2412","Nova 1","Micro / Lite / Pro 覆盖文本到多模态。","https://aws.amazon.com/ai/generative-ai/nova/"],
        ["2504","Nova Premier","Nova 1 家族最高能力层与 teacher 角色。","https://aws.amazon.com/blogs/aws/amazon-nova-premier-our-most-capable-model-for-complex-tasks-and-teacher-for-model-distillation/"],
        ["2512","Nova 2","新一代 reasoning、多模态与 agentic 能力。","https://docs.aws.amazon.com/nova/latest/nova2-userguide/what-is-nova-2.html"]]},
    {"id":"nvidia","dir":"NVIDIA_Nemotron","name":"NVIDIA · Nemotron","region":"海外","color":"#b5e853","thesis":"开放模型 + 数据 + recipe + 推理栈共同服务 enterprise agents。","models":[
        ["2410","Llama 3.1 Nemotron","在 Llama 基座上强化 reasoning 与 agent 能力。","https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct"],
        ["2501","Llama Nemotron","Nano / Super / Ultra agentic family。","https://blogs.nvidia.com/blog/nemotron-model-families/"],
        ["2512","Nemotron 3","从派生 Llama 转向 NVIDIA 自有开放 family。","https://blogs.nvidia.com/blog/nemotron-open-source-ai/"],
        ["2603","Nemotron 3 Super","120B/12B active hybrid MoE，面向 agent 吞吐。","https://blogs.nvidia.com/blog/nemotron-3-super-agentic-ai/"],
        ["2604","Nemotron 3 Nano Omni","30B-A3B omni perception agent。","https://blogs.nvidia.com/blog/nemotron-3-nano-omni-multimodal-ai-agents/"],
        ["2608","Nemotron 3.5 Lightning","30B MoE 服务长时程、多 agent 专项任务。","https://blogs.nvidia.com/blog/nemotron-lightning-switchyard-rtx-dgx/"]]},
    {"id":"cohere","dir":"Cohere","name":"Cohere · Command","region":"海外","color":"#d8a8ff","thesis":"围绕 enterprise RAG、tool use、多语言与私有部署优化。","models":[
        ["2308","Command","企业生成模型与检索增强起点。","https://cohere.com/command"],
        ["2403","Command R","RAG 与 tool use 专用开放权重模型。","https://cohere.com/blog/command-r"],
        ["2404","Command R+","更强 enterprise RAG 与复杂 tool use。","https://cohere.com/blog/command-r-plus-microsoft-azure"],
        ["2503","Command A","111B、256K、双 GPU 私有部署与 agent tasks。","https://cohere.com/blog/command-a"]]},
    {"id":"ibm","dir":"IBM_Granite","name":"IBM · Granite","region":"海外","color":"#93a9ff","thesis":"以透明数据、企业安全、RAG/tool use 和混合 SSM 效率为核心。","models":[
        ["2309","Granite 1","watsonx 企业基础模型起点。","https://www.ibm.com/granite"],
        ["2402","Granite 2","企业语言与代码 family 扩展。","https://www.ibm.com/granite"],
        ["2410","Granite 3.0","Apache 2.0、12T tokens 与 dense/MoE 分层。","https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models"],
        ["2412","Granite 3.1","128K context 与 enterprise workflow 增强。","https://www.ibm.com/new/announcements/granite-3-1-powerful-performance-long-context-and-more"],
        ["2502","Granite 3.2","reasoning 与视觉文档理解。","https://newsroom.ibm.com/2025-02-26-ibm-expands-granite-model-family-with-new-multi-modal-and-reasoning-ai-built-for-the-enterprise"],
        ["2504","Granite 3.3","instruction following、RAG 与工具调用增强。","https://www.ibm.com/new/announcements/ibm-granite-3-3-speech-recognition-refined-reasoning-rag-loras-and-more"],
        ["2510","Granite 4.0","Mamba-2 + Transformer hybrid，面向长上下文效率。","https://www.ibm.com/new/announcements/ibm-granite-4-0-hyper-efficient-high-performance-hybrid-models"]]},
    {"id":"qwen","dir":"Alibaba_Qwen","name":"Alibaba · Qwen","region":"国内","color":"#b991ff","thesis":"统一 thinking/non-thinking，继而走向原生多模态、稀疏高效和 1M context。","models":[
        ["2308","Qwen","通义千问开放权重 family 起点。","https://github.com/QwenLM/Qwen"],
        ["2402","Qwen1.5","多尺寸、MoE 与部署生态扩展。","https://qwenlm.github.io/blog/qwen1.5/"],
        ["2406","Qwen2","多语言、GQA 与长上下文升级。","https://qwenlm.github.io/blog/qwen2/"],
        ["2409","Qwen2.5","大规模 family 与 coder/math 支线成熟。","https://qwenlm.github.io/blog/qwen2.5/"],
        ["2505","Qwen3","thinking/non-thinking 单模型统一。","https://qwenlm.github.io/blog/qwen3/"],
        ["2509","Qwen3-Next","以超稀疏 MoE 和 hybrid attention 预演 Qwen3.5 架构。","https://qwen.ai/blog?id=qwen3-next"],
        ["2602","Qwen3.5","下一代开放模型架构迭代。","https://github.com/QwenLM/Qwen3"],
        ["2604","Qwen3.6","正代 family 的效率与能力升级。","https://github.com/QwenLM/Qwen3"],
        ["2606","Qwen3.7","沿用 hybrid attention 架构并继续推进正代能力。","https://github.com/QwenLM/Qwen3.8-Flash-Next"],
        ["2608","Qwen3.8","原生多模态、1M context 与内置工具。","https://github.com/QwenLM/Qwen3.8"]]},
    {"id":"deepseek","dir":"DeepSeek_AI","name":"DeepSeek AI","region":"国内","color":"#5aa8ff","thesis":"MLA/MoE 训练效率、开放 reasoning RL 与 agentic tool-use 是三条主轴。","models":[
        ["2401","DeepSeek LLM","开放 dense 基模与训练 recipe 起点。","https://huggingface.co/deepseek-ai/deepseek-llm-67b-base"],
        ["2405","DeepSeek-V2","MLA + DeepSeekMoE 显著降低训练/推理成本。","https://huggingface.co/deepseek-ai/DeepSeek-V2"],
        ["2409","DeepSeek-V2.5","通用与 coder 模型合并。","https://huggingface.co/deepseek-ai/DeepSeek-V2.5"],
        ["2412","DeepSeek-V2.5-1210","V2.5 系列最终公开 checkpoint，继续提升数学、代码、写作与角色扮演。","https://huggingface.co/deepseek-ai/DeepSeek-V2.5-1210"],
        ["2412","DeepSeek-V3","671B/37B active、14.8T tokens 与 FP8 训练。","https://huggingface.co/deepseek-ai/DeepSeek-V3"],
        ["2501","DeepSeek-R1","大规模 RL 与极少标注的开放 reasoning 路线。","https://huggingface.co/deepseek-ai/DeepSeek-R1"],
        ["2503","DeepSeek-V3-0324","V3 主部署 checkpoint，显著升级推理、前端、工具调用与中文写作。","https://huggingface.co/deepseek-ai/DeepSeek-V3-0324"],
        ["2505","DeepSeek-R1-0528","R1 主部署 checkpoint，强化深度推理、前端、工具调用并降低幻觉。","https://huggingface.co/deepseek-ai/DeepSeek-R1-0528"],
        ["2508","DeepSeek-V3.1","hybrid inference 与 agent/tool-use 后训练。","https://huggingface.co/deepseek-ai/DeepSeek-V3.1"],
        ["2509","DeepSeek-V3.2-Exp","引入 DeepSeek Sparse Attention，作为下一代架构实验节点。","https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp"],
        ["2509","DeepSeek-V3.1-Terminus","修订 V3.1 的语言一致性、Code Agent 与 Search Agent 表现。","https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus"],
        ["2512","DeepSeek-V3.2","DSA 与 thinking-in-tool-use。","https://huggingface.co/deepseek-ai/DeepSeek-V3.2"],
        ["260424","DeepSeek-V4","V4-Pro / V4-Flash family Preview 首次公开；后续正式 checkpoint 与部署发行物沿同一家族演进。","https://huggingface.co/collections/deepseek-ai/deepseek-v4"]]},
    {"id":"baidu","dir":"Baidu_ERNIE","name":"Baidu · ERNIE","region":"国内","color":"#55d6ce","thesis":"知识增强预训练演进到统一多模态 MoE 与异步 agentic RL。","models":[
        ["1904","ERNIE","entity/phrase masking 注入知识。","https://arxiv.org/abs/1904.09223"],
        ["1907","ERNIE 2.0","continual multi-task pretraining。","https://arxiv.org/abs/1907.12412"],
        ["2107","ERNIE 3.0","统一理解、生成与知识记忆。","https://arxiv.org/abs/2107.02137"],
        ["2310","ERNIE 4.0","理解、生成、推理、记忆全面升级。","https://www.prnewswire.com/news-releases/baidu-unveils-ernie-4-0-301958894.html"],
        ["2503","ERNIE 4.5","heterogeneous multimodal MoE。","https://yiyan.baidu.com/blog/publication/ERNIE_4.5_Technical_Report.pdf"],
        ["2602","ERNIE 5.0","2.4T 统一多模态 autoregressive MoE。","https://arxiv.org/abs/2602.04705"],
        ["2605","ERNIE 5.1","弹性继承与 fully-asynchronous RL。","https://yiyan.baidu.com/blog/posts/ernie5.1"]]},
    {"id":"hunyuan","dir":"Tencent_Hunyuan","name":"Tencent · Hunyuan","region":"国内","color":"#69a9ff","thesis":"腾讯云产品化、MoE 效率、hybrid reasoning 与开放权重并行推进。","models":[
        ["2309","Hunyuan","腾讯通用基模公开发布。","https://www.tencent.com/en-us/articles/2201699.html"],
        ["2405","Hunyuan-Large","大规模 MoE 与长上下文基座。","https://github.com/Tencent/Tencent-Hunyuan-Large"],
        ["2502","Hunyuan-TurboS","Hybrid-Mamba-Transformer 提升长文效率。","https://github.com/Tencent/Hunyuan-Large"],
        ["2504","Hunyuan-T1","hybrid reasoning 模型。","https://cloud.tencent.com/product/tclm"],
        ["2506","Hunyuan-A13B","80B/13B active 开放混合推理 MoE，20T tokens。","https://github.com/Tencent-Hunyuan/Hunyuan-A13B"]]},
    {"id":"seed","dir":"ByteDance_Seed","name":"ByteDance · Seed","region":"国内","color":"#ff6ca8","thesis":"从多模态理解走向真实环境 agency 与 computer use。","models":[
        ["2505","Seed1.5","通用多模态与 reasoning 基座。","https://seed.bytedance.com/en/"],
        ["2506","Seed1.6","多模态 family 与产品部署升级。","https://seed.bytedance.com/en/"],
        ["2512","Seed1.8","真实世界 agent foundation model。","https://seed.bytedance.com/en/blog/official-release-of-seed1-8-a-generalized-agentic-model"],
        ["2602","Seed2.0","Computer Use 与 agent foundation model 扩展。","https://seed.bytedance.com/en/blog/seed-2-0-official-launch"],
        ["2606","Seed2.1","面向真实生产力任务的下一代通用 agent 基座。","https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity"]]},
    {"id":"zhipu","dir":"Zhipu_GLM","name":"Zhipu · GLM","region":"国内","color":"#58e0b5","thesis":"General Language Model 演进为 agentic reasoning/coding 原生基座。","models":[
        ["2210","GLM-130B","双语开放自回归预训练基座。","https://github.com/THUDM/GLM-130B"],
        ["2303","ChatGLM","首代中英双语对话 GLM，将系列带入广泛开源使用。","https://github.com/zai-org/ChatGLM-6B"],
        ["2306","ChatGLM2","1.4T 双语 tokens、32K context 与更高效 MQA 推理。","https://github.com/zai-org/ChatGLM2-6B"],
        ["2310","ChatGLM3","对话、代码与工具调用 family。","https://github.com/THUDM/ChatGLM3"],
        ["2401","GLM-4","新一代多模态与 tool-use 基座。","https://www.zhipuai.cn/"],
        ["2507","GLM-4.5","355B/32B active ARC foundation model。","https://github.com/zai-org/GLM-4.5"],
        ["2509","GLM-4.6","200K 上下文与更强 coding 的通用升级。","https://docs.z.ai/guides/llm/glm-4.6"],
        ["2512","GLM-4.7","coding、tool use 与 interleaved reasoning。","https://docs.z.ai/"],
        ["2602","GLM-5","面向 agentic engineering 的新正代。","https://docs.z.ai/guides/overview/overview"],
        ["2604","GLM-5.1","long-horizon coding agent。","https://docs.z.ai/guides/overview/overview"],
        ["2606","GLM-5.2","1M context 与长时程 coding。","https://docs.z.ai/guides/overview/overview"],
        ["260814","GLM-5.3","沿用 5.2 base、以大规模 post-training 强化 coding、cyber 与长时程 agents。","https://z.ai/blog/glm-5.3"]]},
    {"id":"kimi","dir":"Moonshot_Kimi","name":"Moonshot · Kimi","region":"国内","color":"#9f8cff","thesis":"超长上下文底座逐步转向开放 MoE、视觉 agent 与 agent swarm。","models":[
        ["2310","Moonshot v1","长上下文产品化起点。","https://www.moonshot.cn/"],
        ["2501","Kimi k1.5","多模态 reasoning 与 RL scaling。","https://arxiv.org/abs/2501.12599"],
        ["2507","Kimi K2","1T/32B active agentic intelligence。","https://github.com/MoonshotAI/Kimi-K2"],
        ["2509","Kimi K2-Instruct-0905","K2 主 checkpoint 更新，强化 agentic coding、前端与上下文能力。","https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905"],
        ["2511","Kimi K2 Thinking","K2 正式 reasoning 更新，扩展通用推理与工具任务能力。","https://www.kimi.com/en/blog/kimi-k2-thinking"],
        ["2601","Kimi K2.5","视觉 agent、joint RL 与 Agent Swarm。","https://www.kimi.com/en/blog/kimi-k2-5"],
        ["2604","Kimi K2.6","开放 coding 与 agentic scaling。","https://huggingface.co/moonshotai"],
        ["2607","Kimi K3","2.8T/104B-active 原生多模态 agent 基座，1M context。","https://github.com/MoonshotAI/Kimi-K3"]]},
    {"id":"minimax","dir":"MiniMax","name":"MiniMax","region":"国内","color":"#ff8566","thesis":"长上下文 attention 效率与真实环境 agent RL 双线合流。","models":[
        ["2506","MiniMax-M1","Lightning Attention、1M context 与 CISPO。","https://arxiv.org/abs/2506.13585"],
        ["2510","MiniMax-M2","低激活 MoE 与 coding agent。","https://www.minimax.io/news/minimax-m2"],
        ["2512","MiniMax-M2.1","多语言 coding 与 office agent。","https://www.minimax.io/news"],
        ["2602","MiniMax-M2.5","真实环境 RL、search/tool/office tasks。","https://www.minimax.io/news"],
        ["2603","MiniMax-M2.7","训练流程中的早期 self-evolution。","https://www.minimax.io/news"],
        ["2606","MiniMax-M3","MSA、1M context 与原生多模态。","https://www.minimax.io/news"]]},
    {"id":"mimo","dir":"Xiaomi_MiMo","name":"Xiaomi · MiMo","region":"国内","color":"#ff9b5f","thesis":"小型 reasoning base 演进为低激活、长上下文、全模态 agent family。","models":[
        ["2505","MiMo-7B","25T tokens、MTP 与 reasoning pretraining。","https://arxiv.org/abs/2505.07608"],
        ["2506","MiMo-VL-7B","视觉 grounding 与 MORL。","https://arxiv.org/abs/2506.03569"],
        ["2601","MiMo-V2-Flash","309B/15B、Hybrid SWA 与 MOPD。","https://arxiv.org/abs/2601.02780"],
        ["2603","MiMo-V2-Pro","万亿参数、1M context 与 agent workloads。","https://github.com/XiaomiMiMo"],
        ["2604","MiMo-V2.5","开放 omnimodal agent family。","https://github.com/XiaomiMiMo"],
        ["2604","MiMo-V2.5-Pro","1.02T/42B、长时程 coding agent。","https://github.com/XiaomiMiMo"]]},
    {"id":"longcat","dir":"Meituan_LongCat","name":"Meituan · LongCat","region":"国内","color":"#ffd15f","thesis":"稳定 560B MoE 基座上扩展 thinking、agent、omni 与 formal reasoning。","models":[
        ["2509","LongCat-Flash","560B/27B、Zero-Comp Experts 与 ScMoE。","https://github.com/meituan-longcat/LongCat-Flash-Chat"],
        ["2509","LongCat-Flash-Thinking","Domain-Parallel RL 与长 CoT。","https://arxiv.org/abs/2509.18883"],
        ["2511","LongCat-Flash-Omni","实时音视频 omni 扩展。","https://arxiv.org/abs/2511.00279"],
        ["2601","LongCat-Flash-Lite","68.5B/3B 与 embedding scaling。","https://arxiv.org/abs/2601.21204"],
        ["2601","LongCat-Flash-Thinking-2601","robust RL、agent search 与 1M context。","https://arxiv.org/abs/2601.16725"],
        ["2603","LongCat-Next","DiNA 与原生离散 token omni。","https://arxiv.org/abs/2603.27538"]]},
    {"id":"stepfun","dir":"stepfun","name":"StepFun · Step","region":"国内","color":"#74d6ff","thesis":"大规模 MoE、推理效率与专项 agent/reasoning family。","models":[
        ["2404","Step-1","千亿参数通用基模。","https://www.stepfun.com/"],
        ["2407","Step-2","万亿参数 MoE 与多模态 family。","https://www.stepfun.com/"],
        ["2507","Step-3","196B/11B active 的推理效率路线。","https://github.com/stepfun-ai/Step3"],
        ["2602","Step-3.5-Flash","可扩展 RL loop 与 agentic coding。","https://github.com/stepfun-ai"]]},
    {"id":"ernie_extra","dir":"MiroMind","name":"MiroMind · MiroThinker","region":"国内","color":"#c7a7ff","thesis":"以 interaction scaling 和 verification agent 构建 research-agent 基模。","models":[
        ["2511","MiroThinker v1","600 tool calls/task 的 interaction scaling。","https://arxiv.org/abs/2511.11793"],
        ["2603","MiroThinker 1.7","local/global verification agent。","https://arxiv.org/abs/2603.15726"]]},
]

# Editorial order: the five domestic teams requested by the reader come first,
# followed by the remaining domestic teams, then the overseas top three and the
# rest of the international landscape.  Filtering keeps this same relative
# order, so the domestic view always starts DeepSeek → GLM → Kimi → Qwen → Seed.
TEAM_PRIORITY = [
    "deepseek", "zhipu", "kimi", "qwen", "seed",
    "minimax", "mimo", "longcat", "stepfun", "baidu", "hunyuan", "ernie_extra",
    "openai", "anthropic", "google",
    "meta", "xai", "mistral", "microsoft", "amazon", "nvidia", "cohere", "ibm",
]

# Independently reviewed against the eight teams' official release histories on
# 2026-08-31.  Keeping this separate from TEAMS makes omissions, accidental
# branch promotion, and silent renames fail the build instead of reaching Pages.
TOP8_MAINLINE_CONTRACT = {
    "deepseek": ("DeepSeek LLM", "DeepSeek-V2", "DeepSeek-V2.5", "DeepSeek-V2.5-1210", "DeepSeek-V3", "DeepSeek-R1", "DeepSeek-V3-0324", "DeepSeek-R1-0528", "DeepSeek-V3.1", "DeepSeek-V3.1-Terminus", "DeepSeek-V3.2-Exp", "DeepSeek-V3.2", "DeepSeek-V4", "DeepSeek-V4-Flash", "DeepSeek-V4-Pro", "DeepSeek-V4-Flash-0731", "DeepSeek-V4-Pro-0813"),
    "zhipu": ("GLM-130B", "ChatGLM", "ChatGLM2", "ChatGLM3", "GLM-4", "GLM-4.5", "GLM-4.5-Air", "GLM-4.6", "GLM-4.7", "GLM-4.7-Flash", "GLM-5", "GLM-5.1", "GLM-5.2", "GLM-5.3", "GLM-5.3-Flash"),
    "kimi": ("Moonshot v1", "Kimi k1.5", "Kimi K2", "Kimi K2-Instruct-0905", "Kimi K2 Thinking", "Kimi K2.5", "Kimi K2.6", "Kimi K3"),
    "qwen": ("Qwen", "Qwen1.5", "Qwen2", "Qwen2.5", "Qwen3", "Qwen3-Next", "Qwen3.5", "Qwen3.6", "Qwen3.7", "Qwen3.8"),
    "seed": ("Seed1.5", "Seed1.6", "Seed1.8", "Seed2.0", "MedXIAOHE", "Seed2.1"),
    "openai": ("GPT-1", "GPT-2", "GPT-3", "GPT-3.5", "GPT-4", "GPT-4 Turbo", "GPT-4o", "GPT-4.5", "GPT-4.1", "GPT-5", "GPT-5.1", "GPT-5.2", "GPT-5.3", "GPT-5.4", "GPT-5.5", "GPT-5.6"),
    "anthropic": ("Claude 1", "Claude 2", "Claude 2.1", "Claude 3", "Claude 3.5 Sonnet", "Claude 3.7 Sonnet", "Claude 4", "Claude Opus 4.1", "Claude Sonnet 4.5", "Claude Opus 4.5", "Claude Sonnet 4.6", "Claude Opus 4.6", "Claude Opus 4.7", "Claude Opus 4.8", "Claude Sonnet 5", "Claude Opus 5"),
    "google": ("Gemini 1.0", "Gemini 1.5 Pro", "Gemini 2.0", "Gemini 2.5 Pro", "Gemini 3 Pro", "Gemini 3.1 Pro", "Gemini 3.5 Flash", "Gemini 3.6 Flash", "Gemini 3.7 Flash"),
}

# Top-8 branch audit.  Mainline generations stay in TEAMS; these are specialist
# or modality branches, and are therefore shown as branch chips instead of being
# mixed into the generation timeline.  “models” names canonical representative
# releases rather than every parameter/API snapshot.
VARIANT_FAMILIES = {
    "deepseek": [
        {"name":"Reasoning","models":"R1-Zero · R1 · R1-Distill · V3.2-Speciale","source":"https://github.com/deepseek-ai/DeepSeek-R1"},
        {"name":"Code","models":"DeepSeek-Coder · Coder-V2","source":"https://github.com/deepseek-ai/DeepSeek-Coder-V2"},
        {"name":"Math / Prover","models":"DeepSeekMath · Prover V1/V1.5/V2","source":"https://github.com/deepseek-ai/DeepSeek-Prover-V2"},
        {"name":"Vision / Omni","models":"DeepSeek-VL/VL2 · Janus/Janus-Pro","source":"https://github.com/deepseek-ai/Janus"},
        {"name":"Document","models":"DeepSeek-OCR · OCR2","source":"https://github.com/deepseek-ai/DeepSeek-OCR"},
    ],
    "zhipu": [
        {"name":"Vision","models":"GLM-4V · 4.5V · 4.6V · 5V · CogVLM","source":"https://docs.z.ai/guides/overview/overview"},
        {"name":"Code","models":"CodeGeeX · CodeGeeX4","source":"https://github.com/THUDM/CodeGeeX4"},
        {"name":"Speech","models":"GLM-4-Voice · GLM-TTS","source":"https://github.com/THUDM/GLM-4-Voice"},
        {"name":"Document","models":"GLM-OCR","source":"https://docs.z.ai/guides/overview/overview"},
        {"name":"Image / Video","models":"CogView · CogVideoX","source":"https://github.com/THUDM/CogVideo"},
        {"name":"Agent","models":"AutoGLM · Phone / Computer Use","source":"https://github.com/zai-org/Open-AutoGLM"},
    ],
    "kimi": [
        {"name":"Vision","models":"Kimi-VL · K1.5 · K2.5","source":"https://github.com/MoonshotAI/Kimi-VL"},
        {"name":"Audio","models":"Kimi-Audio","source":"https://github.com/MoonshotAI/Kimi-Audio"},
        {"name":"Code","models":"Kimi-Dev","source":"https://github.com/MoonshotAI/Kimi-Dev"},
        {"name":"Formal Reasoning","models":"Kimina-Prover","source":"https://github.com/MoonshotAI/Kimina-Prover-Preview"},
        {"name":"Efficient Attention","models":"MoBA · Kimi Linear","source":"https://github.com/MoonshotAI/Kimi-Linear"},
    ],
    "qwen": [
        {"name":"Code","models":"Qwen-Coder · Qwen3-Coder · Coder-Next","source":"https://qwenlm.github.io/blog/qwen3-coder/"},
        {"name":"Vision","models":"Qwen-VL · Qwen3-VL · VL-Seg · VLA","source":"https://github.com/QwenLM/Qwen3-VL"},
        {"name":"Omni / Speech","models":"Qwen3-Omni · ASR · TTS","source":"https://github.com/QwenLM/Qwen3-Omni"},
        {"name":"Image","models":"Qwen-Image · Image 2 · VAE 2","source":"https://github.com/QwenLM/Qwen-Image"},
        {"name":"Retrieval","models":"Embedding · Reranker · VL-Embedding","source":"https://github.com/QwenLM/Qwen3-Embedding"},
        {"name":"Safety / Agent","models":"Qwen3Guard · Qwen-Scope","source":"https://github.com/QwenLM/Qwen3Guard"},
    ],
    "seed": [
        {"name":"Vision / Omni","models":"Seed1.5-VL · Seed1.5-Thinking · Seed2.0","source":"https://github.com/ByteDance-Seed/Seed1.5-VL"},
        {"name":"Code / Open","models":"Seed-Coder · Seed-OSS · Seed-Prover","source":"https://github.com/ByteDance-Seed"},
        {"name":"Any-to-any","models":"BAGEL","source":"https://github.com/ByteDance-Seed/Bagel"},
        {"name":"Speech","models":"Seed-TTS","source":"https://seed.bytedance.com/en/"},
        {"name":"Image / Video","models":"Seedream · SeedEdit · Seedance","source":"https://seed.bytedance.com/en/"},
        {"name":"World / Embodied","models":"Seed3D · GR family","source":"https://seed.bytedance.com/en/"},
    ],
    "openai": [
        {"name":"Reasoning","models":"o1 · o3 · o4-mini","source":"https://developers.openai.com/api/docs/models"},
        {"name":"Coding","models":"GPT-5-Codex · 5.1-Codex-Max · 5.2/5.3-Codex","source":"https://developers.openai.com/api/docs/models/gpt-5.3-codex"},
        {"name":"Open weights","models":"gpt-oss-20b · gpt-oss-120b","source":"https://developers.openai.com/api/docs/models"},
        {"name":"Realtime / Audio","models":"GPT-Realtime · Transcribe · TTS","source":"https://developers.openai.com/api/docs/models"},
        {"name":"Image / Cyber","models":"GPT-Image · GPT-5.6 Cyber / Daybreak","source":"https://developers.openai.com/api/docs/models"},
    ],
    "anthropic": [
        {"name":"Capability tiers","models":"Haiku · Sonnet · Opus","source":"https://docs.anthropic.com/en/docs/about-claude/models/overview"},
        {"name":"Hybrid Reasoning","models":"Claude 3.7+ extended thinking","source":"https://www.anthropic.com/news/claude-3-7-sonnet"},
        {"name":"Computer Use","models":"Claude Computer Use","source":"https://www.anthropic.com/news/3-5-models-and-computer-use"},
        {"name":"Special access","models":"Fable 5 · regulated capability programs","source":"https://www.anthropic.com/news"},
    ],
    "google": [
        {"name":"Serving tiers","models":"Pro · Flash · Flash-Lite · Nano","source":"https://deepmind.google/models/model-cards/"},
        {"name":"Deep Think / Computer","models":"Deep Think · Computer Use","source":"https://deepmind.google/models/model-cards/"},
        {"name":"Image / Omni","models":"Flash Image · Gemini Omni","source":"https://deepmind.google/models/"},
        {"name":"Audio / Live","models":"Flash Audio · Live · Translate · Transcribe","source":"https://deepmind.google/models/model-cards/"},
        {"name":"Robotics","models":"Robotics · Robotics-ER · On-Device","source":"https://deepmind.google/models/gemini-robotics/"},
        {"name":"Open sibling","models":"Gemma · CodeGemma · PaliGemma · ShieldGemma","source":"https://deepmind.google/models/model-cards/"},
    ],
}

# Additional named models that should be visible on a team's horizontal line.
PINNED_TIMELINE_VARIANTS = {
    "deepseek": [
        {
            "date": "260424",
            "name": "DeepSeek-V4-Flash",
            "summary": "V4-Flash Preview：284B/13B、1M context，是独立训练的高效率同代 checkpoint。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Flash.md",
            "assetPosters": ["deepseek_v4_flash_poster_zh.html"],
            "lineageType": "mainline",
            "label": "V4 Preview checkpoint",
        },
        {
            "date": "260424",
            "name": "DeepSeek-V4-Pro",
            "summary": "V4-Pro Preview：1.6T/49B、1M context，面向高容量 reasoning 与 agent workload。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Pro.md",
            "assetPosters": ["deepseek_v4_pro_poster_zh.html"],
            "lineageType": "mainline",
            "label": "V4 Preview checkpoint",
        },
        {
            "date": "260627",
            "name": "DeepSeek-V4-Flash-DSpark",
            "summary": "V4-Flash checkpoint 加 DSpark speculative decoding module；官方明确说明它不是新模型。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-DSpark",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Flash-DSpark.md",
            "assetPosters": ["deepseek_v4_flash_dspark_poster_zh.html"],
            "lineageType": "variant",
            "label": "V4 · 推测解码",
        },
        {
            "date": "260627",
            "name": "DeepSeek-V4-Pro-DSpark",
            "summary": "V4-Pro checkpoint 加 DSpark speculative decoding module；官方明确说明它不是新模型。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Pro-DSpark.md",
            "assetPosters": ["deepseek_v4_pro_dspark_poster_zh.html"],
            "lineageType": "variant",
            "label": "V4 · 推测解码",
        },
        {
            "date": "260731",
            "name": "DeepSeek-V4-Flash-0731",
            "summary": "正式替代 Flash Preview 的 agent 增强 checkpoint，内置 DSpark，并支持 low/high/max reasoning effort。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Flash-0731.md",
            "assetPosters": ["deepseek_v4_flash_0731_poster_zh.html"],
            "lineageType": "mainline",
            "label": "V4 release checkpoint",
        },
        {
            "date": "260813",
            "name": "DeepSeek-V4-Pro-0813",
            "summary": "正式替代 Pro Preview 的生产 agent checkpoint，内置 DSpark，并支持 low/high/max reasoning effort。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Pro-0813.md",
            "assetPosters": ["deepseek_v4_pro_0813_poster_zh.html"],
            "lineageType": "mainline",
            "label": "V4 release checkpoint",
        },
        {
            "date": "260831",
            "name": "DeepSeek-V4-Flash-Vision-Exp",
            "summary": "V4 family 首个实验多模态 checkpoint：在 Flash 上加入视觉模块，强化多模态 agent 能力。",
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp",
            "folder": "2604_deepseek_v4",
            "assetNote": "DeepSeek-V4-Flash-Vision-Exp.md",
            "assetPosters": ["deepseek_v4_flash_vision_exp_poster_zh.html"],
            "lineageType": "variant",
            "label": "V4 · 多模态实验",
        },
    ],
    "zhipu": [
        {
            "date": "2507",
            "name": "GLM-4.5-Air",
            "summary": "GLM-4.5 的高效率同代模型：106B 总参数、12B 激活参数，保留混合推理、coding 与 agent 能力。",
            "source": "https://huggingface.co/zai-org/GLM-4.5-Air",
            "folder": "2508_GLM_4_5",
            "assetNote": "GLM-4.5-Air.md",
            "assetPosters": ["glm_4_5_air_poster_zh.html"],
            "lineageType": "mainline",
            "label": "GLM-4.5 同代模型",
        },
        {
            "date": "2601",
            "name": "GLM-4.7-Flash",
            "summary": "GLM-4.7 的轻量同代模型：30B-A3B MoE，面向本地部署、coding 与 agentic tasks。",
            "source": "https://huggingface.co/zai-org/GLM-4.7-Flash",
            "folder": "2512_glm_4_7",
            "assetNote": "GLM-4.7-Flash.md",
            "assetPosters": ["glm_4_7_flash_poster_zh.html"],
            "lineageType": "mainline",
            "label": "GLM-4.7 同代模型",
        },
        {
            "date": "260826",
            "name": "GLM-5.3-Flash",
            "summary": "GLM-5.3 的高效率同代模型：320B 总参数、18B 激活参数，原生多模态并采用混合稀疏/线性注意力。",
            "source": "https://huggingface.co/zai-org/GLM-5.3-Flash",
            "folder": "2608_GLM_5_3_Flash",
            "assetNote": "GLM-5.3-Flash.md",
            "assetPosters": ["glm_5_3_flash_poster_zh.html"],
            "lineageType": "mainline",
            "label": "GLM-5.3 同代模型",
        },
    ],
    "seed": [
        {
            "date": "2602",
            "name": "MedXIAOHE",
            "summary": "ByteDance · Seed 生态中的多模态模型，提供完整的数据与训练 recipe。",
            "source": "https://arxiv.org/abs/2602.12705",
            "folder": "Variants/2602_MedXIAOHE",
            "lineageType": "mainline",
            "label": "Seed 模型",
        }
    ]
}

# Family folders may contain a dedicated note/poster for a sibling SKU.  Keep
# the generic family leaf on its own assets after those sibling files are added.
MODEL_ASSET_OVERRIDES = {
    "DeepSeek-V4": {
        "assetNote": "DeepSeek-V4.md",
        "assetPosters": ["deepseek_v4_poster_zh.html"],
    },
    "GLM-4.5": {
        "folder": "2508_GLM_4_5",
        "assetNote": "GLM-4.5-ARC-Foundation-Models.md",
        "assetPosters": ["GLM_4_5_poster.html", "GLM_4_5_poster_zh.html"],
    },
    "GLM-4.7": {
        "assetNote": "GLM-4.7.md",
        "assetPosters": ["glm_4_7_poster_zh.html"],
    },
}

# Individually addressable Top-8 branch models.  These are model leaves, not
# marketing-family labels: every item gets its own Overview route and remains
# grouped under its official capability/modality branch.
BRANCH_MODEL_NODES = {
    "deepseek": [
        ("2401", "DeepSeekMoE", "Architecture", "https://github.com/deepseek-ai/DeepSeek-MoE"),
        ("2501", "DeepSeek-R1-Zero", "Reasoning", "https://github.com/deepseek-ai/DeepSeek-R1"),
        ("2501", "DeepSeek-R1-Distill", "Reasoning", "https://github.com/deepseek-ai/DeepSeek-R1"),
        ("2505", "DeepSeek-R1-0528", "Reasoning", "https://github.com/deepseek-ai/DeepSeek-R1"),
        ("2311", "DeepSeek-Coder", "Code", "https://github.com/deepseek-ai/DeepSeek-Coder"),
        ("2406", "DeepSeek-Coder-V2", "Code", "https://github.com/deepseek-ai/DeepSeek-Coder-V2"),
        ("2402", "DeepSeekMath", "Math / Prover", "https://github.com/deepseek-ai/DeepSeek-Math"),
        ("2408", "DeepSeek-Prover-V1.5", "Math / Prover", "https://github.com/deepseek-ai/DeepSeek-Prover-V1.5"),
        ("2504", "DeepSeek-Prover-V2", "Math / Prover", "https://github.com/deepseek-ai/DeepSeek-Prover-V2"),
        ("2511", "DeepSeek-Math-V2", "Math / Prover", "https://github.com/deepseek-ai/DeepSeek-Math-V2"),
        ("2403", "DeepSeek-VL", "Vision / Omni", "https://github.com/deepseek-ai/DeepSeek-VL"),
        ("2412", "DeepSeek-VL2", "Vision / Omni", "https://github.com/deepseek-ai/DeepSeek-VL2"),
        ("2410", "Janus", "Vision / Omni", "https://github.com/deepseek-ai/Janus"),
        ("2501", "Janus-Pro", "Vision / Omni", "https://github.com/deepseek-ai/Janus"),
        ("2510", "DeepSeek-OCR", "Document", "https://github.com/deepseek-ai/DeepSeek-OCR"),
        ("2601", "DeepSeek-OCR2", "Document", "https://github.com/deepseek-ai/DeepSeek-OCR-2"),
    ],
    "zhipu": [
        ("2303", "ChatGLM-6B", "ChatGLM", "https://github.com/zai-org/ChatGLM-6B"),
        ("2306", "ChatGLM2-6B", "ChatGLM", "https://github.com/zai-org/ChatGLM2-6B"),
        ("2304", "VisualGLM-6B", "Vision", "https://github.com/zai-org/VisualGLM-6B"),
        ("2310", "CogVLM", "Vision", "https://github.com/THUDM/CogVLM"),
        ("2407", "CogVLM2", "Vision", "https://github.com/THUDM/CogVLM2"),
        ("2311", "CogAgent", "Vision Agent", "https://github.com/zai-org/CogAgent"),
        ("2402", "CogCoM", "Vision Agent", "https://github.com/zai-org/CogCoM"),
        ("2406", "GLM-4V", "Vision", "https://github.com/zai-org/GLM-4"),
        ("2507", "GLM-4.1V-Thinking", "Vision", "https://github.com/zai-org/GLM-V"),
        ("2508", "GLM-4.5V", "Vision", "https://github.com/zai-org/GLM-V"),
        ("2510", "GLM-4.6V", "Vision", "https://docs.z.ai/guides/overview/overview"),
        ("2605", "GLM-5V", "Vision", "https://docs.z.ai/guides/overview/overview"),
        ("2209", "CodeGeeX", "Code", "https://github.com/zai-org/CodeGeeX"),
        ("2307", "CodeGeeX2", "Code", "https://github.com/THUDM/CodeGeeX2"),
        ("2407", "CodeGeeX4", "Code", "https://github.com/THUDM/CodeGeeX4"),
        ("2504", "GLM-Z1", "Reasoning", "https://github.com/zai-org/GLM-4"),
        ("2410", "GLM-4-Voice", "Speech", "https://github.com/THUDM/GLM-4-Voice"),
        ("2512", "GLM-ASR", "Speech", "https://github.com/zai-org/GLM-ASR"),
        ("2604", "GLM-TTS", "Speech", "https://docs.z.ai/guides/overview/overview"),
        ("2602", "GLM-OCR", "Document", "https://docs.z.ai/guides/overview/overview"),
        ("2105", "CogView", "Image / Video", "https://github.com/zai-org/CogView"),
        ("2204", "CogView2", "Image / Video", "https://github.com/zai-org/CogView2"),
        ("2409", "CogView3", "Image / Video", "https://github.com/THUDM/CogView3"),
        ("2409", "CogView4", "Image / Video", "https://github.com/zai-org/CogView4"),
        ("2205", "CogVideo", "Image / Video", "https://github.com/zai-org/CogVideo"),
        ("2408", "CogVideoX", "Image / Video", "https://github.com/zai-org/CogVideo"),
        ("2608", "CogVideoX-3", "Image / Video", "https://docs.z.ai/guides/overview/overview"),
        ("2601", "GLM-Image", "Image / Video", "https://github.com/zai-org/GLM-Image"),
        ("2411", "GLM-Edge", "Edge", "https://github.com/zai-org/GLM-Edge"),
        ("2501", "AutoGLM", "Agent", "https://github.com/zai-org/Open-AutoGLM"),
        ("2512", "AutoGLM-Phone", "Agent", "https://github.com/zai-org/Open-AutoGLM"),
    ],
    "kimi": [
        ("2502", "Moonlight", "Open Pretraining", "https://github.com/MoonshotAI/Moonlight"),
        ("2504", "Kimi-Audio", "Audio", "https://github.com/MoonshotAI/Kimi-Audio"),
        ("2506", "Kimi-Dev", "Code", "https://github.com/MoonshotAI/Kimi-Dev"),
        ("2506", "Kimi-Researcher", "Research Agent", "https://github.com/MoonshotAI/Kimi-Researcher"),
        ("2511", "Kimi K2 Thinking", "Reasoning", "https://github.com/MoonshotAI/Kimi-K2"),
        ("2504", "Kimina-Prover Preview", "Formal Reasoning", "https://github.com/MoonshotAI/Kimina-Prover-Preview"),
        ("2502", "MoBA", "Efficient Attention", "https://github.com/MoonshotAI/MoBA"),
    ],
    "qwen": [
        ("2503", "QwQ-32B", "Reasoning / Math", "https://github.com/QwenLM/QwQ"),
        ("2409", "Qwen2.5-Math", "Reasoning / Math", "https://github.com/QwenLM/Qwen2.5-Math"),
        ("2308", "CodeQwen", "Code", "https://github.com/QwenLM/CodeQwen1.5"),
        ("2409", "Qwen2.5-Coder", "Code", "https://github.com/QwenLM/Qwen2.5-Coder"),
        ("2507", "Qwen3-Coder", "Code", "https://github.com/QwenLM/Qwen3-Coder"),
        ("2603", "Qwen3-Coder-Next", "Code", "https://github.com/QwenLM/Qwen3-Coder"),
        ("2308", "Qwen-VL", "Vision", "https://github.com/QwenLM/Qwen-VL"),
        ("2408", "Qwen2-VL", "Vision", "https://github.com/QwenLM/Qwen2-VL"),
        ("2501", "Qwen2.5-VL", "Vision", "https://github.com/QwenLM/Qwen2.5-VL"),
        ("2511", "Qwen3-VL", "Vision", "https://github.com/QwenLM/Qwen3-VL"),
        ("2605", "Qwen3-VL-Seg", "Vision", "https://github.com/QwenLM/Qwen3-VL"),
        ("2605", "Qwen-VLA", "Vision", "https://github.com/QwenLM"),
        ("2312", "Qwen-Audio", "Omni / Speech", "https://github.com/QwenLM/Qwen-Audio"),
        ("2408", "Qwen2-Audio", "Omni / Speech", "https://github.com/QwenLM/Qwen2-Audio"),
        ("2503", "Qwen2.5-Omni", "Omni / Speech", "https://github.com/QwenLM/Qwen2.5-Omni"),
        ("2509", "Qwen3-Omni", "Omni / Speech", "https://github.com/QwenLM/Qwen3-Omni"),
        ("2601", "Qwen3-ASR", "Omni / Speech", "https://github.com/QwenLM/Qwen3-ASR"),
        ("2601", "Qwen3-TTS", "Omni / Speech", "https://github.com/QwenLM/Qwen3-TTS"),
        ("2508", "Qwen-Image", "Image", "https://github.com/QwenLM/Qwen-Image"),
        ("2512", "Qwen-Image-Layered", "Image", "https://github.com/QwenLM/Qwen-Image-Layered"),
        ("2605", "Qwen-Image-2", "Image", "https://github.com/QwenLM/Qwen-Image"),
        ("2506", "Qwen3-Embedding", "Retrieval", "https://github.com/QwenLM/Qwen3-Embedding"),
        ("2601", "Qwen3-VL-Embedding", "Retrieval", "https://github.com/QwenLM/Qwen3-VL-Embedding"),
        ("2510", "Qwen3Guard", "Safety / Agent", "https://github.com/QwenLM/Qwen3Guard"),
        ("2602", "WebWorld", "Safety / Agent", "https://github.com/QwenLM/WebWorld"),
        ("2606", "Qwen-AgentWorld", "Safety / Agent", "https://github.com/QwenLM/Qwen-AgentWorld"),
        ("2605", "Qwen-Scope", "Safety / Agent", "https://github.com/QwenLM"),
        ("2606", "Qwen-RobotManip", "Robotics", "https://github.com/QwenLM/Qwen-RobotManip"),
        ("2606", "Qwen-RobotNav", "Robotics", "https://github.com/QwenLM/Qwen-RobotNav"),
    ],
    "seed": [
        ("2504", "Seed-Thinking-v1.5", "Reasoning / Math", "https://github.com/ByteDance-Seed/Seed-Thinking-v1.5"),
        ("2507", "Seed-Prover", "Reasoning / Math", "https://github.com/ByteDance-Seed/Seed-Prover"),
        ("2510", "BFS-Prover-V2", "Reasoning / Math", "https://github.com/ByteDance-Seed/BFS-Prover-V2"),
        ("2505", "Seed1.5-VL", "Vision / Omni", "https://github.com/ByteDance-Seed/Seed1.5-VL"),
        ("2507", "Seed-X-7B", "Multilingual", "https://github.com/ByteDance-Seed/Seed-X-7B"),
        ("2508", "Seed-OSS", "Code / Open", "https://github.com/ByteDance-Seed/seed-oss"),
        ("2506", "Seed-Coder", "Code / Open", "https://github.com/ByteDance-Seed"),
        ("2601", "Seed Diffusion Preview", "Code / Open", "https://github.com/ByteDance-Seed/Stable-DiffCoder"),
        ("2505", "BAGEL", "Any-to-any", "https://github.com/ByteDance-Seed/Bagel"),
        ("2405", "Seed-TTS", "Speech", "https://seed.bytedance.com/en/"),
        ("2608", "SeedRealtime", "Speech / Realtime", "https://seed.bytedance.com/en/models/seed_realtime"),
        ("2608", "Seed Audio 1.0", "Speech / Realtime", "https://seed.bytedance.com/en/models/seed_audio"),
        ("2608", "Seeduplex", "Speech / Realtime", "https://seed.bytedance.com/en/models/seeduplex"),
        ("2608", "Seed LiveInterpret 2.0", "Speech / Realtime", "https://seed.bytedance.com/en/models/seed_liveinterpret_2_0"),
        ("2608", "Seed Realtime Voice", "Speech / Realtime", "https://seed.bytedance.com/en/models/seed_realtime_voice"),
        ("2608", "Seed-Music", "Speech / Realtime", "https://seed.bytedance.com/en/models/seed_music"),
        ("2504", "Seedream 3.0", "Image / Video", "https://seed.bytedance.com/en/"),
        ("2509", "Seedream 4.0", "Image / Video", "https://seed.bytedance.com/en/models/seedream_4_0"),
        ("2512", "Seedream 4.5", "Image / Video", "https://seed.bytedance.com/en/models/seedream_4_5"),
        ("2608", "Seedream 5.0 Lite", "Image / Video", "https://seed.bytedance.com/en/models/seedream_5_0_lite"),
        ("2608", "Seedream 5.0 Pro", "Image / Video", "https://seed.bytedance.com/en/models/seedream_5_0_pro"),
        ("2506", "SeedEdit 3.0", "Image / Video", "https://seed.bytedance.com/en/models/seededit_3_0"),
        ("2506", "Seedance 1.0", "Image / Video", "https://seed.bytedance.com/en/"),
        ("2512", "Seedance 1.5 Pro", "Image / Video", "https://seed.bytedance.com/en/models/seedance_1_5_pro"),
        ("2602", "Seedance 2.0", "Image / Video", "https://seed.bytedance.com/en/models/seedance_2_0"),
        ("2608", "Seedance 2.5", "Image / Video", "https://seed.bytedance.com/en/models/seedance_2_5"),
        ("2506", "SeedVR", "Image / Video", "https://github.com/ByteDance-Seed/SeedVR"),
        ("2503", "Seed3D 1.0", "World / Embodied", "https://seed.bytedance.com/en/models/seed3d"),
        ("2608", "Seed3D 2.0", "World / Embodied", "https://seed.bytedance.com/en/models/seed3d_2_0"),
        ("2501", "VideoWorld", "World / Embodied", "https://github.com/ByteDance-Seed/VideoWorld"),
        ("2608", "Seed GR-3", "Robotics", "https://seed.bytedance.com/en/models/seed_gr_3"),
        ("2608", "Seed GR-RL", "Robotics", "https://seed.bytedance.com/en/models/seed_gr_rl"),
        ("2608", "Protenix", "AI for Science", "https://seed.bytedance.com/en/models/protenix"),
    ],
    "openai": [
        ("2409", "o1", "Reasoning", "https://developers.openai.com/api/docs/models/o1"),
        ("2501", "o3-mini", "Reasoning", "https://developers.openai.com/api/docs/models/o3-mini"),
        ("2504", "o3", "Reasoning", "https://developers.openai.com/api/docs/models/o3"),
        ("2506", "o3-pro", "Reasoning", "https://developers.openai.com/api/docs/models/o3-pro"),
        ("2504", "o4-mini", "Reasoning", "https://developers.openai.com/api/docs/models/o4-mini"),
        ("2509", "GPT-5-Codex", "Coding", "https://developers.openai.com/api/docs/models"),
        ("2511", "GPT-5.1-Codex-Max", "Coding", "https://developers.openai.com/api/docs/models"),
        ("2512", "GPT-5.2-Codex", "Coding", "https://developers.openai.com/api/docs/models"),
        ("2602", "GPT-5.3-Codex", "Coding", "https://developers.openai.com/api/docs/models/gpt-5.3-codex"),
        ("2603", "GPT-5.4 Pro", "GPT tiers", "https://developers.openai.com/api/docs/models/gpt-5.4-pro"),
        ("2603", "GPT-5.4 Mini", "GPT tiers", "https://developers.openai.com/api/docs/models/gpt-5.4-mini"),
        ("2603", "GPT-5.4 Nano", "GPT tiers", "https://developers.openai.com/api/docs/models/gpt-5.4-nano"),
        ("2604", "GPT-5.5 Pro", "GPT tiers", "https://developers.openai.com/api/docs/models/gpt-5.5-pro"),
        ("2608", "GPT-5.6 Terra", "GPT tiers", "https://developers.openai.com/api/docs/models/gpt-5.6-terra"),
        ("2608", "GPT-5.6 Luna", "GPT tiers", "https://developers.openai.com/api/docs/models/gpt-5.6-luna"),
        ("2608", "GPT-5.6 Cyber", "Cyber", "https://developers.openai.com/api/docs/models/gpt-5.6-cyber"),
        ("2508", "gpt-oss-20b", "Open weights", "https://openai.com/index/introducing-gpt-oss/"),
        ("2508", "gpt-oss-120b", "Open weights", "https://openai.com/index/introducing-gpt-oss/"),
        ("2508", "GPT-Realtime", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Realtime-2.1", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Realtime-2.1 Mini", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2606", "GPT-Realtime-2", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Realtime-Translate", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2604", "GPT-Realtime-1.5", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2503", "GPT-4o Transcribe", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Transcribe", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Live-Transcribe", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Realtime-Whisper", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2503", "GPT-4o Mini Transcribe", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2503", "GPT-4o Mini TTS", "Realtime / Audio", "https://developers.openai.com/api/docs/models"),
        ("2503", "GPT-Image-1", "Image", "https://developers.openai.com/api/docs/models"),
        ("2608", "GPT-Image-2", "Image", "https://developers.openai.com/api/docs/models"),
    ],
    "anthropic": [
        ("2403", "Claude 3 Haiku", "Haiku", "https://www.anthropic.com/news/claude-3-family"),
        ("2403", "Claude 3 Sonnet", "Sonnet", "https://www.anthropic.com/news/claude-3-family"),
        ("2403", "Claude 3 Opus", "Opus", "https://www.anthropic.com/news/claude-3-family"),
        ("2410", "Claude 3.5 Haiku", "Haiku", "https://www.anthropic.com/system-cards"),
        ("2505", "Claude Sonnet 4", "Sonnet", "https://www.anthropic.com/system-cards"),
        ("2505", "Claude Opus 4", "Opus", "https://www.anthropic.com/system-cards"),
        ("2508", "Claude Opus 4.1", "Opus", "https://www.anthropic.com/system-cards"),
        ("2509", "Claude Sonnet 4.5", "Sonnet", "https://www.anthropic.com/news/claude-sonnet-4-5"),
        ("2602", "Claude Sonnet 4.6", "Sonnet", "https://www.anthropic.com/system-cards"),
        ("2510", "Claude Haiku 4.5", "Haiku", "https://www.anthropic.com/news/claude-haiku-4-5"),
        ("2606", "Claude Fable 5", "Frontier access", "https://www.anthropic.com/system-cards"),
        ("2606", "Claude Mythos 5", "Frontier access", "https://www.anthropic.com/system-cards"),
        ("2604", "Claude Mythos Preview", "Frontier access", "https://www.anthropic.com/system-cards"),
    ],
    "google": [
        ("2504", "Gemini 2.0 Flash", "Flash", "https://deepmind.google/models/model-cards/"),
        ("2504", "Gemini 2.0 Flash-Lite", "Flash-Lite", "https://deepmind.google/models/model-cards/"),
        ("2506", "Gemini 2.5 Pro", "Pro", "https://deepmind.google/models/model-cards/"),
        ("2509", "Gemini 2.5 Flash", "Flash", "https://deepmind.google/models/model-cards/"),
        ("2509", "Gemini 2.5 Flash-Lite", "Flash-Lite", "https://deepmind.google/models/model-cards/"),
        ("2508", "Gemini 2.5 Deep Think", "Deep Think / Computer", "https://deepmind.google/models/model-cards/"),
        ("2510", "Gemini 2.5 Computer Use", "Deep Think / Computer", "https://deepmind.google/models/model-cards/"),
        ("2511", "Gemini 3 Pro", "Pro", "https://deepmind.google/models/model-cards/"),
        ("2512", "Gemini 3 Flash", "Flash", "https://deepmind.google/models/model-cards/"),
        ("2511", "Gemini 3 Pro Image", "Image", "https://deepmind.google/models/model-cards/"),
        ("2602", "Gemini 3.1 Flash Image", "Image", "https://deepmind.google/models/model-cards/"),
        ("2603", "Gemini 3.1 Flash-Lite", "Flash-Lite", "https://deepmind.google/models/model-cards/"),
        ("2604", "Gemini 3.1 Flash Audio", "Audio / Live", "https://deepmind.google/models/model-cards/"),
        ("2605", "Gemini 3.5 Flash", "Flash", "https://deepmind.google/models/model-cards/"),
        ("2607", "Gemini 3.5 Flash-Lite", "Flash-Lite", "https://deepmind.google/models/model-cards/"),
        ("2607", "Gemini 3.6 Flash", "Flash", "https://deepmind.google/models/model-cards/"),
        ("2608", "Gemini 3.7 Flash", "Flash", "https://deepmind.google/models/model-cards/"),
        ("2608", "Gemini Omni Flash", "Omni", "https://deepmind.google/models/model-cards/"),
        ("2511", "Nano Banana", "Image", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Nano Banana 2", "Image", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Nano Banana 2 Lite", "Image", "https://ai.google.dev/gemini-api/docs/models"),
        ("2511", "Nano Banana Pro", "Image", "https://ai.google.dev/gemini-api/docs/models"),
        ("2512", "Gemini 2.5 Flash Live", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2505", "Gemini 2.5 Flash TTS", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2505", "Gemini 2.5 Pro TTS", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Gemini 3.1 Flash Live", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Gemini 3.1 Flash TTS", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Gemini 3.5 Transcribe", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Gemini 3.5 Live Translate", "Audio / Live", "https://ai.google.dev/gemini-api/docs/models"),
        ("2604", "Gemini Deep Research", "Agent", "https://ai.google.dev/gemini-api/docs/models"),
        ("2604", "Gemini Deep Research Max", "Agent", "https://ai.google.dev/gemini-api/docs/models"),
        ("2608", "Gemini Embedding 2", "Embedding", "https://ai.google.dev/gemini-api/docs/models"),
        ("2507", "Gemini Robotics On-Device", "Robotics", "https://deepmind.google/models/gemini-robotics/"),
        ("2509", "Gemini Robotics 1.5", "Robotics", "https://deepmind.google/models/gemini-robotics/"),
        ("2607", "Gemini Robotics-ER 2", "Robotics", "https://deepmind.google/models/model-cards/"),
        ("2607", "Gemini Robotics-ER 1.6", "Robotics", "https://ai.google.dev/gemini-api/docs/models"),
        ("2607", "Gemini Robotics On-Device 2", "Robotics", "https://deepmind.google/models/model-cards/"),
    ],
}

# This release audits only numbered/mainline generations. Keep the previously
# published branch scope stable instead of expanding it during the mainline fix.
_ESTABLISHED_BRANCH_MODELS = {
    "deepseek": {"DeepSeek-R1-Zero", "DeepSeek-R1-Distill", "DeepSeek-Coder", "DeepSeek-Coder-V2", "DeepSeekMath", "DeepSeek-Prover-V1.5", "DeepSeek-Prover-V2", "DeepSeek-VL", "DeepSeek-VL2", "Janus", "Janus-Pro", "DeepSeek-OCR", "DeepSeek-OCR2"},
    "zhipu": {"CogVLM", "CogVLM2", "GLM-4V", "GLM-4.5V", "GLM-4.6V", "GLM-5V", "CodeGeeX2", "CodeGeeX4", "GLM-4-Voice", "GLM-TTS", "GLM-OCR", "CogView3", "CogVideoX", "AutoGLM"},
    "kimi": {"Kimi-Audio", "Kimi-Dev", "Kimina-Prover Preview", "MoBA"},
    "qwen": {"CodeQwen", "Qwen2.5-Coder", "Qwen3-Coder", "Qwen3-Coder-Next", "Qwen-VL", "Qwen2-VL", "Qwen2.5-VL", "Qwen3-VL", "Qwen3-VL-Seg", "Qwen-VLA", "Qwen-Audio", "Qwen2-Audio", "Qwen3-Omni", "Qwen3-ASR", "Qwen3-TTS", "Qwen-Image", "Qwen-Image-2", "Qwen3-Embedding", "Qwen3-VL-Embedding", "Qwen3Guard", "Qwen-Scope"},
    "seed": {"Seed1.5-VL", "Seed-OSS", "Seed-Coder", "BAGEL", "Seed-TTS", "Seedream 3.0", "Seedance 1.0", "Seed3D"},
    "openai": {"o1", "o3-mini", "o3", "o3-pro", "o4-mini", "GPT-5-Codex", "GPT-5.1-Codex-Max", "GPT-5.2-Codex", "GPT-5.3-Codex", "gpt-oss-20b", "gpt-oss-120b", "GPT-Realtime", "GPT-Realtime-2.1", "GPT-4o Transcribe", "GPT-4o Mini TTS", "GPT-Image-1", "GPT-Image-2"},
    "anthropic": {"Claude 3 Haiku", "Claude 3 Sonnet", "Claude 3 Opus", "Claude 3.5 Haiku", "Claude Haiku 4.5", "Claude Fable 5", "Claude Mythos 5"},
    "google": {"Gemini 2.0 Flash", "Gemini 2.0 Flash-Lite", "Gemini 2.5 Flash", "Gemini 2.5 Flash-Lite", "Gemini 2.5 Deep Think", "Gemini 2.5 Computer Use", "Gemini 3 Flash", "Gemini 3 Pro Image", "Gemini 3.1 Flash Image", "Gemini 3.1 Flash-Lite", "Gemini 3.1 Flash Audio", "Gemini 3.5 Flash-Lite", "Gemini Omni Flash", "Gemini Robotics On-Device", "Gemini Robotics 1.5", "Gemini Robotics-ER 2", "Gemini Robotics On-Device 2"},
}
BRANCH_MODEL_NODES = {
    team_id: [node for node in nodes if node[1] in _ESTABLISHED_BRANCH_MODELS[team_id]]
    for team_id, nodes in BRANCH_MODEL_NODES.items()
}


LATEST_PACKS = {
    "xAI_Grok": ("2608_Grok_4_6", "Grok 4.6", "聚焦长时程 agents、交互式工作与视觉产物。", "https://x.ai/news/grok-4-6"),
    "Mistral_AI": ("2512_Mistral_Large_3", "Mistral Large 3", "开放权重、通用、多模态与多语言旗舰。", "https://mistral.ai/models/"),
    "Tencent_Hunyuan": ("2506_Hunyuan_A13B", "Hunyuan-A13B", "80B 总参数、13B 激活的开放 hybrid-reasoning MoE，预训练 20T tokens。", "https://github.com/Tencent-Hunyuan/Hunyuan-A13B"),
    "Amazon_Nova": ("2512_Nova_2", "Amazon Nova 2", "面向 Bedrock 的第二代 reasoning、多模态与 agentic family。", "https://docs.aws.amazon.com/nova/latest/nova2-userguide/what-is-nova-2.html"),
    "NVIDIA_Nemotron": ("2608_Nemotron_3_5_Lightning", "Nemotron 3.5 Lightning", "30B MoE 面向低成本长时程 agent 与多 agent 专项执行。", "https://blogs.nvidia.com/blog/nemotron-lightning-switchyard-rtx-dgx/"),
    "Cohere": ("2503_Command_A", "Command A", "111B、256K context，面向企业 RAG、tool use、多语言与双 GPU 私有部署。", "https://cohere.com/blog/command-a"),
    "IBM_Granite": ("2510_Granite_4_0", "Granite 4.0", "Mamba-2 + Transformer hybrid，以长上下文 RAM/吞吐效率服务 enterprise agents。", "https://www.ibm.com/new/announcements/ibm-granite-4-0-hyper-efficient-high-performance-hybrid-models"),
    "Microsoft": ("2603_Phi_4_Reasoning_Vision", "Phi-4 Reasoning Vision", "15B 开放权重多模态推理模型，混合 direct/reasoning 数据以平衡质量与时延。", "https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/"),
    "Anthropic": ("2607_Claude_Opus_5", "Claude Opus 5", "面向长时程 agents、coding 与专业工作的 Opus 新正代。", "https://www.anthropic.com/news/claude-opus-5"),
    "OpenAI": ("2608_GPT_5_6", "GPT-5.6", "Sol / Terra / Luna 三层，1.05M context，统一 reasoning、web、files 与 computer use。", "https://developers.openai.com/api/docs/models"),
}


def slugify(value: str) -> str:
    value = value.lower().replace("·", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "model"


def pretty_date(raw: str) -> str:
    if len(raw) == 4:
        return f"20{raw[:2]}-{raw[2:]}"
    if len(raw) == 6:
        return f"20{raw[:2]}-{raw[2:4]}-{raw[4:]}"
    return raw


def source_label(url: str) -> str:
    if "arxiv.org" in url: return "Technical report"
    if "github.com" in url or "huggingface.co" in url: return "Official repo / model card"
    if "developers.openai.com" in url or "docs." in url: return "Official docs"
    if url.endswith(".pdf"): return "System / model card"
    return "Official release"


AUDITED_MODEL_FACTS = {
    "DeepSeek-V2.5-1210": "V2.5 系列最终公开 checkpoint；官方明确记录数学、代码、写作与角色扮演继续提升。",
    "DeepSeek-V3-0324": "替换线上 deepseek-chat 的 V3 主 checkpoint，显著增强推理、前端、工具调用、中文写作与搜索。",
    "DeepSeek-R1-0528": "替换线上 deepseek-reasoner 的 R1 主 checkpoint；投入更多后训练算力，并新增函数调用与 JSON 输出。",
    "ChatGLM": "首代中英双语对话 GLM，6.2B 参数，是 ChatGLM 系列公开演进的起点。",
    "ChatGLM2": "第二代 ChatGLM，以 1.4T 双语 tokens、32K context 和 MQA 改善能力与推理效率。",
    "GLM-5.3": "沿用 GLM-5.2 base，以 post-training 把复杂软件工程、长时程 agent 与网络安全能力继续推高；1M context、128K max output。",
    "GLM-5.3 Flash": "320B 总参数、18B 激活的原生多模态模型；混合稀疏/线性注意力、mHC 与 30T multimodal pretraining。",
    "Kimi K3": "2.8T 总参数、104B 激活，KDA + Attention Residuals、原生视觉与 1M context，面向长时程 coding 和知识工作。",
    "Kimi K2-Instruct-0905": "K2 的官方主 checkpoint 更新，提升 agentic coding、前端、上下文与工具任务表现。",
    "Kimi K2 Thinking": "K2 的正式 reasoning 更新，官方单独发布并接入通用推理与工具任务。",
    "Qwen3-Next": "80B/3B-active 超稀疏 MoE，以 Gated DeltaNet + Gated Attention 的 hybrid 架构预演 Qwen3.5。",
    "GPT-4 Turbo": "GPT-4 主系列的重要正式升级：128K context、更新知识截止时间，并显著降低 API 成本。",
    "GPT-5.3": "ChatGPT Instant 正代更新，官方模型目录保留独立 GPT-5.3 Chat 页面。",
    "Claude Sonnet 4.5": "2025-09 正式发布的 Sonnet 主模型，强化 coding、computer use 与长时程 agents。",
    "Claude Sonnet 4.6": "2026-02 正式发布的 Sonnet 主模型，升级 coding、computer use、长上下文和 agent planning。",
    "Qwen3.8-Flash-Next": "125B 主模型加 51B N-gram embeddings、每 token 激活 6B；QSA、Gated Residual 与 Muon 预演 Qwen4 架构。",
    "DeepSeek-V3.2-Exp": "在 V3.1-Terminus 上引入 DeepSeek Sparse Attention，是通往下一代架构的公开实验节点。",
    "DeepSeek-Math-V2": "基于 V3.2-Exp Base 的自验证数学推理模型，把 theorem proving、proof verification 与高难竞赛数学统一。",
    "Seed2.1": "Seed 官网列出的下一代真实生产力 agent 基座。",
    "SeedRealtime": "原生音视频全双工 LLM，联合理解音频、视觉与时间信息并进行低时延交互。",
    "Seed Audio 1.0": "端到端全场景音频生成模型，面向影视级声音创作。",
    "Seedance 2.5": "面向 30 秒叙事、精确参考控制与强编辑能力的新一代视频生成模型。",
    "Seedream 5.0 Pro": "带推理能力的多模态图像生成旗舰，面向专业内容创作。",
    "Seedream 5.0 Lite": "统一多模态图像生成模型，加入深度思考与在线搜索。",
    "Seed3D 2.0": "第二代 3D 生成基模，重点升级几何精度与材质质量。",
    "Seed GR-3": "面向长时程灵巧操作、强调泛化性的 vision-language-action 模型。",
    "GPT-5.6 Terra": "GPT-5.6 的能力—成本平衡层，保留 1.05M context 与统一工具能力。",
    "GPT-5.6 Luna": "GPT-5.6 的高吞吐低成本层，面向规模化工作负载。",
    "GPT-5.6 Cyber": "面向授权漏洞研究与安全测试的专业网络安全模型。",
    "Claude Opus 4.1": "Anthropic system-card 索引中的独立 Opus 更新，不能被 Claude 4 family 标签吞掉。",
    "Claude Mythos Preview": "Anthropic system-card 索引中的前沿能力预览模型。",
    "Gemini 3.7 Flash": "Google 当前最新 Flash，面向 coding、agentic workflows 与可靠多步执行。",
    "Gemini Omni Flash": "带原生音频的视频生成、编辑、关键帧插值与延展模型。",
    "Gemini Robotics-ER 1.6": "面向物理空间理解、仪表读取和多步机器人任务规划的 embodied reasoning 模型。",
}


def find_existing_mainline_dir(team_dir: str, date: str, model_name: str) -> Path | None:
    """Find the canonical pack, tolerating a corrected release month.

    Rich paper packs are sometimes filed by arXiv month rather than product
    release month.  Reuse that unique pack instead of creating a thin duplicate.
    """
    root = SOURCE / team_dir
    suffix = slugify(model_name).replace("-", "_").lower()
    canonical = root / f"{date}_{suffix}"
    if canonical.is_dir():
        return canonical
    if not root.is_dir():
        return None
    matches = []
    for candidate in root.iterdir():
        match = re.match(r"^\d{4}_(.+)$", candidate.name)
        if candidate.is_dir() and match and match.group(1).lower() == suffix:
            matches.append(candidate)
    return matches[0] if len(matches) == 1 else None


def ensure_audited_model_pack(team: dict, date: str, model: str, summary: str, url: str, branch: str | None) -> None:
    """Create the missing source clip, model note and poster without replacing user work."""
    folder = f"{date}_{slugify(model).replace('-', '_')}"
    if branch:
        assets = discover_branch_assets(team["dir"], model, date)
        model_dir = assets.get("dir") if assets else SOURCE / team["dir"] / "Variants" / folder
    else:
        # Mainline packs use an exact canonical directory. Fuzzy discovery can
        # otherwise confuse GLM-4.5 with GLM-4.5V or Qwen3 with Qwen3-Coder.
        model_dir = find_existing_mainline_dir(team["dir"], date, model) or SOURCE / team["dir"] / folder
    model_dir.mkdir(parents=True, exist_ok=True)
    src = model_dir / "src"
    src.mkdir(parents=True, exist_ok=True)

    fact = AUDITED_MODEL_FACTS.get(model, summary)
    source_clip = src / "Official Source.md"
    if not source_clip.exists():
        source_clip.write_text(
            f"# {model} — Official Source\n\n"
            f"- Official URL: {url}\n"
            f"- Publisher: {team['name']}\n"
            f"- Atlas release month: {pretty_date(date)}\n"
            f"- Retrieved: 2026-08-31\n\n"
            "## Verified claim snapshot\n\n"
            f"{fact}\n\n"
            "> This local clip records only claims attributable to the linked first-party source. "
            "Parameter counts or training details that are not public are intentionally left unstated.\n",
            encoding="utf-8",
        )

    existing_notes = sorted(model_dir.glob("*.md"))
    note = existing_notes[0] if existing_notes else model_dir / f"{model.replace(' ', '-').replace('/', '-')}.md"
    if not note.exists():
        branch_line = f"{branch} 支线" if branch else "主干正代"
        note.write_text(f'''---
title: "{model} — Model Overview"
type: model-note
year: {2000 + int(date[:2])}
url: "{url}"
tags: [model-note, base-model, {slugify(team['id'])}]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# {model} — Model Overview

> [!tldr]
> {fact}

## 谱系定位

- 团队：**{team['name']}**
- 时间：**{pretty_date(date)}**
- Atlas 归类：**{branch_line}**
- 一手证据：[{source_label(url)}]({url})

## 核心变化

{fact}

这个节点单独收录，是因为官方把它作为可独立识别的模型 / family 发布；同一 family 内的参数尺寸、服务档位和 dated API snapshot 不再重复拆叶子。

## 阅读判断

- 与前代比较时，优先看架构、数据、post-training 与工具环境四类变化。
- 官方未披露的参数、训练数据和消融不作推断。
- 若该节点是专项模型，应沿团队主干理解其能力迁移，而不是把它误写成新的通用正代。

## 一手资料

- [{url}]({url})
- [[src/Official Source|本地官方来源摘录]]

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
''', encoding="utf-8")

    posters = sorted(model_dir.glob("*poster*.html"))
    if not posters:
        poster = model_dir / f"{slugify(model).replace('-', '_')}_poster_zh.html"
        poster.write_text(render_poster(model, team["name"], fact, url, note.name), encoding="utf-8")


def add_missing_brainhao_packs() -> None:
    # Mainline audit: every visible numbered/mainline leaf has a local source
    # clip, note and poster before it is copied into the public atlas library.
    for team_id in ["deepseek", "zhipu", "kimi", "qwen", "seed", "openai", "anthropic", "google"]:
        team = next(t for t in TEAMS if t["id"] == team_id)
        for date, model, summary, url in team["models"]:
            ensure_audited_model_pack(team, date, model, summary, url, None)

    for team_dir, (folder, model, summary, url) in LATEST_PACKS.items():
        team = SOURCE / team_dir
        target = team / folder
        src = target / "src"
        src.mkdir(parents=True, exist_ok=True)
        source_clip = src / "Official Source.md"
        if not source_clip.exists():
            source_clip.write_text(f"# {model} — Official Source\n\n- URL: {url}\n- Retrieved for atlas: 2026-08-31\n- Scope: official release/model documentation used for the model overview.\n", encoding="utf-8")
        note = target / f"{model.replace(' ', '-').replace('/', '-')}.md"
        poster = target / f"{slugify(model).replace('-', '_')}_poster_zh.html"
        if not note.exists():
            note.write_text(f'''---
title: "{model} — Model Overview"
type: model-note
year: {2000 + int(folder[:2])}
url: "{url}"
tags: [model-note, base-model, {slugify(team_dir)}]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# {model} — Model Overview

> [!tldr]
> {summary}

## 定位

这是为补齐 Base Model Atlas 全球主干谱系而建立的模型概览。当前证据等级为 **{source_label(url)}**；只记录官方材料明确支持的产品定位与能力，不据此虚构训练细节。

## 核心变化

- {summary}
- 在团队谱系中的位置：当前旗舰或关键正代节点。
- 研究阅读重点：架构效率、agent/tool-use 训练、长上下文成本以及公开证据边界。

## 证据与限制

- 官方来源：[{url}]({url})
- 若官方未公开参数、训练数据或消融，本笔记不作推断。

## 导航

- [[Topics/13_base_model/Base Model MOC|Base Model MOC]]
- [[Topics/13_base_model/Base_Model_Global_Coverage_2026|Global Coverage]]
- [[{poster.stem}|中文 Poster]]
''', encoding="utf-8")
        if not poster.exists():
            poster.write_text(render_poster(model, team_dir, summary, url, note.name), encoding="utf-8")

        team_meta = next((t for t in TEAMS if t["dir"] == team_dir), None)
        series = team / f"{team_dir}-Series-Summary.md"
        if team_meta and not series.exists():
            timeline = "\n".join(
                f"| {pretty_date(d)} | {name} | {shift} | [{source_label(source)}]({source}) |"
                for d, name, shift, source in team_meta["models"]
            )
            series.write_text(f'''---
title: "{team_meta['name']} — Series Summary"
type: model-note
tags: [model-note, base-model, series, {slugify(team_dir)}]
created: 2026-08-31
updated: 2026-08-31
---

# {team_meta['name']} — Series Summary

> [!tldr]
> {team_meta['thesis']}

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
{timeline}

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[{folder}/{note.stem}|{model}]]。
''', encoding="utf-8")

    # Keep MedXIAOHE as an ordinary named model in the Seed ecosystem.
    med_dir = SOURCE / "ByteDance_Seed/Variants/2602_MedXIAOHE"
    med_src = med_dir / "src"
    med_src.mkdir(parents=True, exist_ok=True)
    med_note = med_dir / "MedXIAOHE.md"
    med_poster = med_dir / "MedXIAOHE_poster_zh.html"
    med_url = "https://arxiv.org/abs/2602.12705"
    if not (med_src / "Official Source.md").exists():
        (med_src / "Official Source.md").write_text(
            "# MedXIAOHE — Official Source\n\n"
            f"- Technical report: {med_url}\n"
            "- Team: ByteDance XiaoHe Medical AI\n"
            "- Atlas placement: ByteDance · Seed\n"
            "- Retrieved: 2026-08-31\n",
            encoding="utf-8",
        )
    if not med_note.exists():
        med_note.write_text(f'''---
title: "MedXIAOHE — Medical MLLM Overview"
type: model-note
authors: ["ByteDance XiaoHe Medical AI", "et al."]
year: 2026
arxiv: "2602.12705"
url: "{med_url}"
tags: [model-note, base-model, seed, medical, multimodal]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# MedXIAOHE — Medical MLLM Overview

> [!tldr]
> MedXIAOHE 收录在 **ByteDance · Seed** 模型时间线中；这里概括其数据、训练与评测方法。

## 定位

MedXIAOHE 面向医疗多模态理解和长报告生成，重点不是单一 benchmark 冲分，而是把数据构建、偏好准则、证据约束推理与低幻觉长文本生成串成可复现流程。

## 方法与研究价值

- 通过医疗图文数据治理与多阶段训练建立领域能力。
- 引入用户偏好 rubric 与 evidence-grounded reasoning，强调真实医疗指令的可用性。
- 将低幻觉长报告生成视为核心交付，而不是只评短答案准确率。

> [!insight]
> 对 agent training 的启发是：高风险垂直领域不能只靠通用 RL reward；需要把证据引用、偏好 rubric、长报告结构和幻觉惩罚共同写进 verifier 与训练数据闭环。

## 证据边界

- 技术报告：[{med_url}]({med_url})
- 归属口径：Atlas 将其作为 ByteDance · Seed 生态中的一个普通模型节点收录。

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
- [[MedXIAOHE_poster_zh|中文 Poster]]
''', encoding="utf-8")
    if not med_poster.exists():
        med_poster.write_text(render_poster(
            "MedXIAOHE", "ByteDance · Seed",
            "医疗多模态训练 recipe：数据治理、偏好准则、证据约束推理与低幻觉长报告生成。",
            med_url, med_note.name,
        ), encoding="utf-8")

    audit = SOURCE / "Base_Model_Top8_Branch_Audit_2026.md"
    rows = []
    for team_id in ["deepseek", "zhipu", "kimi", "qwen", "seed", "openai", "anthropic", "google"]:
        team = next(t for t in TEAMS if t["id"] == team_id)
        branch_text = "；".join(f"**{b['name']}**：{b['models']}" for b in VARIANT_FAMILIES[team_id])
        rows.append(f"| {team['name']} | {team['models'][-1][1]} | {branch_text} |")
    audit.write_text(f'''---
title: "Base Model Top 8 Branch Audit — 2026-08"
type: insight
tags: [insight, base-model, coverage, variants, top8]
source: "[[Topics/13_base_model/Base Model MOC]]"
created: 2026-08-31
updated: 2026-08-31
---

# Base Model Top 8 Branch Audit — 2026-08

> [!tldr]
> 本审计把国内 Top 5（DeepSeek、GLM、Kimi、Qwen、Seed）和海外 Top 3（GPT、Claude、Gemini）拆成“通用主干正代 + 专项/模态支线”。主干只放跨代旗舰，Coder、Vision、Speech、Robotics、Medical 等单列，避免把 SKU、尺寸和 API snapshot 混成代际。

## 审计总表

| 团队 | 当前主干节点 | 已核对支线 |
|---|---|---|
{chr(10).join(rows)}

## 关键补漏判断

- **DeepSeek**：本地此前几乎只有 V4-Pro；谱系不能因此漏掉 R1、Coder、Math/Prover、VL/Janus 与 OCR 支线。
- **GLM**：已有 4.5V、TTS、OCR，但应把 CogVLM/CodeGeeX/CogView/CogVideoX/AutoGLM 作为历史支系写入地图。
- **Kimi**：已有 VL、K2、Linear、K2.5；缺口主要是 Kimi-Audio、Kimi-Dev 与 Kimina-Prover。
- **Qwen**：本地 Variants 覆盖最完整；需要保持 Coder、VL/VLA、Omni/ASR/TTS、Image、Retrieval 与 Guard 的分支关系。
- **Seed**：除 Seed1.8/2.0 外，必须补 Seed1.5-VL、Seed-OSS/Code、BAGEL、Seed-TTS、Seedream/Seedance、Seed3D 与 MedXIAOHE。
- **GPT**：除 GPT 正代，还要单列 o-series、Codex、gpt-oss、Realtime/Audio、Image/Cyber；这些不应伪装成 GPT 主干新代。
- **Claude**：Haiku/Sonnet/Opus 是能力—成本层；extended thinking、computer use 是能力支线，Claude Code 是产品/agent，不是独立基模。
- **Gemini**：Pro/Flash/Flash-Lite/Nano 是服务层；Deep Think、Computer Use、Audio/Live、Image/Omni、Robotics 是支线；Gemma 是同团队开放 sibling family。

## 一手证据入口

- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [Anthropic system cards](https://www.anthropic.com/system-cards)
- [Google DeepMind model cards](https://deepmind.google/models/model-cards/)
- [DeepSeek changelog](https://api-docs.deepseek.com/updates/)
- [Z.ai model overview](https://docs.z.ai/guides/overview/overview)
- [Moonshot AI official repositories](https://github.com/MoonshotAI)
- [Qwen official blog](https://qwenlm.github.io/blog/)
- [ByteDance Seed official repositories](https://github.com/ByteDance-Seed)
- [MedXIAOHE technical report]({med_url})
''', encoding="utf-8")

    coverage = SOURCE / "Base_Model_Global_Coverage_2026.md"
    if not coverage.exists():
        rows = "\n".join(
            f"| {t['region']} | {t['name']} | {len(t['models'])} | {t['models'][-1][1]} | {t['thesis']} |"
            for t in TEAMS
        )
        coverage.write_text(f'''---
title: "Global Base Model Coverage — 2026-08"
type: insight
tags: [insight, base-model, coverage, timeline]
source: "[[Topics/13_base_model/Base Model MOC]]"
created: 2026-08-31
updated: 2026-08-31
---

# Global Base Model Coverage — 2026-08

> [!tldr]
> 本轮将 Base Model topic 从 15 个已有团队扩为 **22 个厂商团队 + 1 个 research-agent 团队**。这里的“完整”指**团队级主干正代覆盖**，不等于收录每个 API snapshot、参数尺寸、Turbo/Max/Flash SKU 或所有专项模型。

## 编辑口径

- 主树：通用基模正代、团队公认旗舰、改变训练/架构范式的关键节点。
- 支线：Coder、Embedding、ASR/TTS、Robotics、Guard、Image/Video 等进入 Variants 或对应专题。
- 证据：优先 technical report / model card，其次 system card / official docs / official blog。
- 页面：每个叶子都有 overview；已有精读笔记与 Poster 则继续深链，没有则明确标注资料状态。

## 团队覆盖

| 区域 | 团队 | 主干节点 | 当前节点 | 一句话判断 |
|---|---|---:|---|---|
{rows}

## 本轮新增的 P0/P1 团队

DeepSeek、xAI、Mistral、Tencent Hunyuan、Amazon Nova、NVIDIA Nemotron、Cohere Command、IBM Granite、Microsoft Phi；并补齐 Anthropic Claude Opus 5 与 OpenAI GPT-5.6 当前节点。

## 仍不应声称“全收录”的边界

- 未把每个尺寸、服务层、dated API snapshot 拆成独立叶子。
- 华为盘古、商汤日日新等公开一手技术材料不足或产品口径难以稳定映射到独立主干正代，暂列候补，不混入已核验主树。
- 专项生成模型与 physical/world models 不属于本轮通用基模主树。
''', encoding="utf-8")


def render_poster(model: str, team: str, summary: str, url: str, note_name: str) -> str:
    return f'''<!-- index: {html.escape(model)} 中文概览 | 2026-08-31 | Base Model Atlas 补齐页 -->
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(model)} · 中文概览</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#0b0e16;color:#edf3ff;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh;display:grid;place-items:center;padding:28px}}main{{width:min(1080px,100%);background:radial-gradient(circle at 82% 12%,rgba(124,92,255,.24),transparent 34%),linear-gradient(145deg,#141a29,#0f131e);border:1px solid #2a3550;border-radius:28px;padding:clamp(28px,6vw,72px);box-shadow:0 32px 90px #0008}}.eyebrow{{color:#8ee6ff;letter-spacing:.16em;text-transform:uppercase;font-weight:750}}h1{{font-size:clamp(44px,8vw,92px);line-height:.94;margin:18px 0 22px;letter-spacing:-.055em}}.lead{{font-size:clamp(19px,2.5vw,30px);line-height:1.45;color:#cbd6ec;max-width:850px}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:46px 0}}.card{{padding:22px;border-radius:18px;background:#ffffff08;border:1px solid #ffffff16}}.k{{font-size:12px;letter-spacing:.13em;color:#8391aa;text-transform:uppercase}}.v{{font-size:19px;font-weight:720;margin-top:10px}}a{{color:#9bdcff;text-decoration:none}}.actions{{display:flex;gap:12px;flex-wrap:wrap}}.btn{{display:inline-block;padding:12px 16px;border-radius:999px;border:1px solid #3b4967;background:#111827}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><main><div class="eyebrow">Base Model Atlas · {html.escape(team)}</div><h1>{html.escape(model)}</h1><p class="lead">{html.escape(summary)}</p><section class="grid"><div class="card"><div class="k">资料层级</div><div class="v">模型概览</div></div><div class="card"><div class="k">证据等级</div><div class="v">{html.escape(source_label(url))}</div></div><div class="card"><div class="k">更新时间</div><div class="v">2026-08-31</div></div></section><div class="actions"><a class="btn" href="{html.escape(url)}">官方来源 ↗</a><a class="btn" href="{quote(note_name)}">阅读笔记</a></div></main></body></html>'''


def discover_assets(team_dir: str, model_name: str, date: str, folder: str | None = None) -> dict:
    root = SOURCE / team_dir
    if not root.exists(): return {}
    if folder:
        model_dir = root / folder
        if not model_dir.is_dir(): return {}
        notes = sorted(f for f in model_dir.glob("*.md") if f.is_file())
        posters = sorted(f for f in model_dir.glob("*poster*.html") if f.is_file())
        return {"dir": model_dir, "note": notes[0] if notes else None, "posters": posters}
    candidates = []
    for d in root.iterdir():
        if not d.is_dir() or d.name in {"src", "Variants"}: continue
        # A family token alone (for example "Llama") is not enough evidence
        # that a Llama 4 poster belongs to Llama 1. Date alignment is required
        # so the atlas never overstates per-generation reading coverage.
        if not d.name.startswith(date):
            continue
        score = 4
        tokens = [x for x in re.split(r"[^a-z0-9]+", model_name.lower()) if len(x) > 1]
        dn = d.name.lower().replace("_", "-")
        score += sum(1 for token in tokens if token in dn)
        candidates.append((score, -len(d.name), d))
    if not candidates: return {}
    model_dir = sorted(candidates, key=lambda x:(x[0], x[1]), reverse=True)[0][2]
    notes = sorted(f for f in model_dir.glob("*.md") if f.is_file())
    posters = sorted(f for f in model_dir.glob("*poster*.html") if f.is_file())
    return {"dir": model_dir, "note": notes[0] if notes else None, "posters": posters}


def discover_mainline_assets(team_dir: str, model_name: str, date: str, folder: str | None = None) -> dict:
    """Prefer the exact canonical generation folder before fuzzy legacy matching."""
    if folder:
        return discover_assets(team_dir, model_name, date, folder)
    exact = find_existing_mainline_dir(team_dir, date, model_name)
    if exact is None:
        return discover_assets(team_dir, model_name, date)
    if exact.is_dir():
        notes = sorted(f for f in exact.glob("*.md") if f.is_file())
        posters = sorted(f for f in exact.glob("*poster*.html") if f.is_file())
        return {"dir": exact, "note": notes[0] if notes else None, "posters": posters}
    return {}


def apply_asset_overrides(assets: dict, model_name: str, item: dict) -> dict:
    """Select model-specific files when several sibling SKUs share one family folder."""
    model_dir = assets.get("dir")
    if not model_dir:
        return assets
    override = {**MODEL_ASSET_OVERRIDES.get(model_name, {}), **item}
    note_name = override.get("assetNote")
    poster_names = override.get("assetPosters")
    if note_name:
        note = model_dir / note_name
        if not note.is_file():
            raise FileNotFoundError(f"Missing pinned note for {model_name}: {note}")
        assets["note"] = note
    if poster_names:
        posters = [model_dir / name for name in poster_names]
        missing = [str(poster) for poster in posters if not poster.is_file()]
        if missing:
            raise FileNotFoundError(f"Missing pinned poster for {model_name}: {missing}")
        assets["posters"] = posters
    return assets


def discover_branch_assets(team_dir: str, model_name: str, date: str) -> dict:
    """Match branch material only when a distinctive model token agrees."""
    root = SOURCE / team_dir
    if not root.exists():
        return {}
    generic = {"gpt", "glm", "kimi", "qwen", "gemini", "claude", "deepseek", "seed", "model", "preview"}
    wanted = {x for x in re.split(r"[^a-z0-9]+", model_name.lower()) if len(x) >= 3 and x not in generic}
    candidates = []
    dirs = [d for d in root.iterdir() if d.is_dir() and d.name not in {"src", "Variants"}]
    variants = root / "Variants"
    if variants.is_dir():
        dirs.extend(d for d in variants.iterdir() if d.is_dir())
    for d in dirs:
        if not d.name.startswith(date):
            continue
        present = {x for x in re.split(r"[^a-z0-9]+", d.name.lower()) if len(x) >= 3 and x not in generic}
        overlap = wanted & present
        if overlap:
            candidates.append((len(overlap), -len(d.name), d))
    if not candidates:
        return {}
    model_dir = sorted(candidates, reverse=True)[0][2]
    notes = sorted(f for f in model_dir.glob("*.md") if f.is_file())
    posters = sorted(f for f in model_dir.glob("*poster*.html") if f.is_file())
    return {"dir": model_dir, "note": notes[0] if notes else None, "posters": posters}


def copy_file_with_refs(source_file: Path, destination: Path, model_root: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, destination)
    if source_file.suffix.lower() not in {".html", ".md"}: return
    content = source_file.read_text(encoding="utf-8", errors="ignore")
    rewritten = content
    refs = re.findall(r'''(?:src|href)=["']([^"'#?]+)|url\(["']?([^"')]+)|!\[[^\]]*\]\(([^)#?]+)|!\[\[([^\]|#]+)''', content, re.I)
    for pair in refs:
        ref = next((x for x in pair if x), "").strip()
        if not ref or re.match(r"^(?:https?:|data:|javascript:|mailto:)", ref): continue
        candidate = (source_file.parent / ref).resolve()
        try: rel = candidate.relative_to(model_root.resolve())
        except ValueError: continue
        if candidate.is_file():
            out = destination.parent / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, out)
        else:
            # A handful of legacy posters already reference assets that are no
            # longer present in BrainHao. Hide those broken controls/images in
            # the published copy while leaving the source vault untouched.
            escaped = re.escape(ref)
            rewritten = re.sub(
                rf'''src=(["']){escaped}\1''',
                'src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="',
                rewritten,
                flags=re.I,
            )
            rewritten = re.sub(rf'''href=(["']){escaped}\1''', 'href="#"', rewritten, flags=re.I)
    # Published notes are rendered beside the originals; poster/note navigation
    # should always open the HTML reading view rather than raw Markdown.
    rewritten = re.sub(r'''href=(["'])([^"']+?)\.md(?:#[^"']*)?\1''', r'href=\1\2.html\1', rewritten, flags=re.I)
    if rewritten != content:
        destination.write_text(rewritten, encoding="utf-8")


def note_targets() -> dict[str, Path]:
    """Resolve Obsidian wikilinks to their rendered archive HTML page."""
    targets: dict[str, Path] = {}
    for note in SOURCE.rglob("*.md"):
        rel_parts = note.relative_to(SOURCE).parts
        if "src" in rel_parts or "QA" in rel_parts:
            continue
        rel = note.relative_to(SOURCE).with_suffix(".html")
        target = ATLAS / "archive" / rel
        keys = {note.stem, str(note.relative_to(SOURCE).with_suffix("")), str(note.relative_to(BRAINHAO).with_suffix(""))}
        for key in keys:
            targets.setdefault(key.replace("\\", "/"), target)
    return targets


def render_inline_md(text: str, destination: Path, targets: dict[str, Path]) -> str:
    tokens: list[str] = []
    def hold(value: str) -> str:
        tokens.append(value)
        return f"\x00{len(tokens)-1}\x00"

    # Preserve inline code before escaping the remaining prose.
    text = re.sub(r"`([^`]+)`", lambda m: hold(f"<code>{html.escape(m.group(1))}</code>"), text)
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: hold(f'<img src="{html.escape(m.group(2), quote=True)}" alt="{html.escape(m.group(1), quote=True)}">'), text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: hold(f'<a href="{html.escape(m.group(2), quote=True)}" target="_blank" rel="noopener">{m.group(1)}</a>'), text)
    def local_link(m: re.Match[str]) -> str:
        label, href = m.group(1), html.unescape(m.group(2)).strip()
        if Path(href.split("#", 1)[0]).suffix.lower() == ".md":
            path, marker, anchor = href.partition("#")
            href = path + ".html" + (marker + anchor if marker else "")
        return hold(f'<a href="{html.escape(href, quote=True)}">{label}</a>')
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", local_link, text)

    def wiki(m: re.Match[str]) -> str:
        raw = html.unescape(m.group(1))
        target, _, alias = raw.partition("|")
        target = target.split("#", 1)[0].strip()
        label = alias.strip() or Path(target).name
        resolved = targets.get(target) or targets.get(Path(target).name)
        if resolved:
            href = os.path.relpath(resolved, destination.parent).replace(os.sep, "/")
            return hold(f'<a class="wikilink" href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')
        if target.startswith("src/") and "/deepseek/" in destination.as_posix():
            source_target = Path(target)
            if source_target.suffix.lower() == ".md":
                href = str(source_target) + ".html"
            elif source_target.suffix:
                href = str(source_target)
            else:
                href = "Sources.html#" + slugify(source_target.name)
            return hold(f'<a class="wikilink" href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')
        if target.startswith("Topics/13_base_model/") and target.endswith(".html"):
            archive_target = ATLAS / "archive" / Path(target).relative_to("Topics/13_base_model")
            href = os.path.relpath(archive_target, destination.parent).replace(os.sep, "/")
            return hold(f'<a class="wikilink" href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')
        return hold(f'<span class="wikilink unresolved">{html.escape(label)}</span>')

    text = re.sub(r"\[\[([^\]]+)\]\]", wiki, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)
    for i, value in enumerate(tokens):
        text = text.replace(f"\x00{i}\x00", value)
    return text


def render_markdown(source_file: Path, destination: Path, targets: dict[str, Path]) -> None:
    """Render the practical Obsidian subset used by BrainHao notes."""
    raw = source_file.read_text(encoding="utf-8", errors="ignore")
    original_raw = raw
    meta: dict[str, str] = {}
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        if end != -1:
            for line in raw[4:end].splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip().strip('"')
            raw = raw[end + 5:]
    # Hugging Face model cards commonly mix Markdown with centered HTML badge
    # blocks.  Normalize those blocks before the Obsidian-style renderer so
    # readers see the actual card instead of escaped <div>/<img> source text.
    hf_asset_base = ""
    if "huggingface_model_cards" in source_file.parts:
        repo = source_file.stem
        hf_asset_base = f"https://huggingface.co/deepseek-ai/{repo}/resolve/main/"
    elif source_file.name == "hf_model_card.md":
        manifest = source_file.parent / "retrieval_manifest.json"
        if manifest.is_file():
            try:
                raw_url = json.loads(manifest.read_text(encoding="utf-8"))["documents"]["hf_model_card.md"]["url"]
                hf_asset_base = raw_url.replace("/raw/main/README.md", "/resolve/main/")
            except (KeyError, TypeError, json.JSONDecodeError):
                pass
    if hf_asset_base:
        raw = re.sub(
            r'(<img\b[^>]*?\bsrc=["\'])(?!https?://|data:|/)([^"\']+)',
            lambda match: match.group(1) + hf_asset_base + match.group(2),
            raw,
            flags=re.I,
        )
        raw = re.sub(
            r'(!\[[^\]]*\]\()(?!https?://|data:|/)([^)]+)',
            lambda match: match.group(1) + hf_asset_base + match.group(2),
            raw,
        )
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    def html_image(match: re.Match[str]) -> str:
        attrs = match.group(1)
        src_match = re.search(r'\bsrc=["\']([^"\']+)', attrs, re.I)
        if not src_match:
            return ""
        alt_match = re.search(r'\balt=["\']([^"\']*)', attrs, re.I)
        return f"![{alt_match.group(1) if alt_match else ''}]({src_match.group(1)})"
    raw = re.sub(r"<img\b([^>]*?)/?>", html_image, raw, flags=re.I)
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"<hr\s*/?>", "\n---\n", raw, flags=re.I)
    raw = re.sub(r"</?(?:div|p|a|span|details|summary)[^>]*>", "", raw, flags=re.I)
    lines = raw.splitlines()
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if line.startswith("```"):
            lang = line[3:].strip()
            code: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            out.append(f'<pre><div class="code-lang">{html.escape(lang or "code")}</div><code>{html.escape(chr(10).join(code))}</code></pre>')
            continue
        hm = re.match(r"^(#{1,6})\s+(.+)$", line)
        if hm:
            level = len(hm.group(1)); title = re.sub(r"[*_`]", "", hm.group(2)).strip()
            anchor = slugify(title)
            if anchor == "model":
                anchor = f"section-{len(toc)+1}"
            used = {a for _,_,a in toc}
            base_anchor = anchor
            suffix = 2
            while anchor in used:
                anchor = f"{base_anchor}-{suffix}"; suffix += 1
            toc.append((level, title, anchor))
            out.append(f'<h{level} id="{anchor}">{render_inline_md(hm.group(2), destination, targets)}</h{level}>')
            i += 1; continue
        if line.startswith("> [!"):
            cm = re.match(r"> \[!([^\]]+)\][+-]?\s*(.*)", line)
            kind = (cm.group(1) if cm else "note").lower()
            title = (cm.group(2) if cm and cm.group(2) else kind.upper())
            body: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith(">") or not lines[i].strip()):
                if lines[i].startswith(">"):
                    body.append(lines[i][1:].lstrip())
                i += 1
            content = " ".join(render_inline_md(x, destination, targets) for x in body if x)
            out.append(f'<aside class="callout {html.escape(kind)}"><div class="callout-title">{html.escape(title)}</div><div>{content}</div></aside>')
            continue
        if line.startswith(">"):
            body=[]
            while i < len(lines) and lines[i].startswith(">"):
                body.append(lines[i][1:].lstrip()); i += 1
            out.append(f'<blockquote>{"<br>".join(render_inline_md(x,destination,targets) for x in body)}</blockquote>')
            continue
        if i + 1 < len(lines) and "|" in line and re.match(r"^\s*\|?\s*:?-{3,}", lines[i+1]):
            headers=[x.strip() for x in line.strip().strip("|").split("|")]
            i += 2; rows=[]
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([x.strip() for x in lines[i].strip().strip("|").split("|")]); i += 1
            head="".join(f"<th>{render_inline_md(x,destination,targets)}</th>" for x in headers)
            body="".join("<tr>"+"".join(f"<td>{render_inline_md(x,destination,targets)}</td>" for x in row)+"</tr>" for row in rows)
            out.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        lm = re.match(r"^\s*([-*+] |\d+\. )(.+)$", line)
        if lm:
            ordered = lm.group(1)[0].isdigit(); items=[]
            while i < len(lines):
                im = re.match(r"^\s*([-*+] |\d+\. )(.+)$", lines[i])
                if not im or im.group(1)[0].isdigit() != ordered: break
                items.append(im.group(2)); i += 1
            tag="ol" if ordered else "ul"
            out.append(f'<{tag}>'+"".join(f"<li>{render_inline_md(x,destination,targets)}</li>" for x in items)+f'</{tag}>')
            continue
        paragraph=[line.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6})\s|^```|^>|^\s*([-*+] |\d+\. )", lines[i]):
            if i + 1 < len(lines) and "|" in lines[i] and re.match(r"^\s*\|?\s*:?-{3,}", lines[i+1]): break
            paragraph.append(lines[i].strip()); i += 1
        out.append(f'<p>{render_inline_md(" ".join(paragraph),destination,targets)}</p>')

    title = meta.get("title") or next((t for level,t,_ in toc if level == 1), source_file.stem)
    toc_html = "".join(f'<a class="toc-l{level}" href="#{anchor}">{html.escape(text)}</a>' for level,text,anchor in toc if level <= 3)
    tags = meta.get("tags", "").strip("[]")
    note_html = ''.join(out)
    # Older short/image-less model notes must not silently look "finished" in
    # the public library. Explicitly annotated notes own their status; the
    # renderer marks the rest until their official sources and figures exist.
    domestic_focus_dirs = {"DeepSeek_AI", "Zhipu_GLM", "Moonshot_Kimi", "Alibaba_Qwen", "ByteDance_Seed"}
    is_model_note = (
        meta.get("type") in {"model-note", "model-family", "paper"}
        and "src" not in source_file.parts
        and source_file.is_relative_to(SOURCE)
        and any(part in domestic_focus_dirs for part in source_file.parts)
    )
    # Frontmatter alone is not enough: the reader must see the qualification.
    has_explicit_status = "资料充分度" in original_raw
    image_count = len(re.findall(r"!\[[^\]]*\]\([^)]+\)|<img\b", original_raw, flags=re.I))
    evidence_units = len(re.findall(r"[\u4e00-\u9fff]|[A-Za-z0-9]+", raw))
    if is_model_note and not has_explicit_status and (image_count == 0 or evidence_units < 1800):
        missing: list[str] = []
        if image_count == 0:
            missing.append("缺少已本地化的官方图片")
        if evidence_units < 1800:
            missing.append("现有一手资料归档或逐项精读的证据密度不足")
        quality_banner = (
            '<aside class="callout warning quality-warning" style="--accent:#f59e0b;background:#f59e0b14">'
            '<div class="callout-title" style="color:#fbbf24">质量状态：未达到完整精读标准</div>'
            f'<div>当前页面尚不能按完整笔记验收：{"；".join(missing)}。'
            '这不是完整结论页；需要补齐官方 model card / technical report / 发布图，并完成模型特有的架构、训练、评测与证据边界分析后再移除此标记。</div>'
            '</aside>'
        )
        h1_end = note_html.find("</h1>")
        if h1_end >= 0:
            h1_end += len("</h1>")
            note_html = note_html[:h1_end] + quality_banner + note_html[h1_end:]
        else:
            note_html = quality_banner + note_html
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · BrainHao</title><style>{NOTE_CSS}</style></head><body><div class="app"><aside class="rail"><a class="back" href="{os.path.relpath(ATLAS / 'library.html', destination.parent).replace(os.sep,'/')}">← 资料馆</a><div class="vault">BRAINHAO / NOTE</div><h2>{html.escape(title)}</h2><div class="meta">{html.escape(meta.get('type','note'))} · {html.escape(meta.get('year',''))}<br>{html.escape(tags)}</div><nav>{toc_html}</nav></aside><main class="note">{note_html}</main></div></body></html>''', encoding="utf-8")


NOTE_CSS = r'''
:root{--bg:#0b0d12;--panel:#11151d;--line:#283244;--text:#e8edf6;--muted:#8d99ad;--accent:#a78bfa}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 70% -15%,#4338ca2b,transparent 34%),var(--bg);color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.app{max-width:1320px;margin:auto;display:grid;grid-template-columns:290px minmax(0,820px);gap:56px;padding:42px 28px 100px}.rail{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;padding:24px;border:1px solid var(--line);border-radius:20px;background:#11151dcc}.back,.rail nav a{display:block;color:#aeb9ca;text-decoration:none}.vault{font-size:10px;letter-spacing:.18em;color:#8ab4ff;margin:34px 0 12px}.rail h2{font-size:20px;line-height:1.3;margin:0 0 12px}.meta{font-size:11px;line-height:1.7;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:16px}.rail nav a{font-size:12px;padding:6px 0}.rail nav .toc-l3{padding-left:12px;color:#748096}.note{min-width:0;font-family:ui-serif,"Source Han Serif SC","Noto Serif CJK SC",Georgia,serif;font-size:17px;line-height:1.86}.note h1,.note h2,.note h3,.note h4{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:-.025em;scroll-margin-top:24px}.note h1{font-size:clamp(42px,7vw,72px);line-height:1.05;margin:16px 0 42px}.note h2{font-size:30px;margin:58px 0 18px;padding-bottom:10px;border-bottom:1px solid var(--line)}.note h3{font-size:22px;margin:38px 0 12px}.note p{margin:16px 0}.note a{color:#9db7ff;text-decoration:none;border-bottom:1px solid #9db7ff55}.wikilink{font-family:Inter,sans-serif;color:#b9a4ff!important}.unresolved{opacity:.72}.callout{margin:24px 0;padding:18px 20px;border-left:4px solid var(--accent);border-radius:0 14px 14px 0;background:#a78bfa12;font-family:Inter,sans-serif;font-size:15px}.callout-title{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#c4b5fd;margin-bottom:8px}.callout.insight{--accent:#2dd4bf;background:#2dd4bf12}.callout.tldr{--accent:#60a5fa;background:#60a5fa12}blockquote{margin:20px 0;padding:8px 20px;color:#b9c2d1;border-left:2px solid #475569}pre{position:relative;background:#0a0d13;border:1px solid #252e3e;border-radius:14px;padding:38px 18px 18px;overflow:auto;font-size:13px;line-height:1.65}.code-lang{position:absolute;top:10px;right:14px;color:#68758a;font-family:Inter,sans-serif;font-size:10px;text-transform:uppercase}.note code{font-family:"SFMono-Regular",Consolas,monospace}.note p code,.note li code{background:#202737;padding:2px 6px;border-radius:5px;font-size:.84em}.note img{max-width:100%;height:auto;border-radius:14px;border:1px solid var(--line)}.table-wrap{overflow:auto;margin:24px 0;border:1px solid var(--line);border-radius:14px}table{border-collapse:collapse;width:100%;font-family:Inter,sans-serif;font-size:13px}th,td{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#171d28;color:#cdd6e5}tr:last-child td{border-bottom:0}li{margin:7px 0}@media(max-width:900px){.app{grid-template-columns:1fr;padding:20px;gap:28px}.rail{position:relative;top:0;max-height:none}.rail nav{display:none}.note{font-size:16px}}
'''


def sync_source_archive(
    model_root: Path,
    dest_root: Path,
    targets: dict[str, Path],
    include_relative: set[Path] | None = None,
) -> dict | None:
    """Publish a model's auditable first-party archive and a readable index."""
    source_root = model_root / "src"
    if not source_root.is_dir():
        return None
    destination_root = dest_root / "src"
    destination_root.mkdir(parents=True, exist_ok=True)
    rows = []
    source_docs = []
    sources = (p for p in source_root.rglob("*") if p.is_file())
    if include_relative is not None:
        sources = (p for p in sources if p.relative_to(source_root) in include_relative)
    for source in sorted(sources, key=lambda p: str(p).lower()):
        rel = source.relative_to(source_root)
        destination = destination_root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        published = destination
        kind = source.suffix.lower().lstrip(".") or "file"
        if source.suffix.lower() == ".md":
            published = Path(str(destination) + ".html")
            stale_render = destination.with_suffix(".html")
            raw_html_peer = source.with_suffix(".html")
            if stale_render != published and stale_render.exists() and not raw_html_peer.is_file():
                stale_render.unlink()
            render_markdown(source, published, targets)
            kind = "markdown · rendered"
        href = quote(os.path.relpath(published, dest_root).replace(os.sep, "/"), safe="/#?=&")
        rows.append(
            f'<tr id="{slugify(rel.parent.name or rel.stem)}"><td><a href="{html.escape(href, quote=True)}">{html.escape(str(rel))}</a></td>'
            f'<td>{html.escape(kind)}</td><td>{source.stat().st_size:,} B</td></tr>'
        )
        selectable_model_card = rel.parts and rel.parts[0] == "huggingface_model_cards"
        selectable_repo_metadata = rel.parts and rel.parts[0] == "huggingface_repository_metadata"
        if (rel.parent == Path(".") or selectable_model_card or selectable_repo_metadata) and source.name != "Official Source.md":
            if source.name == "hf_model_card.md":
                label = "Hugging Face Model Card · 官方主卡"
            elif selectable_model_card:
                label = f"HF · {source.stem}"
            else:
                label = source.stem.replace("official_", "").replace("_", " ").title()
            if source.suffix.lower() == ".md":
                source_docs.append({
                    "label": f"{label} · Markdown 阅读版",
                    "path": str(published.relative_to(ATLAS)),
                    "kind": "hf-model-card" if selectable_model_card or source.name == "hf_model_card.md" else "readable",
                    "name": source.name,
                })
            elif source.suffix.lower() == ".pdf":
                source_docs.append({
                    "label": f"{label} · PDF",
                    "path": str(published.relative_to(ATLAS)),
                    "kind": "pdf",
                    "name": source.name,
                })
            elif source.suffix.lower() == ".html":
                source_docs.append({
                    "label": f"{label} · 原始 HTML",
                    "path": str(published.relative_to(ATLAS)),
                    "kind": "raw-html",
                    "name": source.name,
                })
            elif source.suffix.lower() == ".json" and selectable_repo_metadata:
                source_docs.append({
                    "label": f"HF · {source.stem} · 官方仓库元数据",
                    "path": str(published.relative_to(ATLAS)),
                    "kind": "hf-repository-metadata",
                    "name": source.name,
                })
    if not rows:
        return None
    index = dest_root / "Sources.html"
    index.write_text(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DeepSeek 一手资料包</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#07111c;color:#eaf4ff;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:34px}}main{{max-width:1120px;margin:auto}}a{{color:#7dd3fc;text-decoration:none}}.back{{display:inline-block;margin-bottom:28px}}h1{{font-size:clamp(40px,7vw,74px);letter-spacing:-.05em;margin:0 0 12px}}.lead{{color:#9db2c3;line-height:1.7;max-width:820px}}.box{{margin-top:30px;overflow:auto;border:1px solid #20415a;border-radius:18px;background:#0b1b29}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{padding:13px 16px;border-bottom:1px solid #18374c;text-align:left;vertical-align:top}}th{{color:#78d7ec;background:#0d2435;position:sticky;top:0}}tr:last-child td{{border:0}}code{{color:#a7c5d8}}@media(max-width:700px){{body{{padding:20px 12px}}}}
</style></head><body><main><a class="back" href="javascript:history.back()">← 返回模型 Overview</a><h1>一手资料包</h1><p class="lead">这里发布 BrainHao 中保存的 DeepSeek 官方网页、模型卡、技术报告与可获得的论文源码。原始文件保留不改写；Markdown 另提供阅读版 HTML。来源 URL、抓取日期、字节数与 SHA-256 见 <a href="src/retrieval_manifest.json">retrieval_manifest.json</a>。</p><div class="box"><table><thead><tr><th>本地文件</th><th>格式</th><th>大小</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></main></body></html>''', encoding="utf-8")
    priorities = {
        "hf_model_card.md": 0,
        "official_pro_model_card.md": 1,
        "official_model_card.md": 2,
        "official_flash_model_card.md": 3,
        "official_readme.md": 4,
        "technical_report.pdf": 5,
        "official_ga_release.md": 20,
        "official_release.md": 21,
        "official_preview_release.md": 22,
        "official_ga_release.html": 20,
        "official_release.html": 31,
        "official_preview_release.html": 32,
    }
    source_docs.sort(key=lambda item: (
        priorities.get(item["name"], 10 if item["kind"] == "hf-model-card" else 50),
        item["label"],
    ))
    return {
        "index": str(index.relative_to(ATLAS)),
        "reader": source_docs[0]["path"] if source_docs else str(index.relative_to(ATLAS)),
        "docs": source_docs,
    }


def sync_library(records: list[dict], targets: dict[str, Path]) -> None:
    # Publish incrementally.  The library is a long-lived public archive: a
    # narrower audit (for example, mainline-only) must not erase previously
    # published deep notes, posters, or their image assets.
    LIBRARY.mkdir(parents=True, exist_ok=True)
    for record in records:
        assets = record.get("_assets") or {}
        model_root = assets.get("dir")
        if not model_root: continue
        dest_root = LIBRARY / record["team"] / record["slug"]
        note = assets.get("note")
        if note:
            dest = dest_root / note.name
            copy_file_with_refs(note, dest, model_root)
            rendered = dest.with_suffix(".html")
            render_markdown(note, rendered, targets)
            record["note"] = str(rendered.relative_to(ATLAS))
        for poster in assets.get("posters", []):
            dest = dest_root / poster.name
            # Do not downgrade an already-published, hand-designed poster with
            # an auto-generated fallback that happens to share its filename.
            source_text = poster.read_text(encoding="utf-8", errors="ignore")
            dest_text = dest.read_text(encoding="utf-8", errors="ignore") if dest.exists() else ""
            source_is_fallback = "Base Model Atlas 补齐页" in source_text
            dest_is_fallback = "Base Model Atlas 补齐页" in dest_text
            if not dest.exists() or dest_is_fallback or (not source_is_fallback and poster.stat().st_size > dest.stat().st_size):
                copy_file_with_refs(poster, dest, model_root)
            record.setdefault("posters", []).append(str(dest.relative_to(ATLAS)))
        if record["team"] == "deepseek":
            compact_v4_source = None
            if record["name"].startswith("DeepSeek-V4") and record["name"] not in {"DeepSeek-V4", "DeepSeek-V4-Flash"}:
                source_name = f"{record['name']}.md"
                source_rel = Path("huggingface_model_cards") / source_name
                if not (model_root / "src" / source_rel).is_file():
                    source_rel = Path("huggingface_repository_metadata") / f"{record['name']}.json"
                compact_v4_source = {
                    source_rel,
                    Path("hf_collection_manifest.json"),
                    Path("retrieval_manifest.json"),
                }
            source_archive = sync_source_archive(
                model_root,
                dest_root,
                targets,
                include_relative=compact_v4_source,
            )
            if source_archive:
                record["sources"] = source_archive["index"]
                record["sourceReader"] = source_archive["reader"]
                record["sourceDocs"] = source_archive["docs"]
                if record["name"].startswith("DeepSeek-V4"):
                    matching_docs = [
                        doc for doc in record["sourceDocs"]
                        if doc["name"] in {f"{record['name']}.md", f"{record['name']}.json"}
                    ]
                    if matching_docs:
                        preferred = matching_docs[0]
                        record["sourceReader"] = preferred["path"]
                        record["sourceDocs"] = [preferred] + [
                            doc for doc in record["sourceDocs"] if doc is not preferred
                        ]


def validate_top8_mainline_contract(records: list[dict]) -> None:
    """Refuse to publish an incomplete or broken Top-8 mainline atlas."""
    errors: list[str] = []
    all_slugs = [record["slug"] for record in records]
    if len(all_slugs) != len(set(all_slugs)):
        errors.append("duplicate model slugs")

    for team_id, expected_oldest_first in TOP8_MAINLINE_CONTRACT.items():
        mainline = [
            record for record in records
            if record["team"] == team_id and record["lineageType"] == "mainline"
        ]
        actual_newest_first = [record["name"] for record in mainline]
        if sorted(actual_newest_first) != sorted(expected_oldest_first):
            missing = [name for name in expected_oldest_first if name not in actual_newest_first]
            unexpected = [name for name in actual_newest_first if name not in expected_oldest_first]
            errors.append(
                f"{team_id}: mainline mismatch; missing={missing}, "
                f"unexpected={unexpected}, actual={actual_newest_first}"
            )

        dates = [record["rawDate"] for record in mainline]
        if dates != sorted(dates, reverse=True):
            errors.append(f"{team_id}: timeline is not newest-first: {dates}")

        for record in mainline:
            prefix = f"{team_id}/{record['name']}"
            if not record.get("source"):
                errors.append(f"{prefix}: missing official source")
            note = record.get("note")
            if not note or not (ATLAS / note).is_file():
                errors.append(f"{prefix}: missing rendered note")
            posters = record.get("posters") or []
            if not posters or not all((ATLAS / poster).is_file() for poster in posters):
                errors.append(f"{prefix}: missing published poster")
            if team_id == "deepseek":
                if not record.get("sources") or not (ATLAS / record["sources"]).is_file():
                    errors.append(f"{prefix}: missing published source archive")
                if not record.get("sourceReader") or not (ATLAS / record["sourceReader"]).is_file():
                    errors.append(f"{prefix}: missing workspace source reader")

    if errors:
        raise RuntimeError("Top-8 mainline contract failed:\n- " + "\n- ".join(errors))


def sync_archive(targets: dict[str, Path]) -> list[dict]:
    """Publish every non-source note and poster, including variant branches."""
    archive = ATLAS / "archive"
    # Keep historical routes stable when the current source inventory is
    # narrower than an earlier publish.
    archive.mkdir(parents=True, exist_ok=True)
    entries = []
    files = sorted(
        list(SOURCE.rglob("*.md")) + list(SOURCE.rglob("*poster*.html")),
        key=lambda p: str(p).lower(),
    )
    for item in files:
        rel = item.relative_to(SOURCE)
        if "src" in rel.parts or "QA" in rel.parts: continue
        destination = archive / rel
        model_root = item.parent
        copy_file_with_refs(item, destination, model_root)
        published = destination
        if item.suffix.lower() == ".md":
            published = destination.with_suffix(".html")
            render_markdown(item, published, targets)
        entries.append({
            "title": item.stem.replace("_", " ").replace("-", " "),
            "path": str(published.relative_to(ATLAS)),
            "team": rel.parts[0] if len(rel.parts) > 1 else "Cross-team",
            "kind": "Poster" if item.suffix.lower() == ".html" else "Note",
        })
    return entries


def sync_deepseek_hf_catalog(targets: dict[str, Path]) -> None:
    """Publish the complete official HF collection inventory, tree-independent."""
    source_root = SOURCE / "DeepSeek_AI"
    inventory_path = source_root / "src/huggingface_collections.json"
    if not inventory_path.is_file():
        return
    destination_root = ATLAS / "library/deepseek/hf-collections"
    destination_root.mkdir(parents=True, exist_ok=True)
    card_routes: dict[str, str] = {}
    for card in sorted(source_root.glob("**/src/huggingface_model_cards/*.md")):
        family = card.parents[2].name
        destination = destination_root / family / card.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(card, destination)
        rendered = Path(str(destination) + ".html")
        render_markdown(card, rendered, targets)
        card_routes[card.stem] = str(rendered.relative_to(ATLAS))

    collections = json.loads(inventory_path.read_text(encoding="utf-8"))
    collection_sections = []
    repository_count = 0
    missing_count = 0
    for collection in collections:
        items = [item for item in collection.get("items", []) if item.get("type") == "model"]
        repository_count += len(items)
        rows = []
        for item in items:
            repo = item["id"]
            name = repo.split("/", 1)[1]
            route = card_routes.get(name)
            if route:
                href = os.path.relpath(ATLAS / route, destination_root).replace(os.sep, "/")
                rows.append(f'<a class="repo" href="{html.escape(href, quote=True)}"><b>{html.escape(name)}</b><span>README.md · HTML 阅读版</span></a>')
            else:
                missing_count += 1
                rows.append(f'<a class="repo missing" href="https://huggingface.co/{html.escape(repo, quote=True)}" target="_blank" rel="noopener"><b>{html.escape(name)}</b><span>官方仓库无 README / model card</span></a>')
        collection_sections.append(
            f'<section><header><div><small>OFFICIAL COLLECTION</small><h2>{html.escape(collection["title"])}</h2></div>'
            f'<a href="https://huggingface.co/collections/{html.escape(collection["slug"], quote=True)}" target="_blank" rel="noopener">HF Collection ↗</a></header>'
            f'<div class="repos">{"".join(rows)}</div></section>'
        )
    (destination_root / "index.html").write_text(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DeepSeek · Hugging Face Collections</title><style>
:root{{--bg:#070b12;--panel:#101722;--line:#29364a;--text:#edf4ff;--muted:#8fa0b8;--cyan:#64dceb}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 72% -10%,#164e633d,transparent 34%),var(--bg);color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}main{{max-width:1320px;margin:auto;padding:36px 24px 90px}}nav{{display:flex;justify-content:space-between}}a{{color:#8be8f4;text-decoration:none}}.hero{{padding:72px 0 48px}}.hero small,section small{{color:var(--cyan);font-size:10px;letter-spacing:.16em}}h1{{font-size:clamp(48px,8vw,98px);line-height:.9;letter-spacing:-.06em;margin:14px 0 24px}}.lead{{max-width:830px;color:#b2bfd1;font-size:19px;line-height:1.65}}.stats{{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}}.stat{{padding:12px 16px;border:1px solid var(--line);border-radius:999px;background:#101722}}.stat b{{font-size:20px;margin-right:6px}}section{{margin-top:18px;border:1px solid var(--line);border-radius:22px;background:#0d141f;overflow:hidden}}section header{{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:20px 22px;border-bottom:1px solid var(--line)}}h2{{margin:5px 0 0;font-size:22px}}.repos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1px;background:var(--line)}}.repo{{display:block;padding:16px 18px;background:#0d141f;color:var(--text)}}.repo:hover{{background:#142131}}.repo b{{display:block;font-size:13px;overflow-wrap:anywhere}}.repo span{{display:block;margin-top:7px;color:var(--muted);font-size:11px}}.repo.missing{{background:#24161a}}.repo.missing span{{color:#f3a6ac}}@media(max-width:700px){{section header{{align-items:flex-start;flex-direction:column}}}}
</style></head><body><main><nav><a href="../../../base_model_atlas.html">← 返回谱系树</a><a href="https://huggingface.co/deepseek-ai/collections" target="_blank" rel="noopener">官方 Collections ↗</a></nav><div class="hero"><small>DEEPSEEK · COMPLETE HF INVENTORY</small><h1>Hugging Face<br>Model Cards</h1><p class="lead">这里按 DeepSeek 官方 collections 逐项对账。API 只用于获得仓库清单；正文全部来自各模型仓库原始 README.md，并预渲染为可读 HTML。同代的 Base / Chat / Lite / Distill 仍归在一个 family，不冒充新正代。</p><div class="stats"><span class="stat"><b>{len(collections)}</b> collections</span><span class="stat"><b>{repository_count}</b> 官方模型仓库</span><span class="stat"><b>{len(card_routes)}</b> 原始 model cards</span><span class="stat"><b>{missing_count}</b> 仓库无卡</span></div></div>{''.join(collection_sections)}</main></body></html>''', encoding="utf-8")


def build_records() -> tuple[list[dict], list[dict]]:
    records = []
    seen_slugs: set[str] = set()
    ordered_teams = sorted(TEAMS, key=lambda t: TEAM_PRIORITY.index(t["id"]) if t["id"] in TEAM_PRIORITY else 999)
    for team in ordered_teams:
        # Newest first: the first screen is current; horizontal movement to the
        # right becomes a deliberate trip back through earlier generations.
        timeline = [
            {"date": d, "name": n, "summary": s, "source": u, "lineageType": "mainline", "label": "主干正代"}
            for d, n, s, u in team["models"]
        ] + PINNED_TIMELINE_VARIANTS.get(team["id"], [])
        for item in sorted(timeline, key=lambda m: m["date"], reverse=True):
            raw_date, name, summary, url = item["date"], item["name"], item["summary"], item["source"]
            asset_folder = item.get("folder") or MODEL_ASSET_OVERRIDES.get(name, {}).get("folder")
            assets = apply_asset_overrides(
                discover_mainline_assets(team["dir"], name, raw_date, asset_folder),
                name,
                item,
            )
            slug = f"{team['id']}-{slugify(name)}"
            if slug in seen_slugs:
                slug = f"{slug}-{raw_date}"
            seen_slugs.add(slug)
            records.append({
                "slug":slug,"team":team["id"],"teamName":team["name"],"teamDir":team["dir"],
                "region":team["region"],"color":team["color"],"date":pretty_date(raw_date),
                "rawDate":raw_date,"name":name,"summary":summary,"source":url,
                "sourceType":source_label(url),"thesis":team["thesis"],
                "lineageType":item.get("lineageType", "variant"),
                "lineageLabel":item.get("label", "专项支线"),
                "variants":VARIANT_FAMILIES.get(team["id"], []),
                "_assets": assets,
            })
        for raw_date, name, branch_name, url in sorted(
            BRANCH_MODEL_NODES.get(team["id"], []), key=lambda m: m[0], reverse=True
        ):
            slug = f"{team['id']}-{slugify(name)}"
            if slug in seen_slugs:
                slug = f"{slug}-{raw_date}"
            seen_slugs.add(slug)
            records.append({
                "slug": slug, "team": team["id"], "teamName": team["name"],
                "teamDir": team["dir"], "region": team["region"], "color": team["color"],
                "date": pretty_date(raw_date), "rawDate": raw_date, "name": name,
                "summary": f"{team['name']} 的 {branch_name} 模型节点。",
                "source": url, "sourceType": source_label(url), "thesis": team["thesis"],
                "lineageType": "variant", "lineageLabel": branch_name,
                "variants": VARIANT_FAMILIES.get(team["id"], []),
                "_assets": discover_branch_assets(team["dir"], name, raw_date),
            })
    return ordered_teams, records


CSS = r'''
:root{--bg:#080b12;--panel:#0f1420;--panel2:#141b2a;--line:#283248;--text:#eef3ff;--muted:#91a0ba;--accent:#8ba7ff}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 55% -10%,#24315a66,transparent 34%),var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.shell{max-width:1680px;margin:auto;padding:28px clamp(18px,4vw,64px) 70px}.topbar{display:flex;justify-content:space-between;gap:20px;align-items:center;margin-bottom:55px}.brand{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:#b8c7e4}.toplinks{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.ghost{color:#b9c7e3;text-decoration:none;border:1px solid var(--line);padding:10px 14px;border-radius:999px}.hero{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr);gap:36px;align-items:end;margin-bottom:34px}.kicker{color:#8fe6ff;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:12px}.hero h1{font-size:clamp(48px,7vw,108px);line-height:.89;letter-spacing:-.065em;margin:15px 0 24px;max-width:980px}.hero p{font-size:clamp(17px,2vw,23px);line-height:1.55;color:#aebbd2;max-width:880px}.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.stat{border:1px solid var(--line);background:#111724aa;padding:20px;border-radius:18px}.stat b{display:block;font-size:31px;letter-spacing:-.04em}.stat span{color:var(--muted);font-size:13px}.controls{position:sticky;top:0;z-index:5;margin:0 -8px 28px;padding:12px 8px;background:#080b12e8;backdrop-filter:blur(14px);display:flex;gap:10px;flex-wrap:wrap}.search{flex:1;min-width:240px;background:#101622;border:1px solid var(--line);border-radius:14px;padding:13px 16px;color:var(--text);font-size:15px}.chip{border:1px solid var(--line);background:#101622;color:#b9c6dc;border-radius:999px;padding:11px 15px;cursor:pointer}.chip.active{background:#dce6ff;color:#111827}.legend{display:flex;gap:18px;color:var(--muted);font-size:12px;margin:0 0 18px 250px}.legend i{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px}.tree{display:flex;flex-direction:column;gap:14px}.branch{display:grid;grid-template-columns:230px minmax(0,1fr);border:1px solid #242e43;background:linear-gradient(100deg,#121827,#0d121d);border-radius:22px;overflow:hidden}.branch.top8{border-color:color-mix(in srgb,var(--team),#283248 72%)}.team{padding:22px;border-right:1px solid var(--line);position:relative}.team:after{content:"";position:absolute;right:-1px;top:50%;width:15px;height:2px;background:var(--team)}.team small{color:var(--muted);font-size:11px;letter-spacing:.12em;text-transform:uppercase}.team h2{font-size:20px;margin:7px 0 8px}.team p{font-size:12px;color:#8290a8;line-height:1.45;margin:0}.modelarea{min-width:0}.timeline{display:flex;align-items:center;gap:26px;padding:20px 30px;overflow-x:auto;min-height:142px;background-image:linear-gradient(90deg,transparent 0 18px,#35415c 18px calc(100% - 18px),transparent calc(100% - 18px));background-size:100% 2px;background-repeat:no-repeat;background-position:center}.leaf{min-width:148px;max-width:180px;color:inherit;text-decoration:none;position:relative;padding-top:44px}.leaf:before{content:"";position:absolute;top:14px;left:9px;width:15px;height:15px;border-radius:50%;background:var(--team);border:4px solid #111724;box-shadow:0 0 0 1px var(--team),0 0 22px color-mix(in srgb,var(--team),transparent 45%)}.leaf:after{content:"";position:absolute;left:16px;top:29px;width:1px;height:12px;background:var(--team)}.leaf time{font-size:11px;color:#74829a}.leaf b{font-size:14px;display:block;margin-top:5px;line-height:1.25}.leaf .status{display:block;font-size:10px;color:#7f8da3;margin-top:7px}.leaf:hover b{color:var(--team)}.leaf.branch-leaf:before{border-radius:4px;transform:rotate(45deg);background:#ff7fb7;box-shadow:0 0 0 1px #ff9bc4,0 0 24px #ff5fa877}.leaf.branch-leaf b{color:#ffc0da}.leaf.branch-leaf .status{color:#ff8fbd;font-weight:700}.variants{display:flex;gap:7px;overflow-x:auto;padding:0 30px 18px}.variants:before{content:"支线";font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#657188;padding:7px 5px 0 0}.variant{flex:0 0 auto;color:#aebbd0;text-decoration:none;font-size:11px;padding:6px 9px;border:1px solid #2a354b;border-radius:999px;background:#111824}.variant:hover{color:var(--team);border-color:var(--team)}.footnote{margin:34px 0 0;color:#7e8aa0;font-size:13px;line-height:1.7}.hidden{display:none!important}
@media(max-width:800px){.hero{grid-template-columns:1fr}.branch{grid-template-columns:1fr}.team{border-right:0;border-bottom:1px solid var(--line)}.team:after{display:none}.legend{margin-left:0}.timeline{padding-left:18px}.topbar{align-items:flex-start}.hero h1{font-size:54px}}
'''


def render_index(teams: list[dict], records: list[dict]) -> str:
    data = json.dumps([{k:v for k,v in r.items() if not k.startswith("_")} for r in records], ensure_ascii=False).replace("</", "<\\/")
    return f'''<!-- index: Base Model Atlas · 全球基模谱系 | 2026-08-31 | 最新优先的可点击模型思维树、Top 8 支线审计与渲染资料库 -->
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="全球基模团队与主干模型时间树，可进入模型 overview、Poster、渲染笔记与 Top 8 支线审计。"><title>Base Model Atlas · 全球基模谱系</title><style>{CSS}</style></head><body><div class="shell"><header class="topbar"><div class="brand">BrainHao / Thinking · Research Atlas</div><div class="toplinks"><a class="ghost" href="base-model-atlas/top8-tree.html">Top 8 综述树</a><a class="ghost" href="base-model-atlas/branch-audit.html">支线审计</a><a class="ghost" href="base-model-atlas/library.html">Poster / 笔记资料馆</a><a class="ghost" href="index.html">返回 Thinking 首页</a></div></header><section class="hero"><div><div class="kicker">Foundation Model Evolution · 2018—2026</div><h1>全球基模<br>谱系树</h1><p>每一条分支是一支基模团队。最新模型固定在最左侧，无需横向拖动；向右拖动是在回溯更早的代际。点击叶子进入 Overview，再继续阅读 Obsidian 风格笔记、Poster 与一手来源。</p></div><div class="stats"><div class="stat"><b>{len(teams)}</b><span>基模团队</span></div><div class="stat"><b>{len(records)}</b><span>可点击模型节点</span></div><div class="stat"><b>{sum(1 for r in records if r.get('note'))}</b><span>主树渲染笔记</span></div><div class="stat"><b>{sum(len(r.get('posters',[])) for r in records)}</b><span>主树已链接 Poster</span></div></div></section><div class="controls"><input class="search" id="search" placeholder="搜索团队、模型、MedXIAOHE 或支线…"><button class="chip active" data-region="all">全部</button><button class="chip" data-region="国内">国内团队</button><button class="chip" data-region="海外">海外团队</button></div><div class="legend"><span><i style="background:#70d9ff"></i>最新 ← 左 · 右 → 更早</span><span><i style="background:#7cf2c8"></i>圆点：主干正代</span><span><i style="background:#ff7fb7;border-radius:2px"></i>菱形：固定支线叶</span></div><main class="tree" id="tree"></main><p class="footnote">编辑口径：主时间线覆盖通用基模正代与改变范式的关键节点；对阅读导航重要的专项模型可作为菱形支线叶直接挂在线上。Top 8 已做独立审计；全部 Markdown 发布时自动渲染为可读 HTML。更新时间：2026-08-31。</p></div><script>const DATA={data};const TEAM_ORDER={json.dumps([t['id'] for t in teams])};const TEAM_META={json.dumps({t['id']:{k:t[k] for k in ('name','region','color','thesis')} for t in teams},ensure_ascii=False)};const TOP8=new Set(['deepseek','zhipu','kimi','qwen','seed','openai','anthropic','google']);let region='all';const tree=document.querySelector('#tree');function draw(){{const q=document.querySelector('#search').value.trim().toLowerCase();tree.innerHTML=TEAM_ORDER.map(id=>{{const meta=TEAM_META[id];const base=DATA.filter(x=>x.team===id).filter(x=>region==='all'||x.region===region);const variants=base[0]?.variants||[];const variantText=variants.map(v=>v.name+' '+v.models).join(' ').toLowerCase();const rows=!q||variantText.includes(q)?base:base.filter(x=>[x.name,x.teamName,x.summary,x.thesis].join(' ').toLowerCase().includes(q));if(!rows.length)return '';const branchChips=variants.map(v=>`<a class="variant" href="${{v.source}}" target="_blank" rel="noopener" title="${{v.models}}">${{v.name}} · ${{v.models}}</a>`).join('');return `<section class="branch ${{TOP8.has(id)?'top8':''}}" style="--team:${{meta.color}}"><div class="team"><small>${{meta.region}} · ${{rows.length}} nodes ${{TOP8.has(id)?'· TOP 8':''}}</small><h2>${{meta.name}}</h2><p>${{meta.thesis}}</p></div><div class="modelarea"><div class="timeline">${{rows.map(x=>`<a class="leaf ${{x.lineageType==='variant'?'branch-leaf':''}}" href="base-model-atlas/model.html?id=${{encodeURIComponent(x.slug)}}" title="${{x.summary}}"><time>${{x.date}}</time><b>${{x.name}}</b><span class="status">${{x.lineageType==='variant'?x.lineageLabel+' · ':''}}${{x.note?'渲染笔记 ':''}}${{x.posters?.length?'· Poster':''}}</span></a>`).join('')}}</div>${{branchChips?`<div class="variants">${{branchChips}}</div>`:''}}</div></section>`}}).join('')}}document.querySelector('#search').addEventListener('input',draw);document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');region=b.dataset.region;draw()}});draw();</script></body></html>'''


def neutralize_single_model_emphasis(page: str) -> str:
    """Keep individually requested models visible without turning them into UI callouts."""
    return (page
        .replace("搜索团队、模型、MedXIAOHE 或支线…", "搜索团队、模型或支线…")
        .replace('<span><i style="background:#ff7fb7;border-radius:2px"></i>菱形：固定支线叶</span>', "")
        .replace("；对阅读导航重要的专项模型可作为菱形支线叶直接挂在线上", "")
        .replace('<span style="color:#ff9fc8">粉色叶：MedXIAOHE · Seed Medical</span>', ""))


def render_index_complete(teams: list[dict], records: list[dict]) -> str:
    sections = []
    for team in teams:
        family = [r for r in records if r["team"] == team["id"]]
        mainline = [r for r in family if r["lineageType"] == "mainline"]
        variants = [r for r in family if r["lineageType"] == "variant"]

        def leaf(r: dict, branch: bool = False) -> str:
            state = " · ".join(x for x in ["渲染笔记" if r.get("note") else "", "Poster" if r.get("posters") else ""] if x)
            return (f'<a class="leaf{" branch-leaf" if branch else ""}" '
                    f'href="base-model-atlas/model.html?id={quote(r["slug"])}" title="{html.escape(r["summary"], quote=True)}">'
                    f'<time>{r["date"]}</time><b>{html.escape(r["name"])}</b>'
                    f'<span class="status">{html.escape(state)}</span></a>')

        branch_groups = []
        for branch_name in dict.fromkeys(r["lineageLabel"] for r in variants):
            nodes = sorted((r for r in variants if r["lineageLabel"] == branch_name), key=lambda r:r["rawDate"], reverse=True)
            branch_groups.append(
                f'<div class="branch-lane"><div class="branch-name">{html.escape(branch_name)}</div>'
                f'<div class="branch-scroll">{"".join(leaf(r, True) for r in nodes)}</div></div>'
            )
        search_text = " ".join([team["name"], team["thesis"]] + [r["name"] + " " + r["lineageLabel"] for r in family]).lower()
        branch_pack = ""
        if branch_groups:
            branch_pack = (
                f'<details class="branch-pack"><summary>展开专项支线 · {len(variants)} 个模型</summary>'
                f'{"".join(branch_groups)}</details>'
            )
        sections.append(
            f'<section class="branch {"top8" if team["id"] in BRANCH_MODEL_NODES else ""}" '
            f'data-region="{team["region"]}" data-search="{html.escape(search_text, quote=True)}" style="--team:{team["color"]}">'
            f'<div class="team"><small>{team["region"]} · {len(family)} 可点击节点</small><h2>{html.escape(team["name"])}</h2><p>{html.escape(team["thesis"])}</p></div>'
            f'<div class="modelarea"><div class="lane-title">主线 · 最新在左</div><div class="timeline">{"".join(leaf(r) for r in mainline)}</div>'
            f'{branch_pack}</div></section>'
        )
    extra_css = r'''
.lane-title{padding:14px 30px 0;color:#66758e;font-size:10px;letter-spacing:.13em;text-transform:uppercase}.branch-pack{border-top:1px solid #202a3d}.branch-pack>summary{cursor:pointer;list-style:none;padding:13px 30px;color:#93a3bc;font-size:11px;font-weight:700;letter-spacing:.04em;user-select:none}.branch-pack>summary::-webkit-details-marker{display:none}.branch-pack>summary:before{content:"＋";display:inline-grid;place-items:center;width:19px;height:19px;margin-right:8px;border:1px solid #34425a;border-radius:50%;color:var(--team)}.branch-pack[open]>summary:before{content:"−"}.branch-pack[open]>summary{color:#d5deed}.branch-lane{display:grid;grid-template-columns:120px minmax(0,1fr);border-top:1px solid #202a3d}.branch-name{padding:24px 12px 20px 30px;color:var(--team);font-size:11px;font-weight:750}.branch-scroll{display:flex;gap:24px;overflow-x:auto;padding:10px 28px 15px;min-height:118px}.branch-scroll .leaf{min-width:132px;padding-top:38px}.branch-scroll .leaf:before{top:11px;width:12px;height:12px;border-radius:50%;transform:none;background:var(--team);box-shadow:none}.branch-scroll .leaf:after{top:25px;height:10px}.branch-scroll .leaf b{color:inherit}.branch-scroll .leaf .status{color:#77869e;font-weight:400}.branch.hidden{display:none}@media(max-width:800px){.branch-lane{grid-template-columns:1fr}.branch-name{padding-bottom:0}}
'''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Base Model Atlas · 全球基模谱系</title><style>{CSS}{extra_css}</style></head><body><div class="shell"><header class="topbar"><div class="brand">BrainHao / Thinking · Research Atlas</div><div class="toplinks"><a class="ghost" href="base-model-atlas/top8-tree.html">Top 8 综述树</a><a class="ghost" href="base-model-atlas/branch-audit.html">支线审计</a><a class="ghost" href="base-model-atlas/library.html">Poster / 笔记资料馆</a><a class="ghost" href="index.html">返回 Thinking 首页</a></div></header><section class="hero"><div><div class="kicker">Foundation Model Evolution · 2018—2026</div><h1>全球基模<br>谱系树</h1><p>每支团队先展示通用主线，再展开逐模型支线。所有时间线都以最新模型在左；向右拖动是在回溯更早模型。点击任一叶子进入 Overview。</p></div><div class="stats"><div class="stat"><b>{len(teams)}</b><span>基模团队</span></div><div class="stat"><b>{len(records)}</b><span>可点击模型叶</span></div><div class="stat"><b>{sum(1 for r in records if r.get("note"))}</b><span>渲染笔记</span></div><div class="stat"><b>{sum(len(r.get("posters", [])) for r in records)}</b><span>已链接 Poster</span></div></div></section><div class="controls"><input class="search" id="search" placeholder="搜索团队、模型或支线…"><button class="chip active" data-region="all">全部</button><button class="chip" data-region="国内">国内团队</button><button class="chip" data-region="海外">海外团队</button></div><div class="legend"><span><i style="background:#70d9ff"></i>最新 ← 左 · 右 → 更早</span><span><i style="background:#7cf2c8"></i>每个圆点均可进入 Overview</span></div><main class="tree">{"".join(sections)}</main><p class="footnote">主线与专项/模态支线分层呈现；同一正代的尺寸与 API snapshot 不重复拆叶。更新时间：2026-08-31。</p></div><script>let region='all';const sections=[...document.querySelectorAll('.branch')];function filter(){{const q=document.querySelector('#search').value.trim().toLowerCase();sections.forEach(s=>{{s.classList.toggle('hidden',(region!=='all'&&s.dataset.region!==region)||(q&&!s.dataset.search.includes(q)));s.querySelectorAll('.branch-pack').forEach(d=>d.open=Boolean(q))}})}}document.querySelector('#search').addEventListener('input',filter);document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');region=b.dataset.region;filter()}});</script></body></html>'''


def render_library(entries: list[dict]) -> str:
    data = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="BrainHao Base Model Poster 与笔记资料馆"><title>Base Model Library · Poster / 笔记</title><style>{CSS}.library-head{{max-width:900px;margin:45px 0}}.library-head h1{{font-size:clamp(48px,7vw,88px);letter-spacing:-.06em;line-height:.95;margin:15px 0}}.gridlib{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}.doc{{display:block;text-decoration:none;color:inherit;padding:18px;border-radius:17px;border:1px solid var(--line);background:#111724}}.doc:hover{{border-color:#6f86ba;transform:translateY(-1px)}}.doc small{{color:#7e8da7}}.doc b{{display:block;margin:8px 0;line-height:1.35}}.badge{{display:inline-block;font-size:10px;padding:4px 7px;border-radius:999px;background:#24304a;color:#c9d5eb}}</style></head><body><div class="shell"><header class="topbar"><div class="brand">BrainHao / Base Model Library</div><div class="toplinks"><a class="ghost" href="top8-tree.html">Top 8 综述树</a><a class="ghost" href="branch-audit.html">支线审计</a><a class="ghost" href="../base_model_atlas.html">返回谱系树</a></div></header><section class="library-head"><div class="kicker">Synced Research Archive</div><h1>Poster / 笔记<br>资料馆</h1><p class="lead2">主干与支线材料统一归档。Markdown 已预渲染为 Obsidian 风格 HTML：支持 callout、表格、代码、图片和可解析的 wikilink，同时保留原始 Markdown 便于追溯。</p></section><div class="controls"><input class="search" id="search" placeholder="搜索资料…"><button class="chip active" data-kind="all">全部</button><button class="chip" data-kind="Poster">Poster</button><button class="chip" data-kind="Note">渲染笔记</button></div><main class="gridlib" id="grid"></main></div><script>const DATA={data};let kind='all';const grid=document.querySelector('#grid');function draw(){{const q=document.querySelector('#search').value.trim().toLowerCase();grid.innerHTML=DATA.filter(x=>kind==='all'||x.kind===kind).filter(x=>!q||[x.title,x.team,x.kind].join(' ').toLowerCase().includes(q)).map(x=>`<a class="doc" href="${{x.path}}"><small>${{x.team}}</small><b>${{x.title}}</b><span class="badge">${{x.kind==='Note'?'HTML 笔记':x.kind}}</span></a>`).join('')}}document.querySelector('#search').addEventListener('input',draw);document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');kind=b.dataset.kind;draw()}});draw();</script></body></html>'''


DETAIL_CSS = CSS + r'''
.detail{max-width:1180px;margin:auto;padding:26px clamp(18px,5vw,70px) 72px}.crumb{display:flex;justify-content:space-between;gap:16px;margin-bottom:60px}.crumb a{color:#aebbd2;text-decoration:none}.model-head{display:grid;grid-template-columns:1fr 260px;gap:35px;align-items:end;border-bottom:1px solid var(--line);padding-bottom:42px}.model-head h1{font-size:clamp(52px,9vw,112px);line-height:.9;letter-spacing:-.065em;margin:15px 0 22px}.datecard{border:1px solid var(--line);border-radius:22px;padding:25px;background:#121827}.datecard b{font-size:33px;display:block}.datecard span{color:var(--muted);font-size:12px}.lead2{font-size:clamp(19px,2.4vw,28px);line-height:1.55;color:#c2cde0;max-width:850px}.section{padding:38px 0;border-bottom:1px solid var(--line)}.section h2{font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#7f8da4;margin:0 0 18px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card2{background:#111724;border:1px solid var(--line);border-radius:18px;padding:20px}.card2 b{display:block;margin-bottom:8px}.card2 span{color:var(--muted);font-size:13px;line-height:1.5}.actions2{display:flex;gap:12px;flex-wrap:wrap}.button{padding:13px 17px;border-radius:999px;border:1px solid var(--line);color:#dce6f8;text-decoration:none;background:#121827}.button.primary{background:var(--team);color:#071019;border-color:transparent;font-weight:750}.empty{color:#79869c}.prevnext{display:grid;grid-template-columns:1fr 1fr;gap:14px}.next{border:1px solid var(--line);border-radius:18px;padding:18px;text-decoration:none;color:inherit}.next:last-child{text-align:right}.next small{color:var(--muted)}@media(max-width:700px){.model-head{grid-template-columns:1fr}.cards{grid-template-columns:1fr}.prevnext{grid-template-columns:1fr}}
'''


def render_detail(records: list[dict]) -> str:
    data = json.dumps([{k:v for k,v in r.items() if not k.startswith("_")} for r in records], ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Base Model Atlas 模型 overview"><title>Model Overview · Base Model Atlas</title><style>{DETAIL_CSS}</style></head><body><main class="detail" id="app"></main><script>const DATA={data};const p=new URLSearchParams(location.search);const id=p.get('id');const x=DATA.find(v=>v.slug===id)||DATA[0];document.title=`${{x.name}} · Base Model Atlas`;const family=DATA.filter(v=>v.team===x.team&&v.lineageType===x.lineageType);const pos=family.findIndex(v=>v.slug===x.slug);const newer=family[pos-1],older=family[pos+1];const atlas='../base_model_atlas.html';const rel=s=>s;document.querySelector('#app').style.setProperty('--team',x.color);const variants=(x.variants||[]).map(v=>`<a class="button" href="${{v.source}}" target="_blank" rel="noopener" title="${{v.models}}">${{v.name}} · ${{v.models}}</a>`).join('');const hasWorkspace=Boolean(x.sources&&x.note);document.querySelector('#app').innerHTML=`<nav class="crumb"><a href="${{atlas}}">← 全球基模谱系</a><span>${{x.teamName}}</span></nav><header class="model-head"><div><div class="kicker">${{x.region}} · ${{x.teamName}} · ${{x.lineageLabel}}</div><h1>${{x.name}}</h1><p class="lead2">${{x.summary}}</p></div><div class="datecard"><span>Release node</span><b>${{x.date}}</b><span>${{x.sourceType}}</span></div></header><section class="section"><h2>在团队谱系中的位置</h2><div class="cards"><div class="card2"><b>${{x.lineageType==='variant'?'专项支线叶':'团队主线'}}</b><span>${{x.lineageType==='variant'?x.lineageLabel+'，直接挂在 '+x.teamName+' 时间线上。':x.thesis}}</span></div><div class="card2"><b>资料状态</b><span>${{x.note?'已有 HTML 渲染笔记':'Overview 已补，独立精读笔记待扩展'}} · ${{x.posters?.length?x.posters.length+' 张 Poster':'独立 Poster 待扩展'}}</span></div><div class="card2"><b>证据边界</b><span>${{x.sourceType}}。未公开的参数、数据、训练 recipe 不作猜测。</span></div></div></section><section class="section"><h2>继续阅读</h2><div class="actions2">${{hasWorkspace?`<a class="button primary" href="workspace.html?id=${{encodeURIComponent(x.slug)}}">进入三合一研读台</a>`:''}}<a class="button ${{hasWorkspace?'':'primary'}}" href="${{x.source}}" target="_blank" rel="noopener">官方一手来源 ↗</a>${{x.note?`<a class="button" href="${{rel(x.note)}}">阅读渲染笔记</a>`:''}}${{x.sources?`<a class="button" href="${{rel(x.sources)}}">浏览本地一手资料包</a>`:''}}${{(x.posters||[]).map((u,i)=>`<a class="button" href="${{rel(u)}}">${{i===0?'打开 Poster':'Poster '+(i+1)}}</a>`).join('')}}</div>${{!x.note&&!x.posters?.length?'<p class="empty">此节点目前以官方材料 + Overview 为主；后续完成源码/技术报告精读后会在这里补上独立笔记与 Poster。</p>':''}}</section>${{x.lineageType==='variant'&&variants?`<section class="section"><h2>团队专项支线</h2><div class="actions2">${{variants}}</div><p class="empty">支线与主干正代分开展示，避免把模态模型、能力层和产品 SKU 误当作新一代通用基模。</p></section>`:''}}<section class="section"><h2>前后节点 · 时间线为最新优先</h2><div class="prevnext">${{newer?`<a class="next" href="?id=${{newer.slug}}"><small>← 更新节点 · ${{newer.date}}</small><br><b>${{newer.name}}</b></a>`:'<div></div>'}}${{older?`<a class="next" href="?id=${{older.slug}}"><small>更早节点 · ${{older.date}} →</small><br><b>${{older.name}}</b></a>`:'<div></div>'}}</div></section>`;</script></body></html>'''


WORKSPACE_CSS = r'''
:root{--bg:#080c12;--panel:#0e141d;--line:#263446;--text:#edf4ff;--muted:#8fa0b5;--accent:#62d8ef;--left:50%}*{box-sizing:border-box}html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}.toolbar{height:68px;padding:0 18px;display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line);background:#0a1018eF;backdrop-filter:blur(18px);position:relative;z-index:30}.back{width:38px;height:38px;display:grid;place-items:center;border:1px solid var(--line);border-radius:12px;color:#c9d7e8;text-decoration:none}.identity{min-width:0;margin-right:auto}.identity small{display:block;color:#69d7eb;font-size:9px;letter-spacing:.15em;text-transform:uppercase}.identity b{display:block;font-size:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.controls{display:flex;gap:7px;align-items:center}.control{height:36px;padding:0 12px;border:1px solid var(--line);border-radius:10px;background:#111a26;color:#dce8f7;font:inherit;font-size:11px;cursor:pointer}.control:hover,.control.active{border-color:#58cce3;background:#123041}.poster-button{background:#9b7cff;color:#0b0715;border-color:transparent;font-weight:800}.desk{height:calc(100vh - 68px);display:grid;grid-template-columns:minmax(280px,var(--left)) 9px minmax(280px,1fr);min-width:0}.panel{min-width:0;height:100%;background:var(--panel);display:grid;grid-template-rows:48px minmax(0,1fr)}.panel-head{padding:0 13px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line);background:#101823}.panel-head b{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:#9eb0c5}.panel-head span{font-size:10px;color:#64768b}.panel-head select{margin-left:auto;max-width:min(290px,47%);height:30px;border:1px solid #314258;border-radius:8px;background:#0b121b;color:#cfe0f3;padding:0 8px;font-size:10px}.open{color:#8ee8f6;text-decoration:none;font-size:10px;white-space:nowrap}.frame{display:block;width:100%;height:100%;border:0;background:#fff}.divider{position:relative;background:#111b27;cursor:col-resize;border-left:1px solid #253548;border-right:1px solid #253548}.divider:after{content:"";position:absolute;left:3px;top:50%;width:2px;height:44px;border-radius:3px;background:#577087;transform:translateY(-50%)}.resizing,.resizing *{cursor:col-resize!important;user-select:none!important}.drawer-backdrop{position:fixed;inset:68px 0 0;background:#0008;z-index:39;opacity:0;pointer-events:none;transition:.22s}.drawer{position:fixed;z-index:40;right:0;top:68px;bottom:0;width:min(720px,64vw);background:#08111a;border-left:1px solid #365064;box-shadow:-28px 0 80px #000a;transform:translateX(100%);transition:transform .25s ease;display:grid;grid-template-rows:50px minmax(0,1fr)}.drawer.open{transform:none}.drawer.open+.drawer-backdrop{opacity:1;pointer-events:auto}.drawer-head{display:flex;align-items:center;gap:10px;padding:0 13px;border-bottom:1px solid var(--line)}.drawer-head b{margin-right:auto}.drawer iframe{width:100%;height:100%;border:0}.mobile-tabs{display:none}.empty-workspace{height:100%;display:grid;place-items:center;text-align:center;color:var(--muted)}@media(max-width:900px){.toolbar{height:112px;align-items:flex-start;padding-top:13px;flex-wrap:wrap}.identity{width:calc(100% - 56px);order:1}.back{order:0}.controls{order:2;width:100%;overflow:auto}.desk{height:calc(100vh - 112px);display:block}.panel{display:none}.desk[data-mobile="source"] .source-panel,.desk[data-mobile="note"] .note-panel{display:grid}.divider{display:none}.mobile-tabs{display:inline-flex}.drawer{top:112px;width:100vw}.drawer-backdrop{inset:112px 0 0}.panel-head select{max-width:44%}}
'''


def render_workspace(records: list[dict]) -> str:
    available = [
        {k: v for k, v in record.items() if not k.startswith("_")}
        for record in records
        if record.get("note") and record.get("sources")
    ]
    data = json.dumps(available, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="官方原文、BrainHao 笔记与 Poster 三合一研读台"><title>三合一研读台 · Base Model Atlas</title><style>{WORKSPACE_CSS}</style></head><body>
<header class="toolbar"><a class="back" id="back" href="model.html">←</a><div class="identity"><small id="meta">BrainHao · Research Workspace</small><b id="title">三合一研读台</b></div><div class="controls"><span class="mobile-tabs"><button class="control active" data-mobile="source">原文</button><button class="control" data-mobile="note">笔记</button></span><button class="control" id="equal">50 / 50</button><a class="control" id="pack" href="#">全部一手资料</a><button class="control poster-button" id="posterToggle">展开 Poster</button></div></header>
<main class="desk" id="desk" data-mobile="source"><section class="panel source-panel"><header class="panel-head"><b>Official source</b><span>一手材料</span><select id="sourceSelect" aria-label="切换一手材料"></select><a class="open" id="sourceOpen" target="_blank" rel="noopener">单独打开 ↗</a></header><iframe class="frame" id="sourceFrame" title="DeepSeek 官方原文"></iframe></section><div class="divider" id="divider" role="separator" aria-label="拖动调整两栏宽度" tabindex="0"></div><section class="panel note-panel"><header class="panel-head"><b>BrainHao note</b><span>精读与判断</span><a class="open" id="noteOpen" target="_blank" rel="noopener">单独打开 ↗</a></header><iframe class="frame" id="noteFrame" title="BrainHao 精读笔记"></iframe></section></main>
<aside class="drawer" id="drawer"><header class="drawer-head"><b id="posterTitle">Research Poster</b><a class="open" id="posterOpen" target="_blank" rel="noopener">单独打开 ↗</a><button class="control" id="posterClose">收起</button></header><iframe id="posterFrame" title="模型研究 Poster"></iframe></aside><div class="drawer-backdrop" id="backdrop"></div>
<script>const DATA={data};const query=new URLSearchParams(location.search);const x=DATA.find(item=>item.slug===query.get('id'))||DATA[0];const desk=document.querySelector('#desk');if(!x){{desk.innerHTML='<div class="empty-workspace"><div><h1>这个节点还没有三合一资料</h1><p>请返回模型 Overview。</p></div></div>'}}else{{document.title=`${{x.name}} · 三合一研读台`;document.querySelector('#title').textContent=x.name;document.querySelector('#meta').textContent=`${{x.teamName}} · ${{x.date}} · 原文 × 笔记 × Poster`;document.querySelector('#back').href=`model.html?id=${{encodeURIComponent(x.slug)}}`;document.querySelector('#pack').href=x.sources;const note=document.querySelector('#noteFrame');const noteOpen=document.querySelector('#noteOpen');note.src=x.note;noteOpen.href=x.note;const docs=x.sourceDocs?.length?x.sourceDocs:[{{label:'一手资料包',path:x.sourceReader||x.sources}}];const select=document.querySelector('#sourceSelect');select.innerHTML=docs.map((doc,i)=>`<option value="${{i}}">${{doc.label}}</option>`).join('');const source=document.querySelector('#sourceFrame');const sourceOpen=document.querySelector('#sourceOpen');function showSource(i){{const doc=docs[Number(i)]||docs[0];source.src=doc.path;sourceOpen.href=doc.path}}select.onchange=()=>showSource(select.value);showSource(0);const poster=(x.posters||[])[0];const drawer=document.querySelector('#drawer');const toggle=document.querySelector('#posterToggle');const close=document.querySelector('#posterClose');function setPoster(open){{drawer.classList.toggle('open',open);toggle.textContent=open?'收起 Poster':'展开 Poster';toggle.classList.toggle('active',open);if(open&&poster&&!document.querySelector('#posterFrame').src)document.querySelector('#posterFrame').src=poster}}toggle.onclick=()=>setPoster(!drawer.classList.contains('open'));close.onclick=()=>setPoster(false);document.querySelector('#backdrop').onclick=()=>setPoster(false);if(poster){{document.querySelector('#posterOpen').href=poster;document.querySelector('#posterTitle').textContent=`${{x.name}} · Research Poster`}}else{{toggle.disabled=true;toggle.textContent='暂无 Poster'}}document.addEventListener('keydown',event=>{{if(event.key==='Escape')setPoster(false)}});let ratio=Math.min(72,Math.max(28,Number(localStorage.getItem('atlasSplit'))||50));function applyRatio(){{desk.style.setProperty('--left',ratio+'%')}}applyRatio();document.querySelector('#equal').onclick=()=>{{ratio=50;localStorage.setItem('atlasSplit',ratio);applyRatio()}};const divider=document.querySelector('#divider');function resize(event){{const box=desk.getBoundingClientRect();ratio=Math.min(72,Math.max(28,(event.clientX-box.left)/box.width*100));applyRatio()}}divider.onpointerdown=event=>{{divider.setPointerCapture(event.pointerId);document.body.classList.add('resizing');resize(event)}};divider.onpointermove=event=>{{if(divider.hasPointerCapture(event.pointerId))resize(event)}};divider.onpointerup=event=>{{divider.releasePointerCapture(event.pointerId);document.body.classList.remove('resizing');localStorage.setItem('atlasSplit',ratio)}};divider.onkeydown=event=>{{if(['ArrowLeft','ArrowRight'].includes(event.key)){{ratio+=event.key==='ArrowLeft'?-2:2;ratio=Math.min(72,Math.max(28,ratio));localStorage.setItem('atlasSplit',ratio);applyRatio()}}}};document.querySelectorAll('[data-mobile]').forEach(button=>button.onclick=()=>{{desk.dataset.mobile=button.dataset.mobile;document.querySelectorAll('[data-mobile]').forEach(item=>item.classList.toggle('active',item===button))}})}};</script></body></html>'''


def render_branch_audit(teams: list[dict]) -> str:
    top_ids = ["deepseek", "zhipu", "kimi", "qwen", "seed", "openai", "anthropic", "google"]
    cards = []
    for tid in top_ids:
        team = next(t for t in teams if t["id"] == tid)
        mainline = "".join(f'<span>{html.escape(name)}</span>' for _,name,_,_ in sorted(team["models"], key=lambda x:x[0], reverse=True))
        branches = "".join(f'<a href="{html.escape(b["source"], quote=True)}" target="_blank" rel="noopener"><b>{html.escape(b["name"])}</b><small>{html.escape(b["models"])}</small></a>' for b in VARIANT_FAMILIES[tid])
        extra = ""
        cards.append(f'<article class="audit-card" style="--team:{team["color"]}"><header><div><small>{team["region"]} TOP</small><h2>{html.escape(team["name"])}</h2></div><b>{len(team["models"])} 主干 · {len(VARIANT_FAMILIES[tid])} 支线</b></header><h3>主干 · 最新优先</h3><div class="mainline">{mainline}</div><h3>专项 / 模态支线</h3><div class="branch-list">{branches}</div>{extra}</article>')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 8 支线审计 · Base Model Atlas</title><style>{CSS}.audit-hero{{max-width:960px;margin:50px 0}}.audit-hero h1{{font-size:clamp(48px,8vw,96px);line-height:.92;letter-spacing:-.06em;margin:15px 0 25px}}.audit-hero p{{color:#aebbd2;font-size:19px;line-height:1.7}}.audit-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.audit-card{{border:1px solid #2a344a;border-top:4px solid var(--team);border-radius:22px;background:#101622;padding:22px}}.audit-card header{{display:flex;align-items:start;justify-content:space-between;gap:20px}}.audit-card header> b{{font-size:11px;color:#8190a8}}.audit-card h2{{margin:5px 0 20px;font-size:27px}}.audit-card h3{{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#78869e;margin:18px 0 10px}}.mainline{{display:flex;gap:6px;overflow-x:auto;padding-bottom:5px}}.mainline span{{white-space:nowrap;border-radius:999px;background:#192234;padding:7px 10px;font-size:11px}}.branch-list{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}}.branch-list a{{text-decoration:none;color:inherit;border:1px solid #2c374c;border-radius:13px;padding:11px;background:#0d121c}}.branch-list b,.branch-list small{{display:block}}.branch-list b{{color:var(--team);font-size:12px;margin-bottom:5px}}.branch-list small{{color:#8996aa;line-height:1.45}}.med{{display:inline-block;margin-top:16px;color:#ffc0da;text-decoration:none}}@media(max-width:800px){{.audit-grid{{grid-template-columns:1fr}}.branch-list{{grid-template-columns:1fr}}}}</style></head><body><div class="shell"><header class="topbar"><div class="brand">BrainHao / Top 8 Branch Audit</div><div class="toplinks"><a class="ghost" href="top8-tree.html">看综述树</a><a class="ghost" href="../base_model_atlas.html">返回谱系</a></div></header><section class="audit-hero"><div class="kicker">Mainline ≠ Variants</div><h1>八大团队<br>支线审计</h1><p>国内 DeepSeek、GLM、Kimi、Qwen、Seed；海外 GPT、Claude、Gemini。每张卡片把通用主干和专项分支拆开，解决“资料有了，但谱系关系看不出来”的问题。</p></section><main class="audit-grid">{''.join(cards)}</main></div></body></html>'''


def render_top8_tree(teams: list[dict]) -> str:
    domestic = ["deepseek", "zhipu", "kimi", "qwen", "seed"]
    overseas = ["openai", "anthropic", "google"]
    def team_box(tid: str) -> str:
        team = next(t for t in teams if t["id"] == tid)
        timeline = [{"date":d,"name":n} for d,n,_,_ in team["models"]] + [
            {"date":x["date"],"name":x["name"]} for x in PINNED_TIMELINE_VARIANTS.get(tid, [])
            if x.get("lineageType") == "mainline"
        ]
        latest = sorted(timeline, key=lambda x:x["date"], reverse=True)[:5]
        generations = "".join(f'<a href="model.html?id={tid}-{slugify(item["name"])}"><time>{pretty_date(item["date"])}</time><b>{html.escape(item["name"])}</b></a>' for item in latest)
        branches = []
        for branch in VARIANT_FAMILIES[tid]:
            branches.append(f'<span class="twig"><b>{html.escape(branch["name"])}</b>{html.escape(branch["models"])}</span>')
        return f'<article class="team-box" style="--team:{team["color"]}"><header><span>{team["region"]}</span><h3>{html.escape(team["name"])}</h3></header><div class="gen">{generations}</div><div class="twigs">{"".join(branches)}</div></article>'
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 8 Foundation Model Tree</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f7f8f4;color:#14233d;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background-image:linear-gradient(#dce3eb66 1px,transparent 1px),linear-gradient(90deg,#dce3eb66 1px,transparent 1px);background-size:48px 48px}}.page{{width:min(1500px,100%);margin:auto;padding:28px 34px 60px}}.nav{{display:flex;justify-content:space-between;align-items:center;font-size:12px;letter-spacing:.12em;text-transform:uppercase}}.nav a{{color:#294f88;text-decoration:none;border:1px solid #b9c7d9;padding:9px 13px;border-radius:999px;background:#fff}}h1{{font-size:clamp(36px,6vw,78px);letter-spacing:-.055em;line-height:.94;text-align:center;margin:36px 0 12px}}.sub{{text-align:center;color:#5e6d81;margin-bottom:34px}}.root{{width:min(780px,90%);margin:0 auto 30px;padding:20px 26px;text-align:center;border-radius:18px;background:#122744;color:white;box-shadow:0 12px 28px #0f274329}}.root b{{display:block;font-size:24px}}.root span{{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#b9d3f4}}.forest{{display:grid;grid-template-columns:5fr 3fr;gap:24px;align-items:start}}.grove{{position:relative;border:2px solid var(--group);border-radius:24px;padding:82px 16px 16px;background:color-mix(in srgb,var(--group),white 94%)}}.grove:before{{content:"";position:absolute;left:50%;top:-32px;width:2px;height:32px;background:#7890ad}}.grove-title{{position:absolute;left:-2px;right:-2px;top:-2px;padding:22px 24px;border-radius:22px 22px 0 0;background:var(--group);color:white;display:flex;justify-content:space-between;align-items:center}}.grove-title b{{font-size:18px}}.grove-title span{{font-size:11px;opacity:.85}}.domestic{{--group:#1768c5}}.overseas{{--group:#128675}}.teams{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}.domestic .team-box:first-child{{grid-column:span 2}}.overseas .teams{{grid-template-columns:1fr}}.team-box{{background:#fff;border:1px solid #c9d4e2;border-top:5px solid var(--team);border-radius:16px;padding:14px;min-width:0}}.team-box header{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}.team-box header span{{font-size:9px;letter-spacing:.13em;color:#7b8797}}.team-box h3{{margin:0;font-size:18px}}.gen{{display:flex;gap:6px;overflow-x:auto;padding:2px 0 9px}}.gen a{{min-width:108px;text-decoration:none;color:#14233d;padding:8px;border-radius:10px;background:#f1f5f9;border:1px solid #d9e1ea}}.gen time,.gen b{{display:block}}.gen time{{font-size:9px;color:#7b8797}}.gen b{{font-size:11px;margin-top:3px}}.twigs{{display:flex;gap:5px;flex-wrap:wrap;padding-top:9px;border-top:1px solid #dfe5ec}}.twig{{font-size:9px;line-height:1.35;color:#657186;background:#f8fafc;border:1px solid #dce3eb;padding:6px 7px;border-radius:8px}}.twig b{{color:#31445f;margin-right:4px}}.med-leaf{{background:#fff0f6;border-color:#ed9ec0;color:#9c315e;box-shadow:0 0 0 2px #fff inset}}.med-leaf b{{color:#c2185b}}.legend{{margin-top:20px;padding:15px 18px;background:#122744;color:#d7e1ee;border-radius:15px;display:flex;gap:24px;justify-content:center;font-size:11px}}@media(max-width:1000px){{.forest{{grid-template-columns:1fr}}.grove:before{{display:none}}}}@media(max-width:650px){{.page{{padding:20px 12px}}.teams{{grid-template-columns:1fr}}.domestic .team-box:first-child{{grid-column:auto}}}}
</style></head><body><main class="page"><nav class="nav"><span>BrainHao · Survey Figure 01</span><a href="../base_model_atlas.html">返回交互谱系</a></nav><h1>FRONTIER FOUNDATION<br>MODEL LANDSCAPE</h1><p class="sub">Top 8 labs · main generations + specialist branches · current state at 2026-08-31</p><section class="root"><span>Survey root</span><b>通用主干 × 模态 / 能力支线</b></section><div class="forest"><section class="grove domestic"><div class="grove-title"><b>国内 TOP 5</b><span>DeepSeek → GLM → Kimi → Qwen → Seed</span></div><div class="teams">{''.join(team_box(x) for x in domestic)}</div></section><section class="grove overseas"><div class="grove-title"><b>海外 TOP 3</b><span>GPT · Claude · Gemini</span></div><div class="teams">{''.join(team_box(x) for x in overseas)}</div></section></div><footer class="legend"><span>正代：近四个主干节点，最新在左</span><span>支线：专项模型族，不伪装成正代</span><span style="color:#ff9fc8">粉色叶：MedXIAOHE · Seed Medical</span></footer></main></body></html>'''


def render_branch_audit_complete(teams: list[dict], records: list[dict]) -> str:
    cards = []
    for team in [t for t in teams if t["id"] in BRANCH_MODEL_NODES]:
        family = [r for r in records if r["team"] == team["id"]]
        mains = [r for r in family if r["lineageType"] == "mainline"]
        variants = [r for r in family if r["lineageType"] == "variant"]
        groups = []
        for label in dict.fromkeys(r["lineageLabel"] for r in variants):
            nodes = sorted((r for r in variants if r["lineageLabel"] == label), key=lambda r:r["rawDate"], reverse=True)
            links = "".join(f'<a href="model.html?id={quote(r["slug"])}"><time>{r["date"]}</time>{html.escape(r["name"])}</a>' for r in nodes)
            groups.append(f'<div class="audit-branch"><b>{html.escape(label)}</b><div>{links}</div></div>')
        main_links = "".join(f'<a href="model.html?id={quote(r["slug"])}">{html.escape(r["name"])}</a>' for r in mains)
        cards.append(f'<article style="--team:{team["color"]}"><header><h2>{html.escape(team["name"])}</h2><span>{len(mains)} 主线 · {len(variants)} 支线模型</span></header><div class="audit-main">{main_links}</div>{"".join(groups)}</article>')
    css = r'''*{box-sizing:border-box}body{margin:0;background:#080b12;color:#edf3ff;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.page{max-width:1500px;margin:auto;padding:28px clamp(16px,4vw,58px) 70px}.nav{display:flex;justify-content:space-between}.nav a{color:#c5d3ea;text-decoration:none;border:1px solid #34415a;padding:9px 13px;border-radius:999px}h1{font-size:clamp(46px,8vw,92px);line-height:.9;letter-spacing:-.06em;margin:60px 0 16px}.lead{color:#a9b6ca;font-size:18px;max-width:900px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px;margin-top:38px}article{border:1px solid #29354a;border-top:4px solid var(--team);border-radius:20px;padding:20px;background:#111724}article header{display:flex;justify-content:space-between;gap:15px;align-items:start}h2{margin:0 0 16px}header span{color:#7f8da3;font-size:11px}.audit-main{display:flex;gap:6px;overflow-x:auto;padding-bottom:13px}.audit-main a,.audit-branch a{color:#c9d5e8;text-decoration:none;border:1px solid #2d394e;background:#0d121d;border-radius:999px;padding:7px 10px;white-space:nowrap;font-size:11px}.audit-branch{border-top:1px solid #253045;padding:13px 0 4px;display:grid;grid-template-columns:112px minmax(0,1fr);gap:8px}.audit-branch>b{color:var(--team);font-size:11px}.audit-branch>div{display:flex;gap:6px;overflow-x:auto}.audit-branch time{color:#718099;margin-right:5px}@media(max-width:850px){.grid{grid-template-columns:1fr}.audit-branch{grid-template-columns:1fr}}'''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 8 支线逐模型审计</title><style>{css}</style></head><body><main class="page"><nav class="nav"><span>BrainHao · Evidence Audit</span><a href="../base_model_atlas.html">返回谱系</a></nav><h1>八大团队<br>逐模型支线审计</h1><p class="lead">不再用一条文字概括整条支线：下面每个名称都是独立、可点击的模型叶，并按支线内部时间降序排列。</p><section class="grid">{"".join(cards)}</section></main></body></html>'''


def render_top8_tree_complete(teams: list[dict], records: list[dict]) -> str:
    order = ["deepseek", "zhipu", "kimi", "qwen", "seed", "openai", "anthropic", "google"]
    boxes = []
    for tid in order:
        team = next(t for t in teams if t["id"] == tid)
        family = [r for r in records if r["team"] == tid]
        main = [r for r in family if r["lineageType"] == "mainline"]
        main_nodes = "".join(f'<a href="model.html?id={quote(r["slug"])}"><time>{r["date"]}</time><b>{html.escape(r["name"])}</b></a>' for r in main)
        boxes.append(f'<article class="team-box {"domestic" if team["region"]=="国内" else "overseas"}" style="--team:{team["color"]}"><header><small>{team["region"]}</small><h2>{html.escape(team["name"])}</h2></header><div class="trunk"><strong>MAINLINE</strong><div>{main_nodes}</div></div></article>')
    css = r'''*{box-sizing:border-box}body{margin:0;background:#f7f8f4;color:#14233d;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background-image:linear-gradient(#dce3eb66 1px,transparent 1px),linear-gradient(90deg,#dce3eb66 1px,transparent 1px);background-size:42px 42px}.page{max-width:1580px;margin:auto;padding:28px clamp(14px,3vw,44px) 65px}.nav{display:flex;justify-content:space-between}.nav a{color:#254f86;text-decoration:none;border:1px solid #b8c5d5;padding:9px 13px;border-radius:999px;background:white}h1{text-align:center;font-size:clamp(42px,7vw,86px);letter-spacing:-.06em;line-height:.9;margin:50px 0 12px}.sub{text-align:center;color:#627186;margin-bottom:25px}.root{width:min(760px,90%);margin:0 auto 28px;background:#142d4d;color:white;text-align:center;border-radius:18px;padding:18px}.forest{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}.team-box{background:white;border:1px solid #cbd5e1;border-top:5px solid var(--team);border-radius:18px;padding:16px;position:relative}.team-box header{display:flex;gap:10px;align-items:baseline}.team-box h2{margin:0 0 12px}.team-box small{color:#7b8797}.trunk,.twig{display:grid;grid-template-columns:105px minmax(0,1fr);gap:8px;padding:10px 0;border-top:1px solid #dce3eb}.trunk strong,.twig>b{font-size:10px;color:var(--team);letter-spacing:.08em}.trunk>div,.twig>div{display:flex;gap:5px;overflow-x:auto}.trunk a,.twig a{min-width:max-content;text-decoration:none;color:#243750;border:1px solid #d5dee9;border-radius:9px;padding:7px 9px;background:#f8fafc;font-size:10px}.trunk a time{display:block;color:#7c8898;margin-bottom:3px}.twig a time{color:#8a96a5;margin-right:5px}.domestic{box-shadow:inset 4px 0 #1768c511}.overseas{box-shadow:inset 4px 0 #12867511}@media(max-width:900px){.forest{grid-template-columns:1fr}.trunk,.twig{grid-template-columns:1fr}}'''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 8 Foundation Model Survey Tree</title><style>{css}</style></head><body><main class="page"><nav class="nav"><span>BrainHao · Survey Tree</span><a href="../base_model_atlas.html">返回交互谱系</a></nav><h1>FRONTIER FOUNDATION<br>MODEL SURVEY TREE</h1><p class="sub">国内 Top 5：DeepSeek → GLM → Kimi → Qwen → Seed · 海外 Top 3：GPT → Claude → Gemini</p><div class="root">Foundation Models · 只看正代 · 左新右旧</div><section class="forest">{"".join(boxes)}</section></main></body></html>'''


def write_legacy_compatibility() -> None:
    redirect = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../../base_model_atlas.html"><link rel="canonical" href="../../base_model_atlas.html"><title>正在打开新版 Base Model Atlas</title></head><body><p><a href="../../base_model_atlas.html">打开新版 Base Model Atlas</a></p><script>location.replace('../../base_model_atlas.html')</script></body></html>'''
    for name in ("13_base_model_汇总.html", "13_base_model_汇总_v2.html"):
        (ATLAS / "archive" / name).write_text(redirect, encoding="utf-8")
    # GitHub Pages assigns MIME types from file extensions, so an HTML payload
    # saved directly as *.md would still display as plain Markdown.  A directory
    # named *.md with index.html makes the old URL receive a normal 301-to-slash
    # followed by a real 200 HTML document.  Build this compatibility route for
    # every rendered note, not only the one URL that exposed the problem.
    library_root = ATLAS / "library"
    legacy_root = library_root / "library"
    rendered_notes = [
        page for page in library_root.rglob("*.html")
        if legacy_root not in page.parents
        and "src" not in page.relative_to(library_root).parts
        and page.with_suffix(".md").is_file()
    ]
    for page in rendered_notes:
        rel = page.relative_to(library_root)
        legacy_dir = legacy_root / rel.with_suffix(".md")
        legacy_dir.mkdir(parents=True, exist_ok=True)
        base_href = "/thinking/base-model-atlas/library/" + quote(str(rel.parent)) + "/"
        content = page.read_text(encoding="utf-8")
        content = content.replace("<head>", f'<head><base href="{base_href}">', 1)
        (legacy_dir / "index.html").write_text(content, encoding="utf-8")
    not_found = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>正在修复旧链接</title></head><body><p id="m">正在跳转到可读 HTML…</p><script>let p=location.pathname;p=p.replace('/base-model-atlas/library/library/','/base-model-atlas/library/').replace(/\.md$/i,'.html');if(p!==location.pathname)location.replace(p+location.search+location.hash);else document.querySelector('#m').innerHTML='<a href="/thinking/base_model_atlas.html">返回 Base Model Atlas</a>';</script></body></html>'''
    (THINKING / "404.html").write_text(not_found, encoding="utf-8")


def main() -> None:
    add_missing_brainhao_packs()
    teams, records = build_records()
    ATLAS.mkdir(exist_ok=True)
    targets = note_targets()
    sync_library(records, targets)
    sync_deepseek_hf_catalog(targets)
    validate_top8_mainline_contract(records)
    archive_entries = sync_archive(targets)
    index_page = render_index_complete(teams, records).replace(
        '<div class="toplinks">',
        '<div class="toplinks"><a class="ghost" href="base-model-atlas/library/deepseek/hf-collections/index.html">DeepSeek HF 全集</a>',
        1,
    )
    (THINKING / "base_model_atlas.html").write_text(index_page, encoding="utf-8")
    (ATLAS / "model.html").write_text(render_detail(records), encoding="utf-8")
    (ATLAS / "workspace.html").write_text(render_workspace(records), encoding="utf-8")
    (ATLAS / "library.html").write_text(render_library(archive_entries), encoding="utf-8")
    (ATLAS / "branch-audit.html").write_text(render_branch_audit_complete(teams, records), encoding="utf-8")
    (ATLAS / "top8-tree.html").write_text(render_top8_tree_complete(teams, records), encoding="utf-8")
    write_legacy_compatibility()
    (ATLAS / "models.json").write_text(json.dumps([{k:v for k,v in r.items() if not k.startswith('_')} for r in records], ensure_ascii=False, indent=2), encoding="utf-8")
    linked_notes = sum(1 for r in records if r.get("note"))
    linked_posters = sum(len(r.get("posters", [])) for r in records)
    print(json.dumps({"teams":len(teams),"models":len(records),"linked_notes":linked_notes,"linked_posters":linked_posters,"archive_items":len(archive_entries)},ensure_ascii=False))


if __name__ == "__main__":
    main()
