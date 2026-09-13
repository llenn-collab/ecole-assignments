---
id: moc
type: moc
palace_ids: []
phase: PACKAGE_RENDER
batch: -
sources: ["raw/QMDJ.json", "raw/state/chart_analysis_package.json"]
updated: 1970-01-01T00:00:00Z
status: frozen
---

# MOC - Carpathia QMDJ Chart Analysis

Run `carpathia-adv-p1-0001` | source sha256 `083a393c855730e9...` | package `4.0.0`

## Articles

- [[Chart-Schema]] - how this export was bound
- [[Chart-Anatomy]] - pillars, season, duty, void, horse, origin sets
- [[Chart-Working-Copy]] - the flattened live board
- [[Chart-Board-Synthesis]] - systems, matrices, Centre reconstitution
- [[Chart-Patterns]] - computed pattern catalog
- [[Chart-Analysis-Report]] - the report
- [[Chart-Red-Team]] - adversarial re-derivation
- [[Palace-Analysis-Index]] - index of palace cards

## Palace cards

- [[Palace-1-Kan]]
- [[Palace-2-Kun]]
- [[Palace-3-Zhen]]
- [[Palace-4-Xun]]
- [[Palace-5-Center]]
- [[Palace-6-Qian]]
- [[Palace-7-Dui]]
- [[Palace-8-Gen]]
- [[Palace-9-Li]]

## State files

- `raw/state/chart_analysis_package.json` - the deliverable package
- `raw/state/solution_seed.json` - chart-derived seeds, not requirement-bound
- `raw/state/archetype_resolutions.json` - scored candidate resolutions
- `raw/state/anomalies.json` - anomaly log

## Dependencies

All articles depend on `palace:1@rev1` through `palace:9@rev1` and on `solution_seed@rev43`.

