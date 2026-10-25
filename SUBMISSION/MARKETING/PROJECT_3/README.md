# PROJECT_3 — QMDJ Chart Analysis for MARKETING Assignment 3
## Search Discoverability & Digital PR Strategy

This folder is the QMDJ Chart Analyst package (charter v7.1.0, `PROMPT/qmdj_chart_analyst_charter.md`)
for the chart cast for `ASSIGNMENTS/MARKETING/project_3.yaml`.

- **Chart source (immutable, read once)**: `QMDJ/MARKETING/project_3.json`
  — Yi Dun · Lun Cang Jia · Hourly Rotating Qimen, Yin Dun 8 Ju · 丙午年 戊戌月 壬申日 庚戌时 · 霜降中元
  — 值符 天辅 → Palace 6 · 值使 杜门 → Palace 7
- **Case context (CONTEXT_NOT_CHART)**: `ASSIGNMENTS/MARKETING/project_3.yaml`
  — ingested as MIXED form; stamped **CONTEXT_DEGRADED** (rows tagged DECLARED/DECOMPOSED)
- **Runtime mode**: TOOLS_PRESENT — all mechanical work (registry, digest, coverage, scoring)
  is executed by `tools/qmdj_toolkit.py`; SCORE_SOURCE = TOOL_TIER2.

## Read this first

| File | What it is |
|---|---|
| `renders/REPORT.md` | **Full human-readable report** — board card, claims with evidence IDs, CMAP case alignment, slide-by-slide guidance for slides 1–12, hypotheses, red team, decision support, gaps |
| `renders/BOUNDED_EXEC.md` | Bounded executive render (top verdicts + decision guard + bounded recommendation) |
| `package/00..16_*.json` | Machine-readable output package, sections 00–16 per charter |
| `state/extract.json` | Board card + evidence registry (191 E-atoms, 34 R-atoms, 60 pattern records) |
| `state/assembled.json` | Claims, ledger, cmap, audit, anomalies (full assembled run state) |
| `state/id_map.txt` | Compact E/R/PAT id map |
| `raw/state/call_log` | Durable CAP call log (grammar-valid `CAP|…|cost=…` lines) |
| `tools/qmdj_toolkit.py` | Deterministic Tier-0/Tier-2 toolkit (extract → assemble → render) |
| `tools/case_context_input.json` | CAP-17 case decomposition rows (each with source sentence + tag) |
| `tools/interpretation.json` | Interpretive layer: I/C/A atoms, claims, CMAP, red team, hypotheses, slide guidance |

## Re-run

```bash
python3 tools/qmdj_toolkit.py extract    # CAP-01..CAP-11, CAP-17  (ingest once)
python3 tools/qmdj_toolkit.py assemble   # B0..B5, P6, RT + CAP-12..CAP-19
python3 tools/qmdj_toolkit.py render     # bounded renders + full report
```

Determinism: identical inputs yield identical structure, IDs and dispositions (law 2).
The chart source is never mutated and never re-read after the board card exists (laws 1–3, 44);
its sha256 is re-verified at each phase boundary (ANOMALY:SOURCE_CHANGED on drift).

## Validity boundary

Traditional interpretive analysis only — **not** factual prediction, **not** a substitute for
professional or academic judgment. The DECLARED unknowns (brand identity from Assignments 1–2,
real keyword volumes, actual media pickup) are **not resolved anywhere** in this package (laws 51–53).

Run summary: 13 claims (all LIVE) · 7 hypotheses · 4 ranked scenarios · 26 CMAP rows ·
all 7 question facets covered (0 uncovered) · CAP-16 self-audit PASS · 0 anomalies ·
21/60 CAP call budget.
