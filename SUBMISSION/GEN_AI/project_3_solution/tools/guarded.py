#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guarded.py — path guard + fingerprint helpers (CAP-01) for the Assignment Solver run.

Charter law 8 / path_policy: the solver NEVER reads the raw chart source and NEVER writes
into the package or the brief. Both policies are enforced here by an executing guard (not a
claim in prose), and every attempted read/write is logged so the self-audit can prove it.
"""
from __future__ import annotations

import hashlib
import json
import os

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
SOLUTION = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PACKAGE = os.path.join(REPO, "SUBMISSION", "GEN_AI", "project_3")
BRIEF = os.path.join(REPO, "ASSIGNMENTS", "GEN_AI", "project_3.yaml")
RESEARCH = os.path.join(REPO, "ASSIGNMENTS", "GEN_AI", "project_3_research.yaml")

READ_LOG: list[dict] = []
WRITE_LOG: list[dict] = []

DENY_READ = [os.path.join(REPO, "QMDJ")]          # raw chart sources, in full
DENY_WRITE = [PACKAGE, BRIEF, RESEARCH]           # immutable inputs


def _under(path, roots):
    ap = os.path.abspath(path)
    return any(ap == os.path.abspath(r) or ap.startswith(os.path.abspath(r) + os.sep) for r in roots)


def guard_read(path):
    ap = os.path.abspath(path)
    if _under(ap, DENY_READ):
        READ_LOG.append({"path": ap, "allowed": False, "code": "DENIED_PATH"})
        raise PermissionError(f"DENIED_PATH (law 8, raw chart source): {ap}")
    READ_LOG.append({"path": ap, "allowed": True, "code": "OK"})
    return ap


def guard_write(path):
    ap = os.path.abspath(path)
    if _under(ap, DENY_WRITE):
        WRITE_LOG.append({"path": ap, "allowed": False, "code": "DENIED_PATH"})
        raise PermissionError(f"DENIED_PATH (immutable input): {ap}")
    WRITE_LOG.append({"path": ap, "allowed": True, "code": "OK"})
    return ap


def read_text(path):
    with open(guard_read(path), encoding="utf-8") as f:
        return f.read()


def read_json(path):
    return json.loads(read_text(path))


def write_text(path, text):
    os.makedirs(os.path.dirname(guard_write(path)), exist_ok=True)
    with open(guard_write(path), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def write_json(path, obj):
    return write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha256(path):
    return hashlib.sha256(open(guard_read(path), "rb").read()).hexdigest()


def fingerprint(path, tag):
    """CAP-01. sha256 available in TOOLS_PRESENT."""
    raw = open(guard_read(path), "rb").read()
    doc = json.loads(raw.decode("utf-8")) if path.endswith(".json") else None
    keys = sorted(doc.keys()) if isinstance(doc, dict) else None
    return {"tag": tag, "path": rel(path), "filename": os.path.basename(path), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "top_level_key_count": len(keys) if keys else None, "top_level_keys": keys,
            "mode": "sha256"}


def rel(path):
    ap = os.path.abspath(path)
    return os.path.relpath(ap, REPO).replace(os.sep, "/")


def log_state():
    return {"read_attempts": len(READ_LOG), "reads_denied": len([r for r in READ_LOG if not r["allowed"]]),
            "write_attempts": len(WRITE_LOG), "writes_denied": len([w for w in WRITE_LOG if not w["allowed"]]),
            "read_log": READ_LOG[-200:], "write_log": WRITE_LOG[-200:]}


def flush_log(out_dir, note="snapshot"):
    """Persist this process's path-guard log. Called once per tool, so the operator keeps the
    accounting for each phase rather than a single merged file."""
    state = log_state()
    state["note"] = note
    state["denied_read_of_raw_chart_source"] = len([r for r in READ_LOG
                                                    if not r["allowed"] and "QMDJ" in r["path"]])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "read_log.json"), "w", encoding="utf-8") as f:
        json.dump({"phase_read_attempts": state["read_attempts"], "reads_denied": state["reads_denied"],
                   "read_log": state["read_log"], "note": note}, f, indent=1, ensure_ascii=False)
    with open(os.path.join(out_dir, "write_log.json"), "w", encoding="utf-8") as f:
        json.dump({"phase_write_attempts": state["write_attempts"], "writes_denied": state["writes_denied"],
                   "write_log": state["write_log"], "note": note}, f, indent=1, ensure_ascii=False)
    return state
