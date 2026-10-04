# OPERATOR / SCORE_SOURCES

| Product | Stamp |
|---|---|
| Candidate scoring | `SCORE_SOURCE=TIER0_TOOL_CAP-10/v1` |
| Lint scan | `EMULATED_LINT` (no external lint binary in this runtime; lexical + phrase + semantic passes implemented deterministically in `tools/scap.py`) |
| Ledger reconciliation | CAP-09, enumerated addends ≤ 9 |
| Requirement fit | CAP-10 lookup tables; model performed no arithmetic (law 26) |
| Evidence provenance | adapted package view, MAPPED from the analyst v7 package; source hashes in MANIFEST.md |

**Upstream scores** from the analyst package (claim confidences) are retained for traceability and stamped
`IGNORED_UPSTREAM_SCORE` for the purposes of this solver's ranking, per rubric note.
