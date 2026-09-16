---
id: "chart-anatomy"
type: "article"
phase: "P0_ANATOMY"
batch: "—"
palace_ids: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
sources:
  - "raw/state/pillars.json"
  - "raw/state/season.json"
  - "raw/state/duty.json"
  - "raw/state/origin_sets.json"
  - "raw/state/lodging.json"
  - "raw/state/marker_validation.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Anatomy

## Four pillars (parsed from combined Ganzhi strings)
| pillar | raw | stem | branch | stem element | void membership | branch palace |
|---|---|---|---|---|---|---|
| year | Bing Wu | Bing (Yang Fire) | Wu (Horse) | Fire | DAY-VOID | 9 |
| month | Ding You | Ding (Yin Fire) | You (Rooster) | Fire | — | 7 |
| day | Ren Chen | Ren (Yang Water) | Chen (Dragon) | Water | — | 4 |
| hour | Xin Hai | Xin (Yin Metal) | Hai (Pig) | Metal | — | 6 |

Pillar relations (computed):
- `stem_combination` ['Bing', 'Xin'] across pillars ['year', 'hour'] (evidence: `chart_info.ganzhi.year`, `chart_info.ganzhi.hour`)
- `stem_combination` ['Ding', 'Ren'] across pillars ['month', 'day'] (evidence: `chart_info.ganzhi.month`, `chart_info.ganzhi.day`)
- `branch_six_combination` ['Chen', 'You'] across pillars ['month', 'day'] (evidence: `chart_info.ganzhi.month`, `chart_info.ganzhi.day`)
- day void metadata `['Wu', 'Wei']` == computed `['Wu', 'Wei']` → **validated**
- hour void metadata `['Yin', 'Mao']` == computed `['Yin', 'Mao']` → **validated**

## Season (raw terms preserved; normalization computed)
| element | raw | normalized |
|---|---|---|
| earth | Resting | resting (computed_mapping) |
| fire | Imprisoned | trapped (computed_mapping) |
| metal | Prosperous | prosperous (computed_mapping) |
| water | Strong | strengthening (computed_mapping) |
| wood | Dead | dead (computed_mapping) |

## Duty & authority
- **fu_tou**: `Jia Chen Ren` → xun leader Jia Chen, yi stem **Ren** (frozen table check: True); Jia concealed under Ren → **Ren is the visible stand-in for the invisible leader Jia**
- **zhi_fu (duty star)**: Tian Rui falling in Zhen 3 Palace → Tian Rui, home 2, active **3**; cross-check in palace star field: {"contains_duty_star": true, "path": "palaces.zhen_3.star", "value": "Heaven Rui & Heaven Qin"}
- **zhi_shi (duty door)**: Death Door falling in Xun 4 Palace → Death, original 2, active **4** (displacement logged); door field cross-check: {"matches": true, "path": "palaces.xun_4.door", "value": "Death"}
- **tian_yi**: Tian Chong → Tian Chong seated in palace 6 (`palaces.qian_6.star`)
- **Chief deity** cross-validates duty star seat: {"matches_duty_star_palace": true, "note": "Chief deity seat cross-validates zhi_fu landing", "palaces": ["3"]}

## Origin sets (selectors are sets — resolved by value match)
- **B1** (day stem trace): ['3'] — day stem Ren on heaven `palaces.zhen_3.heaven_stem`; proxies: lead Ren → ['3'], duty_star palace → ['3'], tomb_of_day_gan → ['4'], earth_or_hidden → ['2', '4']
- **B2** (hour focus): ['6'] (+ hour branch → ['6'], hour horse → ['4'] as trace)
- **B3** (opposite of B1): ['7'] — cost/check
- **B4** (opposite of B2): ['4'] — forward/if-proceed check
- **B5** (remaining, Luo Shu order): ['1', '2', '5', '8', '9']
- Jia on heaven: **false by construction** (Dun Jia); Jia (leader) invisible on plate by Dun Jia construction; lead proxy = Ren via fu_tou Jia Chen Ren; Jia references: [{"palace": "2", "path": "palaces.kun_2.tomb", "role": "tomb_field"}]

## Center lodging graph (Center stays NO_OPPOSITE pivot)
- Ji (heaven_stem) lodged from palace 5 → **3** (`palaces.center_5.heaven_stem`; host confirmation: {"note": "lodged heaven stem rides with host palace"}…)
- Ji (hidden_stem) lodged from palace 5 → **2** (`palaces.center_5.hidden_stem`; host confirmation: {"found_in_host_hidden_field": false, "note": "host palace keeps its own hidden stem; lodger co-resides (not echoed) \u2…)
- Heaven Qin (star) lodged from palace 5 → **3** (`palaces.center_5.star`; host confirmation: {"found_in_host_star_field": true, "path": "palaces.zhen_3.star", "value": "Heaven Rui & Heaven Qin"}…)

## Marker validation (explicit markers vs computed)
- Void: [["2", "VALIDATED"], ["3", "VALIDATED"], ["8", "VALIDATED"], ["9", "VALIDATED"]]
- Horse: computed palaces ['2', '4', '6', '8'] — [["2", "COMPUTED_ONLY_no_marker_is_not_false"], ["6", "COMPUTED_ONLY_no_marker_is_not_false"], ["8", "COMPUTED_ONLY_no_marker_is_not_false"], ["4", "VALIDATED"]]
- Tomb checks: [["2", "Gui", "Wei", true], ["4", "Ren", "Chen", true], ["6", "Wu", "Xu", true], ["8", "Ding", "Chou", true], ["2", "Jia", "Wei", true], ["2", "Gui", "Wei", true], ["4", "Xin", "Chen", true], ["4", "Ren", "Chen", true], ["6", "Yi", "Xu", true], ["6", "Bing", "Xu", true], ["6", "Wu", "Xu", true], ["8", "Ding", "Chou", true], ["8", "Ji", "Chou", true], ["8", "Geng", "Chou", true]]
- Mismatches (recorded, not suppressed): [{"note": "absence of marker != absence of horse; computed horse recorded", "palace": "2", "type": "computed_horse_no_marker"}, {"note": "absence of marker != absence of horse; computed horse recorded", "palace": "6", "type": "computed_horse_no_marker"}, {"note": "absence of marker != absence of horse; computed horse recorded", "palace": "8", "type": "computed_horse_no_marker"}]
- Oppression validation: [["8", "Du", true]]
- Liu-Yi punishment validation (classical table): [["2", "Ji", true], ["3", "Wu", true], ["4", "Ren", true], ["4", "Gui", true], ["8", "Geng", true], ["9", "Xin", true], ["4", "Ren", true]] — all entries match Wu@3/Ji@2/Geng@8/Xin@9/Ren@4/Gui@4
- Name-key consistency: [["1", true], ["2", true], ["3", true], ["4", true], ["5", true], ["6", true], ["7", true], ["8", true], ["9", true]]

See also: [[Chart-Working-Copy]] · [[Palace-Analysis-Index]] · [[MOC]]