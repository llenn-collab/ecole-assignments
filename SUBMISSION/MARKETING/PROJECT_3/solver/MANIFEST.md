# MANIFEST — Carpathia Assignment Solver run (MARKETING Project 3)

runtime_mode: TOOLS_PRESENT · package: qmdj_chart_analyst v7.1.0 sections 00-16 (MAPPED via field_map_v7)
adapter_status: MAPPED · provenance: PROVENANCE_LIMITED for A2 (source file corrupt; user-paste is the verbatim source)

## Inputs

- assignment brief: ASSIGNMENTS/MARKETING/project_3.yaml sha256:c94912b20bce2c7ac911c11a5a22efb44bc1855d536d01b54149035234bf2991
- chart analysis package: SUBMISSION/MARKETING/PROJECT_3/package/*.json (17 sections) sha256(08_claim_lines):ad3d9c8b61ef6aa1235d9e17914a3e986c1f2c5090bc91a5de59295f85b5f272
- A1 source: SUBMISSION/MARKETING/project_1.pdf sha256:472329e5c512573a0e5f22f4a526763b68e660c6608a897d357f6b7dcd9d1da1 (image-only; transcribed via page images)
- A2 source: user-pasted slide text (repo project_2.pdf is a corrupt 2-byte file; recorded as EXTRACTION-source substitution, MAPPED)

## Outputs (SUBMISSION tree)

- Project_1_OffHours_context.docx sha256:3a5e6fff8ce4e160b0fbda01b75ecde239c00ded236c93dd5d30b52226f926d5
- Project_2_OffHours_context.docx sha256:e3ee4172fac7be7df9630cfbf4886ef4d69fb4c3b9d13f5df113bfdc7d1b52ea
- Project_3_OffHours_solution.docx sha256:c36f3dcc3b83f2c26e674cf39693ee612e5fd61c2003104ee0659a003be8b8bf

## Requirement ledger summary

- requirements: 28 · must uncovered/blocked: none · must_not violations: none
- full ledger: solver/requirement_ledger.json

## Gates

- lexical+phrase lint over SUBMISSION docx: PASS (0 violations)
- coverage gate: PASS (no must UNCOVERED/BLOCKED; must_not satisfied by absence with proof in ledger)
- hard-constraint gate: PASS (word-document-only deliverable honoured; no PDF/PPTX produced)
- unsupported format gate: PASS (brief requires text copy in Word; python-docx binary write validated by re-read)
- fallback_mode: none · blocked: none · tied: none
