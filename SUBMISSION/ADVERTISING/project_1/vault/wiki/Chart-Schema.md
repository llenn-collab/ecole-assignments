---
id: chart-schema
type: article
palace_ids: []
phase: PACKAGE_RENDER
batch: -
sources: ["raw/QMDJ.json", "raw/state/chart_analysis_package.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# Chart Schema

This chart does not use the field names the analyst specification expects. It is a *Yi Yun - Lun Zang Jia* hour-rotation export whose keys had to be bound by a least-contradicted mapping before any analysis could begin. That binding is recorded here so every later claim can be traced back to a real path in the source file.

## Infobox

| key | value |
|---|---|
| Source | `vault/raw/QMDJ.json` |
| sha256 | `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7` |
| Bytes | 10007 |
| Detected shape | `carpathia_yiyun_lunzangjia_v1` |
| Matches prompt default | False |
| Palaces | 9 |

## Bind map

| logical field | source path |
|---|---|
| afflictions | `palaces.{id}.active_chart.stems.afflictions` |
| birth_stage_stems | `palaces.{id}.palace_stem_rules.stems_in_birth_stage` |
| center_guest_stem | `palaces.{id}.active_chart.stems.center_guest` |
| chart_pattern | `chart_config.chart_pattern` |
| chart_structure | `chart_config.structure` |
| day_pillar | `timing.four_pillars.day` |
| day_void | `timing.voidness.day_void` |
| door | `palaces.{id}.active_chart.door` |
| door_strength | `palaces.{id}.active_chart.energy_state.door` |
| duty_door_name | `chart_config.duty_door` |
| duty_star_name | `chart_config.duty_star` |
| earth_stem | `palaces.{id}.active_chart.stems.earth` |
| god | `palaces.{id}.active_chart.god` |
| harm_stems | `palaces.{id}.palace_stem_rules.stems_in_harm` |
| heaven_stem | `palaces.{id}.active_chart.stems.heaven` |
| hidden_stem | `palaces.{id}.active_chart.stems.hidden` |
| hour_pillar | `timing.four_pillars.hour` |
| hour_void | `timing.voidness.hour_void` |
| lead_stem | `chart_config.lead_stem` |
| markers | `palaces.{id}.active_chart.status` |
| month_pillar | `timing.four_pillars.month` |
| palace_id | `object key as string 1-9` |
| palace_root | `palaces` |
| palace_strength | `palaces.{id}.active_chart.energy_state.palace` |
| punishment_stems | `palaces.{id}.palace_stem_rules.stems_in_clash_punishment` |
| realm | `palaces.{id}.active_chart.energy_state.realm` |
| seasonal | `element_prosperities` |
| solar_term | `timing.solar_term` |
| star | `palaces.{id}.active_chart.star` |
| star_strength_by_palace | `palaces.{id}.active_chart.energy_state.star.palace_relation` |
| star_strength_seasonal | `palaces.{id}.active_chart.energy_state.star.seasonal` |
| tomb_stems | `palaces.{id}.palace_stem_rules.stems_in_tomb` |
| year_pillar | `timing.four_pillars.year` |

## Named by the specification, absent here

- `chart_metadata.duty_elements.tian_yi`
- `heaven_plate.lodged_star`
- `heaven_plate.lodged_stem`
- `heaven_plate.notes`
- `door.forced`
- `markers.hour_stem_focus`
- `markers.plate_in_tomb`
- `markers.plate_in_punishment`
- `chart_metadata.palace_order`
- `explicit my_answers / hidden_problems / best_solution / yongshen fields`

Because these fields are absent, no claim in this package depends on them. In particular there is no explicit answer, hidden-problem, best-solution or yongshen field anywhere in the chart, so every headline below is COMPUTED, never EXPLICIT.

## Unknown keys kept as evidence

- `system.school`
- `system.chart_type`
- `system.method`
- `timing.solar_term.yuan`
- `timing.solar_term.day`
- `base_position.trigram_numbers`
- `base_position.hetu_numbers`
- `base_position.early_heaven_trigram`
- `base_position.home_god`
- `base_position.home_door`
- `base_position.home_star`
- `palace_stem_rules.stems_in_harm`
- `palace_stem_rules.stems_in_birth_stage`
- `active_chart.note`
- `active_chart.energy_state.realm`
- `active_chart.stems.center_guest`

## See also

- [[Chart-Anatomy]]
- [[MOC]]

## Sources

- `vault/raw/chart/schema.md`
- `vault/raw/state/schema_bind.json`

