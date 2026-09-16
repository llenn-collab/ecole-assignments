---
id: "palace-5"
type: "palace-card"
phase: "B5"
batch: "B5"
palace_ids: ["5"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 5 — Center (中), Center, Earth · batch B5

**Raw key:** `center_5` · **Ring:** inner · **Branches:** —
**Roles:** center_pivot · NO_OPPOSITE · displaced_core (Ji + Tian Qin lodged) · life_stage_seed (Changsheng) · placeholder_relation_fields

## Plates
- Heaven stem: `Ji (lodged in Zhen 3 Palace)` · Earth stem: `Ji` · Hidden stem: `Ji (lodged in Kun 2 Palace)`
- Star: `Heaven Qin (lodged in Zhen 3 Palace)` · Door: `None` · Deity: `Tai Chang`
- Markers: []
- Auspicious (explicit): []
- Inauspicious (explicit): []
- Prosperity/decline: {"palace_state": "Rest"}
- **Absent leaf fields** (registry): `door`, `special_markers`, `auspicious_patterns`, `inauspicious_patterns`, `original_position.deity`, `original_position.door`, `original_position.branches`, `original_position.opposite_palace`, `prosperity_decline.door_strength`, `prosperity_decline.star_strength`

## Verdicts (typed, leaf-cited)
- **CLM-025** [chart_answers_candidate · CONSTRAIN · MED · EXPLICIT · live] The core is displaced: Center's heaven Ji and star Tian Qin are lodged into Zhen 3 (co-lodging confirmed in palace 3 star field), hidden Ji into Kun 2. Center owns no door, no branches, no direction — the central matter is administered from its host palaces; read it through 3 and 2, not directly.
  - evidence: `palaces.center_5.heaven_stem`, `palaces.center_5.star`, `palaces.center_5.hidden_stem`, `palaces.zhen_3.star`, `state:lodging.graph`
- **CLM-026** [chart_answers_candidate · SUPPORT · LOW · EXPLICIT · live] Life-stage seed: Center's life_stage reads 'Changsheng (Longevity)' — the displaced core keeps a generative seed; its Harm/Tomb/Punishment fields are placeholder labels only (logged as anomalies, no content).
  - evidence: `palaces.center_5.life_stage`, `palaces.center_5.harm`, `palaces.center_5.tomb`, `palaces.center_5.punishment`

## Relations (computed)
- *star_home_displacement* — Heaven Qin (lodged in Zhen 3 Palace) home palace None, seated in 5 — DISPLACED (`palaces.center_5.star`, `state:frozen_tables.star_home_luoshu`)
- *day_element_vs_palace* — day element Water vs palace element Earth: palace controls day (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.5.element`)

## Anomalies touching this palace
- **ANO-001** [PLACEHOLDER_LABEL_VALUE] center_5.harm is 'Harm': category label, no stem/branch content
- **ANO-002** [PLACEHOLDER_LABEL_VALUE] center_5.tomb is 'Tomb': category label, no stem/branch content
- **ANO-003** [PLACEHOLDER_LABEL_VALUE] center_5.punishment is 'Punishment': category label, no stem/branch content

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_5.json`