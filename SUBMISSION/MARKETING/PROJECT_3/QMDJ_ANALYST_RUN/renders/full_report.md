# QMDJ Chart Analysis Package — QMDJ-P3-001

**Charter:** PROMPT/qmdj_chart_analyst_charter.md (v7.0) · **Compiler:** qmdj-analyst/1.0.0 · **Runtime:** TOOLS_PRESENT  
**Status:** partial — all 25 coverage batches completed; the package is PARTIAL because the gap register is non-empty by construction: several cold annexes declared by the charter were not supplied, four facets are deferred, and the case context is degraded.  
**Sources:** `QMDJ/MARKETING/project_3.json` · `ASSIGNMENTS/MARKETING/project_3.yaml`

## Validity boundary

Everything in this package is traditional interpretive analysis of one QMDJ chart. It is not a factual prediction, not evidence about any real market, brand, person or outcome, and not a substitute for professional judgment (financial, legal, medical or otherwise). Chart-derived readings are tradition-conditional: they describe symbolic structure, not events.

---

## 02 · Case context

**Context status: CONTEXT_FREE_PROSE_ACCEPTED.** the supplied file is an assignment brief whose single top-level key is 'assignment'; it carries none of the charter's case-context schema keys. Per the charter's degradation rule it is stamped CONTEXT_DEGRADED, its rows are tagged DECOMPOSED, and every derived row may direct relevance but may never enter the CONK/UNK sets at full authority.

| facet | status | what the source asks |
|---|---|---|
| Q1 | PRIMARY | what content must achieve for the brand |
| Q2 | PRIMARY | how the brand should communicate online (core message, tone, principles) |
| Q3 | PRIMARY | 3-5 content pillars, each with a purpose |
| Q4 | PRIMARY | 2-3 primary platforms, justified by audience behaviour |
| Q5 | PRIMARY | one idea adapted across the selected platforms |
| Q6 | PRIMARY | 5-6 content concepts incl. two visual executions |
| Q7 | PRIMARY | one hero campaign idea (insight -> big idea -> message -> execution) |
| Q8 | DEFERRED | community and engagement mechanisms |
| Q9 | DEFERRED | creator/influencer strategy and two recommended creators |
| Q10 | DEFERRED | two-week content calendar with cadence rationale |
| Q11 | DEFERRED | 5-7 metrics, each tied to an objective, plus a one-month read |

Facet cap: 11 facets found, 7 analysed (Q1-Q7) via criterion **DECISION_RELEVANCE rank v2**, 4 deferred (Q8-Q11).

**Known facts (CONK).**

- `CONK01` The deliverable is a marketing assignment titled '2: Content & Social Media Strategy'.
- `CONK02` The submission format is a presentation (PPT/PDF/slides) that continues the same document as the previous assignment.
- `CONK03` The strategy must build on a strategic foundation created in Assignment 1.
- `CONK04` A brand and a target persona exist for the student and are defined outside the supplied material.

**Unknowns (UNK) — not resolved anywhere in this package.**

- `UNK01` The brand's identity, category and positioning must not be assumed or resolved.
- `UNK02` The persona's attributes must not be assumed or resolved.
- `UNK03` The brand's current channel mix and performance data must not be assumed or resolved.
- `UNK04` Whether a product launch is planned must not be assumed or resolved.

_Instruction-injection scan:_ 0 marker(s) found — null result.

---

## 03 · Chart overview

Fingerprint: `project_3.json|14937|2|chart_info,palaces`

SHA-256 of the chart file: `c6e0b8940051e8380e37d883f0624315bcdbf4f65596304ca0cf6f76e50fd0b6`

### Board card (whole chart, one view)

| palace | trigram | direction | deity | gate | star | heaven stem | earth stem | hosted stem | opposites |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Kan 坎 | N | 值符 | 杜门 | 天辅 | 辛 | 丁 | — | 4 |
| 2 | Kun 坤 | SW | 六合 | 休门 | 天蓬 | 丁 | 癸 | — | — |
| 3 | Zhen 震 | E | 九地 | 死门 | 天芮 | 癸 | 壬 | 庚 | — |
| 4 | Xun 巽 | SE | 玄武 | 惊门 | 天柱 | 戊 | 辛 | — | 1 |
| 5 | (centre) | centre | — | — | 天禽 | — | 庚 | — | — |
| 6 | Qian 乾 | NW | 腾蛇 | 伤门 | 天冲 | 壬 | 己 | — | 9 |
| 7 | Dui 兑 | W | 太阴 | 生门 | 天任 | 乙 | 戊 | — | — |
| 8 | Gen 艮 | NE | 九天 | 景门 | 天英 | 丙 | 乙 | — | — |
| 9 | Li 离 | S | 白虎 | 开门 | 天心 | 己 | 丙 | — | 6 |

Root register:

- **governing_spirit_zhi_fu**: {"value": "TianFu 天辅", "palace": 1, "evidence": ["E005", "E022"]}
- **duty_gate_zhi_shi**: {"value": "Du men 杜门", "palace": 1, "evidence": ["E006", "E012"]}
- **day_pillar**: {"value": "Xin Hai 辛亥", "evidence": ["E007"]}
- **hour_pillar**: {"value": "Ding You 丁酉", "evidence": ["E008"]}
- **month_pillar**: {"value": "Ding You 丁酉", "evidence": ["E009"]}
- **year_pillar**: {"value": "Bing Wu 丙午", "evidence": ["E010"]}
- **solar_term**: {"value": "秋分, 上 Yuan (Autumn Equinox, upper yuan)", "evidence": ["E002"]}
- **system**: {"value": "Yi Dun - Lun Cang Jia; Hourly Rotating Qimen, Yin Dun 7 Ju", "evidence": ["E001", "E003", "E004"]}
- **centre**: {"palace": 5, "content": ["TianQin 天禽", "earth-plate Geng 庚"], "evidence": ["E060", "E061", "E062"]}
- **trace_ring**: {"ring": [1, 2, 3, 6, 9, 8, 7, 4], "spur": [[3, 5]], "edges": 9}

### Structure evidence

`106` evidence atoms (E) and `9` relations (R), all with provenance paths and sha256 content addresses. Full tables in `package/05_structure_evidence.json`.

| R | palaces | stem | relation type | trace |
|---|---|---|---|---|
| R001 | 1-2 | 丁 | R.IDENTICAL_STEM | value_trace(丁): ES@1(earth_stem) == HS@2(heaven_stem); matched by FIELD VALUE, not array position |
| R002 | 1-4 | 辛 | R.IDENTICAL_STEM_ON_AXIS | value_trace(辛): HS@1(heaven_stem) == ES@4(earth_stem); matched by FIELD VALUE, not array position |
| R003 | 2-3 | 癸 | R.IDENTICAL_STEM | value_trace(癸): ES@2(earth_stem) == HS@3(heaven_stem); matched by FIELD VALUE, not array position |
| R004 | 3-5 | 庚 | R.IDENTICAL_STEM_LODGING | value_trace(庚): HX@3(hosted_stem) == ES@5(earth_stem); matched by FIELD VALUE, not array position |
| R005 | 3-6 | 壬 | R.IDENTICAL_STEM | value_trace(壬): ES@3(earth_stem) == HS@6(heaven_stem); matched by FIELD VALUE, not array position |
| R006 | 4-7 | 戊 | R.IDENTICAL_STEM | value_trace(戊): HS@4(heaven_stem) == ES@7(earth_stem); matched by FIELD VALUE, not array position |
| R007 | 6-9 | 己 | R.IDENTICAL_STEM_ON_AXIS | value_trace(己): ES@6(earth_stem) == HS@9(heaven_stem); matched by FIELD VALUE, not array position |
| R008 | 7-8 | 乙 | R.IDENTICAL_STEM | value_trace(乙): HS@7(heaven_stem) == ES@8(earth_stem); matched by FIELD VALUE, not array position |
| R009 | 8-9 | 丙 | R.IDENTICAL_STEM | value_trace(丙): HS@8(heaven_stem) == ES@9(earth_stem); matched by FIELD VALUE, not array position |

Trace graph: **single closed circulation over the 8-palace outer ring plus 1 centre spur(s)**; ring `1→2→3→6→9→8→7→4`; centre spur `3-5`.

---

## 06 · Coverage and closure

| palace | closure equation | balances |
|---|---|---|
| 0 | 10 live (6 addressed + 4 deferred) + 0 absent = 10 | True |
| 1 | 12 live (9 addressed + 2 corroborated + 1 deferred) + 2 absent = 14 | True |
| 2 | 12 live (8 addressed + 4 deferred) + 2 absent = 14 | True |
| 3 | 14 live (8 addressed + 1 corroborated + 5 deferred) + 2 absent = 16 | True |
| 4 | 11 live (7 addressed + 1 corroborated + 3 deferred) + 2 absent = 13 | True |
| 5 | 3 live (3 addressed) + 5 absent = 8 | True |
| 6 | 11 live (7 addressed + 2 corroborated + 2 deferred) + 2 absent = 13 | True |
| 7 | 11 live (9 addressed + 2 deferred) + 2 absent = 13 | True |
| 8 | 11 live (7 addressed + 1 corroborated + 3 deferred) + 2 absent = 13 | True |
| 9 | 11 live (7 addressed + 2 corroborated + 2 deferred) + 2 absent = 13 | True |
| global | 0 global absent slots | True |

Totals: 106 live atoms + 21 absent slots = **127 closed slots**.

---

## 08 · Claims

| claim | label | batch | confidence | tier | rank status |
|---|---|---|---|---|---|
| C001 | Single point of gravity | B3 | 0.91 | explicit_chart | confirmed |
| C002 | Restraint as the operating mode | B3 | 0.9 | explicit_chart | bounded |
| C003 | Display is the reach engine | B3 | 0.96 | explicit_chart | bounded |
| C004 | Value accrues through quiet channels | B3 | 0.86 | explicit_chart | bounded |
| C005 | Announcement through the alliance channel fails | B3 | 0.97 | explicit_chart | confirmed |
| C006 | Three friction registers | B3 | 0.86 | explicit_chart | confirmed |
| C007 | The centre is held under contest | B3 | 0.95 | explicit_chart | bounded |
| C008 | One closed circulation | B3 | 0.84 | computed_structure | confirmed |
| C009 | Two axes are already bridged | B3 | 0.81 | computed_structure | bounded |
| C010 | Temporal weight sits twice on palace 7 | B4 | 0.81 | computed_structure | bounded |
| C011 | The opening is real but pressed | B3 | 0.96 | explicit_chart | confirmed |
| C012 | Subject stem and subject seat diverge | B4 | 0.97 | explicit_chart | bounded |
| C013 | Auspicious combination on a depleted substrate | B4 | 0.86 | explicit_chart | bounded |

### C001 — Single point of gravity

- **Archetype:** `ARC-CENTRE-OF-GRAVITY` (explicit chart_field zhi_fu and zhi_shi both name palace 1; day stem present on that palace's heaven plate)
- **Chart support:** E005, E006, E012, E013, E019, E020, E021, E022, E017
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.91 (explicit_chart) · **rank status:** confirmed
- **Rank reason:** no rebutting candidate in the legal candidate set; competing arcs (dispersed, two-centres) have no chart support
- **Guard:** A concentrated reading may not be used to justify concentrating spend on a single surface without a separate reach case.
- **Limitations:** Concentration is a structural observation; it does not by itself rank which surface should receive the concentration.

### C002 — Restraint as the operating mode

- **Archetype:** `ARC-RESTRAINT-MODE` (duty gate office (closing/blocking) plus governing star office (teaching/assistance))
- **Chart support:** E005, E006, E012, E022 · R002
- **Counter-evidence left visible:** E086
- **Confidence:** 0.9 (explicit_chart) · **rank status:** bounded
- **Rank reason:** the reach palace keeps a competing operating mode alive; A003 and A004 both challenge a restraint-only reading
- **Guard:** If the deliverable requires a large-volume launch, this claim is the first to be re-tested against the reach claim C003.
- **Limitations:** The contrary palace 8 display cluster (E085, E086, E095) is left visible and carries the reach function; the two readings coexist by palace, not by contradiction.

### C003 — Display is the reach engine

- **Archetype:** `ARC-VISIBILITY-ENGINE` (display gate + widest-reach deity + radiance star co-located with a cooperation-favourable stem pair)
- **Chart support:** E085, E086, E091, E093, E095 · R008
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.96 (explicit_chart) · **rank status:** bounded
- **Rank reason:** A001 (teaching-led reach) and A002 (alliance reach) are live alternatives; the display reading is not the only route
- **Guard:** Reach built here is display-reach; it must not be reported as trust or conversion.
- **Limitations:** The marker 丙加乙 names cooperation; it does not name a platform or a format.

### C004 — Value accrues through quiet channels

- **Archetype:** `ARC-PRIVATE-GAIN` (generation gate + hidden-support deity + reliability star in a gate-feeds-house palace under the yin-favouring stem pair)
- **Chart support:** E074, E075, E080, E082, E084 · R006
- **Counter-evidence left visible:** E077, E078
- **Confidence:** 0.86 (explicit_chart) · **rank status:** bounded
- **Rank reason:** the same palace's stems sit at the cut-off and death stages, so the channel is favourable in kind but depleted in force
- **Guard:** Private-channel value is slow; it may not be used to promise a fast conversion ramp.
- **Limitations:** The same palace's stems sit at the cut-off and death stages (E077, E078): the channel is favourable in kind but currently depleted in force.

### C005 — Announcement through the alliance channel fails

- **Archetype:** `ARC-BROKEN-BROADCAST` (alliance deity co-located with the message-sinks marker and a locked three-qi in a house that presses its gate)
- **Chart support:** E023, E024, E029, E030, E031, E032 · R003
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.97 (explicit_chart) · **rank status:** confirmed
- **Rank reason:** no candidate can be supported against it; the alliance deity itself remains visible as counterweight
- **Guard:** Do not use this claim to argue against partnership itself; it constrains the message, not the alliance.
- **Limitations:** The marker is polarity-tagged inauspicious in the register; the alliance deity in the same palace is tagged favourable. Both stay visible.

### C006 — Three friction registers

- **Archetype:** `ARC-FRICTION-ZONE` (enumeration of palace-gate relations and stem pairs across palaces 3, 4 and 6)
- **Chart support:** E035, E036, E042, E043, E045, E049, E050, E055, E057, E063, E064, E069, E071 · R005
- **Counter-evidence left visible:** E038, E041
- **Confidence:** 0.86 (explicit_chart) · **rank status:** confirmed
- **Rank reason:** the friction palaces also carry sprouting and maturing stages, which limits rather than rebuts the reading
- **Guard:** Friction markers forbid forcing, not acting; nothing in this claim forbids trying a method once and measuring it.
- **Limitations:** The counter-evidence is explicit: the same palaces carry sprouting and maturing stages (E038, E041), so the registers are impeded rather than dead.

### C007 — The centre is held under contest

- **Archetype:** `ARC-CONTESTED-CENTRE` (centre palace marker register (doubled conflict stem) and its single lodging edge)
- **Chart support:** E060, E061, E062, E047 · R004
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.95 (explicit_chart) · **rank status:** bounded
- **Rank reason:** A004 is a live alternative: the centre's own marker is favourable to the guest and unfavourable to the host, so a challenger posture is not excluded by the chart
- **Guard:** The centre's own marker is favourable to the guest and unfavourable to the host; do not read this as a licence for aggressive comparative positioning.
- **Limitations:** The centre has no gate and no deity in this chart, so the disposition cannot be stated through a gate office.

### C008 — One closed circulation

- **Archetype:** `ARC-CONNECTED-SYSTEM` (graph closure of the identical-stem value traces)
- **Chart support:** E013, E021, E033, E040, E046, E047, E051, E058, E060, E065, E072, E076, E083, E087, E094, E098 · R001, R002, R003, R004, R005, R006, R007, R008, R009
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.84 (computed_structure) · **rank status:** confirmed
- **Rank reason:** graph closure verified by CAP-09 over all nine traces
- **Guard:** A connected structure argues for one system, not for one channel; the claim says nothing about which route is fastest.
- **Limitations:** The ring is a relation over stem values only; it is not a claim about timing or about the strength of each edge.

### C009 — Two axes are already bridged

- **Archetype:** `ARC-BRIDGED-AXES` (both Luoshu opposition pairs coincide with an identical-stem trace)
- **Chart support:** E021, E051, E065, E081 · R002, R007
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.81 (computed_structure) · **rank status:** bounded
- **Rank reason:** only two oppositions exist under the chart's own opposition rule; the claim cannot be extended to the other pairings
- **Guard:** A bridged axis is a channel, not a recommendation; it says the two ends can speak, not that they agree.
- **Limitations:** Only two of the six Luoshu axis relations exist in this chart's opposition rule; the other pairings are not oppositions at all.

### C010 — Temporal weight sits twice on palace 7

- **Archetype:** `ARC-DOUBLED-TEMPORAL-SIGNATURE` (month and hour pillars share the branch the chart binds to palace 7)
- **Chart support:** E007, E008, E009, E010, E078, E100
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.81 (computed_structure) · **rank status:** bounded
- **Rank reason:** structural only: the chart supplies no civil date or clock time
- **Guard:** Branch-to-palace binding is derived from the chart's own stage annotations; it may not be extended into weekdays, hours or campaign dates.
- **Limitations:** The chart supplies no civil date or clock time, so the temporal reading is structural only.

### C011 — The opening is real but pressed

- **Archetype:** `ARC-PRESSED-OPENING` (opening gate in a house that presses it, with maximum-stage stems and a gradual-reveal marker)
- **Chart support:** E097, E099, E100, E102, E104, E106
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.96 (explicit_chart) · **rank status:** confirmed
- **Rank reason:** the pressed-opening reading is supported by two independent marker classes (house-gate relation and stem pair)
- **Guard:** Do not read maximum stage as permission to launch without preparation; the house in this palace presses its gate.
- **Limitations:** The gradual-reveal marker is a general reading; the chart does not state a schedule.

### C012 — Subject stem and subject seat diverge

- **Archetype:** `ARC-DIVERGENT-SUBJECT` (day stem placement on the heaven plate of one palace, day branch bound to another)
- **Chart support:** E007, E021, E051, E063, E064, E066 · R002
- **Counter-evidence left visible:** none recorded
- **Confidence:** 0.97 (explicit_chart) · **rank status:** bounded
- **Rank reason:** depends on assumption A-001 (subject binding); retained with an explicit uncertainty marker
- **Guard:** Divergence is a recorded state, not an invitation to pick the flattering half; both halves must appear in any recommendation that cites this claim.
- **Limitations:** The stem-and-branch reading follows the standard subject binding declared in the dependency assumptions; that binding is assumption-indexed.

### C013 — Auspicious combination on a depleted substrate

- **Archetype:** `ARC-SEED-UNDER-FROST` (twelve-stage readings for the two stems that form the keystone combination, plus the same stage in the adjacent bridged palace)
- **Chart support:** E014, E015, E017, E027, E053 · R002
- **Counter-evidence left visible:** E016, E018
- **Confidence:** 0.86 (explicit_chart) · **rank status:** bounded
- **Rank reason:** the doubled hidden-plate marker corroborates the combination but does not strengthen the substrate reading
- **Guard:** A depleted substrate argues for sequenced effort, not for delaying the start indefinitely.
- **Limitations:** The doubled marker (E016, E018) restates the combination on the hidden plate; it is corroboration of the same reading, not a second finding.

---

## 09 · Case alignment

### Q1 — what content must achieve for the brand (PRIMARY)

| claim | tag |
|---|---|
| C001 | DIRECT |
| C003 | DIRECT |
| C002 | INDIRECT |
| C007 | INDIRECT |
| C005 | NO_CHART_SUPPORT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 2, "INDIRECT": 2, "NO_CHART_SUPPORT": 1} · covered: True

### Q2 — how the brand should communicate online (core message, tone, principles) (PRIMARY)

| claim | tag |
|---|---|
| C005 | DIRECT |
| C002 | DIRECT |
| C013 | INDIRECT |
| C006 | INDIRECT |
| C004 | NO_CHART_SUPPORT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 2, "INDIRECT": 2, "NO_CHART_SUPPORT": 1} · covered: True

### Q3 — 3-5 content pillars, each with a purpose (PRIMARY)

| claim | tag |
|---|---|
| C001 | DIRECT |
| C003 | DIRECT |
| C004 | DIRECT |
| C005 | INDIRECT |
| C002 | INDIRECT |
| C007 | NO_CHART_SUPPORT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 3, "INDIRECT": 2, "NO_CHART_SUPPORT": 1} · covered: True

### Q4 — 2-3 primary platforms, justified by audience behaviour (PRIMARY)

| claim | tag |
|---|---|
| C003 | DIRECT |
| C002 | DIRECT |
| C004 | DIRECT |
| C005 | INDIRECT |
| C006 | INDIRECT |
| C009 | NO_CHART_SUPPORT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 3, "INDIRECT": 2, "NO_CHART_SUPPORT": 1} · covered: True

### Q5 — one idea adapted across the selected platforms (PRIMARY)

| claim | tag |
|---|---|
| C001 | DIRECT |
| C008 | DIRECT |
| C010 | INDIRECT |
| C011 | INDIRECT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 2, "INDIRECT": 2, "NO_CHART_SUPPORT": 0} · covered: True

### Q6 — 5-6 content concepts incl. two visual executions (PRIMARY)

| claim | tag |
|---|---|
| C004 | DIRECT |
| C003 | DIRECT |
| C002 | DIRECT |
| C006 | NO_CHART_SUPPORT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 3, "INDIRECT": 0, "NO_CHART_SUPPORT": 1} · covered: True

### Q7 — one hero campaign idea (insight -> big idea -> message -> execution) (PRIMARY)

| claim | tag |
|---|---|
| C001 | DIRECT |
| C011 | DIRECT |
| C013 | DIRECT |
| C012 | INDIRECT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 3, "INDIRECT": 1, "NO_CHART_SUPPORT": 0} · covered: True

### Q8 — community and engagement mechanisms (DEFERRED)

| claim | tag |
|---|---|
| C005 | DIRECT |
| C004 | DIRECT |
| C006 | INDIRECT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 2, "INDIRECT": 1, "NO_CHART_SUPPORT": 0} · covered: True

### Q9 — creator/influencer strategy and two recommended creators (DEFERRED)

| claim | tag |
|---|---|
| C005 | DIRECT |
| C004 | DIRECT |
| C002 | INDIRECT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 2, "INDIRECT": 1, "NO_CHART_SUPPORT": 0} · covered: True

### Q10 — two-week content calendar with cadence rationale (DEFERRED)

| claim | tag |
|---|---|
| C010 | DIRECT |
| C002 | DIRECT |
| C013 | INDIRECT |
| C006 | NO_CHART_SUPPORT |

Tally: {"CONTRADICTS_KNOWN": 0, "DIRECT": 2, "INDIRECT": 1, "NO_CHART_SUPPORT": 1} · covered: True

### Q11 — 5-7 metrics, each tied to an objective, plus a one-month read (DEFERRED)

| claim | tag |
|---|---|
| C003 | DIRECT |
| C004 | DIRECT |
| C011 | DIRECT |
| C001 | INDIRECT |
| C009 | INDIRECT |
| C012 | CONTRADICTS_KNOWN |

Tally: {"CONTRADICTS_KNOWN": 1, "DIRECT": 3, "INDIRECT": 2, "NO_CHART_SUPPORT": 0} · covered: True

---

## 10 · Red team

- `RT|A001|criticizes=C001|kind=support|status=live` — A concentrated, teaching-led build is the scenario the keystone palace activates; it supports the single-gravity claim rather than competing with it.
- `RT|A001|criticizes=C002|kind=support|status=live` — Teaching from behind a closed door is exactly the restraint reading; the alternative (volume) has no palace of its own.
- `RT|A001|criticizes=C003|kind=alternative|status=live` — Teaching-led reach competes with display-led reach: the governing star suggests the audience arrives to learn, not to watch.
- `RT|A001|criticizes=C007|kind=rebut|status=live` — A build that never enters the centre is not affected by the centre's contest disposition; the claim bounds the strategy only if the strategy fights for the middle.
- `RT|A002|criticizes=C003|kind=rebut|status=live` — If reach arrives through partners rather than through display, the display palace is a supporting engine, not the engine.
- `RT|A002|criticizes=C005|kind=support|status=live` — The alliance scenario confirms that joining is favoured while announcement is not.
- `RT|A002|criticizes=C007|kind=support|status=live` — An alliance-led build that pushes announcements into the alliance channel walks straight into the broken-broadcast marker.
- `RT|A003|criticizes=C002|kind=rebut|status=live` — A volume-led build directly contradicts the restraint reading; the chart answers it with the duty gate sitting in the keystone palace.
- `RT|A003|criticizes=C006|kind=support|status=live` — High cadence runs the calendar straight through the three friction registers; the scenario is the practical test of the friction claim.
- `RT|A004|criticizes=C002|kind=alternative|status=live` — A challenger posture uses the centre's own disposition, which is favourable to the guest and to attack; it is an alternative operating mode, not a violation of the chart.
- `RT|A004|criticizes=C006|kind=rebut|status=superseded` — Forced entry into the friction registers is rebutted by the fold: three palaces carry breakage markers and the fold leaves no candidate standing.
- `RT|A004|criticizes=C007|kind=alternative|status=live` — The centre's marker favours the attacking guest; what it excludes is reading the centre as neutral, not entering it as a challenger.

---

## 12 · Uncertainty and limits

- protocol class **HC**: the semantic_protocol_raw class set was not supplied; no class could be ingested, so no class was inferred (charter Tier2 step 1). The deliverable's strategy content is therefore a structural interpretation, not a class-driven archetype render.
- protocol class **AX**: not supplied
- protocol class **ZQ**: not supplied
- protocol class **CS**: not supplied
- protocol class **JG**: not supplied
- protocol class **QT**: not supplied

Deferred topics: Q8 community (deferred by facet cap), Q9 creators (deferred by facet cap; also blocked by UNK01), Q10 calendar (deferred by facet cap), Q11 measurement (deferred by facet cap), paid distribution, competitor analysis, pricing mechanics

---

## 13 · Decision support

**Bounded recommendation.** Run one cycle on two objectives only (awareness through display; education through the governing star), route value through quiet channels, keep the alliance channel two-way rather than broadcast, and treat the three friction registers as places to measure rather than to push.

| objective | metric class | chart basis |
|---|---|---|
| awareness through display | reach | E086, E085 |
| education through the governing star | saves and returns to a piece | E005, E022, E075 |
| quiet support | private interactions (saves, direct messages) | E074 |
| entry | link clicks from discovery surfaces | E097 |
| alliance | co-created pieces and partner mentions | E023 |
| participation | comments that continue a conversation (not volume) | E024 |
| health of the friction registers | argument threads and complaints per cycle, tracked as a stop signal | E050, E064 |

Validation path:

- Publish one cycle of content built on the two selected objectives and read the response against the metric classes in 13_decision_support.metric_classes.
- Test the privateness claim (C004) by comparing private saves/direct responses with public engagement on the same piece.
- Test the announcement claim (C005) by keeping one partnership campaign message low-key and comparing its reach with one broadcast-style push.
- Test the friction claim (C006) by refusing to enter any contest or pile-on for one cycle and recording what changes.

---

## 14 · Gap report

| id | path | why unaddressed | owner | resolution |
|---|---|---|---|---|
| G001 | schema_adapter.yaml (variants) | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G002 | frozen_tables.yaml | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G003 | wiki_articles corpus | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G004 | semantic_protocol_raw.json | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G005 | pattern_catalog annex A-patterns | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G006 | archetype_scoring_rubric annex A-archetypes | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G007 | coverage_control annex A-coverage | declared by the charter as a cold input; not present in the supplied material | B0 | supply the file; the stand-in used is named in 11_dependency_assumptions |
| G008 | schema_adapter.yaml | no variant registry supplied; least-contradicted bind used | B1 | ANOMALY:SCHEMA_AMBIGUITY was NOT raised because the bind is high-confidence (exact 2-key match, uniform palace key style); a supplied adapter can confirm it |
| G009 | frozen_tables.yaml | no frozen tables supplied; annex A-tables fallback used for identity lookups | B2 | diff annex A-tables against the supplied frozen_tables.yaml |
| G010 | palaces 1-9 / role void | no void (xun-kong) field exists in the chart; recorded ABSENT | B1 | none: absence is factual, not a defect |
| G011 | palaces 1-9 / role horse | no horse (yi-ma) field exists in the chart; recorded ABSENT | B1 | none: absence is factual, not a defect |
| G012 | palace 5 / heaven stem, gate, deity | the centre carries only a star, a palace label and an earth-plate stem | B2 | none: absence is factual; the centre's relation set is the lodging graph only |
| G013 | Q8-Q11 (community, creators, calendar, measurement) | 4 of 11 facets exceed the CAP-17 seven-facet cap and were deferred by the declared ranking criterion A-010 | P5 | the delivered strategy document addresses them as carried-forward content; no new chart claim was created for them |
| G014 | case_context / schema shape | the supplied case context matches no charter schema key; it is ingested through the free_prose path (AMEND-01) rather than as schema keys | P5 | closed by AMEND-01; the v1 CONTEXT_DEGRADED stamp is retained in 02_case_context_digest for audit |
| G015 | case_context / DECOMPOSED authority | every row decomposed from the brief carries DECOMPOSED authority, so CONK01-CONK04 can raise POTENTIAL_CONFLICT but cannot veto a verdict | P5 | no live verdict conflicts with any CONK row, so no claim moves; if the operator wants veto-grade constraints, re-supply them as schema keys |
| G016 | case_context / brand and persona | the brief names the brand and the persona as existing in Assignment 1, which was not supplied; both remain declared unknowns (UNK01, UNK02) and are not resolved by the chart | P5 | supply Assignment 1; it will populate the CONK set and the deliverable's slots - it cannot change any chart claim (cc1/cc2) |
| G017 | creator identity (UNK01/UNK04 guard) | the chart cannot name a person or a brand; naming a real creator would be an invented fact | P5 | supply the Assignment-1 brand and persona; the creator rubric then returns 2 named fits by search |
| G018 | temporal binding | the chart supplies pillars but no civil date or clock time, so no weekday, hour or campaign-date timing can be derived | B4 | supply the cast timestamp if calendar timing is required |
| G019 | grammar gate | no gaps: every emitted claim, CMAP and RT line passed the grammar | B5 | none |
| G020 | anomaly/QUESTION_OVERLOAD | 11 facets detected against the charter's 7-facet cap; the 7 most decision-relevant (Q1-Q7) are analysed under criterion DECISION_RELEVANCE and Q8-Q11 are listed as deferred. Raised on amendment AMEND-01: the v1 run reported the cap inside the digest but did not log the anomaly code CAP-17 step 4 requires. | P5 | see 15_tool_event_log |

---

## 15 · Tool event log

| # | call |
|---|---|
| 1 | `CAP|CAP-01|in=project_3.json|out=fingerprint|cost=14` |
| 2 | `CAP|CAP-02|in=chart|out=normalization|cost=21` |
| 3 | `CAP|CAP-03|in=chart|out=schema_bind|cost=59` |
| 4 | `CAP|CAP-04|in=chart,roles|out=role_map|cost=25` |
| 5 | `CAP|CAP-05|in=chart_info.ganzhi|out=ganzhi_parsed|cost=59` |
| 6 | `CAP|CAP-06|in=ganzhi,palace_elements|out=stem_norm|cost=10` |
| 7 | `CAP|CAP-07|in=palace_elements|out=composite_atoms|cost=85` |
| 8 | `CAP|CAP-08|in=palaces|out=luoshu_geometry|cost=32` |
| 9 | `CAP|CAP-10|in=palaces,/home/user/ecole-assignments/SUBMISSION/MARKETING/PROJECT_3/QMDJ_ANALYST_RUN/CONFIG/marker_reference.json|out=pattern_hits|cost=26` |
| 10 | `CAP|CAP-11|in=chart,roles|out=evidence_registry|cost=28` |
| 11 | `CAP|CAP-17|in=project_3.yaml|out=case_context_digest|cost=31` |
| 12 | `CAP|CAP-09|in=evidence_registry|out=value_trace|cost=82` |
| 13 | `CAP|CAP-01|in=project_3.json|out=fingerprint|cost=14` |
| 14 | `CAP|CAP-15|in=claim_set.json|out=score_card|cost=266` |
| 15 | `CAP|CAP-18|in=claim_set|out=case_alignment|cost=341` |
| 16 | `CAP|CAP-13|in=renders/claim_lines.txt,renders/cmap_lines.txt,renders/rt_lines.txt|out=grammar_check|cost=12` |
| 17 | `CAP|CAP-12|in=evidence_registry,claim_set.json|out=board_digest|cost=36` |
| 18 | `CAP|CAP-14|in=evidence_registry,/home/user/ecole-assignments/SUBMISSION/MARKETING/PROJECT_3/QMDJ_ANALYST_RUN/authored/ledger_sidecar.json|out=ledger_reconcile|cost=31` |
| 19 | `CAP|CAP-16|in=all_state|out=self_audit|cost=31` |
| 20 | `CAP|CAP-19|in=claim_set.json|out=conflict_check|cost=158` |
| 21 | `CAP|CAP-01|in=project_3.json|out=fingerprint|cost=14` |

Anomalies: [{"call_index": 11, "code": "QUESTION_OVERLOAD", "detail": "11 facets detected against the charter's 7-facet cap; the 7 most decision-relevant (Q1-Q7) are analysed under criterion DECISION_RELEVANCE and Q8-Q11 are listed as deferred. Raised on amendment AMEND-01: the v1 run reported the cap inside the digest but did not log the anomaly code CAP-17 step 4 requires.", "path": "02_case_context_digest", "phase": "P5", "raised_by": "AMEND-01"}]

_Anchor items of the P6 registry:_

- `P3-COMBO` state=live hits=18 rank=2 confidence=0.96
- `P3-GATE` state=live hits=18 rank=3 confidence=0.96
- `P3-STRUCT` state=live hits=53 rank=1 confidence=0.96

