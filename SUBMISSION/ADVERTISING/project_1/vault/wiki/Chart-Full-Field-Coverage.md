---
id: chart-full-field-coverage
type: article
phase: P7_FULL_FIELD_COVERAGE
batch: "-"
palace_ids: ["1","2","3","4","5","6","7","8","9"]
sources: ["raw/state/full_coverage.json", "raw/QMDJ.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# Chart Full Field Coverage

Every field in `QMDJ.json` analysed, including the ten subsystems the first pass left unread. The first run cited 144 of 242 leaf paths; this layer closes the remaining 98.

## Infobox

| key | value |
|---|---|
| Leaf paths in source | 242 |
| Cited | 242 |
| Uncited | 0 |
| Subsystems | 10 |
| Findings | 32 |
| Overrides triggered | 2 |

## Why this layer exists

The first pass read the obvious fields - stems, doors, stars, markers, pillars - and stopped. It never opened `hetu_numbers`, `trigram_numbers`, `early_heaven_trigram`, `stems_in_harm`, `stems_in_birth_stage`, or any of the `home_god`/`home_door`/`home_star` base positions. Those fields turned out to contain the discriminator that broke the chart's central unresolved question.

## System, school and method

### [+] school_and_method_declared

*Palaces: * | EXPLICIT*

The chart declares school `Yi Yun - Lun Zang Jia`, type `Hour Rotation Chart`, method `Chai Bu Method`. This is a Yi Yun Lun Zang Jia hour-rotation chart built by the Chai Bu (splitting/tearing) method. Two consequences constrain this analysis: hour-rotation means the plate is specific to this hour and its conclusions decay with the hour, and Lun Zang Jia ('discussing the hidden Jia') is precisely the tradition in which the Jia stem is never shown directly but read through its decade proxy. The absence of Jia from every plate is therefore native to the method, not a defect in the export - which downgrades the earlier HOUR_STEM_NOT_ON_PLATE anomaly from a data problem to an expected feature.

- `system.school`
- `system.chart_type`
- `system.method`
- `chart_config.lead_stem`

## Solar term validation

### [+] structure_matches_solar_term_and_yuan

*Palaces: * | COMPUTED*

`timing.solar_term` reads White Dew, Middle yuan, day 3, and `chart_config.structure` reads Yin Dun 3. For White Dew Middle yuan the canonical structure is Yin Dun 3. These agree, so the chart's own header is self-consistent and the plate was constructed from the stated moment rather than assembled arbitrarily. Every seasonal judgement in this package rests on that agreement.

- `timing.solar_term.name`
- `timing.solar_term.yuan`
- `chart_config.structure`

### [=] white_dew_is_the_metal_gate

*Palaces: * | COMPUTED*

White Dew is the term at which autumn Metal takes over decisively and moisture begins to condense - which is exactly what `element_prosperities` reports (Metal Prosperous, Water Strengthening, Wood Dead). The named term and the numeric prosperity table corroborate each other independently. Day 3 of the middle yuan places this early in that period, so the Metal reading is establishing rather than exhausting.

- `timing.solar_term.name`
- `timing.solar_term.day`
- `element_prosperities.metal`

## Palace id integrity

### [+] id_integrity_confirmed

*Palaces: 1, 2, 3, 4, 5, 6, 7, 8, 9 | COMPUTED*

Every palace's `id` field matches both its object key and its canonical Later Heaven (Hou Tian) palace number. The nine-palace indexing is sound, so no verdict in this package rests on a mis-keyed palace.

- `palaces.1.id`
- `palaces.2.id`
- `palaces.3.id`
- `palaces.4.id`
- `palaces.5.id`
- `palaces.6.id`

## Trigram numbers and Early Heaven

### [+] trigram_numbers_decoded

*Palaces:  | COMPUTED*

The two-number `trigram_numbers` array is not arbitrary: at palaces  it is exactly [Early Heaven number, Later Heaven number]. For example palace 1 Kan carries [6, 1] - Kan is 6 in the Early Heaven arrangement and 1 in the Later Heaven arrangement. This field was previously uninterpreted; it encodes each palace's position in both arrangements simultaneously.


### [+] early_heaven_labels_verified

*Palaces: 1, 2, 3, 4, 6, 7, 8, 9 | COMPUTED*

Every `early_heaven_trigram` label carries the correct canonical Fu Xi number (8/8 verified). The chart's Early Heaven layer is internally consistent and can be trusted as a cross-check.

- `palaces.1.base_position.early_heaven_trigram`
- `palaces.2.base_position.early_heaven_trigram`
- `palaces.3.base_position.early_heaven_trigram`
- `palaces.4.base_position.early_heaven_trigram`
- `palaces.6.base_position.early_heaven_trigram`
- `palaces.7.base_position.early_heaven_trigram`

### [=] early_vs_later_heaven_element_shift

*Palaces: 1, 2, 3, 4, 6, 7, 8, 9 | COMPUTED*

At palaces 1, 2, 3, 4, 6, 7, 8, 9 the Early Heaven trigram's element differs from the Later Heaven palace element - the palace's original nature differs from its manifest nature. Palace 9 (Li, Fire) sits on Early Heaven Qian (Metal): the showpiece position is originally a Metal/authority seat wearing a Fire/visibility face. Palace 2 (Kun, Earth) sits on Early Heaven Xun (Wood): the actor's host is originally a Wood seat, and Wood is Dead this season, which deepens the weakness already found there.

- `palaces.1.base_position.early_heaven_trigram`
- `palaces.2.base_position.early_heaven_trigram`
- `palaces.3.base_position.early_heaven_trigram`
- `palaces.4.base_position.early_heaven_trigram`
- `palaces.6.base_position.early_heaven_trigram`
- `palaces.7.base_position.early_heaven_trigram`

## He Tu numbers

### [+] hetu_element_seasonal_support

*Palaces: 1, 6, 7 | COMPUTED*

By He Tu pairing, palaces 1, 6, 7 carry an element the season supports (Metal 4-9, Water 1-6). These are the palaces whose *deep structure*, not merely their surface placement, is in phase with White Dew.

- `palaces.1.base_position.hetu_numbers`
- `palaces.6.base_position.hetu_numbers`
- `palaces.7.base_position.hetu_numbers`

### [-] hetu_element_seasonally_dead

*Palaces: 3, 4, 9 | COMPUTED*

Palaces 3, 4, 9 carry a He Tu element the season kills (Wood 3-8, Fire 2-7). Palace 9's He Tu pair is 2-7 Fire, and Fire is Imprisoned - the duty palace is structurally out of season at the He Tu layer as well as the surface layer, which is an independent confirmation of the void showpiece finding.

- `palaces.3.base_position.hetu_numbers`
- `palaces.4.base_position.hetu_numbers`
- `palaces.9.base_position.hetu_numbers`

### [=] shared_earth_axis_5_10

*Palaces: 2, 5, 8 | COMPUTED*

Palaces 2, 5, 8 all share the He Tu pair 5-10 (Earth). The Centre (5), the actor's host (2) and the clean outer palace (8) are bound onto one Earth axis. This is the structural reason the displaced day stem can lodge into palace 2 at all, and it is also the channel that connects palace 2 to palace 8.

- `palaces.2.base_position.hetu_numbers`
- `palaces.5.base_position.hetu_numbers`
- `palaces.8.base_position.hetu_numbers`

## Home versus active displacement

### [-] doors_and_stars_have_not_moved

*Palaces: 1, 2, 3, 4, 5, 6, 7, 8, 9 | COMPUTED*

Comparing `base_position.home_door`/`home_star` against `active_chart` across all nine palaces: 0 doors moved and 0 stars moved. This is the independent proof of Fu Yin from the base-position layer, which the earlier analysis asserted from the stems alone. The declaration at `chart_config.chart_pattern` is now confirmed from three separate directions.

- `palaces.1.base_position.home_door`
- `palaces.2.base_position.home_door`
- `palaces.3.base_position.home_door`
- `palaces.4.base_position.home_door`
- `palaces.5.base_position.home_door`
- `palaces.6.base_position.home_door`

### [+] only_the_spirits_moved

*Palaces: 1, 2, 4, 6, 8, 9 | COMPUTED*

The spirits are the sole moving system on this board. Displaced at palaces 1, 2, 4, 6, 8, 9. On a totally frozen Fu Yin plate, the spirit layer carries every bit of the chart's dynamic information - it is the only place where anything is telling you about change rather than stasis.

- `palaces.1.active_chart.god`
- `palaces.2.active_chart.god`
- `palaces.4.active_chart.god`
- `palaces.6.active_chart.god`
- `palaces.8.active_chart.god`
- `palaces.9.active_chart.god`

### [-] zhi_fu_bai_hu_axis_swap

*Palaces: 1, 9 | COMPUTED*

Zhi Fu (Chief) belongs to palace 1 by `home_god` but is active at palace 9; Bai Hu (White Tiger) is listed among palace 9's home gods but is active at palace 1. Authority and predation have traded ends of the Kan-Li axis. Authority has walked onto the void, triple-afflicted showpiece, while the Tiger now sits on the North palace whose star is Obsolete by palace relation. Command has gone somewhere it cannot act, and aggression has gone somewhere nobody is watching.

- `palaces.1.base_position.home_god`
- `palaces.9.active_chart.god`
- `palaces.9.base_position.home_god`
- `palaces.1.active_chart.god`

### [-] jiu_tian_to_the_actors_host

*Palaces: 2, 6 | COMPUTED*

Jiu Tian (Nine Heavens) is the home god of palace 6 but is active at palace 2. The expansion/high-ground spirit has left the one Prosperous palace and landed on the void, Death-door palace that hosts the displaced day stem. Read together with the horse star already found at palace 2, the chart puts both of its movement signals - Nine Heavens and the horse - on the actor's compromised seat. The urge to expand is real and is located precisely where there is no ground to expand from.

- `palaces.6.base_position.home_god`
- `palaces.2.active_chart.god`
- `palaces.2.active_chart.status.has_horse_star`

### [+] spirits_that_stayed_home

*Palaces: 3, 7 | COMPUTED*

Tai Yin (Moon) at palace 3, Liu He (Six Harmony) at palace 8 by way of palace 4's home listing, Jiu Di (Nine Earths) at palace 7 and Teng She (Serpent) at palace 4 are the anchored spirits. Jiu Di staying home at palace 7 reinforces that palace's concealment reading, and Liu He arriving at palace 8 - from palace 4, a Dead-door void palace - is the single constructive spirit movement on the entire board.

- `palaces.7.active_chart.god`
- `palaces.4.base_position.home_god`
- `palaces.8.active_chart.god`

## Harm rules

### [+] harm_rules_are_latent_not_active

*Palaces: 2, 3, 4, 6, 7, 8 | COMPUTED*

Five palaces declare `stems_in_harm` (2:Wu, 3:Ren, 4:Gui, 6:Geng, 7:Ji, 8:Xin). Checking each against the stem actually sitting there: none of them is occupied by its own harmed stem, so every harm rule on this board is latent rather than active. This matters because it removes a whole category of damage that a careless reading would have charged against palaces 6 and 8 - the two surviving solution paths. Neither is actually being harmed.

- `palaces.2.palace_stem_rules.stems_in_harm`
- `palaces.3.palace_stem_rules.stems_in_harm`
- `palaces.4.palace_stem_rules.stems_in_harm`
- `palaces.6.palace_stem_rules.stems_in_harm`
- `palaces.7.palace_stem_rules.stems_in_harm`
- `palaces.8.palace_stem_rules.stems_in_harm`

### [-] harm_target_locations

*Palaces: 2, 3, 4, 6, 7, 8 | COMPUTED*

Cross-referencing each harm rule to where its target stem actually sits: palace 2 harms Wu, which sits at ['3']; palace 3 harms Ren, which sits at ['8']; palace 4 harms Gui, which sits at ['7']; palace 6 harms Geng, which sits at ['1']; palace 7 harms Ji, which sits at ['2']; palace 8 harms Xin, which sits at ['9']. Note palace 8 harms Xin, and Xin is the lead-proxy stem at the duty palace 9. So the clean outer route (8) stands in a harm relationship to the showpiece's visible stem - taking the palace 8 path implies some friction with the duty palace's public face, even though palace 8 itself is undamaged.

- `palaces.2.palace_stem_rules.stems_in_harm`
- `palaces.3.palace_stem_rules.stems_in_harm`
- `palaces.4.palace_stem_rules.stems_in_harm`
- `palaces.6.palace_stem_rules.stems_in_harm`
- `palaces.7.palace_stem_rules.stems_in_harm`
- `palaces.8.palace_stem_rules.stems_in_harm`

## Birth-stage rules

### [=] birth_stage_rules_mostly_latent

*Palaces: 1, 2, 3, 4, 7, 8, 9 | COMPUTED*

Seven palaces declare `stems_in_birth_stage` (1:Xin, 2:Ren, 3:Gui, 4:Geng, 7:Ding+Ji, 8:Bing+Wu, 9:Yi). Checking occupancy: no palace is occupied by a stem in its own birth stage. The birth-stage layer therefore adds no active reinforcement anywhere.

- `palaces.1.palace_stem_rules.stems_in_birth_stage`
- `palaces.2.palace_stem_rules.stems_in_birth_stage`
- `palaces.3.palace_stem_rules.stems_in_birth_stage`
- `palaces.4.palace_stem_rules.stems_in_birth_stage`
- `palaces.7.palace_stem_rules.stems_in_birth_stage`
- `palaces.8.palace_stem_rules.stems_in_birth_stage`

### [+] day_stem_birth_stage_at_palace_8

*Palaces: 8 | COMPUTED*

Palace 8 lists Bing among its birth-stage stems. Bing is the day stem - the actor. So the one clean, unafflicted, void-free palace on this board is also the palace where the actor's element is in its birth stage. Set against palace 6, which is Bing's *tomb*, the two surviving routes are revealed as exact opposites for the actor: palace 8 is where Bing is born, palace 6 is where Bing is buried. This is the sharpest single discriminator the chart offers between the two candidates, and it was entirely missing from the earlier analysis.

- `palaces.8.palace_stem_rules.stems_in_birth_stage`
- `palaces.6.palace_stem_rules.stems_in_tomb`
- `timing.four_pillars.day`

### [=] lead_proxy_birth_stage_at_palace_1

*Palaces: 1 | COMPUTED*

Palace 1 lists Xin - the lead-stem proxy for the invisible Jia-Wu decade - in its birth stage. Xin is active at palace 9. Palace 1 is Xin's origin point and is also where Bai Hu (White Tiger) has just arrived. The public face of the matter is born in the North, in a palace whose star is Obsolete and which now holds the Tiger.

- `palaces.1.palace_stem_rules.stems_in_birth_stage`
- `chart_config.lead_stem`
- `palaces.1.active_chart.god`

## Star energy sub-states

### [=] seasonal_column_is_uniform

*Palaces: 1, 2, 3, 4, 6, 7, 8, 9 | COMPUTED*

Every single palace reports `star.seasonal = Strengthening`. A column with no variance carries no discriminating information, so any ranking that leaned on seasonal star strength would be ranking on noise. All real star information in this chart lives in `palace_relation`.

- `palaces.1.active_chart.energy_state.star.seasonal`
- `palaces.2.active_chart.energy_state.star.seasonal`
- `palaces.3.active_chart.energy_state.star.seasonal`
- `palaces.4.active_chart.energy_state.star.seasonal`
- `palaces.6.active_chart.energy_state.star.seasonal`
- `palaces.7.active_chart.energy_state.star.seasonal`

### [=] stars_outperforming_their_season

*Palaces: 2, 8 | COMPUTED*

At palaces 2, 8 the star is stronger by palace relation than by season - these stars are being carried by their location. Palaces 2 and 8 both reach Prosperous. Palace 2's Tian Rui is the illness star, so a Prosperous reading there means the illness is well-fed, not that the palace is healthy. Palace 8's Tian Ren (Ambassador) reaching Prosperous is a genuine positive and reinforces the palace 8 route.

- `palaces.2.active_chart.energy_state.star.palace_relation`
- `palaces.8.active_chart.energy_state.star.palace_relation`

### [-] stars_undercut_by_their_palace

*Palaces: 1, 3, 4, 9 | COMPUTED*

At palaces 1, 3, 4, 9 the star is weaker by palace relation than by season. Palace 1's Tian Peng falls all the way to Obsolete - the single worst star reading on the board. Palace 9's Tian Ying (Hero), the duty star itself, drops to Resting: the star that is supposed to carry the matter is the fifth-weakest on the board by location.

- `palaces.1.active_chart.energy_state.star.palace_relation`
- `palaces.3.active_chart.energy_state.star.palace_relation`
- `palaces.4.active_chart.energy_state.star.palace_relation`
- `palaces.9.active_chart.energy_state.star.palace_relation`

## Element prosperity

### [+] metal_prosperous_owns_the_working_half

*Palaces: 6, 7 | COMPUTED*

Metal is Prosperous. That single fact governs palaces 6 and 7, the stems Geng and Xin, the doors Kai (Open) and Jing (Fear), and the stars Tian Xin and Tian Zhu. Both Prosperous doors on this board are Metal doors. The chart's entire working capacity is Metal-shaped: cutting, deciding, finishing, publishing, closing. Nothing soft is in season.

- `element_prosperities.metal`
- `palaces.6.active_chart.door`
- `palaces.7.active_chart.door`

### [+] water_strengthening_is_the_rising_current

*Palaces: 1, 8 | COMPUTED*

Water is Strengthening - the only element on the rise. It appears as the stem Ren at palace 8, the stem Gui at palace 7, the Xiu (Rest) door at palace 1 and the star Tian Peng. Palace 8 carrying a Strengthening-element stem is a further independent mark in favour of the palace 8 route: it is the only candidate route whose stem element is gaining rather than peaking.

- `element_prosperities.water`
- `palaces.8.active_chart.stems.heaven`

### [-] wood_dead_erases_the_hour_stem

*Palaces: 3, 4 | COMPUTED*

Wood is Dead. This kills palaces 3 and 4 outright (both Dead in door and palace), kills the stem Yi at palace 4, and - most importantly - kills Jia, which is the hour stem and does not appear on the plate at all. The matter in motion is made of the one element the season has already finished with.

- `element_prosperities.wood`
- `timing.four_pillars.hour`
- `palaces.3.active_chart.energy_state.palace`

### [-] fire_imprisoned_traps_the_actor_and_the_showpiece

*Palaces: 5, 9 | COMPUTED*

Fire is Imprisoned. Fire is the day stem Bing (the actor, stranded in the Centre), the stem Ding at palace 6, the Jing (Scenery) door and the duty star Tian Ying - and palace 9 itself. So the actor, the duty star, the duty door and the duty palace are all made of an Imprisoned element. That is four independent confirmations of the same weakness, and it explains why the showpiece cannot hold regardless of how it is played.

- `element_prosperities.fire`
- `timing.four_pillars.day`
- `chart_config.duty_star`
- `chart_config.duty_door`
- `palaces.9.element`

### [=] earth_resting_is_the_neutral_ground

*Palaces: 2, 5, 8 | COMPUTED*

Earth is Resting - neither helped nor harmed. Earth is palaces 2, 5 and 8, the stems Wu and Ji, and the Sheng (Life) and Si (Death) doors. Palace 8's Life door being Resting rather than Prosperous is the honest cost of that route: it works, but it is not energised, so it will need deliberate push. This is precisely the 0.040 gap between palace 8 and palace 6.

- `element_prosperities.earth`
- `palaces.8.active_chart.energy_state.door`

## Earthly branch system

### [=] twelve_branches_fully_mapped

*Palaces: 1, 2, 3, 4, 5, 6, 7, 8, 9 | COMPUTED*

All twelve earthly branches are distributed across the eight directional palaces (the Centre holds none). Of the twelve, four are occupied by pillars (Wu (Horse), Xu (Dog), You (Rooster)) and eight are unoccupied. The four void branches are Wu (Horse), Wei (Goat), Chen (Dragon), Si (Snake), which map to palaces 2, 4 and 9 - matching the chart's own void flags exactly.

- `palaces.1.base_position.earthly_branches`
- `palaces.2.base_position.earthly_branches`
- `palaces.3.base_position.earthly_branches`
- `palaces.4.base_position.earthly_branches`
- `palaces.5.base_position.earthly_branches`
- `palaces.6.base_position.earthly_branches`

### [-] palace_9_single_branch_fully_loaded

*Palaces: 9 | COMPUTED*

Palace 9 holds exactly one branch, Wu (Horse) - and both the year pillar and the hour pillar carry Wu. A single-branch palace receiving a doubled pillar branch has no room to distribute the load, unlike palaces 2, 4, 6 and 8 which hold two branches each. The duty palace is the narrowest palace on the board and is carrying the heaviest branch concentration, while being void. Structurally it cannot absorb what is being put on it.

- `palaces.9.base_position.earthly_branches`
- `timing.four_pillars.year`
- `timing.four_pillars.hour`

### [=] day_branch_xu_sits_with_the_open_door

*Palaces: 6 | COMPUTED*

The day branch is Xu (Dog), which belongs to palace 6 - the Open-door, Ding, Tian Xin palace. The actor's own branch already sits at the strongest palace on the board, even though the actor's stem is stranded in the Centre. Stem and branch of the day pillar are split between the weakest position (Centre, no seat) and the strongest (palace 6). That split is the clearest statement of the chart's central tension, and it is also why palace 6 keeps scoring highly despite being Bing's tomb.

- `timing.four_pillars.day`
- `palaces.6.base_position.earthly_branches`

### [+] month_branch_you_anchors_the_metal_season

*Palaces: 7 | COMPUTED*

The month branch is You (Rooster), which belongs to palace 7 - pure Metal, Prosperous door, Prosperous palace. The month pillar is the seasonal authority, and it lands on the palace that most purely expresses the prosperous element. This is why the Metal reading throughout this chart is trustworthy: the season's own branch is sitting in its own house.

- `timing.four_pillars.month`
- `palaces.7.base_position.earthly_branches`

## Overrides produced by this layer

### OVR-001 - AR-BEST-01

P7 read fields the earlier run never opened. The birth-stage field resolves a tie the earlier run wrongly declared unresolvable. Early verdict is preserved above, not deleted.

- Was: `{"old_margin_claim": "Declared unresolvable from the chart alone; claimed the separator was assignment information.", "scores": {"BEST-JING-FEAR-W-P7": 0.515, "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE": 0.6887, "BEST-OPEN-DOOR-NW-P6-WITH-DING": 0.6487, "BEST-PUSH-THE-SHOWPIECE-AT-P9": 0.2725, "BEST-RIDE-THE-HORSE-AT-P2": 0.3037}, "status": "RESOLVED (narrow)", "winner": "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE"}`
- Now: `{"scores": {"BEST-JING-FEAR-W-P7": 0.515, "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE": 0.72, "BEST-OPEN-DOOR-NW-P6-WITH-DING": 0.64, "BEST-PUSH-THE-SHOWPIECE-AT-P9": 0.2725, "BEST-RIDE-THE-HORSE-AT-P2": 0.3037}, "status": "RESOLVED_BY_AMENDMENT", "winner": "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE"}`

### OVR-002 - ANOMALY:HOUR_STEM_NOT_ON_PLATE

The school declaration explains the absence as native to the method. Severity corrected; the anomaly is retained, not deleted.

- Was: `{"severity": "HIGH"}`
- Now: `{"severity": "LOW", "status": "DOWNGRADED_BY_P7"}`

## See also

- [[Chart-Analysis-Report]]
- [[Chart-Board-Synthesis]]
- [[MOC]]

## Sources

- `vault/raw/state/full_coverage.json`
- `vault/raw/state/overrides.json`

