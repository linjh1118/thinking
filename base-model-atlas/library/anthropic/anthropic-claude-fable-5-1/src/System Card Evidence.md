# Claude Fable 5.1 & Claude Mythos 5.1 System Card — Evidence Note

> Source: 212-page Anthropic System Card, visually reviewed on 2026-09-02. This file is a compact evidence map, not a substitute for the official PDF.

## Deployment identity

- Executive Summary, pp. 2-4: Fable 5.1 and Mythos 5.1 are two configurations of the same underlying model.
- Fable 5.1 is generally available with additional safeguards; Mythos 5.1 is restricted to trusted access.
- The card evaluates RSP risk, cyber, safeguards / harmlessness, agentic safety, alignment, model welfare, and capabilities.

## Capability pages checked

- pp. 168-170: SWE-bench family, DeepSWE, FrontierCode, FrontierSWE.
- pp. 171-174: Terminal-Bench 4.0, Terminal-Bench-Science 0.1, CursorBench, CritPT-Corrected, ArXivMath.
- pp. 175-183: long context, ProgramBench, agentic search, HLE, multi-agent harnesses.
- pp. 184-197: multimodal, OSWorld, knowledge work, Toolathlon, AutomationBench, ARC-AGI.

## Important configuration notes

- Terminal-Bench 4.0 used Claude Code in `--bare` mode and maximum thinking effort for the headline result.
- Benchmark context-window sizes depend on the evaluation; not every evaluation used the full 1M context.
- Fable 5.1 results can include safety classifiers and fallback behavior, so the deployed system may not behave like one unmediated checkpoint.
- OSWorld partial and strict scores should be retained together; partial success alone overstates end-to-end reliability.

## Safety / alignment evidence boundary

- The system card reports stronger cyber capabilities than earlier Anthropic releases while still assessing the model below the higher FCF cyber risk tier.
- It documents classifiers and fallback routing for some high-risk requests.
- It reports external testing observations and limitations; these should not be flattened into a generic “safe” label.

## What the System Card does not disclose

Parameter count, full architecture, full training-data mixture, optimizer, detailed post-training recipe, and complete RL environment design are not public. The main note therefore avoids reverse-engineering those details from product behavior.

