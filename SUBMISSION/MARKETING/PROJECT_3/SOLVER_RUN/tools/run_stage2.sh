#!/usr/bin/env bash
# CARPATHIA stage 2 — render guards and manifest. Run after all four trees are written.
set -euo pipefail
RUN="/home/user/ecole-assignments/SUBMISSION/MARKETING/PROJECT_3/SOLVER_RUN"
T="$RUN/tools/scap.py"

# idempotent: drop this stage's own prior lines so re-running does not double-log
if [ -f "$RUN/state/call_log" ]; then
  grep -v -E '^CAP\|CAP-(11|14|13)\|' "$RUN/state/call_log" > "$RUN/state/call_log.tmp" || true
  mv "$RUN/state/call_log.tmp" "$RUN/state/call_log"
  rm -f "$RUN/state/anomaly_log.jsonl"
fi

call () { local i="$1" cap="$2" sub="$3"; python3 "$T" "$sub" --call-index "$i" --cap-id "$cap" | tail -1; }

echo "== RENDER_GUARD    CAP-11 lint_scan";           call 14 CAP-11 cap11
echo "== RENDER_GUARD    CAP-14 self_audit";          call 15 CAP-14 cap14
echo "== RENDER_MANIFEST CAP-13 manifest_build";      call 16 CAP-13 cap13
echo "--- call log (tail) ---"; tail -6 "$RUN/state/call_log"
echo "--- anomalies ---"; cat "$RUN/state/anomaly_log.jsonl" 2>/dev/null || echo "(none)"
