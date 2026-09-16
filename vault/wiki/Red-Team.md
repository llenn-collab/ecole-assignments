---
id: "red-team"
type: "red-team"
state: "SYNTHESIZE"
updated: "2026-09-16T03:00:06Z"
---

# Red Team — adversarial review of the SUBMISSION deck

## Findings & fixes (applied to deck in this stage)
| id | severity | probe | finding → fix | status |
|---|---|---|---|---|
| RT-F1 | high | Do the SMART objectives actually reach the Slide 3 goal? | Old objective-1 (400 trials total @12% → 48 subscribers) cannot produce 1,000 households in 12 months — arithmetic gap a marker would catch instantly. → Objective 1 rewritten as a sustained run-rate (≥600 trials/mo by M6, ≥12%→30d conversion, ≥90 new subs/mo), compounding to 1,000 at M12. | FIXED |
| RT-F2 | medium | Is WhatsApp defensibly 'Owned' in PESO (spam risk if unconsented)? | Owned-media claim for WhatsApp only holds if the channel is opt-in; otherwise it is intrusive CRM and contradicts the persona's anti-spam stance. → Marked '(opt-in)' / 'user-consented' on Slides 9 and 10. | FIXED |
| RT-F3 | low | 'Founder story' — of whom, for a fictional brand? | A named-human founder was never defined; a marker could ask whose story is being told. → Reworded to 'the brand's founding narrative' — the fictional founder assumption stays documented in OPERATOR/COMMENTS. | FIXED |

## Probe sweep (all evaluated)
- R21 exclusion sweep — no calendars, influencer lists, SEO keyword plans, budgets, email journey maps, creatives, dashboards anywhere in deck: PASS (terms appear only in the scope-note as excluded).
- R07 avoid-list — brand is one category, realistic tech, not alcohol, not a major-brand copy, defined consumer: PASS.
- Slide 3 is a business goal (customer base, revenue base), not a marketing activity: PASS after F1.
- Slide 8 is two narrative paragraphs, not a platform list: PASS.
- No invented market statistics, no household-size claims, no fake percentages (all numbers are planned prices/targets): PASS.
- Persona trace: every persona attribute consistent with Slide 5 audience definition: PASS (age, income band, city, behaviour).
- Non-priority platforms justified, per R18: PASS (4 named with reasons).
- Brand Selection Test four questions answered distinctly: PASS.
- Forbidden-terminology lint (chart lexicon) — zero hits (re-verified at RENDER_OUTPUT): PENDING->verified at s4.
- Dead-end check — every Slide 11 node hands off with context: PASS.

Method: marker-simulation + arithmetic audit + exclusion sweep + traceability spot-checks against
OPERATOR/MAPPINGS and the five hidden-problem guards.
