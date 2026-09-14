---
id: chart-red-team
type: audit
phase: AUDIT
batch: "-"
palace_ids: []
sources: ["raw/state/chart_analysis_package.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# Chart Red Team

Adversarial pass over this analysis. The goal is to break the package's own conclusions using only the package's own evidence. Two attacks partially succeeded and the conclusions were weakened accordingly rather than defended.

**Result: PASS**

## adversarial_rederivation - REJECTED

**Target:** AR-ANSWERS-01 winner (palace 9 is the subject)

**Attack:** Can the same evidence support 'palace 9 is NOT the subject'? Argument: palace 9 is void, so it is empty and therefore cannot be the subject; the real subject should be the strongest palace, 6 or 7.

Void means 'does not land', not 'is not the subject'. Four independent header fields - is_duty_palace, duty_star, duty_door and the lead-stem proxy Xin - all resolve to palace 9. Reassigning the subject to palace 6 or 7 would be a strength-based guess with no field pointing at it, which laws 7 and 11 forbid.

- `palaces.9.active_chart.status.is_duty_palace`
- `chart_config.duty_star`
- `chart_config.duty_door`
- `chart_config.lead_stem`

## adversarial_rederivation - PARTIALLY_SUCCEEDED

**Target:** AR-BEST-01 leading candidate (palace 8)

**Attack:** Can the same evidence support palace 6 instead? Argument: palace 6 has a Prosperous door AND a Prosperous palace AND a San Qi stem; palace 8 has only a Resting door and a Resting palace.

This attack lands. Palace 6 is genuinely stronger on door and palace strength, and the only thing separating them in the rubric is the extra contradiction from palace 6 being Bing's tomb. The resolution therefore does NOT discard palace 6: it is retained as a live co-candidate with an explicit margin note stating the flip condition. No single winner is asserted more strongly than the evidence allows.

- `palaces.6.active_chart.energy_state.door`
- `palaces.6.palace_stem_rules.stems_in_tomb`
- `palaces.8.active_chart.energy_state.door`

## adversarial_rederivation - PARTIALLY_SUCCEEDED

**Target:** Fu Yin stasis claim

**Attack:** Can the board be argued to be dynamic? Argument: palace 2 carries the horse star, which is movement.

The horse star is real and is recorded as a SEQUENCE verdict, not suppressed. But it sits in a void palace with the Death door, so it is movement without ground. The report states both, rather than resolving the tension by dropping one side.

- `palaces.2.active_chart.status.has_horse_star`
- `palaces.2.active_chart.status.is_void`
- `palaces.2.active_chart.door`

## citation_integrity - PASS

**Target:** every evidence.path in the package

630 paths resolved against the source chart; 0 broken. Paths that did not resolve (for example palaces.5.active_chart.door, which does not exist because the Centre has no door) were pruned rather than cited, in an earlier AUDIT_FIX cycle.

## candidate_contamination - PASS

**Target:** requirement_fit_score across all candidates

Every candidate carries requirement_fit_score = null and the rubric's requirement_fit weight contributes 0.0 to every score. No assignment text was read at any point; no file outside QMDJ/ADVERTISING/project_1.json and the two specification files was opened.

## overclaim_scan - PASS

**Target:** report language vs grounding tier

The report states explicitly that no explicit answer field exists and that all headlines are COMPUTED. The best-solution section opens by conceding no path is clean. The tie between palaces 6 and 8 is disclosed rather than hidden behind a single confident recommendation.

## Standing weaknesses

1. The palace 6 / palace 8 best-path tie is not resolvable from the chart. Any downstream consumer must decide inner vs outer before using either.
2. `door.forced` does not exist in this schema, so no forced-door analysis was possible. If the real export has that field, this analysis is incomplete on that axis.
3. Tian Yi is absent; Zhi Fu (Chief) was used as the nearest authority spirit. That is a substitution, and it is labelled as one rather than presented as equivalent.

## Sources

- `vault/raw/state/red_team.json`

