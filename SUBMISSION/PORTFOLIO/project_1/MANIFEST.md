# MANIFEST — PORTFOLIO / project_1

Pack record for **You On A Shelf: Building A Creative Persona** (brief `ASSIGNMENTS/PORTFOLIO/project_1.md`, chart `QMDJ/PORTFOLIO/project_1.json`).
Format per `AGENT.md` §9 / `PROMPT/prompt.yaml → output_pack.manifest`. Chart reasoning is cited by section, never reproduced here; the audit trail lives in `LAYER_A/`.

## Artifacts

| Path | Tree | sha256 | Deliverable ids |
|---|---|---|---|
| `LAYER_B/LAYER_B_SUBMISSION.md` | LAYER_B | `0190b4870f1e1f43390671a35478cc2c86c1828c6c4b16cc080ffe04086370b3` | D1–D2, D4–D10 |
| `LAYER_A/LAYER_A_TECHNICAL_AUDIT.md` | LAYER_A | `bd9aa335cfdc60c11ea250c753f74963b61cfc2fae2b0c7685da08d17197ab73` | audit of D1–D11 |

Hand-in set: `LAYER_B/` + this file. `LAYER_A/` is committed for the operator's audit, not for the marker.

## Deliverable registry

Built from the brief, not from a template. `except_logo` marks rows where artwork itself is excluded while written direction is still due.

| id | name | format | audience | level | except_logo | source requirement ids | output path | status |
|---|---|---|---|---|---|---|---|---|
| D1 | Product Name + rationale | md | marker/client | must | no | R2, R8 | `LAYER_B/…md` §THE PRODUCT, §4.5 | COVERED |
| D2 | Identity system — mark construction, colour, type, material | md | marker/client | must | yes | R3 | §4.1–4.4 | COVERED as written design direction |
| D3 | Logo artwork (drawn mark) | image | marker/client | must (brief) / excluded here | yes | R3 | — | EXCLUDED_LOGO — construction spec in §4.1 for the student to draw |
| D4 | Packaging — format, finish, final copy on all faces | md | marker/client | must | no | R4 | §5, §4.4 | COVERED |
| D5 | Mockups — shot list + shooting rules | md | marker/client | must | no | R5 | §6 | COVERED — count is a judgement call, see R11 |
| D6 | USP — functional + emotional | md | marker/client | must | no | R6 | §2 | COVERED |
| D7 | Audience — employer's challenge + your role | md | marker/client | must | no | R7 | §3 | COVERED |
| D8 | 3-minute presentation script, timed | md | marker/client/tutor | must | no | R9 | §7 | COVERED |
| D9 | Portfolio "Big Picture" carry-over system | md | marker/client | must | no | R10 | §8 | COVERED |
| D10 | Self-audit against the stated grading criteria | md | marker/client | should | no | R10 | §9 + appendix | COVERED |
| D11 | SWOT + colour/element/stationery symbolism | — | — | may | no | R12 | — | EXCLUDED_BY_BRIEF — "need not be included" |

## Requirement ids (source: `LAYER_A` Phase 0, sections A–J)

| id | Requirement | Brief anchor |
|---|---|---|
| R1 | Objective + framing question; keep it fun | Phase 0 §A |
| R2 | Final deliverable: Product Name | §B.1 |
| R3 | Final deliverable: Identity; logo sketches W1, completed W2 | §B.2, §I |
| R4 | Final deliverable: Packaging; final copy | §B.3, §D |
| R5 | Final deliverable: Mockups | §B.4 |
| R6 | USP: functional AND emotional registers | §C.1 |
| R7 | Audience: challenge + your role | §C.2 |
| R8 | Product = name + logo design sketches (Week 1) | §C.3 |
| R9 | Sequence & timing: W1→W2, 25 Aug / 01 Sep (3 min), 07 Sep with revisions | §D, §E.1–E.2 |
| R10 | Graded on: Uniqueness · Use of Metaphor · Design & Copy · Big Picture | §F.1–F.4 |
| R11 | Not determinable from the brief: submission format/page count; mockup count | §J.2, §J.4 — FLAGGED, not invented |
| R12 | Optional process work excluded from presentation | §H |

Coverage: every requirement is COVERED, EXCLUDED_LOGO, or EXCLUDED_BY_BRIEF; R11 is flagged in both layers (student action: check NLET/tutor). Zero silent `UNCOVERED`.

## Sources (immutable — verify before re-running)

| Path | sha256 |
|---|---|
| `ASSIGNMENTS/PORTFOLIO/project_1.md` | `49878beb37258e57ed1413ece15ee59e8e7c6490093feaa139bf3421218bb84f` |
| `QMDJ/PORTFOLIO/project_1.json` | `00f6353bbe953bba8605011787c06c6ed43c4ded9f5eb77c87b9f28a178480ed` |
| `PROMPT/prompt.yaml` | `98c3369591f92a47beb623b29798477caf757ec4e6619e04c70dcdeda2e149ca` |

## Notes

- **Packaging:** single-file carve-out per `AGENT.md` §2 — the brief names the artefacts, so no 00–07 pack (`UNGROUNDED_PACK` unused). `LAYER_A` carries the ANNOTATED and OPERATOR faces as sections of one audit file; `00_STATUS` equivalent = *FINAL SOLUTION AUDIT* + revision addendum; `PATH_RANK`-equivalent material stays inside `LAYER_A` only.
- **Linter:** LAYER_B passes `PROMPT/forbidden_terms.txt` — 0 violations (checked 2026-09-13).
- **Layout:** migrated 2026-09-13 from legacy flat `SUBMISSION/PORTFOLIO/PROJECT_1/` to the canonical case-correct tree above; content of both layers unchanged apart from the audit's header path corrections.
