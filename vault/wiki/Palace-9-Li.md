---
id: "palace-9"
type: "palace-card"
phase: "B5"
batch: "B5"
palace_ids: ["9"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 9 — Li (离), South, Fire · batch B5

**Raw key:** `li_9` · **Ring:** inner · **Branches:** Horse (Wu)
**Roles:** year_branch_stacked (Wu) · day_void_member · Scenery_at_original_palace · explicit_pattern_conflict (Palace Oppressing Door) · inner_ring · showcase_layer

## Plates
- Heaven stem: `Wu` · Earth stem: `Ding` · Hidden stem: `Yi`
- Star: `Heaven Heart` · Door: `Scenery` · Deity: `Nine Earths`
- Markers: ["Void"]
- Auspicious (explicit): ["Wonder Wandering Salary Position"]
- Inauspicious (explicit): ["Palace Oppressing Door"]
- Prosperity/decline: {"door_strength": "Prosperous", "star_strength": "Imprisoned / Strong", "palace_state": "Imprisoned / Inner"}
- **Absent leaf fields** (registry): `harm`, `tomb`

## Verdicts (typed, leaf-cited)
- **CLM-029** [chart_hidden_problems_candidate · SUPPORT · HIGH · EXPLICIT · live] The showcase layer is void this cycle: Li 9 holds the year-pillar branch Wu stacked in-palace, and Wu is in the day void 'Wu Wei' (explicit Void marker; computed-validated). The public-facing surface of the year's frame does not land as presented; palace state Imprisoned/Inner with seasonal fire Imprisoned compounds it.
  - evidence: `palaces.li_9.special_markers[0]`, `chart_info.void.day`, `chart_info.ganzhi.year`, `palaces.li_9.prosperity_decline.palace_state`, `chart_info.seasonal_strength.fire`
- **CLM-030** [risk · WARN · MED · ANOMALOUS · live] Explicit-vs-computed conflict at Li 9: the chart explicitly lists 'Palace Oppressing Door', but computed elements show Fire palace with Fire door (Scenery, at its original palace) — no control relation exists. Both are preserved; the explicit pattern is flagged ANOMALOUS, not repaired.
  - evidence: `palaces.li_9.inauspicious_patterns[0]`, `palaces.li_9.door`, `palaces.li_9.original_position.door`, `state:relations.palace_9.door_palace_same_element`
- **CLM-031** [timing · SEQUENCE · MED · COMPUTED · live] The void fills on Wu: day-void Wu resolves when Wu day/hour arrives — visibility pushes land then, not before; scheduled showcases in the void window will underperform their billing.
  - evidence: `chart_info.void.day`, `chart_info.ganzhi.year`
- **CLM-032** [chart_best_solution_candidate · VETO · LOW · EXPLICIT · live] Li 9's 'Wonder Wandering Salary Position' (Ding's salary at Wu, earth stem Ding in-palace) reads as a real but void-locked pay-off: a genuine gains-channel that cannot be collected in the current window.
  - evidence: `palaces.li_9.auspicious_patterns[0]`, `palaces.li_9.earth_stem`, `palaces.li_9.special_markers[0]`

## Relations (computed)
- *generation_drain* — Wu earth generates Ding — upper layer drains into lower (`palaces.li_9.heaven_stem`, `palaces.li_9.earth_stem`)
- *control* — Yi wood controls Wu earth (`palaces.li_9.heaven_stem`, `palaces.li_9.hidden_stem`)
- *door_palace_same_element* — door Scenery and palace Fire share element (`palaces.li_9.door`, `state:palace_key_resolution.palaces.9.element`)
- *star_home_displacement* — Tian Xin home palace 6, seated in 9 — DISPLACED (`palaces.li_9.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Scenery sits its original palace (`palaces.li_9.door`, `palaces.li_9.original_position.door`)
- *stacked_pillar_branch_on_palace* — year pillar branch Wu stacked on palace 9 (`chart_info.ganzhi.year`, `state:palace_key_resolution.palaces.9.branches`)
- *day_element_vs_palace* — day element Water vs palace element Fire: day controls palace (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.9.element`)
- *void_palace* — palace 9 void: day-void ['Wu'], hour-void — (`chart_info.void.day`, `chart_info.void.hour`, `state:palace_key_resolution.palaces.9.branches`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_9.json`