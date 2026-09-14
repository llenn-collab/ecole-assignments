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
| Field coverage | 242/242 leaf paths (complete) |
| P7 subsystem findings | 32 |

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

- `BEST-LIFE-DOOR-NE-P8-WITH-LIUHE` | COMPUTED | score 0.72

**Work through palace 6 (Northwest): Open door and Ding, both Prosperous, with Tian Xin (Heart) - the only place on the board with a working method and quality at the same time.**

- `BEST-OPEN-DOOR-NW-P6-WITH-DING` | COMPUTED | score 0.64

  Separated from palace 8 in the P7 amendment by the birth-stage/tomb opposition on the day stem Bing: palace 8 is Bing's birth stage, palace 6 is Bing's tomb. Retained as a live co-candidate and the preferred route for quality, finishing or reputation work, because it holds the only Prosperous door carrying a San Qi stem and the actor's own day branch Xu sits there. It is rejected only as the primary route for the actor's own development.

**Work through palace 7 (West): Jing (Fear) door Prosperous with Gui and Jiu Di.**

- `BEST-JING-FEAR-W-P7` | COMPUTED | score 0.515

  The door is Prosperous but it is the Fear door under a 'Heavenly Net Spread' affliction with Nine Earths concealment. It is a defensive position, not a path to a result.

### Rejected outright

- **Use the horse star at palace 2 to force movement.** (`BEST-RIDE-THE-HORSE-AT-P2`, score 0.3037) - Palace 2 is void, carries the Death door, is clash- and self-punished, and entombs Jia. Movement launched from here has no ground under it. Vetoed by board consistency.

- **Double down on the duty palace and push the showpiece harder.** (`BEST-PUSH-THE-SHOWPIECE-AT-P9`, score 0.2725) - Palace 9 is void, Imprisoned in both door and palace, triple-afflicted and Fu Yin. Amplifying it amplifies nothing. Directly contradicted by the AR-HIDDEN-01 winner, so it fails the cross-palace consistency check.

*Margin:* AMENDED IN P7. The earlier run scored these 0.6887 to 0.6487 and declined to separate them, stating that the discriminator would have to come from assignment information. That was wrong, and the correction matters: the discriminator was sitting unread in the chart itself. `palaces.8.palace_stem_rules.stems_in_birth_stage` contains Bing, the day stem, while `palaces.6.palace_stem_rules.stems_in_tomb` contains the same Bing. Palace 8 is where the actor is born; palace 6 is where the actor is buried. That is a polar opposition on the single most important stem in the chart, and it separates the two candidates without any appeal to the assignment. Amended scores: palace 8 0.72, palace 6 0.64. Palace 6 is NOT discarded - it retains the only Prosperous door on a San Qi stem and holds the actor's own day branch Xu, so it remains the correct choice for anything requiring quality or finishing rather than growth. But as a route for the actor to survive and develop, palace 8 now wins on the chart's own evidence.

### The one thing both surviving paths agree on

Neither of them is palace 9. The chart's own showpiece is the one place the chart says not to push. Both viable routes are away from the duty palace - one inward to Northwest quality, one outward to Northeast partnership. On a Fu Yin board neither happens without deliberate external force.

## 4. Timing

- Metal is **Prosperous** and Water **Strengthening**. Earth is Resting. Fire is **Imprisoned** and Wood is **Dead**.
- The day stem Bing is Fire: **Imprisoned**. The hour stem Jia is Wood: **Dead**.
- Both the actor and the matter are out of season. The two elements the season actually supports, Metal and Water, are exactly the elements sitting at palaces 6, 7 (Metal) and 1, 8 (Water stem Ren at 8, Geng at 1).
- Year branch Wu and hour branch Wu both stack on palace 9, which is void. Timing pressure is pointed at something that cannot receive it.

The seasonal reading and the positional reading agree, which is worth noting: the strong palaces are strong because their element is in season, not because of where they sit. That makes the strength readings unusually trustworthy here.

## 5. Full-field subsystem findings

The first pass through this chart analysed the stems, doors, stars, markers and pillars, and left roughly 40% of the file's fields unread. This section covers everything that was missed: the He Tu numbers, the trigram numbers, the Early Heaven arrangement, the home/active displacement layer, the harm and birth-stage rules, the star energy sub-states, the per-element prosperity map, the solar-term cross-check, the full branch system, and the school declaration. Two of these findings changed conclusions that the earlier pass had already published.

### System, school and method

**[+] school_and_method_declared** (palaces *)

The chart declares school `Yi Yun - Lun Zang Jia`, type `Hour Rotation Chart`, method `Chai Bu Method`. This is a Yi Yun Lun Zang Jia hour-rotation chart built by the Chai Bu (splitting/tearing) method. Two consequences constrain this analysis: hour-rotation means the plate is specific to this hour and its conclusions decay with the hour, and Lun Zang Jia ('discussing the hidden Jia') is precisely the tradition in which the Jia stem is never shown directly but read through its decade proxy. The absence of Jia from every plate is therefore native to the method, not a defect in the export - which downgrades the earlier HOUR_STEM_NOT_ON_PLATE anomaly from a data problem to an expected feature.

### Solar term validation

**[+] structure_matches_solar_term_and_yuan** (palaces *)

`timing.solar_term` reads White Dew, Middle yuan, day 3, and `chart_config.structure` reads Yin Dun 3. For White Dew Middle yuan the canonical structure is Yin Dun 3. These agree, so the chart's own header is self-consistent and the plate was constructed from the stated moment rather than assembled arbitrarily. Every seasonal judgement in this package rests on that agreement.

**[=] white_dew_is_the_metal_gate** (palaces *)

White Dew is the term at which autumn Metal takes over decisively and moisture begins to condense - which is exactly what `element_prosperities` reports (Metal Prosperous, Water Strengthening, Wood Dead). The named term and the numeric prosperity table corroborate each other independently. Day 3 of the middle yuan places this early in that period, so the Metal reading is establishing rather than exhausting.

### Palace id integrity

**[+] id_integrity_confirmed** (palaces 1, 2, 3, 4, 5, 6, 7, 8, 9)

Every palace's `id` field matches both its object key and its canonical Later Heaven (Hou Tian) palace number. The nine-palace indexing is sound, so no verdict in this package rests on a mis-keyed palace.

### Trigram numbers and Early Heaven

**[+] trigram_numbers_decoded** (palaces )

The two-number `trigram_numbers` array is not arbitrary: at palaces  it is exactly [Early Heaven number, Later Heaven number]. For example palace 1 Kan carries [6, 1] - Kan is 6 in the Early Heaven arrangement and 1 in the Later Heaven arrangement. This field was previously uninterpreted; it encodes each palace's position in both arrangements simultaneously.

**[+] early_heaven_labels_verified** (palaces 1, 2, 3, 4, 6, 7, 8, 9)

Every `early_heaven_trigram` label carries the correct canonical Fu Xi number (8/8 verified). The chart's Early Heaven layer is internally consistent and can be trusted as a cross-check.

**[=] early_vs_later_heaven_element_shift** (palaces 1, 2, 3, 4, 6, 7, 8, 9)

At palaces 1, 2, 3, 4, 6, 7, 8, 9 the Early Heaven trigram's element differs from the Later Heaven palace element - the palace's original nature differs from its manifest nature. Palace 9 (Li, Fire) sits on Early Heaven Qian (Metal): the showpiece position is originally a Metal/authority seat wearing a Fire/visibility face. Palace 2 (Kun, Earth) sits on Early Heaven Xun (Wood): the actor's host is originally a Wood seat, and Wood is Dead this season, which deepens the weakness already found there.

### He Tu numbers

**[+] hetu_element_seasonal_support** (palaces 1, 6, 7)

By He Tu pairing, palaces 1, 6, 7 carry an element the season supports (Metal 4-9, Water 1-6). These are the palaces whose *deep structure*, not merely their surface placement, is in phase with White Dew.

**[-] hetu_element_seasonally_dead** (palaces 3, 4, 9)

Palaces 3, 4, 9 carry a He Tu element the season kills (Wood 3-8, Fire 2-7). Palace 9's He Tu pair is 2-7 Fire, and Fire is Imprisoned - the duty palace is structurally out of season at the He Tu layer as well as the surface layer, which is an independent confirmation of the void showpiece finding.

**[=] shared_earth_axis_5_10** (palaces 2, 5, 8)

Palaces 2, 5, 8 all share the He Tu pair 5-10 (Earth). The Centre (5), the actor's host (2) and the clean outer palace (8) are bound onto one Earth axis. This is the structural reason the displaced day stem can lodge into palace 2 at all, and it is also the channel that connects palace 2 to palace 8.

### Home versus active displacement

**[-] doors_and_stars_have_not_moved** (palaces 1, 2, 3, 4, 5, 6, 7, 8, 9)

Comparing `base_position.home_door`/`home_star` against `active_chart` across all nine palaces: 0 doors moved and 0 stars moved. This is the independent proof of Fu Yin from the base-position layer, which the earlier analysis asserted from the stems alone. The declaration at `chart_config.chart_pattern` is now confirmed from three separate directions.

**[+] only_the_spirits_moved** (palaces 1, 2, 4, 6, 8, 9)

The spirits are the sole moving system on this board. Displaced at palaces 1, 2, 4, 6, 8, 9. On a totally frozen Fu Yin plate, the spirit layer carries every bit of the chart's dynamic information - it is the only place where anything is telling you about change rather than stasis.

**[-] zhi_fu_bai_hu_axis_swap** (palaces 1, 9)

Zhi Fu (Chief) belongs to palace 1 by `home_god` but is active at palace 9; Bai Hu (White Tiger) is listed among palace 9's home gods but is active at palace 1. Authority and predation have traded ends of the Kan-Li axis. Authority has walked onto the void, triple-afflicted showpiece, while the Tiger now sits on the North palace whose star is Obsolete by palace relation. Command has gone somewhere it cannot act, and aggression has gone somewhere nobody is watching.

**[-] jiu_tian_to_the_actors_host** (palaces 2, 6)

Jiu Tian (Nine Heavens) is the home god of palace 6 but is active at palace 2. The expansion/high-ground spirit has left the one Prosperous palace and landed on the void, Death-door palace that hosts the displaced day stem. Read together with the horse star already found at palace 2, the chart puts both of its movement signals - Nine Heavens and the horse - on the actor's compromised seat. The urge to expand is real and is located precisely where there is no ground to expand from.

**[+] spirits_that_stayed_home** (palaces 3, 7)

Tai Yin (Moon) at palace 3, Liu He (Six Harmony) at palace 8 by way of palace 4's home listing, Jiu Di (Nine Earths) at palace 7 and Teng She (Serpent) at palace 4 are the anchored spirits. Jiu Di staying home at palace 7 reinforces that palace's concealment reading, and Liu He arriving at palace 8 - from palace 4, a Dead-door void palace - is the single constructive spirit movement on the entire board.

### Harm rules

**[+] harm_rules_are_latent_not_active** (palaces 2, 3, 4, 6, 7, 8)

Five palaces declare `stems_in_harm` (2:Wu, 3:Ren, 4:Gui, 6:Geng, 7:Ji, 8:Xin). Checking each against the stem actually sitting there: none of them is occupied by its own harmed stem, so every harm rule on this board is latent rather than active. This matters because it removes a whole category of damage that a careless reading would have charged against palaces 6 and 8 - the two surviving solution paths. Neither is actually being harmed.

**[-] harm_target_locations** (palaces 2, 3, 4, 6, 7, 8)

Cross-referencing each harm rule to where its target stem actually sits: palace 2 harms Wu, which sits at ['3']; palace 3 harms Ren, which sits at ['8']; palace 4 harms Gui, which sits at ['7']; palace 6 harms Geng, which sits at ['1']; palace 7 harms Ji, which sits at ['2']; palace 8 harms Xin, which sits at ['9']. Note palace 8 harms Xin, and Xin is the lead-proxy stem at the duty palace 9. So the clean outer route (8) stands in a harm relationship to the showpiece's visible stem - taking the palace 8 path implies some friction with the duty palace's public face, even though palace 8 itself is undamaged.

### Birth-stage rules

**[=] birth_stage_rules_mostly_latent** (palaces 1, 2, 3, 4, 7, 8, 9)

Seven palaces declare `stems_in_birth_stage` (1:Xin, 2:Ren, 3:Gui, 4:Geng, 7:Ding+Ji, 8:Bing+Wu, 9:Yi). Checking occupancy: no palace is occupied by a stem in its own birth stage. The birth-stage layer therefore adds no active reinforcement anywhere.

**[+] day_stem_birth_stage_at_palace_8** (palaces 8)

Palace 8 lists Bing among its birth-stage stems. Bing is the day stem - the actor. So the one clean, unafflicted, void-free palace on this board is also the palace where the actor's element is in its birth stage. Set against palace 6, which is Bing's *tomb*, the two surviving routes are revealed as exact opposites for the actor: palace 8 is where Bing is born, palace 6 is where Bing is buried. This is the sharpest single discriminator the chart offers between the two candidates, and it was entirely missing from the earlier analysis.

**[=] lead_proxy_birth_stage_at_palace_1** (palaces 1)

Palace 1 lists Xin - the lead-stem proxy for the invisible Jia-Wu decade - in its birth stage. Xin is active at palace 9. Palace 1 is Xin's origin point and is also where Bai Hu (White Tiger) has just arrived. The public face of the matter is born in the North, in a palace whose star is Obsolete and which now holds the Tiger.

### Star energy sub-states

**[=] seasonal_column_is_uniform** (palaces 1, 2, 3, 4, 6, 7, 8, 9)

Every single palace reports `star.seasonal = Strengthening`. A column with no variance carries no discriminating information, so any ranking that leaned on seasonal star strength would be ranking on noise. All real star information in this chart lives in `palace_relation`.

**[=] stars_outperforming_their_season** (palaces 2, 8)

At palaces 2, 8 the star is stronger by palace relation than by season - these stars are being carried by their location. Palaces 2 and 8 both reach Prosperous. Palace 2's Tian Rui is the illness star, so a Prosperous reading there means the illness is well-fed, not that the palace is healthy. Palace 8's Tian Ren (Ambassador) reaching Prosperous is a genuine positive and reinforces the palace 8 route.

**[-] stars_undercut_by_their_palace** (palaces 1, 3, 4, 9)

At palaces 1, 3, 4, 9 the star is weaker by palace relation than by season. Palace 1's Tian Peng falls all the way to Obsolete - the single worst star reading on the board. Palace 9's Tian Ying (Hero), the duty star itself, drops to Resting: the star that is supposed to carry the matter is the fifth-weakest on the board by location.

### Element prosperity across the board

**[+] metal_prosperous_owns_the_working_half** (palaces 6, 7)

Metal is Prosperous. That single fact governs palaces 6 and 7, the stems Geng and Xin, the doors Kai (Open) and Jing (Fear), and the stars Tian Xin and Tian Zhu. Both Prosperous doors on this board are Metal doors. The chart's entire working capacity is Metal-shaped: cutting, deciding, finishing, publishing, closing. Nothing soft is in season.

**[+] water_strengthening_is_the_rising_current** (palaces 1, 8)

Water is Strengthening - the only element on the rise. It appears as the stem Ren at palace 8, the stem Gui at palace 7, the Xiu (Rest) door at palace 1 and the star Tian Peng. Palace 8 carrying a Strengthening-element stem is a further independent mark in favour of the palace 8 route: it is the only candidate route whose stem element is gaining rather than peaking.

**[-] wood_dead_erases_the_hour_stem** (palaces 3, 4)

Wood is Dead. This kills palaces 3 and 4 outright (both Dead in door and palace), kills the stem Yi at palace 4, and - most importantly - kills Jia, which is the hour stem and does not appear on the plate at all. The matter in motion is made of the one element the season has already finished with.

**[-] fire_imprisoned_traps_the_actor_and_the_showpiece** (palaces 5, 9)

Fire is Imprisoned. Fire is the day stem Bing (the actor, stranded in the Centre), the stem Ding at palace 6, the Jing (Scenery) door and the duty star Tian Ying - and palace 9 itself. So the actor, the duty star, the duty door and the duty palace are all made of an Imprisoned element. That is four independent confirmations of the same weakness, and it explains why the showpiece cannot hold regardless of how it is played.

**[=] earth_resting_is_the_neutral_ground** (palaces 2, 5, 8)

Earth is Resting - neither helped nor harmed. Earth is palaces 2, 5 and 8, the stems Wu and Ji, and the Sheng (Life) and Si (Death) doors. Palace 8's Life door being Resting rather than Prosperous is the honest cost of that route: it works, but it is not energised, so it will need deliberate push. This is precisely the 0.040 gap between palace 8 and palace 6.

### Earthly branch system

**[=] twelve_branches_fully_mapped** (palaces 1, 2, 3, 4, 5, 6, 7, 8, 9)

All twelve earthly branches are distributed across the eight directional palaces (the Centre holds none). Of the twelve, four are occupied by pillars (Wu (Horse), Xu (Dog), You (Rooster)) and eight are unoccupied. The four void branches are Wu (Horse), Wei (Goat), Chen (Dragon), Si (Snake), which map to palaces 2, 4 and 9 - matching the chart's own void flags exactly.

**[-] palace_9_single_branch_fully_loaded** (palaces 9)

Palace 9 holds exactly one branch, Wu (Horse) - and both the year pillar and the hour pillar carry Wu. A single-branch palace receiving a doubled pillar branch has no room to distribute the load, unlike palaces 2, 4, 6 and 8 which hold two branches each. The duty palace is the narrowest palace on the board and is carrying the heaviest branch concentration, while being void. Structurally it cannot absorb what is being put on it.

**[=] day_branch_xu_sits_with_the_open_door** (palaces 6)

The day branch is Xu (Dog), which belongs to palace 6 - the Open-door, Ding, Tian Xin palace. The actor's own branch already sits at the strongest palace on the board, even though the actor's stem is stranded in the Centre. Stem and branch of the day pillar are split between the weakest position (Centre, no seat) and the strongest (palace 6). That split is the clearest statement of the chart's central tension, and it is also why palace 6 keeps scoring highly despite being Bing's tomb.

**[+] month_branch_you_anchors_the_metal_season** (palaces 7)

The month branch is You (Rooster), which belongs to palace 7 - pure Metal, Prosperous door, Prosperous palace. The month pillar is the seasonal authority, and it lands on the palace that most purely expresses the prosperous element. This is why the Metal reading throughout this chart is trustworthy: the season's own branch is sitting in its own house.

## 6. Overrides applied to earlier conclusions

Later evidence overrode earlier verdicts twice. In both cases the original verdict is preserved rather than deleted, and both the old and new evidence are cited.

### OVR-001 - AR-BEST-01

- **Was:** {"old_margin_claim": "Declared unresolvable from the chart alone; claimed the separator was assignment information.", "scores": {"BEST-JING-FEAR-W-P7": 0.515, "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE": 0.6887, "BEST-OPEN-DOOR-NW-P6-WITH-DING": 0.6487, "BEST-PUSH-THE-SHOWPIECE-AT-P9": 0.2725, "BEST-RIDE-THE-HORSE-AT-P2": 0.3037}, "status": "RESOLVED (narrow)", "winner": "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE"}
- **Now:** {"scores": {"BEST-JING-FEAR-W-P7": 0.515, "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE": 0.72, "BEST-OPEN-DOOR-NW-P6-WITH-DING": 0.64, "BEST-PUSH-THE-SHOWPIECE-AT-P9": 0.2725, "BEST-RIDE-THE-HORSE-AT-P2": 0.3037}, "status": "RESOLVED_BY_AMENDMENT", "winner": "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE"}
- **Why:** P7 read fields the earlier run never opened. The birth-stage field resolves a tie the earlier run wrongly declared unresolvable. Early verdict is preserved above, not deleted.

Old evidence:

- `palaces.6.active_chart.energy_state.door`
- `palaces.8.active_chart.energy_state.door`

New evidence:

- `palaces.8.palace_stem_rules.stems_in_birth_stage`
- `palaces.6.palace_stem_rules.stems_in_tomb`
- `palaces.6.base_position.earthly_branches`
- `element_prosperities.water`

### OVR-002 - ANOMALY:HOUR_STEM_NOT_ON_PLATE

- **Was:** {"severity": "HIGH"}
- **Now:** {"severity": "LOW", "status": "DOWNGRADED_BY_P7"}
- **Why:** The school declaration explains the absence as native to the method. Severity corrected; the anomaly is retained, not deleted.

Old evidence:

- `timing.four_pillars.hour`
- `chart_config.lead_stem`

New evidence:

- `system.school`
- `system.method`

## 7. Anomalies and honest limits

- **SCHEMA_AMBIGUITY** (HIGH) - QMDJ.json does not expose chart_metadata.* / heaven_plate.* / markers.* as named in qmdj_complete.schema_bind. Least-contradicted bind applied: timing.four_pillars -> four_pillars, chart_config -> duty_elements, element_prosperities -> seasonal_element_strengths, palaces.N.active_chart.stems.heaven -> heaven_plate.stem, palaces.N.active_chart.stems.earth -> earth_plate.stem, palaces.N.active_chart.stems.hidden -> hidden_stem, palaces.N.active_chart.status -> markers, palaces.N.palace_stem_rules.stems_in_tomb -> tomb_stems, palaces.N.palace_stem_rules.stems_in_clash_punishment -> punishment_stems. binding_failure_policy: continue, do not ask user.
- **TIAN_YI_ABSENT** (LOW) - chart_metadata.duty_elements.tian_yi has no counterpart in this schema; help/quality interpretation class falls back to Zhi Fu (Chief).
- **DAY_STEM_IN_CENTRE** (HIGH) - Day stem Bing sits in the Centre (palace 5) and is lodged into palace 2. B1 primary is therefore a lodging graph, not a simple palace.
- **HOUR_STEM_NOT_ON_PLATE** (LOW) - Hour stem Jia is absent from all plates; proxy set used (lead_stem_proxy Xin, tomb of Jia, hour branch palace). DOWNGRADED FROM HIGH TO LOW IN P7: `system.school` declares Yi Yun - Lun Zang Jia, literally 'discussing the hidden Jia', a tradition in which Jia is never displayed on the plate and is always read through its decade proxy stem. The absence is native to the method, not a defect in the data. The proxy handling already applied was the correct procedure, so no downstream verdict changes - only the severity label.

Three of these materially constrain the analysis:

1. **The schema is not the one the specification expects.** This export uses `timing.*`, `chart_config.*` and `active_chart.*` rather than `chart_metadata.*` and `heaven_plate.*`. A least-contradicted binding was applied and is documented in full in [[Chart-Schema]]. No claim depends on a guessed field.
2. **There is no explicit answer anywhere in this chart.** No `my_answers`, no `hidden_problems`, no `best_solution`, no `yongshen` field exists. Every headline in this report is COMPUTED from values, not read from a slot. The only explicit interpretive field in the file is `chart_config.chart_pattern` = Fu Yin.
3. **Fields the specification names that this chart does not have:** `door.forced`, `tian_yi`, `lodged_star`/`lodged_stem`, `hour_stem_focus`. No forced-door claim and no Tian Yi claim is made anywhere, because the data does not support one.

## 8. Yongshen candidates (unbound)

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

## 10. Verification

| gate | result |
|---|---|
| Field coverage | 242/242 leaf paths, 0 uncited |
| Package schema valid | True |
| Citation integrity | 630 checked, 0 broken |
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

