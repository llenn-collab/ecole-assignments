#!/usr/bin/env python3
"""Prepare the authorized inputs and report the charter's execution blockers.

This is a preflight, not a replacement for the charter's CAP/Tier tool harness.
No other repository files are inspected. No API call is made.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
INPUTS = {
    "system_prompt": "PROMPT/qmdj_chart_analyst_charter.md",
    "chart": "QMDJ/ADVERTISING/project_2.json",
    "case_context": "ASSIGNMENTS/ADVERTISING/project_2.yaml",
}


def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    # Each authorized input is read once per independent preflight invocation.
    raw = {role: (ROOT / path).read_bytes() for role, path in INPUTS.items()}
    text = {role: data.decode("utf-8") for role, data in raw.items()}
    chart = json.loads(text["chart"])
    provenance = [
        {"role": role, "path": INPUTS[role], "bytes": len(data),
         "sha256": hashlib.sha256(data).hexdigest()}
        for role, data in raw.items()
    ]
    save("execution_request.json", {
        "status": "blocked",
        "submitted_to_model": False,
        "messages": [
            {"role": "system", "content": text["system_prompt"]},
            {"role": "user", "content": json.dumps({
                "chart_source": INPUTS["chart"], "chart": chart,
                "case_context_source": INPUTS["case_context"],
                "case_context_format": "YAML", "case_context": text["case_context"],
                "output_directory": "SUBMISSION/ADVERTISING/project_2",
                "scope_constraint": "Do not access other repository files without the user's authorization of their roles, purpose, and use.",
            }, ensure_ascii=False)},
        ],
        "source_provenance": provenance,
    })
    blockers = [
        ("G001", "schema_adapter.yaml", "Schema variants and required role bindings are not supplied or authorized.", "B1"),
        ("G002", "frozen_tables", "Authoritative tables are not supplied or authorized. The charter annex is reference-only and does not supply every required lookup.", "B2"),
        ("G003", "semantic_protocol_raw.json", "Protocol focus keys are not supplied or authorized.", "B0"),
        ("G004", "A-coverage", "Seven-topic order, 25-batch allocation, class matrix, and coverage controls are placeholder annex content.", "B0"),
        ("G005", "A-patterns", "Pattern catalog is a placeholder; do not invent the compute_always set.", "B4"),
        ("G006", "A-archetypes", "Frozen rubric and legal competing candidate sets are not supplied. Archetype labels and scoring are prohibited.", "Tier2"),
        ("G007", "A-tools", "CAP-01 through CAP-19 and Tier-0/Tier-2 bindings are declared but no callable harness was supplied. Shell availability does not establish these bindings.", "B0"),
        ("G008", "wiki_articles", "Background corpus is not supplied or authorized; no background citations are generated.", "B5"),
        ("G009", "case_context_ingest", "CAP-17 binding is unavailable. Canonical decomposition, facet counts, and conflict checks remain deferred.", "ingest"),
    ]
    gaps = [{"id": gid, "path": path, "why_unaddressed": reason,
             "owner_phase": phase,
             "resolution": "Obtain the user's role/purpose/use authorization and the required artifact or real tool binding before resuming."}
            for gid, path, reason, phase in blockers]
    palace_rows = [{"source_path": f"$.palaces.{key}", "raw_name": value.get("palace_name"),
                    "status": "blocked", "canonical_identity": None,
                    "reason": "B0 has not passed; schema and role resolution were not run."}
                   for key, value in chart["palaces"].items()]
    contract = {
        "status": "blocked", "total_batches": 25,
        "max_palace_blocks_per_batch": 1, "max_parallel_palaces": 2,
        "palace_blocking_rules": None, "palace_dependency_chains": None,
        "forbidden_scope": ["Unauthorized repository files", "Invented CAP/tool outputs", "Factual prediction", "Unsupported archetype labels"],
        "eligible_scope": list(INPUTS.values()), "visibility_tags": None,
        "digest_gates": None,
        "stop_conditions": ["B0 contract incomplete", "Required tool bindings unavailable", "Required core roles blocked"],
        "retry_bounds": {"max_retries_per_claim": 1, "max_retries_per_batch": 1,
                         "max_retries_per_p6_or_rt": 1, "max_cap_calls_per_run": 60},
        "topic_order": None, "validation_passed": False,
        "limits_note": "One-palace-block limit is declared for B2; no global limit is invented for the missing coverage control.",
    }
    save("B0_COVERAGE_CONTRACT.json", contract)
    summary = (
        "Execution stopped at B0. The authorized chart and YAML brief have been preserved "
        "in execution_request.json with the exact charter as the system message. "
        "No CAP was invoked, no model request was submitted, and no downstream analysis, "
        "scoring, red-team review, or advertising campaign was generated."
    )
    package = {
        "00_package_manifest": {
            "status": "blocked", "coverage_complete": False, "tool_health": "blocked",
            "package_version": "7.1.0", "runtime_mode": "TOOLS_PRESENT", "language": "English",
            "execution_stage": "preflight", "context_ingest_status": "blocked",
            "context_degraded": True, "downstream_execution_started": False,
            "source_provenance": provenance,
        },
        "01_validity_boundary": {"analysis_only": True, "no_factual_prediction": True,
                                 "no_substitute_for_professional_judgment": True},
        "02_case_context_digest": {
            "ingest_form": "PROSE", "context_status": "DEGRADED",
            "status": "blocked", "source": INPUTS["case_context"],
            "declared_count": None, "decomposed_count": None, "missing_count": None,
            "unmapped_keys": [], "unmapped_keys_verified": False, "slots": [],
            "known_facts": [], "unknowns": [], "domain": None, "timeframe": None,
            "decision_needed": None,
            "note": "The YAML has a file/pages/sections wrapper, not canonical context keys. PROSE denotes fallback ingest, not the file format. CAP-17 has not run; counts and semantic fields are uncomputed, not zero.",
        },
        "03_chart_overview": {"metadata": chart["chart_info"],
            "board_reference": None, "root_register": [], "anomaly_log": [],
            "invalid_chains": [], "source_paths": [INPUTS["chart"]],
            "note": "Metadata copied verbatim; no resolved board card exists."},
        "04_palace_identity_resolution": {"blocks": palace_rows,
            "centre_block_validation": {"status": "blocked", "reason": "B1 not started; no centre opposition or lodging inferred."}},
        "05_structure_evidence": {"E": [], "R": [], "id_derivation_mode": None, "status": "blocked"},
        "06_palace_coverage_matrix": [
            {"source_path": row["source_path"], "status": "blocked", "tallies": None,
             "closure_equation": None, "gap_rows": ["G001", "G004", "G007"],
             "note": "No atom registry; empty evidence does not establish zero source evidence."}
            for row in palace_rows],
        "07_pattern_state_registry": [], "08_claim_lines": [],
        "09_case_alignment": {"rows": [], "facet_coverage_summary": [],
            "tag_tally": {"DIRECT": 0, "INDIRECT": 0, "NO_CHART_SUPPORT": 0, "CONTRADICTS_KNOWN": 0},
            "status": "blocked", "note": "Zero emitted CMAP rows, not verified facet coverage."},
        "10_solution_hypotheses": [],
        "11_dependency_assumptions": {"A": [], "I": [], "assumption_index": []},
        "12_uncertainty_limits": {"assumption_ranking": [], "invalid_chains": [],
            "deferred_topics": ["All B1-B5, P6, RT and Tier2 work"],
            "blocked_classes": ["HC", "AX", "ZQ", "CS", "JG", "QT"], "conflict_register": []},
        "13_decision_support": {
            "decision_guard": "Do not use this preflight as a chart verdict or campaign recommendation.",
            "validation_path": "Authorize and supply dependencies, bind tools, validate B0, then run checkpointed execution.",
            "uncertainty": "No chart-backed interpretation has been validated.",
            "bounded_recommendation": "Resume only after the blockers are resolved."},
        "14_gap_report": gaps,
        "15_tool_event_log": {"cap_calls": [], "cap_call_count": 0,
            "anomaly_log": [], "SCORE_SOURCE": [],
            "preflight_events": [{"event": "AUTHORIZED_INPUT_SNAPSHOT", "status": "ok"},
                                 {"event": "B0_GATE", "status": "blocked"}],
            "note": "Missing bindings were not invoked; this is not a fabricated TOOL_FAILURE response."},
        "16_provenance_appendix": {"raw_to_normalized_map": [],
            "case_context_provenance": [], "reissue_log": [], "compression_log": [],
            "source_provenance": provenance,
            "note": "Raw sources are embedded in execution_request.json. No normalization or decomposition was executed."},
        "bounded_renders": [], "full_report": summary,
    }
    save("analysis_package.json", package)
    print(summary)


if __name__ == "__main__":
    main()
