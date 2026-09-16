---
id: "solution-live"
type: "run-log"
state: "SYNTHESIZE"
updated: "2026-09-16T03:00:06Z"
---

# Solution Live — run ledger

- run: solver v4.0.0 on package 5.0.0 (sha256 4e906b0f47d1c4df…)
- states DONE: INIT, PACKAGE_VALIDATE (PASS_WITH_DEVIATION DEV-001/002), PDF_INGEST (24 reqs), P7_SLOT_BIND
  (3 slots), SOLUTION_ENGINE (winner solver_score 0.8647, margin
  0.1167), SYNTHESIZE (deck + operator + Layer A + red team + wiki)
- pending: RENDER_OUTPUT gates + MANIFEST, then HALT
- machine file: `raw/state/solver_machine.json`; progress log: `vault/progress.md` ([SOLVER] rows)

Key numbers: requirements 24 (22 must, 4 must_not incl. EXCLUDED_LOGO rows, 1 should); deliverables 1 + 1 excluded;
answers slot solver_score 0.8667; hidden problems 5 (scores
[0.8667, 0.7889, 0.7611, 0.7611, 0.7611]); budgets all within objective.
