"""Carpathia QMDJ Chart Analyst v4.0.0 - shared tables and helpers.

Deterministic. No network. No assignment awareness.
Only reads vault/raw/QMDJ.json (immutable) and vault/raw/state/*.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VAULT = os.path.join(ROOT, "vault")
RAW = os.path.join(VAULT, "raw")
STATE = os.path.join(RAW, "state")
TRACES = os.path.join(RAW, "traces")
CHARTDIR = os.path.join(RAW, "chart")
WIKI = os.path.join(VAULT, "wiki")
WIKI_PALACES = os.path.join(WIKI, "palaces")
OUTPUT = os.path.join(VAULT, "output")
QMDJ_PATH = os.path.join(RAW, "QMDJ.json")

PACKAGE_VERSION = "4.0.0"
PROTOCOL_HASH = "sha256:protocol_v2_2_1_0_chart_analyst_v4"
RUBRIC_HASH = "sha256:archetype_scoring_rubric_1_0_0_chart_analyst_v4"
GENERATED_AT = "1970-01-01T00:00:00Z"  # determinism: fixed, see determinism_policy

# ---------------------------------------------------------------- tables ----
STEM_ELEMENT = {
    "Jia": "Wood", "Yi": "Wood",
    "Bing": "Fire", "Ding": "Fire",
    "Wu": "Earth", "Ji": "Earth",
    "Geng": "Metal", "Xin": "Metal",
    "Ren": "Water", "Gui": "Water",
}
STEM_POLARITY = {
    "Jia": "Yang", "Yi": "Yin", "Bing": "Yang", "Ding": "Yin", "Wu": "Yang",
    "Ji": "Yin", "Geng": "Yang", "Xin": "Yin", "Ren": "Yang", "Gui": "Yin",
}
STEM_ORDER = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]

# 天干五合 - stem combinations (classical). transform product is school variant.
STEM_COMBINATIONS = [
    ("Jia", "Ji", "Earth"),
    ("Yi", "Geng", "Metal"),
    ("Bing", "Xin", "Water"),
    ("Ding", "Ren", "Wood"),
    ("Wu", "Gui", "Fire"),
]
# 天干相冲 - stem clashes (four classical pairs; Earth stems exempt)
STEM_CLASHES = [("Jia", "Geng"), ("Yi", "Xin"), ("Bing", "Ren"), ("Ding", "Gui")]

SANQI = ["Yi", "Bing", "Ding"]
LIUYI = ["Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]

DOOR_ELEMENT = {
    "Xiu (Rest)": "Water",
    "Sheng (Life)": "Earth",
    "Shang (Harm)": "Wood",
    "Du (Restraint)": "Wood",
    "Jing (Scenery)": "Fire",
    "Si (Death)": "Earth",
    "Jing (Fear)": "Metal",
    "Kai (Open)": "Metal",
}
STAR_ELEMENT = {
    "Tian Peng (Grass)": "Water",
    "Tian Rui (Grain)": "Earth",
    "Tian Chong (Impulse)": "Wood",
    "Tian Fu (Assistant)": "Wood",
    "Tian Qin (Bird)": "Earth",
    "Tian Xin (Heart)": "Metal",
    "Tian Zhu (Pillar)": "Metal",
    "Tian Ren (Ambassador)": "Earth",
    "Tian Ying (Hero)": "Fire",
}
STAR_HOME_LUOSHU = {
    "Tian Peng (Grass)": "1",
    "Tian Rui (Grain)": "2",
    "Tian Chong (Impulse)": "3",
    "Tian Fu (Assistant)": "4",
    "Tian Qin (Bird)": "5",
    "Tian Xin (Heart)": "6",
    "Tian Zhu (Pillar)": "7",
    "Tian Ren (Ambassador)": "8",
    "Tian Ying (Hero)": "9",
}

# frozen geometry (prompt #/qmdj_complete/palace_identity_table)
PALACE_IDENTITY = {
    "1": {"name": "Kan", "dir": "North", "element": "Water", "branches": ["Zi (Rat)"]},
    "2": {"name": "Kun", "dir": "Southwest", "element": "Earth", "branches": ["Wei (Goat)", "Shen (Monkey)"]},
    "3": {"name": "Zhen", "dir": "East", "element": "Wood", "branches": ["Mao (Rabbit)"]},
    "4": {"name": "Xun", "dir": "Southeast", "element": "Wood", "branches": ["Chen (Dragon)", "Si (Snake)"]},
    "5": {"name": "Center", "dir": "Center", "element": "Earth", "branches": []},
    "6": {"name": "Qian", "dir": "Northwest", "element": "Metal", "branches": ["Xu (Dog)", "Hai (Pig)"]},
    "7": {"name": "Dui", "dir": "West", "element": "Metal", "branches": ["You (Rooster)"]},
    "8": {"name": "Gen", "dir": "Northeast", "element": "Earth", "branches": ["Chou (Ox)", "Yin (Tiger)"]},
    "9": {"name": "Li", "dir": "South", "element": "Fire", "branches": ["Wu (Horse)"]},
}
OPPOSITE = {"1": "9", "9": "1", "2": "8", "8": "2", "3": "7", "7": "3", "4": "6", "6": "4", "5": None}

BRANCH_TO_PALACE = {
    "Zi (Rat)": "1", "Wei (Goat)": "2", "Shen (Monkey)": "2", "Mao (Rabbit)": "3",
    "Chen (Dragon)": "4", "Si (Snake)": "4", "Xu (Dog)": "6", "Hai (Pig)": "6",
    "You (Rooster)": "7", "Chou (Ox)": "8", "Yin (Tiger)": "8", "Wu (Horse)": "9",
}
BRANCH_SHORT = {
    "Zi": "Zi (Rat)", "Chou": "Chou (Ox)", "Yin": "Yin (Tiger)", "Mao": "Mao (Rabbit)",
    "Chen": "Chen (Dragon)", "Si": "Si (Snake)", "Wu": "Wu (Horse)", "Wei": "Wei (Goat)",
    "Shen": "Shen (Monkey)", "You": "You (Rooster)", "Xu": "Xu (Dog)", "Hai": "Hai (Pig)",
}
HORSE_BRANCH = {
    "Shen (Monkey)": "Yin (Tiger)", "Zi (Rat)": "Yin (Tiger)", "Chen (Dragon)": "Yin (Tiger)",
    "Yin (Tiger)": "Shen (Monkey)", "Wu (Horse)": "Shen (Monkey)", "Xu (Dog)": "Shen (Monkey)",
    "Si (Snake)": "Hai (Pig)", "You (Rooster)": "Hai (Pig)", "Chou (Ox)": "Hai (Pig)",
    "Hai (Pig)": "Si (Snake)", "Mao (Rabbit)": "Si (Snake)", "Wei (Goat)": "Si (Snake)",
}

PRODUCES = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
CONTROLS = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

# JSON uses "Imprisoned"/"Obsolete"; prompt scale uses "trapped"/"exhausted".
STRENGTH_ORDER = ["Prosperous", "Strengthening", "Resting", "Imprisoned", "Obsolete", "Dead"]
STRENGTH_SCORE = {"Prosperous": 1.0, "Strengthening": 0.8, "Resting": 0.5,
                  "Imprisoned": 0.25, "Obsolete": 0.15, "Dead": 0.0}

INNER_PALACES_PROMPT = ["2", "5", "6", "7", "9"]
OUTER_PALACES_PROMPT = ["1", "3", "4", "8"]


def rel(a, b):
    """Five-phase relation of element a toward element b."""
    if a is None or b is None:
        return "UNDEFINED"
    if a == b:
        return "SAME"
    if PRODUCES[a] == b:
        return "PRODUCES"
    if PRODUCES[b] == a:
        return "PRODUCED_BY"
    if CONTROLS[a] == b:
        return "CONTROLS"
    if CONTROLS[b] == a:
        return "CONTROLLED_BY"
    return "UNDEFINED"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_qmdj():
    with open(QMDJ_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def jwrite(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    return path


def jread(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def twrite(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def aslist(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def heartbeat(line):
    path = os.path.join(STATE, "progress.md")
    os.makedirs(STATE, exist_ok=True)
    mode = "a" if os.path.exists(path) else "w"
    with open(path, mode, encoding="utf-8") as fh:
        if mode == "w":
            fh.write("# Heartbeat - Carpathia QMDJ Chart Analyst v4.0.0\n\n")
        fh.write(line.rstrip() + "\n")


def path_resolves(path, data):
    """True if a dotted path resolves to a real node in the source chart."""
    if not isinstance(path, str) or not path or "{" in path:
        return True
    cur = data
    for part in path.replace("$.", "").split("."):
        if isinstance(cur, dict):
            if part not in cur:
                return False
            cur = cur[part]
        elif isinstance(cur, list):
            return True
        else:
            return False
    return True


def prune_paths(node, data):
    """Recursively drop evidence paths that do not resolve in the source chart.

    Law 2: never cite a field that does not exist. A pruned path is not evidence.
    """
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k in ("paths", "evidence_paths") and isinstance(v, list):
                node[k] = [p for p in v if path_resolves(p, data)]
            else:
                prune_paths(v, data)
    elif isinstance(node, list):
        for v in node:
            prune_paths(v, data)
    return node
