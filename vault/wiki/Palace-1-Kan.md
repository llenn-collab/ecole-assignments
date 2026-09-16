---
id: "palace-1"
type: "palace-card"
phase: "B5"
batch: "B5"
palace_ids: ["1"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 1 — Kan (坎), North, Water · batch B5

**Raw key:** `kan_1` · **Ring:** outer · **Branches:** Rat (Zi)
**Roles:** Great_Barrier (Geng over Gui) · Shang_injury_door_dead · Great_Yin_cover · outer_ring · groundwork_track

## Plates
- Heaven stem: `Geng` · Earth stem: `Gui` · Hidden stem: `Xin`
- Star: `Heaven Fu` · Door: `Shang` · Deity: `Great Yin`
- Markers: []
- Auspicious (explicit): ["Palace Generating Door"]
- Inauspicious (explicit): ["Great Barrier"]
- Prosperity/decline: {"door_strength": "Dead", "star_strength": "Discarded / Imprisoned", "palace_state": "Strong / Outer"}
- **Absent leaf fields** (registry): `special_markers`, `harm`, `tomb`, `punishment`

## Verdicts (typed, leaf-cited)
- **CLM-020** [chart_hidden_problems_candidate · SUPPORT · MED · EXPLICIT · live] Kan 1 holds the explicit 'Great Barrier' (both pieces exist: heaven Geng, earth Gui) with Shang (injury) door at Dead and star Discarded/Imprisoned under Great Yin — a hard barrier on the groundwork/water track; stalled starts and injurious grind without yield.
  - evidence: `palaces.kan_1.inauspicious_patterns[0]`, `palaces.kan_1.heaven_stem`, `palaces.kan_1.earth_stem`, `palaces.kan_1.door`, `palaces.kan_1.prosperity_decline.star_strength`, `palaces.kan_1.prosperity_decline.door_strength`, `palaces.kan_1.deity`
- **CLM-021** [risk · CONSTRAIN · LOW · EXPLICIT · live] Barrier is intermittent, not terminal: explicit 'Palace Generating Door' and palace state Strong/Outer mean the season still feeds the effort — grind returns poorly now, but the foundation is not dead.
  - evidence: `palaces.kan_1.auspicious_patterns[0]`, `palaces.kan_1.prosperity_decline.palace_state`

## Relations (computed)
- *generation* — Gui water generates Geng metal — plate feeds from below (`palaces.kan_1.heaven_stem`, `palaces.kan_1.earth_stem`)
- *palace_generating_door* — palace Water generates door Shang (Wood) (`palaces.kan_1.door`, `state:palace_key_resolution.palaces.1.element`)
- *star_home_displacement* — Tian Fu home palace 4, seated in 1 — DISPLACED (`palaces.kan_1.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Shang away from original (Rest Door) (`palaces.kan_1.door`, `palaces.kan_1.original_position.door`)
- *branch_clash* — palace branch Zi clashes year pillar branch Wu (Zi-Wu clash) (`chart_info.ganzhi.year`, `state:palace_key_resolution.palaces.1.branches`)
- *day_element_vs_palace* — day element Water vs palace element Water: same element kin (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.1.element`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_1.json`