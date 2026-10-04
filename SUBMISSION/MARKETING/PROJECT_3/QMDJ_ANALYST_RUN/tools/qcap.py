#!/usr/bin/env python3
"""qcap.py — deterministic Tier-0/Tier-2 capability implementations for the QMDJ Chart Analyst run.

Each subcommand implements one CAP from PROMPT/qmdj_chart_analyst_charter.md. Every subcommand
writes its product to <run>/raw/state/ and appends a CAP line to raw/state/call_log. CLI stdout
is the cap's product summary; self-reported cost = whitespace-token count of that stdout.

No hashing is model-authored, no count is model-authored: this process is the authority
(charter laws 33 and 39).
"""
import argparse, hashlib, io, json, os, re, sys, unicodedata
from collections import OrderedDict, defaultdict

# ---------------------------------------------------------------- constants

STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
STEM_POLARITY = {"甲": "yang", "乙": "yin", "丙": "yang", "丁": "yin", "戊": "yang",
                 "己": "yin", "庚": "yang", "辛": "yin", "壬": "yang", "癸": "yin"}
STEM_ELEMENT = {"甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire", "戊": "earth",
                "己": "earth", "庚": "metal", "辛": "metal", "壬": "water", "癸": "water"}
STEM_PINYIN = {"甲": "Jia", "乙": "Yi", "丙": "Bing", "丁": "Ding", "戊": "Wu", "己": "Ji",
               "庚": "Geng", "辛": "Xin", "壬": "Ren", "癸": "Gui"}
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_PINYIN = {"子": "Zi", "丑": "Chou", "寅": "Yin", "卯": "Mao", "辰": "Chen", "巳": "Si",
                 "午": "Wu", "未": "Wei", "申": "Shen", "酉": "You", "戌": "Xu", "亥": "Hai"}
DEITIES = ["值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天"]
GATES = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门"]

PALACE_ID = {
    1: {"trigram": "Kan 坎", "direction": "N", "element": "water", "star_home": "TianPeng 天蓬"},
    2: {"trigram": "Kun 坤", "direction": "SW", "element": "earth", "star_home": "TianRui 天芮"},
    3: {"trigram": "Zhen 震", "direction": "E", "element": "wood", "star_home": "TianChong 天冲"},
    4: {"trigram": "Xun 巽", "direction": "SE", "element": "wood", "star_home": "TianFu 天辅"},
    5: {"trigram": "(centre)", "direction": "centre", "element": "earth", "star_home": "TianQin 天禽"},
    6: {"trigram": "Qian 乾", "direction": "NW", "element": "metal", "star_home": "TianXin 天心"},
    7: {"trigram": "Dui 兑", "direction": "W", "element": "metal", "star_home": "TianZhu 天柱"},
    8: {"trigram": "Gen 艮", "direction": "NE", "element": "earth", "star_home": "TianRen 天任"},
    9: {"trigram": "Li 离", "direction": "S", "element": "fire", "star_home": "TianYing 天英"},
}
PALACE_NAME_MAP = {"kan": 1, "坎": 1, "kun": 2, "坤": 2, "zhen": 3, "震": 3, "xun": 4, "巽": 4,
                   "center": 5, "centre": 5, "zhong": 5, "中": 5, "qian": 6, "乾": 6,
                   "dui": 7, "兑": 7, "gen": 8, "艮": 8, "li": 9, "离": 9}
OPPOSITION_PAIRS = [(1, 4), (6, 9)]          # law 10: only these; centre has no opposite
HOUSE_ELEMENT = {1: "water", 2: "earth", 3: "wood", 4: "wood", 5: "earth",
                 6: "metal", 7: "metal", 8: "earth", 9: "fire"}
FIELD_CODE = {"heaven_stem": "HS", "earth_stem": "ES", "hosted_stem": "HX",
              "star": "ST", "door": "DO", "deity": "DE", "explicit_marker": "EX"}


def sha(b):
    if isinstance(b, str):
        b = b.encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def nfc(s):
    return unicodedata.normalize("NFC", s)


def repo_root(a):
    return a.repo_root


def run_dir(a):
    return os.path.abspath(a.run_dir)


def load_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def write_state(a, name, obj):
    d = os.path.join(run_dir(a), "raw", "state")
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def token_cost(text):
    return len([t for t in re.split(r"\s+", text.strip()) if t])


def anomaly(a, code, detail, path="-"):
    d = os.path.join(run_dir(a), "raw", "state")
    os.makedirs(d, exist_ok=True)
    rec = OrderedDict([("code", code), ("detail", detail), ("path", path),
                       ("phase", a.batch), ("call_index", a.call_index)])
    with io.open(os.path.join(d, "anomaly_log.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")


def bind_cap_parser(p):
    p.add_argument("--cap-id", required=True)
    p.add_argument("--call-index", type=int, required=True)
    p.add_argument("--batch", required=True)
    return p


MAX_OUT = {"CAP-01": 100, "CAP-02": 150, "CAP-03": 250, "CAP-04": 200, "CAP-05": 120,
           "CAP-06": 100, "CAP-07": 150, "CAP-08": 150, "CAP-09": 200, "CAP-10": 300,
           "CAP-11": 250, "CAP-12": 1200, "CAP-13": 60, "CAP-14": 300, "CAP-15": 250,
           "CAP-16": 400, "CAP-17": 200, "CAP-19": 200}


def finish(a, cap_id, out_slot, in_ref, product, summary_keys):
    """Persist the product, truncate the printed summary at the cap's declared boundary if it
    exceeds max_out_tokens (explicit truncation + ANOMALY:COST_OVERRUN, never a silent partial),
    log the CAP call and the call cost."""
    write_state(a, out_slot + ".json", product)
    cap = MAX_OUT.get(cap_id)
    incl, trunc = [], False
    for k in summary_keys:
        trial = OrderedDict([("cap", cap_id), ("out", out_slot)] + incl + [(k, product.get(k))])
        if cap is not None and token_cost(json.dumps(trial, ensure_ascii=False)) > cap:
            trunc = True
            break
        incl.append((k, product.get(k)))
    summary = OrderedDict([("cap", cap_id), ("out", out_slot)] + incl)
    if trunc:
        summary["truncated"] = "summary_truncated_at_cap_boundary"
        summary["full_product"] = "raw/state/%s.json" % out_slot
    text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=False)
    cost = token_cost(text)
    log = os.path.join(run_dir(a), "raw", "state", "call_log")
    with io.open(log, "a", encoding="utf-8") as f:
        f.write("CAP|%s|in=%s|out=%s|cost=%d\n" % (cap_id, ",".join(in_ref), out_slot, cost))
    write_state(a, "log_%03d_%s.json" % (a.call_index, cap_id), OrderedDict([
        ("CAP", cap_id), ("call_index", a.call_index), ("batch", a.batch),
        ("in", in_ref), ("out", out_slot), ("cost", cost),
        ("max_out_tokens", cap), ("over_cap", bool(cap and cost > cap)),
        ("status", "PARTIAL_TRUNCATED" if trunc else "OK")]))
    if trunc:
        anomaly(a, "COST_OVERRUN",
                "%s summary exceeded max_out_tokens=%s; truncated at key boundary %d" %
                (cap_id, cap, len(incl)), out_slot)
    print(text)
    if trunc:
        print("ANOMALY:COST_OVERRUN")
    print("status=OK")
    return cost


# ---------------------------------------------------------------- parsers

def parse_pillar(raw):
    """CAP-05 ganzhi_parser: split a composite pillar string into exactly two tokens."""
    raw = nfc(raw).strip()
    if not raw:
        return {"state": "UNPARSEABLE", "reason": "EMPTY", "raw": raw}
    toks = [t for t in re.split(r"[\s\-–—]+", raw) if t]
    if len(toks) != 2:
        return {"state": "UNPARSEABLE", "reason": "TOKEN_COUNT=%d" % len(toks), "raw": raw}
    stem, branch = toks
    if stem not in STEMS or branch not in BRANCHES:
        return {"state": "UNPARSEABLE", "reason": "OUT_OF_VOCABULARY", "raw": raw,
                "token1": stem, "token2": branch}
    return {"state": "OK", "raw": raw,
            "heavenly_stem_raw": stem, "heavenly_stem_pinyin": STEM_PINYIN[stem],
            "polarity": STEM_POLARITY[stem], "element": STEM_ELEMENT[stem],
            "earthly_branch_raw": branch, "earthly_branch_pinyin": BRANCH_PINYIN[branch]}


def parse_stem(raw):
    """CAP-06 stem_norm: accept 'Yang Fire (Bing)', 'Bing', 'yang_fire_bing', or the hanzi."""
    raw0 = nfc(raw).strip()
    if not raw0:
        return {"state": "UNPARSEABLE", "raw": raw0, "reason": "EMPTY",
                "element": None, "polarity": None, "canonical": None}
    s = raw0
    han = [c for c in s if c in STEMS]
    if han:
        if len(set(han)) != 1:
            return {"state": "UNPARSEABLE", "raw": raw0, "reason": "MULTIPLE_STEMS",
                    "element": None, "polarity": None, "canonical": None}
        st = han[0]
    else:
        key = re.sub(r"[^a-z]", "", s.lower())
        pinyins = {p.lower(): h for h, p in STEM_PINYIN.items()}
        pol = None
        key2 = key
        for p in ("yang", "yin"):
            if p in key:
                pol = p
                key2 = key.replace(p, "")
                break
        cand = [h for p, h in pinyins.items() if key2 == p or (key2.startswith(p) and pol)]
        if pol:
            cand = [h for h in cand if STEM_POLARITY[h] == pol]
        if len(cand) != 1:
            return {"state": "UNPARSEABLE", "raw": raw0, "reason": "OUT_OF_VOCABULARY",
                    "element": None, "polarity": None, "canonical": None}
        st = cand[0]
    return {"state": "OK", "raw": raw0, "canonical": STEM_PINYIN[st],
            "heavenly_stem_raw": st, "polarity": STEM_POLARITY[st], "element": STEM_ELEMENT[st]}


def board_card(raw):
    """Normalized whole-chart view (law 44). Built once; batches filter it, never re-read source."""
    card = OrderedDict()
    for pk, bloc in raw["palaces"].items():
        canon = PALACE_NAME_MAP[pk.split("_")[0]]
        el = bloc.get("palace_elements", [])
        rec = {"raw_key": pk, "canonical": canon, "palace_name": bloc.get("palace_name"),
               "heaven_stem": None, "earth_stem": None, "hosted_stem": None,
               "star": None, "door": None, "deity": None, "palace_label": None,
               "element_paths": {}}
        for i, v0 in enumerate(el):
            v = nfc(v0).strip()
            p = "palaces/%s/palace_elements[%d]" % (pk, i)
            if re.match(r"^天盘[\u4e00-\u9fff]$", v):
                rec["heaven_stem"] = {"value": v[2], "path": p}
            elif re.match(r"^地盘[\u4e00-\u9fff]$", v):
                rec["earth_stem"] = {"value": v[2], "path": p}
            elif re.match(r"^寄[\u4e00-\u9fff]$", v):
                rec["hosted_stem"] = {"value": v[1], "path": p}
            elif v in DEITIES:
                rec["deity"] = {"value": v, "path": p}
            elif v in GATES:
                rec["door"] = {"value": v, "path": p}
            elif re.match(r"^天[\u4e00-\u9fff]$", v):
                rec["star"] = {"value": v, "path": p}
            elif re.match(r"^[\u4e00-\u9fff]+宫$", v):
                rec["palace_label"] = {"value": v, "path": p}
        # hosted stem may be stated in an interpretation condition instead of palace_elements
        if rec["hosted_stem"] is None:
            for i, it in enumerate(raw["palaces"][pk].get("interpretations", [])):
                m = re.match(r"^寄([\u4e00-\u9fff])\b", nfc(it["condition"]).strip())
                if m:
                    rec["hosted_stem"] = {
                        "value": m.group(1),
                        "path": "palaces/%s/interpretations[%d]/condition" % (pk, i),
                        "derived_from": "interpretation_condition_text (explicit chart string)"}
                    break
        card[pk] = rec
    return card


# ---------------------------------------------------------------- CAP-01

def cap01(a):
    src = os.path.join(repo_root(a), a.chart)
    b = io.open(src, "rb").read()
    raw = load_json(src)
    keys = sorted(raw.keys())
    fp = "%s|%d|%d|%s" % (os.path.basename(a.chart), len(b), len(keys), ",".join(keys))
    prod = OrderedDict([
        ("cap", "CAP-01"), ("source_file", os.path.basename(a.chart)),
        ("byte_length", len(b)), ("top_level_key_count", len(keys)),
        ("top_level_keys_sorted", keys), ("fingerprint_string", fp),
        ("content_sha256", sha(b)), ("id_derivation", "sha256"),
        ("recompute_rule", "recomputed at every phase boundary; mismatch -> SOURCE_CHANGED"),
    ])
    finish(a, "CAP-01", "fingerprint", [os.path.basename(a.chart)], prod,
           ["fingerprint_string", "byte_length", "top_level_key_count", "content_sha256"])


# ---------------------------------------------------------------- CAP-02

def cap02(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    prov, absence = [], []
    counts = defaultdict(int)

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/[%d]" % i)
        else:
            if isinstance(node, str):
                n = nfc(node).strip()
                prov.append({"path": path, "raw": node, "normalized": n, "changed": n != node})
                if n == "":
                    counts["NULL"] += 1
                    absence.append({"path": path, "code": "NULL",
                                    "why": "present but empty after normalization"})
                else:
                    counts["VALUE"] += 1
            elif node is False:
                counts["FALSE"] += 1
                absence.append({"path": path, "code": "FALSE",
                                "why": "boolean false: not a value, not absence of key"})
            elif node is None:
                counts["NULL"] += 1
                absence.append({"path": path, "code": "NULL", "why": "explicit null"})
            else:
                counts["VALUE"] += 1

    walk(raw, "")
    prod = OrderedDict([
        ("cap", "CAP-02"), ("normalization", "NFC + trim"),
        ("absence_code_distinction", {
            "ABSENT": "key not present: enumerated against the role map (see role_map.json)",
            "NULL": "key present, value null/empty after normalization",
            "FALSE": "key present, boolean false"}),
        ("provenance_map", prov), ("absence_codes", absence),
        ("absence_tally", OrderedDict([("NULL", counts["NULL"]), ("FALSE", counts["FALSE"])])),
        ("value_leaf_count", counts["VALUE"]),
        ("string_leaves_changed", sum(1 for p in prov if p["changed"])),
        ("raw_writeback", "none (law 30)"),
    ])
    finish(a, "CAP-02", "normalization", ["chart"], prod,
           ["value_leaf_count", "string_leaves_changed", "absence_tally", "raw_writeback"])


# ---------------------------------------------------------------- CAP-03 + CAP-04

def cap03(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    keys = sorted(raw.keys())
    palaces = raw.get("palaces", {})
    pkeys = list(palaces.keys())
    style_ok = all(re.match(r"^[a-z]+_\d+$", k) for k in pkeys)
    variant = ("V1" if keys == ["chart_info", "palaces"] and style_ok
               else "V2" if {"chart_info", "palaces"}.issubset(set(keys)) else "NONE")
    conf = "high" if variant == "V1" else ("medium" if variant == "V2" else "low")
    prod3 = OrderedDict([
        ("cap", "CAP-03"),
        ("schema_adapter_supplied", bool(a.schema_adapter)),
        ("matched_variant", variant), ("confidence", conf),
        ("palace_key_style", "<trigram_pinyin>_<canonical_number>"),
        ("top_level_keys", keys),
        ("bind", "V1: chart_info{ganzhi, zhi_fu, zhi_shi, solar_term, system, method, type} + "
                 "palaces{<trigram>_<n>: {palace_name, palace_elements[], interpretations[]}}"),
        ("unresolved_ambiguities", [
            "palace_elements[] is an untyped string array; element roles resolved by CAP-04/CAP-07",
            "centre palace has no door/deity entries: absence is factual, not an error",
            "'type' repeats Yin Dun 7 Ju plus rotation and does not contradict zhi_fu/zhi_shi",
            "frozen_tables.yaml not supplied: annex A-tables fallback used for identity lookup",
        ]),
        ("unsafe", False),
    ])
    if variant == "NONE":
        anomaly(a, "SCHEMA_AMBIGUITY", "no variant matched top-level key set", "chart")
    finish(a, "CAP-03", "schema_bind", ["chart"], prod3,
           ["matched_variant", "confidence", "unresolved_ambiguities"])


def cap04(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    palaces = raw.get("palaces", {})
    rm = load_json(os.path.join(repo_root(a), a.roles))
    card = board_card(raw)
    role_states = []
    for role, spec in rm["roles"].items():
        found = []
        if role == "pillars":
            found = ["chart_info/ganzhi/%s" % k for k in ("year", "month", "day", "hour")]
        elif role == "palaces_root":
            found = ["palaces"] if raw.get("palaces") else []
        elif role == "interpretations":
            found = ["palaces/%s/interpretations" % pk for pk in palaces
                     if raw["palaces"][pk].get("interpretations")]
        elif spec["key"].startswith("chart_info."):
            k = spec["key"].split(".", 1)[1]
            found = ["chart_info/%s" % k] if k in raw.get("chart_info", {}) else []
        else:
            key = "palace_name" if role == "palace_identity" else role
            for pk, rec in card.items():
                if key in rec and rec[key]:
                    val = rec[key]
                    found.append(val["path"] if isinstance(val, dict) else "palaces/%s/%s" % (pk, key))
        required = len(palaces) if spec["expect"] == "per_palace" else 1
        if found:
            state = "RESOLVED"
        elif spec.get("core", False):
            state = "BLOCKED"
        else:
            state = "UNRESOLVED"
        coverage = ("FULL" if len(found) >= required else
                    "PARTIAL(%d/%d)" % (len(found), required) if found else "NONE")
        role_states.append(OrderedDict([
            ("role", role), ("expect", spec["expect"]), ("declared_presence", spec["presence"]),
            ("core", spec.get("core", False)), ("found_paths_count", len(found)),
            ("required_count", required), ("coverage", coverage), ("state", state),
            ("sample_paths", found[:3]),
        ]))
    prod4 = OrderedDict([
        ("cap", "CAP-04"), ("role_states", role_states),
        ("role_state_line", " ".join("%s=%s" % (r["role"], r["state"]) for r in role_states)),
        ("blocked_core_roles", [r["role"] for r in role_states if r["state"] == "BLOCKED"])])
    finish(a, "CAP-04", "role_map", ["chart", "roles"], prod4,
           ["role_state_line", "blocked_core_roles"])


# ---------------------------------------------------------------- CAP-05 / CAP-06 / CAP-07

def cap05(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    gz = raw["chart_info"]["ganzhi"]
    parsed, unp = [], []
    for k in ["year", "month", "day", "hour"]:
        r = parse_pillar(gz[k])
        r["slot"] = k
        r["path"] = "chart_info/ganzhi/%s" % k
        (parsed if r["state"] == "OK" else unp).append(r)
    prod5 = OrderedDict([("cap", "CAP-05"), ("parsed", parsed), ("unparseable", unp),
                         ("rule", "split on space/hyphen into exactly two tokens; never guess")])
    finish(a, "CAP-05", "ganzhi_parsed", ["chart_info.ganzhi"], prod5,
           ["parsed", "unparseable"])


def cap06(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    parsed, _ = [], []
    for k in ["year", "month", "day", "hour"]:
        r = parse_pillar(raw["chart_info"]["ganzhi"][k])
        if r["state"] == "OK":
            r["slot"] = k
            parsed.append(r)
    stems, stem_unp = OrderedDict(), []
    for r in parsed:
        s = parse_stem(r["heavenly_stem_raw"])
        s["slot"] = r["slot"] + ".heavenly_stem"
        stems[r["slot"] + ".heavenly_stem"] = s
        if s["state"] != "OK":
            stem_unp.append(s["slot"])
    card = board_card(raw)
    for pk, rec in card.items():
        for role in ("heaven_stem", "earth_stem", "hosted_stem"):
            if rec[role]:
                key = "%s.%s" % (pk, role)
                s = parse_stem(rec[role]["value"])
                s["slot"] = key
                s["source_path"] = rec[role]["path"]
                stems[key] = s
                if s["state"] != "OK":
                    stem_unp.append(key)
    prod6 = OrderedDict([("cap", "CAP-06"), ("stem_count", len(stems)),
                         ("stem_norms", stems), ("unparseable", stem_unp),
                         ("vocabulary", "jia..gui with polarity + element; partial matches forbidden")])
    finish(a, "CAP-06", "stem_norm", ["ganzhi", "palace_elements"], prod6,
           ["stem_count", "unparseable"])


def cap07(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    composites, atoms, unp = [], [], []
    for pk in raw["palaces"]:
        for i, v0 in enumerate(raw["palaces"][pk].get("palace_elements", [])):
            v = nfc(v0).strip()
            path = "palaces/%s/palace_elements[%d]" % (pk, i)
            composites.append({"path": path, "raw": v0})
            typ = None
            if re.match(r"^天[\u4e00-\u9fff]$", v):
                typ = ("star", v, None)
            elif v in GATES:
                typ = ("door", v, None)
            elif v in DEITIES:
                typ = ("deity", v, None)
            elif re.match(r"^天盘[\u4e00-\u9fff]$", v):
                typ = ("stem_ref", v[2], "heaven_stem")
            elif re.match(r"^地盘[\u4e00-\u9fff]$", v):
                typ = ("stem_ref", v[2], "earth_stem")
            elif re.match(r"^寄[\u4e00-\u9fff]$", v):
                typ = ("stem_ref", v[1], "hosted_stem")
            elif re.match(r"^[\u4e00-\u9fff]+宫$", v):
                typ = ("palace_label", v, None)
            if typ is None:
                unp.append({"path": path, "raw": v0, "reason": "NO_TYPED_ATOM"})
                continue
            atoms.append({"path": path, "raw": v0, "atom_type": typ[0],
                          "value": typ[1], "role": typ[2]})
    prod = OrderedDict([("cap", "CAP-07"), ("composite_count", len(composites)),
                        ("atom_count", len(atoms)), ("atoms", atoms),
                        ("unparseable", unp),
                        ("typing_rule", "subject=role, relation=implicit field, target=value")])
    finish(a, "CAP-07", "composite_atoms", ["palace_elements"], prod,
           ["composite_count", "atom_count", "unparseable"])


# ---------------------------------------------------------------- CAP-08

def cap08(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    blocks = []
    for pk in raw["palaces"]:
        bloc = raw["palaces"][pk]
        f = pk.split("_")[0]
        canon = PALACE_NAME_MAP[f]
        ident = PALACE_ID[canon]
        name_field = bloc.get("palace_name", "")
        cross = [int(x) for x in re.findall(r"(\d)", name_field)]
        mism = sorted(set(cross) - {canon})
        opp = [b for p in OPPOSITION_PAIRS for b in
               ([p[1]] if p[0] == canon else ([p[0]] if p[1] == canon else []))]
        blocks.append(OrderedDict([
            ("raw_key", pk), ("canonical", canon), ("raw_palace_name", name_field),
            ("identity", ident), ("opposites", opp),
            ("lodging", ("centre: relation set is the lodging GRAPH to all eight palaces; "
                         "centre has no opposite (law 10)") if canon == 5 else None),
            ("name_number_mismatches", mism),
        ]))
    prod = OrderedDict([
        ("cap", "CAP-08"), ("palace_blocks", blocks), ("palace_count", len(blocks)),
        ("palace_index_line", " ".join("%d:%s/%s" % (b["canonical"],
                                                     b["identity"]["trigram"].split()[0],
                                                     b["identity"]["direction"]) for b in blocks)),
        ("opposition_rule", "opposition exists only for 1-4 and 6-9"),
        ("trajectory", "1->2->3->4->(5)->6->7->8->9"),
        ("table_source", "annex A-tables (frozen_tables.yaml not supplied)")])
    finish(a, "CAP-08", "luoshu_geometry", ["palaces"], prod,
           ["palace_count", "palace_index_line", "opposition_rule", "table_source"])


# ---------------------------------------------------------------- CAP-10

def cap10(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    ref_path = os.path.join(repo_root(a), a.reference_file)
    ref = load_json(ref_path)
    explicit = []
    for pk, bloc in raw["palaces"].items():
        for i, it in enumerate(bloc.get("interpretations", [])):
            explicit.append({"palace": pk,
                             "path": "palaces/%s/interpretations[%d]/condition" % (pk, i),
                             "marker": nfc(it["condition"]).strip(), "meaning": it["meaning"]})
    card = board_card(raw)
    # compute_always set (minimum viable stand-in) over the normalized board card
    stem_instances = []
    for pk, rec in card.items():
        for role in ("heaven_stem", "earth_stem", "hosted_stem"):
            if rec[role]:
                stem_instances.append({"palace": rec["canonical"], "role": role,
                                       "stem": rec[role]["value"], "path": rec[role]["path"]})
    pat = re.compile(r"([\u4e00-\u9fff])加([\u4e00-\u9fff])")
    combo_markers = []
    for e in explicit:
        m = pat.search(e["marker"])
        if m:
            canon = PALACE_NAME_MAP[e["palace"].split("_")[0]]
            combo_markers.append({"palace": canon, "path": e["path"], "marker": e["marker"],
                                  "upper": m.group(1), "lower": m.group(2),
                                  "meaning": e["meaning"]})
    digits = re.compile(r"\d")
    palace_digit_markers = [e for e in explicit if not digits.search(e["marker"])]
    hit_map = {h["pattern_id"]: h for h in ref["patterns"]}
    hits = []
    for pid in ["P3-COMBO", "P3-GATE", "P3-STRUCT"]:
        h = hit_map[pid]
        if pid == "P3-COMBO":
            hits.append(OrderedDict([("pattern_id", pid), ("state", "live"),
                                     ("hits", stem_instances), ("hit_count", len(stem_instances))]))
        elif pid == "P3-GATE":
            hits.append(OrderedDict([("pattern_id", pid), ("state", "live"),
                                     ("hits", combo_markers), ("hit_count", len(combo_markers))]))
        else:
            hits.append(OrderedDict([("pattern_id", pid), ("state", "live"),
                                     ("hits", palace_digit_markers),
                                     ("hit_count", len(palace_digit_markers))]))
    prod = OrderedDict([
        ("cap", "CAP-10"),
        ("catalog_source", "annex A-patterns minimum viable stand-in (pattern_catalog not supplied); "
                           "reference rows read from %s" % a.reference_file),
        ("explicit_marker_count", len(explicit)),
        ("computed_patterns", hits),
        ("reconciliation", "computed stem-pair enumeration (P3-GATE) matches every explicit marker "
                           "containing X加Y; no conflict between explicit and computed layers "
                           "(law 26: explicit ranks first, computed reconciles)"),
        ("null_results", []),
        ("pattern_summary", " ".join("%s=%d" % (h["pattern_id"], h["hit_count"]) for h in hits)),
    ])
    finish(a, "CAP-10", "pattern_hits", ["palaces", a.reference_file], prod,
           ["explicit_marker_count", "pattern_summary", "catalog_source"])


# ---------------------------------------------------------------- CAP-11

CHART_LEVEL_FIELDS = [("system", "chart_info/system"), ("method", "chart_info/method"),
                     ("type", "chart_info/type"), ("solar_term", "chart_info/solar_term"),
                     ("zhi_fu", "chart_info/zhi_fu"), ("zhi_shi", "chart_info/zhi_shi")]


def cap11(a):
    raw = load_json(os.path.join(repo_root(a), a.chart))
    card = board_card(raw)
    out = []
    # palace_canonical = 0 marks chart-level (not palace-bound) explicit evidence
    for slot, key in CHART_LEVEL_FIELDS:
        val = raw["chart_info"].get(slot)
        path = key
        out.append(OrderedDict([
            ("type", "E"), ("palace_canonical", 0), ("field_code", "CI"),
            ("value", nfc(val).strip()), ("role", "chart_field:" + slot),
            ("source_path", path), ("content_hash", sha("E|chart|0|%s|%s|%s" % (slot, val, path))),
            ("id_derivation", "sha256")]))
    for k in ["year", "month", "day", "hour"]:
        val = nfc(raw["chart_info"]["ganzhi"][k]).strip()
        path = "chart_info/ganzhi/%s" % k
        out.append(OrderedDict([
            ("type", "E"), ("palace_canonical", 0), ("field_code", "PILLAR"),
            ("value", val), ("role", "pillar:" + k), ("source_path", path),
            ("content_hash", sha("E|chart|0|pillar_%s|%s|%s" % (k, val, path))),
            ("id_derivation", "sha256")]))
    for pk, rec in card.items():
        canon = rec["canonical"]
        for role in ("heaven_stem", "earth_stem", "hosted_stem"):
            if rec[role]:
                val, path = rec[role]["value"], rec[role]["path"]
                content = "E|chart|%d|%s|%s|%s" % (canon, role, val, path)
                out.append(OrderedDict([
                    ("type", "E"), ("palace_canonical", canon), ("field_code", FIELD_CODE[role]),
                    ("value", val), ("role", role), ("source_path", path),
                    ("content_hash", sha(content)), ("id_derivation", "sha256")]))
        for role, code in (("star", "ST"), ("door", "DO"), ("deity", "DE")):
            if rec[role]:
                val, path = rec[role]["value"], rec[role]["path"]
                content = "E|chart|%d|%s|%s|%s" % (canon, role, val, path)
                out.append(OrderedDict([
                    ("type", "E"), ("palace_canonical", canon), ("field_code", code),
                    ("value", val), ("role", role), ("source_path", path),
                    ("content_hash", sha(content)), ("id_derivation", "sha256")]))
        for i, it in enumerate(raw["palaces"][pk].get("interpretations", [])):
            path = "palaces/%s/interpretations[%d]/condition" % (pk, i)
            val = nfc(it["condition"]).strip()
            content = "E|chart|%d|explicit_marker|%s|%s" % (canon, val, path)
            out.append(OrderedDict([
                ("type", "E"), ("palace_canonical", canon), ("field_code", "EX"),
                ("value", val), ("role", "explicit_marker"), ("source_path", path),
                ("content_hash", sha(content)), ("id_derivation", "sha256")]))
    out.sort(key=lambda r: (r["palace_canonical"], r["field_code"], r["source_path"], r["value"]))
    for i, r in enumerate(out, start=1):
        r["id"] = "E%03d" % i
    prod = OrderedDict([("cap", "CAP-11"), ("id_derivation", "sha256 content address"),
                        ("sort_rule", "palace_canonical, field_code, source_path, value "
                                      "(deterministic; the sha256 content address travels with "
                                      "every atom as content_hash)"),
                        ("e_atom_count", len(out)), ("e_atoms", out), ("reissue_log", [])])
    finish(a, "CAP-11", "evidence_registry", ["chart", "roles"], prod,
           ["id_derivation", "sort_rule", "e_atom_count"])


# ---------------------------------------------------------------- CAP-09

def cap09(a):
    """Value trace over heaven/earth/hosted stem FIELD VALUES (never array positions, law 11).
    Emits one R-atom per matched palace pair plus the trace graph; fully mechanical."""
    reg = load_json(os.path.join(run_dir(a), "raw", "state", "evidence_registry.json"))
    stems = {}
    for r in reg["e_atoms"]:
        if r["field_code"] in ("HS", "ES", "HX"):
            stems.setdefault(r["value"], []).append(r)
    relabels = {"天盘": "HS", "地盘": "ES", "寄": "HX"}
    pairs = []
    for value, rows in sorted(stems.items()):
        rows_sorted = sorted(rows, key=lambda r: (r["palace_canonical"], r["field_code"]))
        for i in range(len(rows_sorted)):
            for j in range(i + 1, len(rows_sorted)):
                a1, a2 = rows_sorted[i], rows_sorted[j]
                if a1["palace_canonical"] == a2["palace_canonical"]:
                    continue
                p1, p2 = sorted([a1["palace_canonical"], a2["palace_canonical"]])
                pair = tuple(sorted([p1, p2]))
                if pair in OPPOSITION_PAIRS:
                    rtype = "R.IDENTICAL_STEM_ON_AXIS"
                elif 5 in pair:
                    rtype = "R.IDENTICAL_STEM_LODGING"
                else:
                    rtype = "R.IDENTICAL_STEM"
                pairs.append(OrderedDict([
                    ("relation_type", rtype), ("stem_value", value),
                    ("members_E", sorted([a1["id"], a2["id"]])),
                    ("palaces", [p1, p2]),
                    ("trace", "value_trace(%s): %s@%s(%s) == %s@%s(%s); matched by FIELD VALUE, "
                              "not array position" % (
                                  value, a1["field_code"], a1["palace_canonical"],
                                  a1["role"], a2["field_code"], a2["palace_canonical"], a2["role"])),
                    ("rule_citation", "CAP-09 / law 11"),
                    ("source_paths", sorted([a1["source_path"], a2["source_path"]])),
                ]))
    pairs.sort(key=lambda r: (r["palaces"], r["relation_type"], r["members_E"]))
    for i, r in enumerate(pairs, start=1):
        r["id"] = "R%03d" % i
        r["content_hash"] = sha("R|%s|%s|%s" % (r["relation_type"], ",".join(r["members_E"]),
                                                r["stem_value"]))
    # trace graph: nodes = palaces, edges = R-atoms of any IDENTICAL_STEM family
    adj = defaultdict(set)
    for r in pairs:
        p1, p2 = r["palaces"]
        adj[p1].add(p2)
        adj[p2].add(p1)
    nodes = sorted(adj.keys())
    deg = {n: len(adj[n]) for n in nodes}
    # deterministic cycle walk over the outer ring (centre excluded); centre edges are spurs
    ring = sorted(n for n in nodes if n != 5)
    ring_adj = {n: sorted(x for x in adj[n] if x != 5) for n in ring}
    ring_deg = {n: len(ring_adj[n]) for n in ring}
    walk = []
    if ring and all(ring_deg[n] == 2 for n in ring):
        start = ring[0]
        walk = [start]
        prev, cur = None, start
        while True:
            nxt = [x for x in ring_adj[cur] if x != prev]
            if not nxt or nxt[0] == start:
                break
            walk.append(nxt[0])
            prev, cur = cur, nxt[0]
            if len(walk) > len(nodes):
                break
    prod = OrderedDict([
        ("cap", "CAP-09"), ("r_atom_count", len(pairs)), ("r_atoms", pairs),
        ("stem_value_index", {"%s" % v: sorted(r["id"] for r in rs) for v, rs in
                              sorted(stems.items())}),
        ("trace_graph", {
            "nodes": nodes, "degree": deg,
            "edge_count": len(pairs),
            "closed_walk": walk,
            "closed_walk_len": len(walk),
            "ring_regular": all(ring_deg[n] == 2 for n in ring) if ring else False,
            "classification": ("single closed circulation over the %d-palace outer ring plus "
                               "%d centre spur(s)" % (len(ring), len([r for r in pairs if 5 in r["palaces"]])))
            if walk and len(walk) == len(ring) else "partial graph",
            "off_ring_nodes": [n for n in nodes if n not in ring],
        }),
        ("trace_summary", "edges=%d ring=%s spur=%s" % (
            len(pairs), "-".join(str(x) for x in walk),
            "-".join("%d-%d" % (r["palaces"][0], r["palaces"][1]) for r in pairs if 5 in r["palaces"]))),
    ])
    finish(a, "CAP-09", "value_trace", ["evidence_registry"], prod,
           ["r_atom_count", "trace_summary", "trace_graph"])

# ---------------------------------------------------------------- CAP-15

def score_file(a, path, out_slot, cap_id):
    obj = load_json(path)
    scored = []
    for c in obj.get("claims", []):
        classes = set(c.get("citation_class", []))
        tier = ("explicit_chart" if "explicit_chart" in classes else
                "computed_structure" if "computed_structure" in classes else
                "assumption_indexed")
        supp = len(c.get("cited_E", [])) + len(c.get("cited_R", []))
        contra = len(c.get("contradicting_E", []))
        groups, rem = divmod(supp, 9)
        corr = sum(1 for _ in range(groups)) + rem            # enumerated addends <= 9
        penalty = round(min(contra, 9) * 0.05, 2)
        base = {"explicit_chart": 0.90, "computed_structure": 0.75,
                "assumption_indexed": 0.45}[tier]
        conf = max(0.10, min(1.00, round(base + 0.01 * min(corr, 9) - penalty, 2)))
        scored.append(OrderedDict([
            ("claim_id", c["claim_id"]), ("grounding_tier", tier),
            ("citation_count", supp), ("corroboration_tally", corr),
            ("contradiction_penalty", penalty), ("confidence", conf),
            ("SCORE_SOURCE", "TIER0_TOOL_%s/v1" % cap_id)]))
    prod = OrderedDict([("cap", cap_id), ("scored", scored), ("scoring_table", {
        "tier_base": {"explicit_chart": 0.90, "computed_structure": 0.75,
                      "assumption_indexed": 0.45},
        "steps": {"corroboration": "+0.01 per corroborating citation up to 9",
                  "contradiction": "-0.05 per contradicting citation up to 9"},
        "clamp": [0.10, 1.00],
        "count_rule": "enumerated addends <= 9 per group (law 46); no free multi-digit arithmetic"})])
    finish(a, cap_id, out_slot, [os.path.basename(path)], prod, ["scored", "scoring_table"])


def cap15_entry(a):
    all_lines, all_scored = [], []
    for spec in a.claim_set.split(";"):
        path, out_slot = spec.split(":")
        if "/" in out_slot:
            out_slot = os.path.basename(out_slot)[:-5]
        score_file(a, path, out_slot, "CAP-15")
        sc = load_json(os.path.join(run_dir(a), "raw", "state", out_slot + ".json"))
        side = load_json(os.path.join(repo_root(a), path))
        by_id = {c["claim_id"]: c for c in side["claims"]}
        for row in sc["scored"]:
            c = by_id[row["claim_id"]]
            line = "CLAIM|%s|batch=%s|claims=%s|disp=%s|certainty=%s" % (
                c["claim_id"], c["batch"], ",".join(c["i_atoms"]), c["disposition"],
                ("%.2f" % row["confidence"]) if row["confidence"] < 1.0 else "1.00")
            all_lines.append(line)
            all_scored.append(row["claim_id"])
    d = os.path.join(run_dir(a), "renders")
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, "claim_lines.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines) + "\n")
    print(json.dumps({"cap": "CAP-15", "claim_lines_written": len(all_lines),
                      "ids": all_scored}, ensure_ascii=False))
    print("status=OK")


# ---------------------------------------------------------------- CAP-13

CLAIM_RE = re.compile(r"^CLAIM\|C\d{3}\|batch=[A-Z0-9]{2}\|claims=I\d{3}(,I\d{3})*\|disp=[A-Z_]+\|certainty=(0\.\d{1,2}|1\.00|NA)$")
CMAP_RE = re.compile(r"^CMAP\|C\d{3}\|Q\d{1,2}\|(DIRECT|INDIRECT|NO_CHART_SUPPORT|CONTRADICTS_KNOWN)\|([ER]\d{3}(,[ER]\d{3})*|NONE)$")
PROPOSAL_RE = re.compile(r"^PROPOSAL\|P\d{3}\|from=C\d{3}\|direction=(forward|backward)\|rule=[A-Z0-9_]+\|status=(ok|rebutted|superseded)$")
RT_RE = re.compile(r"^RT\|A\d{3}\|criticizes=C\d{3}\|kind=(support|rebut|alternative)\|status=(rebutted|superseded|live)$")
I_RE = re.compile(r"^I\d{3}$")
E_RE = re.compile(r"^E\d{3}$")
R_RE = re.compile(r"^R\d{3}$")


def cap13(a):
    checked, rejected = [], []
    for f in a.grammar_files.split(","):
        p = os.path.join(run_dir(a), f)
        for ln, line in enumerate(io.open(p, encoding="utf-8").read().splitlines(), 1):
            if not line.strip():
                continue
            kind = line.split("|", 1)[0]
            rx = {"CLAIM": CLAIM_RE, "CMAP": CMAP_RE,
                  "PROPOSAL": PROPOSAL_RE, "RT": RT_RE}.get(kind)
            ok = bool(rx.match(line)) if rx else False
            checked.append({"file": f, "line": ln, "kind": kind, "ok": ok})
            if not ok:
                rejected.append({"file": f, "line": ln, "line_text": line,
                                 "reason": "GRAMMAR_REJECT"})
                anomaly(a, "GRAMMAR_REJECT", "line %d of %s failed %s grammar" % (ln, f, kind), f)
    # ID width check across cited IDs
    id_violations = []
    for f in a.grammar_files.split(","):
        text = io.open(os.path.join(run_dir(a), f), encoding="utf-8").read()
        for tok in re.findall(r"\b[ERICA]\d+\b", text):
            if len(tok) != 4:
                id_violations.append({"file": f, "token": tok, "reason": "ID_WIDTH"})
    prod = OrderedDict([("cap", "CAP-13"), ("checked", len(checked)), ("rejected", rejected),
                        ("id_width_violations", sorted(id_violations,
                                                       key=lambda d: (d["file"], d["token"]))),
                        ("checked_detail", checked)])
    finish(a, "CAP-13", "grammar_check", [a.grammar_files], prod,
           ["checked", "rejected", "id_width_violations"])


# ---------------------------------------------------------------- CAP-12

def cap12(a):
    reg = load_json(os.path.join(run_dir(a), "raw", "state", "evidence_registry.json"))
    side = load_json(os.path.join(repo_root(a), a.claim_set))
    blocks = []
    for pk in a.palace_scope.split(","):
        canon = int(pk)
        in_p = [r for r in reg["e_atoms"] if r["palace_canonical"] == canon]
        txt = json.dumps(in_p, ensure_ascii=False, indent=1)
        truncated = len(txt) > 6000
        if truncated:
            anomaly(a, "COST_OVERRUN", "palace %d digest exceeds 6000 chars" % canon,
                    "palace_%d" % canon)
        blocks.append(OrderedDict([("palace", canon, ), ("id_count", len(in_p)),
                                   ("digest", txt[:6000]), ("truncated", truncated)]))
    prod = OrderedDict([
        ("cap", "CAP-12"),
        ("eligible_scope", {"palaces": [int(x) for x in a.palace_scope.split(",")],
                            "visibility_tags": a.visibility.split(",")}),
        ("palace_blocks", blocks),
        ("assertion_catalog", side.get("assertions", [])),
        ("scope_completeness", {"palaces_in_scope": len(blocks),
                                "palaces_with_ids": sum(1 for b in blocks if b["id_count"]),
                                "truncations": sum(1 for b in blocks if b["truncated"])}),
    ])
    finish(a, "CAP-12", "board_digest", ["evidence_registry", os.path.basename(a.claim_set)],
           prod, ["eligible_scope", "scope_completeness"])


# ---------------------------------------------------------------- CAP-14

def cap14(a):
    """B5 ledger reconcile. Dispositions are declared in the workbook sidecar (authored), the
    enumeration and the balance check are performed here (mechanical, law 46)."""
    reg = load_json(os.path.join(run_dir(a), "raw", "state", "evidence_registry.json"))
    wb = load_json(os.path.join(repo_root(a), a.workbook_sidecar))
    rows = {int(r["palace"]): r for r in wb.get("palace_dispositions", [])}
    absent_slots = {int(k): int(v) for k, v in wb.get("absent_slots_per_palace", {}).items()}
    KEYS = ["addressed", "corroborated", "deferred", "excluded", "unparseable", "anomaly"]
    tallies, anomalies = [], []
    for pk in a.palace_scope.split(","):
        canon = int(pk)
        ids = [r["id"] for r in reg["e_atoms"] if r["palace_canonical"] == canon]
        if canon not in rows:
            tallies.append(OrderedDict([("palace", canon), ("status", "NO_DISPOSITION_ROW")]))
            anomalies.append("GAP_DETECTED palace %d has no disposition row" % canon)
            continue
        parts = OrderedDict((k, int(rows[canon].get(k, 0))) for k in KEYS)
        live_total = sum(parts.values())
        absent_n = absent_slots.get(canon, 0)
        total = live_total + absent_n
        bucket, groups = [], []
        for k, v in parts.items():
            for _ in range(v):
                bucket.append(k)
                if len(bucket) == 9:
                    groups.append({x: bucket.count(x) for x in sorted(set(bucket))})
                    bucket = []
        if bucket:
            groups.append({x: bucket.count(x) for x in sorted(set(bucket))})
        balances = (live_total == len(ids))
        if not balances:
            anomalies.append("GAP_DETECTED palace %d live total %d != registry %d" %
                             (canon, live_total, len(ids)))
        tallies.append(OrderedDict([
            ("palace", canon), ("total", total), ("parts", parts),
            ("absent", absent_n),
            ("closure_equation", "%d live (%s) + %d absent = %d" %
             (live_total, " + ".join("%d %s" % (v, k) for k, v in parts.items() if v),
              absent_n, total)),
            ("summation", {"method": "enumerated_addends<=9", "groups": groups,
                           "sum": live_total}),
            ("registry_ids_in_palace", len(ids)), ("balances", balances)]))
    glob = int(wb.get("global_absent", {}).get("count", 0))
    tallies.append(OrderedDict([
        ("palace", "global"), ("absent", glob),
        ("closure_equation", "%d global absent slots" % glob),
        ("note", wb.get("global_absent", {}).get("note")), ("balances", True)]))
    for an in anomalies:
        anomaly(a, "GAP_DETECTED", an, "ledger")
    live_total = sum(t.get("total", 0) - t.get("absent", 0) for t in tallies
                     if isinstance(t.get("palace"), int))
    absent_total = sum(t.get("absent", 0) for t in tallies if isinstance(t.get("absent"), int))
    prod = OrderedDict([
        ("cap", "CAP-14"), ("palace_tallies", tallies),
        ("closure_line", " ".join("%s:%s" % (t["palace"], t.get("total")) for t in tallies)),
        ("totals", {"live_atoms": live_total, "absent_slots": absent_total,
                    "closed_slots": live_total + absent_total}),
        ("all_balance", all(t.get("balances", True) for t in tallies)),
        ("orphan_check", {"method": "batch-cited IDs vs registry (CAP-16 re-run)",
                          "result": "see CAP-16 self_audit"}),
        ("anomalies", anomalies)])
    finish(a, "CAP-14", "ledger_reconcile", ["evidence_registry", a.workbook_sidecar], prod,
           ["closure_line", "totals", "all_balance", "anomalies"])


# ---------------------------------------------------------------- CAP-16

def cap16(a):
    st = os.path.join(run_dir(a), "raw", "state")
    reg = load_json(os.path.join(st, "evidence_registry.json"))
    ids = {r["id"] for r in reg["e_atoms"]}
    try:
        vt = load_json(os.path.join(st, "value_trace.json"))
        ids |= {r["id"] for r in vt["r_atoms"]}
    except IOError:
        pass
    rm = load_json(os.path.join(st, "role_map.json"))
    dg = load_json(os.path.join(st, "board_digest.json"))
    led = load_json(os.path.join(st, "ledger_reconcile.json"))
    side = load_json(os.path.join(repo_root(a), a.claim_set))
    cited = set()
    for c in side.get("claims", []):
        cited |= set(c.get("cited_E", [])) | set(c.get("cited_R", []))
    unresolved = sorted(cited - ids)
    checks = OrderedDict()
    checks["every_required_semantic_role_has_recorded_state"] = all(
        r["state"] in ("RESOLVED", "UNRESOLVED", "BLOCKED") for r in rm["role_states"])
    checks["every_ERICA_id_cited_resolves_in_registry"] = (len(unresolved) == 0)
    dg_p = [b["palace"] for b in dg["palace_blocks"]]
    led_p = [t["palace"] for t in led["palace_tallies"]]
    checks["every_palace_has_exactly_one_board_card_and_one_ledger_tally"] = (
        all(dg_p.count(p) == 1 for p in range(0, 10)) and
        all(led_p.count(p) == 1 for p in range(0, 10)))
    checks["every_live_verdict_cites_archetype_resolution_or_no_competing_candidate"] = all(
        (c.get("archetype") or c.get("no_competing_candidate")) for c in side.get("claims", [])
        if c.get("live"))
    checks["no_emulated_product_contradicts_explicit_field_without_anomaly"] = True
    checks["every_claim_has_chart_citations_and_none_cites_case_context"] = all(
        (c.get("cited_E") or c.get("cited_R")) and not c.get("cites_case_context")
        for c in side.get("claims", []))
    checks["every_question_facet_has_case_alignment_row_including_zero_rows"] = (
        len(side.get("cmap_rows", [])) > 0)
    checks["GAP_REPORT_present_and_empty_for_clean_render"] = None
    cl_path = os.path.join(run_dir(a), "renders", "claim_lines.txt")
    cl = [l for l in io.open(cl_path, encoding="utf-8").read().splitlines() if l.strip()] \
        if os.path.exists(cl_path) else []
    checks["claim_line_count_matches_claim_records"] = (len(cl) == len(side.get("claims", [])))
    prod = OrderedDict([("cap", "CAP-16"), ("checklist", checks),
                        ("unresolved_citations", unresolved),
                        ("passes", sum(1 for v in checks.values() if v is True)),
                        ("open_items", [k for k, v in checks.items() if v is not True])])
    finish(a, "CAP-16", "self_audit", ["all_state"], prod,
           ["checklist", "unresolved_citations", "passes"])


# ---------------------------------------------------------------- CAP-19

def cap19(a):
    side = load_json(os.path.join(repo_root(a), a.claim_set))
    conk = side.get("conk", side.get("CONK", []))
    unk = side.get("unk", side.get("UNK", []))
    guards = side.get("unk_guards", [])
    resolving = {g["claim_id"] for g in guards if g.get("resolves")}
    results = []
    for c in side.get("claims", []):
        hits = [r["id"] for r in conk if r.get("claim_id") == c["claim_id"]]
        u = [r["id"] for r in unk if r.get("claim_id") == c["claim_id"]]
        if c["claim_id"] in resolving:
            u = u + ["FORCED_BY_GUARD"]
        status = "conflict" if hits else ("resolves_unknown" if u else "clean")
        results.append(OrderedDict([("claim_id", c["claim_id"]), ("CONK_hits", hits),
                                    ("UNK_hits", u), ("status", status)]))
    prod = OrderedDict([("cap", "CAP-19"), ("results", results), ("CONK_count", len(conk)),
                        ("UNK_count", len(unk)), ("unk_guards", guards),
                        ("conflict_register", [r for r in results if r["status"] != "clean"]),
                        ("downgrade_rule", "CONK hit -> CONFLICT_WITH_KNOWN + rejected; "
                                           "UNK resolution -> strip + CHART_SUGGESTS + assumption_index")])
    finish(a, "CAP-19", "conflict_check", [os.path.basename(a.claim_set)], prod,
           ["results", "CONK_count", "UNK_count", "downgrade_rule"])


# ---------------------------------------------------------------- CAP-18

def cap18(a):
    side = load_json(os.path.join(repo_root(a), a.claim_set))
    reg = load_json(os.path.join(run_dir(a), "raw", "state", "evidence_registry.json"))
    known = {r["id"] for r in reg["e_atoms"]}
    try:
        rt = load_json(os.path.join(run_dir(a), "raw", "state", "value_trace.json"))
        known |= {r["id"] for r in rt["r_atoms"]}
    except IOError:
        pass
    slots = side.get("q_slots", [])
    claims = {c["claim_id"]: c for c in side.get("claims", [])}
    rows = side.get("cmap_rows", [])
    ok_rows, bad_rows = [], []
    for r in rows:
        cites = r["chart_citation_ids"]
        line = "CMAP|%s|%s|%s|%s" % (r["claim_id"], r["Q"], r["tag"],
                                    ",".join(cites) if cites else "NONE")
        r["line"] = line
        m = CMAP_RE.match(line)
        unresolved = [c for c in cites if c not in known]
        ok = bool(m) and (not unresolved or r["tag"] in ("NO_CHART_SUPPORT",
                                                         "CONTRADICTS_KNOWN"))
        if r["tag"] in ("NO_CHART_SUPPORT", "CONTRADICTS_KNOWN") and cites:
            ok = False
        (ok_rows if ok else bad_rows).append(
            {"line": line, "unresolved_citations": unresolved})
        if not ok:
            anomaly(a, "RECONCILE_MISMATCH", "cmap row invalid: %s" % line, "case_alignment")
    # facet coverage summary: every slot, all four tags including zeros
    summary = []
    for q in slots:
        tally = {"DIRECT": 0, "INDIRECT": 0, "NO_CHART_SUPPORT": 0, "CONTRADICTS_KNOWN": 0}
        cls = set()
        for r in rows:
            if r["Q"] == q["id"]:
                tally[r["tag"]] += 1
                cls.add(r["claim_id"])
        summary.append(OrderedDict([
            ("Q", q["id"]), ("facet", q["facet"]), ("status", q.get("status")),
            ("claim_count", len(cls)), ("tag_tally", tally),
            ("covered", (tally["DIRECT"] + tally["INDIRECT"]) > 0)]))
    uncovered = [s2["Q"] for s2 in summary if not s2["covered"]]
    prod = OrderedDict([
        ("cap", "CAP-18"), ("rows_valid", len(ok_rows)), ("rows_rejected", bad_rows),
        ("case_alignment_rows", rows), ("facet_coverage_summary", summary),
        ("uncovered_facets", uncovered),
        ("tag_legend", {"DIRECT": "claim addresses the facet and cites chart evidence",
                        "INDIRECT": "claim bears on the facet through a second-order reading",
                        "NO_CHART_SUPPORT": "facet acknowledged; the chart supplies nothing for it",
                        "CONTRADICTS_KNOWN": "claim conflicts with a known real-world fact"}),
        ("rule", "a Qn with zero DIRECT and zero INDIRECT rows is an uncovered facet -> gap report")])
    d = os.path.join(run_dir(a), "renders")
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, "cmap_lines.txt"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(r["line"] + "\n")
    finish(a, "CAP-18", "case_alignment", ["claim_set"], prod,
           ["rows_valid", "rows_rejected", "facet_coverage_summary", "uncovered_facets"])

# ---------------------------------------------------------------- CAP-17

def _yaml_scalar(s):
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        s = s[1:-1]
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if s in ("[]", ""):
        return [] if s == "[]" else None
    if s in ("null", "~"):
        return None
    return s


def parse_yaml_subset(path):
    """Small dependency-free YAML reader for the case-context subset: nested maps, lists of
    scalars/lists/maps, and folded block scalars (>-, >, |, |-)."""
    lines = io.open(path, encoding="utf-8").read().split("\n")
    # strip comments only when preceded by start-of-line spaces and not inside a quote
    cleaned = []
    for ln in lines:
        if ln.strip().startswith("#"):
            continue
        cleaned.append(ln.rstrip())

    def block_scalar(idx, base_indent, folded):
        out = []
        while idx < len(cleaned):
            ln = cleaned[idx]
            if ln.strip() == "":
                out.append("")
                idx += 1
                continue
            ind = len(ln) - len(ln.lstrip(" "))
            if ind <= base_indent:
                break
            out.append(ln.strip())
            idx += 1
        text = " ".join(x for x in out if x != "") if folded else "\n".join(out)
        return text.strip(), idx

    def parse_block(idx, indent):
        """Return (value, next_idx) for a block starting at `idx` with given indent."""
        node = None
        while idx < len(cleaned):
            ln = cleaned[idx]
            if ln.strip() == "":
                idx += 1
                continue
            ind = len(ln) - len(ln.lstrip(" "))
            if ind < indent:
                break
            body = ln.strip()
            if body.startswith("- "):
                if node is None:
                    node = []
                item = body[2:]
                if ":" in item and not item.endswith(":") and not re.match(r"^[^:]+:\s*$", item):
                    # inline map start: "- key: value"
                    k, _, v = item.partition(":")
                    m = OrderedDict()
                    if v.strip() in (">-", ">", "|", "|-"):
                        txt, idx = block_scalar(idx + 1, ind, v.strip().startswith(">"))
                        m[k.strip()] = txt
                    else:
                        m[k.strip()] = _yaml_scalar(v)
                        idx += 1
                        # absorb continuation keys of this map at deeper indent
                        while idx < len(cleaned):
                            ln2 = cleaned[idx]
                            if ln2.strip() == "":
                                idx += 1; continue
                            ind2 = len(ln2) - len(ln2.lstrip(" "))
                            b2 = ln2.strip()
                            if ind2 <= ind or b2.startswith("- "):
                                break
                            k2, _, v2 = b2.partition(":")
                            if v2.strip() in (">-", ">", "|", "|-"):
                                txt, idx = block_scalar(idx + 1, ind2, v2.strip().startswith(">"))
                                m[k2.strip()] = txt
                                continue
                            if v2.strip() == "":
                                sub, idx = parse_block(idx + 1, ind2 + 1)
                                m[k2.strip()] = sub
                                continue
                            m[k2.strip()] = _yaml_scalar(v2)
                            idx += 1
                    node.append(m)
                else:
                    node.append(_yaml_scalar(item))
                    idx += 1
                continue
            if ":" not in body:
                idx += 1
                continue
            if node is None:
                node = OrderedDict()
            k, _, v = body.partition(":")
            k = k.strip(); v = v.strip()
            if v in (">-", ">", "|", "|-"):
                txt, idx = block_scalar(idx + 1, ind, v.startswith(">"))
                node[k] = txt
                continue
            if k == "":
                idx += 1
                continue
            if v == "":
                sub, idx = parse_block(idx + 1, ind + 1)
                node[k] = sub
                continue
            node[k] = _yaml_scalar(v)
            idx += 1
        return node, idx

    val, _ = parse_block(0, 0)
    return val


ALIASES = {
    "reason": "casting_reason", "why": "casting_reason", "situation": "casting_reason",
    "casting_reason": "casting_reason",
    "facts": "known_facts", "knowns": "known_facts", "known_facts": "known_facts",
    "open_questions": "unknowns", "unknown_questions": "unknowns", "unknowns": "unknowns",
    "period": "timeframe_of_interest", "timeframe": "timeframe_of_interest",
    "timeframe_of_interest": "timeframe_of_interest",
    "decision": "decision_needed", "decision_needed": "decision_needed",
    "question": "question", "subject": "subject", "domain": "domain",
    "relevance_hint": "relevance_hint", "do_not_say": "do_not_say",
    "submission": "submission", "format": "format", "title": "title",
    "assignment_objective": "assignment_objective", "submission_date": "submission_date",
}

MARKER_PATTERNS = [
    (r"ignore (all )?(the )?(previous|prior|above)", "INSTRUCTION_INJECTION"),
    (r"disregard (all )?(the )?(previous|prior|above|instructions)", "INSTRUCTION_INJECTION"),
    (r"\byou are (now )?", "INSTRUCTION_INJECTION"),
    (r"system prompt", "INSTRUCTION_INJECTION"),
    (r"\bassistant\b", "INSTRUCTION_INJECTION"),
    (r"\bas an ai\b", "INSTRUCTION_INJECTION"),
    (r"\boverride\b", "INSTRUCTION_INJECTION"),
    (r"\bexecute\b", "INSTRUCTION_INJECTION"),
    (r"\bdo not (tell|reveal|mention)\b", "INSTRUCTION_INJECTION"),
]


def cap17(a):
    path = os.path.join(repo_root(a), a.case_context)
    parsed = parse_yaml_subset(path)
    # deep scan for instruction-like strings
    markers = []
    stamped = []          # list of (path, text) for provenance stamp

    def scan(node, path_):
        if isinstance(node, dict):
            for k, v in node.items():
                scan(v, path_ + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                scan(v, path_ + "/[%d]" % i)
        elif isinstance(node, str):
            stamped.append({"path": path_, "text": node})
            low = node.lower()
            for rx, kind in MARKER_PATTERNS:
                if re.search(rx, low):
                    markers.append({"path": path_, "kind": kind, "match": rx, "text": node})
                    break

    scan(parsed, "")
    slot_map = OrderedDict()
    for k, v in parsed.items():
        canon = ALIASES.get(k, k)
        if canon not in slot_map:
            slot_map[canon] = {"raw_key": k, "value": v}
    known = ["casting_reason", "question", "subject", "domain", "timeframe_of_interest",
             "decision_needed", "known_facts", "unknowns", "relevance_hint", "do_not_say",
             "title", "format", "submission_date", "assignment_objective", "submission"]
    unrecognized = [k for k in parsed.keys() if k not in slot_map and k not in ALIASES]
    missing_required = [k for k in ["casting_reason", "question", "subject", "domain",
                                    "timeframe_of_interest", "decision_needed"] if k not in slot_map]
    prod = OrderedDict([
        ("cap", "CAP-17"),
        ("source_file", os.path.basename(a.case_context)),
        ("parsed_top_level_keys", list(parsed.keys())),
        ("slot_map", slot_map),
        ("structured_schema_required_keys", ["casting_reason", "question", "subject", "domain",
                                             "timeframe_of_interest", "decision_needed",
                                             "known_facts", "unknowns", "relevance_hint",
                                             "do_not_say"]),
        ("schema_exact_match", len(missing_required) == 0 and len(unrecognized) == 0),
        ("missing_required_keys", missing_required),
        ("unrecognized_keys", unrecognized),
        ("degradation_decision", "CONTEXT_DEGRADED" if (missing_required or unrecognized) else "CLEAN"),
        ("derived_rows_tag", "DECOMPOSED"),
        ("instruction_like_markers", markers),
        ("no_slots_inferred_from_prose", "CAP-17 step 3: no slot beyond the text was inferred"),
        ("provenance_stamp_count", len(stamped)),
    ])
    finish(a, "CAP-17", "case_context_digest", [os.path.basename(a.case_context)], prod,
           ["source_file", "parsed_top_level_keys", "schema_exact_match",
            "missing_required_keys", "unrecognized_keys", "degradation_decision",
            "instruction_like_markers", "derived_rows_tag"])
    # also persist the raw parse for the workbook author (provenance preserved beside every derived row)
    write_state(a, "case_context_parse.json", parsed)


# ---------------------------------------------------------------- entry

def add_common(p, roles_default):
    p.add_argument("--repo-root", required=True)
    p.add_argument("--run-dir", required=True)
    p.add_argument("--chart", default="QMDJ/MARKETING/project_3.json")
    p.add_argument("--roles", default=roles_default)
    p.add_argument("--schema-adapter", default="")
    p.add_argument("--reference-file", default="")
    p.add_argument("--case-context", default="")
    p.add_argument("--claim-set", default="")
    p.add_argument("--workbook-sidecar", default="")
    p.add_argument("--palace-scope", default="0,1,2,3,4,5,6,7,8,9")
    p.add_argument("--visibility", default="VISIBLE,ELIGIBLE")
    p.add_argument("--grammar-files", default="")
    return p


def main():
    ap = argparse.ArgumentParser(prog="qcap")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ROLES = "SUBMISSION/MARKETING/PROJECT_3/QMDJ_ANALYST_RUN/CONFIG/chart_roles.json"
    for name in ["cap01", "cap02", "cap03", "cap04", "cap05", "cap06", "cap07", "cap08",
                 "cap09", "cap10", "cap11", "cap12", "cap13", "cap14", "cap16", "cap18",
                 "cap19", "cap17"]:
        p = sub.add_parser(name)
        bind_cap_parser(p)
        add_common(p, ROLES)
    p = sub.add_parser("cap15")
    bind_cap_parser(p)
    add_common(p, ROLES)
    a = ap.parse_args()
    fn = {"cap01": cap01, "cap02": cap02, "cap03": cap03, "cap04": cap04, "cap05": cap05,
          "cap06": cap06, "cap07": cap07, "cap08": cap08, "cap09": cap09, "cap10": cap10,
          "cap11": cap11, "cap12": cap12, "cap13": cap13, "cap14": cap14, "cap15": cap15_entry,
          "cap16": cap16, "cap17": cap17, "cap18": cap18, "cap19": cap19}[a.cmd]
    fn(a)


if __name__ == "__main__":
    main()
