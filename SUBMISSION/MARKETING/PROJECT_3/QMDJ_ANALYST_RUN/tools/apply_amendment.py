#!/usr/bin/env python3
"""apply_amendment.py — applies AMEND-01 (operator context re-classification) to run QMDJ-P3-001.

Mechanical only:
  1. copies CONFIG/context_amendment.json into raw/state/ as a run artefact
  2. raises the QUESTION_OVERLOAD anomaly that CAP-17 step 4 requires and that v1 failed to log
It does not touch the chart, the evidence registry, the claims or any score.
"""
import io, json, os, shutil

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(RUN, "CONFIG/context_amendment.json")
STATE = os.path.join(RUN, "raw/state")


def main():
    amd = json.load(io.open(CFG, encoding="utf-8"))
    with io.open(os.path.join(STATE, "context_amendment.json"), "w", encoding="utf-8") as f:
        json.dump(amd, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    rec = json.dumps({
        "code": "QUESTION_OVERLOAD",
        "detail": "11 facets detected against the charter's 7-facet cap; the 7 most "
                  "decision-relevant (Q1-Q7) are analysed under criterion DECISION_RELEVANCE and "
                  "Q8-Q11 are listed as deferred. Raised on amendment AMEND-01: the v1 run reported "
                  "the cap inside the digest but did not log the anomaly code CAP-17 step 4 requires.",
        "path": "02_case_context_digest",
        "phase": "P5",
        "call_index": 11,
        "raised_by": "AMEND-01"
    }, ensure_ascii=False, sort_keys=True)
    with io.open(os.path.join(STATE, "anomaly_log.jsonl"), "a", encoding="utf-8") as f:
        f.write(rec + "\n")
    print(json.dumps({"applied": "AMEND-01",
                      "context_status": "CONTEXT_FREE_PROSE_ACCEPTED",
                      "slots_filled": 6,
                      "facet_rule": "DECISION_RELEVANCE",
                      "anomaly_raised": "QUESTION_OVERLOAD",
                      "chart_layer_touched": False}, indent=2))


if __name__ == "__main__":
    main()
