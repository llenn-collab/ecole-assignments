---
id: "palace-6"
type: "palace-card"
phase: "B2"
batch: "B2"
palace_ids: ["6"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 6 — Qian (乾), Northwest, Metal · batch B2

**Raw key:** `qian_6` · **Ring:** inner · **Branches:** Dog (Xu), Pig (Hai)
**Roles:** hour_stem_focus · B2_primary · tian_yi_star_seat (Tian Chong) · month_horse · Six_Harmony_seat · inner_ring · clash_to_day_branch (Xu~Chen) · tomb_of_earth_stem (Wu)

## Plates
- Heaven stem: `Xin` · Earth stem: `Wu` · Hidden stem: `Bing`
- Star: `Heaven Chong` · Door: `Life` · Deity: `Six Harmony`
- Markers: ["Tomb (Wu)"]
- Auspicious (explicit): ["Door Generating Palace"]
- Inauspicious (explicit): []
- Prosperity/decline: {"door_strength": "Rest", "star_strength": "Imprisoned / Imprisoned", "palace_state": "Prosperous / Inner"}
- **Absent leaf fields** (registry): `inauspicious_patterns`, `life_stage`, `punishment`

## Verdicts (typed, leaf-cited)
- **CLM-007** [timing · SUPPORT · HIGH · EXPLICIT · live] The execution/timing seat is Qian 6: hour stem Xin on heaven, hour branch Hai resident in palace, and the month horse also lands here — hour focus, hour root and mover coincide in one palace.
  - evidence: `chart_info.ganzhi.hour`, `palaces.qian_6.heaven_stem`, `chart_info.horse.month`, `state:marker_validation.horse`
- **CLM-008** [chart_best_solution_candidate · SUPPORT · MED · EXPLICIT · live] Help/quality pole confirmed at Qian 6: Life door with explicit 'Door Generating Palace', Six Harmony deity (pacts, alignment), and the chart's Tian Yi (Tian Chong) star seated here; hidden Bing under heaven Xin adds a Bing-Xin combination — a binding pact under the help seat.
  - evidence: `chart_info.tian_yi`, `palaces.qian_6.star`, `palaces.qian_6.door`, `palaces.qian_6.deity`, `palaces.qian_6.auspicious_patterns[0]`, `palaces.qian_6.hidden_stem`
- **CLM-009** [risk · CONSTRAIN · MED · EXPLICIT · live] The help engine runs cool: star strength is Imprisoned/Imprisoned (concordant weak), door at Rest, explicit Tomb (Wu) marker, and the tomb field buries Yi, Bing and Wu — including the palace's own earth stem Wu. Support exists but is buried/late: institutional or backstage delivery.
  - evidence: `palaces.qian_6.prosperity_decline.star_strength`, `palaces.qian_6.prosperity_decline.door_strength`, `palaces.qian_6.special_markers[0]`, `palaces.qian_6.tomb`
- **CLM-010** [risk · WARN · MED · COMPUTED · live] Structural jolt: palace branch Xu clashes the day branch Chen — activating the help/harmony palace shakes the day's own root; expect the backing to arrive with friction against current commitments.
  - evidence: `chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.6.branches`, `state:relations.palace_6.branch_clash`

## Relations (computed)
- *generation_drain* — Xin metal generates Wu — upper layer drains into lower (`palaces.qian_6.heaven_stem`, `palaces.qian_6.earth_stem`)
- *stem_combination* — Xin+Bing form a five-combination (heaven/hidden of palace 6) (`palaces.qian_6.heaven_stem`, `palaces.qian_6.hidden_stem`)
- *control* — Bing fire controls Xin metal (`palaces.qian_6.heaven_stem`, `palaces.qian_6.hidden_stem`)
- *door_generating_palace* — door Life (Earth) generates palace Metal (`palaces.qian_6.door`, `state:palace_key_resolution.palaces.6.element`)
- *star_home_displacement* — Tian Chong home palace 3, seated in 6 — DISPLACED (`palaces.qian_6.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Life away from original (Open Door) (`palaces.qian_6.door`, `palaces.qian_6.original_position.door`)
- *branch_clash* — palace branch Xu clashes day pillar branch Chen (Chen-Xu clash) (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.6.branches`)
- *stacked_pillar_branch_on_palace* — hour pillar branch Hai stacked on palace 6 (`chart_info.ganzhi.hour`, `state:palace_key_resolution.palaces.6.branches`)
- *day_element_vs_palace* — day element Water vs palace element Metal: palace produces day (inflow) (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.6.element`)
- *horse_star* — month horse (Hai) in palace 6 (`chart_info.horse.month`, `state:palace_key_resolution.palaces.6.branches`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_6.json`