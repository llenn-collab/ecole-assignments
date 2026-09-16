"""Carpathia Assignment Solver v4.0.0 — shared utilities.
NEVER reads QMDJ chart files. Every read is logged (no_qmdj_read_gate)."""
import json, hashlib, os, re, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VAULT = os.path.join(REPO, "vault")
RAW = os.path.join(VAULT, "raw")
STATE = os.path.join(RAW, "state")
WIKI = os.path.join(VAULT, "wiki")
OUT = os.path.join(VAULT, "output")
ASSIGN = os.path.join(REPO, "ASSIGNMENTS", "MARKETING", "project_1.md")
PKG_SRC = os.path.join(STATE, "chart_analysis_package.json")   # Prompt-1 deliverable (immutable)
PKG_COPY = os.path.join(RAW, "package", "chart_analysis_package.json")
GEN_SPEC = os.path.join(REPO, "PROMPT", "chart_analyser.yaml")
SOLVER_SPEC = os.path.join(REPO, "PROMPT", "assignment_solver.yaml")
DENYLIST_SRC = os.path.join(REPO, "PROMPT", "forbidden_terms.txt")

READ_LOG = os.path.join(STATE, "solver_reads.json")
def logged_read(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    log = json.load(open(READ_LOG)) if os.path.exists(READ_LOG) else {"reads": []}
    rel = os.path.relpath(path, REPO)
    assert not re.search(r"QMDJ", rel), f"DENIED_PATH: QMDJ read attempted: {rel}"
    log["reads"].append({"path": rel, "at": utcnow()})
    json.dump(log, open(READ_LOG, "w"), indent=2)
    return content

def read_json_logged(path):
    return json.loads(logged_read(path))

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def sha256_file(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()

def dump_state(name, obj):
    p = os.path.join(STATE, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")

def load_state(name):
    return json.load(open(os.path.join(STATE, name)))

def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def progress(line):
    shared = os.path.join(STATE, "progress.md")
    with open(shared, "a", encoding="utf-8") as f:
        f.write(f"- `{utcnow()}` [SOLVER] {line}\n")
    mine = os.path.join(STATE, "solver_progress.md")
    with open(mine, "a", encoding="utf-8") as f:
        f.write(f"- `{utcnow()}` {line}\n")

def machine_update(**kw):
    p = os.path.join(STATE, "solver_machine.json")
    m = json.load(open(p)) if os.path.exists(p) else {}
    m.update(kw); m["updated_at"] = utcnow()
    json.dump(m, open(p, "w"), indent=2, sort_keys=True)

# package path resolver: cite claims against the PACKAGE COPY only
def pkg():
    return read_json_logged(PKG_COPY)

def pkg_resolve(path):
    """Resolve dot/bracket path inside package copy. Returns (ok, value)."""
    cur = pkg()
    for m in re.finditer(r'([A-Za-z0-9_\-]+)|\["([^"]+)"\]|\[(\d+)\]', path):
        name, braw, bidx = m.group(1), m.group(2), m.group(3)
        key = braw if braw is not None else (int(bidx) if bidx is not None else name)
        if key is None or key == "": continue
        try:
            if isinstance(key, int):
                cur = cur[key] if isinstance(cur, list) else cur[str(key)]
            elif isinstance(cur, dict):
                cur = cur[key]
            elif isinstance(cur, list):
                hit = [x for x in cur if isinstance(x, dict) and any(key in str(v) for v in x.values())]
                if not hit: return False, None
                cur = hit[0]
            else:
                return False, None
        except (KeyError, IndexError, TypeError):
            return False, None
    return True, cur

PROTO_HASH_PKG = "sha256:protocol_v2_2_2_0_chart_analyst_v5"
RUBRIC_HASH_PKG = "sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5"
RUBRIC_HASH_SOLVER = "sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4"
