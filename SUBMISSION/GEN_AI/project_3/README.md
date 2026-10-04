# QMDJ Chart Analyst — executed run (Assignment 3 case)

Implementation and execution of `PROMPT/qmdj_chart_analyst_charter.md` (v7.0) as the system prompt of a
deterministic, evidence-bound analysis run over one chart, sealed as a reviewable package.

## Inputs (the only three repo paths this run read)

| role | path | use |
|---|---|---|
| system prompt (charter) | `PROMPT/qmdj_chart_analyst_charter.md` | the analyst's identity, laws, capability layer, coverage protocol and output-package contract that govern everything below |
| chart | `QMDJ/GEN_AI/project_3.json` | the single immutable source (ingested once, never re-read; law 3/44). sha256 `20dc73a9…e8360a15`, 16266 B |
| `case_context` | `ASSIGNMENTS/GEN_AI/project_3.yaml` | decides *what matters* (facets, known facts, deferrals), never what is true (cc1). sha256 `5f641d01…bae39cc0`, 9122 B. A byte-identical copy is kept at `raw/case_context.case.yaml` so the seal covers it |

No other repository file was read.

## Headline results

- **Registers**: registry holds 117 E-atoms and 49 R-atoms; the ranked **spine is exactly 37 atoms = 18 structural E + 19 board-internal R** inside palaces {1, 4, 5}; the condition register adds 18 in-scope atoms and the pillar register 6, both tallied separately and never mixed into the spine.
- **Coverage**: **25/25 batches closed**, every atom dispositioned exactly once, run-level reconciliation balances (`186 palace memberships − 20 shared = 166 atoms`), anomaly log empty.
- **Deterministic checks**: all 25 printed phase claims re-derived from the frozen table and matched; 值符/值使 cross-checks consistent; **30 of 32 explicit markers confirmed by their computed rules**, 2 left visible as `EXPLICIT_UNCONFIRMED` (palace 3).
- **Claims**: 12 live bounded hypotheses, **0 confirmed**, 1 draft **rejected as CONFLICTS_WITH_KNOWN** and kept visible, 1 class **BLOCKED** (campaign window: no timeframe in the case), 31 legal alternative candidates carried as `not_rejected`.
- **Gates**: render gate **PASS** (121 checks, 0 failures); a 10-row gap report ships with the package; `QUESTION_OVERLOAD` raised (8 facets > 7) and handled by a declared deferral rather than by invention.
- **Seal**: `package/seal.json` hashes every shipped artifact (58 of them) plus both source fingerprints, and is itself byte-stable across identical re-runs.

## The audit pattern (how the run is built)

1. **ANCHOR** — fingerprint both sources, ingest once, write a board card that every later phase reads instead of the source.
2. **REGISTRY** — atomise into typed atoms with fixed-width ids; keep registers separate (structural / condition / relation / pillar); the 37-atom spine is defined by a stated rule, not by taste.
3. **COVER** — run the complete 25-batch protocol; every atom carries exactly one disposition; per-palace closure and run-level reconciliation both have to balance.
4. **RECONCILE** — explicit chart markers and computed rules meet in one table; neither overwrites the other; unconfirmed markers stay visible instead of being smoothed away.
5. **GATE** — every score and every claim line is computed by `tools/validate_package.py`, never in prose; the gate is allowed to fail.
6. **SEAL** — hash the shipped artifacts against the source fingerprints.
7. **REPORT THE GAPS** — null classes, blocked classes, deferred facets and verification gaps are output, not omissions.

## Folder map

```
config/     cold annexes the charter requires: frozen tables, schema adapter, pattern catalog,
            archetype rubric, coverage control, wiki corpus. Data and rules only — no findings.
tools/      tier0.py (Tier-0 toolchain: ingest, atomise, patterns, ledger, score card),
            validate_package.py (render gate: computes certainties and claim lines),
            render_package.py (assembles the 17-section package + reports + seal)
raw/        source fingerprints, board card, the case-context copy, call logs, anomaly and reissue logs
work/       tool outputs, the authored claims.json, resolved claims, cmap, validation
review/     red-team pack (RT rows + proposal log)
package/        sections/00…17 (schema-valid JSON), full_report.md, renders/brief_1…3, seal.json
```

## Reproduce

```bash
cd SUBMISSION/GEN_AI/project_3
python3 tools/tier0.py --chart ../../../QMDJ/GEN_AI/project_3.json \
                       --case raw/case_context.case.yaml \
                       --config config --raw raw --work work
python3 tools/validate_package.py      # render gate: must print PASS
python3 tools/render_package.py        # writes package/sections, package/full_report.md, package/seal.json
```

Verify the seal (any drift in a shipped artifact or in a source is detectable):

```bash
python3 - <<'PY'
import json, hashlib, os
s = json.load(open("package/seal.json")); bad = []
for path, h in s["artifacts"].items():
    d = hashlib.sha256(open(os.path.join(".", path), "rb").read()).hexdigest()
    if d != h: bad.append(path)
print("drift:", bad or "none", "| artifacts:", s["artifact_count"], "| gate:", s["render_gate"])
PY
```

Same inputs and same frozen artifact set produce byte-identical ids, tallies and dispositions.

## What this run cannot do

- It is analysis only: tradition-conditional interpretation, **not factual prediction**, and never a substitute for professional judgment.
- It cannot supply, confirm or strengthen Assignment-1 evidence. Every directive in `package/renders/` carries a `trace_slot`; the chart side of that slot must still be filled from the research summary, the insight list or a mood-board pin (the draft that tried to let the chart pick the brand name was rejected on exactly this ground — see claim `C013` and `CONK004`).
- Product facts (format, variants, size, price band), audience, channel and budget are outside its jurisdiction; those rows are `NO_CHART_SUPPORT` and the gap report says so.
- The printed board is read, not re-derived: the hourly rotation from the hour pillar was not independently recomputed (`GAP-007`).

## Notes

- `runtime_mode = TOOLS_PRESENT`: the Tier-0 capability names are bound to real local programs shipped in `tools/`, so there are **no EMULATED products** and no model-computed scores (every score line carries `SCORE_SOURCE=TIER2_TOOL`).
- Cap budget used: 27 of 60 calls (15 toolchain, 5 render gate, 7 render).
- `ASSIGNMENTS/GEN_AI/project_3.yaml` is read, copied into `raw/` and hashed; nothing in the repository was modified or deleted outside this folder.
