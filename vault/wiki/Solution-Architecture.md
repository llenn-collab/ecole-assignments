---
id: "solution-architecture"
type: "engine"
state: "SYNTHESIZE"
updated: "2026-09-16T03:00:06Z"
---

# Solution Architecture (solver v4.0.0 run)

## Pipeline FSM
INIT → PACKAGE_VALIDATE → PDF_INGEST → P7_SLOT_BIND → SOLUTION_ENGINE → SYNTHESIZE → RENDER_OUTPUT → HALT

## Components
- `vault/_engine2/common2.py` — logged_read (asserts no raw-chart path), sha256, state dumps, pkg_resolve
- `s1_init_ingest.py` — INIT, package validation (schema+hashes, deviations DEV-001/002), brief ingest (24 reqs)
- `s2_slotbind_engine.py` — slot binding + re-scoring under solver rubric (weights .35/.25/.20/.10/.10; tiers 1.0/.6/.3)
- `s3_synthesize_outputs.py` — deck + ANNOTATED + OPERATOR + LAYER_A authoring
- `s3b_wiki_redteam.py` — red team (3 findings fixed) + wiki corpus (this file)
- `s4_render.py` — lint, gates, manifest, HALT

## Binding
| slot | source of truth | output |
|---|---|---|
| my_answers | solution_seed.answers + RES-001 | deck Slides 1–6, Brand test |
| hidden_problems | solution_seed.hidden_problems + RES-002 | deck guards (Slides 8/10/12), [[Hidden-Problems]] |
| best_solution | solution_seed.best_solution_candidates + RES-003 | deck Slides 8–12 |

## Gates (checked at RENDER_OUTPUT)
package_schema, package_integrity, no_qmdj_read, lint_terms(0), citation_integrity, coverage(0 uncovered),
archetype_resolution_presence, layer_a_contract, red_team_applied
