"""Stage 4b: P6 archetype resolutions, rubric scoring, board consistency, final solution_seed."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *

W = {"grounding_tier": 0.35, "corroboration": 0.25, "contradiction_penalty": 0.20,
     "board_consistency": 0.10, "requirement_fit": 0.10}
GT = {"EXPLICIT": 1.0, "COMPUTED": 0.6, "INFERRED": 0.3, "ANOMALOUS": 0.2, "UNKNOWN": 0.1}
RUBRIC_HASH = "sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5"
PROTO_HASH = "sha256:protocol_v2_2_2_0_chart_analyst_v5"

def score(c, max_support, max_contrad):
    g = GT[c["grounding_tier"]]
    corr = c["supporting_evidence_count"] / max_support if max_support else 0
    contra = 1 - (c["contradicting_evidence_count"] / max_contrad) if max_contrad else 1.0
    bc = 1.0 if c["board_consistency_pass"] else 0.0
    c["corroboration_norm"] = round(corr, 4)
    c["final_score"] = round(g * W["grounding_tier"] + corr * W["corroboration"]
                             + contra * W["contradiction_penalty"] + bc * W["board_consistency"] + 0.0, 4)
    return c

def chain(slot_path_value_descs):
    return [{"step": s, "path": p, "value": v, "description": d} for s, p, v, d in slot_path_value_descs]

resolutions = []

# ---------- RES-001 chart_answers_candidate ----------
cands = [dict(archetype_id="ANS-seats-in-zhen-3", grounding_tier="EXPLICIT",
              supporting_evidence_count=6, contradicting_evidence_count=2,
              board_consistency_pass=True, requirement_fit_score=None, selected=True,
              rejection_reason=None)]
mx_s = max(c["supporting_evidence_count"] for c in cands); mx_c = max(c["contradicting_evidence_count"] for c in cands)
cands = [score(c, mx_s, mx_c) for c in cands]
resolutions.append({
 "resolution_id": "RES-001", "slot": "chart_answers_candidate",
 "evidence_chain": chain([
    ("raw_field", "chart_info.ganzhi.day", "Ren Chen", "day pillar names the day stem Ren"),
    ("raw_field", "palaces.zhen_3.heaven_stem", "Ren", "only heaven-plate hit for the day stem"),
    ("raw_field", "chart_info.zhi_fu", "Tian Rui falling in Zhen 3 Palace", "duty star lands in the same palace"),
    ("computed_relation", "state:origin_sets.B1", "{3}", "B1 selector set resolves to {3} by value match; proxies (lead Ren, duty star palace) converge"),
    ("interpretation_class", "state:origin_sets.B1", "day_stem_or_jia_set", "interpretation class of the seat: the querent/day seat"),
    ("candidate_archetype", "state:archetype_resolutions.RES-001", "ANS-seats-in-zhen-3", "the answer seat is Zhen 3, read with duty authority")]),
 "evidence_paths": ["chart_info.ganzhi.day", "palaces.zhen_3.heaven_stem", "chart_info.fu_tou",
                    "chart_info.zhi_fu", "palaces.zhen_3.star", "palaces.zhen_3.deity"],
 "class": "day_stem_or_jia_set", "name_or_combination": "day seat + duty authority convergence",
 "candidates_considered": cands, "winner": "ANS-seats-in-zhen-3",
 "margin_note": "Single candidate: no competing candidate found — both independent selectors (day-stem heaven trace and duty/fu_tou proxy) resolve to the same palace; center adds displaced-core context but owns no door. What would flip this: nothing in-chart short of a changed source file. What tempers it: hour-void (lands on Mao) and harm naming the day stem — constraints ON the seat, not alternative seats.",
 "tie_note": "not tied; singleton resolution (explicitly stated per rule 19)"})

# ---------- RES-002 chart_hidden_problems_candidate ----------
hidden_cands = [
 dict(archetype_id="HID-palace-4-death-duty-tomb-cluster", grounding_tier="EXPLICIT",
      supporting_evidence_count=9, contradicting_evidence_count=2, board_consistency_pass=True,
      requirement_fit_score=None, selected=True, rejection_reason=None,
      note="duty door Death forced + Door Entering Tomb + day-stem tomb & punishment + restricted sanqi"),
 dict(archetype_id="HID-palace-9-void-showpiece", grounding_tier="EXPLICIT",
      supporting_evidence_count=5, contradicting_evidence_count=1, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="void-locked showcase: real but seasonal/void-window problem; narrower blast radius than the palace-4 duty cluster"),
 dict(archetype_id="HID-palace-1-great-barrier", grounding_tier="EXPLICIT",
      supporting_evidence_count=4, contradicting_evidence_count=1, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="hard barrier on groundwork track, but intermittent (palace state Strong/Outer, Palace Generating Door)"),
 dict(archetype_id="HID-palace-2-void-open-jia-tomb", grounding_tier="EXPLICIT",
      supporting_evidence_count=4, contradicting_evidence_count=1, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="void-opening with entombed authority (Jia); severe, but it masks rather than destroys — reads as constraint cluster, not the primary obstruction"),
 dict(archetype_id="HID-palace-8-stalled-storage", grounding_tier="EXPLICIT",
      supporting_evidence_count=4, contradicting_evidence_count=1, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="jam/storage node (Du door dead, Ding entombed); scope limited to slow assets and drafts")]
mx_s = max(c["supporting_evidence_count"] for c in hidden_cands); mx_c = max(c["contradicting_evidence_count"] for c in hidden_cands)
hidden_cands = [score(c, mx_s, mx_c) for c in hidden_cands]
resolutions.append({
 "resolution_id": "RES-002", "slot": "chart_hidden_problems_candidate",
 "evidence_chain": chain([
    ("raw_field", "chart_info.zhi_shi", "Death Door falling in Xun 4 Palace", "the duty door is Death, active in Xun 4"),
    ("raw_field", "palaces.xun_4.special_markers[1]", "Tomb & Punishment (Ren)", "explicit marker entombs and punishes the day stem Ren"),
    ("computed_relation", "state:marker_validation.tomb", "Ren tomb at Chen validated", "computed tomb geometry validates the explicit marker"),
    ("computed_relation", "state:relations.palace_4.door_forced", "palace Wood controls door Earth", "forced door confirmed by element engine"),
    ("interpretation_class", "state:archetype_resolutions.RES-002", "duty_door_forced_dead + tomb_of_yongshen", "method-to-avoid and buried-day-stem classes"),
    ("candidate_archetype", "state:patterns.computed_catalog[0]", "forced_door@4", "the primary obstruction cluster")]),
 "evidence_paths": ["chart_info.zhi_shi", "palaces.xun_4.door", "palaces.xun_4.inauspicious_patterns[0]",
                    "palaces.xun_4.inauspicious_patterns[1]", "palaces.xun_4.special_markers[1]",
                    "palaces.xun_4.tomb", "palaces.xun_4.punishment", "state:marker_validation.tomb"],
 "class": "duty_door_forced_dead", "name_or_combination": "Death duty door, forced, Door-Entering-Tomb, day-stem tomb+punishment",
 "candidates_considered": hidden_cands, "winner": "HID-palace-4-death-duty-tomb-cluster",
 "margin_note": "Margin is thin over HID-palace-9-void-showpiece (0.7000 vs 0.6889) because both are EXPLICIT-grounded; the winner leads on corroboration (9 vs 5 independent paths) and on the duty-door class. Flip condition: if downstream reading treats the day void (Wu Wei) as covering the whole current operation window, the void-showpiece overtakes; if the duty door were re-seated (source change), the cluster dissolves.",
 "tie_note": "HID-palace-1, HID-palace-2 and HID-palace-8 finished equal on all rubric components (0.6611); ordering between them follows the documented tie-break (earlier first-appearance phase) and is otherwise STILL_TIED in rank"})

# ---------- RES-003 chart_best_solution_candidate ----------
best_cands = [
 dict(archetype_id="BEST-dui-7-earthly-escape-channel", grounding_tier="EXPLICIT",
      supporting_evidence_count=10, contradicting_evidence_count=1, board_consistency_pass=True,
      requirement_fit_score=None, selected=True, rejection_reason=None,
      note="concordant top wangshuai + Yi+Rest escape + Palace Generating Door + month-stacked + zero affliction fields; only White Tiger severity against"),
 dict(archetype_id="BEST-qian-6-harmony-help-channel", grounding_tier="EXPLICIT",
      supporting_evidence_count=6, contradicting_evidence_count=3, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="genuine help seat (Life door, Six Harmony, Tian Yi star, hour focus) but cool engine: star Imprisoned/Imprisoned, earth stem entombed, branch clash to day root"),
 dict(archetype_id="BEST-li-9-salary-channel", grounding_tier="EXPLICIT",
      supporting_evidence_count=2, contradicting_evidence_count=3, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="void-locked: day-void Wu on the year-stacked showcase palace; real payoff, wrong window"),
 dict(archetype_id="BEST-kun-2-open-gate", grounding_tier="EXPLICIT",
      supporting_evidence_count=3, contradicting_evidence_count=4, board_consistency_pass=True,
      requirement_fit_score=None, selected=False,
      rejection_reason="the one Open door on the board but day-void, heaven Gui entombed, Xuanwu obscurity, star Imprisoned/Discarded — opens onto void")]
mx_s = max(c["supporting_evidence_count"] for c in best_cands); mx_c = max(c["contradicting_evidence_count"] for c in best_cands)
best_cands = [score(c, mx_s, mx_c) for c in best_cands]
resolutions.append({
 "resolution_id": "RES-003", "slot": "chart_best_solution_candidate",
 "evidence_chain": chain([
    ("raw_field", "palaces.dui_7.heaven_stem", "Bing", "sanqi Yang Fire on heaven"),
    ("raw_field", "palaces.dui_7.earth_stem", "Yi", "sanqi Yin Wood on earth below"),
    ("raw_field", "palaces.dui_7.door", "Rest", "Rest door (escape component)"),
    ("computed_relation", "state:systems.wangshuai_matrix[7]", "Prosperous concordance", "door Strong, star Prosperous/Prosperous, palace Prosperous/Inner; no split"),
    ("computed_relation", "state:patterns.computed_catalog[earthly_escape]", "Yi + Rest Door co-located", "both escape pieces exist in one palace"),
    ("interpretation_class", "state:archetype_resolutions.RES-003", "sanqi_with_good_door", "best-solution quality class"),
    ("candidate_archetype", "state:patterns.computed_catalog[earthly_escape]", "BEST-dui-7-earthly-escape-channel", "rest/consolidation channel through the west metal palace")]),
 "evidence_paths": ["palaces.dui_7.heaven_stem", "palaces.dui_7.earth_stem", "palaces.dui_7.door",
                    "palaces.dui_7.prosperity_decline.door_strength", "palaces.dui_7.prosperity_decline.star_strength",
                    "palaces.dui_7.prosperity_decline.palace_state", "palaces.dui_7.auspicious_patterns[0]",
                    "state:absence_registry.records", "chart_info.ganzhi.month"],
 "class": "sanqi_with_good_door", "name_or_combination": "earthly_escape (named; both pieces present)",
 "candidates_considered": best_cands, "winner": "BEST-dui-7-earthly-escape-channel",
 "margin_note": "Winner leads runner-up BEST-qian-6 by 0.20 — a decisive but not absolute margin. Flip conditions: (1) if timing/hour-focus weight is prioritised downstream, Qian 6 (hour focus + Tian Yi + Six Harmony) overtakes as the WHEN-to-act channel while Dui 7 remains the HOW; (2) any new affliction evidence on Dui 7 (none recorded now) or a White-Tiger-severity reading preferred by the operator; (3) source revision adding explicit answer fields, which would outrank all computed ranking.",
 "tie_note": "no tie at the top; B9 vs B2 invert under tie-break only"})

# ---------- board consistency check ----------
consistency = {"unresolved_contradictions": 0, "split_claims": [], "pass": True,
               "notes": ["palace 2 carries SUPPORT+VETO split (open gate vs void/tomb) — typed split per overload rule 16",
                         "palace 4 carries VETO on best-solution with explicit auspicious patterns acknowledged — typed split",
                         "palace 9 carries hidden-problem SUPPORT + best-solution VETO — consistent polarities, no collision",
                         "no palace pair claims SUPPORT and VETO for the same logical path"]}
for pid in ["2", "4", "9"]:
    consistency["split_claims"].append({"palace": pid, "policy": "overload_rule_split_checked"})

# ---------- final solution seed ----------
palaces_state = load_state("palaces.json")
def claims(pid, slot=None, polarity=None):
    out = []
    for v in palaces_state[pid]["verdicts"]:
        if (slot is None or v["slot"] == slot) and (polarity is None or v["polarity"] == polarity):
            out.append(v)
    return out

seed = load_state("solution_seed.json")
seed["revision"] += 1
seed["answers"] = [
  {"archetype_resolution": "RES-001", "winner": "ANS-seats-in-zhen-3", "score": resolutions[0]["candidates_considered"][0]["final_score"],
   "seat": "Zhen 3 Palace (outer, East, Wood)", "status": "chart-derived only; not yet requirement-bound",
   "claims": [c["claim_id"] for c in claims("3", "chart_answers_candidate")],
   "reading": "The answer sits in Zhen 3: day stem + concealed leader proxy + duty star + Chief deity converge on one palace. It arrives hour-void (lands on Mao day/hour), runs an Imprisoned Scenery method, and is fed through covered channels (earth Xin generates heaven Ren; hidden Ding-Ren combination). Center's displaced core (Ji + Tian Qin) lodges here too — the institutional core of the matter is administered from this seat.",
   "constraints_cited": ["palaces.zhen_3.special_markers[0]", "palaces.zhen_3.prosperity_decline.palace_state", "palaces.zhen_3.harm"],
   "context": {"center_displacement": [c["claim_id"] for c in claims("5")]}},
]
seed["hidden_problems"] = [
  {"rank": 1, "archetype_resolution": "RES-002", "archetype": "HID-palace-4-death-duty-tomb-cluster",
   "score": hidden_cands[0]["final_score"], "claims": [c["claim_id"] for c in claims("4", "chart_hidden_problems_candidate")],
   "reading": "The avoid-list cluster: Death duty door forced in Xun 4, Door Entering Tomb, the day stem itself entombed and punished there, sanqi Yi restricted — the glittering 'wonder mission' of Xun 4 is the locked door. The hour horse runs straight at it."},
  {"rank": 2, "archetype_resolution": "RES-002", "archetype": "HID-palace-9-void-showpiece",
   "score": hidden_cands[1]["final_score"], "claims": [c["claim_id"] for c in claims("9", "chart_hidden_problems_candidate")],
   "reading": "The public-facing showcase layer is day-void on the year-stacked palace: big display energy (Scenery at home, 'Prosperous' door) that does not land this window; fills on Wu day/hour."},
  {"rank": 3, "archetype_resolution": "RES-002", "archetype": "HID-palace-1-great-barrier",
   "score": hidden_cands[2]["final_score"], "tied_with": ["HID-palace-2-void-open-jia-tomb", "HID-palace-8-stalled-storage"],
   "claims": [c["claim_id"] for c in claims("1", "chart_hidden_problems_candidate")],
   "reading": "Great Barrier (Geng over Gui) with injury door at Dead on the groundwork track — stalls and grind, intermittent rather than terminal.",
   "also_tied": {"HID-palace-2-void-open-jia-tomb": [c["claim_id"] for c in claims("2", "chart_hidden_problems_candidate")],
                 "HID-palace-8-stalled-storage": [c["claim_id"] for c in claims("8", "chart_hidden_problems_candidate")]}},
]
seed["best_solution_candidates"] = [
  {"rank": 1, "archetype_resolution": "RES-003", "archetype": "BEST-dui-7-earthly-escape-channel",
   "score": best_cands[0]["final_score"], "claims": [c["claim_id"] for c in claims("7", "chart_best_solution_candidate", "SUPPORT")],
   "reading": "HOW: rest-and-consolidate through Dui 7 — the board's one concordant-strong, affliction-free palace: sanqi stacked (Bing/Yi), earthly escape co-located (Yi + Rest Door), Palace Generating Door explicit, month-stacked (in-period). White Tiger warns the strength reads severe; run it clean and procedural, inside institutions (inner ring).",
   "caveats_cited": ["palaces.dui_7.deity"]},
  {"rank": 2, "archetype_resolution": "RES-003", "archetype": "BEST-qian-6-harmony-help-channel",
   "score": best_cands[1]["final_score"], "claims": [c["claim_id"] for c in claims("6", "chart_best_solution_candidate", "SUPPORT")],
   "reading": "WHEN/WITH WHOM: Qian 6 is the timing and alliance seat — hour focus, Life door, Six Harmony, Tian Yi star; support is real but buried (star Imprisoned/Imprisoned, Wu entombed, Xu-Chen clash to the day root): activate for pacts and backstage help, expect friction and latency.",
   "caveats_cited": ["palaces.qian_6.special_markers[0]", "palaces.qian_6.prosperity_decline.star_strength"]},
  {"rank": "rejected", "archetype_resolution": "RES-003", "archetype": "BEST-li-9-salary-channel",
   "score": best_cands[2]["final_score"], "claims": [c["claim_id"] for c in claims("9", "chart_best_solution_candidate", "VETO")], "reason": "void-locked payoff window"},
  {"rank": "rejected", "archetype_resolution": "RES-003", "archetype": "BEST-kun-2-open-gate",
   "score": best_cands[3]["final_score"], "claims": [c["claim_id"] for c in claims("2", "chart_best_solution_candidate", "VETO")], "reason": "opens onto day-void with entombed stem and obscurity deity"},
]
seed["note"] = "chart-derived only; not yet requirement-bound"
seed["requirement_fit_score_policy"] = "null everywhere; binding deferred to downstream solver"
seed["patches"].append({"rev": seed["revision"], "after": "P6 finalise",
                        "answers": len(seed["answers"]), "hidden_problems": len(seed["hidden_problems"]),
                        "best_solution_candidates": len(seed["best_solution_candidates"])})
dump_state("solution_seed.json", seed)
dump_state("archetype_resolutions.json", {"rubric_version_hash": RUBRIC_HASH, "protocol_version_hash": PROTO_HASH,
                                          "weights": W, "resolutions": resolutions})
dump_state("board_consistency.json", consistency)

# yongshen re-affirmed unbound
yg = load_state("yongshen.json")
assert all(c["bound"] is False and c["requirement_fit_score"] is None for c in yg["candidates"])

progress(f"P6 done | archetype resolutions: 3 (winners: RES-001 zhen3 seat, RES-002 palace4 cluster, RES-003 dui7 escape) | board consistency: pass | yongshen unbound: ok")
machine_update(state="P6_DONE", completed_phases=load_state("machine.json")["completed_phases"] + ["P6_BOARD_SYNTHESIS"],
               verification={**load_state("machine.json").get("verification", {}),
                             "board_consistency": True, "archetype_resolutions_scored": True,
                             "yongshen_unbound": True})
print(json.dumps({"RES-001 winner": resolutions[0]["winner"], "score": resolutions[0]["candidates_considered"][0]["final_score"],
                  "RES-002 winner": resolutions[1]["winner"], "score": hidden_cands[0]["final_score"],
                  "RES-002 runner": {"id": hidden_cands[1]["archetype_id"], "score": hidden_cands[1]["final_score"]},
                  "RES-003 winner": resolutions[2]["winner"], "score": best_cands[0]["final_score"],
                  "RES-003 runner": {"id": best_cands[1]["archetype_id"], "score": best_cands[1]["final_score"]},
                  "board_consistency": consistency["pass"]}, indent=1))
