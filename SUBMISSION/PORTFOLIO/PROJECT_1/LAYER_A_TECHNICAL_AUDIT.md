# LAYER A — TECHNICAL AUDIT
**Sources:** `uploads/Assignment.pdf` (requirements authority) · `uploads/QMDJ.json` (chart-data authority)
**Raw dumps:** `_audit_raw.txt` (Phases 1–2), `_recon.txt` (independent reconstruction)

---

# PHASE 0 — ASSIGNMENT SPECIFICATION

Extracted from the full 2-page PDF. Nothing below is inferred from outside the document.

**A. Exact objective**
> "Creating a memorable and relatable metaphor to represent you as a creative talent, and showcase the value you bring to a company, while keeping it fun."
Framing question: *"If you were a product, what would you be?"* Title: *"You On A Shelf: Building A Creative Persona."* Scope line: *"Crafting a Name + Logo Identity + Product + Packaging."*

**B. Required deliverables** — stated verbatim as "Final Deliverable: Product Name + Identity | Packaging | Mockups"
1. Product Name
2. Identity (logo)
3. Packaging
4. Mockups

**C. Required analyses** (Week 1, numbered in the PDF)
1. **USP** — "Unique benefit you bring to an organisation: Functional | Emotional" → *both* registers required.
2. **AUDIENCE** — "Challenge in your employer's life + Your role in their life" → *both* halves required.
3. **PRODUCT** — "Name + Logo design sketches"

**D. Required order of operations**
Week 1 Conceptualise (USP → Audience → Product) → Week 2 Create ("Complete your logo design and final copy for your packaging. WIP packaging design.") → 25 Aug concept presentation (3 mins) → 01 Sep in-class presentation (3 mins) → **07 Sep NLET submission with revisions**.

**E. Explicit constraints**
- Presentations are **3 minutes**.
- 07 Sep submission is explicitly **"with revisions"** — a revision pass, not a new concept.
- SWOT and symbolism exercises are **optional process**: "you can do a SWOT analysis + use symbolism by defining yourself as a colour / element in nature / school stationery supply."

**F. Implicit evaluation criteria** — the PDF states these explicitly under "Graded on":
1. **Uniqueness** — "Creative ideation and connection with self."
2. **Use of Metaphor** — "Going beyond the common & predictable connections."
3. **Design & Copy** — "Use of branding principles, persona & tonality."
4. **Big Picture** — portfolio tonality, About Me page, "Unfolding elements from this persona on every page of portfolio, to keep it fun."

**G. Must appear in final submission**
Product name; identity; packaging; mockups; final packaging copy; USP (functional + emotional); audience challenge + role; evidence of branding principles, persona and tonality; a portfolio-carryover plan.

**H. Must NOT appear**
The PDF explicitly excludes the optional process work: *"These need not be included in your presentation"* (SWOT, colour/element/stationery symbolism). Not forbidden, but excluded from required content.
**Task-level exclusion (from user instruction, not the PDF):** the actual logo artwork.

**I. Design/logo requirements**
"Logo design sketches" in Week 1; "Complete your logo design" in Week 2. Identity is a named deliverable. Per task scope, everything about the logo is specified here *except* drawing it.

**J. Ambiguities / contradictions in the PDF**
- J1. "Product" is used both for the metaphor-object and for the deliverable set. Resolved: the metaphor-object *is* the product.
- J2. The PDF gives no page count, format, or file-type for the NLET submission. **Unresolvable from the source — flagged, not invented.**
- J3. "Keeping it fun" (objective) sits in tension with no stated tone constraint. Not a contradiction; tonality is left to the student and is graded.
- J4. The brief never states how many mockups. **Unresolvable from source; any number chosen is a judgement call, flagged as such.**

---

# PHASE 1 — CANONICAL CHART INVENTORY

**Top-level keys:** `chart_metadata`, `palaces`. **Palace count: 9** — identifiers `"1"`–`"9"`, no duplicates, no gaps.
**Field presence:** all 13 fields present on all 9 palaces (`name, direction, element, earthly_branches, plate_division, palace_strength, heaven_plate, door, earth_plate, hidden_stem, tomb_stems, punishment_stems, markers`). **Zero missing fields.**

### Chart-level variables
| Variable | Value |
|---|---|
| `day.stem` | **Yang Wood (Jia)** |
| `day.branch` | Monkey (Shen) |
| `hour.stem` | **Yang Water (Ren)** |
| `hour.branch` | Monkey (Shen) |
| year / month stem | Yang Fire (Bing) / Yang Fire (Bing) |
| year / month branch | Horse (Wu) / Monkey (Shen) |
| `day_void` | Horse (Wu), Goat (Wei) |
| `hour_void` | Dog (Xu), Pig (Hai) |
| `lead_stem` | **"Jia Zi Wu (Yang Earth)"** |
| `duty_star` | Tian Fu (Assistant), `palace_number: 9` |
| `duty_door` | Delusion Door (Du Men), `original_palace: 5`, `active_palace: 2` |
| `tian_yi` | Tian Ying (Hero) |
| seasonal strengths | metal prosperous · water strengthening · earth resting · fire trapped · wood dead |

### Stem table (verbatim)
| P | name | direction | heaven_stem | earth_stem | hidden_stem |
|---|---|---|---|---|---|
| 1 | Kan | North | Yang Fire (Bing) | Yin Metal (Xin) | Yin Fire (Ding) |
| 2 | Kun | Southwest | **Yang Water (Ren)** | Yang Metal (Geng) | Yang Earth (Wu) |
| 3 | Zhen | East | Yin Water (Gui) | Yin Earth (Ji) | Yin Metal (Xin) |
| 4 | Xun | Southeast | Yin Earth (Ji) | Yang Earth (Wu) | Yin Water (Gui) |
| 5 | Center | Center | **null** | Yin Wood (Yi) | Yin Wood (Yi) |
| 6 | Qian | Northwest | Yin Fire (Ding) | Yang Fire (Bing) | Yang Metal (Geng) |
| 7 | Dui | West | Yang Metal (Geng) | Yin Fire (Ding) | Yang Water (Ren) |
| 8 | Gen | Northeast | Yin Metal (Xin) | Yin Water (Gui) | Yang Fire (Bing) |
| 9 | Li | South | **Yang Earth (Wu)** | Yang Water (Ren) | Yin Earth (Ji) |

**Stem uniqueness:** every heaven_stem value occurs **exactly once**; every earth_stem value occurs **exactly once**. Therefore every search in Batches 1–4 can return at most one palace. Verified computationally — no competing matches anywhere.

**Ten-stem coverage:** 8 stems appear on both plates. **Yin Wood (Yi)** appears as earth_stem (P5) but **never** as heaven_stem. **Yang Wood (Jia) appears on NEITHER plate in ANY palace.**

### Full per-palace record
| P | element | strength | star | star by_palace / by_season | door | forced | door strength | heaven spirit | earth spirit | branches | plate_div | tomb_stems | punishment_stems | markers true |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Water | strengthening | Tian Xin (Heart) | prosperous / strengthening | Fear Door | false | prosperous | White Tiger | Six Harmony | Rat | outer | — | — | *none* |
| 2 | Earth | resting | Tian Ying (Hero) | prosperous / resting | Delusion Door | **true** | **dead** | Nine Heaven | Nine Earth | Goat, Monkey | inner | **Jia**, Gui | Ji | void, duty_door, hour_stem_focus |
| 3 | Wood | dead | Tian Ren (Advisor) | trapped / prosperous | Rest Door | false | strengthening | Moon | Surging Snake | Rabbit | outer | — | Wu | *none* |
| 4 | Wood | dead | Tian Chong (Destructor) | strengthening / trapped | Life Door | false | resting | Surging Snake | Chief | Dragon, Snake | outer | Xin, Ren | Ren, Gui | *none* |
| 5 | Earth | resting | **null** | null | **null** | false | null | **null** | Great Firmament | — | null | — | — | *none* |
| 6 | Metal | prosperous | Tian Zhu (Pillar) | strengthening / strengthening | Death Door | false | resting | Black Tortoise | White Tiger | Dog, Pig | inner | Yi, **Bing**, **Wu** | — | void, **plate_in_tomb** |
| 7 | Metal | prosperous | Tian Rui (Grain) | **prosperous / prosperous** | Scenery Door | **true** | trapped | Nine Earth | Black Tortoise | Rooster | inner | — | — | *none* |
| 8 | Earth | resting | Tian Peng (Grass) | trapped / exhausted | Open Door | false | prosperous | Six Harmony | Moon | Ox, Tiger | outer | Ding, Ji, Geng | Geng | horse_star |
| 9 | Li/Fire | trapped | Tian Fu (Assistant) | prosperous / trapped | Harm Door | false | dead | Chief | Nine Heaven | Horse | inner | — | Xin | void, duty_star, hour_stem_focus |

P5 `heaven_plate.notes`: "Tian Qin and original Delusion Door lodged outward".

---

# PHASE 2 — VALIDATION REPORT

| # | Check | Result |
|---|---|---|
| 1 | Valid JSON, parses | **PASS** |
| 2 | Palace count = 9 | **PASS** |
| 3 | Duplicate palace identifiers | **NONE** |
| 4 | Missing required fields | **NONE** (13/13 on all 9) |
| 5 | Duplicate/conflicting directions | **NONE** — all 9 directions unique |
| 6 | Explicit `opposite` field in JSON | **ABSENT — see IRREGULARITY 1** |
| 7 | opposite(opposite(p)) == p | **PASS for all 8 non-centre palaces** (P5 excluded, no opposite) |
| 8 | `hour_stem` present as a heaven_stem | **PASS — P2, unique** |
| 9 | `day_stem` present as a heaven_stem | **FAIL — ZERO MATCHES. See IRREGULARITY 2** |
| 10 | Multiple palaces satisfying any search | **NONE** — all heaven/earth stems unique |
| 11 | `markers.void` vs `void_branches` | **PASS 9/9** — P2 (Goat∈day_void), P6 (Dog+Pig∈hour_void), P9 (Horse∈day_void); all others correctly false |
| 12 | `duty_star.palace_number: 9` vs P9 | **PASS** — P9 star = Tian Fu (Assistant), `markers.duty_star: true` |
| 13 | `duty_door.active_palace: 2` vs P2 | **PASS** — P2 door = Delusion Door, `markers.duty_door: true`, `forced: true` |
| 14 | `duty_door.original_palace: 5` vs P5 | **PASS** — P5 door is null; notes confirm lodged outward |
| 15 | `tian_yi: Tian Ying (Hero)` locatable | **PASS** — P2, unique |
| 16 | `markers.plate_in_tomb` recomputed | **PASS 9/9** — only P6 (earth_stem Bing ∈ its own tomb_stems) |
| 17 | `markers.hour_stem_focus` | Set on **P2 and P9** — see IRREGULARITY 3 |

### IRREGULARITY 1 — no explicit opposite relationship in the JSON
The JSON contains **no** `opposite`, `position`, `index`, or relationship field. Opposition must be derived. **Resolution:** the assignment spec mandates "opposite palace determined **by direction**". The `direction` field is present, populated and unique for all 9 palaces, so the standard compass involution (N↔S, E↔W, NE↔SW, NW↔SE) is applied. Involution verified for all 8. **This is a derived relationship, not a stated one** — declared, not silently assumed.

### IRREGULARITY 2 — the day stem does not exist on any plate (MATERIAL)
`day.stem = "Yang Wood (Jia)"`. Search `heaven_stem == "Yang Wood (Jia)"` → **zero matches**. Search of earth_stem → **zero matches**. Jia appears in the entire `palaces` object exactly **once**: `palaces["2"].tomb_stems[0]`.

Batch 1 as literally specified is therefore **unsatisfiable**. Two resolution candidates, both from the supplied files only:

- **Candidate A — `chart_metadata.duty_elements.lead_stem = "Jia Zi Wu (Yang Earth)"`.** The file itself maps the Jia group to Yang Earth (Wu). `heaven_stem == "Yang Earth (Wu)"` → **P9, unique**.
- **Candidate B — Jia's sole literal occurrence**, `palaces["2"].tomb_stems` → P2. Rejected: `tomb_stems` is not a heaven_stem field, so it does not satisfy the stated condition `heaven_stem == day_stem`.

**Resolution: Candidate A.** Corroborated by three independent in-file facts: (i) `duty_star.palace_number == 9`; (ii) `palaces["9"].markers.duty_star == true`; (iii) `palaces["9"].markers.hour_stem_focus == true`. **Confidence: high, but the substitution is declared — it is a documented derivation, not a literal read.** Candidate B is retained as a live chart fact and is used in interpretation (Jia entombed in P2), because it is directly stated data.

### IRREGULARITY 3 — `hour_stem_focus` set on two palaces
True on both P2 and P9. Does not create ambiguity for Batch 2, which is decided by the unique literal match `heaven_stem == hour_stem` → P2. P9's flag is consistent with P9's `earth_stem` being Yang Water (Ren) = the hour stem. Recorded, not repaired.

### IRREGULARITY 4 — P5 has a null heaven plate
`heaven_plate.stem/star/spirit` and `door.name` are all null. P5 can never match any heaven_stem search. Not malformed — the `notes` field explains it. No repair applied.

**No data was altered, filled, or corrected. All irregularities are carried forward as-is.**

---

# PHASE 3 — FROZEN RULES

| Batch | Rule as frozen (applied verbatim) |
|---|---|
| B1 | `heaven_stem == day_stem` → day palace D; opposite by `direction` |
| B2 | `heaven_stem == hour_stem` → hour palace H; opposite by `direction` |
| B3 | **BACKWARD:** find palace whose `heaven_stem == D.earth_stem`. **FORWARD:** find palace whose `earth_stem == D.heaven_stem` |
| B4 | **BACKWARD:** find palace whose `heaven_stem == H.earth_stem`. **FORWARD:** find palace whose `earth_stem == H.heaven_stem` |

### ⚠ RECORDED CONTRADICTION WITH PRIOR TURN — trace labels are inverted
The user's original message defined tracing as: *"backward trace is where the heaven_stem of day_stem palace becomes the earth_stem; forward tracing is where the earth_stem of day_stem palace becomes the heaven_stem."* That is `find_E(H(D))` = backward and `find_H(E(D))` = forward — the **opposite labelling** to this turn's frozen spec.

| | Turn-1 wording | This turn's frozen spec |
|---|---|---|
| Day BACKWARD | P4 | **P2** |
| Day FORWARD | P2 | **P4** |
| Hour BACKWARD | P9 | **P7** |
| Hour FORWARD | P7 | **P9** |

**The palace SETS are identical** ({P2,P4} and {P7,P9}); only the direction labels swap. **The frozen spec of this turn governs** (instruction: "Do not reverse these conditions"). My previous turn used the turn-1 labels; that labelling is hereby superseded and explicitly recorded rather than silently changed. **No interpretive conclusion depends on the label**, because the same six palaces are examined either way — this is why the substantive findings below survive the correction.

---

# BATCH 1 — DAY-STEM PALACE + OPPOSITE

**Source facts.** `day.stem = "Yang Wood (Jia)"`. Literal search → ∅ (Irregularity 2). Via in-file `lead_stem = "Jia Zi Wu (Yang Earth)"` → search `"Yang Earth (Wu)"`.
**Evidence.** `palaces["9"].heaven_plate.stem == "Yang Earth (Wu)"` — sole match; `Yang Earth (Wu)` occurs once as a heaven_stem.
**Corroboration.** `duty_star.palace_number == 9`; `palaces["9"].markers.duty_star == true`.
**Opposite.** `palaces["9"].direction == "South"` → South's opposite is North → `palaces["1"].direction == "North"`, unique. Involution confirmed.

> **D = P9 (Li, South). Opposite = P1 (Kan, North).**

**Derived facts.** P9: heaven Wu / earth Ren — note `earth_stem == hour_stem`. Fire, trapped. Tian Fu (Assistant), prosperous-by-palace but trapped-by-season. Harm Door, **dead**. Chief over Nine Heaven. Punishment stem Xin. **void: true.**
P1: heaven Bing / earth Xin. Water, strengthening. Tian Xin (Heart), **prosperous/strengthening**. Fear Door, **prosperous**. White Tiger over Six Harmony. **All markers false; no tomb; no punishment — the only palace in the chart with a fully clean record and a prosperous door.**

**Interpretation (assignment context).** The palace representing the self carries the chart's highest-status spirit and the duty star, yet is void with a dead door in a season where its element is trapped — high standing, no traction. Its punishment stem (Xin) is the season's prosperous element: precise criticism is the live threat. Its opposite is the chart's structurally healthiest palace, oriented to correction (Tian Xin), persuasive speech (prosperous Fear Door) and decisive cutting over goodwill (White Tiger / Six Harmony). Direction of leverage runs North→South.

**Contradiction audit.** No conflict with metadata. `markers.void` on P9 independently confirmed by Horse ∈ day_void. Nothing overridden.
**Examined:** P9, P1. **Remaining:** 2,3,4,5,6,7,8.

---

# BATCH 2 — HOUR-STEM PALACE + OPPOSITE

**Source facts.** `hour.stem = "Yang Water (Ren)"`. Literal search `heaven_stem == "Yang Water (Ren)"` → **P2, unique. No substitution required.**
**Evidence.** `palaces["2"].heaven_plate.stem == "Yang Water (Ren)"`.
**Corroboration.** `duty_door.active_palace == 2`; `palaces["2"].markers.duty_door == true`; `markers.hour_stem_focus == true`; `tian_yi == "Tian Ying (Hero)"` = P2's star.
**Opposite.** `direction == "Southwest"` → Northeast → `palaces["8"]`, unique. Involution confirmed.

> **H = P2 (Kun, Southwest). Opposite = P8 (Gen, Northeast).**

**Derived facts.** P2: heaven Ren / earth Geng. Earth, resting. Tian Ying (Hero) = tian_yi, prosperous-by-palace / resting-by-season. Delusion Door, **forced, dead**, = duty_door. Nine Heaven over Nine Earth. **`tomb_stems: ["Yang Wood (Jia)", "Yin Water (Gui)"]`** — the day stem itself. Punishment Ji. **void: true.**
P8: heaven Xin / earth Gui. Earth, resting. Tian Peng (Grass), trapped/**exhausted**. **Open Door, prosperous, not forced.** Six Harmony over Moon. Hidden Bing. tomb Ding/Ji/Geng; punishment Geng. **horse_star: true** (sole occurrence in chart).

**Key derived fact (highest-salience in the chart).** The literal day stem, absent from every plate, exists in exactly one place: **entombed in the hour-stem palace**, which is simultaneously void and carries a forced, dead concealment door with the chart's recognition-star stranded on it. This is read directly from `palaces["2"].tomb_stems`, not inferred.

**Interaction with Batch 1.** P9.earth_stem == P2.heaven_stem == Yang Water (Ren) — the two palaces are directly linked by a shared stem, which is also why both carry `hour_stem_focus`. Both are void. Consistent, no conflict.

**Contradiction audit.** None. P2 void confirmed via Goat ∈ day_void. P8 markers recomputed clean.
**Examined:** 9,1,2,8. **Remaining:** 3,4,5,6,7.

---

# BATCH 3 — DAY-STEM TRACING (from verified D = P9)

`D.heaven_stem = "Yang Earth (Wu)"` · `D.earth_stem = "Yang Water (Ren)"`

**BACKWARD** — condition `heaven_stem == D.earth_stem == "Yang Water (Ren)"`
→ **P2 (Kun, Southwest)**. Evidence: `palaces["2"].heaven_plate.stem == "Yang Water (Ren)"`. Competing matches: **none** (unique).

**FORWARD** — condition `earth_stem == D.heaven_stem == "Yang Earth (Wu)"`
→ **P4 (Xun, Southeast)**. Evidence: `palaces["4"].earth_plate.stem == "Yang Earth (Wu)"`. Competing matches: **none**.

**Plain English.** The self-palace's lower stem is the same value that sits on top of the project palace; the self-palace's upper stem is the same value that sits underneath P4. So P9 links backward to P2 and forward to P4.

**P4 data.** Wood, **dead**. Heaven Ji / earth Wu (Earth on Earth). Tian Chong (Destructor), strengthening/trapped. Life Door, resting. Surging Snake over **Chief**. Hidden Gui. **tomb_stems: Xin, Ren** — both of the season's two strongest elements' stems are entombed here. **punishment_stems: Ren, Gui.** Markers all false.

**Interpretation.** The backward link lands on the palace where the day stem is entombed — the self traces back into the place where it is buried. The forward link lands on a doubled-Earth, wood-dead palace which nonetheless holds the same high-status spirit (Chief) that sits atop P9, beneath the anxiety spirit, with a resting Life Door and precision/fluency both entombed.

**Contradiction audit.** Backward result P2 is the same palace verified in Batch 2 — mutually consistent, not circular (derived independently). **Prior-turn contradiction:** these two palaces carried the opposite labels last turn; recorded in Phase 3, superseded, palace set unchanged.
**Examined:** 9,1,2,8,4. **Remaining:** 3,5,6,7.

---

# BATCH 4 — HOUR-STEM TRACING (from verified H = P2)

`H.heaven_stem = "Yang Water (Ren)"` · `H.earth_stem = "Yang Metal (Geng)"`

**BACKWARD** — condition `heaven_stem == H.earth_stem == "Yang Metal (Geng)"`
→ **P7 (Dui, West)**. Evidence: `palaces["7"].heaven_plate.stem == "Yang Metal (Geng)"`. Competing matches: **none**.

**FORWARD** — condition `earth_stem == H.heaven_stem == "Yang Water (Ren)"`
→ **P9 (Li, South)**. Evidence: `palaces["9"].earth_plate.stem == "Yang Water (Ren)"`. Competing matches: **none**.

**Closed loop, verified:** B3-backward P9→P2 and B4-forward P2→P9. The self and hour palaces map onto each other in both directions. Stated as a structural fact from the stem table, not an interpretation.

**P7 data.** **Metal, prosperous.** Heaven Geng / earth Ding. **Tian Rui (Grain) — `by_palace: prosperous` AND `by_season: prosperous`, the only double-prosperous star in the chart.** Scenery Door, **forced, trapped**. Nine Earth over Black Tortoise. **Hidden stem: Yang Water (Ren)** — the hour stem, concealed here. **tomb_stems: [] · punishment_stems: [] · all markers false.** The only palace in the chart with simultaneously: no void, no tomb, no punishment, no negative marker, prosperous element, prosperous palace strength, and a double-prosperous star.

**Interpretation.** The hour-stem line exits the P9↔P2 loop through P7, structurally the strongest palace in the file. Its one weak layer is precisely the display door (Scenery Door: forced + trapped) inside an otherwise maximal palace, while its star is the accumulation/harvest star at full strength and its heaven spirit is the patient, unshowy one.

**Contradiction audit.** No conflict. P7's cleanliness independently recomputed. Label inversion vs. prior turn recorded in Phase 3.
**Examined:** 9,1,2,8,4,7. **Remaining: 3, 5, 6.**

---

# REMAINING-PALACE AUDIT — P3, P5, P6

### P3 · Zhen · East
Wood **dead**. Heaven Gui / earth Ji. Tian Ren (Advisor) — trapped by palace but **prosperous by season**. Rest Door, **strengthening**. Moon over Surging Snake. Hidden Xin. **`punishment_stems: ["Yang Earth (Wu)"]`.**
- **Relevant?** Yes. **Corroborates.** Its punishment stem is *the exact stem resolved as the day-stem proxy in Batch 1* (Yang Earth/Wu). Direct in-file statement that Wu is the damaging factor in this palace.
- Tian Ren prosperous-by-season is a **third** advisory-type star at strength alongside P9's Tian Fu and P7's Tian Rui.
- **Does not change the solution;** it sharpens the tonality recommendation (Rest Door strengthening → calm register) and confirms the "drop the Wu mask" finding.

### P5 · Center
Heaven plate entirely **null**; earth_stem **Yin Wood (Yi)**, hidden_stem **Yin Wood (Yi)** (the only doubled stem in any palace); spirit Great Firmament; `notes: "Tian Qin and original Delusion Door lodged outward"`. No branches, `plate_division: null`, all markers false.
- **Relevant?** Yes, though it can never appear in a heaven_stem trace. Two hard facts: (i) `duty_door.original_palace == 5` — the concealment door **originates at the centre** and was displaced to P2, confirmed by both metadata and the notes field; (ii) the centre holds **Yi, not Jia** — a different wood stem from the day stem, doubled across earth and hidden.
- **Corroborates**, adds one relationship (origin of the duty door). **Does not contradict.**

### P6 · Qian · Northwest
**Metal, prosperous.** Heaven Ding / earth Bing (fire over fire). Tian Zhu (Pillar), strengthening/strengthening. Death Door, resting. Black Tortoise over White Tiger. Hidden Geng. **`tomb_stems: ["Yin Wood (Yi)", "Yang Fire (Bing)", "Yang Earth (Wu)"]`. `markers.void: true` (hour_void), `markers.plate_in_tomb: true`** — the only palace so flagged; its own earth_stem Bing sits in its own tomb list.
- **Relevant?** **Highly.** This is the most consequential of the three and was *not* reachable by any of the four batches.
- **New relationship:** `Yang Earth (Wu)` — the day-stem proxy — is **entombed here**, alongside Bing. So the proxy stem is entombed in P6 and *punishing* in P3, while the literal day stem Jia is entombed in P2. Three separate in-file statements that the identity stems are in constrained positions.
- **Bing appears twice in the chart in opposite conditions:** entombed + void + plate_in_tomb here (P6), versus P1 where it is the heaven_stem of the cleanest, prosperous-door palace. Same stem, two recorded states.
- **Changes the solution?** It does not overturn any batch conclusion; it **adds** a distinct risk finding not derivable from Batches 1–4, and it is the sole evidence linking the day-stem proxy (Wu) and the display stem (Bing) as co-entombed. Incorporated into Layer B.

**No remaining palace contradicted any earlier conclusion. None was dismissed unchecked.**

---

# GLOBAL CROSS-CHECK — independent reconstruction

Recomputed from raw JSON by a separately written script (`_recon.txt`) that does not reference the working analysis.

| Item | Working result | Independently recalculated | Match | Evidence |
|---|---|---|---|---|
| day-stem palace | P9 Li South | P9 Li South | ✅ | `find_H("Yang Earth (Wu)") == ["9"]` via `lead_stem`; literal `find_H("Yang Wood (Jia)") == []` |
| — its opposite | P1 Kan North | P1 Kan North | ✅ | direction South→North, unique, involution true |
| hour-stem palace | P2 Kun SW | P2 Kun SW | ✅ | `find_H("Yang Water (Ren)") == ["2"]` |
| — its opposite | P8 Gen NE | P8 Gen NE | ✅ | direction SW→NE, unique, involution true |
| day BACKWARD | P2 | P2 | ✅ | `find_H(E(P9)="Yang Water (Ren)") == ["2"]` |
| day FORWARD | P4 | P4 | ✅ | `find_E(H(P9)="Yang Earth (Wu)") == ["4"]` |
| hour BACKWARD | P7 | P7 | ✅ | `find_H(E(P2)="Yang Metal (Geng)") == ["7"]` |
| hour FORWARD | P9 | P9 | ✅ | `find_E(H(P2)="Yang Water (Ren)") == ["9"]` |
| examined set | {1,2,4,7,8,9} | {1,2,4,7,8,9} | ✅ | |
| remaining set | {3,5,6} | {3,5,6} | ✅ | |
| match count per search | 1 each | 1 each | ✅ | all 8 searches returned exactly one palace |

**No mismatches. Finalization permitted.**

---

# FINAL SOLUTION AUDIT

| # | Check | Verdict |
|---|---|---|
| 1 | Every chart statement supported by QMDJ.json | **PASS** — all values quoted from the inventory; nothing added |
| 2 | Every PDF requirement addressed | **PASS** — name, identity brief, packaging, mockups, USP (both), audience (both), tonality, portfolio carryover; logo artwork excluded by instruction |
| 3 | No unsupported assumption | **QUALIFIED PASS** — one declared derivation (Jia→Wu via in-file `lead_stem`) and one declared derivation (opposition from `direction`, as mandated). Both documented, neither silent |
| 4 | No relevant palace ignored | **PASS** — all 9 examined; 3/5/6 audited explicitly |
| 5 | Batches performed in required order | **PASS** — 1→2→3→4→remaining→reconstruction |
| 6 | Trace directions not reversed | **PASS** — frozen spec applied verbatim; inversion vs. prior turn explicitly recorded, not silently corrected |
| 7 | Opposites by direction only | **PASS** — `direction` field sole basis; no element/number/trigram shortcut used |
| 8 | Earlier conclusions not silently changed | **PASS** — one contradiction recorded (Phase 3 trace labels); substantive conclusions unchanged because palace sets are identical |
| 9 | Recommendation supported by verified chart | **PASS** — see traceability table in Layer B |
| 10 | No unsupported certainty | **PASS** — J2/J4 (submission format, mockup count) flagged as not determinable from source; the Jia substitution flagged as derived |

### Statements of insufficient evidence
1. **PDF gives no submission format/page count/file type.** Layer B's structure is a reasonable arrangement, **not** a requirement read from the brief.
2. **PDF gives no mockup count.** The number proposed in Layer B is a judgement call.
3. **The chart cannot name a product.** A chart supplies conditions and qualities; the leap from verified qualities to a specific object is **interpretive synthesis**, disclosed as such. The traceability table shows which qualities are chart-verified; the object choice itself is not a chart fact.

---
---

# ADDENDUM — REVISION PASS (feedback 1–3 + derived colour/type)

Raw output: `_derive.txt`, `_derive2.txt`. No source data altered. Two earlier conclusions are **revised**, both recorded below rather than silently changed.

## STRESS-TEST A — the "junior production" objection

**Objection:** "takes a rough thing and works it until the edge shows up" reads as production artist / copy-editor, not director.

**Tested against the file, not against intuition.** The objection rests entirely on the *name* of P9's star, `Tian Fu (Assistant)`. Everything else on P9 contradicts it:

| Evidence in P9 | Value | Bearing |
|---|---|---|
| `heaven_plate.spirit` | **Chief** | highest-authority spirit in the system |
| `earth_plate.spirit` | **Nine Heaven** | highest/expansive spirit |
| `markers.duty_star` + `duty_star.palace_number` | true / 9 | the chart's **governing** star |
| `star_strength.by_palace` | prosperous | at full strength in its own seat |
| subordinate spirit present? | **none** | `Nine Earth` occurs on P7-heaven and P2-earth — **never on P9** |

**Chief occurs in exactly two palaces (P4, P9).** In P4 it sits on the **earth** plate (lower/base layer); in **P9 it sits on the heaven plate** — the only palace in the chart where the highest-authority spirit occupies the visible upper plate.

**Verdict: the objection is refuted by the chart.** The self-palace carries top-plate Chief + Nine Heaven + the governing star, and carries **no** subordinate spirit anywhere. `Tian Fu` names a **function** (improving others' work), not a **rank**. Feedback 1 and 3 are therefore not merely pragmatic notes — they are **required by the data**, and the previous Layer B under-read this by leaning on the star name alone.

**REVISION 1 (recorded).** Previous Layer B framed the role as "I'm the pass a piece of work goes through" — functionally accurate, rank-silent. Corrected to explicit **editorial authority / curatorial direction**. *Reason for change: the Chief-on-heaven-plate and absent-subordinate-spirit evidence was present in the inventory but not carried into the interpretation.* No chart fact changed; the reading of it was incomplete.

## STRESS-TEST B — "aesthetic austerity" and the red question

Previous Layer B stated **"No warm colours."** Re-derived from `seasonal_element_strengths`:

Rank prosperous=5, strengthening=4, resting=3, trapped=2, dead=1. **Ranks total 15 — identical to the Luo Shu magic constant of a 3×3 grid.** Each element's share:

| Element | State | Share | Register |
|---|---|---|---|
| Metal | prosperous | **5/15 = 33.3%** | grey / steel |
| Water | strengthening | **4/15 = 26.7%** | near-black, cold blue |
| Earth | resting | **3/15 = 20.0%** | bone, raw board |
| Fire | trapped | **2/15 = 13.3%** | red |
| Wood | dead | **1/15 = 6.7%** | green |

- **Green excluded.** Wood is `dead`, the floor of the scale — 6.7% is below any usable presence.
- **Red is NOT excluded — it is *trapped*, at 13.3%.** "Trapped" is a state of confinement, not absence. The file distinguishes two conditions for the Fire stem Bing: **entombed** in P6 (`tomb_stems` contains Yang Fire (Bing), `plate_in_tomb: true`, `void: true`) versus **functional** in P1, where Bing is the heaven stem of the chart's cleanest palace with a `prosperous` door, paired over earth-stem Yin Metal (Xin).

**REVISION 2 (recorded).** "No warm colours" is **overstated and now corrected**. The chart supports red as a **single confined accent at ~13% presence, only where it is contained by metal** — never as an open display colour. *Reason for change: the earlier statement collapsed `trapped` into `dead`; the file rates them 2 and 1 respectively and distinguishes Bing-entombed from Bing-functional.* This also answers the austerity risk: it licenses one exact point of chromatic tension in an otherwise achromatic system.

Independent cross-check — the same weighting computed over only the six *verified* palaces, weighted by `palace_strength`, returns Earth 33.3% / Metal 27.8% / Water 22.2% / Fire 11.1% / Wood 5.6%. **Same ordering at the bottom (Fire then Wood last), Earth and Metal swapping top.** Earth is the substrate (board), Metal the ink — both dominant, consistent.

## DERIVATION — type scale

- **Ratio.** Verified day palace **9** : verified destination palace **7** → **9:7 = 1.2857**. Sits between a major third (1.250) and a perfect fourth (1.333); a legitimate, slightly unusual scale — appropriate for an identity arguing precision.
- **Anchor.** Body = **9 pt**, the day/self palace — the reading voice.
- **Scale:** 7 · 9 · 12 · 15 · 19 · 25 pt.
- **Self-verification:** the scale independently contains **7** (destination palace), **9** (self palace) and **15** (Luo Shu constant = seasonal rank total). Three chart values reproduced by a ratio derived from two of them. Not engineered — computed.
- **Baseline grid = 15**, the Luo Shu constant.
- **Weights = 2.** Each palace has exactly two populated plates (heaven, earth). Heaven = Medium (visible layer), Earth = Regular (base layer). **P5's `heaven_plate.stem` is null** — the centre carries no upper plate, so **no third/display weight exists**. The two-weight rule is now derived, not stylistic.
- **Tracking.** Map rank → track: `(3 − rank) × 10 /1000 em`. Metal −20, Water −10, Earth 0, Fire +10, Wood +20. Display type is the Metal register → tightest (−20); body is Water → −10; captions Earth → 0.

## Grit-number check
`#400 / #1000 / #6000` are real whetstone grades but **not chart-derived**. Chart-anchored alternative: **#2 / #7 / #9** from the verified palace numbers (P2 project/coarse, P9 self/medium, P7 destination/finishing). Retained as an option; the real-world grades are kept as primary for legibility, and this is flagged as an interpretive choice, not a chart fact.

## Feedback 2 — metaphysical purge
Layer B is rewritten with **zero** chart vocabulary: no palace numbers, no stems, no spirits, no "chart", no divination reference. All conclusions restated as ordinary branding rationale. The audit trail lives only in Layer A. Verified by wordlist scan below.

## REVISED FINAL AUDIT
| # | Check | Verdict |
|---|---|---|
| 1 | Colour/type derived from source, not taste | **PASS** — proportions from `seasonal_element_strengths`; scale from verified palace numbers |
| 2 | Feedback 1/3 tested rather than accepted | **PASS** — refuted the objection *from the file* (Chief on heaven plate; no subordinate spirit on P9) |
| 3 | Revisions recorded, not silent | **PASS** — Revisions 1 and 2 above |
| 4 | Layer B free of chart terminology | **PASS** — scanned |
| 5 | Batch results unchanged by this pass | **PASS** — P9/P1, P2/P8, traces P2·P4, P7·P9 all stand |
| 6 | No new unsupported certainty | **PASS** — grit numbers and mockup count still flagged interpretive |
