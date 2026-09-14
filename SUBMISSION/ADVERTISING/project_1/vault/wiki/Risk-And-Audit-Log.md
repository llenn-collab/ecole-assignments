---
id: risk-and-audit-log
type: audit
palace_ids: []
phase: SYNTHESIZE
batch: S3
sources: ["raw/state/solver_audit.json", "raw/state/solver_anomalies.json"]
status: live
---

# Risk-And-Audit-Log

Implements `PROMPT/SKILLS/Audit/skill.md` for the solver phase.

## Gate results — VERDICT PASS (8/8)

| Gate | Name | Status | Detail |
|---|---|---|---|
| 0a | `no_qmdj_read_gate` | PASS | 0 reads; guard verified live; scope = 4 reachable modules |
| 0b | `assignment_input_gate` | PASS | sha256 `96a17883…`, 2433 bytes |
| 1 | `package_schema_gate` | PASS | 9/9 |
| 2 | `lint_terms` | PASS | 0 violations over 10 files |
| 3 | `layer_a_contract` | PASS | 5/5 sections, correct order |
| 4 | `tree_contract` | PASS | All trees and minimum files |
| 5 | `claim_citation_gate` | PASS | 8 live claims, 0 uncited |
| 6 | `registry_status_gate` | PASS | 10/10 deliverables present |

Machine record: `vault/raw/state/solver_audit.json`. **AUDIT_FIX cycles used: 0 of 3.**

## Gate failures found and fixed at source

The first audit run returned **FAIL (5/8)**. All three failures were fixed at source; **no gate was relaxed to make the run pass.**

### Failure 1 — gate 0a false positive (my bug)

The gate scanned for the substring `QMDJ` anywhere in solver tool source. This flagged docstrings, the denylist definition, and the gate's own name.

**Wrong fix:** exclude those lines by pattern. **Fix applied:** match only genuine I/O calls whose argument mentions a QMDJ path, and skip comment lines.

### Failure 2 — gate 1 false positive (my bug)

The gate read `c["status"] == "PASS"`, but validation records use a boolean `pass` field. It reported 0/9 against a record that was genuinely 9/9.

**Fix applied:** read the actual field, and additionally require the record's top-level `pass` to be true.

### Failure 3 — gate 4 genuine finding

`MANIFEST.md` did not exist. The gate was correct. **Fix applied:** wrote the manifest.

### Second run — a real finding, correctly scoped

Run 2 returned FAIL (7/8): gate 0a flagged `common.py:161: with open(QMDJ_PATH...)`. That is a **true read of the chart file** — but in a chart-phase module not executed this phase.

**Wrong fix:** exclude `common.py` by name — unsound, since a future import would go undetected.
**Fix applied:** compute the transitive import closure from the three solver entry points and scan only reachable modules. The closure is 4 modules; `common.py` is not among them. If any solver module ever imports it, the gate catches it automatically.

This is the distinction the audit skill exists to enforce: the gate now tests *reachability*, which is the real property, rather than a filename, which is a proxy.

### Failure 4 — gate 6 was passing vacuously (the most serious finding)

Discovered *after* the suite already reported PASS (8/8), while updating registry statuses.

Gate 6 read `d["filename"]` or `d["path"]`. Registry entries actually carry **`output_path`**. Every lookup returned `None`, and the loop's `if fn and ...` guard silently skipped every entry. The gate reported **"10/10 present" while checking nothing at all.**

A green gate that verifies nothing is worse than a red one: it manufactures false confidence. Had all ten deliverables been absent, this gate would still have reported PASS.

**Fix applied, in two parts:**
1. Read the correct key, `output_path`, resolved against the run root.
2. Treat an entry with **no** resolvable path as a **failure** (`unaddressed`), not as something to skip. The vacuous-pass branch is now impossible by construction.

**Verified by negative test:** a deliverable was temporarily moved out of the tree. The gate returned `FAIL 9/10 present; missing ['output/SUBMISSION/09_RISK_REGISTER.md']`, and PASS again once restored. A gate that has never been observed to fail has not been tested.

**Generalised lesson:** every gate in this suite should be assumed vacuous until it has been seen to fail on a deliberately broken input. Gates 0a, 1, 4 and 6 have all now been observed failing and then passing. Gates 0b, 2, 3 and 5 were observed failing during earlier development.

## Anomalies

| ID | Severity | Status |
|---|---|---|
| `RUBRIC_HASH_LINEAGE` | LOW | Expected. Prompt 1 stamped the chart-analyst rubric; Prompt 2 applies the solver rubric because `requirement_fit_score` goes live. Lineage, not staleness. Both hashes in `MANIFEST.md`. The governing protocol hash matched exactly |
| Markdown input, spec names PDF | INFO | Faithful substitution. No extractor invoked, no page anchors fabricated. See [[Assignment-Corpus]] |

## Compliance

| Law | Status |
|---|---|
| Never read `QMDJ.json` | 0 reads, mechanically enforced |
| Never re-run B1–B5 / Phase 6 | Not re-run |
| Never re-derive palace geometry | Not re-derived |
| Inputs immutable | Hash-verified twice |
| No user questions | None asked |
| No fabricated brief text or package fields | None |
| Every live claim cites a resolution | 8/8 |
| No silent tie-breaking | 0 ties; margins published |
| Vetoed claims never ship | 0 vetoes raised |
| Logo artwork excluded | `EXCLUDE_ARTWORK` |

## Carried-forward correction

Chart-phase **OVR-001** stands: the original AR-BEST-01 verdict claimed the P6/P8 discriminator required assignment information. That was **wrong** — the discriminator was in the chart, in fields not yet read.

The lesson governs this phase: **never declare something unresolvable before every field has been read.** Hence the hard 242/242 coverage gate upstream. The superseded verdict is preserved, not deleted.

## Linked

[[Red-Team]] · [[Solution-Live]] · [[Rubric-Guess]] · [[Constraints-And-Deliverables]]
