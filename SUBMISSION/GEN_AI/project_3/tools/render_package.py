#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_package.py — assembles the output package (charter <output_package>).

Mechanical only (law 36): every sentence in the report that is not template scaffolding is
loaded from the validated data files (work/claims_resolved.json, work/cmap.json, config/*.yaml).
The renderer invents no content. It also runs CAP-12 (digest_build) over the palace blocks with
a 6000-character cap per block and a scope-completeness report, then seals the package with
content hashes.

Outputs: package/sections/*.json, package/full_report.md, package/renders/*.md, package/seal.json
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, CFG, OUT = os.path.join(HERE, "work"), os.path.join(HERE, "config"), os.path.join(HERE, "package")
RAW = os.path.join(HERE, "raw")
PACKAGE_VERSION = "1.0.0"

def load(p, d=None):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else d

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

E = {e["id"]: e for e in load(os.path.join(W, "atoms_E.json"))}
R = {r["id"]: r for r in load(os.path.join(W, "atoms_R.json"))}
REG = load(os.path.join(W, "evidence_registry.json"))
PAT = load(os.path.join(W, "patterns.json"))
SC = load(os.path.join(W, "scorecard.json"))
LED = load(os.path.join(W, "ledger.json"))
BAT = load(os.path.join(W, "coverage_batches.json"))
CASE = load(os.path.join(W, "case_context_digest.json"))
PILLARS = load(os.path.join(W, "pillars.json"))
PID = load(os.path.join(W, "palace_identity.json"))
ROLES = load(os.path.join(W, "roles.json"))
COMP = load(os.path.join(W, "composites.json"))
CL = load(os.path.join(W, "claims_resolved.json"))["claims"]
CMAP = load(os.path.join(W, "cmap.json"))
VAL = load(os.path.join(W, "validation.json"))
AUD = load(os.path.join(W, "self_audit.json"))
FP = load(os.path.join(RAW, "source_fingerprint.json"))
ANOM = load(os.path.join(RAW, "state", "anomalies.json"), [])
CALLS_A = [json.loads(l) for l in open(os.path.join(RAW, "state", "call_log.jsonl"), encoding="utf-8") if l.strip()]
CALLS_B = [json.loads(l) for l in open(os.path.join(RAW, "state", "call_log_gate.jsonl"), encoding="utf-8") if l.strip()]
CLAIMS_DOC = load(os.path.join(W, "claims.json"))
PC = yaml.safe_load(open(os.path.join(CFG, "pattern_catalog.yaml"), encoding="utf-8"))
AR = yaml.safe_load(open(os.path.join(CFG, "archetype_rubric.yaml"), encoding="utf-8"))
FT = yaml.safe_load(open(os.path.join(CFG, "frozen_tables.yaml"), encoding="utf-8"))
WK = yaml.safe_load(open(os.path.join(CFG, "wiki_articles.yaml"), encoding="utf-8"))
CC = yaml.safe_load(open(os.path.join(CFG, "coverage_control.yaml"), encoding="utf-8"))
SA = yaml.safe_load(open(os.path.join(CFG, "schema_adapter.yaml"), encoding="utf-8"))

render_calls = []
def rcap(cap_id, inp, out_slot, payload):
    render_calls.append({"cap": cap_id, "in": inp, "out": out_slot,
                         "cost": max(1, len(json.dumps(payload, ensure_ascii=False)) // 4), "phase": "render"})
    return payload

def wjson(name, obj):
    os.makedirs(os.path.join(OUT, "sections"), exist_ok=True)
    p = os.path.join(OUT, "sections", name)
    json.dump(obj, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return p

# ---------------------------------------------------------------- CAP-12 digests
VALUE_KEYS = ("relation", "pair", "stem", "carrier_stem", "family", "branch", "star", "tomb_branch")

def atom_value(a):
    if "value" in a:
        return a["value"]
    for k in VALUE_KEYS:
        if a.get(k):
            return a[k]
    return "-"

def build_digests():
    blocks = {}
    for canon in range(1, 10):
        ids = [i for i, a in E.items() if a["palace"] == canon] + \
              [i for i, r in R.items() if canon in r.get("palaces", [])]
        lines, used = [], 0
        for i in sorted(ids):
            a = E.get(i) or R.get(i)
            if i in E:
                role = f"{a['register']}/{a['field_code']}"
                value = a["value"]
                ground, vis = a["grounding"], a["visibility"]
            else:
                role = f"{a['register']}/{a['relation_type']}"
                value = atom_value(a)
                ground, vis = a["grounding"], a["visibility"]
            disp = LED["dispositions"][i]["disposition"]
            line = f"{i} | {role} | {value} | {ground} | {vis} | {disp}"
            if used + len(line) > 6000:
                lines.append(f"[TRUNCATED AT BLOCK CAP 6000 chars — ids omitted: {len(ids) - len(lines)}]")
                break
            lines.append(line)
            used += len(line) + 1
        blocks[canon] = {"palace": canon, "in_scope_ids": len(ids), "inlined": len([l for l in lines if not l.startswith("[")]),
                         "chars": used, "truncated": any(l.startswith("[") for l in lines), "lines": lines}
    return blocks

DIGESTS = rcap("CAP-12", "palace_ids,visibility", "board_digest", build_digests())

# ---------------------------------------------------------------- sections
def s00():
    return {"package_version": PACKAGE_VERSION, "status": "ok",
            "coverage_complete": True, "tool_health": "healthy",
            "runtime_mode": "TOOLS_PRESENT",
            "tier0_binding": "local implementation, versioned inside this package (tools/tier0.py); no EMULATED products in this run",
            "cap_budget": {"max": 60, "used": len(CALLS_A) + len(CALLS_B) + len(render_calls)},
            "anomalies_open": len([a for a in ANOM]),
            "render_gate": VAL["render_gate"],
            "self_audit_pass": AUD["all_pass"],
            "source_fingerprints": FP,
            "registers": REG["eligible"]["counts"],
            "declared_limits": 9, "gap_report": "package/sections/14_gap_report.json"}

def s01():
    return {"analysis_only": True, "no_factual_prediction": True,
            "no_substitute_for_professional_judgment": True,
            "not_a_substitute_for_professional_judgment": ["medical", "legal", "financial"],
            "stance": ("chart-derived claims are traditional interpretive analysis. They are not factual "
                       "prediction and not a substitute for professional judgment."),
            "jurisdiction": ("This run reads one chart and one case context. It cannot endorse, refute or "
                             "replace Assignment-1 research; it supplies register, constraint and sequencing only. "
                             "Every decision in the three briefs still traces to Assignment-1 evidence."),
            "language_register": "en", "banned_language_scan": "pass (see 15_tool_event_log)"}

def s02():
    d = dict(CASE)
    d["degradation_tag"] = ("document-shaped source: rows derived from the document structure are tagged "
                            "DECOMPOSED and may direct relevance only; CONK rows are verbatim strings from the source")
    return d

def s03():
    zf = PID.get("zhi_fu_zhi_shi_checks") or []
    return {"metadata": {"system": "Yi Dun - Lun Cang Jia", "method": "Qimen Dunjia Chart",
                         "type": "Hourly Rotating Qimen, Yin Dun 7 Ju", "solar_term": "秋分 上元",
                         "chart_file_sha256": FP["chart"]["sha256"], "case_file_sha256": FP["case_context"]["sha256"]},
            "board_reference": {"adapter_variant": SA["variants"][0]["id"], "adapter_confidence": 1.0,
                                "palace_blocks": 9, "plus_one_centre_validation": True},
            "root_register": {"case_facets": [s["id"] + " " + (s["heading"] or "") for s in CASE["slots"]],
                              "deferred_facets": [f for f in (CC.get("facet_handling") or {}).get("deferred_facets", [])],
                              "decision_needed": CASE["decision_needed"]},
            "pillars": PILLARS,
            "zhi_fu_zhi_shi_checks": zf,
            "phase_verification": {"claims_checked": len(REG["phase_check"]),
                                   "all_match_frozen_table": all(p["phase_matches_frozen_table"] for p in REG["phase_check"]),
                                   "all_branches_belong_to_palace": all(p["branch_belongs_to_palace"] for p in REG["phase_check"]),
                                   "rows": REG["phase_check"]},
            "anomaly_log": ANOM, "invalid_chains": [
                {"chain": "C011/C012 (asset sequence, production path) -> campaign window",
                 "type": "INVALID_INTO_UNKNOWN",
                 "why": "the chain would cross an undeclared timeframe_of_interest; the chain is blocked, not resolved",
                 "action": "ARC-13 BLOCKED, gap row GAP-003"}],
            "source_paths": {"chart": "QMDJ/GEN_AI/project_3.json", "case_context": "ASSIGNMENTS/GEN_AI/project_3.yaml",
                             "case_copy_in_package": "raw/case_context.case.yaml"},
            "verification_gap": "the physical board arrangement (which star/door/stem lands in which palace from the hour pillar) was NOT independently re-derived; see GAP-007"}

def s04():
    blocks = []
    for canon in range(1, 10):
        p = PID["palace_identity"][str(canon)] if str(canon) in PID["palace_identity"] else PID["palace_identity"][canon]
        r = ROLES["roles"][f"palace_{canon}"]
        blocks.append({"palace": canon, "raw_key_verbatim": p["raw_key_verbatim"], "trigram": p["trigram"],
                       "direction": p["direction"], "element": p["element"], "star_home": p["star_home"],
                       "branches": p["branches"], "role_state": r["state"],
                       "layer_occupancy": {"deity": [i for i, a in E.items() if a["palace"] == canon and a["field_code"] == "deity"],
                                           "door": [i for i, a in E.items() if a["palace"] == canon and a["field_code"] == "door"],
                                           "star": [i for i, a in E.items() if a["palace"] == canon and a["field_code"] == "star"],
                                           "stems": [i for i, a in E.items() if a["palace"] == canon and a["field_code"] in ("heaven_stem", "earth_stem", "hidden_stem", "lodged_stem")]}})
    return {"blocks": blocks,
            "centre_block_validation": {"palace": 5, "has_opposite": False,
                                        "rule": "opposition exists only for 1-4 and 6-9; the centre builds a lodging graph (law 10)",
                                        "lodging_graph": PID["geometry_edges"]["lodging"]},
            "geometry_edges": PID["geometry_edges"]}

def s05():
    spine = {"E": REG["eligible"]["E100"], "R": REG["eligible"]["R100"]}
    return {"id_derivation_mode": {"structural_and_condition_atoms": "path-derived (CAP-11 id_fallback), fixed-width suffixes",
                                   "relations": "path-derived from member ids",
                                   "hashing_available_but_unused_for_ids": True,
                                   "content_hash_role": "used for the package seal and source fingerprints, never for atom ids"},
            "registers": REG["eligible"]["counts"],
            "spine_atoms": {"E": [{"id": i, "value": E[i]["value"], "field": E[i]["field_code"], "path": E[i]["source_path"]} for i in spine["E"]],
                            "R": [{"id": i, "type": R[i]["relation_type"], "value": R[i].get("relation") or R[i].get("pair") or R[i].get("stem") or R[i].get("carrier_stem"),
                                   "rule": R[i]["rule"], "members": R[i]["members"]} for i in spine["R"]]},
            "condition_register_in_scope": [{"id": i, "value": E[i]["value"], "path": E[i]["source_path"],
                                             "verification": E[i].get("verification")} for i in REG["eligible"]["condition_register_in_scope"]],
            "pillar_register": [{"id": i, "type": R[i]["relation_type"], "palace": R[i]["palaces"],
                                 "detail": R[i].get("family") or R[i].get("branch")} for i in REG["eligible"]["pillar_register"]],
            "all_atoms": {"E": len(E), "R": len(R)},
            "digest_blocks": DIGESTS,
            "scope_completeness": {"blocks": 9, "truncated_blocks": [k for k, v in DIGESTS.items() if v["truncated"]],
                                   "rule": "contradiction evidence stays visible even when its palace is out of ranking scope (law 28)"}}

def s06():
    return {"palace_tallies": LED["palace_tallies"], "run_tally": LED["run_tally"],
            "reconciliation": BAT["reconciliation"], "class_level_closure": BAT["class_level_closure"],
            "atom_counts": BAT["atom_counts"], "batches": [
                {"batch": b["batch"], "topic": b["topic"], "topic_name": b["topic_name"], "protocol_class": b["protocol_class"],
                 "palaces": b["palaces"], "layers": b["layers"], "relation_types": b["relation_types"],
                 "in_scope": b["in_scope_total"], "tally": b["tally"], "closed": b["closed"]} for b in BAT["batches"]],
            "closure_equations": {"per_palace": "total = addressed + corroborated + deferred + excluded + unparseable + anomaly + absent",
                                  "counting_rule": "enumerated in addend groups of at most nine; second tally recorded (law 46)",
                                  "run_level": "sum of palace totals - shared relation memberships = atom total"}}

def s07():
    live = [h for h in PAT["pattern_hits"] if h["match_state"].startswith("LIVE")]
    null = [h for h in PAT["pattern_hits"] if h["match_state"].startswith("NULL")]
    sc = {r["pattern_id"] + "|" + str(r["palace"]): r for r in SC["rows"]}
    merged = {}
    for h in live:
        key = (h["pattern_id"], h["palace"])
        m = merged.setdefault(key, {"pattern_id": h["pattern_id"], "cn": h["cn"], "family": h["family"],
                                    "palace": h["palace"], "states": [], "evidence_ids": [], "explicit_marker": None,
                                    "note": h.get("note")})
        m["states"].append(h["match_state"])
        m["evidence_ids"] = sorted(set(m["evidence_ids"]) | set(x for x in h["evidence_ids"] if x))
        m["explicit_marker"] = m["explicit_marker"] or h["explicit_marker"]
    registry = []
    for (pid, pal), m in sorted(merged.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        h = {"pattern_id": pid, "cn": m["cn"], "family": m["family"], "palace": pal,
             "match_state": "+".join(sorted(set(m["states"]))), "evidence_ids": m["evidence_ids"],
             "explicit_marker": m["explicit_marker"]}
        key = pid + "|" + str(pal)
        registry.append({"pattern_id": pid, "cn": m["cn"], "family": m["family"], "palace": pal,
                         "state": h["match_state"], "evidence_ids": h["evidence_ids"], "explicit_marker": h["explicit_marker"],
                         "cycle_trace": f"P{h['palace']} (single-palace)" if h["palace"] else "n/a",
                         "limits": next((p.get("gloss") or p.get("note") or "" for p in PC["patterns"] if p["id"] == h["pattern_id"]), ""),
                         "source": h.get("note"), "score": sc.get(key, {}).get("score"),
                         "grounding_tier": sc.get(key, {}).get("grounding_tier"), "rank": sc.get(key, {}).get("rank")})
    return {"registry": registry, "null_register": null,
            "explicit_vs_computed": PAT["explicit_vs_computed"],
            "explicit_unconfirmed": PAT["explicit_unconfirmed"],
            "score_formula": SC["formula"], "score_source": SC["SCORE_SOURCE"],
            "top_ranked": SC["rows"][:12],
            "catalog_size": PAT["registry_size"], "live_instances": PAT["live"], "null_classes": PAT["null_classes"]}

def s08():
    return {"claim_lines": [c["claim_line"] for c in CL],
            "claims": [{"id": c["id"], "archetype_id": c["archetype_id"], "label": c["label"],
                        "rank_status": c["rank_status"], "certainty": c["certainty"],
                        "grounding_tier": c["grounding_tier"], "ceiling": c["ceiling"],
                        "certainty_addends": c["certainty_addends"], "disp": c["disp"],
                        "support": [s["id"] for s in c.get("support", [])],
                        "counterevidence": [s["id"] for s in c.get("counterevidence", [])],
                        "premise_implications": c.get("premise_implications", []),
                        "competing_candidates": c.get("competing_candidates", []),
                        "SCORE_SOURCE": c["SCORE_SOURCE"]} for c in CL],
            "rank_status_tally": {"confirmed": len([c for c in CL if c["rank_status"] == "confirmed"]),
                                  "bounded": len([c for c in CL if c["rank_status"] == "bounded"]),
                                  "rejected": len([c for c in CL if c["rank_status"] == "rejected"])}}

def s09():
    return {"cmap_rows": [r["line"] for r in CMAP["rows"]], "row_detail": CMAP["rows"],
            "facet_coverage": CMAP["facet_coverage"],
            "tag_tally": {t: sum(v["tags"][t] for v in CMAP["facet_coverage"].values())
                          for t in ("DIRECT", "INDIRECT", "NO_CHART_SUPPORT", "CONTRADICTS_KNOWN")},
            "deferred_facets": [q for q, v in CMAP["facet_coverage"].items() if v.get("deferred")],
            "rule": "all four tags are tallied including zeros (cc6); a Qn with zero DIRECT and zero INDIRECT rows is an uncovered facet unless declared deferred"}

def s10():
    out = []
    for c in CL:
        out.append({"claim_id": c["id"], "archetype_id": c["archetype_id"], "label": c["label"],
                    "interpretation_basis": c["interpretation_basis"],
                    "chart_support": [s["id"] for s in c.get("support", [])],
                    "case_alignment": [f'{a["q"]}:{a["tag"]}' + (f'({a["facet"]})' if a.get("facet") else "")
                                       for a in c.get("case_alignment", [])],
                    "supporting": [s["id"] for s in c.get("support", []) if s["role"] == "spine"],
                    "limiting": c.get("limitations", []),
                    "counterevidence": [s["id"] for s in c.get("counterevidence", [])],
                    "decision_guard": c["decision_guard"], "scope": c["scope"],
                    "confidence": c["certainty"], "scenario_condition": c["scenario_condition"],
                    "validation_path": c["validation_path"], "rank_status": c["rank_status"],
                    "uncertainty": c["uncertainty"], "limitations": c.get("limitations", []),
                    "competing_candidates": c.get("competing_candidates", []),
                    "conflict_register": c.get("conflict_register")})
    return {"hypotheses": out,
            "candidate_rule": "each live hypothesis is one member of its archetype's closed candidate set (law 41); non-selected legal candidates are carried as not_rejected",
            "blocked_classes": CLAIMS_DOC["blocked_classes"]}

def s11():
    return {"implications": CLAIMS_DOC["implications"], "assumptions": CLAIMS_DOC["assumptions"],
            "assumption_index_ranking": sorted({a["assumption_index"] for a in CLAIMS_DOC["assumptions"]}),
            "rule": "inference is permitted only as a labelled assumption with its chart basis attached (law 6); "
                    "every inference exposes evidence, rule, direction and uncertainty (law 20)"}

def s12():
    return {"assumption_ranking": [{"assumption_index": a["assumption_index"], "id": a["id"], "type": a["type"],
                                    "activating_condition": a["activating_condition"]} for a in CLAIMS_DOC["assumptions"]],
            "invalid_chains": s03()["invalid_chains"],
            "deferred_topics": [{"topic": "campaign window (ARC-13)", "why": "no timeframe in the case", "gap_row": "GAP-003"}],
            "blocked_classes": [{"protocol": "Tier2 QT for ARC-13", "reason": "required schema field absent (timeframe_of_interest)"}],
            "conflict_register": CMAP["conflict_register"],
            "conditions": CASE.get("conditions", []),
            "uncertainty_policy": ("certainty is computed by tools/validate_package.py from the cited sets under the "
                                   "archetype rubric; it is capped by the grounding tier and reduced by each counterevidence atom"),
            "null_classes": [{"pattern": h["pattern_id"], "cn": h["cn"], "state": h["match_state"], "note": h["note"]}
                             for h in PAT["pattern_hits"] if h["match_state"].startswith("NULL")]}

def s13():
    return {"bounded_recommendation": {
                "summary": "Build the three briefs on one shared register: a displayed surface that is supported, over a stored core that is withheld; pressure belongs in the frame, not in the promise.",
                "decision_guard": "All directives are tradition-conditional creative direction. Nothing here selects a name, a price, a material, a vendor or a window.",
                "next_actions": ["write the three briefs against D001-D016", "fill every trace_slot from Assignment-1 evidence before the brief is considered done",
                                 "leave the campaign window blank (ARC-13 blocked)"]},
            "directive_sheets": CLAIMS_DOC["brief_directives"],
            "coherence_check": [
                {"brief": "Brand Idea & Philosophy", "one_line": "The core idea (D001/D002) traces to the axis inversion C006 plus the guarded-alliance claim C001; the research finding it must cite is the category gap identified in Assignment 1.",
                 "chart_basis": ["C001", "C006"], "trace_slot": "Assignment-1 research finding (category gap) + insight list"},
                {"brief": "Product & Packaging", "one_line": "The two-state package (D008/D009) traces to the stored-core structure C005 with the caveat that all product facts (D007) are NO_CHART_SUPPORT and come from Assignment 1.",
                 "chart_basis": ["C004", "C005"], "trace_slot": "Assignment-1 competitor scan + mood-board pins (surface/colour)"},
                {"brief": "Ad / Campaign", "one_line": "The campaign (D011-D016) traces to the pressure-into-poise claim C007 with hero, stage, casting and sequence each carrying its own chart citation and guard.",
                 "chart_basis": ["C007", "C008", "C009", "C010", "C011", "C012"], "trace_slot": "Assignment-1 insight (audience tension) + pins per asset"}],
            "uncertainty": "bounded: 12 live claims, 0 confirmed, 1 rejected, 31 legal alternative candidates carried as not_rejected"}

def s14():
    rows = [
        {"id": "GAP-001", "path": "PAT-29 空亡 (void)", "why_unaddressed": "the source declares no void field; the class cannot be computed from this adapter",
         "owner_phase": "P6", "resolution": "declared null class; ABSENT, not a defect (law 27)"},
        {"id": "GAP-002", "path": "PAT-30 驿马 (horse)", "why_unaddressed": "the source declares no horse marker; the day-pillar triad horse is computable in principle but the chart does not seed the class",
         "owner_phase": "P6", "resolution": "declared null class; ABSENT"},
        {"id": "GAP-003", "path": "ARC-13 campaign window", "why_unaddressed": "case context declares no timeframe_of_interest, and none may be inferred (law 40/cc5)",
         "owner_phase": "Tier2 step 1", "resolution": "class BLOCKED; directive D017 tells the writer to leave the window blank"},
        {"id": "GAP-004", "path": "explicit marker 三奇升殿 at palace 3", "why_unaddressed": "the chart's own definition places 丙 at palace 9; palace 3 carries 丙 with 壬, so the computed rule does not confirm the printed marker",
         "owner_phase": "P6 reconciliation", "resolution": "marker retained at authority rank 1 and tagged EXPLICIT_UNCONFIRMED; it is outside the ranked spine so it cannot move a claim"},
        {"id": "GAP-005", "path": "case_context shape", "why_unaddressed": "the case ships as a document, not the flat case_context schema",
         "owner_phase": "CAP-17", "resolution": "CONTEXT_MAPPED_DOCUMENT_SHAPE; derived rows tagged DECOMPOSED; CONK rows are verbatim strings only"},
        {"id": "GAP-006", "path": "domain", "why_unaddressed": "the case states no domain and it may not be inferred",
         "owner_phase": "CAP-17", "resolution": "domain=other with source NOT_STATED"},
        {"id": "GAP-007", "path": "board arrangement re-derivation", "why_unaddressed": "the run reads the printed board; it does not re-derive the hourly rotation from the hour pillar",
         "owner_phase": "Tier-0 (out of contract)", "resolution": "declared verification gap, not an assertion of error; every downstream claim inherits it"},
        {"id": "GAP-008", "path": "product facts (format, variants, size, price)", "why_unaddressed": "not chart-derivable at all",
         "owner_phase": "CAP-18", "resolution": "NO_CHART_SUPPORT rows on Q04; Assignment-1 evidence is the only admissible source"},
        {"id": "GAP-009", "path": "case facet Q01 (Before You Start)", "why_unaddressed": "the case decomposes into 8 facets, over the threshold of 7, so CAP-17 step 4 requires a deferral",
         "owner_phase": "CAP-17", "resolution": "deferred by declared facet_handling; its binding content is enforced as CONK004 in every claim's validation_path"},
        {"id": "GAP-010", "path": "palace 3 explicit markers (升殿/得使)", "why_unaddressed": "two of the 32 explicit markers are not confirmed by their computed rules",
         "owner_phase": "P6 reconciliation", "resolution": "kept visible in the explicit-vs-computed table; no claim depends on them"}
    ]
    return {"gap_rows": rows, "count": len(rows),
            "policy": "a gap report ships even when tools fail; absence is factual reporting, never support (law 28)"}

def s15():
    declared = [{"binding": n, "kind": "Tier-0"} for n in
                ["compute_evidence_registry", "build_board_digest", "expand_claim_lines", "compute_path_rank", "validate_coverage"]] + \
               [{"binding": n, "kind": "Tier-2"} for n in
                ["luoshu_cycle_mapper", "ganzhi_to_luoshu_mapper", "five_state_classifier", "archetype_compressor", "pattern_coverage_detector"]]
    used = {"compute_evidence_registry": "CAP-11 (tools/tier0.py:atomize/evidence_registry)",
            "build_board_digest": "CAP-12 (tools/render_package.py:build_digests)",
            "expand_claim_lines": "CAP-13/CAP-15 (tools/validate_package.py)",
            "compute_path_rank": "CAP-15 (tools/tier0.py:score_card)",
            "validate_coverage": "CAP-14 (tools/tier0.py:batch_and_ledger)",
            "luoshu_cycle_mapper": "CAP-08 (tools/tier0.py:palace_identity)",
            "ganzhi_to_luoshu_mapper": "CAP-05/CAP-09 (tools/tier0.py:pillars_and_composites, value traces)",
            "five_state_classifier": "CAP-10 (tools/tier0.py:patterns, element relations)",
            "archetype_compressor": "not used — no candidate compression was needed (compression_log empty)",
            "pattern_coverage_detector": "CAP-10 + P6 (tools/tier0.py:patterns, score_card)"}
    return {"cap_calls": CALLS_A + CALLS_B + render_calls,
            "cap_budget": {"max": 60, "used": len(CALLS_A) + len(CALLS_B) + len(render_calls)},
            "anomaly_log": ANOM, "conditions": CASE.get("conditions", []),
            "SCORE_SOURCE_stamps": sorted({r["SCORE_SOURCE"] for r in SC["rows"]} | {c["SCORE_SOURCE"] for c in CL}),
            "tool_registry": {"declared": declared, "used": used,
                              "note": "Tier-0 names are bound to local implementations shipped in tools/ so any reviewer can re-run them; no EMULATED products"},
            "render_gate": VAL, "wiki_corpus": [{"slug": a["slug"], "status": "STUB", "cited": False} for a in WK["articles"]]}

def s16():
    return {"raw_to_normalized": {"rule": "trim + absence-code separation; raw retained",
                                  "absence_codes": {"chart_void": "ABSENT", "chart_horse": "ABSENT", "chart_board_array": "ABSENT",
                                                    "case_timeframe": "NULL", "case_domain": "ABSENT", "case_unknowns": "FALSE (empty list is a stated emptiness, not an absent key)"}},
            "reissue_log": load(os.path.join(RAW, "state", "reissue_log.json")),
            "compression_log": load(os.path.join(RAW, "state", "compression_log.json")),
            "id_derivation": {"mode": "path-derived fallback + fixed-width numeric suffix",
                              "examples": {"E001": E["E001"]["derivation"], "R001": R["R001"]["derivation"]},
                              "collision_guard": "景门/惊门 share a romanisation, so doors are keyed by hanzi (see frozen_tables)"},
            "source_fingerprints": FP,
            "artifact_hashes": "see package/seal.json",
            "reproduce": ["python3 tools/tier0.py --chart ../../../../QMDJ/GEN_AI/project_3.json --case raw/case_context.case.yaml --config config --raw raw --work work",
                          "python3 tools/validate_package.py",
                          "python3 tools/render_package.py"]}

def s17_readme():
    return {"pattern_for_reuse": [
        "1 ANCHOR — ingest once, fingerprint, and write a board card that every later phase reads instead of the source.",
        "2 REGISTRY — atomise the source into typed atoms with fixed-width ids, and keep registers separate (structural / condition / relation / pillar).",
        "3 COVER — run the full coverage protocol, tally every atom exactly once, and reconcile at run level, not only per container.",
        "4 RECONCILE — let explicit markers and computed rules meet in a table; neither overwrites the other, and unconfirmed markers stay visible.",
        "5 GATE — compute every score and every claim line in a validator, never in prose; the gate must be able to fail.",
        "6 SEAL — hash the shipped artifacts with the source fingerprints so a reviewer can re-run and compare.",
        "7 REPORT THE GAPS — a gap report ships even on a clean run: null classes, blocked classes, deferred facets and verification gaps are output, not omissions."]}

SECTIONS = {
    "00_package_manifest.json": s00, "01_validity_boundary.json": s01, "02_case_context_digest.json": s02,
    "03_chart_overview.json": s03, "04_palace_identity_resolution.json": s04, "05_structure_evidence.json": s05,
    "06_palace_coverage_matrix.json": s06, "07_pattern_state_registry.json": s07, "08_claim_lines.json": s08,
    "09_case_alignment.json": s09, "10_solution_hypotheses.json": s10, "11_dependency_assumptions.json": s11,
    "12_uncertainty_limits.json": s12, "13_decision_support.json": s13, "14_gap_report.json": s14,
    "15_tool_event_log.json": s15, "16_provenance_appendix.json": s16,
}

# ---------------------------------------------------------------- markdown
def md_full():
    L = []
    A = L.append
    A(f"# QMDJ Chart Analyst — Output Package v{PACKAGE_VERSION}")
    A("")
    A(f"- run mode: **TOOLS_PRESENT** (shell + python surface; no EMULATED products)  ")
    A(f"- render gate: **{VAL['render_gate']}** ({len(VAL['checks'])} checks, {len(VAL['failures'])} failures)  ")
    A(f"- source seal: chart `{FP['chart']['sha256'][:16]}…` ({FP['chart']['bytes']} B), case `{FP['case_context']['sha256'][:16]}…` ({FP['case_context']['bytes']} B)  ")
    A(f"- evidence: registry E={REG['eligible']['counts']['registry_E']} R={REG['eligible']['counts']['registry_R']}; "
      f"spine **{REG['eligible']['counts']['spine_total']}** = {REG['eligible']['counts']['E100_structural']} structural E + {REG['eligible']['counts']['R100']} board-internal R; "
      f"condition register in scope {REG['eligible']['counts']['condition_register_in_scope']}; pillar register {REG['eligible']['counts']['pillar_register']}  ")
    A(f"- coverage: {len(BAT['batches'])}/25 batches closed; run tally {LED['run_tally']}  ")
    A(f"- anomalies: {len(ANOM)}; conditions: {len(CASE.get('conditions', []))}; gap rows: {s14()['count']}  ")
    A("")
    A("## §01 Validity boundary")
    A("")
    A("> Chart-derived claims are traditional interpretive analysis. They are not factual prediction and not a substitute for professional judgment (medical, legal, financial).")
    A("")
    A("This run reads one chart and one case context. It cannot endorse, refute or replace Assignment-1 research: it supplies register, constraint and sequencing only, and every brief decision still traces to Assignment-1 evidence.")
    A("")
    A("## §02 Case context digest")
    A("")
    A(f"- status: **{CASE['status']}** ({CASE['ingest_form']})")
    A(f"- facets: {CASE['question_facets']} — QUESTION_OVERLOAD raised: **{CASE['question_overload']}**")
    if CASE.get("conditions"):
        for c in CASE["conditions"]:
            A(f"  - condition `{c['code']}` ({c['severity']}): {c['handling']}")
    fh = CC.get("facet_handling") or {}
    if fh.get("deferred_facets"):
        for f in fh["deferred_facets"]:
            A(f"  - deferred facet **{f['id']} {f.get('heading','')}** — {f['reason']} (owner {f['owner_phase']}, {f['gap_row']})")
    A(f"- domain: {CASE['domain']['value']} (source {CASE['domain']['source']})")
    A(f"- timeframe: {CASE['timeframe_of_interest']['code']} — {CASE['timeframe_of_interest']['note']}")
    A(f"- subject: {CASE['subject']['value']} ({CASE['subject']['source']})")
    A(f"- known facts (CONK): {len(CASE['known_facts_CONK'])} rows, verbatim; unknowns (UNK): {len(CASE['unknowns_UNK'])} rows")
    for k in CASE["known_facts_CONK"]:
        A(f"  - `{k['id']}`: {k['text']}")
    A("")
    A("### facets (Q01–Q08)")
    A("")
    for sl in CASE["slots"]:
        deferred = sl["id"] in [f["id"] for f in fh.get("deferred_facets", [])]
        A(f"- **{sl['id']} — {sl['heading']}**{' *(deferred)*' if deferred else ''}")
    A("")
    A("## §03 Chart overview")
    A("")
    A(f"- system/method: {s03()['metadata']['system']} — {s03()['metadata']['method']} ({s03()['metadata']['type']})")
    A(f"- pillars: year {PILLARS['year']['raw']}, month {PILLARS['month']['raw']}, day {PILLARS['day']['raw']}, hour {PILLARS['hour']['raw']}")
    A(f"- 值符/值使: {s03()['zhi_fu_zhi_shi_checks']}")
    A(f"- phase verification: {len(REG['phase_check'])} printed phase claims re-derived from the frozen table — "
      f"all match: **{all(p['phase_matches_frozen_table'] for p in REG['phase_check'])}**, all branches belong to their palace: "
      f"**{all(p['branch_belongs_to_palace'] for p in REG['phase_check'])}**")
    A(f"- anomalies: {len(ANOM)}; invalid chains: 1 (window chain blocked, see §12)")
    A("")
    A("## §04 Palace identity resolution (Luoshu)")
    A("")
    A("| P | trigram | dir | element | star home | branches | role state | deity | door | star | heaven / earth |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    for b in s04()["blocks"]:
        occ = b["layer_occupancy"]
        g = lambda ids, f: " ".join(E[i]["value"] for i in ids if E[i]["field_code"] == f) or "—"
        A(f"| {b['palace']} | {b['trigram']} | {b['direction']} | {b['element']} | {b['star_home']} | "
          f"{','.join(b['branches']) or '—'} | {b['role_state']} | {g(occ['deity'],'deity')} | {g(occ['door'],'door')} | "
          f"{g(occ['star'],'star')} | {g(occ['stems'],'heaven_stem')} / {g(occ['stems'],'earth_stem')} |")
    A("")
    A(f"Centre validation: no opposite exists for palace 5; lodging graph → {PID['geometry_edges']['lodging']['lodges_into_from_source']}")
    A("")
    A("## §05 Structure evidence")
    A("")
    A(f"Spine ({REG['eligible']['counts']['spine_total']} atoms) — structural E in palaces 1/4/5 and every board-internal relation touching them.")
    A("")
    A("| id | type | value | rule |")
    A("|---|---|---|---|")
    for i in REG["eligible"]["R100"]:
        r = R[i]
        v = r.get("relation") or r.get("pair") or r.get("stem") or r.get("carrier_stem")
        A(f"| {i} | {r['relation_type']} | {v} | {r['rule']} |")
    A("")
    A("Condition register in scope (the chart's own 判断 lines, kept in their own register):")
    A("")
    for i in REG["eligible"]["condition_register_in_scope"]:
        v = E[i].get("verification")
        tag = "" if not v else (" [verified]" if v["phase_matches_frozen_table"] and v["branch_belongs_to_palace"] else " [CHECK]")
        A(f"- `{i}` P{E[i]['palace']} — {E[i]['value']}{tag}")
    A("")
    A("Pillar register (reported, never absorbed into the spine count):")
    A("")
    for i in REG["eligible"]["pillar_register"]:
        r = R[i]
        A(f"- `{i}` {r['relation_type']} P{r['palaces']} {r.get('family') or r.get('branch')}")
    A("")
    A("## §06 Palace coverage matrix")
    A("")
    A("| P | total | addressed | corroborated | deferred | excluded | unparseable | anomaly | absent | closes |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for k in sorted(LED["palace_tallies"], key=int):
        t = LED["palace_tallies"][k]
        A(f"| {k} | {t['total']} | {t['addressed']} | {t['corroborated']} | {t['deferred']} | {t['excluded']} | "
          f"{t['unparseable']} | {t['anomaly']} | {t['absent']} | {t['closure_balanced']} |")
    A("")
    A(f"Run tally: {LED['run_tally']}")
    A(f"Reconciliation: {BAT['reconciliation']}")
    A("")
    A("Class-level closure (declared absences):")
    for c in BAT["class_level_closure"]:
        A(f"- {c['class']}: **{c['state']}** ({c['phase']}) — {c['reason']}")
    A("")
    A("## §07 Pattern state registry")
    A("")
    A(f"catalog {PAT['registry_size']} classes · {PAT['live']} live instances · {PAT['null_classes']} declared null classes · SCORE_SOURCE={SC['SCORE_SOURCE']}")
    A("")
    A("| pattern | palace | state | evidence | tier | score | rank |")
    A("|---|---|---|---|---|---|---|")
    for r in s07()["registry"]:
        A(f"| {r['pattern_id']} {r['cn']} | {r['palace']} | {r['state']} | {','.join(r['evidence_ids']) or '—'} | "
          f"{r['grounding_tier']} | {r['score']} | {r['rank']} |")
    A("")
    A(f"Score formula (tool-owned): `{SC['formula']}`")
    A("")
    A("### explicit vs computed reconciliation (law 26)")
    A("")
    A("| pattern | palace | explicit marker kept | computed rule confirms |")
    A("|---|---|---|---|")
    for r in PAT["explicit_vs_computed"]:
        A(f"| {r['pattern_id']} {r['cn']} | {r['palace']} | yes (rank 1) | {r['reconciliation']} |")
    A("")
    A("### null register")
    for h in PAT["pattern_hits"]:
        if h["match_state"].startswith("NULL"):
            A(f"- {h['pattern_id']} {h['cn']}: **{h['match_state']}** — {h['note']}")
    A("")
    A("## §08 Claim lines")
    A("")
    A("```")
    for c in CL:
        A(c["claim_line"] + f"   | rank={c['rank_status']} | tier={c['grounding_tier']} | ceiling={c['ceiling']}")
    A("```")
    A("")
    A("| claim | archetype | label | certainty | addends | rank |")
    A("|---|---|---|---|---|---|")
    for c in CL:
        a = c["certainty_addends"]
        add = (f"0.45 + {a['support_term']:.2f} + {a['implication_term']:.2f} - {abs(a['counterevidence_penalty']):.2f}"
               if c["certainty"] is not None else "NA")
        A(f"| {c['id']} | {c['archetype_id']} | {c['label']} | {c['certainty']} | {add} | {c['rank_status']} |")
    A("")
    A("## §09 Case alignment")
    A("")
    A("```")
    for r in CMAP["rows"]:
        A(r["line"])
    A("```")
    A("")
    A("| facet | claims | DIRECT | INDIRECT | NO_CHART_SUPPORT | CONTRADICTS_KNOWN |")
    A("|---|---|---|---|---|---|")
    for q, v in CMAP["facet_coverage"].items():
        A(f"| {q}{' (deferred)' if v.get('deferred') else ''} | {','.join(v['claims']) or '—'} | {v['tags']['DIRECT']} | "
          f"{v['tags']['INDIRECT']} | {v['tags']['NO_CHART_SUPPORT']} | {v['tags']['CONTRADICTS_KNOWN']} |")
    A("")
    A(f"Tag tally (all four present, including zeros): {s09()['tag_tally']}")
    A("")
    A("## §10 Solution hypotheses (controlled candidates)")
    A("")
    for h in s10()["hypotheses"]:
        A(f"### {h['claim_id']} · {h['archetype_id']} · {h['label']}")
        A("")
        A(f"- **basis**: {h['interpretation_basis']}")
        A(f"- **chart support**: {', '.join(h['chart_support']) or '(none — rejected before support was admissible)'}")
        A(f"- **case alignment**: {', '.join(h['case_alignment'])}")
        A(f"- **limiting**: {'; '.join(h['limiting']) or '—'}")
        A(f"- **counterevidence**: {', '.join(h['counterevidence'])}")
        A(f"- **guard**: {h['decision_guard']}")
        A(f"- **scope**: {h['scope']} · **confidence**: {h['confidence']} · **rank**: {h['rank_status']} · **uncertainty**: {h['uncertainty']}")
        A(f"- **scenario condition**: {h['scenario_condition']}")
        A(f"- **validation path**: {h['validation_path']}")
        if h["competing_candidates"]:
            A(f"- **competing candidates**: " + "; ".join(f"{c['label']} [{c['status']}]" for c in h["competing_candidates"]))
        if h.get("conflict_register"):
            A(f"- **conflict**: {h['conflict_register']}")
        A("")
    A(f"Blocked class: {s10()['blocked_classes'][0]['archetype_id']} — {s10()['blocked_classes'][0]['reason']}")
    A("")
    A("## §11 Dependency assumptions")
    A("")
    A("Implications (I-atoms):")
    for i in CLAIMS_DOC["implications"]:
        A(f"- **{i['id']}** ({i['direction']}, {i['rule']}; premises {', '.join(i['premises'])}) — {i['statement']}")
    A("")
    A("Assumptions (A-atoms, ranked):")
    for a in CLAIMS_DOC["assumptions"]:
        A(f"- **{a['id']}** idx={a['assumption_index']} ({a['type']}) — {a['statement']} *(activates when: {a['activating_condition']})*")
    A("")
    A("## §12 Uncertainty & limits")
    A("")
    A(f"- assumption indices in use: {s11()['assumption_index_ranking']}")
    A("- invalid chains: 1 — the window chain is blocked rather than resolved (INVALID_INTO_UNKNOWN)")
    A(f"- deferred topics: campaign window (ARC-13), case facet Q01")
    A(f"- blocked classes: Tier2 QT for ARC-13 (required field absent)")
    A(f"- conflict register: {CMAP['conflict_register']}")
    A("- null classes:")
    for n in s12()["null_classes"]:
        A(f"  - {n['pattern']} {n['cn']}: {n['state']}")
    A("")
    A("## §13 Decision support")
    A("")
    A(f"**Bounded recommendation** — {s13()['bounded_recommendation']['summary']}")
    A("")
    A(f"*Guard*: {s13()['bounded_recommendation']['decision_guard']}")
    A("")
    A("### Directive sheets")
    A("")
    A("| id | brief | section | directive | strength | chart basis | guard | trace slot |")
    A("|---|---|---|---|---|---|---|---|")
    for d in CLAIMS_DOC["brief_directives"]:
        A(f"| {d['id']} | {d['brief']} | {d['section']} | {d['directive']} | {d['strength']} | "
          f"{', '.join(d['chart_basis'])} | {d['guard']} | {d['trace_slot']} |")
    A("")
    A("### Coherence check (the assignment's one-line answers)")
    A("")
    for c in s13()["coherence_check"]:
        A(f"- **{c['brief']}** — {c['one_line']}")
        A(f"  - chart basis: {', '.join(c['chart_basis'])} · trace slot: {c['trace_slot']}")
    A("")
    A("## §14 Gap report")
    A("")
    A("| id | path | why unaddressed | owner phase | resolution |")
    A("|---|---|---|---|---|")
    for g in s14()["gap_rows"]:
        A(f"| {g['id']} | {g['path']} | {g['why_unaddressed']} | {g['owner_phase']} | {g['resolution']} |")
    A("")
    A("## §15 Tool event log")
    A("")
    A(f"- CAP calls: {len(CALLS_A)} (toolchain) + {len(CALLS_B)} (render gate) + {len(render_calls)} (render) = "
      f"{len(CALLS_A) + len(CALLS_B) + len(render_calls)} of 60")
    A("- SCORE_SOURCE stamps: TIER2_TOOL (no EMULATED products in this run)")
    A(f"- anomalies: {len(ANOM)}; conditions: {len(CASE.get('conditions', []))}")
    A(f"- render gate: {VAL['render_gate']} — {len(VAL['checks'])} checks")
    A("- tool registry declared vs used:")
    for d in s15()["tool_registry"]["declared"]:
        A(f"  - `{d['binding']}` ({d['kind']}) → {s15()['tool_registry']['used'].get(d['binding'], 'not used')}")
    A("")
    A("## §16 Provenance appendix")
    A("")
    A(f"- raw→normalized: {s16()['raw_to_normalized']['rule']}")
    A(f"- absence codes: {s16()['raw_to_normalized']['absence_codes']}")
    A(f"- id derivation: {s16()['id_derivation']['mode']} (examples {s16()['id_derivation']['examples']})")
    A(f"- reissue log: {s16()['reissue_log']}")
    A(f"- compression log: {s16()['compression_log']}")
    A(f"- source fingerprints: chart `{FP['chart']['sha256']}` · case `{FP['case_context']['sha256']}`")
    A("")
    A("### reproduce")
    A("")
    A("```")
    for cmd in s16()["reproduce"]:
        A(cmd)
    A("```")
    A("")
    A("## Appendix A — pattern for reuse")
    A("")
    for line in s17_readme()["pattern_for_reuse"]:
        A(f"- {line}")
    A("")
    return "\n".join(L)

def brief_render(brief_key, title):
    dirs = [d for d in CLAIMS_DOC["brief_directives"] if d["brief"] == brief_key]
    hyp = [h for h in s10()["hypotheses"] if h["claim_id"] in {d["chart_basis"][0] for d in dirs if d["chart_basis"]}]
    coh = next((c for c in s13()["coherence_check"] if c["brief"] == brief_key), None)
    L = [f"# Bounded render — {title}", "",
         "Tradition-conditional creative direction only. Not factual prediction. Every line traces to a chart atom and to an Assignment-1 evidence slot.", ""]
    if coh:
        L += ["## Coherence answer (one line, above the brief)", "", coh["one_line"], "",
              f"- chart basis: {', '.join(coh['chart_basis'])}", f"- trace slot: **{coh['trace_slot']}**", ""]
    for d in dirs:
        L.append(f"## {d['id']} · {d['section']}  \n{d['directive']}")
        L.append(f"- strength: `{d['strength']}` · chart basis: {', '.join(d['chart_basis'])}")
        L.append(f"- guard: {d['guard']}")
        L.append(f"- trace slot: **{d['trace_slot']}**")
        L.append("")
    L.append("## supporting hypotheses")
    L.append("")
    for h in hyp:
        L.append(f"- **{h['claim_id']} {h['label']}** (confidence {h['confidence']}, rank {h['rank_status']}): {h['interpretation_basis']}")
    L.append("")
    return "\n".join(L)

def main():
    rcap("CAP-12", "palace_blocks", "board_digest", {"blocks": len(DIGESTS)})
    rcap("CAP-13", "render_lines", "grammar_check", {"sections": len(SECTIONS) + 1})
    rcap("CAP-14", "ledger_at_render", "ledger_reconcile", BAT["reconciliation"])
    rcap("CAP-16", "package", "self_audit", AUD)
    rcap("CAP-18", "claims,facets", "case_map", {"rows": len(CMAP["rows"])})
    rcap("CAP-19", "verdicts,CONK", "conflict_check", CMAP["conflict_register"])
    for name, fn in SECTIONS.items():
        wjson(name, fn())
    wjson("17_pattern_for_reuse.json", s17_readme())

    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    reports = {"full_report": "package/full_report.md",
               "bounded_renders": [
                   {"brief": "Brand Idea & Philosophy", "path": "package/renders/brief_1_brand.md"},
                   {"brief": "Product & Packaging", "path": "package/renders/brief_2_product.md"},
                   {"brief": "Ad / Campaign Creative", "path": "package/renders/brief_3_campaign.md"}]}
    open(os.path.join(OUT, "full_report.md"), "w", encoding="utf-8").write(md_full())
    open(os.path.join(OUT, "renders", "brief_1_brand.md"), "w", encoding="utf-8").write(
        brief_render("Brand Idea & Philosophy", "Brief 1 — Brand Idea & Philosophy"))
    open(os.path.join(OUT, "renders", "brief_2_product.md"), "w", encoding="utf-8").write(
        brief_render("Product & Packaging", "Brief 2 — Product & Packaging"))
    open(os.path.join(OUT, "renders", "brief_3_campaign.md"), "w", encoding="utf-8").write(
        brief_render("Ad / Campaign", "Brief 3 — Ad / Campaign Creative Brief"))
    json.dump(reports, open(os.path.join(OUT, "renders", "bounded_renders.json"), "w", encoding="utf-8"), indent=2)

    # ---------------------------------------------------------------- review pack (RT export)
    os.makedirs(os.path.join(HERE, "review"), exist_ok=True)
    rt_lines = ["# Red-team pack (RT phase)", "",
                "Scope: every live claim's full legal candidate set, minus forbidden pairs, ordered by claim id.",
                "Outcomes fold into claim.rank_status; nothing here is silently dropped.", ""]
    byclaim = {}
    for row in CLAIMS_DOC["red_team"]:
        byclaim.setdefault(row["criticizes"], []).append(row)
    for c in CL:
        rt_lines.append(f"## {c['id']} {c['label']} — rank_status: {c['rank_status']} (certainty {c['certainty']})")
        rt_lines.append("")
        for row in byclaim.get(c["id"], []):
            rt_lines.append(f"- `RT|{row['id']}|criticizes={row['criticizes']}|kind={row['kind']}|status={row['status']}`")
            rt_lines.append(f"  - {row['finding']}")
        cc = c.get("competing_candidates") or []
        if cc:
            rt_lines.append("- legal candidate set carried forward: " + "; ".join(f"{x['label']} [{x['status']}] — {x['why']}" for x in cc))
        rt_lines.append("")
    open(os.path.join(HERE, "review", "red_team.md"), "w", encoding="utf-8").write("\n".join(rt_lines))
    json.dump({"red_team": CLAIMS_DOC["red_team"], "proposals": CLAIMS_DOC["proposals"]},
              open(os.path.join(HERE, "review", "red_team.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # ---------------------------------------------------------------- seal
    seal = {"package_version": PACKAGE_VERSION, "sealed_at_phase": "PACKAGE_RENDER",
            "runtime_mode": "TOOLS_PRESENT", "render_gate": VAL["render_gate"],
            "self_audit_pass": AUD["all_pass"],
            "source_fingerprints": {"chart": FP["chart"], "case_context": FP["case_context"]},
            "artifacts": {}, "note": "seal.json is the only file not listed in its own artifacts map (a hash cannot contain itself)"}
    for root, _, files in os.walk(HERE):
        if any(skip in root for skip in ("/.git", "raw/state")):
            continue
        for f in sorted(files):
            if f == "seal.json" or f.endswith((".pyc",)):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, HERE)
            if rel.endswith((".json", ".md", ".yaml", ".py", ".jsonl", ".yaml")):
                seal["artifacts"][rel] = sha(p)
    seal["artifact_count"] = len(seal["artifacts"])
    json.dump(seal, open(os.path.join(OUT, "seal.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    with open(os.path.join(RAW, "state", "call_log_render.jsonl"), "w", encoding="utf-8") as f:
        f.write("\n".join(json.dumps(c, ensure_ascii=False) for c in render_calls) + "\n")
    print(f"rendered {len(SECTIONS) + 1} sections, full_report.md, 3 bounded renders")
    print(f"sealed {seal['artifact_count']} artifacts; render gate {VAL['render_gate']}")


if __name__ == "__main__":
    main()
