---
id: "chart-board-synthesis"
type: "article"
phase: "P6_BOARD_SYNTHESIS"
batch: "—"
palace_ids: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
sources:
  - "raw/state/systems.json"
  - "raw/state/relations.json"
  - "raw/state/patterns.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Board Synthesis (P6)

## Door system map
- **Death** @ palace 4 — palace Wood controls door Death (Earth) — forced door (palace oppressing door) (`palaces.xun_4.door`)
- **Du** @ palace 8 — door Du (Wood) controls palace Earth — door oppressing palace (`palaces.gen_8.door`)
- **Life** @ palace 6 — door Life (Earth) generates palace Metal (`palaces.qian_6.door`)
- **Open** @ palace 2 — palace Earth generates door Open (Metal) (`palaces.kun_2.door`)
- **Rest** @ palace 7 — palace Metal generates door Rest (Water) (`palaces.dui_7.door`)
- **Scenery** @ palace 9 — door Scenery and palace Fire share element (`palaces.li_9.door`)
- **Shang** @ palace 1 — palace Water generates door Shang (Wood) (`palaces.kan_1.door`)

## Star system map (home → seat; all displaced)
- **Tian Chong** (home 3) → seats [["6", true]]
- **Tian Fu** (home 4) → seats [["1", true]]
- **Tian Peng** (home 1) → seats [["2", true]]
- **Tian Qin** (home 5) → seats [["3", true], ["5", false]]
- **Tian Ren** (home 8) → seats [["7", true]]
- **Tian Rui** (home 2) → seats [["3", true]]
- **Tian Xin** (home 6) → seats [["9", true]]
- **Tian Ying** (home 9) → seats [["8", true]]
- **Tian Zhu** (home 7) → seats [["4", true]]

## Deity map
- **Chief** @ palace 3
- **Flying Snake** @ palace 8
- **Great Yin** @ palace 1
- **Nine Earths** @ palace 9
- **Nine Heavens** @ palace 4
- **Six Harmony** @ palace 6
- **Tai Chang** @ palace 5
- **White Tiger** @ palace 7
- **Xuanwu** @ palace 2

## San Qi / Liu Yi positions
| stem | class | positions |
|---|---|---|
| Bing | sanqi | [["6", "hidden"], ["7", "heaven"], ["8", "earth"]] |
| Ding | sanqi | [["3", "hidden"], ["8", "heaven"], ["9", "earth"]] |
| Geng | liuyi | [["1", "heaven"], ["4", "earth"], ["8", "hidden"]] |
| Gui | liuyi | [["1", "earth"], ["2", "heaven"], ["7", "hidden"]] |
| Ji | liuyi | [["5", "heaven"], ["5", "earth"], ["5", "hidden"]] |
| Ren | liuyi | [["2", "earth"], ["3", "heaven"], ["4", "hidden"]] |
| Wu | liuyi | [["2", "hidden"], ["6", "earth"], ["9", "heaven"]] |
| Xin | liuyi | [["1", "hidden"], ["3", "earth"], ["6", "heaven"]] |
| Yi | sanqi | [["4", "heaven"], ["7", "earth"], ["9", "hidden"]] |

## Void · tomb · punishment · force · horse graph
| palace | void | tomb markers | punishment | forced door | horse |
|---|---|---|---|---|---|
| 1 | — | — | — | no | — |
| 2 | palace 2 void: day-void ['Wei'], hour-void — | ["Tomb (Gui)"] | Ji (Wei, Kun 2, Shen) | no | year horse (Shen) in palace 2 |
| 3 | palace 3 void: day-void —, hour-void ['Mao'] | — | Wu (Mao, Zhen 3) | no | — |
| 4 | — | ["Tomb & Punishment (Ren)"] | Ren Gui (Chen, Xun 4, Si) | YES | hour horse (Si) in palace 4 |
| 5 | — | — | Punishment | no | — |
| 6 | — | ["Tomb (Wu)"] | — | no | month horse (Hai) in palace 6 |
| 7 | — | — | — | no | — |
| 8 | palace 8 void: day-void —, hour-void ['Yin'] | ["Tomb (Ding)"] | Geng (Yin, Gen 8, Chou) | no | day horse (Yin) in palace 8 |
| 9 | palace 9 void: day-void ['Wu'], hour-void — | — | Xin (Li 9, Wu) | no | — |

## Inner/outer
- inner: ['2', '5', '6', '7', '9'] — process, constraint, institution, internal rationale
- outer: ['1', '3', '4', '8'] — audience, surface, movement, submission-facing behaviour

## Pillars × palaces
| pillar | stem→palaces | branch→palace | void membership |
|---|---|---|---|
| day (Ren Chen) | [["2", "earth"], ["3", "heaven"], ["4", "hidden"], ["4", "marker_reference"]] | 4 | — |
| hour (Xin Hai) | [["1", "hidden"], ["3", "earth"], ["6", "heaven"]] | 6 | — |
| month (Ding You) | [["3", "hidden"], ["8", "heaven"], ["8", "marker_reference"], ["9", "earth"]] | 7 | — |
| year (Bing Wu) | [["6", "hidden"], ["7", "heaven"], ["8", "earth"]] | 9 | DAY-VOID  |

## Reconstituted center
- center lodging graph: [["Ji", "3"], ["Ji", "2"], ["Heaven Qin", "3"]]
- read-through hosts: ['3 (heaven Ji + Tian Qin)', '2 (hidden Ji)']

## Original-position audit (post-remediation)
| palace | branches | star home | door home | deity note | numbers |
|---|---|---|---|---|---|
| 1 | match | Heavenly Peng→Tian Peng ✓ | Rest Door | rotation-divergence recorded | opaque |
| 2 | match | Heavenly Rui→Tian Rui ✓ | Death Door | rotation-divergence recorded | opaque |
| 3 | match | Heavenly Chong→Tian Chong ✓ | Wound Door | rotation-divergence recorded | opaque |
| 4 | match | Heavenly Auxiliary→Tian Fu ✓ | Du Door | rotation-divergence recorded | opaque |
| 5 | match | Heavenly Bird→Tian Qin ✓ | absent by design | rotation-divergence recorded | opaque |
| 6 | match | Heavenly Heart→Tian Xin ✓ | Open Door | rotation-divergence recorded | opaque |
| 7 | match | Heavenly Pillar→Tian Zhu ✓ | Fright Door | rotation-divergence recorded | opaque |
| 8 | match | Heavenly Ren→Tian Ren ✓ | Life Door | rotation-divergence recorded | opaque |
| 9 | match | Heavenly Hero→Tian Ying ✓ | Scenery Door | rotation-divergence recorded | opaque |
- summary: {"branch_blocks": "8/8 explicit branch lists match frozen identity geometry (center block absent by design)", "door_blocks": "all 8 explicit original doors unique and consistent; center door absent by design", "inconsistent": [], "star_blocks": "all explicit original stars consistent with frozen star-home table"}

## Opposite-palace audit (explicit vs frozen geometry)
| palace | explicit | computed | status |
|---|---|---|---|
| 1 | Kun 8 | Li 9 | MISMATCH |
| 2 | Xun 5 | Gen 8 | MISMATCH |
| 3 | Li 3 | Dui 7 | MISMATCH |
| 4 | Dui 2 | Qian 6 | MISMATCH |
| 5 | None | None | NO_OPPOSITE (center pivot) |
| 6 | Gen 7 | Xun 4 | MISMATCH |
| 7 | Kan 6 | Zhen 3 | MISMATCH |
| 8 | Zhen 4 | Kun 2 | MISMATCH |
| 9 | Qian 1 | Kan 1 | MISMATCH |

Board consistency: **PASS** — split claims recorded for palaces 2, 4, 9 (overload rule); no SUPPORT/VETO collision on the same logical path.

See also: [[Chart-Patterns]] · [[Chart-Analysis-Report]] · [[MOC]]