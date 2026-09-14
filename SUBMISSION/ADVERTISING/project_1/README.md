# ADVERTISING / project_1 — QMDJ Chart Analysis

Produced by **`PROMPT/chart_analyser.yaml`** (Carpathia-QMDJ-Chart-Analyst v4.0.0) operating as
absolute system role, then audited by **`PROMPT/SKILLS/Audit/skill.md`**
(ironclad-post-mortem-integrity-auditor).

- **Chart:** `QMDJ/ADVERTISING/project_1.json`
- **sha256:** `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`
- **Worker state:** `HALT`
- **Audit verdict:** `PASS (SCOPED: CHART-ONLY, PDF GATES NOT RUN)`

## Start here

| I want… | Read |
|---|---|
| The analysis | [`vault/wiki/Chart-Analysis-Report.md`](vault/wiki/Chart-Analysis-Report.md) |
| The audit | [`vault/output/AUDIT_REPORT.md`](vault/output/AUDIT_REPORT.md) |
| The machine package | [`vault/raw/state/chart_analysis_package.json`](vault/raw/state/chart_analysis_package.json) |
| Every remaining field (10 subsystems) | [`vault/wiki/Chart-Full-Field-Coverage.md`](vault/wiki/Chart-Full-Field-Coverage.md) |
| Everything else | [`vault/wiki/MOC.md`](vault/wiki/MOC.md) |

## Layout

```
vault/raw/          immutable chart copy, dumps, per-palace traces, all state files
vault/wiki/         Obsidian-native reasoning layer (8 articles + 9 palace cards)
vault/output/       auditor artifacts (AUDIT_REPORT.md, CONFIDENCE_MATRIX.json)
tools/              the deterministic engine (see below)
```

## Reproducing

```bash
python3 tools/p0_anatomy.py    # INIT -> CHART_INGEST -> P0_ANATOMY
python3 tools/batches.py       # B1 -> B5 palace zoom (S1..S12)
python3 tools/p6_synthesis.py  # P6_BOARD_SYNTHESIS
python3 tools/p7_full_coverage.py  # P7 every remaining field, 10 subsystems
python3 tools/p7_amend.py          # feed P7 evidence back, with explicit overrides
python3 tools/render.py        # PACKAGE_RENDER + wiki
python3 tools/report.py        # report, red team, determinism, MANIFEST
python3 tools/audit.py         # the Audit skill
```

Deterministic: `generated_at` and `run_id` are fixed, so reruns are byte-identical.
The origin-set determinism probe re-derives P0 and diffs it — currently `IDENTICAL`.

## Results

| Gate | Result |
|---|---|
| Package schema | valid |
| Field coverage | **242/242 source leaf paths cited, 0 uncited** |
| Citation integrity | 630 paths checked, **0 broken** |
| Board consistency | pass, 3 split claims recorded |
| Determinism | origin sets identical across re-derivation |
| Red team | PASS (2 attacks partially succeeded → conclusions weakened, not defended) |
| Audit gates 0–5 | all PASS (Gate 5 = field coverage) |

## Two things to know before reusing this

1. **Gate 0b was NOT RUN, not passed.** The chart analyst is assignment-blind by law
   (laws 4 and 21), so no `Assignment.pdf` exists and every PDF-anchored gate in the Audit
   skill was formally excluded. Anything assignment-bound built on this package must be
   re-audited with the PDF present.
2. **The best-path tie is now resolved — on chart evidence.** The first pass called it
   unresolvable and blamed missing assignment context. That was wrong: the discriminator was
   sitting unread in the file. Palace 8 lists the day stem Bing in `stems_in_birth_stage`;
   palace 6 lists the same Bing in `stems_in_tomb`. Birth versus burial of the actor separates
   them 0.72 to 0.64. Palace 6 is retained live as the route for quality/finishing work.

## Chart findings in one paragraph

Whole-board Fu Yin, independently confirmed: every palace has heaven = earth = hidden stem,
every star is home, every door is home. Nothing moves by itself. The day stem Bing is stranded
in the Centre and borrows palace 2 — which is void, horse-struck, clash- and self-punished, and
carries the Death door. The hour stem Jia appears on no plate at all and Wood is Dead this
season. The duty palace 9 is void, Imprisoned in both door and palace, and triple-afflicted,
with year and hour branches both stacking onto it. Marker validation passed on all three axes
(void, horse, duty), so the chart is internally consistent — the problems are real, not
artifacts. The two surviving routes both lead away from the duty palace.
