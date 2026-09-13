---
id: palace-8
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B1
palace_ids: ["8"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 8 - Gen (Northeast)

> Earth palace | realm Outer | strength Resting | opposite 2

## Infobox

| field | value |
|---|---|
| Heaven stem | Ren |
| Earth stem | Ren |
| Hidden stem | Ren |
| Door | Sheng (Life) (Resting) |
| Star | Tian Ren (Ambassador) |
| Spirit | Liu He (Six Harmony) |
| Branches | Chou (Ox), Yin (Tiger) |
| Void | False |
| Horse star | False |
| Afflictions | - |
| Tomb of | Ding, Ji, Geng |
| Punishment of | Geng |

## Roles

- **day_stem_or_jia_set** - Selected by the day-stem origin set.
- **outer** - Realm as declared by the chart.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Ren | Ren | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Ren | Ren | IDENTICAL (Fu Yin) |
| stem_vs_palace | Ren | Earth | CONTROLLED_BY |
| door_vs_palace | Sheng (Life) | Earth | SAME |
| star_vs_palace | Tian Ren (Ambassador) | Earth | SAME |
| star_vs_heaven_stem | Tian Ren (Ambassador) | Ren | CONTROLS |
| stem_vs_door | Ren | Sheng (Life) | CONTROLLED_BY |
| stem_vs_season | Ren | seasonal_element_strengths | Strengthening |
| stem_vs_day_stem | Ren | Bing | CONTROLS |
| stem_combination_across_board | Ren | Ding | COMBINES -> Wood |
| stem_clash_across_board | Ren | Bing | CLASH |
| strength_concordance | 8 | Resting|Resting|Strengthening|Prosperous | SPLIT |

## Verdicts (S11)

### V018-P8 - risk / CONSTRAIN

Palace 8 reads differently from different angles (Resting|Resting|Strengthening|Prosperous). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.8.active_chart.energy_state` = `Resting|Resting|Strengthening|Prosperous`

### V019-P8 - risk / CONSTRAIN

Palace 8 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.8.active_chart.star` = `['Tian Ren (Ambassador)']`
- evidence: `palaces.8.active_chart.door` = `Sheng (Life)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
