# Decision and audit record

Tree: LAYER_A | Status: design complete; formal validation partial | Fallback: false

## 1. Executive reading

The campaign addresses the adult passenger who can be overlooked when two people share a two-wheeler. Published evidence informs a focused pre-ride reminder, but does not prove the proposed execution will change behaviour. The selected idea places a temporary message on the stationary passenger seat and requires its removal before mounting. Receipt media was rejected after an existing campaign was found. The finished submission is a designed proposal with real artwork and explicit source limitations, not a report of deployment.

## 2. Walkthrough

### A specific person and moment

The idea narrows road safety to the second rider and makes the mounting point carry the reminder. This is a design hypothesis that can be tested through unprompted comprehension, not a measured local truth.

**Technical basis:** prior-analysis architecture is recorded in OPERATOR/ARCHITECTURE_AND_SELECTION.md; user preference is recorded in campaign_spec.json. Research trace: SRC-001. Design trace: CON-001.

### Research kept within its population

The hospital study supports investigation of short-trip decisions and forgetting. Its percentages are not representative commuter rates. National fatality figures remain attributed through a reproduced table and matching reporting; they do not enter the immediate-action artwork.

**Technical basis:** campaign_spec.json SRC-001 and SRC-002 include population, data period, inspected location, cross-check and limits. CAMPAIGN_REPORT.md section 2 and presentation slides 3–4 carry the qualifications.

### A safer and more distinct execution

A known receipt-format campaign makes a receipt route less suitable for this assignment. The selected seat placement avoids mock fines and must be supervised; if permission or collection cannot be secured, only the illustrated demonstration should be shown.

**Technical basis:** SRC-005, concept dispositions and deployment_rule in campaign_spec.json. Safety challenge retained in OPERATOR/RED_TEAM.md.

## 3. Candidates and selection

| Candidate | Selection | Reason | Limitation |
| --- | --- | --- | --- |
| Second-seat message | Selected as a design choice | Direct relation between placement, passenger and pre-ride response | Supervision and comprehension must be established |
| Two-person parking slip | Rejected | Close receipt-format precedent | Not a legal finding of infringement |
| Plus-one ride invite | Reserve | Simple existing digital medium | Less immediate and audience behaviour unvalidated |

The margin is qualitative, not a computed score: the selected route has the closest physical relation to the requested response. The user's cause preference also informed the decision. No scored superiority or guaranteed effectiveness is asserted.

## 4. Confidence and residual risk

Confidence is strongest in the existence of the cited research and the completeness of the supplied design artifacts. It is limited concerning local insight, audience response and real-world feasibility. A misunderstanding in a comprehension test, inability to collect cards safely, missing permission or a stronger precedent would change the execution. Costs are planning assumptions, not quotations. No primary fieldwork or behaviour-change results exist.

### Gap report

| ID | Path | Why unresolved | Owner phase | Resolution |
| --- | --- | --- | --- | --- |
| GAP-001 | Formal input acceptance | Upstream narrative has no fully validated structured registry or archetype resolutions; binding/scoring harness unavailable | Formal validation | Preserve limitation; do not certify unavailable guards |
| GAP-002 | Audience validation | No local interviews or comprehension test conducted | Before deployment | Use supplied blank instruments and report actual results |
| GAP-003 | Permissions and supervision | No venue/owner permission confirmed | Deployment | Obtain consent and safe collection; otherwise use illustration only |
| GAP-004 | Original national table cells | Reproduced data and reporting inspected, original ministry cells not directly inspected | Research verification | Disclose chain; inspect original cells before asserting primary inspection |
| GAP-005 | Costs and implementation | Estimates only; no vendor quote or deployment | Production | Confirm before spending; do not invent receipts or outcomes |
| GAP-006 | External delivery | No submission-platform upload or classroom presentation performed | User handoff | Use prepared files for the brief's named milestones |

## 5. Full technical mapping

The appendix below reproduces the current operator documents verbatim. Each SHA-256 value identifies the exact included content. Technical terms in the appendix are audit material, not public campaign framing.

### Technical appendix: COMMENTS.md

SHA-256: `5045e0084d29adaaff33fe4b7d9b29d7f8e261a7f824c39d4818797d59851b14`

# Operator comments

Tree: OPERATOR | Status: partial formal execution; completed design artifacts | Fallback: false

## Role and input boundary

Working charter: `PROMPT/assignment_solver_charter.md` (v7.0.0). The user explicitly requested questions, overriding its no-questions instruction. Brief: `ASSIGNMENTS/ADVERTISING/project_2.yaml`. Interpretive input: the existing `CHART_CASE_ANALYSIS.md`. No raw chart was read during the solver stage; no geometry, pillars, evidence atoms or upstream interpretation were re-derived.

The upstream narrative is a bounded analysis, not a fully accepted structured evidence package. Earlier `analysis_package.json` remains the blocked preflight; it was not rewritten into a false success. Loading the solver charter does not cure absent archetype resolutions, registry atoms, CAP bindings, compatibility verification or rubric hashes. Formal package-acceptance and shipment gates are **not claimed passed**. Deliverables are a complete design proposal with an explicit formal-audit gap, not a certified execution of every charter phase.

## User choices

The user did not strongly favour the original suggestions, authorized factual research, delegated media/production recommendations, and then accepted A/C while leaning toward C. C is the lead cause; A remains the cause-level runner-up. No additional question was necessary to make this reversible creative choice. This is user-guided editorial selection, not a CAP-scored or chart-certified winner.

## Evidence separation

The previous analysis shapes creative architecture: clarity, overlooked second person, contextual medium, low effort, sensitive treatment and prototype-first development. Published sources supply real-world facts; they never strengthen chart evidence. The seat-card execution, copy, audience segment and visual system are explicitly solver-authored design choices, not entities discovered in the chart.

Primary research foundation: Mishra et al., DOI 10.4103/ijciis.ijciis_85_24, hospital data from March–December 2021, published 2025. Do not convert its 346-patient sample into national or local prevalence. Do not present the share of helmet users who were pillions as pillion compliance. The 96.6% figure concerns agreement that helmets are essential; it does not mean that percentage of Indian commuters behaves in a particular way.

National 2024 figures were cross-checked through an inspected OpenCity API table and matching Hindustan Times reporting. Those reproduce a common MoRTH source; original ministry cells were not directly inspected. Public short-form artwork contains no fatality or efficacy statistics. The report and deck disclose the chain and limitation.

## Precedent-driven change

A receipt route was initially considered but rejected after discovering the HDFC Bank/STUDDS Helmet Receipt campaign reported in February 2026. The selected seat placement is not declared globally unprecedented; the review is bounded. There is no fake fine, police role, receipt branding, sponsor logo, helmet product or new service.

## Safety and practical constraint

A loose campaign card is permitted only during an opt-in, supervised, stationary encounter. Engine off. No adhesive, wrapping, attachment or unattended placement. Facilitator collects and accounts for every card before mounting. If that cannot be assured, do not deploy; use the illustrated prototype. The concept is not intended to remain on a vehicle in use. No helmets are modified or certified by appearance. All depicted contexts are illustrations, not evidence of actual deployment.

## Tools and checks actually used

Python standard library, ReportLab, python-pptx, pypdf and PyMuPDF produced and inspected real PDFs, editable slide content and vector/raster artwork. Dependencies were installed in the local excluded `.venv`, not added as a large repository artifact. `build_deliverables.py` is an artifact renderer, not a replacement CAP harness. Its checks prove listed file properties only: parseability, slide/page counts, dimensions, selected copy, budget arithmetic and a limited lexical scan. They do not prove campaign effectiveness, full charter validation, legal approval or empirical completeness.

The first system-wide pip attempt was refused by the managed environment. Recovery was an isolated virtual environment; no system-package override was used. A CSV fetch returned HTTP 500; the available OpenCity API was inspected instead and its exact row/field is recorded. No missing response was invented.

## Residual gaps

No venue permission, primary audience interviews, comprehension tests, vendor quotes, deployment, filmed footage, behaviour-change evidence or exhaustive originality clearance exists. These are disclosed in the design submission and blank instruments. Fieldwork was not required to be fabricated to make a polished presentation. See MANIFEST and LAYER_A for the gap register.


### Technical appendix: MAPPINGS.md

SHA-256: `839032a1364ef51e2bbfe6d07266d91cdc1bc5ef7bc2ecca8d95dff197da16ff`

# Assignment mappings

Tree: OPERATOR | Status: design mapping, formal coverage not certified | Fallback: false

Each brief facet receives one analysis-alignment row. INDIRECT means a symbolic design connection only, not empirical support. Research facts, audience demographics, cause selection and schedule compliance are not established by the analysis. Zero tallies are retained. No E/C/BIND IDs are invented.

| Requirement | Brief anchor | Design artifact match | Analysis alignment |
| --- | --- | --- | --- |
| REQ-001 | `file.pages[0].sections[0].text` | present_as_design_objective | INDIRECT |
| REQ-002 | `file.pages[0].sections[1].heading` | present | NO_CHART_SUPPORT |
| REQ-003 | `file.pages[0].sections[1].items[0]` | present | INDIRECT |
| REQ-004 | `file.pages[0].sections[1].items[1]` | present_as_strategic_focus | NO_CHART_SUPPORT |
| REQ-005 | `file.pages[0].sections[1].items[2]` | present_with_disclosed_source_limits | NO_CHART_SUPPORT |
| REQ-006 | `file.pages[0].sections[2].items[0]` | present_as_relevance_hypothesis | INDIRECT |
| REQ-007 | `file.pages[0].sections[2].items[1]` | present_as_idea_innovation | INDIRECT |
| REQ-008 | `file.pages[0].sections[2].items[2]` | product_service_absent_by_design | INDIRECT |
| REQ-009 | `file.pages[0].sections[3].schedule[0]` | present | INDIRECT |
| REQ-010 | `file.pages[0].sections[3].schedule[1]` | design_files_present_fieldwork_not_claimed | INDIRECT |
| REQ-011 | `file.pages[0].sections[3].schedule[2]` | files_prepared_external_upload_not_performed | NO_CHART_SUPPORT |
| REQ-012 | `file.pages[0].sections[3].schedule[3]` | presentation_prepared_external_presentation_not_performed | NO_CHART_SUPPORT |
| REQ-013 | `file.pages[0].sections[4].text` | single_campaign_design_present_effect_not_claimed | INDIRECT |
| REQ-014 | `file.pages[0].sections[5].items[0]` | present_with_disclosed_source_limits | NO_CHART_SUPPORT |
| REQ-015 | `file.pages[0].sections[5].items[1]` | present_as_design_rationale | INDIRECT |
| REQ-016 | `file.pages[0].sections[5].items[2]` | prototype_present_not_deployed | INDIRECT |
| REQ-017 | `file.pages[0].sections[5].items[3]` | presentation_present_not_empirically_tested | INDIRECT |

Alignment tally: {"DIRECT": 0, "INDIRECT": 11, "NO_CHART_SUPPORT": 6, "CONTRADICTS_KNOWN": 0}.

Full quotations, output locations and specific prior-analysis section references are in `design_requirement_map.json`. This table accounts for all listed brief facets but does not turn pending external actions or untested claims into completed outcomes. Actual NLET upload and classroom presentation remain user actions.


### Technical appendix: PATH_RANK.md

SHA-256: `2b8d69bcd08acac35204f9aed9798d268c33aab89375d1125e69a2c08de3456a`

# Candidate paths and selection

Tree: OPERATOR | Status: editorial comparison only | Fallback: false

No numerical rank, grounding tier, confidence score, requirement-fit score or formal archetype resolution was created. No CAP scorer was available. Counts of sources are not used to fabricate a score.

## Cause choice

- A: unpaid domestic labour. Strong India data and overlooked-work architecture. Retained as runner-up. Do not mix it into the pillion campaign.
- C: pillion helmet use. User indicated a stronger preference for C; immediate action and second-person oversight fit the prior architecture. Developed as lead by explicit user preference, not a claim of superior chart grounding.
- B and D: not selected; retain research dossier and limitations rather than silently discard them.

## Three concepts within selected cause

| Path | Decision | Basis | Counterweight |
| --- | --- | --- | --- |
| CON-001: supervised stationary second-seat card | Selected editorially | The physical placement identifies the passenger and situates the message before mounting; no platform dependency | Consent, supervision and collection are hard deployment conditions. The metaphor and clarity need testing. |
| CON-002: two-person parking receipt | Rejected | Existing Helmet Receipt campaign is a close executional precedent; original development is weaker | This is not a finding of copying or legal infringement; it is a conservative creative-selection choice. |
| CON-003: plus-one ride invite | Reserve | Simple pre-ride shared-message format; easy to demonstrate | Greater distance from the action, unvalidated channel behaviour and risk of generic social content. |

The selected concept remains conditional on safe demonstration. If supervision or permission fails, the safe output is the illustrated mockup, not an unannounced substitution or a claim of deployment. A supporting social artwork reinforces CON-001; it does not assert that the reserve concept won.


### Technical appendix: EVIDENCE_CONSUMPTION.md

SHA-256: `2ee004545b879de9e20d76693049a4cfc520da8bb97aecb717b1620451d729f6`

# Evidence consumption

Tree: OPERATOR | Status: bounded review | Fallback: false

| Existing analysis component | Disposition | Use or reason |
| --- | --- | --- |
| Centre clarity/excess warning | Used as indirect design constraint | One message; no heavy interaction or statistic on hero creative |
| Palace 4 development and conditional amplification | Used as indirect process guidance | Developed media concept, feedback and conditional deployment; adverse entries not erased |
| Palace 2 self-defeating choice / preparation | Used as indirect ethical constraint | No fake fine, shame or implied authority |
| Palace 1 effort and friction | Used as indirect delivery constraint | No mandatory scan, registration or app |
| Palace 3 emergence alongside limits | Used as indirect creative prompt | Overlooked second person; empirical significance supplied separately |
| Palace 6 incubation and coordination caution | Used as indirect process constraint | Prototype-first planning and explicit removal responsibility |
| Palace 7 reception versus initiation | Used as indirect validation prompt | Comprehension instrument; no inference from exposure to effect |
| Palace 8 adverse markers | Used as indirect safety constraint | No traffic stunt, hazardous intervention or crash simulation |
| Palace 9 confusion/deception warning | Used as indirect truth constraint | Attributed data, no guaranteed safety or fabricated results |
| Technical stems, pillars, geometry and extreme literal meanings | Reviewed but not used for assignment facts | No demographic, cause, outcome, legal event or equipment inferred |
| Upstream registry, scored archetypes and closure proof | Deferred / unavailable | Narrative did not supply validated atoms or formal scoring; never reconstructed |

External research is catalogued separately in campaign_spec.json SRC-001..005. It supplies public-health facts and precedent, not chart corroboration. All factual artwork claims are general safety guidance; national statistics and their limitations remain in the report/deck.


### Technical appendix: RED_TEAM.md

SHA-256: `27a2896df5e09b7bc2d815ab9165eca466773dbd774c6d4fbc7c87e114cbe8b8`

# Adversarial design review

Tree: OPERATOR | Status: completed editorial review, not charter RT certification | Fallback: false

| Challenge | Response | Residual status |
| --- | --- | --- |
| This is only a card, not media innovation | The chosen advertising placement is the actual second seat at the mounting decision; contextual referent and timing create the idea. Generic wall placement alone would be weaker. | Creative judgement remains contestable; demonstrate the seat relationship clearly. |
| The metaphor is awkward or confusing | Literal pillion and fastening instructions appear beneath the headline; test unprompted comprehension. | Untested. Replace metaphor if it obscures the response. |
| Awareness is already high; another reminder may not work | Strategy is a contextual pre-ride cue, not generic awareness. Research informs the opportunity but does not prove the intervention. | No effectiveness claim. |
| Loose paper could be a vehicle hazard | Owner opt-in, engine off, direct supervision, removal/accounting before mounting; no unattended placement or attachments. | No deployment if safe collection is uncertain. |
| Pillion users may not have a suitable helmet | Do not pressure a ride, pretend reminder solves access or offer an unrequested rental service. | Structural access remains outside the communication's scope. |
| A receipt execution already exists | CON-002 rejected with published precedent. | Selected concept still lacks exhaustive originality clearance. |
| National figures have a weak primary-source chain | Original ministry cells not directly inspected; reproduced API cells and matching report are attributed. Stats kept out of short creative. | Disclosed research limitation. |
| Hospital sample is not campus prevalence | Population, data period and design limits appear in report and slide 4. | No local rate inferred. |
| 8.8% could be misread as pillion compliance | That statistic is not used. | Specific denominator trap avoided. |
| Other road-safety factors are ignored | WHO safe-system qualification retained; no helmet guarantees all safety. | Campaign deliberately focuses one behaviour. |
| Prototype could be mistaken for real deployment | Context illustrations, HTML sequence and all research instruments labelled honestly. | No fabricated fieldwork, partner or outcome. |
| Formal evidence package and scoring are missing | Retained as a gap; renderer and checks are not presented as CAP tools. | Formal charter certification blocked. |

Limited mechanical checks are in build_checks.json. No source comparison beyond the authorized inputs was run. Golden fixture regression, formal semantic-lint tooling and complete charter guards were not available or claimed. No required non-text artifact is silently represented by written direction: actual PDF, PPTX, SVG and PNG outputs are supplied. The motion deliverable is an HTML illustrated prototype, not an MP4 or completed shoot.
