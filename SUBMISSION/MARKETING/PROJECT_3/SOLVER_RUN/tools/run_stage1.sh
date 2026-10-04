#!/usr/bin/env bash
# CARPATHIA stage 1 — INIT through SOLUTION_ENGINE, plus the pre-render guard caps.
set -euo pipefail
RUN="/home/user/ecole-assignments/SUBMISSION/MARKETING/PROJECT_3/SOLVER_RUN"
T="$RUN/tools/scap.py"

rm -rf "$RUN/state"
mkdir -p "$RUN/state"

call () { local i="$1" cap="$2" sub="$3"; python3 "$T" "$sub" --call-index "$i" --cap-id "$cap" | tail -1; }

echo "== INIT            CAP-01 fingerprint";           call 1  CAP-01 cap01
echo "== PACKAGE_VALIDATE CAP-02 normalize";           call 2  CAP-02 cap02
echo "== PACKAGE_VALIDATE CAP-03 adapter_bind";        call 3  CAP-03 cap03
echo "== PDF_INGEST      CAP-15 pdf_decompose";        call 4  CAP-15 cap15
echo "== PDF_INGEST      CAP-04 requirement_resolve";  call 5  CAP-04 cap04
echo "== P7_SLOT_BIND    CAP-06 binding_atomize";      call 6  CAP-06 cap06
echo "== P7_SLOT_BIND    CAP-16 requirement_map";      call 7  CAP-16 cap16
echo "== P7_SLOT_BIND    CAP-07 card_build";           call 8  CAP-07 cap07
echo "== SOLUTION_ENGINE CAP-09 ledger_reconcile";     call 9  CAP-09 cap09
echo "== SOLUTION_ENGINE CAP-10 score_card";           call 10 CAP-10 cap10
echo "== SOLUTION_ENGINE CAP-18 hidden_translate";     call 11 CAP-18 cap18
echo "== SYNTHESIZE      CAP-12 dependency_check";     call 12 CAP-12 cap12
echo "== SYNTHESIZE      CAP-17 conflict_check";       call 13 CAP-17 cap17
echo "--- call log ---"; cat "$RUN/state/call_log"
echo "--- anomalies ---"; cat "$RUN/state/anomaly_log.jsonl" 2>/dev/null || echo "(none)"
