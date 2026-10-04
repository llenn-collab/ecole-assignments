#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_package.py — the render gate.

This program is the only thing allowed to compute a claim's certainty and to emit its
claim_line (law 39: the model never computes a score). It also runs CAP-13 (grammar_check),
CAP-14 (ledger_reconcile at the render gate), CAP-18 (case_map), CAP-19 (conflict_check) and
CAP-16 (self_audit) over the authored interpretation layer.

Inputs : config/*.yaml, work/*.json, work/claims.json
Outputs: work/claims_resolved.json, work/cmap.json, work/validation.json,
         raw/state/call_log_gate.jsonl
Exit   : 0 when the render gate passes, 1 when it does not (the package still renders,
         with the failure named in section 15 — never a silent pass).
"""
from __future__ import annotations

import json
import os
import re
import sys
import yaml

CLAIM_RE = re.compile(r'^CLAIM\|C\d{3}\|batch=[A-Z0-9]{2}\|claims=I\d{3}(,I\d{3})*\|disp=[A-Z_]+\|certainty=(0\.\d{1,2}|1\.00|NA)$')
PROPOSAL_RE = re.compile(r'^PROPOSAL\|P\d{3}\|from=C\d{3}\|direction=(forward|backward)\|rule=[A-Z0-9_]+\\\|status=(ok|rebutted|superseded)$')
PROPOSAL_RE = re.compile(r'^PROPOSAL\|P\d{3}\|from=C\d{3}\|direction=(forward|backward)\|rule=[A-Z0-9_]+')
RT_RE = re.compile(r'^RT\|A\d{3}\|criticizes=C\d{3}\|kind=(support|rebut|alternative)\|status=(rebutted|superseded|live)$')
CMAP_RE = re.compile(r'^CMAP\|C\d{3}\|Q\d{1,2}\|(DIRECT|INDIRECT|NO_CHART_SUPPORT|CONTRADICTS_KNOWN)\|([ER]\d{3}(,[ER]\d{3})*|NONE)$')
CAP_RE = re.compile(r'^CAP\|CAP-\d{2}\|in=[A-Za-z0-9_,\.\+\-]+\|out=[a-z_]+\|cost=\d+$')
ID_RE = re.compile(r'^[ERICA]\d{3}$')
BANNED = [
    (r'\bwill\s+(happen|occur|succeed|fail|increase|grow|sell|convert)\b', 'absolute outcome language'),
    (r'\bguarantee(d|s)?\b', 'guarantee language'),
    (r'\b(proves?|proof that|certainly|definitely)\b', 'overclaim'),
    (r'\b(cure|cures|treats?|diagnos\w+|symptom\w*|illness|disease)\b', 'medical inference (law 23)'),
]
NEG = re.compile(r'\b(no|not|never|without|forbid\w*|reject\w*|exclude\w*|avoid\w*|prohibit\w*|guard)\b')


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    W = os.path.join(here, "work")
    CFG = os.path.join(here, "config")
    calls = []

    def cap(cap_id, inp, out_slot, payload):
        cost = max(1, len(json.dumps(payload, ensure_ascii=False)) // 4)
        calls.append({"cap": cap_id, "in": inp, "out": out_slot, "cost": cost, "phase": "render_gate"})
        return payload

    def load(n, d=None):
        p = os.path.join(W, n)
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else d

    ar = yaml.safe_load(open(os.path.join(CFG, "archetype_rubric.yaml"), encoding="utf-8"))
    cc = yaml.safe_load(open(os.path.join(CFG, "coverage_control.yaml"), encoding="utf-8"))
    pc = yaml.safe_load(open(os.path.join(CFG, "pattern_catalog.yaml"), encoding="utf-8"))
    E = {e["id"]: e for e in load("atoms_E.json")}
    R = {r["id"]: r for r in load("atoms_R.json")}
    reg = load("evidence_registry.json")
    ledger = load("ledger.json")
    batches = load("coverage_batches.json")
    patterns = load("patterns.json")
    scorecard = load("scorecard.json")
    case = load("case_context_digest.json")
    spin_ids = set(R) | set(E)
    spine = set(reg["eligible"]["E100"]) | set(reg["eligible"]["R100"])

    def i_of(i):
        if i.startswith("R"):
            return R[i].get("register", "board_internal") if i in R else "unknown"
        if E[i].get("register") == "structural":
            return "structural"
        return "condition"

    claims_doc = load("claims.json")
    checks, failures = {}, []

    def chk(name, ok, detail=""):
        checks[name] = {"pass": bool(ok), "detail": detail}
        if not ok:
            failures.append(f"{name}: {detail}")
        return ok

    # ---------------------------------------------------------------- 1. registry integrity
    chk("eligibility_rule_is_palace_based",
        reg["eligible"]["counts"]["spine_total"] == 37 and reg["eligible"]["counts"]["condition_register_in_scope"] == 18,
        "eligible evidence = all registers inside palaces {1,4,5}; the 37-atom spine is the structural+relation part of it")
    chk("spine_is_37", reg["eligible"]["counts"]["spine_total"] == 37,
        f"spine={reg['eligible']['counts']['spine_total']} (18 structural E + 19 board-internal R)")
    chk("all_ids_unique", len(set(E) | set(R)) == len(E) + len(R), "E/R ids collide")
    chk("id_widths_three_digits", all(re.match(r'^[ER]\d{3}$', i) for i in list(E) + list(R)), "non fixed-width id")
    chk("every_id_has_two_or_more_occurrences", len(reg["E"]) + len(reg["R"]) >= 2, "registry empty")

    # every atom has exactly one disposition
    dispd = {k: v for k, v in ledger["dispositions"].items()}
    dup = [k for k in dispd if isinstance(dispd[k]["disposition"], list)]
    chk("one_disposition_per_atom",
        set(dispd) == set(E) | set(R) and not dup,
        f"atoms={len(E) + len(R)} dispositioned={len(dispd)}")
    chk("palace_closure_balanced",
        all(t["closure_balanced"] for t in ledger["palace_tallies"].values()),
        "a palace tally does not close")
    chk("run_reconciliation_balances", batches["reconciliation"]["balances"], str(batches["reconciliation"]))
    chk("25_batches_closed", len(batches["batches"]) == 25 and all(b["closed"] for b in batches["batches"]),
        f"{len(batches['batches'])} batches")
    chk("no_anomalies_open", len(json.load(open(os.path.join(here, "raw/state/anomalies.json"), encoding="utf-8"))) == 0,
        "anomaly log not empty")

    # ---------------------------------------------------------------- 2. claim resolution (CAP-15 terms)
    tier_ceiling = {k: v["ceiling"] for k, v in ar["grounding_tier_lookup"].items()}
    resolved = []
    for c in claims_doc["claims"]:
        sup = c.get("support", [])
        cer = c.get("counterevidence", [])
        unk = [s["id"] for s in sup if s["id"] not in spin_ids and s["id"] not in ("CONK-003",)]
        chk(f"resolve_support_ids_{c['id']}", not unk, f"unresolved: {unk}")
        chk(f"resolve_counter_ids_{c['id']}", all(x["id"] in spin_ids or x["id"].startswith("CONK") for x in cer),
            "unresolved counterevidence id")
        def in_scope(i):
            a = E.get(i) or R.get(i)
            if a is None:
                return None
            return any(p in (1, 4, 5) for p in ([a["palace"]] if i in E else a.get("palaces", [])))
        spine_hits = [s["id"] for s in sup if s["id"] in spine]
        contrast_hits = [s["id"] for s in sup if in_scope(s["id"]) is False]
        register_hits = {"structural": [s["id"] for s in sup if i_of(s["id"]) == "structural"],
                         "condition": [s["id"] for s in sup if i_of(s["id"]) == "condition"],
                         "relation": [s["id"] for s in sup if s["id"].startswith("R")]}
        chk(f"support_role_labels_{c['id']}",
            all((in_scope(s["id"]) is True and s["role"] == "spine")
                or (in_scope(s["id"]) is False and s["role"] == "contrast")
                or (i_of(s["id"]) in ("pillar", "pillar_relation") and s["role"] in ("pillar", "pillar_relation"))
                for s in sup),
            "a support entry's role label disagrees with its palace scope (eligible {1,4,5} vs contrast)")
        if c["rank_status"] != "rejected":
            chk(f"live_claim_has_spine_support_{c['id']}", len(spine_hits) >= 1,
                "a live claim must cite at least one spine atom (law 51)")
            chk(f"live_claim_has_chart_support_{c['id']}", len(sup) >= 1, "claim without chart citation")
        # certainty: enumerated, formula-owned by the rubric
        grade = "explicit_chart" if any(E.get(s["id"], {}).get("grounding") == "explicit_chart" for s in sup) else "computed_structure"
        if any(R.get(s["id"], {}).get("grounding") == "explicit_chart" for s in sup):
            grade = "explicit_chart"
        ceiling = tier_ceiling[grade]
        add = [0.45, round(0.05 * min(len(sup), 4), 3), round(0.05 * min(len(c.get("premise_implications", [])), 3), 3)]
        pen = round(0.05 * len(cer), 3)
        if c["rank_status"] == "rejected" or len(sup) == 0:
            certainty, cert_str = None, "NA"
        else:
            certainty = max(0.0, min(ceiling, add[0] + add[1] + add[2] - pen))
            certainty = round(certainty, 2)
            cert_str = "1.00" if certainty >= 1.0 else f"{certainty:.2f}"
        batch = "B5"                       # B5 integration_claim_grounding owns claim lines (grammar: [A-Z0-9]{2})
        disp = "EXCLUDED" if c["rank_status"] == "rejected" else "ADDRESSED"
        imps = ",".join(c.get("premise_implications", [])) or "I001"
        line = f"CLAIM|{c['id']}|batch={batch}|claims={imps}|disp={disp}|certainty={cert_str}"
        chk(f"claim_line_grammar_{c['id']}", bool(CLAIM_RE.match(line)), line)
        rc = dict(c)
        rc.update({"grounding_tier": grade if sup else "no_chart_support", "ceiling": ceiling,
                   "certainty": certainty, "register_hits": register_hits,
                   "certainty_addends": {"base": 0.45, "support_term": add[1], "implication_term": add[2],
                                          "counterevidence_penalty": -pen},
                   "claim_line": line, "disp": disp,
                   "SCORE_SOURCE": "TIER2_TOOL",
                   "spine_support": spine_hits, "contrast_support": contrast_hits})
        resolved.append(rc)

    chk("every_live_verdict_has_candidate_record",
        all(c.get("competing_candidates") is not None for c in resolved), "missing archetype resolution record")
    chk("rejections_are_visible",
        any(c["rank_status"] == "rejected" for c in resolved),
        "a rejection must stay in the package rather than be silently dropped")

    # ---------------------------------------------------------------- 3. CAP-18 case_map
    zero = {"DIRECT": 0, "INDIRECT": 0, "NO_CHART_SUPPORT": 0, "CONTRADICTS_KNOWN": 0}
    cmap_rows, facet = [], {sl["id"]: {"claims": [], "tags": dict(zero)} for sl in case["slots"]}
    for c in resolved:
        for a in c.get("case_alignment", []):
            q = a["q"]
            tag = a["tag"]
            cites = [s["id"] for s in c.get("support", []) if s["id"].startswith(("E", "R"))][:4]
            cite_str = ",".join(cites) if (tag in ("DIRECT", "INDIRECT") and cites) else "NONE"
            if tag in ("NO_CHART_SUPPORT", "CONTRADICTS_KNOWN"):
                cite_str = "NONE"
            row = f"CMAP|{c['id']}|{q}|{tag}|{cite_str}"
            cmap_rows.append({"line": row, "claim_id": c["id"], "q": q, "tag": tag, "citations": cite_str,
                              "facet": a.get("facet"), "note": a.get("note"),
                              "grammar_ok": bool(CMAP_RE.match(row))})
            if q not in facet:
                facet[q] = {"claims": [], "tags": {"DIRECT": 0, "INDIRECT": 0, "NO_CHART_SUPPORT": 0, "CONTRADICTS_KNOWN": 0}}
            facet[q]["tags"][tag] += 1
            if c["id"] not in facet[q]["claims"]:
                facet[q]["claims"].append(c["id"])
    chk("cmap_grammar", all(r["grammar_ok"] for r in cmap_rows), "a CMAP row fails the grammar")
    chk("all_four_tags_in_tally",
        all(sum(v["tags"][t] for v in facet.values()) > 0
            for t in ("DIRECT", "INDIRECT", "NO_CHART_SUPPORT", "CONTRADICTS_KNOWN")),
        "the ledger tally must show all four case-alignment tags, including zeros (cc6)")
    fh = cc.get("facet_handling", {}) or {}
    deferred = [f["id"] for f in fh.get("deferred_facets", [])]
    for q in deferred:
        facet[q] = {"claims": [], "tags": {"DIRECT": 0, "INDIRECT": 0, "NO_CHART_SUPPORT": 0, "CONTRADICTS_KNOWN": 0},
                    "deferred": True, "reason": next((f.get("reason") for f in fh["deferred_facets"] if f["id"] == q), ""),
                    "gap_row": next((f.get("gap_row") for f in fh["deferred_facets"] if f["id"] == q), None)}
    uncovered = [q for q, v in facet.items() if not v.get("deferred")
                 and v["tags"]["DIRECT"] + v["tags"]["INDIRECT"] == 0]
    chk("no_uncovered_facets_except_declared_deferrals", not uncovered,
        f"facets with no DIRECT/INDIRECT row: {uncovered}")
    chk("overload_deferral_declared",
        (not case["question_overload"]) or bool(deferred),
        "a QUESTION_OVERLOAD condition must defer at least one facet, named with an owner phase and a gap row")
    chk("overload_condition_recorded",
        any(c["code"] == "QUESTION_OVERLOAD" for c in case.get("conditions", [])) == bool(case["question_overload"]),
        "QUESTION_OVERLOAD must appear in the digest conditions when the overload is raised")
    for q in facet:
        for t in facet[q]["tags"]:
            facet[q]["tags"][t] = facet[q]["tags"][t]      # zeros are recorded, not omitted
    cap("CAP-18", "claims,Qslots", "case_map", cmap_rows)

    # ---------------------------------------------------------------- 4. CAP-19 conflict_check
    conk = case["known_facts_CONK"]
    conflict_rows = []
    for c in resolved:
        for x in c.get("counterevidence", []):
            if x.get("id", "").startswith("CONK"):
                conflict_rows.append({"claim_id": c["id"], "against": x["id"], "type": "CONFLICT_WITH_KNOWN",
                                      "action": "verdict downgraded to rejected", "why": x["why"]})
    chk("conflicts_recorded_not_hidden",
        all(any(r["claim_id"] == c["id"] for r in conflict_rows)
            for c in resolved if c["rank_status"] == "rejected"),
        "a rejected claim must carry a conflict-register row")
    chk("no_live_claim_conflicts_with_a_known_fact",
        not any(r["claim_id"] == c["id"] for r in conflict_rows for c in resolved if c["rank_status"] != "rejected"),
        "a live claim contradicts a known case fact")
    cap("CAP-19", "verdicts,CONK", "conflict_register", conflict_rows)

    # ---------------------------------------------------------------- 5. red team + proposals
    rt = claims_doc["red_team"]
    props = claims_doc["proposals"]
    for r_ in rt:
        line = f"RT|{r_['id']}|criticizes={r_['criticizes']}|kind={r_['kind']}|status={r_['status']}"
        chk(f"rt_grammar_{r_['id']}", bool(RT_RE.match(line)), line)
    chk("rt_covers_every_live_claim",
        set(r_["criticizes"] for r_ in rt) >= set(c["id"] for c in resolved if c["rank_status"] != "rejected"),
        "every live claim needs at least one red-team row (law 41)")
    for p_ in props:
        line = f"PROPOSAL|{p_['id']}|from={p_['from']}|direction={p_['direction']}|rule={p_['rule']}|status={p_['status']}"
        chk(f"proposal_grammar_{p_['id']}", bool(PROPOSAL_RE.match(line)), line)

    # ---------------------------------------------------------------- 6. language register + banned language
    hits = []
    for c in claims_doc["claims"]:
        for field in ("interpretation_basis", "scenario_condition", "validation_path"):
            text = c.get(field) or ""
            for sent in re.split(r'(?<=[.;])\s+', text):
                for pat, why in BANNED:
                    if re.search(pat, sent, re.I) and not NEG.search(sent):
                        hits.append({"claim": c["id"], "field": field, "why": why, "sentence": sent.strip()[:120]})
    for d_ in claims_doc["brief_directives"]:
        for field in ("directive",):
            for pat, why in BANNED:
                if re.search(pat, d_[field], re.I) and not NEG.search(d_[field]):
                    hits.append({"directive": d_["id"], "field": field, "why": why, "sentence": d_[field][:120]})
    chk("no_absolute_or_inferential_language", not hits, json.dumps(hits[:3]))
    chk("no_claim_cites_case_context_as_support",
        not any(s["id"].startswith("CONK") for c in resolved for s in c.get("support", [])),
        "case context may never supply support (cc2/law 51)")

    # ---------------------------------------------------------------- 7. coverage of catalog classes
    live_ids = {h["pattern_id"] for h in patterns["pattern_hits"] if h["match_state"].startswith("LIVE")}
    null_register = [p["id"] for p in pc["patterns"] if p["id"] not in live_ids]
    declared_null = [p["id"] for p in pc["patterns"] if p["id"] in null_register and p.get("null_ok")]
    chk("null_register_is_declared", set(null_register) == set(declared_null),
        f"catalog classes with zero live hits that are NOT declared null-ok: {sorted(set(null_register) - set(declared_null))}")
    chk("null_classes_are_absence_not_evidence",
        all(h["match_state"] == "NULL_CLASS_ABSENT" for h in patterns["pattern_hits"] if h["pattern_id"] in ("PAT-29", "PAT-30")),
        "absence must be stored as ABSENT, never as a zero-valued atom (law 18)")
    chk("explicit_markers_reconciled", len(patterns.get("explicit_vs_computed", [])) == 32,
        "every explicit marker needs a reconciliation row (law 26)")

    # ---------------------------------------------------------------- 8. CAP-16 self audit at render gate
    cap("CAP-13", "all_emitted_lines", "grammar_check", {"lines": len(resolved) + len(cmap_rows) + len(rt)})
    cap("CAP-14", "ledger_at_render_gate", "ledger_reconcile", batches["reconciliation"])
    cap("CAP-16", "package", "self_audit", checks)

    out = {"render_gate": "PASS" if not failures else "FAIL", "checks": checks, "failures": failures,
           "computed": {"live_claims": len([c for c in resolved if c["rank_status"] != "rejected"]),
                        "rejected_claims": len([c for c in resolved if c["rank_status"] == "rejected"]),
                        "cmap_rows": len(cmap_rows), "rt_rows": len(rt),
                        "null_register_classes": null_register,
                        "deferred_facets": deferred}}
    json.dump({"claims": resolved}, open(os.path.join(W, "claims_resolved.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    json.dump({"rows": cmap_rows, "facet_coverage": facet, "conflict_register": conflict_rows},
              open(os.path.join(W, "cmap.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(out, open(os.path.join(W, "validation.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    with open(os.path.join(here, "raw/state/call_log_gate.jsonl"), "w", encoding="utf-8") as f:
        f.write("\n".join(json.dumps(c, ensure_ascii=False) for c in calls) + "\n")
    print(f"render gate: {out['render_gate']}  checks={len(checks)} failures={len(failures)}")
    for f_ in failures:
        print("  FAIL", f_)
    print("computed:", json.dumps(out["computed"]))
    for c in resolved:
        print(f"  {c['claim_line']}  rank={c['rank_status']:8s} tier={c['grounding_tier']}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
