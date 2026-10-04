#!/usr/bin/env bash
# Stage 2 — scoring, case alignment, grammar gate, digest, ledger, self-audit, conflict check.
set -euo pipefail
ROOT="/home/user/ecole-assignments"
RUN="$ROOT/SUBMISSION/MARKETING/PROJECT_3/QMDJ_ANALYST_RUN"
T="$RUN/tools/qcap.py"
C="$RUN/CONFIG"
CHART="QMDJ/MARKETING/project_3.json"
CASE="ASSIGNMENTS/MARKETING/project_3.yaml"
SCOPE="0,1,2,3,4,5,6,7,8,9"

call () { # call <index> <batch> <cap_id> <subcmd> [extra...]
  local idx="$1" batch="$2" cap="$3" sub="$4"; shift 4
  python3 "$T" "$sub" --cap-id "$cap" --call-index "$idx" --batch "$batch" \
    --repo-root "$ROOT" --run-dir "$RUN" --chart "$CHART" \
    --roles "$C/chart_roles.json" --reference-file "$C/marker_reference.json" \
    --case-context "$CASE" --claim-set "$RUN/authored/claim_set.json" \
    --workbook-sidecar "$RUN/authored/ledger_sidecar.json" \
    --palace-scope "$SCOPE" --visibility "VISIBLE,ELIGIBLE" "$@"
}

echo "== P5  AMEND-01 operator context amendment"
python3 "$RUN/tools/apply_amendment.py" | tail -1

echo "== P6  CAP-15 score_card + claim lines"
python3 "$T" cap15 --cap-id CAP-15 --call-index 14 --batch P6 \
  --repo-root "$ROOT" --run-dir "$RUN" \
  --claim-set "$RUN/authored/claim_set.json:$RUN/raw/state/score_card.json" | tail -1

echo "== B5  CAP-18 case_map"
call 15 B5 CAP-18 cap18 | tail -1

echo "== RT  red-team line composition"
python3 "$RUN/tools/mk_rt_lines.py" >/dev/null

echo "== B5  CAP-13 grammar gate"
python3 "$T" cap13 --cap-id CAP-13 --call-index 16 --batch B5 \
  --repo-root "$ROOT" --run-dir "$RUN" \
  --grammar-files "renders/claim_lines.txt,renders/cmap_lines.txt,renders/rt_lines.txt" | tail -1

echo "== B5  CAP-12 board digest"
call 17 B5 CAP-12 cap12 | tail -1

echo "== B5  CAP-14 ledger reconcile"
call 18 B5 CAP-14 cap14 | tail -1

echo "== B5  CAP-16 self_audit"
call 19 B5 CAP-16 cap16 | tail -1

echo "== B5  CAP-19 conflict check"
call 20 B5 CAP-19 cap19 | tail -1

echo "== B5  CAP-01 phase-boundary recompute"
call 21 B5 CAP-01 cap01 | tail -1

echo "--- call log ---"
cat "$RUN/raw/state/call_log"
echo "--- anomalies ---"
cat "$RUN/raw/state/anomaly_log.jsonl" 2>/dev/null || echo "(none)"
