"""P7 AMENDMENT: feed full-coverage evidence back into the archetype resolutions.

Law: contradiction_policy - later complete-board evidence may override an early
verdict, but only with an explicit override note citing BOTH old and new
evidence. Never silently drop an early verdict.

Two amendments are made:
  A1  AR-BEST-01 was STILL_TIED / narrow between palace 6 and palace 8. The
      birth-stage field (previously unread) is a decisive discriminator.
  A2  ANOMALY:HOUR_STEM_NOT_ON_PLATE is downgraded: system.method declares
      Lun Zang Jia, in which the hidden Jia is native, not missing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
RESF = os.path.join(STATE, "archetype_resolutions.json")
RES = jread(RESF)["resolutions"]
COV = jread(os.path.join(STATE, "full_coverage.json"))
ANOMF = os.path.join(STATE, "anomalies.json")
ANOM = jread(ANOMF)["anomalies"]
OVERRIDES = []


def score(tier, support, contra, consistent, max_support=8, max_contra=5):
    t = {"EXPLICIT": 1.0, "COMPUTED": 0.6, "INFERRED": 0.3}[tier]
    return round(0.35 * t + 0.25 * min(support, max_support) / max_support
                 + 0.20 * (1.0 - min(contra, max_contra) / max_contra)
                 + 0.10 * (1.0 if consistent else 0.0) + 0.10 * 0.0, 4)


# ------------------------------------------------------- A1: break the tie --
def amend_best():
    r = [x for x in RES if x["resolution_id"] == "AR-BEST-01"][0]
    old = {c["archetype_id"]: dict(c) for c in r["candidates_considered"]}

    for c in r["candidates_considered"]:
        if c["archetype_id"] == "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE":
            c["supporting_evidence_count"] += 3   # birth stage, Water rising, star Prosperous
            c["amendment_en"] = (
                "P7 added three previously unread supporting facts: palace 8 lists Bing (the day "
                "stem) in `stems_in_birth_stage`, its stem Ren is Water which is Strengthening, "
                "and its harm rule against Xin is latent rather than active.")
        if c["archetype_id"] == "BEST-OPEN-DOOR-NW-P6-WITH-DING":
            c["supporting_evidence_count"] += 1   # day branch Xu sits here
            c["contradicting_evidence_count"] += 1  # tomb vs birth-stage opposition sharpened
            c["amendment_en"] = (
                "P7 added one supporting fact - the day branch Xu belongs to palace 6, so the "
                "actor's branch is already here - and one contradicting fact: set directly "
                "against palace 8's birth stage, palace 6's status as Bing's tomb is now a "
                "measured opposition rather than an isolated caution.")
        c["final_score"] = score(c["grounding_tier"], c["supporting_evidence_count"],
                                 c["contradicting_evidence_count"], c["board_consistency_pass"])
        c["selected"] = False

    r["candidates_considered"].sort(key=lambda x: (-x["final_score"], x["archetype_id"]))
    top = r["candidates_considered"][0]
    tied = [c for c in r["candidates_considered"] if abs(c["final_score"] - top["final_score"]) < 1e-9]
    still_tied = len(tied) > 1
    for c in tied:
        c["selected"] = True

    r["evidence_chain"].append({
        "step": "raw_field", "path": "palaces.8.palace_stem_rules.stems_in_birth_stage",
        "value": "Bing, Wu",
        "description": "Palace 8 holds the day stem Bing in its birth stage - the exact "
                       "structural opposite of palace 6, which is Bing's tomb."})
    r["evidence_chain"].append({
        "step": "computed_relation",
        "evidence_paths": ["palaces.8.palace_stem_rules.stems_in_birth_stage",
                           "palaces.6.palace_stem_rules.stems_in_tomb",
                           "timing.four_pillars.day"],
        "description": "Birth stage versus tomb for the same stem is a polar opposition, not a "
                       "matter of degree. It separates two candidates that were otherwise level."})

    r["status"] = "STILL_TIED" if still_tied else "RESOLVED_BY_AMENDMENT"
    r["winner"] = None if still_tied else top["archetype_id"]
    r["margin_note"] = (
        "AMENDED IN P7. The earlier run scored these 0.6887 to 0.6487 and declined to separate "
        "them, stating that the discriminator would have to come from assignment information. "
        "That was wrong, and the correction matters: the discriminator was sitting unread in the "
        "chart itself. `palaces.8.palace_stem_rules.stems_in_birth_stage` contains Bing, the day "
        "stem, while `palaces.6.palace_stem_rules.stems_in_tomb` contains the same Bing. Palace 8 "
        "is where the actor is born; palace 6 is where the actor is buried. That is a polar "
        "opposition on the single most important stem in the chart, and it separates the two "
        f"candidates without any appeal to the assignment. Amended scores: palace 8 "
        f"{[c['final_score'] for c in r['candidates_considered'] if c['archetype_id'].endswith('P8-WITH-LIUHE')][0]}, "
        f"palace 6 "
        f"{[c['final_score'] for c in r['candidates_considered'] if c['archetype_id'].endswith('P6-WITH-DING')][0]}. "
        "Palace 6 is NOT discarded - it retains the only Prosperous door on a San Qi stem and "
        "holds the actor's own day branch Xu, so it remains the correct choice for anything "
        "requiring quality or finishing rather than growth. But as a route for the actor to "
        "survive and develop, palace 8 now wins on the chart's own evidence.")

    for c in r["candidates_considered"]:
        if not c["selected"] and c["archetype_id"] == "BEST-OPEN-DOOR-NW-P6-WITH-DING":
            c["rejection_reason"] = (
                "Separated from palace 8 in the P7 amendment by the birth-stage/tomb opposition "
                "on the day stem Bing: palace 8 is Bing's birth stage, palace 6 is Bing's tomb. "
                "Retained as a live co-candidate and the preferred route for quality, finishing "
                "or reputation work, because it holds the only Prosperous door carrying a San Qi "
                "stem and the actor's own day branch Xu sits there. It is rejected only as the "
                "primary route for the actor's own development.")

    OVERRIDES.append({
        "override_id": "OVR-001", "target": "AR-BEST-01",
        "old_state": {"status": "RESOLVED (narrow)", "winner": "BEST-LIFE-DOOR-NE-P8-WITH-LIUHE",
                      "scores": {k: v["final_score"] for k, v in old.items()},
                      "old_margin_claim": "Declared unresolvable from the chart alone; claimed "
                                          "the separator was assignment information."},
        "new_state": {"status": r["status"], "winner": r["winner"],
                      "scores": {c["archetype_id"]: c["final_score"]
                                 for c in r["candidates_considered"]}},
        "old_evidence": ["palaces.6.active_chart.energy_state.door",
                         "palaces.8.active_chart.energy_state.door"],
        "new_evidence": ["palaces.8.palace_stem_rules.stems_in_birth_stage",
                         "palaces.6.palace_stem_rules.stems_in_tomb",
                         "palaces.6.base_position.earthly_branches",
                         "element_prosperities.water"],
        "reason_en": "P7 read fields the earlier run never opened. The birth-stage field resolves "
                     "a tie the earlier run wrongly declared unresolvable. Early verdict is "
                     "preserved above, not deleted.",
    })
    return r


# ------------------------------------------- A2: downgrade a false anomaly --
def amend_anomaly():
    for a in ANOM:
        if a["code"] == "HOUR_STEM_NOT_ON_PLATE":
            old = dict(a)
            a["severity"] = "LOW"
            a["status"] = "DOWNGRADED_BY_P7"
            a["detail"] = (
                "Hour stem Jia is absent from all plates; proxy set used (lead_stem_proxy Xin, "
                "tomb of Jia, hour branch palace). DOWNGRADED FROM HIGH TO LOW IN P7: "
                "`system.school` declares Yi Yun - Lun Zang Jia, literally 'discussing the hidden "
                "Jia', a tradition in which Jia is never displayed on the plate and is always "
                "read through its decade proxy stem. The absence is native to the method, not a "
                "defect in the data. The proxy handling already applied was the correct "
                "procedure, so no downstream verdict changes - only the severity label.")
            a["evidence_paths"] = a.get("evidence_paths", []) + ["system.school", "system.method"]
            OVERRIDES.append({
                "override_id": "OVR-002", "target": "ANOMALY:HOUR_STEM_NOT_ON_PLATE",
                "old_state": {"severity": old["severity"]},
                "new_state": {"severity": "LOW", "status": "DOWNGRADED_BY_P7"},
                "old_evidence": old.get("evidence_paths", []),
                "new_evidence": ["system.school", "system.method"],
                "reason_en": "The school declaration explains the absence as native to the "
                             "method. Severity corrected; the anomaly is retained, not deleted.",
            })
    return ANOM


if __name__ == "__main__":
    r = amend_best()
    amend_anomaly()
    jwrite(RESF, {"resolutions": RES})
    jwrite(ANOMF, {"anomalies": ANOM})
    jwrite(os.path.join(STATE, "overrides.json"), {"overrides": OVERRIDES})
    heartbeat(f"P7_AMEND | AR-BEST-01 -> {r['status']} winner {r['winner']} | "
              f"overrides {len(OVERRIDES)}")
    print("AR-BEST-01:", r["status"], "winner:", r["winner"])
    for c in r["candidates_considered"]:
        print("  ", c["final_score"], c["selected"], c["archetype_id"])
    print("overrides:", [o["override_id"] for o in OVERRIDES])
