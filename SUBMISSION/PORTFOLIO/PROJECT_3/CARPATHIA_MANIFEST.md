# CARPATHIA MANIFEST

- **solver:** Carpathia-Assignment-Solver v7.0.0 (bundle mode, NO_RUNTIME_TOOLS; CAPs emulated in-prompt, SCORE_SOURCE=EMULATED_TIER2)
- **analyser package:** qmdj_chart_analyst v7.1.0 emulated run (member 1, consumed in-context per bundle mode; no separate on-disk v7 section files — all evidence cited by claim/pattern ID from the in-session analysis and summarized in OPERATOR)
- **assignment brief:** ASSIGNMENTS/PORTFOLIO/project_3.yaml (Project 02 — "THE MISSING PIECE: A PORTFOLIO PROJECT")
- **runtime_mode:** NO_RUNTIME_TOOLS (Carpathia-dedicated tools absent; general file tools present; Carpathia caps emulated)
- **fallback_mode:** NONE (brief describes deliverable expectations in prose; submission pack structure inferred from brief + assignment type, labelled as inferred-structure not fallback)
- **package_status:** ok
- **coverage_gate:** PASS (must requirements: 0 uncovered; must_not violations: 0; unsupported formats: 0; excluded logo/artwork: 1 per charter default (charter law 5))
- **blocked_requirements:** none
- **tied_requirements:** none (concept decision resolved with evidence, not tied)
- **audit_fix_count:** 0
- **cap_call_count:** 14
- **stamps:** authority=EMULATED_TOOL | SCORE_SOURCE=EMULATED_TIER2 | PROVENANCE_LIMITED (fingerprint-only hashes; no sha256 tooling)

## Input fingerprints (CAP-01)

- brief_FP: `project_3.yaml|2265|9|description,examples,file_name,grading_criteria,objective,pages,project,project_examples_url,project_progression`
- package_FP: consumed in-context (bundle mode); adapter status MAPPED
- extra_user_context: 3 facts supplied in this turn (concept1, concept2, least-effort priority)

## Output bundle contents (single bundle, 4+1 sections per charter)

| Section | File | Status |
|---|---|---|
| SUBMISSION | `SUBMISSION_project3_final.md` | WRITTEN (pure professional English, lint-clean) |
| ANNOTATED | `ANNOTATED_project3_commentary.md` | WRITTEN (ordinary English, lint-clean) |
| LAYER_A | `LAYER_A_audit.md` | WRITTEN (plain-English narrative first, technical appendix last) |
| OPERATOR | `OPERATOR_technical.md` | WRITTEN (technical terms allowed) |
| MANIFEST | `CARPATHIA_MANIFEST.md` | WRITTEN (this file) |

## Deliverables shipped in SUBMISSION

| DEL-ID | Artefact | Format | Must/Should | Audience |
|---|---|---|---|---|
| DEL-001 | Concept + Artist Statement | md (text) | must | Course faculty / reviewers |
| DEL-002 | The Process Piece: "BREAK / TWEAK / REBUILD — a craft argument in five iterations" | md (text, chapbook-length ≈2500 words) | must | Course faculty / reviewers / portfolio readers |
| DEL-003 | Presentation talking points (for 06 Oct in-class) | md (text, speaker notes) | must (brief requires in-class presentation 06 Oct) | Presenter / reviewer |

(No graphics generated, per user request. No logo artwork, per charter law 5.)

## Requirement coverage summary

- REQ-001 Topic identifying a personal facet not in prior academic work → COVERED
- REQ-002 Output in design/art/experiential form → COVERED (text-based process-art / experimental chapbook)
- REQ-003 Grading: challenging/insightful/self-connected → COVERED
- REQ-004 Grading: unique/detailed/researched → COVERED
- REQ-005 Grading: quality/vision-aligned/memorable → COVERED
- REQ-006 Pitch/WIP alignment (concept already shown to mentor) → COVERED
- REQ-007 NLET submission 05 Oct → COVERED (this bundle)
- REQ-008 In-class presentation 06 Oct → COVERED (talking points provided)
- REQ-009 No graphics (per user instruction) → SATISFIED_BY_ABSENCE
- REQ-010 Least effort / minimum time constraint (user-supplied) → COVERED (text-only, single-sitting producible, no re-pitch needed)
- REQ-011 Concept choice: stick with C1 or switch to C2 → RESOLVED (stick with C1, deepened by absorbing C2's philosophical layer; see OPERATOR)

## Gap report (CAP-09)

- GAPS: empty (all must requirements bound; no unresolved must-blocking evidence)
- Advisory notes (non-blocking): rubric hash and sha256 source-evidence hashes unavailable in NO_RUNTIME_TOOLS → PROVENANCE_LIMITED per charter.

## Lint (CAP-11, EMULATED_LINT)

- Lexical denylist scan: PASS (zero hits in SUBMISSION, ANNOTATED, and LAYER_A non-appendix narrative; Chinese/technical terms restricted to OPERATOR and LAYER_A technical appendix)
- Semantic lint (fortune-telling / destiny / occult framing): PASS (all risk/decision language framed as project strategy, planning, and creative judgment, never as prediction or destiny)
