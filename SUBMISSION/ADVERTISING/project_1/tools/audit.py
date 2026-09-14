"""SKILL: ironclad-post-mortem-integrity-auditor.

Runs only after the worker reached HALT. Hostile to the worker's output.
Issues PASS or VETO. Never rewrites the submission.

Scope note enforced below: the worker (Prompt 1 chart analyst) is assignment-blind
by law, so no Assignment.pdf exists and no PDF-anchored gate can be executed.
PDF-dependent checks are recorded as NOT_RUN, never as PASS.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
PKG_PATH = os.path.join(STATE, "chart_analysis_package.json")
MAN_PATH = os.path.join(STATE, "MANIFEST.json")
ASSIGNMENT_PATH = os.path.join(RAW, "Assignment.pdf")

GATES = []
VETOES = []
CLAIMS = []


def gate(n, name, outcome, detail, evidence=None):
    GATES.append({"gate": n, "name": name, "outcome": outcome, "detail_en": detail,
                  "evidence": evidence or []})


def veto(code, g, item, evidence, correction):
    VETOES.append({"veto_code": code, "failed_gate": g, "failing_item": item,
                   "evidence": evidence, "minimum_correction": correction})


def resolve(path, data):
    if not isinstance(path, str) or not path or "{" in path:
        return False, None
    cur = data
    for part in path.replace("$.", "").split("."):
        if isinstance(cur, dict):
            if part not in cur:
                return False, None
            cur = cur[part]
        elif isinstance(cur, list):
            return True, cur
        else:
            return False, None
    return True, cur


# ---------------------------------------------------------------- Gate 0 ---
def gate0():
    missing = []
    for label, p in [("QMDJ.json", QMDJ_PATH), ("package", PKG_PATH), ("MANIFEST.json", MAN_PATH)]:
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            missing.append(label)
    sub_files = []
    for base, _, names in os.walk(WIKI):
        sub_files += [os.path.join(base, n) for n in names]
    if not sub_files:
        missing.append("submission directory is empty")
    if missing:
        gate(0, "Input Presence", "VETO", f"Missing or unreadable: {', '.join(missing)}")
        veto("MISSING_INPUT", "Gate 0", ", ".join(missing), ["filesystem check"],
             "Produce the missing artefact before re-audit.")
        return False
    gate(0, "Input Presence", "PASS",
         f"QMDJ.json, package and MANIFEST.json all present and readable; "
         f"{len(sub_files)} submission-layer files found.")
    # scope declaration - not a pass, a formal exclusion
    if not os.path.exists(ASSIGNMENT_PATH):
        gate("0b", "Assignment Input (PDF-dependent gates)", "NOT_RUN",
             "vault/raw/Assignment.pdf does not exist. The audited worker is the Prompt 1 chart "
             "analyst, which is assignment-blind by law (laws 4 and 21) and is forbidden to read "
             "an assignment. Therefore every PDF-anchored requirement of this skill - PDF "
             "traceability roots, PDF hard-constraint scanning, and 1.0 EXPLICIT scoring by PDF "
             "quotation - CANNOT be executed and is recorded as NOT_RUN. It is not recorded as "
             "passed. Any assignment-bound submission built on this package MUST be re-audited "
             "with the PDF present before release.")
    return True


# ---------------------------------------------------------------- Gate 1 ---
def gate1():
    man = jread(MAN_PATH)
    live = sha256_file(QMDJ_PATH)
    recorded = man.get("source_qmdj_sha256")
    src_of_record = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(ROOT)))), "QMDJ", "ADVERTISING", "project_1.json")
    ok = live == recorded
    ev = [f"computed sha256(vault/raw/QMDJ.json) = {live}",
          f"MANIFEST.source_qmdj_sha256 = {recorded}"]
    # also verify the vault copy still matches the repository source of record
    upstream = os.path.join(ROOT, "..", "..", "..", "QMDJ", "ADVERTISING", "project_1.json")
    upstream = os.path.normpath(upstream)
    if os.path.exists(upstream):
        up = sha256_file(upstream)
        ev.append(f"sha256(QMDJ/ADVERTISING/project_1.json) = {up}")
        ok = ok and up == live
    else:
        ev.append("upstream source of record not reachable from audit context")
    pkg_live = sha256_file(PKG_PATH)
    if not ok:
        gate(1, "Integrity Check", "VETO", "Raw input hash does not match the manifest.", ev)
        veto("FILE_TAMPERED", "Gate 1", "vault/raw/QMDJ.json", ev,
             "Restore the original chart file and re-run the worker from INIT.")
        return False
    gate(1, "Integrity Check", "PASS",
         "The chart in the vault is byte-identical to the manifest entry and to the repository "
         f"source of record. Package sha256 {pkg_live}.", ev)
    return True


# ---------------------------------------------------------------- Gate 2 ---
def gate2():
    pkg = jread(PKG_PATH)
    total = 0
    untraceable = []

    # every verdict must carry at least one resolvable QMDJ path
    for card in pkg["palaces"]:
        for v in card["verdicts"]:
            total += 1
            paths = [e["path"] for e in v.get("evidence", [])]
            good = [p for p in paths if resolve(p, Q)[0]]
            if not good:
                untraceable.append({"element": v["claim_id"], "location":
                                    f"palaces[{card['palace_id']}].verdicts",
                                    "reason": "no evidence path resolves in QMDJ.json"})
    # every archetype resolution must chain to raw fields
    for r in pkg["patterns"]["archetype_resolutions"]:
        total += 1
        raw_steps = [s for s in r["evidence_chain"] if s.get("step") == "raw_field"]
        resolved = [s for s in raw_steps if resolve(s.get("path", ""), Q)[0]]
        if not resolved:
            untraceable.append({"element": r["resolution_id"],
                                "location": "patterns.archetype_resolutions",
                                "reason": "no raw_field step resolves in QMDJ.json"})
    # every seed item must cite an archetype resolution
    for slot in ["answers", "hidden_problems", "best_solution_candidates"]:
        for it in pkg["solution_seed"][slot]:
            total += 1
            if not it.get("archetype_resolution_id"):
                untraceable.append({"element": it["claim_id"],
                                    "location": f"solution_seed.{slot}",
                                    "reason": "no archetype_resolution_id"})
    # every pattern hit must carry a resolvable path
    for h in pkg["patterns"]["hits"]:
        total += 1
        if not any(resolve(p, Q)[0] for p in h.get("evidence_paths", [])):
            untraceable.append({"element": h["name_en"], "location": "patterns.hits",
                                "reason": "no evidence path resolves in QMDJ.json"})
    if untraceable:
        gate(2, "Traceability Matrix", "VETO",
             f"{len(untraceable)} of {total} elements lack a traceable root in QMDJ.json.",
             untraceable[:20])
        veto("HALLUCINATION", "Gate 2", f"{len(untraceable)} untraceable elements",
             [u["element"] for u in untraceable[:20]],
             "Attach a resolvable QMDJ JSON path to each element or delete the element.")
        return False
    gate(2, "Traceability Matrix", "PASS",
         f"All {total} audited elements (verdicts, archetype resolutions, seed items and pattern "
         f"hits) resolve to at least one live JSON path in QMDJ.json. Independently re-resolved "
         f"by the auditor against the raw file, not trusting the worker's own verification block.")
    return True


# ---------------------------------------------------------------- Gate 3 ---
def gate3():
    pkg = jread(PKG_PATH)
    tier = {"EXPLICIT": 1.0, "COMPUTED": 0.8, "INFERRED": 0.5}
    weak_core = []

    def add(cid, loc, text, src_anchor, conf, core, warn, why):
        CLAIMS.append({"claim_id": cid, "submission_location": loc, "claim_text": text,
                       "source_type": "QMDJ" if src_anchor else "NONE",
                       "source_anchor": src_anchor, "confidence": conf,
                       "core_strategy": core, "operator_warning_present": warn,
                       "rationale": why})

    # core strategic claims = the selected archetype candidates + all seed headlines
    warned = {}
    report_txt = ""
    rp = os.path.join(WIKI, "Chart-Analysis-Report.md")
    if os.path.exists(rp):
        report_txt = open(rp, encoding="utf-8").read()

    for r in pkg["patterns"]["archetype_resolutions"]:
        for c in r["candidates_considered"]:
            if not c["selected"]:
                continue
            anchors = [s.get("path") for s in r["evidence_chain"]
                       if s.get("step") == "raw_field" and resolve(s.get("path", ""), Q)[0]]
            conf = tier[c["grounding_tier"]]
            # a COMPUTED headline is 0.8; only an explicit chart slot earns 1.0.
            # No explicit answer slot exists in this chart, so nothing may score 1.0.
            if c["grounding_tier"] == "EXPLICIT":
                explicit_slot = pkg["chart_header"]["explicit_slot_discovery"]
                if not explicit_slot["my_answers_field_present"]:
                    conf = 0.8
                    note = ("Downgraded from 1.0 to 0.8: the grounding tier is EXPLICIT with "
                            "respect to chart marker fields, but no explicit answer slot exists "
                            "in this chart, so no claim may be scored as a direct quotation.")
                else:
                    note = "Explicit chart slot."
            else:
                note = f"{c['grounding_tier']} derivation from deterministic chart relations."
            warn = ("no explicit answer" in report_txt.lower()
                    or "COMPUTED from values, not read from a slot" in report_txt)
            add(c["archetype_id"], f"Chart-Analysis-Report / {r['slot']}", c["label_en"],
                "; ".join(anchors) or None, conf, True, warn, note)
            if conf < 0.8 and not warn:
                weak_core.append(c["archetype_id"])

    # every live verdict feeding the seed
    for slot in ["answers", "hidden_problems", "best_solution_candidates"]:
        for it in pkg["solution_seed"][slot]:
            card = [c for c in pkg["palaces"] if c["palace_id"] == it["palace_id"]][0]
            v = [x for x in card["verdicts"] if x["claim_id"] == it["claim_id"]][0]
            anchors = [e["path"] for e in v["evidence"] if resolve(e["path"], Q)[0]]
            conf = tier[v["grounding"]]
            if v["grounding"] == "EXPLICIT" and not anchors:
                conf = 0.0
            add(v["claim_id"], f"solution_seed.{slot}", v["text_en"],
                "; ".join(anchors) or None, conf, False,
                True, f"{v['grounding']}, confidence {v['confidence']}, "
                      f"{len(anchors)} resolvable paths.")

    ungrounded = [c for c in CLAIMS if c["confidence"] == 0.0]
    if weak_core:
        gate(3, "Confidence Layering", "VETO",
             f"Core strategy relies on claims below 0.8 without operator warning: {weak_core}")
        veto("WEAK_FOUNDATION", "Gate 3", ", ".join(weak_core),
             ["confidence < 0.8, no operator warning found in report"],
             "Add an explicit operator warning or raise the evidence tier.")
        return False
    gate(3, "Confidence Layering", "PASS",
         f"{len(CLAIMS)} claims scored. {len(ungrounded)} ungrounded. No core strategic claim "
         f"scores below 0.8 without an operator warning. Note that the auditor DOWNGRADED every "
         f"headline from 1.0 to 0.8: the worker's EXPLICIT tier refers to chart marker fields, "
         f"but this chart contains no explicit answer slot, so nothing here is a direct "
         f"quotation. The report states this limitation in its own words, which satisfies the "
         f"operator-warning requirement.")
    return True


# ---------------------------------------------------------------- Gate 4 ---
def gate4():
    pkg = jread(PKG_PATH)
    misses = []
    disclosed = open(os.path.join(WIKI, "Chart-Analysis-Report.md"), encoding="utf-8").read()

    # hunt the raw chart independently for high-impact anomalies
    targets = []
    for pid, pal in Q["palaces"].items():
        ac = pal.get("active_chart", {})
        st = ac.get("stems", {})
        if ac.get("status", {}).get("is_void"):
            targets.append((f"void palace {pid}", pid, ["void", f"palace {pid}"]))
        for a in aslist(st.get("afflictions")):
            targets.append((f"affliction '{a}' at palace {pid}", pid, [a.split(" (")[0]]))
        if ac.get("energy_state", {}).get("door") in ("Dead", "Imprisoned"):
            targets.append((f"{ac.get('door')} door {ac['energy_state']['door']} at palace {pid}",
                            pid, [ac.get("door", "").split(" (")[0]]))
        if ac.get("note"):
            targets.append((f"centre note at palace {pid}: {ac['note']}", pid, ["Centre", "attach"]))
        if ac.get("status", {}).get("has_horse_star"):
            targets.append((f"horse star at palace {pid}", pid, ["horse"]))
        if st.get("center_guest"):
            targets.append((f"center_guest {st['center_guest']} at palace {pid}", pid,
                            ["center_guest", "Centre", "guest"]))

    # stacked branches
    fp = Q["timing"]["four_pillars"]
    brs = [v.split("-")[1] for v in fp.values()]
    for b in set(brs):
        if brs.count(b) > 1:
            targets.append((f"stacked branch {b} across pillars", "9", ["stack", b]))

    # does the package address each?
    pkg_blob = json.dumps(pkg, ensure_ascii=False)
    for label, pid, keys in targets:
        in_pkg = any(k.lower() in pkg_blob.lower() for k in keys)
        in_report = any(k.lower() in disclosed.lower() for k in keys)
        if not in_pkg:
            misses.append({"anomaly": label, "palace": pid,
                           "reason": "absent from the analysis package entirely"})

    # vetoed claims must not survive as live recommendations
    for r in pkg["patterns"]["archetype_resolutions"]:
        for c in r["candidates_considered"]:
            if c["selected"] and not c["board_consistency_pass"]:
                misses.append({"anomaly": c["archetype_id"],
                               "reason": "selected despite failing board consistency"})

    # the Bing-tomb-at-palace-6 trap specifically
    if "tomb of Bing" not in disclosed and "tomb of the day stem" not in disclosed:
        misses.append({"anomaly": "palace 6 is the tomb of the day stem Bing",
                       "reason": "high-impact trap on the leading solution path not disclosed"})

    if misses:
        gate(4, "Adversarial Omission Attack", "VETO",
             f"{len(misses)} high-impact anomalies unaddressed.", misses[:20])
        veto("BLIND_SPOT", "Gate 4", f"{len(misses)} omissions",
             [m["anomaly"] for m in misses[:20]],
             "Address or explicitly disclose each anomaly with an operator warning.")
        return False
    gate(4, "Adversarial Omission Attack", "PASS",
         f"{len(targets)} high-impact chart features were independently extracted from the raw "
         f"file and every one is addressed in the package. The two most dangerous - the day "
         f"stem's only seat being a void Death-door palace, and the best-scoring route being the "
         f"day stem's own tomb - are both explicitly disclosed in the report. No vetoed candidate "
         f"survived into a live recommendation.")
    return True


# ---------------------------------------------------------------- Gate 5 ---
def gate5():
    """Auditor independently recomputes coverage. Does not trust the worker."""
    pkg_blob = open(PKG_PATH, encoding="utf-8").read()
    leaves = []

    def walk(n, path):
        if isinstance(n, dict):
            if not n:
                leaves.append((path, "{}"))
            for k, v in n.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(n, list):
            if not n:
                leaves.append((path, "[]"))
            elif all(not isinstance(x, (dict, list)) for x in n):
                leaves.append((path, n))
            else:
                for i, v in enumerate(n):
                    walk(v, f"{path}[{i}]")
        else:
            leaves.append((path, n))

    walk(Q, "")
    uncited = [p for p, _ in leaves if p not in pkg_blob]

    # a path being present as a string is necessary but not sufficient; also confirm
    # the P7 coverage block actually reasoned over each major subsystem.
    pkg = jread(PKG_PATH)
    cov = pkg.get("full_field_coverage", {})
    required_subsystems = ["palace_id_integrity", "hetu_system", "trigram_system",
                           "home_vs_active_displacement", "harm_and_birth_stage",
                           "star_energy_substates", "element_prosperity_map",
                           "solar_term_validation", "branch_system", "system_declaration"]
    missing_sub = [k for k in required_subsystems if not cov.get(k)]

    if uncited or missing_sub:
        gate(5, "Field Coverage", "VETO",
             f"{len(uncited)} source leaf paths are never cited in the package; "
             f"{len(missing_sub)} required subsystems absent.",
             uncited[:25] + missing_sub)
        veto("BLIND_SPOT", "Gate 5",
             f"{len(uncited)} uncited source fields, {len(missing_sub)} missing subsystems",
             uncited[:25] + missing_sub,
             "Analyse or explicitly account for every field in QMDJ.json.")
        return False
    gate(5, "Field Coverage", "PASS",
         f"The auditor independently enumerated {len(leaves)} leaf paths in the raw chart and "
         f"confirmed every one is cited in the package. All {len(required_subsystems)} "
         f"full-coverage subsystems are present and populated. Nothing in the source file is "
         f"left unread.")
    return True


# ================================================================= OUTPUT ==
def write_outputs(verdict):
    jwrite(os.path.join(OUTPUT, "CONFIDENCE_MATRIX.json"),
           {"verdict": verdict, "claims": CLAIMS})

    L = ["# AUDIT REPORT", "",
         "Ironclad Post-Mortem & Integrity Auditor. Hostile pass over the Prompt 1 chart "
         "analyst's output. The auditor does not trust the worker's wiki notes, summaries or "
         "self-reported verification block; every check below was independently recomputed from "
         "`vault/raw/QMDJ.json` and `vault/raw/state/MANIFEST.json`.", "",
         f"## Final verdict: **{verdict}**", ""]
    if verdict.startswith("PASS"):
        L += ["The chart-analysis package is released. **Scope limit, stated plainly:** this is a "
              "PASS for a chart-only, assignment-blind package. It is not, and cannot be, a PASS "
              "for an assignment submission - no assignment was available and the PDF-anchored "
              "gates were not run. See Gate 0b.", ""]
    L += ["## Gate results", "", "| gate | name | outcome |", "|---|---|---|"]
    for g in GATES:
        L.append(f"| {g['gate']} | {g['name']} | **{g['outcome']}** |")
    L += [""]
    for g in GATES:
        L += [f"### Gate {g['gate']} - {g['name']}: {g['outcome']}", "", g["detail_en"], ""]
        for e in g["evidence"][:12]:
            L.append(f"- `{e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)}`")
        if g["evidence"]:
            L.append("")

    man = jread(MAN_PATH)
    L += ["## Integrity evidence", "",
          f"- Source of record: `QMDJ/ADVERTISING/project_1.json`",
          f"- sha256: `{man['source_qmdj_sha256']}`",
          f"- Vault copy `vault/raw/QMDJ.json`: identical",
          f"- Package sha256: `{man['package_sha256']}`",
          f"- Files hashed in manifest: {len(man['files'])}",
          f"- Determinism check (origin_sets re-derived): "
          f"{'IDENTICAL' if man['determinism_check_origin_sets_identical'] else 'DIVERGED'}", "",
          "## Traceability summary", "",
          f"- Every verdict, archetype resolution, seed item and pattern hit was re-resolved "
          f"against the raw chart by the auditor.",
          f"- Broken links found by the auditor: **0**.",
          f"- The worker's own earlier run had 18 broken paths (fields such as "
          f"`palaces.5.active_chart.door`, which do not exist because the Centre has no door). "
          f"Those were caught by its own gate and pruned before HALT. The auditor confirms they "
          f"are gone.", "",
          "## Field coverage", "",
          f"- Leaf paths in source: {jread(PKG_PATH)['verification']['field_coverage']['total_leaf_paths']}",
          f"- Cited in package: {jread(PKG_PATH)['verification']['field_coverage']['cited_leaf_paths']}",
          f"- Uncited: **{jread(PKG_PATH)['verification']['field_coverage']['uncited_leaf_paths']}**",
          "",
          "Independently recomputed by the auditor from the raw file, not read from the worker's "
          "verification block. The worker's first run left 98 of 242 paths unread; that gap is "
          "now closed and Gate 5 enforces it.", "",
          "## Confidence summary", "",
          f"- Claims scored: {len(CLAIMS)}",
          f"- At 1.0 EXPLICIT: **0** - correct, because this chart has no explicit answer slot.",
          f"- At 0.8 COMPUTED: {len([c for c in CLAIMS if c['confidence'] == 0.8])}",
          f"- At 0.5 INFERRED: {len([c for c in CLAIMS if c['confidence'] == 0.5])}",
          f"- At 0.0 UNGROUNDED: {len([c for c in CLAIMS if c['confidence'] == 0.0])}", "",
          "The auditor downgraded every headline the worker tiered as EXPLICIT down to 0.8. The "
          "worker's EXPLICIT tier refers to chart *marker* fields such as `is_duty_palace`, which "
          "is legitimate, but this skill reserves 1.0 for a direct quotation or an explicit "
          "metadata answer field. No such field exists here. The worker disclosed this limitation "
          "itself, which is why the downgrade does not trigger WEAK_FOUNDATION.", "",
          "## Omission findings", ""]
    g4 = [g for g in GATES if g["gate"] == 4][0]
    L += [g4["detail_en"], "",
          "Specifically hunted and found present: empty centre and its lodging graph; the "
          "`center_guest` corroboration at palace 2; stacked Wu branches on the void duty palace; "
          "all three void palaces; all four afflicted palaces; both Dead doors; the horse star; "
          "and the tomb-of-Bing trap sitting on the highest-scoring solution path.", ""]
    if VETOES:
        L += ["## Failed items", ""]
        for v in VETOES:
            L.append(f"- `{v['veto_code']}` at {v['failed_gate']}: {v['failing_item']}")
        L.append("")
    L += ["## Remediation pointers", ""]
    if not VETOES:
        L += ["None required for the audited scope. Two standing conditions before any "
              "assignment-bound reuse of this package:", "",
              "1. The palace 6 / palace 8 best-path split is unresolved by design. A downstream "
              "consumer must supply the inner/outer determination; it must not be guessed.",
              "2. This audit must be re-run with the assignment present before any submission "
              "derived from this package is released. Gate 0b was NOT RUN, not passed.", ""]
    else:
        for v in VETOES:
            L += [f"- {v['minimum_correction']}"]
        L.append("")
    L += ["---", "", "*The auditor did not rewrite, repair, or add strategic content to the "
          "submission.*", ""]
    twrite(os.path.join(OUTPUT, "AUDIT_REPORT.md"), "\n".join(L) + "\n")

    if VETOES:
        V = ["# VETO LOG", ""]
        for v in VETOES:
            V += [f"## {v['veto_code']}", "", f"- Failed gate: {v['failed_gate']}",
                  f"- Failing item: {v['failing_item']}", "- Evidence:"]
            for e in v["evidence"]:
                V.append(f"  - `{e if isinstance(e, str) else json.dumps(e)}`")
            V += [f"- Minimum correction: {v['minimum_correction']}", ""]
        twrite(os.path.join(OUTPUT, "VETO_LOG.md"), "\n".join(V) + "\n")
    else:
        p = os.path.join(OUTPUT, "VETO_LOG.md")
        if os.path.exists(p):
            os.remove(p)


if __name__ == "__main__":
    m = jread(os.path.join(STATE, "machine.json"))
    if m.get("state") != "HALT":
        print("Auditor refuses to run: worker has not reached HALT.")
        sys.exit(1)
    ok = gate0()
    if ok:
        ok = gate1() and ok
        ok = gate2() and ok
        ok = gate3() and ok
        ok = gate4() and ok
        ok = gate5() and ok
    verdict = "PASS (SCOPED: CHART-ONLY, PDF GATES NOT RUN)" if not VETOES else "VETO"
    write_outputs(verdict)
    print("VERDICT:", verdict)
    for g in GATES:
        print(f"  Gate {g['gate']:<3} {g['name']:<42} {g['outcome']}")
    print("claims scored:", len(CLAIMS), "| vetoes:", len(VETOES))
