---
title: "GLM-TTS Technical Report"
type: paper
authors: ["Jiayan Cui", "Zhihan Yang", "Naihan Li", "Jiankun Tian", "Xingyu Ma", "Yi Zhang", "Guangyu Chen", "Runxuan Yang", "Zijian Huang", "Yuqing Cheng", "Yizhi Zhou", "Guochen Yu", "Xiaotao Gu", "Jie Tang"]
year: 2025
venue: arXiv
arxiv: "2512.14291"
url: "https://arxiv.org/abs/2512.14291"
tags: [paper, glm, tts, speech-synthesis, reinforcement-learning]
topic: "13_base_model"
status: read
rating: 4
created: 2026-05-30
---

# TL;DR

GLM-TTS 是一个生产级 TTS 系统，仅用 **100k 小时**训练数据（远低于 CosyVoice3 的 1M 小时），通过两阶段架构（Text-to-Token AR + Token-to-Waveform Diffusion）和 **GRPO 多 reward RL** 在开源 benchmark 上达到 SOTA；其 LoRA 声音定制只需 15% 参数 + 1 小时单说话人音频，Phoneme-in 机制解决多音字/罕见字发音控制问题。

## 问题与动机

当前 SOTA TTS 系统面临五大挑战：
1. 高质量 voice cloning 需要大规模训练数据和长参考录音
2. 情感表现力受限，大多数模型依赖显式情感标签
3. 多音字、罕见字、方言发音精度不足（尤其中文）
4. RL 在 TTS 中未被充分探索（reward 设计难 + 训练不稳定）
5. 顶级/个性化声音适配依赖全量微调，成本高

## 方法核心思路

### 架构：两阶段生成
- **Stage 1: Text-to-Token AR Model**：将文本转为离散 speech token（25Hz, 32k vocab）
- **Stage 2: Token-to-Waveform Diffusion (Vocos2D)**：将 token 重建为波形

### Speech Tokenizer 优化（基于 Whisper-VQ）
- Token rate: 12.5Hz → **25Hz**，vocab: 16k → **32k**，减少高速发音 glitch，改善笑声/呼吸等副语言特征自然度
- **Pitch Estimator (PE) Module**：提升 pitch 建模精度，改善克隆 TTS 与参考音频的韵律对齐
- **Non-Causal Architecture**：移除 block attention 和因果卷积，提升 ASR 和 PE 模块精度
- **Expanded Training Data**：加入大方言数据集和高音质歌唱数据

### Text Tokenizer：Vocabulary Pruning
去除由两个以上中文字符组成的 token，降低语义-声学对齐难度，将 text-to-acoustic length ratio 分布中心化。

### GRPO Multi-Reward RL（核心创新）
四个 reward 融合：
- **CER**：发音准确度
- **SIM**：音色相似度
- **Emotion**：情感自然度
- **Laughter**：副语言真实感（ASR 转写为空则 reward=1，否则=0）

关键训练技术：
- **多维正则化奖励机制**：分层处理（individual reward regularization → weighted fusion → overall regularization）
- **动态采样**：当 batch reward 同质化时自动重采样（最多 3 次），避免梯度消失
- **自适应梯度裁剪**（Clip-Higher）：$\epsilon_{high}$ 和 $\epsilon_{low}$ 随训练步动态调整——早期严格防止 reward hacking，后期放松鼓励探索；设 $\epsilon_{high} > \epsilon_{low}$ 鼓励生成低概率 token

### LoRA 声音定制
- 只调 15% 参数（≈全量微调效果）
- 最低 1 小时单说话人音频
- 相比初始探索（只调 0.3%-5% 参数效果有限），15% 是稳定 production 门槛

### Phoneme-in 精确发音控制
- **Hybrid Phoneme + Text 输入**：标准字符 20% 概率替换为 phoneme；多音字/罕见字保留原文本但通过 G2P 提供 phoneme sequence
- 推理时：polyphone/rare char → phoneme 替换 → 模型输入为混合模态
- 在 hard case 数据集上：PER 从 13.23% → **5.14%**

### Vocos2D Vocoder
- 核心改进：将 1D 卷积替换为 **2D 卷积**处理频率子带
- 去掉 Multi-Period Discriminator（对高频 Bin 的 linear spectrogram 有害）
- 加 Discriminator Augmentation (DA)：只对 Discriminator 用数据增强，梯度回传到 Generator 但不强迫 Generator 建模增强

## 关键结果

### Seed-TTS-eval Benchmark

| Model | Params | CER (zh) ↓ | SIM (zh) ↑ | WER (en) ↓ | SIM (en) ↑ |
|-------|--------|-----------|-----------|-----------|-----------|
| MiniMax-Speech | - | 0.83 | 78.3 | 1.65 | 69.2 |
| Seed-TTS | - | 1.12 | **79.6** | 2.25 | **76.2** |
| CosyVoice3 (开源) | 0.5B | 1.16 | 78.0 | 2.02 | 71.8 |
| **GLM-TTS** | 1.5B | 1.03 | 76.1 | 2.23 | 67.2 |
| **GLM-TTS_RL** | 1.5B | **0.89** | 76.4 | 1.91 | 68.1 |

GLM-TTS 在 1.5B 开源模型中达到 top-tier，RL 后 CER=0.89% 接近最优。

### Vocos2D vs Vocos

| Metric | GT | Vocos | Vocos2D |
|--------|-----|-------|---------|
| NISQA ↑ | 3.47 | 3.16 | **3.40** |
| UTMOS ↑ | 2.11 | 1.87 | **1.91** |
| MOS ↑ | 4.77 | 3.58 | **4.16** |

### Phoneme-in 消融
PER: 13.23% → **5.14%**（hard case dataset）

## 对研究的启发

> [!insight]
> 1. **GRPO 多 reward RL 在 TTS 的可行路径**：Clip-Higher + 动态采样 + 自适应梯度裁剪三合一，解决了 TTS RL 训练不稳定和 reward hacking 的核心痛点。这对语音/音频生成领域的 RL 应用有直接参考价值
> 2. **数据效率**：100k 小时 vs 1M+ 小时达到同等质量，说明数据清洗/质量比数量更重要
> 3. **Phoneme-in 机制**：对需要精确发音控制的垂直场景（教育/医疗/金融）很有价值，用 20% 概率替换 + 离线路由即可实现，无需复杂 G2P 在线预测
> 4. **副语言特征（笑声/呼吸）RL**：将 ASR 转写为空作为正 reward signal，是处理非文本内容的聪明做法

## 相关链接
- 论文: [arXiv 2512.14291](https://arxiv.org/abs/2512.14291)
- 源码: [github.com/zai-org/GLM-TTS](https://github.com/zai-org/GLM-TTS)
- Demo: [audio.z.ai](https://audio.z.ai/)
