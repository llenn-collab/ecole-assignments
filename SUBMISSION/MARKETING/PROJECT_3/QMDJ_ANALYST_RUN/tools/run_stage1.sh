#!/usr/bin/env bash
# Stage 1 — ingest through evidence registry (B0/B1/B2/B3-prep capabilities).
# Every CAP runs as a real process; raw/state/call_log is the durable memory of the run.
set -euo pipefail
ROOT="/home/user/ecole-assignments"
RUN="$ROOT/SUBMISSION/MARKETING/PROJECT_3/QMDJ_ANALYST_RUN"
T="$RUN/tools/qcap.py"
C="$RUN/CONFIG"
CHART="QMDJ/MARKETING/project_3.json"
CASE="ASSIGNMENTS/MARKETING/project_3.yaml"

rm -rf "$RUN/raw/state"
mkdir -p "$RUN/raw/state"

call () { # call <index> <batch> <cap_id> <subcmd>
  local idx="$1" batch="$2" cap="$3" sub="$4"
  python3 "$T" "$sub" --cap-id "$cap" --call-index "$idx" --batch "$batch" \
    --repo-root "$ROOT" --run-dir "$RUN" --chart "$CHART" \
    --roles "$C/chart_roles.json" --reference-file "$C/marker_reference.json" \
    --case-context "$CASE" --palace-scope "0,1,2,3,4,5,6,7,8,9" \
    --visibility "VISIBLE,ELIGIBLE"
}

echo "== B0  CAP-01 fingerprint";     call 1  B0 CAP-01 cap01 | tail -1
echo "== B1  CAP-02 normalize";       call 2  B1 CAP-02 cap02 | tail -1
echo "== B1  CAP-03 schema_bind";     call 3  B1 CAP-03 cap03 | tail -1
echo "== B1  CAP-04 role_resolve";    call 4  B1 CAP-04 cap04 | tail -1
echo "== B1  CAP-05 ganzhi_parser";   call 5  B1 CAP-05 cap05 | tail -1
echo "== B1  CAP-06 stem_norm";       call 6  B1 CAP-06 cap06 | tail -1
echo "== B1  CAP-07 composite_field"; call 7  B1 CAP-07 cap07 | tail -1
echo "== B2  CAP-08 luoshu_geometry"; call 8  B2 CAP-08 cap08 | tail -1
echo "== B3  CAP-10 pattern_detect";  call 9  B3 CAP-10 cap10 | tail -1
echo "== B3  CAP-11 atomize";         call 10 B3 CAP-11 cap11 | tail -1
echo "== P5  CAP-17 case_decompose";  call 11 P5 CAP-17 cap17 | tail -1
echo "== B3  CAP-09 value_trace"
call 12 B3 CAP-09 cap09 | tail -1
echo "== B1d CAP-01 phase-boundary recompute"
call 13 B1 CAP-01 cap01 | tail -1

echo "--- call log ---"
cat "$RUN/raw/state/call_log"
echo "--- anomalies ---"
cat "$RUN/raw/state/anomaly_log.jsonl" 2>/dev/null || echo "(none)"
