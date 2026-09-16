"""Carpathia QMDJ Chart Analyst v5.0.0 — shared engine utilities.
Source JSON is immutable. Computed objects are written to vault/raw/state only."""
import json, hashlib, os, re, datetime, uuid

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_REL = "QMDJ/MARKETING/project_1.json"
SRC = os.path.join(REPO, SRC_REL)
VAULT = os.path.join(REPO, "vault")
RAW = os.path.join(VAULT, "raw")
STATE = os.path.join(RAW, "state")
TRACES = os.path.join(RAW, "traces")
WIKI = os.path.join(VAULT, "wiki")

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: str) -> str:
    with open(p, "rb") as f:
        return sha256_bytes(f.read())

def load_source():
    with open(SRC, "r", encoding="utf-8") as f:
        return json.load(f)

def src_raw_bytes():
    with open(SRC, "rb") as f:
        return f.read()

def dump_state(name: str, obj):
    p = os.path.join(STATE, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")

def load_state(name: str):
    with open(os.path.join(STATE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def state_exists(name: str) -> bool:
    return os.path.exists(os.path.join(STATE, name))

def write_text(path: str, text: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def progress(line: str):
    p = os.path.join(STATE, "progress.md")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"- `{utcnow()}` {line}\n")

def machine_update(**kw):
    m = load_state("machine.json") if state_exists("machine.json") else {}
    m.update(kw)
    m["updated_at"] = utcnow()
    dump_state("machine.json", m)

def next_id(kind: str) -> str:
    """Sequential claim/anomaly ids, persisted for determinism within run."""
    p = os.path.join(STATE, "id_counters.json")
    c = json.load(open(p)) if os.path.exists(p) else {}
    c[kind] = c.get(kind, 0) + 1
    json.dump(c, open(p, "w"), indent=2, sort_keys=True)
    return f"{kind}-{c[kind]:03d}"

# ---------- path resolver (citation integrity) ----------
_TOKEN = re.compile(r'([A-Za-z0-9_ ]+)|\["([^"]+)"\]|\[(\d+)\]')

def resolve_path(root, path: str):
    """Resolve normalized citation path against a dict/list tree.
    Supports: a.b.c, a["raw key"], a[0]. Returns (ok, value)."""
    cur = root
    i = 0
    for m in _TOKEN.finditer(path):
        name, braw, bidx = m.group(1), m.group(2), m.group(3)
        if name is not None and name.strip() in (".", ""):
            continue
        key = None
        if braw is not None:
            key = braw
        elif bidx is not None:
            key = int(bidx)
        elif name is not None:
            key = name.strip()
        if key is None:
            continue
        try:
            if isinstance(key, int):
                cur = cur[key]
            elif isinstance(cur, dict):
                cur = cur[key]
            else:
                return False, None
        except (KeyError, IndexError, TypeError):
            return False, None
    return True, cur

def cite_source(path: str):
    return resolve_path(load_source(), path)

def norm_key(k: str) -> str:
    return k.strip() if isinstance(k, str) else k

def norm_str(v):
    return v.strip() if isinstance(v, str) else v

# ---------- frozen reference tables (from analyst spec) ----------
PALACE_IDENTITY = {
    "1": dict(name="Kan", han="坎", dir="North", element="Water", branches=["Rat (Zi)"]),
    "2": dict(name="Kun", han="坤", dir="Southwest", element="Earth", branches=["Goat (Wei)", "Monkey (Shen)"]),
    "3": dict(name="Zhen", han="震", dir="East", element="Wood", branches=["Rabbit (Mao)"]),
    "4": dict(name="Xun", han="巽", dir="Southeast", element="Wood", branches=["Dragon (Chen)", "Snake (Si)"]),
    "5": dict(name="Center", han="中", dir="Center", element="Earth", branches=[]),
    "6": dict(name="Qian", han="乾", dir="Northwest", element="Metal", branches=["Dog (Xu)", "Pig (Hai)"]),
    "7": dict(name="Dui", han="兑", dir="West", element="Metal", branches=["Rooster (You)"]),
    "8": dict(name="Gen", han="艮", dir="Northeast", element="Earth", branches=["Ox (Chou)", "Tiger (Yin)"]),
    "9": dict(name="Li", han="离", dir="South", element="Fire", branches=["Horse (Wu)"]),
}
OPPOSITION = {"Kan": "Li", "Kun": "Gen", "Zhen": "Dui", "Xun": "Qian",
              "Dui": "Zhen", "Qian": "Xun", "Gen": "Kun", "Li": "Kan", "Center": None}
STAR_HOME = {
    "Tian Peng": 1, "Tian Rui": 2, "Tian Chong": 3, "Tian Fu": 4, "Tian Qin": 5,
    "Tian Xin": 6, "Tian Zhu": 7, "Tian Ren": 8, "Tian Ying": 9,
}
STAR_ALIASES = {  # English door/star names used by this exporter -> canonical
    "Heaven Pillar": "Tian Zhu", "Heaven Heart": "Tian Xin", "Heaven Peng": "Tian Peng",
    "Heaven Rui": "Tian Rui", "Heaven Qin": "Tian Qin", "Heaven Ren": "Tian Ren",
    "Heaven Ying": "Tian Ying", "Heaven Fu": "Tian Fu", "Heaven Chong": "Tian Chong",
    "Heavenly Auxiliary": "Tian Fu", "Heavenly Hero": "Tian Ying", "Heavenly Rui": "Tian Rui",
    "Heavenly Chong": "Tian Chong", "Heavenly Pillar": "Tian Zhu", "Heavenly Ren": "Tian Ren",
    "Heavenly Peng": "Tian Peng", "Heavenly Heart": "Tian Xin", "Heavenly Bird": "Tian Qin",
}
STEMS = {  # pinyin -> (element, polarity)
    "Jia": ("Wood", "Yang"), "Yi": ("Wood", "Yin"), "Bing": ("Fire", "Yang"),
    "Ding": ("Fire", "Yin"), "Wu": ("Earth", "Yang"), "Ji": ("Earth", "Yin"),
    "Geng": ("Metal", "Yang"), "Xin": ("Metal", "Yin"), "Ren": ("Water", "Yang"),
    "Gui": ("Water", "Yin"),
}
BRANCHES = {  # pinyin -> (animal, element, polarity)
    "Zi": ("Rat", "Water", "Yang"), "Chou": ("Ox", "Earth", "Yin"), "Yin": ("Tiger", "Wood", "Yang"),
    "Mao": ("Rabbit", "Wood", "Yin"), "Chen": ("Dragon", "Earth", "Yang"), "Si": ("Snake", "Fire", "Yin"),
    "Wu": ("Horse", "Fire", "Yang"), "Wei": ("Goat", "Earth", "Yin"), "Shen": ("Monkey", "Metal", "Yang"),
    "You": ("Rooster", "Metal", "Yin"), "Xu": ("Dog", "Earth", "Yang"), "Hai": ("Pig", "Water", "Yin"),
}
BRANCH_TO_PALACE = {"Zi": "1", "Wei": "2", "Shen": "2", "Mao": "3", "Chen": "4",
                    "Si": "4", "Xu": "6", "Hai": "6", "You": "7", "Chou": "8", "Yin": "8", "Wu": "9"}
HORSE_TABLE = {"Shen": "Yin", "Zi": "Yin", "Chen": "Yin", "Yin": "Shen", "Wu": "Shen",
               "Xu": "Shen", "Si": "Hai", "You": "Hai", "Chou": "Hai", "Hai": "Si",
               "Mao": "Si", "Wei": "Si"}
DOOR_ELEMENTS = {"Open": "Metal", "Rest": "Water", "Life": "Earth", "Shang": "Wood",
                 "Du": "Wood", "Scenery": "Fire", "Death": "Earth", "Fright": "Metal",
                 "Wound": "Wood", "Injury": "Wood"}
CONTROL = {("Wood", "Earth"), ("Earth", "Water"), ("Water", "Fire"), ("Fire", "Metal"), ("Metal", "Wood")}
GENERATE = {("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"), ("Metal", "Water"), ("Water", "Wood")}
STEM_COMBINE = [{"Jia", "Ji"}, {"Yi", "Geng"}, {"Bing", "Xin"}, {"Ding", "Ren"}, {"Wu", "Gui"}]
SIX_CLASH = [("Zi", "Wu"), ("Chou", "Wei"), ("Yin", "Shen"), ("Mao", "You"), ("Chen", "Xu"), ("Si", "Hai")]
SIX_COMBINE_B = [("Zi", "Chou"), ("Yin", "Hai"), ("Mao", "Xu"), ("Chen", "You"), ("Si", "Shen"), ("Wu", "Wei")]
INNER_PALACES = {"2", "5", "6", "7", "9"}
RAW_STRENGTH_MAP = {"Prosperous": ("prosperous", "computed_mapping"),
                    "Strong": ("strengthening", "computed_mapping"),
                    "Resting": ("resting", "computed_mapping"),
                    "Rest": ("resting", "computed_mapping"),
                    "Imprisoned": ("trapped", "computed_mapping"),
                    "Dead": ("dead", "computed_mapping"),
                    "Discarded": ("unknown_or_exhausted_like", "uncertain_mapping")}
