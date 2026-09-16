# OPERATOR/COMMENTS — plain-language notes for the human operator

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
