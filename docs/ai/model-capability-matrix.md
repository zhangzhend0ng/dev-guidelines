# Model Capability Matrix

This document defines default autonomy for AI models used in this repository.
The goal is to reduce human workload by making most decisions automatic.
Human intervention is reserved for exceptions, high-risk actions, or repeated failures.

## Levels

| Level | Default Use | Allowed Actions | Human Involvement |
|------|-------------|-----------------|-------------------|
| T0 | Untrusted / new model | Summarize, classify, extract facts | Spot-check only |
| T1 | Weak but usable model | Plan, select harnesses, explain risks, produce short status updates | Required only before editing |
| T2 | Repository-calibrated model | Small bounded patch, review, verification summaries | Required at approval gate |
| T3 | Strong model with eval pass | Multi-file change within a known subsystem | Required for final review only |
| T4 | Autonomous tool-using agent | Tool calls, file edits, verification loops | Human approval for high-impact actions |

## Default Policy

1. Unknown models start at T0/T1.
2. Weak models must use the weak-model prompt templates.
3. A model may move up one level only after repo-specific evals pass.
4. Failures that repeat twice reduce the allowed level.
5. Failures that repeat three times require human or stronger-model takeover.
6. Human work should only be needed for approval, escalation, or judgment calls.

## C++ Task Mapping

| Task Type | Minimum Level | Notes |
|-----------|---------------|-------|
| Harness selection | T1 | Must list applicable harnesses before editing |
| Small C++ fix | T2 | Must include build/test evidence |
| Multi-file subsystem change | T3 | Must include review + rollback path |
| Tool-driven workspace edits | T4 | Must obey tool-control harness |

## Progress Reporting Rule

Weak models should keep user-visible updates short:
- one-line goal at start
- one-line status at each boundary
- one-line blocker if stuck
- one concise final summary

Do not print hidden reasoning, raw logs, repeated file listings, or long narrative steps.

