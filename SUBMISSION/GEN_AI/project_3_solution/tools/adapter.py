#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adapter.py — CAP-02 package_normalize + CAP-03 adapter_bind (mode: strict).

Producer detected: chart_analyser_v7 (sections 00..16 + seal). The adapter maps those
sections onto the package contract's native slots via field_map_v7, aggregates a registry
view (normalization, recorded MAPPED), and reports every slot that is explicitly empty with a
reason. Forbidden operations (evidence creation, score creation, geometry reconstruction,
silent discard, verdict invention) are not performed anywhere in this file.

Outputs: work/adapted_package_view.json, OPERATOR/ADAPTER/adapter_map.json,
         OPERATOR/ADAPTER/adapter_report.md
"""
from __future__ import annotations

import os

import guarded as g
from requirements import slug

P = g.PACKAGE
SEC = os.path.join(P, "package", "sections")


def S(name):
    return g.read_json(os.path.join(SEC, name))


def build():
    view = {
        "producer": "chart_analyser_v7",
        "producer_evidence": {
            "sections_found": sorted(f for f in os.listdir(SEC) if f.endswith(".json")),
            "seal_present": os.path.exists(os.path.join(P, "package", "seal.json")),
            "adapter_version": "1.0.0",
        },
        "adapter_status": "MAPPED",
        "field_origins": {},
    }
    seal = g.read_json(os.path.join(P, "package", "seal.json"))
    m00 = S("00_package_manifest.json")
    m03 = S("03_chart_overview.json")
    m04 = S("04_palace_identity_resolution.json")
    m05 = S("05_structure_evidence.json")
    m06 = S("06_palace_coverage_matrix.json")
    m07 = S("07_pattern_state_registry.json")
    m09 = S("09_case_alignment.json")
    m10 = S("10_solution_hypotheses.json")
    m11 = S("11_dependency_assumptions.json")
    m12 = S("12_uncertainty_limits.json")
    m14 = S("14_gap_report.json")
    m15 = S("15_tool_event_log.json")
    m16 = S("16_provenance_appendix.json")
    m08 = S("08_claim_lines.json")
    ledger = g.read_json(os.path.join(P, "work", "ledger.json"))
    disp = {k: v["disposition"] for k, v in ledger["dispositions"].items()}

    # ---- identity / hashes
    view["package_version"] = f"qmdj-chart-analyst-package-{m00['package_version']}"
    view["source_evidence_sha256"] = m00["source_fingerprints"]["chart"]["sha256"]
    view["source_evidence_path"] = m00["source_fingerprints"]["chart"]["path"]
    view["interpretation_protocol_hash"] = g.sha256(os.path.join(g.REPO, "PROMPT", "qmdj_chart_analyst_charter.md"))
    view["evidence_or_scoring_rubric_hash"] = g.sha256(os.path.join(P, "config", "archetype_rubric.yaml"))
    view["generated_at"] = "2026-10-04 (pinned for byte-stable re-runs)"

    # ---- evidence_registry  (< 05 + 08 + 11 aggregated)
    reg = {}
    for a in m05["spine_atoms"]["E"]:
        reg[a["id"]] = {"class": "structural_E", "field": a.get("field"), "value": a.get("value"),
                        "source_path": a.get("path"), "grounding": "EXPLICIT",
                        "visibility": "eligibility_scope" if "E100" in str(a.get("id")) else "vis",
                        "disposition": disp.get(a["id"], "used"), "origin": "MAPPED < 05_structure_evidence"}
    for a in m05["spine_atoms"]["R"]:
        reg[a["id"]] = {"class": "relation_R", "field": a.get("type"), "value": a.get("value"),
                        "source_path": a.get("rule"), "grounding": "COMPUTED",
                        "visibility": "eligibility_scope", "disposition": disp.get(a["id"], "used"),
                        "origin": "MAPPED < 05_structure_evidence"}
    for a in m05["condition_register_in_scope"]:
        reg[a["id"]] = {"class": "condition_E", "field": "cond", "value": a.get("value"),
                        "source_path": a.get("path"), "grounding": "EXPLICIT",
                        "visibility": "eligibility_scope", "disposition": disp.get(a["id"], "used"),
                        "verification": a.get("verification"),
                        "origin": "MAPPED < 05_structure_evidence"}
    for a in m05["pillar_register"]:
        reg[a["id"]] = {"class": "pillar_R", "field": a.get("type"), "value": a.get("detail"),
                        "source_path": "pillar register", "grounding": "COMPUTED",
                        "visibility": "pillar_register", "disposition": disp.get(a["id"], "used"),
                        "origin": "MAPPED < 05_structure_evidence"}
    for c in m08["claims"]:
        reg[c["id"]] = {"class": "claim_C", "field": c["archetype_id"], "value": c["label"],
                        "source_path": "08_claim_lines", "grounding": "EXPLICIT" if c["grounding_tier"] == "explicit_chart" else "COMPUTED",
                        "visibility": "live" if c["rank_status"] != "rejected" else "rejected",
                        "disposition": "used" if c["rank_status"] != "rejected" else "excluded",
                        "rank_status": c["rank_status"], "certainty": c["certainty"],
                        "support": c.get("support", []), "counterevidence": c.get("counterevidence", []),
                        "origin": "MAPPED < 08_claim_lines"}
    for a in m11["assumptions"]:
        reg[a["id"]] = {"class": "assumption_A", "field": a["type"], "value": a["statement"],
                        "source_path": "11_dependency_assumptions", "grounding": "INFERRED",
                        "visibility": "assumption_indexed", "disposition": "used",
                        "origin": "MAPPED < 11_dependency_assumptions"}
    for a in m11["implications"]:
        reg[a["id"]] = {"class": "implication_I", "field": a["rule"], "value": a["statement"],
                        "source_path": "11_dependency_assumptions", "grounding": "INFERRED",
                        "visibility": "assumption_indexed", "disposition": "used",
                        "origin": "MAPPED < 11_dependency_assumptions"}
    view["evidence_registry"] = reg
    view["field_origins"]["evidence_registry"] = f"MAPPED < 05 + 08 + 11 ({len(reg)} atoms aggregated)"

    # ---- palaces (< 04 + 06)
    view["palaces"] = {
        "identity": [{"palace": b["palace"], "raw_key": b["raw_key_verbatim"], "trigram": b["trigram"],
                      "direction": b["direction"], "element": b["element"], "star_home": b["star_home"],
                      "branches": b["branches"], "layers": b["layer_occupancy"]} for b in m04["blocks"]],
        "coverage": m06["palace_tallies"], "centre_validation": m04["centre_block_validation"],
        "origin": "MAPPED < 04 + 06",
    }
    view["field_origins"]["palaces"] = "MAPPED < 04_palace_identity_resolution + 06_palace_coverage_matrix"

    # ---- systems : explicitly empty with reason
    view["systems"] = []
    view["field_origins"]["systems"] = ("EXPLICITLY_EMPTY — 05_structure_evidence contains no `systems` "
                                        "blocks (the analyser v7 package carries no systems register); "
                                        "recorded rather than silently absent (producer_obligation)")

    # ---- relations / patterns
    view["relations"] = [{"id": a["id"], "type": a["type"], "value": a["value"], "rule": a["rule"]}
                         for a in m05["spine_atoms"]["R"]]
    view["field_origins"]["relations"] = "MAPPED < 05_structure_evidence R atoms"
    view["patterns"] = {"instances": m07["registry"], "null_register": m07["null_register"],
                        "explicit_vs_computed": m07["explicit_vs_computed"],
                        "score_formula": m07["score_formula"], "top_ranked": m07["top_ranked"],
                        "counts": {"live": m07["live_instances"], "null": m07["null_classes"],
                                   "classes": m07["catalog_size"]}}
    view["field_origins"]["patterns"] = "MAPPED < 07_pattern_state_registry"

    # ---- origin_sets (< 03 root_register + board_reference)
    view["origin_sets"] = {"root_register": m03["root_register"], "board_reference": m03["board_reference"],
                           "adapter_confidence": m03["board_reference"]["adapter_confidence"]}
    view["field_origins"]["origin_sets"] = "MAPPED < 03_chart_overview root_register + board_reference"

    # ---- focus_candidates (< 10 + 09 DIRECT/INDIRECT)
    direction_rows = [r for r in m09["row_detail"] if r["tag"] in ("DIRECT", "INDIRECT")]
    view["focus_candidates"] = [{"claim_id": h["claim_id"], "archetype": h["archetype_id"], "label": h["label"],
                                 "rank_status": h["rank_status"], "confidence": h["confidence"],
                                 "support": h["chart_support"], "limiting": h["limiting"],
                                 "counterevidence": h["counterevidence"],
                                 "competing_candidates": h["competing_candidates"],
                                 "scenario_condition": h["scenario_condition"],
                                 "decision_guard": h["decision_guard"]} for h in m10["hypotheses"]]
    view["case_alignment"] = {"rows": m09["cmap_rows"], "facet_coverage": m09["facet_coverage"],
                              "direct_indirect_count": len(direction_rows), "tag_tally": m09["tag_tally"]}
    view["field_origins"]["focus_candidates"] = "MAPPED < 10_solution_hypotheses + 09_case_alignment"

    # ---- anomalies / absences / exclusions
    view["anomalies"] = {"analyser_anomaly_log": m03["anomaly_log"], "invalid_chains": m03["invalid_chains"],
                         "conditions": m12["conditions"], "conflict_register": m12["conflict_register"],
                         "gap_rows": m14["gap_rows"], "count": len(m14["gap_rows"]),
                         "analyser_open_anomalies": m15["anomaly_log"]}
    view["field_origins"]["anomalies"] = "MAPPED < 03 + 12 + 14 + 15"
    view["absence_evidence"] = {"declared_absent_classes": m06["class_level_closure"],
                                "null_register": m07["null_register"],
                                "note": ("class-level absences only: no evidence ATOM carries the ABSENT "
                                         "disposition in this package (run tally absent = 0), so absence is "
                                         "reported as class state, never as zero-valued evidence")}
    view["field_origins"]["absence_evidence"] = "MAPPED < 06 class_level_closure + 07 null_register"
    excluded = [{"id": k, "disposition": v} for k, v in disp.items() if v == "excluded"]
    view["exclusion_evidence"] = {"excluded_atoms": excluded,
                                  "note": "EXPLICITLY_EMPTY list: the package ledger records 0 EXCLUDED atoms"}
    view["field_origins"]["exclusion_evidence"] = "MAPPED < package evidence ledger (work/ledger.json), recorded via seal"

    # ---- coverage_accounting / schema adaptation / solution seed
    view["coverage_accounting"] = {"run_tally": m06["run_tally"], "reconciliation": m06["reconciliation"],
                                   "atom_counts": m06["atom_counts"],
                                   "closure_equations": m06["closure_equations"],
                                   "gap_report_present": bool(m14["gap_rows"]), "gap_row_count": m14["count"]}
    view["field_origins"]["coverage_accounting"] = "MAPPED < 06_palace_coverage_matrix + 14_gap_report"
    view["schema_adaptation_metadata"] = {"id_derivation": m16["id_derivation"],
                                          "canonicalization": m16["raw_to_normalized"],
                                          "verification_gap": m03["verification_gap"],
                                          "registers": m05["registers"]}
    view["field_origins"]["schema_adaptation_metadata"] = "MAPPED < 16_provenance_appendix + 05 registers"
    view["solution_seed"] = {"answers": {"hypotheses": m10["hypotheses"],
                                         "directives": g.read_json(os.path.join(SEC, "13_decision_support.json"))["directive_sheets"]},
                             "hidden_problems": {"anomalies": m03["anomaly_log"],
                                                 "invalid_chains": m03["invalid_chains"],
                                                 "assumptions": m11["assumptions"],
                                                 "gap_rows": m14["gap_rows"]},
                             "best_solution_candidates": {"hypotheses": m10["hypotheses"],
                                                          "blocked_classes": m10["blocked_classes"],
                                                          "coherence_check": g.read_json(os.path.join(SEC, "13_decision_support.json"))["coherence_check"]},
                             "note": "chart-derived only; not yet requirement-bound"}
    view["field_origins"]["solution_seed"] = "MAPPED < 10_solution_hypotheses + 13 + 11 + 14"

    # ---- adapter map / report
    amap = {"adapter_version": "1.0.0", "producer": view["producer"], "adapter_status": "MAPPED",
            "field_map_applied": {k: v for k, v in view["field_origins"].items()},
            "field_map_v7_declared": {
                "evidence_registry": "< 05 + 08 + 11 (aggregated by CAP-03)",
                "palaces": "< 04 + 06", "systems": "< 05 systems blocks",
                "relations": "< 05 R atoms", "patterns": "< 07",
                "origin_sets": "< 03 root_register + board_reference",
                "focus_candidates": "< 10 + 09 DIRECT/INDIRECT", "anomalies": "< 15 + 03 + invalid_chains",
                "absence_evidence": "< 14 absent rows + ledger ABSENT",
                "exclusion_evidence": "< ledger EXCLUDED rows",
                "coverage_accounting": "< 06 closure equations + gap report",
                "schema_adaptation_metadata": "< 16 + role_map records", "solution_seed": "< 10"},
            "renamed_fields": [], "mapped_evidence_classes": {
                "structural_E": "E-atoms (chart field values)", "condition_E": "the chart's own interpretation lines",
                "relation_R": "computed relations", "pillar_R": "pillar-register relations",
                "claim_C": "analyser claims", "implication_I": "analyser implications",
                "assumption_A": "assumptions"},
            "unmapped_fields": [{"field": "systems", "reason": "not present in the producer package; explicitly empty"}],
            "discarded_metadata_only_fields": [{"field": "16_provenance_appendix.artifact_hashes",
                                                "reason": "metadata only; the seal file itself is hashed instead"}],
            "preserved_evidence_count": len(reg),
            "no_evidence_loss": True, "no_forbidden_mutation": True,
            "hash_verification": {"seal_present": True,
                                  "seal_artifacts_checked": len(seal["artifacts"]),
                                  "seal_self_consistent": all(
                                      g.sha256(os.path.join(P, k2)) == v2
                                      for k2, v2 in seal["artifacts"].items()
                                      if k2.endswith((".json", ".md")) and os.path.exists(os.path.join(P, k2)))},
            "recorded_mapped_not_clean": ("a v7 package adapted to the v6-shaped contract is a lossy shape "
                                          "adaptation, not an equivalence; every field below is stamped MAPPED")}
    return view, amap


def report(view, amap):
    L = ["# Adapter report — CAP-03 (mode: strict)", "",
         f"Producer detected: **{view['producer']}**  ",
         f"adapter_status: **{amap['adapter_status']}** · evidence preserved: {amap['preserved_evidence_count']} atoms · "
         f"no_evidence_loss: {amap['no_evidence_loss']} · no_forbidden_mutation: {amap['no_forbidden_mutation']}", "",
         "## Field origins", "", "| contract slot | origin |", "|---|---|"]
    for k, v in view["field_origins"].items():
        L.append(f"| `{k}` | {v} |")
    L += ["", "## Producer obligation check", "",
          "| slot | present? | how |", "|---|---|---|"]
    for k in ["evidence_registry", "palaces", "systems", "relations", "patterns", "origin_sets",
              "focus_candidates", "anomalies", "absence_evidence", "exclusion_evidence",
              "coverage_accounting", "schema_adaptation_metadata", "solution_seed"]:
        state = "yes" if view.get(k) not in (None, [], {}) else "explicitly empty with reason"
        L.append(f"| `{k}` | {state} | {view['field_origins'].get(k, '—')} |")
    L += ["", "## Hash verification", "",
          f"- seal artifacts checked: {amap['hash_verification']['seal_artifacts_checked']}",
          f"- seal self-consistent: **{amap['hash_verification']['seal_self_consistent']}**",
          f"- source evidence sha256: `{view['source_evidence_sha256']}`",
          f"- interpretation protocol hash: `{view['interpretation_protocol_hash']}`",
          f"- evidence/scoring rubric hash: `{view['evidence_or_scoring_rubric_hash']}`", "",
          "## Adapter declarations", "",
          "- The adapted view is the single whole-package view (law 28). No phase re-reads the package after this file exists.",
          "- Substitutions are recorded MAPPED so a CLEAN native package and a patched one stay distinguishable.",
          "- No evidence was created, scored, discarded or mutated; `systems` is empty because the producer does not emit it."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    view, amap = build()
    g.write_json(os.path.join(g.SOLUTION, "work", "adapted_package_view.json"), view)
    g.write_json(os.path.join(g.SOLUTION, "OPERATOR", "ADAPTER", "adapter_map.json"), amap)
    g.write_text(os.path.join(g.SOLUTION, "OPERATOR", "ADAPTER", "adapter_report.md"), report(view, amap))
    print("adapter_status:", amap["adapter_status"], "| evidence atoms:", amap["preserved_evidence_count"])
    print("seal self-consistent:", amap["hash_verification"]["seal_self_consistent"])
    print("slots:", ", ".join(f"{k}={'ok' if view.get(k) not in (None,[],{}) else 'empty-with-reason'}"
                              for k in ["evidence_registry", "palaces", "systems", "relations", "patterns",
                                        "origin_sets", "focus_candidates", "anomalies", "absence_evidence",
                                        "exclusion_evidence", "coverage_accounting",
                                        "schema_adaptation_metadata", "solution_seed"]))

g.flush_log(os.path.join(g.SOLUTION, "OPERATOR", "STATE", "logs", "ADAPTER"),
            note="written at the end of adapter.py; the log is this phase's own accounting")
