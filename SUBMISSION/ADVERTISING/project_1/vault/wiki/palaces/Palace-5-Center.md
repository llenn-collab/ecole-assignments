---
id: palace-5
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B1
palace_ids: ["5"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 5 - Zhong (Center)

> Earth palace | realm Centre | strength Resting | opposite NO_OPPOSITE

## Infobox

| field | value |
|---|---|
| Heaven stem | Bing |
| Earth stem | Bing |
| Hidden stem | Bing |
| Door | None (None) |
| Star | - |
| Spirit | Tai Chang (Grand Blessing) |
| Branches | - |
| Void | False |
| Horse star | False |
| Afflictions | - |
| Tomb of | - |
| Punishment of | - |

## Roles

- **day_stem_or_jia_set** - Selected by the day-stem origin set.
- **outer** - Centre: no realm field; treated as inner pivot.
- **lodged_from_center** - Centre content is hosted by palace 2.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Bing | Bing | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Bing | Bing | IDENTICAL (Fu Yin) |
| stem_vs_palace | Bing | Earth | PRODUCES |
| stem_vs_season | Bing | seasonal_element_strengths | Imprisoned |
| stem_vs_day_stem | Bing | Bing | SAME |
| stem_combination_across_board | Bing | Xin | COMBINES -> Water |
| stem_clash_across_board | Bing | Ren | CLASH |
| strength_concordance | 5 | Resting | CONCORDANT |

## Verdicts (S11)

### V009-P5 - chart_best_solution_candidate / SUPPORT

Palace 5 holds the San Qi stem Bing. Quality, reputation and visibility are concentrated here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.5.active_chart.stems.heaven` = `Bing`
- evidence: `element_prosperities` = `Imprisoned`

### V010-P5 - chart_hidden_problems_candidate / CONSTRAIN

The stem Bing (Fire) at palace 5 is Imprisoned this season. The climate does not support it however good it looks on the board.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.5.active_chart.stems.heaven` = `Bing`
- evidence: `element_prosperities` = `Imprisoned`

### V011-P5 - chart_answers_candidate / CONSTRAIN

The day stem Bing sits in the Centre and is attached to palace 2. The actor is displaced: it has no directional position of its own and must operate through its host.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.5.active_chart.stems.heaven` = `Bing`
- evidence: `palaces.5.active_chart.note` = `Attached to Palace 2`
- evidence: `palaces.2.active_chart.stems.center_guest` = `Bing`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
