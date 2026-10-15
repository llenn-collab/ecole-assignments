# AGENTS.md — Repository Instructions

## Purpose

This repository is an assignment-to-submission workflow. For each project, pair the original brief in `ASSIGNMENTS/` with its matching QMDJ chart in `QMDJ/`, preserve an auditable evidence trail, and produce the requested hand-in under `SUBMISSION/`.

## Read First

Before doing project work, read these files in order:

1. `AGENT.md` — operational rules for paths, project pairing, Git, and completion.
2. `PROMPT/prompt.yaml` — authoritative solver specification, phases, batch rules, chart geometry, and validation gates.
3. `PROMPT/forbidden_terms.txt` — terms prohibited in marker/client-facing `LAYER_B` content.
4. The target brief in `ASSIGNMENTS/{track}/{slug}.md` (PDF briefs are also valid).
5. The matching chart in `QMDJ/{track}/{slug}.json`.

If a file referenced above is missing, do not invent its contents. Record the missing input and follow the failure policy in the repository instructions.

## Source-of-Truth and Precedence

Use this precedence order:

1. `AGENT.md`: repository paths, pairing, naming, Git, and definition of done.
2. `PROMPT/prompt.yaml`: solver phases, procedures, chart interpretation, and gates.
3. `ASSIGNMENTS/**`: required deliverables, audience, constraints, and exclusions.
4. `QMDJ/**`: chart evidence.

Brief requirements take precedence over chart preferences. Treat explicit chart fields as authoritative only where present. Otherwise distinguish computed evidence from inference, preserve the relevant JSON paths, and never present an inference as an explicit chart verdict.

Treat `ASSIGNMENTS/`, `QMDJ/`, and `PROMPT/prompt.yaml` as immutable inputs during a run. Do not silently rewrite briefs, charts, or solver rules to make a result pass.

## Project Pairing and Paths

A project is identified by `(track, slug)`:

- Brief: `ASSIGNMENTS/{track}/{slug}.md` or `.pdf`
- Chart: `QMDJ/{track}/{slug}.json`
- Scratch/evidence: `WORK/{track}/{slug}/`
- Hand-in: `SUBMISSION/{track}/{slug}/`

Keep track folders intact; do not flatten the directory structure. Match the brief and chart by track and slug, case-insensitively; use the spelling from `ASSIGNMENTS/` for the submission folder. New slugs should use `lower_snake_case`. Preserve UTF-8/NFC and do not rename Chinese filenames.

Do not assume every brief asks for a fixed set of documents. Produce the artefacts the brief actually requests. For a brief asking for one document, use the established single-document structure:

- `SUBMISSION/{track}/{slug}/LAYER_B/LAYER_B_SUBMISSION.md`
- `SUBMISSION/{track}/{slug}/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md`

## Output Boundaries

- `LAYER_B/`: only the clean artefacts requested by the brief, written for the marker/client. Do not expose chart jargon, operator mappings, or audit notes here. Do not include logo artwork unless the brief requires a non-artwork stand-in such as naming, colour intent, or written direction.
- `LAYER_A/ANNOTATED/`: ordinary-English situation and status notes, including `00_STATUS.md`.
- `LAYER_A/OPERATOR/`: technical audit material, including `COMMENTS.md`, `MAPPINGS.md`, and `PATH_RANK.md`, as applicable.
- `MANIFEST.md`: registry of output paths, SHA-256 hashes, requirement coverage, deliverable IDs, and tree/layer.
- `WORK/{track}/{slug}/`: generated traces, extracts, wiki cards, indexes, and machine state. This is scratch/evidence, not the hand-in.

Never place `PATH_RANK.md` in `LAYER_B/`. If the brief does not specify a packaging format, any fallback pack must be clearly labelled `UNGROUNDED_PACK` and explained in the operator audit.

## Solver Workflow

Follow the phase and batch order in `PROMPT/prompt.yaml` and `AGENT.md`; do not skip gates or substitute an improvised workflow. The documented loop is:

`INIT → CHART_INGEST → P0_ANATOMY → PDF_INGEST → B1 → B2 → B3 → B4 → B5 → P6_BOARD_SYNTHESIS → SYNTHESIZE → AUDIT_FIX? → RENDER_OUTPUT → HALT`

Honor resume state in `WORK/{track}/{slug}/state/machine.json`. Resume an existing run unless explicitly instructed to redo B1. A B1 redo must purge the relevant B1 traces/verdicts and rerun that batch according to the specification.

Preserve unknown chart keys; do not rebuild the chart from remembered textbook structures. Treat selectors as sets where the specification requires it. Do not invent missing stems, chart fields, evidence, or deliverables. If the brief or chart is empty, follow the documented failure policy and write `LAYER_A/OPERATOR/FAILURE.md`; do not ask follow-up questions or fabricate inputs.

## Validation and Definition of Done

Do not report a project complete until all applicable checks pass:

- Project pairing is resolved and input sources are hashed.
- `WORK/{track}/{slug}/state/machine.json` reaches `HALT`.
- Phase 0, batches B1–B5, and Phase 6 are complete, or anomalies are documented under the partial-chart policy.
- `solution.json` is frozen and no live claim remains supported by `VETO` evidence.
- `LAYER_B` covers the deliverable registry, except for explicitly excluded logo artwork.
- `LAYER_B` passes the forbidden-term linter using `PROMPT/forbidden_terms.txt`.
- `LAYER_A/ANNOTATED/00_STATUS.md` exists.
- `LAYER_A/OPERATOR/` contains `COMMENTS.md`, `MAPPINGS.md`, and `PATH_RANK.md`, as required by the workflow.
- `MANIFEST.md` records output paths, SHA-256 hashes, requirement IDs, deliverable IDs, and tree/layer.
- Overloaded palaces are represented as split claims rather than averaged into one score.

Label evidence as explicit, computed, inferred, or external as appropriate. External research is out of scope unless the brief requires current facts and the chart is silent; label such evidence `EXTERNAL`. A least-contradicted option is an operator assessment, not a chart verdict, and must not be represented as one in `LAYER_B`.

## Git and Repository Hygiene

Commit source briefs, charts, solver instructions, and intended submission artefacts. Do not commit generated `WORK/**` dumps, extracted binary logo images, editor noise, or local caches unless there is an explicit reason and the repository's ignore rules are adjusted deliberately.

Respect `.gitignore`; do not weaken ignore rules casually. Keep generated scratch separate from hand-in files. Make focused changes and avoid unrelated formatting or renaming.

## Interaction and Reporting

The workflow is not a conversational brief assistant: do not ask clarifying questions during a run. Use available inputs, document uncertainty and anomalies, and stop according to the specified failure policy. Report the project path, outputs created, validation results, and any unresolved blockers concisely.
