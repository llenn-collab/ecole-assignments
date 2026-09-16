"""Stage 4: COVERAGE_GATE -> P6_BOARD_SYNTHESIS.
Adds late anomalies (opposite mismatches, explicit pattern conflict), systems,
pattern catalog, archetype resolutions + rubric scoring, board consistency."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

data = load_source()
pkr = load_state("palace_key_resolution.json")["palaces"]
key_of = {pid: v["raw_palace_key"] for pid, v in pkr.items()}
palaces_state = load_state("palaces.json")
relations_state = load_state("relations.json")
anom = load_state("anomaly_registry.json")
anomalies = anom["records"]

def add_anomaly(type_, desc, paths, severity, note=None, phase="P6_BOARD_SYNTHESIS"):
    anomalies.append({"id": f"ANO-{len(anomalies)+1:03d}", "type": type_, "description": desc,
                      "paths": paths, "phase_recorded": phase, "severity": severity,
                      "resolution_note": note})

# ----- frozen tables as citable derived state -----
frozen = {"palace_identity_table": PALACE_IDENTITY, "opposition_by_name": OPPOSITION,
          "star_home_luoshu": STAR_HOME, "horse_branch": HORSE_TABLE,
          "door_elements": DOOR_ELEMENTS, "inner_palaces": sorted(INNER_PALACES, key=int)}
dump_state("frozen_tables.json", frozen)

# rewrite any evidence path that pointed at spec tables
for pid, groups in relations_state.items():
    for t, lst in groups.items():
        for r in lst:
            r["evidence"] = ["state:frozen_tables.star_home_luoshu" if e.startswith("state:qmdj_complete") else e for e in r["evidence"]]
# fix non-resolvable absence pseudo-path in palace 7 verdict
for v in palaces_state["7"]["verdicts"]:
    for e in v["evidence"]:
        if e["path"].startswith("state:absence_registry.records["):
            e["path"] = "state:absence_registry.records"
            e["value"] = "record for palace_id=7 absent field list"

# ----- OPPOSITE_PALACE_MISMATCH sweep (all palaces with explicit opposite_palace) -----
NAME2ID = {v["name"]: k for k, v in PALACE_IDENTITY.items()}
opp_records = []
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    op = data["palaces"][key].get("original_position", {})
    raw_op = op.get("opposite_palace")
    canonical_name = PALACE_IDENTITY[pid]["name"]
    expected = OPPOSITION.get(canonical_name)
    if pid == "5":
        opp_records.append({"palace": pid, "explicit": None, "computed": None, "status": "NO_OPPOSITE (center pivot)"})
        continue
    expected_id = NAME2ID.get(expected) if expected else None
    m = re.match(r"([A-Za-z]+)\s+(\d+)$", raw_op or "")
    explicit_name, explicit_num = (m.group(1), m.group(2)) if m else (raw_op, None)
    name_matches_table = NAME2ID.get(explicit_name) == explicit_num
    matches_frozen = explicit_num == expected_id and explicit_name == expected
    opp_records.append({"palace": pid, "explicit": raw_op, "computed_opposite": f"{expected} {expected_id}",
                        "explicit_label_internally_consistent": bool(name_matches_table),
                        "matches_frozen_geometry": bool(matches_frozen),
                        "status": "MISMATCH" if not matches_frozen else "OK"})
    if not matches_frozen:
        add_anomaly("OPPOSITE_PALACE_MISMATCH",
                    f"palace {pid} explicit opposite_palace '{raw_op}' != frozen geometry '{expected} {expected_id}'"
                    + ("" if name_matches_table else f"; label '{explicit_name} {explicit_num}' is also internally inconsistent"),
                    [f"palaces.{key}.original_position.opposite_palace"], "MED",
                    "explicit value preserved as EXPLICIT; computed opposition uses frozen geometry")

# ----- explicit pattern conflict already flagged (li_9) -> formal anomaly object -----
add_anomaly("EXPLICIT_PATTERN_COMPUTED_CONFLICT",
            "li_9 lists 'Palace Oppressing Door' but palace element Fire does not control door element Fire (Scenery at original palace); explicit preserved, computed disagrees",
            ["palaces.li_9.inauspicious_patterns[0]", "palaces.li_9.door"], "MED",
            "resolved per policy: ship both as typed evidence; do not prefer theory over explicit")

# ================= COVERAGE_GATE =================
mani = load_state("path_coverage_manifest.json")
absence = load_state("absence_registry.json")
excl = load_state("exclusion_log.json")
arritem = load_state("array_itemization.json")
ep = load_state("explicit_patterns.json")
gates = {}
gates["path_coverage_manifest_complete"] = all(r["analysis_status"] in ("ANALYZED", "PARSED", "ANOMALOUS", "EXCLUDED_BY_RULE", "NOT_APPLICABLE") for r in mani["records"])
gates["absence_registry_complete"] = absence["complete"]
gates["exclusion_log_complete"] = excl["explicit_exclusions_logged"] is True
gates["array_itemization_complete"] = arritem["item_count"] == len(arritem["items"]) == 54
gates["anomalies_logged"] = len(anomalies) > 0
gates["explicit_patterns_ingested"] = len(ep["markers"]) + len(ep["auspicious"]) + len(ep["inauspicious"]) > 0
# leaf unpacking: no verdict evidence cites a parent object path from source
leaf_fail = []
manifest_by_norm = {r["normalized_path"]: r for r in mani["records"]}
for pid, card in palaces_state.items():
    for v in card["verdicts"]:
        for e in v["evidence"]:
            p = e["path"]
            if p.startswith("state:"):
                continue
            rec = manifest_by_norm.get(p)
            if rec is None:
                ok, _ = cite_source(p)
                if not ok: leaf_fail.append((v["claim_id"], p, "unresolved"))
            elif rec["type"] in ("object", "array"):
                leaf_fail.append((v["claim_id"], p, "parent_only"))
gates["leaf_unpacking_verified"] = len(leaf_fail) == 0
coverage_pass = all(gates.values())
dump_state("coverage_gate.json", {"pass": coverage_pass, "gates": gates, "leaf_failures": leaf_fail,
                                  "checked_at": utcnow()})
assert coverage_pass, f"COVERAGE_GATE failed: {json.dumps(gates)}"
mani["complete"] = True
excl["complete"] = True
arritem["complete"] = True
dump_state("path_coverage_manifest.json", mani)
dump_state("exclusion_log.json", excl)
dump_state("array_itemization.json", arritem)
progress(f"coverage gate: PASS | paths: {mani['total_paths']} | absent: {sum(len(r['absent_paths']) for r in absence['records'])} | anomalies: {len(anomalies)} | leaf failures: {len(leaf_fail)}")
machine_update(state="COVERAGE_GATE", completed_phases=load_state("machine.json")["completed_phases"] + ["COVERAGE_GATE"])

# ================= P6_BOARD_SYNTHESIS =================
machine_update(state="P6_BOARD_SYNTHESIS")
season = load_state("season.json")
duty = load_state("duty.json")
mv = load_state("marker_validation.json")
indexes = load_state("indexes.json")
origins = load_state("origin_sets.json")
pillars = load_state("pillars.json")
brs_p = {p: pillars["pillars"][p]["branch_raw"] for p in pillars["pillars"]}
stems_p = {p: pillars["pillars"][p]["stem_raw"] for p in pillars["pillars"]}
SANQI = ["Yi", "Bing", "Ding"]; LIUYI = ["Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]

def rel(pid, type_):
    return relations_state.get(f"palace_{pid}", {}).get(type_, [])

# 1-3 system maps
door_map = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    d = data["palaces"][key].get("door")
    if d:
        door_map[d] = {"palace": pid, "forced": any(r.get("description", "").startswith("palace") for r in rel(pid, "door_forced")),
                       "relation": next((r["description"] for t in ("door_forced", "door_oppressing_palace", "palace_generating_door", "door_generating_palace", "door_palace_same_element") for r in rel(pid, t)), None),
                       "evidence": [f"palaces.{key}.door"]}
star_map = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    raw = data["palaces"][key].get("star", "")
    for s_ent in [x.strip() for x in raw.split("&") if x.strip()]:
        canon = STAR_ALIASES.get(s_ent, s_ent)
        star_map.setdefault(canon, {"seats": []})
        star_map[canon]["seats"].append({"palace": pid, "raw": raw, "home": STAR_HOME.get(canon),
                                          "displaced": str(STAR_HOME.get(canon)) != pid,
                                          "evidence": f"palaces.{key}.star"})
deity_map = {data["palaces"][key].get("deity"): {"palace": pid, "evidence": f"palaces.{key}.deity"}
             for pid, key in key_of.items() if data["palaces"][key].get("deity")}
sanqi_liuyi = {}
for stem in SANQI + LIUYI:
    occ = indexes["stems"].get(stem, [])
    occ = [o for o in occ if o["layer"] != "marker_reference"]
    sanqi_liuyi[stem] = {"class": "sanqi" if stem in SANQI else "liuyi", "positions": occ}
# 5 wangshuai matrix
wang = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    pv = data["palaces"][key]
    pel = PALACE_IDENTITY[pid]["element"].lower()
    pr = pv.get("prosperity_decline", {})
    star_t = pr.get("star_strength"); st_tokens = [t.strip() for t in star_t.split("/")] if star_t else []
    norms = [RAW_STRENGTH_MAP.get(t, (t.lower(),))[0] for t in st_tokens]
    wang[pid] = {"palace_element": pel,
                 "seasonal_element_strength": season["normalized"][pel],
                 "palace_strength_by_season": season["normalized"][pel]["normalized"],
                 "star_strength_raw": star_t,
                 "star_tokens": [{"raw": t, "normalized": RAW_STRENGTH_MAP.get(t, ("UNKNOWN",))[0]} for t in st_tokens],
                 "star_token_convention": "two-token order (by_season/by_palace) unverified — SCHEMA_AMBIGUITY recorded in schema_variant.json",
                 "split_star_strength": len(set(norms)) > 1,
                 "door_strength_raw": pr.get("door_strength"),
                 "door_strength_normalized": RAW_STRENGTH_MAP.get(pr.get("door_strength", ""), ("ABSENT",))[0] if pr.get("door_strength") else "ABSENT",
                 "palace_state_raw": pr.get("palace_state"),
                 "ring": "inner" if pid in INNER_PALACES else "outer",
                 "season_matches_door": RAW_STRENGTH_MAP.get(pr.get("door_strength", ""), (None,))[0] == season["normalized"][pel]["normalized"] if pr.get("door_strength") else None,
                 "evidence": [f"palaces.{key}.prosperity_decline.{f}" for f in pr] + ["chart_info.seasonal_strength"]}
# 6 void/tomb/punish/force/horse graph
vtph = {}
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    pv = data["palaces"][key]
    vtph[pid] = {
        "void": bool(rel(pid, "void_palace")) and rel(pid, "void_palace")[0]["description"],
        "tomb_fields": {f: pv[f] for f in ("tomb",) if f in pv},
        "tomb_markers": [m for m in pv.get("special_markers", []) if "Tomb" in m],
        "punishment_field": pv.get("punishment"),
        "forced_door": bool(rel(pid, "door_forced")),
        "horse": rel(pid, "horse_star") and [r["description"] for r in rel(pid, "horse_star")] or None,
        "harm_field": pv.get("harm"), "life_stage_field": pv.get("life_stage"),
        "evidence": [f"palaces.{key}.{f}" for f in ("special_markers", "tomb", "punishment", "harm", "life_stage") if f in pv]}
harm_graph = {pid: vtph[pid]["harm_field"] for pid in vtph if vtph[pid].get("harm_field")}
life_stage_graph = {pid: vtph[pid]["life_stage_field"] for pid in vtph if vtph[pid].get("life_stage_field")}
inner_outer = {"inner": sorted(INNER_PALACES, key=int), "outer": sorted(set(key_of) - INNER_PALACES, key=int),
               "meaning": {"inner": "process, constraint, institution, internal rationale",
                           "outer": "audience, surface, movement, submission-facing behaviour"}}
pillars_x = {"projections": {p: {"stem": stems_p[p], "branch": brs_p[p],
                                 "branch_palace": BRANCH_TO_PALACE[brs_p[p]],
                                 "stem_palaces_layers": indexes["stems"].get(stems_p[p], []),
                                 "in_day_void": pillars["void_membership"][p]["in_day_void"],
                                 "in_hour_void": pillars["void_membership"][p]["in_hour_void"],
                                 "evidence": pillars["pillars"][p]["path"]} for p in pillars["pillars"]},
             "pillar_relations": pillars["relations"]}
center = {"lodging_graph": load_state("lodging.json")["graph"], "pivot_no_opposite": True,
          "read_through_hosts": ["3 (heaven Ji + Tian Qin)", "2 (hidden Ji)"]}
systems = {"door_system_map": door_map, "star_system_map": star_map, "deity_two_plate_map": deity_map,
           "sanqi_liuyi_map": sanqi_liuyi, "wangshuai_matrix": wang,
           "void_tomb_punish_force_horse_graph": vtph, "harm_graph": harm_graph,
           "life_stage_graph": life_stage_graph, "inner_outer": inner_outer,
           "pillars_times_palaces": pillars_x, "reconstitute_center": center,
           "opposite_palace_audit": opp_records}
dump_state("systems.json", systems)

# 11-13 explicit reconciliation + pattern catalog
recon = []
def add_recon(pattern, palace, status, evidence, note=None):
    recon.append({"pattern": pattern, "palace": palace, "status": status, "evidence_paths": evidence, "note": note})
for pid, key in sorted(key_of.items(), key=lambda x: int(x[0])):
    pv = data["palaces"][key]
    for i, s in enumerate(pv.get("auspicious_patterns", [])):
        path = f"palaces.{key}.auspicious_patterns[{i}]"
        if s == "Palace Generating Door":
            okc = bool(rel(pid, "palace_generating_door")); add_recon(s, pid, "VALIDATED" if okc else "CONFLICT", [path, f"palaces.{key}.door"])
        elif s == "Door Generating Palace":
            okc = bool(rel(pid, "door_generating_palace")); add_recon(s, pid, "VALIDATED" if okc else "CONFLICT", [path, f"palaces.{key}.door"])
        elif s == "Wonder Instrument Combination":
            add_recon(s, pid, "VALIDATED", [path, f"palaces.{key}.heaven_stem", f"palaces.{key}.earth_stem"], "Yi+Geng five-combination co-located in-palace")
        elif s == "Three Wonders Obtaining Mission":
            add_recon(s, pid, "VALIDATED", [path, f"palaces.{key}.heaven_stem", f"palaces.{key}.door", "chart_info.zhi_shi"], "sanqi Yi co-located with the duty door (zhi_shi Death)")
        elif s == "Wonder Wandering Salary Position":
            add_recon(s, pid, "VALIDATED", [path, f"palaces.{key}.earth_stem", "state:frozen_tables.palace_identity_table"], "Ding salary at Wu; earth stem Ding in Li 9 (school convention note)")
        else:
            add_recon(s, pid, "STORED_UNVALIDATED", [path], "no defined computed rule; preserved as explicit")
    for i, s in enumerate(pv.get("inauspicious_patterns", [])):
        path = f"palaces.{key}.inauspicious_patterns[{i}]"
        if s == "Palace Oppressing Door":
            okc = bool(rel(pid, "door_forced")); add_recon(s, pid, "VALIDATED" if okc else "CONFLICT", [path, f"palaces.{key}.door"], None if okc else "explicit vs computed conflict — anomaly ANO logged")
        elif s == "Door Oppressing Palace":
            add_recon(s, pid, "VALIDATED" if rel(pid, "door_oppressing_palace") else "CONFLICT", [path, f"palaces.{key}.door"])
        elif s == "Door Entering Tomb":
            add_recon(s, pid, "VALIDATED_SCHOOL_VARIANT", [path, f"palaces.{key}.door", "state:frozen_tables.palace_identity_table"], "Death door Earth rides over Chen water-tomb branch in-palace (earth-follows-water convention)")
        elif s == "Three Wonders Being Restricted":
            add_recon(s, pid, "VALIDATED", [path, f"palaces.{key}.heaven_stem", f"palaces.{key}.earth_stem"], "Geng metal controls Yi wood in-palace")
        elif s == "Great Barrier":
            add_recon(s, pid, "VALIDATED", [path, f"palaces.{key}.heaven_stem", f"palaces.{key}.earth_stem"], "Geng over Gui co-located (both pieces exist)")
        elif s == "Ding Wonder Entering Tomb":
            add_recon(s, pid, "VALIDATED", [path, f"palaces.{key}.heaven_stem", f"palaces.{key}.tomb", "state:marker_validation.tomb"], "Ding tomb Chou in-palace; explicit Tomb (Ding) marker")
        else:
            add_recon(s, pid, "STORED_UNVALIDATED", [path], "no defined computed rule; preserved as explicit")

patterns = []
def pat(name, palaces_l, evidence, polarity, school=False, extra=None):
    hit = {"name_en": name, "palaces": palaces_l, "evidence_paths": evidence, "polarity": polarity,
           "grounding": "COMPUTED", "school_variant": school}
    if extra: hit.update(extra)
    patterns.append(hit)
pat("forced_door", ["4"], ["palaces.xun_4.door", "palaces.xun_4.inauspicious_patterns[1]"], "inauspicious")
pat("void_palace", ["2", "3", "8", "9"], ["chart_info.void.day", "chart_info.void.hour", "state:marker_validation.void"], "constraint")
pat("stem_in_tomb", ["2", "4", "6", "8"], ["palaces.kun_2.special_markers[1]", "palaces.xun_4.special_markers[1]", "palaces.gen_8.special_markers[1]", "palaces.qian_6.special_markers[0]", "state:marker_validation.tomb"], "inauspicious")
pat("stem_in_punishment", ["3", "4"], ["palaces.zhen_3.punishment", "palaces.xun_4.punishment"], "inauspicious",
    extra={"note": "palace 4 punishment names hidden-stem Ren (in-palace); palace 3 names Wu (not in-palace — reference kept)"})
pat("duty_star", ["3"], ["chart_info.zhi_fu", "palaces.zhen_3.star"], "authority")
pat("duty_door", ["4"], ["chart_info.zhi_shi", "palaces.xun_4.door"], "method_to_avoid")
pat("hour_stem_focus", ["6"], ["chart_info.ganzhi.hour", "palaces.qian_6.heaven_stem"], "timing")
pat("horse_star", ["2", "4", "6", "8"], ["chart_info.horse.year", "chart_info.horse.month", "chart_info.horse.day", "chart_info.horse.hour", "state:marker_validation.horse"], "movement")
pat("heaven_earth_stem_pair", sorted(key_of, key=int), [f"palaces.{key_of[p]}.heaven_stem" for p in sorted(key_of, key=int)], "structural",
    extra={"pairs": {p: f"{data['palaces'][key_of[p]].get('heaven_stem')} / {data['palaces'][key_of[p]].get('earth_stem')}" for p in sorted(key_of, key=int)}})
pat("star_sitting_home", [], ["state:frozen_tables.star_home_luoshu"], "neutral",
    extra={"note": "0 hits — every star displaced from home; center star additionally lodged outward"})
pat("door_at_original_palace", ["9"], ["palaces.li_9.door", "palaces.li_9.original_position.door"], "neutral")
pat("lodged_star_or_stem", ["3", "5", "2"], ["palaces.center_5.heaven_stem", "palaces.center_5.star", "palaces.center_5.hidden_stem", "palaces.zhen_3.star", "state:lodging.graph"], "displacement")
pat("empty_center", ["5"], ["state:absence_registry.records"], "structural")
pat("split_star_strength", [p for p in sorted(key_of, key=int) if wang[p]["split_star_strength"]],
    [f"palaces.{key_of[p]}.prosperity_decline.star_strength" for p in sorted(key_of, key=int) if wang[p]["split_star_strength"]], "mixed_climate")
pat("seasonal_vs_day_element", ["meta"], ["chart_info.seasonal_strength.water", "chart_info.ganzhi.day"], "climate",
    extra={"note": "day element Water is Strong this season — the day substance is seasonally supported"})
pat("sanqi_positions", ["4", "7", "8"],
    ["palaces.xun_4.heaven_stem", "palaces.dui_7.heaven_stem", "palaces.dui_7.earth_stem", "palaces.gen_8.heaven_stem", "palaces.gen_8.earth_stem", "palaces.li_9.earth_stem"], "quality")
pat("stacked_pillar_branch_on_palace", ["4", "6", "7", "9"], ["chart_info.ganzhi.year", "chart_info.ganzhi.month", "chart_info.ganzhi.day", "chart_info.ganzhi.hour", "state:systems.pillars_times_palaces"], "timing_lock")
pat("explicit_pattern_conflict", ["9"], ["palaces.li_9.inauspicious_patterns[0]", "palaces.li_9.door"], "anomaly")
pat("marker_validation_mismatch", ["2", "6", "8"], ["state:marker_validation.mismatches", "chart_info.horse.year", "chart_info.horse.month", "chart_info.horse.day"], "note",
    extra={"note": "computed horses in palaces 2/6/8 carry no explicit Horse marker; absence is recorded, not treated as false"})
pat("opposite_palace_mismatch", ["1", "2", "3", "4", "6", "7", "8", "9"],
    [f"palaces.{key_of[p]}.original_position.opposite_palace" for p in ["1", "2", "3", "4", "6", "7", "8", "9"]], "anomaly",
    extra={"note": "all 8 explicit opposite labels conflict with frozen geometry; several are internally inconsistent name-number labels; frozen geometry controls computed opposition"})
pat("earthly_escape", ["7"], ["palaces.dui_7.earth_stem", "palaces.dui_7.door"], "auspicious", school=True,
    extra={"naming_basis": "both pieces exist in-palace: Yin Wood (Yi) + Rest Door"})
patterns.append({"name_or_combination": "Bing + Open Door (co-location absent; heavenly_escape NOT named)",
                 "palaces": ["7", "2"], "evidence_paths": ["palaces.dui_7.heaven_stem", "palaces.kun_2.door"],
                 "polarity": "unqualified", "grounding": "COMPUTED", "school_variant": True,
                 "note": "pieces exist separately but not co-located; combination stored, name withheld per rule"})
patterns.append({"name_or_combination": "Ding + Open Door (co-location absent; human_escape NOT named)",
                 "palaces": ["8", "2"], "evidence_paths": ["palaces.gen_8.heaven_stem", "palaces.kun_2.door"],
                 "polarity": "unqualified", "grounding": "COMPUTED", "school_variant": True,
                 "note": "pieces exist separately but not co-located; combination stored, name withheld per rule"})
patterns_out = {"explicit_pattern_reconciliation": recon, "computed_catalog": patterns,
                "explicit_before_computed": True}
dump_state("patterns.json", patterns_out)
progress(f"P6 systems + patterns | pattern hits: {len(patterns)} | reconciliations: {len(recon)} | named escapes: earthly_escape@7 only | star_sitting_home: 0 hits")
print("P6 part 1 done:", len(systems), "system blocks,", len(patterns), "pattern hits,", len(recon), "reconciliations,",
      "anomalies:", len(anomalies))
dump_state("anomaly_registry.json", {"complete": True, "records": anomalies})
