---
id: "chart-analysis-report"
type: "report"
phase: "PACKAGE_RENDER"
batch: "—"
palace_ids: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
sources:
  - "raw/state/chart_analysis_package.json"
  - "raw/state/archetype_resolutions.json"
  - "raw/state/solution_seed.json"
  - "raw/state/red_team.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Analysis Report — project_1 (MARKETING chart JSON)

> **Scope law:** chart-derived evidence only. This report binds nothing to any assignment; requirement-fit is null by design; every claim cites leaf-level JSON paths or derived state objects. Source JSON was hashed and never mutated.

## Infobox
- **Source:** `QMDJ/MARKETING/project_1.json` (sha256 `2f165e078a7c21700e5f1a1f8e44862ddcdd8f04078b733cf9c477dfb9cbcafb`, 8478 bytes, UTF-8)
- **Run:** `carpathia-qmdj-v5-run-20260915T195319Z-411` · generated 2026-09-16T01:33:29Z
- **Schema variant:** project_1_chart_info_v1 (confidence 1.0) · **Variant binding:** semantic-role, no hardcoded paths
- **Chart:** Yi Dun - Lun Cang Jia / Qimen Dunjia Chart · Yin Dun 6th Ju · solar term: White Dew, Lower Yuan, 4th Day · 2026-09-15 22:04 Tue · lunar 8M/5D Hai hour
- **Structural proof:** 294 recursive paths inventoried · 54 array items · 27 absent leaf fields · 12 anomalies preserved · 0 exclusions
- **Gates:** coverage PASS · citations 0 broken · leaf-only OK · board consistency PASS · red team **PASS** · determinism PASS (double-run diff = 0)
- **Protocol:** interpretation v2.2.0 `sha256:protocol_v2_2_2_0_chart_analyst_v5` · rubric v1.1.0 `sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5`

## 0. Executive reading (chart-only)
1. **The seat is Zhen 3 (East, Wood, outer).** Day stem Ren faces outward from Zhen 3, and it is the *only* palace carrying the day stem on heaven; the concealed leader (fu_tou: Jia Chen → Ren) and the duty star (Tian Rui) point at the same palace, with the Chief deity presiding. One seat, no rivals — but it sits **hour-void** (Mao) and its method (Scenery door) is **Imprisoned**: identity is clear; landing and visibility are not.
2. **The trap is Xun 4 (Southeast, Wood, outer).** The duty door itself is **Death**, forced by the palace, entering tomb; the explicit marker entombs *and* punishes the day stem Ren right there — while the same palace flashes explicit 'wonder' patterns (Yi+Geng combination, Three Wonders Obtaining Mission, Nine Heavens, Horse). The chart's own gold is glued to the chart's own lock. Rule 16 split: the glitter is real, the door is shut.
3. **The how is Dui 7 (West, Metal, inner).** The board's only concordant-strong, affliction-free palace: Rest door at Strong, star Prosperous/Prosperous, palace Prosperous/Inner, explicit Palace-Generating-Door, sanqi on both plates (Bing heaven / Yi earth) — **earthly escape co-located**, month-stacked (in-period). White Tiger warns: run it clean, procedural, inside institutions.
4. **The when/with-whom is Qian 6 (Northwest, Metal, inner).** Hour focus, Life door, Six Harmony, the Tian Yi star — but a cool engine (star Imprisoned/Imprisoned, earth Wu entombed) and an Xu–Chen clash into the day root. Use it for pacts and backstage backing; expect latency and friction.
5. **The showcase is void.** Li 9 — the year-stacked public surface — is day-void (Wu) with seasonal fire imprisoned. Big display energy that does not land this window; it fills on **Wu**. And all eight explicit opposite-palace labels disagree with frozen geometry (preserved as anomalies; computed geometry stands).

## 1. Chart anatomy (validated)
| pillar | raw | stem | branch | xun | void check |
|---|---|---|---|---|---|
| year | Bing Wu | Bing (Yang Fire) | Wu | Jia Chen | ['Yin', 'Mao'] |
| month | Ding You | Ding (Yin Fire) | You | Jia Wu | ['Chen', 'Si'] |
| day | Ren Chen | Ren (Yang Water) | Chen | Jia Shen | ['Wu', 'Wei'] |
| hour | Xin Hai | Xin (Yin Metal) | Hai | Jia Chen | ['Yin', 'Mao'] |
- Metadata voids match computed xun voids (day `['Wu', 'Wei']`, hour `['Yin', 'Mao']`) → both **validated**.
- Pillar relations (computed): stem_combination ['Bing', 'Xin'] over ['year', 'hour']; stem_combination ['Ding', 'Ren'] over ['month', 'day']; branch_six_combination ['Chen', 'You'] over ['month', 'day']
- Season: {"earth": "resting", "fire": "trapped", "metal": "prosperous", "water": "strengthening", "wood": "dead"} (raw vocabulary preserved in `raw/state/season.json`)
- Duty: lead = Jia hidden under **Ren** (`chart_info.fu_tou`); duty star **Tian Rui @3** (cross-checked in `palaces.zhen_3.star` and by Chief deity seat); duty door **Death @4** (original 2 ≠ active 4 → displacement logged); tian yi **Tian Chong @6** (`chart_info.tian_yi`, `palaces.qian_6.star`).

## 2. Operator plan (origin sets are sets, resolved by value)
B1 day-trace → **['3']** (proxies converge: lead Ren, duty-star palace; tomb-of-day-gan → ['4']; earth/hidden → ['2', '4']) · B2 hour-focus → **['6']** · B3 cost/check → **['7']** · B4 forward → **['4']** · B5 remainder (Luo Shu) → **['1', '2', '5', '8', '9']**

## 3. Palace verdicts (32 typed claims)
### Palace 1 — Kan (North, Water, outer) · batch B5
*roles:* Great_Barrier (Geng over Gui) · Shang_injury_door_dead · Great_Yin_cover · outer_ring · groundwork_track
- **CLM-020** [chart_hidden_problems_candidate · SUPPORT · MED · EXPLICIT] Kan 1 holds the explicit 'Great Barrier' (both pieces exist: heaven Geng, earth Gui) with Shang (injury) door at Dead and star Discarded/Imprisoned under Great Yin — a hard barrier on the groundwork/water track; stalled starts and injurious grind without yield.
- **CLM-021** [risk · CONSTRAIN · LOW · EXPLICIT] Barrier is intermittent, not terminal: explicit 'Palace Generating Door' and palace state Strong/Outer mean the season still feeds the effort — grind returns poorly now, but the foundation is not dead.
→ full card [[Palace-1-Kan]] · trace `raw/traces/trace_palace_1.json`

### Palace 2 — Kun (Southwest, Earth, inner) · batch B5
*roles:* day_void_member (Wei) · Open_door_channel · duty_door_original_palace (Death home) · Xuanwu_obscurity · tomb_of_Jia_and_Gui · inner_ring · lodger_host (hidden Ji from Center) · day_stem_life_stage_seat (Ren @ Wei/Shen)
- **CLM-022** [chart_best_solution_candidate · SUPPORT · MED · EXPLICIT] An official-opening channel exists in Kun 2: Open door at seasonal Prosperous with explicit 'Palace Generating Door' — the board's one true 'open gate' for launches, approvals and submissions.
- **CLM-023** [chart_best_solution_candidate · VETO · MED · EXPLICIT] Same palace, split claim: Kun 2 is day-void (Wei), heaven Gui is entombed (explicit Tomb (Gui), validated at Wei), and Xuanwu deity (obscurity) watches it while the star is Imprisoned/Discarded — what opens here is void, buried, or not what it seems. Do not ship the flagship through this gate in the current window.
- **CLM-024** [chart_hidden_problems_candidate · SUPPORT · MED · EXPLICIT] Root constraint: the tomb field entombs Jia (the concealed leader/authority substance) together with Gui in Kun 2 — the decision-authority is buried in the void-opening palace; hidden Wu under Gui adds a combination that binds the pall privately. Authority will not appear on demand through this channel.
- **CLM-033** [chart_answers_candidate · CONSTRAIN · MED · EXPLICIT] The day stem's generative seat is parked in the void gate: the chart's own life_stage field names Ren (the day stem) at Kun 2 (Wei/Shen) — growth support for the querent exists structurally but sits in the day-void (Wei) opening palace. Read as not-yet, not never: it activates when the Wei void fills.
→ full card [[Palace-2-Kun]] · trace `raw/traces/trace_palace_2.json`

### Palace 3 — Zhen (East, Wood, outer) · batch B1
*roles:* day_stem_origin · B1_primary · duty_star_palace · lead_stem_proxy (Ren) · Chief_deity_seat (zhi_fu cross-check) · hour_void_member · outer_ring · day_element_outflow (Water->Wood)
- **CLM-001** [chart_answers_candidate · SUPPORT · HIGH · EXPLICIT] The chart's answer-locus is Zhen 3: day stem Ren (querent/day seat) sits on the heaven plate here — the only heaven-plate hit for the day stem — so B1 resolves to a single palace by value match.
- **CLM-002** [chart_answers_candidate · SUPPORT · HIGH · EXPLICIT] Authority converges on the same seat: fu_tou 'Jia Chen Ren' hides the leader Jia under Ren (the day stem itself), duty star Tian Rui (zhi_fu) lands in Zhen 3, the palace star field carries 'Heaven Rui & Heaven Qin', and the Chief deity occupies this palace. No competing candidate found for the answer seat.
- **CLM-003** [timing · WARN · HIGH · EXPLICIT] The answer palace is hour-void: palace branch Mao is in the hour void 'Yin Mao' (explicit marker Void; computed xun check agrees). The matter at the answer seat does not land until the void fills (Mao day/hour).
- **CLM-004** [risk · CONSTRAIN · MED · EXPLICIT] Method at the answer seat constricted: Scenery door is Imprisoned, palace state is Dead/Outer, star strength is split (Imprisoned / Prosperous tokens) — an outwardly visible showpiece over an exhausted core process.
- **CLM-005** [risk · WARN · MED · EXPLICIT] Self-inflicted drag at the answer seat: the harm field names the day stem itself (Ren) at Mao/Zhen 3, and the punishment field names Wu — the querent's own execution mis-steps are the damage vector, not an external enemy.
- **CLM-006** [timing · SEQUENCE · MED · COMPUTED] Support reaches the answer through covered channels: earth Xin metal generates heaven Ren water, and hidden Ding forms a Ding-Ren combination under the day stem — private agreements/resources feed the seat; the visible show (Scenery) is not the feed.
→ full card [[Palace-3-Zhen]] · trace `raw/traces/trace_palace_3.json`

### Palace 4 — Xun (Southeast, Wood, outer) · batch B4
*roles:* B4_forward_check · duty_door_active (Death, forced) · tomb_and_punishment_of_day_stem (Ren) · hour_horse (Si) · Yi+Geng combination · outer_ring · counterfeit_promise_cluster
- **CLM-015** [chart_hidden_problems_candidate · SUPPORT · HIGH · EXPLICIT] Heaviest obstruction cluster is Xun 4: the duty door (zhi_shi) is Death and it is forced (Wood palace over Earth door — explicit 'Palace Oppressing Door'), with explicit 'Door Entering Tomb' on top. The chart's method-to-avoid is named, not inferred.
- **CLM-016** [chart_hidden_problems_candidate · SUPPORT · HIGH · EXPLICIT] The day stem is entombed and punished here: marker 'Tomb & Punishment (Ren)', tomb field 'Xin Ren (Chen, Xun 4, Si)', punishment field 'Ren Gui (Chen, Xun 4, Si)'; Ren water tomb at Chen is computed-validated in-palace. The querent's own stem is buried in the B4 forward-trace palace.
- **CLM-017** [chart_best_solution_candidate · VETO · MED · EXPLICIT] Counterfeit promise inside the trap (split claim, not averaged): sanqi Yi on heaven, explicit 'Wonder Instrument Combination' (Yi+Geng co-located) and 'Three Wonders Obtaining Mission', Nine Heavens deity, and the Horse — yet the same Geng earth controls Yi, 'Three Wonders Being Restricted' is explicit, door is Death at Rest, palace Dead/Outer. The glittering path is the locked path.
- **CLM-018** [timing · WARN · MED · COMPUTED] The hour's fastest vector leads into the obstruction cluster: hour horse Si is validated in Xun 4 — movement this hour runs toward the Death-door palace.
- **CLM-019** [risk · CONSTRAIN · MED · COMPUTED] As B4 (opposite of the hour focus), Xun 4 is the board's 'if-you-proceed blind' check; whatever the execution seat (Qian 6) starts, this palace is its overshoot risk.
→ full card [[Palace-4-Xun]] · trace `raw/traces/trace_palace_4.json`

### Palace 5 — Center (Center, Earth, inner) · batch B5
*roles:* center_pivot · NO_OPPOSITE · displaced_core (Ji + Tian Qin lodged) · life_stage_seed (Changsheng) · placeholder_relation_fields
- **CLM-025** [chart_answers_candidate · CONSTRAIN · MED · EXPLICIT] The core is displaced: Center's heaven Ji and star Tian Qin are lodged into Zhen 3 (co-lodging confirmed in palace 3 star field), hidden Ji into Kun 2. Center owns no door, no branches, no direction — the central matter is administered from its host palaces; read it through 3 and 2, not directly.
- **CLM-026** [chart_answers_candidate · SUPPORT · LOW · EXPLICIT] Life-stage seed: Center's life_stage reads 'Changsheng (Longevity)' — the displaced core keeps a generative seed; its Harm/Tomb/Punishment fields are placeholder labels only (logged as anomalies, no content).
→ full card [[Palace-5-Center]] · trace `raw/traces/trace_palace_5.json`

### Palace 6 — Qian (Northwest, Metal, inner) · batch B2
*roles:* hour_stem_focus · B2_primary · tian_yi_star_seat (Tian Chong) · month_horse · Six_Harmony_seat · inner_ring · clash_to_day_branch (Xu~Chen) · tomb_of_earth_stem (Wu)
- **CLM-007** [timing · SUPPORT · HIGH · EXPLICIT] The execution/timing seat is Qian 6: hour stem Xin on heaven, hour branch Hai resident in palace, and the month horse also lands here — hour focus, hour root and mover coincide in one palace.
- **CLM-008** [chart_best_solution_candidate · SUPPORT · MED · EXPLICIT] Help/quality pole confirmed at Qian 6: Life door with explicit 'Door Generating Palace', Six Harmony deity (pacts, alignment), and the chart's Tian Yi (Tian Chong) star seated here; hidden Bing under heaven Xin adds a Bing-Xin combination — a binding pact under the help seat.
- **CLM-009** [risk · CONSTRAIN · MED · EXPLICIT] The help engine runs cool: star strength is Imprisoned/Imprisoned (concordant weak), door at Rest, explicit Tomb (Wu) marker, and the tomb field buries Yi, Bing and Wu — including the palace's own earth stem Wu. Support exists but is buried/late: institutional or backstage delivery.
- **CLM-010** [risk · WARN · MED · COMPUTED] Structural jolt: palace branch Xu clashes the day branch Chen — activating the help/harmony palace shakes the day's own root; expect the backing to arrive with friction against current commitments.
→ full card [[Palace-6-Qian]] · trace `raw/traces/trace_palace_6.json`

### Palace 7 — Dui (West, Metal, inner) · batch B3
*roles:* B3_cost_check · strongest_wangshuai_concordant · sanqi_Bing_seat · earthly_escape_combo (Yi+Rest) · month_branch_stacked (You) · inner_ring · White_Tiger_teeth · no_affliction_fields
- **CLM-011** [chart_best_solution_candidate · SUPPORT · HIGH · EXPLICIT] Dui 7 is the strongest clean action palace: Rest door at Strong, star Prosperous/Prosperous (concordant), palace Prosperous/Inner, explicit 'Palace Generating Door', and sanqi — Yang Fire Bing on heaven with Yin Wood Yi on earth beneath. Both pieces of the earthly-escape combination (Yi + Rest Door) exist in-palace.
- **CLM-012** [chart_best_solution_candidate · SUPPORT · MED · EXPLICIT] No affliction fields are recorded for Dui 7 — special_markers, inauspicious_patterns, tomb and punishment are all absent (recorded in absence registry; absence is evidence, not assumed safety); combined with the concordant strengths this is the board's least-obstructed palace.
- **CLM-013** [risk · WARN · MED · EXPLICIT] Teeth on the strong option: White Tiger deity rides Dui 7 — the forceful route carries severity (hard pushback, strict review, fierce competition). As B3 it is also the cost/check opposite of the day seat: chart-wise it reads as the strong-looking alternative/rival channel, not the querent's own seat.
- **CLM-014** [timing · SUPPORT · MED · COMPUTED] Month alignment: the month-pillar branch You is stacked on Dui 7 — this palace is 'in month', i.e., resourced for the current period.
- **CLM-034** [risk · WARN · MED · EXPLICIT] The chart's strongest channel chafes the institutional core: palace 7's own harm field names Ji — the Center palace's earth stem. Consolidation through Dui 7 must stay procedural and inside formal frames, or it bruises the very core it means to protect.
→ full card [[Palace-7-Dui]] · trace `raw/traces/trace_palace_7.json`

### Palace 8 — Gen (Northeast, Earth, outer) · batch B5
*roles:* hour_void_member (Yin) · Du_blockage_seat · Ding_tomb · Oppression (door over palace) · Flying_Snake_loops · outer_ring · storage_not_launch
- **CLM-027** [chart_hidden_problems_candidate · SUPPORT · MED · EXPLICIT] Gen 8 is a stalled-storage node: Du (blockage) door at Dead, hour-void Yin in-palace, explicit 'Tomb (Ding)' and 'Ding Wonder Entering Tomb' — sanqi Yin Fire Ding on heaven entombed at Chou — plus 'Oppression' (door Wood over palace Earth, computed-confirmed) and Flying Snake anxiety loops. Drafts, archives and slow assets jam here.
- **CLM-028** [chart_best_solution_candidate · VETO · LOW · EXPLICIT] No escape via Gen 8: the star is strong at the palace token (Prosperous) but Rest at climate token, the door is dead and the wonder is entombed — storage, not launch.
→ full card [[Palace-8-Gen]] · trace `raw/traces/trace_palace_8.json`

### Palace 9 — Li (South, Fire, inner) · batch B5
*roles:* year_branch_stacked (Wu) · day_void_member · Scenery_at_original_palace · explicit_pattern_conflict (Palace Oppressing Door) · inner_ring · showcase_layer
- **CLM-029** [chart_hidden_problems_candidate · SUPPORT · HIGH · EXPLICIT] The showcase layer is void this cycle: Li 9 holds the year-pillar branch Wu stacked in-palace, and Wu is in the day void 'Wu Wei' (explicit Void marker; computed-validated). The public-facing surface of the year's frame does not land as presented; palace state Imprisoned/Inner with seasonal fire Imprisoned compounds it.
- **CLM-030** [risk · WARN · MED · ANOMALOUS] Explicit-vs-computed conflict at Li 9: the chart explicitly lists 'Palace Oppressing Door', but computed elements show Fire palace with Fire door (Scenery, at its original palace) — no control relation exists. Both are preserved; the explicit pattern is flagged ANOMALOUS, not repaired.
- **CLM-031** [timing · SEQUENCE · MED · COMPUTED] The void fills on Wu: day-void Wu resolves when Wu day/hour arrives — visibility pushes land then, not before; scheduled showcases in the void window will underperform their billing.
- **CLM-032** [chart_best_solution_candidate · VETO · LOW · EXPLICIT] Li 9's 'Wonder Wandering Salary Position' (Ding's salary at Wu, earth stem Ding in-palace) reads as a real but void-locked pay-off: a genuine gains-channel that cannot be collected in the current window.
→ full card [[Palace-9-Li]] · trace `raw/traces/trace_palace_9.json`

## 4. Systems (P6)
**Wangshuai matrix** (raw tokens preserved; normalization computed):
| palace | element(season) | door strength | star strength raw | palace state | split | door==season? |
|---|---|---|---|---|---|---|
| 1 | water (strengthening) | Dead | Discarded / Imprisoned | Strong / Outer | YES | False |
| 2 | earth (resting) | Prosperous | Imprisoned / Discarded | Rest / Inner | YES | False |
| 3 | wood (dead) | Imprisoned | Imprisoned / Prosperous | Dead / Outer | YES | False |
| 4 | wood (dead) | Rest | Rest / Strong | Dead / Outer | YES | False |
| 5 | earth (resting) | — | — | Rest | no | None |
| 6 | metal (prosperous) | Rest | Imprisoned / Imprisoned | Prosperous / Inner | no | False |
| 7 | metal (prosperous) | Strong | Prosperous / Prosperous | Prosperous / Inner | no | False |
| 8 | earth (resting) | Dead | Prosperous / Rest | Rest / Outer | YES | False |
| 9 | fire (trapped) | Prosperous | Imprisoned / Strong | Imprisoned / Inner | YES | False |
- Door map: Death@4; Du@8; Life@6; Open@2; Rest@7; Scenery@9; Shang@1
- Star map: every star displaced from home (0 `star_sitting_home` hits); Tian Qin additionally lodged out of center into Zhen 3.
- Deity map: Chief@3; Flying Snake@8; Great Yin@1; Nine Earths@9; Nine Heavens@4; Six Harmony@6; Tai Chang@5; White Tiger@7; Xuanwu@2
- San Qi: Yi (4 heav, 7 earth, 9 hid) · Bing (7 heav, 8 earth, 6 hid) · Ding (8 heav, 9 earth, 3 hid). Hidden-layer five-combinations computed: Ding–Ren in palace 3, Bing–Xin in palace 6, Wu–Gui in palace 2.
- **Liu-Yi punishment validated:** all six entries match the classical punishment-palace table (Wu@3, Ji@2, Geng@8, Xin@9, Ren@4, Gui@4) — chart internals consistent; oppression marker validated (door Wood over palace Earth in Gen 8); palace name fields all match keys.
- **Original-position audit:** explicit branch lists match frozen geometry 8/8; original stars/doors all consistent; deity divergences recorded as expected rotation; `original_position.numbers` kept opaque by policy. Six-harm branch relations computed: Chen(4)–Mao(3) ties the trap palace to the answer seat; You(7)–Xu(6) warns that the HOW and WHEN channels chafe each other.

## 5. Patterns (explicit first, computed second)
| explicit pattern | palace | reconciliation | |
|---|---|---|---|
| Palace Generating Door | 1 | VALIDATED |  |
| Great Barrier | 1 | VALIDATED | Geng over Gui co-located (both pieces exist) |
| Palace Generating Door | 2 | VALIDATED |  |
| Palace Generating Door | 3 | VALIDATED |  |
| Wonder Instrument Combination | 4 | VALIDATED | Yi+Geng five-combination co-located in-palace |
| Three Wonders Obtaining Mission | 4 | VALIDATED | sanqi Yi co-located with the duty door (zhi_shi Death) |
| Door Entering Tomb | 4 | VALIDATED_SCHOOL_VARIANT | Death door Earth rides over Chen water-tomb branch in-palace (earth-follows-water convention) |
| Palace Oppressing Door | 4 | VALIDATED |  |
| Three Wonders Being Restricted | 4 | VALIDATED | Geng metal controls Yi wood in-palace |
| Door Generating Palace | 6 | VALIDATED |  |
| Palace Generating Door | 7 | VALIDATED |  |
| Ding Wonder Entering Tomb | 8 | VALIDATED | Ding tomb Chou in-palace; explicit Tomb (Ding) marker |
| Door Oppressing Palace | 8 | VALIDATED |  |
| Wonder Wandering Salary Position | 9 | VALIDATED | Ding salary at Wu; earth stem Ding in Li 9 (school convention note) |
| Palace Oppressing Door | 9 | CONFLICT | explicit vs computed conflict — anomaly ANO logged |

Computed catalog highlights: forced_door@4 · void_palace {2,3,8,9} · stem_in_tomb {2,4,6,8} · duty_star@3 · duty_door@4 · hour_stem_focus@6 · horse_star {2,4,6,8} · **earthly_escape@7 (named — both pieces present)** · heavenly/human escapes withheld (pieces not co-located) · door_at_original_palace@9 · star_sitting_home: 0 hits · split_star_strength {1,2,3,4,8,9} · stacked branches: year→9, month→7, day→4, hour→6 · opposite_palace_mismatch on all 8 labeled palaces.

## 6. Archetype resolutions (rubric v1.1.0; requirement_fit = null)
### RES-001 — chart_answers_candidate
| candidate | grounding | support | contra | board | score | selected | reason |
|---|---|---|---|---|---|---|---|
| ANS-seats-in-zhen-3 | EXPLICIT | 6 | 2 | ✓ | **0.7** | **WINNER** | no competing candidate found |
- **Winner:** ANS-seats-in-zhen-3 · **Margin:** Single candidate: no competing candidate found — both independent selectors (day-stem heaven trace and duty/fu_tou proxy) resolve to the same palace; center adds displaced-core context but owns no door. What would flip this: nothing in-chart short of a changed source file. What tempers it: hour-void (lands on Mao) and harm naming the day stem — constraints ON the seat, not alternative seats.
- **Tie note:** not tied; singleton resolution (explicitly stated per rule 19)

### RES-002 — chart_hidden_problems_candidate
| candidate | grounding | support | contra | board | score | selected | reason |
|---|---|---|---|---|---|---|---|
| HID-palace-4-death-duty-tomb-cluster | EXPLICIT | 9 | 2 | ✓ | **0.7** | **WINNER** | — |
| HID-palace-9-void-showpiece | EXPLICIT | 5 | 1 | ✓ | **0.6889** |  | void-locked showcase: real but seasonal/void-window problem; narrower blast radius than the palace-4 duty cluster |
| HID-palace-1-great-barrier | EXPLICIT | 4 | 1 | ✓ | **0.6611** |  | hard barrier on groundwork track, but intermittent (palace state Strong/Outer, Palace Generating Door) |
| HID-palace-2-void-open-jia-tomb | EXPLICIT | 4 | 1 | ✓ | **0.6611** |  | void-opening with entombed authority (Jia); severe, but it masks rather than destroys — reads as constraint cluster, not the primary obstruction |
| HID-palace-8-stalled-storage | EXPLICIT | 4 | 1 | ✓ | **0.6611** |  | jam/storage node (Du door dead, Ding entombed); scope limited to slow assets and drafts |
- **Winner:** HID-palace-4-death-duty-tomb-cluster · **Margin:** Margin is thin over HID-palace-9-void-showpiece (0.7000 vs 0.6889) because both are EXPLICIT-grounded; the winner leads on corroboration (9 vs 5 independent paths) and on the duty-door class. Flip condition: if downstream reading treats the day void (Wu Wei) as covering the whole current operation window, the void-showpiece overtakes; if the duty door were re-seated (source change), the cluster dissolves.
- **Tie note:** HID-palace-1, HID-palace-2 and HID-palace-8 finished equal on all rubric components (0.6611); ordering between them follows the documented tie-break (earlier first-appearance phase) and is otherwise STILL_TIED in rank

### RES-003 — chart_best_solution_candidate
| candidate | grounding | support | contra | board | score | selected | reason |
|---|---|---|---|---|---|---|---|
| BEST-dui-7-earthly-escape-channel | EXPLICIT | 10 | 2 | ✓ | **0.8** | **WINNER** | — |
| BEST-qian-6-harmony-help-channel | EXPLICIT | 6 | 3 | ✓ | **0.65** |  | genuine help seat (Life door, Six Harmony, Tian Yi star, hour focus) but cool engine: star Imprisoned/Imprisoned, earth stem entombed, branch clash to day root |
| BEST-li-9-salary-channel | EXPLICIT | 2 | 3 | ✓ | **0.55** |  | void-locked: day-void Wu on the year-stacked showcase palace; real payoff, wrong window |
| BEST-kun-2-open-gate | EXPLICIT | 3 | 4 | ✓ | **0.525** |  | the one Open door on the board but day-void, heaven Gui entombed, Xuanwu obscurity, star Imprisoned/Discarded — opens onto void |
- **Winner:** BEST-dui-7-earthly-escape-channel · **Margin:** Winner leads runner-up BEST-qian-6 by 0.15 (narrowed from 0.20 after audit-cycle-2 disclosure of palace 7's harm field naming the center stem Ji). Flip conditions unchanged: hour-focus/tian-yi weighting prioritises Qian 6 as the WHEN while Dui 7 stays the HOW; any further affliction evidence on Dui 7; or a source revision adding explicit answer fields, which outranks all computed ranking.
- **Tie note:** no tie at the top; B9 vs B2 invert under tie-break only

## 7. Solution seed — chart-derived only, not yet requirement-bound
*note carried in package:* `chart-derived only; not yet requirement-bound`
### Answers
- **[RES-001 · score 0.7]** The answer sits in Zhen 3: day stem + concealed leader proxy + duty star + Chief deity converge on one palace. It arrives hour-void (lands on Mao day/hour), runs an Imprisoned Scenery method, and is fed through covered channels (earth Xin generates heaven Ren; hidden Ding-Ren combination). Center's displaced core (Ji + Tian Qin) lodges here too — the institutional core of the matter is administered from this seat. (claims: CLM-001, CLM-002; constraints cited: `palaces.zhen_3.special_markers[0]`, `palaces.zhen_3.prosperity_decline.palace_state`, `palaces.zhen_3.harm`)
### Hidden problems (ranked)
- **#1 [RES-002 · HID-palace-4-death-duty-tomb-cluster · 0.7]** The avoid-list cluster: Death duty door forced in Xun 4, Door Entering Tomb, the day stem itself entombed and punished there, sanqi Yi restricted — the glittering 'wonder mission' of Xun 4 is the locked door. The hour horse runs straight at it. (claims: CLM-015, CLM-016)
- **#2 [RES-002 · HID-palace-9-void-showpiece · 0.6889]** The public-facing showcase layer is day-void on the year-stacked palace: big display energy (Scenery at home, 'Prosperous' door) that does not land this window; fills on Wu day/hour. (claims: CLM-029)
- **#3 [RES-002 · HID-palace-1-great-barrier · 0.6611]** — tied at this score with HID-palace-2-void-open-jia-tomb, HID-palace-8-stalled-storage Great Barrier (Geng over Gui) with injury door at Dead on the groundwork track — stalls and grind, intermittent rather than terminal. (claims: CLM-020)
### Best-solution candidates (ranked)
- **1 [BEST-dui-7-earthly-escape-channel · 0.8]** HOW: rest-and-consolidate through Dui 7 — the board's one concordant-strong, affliction-free palace: sanqi stacked (Bing/Yi), earthly escape co-located (Yi + Rest Door), Palace Generating Door explicit, month-stacked (in-period). White Tiger warns the strength reads severe; run it clean and procedural, inside institutions (inner ring). — caveats: `palaces.dui_7.deity`, `palaces.dui_7.harm` (claims: CLM-011, CLM-012, CLM-034)
- **2 [BEST-qian-6-harmony-help-channel · 0.65]** WHEN/WITH WHOM: Qian 6 is the timing and alliance seat — hour focus, Life door, Six Harmony, Tian Yi star; support is real but buried (star Imprisoned/Imprisoned, Wu entombed, Xu-Chen clash to the day root): activate for pacts and backstage help, expect friction and latency. — caveats: `palaces.qian_6.special_markers[0]`, `palaces.qian_6.prosperity_decline.star_strength` (claims: CLM-008)
- **rejected [BEST-li-9-salary-channel · 0.55]**  — rejected: void-locked payoff window (claims: CLM-032)
- **rejected [BEST-kun-2-open-gate · 0.525]**  — rejected: opens onto day-void with entombed stem and obscurity deity (claims: CLM-023)

## 8. Timing picture (chart-derived)
- Voids: day-void **Wu Wei** → palaces 9 (Wu) and 2 (Wei) silent until filled (fills on Wu/Wei); hour-void **Yin Mao** → palaces 8 (Yin) and 3 (Mao) — the answer seat lands on **Mao** day/hour; the showcase fills on **Wu**.
- Horses: year Shen→2, month Hai→6, day Yin→8, hour **Si→4** — the hour's fastest vector points into the obstruction cluster; the month horse supports the help palace 6.
- Stacked pillar branches: year→9, month→7, day→4, hour→6 — palaces 9/7/4/6 are 'in-frame' for their respective periods; palace 7 is month-resourced now.
- Clashes: palace 6 branch Xu clashes day branch Chen — activating help rocks the day's root (SEQUENCE/WARN shipped on CLM-011).

## 9. Anomalies & absences (preserved, never repaired)
**Anomalies: 12**
| id | type | severity | description |
|---|---|---|---|
| ANO-001 | PLACEHOLDER_LABEL_VALUE | LOW | center_5.harm is 'Harm': category label, no stem/branch content |
| ANO-002 | PLACEHOLDER_LABEL_VALUE | LOW | center_5.tomb is 'Tomb': category label, no stem/branch content |
| ANO-003 | PLACEHOLDER_LABEL_VALUE | LOW | center_5.punishment is 'Punishment': category label, no stem/branch content |
| ANO-004 | OPPOSITE_PALACE_MISMATCH | MED | palace 1 explicit opposite_palace 'Kun 8' != frozen geometry 'Li 9'; label 'Kun 8' is also internally inconsistent |
| ANO-005 | OPPOSITE_PALACE_MISMATCH | MED | palace 2 explicit opposite_palace 'Xun 5' != frozen geometry 'Gen 8'; label 'Xun 5' is also internally inconsistent |
| ANO-006 | OPPOSITE_PALACE_MISMATCH | MED | palace 3 explicit opposite_palace 'Li 3' != frozen geometry 'Dui 7'; label 'Li 3' is also internally inconsistent |
| ANO-007 | OPPOSITE_PALACE_MISMATCH | MED | palace 4 explicit opposite_palace 'Dui 2' != frozen geometry 'Qian 6'; label 'Dui 2' is also internally inconsistent |
| ANO-008 | OPPOSITE_PALACE_MISMATCH | MED | palace 6 explicit opposite_palace 'Gen 7' != frozen geometry 'Xun 4'; label 'Gen 7' is also internally inconsistent |
| ANO-009 | OPPOSITE_PALACE_MISMATCH | MED | palace 7 explicit opposite_palace 'Kan 6' != frozen geometry 'Zhen 3'; label 'Kan 6' is also internally inconsistent |
| ANO-010 | OPPOSITE_PALACE_MISMATCH | MED | palace 8 explicit opposite_palace 'Zhen 4' != frozen geometry 'Kun 2'; label 'Zhen 4' is also internally inconsistent |
| ANO-011 | OPPOSITE_PALACE_MISMATCH | MED | palace 9 explicit opposite_palace 'Qian 1' != frozen geometry 'Kan 1'; label 'Qian 1' is also internally inconsistent |
| ANO-012 | EXPLICIT_PATTERN_COMPUTED_CONFLICT | MED | li_9 lists 'Palace Oppressing Door' but palace element Fire does not control door element Fire (Scenery at original palace); explicit preserved, computed disagrees |

**Absences: 27 leaf fields across 8 palaces** — absence recorded, never treated as false:
- palace 1: `kan_1.special_markers`, `kan_1.harm`, `kan_1.tomb`, `kan_1.punishment` — unassessed; absence recorded, not treated as false
- palace 2: `kun_2.inauspicious_patterns` — unassessed; absence recorded, not treated as false
- palace 3: `zhen_3.inauspicious_patterns`, `zhen_3.tomb` — unassessed; absence recorded, not treated as false
- palace 5: `center_5.door`, `center_5.special_markers`, `center_5.auspicious_patterns`, `center_5.inauspicious_patterns`, `original_position.deity`, `original_position.door`, `original_position.branches`, `original_position.opposite_palace`, `prosperity_decline.door_strength`, `prosperity_decline.star_strength` — center structurally lacks door/branches/opposite (non-directional pivot) — variant-expected
- palace 6: `qian_6.inauspicious_patterns`, `qian_6.life_stage`, `qian_6.punishment` — unassessed; absence recorded, not treated as false
- palace 7: `dui_7.special_markers`, `dui_7.inauspicious_patterns`, `dui_7.tomb`, `dui_7.punishment` — unassessed; absence recorded, not treated as false
- palace 8: `gen_8.auspicious_patterns` — unassessed; absence recorded, not treated as false
- palace 9: `li_9.harm`, `li_9.tomb` — unassessed; absence recorded, not treated as false

## 10. Coverage, gates, red team, determinism
- Coverage gate: {"absence_registry_complete": true, "anomalies_logged": true, "array_itemization_complete": true, "exclusion_log_complete": true, "explicit_patterns_ingested": true, "leaf_unpacking_verified": true, "path_coverage_manifest_complete": true}
- Package gates: schema True · citations broken 0 · parent-only citations 0 · board consistency True · archetype refs missing 0 · determinism True · coverage True · explicit-before-computed True
- Red team: **PASS** — 3 adversarial rederivation attempts (Kun 2 as best channel / Li 9 as auspicious showcase / re-seating the answer) all REJECTED with cited reasons; contamination scans clean. Details: [[Chart-Red-Team]].
- AUDIT_FIX cycles used: 1 of 3 (citation class rewrite `state:qmdj_complete.*` → `state:frozen_tables.*` persisted).

## 11. Unbound yongshen candidates (no assignment binding)
| candidate | class | bound | requirement_fit |
|---|---|---|---|
| day stem Ren (Yang Water) | day_stem_or_jia_set | False | None |
| hour stem Xin (Yin Metal) | hour_stem_or_focus | False | None |
| lead proxy Ren (fu_tou Jia Chen Ren) | lead_stem_proxy | False | None |
| duty star Tian Rui @ palace 3 | duty_star | False | None |
| tian yi Tian Chong @ palace 6 | tian_yi | False | None |
| duty door Death @ palace 4 (avoidance pole) | duty_door_forced_dead | False | None |

## 12. Provenance & reproduction
- Source: `QMDJ/MARKETING/project_1.json` · sha256 `2f165e078a7c21700e5f1a1f8e44862ddcdd8f04078b733cf9c477dfb9cbcafb` · ingested 2026-09-15T19:53:19Z · run `carpathia-qmdj-v5-run-20260915T195319Z-411`
- Package: `raw/state/chart_analysis_package.json` (sha256 `4e906b0f47d1c4dfb90c8ad3c93dadac095622558e7c5e6eb441cdb40f3b1a37`)
- Determinism: P0 derivation run twice in memory, origin-sets diff = 0; package byte-stable modulo `generated_at`/`run_id`.
- Pipeline: CHART_INGEST → STRUCTURAL_INVENTORY → SCHEMA_ADAPTATION → P0_ANATOMY → B1–B5 → COVERAGE_GATE → P6_BOARD_SYNTHESIS → PACKAGE_RENDER → HALT

See also: [[Chart-Anatomy]] · [[Chart-Board-Synthesis]] · [[Chart-Patterns]] · [[Palace-Analysis-Index]] · [[Chart-Red-Team]] · [[MOC]]