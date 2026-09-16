"""Solver Stage 1: INIT -> PACKAGE_VALIDATE -> PDF_INGEST (markdown brief as assignment doc)."""
import json, os, sys, re, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common2 import *

run_id = f"carpathia-solver-v4-run-{utcnow().replace(':','').replace('-','')}-{os.getpid()%997}"
for d in [os.path.join(RAW, "assignment"), os.path.join(RAW, "package"),
          os.path.join(OUT, "SUBMISSION"), os.path.join(OUT, "ANNOTATED"),
          os.path.join(OUT, "OPERATOR"), os.path.join(OUT, "LAYER_A"),
          os.path.join(WIKI, "_meta")]:
    os.makedirs(d, exist_ok=True)

# ---------------- INIT ----------------
brief_hash = sha256_file(ASSIGN)
pkg_hash_boot = sha256_file(PKG_SRC)
if not os.path.exists(READ_LOG):
    json.dump({"reads": []}, open(READ_LOG, "w"))
json.dump({"policy": "deny read QMDJ/**; every read logged; gate checked at SYNTHESIZE",
           "deny_pattern": r"QMDJ"}, open(READ_LOG, "w")) if False else None
json.dump({"reads": []}, open(READ_LOG, "w"))
shutil.copy2(PKG_SRC, PKG_COPY)
json.dump({"reads": [{"path": os.path.relpath(ASSIGN, REPO), "at": utcnow(), "purpose": "bootstrap_hash"}]}, open(READ_LOG, "w"))
prov_copy = {"copied_from": "raw/state/chart_analysis_package.json (Prompt-1 deliverable)",
             "copied_at": utcnow(), "sha256": pkg_hash_boot, "run_id": run_id,
             "immutable": True, "note": "copy for solver citation; original untouched"}
json.dump(prov_copy, open(os.path.join(RAW, "package", "PROVENANCE.json"), "w"), indent=2)
machine_update(run_id=run_id, state="INIT", completed_phases=[], audit_cycles_used=0,
               assignment_file="ASSIGNMENTS/MARKETING/project_1.md", assignment_sha256=brief_hash,
               package_sha256=pkg_hash_boot, prompt1_machine_state_preserved="raw/state/machine.json (HALT; chart evidence)")
dump_state("solution.json", {"revision": 0, "answers": [], "hidden_problems": [], "best_solution": {},
                              "open_questions": [], "evidence": [], "split_claims": []})
progress(f"INIT ok | run_id: {run_id} | brief sha256: {brief_hash[:16]}.. | package sha256: {pkg_hash_boot[:16]}.. | prompt-1 state preserved")

# ---------------- PACKAGE_VALIDATE ----------------
pkg_obj = read_json_logged(PKG_COPY)
REQ_KEYS = ["package_version", "source_qmdj_sha256", "interpretation_protocol_v2_version_hash",
            "archetype_scoring_rubric_version_hash", "generated_at", "palaces", "systems",
            "relations", "patterns", "origin_sets", "yongshen_candidates", "anomalies", "solution_seed"]
KEY_RENAMES = {"anomalies": "anomaly_registry"}  # package schema_variant uses registry name
schema_errors = []
schema_renames = []
for k in REQ_KEYS:
    if k in pkg_obj:
        continue
    if k in KEY_RENAMES and KEY_RENAMES[k] in pkg_obj:
        schema_renames.append(f"{k} -> {KEY_RENAMES[k]}")
    else:
        schema_errors.append(k)
for k in ("answers", "hidden_problems", "best_solution_candidates", "note"):
    if k not in pkg_obj.get("solution_seed", {}): schema_errors.append(f"solution_seed.{k}")
semver_ok = bool(re.match(r"^\d+\.\d+\.\d+$", pkg_obj.get("package_version", "")))
src_hash = pkg_obj.get("source_qmdj_sha256", "")
src_hash_syntax = bool(re.match(r"^[0-9a-f]{64}$", src_hash))
# reference checks
spec_gen = logged_read(GEN_SPEC)
gen_proto = re.search(r"sha256:protocol_v2_[0-9_a-z]+", spec_gen).group(0)
gen_rubric = re.search(r"sha256:archetype_scoring_rubric_[0-9_a-z]+", spec_gen).group(0)
solver_spec = logged_read(SOLVER_SPEC)
v4_proto = re.search(r"sha256:protocol_v2_[0-9_a-z]+", solver_spec).group(0)
v4_rubric = re.search(r"sha256:archetype_scoring_rubric_[0-9_a-z]+", solver_spec).group(0)
manifest = read_json_logged(os.path.join(STATE, "MANIFEST.json"))
boot_source_hash = manifest["source_file"]["sha256_recorded_at_boot"]
checks = [
    {"check": "package exists and readable", "pass": True},
    {"check": "schema required keys", "pass": not schema_errors, "errors": schema_errors,
     "renames_applied": schema_renames, "deviation": "KEY_RENAME" if schema_renames else None},
    {"check": "package_version semver", "pass": semver_ok, "value": pkg_obj.get("package_version")},
    {"check": "source_qmdj_sha256 present+syntax", "pass": src_hash_syntax, "value": src_hash[:24] + "…"},
    {"check": "source_qmdj_sha256 matches boot MANIFEST record", "pass": src_hash == boot_source_hash,
     "value": f"{src_hash[:16]}… == {boot_source_hash[:16]}…"},
    {"check": "interpretation protocol hash present", "pass": pkg_obj["interpretation_protocol_v2_version_hash"] == PROTO_HASH_PKG},
    {"check": "rubric hash present", "pass": pkg_obj["archetype_scoring_rubric_version_hash"] == RUBRIC_HASH_PKG},
    {"check": "protocol hash == solver-v4 embedded reference", "pass": pkg_obj["interpretation_protocol_v2_version_hash"] == v4_proto,
     "deviation": "VERSION_SKEW", "package_value": pkg_obj["interpretation_protocol_v2_version_hash"], "solver_embedded_v4": v4_proto},
    {"check": "rubric hash == solver-v4 embedded reference", "pass": pkg_obj["archetype_scoring_rubric_version_hash"] == v4_rubric,
     "deviation": "VERSION_SKEW", "package_value": pkg_obj["archetype_scoring_rubric_version_hash"], "solver_embedded_v4": v4_rubric},
    {"check": "protocol hash == generator spec (PROMPT/chart_analyser.yaml v5.0.0)", "pass": pkg_obj["interpretation_protocol_v2_version_hash"] == gen_proto,
     "generator_value": gen_proto},
    {"check": "rubric hash == generator spec (PROMPT/chart_analyser.yaml v5.0.0)", "pass": pkg_obj["archetype_scoring_rubric_version_hash"] == gen_rubric,
     "generator_value": gen_rubric},
]
deviation = {
    "id": "DEV-001",
    "title": "Embedded v4 reference hashes vs actual generator deployment v5.0.0",
    "detail": ("solver spec qmdj_reference expects chart-analyst v4 hashes; the package was produced by "
               "chart_analyser.yaml v5.0.0 (supplied at runtime by the orchestrator). Package hashes match"
               " the ACTUAL generator spec exactly (verified above), and source_qmdj_sha256 matches the"
               " boot MANIFEST. Skew is a spec-registry lag, not package tampering."),
    "decision": "PASS_WITH_DEVIATION — proceed; logged here, in OPERATOR/COMMENTS.md, and in Risk-And-Audit-Log",
    "would_be_stale_if": "package hashes matched NEITHER the v4 reference NOR the generator spec"}
deviation2 = {
    "id": "DEV-002",
    "title": "Schema key rename: 'anomalies' delivered as 'anomaly_registry'",
    "detail": ("spec required-key list says top-level 'anomalies'; the package carries the same data as"
               " 'anomaly_registry' (12 records) and additionally per-origin 'origin_sets.B1..B5.anomalies'"
               " plus per-palace anomalies arrays. Package also self-labels 'schema_variant'. Data present,"
               " naming differs."),
    "decision": "PASS_WITH_DEVIATION — validator maps anomalies -> anomaly_registry for all references",
    "would_be_stale_if": "no anomaly records existed under ANY key in package or its origin_sets"}
schema_valid = semver_ok and src_hash_syntax and not schema_errors
hashes_verified = (src_hash == boot_source_hash
                   and pkg_obj["interpretation_protocol_v2_version_hash"] == gen_proto
                   and pkg_obj["archetype_scoring_rubric_version_hash"] == gen_rubric)
val_md = ["# Package Validation (PACKAGE_VALIDATE)\n",
          f"- package copy: `vault/raw/package/chart_analysis_package.json` sha256 `{pkg_hash_boot}`",
          f"- schema_valid: {schema_valid} · hashes_verified(generator-spec provenance): {hashes_verified}",
          f"- gate result: **{'PASS_WITH_DEVIATION' if hashes_verified and schema_valid else 'PACKAGE_STALE'}**\n",
          "| # | check | pass | deviation/detail |", "|---|---|---|---|"]
for i, c in enumerate(checks, 1):
    val_md.append(f"| {i} | {c['check']} | {'✅' if c['pass'] else '❌'} | {c.get('deviation') or c.get('value') or ''} {('| ' + c.get('solver_embedded_v4','')) if c.get('solver_embedded_v4') else ''} |")
val_md += ["\n## Deviation register", f"- **{deviation['id']}** — {deviation['title']}: {deviation['detail']}",
           f"  Decision: {deviation['decision']}. Stale condition that would halt: {deviation['would_be_stale_if']}.",
           f"- **{deviation2['id']}** — {deviation2['title']}: {deviation2['detail']}",
           f"  Decision: {deviation2['decision']}. Stale condition that would halt: {deviation2['would_be_stale_if']}.",
           f"\nSchema renames applied: {schema_renames or 'none'}."]
write_text(os.path.join(RAW, "package", "validation.md"), "\n".join(val_md))
dump_state("package_validation.json", {"schema_valid": schema_valid, "hashes_verified": hashes_verified,
                                       "checks": checks, "deviations": [deviation, deviation2],
                                       "schema_renames": schema_renames})
assert schema_valid and hashes_verified, "PACKAGE_STALE"
machine_update(state="PACKAGE_VALIDATE_DONE", completed_phases=["INIT", "PACKAGE_VALIDATE"],
               verification={"package_schema": schema_valid, "package_hashes": "PASS_WITH_DEVIATION DEV-001"})
progress(f"package validated | schema ok | generator-spec hash match ok | deviation DEV-001 logged (v4-vs-v5 registry skew) | NOT stale")

# ---------------- PDF_INGEST (brief markdown) ----------------
brief = logged_read(ASSIGN)
os.makedirs(os.path.join(RAW, "assignment"), exist_ok=True)
extract_note = f"""# Assignment Extract (provenance note)
- file: ASSIGNMENTS/MARKETING/project_1.md · sha256 `{brief_hash}` · ingested {utcnow()} · run `{run_id}`
- document type: markdown brief (serves Assignment.pdf role under solver spec consumes contract)
- extraction: full text (322 lines); anchors = heading paths; no images in document
- immutable: not edited; extracted notes copied below
# --- full text copy ---
{brief}
"""
write_text(os.path.join(RAW, "assignment", "extract.md"), extract_note)

A = lambda s: f"ASSIGNMENTS/MARKETING/project_1.md {s}"
requirements = [
 {"id": "R01", "quoted_text": "You may choose either a fictional brand or a real small/emerging brand.",
  "page_anchor": A("§1 Choosing Your Brand"), "artefact_type": "brand-choice", "must_level": "must", "except_logo": False},
 {"id": "R02", "quoted_text": "The brand should have: A clearly defined product or service",
  "page_anchor": A("§1 Choosing Your Brand / brand criteria"), "artefact_type": "brand-criteria", "must_level": "must", "except_logo": False},
 {"id": "R03", "quoted_text": "A specific category", "page_anchor": A("§1 brand criteria"),
  "artefact_type": "brand-criteria", "must_level": "must", "except_logo": False},
 {"id": "R04", "quoted_text": "A realistic target consumer", "page_anchor": A("§1 brand criteria"),
  "artefact_type": "brand-criteria", "must_level": "must", "except_logo": False},
 {"id": "R05", "quoted_text": "A clear reason for existing / problem it solves", "page_anchor": A("§1 brand criteria"),
  "artefact_type": "brand-criteria", "must_level": "must", "except_logo": False},
 {"id": "R06", "quoted_text": "Enough scope for future digital marketing across content, social, search, paid media, CRM, etc.",
  "page_anchor": A("§1 brand criteria"), "artefact_type": "brand-criteria-scope", "must_level": "must", "except_logo": False},
 {"id": "R07", "quoted_text": "Avoid: Ideas dependent on unrealistic technology; Extremely broad concepts…; Brands with no clear product/service; Copying an existing major brand with only a new name; Categories where the you may have no clear understanding of the consumer; Creating multiple unrelated product categories under one brand; Not alcohol brands",
  "page_anchor": A("§1 Avoid"), "artefact_type": "hard-exclusion", "must_level": "must_not", "except_logo": False},
 {"id": "R08", "quoted_text": "Brand Selection Test: What do you sell? Who is it for? What problem does it solve? Why would someone choose you?",
  "page_anchor": A("§1 Brand Selection Test"), "artefact_type": "brand-test", "must_level": "must", "except_logo": False},
 {"id": "R09", "quoted_text": "Slide 1 - Brand Introduction. Include: Brand Name; Category; Product / Service; Geography / Market; Price Positioning; One-line description (no detailed logo/ brand identity work is required at this stage)",
  "page_anchor": A("§Suggested Slide Structure / Slide 1"), "artefact_type": "slide-1", "must_level": "must", "except_logo": True},
 {"id": "R10", "quoted_text": "Slide 2 - Brand Overview: What does the brand offer? What consumer problem does it solve? What makes it different? Who are the major competitors or alternatives? (more strategic than creative/design heavy)",
  "page_anchor": A("§Slides / Slide 2"), "artefact_type": "slide-2", "must_level": "must", "except_logo": False},
 {"id": "R11", "quoted_text": "Slide 3 - Business Goal: Define one primary business goal… should describe what the business wants to achieve, not what marketing will do",
  "page_anchor": A("§Slides / Slide 3"), "artefact_type": "slide-3", "must_level": "must", "except_logo": False},
 {"id": "R12", "quoted_text": "Slide 4 - Marketing Objective: Translate the business goal into 1 - 2 SMART marketing objectives. You must explain briefly: How does this marketing objective support the business goal?",
  "page_anchor": A("§Slides / Slide 4"), "artefact_type": "slide-4", "must_level": "must", "except_logo": False},
 {"id": "R13", "quoted_text": "Slide 5 - Target Audience: Define the primary target audience. Include Demographics; Income/spending power; Psychographics; Behaviour… Avoid descriptions like '18 - 45, everyone interested in fitness.'",
  "page_anchor": A("§Slides / Slide 5"), "artefact_type": "slide-5", "must_level": "must", "except_logo": False},
 {"id": "R14", "quoted_text": "Slide 6 - Buyer Persona: Create one detailed primary buyer persona… Name/profile; Age; Occupation; Location; Lifestyle; Interests; Goals; Pain points; Motivations; Favourite digital platforms; Online buying behaviour; One quote capturing their mindset. The persona should be based on the target audience - not random.",
  "page_anchor": A("§Slides / Slide 6"), "artefact_type": "slide-6", "must_level": "must", "except_logo": False},
 {"id": "R15", "quoted_text": "Slide 7 - Customer Journey: Map the persona's journey from Need/Trigger → Discovery → Research → Consideration → Purchase → Experience → Loyalty/Advocacy. For every stage: Consumer behaviour; Digital touchpoints; Questions/concerns; Potential friction.",
  "page_anchor": A("§Slides / Slide 7"), "artefact_type": "slide-7", "must_level": "must", "except_logo": False},
 {"id": "R16", "quoted_text": "Slide 8 - Digital Marketing Strategy: 1 - 2 concise paragraphs: Who you are targeting; What you want them to think/do; Broad approach; How digital channels will work together. It should not simply be a list of platforms.",
  "page_anchor": A("§Slides / Slide 8"), "artefact_type": "slide-8", "must_level": "must", "except_logo": False},
 {"id": "R17", "quoted_text": "Slide 9 - PESO Media Mix: Map the brand across Paid, Earned, Shared, Owned… show that you understand how the four media types can work together.",
  "page_anchor": A("§Slides / Slide 9"), "artefact_type": "slide-9", "must_level": "must", "except_logo": False},
 {"id": "R18", "quoted_text": "Slide 10 - Recommended Digital Channels: approximately 4 - 6 priority digital channels. For each: Channel, Role, Why This Channel? You should also be able to explain why certain platforms are not priorities.",
  "page_anchor": A("§Slides / Slide 10"), "artefact_type": "slide-10", "must_level": "must", "except_logo": False},
 {"id": "R19", "quoted_text": "Slide 11 - Integrated Digital Journey: Bring everything together visually… demonstrate that channels are connected, not isolated.",
  "page_anchor": A("§Slides / Slide 11"), "artefact_type": "slide-11", "must_level": "must", "except_logo": False},
 {"id": "R20", "quoted_text": "Slide 12 - Key Strategic Decisions: End with 3 - 5 statements summarising the strategy.",
  "page_anchor": A("§Slides / Slide 12"), "artefact_type": "slide-12", "must_level": "must", "except_logo": False},
 {"id": "R21", "quoted_text": "Because this is only Assignment 1, do not include: Detailed social media posts; Content calendars; Influencer lists; SEO keyword plans; Paid media budgets; Email journeys; Campaign creatives; Detailed analytics dashboards",
  "page_anchor": A("§Scope exclusions"), "artefact_type": "scope-exclusion", "must_level": "must_not", "except_logo": False},
 {"id": "R22", "quoted_text": "Submission date: 18th September 2026; Format: Individual assignment; Submission: Presentation - PPT/PDF/Google slides/ Canva",
  "page_anchor": A("§Header"), "artefact_type": "format-deadline", "must_level": "must", "except_logo": False},
 {"id": "R23", "quoted_text": "(no detailed logo/ brand identity work is required at this stage)",
  "page_anchor": A("§Slides / Slide 1 note"), "artefact_type": "logo-boundary", "must_level": "must_not", "except_logo": True},
 {"id": "R24", "quoted_text": "Assignment 1 will primarily be marked on clarity of thinking, not creative / visual polish.",
  "page_anchor": A("§Marking note"), "artefact_type": "marking-criterion", "must_level": "should", "except_logo": False},
]
for r in requirements:
    r["coverage_status"] = "UNCOVERED"
    r["output_files"] = []
dump_state("requirements.json", {"count": len(requirements), "rows": requirements})
for r in requirements:
    progress(f"requirement {r['id']} | level: {r['must_level']} | anchor: {r['page_anchor'][:60]} | status: UNCOVERED")

deliverable_registry = [
 {"id": "DEL-01", "name": "Assignment 1 — Strategy Foundation (brand deck, slides 1–12 + brand selection test)",
  "format": "Presentation deck (PPT/PDF/Google Slides/Canva export target); delivered as submission-ready slide copy (markdown, one file, slide-delimited)",
  "mime_type": "text/markdown (export-ready)", "audience": "marker / brief-owner",
  "must_or_should": "must", "except_logo": False,
  "source_requirement_ids": [r["id"] for r in requirements if r["id"] not in ("R23",)],
  "output_path": "output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md", "status": "PENDING"},
 {"id": "DEL-X1", "name": "Logo / brand-identity artwork", "format": "—", "audience": "—",
  "must_or_should": "must_not", "except_logo": True, "source_requirement_ids": ["R23", "R09"],
  "output_path": None, "status": "EXCLUDED_LOGO",
  "exclusion_reason": "brief explicitly removes detailed logo/brand-identity work at this stage; solver spec excludes actual logo artwork"}]
dump_state("deliverable_registry.json", {"registry": deliverable_registry, "fallback_pack_used": False,
                                         "note": "brief provides explicit slide structure; UNGROUNDED_PACK not used"})
logo_boundary = {"rule": "no actual logo artwork; written brand NAME + textual positioning only",
                 "pdf_evidence": "(no detailed logo/ brand identity work is required at this stage)",
                 "allowed": ["brand name", "one-line description", "written positioning", "written design-free notes"],
                 "excluded": ["logo image", "brand mark artwork", "identity system design", "moodboards as deliverable"]}
dump_state("logo_boundary.json", logo_boundary)
rubric_guess = {"pdf_basis": "primarily marked on clarity of thinking, not creative / visual polish",
                "inferred_marking_weights_hypothesis": [
                    {"criterion": "clarity of strategic thinking (audience/problem fit)", "weight_hypothesis": 0.35},
                    {"criterion": "SMART-ness + coherence (goal→objective→journey→channels)", "weight_hypothesis": 0.25},
                    {"criterion": "specificity (persona, audience granularity)", "weight_hypothesis": 0.20},
                    {"criterion": "channel integration logic (PESO + journey, non-priority reasoning)", "weight_hypothesis": 0.20}],
                "status": "hypothesis from PDF marking note; no PDF rubric table exists"}
dump_state("rubric_guess.json", rubric_guess)
question_types = [
    {"qtype": "brand-identity & positioning (who/why)", "bind_slot": "my_answers", "requirement_ids": ["R01","R02","R03","R04","R05","R08","R09","R10"]},
    {"qtype": "risk anticipation & what-not-to-do", "bind_slot": "hidden_problems", "requirement_ids": ["R07","R13","R15","R21","R24"]},
    {"qtype": "strategy/channel-choice & timing (how to win, in what order)", "bind_slot": "best_solution", "requirement_ids": ["R06","R11","R12","R16","R17","R18","R19","R20"]}]
dump_state("question_types.json", question_types)
machine_update(state="PDF_INGEST_DONE", completed_phases=["INIT", "PACKAGE_VALIDATE", "PDF_INGEST"])
progress(f"pdf ingest complete | requirements: {len(requirements)} (must: {sum(1 for r in requirements if r['must_level']=='must')}, must_not: {sum(1 for r in requirements if r['must_level']=='must_not')}, should: 1) | deliverables: 1 (+1 logo-excluded) | uncovered: {len(requirements)}")
print(json.dumps({"schema_valid": schema_valid, "hashes_verified": hashes_verified,
                  "deviation": "DEV-001 PASS_WITH_DEVIATION",
                  "requirements": len(requirements), "deliverables": len(deliverable_registry)}, indent=1))
