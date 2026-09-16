---
id: "palace-3"
type: "palace-card"
phase: "B1"
batch: "B1"
palace_ids: ["3"]
sources:
  - "raw/state/path_coverage_manifest.json"
  - "raw/state/indexes.json"
  - "raw/chart/dump.md"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "verdicted"
---


# Palace 3 — Zhen (震), East, Wood · batch B1

**Raw key:** `zhen_3` · **Ring:** outer · **Branches:** Rabbit (Mao)
**Roles:** day_stem_origin · B1_primary · duty_star_palace · lead_stem_proxy (Ren) · Chief_deity_seat (zhi_fu cross-check) · hour_void_member · outer_ring · day_element_outflow (Water->Wood)

## Plates
- Heaven stem: `Ren` · Earth stem: `Xin` · Hidden stem: `Ding`
- Star: `Heaven Rui & Heaven Qin` · Door: `Scenery` · Deity: `Chief`
- Markers: ["Void"]
- Auspicious (explicit): ["Palace Generating Door"]
- Inauspicious (explicit): []
- Prosperity/decline: {"door_strength": "Imprisoned", "star_strength": "Imprisoned / Prosperous", "palace_state": "Dead / Outer"}
- **Absent leaf fields** (registry): `inauspicious_patterns`, `tomb`

## Verdicts (typed, leaf-cited)
- **CLM-001** [chart_answers_candidate · SUPPORT · HIGH · EXPLICIT · live] The chart's answer-locus is Zhen 3: day stem Ren (querent/day seat) sits on the heaven plate here — the only heaven-plate hit for the day stem — so B1 resolves to a single palace by value match.
  - evidence: `chart_info.ganzhi.day`, `palaces.zhen_3.heaven_stem`, `state:origin_sets.B1.heaven_hits`
- **CLM-002** [chart_answers_candidate · SUPPORT · HIGH · EXPLICIT · live] Authority converges on the same seat: fu_tou 'Jia Chen Ren' hides the leader Jia under Ren (the day stem itself), duty star Tian Rui (zhi_fu) lands in Zhen 3, the palace star field carries 'Heaven Rui & Heaven Qin', and the Chief deity occupies this palace. No competing candidate found for the answer seat.
  - evidence: `chart_info.fu_tou`, `chart_info.zhi_fu`, `palaces.zhen_3.star`, `palaces.zhen_3.deity`
- **CLM-003** [timing · WARN · HIGH · EXPLICIT · live] The answer palace is hour-void: palace branch Mao is in the hour void 'Yin Mao' (explicit marker Void; computed xun check agrees). The matter at the answer seat does not land until the void fills (Mao day/hour).
  - evidence: `chart_info.void.hour`, `palaces.zhen_3.special_markers[0]`, `state:marker_validation.void`
- **CLM-004** [risk · CONSTRAIN · MED · EXPLICIT · live] Method at the answer seat constricted: Scenery door is Imprisoned, palace state is Dead/Outer, star strength is split (Imprisoned / Prosperous tokens) — an outwardly visible showpiece over an exhausted core process.
  - evidence: `palaces.zhen_3.prosperity_decline.door_strength`, `palaces.zhen_3.prosperity_decline.star_strength`, `palaces.zhen_3.prosperity_decline.palace_state`, `palaces.zhen_3.door`
- **CLM-005** [risk · WARN · MED · EXPLICIT · live] Self-inflicted drag at the answer seat: the harm field names the day stem itself (Ren) at Mao/Zhen 3, and the punishment field names Wu — the querent's own execution mis-steps are the damage vector, not an external enemy.
  - evidence: `palaces.zhen_3.harm`, `palaces.zhen_3.punishment`, `chart_info.ganzhi.day`
- **CLM-006** [timing · SEQUENCE · MED · COMPUTED · live] Support reaches the answer through covered channels: earth Xin metal generates heaven Ren water, and hidden Ding forms a Ding-Ren combination under the day stem — private agreements/resources feed the seat; the visible show (Scenery) is not the feed.
  - evidence: `palaces.zhen_3.earth_stem`, `palaces.zhen_3.hidden_stem`, `palaces.zhen_3.heaven_stem`

## Relations (computed)
- *generation_drain* — Ren water generates Xin — upper layer drains into lower (`palaces.zhen_3.heaven_stem`, `palaces.zhen_3.earth_stem`)
- *stem_combination* — Ren+Ding form a five-combination (heaven/hidden of palace 3) (`palaces.zhen_3.heaven_stem`, `palaces.zhen_3.hidden_stem`)
- *control* — Ren water controls Ding fire (`palaces.zhen_3.heaven_stem`, `palaces.zhen_3.hidden_stem`)
- *palace_generating_door* — palace Wood generates door Scenery (Fire) (`palaces.zhen_3.door`, `state:palace_key_resolution.palaces.3.element`)
- *star_home_displacement* — Tian Rui home palace 2, seated in 3 — DISPLACED (`palaces.zhen_3.star`, `state:frozen_tables.star_home_luoshu`)
- *star_home_displacement* — Tian Qin home palace 5, seated in 3 — DISPLACED (`palaces.zhen_3.star`, `state:frozen_tables.star_home_luoshu`)
- *door_at_original_palace* — door Scenery away from original (Wound Door) (`palaces.zhen_3.door`, `palaces.zhen_3.original_position.door`)
- *branch_clash* — palace branch Mao clashes month pillar branch You (Mao-You clash) (`chart_info.ganzhi.month`, `state:palace_key_resolution.palaces.3.branches`)
- *day_element_vs_palace* — day element Water vs palace element Wood: day produces palace (outflow) (`chart_info.ganzhi.day`, `state:palace_key_resolution.palaces.3.element`)
- *void_palace* — palace 3 void: day-void —, hour-void ['Mao'] (`chart_info.void.day`, `chart_info.void.hour`, `state:palace_key_resolution.palaces.3.branches`)

See also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_3.json`