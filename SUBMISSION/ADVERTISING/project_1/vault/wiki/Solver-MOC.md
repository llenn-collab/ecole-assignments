---
id: solver-moc
type: moc
palace_ids: []
phase: SYNTHESIZE
batch: S3
sources: ["raw/assignment/Assignment.md", "raw/package/chart_analysis_package.json"]
status: live
---

# Solver-MOC — Carpathia Assignment Solver

Run: assignment-solver v4.0.0 · Assignment `ADVERTISING/project_1` · Verdict **PASS (8/8)**

Chart-phase map of content: [[MOC]]. This article maps the **solver** phase only.

## Inputs

| Input | Hash | Read? |
|---|---|---|
| `ASSIGNMENTS/ADVERTISING/project_1.md` | `96a17883…f9d6` | Yes |
| `chart_analysis_package.json` | `59ddb7ea…` | Yes |
| `QMDJ/ADVERTISING/project_1.json` | `083a393c…` | **Never — law 8, 0 reads** |

## Articles

### The brief
- [[Assignment-Brief]] — what is asked, and the stated purpose that drives everything
- [[Assignment-Corpus]] — addressable text and the Markdown anchor scheme
- [[Requirements-Matrix]] — 22 requirements, 22 covered
- [[Constraints-And-Deliverables]] — registry (10/10 delivered) and constraint set
- [[Rubric-Guess]] — inferred grading weights, labelled as inference
- [[Logo-Boundary]] — `EXCLUDE_ARTWORK`

### The reasoning
- [[Hidden-Problems]] — five live problems, one withheld
- [[Recommended-Answers]] — two live answers, one rejected
- [[Solution-Architecture]] — how the chart reading became a campaign
- [[Solution-Live]] — the live claim register, 8 claims, 0 uncited
- [[Path-Rank]] — full rankings with published margins

### The scrutiny
- [[Risk-And-Audit-Log]] — 8 gates, failures found and fixed at source
- [[Red-Team]] — 8 adversarial attacks, 4 land, all pre-disclosed

## Output trees

| Tree | Files | Audience |
|---|---|---|
| `output/SUBMISSION/` | 10 | The assessor. Pure English, lint-verified |
| `output/ANNOTATED/` | 1 | The student. Ordinary-English situation commentary |
| `output/OPERATOR/` | 3 | The operator. Chart terminology permitted |
| `output/LAYER_A/` | 1 | Technical audit, 5 sections in fixed order |
| `output/MANIFEST.md` | 1 | Hashes, verdict, compliance |

## The answer in one line

**Lead with participation, not spectacle** — an invitation the audience accepts and passes on, with every medium doing one job the other five cannot do.

Realised as *The Hundred-Year Handshake* for Meghalaya's living root bridges: the only place where the landmark you came to see is not finished, and where you can add to it.

## Run properties

| Property | Value |
|---|---|
| States traversed | INIT → PACKAGE_VALIDATE → PDF_INGEST → P7_SLOT_BIND → SOLUTION_ENGINE → SYNTHESIZE |
| Slot bindings | 6/6, 0 unbound |
| Resolutions | 3, all RESOLVED, 0 `STILL_TIED` |
| Live claims | 8, all citing a resolution |
| Hard eliminations | 2, before scoring |
| Anomalies | 1 LOW, 1 INFO |
| AUDIT_FIX cycles | 0 of 3 |
| `QMDJ.json` reads | 0 |

## Tools

`tools/solver_common.py` · `tools/s1_ingest.py` · `tools/s2_solution_engine.py` · `tools/s3_audit.py`

Chart-phase tools reused unmodified and not re-run.
