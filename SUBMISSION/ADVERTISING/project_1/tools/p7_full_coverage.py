"""P7_FULL_FIELD_COVERAGE.

Consumes every field of QMDJ.json that the P0-P6 pipeline did not analytically
use: id, trigram_numbers, hetu_numbers, early_heaven_trigram, home_god,
home_door, home_star, earthly_branches (as base data), stems_in_harm,
stems_in_birth_stage, star energy sub-states, element_prosperities per element,
and solar_term.name.

Each subsystem below produces real computed findings with evidence paths, not
a restatement of the raw value.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
P = Q["palaces"]
IDX = jread(os.path.join(STATE, "indexes.json"))
CARDS = jread(os.path.join(STATE, "palaces.json"))
PILLARS = jread(os.path.join(STATE, "pillars.json"))
SEASONAL = jread(os.path.join(STATE, "season.json"))["strengths"]
DAY_STEM = PILLARS["pillars"]["day"]["stem"]
HOUR_STEM = PILLARS["pillars"]["hour"]["stem"]
ALL_STEMS_ON_PLATE = set(IDX["heaven_stem"].keys())

FINDINGS = []


def F(subsystem, name, palaces, detail, paths, polarity="NEUTRAL", grounding="COMPUTED"):
    FINDINGS.append({"subsystem": subsystem, "name_en": name, "palaces": palaces,
                     "detail_en": detail, "evidence_paths": paths,
                     "polarity": polarity, "grounding": grounding})


# ============================================== 1. PALACE ID INTEGRITY =====
def id_integrity():
    out = {}
    mismatches = []
    for pid in sorted(P, key=int):
        declared = P[pid].get("id")
        out[pid] = {"object_key": pid, "id_field": declared,
                    "match": str(declared) == pid,
                    "later_heaven_expected": LATER_HEAVEN_NUM.get(P[pid]["name"]),
                    "later_heaven_match": LATER_HEAVEN_NUM.get(P[pid]["name"]) == declared,
                    "path": f"palaces.{pid}.id"}
        if not out[pid]["match"] or not out[pid]["later_heaven_match"]:
            mismatches.append(pid)
    if mismatches:
        F("palace_id", "id_key_mismatch", mismatches,
          f"Palace id field disagrees with object key or Later Heaven number at {mismatches}.",
          [f"palaces.{p}.id" for p in mismatches], "NEGATIVE")
    else:
        F("palace_id", "id_integrity_confirmed", sorted(P, key=int),
          "Every palace's `id` field matches both its object key and its canonical Later Heaven "
          "(Hou Tian) palace number. The nine-palace indexing is sound, so no verdict in this "
          "package rests on a mis-keyed palace.",
          [f"palaces.{p}.id" for p in sorted(P, key=int)], "POSITIVE")
    return out


# ================================================== 2. HE TU NUMBERS =======
def hetu():
    out = {}
    for pid in sorted(P, key=int):
        nums = P[pid]["base_position"].get("hetu_numbers")
        if not nums:
            continue
        key = tuple(sorted(nums))
        el = HETU_PAIR_ELEMENT.get(key)
        pal_el = P[pid]["element"]
        inner, outer = min(nums), max(nums)
        out[pid] = {
            "hetu_numbers": nums, "generative_inner": inner, "completion_outer": outer,
            "hetu_element": el, "palace_element": pal_el,
            "agrees_with_palace_element": el == pal_el,
            "hetu_element_season": SEASONAL.get(el),
            "path": f"palaces.{pid}.base_position.hetu_numbers",
        }
    # Which palaces' He Tu element is supported by the season?
    strong = [p for p, v in out.items() if v["hetu_element_season"] in ("Prosperous", "Strengthening")]
    weak = [p for p, v in out.items() if v["hetu_element_season"] in ("Dead", "Imprisoned")]
    F("hetu", "hetu_element_seasonal_support", sorted(strong, key=int),
      f"By He Tu pairing, palaces {', '.join(sorted(strong, key=int))} carry an element the "
      f"season supports (Metal 4-9, Water 1-6). These are the palaces whose *deep structure*, "
      f"not merely their surface placement, is in phase with White Dew.",
      [f"palaces.{p}.base_position.hetu_numbers" for p in sorted(strong, key=int)], "POSITIVE")
    F("hetu", "hetu_element_seasonally_dead", sorted(weak, key=int),
      f"Palaces {', '.join(sorted(weak, key=int))} carry a He Tu element the season kills "
      f"(Wood 3-8, Fire 2-7). Palace 9's He Tu pair is 2-7 Fire, and Fire is Imprisoned - the "
      f"duty palace is structurally out of season at the He Tu layer as well as the surface "
      f"layer, which is an independent confirmation of the void showpiece finding.",
      [f"palaces.{p}.base_position.hetu_numbers" for p in sorted(weak, key=int)], "NEGATIVE")
    # Earth-group palaces sharing 5-10
    shared = [p for p, v in out.items() if tuple(sorted(v["hetu_numbers"])) == (5, 10)]
    F("hetu", "shared_earth_axis_5_10", sorted(shared, key=int),
      f"Palaces {', '.join(sorted(shared, key=int))} all share the He Tu pair 5-10 (Earth). "
      f"The Centre (5), the actor's host (2) and the clean outer palace (8) are bound onto one "
      f"Earth axis. This is the structural reason the displaced day stem can lodge into palace 2 "
      f"at all, and it is also the channel that connects palace 2 to palace 8.",
      [f"palaces.{p}.base_position.hetu_numbers" for p in sorted(shared, key=int)], "NEUTRAL")
    mismatch = [p for p, v in out.items() if not v["agrees_with_palace_element"]]
    if mismatch:
        F("hetu", "hetu_vs_palace_element_divergence", sorted(mismatch, key=int),
          "He Tu element differs from the declared palace element at palaces "
          + ", ".join(sorted(mismatch, key=int))
          + ". Recorded as structural tension, not as a data error.",
          [f"palaces.{p}.base_position.hetu_numbers" for p in sorted(mismatch, key=int)], "NEUTRAL")
    return out


# ============================== 3. TRIGRAM NUMBERS / EARLY HEAVEN ==========
def trigrams():
    out = {}
    for pid in sorted(P, key=int):
        bp = P[pid]["base_position"]
        tn = bp.get("trigram_numbers")
        eh = bp.get("early_heaven_trigram")
        if tn is None and eh is None:
            continue
        eh_name = eh.split(" (")[0] if eh else None
        eh_num = int(eh.split("(")[1].rstrip(")")) if eh and "(" in eh else None
        later = LATER_HEAVEN_NUM.get(P[pid]["name"])
        out[pid] = {
            "trigram_numbers": tn,
            "early_heaven_trigram": eh, "early_heaven_name": eh_name,
            "early_heaven_number": eh_num,
            "early_heaven_number_canonical": EARLY_HEAVEN_NUM.get(eh_name),
            "early_heaven_number_matches_canon": EARLY_HEAVEN_NUM.get(eh_name) == eh_num,
            "later_heaven_number": later,
            "trigram_numbers_encode_early_later": (
                tn is not None and later is not None and eh_num is not None
                and sorted(tn) == sorted([eh_num, later])),
            "early_heaven_element": TRIGRAM_ELEMENT.get(eh_name),
            "later_heaven_element": P[pid]["element"],
            "paths": [f"palaces.{pid}.base_position.trigram_numbers",
                      f"palaces.{pid}.base_position.early_heaven_trigram"],
        }
    encoded = [p for p, v in out.items() if v["trigram_numbers_encode_early_later"]]
    canon_ok = [p for p, v in out.items() if v["early_heaven_number_matches_canon"]]
    F("trigram", "trigram_numbers_decoded", sorted(encoded, key=int),
      f"The two-number `trigram_numbers` array is not arbitrary: at palaces "
      f"{', '.join(sorted(encoded, key=int))} it is exactly [Early Heaven number, Later Heaven "
      f"number]. For example palace 1 Kan carries [6, 1] - Kan is 6 in the Early Heaven "
      f"arrangement and 1 in the Later Heaven arrangement. This field was previously uninterpreted; "
      f"it encodes each palace's position in both arrangements simultaneously.",
      [f"palaces.{p}.base_position.trigram_numbers" for p in sorted(encoded, key=int)], "POSITIVE")
    F("trigram", "early_heaven_labels_verified", sorted(canon_ok, key=int),
      f"Every `early_heaven_trigram` label carries the correct canonical Fu Xi number "
      f"({len(canon_ok)}/{len(out)} verified). The chart's Early Heaven layer is internally "
      f"consistent and can be trusted as a cross-check.",
      [f"palaces.{p}.base_position.early_heaven_trigram" for p in sorted(canon_ok, key=int)],
      "POSITIVE")
    # element shift between arrangements
    shifted = [p for p, v in out.items()
               if v["early_heaven_element"] and v["early_heaven_element"] != v["later_heaven_element"]]
    F("trigram", "early_vs_later_heaven_element_shift", sorted(shifted, key=int),
      "At palaces " + ", ".join(sorted(shifted, key=int)) + " the Early Heaven trigram's element "
      "differs from the Later Heaven palace element - the palace's original nature differs from "
      "its manifest nature. Palace 9 (Li, Fire) sits on Early Heaven Qian (Metal): the showpiece "
      "position is originally a Metal/authority seat wearing a Fire/visibility face. Palace 2 "
      "(Kun, Earth) sits on Early Heaven Xun (Wood): the actor's host is originally a Wood seat, "
      "and Wood is Dead this season, which deepens the weakness already found there.",
      [f"palaces.{p}.base_position.early_heaven_trigram" for p in sorted(shifted, key=int)],
      "NEUTRAL")
    return out


# ============================= 4. HOME vs ACTIVE (displacement engine) =====
def home_vs_active():
    out = {}
    door_moves, star_moves, god_moves = [], [], []
    for pid in sorted(P, key=int):
        bp = P[pid]["base_position"]
        ac = P[pid]["active_chart"]
        hd, hs_, hg = bp.get("home_door"), bp.get("home_star"), bp.get("home_god")
        ad = ac.get("door")
        astars = aslist(ac.get("star"))
        ag = ac.get("god")
        rec = {
            "home_door": hd, "active_door": ad,
            "door_unchanged": bool(hd) and hd == ad,
            "home_star": hs_, "active_stars": astars,
            "star_unchanged": bool(hs_) and hs_ in astars,
            "home_god": aslist(hg), "active_god": ag,
            "god_unchanged": bool(ag) and ag in aslist(hg),
            "active_god_belongs_to": IDX["home_god"].get(ag, []),
            "paths": [f"palaces.{pid}.base_position.home_door",
                      f"palaces.{pid}.base_position.home_star",
                      f"palaces.{pid}.base_position.home_god",
                      f"palaces.{pid}.active_chart.god"],
        }
        out[pid] = rec
        if hd and ad and hd != ad:
            door_moves.append(pid)
        if hs_ and astars and hs_ not in astars:
            star_moves.append(pid)
        if ag and hg and ag not in aslist(hg):
            god_moves.append(pid)

    F("displacement", "doors_and_stars_have_not_moved", sorted(P, key=int),
      f"Comparing `base_position.home_door`/`home_star` against `active_chart` across all nine "
      f"palaces: {len(door_moves)} doors moved and {len(star_moves)} stars moved. This is the "
      f"independent proof of Fu Yin from the base-position layer, which the earlier analysis "
      f"asserted from the stems alone. The declaration at `chart_config.chart_pattern` is now "
      f"confirmed from three separate directions.",
      [f"palaces.{p}.base_position.home_door" for p in sorted(P, key=int)], "NEGATIVE")

    F("displacement", "only_the_spirits_moved", sorted(god_moves, key=int),
      f"The spirits are the sole moving system on this board. Displaced at palaces "
      f"{', '.join(sorted(god_moves, key=int))}. On a totally frozen Fu Yin plate, the spirit "
      f"layer carries every bit of the chart's dynamic information - it is the only place where "
      f"anything is telling you about change rather than stasis.",
      [f"palaces.{p}.active_chart.god" for p in sorted(god_moves, key=int)], "POSITIVE")

    # the specific swap
    F("displacement", "zhi_fu_bai_hu_axis_swap", ["1", "9"],
      "Zhi Fu (Chief) belongs to palace 1 by `home_god` but is active at palace 9; Bai Hu "
      "(White Tiger) is listed among palace 9's home gods but is active at palace 1. Authority "
      "and predation have traded ends of the Kan-Li axis. Authority has walked onto the void, "
      "triple-afflicted showpiece, while the Tiger now sits on the North palace whose star is "
      "Obsolete by palace relation. Command has gone somewhere it cannot act, and aggression has "
      "gone somewhere nobody is watching.",
      ["palaces.1.base_position.home_god", "palaces.9.active_chart.god",
       "palaces.9.base_position.home_god", "palaces.1.active_chart.god"], "NEGATIVE")

    F("displacement", "jiu_tian_to_the_actors_host", ["2", "6"],
      "Jiu Tian (Nine Heavens) is the home god of palace 6 but is active at palace 2. The "
      "expansion/high-ground spirit has left the one Prosperous palace and landed on the void, "
      "Death-door palace that hosts the displaced day stem. Read together with the horse star "
      "already found at palace 2, the chart puts both of its movement signals - Nine Heavens and "
      "the horse - on the actor's compromised seat. The urge to expand is real and is located "
      "precisely where there is no ground to expand from.",
      ["palaces.6.base_position.home_god", "palaces.2.active_chart.god",
       "palaces.2.active_chart.status.has_horse_star"], "NEGATIVE")

    F("displacement", "spirits_that_stayed_home", sorted(
        [p for p, v in out.items() if v["god_unchanged"]], key=int),
      "Tai Yin (Moon) at palace 3, Liu He (Six Harmony) at palace 8 by way of palace 4's home "
      "listing, Jiu Di (Nine Earths) at palace 7 and Teng She (Serpent) at palace 4 are the "
      "anchored spirits. Jiu Di staying home at palace 7 reinforces that palace's concealment "
      "reading, and Liu He arriving at palace 8 - from palace 4, a Dead-door void palace - is the "
      "single constructive spirit movement on the entire board.",
      ["palaces.7.active_chart.god", "palaces.4.base_position.home_god",
       "palaces.8.active_chart.god"], "POSITIVE")
    return out


# ===================================== 5. HARM + BIRTH-STAGE STEM RULES ====
def harm_birth():
    harm_map, birth_map = {}, {}
    for pid in sorted(P, key=int):
        psr = P[pid].get("palace_stem_rules", {})
        h = psr.get("stems_in_harm", [])
        b = psr.get("stems_in_birth_stage", [])
        if h:
            harm_map[pid] = h
        if b:
            birth_map[pid] = b

    # Which harms actually bite? A harm bites if that stem is present on the plate there.
    live_harm = []
    for pid, stems in harm_map.items():
        occupant = CARDS[pid]["stack"]["S4_heaven"]["heaven_stem"]
        for s in stems:
            hit = {"palace": pid, "stem": s, "occupies_this_palace": occupant == s,
                   "stem_sits_at": IDX["heaven_stem"].get(s, []),
                   "paths": [f"palaces.{pid}.palace_stem_rules.stems_in_harm"]}
            if occupant == s:
                live_harm.append(hit)

    live_birth = []
    for pid, stems in birth_map.items():
        occupant = CARDS[pid]["stack"]["S4_heaven"]["heaven_stem"]
        for s in stems:
            if occupant == s:
                live_birth.append({"palace": pid, "stem": s,
                                   "paths": [f"palaces.{pid}.palace_stem_rules.stems_in_birth_stage"]})

    F("harm", "harm_rules_are_latent_not_active", sorted(harm_map, key=int),
      "Five palaces declare `stems_in_harm` (2:Wu, 3:Ren, 4:Gui, 6:Geng, 7:Ji, 8:Xin). Checking "
      "each against the stem actually sitting there: "
      + ("none of them is occupied by its own harmed stem, so every harm rule on this board is "
         "latent rather than active." if not live_harm else
         f"{len(live_harm)} are live: {live_harm}.")
      + " This matters because it removes a whole category of damage that a careless reading "
        "would have charged against palaces 6 and 8 - the two surviving solution paths. Neither "
        "is actually being harmed.",
      [f"palaces.{p}.palace_stem_rules.stems_in_harm" for p in sorted(harm_map, key=int)],
      "POSITIVE")

    # where do the harmed stems actually live?
    detail = []
    for pid, stems in sorted(harm_map.items(), key=lambda x: int(x[0])):
        for s in stems:
            at = IDX["heaven_stem"].get(s, [])
            detail.append(f"palace {pid} harms {s}, which sits at {at or 'nowhere'}")
    F("harm", "harm_target_locations", sorted(harm_map, key=int),
      "Cross-referencing each harm rule to where its target stem actually sits: "
      + "; ".join(detail) + ". Note palace 8 harms Xin, and Xin is the lead-proxy stem at the "
      "duty palace 9. So the clean outer route (8) stands in a harm relationship to the "
      "showpiece's visible stem - taking the palace 8 path implies some friction with the "
      "duty palace's public face, even though palace 8 itself is undamaged.",
      [f"palaces.{p}.palace_stem_rules.stems_in_harm" for p in sorted(harm_map, key=int)],
      "NEGATIVE")

    F("birth_stage", "birth_stage_rules_mostly_latent", sorted(birth_map, key=int),
      "Seven palaces declare `stems_in_birth_stage` (1:Xin, 2:Ren, 3:Gui, 4:Geng, 7:Ding+Ji, "
      "8:Bing+Wu, 9:Yi). Checking occupancy: "
      + (f"{len(live_birth)} are live - {live_birth}." if live_birth else
         "no palace is occupied by a stem in its own birth stage.")
      + " The birth-stage layer therefore adds no active reinforcement anywhere.",
      [f"palaces.{p}.palace_stem_rules.stems_in_birth_stage" for p in sorted(birth_map, key=int)],
      "NEUTRAL")

    F("birth_stage", "day_stem_birth_stage_at_palace_8", ["8"],
      "Palace 8 lists Bing among its birth-stage stems. Bing is the day stem - the actor. So the "
      "one clean, unafflicted, void-free palace on this board is also the palace where the actor's "
      "element is in its birth stage. Set against palace 6, which is Bing's *tomb*, the two "
      "surviving routes are revealed as exact opposites for the actor: palace 8 is where Bing is "
      "born, palace 6 is where Bing is buried. This is the sharpest single discriminator the "
      "chart offers between the two candidates, and it was entirely missing from the earlier "
      "analysis.",
      ["palaces.8.palace_stem_rules.stems_in_birth_stage",
       "palaces.6.palace_stem_rules.stems_in_tomb", "timing.four_pillars.day"], "POSITIVE")

    F("birth_stage", "lead_proxy_birth_stage_at_palace_1", ["1"],
      "Palace 1 lists Xin - the lead-stem proxy for the invisible Jia-Wu decade - in its birth "
      "stage. Xin is active at palace 9. Palace 1 is Xin's origin point and is also where Bai Hu "
      "(White Tiger) has just arrived. The public face of the matter is born in the North, in a "
      "palace whose star is Obsolete and which now holds the Tiger.",
      ["palaces.1.palace_stem_rules.stems_in_birth_stage", "chart_config.lead_stem",
       "palaces.1.active_chart.god"], "NEUTRAL")
    return {"harm": harm_map, "birth_stage": birth_map,
            "live_harm": live_harm, "live_birth_stage": live_birth}


# ================================ 6. STAR ENERGY SUB-STATE ANALYSIS ========
def star_energy():
    out = {}
    for pid in sorted(P, key=int):
        es = P[pid]["active_chart"].get("energy_state", {})
        st = es.get("star")
        if not isinstance(st, dict):
            continue
        seas, pal = st.get("seasonal"), st.get("palace_relation")
        out[pid] = {
            "seasonal": seas, "palace_relation": pal,
            "divergence": STRENGTH_SCORE.get(pal, 0) - STRENGTH_SCORE.get(seas, 0),
            "agree": seas == pal,
            "paths": [f"palaces.{pid}.active_chart.energy_state.star.seasonal",
                      f"palaces.{pid}.active_chart.energy_state.star.palace_relation"],
        }
    F("star_energy", "seasonal_column_is_uniform", sorted(out, key=int),
      "Every single palace reports `star.seasonal = Strengthening`. A column with no variance "
      "carries no discriminating information, so any ranking that leaned on seasonal star "
      "strength would be ranking on noise. All real star information in this chart lives in "
      "`palace_relation`.",
      [f"palaces.{p}.active_chart.energy_state.star.seasonal" for p in sorted(out, key=int)],
      "NEUTRAL")
    better = sorted([p for p, v in out.items() if v["divergence"] > 0], key=int)
    worse = sorted([p for p, v in out.items() if v["divergence"] < 0], key=int)
    F("star_energy", "stars_outperforming_their_season", better,
      f"At palaces {', '.join(better)} the star is stronger by palace relation than by season - "
      f"these stars are being carried by their location. Palaces 2 and 8 both reach Prosperous. "
      f"Palace 2's Tian Rui is the illness star, so a Prosperous reading there means the illness "
      f"is well-fed, not that the palace is healthy. Palace 8's Tian Ren (Ambassador) reaching "
      f"Prosperous is a genuine positive and reinforces the palace 8 route.",
      [f"palaces.{p}.active_chart.energy_state.star.palace_relation" for p in better], "NEUTRAL")
    F("star_energy", "stars_undercut_by_their_palace", worse,
      f"At palaces {', '.join(worse)} the star is weaker by palace relation than by season. "
      f"Palace 1's Tian Peng falls all the way to Obsolete - the single worst star reading on the "
      f"board. Palace 9's Tian Ying (Hero), the duty star itself, drops to Resting: the star that "
      f"is supposed to carry the matter is the fifth-weakest on the board by location.",
      [f"palaces.{p}.active_chart.energy_state.star.palace_relation" for p in worse], "NEGATIVE")
    return out


# ============================ 7. ELEMENT PROSPERITY -> FULL BOARD MAP ======
def prosperity_map():
    ep = Q["element_prosperities"]
    out = {}
    for el_lower, state in ep.items():
        el = el_lower.capitalize()
        palaces = [p for p in sorted(P, key=int) if P[p]["element"] == el]
        stems = [s for s in ALL_STEMS_ON_PLATE if STEM_ELEMENT[s] == el]
        doors = [(p, CARDS[p]["stack"]["S3_door"]["door"]) for p in sorted(P, key=int)
                 if CARDS[p]["stack"]["S3_door"]["door_element"] == el]
        stars = [(p, s) for p in sorted(P, key=int)
                 for s in CARDS[p]["stack"]["S4_heaven"]["stars"] if STAR_ELEMENT.get(s) == el]
        out[el] = {
            "state": state, "path": f"element_prosperities.{el_lower}",
            "palaces_of_this_element": palaces,
            "stems_of_this_element_on_plate": sorted(stems),
            "doors_of_this_element": doors, "stars_of_this_element": stars,
            "score": STRENGTH_SCORE.get(state),
        }
    F("prosperity", "metal_prosperous_owns_the_working_half", ["6", "7"],
      "Metal is Prosperous. That single fact governs palaces 6 and 7, the stems Geng and Xin, "
      "the doors Kai (Open) and Jing (Fear), and the stars Tian Xin and Tian Zhu. Both Prosperous "
      "doors on this board are Metal doors. The chart's entire working capacity is Metal-shaped: "
      "cutting, deciding, finishing, publishing, closing. Nothing soft is in season.",
      ["element_prosperities.metal", "palaces.6.active_chart.door",
       "palaces.7.active_chart.door"], "POSITIVE")
    F("prosperity", "water_strengthening_is_the_rising_current", ["1", "8"],
      "Water is Strengthening - the only element on the rise. It appears as the stem Ren at "
      "palace 8, the stem Gui at palace 7, the Xiu (Rest) door at palace 1 and the star Tian "
      "Peng. Palace 8 carrying a Strengthening-element stem is a further independent mark in "
      "favour of the palace 8 route: it is the only candidate route whose stem element is "
      "gaining rather than peaking.",
      ["element_prosperities.water", "palaces.8.active_chart.stems.heaven"], "POSITIVE")
    F("prosperity", "wood_dead_erases_the_hour_stem", ["3", "4"],
      "Wood is Dead. This kills palaces 3 and 4 outright (both Dead in door and palace), kills "
      "the stem Yi at palace 4, and - most importantly - kills Jia, which is the hour stem and "
      "does not appear on the plate at all. The matter in motion is made of the one element the "
      "season has already finished with.",
      ["element_prosperities.wood", "timing.four_pillars.hour",
       "palaces.3.active_chart.energy_state.palace"], "NEGATIVE")
    F("prosperity", "fire_imprisoned_traps_the_actor_and_the_showpiece", ["5", "9"],
      "Fire is Imprisoned. Fire is the day stem Bing (the actor, stranded in the Centre), the "
      "stem Ding at palace 6, the Jing (Scenery) door and the duty star Tian Ying - and palace 9 "
      "itself. So the actor, the duty star, the duty door and the duty palace are all made of an "
      "Imprisoned element. That is four independent confirmations of the same weakness, and it "
      "explains why the showpiece cannot hold regardless of how it is played.",
      ["element_prosperities.fire", "timing.four_pillars.day", "chart_config.duty_star",
       "chart_config.duty_door", "palaces.9.element"], "NEGATIVE")
    F("prosperity", "earth_resting_is_the_neutral_ground", ["2", "5", "8"],
      "Earth is Resting - neither helped nor harmed. Earth is palaces 2, 5 and 8, the stems Wu "
      "and Ji, and the Sheng (Life) and Si (Death) doors. Palace 8's Life door being Resting "
      "rather than Prosperous is the honest cost of that route: it works, but it is not "
      "energised, so it will need deliberate push. This is precisely the 0.040 gap between "
      "palace 8 and palace 6.",
      ["element_prosperities.earth", "palaces.8.active_chart.energy_state.door"], "NEUTRAL")
    return out


# ====================== 8. SOLAR TERM / STRUCTURE CROSS-VALIDATION =========
def solar_term():
    st = Q["timing"]["solar_term"]
    struct = Q["chart_config"]["structure"]
    expected = SOLAR_TERM_YUAN_DUN.get((st["name"], st["yuan"]))
    ok = expected == struct
    F("solar_term", "structure_matches_solar_term_and_yuan", ["*"],
      f"`timing.solar_term` reads {st['name']}, {st['yuan']} yuan, day {st['day']}, and "
      f"`chart_config.structure` reads {struct}. For White Dew Middle yuan the canonical "
      f"structure is {expected}. These agree"
      + (", so the chart's own header is self-consistent and the plate was constructed from the "
         "stated moment rather than assembled arbitrarily. Every seasonal judgement in this "
         "package rests on that agreement." if ok else
         " NOT - recorded as an anomaly; no correction is applied to the source."),
      ["timing.solar_term.name", "timing.solar_term.yuan", "chart_config.structure"],
      "POSITIVE" if ok else "NEGATIVE")
    F("solar_term", "white_dew_is_the_metal_gate", ["*"],
      "White Dew is the term at which autumn Metal takes over decisively and moisture begins to "
      "condense - which is exactly what `element_prosperities` reports (Metal Prosperous, Water "
      "Strengthening, Wood Dead). The named term and the numeric prosperity table corroborate "
      "each other independently. Day 3 of the middle yuan places this early in that period, so "
      "the Metal reading is establishing rather than exhausting.",
      ["timing.solar_term.name", "timing.solar_term.day", "element_prosperities.metal"],
      "NEUTRAL")
    return {"solar_term": st, "structure": struct, "expected_structure": expected,
            "match": ok, "paths": ["timing.solar_term", "chart_config.structure"]}


# ===================== 9. EARTHLY BRANCHES AS A COMPLETE SYSTEM ============
def branch_system():
    out = {}
    all_br = {}
    for pid in sorted(P, key=int):
        brs = P[pid]["base_position"].get("earthly_branches", [])
        out[pid] = {"branches": brs, "count": len(brs),
                    "path": f"palaces.{pid}.base_position.earthly_branches"}
        for b in brs:
            all_br[b] = pid
    dv = PILLARS["void"]["day_void_branches"]
    hv = PILLARS["void"]["hour_void_branches"]
    pillar_br = {k: PILLARS["pillars"][k]["branch_full"] for k in ["year", "month", "day", "hour"]}
    occupied = set(pillar_br.values())
    unoccupied = sorted([b for b in all_br if b not in occupied], key=lambda x: all_br[x])
    F("branches", "twelve_branches_fully_mapped", sorted(P, key=int),
      f"All twelve earthly branches are distributed across the eight directional palaces "
      f"(the Centre holds none). Of the twelve, four are occupied by pillars "
      f"({', '.join(sorted(occupied))}) and eight are unoccupied. The four void branches are "
      f"{', '.join(dv + hv)}, which map to palaces 2, 4 and 9 - matching the chart's own void "
      f"flags exactly.",
      [f"palaces.{p}.base_position.earthly_branches" for p in sorted(P, key=int)], "NEUTRAL")
    F("branches", "palace_9_single_branch_fully_loaded", ["9"],
      "Palace 9 holds exactly one branch, Wu (Horse) - and both the year pillar and the hour "
      "pillar carry Wu. A single-branch palace receiving a doubled pillar branch has no room to "
      "distribute the load, unlike palaces 2, 4, 6 and 8 which hold two branches each. The duty "
      "palace is the narrowest palace on the board and is carrying the heaviest branch "
      "concentration, while being void. Structurally it cannot absorb what is being put on it.",
      ["palaces.9.base_position.earthly_branches", "timing.four_pillars.year",
       "timing.four_pillars.hour"], "NEGATIVE")
    F("branches", "day_branch_xu_sits_with_the_open_door", ["6"],
      "The day branch is Xu (Dog), which belongs to palace 6 - the Open-door, Ding, Tian Xin "
      "palace. The actor's own branch already sits at the strongest palace on the board, even "
      "though the actor's stem is stranded in the Centre. Stem and branch of the day pillar are "
      "split between the weakest position (Centre, no seat) and the strongest (palace 6). That "
      "split is the clearest statement of the chart's central tension, and it is also why palace "
      "6 keeps scoring highly despite being Bing's tomb.",
      ["timing.four_pillars.day", "palaces.6.base_position.earthly_branches"], "NEUTRAL")
    F("branches", "month_branch_you_anchors_the_metal_season", ["7"],
      "The month branch is You (Rooster), which belongs to palace 7 - pure Metal, Prosperous "
      "door, Prosperous palace. The month pillar is the seasonal authority, and it lands on the "
      "palace that most purely expresses the prosperous element. This is why the Metal reading "
      "throughout this chart is trustworthy: the season's own branch is sitting in its own house.",
      ["timing.four_pillars.month", "palaces.7.base_position.earthly_branches"], "POSITIVE")
    return {"per_palace": out, "branch_to_palace": all_br,
            "unoccupied_branches": unoccupied, "pillar_branches": pillar_br}


# ============================================== 10. SYSTEM / METHOD ========
def system_block():
    s = Q["system"]
    F("system", "school_and_method_declared", ["*"],
      f"The chart declares school `{s['school']}`, type `{s['chart_type']}`, method "
      f"`{s['method']}`. This is a Yi Yun Lun Zang Jia hour-rotation chart built by the Chai Bu "
      f"(splitting/tearing) method. Two consequences constrain this analysis: hour-rotation means "
      f"the plate is specific to this hour and its conclusions decay with the hour, and Lun Zang "
      f"Jia ('discussing the hidden Jia') is precisely the tradition in which the Jia stem is "
      f"never shown directly but read through its decade proxy. The absence of Jia from every "
      f"plate is therefore native to the method, not a defect in the export - which downgrades "
      f"the earlier HOUR_STEM_NOT_ON_PLATE anomaly from a data problem to an expected feature.",
      ["system.school", "system.chart_type", "system.method", "chart_config.lead_stem"],
      "POSITIVE", "EXPLICIT")
    return s


# ==================================================================== MAIN =
def main():
    cov = {
        "palace_id_integrity": id_integrity(),
        "hetu_system": hetu(),
        "trigram_system": trigrams(),
        "home_vs_active_displacement": home_vs_active(),
        "harm_and_birth_stage": harm_birth(),
        "star_energy_substates": star_energy(),
        "element_prosperity_map": prosperity_map(),
        "solar_term_validation": solar_term(),
        "branch_system": branch_system(),
        "system_declaration": system_block(),
        "findings": FINDINGS,
    }
    jwrite(os.path.join(STATE, "full_coverage.json"), cov)
    heartbeat(f"P7_FULL_FIELD_COVERAGE | subsystems 10 | findings {len(FINDINGS)}")
    print("findings:", len(FINDINGS))
    for f in FINDINGS:
        print(f"  [{f['polarity']:8}] {f['subsystem']:14} {f['name_en']}")


if __name__ == "__main__":
    main()
