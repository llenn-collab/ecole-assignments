# MANIFEST — ADVERTISING / project_1
run: ADVERTISING-project_1-20260913T085250Z · rendered: 2026-09-13T09:30:59Z · post-mortem applied at 2026-09-13T09:30:59Z

Single-file pack form per AGENT.md §2 carve-out (brief names one final deliverable: the campaign deck).

| path | sha256 | tree | deliverable ids | requirement coverage |
|---|---|---|---|---|
| SUBMISSION/ADVERTISING/project_1/LAYER_B/LAYER_B_SUBMISSION.md | 46848c8f330f09739130150363f43b239e69e4f63c6efa9435b5928b0749591c | LAYER_B | D-01…D-08 | R-01..R-14 all COVERED (map: LAYER_A §4) |
| SUBMISSION/ADVERTISING/project_1/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md | 080b2305812018edc35a5690b6ea24b46a01ce71d5ffe08fe57790738e805170 | LAYER_A | audit pack | status+ANNOTATED+COMMENTS+MAPPINGS+PATH_RANK+CONFIDENCE-LEDGER |

## Source integrity (dual-checked post-mortem)

- `ASSIGNMENTS/ADVERTISING/project_1.md` sha256 `96a178833dfe2d82ab620cacfd1989c57f977ee97d2bdc7360ee93a87821f9d6` — equals INIT hash; `git diff HEAD` clean → untouched.
- `QMDJ/ADVERTISING/project_1.json` sha256 `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7` — equals INIT hash; `git diff HEAD` clean → untouched.
- `PROMPT/prompt.yaml` sha256 `98c3369591f92a47beb623b29798477caf757ec4e6619e04c70dcdeda2e149ca` — `git diff HEAD` clean → untouched.

## Exclusions

- Logo/artwork boundary: no mark/wordmark/lockup/favicon/grid/SVG/rendered-image artwork anywhere in the pack (brief requested none); written brand-usage note only (Slide 16).
- Media creatives delivered as designer-ready written specs; no binary artwork committed.

## Gates (final, after post-mortem)

- LAYER_B forbidden-term linter (60 seeded terms, word-boundary/substring rules per PROMPT/forbidden_terms.txt): **PASS — 0 violations**
- Advisory context pass: hits adjudicated ('tourism board' = ordinary English); jargon-word rewordings applied defensively.
- Coverage: 14/14 requirements COVERED · 0 UNCOVERED · logo EXCLUDED by default.
- Evidence re-verification: every resolvable claim path machine-checked against the raw JSON — **54 VERIFIED, 0 MISMATCH**; 6 legitimate cross-palace aggregates logged in WORK/state/postmortem.json with trace proofs. Four recorded values normalised to exact source fields (2 truncations + 2 annotation artifacts) — no claim direction changed, only precision hardened.
