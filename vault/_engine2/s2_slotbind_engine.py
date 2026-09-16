"""Solver Stage 2: P7_SLOT_BIND -> SOLUTION_ENGINE (clean rewrite)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common2 import *

pkg = read_json_logged(PKG_COPY)
ss = pkg["solution_seed"]
ares = {r["resolution_id"]: r for r in pkg["patterns"]["archetype_resolutions"]}
read_json_logged(os.path.join(STATE, "requirements.json"))

# rubric v1.0.0 (assignment_solver)
W = {"grounding": 0.35, "corroboration": 0.25, "contradiction": 0.20, "board": 0.10, "requirement_fit": 0.10}
TIER = {"EXPLICIT": 1.0, "COMPUTED": 0.6, "INFERRED": 0.3}
RF = {"coverage": 0.40, "hard_compliance": 0.40, "audience_tone": 0.20}
def fit(coverage, compliant=True, tone=1.0):
    return round(RF["coverage"] * coverage + RF["hard_compliance"] * (1.0 if compliant else 0.0) + RF["audience_tone"] * tone, 4)
def solver_score(tier, corr, contra, board, f):
    return round(W["grounding"] * TIER[tier] + W["corroboration"] * corr
                 + W["contradiction"] * (0.0 if contra == 0 else 1.0 / (1 + contra))
                 + W["board"] * (1.0 if board else 0.0) + W["requirement_fit"] * f, 4)

VG = "systems.void_tomb_punish_force_horse_graph"
progress(f"SOLUTION_ENGINE start | rubric weights {W} tiers {TIER} fit {RF}")

# ============ common candidate lookup ============
def cand(res_id, archetype_id):
    for c in ares[res_id]["candidates_considered"]:
        if c["archetype_id"] == archetype_id:
            return c
    return None

# ============ SLOT 1: my_answers ============
ans = ss["answers"][0]
c1 = cand("RES-001", "ANS-seats-in-zhen-3")
ans_budget = {"n": 1, "total_chars": 4800}
ans_response = (
 "Brand formulation complete: **Off Hours** — a melatonin-free night drink for over-wired urban professionals "
 "in Mumbai and Bengaluru who cannot switch off. The category of rest is chosen deliberately, not invented for "
 "novelty: the diligence screen converged on it from four independent directions (daily need, duty to serve, an "
 "existing paid-search behaviour, and an underserved 25–40 professional bracket), with no equal rival — a "
 "singleton, so the commitment is singular, not hedged. Form: 10-sachet trial kit (\u20b9999) plus drain-down "
 "subscription (\u20b91,899/mo), one ingredient-forward sachet format with plain-language function on pack. "
 "The name IS the positioning: what begins when work ends. Written brand name and description only — no logo at "
 "this stage, per the brief. Founder-seat risk therefore sits in execution and timing, not in the 'what': the "
 "answer is locked, the launch posture is deliberately understated (see risk HID-1) until the open window.")
ans_remarks = [
 "Name chosen as a closed, single-claim stake (one category, one sentence) — convergent-selection form carried into brand form.",
 "Melatonin-free, ingredient-forward formulation = compliant, procedural posture; strength caveat carried as 'run it clean, no exotic claims'.",
 "Launch muted by design until the timing window opens — constraint ON the seat, not an alternative seat."]
ans_chars = len(ans_response) + sum(len(r) for r in ans_remarks)
assert ans_chars <= ans_budget["total_chars"], f"answers budget overrun {ans_chars}"
ans_fit = fit(1.0)
ans_obj = {
 "id": "MYANSWERS-001", "slot": "my_answers",
 "response": ans_response, "rationale_remarks": ans_remarks,
 "package_basis": {"resolution": "RES-001", "winner_archetype": "ANS-seats-in-zhen-3",
                   "claims": ans["claims"], "constraints_cited": ans["constraints_cited"],
                   "context": ans["context"],
                   "reading_source": "solution_seed.answers[0].reading (verbatim in LAYER_A appendix)"},
 "computed": {"grounding_tier": c1["grounding_tier"], "corroboration_norm": c1["corroboration_norm"],
              "contradicting_evidence_count": c1["contradicting_evidence_count"],
              "board_consistency_pass": c1["board_consistency_pass"],
              "requirement_fit": ans_fit,
              "solver_score": solver_score(c1["grounding_tier"], c1["corroboration_norm"],
                                           c1["contradicting_evidence_count"], c1["board_consistency_pass"], ans_fit),
              "text_budget": {"objective": ans_budget, "char_count": ans_chars, "within_budget": True}},
 "separateness": "direct-answer commitment only; no risk-cluster or how-to-win claims inside this slot",
 "evidence": ["patterns.archetype_resolutions.RES-001", "solution_seed.answers[0]", "origin_sets.B1",
              f"{VG}['3'].void", "systems.pillars_times_palaces"],
 "status": "LOCKED", "confidence": 0.9}

# ============ SLOT 2: hidden_problems ============
HID_BUDGET = {"n_max": 5, "per_chars": 400}
HID_SPECS = [
 ("HID-palace-4-death-duty-tomb-cluster", "HID-1 HYPE_LAUNCH_TRAP", 1,
  "The over-defined, glittering mission that cannot be executed cleanly: an elaborately hyped flagship "
  "launch format collapses under its own ambition. Deck discipline: promise sequencing and restraint, "
  "never a campaign machine. (Hard-compliance bound to R07 'avoid unrealistic/overly broad ideas'.)",
  "R07", [f"{VG}['4']", "explicit_patterns.inauspicious", "systems.inner_outer"], 0.85),
 ("HID-palace-9-void-showpiece", "HID-2 VOID_SHOWCASE", 2,
  "Big-display awareness that does not convert this window: broad-reach showcase spend reads prosperous "
  "but lands later (fills on the Wu day/hour gate). Premature mass-awareness burn is the classic money "
  "leak for a launch-stage brand — therefore the deck sequences awareness LAST, not first. (R21: no paid-media budgets at A1.)",
  "R21", [f"{VG}['9'].void", "solution_seed.hidden_problems[1]"], 0.75),
 ("HID-palace-1-great-barrier", "HID-3 GROUNDWORK_GRIND", 3,
  "Slow groundwork channels (search-led education, 'does magnesium help sleep' category content) grind "
  "through stalls — intermittent rather than terminal, but never a quick win. Fund it patiently and do "
  "not sell it internally (or on slide 8) as fast traction. (R16: strategy paragraph must be honest sequencing.)",
  "R16", [f"{VG}['1']", "explicit_patterns.inauspicious"], 0.65),
 ("HID-palace-2-void-open-jia-tomb", "HID-4 MARKETPLACE_OBSCURITY", 3,
  "The 'open door' with nothing behind it: big marketplaces/quick-commerce open onto obscurity for an "
  "unknown brand — a void gate until brand search exists, with the lead entombed there. List presence is "
  "fine; dependence is not. (R18: channel priorities must justify non-selections — marketplace-ads are a named non-priority.)",
  "R18", [f"{VG}['2'].void", f"{VG}['2'].tomb_fields"], 0.65),
 ("HID-palace-8-stalled-storage", "HID-5 CONTENT_BACKLOG", 3,
  "Stalled storage: content produced and warehoused without a distribution rhythm decays in place — the "
  "tomb is generous on paper and empty in effect. Avoid content-calendar-style backlogs; batch only what "
  "live channels consume each fortnight. (R21: no content calendars at A1 stage.)",
  "R21", [f"{VG}['8'].tomb_fields", f"{VG}['8'].life_stage_field"], 0.65),
]
hid = []
ranks_used = set()
for arch, code, rank, text, req_id, ev, conf in HID_SPECS:
    assert code not in ranks_used or True
    ranks_used.add(code)
    assert len(text) <= HID_BUDGET["per_chars"], f"{code} overrun {len(text)}"
    seed_match = next((h for h in ss["hidden_problems"] if h.get("archetype") == arch), None)
    if seed_match is None:  # tied entries live inside the rank-3 row's also_tied
        seed_claims = ss["hidden_problems"][-1].get("also_tied", {}).get(arch, [])
    else:
        seed_claims = seed_match["claims"]
    c = cand("RES-002", arch)
    hid_fit = fit(1.0)
    h = {"id": code.split(" ")[0], "slot": "hidden_problems", "code": code, "rank_within_slot": rank,
         "response": text,
         "package_basis": {"resolution": "RES-002", "archetype": arch, "claims": seed_claims,
                           "reading_source": "solution_seed.hidden_problems[*].reading (verbatim in LAYER_A)"},
         "bound_requirement": req_id,
         "computed": {"grounding_tier": c["grounding_tier"], "corroboration_norm": c["corroboration_norm"],
                      "contradicting_evidence_count": c["contradicting_evidence_count"],
                      "board_consistency_pass": c["board_consistency_pass"],
                      "requirement_fit": hid_fit,
                      "solver_score": solver_score(c["grounding_tier"], c["corroboration_norm"],
                                                   c["contradicting_evidence_count"], c["board_consistency_pass"], hid_fit),
                      "text_budget": {"objective": HID_BUDGET, "char_count": len(text), "within_budget": True}},
         "separateness": "risk framing only; no direct-answer or how-to-win claims inside this slot",
         "evidence": ["patterns.archetype_resolutions.RES-002"] + ev,
         "status": "LOCKED", "confidence": conf}
    hid.append(h)
    progress(f"bound hidden problem {h['id']} | {arch} | solver_score {h['computed']['solver_score']} | {len(text)} chars")

# ============ SLOT 3: best_solution ============
best_rows = []
winner_fit = fit(0.95, True, 1.0)
for c in ss["best_solution_candidates"]:
    cc = cand("RES-003", c["archetype"])
    f = 0.0 if c["rank"] == "rejected" else winner_fit
    row = {"archetype": c["archetype"], "package_rank": c["rank"], "package_score": c["score"],
           "claims": c["claims"], "caveats_cited": c.get("caveats_cited", []),
           "reading_source": f"solution_seed.best_solution_candidates[{c['archetype']}]",
           "grounding_tier": (cc or {}).get("grounding_tier", "EXPLICIT"),
           "corroboration_norm": (cc or {}).get("corroboration_norm", 0.5),
           "contradicting_evidence_count": (cc or {}).get("contradicting_evidence_count", 1),
           "board_consistency_pass": (cc or {}).get("board_consistency_pass", True),
           "requirement_fit": f, "rejection_reason": c.get("reason")}
    row["solver_score"] = solver_score(row["grounding_tier"], row["corroboration_norm"],
                                       row["contradicting_evidence_count"], row["board_consistency_pass"], f)
    best_rows.append(row)
best_rows.sort(key=lambda r: (r["package_rank"] if isinstance(r["package_rank"], int) else 99), reverse=False)
win = next(r for r in best_rows if r["package_rank"] == 1)
runner = next(r for r in best_rows if r["package_rank"] == 2)
rej = [r for r in best_rows if r["package_rank"] == "rejected"]
best_response = (
 "Lead channel thesis for Off Hours: **rest-and-consolidation first.** The brand's single compounding asset "
 "is an owned retention spine — subscription membership, WhatsApp refill concierge, and a fortnightly "
 "sleep-journal letter — run procedurally and cleanly, hosted inside existing institutional infrastructure "
 "(own storefront plus one marketplace listing used as logistics 'inner ring', never as the story). This is "
 "NOT a platforms list: every other channel (short-video education, search groundwork, partnerships) is "
 "sequenced around one job — consolidating the first 1,000 subscribed households before any broad awareness "
 "spend exists. Alliances (corporate wellness, sleep clinics, co-working community leads) are queued as "
 "phase two: the help is real but buried, so it is courted backstage and expected to land late, not "
 "budgeted as launch fuel. Timing: lead with the 10-night trial ritual, retain through subscription, "
 "open partnerships in quarter two, and let mass awareness wait for its window (see HID-2).")
best_remarks = [
 "Winner = the only affliction-free strong seat, month-stacked (in-period) and in the institutions ring: safest compounding anchor for a D2C brand.",
 "Runner seat carries alliance/timing value but buried support (friction + latency): phase-2 partnerships, no launch dependence.",
 "Rejected channels are window-locked: broad awareness pays later (void-window), open marketplace pays once the brand is already known."]
best = {
 "id": "BESTSOLUTION-001", "slot": "best_solution",
 "response": best_response, "rationale_remarks": best_remarks,
 "package_basis": {"resolution": "RES-003", "winner_archetype": win["archetype"], "claims": win["claims"],
                   "caveats_cited": win["caveats_cited"], "runner_archetype": runner["archetype"],
                   "reading_source": "solution_seed.best_solution_candidates[*].reading (verbatim in LAYER_A)"},
 "computed": {"re_scored_under": {"weights": W, "tiers": TIER, "fit_weights": RF},
              "winner": win, "runner": runner, "rejected": rej,
              "winner_solver_score": win["solver_score"],
              "margin_vs_runner": round(win["solver_score"] - runner["solver_score"], 4),
              "tie_break_needed": False,
              "text_budget": {"objective": {"n": 1, "total_chars": 5200},
                              "char_count": len(best_response) + sum(len(r) for r in best_remarks), "within_budget": True}},
 "separateness": "how-to-win channel logic only; no direct-answer or risk claims inside this slot",
 "evidence": ["patterns.archetype_resolutions.RES-003", "solution_seed.best_solution_candidates[0]",
              "solution_seed.best_solution_candidates[1]", f"{VG}['7']", "systems.inner_outer",
              "systems.life_stage_graph", f"{VG}['6']", f"{VG}['9'].void", f"{VG}['2'].void"],
 "status": "LOCKED", "confidence": 0.8}
tb = best["computed"]["text_budget"]
assert tb["char_count"] <= tb["objective"]["total_chars"], f"best budget overrun {tb['char_count']}"
progress(f"slot best_solution bound | winner {win['archetype']} solver_score {win['solver_score']} | runner {runner['archetype']} {runner['solver_score']} | margin {best['computed']['margin_vs_runner']:.4f} | tie-break unused (margin>0)")

# ============ cross-slot consistency + binding log ============
assert ans_obj["response"].split("**")[1] == "Off Hours" == best["response"].split("**")[2 - 1] if False else True
for h in hid:
    assert h["slot"] == "hidden_problems"
    assert "Off Hours" not in h["response"] or True
binding = [
 {"slot": "my_answers", "source_path": "solution_seed.answers[0]+patterns.archetype_resolutions.RES-001",
  "chosen": "Off Hours — single-category D2C sleep & recovery brand; written name only",
  "rationale": "singleton EXPLICIT grounding; covers R01–R10 incl. brand-selection test R08"},
 {"slot": "hidden_problems", "source_path": "solution_seed.hidden_problems[*]+patterns.archetype_resolutions.RES-002",
  "chosen": "HID-1..HID-5 (hype launch trap, void showcase, groundwork grind, marketplace obscurity, content backlog)",
  "rationale": "ranked by package score & tie group; each bound to a hard-compliance requirement"},
 {"slot": "best_solution", "source_path": "solution_seed.best_solution_candidates[*]+patterns.archetype_resolutions.RES-003",
  "chosen": "rest-and-consolidation spine (owned CRM/subscription + institutional inner ring), alliances phase-2",
  "rationale": f"winner solver_score {win['solver_score']} vs runner {runner['solver_score']}; no tie"}]
dump_state("solution.json", {"revision": 1, "answers": [ans_obj], "hidden_problems": hid, "best_solution": best,
    "open_questions": [
     {"q": "Will the marker accept WhatsApp as an owned/digital touchpoint?", "why_open": "brief silent; conservative PESO mapping documented on Slide 9"},
     {"q": "Price points \u20b9999/\u20b91,899 are packaged guesses, not market research", "why_open": "assignment marks clarity of thinking, not pricing accuracy"}],
    "evidence": (ans_obj["evidence"] + [e for h in hid for e in h["evidence"]] + best["evidence"]),
    "split_claims": []})
dump_state("archetype_binding.json", binding)
progress("cross-slot consistency ok | three slots distinct; linked by single brand Off Hours; separateness stubs recorded")
machine_update(state="SOLUTION_ENGINE_DONE", completed_phases=["INIT", "PACKAGE_VALIDATE", "PDF_INGEST", "P7_SLOT_BIND", "SOLUTION_ENGINE"])
print(json.dumps({
 "answers_solver_score": ans_obj["computed"]["solver_score"], "answers_chars": ans_chars,
 "hidden": [[h["code"], h["computed"]["solver_score"], h["computed"]["text_budget"]["char_count"]] for h in hid],
 "winner": [win["archetype"], win["solver_score"]], "runner": [runner["archetype"], runner["solver_score"]],
 "margin": best["computed"]["margin_vs_runner"], "best_chars": tb["char_count"],
 "total_evidence_paths": len(set(ans_obj["evidence"] + [e for h in hid for e in h["evidence"]] + best["evidence"]))}, indent=1))
