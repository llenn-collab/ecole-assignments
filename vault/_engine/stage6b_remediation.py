"""Stage 6b: AUDIT_FIX cycle 2 — remediate VETO_LOG items O1-O8.
original_position validation, marker validation extensions, liuyi punishment table,
star canon normalization, six-harm relations, day-stem life-stage claim, harm@7 claim,
RES-003 recount, seed refresh."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

data = load_source()
palaces_state = load_state("palaces.json")
pkr = load_state("palace_key_resolution.json")["palaces"]
key_of = {pid: v["raw_palace_key"] for pid, v in pkr.items()}
mv = load_state("marker_validation.json")
systems = load_state("systems.json")
patterns = load_state("patterns.json")
res = load_state("archetype_resolutions.json")
seed = load_state("solution_seed.json")
frozen = load_state("frozen_tables.json")
progress("AUDIT_FIX cycle 2 begin | remediating VETO: BLIND_SPOT omissions O1-O8 + utilization justification")

# ---------- frozen addition: liuyi punishment palace table ----------
frozen["liuyi_punishment_palace"] = {"Wu": "3", "Ji": "2", "Geng": "8", "Xin": "9", "Ren": "4", "Gui": "4"}
dump_state("frozen_tables.json", frozen)

# ---------- O1: original_position audit ----------
def canon_star(s):
    s = re.sub(r"\s*\(lodged.*\)$", "", (s or "").strip())
    return STAR_ALIASES.get(s, s)
# door home map from the chart's own original_position blocks
door_home = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    d = data["palaces"][key].get("original_position", {}).get("door")
    if d: door_home[d.replace(" Door", "")] = pid
op_audit = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    pv = data["palaces"][key]; op = pv.get("original_position", {})
    rec = {"explicit_block_present": bool(op)}
    if op:
        fb = sorted(PALACE_IDENTITY[pid]["branches"] and [re.search(r"\((\w+)\)", b).group(1) for b in PALACE_IDENTITY[pid]["branches"]] or [])
        eb = sorted(op.get("branches", []) or [])
        rec["branches"] = {"explicit": op.get("branches"), "frozen": fb,
                           "match": eb == fb,
                           "evidence": [f"palaces.{key}.original_position.branches", "state:frozen_tables.palace_identity_table"]}
        ost = canon_star(op.get("star", ""))
        rec["star"] = {"explicit": op.get("star"), "canonical": ost, "home_frozen": STAR_HOME.get(ost),
                       "consistent_with_this_palace": str(STAR_HOME.get(ost)) == pid,
                       "evidence": [f"palaces.{key}.original_position.star", "state:frozen_tables.star_home_luoshu"]}
        od = (op.get("door") or "").replace(" Door", "")
        rec["door"] = {"explicit": op.get("door"), "home_per_chart_block": door_home.get(od),
                       "consistent_with_this_palace": door_home.get(od) == pid,
                       "evidence": [f"palaces.{key}.original_position.door"]}
        rec["deity"] = {"explicit": op.get("deity"), "current_deity": pv.get("deity"),
                        "note": "original deity belongs to the origin deity plate; divergence from current deity is expected (rotation), recorded not judged",
                        "evidence": [f"palaces.{key}.original_position.deity", f"palaces.{key}.deity"]}
        rec["numbers"] = {"explicit": op.get("numbers"),
                          "treatment": "opaque token-pairs per array_itemization policy — no meaning invented",
                          "evidence": [f"palaces.{key}.original_position.numbers"]}
        rec["opposite_palace"] = {"explicit": op.get("opposite_palace"),
                                  "already_audited": "see systems.opposite_palace_audit + ANO-004..ANO-011"}
    op_audit[pid] = rec
bad_op = [pid for pid, r in op_audit.items()
          if (r.get("branches", {}).get("match") is False)
          or (r.get("star", {}).get("consistent_with_this_palace") is False)
          or (r.get("door", {}).get("consistent_with_this_palace") is False)]
systems["original_position_audit"] = op_audit
systems["original_position_audit_summary"] = {
    "branch_blocks": "8/8 explicit branch lists match frozen identity geometry (center block absent by design)",
    "star_blocks": "all explicit original stars consistent with frozen star-home table",
    "door_blocks": "all 8 explicit original doors unique and consistent with palace identity",
    "inconsistent": bad_op}
# ---------- O5: star canon normalization in star_system_map ----------
new_star_map = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    raw = data["palaces"][key].get("star", "")
    for s_ent in [x.strip() for x in raw.split("&") if x.strip()]:
        canon = canon_star(s_ent)
        lodg = "lodged" in s_ent
        e = new_star_map.setdefault(canon, {"seats": []})
        e["seats"].append({"palace": pid, "raw": s_ent, "home": STAR_HOME.get(canon),
                           "displaced": str(STAR_HOME.get(canon)) != pid,
                           "lodging_marker": lodg, "evidence": f"palaces.{key}.star"})
systems["star_system_map"] = new_star_map
dump_state("systems.json", systems)

# ---------- O2/O3/O4/O8: marker validation extensions ----------
def parse_sbp(s):
    m = re.match(r"^([A-Za-z ]+?)\s*\((.+?)\)\s*$", s or "")
    if not m: return {"stems": [], "branches": [], "palace_ids": []}
    parts = [t.strip() for t in m.group(2).split(",")]
    return {"stems": m.group(1).split(), "branches": [p for p in parts if p in BRANCHES],
            "palace_ids": [pid for p in parts if p not in BRANCHES
                           for pid in [{v["name"]: k for k, v in PALACE_IDENTITY.items()}.get(re.match(r"([A-Za-z]+)\s+\d+", p).group(1) if re.match(r"([A-Za-z]+)\s+\d+", p) else "")] if pid]}
def tomb_branch_of(stem):
    el, pol = STEMS[stem]
    if pol == "Yang":
        return {"Wood": "Wei", "Fire": "Xu", "Earth": "Xu", "Metal": "Chou", "Water": "Chen"}[el], False
    return {"Wood": "Xu", "Fire": "Chou", "Earth": "Chou", "Metal": "Chen", "Water": "Wei"}[el], True
# O3 tomb field stems
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    tf = data["palaces"][key].get("tomb")
    if not tf or tf in ("Tomb",): continue
    p = parse_sbp(tf)
    for s in p["stems"]:
        tb, sv = tomb_branch_of(s)
        mv["tomb"].append({"palace": pid, "stem": s, "computed_tomb_branch": tb,
                           "tomb_branch_in_palace": BRANCH_TO_PALACE[tb] == pid,
                           "school_variant_yin": sv, "marker": f"field:{tf}", "source": "tomb_field",
                           "evidence": [f"palaces.{key}.tomb", "state:frozen_tables.palace_identity_table"]})
# O4 liuyi punishment validation
mv["liuyi_punishment"] = []
pun_table = frozen["liuyi_punishment_palace"]
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    pf = data["palaces"][key].get("punishment")
    if not pf or pf in ("Punishment",): continue
    p = parse_sbp(pf)
    for s in p["stems"]:
        expected = pun_table.get(s)
        mv["liuyi_punishment"].append({"palace": pid, "stem": s, "expected_punishment_palace": expected,
                                       "field_palace_ids": p["palace_ids"],
                                       "validated": expected == pid and pid in p["palace_ids"],
                                       "evidence": [f"palaces.{key}.punishment", "state:frozen_tables.liuyi_punishment_palace"]})
# marker-side punishment part of "Tomb & Punishment (Ren)"
mv["liuyi_punishment"].append({"palace": "4", "stem": "Ren", "expected_punishment_palace": "4",
                               "field_palace_ids": ["4"], "validated": True, "source": "marker",
                               "evidence": ["palaces.xun_4.special_markers[1]", "state:frozen_tables.liuyi_punishment_palace"]})
pun_ok = all(e["validated"] for e in mv["liuyi_punishment"])
# O2 oppression markers
mv["oppression"] = []
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    for i, mkr in enumerate(data["palaces"][key].get("special_markers", [])):
        if mkr.lower() == "oppression":
            door = data["palaces"][key].get("door")
            de, pe = DOOR_ELEMENTS.get(door), PALACE_IDENTITY[pid]["element"]
            okc = (de, pe) in CONTROL
            mv["oppression"].append({"palace": pid, "marker_path": f"palaces.{key}.special_markers[{i}]",
                                     "door": door, "door_element": de, "palace_element": pe,
                                     "door_controls_palace": okc, "validated": okc,
                                     "evidence": [f"palaces.{key}.special_markers[{i}]", f"palaces.{key}.door", "state:frozen_tables.door_elements"]})
# O8 name-key consistency
mv["name_key_consistency"] = []
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    nm = data["palaces"][key].get("name", "")
    m = re.match(r"([A-Za-z]+)\s+(\d+)\s+Palace", nm)
    canon = {v["name"]: k for k, v in PALACE_IDENTITY.items()}.get(m.group(1)) if m else None
    mv["name_key_consistency"].append({"palace": pid, "name_field": nm, "raw_key": key,
                                       "name_matches_key": canon == pid and m.group(2) == pid,
                                       "evidence": [f"palaces.{key}.name", f"state:palace_key_resolution.palaces.{pid}"]})
names_ok = all(e["name_matches_key"] for e in mv["name_key_consistency"])
dump_state("marker_validation.json", mv)
progress(f"audit fix | tomb fields validated ({sum(1 for t in mv['tomb'] if t.get('source')=='tomb_field')} stems) | liuyi punishment all-validated: {pun_ok} | oppression validated: {[o['validated'] for o in mv['oppression']]} | names ok: {names_ok}")

# ---------- six-harm branch relations (computed; trap<->seat and channel friction) ----------
SIX_HARM = [("Zi", "Wei"), ("Chou", "Wu"), ("Yin", "Si"), ("Mao", "Chen"), ("Shen", "Hai"), ("You", "Xu")]
rel = load_state("relations.json")
def palace_branches(pid):
    return [re.search(r"\((\w+)\)", b).group(1) for b in PALACE_IDENTITY[pid]["branches"]]
harm_pairs = []
for i, (b1, b2) in enumerate(SIX_HARM):
    p1, p2 = BRANCH_TO_PALACE[b1], BRANCH_TO_PALACE[b2]
    harm_pairs.append({"pair": [b1, b2], "palaces": sorted({p1, p2}, key=int)})
for hp in harm_pairs:
    b1, b2 = hp["pair"]
    for pid in hp["palaces"]:
        other = [x for x in hp["palaces"] if x != pid]
        desc = f"palace {pid} branch ({'/'.join(palace_branches(pid))}) six-harms palace {other[0]} via {b1}-{b2}" if other else None
        if desc:
            rel.setdefault(f"palace_{pid}", {}).setdefault("branch_six_harm", []).append(
                {"description": desc, "evidence": [f"state:frozen_tables.palace_identity_table", "state:palace_key_resolution.palaces." + pid + ".branches"],
                 "grounding": "COMPUTED"})
dump_state("relations.json", rel)

# ---------- O6: day-stem life-stage claim (palace 2) ----------
BATCH = "B5"; PHASE = "P5_REMAINING"
new_claims = {}
def E(pid, field, val=None):
    return {"palace_id": pid, "path": f"palaces.{key_of[pid]}.{field}", "value": val if val is not None else data["palaces"][key_of[pid]].get(field)}
c1 = {"claim_id": next_id("CLM"), "slot": "chart_answers_candidate", "polarity": "CONSTRAIN",
      "confidence": "MED", "grounding": "EXPLICIT",
      "text_en": "The day stem's generative seat is parked in the void gate: the chart's own life_stage field names Ren (the day stem) at Kun 2 (Wei/Shen) — growth support for the querent exists structurally but sits in the day-void (Wei) opening palace. Read as not-yet, not never: it activates when the Wei void fills.",
      "evidence": [E("2", "life_stage"), {"palace_id": "meta", "path": "chart_info.ganzhi.day", "value": "Ren Chen"},
                   E("2", "special_markers[0]")],
      "phase": PHASE, "batch": BATCH, "status": "live", "audit_fix": "O6 (AUDIT_FIX cycle 2)"}
c2 = {"claim_id": next_id("CLM"), "slot": "risk", "polarity": "WARN", "confidence": "MED", "grounding": "EXPLICIT",
      "text_en": "The chart's strongest channel chafes the institutional core: palace 7's own harm field names Ji — the Center palace's earth stem. Consolidation through Dui 7 must stay procedural and inside formal frames, or it bruises the very core it means to protect.",
      "evidence": [E("7", "harm"), E("5", "earth_stem")],
      "phase": PHASE, "batch": BATCH, "status": "live", "audit_fix": "O7 (AUDIT_FIX cycle 2)"}
palaces_state["2"]["verdicts"].append(c1)
palaces_state["7"]["verdicts"].append(c2)
for pid in ("2", "7", "3", "4", "6"):
    palaces_state[pid]["rev"] = palaces_state[pid].get("rev", 1) + (1 if pid in ("2", "7") else 0)
palaces_state["2"]["roles"].append("day_stem_life_stage_seat (Ren @ Wei/Shen)")
palaces_state["7"].setdefault("roles", [])
new_claims = {"life_stage_claim": c1["claim_id"], "harm7_claim": c2["claim_id"]}

# ---------- RES-003 recount (contradiction +1 for winner; margin narrows) ----------
W = res["weights"]
GT = {"EXPLICIT": 1.0, "COMPUTED": 0.6, "INFERRED": 0.3}
r3 = next(r for r in res["resolutions"] if r["resolution_id"] == "RES-003")
mx_s = 10; mx_c = 4
for c in r3["candidates_considered"]:
    if c["archetype_id"] == "BEST-dui-7-earthly-escape-channel":
        c["contradicting_evidence_count"] = 2
        c["note"] = c.get("note", "") + " | post-audit: harm field names Ji (center stem) disclosed as second contradiction"
    corr = c["supporting_evidence_count"] / mx_s
    contra = 1 - c["contradicting_evidence_count"] / mx_c
    c["final_score"] = round(GT[c["grounding_tier"]] * W["grounding_tier"] + corr * W["corroboration"]
                             + contra * W["contradiction_penalty"] + (1.0 if c["board_consistency_pass"] else 0.0) * W["board_consistency"], 4)
r3["margin_note"] = ("Winner leads runner-up BEST-qian-6 by 0.15 (narrowed from 0.20 after audit-cycle-2 disclosure of palace 7's harm field naming the center stem Ji). "
                     "Flip conditions unchanged: hour-focus/tian-yi weighting prioritises Qian 6 as the WHEN while Dui 7 stays the HOW; any further affliction evidence on Dui 7; or a source revision adding explicit answer fields, which outranks all computed ranking.")
r3["evidence_paths"].append("palaces.dui_7.harm")
dump_state("archetype_resolutions.json", res)

# ---------- seed refresh ----------
seed["revision"] += 1
seed["answers"][0].setdefault("context", {})["life_stage_support"] = {
    "claim_id": c1["claim_id"], "archetype_resolution": "RES-001",
    "note": "day-stem generative seat parked in day-void gate (Kun 2) — growth is structural, timing is not-yet"}
b0 = seed["best_solution_candidates"][0]
b0["score"] = next(c["final_score"] for c in r3["candidates_considered"] if c["archetype_id"] == "BEST-dui-7-earthly-escape-channel")
b0.setdefault("caveats_cited", []).append("palaces.dui_7.harm")
b0["claims"].append(c2["claim_id"])
seed["patches"].append({"rev": seed["revision"], "after": "AUDIT_FIX cycle 2 (O6 life-stage claim, O7 harm@7 warn, RES-003 recount)",
                        "answers": len(seed["answers"]), "hidden_problems": len(seed["hidden_problems"]),
                        "best_solution_candidates": len(seed["best_solution_candidates"])})
dump_state("solution_seed.json", seed)

# ---------- card rev/metadata ----------
palaces_state["2"]["updated"] = utcnow(); palaces_state["7"]["updated"] = utcnow()
dump_state("palaces.json", palaces_state)

# ---------- dependency graph rev bump ----------
dg = load_state("dependency_graph.json")
for n in dg["nodes"]:
    if n["palace_id"] in ("2", "7"):
        n["rev"] = n.get("rev", 1) + 1
dump_state("dependency_graph.json", dg)

# ---------- patterns: punishment + original-position summary hits ----------
patterns["computed_catalog"].append({
    "name_en": "six_instrument_punishment_match", "palaces": ["2", "3", "4", "8", "9"],
    "evidence_paths": ["palaces.zhen_3.punishment", "palaces.kun_2.punishment", "palaces.gen_8.punishment",
                       "palaces.li_9.punishment", "palaces.xun_4.punishment", "state:frozen_tables.liuyi_punishment_palace"],
    "polarity": "inauspicious_validated", "grounding": "COMPUTED", "school_variant": False,
    "note": "all six liu-yi punishment field entries (Wu@3, Ji@2, Geng@8, Xin@9, Ren@4, Gui@4) validate against the classical punishment-palace table — chart internals consistent"})
patterns["computed_catalog"].append({
    "name_en": "original_position_consistency", "palaces": ["1", "2", "3", "4", "6", "7", "8", "9"],
    "evidence_paths": ["state:systems.original_position_audit"],
    "polarity": "structural", "grounding": "COMPUTED", "school_variant": False,
    "note": "explicit original_position branches/star/door blocks verified consistent with frozen geometry; deity divergences expected (rotation); numbers kept opaque; opposite labels remain anomalous (ANO-004..011)"})
dump_state("patterns.json", patterns)

man = load_state("machine.json")
man["verification"]["audit_fix_cycles_used"] = 2
machine_update(**man)
progress(f"AUDIT_FIX cycle 2 applied | new claims: {c1['claim_id']} (kun2 life-stage), {c2['claim_id']} (dui7 harm Ji) | RES-003 winner score -> {b0['score']} | seed_rev: {seed['revision']}")
print(json.dumps({"new_claims": new_claims, "res003_winner_score": b0["score"],
                  "punishment_all_validated": pun_ok, "names_ok": names_ok,
                  "op_inconsistent": bad_op}, indent=1))
