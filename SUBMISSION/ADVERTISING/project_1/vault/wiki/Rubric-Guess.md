---
id: rubric-guess
type: inference
palace_ids: []
phase: PDF_INGEST
batch: S1
sources: ["raw/state/rubric_guess.json"]
status: live
---

# Rubric-Guess

**This article records an inference. It is labelled as such everywhere it is used.**

## What the brief states

Four grading criteria, named, with **no weights**:

- Research
- Strategy
- Execution
- Presentation

## What is inferred

| Criterion | Inferred weight | Reasoning |
|---|---|---|
| Research | 0.25 | The brief demands niche selection and audience definition, both research-dependent |
| Strategy | 0.25 | USP and creative strategy are separately named tasks |
| **Execution** | **0.30** | Six media executions plus a key creative account for most of the required output volume |
| Presentation | 0.20 | A deck is the named deliverable, but it packages the other three rather than standing alone |

Sum: 1.00.

## Rubric hash lineage

| Rubric | Hash |
|---|---|
| Prompt 1 (stamped in package) | `sha256:archetype_scoring_rubric_1_0_0_chart_analyst_v4` |
| Prompt 2 (applied this phase) | `sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4` |

The difference is **lineage, not staleness**: `requirement_fit_score` is null under Prompt 1 and live under Prompt 2, and the rubric change encodes exactly that reversal. Logged as `RUBRIC_HASH_LINEAGE`, severity LOW. Both hashes are recorded in `MANIFEST.md`.

Critically, `interpretation_protocol_v2_version_hash` — the hash that actually governs `PACKAGE_STALE` — **matched the reference exactly**. Had it differed, the correct action would have been to halt, not to note and proceed.

## How the inference is used, and how it is not

**Used for:** checking that the submission's effort is balanced — that Execution, the heaviest criterion, receives the most output.

**Never used for:** justifying the omission or thinning of any requirement. Every one of the 22 requirements in [[Requirements-Matrix]] has a coverage location regardless of which criterion it serves.

This distinction matters. An inferred weight used to skip work would convert a guess into a silent scope cut. An inferred weight used to check balance is a sanity test with no downside if wrong.

## Residual risk

If the real weights differ substantially — for instance if Research were 0.40 — the submission would still cover every requirement, but its effort distribution would be suboptimal. That risk is accepted and disclosed rather than mitigated, because mitigating it would require information the brief does not provide.

## Linked

[[Requirements-Matrix]] · [[Assignment-Brief]] · [[Risk-And-Audit-Log]]
