---
id: requirements-matrix
type: matrix
palace_ids: []
phase: PDF_INGEST
batch: S1
sources: ["raw/state/requirements.json"]
status: live
---

# Requirements-Matrix

22 requirements extracted from the brief. Every one has a coverage location. **22/22 covered.**

## Legend

- **Type** — `must` (required), `must_not` (prohibited), `should` (expected)
- **Hard** — a violation disqualifies a candidate solution *before* scoring

## The matrix

| ID | Type | Hard | Requirement | Covered in |
|---|---|---|---|---|
| R01 | must | **Y** | Integrate one idea across six media, not size-adapt it | `06_INTEGRATION_PROOF.md` (whole) |
| R02 | must | | Select a single state | `02` §1, `00_README` |
| R03 | must | | Define the target group | `01` §3, `02` §2 |
| R04 | must | | Ground the campaign in research | `02` (whole) |
| R05 | **must_not** | **Y** | No sight-seeing / shopping / common spots | `02` §1, re-verified `06` §6 |
| R06 | must | | Identify and state the USP | `01` §2, `02` §3 |
| R07 | must | | Produce a key creative | `01` §6, `03` |
| R08 | must | | Three traditional channels | `04` |
| R09 | must | | Three digital channels | `05` |
| R10 | must | **Y** | Craft the idea to suit each medium | `06` §2 Swap Test |
| R11 | must | | Articulate a creative strategy | `01` §5 |
| R12 | must | | Present a big idea | `01` §4 |
| R13 | should | | Make the campaign coherent as one campaign | `01` §8, `06` §4 |
| R14 | must | | Minimum three creative routes at Week 01 | `07` (five developed) |
| R15 | must | | Week 02: develop the chosen route fully | `08` §2, `01`–`06` |
| R16 | must | | Deliver a campaign deck | `01` |
| R17 | should | | Respect the stated two-week structure | `08` §1–2 |
| R18 | should | | Acknowledge practical feasibility | `08` §3, `09` |
| R19 | should | | Show audience reasoning, not assertion | `02` §2 |
| R20 | should | | Demonstrate craft in execution | `03`, `04`, `05` |
| R21 | should | | Address responsible tourism | `09` C1–C3 |
| R22 | must | | Prove integration rather than claim it | `06` §2–§3 |

## Hard constraints in detail

Three requirements are load-bearing enough that a candidate violating them is removed before scoring rather than penalised within it.

| ID | Why it is hard |
|---|---|
| **R05** | An explicit `must_not` in the brief. A campaign that slides into sightseeing has failed the brief's own terms regardless of quality |
| **R01** | The brief's stated purpose. Adapt-campaign behaviour is the specific failure mode being tested |
| **R10** | The operational form of R01. Without per-medium crafting, R01 cannot be satisfied |

Two candidates were eliminated on these grounds — see [[Path-Rank]].

## Coverage discipline

Grading weights are inferred, not stated ([[Rubric-Guess]]). **No requirement was skipped or down-prioritised on the basis of an inferred weight.** Low-weight requirements receive coverage locations identically to high-weight ones. Inference informs balance, never omission.

## Linked

[[Assignment-Brief]] · [[Constraints-And-Deliverables]] · [[Rubric-Guess]] · [[Solution-Architecture]]
