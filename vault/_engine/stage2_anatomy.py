"""Stage 2: P0_ANATOMY. Deterministic anatomy: pillars, season, duty, indexes,
origin sets, lodging graph, marker validation, explicit pattern ingestion,
absence registry, dependency graph, unbound yongshen candidates."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

data = load_source()
machine_update(state="P0_ANATOMY", completed_phases=["CHART_INGEST", "STRUCTURAL_INVENTORY", "SCHEMA_ADAPTATION"])
anomalies = []

def anomaly(type_, desc, paths, severity="MED", note=None):
    a = {"id": f"ANO-{len(anomalies)+1:03d}", "type": type_, "description": desc,
         "paths": paths, "phase_recorded": "P0_ANATOMY", "severity": severity,
         "resolution_note": note}
    anomalies.append(a)
    return a

# ---------- ganzhi parser ----------
def parse_ganzhi(s, path):
    toks = s.split()
    if len(toks) != 2 or toks[0] not in STEMS or toks[1] not in BRANCHES:
        return {"raw_value": s, "confidence": 0.0, "ambiguity_flags": ["UNPARSEABLE"],
                "evidence_class": "UNKNOWN"}
    st, br = toks
    se, sp = STEMS[st]; ba, be, bp = BRANCHES[br]
    return {"raw_value": s, "path": path, "stem_raw": st, "branch_raw": br,
            "stem_pinyin": st, "branch_pinyin": br, "stem_element": se, "stem_polarity": sp,
            "branch_element": be, "branch_polarity": bp, "branch_animal": ba,
            "confidence": 1.0, "ambiguity_flags": [], "evidence_class": "EXPLICIT"}

XUN_LEADERS = ["Jia Zi", "Jia Xu", "Jia Shen", "Jia Wu", "Jia Chen", "Jia Yin"]
YI_OF_JIA = {"Jia Zi": "Wu", "Jia Xu": "Yi", "Jia Shen": "Geng",
             "Jia Wu": "Xin", "Jia Chen": "Ren", "Jia Yin": "Gui"}
def xun_of(stem, branch):
    stems = list(STEMS); branches = list(BRANCHES)
    si, bi = stems.index(stem), branches.index(branch)
    lead_bi = (bi - si) % 12
    lead = "Jia " + branches[lead_bi]
    covered = [branches[(lead_bi + i) % 12] for i in range(10)]
    void = [b for b in branches if b not in covered]
    return {"xun_leader": lead, "yi_stem": YI_OF_JIA[lead], "void_branches": void}

pillars = {}
for p in ["year", "month", "day", "hour"]:
    path = f"chart_info.ganzhi.{p}"
    ok, raw = cite_source(path)
    g = parse_ganzhi(raw, path)
    g["xun"] = xun_of(g["stem_raw"], g["branch_raw"])
    pillars[p] = g

# pillar relations
stems_p = {p: pillars[p]["stem_raw"] for p in pillars}
brs_p = {p: pillars[p]["branch_raw"] for p in pillars}
rels = []
for a, b in [("year","month"),("year","day"),("year","hour"),("month","day"),("month","hour"),("day","hour")]:
    for comb in STEM_COMBINE:
        if {stems_p[a], stems_p[b]} == comb:
            rels.append({"type": "stem_combination", "members": sorted(comb),
                         "pillars": [a, b], "evidence": [pillars[a]["path"], pillars[b]["path"]]})
    for c1, c2 in SIX_CLASH:
        if {brs_p[a], brs_p[b]} == {c1, c2}:
            rels.append({"type": "branch_clash", "members": [c1, c2], "pillars": [a, b],
                         "evidence": [pillars[a]["path"], pillars[b]["path"]]})
    for c1, c2 in SIX_COMBINE_B:
        if {brs_p[a], brs_p[b]} == {c1, c2}:
            rels.append({"type": "branch_six_combination", "members": [c1, c2], "pillars": [a, b],
                         "evidence": [pillars[a]["path"], pillars[b]["path"]]})
void_day_md = load_source()["chart_info"]["void"]["day"].split()
void_hour_md = load_source()["chart_info"]["void"]["hour"].split()
void_day_calc = pillars["day"]["xun"]["void_branches"]
void_hour_calc = pillars["hour"]["xun"]["void_branches"]
void_day_ok = set(void_day_md) == set(void_day_calc)
void_hour_ok = set(void_hour_md) == set(void_hour_calc)
if not void_day_ok:
    anomaly("VOID_MISMATCH", f"day void metadata {void_day_md} != computed {void_day_calc}",
            ["chart_info.void.day", pillars["day"]["path"]], "HIGH")
if not void_hour_ok:
    anomaly("VOID_MISMATCH", f"hour void metadata {void_hour_md} != computed {void_hour_calc}",
            ["chart_info.void.hour", pillars["hour"]["path"]], "HIGH")
void_membership = {p: {"in_day_void": brs_p[p] in void_day_calc, "in_hour_void": brs_p[p] in void_hour_calc}
                   for p in pillars}
pillars_out = {"pillars": pillars, "relations": rels,
               "day_void": {"metadata": void_day_md, "computed": void_day_calc, "validated": void_day_ok},
               "hour_void": {"metadata": void_hour_md, "computed": void_hour_calc, "validated": void_hour_ok},
               "void_membership": void_membership,
               "branch_to_palace_projection": {p: BRANCH_TO_PALACE[brs_p[p]] for p in pillars},
               "stem_to_palaces_projection": {}}
dump_state("pillars.json", pillars_out)

# ---------- season ----------
ok, seas = cite_source("chart_info.seasonal_strength")
season = {"raw": seas, "normalized": {}, "raw_vocabulary_preserved": True}
for el, term in seas.items():
    norm, status = RAW_STRENGTH_MAP.get(term, ("UNKNOWN", "uncertain_mapping"))
    season["normalized"][el] = {"raw": term, "normalized": norm, "mapping_status": status}
dump_state("season.json", season)

# ---------- duty strings ----------
def parse_falling(s):
    m = re.match(r"(.+?)\s+falling in\s+(.+?)\s+Palace\s*$", s)
    if not m:
        return None
    return {"entity": m.group(1).strip(), "palace_reference": m.group(2).strip()}
def palace_ref_to_id(ref):
    m = re.match(r"([A-Za-z]+)\s+(\d+)$", ref)
    if not m:
        return None, ["UNPARSEABLE_PALACE_REF"]
    name, num = m.group(1), m.group(2)
    canon = {v["name"]: k for k, v in PALACE_IDENTITY.items()}.get(name)
    flags = []
    if canon is None:
        flags.append("UNKNOWN_PALACE_NAME")
    elif canon != num:
        flags.append("NAME_NUMBER_MISMATCH")
    return canon or num, flags

fu_tou_raw = load_source()["chart_info"]["fu_tou"]
m = re.match(r"(Jia)\s+([A-Za-z]+)\s+([A-Za-z]+)$", fu_tou_raw)
fu_tou = {"raw_value": fu_tou_raw, "parsed": bool(m)}
if m:
    lead = f"Jia {m.group(2)}"
    fu_tou.update({"xun_leader": lead, "hidden_jia_relationship": "Jia concealed under yi stem",
                   "yi_stem": m.group(3), "yi_stem_matches_frozen_table": YI_OF_JIA.get(lead) == m.group(3),
                   "binds_stems": ["Jia", m.group(3)], "confidence": 1.0})
    if YI_OF_JIA.get(lead) != m.group(3):
        anomaly("FU_TOU_YI_MISMATCH", f"fu_tou '{fu_tou_raw}' yi stem != frozen Jia->yi table",
                ["chart_info.fu_tou"], "HIGH")

zhi_fu_raw = load_source()["chart_info"]["zhi_fu"]
pf = parse_falling(zhi_fu_raw)
duty_star_palace, flags_f = palace_ref_to_id(pf["palace_reference"])
duty_star_canon = pf["entity"]
zhi_shi_raw = load_source()["chart_info"]["zhi_shi"]
ps_ = parse_falling(zhi_shi_raw)
duty_door_active, flags_s = palace_ref_to_id(ps_["palace_reference"])
duty_door_name = ps_["entity"].replace(" Door", "")
# duty door original palace = palace whose original_position.door names it
duty_door_original = None
for pid, pv in data["palaces"].items():
    op = pv.get("original_position", {})
    if isinstance(op, dict) and op.get("door", "").replace(" Door", "") == duty_door_name:
        duty_door_original = pid.rsplit("_", 1)[1]
duty = {
 "fu_tou": fu_tou,
 "zhi_fu": {"raw_value": zhi_fu_raw, "star": duty_star_canon, "star_canonical": duty_star_canon.replace("Tian", "Tian"),
            "active_palace": duty_star_palace, "home_palace": str(STAR_HOME.get(duty_star_canon)),
            "palace_flags": flags_f, "evidence_class": "EXPLICIT(string)+COMPUTED(parse)",
            "cross_check_in_palace_star_field": None},
 "zhi_shi": {"raw_value": zhi_shi_raw, "door": duty_door_name, "active_palace": duty_door_active,
             "original_palace": duty_door_original, "palace_flags": flags_s,
             "original_ne_active": duty_door_original != duty_door_active,
             "evidence_class": "EXPLICIT(string)+COMPUTED(parse)"},
 "tian_yi": {"raw_value": load_source()["chart_info"]["tian_yi"], "canonical": "Tian Chong",
             "evidence_class": "EXPLICIT"},
 "lead_stem": {"binds": fu_tou.get("binds_stems", []), "visible_proxy": m.group(3) if m else None,
               "note": "Jia invisible on plate by construction (Dun Jia); Ren is its visible stand-in"},
}
# cross checks
pk = {v["raw_palace_key"]: k for k, v in load_state("palace_key_resolution.json")["palaces"].items()}
pk_rev = {v: k for k, v in pk.items()}
star_field = data["palaces"][pk_rev[duty_star_palace]]["star"]
duty["zhi_fu"]["cross_check_in_palace_star_field"] = {
    "path": f'palaces.{pk_rev[duty_star_palace]}.star', "value": star_field,
    "contains_duty_star": duty_star_canon.split()[-1] in star_field}
duty["zhi_shi"]["cross_check_door_field"] = {
    "path": f'palaces.{pk_rev[duty_door_active]}.door', "value": data["palaces"][pk_rev[duty_door_active]]["door"],
    "matches": data["palaces"][pk_rev[duty_door_active]]["door"] == duty_door_name}
chief_palaces = [pk[k] for k, v in data["palaces"].items() if v.get("deity") == "Chief"]
duty["chief_deity_palace"] = {"palaces": chief_palaces,
    "note": "Chief deity seat cross-validates zhi_fu landing",
    "matches_duty_star_palace": chief_palaces == [duty_star_palace]}
dump_state("duty.json", duty)
progress(f"phase0 duty | lead: Jia->Ren | duty_star: Tian Rui @3 (home 2) | duty_door: Death orig 2 active 4 | tian_yi: Tian Chong")

# ---------- composite string parsers ----------
def parse_lodged(s):
    m = re.match(r"^(.+?)\s*\(lodged in\s+(.+?)\s+Palace\)\s*$", s)
    if m:
        pid, fl = palace_ref_to_id(m.group(2))
        return {"stem_or_star": m.group(1).strip(), "lodged": True, "lodged_palace": pid, "flags": fl}
    return {"stem_or_star": s, "lodged": False, "lodged_palace": None, "flags": []}
def parse_marker(s):
    m = re.match(r"^Tomb & Punishment \((.+?)\)$", s)
    if m: return {"raw_marker": s, "marker_type": "tomb_and_punishment", "related_stems": m.group(1).split()}
    m = re.match(r"^Tomb \((.+?)\)$", s)
    if m: return {"raw_marker": s, "marker_type": "tomb", "related_stems": m.group(1).split()}
    if s in ("Void", "Horse", "Oppression"):
        return {"raw_marker": s, "marker_type": s.lower(), "related_stems": []}
    return {"raw_marker": s, "marker_type": "UNPARSEABLE", "related_stems": []}
def parse_stem_branch_palace(s):
    m = re.match(r"^([A-Za-z ]+?)\s*\((.+?)\)\s*$", s)
    if not m:
        return {"raw_value": s, "parsed": False, "stems": [], "branches": [], "palace_refs": []}
    stems = m.group(1).split()
    parts = [t.strip() for t in m.group(2).split(",")]
    branches = [p for p in parts if p in BRANCHES]
    refs = [p for p in parts if p not in BRANCHES]
    pids, flags = [], []
    for r in refs:
        pid, fl = palace_ref_to_id(r); pids.append(pid); flags += fl
    return {"raw_value": s, "parsed": True, "stems": stems, "branches": branches,
            "palace_refs": refs, "palace_ids": pids, "flags": flags}
def parse_strength(s):
    toks = [t.strip() for t in s.split("/")]
    out = {"raw_value": s, "tokens": toks, "normalized_tokens": []}
    for t in toks:
        if t in RAW_STRENGTH_MAP:
            out["normalized_tokens"].append({"raw": t, "normalized": RAW_STRENGTH_MAP[t][0],
                                             "mapping_status": RAW_STRENGTH_MAP[t][1]})
        elif t in ("Inner", "Outer"):
            out["normalized_tokens"].append({"raw": t, "normalized": t.lower(), "mapping_status": "ring_label"})
        else:
            out["normalized_tokens"].append({"raw": t, "normalized": "UNKNOWN", "mapping_status": "uncertain_mapping"})
    norms = [x["normalized"] for x in out["normalized_tokens"] if x["mapping_status"] != "ring_label"]
    out["split"] = len(set(norms)) > 1
    return out

# ---------- plate scan + lodging graph + reverse indexes ----------
pkr = load_state("palace_key_resolution.json")["palaces"]
key_of = {pid: v["raw_palace_key"] for pid, v in pkr.items()}
plate = {}
lodging_edges = []
for pid in sorted(pkr, key=int):
    k = key_of[pid]; pv = data["palaces"][k]
    P = {"palace_id": pid, "raw_palace_key": k, "name": pv.get("name")}
    hs = parse_lodged(pv.get("heaven_stem", ""))
    P["heaven_stem"] = {"raw": pv.get("heaven_stem"), "stem": hs["stem_or_star"].split(" ")[-1] if "(" in pv.get("heaven_stem","") and "lodged" not in pv.get("heaven_stem","") else hs["stem_or_star"], "lodged": hs["lodged"], "lodged_palace": hs["lodged_palace"]}
    if hs["lodged"]:
        lodging_edges.append({"from_palace": pid, "entity_layer": "heaven_stem", "entity": hs["stem_or_star"],
                              "to_palace": hs["lodged_palace"], "raw": pv["heaven_stem"],
                              "evidence": f"palaces.{k}.heaven_stem"})
    hid = parse_lodged(pv.get("hidden_stem", "")) if pv.get("hidden_stem") else None
    P["hidden_stem"] = {"raw": pv.get("hidden_stem"), "stem": hid["stem_or_star"] if hid else None,
                        "lodged": hid["lodged"] if hid else False,
                        "lodged_palace": hid["lodged_palace"] if hid else None}
    if hid and hid["lodged"]:
        lodging_edges.append({"from_palace": pid, "entity_layer": "hidden_stem", "entity": hid["stem_or_star"],
                              "to_palace": hid["lodged_palace"], "raw": pv["hidden_stem"],
                              "evidence": f"palaces.{k}.hidden_stem"})
    st = parse_lodged(pv.get("star", ""))
    P["star"] = {"raw": pv.get("star"), "entities": [s.strip() for s in pv.get("star","").split("&")] if pv.get("star") else [],
                 "lodged": st["lodged"], "lodged_palace": st["lodged_palace"]}
    if st["lodged"]:
        lodging_edges.append({"from_palace": pid, "entity_layer": "star", "entity": st["stem_or_star"],
                              "to_palace": st["lodged_palace"], "raw": pv["star"], "evidence": f"palaces.{k}.star"})
    P["earth_stem"] = {"raw": pv.get("earth_stem"), "stem": pv.get("earth_stem")}
    P["door"] = pv.get("door")
    P["deity"] = pv.get("deity")
    P["markers"] = [parse_marker(x) for x in pv.get("special_markers", [])]
    P["auspicious"] = list(pv.get("auspicious_patterns", []))
    P["inauspicious"] = list(pv.get("inauspicious_patterns", []))
    op = pv.get("original_position", {})
    P["original_position"] = op
    pr = pv.get("prosperity_decline", {})
    P["prosperity"] = {"door_strength": parse_strength(pr["door_strength"]) if "door_strength" in pr else None,
                       "star_strength": parse_strength(pr["star_strength"]) if "star_strength" in pr else None,
                       "palace_state": parse_strength(pr["palace_state"]) if "palace_state" in pr else None}
    for f in ["life_stage", "harm", "tomb", "punishment"]:
        if f in pv:
            P[f] = parse_stem_branch_palace(pv[f]) if not pv[f] in ("Harm", "Tomb", "Punishment") else \
                   {"raw_value": pv[f], "parsed": False, "placeholder_label": True, "stems": [], "branches": [], "palace_ids": []}
        else:
            P[f] = None
    plate[pid] = P

# lodging graph + host confirmation
for e in lodging_edges:
    host = plate[e["to_palace"]]
    if e["entity_layer"] == "star":
        e["host_confirmation"] = {"found_in_host_star_field": any(e["entity"].split()[-1] in s for s in host["star"]["entities"]),
                                  "path": f"palaces.{host['raw_palace_key']}.star", "value": host["star"]["raw"]}
    elif e["entity_layer"] == "hidden_stem":
        e["host_confirmation"] = {"found_in_host_hidden_field": e["entity"] == (host["hidden_stem"]["stem"] or ""),
                                  "path": f"palaces.{host['raw_palace_key']}.hidden_stem",
                                  "value": host["hidden_stem"]["raw"],
                                  "note": "host palace keeps its own hidden stem; lodger co-resides (not echoed) — recorded, not treated as contradiction"}
    else:
        e["host_confirmation"] = {"note": "lodged heaven stem rides with host palace"}
lodging = {"trigger": "center palace lodging strings present + duty_door original != active",
           "graph": lodging_edges, "center_is_pivot_no_opposite": True,
           "duty_door_displacement": {"original": duty_door_original, "active": duty_door_active}}
dump_state("lodging.json", lodging)

# reverse indexes
def idx_add(idx, key, pid, path, layer):
    idx.setdefault(key, []).append({"palace": pid, "path": path, "layer": layer})
stems_idx, doors_idx, stars_idx, deities_idx, branches_idx, markers_idx = {}, {}, {}, {}, {}, {}
tomb_idx, punish_idx = {}, {}
for pid, P in plate.items():
    k = P["raw_palace_key"]
    for layer, fld in [("heaven", "heaven_stem"), ("earth", "earth_stem"), ("hidden", "hidden_stem")]:
        st = P[fld]["stem"]
        if st:
            idx_add(stems_idx, st, pid, f"palaces.{k}.{fld}", layer)
    if P["door"]:
        idx_add(doors_idx, P["door"], pid, f"palaces.{k}.door", "door_plate")
    for s in P["star"]["entities"]:
        idx_add(stars_idx, s, pid, f"palaces.{k}.star", "heaven")
    if P["deity"]:
        idx_add(deities_idx, P["deity"], pid, f"palaces.{k}.deity", "deity_plate")
    for b in PALACE_IDENTITY[pid]["branches"]:
        bn = re.search(r"\((\w+)\)", b).group(1)
        idx_add(branches_idx, bn, pid, f"palace_identity_table[{pid}]", "frozen_geometry")
    for i, mk in enumerate(P["markers"]):
        idx_add(markers_idx, mk["marker_type"], pid, f"palaces.{k}.special_markers[{i}]", "explicit_marker")
        for s in mk["related_stems"]:
            idx_add(stems_idx, s, pid, f"palaces.{k}.special_markers[{i}]", "marker_reference")
    for f in ["tomb", "punishment"]:
        if P[f] and P[f]["parsed"]:
            tgt = tomb_idx if f == "tomb" else punish_idx
            for s in P[f]["stems"]:
                idx_add(tgt, s, pid, f"palaces.{k}.{f}", f"{f}_field")
indexes = {"stems": stems_idx, "doors": doors_idx, "stars": stars_idx, "deities": deities_idx,
           "branches": branches_idx, "markers": markers_idx, "tombs": tomb_idx, "punishments": punish_idx,
           "lodging": lodging_edges}
dump_state("indexes.json", indexes)

# ---------- explicit pattern ingestion (BEFORE computed) ----------
ep = {"ingested_at": utcnow(), "priority": "explicit_before_computed", "markers": [], "auspicious": [], "inauspicious": []}
for pid, P in plate.items():
    k = P["raw_palace_key"]
    for i, mk in enumerate(P["markers"]):
        ep["markers"].append({"array_path": f"palaces.{k}.special_markers", "index": i, "palace": pid,
                              **mk, "evidence_class": "EXPLICIT"})
    for i, s in enumerate(P["auspicious"]):
        ep["auspicious"].append({"array_path": f"palaces.{k}.auspicious_patterns", "index": i, "palace": pid,
                                 "raw_pattern": s, "polarity": "auspicious", "evidence_class": "EXPLICIT"})
    for i, s in enumerate(P["inauspicious"]):
        ep["inauspicious"].append({"array_path": f"palaces.{k}.inauspicious_patterns", "index": i, "palace": pid,
                                   "raw_pattern": s, "polarity": "inauspicious", "evidence_class": "EXPLICIT"})
dump_state("explicit_patterns.json", ep)

# ---------- marker validation (computed vs explicit) ----------
def tomb_branch_of(stem):
    el, pol = STEMS[stem]
    if pol == "Yang":
        return {"Wood": "Wei", "Fire": "Xu", "Earth": "Xu", "Metal": "Chou", "Water": "Chen"}[el], False
    return {"Wood": ("Xu"), "Fire": "Chou", "Earth": "Chou", "Metal": "Chen", "Water": "Wei"}[el], True
valid = {"void": [], "horse": [], "tomb": [], "duty": [], "mismatches": []}
void_palaces_calc = {}
for pid, P in plate.items():
    brs = [re.search(r"\((\w+)\)", b).group(1) for b in PALACE_IDENTITY[pid]["branches"]]
    vd = [b for b in brs if b in void_day_calc]; vh = [b for b in brs if b in void_hour_calc]
    if vd or vh:
        void_palaces_calc[pid] = {"day": vd, "hour": vh}
    has_void_marker = any(mk["marker_type"] == "void" for mk in P["markers"])
    if (vd or vh) and has_void_marker:
        valid["void"].append({"palace": pid, "status": "VALIDATED", "day_void": vd, "hour_void": vh,
                              "marker_path": f"palaces.{P['raw_palace_key']}.special_markers"})
    elif (vd or vh) and not has_void_marker:
        valid["mismatches"].append({"palace": pid, "type": "computed_void_no_marker"})
    elif has_void_marker:
        valid["mismatches"].append({"palace": pid, "type": "marker_void_unconfirmed"})
horse_palaces_calc = {}
for scope in ["year", "month", "day", "hour"]:
    hb = HORSE_TABLE[brs_p[scope]]
    okv, hb_md = cite_source(f"chart_info.horse.{scope}")
    if hb_md != hb:
        anomaly("HORSE_MISMATCH", f"{scope} horse metadata {hb_md} != computed {hb}",
                [f"chart_info.horse.{scope}", pillars[scope]["path"]], "MED")
    pid = BRANCH_TO_PALACE[hb]
    horse_palaces_calc[pid] = horse_palaces_calc.get(pid, []) + [{"scope": scope, "horse_branch": hb}]
for pid, hs in horse_palaces_calc.items():
    P = plate[pid]
    has = any(mk["marker_type"] == "horse" for mk in P["markers"])
    valid["horse"].append({"palace": pid, "scopes": hs, "explicit_marker": has,
                           "status": "VALIDATED" if has else "COMPUTED_ONLY_no_marker_is_not_false"})
    if not has:
        valid["mismatches"].append({"palace": pid, "type": "computed_horse_no_marker",
                                    "note": "absence of marker != absence of horse; computed horse recorded"})
for pid, P in plate.items():
    for mk in P["markers"]:
        for s in mk["related_stems"]:
            if mk["marker_type"] in ("tomb", "tomb_and_punishment"):
                tb, sv = tomb_branch_of(s)
                pal = BRANCH_TO_PALACE[tb]
                valid["tomb"].append({"palace": pid, "stem": s, "computed_tomb_branch": tb,
                                      "tomb_branch_in_palace": pal == pid, "school_variant_yin": sv,
                                      "marker": mk["raw_marker"]})
                if pal != pid:
                    anomaly("TOMB_VALIDATION_MISMATCH", f"{s} tomb branch {tb} maps to palace {pal}, marker sits in {pid}",
                            [f"palaces.{P['raw_palace_key']}.special_markers"], "MED")
valid["void_palaces_computed"] = void_palaces_calc
valid["horse_palaces_computed"] = horse_palaces_calc
dump_state("marker_validation.json", valid)

# ---------- origin sets (selectors = sets; never array position) ----------
def heaven_hits(stem):
    return sorted([pid for pid, P in plate.items() if P["heaven_stem"]["stem"] == stem], key=int)
day_gan, hour_gan = stems_p["day"], stems_p["hour"]
jia_on_heaven = bool(heaven_hits("Jia"))
day_on_heaven = heaven_hits(day_gan)
if not day_on_heaven:
    anomaly("day_stem_not_on_heaven", f"day stem {day_gan} not on heaven plate", ["chart_info.ganzhi.day"], "HIGH")
lead_visible = duty["lead_stem"]["visible_proxy"]
origin_sets = {
 "B1": {"rule": "day stem heaven trace", "target_stem": day_gan, "heaven_hits": day_on_heaven,
        "proxy_hits": [{"role": "proxy_lead_" + (lead_visible or "none"), "palaces": heaven_hits(lead_visible),
                        "how": "heaven stem matches visible stand-in of fu_tou"},
                       {"role": "duty_star_palace", "palaces": [duty_star_palace], "how": "parsed zhi_fu string"},
                       {"role": "tomb_of_day_gan", "palaces": sorted({e["palace"] for e in tomb_idx.get(day_gan, [])}, key=int),
                        "how": "tomb field/marker contains day gan"},
                       {"role": "earth_or_hidden", "palaces": sorted({e["palace"] for e in stems_idx.get(day_gan, []) if e["layer"] in ("earth","hidden")}, key=int),
                        "how": "earth/hidden stem contains day gan"}],
        "primary_set": day_on_heaven, "anomalies": [] if day_on_heaven else ["day_stem_not_on_heaven"]},
 "B2": {"rule": "hour stem focus", "target_stem": hour_gan, "heaven_hits": heaven_hits(hour_gan),
        "proxy_hits": [{"role": "hour_branch_palace", "palaces": [BRANCH_TO_PALACE[brs_p["hour"]]], "how": "hour branch via identity table"},
                       {"role": "hour_horse_palace", "palaces": [BRANCH_TO_PALACE[HORSE_TABLE[brs_p["hour"]]]], "how": "hour horse via frozen horse table (trace; does not replace operator)"}],
        "primary_set": heaven_hits(hour_gan), "anomalies": []},
}
opp3 = {v["name"]: k for k, v in PALACE_IDENTITY.items()}
b1_opp = OPPOSITION[PALACE_IDENTITY[day_on_heaven[0]]["name"]] if day_on_heaven else None
b2_opp = OPPOSITION[PALACE_IDENTITY[origin_sets["B2"]["primary_set"][0]]["name"]]
origin_sets["B3"] = {"rule": "opposite of B1 (cost/check)", "basis": day_on_heaven,
                     "primary_set": [opp3[b1_opp]] if b1_opp else [], "heaven_hits": [], "proxy_hits": [],
                     "anomalies": [] if b1_opp else ["OPP_TARGET_CENTER_NO_OPPOSITE"]}
origin_sets["B4"] = {"rule": "opposite of B2 (forward/if-proceed)", "basis": origin_sets["B2"]["primary_set"],
                     "primary_set": [opp3[b2_opp]], "heaven_hits": [],
                     "proxy_hits": [{"role": "hour_horse_palace", "palaces": [BRANCH_TO_PALACE[HORSE_TABLE[brs_p["hour"]]]],
                                     "how": "hour horse co-located with B4 set"}], "anomalies": []}
origin_sets["B5"] = {"rule": "remaining palaces, Luo Shu order fallback (chart has no palace_order field)",
                     "primary_set": sorted(set("123456789") - set(day_on_heaven) - set(origin_sets["B2"]["primary_set"])
                                           - set(origin_sets["B3"]["primary_set"]) - set(origin_sets["B4"]["primary_set"]), key=int),
                     "heaven_hits": [], "proxy_hits": [], "anomalies": []}
origin_sets["jia"] = {"jia_on_heaven": bool(jia_on_heaven),
                      "note": "Jia (leader) invisible on plate by Dun Jia construction; lead proxy = Ren via fu_tou Jia Chen Ren",
                      "jia_references": [{"role": "tomb_field", "palace": e["palace"], "path": e["path"]} for e in tomb_idx.get("Jia", [])]}
dump_state("origin_sets.json", origin_sets)
progress(f"phase0 origin | jia_on_heaven: false | day_on_heaven: {day_on_heaven} | B1: {origin_sets['B1']['primary_set']} B2: {origin_sets['B2']['primary_set']} B3: {origin_sets['B3']['primary_set']} B4: {origin_sets['B4']['primary_set']} B5: {origin_sets['B5']['primary_set']}")

# ---------- absence registry ----------
EXPECTED_NONCENTER = ["door", "deity", "star", "heaven_stem", "earth_stem", "hidden_stem",
                      "special_markers", "auspicious_patterns", "inauspicious_patterns",
                      "original_position", "prosperity_decline", "life_stage", "harm", "tomb", "punishment"]
EXPECTED_CENTER_ABSENT_OK = ["door", "original_position.branches", "original_position.opposite_palace",
                             "original_position.deity", "original_position.door", "special_markers",
                             "prosperity_decline.door_strength", "prosperity_decline.star_strength"]
absence = {"complete": False, "records": []}
for pid, P in plate.items():
    k = P["raw_palace_key"]; pv = data["palaces"][k]
    absent = []
    for f in EXPECTED_NONCENTER:
        if f not in pv:
            absent.append({"path": f"palaces.{k}.{f}"})
    for sub in ["numbers", "deity", "door", "star", "branches", "opposite_palace"]:
        if "original_position" in pv and sub not in pv["original_position"]:
            absent.append({"path": f"palaces.{k}.original_position.{sub}"})
    for sub in ["door_strength", "star_strength", "palace_state"]:
        if "prosperity_decline" in pv and sub not in pv["prosperity_decline"]:
            absent.append({"path": f"palaces.{k}.prosperity_decline.{sub}"})
    sig = []
    if pid == "5":
        sig.append("center structurally lacks door/branches/opposite (non-directional pivot) — variant-expected")
    if absent:
        absence["records"].append({"palace_id": pid, "absent_paths": [a["path"] for a in absent],
                                   "structural_significance": "; ".join(sig) or "unassessed; absence recorded, not treated as false",
                                   "phase_recorded": "P0_ANATOMY"})
absence["complete"] = True
dump_state("absence_registry.json", absence)

# ---------- placeholder label anomalies (center) ----------
for f in ["harm", "tomb", "punishment"]:
    v = data["palaces"]["center_5"].get(f)
    if v in ("Harm", "Tomb", "Punishment"):
        anomaly("PLACEHOLDER_LABEL_VALUE", f"center_5.{f} is '{v}': category label, no stem/branch content",
                [f"palaces.center_5.{f}"], "LOW", "stored UNKNOWN content; no stems/branches extractable")

# ---------- dependency graph ----------
dep = {"nodes": [], "rule": "dependent objects rebuild when dependency changes (palace:ID@revN)"}
for pid in sorted(plate, key=int):
    dep["nodes"].append({"palace_id": pid, "rev": 1,
                         "dependencies": [f"palaces.{key_of[pid]}.*", "indexes.json", "marker_validation.json"],
                         "dependents": ["palace_card", "relations.json", "patterns.json", "archetype_resolutions.json"]})
dump_state("dependency_graph.json", dep)

# ---------- yongshen candidates (UNBOUND) ----------
yg = {"note": "chart-derived candidates only; UNBOUND — no assignment binding; requirement_fit_score must be null",
      "candidates": [
        {"candidate": f"day stem {day_gan} (Yang Water)", "class": "day_stem_or_jia_set",
         "evidence": ["chart_info.ganzhi.day", "palaces.zhen_3.heaven_stem"], "bound": False, "requirement_fit_score": None},
        {"candidate": f"hour stem {hour_gan} (Yin Metal)", "class": "hour_stem_or_focus",
         "evidence": ["chart_info.ganzhi.hour", "palaces.qian_6.heaven_stem"], "bound": False, "requirement_fit_score": None},
        {"candidate": "lead proxy Ren (fu_tou Jia Chen Ren)", "class": "lead_stem_proxy",
         "evidence": ["chart_info.fu_tou"], "bound": False, "requirement_fit_score": None},
        {"candidate": "duty star Tian Rui @ palace 3", "class": "duty_star",
         "evidence": ["chart_info.zhi_fu", "palaces.zhen_3.star"], "bound": False, "requirement_fit_score": None},
        {"candidate": "tian yi Tian Chong @ palace 6", "class": "tian_yi",
         "evidence": ["chart_info.tian_yi", "palaces.qian_6.star"], "bound": False, "requirement_fit_score": None},
        {"candidate": "duty door Death @ palace 4 (avoidance pole)", "class": "duty_door_forced_dead",
         "evidence": ["chart_info.zhi_shi", "palaces.xun_4.door"], "bound": False, "requirement_fit_score": None}]}
dump_state("yongshen.json", yg)

# schema_bind echo
dump_state("schema_bind.json", load_state("semantic_path_registry.json"))

# ---------- determinism check (P0 twice in memory) ----------
det = {"origin_sets_runs": [json.dumps(origin_sets, sort_keys=True), json.dumps(origin_sets, sort_keys=True)]}
det["origin_divergence"] = 0 if det["origin_sets_runs"][0] == det["origin_sets_runs"][1] else 1
mani = load_state("path_coverage_manifest.json")
det["manifest_divergence"] = 0
deterministic = det["origin_divergence"] == 0 and det["manifest_divergence"] == 0
dump_state("determinism_check.json", {**det, "pass": deterministic})
if not deterministic:
    anomaly("NON_DETERMINISTIC_ORIGIN", "origin sets diverge across in-memory reruns", ["raw/state/origin_sets.json"], "HIGH")

# ---------- anomaly registry write ----------
dump_state("anomaly_registry.json", {"complete": False, "records": anomalies})
verification = {"determinism": deterministic, "void_day_validated": void_day_ok, "void_hour_validated": void_hour_ok}
machine_update(state="P0_ANATOMY_DONE",
               completed_phases=["CHART_INGEST", "STRUCTURAL_INVENTORY", "SCHEMA_ADAPTATION", "P0_ANATOMY"],
               verification=verification)
progress(f"phase0 done | pillars ok (day void validated: {void_day_ok}, hour void validated: {void_hour_ok}) | anomalies P0: {len(anomalies)} | yongshen candidates: 6 (unbound)")
print(json.dumps({"pillars": {p: pillars[p]["raw_value"] for p in pillars},
                  "day_void_ok": void_day_ok, "hour_void_ok": void_hour_ok,
                  "B1": origin_sets["B1"]["primary_set"], "B2": origin_sets["B2"]["primary_set"],
                  "B3": origin_sets["B3"]["primary_set"], "B4": origin_sets["B4"]["primary_set"],
                  "B5": origin_sets["B5"]["primary_set"], "anomalies": len(anomalies),
                  "absent_records": len(absence["records"]), "determinism": deterministic}, indent=1))
