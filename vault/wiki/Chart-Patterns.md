---
id: "chart-patterns"
type: "article"
phase: "P6_BOARD_SYNTHESIS"
batch: "—"
palace_ids: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
sources:
  - "raw/state/patterns.json"
  - "raw/state/explicit_patterns.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Patterns

## Explicit pattern reconciliation (explicit ingested before computed)
| explicit pattern | palace | status | note |
|---|---|---|---|
| Palace Generating Door | 1 | **VALIDATED** | — |
| Great Barrier | 1 | **VALIDATED** | Geng over Gui co-located (both pieces exist) |
| Palace Generating Door | 2 | **VALIDATED** | — |
| Palace Generating Door | 3 | **VALIDATED** | — |
| Wonder Instrument Combination | 4 | **VALIDATED** | Yi+Geng five-combination co-located in-palace |
| Three Wonders Obtaining Mission | 4 | **VALIDATED** | sanqi Yi co-located with the duty door (zhi_shi Death) |
| Door Entering Tomb | 4 | **VALIDATED_SCHOOL_VARIANT** | Death door Earth rides over Chen water-tomb branch in-palace (earth-follows-water convention) |
| Palace Oppressing Door | 4 | **VALIDATED** | — |
| Three Wonders Being Restricted | 4 | **VALIDATED** | Geng metal controls Yi wood in-palace |
| Door Generating Palace | 6 | **VALIDATED** | — |
| Palace Generating Door | 7 | **VALIDATED** | — |
| Ding Wonder Entering Tomb | 8 | **VALIDATED** | Ding tomb Chou in-palace; explicit Tomb (Ding) marker |
| Door Oppressing Palace | 8 | **VALIDATED** | — |
| Wonder Wandering Salary Position | 9 | **VALIDATED** | Ding salary at Wu; earth stem Ding in Li 9 (school convention note) |
| Palace Oppressing Door | 9 | **CONFLICT** | explicit vs computed conflict — anomaly ANO logged |

## Computed catalog (always-on extraction)
| pattern | palaces | polarity | grounding | note |
|---|---|---|---|---|
| forced_door | ['4'] | inauspicious | COMPUTED | — |
| void_palace | ['2', '3', '8', '9'] | constraint | COMPUTED | — |
| stem_in_tomb | ['2', '4', '6', '8'] | inauspicious | COMPUTED | — |
| stem_in_punishment | ['3', '4'] | inauspicious | COMPUTED | palace 4 punishment names hidden-stem Ren (in-palace); palace 3 names Wu (not in-palace — reference kept) |
| duty_star | ['3'] | authority | COMPUTED | — |
| duty_door | ['4'] | method_to_avoid | COMPUTED | — |
| hour_stem_focus | ['6'] | timing | COMPUTED | — |
| horse_star | ['2', '4', '6', '8'] | movement | COMPUTED | — |
| heaven_earth_stem_pair | ['1', '2', '3', '4', '5', '6', '7', '8', '9'] | structural | COMPUTED | — |
| star_sitting_home | [] | neutral | COMPUTED | 0 hits — every star displaced from home; center star additionally lodged outward |
| door_at_original_palace | ['9'] | neutral | COMPUTED | — |
| lodged_star_or_stem | ['3', '5', '2'] | displacement | COMPUTED | — |
| empty_center | ['5'] | structural | COMPUTED | — |
| split_star_strength | ['1', '2', '3', '4', '8', '9'] | mixed_climate | COMPUTED | — |
| seasonal_vs_day_element | ['meta'] | climate | COMPUTED | day element Water is Strong this season — the day substance is seasonally supported |
| sanqi_positions | ['4', '7', '8'] | quality | COMPUTED | — |
| stacked_pillar_branch_on_palace | ['4', '6', '7', '9'] | timing_lock | COMPUTED | — |
| explicit_pattern_conflict | ['9'] | anomaly | COMPUTED | — |
| marker_validation_mismatch | ['2', '6', '8'] | note | COMPUTED | computed horses in palaces 2/6/8 carry no explicit Horse marker; absence is recorded, not treated as false |
| opposite_palace_mismatch | ['1', '2', '3', '4', '6', '7', '8', '9'] | anomaly | COMPUTED | all 8 explicit opposite labels conflict with frozen geometry; several are internally inconsistent name-number labels; frozen geometry controls computed opposition |
| earthly_escape | ['7'] | auspicious | COMPUTED | — |
| Bing + Open Door (co-location absent; heavenly_escape NOT named) | ['7', '2'] | unqualified | COMPUTED | pieces exist separately but not co-located; combination stored, name withheld per rule |
| Ding + Open Door (co-location absent; human_escape NOT named) | ['8', '2'] | unqualified | COMPUTED | pieces exist separately but not co-located; combination stored, name withheld per rule |
| six_instrument_punishment_match | ['2', '3', '4', '8', '9'] | inauspicious_validated | COMPUTED | all six liu-yi punishment field entries (Wu@3, Ji@2, Geng@8, Xin@9, Ren@4, Gui@4) validate against the classical punishment-palace table — chart internals consistent |
| original_position_consistency | ['1', '2', '3', '4', '6', '7', '8', '9'] | structural | COMPUTED | explicit original_position branches/star/door blocks verified consistent with frozen geometry; deity divergences expected (rotation); numbers kept opaque; opposite labels remain anomalous (ANO-004..011) |

Naming discipline: **earthly_escape** named (both pieces co-located in palace 7). Heavenly/human escapes stored as unnamed combinations only — pieces exist but are not co-located.

See also: [[Chart-Board-Synthesis]] · [[Chart-Analysis-Report]] · [[MOC]]