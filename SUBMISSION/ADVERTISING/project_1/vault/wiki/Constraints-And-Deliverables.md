---
id: constraints-and-deliverables
type: registry
palace_ids: []
phase: PDF_INGEST
batch: S1
sources: ["raw/state/deliverable_registry.json", "raw/state/requirements.json"]
status: live
---

# Constraints-And-Deliverables

## Deliverable registry — brief-derived

The registry is derived from the brief, **not** from a fixed template. The `UNGROUNDED_PACK` fallback was **not** used, because the brief is explicit about structure (deck, routes, six media, two-week milestones).

| ID | File | Derived from | Status |
|---|---|---|---|
| D01 | `01_CAMPAIGN_DECK.md` | "Deliverable: campaign deck" | **DELIVERED** |
| D02 | `02_RESEARCH_AND_INSIGHT.md` | Niche selection, USP, target group, Research criterion | **DELIVERED** |
| D03 | `03_KEY_CREATIVE.md` | "Key creative" as a named task | **DELIVERED** |
| D04 | `04_TRADITIONAL_MEDIA.md` | Three traditional channels | **DELIVERED** |
| D05 | `05_DIGITAL_MEDIA.md` | Three digital channels | **DELIVERED** |
| D06 | `06_INTEGRATION_PROOF.md` | Stated purpose: integrated vs adapt | **DELIVERED** |
| D07 | `07_CREATIVE_ROUTES.md` | "Week 01: minimum three routes" | **DELIVERED** |
| D08 | `08_DELIVERY_PLAN.md` | Two-week timeline structure | **DELIVERED** |
| D09 | `09_RISK_REGISTER.md` | Feasibility and responsible-tourism expectations | **DELIVERED** |
| D10 | `00_README.md` | Navigability of a multi-document deck | **DELIVERED** |

**10/10 delivered.** Verified mechanically by audit gate 6.

## Constraints

### Hard (elimination before scoring)

| ID | Constraint |
|---|---|
| R05 | No sight-seeing / shopping / common spots |
| R01 | Integration across six media, not size adaptation |
| R10 | The idea must be crafted to suit each medium |

### Policy constraints from the solver role

| Constraint | Effect |
|---|---|
| Never read `QMDJ.json` | Audit gate 0a; `guard_path` raises `PermissionError` |
| Never re-run B1–B5 or Phase 6 | Package consumed as given |
| Never re-derive palace geometry | Inherited from package |
| Inputs immutable | Hash-verified at ingest and audit |
| Never ask the user questions | None asked |
| Never fabricate brief text or package fields | None fabricated |
| Exclude logo artwork | [[Logo-Boundary]] — `EXCLUDE_ARTWORK` |
| `SUBMISSION/` language purity | Lint gate 2, 0 violations |

### Tree contract

| Tree | Minimum | Delivered |
|---|---|---|
| `SUBMISSION/` | Registry deliverables, pure English | 10 files, lint PASS |
| `ANNOTATED/` | `00_STATUS.md` | 1 file |
| `OPERATOR/` | `COMMENTS.md`, `MAPPINGS.md`, `PATH_RANK.md` | 3 files |
| `LAYER_A/` | `LAYER_A_TECHNICAL_AUDIT.md`, 5 sections in order | 1 file, order verified |
| Root | `MANIFEST.md` | Present |

## Linked

[[Requirements-Matrix]] · [[Logo-Boundary]] · [[Solution-Architecture]] · [[Risk-And-Audit-Log]]
