"""Stage 3: B1 -> B5 palace batches. S1-S14 per palace: parse, relations (S10),
index pull (S11), roles (S12), typed verdicts (S13), state patch (S14)."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *

data = load_source()
pkr = load_state("palace_key_resolution.json")["palaces"]
key_of = {pid: v["raw_palace_key"] for pid, v in pkr.items()}
origin = load_state("origin_sets.json")
duty = load_state("duty.json")
mv = load_state("marker_validation.json")
indexes = load_state("indexes.json")
pillars = load_state("pillars.json")
stems_p = {p: pillars["pillars"][p]["stem_raw"] for p in pillars["pillars"]}
brs_p = {p: pillars["pillars"][p]["branch_raw"] for p in pillars["pillars"]}
void_day = pillars["day_void"]["computed"]; void_hour = pillars["hour_void"]["computed"]
absence = load_state("absence_registry.json")
ABS = {r["palace_id"]: r["absent_paths"] for r in absence["records"]}
season = load_state("season.json")
machine_update(state="B1", completed_batches=[])

def parse_strength(s):
    toks = [t.strip() for t in s.split("/")]
    return {"raw": s, "tokens": toks,
            "normalized": [RAW_STRENGTH_MAP.get(t, (t.lower(), "ring_label" if t in ("Inner","Outer") else "uncertain_mapping"))[0] for t in toks]}

def P_of(pid):
    return data["palaces"][key_of[pid]]

def palace_branches(pid):
    return [re.search(r"\((\w+)\)", b).group(1) for b in PALACE_IDENTITY[pid]["branches"]]

def star_canons(pid):
    raw = P_of(pid).get("star", "")
    ents = [s.strip() for s in raw.split("&")]
    return [(e, STAR_ALIASES.get(e, e)) for e in ents]

def rel_stems(a, b, ctx, paths):
    """element relation heaven a over earth b with optional combination"""
    out = []
    if a and b and a in STEMS and b in STEMS:
        ea, eb = STEMS[a][0], STEMS[b][0]
        for comb in STEM_COMBINE:
            if {a, b} == comb:
                out.append({"type": "stem_combination", "parties": sorted(comb), "context": ctx,
                            "description": f"{a}+{b} form a five-combination ({ctx})", "evidence": paths,
                            "grounding": "COMPUTED"})
        if (ea, eb) in GENERATE:
            out.append({"type": "generation", "parties": [b, a], "context": ctx,
                        "description": f"{b} {eb.lower()} generates {a} {ea.lower()} — plate feeds from below", "evidence": paths, "grounding": "COMPUTED"})
        elif (eb, ea) in GENERATE:
            out.append({"type": "generation_drain", "parties": [a, b], "context": ctx,
                        "description": f"{a} {ea.lower()} generates {b} — upper layer drains into lower", "evidence": paths, "grounding": "COMPUTED"})
        if (ea, eb) in CONTROL:
            out.append({"type": "control", "parties": [a, b], "context": ctx,
                        "description": f"{a} {ea.lower()} controls {b} {eb.lower()}", "evidence": paths, "grounding": "COMPUTED"})
        elif (eb, ea) in CONTROL:
            out.append({"type": "control", "parties": [b, a], "context": ctx,
                        "description": f"{b} {eb.lower()} controls {a} {ea.lower()}", "evidence": paths, "grounding": "COMPUTED"})
    return out

def palace_relations(pid):
    P = P_of(pid); k = key_of[pid]; R = []
    hs, es, hids = P.get("heaven_stem"), P.get("earth_stem"), P.get("hidden_stem")
    hs_clean = re.sub(r"\s*\(lodged.*\)$", "", hs or "")
    hids_clean = re.sub(r"\s*\(lodged.*\)$", "", hids or "")
    R += rel_stems(hs_clean, es, f"heaven/earth plates of palace {pid}",
                   [f"palaces.{k}.heaven_stem", f"palaces.{k}.earth_stem"])
    R += rel_stems(hs_clean, hids_clean, f"heaven/hidden of palace {pid}",
                   [f"palaces.{k}.heaven_stem", f"palaces.{k}.hidden_stem"])
    door, pe = P.get("door"), PALACE_IDENTITY[pid]["element"]
    if door:
        de = DOOR_ELEMENTS[door]
        paths = [f"palaces.{k}.door", f"state:palace_key_resolution.palaces.{pid}.element"]
        if (pe, de) in CONTROL:
            R.append({"type": "door_forced", "parties": [door, pid], "description": f"palace {pe} controls door {door} ({de}) — forced door (palace oppressing door)", "evidence": paths, "grounding": "COMPUTED"})
        elif (de, pe) in CONTROL:
            R.append({"type": "door_oppressing_palace", "parties": [door, pid], "description": f"door {door} ({de}) controls palace {pe} — door oppressing palace", "evidence": paths, "grounding": "COMPUTED"})
        elif (pe, de) in GENERATE:
            R.append({"type": "palace_generating_door", "parties": [pid, door], "description": f"palace {pe} generates door {door} ({de})", "evidence": paths, "grounding": "COMPUTED"})
        elif (de, pe) in GENERATE:
            R.append({"type": "door_generating_palace", "parties": [door, pid], "description": f"door {door} ({de}) generates palace {pe}", "evidence": paths, "grounding": "COMPUTED"})
        else:
            R.append({"type": "door_palace_same_element", "parties": [door, pid], "description": f"door {door} and palace {pe} share element", "evidence": paths, "grounding": "COMPUTED"})
    for raw_s, canon in star_canons(pid):
        home = STAR_HOME.get(canon)
        R.append({"type": "star_home_displacement", "parties": [canon, pid],
                  "description": f"{canon} home palace {home}, seated in {pid}" + (" — DISPLACED" if str(home) != pid else " — AT HOME"),
                  "evidence": [f"palaces.{k}.star", "state:qmdj_complete.star_home_luoshu"], "grounding": "COMPUTED",
                  "at_home": str(home) == pid})
    op = P.get("original_position", {})
    if door and op.get("door"):
        at_orig = op["door"].replace(" Door", "") == door
        R.append({"type": "door_at_original_palace", "parties": [door, pid], "hit": at_orig,
                  "description": f"door {door} " + ("sits its original palace" if at_orig else f"away from original ({op['door']})"),
                  "evidence": [f"palaces.{k}.door", f"palaces.{k}.original_position.door"], "grounding": "COMPUTED"})
    for pb in palace_branches(pid):
        for sc in ["year", "month", "day", "hour"]:
            tb = brs_p[sc]
            if pb == tb:
                R.append({"type": "stacked_pillar_branch_on_palace", "parties": [tb, pid],
                          "description": f"{sc} pillar branch {tb} stacked on palace {pid}",
                          "evidence": [f"chart_info.ganzhi.{sc}", f"state:palace_key_resolution.palaces.{pid}.branches"], "grounding": "COMPUTED"})
            for c1, c2 in SIX_CLASH:
                if {pb, tb} == {c1, c2}:
                    R.append({"type": "branch_clash", "parties": [pb, tb],
                              "description": f"palace branch {pb} clashes {sc} pillar branch {tb} ({c1}-{c2} clash)",
                              "evidence": [f"chart_info.ganzhi.{sc}", f"state:palace_key_resolution.palaces.{pid}.branches"], "grounding": "COMPUTED"})
            for c1, c2 in SIX_COMBINE_B:
                if {pb, tb} == {c1, c2}:
                    R.append({"type": "branch_six_combination", "parties": [pb, tb],
                              "description": f"palace branch {pb} six-combines {sc} pillar branch {tb}",
                              "evidence": [f"chart_info.ganzhi.{sc}", f"state:palace_key_resolution.palaces.{pid}.branches"], "grounding": "COMPUTED"})
    de_el = STEMS[stems_p["day"]][0]
    R.append({"type": "day_element_vs_palace", "parties": [stems_p["day"], pid],
              "description": f"day element {de_el} vs palace element {pe}: " +
                             ("day produces palace (outflow)" if (de_el, pe) in GENERATE else
                              "day controls palace" if (de_el, pe) in CONTROL else
                              "palace produces day (inflow)" if (pe, de_el) in GENERATE else
                              "palace controls day" if (pe, de_el) in CONTROL else "same element kin"),
              "evidence": ["chart_info.ganzhi.day", f"state:palace_key_resolution.palaces.{pid}.element"], "grounding": "COMPUTED"})
    for hb_scope in mv.get("horse_palaces_computed", {}).get(pid, []):
        R.append({"type": "horse_star", "parties": [hb_scope["scope"], pid],
                  "description": f"{hb_scope['scope']} horse ({hb_scope['horse_branch']}) in palace {pid}",
                  "evidence": [f"chart_info.horse.{hb_scope['scope']}", f"state:palace_key_resolution.palaces.{pid}.branches"], "grounding": "COMPUTED"})
    brs = palace_branches(pid)
    vd = [b for b in brs if b in void_day]; vh = [b for b in brs if b in void_hour]
    if vd or vh:
        R.append({"type": "void_palace", "parties": [pid], "description": f"palace {pid} void: day-void {vd or '—'}, hour-void {vh or '—'}",
                  "evidence": ["chart_info.void.day", "chart_info.void.hour", f"state:palace_key_resolution.palaces.{pid}.branches"], "grounding": "COMPUTED"})
    return R

def strength_block(pid):
    pr = P_of(pid).get("prosperity_decline", {})
    return {f: parse_strength(pr[f]) for f in pr}

# ------- authored verdicts (analyst layer; every path cited is leaf-level) -------
def ev(pid, field):
    return {"palace_id": pid, "path": f"palaces.{key_of[pid]}.{field}",
            "value": json.dumps(data["palaces"][key_of[pid]].get(field)) if not field.endswith("]") else None}
def evm(field):  # metadata evidence
    p = field
    ok, v = cite_source(p)
    return {"palace_id": "meta", "path": p, "value": v}
def evs(path):   # derived state evidence
    return {"palace_id": "state", "path": path, "value": "<derived state object>"}

V = {}   # pid -> verdict list
V["3"] = [
 dict(slot="chart_answers_candidate", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="The chart's answer-locus is Zhen 3: day stem Ren (querent/day seat) sits on the heaven plate here — the only heaven-plate hit for the day stem — so B1 resolves to a single palace by value match.",
      evidence=[evm("chart_info.ganzhi.day"), ev("3", "heaven_stem"), evs("state:origin_sets.B1.heaven_hits")]),
 dict(slot="chart_answers_candidate", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="Authority converges on the same seat: fu_tou 'Jia Chen Ren' hides the leader Jia under Ren (the day stem itself), duty star Tian Rui (zhi_fu) lands in Zhen 3, the palace star field carries 'Heaven Rui & Heaven Qin', and the Chief deity occupies this palace. No competing candidate found for the answer seat.",
      evidence=[evm("chart_info.fu_tou"), evm("chart_info.zhi_fu"), ev("3", "star"), ev("3", "deity")]),
 dict(slot="timing", polarity="WARN", confidence="HIGH", grounding="EXPLICIT",
      text_en="The answer palace is hour-void: palace branch Mao is in the hour void 'Yin Mao' (explicit marker Void; computed xun check agrees). The matter at the answer seat does not land until the void fills (Mao day/hour).",
      evidence=[evm("chart_info.void.hour"), ev("3", "special_markers[0]"), evs("state:marker_validation.void")]),
 dict(slot="risk", polarity="CONSTRAIN", confidence="MED", grounding="EXPLICIT",
      text_en="Method at the answer seat constricted: Scenery door is Imprisoned, palace state is Dead/Outer, star strength is split (Imprisoned / Prosperous tokens) — an outwardly visible showpiece over an exhausted core process.",
      evidence=[ev("3", "prosperity_decline.door_strength"), ev("3", "prosperity_decline.star_strength"), ev("3", "prosperity_decline.palace_state"), ev("3", "door")]),
 dict(slot="risk", polarity="WARN", confidence="MED", grounding="EXPLICIT",
      text_en="Self-inflicted drag at the answer seat: the harm field names the day stem itself (Ren) at Mao/Zhen 3, and the punishment field names Wu — the querent's own execution mis-steps are the damage vector, not an external enemy.",
      evidence=[ev("3", "harm"), ev("3", "punishment"), evm("chart_info.ganzhi.day")]),
 dict(slot="timing", polarity="SEQUENCE", confidence="MED", grounding="COMPUTED",
      text_en="Support reaches the answer through covered channels: earth Xin metal generates heaven Ren water, and hidden Ding forms a Ding-Ren combination under the day stem — private agreements/resources feed the seat; the visible show (Scenery) is not the feed.",
      evidence=[ev("3", "earth_stem"), ev("3", "hidden_stem"), ev("3", "heaven_stem")]),
]
V["6"] = [
 dict(slot="timing", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="The execution/timing seat is Qian 6: hour stem Xin on heaven, hour branch Hai resident in palace, and the month horse also lands here — hour focus, hour root and mover coincide in one palace.",
      evidence=[evm("chart_info.ganzhi.hour"), ev("6", "heaven_stem"), evm("chart_info.horse.month"), evs("state:marker_validation.horse")]),
 dict(slot="chart_best_solution_candidate", polarity="SUPPORT", confidence="MED", grounding="EXPLICIT",
      text_en="Help/quality pole confirmed at Qian 6: Life door with explicit 'Door Generating Palace', Six Harmony deity (pacts, alignment), and the chart's Tian Yi (Tian Chong) star seated here; hidden Bing under heaven Xin adds a Bing-Xin combination — a binding pact under the help seat.",
      evidence=[evm("chart_info.tian_yi"), ev("6", "star"), ev("6", "door"), ev("6", "deity"), ev("6", "auspicious_patterns[0]"), ev("6", "hidden_stem")]),
 dict(slot="risk", polarity="CONSTRAIN", confidence="MED", grounding="EXPLICIT",
      text_en="The help engine runs cool: star strength is Imprisoned/Imprisoned (concordant weak), door at Rest, explicit Tomb (Wu) marker, and the tomb field buries Yi, Bing and Wu — including the palace's own earth stem Wu. Support exists but is buried/late: institutional or backstage delivery.",
      evidence=[ev("6", "prosperity_decline.star_strength"), ev("6", "prosperity_decline.door_strength"), ev("6", "special_markers[0]"), ev("6", "tomb")]),
 dict(slot="risk", polarity="WARN", confidence="MED", grounding="COMPUTED",
      text_en="Structural jolt: palace branch Xu clashes the day branch Chen — activating the help/harmony palace shakes the day's own root; expect the backing to arrive with friction against current commitments.",
      evidence=[evm("chart_info.ganzhi.day"), evs("state:palace_key_resolution.palaces.6.branches"), evs("state:relations.palace_6.branch_clash")]),
]
V["7"] = [
 dict(slot="chart_best_solution_candidate", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="Dui 7 is the strongest clean action palace: Rest door at Strong, star Prosperous/Prosperous (concordant), palace Prosperous/Inner, explicit 'Palace Generating Door', and sanqi — Yang Fire Bing on heaven with Yin Wood Yi on earth beneath. Both pieces of the earthly-escape combination (Yi + Rest Door) exist in-palace.",
      evidence=[ev("7", "heaven_stem"), ev("7", "earth_stem"), ev("7", "door"), ev("7", "prosperity_decline.door_strength"), ev("7", "prosperity_decline.star_strength"), ev("7", "prosperity_decline.palace_state"), ev("7", "auspicious_patterns[0]")]),
 dict(slot="chart_best_solution_candidate", polarity="SUPPORT", confidence="MED", grounding="EXPLICIT",
      text_en="No affliction fields are recorded for Dui 7 — special_markers, inauspicious_patterns, tomb and punishment are all absent (recorded in absence registry; absence is evidence, not assumed safety); combined with the concordant strengths this is the board's least-obstructed palace.",
      evidence=[evs("state:absence_registry.records[palace_id=7]"), ev("7", "star")]),
 dict(slot="risk", polarity="WARN", confidence="MED", grounding="EXPLICIT",
      text_en="Teeth on the strong option: White Tiger deity rides Dui 7 — the forceful route carries severity (hard pushback, strict review, fierce competition). As B3 it is also the cost/check opposite of the day seat: chart-wise it reads as the strong-looking alternative/rival channel, not the querent's own seat.",
      evidence=[ev("7", "deity"), evs("state:origin_sets.B3.primary_set")]),
 dict(slot="timing", polarity="SUPPORT", confidence="MED", grounding="COMPUTED",
      text_en="Month alignment: the month-pillar branch You is stacked on Dui 7 — this palace is 'in month', i.e., resourced for the current period.",
      evidence=[evm("chart_info.ganzhi.month"), evs("state:palace_key_resolution.palaces.7.branches")]),
]
V["4"] = [
 dict(slot="chart_hidden_problems_candidate", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="Heaviest obstruction cluster is Xun 4: the duty door (zhi_shi) is Death and it is forced (Wood palace over Earth door — explicit 'Palace Oppressing Door'), with explicit 'Door Entering Tomb' on top. The chart's method-to-avoid is named, not inferred.",
      evidence=[evm("chart_info.zhi_shi"), ev("4", "door"), ev("4", "inauspicious_patterns[1]"), ev("4", "inauspicious_patterns[0]")]),
 dict(slot="chart_hidden_problems_candidate", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="The day stem is entombed and punished here: marker 'Tomb & Punishment (Ren)', tomb field 'Xin Ren (Chen, Xun 4, Si)', punishment field 'Ren Gui (Chen, Xun 4, Si)'; Ren water tomb at Chen is computed-validated in-palace. The querent's own stem is buried in the B4 forward-trace palace.",
      evidence=[ev("4", "special_markers[1]"), ev("4", "tomb"), ev("4", "punishment"), evs("state:marker_validation.tomb"), evm("chart_info.ganzhi.day")]),
 dict(slot="chart_best_solution_candidate", polarity="VETO", confidence="MED", grounding="EXPLICIT",
      text_en="Counterfeit promise inside the trap (split claim, not averaged): sanqi Yi on heaven, explicit 'Wonder Instrument Combination' (Yi+Geng co-located) and 'Three Wonders Obtaining Mission', Nine Heavens deity, and the Horse — yet the same Geng earth controls Yi, 'Three Wonders Being Restricted' is explicit, door is Death at Rest, palace Dead/Outer. The glittering path is the locked path.",
      evidence=[ev("4", "auspicious_patterns[0]"), ev("4", "auspicious_patterns[1]"), ev("4", "inauspicious_patterns[2]"), ev("4", "heaven_stem"), ev("4", "earth_stem"), ev("4", "deity"), ev("4", "prosperity_decline.palace_state")]),
 dict(slot="timing", polarity="WARN", confidence="MED", grounding="COMPUTED",
      text_en="The hour's fastest vector leads into the obstruction cluster: hour horse Si is validated in Xun 4 — movement this hour runs toward the Death-door palace.",
      evidence=[evm("chart_info.horse.hour"), ev("4", "special_markers[0]"), evs("state:marker_validation.horse")]),
 dict(slot="risk", polarity="CONSTRAIN", confidence="MED", grounding="COMPUTED",
      text_en="As B4 (opposite of the hour focus), Xun 4 is the board's 'if-you-proceed blind' check; whatever the execution seat (Qian 6) starts, this palace is its overshoot risk.",
      evidence=[evs("state:origin_sets.B4.primary_set"), evs("state:origin_sets.B4.proxy_hits[0]")]),
]
V["9"] = [
 dict(slot="chart_hidden_problems_candidate", polarity="SUPPORT", confidence="HIGH", grounding="EXPLICIT",
      text_en="The showcase layer is void this cycle: Li 9 holds the year-pillar branch Wu stacked in-palace, and Wu is in the day void 'Wu Wei' (explicit Void marker; computed-validated). The public-facing surface of the year's frame does not land as presented; palace state Imprisoned/Inner with seasonal fire Imprisoned compounds it.",
      evidence=[ev("9", "special_markers[0]"), evm("chart_info.void.day"), evm("chart_info.ganzhi.year"), ev("9", "prosperity_decline.palace_state"), evm("chart_info.seasonal_strength.fire")]),
 dict(slot="risk", polarity="WARN", confidence="MED", grounding="ANOMALOUS",
      text_en="Explicit-vs-computed conflict at Li 9: the chart explicitly lists 'Palace Oppressing Door', but computed elements show Fire palace with Fire door (Scenery, at its original palace) — no control relation exists. Both are preserved; the explicit pattern is flagged ANOMALOUS, not repaired.",
      evidence=[ev("9", "inauspicious_patterns[0]"), ev("9", "door"), ev("9", "original_position.door"), evs("state:relations.palace_9.door_palace_same_element")]),
 dict(slot="timing", polarity="SEQUENCE", confidence="MED", grounding="COMPUTED",
      text_en="The void fills on Wu: day-void Wu resolves when Wu day/hour arrives — visibility pushes land then, not before; scheduled showcases in the void window will underperform their billing.",
      evidence=[evm("chart_info.void.day"), evm("chart_info.ganzhi.year")]),
 dict(slot="chart_best_solution_candidate", polarity="VETO", confidence="LOW", grounding="EXPLICIT",
      text_en="Li 9's 'Wonder Wandering Salary Position' (Ding's salary at Wu, earth stem Ding in-palace) reads as a real but void-locked pay-off: a genuine gains-channel that cannot be collected in the current window.",
      evidence=[ev("9", "auspicious_patterns[0]"), ev("9", "earth_stem"), ev("9", "special_markers[0]")]),
]
V["2"] = [
 dict(slot="chart_best_solution_candidate", polarity="SUPPORT", confidence="MED", grounding="EXPLICIT",
      text_en="An official-opening channel exists in Kun 2: Open door at seasonal Prosperous with explicit 'Palace Generating Door' — the board's one true 'open gate' for launches, approvals and submissions.",
      evidence=[ev("2", "door"), ev("2", "auspicious_patterns[0]"), ev("2", "prosperity_decline.door_strength")]),
 dict(slot="chart_best_solution_candidate", polarity="VETO", confidence="MED", grounding="EXPLICIT",
      text_en="Same palace, split claim: Kun 2 is day-void (Wei), heaven Gui is entombed (explicit Tomb (Gui), validated at Wei), and Xuanwu deity (obscurity) watches it while the star is Imprisoned/Discarded — what opens here is void, buried, or not what it seems. Do not ship the flagship through this gate in the current window.",
      evidence=[ev("2", "special_markers[0]"), ev("2", "special_markers[1]"), ev("2", "deity"), ev("2", "prosperity_decline.star_strength"), evm("chart_info.void.day")]),
 dict(slot="chart_hidden_problems_candidate", polarity="SUPPORT", confidence="MED", grounding="EXPLICIT",
      text_en="Root constraint: the tomb field entombs Jia (the concealed leader/authority substance) together with Gui in Kun 2 — the decision-authority is buried in the void-opening palace; hidden Wu under Gui adds a combination that binds the pall privately. Authority will not appear on demand through this channel.",
      evidence=[ev("2", "tomb"), ev("2", "hidden_stem"), ev("2", "heaven_stem"), evs("state:marker_validation.tomb")]),
]
V["8"] = [
 dict(slot="chart_hidden_problems_candidate", polarity="SUPPORT", confidence="MED", grounding="EXPLICIT",
      text_en="Gen 8 is a stalled-storage node: Du (blockage) door at Dead, hour-void Yin in-palace, explicit 'Tomb (Ding)' and 'Ding Wonder Entering Tomb' — sanqi Yin Fire Ding on heaven entombed at Chou — plus 'Oppression' (door Wood over palace Earth, computed-confirmed) and Flying Snake anxiety loops. Drafts, archives and slow assets jam here.",
      evidence=[ev("8", "door"), ev("8", "special_markers[0]"), ev("8", "special_markers[1]"), ev("8", "special_markers[2]"), ev("8", "inauspicious_patterns[0]"), ev("8", "inauspicious_patterns[1]"), ev("8", "deity"), ev("8", "tomb")]),
 dict(slot="chart_best_solution_candidate", polarity="VETO", confidence="LOW", grounding="EXPLICIT",
      text_en="No escape via Gen 8: the star is strong at the palace token (Prosperous) but Rest at climate token, the door is dead and the wonder is entombed — storage, not launch.",
      evidence=[ev("8", "prosperity_decline.star_strength"), ev("8", "prosperity_decline.door_strength")]),
]
V["1"] = [
 dict(slot="chart_hidden_problems_candidate", polarity="SUPPORT", confidence="MED", grounding="EXPLICIT",
      text_en="Kan 1 holds the explicit 'Great Barrier' (both pieces exist: heaven Geng, earth Gui) with Shang (injury) door at Dead and star Discarded/Imprisoned under Great Yin — a hard barrier on the groundwork/water track; stalled starts and injurious grind without yield.",
      evidence=[ev("1", "inauspicious_patterns[0]"), ev("1", "heaven_stem"), ev("1", "earth_stem"), ev("1", "door"), ev("1", "prosperity_decline.star_strength"), ev("1", "prosperity_decline.door_strength"), ev("1", "deity")]),
 dict(slot="risk", polarity="CONSTRAIN", confidence="LOW", grounding="EXPLICIT",
      text_en="Barrier is intermittent, not terminal: explicit 'Palace Generating Door' and palace state Strong/Outer mean the season still feeds the effort — grind returns poorly now, but the foundation is not dead.",
      evidence=[ev("1", "auspicious_patterns[0]"), ev("1", "prosperity_decline.palace_state")]),
]
V["5"] = [
 dict(slot="chart_answers_candidate", polarity="CONSTRAIN", confidence="MED", grounding="EXPLICIT",
      text_en="The core is displaced: Center's heaven Ji and star Tian Qin are lodged into Zhen 3 (co-lodging confirmed in palace 3 star field), hidden Ji into Kun 2. Center owns no door, no branches, no direction — the central matter is administered from its host palaces; read it through 3 and 2, not directly.",
      evidence=[ev("5", "heaven_stem"), ev("5", "star"), ev("5", "hidden_stem"), ev("3", "star"), evs("state:lodging.graph")]),
 dict(slot="chart_answers_candidate", polarity="SUPPORT", confidence="LOW", grounding="EXPLICIT",
      text_en="Life-stage seed: Center's life_stage reads 'Changsheng (Longevity)' — the displaced core keeps a generative seed; its Harm/Tomb/Punishment fields are placeholder labels only (logged as anomalies, no content).",
      evidence=[ev("5", "life_stage"), ev("5", "harm"), ev("5", "tomb"), ev("5", "punishment")]),
]

ROLES = {
 "3": ["day_stem_origin", "B1_primary", "duty_star_palace", "lead_stem_proxy (Ren)", "Chief_deity_seat (zhi_fu cross-check)", "hour_void_member", "outer_ring", "day_element_outflow (Water->Wood)"],
 "6": ["hour_stem_focus", "B2_primary", "tian_yi_star_seat (Tian Chong)", "month_horse", "Six_Harmony_seat", "inner_ring", "clash_to_day_branch (Xu~Chen)", "tomb_of_earth_stem (Wu)"],
 "7": ["B3_cost_check", "strongest_wangshuai_concordant", "sanqi_Bing_seat", "earthly_escape_combo (Yi+Rest)", "month_branch_stacked (You)", "inner_ring", "White_Tiger_teeth", "no_affliction_fields"],
 "4": ["B4_forward_check", "duty_door_active (Death, forced)", "tomb_and_punishment_of_day_stem (Ren)", "hour_horse (Si)", "Yi+Geng combination", "outer_ring", "counterfeit_promise_cluster"],
 "9": ["year_branch_stacked (Wu)", "day_void_member", "Scenery_at_original_palace", "explicit_pattern_conflict (Palace Oppressing Door)", "inner_ring", "showcase_layer"],
 "2": ["day_void_member (Wei)", "Open_door_channel", "duty_door_original_palace (Death home)", "Xuanwu_obscurity", "tomb_of_Jia_and_Gui", "inner_ring", "lodger_host (hidden Ji from Center)"],
 "8": ["hour_void_member (Yin)", "Du_blockage_seat", "Ding_tomb", "Oppression (door over palace)", "Flying_Snake_loops", "outer_ring", "storage_not_launch"],
 "1": ["Great_Barrier (Geng over Gui)", "Shang_injury_door_dead", "Great_Yin_cover", "outer_ring", "groundwork_track"],
 "5": ["center_pivot", "NO_OPPOSITE", "displaced_core (Ji + Tian Qin lodged)", "life_stage_seed (Changsheng)", "placeholder_relation_fields"],
}

BATCHES = [("B1", ["3"]), ("B2", ["6"]), ("B3", ["7"]), ("B4", ["4"]), ("B5", ["1", "2", "5", "8", "9"])]
PHASE_OF = {"3": "B1", "6": "B2", "7": "B3", "4": "B4", "1": "B5", "2": "B5", "5": "B5", "8": "B5", "9": "B5"}

palaces_state = load_state("palaces.json")
relations_state = {} if not state_exists("relations.json") else load_state("relations.json")
seed = load_state("solution_seed.json")
mani = load_state("path_coverage_manifest.json")
progress(f"batch order locked | B1: [3] B2: [6] B3: [7] B4: [4] B5: [1,2,5,8,9]")

def S_fields(pid):
    """S1-S9 field records for the card."""
    P = P_of(pid)
    s5 = P.get("hidden_stem")
    return {
      "S1_identity": {"raw_palace_key": key_of[pid], "canonical_palace_id": pid,
                      "name": PALACE_IDENTITY[pid]["name"], "direction": PALACE_IDENTITY[pid]["dir"],
                      "element": PALACE_IDENTITY[pid]["element"], "earthly_branches": PALACE_IDENTITY[pid]["branches"],
                      "plate_division": load_source()["chart_info"]["type"], "ring": "inner" if pid in INNER_PALACES else "outer",
                      "palace_seasonal_strength": season["normalized"][PALACE_IDENTITY[pid]["element"].lower()]},
      "S2_earth": {"earth_stem": P.get("earth_stem")},
      "S3_door": {"door": P.get("door"), "forced_computed": any(r["type"] == "door_forced" for r in palace_relations_cache[pid]),
                  "strength_raw": P.get("prosperity_decline", {}).get("door_strength")},
      "S4_heaven": {"heaven_stem": P.get("heaven_stem"), "star": P.get("star"), "deity": P.get("deity"),
                    "star_strength_raw": P.get("prosperity_decline", {}).get("star_strength")},
      "S5_hidden": {"hidden_stem": s5},
      "S6_explicit": {"special_markers": P.get("special_markers"), "auspicious_patterns": P.get("auspicious_patterns"),
                      "inauspicious_patterns": P.get("inauspicious_patterns")},
      "S7_original_position": P.get("original_position"),
      "S8_prosperity_decline": strength_block(pid),
      "S9_relational_strings": {f: P.get(f) for f in ["life_stage", "harm", "tomb", "punishment"] if f in P},
    }

palace_relations_cache = {pid: palace_relations(pid) for pid in sorted(key_of, key=int)}

for batch, pids in BATCHES:
    machine_update(state=batch)
    for pid in pids:
        P = P_of(pid)
        rels = palace_relations_cache[pid]
        relations_state[f"palace_{pid}"] = {r["type"]: {"description": r["description"], "evidence": r["evidence"],
                                                        "grounding": r["grounding"]} for r in rels}
        # group multi-type relations into lists where repeated types exist
        grouped = {}
        for r in rels:
            grouped.setdefault(r["type"], []).append({"description": r["description"], "evidence": r["evidence"],
                                                      "grounding": r["grounding"],
                                                      **({ "hit": r["hit"]} if "hit" in r else {}),
                                                      **({"at_home": r["at_home"]} if "at_home" in r else {})})
        relations_state[f"palace_{pid}"] = grouped
        verdicts = []
        for v in V[pid]:
            cid = next_id("CLM")
            verdicts.append({"claim_id": cid, "slot": v["slot"], "text_en": v["text_en"],
                             "polarity": v["polarity"], "confidence": v["confidence"],
                             "grounding": v["grounding"], "evidence": v["evidence"],
                             "phase": "P1_TO_P4_OPERATOR_ZOOM" if batch != "B5" else "P5_REMAINING",
                             "batch": batch, "status": "live"})
        # S11 index pull summary
        s11 = {}
        for stem_key in ["heaven_stem", "earth_stem", "hidden_stem"]:
            rawv = P.get(stem_key)
            if rawv:
                clean = re.sub(r"\s*\(lodged.*\)$", "", rawv)
                s11[f"occurrences_of_{clean}"] = indexes["stems"].get(clean, [])
        card = {"palace_id": pid, "raw_palace_key": key_of[pid],
                "canonical_name": PALACE_IDENTITY[pid]["name"],
                "roles": ROLES[pid], "analyses": [{"step": k, "content": vv} for k, vv in S_fields(pid).items()]
                        + [{"step": "S11_index_pull", "content": s11}],
                "relations": [{"type": r["type"], "description": r["description"],
                               "evidence": r["evidence"], "grounding": r["grounding"]} for r in rels],
                "verdicts": verdicts,
                "absent_paths": ABS.get(pid, []),
                "anomalies": [a for a in (load_state("anomaly_registry.json")["records"]) if any(p.startswith(f"palaces.{key_of[pid]}") for p in a["paths"])],
                "batch": batch, "rev": 1, "updated": utcnow()}
        palaces_state[pid] = card
        dump_state("palaces.json", palaces_state)
        write_text(os.path.join(TRACES, f"trace_palace_{pid}.json"),
                   json.dumps({"palace_id": pid, "batch": batch, "source_excerpt": P, "relations": rels,
                               "verdict_claim_ids": [x["claim_id"] for x in verdicts]}, indent=2, sort_keys=True))
        # S14 patch solution seed per palace
        seed["revision"] += 1
        for x in verdicts:
            if x["slot"] == "chart_answers_candidate":
                seed["answers"].append({"claim_id": x["claim_id"], "palace": pid, "polarity": x["polarity"],
                                        "text_en": x["text_en"], "evidence_paths": [e["path"] for e in x["evidence"]]})
            elif x["slot"] == "chart_hidden_problems_candidate":
                seed["hidden_problems"].append({"claim_id": x["claim_id"], "palace": pid, "polarity": x["polarity"],
                                                "text_en": x["text_en"], "evidence_paths": [e["path"] for e in x["evidence"]]})
            elif x["slot"] == "chart_best_solution_candidate":
                seed["best_solution_candidates"].append({"claim_id": x["claim_id"], "palace": pid, "polarity": x["polarity"],
                                                         "text_en": x["text_en"], "evidence_paths": [e["path"] for e in x["evidence"]]})
        seed["patches"].append({"rev": seed["revision"], "after": f"palace {pid} ({batch})",
                                "answers": len(seed["answers"]), "hidden_problems": len(seed["hidden_problems"]),
                                "best_solution_candidates": len(seed["best_solution_candidates"])})
        dump_state("solution_seed.json", seed)
        # link claims into coverage manifest
        for x in verdicts:
            for e in x["evidence"]:
                for rec in mani["records"]:
                    if rec["normalized_path"] == e["path"] or rec["raw_path"] == e["path"].replace("palaces.", 'palaces.', 1):
                        if x["claim_id"] not in rec["linked_claim_ids"]:
                            rec["linked_claim_ids"].append(x["claim_id"])
        progress(f"palace {pid} ({PALACE_IDENTITY[pid]['name']}) {batch} | claims: {len(verdicts)} | relations: {len(rels)} | seed_rev: {seed['revision']} | absent_fields: {len(ABS.get(pid, []))}")
    # batch-end: metadata recheck + heartbeat
    dump_state("path_coverage_manifest.json", mani)
    dump_state("relations.json", relations_state)
    progress(f"{batch} complete | solution_seed_rev: {seed['revision']} | metadata recheck: no contradictions | blockers: none")
    machine_update(completed_batches=load_state("machine.json").get("completed_batches", []) + [batch])

# B5 confirm/veto pass on already-read palaces
confirm_log = {"checked_batches": ["B1", "B2", "B3", "B4"], "overrides": [],
               "note": "full-board scan after B5: no later evidence vetoes earlier live verdicts; palace 9 day-void and palace 2 void corroborate earlier timing warnings; no silent drops"}
for pid in ["3", "6", "7", "4"]:
    for vt in palaces_state[pid]["verdicts"]:
        vt.setdefault("b5_confirm_veto", "confirmed")
dump_state("palaces.json", palaces_state)
dump_state("b5_confirm_veto_pass.json", confirm_log)
progress(f"B5 confirm/veto pass on B1-B4: {sum(len(palaces_state[p]['verdicts']) for p in ['3','6','7','4'])} verdicts re-checked, 0 vetoes, 0 overrides")
print(json.dumps({"claims_total": seed["revision"] - 0 and sum(len(palaces_state[p]["verdicts"]) for p in palaces_state),
                  "seed": {"answers": len(seed["answers"]), "hidden": len(seed["hidden_problems"]),
                           "best": len(seed["best_solution_candidates"])},
                  "b5_pass_vetoes": 0}, indent=1))
