# Package Validation

- Package: `vault/raw/package/chart_analysis_package.json`
- sha256: `59ddb7eab387461f63d35ca0610a26e1f06d0c89fe9a7c3dfddfa3ba1fc6a466`
- package_version: `4.0.0`
- source chart sha256 (carried, not re-read): `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`

| check | result | detail |
|---|---|---|
| package_schema_required_keys | PASS | all 13 required keys present |
| package_version_semver | PASS | package_version = 4.0.0 |
| source_qmdj_sha256_valid | PASS | sha256 = 083a393c855730e9bf62... |
| interpretation_protocol_hash_matches_reference | PASS | package=sha256:protocol_v2_2_1_0_chart_analyst_v4 expected=sha256:protocol_v2_2_1_0_chart_analyst_v4 |
| archetype_rubric_hash_present | PASS | prompt1 rubric = sha256:archetype_scoring_rubric_1_0_0_chart_analyst_v4 |
| prompt1_requirement_fit_all_null | PASS | all candidates carry requirement_fit_score = null, as Prompt 1 requires |
| upstream_field_coverage_complete | PASS | 242/242 source paths cited upstream |
| upstream_citation_integrity | PASS | 0 broken evidence links in the package |
| upstream_board_consistency | PASS | cross-palace consistency passed upstream |

## Law 8 compliance

The solver never opens the source chart file. Every chart fact used downstream is read from the package above, which carries the chart's hash for provenance.

