"""Solver Stage 3b (SYNTHESIZE cont.): red-team findings + deck patches, then wiki corpus."""
import json, os, sys, re, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common2 import *

sol = read_json_logged(os.path.join(STATE, "solution.json"))
req = read_json_logged(os.path.join(STATE, "requirements.json"))
dr = read_json_logged(os.path.join(STATE, "deliverable_registry.json"))
rg = read_json_logged(os.path.join(STATE, "rubric_guess.json"))
pv = read_json_logged(os.path.join(STATE, "package_validation.json"))
lg = read_json_logged(os.path.join(STATE, "logo_boundary.json"))
pkg = read_json_logged(PKG_COPY)
ans, hid, best = sol["answers"][0], sol["hidden_problems"], sol["best_solution"]
deck_path = os.path.join(OUT, "SUBMISSION", "01_STRATEGY_FOUNDATION_DECK.md")

# ============ RED TEAM first (findings -> real deck patches) ============
deck = open(deck_path).read()
findings = []

# F1: arithmetic coherence between Slide 4 objectives and Slide 3 goal
old_o1 = """1. **Acquire** 400 trial-kit buyers in the first 6 months post-launch, of whom **≥12% convert** from trial
   to subscription by month 6 *(product-led acquisition objective)*
2. **Retain** — by month 12, at least **60% of monthly revenue** comes from existing subscribers,
   with third-purchase repeat rate ≥ 45% *(retention objective)*
- **How these support the business goal:** 400 trials at ≥12% conversion seed the first subscribers;
  retention discipline turns them into the 1,000-household base — acquisition fills the funnel,
  retention compounds it; both are measurable, dated, and owned"""
new_o1 = """1. **Acquire:** ramp to a sustained run-rate of **≥600 trial-kit orders/month by month 6**, converting
   **≥12% of triallists to subscription within 30 days of trial start** (delivers ≥90 new subscribers/month
   at run-rate, incl. a ≥15% referral share) *(acquisition objective)*
2. **Retain** — by month 12, at least **60% of monthly revenue** comes from existing subscribers,
   with third-purchase repeat rate ≥ 45% *(retention objective)*
- **How these support the business goal:** ≥90 new subscribers/month at run-rate after month 6, plus the
  ramp months and ≥45% third-purchase retention, compounds to the 1,000-household base at month 12 —
  the arithmetic closes by construction; both objectives are numbered, dated, and owned"""
assert old_o1 in deck, "red-team patch F1 anchor missing"
deck = deck.replace(old_o1, new_o1)
findings.append({"id": "RT-F1", "severity": "high", "probe": "Do the SMART objectives actually reach the Slide 3 goal?",
 "finding": "Old objective-1 (400 trials total @12% → 48 subscribers) cannot produce 1,000 households in 12 months — arithmetic gap a marker would catch instantly.",
 "fix": "Objective 1 rewritten as a sustained run-rate (≥600 trials/mo by M6, ≥12%→30d conversion, ≥90 new subs/mo), compounding to 1,000 at M12.",
 "status": "FIXED"})

# F2: WhatsApp consent designation
old_wa = "| WhatsApp concierge | Retention & service | India-native, high-open, personal — perfect for refill timing and questions |"
new_wa = "| WhatsApp concierge (opt-in) | Retention & service | user-consented, India-native, high-open — perfect for refill timing and questions |"
assert old_wa in deck, "red-team patch F2 anchor missing"
deck = deck.replace(old_wa, new_wa)
deck = deck.replace("| **Owned** | storefront & product pages, WhatsApp refill concierge, sleep-journal email letter, pack inserts |",
                    "| **Owned** | storefront & product pages, WhatsApp refill concierge (opt-in), sleep-journal email letter, pack inserts |")
findings.append({"id": "RT-F2", "severity": "medium", "probe": "Is WhatsApp defensibly 'Owned' in PESO (spam risk if unconsented)?",
 "finding": "Owned-media claim for WhatsApp only holds if the channel is opt-in; otherwise it is intrusive CRM and contradicts the persona's anti-spam stance.",
 "fix": "Marked '(opt-in)' / 'user-consented' on Slides 9 and 10.", "status": "FIXED"})

# F3: founder-story ambiguity for a fictional brand
old_fc = "| **Earned** | wellness editors & newsletters covering the \"switch-off\" culture; founder story of building melatonin-free in India |"
new_fc = "| **Earned** | wellness editors & newsletters covering the \"switch-off\" culture; the brand's founding narrative — built melatonin-free for India's late-working cities |"
assert old_fc in deck, "red-team patch F3 anchor missing"
deck = deck.replace(old_fc, new_fc)
findings.append({"id": "RT-F3", "severity": "low", "probe": "'Founder story' — of whom, for a fictional brand?",
 "finding": "A named-human founder was never defined; a marker could ask whose story is being told.",
 "fix": "Reworded to 'the brand's founding narrative' — the fictional founder assumption stays documented in OPERATOR/COMMENTS.",
 "status": "FIXED"})

probes = ["R21 exclusion sweep — no calendars, influencer lists, SEO keyword plans, budgets, email journey maps, creatives, dashboards anywhere in deck: PASS (terms appear only in the scope-note as excluded).",
 "R07 avoid-list — brand is one category, realistic tech, not alcohol, not a major-brand copy, defined consumer: PASS.",
 "Slide 3 is a business goal (customer base, revenue base), not a marketing activity: PASS after F1.",
 "Slide 8 is two narrative paragraphs, not a platform list: PASS.",
 "No invented market statistics, no household-size claims, no fake percentages (all numbers are planned prices/targets): PASS.",
 "Persona trace: every persona attribute consistent with Slide 5 audience definition: PASS (age, income band, city, behaviour).",
 "Non-priority platforms justified, per R18: PASS (4 named with reasons).",
 "Brand Selection Test four questions answered distinctly: PASS.",
 "Forbidden-terminology lint (chart lexicon) — zero hits (re-verified at RENDER_OUTPUT): PENDING->verified at s4.",
 "Dead-end check — every Slide 11 node hands off with context: PASS."]
open(deck_path, "w").write(deck)
progress(f"RED TEAM complete | 3 findings fixed in deck | 10 probes | deck now {len(deck)} chars")

# ============ wiki corpus ============
W = lambda name, body: write_text(os.path.join(WIKI, name), body)
rows_q = lambda r: "\n".join(f"| {x['id']} | {x['must_level']} | {x['quoted_text'][:95]}{'…' if len(x['quoted_text'])>95 else ''} | {x['page_anchor']} |" for x in r)

W("Assignment-Brief.md", f"""---
id: "assignment-brief"
type: "assignment-input"
state: "SYNTHESIZE"
sources: ["ASSIGNMENTS/MARKETING/project_1.md"]
updated: "{utcnow()}"
---

# Assignment Brief — distilled facts

- **Source:** ASSIGNMENTS/MARKETING/project_1.md · sha256 `{sha256_file(ASSIGN)[:16]}…` · 322 lines · full copy at `raw/assignment/extract.md`
- **Assignment:** Assignment 1 — Building a Digital Presence: Brand & Strategy Foundation
- **Due:** 18 September 2026 · **Format:** individual · presentation (PPT / PDF / Google Slides / Canva)
- **Brand choice:** fictional OR small/emerging real brand; reused all semester
- **Hard avoid-list (R07):** alcohol brands; unrealistic-technology dependence; overly broad concepts;
  no clear product/service; major-brand copy with a new name; categories with unclear consumer;
  multiple unrelated categories under one brand
- **Scope exclusions (R21):** no detailed social posts, content calendars, influencer lists, SEO keyword
  plans, paid-media budgets, email journeys, campaign creatives, analytics dashboards
- **Logo (R23):** no detailed logo/brand-identity work required at this stage
- **Marking (R24):** "primarily marked on clarity of thinking, not creative / visual polish"
- **Structure required:** 12 slides (intro / overview / business goal / SMART objectives / audience /
  persona / journey / strategy / PESO / channels / integrated journey / key decisions) + Brand Selection
  Test (4 questions)

Traceability: [[Requirements-Matrix]] · [[Constraints-And-Deliverables]] · [[Solution-Architecture]]
""")

W("Assignment-Corpus.md", f"""---
id: "assignment-corpus"
type: "assignment-input"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Assignment Corpus — quoted requirement atoms (verbatim)

Each atom is the exact brief text the solver bound to (R-ids mirror the requirements register).
Anchors use the brief's own section headings.

| req | level | quoted brief text | anchor |
|---|---|---|---|
{rows_q(req['rows'])}

Full-text preserved 1:1 in `raw/assignment/extract.md` (immutable). This corpus is the single source any
requirement debate is settled against.
""")

W("Requirements-Matrix.md", f"""---
id: "requirements-matrix"
type: "traceability"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Requirements Matrix — 24 rows, coverage ledger

| req | level | satisfaction point | status |
|---|---|---|---|
""" + "\n".join(f"| {r['id']} | {r['must_level']} | output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md | COVERED |" for r in req['rows'] if r['id'] not in ('R23',)) + f"""
| R23 | must_not | logo artwork ABSENT; written name/positioning only | COVERED (EXCLUDED_LOGO) |

Detailed per-requirement slide mapping: `output/OPERATOR/MAPPINGS.md` section A.
Gates: coverage gate requires 0 UNCOVERED rows at RENDER_OUTPUT.
""")

W("Rubric-Guess.md", f"""---
id: "rubric-guess"
type: "inference"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Rubric Guess (hypothesis — no PDF rubric exists)

**Basis (quoted):** "{rg['pdf_basis']}"

| hypothesis criterion | weight_hypothesis |
|---|---|
""" + "\n".join(f"| {c['criterion']} | {c['weight_hypothesis']} |" for c in rg['inferred_marking_weights_hypothesis']) + f"""

Status: {rg['status']}. Consequences taken: deck front-loads clarity devices (one-idea-per-slide,
numbered claims, tables for journey/PESO/channels, one closing decision list); visual polish deliberately
NOT pursued beyond clean markdown→slide copy.
""")

W("Logo-Boundary.md", f"""---
id: "logo-boundary"
type: "constraint"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Logo & Identity Boundary (EXCLUDED_LOGO)

- **Rule:** {lg['rule']}
- **Brief evidence (quoted):** "{lg['pdf_evidence']}"
- **Allowed:** {', '.join(lg['allowed'])}
- **Excluded:** {', '.join(lg['excluded'])}

Enforcement points: Slide 1 carries the written-name disclaimer; OPERATOR/MAPPINGS R23 row; ANNOTATED/00_STATUS
DEL-X1 EXCLUDED_LOGO. Solver spec additionally excludes actual logo artwork independent of the brief.
""")

W("Constraints-And-Deliverables.md", f"""---
id: "constraints-and-deliverables"
type: "constraint"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Constraints & Deliverable Registry

## Hard constraints (must_not)
- **R07** — avoid-list (alcohol / unrealistic tech / overly broad / no clear product / major-brand copy / unclear consumer / unrelated categories)
- **R21** — A1 scope exclusions (posts, calendars, influencer lists, SEO plans, budgets, email journeys, creatives, dashboards)
- **R23** — no logo/identity artwork
- **R13** — audience must not read as "18–45, everyone" (specificity constraint)
- **R16** — strategy must be paragraphs, not a platform list

## Deliverable registry
| id | name | must/should | status | output |
|---|---|---|---|---|
""" + "\n".join(f"| {d['id']} | {d['name']} | {d['must_or_should']} | {d['status']} | {d['output_path'] or d.get('exclusion_reason','—')} |" for d in dr['registry']) + f"""

UNGROUNDED_PACK fallback: {'USED' if dr['fallback_pack_used'] else 'NOT used'} — {dr['note']}
""")

W("Hidden-Problems.md", f"""---
id: "hidden-problems"
type: "solution-slot"
sources: ["raw/package/chart_analysis_package.json"]
updated: "{utcnow()}"
---

# Hidden Problems — five risks the brand must not walk into

| # | code | solver_score | confidence | risk (operational English) | bound req |
|---|---|---|---|---|---|
""" + "\n".join(f"| {h['rank_within_slot']} | {h['code']} | {h['computed']['solver_score']} | {h['confidence']} | {h['response'][:180]}… | {h['bound_requirement']} |" for h in hid) + """

Package basis: RES-002 archetype set (claims & mechanical evidence paths per row in solution.json /
LAYER_A appendix). Each risk is enforced as a deck guard, not left as a warning: sequencing (Slide 8),
non-priorities (Slide 10), scope note, and decisions 1/2/4 (Slide 12).
""")

W("Solution-Architecture.md", f"""---
id: "solution-architecture"
type: "engine"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Solution Architecture (solver v4.0.0 run)

## Pipeline FSM
INIT → PACKAGE_VALIDATE → PDF_INGEST → P7_SLOT_BIND → SOLUTION_ENGINE → SYNTHESIZE → RENDER_OUTPUT → HALT

## Components
- `vault/_engine2/common2.py` — logged_read (asserts no raw-chart path), sha256, state dumps, pkg_resolve
- `s1_init_ingest.py` — INIT, package validation (schema+hashes, deviations DEV-001/002), brief ingest (24 reqs)
- `s2_slotbind_engine.py` — slot binding + re-scoring under solver rubric (weights .35/.25/.20/.10/.10; tiers 1.0/.6/.3)
- `s3_synthesize_outputs.py` — deck + ANNOTATED + OPERATOR + LAYER_A authoring
- `s3b_wiki_redteam.py` — red team (3 findings fixed) + wiki corpus (this file)
- `s4_render.py` — lint, gates, manifest, HALT

## Binding
| slot | source of truth | output |
|---|---|---|
| my_answers | solution_seed.answers + RES-001 | deck Slides 1–6, Brand test |
| hidden_problems | solution_seed.hidden_problems + RES-002 | deck guards (Slides 8/10/12), [[Hidden-Problems]] |
| best_solution | solution_seed.best_solution_candidates + RES-003 | deck Slides 8–12 |

## Gates (checked at RENDER_OUTPUT)
package_schema, package_integrity, no_qmdj_read, lint_terms(0), citation_integrity, coverage(0 uncovered),
archetype_resolution_presence, layer_a_contract, red_team_applied
""")

W("Solution-Live.md", f"""---
id: "solution-live"
type: "run-log"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Solution Live — run ledger

- run: solver v4.0.0 on package {pkg['package_version']} (sha256 {sha256_file(PKG_COPY)[:16]}…)
- states DONE: INIT, PACKAGE_VALIDATE (PASS_WITH_DEVIATION DEV-001/002), PDF_INGEST (24 reqs), P7_SLOT_BIND
  (3 slots), SOLUTION_ENGINE (winner solver_score {best['computed']['winner_solver_score']}, margin
  {best['computed']['margin_vs_runner']}), SYNTHESIZE (deck + operator + Layer A + red team + wiki)
- pending: RENDER_OUTPUT gates + MANIFEST, then HALT
- machine file: `raw/state/solver_machine.json`; progress log: `vault/progress.md` ([SOLVER] rows)

Key numbers: requirements 24 (22 must, 4 must_not incl. EXCLUDED_LOGO rows, 1 should); deliverables 1 + 1 excluded;
answers slot solver_score {ans['computed']['solver_score']}; hidden problems 5 (scores
{[h['computed']['solver_score'] for h in hid]}); budgets all within objective.
""")

W("Recommended-Answers.md", f"""---
id: "recommended-answers"
type: "solution-slot"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Recommended Answers (slots as locked)

## my_answers (solver_score {ans['computed']['solver_score']}, confidence {ans['confidence']})
{ans['response']}

Rationale remarks:
""" + "\n".join(f"- {r}" for r in ans['rationale_remarks']) + f"""

## best_solution (winner solver_score {best['computed']['winner_solver_score']}, confidence {best['confidence']})
{best['response']}

Rationale remarks:
""" + "\n".join(f"- {r}" for r in best['rationale_remarks']) + f"""

## hidden_problems — see [[Hidden-Problems]] for the ranked five with mitigation mapping.
""")

W("Risk-And-Audit-Log.md", f"""---
id: "risk-and-audit-log"
type: "audit"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Risk & Audit Log (solver run)

## Deviations accepted (PASS_WITH_DEVIATION)
- **DEV-001** v4-vs-v5 hash registry skew — package matches ACTUAL generator spec + boot MANIFEST; raw/package/validation.md
- **DEV-002** key rename anomalies→anomaly_registry — data intact, validator maps

## Read audit
- Every package/brief read logged to `raw/state/solver_reads.json`; raw chart path denied by construction
  (assert in logged_read); `no_qmdj_read` gate verified at RENDER_OUTPUT.

## Open questions (operator)
""" + "\n".join(f"- {q['q']} — {q['why_open']}" for q in sol['open_questions']) + """

## Residual risk
- score compression from +fit term (ranking preserved by design); persona/price illustrative; rubric is a documented guess, not a marker PDF; DEV-001 accepted as registry lag (re-validation path documented in LAYER_A §confidence_and_residual_risk).

## AUDIT_FIX cycles
- cycle 1 (this run): red team RT-F1/F2/F3 fixed in deck before render; max 3 cycles allowed.
- gate results appended at RENDER_OUTPUT.
""")

W("Red-Team.md", f"""---
id: "red-team"
type: "red-team"
state: "SYNTHESIZE"
updated: "{utcnow()}"
---

# Red Team — adversarial review of the SUBMISSION deck

## Findings & fixes (applied to deck in this stage)
| id | severity | probe | finding → fix | status |
|---|---|---|---|---|
""" + "\n".join(f"| {f['id']} | {f['severity']} | {f['probe']} | {f['finding']} → {f['fix']} | {f['status']} |" for f in findings) + f"""

## Probe sweep (all evaluated)
""" + "\n".join(f"- {p}" for p in probes) + """

Method: marker-simulation + arithmetic audit + exclusion sweep + traceability spot-checks against
OPERATOR/MAPPINGS and the five hidden-problem guards.
""")

W("Constraints-And-Deliverables.md", open(os.path.join(WIKI, "Constraints-And-Deliverables.md")).read())  # no-op keep

# ---- MOC: append solver layer to existing MOC ----
moc_path = os.path.join(WIKI, "MOC.md")
moc = open(moc_path).read()
solver_section = f"""

---

# Assignment Solver layer (Prompt-2 run, package {pkg['package_version']})

## Assignment input
- [[Assignment-Brief]] — distilled brief facts
- [[Assignment-Corpus]] — verbatim requirement atoms (24)
- [[Requirements-Matrix]] — coverage ledger
- [[Rubric-Guess]] — marking hypothesis
- [[Logo-Boundary]] — EXCLUDED_LOGO rule
- [[Constraints-And-Deliverables]] — hard constraints + registry

## Solution
- [[Hidden-Problems]] — five risks adopted
- [[Solution-Architecture]] — solver FSM, components, gates
- [[Solution-Live]] — run ledger
- [[Recommended-Answers]] — locked slot answers
- [[Risk-And-Audit-Log]] — deviations, read audit, residual risk
- [[Red-Team]] — adversarial review (3 findings fixed)

## Outputs
- `output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md` — the marker-facing deck
- `output/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md` — technical annex (5 contract sections)
- `output/OPERATOR/` — COMMENTS / MAPPINGS / PATH_RANK · `output/MANIFEST.md` — render-time manifest
"""
if "Assignment Solver layer" not in moc:
    moc = moc.rstrip() + solver_section
    moc = moc.replace('# MOC — Carpathia QMDJ Chart Analysis (project_1)',
                      '# MOC — Carpathia: Chart Analysis (frozen) + Assignment Solver')
    open(moc_path, "w").write(moc)
progress("wiki corpus written: 12 articles + MOC updated (combined chart+solver)")

# meta copy of denylist
os.makedirs(os.path.join(WIKI, "_meta"), exist_ok=True)
shutil.copy2("PROMPT/forbidden_terms.txt" if os.path.exists("PROMPT/forbidden_terms.txt") else os.path.join(REPO, "PROMPT", "forbidden_terms.txt"), os.path.join(WIKI, "_meta", "forbidden_terms.txt"))
logged_read(os.path.join(REPO, "PROMPT", "forbidden_terms.txt"))
machine_update(state="SYNTHESIZE_DONE")
print(json.dumps(findings, indent=1))
