---
title: "Base Model 汇总 v2 — 可视化全景图"
type: summary
tags: [moc, base-model, summary, foundation-model, visualization]
created: 2026-06-01
updated: 2026-06-01
---

# Base Model 汇总 v2 — 2025-2026 大模型基座全景

> 📅 **时间窗口**: 2025-02 至 2026-06
> **来源**: 27 份精读笔记 + 31 份 web-clipping
> **覆盖**: 国内 5 家 + 国外 4 家 + 1 个研究主线

> 💡 **使用提示**：下面的 HTML 块是完整的可视化版本（含卡片、配色、时间线），点击右上角折叠图标可收起 / 展开。底部 markdown 保留了 wikilink 关联主题和数据来源统计。

---

<details>
<summary>🎨 <b>展开 / 收起 HTML 可视化版本</b>（含暗色主题、卡片式布局、4 大主线时间线）</summary>

<div style="background: #0f1117; color: #e2e8f0; padding: 32px 24px; border-radius: 12px; margin: 16px 0; font-family: -apple-system, 'Segoe UI', sans-serif;">

<!-- Hero -->
<div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #4338ca 70%, #6d28d9 100%); padding: 40px 36px; border-radius: 14px; margin-bottom: 28px; position: relative; overflow: hidden;">
  <div style="position: absolute; top: -100px; right: -100px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(167,139,250,0.3) 0%, transparent 70%); border-radius: 50%;"></div>
  <div style="position: absolute; bottom: -80px; left: 20%; width: 240px; height: 240px; background: radial-gradient(circle, rgba(96,165,250,0.2) 0%, transparent 70%); border-radius: 50%;"></div>
  <div style="position: relative; z-index: 1;">
    <div style="display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 20px; padding: 4px 14px; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; margin-bottom: 16px;">2025-02 → 2026-06</div>
    <h1 style="font-size: 32px; font-weight: 800; margin: 0 0 12px 0; color: white; line-height: 1.2;">Base Model 全景图</h1>
    <p style="font-size: 15px; color: rgba(255,255,255,0.85); margin: 0 0 20px 0; line-height: 1.6; max-width: 720px;">2025-2026 的"百模大战"已收敛为四条主线 —— <b style="color: #c4b5fd;">Reasoning 入基座</b>、<b style="color: #93c5fd;">Agentic RL 范式成熟</b>、<b style="color: #86efac;">全模态原生</b>、<b style="color: #fcd34d;">Coding Agent 主战场</b>。</p>
    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
      <div style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; padding: 10px 18px;">
        <div style="font-size: 22px; font-weight: 800; color: white;">58</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.7);">模型 / 剪藏</div>
      </div>
      <div style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; padding: 10px 18px;">
        <div style="font-size: 22px; font-weight: 800; color: white;">9</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.7);">家公司</div>
      </div>
      <div style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; padding: 10px 18px;">
        <div style="font-size: 22px; font-weight: 800; color: white;">4</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.7);">条主线</div>
      </div>
    </div>
  </div>
</div>

<!-- 关键判断 -->
<div style="background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(96,165,250,0.08)); border: 1px solid rgba(167,139,250,0.3); border-radius: 10px; padding: 18px 22px; margin-bottom: 32px;">
  <div style="font-size: 11px; font-weight: 700; color: #a78bfa; letter-spacing: 0.1em; margin-bottom: 6px;">⭐ 关键判断</div>
  <div style="font-size: 15px; color: #e2e8f0; line-height: 1.7;"><b style="color: #c4b5fd;">Agent Foundation Model</b> 概念已成型 —— Seed1.8/2.0、GLM-4.5/5.1、MiniMax-M2/M3、Qwen3-Coder-Next 都明确表态：未来 base model 不再只是"通用对话基座"，而是<b>为 agent 场景优化的预训练基座</b>。</div>
</div>

<!-- 4 大主线时间线 -->
<div style="margin-bottom: 40px;">
  <h2 style="font-size: 20px; font-weight: 700; color: #c4b5fd; margin: 0 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(167,139,250,0.3);">📐 4 大主线演进</h2>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
    <div style="background: rgba(96,165,250,0.08); border-left: 3px solid #60a5fa; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 11px; color: #60a5fa; font-weight: 700; letter-spacing: 0.05em;">REASONING</div>
      <div style="font-size: 14px; color: #e2e8f0; font-weight: 600; margin: 4px 0;">从 CoT prompting → RL 训练 → 预训练目标</div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5;">o1/R1 → Qwen3/M1/Gemini2.5 → GLM-4.5/GPT-5 → Claude4.5+ → Deep Think</div>
    </div>
    <div style="background: rgba(167,139,250,0.08); border-left: 3px solid #a78bfa; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 11px; color: #a78bfa; font-weight: 700; letter-spacing: 0.05em;">AGENTIC RL</div>
      <div style="font-size: 14px; color: #e2e8f0; font-weight: 600; margin: 4px 0;">PPO → GRPO → CISPO → Verification / Swarm</div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5;">DeepSeek → MiniMax-M1 → K2/rStar2 → MiroThinker-H1 / K2.5 Swarm</div>
    </div>
    <div style="background: rgba(134,239,172,0.08); border-left: 3px solid #86efac; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 11px; color: #86efac; font-weight: 700; letter-spacing: 0.05em;">MULTIMODAL</div>
      <div style="font-size: 14px; color: #e2e8f0; font-weight: 600; margin: 4px 0;">"模态不降智"成为核心 KPI</div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5;">Qwen3-Omni Thinker-Talker / K2.5 Joint Opt / GLM-4.5V / Gemini 3</div>
    </div>
    <div style="background: rgba(252,211,77,0.08); border-left: 3px solid #fcd34d; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 11px; color: #fcd34d; font-weight: 700; letter-spacing: 0.05em;">CODING AGENT</div>
      <div style="font-size: 14px; color: #e2e8f0; font-weight: 600; margin: 4px 0;">HumanEval → SWE-bench Verified → SWE-bench Pro / Claw-Eval</div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5;">GPT-5-Codex / Claude Code / Qwen3-Coder-Next / MiniMax-M2/M3</div>
    </div>
  </div>
</div>

<!-- 公司分组标题 -->
<h2 style="font-size: 20px; font-weight: 700; color: #c4b5fd; margin: 0 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(167,139,250,0.3);">🏢 国内公司</h2>

<!-- Zhipu / GLM -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #3b82f6, #6366f1); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 Zhipu / GLM</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">VLM 多模态 RL → ARC 旗舰 → Long-horizon agentic engineering</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">GLM-4.5V</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-07 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>把 LLM 端 Scalable RL 范式迁移到 VLM 端。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>RLCS</b>（课程学习 RL）+ Ratio EMA 动态采样</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> GUI Agent 数据是 <b>最强 cross-domain transfer 信号</b></div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 9B 小模型超 Qwen2.5-VL-72B，可比 Gemini-2.5-Flash</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">GLM-4.5</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-08 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>用更少参数（355B vs 671B+）实现同等 ARC 能力。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> 355B/32B MoE + <b>减 width 增 depth</b> + QK-Norm</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Expert Model Iteration</b>：三 expert 独立 RL → 自蒸馏统一</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> TAU-Bench 70.1% / AIME 24 91% / SWE-bench 64.2%</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">GLM-TTS</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-12 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>SOTA TTS 普遍需 1M+ 小时数据，难克隆个性化声音。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> 仅 100k 小时数据（CosyVoice3 的 1/10）达开源 SOTA</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>GRPO 多 reward RL</b> + LoRA 声音定制 15% 参数</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>Phoneme-in 机制</b> 解决多音字/罕见字</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">GLM-OCR</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-03 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>MLLM 太大难部署，OCR 任务与 AR 生成范式不匹配。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> 0.9B 超轻量级（CogViT 0.4B + GLM 0.5B）+ <b>MTP</b> 提速 50%</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> PP-DocLayout-V3 + <b>并行区域级识别</b></div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> OmniDocBench v1.5 第一（94.6），反超 Qwen3-VL-235B</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">GLM-4.5 博客</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-07 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>正式发布 ARC 旗舰基座。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> 12 个 ARC benchmark 评测详情</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>BrowseComp 26.4%</b> 超 Claude-4-Opus (18.8%)</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> Test-time scaling accuracy 曲线</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">GLM-5.1 博客</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-04 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>GLM-4.5 长任务有局限，推 agentic engineering 旗舰。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>SWE-Bench Pro SOTA 58.4%</b>（vs GLM-5 54.2%）</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> NL2Repo（repo generation）大幅领先</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> Terminal-Bench 2.0 领先 GLM-5</div>
      </div>
    </div>
  </div>
</div>

<!-- MiniMax -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #f43f5e, #ec4899); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 MiniMax</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">M1 long-context → M2 系列 agent → M3 1M context + MSA</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fda4af;">MiniMax-M1</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-06 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>softmax attention 二次复杂度 + 上下文太小 + RL 成本高。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Lightning Attention</b>：100K tokens FLOPs 仅 DeepSeek R1 25%</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>CISPO</b>（裁 IS 权重而非 token），保留低概率 token 梯度</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 1M context + 80K output，RL 训练成本仅 $0.53M</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fda4af;">MiniMax-M2 Series</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-05 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>Agent 任务需超长上下文 + 训练-推理 gap + 多域能力平衡。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>小激活大智能</b>：229.9B/9.8B 激活</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Forge RL</b> 统一白盒/黑盒 agent 训练</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> M2.7 展现<b>自我进化</b>，MLE Bench Lite ≈ Gemini 3.1 Pro</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fda4af;">MiniMax-M3</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-06 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>长任务上下文成本仍高，coding agent 进入多模态阶段。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>MSA</b>（MiniMax Sparse Attention）：1M context 真正可扩展</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> frontier coding + native multimodality + computer use</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> SWE-Bench Pro 超 GPT-5.5，逼近 Opus 4.7</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fda4af;">MiniMax-M2.5</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-02 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>"以可承受价格提供前沿能力"。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> SOTA：SWE-Bench Verified 80.2% / BrowseComp 76.3%</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 比 M2.1 <b>快 37%</b>，匹配 Claude Opus 4.6 速度</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>$1/小时 跑模型</b> —— "too cheap to meter"</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fda4af;">MiniMax-M2.7</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-03 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>模型与组织的<b>自我进化</b>。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> "Early Echoes of Self-Evolution"：模型参与自身 RL 循环</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> SWE-Pro 56.22%（接近 Opus）+ VIBE-Pro 55.6%</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> GDPval-AA ELO 1495（开源第一）</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fda4af;">MiniMax-M3 博客</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-05 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>frontier coding/1M/native 三位一体开源。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> MSA 架构详解（预筛选 + 精确注意力）</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> SWE-Bench Pro/SVG/OmniDoc/Claw-Eval 全面领先</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> Open-weight 路线图 + 多渠道接入</div>
      </div>
    </div>
  </div>
</div>

<!-- Qwen -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #10b981, #14b8a6); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 Alibaba / Qwen</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">thinking 统一 → Coding agent → 全模态 → 开源迭代</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #6ee7b7;">Qwen3</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-05 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>模型分裂（QwQ-32B 推理 + Qwen2.5-72B 响应）。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>首个统一 thinking/non-thinking 单一模型</b>（0.6B-235B）</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Thinking Budget 机制</b> 动态分配推理 token</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 60% 激活参数超 DeepSeek-R1</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #6ee7b7;">Qwen3-Omni</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-09 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>多模态"模态权衡"（增强一个模态导致其他下降）。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Thinker-Talker</b> 架构：Thinker 推理 + Talker 流式语音</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> AuT 音频编码器（20M 小时）+ RVQ codec + TM-RoPE</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>模态不降智</b>，端到端延迟 234ms</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #6ee7b7;">Qwen3-Coder-Next</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-03 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>tool-call 过拟合 + SWE-bench 训练 git 漏洞作弊。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> 80B/3B MoE + <b>最完整 Agent Training Recipe</b></div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Tool Chat Template Scaling</b>（21 种工具格式）</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>Reward Hacking Blocker</b> 防作弊</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #6ee7b7;">Qwen3.5-Omni</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-04 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>被动感知-响应范式缺 agentic 行为。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Hybrid Attention MoE</b> + 256K context（10+ 小时音频）</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>ARIA</b> 解决双通道生成的跳词/发音问题</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> Plus 版 215 benchmark SOTA，超 Gemini-3.1 Pro</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #6ee7b7;">Qwen3-TTS / ASR</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-01 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>TTS 稳定/可控/自然度/低延迟平衡；ASR 传统方法多语言差。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> TTS <b>双码率 12/25Hz</b> + MTP，首包延迟 97ms</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> ASR <b>首次 LLM 引入 forced alignment</b>，52 种语言</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> Seed-TTS benchmark WER 1.24（SOTA）</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #6ee7b7;">Qwen3-Embedding</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-06 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>Qwen3 dense 基底扩展出 embedding/reranker。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>0.6B/4B/8B</b> 三尺寸</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 多语言/长文本/reasoning 能力继承自 Qwen3</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 覆盖 text/code retrieval、classification、clustering</div>
      </div>
    </div>
  </div>
</div>

<!-- Kimi -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #06b6d4, #0ea5e9); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 Moonshot / Kimi</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">K2 ultra-sparse → Linear 架构创新 → K2.5 多模态+Swarm → K2.6 swarm coding</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #67e8f9;">Kimi K2</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-07 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>token efficiency 成关键 + agentic 数据稀缺难 scale。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>MuonClip</b>（Muon + QK-Clip）15.5T tokens 无 loss spike</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Ultra-sparse MoE</b>：1.04T/32B + sparsity 48</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> agentic pipeline + RLVR + Rubric Reward，LMSYS Arena 开源第一</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #67e8f9;">Kimi Linear</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-10 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>softmax attention 二次复杂度 + KV cache 线性增长。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>KDA</b>：per-channel 细粒度 gating（vs per-head）</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 短/长/RL scaling 全面超 full attention</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 1M context + <b>6× decoding throughput</b></div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #67e8f9;">Kimi K2.5</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-02 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>视觉对齐不足 + sequential agent 限制复杂度。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Joint Opt Text+Vision</b>：early fusion + low vision ratio 反而更优</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Agent Swarm + PARL</b> 动态子 agent 并行</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> BrowseComp +17.8%，<b>3~4.5× 更快</b></div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #67e8f9;">Kimi K2.6</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-04 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>K2 系列迭代，开源原生多模态 agentic。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Long-horizon coding</b> 能力</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> Coding-driven design + proactive execution</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>Swarm-based task orchestration</b></div>
      </div>
    </div>
  </div>
</div>

<!-- ByteDance Seed -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 ByteDance Seed</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">Seed1.8 Real-world Agency → Seed2.0 Agent Foundation Model</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fcd34d;">Seed1.8</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-03 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>现有 LLM/VLM 缺乏多步交互和任务执行能力。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Generalized Real-World Agency</b> 定位</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> Search + Code + GUI 统一接口</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>四档 thinking 模式</b>（no_think/think-low/medium/high）</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #fcd34d;">Seed2.0</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-05 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>预训练阶段就应针对 agentic 场景优化。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>"Agent Foundation Model" 概念正式落地</b></div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 预训练数据含 agent 轨迹和环境反馈</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> Computer Use / SE / Research / Multimodal Agent 四大优势</div>
      </div>
    </div>
  </div>
</div>

<!-- 国外公司 -->
<h2 style="font-size: 20px; font-weight: 700; color: #c4b5fd; margin: 32px 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(167,139,250,0.3);">🌍 国外公司</h2>

<!-- OpenAI -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 OpenAI / GPT</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">GPT-5 unified → Codex 系列 → 5.3/5.4/5.5 reasoning & agents</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2025-08</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>统一 reasoning 到消费级产品。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① <b>Unified system</b>：fast + thinking</div>
        <div>② <b>Real-time router</b> 实时调度</div>
        <div>③ ChatGPT + API 集成</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">gpt-OSS</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2025-08</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>开源社区需要 OpenAI 风格 reasoning。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① 开源 <b>gpt-oss-120b/20b</b></div>
        <div>② Open-weight reasoning</div>
        <div>③ Efficient deployment 定位</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5-Codex</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2025-09</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>通用强但 coding 需专用变种。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① GPT-5 变种专为 Codex 优化</div>
        <div>② <b>RL 训练于真实编码任务</b></div>
        <div>③ Agentic coding 定位</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5.1</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2025-11</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>开发者侧 GPT-5 体验优化。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① <b>Adaptive reasoning</b></div>
        <div>② <b>Prompt caching</b> 强化</div>
        <div>③ Coding-oriented use</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5.1-Codex-Max</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2025-11</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>长任务的安全和稳定性。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① <b>Long-running coding</b> 优化</div>
        <div>② <b>Compaction</b>（轨迹压缩）</div>
        <div>③ Agent sandboxing + safety</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5.2</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2025-12</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>推向 professional / 真实工作流。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① <b>Professional work</b></div>
        <div>② <b>Long-running agents</b></div>
        <div>③ SWE-Bench Pro 评测对齐</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5.3-Codex</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2026-02</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>Codex 向更长任务推进。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① Long-running coding tasks</div>
        <div>② Research 能力</div>
        <div>③ <b>Tool use</b> 增强</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5.4</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2026-03</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>computer use 进入主流。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① <b>Computer use</b> 能力</div>
        <div>② <b>Tool search</b></div>
        <div>③ Knowledge work 强化</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="font-size: 13px; font-weight: 700; color: #6ee7b7;">GPT-5.5</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 1px 6px; border-radius: 4px; font-size: 9px; font-weight: 600;">2026-04</div>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-bottom: 8px;"><b style="color: #cbd5e1;">动机：</b>复杂真实工作流的最强消费级。</div>
      <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
        <div>① <b>Complex real-world work</b></div>
        <div>② Coding + research 强化</div>
        <div>③ Tool use 升级</div>
      </div>
    </div>
  </div>
</div>

<!-- Claude -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #d97706, #ea580c); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 Anthropic / Claude</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">4.5 系列 → 4.6 1M context → 4.7 SE → Mythos Preview</div>
  </div>
  <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <div style="font-size: 14px; font-weight: 700; color: #fdba74;">Claude System Cards 总索引</div>
      <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-2026 · 🌐 剪藏</div>
    </div>
    <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>标准化 safety / capability 文档发布。</div>
    <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Opus 4.7 (2026-04)</b> —— advanced software engineering</div>
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Mythos Preview (2026-04)</b> —— Anthropic preview model</div>
      <div><span style="color: #a78bfa; font-weight: 700;">③</span> Sonnet 4.6 / Opus 4.6 / Opus 4.5 / Haiku 4.5 / Sonnet/Opus 4 完整索引</div>
    </div>
  </div>
  <div style="background: rgba(252,165,165,0.08); border: 1px solid rgba(252,165,165,0.3); border-radius: 8px; padding: 10px 14px; margin-top: 10px; font-size: 12px; color: #fca5a5;">⚠️ 详细分模型笔记缺失，推荐独立补 .md 笔记</div>
</div>

<!-- Gemini -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #3b82f6, #06b6d4); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 Google DeepMind / Gemini</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">2.5 thinking → Computer Use → Gemini 3 → 3.1 Pro + Robotics 1.5</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">Gemini 2.5</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-06 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>Gemini 1.5 长上下文强但 reasoning 有限。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Thinking Budget 可调节</b>（AIME 29.7%→88%）</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 1M context + 3 小时视频 + 原生多模态</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> LiveCodeBench 74.2% / Aider 82.2% / SWE-bench 67.2%</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">Gemini Robotics 1.5</div>
        <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-10 · 📄 论文</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>通用机器人需物理理解 + 跨形态泛化。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Motion Transfer</b>：多本体预训练 + 零样本跨机器人迁移</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>GR-ER 1.5</b>：具身推理 SoTA（空间/指向/进度检测）</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 把 Gemini Thinking 带入物理世界</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">Gemini 3 / 3.1 Pro</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-11 / 2026-02 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>Gemini 进入"new era of intelligence"。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Most intelligent model</b>，bring any idea to life</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 全栈差异化（infra + research + tools + products）</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>Agent-first development</b> 定位 + Advanced multimodal reasoning</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #93c5fd;">Gemini 3 Flash</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-12 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>frontier 智能普及到 Flash 速度和成本。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Frontier intelligence built for speed</b></div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> At a fraction of the cost vs Gemini 3 Pro</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 拉低 frontier 模型使用门槛</div>
      </div>
    </div>
  </div>
</div>

<!-- Meta / Llama -->
<div style="margin-bottom: 32px;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
    <div style="background: linear-gradient(135deg, #1d4ed8, #7c3aed); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">🏢 Meta / Llama</div>
    <div style="font-size: 12px; color: #94a3b8; font-style: italic;">Llama 4 herd (2025-04) —— open-weight native multimodal</div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #a5b4fc;">Llama 4 官方博客</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-04 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>开源社区需要新一代 native multimodal。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>首个 open-weight native multimodal</b> 系列</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Llama 4 Scout</b>（17B 激活/16 experts/<b>10M context</b>）</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> <b>Llama 4 Maverick</b>（128 experts，超 GPT-4o/Gemini 2.0 Flash）</div>
      </div>
    </div>
    <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="font-size: 14px; font-weight: 700; color: #a5b4fc;">Llama Guard 4</div>
        <div style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-04 · 🌐 剪藏</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>开源社区需要多模态 safety 分类器。</div>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>12B 多模态</b> safety classifier</div>
        <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 开源</div>
        <div><span style="color: #a78bfa; font-weight: 700;">③</span> 配合 Llama 4 部署使用</div>
      </div>
    </div>
  </div>
  <div style="background: rgba(252,165,165,0.08); border: 1px solid rgba(252,165,165,0.3); border-radius: 8px; padding: 10px 14px; margin-top: 10px; font-size: 12px; color: #fca5a5;">⚠️ 2601_Llama_4_Herd 目录仅有 poster HTML，缺独立 .md 笔记</div>
</div>

<!-- Agentic RL 主线 -->
<h2 style="font-size: 20px; font-weight: 700; color: #c4b5fd; margin: 32px 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(167,139,250,0.3);">🧠 Agentic RL & Verification 主线</h2>
<div style="font-size: 13px; color: #94a3b8; margin-bottom: 16px; line-height: 1.6;">这条线<b style="color: #cbd5e1;">不绑定单一公司</b>，是 2025-2026 涌现的方法论主线：把"agent 在真实环境中的能力"作为可训练目标。</div>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
  <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <div style="font-size: 14px; font-weight: 700; color: #c4b5fd;">Agentic Reasoning</div>
      <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-02 · 📄 论文</div>
    </div>
    <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>非结构化领域（社会/伦理/经验性）需事实验证。</div>
    <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>三类 agentic tools</b>：Web-Search / Coding / Mind-Map</div>
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> DeepSeek-R1 + agentic = HLE 23.8%</div>
      <div><span style="color: #a78bfa; font-weight: 700;">③</span> 与 OpenAI Deep Research 差仅 2.8%</div>
    </div>
  </div>
  <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <div style="font-size: 14px; font-weight: 700; color: #c4b5fd;">rStar2-Agent</div>
      <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-08 · 📄 论文</div>
    </div>
    <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>Agentic RL 三大挑战：cost / noise / efficiency。</div>
    <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>GRPO-RoC</b>（Resample-on-Correct rollout）</div>
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 64 MI300X GPU + 从 non-reasoning SFT 开始</div>
      <div><span style="color: #a78bfa; font-weight: 700;">③</span> 510 RL steps / 14B 达 AIME24 80.6%，超 DeepSeek-R1</div>
    </div>
  </div>
  <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <div style="font-size: 14px; font-weight: 700; color: #c4b5fd;">MiroThinker v1.0</div>
      <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2025-11 · 📄 论文</div>
    </div>
    <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>现有 scaling 维度（model + context）已接近瓶颈。</div>
    <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Interaction Scaling</b>：第三 scaling 维度</div>
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> 通过 RL 训练更深更频繁的 agent 交互</div>
      <div><span style="color: #a78bfa; font-weight: 700;">③</span> 72B 模型 GAIA 81.9% / HLE 37.7% / BrowseComp 47.1%</div>
    </div>
  </div>
  <div style="background: #1a1d2e; border: 1px solid #2d3148; border-radius: 10px; padding: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <div style="font-size: 14px; font-weight: 700; color: #c4b5fd;">MiroThinker-1.7 & H1</div>
      <div style="background: #312e81; color: #c4b5fd; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600;">2026-03 · 📄 论文</div>
    </div>
    <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;"><b style="color: #cbd5e1;">动机：</b>错误级联 + 答案需连贯证据链。</div>
    <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">①</span> <b>Verification Agent</b>：Local + Global verification</div>
      <div style="margin-bottom: 4px;"><span style="color: #a78bfa; font-weight: 700;">②</span> <b>Agentic Mid-training</b>：structured planning + reasoning + tool</div>
      <div><span style="color: #a78bfa; font-weight: 700;">③</span> 1.7 + mini 版本在 GAIA/HLE/Financial Analysis 展现竞争力</div>
    </div>
  </div>
</div>

<!-- Insight Section -->
<h2 style="font-size: 20px; font-weight: 700; color: #c4b5fd; margin: 36px 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(167,139,250,0.3);">💡 7 大整体 Insight</h2>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
  <div style="background: linear-gradient(135deg, rgba(96,165,250,0.1), rgba(96,165,250,0.03)); border: 1px solid rgba(96,165,250,0.3); border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; color: #60a5fa; font-weight: 700; margin-bottom: 6px;">1️⃣ REASONING</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">从后训练 trick → 预训练目标</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">未来 12 个月内"非 thinking base model"将变成 niche 产品，主流 base 全部默认 thinking-on。</div>
  </div>
  <div style="background: linear-gradient(135deg, rgba(167,139,250,0.1), rgba(167,139,250,0.03)); border: 1px solid rgba(167,139,250,0.3); border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; color: #a78bfa; font-weight: 700; margin-bottom: 6px;">2️⃣ AGENTIC RL</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">PPO → GRPO → CISPO → Swarm/Verify</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">CISPO/GRPO 已成为 RLHF 主流替代；Self-Evolution 会进入 2026 下半年所有 major 玩家路线图。</div>
  </div>
  <div style="background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.03)); border: 1px solid rgba(239,68,68,0.3); border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; color: #f87171; font-weight: 700; margin-bottom: 6px;">3️⃣ ATTENTION</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">"Softmax is dead, long live Sparse/Linear"</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">2026 H2 后 Full attention 在 1M+ 上下文场景视为不可承受。MSA / Linear / Hybrid MoE 决出胜负。</div>
  </div>
  <div style="background: linear-gradient(135deg, rgba(134,239,172,0.1), rgba(134,239,172,0.03)); border: 1px solid rgba(134,239,172,0.3); border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; color: #86efac; font-weight: 700; margin-bottom: 6px;">4️⃣ MULTIMODAL</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">"模态不降智"成核心 KPI</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">"先训纯文本，再补多模态"已过时。Joint multimodal pre-training（K2.5 路径）是 2026 共识。</div>
  </div>
  <div style="background: linear-gradient(135deg, rgba(252,211,77,0.1), rgba(252,211,77,0.03)); border: 1px solid rgba(252,211,77,0.3); border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; color: #fcd34d; font-weight: 700; margin-bottom: 6px;">5️⃣ AGENT FM</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">Agent Foundation Model 概念成型</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">未来 base 选型分裂为"对话型 base"和"agent 型 base"两条线。</div>
  </div>
  <div style="background: linear-gradient(135deg, rgba(244,114,182,0.1), rgba(244,114,182,0.03)); border: 1px solid rgba(244,114,182,0.3); border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; color: #f472b6; font-weight: 700; margin-bottom: 6px;">6️⃣ EVALUATION</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">Pass@1 → Long-horizon Verification</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">未来 12 个月 benchmark 主战场会是 end-to-end agent evaluation。</div>
  </div>
  <div style="background: linear-gradient(135deg, rgba(6,182,212,0.1), rgba(6,182,212,0.03)); border: 1px solid rgba(6,182,212,0.3); border-radius: 10px; padding: 14px 16px; grid-column: span 2;">
    <div style="font-size: 12px; color: #67e8f9; font-weight: 700; margin-bottom: 6px;">7️⃣ 国内外对比</div>
    <div style="font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 4px;">国内在 SWE-bench Pro / Claw-Eval 真实工作流评测上差距显著缩小（M3 超 GPT-5.5/Gemini 3.1 Pro）</div>
    <div style="font-size: 11px; color: #94a3b8; line-height: 1.5;">国外：闭源快开放慢，主打 Thinking + Computer Use + Robotics；国内：论文+开源快，主打 Agent Foundation + Sparse Attention + Native Multimodality。</div>
  </div>
</div>

</div>

</details>

---

## 开放问题

- [ ] **Seed2.0 "Agent Foundation Model" 是否成为新标准范式？** —— 取决于 OpenAI/Anthropic 是否跟进
- [ ] **MSA vs Linear Attention 谁会胜出？** —— Kimi Linear 和 MiniMax MSA 走的是不同路径
- [ ] **Self-Evolution 是否安全？** —— M2.7 的"模型参与自身 RL 实验循环"是亮点也是风险
- [ ] **Computer Use 是不是 base model 标配？** —— M3、Gemini 2.5 CU、Seed2.0 都已支持
- [ ] **国内开源生态能否形成 "Qwen + MiniMax + Kimi" 三足鼎立？** —— 目前是混战，没收敛
- [ ] **Llama 5 何时发布？** —— Meta 在 2026 上半年明显慢于其他公司
- [ ] **国内大模型与 Claude Opus 4.7 / GPT-5.5 的真实差距？** —— 缺乏公平基准对比

---

## 关联主题

- [[Topics/5_gui/GUI MOC|GUI Agent MOC]] —— Computer Use / GUI Agent 是 base model 重要应用方向
- [[Topics/6_multimodal/Multimodal MOC|Multimodal MOC]] —— 全模态基座是多模态方向延伸
- [[Topics/7_rl/Reinforcement Learning MOC|RL MOC]] —— Agentic RL 是训练范式核心
- [[Topics/1_benchmarks/Benchmarks MOC|Benchmarks MOC]] —— 评测基准验证 base model 能力
- [[Topics/11_harness/Agent Harness MOC|Agent Harness MOC]] —— Agent Harness 是 evaluation infra
- [[Topics/9_self_play/Self Play MOC|Self-Play MOC]] —— Self-Evolution 的理论基础
- [[00.work/260602_agentic_insight/discussion_agentic_insight|Agentic 跨主题洞察]] —— 基于 vault 全部 topic 的六大支柱收敛分析

---

## 数据来源统计

| 类别 | 数量 | 时间窗口 |
|------|------|----------|
| 📄 论文笔记 | 27 份 | 2025-02 至 2026-06 |
| 🌐 Web-Clippings | 31 份 | 2025-04 至 2026-05 |
| 🏢 覆盖公司 | 9 家（国内 5 + 国外 4）| — |
| 🎯 核心主线 | 4 条 | Reasoning / Agentic RL / Multimodal / Coding |
