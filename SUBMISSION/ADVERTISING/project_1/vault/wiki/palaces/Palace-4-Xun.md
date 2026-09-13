---
id: palace-4
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B3
palace_ids: ["4"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 4 - Xun (Southeast)

> Wood palace | realm Outer | strength Dead | opposite 6

## Infobox

| field | value |
|---|---|
| Heaven stem | Yi |
| Earth stem | Yi |
| Hidden stem | Yi |
| Door | Du (Restraint) (Dead) |
| Star | Tian Fu (Assistant) |
| Spirit | Teng She (Serpent) |
| Branches | Chen (Dragon), Si (Snake) |
| Void | True |
| Horse star | False |
| Afflictions | - |
| Tomb of | Xin, Ren |
| Punishment of | Ren, Gui |

## Roles

- **void_on_showpiece** - Void palace.
- **outer** - Realm as declared by the chart.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Yi | Yi | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Yi | Yi | IDENTICAL (Fu Yin) |
| stem_vs_palace | Yi | Wood | SAME |
| door_vs_palace | Du (Restraint) | Wood | SAME |
| star_vs_palace | Tian Fu (Assistant) | Wood | SAME |
| star_vs_heaven_stem | Tian Fu (Assistant) | Yi | SAME |
| stem_vs_door | Yi | Du (Restraint) | SAME |
| stem_vs_season | Yi | seasonal_element_strengths | Dead |
| stem_vs_day_stem | Yi | Bing | PRODUCES |
| stem_combination_across_board | Yi | Geng | COMBINES -> Metal |
| stem_clash_across_board | Yi | Xin | CLASH |
| strength_concordance | 4 | Dead|Dead|Strengthening|Imprisoned | SPLIT |

## Verdicts (S11)

### V030-P4 - chart_hidden_problems_candidate / WARN

Palace 4 (Xun, Southeast) is void. Whatever is shown here does not land as displayed: it is announced but not received.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.4.active_chart.status.is_void` = `True`
- evidence: `timing.voidness` = `['Wu (Horse)', 'Wei (Goat)', 'Chen (Dragon)', 'Si (Snake)']`

### V031-P4 - chart_hidden_problems_candidate / VETO

The Du (Restraint) door at palace 4 is Dead. This method is available on paper but has no force behind it; using it costs effort and returns little.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.4.active_chart.energy_state.door` = `Dead`
- evidence: `palaces.4.active_chart.door` = `Du (Restraint)`

### V032-P4 - chart_best_solution_candidate / SUPPORT

Palace 4 holds the San Qi stem Yi. Quality, reputation and visibility are concentrated here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.4.active_chart.stems.heaven` = `Yi`
- evidence: `element_prosperities` = `Dead`

### V033-P4 - chart_hidden_problems_candidate / CONSTRAIN

The stem Yi (Wood) at palace 4 is Dead this season. The climate does not support it however good it looks on the board.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.4.active_chart.stems.heaven` = `Yi`
- evidence: `element_prosperities` = `Dead`

### V034-P4 - risk / CONSTRAIN

Palace 4 reads differently from different angles (Dead|Dead|Strengthening|Imprisoned). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.4.active_chart.energy_state` = `Dead|Dead|Strengthening|Imprisoned`

### V035-P4 - risk / CONSTRAIN

Palace 4 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.4.active_chart.star` = `['Tian Fu (Assistant)']`
- evidence: `palaces.4.active_chart.door` = `Du (Restraint)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
