# PROJECT 3 — Submission folder

> ## ▶ FINAL DELIVERABLE — `SOLVER_RUN/`
> The submitted work is the **Assignment Solver run** in **`SOLVER_RUN/`**, executed under
> `PROMPT/assignment_solver_charter.md`, consuming **only** the analyst's adapted package
> (`QMDJ_ANALYST_RUN/package/qmdj_analysis_package.json`) and never the raw chart.
>
> | | |
> |---|---|
> | **The deck** | `SOLVER_RUN/SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pptx` · `.pdf` (15 slides / pages) |
> | **Long-form strategy** | `SOLVER_RUN/SUBMISSION/00_off_hours_content_strategy.md` (P2-01 … P2-12) |
> | **Supporting artefacts** | calendar CSV · measurement CSV · creator dossier · copy pack · two visual mock-ups |
> | **Reading paths** | `SOLVER_RUN/ANNOTATED/` (plain English) · `SOLVER_RUN/LAYER_A/` (analyst) · `SOLVER_RUN/OPERATOR/` (technical) |
> | **Run record** | `SOLVER_RUN/MANIFEST.md` — hashes, capability ledger, requirement coverage, coverage gate, gap report, fallback flag |
> | **Result** | Coverage gate **PASS** — all 17 requirement facets terminal; 13 DIRECT · 1 INDIRECT · 3 NO_CHART_SUPPORT · 0 CONTRADICTS_KNOWN; lint clean (0 violations, binaries included); 9/9 audit checks; no fallback mode |
>
> Everything below this banner is the **earlier analyst-run material**, retained as reference. The
> analyser's own draft strategy (`ASSIGNMENT_2_STRATEGY.md`) is superseded by the solver's submission:
> same evidence, different register, requirement-bound, and extended with the brand facts recovered from
> the Assignment 1 deck.

---

## Analyst run (reference)

Assignment 2: *Content & Social Media Strategy* (`ASSIGNMENTS/MARKETING/project_3.yaml`), executed as a
**QMDJ Chart Analyst run** under `PROMPT/qmdj_chart_analyst_charter.md`, reading the chart at
`QMDJ/MARKETING/project_3.json`.

---

## What is in here

| Path | What it is |
|---|---|
| **`ASSIGNMENT_2_STRATEGY.md`** | The deliverable: slide-by-slide content for all 11 sections of the brief, every strategic decision tagged with its chart basis, its claim ID and its evidence IDs. |
| **`BRAND_SUBSTITUTION_MAP.md`** | The slots your Assignment-1 brand fills in. One pass and the deck is complete. |
| **`mockups/`** | The two visual executions the brief requires (carousel cover + Reel key frame). |
| **`QMDJ_ANALYST_RUN/`** | The analysis itself: the run configuration, the capability tools, the 25-batch coverage contract, the authored workbook, the raw state, and the 16-section output package with a human-readable report. |

---

## The analysis at a glance

| | |
|---|---|
| **Run ID** | QMDJ-P3-001 |
| **Runtime mode** | `TOOLS_PRESENT` — every capability executed as a real process; nothing emulated in-prompt |
| **Capability calls** | 21 of a 60-call budget |
| **Batch coverage** | 25 of 25 batches completed (law 29) |
| **Evidence** | 106 chart-evidence atoms (E001–E106) + 9 computed relations (R001–R009), all with provenance paths and sha256 content addresses |
| **Closed slots** | 127 (106 live atoms + 21 declared absence slots); every palace's ledger balances |
| **Claims** | 13, each with a controlled candidate set, a competing-candidate record and a guard |
| **Grammar gate** | 75 emitted lines (claim / alignment / red-team), 0 rejected, 0 ID-width violations |
| **Anomalies** | 1 (`QUESTION_OVERLOAD` — 11 facets against the charter's 7-facet cap; Q1–Q7 analysed, Q8–Q11 deferred) |
| **Context status** | `CONTEXT_FREE_PROSE_ACCEPTED` (AMEND-01; v1 `CONTEXT_DEGRADED` retained) |
| **Package status** | `partial` — honest: the gap register is non-empty because several cold annexes the charter names were not supplied (they are listed with their stand-ins in `package/14_gap_report.json`) |

### The three structural findings the strategy rests on

1. **Concentration.** The governing spirit (值符 = 天辅, the teaching star) and the duty gate (值使 = 杜门, the closing gate) both resolve to the same palace — palace 1 — and the day stem sits there too, in the explicit marker 辛加丁『狱神得奇』 with 玉女守门 and 宫生门. *One voice, teaching, from behind a closed door.* → `C001`, `C002`
2. **Two engines, two behaviours.** Display (景门 + 九天 + 天英) generates reach; generation (生门 + 太阴) accumulates value quietly. They are in different palaces and behave differently → *show for reach, teach for depth, keep the results private.* → `C003`, `C004`
3. **One closed circulation, and three friction registers.** The nine stem-value traces form a single closed ring over the eight outer palaces (`1-2-3-6-9-8-7-4`) with one spur to the centre — no isolated islands, so the strategy must be one connected system. Three palaces carry markers of breakage, repetition and alarm: forcing things there is what the structure warns against. → `C006`, `C008`

---

## How the run works (if you want to re-run or audit it)

```bash
cd /home/user/ecole-assignments
RUN=SUBMISSION/MARKETING/PROJECT_3/QMDJ_ANALYST_RUN
bash $RUN/tools/run_stage1.sh     # B0 → evidence registry (CAP-01…CAP-11, CAP-17, CAP-09)
python3 $RUN/tools/mk_sidecar.py  # B5 disposition workbook (rules declared, partition computed)
bash $RUN/tools/run_stage2.sh     # scoring, case alignment, grammar, digest, ledger, audit, conflicts
python3 $RUN/tools/render_package.py
```

Determinism: the chart is read once and never mutated; every number in the package is produced by a
process, not by prose. Re-running the four commands above reproduces the same IDs, the same tallies
and the same verdicts.

### Where to look first

- `QMDJ_ANALYST_RUN/renders/full_report.md` — the whole analysis, readable end to end
- `QMDJ_ANALYST_RUN/renders/bounded/01_structure_brief.md` — one page of pure structure
- `QMDJ_ANALYST_RUN/package/14_gap_report.json` — everything the run could not do, and why
- `QMDJ_ANALYST_RUN/authored/dependency_assumptions.json` — every bridge from chart structure to marketing practice, with its risk level

---

## Two honest notes

**On the case context.** The assignment brief is the case context, and it is the reason the chart was
cast (operator declaration, recorded as **AMEND-01**). The brief matches none of the charter's
case-context schema keys, so the ingestion path is the charter's **free_prose** route: the six slots —
casting reason, question, subject, domain, timeframe, decision — are filled from the brief, and every
row taken from it stays tagged `DECOMPOSED` with no veto power. The first pass had stamped this
`CONTEXT_DEGRADED` under the schema-mismatch rule; AMEND-01 re-classifies the path explicitly and the
old stamp is kept beside the new one for audit (`package/02_case_context_digest.json`).

**On what this is.** The chart analysis is traditional interpretive analysis of one QMDJ chart. It is
not a prediction, not evidence about any real market, and not a substitute for professional judgment.
The strategy document is a marketing strategy reasoned *from* that analysis, with each bridge
declared as an assumption.
