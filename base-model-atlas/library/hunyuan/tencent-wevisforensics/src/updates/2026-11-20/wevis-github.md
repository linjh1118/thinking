<div align="center">

# WeVisForensics

### Self-Evolving Agent for Omni AI-Generated Video Detection

<p>
  <a href="https://tencent.github.io/WeVisForensics"><img src="https://img.shields.io/badge/Project-Page-4285F4?logo=googlechrome&logoColor=white" alt="Project Page"></a>
  <a href="https://arxiv.org/abs/2611.21373"><img src="https://img.shields.io/badge/Paper-arXiv-EA4335?logo=arxiv&logoColor=white" alt="Paper"></a>
  <a href="https://huggingface.co/tencent/WeVisForensics"><img src="https://img.shields.io/badge/🤗%20Model-WeVisForensics--4B-FBBC04" alt="WeVisForensics-4B"></a>
  <a href="LICENSE.txt"><img src="https://img.shields.io/badge/License-Apache%202.0-blue" alt="License"></a>
</p>

**English** | [简体中文](README_zh-CN.md)

</div>

> **WeVisForensics** treats AI-generated video detection as an investigation. A main agent, the **investigator**, watches a coarse overview and decides which artifact to examine, over which window, and when to conclude. It dispatches each inspection to a self-evolving library of forensic sub-agents, the **inspectors**, that cover visual appearance, physical consistency, common sense, on-screen text, and the audio track.

![Teaser](assets/teaser.png)

## ✨ Highlights

- 🕵️ **Adaptive investigation**: the investigator calls only the inspectors a video needs, at the moments that matter, and stops as soon as the evidence is decisive.
- 🧰 **Omni-modal inspector library**: four trained visual inspectors plus speech and speaker tools, so the same agent catches rendering artifacts, broken physics, impossible events, warped text, and mismatched voices.
- 🔁 **Self-evolving training (DTPO)**: the investigator and its inspectors co-evolve from shared interactions, with fast reinforcement learning for the investigator and slower refinement of the inspectors.
- 🏆 **State of the art**: 95.2% average accuracy across in-domain, out-of-domain, and agentic benchmarks, 9.0 points above the strongest prior detector.

## 📢 News

- **[2026-11]** 🎉 We release **WeVisForensics**: the technical report, the 4B LoRA weights, the inference package and the Gradio demo.

## 📝 TODO

- [x] Inference package
- [x] Gradio demo
- [x] Evaluation pipeline
- [x] Technical report on arXiv
- [ ] Model weights on Hugging Face
- [ ] AgenticCue benchmark

## 🏆 Performance at a Glance

Headline detection accuracy (%) of **WeVisForensics-4B** against the strongest prior method on each benchmark (such as Qwen3.5-397B, Gemini-3.1-Pro, and MLLM-based video forgery detectors like BusterX++, Skyra and VideoVeritas).

| Split | Benchmark | Best Baseline | **WeVisForensics** |
| --- | --- | --- | --- |
| 🏠 In-domain | GenBuster-Bench | 94.3 | **97.7** |
| 🌍 Out-of-domain | GenBuster-Bench++ | 91.4 | **97.5** |
| 🌍 Out-of-domain | MintVid General | 82.2 | **88.0** |
| 🧩 Agentic | AgenticCue | 79.3 | **97.8** |
| ⭐ | Average | 86.2 | **95.2** |

<sub>Each benchmark row reports the strongest prior detector on that benchmark. The Average row is the best average over prior detectors.</sub>

<details>
<summary><b>📊 Full results (click to expand)</b></summary>

<table>
<thead>
<tr><th rowspan="2" align="left">Method</th><th rowspan="2">GB</th><th rowspan="2">GB++</th><th colspan="6">MintVid General</th><th colspan="5">AgenticCue</th><th rowspan="2">Avg.</th></tr>
<tr><th>Hailuo</th><th>Jimeng</th><th>Kling</th><th>Seedance</th><th>Sora2</th><th>Wan2.5</th><th>Visual</th><th>Physical</th><th>OCR</th><th>Common</th><th>Audio</th></tr>
</thead>
<tbody>
<tr><td colspan="15" align="left"><i>Binary detectors</i></td></tr>
<tr><td align="left">NSG-VD</td><td>46.4</td><td>53.7</td><td>57.1</td><td>48.5</td><td>52.6</td><td>54.7</td><td>57.1</td><td>51.0</td><td>41.7</td><td>43.2</td><td>41.7</td><td>34.2</td><td>44.4</td><td>48.7</td></tr>
<tr><td align="left">ReStraV</td><td>51.9</td><td>66.9</td><td>59.5</td><td>56.8</td><td>55.6</td><td>64.0</td><td>50.8</td><td>54.9</td><td>55.5</td><td>54.6</td><td>51.6</td><td>47.0</td><td>51.8</td><td>57.0</td></tr>
<tr><td colspan="15" align="left"><i>Generic MLLMs</i></td></tr>
<tr><td align="left">Qwen3.5-4B</td><td>82.9</td><td>73.2</td><td>63.5</td><td>56.5</td><td>65.1</td><td>73.8</td><td>57.0</td><td>73.2</td><td>73.7</td><td>71.8</td><td>83.8</td><td>94.4</td><td>58.1</td><td>74.3</td></tr>
<tr><td align="left">Qwen3.5-397B</td><td>65.1</td><td>66.7</td><td>54.7</td><td>52.0</td><td>55.8</td><td>63.0</td><td>51.4</td><td>63.4</td><td>69.2</td><td>66.7</td><td>86.0</td><td>94.5</td><td>54.1</td><td>65.7</td></tr>
<tr><td align="left">Qwen3-VL-8B</td><td>44.8</td><td>55.2</td><td>52.0</td><td>50.4</td><td>50.5</td><td>63.0</td><td>52.6</td><td>55.9</td><td>61.7</td><td>58.6</td><td>72.2</td><td>91.9</td><td>47.8</td><td>55.1</td></tr>
<tr><td align="left">Qwen3-Omni-30B-A3B</td><td>50.7</td><td>55.2</td><td>51.7</td><td>51.9</td><td>52.9</td><td>61.4</td><td>54.6</td><td>56.3</td><td>57.5</td><td>54.8</td><td>70.6</td><td>85.6</td><td>43.1</td><td>55.8</td></tr>
<tr><td align="left">Gemini-3.1-Pro</td><td>69.4</td><td>54.3</td><td>55.1</td><td>54.4</td><td>54.6</td><td>45.3</td><td>48.6</td><td>54.9</td><td>61.8</td><td>61.6</td><td>63.4</td><td>63.4</td><td>63.1</td><td>59.6</td></tr>
<tr><td colspan="15" align="left"><i>MLLM-based video forgery detectors</i></td></tr>
<tr><td align="left">BusterX++</td><td>70.1</td><td>79.6</td><td>70.4</td><td>71.7</td><td>82.3</td><td>71.8</td><td>58.7</td><td><b>87.3</b></td><td>64.4</td><td>65.1</td><td>71.1</td><td>87.1</td><td>49.9</td><td>72.7</td></tr>
<tr><td align="left">DeepTraceReward</td><td>76.4</td><td>58.8</td><td>64.5</td><td>64.1</td><td>63.9</td><td>56.5</td><td>59.3</td><td>65.5</td><td>55.5</td><td>54.2</td><td>51.9</td><td>55.4</td><td>53.5</td><td>62.9</td></tr>
<tr><td align="left">Skyra-RL</td><td>68.2</td><td>55.7</td><td>51.7</td><td>51.7</td><td>53.5</td><td>63.4</td><td>50.6</td><td>59.6</td><td>83.4</td><td>83.8</td><td>74.0</td><td>86.9</td><td>68.5</td><td>64.6</td></tr>
<tr><td align="left">VideoVeritas</td><td>94.3</td><td>91.4</td><td>85.8</td><td>80.8</td><td>86.0</td><td>86.6</td><td>67.6</td><td>86.3</td><td>72.4</td><td>75.3</td><td>76.0</td><td>91.5</td><td>69.3</td><td>86.2</td></tr>
<tr><td align="left">ARGUS</td><td>86.4</td><td>78.9</td><td>61.8</td><td>56.5</td><td>65.1</td><td>67.6</td><td>56.1</td><td>73.5</td><td>73.3</td><td>71.1</td><td>80.4</td><td>90.5</td><td>64.2</td><td>76.2</td></tr>
<tr><td colspan="15" align="left"><i>Agentic investigation</i></td></tr>
<tr><td align="left">WeVisForensics-SFT</td><td>93.9</td><td>94.2</td><td>83.8</td><td>77.9</td><td>82.1</td><td>95.6</td><td>75.9</td><td>82.5</td><td>92.4</td><td>94.2</td><td>93.6</td><td>96.0</td><td>95.2</td><td>91.3</td></tr>
<tr><td align="left"><b>WeVisForensics-DTPO</b></td><td><b>97.7</b></td><td><b>97.5</b></td><td><b>88.9</b></td><td><b>82.9</b></td><td><b>89.6</b></td><td><b>98.6</b></td><td><b>82.4</b></td><td>85.6</td><td><b>97.3</b></td><td><b>98.0</b></td><td><b>98.0</b></td><td><b>98.8</b></td><td><b>97.0</b></td><td><b>95.2</b></td></tr>
</tbody>
</table>

</details>

## 🏗️ How It Works

![Overview](assets/overview.png)

**1. Investigator.** The main agent reads a 1 FPS overview of up to 16 frames and, at each step, emits one JSON action: call an inspector on a time window, or answer `real` / `fake`. It reads each observation before deciding what to examine next, and concludes within five steps.

**2. Forensic sub-agent library.** Each inspector focuses on one artifact type, decodes its own window at 2 FPS and returns a verdict, a confidence, and a short report of what it saw.

| Inspector | Looks at | Checks |
| --- | --- | --- |
| 🎨 `visual_appearance` | a time window | texture, boundaries, flicker, lighting |
| ⚙️ `physical_consistency` | a time window | motion, anatomy, contact, materials |
| 🧠 `common_sense` | a time window | causality, affordance, event order |
| 🔤 `ocr_consistency` | one moment | text detection, then a glyph check on each crop |
| 🗣️ `voice_profile` | the audio track | speaker age, gender, and affect against the visible speaker |
| 📝 `asr_analysis` | the audio track | transcript content and timing |

**3. Dual-timescale co-evolution (DTPO).** Interactions feed both levels: the investigator learns fast, through reinforcement learning with call-level credit for inspections worth making; the inspectors refine slowly, guided by annotated artifact intervals, to report subtle artifacts they once dismissed.

![DTPO](assets/method.png)

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Tencent/WeVisForensics.git && cd WeVisForensics
conda create -n wevisforensics python=3.10 -y && conda activate wevisforensics
conda install -c conda-forge ffmpeg -y
pip install -r requirements.txt && pip install -e .
```

WeVisForensics can be deployed in three ways. The multi-GPU setup gives each inspector its own vLLM server and suits large-scale evaluation. The single-GPU setup runs everything on one card and is the easiest way to try it locally. The Transformers setup needs no vLLM and backs the Gradio demo and the Hugging Face Space.

### Option 1: Multi-GPU deployment

Merge the adapters, serve each inspector on its own GPU, and run the investigator in-process:

```bash
python scripts/merge_lora.py --base Qwen/Qwen3.5-4B \
  --adapters weights/WeVisForensics-4B-LoRA --output weights/WeVisForensics-4B-merged

MODEL_ROOT=weights/WeVisForensics-4B-merged ASR_MODEL=Qwen/Qwen3.5-4B \
  GPUS=0,1,2,3,4 bash scripts/serve_full.sh
```

Point `engine.model` in `configs/multi_server.json` at `weights/WeVisForensics-4B-merged/main`, then run:

```bash
python scripts/infer.py demo/examples/c04559bab78f9a8b5b7e.mp4
```

See [docs/deployment.md](docs/deployment.md) for details.

### Option 2: Single-GPU deployment

Here the investigator and all inspectors share one base model, switching between LoRA adapters inside a single vLLM process, so no merge step is needed. A single 24 GB GPU is enough:

```bash
BASE=Qwen/Qwen3.5-4B ADAPTERS=weights/WeVisForensics-4B-LoRA \
  GPU_MEMORY_UTILIZATION=0.66 bash scripts/serve_lora.sh

python scripts/infer.py demo/examples/c04559bab78f9a8b5b7e.mp4 \
  --config configs/lora_single_server.json --main-backend http
```

### Option 3: Transformers (Gradio demo / Hugging Face Space)

The whole agent runs in-process with Transformers on one GPU with at least 24 GB. The investigator and the four visual inspectors share one copy of the base model, and the active role's adapter is merged into its weights before each call. OCR runs on CPU, so the same code also fits ZeroGPU. It pins its own PyTorch, so use a separate environment:

```bash
pip install -r demo/requirements.txt "gradio>=6.0"
WVF_ADAPTERS=weights/WeVisForensics-4B-LoRA python demo/app.py
```

Upload a video, pick a window of up to 16 s, and follow the investigation step by step. To deploy it as a Space, upload the contents of `demo/` as the Space root; settings are listed in [demo/README.md](demo/README.md).

### Python API

```python
import asyncio
from main_agent import build_agent, load_config

agent = build_agent(load_config("configs/multi_server.json"))
# Single GPU: build_agent(load_config("configs/lora_single_server.json"), main_backend="http")
trajectory = asyncio.run(agent.run("demo/examples/c04559bab78f9a8b5b7e.mp4"))

print(trajectory.answer)            # "real" or "fake"
for step in trajectory.steps:       # every action, inspector call, and observation
    print(step["action"], step.get("observation"))
```

## 🎮 Gradio Demo

Live analysis runs on the Transformers backend of [Option 3](#option-3-transformers-gradio-demo--hugging-face-space). To browse the ten recorded investigations in `demo/examples/` without a GPU:

```bash
pip install "gradio>=6.0"
WVF_LOCAL=0 python demo/app.py
```

## 📊 Evaluation

See [evaluation/README.md](evaluation/README.md).

## 🖼️ Representative Visualizations

Turn-by-turn rollouts of WeVisForensics on held-out videos, covering visual appearance, physical consistency, OCR, common sense, voice profile and real videos, are available on our [project page](https://tencent.github.io/WeVisForensics/#demo).

## 📖 Citation

If WeVisForensics is helpful to your work, please consider giving us a ⭐ and citing:

```bibtex
@misc{du2026wevisforensicsselfevolvingagentomni,
      title={WeVisForensics: Self-Evolving Agent for Omni AI-Generated Video Detection}, 
      author={Yipeng Du and Yuxi Li and Ying Zhang and Chong Sun and Chen Li and Jing Lyu and Ying Tai},
      year={2026},
      eprint={2611.21373},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2611.21373}, 
}
```

## 📜 License

WeVisForensics is released under the [Apache-2.0 License](LICENSE.txt). Third-party components keep their original licenses.
