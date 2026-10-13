---
license: mit
---

# FrogNano

# Model summary

|Field | Value
| --- | --- |
| Developer | Microsoft Corporation |
| Description | FrogNano is a compact repository-level coding agent derived from Qwen/Qwen3.5-4B. It is post-trained exclusively with reinforcement learning on approximately 1,500 synthetic software-engineering tasks generated, validated, and calibrated against the evolving policy using TaskPilot. FrogNano operates through the lightweight five-tool Leaf harness. Its agent-specific post-training uses no stronger-model solution trajectories, actions, reasoning traces, or patch targets. |
| Model architecture | *Dense 32-layer hybrid Gated DeltaNet/gated-attention causal language model; vision components are inherited but not post-trained.* |
| Parameters | *500M-5B* |
| Inputs | *Text only for* *FrogNano’s* *intended and evaluated use, including natural-language instructions, source code, and textual tool outputs.* *FrogNano's* *main benchmark evaluations use a combined interaction context of approximately 131K tokens, including room for generated output. The upstream checkpoint* *contains* *image and video input components, but* *FrogNano* *did not post-train or evaluate those modalities and does not claim them as supported.* |
| Outputs | *Text, including natural-language responses, reasoning text, source code, and structured tool calls. The validated FrogNano configuration allows up to 8,192 generated tokens per assistant turn.* |
| Context length | Approximately 131K tokens in the evaluated FrogNano coding-agent configuration. |
| Training Dates | *Jun* *2026* *to* *Aug* *2026* |
| Release date | *22-SEP-2026* |
| Release date in the EU (if different) |  |
| License | Apache License 2.0. FrogNano is derived from Qwen/Qwen3.5-4B; applicable upstream copyright and attribution notices are retained. |
| Model dependencies: | [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) |
| List and link to any additional related assets | [Technical report;](https://aka.ms/frognano-tech-report) [Leaf harness.](https://github.com/microsoft/FrogNano) |
| Acceptable use policy | *N/A* |
 
# 1. Model overview
FrogNano is derived from Qwen/Qwen3.5-4B, a general-purpose post-trained model designed for language, reasoning, coding, agentic, and multimodal tasks. FrogNano inherits Qwen3.5-4B's dense 32-layer hybrid Gated DeltaNet and gated-attention architecture, but its additional post-training is text-only and focused on repository-level software engineering. The model is further trained using reinforcement learning on approximately 1,500 synthetic SWE task environments generated and calibrated against the evolving policy using TaskPilot. Training uses the five-tool Leaf harness and executable test-based rewards over complete multi-turn coding trajectories.

The additional post-training is intended to improve long-horizon repository navigation, debugging, code editing, test execution, and patch generation in a compact 4B model. Unlike approaches based on behavioral distillation, FrogNano does not train on stronger-model solution trajectories, actions, reasoning traces, or patch targets. This specialization also introduces limitations and risks: performance is sensitive to the Leaf harness and test quality, training data are Python-heavy and primarily English, and generated patches may be incorrect or insecure despite passing available tests. When integrated with the Leaf harness, FrogNano generates structured tool calls that can propose repository changes. Leaf executes authorized tool calls within an isolated repository environment to produce a candidate patch; FrogNano does not itself deploy the changes. Any resulting patches require human review, regression testing, and security validation before use or deployment. 
## 1.1 Key model capabilities
• Repository-level software issue resolution from natural-language task descriptions and existing source code.

• Codebase navigation, cross-file code understanding, debugging, bug fixing, and feature implementation.

• Generation of structured Leaf tool calls that the harness executes in an isolated repository environment to inspect and search files, edit code, run shell commands, and run tests.

• Iterative generation and refinement of multi-file patches using command and test feedback.

• Long-context processing of text and source code, with a supported combined context length of approximately 131K tokens.
## 1.2 Alignment approach
FrogNano starts from the post-trained Qwen3.5-4B checkpoint and retains its upstream alignment characteristics, subject to changes introduced by subsequent reinforcement learning. FrogNano-specific post-training did not use dedicated safety-preference, refusal, harmful-content, or adversarial datasets. Instead, it applied executable-reward reinforcement learning to approximately 1,500 synthetic repository-level software-engineering tasks generated and calibrated through TaskPilot; generated task tests and existing regression tests rewarded functional correctness, reliable tool use, and preservation of existing behavior. This process was designed primarily for coding performance and regression avoidance, not for broad content-safety or cyber-misuse prevention, so FrogNano should not be considered independently safety-aligned for unrestricted autonomous deployment.
# 2. Usage
## 2.1 Primary use cases
FrogNano is intended for software-engineering research and human-supervised development. Given an authorized repository snapshot and an English natural-language issue, the model generates text and structured Leaf tool calls. The Leaf harness executes those calls within an isolated repository environment, enabling iterative file inspection and search, code editing, shell-command and test execution, and production of a candidate patch. This workflow supports bug diagnosis and repair, scoped feature implementation, regression fixing, test-driven code maintenance, and research on long-horizon coding agents. A candidate patch is a proposal, not an approved change, and requires qualified human review and independent regression and security testing before use or deployment.

FrogNano is best suited to English-language, Python-heavy repositories with reproducible environments, clearly scoped tasks, and executable test suites. It is intended for use within the sandboxed Leaf harness or a comparably controlled environment, with generated changes reviewed by a qualified developer and subjected to regression and security testing before deployment.
## 2.2 Out-of-scope use cases
FrogNano was not designed or evaluated as a general-purpose assistant, a multimodal model, or a source of guaranteed correct, secure, or production-ready code. Image and video use are unsupported despite components inherited from the base model. Performance has not been established for non-English interaction, repositories substantially different from its Python-heavy training setting, formal verification, safety-critical software, or high-impact medical, legal, financial, industrial, or critical-infrastructure applications.

FrogNano was not designed or evaluated for integration into workflows that act directly on production systems, access repositories without authorization, or give the executing harness unrestricted access to credentials, sensitive data, networks, or privileged infrastructure. Resulting repository changes are candidate patches and are not automatically deployed; they must not be merged or deployed without qualified human code review and appropriate functional, regression, and security testing. FrogNano is not intended to support harmful or illegal software activity, including unauthorized system access, malware deployment, credential theft, vulnerability exploitation without authorization, or evasion of security controls.
## 2.3 Distribution channels
FrogNano’s distribution channels include:

• Public access to downloadable model weights, configuration files, tokenizer assets, and the model card through a Hugging Face model repository.

https://huggingface.co/microsoft/FrogNano-4B-2609

• Public access to the technical report and any released inference, agent-harness, or evaluation code through a GitHub repository.

https://github.com/microsoft/FrogNano
## 2.4 Technical requirements and integration guidance
FrogNano requires an inference runtime that supports the Qwen3.5 architecture. The upstream architecture is compatible with Hugging Face Transformers, vLLM, SGLang, and KTransformers; FrogNano’s documented rollout configuration uses SGLang on GPU servers. In BF16, the approximately 4.66-billion-parameter checkpoint requires about 9.3 GB for model weights alone, with additional memory needed for runtime state, tool-call concurrency, and the key-value cache. Memory requirements increase substantially as the combined context approaches FrogNano’s evaluated limit of approximately 131K tokens. The exact minimum GPU model, VRAM configuration, runtime versions, and performance profile must still be validated before release.

Repository-agent integration requires the model tokenizer and chat template, JSON-schema tool-call parsing, and the Leaf interaction loop. Leaf provides five tools for reading, writing, and editing files, glob-based search, and shell execution. These tools should operate inside an isolated repository sandbox with bounded permissions, timeouts, resource limits, and test execution. A response containing tool calls continues the interaction; a response without a tool call terminates it. The main benchmark evaluations use a budget of 150 interaction steps and approximately 131K context tokens. The documented RL training configuration allows up to 8,192 generated tokens per assistant turn. The first four training iterations used a 65,536-token context limit and 75 tool turns; the fifth iteration increased these limits to approximately 131K tokens and 150 turns.

FrogNano is suitable for controlled research agents, developer-assistance systems, and human-AI coding workflows in which patches are reviewed and tested before use. It is not suitable for unrestricted autonomous production access, safety-critical applications, or systems that permit unreviewed changes to privileged infrastructure. English is the supported natural-language interaction language, and Python is the primary validated programming-language domain; other natural and programming languages have not been adequately evaluated for FrogNano, even though the upstream model advertises broader multilingual support. CPU-only servers, desktop operating systems, mobile devices, and optimized or quantized FrogNano formats have not yet been validated; no separate optimized-format links are currently available.
## 2.5 Supported languages
FrogNano-specific post-training and evaluation primarily use English task descriptions, so no additional natural languages are currently claimed as supported. The upstream Qwen3.5-4B model advertises broader multilingual coverage, but this has not been independently validated for FrogNano.
## 2.6 Responsible AI considerations
Developers should perform a documented use-case and impact assessment, comply with applicable privacy, intellectual-property, cybersecurity, accessibility, employment, sector-specific, and AI laws, and process only code and data they are authorized to access. FrogNano should run in an isolated, least-privilege sandbox with network access disabled by default, tightly scoped credentials, filesystem and command restrictions, resource and time limits, action logging, and incident-response procedures. All generated changes should receive qualified human review and appropriate functional, regression, security, privacy, and license-compliance testing before use. FrogNano has not been validated for high-risk, safety-critical, or consequential applications; any proposed use in such settings requires independent domain validation, meaningful human oversight, appeal or override mechanisms, fail-safe behavior, and ongoing monitoring. Additional governance guidance is available in [Microsoft’s Responsible AI resources](https://www.microsoft.com/en-ca/ai/responsible-ai).
## 2.7 Known limitations
FrogNano is specialized for English-language, Python-heavy repository tasks using the Leaf harness. It may underperform on non-English instructions, other programming languages and frameworks, unfamiliar repository structures, ambiguous or underspecified issues, projects without reliable tests, and tasks that exceed its context or tool budget. Its image and video components were inherited from Qwen3.5-4B but were not post-trained or evaluated for FrogNano and are therefore unsupported. Performance is also sensitive to the agent harness, prompt format, available tools, and execution environment.

FrogNano may misunderstand requirements, hallucinate APIs or repository behavior, make incomplete or overly broad edits, introduce regressions or vulnerabilities, or produce a patch that passes available tests without being correct or secure. It inherits potential biases, stereotypes, offensive-content behavior, and representation gaps from the base model and upstream data; these risks were not comprehensively reevaluated after coding-focused post-training and may appear in comments, documentation, identifiers, generated logic, or user-facing behavior. Its coding and tool-use capabilities could also be misused for malware, unauthorized vulnerability exploitation, or other harmful automation. Outputs require sandboxed execution, human review, and independent functional and security validation.
# 3. Quality and performance evaluation
FrogNano’s evaluation focuses on repository-level software engineering and terminal-based tasks. The Qwen3.5-4B base model achieved an Avg@3 resolution rate of 39.4% when evaluated on SWE-bench Verified using the Leaf harness. Across five TaskPilot-guided RL iterations, the resolution rate increased to 49.1%, 53.1%, 56.7%, 59.1%, and 61.5%, respectively. Training used approximately 1,500 policy-calibrated synthetic software-engineering tasks in total, yielding an improvement of 22.1 percentage points, or approximately 56% relative to the base model.

On the held-out benchmarks, FrogNano achieved Avg@3 resolution rates of 37.6% on SWE-bench Pro, 31.1% on Terminal-Bench 2.0, and 47.3% on PatchEval-Verified. Appendix C of our technical report additionally provides Pass@3 scores of 71.0% on SWE-bench Verified and 47.6% on SWE-bench Pro. FrogNano has not been separately evaluated for general language understanding, mathematics, or multilingual performance, and upstream Qwen3.5-4B scores in those areas should not be attributed to FrogNano.
## 3.1 Benchmarking methodology 
FrogNano is evaluated on four benchmarks. SWE-bench Verified contains 500 human-validated issues from real Python repositories and serves as the validation set. The other three benchmarks are held-out test sets: SWE-bench Pro contains 731 longer-horizon tasks from 11 repositories spanning Python, JavaScript, TypeScript, and Go; Terminal-Bench 2.0 contains 89 tasks covering software engineering, system administration, security, machine learning, and scientific computing; and PatchEval-Verified contains 230 real CVE repair cases disclosed between 2015 and 2025 across Python, JavaScript, and Go.

The benchmark evaluations use the Leaf harness with each benchmark’s official isolated execution environment and verifier. Each trajectory has a budget of 150 interaction steps and approximately 131K context tokens, with a sampling temperature of 0.6 and a repetition penalty of 1.0. Within each benchmark, model comparisons use the same harness configuration and per-trajectory budget unless explicitly stated otherwise.

For SWE-bench Verified and SWE-bench Pro, the agent starts from the unmodified repository and submits one patch per trajectory. A task succeeds only if the patch passes all designated fail-to-pass tests while preserving the pass-to-pass tests. Terminal-Bench 2.0 uses automated tests to grade the final task-specific container state rather than a submitted repository patch. PatchEval-Verified applies the submitted patch in the case’s Docker environment and uses a dynamic validator to check whether the vulnerability is repaired, without requiring the patch to match the original developer solution.

Patches or final environment states are evaluated when the agent terminates, including after exhausting its step budget. Budget exhaustion alone does not automatically imply failure; partial solutions, patches that fail to apply, and invalid final states count as failures. Avg@3 measures single-attempt success, with scores averaged across three seeds. Pass@3, reported for SWE-bench Verified and SWE-bench Pro, measures whether at least one of three sampled trajectories succeeds and is distinct from the average single-attempt score.
## 3.2 Safety evaluation and red-teaming
FrogNano is a compact model released primarily as a research artifact for studying repository-level coding agents, rather than as a production-ready model for integration into consumer-facing or consequential products. Its safety evaluation is scoped mainly to risks arising in controlled software-engineering research. Executable benchmark tests provide evidence of functional correctness, regression avoidance, and vulnerability repair, but passing those tests does not establish that a patch is correct or secure beyond the behavior they cover.

The technical report includes failure-mode analyses and reward-hacking assessments of benchmark trajectories. No successful reward hacks were identified for FrogNano in the analyzed evaluations under the benchmark harness and infrastructure controls. These findings do not establish comprehensive safety against insecure code generation, harmful coding requests, prompt injection through repository content, unauthorized tool actions, or exposure of secrets or copyrighted code; those areas require separate evaluation.

FrogNano has not undergone the comprehensive product-level red-teaming needed to establish safety across sexual, violent, hateful, or self-harm content; bias and representation; copyright and IP; privacy; jailbreaks; or broader cyber misuse. Its small size and research positioning do not eliminate these risks. Practitioners should not treat the model as suitable for production deployment without conducting application-specific safety testing, red-teaming, legal review, sandboxing, access control, and ongoing monitoring.
# 4. Data overview
## 4.1 Training, testing, and validation datasets
**4.1.1 Size of dataset and characteristics**

The current release description targets approximately 1,500 validated synthetic SWE task environments across five TaskPilot iterations. Each environment contains a repository snapshot, runtime, problem statement, reference patch, generated grading tests, and existing regression tests. Multiple online policy trajectories are generated for task calibration and reinforcement learning. 

**4.1.2.A Text training data size:**

1 billion to 1 trillion tokens

**4.1.2.B Text training data content:**

Source code, software issue descriptions, synthetic problem statements, reference patches, generated and existing tests, model-generated reasoning, JSON-schema tool calls, file and search results, shell-command output, test logs, and generated code patches.

**4.1.2.C Image training data size:** 

Not applicable. Images are not part of the training data

**4.1.2.D Image training data content:** 

*Not applicable*

**4.1.3.A Audio training data size:** 

Not applicable. Audio data is not part of the training data

**4.1.3.B Audio training data content:** 

*Not applicable*

**4.1.4.A Video training data size:** 

Not applicable. Video data is not part of the training data

**4.1.4.B Video training data content:** 

*Not applicable*

**4.1.5.A Other training data size:** 

*Not applicable*

**4.1.5.B Other training data content:** 

*Not applicable*

**4.1.6 Latest date of data acquisition/collection for model training:** 20-AUG-2026

**4.1.7 Is data collection ongoing to update the model with new data collection after deployment?** 

No

**4.1.8 Date the training dataset was first used to train the model:** JUN 2026

**4.1.9 Rationale or purpose of data selection:** 

The data were selected to train repository-level coding behavior using realistic codebases and objective executable feedback. Jointly generated problems, patches, and tests provide verifiable task outcomes, while current-policy calibration retains tasks that supply useful reinforcement-learning signal as the model improves, without using stronger-model solution trajectories as behavioral targets.
## 4.2 List of data sources

### 4.2.1 Publicly available datasets

**4.2.1A Have you used publicly available datasets to train the model?**

Yes

### 4.2.2 Private non-publicly available datasets obtained from third parties 

#### 4.2.2.1 Datasets commercially licensed by rightsholders or their representatives 

**4.2.2.1A Have you concluded transactional commercial licensing agreement(s) with rightsholder(s) or with their representatives?** 

No

#### 4.2.2.2 Private datasets obtained from other third parties 

**4.2.2.2.A Have you obtained private datasets from third parties that are not licensed as described in Section 2.2.1, such as data obtained from providers of private databases, or data intermediaries?** 

No

## 4.3 Personal Data
**4.3.1 Was personal data used to train the model?** Microsoft follows applicable laws and best practices pertaining to personal data.
### 4.4 Synthetic data 
**4.4.1 Was any synthetic AI-generated data used to train the model?** 

Yes. TaskPilot uses an AI task-authoring model to generate problem statements, reference patches, and hidden tests from real repository snapshots. These synthetic artifacts define executable training environments and reward signals rather than stronger-model solution trajectories or behavioral targets. FrogNano also learns from online Leaf trajectories generated by the evolving FrogNano policy itself during reinforcement learning.
## 4.5 Data processing aspects 
### 4.5.1 Respect of reservation of rights from text and data mining exception or limitation 
**4.5.1A Does this dataset include any data protected by copyright, trademark, or patent?** Microsoft follows applicable laws and best practices for processing data protected by copyright, trademark, or patent.
### 4.5.2 Other information 
**4.5.2A Does the dataset include information about consumer groups without revealing individual consumer identities?** Microsoft follows applicable laws and best practices for protecting consumer identities.

**4.5.2B Was the dataset cleaned or modified before model training?** 

Yes. Candidate tasks are executable-validated, filtered, and sometimes repaired before training. Generated fail-to-pass tests must fail on the original repository and pass with the reference patch, existing pass-to-pass tests must remain stable, and current-policy calibration retains only mixed-success tasks. Candidates that remain invalid, saturated, or unsolved across the calibration rollouts are discarded.

# 5. Contact
Requests for additional information can be directed to [MSFTAIActRequest@microsoft.com](mailto:MSFTAIActRequest@microsoft.com).

**Authorized representative:** Microsoft Ireland Operations Limited 70 Sir John Rogerson’s Quay, Dublin 2, D02 R296, Ireland
