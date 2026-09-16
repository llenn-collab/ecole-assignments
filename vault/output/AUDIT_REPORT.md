# AUDIT REPORT — Ironclad Post-Mortem & Integrity Auditor
- audited run: `carpathia-qmdj-v5-run-20260915T195319Z-411` · audit time 2026-09-16T01:32:59Z
- skill: PROMPT/SKILLS/Audit/skill.md · scope adaptation: chart-only pipeline (Assignment.pdf/SUBMISSION out of scope by assignment-blind law); Gates 2–4 at full force against `chart_analysis_package.json`

## Final verdict: **PASS**

## Run history
- **Run 1 verdict: VETO** — gate 4 (adversarial omission attack) fired: 8 omissions + 58 harvest-level unjustified leaves (see VETO_LOG.md). Code: BLIND_SPOT.
- Worker response: AUDIT_FIX cycle 2 (PROMPT budget allows 3; cycles used: 2). New claims CLM-033/CLM-034, RES-003 recount (winner 0.85→0.80, margin note updated), package re-rendered (sha256 `4e906b0f47d1c4df…`).
- **Run 2 verdict: PASS.**

## Gate results (run 2)
- Gate 0 input presence: PASS (adapted contract recorded)
- Gate 1 integrity: PASS — source sha256 stable `2f165e078a7c2170…` across boot → remediation → re-audit; package re-hashed after re-render
- Gate 2 traceability: PASS — 0 broken citations across 34 claims + relations + patterns + resolutions (independent resolver, worker wiki not trusted)
- Gate 3 confidence layering: PASS — core-strategy claims minimum confidence 1.0; no sub-0.8 core without operator warning
- Gate 4 omission attack: PASS
  - O1_original_position_audit: REMEDIATED
  - O2_oppression_validated: REMEDIATED
  - O3_tomb_fields_validated: REMEDIATED
  - O4_liuyi_punishment_validated: REMEDIATED
  - O5_star_canon_normalized: REMEDIATED
  - O6_life_stage_interpreted: REMEDIATED
  - O7_harm7_disclosed: REMEDIATED
  - O8_names_validated: REMEDIATED

## Field utilization (the consuming question)
- total leaf fields: **226**
- cited in verdicts/relations/patterns/audits or consumed by named engines: **202**
- justified unused (whitelisted categories only: attribution_provenance, opaque_policy): **24**
- **unjustified unused: 0** 

## Omission findings (run 1 → resolution)
- [HIGH] original_position never validated: branches/star/door/deity inside original_position blocks were stored but never checked against frozen geometry or current palace → correction: execute original_position_parser: branch mapping vs frozen identity, star/door home checks, deity two-plate note, per-palace verdicts
- [MED] special_markers 'Oppression' (palace 8) never validated by the marker engine → correction: validate oppression markers against door_oppressing_palace relation
- [HIGH] tomb field stems never validated: 'Jia Gui', 'Xin Ren', 'Ding Ji Geng', 'Yi Bing Wu' tomb strings stored but stems never checked against tomb-branch geometry → correction: parse each tomb field; validate every stem's tomb branch against in-palace branches; log school variants
- [HIGH] punishment fields never validated: 'Wu (Mao, Zhen 3)', 'Ji (…Kun 2)', 'Geng (…Gen 8)', 'Xin (…Li 9)', 'Ren Gui (…Xun 4)' match classical Liu-Yi punishment palace table (Wu@3, Ji@2, Geng@8, Xin@9, Ren@4, Gui@4) — a deterministic check left unexecuted → correction: validate all six punishment field entries against Wu@3/Ji@2/Geng@8/Xin@9/Ren@4/Gui@4 table; publish per-entry verdicts
- [MED] center lodged star never canonicalized in star system map ('Heaven Qin (lodged in Zhen 3 Palace)' kept as raw key; home/displacement not computed) → correction: canonicalize to Tian Qin with home 5, displacement true, lodging edge retained
- [MED] day stem life-stage evidence unused: chart's own life_stage field names day stem Ren at Kun 2 (Wei/Shen) — the day stem's generative seat evidence never interpreted → correction: interpret day-stem life-stage seat (Kun 2) as typed claim with EXPLICIT field grounding
- [MED] palace 7 harm field 'Ji (Dui 7, You)' absent from palace 7 verdicts — the best-solution winner's friction with the center stem (Ji) never disclosed → correction: add WARN claim citing palaces.dui_7.harm; refresh RES-003 contradiction count and margin
- [LOW] palace 'name' fields never validated against palace keys → correction: validate each name string against resolved canonical palace id

## Integrity evidence
- boot hash: `2f165e078a7c21700e5f1a1f8e44862ddcdd8f04078b733cf9c477dfb9cbcafb`
- re-audit hash: `2f165e078a7c21700e5f1a1f8e44862ddcdd8f04078b733cf9c477dfb9cbcafb` — identical; source untouched through two audit-fix cycles
- package gates re-run: {"archetype_resolution_presence": true, "board_consistency": true, "citation_integrity": true, "coverage_complete": true, "determinism_check": true, "explicit_pattern_priority": true, "leaf_citation_integrity": true, "validate_schema": true}
- red team re-run: PASS

## Residual disclosed limits (not failures)
- `original_position.numbers` remain opaque by spec policy (no invented meaning).
- harm/life_stage strings are stored typed atoms: no stem-harm or 12-stage authority table exists in the spec regime; day-stem occurrences were interpreted (CLM-033); branch-level six-harm relations were computed instead (Chen–Mao trap↔seat, You–Xu channel friction).
- star_strength two-token convention stays flagged SCHEMA_AMBIGUITY; raw tokens preserved, never force-mapped.
- 12 anomalies remain visible in the package (8 opposite-palace label mismatches, explicit pattern conflict, placeholder labels) — none suppressed.