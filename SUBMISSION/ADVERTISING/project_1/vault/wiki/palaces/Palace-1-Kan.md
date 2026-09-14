---
id: palace-1
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B3
palace_ids: ["1"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 1 - Kan (North)

> Water palace | realm Outer | strength Strengthening | opposite 9

## Infobox

| field | value |
|---|---|
| Heaven stem | Geng |
| Earth stem | Geng |
| Hidden stem | Geng |
| Door | Xiu (Rest) (Strengthening) |
| Star | Tian Peng (Grass) |
| Spirit | Bai Hu (White Tiger) |
| Branches | Zi (Rat) |
| Void | False |
| Horse star | False |
| Afflictions | - |
| Tomb of | - |
| Punishment of | - |

## Roles

- **outer** - Realm as declared by the chart.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Geng | Geng | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Geng | Geng | IDENTICAL (Fu Yin) |
| stem_vs_palace | Geng | Water | PRODUCES |
| door_vs_palace | Xiu (Rest) | Water | SAME |
| star_vs_palace | Tian Peng (Grass) | Water | SAME |
| star_vs_heaven_stem | Tian Peng (Grass) | Geng | PRODUCED_BY |
| stem_vs_door | Geng | Xiu (Rest) | PRODUCES |
| stem_vs_season | Geng | seasonal_element_strengths | Prosperous |
| stem_vs_day_stem | Geng | Bing | CONTROLLED_BY |
| stem_combination_across_board | Geng | Yi | COMBINES -> Metal |
| strength_concordance | 1 | Strengthening|Strengthening|Strengthening|Obsolete | SPLIT |

## Verdicts (S11)

### V028-P1 - risk / CONSTRAIN

Palace 1 reads differently from different angles (Strengthening|Strengthening|Strengthening|Obsolete). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.1.active_chart.energy_state` = `Strengthening|Strengthening|Strengthening|Obsolete`

### V029-P1 - risk / CONSTRAIN

Palace 1 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.1.active_chart.star` = `['Tian Peng (Grass)']`
- evidence: `palaces.1.active_chart.door` = `Xiu (Rest)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
