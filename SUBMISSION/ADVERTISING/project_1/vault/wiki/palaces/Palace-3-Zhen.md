---
id: palace-3
type: palace-card
phase: P5_REMAINING
batch: B5
palace_ids: ["3"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 3 - Zhen (East)

> Wood palace | realm Outer | strength Dead | opposite 7

## Infobox

| field | value |
|---|---|
| Heaven stem | Wu |
| Earth stem | Wu |
| Hidden stem | Wu |
| Door | Shang (Harm) (Dead) |
| Star | Tian Chong (Impulse) |
| Spirit | Tai Yin (Moon) |
| Branches | Mao (Rabbit) |
| Void | False |
| Horse star | False |
| Afflictions | Six Instruments Clash Punishment (Liu Yi Ji Xing) |
| Tomb of | - |
| Punishment of | Wu |

## Roles

- **outer** - Realm as declared by the chart.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Wu | Wu | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Wu | Wu | IDENTICAL (Fu Yin) |
| stem_vs_palace | Wu | Wood | CONTROLLED_BY |
| door_vs_palace | Shang (Harm) | Wood | SAME |
| star_vs_palace | Tian Chong (Impulse) | Wood | SAME |
| star_vs_heaven_stem | Tian Chong (Impulse) | Wu | CONTROLS |
| stem_vs_door | Wu | Shang (Harm) | CONTROLLED_BY |
| stem_vs_season | Wu | seasonal_element_strengths | Resting |
| stem_vs_day_stem | Wu | Bing | PRODUCED_BY |
| stem_combination_across_board | Wu | Gui | COMBINES -> Fire |
| self_punished | Wu | 3 | STEM_IN_OWN_PUNISHMENT_PALACE |
| strength_concordance | 3 | Dead|Dead|Strengthening|Imprisoned | SPLIT |

## Verdicts (S11)

### V036-P3 - chart_hidden_problems_candidate / VETO

Palace 3 carries the affliction 'Six Instruments Clash Punishment (Liu Yi Ji Xing)'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.3.active_chart.stems.afflictions` = `Six Instruments Clash Punishment (Liu Yi Ji Xing)`

### V037-P3 - chart_hidden_problems_candidate / VETO

The Shang (Harm) door at palace 3 is Dead. This method is available on paper but has no force behind it; using it costs effort and returns little.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.3.active_chart.energy_state.door` = `Dead`
- evidence: `palaces.3.active_chart.door` = `Shang (Harm)`

### V038-P3 - risk / CONSTRAIN

Palace 3 reads differently from different angles (Dead|Dead|Strengthening|Imprisoned). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.3.active_chart.energy_state` = `Dead|Dead|Strengthening|Imprisoned`

### V039-P3 - risk / CONSTRAIN

Palace 3 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.3.active_chart.star` = `['Tian Chong (Impulse)']`
- evidence: `palaces.3.active_chart.door` = `Shang (Harm)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
