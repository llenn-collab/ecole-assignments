#!/usr/bin/env python3
"""Write transparent design-coverage records, audit notes and a SHA-256 manifest.
This is ordinary artifact packaging, not charter CAP execution or evidence creation.
"""
import hashlib
import json
import zipfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[2]
SUB=BASE/'SUBMISSION'
OP=BASE/'OPERATOR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

# Quotes and section anchors preserve the supplied brief's actual requirements.
# These records describe design-artifact presence, not certified charter coverage.
rows=[
('REQ-001','Creating an impactful communication towards a social cause using media innovation.','sections[0].text','must','CAMPAIGN_REPORT.md §§1,4,6; presentation slides 1,5–11','present_as_design_objective','INDIRECT','CHART_CASE_ANALYSIS.md §§2,3,6'),
('REQ-002','PICK A SOCIAL CAUSE OF YOUR CHOICE','sections[1].heading','must','CAMPAIGN_REPORT.md §1','present','NO_CHART_SUPPORT',None),
('REQ-003','Narrow down the industry / sector / segment of society it affects','sections[1].items[0]','must','CAMPAIGN_REPORT.md §§1,3','present','INDIRECT','CHART_CASE_ANALYSIS.md §§5,6'),
('REQ-004','Define your target audience','sections[1].items[1]','must','CAMPAIGN_REPORT.md §3','present_as_strategic_focus','NO_CHART_SUPPORT',None),
('REQ-005','Support your social cause (prevalence / impact) with data / research','sections[1].items[2]','must','CAMPAIGN_REPORT.md §2 and source register; campaign_spec.json research SRC-001..004','present_with_disclosed_source_limits','NO_CHART_SUPPORT',None),
('REQ-006','Pick a media channel that is relevant to your target audience.','sections[2].items[0]','must','CAMPAIGN_REPORT.md §§5,6; ARTWORK/seat_card_A6.pdf','present_as_relevance_hypothesis','INDIRECT','CHART_CASE_ANALYSIS.md §§5,6,7'),
('REQ-007',"Create either an idea innovation (how it's used) or a tech innovation, to deliver your message effectively.",'sections[2].items[1]','must','CAMPAIGN_REPORT.md §§5,6; ARTWORK/stationary_context_mockup.pdf','present_as_idea_innovation','INDIRECT','CHART_CASE_ANALYSIS.md §§3,6,7'),
('REQ-008','IMPORTANT: The impact lies in your message - avoid creating a product line / service for your social cause. Aim to bring a change in awareness or behaviour through your communication.','sections[2].items[2]','must_not','CAMPAIGN_REPORT.md §§1,4,5,6; all public artwork','product_service_absent_by_design','INDIRECT','CHART_CASE_ANALYSIS.md §§1,6,7'),
('REQ-009','Chosen social cause + Data / Insight + 3 media innovation concepts','sections[3].schedule[0]','must','CAMPAIGN_REPORT.md §§1–5; presentation slides 2–7','present','INDIRECT','CHART_CASE_ANALYSIS.md §§6,7,8'),
('REQ-010','WIP - Design Execution','sections[3].schedule[1]','must','PDF/SVG/PNG artwork; motion prototype; CAMPAIGN_REPORT.md §§6–8','design_files_present_fieldwork_not_claimed','INDIRECT','CHART_CASE_ANALYSIS.md §§5,8'),
('REQ-011','NLET Submission','sections[3].schedule[2]','must','User-ready campaign report/presentation/artwork; CAMPAIGN_REPORT.md §11','files_prepared_external_upload_not_performed','NO_CHART_SUPPORT',None),
('REQ-012','Class Presentation & Final Review','sections[3].schedule[3]','must','19-slide PDF/PPTX/HTML and SPEAKER_NOTES.md','presentation_prepared_external_presentation_not_performed','NO_CHART_SUPPORT',None),
('REQ-013','A single ad campaign using innovative use of media, that drives a powerful message / statement to its target audience about the chosen social cause. Please include: data on your social cause data | target audience insight | creative strategy.','sections[4].text','must','CAMPAIGN_REPORT.md §§2–6; all final artwork shares one cause and one instruction','single_campaign_design_present_effect_not_claimed','INDIRECT','CHART_CASE_ANALYSIS.md §§2,6,7'),
('REQ-014','Research: Identifying a niche problem. Providing stats.','sections[5].items[0]','must','CAMPAIGN_REPORT.md §§1–3 and source register','present_with_disclosed_source_limits','NO_CHART_SUPPORT',None),
('REQ-015','Ideation: Creative thinking, balancing topic and audience sensitivity','sections[5].items[1]','must','CAMPAIGN_REPORT.md §§4,5,8','present_as_design_rationale','INDIRECT','CHART_CASE_ANALYSIS.md §§4,5,6'),
('REQ-016','Execution: Use of media innovation','sections[5].items[2]','must','Seat-card artwork and stationary context illustration; motion prototype','prototype_present_not_deployed','INDIRECT','CHART_CASE_ANALYSIS.md §§3,6,7'),
('REQ-017','Presentation: Clarity of solution and presentation','sections[5].items[3]','must','19-slide presentation, report and source qualifications','presentation_present_not_empirically_tested','INDIRECT','CHART_CASE_ANALYSIS.md §§2,5,6')
]
requirements=[]
for rid,quote,anchor,level,outputs,design_status,alignment,basis in rows:
 requirements.append({'id':rid,'quoted_text':quote,'source':'ASSIGNMENTS/ADVERTISING/project_2.yaml','page_anchor':'file.pages[0].'+anchor,'must_level':level,'design_output_locations':outputs,'design_status':design_status,'analysis_alignment':alignment,'analysis_basis':basis,'formal_charter_coverage_certified':False})
(OP/'design_requirement_map.json').write_text(json.dumps({'record_type':'design_artifact_map_not_certified_charter_requirement_objects','requirements':requirements},ensure_ascii=False,indent=2)+'\n')
tallies={tag:sum(r['analysis_alignment']==tag for r in requirements) for tag in ['DIRECT','INDIRECT','NO_CHART_SUPPORT','CONTRADICTS_KNOWN']}
md='# Assignment mappings\n\nTree: OPERATOR | Status: design mapping, formal coverage not certified | Fallback: false\n\nEach brief facet receives one analysis-alignment row. INDIRECT means a symbolic design connection only, not empirical support. Research facts, audience demographics, cause selection and schedule compliance are not established by the analysis. Zero tallies are retained. No E/C/BIND IDs are invented.\n\n'
md+='| Requirement | Brief anchor | Design artifact match | Analysis alignment |\n| --- | --- | --- | --- |\n'
for r in requirements:md+=f'| {r["id"]} | `{r["page_anchor"]}` | {r["design_status"]} | {r["analysis_alignment"]} |\n'
md+='\nAlignment tally: '+json.dumps(tallies)+'.\n\nFull quotations, output locations and specific prior-analysis section references are in `design_requirement_map.json`. This table accounts for all listed brief facets but does not turn pending external actions or untested claims into completed outcomes. Actual NLET upload and classroom presentation remain user actions.\n'
(OP/'MAPPINGS.md').write_text(md)

consumption='''# Evidence consumption

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
'''
(OP/'EVIDENCE_CONSUMPTION.md').write_text(consumption)

red='''# Adversarial design review

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
'''
(OP/'RED_TEAM.md').write_text(red)

slides=json.loads((OP/'presentation_content.json').read_text())
speaker='# Presentation speaker notes\n\nTree: SUBMISSION | Status: design complete, not deployed | Fallback: false\n\nSuggested pace: 7–9 minutes. Treat the research limitations as part of the argument, not fine print. Do not claim the audience has been interviewed or the campaign has been tested.\n\n'
for i,s in enumerate(slides):
 speaker+=f'## Slide {i+1}: {s["title"].replace(chr(10)," ")}\n\n{s["body"]}\n\n**Qualification / delivery note:** {s["note"]}\n\n'
(SUB/'SPEAKER_NOTES.md').write_text(speaker.rstrip()+'\n')

# Plain-English narrative precedes the current operator appendix.
operator_parts=[]
for name in ['COMMENTS.md','MAPPINGS.md','PATH_RANK.md','EVIDENCE_CONSUMPTION.md','RED_TEAM.md']:
 p=OP/name
 operator_parts.append({'name':name,'sha256':sha(p),'text':p.read_text()})
layer='''# Decision and audit record

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

'''
for part in operator_parts:
 layer+=f'### Technical appendix: {part["name"]}\n\nSHA-256: `{part["sha256"]}`\n\n'+part['text']+'\n\n'
(BASE/'LAYER_A').mkdir(exist_ok=True)
(BASE/'LAYER_A/DECISION_AND_AUDIT.md').write_text(layer.rstrip()+'\n')

# Update only the solver configuration, never upstream immutable analysis artifacts.
config=BASE/'solver_execution_config.json'
s=json.loads(config.read_text())
s.update({'status':'design_complete_formal_validation_partial','selected_cause':'C: adult pillion helmet use','selected_concept':'CON-001: supervised stationary second-seat card','selection_basis':'User leans toward C; transparent editorial concept comparison','raw_chart_access':False,'formal_solver_validation_claimed':False,'pending_decisions':[],'pending_external_actions':['venue and owner permission','comprehension testing','optional safe deployment','actual NLET upload and class presentation']})
config.write_text(json.dumps(s,ensure_ascii=False,sort_keys=True,indent=2)+'\n')

# Snapshot only explicitly authorized input paths; do not inspect other repo files.
inputs=[ROOT/'PROMPT/assignment_solver_charter.md',ROOT/'ASSIGNMENTS/ADVERTISING/project_2.yaml',BASE/'CHART_CASE_ANALYSIS.md']
input_rows=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs]
files=[]
for tree in ['SUBMISSION','ANNOTATED','LAYER_A','OPERATOR']:
 for p in sorted((BASE/tree).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   files.append({'path':str(p.relative_to(BASE)),'tree':tree,'bytes':p.stat().st_size,'sha256':sha(p)})
archive=BASE/'PROJECT_2_SUBMISSION.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(SUB.rglob('*')):
  if p.is_file():
   info=zipfile.ZipInfo(str(p.relative_to(BASE)),date_time=(2026,10,14,0,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,p.read_bytes())
archive_record={'path':archive.name,'sha256':sha(archive),'bytes':archive.stat().st_size,'contents':'Professional SUBMISSION tree only; technical operator records stay separate.'}
manifest={'delivery_archive':archive_record,'package':'THIS SEAT HAS A HEAD.','prepared_on':'2026-10-14','runtime_mode':'TOOLS_PRESENT','design_status':'complete_as_designed_proposal','formal_charter_status':'partial_not_certified','fallback_mode':False,'input_provenance':input_rows,'output_files':files,'output_count':len(files),'total_output_bytes':sum(x['bytes'] for x in files),'interpretation_protocol_hash':None,'evidence_or_scoring_rubric_hash':None,'hash_absence_reason':'Authoritative frozen protocol/rubric artifacts were not supplied or authorized; no expected hash is invented.','source_evidence_sha256':None,'source_evidence_hash_reason':'Raw source is forbidden in solver stage; analysis-input hash recorded instead.','blocked_requirements':['Formal package acceptance and certification are not available.'],'tied_requirements':[],'unsupported_required_formats':[],'external_actions_pending':s['pending_external_actions'],'gap_report_reference':'LAYER_A/DECISION_AND_AUDIT.md section 4','checks_reference':'OPERATOR/build_checks.json','notes':['No raw chart read in solver stage.','No CAP/score/guard certification claimed.','No fieldwork, permission, deployment or effectiveness fabricated.','Input hashes are recorded, but no externally supplied expected hash was available.','Real PDFs/PPTX/SVG/PNG delivered; HTML motion prototype is not a live-action film.']}
(BASE/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
m='# Delivery manifest\n\n**Campaign: THIS SEAT HAS A HEAD.**\n\nDesign status: complete as a designed proposal. Formal charter status: partial, not certified. Runtime: TOOLS_PRESENT. Fallback: false.\n\n## Open first\n\n- `SUBMISSION/CAMPAIGN_PRESENTATION.pdf` — 19-slide presentation.\n- `SUBMISSION/CAMPAIGN_PRESENTATION.pptx` — editable slide deck.\n- `SUBMISSION/CAMPAIGN_REPORT.pdf` — complete strategy and research document.\n- `SUBMISSION/PRESENTATION.html` — responsive deck preview.\n- `SUBMISSION/MOTION_PROTOTYPE.html` — captioned 15-second illustrated sequence.\n- `SUBMISSION/ARTWORK/` — finished hero, poster, social and contextual illustration files.\n\nThe professional submission contains no technical interpretive framing. Supporting research qualifications, commentary and audit records remain explicit. No real deployment or fieldwork is claimed.\n\n## Input provenance\n\n'
for r in input_rows:m+=f'- `{r["path"]}`: `{r["sha256"]}` ({r["bytes"]} bytes).\n'
m+=f'\nProfessional submission archive: `{archive_record["path"]}` ({archive_record["bytes"]} bytes), SHA-256 `{archive_record["sha256"]}`. Contains only the SUBMISSION tree.\n'
m+='\nAuthoritative frozen protocol/rubric hashes and externally expected acceptance hashes were unavailable; PROVENANCE_LIMITED. Raw-source evidence hash was not recomputed because the solver must not read it. Full input acceptance, formal archetype resolutions and CAP execution remain unverified, not silently passed.\n\n## Gaps and external actions\n\nThe gap register in `LAYER_A/DECISION_AND_AUDIT.md` records formal-package limitations, audience testing, permissions, original national-table inspection, actual costs/implementation and external submission/presentation. Blank instruments remain blank. The national-data chain is reproduced-table plus corroborating reporting, not asserted original-cell inspection.\n\n## File checksums\n\nMANIFEST.json contains the same file records in machine-readable form. Hashes below cover the four delivery trees; the manifests do not claim to hash themselves. Earlier root-level preflight artifacts are retained as historical analysis-stage work, not silently included as successful solver output.\n\n| File | Bytes | SHA-256 |\n| --- | --- | --- |\n'
for r in files:m+=f'| `{r["path"]}` | {r["bytes"]} | `{r["sha256"]}` |\n'
(BASE/'MANIFEST.md').write_text(m)
print(f'Finalized {len(files)} output records; {sum(x["bytes"] for x in files)} bytes. Alignment tallies: {tallies}. No formal scores or evidence atoms created.')
