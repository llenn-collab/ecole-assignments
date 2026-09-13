---
id: chart-anatomy
type: article
palace_ids: []
phase: PACKAGE_RENDER
batch: -
sources: ["raw/QMDJ.json", "raw/state/chart_analysis_package.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# Chart Anatomy

The anatomy layer fixes what the chart *is* before anything is interpreted: four pillars, season, duty elements, void, horse, and where the day and hour stems actually live. Two structural facts dominate everything downstream - the day stem is stranded in the Centre, and the hour stem does not appear on the board at all.

## Four pillars

| pillar | stem | element | branch | lands on palace |
|---|---|---|---|---|
| year | Bing | Fire | Wu (Horse) | 9 (Li) |
| month | Ding | Fire | You (Rooster) | 7 (Dui) |
| day | Bing | Fire | Xu (Dog) | 6 (Qian) |
| hour | Jia | Wood | Wu (Horse) | 9 (Li) |

Repeated branches: **Wu (Horse)**. Year and hour both carry Wu (Horse), and both land on palace 9 - which is the duty palace and is void. Timing is concentrated on a palace that cannot hold it.

## Season

| element | state |
|---|---|
| Wood | Dead |
| Fire | Imprisoned |
| Earth | Resting |
| Metal | Prosperous |
| Water | Strengthening |

The day stem **Bing** is Fire, which is **Imprisoned** this season. The hour stem **Jia** is Wood, which is **Dead**. Both the actor and the matter in motion are working against the climate; only Metal and Water are supported.

## Void and horse

- Void palaces (computed and marked, agreeing): **2, 4, 9**
- Day void branches: Wu (Horse), Wei (Goat)
- Hour void branches: Chen (Dragon), Si (Snake)
- Horse star: palace **2** (day horse Shen (Monkey), hour horse Shen (Monkey))

Marker validation passed on all three axes - void, horse and duty all agree between the chart's own flags and independent computation. The chart is internally consistent.

## Duty

- Lead stem: `Jia-Wu Xin` - the Jia-Wu decade, whose visible stand-in is **Xin** at palace 9
- Duty star: **Tian Ying (Hero)** at palace 9
- Duty door: **Jing (Scenery)** at palace 9
- Structure: Yin Dun 3 | Pattern: Fu Yin (All elements in home positions)
- Tian Yi: not exposed by this schema. Tian Yi is not exposed by this schema. Zhi Fu (Chief) is the nearest authority spirit and sits at palace(s) ['9'].

## Where the day stem lives

The day stem **Bing** appears on exactly one palace: the Centre (5). The Centre has no directional opposite, and this chart explicitly attaches it to palace 2 (`palaces.5.active_chart.note`). Palace 2 independently confirms the arrangement by carrying `center_guest: Bing`. So the actor is a guest in someone else's house, and that house is void, horse-struck, self-punished and carries the Death door.

## Where the hour stem lives

**Nowhere.** Jia appears on no heaven, earth or hidden plate. It is represented only by (a) its decade proxy stem Xin at palace 9, (b) its tomb at palace 2, and (c) its branch Wu landing on palace 9. Wood is Dead this season. The matter in motion has no body on this board.

## Batch selectors

| batch | palaces | rule |
|---|---|---|
| B1 | 2, 5, 6, 8, 9 | day-stem set incl. Centre + lodging host + duty-star proxy |
| B2 | 2, 9 | hour-stem proxy set (Jia absent from plate) |
| B3 | 1, 2, 4, 8 | directional opposites of B1 (Centre excluded, host 2 -> 8) |
| B4 | 1, 8 | directional opposites of B2 |
| B5 | 3, 7 | remaining palaces, Luo Shu order |

## See also

- [[Chart-Board-Synthesis]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/state/pillars.json`
- `vault/raw/state/season.json`
- `vault/raw/state/duty.json`
- `vault/raw/state/origin_sets.json`

