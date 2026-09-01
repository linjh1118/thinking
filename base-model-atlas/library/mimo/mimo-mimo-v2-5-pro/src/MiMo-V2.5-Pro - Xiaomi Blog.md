---
title: "MiMo-V2.5-Pro | Xiaomi"
source: "https://mimo.xiaomi.com/mimo-v2-5-pro/"
author:
published: 2026-04-27
created: 2026-06-11
description:
tags:
  - "clippings"
---
Today, we are releasing and open-sourcing MiMo-V2.5-Pro. It is our most capable model to date, delivering significant improvements over its predecessor, MiMo-V2-Pro, in general agentic capabilities, complex software engineering, and long-horizon tasks. MiMo-V2.5-Pro is a 1.02T-parameter Mixture-of-Experts model with 42B active parameters, built on a hybrid-attention architecture with a 1M-token context window.

MiMo-V2.5-Pro MiMo-V2.5 MiMo-V2-Pro Claude Opus 4.6 Gemini 3.1 Pro GPT-5.4

Coding Agent

57.2

MiMo-V2.5-Pro: 57.2

56.1

MiMo-V2.5: 56.1

55.0

MiMo-V2-Pro: 55.0

57.3

Claude Opus 4.6: 57.3

54.2

Gemini 3.1 Pro: 54.2

57.7

GPT-5.4: 57.7

SWE-Bench Pro

73.7

MiMo-V2.5-Pro: 73.7

71.8

MiMo-V2.5: 71.8

71.5

MiMo-V2-Pro: 71.5

77.1

Claude Opus 4.6: 77.1

67.8

Gemini 3.1 Pro: 67.8

MiMo Coding Bench

68.4

MiMo-V2.5-Pro: 68.4

65.8

MiMo-V2.5: 65.8

57.1

MiMo-V2-Pro: 57.1

65.4

Claude Opus 4.6: 65.4

68.5

Gemini 3.1 Pro: 68.5

75.1

GPT-5.4: 75.1

Terminal-Bench 2.0

#3.4

MiMo-V2.5-Pro: #3.4

#5.0

MiMo-V2-Pro: #5.0

#2.0

Claude Opus 4.6: #2.0

#3.9

Gemini 3.1 Pro: #3.9

#1.9

GPT-5.4: #1.9

FrontierSWE (Impl., rank)

General Agent

Reasoning

1581

MiMo-V2.5-Pro: 1581

1426

MiMo-V2-Pro: 1426

1606

Claude Opus 4.6: 1606

1317

Gemini 3.1 Pro: 1317

1674

GPT-5.4: 1674

GDPVal-AA

72.9

MiMo-V2.5-Pro: 72.9

69.5

MiMo-V2.5: 69.5

64.5

MiMo-V2-Pro: 64.5

72.4

Claude Opus 4.6: 72.4

67.1

Gemini 3.1 Pro: 67.1

72.9

GPT-5.4: 72.9

τ3-bench

63.8

MiMo-V2.5-Pro: 63.8

62.3

MiMo-V2.5: 62.3

57.8

MiMo-V2-Pro: 57.8

70.4

Claude Opus 4.6: 70.4

57.8

Gemini 3.1 Pro: 57.8

60.3

GPT-5.4: 60.3

Claw-Eval (pass^3)

no tools with tools

48.0

34.0

MiMo-V2.5-Pro: 34.0 / 48.0 w/ tools

40.0

28.0

MiMo-V2-Pro: 28.0 / 40.0 w/ tools

53.0

40.0

Claude Opus 4.6: 40.0 / 53.0 w/ tools

51.4

44.4

Gemini 3.1 Pro: 44.4 / 51.4 w/ tools

58.7

42.7

GPT-5.4: 42.7 / 58.7 w/ tools

Humanity's Last Exam

In internal testing, V2.5-Pro demonstrated a new level of intelligence that, in turn, pushed our researchers to rethink how they work with it. When paired with a proper harness, V2.5-Pro can sustain complex, long-horizon tasks spanning more than a thousand tool calls. We also see substantial improvements in instruction following within agentic scenarios. It reliably adheres to subtle requirements embedded in context and maintains strong coherence across ultra-long contexts.

MiMo-V2.5-Pro is now fully rolled out across our API Platform, AI Studio, and other surfaces, with no change in pricing. Simply replace the model tag with `mimo-v2.5-pro` to get started.

## Built to Solve Harder

MiMo-V2.5-Pro is built for harder goals. We've given it tasks that would take human experts days or weeks, and let it run autonomously. Here's what it delivers:

### SysY Compiler in Rust

Sourced from Peking University's [*Compiler Principles*](https://github.com/pku-minic) course project, this task asks the model to implement a complete SysY compiler in Rust from scratch: lexer, parser, AST, Koopa IR codegen, RISC-V assembly backend, and performance optimization. The reference project typically takes a PKU CS major student several weeks. MiMo-V2.5-Pro finished in 4.3 hours across 672 tool calls, scoring a perfect 233/233 against the course's hidden test suite.

Building a complete SysY compiler in Rust, from scratch to 100%

**mimo-v2.5-pro** 672 tool calls 4.3 hours 233 / 233 passed

<svg viewBox="0 0 780 400" preserveAspectRatio="xMidYMid meet" role="img" aria-label="SysY compiler pass rate over 4.3 hours"><rect x="44" y="62" width="46.41333333333333" height="284" fill="#F0E5D3" opacity="0.55"></rect><rect x="90.41333333333333" y="62" width="232.06666666666663" height="284" fill="#F1E3CB" opacity="0.55"></rect><rect x="322.47999999999996" y="62" width="273.75999999999993" height="284" fill="#F5DDBE" opacity="0.55"></rect><rect x="596.2399999999999" y="62" width="155.7600000000001" height="284" fill="#DEEBD8" opacity="0.55"></rect><line x1="90.41333333333333" x2="90.41333333333333" y1="62" y2="346" stroke="currentColor" stroke-opacity="0.2"></line><line x1="322.47999999999996" x2="322.47999999999996" y1="62" y2="346" stroke="currentColor" stroke-opacity="0.2"></line><line x1="596.2399999999999" x2="596.2399999999999" y1="62" y2="346" stroke="currentColor" stroke-opacity="0.2"></line><line x1="44" x2="752" y1="346" y2="346" stroke="currentColor" stroke-opacity="0.2"></line><text x="36" y="349.5" text-anchor="end" fill="currentColor">0%</text> <line x1="44" x2="752" y1="289.20000000000005" y2="289.20000000000005" stroke="currentColor" stroke-opacity="0.2"></line><text x="36" y="292.70000000000005" text-anchor="end" fill="currentColor">20%</text> <line x1="44" x2="752" y1="232.4" y2="232.4" stroke="currentColor" stroke-opacity="0.2"></line><text x="36" y="235.9" text-anchor="end" fill="currentColor">40%</text> <line x1="44" x2="752" y1="175.60000000000002" y2="175.60000000000002" stroke="currentColor" stroke-opacity="0.2"></line><text x="36" y="179.10000000000002" text-anchor="end" fill="currentColor">60%</text> <line x1="44" x2="752" y1="118.79999999999998" y2="118.79999999999998" stroke="currentColor" stroke-opacity="0.2"></line><text x="36" y="122.29999999999998" text-anchor="end" fill="currentColor">80%</text> <line x1="44" x2="752" y1="62" y2="62" stroke="currentColor" stroke-opacity="0.2"></line><text x="36" y="65.5" text-anchor="end" fill="currentColor">100%</text> <line x1="44" x2="752" y1="62" y2="62" stroke="currentColor" stroke-opacity="0.2"></line><path d="M 44.00,346.00 L 48.72,346.00 L 51.87,346.00 L 56.59,346.00 L 61.31,346.00 L 66.03,346.00 L 91.20,257.02 L 105.36,257.02 L 121.09,257.02 L 128.96,250.93 L 133.68,250.93 L 146.27,247.27 L 150.99,247.27 L 158.85,242.39 L 163.57,242.39 L 169.87,242.39 L 174.59,242.39 L 182.45,233.86 L 190.32,228.99 L 209.20,228.99 L 215.49,228.99 L 229.65,228.99 L 275.28,219.24 L 314.61,214.36 L 322.48,211.92 L 328.77,211.92 L 336.64,211.92 L 357.09,211.92 L 363.39,211.92 L 369.68,211.92 L 375.97,211.92 L 386.99,211.92 L 391.71,211.92 L 398.00,211.92 L 405.87,211.92 L 420.03,211.92 L 424.75,211.92 L 435.76,211.92 L 459.36,211.92 L 503.41,211.92 L 517.57,211.92 L 527.01,211.92 L 545.89,211.92 L 553.76,211.92 L 560.05,211.92 L 596.24,211.92 L 600.96,211.92 L 610.40,211.92 L 615.12,211.92 L 654.45,211.92 L 717.39,211.92 L 717.39,346.00 L 654.45,346.00 L 615.12,346.00 L 610.40,346.00 L 600.96,346.00 L 596.24,346.00 L 560.05,346.00 L 553.76,346.00 L 545.89,346.00 L 527.01,346.00 L 517.57,346.00 L 503.41,346.00 L 459.36,346.00 L 435.76,346.00 L 424.75,346.00 L 420.03,346.00 L 405.87,346.00 L 398.00,346.00 L 391.71,346.00 L 386.99,346.00 L 375.97,346.00 L 369.68,346.00 L 363.39,346.00 L 357.09,346.00 L 336.64,346.00 L 328.77,346.00 L 322.48,346.00 L 314.61,346.00 L 275.28,346.00 L 229.65,346.00 L 215.49,346.00 L 209.20,346.00 L 190.32,346.00 L 182.45,346.00 L 174.59,346.00 L 169.87,346.00 L 163.57,346.00 L 158.85,346.00 L 150.99,346.00 L 146.27,346.00 L 133.68,346.00 L 128.96,346.00 L 121.09,346.00 L 105.36,346.00 L 91.20,346.00 L 66.03,346.00 L 61.31,346.00 L 56.59,346.00 L 51.87,346.00 L 48.72,346.00 L 44.00,346.00 Z" fill="#D9B16B" opacity="0.55"></path><path d="M 44.00,346.00 L 48.72,346.00 L 51.87,346.00 L 56.59,346.00 L 61.31,346.00 L 66.03,346.00 L 91.20,179.01 L 105.36,179.01 L 121.09,179.01 L 128.96,166.82 L 133.68,166.82 L 146.27,159.51 L 150.99,159.51 L 158.85,149.76 L 163.57,149.76 L 169.87,149.76 L 174.59,149.76 L 182.45,140.01 L 190.32,135.13 L 209.20,135.13 L 215.49,135.13 L 229.65,135.13 L 275.28,125.38 L 314.61,120.51 L 322.48,118.07 L 328.77,118.07 L 336.64,118.07 L 357.09,108.32 L 363.39,108.32 L 369.68,108.32 L 375.97,108.32 L 386.99,108.32 L 391.71,108.32 L 398.00,108.32 L 405.87,104.66 L 420.03,103.44 L 424.75,103.44 L 435.76,105.88 L 459.36,101.00 L 503.41,102.22 L 517.57,102.22 L 527.01,90.03 L 545.89,90.03 L 553.76,88.82 L 560.05,88.82 L 596.24,86.38 L 600.96,86.38 L 610.40,86.38 L 615.12,86.38 L 654.45,86.38 L 717.39,86.38 L 717.39,211.92 L 654.45,211.92 L 615.12,211.92 L 610.40,211.92 L 600.96,211.92 L 596.24,211.92 L 560.05,211.92 L 553.76,211.92 L 545.89,211.92 L 527.01,211.92 L 517.57,211.92 L 503.41,211.92 L 459.36,211.92 L 435.76,211.92 L 424.75,211.92 L 420.03,211.92 L 405.87,211.92 L 398.00,211.92 L 391.71,211.92 L 386.99,211.92 L 375.97,211.92 L 369.68,211.92 L 363.39,211.92 L 357.09,211.92 L 336.64,211.92 L 328.77,211.92 L 322.48,211.92 L 314.61,214.36 L 275.28,219.24 L 229.65,228.99 L 215.49,228.99 L 209.20,228.99 L 190.32,228.99 L 182.45,233.86 L 174.59,242.39 L 169.87,242.39 L 163.57,242.39 L 158.85,242.39 L 150.99,247.27 L 146.27,247.27 L 133.68,250.93 L 128.96,250.93 L 121.09,257.02 L 105.36,257.02 L 91.20,257.02 L 66.03,346.00 L 61.31,346.00 L 56.59,346.00 L 51.87,346.00 L 48.72,346.00 L 44.00,346.00 Z" fill="#FF9B5B" opacity="0.5"></path><path d="M 44.00,346.00 L 48.72,346.00 L 51.87,346.00 L 56.59,346.00 L 61.31,346.00 L 66.03,346.00 L 91.20,179.01 L 105.36,179.01 L 121.09,179.01 L 128.96,166.82 L 133.68,166.82 L 146.27,159.51 L 150.99,159.51 L 158.85,149.76 L 163.57,149.76 L 169.87,149.76 L 174.59,149.76 L 182.45,140.01 L 190.32,135.13 L 209.20,135.13 L 215.49,135.13 L 229.65,135.13 L 275.28,125.38 L 314.61,120.51 L 322.48,118.07 L 328.77,118.07 L 336.64,118.07 L 357.09,108.32 L 363.39,108.32 L 369.68,108.32 L 375.97,108.32 L 386.99,108.32 L 391.71,108.32 L 398.00,108.32 L 405.87,104.66 L 420.03,103.44 L 424.75,103.44 L 435.76,105.88 L 459.36,101.00 L 503.41,102.22 L 517.57,102.22 L 527.01,90.03 L 545.89,90.03 L 553.76,88.82 L 560.05,88.82 L 596.24,86.38 L 600.96,86.38 L 610.40,86.38 L 615.12,86.38 L 654.45,62.00 L 717.39,62.00 L 717.39,86.38 L 654.45,86.38 L 615.12,86.38 L 610.40,86.38 L 600.96,86.38 L 596.24,86.38 L 560.05,88.82 L 553.76,88.82 L 545.89,90.03 L 527.01,90.03 L 517.57,102.22 L 503.41,102.22 L 459.36,101.00 L 435.76,105.88 L 424.75,103.44 L 420.03,103.44 L 405.87,104.66 L 398.00,108.32 L 391.71,108.32 L 386.99,108.32 L 375.97,108.32 L 369.68,108.32 L 363.39,108.32 L 357.09,108.32 L 336.64,118.07 L 328.77,118.07 L 322.48,118.07 L 314.61,120.51 L 275.28,125.38 L 229.65,135.13 L 215.49,135.13 L 209.20,135.13 L 190.32,135.13 L 182.45,140.01 L 174.59,149.76 L 169.87,149.76 L 163.57,149.76 L 158.85,149.76 L 150.99,159.51 L 146.27,159.51 L 133.68,166.82 L 128.96,166.82 L 121.09,179.01 L 105.36,179.01 L 91.20,179.01 L 66.03,346.00 L 61.31,346.00 L 56.59,346.00 L 51.87,346.00 L 48.72,346.00 L 44.00,346.00 Z" fill="#8FBF9E" opacity="0.7"></path><path d="M 44.00,346.00 L 48.72,346.00 L 51.87,346.00 L 56.59,346.00 L 61.31,346.00 L 66.03,346.00 L 91.20,179.01 L 105.36,179.01 L 121.09,179.01 L 128.96,166.82 L 133.68,166.82 L 146.27,159.51 L 150.99,159.51 L 158.85,149.76 L 163.57,149.76 L 169.87,149.76 L 174.59,149.76 L 182.45,140.01 L 190.32,135.13 L 209.20,135.13 L 215.49,135.13 L 229.65,135.13 L 275.28,125.38 L 314.61,120.51 L 322.48,118.07 L 328.77,118.07 L 336.64,118.07 L 357.09,108.32 L 363.39,108.32 L 369.68,108.32 L 375.97,108.32 L 386.99,108.32 L 391.71,108.32 L 398.00,108.32 L 405.87,104.66 L 420.03,103.44 L 424.75,103.44 L 435.76,105.88 L 459.36,101.00 L 503.41,102.22 L 517.57,102.22 L 527.01,90.03 L 545.89,90.03 L 553.76,88.82 L 560.05,88.82 L 596.24,86.38 L 600.96,86.38 L 610.40,86.38 L 615.12,86.38 L 654.45,62.00 L 717.39,62.00" fill="none" stroke="currentColor"></path><path d="M 44.00,346.00 L 48.72,346.00 L 51.87,346.00 L 56.59,346.00 L 61.31,346.00 L 66.03,346.00 L 91.20,179.01 L 105.36,179.01 L 121.09,179.01 L 128.96,166.82 L 133.68,166.82 L 146.27,159.51 L 150.99,159.51 L 158.85,149.76 L 163.57,149.76 L 169.87,149.76 L 174.59,149.76 L 182.45,140.01 L 190.32,135.13 L 209.20,135.13 L 215.49,135.13 L 229.65,135.13 L 275.28,125.38 L 314.61,120.51 L 322.48,118.07 L 328.77,118.07 L 336.64,118.07 L 357.09,108.32 L 363.39,108.32 L 369.68,108.32 L 375.97,108.32 L 386.99,108.32 L 391.71,108.32 L 398.00,108.32 L 405.87,104.66 L 420.03,103.44 L 424.75,103.44 L 435.76,105.88 L 459.36,101.00 L 503.41,102.22 L 517.57,102.22 L 527.01,90.03 L 545.89,90.03 L 553.76,88.82 L 560.05,88.82 L 596.24,86.38 L 600.96,86.38 L 610.40,86.38 L 615.12,86.38 L 654.45,62.00 L 717.39,62.00" fill="none" stroke="currentColor"></path><circle cx="44" cy="346" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="48.72" cy="346" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="51.86666666666667" cy="346" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="56.586666666666666" cy="346" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="61.30666666666667" cy="346" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="66.02666666666667" cy="346" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="91.2" cy="179.0128755364807" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="105.36" cy="179.0128755364807" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="121.09333333333333" cy="179.0128755364807" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="128.96" cy="166.82403433476395" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="133.68" cy="166.82403433476395" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="146.26666666666668" cy="159.51072961373396" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="150.98666666666668" cy="159.51072961373396" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="158.85333333333332" cy="149.75965665236052" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="163.57333333333332" cy="149.75965665236052" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="169.86666666666667" cy="149.75965665236052" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="174.58666666666667" cy="149.75965665236052" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="182.45333333333335" cy="140.0085836909871" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="190.32" cy="135.13304721030045" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="209.2" cy="135.13304721030045" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="215.49333333333334" cy="135.13304721030045" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="229.6533333333333" cy="135.13304721030045" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="275.28" cy="125.38197424892704" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="314.61333333333334" cy="120.50643776824036" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="322.47999999999996" cy="118.06866952789701" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="328.77333333333337" cy="118.06866952789701" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="336.64" cy="118.06866952789701" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="357.09333333333336" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="363.38666666666666" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="369.67999999999995" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="375.9733333333333" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="386.9866666666667" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="391.70666666666665" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="398" cy="108.3175965665236" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="405.8666666666666" cy="104.6609442060086" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="420.02666666666664" cy="103.44206008583689" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="424.74666666666667" cy="103.44206008583689" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="435.76" cy="105.87982832618026" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="459.36" cy="101.00429184549353" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="503.4133333333333" cy="102.22317596566523" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="517.5733333333333" cy="102.22317596566523" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="527.0133333333333" cy="90.0343347639485" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="545.8933333333333" cy="90.0343347639485" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="553.76" cy="88.81545064377683" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="560.0533333333333" cy="88.81545064377683" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="596.2399999999999" cy="86.37768240343347" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="600.9599999999999" cy="86.37768240343347" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="610.4" cy="86.37768240343347" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="615.12" cy="86.37768240343347" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="654.4533333333334" cy="62" r="2.2" fill="none" stroke="currentColor"></circle><circle cx="717.3866666666667" cy="62" r="2.2" fill="none" stroke="currentColor"></circle><text x="67.20666666666666" y="34" text-anchor="middle" fill="#9C7A4A">PHASE 1</text> <text x="67.20666666666666" y="47" text-anchor="middle" fill="#9C7A4A" opacity="0.85">Scaffolding &amp; AST</text> <text x="206.44666666666666" y="34" text-anchor="middle" fill="#A8754A">PHASE 2</text> <text x="206.44666666666666" y="47" text-anchor="middle" fill="#A8754A" opacity="0.85">Koopa IR Codegen</text> <text x="459.3599999999999" y="34" text-anchor="middle" fill="#C2591C">PHASE 3</text> <text x="459.3599999999999" y="47" text-anchor="middle" fill="#C2591C" opacity="0.85">RISC-V Backend</text> <text x="674.1199999999999" y="34" text-anchor="middle" fill="#5A8A5F">PHASE 4</text> <text x="674.1199999999999" y="47" text-anchor="middle" fill="#5A8A5F" opacity="0.85">Perf Optimization</text> <rect x="73.53333333333336" y="237.27999999999997" width="114" height="30" rx="5" ry="5" fill="#ffffff" stroke="#c9c0b5"></rect><text x="130.53333333333336" y="249.27999999999997" text-anchor="middle" fill="#6E4E22" font-style="normal">First compile succeeds</text> <text x="130.53333333333336" y="261.28" text-anchor="middle" fill="#6E4E22" font-style="normal">137 / 233 = 59%</text> <path d="M 130.53333333333336 237.27999999999997 L 91.2 179.0128755364807" fill="none" stroke="currentColor"></path><circle cx="91.2" cy="179.0128755364807" r="2.5" fill="#6E4E22"></circle><rect x="207.26666666666665" y="154.92000000000002" width="114" height="30" rx="5" ry="5" fill="#ffffff" stroke="#c9c0b5"></rect><text x="264.26666666666665" y="166.92000000000002" text-anchor="middle" fill="#A8754A" font-style="normal">Koopa IR 110 / 110</text> <text x="264.26666666666665" y="178.92000000000002" text-anchor="middle" fill="#A8754A" font-style="normal">All IR levels passed</text> <path d="M 321.26666666666665 169.92000000000002 L 322.47999999999996 118.06866952789701" fill="none" stroke="currentColor"></path><circle cx="322.47999999999996" cy="118.06866952789701" r="2.5" fill="#A8754A"></circle><rect x="447" y="109.47999999999999" width="138" height="30" rx="5" ry="5" fill="#ffffff" stroke="#c9c0b5"></rect><text x="516" y="121.47999999999999" text-anchor="middle" fill="#B8501C" font-style="normal">All functional tests pass</text> <text x="516" y="133.48" text-anchor="middle" fill="#B8501C" font-style="normal">213 / 213 = 91%</text> <path d="M 585 124.47999999999999 L 596.2399999999999 86.37768240343347" fill="none" stroke="currentColor"></path><circle cx="596.2399999999999" cy="86.37768240343347" r="2.5" fill="#B8501C"></circle><rect x="427.53333333333336" y="191.84" width="114" height="30" rx="5" ry="5" fill="#ffffff" stroke="#c9c0b5"></rect><text x="484.53333333333336" y="203.84" text-anchor="middle" fill="#C62828" font-style="italic">Regression &amp; recovery</text> <text x="484.53333333333336" y="215.84" text-anchor="middle" fill="#C62828" font-style="italic">refactoring lv9/riscv</text> <path d="M 484.53333333333336 191.84 L 435.76 105.87982832618026" fill="none" stroke="currentColor"></path><circle cx="435.76" cy="105.87982832618026" r="2.5" fill="#C62828"></circle><rect x="597.4533333333334" y="92.44000000000001" width="114" height="30" rx="5" ry="5" fill="#D5E9D3" stroke="#2E7D32"></rect><text x="654.4533333333334" y="104.44000000000001" text-anchor="middle" fill="#2E7D32" font-style="normal">PERFECT SCORE</text> <text x="654.4533333333334" y="116.44000000000001" text-anchor="middle" fill="#2E7D32" font-style="normal">233 / 233 = 100%</text> <path d="M 654.4533333333334 92.44000000000001 L 654.4533333333334 62" fill="none" stroke="currentColor"></path><circle cx="654.4533333333334" cy="62" r="2.5" fill="#2E7D32"></circle><text x="44" y="362" text-anchor="middle" fill="currentColor">0.0h</text> <text x="122.66666666666666" y="362" text-anchor="middle" fill="currentColor">0.5h</text> <text x="201.33333333333331" y="362" text-anchor="middle" fill="currentColor">1.0h</text> <text x="280" y="362" text-anchor="middle" fill="currentColor">1.5h</text> <text x="358.66666666666663" y="362" text-anchor="middle" fill="currentColor">2.0h</text> <text x="437.33333333333337" y="362" text-anchor="middle" fill="currentColor">2.5h</text> <text x="516" y="362" text-anchor="middle" fill="currentColor">3.0h</text> <text x="594.6666666666666" y="362" text-anchor="middle" fill="currentColor">3.5h</text> <text x="673.3333333333333" y="362" text-anchor="middle" fill="currentColor">4.0h</text> <text x="752" y="362" text-anchor="middle" fill="currentColor">4.5h</text> <text x="398" y="390" text-anchor="middle" fill="currentColor">Elapsed Time</text> <text x="12" y="204" text-anchor="middle" transform="rotate(-90 12 204)" fill="currentColor">Pass Rate</text><line x1="0" x2="0" y1="62" y2="346" stroke="currentColor" stroke-opacity="0.2"></line><circle cx="0" cy="0" r="4" fill="none" stroke="currentColor"></circle><rect x="44" y="62" width="708" height="284" fill="transparent" style="cursor: crosshair;"></rect></svg>

Koopa IR (110) RISC-V Backend (103) Perf Optimization (20) Total Pass Rate

Rather than thrashing through trial and error, the model built the compiler layer by layer: scaffold the full pipeline first, perfect Koopa IR (110/110), then the RISC-V backend (103/103), then performance (20/20). The first compile alone passed 137/233 tests, a 59% cold start that suggests the architecture was designed correctly before a single test was run. At turn 512 a refactoring pass regressed lv9/riscv by two tests; the model diagnosed the failures, recovered, and pushed on. Long-horizon work rewards this kind of structured, self-correcting discipline.

### A Full-Featured Video Editor

With just a few simple prompts, MiMo-V2.5-Pro delivered a working desktop app: multi-track timeline, clip trimming, cross-fades, audio mixing, and export pipeline. The final build is **8,192 lines of code**, produced over **1,868 tool calls** across **11.5 hours** of autonomous work.

<iframe src="https://player.bilibili.com/player.html?bvid=BV1nuo4BnEda&amp;autoplay=0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

A demo of the video editor MiMo-V2.5-Pro wrote end-to-end, including AI voice-over driven by MiMo-V2-TTS.

### Analog EDA: FVF-LDO Design & Optimization

A graduate-level analog-circuit EDA task: design and optimize a complete FVF-LDO (Flipped-Voltage-Follower low-dropout regulator) from scratch in the TSMC 180nm CMOS process. The model has to size the power transistor, tune the compensation network, and pick bias voltages so that six metrics land within spec simultaneously — phase margin, line regulation, load regulation, quiescent current, PSRR, and transient response. A trained analog designer typically spends several days on a project of this scope.

We wired MiMo-V2.5-Pro into an ngspice simulation loop with Claude Code as the harness. In about an hour of closed-loop iteration — calling the simulator, reading waveforms, tweaking parameters — the model produced a design where every target metric is met, and the four shown below are improved by an order of magnitude over its own initial attempt.

<svg viewBox="0 0 820 320" preserveAspectRatio="xMidYMid meet" role="img" aria-label="FVF-LDO multi-metric optimization results"><text x="150" y="50.5" text-anchor="end" fill="currentColor">Line Regulation</text> <rect x="168" y="26.5" width="535.44" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="693.44" y="41.5" text-anchor="end" fill="currentColor">0.65 mV/V</text> <rect x="168" y="52.5" width="24.712615384615386" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="200.7126153846154" y="67.5" fill="currentColor">0.03 mV/V</text> <text x="785" y="56.5" text-anchor="middle" fill="currentColor">22×</text> <text x="150" y="123.5" text-anchor="end" fill="currentColor">Load Regulation</text> <rect x="168" y="99.5" width="535.44" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="693.44" y="114.5" text-anchor="end" fill="currentColor">0.51 mV/mA</text> <rect x="168" y="125.5" width="31.496470588235297" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="207.4964705882353" y="140.5" fill="currentColor">0.03 mV/mA</text> <text x="785" y="129.5" text-anchor="middle" fill="currentColor">17×</text> <text x="150" y="196.5" text-anchor="end" fill="currentColor">Quiescent Current</text> <rect x="168" y="172.5" width="535.44" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="693.44" y="187.5" text-anchor="end" fill="currentColor">536 µA</text> <rect x="168" y="198.5" width="58.93835820895523" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="234.93835820895524" y="213.5" fill="currentColor">59 µA</text> <text x="785" y="202.5" text-anchor="middle" fill="currentColor">9×</text> <text x="150" y="269.5" text-anchor="end" fill="currentColor">Undershoot</text> <rect x="168" y="245.5" width="535.44" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="693.44" y="260.5" text-anchor="end" fill="currentColor">20.4 mV</text> <rect x="168" y="271.5" width="39.89552941176472" height="22" rx="3" fill="none" stroke="currentColor"></rect><text x="215.89552941176473" y="286.5" fill="currentColor">1.52 mV</text> <text x="785" y="275.5" text-anchor="middle" fill="currentColor">13×</text></svg>

Throughout these experiments, V2.5-Pro exhibits a remarkable "harness awareness": it makes full use of the affordances of its harness environment, manages its memory, and shapes how its own context is populated toward the final objective.

## Frontier Coding Intelligence

We further advanced the model's coding intelligence by scaling post-training compute.

MiMo Coding Bench is our in-house evaluation suite for assessing models' ability to handle diverse coding tasks within agentic frameworks such as Claude Code. It covers repo understanding, project building, code review, structured artifact generation, planning, SWE, and more. MiMo-V2.5-Pro further enhances the user experience in real-world coding scenarios, better handling a wide variety of development needs.

MiMo Coding Bench — closing the gap to Opus 4.6

<svg viewBox="0 0 820 180" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MiMo Coding Bench overall score comparison"><line x1="40" x2="40" y1="105" y2="109" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="123" text-anchor="middle" fill="currentColor">60</text> <line x1="225" x2="225" y1="105" y2="109" stroke="currentColor" stroke-opacity="0.2"></line><text x="225" y="123" text-anchor="middle" fill="currentColor">65</text> <line x1="410" x2="410" y1="105" y2="109" stroke="currentColor" stroke-opacity="0.2"></line><text x="410" y="123" text-anchor="middle" fill="currentColor">70</text> <line x1="595" x2="595" y1="105" y2="109" stroke="currentColor" stroke-opacity="0.2"></line><text x="595" y="123" text-anchor="middle" fill="currentColor">75</text> <line x1="780" x2="780" y1="105" y2="109" stroke="currentColor" stroke-opacity="0.2"></line><text x="780" y="123" text-anchor="middle" fill="currentColor">80</text> <line x1="40" x2="780" y1="105" y2="105" stroke="currentColor" stroke-opacity="0.2"></line><rect x="40" y="73" width="425.49999999999994" height="28" rx="4" ry="4" fill="none" stroke="currentColor"></rect><rect x="465.49999999999994" y="73" width="81.40000000000015" height="28" rx="4" ry="4" fill="none" stroke="currentColor"></rect><line x1="465.49999999999994" x2="465.49999999999994" y1="71" y2="103" stroke="currentColor" stroke-opacity="0.2"></line><text x="465.49999999999994" y="145" text-anchor="middle" fill="#909090">MiMo-V2-Pro</text> <text x="465.49999999999994" y="159" text-anchor="middle" fill="#909090">71.5</text> <text x="546.9000000000001" y="53" text-anchor="middle" fill="currentColor">MiMo-V2.5-Pro</text> <text x="546.9000000000001" y="67" text-anchor="middle" fill="currentColor">73.7</text> <line x1="328.5999999999999" x2="328.5999999999999" y1="69" y2="105" stroke="currentColor" stroke-opacity="0.2"></line><circle cx="328.5999999999999" cy="87" r="3.5" fill="none" stroke="currentColor"></circle><text x="328.5999999999999" y="145" text-anchor="middle" fill="currentColor">Gemini 3.1 Pro</text> <text x="328.5999999999999" y="159" text-anchor="middle" fill="currentColor">67.8</text> <line x1="672.6999999999998" x2="672.6999999999998" y1="69" y2="105" stroke="currentColor" stroke-opacity="0.2"></line><circle cx="672.6999999999998" cy="87" r="3.5" fill="none" stroke="currentColor"></circle><text x="672.6999999999998" y="53" text-anchor="middle" fill="currentColor">Claude Opus 4.6</text> <text x="672.6999999999998" y="67" text-anchor="middle" fill="currentColor">77.1</text></svg>

We welcome developers worldwide to integrate MiMo-V2.5 series into scaffolds such as Claude Code, OpenCode, and Kilo — accessing top-tier intelligence at a lower cost.

## Token Efficiency

Higher intelligence isn't just about higher scores — it's about getting there with fewer tokens. MiMo-V2.5-Pro reaches frontier-tier capability while spending dramatically less on tokens per trajectory. On ClawEval, V2.5-Pro lands at 64% Pass^3 using only ~70K tokens per trajectory — roughly **40–60% fewer tokens** than Claude Opus 4.6, Gemini 3.1 Pro, and GPT-5.4 at comparable capability levels. The upper-left corner of the chart is where you want to be: higher score for lower cost.

Pass^3 vs. Token Efficiency on ClawEval

Upper-left is better · x = (total input + output tokens) / #trajectories

<svg viewBox="0 0 820 480" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Pass^3 vs token efficiency scatter plot"><defs><radialGradient id="te-grad-wseae" cx="0" cy="0" r="1.1" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="#22c55e" stop-opacity="0.22"></stop><stop offset="0.7" stop-color="#22c55e" stop-opacity="0"></stop></radialGradient></defs><rect x="68" y="36" width="720" height="384" fill="url(#te-grad-wseae)"></rect><text x="78" y="56">↖ better</text> <line x1="68" x2="788" y1="420" y2="420"></line><text x="58" y="424" text-anchor="end">0%</text> <line x1="68" x2="788" y1="368.8" y2="368.8"></line><text x="58" y="372.8" text-anchor="end">10%</text> <line x1="68" x2="788" y1="317.6" y2="317.6"></line><text x="58" y="321.6" text-anchor="end">20%</text> <line x1="68" x2="788" y1="266.4" y2="266.4"></line><text x="58" y="270.4" text-anchor="end">30%</text> <line x1="68" x2="788" y1="215.2" y2="215.2"></line><text x="58" y="219.2" text-anchor="end">40%</text> <line x1="68" x2="788" y1="164" y2="164"></line><text x="58" y="168" text-anchor="end">50%</text> <line x1="68" x2="788" y1="112.79999999999998" y2="112.79999999999998"></line><text x="58" y="116.79999999999998" text-anchor="end">60%</text> <line x1="68" x2="788" y1="61.599999999999994" y2="61.599999999999994"></line><text x="58" y="65.6" text-anchor="end">70%</text> <line x1="68.91968284274012" x2="68.91968284274012" y1="36" y2="420"></line><text x="68.91968284274012" y="438" text-anchor="middle">50K</text> <line x1="242.31388396267397" x2="242.31388396267397" y1="36" y2="420"></line><text x="242.31388396267397" y="438" text-anchor="middle">100K</text> <line x1="415.70808508260785" x2="415.70808508260785" y1="36" y2="420"></line><text x="415.70808508260785" y="438" text-anchor="middle">150K</text> <line x1="589.1022862025418" x2="589.1022862025418" y1="36" y2="420"></line><text x="589.1022862025418" y="438" text-anchor="middle">200K</text> <line x1="762.4964873224757" x2="762.4964873224757" y1="36" y2="420"></line><text x="762.4964873224757" y="438" text-anchor="middle">250K</text> <line x1="68" y1="420" x2="788" y2="420"></line><line x1="68" y1="36" x2="68" y2="420"></line><text x="428" y="466" text-anchor="middle">Avg. tokens per trajectory (input + output)</text> <text x="20" y="228" text-anchor="middle" transform="rotate(-90 20 228)">Pass^3 (%)</text> <circle cx="291.3185530831897" cy="57.50400000000002" r="5" fill="#7c3aed"></circle><text x="305.3185530831897" y="55.50400000000002" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Claude Opus 4.6</text> <circle cx="388.7730298806373" cy="70.30400000000002" r="5" fill="#1d4ed8"></circle><text x="402.7730298806373" y="72.30400000000002" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Claude Sonnet 4.6</text> <g transform="translate(137.6774193548387 92.31999999999998)"><path d="M 0.00,-11.50 L 2.84,-3.91 L 10.94,-3.55 L 4.59,1.49 L 6.76,9.30 L 0.00,4.83 L -6.76,9.30 L -4.59,1.49 L -10.94,-3.55 L -2.84,-3.91 Z" fill="#FF6700" stroke="#fff" stroke-width="1.6"></path></g><text x="151.6774193548387" y="84.31999999999998" text-anchor="start" fill="#FF6700" style="font-size: 10.5px;font-size: 11.5px;">MiMo-V2.5-Pro</text> <line x1="464.35098101322853" y1="97.11904661822945" x2="502.28078403172015" y2="81.9471254108328"></line><circle cx="459.70859755880224" cy="98.97599999999997" r="5" fill="#0668E1"></circle><text x="509.70859755880224" y="78.97599999999997" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Muse Spark</text> <line x1="184.32046191370793" y1="103.80361720794193" x2="188.14818260531035" y2="105.23901246729284"></line><g transform="translate(179.6388160258627 102.04799999999997)"><path d="M 0.00,-11.50 L 2.84,-3.91 L 10.94,-3.55 L 4.59,1.49 L 6.76,9.30 L 0.00,4.83 L -6.76,9.30 L -4.59,1.49 L -10.94,-3.55 L -2.84,-3.91 Z" fill="#FF8A3D" stroke="#fff" stroke-width="1.6"></path></g><text x="195.6388160258627" y="108.04799999999997" text-anchor="start" fill="#FF8A3D" style="font-size: 10.5px;font-size: 11.5px;">MiMo-V2.5</text> <line x1="317.79388081226745" y1="101.35711652646563" x2="323.2333209099767" y2="95.14061355765504"></line><circle cx="314.50135777292485" cy="105.12000000000002" r="5" fill="#f472b6"></circle><text x="328.50135777292485" y="89.12000000000002" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Kimi K2.6</text> <circle cx="530.6961834973033" cy="111.77599999999997" r="5" fill="#059669"></circle><text x="518.6961834973033" y="109.77599999999997" text-anchor="end" fill="undefined" style="font-size: 10.5px;">GPT-5.4</text> <circle cx="408.64400532898173" cy="124.06400000000002" r="5" fill="#6366f1"></circle><text x="418.64400532898173" y="134.06400000000002" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Qwen3.5 397A17B</text> <circle cx="246.60712438240355" cy="127.64800000000001" r="5" fill="#909090"></circle><text x="256.6071243824035" y="127.64800000000001" text-anchor="start" fill="undefined" style="font-size: 10.5px;">MiMo-V2-Pro</text> <circle cx="204.59370945104357" cy="127.64800000000001" r="5" fill="#a78bfa"></circle><text x="194.59370945104357" y="127.64800000000001" text-anchor="end" fill="undefined" style="font-size: 10.5px;">GLM 5 Turbo</text> <circle cx="682.6484577067461" cy="133.79200000000003" r="5" fill="#f5a524"></circle><text x="670.6484577067461" y="131.79200000000003" text-anchor="end" fill="undefined" style="font-size: 10.5px;">Gemini 3.1 Pro</text> <line x1="217.46585640287765" y1="150.4859949365268" x2="200.28897741269552" y2="153.34880810155715"></line><circle cx="222.39782602203837" cy="149.66400000000002" r="5" fill="#8b5cf6"></circle><text x="192.39782602203837" y="154.66400000000002" text-anchor="end" fill="undefined" style="font-size: 10.5px;">GLM 5V Turbo</text> <line x1="238.15792446994564" y1="151.90006797749982" x2="246.53037098694674" y2="156.08629123600036"></line><circle cx="233.68578851494607" cy="149.66400000000002" r="5" fill="#ec4899"></circle><text x="253.68578851494607" y="159.66400000000002" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Kimi K2.5</text> <circle cx="387.20554630251314" cy="152.736" r="5" fill="#b91c1c"></circle><text x="394.20554630251314" y="162.736" text-anchor="start" fill="undefined" style="font-size: 10.5px;">MiMo-V2-Omni</text> <line x1="213.36598750065406" y1="170.20272803101528" x2="218.69925946963875" y2="184.0692351503755"></line><circle cx="211.5710921041097" cy="165.53599999999997" r="5" fill="#0d9488"></circle><text x="221.5710921041097" y="191.53599999999997" text-anchor="start" fill="undefined" style="font-size: 10.5px;">MiniMax M2.7</text> <line x1="180.07923686160058" y1="177.18576169438924" x2="179.72842588187117" y2="184.20198128897727"></line><circle cx="180.32892494632003" cy="172.192" r="5" fill="#ea4335"></circle><text x="179.32892494632003" y="192.192" text-anchor="end" fill="undefined" style="font-size: 10.5px;">Gemini 3 Flash</text> <circle cx="718.3225806451612" cy="203.93599999999998" r="5" fill="#0284c7"></circle><text x="706.3225806451612" y="201.93599999999998" text-anchor="end" fill="undefined" style="font-size: 10.5px;">DeepSeek V3.2</text> <circle cx="225.5050501061076" cy="385.18399999999997" r="5" fill="#84cc16"></circle><text x="239.5050501061076" y="387.18399999999997" text-anchor="start" fill="undefined" style="font-size: 10.5px;">Nemotron 3 Super</text></svg>

## Token Plan Updates

Alongside a stronger model, we've also upgraded our inference infrastructure. The Token Plan now comes with a few meaningful improvements:

![Token Plan updates](https://mimo.xiaomi.com/mimo-v2-5-pro/assets/tokenplan.png)

All users who purchased a Token Plan before 14:00 UTC on April 21 will have their used Credit balance reset.

## Open Source

MiMo-V2.5-Pro is now fully open-sourced under a permissive license. Weights, tokenizer, and the full model card are available on Hugging Face.

### Model specifications

| Model | Total Params | Active Params | Context | Precision | Download |
| --- | --- | --- | --- | --- | --- |
| MiMo-V2.5-Pro-Base | 1.02T | 42B | 256K | FP8 (E4M3) Mixed | [Hugging Face](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro-Base) |
| MiMo-V2.5-Pro | 1.02T | 42B | 1M | FP8 (E4M3) Mixed | [Hugging Face](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro) |

### Architecture & training

MiMo-V2.5-Pro inherits the **hybrid attention** and **Multi-Token Prediction (MTP)** design from [MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash). Local Sliding Window Attention (SWA) and Global Attention (GA) are interleaved at a 6:1 ratio with a 128-token window, which cuts KV-cache storage by nearly 7× at long context while preserving performance through a learnable attention-sink bias. A lightweight MTP module with dense FFNs is natively integrated for training and inference, roughly tripling output throughput and accelerating RL rollouts.

Pre-training runs on **27T tokens** using **FP8 mixed precision** at a native 32K sequence length, with context extended up to 1M tokens. Post-training follows the three-stage paradigm introduced in MiMo-V2-Flash: (1) **Supervised Fine-Tuning** to establish foundational instruction following on curated data pairs; (2) **Domain-Specialized Training**, where separate teacher models are each optimized via domain-specific RL across math, safety, agentic tool-use, and more; and (3) **Multi-Teacher On-Policy Distillation (MOPD)**, where a single student model learns on-policy from its own rollouts under token-level guidance from every specialist teacher, merging their capabilities into one unified model.

See the [model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro) on Hugging Face for architecture details, evaluation tables, and deployment guides for SGLang and vLLM.

### Full benchmark results

Best open-source Best overall

<table><thead><tr><th>Benchmark</th><th>MiMo-V2.5-Pro1.02T / 42B</th><th>MiMo-V2-Pro1.02T / 42B</th><th>DeepSeek V4 Pro1.6T / 49B</th><th>Kimi K2.61T / 32B</th><th>GLM 5.1744B / 40B</th><th>Gemini 3.1 Pro</th><th>GPT-5.4</th><th>Claude Opus 4.6</th></tr></thead><tbody><tr><td colspan="9">General Agent</td></tr><tr><td>GDPVal-AA (Elo)</td><td>1581</td><td>1426</td><td>1554</td><td>1480</td><td>1535</td><td>1317</td><td>1674</td><td>1606</td></tr><tr><td>τ³-bench</td><td>72.9</td><td>64.5</td><td>71.8</td><td>71.0</td><td>70.6</td><td>67.1</td><td>72.9</td><td>72.4</td></tr><tr><td>Claw-Eval (pass^3)</td><td>63.8</td><td>57.8</td><td>59.8</td><td>62.3</td><td>62.7</td><td>57.8</td><td>60.3</td><td>70.4</td></tr><tr><td>Humanity's Last Exam</td><td>48.0w.o. tools34.0</td><td>40.0w.o. tools28.0</td><td>48.2w.o. tools37.7</td><td>54.0w.o. tools34.7</td><td>52.3w.o. tools31.0</td><td>51.4w.o. tools44.4</td><td>58.7w.o. tools42.7</td><td>53.0w.o. tools40.0</td></tr><tr><td colspan="9">Coding Agent</td></tr><tr><td>SWE-Bench Pro</td><td>57.2</td><td>55.0</td><td>55.4</td><td>58.6</td><td>58.4</td><td>54.2</td><td>57.7</td><td>57.3</td></tr><tr><td>SWE-bench Verified</td><td>78.9</td><td>78.0</td><td>80.6</td><td>80.2</td><td>—</td><td>76.2</td><td>—</td><td>80.8</td></tr><tr><td>Terminal-Bench 2.0</td><td>68.4</td><td>57.1</td><td>67.9</td><td>66.7</td><td>69.0</td><td>68.5</td><td>75.1</td><td>65.4</td></tr><tr><td>FrontierSWE (Impl.)</td><td>#3.4</td><td>#5.0</td><td>—</td><td>—</td><td>—</td><td>#3.9</td><td>#1.9</td><td>#2.0</td></tr></tbody></table>

Higher is better unless marked (rank). "—" = not evaluated. DeepSeek V4 Pro numbers are with its `max` effort setting.
