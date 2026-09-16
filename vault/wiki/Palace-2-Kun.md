---
id: "palace-2"
type: "palace-card"
phase: "B5"
batch: "B5"
palace_ids: ["2"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 2 — Kun (坤), Southwest, Earth · batch B5

**Raw key:** `kun_2` · **Ring:** inner · **Branches:** Goat (Wei), Monkey (Shen)
**Roles:** day_void_member (Wei) · Open_door_channel · duty_door_original_palace (Death home) · Xuanwu_obscurity · tomb_of_Jia_and_Gui · inner_ring · lodger_host (hidden Ji from Center) · day_stem_life_stage_seat (Ren @ Wei/Shen)

## Plates
- Heaven stem: `Gui` · Earth stem: `Ren` · Hidden stem: `Wu`
- Star: `Heaven Peng` · Door: `Open` · Deity: `Xuanwu`
- Markers: ["Void", "Tomb (Gui)"]
- Auspicious (explicit): ["Palace Generating Door"]
- Inauspicious (explicit): []
- Prosperity/decline: {"door_strength": "Prosperous", "star_strength": "Imprisoned / Discarded", "palace_state": "Rest / Inner"}
- **Absent leaf fields** (registry): `inauspicious_patterns`

## Verdicts (typed, leaf-cited)
- **CLM-022** [chart_best_solution_candidate · SUPPORT · MED · EXPLICIT · live] An official-opening channel exists in Kun 2: Open door at seasonal Prosperous with explicit 'Palace Generating Door' — the board's one true 'open gate' for launches, approvals and submissions.
  - evidence: `palaces.kun_2.door`, `palaces.kun_2.auspicious_patterns[0]`, `palaces.kun_2.prosperity_decline.door_strength`
- **CLM-023** [chart_best_solution_candidate · VETO · MED · EXPLICIT · live] Same palace, split claim: Kun 2 is day-void (Wei), heaven Gui is entombed (explicit Tomb (Gui), validated at Wei), and Xuanwu deity (obscurity) watches it while the star is Imprisoned/Discarded — what opens here is void, buried, or not what it seems. Do not ship the flagship through this gate in the current window.
  - evidence: `palaces.kun_2.special_markers[0]`, `palaces.kun_2.special_markers[1]`, `palaces.kun_2.deity`, `palaces.kun_2.prosperity_decline.star_strength`, `chart_info.void.day`
- **CLM-024** [chart_hidden_problems_candidate · SUPPORT · MED · EXPLICIT · live] Root constraint: the tomb field entombs Jia (the concealed leader/authority substance) together with Gui in Kun 2 — the decision-authority is buried in the void-opening palace; hidden Wu under Gui adds a combination that binds the pall privately. Authority will not appear on demand through this channel.
  - evidence: `palaces.kun_2.tomb`, `palaces.kun_2.hidden_stem`, `palaces.kun_2.heaven_stem`, `state:marker_validation.tomb`
- **CLM-033** [chart_answers_candidate · CONSTRAIN · MED · EXPLICIT · live] The day stem's generative seat is parked in the void gate: the chart's own life_stage field names Ren (the day stem) at Kun 2 (Wei/Shen) — growth support for the querent exists structurally but sits in the day-void (Wei) opening palace. Read as not-yet, not never: it activates when the Wei void fills.
  - evidence: `palaces.kun_2.life_stage`, `chart_info.ganzhi.day`, `palaces.kun_2.special_markers[0]`

## Relations (computed)
- *stem_combination* — Gui+Wu form a five-combination (heaven/hidden of palace 2) (`palaces.kun_2.heaven_stem`, `palaces.kun_2.hidden_stem`)
- *control* — Wu earth controls Gui water (`palaces.kun_2.heaven_stem`, `palaces.kun_2.hidden_stem`)
- *palace_generating_door* — palace Earth generates door Open (Metal) (`palaces.kun_2.door`, `state:palace_key_resolution.palaces.2.element`)
- *star_home_displacement* — Tian Peng home palace 1, seated in 2 — DISPLACED (`palaces.kun_2.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Open away from original (Death Door) (`palaces.kun_2.door`, `palaces.kun_2.original_position.door`)
- *branch_six_combination* — palace branch Wei six-combines year pillar branch Wu (`chart_info.ganzhi.year`, `state:palace_key_resolution.palaces.2.branches`)
- *day_element_vs_palace* — day element Water vs palace element Earth: palace controls day (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.2.element`)
- *horse_star* — year horse (Shen) in palace 2 (`chart_info.horse.year`, `state:palace_key_resolution.palaces.2.branches`)
- *void_palace* — palace 2 void: day-void ['Wei'], hour-void — (`chart_info.void.day`, `chart_info.void.hour`, `state:palace_key_resolution.palaces.2.branches`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_2.json`