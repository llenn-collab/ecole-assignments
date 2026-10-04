# Assignment 3 — executed by Carpathia Assignment Solver v7.0.0

**The assignment.** Three interconnected briefs for a new premium ready-to-drink coffee brand — Brand Idea &
Philosophy, Product & Packaging, and Ad / Campaign Creative Brief — plus the coherence check and the deliverable &
submission rules.

**The brand produced.** *AURA Cold Extraction* — cold-extracted coffee kept cold from press to hand, with one
provable idea: freshness is a temperature, not a claim. One can, two variants, a pack whose unprinted aluminium
band frosts in the cold case, and a campaign line: **Take It Slow.**

**Where to read it.**

| Start here | For |
|---|---|
| `SUBMISSION/00_cover_and_index.md` | what the package is and where everything lives |
| `SUBMISSION/01…03_*.md` | the three briefs themselves (the deliverable) |
| `SUBMISSION/04_coherence_check.md` | how the three briefs hold together, decision by decision |
| `SUBMISSION/05…09_*.md` | logline · mood-board index · production & AI workflow · risks · research index |
| `ANNOTATED/` | the same briefs with the reasoning, the exact evidence and the response map |
| `LAYER_A/` | plain-English walkthrough, candidate scoring, confidence, then the technical appendix |
| `OPERATOR/` | the machine record: state, ledgers, gates, veto, gap register, lint, red team, call log |
| `MANIFEST.md` | every artefact with its sha256, the input hashes, and the gates' results |

**Inputs, all read-only.**

- `ASSIGNMENTS/GEN_AI/project_3.yaml` — the assignment brief (34 obligations: 24 required, 4 prohibitions, 6 should-level)
- `ASSIGNMENTS/GEN_AI/project_3_research.yaml` — the Assignment-1 research the brief requires (74 indexed references)
- `SUBMISSION/GEN_AI/project_3/` — the sealed chart-analysis package from the previous run (consumed read-only; the raw chart source was never opened)

**Final result.**

- Direction selected: **Guarded Pact** (requirement fit 0.9328) over four alternatives; one direction vetoed for
  inventing an audience the research does not support and kept visible rather than deleted.
- Coverage gate **PASS** — 0 required facets unanswered, 0 blocked, 0 prohibitions violated, 0 unsupported
  required formats, with 2 input prerequisites declared as substituted rather than invented (the insight list
  and the live mood board, neither of which was supplied).
- Forbidden-output lint **CLEAN** over all plain-English scopes (framework vocabulary and ids confined to the
  annotated and operator layers).
- Layer-A contract **PASS** — plain English first, operator appendix appended verbatim and hash-verified.
- Manifest covers 56 artefacts plus itself; two full chain re-runs reproduce identical digests.

**Declared gaps (nothing invented to hide them).** The live Pinterest board / insight list were not supplied: the
board index is reconstructed from the research pack's own art-direction codes and flagged row by row; the insight
material is taken from the research pack's psychographic and gap sections; the packaged-artwork exclusion is
honoured as written direction only.

**Reproduce.**

```bash
cd SUBMISSION/GEN_AI/project_3_solution/tools
python3 requirements.py     # decompose the brief, index the research
python3 adapter.py          # adapt the sealed analysis package
python3 solve.py            # bindings, ledgers, scoring, gates
python3 render.py           # submission (10 files) + annotated (5 files)
python3 finalize.py         # operator pack, layer A, lint, manifest
```
