# MANIFEST — CARPATHIA Assignment Solver run

**Run id:** `CARPATHIA-P3-CONTENT-STRATEGY-001` · **Charter:** Assignment Solver v7.0.0  
**Runtime:** TOOLS_PRESENT (shell + file tools; pypdf, python-pptx, reportlab, PyMuPDF available)  
**Generated:** 2026-10-04 18:47 UTC  
**Terminal state:** `HALT` — every FSM state entered, coverage gate passed, no fallback mode.

---

## 1. Inputs (frozen, hashed)

| Input | Role | Bytes | SHA-256 |
|---|---|---|---|
| `project_3.yaml` | assignment_brief | 10478 | `1002fdad1907adceff87c6b1d3507e4eb3a3827a1e729d86054f937d4f26a423` |
| `qmdj_analysis_package.json` | chart_analysis_package | 309543 | `011d3b5fa4d168d2c0cd7ddf5b568e55636dc70c2747ff76cdfcb34d534df3b5` |
| `project_1.pdf` | prior_submission_part1 | 2952805 | `472329e5c512573a0e5f22f4a526763b68e660c6608a897d357f6b7dcd9d1da1` |
| `part1_facts.json` | part1_extracted_facts | 8500 | `9786265243601a5b7fc0c83df85600ecabc37e737350c0935bb1c64c76fd883f` |

**Law 8 (raw-chart quarantine).** The solver never read `QMDJ/MARKETING/project_3.json`. The only
chart-derived input was the adapted package view built by `CAP-03` from
`QMDJ_ANALYST_RUN/package/qmdj_analysis_package.json`: `adapter_status=MAPPED`,
`preserved_evidence_count=115`, `unmapped_fields=[]`.

## 2. Capability ledger

| CAP | Product | State |
|---|---|---|
| CAP-01 | `state/fingerprint.json` | 51 |
| CAP-02 | `state/package_normalize.json` | 18 |
| CAP-03 | `state/adapted_package_view.json` | 27 |
| CAP-15 | `state/brief_decompose.json` | 59 |
| CAP-04 | `state/requirement_resolve.json` | 230 |
| CAP-06 | `state/binding_manifest.json` | 20 |
| CAP-16 | `state/requirement_map.json` | 35 |
| CAP-07 | `state/cards.json` | 30 |
| CAP-09 | `state/ledger_reconcile.json` | 60 |
| CAP-10 | `state/score_card.json` | 133 |
| CAP-18 | `state/hidden_translate.json` | 22 |
| CAP-12 | `state/dependency_check.json` | 12 |
| CAP-17 | `state/conflict_check.json` | 179 |
| CAP-11 | `state/lint_scan.json` | 14 |
| CAP-14 | `state/self_audit.json` | 33 |
| CAP-13 | `state/manifest_build.json` | 62 |

**Capability calls used:** 16 of a maximum 80 · **Anomalies:** none.
**Package mutation:** none (law 3) · **package non-scalar absences recorded:** 267.

## 3. Requirement coverage — every facet carries an alignment row

Zeros are shown, not omitted. `DIRECT` = the facet is bound to evidence that speaks to it; `INDIRECT` =
supported through a parent artefact; `NO_CHART_SUPPORT` = outside what the evidence can speak to;
`CONTRADICTS_KNOWN` = evidence contradicts a stated known fact.

| Requirement | Level | Facet (from the brief) | CMAP tag | Terminal state | Anchor |
|---|---|---|---|---|---|
| REQ-001 | must | Individual assignment; Presentation - PPT/PDF/Google sli… | DIRECT | RESOLVED | `assignment.format + assignment.submission` |
| REQ-002 | may | recommended_length: No recommended length of slides, but… | NO_CHART_SUPPORT | RESOLVED | `assignment.recommended_length` |
| REQ-003 | must | Using the strategic foundation created in Assignment 1, … | DIRECT | RESOLVED | `assignment.assignment_objective` |
| REQ-004 | must | Content Marketing Objective. What does content need to a… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 1]` |
| REQ-005 | must | Brand Story & Communication. Define how the brand should… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 2]` |
| REQ-006 | must | Content Pillars. Develop 3 - 5 content pillars for the b… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 3]` |
| REQ-007 | must | Platform Strategy. {"\"Choose 2 - 3 primary social platf… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 4]` |
| REQ-008 | must | One Idea, Different Platforms. Choose one content idea/c… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 5]` |
| REQ-009 | must | Content Concepts. Develop 5 - 6 actual content ideas. / … | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 6]` |
| REQ-010 | must | Hero Content / Campaign Idea. Develop one larger social/… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 7]` |
| REQ-011 | must | Community & Engagement Strategy. How will your brand tur… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 8]` |
| REQ-012 | must | Influencer / Creator Strategy. {"\"Define": "Who should … | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 9]` |
| REQ-013 | must | Two-Week Content Calendar. {"\"Create a 2 week content p… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 10]` |
| REQ-014 | must | Measurement & Success. Students define 5 - 7 metrics the… | DIRECT | RESOLVED | `assignment.suggested_slide_structure[slide 11]` |
| REQ-015 | must | 1. Content marketing objective(s); 2. Brand message + to… | INDIRECT | RESOLVED | `assignment.assignment_checklist` |
| REQ-016 | should | {"\"1. Strategic relevance": "Does the content make sens… | NO_CHART_SUPPORT | RESOLVED | `assignment.evaluation_criteria` |
| REQ-017 | must | 5th October 2026… | NO_CHART_SUPPORT | RESOLVED | `assignment.submission_date` |

**CMAP tally:** DIRECT 13 · INDIRECT 1 · **NO_CHART_SUPPORT 3** · **CONTRADICTS_KNOWN 0**.
**Requirement closure:** must 15 = satisfied 15 + uncovered 0 + blocked 0; should 1 satisfied; must_not 0 as satisfied-by-absence
**Unresolved requirements:** none
**No-compliant-candidate check:** a compliant winner exists (S-01). The two non-compliant candidates were
vetoed by hard constraints and are recorded with reasons, not silently dropped.

### Coverage gate

| Gate check | Result |
|---|---|
| Every requirement has a terminal state | PASS |
| Evidence ledger balances | PASS — 115 = 42 used + 8 corroborated + 65 deferred |
| No invalid or dangling citations | PASS — 0 unresolved across 17 rows |
| **Gate verdict** | **PASS — nothing left uncovered or blocked** |

## 4. Output trees

| Tree | Contents | Reader |
|---|---|---|
| `SUBMISSION/` | the deliverable: deck (PPTX + PDF), long-form strategy, calendar CSV, measurement CSV, creator dossier, copy pack, two visual mock-ups | marker / client |
| `ANNOTATED/` | plain-English commentary — what the strategy bets on, what it refuses, and where it could be wrong | non-specialist |
| `LAYER_A/` | executive reading, walkthrough, candidate comparison, confidence and residual risk, machine-readable products, technical appendix | analyst |
| `OPERATOR/` | binding summary, evidence→content map, path rank, evidence consumption, veto record, score sources | operator |

## 5. Artefact register (SHA-256)

*(Registers every artefact present at manifest time; the manifest cannot hash itself.)*

| Path | Bytes | SHA-256 |
|---|---|---|
| `ANNOTATED/situation_commentary.md` | 4951 | `12e51abe805aa4d3992af7b4bfc23ff4824444a5b28646b3d9714cd7fa0f8180` |
| `LAYER_A/00_executive_reading.md` | 2657 | `d7ce9ad619e7457ad2df6fca0e238a73d8d4f8a761291781d56fbd054dd486f8` |
| `LAYER_A/01_walkthrough.md` | 2861 | `c1c54693afd2229de0c92065cf1c29a440111163a1e384bf675115a90018bef0` |
| `LAYER_A/02_candidates_and_selection.md` | 2730 | `d4b0cce591c08380f65a9f33287f0e1dc4f5155f7fd5a24b518c8b6b18a8cae5` |
| `LAYER_A/03_confidence_and_residual_risk.md` | 3064 | `e87bfdcd4ca88f5aa03c3fb9c802f42be535a597911102e11d9a3a996340f638` |
| `LAYER_A/04_machine_readable/adapted_package_view.json` | 155696 | `0db4d4011737eef5b4a6ea108ec94bfe10028e5844dc7abffe56b76f4c6f4dd4` |
| `LAYER_A/04_machine_readable/binding_manifest.json` | 7430 | `5b7b184ce779e40b0f3526f68b76ef8fb79785a39e4cc1340d2721c2b1eea7bd` |
| `LAYER_A/04_machine_readable/brief_decompose.json` | 8580 | `46f53538d74063266de4b5f2d1679bb78f6d75493fcb23857b1d8cce7b7e4560` |
| `LAYER_A/04_machine_readable/brief_facts.json` | 3317 | `74d3ccf8200a6d361f0e809f438fba8e616d6622ac877acbcf3254c7a2345c44` |
| `LAYER_A/04_machine_readable/cards.json` | 18011 | `8cbda3b87a9b3a92aa6aeeb460b712c0559b58135e84be4d05dc2292ab2799bc` |
| `LAYER_A/04_machine_readable/conflict_check.json` | 3401 | `2e4ace13ad84b1e6237ea5ed58b3eb2f259df569fcd38072f40743730ebe5a54` |
| `LAYER_A/04_machine_readable/dependency_check.json` | 549 | `d616d84cf7fe1636a1d4c5c8176b70777e656fcae85ea2511685e107f305b6d7` |
| `LAYER_A/04_machine_readable/evidence_ledger.json` | 3319 | `5fa1d4a4ac6a532112103f8b61b985ed17595422e44ae64fc6d4be5af7ad3c10` |
| `LAYER_A/04_machine_readable/fingerprint.json` | 969 | `2cfadea030f0bc102ed693a4e92aca5e93add07c4b185509e6472d02b97b1b6a` |
| `LAYER_A/04_machine_readable/hidden_problems.json` | 3929 | `32921564df9aa1b90a42941db7bd6c5c8b7d0aa96d00e792becbd3cfc271c492` |
| `LAYER_A/04_machine_readable/ledger_reconcile.json` | 1053 | `888c68db831e6c577c0f90058e477bacc5f7b32b3fb10b164a6d53b3bec19b7c` |
| `LAYER_A/04_machine_readable/lint_scan.json` | 284 | `e5cb51f8cd70fb007c36cb1841a313f9ed5bf45d73b391d9347634eb99c62caf` |
| `LAYER_A/04_machine_readable/package_normalize.json` | 29148 | `16e44748e4a197efe8e3a88ec287977f4aefa39d57105b454073b47376acf750` |
| `LAYER_A/04_machine_readable/part1_facts.json` | 8500 | `9786265243601a5b7fc0c83df85600ecabc37e737350c0935bb1c64c76fd883f` |
| `LAYER_A/04_machine_readable/requirement_map.json` | 4548 | `166f3848ceaec761fb81e5a7ab7f7fd29d8dfb2b488abc1bb297b29489d8db8d` |
| `LAYER_A/04_machine_readable/requirement_resolve.json` | 3360 | `0aabb880d78f60dcb5aa58b6f233470c02c07ff8b9c72fd0566f20d19e45e8d7` |
| `LAYER_A/04_machine_readable/score_card.json` | 3174 | `310f1bce712e93722326946a8d32f88fb740f15707d5fa241109c56cf102b1f9` |
| `LAYER_A/04_machine_readable/self_audit.json` | 627 | `0693dfd50b906b9fe556cc34c8779ecd7edf90296a15bafbf181a362e93c78db` |
| `LAYER_A/04_machine_readable/solution.json` | 22915 | `890a8a7b28496762553377f5666ade1a7af6abbf0a272c91f3e8f02b50592bf0` |
| `LAYER_A/04_machine_readable/solution_seed.json` | 2109 | `86378a8e34b17881389892d6a30ccb93a4fff9347c6a99a9a50cd38f25461c48` |
| `LAYER_A/05_technical_appendix_chart_language.md` | 3508 | `7fc86bfeb42793adbfaa87a7eb854a9b2c88c3b2756caa321e12758775eb0fa3` |
| `OPERATOR/COMMENTS.md` | 2860 | `a1842fbacdf4273a21b27b73ff2711cbfadca221a6c8d52a5d18075ae4a3e404` |
| `OPERATOR/EVIDENCE_CONSUMPTION.md` | 1642 | `0140a76574b8035d5844a070d98a6be556d4441d36f9fe9834ed5327bd9f1009` |
| `OPERATOR/HARD_CONSTRAINT_VETO.md` | 1681 | `d9c99309b27bd637afdd4233f39ea2288fc54b2e69a763916b90e5a5e9712e2a` |
| `OPERATOR/MAPPINGS.md` | 2111 | `d1a0a1c747003152683890beaf1581a2256b56acdaf6b73c2cedbdc685fd41dd` |
| `OPERATOR/PATH_RANK.md` | 1269 | `80cb74c8d428c61cfcc4140600fb9d2fc2a636e4efda032c24aed680f1cb8179` |
| `OPERATOR/SCORE_SOURCES.md` | 727 | `c39394f83352256f0e9f651e9d22f17d65d57aa85813d5f2f8bb295aeef72c29` |
| `SUBMISSION/00_off_hours_content_strategy.md` | 29729 | `f51ae520887f44849ebdc14f3d56665b2deaf6ab4f2fcc4239485e652c4d4725` |
| `SUBMISSION/01_two_week_calendar.csv` | 1267 | `b6132fc13648e47b5f4022f4bd3aa2a9aa07073fd8edf3061a448d80198d2723` |
| `SUBMISSION/02_measurement_framework.csv` | 954 | `6c11d455138df0f01171346490199cbdb168aa442924823bbc570e6d9e6948f7` |
| `SUBMISSION/03_creator_dossier.md` | 7276 | `947fb190176f964c8697e6f0d933abfa49a2d9cd3f417d30f4227ad4c166a029` |
| `SUBMISSION/04_copy_pack.md` | 3934 | `d3affa407e93985b2f2f1eda945b29bf3d4b5ea3cc39be5348a20f814b45abc6` |
| `SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pdf` | 3307230 | `395d3c0ad468e2c17c05c9fa071540a05ee50335379eb58c165da1ca093aa584` |
| `SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pptx` | 2704006 | `9130042014ec5fa54ebc3be045eb33fc43d4e1ffc5725186cd9b99e84d84fa92` |
| `SUBMISSION/assets/mockup_1_carousel_cover.png` | 1107402 | `07721161dd3de7b0df21b6f30d6f183a5580356d275a4fb8cbb712cd391922df` |
| `SUBMISSION/assets/mockup_2_reel_storyboard.png` | 1540216 | `7583462c19a1d4c7c20d88ef5738389371a5f4dda2137c66a1e5b77d6a27e251` |
| `tools/build_deck.py` | 26856 | `e11723b5843a6a6f9596ff85a19f7e276ed0bc01379a76935fae50d2a915e6d2` |
| `tools/mk_manifest.py` | 10767 | `d7b1e2cedac6d1f206d566e63d5a6d7a6e6e9c7cae62bf58dad66347245a5d99` |
| `tools/run_stage1.sh` | 1508 | `a32977da2f11556a398630521f8c34acbc48e261072f93a5d5005f5e09129685` |
| `tools/run_stage2.sh` | 1028 | `0304b3460352c6bfe905226924905712fd23fafab4ba1f1780e747ffc05eb3cf` |
| `tools/scap.py` | 37201 | `addf2ae02773a7a6035b54827c63bbf9426a111c5405af98b7036b32dd2d37f1` |
| `tools/style_lint.py` | 4575 | `cc53eb4e4428c5093e8d6a8463fe2eb532b110905730c0f9ae524243e854b191` |

## 6. Guards and stamps

| Guard | Result |
|---|---|
| CAP-11 regime lint | **PASS** — 6 text files + 2 shipped binaries scanned; 0 lexical, 0 semantic violations |
| Lint stamp | `EMULATED_LINT` |
| CAP-14 self-audit | **9/9 checks pass**, 0 open items, 1 not applicable (run is not in fallback mode) |
| CAP-12 dependency check | PASS — stale: none |
| CAP-17 conflict check | 2 conflicts; uncertainties resolved: V-009←UNK02 |
| CAP-10 scoring | `TIER0_TOOL_CAP-10/v1` · tie state `RESOLVED` · winner `S-01` |
| Register control | no chart terminology or metaphysical framing anywhere in the submission (appendix and operator tree excluded by scope) |
| Style profile (`PROMPT/SKILLS/human-writer.md`) | **PASS** - 0 hits across 7 shipped artefacts; rules: no em dash, no semicolon, no asterisk, no hashtag, no banned vocabulary |

## 7. Fallback flag

| Flag | Value |
|---|---|
| `fallback_mode` | **OFF** |
| `fallback_reason` | — (no degraded producer; the brief is machine-readable and the adapter mapped fully) |
| `fallback_conclusion` | none emitted |
| `stale_products` | none |

The brief's ingestion completed with `COMPLETE`; all required sections resolved; the ledger balances and the package
view mapped without loss. Nothing was degraded, so nothing was softened.

## 8. Gap report

| Gap | Where | Handling |
|---|---|---|
| Two marker families are `UNRESOLVED` upstream (void markers; the horse-star relation) | analyst package §14 | Not needed by any required section; disclosed in the technical appendix; **no assertion made** |
| One region carries no gate or deity marker | analyst package §04/§06 | Disclosed; the submission asserts nothing on that facet |
| Facet coverage is `PARTIAL` (stems/doors/deities 8/9; hosted stems 1/9) | analyst package §06 | Disclosed; the submission's claims rest on fully resolved regions |
| Creator category conflicts and audience geography | live-web verification | Recorded as three pre-activation checks; the filters, not the names, are the recommendation |
| A leader/challenger posture is available and deliberately declined | solution evidence | Named as a decision with its own cost in the annotated risk table, not as an omission |

*The solver's own gap list is empty: no requirement is uncovered, blocked, or carried by a soft-cascade reference.*

## 9. Deliverable formats

| Format | File | Note |
|---|---|---|
| PPTX | `SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pptx` | 15 slides, 16:9, both mock-ups embedded |
| PDF | `SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pdf` | 15 pages, same content as the PPTX |
| Markdown | `SUBMISSION/00_off_hours_content_strategy.md` | long-form source of record for the deck |
| CSV | `SUBMISSION/01_two_week_calendar.csv`, `SUBMISSION/02_measurement_framework.csv` | calendar and measurement framework as data |

## 10. Reproduce

```bash
bash    SUBMISSION/MARKETING/PROJECT_3/SOLVER_RUN/tools/run_stage1.sh    # INIT → SOLUTION_ENGINE
python3 SUBMISSION/MARKETING/PROJECT_3/SOLVER_RUN/tools/build_deck.py  # PPTX + PDF deck
bash    SUBMISSION/MARKETING/PROJECT_3/SOLVER_RUN/tools/run_stage2.sh    # guards + manifest
```

## 11. Known limitations of this run

1. **Ranking margin is narrow** (0.8407 vs 0.8163). Stated in the deck; the runner-up is recorded as a legitimate substitution.
2. **Creator reach data is neither used nor verified**; selection is filter-driven and category conflicts remain unchecked.
3. **Content metric targets are directional** — the numeric bar is inherited from Assignment 1's SMART objectives.
4. **Weekday assignment in the calendar is an operational convention**, not an evidenced finding.
5. **Two evidence atoms contradict the winning candidate** and are surfaced in the annotated risk table rather than suppressed.
