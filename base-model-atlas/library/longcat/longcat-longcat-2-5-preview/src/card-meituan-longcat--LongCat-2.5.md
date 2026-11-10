---
license: mit
pipeline_tag: image-text-to-text
tags:
- multimodal
- image-text-to-text
- text-generation
- mixture-of-experts
- agentic
---

# LongCat-2.5

<div align="center">
  <img src="figures/longcat_logo.svg" width="45%" alt="LongCat-2.5" />
</div>
<hr>

<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/meituan-longcat" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-LongCat-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://www.modelscope.cn/organization/meituan-longcat" target="_blank" style="margin: 2px;">
    <img alt="ModelScope" src="https://img.shields.io/badge/%F0%9F%A4%96%20ModelScope-LongCat-624AFF?logo=modelscope&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/meituan-longcat/LongCat-2.5/blob/main/figures/wechat_official_accounts.png" target="_blank" style="margin: 2px;">
    <img alt="Wechat" src="https://img.shields.io/badge/WeChat-LongCat-brightgreen?logo=wechat&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://discord.com/invite/jmuv5TQzKU" target="_blank" style="margin: 2px;">
    <img alt="Discord" src="https://img.shields.io/badge/Discord-Join%20Chat-5865F2?logo=discord&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://x.com/Meituan_LongCat" target="_blank" style="margin: 2px;">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-LongCat-white?logo=x&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/meituan-longcat/LongCat-2.5/blob/main/LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<p align="center">
  <a href="https://longcat.ai/blog/longcat-2.5/"><b>Tech Blog</b>&nbsp;📄</a>
</p>

## Model Introduction

LongCat-2.5 is a native multimodal MoE model for long-horizon agentic tasks, with **1.6 trillion total parameters** and approximately **48 billion activated per token**. Building on LongCat-2.0, it combines visual understanding with agentic coding for complex codebase development, full-project builds, creative design, and 3D tasks. Long-sequence training, large-scale RL, multi-teacher learning, and infrastructure optimizations on domestic AI accelerators underpin these capabilities.

<div align="center">
  <img src="figures/metrics-dashboard.png" width="100%" alt="LongCat-2.5 Benchmark Charts" />
</div>

### LongCat-2.5 Highlights

- **Native Visual Modeling:** Building on [LongCat-Next](https://arxiv.org/abs/2603.27538), native-resolution visual features are converted into discrete tokens and jointly aligned with text in a shared semantic space.

- **Long-Horizon Agentic RL:** Training combines real-world engineering tasks and reproducible agent failures with efficient rollout strategies and safeguards against reward hacking, improving reliable end-to-end task execution.

- **Multi-Teacher Learning:** Specialized agent, reasoning, and interaction teachers guide the model through [full-vocabulary KL distillation](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/DeepSeek_V41_Tech_Report.pdf) and [Tree Attention](https://arxiv.org/pdf/1909.07606), strengthening multi-turn execution, reasoning, instruction following, and safety.

- **Efficient Long-Context Training:** Supernode-aware parallelism, efficient sharding, and communication–computation overlap improve training efficiency, achieving **86% higher per-device throughput than the DDP baseline** in reported long-sequence SFT tasks.

- **RL Infrastructure:** Drawing on community practices, aligned training and inference logic maintains bitwise-identical token log probabilities across training, prefill, and decoding. KV cache optimization and LSA improve serving efficiency, nearly doubling decode KV capacity without increasing TPOT on the tested workload.

For full technical details, see our [blog](https://longcat.ai/blog/longcat-2.5/).

## Evaluation Results

We evaluate LongCat-2.5 across coding, general agent, and visual tasks. Scores marked with `*` are cited from public technical reports, blog posts, or official leaderboards; unmarked scores are measured in-house and are indicative only. `-` indicates an unreported score. See the expandable footnotes below for evaluation settings.

<table>
<thead>
<tr><th align="center">Benchmark</th><th align="center">LongCat-2.5</th><th align="center">LongCat-2.0</th><th align="center">GPT-5.5</th><th align="center">GPT-5.6-Sol</th><th align="center">Claude-Opus-4.8</th><th align="center">Claude-Opus-5</th><th align="center">GLM-5.3</th><th align="center">kimi-k3</th><th align="center">DeepSeek-V4.1-Flash</th></tr>
</thead>
<tbody>
<tr><td colspan="10" align="center"><strong>Code Agent</strong></td></tr>
<tr><td align="center">Terminal Bench v2.1</td><td align="center">88.4</td><td align="center">70.8</td><td align="center">83.2*</td><td align="center">88.8*</td><td align="center">74.6*</td><td align="center">89.1*</td><td align="center">88.2*</td><td align="center">88.3*</td><td align="center">90.6*</td></tr>
<tr><td align="center">Terminal Bench v4.0</td><td align="center">38.5</td><td align="center">3.0</td><td align="center">-</td><td align="center">37.3*</td><td align="center">23.6*</td><td align="center">53.9*</td><td align="center">41.8*</td><td align="center">12.6*</td><td align="center">31.2*</td></tr>
<tr><td align="center">Program Bench (Almost Resolved)</td><td align="center">25.5</td><td align="center">2.5</td><td align="center">13.5*</td><td align="center">23.0*</td><td align="center">16.5*</td><td align="center">37.0*</td><td align="center">19.0*</td><td align="center">17.5*</td><td align="center">20.3*</td></tr>
<tr><td align="center">DeepSWE (v1.1)</td><td align="center">64.6</td><td align="center">9.7</td><td align="center">67.0*</td><td align="center">72.7*</td><td align="center">59.0*</td><td align="center">68.8*</td><td align="center">66.9*</td><td align="center">67.5*</td><td align="center">74.2*</td></tr>
<tr><td align="center">PaperBench</td><td align="center">82.1</td><td align="center">45.2</td><td align="center">80.0</td><td align="center">83.3</td><td align="center">72.9</td><td align="center">79.1</td><td align="center">73.7</td><td align="center">77.5</td><td align="center">-</td></tr>
<tr><td align="center">SWE Atlas - Codebase QnA</td><td align="center">58.3</td><td align="center">33.1</td><td align="center">45.4*</td><td align="center">46.0*</td><td align="center">57.3*</td><td align="center">63.2*</td><td align="center">58.3</td><td align="center">54.3</td><td align="center">55.2</td></tr>
<tr><td align="center">SWE Atlas - Refactoring</td><td align="center">55.2</td><td align="center">35.7</td><td align="center">44.8</td><td align="center">-</td><td align="center">46.7</td><td align="center">51.9</td><td align="center">-</td><td align="center">49.5</td><td align="center">56.7</td></tr>
<tr><td align="center">SWE Atlas - Test Writing</td><td align="center">47.8</td><td align="center">28.0</td><td align="center">42.6</td><td align="center">45.9</td><td align="center">49.6</td><td align="center">62.2</td><td align="center">42.2</td><td align="center">42.2</td><td align="center">48.9</td></tr>
<tr><td align="center">NL2Repo</td><td align="center">60.5</td><td align="center">40.9</td><td align="center">-</td><td align="center">56.8*</td><td align="center">69.7*</td><td align="center">75.3*</td><td align="center">58.0*</td><td align="center">58.0*</td><td align="center">65.4*</td></tr>
<tr><td align="center">LongCat AppDev (Internal)</td><td align="center">73.7</td><td align="center">47.7</td><td align="center">-</td><td align="center">68.8</td><td align="center">-</td><td align="center">76.4</td><td align="center">73.5</td><td align="center">75.1</td><td align="center">-</td></tr>
<tr><td colspan="10" align="center"><strong>General Agent</strong></td></tr>
<tr><td align="center">BrowseComp</td><td align="center">91.9</td><td align="center">79.9</td><td align="center">84.4*</td><td align="center">90.4*</td><td align="center">84.3*</td><td align="center">90.8*</td><td align="center">81.0</td><td align="center">91.2*</td><td align="center">91.5</td></tr>
<tr><td align="center">AutomationBench (v1.0.6)</td><td align="center">51.8</td><td align="center">15.8</td><td align="center">39.7</td><td align="center">45.8*</td><td align="center">41.0*</td><td align="center">50.3*</td><td align="center">48.2*</td><td align="center">46.7*</td><td align="center">54.8*</td></tr>
<tr><td align="center">HLE (w/ tools)</td><td align="center">63.1</td><td align="center">37.5</td><td align="center">52.2</td><td align="center">58.0*</td><td align="center">57.9*</td><td align="center">64.7*</td><td align="center">62.5*</td><td align="center">56.0*</td><td align="center">63.9*</td></tr>
<tr><td align="center">ALE (v1.1)</td><td align="center">38.5</td><td align="center">-</td><td align="center">-</td><td align="center">30.3*</td><td align="center">-</td><td align="center">-</td><td align="center">26.2*</td><td align="center">35.2*</td><td align="center">-</td></tr>
<tr><td align="center">ResearchRubrics</td><td align="center">81.0</td><td align="center">71.9</td><td align="center">-</td><td align="center">74.2</td><td align="center">-</td><td align="center">72.9</td><td align="center">79.9</td><td align="center">78.8</td><td align="center">80.9</td></tr>
<tr><td align="center">MCP Atlas</td><td align="center">83.1</td><td align="center">61.8</td><td align="center">75.3*</td><td align="center">81.8*</td><td align="center">82.2*</td><td align="center">85.8*</td><td align="center">84.2*</td><td align="center">84.2*</td><td align="center">84.4</td></tr>
<tr><td align="center">JobBench</td><td align="center">65.4</td><td align="center">44.4</td><td align="center">38.3*</td><td align="center">45.4*</td><td align="center">48.4*</td><td align="center">66.7*</td><td align="center">61.4*</td><td align="center">52.9*</td><td align="center">63.2</td></tr>
<tr><td align="center">SkillsBench</td><td align="center">63.3</td><td align="center">36.8</td><td align="center">62.6*</td><td align="center">54.1*</td><td align="center">59.2*</td><td align="center">60.4*</td><td align="center">52.9</td><td align="center">-</td><td align="center">69.8*</td></tr>
<tr><td align="center">GDPVal-AA rubrics</td><td align="center">84.8</td><td align="center">72.9</td><td align="center">-</td><td align="center">-</td><td align="center">-</td><td align="center">87.7</td><td align="center">87.7</td><td align="center">86.6</td><td align="center">86.8</td></tr>
<tr><td align="center">FrontierScience</td><td align="center">77.0</td><td align="center">66.0</td><td align="center">-</td><td align="center">-</td><td align="center">-</td><td align="center">78.0</td><td align="center">75.0</td><td align="center">70.0</td><td align="center">73.0</td></tr>
<tr><td align="center">SpreadsheetBench 2</td><td align="center">34.9</td><td align="center">24.1</td><td align="center">30.2</td><td align="center">33.3</td><td align="center">-</td><td align="center">33.0</td><td align="center">35.8</td><td align="center">34.8*</td><td align="center">33.0</td></tr>
<tr><td align="center">FinSearchComp (T3)</td><td align="center">63.4</td><td align="center">42.4</td><td align="center">62.2</td><td align="center">62.2</td><td align="center">-</td><td align="center">64.0</td><td align="center">62.2</td><td align="center">64.0</td><td align="center">64.3</td></tr>
<tr><td align="center">Claw-Eval (Pass^3)</td><td align="center">78.3</td><td align="center">67.1</td><td align="center">-</td><td align="center">79.5</td><td align="center">82.0</td><td align="center">80.8</td><td align="center">73.9</td><td align="center">73.9</td><td align="center">-</td></tr>
<tr><td align="center">LongCatClawBench (FORTE)</td><td align="center">83.3</td><td align="center">72.2</td><td align="center">80.7</td><td align="center">80.6</td><td align="center">80.6</td><td align="center">82.6</td><td align="center">85.6</td><td align="center">86.3</td><td align="center">73.5</td></tr>
<tr><td colspan="10" align="center"><strong>Visual</strong></td></tr>
<tr><td align="center">3DCodeBench (Text→3D)</td><td align="center">55.4</td><td align="center">-</td><td align="center">51.9</td><td align="center">52.3</td><td align="center">52.7</td><td align="center">54.3</td><td align="center">53.4</td><td align="center">49.3</td><td align="center">53.3</td></tr>
<tr><td align="center">Vision2Web</td><td align="center">78.6</td><td align="center">-</td><td align="center">74.6</td><td align="center">73.5*</td><td align="center">76.1*</td><td align="center">80.2*</td><td align="center">77.8*</td><td align="center">79.0*</td><td align="center">79.2</td></tr>
<tr><td align="center">CharXiv-RQ (w/ tools)</td><td align="center">90.2</td><td align="center">-</td><td align="center">89.0*</td><td align="center">89.1*</td><td align="center">89.9*</td><td align="center">89.3*</td><td align="center">-</td><td align="center">91.3*</td><td align="center">87.7</td></tr>
<tr><td align="center">MathVision (w/ tools)</td><td align="center">96.5</td><td align="center">-</td><td align="center">96.8*</td><td align="center">97.8*</td><td align="center">97.1*</td><td align="center">-</td><td align="center">-</td><td align="center">97.8*</td><td align="center">97.4</td></tr>
<tr><td align="center">VideoMME</td><td align="center">85.2</td><td align="center">-</td><td align="center">-</td><td align="center">89.5*</td><td align="center">86.0*</td><td align="center">-</td><td align="center">-</td><td align="center">90.0*</td><td align="center">-</td></tr>
<tr><td align="center">PosterBench</td><td align="center">77.4</td><td align="center">-</td><td align="center">-</td><td align="center">-</td><td align="center">82.3</td><td align="center">-</td><td align="center">82.4</td><td align="center">76.8</td><td align="center">75.3</td></tr>
<tr><td align="center">LongCatClawBench-MM (FORTE-MM)</td><td align="center">72.1</td><td align="center">-</td><td align="center">63.5</td><td align="center">73.2</td><td align="center">69.9</td><td align="center">73.1</td><td align="center">69.0</td><td align="center">70.7</td><td align="center">72.8</td></tr>
</tbody>
</table>

<details>
<summary><b>Footnotes: Evaluation Settings</b></summary>

Unless otherwise specified, all LongCat-2.5 results use `enable_thinking=on`, `temperature=1.0`, and `top_p=0.95`.

**Coding**

1. Terminal Bench v4.0 / v2.1, Program Bench, NL2Repo: Claude Code harness (v2.1.280) with max_seq_length = 512K; Terminal Bench v2.1 results are averaged over three independent runs.
2. DeepSWE v1.1: mini-swe-agent at temperature = 1.0, top_p = 0.95 and max_seq_length = 1M; results are averaged over three independent runs.
3. SWE Atlas - Codebase QnA and Test Writing: Claude Code (v2.1.116) with Claude Opus 4.5 as the judge (majority vote over three judgments); results are averaged over three independent runs.

**Agentic**

4. BrowseComp: Custom lightweight harness with Verify and Discard-All modules (Discard-All threshold 256K), capped at 1,024 exploration rounds; only the `search` and `browse_with_goal` tools are available.
5. HLE w/ tools: Full set, evaluated with Claude Code (v2.1.116); maximum generation length 256K tokens.
6. MCP Atlas: Reasoning effort set to "max", temperature = 0.7, top_p = 0.95, 256K context.
7. AutomationBench (public v1.0.6): All 600 public tasks, evaluated with the benchmark's official evaluation code; temperature = 1.0, top_p = 0.95.
8. JobBench (Main 65): Claude Code harness (v2.1.280); scoring follows the official JobBench LLM-as-judge protocol (chained rubrics over the submitted deliverables) with gemini-3.6-flash as the judge; temperature = 1.0, top_p = 0.95, thinking enabled.
9. SpreadsheetBench 2: Claude Code harness (v2.1.116), scoring follows the benchmark's official protocol; the Visualization subset is judged by gemini-3.6-flash, with charts rendered on Linux via headless LibreOffice (UNO object-level export) and a pure-Python OOXML/Pillow renderer as fallback.
10. SkillsBench v1.1 (87 tasks): Evaluated with the Codex harness at temperature = 1.0, top_p = 0.95 and top_k = -1.

**Visual**

11. Vision2Web: Claude Code (v2.1.7) at temperature = 1.0, top_p = 0.95, top_k = 50 and a sequence length of 256K.
12. VideoMME: At most 2,048 frames sampled per video (1 fps) and at most 256 tokens per frame, with thinking mode enabled, using the prompt "Answer with the option's letter from the given choices directly. You can only answer one letter from A, B, C, or D."
13. CharXiv-RQ (w/ tools) and MathVision (w/ tools): Temperature = 1.0 and top_p = 0.95, with a maximum generation length of 131,972 tokens.

</details>

## Quantization

LongCat-2.5 applies W4A4 quantization to expert weights and activations, enabling native INT4 computation on domestic AI accelerators. Using FlatQuant-style learnable transformations, it maintains accuracy comparable to the unquantized model on evaluated benchmarks. A shared expert-input transformation enables quantization to be applied prior to token replication and dispatch, allowing the same INT4 representation to be reused across communication and computation. Fused kernels for transformation, scaling, quantization, and packing, together with optimized weight layouts and separately tuned prefill/decode pipelines, reduce data movement and communication overhead.

Compared with a W8A8 MoE baseline, online stress tests show 43.3% higher prefill throughput, 42.77% higher decode throughput, 15.91% lower TTFT, and 19.72% lower TPOT. Grouped GEMM (GMM) kernels achieve an average 1.73× speedup over W8A8. Combined with KV cache quantization, W4A4KV8 delivers 92% higher decode throughput than W8A8KV16.

## Deployment

LongCat-2.5 can be deployed on NPU platforms.

### NPU

For NPU deployment, please refer to [SGLang-FluentLLM](https://github.com/meituan-longcat/SGLang-FluentLLM/blob/longcat-2.5-npu/npu_test/ReadMe.md).

## Model Usage

LongCat-2.5 is a hybrid model that supports both thinking mode and non-thinking mode.
- Thinking mode on(`enable_thinking=True`), keeping all reasoning content(`save_history_reasoning_content=True`) for better performance.
- Thinking mode off(`enable_thinking=False`), for better token efficiency.

```python
import openai

def chat_with_thinking_mode_on_and_keeping_all_reasoning_content(client: openai.OpenAI, model_name: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_book_price",
                "description": "Look up a book's current price and stock in the bookstore catalog.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Book title as printed on the cover"
                        },
                        "edition": {
                            "type": "string",
                            "description": "Edition printed on the cover, if visible"
                        }
                    },
                    "required": ["title"]
                }
            }
        }
    ]

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in the picture?"},
                {"type": "image_url", "image_url": { "url": "./assets/book.png"}}
            ]
        },
        {
            "role": "assistant",
            "content": "The picture shows the cover of the novel **\"To Kill a Mockingbird\" by Harper Lee** — specifically the **65th Anniversary Edition** published by Penguin Books.\n\nKey details visible:\n- **Cover art:** A black silhouette of a child lying on a large tire swing hanging from a tree branch, set against a cream/off-white background\n- **Title and author:** Written in a hand-drawn, brushstroke-style font\n- **Gold seal:** Reads \"Over 42 million copies sold worldwide\" and \"65th Anniversary Edition\"\n- **Spine:** Shows the title, author's name, and the classic orange Penguin Books logo (also repeated at the bottom right of the front cover)",
            "reasoning_content": "\nThe user is asking what's in the picture. I can see it's a book cover of \"To Kill a Mockingbird\" by Harper Lee. Let me describe the details visible: it's a 65th Anniversary Edition, with a black silhouette illustration of a child on a tire swing hanging from a tree branch, the title in handwritten-style lettering, author's name Harper Lee, a gold seal indicating \"Over 42 million copies sold worldwide\" and \"65th Anniversary Edition\", and Penguin Books logo (orange oval with penguin) at the bottom. The spine shows the title, author, and penguin logo as well.\n\nThis is a simple image description question, so a concise answer is appropriate."
        },
        {
            "role": "user",
            "content": "How much is this book?"
        },
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_b96937c91aee4ede9d92c043",
                    "index": 0,
                    "type": "function",
                    "function": {
                        "name": "get_book_price",
                        "arguments": "{\"title\": \"To Kill a Mockingbird\", \"edition\": \"65th Anniversary Edition\"}"
                    }
                }
            ],
            "reasoning_content": "\nThe user is asking about the price of the book shown in the image. I have access to a tool called get_book_price that can look up a book's current price and stock. The book is \"To Kill a Mockingbird\" by Harper Lee, 65th Anniversary Edition.\n\nI should use the tool to look up the price. The edition visible is the 65th Anniversary Edition."
        },
        {
            "role": "tool",
            "tool_call_id": "call_b96937c91aee4ede9d92c043",
            "name": "get_book_price",
            "content": "{\"price\": \"US $19.09\", \"source\": \"ebay\"}"
        }
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        stream=False,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": True,
                "save_history_reasoning_content": True,
            }
        },
    )
    
    message = response.choices[0].message
    print(f"reasoning_content: {getattr(message, 'reasoning_content', None)}")
    return message.content

```


## Chat Website
You can chat with LongCat-2.5 on our official website: [https://longcat.ai/](https://longcat.ai/).

## License Agreement

The **model weights** are released under the **MIT License**.

Any contributions to this repository are licensed under the MIT License, unless otherwise stated. This license does not grant any rights to use Meituan trademarks or patents.

See the [LICENSE](https://huggingface.co/meituan-longcat/LongCat-2.5/blob/main/LICENSE) file for the full license text.

## Usage Considerations
This model has not been specifically designed or comprehensively evaluated for every possible downstream application.

Developers should take into account the known limitations of large language models, including performance variations across different languages, and carefully assess accuracy, safety, and fairness before deploying the model in sensitive or high-risk scenarios.
It is the responsibility of developers and downstream users to understand and comply with all applicable laws and regulations relevant to their use case, including but not limited to data protection, privacy, and content safety requirements.

Nothing in this Model Card should be interpreted as altering or restricting the terms of the MIT License under which the model is released.

## Contact
Please contact us at <a href="mailto:longcat-team@meituan.com">longcat-team@meituan.com</a> or open an issue if you have any questions.

---
