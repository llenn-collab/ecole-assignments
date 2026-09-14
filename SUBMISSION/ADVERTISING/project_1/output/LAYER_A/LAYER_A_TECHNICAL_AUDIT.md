# Layer A — Technical Audit

**Tree:** LAYER_A · Sections appear in the required fixed order.

---

## 1. Executive Reading

The assignment is a state-tourism integrated campaign brief whose stated purpose is to teach the difference between an integrated campaign and an adapt campaign. The chart package, read before the brief was scored, says three things that map onto that purpose with unusual directness.

**The governing answer:** lead with participation, not spectacle. Build the campaign as an invitation the audience accepts and passes on, with every medium doing one job the other five cannot do. This resolved cleanly at 0.8200 with a perfect requirement fit of 1.00, against a runner-up at 0.7170.

**The governing warning:** the most visible part of the work is the weakest. The headline idea is announced loudly and carried lightly; the structure beneath it is more solid than the surface. Five hidden problems ship live, all consistent with each other and with the answer.

**The resulting output:** ten SUBMISSION deliverables built around a single divisible idea — *The Hundred-Year Handshake* — deployed across three traditional and three digital channels, each exploiting a capability unique to its medium, with the integration claim tested by a formal Swap Test rather than asserted.

**Confidence: HIGH** on the governing answer, **MEDIUM** on the audience characterisation, which is the one load-bearing claim that is reasoned rather than evidenced.

**Zero reads of `QMDJ.json`.** Enforced mechanically.

---

## 2. Walkthrough

### 2.1 State progression

`INIT → PACKAGE_VALIDATE → PDF_INGEST → P7_SLOT_BIND → SOLUTION_ENGINE → SYNTHESIZE`

No state was skipped and no state was re-entered.

### 2.2 PACKAGE_VALIDATE — 9/9 PASS

| Check | Result |
|---|---|
| Schema keys present (13) | PASS |
| Semver well-formed | PASS |
| Source sha256 present | PASS |
| `interpretation_protocol_v2_version_hash` matches reference | **PASS — exact match** |
| Rubric hash present | PASS (lineage difference logged, see §4) |
| `prompt1_requirement_fit_all_null` | PASS |
| Upstream field coverage 242/242 | PASS |
| Broken internal links | 0 |
| Board consistency | PASS |

The protocol hash is the one that governs `PACKAGE_STALE`. It matched exactly, so no halt was warranted.

### 2.3 PDF_INGEST

Input is Markdown (`project_1.md`, 64 lines, sha256 `96a17883…f9d6`), not PDF. No extractor was invoked; no page anchors were fabricated. Markdown headings and line numbers serve as anchors.

Produced: 22 requirements (R01–R22), 10 deliverables (D01–D10), logo boundary `EXCLUDE_ARTWORK`, rubric guess with inferred weights.

Hard constraints identified: **R05** (no sight-seeing/shopping/common spots), **R10** (craft the idea per medium), **R01** (integration across six media, not size adaptation).

### 2.4 P7_SLOT_BIND — 6/6 bound, 0 unbound

Every chart slot bound to an assignment question. No slot invented, no deliverable created to consume a spare slot. Full table in `OPERATOR/MAPPINGS.md` §1.

### 2.5 SOLUTION_ENGINE

Two candidates hard-eliminated **before** scoring (R05; R05+R01). Three resolutions scored; all RESOLVED; zero `STILL_TIED`.

### 2.6 SYNTHESIZE

Ten SUBMISSION files, one ANNOTATED file, three OPERATOR files, this audit, and the manifest. Forbidden-term lint run over `output/SUBMISSION/`: **PASS, 0 violations.**

---

## 3. Candidates and Selection

### 3.1 Best solution (SR-BEST-01)

| Candidate | Score | rfit | Outcome |
|---|---|---|---|
| `BEST-LIFE-DOOR-NE-P8-WITH-LIUHE` | **0.8200** | 1.00 | Selected |
| `BEST-OPEN-DOOR-NW-P6-WITH-DING` | 0.7170 | 0.77 | Retained — key creative standard |
| `BEST-JING-DOOR-S-P9` | 0.5670 | — | Not selected |
| `BEST-RIDE-THE-HORSE-AT-P2` | — | — | Hard-eliminated pre-scoring (R05) |
| `BEST-PUSH-THE-SHOWPIECE-AT-P9` | — | — | Hard-eliminated pre-scoring (R05, R01) |

Margin 0.1030. The decisive factor is that Liu He supplies a transmission mechanism — something handed over and accepted — which the integration requirement rewards heavily. The Open door supplies authority without transmission.

The runner-up was not discarded. It governs the key creative, where the audience is necessarily passive and finish is the requirement. This split is a judgement call and is flagged as such in `OPERATOR/COMMENTS.md` §5.1.

### 3.2 Answers (SR-ANSWERS-01)

Winner `ANS-DUTY-PALACE-9-VOID-SHOWPIECE` at 0.9500 (rfit 0.90); secondary `ANS-ACTOR-DISPLACED-TO-CENTRE` at 0.8815 ships live alongside it, since it answers a different question. Third candidate rejected at 0.2602 on board-consistency failure with four contradictions.

### 3.3 Hidden problems (SR-HIDDEN-01)

Ranked slot; top five ship (0.9600, 0.9228, 0.8515, 0.6803, 0.6490). Sixth withheld at 0.1902.

### 3.4 Tie handling

No ties. All margins stated in `OPERATOR/PATH_RANK.md`. No silent tie-breaking occurred; no `STILL_TIED` split candidates were required.

---

## 4. Confidence and Residual Risk

### 4.1 Confidence by claim

| Claim | Confidence | Basis |
|---|---|---|
| BEST-01 participation over spectacle | HIGH | 0.8200, rfit 1.00, margin 0.1030, uncontradicted |
| ANS-01 one idea across six media | HIGH | Winner at 0.9500, eight supporting evidence paths |
| ANS-02 audience characterisation | **MED** | Single evidence path; reasoned, not validated |
| HID-01 visible part is weakest | HIGH | 0.9600, zero contradictions |
| HID-02 no natural home | HIGH | 0.9228, zero contradictions |
| HID-03 nothing moves by itself | HIGH | 0.8515 |
| HID-04 craft route seduction | MED | 0.6803 |
| HID-05 late-visible connector | MED | 0.6490 |

### 4.2 Anomalies

**`RUBRIC_HASH_LINEAGE` — severity LOW.** Package carries the chart-analyst rubric hash; this phase applies the assignment-solver rubric hash. Expected: `requirement_fit_score` goes live in this phase, which is exactly what the rubric change encodes. Lineage, not staleness. Both hashes recorded in `MANIFEST.md`. The governing protocol hash matched exactly.

**Markdown-not-PDF.** Noted, not remediated — the substitution is faithful and nothing was fabricated. `OPERATOR/COMMENTS.md` §2.

### 4.3 Residual risk

| Risk | Severity | Status |
|---|---|---|
| Audience insight unvalidated | Medium | Disclosed in three SUBMISSION locations |
| Research secondary only | Medium | Disclosed in `00_README.md` and `09_RISK_REGISTER.md` |
| Split governance between two routes | Low | Deliberate, scored, documented both operator- and user-facing |
| Over-tourism damaging the subject | High (campaign-level) | Designed against: caps, council-routed booking, volume refused as a success metric |
| Inferred grading weights | Low | Used only for balance checking; never to skip a requirement |

### 4.4 Compliance

| Law | Status |
|---|---|
| No `QMDJ.json` reads (law 8) | **0 reads** — `guard_path` raises `PermissionError: DENIED_PATH` |
| B1–B5 / Phase 6 not re-run | Not re-run; package consumed as given |
| Palace geometry not re-derived | Not re-derived |
| Inputs immutable | Both inputs hash-verified, unmodified |
| No user questions asked | None asked |
| No fabricated brief text or package fields | None |
| Every live claim cites a resolution | All 8 live claims cite one of SR-ANSWERS-01, SR-HIDDEN-01, SR-BEST-01 |
| Vetoed claims never ship | No vetoes raised |
| AUDIT_FIX cycles | 0 of 3 used |
| Logo artwork excluded | No artwork produced; written direction only |
| SUBMISSION language purity | Lint PASS, 0 violations |

---

## 5. Full Technical Mapping — Appendix

### 5.1 Slot → question → deliverable

| Slot | Question | Resolution | SUBMISSION location |
|---|---|---|---|
| `YS-DUTY-9` | Q1 my_answers | SR-ANSWERS-01 | `01` §4; `ANNOTATED` §2.1 |
| `YS-DAY-BING` | Q4 my_answers | SR-ANSWERS-01 (secondary) | `02` §2; `ANNOTATED` §2.2 |
| `YS-HOUR-JIA` | Q5 timing | — | `08` §4 launch sequence |
| `YS-LEAD-XIN` | Q1 key creative | SR-BEST-01 runner-up | `03` §5, §8 |
| `YS-OPEN-6` | Q3 best_solution (craft) | SR-BEST-01 runner-up | `03`; `06` §4 |
| `YS-LIFE-8` | Q3 best_solution (reach) | SR-BEST-01 winner | `01` §5; `04`; `05` |

### 5.2 Live claims

| Claim | Slot | Confidence | Resolution | Requirements |
|---|---|---|---|---|
| ANS-01 | my_answers | HIGH | SR-ANSWERS-01 | R06, R01, R12 |
| ANS-02 | my_answers | MED | SR-ANSWERS-01 | R03, R19 |
| HID-01 | hidden_problems | HIGH | SR-HIDDEN-01 | R01, R10, R22 |
| HID-02 | hidden_problems | HIGH | SR-HIDDEN-01 | R03, R19 |
| HID-03 | hidden_problems | HIGH | SR-HIDDEN-01 | R14, R15 |
| HID-04 | hidden_problems | MED | SR-HIDDEN-01 | R20, R07 |
| HID-05 | hidden_problems | MED | SR-HIDDEN-01 | R22, R13 |
| BEST-01 | best_solution | HIGH | SR-BEST-01 | R01, R03, R06, R08, R09, R10, R20, R22 |

**8 live claims, 8 citing a resolution, 0 uncited, 0 split.**

### 5.3 Scoring functions

```
final_score      = 0.35·tier + 0.25·support + 0.20·(1−contra)
                 + 0.10·consistency + 0.10·requirement_fit

requirement_fit  = 0.40·requirement_coverage
                 + 0.40·hard_constraint_compliance
                 + 0.20·audience_and_tone_fit
```

Hard-constraint elimination runs **before** scoring. Eliminated candidates carry no score.

### 5.4 Requirement coverage

22 of 22 requirements have a named coverage location. Hard constraints R01, R05, R10 each additionally verified in `06_INTEGRATION_PROOF.md` §6 and §2.

### 5.5 Plain-English translation table

| Technical reading | SUBMISSION/ANNOTATED wording |
|---|---|
| Whole-board stasis | "Nothing moves by itself; each execution must be pushed" |
| Void showpiece at duty palace | "The most visible part is the weakest" |
| Displaced actor, no seat | "No natural home for the work" |
| P8 Life door with Liu He | "An invitation the audience accepts and passes on" |
| P6 Open door with Ding | "Craft, finish and authority" |
| Jing door Imprisoned | "Announced but does not land" |

This table is the boundary control between trees. No term in the left column appears anywhere in `SUBMISSION/`.

### 5.6 Artefact inventory

| Tree | Files |
|---|---|
| `SUBMISSION/` | 10 |
| `ANNOTATED/` | 1 |
| `OPERATOR/` | 3 |
| `LAYER_A/` | 1 |
| Root | `MANIFEST.md` |
