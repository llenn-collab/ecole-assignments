---
id: "palace-8"
type: "palace-card"
phase: "B5"
batch: "B5"
palace_ids: ["8"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 8 — Gen (艮), Northeast, Earth · batch B5

**Raw key:** `gen_8` · **Ring:** outer · **Branches:** Ox (Chou), Tiger (Yin)
**Roles:** hour_void_member (Yin) · Du_blockage_seat · Ding_tomb · Oppression (door over palace) · Flying_Snake_loops · outer_ring · storage_not_launch

## Plates
- Heaven stem: `Ding` · Earth stem: `Bing` · Hidden stem: `Geng`
- Star: `Heaven Ying` · Door: `Du` · Deity: `Flying Snake`
- Markers: ["Void", "Tomb (Ding)", "Oppression"]
- Auspicious (explicit): []
- Inauspicious (explicit): ["Ding Wonder Entering Tomb", "Door Oppressing Palace"]
- Prosperity/decline: {"door_strength": "Dead", "star_strength": "Prosperous / Rest", "palace_state": "Rest / Outer"}
- **Absent leaf fields** (registry): `auspicious_patterns`

## Verdicts (typed, leaf-cited)
- **CLM-027** [chart_hidden_problems_candidate · SUPPORT · MED · EXPLICIT · live] Gen 8 is a stalled-storage node: Du (blockage) door at Dead, hour-void Yin in-palace, explicit 'Tomb (Ding)' and 'Ding Wonder Entering Tomb' — sanqi Yin Fire Ding on heaven entombed at Chou — plus 'Oppression' (door Wood over palace Earth, computed-confirmed) and Flying Snake anxiety loops. Drafts, archives and slow assets jam here.
  - evidence: `palaces.gen_8.door`, `palaces.gen_8.special_markers[0]`, `palaces.gen_8.special_markers[1]`, `palaces.gen_8.special_markers[2]`, `palaces.gen_8.inauspicious_patterns[0]`, `palaces.gen_8.inauspicious_patterns[1]`, `palaces.gen_8.deity`, `palaces.gen_8.tomb`
- **CLM-028** [chart_best_solution_candidate · VETO · LOW · EXPLICIT · live] No escape via Gen 8: the star is strong at the palace token (Prosperous) but Rest at climate token, the door is dead and the wonder is entombed — storage, not launch.
  - evidence: `palaces.gen_8.prosperity_decline.star_strength`, `palaces.gen_8.prosperity_decline.door_strength`

## Relations (computed)
- *control* — Ding fire controls Geng metal (`palaces.gen_8.heaven_stem`, `palaces.gen_8.hidden_stem`)
- *door_oppressing_palace* — door Du (Wood) controls palace Earth — door oppressing palace (`palaces.gen_8.door`, `state:palace_key_resolution.palaces.8.element`)
- *star_home_displacement* — Tian Ying home palace 9, seated in 8 — DISPLACED (`palaces.gen_8.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Du away from original (Life Door) (`palaces.gen_8.door`, `palaces.gen_8.original_position.door`)
- *branch_six_combination* — palace branch Yin six-combines hour pillar branch Hai (`chart_info.ganzhi.hour`, `state:palace_key_resolution.palaces.8.branches`)
- *day_element_vs_palace* — day element Water vs palace element Earth: palace controls day (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.8.element`)
- *horse_star* — day horse (Yin) in palace 8 (`chart_info.horse.day`, `state:palace_key_resolution.palaces.8.branches`)
- *void_palace* — palace 8 void: day-void —, hour-void ['Yin'] (`chart_info.void.day`, `chart_info.void.hour`, `state:palace_key_resolution.palaces.8.branches`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_8.json`