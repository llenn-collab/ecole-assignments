---
id: chart-analysis-report
type: report
phase: PACKAGE_RENDER
batch: "-"
palace_ids: ["1","2","3","4","5","6","7","8","9"]
sources: ["raw/state/chart_analysis_package.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# Chart Analysis Report

**Chart-only analysis. No assignment was read, and nothing here is bound to a requirement.** Every conclusion below is evidence for a downstream solver, not a submission. Where the chart is ambiguous the ambiguity is preserved rather than resolved.

## Infobox

| key | value |
|---|---|
| Source | `QMDJ/ADVERTISING/project_1.json` |
| sha256 | `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7` |
| Package version | 4.0.0 |
| System | Yi Yun - Lun Zang Jia, Hour Rotation Chart, Chai Bu Method |
| Structure | Yin Dun 3 |
| Solar term | White Dew, Middle yuan, day 3 |
| Four pillars | Bing-Wu / Ding-You / Bing-Xu / Jia-Wu |
| Chart pattern | Fu Yin (All elements in home positions) |
| Duty star / door | Tian Ying (Hero) / Jing (Scenery), palace 9 |
| Void palaces | 2, 4, 9 |
| Horse palace | 2 |
| Verdicts | 43 across 9 palaces |
| Pattern hits | 54 |
| Anomalies | 4 |

## Lead

This is a completely static board. The chart declares Fu Yin and the declaration checks out independently: in all nine palaces the heaven, earth and hidden stems are the same stem, every star sits in its Luo Shu home, and every door sits at its original palace. Nothing on this board moves by itself.

Against that frozen background, three facts do the real work. The day stem **Bing** - the actor - is stranded in the Centre and has to borrow palace 2 to exist at all. The hour stem **Jia** - the matter in motion - does not appear on any plate anywhere, and Wood is Dead this season. And the duty palace, the thing the chart says the question is actually about, is **void**, imprisoned in both door and palace, and carries three stacked afflictions at once.

The short version: the visible centrepiece is the weakest thing on the board, the actor has no ground of its own, and nothing will change unless it is changed deliberately from outside.

## 1. What the chart says the matter is

**The subject of the question is the showpiece at palace 9, and it is void.**

- archetype `ANS-DUTY-PALACE-9-VOID-SHOWPIECE` | grounding EXPLICIT | score 0.86 | resolution `AR-ANSWERS-01`

Palace 9 (Li, South) is flagged `is_duty_palace`, carries the duty star Tian Ying (Hero) and the duty door Jing (Scenery), and holds Xin - the visible stand-in stem for the invisible Jia-Wu decade named in `chart_config.lead_stem`. Four separate header fields point at the same palace, so the subject of this chart is not in doubt.

What is in doubt is whether it holds. The same palace is void, its door is Imprisoned, the palace itself is Imprisoned, and it carries `Clash Punishment (Ji Xing)`, `Self Punishment` and `Fu Yin` simultaneously. The year branch Wu and the hour branch Wu both stack onto it. The chart concentrates all its attention - and all its timing - on a position that is explicitly marked as not landing.

Tian Ying (Hero) is the showpiece star, Jing (Scenery) is the showpiece door, and Li is the palace of visibility, reputation and display. This is a chart about something *being seen*. The void says it is seen but not received.

**Secondary answer, retained live:**

- The actor (day stem Bing) has no seat of its own and operates through palace 2. (`ANS-ACTOR-DISPLACED-TO-CENTRE`, score 0.7975)

  Not selected as the headline answer because it answers a different question: it describes where the actor stands, not what the chart says the matter is. Retained as a live secondary answer - it is not contradicted by anything on the board.

*Margin:* The runner-up (actor displaced to the Centre) is only 0.05 behind and is not really a rival: it describes the same situation from the actor's side rather than the subject's side. Both are kept live. The decision would flip only if the chart exposed an explicit yongshen field pointing somewhere other than palace 9.

## 2. Hidden problems

The chart carries five distinct problems. They are listed in scored order, but the top four are all live and none of them cancels another.

**1. The showpiece is void and punished: the loudest, most visible element is the one that will not hold.** **(headline)**

- `HID-VOID-SHOWPIECE-UNDER-PUNISHMENT` | EXPLICIT | score 0.9 | supporting paths 8, contradicting 0

**2. The actor's only landing place (palace 2) is void, horse-struck, self-punished and carries the Death door.**

- `HID-ACTORS-ONLY-SEAT-IS-A-DEATH-DOOR` | EXPLICIT | score 0.8688 | supporting paths 7, contradicting 0

**3. Whole-board Fu Yin: nothing moves on its own, so no result appears without deliberate external force.**

- `HID-TOTAL-FU-YIN-STASIS` | EXPLICIT | score 0.7975 | supporting paths 6, contradicting 1

**4. The most attractive palace (6, Open door + Ding, both Prosperous) is simultaneously the tomb of the day stem.**

- `HID-BEST-EXIT-IS-THE-SELF-TOMB` | COMPUTED | score 0.6262 | supporting paths 5, contradicting 1

**5. The hour stem Jia is absent from every plate and Wood is Dead: the matter in motion has no visible body this season.**

- `HID-WOOD-DEAD-KILLS-THE-HOUR` | COMPUTED | score 0.595 | supporting paths 4, contradicting 1

### Why the actor's position is the sharpest of these

Palace 2 is where the day stem has to live, and palace 2 is the worst-conditioned palace on the board. It is void. It carries the horse star, so it will not stay still. Its door is Si (Death). Its stems carry `Clash Punishment (Ji Xing)` and `Self Punishment`. It is the tomb of Jia - which is the hour stem, the matter in motion - and the tomb of Gui. The star Tian Rui (Grain) is the illness star.

So the actor's only seat is void, moving, punished, and is simultaneously the grave of the very thing being asked about. That is not a subtle warning.

### The trap that is easy to miss

Palace 6 is the most attractive palace on the board - Open door and Ding, both Prosperous, with Tian Xin (Heart), the healing star. It is also, per `palaces.6.palace_stem_rules.stems_in_tomb`, the tomb of Bing. The single best-looking room on the board is the one that buries the actor. Any recommendation that routes through palace 6 has to carry this warning with it.

*Margin:* The top two are separated by roughly 0.03. They are not mutually exclusive and both remain live hidden problems: one describes the subject, the other the actor's seat. Nothing in the chart would demote either short of an explicit metadata override.

## 3. Best available paths

No path on this board is clean. The two best candidates are close enough that the chart alone does not separate them, and the difference between them is a question about the assignment that this analysis is not permitted to ask.

**Work through palace 8 (Northeast): Life door with Liu He (Six Harmony) and Ren, star Prosperous by palace, no void, no affliction - the only clean outer palace, i.e. the only clean way to reach an audience.** **(leading)**

- `BEST-LIFE-DOOR-NE-P8-WITH-LIUHE` | COMPUTED | score 0.6887

**Work through palace 6 (Northwest): Open door and Ding, both Prosperous, with Tian Xin (Heart) - the only place on the board with a working method and quality at the same time.**

- `BEST-OPEN-DOOR-NW-P6-WITH-DING` | COMPUTED | score 0.6487

  Edged out by palace 8 on contradiction count only, because palace 6 is the tomb of the day stem Bing: the best-looking room on the board is also the one that buries the actor. Retained as a live co-candidate, not discarded - it wins outright if the matter is inner rather than outer.

**Work through palace 7 (West): Jing (Fear) door Prosperous with Gui and Jiu Di.**

- `BEST-JING-FEAR-W-P7` | COMPUTED | score 0.515

  The door is Prosperous but it is the Fear door under a 'Heavenly Net Spread' affliction with Nine Earths concealment. It is a defensive position, not a path to a result.

### Rejected outright

- **Use the horse star at palace 2 to force movement.** (`BEST-RIDE-THE-HORSE-AT-P2`, score 0.3037) - Palace 2 is void, carries the Death door, is clash- and self-punished, and entombs Jia. Movement launched from here has no ground under it. Vetoed by board consistency.

- **Double down on the duty palace and push the showpiece harder.** (`BEST-PUSH-THE-SHOWPIECE-AT-P9`, score 0.2725) - Palace 9 is void, Imprisoned in both door and palace, triple-afflicted and Fu Yin. Amplifying it amplifies nothing. Directly contradicted by the AR-HIDDEN-01 winner, so it fails the cross-palace consistency check.

*Margin:* Narrow win, not a comfortable one: palace 8 leads palace 6 by 0.040 on a 0-1 scale. The only separator is the contradiction count - palace 6 is the tomb of the day stem Bing, which palace 8 is not. Everything else is level: same grounding tier, same corroboration, both pass board consistency. The decision would flip to palace 6 if the matter turns out to be inner (process, institution, quality of the thing itself) rather than outer (audience, reach, agreement), because palace 6 carries the San Qi stem and the Prosperous Open door while palace 8's Life door is only Resting. That inner/outer determination is assignment information, which Prompt 1 is forbidden to use, so palace 6 is retained as a live runner-up rather than discarded.

### The one thing both surviving paths agree on

Neither of them is palace 9. The chart's own showpiece is the one place the chart says not to push. Both viable routes are away from the duty palace - one inward to Northwest quality, one outward to Northeast partnership. On a Fu Yin board neither happens without deliberate external force.

## 4. Timing

- Metal is **Prosperous** and Water **Strengthening**. Earth is Resting. Fire is **Imprisoned** and Wood is **Dead**.
- The day stem Bing is Fire: **Imprisoned**. The hour stem Jia is Wood: **Dead**.
- Both the actor and the matter are out of season. The two elements the season actually supports, Metal and Water, are exactly the elements sitting at palaces 6, 7 (Metal) and 1, 8 (Water stem Ren at 8, Geng at 1).
- Year branch Wu and hour branch Wu both stack on palace 9, which is void. Timing pressure is pointed at something that cannot receive it.

The seasonal reading and the positional reading agree, which is worth noting: the strong palaces are strong because their element is in season, not because of where they sit. That makes the strength readings unusually trustworthy here.

## 5. Anomalies and honest limits

- **SCHEMA_AMBIGUITY** (HIGH) - QMDJ.json does not expose chart_metadata.* / heaven_plate.* / markers.* as named in qmdj_complete.schema_bind. Least-contradicted bind applied: timing.four_pillars -> four_pillars, chart_config -> duty_elements, element_prosperities -> seasonal_element_strengths, palaces.N.active_chart.stems.heaven -> heaven_plate.stem, palaces.N.active_chart.stems.earth -> earth_plate.stem, palaces.N.active_chart.stems.hidden -> hidden_stem, palaces.N.active_chart.status -> markers, palaces.N.palace_stem_rules.stems_in_tomb -> tomb_stems, palaces.N.palace_stem_rules.stems_in_clash_punishment -> punishment_stems. binding_failure_policy: continue, do not ask user.
- **TIAN_YI_ABSENT** (LOW) - chart_metadata.duty_elements.tian_yi has no counterpart in this schema; help/quality interpretation class falls back to Zhi Fu (Chief).
- **DAY_STEM_IN_CENTRE** (HIGH) - Day stem Bing sits in the Centre (palace 5) and is lodged into palace 2. B1 primary is therefore a lodging graph, not a simple palace.
- **HOUR_STEM_NOT_ON_PLATE** (HIGH) - Hour stem Jia is absent from all plates; proxy set used (lead_stem_proxy Xin, tomb of Jia, hour branch palace).

Three of these materially constrain the analysis:

1. **The schema is not the one the specification expects.** This export uses `timing.*`, `chart_config.*` and `active_chart.*` rather than `chart_metadata.*` and `heaven_plate.*`. A least-contradicted binding was applied and is documented in full in [[Chart-Schema]]. No claim depends on a guessed field.
2. **There is no explicit answer anywhere in this chart.** No `my_answers`, no `hidden_problems`, no `best_solution`, no `yongshen` field exists. Every headline in this report is COMPUTED from values, not read from a slot. The only explicit interpretive field in the file is `chart_config.chart_pattern` = Fu Yin.
3. **Fields the specification names that this chart does not have:** `door.forced`, `tian_yi`, `lodged_star`/`lodged_stem`, `hour_stem_focus`. No forced-door claim and no Tian Yi claim is made anywhere, because the data does not support one.

## 6. Yongshen candidates (unbound)

These are candidate useful-gods derived from the chart alone. **None is bound to any requirement**, and every `requirement_fit_score` is null, as Prompt 1 requires.

| candidate | palaces | grounding | condition |
|---|---|---|---|
| Day stem Bing (self / actor) | 5, 2 | COMPUTED | Centre-lodged into a void, horse-struck, Death-door palace; Fire is Imprisoned this season; Bing's tomb is palace 6. |
| Hour stem Jia (matter in motion) | 2, 9 | COMPUTED | Absent from every plate; entombed at palace 2; proxied by Xin at palace 9; Wood is Dead this season. |
| Lead proxy stem Xin (visible stand-in) | 9 | EXPLICIT | Metal is Prosperous, but palace 9 is void, duty palace, clash-punished, self-punished and Fu Yin. |
| Duty star Tian Ying + duty door Jing (Scenery) at palace 9 | 9 | EXPLICIT | Authority of the matter; imprisoned door, imprisoned palace, void. |
| Kai (Open) door + Ding + Tian Xin at palace 6 | 6 | COMPUTED | Only Prosperous door+palace pair carrying a San Qi stem; also the tomb palace of the day stem Bing. |
| Sheng (Life) door + Ren + Liu He at palace 8 | 8 | COMPUTED | Outer realm, Resting door, Six Harmony spirit, star Prosperous by palace. |

## 7. Board consistency

- Result: **PASS** | unresolved contradictions: 0 | split claims recorded: 3

- Palace 4: Palace 4 carries both SUPPORT and VETO claims. Per the overload rule these are kept as separate typed claims and are not averaged into one verdict.
- Palace 6: Palace 6 carries both SUPPORT and VETO claims. Per the overload rule these are kept as separate typed claims and are not averaged into one verdict.
- Palace 9: Palace 9 carries both SUPPORT and VETO claims. Per the overload rule these are kept as separate typed claims and are not averaged into one verdict.

Three palaces carry both supporting and vetoing claims at the same time. Per the overload rule these are kept as separate typed claims rather than averaged into a single score - a palace really can be both the best method and a trap, and palace 6 is exactly that.

## 8. Verification

| gate | result |
|---|---|
| Package schema valid | True |
| Citation integrity | 626 checked, 0 broken |
| Board consistency | True |
| Archetype resolution present on every seed claim | True |
| requirement_fit_score null everywhere | True |
| Assignment-blind | True |

## See also

- [[Chart-Anatomy]]
- [[Chart-Board-Synthesis]]
- [[Chart-Patterns]]
- [[Chart-Red-Team]]
- [[Palace-Analysis-Index]]

## Sources

- `vault/raw/QMDJ.json`
- `vault/raw/state/chart_analysis_package.json`
- `vault/raw/state/archetype_resolutions.json`

