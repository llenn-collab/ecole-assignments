"""Stage 5a: PACKAGE_RENDER part 1 — assemble chart_analysis_package.json,
validate (machine-checkable gates), red-team audit, record package sha256."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

STATE_FILES = {n[:-5]: n for n in os.listdir(STATE) if n.endswith(".json")}

def resolve_state(path):
    """resolve 'state:<file>.<sub>' against raw/state files with symbolic list indexers."""
    body = path[len("state:"):]
    first, _, rest = body.partition(".")
    fname = first if first in STATE_FILES else first + ""
    if fname not in STATE_FILES:
        return False, f"no state file {first}"
    root = load_state(STATE_FILES[fname])
    if not rest:
        return True, root
    cur = root
    for m in re.finditer(r'([A-Za-z0-9_\-]+)|\[([^\]]+)\]', rest):
        name, idx = m.group(1), m.group(2)
        if name:
            if isinstance(cur, dict) and name in cur:
                cur = cur[name]
            elif isinstance(cur, dict) and "resolutions" in cur and isinstance(cur["resolutions"], list):
                hit = [x for x in cur["resolutions"] if x.get("resolution_id") == name]
                if hit: cur = hit[0]
                else: return False, f"token {name} not found"
            else:
                return False, f"token {name} not found"
        elif idx is not None:
            if idx.isdigit():
                i = int(idx)
                if isinstance(cur, list) and i < len(cur): cur = cur[i]
                elif isinstance(cur, dict) and str(i) in cur: cur = cur[str(i)]
                else: return False, f"index {idx} out of range"
            else:  # symbolic: match list member by any string field
                if isinstance(cur, list):
                    hit = [x for x in cur if isinstance(x, dict) and any(idx in str(v) for v in x.values())]
                    if hit: cur = hit[0]
                    else: return False, f"symbolic indexer [{idx}] no match"
                else:
                    return False, f"symbolic indexer [{idx}] on non-list"
    return True, cur

def cite_ok(path):
    if path.startswith("state:"):
        return resolve_state(path)[0]
    return resolve_path(load_source(), path)[0]

# ---------- assemble package ----------
prov = load_state("raw_provenance.json")
mani = load_state("path_coverage_manifest.json")
absence = load_state("absence_registry.json")
excl = load_state("exclusion_log.json")
anom = load_state("anomaly_registry.json")
ep = load_state("explicit_patterns.json")
palaces_state = load_state("palaces.json")
res = load_state("archetype_resolutions.json")
patterns = load_state("patterns.json")
patterns_pkg = dict(patterns)
patterns_pkg["archetype_resolutions"] = res["resolutions"]
yg = load_state("yongshen.json")
seed = load_state("solution_seed.json")
machine = load_state("machine.json")

package = {
 "package_version": "5.0.0",
 "source_file_name": prov["file"],
 "source_qmdj_sha256": prov["sha256"],
 "schema_variant": load_state("schema_variant.json"),
 "semantic_path_map": load_state("semantic_path_registry.json")["roles"],
 "path_coverage_manifest": mani["records"],
 "absence_registry": absence["records"],
 "exclusion_log": excl["records"],
 "anomaly_registry": anom["records"],
 "explicit_patterns": {"markers": ep["markers"], "auspicious": ep["auspicious"], "inauspicious": ep["inauspicious"],
                       "priority": ep["priority"], "ingested_at": ep["ingested_at"]},
 "interpretation_protocol_v2_version_hash": "sha256:protocol_v2_2_2_0_chart_analyst_v5",
 "archetype_scoring_rubric_version_hash": "sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5",
 "generated_at": utcnow(),
 "run_id": machine["run_id"],
 "palaces": [palaces_state[pid] for pid in sorted(palaces_state, key=int)],
 "systems": load_state("systems.json"),
 "relations": load_state("relations.json"),
 "patterns": patterns_pkg,
 "origin_sets": load_state("origin_sets.json"),
 "yongshen_candidates": yg["candidates"],
 "solution_seed": {k: seed[k] for k in ("answers", "hidden_problems", "best_solution_candidates", "note")},
}
dump_state("chart_analysis_package.json", package)

# ---------- machine-checkable gates ----------
gates = {}
REQ = ["package_version","source_file_name","source_qmdj_sha256","schema_variant","semantic_path_map",
       "path_coverage_manifest","absence_registry","exclusion_log","anomaly_registry","explicit_patterns",
       "interpretation_protocol_v2_version_hash","archetype_scoring_rubric_version_hash","generated_at",
       "palaces","systems","relations","patterns","origin_sets","yongshen_candidates","solution_seed"]
schema_errors = [k for k in REQ if k not in package]
for fld in ("answers", "hidden_problems", "best_solution_candidates", "note"):
    if fld not in package["solution_seed"]: schema_errors.append(f"solution_seed.{fld}")
for p in package["palaces"]:
    for fld in ("palace_id", "raw_palace_key", "roles", "analyses", "relations", "verdicts"):
        if fld not in p: schema_errors.append(f"palace.{p.get('palace_id')}.{fld}")
    for v in p["verdicts"]:
        for fld in ("claim_id","slot","text_en","polarity","confidence","grounding","evidence","phase","batch","status"):
            if fld not in v: schema_errors.append(f"{v.get('claim_id')}.{fld}")
gates["validate_schema"] = {"valid": len(schema_errors) == 0, "errors": schema_errors}

broken = []
def check_paths(paths, origin):
    for p in paths:
        if not cite_ok(p):
            broken.append({"origin": origin, "path": p})
for p in package["palaces"]:
    for v in p["verdicts"]:
        check_paths([e["path"] for e in v["evidence"]], v["claim_id"])
    for r in p["relations"]:
        check_paths(r["evidence"], f"palace_{p['palace_id']}_relation_{r['type']}")
for r_ in res["resolutions"]:
    check_paths(r_["evidence_paths"], r_["resolution_id"])
    check_paths([s["path"] for s in r_["evidence_chain"]], r_["resolution_id"] + ".chain")
for hit in patterns["computed_catalog"]:
    check_paths(hit["evidence_paths"], f"pattern:{hit.get('name_en', hit.get('name_or_combination'))}")
for rc in patterns["explicit_pattern_reconciliation"]:
    check_paths(rc["evidence_paths"], f"recon:{rc['pattern']}@{rc['palace']}")
gates["citation_integrity"] = {"broken_links": len(broken), "broken": broken}

parent_only = [b for b in broken if False]  # leaf check below
leaf_bad = []
manifest_by_norm = {r["normalized_path"]: r for r in mani["records"]}
def leaf_check(paths, origin):
    for p in paths:
        if p.startswith("state:"): continue
        rec = manifest_by_norm.get(p)
        if rec and rec["type"] in ("object", "array"):
            leaf_bad.append({"origin": origin, "path": p, "type": rec["type"]})
for p in package["palaces"]:
    for v in p["verdicts"]:
        leaf_check([e["path"] for e in v["evidence"]], v["claim_id"])
gates["leaf_citation_integrity"] = {"parent_only_citations": len(leaf_bad), "bad": leaf_bad}

bc = load_state("board_consistency.json")
gates["board_consistency"] = {"unresolved_contradictions": bc["unresolved_contradictions"],
                              "split_claims_recorded": len(bc["split_claims"]), "pass": bc["pass"]}

seed_missing_ref = []
for group in ("answers", "hidden_problems", "best_solution_candidates"):
    for entry in package["solution_seed"][group]:
        if "archetype_resolution" not in entry:
            seed_missing_ref.append(entry)
gates["archetype_resolution_presence"] = {"missing": len(seed_missing_ref), "pass": len(seed_missing_ref) == 0}
det = load_state("determinism_check.json")
gates["determinism_check"] = {"origin_sets_diff": det["origin_divergence"], "pass": det["pass"]}
cg = load_state("coverage_gate.json")
gates["coverage_complete"] = {"pass": cg["pass"], "gates": cg["gates"]}
ep_first = os.path.getmtime(os.path.join(STATE, "explicit_patterns.json")) <= os.path.getmtime(os.path.join(STATE, "patterns.json"))
gates["explicit_pattern_priority"] = {"explicit_ingested_before_computed": bool(ep_first), "pass": bool(ep_first)}
all_pass = all(v.get("pass", v.get("valid", v.get("broken_links", 1) == 0 and True)) if isinstance(v, dict) else v for v in [
    gates["validate_schema"], {"valid": gates["validate_schema"]["valid"]}]) and \
    gates["citation_integrity"]["broken_links"] == 0 and \
    gates["leaf_citation_integrity"]["parent_only_citations"] == 0 and \
    gates["board_consistency"]["pass"] and gates["archetype_resolution_presence"]["pass"] and \
    gates["determinism_check"]["pass"] and gates["coverage_complete"]["pass"] and gates["explicit_pattern_priority"]["pass"]

# ---------- red team ----------
rt = {}
# 1 adversarial rederivation
rt["adversarial_rederivation"] = [
  {"attempt": "Make Kun 2 (Open door Prosperous, Palace Generating Door) the best-solution winner instead of Dui 7",
   "result": "REJECTED",
   "why": ["day-void branch Wei in-palace (palaces.kun_2.special_markers[0] + chart_info.void.day validated)",
           "heaven Gui explicitly entombed (palaces.kun_2.special_markers[1], validated at Wei)",
           "star Imprisoned/Discarded (palaces.kun_2.prosperity_decline.star_strength)",
           "Xuanwu deity obscurity (palaces.kun_2.deity)"],
   "verdict_effect": "confirms RES-003 runner-down ranking; no evidence path supports a clean opening through Kun 2 in-window"},
  {"attempt": "Declare Li 9 showcase auspicious because Scenery door is 'Prosperous' and sits its original palace",
   "result": "REJECTED with nuance",
   "why": ["door prosperity token is real (palaces.li_9.prosperity_decline.door_strength) and was kept as a separate typed claim, not averaged",
           "but day-void Wu on the year-stacked palace (palaces.li_9.special_markers[0] + chart_info.ganzhi.year + chart_info.void.day) defeats landing in-window",
           "the explicit 'Palace Oppressing Door' contradicts computed geometry — kept as ANOMALOUS, cannot be used as support either way"],
   "verdict_effect": "palace 9 remains a void-locked payoff channel (VETO with SEQUENCE to Wu day/hour), not an inversion"},
  {"attempt": "Re-seat the answer away from Zhen 3 because the palace is hour-void and harm names the day stem",
   "result": "REJECTED",
   "why": ["void and harm are constraints on timing/method, not alternative seats; both independent selectors (day-stem trace, duty proxy) hit only palace 3",
           "rule: a flawed seat is still the seat — no competing candidate found (recorded in RES-001)"],
   "verdict_effect": "none; constraints already shipped as CONSTRAIN/WARN claims on RES-001"},
]
# 2 citation integrity (reuse)
rt["citation_integrity"] = gates["citation_integrity"]
# 3 candidate contamination
contam = []
def scan(obj, where):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "requirement_fit_score" and v is not None:
                contam.append({"where": where, "value": v})
            if isinstance(v, str) and re.search(r"ASSIGNMENT|Assignment\.pdf|deliverable|requirement fit", v):
                contam.append({"where": where, "string": v[:80]})
            scan(v, where)
    elif isinstance(obj, list):
        for x in obj: scan(x, where)
scan(package, "package")
rt["candidate_contamination"] = {"violations": contam, "pass": len(contam) == 0}
# 4 coverage contamination: every verdict evidence path is inventoried or derived state
not_inventoryed = []
for p in package["palaces"]:
    for v in p["verdicts"]:
        for e in v["evidence"]:
            if e["path"].startswith("state:"): continue
            if e["path"] not in manifest_by_norm:
                not_inventoryed.append({"claim": v["claim_id"], "path": e["path"]})
rt["coverage_contamination"] = {"claims_citing_uninventoryed_paths": not_inventoryed, "pass": len(not_inventoryed) == 0}
# 5 anomaly suppression: all registry anomalies present in package + visible list
rt["anomaly_suppression_check"] = {"registry_count": len(anom["records"]),
                                   "package_count": len(package["anomaly_registry"]),
                                   "all_present": len(anom["records"]) == len(package["anomaly_registry"]),
                                   "ids": [a["id"] for a in package["anomaly_registry"]]}
red_pass = (rt["citation_integrity"]["broken_links"] == 0 and rt["candidate_contamination"]["pass"]
            and rt["coverage_contamination"]["pass"] and rt["anomaly_suppression_check"]["all_present"])
dump_state("red_team.json", {"checks": rt, "pass": red_pass})
dump_state("package_gates.json", {"gates": gates, "all_pass": all_pass})
pkg_hash = sha256_file(os.path.join(STATE, "chart_analysis_package.json"))
machine_update(verification={**load_state("machine.json").get("verification", {}),
                             "package_gates": {k: (v.get("pass", v.get("valid"))) for k, v in gates.items()},
                             "red_team": red_pass, "package_sha256": pkg_hash})
progress(f"package render 1/2 | gates all_pass: {all_pass} | citations broken: {len(broken)} | leaf violations: {len(leaf_bad)} | red team: {'PASS' if red_pass else 'FAIL'} | package sha256: {pkg_hash[:16]}...")
print(json.dumps({"all_gates_pass": all_pass, "broken_citations": broken, "leaf_bad": leaf_bad,
                  "contamination": contam, "not_inventoryed": not_inventoryed, "red_team_pass": red_pass,
                  "package_sha256": pkg_hash}, indent=1))
assert all_pass and red_pass, "gate or red team failure"
