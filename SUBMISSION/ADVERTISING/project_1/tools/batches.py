"""B1 -> B5 operator zoom. Executes S1..S12 for every selected palace.

Palace cards are JSON-first; markdown views are generated from JSON.
Verdicts are typed objects with evidence paths. Roles are append-only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
P = Q["palaces"]
IDX = jread(os.path.join(STATE, "indexes.json"))
ORIGIN = jread(os.path.join(STATE, "origin_sets.json"))
PILLARS = jread(os.path.join(STATE, "pillars.json"))
SEASON = jread(os.path.join(STATE, "season.json"))
DUTY = jread(os.path.join(STATE, "duty.json"))
LODGING = jread(os.path.join(STATE, "lodging.json"))
VALID = jread(os.path.join(STATE, "validation.json"))

DAY_STEM = PILLARS["pillars"]["day"]["stem"]
HOUR_STEM = PILLARS["pillars"]["hour"]["stem"]
SEASONAL = SEASON["strengths"]

CARDS = {}
SEED = {"answers": [], "hidden_problems": [], "best_solution_candidates": [],
        "note": "chart-derived only; not yet requirement-bound"}
SEED_REV = 0
RELATIONS = {}


def ev(pid, path, value):
    return {"palace_id": pid, "path": path, "value": str(value)}


def role(pid, name, rationale, paths):
    return {"palace_id": pid, "role": name, "rationale_en": rationale, "evidence_paths": paths}


# --------------------------------------------------------------- S1 .. S7 --
def stack(pid):
    pal = P[pid]
    ac = pal.get("active_chart", {})
    bp = pal.get("base_position", {})
    st = ac.get("stems", {})
    es = ac.get("energy_state", {})
    ident = PALACE_IDENTITY[pid]
    s = {}
    s["S1_identity"] = {
        "id": pid, "name": pal.get("name"), "canonical_name": ident["name"],
        "direction": pal.get("direction"), "element": pal.get("element"),
        "earthly_branches": bp.get("earthly_branches", []),
        "realm": es.get("realm"), "palace_strength": es.get("palace"),
        "trigram_numbers": bp.get("trigram_numbers"),
        "hetu_numbers": bp.get("hetu_numbers"),
        "early_heaven_trigram": bp.get("early_heaven_trigram"),
        "opposite_palace": OPPOSITE[pid],
        "paths": [f"palaces.{pid}.name", f"palaces.{pid}.direction",
                  f"palaces.{pid}.element",
                  f"palaces.{pid}.active_chart.energy_state.palace"],
    }
    s["S2_earth"] = {"earth_stem": st.get("earth"),
                     "earth_stem_element": STEM_ELEMENT.get(st.get("earth")),
                     "god": ac.get("god"), "home_god": bp.get("home_god"),
                     "paths": [f"palaces.{pid}.active_chart.stems.earth",
                               f"palaces.{pid}.active_chart.god"]}
    s["S3_door"] = {"door": ac.get("door"), "door_element": DOOR_ELEMENT.get(ac.get("door")),
                    "door_strength": es.get("door"), "home_door": bp.get("home_door"),
                    "door_at_original_palace": bool(ac.get("door")) and ac.get("door") == bp.get("home_door"),
                    "forced": None,
                    "paths": [f"palaces.{pid}.active_chart.door",
                              f"palaces.{pid}.active_chart.energy_state.door"]}
    stars = aslist(ac.get("star"))
    s["S4_heaven"] = {
        "heaven_stem": st.get("heaven"), "heaven_stem_element": STEM_ELEMENT.get(st.get("heaven")),
        "stars": stars, "star_elements": [STAR_ELEMENT.get(x) for x in stars],
        "star_home_palaces": [STAR_HOME_LUOSHU.get(x) for x in stars],
        "star_sitting_home": [x for x in stars if STAR_HOME_LUOSHU.get(x) == pid],
        "star_strength_seasonal": (es.get("star") or {}).get("seasonal"),
        "star_strength_by_palace": (es.get("star") or {}).get("palace_relation"),
        "home_star": bp.get("home_star"),
        "center_guest_stem": st.get("center_guest"),
        "note": ac.get("note"),
        "paths": [f"palaces.{pid}.active_chart.stems.heaven",
                  f"palaces.{pid}.active_chart.star",
                  f"palaces.{pid}.active_chart.energy_state.star"],
    }
    s["S5_hidden"] = {"hidden_stem": st.get("hidden"),
                      "hidden_stem_element": STEM_ELEMENT.get(st.get("hidden")),
                      "paths": [f"palaces.{pid}.active_chart.stems.hidden"]}
    status = ac.get("status", {})
    s["S6_markers"] = {
        "is_void": status.get("is_void", False),
        "has_horse_star": status.get("has_horse_star", False),
        "is_duty_palace": status.get("is_duty_palace", False),
        "carries_duty_star": DUTY["duty_star"] in stars,
        "carries_duty_door": ac.get("door") == DUTY["duty_door"],
        "hour_stem_focus": pid in ORIGIN["batch_selectors"]["B2"]["palaces"],
        "afflictions": st.get("afflictions", []),
        "paths": [f"palaces.{pid}.active_chart.status",
                  f"palaces.{pid}.active_chart.stems.afflictions"],
    }
    psr = pal.get("palace_stem_rules", {})
    s["S7_lists"] = {
        "tomb_stems": psr.get("stems_in_tomb", []),
        "punishment_stems": psr.get("stems_in_clash_punishment", []),
        "harm_stems": psr.get("stems_in_harm", []),
        "birth_stage_stems": psr.get("stems_in_birth_stage", []),
        "entombs_day_stem": DAY_STEM in psr.get("stems_in_tomb", []),
        "entombs_hour_stem": HOUR_STEM in psr.get("stems_in_tomb", []),
        "paths": [f"palaces.{pid}.palace_stem_rules"],
    }
    return s


# ------------------------------------------------------------------- S8 ----
def relations(pid, s):
    pal_el = s["S1_identity"]["element"]
    hs = s["S4_heaven"]["heaven_stem"]
    es_ = s["S2_earth"]["earth_stem"]
    hd = s["S5_hidden"]["hidden_stem"]
    door = s["S3_door"]["door"]
    door_el = s["S3_door"]["door_element"]
    out = []

    def add(kind, a, b, r, paths, note=""):
        out.append({"kind": kind, "a": a, "b": b, "relation": r,
                    "evidence_paths": paths, "note_en": note})

    if hs and es_:
        add("heaven_earth_stem_pair", hs, es_,
            "IDENTICAL (Fu Yin)" if hs == es_ else rel(STEM_ELEMENT[hs], STEM_ELEMENT[es_]),
            [f"palaces.{pid}.active_chart.stems.heaven", f"palaces.{pid}.active_chart.stems.earth"],
            "Heaven stem equals earth stem: no host/guest tension, the palace repeats itself."
            if hs == es_ else "")
    if hs and hd:
        add("heaven_hidden_stem_pair", hs, hd,
            "IDENTICAL (Fu Yin)" if hs == hd else rel(STEM_ELEMENT[hs], STEM_ELEMENT[hd]),
            [f"palaces.{pid}.active_chart.stems.heaven", f"palaces.{pid}.active_chart.stems.hidden"])
    if hs:
        add("stem_vs_palace", hs, pal_el, rel(STEM_ELEMENT[hs], pal_el),
            [f"palaces.{pid}.active_chart.stems.heaven", f"palaces.{pid}.element"])
    if door_el:
        add("door_vs_palace", door, pal_el, rel(door_el, pal_el),
            [f"palaces.{pid}.active_chart.door", f"palaces.{pid}.element"])
    for st_ in s["S4_heaven"]["stars"]:
        se = STAR_ELEMENT.get(st_)
        if se:
            add("star_vs_palace", st_, pal_el, rel(se, pal_el),
                [f"palaces.{pid}.active_chart.star", f"palaces.{pid}.element"])
        if hs:
            add("star_vs_heaven_stem", st_, hs, rel(se, STEM_ELEMENT[hs]),
                [f"palaces.{pid}.active_chart.star", f"palaces.{pid}.active_chart.stems.heaven"])
    if hs and door_el:
        add("stem_vs_door", hs, door, rel(STEM_ELEMENT[hs], door_el),
            [f"palaces.{pid}.active_chart.stems.heaven", f"palaces.{pid}.active_chart.door"])
    if hs:
        add("stem_vs_season", hs, "seasonal_element_strengths",
            SEASONAL[STEM_ELEMENT[hs]],
            [f"palaces.{pid}.active_chart.stems.heaven", "element_prosperities"])
        add("stem_vs_day_stem", hs, DAY_STEM, rel(STEM_ELEMENT[hs], STEM_ELEMENT[DAY_STEM]),
            [f"palaces.{pid}.active_chart.stems.heaven", "timing.four_pillars.day"])
        for (a, b, prod) in STEM_COMBINATIONS:
            if hs in (a, b):
                other = b if hs == a else a
                if other in IDX["heaven_stem"]:
                    add("stem_combination_across_board", hs, other, f"COMBINES -> {prod}",
                        [f"palaces.{pid}.active_chart.stems.heaven",
                         f"palaces.{IDX['heaven_stem'][other][0]}.active_chart.stems.heaven"],
                        f"{hs} pairs with {other} at palace {IDX['heaven_stem'][other]}.")
        for (a, b) in STEM_CLASHES:
            if hs in (a, b):
                other = b if hs == a else a
                if other in IDX["heaven_stem"]:
                    add("stem_clash_across_board", hs, other, "CLASH",
                        [f"palaces.{pid}.active_chart.stems.heaven",
                         f"palaces.{IDX['heaven_stem'][other][0]}.active_chart.stems.heaven"],
                        f"{hs} clashes {other} at palace {IDX['heaven_stem'][other]}.")
    if hs and s["S7_lists"]["tomb_stems"] and hs in s["S7_lists"]["tomb_stems"]:
        add("self_entombed", hs, pid, "STEM_IN_OWN_TOMB_PALACE",
            [f"palaces.{pid}.active_chart.stems.heaven",
             f"palaces.{pid}.palace_stem_rules.stems_in_tomb"])
    if hs and hs in s["S7_lists"]["punishment_stems"]:
        add("self_punished", hs, pid, "STEM_IN_OWN_PUNISHMENT_PALACE",
            [f"palaces.{pid}.active_chart.stems.heaven",
             f"palaces.{pid}.palace_stem_rules.stems_in_clash_punishment"])
    # strength concordance
    vals = [s["S1_identity"]["palace_strength"], s["S3_door"]["door_strength"],
            s["S4_heaven"]["star_strength_seasonal"], s["S4_heaven"]["star_strength_by_palace"]]
    vals = [v for v in vals if v]
    add("strength_concordance", pid, "|".join(vals),
        "CONCORDANT" if len(set(vals)) == 1 else "SPLIT",
        [f"palaces.{pid}.active_chart.energy_state"],
        "Split strength: the palace does not read the same from every angle."
        if len(set(vals)) > 1 else "")
    RELATIONS[pid] = out
    return out


# ------------------------------------------------------------------- S9 ----
def index_pull(pid, s):
    pulls = {}
    hs = s["S4_heaven"]["heaven_stem"]
    if hs:
        pulls["same_heaven_stem_elsewhere"] = [x for x in IDX["heaven_stem"].get(hs, []) if x != pid]
        pulls["this_stem_entombed_at"] = IDX["tomb_stems"].get(hs, [])
        pulls["this_stem_punished_at"] = IDX["punishment_stems"].get(hs, [])
        pulls["this_stem_harmed_at"] = IDX["harm_stems"].get(hs, [])
        pulls["this_stem_in_birth_stage_at"] = IDX["birth_stage_stems"].get(hs, [])
    d = s["S3_door"]["door"]
    if d:
        pulls["same_door_elsewhere"] = [x for x in IDX["door"].get(d, []) if x != pid]
    for st_ in s["S4_heaven"]["stars"]:
        pulls.setdefault("same_star_elsewhere", []).extend(
            [x for x in IDX["star"].get(st_, []) if x != pid])
    g = s["S2_earth"]["god"]
    if g:
        pulls["same_god_elsewhere"] = [x for x in IDX["god"].get(g, []) if x != pid]
        pulls["this_god_is_home_god_of"] = IDX["home_god"].get(g, [])
    return pulls


# ------------------------------------------------------------- verdicts ----
CID = [0]


def mk(pid, slot, text, polarity, confidence, grounding, evidence, phase, batch):
    CID[0] += 1
    return {"claim_id": f"V{CID[0]:03d}-P{pid}", "slot": slot, "text_en": text,
            "polarity": polarity, "confidence": confidence, "grounding": grounding,
            "evidence": evidence, "phase": phase, "batch": batch, "status": "live",
            "palace_id": pid}


def verdicts(pid, s, rels, batch):
    V = []
    R = []
    ident = s["S1_identity"]
    m = s["S6_markers"]
    hs = s["S4_heaven"]["heaven_stem"]
    door = s["S3_door"]["door"]
    ph = "P1_TO_P4_OPERATOR_ZOOM" if batch != "B5" else "P5_REMAINING"

    # ---- role overlays (append-only)
    if pid in ORIGIN["batch_selectors"]["B1"]["palaces"]:
        R.append(role(pid, "day_stem_or_jia_set", "Selected by the day-stem origin set.",
                      ["timing.four_pillars.day"]))
    if m["hour_stem_focus"]:
        R.append(role(pid, "hour_stem_or_focus", "Selected by the hour-stem proxy set.",
                      ["timing.four_pillars.hour", "chart_config.lead_stem"]))
    if m["carries_duty_star"]:
        R.append(role(pid, "duty_star", "Carries the duty star, the authority of the matter.",
                      ["chart_config.duty_star"]))
    if m["carries_duty_door"]:
        R.append(role(pid, "duty_door", "Carries the duty door.", ["chart_config.duty_door"]))
    if m["is_void"]:
        R.append(role(pid, "void_on_showpiece", "Void palace.",
                      [f"palaces.{pid}.active_chart.status.is_void"]))
    if m["has_horse_star"]:
        R.append(role(pid, "horse_plus_open", "Horse star present: movement/relocation.",
                      [f"palaces.{pid}.active_chart.status.has_horse_star"]))
    if s["S7_lists"]["entombs_day_stem"]:
        R.append(role(pid, "tomb_of_yongshen", "Entombs the day stem.",
                      [f"palaces.{pid}.palace_stem_rules.stems_in_tomb"]))
    if s["S7_lists"]["entombs_hour_stem"]:
        R.append(role(pid, "tomb_of_yongshen", "Entombs the hour stem.",
                      [f"palaces.{pid}.palace_stem_rules.stems_in_tomb"]))
    R.append(role(pid, "inner" if ident["realm"] == "Inner" else "outer",
                  "Realm as declared by the chart."
                  if ident["realm"] else "Centre: no realm field; treated as inner pivot.",
                  [f"palaces.{pid}.active_chart.energy_state.realm"]))
    if pid == "5":
        R.append(role(pid, "lodged_from_center", "Centre content is hosted by palace 2.",
                      ["palaces.5.active_chart.note"]))
    if pid == LODGING["host_palace"]:
        R.append(role(pid, "lodged_from_center", "Hosts the displaced Centre.",
                      ["palaces.5.active_chart.note", "palaces.2.active_chart.stems.center_guest"]))
    if pid in [PILLARS["pillars"][k]["branch_palace"] for k in ["year", "month", "day", "hour"]]:
        which = [k for k in ["year", "month", "day", "hour"]
                 if PILLARS["pillars"][k]["branch_palace"] == pid]
        R.append(role(pid, "stacked_branch", f"Pillar branch(es) {which} land here.",
                      [f"timing.four_pillars.{w}" for w in which]))
    if hs == DUTY["lead_proxy_stem"] and pid in DUTY["lead_proxy_palaces"]:
        R.append(role(pid, "lead_stem_proxy", "Visible stand-in for the invisible Jia decade.",
                      ["chart_config.lead_stem"]))

    # ---- verdict rules (split claims; never average)
    if m["is_void"]:
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"Palace {pid} ({ident['name']}, {ident['direction']}) is void. Whatever is "
                    f"shown here does not land as displayed: it is announced but not received.",
                    "WARN", "HIGH", "EXPLICIT",
                    [ev(pid, f"palaces.{pid}.active_chart.status.is_void", True),
                     ev(pid, "timing.voidness", PILLARS["void"]["day_void_branches"]
                        + PILLARS["void"]["hour_void_branches"])], ph, batch))
    if m["has_horse_star"]:
        V.append(mk(pid, "timing",
                    f"Palace {pid} carries the horse star: the matter here moves, travels or "
                    f"changes hands rather than staying put.",
                    "SEQUENCE", "MED", "EXPLICIT",
                    [ev(pid, f"palaces.{pid}.active_chart.status.has_horse_star", True),
                     ev(pid, "timing.four_pillars.day", PILLARS["pillars"]["day"]["raw"])], ph, batch))
    for a in m["afflictions"]:
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"Palace {pid} carries the affliction '{a}'. Self-inflicted damage or "
                    f"internal contradiction is recorded on this palace by the chart itself.",
                    "VETO" if "Punishment" in a else "WARN", "HIGH", "EXPLICIT",
                    [ev(pid, f"palaces.{pid}.active_chart.stems.afflictions", a)], ph, batch))
    ds = s["S3_door"]["door_strength"]
    if ds in ("Dead", "Imprisoned"):
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"The {door} door at palace {pid} is {ds}. This method is available on paper "
                    f"but has no force behind it; using it costs effort and returns little.",
                    "VETO", "HIGH", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.active_chart.energy_state.door", ds),
                     ev(pid, f"palaces.{pid}.active_chart.door", door)], ph, batch))
    elif ds == "Prosperous":
        V.append(mk(pid, "chart_best_solution_candidate",
                    f"The {door} door at palace {pid} is Prosperous. This is a method the season "
                    f"actually supports.",
                    "SUPPORT", "HIGH", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.active_chart.energy_state.door", ds),
                     ev(pid, f"palaces.{pid}.active_chart.door", door),
                     ev(pid, "element_prosperities", SEASONAL.get(DOOR_ELEMENT.get(door, ""), ""))],
                    ph, batch))
    if hs in SANQI:
        V.append(mk(pid, "chart_best_solution_candidate",
                    f"Palace {pid} holds the San Qi stem {hs}. Quality, reputation and visibility "
                    f"are concentrated here.",
                    "SUPPORT", "MED", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.active_chart.stems.heaven", hs),
                     ev(pid, "element_prosperities", SEASONAL[STEM_ELEMENT[hs]])], ph, batch))
    if hs and SEASONAL[STEM_ELEMENT[hs]] in ("Dead", "Imprisoned"):
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"The stem {hs} ({STEM_ELEMENT[hs]}) at palace {pid} is "
                    f"{SEASONAL[STEM_ELEMENT[hs]]} this season. The climate does not support it "
                    f"however good it looks on the board.",
                    "CONSTRAIN", "HIGH", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.active_chart.stems.heaven", hs),
                     ev(pid, "element_prosperities", SEASONAL[STEM_ELEMENT[hs]])], ph, batch))
    if s["S7_lists"]["entombs_day_stem"]:
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"Palace {pid} is the tomb of the day stem {DAY_STEM}. Committing the self "
                    f"here buries it: effort goes in and does not come back out.",
                    "VETO", "HIGH", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.palace_stem_rules.stems_in_tomb", DAY_STEM),
                     ev(pid, "timing.four_pillars.day", PILLARS["pillars"]["day"]["raw"])], ph, batch))
    if s["S7_lists"]["entombs_hour_stem"]:
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"Palace {pid} is the tomb of the hour stem {HOUR_STEM}. The matter in motion "
                    f"is already buried at this location.",
                    "VETO", "HIGH", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.palace_stem_rules.stems_in_tomb", HOUR_STEM),
                     ev(pid, "timing.four_pillars.hour", PILLARS["pillars"]["hour"]["raw"])], ph, batch))
    if m["is_duty_palace"]:
        V.append(mk(pid, "chart_answers_candidate",
                    f"Palace {pid} is the duty palace: it carries both the duty star "
                    f"{DUTY['duty_star']} and the duty door {DUTY['duty_door']}. This is where the "
                    f"chart says the subject of the question actually sits.",
                    "SUPPORT", "HIGH", "EXPLICIT",
                    [ev(pid, f"palaces.{pid}.active_chart.status.is_duty_palace", True),
                     ev(pid, "chart_config.duty_star", DUTY["duty_star"]),
                     ev(pid, "chart_config.duty_door", DUTY["duty_door"])], ph, batch))
    conc = [r for r in rels if r["kind"] == "strength_concordance"][0]
    if conc["relation"] == "SPLIT":
        V.append(mk(pid, "risk",
                    f"Palace {pid} reads differently from different angles ({conc['b']}). It looks "
                    f"one way and behaves another; do not trust a single strength reading here.",
                    "CONSTRAIN", "MED", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.active_chart.energy_state", conc["b"])], ph, batch))
    if s["S4_heaven"]["star_sitting_home"] and s["S3_door"]["door_at_original_palace"]:
        V.append(mk(pid, "risk",
                    f"Palace {pid} has its own star and its own door at home, with heaven, earth "
                    f"and hidden stems identical. Nothing here is in motion; the position repeats "
                    f"itself rather than developing.",
                    "CONSTRAIN", "HIGH", "COMPUTED",
                    [ev(pid, f"palaces.{pid}.active_chart.star", s["S4_heaven"]["stars"]),
                     ev(pid, f"palaces.{pid}.active_chart.door", door),
                     ev(pid, "chart_config.chart_pattern", Q["chart_config"]["chart_pattern"])],
                    ph, batch))
    if pid == "5":
        V.append(mk(pid, "chart_answers_candidate",
                    f"The day stem {DAY_STEM} sits in the Centre and is attached to palace 2. The "
                    f"actor is displaced: it has no directional position of its own and must "
                    f"operate through its host.",
                    "CONSTRAIN", "HIGH", "EXPLICIT",
                    [ev("5", "palaces.5.active_chart.stems.heaven", "Bing"),
                     ev("5", "palaces.5.active_chart.note", "Attached to Palace 2"),
                     ev("2", "palaces.2.active_chart.stems.center_guest", "Bing")], ph, batch))
    if pid == LODGING["host_palace"]:
        V.append(mk(pid, "chart_hidden_problems_candidate",
                    f"Palace {pid} hosts the displaced day stem Bing while being void, "
                    f"horse-struck, clash-punished and carrying the Death door. The actor's only "
                    f"landing place is the worst-conditioned palace on the board.",
                    "VETO", "HIGH", "COMPUTED",
                    [ev("2", "palaces.2.active_chart.stems.center_guest", "Bing"),
                     ev("2", "palaces.2.active_chart.status.is_void", True),
                     ev("2", "palaces.2.active_chart.door", P["2"]["active_chart"]["door"]),
                     ev("2", "palaces.2.active_chart.stems.afflictions",
                        P["2"]["active_chart"]["stems"]["afflictions"])], ph, batch))
    return V, R


# ------------------------------------------------------------- S12 patch ---
def patch_seed(V):
    global SEED_REV
    for v in V:
        if v["polarity"] == "SILENT":
            continue
        item = {"claim_id": v["claim_id"], "palace_id": v["palace_id"],
                "text_en": v["text_en"], "polarity": v["polarity"],
                "grounding": v["grounding"], "confidence": v["confidence"],
                "archetype_resolution_id": None}
        if v["slot"] == "chart_answers_candidate":
            SEED["answers"].append(item)
        elif v["slot"] == "chart_hidden_problems_candidate":
            SEED["hidden_problems"].append(item)
        elif v["slot"] == "chart_best_solution_candidate":
            SEED["best_solution_candidates"].append(item)
        SEED_REV += 1
    jwrite(os.path.join(STATE, "solution_seed.json"),
           {"revision": SEED_REV, **SEED})


def card_md(card):
    s = card["stack"]
    L = ["---", f"id: palace-{card['palace_id']}", "type: palace-card",
         f"phase: {card['phase']}", f"batch: {card['batch']}",
         f"palace_ids: [\"{card['palace_id']}\"]",
         "sources: [\"raw/chart/dump.md\", \"raw/state/indexes.json\", \"raw/QMDJ.json\"]",
         f"updated: {GENERATED_AT}", "status: verdicted", "---", "",
         f"# Palace {card['palace_id']} - {s['S1_identity']['name']} "
         f"({s['S1_identity']['direction']})", "",
         f"> {s['S1_identity']['element']} palace | realm "
         f"{s['S1_identity']['realm'] or 'Centre'} | strength "
         f"{s['S1_identity']['palace_strength']} | opposite "
         f"{s['S1_identity']['opposite_palace'] or 'NO_OPPOSITE'}", "",
         "## Infobox", "",
         "| field | value |", "|---|---|",
         f"| Heaven stem | {s['S4_heaven']['heaven_stem']} |",
         f"| Earth stem | {s['S2_earth']['earth_stem']} |",
         f"| Hidden stem | {s['S5_hidden']['hidden_stem']} |",
         f"| Door | {s['S3_door']['door']} ({s['S3_door']['door_strength']}) |",
         f"| Star | {', '.join(s['S4_heaven']['stars']) or '-'} |",
         f"| Spirit | {s['S2_earth']['god']} |",
         f"| Branches | {', '.join(s['S1_identity']['earthly_branches']) or '-'} |",
         f"| Void | {s['S6_markers']['is_void']} |",
         f"| Horse star | {s['S6_markers']['has_horse_star']} |",
         f"| Afflictions | {', '.join(s['S6_markers']['afflictions']) or '-'} |",
         f"| Tomb of | {', '.join(s['S7_lists']['tomb_stems']) or '-'} |",
         f"| Punishment of | {', '.join(s['S7_lists']['punishment_stems']) or '-'} |", "",
         "## Roles", ""]
    for r in card["roles"]:
        L.append(f"- **{r['role']}** - {r['rationale_en']}")
    L += ["", "## Relations (S8)", "", "| kind | a | b | relation |", "|---|---|---|---|"]
    for r in card["relations"]:
        L.append(f"| {r['kind']} | {r['a']} | {r['b']} | {r['relation']} |")
    L += ["", "## Verdicts (S11)", ""]
    for v in card["verdicts"]:
        L.append(f"### {v['claim_id']} - {v['slot']} / {v['polarity']}")
        L.append("")
        L.append(v["text_en"])
        L.append("")
        L.append(f"- grounding: `{v['grounding']}` | confidence: `{v['confidence']}`")
        for e in v["evidence"]:
            L.append(f"- evidence: `{e['path']}` = `{e['value']}`")
        L.append("")
    L += ["## See also", "", "- [[Chart-Board-Synthesis]]", "- [[Chart-Patterns]]",
          "- [[Palace-Analysis-Index]]", "",
          "## Sources", "", "- `vault/raw/QMDJ.json`", "- `vault/raw/chart/dump.md`",
          "- `vault/raw/state/indexes.json`", ""]
    return "\n".join(L)


def run_batch(batch, pids):
    for pid in pids:
        if pid in CARDS:
            # confirm/veto pass on already-read palace: append batch tag only
            CARDS[pid]["also_selected_in"].append(batch)
            continue
        s = stack(pid)
        rels = relations(pid, s)
        pulls = index_pull(pid, s)
        V, R = verdicts(pid, s, rels, batch)
        card = {"palace_id": pid, "canonical_name": PALACE_IDENTITY[pid]["name"],
                "phase": "P1_TO_P4_OPERATOR_ZOOM" if batch != "B5" else "P5_REMAINING",
                "batch": batch, "also_selected_in": [], "stack": s,
                "index_pull": pulls, "roles": R, "analyses": [
                    {"step": "S8", "summary_en": f"{len(rels)} intra-palace relations computed."},
                    {"step": "S9", "summary_en": "Reverse-index occurrences pulled."},
                ], "relations": rels, "verdicts": V}
        card = prune_paths(card, Q)
        card["verdicts"] = [dict(v, evidence=[e for e in v["evidence"]
                                              if path_resolves(e["path"], Q)])
                            for v in card["verdicts"]]
        CARDS[pid] = card
        patch_seed(V)
        jwrite(os.path.join(TRACES, f"palace-{pid}.json"), card)
        twrite(os.path.join(WIKI_PALACES, f"Palace-{pid}-{PALACE_IDENTITY[pid]['name']}.md"),
               card_md(card))
        heartbeat(f"{batch} | palace {pid} {PALACE_IDENTITY[pid]['name']} done | "
                  f"verdicts: {len(V)} | seed_rev: {SEED_REV}")
    m = jread(os.path.join(STATE, "machine.json"))
    m["completed_batches"] = sorted(set(m["completed_batches"] + [batch]))
    m["state"] = batch
    m["palaces"] = {k: {"status": "verdicted", "batch": CARDS[k]["batch"],
                        "verdict_count": len(CARDS[k]["verdicts"])} for k in CARDS}
    m["solution_seed_revision"] = SEED_REV
    jwrite(os.path.join(STATE, "machine.json"), m)
    heartbeat(f"{batch} complete | palaces {pids} | seed_rev {SEED_REV}")


if __name__ == "__main__":
    sel = ORIGIN["batch_selectors"]
    for b in ["B1", "B2", "B3", "B4", "B5"]:
        run_batch(b, sel[b]["palaces"])
    jwrite(os.path.join(STATE, "palaces.json"), CARDS)
    jwrite(os.path.join(STATE, "relations.json"),
           {"per_palace": RELATIONS,
            "note": "S8 intra-palace relation engine output, computed from value matches only."})
    print("palaces analysed:", sorted(CARDS, key=int))
    print("total verdicts:", sum(len(c["verdicts"]) for c in CARDS.values()))
    print("seed answers/hidden/best:",
          len(SEED["answers"]), len(SEED["hidden_problems"]), len(SEED["best_solution_candidates"]))
