"""Carpathia QMDJ Assignment Solver v4.0.0 - shared layer.

LAW 8: never reads QMDJ.json. Reads only the assignment brief and the
chart_analysis_package.json produced by Prompt 1.
"""
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VAULT = os.path.join(ROOT, "vault")
RAW = os.path.join(VAULT, "raw")
STATE = os.path.join(RAW, "state")
WIKI = os.path.join(VAULT, "wiki")
META = os.path.join(WIKI, "_meta")
OUT = os.path.join(ROOT, "output")
SUB = os.path.join(OUT, "SUBMISSION")
ANN = os.path.join(OUT, "ANNOTATED")
OPR = os.path.join(OUT, "OPERATOR")
LYA = os.path.join(OUT, "LAYER_A")

ASSIGNMENT = os.path.join(RAW, "assignment", "Assignment.md")
PACKAGE = os.path.join(RAW, "package", "chart_analysis_package.json")
FORBIDDEN = os.path.join(META, "forbidden_terms.txt")

RUN_ID = "carpathia-adv-p1-solver-0001"
GENERATED_AT = "1970-01-01T00:00:00Z"
SOLVER_VERSION = "4.0.0"
EXPECTED_PROTOCOL_HASH = "sha256:protocol_v2_2_1_0_chart_analyst_v4"
SOLVER_RUBRIC_HASH = "sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4"

# DENY LIST - law 8 enforcement
DENY_READ = ("QMDJ.json",)


def guard_path(path):
    base = os.path.basename(path)
    if base in DENY_READ:
        raise PermissionError(
            f"DENIED_PATH: law 8 forbids reading {base} in the assignment solver.")
    return path


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def jread(path):
    guard_path(path)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def jwrite(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    return path


def tread(path):
    guard_path(path)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def twrite(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def heartbeat(line):
    p = os.path.join(STATE, "solver_progress.md")
    os.makedirs(STATE, exist_ok=True)
    mode = "a" if os.path.exists(p) else "w"
    with open(p, mode, encoding="utf-8") as fh:
        if mode == "w":
            fh.write("# Heartbeat - Carpathia QMDJ Assignment Solver v4.0.0\n\n")
        fh.write(line.rstrip() + "\n")


def fm(d):
    out = ["---"]
    for k, v in d.items():
        out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out)


# ------------------------------------------------------------- term linter --
DENY_DEFAULTS = [
    "QMDJ", "Qimen", "Dunjia", "奇门", "遁甲", "palace", "宫",
    "heaven stem", "earth stem", "day stem", "hour stem",
    "天盘", "地盘", "人盘", "神盘", "九星", "八门", "八神", "值符", "值使",
    "旬空", "空亡", "马星", "入墓", "击刑", "门迫", "反吟", "伏吟", "天乙",
    "阳遁", "阴遁", "节气", "用神", "stem", "branch", "干", "支",
    "Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui",
    "Yang Wood", "Yin Wood", "Yang Fire", "Yin Fire", "Yang Earth", "Yin Earth",
    "Yang Metal", "Yin Metal", "Yang Water", "Yin Water",
    "the day palace", "the hour palace", "chart-reading slang",
    # extra chart vocabulary that must never reach the client tree
    "Fu Yin", "San Qi", "Liu Yi", "He Tu", "Luo Shu", "trigram", "Kan", "Kun",
    "Zhen", "Xun", "Qian", "Dui", "Gen", "Li", "Zhong", "Tian Ying", "Tian Xin",
    "Tian Rui", "Tian Peng", "Tian Chong", "Tian Fu", "Tian Qin", "Tian Zhu",
    "Tian Ren", "Zhi Fu", "Bai Hu", "Teng She", "Liu He", "Tai Yin", "Tai Chang",
    "Jiu Tian", "Jiu Di", "Xuan Wu", "Zhu Que", "Gou Chen", "yongshen",
    "void palace", "horse star", "duty palace", "duty star", "duty door",
    "Yin Dun", "Chai Bu", "Lun Zang", "solar term", "White Dew", "Luoshu",
    "earthly branch", "heavenly stem", "five element", "wu xing",
]

# words that are legitimate English and must not trigger on substrings
_WORD_BOUNDARY_TERMS = {
    "Yi", "Wu", "Ji", "Ren", "Gui", "Xin", "Li", "Gen", "Dui", "Kan", "Kun",
    "Zhen", "Xun", "Qian", "Zhong", "stem", "branch", "palace", "trigram",
    "Jia", "Bing", "Ding", "Geng", "支", "干",
}


def write_denylist():
    os.makedirs(META, exist_ok=True)
    twrite(FORBIDDEN, "\n".join(DENY_DEFAULTS) + "\n")
    return FORBIDDEN


def lint_terms(path, denylist=None):
    """Return violations of the forbidden-term denylist in a file."""
    terms = denylist or DENY_DEFAULTS
    text = tread(path)
    violations = []
    for ln, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for t in terms:
            tl = t.lower()
            if t in _WORD_BOUNDARY_TERMS:
                if re.search(rf"\b{re.escape(tl)}\b", low):
                    violations.append({"file": os.path.relpath(path, ROOT),
                                       "line": ln, "term": t,
                                       "context": line.strip()[:160]})
            elif tl in low:
                violations.append({"file": os.path.relpath(path, ROOT),
                                   "line": ln, "term": t,
                                   "context": line.strip()[:160]})
    return {"pass": not violations, "violations": violations}


def lint_tree(root, denylist=None):
    allv = []
    for base, _, names in os.walk(root):
        for n in sorted(names):
            if n.endswith((".md", ".txt", ".csv")):
                allv += lint_terms(os.path.join(base, n), denylist)["violations"]
    return {"pass": not allv, "violations": allv}
