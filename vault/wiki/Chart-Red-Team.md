---
id: "chart-red-team"
type: "article"
phase: "AUDIT"
batch: "—"
palace_ids: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
sources:
  - "raw/state/red_team.json"
  - "raw/state/package_gates.json"
updated: "2026-09-16T01:33:29Z"
status: "frozen"
---


# Chart Red Team

## Adversarial rederivation 1: Make Kun 2 (Open door Prosperous, Palace Generating Door) the best-solution winner instead of Dui 7
**Result: REJECTED**
- day-void branch Wei in-palace (palaces.kun_2.special_markers[0] + chart_info.void.day validated)
- heaven Gui explicitly entombed (palaces.kun_2.special_markers[1], validated at Wei)
- star Imprisoned/Discarded (palaces.kun_2.prosperity_decline.star_strength)
- Xuanwu deity obscurity (palaces.kun_2.deity)
- verdict effect: confirms RES-003 runner-down ranking; no evidence path supports a clean opening through Kun 2 in-window

## Adversarial rederivation 2: Declare Li 9 showcase auspicious because Scenery door is 'Prosperous' and sits its original palace
**Result: REJECTED with nuance**
- door prosperity token is real (palaces.li_9.prosperity_decline.door_strength) and was kept as a separate typed claim, not averaged
- but day-void Wu on the year-stacked palace (palaces.li_9.special_markers[0] + chart_info.ganzhi.year + chart_info.void.day) defeats landing in-window
- the explicit 'Palace Oppressing Door' contradicts computed geometry — kept as ANOMALOUS, cannot be used as support either way
- verdict effect: palace 9 remains a void-locked payoff channel (VETO with SEQUENCE to Wu day/hour), not an inversion

## Adversarial rederivation 3: Re-seat the answer away from Zhen 3 because the palace is hour-void and harm names the day stem
**Result: REJECTED**
- void and harm are constraints on timing/method, not alternative seats; both independent selectors (day-stem trace, duty proxy) hit only palace 3
- rule: a flawed seat is still the seat — no competing candidate found (recorded in RES-001)
- verdict effect: none; constraints already shipped as CONSTRAIN/WARN claims on RES-001

## Machine checks
- citation integrity: broken links = 0
- candidate contamination (requirement-fit / assignment leakage): 0 violations → PASS
- coverage contamination (claims citing uninventoryed paths): 0 → PASS
- anomaly suppression: 12 registry anomalies == 12 packaged → all visible → PASS

Overall red-team verdict: **PASS**