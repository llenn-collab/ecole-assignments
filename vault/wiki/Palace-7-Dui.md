---
id: "palace-7"
type: "palace-card"
phase: "B3"
batch: "B3"
palace_ids: ["7"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 7 — Dui (兑), West, Metal · batch B3

**Raw key:** `dui_7` · **Ring:** inner · **Branches:** Rooster (You)
**Roles:** B3_cost_check · strongest_wangshuai_concordant · sanqi_Bing_seat · earthly_escape_combo (Yi+Rest) · month_branch_stacked (You) · inner_ring · White_Tiger_teeth · no_affliction_fields

## Plates
- Heaven stem: `Bing` · Earth stem: `Yi` · Hidden stem: `Gui`
- Star: `Heaven Ren` · Door: `Rest` · Deity: `White Tiger`
- Markers: []
- Auspicious (explicit): ["Palace Generating Door"]
- Inauspicious (explicit): []
- Prosperity/decline: {"door_strength": "Strong", "star_strength": "Prosperous / Prosperous", "palace_state": "Prosperous / Inner"}
- **Absent leaf fields** (registry): `special_markers`, `inauspicious_patterns`, `tomb`, `punishment`

## Verdicts (typed, leaf-cited)
- **CLM-011** [chart_best_solution_candidate · SUPPORT · HIGH · EXPLICIT · live] Dui 7 is the strongest clean action palace: Rest door at Strong, star Prosperous/Prosperous (concordant), palace Prosperous/Inner, explicit 'Palace Generating Door', and sanqi — Yang Fire Bing on heaven with Yin Wood Yi on earth beneath. Both pieces of the earthly-escape combination (Yi + Rest Door) exist in-palace.
  - evidence: `palaces.dui_7.heaven_stem`, `palaces.dui_7.earth_stem`, `palaces.dui_7.door`, `palaces.dui_7.prosperity_decline.door_strength`, `palaces.dui_7.prosperity_decline.star_strength`, `palaces.dui_7.prosperity_decline.palace_state`, `palaces.dui_7.auspicious_patterns[0]`
- **CLM-012** [chart_best_solution_candidate · SUPPORT · MED · EXPLICIT · live] No affliction fields are recorded for Dui 7 — special_markers, inauspicious_patterns, tomb and punishment are all absent (recorded in absence registry; absence is evidence, not assumed safety); combined with the concordant strengths this is the board's least-obstructed palace.
  - evidence: `state:absence_registry.records`, `palaces.dui_7.star`
- **CLM-013** [risk · WARN · MED · EXPLICIT · live] Teeth on the strong option: White Tiger deity rides Dui 7 — the forceful route carries severity (hard pushback, strict review, fierce competition). As B3 it is also the cost/check opposite of the day seat: chart-wise it reads as the strong-looking alternative/rival channel, not the querent's own seat.
  - evidence: `palaces.dui_7.deity`, `state:origin_sets.B3.primary_set`
- **CLM-014** [timing · SUPPORT · MED · COMPUTED · live] Month alignment: the month-pillar branch You is stacked on Dui 7 — this palace is 'in month', i.e., resourced for the current period.
  - evidence: `chart_info.ganzhi.month`, `state:palace_key_resolution.palaces.7.branches`
- **CLM-034** [risk · WARN · MED · EXPLICIT · live] The chart's strongest channel chafes the institutional core: palace 7's own harm field names Ji — the Center palace's earth stem. Consolidation through Dui 7 must stay procedural and inside formal frames, or it bruises the very core it means to protect.
  - evidence: `palaces.dui_7.harm`, `palaces.center_5.earth_stem`

## Relations (computed)
- *generation_drain* — Bing fire generates Yi — upper layer drains into lower (`palaces.dui_7.heaven_stem`, `palaces.dui_7.earth_stem`)
- *control* — Gui water controls Bing fire (`palaces.dui_7.heaven_stem`, `palaces.dui_7.hidden_stem`)
- *palace_generating_door* — palace Metal generates door Rest (Water) (`palaces.dui_7.door`, `state:palace_key_resolution.palaces.7.element`)
- *star_home_displacement* — Tian Ren home palace 8, seated in 7 — DISPLACED (`palaces.dui_7.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Rest away from original (Fright Door) (`palaces.dui_7.door`, `palaces.dui_7.original_position.door`)
- *stacked_pillar_branch_on_palace* — month pillar branch You stacked on palace 7 (`chart_info.ganzhi.month`, `state:palace_key_resolution.palaces.7.branches`)
- *branch_six_combination* — palace branch You six-combines day pillar branch Chen (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.7.branches`)
- *day_element_vs_palace* — day element Water vs palace element Metal: palace produces day (inflow) (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.7.element`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_7.json`