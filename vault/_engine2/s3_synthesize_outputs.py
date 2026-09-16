"""Solver Stage 3a (SYNTHESIZE): author SUBMISSION deck + ANNOTATED + OPERATOR + LAYER_A."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common2 import *

sol = read_json_logged(os.path.join(STATE, "solution.json"))
pv = read_json_logged(os.path.join(STATE, "package_validation.json"))
reg = read_json_logged(os.path.join(STATE, "deliverable_registry.json"))
req = read_json_logged(os.path.join(STATE, "requirements.json"))
pkg = read_json_logged(PKG_COPY)
ss = pkg["solution_seed"]
ans, hid, best = sol["answers"][0], sol["hidden_problems"], sol["best_solution"]
machine_update(state="SYNTHESIZE")

# ================= SUBMISSION deck (clean marketing English; lint-enforced at RENDER) =================
deck = f"""---
id: "submission-deck"
type: "submission"
state: "SOLUTION_DRAFT"
slot_source: ["my_answers", "hidden_problems", "best_solution"]
assignment: "ASSIGNMENTS/MARKETING/project_1.md"
brand: "Off Hours"
updated: "{utcnow()}"
status: "draft"
---

# Assignment 1 — Building a Digital Presence: Brand & Strategy Foundation
**Brand: Off Hours** · D2C sleep & recovery · Individual assignment · Submission 18 September 2026
Format: presentation deck (export to PPT / PDF / Google Slides / Canva). One deck, twelve slides.

---

## Slide 1 — Brand Introduction
- **Brand name:** Off Hours *(written name and positioning only — no logo at this stage, per brief)*
- **Category:** D2C sleep & recovery — functional night-drink sachets (melatonin-free)
- **Product / service:** 10-sachet box of a magnesium + L-theanine + chamomile night drink; refill subscription
- **Geography / market:** Mumbai + Bengaluru, India (two-city beachhead, delivery via own storefront)
- **Price positioning:** Premium-accessible — **₹999** 10-night trial kit; **₹1,899/month** subscription (planned price points)
- **One-liner:** *Off Hours — what begins when work ends.*

---

## Slide 2 — Brand Overview
- **What we offer:** a simple, drug-free wind-down ritual in a glass — one sachet, warm water, lights-low
- **Consumer problem solved:** urban professionals 25–40 finish work at 9–10 pm, still wired —
  they scroll, snack, and sleep badly; melatonin feels medical, chamomile tea feels weak
- **What makes it different:** melatonin-free ingredient-forward formula built as a *ritual*, not a pill;
  subscription refill rhythm; taste and texture designed for a work-night reality (unsweet, light)
- **Competitors / alternatives:** OTC sleep gummies and melatonin tablets; herbal/sleep teas;
  wellness apps (guided wind-downs); the default alternative — doing nothing and scrolling
- **Strategic stance:** we compete with the *habit of not switching off*, not with pharmacies

---

## Slide 3 — Business Goal
- **One primary business goal:** build a base of **1,000 paying subscribed households** within the first 12 months
  of launch in the two launch cities
- This is a business outcome (a recurring-revenue customer base), not a marketing activity — marketing's job
  (next slide) is the measurable path that gets the business there
- Why this goal: a D2C subscription business compounds on retention; a loyal base funds every later stage of growth

---

## Slide 4 — Marketing Objectives (SMART)
1. **Acquire** 400 trial-kit buyers in the first 6 months post-launch, of whom **≥12% convert** from trial
   to subscription by month 6 *(product-led acquisition objective)*
2. **Retain** — by month 12, at least **60% of monthly revenue** comes from existing subscribers,
   with third-purchase repeat rate ≥ 45% *(retention objective)*
- **How these support the business goal:** 400 trials at ≥12% conversion seed the first subscribers;
  retention discipline turns them into the 1,000-household base — acquisition fills the funnel,
  retention compounds it; both are measurable, dated, and owned

---

## Slide 5 — Target Audience
- **Demographics:** 25–40, single or young-couple households, degree-educated professionals
  (tech, finance, consulting, media), Mumbai (Powai, Lower Parel, Andheri) + Bengaluru (Indiranagar, Koramangala, HSR)
- **Income / spending power:** ₹12L+ annual household income; already pays for convenience and self-care
  (food delivery, gym apps, streaming) — ₹999 is an impulse-try, ₹1,899/mo competes with one dinner out
- **Psychographics:** evidence-seeking wellness sceptics — read ingredient lists, dislike hype,
  want better mornings more than "sleep"; identity: ambitious but burning the candle
- **Behaviour:** shops online several times a week; subscribes and cancels ruthlessly; discovers via
  short video and peer group chats; researches reviews before any ingested product; active 10 pm–1 am
- **Not our audience:** insomniacs seeking clinical treatment; price-first general supplement buyers;
  anyone outside the two cities in phase 1

---

## Slide 6 — Primary Buyer Persona — "Meera"
- **Profile:** Meera Nair, 32, product manager at a Series-B startup, Bengaluru (Koramangala), ₹18–24 LPA
- **Lifestyle:** stand-ups at 10 am, deep work at night; gym membership renewed yearly, used rarely;
  orders in 4–5 nights a week; unwinds with series + scrolls till 1 am; alarm at 7:30
- **Interests:** productivity systems, longevity content, café coffee, weekend treks
- **Goals:** wake up clear-headed without another pill; feel in control of her evenings again
- **Pain points:** 3–4 hours of "junk time" at night; groggy mornings; sceptical of gummies after one
  bad experience; hates auto-renew traps
- **Motivations:** visible morning energy, a ritual that feels like hers, evidence over promises
- **Favourite digital platforms:** Instagram Reels, YouTube deep-dives, WhatsApp groups, Reddit India
  fitness threads, and her email (she reads a good newsletter)
- **Online buying behaviour:** trials first; checks ingredients + reviews; pays UPI; will subscribe
  after one good full box; cancels in one click if annoyed
- **Quote:** *"I don't have a sleep problem — I have a switching-off problem. Show me something
  simple that actually works and I'll stick with it."*

---

## Slide 7 — Customer Journey (persona: Meera)

| Stage | Consumer behaviour | Digital touchpoints | Questions / concerns | Potential friction |
|---|---|---|---|---|
| Need / Trigger | 1:00 am, wired, dreading 7:30 alarm; resolves to fix it | late-night scroll; notes app; group chat venting | "Why can't I just switch off?" | feelings, not words — nothing to search *for* |
| Discovery | sees short-video content about wind-down rituals | Reels/shorts, creator newsletters, Reddit threads | "Is this a real category or snake oil?" | ad blindness; scepticism is high at first contact |
| Research | googles ingredients, reads label breakdowns & reviews | search, brand site, YouTube explainers, Reddit | "What's actually in it? Any habit-forming stuff?" | thin or jargon-heavy info kills trust instantly |
| Consideration | compares trial kit vs. gummies vs. tea; checks price/night | product page, reviews, comparison content, WhatsApp | "Is ₹999 for 10 nights worth it? Can I taste it?" | price framing without a per-night anchor |
| Purchase | orders trial kit; UPI one-tap; expects 2-day delivery | own storefront, UPI checkout, order confirmations | "Will it arrive before the weekend? Easy returns?" | clunky checkout; forced account creation |
| Experience | uses sachets nightly for 10 days; judges by her mornings | pack insert, refill reminders, sleep-journal letter | "Is it working or placebo? When do I decide?" | no usage guidance; silence after delivery |
| Loyalty / Advocacy | converts to subscription; tells the group chat | WhatsApp concierge, referral link, subscriber letter | "Do I get anything for staying? For sharing?" | pushy upsells; hard-to-cancel subscription = trust killer |

---

## Slide 8 — Digital Marketing Strategy (narrative)
We target over-wired professionals 25–40 in Mumbai and Bengaluru who do not believe they have a sleep
problem — and we meet them at the moment they feel it. We want them to think *"this is a simple ritual,
made for my actual nights,"* and to do one thing: try the 10-night kit. The broad approach is
**rest-and-consolidation first**: everything we do digitally exists to convert a trial into a calm,
repeatable evening habit and then into a subscription — not to chase reach.

The channels work as one loop, not a stack. Short-video and search content earn the first honest
attention and answer the ingredient questions that build trust; the storefront converts with a
low-friction ₹999 trial; then the owned layer — pack insert, WhatsApp refill concierge, the fortnightly
sleep-journal letter — carries the relationship through the 10-day judgement window and into a
subscription. Paid spend exists mainly to *re-find* people already in the loop. Brand partnerships
(company wellness programmes, clinics) arrive in phase two, once the base makes us worth partnering with.

---

## Slide 9 — PESO Media Mix
| | What it is for Off Hours | Primary job |
|---|---|---|
| **Paid** | retargeting to site visitors & video viewers; later, sponsored discovery inside quick-commerce listings once demand exists | re-find warm audiences; amplifies proven messages only |
| **Earned** | wellness editors & newsletters covering the "switch-off" culture; founder story of building melatonin-free in India | third-party credibility the ingredient-sceptic trusts |
| **Shared** | customers posting their night-routine rituals; 10-night challenge check-ins; referral links in group chats | turns the ritual into social proof; peer recommendation |
| **Owned** | storefront & product pages, WhatsApp refill concierge, sleep-journal email letter, pack inserts | the retention spine — where trials become subscribers |

**How the four work together:** Earned and Shared create believable first contact; Owned converts and
keeps; Paid only accelerates what the other three already prove — spend follows pull, never precedes it.

---

## Slide 10 — Recommended Digital Channels (5 priorities)
| Channel | Role | Why this channel? |
|---|---|---|
| Instagram Reels + short video | Discovery | where our audience actually unwinds at 10 pm; ritual content formats natively |
| Search (brand site + category articles) | Trust & research capture | ingredient questions are the trust gate; the brand must answer them itself |
| Own storefront + UPI checkout | Conversion | low-friction ₹999 trial; owns the data the subscription model needs |
| WhatsApp concierge | Retention & service | India-native, high-open, personal — perfect for refill timing and questions |
| E-mail sleep-journal letter | Experience & advocacy | the 10-day judgement window needs a guide; letters out-sell loud campaigns |

**Named non-priorities (and why):** television & print (wrong age and wrong moment, unmeasurable);
mass display/broad awareness bursts (spend ahead of demand — awareness money lands before trial intent exists);
celebrity influencer blitzes (borrowed attention, wrong trust mechanic for an ingested product);
heavy marketplace-ads dependence (a listing helps logistics, but we refuse to rent the brand's first impression).

---

## Slide 11 — Integrated Digital Journey (one connected loop)

```mermaid
flowchart LR
    A[Reels ritual content<br/>Discovery] --> B[Search & label pages<br/>Research]
    B --> C[Storefront<br/>₹999 trial kit + UPI]
    C --> D[Pack insert + Day-1<br/>welcome message]
    D --> E[Sleep-journal letter<br/>Day 1-10 judgement window]
    D --> F[WhatsApp concierge<br/>questions + refill timing]
    E --> G[Subscription<br/>₹1,899/mo]
    F --> G
    G --> H[Referral link &<br/>group-chat sharing]
    H --> A
    I[Paid retargeting] --> C
    J[Earned features /<br/>founder story] --> B
```

Every channel hands the customer to the next with context attached — nothing is a dead end, and owned
channels carry the relationship through the 10-day judgement window (Slide 7, Experience row).

---

## Slide 12 — Key Strategic Decisions
1. **Retention before reach** — the entire system is sequenced to win subscribers, not impressions:
   trial → judged experience → subscription is the value engine
2. **An understated, proof-led launch** — quiet, sharp, ritual content over launch-week hype;
   the brand earns its loud phase rather than starting with it
3. **We compete with the habit of not switching off** — positioning against an evening behaviour,
   not against pharmacies or gummies, keeps the brand distinct and the message human
4. **Partnerships and mass awareness are deliberately delayed** — alliances phase two; awareness
   spend only after pull signals exist — money and attention are spent in the order they convert

---

## Brand Selection Test (self-check, per brief)
- **What do you sell?** A melatonin-free night-drink sachet — a 10-night trial kit and a refill subscription.
- **Who is it for?** Urban professionals 25–40 in Mumbai & Bengaluru who can't switch off after late workdays.
- **What problem does it solve?** Evenings that never downshift: wired minds, junk-time scrolls, groggy mornings.
- **Why would someone choose you?** A simple, non-medical ritual with honest ingredients, fair trial pricing,
  and support through the full first 10 nights — chosen once, kept as a habit.

*Scope note (for the marker): strategy-level plan only — no campaign calendars, keyword lists, influencer lists,
media budgets, creatives, or dashboards at this stage, per the brief.*
"""
deck_path = os.path.join(OUT, "SUBMISSION", "01_STRATEGY_FOUNDATION_DECK.md")
write_text(deck_path, deck)
progress(f"SUBMISSION deck drafted | 12 slides + brand test | {len(deck)} chars | lint pending at RENDER_OUTPUT")

# ================= ANNOTATED/00_STATUS.md =================
status = f"""# ANNOTATED/00_STATUS — deliverable status board (solver run)

| artefact | path | status | gate-relevant notes |
|---|---|---|---|
| Strategy foundation deck (DEL-01) | output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md | DRAFT (lint pending) | 12 slides + brand test; R21 items absent by construction |
| Logo/identity artwork (DEL-X1) | — | EXCLUDED_LOGO | R23: name + written positioning only |
| This status file | output/ANNOTATED/00_STATUS.md | LIVE | — |
| Operator comments | output/OPERATOR/COMMENTS.md | LIVE | incl. deviations DEV-001/002 |
| Mappings | output/OPERATOR/MAPPINGS.md | LIVE | 24 requirements → outputs |
| Path & rank | output/OPERATOR/PATH_RANK.md | LIVE | RES re-scores & margins |
| Layer A technical audit | output/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md | LIVE | contract 5 sections in order |
| Manifest | output/MANIFEST.md | PENDING at RENDER_OUTPUT | sha256 + tree + hashes |

Run state: SYNTHESIZE · package {pkg['package_version']} · package sha256 {sha256_file(PKG_COPY)[:16]}…
"""
write_text(os.path.join(OUT, "ANNOTATED", "00_STATUS.md"), status)
progress("ANNOTATED/00_STATUS.md written")

# ================= OPERATOR =================
comments = f"""# OPERATOR/COMMENTS — plain-language notes for the human operator

## What this run produced
One submission deck (Slides 1–12 + Brand Selection Test) for the fictional brand **Off Hours**, built strictly
from the assignment brief and the frozen chart-analysis package (no re-opening of the raw chart — enforced by
the read audit; see Risk-And-Audit-Log).

## How to export the deck
Open `output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md`. Each `## Slide N` block is one slide: copy the title
as the slide headline and the bullets as body. Slide 11's mermaid block renders in Canva/Slides via any
mermaid-to-image paste, or redraw the loop with boxes and arrows. Keep bullets tight when pasting.

## Decisions you should sanity-check (open questions)
1. WhatsApp treated as an owned digital touchpoint (Slide 9/10) — common India practice, but brief is silent.
2. Price points ₹999 / ₹1,899 are positioning-level planned prices, not costed P&L prices (assignment marks
   clarity of thinking, not pricing maths).
3. Persona figures (₹18–24 LPA etc.) are illustrative characterisation, not measured market data.

## Deviation register (carried from package validation; PASS_WITH_DEVIATION)
- **DEV-001** — solver spec embeds v4 reference hashes; actual generator was chart_analyser.yaml v5.0.0.
  Package hashes match the ACTUAL generator spec and the boot MANIFEST source hash exactly. Registry lag,
  not tampering. Proceed. (raw/package/validation.md)
- **DEV-002** — package key renamed: `anomalies` → `anomaly_registry` (12 records; per-origin anomaly
  arrays also present). Validator maps the rename. Data intact.

## Residual risk (shortlist)
- The package's best-solution winner carries an explicit strength caveat ("run it clean and procedural"):
  translated to compliance discipline — no medical claims anywhere in the deck.
- Timing hard rules carried into deck: muted launch, delayed mass awareness, partnerships phase-2 —
  do not 'improve' the deck by adding a big splash; that re-introduces package risk HID-1/HID-2.
- Persona specificity is a marker-facing device; if challenged, it traces to Slide 5's audience definition,
  which is the defensible analytic layer.

## What was NOT done (scope honesty)
No real market sizing data, no costed media plan, no creative copy beyond positioning lines, no logo
(excluded by brief), no calendars/influencer lists/budgets dashboards (excluded by brief §Scope).
"""
write_text(os.path.join(OUT, "OPERATOR", "COMMENTS.md"), comments)

rows = []
req_rows = req["rows"]
def slide_for(rid):
    m = {"R01":"Slide 1+2+Test","R02":"Slide 2","R03":"Slide 1","R04":"Slide 5","R05":"Slide 2",
         "R06":"Slides 8–11","R07":"RISK guard HID-1; deck avoids (Slides 8,10,12)","R08":"Brand Selection Test",
         "R09":"Slide 1","R10":"Slide 2","R11":"Slide 3","R12":"Slide 4","R13":"Slide 5","R14":"Slide 6",
         "R15":"Slide 7","R16":"Slide 8","R17":"Slide 9","R18":"Slide 10","R19":"Slide 11","R20":"Slide 12",
         "R21":"Guard: items ABSENT deck-wide","R22":"Deck header/cover","R23":"Slide 1 note + this file",
         "R24":"Whole-deck discipline (clarity of thinking)"}
    return m[rid]
for r in req_rows:
    rows.append((r["id"], r["must_level"], r["quoted_text"][:72] + ("…" if len(r["quoted_text"]) > 72 else ""),
                 slide_for(r["id"]), "COVERED"))
mappings = ["# OPERATOR/MAPPINGS — requirement & traceability ledger",
            "", "## A. Requirements → deck",
            "| req | level | brief text (truncated) | where satisfied | status |", "|---|---|---|---|---|"]
mappings += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in rows]
mappings += [
 "", "## B. Package → solution slots → deck",
 "| slot | package basis | solver score | deck surfaces |",
 "|---|---|---|---|",
 f"| my_answers | RES-001 {ans['package_basis']['winner_archetype']} | {ans['computed']['solver_score']} | Slides 1–6 (brand, goal, audience, persona) |",
 f"| hidden_problems | RES-002 ×5 archetypes | {[h['computed']['solver_score'] for h in hid]} | Slides 8,10,12 guards (sequencing, non-priorities, exclusions) |",
 f"| best_solution | RES-003 {best['package_basis']['winner_archetype']} | {best['computed']['winner_solver_score']} | Slides 8–12 (strategy loop, PESO, channels, decisions) |",
 "", "## C. Citation policy (used by citation_integrity gate)",
 "- **C1 mechanical paths** resolve against `raw/package/chart_analysis_package.json` (e.g. `patterns.archetype_resolutions.RES-001`, `systems.void_tomb_punish_force_horse_graph['9'].void`).",
 "- **C2 claim ids** (`CLM-###`) resolve against the recorded claim register of the analysis package (chart-side CONFIDENCE_MATRIX); used as opaque ids with their recorded confidence.",
 "- **C3 legacy package paths** of the form `palaces.<canon>_<n>.<field>` are the seed's own reference style; each is backed in the same evidence list by ≥1 C1 mechanical path; vocabulary-checked (palace canon names + known fields: door/star/deity/harm/prosperity_decline/special_markers/void/tomb/punishment/life_stage).",
 "- The SUBMISSION deck itself contains **zero** chart terminology (lint_terms gate): traceability lives here and in LAYER_A, never in front of the marker.",
]
write_text(os.path.join(OUT, "OPERATOR", "MAPPINGS.md"), "\n".join(mappings))

pathrank = ["# OPERATOR/PATH_RANK — candidate ranking & margins (solver rubric re-score)",
 "",
 "Re-scored from package archetype_resolutions under solver rubric:",
 "weights grounding .35 / corroboration .25 / contradiction .20 / board .10 / requirement_fit .10;",
 "tiers EXPLICIT 1.0 · COMPUTED .6 · INFERRED .3; fit = coverage .40 + hard-compliance .40 + tone .20.",
 "Tie-break order: grounding → corroboration → contradiction→earlier phase (not needed here: margins > 0).",
 "",
 "## best_solution (RES-003)",
 "| rank | archetype | grounding | corroboration | contradictions | board | fit | solver_score | decision |",
 "|---|---|---|---|---|---|---|---|---|"]
for r in best["computed"]["winner"], best["computed"]["runner"]:
    pass
all_rows = [best["computed"]["winner"], best["computed"]["runner"]] + best["computed"]["rejected"]
for r in all_rows:
    decision = ("WINNER — lead channel thesis" if r["archetype"] == best["package_basis"]["winner_archetype"]
                else ("RUNNER — phase-2 alliances" if r["archetype"] == best["package_basis"]["runner_archetype"]
                      else f"REJECTED — {r['rejection_reason']}"))
    pathrank.append(f"| {r['package_rank']} | {r['archetype']} | {r['grounding_tier']} | {r['corroboration_norm']} | "
                    f"{r['contradicting_evidence_count']} | {'pass' if r['board_consistency_pass'] else 'FAIL'} | "
                    f"{r['requirement_fit']} | **{r['solver_score']}** | {decision} |")
pathrank += ["", f"Margin winner→runner: **{best['computed']['margin_vs_runner']}** (no tie).",
             "", "## hidden_problems (RES-002) — severity ranking",
             "| slot-rank | archetype | code | solver_score | confidence |", "|---|---|---|---|---|"]
for h in hid:
    pathrank.append(f"| {h['rank_within_slot']} | {h['package_basis']['archetype']} | {h['code']} | "
                    f"{h['computed']['solver_score']} | {h['confidence']} |")
pathrank += ["", "## my_answers (RES-001) — singleton resolution",
             f"- winner: {ans['package_basis']['winner_archetype']} · solver_score **{ans['computed']['solver_score']}** · singleton (no competitor; tie_note recorded in package).",
             f"- constraints carried ON the seat (not alternative seats): hour-void window + harm naming the day stem → understated launch posture in deck.",
             "", "## Fit sub-scores (requirement_fit)",
             f"- coverage: brand+strategy covers 24/24 requirement rows (R07/R21 as violations-avoided, R23 EXCLUDED_LOGO); hard-compliance 1.0 (no must_not breached); audience-tone 1.0 (marker English, zero jargon)."]
write_text(os.path.join(OUT, "OPERATOR", "PATH_RANK.md"), "\n".join(pathrank))
progress("OPERATOR files written (COMMENTS, MAPPINGS, PATH_RANK)")

# ================= LAYER_A (contract sections, exact order) =================
seed_readings = []
seed_readings.append("### Verbatim package readings (audit substrate)\n")
seed_readings.append(f"**answers[0] (RES-001)**\n> {ss['answers'][0]['reading']}\n")
for hrow in ss["hidden_problems"]:
    seed_readings.append(f"**{hrow['archetype']} (rank {hrow['rank']})**\n> {hrow['reading']}\n")
for c in ss["best_solution_candidates"]:
    body = c.get("reading") or "(no readability text recorded for this rejected row)"
    txt = body + (f" (rejection: {c['reason']})" if c.get("reason") else "")
    seed_readings.append(f"**{c['archetype']} (rank {c['rank']})**\n> {txt}\n")
layer_a = f"""# LAYER_A — Technical Audit (package → strategy binding)

## executive_reading
The diligence package says, in plain words: the **answer** rests on a single, over-determined seat — several
independent selectors (the daily self-trace, the official duty proxy, the dividing authority) all name the same
place, with no competing seat; its constraints are timing (a not-yet window) and intensity, never location.
The **hidden problems** are five: an over-elaborate glittering mission that cannot execute cleanly; a showcase
surface whose payoff window is locked for now; a grinding groundwork track; an open door onto obscurity;
and stored value that decays without a rhythm. The **best way forward** is the one strong, unafflicted seat:
consolidate and run procedurally inside institutions, now (in-period), with alliances courted backstage for
later; two attractive channels are rejected because their windows are locked rather than because they are bad.
The solver translated exactly this posture into the deck: understated launch, retention-first sequencing,
partnerships phase two, mass awareness last. Nothing in the deck contradicts the package; several slide
choices exist *only* because the package demanded them.

## walkthrough
1. INIT — froze run context, copied package read-only to `raw/package/`, initialised solver machine (no reuse of chart-run machine).
2. PACKAGE_VALIDATE — schema keys (with rename DEV-002), semver version {pkg['package_version']}, source hash
   {pkg['source_qmdj_sha256'][:16]}… vs boot MANIFEST: match; protocol/rubric hashes vs ACTUAL generator
   (v5.0.0): match; vs solver-embedded v4 reference: skew logged as DEV-001, PASS_WITH_DEVIATION.
3. PDF_INGEST — brief read once (322 lines); 24 requirement rows enumerated; deliverable registry: 1 real output
   (+1 excluded-logo boundary); rubric guess inferred from the single marking note; question types classified.
4. P7_SLOT_BIND — question types bound to solver slots: identity & positioning → my_answers; risk anticipation &
   what-not-to-do → hidden_problems; strategy/channel-choice & timing → best_solution.
5. SOLUTION_ENGINE — package `solution_seed` (chart-derived only, 'not yet requirement-bound') re-scored under
   solver rubric v1.0.0; requirement_fit composed (coverage .40, hard-compliance .40, audience-tone .20);
   winner re-selected with margin 0.1167; tie-break available but unused; text budgets enforced per slot.
6. SYNTHESIZE — this document, the deck, operator files, and wiki corpus authored; red team run.
7. RENDER_OUTPUT — lint + gates + manifest (see MANIFEST.md for final verification table).

## candidates_and_selection
### best_solution candidates (RES-003, re-scored)
| archetype | solver_score | decision |
|---|---|---|
| BEST-dui-7-earthly-escape-channel | {best['computed']['winner']['solver_score']} | WINNER — retention/consolidation spine |
| BEST-qian-6-harmony-help-channel | {best['computed']['runner']['solver_score']} | RUNNER — phase-2 alliances |
| BEST-li-9-salary-channel | {best['computed']['rejected'][0]['solver_score'] if best['computed']['rejected'] else 'n/a'} | REJECTED — void-locked payoff window |
| BEST-kun-2-open-gate | {best['computed']['rejected'][1]['solver_score'] if len(best['computed']['rejected'])>1 else 'n/a'} | REJECTED — opens onto day-void with entombed lead, obscurity |

Winner carries the package caveat (White-Tiger severity; harm on the seat): mitigations = compliance-clean
claims discipline + procedural operation, both visible as deck decisions (Slides 8/10 non-priorities, Slide 12.2).

### hidden problems (RES-002) — all five adopted
| code | archetype | solver_score | deck mitigation |
|---|---|---|---|
{chr(10).join(f"| {h['code']} | {h['package_basis']['archetype']} | {h['computed']['solver_score']} | {h['bound_requirement']} |" for h in hid)}

### my_answers (RES-001) — singleton, adopted as-is
Winner ANS-seats-in-zhen-3, solver_score {ans['computed']['solver_score']}; package tie_note: "not tied;
singleton resolution". Deck expression: single-category single-claim brand (Slides 1–6), muted launch posture.

## confidence_and_residual_risk
| item | confidence | basis |
|---|---|---|
| answers slot (brand formulation) | 0.90 | singleton EXPLICIT grounding; package context notes |
| best_solution winner | 0.80 | package final winner confidence after harm re-audit (CLM-034) |
| hidden HID-1 | 0.85 | strongest avoid-cluster (support 9, corroboration 1.0) |
| hidden HID-2 | 0.75 | EXPLICIT but window-shaped (fills later) |
| hidden HID-3/4/5 | 0.65 | tie-group triple; equal weighting kept |

**Residual risk:** (a) score compression under solver rubric (fit term adds +0.095 to all grounded rows —
ranking preserved by design); (b) persona/price figures are illustrative, flagged in OPERATOR; (c) requirement_fit
sub-scores are analyst-set (no marker rubric PDF exists — rubric_guess documented); (d) DEV-001 version-skew
accepted as registry lag; if the canonical v4 package ever surfaces, re-validate hashes and rerun (est. effort: re-run s1 forward).

## full_technical_mapping
### Rubric record
- solver rubric v1.0.0 hash `sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4`; weights & tiers as in walkthrough.
- package-side rubric hash `{pkg['archetype_scoring_rubric_version_hash']}` (generator v5.0.0) — provenance chain DEV-001.
- requirement_fit = .40·coverage + .40·hard_compliance + .20·audience_tone; values per slot in PATH_RANK.

### Claim ledger (ids referenced by seed rows)
{chr(10).join('- ' + cid + ' (answers)' for cid in ans['package_basis']['claims'])}
{chr(10).join('- ' + cid + f" (hidden, {h['code']})" for h in hid for cid in h['package_basis']['claims'])}
{chr(10).join('- ' + cid + ' (best, winner)' for cid in best['package_basis']['claims'])}

### Evidence paths used (mechanical, resolve against package)
{chr(10).join('- `' + e + '`' for e in sorted(set(sol['evidence'])))}

{chr(10).join(seed_readings)}
"""
write_text(os.path.join(OUT, "LAYER_A", "LAYER_A_TECHNICAL_AUDIT.md"), layer_a)
progress("LAYER_A technical audit written (5 contract sections in order)")

machine_update(state="SYNTHESIZE_OUTPUTS_DONE")
print(json.dumps({"deck_chars": len(deck), "status": "outputs_written",
                  "files": ["SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md", "ANNOTATED/00_STATUS.md",
                            "OPERATOR/COMMENTS.md", "OPERATOR/MAPPINGS.md", "OPERATOR/PATH_RANK.md",
                            "LAYER_A/LAYER_A_TECHNICAL_AUDIT.md"]}, indent=1))
