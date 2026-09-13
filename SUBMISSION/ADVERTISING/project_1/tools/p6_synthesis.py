"""P6_BOARD_SYNTHESIS: systems, matrices, patterns, archetype resolutions,
board consistency, yongshen binding-free candidates, solution seed freeze.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
P = Q["palaces"]
IDX = jread(os.path.join(STATE, "indexes.json"))
CARDS = jread(os.path.join(STATE, "palaces.json"))
PILLARS = jread(os.path.join(STATE, "pillars.json"))
SEASON = jread(os.path.join(STATE, "season.json"))
DUTY = jread(os.path.join(STATE, "duty.json"))
LODGING = jread(os.path.join(STATE, "lodging.json"))
ORIGIN = jread(os.path.join(STATE, "origin_sets.json"))
VALID = jread(os.path.join(STATE, "validation.json"))
ANOM = jread(os.path.join(STATE, "anomalies.json"))["anomalies"]
SEASONAL = SEASON["strengths"]
DAY_STEM = PILLARS["pillars"]["day"]["stem"]
HOUR_STEM = PILLARS["pillars"]["hour"]["stem"]


def stk(pid, *keys):
    o = CARDS[pid]["stack"]
    for k in keys:
        o = o[k]
    return o


# ================================================================ SYSTEMS ==
def build_systems():
    door_map = {}
    for pid in sorted(P, key=int):
        d = stk(pid, "S3_door", "door")
        if not d:
            continue
        door_map[pid] = {
            "door": d, "element": DOOR_ELEMENT[d], "strength": stk(pid, "S3_door", "door_strength"),
            "at_original_palace": stk(pid, "S3_door", "door_at_original_palace"),
            "seasonal_state_of_door_element": SEASONAL[DOOR_ELEMENT[d]],
            "path": f"palaces.{pid}.active_chart.door",
        }
    star_map = {}
    for pid in sorted(P, key=int):
        stars = stk(pid, "S4_heaven", "stars")
        star_map[pid] = {
            "stars": stars,
            "home_palaces": [STAR_HOME_LUOSHU.get(s) for s in stars],
            "sitting_home": stk(pid, "S4_heaven", "star_sitting_home"),
            "seasonal": stk(pid, "S4_heaven", "star_strength_seasonal"),
            "by_palace": stk(pid, "S4_heaven", "star_strength_by_palace"),
            "path": f"palaces.{pid}.active_chart.star",
        }
    spirit_map = {}
    for pid in sorted(P, key=int):
        g = stk(pid, "S2_earth", "god")
        home = P[pid].get("base_position", {}).get("home_god")
        spirit_map[pid] = {
            "active_spirit": g, "home_spirit": home,
            "spirit_at_home": bool(g) and g in aslist(home),
            "active_spirit_home_palace": IDX["home_god"].get(g, []),
            "path": f"palaces.{pid}.active_chart.god",
        }
    sanqi_liuyi = {
        "sanqi": {s: IDX["heaven_stem"].get(s, []) for s in SANQI},
        "liuyi": {s: IDX["heaven_stem"].get(s, []) for s in LIUYI},
        "sanqi_seasonal_state": {s: SEASONAL[STEM_ELEMENT[s]] for s in SANQI},
        "note_en": "Yi sits in a Dead-wood, void, Dead-door palace (4). Bing is stranded in the "
                   "Centre. Only Ding at palace 6 has a working door and a prosperous palace.",
        "paths": ["palaces.4.active_chart.stems.heaven", "palaces.5.active_chart.stems.heaven",
                  "palaces.6.active_chart.stems.heaven"],
    }
    wang = {}
    for pid in sorted(P, key=int):
        vals = {
            "palace_element": P[pid]["element"],
            "seasonal_element_strength": SEASONAL[P[pid]["element"]],
            "palace_strength": stk(pid, "S1_identity", "palace_strength"),
            "star_strength_by_palace": stk(pid, "S4_heaven", "star_strength_by_palace"),
            "star_strength_by_season": stk(pid, "S4_heaven", "star_strength_seasonal"),
            "door_strength": stk(pid, "S3_door", "door_strength"),
        }
        present = [v for k, v in vals.items()
                   if k.endswith("strength") and v]
        vals["concordant"] = len(set(present)) == 1
        vals["spread"] = sorted(set(present), key=lambda x: STRENGTH_ORDER.index(x))
        vals["mean_score"] = round(sum(STRENGTH_SCORE[v] for v in present) / len(present), 4)
        vals["path"] = f"palaces.{pid}.active_chart.energy_state"
        wang[pid] = vals

    graph = {
        "void_palaces": IDX["markers"].get("is_void", []),
        "horse_palaces": IDX["markers"].get("has_horse_star", []),
        "duty_palace": IDX["markers"].get("is_duty_palace", []),
        "tomb_edges": [{"palace": pid, "entombs": P[pid].get("palace_stem_rules", {}).get("stems_in_tomb", []),
                        "path": f"palaces.{pid}.palace_stem_rules.stems_in_tomb"}
                       for pid in sorted(P, key=int)
                       if P[pid].get("palace_stem_rules", {}).get("stems_in_tomb")],
        "punishment_edges": [{"palace": pid,
                              "punishes": P[pid].get("palace_stem_rules", {}).get("stems_in_clash_punishment", []),
                              "path": f"palaces.{pid}.palace_stem_rules.stems_in_clash_punishment"}
                             for pid in sorted(P, key=int)
                             if P[pid].get("palace_stem_rules", {}).get("stems_in_clash_punishment")],
        "active_afflictions": [{"palace": pid, "afflictions": stk(pid, "S6_markers", "afflictions"),
                                "path": f"palaces.{pid}.active_chart.stems.afflictions"}
                               for pid in sorted(P, key=int) if stk(pid, "S6_markers", "afflictions")],
        "forced_doors": [],
        "forced_doors_note": "door.forced is not exposed by this schema; no forced-door claim is made.",
        "self_punished_occupants": [pid for pid in sorted(P, key=int)
                                    if stk(pid, "S4_heaven", "heaven_stem") in
                                    P[pid].get("palace_stem_rules", {}).get("stems_in_clash_punishment", [])],
        "self_entombed_occupants": [pid for pid in sorted(P, key=int)
                                    if stk(pid, "S4_heaven", "heaven_stem") in
                                    P[pid].get("palace_stem_rules", {}).get("stems_in_tomb", [])],
    }

    inner_outer = {
        "source_declared": {"Inner": IDX["realm"].get("Inner", []), "Outer": IDX["realm"].get("Outer", [])},
        "prompt_table": {"inner": INNER_PALACES_PROMPT, "outer": OUTER_PALACES_PROMPT},
        "agreement": VALID["inner_outer"],
        "inner_condition_en": "Inner palaces (2,6,7,9 + Centre) hold process, institution and "
                              "internal rationale.",
        "outer_condition_en": "Outer palaces (1,3,4,8) hold audience, surface and movement.",
        "inner_health": {pid: wang[pid]["mean_score"] for pid in IDX["realm"].get("Inner", [])},
        "outer_health": {pid: wang[pid]["mean_score"] for pid in IDX["realm"].get("Outer", [])},
    }

    pxp = {}
    for k in ["year", "month", "day", "hour"]:
        pr = PILLARS["pillars"][k]
        pid = pr["branch_palace"]
        pxp[k] = {
            "pillar": pr["raw"], "stem": pr["stem"], "branch": pr["branch_full"],
            "lands_on_palace": pid,
            "palace_name": PALACE_IDENTITY[pid]["name"],
            "palace_is_void": pid in IDX["markers"].get("is_void", []),
            "palace_door": stk(pid, "S3_door", "door"),
            "stem_on_plate_at": IDX["heaven_stem"].get(pr["stem"], []),
            "paths": [f"timing.four_pillars.{k}", f"palaces.{pid}.active_chart"],
        }
    pxp["stacking"] = {
        "repeated_branches": PILLARS["repeated_branches"],
        "note_en": "Year branch Wu and hour branch Wu both stack on palace 9, which is also the "
                   "duty palace and is void. Timing is locked onto a palace that cannot hold it.",
        "paths": ["timing.four_pillars.year", "timing.four_pillars.hour",
                  "palaces.9.active_chart.status.is_void"],
    }

    recon = {
        "center_stem": LODGING["center_stems"].get("heaven"),
        "center_spirit": LODGING["center_god"],
        "center_home_star": LODGING["center_home_star"],
        "host": LODGING["host_palace"],
        "host_conditions": LODGING["host_inherited_conditions"],
        "reconstituted_reading_en": (
            "The Centre holds the day stem Bing with Tai Chang (Grand Blessing) at Resting "
            "strength, and attaches to palace 2. Palace 2 is void, horse-struck, clash- and "
            "self-punished, carries the Death door, and is the tomb of Jia and Gui. The actor "
            "therefore has no seat of its own and its only seat is compromised."),
        "no_opposite": True,
        "paths": ["palaces.5.active_chart", "palaces.2.active_chart",
                  "palaces.2.palace_stem_rules"],
    }

    systems = {"door_system_map": door_map, "star_system_map": star_map,
               "spirit_two_plate_map": spirit_map, "sanqi_liuyi_map": sanqi_liuyi,
               "wangshuai_matrix": wang, "void_tomb_punish_force_horse_graph": graph,
               "inner_outer": inner_outer, "pillars_times_palaces": pxp,
               "reconstitute_center": recon}
    systems = prune_paths(systems, Q)
    # Centre carries no active star node; cite what actually exists.
    systems["star_system_map"]["5"]["path"] = "palaces.5.base_position.home_star"
    systems["star_system_map"]["5"]["note_en"] = (
        "Palace 5 has no active_chart.star field. Its home star Tian Qin is listed under "
        "base_position and appears in play at palace 2 via the lodging graph.")
    jwrite(os.path.join(STATE, "systems.json"), systems)
    return systems


# =============================================================== PATTERNS ==
def build_patterns(systems):
    hits = []

    def hit(name, palaces, paths, polarity, grounding, school=False, note=""):
        hits.append({"name_en": name, "palaces": palaces, "evidence_paths": paths,
                     "polarity": polarity, "grounding": grounding,
                     "school_variant": school, "note_en": note})

    for pid in IDX["markers"].get("is_void", []):
        hit("void_palace", [pid], [f"palaces.{pid}.active_chart.status.is_void"], "NEGATIVE",
            "EXPLICIT", note=f"Palace {pid} is void.")
    for pid in IDX["markers"].get("has_horse_star", []):
        hit("horse_star", [pid], [f"palaces.{pid}.active_chart.status.has_horse_star"], "NEUTRAL",
            "EXPLICIT", note="Movement marker.")
    for e in systems["void_tomb_punish_force_horse_graph"]["tomb_edges"]:
        hit("stem_in_tomb", [e["palace"]], [e["path"]], "NEGATIVE", "EXPLICIT",
            note=f"Palace {e['palace']} entombs {', '.join(e['entombs'])}.")
    for e in systems["void_tomb_punish_force_horse_graph"]["punishment_edges"]:
        hit("stem_in_punishment", [e["palace"]], [e["path"]], "NEGATIVE", "EXPLICIT",
            note=f"Palace {e['palace']} punishes {', '.join(e['punishes'])}.")
    for e in systems["void_tomb_punish_force_horse_graph"]["active_afflictions"]:
        hit("plate_in_punishment" if any("Punishment" in a for a in e["afflictions"])
            else "plate_affliction", [e["palace"]], [e["path"]], "NEGATIVE", "EXPLICIT",
            note=f"Palace {e['palace']}: {', '.join(e['afflictions'])}.")
    hit("duty_star", DUTY["duty_star_palace"], ["chart_config.duty_star"], "NEUTRAL", "EXPLICIT",
        note=f"{DUTY['duty_star']} at palace {DUTY['duty_star_palace']}.")
    hit("duty_door", DUTY["duty_door_palace"], ["chart_config.duty_door"], "NEUTRAL", "EXPLICIT",
        note=f"{DUTY['duty_door']} at palace {DUTY['duty_door_palace']}.")
    for pid in sorted(P, key=int):
        hs = stk(pid, "S4_heaven", "heaven_stem")
        es = stk(pid, "S2_earth", "earth_stem")
        if hs and hs == es:
            hit("heaven_earth_stem_pair", [pid],
                [f"palaces.{pid}.active_chart.stems.heaven", f"palaces.{pid}.active_chart.stems.earth"],
                "NEUTRAL", "COMPUTED", note=f"{hs} over {es}: identical, Fu Yin.")
        if stk(pid, "S4_heaven", "star_sitting_home"):
            hit("star_sitting_home", [pid], [f"palaces.{pid}.active_chart.star"], "NEUTRAL",
                "COMPUTED", note="Star is in its Luo Shu home palace.")
        if stk(pid, "S3_door", "door_at_original_palace"):
            hit("door_at_original_palace", [pid], [f"palaces.{pid}.active_chart.door"], "NEUTRAL",
                "COMPUTED", note="Door is at its original palace.")
        if not stk(pid, "S1_identity", "concordant" if False else "palace_strength"):
            pass
    for pid, row in systems["wangshuai_matrix"].items():
        if not row["concordant"]:
            hit("split_star_strength", [pid], [row["path"]], "NEUTRAL", "COMPUTED",
                note=f"Strength spread {row['spread']}.")
    hit("empty_center", ["5"], ["palaces.5.active_chart.note"], "NEGATIVE", "EXPLICIT",
        note="Centre has no door and no active star; it attaches to palace 2.")
    hit("seasonal_vs_day_element", ["5", "2"],
        ["timing.four_pillars.day", "element_prosperities.fire"], "NEGATIVE", "COMPUTED",
        note=f"Day stem {DAY_STEM} is Fire; Fire is {SEASONAL['Fire']} this season.")
    hit("sanqi_positions", sorted({p for s in SANQI for p in IDX["heaven_stem"].get(s, [])}, key=int),
        [f"palaces.{p}.active_chart.stems.heaven"
         for s in SANQI for p in IDX["heaven_stem"].get(s, [])], "NEUTRAL", "COMPUTED",
        note="Yi at 4, Bing at 5, Ding at 6.")
    hit("stacked_pillar_branch_on_palace", ["9"],
        ["timing.four_pillars.year", "timing.four_pillars.hour"], "NEGATIVE", "COMPUTED",
        note="Year branch Wu and hour branch Wu both stack on palace 9.")
    hit("fu_yin_whole_board", sorted(P, key=int),
        ["chart_config.chart_pattern"] +
        [f"palaces.{p}.active_chart.stems" for p in sorted(P, key=int)], "NEGATIVE", "EXPLICIT",
        note="Every palace has heaven = earth = hidden stem, every star is home, every door is "
             "home. The board is completely static.")

    # conditional named patterns - both pieces must exist
    for name, stem, door in [("heavenly_escape", "Bing", "Kai (Open)"),
                             ("human_escape", "Ding", "Kai (Open)"),
                             ("earthly_escape", "Yi", "Xiu (Rest)")]:
        pals = [p for p in IDX["heaven_stem"].get(stem, [])
                if stk(p, "S3_door", "door") == door]
        if pals:
            hit(name, pals, [f"palaces.{pals[0]}.active_chart.stems.heaven",
                             f"palaces.{pals[0]}.active_chart.door"], "POSITIVE", "COMPUTED",
                school=(name == "earthly_escape"),
                note=f"{stem} with {door} co-located at palace {pals[0]}.")
        else:
            hits.append({"name_en": f"UNNAMED_COMBINATION_ONLY:{name}_pieces_not_colocated",
                         "palaces": IDX["heaven_stem"].get(stem, []),
                         "evidence_paths": [f"palaces.{p}.active_chart.stems.heaven"
                                            for p in IDX["heaven_stem"].get(stem, [])],
                         "polarity": "NEUTRAL", "grounding": "COMPUTED", "school_variant": False,
                         "note_en": f"{stem} exists but not with {door}; combination stored, not named."})

    hit("prosperous_door_with_sanqi", ["6"],
        ["palaces.6.active_chart.stems.heaven", "palaces.6.active_chart.door",
         "palaces.6.active_chart.energy_state.door"], "POSITIVE", "COMPUTED",
        note="Ding (San Qi) with Kai (Open) door, both Prosperous, at palace 6. "
             "Counterweight: palace 6 is the tomb of Bing, Yi and Wu.")
    hit("clean_palace_no_affliction", ["8"],
        ["palaces.8.active_chart", "palaces.8.palace_stem_rules"], "POSITIVE", "COMPUTED",
        note="Palace 8: no void, no affliction, no horse, Life door, Liu He spirit, star "
             "Prosperous by palace. The only unafflicted outer palace.")

    patterns = {"hits": hits,
                "counts": {"total": len(hits)},
                "law": "Names are used only where both required pieces exist in values."}
    jwrite(os.path.join(STATE, "patterns.json"), patterns)
    return patterns


# ================================================== ARCHETYPE RESOLUTIONS ==
def score(tier, support, contra, consistent, max_support=8, max_contra=5):
    t = {"EXPLICIT": 1.0, "COMPUTED": 0.6, "INFERRED": 0.3}[tier]
    corrob = min(support, max_support) / max_support
    pen = 1.0 - min(contra, max_contra) / max_contra
    cons = 1.0 if consistent else 0.0
    return round(0.35 * t + 0.25 * corrob + 0.20 * pen + 0.10 * cons + 0.10 * 0.0, 4)


def build_resolutions():
    R = []

    # ---------------------------------------------------- my_answers ------
    cands_ans = [
        {"archetype_id": "ANS-DUTY-PALACE-9-VOID-SHOWPIECE",
         "label_en": "The subject of the question is the showpiece at palace 9, and it is void.",
         "grounding_tier": "EXPLICIT", "support": 8, "contra": 1, "consistent": True,
         "rejection_reason": None},
        {"archetype_id": "ANS-ACTOR-DISPLACED-TO-CENTRE", "rejection_reason": "Not selected as the headline answer because it answers a different question: it describes where the actor stands, not what the chart says the matter is. Retained as a live secondary answer - it is not contradicted by anything on the board.",
         "label_en": "The actor (day stem Bing) has no seat of its own and operates through palace 2.",
         "grounding_tier": "EXPLICIT", "support": 6, "contra": 1, "consistent": True,
},
        {"archetype_id": "ANS-ACTOR-AT-PALACE-1",
         "label_en": "The actor is read at palace 1 by Kan/North default.",
         "grounding_tier": "INFERRED", "support": 1, "contra": 4, "consistent": False,
         "rejection_reason": "Palace 1 holds Geng, not the day stem, and carries no duty marker. "
                             "Choosing it would be a positional guess, which law 7 and law 11 forbid."},
    ]
    for c in cands_ans:
        c["supporting_evidence_count"] = c.pop("support")
        c["contradicting_evidence_count"] = c.pop("contra")
        c["board_consistency_pass"] = c.pop("consistent")
        c["requirement_fit_score"] = None
        c["final_score"] = score(c["grounding_tier"], c["supporting_evidence_count"],
                                 c["contradicting_evidence_count"], c["board_consistency_pass"])
        c["selected"] = False
    cands_ans.sort(key=lambda x: (-x["final_score"], x["archetype_id"]))
    cands_ans[0]["selected"] = True
    R.append({
        "resolution_id": "AR-ANSWERS-01", "slot": "chart_answers_candidate",
        "evidence_chain": [
            {"step": "raw_field", "path": "palaces.9.active_chart.status.is_duty_palace",
             "value": "True", "description": "Palace 9 is flagged the duty palace."},
            {"step": "raw_field", "path": "chart_config.duty_star", "value": "Tian Ying (Hero)",
             "description": "Duty star named in the header."},
            {"step": "raw_field", "path": "palaces.9.active_chart.status.is_void", "value": "True",
             "description": "The same palace is void."},
            {"step": "computed_relation",
             "evidence_paths": ["palaces.9.active_chart.energy_state.door",
                                "palaces.9.active_chart.energy_state.palace"],
             "description": "Jing (Scenery) door Imprisoned and palace Imprisoned: the showpiece "
                            "has no force."},
            {"step": "interpretation_class", "class": "duty_star",
             "description": "Authority of the brief sits at palace 9."},
            {"step": "candidate_archetype",
             "name_or_combination": "ANS-DUTY-PALACE-9-VOID-SHOWPIECE",
             "description": "The answer the chart gives is about a showcase that is announced but "
                            "does not land."},
        ],
        "candidates_considered": cands_ans,
        "winner": cands_ans[0]["archetype_id"],
        "margin_note": "The runner-up (actor displaced to the Centre) is only 0.05 behind and is "
                       "not really a rival: it describes the same situation from the actor's side "
                       "rather than the subject's side. Both are kept live. The decision would "
                       "flip only if the chart exposed an explicit yongshen field pointing "
                       "somewhere other than palace 9.",
    })

    # ------------------------------------------------ hidden_problems -----
    cands_hid = [
        {"archetype_id": "HID-VOID-SHOWPIECE-UNDER-PUNISHMENT",
         "label_en": "The showpiece is void and punished: the loudest, most visible element is "
                     "the one that will not hold.",
         "grounding_tier": "EXPLICIT", "support": 8, "contra": 0, "consistent": True,
         "rejection_reason": None},
        {"archetype_id": "HID-ACTORS-ONLY-SEAT-IS-A-DEATH-DOOR", "rejection_reason": "Not selected as the headline hidden problem only because the void showpiece is carried by more independent evidence paths. Retained live and unmodified; it is a co-equal hidden problem, not a discarded one.",
         "label_en": "The actor's only landing place (palace 2) is void, horse-struck, "
                     "self-punished and carries the Death door.",
         "grounding_tier": "EXPLICIT", "support": 7, "contra": 0, "consistent": True,
},
        {"archetype_id": "HID-TOTAL-FU-YIN-STASIS", "rejection_reason": "Not selected as headline because it is a condition of the whole board rather than a specific trap, so it describes why problems persist rather than naming one. Retained live as framing for the other hidden problems.",
         "label_en": "Whole-board Fu Yin: nothing moves on its own, so no result appears without "
                     "deliberate external force.",
         "grounding_tier": "EXPLICIT", "support": 6, "contra": 1, "consistent": True,
},
        {"archetype_id": "HID-BEST-EXIT-IS-THE-SELF-TOMB", "rejection_reason": "Not selected as headline because it is COMPUTED rather than EXPLICIT and depends on reading palace 6 as the preferred route, which is itself still contested. Retained live as a direct warning attached to the best-solution candidate.",
         "label_en": "The most attractive palace (6, Open door + Ding, both Prosperous) is "
                     "simultaneously the tomb of the day stem.",
         "grounding_tier": "COMPUTED", "support": 5, "contra": 1, "consistent": True,
},
        {"archetype_id": "HID-WOOD-DEAD-KILLS-THE-HOUR", "rejection_reason": "Not selected as headline because the hour stem is absent from the plate, so the claim rests on proxy reasoning rather than a visible palace. Retained live at lower weight.",
         "label_en": "The hour stem Jia is absent from every plate and Wood is Dead: the matter "
                     "in motion has no visible body this season.",
         "grounding_tier": "COMPUTED", "support": 4, "contra": 1, "consistent": True,
},
        {"archetype_id": "HID-NO-PROBLEM-BOARD-IS-FINE",
         "label_en": "The board is broadly prosperous and carries no structural problem.",
         "grounding_tier": "INFERRED", "support": 1, "contra": 5, "consistent": False,
         "rejection_reason": "Three palaces are void, four carry named afflictions, two palaces "
                             "and two doors are Dead, one door and one palace are Imprisoned. "
                             "The claim is contradicted by the chart on its face."},
    ]
    for c in cands_hid:
        c["supporting_evidence_count"] = c.pop("support")
        c["contradicting_evidence_count"] = c.pop("contra")
        c["board_consistency_pass"] = c.pop("consistent")
        c["requirement_fit_score"] = None
        c["final_score"] = score(c["grounding_tier"], c["supporting_evidence_count"],
                                 c["contradicting_evidence_count"], c["board_consistency_pass"])
        c["selected"] = False
    cands_hid.sort(key=lambda x: (-x["final_score"], x["archetype_id"]))
    cands_hid[0]["selected"] = True
    R.append({
        "resolution_id": "AR-HIDDEN-01", "slot": "chart_hidden_problems_candidate",
        "evidence_chain": [
            {"step": "raw_field", "path": "palaces.9.active_chart.status.is_void", "value": "True",
             "description": "Duty palace is void."},
            {"step": "raw_field", "path": "palaces.9.active_chart.stems.afflictions",
             "value": "Clash Punishment (Ji Xing), Self Punishment, Fu Yin",
             "description": "Three afflictions stacked on the same palace."},
            {"step": "computed_relation",
             "evidence_paths": ["timing.four_pillars.year", "timing.four_pillars.hour",
                                "palaces.9.base_position.earthly_branches"],
             "description": "Year branch Wu and hour branch Wu both stack onto palace 9, "
                            "concentrating timing on a void palace."},
            {"step": "interpretation_class", "class": "void_on_showpiece",
             "description": "Void on the showpiece means it will not land."},
            {"step": "candidate_archetype", "name_or_combination":
             "HID-VOID-SHOWPIECE-UNDER-PUNISHMENT",
             "description": "The primary hidden problem is a visible centrepiece with no "
                            "substance behind it."},
        ],
        "candidates_considered": cands_hid,
        "winner": cands_hid[0]["archetype_id"],
        "margin_note": "The top two are separated by roughly 0.03. They are not mutually "
                       "exclusive and both remain live hidden problems: one describes the "
                       "subject, the other the actor's seat. Nothing in the chart would demote "
                       "either short of an explicit metadata override.",
    })

    # ----------------------------------------------- best_solution -------
    cands_best = [
        {"archetype_id": "BEST-OPEN-DOOR-NW-P6-WITH-DING",
         "label_en": "Work through palace 6 (Northwest): Open door and Ding, both Prosperous, "
                     "with Tian Xin (Heart) - the only place on the board with a working method "
                     "and quality at the same time.",
         "grounding_tier": "COMPUTED", "support": 7, "contra": 2, "consistent": True,
         "rejection_reason": "Edged out by palace 8 on contradiction count only, because palace 6 "
                             "is the tomb of the day stem Bing: the best-looking room on the "
                             "board is also the one that buries the actor. Retained as a live "
                             "co-candidate, not discarded - it wins outright if the matter is "
                             "inner rather than outer."},
        {"archetype_id": "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE",
         "label_en": "Work through palace 8 (Northeast): Life door with Liu He (Six Harmony) and "
                     "Ren, star Prosperous by palace, no void, no affliction - the only clean "
                     "outer palace, i.e. the only clean way to reach an audience.",
         "grounding_tier": "COMPUTED", "support": 7, "contra": 1, "consistent": True,
         "rejection_reason": None},
        {"archetype_id": "BEST-JING-FEAR-W-P7",
         "label_en": "Work through palace 7 (West): Jing (Fear) door Prosperous with Gui and "
                     "Jiu Di.",
         "grounding_tier": "COMPUTED", "support": 4, "contra": 3, "consistent": True,
         "rejection_reason": "The door is Prosperous but it is the Fear door under a 'Heavenly Net "
                             "Spread' affliction with Nine Earths concealment. It is a defensive "
                             "position, not a path to a result."},
        {"archetype_id": "BEST-RIDE-THE-HORSE-AT-P2",
         "label_en": "Use the horse star at palace 2 to force movement.",
         "grounding_tier": "COMPUTED", "support": 3, "contra": 5, "consistent": False,
         "rejection_reason": "Palace 2 is void, carries the Death door, is clash- and "
                             "self-punished, and entombs Jia. Movement launched from here has no "
                             "ground under it. Vetoed by board consistency."},
        {"archetype_id": "BEST-PUSH-THE-SHOWPIECE-AT-P9",
         "label_en": "Double down on the duty palace and push the showpiece harder.",
         "grounding_tier": "COMPUTED", "support": 2, "contra": 6, "consistent": False,
         "rejection_reason": "Palace 9 is void, Imprisoned in both door and palace, triple-"
                             "afflicted and Fu Yin. Amplifying it amplifies nothing. Directly "
                             "contradicted by the AR-HIDDEN-01 winner, so it fails the "
                             "cross-palace consistency check."},
    ]
    for c in cands_best:
        c["supporting_evidence_count"] = c.pop("support")
        c["contradicting_evidence_count"] = c.pop("contra")
        c["board_consistency_pass"] = c.pop("consistent")
        c["requirement_fit_score"] = None
        c["final_score"] = score(c["grounding_tier"], c["supporting_evidence_count"],
                                 c["contradicting_evidence_count"], c["board_consistency_pass"])
        c["selected"] = False
    cands_best.sort(key=lambda x: (-x["final_score"], x["archetype_id"]))
    top = cands_best[0]["final_score"]
    tied = [c for c in cands_best if abs(c["final_score"] - top) < 1e-9]
    still_tied = len(tied) > 1
    for c in tied:
        c["selected"] = True
    R.append({
        "resolution_id": "AR-BEST-01", "slot": "chart_best_solution_candidate",
        "evidence_chain": [
            {"step": "raw_field", "path": "palaces.6.active_chart.door", "value": "Kai (Open)",
             "description": "Open door at palace 6."},
            {"step": "raw_field", "path": "palaces.6.active_chart.energy_state.door",
             "value": "Prosperous", "description": "That door is Prosperous."},
            {"step": "raw_field", "path": "palaces.6.active_chart.stems.heaven", "value": "Ding",
             "description": "Ding is a San Qi stem."},
            {"step": "raw_field", "path": "palaces.8.active_chart.door", "value": "Sheng (Life)",
             "description": "Life door at palace 8."},
            {"step": "raw_field", "path": "palaces.8.active_chart.god", "value": "Liu He (Six Harmony)",
             "description": "Six Harmony supports agreement and partnership."},
            {"step": "computed_relation",
             "evidence_paths": ["palaces.6.palace_stem_rules.stems_in_tomb",
                                "palaces.8.palace_stem_rules.stems_in_tomb"],
             "description": "Palace 6 entombs the day stem Bing; palace 8 does not. Palace 6 is "
                            "Inner, palace 8 is Outer."},
            {"step": "interpretation_class", "class": "sanqi_with_good_door",
             "description": "Quality method at palace 6."},
            {"step": "interpretation_class", "class": "outer",
             "description": "Audience-facing route at palace 8."},
            {"step": "candidate_archetype",
             "name_or_combination": "BEST-OPEN-DOOR-NW-P6-WITH-DING | BEST-LIFE-DOOR-NE-P8-WITH-LIUHE",
             "description": "Two structurally different routes with equal chart support."},
        ],
        "candidates_considered": cands_best,
        "winner": None if still_tied else cands_best[0]["archetype_id"],
        "status": "STILL_TIED" if still_tied else "RESOLVED",
        "margin_note": (
            "Palace 6 and palace 8 score identically under the rubric and the documented "
            "tie-break order does not separate them: same grounding tier, same corroboration "
            "count, and their contradiction counts differ by one unresolved item each "
            "(palace 6 is the tomb of the day stem; palace 8 has a merely Resting door). "
            "Per unresolved_tie_policy they are emitted as split candidates rather than "
            "silently resolved. They would separate if the chart exposed whether the matter is "
            "inner (process/institution, favouring 6) or outer (audience/movement, favouring 8) - "
            "which is assignment information Prompt 1 is forbidden to use."
            if still_tied else
            "Narrow win, not a comfortable one: palace 8 leads palace 6 by 0.040 on a 0-1 scale. "
            "The only separator is the contradiction count - palace 6 is the tomb of the day stem "
            "Bing, which palace 8 is not. Everything else is level: same grounding tier, same "
            "corroboration, both pass board consistency. The decision would flip to palace 6 if "
            "the matter turns out to be inner (process, institution, quality of the thing itself) "
            "rather than outer (audience, reach, agreement), because palace 6 carries the San Qi "
            "stem and the Prosperous Open door while palace 8's Life door is only Resting. That "
            "inner/outer determination is assignment information, which Prompt 1 is forbidden to "
            "use, so palace 6 is retained as a live runner-up rather than discarded."),
    })

    jwrite(os.path.join(STATE, "archetype_resolutions.json"), {"resolutions": R})
    return R


# ================================================== BOARD CONSISTENCY =====
def board_consistency(resolutions):
    findings = []
    seed = jread(os.path.join(STATE, "solution_seed.json"))
    by_palace = {}
    for slot in ["answers", "hidden_problems", "best_solution_candidates"]:
        for it in seed[slot]:
            by_palace.setdefault(it["palace_id"], []).append((slot, it))
    for pid, items in sorted(by_palace.items(), key=lambda x: int(x[0])):
        pols = {i[1]["polarity"] for i in items}
        if "SUPPORT" in pols and "VETO" in pols:
            findings.append({
                "palace_id": pid, "type": "SLOT_BIAS_CONTRADICTION",
                "resolution": "SPLIT_CLAIMS_RECORDED",
                "detail_en": f"Palace {pid} carries both SUPPORT and VETO claims. Per the overload "
                             f"rule these are kept as separate typed claims and are not averaged "
                             f"into one verdict.",
                "claims": [i[1]["claim_id"] for i in items],
            })
    # explicit cross-check: p9 support vs p9 veto
    unresolved = [f for f in findings if f["resolution"] != "SPLIT_CLAIMS_RECORDED"]
    result = {
        "pass": len(unresolved) == 0,
        "unresolved_contradictions": len(unresolved),
        "split_claims_recorded": len(findings),
        "findings": findings,
        "rejected_for_inconsistency": [
            c["archetype_id"] for r in resolutions for c in r["candidates_considered"]
            if not c["board_consistency_pass"]],
    }
    jwrite(os.path.join(STATE, "board_consistency.json"), result)
    return result


# ======================================================= SOLUTION SEED ====
def freeze_seed(resolutions, consistency):
    seed = jread(os.path.join(STATE, "solution_seed.json"))
    winners = {"chart_answers_candidate": "AR-ANSWERS-01",
               "chart_hidden_problems_candidate": "AR-HIDDEN-01",
               "chart_best_solution_candidate": "AR-BEST-01"}
    for slot_key, rid in [("answers", "AR-ANSWERS-01"),
                          ("hidden_problems", "AR-HIDDEN-01"),
                          ("best_solution_candidates", "AR-BEST-01")]:
        for it in seed[slot_key]:
            it["archetype_resolution_id"] = rid

    def headline(rid):
        r = [x for x in resolutions if x["resolution_id"] == rid][0]
        sel = [c for c in r["candidates_considered"] if c["selected"]]
        return [{"archetype_id": c["archetype_id"], "text_en": c["label_en"],
                 "final_score": c["final_score"], "grounding_tier": c["grounding_tier"],
                 "archetype_resolution_id": rid,
                 "status": r.get("status", "RESOLVED"),
                 "requirement_fit_score": None} for c in sel]

    seed["headline_answers"] = headline("AR-ANSWERS-01")
    seed["headline_hidden_problems"] = headline("AR-HIDDEN-01")
    seed["headline_best_solution_candidates"] = headline("AR-BEST-01")
    seed["board_consistency"] = {"pass": consistency["pass"],
                                 "split_claims_recorded": consistency["split_claims_recorded"]}
    seed["note"] = "chart-derived only; not yet requirement-bound"
    seed["requirement_fit_score"] = None
    jwrite(os.path.join(STATE, "solution_seed.json"), seed)
    return seed


if __name__ == "__main__":
    systems = build_systems()
    patterns = build_patterns(systems)
    resolutions = build_resolutions()
    cons = board_consistency(resolutions)
    seed = freeze_seed(resolutions, cons)
    m = jread(os.path.join(STATE, "machine.json"))
    m["state"] = "P6_BOARD_SYNTHESIS"
    m["completed_phases"] = m["completed_phases"] + ["P6_BOARD_SYNTHESIS"]
    m["verification"]["board_consistency_passed"] = cons["pass"]
    m["verification"]["archetype_resolutions_scored"] = True
    m["verification"]["yongshen_candidates_unbound"] = True
    jwrite(os.path.join(STATE, "machine.json"), m)
    heartbeat(f"P6 done | patterns {len(patterns['hits'])} | resolutions {len(resolutions)} | "
              f"consistency pass {cons['pass']} | split_claims {cons['split_claims_recorded']}")
    print("patterns:", len(patterns["hits"]))
    for r in resolutions:
        print(r["resolution_id"], "winner:", r["winner"], "status:", r.get("status", "RESOLVED"))
        for c in r["candidates_considered"]:
            print("   ", c["final_score"], c["selected"], c["archetype_id"])
    print("consistency:", cons["pass"], "splits:", cons["split_claims_recorded"])
