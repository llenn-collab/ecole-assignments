---
id: "chart-working-copy"
type: "article"
phase: "P6_BOARD_SYNTHESIS"
batch: "—"
palace_ids: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
sources:
  - "raw/state/systems.json"
  - "raw/state/palaces.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Working Copy (normalized board)

| palace | heaven/earth/hidden | star | door | deity | door str | star str (raw tokens) | palace state | ring | split |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Kan | Geng / Gui / Xin | Heaven Fu | Shang | Great Yin | Dead | Discarded / Imprisoned | Strong / Outer | outer | YES |
| 2 Kun | Gui / Ren / Wu | Heaven Peng | Open | Xuanwu | Prosperous | Imprisoned / Discarded | Rest / Inner | inner | YES |
| 3 Zhen | Ren / Xin / Ding | Heaven Rui & Heaven Qin | Scenery | Chief | Imprisoned | Imprisoned / Prosperous | Dead / Outer | outer | YES |
| 4 Xun | Yi / Geng / Ren | Heaven Pillar | Death | Nine Heavens | Rest | Rest / Strong | Dead / Outer | outer | YES |
| 5 Center | Ji (lodged in Zhen 3 Palace) / Ji / Ji (lodged in Kun 2 Palace) | Heaven Qin (lodged in Zhen 3 Palace) | — | Tai Chang | — | — | Rest | inner | no |
| 6 Qian | Xin / Wu / Bing | Heaven Chong | Life | Six Harmony | Rest | Imprisoned / Imprisoned | Prosperous / Inner | inner | no |
| 7 Dui | Bing / Yi / Gui | Heaven Ren | Rest | White Tiger | Strong | Prosperous / Prosperous | Prosperous / Inner | inner | no |
| 8 Gen | Ding / Bing / Geng | Heaven Ying | Du | Flying Snake | Dead | Prosperous / Rest | Rest / Outer | outer | YES |
| 9 Li | Wu / Ding / Yi | Heaven Heart | Scenery | Nine Earths | Prosperous | Imprisoned / Strong | Imprisoned / Inner | inner | YES |

*Raw vocabulary preserved; normalization is computed only. Star two-token convention (by_season/by_palace order) is flagged SCHEMA_AMBIGUITY — tokens never force-mapped.*

See also: [[Chart-Anatomy]] · [[Chart-Board-Synthesis]] · [[MOC]]