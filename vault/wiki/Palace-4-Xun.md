---
id: "palace-4"
type: "palace-card"
phase: "B4"
batch: "B4"
palace_ids: ["4"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 4 — Xun (巽), Southeast, Wood · batch B4

**Raw key:** `xun_4` · **Ring:** outer · **Branches:** Dragon (Chen), Snake (Si)
**Roles:** B4_forward_check · duty_door_active (Death, forced) · tomb_and_punishment_of_day_stem (Ren) · hour_horse (Si) · Yi+Geng combination · outer_ring · counterfeit_promise_cluster

## Plates
- Heaven stem: `Yi` · Earth stem: `Geng` · Hidden stem: `Ren`
- Star: `Heaven Pillar` · Door: `Death` · Deity: `Nine Heavens`
- Markers: ["Horse", "Tomb & Punishment (Ren)"]
- Auspicious (explicit): ["Wonder Instrument Combination", "Three Wonders Obtaining Mission"]
- Inauspicious (explicit): ["Door Entering Tomb", "Palace Oppressing Door", "Three Wonders Being Restricted"]
- Prosperity/decline: {"door_strength": "Rest", "star_strength": "Rest / Strong", "palace_state": "Dead / Outer"}

## Verdicts (typed, leaf-cited)
- **CLM-015** [chart_hidden_problems_candidate · SUPPORT · HIGH · EXPLICIT · live] Heaviest obstruction cluster is Xun 4: the duty door (zhi_shi) is Death and it is forced (Wood palace over Earth door — explicit 'Palace Oppressing Door'), with explicit 'Door Entering Tomb' on top. The chart's method-to-avoid is named, not inferred.
  - evidence: `chart_info.zhi_shi`, `palaces.xun_4.door`, `palaces.xun_4.inauspicious_patterns[1]`, `palaces.xun_4.inauspicious_patterns[0]`
- **CLM-016** [chart_hidden_problems_candidate · SUPPORT · HIGH · EXPLICIT · live] The day stem is entombed and punished here: marker 'Tomb & Punishment (Ren)', tomb field 'Xin Ren (Chen, Xun 4, Si)', punishment field 'Ren Gui (Chen, Xun 4, Si)'; Ren water tomb at Chen is computed-validated in-palace. The querent's own stem is buried in the B4 forward-trace palace.
  - evidence: `palaces.xun_4.special_markers[1]`, `palaces.xun_4.tomb`, `palaces.xun_4.punishment`, `state:marker_validation.tomb`, `chart_info.ganzhi.day`
- **CLM-017** [chart_best_solution_candidate · VETO · MED · EXPLICIT · live] Counterfeit promise inside the trap (split claim, not averaged): sanqi Yi on heaven, explicit 'Wonder Instrument Combination' (Yi+Geng co-located) and 'Three Wonders Obtaining Mission', Nine Heavens deity, and the Horse — yet the same Geng earth controls Yi, 'Three Wonders Being Restricted' is explicit, door is Death at Rest, palace Dead/Outer. The glittering path is the locked path.
  - evidence: `palaces.xun_4.auspicious_patterns[0]`, `palaces.xun_4.auspicious_patterns[1]`, `palaces.xun_4.inauspicious_patterns[2]`, `palaces.xun_4.heaven_stem`, `palaces.xun_4.earth_stem`, `palaces.xun_4.deity`, `palaces.xun_4.prosperity_decline.palace_state`
- **CLM-018** [timing · WARN · MED · COMPUTED · live] The hour's fastest vector leads into the obstruction cluster: hour horse Si is validated in Xun 4 — movement this hour runs toward the Death-door palace.
  - evidence: `chart_info.horse.hour`, `palaces.xun_4.special_markers[0]`, `state:marker_validation.horse`
- **CLM-019** [risk · CONSTRAIN · MED · COMPUTED · live] As B4 (opposite of the hour focus), Xun 4 is the board's 'if-you-proceed blind' check; whatever the execution seat (Qian 6) starts, this palace is its overshoot risk.
  - evidence: `state:origin_sets.B4.primary_set`, `state:origin_sets.B4.proxy_hits[0]`

## Relations (computed)
- *stem_combination* — Yi+Geng form a five-combination (heaven/earth plates of palace 4) (`palaces.xun_4.heaven_stem`, `palaces.xun_4.earth_stem`)
- *control* — Geng metal controls Yi wood (`palaces.xun_4.heaven_stem`, `palaces.xun_4.earth_stem`)
- *generation_drain* — Yi wood generates Ren — upper layer drains into lower (`palaces.xun_4.heaven_stem`, `palaces.xun_4.hidden_stem`)
- *door_forced* — palace Wood controls door Death (Earth) — forced door (palace oppressing door) (`palaces.xun_4.door`, `state:palace_key_resolution.palaces.4.element`)
- *star_home_displacement* — Tian Zhu home palace 7, seated in 4 — DISPLACED (`palaces.xun_4.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Death away from original (Du Door) (`palaces.xun_4.door`, `palaces.xun_4.original_position.door`)
- *branch_six_combination* — palace branch Chen six-combines month pillar branch You (`chart_info.ganzhi.month`, `state:palace_key_resolution.palaces.4.branches`)
- *stacked_pillar_branch_on_palace* — day pillar branch Chen stacked on palace 4 (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.4.branches`)
- *branch_clash* — palace branch Si clashes hour pillar branch Hai (Si-Hai clash) (`chart_info.ganzhi.hour`, `state:palace_key_resolution.palaces.4.branches`)
- *day_element_vs_palace* — day element Water vs palace element Wood: day produces palace (outflow) (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.4.element`)
- *horse_star* — hour horse (Si) in palace 4 (`chart_info.horse.hour`, `state:palace_key_resolution.palaces.4.branches`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_4.json`