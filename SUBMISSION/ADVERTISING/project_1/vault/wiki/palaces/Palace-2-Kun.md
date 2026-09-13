---
id: palace-2
type: palace-card
phase: P1_TO_P4_OPERATOR_ZOOM
batch: B1
palace_ids: ["2"]
sources: ["raw/chart/dump.md", "raw/state/indexes.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: verdicted
---

# Palace 2 - Kun (Southwest)

> Earth palace | realm Inner | strength Resting | opposite 8

## Infobox

| field | value |
|---|---|
| Heaven stem | Ji |
| Earth stem | Ji |
| Hidden stem | Ji |
| Door | Si (Death) (Resting) |
| Star | Tian Rui (Grain), Tian Qin (Bird) |
| Spirit | Jiu Tian (Nine Heavens) |
| Branches | Wei (Goat), Shen (Monkey) |
| Void | True |
| Horse star | True |
| Afflictions | Clash Punishment (Ji Xing), Self Punishment |
| Tomb of | Jia, Gui |
| Punishment of | Ji |

## Roles

- **day_stem_or_jia_set** - Selected by the day-stem origin set.
- **hour_stem_or_focus** - Selected by the hour-stem proxy set.
- **void_on_showpiece** - Void palace.
- **horse_plus_open** - Horse star present: movement/relocation.
- **tomb_of_yongshen** - Entombs the hour stem.
- **inner** - Realm as declared by the chart.
- **lodged_from_center** - Hosts the displaced Centre.

## Relations (S8)

| kind | a | b | relation |
|---|---|---|---|
| heaven_earth_stem_pair | Ji | Ji | IDENTICAL (Fu Yin) |
| heaven_hidden_stem_pair | Ji | Ji | IDENTICAL (Fu Yin) |
| stem_vs_palace | Ji | Earth | SAME |
| door_vs_palace | Si (Death) | Earth | SAME |
| star_vs_palace | Tian Rui (Grain) | Earth | SAME |
| star_vs_heaven_stem | Tian Rui (Grain) | Ji | SAME |
| star_vs_palace | Tian Qin (Bird) | Earth | SAME |
| star_vs_heaven_stem | Tian Qin (Bird) | Ji | SAME |
| stem_vs_door | Ji | Si (Death) | SAME |
| stem_vs_season | Ji | seasonal_element_strengths | Resting |
| stem_vs_day_stem | Ji | Bing | PRODUCED_BY |
| self_punished | Ji | 2 | STEM_IN_OWN_PUNISHMENT_PALACE |
| strength_concordance | 2 | Resting|Resting|Strengthening|Prosperous | SPLIT |

## Verdicts (S11)

### V001-P2 - chart_hidden_problems_candidate / WARN

Palace 2 (Kun, Southwest) is void. Whatever is shown here does not land as displayed: it is announced but not received.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.2.active_chart.status.is_void` = `True`
- evidence: `timing.voidness` = `['Wu (Horse)', 'Wei (Goat)', 'Chen (Dragon)', 'Si (Snake)']`

### V002-P2 - timing / SEQUENCE

Palace 2 carries the horse star: the matter here moves, travels or changes hands rather than staying put.

- grounding: `EXPLICIT` | confidence: `MED`
- evidence: `palaces.2.active_chart.status.has_horse_star` = `True`
- evidence: `timing.four_pillars.day` = `Bing-Xu`

### V003-P2 - chart_hidden_problems_candidate / VETO

Palace 2 carries the affliction 'Clash Punishment (Ji Xing)'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.2.active_chart.stems.afflictions` = `Clash Punishment (Ji Xing)`

### V004-P2 - chart_hidden_problems_candidate / VETO

Palace 2 carries the affliction 'Self Punishment'. Self-inflicted damage or internal contradiction is recorded on this palace by the chart itself.

- grounding: `EXPLICIT` | confidence: `HIGH`
- evidence: `palaces.2.active_chart.stems.afflictions` = `Self Punishment`

### V005-P2 - chart_hidden_problems_candidate / VETO

Palace 2 is the tomb of the hour stem Jia. The matter in motion is already buried at this location.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.2.palace_stem_rules.stems_in_tomb` = `Jia`
- evidence: `timing.four_pillars.hour` = `Jia-Wu`

### V006-P2 - risk / CONSTRAIN

Palace 2 reads differently from different angles (Resting|Resting|Strengthening|Prosperous). It looks one way and behaves another; do not trust a single strength reading here.

- grounding: `COMPUTED` | confidence: `MED`
- evidence: `palaces.2.active_chart.energy_state` = `Resting|Resting|Strengthening|Prosperous`

### V007-P2 - risk / CONSTRAIN

Palace 2 has its own star and its own door at home, with heaven, earth and hidden stems identical. Nothing here is in motion; the position repeats itself rather than developing.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.2.active_chart.star` = `['Tian Rui (Grain)', 'Tian Qin (Bird)']`
- evidence: `palaces.2.active_chart.door` = `Si (Death)`
- evidence: `chart_config.chart_pattern` = `Fu Yin (All elements in home positions)`

### V008-P2 - chart_hidden_problems_candidate / VETO

Palace 2 hosts the displaced day stem Bing while being void, horse-struck, clash-punished and carrying the Death door. The actor's only landing place is the worst-conditioned palace on the board.

- grounding: `COMPUTED` | confidence: `HIGH`
- evidence: `palaces.2.active_chart.stems.center_guest` = `Bing`
- evidence: `palaces.2.active_chart.status.is_void` = `True`
- evidence: `palaces.2.active_chart.door` = `Si (Death)`
- evidence: `palaces.2.active_chart.stems.afflictions` = `['Clash Punishment (Ji Xing)', 'Self Punishment']`

## See also

- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/chart/dump.md`
- `vault/raw/state/indexes.json`
