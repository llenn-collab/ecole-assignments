# Plan — Cutting `chart_analyser.yaml` from 1M–3M tokens to ≤7k per call (≤45k uncached) without losing accuracy

**Status:** planning only. No prompt has been changed yet.
**Scope:** `PROMPT/chart_analyser.yaml` (v5.0.0). Downstream `assignment_solver.yaml` is untouched by Phases 0–4, and gets the same treatment in Phase 6.
**Date:** 2026-09-18

---

## 0. Decisions locked

| # | Decision | Status |
|---|---|---|
| 1 | Tier 0 (inventory, parsing, indexing, pattern computation) is **real Python** at `tools/chartc/` | ✅ Locked |
| 2 | Wiki/Markdown layer is **kept, but generated from JSON** — never model-authored | ✅ Locked |
| 3 | Contract break (§9.1) fixed as **Phase 0a, on the critical path** | ✅ Locked — see §9.1 |
| 4 | Reconciled with the cumulative audit A-01…A-23 (§12): **18 adopt, 2 adopt-amended, 1 defer, 1 reject** | ✅ Locked |
| 5 | Evidence addressing uses **stable IDs** (`E#`/`R#`/`I#`/`C#`/`A#`), superseding path aliases | ✅ Locked — A-07 supersedes §5 note 1 |
| 6 | B1–B5 become **specified batch contracts**, not collapsed passes | ✅ Locked — A-12 supersedes the earlier 2-pass design |
| 7 | Tier-1 topology is **7 calls** — B1–B5 + P6 + blind red-team (supersedes the earlier 3-call sketch; C-07) | ✅ Locked — §5 diagram |
| 8 | Token target is **two-metric with per-call shapes** (C-36/C-38): hard ceiling ≤7k/call — B1–B5 ~3–4k, P6 ~5–6k, RT ~4–5k — and ≤35–45k cumulative uncached; ~30k is a caching-dependent stretch (C-10) | ✅ Locked — §2 |
| 9 | The legacy baseline is **telemetry, not an oracle**; golden packages carry adjudication status (C-01/C-02) | ✅ Locked — §7.1 |
| 10 | The Tier-1 charter carries **no deterministic tools** — emission only (C-13) | ✅ Locked — Phase 3b |
| 11 | Execution control is a **host-managed DAG** — the prompt carries zero `fsm_transition_table` logic (C-51) | ✅ Locked — §5 |
| 12 | **No unconditional "100% accuracy" claim anywhere** — determinism is reproducibility, not truth (C-58); the accuracy budget is the eight-zero contract (C-60) | ✅ Locked — §4, §7.3 |
| 13 | **The three non-negotiables** before implementation freeze: batch-scope completeness, controlled `MODEL_PROPOSAL` lane, candidate-set red-teaming (C-39/C-42/C-43) | ✅ Locked — §14.1 |

---

## 1. The one-sentence diagnosis

The chart is ~2,000 tokens. The spec is ~27,000 tokens. Everything else — the ~1M–3M — is **the model paying LLM prices to do table lookups, JSON traversal, and to re-read its own output back into context five times.**

Three-quarters of what `chart_analyser.yaml` mandates is deterministic work guarded by frozen tables (`palace_identity_table`, `opposition_by_name`, `star_home_luoshu`, `horse_branch`, `sanqi`, `liuyi`, `strength_scale`) and asserted byte-identical by its own regression harness. Work that must be byte-identical and is driven by frozen tables is **compiler work, not model work.** Today a stochastic model is doing it, 323 nodes at a time, and then re-reading the result.

---

## 2. Where the tokens actually go

### Measured (not estimated)

| Thing | Measured value |
|---|---|
| Source chart, `PORTFOLIO/project_1.json` | 323 nodes, 7.6 KB, **~2,054 tokens** |
| Source chart, `EDITORIAL` | 285 nodes, **~2,154 tokens** |
| Source chart, `ADVERTISING` | 314 nodes, **~2,035 tokens** |
| Source chart, `MARKETING` | 239 nodes, **~1,815 tokens** |
| `chart_analyser.yaml` spec | 99,874 chars, **~26,979 tokens** |
| `assignment_solver.yaml` spec | 89,990 chars, **~24,296 tokens** |

The input is 2k tokens. **The machine is spending 500×–1500× the size of its input.**

### Modelled output volume (assumptions stated)

| Mandated artefact | Driver from the spec | Est. tokens |
|---|---|---|
| `path_coverage_manifest.json` | 323 nodes × 14 `node_record_fields` ≈ 524 B/record | **~46,000** |
| Palace cards (JSON + Markdown view) | `max_palace_reads: 40` × (S1–S14 record + MD view) | **~81,000** |
| Wiki layer | 9 mandated articles × ~6 KB × ~8 rebuilds (per phase + per `AUDIT_FIX`) | **~117,000** |
| State JSON files | 15 files (pillars, season, duty, indexes, origin_sets, systems, relations, patterns, …) | **~16,000** |
| `chart_analysis_package.json` render | assembles all of the above | **~11,000** |
| Report + red team + heartbeats + audit logs | `update_frequency: after every palace, batch, phase, and coverage gate` | **~8,000** |
| **Total generated** | | **~280,000** |

Then the multipliers turn 280k into 1M–3M:

1. **Read-back.** `rag.retrieve_before_read: true` and the retrieval step pull the artefacts back into context. Generated once, paid for twice.
2. **Compaction thrash — the big one.** `rag.compaction_trigger.threshold: 10,000` tokens. But the `context_compaction_law` *mandates retaining* machine state, solution_seed, MOC, **path coverage manifest (46k)**, absence registry, indexes, origin sets, systems, patterns, archetype_resolutions. The retained set is **>100k tokens** against a **10k** threshold. The spec asks the model to compact below a floor that its own mandatory retention exceeds by 10×. It thrashes continuously, and every compaction re-emits the 27k spec (`repeat_at_top_of_context: true`) plus the retained set. 27k × ~30 compactions alone is **~800k tokens**.
3. **Duplication.** The same fact is written up to five times: state JSON → wiki MD → package → `Chart-Analysis-Report.md` → (downstream) `LAYER_A` appendix.

---

## 3. Five root causes

### RC-1 — Mechanical work assigned to the model
Recursive inventory (323 nodes), key/value whitespace normalisation, Ganzhi parsing, palace-key resolution, reverse indexes, geometry opposition, void/tomb/punishment/horse lookups, strength normalisation, `wangshuai_matrix`, and all 22 `pattern_catalog.compute_always` patterns are **set membership and table lookup**. Zero judgment. This is ~85% of the artefact volume.

### RC-2 — Context carries artefacts instead of facts
The 46k path coverage manifest lives in context permanently. But nothing downstream *reads* it — it only needs its **completion counts** and the ability to resolve a cited path. Proof-of-coverage is a boolean; the manifest is evidence for a boolean.

### RC-3 — Five sequential passes over the same nine palaces
`B1`–`B5` with `max_palace_reads: 40` means up to 40 executions of the S1–S14 stack. S1–S12 are deterministic. Only **S13 (typed verdicts)** needs a model — and verdicts don't require sequential ordering once every fact carries an `evidence_phase` stamp (which the tie-break rule already consumes as data).

### RC-4 — Markdown views re-authored rather than generated
`palace_card_shape.markdown_view_generated_from_json: true` and `push_pull_rule` already say the MD is a *generated view*. There is no generator, so the model re-writes each article — and the two copies drift. The downstream `G-LAYER-A-CONTRACT-SATISFIED` guard (appendix hash must match current operator output) exists **precisely because this drift already happens.**

### RC-5 — 27k of spec re-injected, of which ~20k is reference data
Frozen tables, JSON schemas, and tool schemas are ~20k of the 27k. They are needed by *code*, never by the model's reasoning. The model needs the ~25 laws, 5 grounding classes, 6 verdict polarities, and the output contract: **~3–4k tokens.**

### RC-6 — B1–B5 are referenced 30+ times and defined nowhere
The execution FSM says:

```yaml
B1:
  do:
    - "execute B1 from scratch"
B2:
  do:
    - "execute B2"
```

No definition of B1–B5 exists anywhere in the file. The only hints: `jia_protocol.if_day_gan_on_heaven: "B1 primary = those palaces"`, `rag.retrieval_step.pull: "origin sets for B1-B4"`, `P5_REMAINING.id: "B5"`. Meanwhile the post-batch audit at L1748 demands *"palaces selected match the batch rule as sets; prove with field values"* — **there is no batch rule**, so that gate is unverifiable by construction.

Consequences: the model invents a batch definition on every run (non-deterministic by design), and `byte_identical_target: true` is unachievable for anything downstream of B1. This is why A-12 is not merely an optimisation.

---

## 4. The core idea: deterministic floor + model ceiling

Split the pipeline by *epistemic type*, not by phase.

- **Deterministic floor** — anything byte-identical and table-driven. Runs as code. **Costs 0 tokens.** Determinism eliminates *stochastic execution drift* — it is reproducibility, not truth; semantic correctness stays governed by validated rules, fixtures, adjudication, and regression gates (§7.2, C-58).
- **Model ceiling** — only interpretive judgment on non-boilerplate content. Runs on a compressed digest. **Small.**

The spec already demands this split. `meta.determinism_policy.byte_identical_target: true` is a claim that the work is deterministic. We are not changing a law — we are finally enforcing one.

Critically, this is **not** an accuracy trade-off. On the mechanical slice, code is strictly more accurate than a model asked to enumerate 323 nodes from memory. The mechanical slice is also where today's silent accuracy loss concentrates (see §9).

---

## 5. Target architecture

```
tools/chartc/                        ← TIER 0, deterministic, 0 model tokens
  QMDJ/{track}/project_1.json
      ├─ traverse · normalise keys/values · detect variant · bind semantic roles
      ├─ parse stems/ganzhi/strength/composite strings · resolve palace keys
      ├─ build reverse indexes · origin sets · lodging graph · dependency graph
      ├─ compute relations · wangshuai matrix · all 22 compute_always patterns
      ├─ seed claims/candidates from ALL protocol classes, not just the catalog (C-41)
      └─ emit: state/*.json · board_digest.md · evidence_registry.json · anomaly_registry.json · gates.json

TIER 1 — chart_analysis core          ← model, 7 calls, per-batch scoped digests,
                                         controlled PROPOSAL lane (C-42)
  B1  origin / day-stem            in: digest[B1]           out: typed claims (compact lines)
  B2  hour focus / execution       in: digest[B2]           out: typed claims
  B3  forward / backward traces    in: digest[B3]           out: typed claims
  B4  opposition · void · tomb ·
      punishment · risk            in: digest[B4]           out: typed claims
  B5  residual coverage            in: digest[B5]           out: typed claims
  P6  board adjudication           in: claim graph +
                                       candidate seeds      out: candidate adjudication —
                                       prefer / reject / unresolved (C-46);
                                       the BUILDER resolves + scores, never the model
  RT  blind red-team on the        in: evidence graph +
      CANDIDATE SET (C-43)           full candidate set +     out: SUPPORT / VETO /
                                       candidate E-IDs         SPLIT_PROPOSED (C-45)
                                       (NO original rationale)  RT-1 contradict selected ·
                                                               RT-2 rejected better? ·
                                                               RT-3 candidate missing?
                                       → 3d′ deterministic re-resolution if material

tools/chartc/build_package.py         ← TIER 2, deterministic, 0 model tokens —
                                       a compiler, not a second analyst (C-63)
  state + verdicts + archetypes + redteam
      ├─ expand compact line-notation → full JSON
      ├─ resolve E-IDs → registry entries (raw value + leaf path)   (citation_leaf_integrity gate)
      ├─ deterministic resolution: statuses · vetoes · splits · ties (C-46)
      ├─ compute rubric scores, corroboration, contradiction penalty   ← model never does arithmetic
      ├─ serialize failure states as package-valid objects (C-47/C-48)
      └─ emit: chart_analysis_package.json (SHARED SCHEMA) + wiki/*.md (generated views)
```

**Orchestration (C-51): a host-managed DAG, not an LLM FSM.** Tier 0 and Tier 2 are Python; they cannot be autonomously driven from inside a prompt loop. A host DAG (`tools/chartc/pipeline.py`) executes Tier 0 → B1–B5 (parallelisable where scope-safe) → P6 → deterministic resolution/scoring → RT → conditional re-resolution → Tier 2. The prompt carries **zero** `fsm_transition_table` logic — the model is not the operating system. *Unverified execution assumption:* this requires the host runtime to orchestrate external calls; confirmed or worked around before Phase 1.

### The board digest — the key artefact

The model sees *resolved facts*, not traversal. Each fact carries its `E###` ID; the raw value, normalized value, semantic role, and source leaf path live in `evidence_registry.json` on disk (C-22). Raw paths appear only in anomaly/debug contexts.

A scoped digest is **content-bearing by requirement** (C-37): every in-scope `E`-ID inlines its normalized value, semantic role, grounding, relevant relation summaries, and anomaly/absence flags. An ID list is not a digest — if the model cannot judge from it, it is not complete.

```
CHART PORTFOLIO/project_1.json sha=ab12cd… variant=standard_qmdj_metadata_v1(conf=1.0)
PILLARS y=Bing-Wu m=Ding-You d=Bing-Xu h=Jia-Wu | void[day]=Wu,Wei void[hour]=Chen,Si
SEASON  metal:prosperous water:strengthening earth:resting fire:trapped wood:dead
DUTY    lead=Jia-Wu Xin star=TianYing@9 door=Jing@9 tianyi=Wagtail
REALM   inner={2,5,6,7,9} outer={1,3,4,8}
IDX     Bing→{E104} Xin→{E107,E121} Ding→{E118} …   (reverse index, E-referenced)

P1 Kan N Water outer str=strengthening
  hs=Bing(YangFire) star=TianXin[home=6] deity=WhiteTiger strP=prosperous strS=strengthening
  es=Xin(YinMetal) deity=SixHarmony hid=Ding(YinFire)
  door=Fear forced=F doorStr=prosperous
  tomb=[] punish=[] void=F horse=F
  op=P9(Li)
  HITS star_off_home(P1.hs) heaven_earth_pair(Bing/Xin fire>metal)(P1.hs,P1.es)
  EXPL (none)
```

~100 tokens per palace → **~1,000 tokens for all nine palaces**, ~3k with board header and anomaly list. Down from ~100k+ retained.

### Four compression tricks that pay for themselves

1. **Stable evidence IDs (adopted from A-07; supersedes path aliasing).** Every evidence atom, relation, interpretation, claim and candidate gets a short opaque ID:

   | Prefix | Object | Example |
   |---|---|---|
   | `E###` | evidence atom (a single leaf value or parsed composite atom) | `E104` = `palaces.1.heaven_plate.stem` = `"Yang Fire (Bing)"` |
   | `R###` | computed relation | `R07` = `Bing/Xin → fire controls metal` |
   | `I###` | interpretation (protocol-v2 class assignment) | `I12` = `heaven_earth_stem_pair` |
   | `C###` | typed claim / verdict | `C31` |
   | `A###` | archetype candidate | `A04` |

   The model cites `E104,R07`, never `chart_metadata.duty_elements.duty_door.active_palace` (~20 tokens → ~2). With hundreds of citations this is tens of thousands of tokens. **Why IDs beat path aliases:** they also cover board-level evidence (void branches, seasonal strengths, duty elements) and computed relations, which have no source path at all. The `E###` registry records `source_leaf_path` for every atom, so `citation_leaf_integrity` and law 28 (leaf-level citations) stay satisfiable — the ID is a pointer, not a substitute.

   **IDs are content-addressed, not traversal-order (C-21).** `E = hash(source identity + canonical leaf path + atom index)`; `R = hash(relation type + sorted E-IDs)`; `I`/`C`/`A` analogous (protocol class; claim type + target slot; archetype type + sorted `C`-IDs). Short display IDs derive deterministically from the hash, so upstream JSON re-ordering cannot renumber the evidence base. **Stability is version-scoped (C-56):** IDs hold within a given compiler version and ID-schema version; a parser or canonicalization change legitimately re-atomizes content and therefore reissues IDs. The package records `compiler_version`, `id_schema_hash`, and `contract_hash`, so an ID change across versions is explainable — never silent. And the **registry, not an alias table, is the source of truth (C-22):** `evidence_registry.json` (ID, source file, leaf path, raw value, normalized value, semantic role, grounding, parser status) replaces `path_alias_table.json` as the citation mechanism; the model rarely sees a raw path outside anomaly/debug context.

2. **Compact line-notation output.** The model emits `C31|P1|CONSTRAIN|MED|my_answers|ev=E104,E107,R07|note=Bing/Xin fire>metal` (~20 tokens) instead of a ~120-token JSON verdict. Tier 2 expands it. The notation is now load-bearing, so it gets a **strict grammar** (C-24): fixed field order, one validated regex per line type. Tier 2 validates every line on receipt; a malformed line is rejected and **that claim alone** is re-asked — a malformed claim never silently coerces into a score.

3. **The model never computes a score — and never discovers the phenomenon.** It supplies evidence ID lists and vocabulary-constrained labels. Tier 2 computes `grounding_tier`, `corroboration`, `contradiction_penalty`, `board_consistency`, `final_score`. This is what makes the existing golden assertion *"archetype_resolution winner + score must match golden baseline"* achievable — today the model both picks evidence **and** does the arithmetic, so the score can drift twice. Symmetrically (C-20/C-25): Tier 0 emits **claim and candidate seeds** — palace, class, slot bias, evidence IDs — from **all mechanically identifiable protocol classes** (C-41): the 22 `compute_always` patterns *plus* origin/day-stem/Jia-set, hour/focus, duty star/door, forward/backward traces, opposition, tomb/punishment/void, horse, original position, prosperity/decline, lodging, and yongshen classes — proven by a protocol-class coverage matrix, so the pattern catalog cannot become the epistemic horizon. The model judges what a detected phenomenon *means*, not whether it exists; it chooses among lawful seeds, and anything outside the taxonomy travels the **controlled `MODEL_PROPOSAL` lane** (C-42): `PROPOSAL|new_class|ev=E14,E27,R08|reason=…` — marked `PROPOSED`, never auto-live, checked against deterministic evidence-validity rules, admitted to adjudication only where protocol permits. The model chooses among lawful possibilities; it does not invent the law — and a closed world requires a controlled escape hatch, or the seeds become a silent ceiling. Scoring itself splits in two (C-26, §9.6): Prompt 1 scores grounding/corroboration/contradiction/board-consistency with **no** `requirement_fit` placeholder; Prompt 2 adds requirement fit. `evidence_phase` becomes provenance metadata, never a quality signal (C-29, §9.6).

4. **Deterministic evidence neighbourhoods instead of RAG (strengthens A-23).** The audit's concern is "bounded RAG fails if retrieval is bad." The right answer here is stronger than a fallback: **delete retrieval from this pipeline.** The entire evidence set derives from a ~2,000-token source; there is no corpus large enough to justify an index. Retrieval here is indexing 323 nodes so the model can search 323 nodes. Tier 0 emits static neighbourhood snapshots per batch question — `E`-ID sets, resolved at compile time. Every ID resolves by construction, so retrieval reliability stops being a risk at all.

### Token budget: before / after

| Slice | Today (est.) | Target | Method |
|---|---|---|---|
| Spec in context | ~800k (27k × ~30 compactions) | **~4k** | RC-5: charter vs. reference split; compaction effectively never fires |
| Structural inventory + coverage | ~46k | **0** | RC-1: Tier 0 |
| Palace cards ×40 reads | ~81k | **~24–31k in / ~5–6k out** (7 shaped calls) | RC-3: bounded batch queries on scoped digests (C-36) |
| Wiki layer | ~117k | **0** | RC-4 / Decision 2: generated by Tier 2 |
| State + package + report | ~35k | **0** | Tier 2 |
| Red team / audit | ~8k | **~12k** | *Increased deliberately* — this is where accuracy is defended |
| **Total** | **~1.0M–3.0M** | **per budget below** | **~30–60× reduction** |

**Two-metric budget (replaces the single "~30k" headline).** Per-call context and cumulative inference are different things; with 7 calls the charter and digest may be seen repeatedly unless the runtime caches a stable prefix. And a budget is not real until it names what counts (C-38): *input context* (charter + digest + tool results), *generation*, and a *hard context ceiling* — retries and prior turns included.

| Metric | Target | Notes |
|---|---|---|
| Hard context ceiling, any Tier-1 call | **≤ 7k tokens** | charter (~4k) + largest scoped digest; retries included |
| Cumulative **uncached** Tier-1 inference | **≤ 35–45k tokens** | 7 calls, no caching assumed |
| Stretch target | **~30k** | only if prompt caching / persistent session is real |
| Cached-prefix tax | **measured, not assumed** | if the runtime caches, charter+digest re-reads drop ~10× |

**Per-call shapes (C-36) — aggregation calls are not scoped calls.** B1–B5 receive scoped digests; P6 receives the claim graph + candidate seeds; RT receives the evidence graph + the candidate set. Planning estimates — validated in Phase 0, because claim-graph and neighbourhood sizes on complex charts may exceed them:

| Call | Input target | Output target |
|---|---:|---:|
| B1–B5 (each) | ~3–4k | ~500–800 |
| P6 board adjudication | ~5–6k | ~1–1.5k |
| RT blind red-team | ~4–5k | ~1k |

The "~30k" figure is therefore a *stretch* target conditional on caching, not the headline claim. The defensible unconditional claims are the per-call shapes above, the ≤7k hard ceiling, and ≤45k cumulative uncached.

---

## 6. What the model still does (and why accuracy doesn't drop)

Narrowed to the genuinely non-deterministic:

| Kept with the model | Why it can't be coded |
|---|---|
| Typed verdicts: polarity + confidence per palace | Judgment under ambiguity |
| **Overload splitting** (law 16) | Requires reading co-located opposite polarities as separate claims |
| Archetype candidate generation + `rejection_reason` + `margin_note` | Abductive; needs plain-English justification |
| Adversarial re-derivation (red team) | Its whole value is being a second, contrary viewpoint |
| `STILL_TIED` / split-claim decisions | Rubric-terminal; code flags, model justifies |

Everything else moves to code. Note the red-team pass is the one place the plan **increases** spend.

---

## 7. How "near 100%" is actually guaranteed

Be precise about what 100% can mean — and about what it cannot. Three separate accuracy contracts (C-03):

| Layer | Contract | Method | Ceiling |
|---|---|---|---|
| **Structural** | exact | deterministic: leaf-set equivalence, binding equivalence, coverage completeness | exactness is a binary, verifiable property — achievable, and *not* achieved today (LLM recall drift over 323 nodes) |
| **Computational** | exact against golden fixtures | deterministic: relation equivalence, pattern equivalence, rubric arithmetic | exact only if the rule tables are right — see §9.3 and §9.6 |
| **Interpretive** | adjudicated | diff discovery + expert review; no mechanical oracle exists | no numeric ceiling; governed by the accuracy budget (§7.3) |

### 7.1 The legacy baseline is not an oracle — it is telemetry (C-01/C-02)

This corrects an error in the earlier version of this plan, which proposed "parity with the current baseline" as the accuracy guarantee. **That is unsafe**, for three verified reasons:

- §9.3: the strength vocabulary is ~20% complete, with a case mismatch that misses *every* PORTFOLIO value.
- RC-6/§9.5: `B1`–`B5` are undefined, so `"execute B1 from scratch"` is improvisation by construction.
- `binding_failure_policy` explicitly instructs *"choose least-contradicted bind"* on 2 of 4 real charts (§9.2).

Parity with a stochastic run that was guessing is parity with a guess. Legacy outputs are therefore used for **telemetry and diff discovery only** — never as a pass/fail semantic gate. Golden packages must carry an explicit **adjudication status** (`UNREVIEWED` / `ADJUDICATED_ACCEPT` / `ADJUDICATED_CORRECT`), and a diff against legacy is a *question*, not a *failure*.

### 7.2 Determinism is not truth (C-15)

The earlier claim that "Phases 1–2 cannot regress accuracy" is **withdrawn**. Code removes *stochastic* risk; it does not confer semantic correctness. A parser can be deterministically wrong — §9.3's vocabulary table is exactly that failure mode today, and it is deterministic. Phase 1 therefore carries **semantic fixtures** (typed-atom equivalence, relation equivalence, pattern equivalence, anomaly-class parity), not merely node counts.

### 7.3 Accuracy budget (C-35)

Enforced by gates, not by intent:

```
0  silently dropped source atoms
0  unexplained semantic diffs vs. adjudicated goldens
0  uncited live claims
0  silently suppressed candidates
0  silent ties
0  accepted diffs without a recorded adjudication object (C-60)
0  model claims whose evidence neighbourhood was not Tier-0-generated (C-60)
1  deterministic final score for a given (source, compiler version, contract hash)
```

### The parity harness is the deliverable, not an afterthought

The spec's `regression_harness` already names the assertions. We make them executable and run them in **shadow mode**: old path and new path run side by side on all four real charts; packages are diffed.

| Existing assertion | Today | After |
|---|---|---|
| "run twice produces byte-identical package modulo `generated_at`/`run_id`" | Unverifiable (model output) | True by construction for Tier 0/2; constrained vocabulary for Tier 1 |
| "STRUCTURAL_INVENTORY outputs must account for every source path" | Self-reported | Code-checked against the node count |
| "origin_sets must be identical to golden baseline" | Model-derived | Code-derived, diffed |
| "archetype_resolution winner + score must match golden baseline" | Model computes both | Code computes score; model picks evidence |
| "no parent-only citations where leaf paths exist" | Self-reported | Alias resolver fails closed |

### Mechanical gates replace self-reporting
`path_coverage_manifest.complete`, `absence_registry.complete`, `leaf_unpacking_verified`, `explicit_patterns_ingested`, `citation_leaf_integrity`, `determinism_check` (run Tier 0 twice, diff), `rubric arithmetic`, `law_coverage` (every law ID maps to either a code check or a prompt clause). All become code. `law_coverage` is the guard against RC-5's risk of the model forgetting a rule it can no longer see.

### Layered comparison, not package-level diffing (C-33/C-34)

A final-package diff cannot localize a regression. The harness diffs at eleven layers:

`G0` raw source identity · `G1` normalized source · `G2` schema binding · `G3` evidence atoms · `G4` relations · `G5` patterns · `G6` batch evidence scopes · `G7` claim graph · `G8` candidate set · `G9` archetype resolution · `G10` final solution seed

A failure must be able to say *"the strength parser changed,"* not just *"the candidate changed."* Node-count equality is necessary but nearly vacuous: equivalence is asserted on raw leaf sets, typed atoms, semantic bindings, relations, patterns, and **anomaly classes** — counting leaves does not prove you understood the tree.

**Layer provenance (C-55):** `G0`–`G5` are legacy-diffable where legacy output is trustworthy; `G6`–`G10` are **fixture/adjudication-only** — B1–B5 evidence scopes and the new claim/candidate graph have no legacy semantics to diff against. You cannot diff what never existed; regression docs must not imply legacy parity for the new layers.

**Mutation testing (C-59):** gate sensitivity is proven, not assumed — inject known faults (swap palace IDs, remove a leaf, change a strength value, alter an opposition, flip a polarity, delete an evidence atom, change a schema path) and assert the *expected* G-layer fails each time. A gate that never fails is not a gate.

### Digest completeness is provable, not hoped for
`digest_coverage_gate`: for every inventoried leaf path, the digest must contain either the value or an explicit `unmapped`/`opaque` atom, with its `E`-ID resolvable in the registry. This is the existing `leaf_unpacking_verified` gate, checked by code instead of asserted in prose. The model never sees the 46k manifest; it sees a digest that is *provably* complete.

---

## 8. Phased roadmap

Each phase has an exit criterion. No phase starts before the previous one's exit is green.

| Phase | Work | Exit criterion | Risk if skipped |
|---|---|---|---|
| **0. Baseline + telemetry** | Freeze current behaviour. Run **both prompts** — analyser *and* solver (C-06) — on all 4 charts; capture reference packages + a **mechanism-level** token ledger (C-11): compaction count, law-reinjection bytes, tool-call fan-out, palace/file reads+writes, wiki rebuilds, retrieval calls, audit-fix cycles, solver overhead. Goldens recorded with adjudication status `UNREVIEWED` (C-02). **Does not wait for 0a** (C-04) — a broken downstream contract does not prevent measuring the upstream fire. **Fixture manifest first (C-61):** record the four real pairings — `ASSIGNMENTS/<P>/project_1.md` + `QMDJ/<P>/project_1.json` (verified present; Markdown, not PDF — the solver's `pdf_extract` path needs a format check). Verify the two runtime capabilities Phase 3 depends on: structured-output enforcement (C-50), external DAG orchestration (C-51). | Reference packages + two-prompt ledger with mechanism breakdown committed to `tests/golden/`; phase-gate review confirms or falsifies the RC-1…RC-5 diagnosis (C-12); **golden adjudication is a scheduled blocking task with a named owner (C-54)** | No way to prove parity later; the wrong mechanism gets prioritised; the 3c/3d gates silently weaken |
| **0a. Shared schema + producer/consumer matrix** | One JSON Schema both prompts reference; reconcile the field-name and required-field gaps (§9.1). Build the **producer→consumer matrix** (C-05): every package field → producer, consumer, required-by-which-prompt, action (rename / derive / produce / optional). Required semantics are **producer obligations** (C-31): the compiler must *produce* `evidence_registry`, `focus_candidates`, `coverage_accounting`, `schema_adaptation_metadata`, `absence_evidence`, `exclusion_evidence`, `source_identity` — renaming optional debris does not fill a hole. Runs **in parallel with Phase 0** (C-04). **Contract manifest (C-52):** `PROMPT/contracts/contract_manifest.json` hashes every contract file — package schema, claim grammar/schema, batch contracts, rubrics, producer matrix, evidence schema, strength semantic map — and each run records the contract hash. | Both prompts validate against the same file; every solver-required field has a producer rule with genuinely identical semantics; **non-triviality assertions pass (C-53)** — registry size sane vs. node count, zero-length fields only with an explicit reason code; degenerate empty outputs fail validation | Phases 1 & 4 build against a broken contract; presence-as-performance |
| **1. Tier-0 mechanical slice** | `tools/chartc/`: traverse, normalise, variant-detect, bind, **typed composite parser** (C-16: raw original + typed atoms + primary/secondary value + role annotation + semantic type + provenance + parser status — classify, don't cut), index, compute relations + the `compute_always` patterns (count read from the spec — C-19). Every unmapped/failed value dumps **raw** into the `anomaly_registry` (C-17) — no parse failure disappears. Emits **claim/candidate seeds from all mechanically identifiable protocol classes** (C-20/C-25/C-41) — the 22 patterns *plus* origin/day-stem/Jia-set, hour/focus, duty star/door, traces, opposition, tomb/punishment/void, horse, original position, prosperity/decline, lodging, and yongshen classes — proven by a **protocol-class coverage matrix**. Also emits `strength_vocabulary_semantic_map.json` (C-57, §9.3). Covers RC-1. | Byte-identical across 2 runs; **semantic fixtures pass** (C-34): raw-leaf-set, typed-atom, binding, relation, pattern, and anomaly-class equivalence vs. goldens — not just node counts; **0 model tokens** for this slice | Core saving unrealised; a parser bug ships deterministically wrong everywhere at once |
| **2. Evidence registry + digest** | `evidence_registry.json` with **content-addressed IDs** (C-21) as the citation mechanism (C-22); `board_digest` — global **and per-batch scoped** (C-23) — + `digest_coverage_gate`. Covers RC-2. | Digest covers 100% of inventoried leaf paths on all 4 charts; every scoped digest is **content-bearing** — inlined values, roles, grounding, relation summaries, anomaly flags; never bare ID lists (C-37); global + B1–B5 scoped digests generate **without rewriting `digest.py`**; global digest ≤ 4k tokens; IDs stable across source-order shuffles | Model loses raw texture with no proof of completeness; Phase 3a is blocked on digest rework |
| **3a. Batch contracts** | Specify B1–B5 as bounded contracts: purpose, eligible `E`-ID set, **typed evidence visibility** — `VISIBLE` / `ELIGIBLE` / `FORBIDDEN_AS_PRIMARY` / `FORBIDDEN` (C-40) — candidate classes, output claim types, token budget (C-08). Plus the **`batch_scope_completeness` gate** (C-39): every atom whose role, relation, origin, dependency, adjacency, or protocol class makes it legally relevant to a batch must be in that batch's digest — no arbitrary omission for token budget, no seed-only scopes. A batch is a bounded question, not another full-chart reading. Covers RC-6 / A-12. | Each batch's `E`/`R` scope is computable by Tier 0, within budget, and carries a **scope-completeness report** on all 4 charts | Tier-1 calls cannot be determinism-tested |
| **3b. Tier-1 adjudication** | 5 bounded batch calls + P6 adjudication on a ~4k charter. **No deterministic tools in the charter** (C-13) — the 15 tool schemas (verified in both files) belong to Tier 0/2; Tier 1 gets emission only (`emit_verdicts` / compact lines). Constrained vocabularies; `E`-ID citations; **prefer API-enforced structured outputs where the runtime supports them** — syntax validity machine-enforced, not prompt-begged; the line grammar is the measured fallback (C-50). **Retry budget** — max retries per claim, per batch, per P6/RT cycle + total audit-fix tokens (C-49), exhausting into §9.7's named terminal states (C-47). **Controlled `MODEL_PROPOSAL` lane** (C-42): proposed classes are marked `PROPOSED`, evidence-validity-checked, and adjudicated — never silently accepted or dropped. Archetype resolution demand-driven (A-14). Covers RC-3. | Verdict sets and archetype winners match adjudicated goldens, **or** every diff is adjudicated and accepted | Accuracy regression goes undetected; the audit-fix loop becomes a silent full rerun |
| **3c. Parity gates (semantic + anomaly)** | Semantic parity: **G0–G10 layered diff** vs. goldens (C-33). Anomaly parity: Tier-0 surfaces **every** parse failure, unknown term, unmapped path, malformed composite into `anomaly_registry` (C-17), each tagged with reason code + class — `UNKNOWN_TERM` / `UNMAPPED_VALID_DOMAIN_VALUE` / `MALFORMED_VALUE` / `SEMANTIC_CONFLICT` / `SCHEMA_AMBIGUITY` / `PARSER_FAILURE` (C-18). Covers A-22. | Zero silently-dropped values; **anomaly-class and reason-code parity**, not just count (count alone is gameable); every §9.3 term mapped or an explicit anomaly; no unexplained G-layer diff | **The refactor silently reduces accuracy** — the one way this plan loses ground |
| **3d. Deterministic resolution + scoring** | **Adjudication ≠ resolution ≠ score (C-46):** P6 adjudicates — the model prefers/rejects/leaves unresolved; this phase *resolves* deterministically (statuses, contradictions, veto/split/tie logic) and scores. **Two rubrics** replace the shared one (§9.6): Prompt 1 without `requirement_fit`; Prompt 2 with it (C-26). `evidence_phase` demoted to metadata; tie-break on substance, then stable-ID order; ties surface as `STILL_TIED` (C-29). Batch/palace auditability stays **external** (C-62): `current_revision`, `current_batch_revision`, `batch_delta`, claims added/superseded, candidates added/vetoed — event-sourced state (A-09; reuses the solver's `supersession_policy` record shape), never resent as cumulative model context. After RT: conditional **3d′ re-resolution** on material issues. | Score deterministic for a given (source, compiler version, contract hash); **0 silent ties; 0 silently suppressed candidates** (§7.3) | Score drift and ARCHETYPE_CONFLICT-style suppression return |
| **3e. Blind red-team on the candidate set** | Targeted (A-15) and **blind** (C-27): receives the immutable evidence graph + the **full legal candidate set** + candidate evidence IDs — never the original adjudication rationale — and must answer three checks (C-43): **RT-1** can the selected candidate be contradicted? **RT-2** is a rejected candidate better supported? **RT-3** is there evidence for a *missing* candidate? Output constrained to `SUPPORT` / `VETO` / `SPLIT_PROPOSED` (C-45); Tier-2 deterministically converts `SPLIT_PROPOSED` → `STILL_TIED`; material issues trigger 3d′ re-resolution. Known limit, stated in the spec (C-44): blind ≠ independent — RT is bounded by the deterministic candidate/evidence frame; full re-derivation is intentionally not funded. | RT-1/RT-2/RT-3 all answered; no freeform verdict reaches the solver; every challenge resolved or split recorded | An anchored red-team rubber-stamps the verdict — or a better rejected candidate stays rejected |
| **4. Tier-2 builder + gates** | Package builder, generated MD views, mechanical gates. The package carries compact **`coverage_accounting`** (counts, completeness, hashes, unresolved count); the full manifest moves to the `audit/coverage.json` **sidecar** (C-30) — heavy audit artifacts leave the model-facing package surface now, ahead of the wider A-19 sidecar split (C-32). Failure is **package-valid** (C-47/C-48): exhausted retries serialize as schema-compliant `UNRESOLVED` / `ESCALATED` / `FAILED_CONVERGENCE` objects — or explicit empty states in the solver's own verified vocabulary (`NO_EVIDENCE`, `EMPTY_EVIDENCE`, `STILL_TIED`, `BLOCKED_EVIDENCE_TIED`). Tier 2 builds, serializes, scores, gates — **zero interpretation logic** (C-63): the builder is a compiler, not a second analyst. Covers RC-4. | Package validates against the shared schema; determinism check green; solver loads the compact core **without ingesting the full audit universe**; **`assignment_solver` accepts the package** — including an unresolved-state fixture (C-48) | Downstream breaks; downstream reasoning pays for upstream bookkeeping |
| **5. Cutover** | Spec right-sizing (charter vs. reference), archive old prompt, wire regression CI. Covers RC-5. | Ledger shows target; harness green on all 4 charts | Old and new paths coexist indefinitely |
| **6. (Next)** | Apply the same pattern to `assignment_solver.yaml` — identical shape: 24k spec, 14 mandated wiki articles, self-reported gates. | — | Second 1M-token pipeline remains |

**Why 0a moved ahead of 1.** The Phase-1 compiler and the Phase-4 builder both emit against the package contract. Building them against the current, broken contract would bake the defect into the new code. 0a is on the critical path either way; doing it first costs nothing extra. **But 0a gates only the compiler and builder — not Phase 0** (C-04): telemetry starts immediately even while the solver still rejects packages, and 0a runs as a parallel workstream.

**Sequencing note (corrected per C-15):** Phases 1–2 are pure code with a *structural* oracle (leaf-set equivalence, hash equality) — that oracle is strong for structural correctness and silent on semantic correctness. They remove stochastic drift but remain subject to deterministic mis-typing, which is why Phase 3c carries semantic fixtures rather than node counts. Phase 3 remains the only phase that can regress interpretive accuracy; Phase 1 is the phase most likely to introduce a *systematic* semantic error, because a parser bug is applied uniformly to every chart.

---

## 9. Findings that need a decision (found while reading, not part of the token work)

These are live defects. Two of them affect accuracy *today*, independent of the token work.

### 9.1 — The two prompts disagree on the package contract — **hard stop, fix in Phase 0a**

`assignment_solver.yaml` requires fields that `chart_analyser.yaml` never emits:

| Field | occurrences in analyser | occurrences in solver |
|---|---|---|
| `focus_candidates` | **0** | 3 |
| `evidence_registry` | **0** | 2 |
| `coverage_accounting` | **0** | 3 |
| `schema_adaptation_metadata` | **0** | 2 |
| `absence_evidence` / `exclusion_evidence` | **0** | 2 each |
| `yongshen_candidates` | 5 | 0 |

The only `focus` matches in the analyser are `hour_stem_focus` — an unrelated concept. This is enforced by **three independent gates, all failing to `PACKAGE_STALE`:**

1. `schemas.chart_analysis_package.required` lists `evidence_registry` and `focus_candidates`.
2. The integrity gate check: *"evidence registry, anomalies, absences, exclusions, coverage accounting, and source identity are present or explicitly empty with reason"* → `on_failure: PACKAGE_STALE`.
3. `canonical_evidence_classes` requires `coverage_accounting`, `schema_adaptation`, `source_identity` — each 0-occurrence in the analyser.

`PACKAGE_STALE` → `FAILURE` with no partial ship. **As written, the pipeline cannot complete.**

Compounding it: the adapter's `field_aliases` covers only `source_evidence_sha256` and `anomalies`. It has **no alias** for `interpretation_protocol_hash` (solver) vs `interpretation_protocol_v2_version_hash` (analyser), nor for `evidence_or_scoring_rubric_hash` vs `archetype_scoring_rubric_version_hash`.

**Fix (Phase 0a):** create `PROMPT/schemas/chart_analysis_package.schema.json`; have both YAMLs reference it instead of carrying divergent inline copies; add the missing aliases. Two hand-maintained copies of one contract already diverged — the shared file is what stops it recurring.

### 9.2 — The schema adapter covers 2 of the 4 real charts

`schema_adapter.variants` declares `standard_qmdj_metadata_v1` (`chart_metadata` + `palaces`, numeric keys) and `project_1_chart_info_v1` (`chart_info` + `palaces`, `xun_4`-style keys).

| Chart | Top-level keys | Palace keys | Matches a declared variant? |
|---|---|---|---|
| PORTFOLIO | `chart_metadata`, `palaces` | `1`…`9` | ✅ |
| MARKETING | `chart_info`, `palaces` | `xun_4` | ✅ |
| ADVERTISING | `system`, `timing`, `element_prosperities`, `chart_config`, `palaces` | `1`…`9` | ❌ |
| EDITORIAL | `qmdj` | `Xun 4 (Southeast)` | ❌ |

50% of real inputs fall through to `binding_failure_policy` → *"choose least-contradicted bind, record anomaly, label SCHEMA_AMBIGUITY."* Note also that `schema_detection_pass.fallback_library` names `exporter_A_format` and `exporter_B_format`, which are **never defined anywhere** — dead weight the model is told to match against.

**Fix (Phase 1):** table-driven detection + two new variant entries. Cheap, and removes half of today's anomaly noise.

### 9.3 — The strength vocabulary table is ~20% complete (accuracy defect)

`strength_scale.raw_vocabulary_mapping` has 6 entries: `Prosperous`, `Strong`, `Resting`, `Imprisoned`, `Dead`, `Discarded`.

The four real charts contain **30+ distinct raw strength strings**, most unmapped:

- **Case mismatch:** mapping keys are Title Case; PORTFOLIO uses lowercase (`prosperous`, `resting`, `strengthening`, `trapped`, `exhausted`, `dead`). A literal lookup misses **every** PORTFOLIO strength value.
- **Unmapped atoms:** `Rest`, `Strengthening` (note `Strong` is mapped but `Strengthening` is not — both appear), `Obsolete`, `Inner`, `Outer`, `exhausted`, `trapped`.
- **Composite strings needing a splitter that doesn't exist:** `"Dead / Outer"`, `"Imprisoned / Inner"`, `"Rest / Strong"`, `"Prosperous / Prosperous"`, `"Discarded / Imprisoned"`. **Law 31** requires composites be "parsed into typed evidence atoms or explicitly marked UNPARSEABLE." There is no `" / "` splitter for strength fields.
- **Overloaded fields:** `"Prosperous / Inner"` mixes a strength term with an `inner_outer_system` value in one string.
- **Parenthesised role annotations:** `"Yang Earth (Hidden Stem)"`, `"Yin Fire (Heavenly Stem)"` inside `active_stem_states.*[]`.

This feeds `wangshuai_matrix` → `board_consistency` → `archetype_scoring_rubric`. Unmapped vocabulary here is a direct, silent accuracy leak on the scoring path.

**Fix (Phase 1, amended by C-57):** treat the vocabulary as data — but *string similarity is not semantic identity*. `Rest` vs `Resting` and `Strong` vs `Strengthening` may be domain distinctions, not spelling variants, so silent normalization is forbidden. Produce `strength_vocabulary_semantic_map.json`: raw term → normalized term → semantic class → source → confidence → status (`CONFIRMED` / `MAPPED` / `DOMAIN_EQUIVALENCE_REQUIRES_ADJUDICATION` / `UNKNOWN`), plus a `SEMANTIC_UNCERTAINTY` anomaly class. A `" / "` composite splitter and a parenthesised-role stripper handle *structure*; every residual or uncertain term becomes an explicit anomaly rather than an improvisation.

### 9.4 — No chart has explicit answer / hidden-problem / best-solution fields

I searched all four charts for `answer`, `hidden_problems`, `best_solution`, `yongshen`, `recommend`, `conclusion`. **Zero hits.** (The apparent `hidden` matches are only `hidden_stem`.)

Consequence: the "explicit first" doctrine contributes **no shortcuts** on any real input — everything is COMPUTED or INFERRED. The interpretive core is genuinely load-bearing, which is why Phase 3 needs the parity harness rather than a quick eyeball.

### 9.5 — B1–B5 are undefined (blocks A-12 and determinism)

See RC-6. `B1`–`B5` appear 30+ times; the file never says what they are. The FSM instruction is literally `"execute B1 from scratch"` — with no B1 to execute. The post-batch audit requires palaces to "match the batch rule," and no batch rule exists.

**Fix (Phase 3a, ahead of Tier-1 calls):** specify each batch as a contract — purpose, eligible `E`-ID set, **forbidden evidence**, candidate classes, output claim types, token budget (C-08) — following A-12's proposed split (B1 origin, B2 hour/execution, B3 traces, B4 risk/opposition/void/tomb, B5 residual coverage). A batch is a bounded question, not another full-chart reading. Until this exists, no Tier-1 call can be determinism-tested.

---

### 9.6 — One rubric serves two pipelines, and it tie-breaks on the wrong thing (C-26/C-29)

`archetype_scoring_rubric` v1.1.0 (analyser) and v2.0.0 (solver) carry the same weights, including `requirement_fit: 0.10` — but the analyser's own rule says *"Prompt 2 only; must be 0 in Prompt 1 output."* Prompt 1 therefore carries a permanent placeholder zero: 10% of the rubric is a component that cannot exist upstream. Absence of assignment context is not zero requirement satisfaction. The two copies have also already drifted (`grounding_tier_scores.UNKNOWN`: `0.1` in the analyser, `0.0` in the solver) — the standard failure mode of a shared constant pasted into two files.

Second defect: the solver's `tie_break_order` ends with **"earlier `evidence_phase`"** — provenance used as an epistemic quality signal. Earlier evidence is not truer evidence; under batching it would just mean "born in B1." And in both files, a tie that survives the tie-break chain sets `ARCHETYPE_CONFLICT`, which suppresses the answer — a silent tie-break by omission, and a silent candidate suppression under the accuracy budget (§7.3).

**Fix (Phase 3d):** two rubrics — **Prompt 1:** grounding, corroboration, contradiction penalty, board consistency; **Prompt 2:** those plus requirement fit (computed by the solver's `solution_engine`). Tie-break order becomes: grounding → corroboration → contradiction → board consistency → substantive protocol priority → deterministic stable-ID order. `evidence_phase` remains metadata only. Ties surface as explicit `STILL_TIED` output — never silently resolved, never answer-suppressing.

---

### 9.7 — "Mark unresolved and escalate" is undefined — and `never_ask_user` forbids the obvious reading (C-47/C-48)

Both prompts pin `interaction_policy: never_ask_user_about_chart` / `never_ask_user_about_assignment` (verified). "Escalate" therefore cannot mean "ask a human mid-run" — an undefined escalation is a hidden hang. Retry exhaustion must land in a **named terminal state**:

- **Critical unresolved object** — blocks a package field the solver hard-requires → halt into an explicit failure state with a written operator report, mirroring the solver's own `PACKAGE_STALE` / `FATAL_AUDIT_LOOP` pattern (*"do not ship partial artefacts"*).
- **Non-critical unresolved object** → ship the package with explicit `UNRESOLVED` / `ESCALATED` markers as **schema-compliant objects** — failure must be package-valid, not merely logged.

The downstream vocabulary already exists (verified in `assignment_solver.yaml`): `empty_evidence_policy` maps `NO_EVIDENCE` → blocks related must-requirements, `EMPTY_EVIDENCE` → continue only for optional slots, `no_archetype_resolution` → no live verdict for that slot; `unresolved_tie_policy` emits `STILL_TIED` split candidates and `BLOCKED_EVIDENCE_TIED` where a single answer is required. The producer serializes into **that** vocabulary — fixture-tested in Phase 4, not assumed.

---

## 9A. The laws mandate the expensive behaviour — they must be amended, not just worked around

The audit correctly says *"do not begin by deleting laws."* But the converse also holds: **several laws currently forbid the target architecture.** Building the compiler without amending them leaves the engine in violation of its own spec, and the `law_coverage` gate would flag it.

| Law | Text (abbrev.) | Verdict under the new architecture |
|---|---|---|
| 6 | "Recursive path inventory and schema adaptation are mandatory before Phase 0" | ✅ **Satisfied by code.** Still mandatory, still before Phase 0 — just executed by `chartc`. |
| 12 | "The `solution_seed` object updates **after every palace** and every phase" | ⚠️ **Conflicts.** Directly contradicts batching (A-11/A-12) and delta-passing (A-09). The **law text itself is amended** (C-14) to "after every batch and every phase" — laws must describe the new loop, not the old one. |
| 22 | "Every JSON path must be inventoried before interpretation" | ✅ **Satisfied by code.** |
| 28 | "No synthesis verdict may cite only a parent object when child leaf paths exist" | ✅ **Satisfied** — `E###` registry stores `source_leaf_path`; resolver fails closed. |
| 31 | "Composite strings must be parsed into typed evidence atoms or marked UNPARSEABLE" | ⚠️ **Currently violated in practice** — no `" / "` splitter exists (§9.3). Needs the splitter, then code-enforced. |
| 32 | "Coverage gates block Phase 6 and PACKAGE_RENDER unless … complete" | ✅ **Satisfied by code gates.** Stronger, in fact — currently self-reported. |

**Only law 12 needs a genuine semantic change.** Everything else is a change of *executor*, not of *rule*. That is the argument for framing this as enforcement rather than as a rewrite.

---

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Digest omits texture the model needed | `digest_coverage_gate` proves full leaf coverage; raw stays one tool-read away; Phase 3 diffs against baseline catch omissions |
| Collapsing B1–B5 loses evidence-phase ordering | `evidence_phase` becomes a data field stamped by Tier 0; `tie_break_order` consumes it as data. `P5.confirm_veto_pass_on_already_read_palaces` is preserved as an explicit Pass-B stage |
| Model forgets a law it can no longer see | `law_coverage` gate: every law ID must map to a code check or a charter clause |
| Tier 0 has a bug → silently wrong package | `determinism_check` (run twice, diff) + Phase 0 golden fixtures + **semantic fixtures** (C-34): leaf-set, typed-atom, binding, relation, pattern, anomaly-class equivalence. Deterministically wrong is still possible — that is what the fixtures are for (C-15) |
| Runtime has no prompt caching / persistent session | The per-call ≤7k bound still holds; the ~30k stretch slips to ≤45k uncached — cached-prefix behaviour is **measured in Phase 0**, not assumed (C-10) |
| Telemetry falsifies the compaction/RC diagnosis | Phase gates include a mechanism review (C-11/C-12); the roadmap order is hypothesis-driven and gets re-prioritised on evidence, not defended |
| Parser mis-types a composite (e.g. `Yang Earth (Hidden Stem)`) | Typed parser preserves raw original + role annotation (C-16); anything unmapped lands in `anomaly_registry` with a reason code (C-17/C-18); the G-layer diff localises the damage (C-33) |
| Parity diffs in Phase 3 are real regressions, not improvements | Every diff adjudicated explicitly; a diff can be accepted as an *improvement* only with a written reason |
| Over-compression forces rework | Digest budget is 4k, ~50% headroom over the ~2.5k estimate; red-team spend deliberately increased |
| Generated wiki views diverge from the package | Impossible by construction — both render from the same state JSON; the `G-LAYER-A-CONTRACT-SATISFIED` hash check becomes trivially satisfiable |
| Runtime lacks API-enforced structured outputs | The strict line grammar + per-claim re-ask stays as the fallback; capability verified in Phase 0 before anything is deleted (C-50) |
| Host runtime cannot orchestrate the Python tiers | C-51's DAG needs an alternate execution harness; **verify before Phase 1** — the plan's largest unverified execution assumption |
| Solver graceful degradation is assumed, not tested | Phase 4 exit includes an unresolved-state fixture consumed by the real solver (C-48) |
| P6/RT budgets are planning estimates | Claim-graph and neighbourhood sizes may exceed them on complex charts; validated in Phase 0 telemetry (C-36/C-38) |
| Golden adjudication has no owner | Phase 0/3c line item with a named owner; unadjudicated diffs block 3c/3d exit — otherwise the gates silently weaken (C-54) |

---

## 11. Repository layout after the change

```
PROMPT/
  chart_analyser.yaml                  ← slimmed to a ~4k Tier-1 charter, no deterministic tools (C-13), zero FSM transitions (C-51)
  assignment_solver.yaml               ← Phase 6
  schemas/
    chart_analysis_package.schema.json  ← NEW (Phase 0a): single shared contract
    producer_consumer_matrix.yaml      ← NEW (Phase 0a): field → producer / consumer / action (C-05)
    batch_contracts.yaml               ← NEW (Phase 3a): B1–B5 bounded contracts (C-08)
    rubrics.yaml                       ← NEW (Phase 3d): two rubrics, shared constants (C-26)
    claim_line_grammar.txt             ← NEW (Phase 3b): regex per compact line type (C-24)
    strength_vocabulary_semantic_map.json ← NEW (Phase 1): raw → normalized → class → confidence → adjudication status (C-57)
  contracts/
    contract_manifest.json             ← NEW (Phase 0a): hashes of every contract file; recorded per run (C-52)
  PLAN-token-reduction.md              ← this file

tools/chartc/                           ← NEW (Phase 1): deterministic, 0 model tokens
  __init__.py
  pipeline.py         host DAG: Tier 0 → B1–B5 → P6 → resolve/score → RT → 3d′ → Tier 2 (C-51)
  inventory.py        traverse · normalise · coverage manifest · absence/exclusion
  schema_adapter.py   variant detection · semantic binding · palace-key resolution
  parsers.py          typed composite parser (atoms · roles · status — C-16) · stems · ganzhi · strength
  geometry.py         opposition · star home · horse · sanqi/liuyi · inner/outer
  patterns.py         all compute_always patterns (count read from spec — C-19) · wangshuai matrix
  registry.py         evidence_registry · content-addressed IDs (C-21/C-22) · anomaly_registry + taxonomy (C-18)
  seeds.py            claim/candidate seeds from ALL protocol classes + coverage matrix (C-20/C-25/C-41)
  digest.py           board digest — global + per-batch scoped, content-bearing (C-23/C-37) · digest_coverage_gate
  build_package.py    Tier-2 assembly · ID resolution · scoring (two rubrics) · coverage_accounting + audit/coverage.json sidecar (C-30) · failure serialization (C-47/C-48) · generated wiki views
  gates.py            all mechanical gates · G0–G10 layered diff (C-33) · retry budget enforcement (C-28) · batch_scope_completeness (C-39) · contract-hash check (C-52)

tests/
  golden/                               ← Phase 0: reference packages (adjudication status) + two-prompt token ledger
  golden/fixture_manifest.yaml         ← the four real Assignment↔chart pairings (C-61)
  fixtures/                             ← semantic fixtures: typed atoms · relations · patterns · anomaly classes (C-34)
  mutation/                             ← injected faults → expected G-layer failures (C-59)
  test_chartc.py                        ← determinism · semantic fixtures · vocabulary coverage
```

The four charts in `QMDJ/` are the fixture set: PORTFOLIO and MARKETING as the two covered variants, ADVERTISING and EDITORIAL as the two uncovered ones (§9.2). That is unusually good coverage for a regression harness — four real inputs, four different encodings of the same semantics.

---

## 12. Reconciliation with the cumulative audit (A-01 … A-23)

The audit and this plan converge independently on the same thesis: **the token cost is architectural, not editorial.** Verdict: **18 adopt, 2 adopt-amended, 1 defer, 1 reject.**

### 12.1 Resolving the audit's own "unverified" claims

| Audit claim | Status after checking the repo |
|---|---|
| #3 — "`repeat_at_top_of_context` must be verified; if absent the claim weakens" | ✅ **Verified present** in *both* files (chart_analyser L117, assignment_solver L181). The mechanism is real. The *magnitude* (~800k) remains modelled, not measured. |
| #1 — "token estimates not yet measured" | ✅ Agreed. The ~280k generated figure is modelled from the spec's own field lists; the 1M–3M is the user's observed range. **Phase 0 exists to replace both with telemetry.** |
| #2 — "runtime capability assumed" | ✅ Resolved: Tier 0 as Python in-repo is now locked (Decision 1). |
| #6 — "downstream solver compatibility must be checked" | ⚠️ **Escalated.** Not a risk to check — a confirmed hard stop. See §9.1: three independent gates → `PACKAGE_STALE`. Their "may still demand too much" is an understatement; it demands fields that are never emitted. |
| #5 — "'near 100%' is overclaimed unless segmented" | ✅ Agreed and adopted as A-20's three-way split (§12.3). |

### 12.2 Where the audit is better than this plan — adopted

| Item | Why it wins | Change made |
|---|---|---|
| **A-07** stable IDs (`E#`/`R#`/`I#`/`C#`/`A#`) | My path-aliasing (`P1.hs`) only covers source paths. It cannot address board-level evidence (void branches, seasonal strengths) or computed relations, which have no source path. IDs are uniform and support the claim/candidate/conflict graphs L2 needs. | §5 note 1 rewritten; Decision 5 locked |
| **A-12** B1–B5 as specialised bounded queries | My plan collapsed B1–B5 into 2 passes. That threw away the batches' semantic purpose and, with it, the `evidence_phase` provenance the tie-break rule consumes. Their version preserves it *and* bounds the context. Cost ~15k vs ~9k — immaterial against 1M–3M. | Decision 6 locked; Phase 3a added |
| **A-14** demand-driven archetype resolution | Genuine omission from my plan. Note it is *compatible* with existing law 18, which only requires archetype_resolution for verdicts feeding `best_solution` / `hidden_problems` / `my_answers`. | Folded into Phase 3 |
| **A-20** three-way accuracy split | Superior to my two-way split. Structural / computational / interpretive are genuinely distinct failure modes — §9.3's strength-vocabulary defect is a **computational** rule-table error, not structural and not interpretive, and only the 3-way split classifies it correctly. | Adopted (§12.3) |

### 12.3 Adopted as-is

A-01 (stop law reinjection) · A-02 (consolidate palace objects) · A-03 (batch-level retrieval) · A-04 (ban manifests from context) · A-05 (compile, don't narrate) · A-06 (schema adaptation as code) · A-08 (split palace evidence from claims) · A-09 (event-source `solution_seed`, pass deltas) · A-10 (compress S1–S14) · A-11 (batch verdicts) · A-13 (P6 consumes graphs) · A-15 (targeted red team) · A-16 (defer Markdown to final render) · A-18 (targeted AUDIT_FIX) · A-21 (regression pyramid) · A-22 (preserve anomalies) · A-23 (guard retrieval).

### 12.4 Amended

| Item | Amendment |
|---|---|
| **A-17** (move double-compute determinism out of production) | Direction right, but **it dissolves rather than needs solving.** The double-run is expensive only because it is LLM work. Once A-05 lands, `determinism_check` runs a pure function twice — microseconds, zero tokens. Keep the check in production; it becomes free. No need to demote it to release-time. |
| **A-22** (anomaly preservation) | Audit files this as **P2** governance. Wrong priority: it is the **single mechanism by which this refactor can lose accuracy**, and §9.3 shows the failure is already happening (30+ real strength strings, 6 mapped). Promoted to **blocking gate** — now Phase 3c, strengthened by the anomaly taxonomy (C-18) and class-parity (not count) checks. |

### 12.5 Deferred / rejected

| Item | Verdict | Reasoning |
|---|---|---|
| **A-19** (manifest + sidecars) | **Defer to Phase 6** | Right instinct, wrong moment. The solver's `package_integrity_gate` currently expects one `chart_analysis_package.json` with a single `package_file_sha256`; splitting now means redesigning provenance and the strict adapter *while simultaneously* fixing the contract break (§9.1). Sequencing risk for no gain: post-compiler the package is compact anyway, since the 46k path manifest is the only real bloat — and **that** is the natural first sidecar (`audit/coverage.json`). Do the shared schema first; revisit when the solver itself is refactored. |
| — (audit's 60–70% reduction target) | **Reject as a target** | It is ~10× too pessimistic because it assumes the mechanical work stays with the model. It would leave you at ~300k–1M tokens. The compiler architecture reaches ~25–40k, i.e. ~97–99%. Settling for 60–70% means leaving the actual root cause (RC-1) in place. |

### 12.6 What the audit missed

Four findings from this repo, all confirmed, none present in the audit:

1. **§9.1 — contract break is a hard stop**, not a compatibility risk. Three independent gates → `PACKAGE_STALE` → `FAILURE`. Their risk #6 says "must be checked"; it is already failing.
2. **§9.2 — the schema adapter covers 2 of 4 real charts.** This is a *prerequisite* for A-05/A-06: you cannot write a deterministic compiler over an adapter that fails on half your inputs. ADVERTISING and EDITORIAL must get variant definitions first.
3. **§9.3 — the strength vocabulary table is ~20% complete**, including a case mismatch that misses *every* PORTFOLIO value. Concrete proof that A-22's risk is live today, not hypothetical.
4. **§9.4 — no chart has explicit answer/hidden-problem/best-solution fields.** Bounds how far compression can go: the interpretive core is load-bearing on 100% of real inputs.

Plus **RC-6 / §9.5 — B1–B5 are undefined**, which converts A-12 from an efficiency win into a correctness prerequisite.

### 12.7 One thing both of us missed

**The laws mandate the expensive behaviour.** The audit says "do not begin by deleting laws," but the deeper issue is that law 12 ("`solution_seed` updates after every palace") *forbids* batching, and laws 6/22/28/31/32 must be re-pointed at a new executor. See §9A — only law 12 needs a genuine semantic change; the rest change executor, not rule. This matters because `law_coverage` (§7) would otherwise flag the new architecture as a violation of its own spec.

### 12.8 Revised implementation order

The audit's step 1 is "instrument the current run." **Correction:** if §9.1 is a hard stop, there is no completed run to instrument — you would be measuring a failure. Order:

1. **Confirm or clear the contract break** (§9.1) — cheapest first step, and unblocks everything.
2. **Instrument** — tokens by stage, tool calls, retrieval count, law re-injection count, file writes, audit-fix cycles (A-01's magnitude finally becomes measured, not modelled).
3. **Shared schema** (Phase 0a) + **variant definitions for ADVERTISING/EDITORIAL** (§9.2).
4. **Deterministic compiler** (A-05/A-06) + **anomaly-parity gate** (A-22, now Phase 3c) + **vocabulary repair** (§9.3).
5. **Evidence IDs + registry** (A-07), **palace evidence/claims split** (A-08), **delete RAG** (§5 note 4).
6. **Batch contracts** (A-12/RC-6) → **Tier-1 prompts** (A-11/A-14) → **graph synthesis** (A-13) → **targeted red team** (A-15).
7. **Package + final render** (A-16/A-19-deferred), then **Phase 6 for `assignment_solver.yaml`**.

---

## 13. Reconciliation with audit round 3 (C-01 … C-35)

Round 3 is a tightening pass, not a redirection: it accepts the target architecture and corrects this plan where it was wrong, vague, or self-contradictory. **All 35 items are adopted** — none rejected — of which several were corrections this document had to accept, and one (C-14) was already present in substance (§9A).

### 13.1 Corrections this plan had to accept

| Item | What was wrong here | Fix |
|---|---|---|
| C-01/C-02 | "Parity with the current baseline" was offered as the accuracy guarantee — parity with a baseline that guesses (§9.3, §9.5, §9.2) is parity with a guess | Withdrawn — §7.1: legacy outputs are telemetry and diff discovery only; goldens carry adjudication status |
| C-03 | Two-layer accuracy model (deterministic / interpretive) | Three contracts: structural / computational / interpretive (§7) — this is what classifies §9.3 correctly as a *computational* defect |
| C-07 | §5 still said "3 calls" after B1–B5 batching was locked — a live self-contradiction | 7-call topology (B1–B5 + P6 + blind RT) in the diagram, budgets, and decision 7 |
| C-10 | "~25–40k" headline conflated per-call context with cumulative inference | Two-metric budget (§2): ≤6–7k per call, ≤35–45k uncached; ~30k is a caching-dependent stretch |
| C-15 | "Phases 1–2 cannot regress accuracy" | Withdrawn (§7.2): determinism ≠ truth; a parser bug is deterministic and wrong — semantic fixtures added everywhere node counts stood |
| C-19 | Plan hard-coded "23 compute_always patterns" | **Verified against the file: 22.** Corrected in 4 places; the count is now data-driven, asserted as `pattern_catalog_count == source_spec_count` |
| C-26/C-29 | The shared-rubric placeholder zero and the `earlier evidence_phase` tie-break were unlisted defects | §9.6: two rubrics; tie-break on substance then stable-ID; ties surface, never suppress |
| C-35 | "Near 100%" had no enforcement form | §7.3 accuracy budget — six zeros and a determinism requirement, gate-enforced |

### 13.2 Adopted new mechanisms

C-05 producer→consumer matrix (0a) · C-08 batch-contract fields incl. **forbidden evidence** (3a) · C-13 tool-free Tier-1 charter (3b) · C-16 typed composite parser — classify, don't cut (1) · C-17/C-18 anomaly registry with reason codes + six-class taxonomy (1/3c) · C-20/C-25 deterministic claim & candidate seeds (1) · C-21 content-addressed IDs (2) · C-22 `evidence_registry` replaces the alias table (2) · C-23 per-batch digest scoping as a Phase-2 exit criterion (2) · C-24 strict line grammar + per-claim re-ask (3b) · C-27 blind red-team (3e) · C-28 retry budget with escalation (3b) · C-30/C-31/C-32 `coverage_accounting` vs `audit/coverage.json`, producer obligations (0a/4) · C-33/C-34 G0–G10 layered diff + semantic fixtures (1/3c).

### 13.3 Sequencing adopted

C-04 — Phase 0 telemetry does **not** wait for 0a; 0a runs in parallel and gates only the compiler/builder. C-06 — the solver is measured in Phase 0 (half-measured pipelines produce false victories). C-11 — mechanism-level telemetry, not just totals. C-12 — phase gates include a telemetry review; the roadmap is a hypothesis, not a covenant. C-14 — law 12's text is amended, not worked around. The roadmap's 3a–3e now mirrors the audit's locked order, with 3d (deterministic resolution + scoring) and 3e (blind red-team) as explicit gates rather than folded into "Tier-1 prompts."

### 13.4 Superseded statements — purged from this document

1. "Tier-1 is a 3-call system" — §5 diagram; now 7 calls.
2. "~30k total" as the standalone headline — now a caching-dependent stretch (§2).
3. "Phase 1 cannot regress accuracy" — withdrawn (§7.2).
4. "23 compute_always patterns" — 22, and data-driven regardless.
5. "Parity with legacy baseline proves accuracy" — §7.1.
6. "Path alias table is the primary citation mechanism" — superseded by decision 5 (A-07) and `evidence_registry` (C-22).
7. "Aliases can fix missing package semantics" — never claimed here, now structurally excluded by producer obligations (C-31, Phase 0a).

### 13.5 Residual honest unknowns (this round changed none of them)

Token mechanics remain **modelled** until Phase 0 telemetry lands (compaction count, law-reinjection bytes, fan-out). Legacy-baseline corruption remains **asserted** until the golden scrub (§7.1 adjudication status). Runtime caching behaviour remains **unmeasured**. Each has a named gate: C-11's mechanism ledger, C-02's adjudication status, C-10's cached-prefix measurement. Until those gates run, every number in §2 is a model with its assumptions stated, not a measurement.

---

## 14. Reconciliation with audit round 4 (C-36 … C-63)

Round 4 changes the thesis. Rounds 1–3 asked *how to stop paying 1M–3M tokens*; this round asks the question that follows: **once the compiler owns evidence selection, what stops it from becoming a deterministic information-selection bottleneck?** A wrong rule perfectly implemented is still wrong (C-58), and a seed set that under-covers the protocol silently starves the model (C-41). **All 28 items adopted** — five of them corrections to this plan's own round-3 text.

### 14.1 The mandatory three — locked as gates before any Tier-1 code

1. **Scoped-evidence completeness (C-39, with C-37/C-40).** Global digest coverage is not batch sufficiency. Every batch receives every legally relevant atom — **content-bearing** (values, roles, grounding, relation summaries), never bare ID lists — with **typed visibility** (`VISIBLE` / `ELIGIBLE` / `FORBIDDEN_AS_PRIMARY` / `FORBIDDEN`) so exclusion never blinds a contradiction check. Gate: `batch_scope_completeness` report per batch (Phase 3a exit).
2. **Controlled `MODEL_PROPOSAL` lane (C-42, with C-41).** Deterministic seeds must not become a silent ceiling. Seeds cover *all* mechanically identifiable protocol classes (coverage matrix, Phase 1), and the model can propose a new class — `PROPOSED`, evidence-validity-checked, adjudicated only where protocol permits. Never auto-live; never silently dropped.
3. **Candidate-set red-teaming (C-43, with C-44/C-45).** RT attacks the selection *and the universe*: RT-1 contradict the selected candidate, RT-2 rehabilitate a rejected one, RT-3 detect a missing one. Output terminates in `SUPPORT` / `VETO` / `SPLIT_PROPOSED`, converted deterministically by Tier-2. And the spec says plainly: blind ≠ independent — RT is bounded by the deterministic frame; full re-derivation is intentionally not funded.

### 14.2 Corrections to this plan's round-3 text

| Item | What was wrong here | Fix |
|---|---|---|
| C-58 | §4 said "**Accuracy 100% by construction**" — verbatim the overclaim round 3 should have killed | Withdrawn (§4): determinism is reproducibility, not truth; §7's "100% achievable" cells re-worded as exact-binary properties |
| C-36/C-38 | The two-metric budget applied one uniform ≤6–7k envelope to all 7 calls | Per-call shapes (§2): B1–B5 ~3–4k/500–800, P6 ~5–6k/1–1.5k, RT ~4–5k/1k; budgets now name what counts (input / generation / hard ceiling) |
| C-56 | Trick 1 claimed a compiler bump "cannot silently renumber" IDs — overclaim | Stability is **version-scoped**: IDs hold within compiler + ID-schema version; parser changes legitimately re-atomize; packages record `compiler_version` + `id_schema_hash` + `contract_hash`, so changes are explainable, never silent |
| C-43 | 3e red-teamed only the selected candidate — it could never find a missing one | Candidate-set RT with RT-1/RT-2/RT-3 (Phase 3e) |
| C-47 | "Mark unresolved and escalate" was undefined — and `never_ask_user` (verified in both files) forbids the human reading | §9.7: named terminal states — critical → explicit failure state + operator report; non-critical → package-valid `UNRESOLVED`/`ESCALATED` markers |

### 14.3 Uncertainties resolved against the repo this round

- **C-61 — the fixture pairings exist.** `ASSIGNMENTS/{PORTFOLIO,MARKETING,ADVERTISING,EDITORIAL}/project_1.md` + `QMDJ/<same>/project_1.json`: four real Assignment↔chart pairs, so the solver baseline needs no fabrication. Caveat found: assignments are **Markdown, not PDF** — the solver's `pdf_extract` path needs a format check before Phase 0.
- **C-48 — the solver already speaks "unresolved".** Verified in `assignment_solver.yaml`: `empty_evidence_policy` (`NO_EVIDENCE` blocks related musts; `EMPTY_EVIDENCE` continues only for optional slots; `no_archetype_resolution` → no live verdict), `unresolved_tie_policy` (`STILL_TIED`, `BLOCKED_EVIDENCE_TIED`), and `supersession_policy` (a record schema 3d's event log reuses). Failure serialization has a concrete target vocabulary — but the pass check stays fixture-tested, not assumed.
- **C-47 — `never_ask_user` confirmed** in both files (`interaction_policy: never_ask_user_about_chart` / `..._about_assignment`).

### 14.4 Adopted mechanisms

C-36/C-37/C-38 (call-shaped budgets; content-bearing digests; budgets that name what counts) · C-39/C-40 (batch-scope completeness; typed visibility) · C-41 (protocol-class coverage matrix beyond the 22 patterns) · C-42 (`MODEL_PROPOSAL` lane) · C-44/C-45 (RT bounds stated; machine-resolvable RT statuses) · C-46 (adjudicate / resolve / score split + 3d′ re-resolution) · C-49 (retry caps per P6/RT cycle) · C-50 (API-enforced structured outputs preferred; line grammar as measured fallback) · C-51 (host DAG replaces the `fsm_transition_table`; the prompt keeps zero transition logic) · C-52/C-53 (contract manifest with per-run hashes; non-triviality assertions) · C-54 (golden adjudication as scheduled, owned, blocking work) · C-55 (G0–G5 legacy-diffable; G6–G10 adjudication-only) · C-57 (strength semantic map; `SEMANTIC_UNCERTAINTY` class) · C-59 (mutation testing) · C-60 (two more budget zeros) · C-62 (external event-sourced auditability) · C-63 (frozen pipeline; Tier 2 = compiler, not analyst).

### 14.5 Superseded statements — purged

1. "All calls fit the same ≤7k envelope" → per-call shapes (§2). 2. "Scoped digest = ID coverage" → content-bearing (C-37). 3. "Blind red-team is independent" → bounded by the frame (C-44). 4. "Retry exhaustion escalates to a human" → §9.7 terminal states. 5. "Field presence satisfies the contract" → non-triviality (C-53). 6. "Stable IDs are stable forever" → version-scoped (C-56). 7. "Pattern seeds are sufficient" → protocol-class matrix + proposal lane (C-41/C-42). 8. "Accuracy 100% by construction" → withdrawn (§4, C-58).

### 14.6 Still unverified — each now has a named gate

Runtime structured-output support (Phase 0 check, C-50) · host DAG orchestration capability (**the plan's largest unverified execution assumption** — verify before Phase 1, C-51) · P6/RT real sizes vs. the planning table (Phase 0 telemetry, C-36) · solver graceful degradation on unresolved-state packages (Phase 4 fixture, C-48) · golden adjudication ownership (Phase 0 line item, C-54).
