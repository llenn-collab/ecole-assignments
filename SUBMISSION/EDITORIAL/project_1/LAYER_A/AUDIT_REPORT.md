# AUDIT REPORT — EDITORIAL/project_1

**Skill:** `PROMPT/SKILLS/Audit/skill.md` (= `PROMPT/SKILLS/audit.md` on `origin/main`; identical body, longer frontmatter). Ironclad Post-Mortem & Integrity Auditor.
**Audited artefact:** `SUBMISSION/EDITORIAL/project_1/LAYER_B/NASA_BOOK_CONTENT_STRUCTURE.md`
**Scope declared by the operator:** concept + larger content buckets + finalised content structure. Not the full submission pack.
**Auditor posture:** hostile. No benefit of the doubt given. The auditor did not write, repair or improve the artefact.

---

## PASS 1 — verdict: **VETO**

Audited 2026-09-18T01:20Z. Gates 0 and 1 pass. **Gates 2, 3 and 4 fail.**
Veto codes issued: `HALLUCINATION` (Gate 2), `WEAK_FOUNDATION` (Gate 3), `BLIND_SPOT` (Gate 4).
Details in `LAYER_A/VETO_LOG.md`; per-claim scoring in `LAYER_A/CONFIDENCE_MATRIX.json` (38 claims, 24 core).

### Activation caveat, recorded rather than waived

The skill requires a worker at HALT with a complete submission package. The worker is at `PAUSED_CONCEPT_AND_INDEX` by explicit operator instruction, and `LAYER_A/LAYER_A_TECHNICAL_AUDIT.md`, the OPERATOR tree and `MANIFEST.md` do not exist yet. The audit was run anyway because the operator ordered it, on the one artefact that does exist. **The verdict below therefore covers that artefact only.** It is not a verdict on a submission pack, and it must not be read as one. A pack-level audit at HALT is still owed.

---

## Gate 0 — Input presence · **PASS**

| Required input | Repo path (AGENT.md §4 map) | Present | Readable |
|---|---|---|---|
| `vault/raw/Assignment.pdf` | `ASSIGNMENTS/EDITORIAL/project_1.md` (1,342 B, 29 lines) | yes | yes |
| `vault/raw/QMDJ.json` | `QMDJ/EDITORIAL/project_1.json` (11,131 B) | yes | yes |
| `vault/output/SUBMISSION/` | `SUBMISSION/EDITORIAL/project_1/LAYER_B/` (1 file, 57,561 B) | yes, non-empty | yes |
| `vault/raw/state/MANIFEST.json` | `WORK/EDITORIAL/project_1/state/MANIFEST.json` | yes | yes |

Additional raw input, hashed and treated as authoritative for the artefact's form: the content-structure worksheet, absent from branch base `9815d73` and recovered read-only from `a4dbd32:ASSIGNMENTS/EDITORIAL/NASA_BOOK_CONTENT_STRUCTURE.md`. The recovered copy is byte-identical to the object in `origin/main` (both sha256 `a9281eca…`). `ASSIGNMENTS/**` and `QMDJ/**` were not mutated.

### Gate 1 — Integrity check · **PASS**

| Raw input | sha256 | Manifest | Result |
|---|---|---|---|
| `ASSIGNMENTS/EDITORIAL/project_1.md` | `d9f6d817fe615df5…` | `d9f6d817fe615df5…` | MATCH |
| worksheet template | `a9281ecaeea50a57…` | `a9281ecaeea50a57…` | MATCH |
| `chart_analysis_package.json` | `e535d406852b1b58…` | `e535d406852b1b58…` | MATCH |
| `QMDJ/EDITORIAL/project_1.json` | `ee434d4bd41771d3…` | `ee434d4bd41771d3…` | MATCH |

Artefact under audit: sha256 `88f9146ca6bde040…`, matching its manifest snapshot. No tampering.

---

## Gate 2 — Traceability matrix · **FAIL → `VETO: HALLUCINATION`**

**What traces cleanly.** Every structural and constraint claim in the artefact has an explicit anchor in the brief with a line number, or in the worksheet by row index, or in the evidence package by resolution id:

| Element | Root | Anchor |
|---|---|---|
| 72 pages ≥ 60 minimum | PDF | `project_1.md` L5–L6 |
| Topic is NASA-related | PDF | L6 "at any cost" |
| Not one of the fourteen | PDF | L9–L23 |
| Concept = mentor idea #1 | PDF | L28 |
| Rejection of mentor idea #2 | PDF | L18, L22, L29 |
| 49 rows × 5 columns, headings byte-identical | worksheet | sha `a9281eca…` |
| 15 seeded interaction labels on their exact rows | worksheet | rows 1, 2×2, 6, 10, 11, 27, 28, 31, 32, 33, 38, 41, 43, 46, 48 |
| Interactions column left empty on 33 rows | operator instruction + worksheet heading "if any" | — |
| Concept decisions D1–D5 | package | `archetype_resolutions.resolutions[AR-BEST-01 / AR-ANS-01 / AR-HID-01 / AR-HID-04 / AR-HID-05]`, `anomaly_registry[ANOM-027]` |
| Twelve blocks of historical fact | EXTERNAL, retrieved in session | §6 documented table, 12 named URLs |

**What does not trace.** Twenty-four figures and dates appear in the artefact with **no source anchor anywhere in it**, and eleven of them are demonstrably false against dates the artefact itself sources elsewhere. Under this skill a missing anchor is a failure and a self-contradiction is a failure; neither is a rounding error.

### 2a. Claims contradicted by the artefact's own sourced material — the serious class

| id | Location | Claim as written | Recomputed from sourced dates | Status |
|---|---|---|---|---|
| C-15 | row 12, p21–22 | "the United States had accumulated **five hours and twenty-two minutes** of crewed spaceflight" by 25 May 1961 | Shepard, 5 May 1961, **15 min 22 s**, is the only US crewed flight before that date — stated correctly by this artefact at row 9 | FALSE, self-contradictory |
| C-22 | row 44, p65 | the ascent-stage engine "had **never been test-fired in flight with a crew aboard**" | rows 37 and 38 of the same artefact state Apollo 9 flew it with a crew in Earth orbit and Apollo 10 flew it in lunar orbit | FALSE, self-contradictory |
| C-16 | row 29, p47–48 | after the fire the programme "had **twenty-two months** of deadline left" | 27 Jan 1967 → 31 Dec 1969 = 2 y 11 m 04 d; → 20 Jul 1969 = 2 y 5 m 23 d | FALSE either way |
| C-17 | row 35, p56 | Apollo 7 flew "**twenty-two months** after the fire" | 27 Jan 1967 → 11 Oct 1968 = 1 y 8 m 14 d ≈ **20.5 months** | FALSE |
| C-18 | row 35, p56 | at Apollo 7 "the countdown read **five months and nine days**" | → decade 1 y 2 m 20 d; → landing 9 m 9 d | FALSE either way |
| C-20 | row 4, p6–7 | Sputnik was "**thirteen months** before NASA existed" | 4 Oct 1957 → 1 Oct 1958 = **362 days = 11 m 27 d** | FALSE |
| C-24 | row 41 heading | the descent ran "**20:04–20:17 UTC**" | 101:36 GET from a 13:32 UTC launch = **19:08 UTC**; PDI to touchdown = 1 h 09 m 43 s. The sourced 12.5 minutes is the final powered phase only | FALSE |
| C-14 | §1.1, §1.3, 8 rows | ten countdown-clock readings | §1.1 targets 20 Jul 1969 while row 12's title "Eight Years, Seven Months" targets 31 Dec 1969; both cannot hold. Row 11 `T−8y 00m 00d` ≠ 8 y 07 m 06 d; row 29 `T−2y 05m 24d` ≠ 2 y 11 m 04 d; row 32 `T−1y 06m` has **no date anchor at all**; row 45 "reaches zero" is false under the decade target | FALSE / UNANCHORED |
| C-31 | §1.2 table | sections per year "4.8 / 4.9 / ≈400" for Parts III–V | recomputed: **4.9 / 5.0 / 411** | MIS-COMPUTED, and this table is the concept's central quantitative claim |
| C-21 | row 42, p63 | the hatch opened "**six hours and thirty-nine minutes**" after touchdown | §6's own source says "about 6.5 hours"; no cited source gives a minute-exact value | UNSUPPORTED PRECISION |
| C-23 | row 41, p62 | "a **26-year-old** controller … called it go" | §6's source names the guidance controller and his support without ages, and the call was relayed by the CAPCOM | UNSUPPORTED |

### 2b. Claims with no anchor that are not contradicted — the disclosure class

C-25 Soviet-firsts ledger, seven dates (row 6) · C-26 Mercury Seven 9 Apr 1959, Shepard 15 min 22 s, Gagarin 108 min (rows 7–9) · C-27 NACA founded 1915 (row 3) · C-28 Gemini 3 4 h 52 m and Gemini 5 7 d 22 h (rows 21, 23) · C-29 thirty lunar orbits, December 1972, 384,400 km, 240,000 miles, non-flammable cloth (rows 31, 43, 47, 48) · C-30 transmitter ran twenty-one days, ninety-degree field of view, two vehicles "stand in museums" (rows 4, 27, 47).

The artefact already contains the correct mechanism for these — §6's "commonly cited, confirm before print" table, which flags five figures honestly. **Twenty-four more needed the same treatment and did not get it.** That inconsistency is the traceability failure: the document asserts a standard in §1.3 rule 3 ("No page carries a figure that is not dated and sourced in §6") and then breaks it in its own index.

---

## Gate 3 — Confidence layering · **FAIL → `VETO: WEAK_FOUNDATION`**

38 claims scored: 9 at `1.0 EXPLICIT`, 7 at `0.8`, 11 at `0.5 INFERRED`, 11 at `0.0 UNGROUNDED`. 24 are core. **Nine core claims score below 0.8 with no operator-visible warning.**

Schema deviation, declared: the skill's `source_type` enum is `PDF | QMDJ | NONE` and has no value for third-party research. `EXTERNAL` was added for the twelve verified blocks in §6, because AGENT.md §13 provides for `EXTERNAL` research where the brief demands a live fact and the evidence package is silent. Those claims are scored `0.8`, not `1.0`: each was checked against a retrieved source this session and the anchor is printed in the artefact, but a secondary web page is not a raw input.

The four structural strategies the book actually rests on are sound — page count (`1.0`), worksheet compliance (`1.0`), seeded-interaction compliance (`1.0`), topic provenance (`1.0`). What fails is the **collision-boundary strategy**: R4 is a veto-level hard constraint stated in the brief's strongest language ("dont even attempt to go near", L25), and three of the boundaries that satisfy it are interpretive judgements at `0.5` — the helmet gatefold against *Dressed for space* (C-04), five pages of unmanned spacecraft against *Robotics as human's first explorers* (C-05), and three failures against *The myth of perfection* (C-07). §2 discloses each boundary and argues it. **Disclosure is not a warning.** None of the three says "this is the residual risk and the mentor should confirm it", so a reader could take the boundaries as settled when they are the least settled thing in the document.

---

## Gate 4 — Adversarial omission attack · **FAIL → `VETO: BLIND_SPOT`**

### 4a. Timing contradictions — an explicit Gate 4 target, and the artefact is full of them

The countdown running head is the concept's primary device (§1.1 proxy 1). It is stated ten times and **no two statements agree on what it counts down to**. §1.1 says 20 July 1969. Row 12's title says the interval to the deadline is "Eight Years, Seven Months", which is 31 December 1969 (verified: 25 May 1961 → 31 Dec 1969 = 8 y 07 m 06 d; → 20 Jul 1969 = 8 y 01 m 25 d). Rows 36 and 38 use the landing target; row 12 uses the decade target; row 32 uses neither and is unanchored. A device that is the book's argument cannot be internally inconsistent, and the worker did not flag it.

### 4b. Hard-constraint scan of the brief

Constraint language at L6 ("has to be", "at any cost", "60 is the minimum"), L7 ("cant choose") and L25 ("dont even attempt to go near"):

| Constraint | Verdict |
|---|---|
| ≥ 60 pages | **SATISFIED** — 72, machine-verified contiguous |
| NASA-related at any cost | **SATISFIED** |
| Not one of the fourteen | **SATISFIED** |
| "dont even attempt to go near" the fourteen | **SATISFIED WITH UNWARNED RESIDUAL RISK** on three boundaries (C-04, C-05, C-07) |

### 4c. Collision inside the assignment itself — detected, resolved, not escalated

The worksheet pre-seeds `**Helmet Foldout:**` at row 27. The brief forbids going near *Dressed for space*. Both are `ASSIGNMENTS/**` inputs. The worker resolved it in favour of the hard constraint (helmet framed as a pressure vessel with a certification date, one appearance, no wardrobe or materials content) and still satisfied the seeded slot. **The resolution is defensible and the auditor does not overturn it.** But it is a genuine collision between two assignment inputs, it was resolved silently inside a table cell in §2, and it was not escalated to the operator as a decision that could reasonably go the other way. The operator's own permission — "you can ignore a column if nothing fit" — covers columns, not pre-seeded interaction labels, so it does not authorise dropping the slot.

### 4d. Evidence-package omission scan

Package `archetype_resolutions` (12 resolutions, `still_tied: false` on all three primary slots) and `anomaly_registry` (41 records: 9 HIGH, 19 MED, 13 LOW) were scanned for high-impact items the artefact ignores.

- All nine HIGH anomalies are `BASE_TRIGRAM_LABEL_MISMATCH` (8) and `STRENGTH_FIELD_NOT_REPRODUCIBLE` (1) — upstream source-labelling defects, carried with `handling` recorded in the package. **None bears on any design decision in this artefact.** No omission.
- `DAY_STEM_NOT_ON_HEAVEN` (ANOM-027) → used, D2.
- `EXPLICIT_PATTERN_NAME_VS_VALUE_DIVERGENCE` and `EXPLICIT_PATTERN_PARTIALLY_SUPPORTED` → used, D5.
- The three primary resolutions `AR-BEST-01`, `AR-ANS-01`, `AR-HID-01` and the two ranked runners-up `DEAD_METHOD_EAST_p3`, `PROXY_ON_EARTH_AT_ORIGIN_p8` → all five appear in the binding at `WORK/EDITORIAL/project_1/state/concept_binding.md`. **No high-impact chart evidence was dropped.**
- No vetoed claim survives into the artefact. No `VETO`-tagged evidence is cited anywhere in `concept_binding.md`.
- Role-boundary note: the solver's `never_reads: QMDJ.json` binds the solver role. This auditor hashed `QMDJ/EDITORIAL/project_1.json` for Gates 0–1 and did **not** open it for Gate 4; the package's registries are the authoritative derivative and re-deriving geometry from the raw source is prohibited by solver law 8. Gate 4d was therefore run against the package, which is the accepted adapter input. Declared as a deviation from the skill's literal instruction, with the reason.

### 4e. Omission scan against the brief's own content

The brief's L28 idea contains a second claim the artefact does not carry: *"Along with being the apex in the field, in which they had a late start."* The "late start" is the whole of Part I. **The "apex in the field" half appears only implicitly** — in §1.4's spike argument and in row 47. That is a defensible editorial choice, but it is a partial omission of an explicit element of the operator's own stated idea, and it is nowhere disclosed. Minor; recorded, not vetoed on its own.

---

## Failed items, consolidated

1. **C-15, C-22** — two claims false against the artefact's own sourced content.
2. **C-16, C-17, C-18, C-20, C-24** — five interval/date claims false against sourced dates.
3. **C-14** — ten countdown readings, inconsistent target, one wholly unanchored.
4. **C-31** — the pacing table's sections-per-year column mis-computed in two of five cells.
5. **C-21, C-23, C-30** — three claims asserting precision no cited source supports.
6. **C-25 to C-29** — twenty-four further figures with no source anchor, in a document that promises none exist.
7. **C-04, C-05, C-07** — three interpretive boundaries carrying a veto-level hard constraint, disclosed but not warned.
8. **§4c** — an input-vs-input collision resolved silently rather than escalated.
9. **§4e** — the "apex in the field" half of the operator's stated idea not carried and not disclosed.

## Minimal remediation pointers

- Pick one countdown target — 31 December 1969, the deadline as literally stated — and recompute all ten readings from it; anchor row 32 to a stated narrative date; change row 45 from "reaches zero" to the unused margin (splashdown → decade = 5 m 07 d).
- Correct C-15, C-16, C-17, C-18, C-20, C-22, C-24 to the recomputed values.
- Correct §1.2's sections-per-year cells to 4.9 / 5.0 / 411.
- Downgrade C-21, C-23, C-30 to the precision the cited sources actually support; delete "stand in museums".
- Add a third table to §6 — *used but not verified in this pass* — listing every C-25…C-29 figure with the row it appears on. Do not promote any of them to the documented table without checking it.
- Convert the three §2 boundary rows from disclosure to warning: state the residual risk and that the mentor should confirm it.
- Escalate the worksheet-vs-brief helmet collision to the operator explicitly, in §2 and in §7.
- Either carry "apex in the field" or state in §1.4 that it is deliberately reduced to the spike argument.

The auditor does not perform any of the above.

---

# PASS 2 — verdict: **PASS**

Re-audited 2026-09-18T01:40Z on the rewritten artefact, sha256 `cde0842c05a35970115a587466bde78e41eacdaab3605f0b1d1dbb6f1b001b65` (64,124 B). All five gates re-run from scratch; no pass-1 result carried forward.

## Gate 0 — Input presence · **PASS**
Unchanged. Four raw inputs present and readable; `LAYER_B/` non-empty; boot manifest present.

## Gate 1 — Integrity check · **PASS**
All four raw-input hashes still match `MANIFEST.json` exactly: `d9f6d817…`, `a9281eca…`, `e535d406…`, `ee434d4b…`. The artefact hash differs from pass 1 by design — the worker rewrote it — and the raw inputs did not move underneath it, which is the condition this gate exists to test.

## Gate 2 — Traceability matrix · **PASS**
Every figure in the artefact now falls into one of three declared classes, and the classes are exhaustive:

| Class | Count | Anchor |
|---|---|---|
| Structural / constraint claims | 14 | brief line number, worksheet row index, or package resolution id |
| Documented historical fact | 21 rows | §6 documented table, 21 rows of named retrieved sources |
| Commonly cited, flagged | 5 | §6 middle table, each with its confirmation step |
| Declared open | 3 | §6 "Still open" table, each with the page it appears on and what it needs |

The eleven false or unsupported claims from pass 1 were corrected rather than re-worded, and each correction was reproduced independently from dates the artefact itself sources:

| pass-1 id | Correction verified against |
|---|---|
| C-15 | Shepard 15 min 22 s, 5 May 1961 — retrieved source now in §6 |
| C-16 | 27 Jan 1967 → 31 Dec 1969 = 2 y 11 m 04 d — recomputed |
| C-17 | 27 Jan 1967 → 11 Oct 1968 = 1 y 8 m 14 d ≈ 20 months — recomputed |
| C-18 | 11 Oct 1968 → 31 Dec 1969 = 1 y 2 m 20 d — recomputed |
| C-20 | 4 Oct 1957 → 1 Oct 1958 = 362 d — recomputed |
| C-21 | reduced to the cited source's own precision ("about six and a half hours") |
| C-22 | clause deleted; the surviving text agrees with rows 37 and 38 |
| C-23 | age deleted; attribution now matches the cited source |
| C-24 | invented UTC window deleted from the heading |
| C-30 | museum clause deleted; field-of-view figure removed from the text and moved to §6 as a production input |
| C-31 | 4.9 / 5.0 / 411 — recomputed from the artefact's own spans |

Pass 2 additionally verified, by independent date arithmetic, **every** clock reading in the artefact against the single named target of 31 December 1969: `T−8y 07m 06d` (p20), `T−2y 11m 04d` (p47), `T−2y 06m 01d` (p52, now anchored to a stated narrative date of 30 June 1967), `T−1y 02m 20d` (p56), `T−0y 06m 01d` (p61), `T−0y 05m 07d` (p66). Six of six reproduce exactly. The two prose intervals at p57 (one year and ten days to the deadline; six months and twenty-nine days to the landing) and p59 (two months to the landing, seven to the deadline) also reproduce exactly.

**Three errors the pass-1 audit missed were found by the worker during correction** and are recorded here because an audit that under-reports is not a clean audit: "nineteen days after the first American suborbital flight" (20 days), "three weeks after the first human orbit" (43 days), and "eleven months after the fire" for Apollo 4 (9½ months). All three are now correct. Pass 1 was not exhaustive and should not be cited as though it were.

## Gate 3 — Confidence layering · **PASS**
38 claims re-scored. Distribution now: 10 at `1.0`, 23 at `0.8`, 5 at `0.5`, **0 at `0.0`** (pass 1: 9 / 7 / 11 / 11). Core claims below 0.8 without an operator-visible warning: **0** (was 9). The three interpretive boundaries C-04, C-05 and C-07 remain at `0.5` — they are judgements and cannot be scored higher — but each now carries an explicit residual-risk warning in §2 naming the risk, the cheapest correction, and who has to decide. That satisfies the gate's second branch.

## Gate 4 — Adversarial omission attack · **PASS**
- **Timing contradictions:** none remain. One countdown target is named in §1.1 and all ten readings derive from it.
- **Hard constraints:** all four satisfied; the three proximity judgements are now warned, not merely disclosed.
- **Input-vs-input collision (pass 1 §4c):** escalated. It is stated in §2 as a decision belonging to the mentor, repeated in §7 with the exact consequence of the alternative (row 27 becomes an empty interaction cell; one spread changes), and the operator's column-ignoring permission is explicitly noted as *not* covering a pre-seeded interaction label.
- **"Apex in the field" (pass 1 §4e):** now carried explicitly in §1.4, with the reduction stated rather than left to be noticed.
- **Evidence package:** re-scanned. All nine HIGH anomalies remain upstream source-labelling defects with `handling` recorded, none bearing on a design decision. `AR-BEST-01`, `AR-ANS-01`, `AR-HID-01`, `AR-HID-04`, `AR-HID-05`, `DEAD_METHOD_EAST_p3`, `PROXY_ON_EARTH_AT_ORIGIN_p8` and `ANOM-027` all appear in `WORK/EDITORIAL/project_1/state/concept_binding.md`. No vetoed claim reaches the artefact.
- **New content audited:** §3 (content buckets) was added after pass 1 and is audited here for the first time. Ownership parsed independently: 9 buckets, 49 rows, one-to-one, no row double-owned, no row unowned; the stated page column sums to 72 and matches §4's actual allocation bucket for bucket (17/8/6/12/8/5/4/7/5).

## Structural invariants, re-verified
49 data rows · 5 cells on every row · headings byte-identical to the worksheet · pages contiguous 1–72, total 72 against a stated minimum of 60 · all 15 pre-seeded interaction labels on their exact template rows · Interactions column left as an em dash on 33 rows · forbidden-term lint **0 violations across all 60 entries**.

## Residual risk carried forward, not cleared

1. **Three figures are declared open, not sourced** (§6): Sputnik's transmitter duration, Gagarin's 108 minutes, the Earth–Moon distance printed on the volvelle. The second is a chapter title. None may ship unchecked.
2. **Three collision boundaries are judgements** at `0.5` and need the mentor's confirmation. The helmet foldout is the exposed one.
3. **The production specification is untested.** Five gatefolds, four tipped-in inserts and a riveted volvelle in nine signatures have not been costed or checked against a binder (C-38, `0.5`, non-core).
4. **This is not a pack-level audit.** LAYER_A's technical audit document, the OPERATOR tree and `MANIFEST.md` do not exist; the worker is at `PAUSED_CONCEPT_AND_INDEX`, not HALT. The verdict above covers one artefact. A full audit is still owed at HALT.

**Final verdict: `PASS`** for the concept-and-index artefact, with the four residual risks recorded above. Released to the operator.

---

# ADDENDUM — post-pass-2 events, recorded not concealed

Two things happened after the pass-2 verdict. Neither invalidates it, and both are recorded here because an audit trail that stops at the verdict is not an audit trail.

## A. The brief changed upstream

`ASSIGNMENTS/EDITORIAL/project_1.md` on `origin/main` is now `bbe3b9632e1e52f7976ad8244089ad610557f41e718ff21b40a7c35e71ff13ba`. The copy audited in both passes was `d9f6d817fe615df53a215082bf7a6803387742b22b1122978d931991a97457ec`, which is still what the working tree holds.

- **Delta:** purely additive, +6 lines at the end of file — a `### Class Timeline [till now]` section listing three steps: *choose a topic*, *organise larger content buckets*, *finalise content structure*. Saved at `WORK/EDITORIAL/project_1/raw/assignment/brief_delta.patch`; the updated brief at `extract_origin_main.md`.
- **Effect on the audit:** none of the anchors cited in either pass moves. L3, L5, L6, L7, L9–L23, L25 and L28 are byte-identical in both versions because the change is appended. Gates 1–4 results stand.
- **Effect on the artefact:** the three added steps became requirements R8–R10. All three were already satisfied — §1–§2 (choose a topic), §3 (content buckets), §4 (finalised structure) — because the operator supplied the same three lines in-session before the upstream commit was seen. A requirement-to-location table has since been added to the artefact covering R1–R10.
- **Why no restart:** `ASSIGNMENTS/**` is immutable and was not mutated (AGENT.md §4). A hash mismatch on a *changed upstream* input normally invalidates state; here the change adds requirements that are demonstrably covered and moves no anchor, so the run was continued and the change disclosed rather than silently absorbed. **A formal re-audit against `bbe3b963…` is owed at HALT.**

Also moved upstream during the run: the audit skill itself was renamed and shortened (`PROMPT/SKILLS/Audit/skill.md`, 260 lines → `PROMPT/SKILLS/audit.md`, 190 lines), and the worksheet was committed at `ASSIGNMENTS/EDITORIAL/NASA_BOOK_CONTENT_STRUCTURE.md`. The worksheet on `origin/main` is byte-identical (`a9281eca…`) to the copy recovered during the run, which confirms the recovery was faithful. The audit ran against the 260-line version, whose gates are a superset of the 190-line version's; no gate was skipped by the rename.

## B. The artefact changed after the verdict

A requirement-to-location table was added to the artefact after pass 2, taking it from `cde0842c05a35970…` (64,124 B) to `e8e85b54fe64a3c718377a9eefbbd18a6cbec5bd7ea67239430c57b2ea321e0e` (65,751 B). **The pass-2 verdict was issued against the earlier hash.** All structural invariants were re-run on the current file and are unchanged: 49 data rows · 5 cells on every row · headings byte-identical to the worksheet · pages contiguous 1–72 · 15 of 15 seeded interaction labels on their exact rows · Interactions column empty on 33 rows · ten tables, all internally consistent · forbidden-term lint **0 of 60**. The addition is a traceability table and changes no claim, no figure and no design decision. A full third pass is not warranted for it, and this addendum is the disclosure that stands in for one.

## C. The audit's own inputs were lost and reconstructed

`WORK/**` is gitignored and was dropped when the workspace was re-materialised from a snapshot at approximately 01:51Z — after pass 2, before this addendum. The boot manifest, the recovered worksheet copy and the binding notes were gone. All were reconstructed from the hashes printed inline in this report, and every reconstructed hash was recomputed from disk and matched: `d9f6d817…`, `a9281eca…`, `e535d406…`, `ee434d4b…`. No integrity claim in either pass rests on a file that cannot be re-verified, which is the reason the hashes are printed in this report rather than only referenced. The reconstructed manifest says plainly that it is a reconstruction.

**Verdict unchanged: `PASS`** on the concept-and-index artefact, with the four residual risks from pass 2 and the re-audit obligation in §A above.
