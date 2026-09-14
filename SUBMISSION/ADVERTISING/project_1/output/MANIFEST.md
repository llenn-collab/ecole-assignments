# MANIFEST

**Run:** Carpathia-QMDJ-Assignment-Solver v4.0.0
**Assignment:** `ASSIGNMENTS/ADVERTISING/project_1.md` — state tourism integrated campaign
**Output root:** `SUBMISSION/ADVERTISING/project_1/output/`

---

## 1. Inputs (immutable, hash-verified)

| Input | sha256 | Note |
|---|---|---|
| Assignment brief | `96a178833dfe2d82ab620cacfd1989c57f977ee97d2bdc7360ee93a87821f9d6` | Markdown, 64 lines, 2433 bytes. Copy at `vault/raw/assignment/Assignment.md` |
| Chart analysis package | `59ddb7eab387461f63d35ca0…` | `vault/raw/package/chart_analysis_package.json`, version 4.0.0 |
| Source chart (upstream only) | `083a393c855730e9bf62e792…` | Recorded for lineage. **Not read this phase** — law 8 |

Neither input was modified. Both hashes re-verified at audit time.

---

## 2. Version and rubric hashes

| Hash | Value | Status |
|---|---|---|
| `interpretation_protocol_v2_version_hash` | `sha256:protocol_v2_2_1_0_chart_analyst_v4` | **Exact match to reference** — no `PACKAGE_STALE` |
| Prompt 1 rubric (stamped in package) | `sha256:archetype_scoring_rubric_1_0_0_chart_analyst_v4` | Recorded |
| Solver rubric (applied this phase) | `sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4` | Applied |

Both rubric hashes are recorded deliberately. The difference is lineage, not staleness: `requirement_fit_score` is null in Prompt 1 and live in Prompt 2, and the rubric change encodes exactly that. Logged as anomaly `RUBRIC_HASH_LINEAGE`, severity LOW. The governing protocol hash matched.

---

## 3. Artefacts

### SUBMISSION/ — assessor-facing, pure English

| File | sha256 | Bytes | Deliverable |
|---|---|---|---|
| `00_README.md` | `0b3ce448a709` | 3410 | D10 |
| `01_CAMPAIGN_DECK.md` | `d3d897e5eeea` | 7207 | D01 |
| `02_RESEARCH_AND_INSIGHT.md` | `72877a0c0a38` | 5566 | D02 |
| `03_KEY_CREATIVE.md` | `4073c9e8382e` | 5580 | D03 |
| `04_TRADITIONAL_MEDIA.md` | `b8cc67bc09be` | 6228 | D04 |
| `05_DIGITAL_MEDIA.md` | `71eb31d6e775` | 7340 | D05 |
| `06_INTEGRATION_PROOF.md` | `e4e3359c445c` | 7105 | D06 |
| `07_CREATIVE_ROUTES.md` | `f87b5d623bca` | 5134 | D07 |
| `08_DELIVERY_PLAN.md` | `98dc0fa3d7ad` | 4554 | D08 |
| `09_RISK_REGISTER.md` | `1eb0eafa503c` | 4973 | D09 |

10/10 registered deliverables present. Registry is brief-derived; `UNGROUNDED_PACK` fallback not used.

### ANNOTATED/ — ordinary-English situation commentary

| File | sha256 | Bytes |
|---|---|---|
| `00_STATUS.md` | `2c35cee15e78` | 6122 |

### OPERATOR/ — chart terminology permitted

| File | sha256 | Bytes |
|---|---|---|
| `COMMENTS.md` | `c099c72f2317` | 6070 |
| `MAPPINGS.md` | `e756810e3862` | 4957 |
| `PATH_RANK.md` | `aa65e5f3e4f2` | 3799 |

### LAYER_A/

| File | sha256 | Bytes |
|---|---|---|
| `LAYER_A_TECHNICAL_AUDIT.md` | `de6f0a7254cb` | 10235 |

Five required sections, in required order.

---

## 4. Audit verdict

| Gate | Name | Status |
|---|---|---|
| 0a | `no_qmdj_read_gate` | PASS — 0 reads, guard verified live |
| 0b | `assignment_input_gate` | PASS |
| 1 | `package_schema_gate` | PASS — 9/9 |
| 2 | `lint_terms` | PASS — 0 violations |
| 3 | `layer_a_contract` | PASS — 5/5, correct order |
| 4 | `tree_contract` | PASS |
| 5 | `claim_citation_gate` | PASS — 8 live claims, 0 uncited |
| 6 | `registry_status_gate` | PASS — 10/10 |

**VERDICT: PASS (8/8).** AUDIT_FIX cycles used: 0 of 3. Machine-readable record: `vault/raw/state/solver_audit.json`.

### Gate failures found and fixed at source

The suite did not pass first time, and no gate was relaxed to make it pass.

| Run | Verdict | Failure | Resolution |
|---|---|---|---|
| 1 | FAIL 5/8 | Gate 0a substring scan flagged docstrings and its own denylist | Match genuine I/O calls only |
| 1 | FAIL | Gate 1 read `status` where records carry boolean `pass` | Read the real field |
| 1 | FAIL | `MANIFEST.md` absent — **genuine finding** | Manifest written |
| 2 | FAIL 7/8 | Gate 0a flagged a real chart read in `common.py`, a module not executed this phase | Scan the transitive import closure from solver entry points, not filenames |
| post-PASS | **Vacuous pass** | Gate 6 read a key the registry does not use, so it verified **nothing** while reporting 10/10 | Read `output_path`; treat unresolvable entries as failures. Confirmed by negative test |

The gate 6 finding is the most serious: a green gate that checks nothing manufactures false confidence. It was caught only because registry statuses were being updated by hand. Gates 0a, 1, 4 and 6 have each now been observed to fail on a broken input and pass on a sound one. Detail in `vault/wiki/Risk-And-Audit-Log.md`.

---

## 5. Compliance statement

| Law / constraint | Status |
|---|---|
| Never read `QMDJ.json` (law 8) | 0 reads; `guard_path` raises `PermissionError: DENIED_PATH` |
| Never re-run B1–B5 or Phase 6 | Not re-run |
| Never re-derive palace geometry | Not re-derived |
| Inputs immutable | Verified by hash |
| No questions asked of the user | None |
| No fabricated brief text or package fields | None |
| No fabricated PDF page anchors | None — Markdown anchors used, disclosed in `OPERATOR/COMMENTS.md` §2 |
| Every live claim cites a resolution | 8/8 |
| No silent tie-breaking | 0 ties; all margins published in `OPERATOR/PATH_RANK.md` |
| Vetoed claims never ship | No vetoes raised |
| Logo artwork excluded | `EXCLUDE_ARTWORK`; written direction only |
| SUBMISSION language purity | Lint PASS over 10 files |

---

## 6. Resolutions

| Resolution | Slot | Winner | Score | Status |
|---|---|---|---|---|
| `SR-ANSWERS-01` | my_answers | `ANS-DUTY-PALACE-9-VOID-SHOWPIECE` | 0.9500 | RESOLVED |
| `SR-HIDDEN-01` | hidden_problems | `HID-VOID-SHOWPIECE-UNDER-PUNISHMENT` | 0.9600 | RESOLVED |
| `SR-BEST-01` | best_solution | `BEST-LIFE-DOOR-NE-P8-WITH-LIUHE` | 0.8200 | RESOLVED |

0 `STILL_TIED`. 2 candidates hard-eliminated before scoring. `SUP-001`: requirement fit widened margins without reordering any slot.

---

## 7. Anomalies

| ID | Severity | Status |
|---|---|---|
| `RUBRIC_HASH_LINEAGE` | LOW | Explained, both hashes recorded, no remediation required |
| Markdown input where spec names PDF | INFO | Faithful substitution; nothing fabricated; disclosed |

---

## 8. Tooling

| Tool | Role |
|---|---|
| `tools/solver_common.py` | Paths, `guard_path` deny-list, hashing, I/O, heartbeat, `lint_terms`/`lint_tree` |
| `tools/s1_ingest.py` | PACKAGE_VALIDATE + PDF_INGEST |
| `tools/s2_solution_engine.py` | P7_SLOT_BIND + SOLUTION_ENGINE |
| `tools/s3_audit.py` | 8 solver gates implementing the Audit skill |

Chart-phase tools (`p0`–`p7`, `render`, `report`, `audit`) were reused unmodified and not re-run.
