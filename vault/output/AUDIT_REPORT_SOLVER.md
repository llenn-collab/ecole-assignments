# AUDIT REPORT (Solver Submission) — Ironclad Post-Mortem & Integrity Auditor

- audited artefact: `output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md` (operator annexes read only for warning verification)
- audit time: 2026-09-16T05:30:35.459649Z
- adaptations: A1 `_SOLVER` outputs · A2 brief = PDF-equivalent (+extract fidelity check) · A3 QMDJ hash-only · A4 frozen package as chart trust-object

## FINAL VERDICT: **VETO** — `VETO: FILE_TAMPERED`

## Gate-by-gate results

### ✅ Gate 0 — Input Presence — PASS
  - assignment brief (raw original): OK
  - assignment extract (PDF-equivalent): OK
  - raw QMDJ.json (hash-only): OK
  - frozen package copy: OK
  - frozen package original (state): OK
  - boot MANIFEST.json: OK
  - chart-run machine.json: OK
  - SUBMISSION deck: OK

### ❌ Gate 1 — Integrity Check — FAIL
  - QMDJ.json sha256 vs MANIFEST.json boot: OK
  - package copy == package original (state): OK
  - package original vs machine.json HALT pin: OK
  - package original vs MANIFEST.json package entry: MISMATCH
  - brief sha256 registered by auditor (no boot entry exists): OK

### ✅ Gate 2 — Traceability Matrix — PASS
  - 48 elements; failures: 0

### ✅ Gate 3 — Confidence Layering — PASS
  - 35 core claims; weak-uncovered: 0

### ✅ Gate 4 — Adversarial Omission Attack — PASS
  - fatal items: 0

## Integrity evidence (Gate 1 detail)
| check | computed | reference | result |
|---|---|---|---|
| QMDJ.json sha256 vs MANIFEST.json boot | `2f165e078a7c21700e5f1a1f8e4486…` | `2f165e078a7c21700e5f1a1f8e4486…` | OK |
| package copy == package original (state) | `4e906b0f47d1c4dfb90c8ad3c93dad…` | `4e906b0f47d1c4dfb90c8ad3c93dad…` | OK |
| package original vs machine.json HALT pin | `4e906b0f47d1c4dfb90c8ad3c93dad…` | `4e906b0f47d1c4dfb90c8ad3c93dad…` | OK |
| package original vs MANIFEST.json package entry | `4e906b0f47d1c4dfb90c8ad3c93dad…` | `38dd238df6fd2925df4df59d99003c…` | **MISMATCH** |
| brief sha256 registered by auditor (no boot entry exists) | `b0ccd92e1cf964fec17e74dcfaa038…` | `—…` | OK |

Chronology of the stale MANIFEST entry (raw/state/progress.md, trust-verified):
- `38dd238d` — 2026-09-15T20:20/20:27Z pre-remediation render (progress.md L33-34); MANIFEST.json captured here
- `70d87cd9` — 2026-09-16T01:29Z remediation re-render (progress.md L41-42)
- `4e906b0f` — 2026-09-16T01:33Z FINAL render; audit PASS; machine.json HALT (progress.md L46-48)

## Traceability summary (Gate 2)

- elements enumerated: **48** (every slide, every headline claim, SMART pair, journey/PESO/channel tables, brand test, scope note)
- pointer classes: requirement anchors (verbatim vs raw brief) · package paths (mechanically resolved) · package claim ids (solution_seed membership)
- untraceable elements: **0** — none
- per-element verified anchors: `output/CONFIDENCE_MATRIX_SOLVER.json` (source_anchor field)

## Confidence summary (Gate 3)

- core claims scored: **35** — 1.0 EXPLICIT: 20 · 0.8 COMPUTED: 13 · 0.5 INFERRED: 1 · 0.0 flagged: 1 (non-core elements: 13)
- below-0.8 core dependencies lacking an operator-visible warning: **0**

## Findings register (all gates)
| gate | severity | item | disposition |
|---|---|---|---|
| G1 | HIGH | MANIFEST.json staleness | VETO: FILE_TAMPERED per Gate-1 letter; classified stale-lattice-entry, evidence points to misse |
| G1 | LOW | brief has no boot-manifest entry | convention gap; recommend registry fix (worker side) |
| G2 | HIGH | requirement-register quote-form defect | substance verified against raw brief; register should embed verbatim quotes (worker fix, non-bl |
| G3 | LOW | target-statement classification policy | recorded; no VETO |
| G4 | INFO | brief modal sweep | hard classes bound to verified anchors |
| G4 | INFO | anomaly registry sweep | no deck-affecting omission; optional operator disclosure note for ANO-012 (non-blocking) |
| G4 | INFO | post-remediation consistency | consistent with final audited package |
| G4 | INFO | R21 inclusion sweep (line-scoped) | compliant |
| G4 | INFO | R07 avoid-list conformance | 7/7 conformant |
| G4 | INFO | chart-trap scan | no timing/strategy contradiction |

## Failed items & minimal remediation pointers

- **Blocking — Gate 1 (FILE_TAMPERED):** `raw/state/MANIFEST.json` package entry pins pre-remediation hash `38dd238d…`; the served/authentic final package is `4e906b0f…` (corroborated by machine.json HALT pin + progress.md chronology + final chart AUDIT_REPORT). **Minimum correction (outside auditor's power):** chart agent (or orchestrator-authorized lattice repair) refreshes the MANIFEST.json package entry to the machine-pinned final hash; then re-run this audit. **No submission content change is implicated by Gates 2–4.**
- **Non-blocking:** requirements register quote-form defect (auditor re-anchored to verbatim raw text — worker should embed verbatim quotes); brief lacks boot-manifest entry (convention gap); optional OPERATOR disclosure of ANO-012.

## Scope discipline
- auditor rewrote nothing; deck untouched; every verdict anchored to raw files or verified raw-brief anchors.
