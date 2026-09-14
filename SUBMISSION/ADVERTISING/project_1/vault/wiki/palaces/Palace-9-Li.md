---
id: palace-9
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B1
palace_ids: ["9"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 9 - Li (South)

> Fire palace | realm Inner | strength Imprisoned | opposite 1

## Infobox

| field | value |
|---|---|
| Heaven stem | Xin |
| Earth stem | Xin |
| Hidden stem | Xin |
| Door | Jing (Scenery) (Imprisoned) |
| Star | Tian Ying (Hero) |
| Spirit | Zhi Fu (Chief) |
| Branches | Wu (Horse) |
| Void | True |
| Horse star | False |
| Afflictions | Clash Punishment (Ji Xing), Self Punishment, Fu Yin |
| Tomb of | - |
| Punishment of | Xin |

## Roles

- **day_stem_or_jia_set** - Selected by the day-stem origin set.
- **hour_stem_or_focus** - Selected by the hour-stem proxy set.
- **duty_star** - Carries the duty star, the authority of the matter.
- **duty_door** - Carries the duty door.
- **void_on_showpiece** - Void palace.
- **inner** - Realm as declared by the chart.
- **stacked_branch** - Pillar branch(es) ['year', 'hour'] land here.
- **lead_stem_proxy** - Visible stand-in for the invisible Jia decade.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Xin | Xin | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Xin | Xin | IDENTICAL (Fu Yin) |
| stem_vs_palace | Xin | Fire | CONTROLLED_BY |
| door_vs_palace | Jing (Scenery) | Fire | SAME |
| star_vs_palace | Tian Ying (Hero) | Fire | SAME |
| star_vs_heaven_stem | Tian Ying (Hero) | Xin | CONTROLS |
| stem_vs_door | Xin | Jing (Scenery) | CONTROLLED_BY |
| stem_vs_season | Xin | seasonal_element_strengths | Prosperous |
| stem_vs_day_stem | Xin | Bing | CONTROLLED_BY |
| stem_combination_across_board | Xin | Bing | COMBINES -> Water |
| stem_clash_across_board | Xin | Yi | CLASH |
| self_punished | Xin | 9 | STEM_IN_OWN_PUNISHMENT_PALACE |
| strength_concordance | 9 | Imprisoned|Imprisoned|Strengthening|Resting | SPLIT |

## Verdicts (S11)

### V020-P9 - chart_hidden_problems_candidate / WARN

Palace 9 (Li, South) is void. Whatever is shown here does not land as displayed: it is announced but not received.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.status.is_void` = `True`
- evidence: `timing.voidness` = `['Wu (Horse)', 'Wei (Goat)', 'Chen (Dragon)', 'Si (Snake)']`

### V021-P9 - chart_hidden_problems_candidate / VETO

Palace 9 carries the affliction 'Clash Punishment (Ji Xing)'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.stems.afflictions` = `Clash Punishment (Ji Xing)`

### V022-P9 - chart_hidden_problems_candidate / VETO

Palace 9 carries the affliction 'Self Punishment'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.stems.afflictions` = `Self Punishment`

### V023-P9 - chart_hidden_problems_candidate / WARN

Palace 9 carries the affliction 'Fu Yin'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.stems.afflictions` = `Fu Yin`

### V024-P9 - chart_hidden_problems_candidate / VETO

The Jing (Scenery) door at palace 9 is Imprisoned. This method is available on paper but has no force behind it; using it costs effort and returns little.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.energy_state.door` = `Imprisoned`
- evidence: `palaces.9.active_chart.door` = `Jing (Scenery)`

### V025-P9 - chart_answers_candidate / SUPPORT

Palace 9 is the duty palace: it carries both the duty star Tian Ying (Hero) and the duty door Jing (Scenery). This is where the chart says the subject of the question actually sits.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.status.is_duty_palace` = `True`
- evidence: `chart_config.duty_star` = `Tian Ying (Hero)`
- evidence: `chart_config.duty_door` = `Jing (Scenery)`

### V026-P9 - risk / CONSTRAIN

Palace 9 reads differently from different angles (Imprisoned|Imprisoned|Strengthening|Resting). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.9.active_chart.energy_state` = `Imprisoned|Imprisoned|Strengthening|Resting`

### V027-P9 - risk / CONSTRAIN

Palace 9 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.9.active_chart.star` = `['Tian Ying (Hero)']`
- evidence: `palaces.9.active_chart.door` = `Jing (Scenery)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
