---
id: palace-7
type: palace-card
phase: P5_REMAINING
batch: B5
palace_ids: ["7"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 7 - Dui (West)

> Metal palace | realm Inner | strength Prosperous | opposite 3

## Infobox

| field | value |
|---|---|
| Heaven stem | Gui |
| Earth stem | Gui |
| Hidden stem | Gui |
| Door | Jing (Fear) (Prosperous) |
| Star | Tian Zhu (Pillar) |
| Spirit | Jiu Di (Nine Earths) |
| Branches | You (Rooster) |
| Void | False |
| Horse star | False |
| Afflictions | Heavenly Net Spread |
| Tomb of | - |
| Punishment of | - |

## Roles

- **inner** - Realm as declared by the chart.
- **stacked_branch** - Pillar branch(es) ['month'] land here.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Gui | Gui | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Gui | Gui | IDENTICAL (Fu Yin) |
| stem_vs_palace | Gui | Metal | PRODUCED_BY |
| door_vs_palace | Jing (Fear) | Metal | SAME |
| star_vs_palace | Tian Zhu (Pillar) | Metal | SAME |
| star_vs_heaven_stem | Tian Zhu (Pillar) | Gui | PRODUCES |
| stem_vs_door | Gui | Jing (Fear) | PRODUCED_BY |
| stem_vs_season | Gui | seasonal_element_strengths | Strengthening |
| stem_vs_day_stem | Gui | Bing | CONTROLS |
| stem_combination_across_board | Gui | Wu | COMBINES -> Fire |
| stem_clash_across_board | Gui | Ding | CLASH |
| strength_concordance | 7 | Prosperous|Prosperous|Strengthening|Strengthening | SPLIT |

## Verdicts (S11)

### V040-P7 - chart_hidden_problems_candidate / WARN

Palace 7 carries the affliction 'Heavenly Net Spread'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.7.active_chart.stems.afflictions` = `Heavenly Net Spread`

### V041-P7 - chart_best_solution_candidate / SUPPORT

The Jing (Fear) door at palace 7 is Prosperous. This is a method the season actually supports.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.7.active_chart.energy_state.door` = `Prosperous`
- evidence: `palaces.7.active_chart.door` = `Jing (Fear)`
- evidence: `element_prosperities` = `Prosperous`

### V042-P7 - risk / CONSTRAIN

Palace 7 reads differently from different angles (Prosperous|Prosperous|Strengthening|Strengthening). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.7.active_chart.energy_state` = `Prosperous|Prosperous|Strengthening|Strengthening`

### V043-P7 - risk / CONSTRAIN

Palace 7 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.7.active_chart.star` = `['Tian Zhu (Pillar)']`
- evidence: `palaces.7.active_chart.door` = `Jing (Fear)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
