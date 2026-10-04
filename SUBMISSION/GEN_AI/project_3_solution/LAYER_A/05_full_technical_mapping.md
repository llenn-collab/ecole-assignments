# 05 — Full technical mapping

The plain-English layer ends here. What follows is the operator's own tree, appended verbatim so the reasoning can be audited without any of it leaking into the submission.

<!-- OPERATOR-APPENDIX-START -->

## Requirement → deliverable → binding

| Requirement | Level | Status | Deliverable(s) | Bindings |
|---|---|---|---|---|
| `REQ-001` input_assignment_1_research_summary | must | COVERED | 09_research_reference_index.md | BIND-001 |
| `REQ-002` input_insight_list | must | SUBSTITUTED_INPUT_DECLARED | 09_research_reference_index.md | BIND-002 |
| `REQ-003` input_pinterest_mood_board | must | SUBSTITUTED_INPUT_DECLARED | 06_mood_board_index.md | BIND-003 |
| `REQ-004` traceability_requirement | must | COVERED | 04_coherence_check.md | BIND-004 |
| `REQ-005` before_you_start_umbrella | must | COVERED | 00_cover_and_index.md | BIND-005 |
| `REQ-006` what_you_re_producing_three_distinct_briefs_umbrella | must | COVERED | 00_cover_and_index.md | BIND-006 |
| `REQ-007` brief_1_brand_idea_philosophy_core_idea_1_2_sentences | must | COVERED | 01_brief_1_brand_idea_and_philosophy.md | BIND-007 |
| `REQ-008` brief_1_brand_idea_philosophy_philosophy_point_of_view | must | COVERED | 01_brief_1_brand_idea_and_philosophy.md | BIND-008 |
| `REQ-009` brief_1_brand_idea_philosophy_positioning_statement | must | COVERED | 01_brief_1_brand_idea_and_philosophy.md | BIND-009 |
| `REQ-010` brief_1_brand_idea_philosophy_personality_tone_of_voice | must | COVERED | 01_brief_1_brand_idea_and_philosophy.md | BIND-010 |
| `REQ-011` brief_1_brand_idea_philosophy_name_rationale | must | COVERED | 01_brief_1_brand_idea_and_philosophy.md | BIND-011 |
| `REQ-012` brief_1_brand_idea_philosophy_logo_direction_not_the_logo_itself_a_brief_for_it | must | COVERED | 01_brief_1_brand_idea_and_philosophy.md, 06_mood_board_index.md | BIND-012 |
| `REQ-013` brief_2_product_packaging_product_definition | must | COVERED | 02_brief_2_product_and_packaging.md | BIND-013 |
| `REQ-014` brief_2_product_packaging_packaging_direction | must | COVERED | 02_brief_2_product_and_packaging.md, 06_mood_board_index.md | BIND-014 |
| `REQ-015` brief_2_product_packaging_functional_to_emotional_bridge | must | COVERED | 02_brief_2_product_and_packaging.md | BIND-015 |
| `REQ-016` brief_2_product_packaging_shelf_competitive_differentiation | must | COVERED | 02_brief_2_product_and_packaging.md | BIND-016 |
| `REQ-017` brief_3_ad_campaign_creative_brief_campaign_concept_the_big_idea | must | COVERED | 03_brief_3_ad_campaign.md, 05_logline.md | BIND-017 |
| `REQ-018` brief_3_ad_campaign_creative_brief_hero_shot_direction | must | COVERED | 03_brief_3_ad_campaign.md | BIND-018 |
| `REQ-019` brief_3_ad_campaign_creative_brief_stage_environment | must | COVERED | 03_brief_3_ad_campaign.md | BIND-019 |
| `REQ-020` brief_3_ad_campaign_creative_brief_models_casting_direction | must | COVERED | 03_brief_3_ad_campaign.md | BIND-020 |
| `REQ-021` brief_3_ad_campaign_creative_brief_plan_of_action_creative_direction_sequence | must | COVERED | 03_brief_3_ad_campaign.md, 06_mood_board_index.md | BIND-021 |
| `REQ-022` brief_3_ad_campaign_creative_brief_production_requirements | must | COVERED | 03_brief_3_ad_campaign.md, 07_production_and_ai_workflow.md | BIND-022 |
| `REQ-023` brief_3_ad_campaign_creative_brief_umbrella | should | COVERED | 03_brief_3_ad_campaign.md | BIND-023 |
| `REQ-024` coherence_check_do_this_before_submitting_umbrella | must | COVERED | 04_coherence_check.md | BIND-024 |
| `REQ-025` deliverable_submission_umbrella | must | COVERED | 00_cover_and_index.md | BIND-025 |
| `REQ-026` evaluation_criteria_traceability | should | COVERED | 04_coherence_check.md | BIND-026 |
| `REQ-027` evaluation_criteria_specificity | should | COVERED | 03_brief_3_ad_campaign.md | BIND-027 |
| `REQ-028` evaluation_criteria_internal_consistency | should | COVERED | 04_coherence_check.md | BIND-028 |
| `REQ-029` evaluation_criteria_production_realism | should | COVERED | 07_production_and_ai_workflow.md, 08_risks_and_how_they_are_handled.md | BIND-029 |
| `REQ-030` evaluation_criteria_differentiation | should | COVERED | 02_brief_2_product_and_packaging.md | BIND-030 |
| `REQ-031` exclusion_logo_artwork | must_not | SATISFIED_BY_ABSENCE | 01_brief_1_brand_idea_and_philosophy.md | BIND-031 |
| `REQ-032` prohibition_new_audience | must_not | SATISFIED_BY_ABSENCE | 01_brief_1_brand_idea_and_philosophy.md | BIND-032 |
| `REQ-033` prohibition_logo_style | must_not | SATISFIED_BY_ABSENCE | 01_brief_1_brand_idea_and_philosophy.md | BIND-033 |
| `REQ-034` prohibition_untraced_decisions | must_not | SATISFIED_BY_ABSENCE | 04_coherence_check.md | BIND-034 |

## Adapter status and evidence tallies

- Package adapter: **MAPPED**; evidence atoms: **87**; package seal self-consistent (verified by the adapter)
- Evidence dispositions: deferred=37, corroborated=13, used=37
- Gates: hard_constraint_gate=PASS, coverage_gate=PASS, unsupported_format_gate=PASS, logo_gate=PASS, tie_state=PASS, stale_dependency=PASS, citation_leaf_integrity=PASS, evidence_consumption=PASS, no_raw_chart_read=PASS, fallback_transparency=PASS, producer_obligation=PASS, layer_a_contract=PASS, requirement_ledger_closure=PASS
- Risks translated: 8; vetoed candidates: 1
- Call budget used: 57 of 80

## Operator tree, verbatim with hashes

- `ANNOTATED/01_brief_1_brand_idea_and_philosophy.annotated.md` — `eca69d7acc5fd4ae…`
- `ANNOTATED/02_brief_2_product_and_packaging.annotated.md` — `a5b3ec668739cc0d…`
- `ANNOTATED/03_brief_3_ad_campaign.annotated.md` — `e4f75e8fef7d5f23…`
- `ANNOTATED/position_in_wider_answer.md` — `a3c5170e3505a0ab…`
- `ANNOTATED/response_map.md` — `94faee7f978dbeda…`
- `LAYER_A/01_executive_reading.md` — `2b141e69f13dcda9…`
- `LAYER_A/02_walkthrough.md` — `83d7aa93464a449b…`
- `LAYER_A/03_candidates_and_selection.md` — `a3390bca65bd93fb…`
- `LAYER_A/04_confidence_and_residual_risk.md` — `cbc5748a942a5df8…`
- `OPERATOR/ADAPTER/adapter_map.json` — `79bf0f63944dc0e3…`
- `OPERATOR/ADAPTER/adapter_report.md` — `7b0128917180a565…`
- `OPERATOR/ANOMALY_LOG.md` — `914ed95976b4c02b…`
- `OPERATOR/CALL_LOG.jsonl` — `d3720269e2a451ef…`
- `OPERATOR/GAP_REGISTER.md` — `dade6b30a28fbc7c…`
- `OPERATOR/HARD_CONSTRAINT_VETO.md` — `603bd66e13223879…`
- `OPERATOR/SOURCE_HASHES.json` — `830bdbb461158fe8…`
- `OPERATOR/STATE/logs/ADAPTER/read_log.json` — `f4e494719d5bf6ee…`
- `OPERATOR/STATE/logs/ADAPTER/write_log.json` — `f36d426d2dd3b809…`
- `OPERATOR/STATE/logs/FINALIZE/read_log.json` — `8b5c4922a04a4c63…`
- `OPERATOR/STATE/logs/FINALIZE/write_log.json` — `bd5de91af940dc59…`
- `OPERATOR/STATE/logs/INGEST/read_log.json` — `861f4592ea0aac70…`
- `OPERATOR/STATE/logs/INGEST/write_log.json` — `24a708c4be3a0988…`
- `OPERATOR/STATE/logs/RENDER/read_log.json` — `aadf1a567b6a8281…`
- `OPERATOR/STATE/logs/RENDER/write_log.json` — `78c88c0686785aa4…`
- `OPERATOR/STATE/logs/SOLUTION/read_log.json` — `8c8a005b5e457b84…`
- `OPERATOR/STATE/logs/SOLUTION/write_log.json` — `7ca63f77340d223b…`
- `OPERATOR/STATE/machine_state.json` — `16de655be367e806…`
- `OPERATOR/STATE/pdf_ingest.json` — `62ee96cea59ea362…`
- `OPERATOR/STATE/second_tally.md` — `c383f41f414cf912…`
- `OPERATOR/VERIFICATION/gates.json` — `243cae26a1a31112…`
- `OPERATOR/VERIFICATION/layer_a_contract.json` — `5f31b933e1db08ee…`
- `OPERATOR/VERIFICATION/lint_report.md` — `49eb251c474e1a32…`
- `OPERATOR/VERIFICATION/proof.md` — `a4564ce5e47f91f1…`
- `OPERATOR/VERIFICATION/red_team.json` — `751ea463dd8b4fa4…`
- `OPERATOR/VERIFICATION/red_team.md` — `e6dd9f596478d5c8…`
- `README.md` — `217ee77b70ffb09b…`
- `SUBMISSION/00_cover_and_index.md` — `d4d072bfa1327913…`
- `SUBMISSION/01_brief_1_brand_idea_and_philosophy.md` — `99fa1599ae69925c…`
- `SUBMISSION/02_brief_2_product_and_packaging.md` — `0a69619943db2bf0…`
- `SUBMISSION/03_brief_3_ad_campaign.md` — `bc6a4dd66f1b482f…`
- `SUBMISSION/04_coherence_check.md` — `d753bee1a71ad0f9…`
- `SUBMISSION/05_logline.md` — `75f3f21bbf0bc894…`
- `SUBMISSION/06_mood_board_index.md` — `8e4af8fb73821c16…`
- `SUBMISSION/07_production_and_ai_workflow.md` — `aad6209e3a6bee4a…`
- `SUBMISSION/08_risks_and_how_they_are_handled.md` — `d1c82b7c33bb0534…`
- `SUBMISSION/09_research_reference_index.md` — `92e9ff12cc52842f…`
- `config/scoring.yaml` — `3584e4d894aeaa6e…`
- `raw/assignment_1_research.yaml` — `88a687279df66203…`
- `raw/assignment_brief.yaml` — `5f641d01f096e6a1…`
- `tools/adapter.py` — `037eedb12bd39162…`
- `tools/finalize.py` — `e365713c2dd451da…`
- `tools/guarded.py` — `c25a12ca4f3d7842…`
- `tools/render.py` — `7df915d3e85614a8…`
- `tools/requirements.py` — `80e6d8ef01e3afeb…`
- `tools/solve.py` — `3baf12316e351acc…`
- `work/adapted_package_view.json` — `ea5296f17a2fedef…`
- `work/bindings.json` — `be47f1b7b19df75e…`
- `work/bindings_ledger.json` — `22c32b4b9c8dcba5…`
- `work/candidates_scored.json` — `b2f88e7778c1128f…`
- `work/cmap.jsonl` — `6567b44808f2fcf4…`
- `work/evidence_ledger.json` — `2c28b7d0a1640649…`
- `work/gates.json` — `2d74de54330acb09…`
- `work/hidden_problems_resolved.json` — `ae3d68a8edb8100c…`
- `work/requirement_ledger.json` — `2fc2045c9ef0b9b7…`
- `work/requirements.json` — `2b0592555469dd41…`
- `work/research_index.json` — `61082a61494e3c34…`
- `LAYER_A/05_full_technical_mapping.md` — self; excluded from the appendix's own hash set by construction (the manifest carries its digest)

The appendix covers every artefact written before it; the verification proof and the manifest are written afterwards and carry their own digests. Every hash above is recomputed after writing, and the appendix is valid only if it still matches at the end of the run.
