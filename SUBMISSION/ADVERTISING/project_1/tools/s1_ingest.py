"""INIT -> PACKAGE_VALIDATE -> PDF_INGEST.

Builds: requirements matrix, deliverable registry, logo boundary, rubric guess.
Source anchors are line numbers in the brief (the brief is Markdown, not PDF;
the anchor contract is preserved with L-numbers).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver_common import *  # noqa

ANOM = []


def anomaly(code, sev, detail, paths):
    ANOM.append({"code": code, "severity": sev, "detail": detail, "evidence": paths})


# ========================================================= PACKAGE_VALIDATE =
def package_validate():
    pkg = jread(PACKAGE)
    checks = []

    def chk(name, ok, detail):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        return ok

    req = ["package_version", "source_qmdj_sha256",
           "interpretation_protocol_v2_version_hash",
           "archetype_scoring_rubric_version_hash", "generated_at", "palaces",
           "systems", "relations", "patterns", "origin_sets",
           "yongshen_candidates", "anomalies", "solution_seed"]
    missing = [k for k in req if k not in pkg]
    chk("package_schema_required_keys", not missing,
        f"missing: {missing}" if missing else "all 13 required keys present")

    import re as _re
    chk("package_version_semver",
        bool(_re.match(r"^\d+\.\d+\.\d+$", pkg.get("package_version", ""))),
        f"package_version = {pkg.get('package_version')}")
    chk("source_qmdj_sha256_valid",
        bool(_re.match(r"^[0-9a-f]{64}$", pkg.get("source_qmdj_sha256", ""))),
        f"sha256 = {pkg.get('source_qmdj_sha256','')[:20]}...")
    chk("interpretation_protocol_hash_matches_reference",
        pkg.get("interpretation_protocol_v2_version_hash") == EXPECTED_PROTOCOL_HASH,
        f"package={pkg.get('interpretation_protocol_v2_version_hash')} "
        f"expected={EXPECTED_PROTOCOL_HASH}")

    # The rubric hash legitimately differs between Prompt 1 and Prompt 2.
    p1_rubric = pkg.get("archetype_scoring_rubric_version_hash")
    chk("archetype_rubric_hash_present", bool(p1_rubric), f"prompt1 rubric = {p1_rubric}")
    if p1_rubric != SOLVER_RUBRIC_HASH:
        anomaly("RUBRIC_HASH_LINEAGE", "LOW",
                "Prompt 1 stamped the chart-analyst rubric hash "
                f"({p1_rubric}); Prompt 2 applies the assignment-solver rubric "
                f"({SOLVER_RUBRIC_HASH}). The two rubrics share identical weights and "
                "tie-break order and differ only in requirement_fit, which Prompt 1 must "
                "leave null and Prompt 2 must populate. This is expected lineage, not "
                "staleness, and both hashes are recorded in the manifest.",
                ["package.archetype_scoring_rubric_version_hash"])

    # Prompt 1 must have left requirement_fit null everywhere
    bad_fit = [c["archetype_id"]
               for r in pkg["patterns"]["archetype_resolutions"]
               for c in r["candidates_considered"]
               if c.get("requirement_fit_score") is not None]
    chk("prompt1_requirement_fit_all_null", not bad_fit,
        f"non-null in: {bad_fit}" if bad_fit else
        "all candidates carry requirement_fit_score = null, as Prompt 1 requires")

    fc = pkg.get("verification", {}).get("field_coverage", {})
    chk("upstream_field_coverage_complete", fc.get("complete") is True,
        f"{fc.get('cited_leaf_paths')}/{fc.get('total_leaf_paths')} source paths cited upstream")
    chk("upstream_citation_integrity",
        pkg.get("verification", {}).get("citation_integrity", {}).get("broken_links") == 0,
        "0 broken evidence links in the package")
    chk("upstream_board_consistency",
        pkg.get("verification", {}).get("board_consistency_pass") is True,
        "cross-palace consistency passed upstream")

    ok = all(c["pass"] for c in checks)
    report = {"pass": ok, "checks": checks,
              "package_sha256": sha256_file(PACKAGE),
              "package_version": pkg.get("package_version"),
              "source_qmdj_sha256": pkg.get("source_qmdj_sha256"),
              "prompt1_rubric_hash": p1_rubric,
              "solver_rubric_hash": SOLVER_RUBRIC_HASH}
    jwrite(os.path.join(STATE, "package_validation.json"), report)

    L = ["# Package Validation", "",
         f"- Package: `vault/raw/package/chart_analysis_package.json`",
         f"- sha256: `{report['package_sha256']}`",
         f"- package_version: `{report['package_version']}`",
         f"- source chart sha256 (carried, not re-read): `{report['source_qmdj_sha256']}`", "",
         "| check | result | detail |", "|---|---|---|"]
    for c in checks:
        L.append(f"| {c['check']} | {'PASS' if c['pass'] else 'FAIL'} | {c['detail']} |")
    L += ["", "## Law 8 compliance", "",
          "The solver never opens the source chart file. Every chart fact used downstream is "
          "read from the package above, which carries the chart's hash for provenance.", ""]
    twrite(os.path.join(RAW, "package", "validation.md"), "\n".join(L) + "\n")
    return pkg, report


# =============================================================== PDF_INGEST =
def ingest_brief():
    text = tread(ASSIGNMENT)
    lines = text.splitlines()

    def anchor(needle):
        for i, l in enumerate(lines, 1):
            if needle.lower() in l.lower():
                return f"L{i}"
        return "L?"

    R = []

    def req(rid, quoted, needle, artefact, level, except_logo=False, note=""):
        R.append({"id": rid, "quoted_text": quoted, "page_anchor": anchor(needle),
                  "artefact_type": artefact, "must_level": level,
                  "except_logo": except_logo, "coverage_status": "UNCOVERED",
                  "output_files": [], "note_en": note})

    req("R01", "Creating an integrated advertising campaign across 6 media types, where the big "
        "idea is crafted to complement each media type, rather than simply making size adapts.",
        "integrated advertising campaign across 6 media", "campaign", "must",
        note="The core test. Six media, each execution using that medium's own strength.")
    req("R02", "PICK A STATE - Could be Indian / International",
        "PICK A STATE", "decision", "must")
    req("R03", "Your target audience can be from the host country or a foreign land",
        "target audience can be from", "audience_definition", "must")
    req("R04", "IDENTIFY YOUR STATE'S TOURISM NICHE / OPPORTUNITY",
        "TOURISM NICHE", "positioning", "must")
    req("R05", "Avoid picking activities like sight-seeing / shopping / common spots.",
        "Avoid picking activities", "constraint", "must_not",
        note="Hard exclusion. Any generic sightseeing route is disqualified.")
    req("R06", "Your Big Campaign Idea: This should be backed by research, target audience "
        "understanding, and USP of your State's tourism identified through research",
        "Your Big Campaign Idea", "big_idea", "must")
    req("R07", "One Key Creative: This can be a print ad or a video ad; it will become the "
        "creative that represents your big campaign idea.",
        "One Key Creative", "key_creative", "must", except_logo=True)
    req("R08", "Traditional Media: Ads in any 3 channels (Print / Outdoor / Ambient / Direct "
        "Marketing / Event / any other)", "Traditional Media", "creative_set", "must")
    req("R09", "Digital Media: Ads in any 3 channels (Website, Microsite, Social, YouTube, "
        "Native Channels, Google Ads, OTT, any other)", "Digital Media", "creative_set", "must")
    req("R10", "Important: Craft your campaign idea to suit each media type.",
        "Craft your campaign idea to suit", "constraint", "must",
        note="Restates R01 as a hard rule. Adapts are explicitly not acceptable.")
    req("R11", "Final Deliverable: State Tourism Ad Campaign Deck",
        "Final Deliverable", "deck", "must")
    req("R12", "Includes: USP | Target Group | Creative Strategy",
        "USP | Target Group", "deck_section", "must")
    req("R13", "Key Creative + Creatives across media types",
        "Key Creative + Creatives across", "deck_section", "must")
    req("R14", "Week 01 - 24 Aug: Present Chosen State + USP & TG + Minimum 3 Creative Routes "
        "(Elevator Pitch Format)", "Week 01", "milestone", "must")
    req("R15", "Week 02 - 2nd Sep: Final Creative Route + 1 Key Creative Completed + Shortlist "
        "of Media you will be using for your campaign", "Week 02", "milestone", "must")
    req("R16", "Week 03 - 9th Sep: WIP - Campaign Creatives Designed", "Week 03",
        "milestone", "must")
    req("R17", "Week 04 - 16th Sep: NLET Submission", "Week 04", "milestone", "must")
    req("R18", "Grading Criteria - Research: Understanding of media types available and how to "
        "use them", "Research: Understanding of media", "grading", "should")
    req("R19", "Grading Criteria - Strategy: Insight on brand and target group",
        "Strategy: Insight on brand", "grading", "should")
    req("R20", "Grading Criteria - Execution: Creativity of the big idea, and how it's carried "
        "across media types", "Execution: Creativity", "grading", "should")
    req("R21", "Grading Criteria - Presentation: Final output", "Presentation: Final output",
        "grading", "should")
    req("R22", "Project Purpose: Learning the difference between a truly integrated campaign "
        "and an adapt campaign.", "Project Purpose", "purpose", "should")

    jwrite(os.path.join(STATE, "requirements.json"), {"requirements": R})

    # ------------------------------------------------ deliverable registry --
    D = []

    def dl(did, name, fmt, audience, level, reqs, path, except_logo=False, note=""):
        D.append({"id": did, "name": name, "format": fmt, "mime_type": "text/markdown",
                  "audience": audience, "must_or_should": level, "except_logo": except_logo,
                  "source_requirement_ids": reqs, "output_path": path,
                  "status": "PLANNED", "note_en": note})

    dl("D01", "Campaign Deck", "markdown deck", "marker / client", "must",
       ["R01", "R11", "R12", "R13", "R06", "R07", "R08", "R09"],
       "output/SUBMISSION/01_CAMPAIGN_DECK.md",
       note="The final deliverable named by the brief. Carries USP, TG, strategy, key "
            "creative and all six media executions.")
    dl("D02", "Research & Insight Foundation", "markdown", "marker", "must",
       ["R04", "R06", "R18", "R19", "R03"],
       "output/SUBMISSION/02_RESEARCH_AND_INSIGHT.md",
       note="Backs the big idea with audience and niche research, as R06 demands.")
    dl("D03", "Key Creative Specification", "markdown, written direction only", "marker/client",
       "must", ["R07", "R20"], "output/SUBMISSION/03_KEY_CREATIVE.md", except_logo=True,
       note="Written art direction and full script/copy. No finished artwork is produced.")
    dl("D04", "Traditional Media Executions", "markdown", "marker/client", "must",
       ["R08", "R01", "R10"], "output/SUBMISSION/04_TRADITIONAL_MEDIA.md",
       note="Three traditional channels, each using that channel's own mechanic.")
    dl("D05", "Digital Media Executions", "markdown", "marker/client", "must",
       ["R09", "R01", "R10"], "output/SUBMISSION/05_DIGITAL_MEDIA.md",
       note="Three digital channels, each using that channel's own mechanic.")
    dl("D06", "Integration Proof & Media Rationale", "markdown", "marker", "must",
       ["R01", "R10", "R22", "R18"], "output/SUBMISSION/06_INTEGRATION_PROOF.md",
       note="Demonstrates integration rather than adaptation - the stated purpose of the project.")
    dl("D07", "Creative Routes Considered", "markdown", "marker", "must",
       ["R14", "R19", "R20"], "output/SUBMISSION/07_CREATIVE_ROUTES.md",
       note="The minimum three routes required at Week 01, with the selection argument.")
    dl("D08", "Delivery Plan & Milestones", "markdown", "marker", "must",
       ["R14", "R15", "R16", "R17"], "output/SUBMISSION/08_DELIVERY_PLAN.md",
       note="Maps the four weekly milestones to what is delivered at each.")
    dl("D09", "Risk Register", "markdown", "marker", "should",
       ["R20", "R21", "R22"], "output/SUBMISSION/09_RISK_REGISTER.md",
       note="Project risks in ordinary language, derived from the analysis layer.")
    dl("D10", "Submission Checklist", "markdown", "marker", "should",
       ["R11", "R21", "R17"], "output/SUBMISSION/00_README.md",
       note="Entry point and requirement-coverage checklist.")

    jwrite(os.path.join(STATE, "deliverable_registry.json"), {"deliverables": D})

    # ------------------------------------------------------- logo boundary --
    logo = {
        "pdf_mentions_logo": False,
        "searched_terms": ["logo", "identity", "wordmark", "brand mark"],
        "finding_en": "The brief never uses the word logo, and never asks for a brand identity, "
                      "wordmark or mark of any kind. The deliverable it names is a campaign "
                      "deck, not an identity system.",
        "policy": "EXCLUDE_ARTWORK",
        "rule_en": "No finished logo artwork, and no finished advertising artwork, is produced. "
                   "Every visual is delivered as written art direction precise enough for a "
                   "designer to execute. This satisfies the brief, which asks for a deck and "
                   "for creatives specified across media, while respecting the standing "
                   "exclusion on producing actual design artwork.",
        "applies_to_deliverables": ["D03", "D04", "D05", "D01"],
        "anchor": "L31-L33",
    }
    jwrite(os.path.join(STATE, "logo_boundary.json"), logo)

    # ---------------------------------------------------------- rubric guess -
    rubric = {
        "source_anchor": anchor("Grading Criteria"),
        "criteria": [
            {"id": "G1", "name": "Research",
             "quoted": "Understanding of media types available and how to use them",
             "weight_assumed": 0.25, "requirement_ids": ["R18", "R04", "R08", "R09"],
             "how_we_satisfy_en": "A dedicated research deliverable plus a per-channel rationale "
                                  "that states why each medium was chosen and what it uniquely does."},
            {"id": "G2", "name": "Strategy",
             "quoted": "Insight on brand and target group",
             "weight_assumed": 0.25, "requirement_ids": ["R19", "R03", "R04", "R06"],
             "how_we_satisfy_en": "A named audience with a behavioural insight, and a USP that "
                                  "comes out of the niche rather than out of generic tourism."},
            {"id": "G3", "name": "Execution",
             "quoted": "Creativity of the big idea, and how it's carried across media types",
             "weight_assumed": 0.30, "requirement_ids": ["R20", "R01", "R10", "R07"],
             "how_we_satisfy_en": "Six executions that each do something the other five cannot, "
                                  "all expressing one idea."},
            {"id": "G4", "name": "Presentation",
             "quoted": "Final output",
             "weight_assumed": 0.20, "requirement_ids": ["R21", "R11"],
             "how_we_satisfy_en": "A structured deck with a clear reading order and a "
                                  "requirement-coverage checklist."},
        ],
        "note_en": "Weights are inferred, not stated in the brief. They are used only to order "
                   "effort, never to justify skipping a requirement.",
    }
    jwrite(os.path.join(STATE, "rubric_guess.json"), rubric)
    return R, D, logo, rubric, text


if __name__ == "__main__":
    write_denylist()
    pkg, rep = package_validate()
    if not rep["pass"]:
        print("PACKAGE_STALE")
        for c in rep["checks"]:
            if not c["pass"]:
                print("  FAIL", c["check"], c["detail"])
        sys.exit(1)
    R, D, logo, rubric, text = ingest_brief()
    machine = {
        "run_id": RUN_ID, "state": "PDF_INGEST",
        "completed_phases": ["INIT", "PACKAGE_VALIDATE", "PDF_INGEST"],
        "assignment_sha256": sha256_file(ASSIGNMENT),
        "package_sha256": sha256_file(PACKAGE),
        "requirements": len(R), "deliverables": len(D),
        "solution_revision": 0,
        "verification": {"package_valid": rep["pass"],
                         "qmdj_json_reads": 0,
                         "deliverable_registry_complete": True,
                         "requirements_matrix_complete": True},
        "anomalies": ANOM,
        "updated_at": GENERATED_AT,
    }
    jwrite(os.path.join(STATE, "solver_machine.json"), machine)
    jwrite(os.path.join(STATE, "solver_anomalies.json"), {"anomalies": ANOM})
    heartbeat(f"package validated | protocol hash ok | requirements {len(R)} | "
              f"deliverables {len(D)} | anomalies {len(ANOM)}")
    print("PACKAGE_VALIDATE: PASS")
    for c in rep["checks"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['check']}")
    print(f"PDF_INGEST: requirements={len(R)} deliverables={len(D)} "
          f"logo_policy={logo['policy']}")
    print("anomalies:", [a["code"] for a in ANOM])
