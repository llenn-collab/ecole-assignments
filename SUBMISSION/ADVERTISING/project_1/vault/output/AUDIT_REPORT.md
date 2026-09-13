# AUDIT REPORT

Ironclad Post-Mortem & Integrity Auditor. Hostile pass over the Prompt 1 chart analyst's output. The auditor does not trust the worker's wiki notes, summaries or self-reported verification block; every check below was independently recomputed from `vault/raw/QMDJ.json` and `vault/raw/state/MANIFEST.json`.

## Final verdict: **PASS (SCOPED: CHART-ONLY, PDF GATES NOT RUN)**

The chart-analysis package is released. **Scope limit, stated plainly:** this is a PASS for a chart-only, assignment-blind package. It is not, and cannot be, a PASS for an assignment submission - no assignment was available and the PDF-anchored gates were not run. See Gate 0b.

## Gate results

| gate | name | outcome |
|---|---|---|
| 0 | Input Presence | **PASS** |
| 0b | Assignment Input (PDF-dependent gates) | **NOT_RUN** |
| 1 | Integrity Check | **PASS** |
| 2 | Traceability Matrix | **PASS** |
| 3 | Confidence Layering | **PASS** |
| 4 | Adversarial Omission Attack | **PASS** |
| 5 | Field Coverage | **PASS** |

### Gate 0 - Input Presence: PASS

QMDJ.json, package and MANIFEST.json all present and readable; 19 submission-layer files found.

### Gate 0b - Assignment Input (PDF-dependent gates): NOT_RUN

vault/raw/Assignment.pdf does not exist. The audited worker is the Prompt 1 chart analyst, which is assignment-blind by law (laws 4 and 21) and is forbidden to read an assignment. Therefore every PDF-anchored requirement of this skill - PDF traceability roots, PDF hard-constraint scanning, and 1.0 EXPLICIT scoring by PDF quotation - CANNOT be executed and is recorded as NOT_RUN. It is not recorded as passed. Any assignment-bound submission built on this package MUST be re-audited with the PDF present before release.

### Gate 1 - Integrity Check: PASS

The chart in the vault is byte-identical to the manifest entry and to the repository source of record. Package sha256 59ddb7eab387461f63d35ca0610a26e1f06d0c89fe9a7c3dfddfa3ba1fc6a466.

- `computed sha256(vault/raw/QMDJ.json) = 083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`
- `MANIFEST.source_qmdj_sha256 = 083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`
- `sha256(QMDJ/ADVERTISING/project_1.json) = 083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`

### Gate 2 - Traceability Matrix: PASS

All 126 audited elements (verdicts, archetype resolutions, seed items and pattern hits) resolve to at least one live JSON path in QMDJ.json. Independently re-resolved by the auditor against the raw file, not trusting the worker's own verification block.

### Gate 3 - Confidence Layering: PASS

29 claims scored. 0 ungrounded. No core strategic claim scores below 0.8 without an operator warning. Note that the auditor DOWNGRADED every headline from 1.0 to 0.8: the worker's EXPLICIT tier refers to chart marker fields, but this chart contains no explicit answer slot, so nothing here is a direct quotation. The report states this limitation in its own words, which satisfies the operator-warning requirement.

### Gate 4 - Adversarial Omission Attack: PASS

17 high-impact chart features were independently extracted from the raw file and every one is addressed in the package. The two most dangerous - the day stem's only seat being a void Death-door palace, and the best-scoring route being the day stem's own tomb - are both explicitly disclosed in the report. No vetoed candidate survived into a live recommendation.

### Gate 5 - Field Coverage: PASS

The auditor independently enumerated 242 leaf paths in the raw chart and confirmed every one is cited in the package. All 10 full-coverage subsystems are present and populated. Nothing in the source file is left unread.

## Integrity evidence

- Source of record: `QMDJ/ADVERTISING/project_1.json`
- sha256: `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`
- Vault copy `vault/raw/QMDJ.json`: identical
- Package sha256: `59ddb7eab387461f63d35ca0610a26e1f06d0c89fe9a7c3dfddfa3ba1fc6a466`
- Files hashed in manifest: 58
- Determinism check (origin_sets re-derived): IDENTICAL

## Traceability summary

- Every verdict, archetype resolution, seed item and pattern hit was re-resolved against the raw chart by the auditor.
- Broken links found by the auditor: **0**.
- The worker's own earlier run had 18 broken paths (fields such as `palaces.5.active_chart.door`, which do not exist because the Centre has no door). Those were caught by its own gate and pruned before HALT. The auditor confirms they are gone.

## Field coverage

- Leaf paths in source: 242
- Cited in package: 242
- Uncited: **0**

Independently recomputed by the auditor from the raw file, not read from the worker's verification block. The worker's first run left 98 of 242 paths unread; that gap is now closed and Gate 5 enforces it.

## Confidence summary

- Claims scored: 29
- At 1.0 EXPLICIT: **0** - correct, because this chart has no explicit answer slot.
- At 0.8 COMPUTED: 17
- At 0.5 INFERRED: 0
- At 0.0 UNGROUNDED: 0

The auditor downgraded every headline the worker tiered as EXPLICIT down to 0.8. The worker's EXPLICIT tier refers to chart *marker* fields such as `is_duty_palace`, which is legitimate, but this skill reserves 1.0 for a direct quotation or an explicit metadata answer field. No such field exists here. The worker disclosed this limitation itself, which is why the downgrade does not trigger WEAK_FOUNDATION.

## Omission findings

17 high-impact chart features were independently extracted from the raw file and every one is addressed in the package. The two most dangerous - the day stem's only seat being a void Death-door palace, and the best-scoring route being the day stem's own tomb - are both explicitly disclosed in the report. No vetoed candidate survived into a live recommendation.

Specifically hunted and found present: empty centre and its lodging graph; the `center_guest` corroboration at palace 2; stacked Wu branches on the void duty palace; all three void palaces; all four afflicted palaces; both Dead doors; the horse star; and the tomb-of-Bing trap sitting on the highest-scoring solution path.

## Remediation pointers

None required for the audited scope. Two standing conditions before any assignment-bound reuse of this package:

1. The palace 6 / palace 8 best-path split is unresolved by design. A downstream consumer must supply the inner/outer determination; it must not be guessed.
2. This audit must be re-run with the assignment present before any submission derived from this package is released. Gate 0b was NOT RUN, not passed.

---

*The auditor did not rewrite, repair, or add strategic content to the submission.*

