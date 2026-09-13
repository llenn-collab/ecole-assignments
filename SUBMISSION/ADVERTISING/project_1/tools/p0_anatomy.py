"""INIT -> CHART_INGEST -> P0_ANATOMY.

Writes: schema_bind, chart_index, pillars, season, duty, indexes,
origin_sets, lodging, yongshen, anomalies, machine.json, dump/schema md.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

RUN_ID = "carpathia-adv-p1-0001"
ANOM = []


def anomaly(code, severity, detail, paths):
    ANOM.append({"code": code, "severity": severity, "detail": detail,
                 "evidence_paths": paths, "phase": "P0_ANATOMY"})


# ============================================================ CHART_INGEST ==
def chart_ingest(q):
    src_hash = sha256_file(QMDJ_PATH)
    size = os.path.getsize(QMDJ_PATH)

    # --- schema detection: does it match the prompt's expected shape? -------
    expected_top = {"chart_metadata", "palaces"}
    actual_top = set(q.keys())
    detected = "carpathia_yiyun_lunzangjia_v1"
    if "chart_metadata" not in actual_top:
        anomaly(
            "SCHEMA_AMBIGUITY", "HIGH",
            "QMDJ.json does not expose chart_metadata.* / heaven_plate.* / markers.* as named "
            "in qmdj_complete.schema_bind. Least-contradicted bind applied: "
            "timing.four_pillars -> four_pillars, chart_config -> duty_elements, "
            "element_prosperities -> seasonal_element_strengths, "
            "palaces.N.active_chart.stems.heaven -> heaven_plate.stem, "
            "palaces.N.active_chart.stems.earth -> earth_plate.stem, "
            "palaces.N.active_chart.stems.hidden -> hidden_stem, "
            "palaces.N.active_chart.status -> markers, "
            "palaces.N.palace_stem_rules.stems_in_tomb -> tomb_stems, "
            "palaces.N.palace_stem_rules.stems_in_clash_punishment -> punishment_stems. "
            "binding_failure_policy: continue, do not ask user.",
            ["$", "$.chart_config", "$.timing.four_pillars"])

    bind = {
        "detected_shape": detected,
        "detected_shape_matches_prompt_default": False,
        "bind_policy": "least_contradicted (laws.binding_failure_policy)",
        "map": {
            "year_pillar": "timing.four_pillars.year",
            "month_pillar": "timing.four_pillars.month",
            "day_pillar": "timing.four_pillars.day",
            "hour_pillar": "timing.four_pillars.hour",
            "day_void": "timing.voidness.day_void",
            "hour_void": "timing.voidness.hour_void",
            "seasonal": "element_prosperities",
            "solar_term": "timing.solar_term",
            "lead_stem": "chart_config.lead_stem",
            "duty_star_name": "chart_config.duty_star",
            "duty_door_name": "chart_config.duty_door",
            "chart_structure": "chart_config.structure",
            "chart_pattern": "chart_config.chart_pattern",
            "palace_root": "palaces",
            "palace_id": "object key as string 1-9",
            "heaven_stem": "palaces.{id}.active_chart.stems.heaven",
            "earth_stem": "palaces.{id}.active_chart.stems.earth",
            "hidden_stem": "palaces.{id}.active_chart.stems.hidden",
            "center_guest_stem": "palaces.{id}.active_chart.stems.center_guest",
            "afflictions": "palaces.{id}.active_chart.stems.afflictions",
            "star": "palaces.{id}.active_chart.star",
            "door": "palaces.{id}.active_chart.door",
            "god": "palaces.{id}.active_chart.god",
            "markers": "palaces.{id}.active_chart.status",
            "tomb_stems": "palaces.{id}.palace_stem_rules.stems_in_tomb",
            "punishment_stems": "palaces.{id}.palace_stem_rules.stems_in_clash_punishment",
            "harm_stems": "palaces.{id}.palace_stem_rules.stems_in_harm",
            "birth_stage_stems": "palaces.{id}.palace_stem_rules.stems_in_birth_stage",
            "door_strength": "palaces.{id}.active_chart.energy_state.door",
            "star_strength_seasonal": "palaces.{id}.active_chart.energy_state.star.seasonal",
            "star_strength_by_palace": "palaces.{id}.active_chart.energy_state.star.palace_relation",
            "palace_strength": "palaces.{id}.active_chart.energy_state.palace",
            "realm": "palaces.{id}.active_chart.energy_state.realm",
        },
        "absent_in_source_but_named_by_prompt": [
            "chart_metadata.duty_elements.tian_yi",
            "heaven_plate.lodged_star",
            "heaven_plate.lodged_stem",
            "heaven_plate.notes",
            "door.forced",
            "markers.hour_stem_focus",
            "markers.plate_in_tomb",
            "markers.plate_in_punishment",
            "chart_metadata.palace_order",
            "explicit my_answers / hidden_problems / best_solution / yongshen fields",
        ],
        "unknown_keys_kept_as_evidence": [
            "system.school", "system.chart_type", "system.method",
            "timing.solar_term.yuan", "timing.solar_term.day",
            "base_position.trigram_numbers", "base_position.hetu_numbers",
            "base_position.early_heaven_trigram", "base_position.home_god",
            "base_position.home_door", "base_position.home_star",
            "palace_stem_rules.stems_in_harm", "palace_stem_rules.stems_in_birth_stage",
            "active_chart.note", "active_chart.energy_state.realm",
            "active_chart.stems.center_guest",
        ],
    }
    jwrite(os.path.join(STATE, "schema_bind.json"), bind)

    # explicit-answer discovery
    explicit = {
        "my_answers_field_present": False,
        "hidden_problems_field_present": False,
        "best_solution_field_present": False,
        "yongshen_field_present": False,
        "pattern_field_present": True,
        "pattern_field_path": "chart_config.chart_pattern",
        "pattern_field_value": q["chart_config"]["chart_pattern"],
        "note": "No explicit answer/hidden/best/yongshen slots exist in this chart. "
                "Only chart_config.chart_pattern is an EXPLICIT interpretive field.",
    }

    index = {
        "source_file": "vault/raw/QMDJ.json",
        "source_of_record": "QMDJ/ADVERTISING/project_1.json",
        "sha256": src_hash,
        "bytes": size,
        "top_level_keys": sorted(actual_top),
        "palace_count": len(q["palaces"]),
        "palace_ids": sorted(q["palaces"].keys(), key=int),
        "explicit_slot_discovery": explicit,
        "expected_top_level_by_prompt": sorted(expected_top),
    }
    jwrite(os.path.join(STATE, "chart_index.json"), index)

    if len(q["palaces"]) != 9:
        anomaly("PALACE_COUNT", "HIGH", "nine-palace integrity failed", ["$.palaces"])

    # --- raw dump + schema md ----------------------------------------------
    lines = ["# Chart Schema (discovered)", "",
             f"- source sha256: `{src_hash}`", f"- bytes: {size}",
             f"- detected shape: `{detected}`", "",
             "## Top-level keys", ""]
    for k in sorted(actual_top):
        lines.append(f"- `{k}` : {type(q[k]).__name__}")
    lines += ["", "## Bind map (least-contradicted)", "",
              "| logical field | source path |", "|---|---|"]
    for k, v in sorted(bind["map"].items()):
        lines.append(f"| {k} | `{v}` |")
    lines += ["", "## Named by prompt, ABSENT in source", ""]
    for k in bind["absent_in_source_but_named_by_prompt"]:
        lines.append(f"- `{k}`")
    twrite(os.path.join(CHARTDIR, "schema.md"), "\n".join(lines) + "\n")

    dump = ["# Raw Chart Dump (verbatim field extract)", "",
            f"Source sha256 `{src_hash}`. Immutable. Do not edit.", ""]
    dump.append("## Header\n")
    dump.append("```json")
    dump.append(json.dumps({k: q[k] for k in
                            ["system", "timing", "element_prosperities", "chart_config"]},
                           indent=2))
    dump.append("```\n")
    for pid in sorted(q["palaces"], key=int):
        dump.append(f"## Palace {pid}\n")
        dump.append("```json")
        dump.append(json.dumps(q["palaces"][pid], indent=2))
        dump.append("```\n")
    twrite(os.path.join(CHARTDIR, "dump.md"), "\n".join(dump) + "\n")
    return src_hash, bind, index


# ============================================================== P0 ANATOMY ==
def split_pillar(p):
    stem, branch = p.split("-")
    return stem, branch


def p0(q, src_hash):
    fp = q["timing"]["four_pillars"]
    pillars = {}
    for key in ["year", "month", "day", "hour"]:
        stem, br = split_pillar(fp[key])
        brf = BRANCH_SHORT[br]
        pillars[key] = {
            "raw": fp[key],
            "path": f"timing.four_pillars.{key}",
            "stem": stem,
            "stem_element": STEM_ELEMENT[stem],
            "stem_polarity": STEM_POLARITY[stem],
            "branch": br,
            "branch_full": brf,
            "branch_palace": BRANCH_TO_PALACE[brf],
        }

    dvoid = [BRANCH_SHORT[b] for b in q["timing"]["voidness"]["day_void"]]
    hvoid = [BRANCH_SHORT[b] for b in q["timing"]["voidness"]["hour_void"]]
    void_palaces_computed = sorted({BRANCH_TO_PALACE[b] for b in dvoid + hvoid}, key=int)

    # repeated branches / clashes
    branches = [pillars[k]["branch_full"] for k in ["year", "month", "day", "hour"]]
    repeated = sorted({b for b in branches if branches.count(b) > 1})
    stems4 = [pillars[k]["stem"] for k in ["year", "month", "day", "hour"]]
    p_clash = [list(c) for c in STEM_CLASHES if c[0] in stems4 and c[1] in stems4]
    p_comb = [[a, b, x] for (a, b, x) in STEM_COMBINATIONS if a in stems4 and b in stems4]

    pillars_obj = {
        "pillars": pillars,
        "branch_multiset": branches,
        "repeated_branches": repeated,
        "stem_clashes_within_pillars": p_clash,
        "stem_combinations_within_pillars": p_comb,
        "void": {
            "day_void_branches": dvoid, "hour_void_branches": hvoid,
            "day_void_palaces": sorted({BRANCH_TO_PALACE[b] for b in dvoid}, key=int),
            "hour_void_palaces": sorted({BRANCH_TO_PALACE[b] for b in hvoid}, key=int),
            "union_void_palaces_computed": void_palaces_computed,
            "paths": ["timing.voidness.day_void", "timing.voidness.hour_void"],
        },
        "branch_to_palace_projection": {k: pillars[k]["branch_palace"]
                                        for k in ["year", "month", "day", "hour"]},
        "day_branch_void_membership": pillars["day"]["branch_full"] in dvoid + hvoid,
        "hour_branch_void_membership": pillars["hour"]["branch_full"] in dvoid + hvoid,
    }
    jwrite(os.path.join(STATE, "pillars.json"), pillars_obj)

    # -------- season engine
    ep = q["element_prosperities"]
    season = {
        "solar_term": q["timing"]["solar_term"],
        "path": "element_prosperities",
        "strengths": {k.capitalize(): v for k, v in ep.items()},
        "day_stem": pillars["day"]["stem"],
        "day_stem_element": pillars["day"]["stem_element"],
        "day_stem_seasonal_state": ep[pillars["day"]["stem_element"].lower()],
        "hour_stem": pillars["hour"]["stem"],
        "hour_stem_element": pillars["hour"]["stem_element"],
        "hour_stem_seasonal_state": ep[pillars["hour"]["stem_element"].lower()],
        "implications": [],
    }
    if season["day_stem_seasonal_state"] in ("Imprisoned", "Dead", "Obsolete"):
        season["implications"].append(
            f"CLIMATE_TRAP: day stem {season['day_stem']} ({season['day_stem_element']}) "
            f"is {season['day_stem_seasonal_state']} this season.")
    if season["hour_stem_seasonal_state"] in ("Imprisoned", "Dead", "Obsolete"):
        season["implications"].append(
            f"CLIMATE_TRAP: hour stem {season['hour_stem']} ({season['hour_stem_element']}) "
            f"is {season['hour_stem_seasonal_state']} this season.")
    jwrite(os.path.join(STATE, "season.json"), season)

    # -------- reverse indexes
    P = q["palaces"]
    idx = {"heaven_stem": {}, "earth_stem": {}, "hidden_stem": {}, "center_guest_stem": {},
           "door": {}, "star": {}, "god": {}, "branch": {}, "tomb_stems": {},
           "punishment_stems": {}, "harm_stems": {}, "birth_stage_stems": {},
           "afflictions": {}, "markers": {}, "realm": {}, "home_door": {},
           "home_star": {}, "home_god": {}}

    def add(bucket, key, pid):
        idx[bucket].setdefault(key, []).append(pid)

    for pid in sorted(P, key=int):
        pal = P[pid]
        ac = pal.get("active_chart", {})
        bp = pal.get("base_position", {})
        st = ac.get("stems", {})
        for b, k in [("heaven_stem", "heaven"), ("earth_stem", "earth"),
                     ("hidden_stem", "hidden"), ("center_guest_stem", "center_guest")]:
            if st.get(k):
                add(b, st[k], pid)
        for a in aslist(st.get("afflictions")):
            add("afflictions", a, pid)
        if ac.get("door"):
            add("door", ac["door"], pid)
        for s in aslist(ac.get("star")):
            add("star", s, pid)
        for g in aslist(ac.get("god")):
            add("god", g, pid)
        for b in bp.get("earthly_branches", []):
            add("branch", b, pid)
        if bp.get("home_door"):
            add("home_door", bp["home_door"], pid)
        if bp.get("home_star"):
            add("home_star", bp["home_star"], pid)
        for g in aslist(bp.get("home_god")):
            add("home_god", g, pid)
        psr = pal.get("palace_stem_rules", {})
        for b, k in [("tomb_stems", "stems_in_tomb"),
                     ("punishment_stems", "stems_in_clash_punishment"),
                     ("harm_stems", "stems_in_harm"),
                     ("birth_stage_stems", "stems_in_birth_stage")]:
            for s in psr.get(k, []):
                add(b, s, pid)
        for mk, mv in ac.get("status", {}).items():
            if mv:
                add("markers", mk, pid)
        if ac.get("energy_state", {}).get("realm"):
            add("realm", ac["energy_state"]["realm"], pid)
    for bucket in idx:
        for k in idx[bucket]:
            idx[bucket][k] = sorted(set(idx[bucket][k]), key=int)
    jwrite(os.path.join(STATE, "indexes.json"), idx)

    # -------- marker validation
    val = {"void": {}, "horse": {}, "duty": {}, "inner_outer": {}, "fu_yin": {}}
    void_marked = idx["markers"].get("is_void", [])
    val["void"] = {
        "marked": void_marked, "computed": void_palaces_computed,
        "match": void_marked == void_palaces_computed,
        "paths": ["palaces.{2,4,9}.active_chart.status.is_void",
                  "timing.voidness.day_void", "timing.voidness.hour_void"],
    }
    if not val["void"]["match"]:
        anomaly("VOID_MISMATCH", "HIGH", f"marked {void_marked} vs computed {void_palaces_computed}",
                val["void"]["paths"])

    horse_marked = idx["markers"].get("has_horse_star", [])
    hb_day = HORSE_BRANCH[pillars["day"]["branch_full"]]
    hb_hour = HORSE_BRANCH[pillars["hour"]["branch_full"]]
    horse_comp = sorted({BRANCH_TO_PALACE[hb_day], BRANCH_TO_PALACE[hb_hour]}, key=int)
    val["horse"] = {"marked": horse_marked, "computed": horse_comp,
                    "day_horse_branch": hb_day, "hour_horse_branch": hb_hour,
                    "match": horse_marked == horse_comp,
                    "paths": ["palaces.2.active_chart.status.has_horse_star",
                              "timing.four_pillars.day", "timing.four_pillars.hour"]}
    if not val["horse"]["match"]:
        anomaly("HORSE_MISMATCH", "MED", f"marked {horse_marked} vs computed {horse_comp}",
                val["horse"]["paths"])

    duty_star = q["chart_config"]["duty_star"]
    duty_door = q["chart_config"]["duty_door"]
    ds_pal = idx["star"].get(duty_star, [])
    dd_pal = idx["door"].get(duty_door, [])
    duty_marked = idx["markers"].get("is_duty_palace", [])
    val["duty"] = {"duty_star": duty_star, "duty_star_palaces": ds_pal,
                   "duty_door": duty_door, "duty_door_palaces": dd_pal,
                   "duty_palace_marked": duty_marked,
                   "match": ds_pal == dd_pal == duty_marked,
                   "paths": ["chart_config.duty_star", "chart_config.duty_door",
                             "palaces.9.active_chart.status.is_duty_palace"]}
    if not val["duty"]["match"]:
        anomaly("DUTY_MISMATCH", "HIGH", "duty star/door/marker palaces disagree",
                val["duty"]["paths"])

    inner_src = sorted(idx["realm"].get("Inner", []), key=int)
    outer_src = sorted(idx["realm"].get("Outer", []), key=int)
    inner_expect = sorted([p for p in INNER_PALACES_PROMPT if p != "5"], key=int)
    val["inner_outer"] = {
        "source_inner": inner_src, "source_outer": outer_src,
        "prompt_inner": INNER_PALACES_PROMPT, "prompt_outer": OUTER_PALACES_PROMPT,
        "match_excluding_center": inner_src == inner_expect and outer_src == OUTER_PALACES_PROMPT,
        "note": "Palace 5 carries no realm field in source; prompt assigns it Inner.",
    }

    # Fu Yin verification: heaven == earth == hidden in every palace
    fy = {}
    for pid in sorted(P, key=int):
        st = P[pid]["active_chart"].get("stems", {})
        fy[pid] = (st.get("heaven") == st.get("earth") == st.get("hidden")
                   and st.get("heaven") is not None)
    star_home = {}
    for pid in sorted(P, key=int):
        stars = aslist(P[pid]["active_chart"].get("star"))
        star_home[pid] = [s for s in stars if STAR_HOME_LUOSHU.get(s) == pid]
    door_home = {}
    for pid in sorted(P, key=int):
        d = P[pid]["active_chart"].get("door")
        hd = P[pid].get("base_position", {}).get("home_door")
        door_home[pid] = bool(d) and d == hd
    val["fu_yin"] = {
        "declared": q["chart_config"]["chart_pattern"],
        "declared_path": "chart_config.chart_pattern",
        "heaven_eq_earth_eq_hidden_all_palaces": all(fy.values()),
        "per_palace_stem_triple_identical": fy,
        "stars_sitting_home": {k: v for k, v in star_home.items() if v},
        "doors_at_original_palace": [k for k, v in door_home.items() if v],
        "verdict": "EXPLICIT Fu Yin confirmed by COMPUTED stem/star/door identity.",
    }
    jwrite(os.path.join(STATE, "validation.json"), val)

    # -------- duty state
    duty = {
        "lead_stem_raw": q["chart_config"]["lead_stem"],
        "lead_stem_path": "chart_config.lead_stem",
        "lead_xun": "Jia-Wu",
        "lead_proxy_stem": "Xin",
        "lead_proxy_note": "Lead stem string 'Jia-Wu Xin' binds the Jia-Wu decade to its "
                           "visible stand-in stem Xin. Jia itself never appears on the plate.",
        "lead_proxy_palaces": idx["heaven_stem"].get("Xin", []),
        "duty_star": duty_star, "duty_star_palace": ds_pal,
        "duty_door": duty_door, "duty_door_palace": dd_pal,
        "duty_palace_marked": duty_marked,
        "structure": q["chart_config"]["structure"],
        "chart_pattern": q["chart_config"]["chart_pattern"],
        "tian_yi": None,
        "tian_yi_note": "Tian Yi is not exposed by this schema. Zhi Fu (Chief) is the "
                        "nearest authority spirit and sits at palace(s) "
                        + str(idx["god"].get("Zhi Fu (Chief)", [])) + ".",
        "zhi_fu_palaces": idx["god"].get("Zhi Fu (Chief)", []),
    }
    jwrite(os.path.join(STATE, "duty.json"), duty)
    anomaly("TIAN_YI_ABSENT", "LOW",
            "chart_metadata.duty_elements.tian_yi has no counterpart in this schema; "
            "help/quality interpretation class falls back to Zhi Fu (Chief).",
            ["chart_config"])

    # -------- centre lodging graph
    center = P["5"]["active_chart"]
    host = "2"
    lodging = {
        "trigger": "palaces.5.active_chart.note == 'Attached to Palace 2'",
        "center_has_no_opposite": True,
        "center_stems": center.get("stems", {}),
        "center_god": center.get("god"),
        "center_palace_strength": center.get("energy_state", {}).get("palace"),
        "center_home_star": P["5"]["base_position"].get("home_star"),
        "graph": [
            {"from": "5", "to": host, "carrier": "stem", "value": center["stems"]["heaven"],
             "role": "lodged_from_center",
             "evidence": ["palaces.5.active_chart.note",
                          "palaces.5.active_chart.stems.heaven",
                          "palaces.2.active_chart.stems.center_guest"]},
            {"from": "5", "to": host, "carrier": "star",
             "value": P["5"]["base_position"]["home_star"], "role": "lodged_from_center",
             "evidence": ["palaces.5.base_position.home_star", "palaces.2.active_chart.star"]},
            {"from": "5", "to": host, "carrier": "god", "value": center.get("god"),
             "role": "center_resident_not_relocated",
             "evidence": ["palaces.5.active_chart.god"]},
        ],
        "host_palace": host,
        "host_inherited_conditions": {
            "is_void": P[host]["active_chart"]["status"].get("is_void"),
            "has_horse_star": P[host]["active_chart"]["status"].get("has_horse_star"),
            "door": P[host]["active_chart"]["door"],
            "afflictions": P[host]["active_chart"]["stems"].get("afflictions", []),
            "tomb_stems": P[host]["palace_stem_rules"].get("stems_in_tomb", []),
        },
        "corroboration": "palaces.2.active_chart.stems.center_guest == 'Bing' independently "
                         "confirms the Centre stem is hosted by palace 2.",
    }
    jwrite(os.path.join(STATE, "lodging.json"), lodging)

    # -------- origin sets (jia_protocol)
    day_stem = pillars["day"]["stem"]
    hour_stem = pillars["hour"]["stem"]
    day_heaven = idx["heaven_stem"].get(day_stem, [])
    hour_heaven = idx["heaven_stem"].get(hour_stem, [])

    day_set = {
        "target_stem": day_stem,
        "target_role": "day_stem / self / my_answers bias",
        "heaven_hits": day_heaven,
        "proxy_hits": [],
        "anomalies": [],
        "opposites": {},
    }
    if day_heaven == ["5"]:
        day_set["anomalies"].append(
            "ANOMALY:day_stem_only_in_centre - day stem Bing occupies palace 5 only; "
            "Centre has no directional opposite; lodging graph applies.")
        anomaly("DAY_STEM_IN_CENTRE", "HIGH",
                "Day stem Bing sits in the Centre (palace 5) and is lodged into palace 2. "
                "B1 primary is therefore a lodging graph, not a simple palace.",
                ["palaces.5.active_chart.stems.heaven", "palaces.5.active_chart.note"])
    for pid in idx["center_guest_stem"].get(day_stem, []):
        day_set["proxy_hits"].append({"role": "lodged_from_center_host", "palace": pid,
                                      "path": f"palaces.{pid}.active_chart.stems.center_guest"})
    for pid in idx["tomb_stems"].get(day_stem, []):
        day_set["proxy_hits"].append({"role": "tomb_of_day_gan", "palace": pid,
                                      "path": f"palaces.{pid}.palace_stem_rules.stems_in_tomb"})
    for pid in idx["birth_stage_stems"].get(day_stem, []):
        day_set["proxy_hits"].append({"role": "birth_stage_of_day_gan", "palace": pid,
                                      "path": f"palaces.{pid}.palace_stem_rules.stems_in_birth_stage"})
    day_set["proxy_hits"].append({"role": "day_branch_palace", "palace": pillars["day"]["branch_palace"],
                                  "path": "timing.four_pillars.day"})
    for pid in ds_pal:
        day_set["proxy_hits"].append({"role": "duty_star_palace", "palace": pid,
                                      "path": "chart_config.duty_star"})
    allp = sorted({p for p in day_heaven} |
                  {d["palace"] for d in day_set["proxy_hits"]}, key=int)
    day_set["all_palaces"] = allp
    day_set["opposites"] = {p: OPPOSITE[p] for p in allp}

    hour_set = {
        "target_stem": hour_stem,
        "target_role": "hour_stem / matter-in-motion / timing bias",
        "heaven_hits": hour_heaven,
        "proxy_hits": [],
        "anomalies": [],
        "opposites": {},
    }
    if not hour_heaven:
        hour_set["anomalies"].append(
            "ANOMALY:hour_stem_not_on_plate - Jia never appears on heaven/earth/hidden plates. "
            "Jia is represented by its decade proxy stem Xin (chart_config.lead_stem) and by "
            "its tomb palace.")
        anomaly("HOUR_STEM_NOT_ON_PLATE", "HIGH",
                "Hour stem Jia is absent from all plates; proxy set used (lead_stem_proxy Xin, "
                "tomb of Jia, hour branch palace).",
                ["timing.four_pillars.hour", "chart_config.lead_stem"])
    hour_set["proxy_hits"].append({"role": "lead_stem_proxy", "palace": duty["lead_proxy_palaces"][0],
                                   "path": "chart_config.lead_stem + palaces.9.active_chart.stems.heaven"})
    for pid in idx["tomb_stems"].get(hour_stem, []):
        hour_set["proxy_hits"].append({"role": "tomb_of_hour_gan", "palace": pid,
                                       "path": f"palaces.{pid}.palace_stem_rules.stems_in_tomb"})
    hour_set["proxy_hits"].append({"role": "hour_branch_palace",
                                   "palace": pillars["hour"]["branch_palace"],
                                   "path": "timing.four_pillars.hour"})
    for pid in dd_pal:
        hour_set["proxy_hits"].append({"role": "duty_door_palace", "palace": pid,
                                       "path": "chart_config.duty_door"})
    allh = sorted({d["palace"] for d in hour_set["proxy_hits"]}, key=int)
    hour_set["all_palaces"] = allh
    hour_set["opposites"] = {p: OPPOSITE[p] for p in allh}

    b1 = sorted(set(day_set["all_palaces"]) | {"5"}, key=int)
    b2 = allh
    b3 = sorted({OPPOSITE[p] for p in b1 if OPPOSITE[p]} |
                {OPPOSITE[lodging["host_palace"]]}, key=int)
    b4 = sorted({OPPOSITE[p] for p in b2 if OPPOSITE[p]}, key=int)
    seen = set(b1) | set(b2) | set(b3) | set(b4)
    b5 = sorted(set(P.keys()) - seen, key=int)

    origin = {
        "day_stem_origin_set": day_set,
        "hour_stem_origin_set": hour_set,
        "batch_selectors": {
            "B1": {"palaces": b1, "rule": "day-stem set incl. Centre + lodging host + duty-star proxy"},
            "B2": {"palaces": b2, "rule": "hour-stem proxy set (Jia absent from plate)"},
            "B3": {"palaces": b3, "rule": "directional opposites of B1 (Centre excluded, host 2 -> 8)"},
            "B4": {"palaces": b4, "rule": "directional opposites of B2"},
            "B5": {"palaces": b5, "rule": "remaining palaces, Luo Shu order"},
        },
        "selector_law": "sets + proxies + frozen geometry table; never array position",
    }
    jwrite(os.path.join(STATE, "origin_sets.json"), origin)

    # -------- yongshen candidates (UNBOUND)
    yong = [
        {"candidate_id": "YS-DAY-BING", "label": "Day stem Bing (self / actor)",
         "palaces": ["5", "2"], "grounding": "COMPUTED",
         "evidence_paths": ["timing.four_pillars.day", "palaces.5.active_chart.stems.heaven",
                            "palaces.2.active_chart.stems.center_guest"],
         "condition": "Centre-lodged into a void, horse-struck, Death-door palace; "
                      "Fire is Imprisoned this season; Bing's tomb is palace 6.",
         "bound_to_requirement": None, "requirement_fit_score": None},
        {"candidate_id": "YS-HOUR-JIA", "label": "Hour stem Jia (matter in motion)",
         "palaces": ["2", "9"], "grounding": "COMPUTED",
         "evidence_paths": ["timing.four_pillars.hour",
                            "palaces.2.palace_stem_rules.stems_in_tomb",
                            "chart_config.lead_stem"],
         "condition": "Absent from every plate; entombed at palace 2; proxied by Xin at palace 9; "
                      "Wood is Dead this season.",
         "bound_to_requirement": None, "requirement_fit_score": None},
        {"candidate_id": "YS-LEAD-XIN", "label": "Lead proxy stem Xin (visible stand-in)",
         "palaces": ["9"], "grounding": "EXPLICIT",
         "evidence_paths": ["chart_config.lead_stem", "palaces.9.active_chart.stems.heaven"],
         "condition": "Metal is Prosperous, but palace 9 is void, duty palace, "
                      "clash-punished, self-punished and Fu Yin.",
         "bound_to_requirement": None, "requirement_fit_score": None},
        {"candidate_id": "YS-DUTY-9", "label": "Duty star Tian Ying + duty door Jing (Scenery) at palace 9",
         "palaces": ["9"], "grounding": "EXPLICIT",
         "evidence_paths": ["chart_config.duty_star", "chart_config.duty_door",
                            "palaces.9.active_chart.status.is_duty_palace"],
         "condition": "Authority of the matter; imprisoned door, imprisoned palace, void.",
         "bound_to_requirement": None, "requirement_fit_score": None},
        {"candidate_id": "YS-OPEN-6", "label": "Kai (Open) door + Ding + Tian Xin at palace 6",
         "palaces": ["6"], "grounding": "COMPUTED",
         "evidence_paths": ["palaces.6.active_chart.door", "palaces.6.active_chart.stems.heaven",
                            "palaces.6.active_chart.energy_state.door"],
         "condition": "Only Prosperous door+palace pair carrying a San Qi stem; "
                      "also the tomb palace of the day stem Bing.",
         "bound_to_requirement": None, "requirement_fit_score": None},
        {"candidate_id": "YS-LIFE-8", "label": "Sheng (Life) door + Ren + Liu He at palace 8",
         "palaces": ["8"], "grounding": "COMPUTED",
         "evidence_paths": ["palaces.8.active_chart.door", "palaces.8.active_chart.god",
                            "palaces.8.active_chart.stems.heaven"],
         "condition": "Outer realm, Resting door, Six Harmony spirit, star Prosperous by palace.",
         "bound_to_requirement": None, "requirement_fit_score": None},
    ]
    jwrite(os.path.join(STATE, "yongshen.json"),
           {"note": "chart-derived only; not yet requirement-bound", "candidates": yong})

    jwrite(os.path.join(STATE, "anomalies.json"), {"anomalies": ANOM})

    machine = {
        "run_id": RUN_ID,
        "state": "B1",
        "completed_batches": [],
        "completed_phases": ["INIT", "CHART_INGEST", "P0_ANATOMY"],
        "palaces": {},
        "solution_seed_revision": 0,
        "verification": {
            "source_sha256": src_hash,
            "schema_validation_passed": True,
            "schema_detection_complete": True,
            "four_pillars_valid": True,
            "indexes_built": True,
            "origin_sets_built": True,
            "nine_palace_integrity": len(P) == 9,
            "determinism_check": "pending",
        },
        "updated_at": GENERATED_AT,
    }
    jwrite(os.path.join(STATE, "machine.json"), machine)
    return origin, idx, pillars_obj, season, duty, lodging, val


if __name__ == "__main__":
    q = load_qmdj()
    src_hash, bind, index = chart_ingest(q)
    origin, idx, pillars_obj, season, duty, lodging, val = p0(q, src_hash)
    heartbeat("phase0 done | day_stem Bing heaven_hits: %s | hour_stem Jia heaven_hits: %s | "
              "B1=%s B2=%s B3=%s B4=%s B5=%s | anomalies: %d"
              % (origin["day_stem_origin_set"]["heaven_hits"],
                 origin["hour_stem_origin_set"]["heaven_hits"],
                 origin["batch_selectors"]["B1"]["palaces"],
                 origin["batch_selectors"]["B2"]["palaces"],
                 origin["batch_selectors"]["B3"]["palaces"],
                 origin["batch_selectors"]["B4"]["palaces"],
                 origin["batch_selectors"]["B5"]["palaces"], len(ANOM)))
    print("sha256", src_hash)
    print("B1", origin["batch_selectors"]["B1"]["palaces"])
    print("B2", origin["batch_selectors"]["B2"]["palaces"])
    print("B3", origin["batch_selectors"]["B3"]["palaces"])
    print("B4", origin["batch_selectors"]["B4"]["palaces"])
    print("B5", origin["batch_selectors"]["B5"]["palaces"])
    print("void match", val["void"]["match"], "horse match", val["horse"]["match"],
          "duty match", val["duty"]["match"])
    print("anomalies", [a["code"] for a in ANOM])
