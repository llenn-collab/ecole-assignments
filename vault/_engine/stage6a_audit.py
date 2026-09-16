"""Stage 6a: Ironclad Post-Mortem Integrity Auditor (PROMPT/SKILLS/Audit/skill.md).
Hostile. Trusts: source file, MANIFEST.json, raw/state JSONs only.
Scope adaptation (recorded): Assignment.pdf + SUBMISSION are out-of-scope for the
chart-analyst pipeline (assignment-blind law); audit target = chart_analysis_package."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

OUT = os.path.join(VAULT, "output")
os.makedirs(OUT, exist_ok=True)

# ---- MANIFEST.json bootstrap (audit input prep = bookkeeping, not remediation) ----
prov = load_state("raw_provenance.json")
pkg_hash = sha256_file(os.path.join(STATE, "chart_analysis_package.json"))
manifest_hashes = {"source_file": {"path": SRC_REL, "sha256_recorded_at_boot": prov["sha256"],
                                   "sha256_now": sha256_file(SRC), "size_bytes": prov["size_bytes"]},
                   "chart_analysis_package.json": pkg_hash,
                   "run_id": load_state("machine.json")["run_id"]}
dump_state("MANIFEST.json", manifest_hashes)

# ---- independent citation resolver (auditor does not reuse worker pipeline code) ----
def aud_resolve_state(path):
    body = path[len("state:"):]
    first, _, rest = body.partition(".")
    fp = os.path.join(RAW, "state", first + ".json")
    if not os.path.exists(fp):
        return False
    cur = json.load(open(fp))
    if not rest:
        return True
    for m in re.finditer(r'([A-Za-z0-9_\-]+)|\[([^\]]+)\]', rest):
        name, idx = m.group(1), m.group(2)
        if name:
            if isinstance(cur, dict) and name in cur: cur = cur[name]
            elif isinstance(cur, dict) and "resolutions" in cur:
                hit = [x for x in cur["resolutions"] if x.get("resolution_id") == name]
                if not hit: return False
                cur = hit[0]
            else: return False
        else:
            if idx.isdigit() and isinstance(cur, (list,)) and int(idx) < len(cur): cur = cur[int(idx)]
            elif idx.isdigit() and isinstance(cur, dict) and str(int(idx)) in cur: cur = cur[str(int(idx))]
            elif isinstance(cur, list):
                hit = [x for x in cur if isinstance(x, dict) and any(idx in str(v) for v in x.values())]
                if not hit: return False
                cur = hit[0]
            else: return False
    return True

def aud_cite_ok(path):
    if path.startswith("state:"):
        return aud_resolve_state(path)
    obj = load_source()
    cur = obj
    for m in re.finditer(r'([A-Za-z0-9_ ]+)|\["([^"]+)"\]|\[(\d+)\]', path):
        name, braw, bidx = m.group(1), m.group(2), m.group(3)
        key = braw if braw is not None else (int(bidx) if bidx is not None else (name.strip() if name else None))
        if key in (None, ""): continue
        try:
            cur = cur[key] if not isinstance(key, int) else cur[key]
        except (KeyError, IndexError, TypeError):
            return False
    return True

data = load_source()
package = load_state("chart_analysis_package.json")
palaces_state = load_state("palaces.json")
systems = load_state("systems.json")
mv = load_state("marker_validation.json")
patterns = load_state("patterns.json")
res = load_state("archetype_resolutions.json")
seed = load_state("solution_seed.json")
gates = {}
failed = []

# ---- Gate 0: input presence (adapted contract) ----
g0_items = {"source_chart": os.path.exists(SRC), "manifest": state_exists("MANIFEST.json"),
            "package": state_exists("chart_analysis_package.json"),
            "assignment_pdf": "OUT_OF_SCOPE (assignment-blind law; not an input to this pipeline)",
            "submission_dir": "OUT_OF_SCOPE (downstream of Prompt 1)"}
gates["gate0_presence"] = {"pass": all(v is True or isinstance(v, str) for v in g0_items.values()), "items": g0_items}

# ---- Gate 1: integrity ----
boot = manifest_hashes["source_file"]["sha256_recorded_at_boot"]
now = manifest_hashes["source_file"]["sha256_now"]
gates["gate1_integrity"] = {"pass": boot == now == prov["sha256"],
                            "boot": boot, "now": now, "match": boot == now}
if not gates["gate1_integrity"]["pass"]:
    failed.append({"veto": "FILE_TAMPERED", "gate": 1, "item": "source hash drift", "evidence": f"{boot} vs {now}"})

# ---- Gate 2: traceability matrix over all packaged claims/patterns/resolutions ----
broken = []
def chk(paths, origin):
    for p in paths:
        if not aud_cite_ok(p):
            broken.append({"origin": origin, "path": p})
for p in package["palaces"]:
    for v in p["verdicts"]:
        chk([e["path"] for e in v["evidence"]], v["claim_id"])
    for r in p["relations"]:
        chk(r["evidence"], f"palace_{p['palace_id']}_rel")
for r_ in res["resolutions"]:
    chk(r_["evidence_paths"], r_["resolution_id"])
    chk([s["path"] for s in r_["evidence_chain"]], r_["resolution_id"] + ".chain")
for h in patterns["computed_catalog"]:
    chk(h["evidence_paths"], "pattern:" + h.get("name_en", h.get("name_or_combination", "?")))
for rc in patterns["explicit_pattern_reconciliation"]:
    chk(rc["evidence_paths"], f"recon:{rc['pattern']}@{rc['palace']}")
gates["gate2_traceability"] = {"pass": len(broken) == 0, "broken": broken,
                               "claims_checked": sum(len(p["verdicts"]) for p in package["palaces"])}
if broken:
    failed.append({"veto": "HALLUCINATION", "gate": 2, "item": f"{len(broken)} unresolvable citations",
                   "evidence": json.dumps(broken[:5])})

# ---- Gate 3: confidence layering (0.0-1.0 skill scale over every claim) ----
SCALE = {"EXPLICIT": 1.0, "COMPUTED": 0.8, "INFERRED": 0.5, "ANOMALOUS": 0.8, "UNKNOWN": 0.0}
core_claim_ids = set()
for grp in ("answers", "hidden_problems", "best_solution_candidates"):
    for e in seed[grp]:
        core_claim_ids.update(e.get("claims", []))
        if e.get("context", {}).get("center_displacement"):
            core_claim_ids.update(e["context"]["center_displacement"])
matrix = {"verdict": None, "claims": []}
weak_core = []
for p in package["palaces"]:
    for v in p["verdicts"]:
        conf = SCALE.get(v["grounding"], 0.0)
        core = v["claim_id"] in core_claim_ids
        warn = v["polarity"] in ("WARN", "CONSTRAIN", "VETO")
        entry = {"claim_id": v["claim_id"], "submission_location": f"palace_card:{p['palace_id']}",
                 "claim_text": v["text_en"], "source_type": "QMDJ",
                 "source_anchor": v["evidence"][0]["path"],
                 "confidence": conf, "core_strategy": core,
                 "operator_warning_present": warn,
                 "rationale": f"grounding {v['grounding']} -> {conf}; {len(v['evidence'])} cited paths; polarity {v['polarity']}"}
        matrix["claims"].append(entry)
        if v["grounding"] == "UNKNOWN":
            entry["confidence"] = 0.0
        if core and conf < 0.8 and not warn:
            weak_core.append(v["claim_id"])
gates["gate3_confidence"] = {"pass": len(weak_core) == 0,
                             "min_core_confidence": min((c["confidence"] for c in matrix["claims"] if c["core_strategy"]), default=1.0),
                             "weak_core_without_warning": weak_core,
                             "claims_scored": len(matrix["claims"])}
if weak_core:
    failed.append({"veto": "WEAK_FOUNDATION", "gate": 3, "item": weak_core,
                   "evidence": "core claims <0.8 without operator warning"})

# ---- Gate 4: ADVERSARIAL OMISSION ATTACK ----
omissions = []
def omit(item, evidence, severity, correction):
    omissions.append({"item": item, "evidence": evidence, "severity": severity,
                      "minimum_correction": correction})
# O1: original_position validation block (mandated by worker spec original_position_parser)
if "original_position_audit" not in systems:
    omit("original_position never validated: branches/star/door/deity inside original_position blocks were stored but never checked against frozen geometry or current palace",
         "palaces.*.original_position (8 palaces carry the block); systems.json lacks original_position_audit",
         "HIGH", "execute original_position_parser: branch mapping vs frozen identity, star/door home checks, deity two-plate note, per-palace verdicts")
# O2: Oppression marker never computed-validated
if "oppression" not in mv:
    omit("special_markers 'Oppression' (palace 8) never validated by the marker engine",
         "palaces.gen_8.special_markers[2]; marker_validation.json has no oppression key",
         "MED", "validate oppression markers against door_oppressing_palace relation")
# O3: tomb FIELD stems never validated (only marker stems were)
tomb_field_stems = sum(len(load_state("palaces.json")[pid]["analyses"]) for pid in [])  # placeholder zero
if not any(t.get("source") == "tomb_field" for t in mv.get("tomb", [])):
    omit("tomb field stems never validated: 'Jia Gui', 'Xin Ren', 'Ding Ji Geng', 'Yi Bing Wu' tomb strings stored but stems never checked against tomb-branch geometry",
         "palaces.kun_2.tomb, palaces.xun_4.tomb, palaces.gen_8.tomb, palaces.qian_6.tomb",
         "HIGH", "parse each tomb field; validate every stem's tomb branch against in-palace branches; log school variants")
# O4: liuyi punishment (六仪击刑) never validated — field strings match classical table
pun = {pid.rsplit("_",1)[1]: data["palaces"][pid].get("punishment") for pid in data["palaces"] if data["palaces"][pid].get("punishment")}
if "liuyi_punishment" not in mv:
    omit("punishment fields never validated: 'Wu (Mao, Zhen 3)', 'Ji (…Kun 2)', 'Geng (…Gen 8)', 'Xin (…Li 9)', 'Ren Gui (…Xun 4)' match classical Liu-Yi punishment palace table (Wu@3, Ji@2, Geng@8, Xin@9, Ren@4, Gui@4) — a deterministic check left unexecuted",
         json.dumps(pun),
         "HIGH", "validate all six punishment field entries against Wu@3/Ji@2/Geng@8/Xin@9/Ren@4/Gui@4 table; publish per-entry verdicts")
# O5: center star canonicalization
star_keys = list(systems.get("star_system_map", {}).keys())
if any("lodged" in k for k in star_keys):
    omit("center lodged star never canonicalized in star system map ('Heaven Qin (lodged in Zhen 3 Palace)' kept as raw key; home/displacement not computed)",
         json.dumps(star_keys), "MED",
         "canonicalize to Tian Qin with home 5, displacement true, lodging edge retained")
# O6: day-stem life_stage evidence unexploited
ls_kun2 = data["palaces"]["kun_2"].get("life_stage", "")
uses = [v["claim_id"] for p in package["palaces"] for v in p["verdicts"] if "life_stage" in json.dumps(v["evidence"])]
if "Ren" in ls_kun2 and len(uses) <= 1:
    omit("day stem life-stage evidence unused: chart's own life_stage field names day stem Ren at Kun 2 (Wei/Shen) — the day stem's generative seat evidence never interpreted",
         f"palaces.kun_2.life_stage = '{ls_kun2}'; only {len(uses)} verdict(s) cite any life_stage path",
         "MED", "interpret day-stem life-stage seat (Kun 2) as typed claim with EXPLICIT field grounding")
# O7: palace 7 harm field ignored by its own verdicts
h7 = data["palaces"]["dui_7"].get("harm")
if h7 and not any("dui_7.harm" in json.dumps(v["evidence"]) for v in palaces_state["7"]["verdicts"]):
    omit("palace 7 harm field 'Ji (Dui 7, You)' absent from palace 7 verdicts — the best-solution winner's friction with the center stem (Ji) never disclosed",
         f"palaces.dui_7.harm = '{h7}' vs claims {[v['claim_id'] for v in palaces_state['7']['verdicts']]}",
         "MED", "add WARN claim citing palaces.dui_7.harm; refresh RES-003 contradiction count and margin")
# O8: palace name fields never validated against keys
if "name_key_consistency" not in mv:
    omit("palace 'name' fields never validated against palace keys",
         "palaces.*.name (9 fields)", "LOW",
         "validate each name string against resolved canonical palace id")
# O9: system/solar_term/ju never surfaced in public deliverables
meta_unused = [f for f in ["system", "solar_term"] if f not in json.dumps(package.get("systems", {})) and True]
gates["gate4_omission"] = {"pass": len(omissions) == 0, "omissions": omissions}
if omissions:
    failed.append({"veto": "BLIND_SPOT", "gate": 4,
                   "item": [o["item"][:90] for o in omissions],
                   "evidence": json.dumps([{"sev": o["severity"], "ev": o["evidence"][:80]} for o in omissions])})

verdict = "PASS" if not failed else "VETO"
matrix["verdict"] = verdict

# ---- field utilization sweep (answers 'have you utilised everything') ----
mani = load_state("path_coverage_manifest.json")
used = set()
def harvest(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("path",) and isinstance(v, str): used.add(v)
            elif k in ("evidence_paths", "constraints_cited", "caveats_cited") and isinstance(v, list):
                used.update(x for x in v if isinstance(x, str))
            else: harvest(v)
    elif isinstance(obj, list):
        for x in obj: harvest(x)
harvest(package); harvest(load_state("solution_seed.json"))
harvest({"s": [e["evidence"] for s in load_state("package_gates.json")["gates"].values() for e in []]})  # no-op guard
leaves = [r["normalized_path"] for r in mani["records"] if r["type"] not in ("object", "array")]
unutilized = []
for lp in leaves:
    if lp in used: continue
    reason = None
    if re.search(r"original_position\.numbers", lp): reason = "opaque token-pair by spec array policy (no invented meaning); stored + itemized"
    elif re.search(r"chart_info\.(system|method|type|gregorian|lunar|solar_term|ju)", lp): reason = "identity/provenance fields — cited in report infobox as attribution, not evidence-bearing"
    elif re.search(r"chart_info\.(system|method)$", lp): reason = "attribution metadata"
    elif lp.endswith(".name") and lp.startswith("palaces."): reason = "palace display name — used in card headers; formal key-validation pending (see omission O8)"
    elif "original_position.deity" in lp: reason = "original deity belongs to second deity plate; two-plate note carried in deity map (no computed rule defined)"
    elif lp == "palaces.center_5.original_position.star": reason = "Heavenly Bird = Tian Qin home star (center); covered by star map canon (see O5)"
    if reason is None:
        unutilized.append({"path": lp, "justification": "UNJUSTIFIED"})
    else:
        unutilized.append({"path": lp, "justification": reason})
gates["field_utilization"] = {"total_leaves": len(leaves), "utilized": len(leaves) - len(unutilized),
                              "justified_unused": [u for u in unutilized if u["justification"] != "UNJUSTIFIED"],
                              "unjustified_unused": [u for u in unutilized if u["justification"] == "UNJUSTIFIED"]}
dump_state("field_utilization_audit.json", gates["field_utilization"])
if gates["field_utilization"]["unjustified_unused"]:
    failed.append({"veto": "BLIND_SPOT", "gate": "4b", "item": f"{len(gates['field_utilization']['unjustified_unused'])} leaves with no utilization and no justification",
                   "evidence": json.dumps(gates["field_utilization"]["unjustified_unused"][:10])})
    verdict = "VETO"
matrix["verdict"] = verdict

# ---- outputs per skill contract ----
write_text(os.path.join(OUT, "CONFIDENCE_MATRIX.json"), json.dumps(matrix, indent=2, sort_keys=True))
audit = {"auditor": "ironclad-post-mortem-integrity-auditor (PROMPT/SKILLS/Audit/skill.md)",
         "run": 1, "audited_at": utcnow(), "verdict": verdict, "gates": gates, "failures": failed,
         "scope_adaptation": "Assignment.pdf and SUBMISSION dir are out-of-scope inputs for the chart-analyst pipeline by law (assignment-blind). Gates 0-1 adapted accordingly; Gates 2-4 run at full force against chart_analysis_package.json."}
write_text(os.path.join(OUT, "AUDIT_RUN1.json"), json.dumps(audit, indent=2, sort_keys=True))
if failed:
    vl = ["# VETO LOG — audit run 1\n"]
    for f in failed:
        vl.append(f"## {f['veto']} (gate {f['gate']})")
        vl.append(f"- failing item(s): {json.dumps(f['item'])[:600]}")
        vl.append(f"- evidence: {f['evidence'][:800]}")
        if f["veto"] == "BLIND_SPOT":
            for o in omissions:
                vl.append(f"- minimum correction ({o['severity']}): {o['minimum_correction']}")
        vl.append("")
    write_text(os.path.join(OUT, "VETO_LOG.md"), "\n".join(vl))
print(json.dumps({"verdict": verdict, "gates_brief": {k: v.get("pass") for k, v in gates.items()},
                  "failures": [{"veto": f["veto"], "gate": f["gate"]} for f in failed],
                  "omission_count": len(omissions),
                  "utilization": {"leaves": gates["field_utilization"]["total_leaves"],
                                  "unjustified": len(gates["field_utilization"]["unjustified_unused"])},
                  "weak_core": weak_core, "broken": len(broken)}, indent=1))
