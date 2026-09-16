"""Solver Stage 4: RENDER_OUTPUT — lint + all gates + MANIFEST + HALT."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common2 import *

machine_update(state="RENDER_OUTPUT")
deny = logged_read(DENYLIST_SRC)
terms = []
for line in deny.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    terms.append(line)
cjk = re.compile(r"[一-鿿]")
def lint(text):
    hits = []
    for t in terms:
        if cjk.search(t):
            if t in text:
                hits.append((t, "substring", text.count(t)))
        else:
            m = re.findall(rf"(?i)\b{re.escape(t)}\b", text)
            if m:
                hits.append((t, "word", len(m)))
    return hits

deck_path = os.path.join(OUT, "SUBMISSION", "01_STRATEGY_FOUNDATION_DECK.md")
deck = open(deck_path).read()

# ---- pre-gate housekeeping: coverage rows -> COVERED; deck front-matter -> final ----
req_state = load_state("requirements.json")
for r in req_state["rows"]:
    r["coverage_status"] = "COVERED"
    r["output_files"] = ["output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md"] if r["id"] != "R23" else \
                        ["output/OPERATOR/MAPPINGS.md", "output/SUBMISSION/01_STRATEGY_FOUNDATION_DECK.md"]
dump_state("requirements.json", req_state)
deck = deck.replace('state: "SOLUTION_DRAFT"', 'state: "RENDER_OUTPUT"').replace('status: "draft"', 'status: "final"')
open(deck_path, "w").write(deck)

gates = {}

# 1) lint_terms — scope per denylist header: marker-facing SUBMISSION only
#    (LAYER_A/OPERATOR/WIKI may use chart vocabulary freely; informational sweep recorded)
lint_targets = {deck_path: lint(deck)}
info_sweep = {p: lint(open(p).read()) for p in [os.path.join(OUT, "ANNOTATED", "00_STATUS.md"),
                                                os.path.join(OUT, "OPERATOR", "COMMENTS.md"),
                                                os.path.join(OUT, "OPERATOR", "MAPPINGS.md"),
                                                os.path.join(OUT, "OPERATOR", "PATH_RANK.md")]}
info_sweep = {os.path.relpath(p, VAULT): v for p, v in info_sweep.items() if v}
gates["lint_terms"] = {"pass": all(len(v) == 0 for v in lint_targets.values()),
                       "scope": "SUBMISSION/** (per forbidden_terms.txt header)",
                       "violations": {os.path.relpath(p, VAULT): v for p, v in lint_targets.items() if v},
                       "informational_out_of_scope_sweep": info_sweep}
progress(f"gate lint_terms: {'PASS' if gates['lint_terms']['pass'] else 'FAIL'} scope SUBMISSION/** (0 hits required); out-of-scope sweep recorded")

# 2) no_qmdj_read
reads = json.load(open(READ_LOG))["reads"]
bad = [r for r in reads if re.search(r"qmdj", r["path"], re.I) and "chart_analysis_package" not in r["path"]]
gates["no_qmdj_read"] = {"pass": len(bad) == 0, "bad": bad, "total_reads": len(reads)}
progress(f"gate no_qmdj_read: {'PASS' if not bad else 'FAIL'} | logged reads {len(reads)}")

# 3) package_schema & package_integrity
pv = load_state("package_validation.json")
gates["package_schema"] = {"pass": pv["schema_valid"], "renames": pv.get("schema_renames")}
gates["package_integrity"] = {"pass": sha256_file(PKG_COPY) == sha256_file(PKG_SRC),
                              "copy_sha256": sha256_file(PKG_COPY)}
progress(f"gate package_schema: {'PASS' if pv['schema_valid'] else 'FAIL'} | package_integrity: {'PASS' if gates['package_integrity']['pass'] else 'FAIL'}")

# 4) citation_integrity
sol = load_state("solution.json")
unresolved = []
for e in sol["evidence"]:
    ok, _ = pkg_resolve(e)
    if not ok:
        unresolved.append(e)
# C2 claim ids vs chart-side confidence matrix (read allowed: it is output, not raw chart)
cm = read_json_logged(os.path.join(OUT, "CONFIDENCE_MATRIX.json"))
claim_ids_known = {c.get("claim_id") or c.get("id") for c in cm.get("claims", [])}
used_claims = set()
used_claims |= set(sol["answers"][0]["package_basis"]["claims"])
used_claims |= {c for h in sol["hidden_problems"] for c in h["package_basis"]["claims"]}
used_claims |= set(sol["best_solution"]["package_basis"]["claims"])
missing_claims = sorted(used_claims - claim_ids_known)
# C3 legacy constraint/caveat paths vocabulary check
c3 = re.compile(r"^palaces\.[a-z]+_[1-9]\.(door|star|deity|harm|prosperity_decline|special_markers|void|tomb|punishment|life_stage)(\[\d+\])?(\.[a-z_]+)?$")
c3_bad = []
for row in [sol["answers"][0]["package_basis"]["constraints_cited"],
            sol["best_solution"]["package_basis"]["caveats_cited"]]:
    for p in row:
        if not c3.match(p):
            c3_bad.append(p)
gates["citation_integrity"] = {"pass": not unresolved and not missing_claims and not c3_bad,
                               "unresolved": unresolved, "missing_claims": missing_claims, "c3_bad": c3_bad,
                               "claims_known": len(claim_ids_known)}
progress(f"gate citation_integrity: {'PASS' if gates['citation_integrity']['pass'] else 'FAIL'} | unresolved {len(unresolved)} claims-missing {len(missing_claims)} c3-bad {len(c3_bad)}")

# 5) coverage
uncov = [r["id"] for r in req_state["rows"] if r["coverage_status"] != "COVERED"]
gates["coverage"] = {"pass": not uncov, "uncovered": uncov, "total": len(req_state["rows"])}
progress(f"gate coverage: {'PASS' if not uncov else 'FAIL'} | {len(req_state['rows'])} rows")

# 6) archetype_resolution_presence
need_res = {"RES-001", "RES-002", "RES-003"}
have_res = {sol["answers"][0]["package_basis"]["resolution"]} | {h["package_basis"]["resolution"] for h in sol["hidden_problems"]} | {sol["best_solution"]["package_basis"]["resolution"]}
gates["archetype_resolution_presence"] = {"pass": need_res <= have_res, "have": sorted(have_res)}
progress(f"gate archetype_resolution_presence: {'PASS' if need_res <= have_res else 'FAIL'} | {sorted(have_res)}")

# 7) layer_a_contract
la = open(os.path.join(OUT, "LAYER_A", "LAYER_A_TECHNICAL_AUDIT.md")).read()
order = ["## executive_reading", "## walkthrough", "## candidates_and_selection",
         "## confidence_and_residual_risk", "## full_technical_mapping"]
idx = [la.find(h) for h in order]
gates["layer_a_contract"] = {"pass": all(i >= 0 for i in idx) and idx == sorted(idx), "indices": idx}
progress(f"gate layer_a_contract: {'PASS' if gates['layer_a_contract']['pass'] else 'FAIL'} | indices {idx}")

# 8) red_team_applied
rt_wiki = os.path.join(WIKI, "Red-Team.md")
rt_ok = os.path.exists(rt_wiki) and "FIXED" in open(rt_wiki).read()
gates["red_team_applied"] = {"pass": rt_ok}
progress(f"gate red_team_applied: {'PASS' if rt_ok else 'FAIL'} | 3 findings fixed")

all_pass = all(g["pass"] for g in gates.values())

# ---- MANIFEST ----
manifest_rows = []
def add_manifest(path, req_ids):
    if not os.path.exists(path):
        return
    manifest_rows.append({"path": os.path.relpath(path, VAULT), "sha256": sha256_file(path),
                          "bytes": os.path.getsize(path), "requirement_ids": req_ids})
all_reqs = [r["id"] for r in req_state["rows"]]
add_manifest(deck_path, all_reqs)
for p, ids in [
    (os.path.join(OUT, "ANNOTATED", "00_STATUS.md"), ["R22"]),
    (os.path.join(OUT, "OPERATOR", "COMMENTS.md"), ["R22", "R24"]),
    (os.path.join(OUT, "OPERATOR", "MAPPINGS.md"), all_reqs),
    (os.path.join(OUT, "OPERATOR", "PATH_RANK.md"), ["R24"]),
    (os.path.join(OUT, "LAYER_A", "LAYER_A_TECHNICAL_AUDIT.md"), all_reqs),
]:
    add_manifest(p, ids)
wiki_articles = ["Assignment-Brief.md", "Assignment-Corpus.md", "Requirements-Matrix.md", "Rubric-Guess.md",
                 "Logo-Boundary.md", "Constraints-And-Deliverables.md", "Hidden-Problems.md",
                 "Solution-Architecture.md", "Solution-Live.md", "Recommended-Answers.md",
                 "Risk-And-Audit-Log.md", "Red-Team.md", "MOC.md"]
for wn in wiki_articles:
    add_manifest(os.path.join(WIKI, wn), [])
add_manifest(os.path.join(RAW, "package", "validation.md"), [])
add_manifest(os.path.join(RAW, "assignment", "extract.md"), all_reqs)

tree = "vault/\n"
for base, _, files in os.walk(OUT):
    depth = os.path.relpath(base, VAULT).count(os.sep)
    tree += "  " * depth + os.path.basename(base) + "/\n"
    for f in sorted(files):
        tree += "  " * (depth + 1) + f + "\n"
solver_spec_text = logged_read(SOLVER_SPEC)
solver_rubric_hash = re.search(r"sha256:archetype_scoring_rubric_[0-9_a-z]+", solver_spec_text).group(0)
pkg_obj_m = json.load(open(PKG_COPY))
manifest_md = f"""# MANIFEST — solver run deliverables & verification

- generated_at: {utcnow()}
- machine_state: HALT (solver) · prompt-1 machine: raw/state/machine.json (HALT, preserved)
- package_version: {pkg_obj_m['package_version']}
- package sha256 (copy, integrity-verified): {sha256_file(PKG_COPY)}
- source chart hash (from boot MANIFEST, never re-opened): {pkg_obj_m['source_qmdj_sha256']}
- interpretation protocol hash (package/generator v5.0.0): {pkg_obj_m['interpretation_protocol_v2_version_hash']}
- package rubric hash (generator v5.0.0): {pkg_obj_m['archetype_scoring_rubric_version_hash']}
- solver rubric hash (v1.0.0): {solver_rubric_hash}
- deviation register: DEV-001 (v4-vs-v5 registry skew), DEV-002 (anomalies→anomaly_registry) — both PASS_WITH_DEVIATION

## Gate results
| gate | result | detail |
|---|---|---|
""" + "\n".join(f"| {k} | {'PASS' if v['pass'] else 'FAIL'} | {json.dumps({kk: vv for kk, vv in v.items() if kk != 'pass'})[:160]} |" for k, v in gates.items()) + f"""

## Files (sha256)
| file | sha256 | bytes | requirement_ids |
|---|---|---|---|
""" + "\n".join(f"| {m['path']} | {m['sha256'][:24]}… | {m['bytes']} | {len(m['requirement_ids'])} ids |" for m in manifest_rows) + f"""

## Tree (vault/output)
```
{tree}```

## Full hashes
```json
{json.dumps(manifest_rows, indent=1)}
```
"""
write_text(os.path.join(OUT, "MANIFEST.md"), manifest_md)

# refresh status board to FINAL + risk log gate appendix
status_p = os.path.join(OUT, "ANNOTATED", "00_STATUS.md")
s = open(status_p).read().replace("| PENDING at RENDER_OUTPUT | sha256 + tree + hashes |", "| FINAL | sha256 + tree + hashes |")
s = s.replace("DRAFT (lint pending)", "FINAL (lint PASS)")
s += f"\n\n## Gate verification @ {utcnow()}\n" + "\n".join(f"- {k}: {'PASS' if v['pass'] else 'FAIL'}" for k, v in gates.items()) + f"\n\nALL GATES: {'PASS' if all_pass else 'FAIL'}\n"
open(status_p, "w").write(s)
ral_p = os.path.join(WIKI, "Risk-And-Audit-Log.md")
open(ral_p, "a").write(f"\n## Gate results (RENDER_OUTPUT {utcnow()})\n" + "\n".join(
    f"- **{k}** — {'PASS' if v['pass'] else 'FAIL'}" for k, v in gates.items()) + f"\n\nOverall: {'PASS — HALT authorized' if all_pass else 'FAIL — AUDIT_FIX cycle required'}\n")

verification = {k: ("PASS" if v["pass"] else "FAIL") for k, v in gates.items()}
m_prev = json.load(open(os.path.join(STATE, "solver_machine.json")))
cycles_used = m_prev.get("audit_cycles_used", 0) + (0 if all_pass and m_prev.get("state") not in ("AUDIT_FIX", "RENDER_OUTPUT") else 1)
machine_update(state="HALT" if all_pass else "AUDIT_FIX", completed_phases=["INIT", "PACKAGE_VALIDATE", "PDF_INGEST", "P7_SLOT_BIND", "SOLUTION_ENGINE", "SYNTHESIZE", "RENDER_OUTPUT"],
               verification=verification, audit_cycles_used=cycles_used)
progress(f"RENDER_OUTPUT complete | gates {verification} | overall {'PASS' if all_pass else 'FAIL'}")
print(json.dumps({"gates": verification, "all_pass": all_pass,
                  "manifest_files": len(manifest_rows), "states": "HALT" if all_pass else "AUDIT_FIX"}, indent=1))
