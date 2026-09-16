---
id: "chart-schema"
type: "article"
phase: "CHART_INGEST"
batch: "—"
palace_ids: []
sources:
  - "raw/chart/schema.md"
  - "raw/state/schema_variant.json"
  - "raw/state/semantic_path_registry.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Schema

Detected variant: **project_1_chart_info_v1** (confidence 1.0). Match evidence:
- top_level_keys == {chart_info, palaces}
- palace_key_style == compound_trigram_number
- pillars are combined ganzhi strings (e.g. 'Ren Chen')
- duty fields are composite strings (e.g. 'Tian Rui falling in Zhen 3 Palace')
- markers/patterns are explicit string arrays
- strength fields composite (e.g. 'Rest / Strong')
- center palace lacks door/branches/opposite_palace

Unresolved ambiguities:
- star_strength two-token convention ('A / B') by_season vs by_palace order unverified; raw preserved, tokens normalized separately

## Semantic path registry (bind by role, never hardcoded)
| role | resolved path | status | parser |
|---|---|---|---|
| auspicious_patterns | `auspicious_patterns` | BOUND | True |
| chart_type | `chart_info.type` | BOUND | False |
| day_pillar | `chart_info.ganzhi.day` | BOUND | True |
| day_void | `chart_info.void.day` | BOUND | False |
| deity | `deity` | BOUND | False |
| door | `door` | BOUND | False |
| duty_door_active | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| duty_door_name | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| duty_door_original | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| duty_star_name | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| duty_star_palace | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| earth_stem | `earth_stem` | BOUND | False |
| fu_tou | `chart_info.fu_tou` | BOUND | True |
| gregorian | `chart_info.gregorian` | BOUND | False |
| harm | `harm` | BOUND | True |
| heaven_stem | `heaven_stem` | BOUND | True |
| hidden_stem | `hidden_stem` | BOUND | True |
| horse_day | `chart_info.horse.day` | BOUND | False |
| horse_hour | `chart_info.horse.hour` | BOUND | False |
| horse_month | `chart_info.horse.month` | BOUND | False |
| horse_year | `chart_info.horse.year` | BOUND | False |
| hour_pillar | `chart_info.ganzhi.hour` | BOUND | True |
| hour_void | `chart_info.void.hour` | BOUND | False |
| inauspicious_patterns | `inauspicious_patterns` | BOUND | True |
| ju | `chart_info.ju` | BOUND | False |
| lead_stem | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| life_stage | `life_stage` | BOUND | True |
| lodged_star | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| lodged_stem | `None` | ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol | True |
| lunar | `chart_info.lunar` | BOUND | False |
| metadata_root | `chart_info` | BOUND | False |
| method | `chart_info.method` | BOUND | False |
| month_pillar | `chart_info.ganzhi.month` | BOUND | True |
| original_position | `original_position` | BOUND | True |
| palace_identity | `object_key + name + original_position` | BOUND | False |
| palaces_root | `palaces` | BOUND | False |
| prosperity_decline | `prosperity_decline` | BOUND | True |
| punishment | `punishment` | BOUND | True |
| seasonal_strength | `chart_info.seasonal_strength` | BOUND | False |
| solar_term | `chart_info.solar_term` | BOUND | False |
| special_markers | `special_markers` | BOUND | True |
| star | `star` | BOUND | True |
| system | `chart_info.system` | BOUND | False |
| tian_yi | `chart_info.tian_yi` | BOUND | False |
| tomb | `tomb` | BOUND | True |
| year_pillar | `chart_info.ganzhi.year` | BOUND | True |
| zhi_fu | `chart_info.zhi_fu` | BOUND | True |
| zhi_shi | `chart_info.zhi_shi` | BOUND | True |

See also: [[Chart-Anatomy]] · [[MOC]]