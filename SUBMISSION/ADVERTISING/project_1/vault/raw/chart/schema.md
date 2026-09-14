# Chart Schema (discovered)

- source sha256: `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`
- bytes: 10007
- detected shape: `carpathia_yiyun_lunzangjia_v1`

## Top-level keys

- `chart_config` : dict
- `element_prosperities` : dict
- `palaces` : dict
- `system` : dict
- `timing` : dict

## Bind map (least-contradicted)

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

## Named by prompt, ABSENT in source

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
