# Advertising project 2 — final campaign and supporting analysis

## Final campaign: THIS SEAT HAS A HEAD.

The selected cause is adult pillion helmet use. Start with:

- **`SUBMISSION/CAMPAIGN_PRESENTATION.pdf`** — 19-slide presentation.
- **`SUBMISSION/CAMPAIGN_PRESENTATION.pptx`** — editable presentation.
- **`SUBMISSION/CAMPAIGN_REPORT.pdf`** — six-page strategy, research and execution document.
- **`SUBMISSION/index.html`** — browser handoff with links to the deck, artwork and motion prototype.
- **`PROJECT_2_SUBMISSION.zip`** — professional submission files together.
- **`MANIFEST.md`** — delivery inventory, checksums and limitations.

Artwork includes a finished A6 hero card, A3 supporting poster, vertical social execution and illustrated stationary-placement mockup. The public submission is separated from `ANNOTATED`, `LAYER_A` and `OPERATOR` records. The campaign is complete as a design proposal, **not deployed or audience-tested**, and formal charter validation is not claimed.

To rebuild generated design files, use a local virtual environment with `OPERATOR/requirements.txt`, then run `OPERATOR/build_deliverables.py` and `OPERATOR/finalize_package.py`. These renderers are not CAP-tool replacements. Running the older root `run.py` only regenerates the historical blocked preflight.


## Main deliverable

Read **`CHART_CASE_ANALYSIS.md`** for the bounded analysis of the supplied chart in relation to the advertising assignment. It discusses all nine palaces, separates chart text from advisory applications, and provides three provisional media-development directions. No empirical cause data or campaign-effectiveness claims are invented. Formal CAP execution remains blocked as documented below. Running `run.py` regenerates only the earlier preflight JSON artifacts; it does not generate or validate the interpretive report.

## Authorized scope

Only these repository input files are accessed:

- `QMDJ/ADVERTISING/project_2.json` — immutable QMDJ chart.
- `ASSIGNMENTS/ADVERTISING/project_2.yaml` — assignment brief supplied as `case_context`.
- `PROMPT/qmdj_chart_analyst_charter.md` — execution system prompt, preserved verbatim.

All work and generated outputs are confined to this submission directory. No other repository inputs were inspected, including the second charter mentioned in the system prompt.

## Run

From this directory:

```sh
python3 run.py
```

The runner uses only Python's standard library. It reads each authorized source once per invocation, records byte lengths and SHA-256 checksums, and writes deterministic preflight artifacts. It does **not** call an external model or implement substitutes for the charter's tools.

## Output roles

- `execution_request.json`: prepared system/user messages. The system message is exactly the supplied charter; the user message contains the chart and raw YAML case context. This request has **not** been submitted to a model.
- `B0_COVERAGE_CONTRACT.json`: known contract requirements and explicitly unresolved requirements; validation does not pass.
- `analysis_package.json`: all 17 requested output sections, with explicit blocked states, uncomputed values, palace coverage placeholders, provenance, and a mandatory gap report. It is a preflight package, not a completed analysis.
- `REPORT.md`: readable status, brief requirements, and dependency handoff.

## Execution boundary

Shell tools are available, so runtime mode is `TOOLS_PRESENT`. The charter requires actual CAP and Tier tool bindings in this mode and prohibits their emulation. Those bindings have not been supplied. Its pattern, archetype, and coverage annexes are placeholders. Other required reference artifacts have not been supplied or authorized.

B0 therefore cannot pass. B1–B5, P6, RT, and Tier2 have not run. No evidence atoms, claims, symbolic verdicts, scores, or campaign recommendations are fabricated. Empty output arrays mean no products were emitted, not that the underlying chart lacks evidence. Unknown counts are `null`, not zero.

Before proceeding, the user must identify the roles, purpose, and use of the required dependency files/tools and authorize their access. This runner does not search for them.
