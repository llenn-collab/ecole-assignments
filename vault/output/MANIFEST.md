# MANIFEST — solver run deliverables & verification

- generated_at: 2026-09-16T03:00:06Z
- machine_state: HALT (solver) · prompt-1 machine: raw/state/machine.json (HALT, preserved)
- package_version: 5.0.0
- package sha256 (copy, integrity-verified): 4e906b0f47d1c4dfb90c8ad3c93dadac095622558e7c5e6eb441cdb40f3b1a37
- source chart hash (from boot MANIFEST, never re-opened): 2f165e078a7c21700e5f1a1f8e44862ddcdd8f04078b733cf9c477dfb9cbcafb
- interpretation protocol hash (package/generator v5.0.0): sha256:protocol_v2_2_2_0_chart_analyst_v5
- package rubric hash (generator v5.0.0): sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5
- solver rubric hash (v1.0.0): sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4
- deviation register: DEV-001 (v4-vs-v5 registry skew), DEV-002 (anomalies→anomaly_registry) — both PASS_WITH_DEVIATION

## Gate results
| gate | result | detail |
|---|---|---|
| lint_terms | PASS | {"scope": "SUBMISSION/** (per forbidden_terms.txt header)", "violations": {}, "informational_out_of_scope_sweep": {"output/OPERATOR/MAPPINGS.md": [["palace", "w |
| no_qmdj_read | PASS | {"bad": [], "total_reads": 111} |
| package_schema | PASS | {"renames": ["anomalies -> anomaly_registry"]} |
| package_integrity | PASS | {"copy_sha256": "4e906b0f47d1c4dfb90c8ad3c93dadac095622558e7c5e6eb441cdb40f3b1a37"} |
| citation_integrity | PASS | {"unresolved": [], "missing_claims": [], "c3_bad": [], "claims_known": 34} |
| coverage | PASS | {"uncovered": [], "total": 24} |
| archetype_resolution_presence | PASS | {"have": ["RES-001", "RES-002", "RES-003"]} |
| layer_a_contract | PASS | {"indices": [58, 1219, 2581, 4008, 4959]} |
| red_team_applied | PASS | {} |

## Files (sha256)
| file | sha256 | bytes | requirement_ids |
|---|---|---|---|
| output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md | 7b93816445b23d8a48e50e0b… | 13031 | 24 ids |
| output/ANNOTATED/00_STATUS.md | 2ba97b06703745411e7b910b… | 991 | 1 ids |
| output/OPERATOR/COMMENTS.md | 98a121e33e231e53644c95dd… | 2446 | 2 ids |
| output/OPERATOR/MAPPINGS.md | eede4b075cfc02c66cedd457… | 4303 | 24 ids |
| output/OPERATOR/PATH_RANK.md | 6c066b0efb8f537dde60d6e2… | 2279 | 1 ids |
| output/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md | 708327720e540985b4da1545… | 9135 | 24 ids |
| wiki/Assignment-Brief.md | a4e4dd2592d932724ce6c5ef… | 1555 | 0 ids |
| wiki/Assignment-Corpus.md | b222c9d376748b53957aea38… | 4394 | 0 ids |
| wiki/Requirements-Matrix.md | 887449030efffd1c6a25f1e4… | 2227 | 0 ids |
| wiki/Rubric-Guess.md | 45eb0010ff225983c8370bc7… | 868 | 0 ids |
| wiki/Logo-Boundary.md | 7fae77bff608e763e48222dd… | 734 | 0 ids |
| wiki/Constraints-And-Deliverables.md | 84a45e0ac3d5cc375b8a29be… | 1205 | 0 ids |
| wiki/Hidden-Problems.md | 4f71625926066c8babc6b598… | 1786 | 0 ids |
| wiki/Solution-Architecture.md | 6ebddb8b718edc542bce4679… | 1415 | 0 ids |
| wiki/Solution-Live.md | 22ff435278b7f693acb6c995… | 839 | 0 ids |
| wiki/Recommended-Answers.md | 5b95f20eccfcaa27b44a414d… | 3182 | 0 ids |
| wiki/Risk-And-Audit-Log.md | 8369abc58377d7dc88b31d70… | 1309 | 0 ids |
| wiki/Red-Team.md | 9555fab63e9a8fba6918a9c5… | 2521 | 0 ids |
| wiki/MOC.md | 08166e95e484848400018aa2… | 2110 | 0 ids |
| raw/package/validation.md | 440bf191cb8acec58b4073af… | 2486 | 0 ids |
| raw/assignment/extract.md | c79e5dc3d4a3edfa9d3af60b… | 7866 | 24 ids |

## Tree (vault/output)
```
vault/
output/
  AUDIT_REPORT.md
  AUDIT_RUN1.json
  CONFIDENCE_MATRIX.json
  MANIFEST.md
  VETO_LOG.md
  SUBMISSION/
    01_STRATEGY_FOUNDATION_DECK.md
  ANNOTATED/
    00_STATUS.md
  OPERATOR/
    COMMENTS.md
    MAPPINGS.md
    PATH_RANK.md
  LAYER_A/
    LAYER_A_TECHNICAL_AUDIT.md
```

## Full hashes
```json
[
 {
  "path": "output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md",
  "sha256": "7b93816445b23d8a48e50e0b66fa5b89d261b6a97c03559ac31011bd91ff0214",
  "bytes": 13031,
  "requirement_ids": [
   "R01",
   "R02",
   "R03",
   "R04",
   "R05",
   "R06",
   "R07",
   "R08",
   "R09",
   "R10",
   "R11",
   "R12",
   "R13",
   "R14",
   "R15",
   "R16",
   "R17",
   "R18",
   "R19",
   "R20",
   "R21",
   "R22",
   "R23",
   "R24"
  ]
 },
 {
  "path": "output/ANNOTATED/00_STATUS.md",
  "sha256": "2ba97b06703745411e7b910babe65950b6d9287c35ec935e972d42e29026cc6e",
  "bytes": 991,
  "requirement_ids": [
   "R22"
  ]
 },
 {
  "path": "output/OPERATOR/COMMENTS.md",
  "sha256": "98a121e33e231e53644c95dd608f6b6176177b8a001b9aecd64b2d6a41fea752",
  "bytes": 2446,
  "requirement_ids": [
   "R22",
   "R24"
  ]
 },
 {
  "path": "output/OPERATOR/MAPPINGS.md",
  "sha256": "eede4b075cfc02c66cedd457d5dc7f68ddec552cd2a04020ef5485b968dc7bc9",
  "bytes": 4303,
  "requirement_ids": [
   "R01",
   "R02",
   "R03",
   "R04",
   "R05",
   "R06",
   "R07",
   "R08",
   "R09",
   "R10",
   "R11",
   "R12",
   "R13",
   "R14",
   "R15",
   "R16",
   "R17",
   "R18",
   "R19",
   "R20",
   "R21",
   "R22",
   "R23",
   "R24"
  ]
 },
 {
  "path": "output/OPERATOR/PATH_RANK.md",
  "sha256": "6c066b0efb8f537dde60d6e2fd81e4626dad5f22f97625359da584bc82fa79d6",
  "bytes": 2279,
  "requirement_ids": [
   "R24"
  ]
 },
 {
  "path": "output/LAYER_A/LAYER_A_TECHNICAL_AUDIT.md",
  "sha256": "708327720e540985b4da154540e62e72d3f7d2d84626308300631eb30ca8d0c0",
  "bytes": 9135,
  "requirement_ids": [
   "R01",
   "R02",
   "R03",
   "R04",
   "R05",
   "R06",
   "R07",
   "R08",
   "R09",
   "R10",
   "R11",
   "R12",
   "R13",
   "R14",
   "R15",
   "R16",
   "R17",
   "R18",
   "R19",
   "R20",
   "R21",
   "R22",
   "R23",
   "R24"
  ]
 },
 {
  "path": "wiki/Assignment-Brief.md",
  "sha256": "a4e4dd2592d932724ce6c5ef1a46a4e8398866f920e86183c79edf64ec6e158b",
  "bytes": 1555,
  "requirement_ids": []
 },
 {
  "path": "wiki/Assignment-Corpus.md",
  "sha256": "b222c9d376748b53957aea3807291e802a2a68aa8ab6e1e933169db368cc3aa2",
  "bytes": 4394,
  "requirement_ids": []
 },
 {
  "path": "wiki/Requirements-Matrix.md",
  "sha256": "887449030efffd1c6a25f1e43919ff953c4a41bf44ed651bba0d11ab5073bb34",
  "bytes": 2227,
  "requirement_ids": []
 },
 {
  "path": "wiki/Rubric-Guess.md",
  "sha256": "45eb0010ff225983c8370bc7edf317ae14c1243cf7e21aac84d541e09a025a75",
  "bytes": 868,
  "requirement_ids": []
 },
 {
  "path": "wiki/Logo-Boundary.md",
  "sha256": "7fae77bff608e763e48222dd14f1c2469dbd22cdd1bf23ec3bdb712126c7104d",
  "bytes": 734,
  "requirement_ids": []
 },
 {
  "path": "wiki/Constraints-And-Deliverables.md",
  "sha256": "84a45e0ac3d5cc375b8a29be5abf1cc41f45b2cb6a46af7325f266593db711d2",
  "bytes": 1205,
  "requirement_ids": []
 },
 {
  "path": "wiki/Hidden-Problems.md",
  "sha256": "4f71625926066c8babc6b59873a4b545cfecf6db91ead748c803707361989dec",
  "bytes": 1786,
  "requirement_ids": []
 },
 {
  "path": "wiki/Solution-Architecture.md",
  "sha256": "6ebddb8b718edc542bce467960f43cddac10fc50b000ce294f204c7dc0167563",
  "bytes": 1415,
  "requirement_ids": []
 },
 {
  "path": "wiki/Solution-Live.md",
  "sha256": "22ff435278b7f693acb6c995b8bb46ba818442791f8cdfed904eec6f59e60208",
  "bytes": 839,
  "requirement_ids": []
 },
 {
  "path": "wiki/Recommended-Answers.md",
  "sha256": "5b95f20eccfcaa27b44a414d3f385956cee5d57df07dee323d768cc558ee8f8f",
  "bytes": 3182,
  "requirement_ids": []
 },
 {
  "path": "wiki/Risk-And-Audit-Log.md",
  "sha256": "8369abc58377d7dc88b31d709e07fc636e91210157760e4e0e6df884371ef6c0",
  "bytes": 1309,
  "requirement_ids": []
 },
 {
  "path": "wiki/Red-Team.md",
  "sha256": "9555fab63e9a8fba6918a9c5c3be8a2ae401f93785e74695610d38e4ceb43d8d",
  "bytes": 2521,
  "requirement_ids": []
 },
 {
  "path": "wiki/MOC.md",
  "sha256": "08166e95e484848400018aa27f956da5e31e1fd08427c6f8050a9f9221803b19",
  "bytes": 2110,
  "requirement_ids": []
 },
 {
  "path": "raw/package/validation.md",
  "sha256": "440bf191cb8acec58b4073afba085531a7d88e36863f0aaa1926aacd660db063",
  "bytes": 2486,
  "requirement_ids": []
 },
 {
  "path": "raw/assignment/extract.md",
  "sha256": "c79e5dc3d4a3edfa9d3af60b80295413b96dfd060f6301379fef0e1315ef2c35",
  "bytes": 7866,
  "requirement_ids": [
   "R01",
   "R02",
   "R03",
   "R04",
   "R05",
   "R06",
   "R07",
   "R08",
   "R09",
   "R10",
   "R11",
   "R12",
   "R13",
   "R14",
   "R15",
   "R16",
   "R17",
   "R18",
   "R19",
   "R20",
   "R21",
   "R22",
   "R23",
   "R24"
  ]
 }
]
```
