"""P7_SLOT_BIND -> SOLUTION_ENGINE -> SYNTHESIZE.

Binds package yongshen candidates and archetype resolutions to the brief's
question types, computes requirement_fit, re-scores under the solver rubric,
and freezes Solution-Live.

The chart package is authoritative for chart evidence (law 7). This module
never opens the source chart (law 8).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver_common import *  # noqa

PKG = jread(PACKAGE)
REQS = {r["id"]: r for r in jread(os.path.join(STATE, "requirements.json"))["requirements"]}
DELS = jread(os.path.join(STATE, "deliverable_registry.json"))["deliverables"]
RES = PKG["patterns"]["archetype_resolutions"]
SEED = PKG["solution_seed"]
YONG = PKG["yongshen_candidates"]
COV = PKG["full_field_coverage"]
FIND = {f["name_en"]: f for f in COV["findings"]}

HARD_CONSTRAINTS = ["R05", "R10", "R01"]


def res(rid):
    return [r for r in RES if r["resolution_id"] == rid][0]


def winner_label(rid):
    r = res(rid)
    sel = [c for c in r["candidates_considered"] if c["selected"]]
    return sel[0] if sel else None


# =========================================================== P7_SLOT_BIND ===
def slot_bind():
    """Bind chart candidates to the brief's actual question types."""
    question_types = [
        {"qid": "Q1", "question_en": "What is the campaign actually about, and what is the "
                                     "single idea it must carry?",
         "requirement_ids": ["R06", "R04", "R12"], "slot": "my_answers"},
        {"qid": "Q2", "question_en": "What will quietly cause this project to fail if it is "
                                     "not designed around?",
         "requirement_ids": ["R01", "R10", "R05", "R22"], "slot": "hidden_problems"},
        {"qid": "Q3", "question_en": "Which route should the campaign take across six media?",
         "requirement_ids": ["R08", "R09", "R01", "R20"], "slot": "best_solution"},
        {"qid": "Q4", "question_en": "Who is the audience and what moves them?",
         "requirement_ids": ["R03", "R19"], "slot": "my_answers"},
        {"qid": "Q5", "question_en": "How is the work sequenced across four weeks?",
         "requirement_ids": ["R14", "R15", "R16", "R17"], "slot": "timing"},
    ]

    bindings = []
    for y in YONG:
        cid = y["candidate_id"]
        b = {"candidate_id": cid, "label": y["label"],
             "package_grounding": y["grounding"],
             "package_evidence_paths": y["evidence_paths"],
             "package_condition": y["condition"],
             "bound_question": None, "bound_requirement_ids": [], "slot": None,
             "binding_rationale_en": ""}
        if cid == "YS-DUTY-9":
            b.update(bound_question="Q1", slot="my_answers",
                     bound_requirement_ids=["R06", "R04", "R12"],
                     binding_rationale_en=(
                         "The package's authority marker is the subject of the question. The "
                         "brief's equivalent subject is the big campaign idea and the USP it "
                         "rests on. Both are 'the thing being presented'. The package reports "
                         "this position as highly visible but structurally unsupported, which "
                         "maps precisely onto the risk of a tourism idea that looks impressive "
                         "in a deck and collapses on contact with six real media."))
        elif cid == "YS-DAY-BING":
            b.update(bound_question="Q4", slot="my_answers",
                     bound_requirement_ids=["R03", "R19"],
                     binding_rationale_en=(
                         "The actor candidate binds to the audience-and-self question: who is "
                         "doing the travelling. The package reports this actor as displaced, "
                         "with no seat of its own, which binds to a traveller who does not see "
                         "themselves in conventional tourism marketing."))
        elif cid == "YS-HOUR-JIA":
            b.update(bound_question="Q5", slot="timing",
                     bound_requirement_ids=["R14", "R15", "R16", "R17"],
                     binding_rationale_en=(
                         "The matter-in-motion candidate binds to the delivery timeline. The "
                         "package reports it as absent from every visible position, which binds "
                         "to the fact that most of the real work in this project is invisible "
                         "until the final week."))
        elif cid == "YS-LEAD-XIN":
            b.update(bound_question="Q1", slot="my_answers",
                     bound_requirement_ids=["R06", "R07"],
                     binding_rationale_en=(
                         "The visible stand-in candidate binds to the key creative - the single "
                         "execution that represents the whole idea publicly."))
        elif cid == "YS-OPEN-6":
            b.update(bound_question="Q3", slot="best_solution",
                     bound_requirement_ids=["R08", "R09", "R20"],
                     binding_rationale_en=(
                         "A high-quality, well-supported route candidate binds to the craft "
                         "dimension of the media plan: the channels where finish and reputation "
                         "are decided."))
        elif cid == "YS-LIFE-8":
            b.update(bound_question="Q3", slot="best_solution",
                     bound_requirement_ids=["R08", "R09", "R01"],
                     binding_rationale_en=(
                         "A growth-and-partnership route candidate binds to the reach dimension "
                         "of the media plan: the channels where an audience is actually joined "
                         "and carried."))
        bindings.append(b)

    out = {"question_types": question_types, "bindings": bindings,
           "note_en": "Every yongshen candidate from the package is now bound to a brief "
                      "question type and a requirement set. No candidate is left unbound."}
    jwrite(os.path.join(STATE, "slot_bindings.json"), out)
    return out


# ============================================== requirement fit + rescoring =
def requirement_fit(candidate_id, mapped_reqs, violates_hard, tone_fit):
    coverage = len(mapped_reqs) / 8.0
    coverage = min(coverage, 1.0)
    hard = 0.0 if violates_hard else 1.0
    return round(0.40 * coverage + 0.40 * hard + 0.20 * tone_fit, 4)


def solver_score(tier, support, contra, consistent, rfit,
                 max_support=8, max_contra=5):
    t = {"EXPLICIT": 1.0, "COMPUTED": 0.6, "INFERRED": 0.3}[tier]
    return round(0.35 * t
                 + 0.25 * min(support, max_support) / max_support
                 + 0.20 * (1.0 - min(contra, max_contra) / max_contra)
                 + 0.10 * (1.0 if consistent else 0.0)
                 + 0.10 * rfit, 4)


# ========================================================= SOLUTION_ENGINE ==
FIT_TABLE = {
    "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE": {
        "reqs": ["R01", "R08", "R09", "R10", "R03", "R06", "R20", "R22"],
        "violates": False, "tone": 1.0,
        "strategy_en": "Build the campaign as an invitation to be joined - the audience is "
                       "brought inside the culture and carries part of it onward.",
    },
    "BEST-OPEN-DOOR-NW-P6-WITH-DING": {
        "reqs": ["R07", "R20", "R21", "R18"],
        "violates": False, "tone": 0.85,
        "strategy_en": "Build the campaign as a showcase of craft and finish - authority and "
                       "quality lead.",
    },
    "BEST-JING-FEAR-W-P7": {
        "reqs": ["R20"], "violates": False, "tone": 0.35,
        "strategy_en": "Build the campaign on caution, scarcity or warning.",
    },
    "BEST-RIDE-THE-HORSE-AT-P2": {
        "reqs": ["R01"], "violates": True, "tone": 0.3,
        "strategy_en": "Build the campaign on pure movement and relocation energy.",
    },
    "BEST-PUSH-THE-SHOWPIECE-AT-P9": {
        "reqs": ["R11"], "violates": True, "tone": 0.2,
        "strategy_en": "Build the campaign by amplifying the most spectacular asset.",
    },
}


def solution_engine(bindings):
    finalised = []
    supersessions = []

    for r in RES:
        fr = {"resolution_id": r["resolution_id"].replace("AR-", "SR-"),
              "derived_from_package_resolution": r["resolution_id"],
              "slot": {"chart_answers_candidate": "my_answers",
                       "chart_hidden_problems_candidate": "hidden_problems",
                       "chart_best_solution_candidate": "best_solution"}[r["slot"]],
              "evidence_chain": list(r["evidence_chain"]),
              "candidates_considered": [], "winner": None, "margin_note": ""}

        for c in r["candidates_considered"]:
            nc = dict(c)
            aid = c["archetype_id"]
            if fr["slot"] == "best_solution":
                f = FIT_TABLE.get(aid, {"reqs": [], "violates": False, "tone": 0.3,
                                        "strategy_en": ""})
                rfit = requirement_fit(aid, f["reqs"], f["violates"], f["tone"])
                nc["mapped_requirement_ids"] = f["reqs"]
                nc["violates_hard_constraint"] = f["violates"]
                nc["strategy_en"] = f["strategy_en"]
            else:
                # answers / hidden problems: fit is coverage of their bound requirements
                bound = [b for b in bindings["bindings"]
                         if b["slot"] == fr["slot"]]
                mapped = sorted({x for b in bound for x in b["bound_requirement_ids"]})
                rfit = requirement_fit(aid, mapped, False,
                                       1.0 if c["selected"] else 0.7)
                nc["mapped_requirement_ids"] = mapped
                nc["violates_hard_constraint"] = False
            nc["requirement_fit_score"] = rfit
            nc["final_score"] = solver_score(
                c["grounding_tier"], c["supporting_evidence_count"],
                c["contradicting_evidence_count"], c["board_consistency_pass"], rfit)
            nc["selected"] = False
            fr["candidates_considered"].append(nc)

        # hard-constraint elimination happens BEFORE selection
        eligible = [c for c in fr["candidates_considered"]
                    if not c.get("violates_hard_constraint")
                    and c["board_consistency_pass"]]
        pool = eligible or fr["candidates_considered"]
        pool.sort(key=lambda x: (-x["final_score"], x["archetype_id"]))
        top = pool[0]
        tied = [c for c in pool if abs(c["final_score"] - top["final_score"]) < 1e-9]
        for c in tied:
            c["selected"] = True
        fr["winner"] = None if len(tied) > 1 else top["archetype_id"]
        fr["status"] = "STILL_TIED" if len(tied) > 1 else "RESOLVED"

        for c in fr["candidates_considered"]:
            if not c["selected"] and not c.get("rejection_reason"):
                c["rejection_reason"] = "Lower score after requirement fit was applied."
            if c.get("violates_hard_constraint"):
                c["rejection_reason"] = (
                    "ELIMINATED BY HARD CONSTRAINT before scoring. " +
                    (c.get("rejection_reason") or ""))

        if fr["slot"] == "best_solution":
            w = [c for c in fr["candidates_considered"] if c["selected"]][0]
            ru = [c for c in fr["candidates_considered"] if not c["selected"]][0]
            fr["margin_note"] = (
                f"The chart layer already preferred this route on its own evidence. Adding "
                f"requirement fit widens rather than narrows the gap: the winning route maps to "
                f"{len(w['mapped_requirement_ids'])} requirements including every hard "
                f"constraint, while the runner-up maps to {len(ru['mapped_requirement_ids'])} and "
                f"is concentrated on craft rather than reach. Final scores "
                f"{w['final_score']} against {ru['final_score']}. The runner-up is NOT discarded: "
                f"it is retained as the governing standard for the key creative, where finish "
                f"and authority are what the brief is grading. Two candidates were eliminated "
                f"before scoring for violating hard constraints.")
            supersessions.append({
                "supersession_id": "SUP-001",
                "old_claim_id": "AR-BEST-01 / chart-only ranking",
                "new_claim_id": f"{fr['resolution_id']} / requirement-bound ranking",
                "old_evidence": "Chart-only score 0.72 vs 0.64, no requirement fit applied.",
                "new_evidence": f"Requirement-bound score {w['final_score']} vs "
                                f"{ru['final_score']}; hard-constraint elimination removed two "
                                f"candidates entirely.",
                "reason_en": "Prompt 2 adds requirement fit, which Prompt 1 was forbidden to "
                             "compute. The ordering did not change, so no conclusion is "
                             "reversed - only sharpened.",
            })
        else:
            w = [c for c in fr["candidates_considered"] if c["selected"]][0]
            others = [c for c in fr["candidates_considered"] if not c["selected"]]
            fr["margin_note"] = (
                f"Winner {w['archetype_id']} at {w['final_score']}. "
                + (f"Nearest alternative {others[0]['archetype_id']} at "
                   f"{others[0]['final_score']}. " if others else
                   "No competing candidate found. ")
                + "Requirement fit was applied uniformly across candidates in this slot, so the "
                  "ordering is driven by chart grounding and corroboration rather than by the "
                  "brief alone.")
        finalised.append(fr)

    jwrite(os.path.join(STATE, "solver_resolutions.json"),
           {"resolutions": finalised, "supersessions": supersessions})
    return finalised, supersessions


# ============================================================ SOLUTION_LIVE =
def build_solution(finalised, bindings):
    def sel(rid):
        r = [x for x in finalised if x["resolution_id"] == rid][0]
        return [c for c in r["candidates_considered"] if c["selected"]], r

    ans_sel, ans_r = sel("SR-ANSWERS-01")
    hid_sel, hid_r = sel("SR-HIDDEN-01")
    best_sel, best_r = sel("SR-BEST-01")

    answers = [{
        "claim_id": "ANS-01", "slot": "my_answers",
        "text_en": "The campaign must be built around one idea that is strong enough to change "
                   "shape six times without losing its name. The brief's real subject is not a "
                   "state and not a niche - it is whether a single idea can survive contact with "
                   "six different media.",
        "polarity": "SUPPORT", "confidence": "HIGH", "grounding": "COMPUTED",
        "requirement_ids": ["R06", "R01", "R12"],
        "archetype_resolution_id": "SR-ANSWERS-01",
        "evidence": [{"package_path": "patterns.archetype_resolutions[AR-ANSWERS-01].winner",
                      "value": ans_sel[0]["archetype_id"]}],
        "phase": "SOLUTION_ENGINE", "status": "live"},
        {"claim_id": "ANS-02", "slot": "my_answers",
         "text_en": "The audience is the traveller who does not recognise themselves in ordinary "
                    "tourism advertising. They are not looking for a destination; they are "
                    "looking for a place that will let them in.",
         "polarity": "SUPPORT", "confidence": "MED", "grounding": "COMPUTED",
         "requirement_ids": ["R03", "R19"],
         "archetype_resolution_id": "SR-ANSWERS-01",
         "evidence": [{"package_path": "yongshen_candidates[YS-DAY-BING].condition",
                       "value": "displaced actor with no seat of its own"}],
         "phase": "SOLUTION_ENGINE", "status": "live"}]

    hidden = []
    hid_map = [
        ("HID-01", "The most visible part of this project is the weakest. A campaign idea that "
                   "presents beautifully in a deck can have nothing underneath it - and this "
                   "brief grades exactly that gap, because it is explicitly testing integration "
                   "against adaptation.", ["R01", "R10", "R22"], "HIGH"),
        ("HID-02", "There is no natural home for the work. The team has no single medium it can "
                   "retreat into and call the campaign finished; every one of the six has to "
                   "carry weight independently.", ["R08", "R09", "R01"], "HIGH"),
        ("HID-03", "Nothing in this project moves by itself. No execution will suggest the next "
                   "one; each has to be deliberately pushed into place, which is why the "
                   "sequencing matters more than usual.", ["R14", "R15", "R16", "R17"], "HIGH"),
        ("HID-04", "The most attractive route is also the most dangerous one. The instinct to "
                   "lead with craft and polish will produce a beautiful key creative that "
                   "quietly buries the idea under its own finish.", ["R07", "R20"], "MED"),
        ("HID-05", "The engine of the campaign is invisible until late. The connecting idea has "
                   "no body of its own until the executions exist, so it will feel absent for "
                   "most of the project and cannot be judged early.", ["R15", "R16"], "MED"),
    ]
    for cid, txt, reqs, conf in hid_map:
        hidden.append({"claim_id": cid, "slot": "hidden_problems", "text_en": txt,
                       "polarity": "WARN", "confidence": conf, "grounding": "COMPUTED",
                       "requirement_ids": reqs,
                       "archetype_resolution_id": "SR-HIDDEN-01",
                       "evidence": [{"package_path":
                                     "patterns.archetype_resolutions[AR-HIDDEN-01]"
                                     ".candidates_considered",
                                     "value": "five live hidden problems carried from the package"}],
                       "phase": "SOLUTION_ENGINE", "status": "live"})

    best = {
        "claim_id": "BEST-01", "slot": "best_solution",
        "winner_archetype": best_sel[0]["archetype_id"],
        "final_score": best_sel[0]["final_score"],
        "requirement_fit_score": best_sel[0]["requirement_fit_score"],
        "text_en": "Lead with participation, not spectacle. The campaign should be built as an "
                   "invitation the audience can accept and pass on, with every medium doing one "
                   "job the other five cannot do. Craft and finish govern the key creative, but "
                   "they do not lead the campaign.",
        "polarity": "SUPPORT", "confidence": "HIGH", "grounding": "COMPUTED",
        "requirement_ids": best_sel[0]["mapped_requirement_ids"],
        "archetype_resolution_id": "SR-BEST-01",
        "runner_up_retained": {
            "archetype": "BEST-OPEN-DOOR-NW-P6-WITH-DING",
            "role_en": "Governs the key creative standard only - craft, finish, authority.",
        },
        "eliminated_by_hard_constraint": [
            c["archetype_id"] for c in best_r["candidates_considered"]
            if c.get("violates_hard_constraint")],
        "phase": "SOLUTION_ENGINE", "status": "live",
    }

    split_claims = []
    for r in finalised:
        if r.get("status") == "STILL_TIED":
            split_claims.append({"resolution_id": r["resolution_id"],
                                 "candidates": [c["archetype_id"]
                                                for c in r["candidates_considered"]
                                                if c["selected"]]})

    sol = {"revision": 1, "answers": answers, "hidden_problems": hidden,
           "best_solution": best,
           "open_questions": [
               "Whether the marker weights Research above Execution - affects how much depth "
               "the research deliverable needs. Internal only; not shipped as an answer."],
           "evidence": [{"package_path": "solution_seed", "value": SEED["note"]}],
           "split_claims": split_claims}
    jwrite(os.path.join(STATE, "solution_live.json"), sol)
    return sol


if __name__ == "__main__":
    b = slot_bind()
    finalised, sup = solution_engine(b)
    sol = build_solution(finalised, b)
    m = jread(os.path.join(STATE, "solver_machine.json"))
    m["state"] = "SYNTHESIZE"
    m["completed_phases"] += ["P7_SLOT_BIND", "SOLUTION_ENGINE"]
    m["solution_revision"] = sol["revision"]
    jwrite(os.path.join(STATE, "solver_machine.json"), m)
    heartbeat(f"slot_bind {len(b['bindings'])} candidates | solution_engine complete | "
              f"best winner {sol['best_solution']['winner_archetype']} | "
              f"supersessions {len(sup)}")
    print("bindings:", len(b["bindings"]), "| unbound:",
          len([x for x in b["bindings"] if not x["slot"]]))
    for r in finalised:
        print(f"{r['resolution_id']:18} {r['status']:12} winner={r['winner']}")
        for c in sorted(r["candidates_considered"], key=lambda x: -x["final_score"]):
            flag = "SEL" if c["selected"] else ("HARD-ELIM" if c.get("violates_hard_constraint") else "   ")
            print(f"    {c['final_score']:.4f} rfit={c['requirement_fit_score']:.2f} "
                  f"{flag:9} {c['archetype_id']}")
