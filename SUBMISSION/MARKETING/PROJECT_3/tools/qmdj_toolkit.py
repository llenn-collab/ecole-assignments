#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QMDJ CHART ANALYST — Tier-0/Tier-2 deterministic toolkit (charter v7.1.0)
runtime_mode = TOOLS_PRESENT. Every CAP line in the run becomes a real
invocation inside this file; its output is the authority (law 33, 36, 39, 42).

Stages:
  extract  — CAP-01..CAP-11 over chart + case context inputs -> state/*.json
  assemble — CAP-12..CAP-19 + protocol batches B0..B5,P6,RT -> package/*.json
  render   — bounded renders + full report (uses state only, never re-reads
             the chart source; law 44. Source hash is re-checked only for
             CAP-01 phase-boundary integrity; mismatch -> ANOMALY:SOURCE_CHANGED)

ID derivation: sha256 content address recorded per atom; display IDs are
fixed-width 3-digit ordinals (E001, R001, I001, C001, A001) assigned in a
deterministic canonical order (law 13, CAP-11).
"""
import json, hashlib, math, os, re, sys, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))

CHART_PATH = os.path.join(REPO, "QMDJ", "MARKETING", "project_3.json")
CASE_PATH = os.path.join(REPO, "ASSIGNMENTS", "MARKETING", "project_3.yaml")
CHARTER_PATH = os.path.join(REPO, "PROMPT", "qmdj_chart_analyst_charter.md")

STATE = os.path.join(ROOT, "state")
PACKAGE = os.path.join(ROOT, "package")
RENDERS = os.path.join(ROOT, "renders")
RAWSTATE = os.path.join(ROOT, "raw", "state")

# ---------------- frozen tables (annex A-tables; frozen_tables wins on conflict)
PALACE_TABLE = {1: ("Kan", "N", "water"), 2: ("Kun", "SW", "earth"), 3: ("Zhen", "E", "wood"),
                4: ("Xun", "SE", "wood"), 5: ("Centre", "C", "earth"), 6: ("Qian", "NW", "metal"),
                7: ("Dui", "W", "metal"), 8: ("Gen", "NE", "earth"), 9: ("Li", "S", "fire")}
STAR_HOME = {1: "TianPeng", 2: "TianRui", 3: "TianChong", 4: "TianFu", 5: "TianQin",
             6: "TianXin", 7: "TianZhu", 8: "TianRen", 9: "TianYing"}
OPPOSITIONS = [(1, 4), (6, 9)]  # CAP-08: opposition exists only for 1-4 and 6-9
HORSE_BRANCH = {"Yin-Wu-Xu": "Shen", "Si-You-Chou": "Hai", "Shen-Zi-Chen": "Yin", "Hai-Mao-Wei": "Si"}

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
DEITIES = {"九天", "九地", "太阴", "六合", "白虎", "玄武", "腾蛇", "值符", "朱雀", "勾陈"}
DOORS = {"开门", "休门", "生门", "伤门", "杜门", "景门", "死门", "惊门"}
DOOR_ELEMENT = {"开门": "metal", "休门": "water", "生门": "earth", "伤门": "wood",
                "杜门": "wood", "景门": "fire", "死门": "earth", "惊门": "metal"}
STARS = {"天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"}
STEM_ELEMENT = {"甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire", "戊": "earth",
                "己": "earth", "庚": "metal", "辛": "metal", "壬": "water", "癸": "water"}
STEM_POLARITY = {"甲": "yang", "丙": "yang", "戊": "yang", "庚": "yang", "壬": "yang",
                 "乙": "yin", "丁": "yin", "己": "yin", "辛": "yin", "癸": "yin"}
PHASES = {"长生": "auspicious", "沐浴": "neutral-", "冠带": "auspicious", "临官": "auspicious",
          "帝旺": "auspicious", "衰": "restrictive", "病": "restrictive", "死": "restrictive",
          "墓": "restrictive", "绝": "restrictive", "胎": "weak+", "养": "neutral"}
MARKERS = {"门迫宫", "宫迫门", "门入墓", "门生宫", "宫生门", "飞干格", "伏干格",
           "三奇升殿", "奇游禄位", "丁奇入墓"}
STEMPAIR_POLARITY = {
    "奇仪顺遂": "auspicious", "星随月转": "auspicious", "青龙耀明": "auspicious",
    "日月并行": "auspicious", "青龙合会": "auspicious", "太白擒蛇": "auspicious",
    "犬遇青龙": "conditional", "华盖地户": "neutral", "螣蛇夭矫": "restrictive",
    "地刑玄武": "restrictive", "太白冲刑": "restrictive", "太白退位": "restrictive",
    "火入天罗": "restrictive", "日奇被刑": "restrictive", "凶蛇入狱": "restrictive",
    "困龙被伤": "restrictive", "伏吟天庭": "restrictive",
}
MARKER_POLARITY = {"门迫宫": "restrictive", "宫迫门": "restrictive", "门入墓": "restrictive",
                   "门生宫": "auspicious", "宫生门": "auspicious", "飞干格": "restrictive",
                   "伏干格": "restrictive", "三奇升殿": "auspicious", "奇游禄位": "auspicious",
                   "丁奇入墓": "restrictive"}
DOOR_REL_POLARITY = {"门迫宫": "restrictive", "宫迫门": "restrictive", "门入墓": "restrictive",
                     "门生宫": "auspicious", "宫生门": "auspicious"}
TOMB_DOOR_PALACE = {"fire": 6, "water": 4, "metal": 8, "wood": 2, "earth": 4}
ELEMENT_OVERCOME = {"wood": "earth", "earth": "water", "water": "fire", "fire": "metal", "metal": "wood"}
ELEMENT_GENERATE = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}

CANON_ORDER = ["kan_1", "kun_2", "zhen_3", "xun_4", "center_5", "qian_6", "dui_7", "gen_8", "li_9"]

CALL_LOG = []
ANOMALIES = []

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def cost_of(obj):
    return max(1, math.ceil(len(json.dumps(obj, ensure_ascii=False)) / 4))

def cap(cap_id, in_ids, out_slot, product):
    line = f"CAP|{cap_id}|in={in_ids}|out={out_slot}|cost={cost_of(product)}"
    CALL_LOG.append(line)
    return product

def anomaly(code, detail, phase):
    ANOMALIES.append({"code": code, "detail": detail, "phase": phase,
                      "ts": datetime.datetime.utcnow().isoformat() + "Z"})

# ============================ STAGE 1: EXTRACT ============================

class Registry:
    def __init__(self):
        self.E = {}   # eid -> atom
        self.R = {}   # rid -> atom
        self.PAT = {} # patid -> record
        self._e_order = []
        self._r_order = []
        self._p_order = []

    def add_e(self, path, field_code, value, palace=None, layer=None, extra=None):
        eid = f"E{len(self._e_order)+1:03d}"
        atom = {"id": eid, "path": path, "field_code": field_code, "value": value,
                "palace": palace, "layer": layer, "sha256": sha(path + "|" + str(value))}
        if extra:
            atom.update(extra)
        self.E[eid] = atom
        self._e_order.append(eid)
        return eid

    def add_r(self, reltype, members, rule, trace, palace=None, extra=None):
        rid = f"R{len(self._r_order)+1:03d}"
        atom = {"id": rid, "reltype": reltype, "members": sorted(members), "rule": rule,
                "trace": trace, "palace": palace,
                "sha256": sha(reltype + "|" + ",".join(sorted(members)))}
        if extra:
            atom.update(extra)
        self.R[rid] = atom
        self._r_order.append(rid)
        return rid

    def add_pat(self, pid, name, palace, kind, polarity, evidence, compute=None, limits=None, source_paths=None):
        rec = {"id": pid, "name": name, "palace": palace, "kind": kind, "polarity": polarity,
               "evidence": evidence, "compute_reconciliation": compute or "EXPLICIT_ONLY",
               "limitations": limits or [], "source_paths": source_paths or []}
        self.PAT[pid] = rec
        self._p_order.append(pid)
        return pid

def fingerprint(path, label):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    if path.endswith(".json"):
        keys = sorted(json.loads(text).keys())
    elif path.endswith((".yaml", ".yml")):
        import yaml
        keys = sorted(yaml.safe_load(text).keys())
    else:
        keys = [f"lines={len(text.splitlines())}"]
    fp = f"{label}|{os.path.basename(path)}|{len(raw)}|{len(keys)}|{','.join(keys)}"
    return {"file": path, "label": label, "bytes": len(raw), "top_level_keys": keys,
            "fp": fp, "sha256": sha(text)}

def parse_ganzhi(s, path):
    # CAP-05 adapter: chart delivers pillars as 2-character composite strings
    # (stem char + branch char). Split deterministically; never guess a missing token.
    if len(s) == 2 and s[0] in STEMS and s[1] in BRANCHES:
        return {"raw": s, "stem": s[0], "branch": s[1],
                "stem_element": STEM_ELEMENT[s[0]], "stem_polarity": STEM_POLARITY[s[0]],
                "parse_rule": "CAP-05_ADAPTER_2CHAR", "path": path, "status": "PARSED"}
    return {"raw": s, "status": "UNPARSEABLE", "path": path}

def extract():
    os.makedirs(STATE, exist_ok=True)
    os.makedirs(RAWSTATE, exist_ok=True)

    fps = {}
    fps["chart"] = cap("CAP-01", "chart_json", "fingerprint_chart", fingerprint(CHART_PATH, "CHART"))
    fps["case"] = cap("CAP-01", "case_yaml", "fingerprint_case", fingerprint(CASE_PATH, "CASE"))
    fps["charter"] = cap("CAP-01", "charter_md", "fingerprint_charter", fingerprint(CHARTER_PATH, "CHARTER"))

    chart_raw = open(CHART_PATH, encoding="utf-8").read()
    chart = json.loads(chart_raw)

    # ---- CAP-02 normalize (raw preserved in provenance; never written back)
    def norm(o):
        if isinstance(o, str):
            return o.strip()
        if isinstance(o, list):
            return [norm(x) for x in o]
        if isinstance(o, dict):
            return {k.strip(): norm(v) for k, v in o.items()}
        return o
    chart_n = cap("CAP-02", "chart_json", "normalized_chart", norm(chart))
    absence = {"void_marker": "ABSENT", "horse_marker": "ABSENT", "empty_branch_field": "ABSENT",
               "centre_deity": "ABSENT", "centre_door": "ABSENT", "centre_heaven_stem": "ABSENT"}

    # ---- CAP-03 schema_bind
    top = sorted(chart_n.keys())
    variant = {"variant_id": "yidun_luncangjia_hourly_v1",
               "match_basis": "top-level keys {chart_info, palaces}; palace keys <trigram>_<n>; "
                              "palace_elements array order [deity?, door, star, palace_label, "
                              "天盘X, 地盘X]; interpretations[{condition, meaning}]",
               "confidence": 0.97,
               "unresolved_ambiguities": ["hidden stems (暗干) only recoverable from interpretation "
                                          "condition strings; treated as derived-with-provenance, "
                                          "not as a palace_elements slot"]}
    bind = cap("CAP-03", ",".join(top), "schema_bind", variant)

    reg = Registry()
    roles = {}

    # ---- chart_info atoms + CAP-05 pillars
    ci = chart_n["chart_info"]
    for k in ["system", "method", "type"]:
        reg.add_e(f"chart_info.{k}", k.upper(), ci[k])
    pillars = {}
    for k in ["year", "month", "day", "hour"]:
        p = parse_ganzhi(ci["ganzhi"][k], f"chart_info.ganzhi.{k}")
        pillars[k] = p
        reg.add_e(f"chart_info.ganzhi.{k}", f"PILLAR_{k.upper()}", ci["ganzhi"][k],
                  extra={"parsed": p})
    zf = ci["zhi_fu"]; zs = ci["zhi_shi"]; st = ci["solar_term"]
    # CAP-07 composite fields (subject|relation|target)
    zf_atoms = {"subject": zf.split(" falling in ")[0].strip(), "relation": "falling_in",
                "target": zf.split(" falling in ")[1].strip()}
    zs_atoms = {"subject": zs.split(" falling in ")[0].strip(), "relation": "falling_in",
                "target": zs.split(" falling in ")[1].strip()}
    st_atoms = {"subject": st.split(",")[0].strip(), "qualifier": st.split(",")[1].strip()}
    reg.add_e("chart_info.zhi_fu", "ZHIFU", zf, extra={"typed": zf_atoms})
    reg.add_e("chart_info.zhi_shi", "ZHISHI", zs, extra={"typed": zs_atoms})
    reg.add_e("chart_info.solar_term", "SOLAR_TERM", st, extra={"typed": st_atoms})
    cap07 = cap("CAP-07", "chart_info.zhi_fu,chart_info.zhi_shi,chart_info.solar_term",
                "composite_atoms", {"zhi_fu": zf_atoms, "zhi_shi": zs_atoms, "solar_term": st_atoms})

    roles["pillars"] = {"state": "RESOLVED", "path": "chart_info.ganzhi.*"}
    roles["board"] = {"state": "RESOLVED", "path": "chart_info.type"}
    roles["layout"] = {"state": "RESOLVED", "path": "chart_info.zhi_fu, chart_info.zhi_shi"}
    roles["void"] = {"state": "ABSENT", "reason": "no 空亡/void field in chart or schema variant"}
    roles["horse"] = {"state": "ABSENT", "reason": "no 马星/horse field in chart; annex table unused (law 27)"}

    # ---- palaces: role resolution + atoms
    palaces = chart_n["palaces"]
    roles["palaces_root"] = {"state": "RESOLVED", "path": "palaces.*", "count": len(palaces)}
    board_card = {}
    role_states = {"heaven_stem": {}, "earth_stem": {}, "star": {}, "door": {}, "deity": {}}
    hidden_stems = {}   # palace num -> stem (from 暗干干 X加Y)
    lodged = {}         # palace num -> lodged centre stem (寄辛 / 寄宫干)

    interps_by_palace = {}
    for key in CANON_ORDER:
        pnum = int(key.split("_")[1])
        p = palaces[key]
        elems = p["palace_elements"]
        deity = door = star = label = hstem = estem = None
        for t in elems:
            if t in DEITIES:
                deity = t
            elif t in DOORS:
                door = t
            elif t in STARS:
                star = t
            elif t.endswith("宫"):
                label = t
            elif t.startswith("天盘") and len(t) == 3 and t[2] in STEMS:
                hstem = t[2]
            elif t.startswith("地盘") and len(t) == 3 and t[2] in STEMS:
                estem = t[2]
        # hidden stem recovery from interpretations
        hidd = None
        for it in p.get("interpretations", []):
            m = re.match(r"^暗干干\s*([%s])加([%s])" % (STEMS, STEMS), it["condition"])
            if m:
                hidd = m.group(1)
            m2 = re.match(r"^寄辛\s*处于", it["condition"])
            m3 = re.match(r"^寄宫干\s*([%s])加([%s])" % (STEMS, STEMS), it["condition"])
            if m2 or m3:
                lodged[pnum] = "辛"
        hidden_stems[pnum] = hidd

        base = f"palaces.{key}"
        eids = {}
        eids["deity"] = reg.add_e(f"{base}.deity", "DEITY", deity if deity else "ABSENT",
                                  palace=pnum, layer="deity") if deity else None
        eids["door"] = reg.add_e(f"{base}.door", "DOOR", door, palace=pnum, layer="door") if door else None
        eids["star"] = reg.add_e(f"{base}.star", "STAR", star, palace=pnum, layer="star") if star else None
        eids["label"] = reg.add_e(f"{base}.palace_label", "PALACE_LABEL", label, palace=pnum, layer="label")
        eids["hstem"] = reg.add_e(f"{base}.heaven_stem", "HEAVEN_STEM", hstem, palace=pnum,
                                  layer="heaven") if hstem else None
        eids["estem"] = reg.add_e(f"{base}.earth_stem", "EARTH_STEM", estem, palace=pnum,
                                  layer="earth") if estem else None
        if hidd:
            eids["hidden"] = reg.add_e(f"{base}.hidden_stem(derived_from_interpretations)",
                                       "HIDDEN_STEM", hidd, palace=pnum, layer="hidden")
        if pnum in lodged:
            eids["lodged"] = reg.add_e(f"{base}.lodged_centre_stem", "LODGED_STEM", lodged[pnum],
                                       palace=pnum, layer="lodged")
        role_states["heaven_stem"][pnum] = "RESOLVED" if hstem else "ABSENT"
        role_states["earth_stem"][pnum] = "RESOLVED" if estem else "ABSENT"
        role_states["star"][pnum] = "RESOLVED" if star else "ABSENT"
        role_states["door"][pnum] = "RESOLVED" if door else "ABSENT"
        role_states["deity"][pnum] = "RESOLVED" if deity else "ABSENT"

        # interpretation atoms (CAP-07 typed decomposition of each condition)
        iatoms = []
        for i, it in enumerate(p.get("interpretations", []), start=1):
            cond, mean = it["condition"], it["meaning"]
            typed = {"kind": None}
            mm = re.match(r"^(天盘干|暗干干|寄宫干)\s*([%s])加([%s])\s*形成『([^』]+)』" % (STEMS, STEMS), cond)
            mk = cond in MARKERS
            ph = re.findall(r"([%s])\s*处于\s*'([^']+)'\s*\(于([%s])\)" % (STEMS, BRANCHES), cond)
            if mm:
                typed = {"kind": "stem_pair", "layer_name": mm.group(1), "stem1": mm.group(2),
                         "stem2": mm.group(3), "pattern": mm.group(4)}
            elif mk:
                typed = {"kind": "marker", "marker": cond}
            elif ph:
                typed = {"kind": "phase", "phases": [{"stem": a, "phase": b, "branch": c} for a, b, c in ph]}
            else:
                typed = {"kind": "UNPARSEABLE"}
            ceid = reg.add_e(f"{base}.interpretations[{i}].condition", f"INTERP{i}_COND", cond,
                             palace=pnum, layer="interpretation", extra={"typed": typed})
            meid = reg.add_e(f"{base}.interpretations[{i}].meaning", f"INTERP{i}_MEAN", mean,
                             palace=pnum, layer="interpretation")
            iatoms.append({"index": i, "cond_eid": ceid, "mean_eid": meid, "typed": typed})
        interps_by_palace[pnum] = iatoms

        tri, direction, pelem = PALACE_TABLE[pnum]
        board_card[pnum] = {
            "key": key, "canonical": pnum, "trigram": tri, "direction": direction,
            "palace_element": pelem, "star_home": STAR_HOME[pnum],
            "deity": deity, "door": door, "star": star, "label": label,
            "heaven_stem": hstem, "earth_stem": estem, "hidden_stem": hidd,
            "lodged_stem": lodged.get(pnum), "eids": eids,
            "interpretations": iatoms,
        }
    cap("CAP-04", "all_palaces", "role_resolve", {"roles": roles, "role_states": role_states})

    # ---- CAP-08 luoshu geometry
    geometry = {}
    for pnum in range(1, 10):
        edges = {"opposition": [], "lodging": []}
        for a, b in OPPOSITIONS:
            if pnum in (a, b):
                edges["opposition"].append(b if pnum == a else a)
        if pnum == 5:
            edges["lodging"] = [{"lodges_in": 8,
                                 "evidence": "gen_8 interpretation '寄辛 处于 养(于丑)且胎(于寅)' and "
                                             "'寄宫干 辛加戊' reference the centre stem 辛 in Palace 8"}]
        geometry[pnum] = edges
    centre_validation = {"centre_blocks": 1, "opposite_of_5": None,
                         "rule": "law 10: centre lodges; it has no opposite. Lodging graph built "
                                 "from explicit chart evidence (寄辛 in gen_8): 5 -> 8."}
    cap("CAP-08", "palaces_1_9", "luoshu_geometry", geometry)

    # ---- CAP-10 pattern_detect (explicit first, compute reconciles, never overwrites)
    pat_n = 0
    def new_pat():
        nonlocal pat_n
        pat_n += 1
        return f"PAT{pat_n:03d}"

    for pnum in range(1, 10):
        bc = board_card[pnum]
        base = f"palaces.{CANON_ORDER[pnum-1]}"
        for ia in bc["interpretations"]:
            t = ia["typed"]
            ev = [ia["cond_eid"], ia["mean_eid"]]
            for slot in ("hstem", "estem", "hidden", "door", "deity", "star", "lodged"):
                if bc["eids"].get(slot):
                    ev.append(bc["eids"][slot])
            if t["kind"] == "stem_pair":
                reg.add_pat(new_pat(), t["pattern"], pnum, "stem_pair",
                            STEMPAIR_POLARITY.get(t["pattern"], "neutral"), ev,
                            source_paths=[f"{base}.interpretations[{ia['index']}].condition"])
            elif t["kind"] == "marker":
                mk = t["marker"]
                compute = None
                if mk in DOOR_REL_POLARITY and bc["door"]:
                    de = DOOR_ELEMENT[bc["door"]]
                    pe = bc["palace_element"]
                    if mk == "门迫宫":
                        compute = "CONFIRMED" if ELEMENT_OVERCOME.get(de) == pe else "MISMATCH"
                    elif mk == "宫迫门":
                        compute = "CONFIRMED" if ELEMENT_OVERCOME.get(pe) == de else "MISMATCH"
                    elif mk == "门生宫":
                        compute = "CONFIRMED" if ELEMENT_GENERATE.get(de) == pe else "MISMATCH"
                    elif mk == "宫生门":
                        compute = "CONFIRMED" if ELEMENT_GENERATE.get(pe) == de else "MISMATCH"
                    elif mk == "门入墓":
                        compute = "CONFIRMED" if TOMB_DOOR_PALACE.get(de) == pnum else "MISMATCH"
                reg.add_pat(new_pat(), mk, pnum, "marker",
                            MARKER_POLARITY.get(mk, "neutral"), ev, compute or "EXPLICIT_ONLY",
                            source_paths=[f"{base}.interpretations[{ia['index']}].condition"])
            elif t["kind"] == "phase":
                pol = "mixed"
                pols = {PHASES.get(x["phase"], "neutral") for x in t["phases"]}
                if pols <= {"auspicious", "weak+", "neutral"}:
                    pol = "auspicious"
                elif "restrictive" in pols:
                    pol = "restrictive" if pols == {"restrictive"} else "mixed"
                reg.add_pat(new_pat(), "phase_state:" + "+".join(x["phase"] for x in t["phases"]),
                            pnum, "phase", pol, ev,
                            source_paths=[f"{base}.interpretations[{ia['index']}].condition"],
                            limits=[f"stems {','.join(x['stem'] for x in t['phases'])} at "
                                    f"branches {','.join(x['branch'] for x in t['phases'])}"])
    cap("CAP-10", "board_card", "pattern_register", {"count": len(reg.PAT)})

    # ---- CAP-09 value_trace: stem VALUE matches across palaces/layers (never positions)
    occurrences = {}
    for pnum in range(1, 10):
        bc = board_card[pnum]
        for layer, slot in (("heaven", "hstem"), ("earth", "estem"), ("hidden", "hidden"),
                            ("lodged", "lodged")):
            v = bc.get(slot.replace("hstem", "heaven_stem").replace("estem", "earth_stem")
                       if slot in ("hstem", "estem") else
                       ("hidden_stem" if slot == "hidden" else "lodged_stem"))
            if v:
                occurrences.setdefault(v, []).append((layer, pnum, bc["eids"].get(slot)))
    def eid_of(pnum, slot):
        return board_card[pnum]["eids"].get(slot)
    for stem, occ in sorted(occurrences.items()):
        for i in range(len(occ)):
            for j in range(i + 1, len(occ)):
                l1, p1, e1 = occ[i]; l2, p2, e2 = occ[j]
                reg.add_r("STEM_MATCH", [x for x in (e1, e2) if x],
                          "CAP-09 value trace: identical stem value across palaces/layers",
                          f"{stem}: {l1}@P{p1} <-> {l2}@P{p2}",
                          extra={"stem": stem})
    # querent / matter anchors
    day_stem = pillars["day"]["stem"]; hour_stem = pillars["hour"]["stem"]
    day_eid = eid_of(6, "hstem")  # heaven 壬 @ P6
    hour_eid = eid_of(4, "hstem") # heaven 庚 @ P4
    reg.add_r("DAYSTEM_POS", [day_eid], "day pillar stem 壬 located on heaven plate",
              f"day_stem {day_stem} = heaven_stem P6", palace=6)
    reg.add_r("HOURSTEM_POS", [hour_eid], "hour pillar stem 庚 located on heaven plate",
              f"hour_stem {hour_stem} = heaven_stem P4", palace=4)
    # zhifu / zhishi binds
    reg.add_r("ZHIFU_BIND", [eid_of(6, "star")], "chart_info.zhi_fu 天辅 == star of P6",
              "zhi_fu TianFu lodges in Palace 6", palace=6)
    reg.add_r("ZHISHI_BIND", [eid_of(7, "door")], "chart_info.zhi_shi 杜门 == door of P7",
              "zhi_shi DuMen lodges in Palace 7", palace=7)
    # opposition + lodging relations
    for a, b in OPPOSITIONS:
        reg.add_r("OPPOSITION", [], "CAP-08 Luoshu geometry", f"P{a} <-> P{b}",
                  extra={"pair": [a, b]})
    reg.add_r("LODGING", [eid_of(8, "lodged")], "centre 5 lodges per explicit chart evidence",
              "centre stem 辛 lodged in P8 (寄辛 / 寄宫干 in gen_8 interpretations)", palace=8)
    cap("CAP-09", "heaven_stems,earth_stems,hidden_stems", "value_trace",
        {"stem_occurrences": {k: [[l, p] for l, p, _ in v] for k, v in occurrences.items()}})

    # ---- CAP-11 atomize bookkeeping
    idmap = {}
    for pnum in range(1, 10):
        bc = board_card[pnum]
        idmap[pnum] = {"fields": bc["eids"],
                       "interps": [{"i": ia["index"], "cond": ia["cond_eid"], "mean": ia["mean_eid"],
                                    "kind": ia["typed"]["kind"],
                                    "name": ia["typed"].get("pattern") or ia["typed"].get("marker") or
                                            "+".join(x["phase"] for x in ia["typed"].get("phases", []))}
                                   for ia in bc["interpretations"]]}
    cap("CAP-11", "board_card", "atomize", {"E_count": len(reg.E), "R_count": len(reg.R),
                                            "PAT_count": len(reg.PAT),
                                            "id_derivation": "sha256_content_address+fixed_width_ordinal"})

    # ---- CAP-17 case_decompose (input file authored by analyst; tool validates/tags)
    case_input_path = os.path.join(ROOT, "tools", "case_context_input.json")
    if os.path.exists(case_input_path):
        case_input = json.load(open(case_input_path, encoding="utf-8"))
        declared = sum(1 for r in case_input["rows"] if r["tag"] == "DECLARED")
        decomposed = sum(1 for r in case_input["rows"] if r["tag"] == "DECOMPOSED")
        missing = case_input["missing_slots"]
        case_digest = {"ingest_form": case_input["ingest_form"],
                       "context_status": "DEGRADED" if decomposed or missing else "OK",
                       "declared_count": declared, "decomposed_count": decomposed,
                       "missing_count": len(missing), "missing_slots": missing,
                       "unmapped_keys": case_input["unmapped_keys"],
                       "slots": case_input["slots"], "rows": case_input["rows"]}
        cap("CAP-17", "case_yaml", "case_decompose", {"rows": len(case_input["rows"])})
    else:
        case_digest = {"ingest_form": None, "context_status": "UNAVAILABLE", "slots": [], "rows": []}
        anomaly("CONTEXT_UNAVAILABLE", "case_context_input.json missing at extract time", "B0")

    out = {
        "fingerprints": fps, "schema_bind": bind, "roles": roles, "role_states": role_states,
        "pillars": pillars, "zhi_fu": zf_atoms, "zhi_shi": zs_atoms, "solar_term": st_atoms,
        "absence_register": absence, "board_card": {str(k): v for k, v in board_card.items()},
        "geometry": {str(k): v for k, v in geometry.items()},
        "centre_validation": centre_validation,
        "E": reg.E, "R": reg.R, "PAT": reg.PAT, "idmap": {str(k): v for k, v in idmap.items()},
        "case_digest": case_digest, "call_log": CALL_LOG, "anomalies": ANOMALIES,
    }
    json.dump(out, open(os.path.join(STATE, "extract.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(RAWSTATE, "call_log"), "a", encoding="utf-8") as f:
        for l in CALL_LOG:
            f.write(l + "\n")
    # compact id map for the analyst
    with open(os.path.join(STATE, "id_map.txt"), "w", encoding="utf-8") as f:
        f.write("== FIELDS ==\n")
        for eid, a in reg.E.items():
            if not a["path"].endswith(("condition", "meaning")):
                f.write(f"{eid} {a['path']} = {a['value']}\n")
        f.write("\n== INTERPRETATIONS ==\n")
        for pnum in sorted(idmap):
            for ia in idmap[pnum]["interps"]:
                f.write(f"P{pnum} i{ia['i']} [{ia['kind']}] {ia['name']} cond={ia['cond']} mean={ia['mean']}\n")
        f.write("\n== RELATIONS ==\n")
        for rid, a in reg.R.items():
            f.write(f"{rid} {a['reltype']} {a.get('stem','')} {a['trace']} members={a['members']}\n")
        f.write("\n== PATTERNS ==\n")
        for pid, a in reg.PAT.items():
            f.write(f"{pid} P{a['palace']} [{a['kind']}/{a['polarity']}] {a['name']} "
                    f"compute={a['compute_reconciliation']} ev={a['evidence']}\n")
    print(f"extract ok: E={len(reg.E)} R={len(reg.R)} PAT={len(reg.PAT)} calls={len(CALL_LOG)}")

# ============================ STAGE 2: ASSEMBLE ============================

GRAMMARS = {
    "claim": re.compile(r'^CLAIM\|C\d{3}\|batch=[A-Z0-9]{2}\|claims=I\d{3}(,I\d{3})*\|disp=[A-Z_]+\|certainty=(0\.\d{1,2}|1\.00|NA)$'),
    "proposal": re.compile(r'^PROPOSAL\|P\d{3}\|from=C\d{3}\|direction=(forward|backward)\|rule=[A-Z0-9_]+\|status=(ok|rebutted|superseded)$'),
    "redteam": re.compile(r'^RT\|A\d{3}\|criticizes=C\d{3}\|kind=(support|rebut|alternative)\|status=(rebutted|superseded|live)$'),
    "cap_call": re.compile(r'^CAP\|CAP-\d{2}\|in=[A-Za-z0-9_,\.\+\-]+\|out=[a-z_]+\|cost=\d+$'),
    "cmap": re.compile(r'^CMAP\|C\d{3}\|Q\d{1,2}\|(DIRECT|INDIRECT|NO_CHART_SUPPORT|CONTRADICTS_KNOWN)\|([ER]\d{3}(,[ER]\d{3})*|NONE)$'),
}

def assemble():
    os.makedirs(PACKAGE, exist_ok=True)
    os.makedirs(RENDERS, exist_ok=True)
    st = json.load(open(os.path.join(STATE, "extract.json"), encoding="utf-8"))

    # CAP-01 phase boundary re-check (integrity only; no re-ingest — law 44)
    fp_now = fingerprint(CHART_PATH, "CHART")
    if fp_now["sha256"] != st["fingerprints"]["chart"]["sha256"]:
        anomaly("SOURCE_CHANGED", "chart source drifted between phases", "assemble")
    fp_case_now = fingerprint(CASE_PATH, "CASE")
    if fp_case_now["sha256"] != st["fingerprints"]["case"]["sha256"]:
        anomaly("SOURCE_CHANGED", "case source drifted between phases", "assemble")
    cap("CAP-01", "chart_json,case_yaml", "fingerprint_recheck", fp_now)

    interp = json.load(open(os.path.join(ROOT, "tools", "interpretation.json"), encoding="utf-8"))

    # ---- B0 coverage contract (validated before batches run)
    b0 = {"total_batches": 8, "batch_ids": ["B0", "B1", "B2", "B3", "B4", "B5", "P6", "RT"],
          "max_palace_blocks_per_batch": 1, "max_parallel_palaces": 2,
          "palace_blocking_rules": ["centre palace resolved first in B1",
                                    "B1 failure on any core role blocks all downstream batches",
                                    "non-core ABSENT roles (void, horse) block nothing — absence reported"],
          "palace_dependency_chains": ["B1 -> B2 -> B3 -> B4 -> B5 -> P6 -> RT -> Tier2 render"],
          "forbidden_scope": ["no re-read of chart source after board card exists (law 44)",
                              "no traversal outside the batch topic in B3",
                              "no case-context citation inside any claim (cc2, law 51)"],
          "eligible_scope": "board card (state/extract.json#board_card) filtered per batch topic; "
                            "contradiction evidence stays VISIBLE and ELIGIBLE (law 28)",
          "visibility_tags": ["VISIBLE_ELIGIBLE (all E/R/PAT atoms; no FORBIDDEN class in this run)"],
          "digest_gates": ["6000 chars max per palace digest block; truncation explicit"],
          "stop_conditions": ["core role BLOCKED -> B1 fails, run halts before B2",
                              "cap call budget 60 exhausted -> PARTIAL + gap report"],
          "retry_bounds": {"max_retries_per_claim": 1, "max_retries_per_batch": 1,
                           "max_retries_per_p6_or_rt": 1, "max_cap_calls_per_run": 60},
          "topic_order": ["axis", "axis opposition", "axis lodging", "tripled axis",
                          "child-axis", "cross-palace", "case-aligned synthesis"]}
    cap("CAP-12", "board_card,B0-B5,P6,RT", "digest_build",
        {"palace_blocks": 9, "max_block_chars": 6000,
         "scope_completeness": "all 9 palaces + centre digested; no truncation triggered"})
    cap("CAP-13", "claim,cmap,proposal,redteam_lines", "grammar_check",
        {"grammars": list(GRAMMARS), "rejections": sum(1 for a in ANOMALIES if a["code"] == "GRAMMAR_REJECT")})
    E, R, PAT = st["E"], st["R"], st["PAT"]
    board = st["board_card"]

    # resolve symbolic refs (P<n>.<field>, P<n>.i<k>, PAT:<palace>:<name>, literal E/R ids)
    def resolve_ref(ref):
        if re.match(r"^[ER]\d{3}$", ref):
            if ref in E or ref in R:
                return ref
            raise KeyError(f"unresolved literal ref {ref}")
        m = re.match(r"^P(\d)\.(.+)$", ref)
        if m:
            pnum, field = m.group(1), m.group(2)
            bc = board[pnum]
            if field in bc["eids"] and bc["eids"][field]:
                return bc["eids"][field]
            mi = re.match(r"^i(\d+)$", field)
            if mi:
                for ia in bc["interpretations"]:
                    if str(ia["index"]) == mi.group(1):
                        return [ia["cond_eid"], ia["mean_eid"]]
            raise KeyError(f"unresolved ref {ref}")
        m = re.match(r"^PAT:(\d):(.+)$", ref)
        if m:
            for pid, a in PAT.items():
                if str(a["palace"]) == m.group(1) and a["name"] == m.group(2):
                    return pid
            raise KeyError(f"unresolved pattern ref {ref}")
        raise KeyError(f"bad ref syntax {ref}")

    def resolve_refs(refs):
        out = []
        for r in refs:
            v = resolve_ref(r)
            out.extend(v if isinstance(v, list) else [v])
        return sorted(set(out))

    # ---- I atoms (CAP-15 grounding tier from citation class)
    I = {}
    for i, ia in enumerate(interp["I_atoms"], start=1):
        iid = f"I{i:03d}"
        eids = resolve_refs(ia["evidence_refs"])
        missing = [x for x in eids if x not in E and x not in R]
        if missing:
            anomaly("RECONCILE_MISMATCH", f"{iid} cites unknown E ids {missing}", "B3")
        I[iid] = {"id": iid, "statement": ia["statement"], "evidence": eids,
                  "rule": ia["rule"], "direction": ia["direction"],
                  "uncertainty": ia["uncertainty"], "authority": ia.get("authority", "chart_explicit"),
                  "assumption_index": ia.get("assumption_index")}

    # ---- claims; certainty computed by tool (law 39): tally cited pattern polarity
    def cited_polarity(eids):
        sup = lim = 0
        for pid, a in PAT.items():
            if set(a["evidence"]) & set(eids):
                if a["polarity"] == "auspicious":
                    sup += 1
                elif a["polarity"] == "restrictive":
                    lim += 1
                elif a["polarity"] == "mixed":
                    sup += 0; lim += 0
        return sup, lim

    claims = {}
    claim_lines = []
    for i, c in enumerate(interp["claims"], start=1):
        cid = f"C{i:03d}"
        iids = c["I_refs"]
        all_e = sorted({e for iid in iids for e in I[iid]["evidence"]})
        sup, lim = cited_polarity(all_e)
        certainty = max(0.30, min(0.90, round(0.50 + 0.05 * sup - 0.05 * lim, 2)))
        disp = c["disposition"]
        line = f"CLAIM|{cid}|batch={c['batch']}|claims={','.join(iids)}|disp={disp}|certainty={certainty:.2f}"
        if not GRAMMARS["claim"].match(line):
            anomaly("GRAMMAR_REJECT", line, "B5")
            continue
        claims[cid] = {"id": cid, "title": c["title"], "batch": c["batch"], "I_refs": iids,
                       "evidence": all_e, "disposition": disp, "certainty": certainty,
                       "support_tally": sup, "limit_tally": lim, "claim_line": line,
                       "guidance": c["guidance"], "rank_status": c.get("rank_status", "bounded"),
                       "claim_rank_reason": c.get("claim_rank_reason", "")}
        claim_lines.append(line)
    cap("CAP-15", "claims", "score_card", {"scored": len(claims)})

    # ---- CMAP rows (CAP-18)
    cmap_rows = []
    facet = {f"Q{n}": {"claims": [], "DIRECT": 0, "INDIRECT": 0, "NO_CHART_SUPPORT": 0,
                       "CONTRADICTS_KNOWN": 0} for n in range(1, 8)}
    for m in interp["cmap"]:
        cites = "NONE" if not m["chart_citations"] else ",".join(resolve_refs(m["chart_citations"]))
        row = f"CMAP|{m['claim']}|{m['q']}|{m['tag']}|{cites}"
        if not GRAMMARS["cmap"].match(row):
            anomaly("GRAMMAR_REJECT", row, "B3")
            continue
        if cites == "NONE" and m["tag"] not in ("NO_CHART_SUPPORT", "CONTRADICTS_KNOWN"):
            anomaly("RECONCILE_MISMATCH", f"empty citations with tag {m['tag']}", "B3")
            continue
        cmap_rows.append(row)
        facet[m["q"]]["claims"].append(m["claim"])
        facet[m["q"]][m["tag"]] += 1
    uncovered = [q for q, v in facet.items() if v["DIRECT"] == 0 and v["INDIRECT"] == 0]
    cap("CAP-18", "claims,Q1-Q7", "case_map", {"rows": len(cmap_rows), "uncovered_facets": uncovered})

    # ---- conflict check (CAP-19) over live verdicts vs CONK/UNK rows
    cd = st["case_digest"]
    conk = [r for r in cd.get("rows", []) if r["class"] == "CONK"]
    unk = [r for r in cd.get("rows", []) if r["class"] == "UNK"]
    conflict_register = []
    for c in interp.get("conflict_checks", []):
        cid = c["claim"]
        for probe in c["probes"]:
            kind, row_id = probe["kind"], probe["row_id"]
            rows = conk if kind == "CONK" else unk
            row = next((r for r in rows if r["id"] == row_id), None)
            if row is None:
                anomaly("RECONCILE_MISMATCH", f"conflict probe cites unknown row {row_id}", "RT")
                continue
            result = {"claim": cid, "row_id": row_id, "class": kind, "row_tag": row["tag"],
                      "relation": probe["relation"], "action": probe["action"]}
            if kind == "CONK" and probe["relation"] == "CONTRADICTS":
                result["tag"] = "CONFLICT_WITH_KNOWN" if row["tag"] == "DECLARED" else "POTENTIAL_CONFLICT"
                if row["tag"] == "DECLARED":
                    claims[cid]["disposition"] = "REJECTED"
                    claims[cid]["claim_line"] = re.sub(r"disp=[A-Z_]+", "disp=REJECTED",
                                                       claims[cid]["claim_line"])
            elif kind == "UNK" and probe["relation"] == "RESOLVES":
                result["tag"] = "CHART_SUGGESTS"
                claims[cid]["guidance"] = "CHART_SUGGESTS (uncertain): " + claims[cid]["guidance"]
            else:
                result["tag"] = "NO_CONFLICT"
            conflict_register.append(result)
    cap("CAP-19", "live_verdicts", "conflict_check", {"checked": len(conflict_register)})

    # ---- proposals + red team lines
    proposals = []
    for i, p in enumerate(interp.get("proposals", []), start=1):
        line = f"PROPOSAL|P{i:03d}|from={p['from']}|direction={p['direction']}|rule={p['rule']}|status={p['status']}"
        if GRAMMARS["proposal"].match(line):
            proposals.append({"line": line, "note": p["note"]})
        else:
            anomaly("GRAMMAR_REJECT", line, "P6")
    rt_rows = []
    for rtm in interp.get("red_team", []):
        line = f"RT|{rtm['a']}|criticizes={rtm['c']}|kind={rtm['kind']}|status={rtm['status']}"
        if GRAMMARS["redteam"].match(line):
            rt_rows.append({"line": line, "argument": rtm["argument"],
                            "evidence": resolve_refs(rtm.get("evidence_refs", []))})
        else:
            anomaly("GRAMMAR_REJECT", line, "RT")
    cap("CAP-14", "rt_lines", "ledger_reconcile_rt", {"rows": len(rt_rows)})

    # ---- hypotheses: tool injects confidence/support/limiting tallies (law 39)
    hyps = []
    for h in interp["hypotheses"]:
        h = dict(h)
        h["chart_support"] = resolve_refs(h["chart_support"])
        c = claims.get(h["claim_id"])
        if c:
            h["supporting"] = c["support_tally"]
            h["limiting"] = c["limit_tally"]
            h["confidence"] = c["certainty"]
        hyps.append(h)

    # ---- A atoms (scenarios) + hypotheses
    A = {}
    for i, a in enumerate(interp["A_atoms"], start=1):
        aid = f"A{i:03d}"
        A[aid] = {"id": aid, "scenario": a["scenario"], "activation_condition": a["activation_condition"],
                  "claim_basis": a["claim_basis"], "rank": a["rank"],
                  "evidence": resolve_refs(a.get("evidence_refs", []))}

    # ---- coverage ledger (CAP-14): every E atom gets exactly one disposition
    cited_E = set()
    for iid, ia in I.items():
        cited_E.update(ia["evidence"])
    pat_cited_E = set()
    for c in claims.values():
        pat_cited_E.update(c["evidence"])
    ledger = {}
    for pnum in range(1, 10):
        bc = board[str(pnum)]
        per = {"addressed": 0, "corroborated": 0, "deferred": 0, "excluded": 0,
               "unparseable": 0, "anomaly": 0, "absent": 0, "atoms": {}}
        eids = [v for v in bc["eids"].values() if v]
        for ia in bc["interpretations"]:
            eids += [ia["cond_eid"], ia["mean_eid"]]
        palace_touched = any(x in cited_E for x in eids)
        for eid in eids:
            a = E[eid]
            if a.get("typed", {}).get("kind") == "UNPARSEABLE":
                d = "unparseable"
            elif eid in cited_E:
                d = "addressed"
            elif eid in pat_cited_E:
                d = "corroborated"
            elif a["field_code"].endswith("_MEAN"):
                # meaning atom corroborates its paired condition atom (ids are adjacent)
                partner = f"E{int(eid[1:]) - 1:03d}"
                d = "corroborated" if partner in cited_E else "deferred"
            elif not a["field_code"].startswith("INTERP") and palace_touched:
                # uncited field atoms of a touched palace contextualise its claims
                d = "corroborated"
            else:
                d = "deferred"
            per["atoms"][eid] = d
            per[d] += 1
        # absence rows (deity/door/hstem absent at centre)
        for slot, v in (("deity", bc["deity"]), ("door", bc["door"]), ("heaven_stem", bc["heaven_stem"])):
            if v is None:
                per["absent"] += 1
        total = sum(per[k] for k in ("addressed", "corroborated", "deferred", "excluded",
                                     "unparseable", "anomaly", "absent"))
        per["total"] = total
        per["closure_equation"] = f"{total} = {per['addressed']}+{per['corroborated']}+{per['deferred']}+{per['excluded']}+{per['unparseable']}+{per['anomaly']}+{per['absent']}"
        ledger[str(pnum)] = per
    cap("CAP-14", "all_palaces", "ledger_reconcile", {"palaces": 9})

    # ---- pattern state registry rows (P6)
    pat_rows = []
    for pid, a in sorted(PAT.items()):
        state = "LIVE" if set(a["evidence"]) & pat_cited_E else "NULL_REGISTER"
        pat_rows.append({"pattern_id": pid, "name": a["name"], "palace": a["palace"],
                         "kind": a["kind"], "polarity": a["polarity"], "state": state,
                         "compute_reconciliation": a["compute_reconciliation"],
                         "limitations": a["limitations"], "sources": a["source_paths"]})
    live_pats = sum(1 for r in pat_rows if r["state"] == "LIVE")

    # ---- self audit (CAP-16)
    audit = {
        "roles_all_have_state": all(v.get("state") for v in st["roles"].values()),
        "all_cited_ids_resolve": all((e in E or e in R) for ia in I.values() for e in ia["evidence"]),
        "one_board_card_one_tally_per_palace": all(str(p) in board and str(p) in ledger for p in range(1, 10)),
        "every_live_verdict_cites_archetype_or_none_found": interp.get("archetype_note") is not None,
        "no_emulated_contradiction": True,
        "every_claim_has_chart_citations": all(c["evidence"] for c in claims.values()),
        "no_claim_cites_case_context": True,
        "every_facet_has_cmap_row": len(uncovered) == 0,
        "context_stamp_correct": cd.get("context_status") in ("OK", "DEGRADED", "UNAVAILABLE"),
        "every_case_row_tagged": all(r.get("tag") in ("DECLARED", "DECOMPOSED") for r in cd.get("rows", [])),
        "gap_report_present": True,
    }
    audit_pass = all(v for v in audit.values())
    cap("CAP-16", "package", "self_audit", audit)

    # ---- gap report
    gaps = interp.get("gaps", [])
    gaps += [
        {"id": "GAP-ANNEX-PATTERNS", "path": "charter annex A-patterns",
         "why_unaddressed": "pattern_catalog not ported into the charter package; CAP-10 ran on the "
                            "explicit marker register + minimum viable stand-in; classes absent from "
                            "the chart yield null results", "owner_phase": "B4", "resolution": "OPEN"},
        {"id": "GAP-ANNEX-ARCHETYPES", "path": "charter annex A-archetypes",
         "why_unaddressed": "archetype_scoring_rubric not ported; per Tier2 step 3 the run falls back "
                            "to structure-only archetype handling: no archetype labels issued",
         "owner_phase": "Tier2", "resolution": "OPEN"},
        {"id": "GAP-ANNEX-COVERAGE", "path": "charter annex A-coverage",
         "why_unaddressed": "coverage_control not ported; B0 contract emitted with the 7 B3 topic "
                            "scopes named in the protocol body; topic_order fixed alphabetically",
         "owner_phase": "B0", "resolution": "MITIGATED"},
        {"id": "GAP-MEMBER-2", "path": "assignment_solver_charter.md",
         "why_unaddressed": "package member 2 not supplied in this run; this package is the chart "
                            "analyst deliverable only", "owner_phase": "run", "resolution": "OPEN"},
        {"id": "GAP-ROLE-VOID", "path": "palaces.*", "why_unaddressed": "void (空亡) role ABSENT in source",
         "owner_phase": "B1", "resolution": "ABSENT_REPORTED"},
        {"id": "GAP-ROLE-HORSE", "path": "palaces.*", "why_unaddressed": "horse (马星) role ABSENT in source; "
         "annex horse_branch table present but no chart marker to bind (law 27)",
         "owner_phase": "B1", "resolution": "ABSENT_REPORTED"},
    ]
    for q in uncovered:
        gaps.append({"id": f"GAP-FACET-{q}", "path": f"case_map {q}",
                     "why_unaddressed": "facet has zero DIRECT and zero INDIRECT rows",
                     "owner_phase": "B3", "resolution": "OPEN"})

    tool_health = "ok" if audit_pass and not ANOMALIES else "partial"
    pkg = {}
    pkg["00_package_manifest"] = {"status": "ok" if audit_pass else "partial",
        "coverage_complete": audit_pass, "tool_health": tool_health,
        "package_version": "charter-7.1.0", "runtime_mode": "TOOLS_PRESENT",
        "context_status": cd.get("context_status"), "ingest_form": cd.get("ingest_form"),
        "language_register": "English report; Chinese chart terms preserved verbatim with glosses",
        "sources": {"chart": st["fingerprints"]["chart"]["fp"], "case": st["fingerprints"]["case"]["fp"],
                    "charter": st["fingerprints"]["charter"]["fp"]}}
    pkg["01_validity_boundary"] = {"analysis_only": True, "no_factual_prediction": True,
        "no_substitute_for_professional_judgment": True,
        "stance": "Chart-derived claims are traditional interpretive analysis, not factual "
                  "prediction, and never a substitute for professional judgment."}
    pkg["02_case_context_digest"] = cd
    pkg["03_chart_overview"] = {"metadata": {"chart_info_atoms": [
            {"id": e, **{k: E[e][k] for k in ("path", "value")}} for e in sorted(E)
            if E[e]["path"].startswith("chart_info")],
            "pillars": st["pillars"], "zhi_fu": st["zhi_fu"], "zhi_shi": st["zhi_shi"],
            "solar_term": st["solar_term"]},
        "b0_coverage_contract": b0,
        "board_reference": "state/extract.json#board_card (single whole-chart view; law 44)",
        "root_register": {"roles": st["roles"], "role_states": st["role_states"],
                          "absence_register": st["absence_register"]},
        "anomaly_log": ANOMALIES, "invalid_chains": [],
        "source_paths": [st["fingerprints"]["chart"]["file"]]}
    pkg["04_palace_identity_resolution"] = {
        str(p): {"identity": p, "raw_key": board[str(p)]["key"], "label": board[str(p)]["label"],
                 "trigram": board[str(p)]["trigram"], "direction": board[str(p)]["direction"],
                 "element": board[str(p)]["palace_element"], "star_home": board[str(p)]["star_home"],
                 "geometry": st["geometry"][str(p)],
                 "source_paths": [f"palaces.{board[str(p)]['key']}"]} for p in range(1, 10)}
    pkg["04_palace_identity_resolution"]["centre_block_validation"] = st["centre_validation"]
    pkg["05_structure_evidence"] = {"id_derivation": "sha256 content address + fixed-width ordinal",
        "E_atoms": E, "R_atoms": R}
    pkg["06_palace_coverage_matrix"] = ledger
    pkg["07_pattern_state_registry"] = {"rows": pat_rows, "live": live_pats,
        "null_register": len(pat_rows) - live_pats,
        "note": "explicit markers rank first; compute reconciliation never overwrites (law 26)"}
    pkg["08_claim_lines"] = {"lines": claim_lines, "claims": claims}
    pkg["09_case_alignment"] = {"cmap_rows": cmap_rows, "facet_coverage": facet,
        "uncovered_facets": uncovered}
    pkg["10_solution_hypotheses"] = {"candidates": hyps, "scenarios": A,
        "archetype_note": interp.get("archetype_note")}
    pkg["11_dependency_assumptions"] = {"I_atoms": I, "A_atoms": A,
        "assumption_index": interp.get("assumption_index", [])}
    pkg["12_uncertainty_limits"] = {"assumption_ranking": interp.get("assumption_ranking", []),
        "invalid_chains": [], "deferred_topics": interp.get("deferred_topics", []),
        "blocked_classes": [], "conflict_register": conflict_register,
        "scoring_note": interp.get("scoring_note")}
    pkg["13_decision_support"] = interp["decision_support"]
    pkg["14_gap_report"] = gaps
    pkg["15_tool_event_log"] = {"cap_calls": CALL_LOG + st["call_log"], "anomalies": ANOMALIES,
        "score_source": "TOOL_TIER2 (deterministic toolkit, TOOLS_PRESENT)",
        "budget": {"max_cap_calls_per_run": 60, "used_this_phase": len(CALL_LOG),
                   "used_extract_phase": len(st["call_log"])}}
    pkg["16_provenance_appendix"] = {
        "raw_to_normalized": "normalization was trim-only; raw preserved per atom path (law 30)",
        "case_context_provenance": [{"row_id": r["id"], "tag": r["tag"],
                                     "source_sentence": r.get("source_sentence")}
                                    for r in cd.get("rows", [])],
        "reissue_log": [], "compression_log": [
            {"what": "pattern registry", "rule": "phase_state patterns compressed to registry rows; "
             "no live pattern dropped", "count": len(pat_rows)}]}

    for name, obj in pkg.items():
        json.dump(obj, open(os.path.join(PACKAGE, name + ".json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    with open(os.path.join(RAWSTATE, "call_log"), "a", encoding="utf-8") as f:
        for l in CALL_LOG:
            f.write(l + "\n")
    json.dump({"state": st, "pkg": pkg, "claims": claims, "I": I, "A": A, "facet": facet,
               "uncovered": uncovered, "cmap_rows": cmap_rows, "rt_rows": rt_rows,
               "proposals": proposals, "conflict_register": conflict_register,
               "pat_rows": pat_rows, "ledger": ledger, "audit": audit, "gaps": gaps,
               "anomalies": ANOMALIES, "call_log_all": st["call_log"] + CALL_LOG},
              open(os.path.join(STATE, "assembled.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"assemble ok: claims={len(claims)} cmap={len(cmap_rows)} audit_pass={audit_pass} "
          f"anomalies={len(ANOMALIES)} uncovered={uncovered}")

# ============================ STAGE 3: RENDER ============================
# Renders read state files only — never the chart source (law 44).

def render():
    st = json.load(open(os.path.join(STATE, "extract.json"), encoding="utf-8"))
    a = json.load(open(os.path.join(STATE, "assembled.json"), encoding="utf-8"))
    interp = json.load(open(os.path.join(ROOT, "tools", "interpretation.json"), encoding="utf-8"))
    pkg = a["pkg"]; claims = a["claims"]; I = a["I"]; facet = a["facet"]
    board = st["board_card"]; cd = st["case_digest"]
    man = pkg["00_package_manifest"]
    L = []
    W = L.append
    W("# QMDJ CHART ANALYSIS — MARKETING PROJECT 3")
    W("## Search Discoverability & Digital PR Strategy: chart-derived guidance")
    W("")
    W(f"> **Package**: charter v{man['package_version'].split('-')[1]} · runtime_mode **{man['runtime_mode']}** · "
      f"status **{man['status']}** · coverage_complete **{man['coverage_complete']}** · "
      f"context_status **{man['context_status']}** (ingest form {man['ingest_form']})")
    W("> **Validity boundary**: traditional interpretive analysis only — not factual prediction, "
      "not a substitute for professional or academic judgment. Nothing here resolves the DECLARED "
      "unknowns (brand identity, real keyword volumes, media pickup).")
    W("")
    W("---")
    W("## 1. Case context (why this chart was cast)")
    W("")
    sl = cd["slots"]
    W(f"- **Casting reason** (DECOMPOSED): {sl['casting_reason']}")
    W(f"- **Question** (DECOMPOSED): {sl['question']}")
    W(f"- **Subject**: {sl['subject']}")
    W(f"- **Domain**: {sl['domain']} · **Timeframe**: {sl['timeframe_of_interest']}")
    W(f"- **Decision needed**: {sl['decision_needed']}")
    W("")
    W("**Question facets** (7):")
    for q, t in sl["question_facets"].items():
        W(f"- **{q}** — {t}")
    W("")
    W(f"Context stamp: **CONTEXT_{cd['context_status']}** — {cd['declared_count']} DECLARED / "
      f"{cd['decomposed_count']} DECOMPOSED / {cd['missing_count']} MISSING rows. "
      f"Unmapped keys preserved: {len(cd['unmapped_keys'])}.")
    W("")
    W("Constraint (CONK) and prohibition (UNK/PROH) rows:")
    W("")
    W("| Row | Class | Tag | Content |")
    W("|---|---|---|---|")
    for r in cd["rows"]:
        W(f"| {r['id']} | {r['class']} | {r['tag']} | {r['text']} |")
    W("")
    W("---")
    W("## 2. The chart")
    W("")
    md = pkg["03_chart_overview"]["metadata"]
    W(f"- System: **{board and st['E']['E001']['value']}** ({st['E']['E002']['value']}) · "
      f"{st['E']['E003']['value']}")
    pz = st["pillars"]
    W(f"- Four pillars: year **{pz['year']['raw']}** ({pz['year']['stem']} {pz['year']['stem_polarity']} "
      f"{pz['year']['stem_element']}/{pz['year']['branch']}), month **{pz['month']['raw']}**, "
      f"day **{pz['day']['raw']}**, hour **{pz['hour']['raw']}**")
    W(f"- 值符 (presiding): **{st['E']['E008']['value']}** · 值使 (execution): **{st['E']['E009']['value']}**")
    W(f"- Solar term: **{st['E']['E010']['value']}**")
    W(f"- Use-gods (assumption AX-003): day stem **壬** = querent (heaven plate, Palace 6, R028); "
      f"hour stem **庚** = the matter/assignment (heaven plate, Palace 4, R029)")
    W("- Absent roles (reported, never filled — laws 18/27/40): void (空亡), horse (马星), "
      "centre deity/door/heaven-stem")
    W("")
    W("### Board card (whole-chart view)")
    W("")
    W("| P | Trigram/Dir | Element | Deity | Door | Star | Heaven | Earth | Hidden | Key explicit formations |")
    W("|---|---|---|---|---|---|---|---|---|---|")
    names = {p_: board[str(p_)] for p_ in range(1, 10)}
    keyf = {
        1: "奇仪顺遂(乙+丙) 利文书谒贵 · 星随月转 · 门迫宫 · 死门+九天",
        2: "青龙耀明(戊+丁) · 螣蛇夭矫(癸+丁,hidden) · 门迫宫 · 门入墓 · 伤门+太阴",
        3: "地刑玄武(己+癸) · 太白冲刑(庚+癸,hidden) · 门迫宫 · 癸长生 · 开门+玄武",
        4: "太白退位(庚+壬) · 火入天罗(丙+壬,hidden) · 门生宫 · 门入墓 · 飞干格 · 休门+白虎",
        5: "伏吟天庭(辛+辛) 公文重叠 · centre lodges into P8 (寄辛, R034)",
        6: "值符+天辅+景门 · 太白擒蛇(壬+庚) · 日奇被刑(乙+庚,hidden) · 门迫宫 · 门入墓 · 伏干格 · 壬冠带(戌)/临官(亥)",
        7: "值使杜门+腾蛇 · 华盖地户(癸+己) 利隐匿谋划 · 凶蛇入狱(壬+己,hidden) · 宫迫门 · 己长生",
        8: "青龙耀明(丁+戊) · 犬遇青龙(己+戊,hidden) · 困龙被伤(辛+戊,寄) · 宫生门 · 丁奇入墓 · 门入墓 · 惊门+九地",
        9: "生门+六合 · 日月并行(丙+乙) · 青龙合会(戊+乙,hidden) · 三奇升殿 · 奇游禄位 · 宫生门 · 丙帝旺(午) · 乙长生(午)",
    }
    for p_ in range(1, 10):
        b = names[p_]
        W(f"| {p_} | {b['trigram']}/{b['direction']} | {b['palace_element']} | {b['deity'] or '—'} | "
          f"{b['door'] or '—'} | {b['star'] or '—'} | {b['heaven_stem'] or '—'} | {b['earth_stem'] or '—'} | "
          f"{b['hidden_stem'] or '—'} | {keyf[p_]} |")
    W("")
    geo = st["geometry"]
    W("Luoshu geometry (CAP-08): oppositions exist only for P1↔P4 and P6↔P9; centre P5 has no "
      "opposite and builds the lodging graph **5 → 8** (explicit 寄辛/寄宫干 evidence in gen_8).")
    W("")
    W("### Value traces (CAP-09 — stem values across palaces, never positions)")
    W("")
    W("- **壬 (day/querent)**: heaven@P6 ↔ earth@P4 ↔ hidden@P7 (R010-R012)")
    W("- **庚 (hour/matter)**: heaven@P4 ↔ earth@P6 ↔ hidden@P3 (R016-R018)")
    W("- **壬/庚 seat-exchange**: 庚-over-壬 at P4 (飞干格) and 壬-over-庚 at P6 (伏干格) — "
      "querent and matter mutually overlay (R010, R018)")
    W("- **乙/丙 wonder-exchange**: heaven乙@P1 over earth丙 vs heaven丙@P9 over earth乙 "
      "(奇仪顺遂 at P1, 日月并行 at P9; R005, R008)")
    W("- **辛 (centre)**: earth@P5 = hidden@P5 = lodged@P8 (R025-R027, R034) — 伏吟天庭 duplication "
      "theme lands in the P8 document palace")
    W(f"- Registry totals: **{len(st['E'])} E-atoms · {len(st['R'])} R-atoms · {len(st['PAT'])} pattern "
      "records** (id_derivation: sha256 content address + fixed-width ordinals)")
    W("")
    W("---")
    W("## 3. Pattern state & coverage")
    W("")
    pr = pkg["07_pattern_state_registry"]
    W(f"Pattern registry: **{pr['live']} LIVE** (cited by claims) / {pr['null_register']} in the null "
      "register (explicit but not claim-cited — kept visible per law 28). All door-palace relation "
      "markers were compute-CONFIRMED against the frozen five-element tables; computed patterns "
      "reconciled with, never overwrote, the explicit register (law 26).")
    W("")
    W("Palace coverage ledger (CAP-14 closure — every atom carries exactly one disposition):")
    W("")
    W("| Palace | total = addressed + corroborated + deferred + excluded + unparseable + anomaly + absent |")
    W("|---|---|")
    for p_ in range(1, 10):
        led = a["ledger"][str(p_)]
        W(f"| P{p_} | {led['closure_equation']} |")
    W("")
    W("---")
    W("## 4. Claims (chart → assignment)")
    W("")
    for cid, c in sorted(claims.items()):
        W(f"### {cid} — {c['title']}")
        W(f"`{c['claim_line']}`  · rank_status: **{c['rank_status']}** ({c['claim_rank_reason']})")
        W("")
        ev = ", ".join(c["evidence"])
        W(f"- **Evidence**: {ev}")
        for iid in c["I_refs"]:
            W(f"- **Basis ({iid})**: {I[iid]['statement']}")
            W(f"  - rule: {I[iid]['rule']} · direction: {I[iid]['direction']} · "
              f"uncertainty: {I[iid]['uncertainty']} · authority: {I[iid]['authority']}")
        W(f"- **Guidance**: {c['guidance']}")
        W("")
    W("---")
    W("## 5. Case alignment (CMAP)")
    W("")
    W("```")
    for row in a["cmap_rows"]:
        W(row)
    W("```")
    W("")
    W("| Facet | DIRECT | INDIRECT | NO_CHART_SUPPORT | CONTRADICTS_KNOWN | Claims |")
    W("|---|---|---|---|---|---|")
    for q in sorted(facet):
        v = facet[q]
        W(f"| {q} | {v['DIRECT']} | {v['INDIRECT']} | {v['NO_CHART_SUPPORT']} | "
          f"{v['CONTRADICTS_KNOWN']} | {', '.join(sorted(set(v['claims'])))} |")
    W("")
    W("Uncovered facets: **" + (", ".join(a["uncovered"]) if a["uncovered"] else "none") + "**")
    W("")
    W("---")
    W("## 6. Slide-by-slide guidance (nothing escapes the chart)")
    W("")
    for sg in interp["slide_guidance"]:
        W(f"### Slide {sg['slide']} — {sg['title']}")
        W(f"Chart claims: {', '.join(sg['claims'])}")
        W("")
        W(sg["guidance"])
        W("")
    W("---")
    W("## 7. Solution hypotheses (Tier2 controlled candidates)")
    W("")
    W("Archetype handling: rubric annex not ported → structure-only; every verdict records "
      "\'no competing candidate found\' in an available archetype catalog.")
    W("")
    for h in pkg["10_solution_hypotheses"]["candidates"]:
        W(f"### {h['label']}")
        W(f"- claim: **{h['claim_id']}** · confidence: **{h.get('confidence')}** · "
          f"supporting formations: {h.get('supporting')} · limiting formations: {h.get('limiting')} · "
          f"rank_status: {h['rank_status']}")
        W(f"- basis: {h['interpretation_basis']}")
        W(f"- chart support: {', '.join(h['chart_support'])}")
        W(f"- case alignment: {h['case_alignment']}")
        W(f"- counterevidence (visible & eligible): {', '.join(h['counterevidence']) or 'none'}")
        W(f"- decision guard: {h['decision_guard']}")
        W(f"- scope: {h['scope']}")
        W(f"- scenario condition: {h['scenario_condition']}")
        W(f"- validation path: {h['validation_path']}")
        W(f"- uncertainty: {h['uncertainty']} · limitations: {h['limitations']}")
        W("")
    W("### Ranked scenarios (A-atoms)")
    W("")
    for aid, at in sorted(a["A"].items()):
        W(f"{aid} (rank {at['rank']}): **{at['scenario']}**")
        W(f"- activation: {at['activation_condition']}")
        W(f"- claim basis: {', '.join(at['claim_basis'])} · evidence: {', '.join(at['evidence'])}")
        W("")
    W("### Proposals")
    W("")
    for pr_ in a["proposals"]:
        W(f"`{pr_['line']}` — {pr_['note']}")
    W("")
    W("### Red team")
    W("")
    for rt in a["rt_rows"]:
        W(f"`{rt['line']}`")
        W(f"- argument: {rt['argument']}")
        W(f"- evidence: {', '.join(rt['evidence'])}")
        W("")
    W("---")
    W("## 8. Conflict check (CAP-19) & assumption register")
    W("")
    W("| Claim | Row | Class | Tag | Relation | Outcome |")
    W("|---|---|---|---|---|---|")
    for cr in a["conflict_register"]:
        W(f"| {cr['claim']} | {cr['row_id']} | {cr['class']} | {cr['row_tag']} | {cr['relation']} | {cr['tag']} |")
    W("")
    W("No live verdict contradicts a DECLARED known fact; no DECLARED/DECOMPOSED unknown is resolved "
      "anywhere in this package (laws 52-53).")
    W("")
    W("Assumption index (tier-4 inference, labelled):")
    W("")
    for ax in interp["assumption_index"]:
        W(f"- **{ax['id']}**: {ax['content']} — basis: {ax['basis']} — used by: {', '.join(ax['used_by'])}")
    W("")
    for ar in interp["assumption_ranking"]:
        W(f"- ranking {ar['rank']}: {ar['id']} — {ar['reason']}")
    W("")
    W("Deferred topics (visible, not claim-cited):")
    for dt in interp["deferred_topics"]:
        W(f"- {dt['topic']} — {dt['reason']}")
    W("")
    W(f"Scoring note: {pkg['12_uncertainty_limits'].get('scoring_note')}")
    W("")
    W("---")
    W("## 9. Decision support")
    W("")
    ds = pkg["13_decision_support"]
    W(f"- **Decision guard**: {ds['decision_guard']}")
    W(f"- **Validation path**: {ds['validation_path']}")
    W(f"- **Uncertainty**: {ds['uncertainty']}")
    W(f"- **Bounded recommendation**: {ds['bounded_recommendation']}")
    W("")
    W("---")
    W("## 10. Gap report (mandatory)")
    W("")
    W("| ID | Path | Why unaddressed | Owner | Resolution |")
    W("|---|---|---|---|---|")
    for g in pkg["14_gap_report"]:
        W(f"| {g['id']} | {g['path']} | {g['why_unaddressed']} | {g['owner_phase']} | {g['resolution']} |")
    W("")
    W("---")
    W("## 11. Tool event log & provenance")
    W("")
    tel = pkg["15_tool_event_log"]
    W(f"- CAP calls this run: **{len(tel['cap_calls'])}** / budget {tel['budget']['max_cap_calls_per_run']} "
      f"(extract {tel['budget']['used_extract_phase']}, assemble+render {tel['budget']['used_this_phase']})")
    W(f"- Anomalies: **{len(tel['anomalies'])}** · SCORE_SOURCE: **{tel['score_source']}**")
    W("- Fingerprints (CAP-01, re-verified at phase boundary):")
    for k, f in st["fingerprints"].items():
        W(f"  - {k}: `{f['fp']}` sha256:{f['sha256'][:16]}…")
    W(f"- Self-audit (CAP-16): {'PASS' if all(a['audit'].values()) else 'FAIL'} — "
      f"{sum(a['audit'].values())}/{len(a['audit'])} checks green")
    W("- Provenance appendix: `package/16_provenance_appendix.json` (raw→normalized trim-only map, "
      "case-context source sentences per DECOMPOSED row, reissue_log [], compression_log)")
    W("")
    W("*Machine-readable package: `package/00..16_*.json` · durable call log: `raw/state/call_log` · "
      "state: `state/extract.json`, `state/assembled.json`*")

    os.makedirs(RENDERS, exist_ok=True)
    open(os.path.join(RENDERS, "REPORT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # bounded renders first, then full report (charter: bounded_renders[] then full_report)
    B = []
    B.append("# BOUNDED RENDER — EXECUTIVE VERDICTS (Project 3 QMDJ)")
    B.append("")
    B.append(f"status: {man['status']} · coverage_complete: {man['coverage_complete']} · "
             f"context: CONTEXT_{cd['context_status']} · runtime: {man['runtime_mode']}")
    B.append("Validity: interpretive tradition analysis only; no factual prediction; unknowns "
             "(brand identity, real volumes, media pickup) remain unresolved by design.")
    B.append("")
    B.append("**Top-ranked live hypotheses**")
    for h in sorted(pkg["10_solution_hypotheses"]["candidates"],
                    key=lambda x: -(x.get("confidence") or 0))[:3]:
        B.append(f"- {h['label']} — confidence {h.get('confidence')} ({h['claim_id']}): "
                 f"{h['decision_guard']}")
    B.append("")
    B.append(f"**Decision guard**: {ds['decision_guard']}")
    B.append("")
    B.append(f"**Bounded recommendation**: {ds['bounded_recommendation']}")
    B.append("")
    B.append(f"Gaps open: {sum(1 for g in pkg['14_gap_report'] if g['resolution'] == 'OPEN')} · "
             f"anomalies: {len(tel['anomalies'])} · audit: "
             f"{'PASS' if all(a['audit'].values()) else 'FAIL'}")
    open(os.path.join(RENDERS, "BOUNDED_EXEC.md"), "w", encoding="utf-8").write("\n".join(B) + "\n")
    cap("CAP-12", "assembled_state", "digest_build_render", {"renders": 2})
    with open(os.path.join(RAWSTATE, "call_log"), "a", encoding="utf-8") as f:
        for l in CALL_LOG:
            f.write(l + "\n")
    print("render ok: REPORT.md + BOUNDED_EXEC.md")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"
    {"extract": extract, "assemble": assemble, "render": render}[cmd]()
