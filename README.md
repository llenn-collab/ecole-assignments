# Assignment Solver Vault

Closed-world pipeline: a brief in `ASSIGNMENTS/`, a chart in `QMDJ/`, a solver spec in `PROMPT/`, a hand-in in `SUBMISSION/`.

Humans read this file. Agents read [`AGENT.md`](AGENT.md) first, then [`PROMPT/prompt.yaml`](PROMPT/prompt.yaml).

| You are… | Start here |
|---|---|
| Person dropping a brief | [Quick start](#quick-start) |
| Person reviewing a pack | [`SUBMISSION/`](#submission-what-you-hand-in) |
| Agent / orchestrator | [`AGENT.md`](AGENT.md) |

The solver does not chat, does not ask clarifying questions, and does not put chart jargon in the files you submit.

---

## What this repo is

Each project is a pair:

1. **Brief** — what the marker actually asked for (`ASSIGNMENTS/{track}/{slug}.md` or `.pdf`).
2. **Chart** — `QMDJ/{track}/{slug}.json`, treated as authority for *answers / hidden problems / best path* when those fields exist; otherwise as computed then inferred evidence, never as fake explicit text.

The agent reads both, keeps a durable evidence trail under `WORK/`, and writes:

- **LAYER_B** — clean English artefacts for the marker/client (the hand-in).
- **LAYER_A** — audit face: ordinary-English situation notes plus operator mappings.

Logo artwork is excluded unless the brief requires a non-artwork stand-in (naming, colour intent, written direction).

---

## Repository layout

```
.
├── README.md                 ← humans (this file)
├── AGENT.md                  ← agents: paths, pairing, git, definition of done
├── .gitignore                ← ships here: keeps WORK/** and editor noise out of git
├── PROMPT/
│   ├── prompt.yaml           ← full solver law (phases, batches, QMDJ geometry)
│   └── forbidden_terms.txt   ← LAYER_B linter denylist (seeded from prompt.yaml; commit any extension)
├── ASSIGNMENTS/
│   └── {track}/{slug}.md     ← brief (.pdf also valid)
├── QMDJ/
│   └── {track}/{slug}.json   ← chart; 1:1 with the brief
├── WORK/                     ← generated scratch; not the hand-in (gitignored by default)
│   └── {track}/{slug}/
│       ├── raw/              ← extracts, traces, dumps
│       ├── wiki/             ← structured cards / articles
│       └── state/            ← machine.json, solution.json, indexes, …
└── SUBMISSION/
    └── {track}/{slug}/
        ├── MANIFEST.md
        ├── LAYER_B/          ← hand-in pack
        └── LAYER_A/          ← audit
            ├── ANNOTATED/    ← ordinary English situation
            └── OPERATOR/     ← COMMENTS.md, MAPPINGS.md, PATH_RANK.md
```

`WORK/` keeps traces off the zip you send a marker. It is created at run time and is gitignored — a fresh clone will not show it. If you must keep only four top-level domain folders, use `SUBMISSION/{track}/{slug}/_work/` with the same three subfolders and gitignore it.

### What the repo holds today

```
PROMPT/prompt.yaml                            ← solver spec
PROMPT/forbidden_terms.txt                    ← 60-term denylist, seeded from prompt.yaml
ASSIGNMENTS/PORTFOLIO/project_1.md            ← brief: "You On A Shelf"
QMDJ/PORTFOLIO/project_1.json                 ← its 1:1 chart
SUBMISSION/PORTFOLIO/project_1/
├── MANIFEST.md                               ← registry, sha256s, requirement coverage
├── LAYER_B/LAYER_B_SUBMISSION.md             ← the GRIT hand-in (lint-clean)
└── LAYER_A/LAYER_A_TECHNICAL_AUDIT.md        ← full audit trail
```

### Pairing rule

One project = `(track, slug)`.

| Role | Path |
|---|---|
| Brief | `ASSIGNMENTS/PORTFOLIO/project_1.md` |
| Chart | `QMDJ/PORTFOLIO/project_1.json` |
| Scratch | `WORK/PORTFOLIO/project_1/` |
| Hand-in | `SUBMISSION/PORTFOLIO/project_1/` |

Slug = filename without extension. Track = parent folder. Do not flatten tracks. Case-insensitive match (`PROJECT_1` ≡ `project_1`); the spelling under `ASSIGNMENTS/` wins for the submission folder.

Legacy flat drops are accepted on read but no longer exist in this repo (migrated 2026-09-13):

| Old | Canonical |
|---|---|
| `SUBMISSION/PORTFOLIO/PROJECT_1/LAYER_B_SUBMISSION.md` | `SUBMISSION/PORTFOLIO/project_1/LAYER_B/LAYER_B_SUBMISSION.md` |
| `SUBMISSION/PORTFOLIO/PROJECT_1/LAYER_A_TECHNICAL_AUDIT.md` | `SUBMISSION/PORTFOLIO/project_1/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md` |

If the brief asks for one document, write `LAYER_B/LAYER_B_SUBMISSION.md` and `LAYER_A/LAYER_A_TECHNICAL_AUDIT.md`. Do not invent a numbered 00–07 pack when the brief already names the artefacts.

---

## Precedence

| Rank | Source | Owns |
|---|---|---|
| 1 | `AGENT.md` | Paths, pairing, naming, git, done |
| 2 | `PROMPT/prompt.yaml` | Laws, Phase 0–6, batches B1–B5, geometry, gates |
| 3 | `ASSIGNMENTS/**` | Due artefacts, hard constraints, logo boundary, audience |
| 4 | `QMDJ/**` | Explicit slots first; else COMPUTED (with JSON paths) then INFERRED |

Brief hard constraints win over a chart “nice to have”. A missing required artefact is a fail even if the chart looks favourable.

`ASSIGNMENTS/`, `QMDJ/`, and `PROMPT/prompt.yaml` are immutable at runtime. Hashes go into `WORK/…/state/machine.json`.

---

## Quick start

### New project

1. Add the brief:

   ASSIGNMENTS/PORTFOLIO/project_2.md

2. Add the matching chart:

   QMDJ/PORTFOLIO/project_2.json

3. Tell the agent:

   Run AGENT.md on PORTFOLIO/project_2

The agent creates `WORK/PORTFOLIO/project_2/` and `SUBMISSION/PORTFOLIO/project_2/`, runs the loop, writes `MANIFEST.md`, and stops.

### Redo batch 1

Redo B1 on PORTFOLIO/project_2

Purges B1 traces/verdicts, then re-runs B1 from scratch.

### Resume

If `WORK/{track}/{slug}/state/machine.json` exists, the agent resumes unless you asked for a B1 redo.

---

## Submission: what you hand in

Ship **`SUBMISSION/{track}/{slug}/LAYER_B/`** plus **`MANIFEST.md`**.

| Tree | Who reads it | Chart jargon | What it is |
|---|---|---|---|
| `LAYER_B/` | Marker / client | Forbidden | Exactly the artefacts the brief asked for (minus excluded logo artwork) |
| `LAYER_A/ANNOTATED/` | You, in English | Forbidden | Same story as situation: risks, timing, constraints, `00_STATUS.md` |
| `LAYER_A/OPERATOR/` | You, technical | Allowed | `COMMENTS.md`, `MAPPINGS.md`, `PATH_RANK.md` — paragraph → requirement id, palace, batch, JSON path |
| `WORK/` | Nobody external | Allowed | Evidence trail. Not the hand-in. |

`PATH_RANK.md` never belongs in LAYER_B.

If the brief is silent on packaging, the agent may write a labelled fallback pack (`UNGROUNDED_PACK`) inside LAYER_B and say so only in OPERATOR. When the brief asks for one document, each layer is one markdown file (`LAYER_B_SUBMISSION.md`, `LAYER_A_TECHNICAL_AUDIT.md`) inside its folder — the seeded `project_1` pack uses that form; see its `MANIFEST.md`.

---

## Agent loop (summary)

```
INIT → CHART_INGEST → P0_ANATOMY → PDF_INGEST → PURGE_B1?
    → B1 → B2 → B3 → B4 → B5 → P6_BOARD_SYNTHESIS
    → SYNTHESIZE → AUDIT_FIX? → RENDER_OUTPUT → HALT
```

- **Phase 0** — bind the real JSON schema, four pillars, season, duty, reverse indexes, Jia origin set, centre lodging. Mandatory before B1.
- **B1–B4** — operator zoom order (day set + opposite, hour set + opposite, day traces, hour traces). Selectors return **sets**, not a guessed single palace.
- **B5** — remaining palaces plus confirm/veto.
- **Phase 6** — whole-board maps and patterns, then freeze.

Centre has no directional opposite. Lodging is a graph. The JSON plate is the board: the solver does not rebuild a remembered chart structure. Unknown keys are stored, not dropped.

Full tables, Jia protocol, palace stack S1–S12, and interpretation classes live in `PROMPT/prompt.yaml`. Do not copy them into this README.

---

## Definition of done

A project is done when all of these hold:

- Pair resolved; sources hashed; `machine.json` state is `HALT`
- Phase 0, B1–B5, and Phase 6 completed (or anomalies logged under partial-chart policy)
- `solution.json` frozen; no live claim still supported by `VETO` evidence
- LAYER_B covers the deliverable registry except excluded logo artwork
- LAYER_B passes the forbidden-term linter (`PROMPT/forbidden_terms.txt`)
- LAYER_A ANNOTATED includes `00_STATUS.md`
- LAYER_A OPERATOR includes COMMENTS, MAPPINGS, and PATH_RANK
- `MANIFEST.md` lists path, sha256, requirement ids, deliverable id, tree
- Overloaded palaces are split claims, not averaged into one score

Empty brief or empty chart → `LAYER_A/OPERATOR/FAILURE.md`, no questions, no invented stems.

---

## Naming

| Thing | Convention |
|---|---|
| Track folders | Keep the committed spelling (`PORTFOLIO`). New tracks: one token, match existing style |
| Slugs | `lower_snake` (`project_1`) |
| Submission folder | Same spelling as `ASSIGNMENTS/` |
| Encoding | UTF-8, NFC. Do not rewrite Chinese filenames |

One palace → one wiki card → one trace file under `WORK/…/raw/traces/`. Machine JSON is primary; markdown is a view.

---

## Git

**Commit**

- `README.md`, `AGENT.md`
- `PROMPT/`
- `ASSIGNMENTS/`
- `QMDJ/`
- `SUBMISSION/**/LAYER_B/`
- `SUBMISSION/**/MANIFEST.md`
- `SUBMISSION/**/LAYER_A/` if you want the audit in-repo

**Do not commit** (unless you have a reason)

- `WORK/**` dumps and extracted binary logo images
- Local noise (`.DS_Store`, `__pycache__/`)

The repo ships `.gitignore` with:

```gitignore
WORK/**
**/.DS_Store
**/__pycache__/
```

Default: ignore all of `WORK/`. Keep `WORK/**/state/machine.json` only if you need resume across machines (add an explicit `!` line). Extend the file if needed; do not weaken it.

---

## Operator commands

| Intent | Say |
|---|---|
| Run one project | `Run AGENT.md on PORTFOLIO/project_2` |
| Redo day-stem batch | `Redo B1 on PORTFOLIO/project_2` |
| Resume | (say nothing extra if `machine.json` exists) |

Do not ask the agent to “just invent the missing hour stem” or to put palace names in LAYER_B. Those are hard fails.

---

## What this is not

- Not a chat bot for the brief
- Not a fortune-telling lecture in the hand-in
- Not a fixed 00–07 template that overrides the brief
- Not a place to rebuild charts from textbook memory
- Not a web-research agent (live facts only if the brief demands them *and* the chart is silent; label `EXTERNAL`)

If the chart has no explicit answer / hidden-problem / best-solution fields, LAYER_B decisions are computed or inferred. Least-contradicted choices are labelled in OPERATOR only — never presented as a chart verdict.

---

## File map for agents

`PROMPT/prompt.yaml` still talks about `vault/raw/…`. Translate using [`AGENT.md` §4](AGENT.md). Short form:

| Spec path | Repo path |
|---|---|
| `vault/raw/Assignment.pdf` | `ASSIGNMENTS/{track}/{slug}.*` |
| `vault/raw/QMDJ.json` | `QMDJ/{track}/{slug}.json` |
| `vault/raw/state/*` | `WORK/{track}/{slug}/state/` |
| `vault/wiki/*` | `WORK/{track}/{slug}/wiki/` |
| `vault/output/SUBMISSION/` | `SUBMISSION/{track}/{slug}/LAYER_B/` |
| `vault/output/ANNOTATED/` | `SUBMISSION/{track}/{slug}/LAYER_A/ANNOTATED/` |
| `vault/output/OPERATOR/` | `SUBMISSION/{track}/{slug}/LAYER_A/OPERATOR/` |
