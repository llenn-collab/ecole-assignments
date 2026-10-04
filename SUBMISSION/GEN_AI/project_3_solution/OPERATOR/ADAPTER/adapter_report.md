# Adapter report — CAP-03 (mode: strict)

Producer detected: **chart_analyser_v7**  
adapter_status: **MAPPED** · evidence preserved: 87 atoms · no_evidence_loss: True · no_forbidden_mutation: True

## Field origins

| contract slot | origin |
|---|---|
| `evidence_registry` | MAPPED < 05 + 08 + 11 (87 atoms aggregated) |
| `palaces` | MAPPED < 04_palace_identity_resolution + 06_palace_coverage_matrix |
| `systems` | EXPLICITLY_EMPTY — 05_structure_evidence contains no `systems` blocks (the analyser v7 package carries no systems register); recorded rather than silently absent (producer_obligation) |
| `relations` | MAPPED < 05_structure_evidence R atoms |
| `patterns` | MAPPED < 07_pattern_state_registry |
| `origin_sets` | MAPPED < 03_chart_overview root_register + board_reference |
| `focus_candidates` | MAPPED < 10_solution_hypotheses + 09_case_alignment |
| `anomalies` | MAPPED < 03 + 12 + 14 + 15 |
| `absence_evidence` | MAPPED < 06 class_level_closure + 07 null_register |
| `exclusion_evidence` | MAPPED < package evidence ledger (work/ledger.json), recorded via seal |
| `coverage_accounting` | MAPPED < 06_palace_coverage_matrix + 14_gap_report |
| `schema_adaptation_metadata` | MAPPED < 16_provenance_appendix + 05 registers |
| `solution_seed` | MAPPED < 10_solution_hypotheses + 13 + 11 + 14 |

## Producer obligation check

| slot | present? | how |
|---|---|---|
| `evidence_registry` | yes | MAPPED < 05 + 08 + 11 (87 atoms aggregated) |
| `palaces` | yes | MAPPED < 04_palace_identity_resolution + 06_palace_coverage_matrix |
| `systems` | explicitly empty with reason | EXPLICITLY_EMPTY — 05_structure_evidence contains no `systems` blocks (the analyser v7 package carries no systems register); recorded rather than silently absent (producer_obligation) |
| `relations` | yes | MAPPED < 05_structure_evidence R atoms |
| `patterns` | yes | MAPPED < 07_pattern_state_registry |
| `origin_sets` | yes | MAPPED < 03_chart_overview root_register + board_reference |
| `focus_candidates` | yes | MAPPED < 10_solution_hypotheses + 09_case_alignment |
| `anomalies` | yes | MAPPED < 03 + 12 + 14 + 15 |
| `absence_evidence` | yes | MAPPED < 06 class_level_closure + 07 null_register |
| `exclusion_evidence` | yes | MAPPED < package evidence ledger (work/ledger.json), recorded via seal |
| `coverage_accounting` | yes | MAPPED < 06_palace_coverage_matrix + 14_gap_report |
| `schema_adaptation_metadata` | yes | MAPPED < 16_provenance_appendix + 05 registers |
| `solution_seed` | yes | MAPPED < 10_solution_hypotheses + 13 + 11 + 14 |

## Hash verification

- seal artifacts checked: 58
- seal self-consistent: **True**
- source evidence sha256: `20dc73a91a46c4dca78cca6fc9bc7520b91c7b16d9edb18fb93f76d1e8360a15`
- interpretation protocol hash: `4cbd13bd8ecbbf85eaa18e50bcb15f6cd82992a2c348472306b4547a025614e6`
- evidence/scoring rubric hash: `f405d00461a6cd434d6cb1546c2207092de0e054b752149bd24cdf523ae915f2`

## Adapter declarations

- The adapted view is the single whole-package view (law 28). No phase re-reads the package after this file exists.
- Substitutions are recorded MAPPED so a CLEAN native package and a patched one stay distinguishable.
- No evidence was created, scored, discarded or mutated; `systems` is empty because the producer does not emit it.
