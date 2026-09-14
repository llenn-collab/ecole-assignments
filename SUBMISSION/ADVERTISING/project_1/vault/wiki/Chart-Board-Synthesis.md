---
id: chart-board-synthesis
type: article
palace_ids: ["1","2","3","4","5","6","7","8","9"]
phase: PACKAGE_RENDER
batch: -
sources: ["raw/QMDJ.json", "raw/state/chart_analysis_package.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# Chart Board Synthesis

Phase 6 reads the board as one object rather than nine. The systems below are computed from values only; where the specification names a field this export does not have (forced doors, Tian Yi), no claim is made.

## Door system

| palace | door | element | strength | at home | element in season |
|---|---|---|---|---|---|
| 1 | Xiu (Rest) | Water | Strengthening | True | Strengthening |
| 2 | Si (Death) | Earth | Resting | True | Resting |
| 3 | Shang (Harm) | Wood | Dead | True | Dead |
| 4 | Du (Restraint) | Wood | Dead | True | Dead |
| 6 | Kai (Open) | Metal | Prosperous | True | Prosperous |
| 7 | Jing (Fear) | Metal | Prosperous | True | Prosperous |
| 8 | Sheng (Life) | Earth | Resting | True | Resting |
| 9 | Jing (Scenery) | Fire | Imprisoned | True | Imprisoned |

Every door sits at its original palace - a direct consequence of Fu Yin. The two Prosperous doors are Kai (Open) at 6 and Jing (Fear) at 7, both Metal, and Metal is the Prosperous element this season. The two Dead doors are Shang (Harm) at 3 and Du (Restraint) at 4, both Wood, and Wood is Dead. Method strength in this chart is almost entirely a function of the season, not of position.

## Star system

| palace | star(s) | home | sitting home | seasonal | by palace |
|---|---|---|---|---|---|
| 1 | Tian Peng (Grass) | 1 | Tian Peng (Grass) | Strengthening | Obsolete |
| 2 | Tian Rui (Grain), Tian Qin (Bird) | 2, 5 | Tian Rui (Grain) | Strengthening | Prosperous |
| 3 | Tian Chong (Impulse) | 3 | Tian Chong (Impulse) | Strengthening | Imprisoned |
| 4 | Tian Fu (Assistant) | 4 | Tian Fu (Assistant) | Strengthening | Imprisoned |
| 5 | - | - | - | - | - |
| 6 | Tian Xin (Heart) | 6 | Tian Xin (Heart) | Strengthening | Strengthening |
| 7 | Tian Zhu (Pillar) | 7 | Tian Zhu (Pillar) | Strengthening | Strengthening |
| 8 | Tian Ren (Ambassador) | 8 | Tian Ren (Ambassador) | Strengthening | Prosperous |
| 9 | Tian Ying (Hero) | 9 | Tian Ying (Hero) | Strengthening | Resting |

Every star is in its own Luo Shu home. Note that every star is *Strengthening* by season - that column is uniform and therefore carries no discriminating information. The useful column is `by palace`, which splits: Prosperous at 2 and 8, Strengthening at 6 and 7, Resting at 9, Imprisoned at 3 and 4, Obsolete at 1.

## Spirit map

| palace | active spirit | home spirit | at home |
|---|---|---|---|
| 1 | Bai Hu (White Tiger) | Zhi Fu (Chief) | False |
| 2 | Jiu Tian (Nine Heavens) | Zhu Que (Vermilion Bird), Xuan Wu (Black Tortoise) | False |
| 3 | Tai Yin (Moon) | Tai Yin (Moon) | True |
| 4 | Teng She (Serpent) | Liu He (Six Harmony) | False |
| 5 | Tai Chang (Grand Blessing) | - | False |
| 6 | Xuan Wu (Black Tortoise) | Jiu Tian (Nine Heavens) | False |
| 7 | Jiu Di (Nine Earths) | Jiu Di (Nine Earths) | True |
| 8 | Liu He (Six Harmony) | Teng She (Serpent) | False |
| 9 | Zhi Fu (Chief) | Gou Chen (Hooked Array), Bai Hu (White Tiger) | False |

The spirits are the one system that is *not* frozen in place: Zhi Fu (Chief) has moved from palace 1 to palace 9, and Bai Hu (White Tiger) from 9 to 1. The authority spirit and the aggression spirit have swapped ends of the board. In a chart that is otherwise completely static, spirit placement is where the movement information is.

## San Qi and Liu Yi

| stem | palaces | season |
|---|---|---|
| Yi (San Qi) | 4 | Dead |
| Bing (San Qi) | 5 | Imprisoned |
| Ding (San Qi) | 6 | Imprisoned |
| Wu (Liu Yi) | 3 | Resting |
| Ji (Liu Yi) | 2 | Resting |
| Geng (Liu Yi) | 1 | Prosperous |
| Xin (Liu Yi) | 9 | Prosperous |
| Ren (Liu Yi) | 8 | Strengthening |
| Gui (Liu Yi) | 7 | Strengthening |

Yi sits in a Dead-wood, void, Dead-door palace (4). Bing is stranded in the Centre. Only Ding at palace 6 has a working door and a prosperous palace.

## Wang Shuai matrix

| palace | element | season | palace str | door str | star (season) | star (palace) | concordant | mean |
|---|---|---|---|---|---|---|---|---|
| 1 | Water | Strengthening | Strengthening | Strengthening | Strengthening | Obsolete | True | 0.8 |
| 2 | Earth | Resting | Resting | Resting | Strengthening | Prosperous | True | 0.5 |
| 3 | Wood | Dead | Dead | Dead | Strengthening | Imprisoned | True | 0.0 |
| 4 | Wood | Dead | Dead | Dead | Strengthening | Imprisoned | True | 0.0 |
| 5 | Earth | Resting | Resting | - | - | - | True | 0.5 |
| 6 | Metal | Prosperous | Prosperous | Prosperous | Strengthening | Strengthening | True | 1.0 |
| 7 | Metal | Prosperous | Prosperous | Prosperous | Strengthening | Strengthening | True | 1.0 |
| 8 | Earth | Resting | Resting | Resting | Strengthening | Prosperous | True | 0.5 |
| 9 | Fire | Imprisoned | Imprisoned | Imprisoned | Strengthening | Resting | True | 0.25 |

Exhausted and Obsolete states are included, not filtered. Split strength is the norm here, not the exception: only palaces 6 and 7 read the same from every angle. Palace 1 is the sharpest split - the palace is Strengthening and the door is Strengthening, but the star is Obsolete by palace relation.

## Inner and outer

- Inner (process, institution, internal rationale): 2, 6, 7, 9
- Outer (audience, surface, movement): 1, 3, 4, 8
- Centre: no realm field in source; the specification treats it as inner.

Mean health, inner: P2 0.5, P6 1.0, P7 1.0, P9 0.25

Mean health, outer: P1 0.8, P3 0.0, P4 0.0, P8 0.5

The inner realm is stronger on average, but its strength is concentrated in 6 and 7 while its two weakest members (2 and 9) are exactly the two palaces the actor and the brief actually occupy. The outer realm is weak apart from palace 8.

## Pillars times palaces

| pillar | stem | branch | palace | void | door |
|---|---|---|---|---|---|
| year | Bing | Wu (Horse) | 9 (Li) | True | Jing (Scenery) |
| month | Ding | You (Rooster) | 7 (Dui) | False | Jing (Fear) |
| day | Bing | Xu (Dog) | 6 (Qian) | False | Kai (Open) |
| hour | Jia | Wu (Horse) | 9 (Li) | True | Jing (Scenery) |

Year branch Wu and hour branch Wu both stack on palace 9, which is also the duty palace and is void. Timing is locked onto a palace that cannot hold it.

## Reconstituted Centre

The Centre holds the day stem Bing with Tai Chang (Grand Blessing) at Resting strength, and attaches to palace 2. Palace 2 is void, horse-struck, clash- and self-punished, carries the Death door, and is the tomb of Jia and Gui. The actor therefore has no seat of its own and its only seat is compromised.

The Centre is not forced into a directional pair. It is held as a graph: stem and star lodge into palace 2, the spirit Tai Chang stays with the Centre itself, and the Centre keeps `NO_OPPOSITE` status.

## Board consistency

- Pass: **True** | unresolved contradictions: 0 | split claims recorded: 3

- Palace 4: Palace 4 carries both SUPPORT and VETO claims. Per the overload rule these are kept as separate typed claims and are not averaged into one verdict.
- Palace 6: Palace 6 carries both SUPPORT and VETO claims. Per the overload rule these are kept as separate typed claims and are not averaged into one verdict.
- Palace 9: Palace 9 carries both SUPPORT and VETO claims. Per the overload rule these are kept as separate typed claims and are not averaged into one verdict.

## See also

- [[Chart-Patterns]]
- [[Chart-Analysis-Report]]

## Sources

- `vault/raw/state/systems.json`
- `vault/raw/state/board_consistency.json`

