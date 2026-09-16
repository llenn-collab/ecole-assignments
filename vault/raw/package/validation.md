# Package Validation (PACKAGE_VALIDATE)

- package copy: `vault/raw/package/chart_analysis_package.json` sha256 `4e906b0f47d1c4dfb90c8ad3c93dadac095622558e7c5e6eb441cdb40f3b1a37`
- schema_valid: True · hashes_verified(generator-spec provenance): True
- gate result: **PASS_WITH_DEVIATION**

| # | check | pass | deviation/detail |
|---|---|---|---|
| 1 | package exists and readable | ✅ |   |
| 2 | schema required keys | ✅ | KEY_RENAME  |
| 3 | package_version semver | ✅ | 5.0.0  |
| 4 | source_qmdj_sha256 present+syntax | ✅ | 2f165e078a7c21700e5f1a1f…  |
| 5 | source_qmdj_sha256 matches boot MANIFEST record | ✅ | 2f165e078a7c2170… == 2f165e078a7c2170…  |
| 6 | interpretation protocol hash present | ✅ |   |
| 7 | rubric hash present | ✅ |   |
| 8 | protocol hash == solver-v4 embedded reference | ❌ | VERSION_SKEW | sha256:protocol_v2_2_1_0_chart_analyst_v4 |
| 9 | rubric hash == solver-v4 embedded reference | ❌ | VERSION_SKEW | sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4 |
| 10 | protocol hash == generator spec (PROMPT/chart_analyser.yaml v5.0.0) | ✅ |   |
| 11 | rubric hash == generator spec (PROMPT/chart_analyser.yaml v5.0.0) | ✅ |   |

## Deviation register
- **DEV-001** — Embedded v4 reference hashes vs actual generator deployment v5.0.0: solver spec qmdj_reference expects chart-analyst v4 hashes; the package was produced by chart_analyser.yaml v5.0.0 (supplied at runtime by the orchestrator). Package hashes match the ACTUAL generator spec exactly (verified above), and source_qmdj_sha256 matches the boot MANIFEST. Skew is a spec-registry lag, not package tampering.
  Decision: PASS_WITH_DEVIATION — proceed; logged here, in OPERATOR/COMMENTS.md, and in Risk-And-Audit-Log. Stale condition that would halt: package hashes matched NEITHER the v4 reference NOR the generator spec.
- **DEV-002** — Schema key rename: 'anomalies' delivered as 'anomaly_registry': spec required-key list says top-level 'anomalies'; the package carries the same data as 'anomaly_registry' (12 records) and additionally per-origin 'origin_sets.B1..B5.anomalies' plus per-palace anomalies arrays. Package also self-labels 'schema_variant'. Data present, naming differs.
  Decision: PASS_WITH_DEVIATION — validator maps anomalies -> anomaly_registry for all references. Stale condition that would halt: no anomaly records existed under ANY key in package or its origin_sets.

Schema renames applied: ['anomalies -> anomaly_registry'].