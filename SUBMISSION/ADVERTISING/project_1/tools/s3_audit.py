#!/usr/bin/env python3
"""Solver-phase audit gates.

Implements PROMPT/SKILLS/Audit/skill.md for the assignment-solver phase.
Gates are pass/fail. A gate is NEVER relaxed to make a run pass; a failing
gate is fixed at source.

Gates
-----
0a  no_qmdj_read_gate      zero reads of QMDJ.json anywhere in the run
0b  assignment_input_gate  brief present, hash-stable, non-empty
1   package_schema_gate    package validation was run and passed 9/9
2   lint_terms             SUBMISSION/ tree free of forbidden terminology
3   layer_a_contract       5 required sections, in the required order
4   tree_contract          required trees and minimum files exist
5   claim_citation_gate    every live claim cites an archetype_resolution
6   registry_status_gate   every registered deliverable exists on disk
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import solver_common as sc  # noqa: E402

RUN = sc.RUN_ROOT if hasattr(sc, "RUN_ROOT") else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, "output")
STATE = os.path.join(RUN, "vault", "raw", "state")

RESULTS = []


def gate(gate_id, name, ok, detail=""):
    RESULTS.append({
        "gate": gate_id,
        "name": name,
        "status": "PASS" if ok else "FAIL",
        "detail": detail,
    })
    return ok


# ---------------------------------------------------------------- gate 0a
def g_no_qmdj_read():
    """Law 8. Prove zero reads, and prove the guard actually bites."""
    violations = []
    tools_dir = os.path.join(RUN, "tools")

    # 1. Determine the modules actually reachable from the solver entry
    #    points by transitive import closure. Chart-phase modules
    #    (common.py, p0..p7, render, report, audit) legitimately read the
    #    source chart, but they are not imported or executed in this phase.
    #    Scanning unreachable files would be a false positive; excluding
    #    them by name would be unsound. Reachability is the honest test.
    entry = ["s1_ingest.py", "s2_solution_engine.py", "s3_audit.py"]
    imp = re.compile(r"^\s*(?:from\s+(\w+)\s+import|import\s+(\w+))", re.M)
    reachable, stack = set(), list(entry)
    while stack:
        fn = stack.pop()
        if fn in reachable or not os.path.exists(os.path.join(tools_dir, fn)):
            continue
        reachable.add(fn)
        src = sc.tread(os.path.join(tools_dir, fn))
        for m in imp.finditer(src):
            mod = m.group(1) or m.group(2)
            cand = f"{mod}.py"
            if os.path.exists(os.path.join(tools_dir, cand)):
                stack.append(cand)

    # 2. Within reachable modules, flag actual I/O against a QMDJ path.
    #    Mentions in docstrings, comments, denylists and gate names are
    #    not reads.
    io_call = re.compile(
        r"\b(open|tread|jread|read_text|read_bytes|load|loads)\s*\([^)]*QMDJ",
        re.IGNORECASE,
    )
    for fn in sorted(reachable):
        src = sc.tread(os.path.join(tools_dir, fn))
        for m in io_call.finditer(src):
            line = src[:m.start()].count("\n") + 1
            ctx = src.splitlines()[line - 1].strip()
            if ctx.startswith("#"):
                continue
            violations.append(f"{fn}:{line}: {ctx[:70]}")
    scope = f"{len(reachable)} reachable modules: {sorted(reachable)}"
    # 2. live proof the guard raises
    guard_bites = False
    try:
        sc.guard_path("/any/where/QMDJ.json")
    except PermissionError:
        guard_bites = True
    except Exception:
        pass
    if not guard_bites:
        violations.append("guard_path did not raise on a QMDJ.json path")
    return gate("0a", "no_qmdj_read_gate", not violations,
                "; ".join(violations)
                or f"0 reads; guard verified live; scope={scope}")


# ---------------------------------------------------------------- gate 0b
def g_assignment_input():
    p = os.path.join(RUN, "vault", "raw", "assignment", "Assignment.md")
    if not os.path.exists(p):
        return gate("0b", "assignment_input_gate", False, "brief copy missing")
    h = sc.sha256_file(p)
    body = sc.tread(p).strip()
    ok = len(body) > 500 and h.startswith("96a17883")
    return gate("0b", "assignment_input_gate", ok,
                f"sha256={h[:16]} bytes={len(body)}")


# ----------------------------------------------------------------- gate 1
def g_package_schema():
    p = os.path.join(STATE, "package_validation.json")
    if not os.path.exists(p):
        return gate("1", "package_schema_gate", False, "no validation record")
    v = sc.jread(p)
    checks = v.get("checks", [])
    # records use a boolean `pass` field, not a `status` string
    failed = [c for c in checks if c.get("pass") is not True]
    ok = bool(checks) and not failed and v.get("pass") is True
    return gate("1", "package_schema_gate", ok,
                f"{len(checks) - len(failed)}/{len(checks)} PASS"
                + (f"; failed {[c.get('check') for c in failed]}"
                   if failed else ""))


# ----------------------------------------------------------------- gate 2
def g_lint():
    r = sc.lint_tree(os.path.join(OUT, "SUBMISSION"))
    v = r.get("violations", [])
    return gate("2", "lint_terms", r.get("pass") is True,
                f"{len(v)} violations" + (f": {v[:3]}" if v else ""))


# ----------------------------------------------------------------- gate 3
def g_layer_a():
    p = os.path.join(OUT, "LAYER_A", "LAYER_A_TECHNICAL_AUDIT.md")
    if not os.path.exists(p):
        return gate("3", "layer_a_contract", False, "audit file missing")
    txt = sc.tread(p).lower()
    required = [
        "executive reading",
        "walkthrough",
        "candidates and selection",
        "confidence and residual risk",
        "full technical mapping",
    ]
    pos, missing = [], []
    for s in required:
        i = txt.find(s)
        (missing if i < 0 else pos).append(s if i < 0 else i)
    if missing:
        return gate("3", "layer_a_contract", False, f"missing: {missing}")
    ordered = pos == sorted(pos)
    return gate("3", "layer_a_contract", ordered,
                "5/5 sections, correct order" if ordered else "out of order")


# ----------------------------------------------------------------- gate 4
def g_trees():
    need = {
        "SUBMISSION": None,
        "ANNOTATED": ["00_STATUS.md"],
        "OPERATOR": ["COMMENTS.md", "MAPPINGS.md", "PATH_RANK.md"],
        "LAYER_A": ["LAYER_A_TECHNICAL_AUDIT.md"],
    }
    missing = []
    for tree, files in need.items():
        d = os.path.join(OUT, tree)
        if not os.path.isdir(d):
            missing.append(f"tree {tree}")
            continue
        for f in files or []:
            if not os.path.exists(os.path.join(d, f)):
                missing.append(f"{tree}/{f}")
    if not os.path.exists(os.path.join(OUT, "MANIFEST.md")):
        missing.append("MANIFEST.md")
    return gate("4", "tree_contract", not missing,
                "; ".join(missing) or "all trees and minimum files present")


# ----------------------------------------------------------------- gate 5
def g_claim_citation():
    p = os.path.join(STATE, "solution_live.json")
    live = sc.jread(p)
    claims = []
    claims += live.get("answers", [])
    claims += live.get("hidden_problems", [])
    if live.get("best_solution"):
        claims.append(live["best_solution"])
    uncited = [c.get("claim_id") for c in claims
               if c.get("status") == "live"
               and not c.get("archetype_resolution_id")]
    n = len([c for c in claims if c.get("status") == "live"])
    return gate("5", "claim_citation_gate", not uncited,
                f"{n} live claims, {len(uncited)} uncited"
                + (f": {uncited}" if uncited else ""))


# ----------------------------------------------------------------- gate 6
def g_registry():
    p = os.path.join(STATE, "deliverable_registry.json")
    reg = sc.jread(p)
    items = reg.get("deliverables", reg if isinstance(reg, list) else [])
    if not items:
        return gate("6", "registry_status_gate", False, "registry empty")
    missing, unaddressed = [], []
    for d in items:
        # registry entries carry `output_path`, relative to the run root.
        fn = d.get("output_path") or d.get("filename") or d.get("path")
        if not fn:
            # an entry with no path cannot be verified; that is a failure,
            # not something to skip. Skipping it would pass the gate
            # vacuously, which is exactly what this branch prevents.
            unaddressed.append(d.get("id", "<no id>"))
            continue
        if not os.path.exists(os.path.join(RUN, fn)):
            missing.append(fn)
    bad = missing + unaddressed
    return gate("6", "registry_status_gate", not bad,
                f"{len(items) - len(bad)}/{len(items)} present"
                + (f"; missing {missing}" if missing else "")
                + (f"; unaddressed {unaddressed}" if unaddressed else ""))


def main():
    g_no_qmdj_read()
    g_assignment_input()
    g_package_schema()
    g_lint()
    g_layer_a()
    g_trees()
    g_claim_citation()
    g_registry()

    failed = [r for r in RESULTS if r["status"] == "FAIL"]
    report = {
        "phase": "SOLVER_AUDIT",
        "gates_run": len(RESULTS),
        "gates_passed": len(RESULTS) - len(failed),
        "verdict": "PASS" if not failed else "FAIL",
        "results": RESULTS,
    }
    sc.jwrite(os.path.join(STATE, "solver_audit.json"), report)

    w = max(len(r["name"]) for r in RESULTS)
    print(f"\n{'GATE':<5}{'NAME':<{w + 2}}{'STATUS':<8}DETAIL")
    print("-" * (w + 60))
    for r in RESULTS:
        print(f"{r['gate']:<5}{r['name']:<{w + 2}}{r['status']:<8}{r['detail']}")
    print("-" * (w + 60))
    print(f"VERDICT: {report['verdict']} "
          f"({report['gates_passed']}/{report['gates_run']})\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
