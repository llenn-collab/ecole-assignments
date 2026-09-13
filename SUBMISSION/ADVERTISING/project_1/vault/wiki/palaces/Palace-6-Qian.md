---
id: palace-6
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B1
palace_ids: ["6"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 6 - Qian (Northwest)

> Metal palace | realm Inner | strength Prosperous | opposite 4

## Infobox

| field | value |
|---|---|
| Heaven stem | Ding |
| Earth stem | Ding |
| Hidden stem | Ding |
| Door | Kai (Open) (Prosperous) |
| Star | Tian Xin (Heart) |
| Spirit | Xuan Wu (Black Tortoise) |
| Branches | Xu (Dog), Hai (Pig) |
| Void | False |
| Horse star | False |
| Afflictions | - |
| Tomb of | Yi, Bing, Wu |
| Punishment of | - |

## Roles

- **day_stem_or_jia_set** - Selected by the day-stem origin set.
- **tomb_of_yongshen** - Entombs the day stem.
- **inner** - Realm as declared by the chart.
- **stacked_branch** - Pillar branch(es) ['day'] land here.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Ding | Ding | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Ding | Ding | IDENTICAL (Fu Yin) |
| stem_vs_palace | Ding | Metal | CONTROLS |
| door_vs_palace | Kai (Open) | Metal | SAME |
| star_vs_palace | Tian Xin (Heart) | Metal | SAME |
| star_vs_heaven_stem | Tian Xin (Heart) | Ding | CONTROLLED_BY |
| stem_vs_door | Ding | Kai (Open) | CONTROLS |
| stem_vs_season | Ding | seasonal_element_strengths | Imprisoned |
| stem_vs_day_stem | Ding | Bing | SAME |
| stem_combination_across_board | Ding | Ren | COMBINES -> Wood |
| stem_clash_across_board | Ding | Gui | CLASH |
| strength_concordance | 6 | Prosperous|Prosperous|Strengthening|Strengthening | SPLIT |

## Verdicts (S11)

### V012-P6 - chart_best_solution_candidate / SUPPORT

The Kai (Open) door at palace 6 is Prosperous. This is a method the season actually supports.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.6.active_chart.energy_state.door` = `Prosperous`
- evidence: `palaces.6.active_chart.door` = `Kai (Open)`
- evidence: `element_prosperities` = `Prosperous`

### V013-P6 - chart_best_solution_candidate / SUPPORT

Palace 6 holds the San Qi stem Ding. Quality, reputation and visibility are concentrated here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.6.active_chart.stems.heaven` = `Ding`
- evidence: `element_prosperities` = `Imprisoned`

### V014-P6 - chart_hidden_problems_candidate / CONSTRAIN

The stem Ding (Fire) at palace 6 is Imprisoned this season. The climate does not support it however good it looks on the board.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.6.active_chart.stems.heaven` = `Ding`
- evidence: `element_prosperities` = `Imprisoned`

### V015-P6 - chart_hidden_problems_candidate / VETO

Palace 6 is the tomb of the day stem Bing. Committing the self here buries it: effort goes in and does not come back out.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.6.palace_stem_rules.stems_in_tomb` = `Bing`
- evidence: `timing.four_pillars.day` = `Bing-Xu`

### V016-P6 - risk / CONSTRAIN

Palace 6 reads differently from different angles (Prosperous|Prosperous|Strengthening|Strengthening). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.6.active_chart.energy_state` = `Prosperous|Prosperous|Strengthening|Strengthening`

### V017-P6 - risk / CONSTRAIN

Palace 6 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.6.active_chart.star` = `['Tian Xin (Heart)']`
- evidence: `palaces.6.active_chart.door` = `Kai (Open)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
