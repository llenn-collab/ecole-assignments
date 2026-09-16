# LAYER_A — Technical Audit (package → strategy binding)

## executive_reading
The diligence package says, in plain words: the **answer** rests on a single, over-determined seat — several
independent selectors (the daily self-trace, the official duty proxy, the dividing authority) all name the same
place, with no competing seat; its constraints are timing (a not-yet window) and intensity, never location.
The **hidden problems** are five: an over-elaborate glittering mission that cannot execute cleanly; a showcase
surface whose payoff window is locked for now; a grinding groundwork track; an open door onto obscurity;
and stored value that decays without a rhythm. The **best way forward** is the one strong, unafflicted seat:
consolidate and run procedurally inside institutions, now (in-period), with alliances courted backstage for
later; two attractive channels are rejected because their windows are locked rather than because they are bad.
The solver translated exactly this posture into the deck: understated launch, retention-first sequencing,
partnerships phase two, mass awareness last. Nothing in the deck contradicts the package; several slide
choices exist *only* because the package demanded them.

## walkthrough
1. INIT — froze run context, copied package read-only to `raw/package/`, initialised solver machine (no reuse of chart-run machine).
2. PACKAGE_VALIDATE — schema keys (with rename DEV-002), semver version 5.0.0, source hash
   2f165e078a7c2170… vs boot MANIFEST: match; protocol/rubric hashes vs ACTUAL generator
   (v5.0.0): match; vs solver-embedded v4 reference: skew logged as DEV-001, PASS_WITH_DEVIATION.
3. PDF_INGEST — brief read once (322 lines); 24 requirement rows enumerated; deliverable registry: 1 real output
   (+1 excluded-logo boundary); rubric guess inferred from the single marking note; question types classified.
4. P7_SLOT_BIND — question types bound to solver slots: identity & positioning → my_answers; risk anticipation &
   what-not-to-do → hidden_problems; strategy/channel-choice & timing → best_solution.
5. SOLUTION_ENGINE — package `solution_seed` (chart-derived only, 'not yet requirement-bound') re-scored under
   solver rubric v1.0.0; requirement_fit composed (coverage .40, hard-compliance .40, audience-tone .20);
   winner re-selected with margin 0.1167; tie-break available but unused; text budgets enforced per slot.
6. SYNTHESIZE — this document, the deck, operator files, and wiki corpus authored; red team run.
7. RENDER_OUTPUT — lint + gates + manifest (see MANIFEST.md for final verification table).

## candidates_and_selection
### best_solution candidates (RES-003, re-scored)
| archetype | solver_score | decision |
|---|---|---|
| BEST-dui-7-earthly-escape-channel | 0.8647 | WINNER — retention/consolidation spine |
| BEST-qian-6-harmony-help-channel | 0.748 | RUNNER — phase-2 alliances |
| BEST-li-9-salary-channel | 0.55 | REJECTED — void-locked payoff window |
| BEST-kun-2-open-gate | 0.565 | REJECTED — opens onto day-void with entombed lead, obscurity |

Winner carries the package caveat (White-Tiger severity; harm on the seat): mitigations = compliance-clean
claims discipline + procedural operation, both visible as deck decisions (Slides 8/10 non-priorities, Slide 12.2).

### hidden problems (RES-002) — all five adopted
| code | archetype | solver_score | deck mitigation |
|---|---|---|---|
| HID-1 HYPE_LAUNCH_TRAP | HID-palace-4-death-duty-tomb-cluster | 0.8667 | R07 |
| HID-2 VOID_SHOWCASE | HID-palace-9-void-showpiece | 0.7889 | R21 |
| HID-3 GROUNDWORK_GRIND | HID-palace-1-great-barrier | 0.7611 | R16 |
| HID-4 MARKETPLACE_OBSCURITY | HID-palace-2-void-open-jia-tomb | 0.7611 | R18 |
| HID-5 CONTENT_BACKLOG | HID-palace-8-stalled-storage | 0.7611 | R21 |

### my_answers (RES-001) — singleton, adopted as-is
Winner ANS-seats-in-zhen-3, solver_score 0.8667; package tie_note: "not tied;
singleton resolution". Deck expression: single-category single-claim brand (Slides 1–6), muted launch posture.

## confidence_and_residual_risk
| item | confidence | basis |
|---|---|---|
| answers slot (brand formulation) | 0.90 | singleton EXPLICIT grounding; package context notes |
| best_solution winner | 0.80 | package final winner confidence after harm re-audit (CLM-034) |
| hidden HID-1 | 0.85 | strongest avoid-cluster (support 9, corroboration 1.0) |
| hidden HID-2 | 0.75 | EXPLICIT but window-shaped (fills later) |
| hidden HID-3/4/5 | 0.65 | tie-group triple; equal weighting kept |

**Residual risk:** (a) score compression under solver rubric (fit term adds +0.095 to all grounded rows —
ranking preserved by design); (b) persona/price figures are illustrative, flagged in OPERATOR; (c) requirement_fit
sub-scores are analyst-set (no marker rubric PDF exists — rubric_guess documented); (d) DEV-001 version-skew
accepted as registry lag; if the canonical v4 package ever surfaces, re-validate hashes and rerun (est. effort: re-run s1 forward).

## full_technical_mapping
### Rubric record
- solver rubric v1.0.0 hash `sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4`; weights & tiers as in walkthrough.
- package-side rubric hash `sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5` (generator v5.0.0) — provenance chain DEV-001.
- requirement_fit = .40·coverage + .40·hard_compliance + .20·audience_tone; values per slot in PATH_RANK.

### Claim ledger (ids referenced by seed rows)
- CLM-001 (answers)
- CLM-002 (answers)
- CLM-015 (hidden, HID-1 HYPE_LAUNCH_TRAP)
- CLM-016 (hidden, HID-1 HYPE_LAUNCH_TRAP)
- CLM-029 (hidden, HID-2 VOID_SHOWCASE)
- CLM-020 (hidden, HID-3 GROUNDWORK_GRIND)
- CLM-024 (hidden, HID-4 MARKETPLACE_OBSCURITY)
- CLM-027 (hidden, HID-5 CONTENT_BACKLOG)
- CLM-011 (best, winner)
- CLM-012 (best, winner)
- CLM-034 (best, winner)

### Evidence paths used (mechanical, resolve against package)
- `explicit_patterns.inauspicious`
- `origin_sets.B1`
- `patterns.archetype_resolutions.RES-001`
- `patterns.archetype_resolutions.RES-002`
- `patterns.archetype_resolutions.RES-003`
- `solution_seed.answers[0]`
- `solution_seed.best_solution_candidates[0]`
- `solution_seed.best_solution_candidates[1]`
- `solution_seed.hidden_problems[1]`
- `systems.inner_outer`
- `systems.life_stage_graph`
- `systems.pillars_times_palaces`
- `systems.void_tomb_punish_force_horse_graph['1']`
- `systems.void_tomb_punish_force_horse_graph['2'].tomb_fields`
- `systems.void_tomb_punish_force_horse_graph['2'].void`
- `systems.void_tomb_punish_force_horse_graph['3'].void`
- `systems.void_tomb_punish_force_horse_graph['4']`
- `systems.void_tomb_punish_force_horse_graph['6']`
- `systems.void_tomb_punish_force_horse_graph['7']`
- `systems.void_tomb_punish_force_horse_graph['8'].life_stage_field`
- `systems.void_tomb_punish_force_horse_graph['8'].tomb_fields`
- `systems.void_tomb_punish_force_horse_graph['9'].void`

### Verbatim package readings (audit substrate)

**answers[0] (RES-001)**
> The answer sits in Zhen 3: day stem + concealed leader proxy + duty star + Chief deity converge on one palace. It arrives hour-void (lands on Mao day/hour), runs an Imprisoned Scenery method, and is fed through covered channels (earth Xin generates heaven Ren; hidden Ding-Ren combination). Center's displaced core (Ji + Tian Qin) lodges here too — the institutional core of the matter is administered from this seat.

**HID-palace-4-death-duty-tomb-cluster (rank 1)**
> The avoid-list cluster: Death duty door forced in Xun 4, Door Entering Tomb, the day stem itself entombed and punished there, sanqi Yi restricted — the glittering 'wonder mission' of Xun 4 is the locked door. The hour horse runs straight at it.

**HID-palace-9-void-showpiece (rank 2)**
> The public-facing showcase layer is day-void on the year-stacked palace: big display energy (Scenery at home, 'Prosperous' door) that does not land this window; fills on Wu day/hour.

**HID-palace-1-great-barrier (rank 3)**
> Great Barrier (Geng over Gui) with injury door at Dead on the groundwork track — stalls and grind, intermittent rather than terminal.

**BEST-dui-7-earthly-escape-channel (rank 1)**
> HOW: rest-and-consolidate through Dui 7 — the board's one concordant-strong, affliction-free palace: sanqi stacked (Bing/Yi), earthly escape co-located (Yi + Rest Door), Palace Generating Door explicit, month-stacked (in-period). White Tiger warns the strength reads severe; run it clean and procedural, inside institutions (inner ring).

**BEST-qian-6-harmony-help-channel (rank 2)**
> WHEN/WITH WHOM: Qian 6 is the timing and alliance seat — hour focus, Life door, Six Harmony, Tian Yi star; support is real but buried (star Imprisoned/Imprisoned, Wu entombed, Xu-Chen clash to the day root): activate for pacts and backstage help, expect friction and latency.

**BEST-li-9-salary-channel (rank rejected)**
> (no readability text recorded for this rejected row) (rejection: void-locked payoff window)

**BEST-kun-2-open-gate (rank rejected)**
> (no readability text recorded for this rejected row) (rejection: opens onto day-void with entombed stem and obscurity deity)

