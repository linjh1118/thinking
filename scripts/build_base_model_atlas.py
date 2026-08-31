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
        ["2405","GPT-4o","原生 omni 交互与低时延统一。","https://openai.com/index/hello-gpt-4o/"],
        ["2508","GPT-5","reasoning、fast path 与工具能力统一。","https://developers.openai.com/api/docs/models/gpt-5"],
        ["2511","GPT-5.1","强化 coding 与 agentic task。","https://developers.openai.com/api/docs/models/gpt-5.1"],
        ["2512","GPT-5.2","面向专业工作的可配置推理旗舰。","https://developers.openai.com/api/docs/models/gpt-5.2"],
        ["2603","GPT-5.4","1.05M context 与 computer use 进入通用旗舰。","https://developers.openai.com/api/docs/models/gpt-5.4"],
        ["2604","GPT-5.5","复杂 coding 与专业工作质量上移。","https://developers.openai.com/api/docs/models/gpt-5.5"],
        ["2608","GPT-5.6 Sol","Sol / Terra / Luna 分层，旗舰统一到 1.05M context。","https://developers.openai.com/api/docs/models/gpt-5.6-sol"]]},
    {"id":"anthropic","dir":"Anthropic","name":"Anthropic · Claude","region":"海外","color":"#ffb36b","thesis":"以 Constitutional AI、安全评估和长时程 agentic coding 为主轴。","models":[
        ["2303","Claude 1","Constitutional AI 路线首次产品化。","https://www.anthropic.com/news/introducing-claude"],
        ["2307","Claude 2","长上下文与 coding 能力增强。","https://www.anthropic.com/news/claude-2"],
        ["2403","Claude 3","Haiku / Sonnet / Opus 能力—成本分层。","https://www.anthropic.com/news/claude-3-family"],
        ["2406","Claude 3.5 Sonnet","coding 与 computer use 成为核心优势。","https://www.anthropic.com/news/claude-3-5-sonnet"],
        ["2502","Claude 3.7 Sonnet","hybrid reasoning 统一快答与 extended thinking。","https://www.anthropic.com/news/claude-3-7-sonnet"],
        ["2505","Claude 4","Opus / Sonnet 进入 agent 与长任务阶段。","https://www.anthropic.com/news/claude-4"],
        ["2511","Claude Opus 4.5","coding、computer use 与自主工作增强。","https://www.anthropic.com/news/claude-opus-4-5"],
        ["2602","Claude Opus 4.6","1M context 与 agent planning 持续增强。","https://www.anthropic.com/news/claude-opus-4-6"],
        ["2604","Claude Opus 4.7","长时程软件工程与自验证进一步提升。","https://www.anthropic.com/news/claude-opus-4-7"],
        ["2605","Claude Opus 4.8","更可靠的判断、工具效率与诚实性。","https://www.anthropic.com/news/claude-opus-4-8"],
        ["2606","Claude Sonnet 5","把高阶 agent 能力下放到 Sonnet 成本层。","https://www.anthropic.com/news/claude-sonnet-5"],
        ["2607","Claude Opus 5","面向长时程 agents 的 Opus 代际跃迁。","https://www.anthropic.com/news/claude-opus-5"]]},
    {"id":"google","dir":"Google_DeepMind","name":"Google DeepMind · Gemini","region":"海外","color":"#78a8ff","thesis":"原生多模态、超长上下文与推理/工具生态合流。","models":[
        ["2312","Gemini 1.0","Ultra / Pro / Nano 原生多模态分层。","https://deepmind.google/technologies/gemini/"],
        ["2402","Gemini 1.5","MoE 与百万 token context。","https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/"],
        ["2412","Gemini 2.0","agentic era、原生工具与实时交互。","https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/"],
        ["2503","Gemini 2.5","thinking model 成为主线。","https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/"],
        ["2511","Gemini 3","多模态 reasoning 与 agent 工具链升级。","https://deepmind.google/models/gemini/"],
        ["2602","Gemini 3.1 Pro","面向复杂专业任务与长时程 agents。","https://deepmind.google/models/gemini/"],
        ["2606","Gemini 3.5 Flash","更低成本的前沿 agentic 能力。","https://deepmind.google/models/gemini/"]]},
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
        ["2602","Qwen3.5","下一代开放模型架构迭代。","https://github.com/QwenLM/Qwen3"],
        ["2604","Qwen3.6","正代 family 的效率与能力升级。","https://github.com/QwenLM/Qwen3"],
        ["2608","Qwen3.8","原生多模态、1M context 与内置工具。","https://qwenlm.github.io/"]]},
    {"id":"deepseek","dir":"DeepSeek_AI","name":"DeepSeek AI","region":"国内","color":"#5aa8ff","thesis":"MLA/MoE 训练效率、开放 reasoning RL 与 agentic tool-use 是三条主轴。","models":[
        ["2401","DeepSeek LLM","开放 dense 基模与训练 recipe 起点。","https://github.com/deepseek-ai/DeepSeek-LLM"],
        ["2405","DeepSeek-V2","MLA + DeepSeekMoE 显著降低训练/推理成本。","https://github.com/deepseek-ai/DeepSeek-V2"],
        ["2409","DeepSeek-V2.5","通用与 coder 模型合并。","https://api-docs.deepseek.com/news/news0905"],
        ["2412","DeepSeek-V3","671B/37B active、14.8T tokens 与 FP8 训练。","https://api-docs.deepseek.com/news/news1226"],
        ["2501","DeepSeek-R1","大规模 RL 与极少标注的开放 reasoning 路线。","https://api-docs.deepseek.com/news/news250120/"],
        ["2508","DeepSeek-V3.1","hybrid inference 与 agent/tool-use 后训练。","https://api-docs.deepseek.com/news/news250821/"],
        ["2512","DeepSeek-V3.2","DSA 与 thinking-in-tool-use。","https://api-docs.deepseek.com/news/news251201/"],
        ["2604","DeepSeek-V4","Pro / Flash 分层并原生适配 agent API。","https://api-docs.deepseek.com/updates/"],
        ["2608","DeepSeek-V4 Pro","GA 版本强化 production agent 与 Responses API。","https://api-docs.deepseek.com/updates/"]]},
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
        ["2603","Seed1.8","真实世界 agent foundation model。","https://seed.bytedance.com/en/"],
        ["2605","Seed2.0","Computer Use 与 agent foundation model 扩展。","https://seed.bytedance.com/en/"]]},
    {"id":"zhipu","dir":"Zhipu_GLM","name":"Zhipu · GLM","region":"国内","color":"#58e0b5","thesis":"General Language Model 演进为 agentic reasoning/coding 原生基座。","models":[
        ["2210","GLM-130B","双语开放自回归预训练基座。","https://github.com/THUDM/GLM-130B"],
        ["2310","ChatGLM3","对话、代码与工具调用 family。","https://github.com/THUDM/ChatGLM3"],
        ["2401","GLM-4","新一代多模态与 tool-use 基座。","https://www.zhipuai.cn/"],
        ["2508","GLM-4.5","355B/32B active ARC foundation model。","https://github.com/zai-org/GLM-4.5"],
        ["2509","GLM-4.7","coding、tool use 与 interleaved reasoning。","https://docs.z.ai/"],
        ["2602","GLM-5","面向 agentic engineering 的新正代。","https://z.ai/blog"],
        ["2604","GLM-5.1","long-horizon coding agent。","https://z.ai/blog"],
        ["2606","GLM-5.2","1M context 与长时程 coding。","https://z.ai/blog"],
        ["2608","GLM-5.3 Flash","原生多模态与成本/速度 Pareto。","https://z.ai/blog"]]},
    {"id":"kimi","dir":"Moonshot_Kimi","name":"Moonshot · Kimi","region":"国内","color":"#9f8cff","thesis":"超长上下文底座逐步转向开放 MoE、视觉 agent 与 agent swarm。","models":[
        ["2310","Moonshot v1","长上下文产品化起点。","https://www.moonshot.cn/"],
        ["2501","Kimi k1.5","多模态 reasoning 与 RL scaling。","https://arxiv.org/abs/2501.12599"],
        ["2504","Kimi-VL","低激活 MoE 视觉语言模型。","https://github.com/MoonshotAI/Kimi-VL"],
        ["2507","Kimi K2","1T/32B active agentic intelligence。","https://github.com/MoonshotAI/Kimi-K2"],
        ["2510","Kimi Linear","KDA hybrid linear attention 与 1M context。","https://arxiv.org/abs/2510.26692"],
        ["2602","Kimi K2.5","视觉 agent、joint RL 与 Agent Swarm。","https://arxiv.org/abs/2602.02276"],
        ["2604","Kimi K2.6","开放 coding 与 agentic scaling。","https://huggingface.co/moonshotai"]]},
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


LATEST_PACKS = {
    "DeepSeek_AI": ("2608_DeepSeek_V4_Pro", "DeepSeek-V4-Pro", "GA 版本强化 production agent、原生 Responses API 与长时程工具任务。", "https://api-docs.deepseek.com/updates/"),
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
    return f"20{raw[:2]}-{raw[2:]}" if len(raw) == 4 else raw


def source_label(url: str) -> str:
    if "arxiv.org" in url: return "Technical report"
    if "github.com" in url or "huggingface.co" in url: return "Official repo / model card"
    if "developers.openai.com" in url or "docs." in url: return "Official docs"
    if url.endswith(".pdf"): return "System / model card"
    return "Official release"


def add_missing_brainhao_packs() -> None:
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


def discover_assets(team_dir: str, model_name: str, date: str) -> dict:
    root = SOURCE / team_dir
    if not root.exists(): return {}
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


def copy_file_with_refs(source_file: Path, destination: Path, model_root: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, destination)
    if source_file.suffix.lower() != ".html": return
    content = source_file.read_text(encoding="utf-8", errors="ignore")
    rewritten = content
    refs = re.findall(r'''(?:src|href)=["']([^"'#?]+)|url\(["']?([^"')]+)''', content, re.I)
    for pair in refs:
        ref = next((x for x in pair if x), "")
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
    if rewritten != content:
        destination.write_text(rewritten, encoding="utf-8")


def sync_library(records: list[dict]) -> None:
    if LIBRARY.exists(): shutil.rmtree(LIBRARY)
    LIBRARY.mkdir(parents=True)
    for record in records:
        assets = record.get("_assets") or {}
        model_root = assets.get("dir")
        if not model_root: continue
        dest_root = LIBRARY / record["team"] / record["slug"]
        note = assets.get("note")
        if note:
            dest = dest_root / note.name
            copy_file_with_refs(note, dest, model_root)
            record["note"] = str(dest.relative_to(ATLAS))
        for poster in assets.get("posters", []):
            dest = dest_root / poster.name
            copy_file_with_refs(poster, dest, model_root)
            record.setdefault("posters", []).append(str(dest.relative_to(ATLAS)))


def sync_archive() -> list[dict]:
    """Publish every non-source note and poster, including variant branches."""
    archive = ATLAS / "archive"
    if archive.exists(): shutil.rmtree(archive)
    archive.mkdir(parents=True)
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
        entries.append({
            "title": item.stem.replace("_", " ").replace("-", " "),
            "path": str(destination.relative_to(ATLAS)),
            "team": rel.parts[0] if len(rel.parts) > 1 else "Cross-team",
            "kind": "Poster" if item.suffix.lower() == ".html" else "Note",
        })
    return entries


def build_records() -> tuple[list[dict], list[dict]]:
    records = []
    for team in TEAMS:
        for raw_date, name, summary, url in team["models"]:
            slug = f"{team['id']}-{slugify(name)}"
            records.append({
                "slug":slug,"team":team["id"],"teamName":team["name"],"teamDir":team["dir"],
                "region":team["region"],"color":team["color"],"date":pretty_date(raw_date),
                "rawDate":raw_date,"name":name,"summary":summary,"source":url,
                "sourceType":source_label(url),"thesis":team["thesis"],
                "_assets":discover_assets(team["dir"], name, raw_date),
            })
    return TEAMS, records


CSS = r'''
:root{--bg:#080b12;--panel:#0f1420;--panel2:#141b2a;--line:#283248;--text:#eef3ff;--muted:#91a0ba;--accent:#8ba7ff}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 55% -10%,#24315a66,transparent 34%),var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.shell{max-width:1680px;margin:auto;padding:28px clamp(18px,4vw,64px) 70px}.topbar{display:flex;justify-content:space-between;gap:20px;align-items:center;margin-bottom:55px}.brand{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:#b8c7e4}.ghost{color:#b9c7e3;text-decoration:none;border:1px solid var(--line);padding:10px 14px;border-radius:999px}.hero{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr);gap:36px;align-items:end;margin-bottom:34px}.kicker{color:#8fe6ff;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:12px}.hero h1{font-size:clamp(48px,7vw,108px);line-height:.89;letter-spacing:-.065em;margin:15px 0 24px;max-width:980px}.hero p{font-size:clamp(17px,2vw,23px);line-height:1.55;color:#aebbd2;max-width:880px}.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.stat{border:1px solid var(--line);background:#111724aa;padding:20px;border-radius:18px}.stat b{display:block;font-size:31px;letter-spacing:-.04em}.stat span{color:var(--muted);font-size:13px}.controls{position:sticky;top:0;z-index:5;margin:0 -8px 28px;padding:12px 8px;background:#080b12e8;backdrop-filter:blur(14px);display:flex;gap:10px;flex-wrap:wrap}.search{flex:1;min-width:240px;background:#101622;border:1px solid var(--line);border-radius:14px;padding:13px 16px;color:var(--text);font-size:15px}.chip{border:1px solid var(--line);background:#101622;color:#b9c6dc;border-radius:999px;padding:11px 15px;cursor:pointer}.chip.active{background:#dce6ff;color:#111827}.legend{display:flex;gap:18px;color:var(--muted);font-size:12px;margin:0 0 18px 250px}.legend i{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px}.tree{display:flex;flex-direction:column;gap:14px}.branch{display:grid;grid-template-columns:230px minmax(0,1fr);border:1px solid #242e43;background:linear-gradient(100deg,#121827,#0d121d);border-radius:22px;overflow:hidden}.team{padding:22px;border-right:1px solid var(--line);position:relative}.team:after{content:"";position:absolute;right:-1px;top:50%;width:15px;height:2px;background:var(--team)}.team small{color:var(--muted);font-size:11px;letter-spacing:.12em;text-transform:uppercase}.team h2{font-size:20px;margin:7px 0 8px}.team p{font-size:12px;color:#8290a8;line-height:1.45;margin:0}.timeline{display:flex;align-items:center;gap:26px;padding:20px 30px;overflow-x:auto;min-height:142px;background-image:linear-gradient(90deg,transparent 0 18px,#35415c 18px calc(100% - 18px),transparent calc(100% - 18px));background-size:100% 2px;background-repeat:no-repeat;background-position:center}.leaf{min-width:148px;max-width:180px;color:inherit;text-decoration:none;position:relative;padding-top:44px}.leaf:before{content:"";position:absolute;top:14px;left:9px;width:15px;height:15px;border-radius:50%;background:var(--team);border:4px solid #111724;box-shadow:0 0 0 1px var(--team),0 0 22px color-mix(in srgb,var(--team),transparent 45%)}.leaf:after{content:"";position:absolute;left:16px;top:29px;width:1px;height:12px;background:var(--team)}.leaf time{font-size:11px;color:#74829a}.leaf b{font-size:14px;display:block;margin-top:5px;line-height:1.25}.leaf .status{display:block;font-size:10px;color:#7f8da3;margin-top:7px}.leaf:hover b{color:var(--team)}.footnote{margin:34px 0 0;color:#7e8aa0;font-size:13px;line-height:1.7}.hidden{display:none!important}
@media(max-width:800px){.hero{grid-template-columns:1fr}.branch{grid-template-columns:1fr}.team{border-right:0;border-bottom:1px solid var(--line)}.team:after{display:none}.legend{margin-left:0}.timeline{padding-left:18px}.topbar{align-items:flex-start}.hero h1{font-size:54px}}
'''


def render_index(teams: list[dict], records: list[dict]) -> str:
    data = json.dumps([{k:v for k,v in r.items() if not k.startswith("_")} for r in records], ensure_ascii=False).replace("</", "<\\/")
    return f'''<!-- index: Base Model Atlas · 全球基模谱系 | 2026-08-31 | 22 个团队、从老到新的可点击模型思维树与精读资料库 -->
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="全球基模团队与主干模型时间树，可进入模型 overview、Poster 与 BrainHao 笔记。"><title>Base Model Atlas · 全球基模谱系</title><style>{CSS}</style></head><body><div class="shell"><header class="topbar"><div class="brand">BrainHao / Thinking · Research Atlas</div><div><a class="ghost" href="base-model-atlas/library.html">Poster / 笔记资料馆</a> <a class="ghost" href="index.html">返回 Thinking 首页</a></div></header><section class="hero"><div><div class="kicker">Foundation Model Evolution · 2018—2026</div><h1>全球基模<br>谱系树</h1><p>每一条分支是一支基模团队；每片叶子按时间从左到右生长。点击模型进入 Overview，并继续阅读已同步的 Poster、精读笔记与官方一手来源。</p></div><div class="stats"><div class="stat"><b>{len(teams)}</b><span>基模团队</span></div><div class="stat"><b>{len(records)}</b><span>主干模型节点</span></div><div class="stat"><b>{sum(1 for r in records if r.get('note'))}</b><span>主树已链接笔记</span></div><div class="stat"><b>{sum(len(r.get('posters',[])) for r in records)}</b><span>主树已链接 Poster</span></div></div></section><div class="controls"><input class="search" id="search" placeholder="搜索团队、模型或关键技术…"><button class="chip active" data-region="all">全部</button><button class="chip" data-region="国内">国内团队</button><button class="chip" data-region="海外">海外团队</button></div><div class="legend"><span><i style="background:#70d9ff"></i>旧 → 新</span><span><i style="background:#7cf2c8"></i>叶子可点击</span><span>主树不拆 API snapshot / 参数 SKU</span></div><main class="tree" id="tree"></main><p class="footnote">编辑口径：覆盖独立通用基模团队的主干正代与改变范式的关键节点；Coder、Embedding、ASR/TTS、Robotics、Guard 等专项支线不与正代混排。全部既有 Poster / 笔记（含支线）已进入资料馆。没有公开训练细节的闭源模型只陈述官方披露，不做架构猜测。更新时间：2026-08-31。</p></div><script>const DATA={data};const TEAM_ORDER={json.dumps([t['id'] for t in teams])};const TEAM_META={json.dumps({t['id']:{k:t[k] for k in ('name','region','color','thesis')} for t in teams},ensure_ascii=False)};let region='all';const tree=document.querySelector('#tree');function draw(){{const q=document.querySelector('#search').value.trim().toLowerCase();tree.innerHTML=TEAM_ORDER.map(id=>{{const meta=TEAM_META[id];const rows=DATA.filter(x=>x.team===id).filter(x=>region==='all'||x.region===region).filter(x=>!q||[x.name,x.teamName,x.summary,x.thesis].join(' ').toLowerCase().includes(q));if(!rows.length)return '';return `<section class="branch" style="--team:${{meta.color}}"><div class="team"><small>${{meta.region}} · ${{rows.length}} nodes</small><h2>${{meta.name}}</h2><p>${{meta.thesis}}</p></div><div class="timeline">${{rows.map(x=>`<a class="leaf" href="base-model-atlas/model.html?id=${{encodeURIComponent(x.slug)}}" title="${{x.summary}}"><time>${{x.date}}</time><b>${{x.name}}</b><span class="status">${{x.note?'笔记 ':''}}${{x.posters?.length?'· Poster':''}}</span></a>`).join('')}}</div></section>`}}).join('')}}document.querySelector('#search').addEventListener('input',draw);document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');region=b.dataset.region;draw()}});draw();</script></body></html>'''


def render_library(entries: list[dict]) -> str:
    data = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="BrainHao Base Model Poster 与笔记资料馆"><title>Base Model Library · Poster / 笔记</title><style>{CSS}.library-head{{max-width:900px;margin:45px 0}}.library-head h1{{font-size:clamp(48px,7vw,88px);letter-spacing:-.06em;line-height:.95;margin:15px 0}}.gridlib{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}.doc{{display:block;text-decoration:none;color:inherit;padding:18px;border-radius:17px;border:1px solid var(--line);background:#111724}}.doc:hover{{border-color:#6f86ba;transform:translateY(-1px)}}.doc small{{color:#7e8da7}}.doc b{{display:block;margin:8px 0;line-height:1.35}}.badge{{display:inline-block;font-size:10px;padding:4px 7px;border-radius:999px;background:#24304a;color:#c9d5eb}}</style></head><body><div class="shell"><header class="topbar"><div class="brand">BrainHao / Base Model Library</div><a class="ghost" href="../base_model_atlas.html">返回谱系树</a></header><section class="library-head"><div class="kicker">Synced Research Archive</div><h1>Poster / 笔记<br>资料馆</h1><p class="lead2">主干与支线材料统一归档。搜索团队、模型或文件名，直接打开 Poster 或 Markdown 笔记。</p></section><div class="controls"><input class="search" id="search" placeholder="搜索资料…"><button class="chip active" data-kind="all">全部</button><button class="chip" data-kind="Poster">Poster</button><button class="chip" data-kind="Note">笔记</button></div><main class="gridlib" id="grid"></main></div><script>const DATA={data};let kind='all';const grid=document.querySelector('#grid');function draw(){{const q=document.querySelector('#search').value.trim().toLowerCase();grid.innerHTML=DATA.filter(x=>kind==='all'||x.kind===kind).filter(x=>!q||[x.title,x.team,x.kind].join(' ').toLowerCase().includes(q)).map(x=>`<a class="doc" href="${{x.path}}"><small>${{x.team}}</small><b>${{x.title}}</b><span class="badge">${{x.kind}}</span></a>`).join('')}}document.querySelector('#search').addEventListener('input',draw);document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');kind=b.dataset.kind;draw()}});draw();</script></body></html>'''


DETAIL_CSS = CSS + r'''
.detail{max-width:1180px;margin:auto;padding:26px clamp(18px,5vw,70px) 72px}.crumb{display:flex;justify-content:space-between;gap:16px;margin-bottom:60px}.crumb a{color:#aebbd2;text-decoration:none}.model-head{display:grid;grid-template-columns:1fr 260px;gap:35px;align-items:end;border-bottom:1px solid var(--line);padding-bottom:42px}.model-head h1{font-size:clamp(52px,9vw,112px);line-height:.9;letter-spacing:-.065em;margin:15px 0 22px}.datecard{border:1px solid var(--line);border-radius:22px;padding:25px;background:#121827}.datecard b{font-size:33px;display:block}.datecard span{color:var(--muted);font-size:12px}.lead2{font-size:clamp(19px,2.4vw,28px);line-height:1.55;color:#c2cde0;max-width:850px}.section{padding:38px 0;border-bottom:1px solid var(--line)}.section h2{font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#7f8da4;margin:0 0 18px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card2{background:#111724;border:1px solid var(--line);border-radius:18px;padding:20px}.card2 b{display:block;margin-bottom:8px}.card2 span{color:var(--muted);font-size:13px;line-height:1.5}.actions2{display:flex;gap:12px;flex-wrap:wrap}.button{padding:13px 17px;border-radius:999px;border:1px solid var(--line);color:#dce6f8;text-decoration:none;background:#121827}.button.primary{background:var(--team);color:#071019;border-color:transparent;font-weight:750}.empty{color:#79869c}.prevnext{display:grid;grid-template-columns:1fr 1fr;gap:14px}.next{border:1px solid var(--line);border-radius:18px;padding:18px;text-decoration:none;color:inherit}.next:last-child{text-align:right}.next small{color:var(--muted)}@media(max-width:700px){.model-head{grid-template-columns:1fr}.cards{grid-template-columns:1fr}.prevnext{grid-template-columns:1fr}}
'''


def render_detail(records: list[dict]) -> str:
    data = json.dumps([{k:v for k,v in r.items() if not k.startswith("_")} for r in records], ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Base Model Atlas 模型 overview"><title>Model Overview · Base Model Atlas</title><style>{DETAIL_CSS}</style></head><body><main class="detail" id="app"></main><script>const DATA={data};const p=new URLSearchParams(location.search);const id=p.get('id');const x=DATA.find(v=>v.slug===id)||DATA[0];document.title=`${{x.name}} · Base Model Atlas`;const family=DATA.filter(v=>v.team===x.team);const pos=family.findIndex(v=>v.slug===x.slug);const prev=family[pos-1],next=family[pos+1];const atlas='../base_model_atlas.html';const rel=s=>'library/'+s;document.querySelector('#app').style.setProperty('--team',x.color);document.querySelector('#app').innerHTML=`<nav class="crumb"><a href="${{atlas}}">← 全球基模谱系</a><span>${{x.teamName}}</span></nav><header class="model-head"><div><div class="kicker">${{x.region}} · ${{x.teamName}}</div><h1>${{x.name}}</h1><p class="lead2">${{x.summary}}</p></div><div class="datecard"><span>Release node</span><b>${{x.date}}</b><span>${{x.sourceType}}</span></div></header><section class="section"><h2>在团队谱系中的位置</h2><div class="cards"><div class="card2"><b>团队主线</b><span>${{x.thesis}}</span></div><div class="card2"><b>资料状态</b><span>${{x.note?'已有可读笔记':'Overview 已补，独立精读笔记待扩展'}} · ${{x.posters?.length?x.posters.length+' 张 Poster':'独立 Poster 待扩展'}}</span></div><div class="card2"><b>证据边界</b><span>${{x.sourceType}}。未公开的参数、数据、训练 recipe 不作猜测。</span></div></div></section><section class="section"><h2>继续阅读</h2><div class="actions2"><a class="button primary" href="${{x.source}}" target="_blank" rel="noopener">官方一手来源 ↗</a>${{x.note?`<a class="button" href="${{rel(x.note)}}">阅读笔记</a>`:''}}${{(x.posters||[]).map((u,i)=>`<a class="button" href="${{rel(u)}}">${{i===0?'打开 Poster':'Poster '+(i+1)}}</a>`).join('')}}</div>${{!x.note&&!x.posters?.length?'<p class="empty">此节点目前以官方材料 + Overview 为主；后续完成源码/技术报告精读后会在这里补上独立笔记与 Poster。</p>':''}}</section><section class="section"><h2>前后代</h2><div class="prevnext">${{prev?`<a class="next" href="?id=${{prev.slug}}"><small>← 上一代 · ${{prev.date}}</small><br><b>${{prev.name}}</b></a>`:'<div></div>'}}${{next?`<a class="next" href="?id=${{next.slug}}"><small>下一代 · ${{next.date}} →</small><br><b>${{next.name}}</b></a>`:'<div></div>'}}</div></section>`;</script></body></html>'''


def main() -> None:
    add_missing_brainhao_packs()
    teams, records = build_records()
    ATLAS.mkdir(exist_ok=True)
    sync_library(records)
    archive_entries = sync_archive()
    (THINKING / "base_model_atlas.html").write_text(render_index(teams, records), encoding="utf-8")
    (ATLAS / "model.html").write_text(render_detail(records), encoding="utf-8")
    (ATLAS / "library.html").write_text(render_library(archive_entries), encoding="utf-8")
    (ATLAS / "models.json").write_text(json.dumps([{k:v for k,v in r.items() if not k.startswith('_')} for r in records], ensure_ascii=False, indent=2), encoding="utf-8")
    linked_notes = sum(1 for r in records if r.get("note"))
    linked_posters = sum(len(r.get("posters", [])) for r in records)
    print(json.dumps({"teams":len(teams),"models":len(records),"linked_notes":linked_notes,"linked_posters":linked_posters,"archive_items":len(archive_entries)},ensure_ascii=False))


if __name__ == "__main__":
    main()
