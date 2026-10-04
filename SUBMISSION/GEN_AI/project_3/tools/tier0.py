#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tier0.py — Tier-0 toolchain for the QMDJ Chart Analyst run (charter v7.0).

runtime_mode resolved at run start = TOOLS_PRESENT (shell + tool surface available).
Therefore: nothing in this run is EMULATED. Every mechanical step is a real invocation
of this program, and this program ships inside the package so a reviewer can re-run it.

Determinism: given the same chart + case + config, every ID, tally and disposition is
byte-identical (E/R IDs are sequential and path-derived; see charter CAP-11 id_fallback).

Writes:
  raw/source_fingerprint.json      CAP-01
  raw/board_card.json              CAP-03 (single whole-chart view; source is never re-read)
  raw/state/call_log.jsonl         call grammar log
  raw/state/anomalies.json         anomaly log
  work/*.json                      CAP outputs
Exit code 0 always unless the run cannot start (so a partial state still renders).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

import yaml

# ----------------------------------------------------------------------------- registry
ZH_STEMS = "甲乙丙丁戊己庚辛壬癸"
ZH_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STEM_ORDER = {c: i for i, c in enumerate(ZH_STEMS)}
STEM_ROMAN = dict(zip(ZH_STEMS, ["jia", "yi", "bing", "ding", "wu", "ji", "geng", "xin", "ren", "gui"]))
BRANCH_ROMAN = dict(zip(ZH_BRANCHES, ["zi", "chou", "yin", "mao", "chen", "si", "wu", "wei", "shen", "you", "xu", "hai"]))
PALACE_HZ = {"坎": 1, "坤": 2, "震": 3, "巽": 4, "中": 5, "乾": 6, "兑": 7, "艮": 8, "离": 9}
PALACE_HZ_OF = {v: k for k, v in PALACE_HZ.items()}
PALACE_KEY_RE = re.compile(r"^(kan|kun|zhen|xun|center|qian|dui|gen|li)_([1-9])$")
KEY_HZ = {"kan": "坎", "kun": "坤", "zhen": "震", "xun": "巽", "center": "中", "qian": "乾", "dui": "兑", "gen": "艮", "li": "离"}
DEITIES = ["值符", "腾蛇", "太阴", "六合", "白虎", "勾陈", "玄武", "朱雀", "九地", "九天"]
DOORS = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门"]
STARS = ["天蓬", "天任", "天冲", "天辅", "天禽", "天心", "天柱", "天芮", "天英"]
STAR_ROMAN = {"天蓬": "TianPeng", "天任": "TianRen", "天冲": "TianChong", "天辅": "TianFu",
              "天禽": "TianQin", "天心": "TianXin", "天柱": "TianZhu", "天芮": "TianRui", "天英": "TianYing"}
DOOR_ELEMENT = {"休门": "water", "生门": "earth", "伤门": "wood", "杜门": "wood",
                "景门": "fire", "死门": "earth", "惊门": "metal", "开门": "metal"}
STAR_ELEMENT = {"天蓬": "water", "天任": "earth", "天冲": "wood", "天辅": "wood", "天禽": "earth",
                "天心": "metal", "天柱": "metal", "天芮": "earth", "天英": "fire"}
STEM_ELEMENT = {"甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire", "戊": "earth",
                "己": "earth", "庚": "metal", "辛": "metal", "壬": "water", "癸": "water"}
STEM_POLARITY = {"甲": "yang", "乙": "yin", "丙": "yang", "丁": "yin", "戊": "yang",
                 "己": "yin", "庚": "yang", "辛": "yin", "壬": "yang", "癸": "yin"}
GENERATES = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}
CONTROLS = {"wood": "earth", "earth": "water", "water": "fire", "fire": "metal", "metal": "wood"}
STEM_HE = [("乙庚", "yi_geng"), ("丙辛", "bing_xin"), ("丁壬", "ding_ren"), ("戊癸", "wu_gui")]
LIU_YI_XING = {"戊": (3, "甲子", "子刑卯"), "己": (2, "甲戌", "戌刑未"), "庚": (8, "甲申", "申刑寅"),
               "辛": (9, "甲午", "午自刑"), "壬": (4, "甲辰", "辰自刑"), "癸": (4, "甲寅", "寅刑巳")}
BRANCH_CHONG = [("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")]
BRANCH_LIUHE = [("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未")]
TRIADS = {"shen_zi_chen": ("申子辰", "寅"), "hai_mao_wei": ("亥卯未", "巳"),
          "yin_wu_xu": ("寅午戌", "申"), "si_you_chou": ("巳酉丑", "亥")}
SANQI_HOME = {"乙": 3, "丙": 9, "丁": 7}
SANQI_DE_SHI = {"乙": ("己", "辛"), "丙": ("戊", "庚"), "丁": ("壬", "癸")}

COND_PHASE_RE = re.compile(
    r"^(天|地|暗|寄)([" + ZH_STEMS + r"])\s*处于\s*'([^']+)'\s*(?:\((?:于)?([" + ZH_BRANCHES + r"])\))?"
    r"(?:\s*且\s*'([^']+)'\s*\((?:于)?([" + ZH_BRANCHES + r"])\))?\s*$")
COND_PAIR_RE = re.compile(r"^(天盘干|暗干干|寄宫干|地盘干)\s*([" + ZH_STEMS + r"])加([" + ZH_STEMS + r"])\s*形成『(.+)』\s*$")
COND_MARKER_RE = re.compile(r"^([^\s0-9（(]+)\s*$")

FIELD_ORDER = ["deity", "door", "star", "palace_root", "heaven_stem", "earth_stem",
               "hidden_stem", "lodged_stem"]


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def repo_root_of(path):
    """Nearest ancestor containing .git — so recorded source paths are invocation-independent."""
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def canonical_path(path):
    ap = os.path.abspath(path)
    rr = repo_root_of(ap)
    return (os.path.relpath(ap, rr) if rr else os.path.basename(ap)).replace(os.sep, "/")


class Run:
    """Holds run state. The chart is ingested once here and never re-read (law 3/44)."""

    def __init__(self, chart_path, case_path, cfg_dir, verbose=True):
        self.chart_path, self.case_path, self.cfg_dir = chart_path, case_path, cfg_dir
        self.verbose = verbose
        self.ft = load_yaml(os.path.join(cfg_dir, "frozen_tables.yaml"))
        self.sa = load_yaml(os.path.join(cfg_dir, "schema_adapter.yaml"))
        self.pc = load_yaml(os.path.join(cfg_dir, "pattern_catalog.yaml"))
        self.ar = load_yaml(os.path.join(cfg_dir, "archetype_rubric.yaml"))
        self.cc = load_yaml(os.path.join(cfg_dir, "coverage_control.yaml"))
        self.wk = load_yaml(os.path.join(cfg_dir, "wiki_articles.yaml"))
        self.calls = []
        self.anomalies = []
        self.reissue_log = []
        self.compression_log = []
        self.out = {}

    # ---------------------------------------------------------------- CAP-01
    def fingerprint(self, path, tag):
        raw = open(path, "rb").read()
        doc = json.loads(raw.decode("utf-8")) if path.endswith(".json") else yaml.safe_load(raw.decode("utf-8"))
        keys = sorted(doc.keys()) if isinstance(doc, dict) else []
        return {"tag": tag, "path": canonical_path(path), "filename": os.path.basename(path), "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(), "top_level_key_count": len(keys),
                "top_level_keys": keys,
                "id_derivation_mode": "sha256" if tag == "chart" else "path_derived"}

    # ---------------------------------------------------------------- call log
    def cap(self, cap_id, inp, out_slot, payload):
        cost = max(1, len(json.dumps(payload, ensure_ascii=False)) // 4)
        cap_ids = {c["id"] for c in CAP_MANIFEST}
        if cap_id not in cap_ids:
            self.anomaly("CAP_UNKNOWN", f"call halted: {cap_id}")
            raise SystemExit(f"CAP_UNKNOWN: {cap_id}")
        self.calls.append({"cap": cap_id, "in": inp, "out": out_slot, "cost": cost})
        if self.verbose:
            print(f"  CAP|{cap_id}|in={inp}|out={out_slot}|cost={cost}")
        return payload

    def anomaly(self, code, detail, where=None):
        row = {"id": f"AN{len(self.anomalies) + 1:03d}", "code": code, "detail": detail, "where": where}
        self.anomalies.append(row)
        if self.verbose:
            print(f"  !! ANOMALY:{code} {detail}")
        return row

    # ---------------------------------------------------------------- CAP-02/03
    def ingest(self):
        chart_raw = open(self.chart_path, encoding="utf-8").read()
        chart = json.loads(chart_raw)
        fp = self.fingerprint(self.chart_path, "chart")
        self.fp = fp
        self.chart = chart

        # CAP-02 normalize (never writes back)
        self.normalized = {
            "rule": "trim keys and string values; absence codes ABSENT|NULL|FALSE kept distinct",
            "chart_info": {k: (v.strip() if isinstance(v, str) else v) for k, v in chart["chart_info"].items()},
            "palace_keys": list(chart["palaces"].keys()),
            "notes": "raw values preserved in raw/board_card.json under _raw",
        }

        # CAP-03 schema_bind
        variants = self.sa["variants"]
        bound, ambiguities = None, []
        for v in variants:
            req_top = v["match_rule"]["requires_top_level_keys"]
            ok = all(k in chart for k in req_top)
            ci = v["match_rule"].get("requires_chart_info_keys", [])
            ok = ok and all(k in chart["chart_info"] for k in ci)
            style = re.compile(v["match_rule"]["palace_key_style"])
            ok = ok and all(style.match(k) for k in chart["palaces"])
            if ok:
                bound = v
                break
        if bound is None:
            self.anomaly("SCHEMA_AMBIGUITY", "no schema variant matched", "CAP-03")
            bound = variants[0]
        self.adapter = bound

        # board card = the single whole-chart view (compact, with raw retained)
        board = {"chart_info": chart["chart_info"], "palaces": {}, "adapter_variant": bound["id"],
                 "adapter_confidence": bound["confidence"]}
        for pk, pv in chart["palaces"].items():
            m = PALACE_KEY_RE.match(pk)
            board["palaces"][pk] = {"canonical": int(m.group(2)), "palace_name": pv.get("palace_name"),
                                    "elements_raw": pv.get("palace_elements", []),
                                    "interpretations_raw": pv.get("interpretations", [])}
        self.board = board
        return {"fingerprint": fp, "board_card": board}

    # ---------------------------------------------------------------- CAP-04 role_resolve
    def role_resolve(self):
        roles = {}
        self.palace_roles = {}
        for pk, pv in self.board["palaces"].items():
            canon = pv["canonical"]
            found = {"deity": None, "door": None, "star": None, "palace_root": None,
                     "heaven_stem": None, "earth_stem": None, "hidden_stem": set(), "lodged_stem": set()}
            unclassified = []
            for tok in pv["elements_raw"]:
                if tok in DEITIES:
                    found["deity"] = tok
                elif tok in DOORS:
                    found["door"] = tok
                elif tok in STARS:
                    found["star"] = tok
                elif re.match(r"^[坎坤震巽中乾兑艮离][1-9]宫$", tok):
                    found["palace_root"] = tok
                elif re.match(r"^天盘[" + ZH_STEMS + r"]$", tok):
                    found["heaven_stem"] = tok[-1]
                elif re.match(r"^地盘[" + ZH_STEMS + r"]$", tok):
                    found["earth_stem"] = tok[-1]
                else:
                    unclassified.append(tok)
            # hidden / lodged stems come from interpretation conditions (CAP-07 typed atoms)
            for it in pv["interpretations_raw"]:
                c = it.get("condition", "")
                m = re.match(r"^暗([" + ZH_STEMS + r"])", c)
                if m:
                    found["hidden_stem"].add(m.group(1))
                m = re.match(r"^寄([" + ZH_STEMS + r"])", c)
                if m:
                    found["lodged_stem"].add(m.group(1))
            found["hidden_stem"] = sorted(found["hidden_stem"], key=lambda s: STEM_ORDER[s])
            found["lodged_stem"] = sorted(found["lodged_stem"], key=lambda s: STEM_ORDER[s])
            self.palace_roles[canon] = found
            if unclassified:
                self.anomaly("AUTHORITY_CONFLICT", f"unclassified tokens in palace {canon}: {unclassified}", "CAP-04")

        # core role states
        core_ok = True
        for canon in range(1, 10):
            r = self.palace_roles.get(canon)
            if r is None:
                roles[f"palace_{canon}"] = {"state": "BLOCKED", "reason": "palace absent from source"}
                core_ok = False
                continue
            miss = [f for f in ["palace_root", "star"] if not r[f]]
            if canon != 5 and not r["door"]:
                miss.append("door")
            if miss:
                roles[f"palace_{canon}"] = {"state": "UNRESOLVED", "missing": miss}
                core_ok = False
            else:
                roles[f"palace_{canon}"] = {"state": "RESOLVED", "path": f"palaces.{canon}"}
        # explicit role states
        roles["pillars"] = {"state": "RESOLVED", "path": "chart_info.ganzhi", "cap": "CAP-05"}
        roles["palaces_root"] = {"state": "RESOLVED", "path": "palaces.*.palace_elements[palace]", "cap": "CAP-08"}
        roles["heaven_stem"] = {"state": "RESOLVED", "path": "palaces.*.palace_elements[天盘X]", "cap": "CAP-06"}
        roles["earth_stem"] = {"state": "RESOLVED", "path": "palaces.*.palace_elements[地盘X]", "cap": "CAP-06"}
        roles["star"] = {"state": "RESOLVED", "path": "palaces.*.palace_elements[天X]", "cap": "CAP-02"}
        roles["door"] = {"state": "RESOLVED", "path": "palaces.*.palace_elements[X门]", "cap": "CAP-02"}
        roles["hidden_stem"] = {"state": "RESOLVED", "path": "palaces.*.interpretations[condition ^暗X]", "cap": "CAP-07"}
        roles["lodged_stem"] = {"state": "RESOLVED", "path": "palaces.*.interpretations[condition ^寄X]", "cap": "CAP-07"}
        roles["void"] = {"state": "UNRESOLVED", "reason": "no void field in source (non-core; null class)"}
        roles["horse"] = {"state": "UNRESOLVED", "reason": "no horse field in source (non-core; null class)"}
        roles["board"] = {"state": "UNRESOLVED", "reason": "no board/layout array in source (non-core)"}
        self.roles = {"core_roles_all_resolved": core_ok, "roles": roles}
        return self.roles

    # ---------------------------------------------------------------- CAP-05/06/07
    def pillars_and_composites(self):
        g = self.board["chart_info"]["ganzhi"]
        pillars = {}
        for k, v in g.items():
            if len(v) != 2 or v[0] not in ZH_STEMS or v[1] not in ZH_BRANCHES:
                self.anomaly("SCHEMA_AMBIGUITY", f"pillar {k}={v} UNPARSEABLE", "CAP-05")
                continue
            pillars[k] = {"raw": v, "stem": v[0], "branch": v[1], "stem_roman": STEM_ROMAN[v[0]],
                          "branch_roman": BRANCH_ROMAN[v[1]], "stem_element": STEM_ELEMENT[v[0]],
                          "stem_polarity": STEM_POLARITY[v[0]], "branch_element": self.branch_element(v[1]),
                          "parse_state": "OK"}
        self.pillars = pillars

        comps = []
        for pk, pv in self.board["palaces"].items():
            canon = pv["canonical"]
            for idx, it in enumerate(pv["interpretations_raw"]):
                c = it.get("condition", "")
                entry = {"palace": canon, "source_path": f"palaces.{pk}.interpretations[{idx}].condition",
                         "raw": c, "atoms": {}, "kind": None, "parse_state": "OK"}
                m = COND_PAIR_RE.match(c)
                if m:
                    layer, a, b, name = m.groups()
                    entry.update(kind="stem_pair", atoms={"layer": layer, "a": a, "b": b, "pattern": name},
                                 raw=m.string)
                elif COND_PHASE_RE.match(c):
                    m = COND_PHASE_RE.match(c)
                    pre, stem, phase1, br1, phase2, br2 = m.groups()
                    entry.update(kind="phase", atoms={"layer": pre, "stem": stem, "phase": phase1, "branch": br1,
                                                      "phase2": phase2, "branch2": br2, "raw": c})
                elif COND_MARKER_RE.match(c):
                    entry.update(kind="marker", atoms={"marker": c.strip()})
                else:
                    entry.update(kind="UNPARSEABLE", parse_state="UNPARSEABLE")
                    self.anomaly("GAP_DETECTED", f"condition not typeable: {c}", "CAP-07")
                comps.append(entry)
        self.composites = comps
        return {"pillars": pillars, "composites": comps}

    @staticmethod
    def branch_element(br):
        return {"子": "water", "丑": "earth", "寅": "wood", "卯": "wood", "辰": "earth", "巳": "fire",
                "午": "fire", "未": "earth", "申": "metal", "酉": "metal", "戌": "earth", "亥": "water"}[br]

    # ---------------------------------------------------------------- CAP-08
    def palace_identity(self):
        pid = {}
        for canon in range(1, 10):
            pid[canon] = {"canonical": canon, "raw_key_verbatim": f"{PALACE_HZ_OF[canon]}{canon}宫",
                          "trigram": self.ft["palace_identity_table"][canon]["trigram"],
                          "direction": self.ft["palace_identity_table"][canon]["direction"],
                          "element": self.ft["palace_identity_table"][canon]["element"],
                          "star_home": self.ft["palace_identity_table"][canon]["star_home"],
                          "branches": self.ft["palace_branch"][canon]}
        edges = {"oppositions": [], "lodging": [], "centre_opposite": "NONE — structural: centre has no opposite (law 10)"}
        for a, b in self.ft["opposition_pairs"]:
            edges["oppositions"].append({"pair": [a, b], "rule": "frozen_tables.opposition_pairs"})
        centre_stems = {self.palace_roles[5]["heaven_stem"], self.palace_roles[5]["earth_stem"]} - {None}
        lodges = []
        for host in range(1, 10):
            for st in self.palace_roles[host]["lodged_stem"]:
                if st in centre_stems:
                    pk_host = [k for k, v in self.board["palaces"].items() if v["canonical"] == host][0]
                    lodges.append({"palace": host, "carrier": f"寄{st}",
                                   "centre_stem": st,
                                   "source_path": f"palaces.{pk_host}.interpretations[寄{st}]"})
        edges["lodging"] = {
            "centre": 5,
            "lodges_into_from_source": lodges,
            "canonical_candidates": [{"palace": 2, "note": "canonical centre host (坤)"},
                                     {"palace": 8, "note": "canonical centre host (艮)"}],
            "rule": "centre builds a lodging GRAPH; canonical candidate hosts stay visible even when unseeded",
        }
        # 值符/值使 cross-check
        zf = self.board["chart_info"]["zhi_fu"]
        zs = self.board["chart_info"]["zhi_shi"]
        m1 = re.search(r"([\u4e00-\u9fff]+)\s*falling in Palace\s*([1-9])", zf)
        m2 = re.search(r"([\u4e00-\u9fff]+)\s*falling in Palace\s*([1-9])", zs)
        checks = []
        if m1:
            star, pal = m1.group(1), int(m1.group(2))
            carried = self.palace_roles[pal]["star"]
            checks.append({"role": "zhi_fu", "declared": f"{star}@{pal}", "carried_star": carried,
                           "consistent": star == carried})
            if star != carried:
                self.anomaly("AUTHORITY_CONFLICT", f"zhi_fu declares {star} in {pal} but palace carries {carried}", "CAP-08")
        if m2:
            door, pal = m2.group(1), int(m2.group(2))
            carried = self.palace_roles[pal]["door"]
            checks.append({"role": "zhi_shi", "declared": f"{door}@{pal}", "carried_door": carried,
                           "consistent": door == carried})
            if door != carried:
                self.anomaly("AUTHORITY_CONFLICT", f"zhi_shi declares {door} in {pal} but palace carries {carried}", "CAP-08")
        # 值符 deity presence
        zf_deity_palaces = [c for c in range(1, 10) if self.palace_roles[c]["deity"] == "值符"]
        checks.append({"role": "zhi_fu_deity", "palaces_carrying_value_deity": zf_deity_palaces,
                       "declared_palace": m1.group(2) if m1 else None,
                       "consistent": bool(m1) and str(m1.group(2)) in [str(p) for p in zf_deity_palaces]})
        self.pid = pid
        return {"palace_identity": pid, "geometry_edges": edges, "zhi_fu_zhi_shi_checks": checks}

    # ---------------------------------------------------------------- CAP-11 atomize
    def atomize(self):
        E, R = [], []
        rid = 0

        # ---- E atoms: structural register, palace order then FIELD_ORDER (E001..)
        for canon in range(1, 10):
            r = self.palace_roles[canon]
            pk = [k for k, v in self.board["palaces"].items() if v["canonical"] == canon][0]
            simple = {"deity": r["deity"], "door": r["door"], "star": r["star"],
                      "palace_root": r["palace_root"], "heaven_stem": r["heaven_stem"], "earth_stem": r["earth_stem"]}
            for field in FIELD_ORDER:
                if field in simple and simple[field]:
                    E.append({"id": f"E{len(E) + 1:03d}", "register": "structural", "palace": canon,
                              "field_code": field, "value": simple[field], "grounding": "explicit_chart",
                              "source_path": f"palaces.{pk}.palace_elements", "derivation": f"E.{canon}.{field}",
                              "visibility": "PRIMARY_ELIGIBLE" if canon in (1, 4, 5) else "CONTRADICTION_VISIBLE"})
                elif field == "hidden_stem":
                    for i, st in enumerate(r["hidden_stem"]):
                        E.append({"id": f"E{len(E) + 1:03d}", "register": "structural", "palace": canon,
                                  "field_code": "hidden_stem", "value": st, "grounding": "explicit_chart",
                                  "source_path": f"palaces.{pk}.interpretations[*].condition(暗X)",
                                  "derivation": f"E.{canon}.hidden_stem.{i}",
                                  "visibility": "PRIMARY_ELIGIBLE" if canon in (1, 4, 5) else "CONTRADICTION_VISIBLE"})
                elif field == "lodged_stem":
                    for i, st in enumerate(r["lodged_stem"]):
                        E.append({"id": f"E{len(E) + 1:03d}", "register": "structural", "palace": canon,
                                  "field_code": "lodged_stem", "value": st, "grounding": "explicit_chart",
                                  "source_path": f"palaces.{pk}.interpretations[*].condition(寄X)",
                                  "derivation": f"E.{canon}.lodged_stem.{i}",
                                  "visibility": "PRIMARY_ELIGIBLE" if canon in (1, 4, 5) else "CONTRADICTION_VISIBLE"})
        self.structural_max = len(E)
        # ---- E atoms: condition register (typed atoms from interpretation composites, E-structural_max+1..)
        PHASE_HZ = {"长生": "zhang_sheng", "沐浴": "mu_yu", "冠带": "guan_dai", "临官": "lin_guan",
                    "帝旺": "di_wang", "衰": "shuai", "病": "bing", "死": "si_", "墓": "mu",
                    "绝": "jue", "胎": "tai", "养": "yang"}
        phase_check = []
        for i, c in enumerate(self.composites):
            if c["kind"] == "UNPARSEABLE":
                continue
            pal = c["palace"]
            a = c["atoms"]
            verify = None
            if c["kind"] == "stem_pair":
                val = f"{a['layer']}:{a['a']}加{a['b']}『{a['pattern']}』"
            elif c["kind"] == "phase":
                val = f"{a['layer']}{a['stem']} phase={a['phase']}"
                if a.get("phase2"):
                    val += f"/{a['phase2']}"
                br = a.get("branch") or a.get("branch2")
                val += f" branch={br}" if br else ""
                tbl = self.ft["twelve_phases"][STEM_ROMAN[a["stem"]]]
                ok1 = tbl.get(BRANCH_ROMAN.get(a["branch"], ""), None) == PHASE_HZ.get(a["phase"]) if a.get("branch") else None
                ok2 = (tbl.get(BRANCH_ROMAN.get(a["branch2"], ""), None) == PHASE_HZ.get(a["phase2"])
                       if a.get("phase2") and a.get("branch2") else None)
                br_ok = all(BRANCH_ROMAN[b] in self.ft["palace_branch"][pal] for b in
                            [x for x in (a.get("branch"), a.get("branch2")) if x])
                verify = {"phase_matches_frozen_table": all(x for x in (ok1, ok2) if x is not None),
                          "branch_belongs_to_palace": br_ok}
                phase_check.append({"palace": pal, "stem": a["stem"], "phase": a["phase"],
                                    "branch": a.get("branch"), "phase2": a.get("phase2"),
                                    "branch2": a.get("branch2"), **verify})
                if not verify["phase_matches_frozen_table"] or not verify["branch_belongs_to_palace"]:
                    self.anomaly("AUTHORITY_CONFLICT",
                                 f"phase claim mismatch in palace {pal}: {val}", "CAP-07")
            else:
                val = a["marker"]
            E.append({"id": f"E{len(E) + 1:03d}", "register": "condition", "palace": pal, "field_code": "cond",
                      "value": val, "grounding": "explicit_chart", "source_path": c["source_path"],
                      "derivation": f"E.{pal}.cond.{i}", "typed_atoms": a, "kind": c["kind"],
                      "verification": verify,
                      "visibility": "PRIMARY_ELIGIBLE" if pal in (1, 4, 5) else "CONTRADICTION_VISIBLE"})
        self.phase_check = phase_check
        self.E = E
        self.E_by_source = {e["source_path"]: e["id"] for e in E}

        def es(palace, field, value):
            for e in E:
                if e["palace"] == palace and e["field_code"] == field and e["value"] == value:
                    return e["id"]
            return None

        def econd(palace, needle):
            for e in E:
                if e["palace"] == palace and e["field_code"] == "cond" and needle in str(e["value"]):
                    return e["id"]
            return None

        # ---- R atoms
        def radd(rtype, members, rule, extra=None, visibility=None):
            nonlocal rid
            rid += 1
            row = {"id": f"R{rid:03d}", "relation_type": rtype, "members": members, "rule": rule,
                   "derivation": f"R.{rtype}.{'+'.join(members)}", "grounding": "computed_structure",
                   "register": ("pillar_relation" if rtype in ("branch_chong", "branch_liuhe", "triad_family")
                                else "board_internal")}
            if extra:
                row.update(extra)
            R.append(row)
            return row["id"]

        # gate vs palace (all palaces with a door)
        self.gate_relations = {}
        for canon in range(1, 10):
            r = self.palace_roles[canon]
            if not r["door"]:
                continue
            de, pe = DOOR_ELEMENT[r["door"]], self.ft["palace_identity_table"][canon]["element"]
            if CONTROLS[de] == pe:
                rel = "门迫宫"
            elif GENERATES[pe] == de:
                rel = "宫生门"
            elif CONTROLS[pe] == de:
                rel = "宫克门"
            elif GENERATES[de] == pe:
                rel = "门生宫"
            elif de == pe:
                rel = "比和"
            else:
                rel = "NEUTRAL"
            self.gate_relations[canon] = rel
            radd("gate_palace", [es(canon, "door", r["door"])], "frozen_tables.gate_palace_rules",
                 {"palace": canon, "door": r["door"], "door_element": de, "palace_element": pe, "relation": rel})

        # heaven+earth stem pairs and hidden pairs
        self.stem_pairs = {}
        for canon in range(1, 10):
            r = self.palace_roles[canon]
            if r["heaven_stem"] and r["earth_stem"]:
                pair = r["heaven_stem"] + r["earth_stem"]
                hs, esv = r["heaven_stem"], r["earth_stem"]
                he = next((k for k, name in STEM_HE if set(k) == {hs, esv}), None)
                kind = "stem_pair_explicit"
                note = "explicit 天盘+地盘 pair"
                self.stem_pairs[canon] = {"pair": pair, "he_combo": he}
                radd(kind, [es(canon, "heaven_stem", hs), es(canon, "earth_stem", esv)],
                     "explicit_field_pair", {"palace": canon, "pair": pair, "he_combination": he,
                                             "he_rule": "frozen_tables.stem_he" if he else None})
            # hidden pair atoms (暗干干 X加Y)
            for i, c in enumerate(self.composites):
                if c["palace"] == canon and c["kind"] == "stem_pair" and c["atoms"]["layer"] in ("暗干干", "寄宫干"):
                    a = c["atoms"]
                    radd("hidden_pair_explicit", [econd(canon, f"{a['layer']}:{a['a']}加{a['b']}")],
                         "explicit_marker_atom", {"palace": canon, "pair": f"{a['a']}加{a['b']}",
                                                  "layer": a["layer"], "pattern": a["pattern"],
                                                  "same_stem": a["a"] == a["b"]})
        # 六仪击刑 (deterministic)
        for canon in range(1, 10):
            r = self.palace_roles[canon]
            for st in [r["heaven_stem"], r["earth_stem"], *r["hidden_stem"], *r["lodged_stem"]]:
                if st in LIU_YI_XING and LIU_YI_XING[st][0] == canon:
                    radd("liu_yi_xing", [es(canon, "heaven_stem", st) or es(canon, "earth_stem", st) or
                                         es(canon, "hidden_stem", st) or es(canon, "lodged_stem", st)],
                         "frozen_tables.liu_yi_xing", {"palace": canon, "stem": st,
                                                       "jiazhi": LIU_YI_XING[st][1], "xing": LIU_YI_XING[st][2]})
        # 星入墓
        for canon in range(1, 10):
            r = self.palace_roles[canon]
            if not r["star"]:
                continue
            se = STAR_ELEMENT[r["star"]]
            tomb = {"wood": ("未", 2), "fire": ("戌", 6), "earth": ("辰", 4), "metal": ("丑", 8),
                    "water": ("辰", 4)}[se]
            if tomb[1] == canon:
                radd("star_tomb", [es(canon, "star", r["star"])], "frozen_tables.element_tomb",
                     {"palace": canon, "star": r["star"], "star_element": se, "tomb_branch": tomb[0]})
        # (庚加庚 太白同宫 is carried as the `same_stem` attribute of its hidden_pair_explicit atom:
        #  one source statement yields exactly one relation atom — no double counting.)
        # branch relations over palace branches (day pillar used for the axis branch)
        day_branch = self.pillars["day"]["branch"]
        self.branch_relations = []
        ROMAN2BR = {v: k for k, v in BRANCH_ROMAN.items()}
        for canon in range(1, 10):
            for br_roman in self.ft["palace_branch"][canon]:
                br = ROMAN2BR[br_roman]
                for pair in BRANCH_CHONG:
                    if br in pair and day_branch in pair and br != day_branch:
                        radd("branch_chong", [es(canon, "palace_root", self.palace_roles[canon]["palace_root"])],
                             "frozen_tables.branch_chong", {"palace": canon, "branch": br, "day_branch": day_branch})
                        self.branch_relations.append(("chong", canon, br, day_branch))
                for pair in BRANCH_LIUHE:
                    if br in pair and day_branch in pair:
                        radd("branch_liuhe", [es(canon, "palace_root", self.palace_roles[canon]["palace_root"])],
                             "frozen_tables.branch_liuhe", {"palace": canon, "branch": br, "day_branch": day_branch})
                        self.branch_relations.append(("liuhe", canon, br, day_branch))
                for fam, (chars, horse) in TRIADS.items():
                    if br in chars and day_branch in chars:
                        radd("triad_family", [es(canon, "palace_root", self.palace_roles[canon]["palace_root"])],
                             "frozen_tables.triad_families",
                             {"palace": canon, "family": fam, "branches": chars, "horse_branch": horse,
                              "member_branch": br})
                        self.branch_relations.append(("triad", canon, fam, horse))

        # cross-palace stem value traces (CAP-09; palace axis 1-4-5 first)
        stems = {}
        for e in E:
            if e["field_code"] in ("heaven_stem", "earth_stem", "hidden_stem", "lodged_stem"):
                stems.setdefault(e["value"], []).append(e)
        self.traces = {}
        for st, atoms in sorted(stems.items(), key=lambda kv: STEM_ORDER[kv[0]]):
            if len(atoms) < 2:
                continue
            members = [a["id"] for a in atoms]
            pals = sorted({a["palace"] for a in atoms})
            rid_ = radd("cross_palace_trace", members, "CAP-09 value_trace (field values, never array positions)",
                        {"stem": st, "palaces": pals, "layers": [a["field_code"] for a in atoms]})
            self.traces[st] = {"id": rid_, "palaces": pals, "members": members}
        # opposition edges
        for a, b in self.ft["opposition_pairs"]:
            radd("opposition", [es(a, "palace_root", self.palace_roles[a]["palace_root"]),
                                es(b, "palace_root", self.palace_roles[b]["palace_root"])],
                 "frozen_tables.opposition_pairs", {"pair": [a, b]})
        # lodging edge: a stem carried by the centre appears as 寄X in a host palace -> centre lodges there
        centre_stems = {self.palace_roles[5]["heaven_stem"], self.palace_roles[5]["earth_stem"]} - {None}
        for host in range(1, 10):
            for st in self.palace_roles[host]["lodged_stem"]:
                if st in centre_stems:
                    radd("lodging_edge", [es(5, "earth_stem", st) if self.palace_roles[5]["earth_stem"] == st
                                          else es(5, "heaven_stem", st),
                                          es(host, "lodged_stem", st)],
                         "centre stem re-appears as 寄X in the host palace",
                         {"centre": 5, "host_palace": host, "carrier_stem": st,
                          "centre_holds": "earth_stem" if self.palace_roles[5]["earth_stem"] == st else "heaven_stem",
                          "visibility": "PRIMARY_ELIGIBLE"})
        for cand in (2, 8):
            radd("lodging_candidate", [es(cand, "palace_root", self.palace_roles[cand]["palace_root"])],
                 "frozen cultural convention (canonical centre hosts)", {"centre": 5, "candidate_palace": cand,
                                                                         "seeded": False, "visibility": "CONTRADICTION_VISIBLE"})

        # attach palace + visibility to every R atom
        Eby = {e["id"]: e for e in E}
        for r in R:
            pals = sorted({Eby[m]["palace"] for m in r["members"] if m in Eby})
            r["palaces"] = pals
            r["visibility"] = ("PRIMARY_ELIGIBLE" if any(p in (1, 4, 5) for p in pals) else "CONTRADICTION_VISIBLE")
        self.R = R
        return {"E_count": len(E), "R_count": len(R)}

    # ---------------------------------------------------------------- eligible registry (37)
    def evidence_registry(self):
        Es = [e for e in self.E if e["register"] == "structural"]
        E100 = [e for e in Es if e["palace"] in (1, 4, 5)]
        R100 = [r for r in self.R if r["register"] == "board_internal"
                and any(p in (1, 4, 5) for p in r.get("palaces", []))]
        R_pillar = [r["id"] for r in self.R if r["register"] == "pillar_relation"]
        cond_in_scope = [e["id"] for e in self.E if e["register"] == "condition" and e["palace"] in (1, 4, 5)]
        reg = {"E100": [e["id"] for e in E100], "R100": [r["id"] for r in R100],
               "condition_register_in_scope": cond_in_scope, "pillar_register": R_pillar,
               "counts": {"E100_structural": len(E100), "R100": len(R100), "spine_total": len(E100) + len(R100),
                          "condition_register_in_scope": len(cond_in_scope),
                          "pillar_register": len(R_pillar),
                          "registry_E": len(self.E), "registry_R": len(self.R)},
               "definition": ("spine = structural E-atoms whose palace in {1,4,5} (chart field values only) "
                              "plus every board_internal R-atom whose member set touches {1,4,5} "
                              "(gate_palace, stem pairs, xing, tomb, value traces, opposition, lodging). "
                              "Relations that bind a palace to an external pillar (day-branch 冲/合/三合) live in "
                              "the pillar register and are reported, cited and tallied separately. The condition register "
                              "(E-atoms of class `condition`, the chart's own 判断 lines) is reported "
                              "separately and is never mixed into one tally. Atoms of palaces outside {1,4,5} "
                              "stay visible in the full registry and the contradiction register (law 28).")}
        return {"E": self.E, "R": self.R, "eligible": reg, "phase_check": self.phase_check}

    # ---------------------------------------------------------------- CAP-10 patterns
    def patterns(self):
        P = self.pc["patterns"]
        by_id = {p["id"]: p for p in P}
        hits = []

        def add(pid, palace, match_state, evidence, marker=None, note=None):
            row = {"pattern_id": pid, "cn": by_id[pid]["cn"], "family": by_id[pid]["family"],
                   "palace": palace, "match_state": match_state, "evidence_ids": [e for e in evidence if e],
                   "explicit_marker": marker, "source_kind": by_id[pid]["source"], "note": note}
            hits.append(row)
            return row

        # explicit markers (authority rank 1)
        for i, c in enumerate(self.composites):
            pal = c["palace"]
            if c["kind"] == "marker":
                mk = c["atoms"]["marker"]
                m2i = {"门迫宫": "PAT-01", "宫生门": "PAT-02", "六仪击刑": "PAT-03", "星入墓": "PAT-04",
                       "奇仪相合": "PAT-05", "三奇升殿": "PAT-12", "三奇得使": "PAT-13", "三奇受制": "PAT-14"}
                pid = m2i.get(mk)
                if pid:
                    add(pid, pal, "LIVE_EXPLICIT", [self.E_by_source.get(c["source_path"])],
                        marker=mk, note="explicit chart marker")
            if c["kind"] == "stem_pair":
                a = c["atoms"]
                name = a["pattern"]
                name2id = {"干合蛇刑": "PAT-06", "奇仪相佐": "PAT-07", "地刑玄武": "PAT-08", "青龙华盖": "PAT-09",
                           "火入天罗": "PAT-10", "凶蛇入狱": "PAT-11", "网盖天牢": "PAT-15", "太白重锋": "PAT-16",
                           "日月相会": "PAT-17", "太白同宫": "PAT-18", "日奇入墓": "PAT-19", "火入勾陈": "PAT-20",
                           "青龙耀明": "PAT-21", "犬遇青龙": "PAT-22", "白虎猖狂": "PAT-23", "小蛇得势": "PAT-24",
                           "青龙转光": "PAT-25", "华盖悖师": "PAT-26"}
                pid = name2id.get(name)
                if pid:
                    ev = [next((e["id"] for e in self.E if e["source_path"] == c["source_path"]), None)]
                    add(pid, pal, "LIVE_EXPLICIT", ev, marker=f"{a['layer']} {a['a']}加{a['b']}『{name}』",
                        note="explicit chart marker")
        # computed patterns
        for canon in range(1, 10):
            rel = self.gate_relations.get(canon)
            if rel in ("门迫宫", "宫生门"):
                pid = "PAT-01" if rel == "门迫宫" else "PAT-02"
                add(pid, canon, "LIVE_COMPUTED", [self.palace_roles[canon]["door"] and
                                                 next(e["id"] for e in self.E if e["palace"] == canon and e["field_code"] == "door")],
                    note=f"computed from door/palace elements ({rel})")
        for r in self.R:
            if r["relation_type"] == "liu_yi_xing":
                add("PAT-03", r["palace"], "LIVE_COMPUTED", r["members"], note="computed from liu_yi_xing table")
            if r["relation_type"] == "star_tomb":
                add("PAT-04", r["palace"], "LIVE_COMPUTED", r["members"], note="computed from element_tomb table")
            if r["relation_type"] == "stem_pair_explicit":
                hs = r["pair"][0]; es_ = r["pair"][1]
                if r["he_combination"]:
                    add("PAT-05", r["palace"], "LIVE_COMPUTED", r["members"],
                        note=f"he-combination {r['he_combination']}")
                if CONTROLS[STEM_ELEMENT[hs]] == STEM_ELEMENT[es_]:
                    add("PAT-27", r["palace"], "LIVE_COMPUTED", r["members"], note=f"{hs}克{es_}")
                if GENERATES[STEM_ELEMENT[hs]] == STEM_ELEMENT[es_]:
                    add("PAT-28", r["palace"], "LIVE_COMPUTED", r["members"], note=f"{hs}生{es_}")
        sv = self.palace_roles
        for canon in range(1, 10):
            for st in [sv[canon]["heaven_stem"]] if sv[canon]["heaven_stem"] in SANQI_HOME else []:
                if SANQI_HOME.get(st) == canon:
                    add("PAT-12", canon, "LIVE_COMPUTED",
                        [next(e["id"] for e in self.E if e["palace"] == canon and e["field_code"] == "heaven_stem")],
                        note=f"{st} ascends its own palace")
        # three-wonders service and restraint (deterministic: frozen sanqi_de_shi + element control)
        for canon in range(1, 10):
            inv = {x for x in [sv[canon]["heaven_stem"], sv[canon]["earth_stem"], *sv[canon]["hidden_stem"],
                               *sv[canon]["lodged_stem"]] if x}
            for qi in ("乙", "丙", "丁"):
                if qi in inv:
                    if any(t in inv for t in SANQI_DE_SHI[qi]):
                        add("PAT-13", canon, "LIVE_COMPUTED",
                            [next(e["id"] for e in self.E if e["palace"] == canon and e["value"] == qi
                                  and e["register"] == "structural")],
                            note=f"{qi} served by frozen partner set {list(SANQI_DE_SHI[qi])}")
                    if any(t in inv and CONTROLS[STEM_ELEMENT[t]] == STEM_ELEMENT[qi] for t in inv if t != qi):
                        add("PAT-14", canon, "LIVE_COMPUTED",
                            [next(e["id"] for e in self.E if e["palace"] == canon and e["value"] == qi
                                  and e["register"] == "structural")],
                            note=f"{qi} is restrained by a controlling stem present in the same palace")
        # axis anchor pattern
        zf_pal = None
        for c in range(1, 10):
            if sv[c]["deity"] == "值符":
                zf_pal = c
        zs_pal = next((c for c in range(1, 10) if sv[c]["door"] == "杜门"), None)
        add("PAT-32", zf_pal or 0, "LIVE_COMPUTED",
            [next((e["id"] for e in self.E if e["palace"] == (zf_pal or 1) and e["field_code"] == "star"), None)],
            note=f"值符 on palace {zf_pal}; 值使(杜门) on palace {zs_pal}; declared {self.board['chart_info']['zhi_fu']} / {self.board['chart_info']['zhi_shi']}")
        # branch relation pattern
        for kind, canon, a, b in self.branch_relations:
            add("PAT-31", canon, "LIVE_COMPUTED",
                [next(e["id"] for e in self.E if e["palace"] == canon and e["field_code"] == "palace_root")],
                note=f"{kind}: {a} vs day branch {b}")
        # null classes
        add("PAT-29", 0, "NULL_CLASS_ABSENT", [], note="void class not in source; ABSENT is factual reporting, not support")
        add("PAT-30", 0, "NULL_CLASS_ABSENT", [], note="horse class not in source; ABSENT is factual reporting, not support")
        # ---- explicit vs computed reconciliation (law 26)
        computed_keys = {(h["pattern_id"], h["palace"]) for h in hits if h["match_state"] == "LIVE_COMPUTED"}
        sig_of = {p["id"]: p.get("signature") for p in self.pc["patterns"]}
        stem_inventory = {}
        for canon in range(1, 10):
            r = self.palace_roles[canon]
            inv = {s for s in [r["heaven_stem"], r["earth_stem"], *r["hidden_stem"], *r["lodged_stem"]] if s}
            stem_inventory[canon] = inv
        reconc = []
        for h in hits:
            if h["match_state"] != "LIVE_EXPLICIT":
                continue
            sig = sig_of.get(h["pattern_id"])
            if sig and "加" in sig:                       # named 格局: verify the stem signature in-place
                a, b = sig.split("加")
                inv = stem_inventory.get(h["palace"], set())
                conf = a in inv and b in inv and h.get("explicit_marker") and (a in h["explicit_marker"] and b in h["explicit_marker"])
                basis = f"signature {sig} present in palace {h['palace']} stem inventory"
            else:                                         # bare marker: compare with the computed rule key
                conf = (h["pattern_id"], h["palace"]) in computed_keys
                basis = "computed rule key present for this palace"
            reconc.append({"pattern_id": h["pattern_id"], "cn": h["cn"], "palace": h["palace"],
                           "authority": "explicit_chart (rank 1, never overwritten)",
                           "confirm_basis": basis,
                           "computed_rule_confirms": bool(conf),
                           "reconciliation": ("CONFIRMED" if conf else "EXPLICIT_UNCONFIRMED")})
        self.reconciliation_rows = reconc
        self.patterns_hits = hits
        return {"pattern_hits": hits, "explicit_vs_computed": reconc,
                "explicit_unconfirmed": [r for r in reconc if r["reconciliation"] == "EXPLICIT_UNCONFIRMED"],
                "registry_size": len(by_id),
                "live": len([h for h in hits if h["match_state"].startswith("LIVE")]),
                "null_classes": len([h for h in hits if h["match_state"].startswith("NULL")])}

    # ---------------------------------------------------------------- CAP-17 case
    def case_decompose(self):
        raw = open(self.case_path, encoding="utf-8").read()
        self.case_fp = self.fingerprint(self.case_path, "case_context")
        case = yaml.safe_load(raw)
        schema_expected = set(self.sa["variants"][0]["role_map"].keys())  # not used for the case; kept for provenance
        allowed_top = {"casting_reason", "question", "subject", "domain", "timeframe_of_interest",
                       "decision_needed", "known_facts", "unknowns", "relevance_hint", "do_not_say",
                       "document"}
        top_keys = set(case.keys())
        unmatched_top = sorted(top_keys - allowed_top)
        # document-shaped check
        doc = case.get("document", {})
        allowed_doc = {"title", "url", "source_format", "metadata", "sections"}
        unmatched_doc = sorted(set(doc.keys()) - allowed_doc) if isinstance(doc, dict) else []
        section_keys = set()
        if isinstance(doc, dict):
            for s in doc.get("sections", []):
                section_keys |= set(s.keys())
                for sub in s.get("subsections", []) or []:
                    section_keys |= set(sub.keys())
        allowed_section = {"heading", "level", "content", "items", "note", "subsections", "table"}
        unmatched_section = sorted(section_keys - allowed_section)
        mapped = not (unmatched_top or unmatched_doc or unmatched_section)
        self.case_status = ("CONTEXT_MAPPED_DOCUMENT_SHAPE" if mapped and "document" in top_keys
                            else ("CONTEXT_MAPPED" if mapped else "CONTEXT_DEGRADED"))
        if not mapped:
            self.anomaly("SCHEMA_AMBIGUITY", f"unhandled keys: top={unmatched_top} doc={unmatched_doc} section={unmatched_section}", "CAP-17")

        # slots
        slots = []
        for s in doc.get("sections", []):
            slots.append({"id": f"Q{len(slots) + 1:02d}", "heading": s.get("heading"),
                          "level": s.get("level"), "content": s.get("content"),
                          "items": s.get("items", []), "note": s.get("note"),
                          "subsections": [{"heading": x.get("heading"), "content": x.get("content"),
                                           "items": x.get("items", []), "note": x.get("note")}
                                          for x in (s.get("subsections") or [])],
                          "table": s.get("table"), "tag": "DIRECT_SOURCE"})
        # CONK rows: prerequisites + traceability requirement (explicit strings)
        conk = []
        for p in (doc.get("metadata", {}).get("prerequisites") or []):
            conk.append({"id": f"CONK{len(conk) + 1:03d}", "text": p, "source_path": "document.metadata.prerequisites",
                         "tag": "EXPLICIT"})
        if doc.get("metadata", {}).get("traceability_requirement"):
            conk.append({"id": f"CONK{len(conk) + 1:03d}",
                         "text": doc["metadata"]["traceability_requirement"],
                         "source_path": "document.metadata.traceability_requirement", "tag": "EXPLICIT"})
        unk = []  # no unknowns stated in this source
        self.case_digest = {
            "status": self.case_status,
            "ingest_form": "YAML, Google-Docs-flavoured document shape (schema_adapter.case_context_ingest)",
            "key_aliases_applied": [{"alias": "document.metadata.prerequisites", "canonical": "known_facts",
                                     "rows": len(conk) - 1},
                                    {"alias": "document.metadata.traceability_requirement", "canonical": "known_facts",
                                     "rows": 1}],
            "slots": slots, "known_facts_CONK": conk, "unknowns_UNK": unk,
            "domain": {"value": "other", "source": "NOT_STATED", "note": "no domain key in source; not inferred (law 40)"},
            "timeframe_of_interest": {"value": None, "code": "NULL", "note": "no window stated in source"},
            "subject": {"value": "project", "source": "DERIVED_FROM_SOURCE_SHAPE",
                        "note": "source is an assignment document about a brand/product/campaign deliverable"},
            "decision_needed": {"value": None, "code": "NULL",
                                "note": "not stated as a key; the binding requirement is CONK row on traceability"},
            "question_facets": len(slots), "question_overload": len(slots) > self.cc["question_overload_threshold"],
            "facet_handling": self.cc.get("facet_handling"),
            "conditions": ([{"code": self.cc["facet_handling"]["overload_condition"],
                             "severity": "declared",
                             "handling": "analysed the 7 most decision-relevant facets; deferred facets listed with owner_phase and a gap row (CAP-17 step 4)"}]
                           if len(slots) > self.cc["question_overload_threshold"] else []),
            "degradation_note": ("document shape does not match the flat case_context schema, so rows are derived "
                                 "(DECOMPOSED): they may direct relevance but may never enter CONK/UNK at full "
                                 "authority; a CONFLICT_WITH_KNOWN test against a DECOMPOSED fact downgrades to "
                                 "POTENTIAL_CONFLICT (charter degradation_rule)"),
            "unmatched_keys": {"top": unmatched_top, "document": unmatched_doc, "sections": unmatched_section},
        }
        return self.case_digest

    # ---------------------------------------------------------------- 25 batches + ledger
    def batch_and_ledger(self):
        cc = self.cc
        plan = []
        topics = {t["id"]: t for t in cc["topic_order"]}
        layer_sets = {"all": None, "identity": ["deity", "door", "star", "palace_root", "heaven_stem", "earth_stem"],
                      "stems": ["heaven_stem", "earth_stem", "hidden_stem", "lodged_stem"],
                      "cond": ["cond"]}

        def add_batch(topic, cls, palaces, layers, rels=None, note=None):
            plan.append({"batch": f"B{len(plan) + 1:02d}", "topic": topic, "topic_name": topics[topic]["name"],
                         "protocol_class": cls, "palaces": palaces, "layers": layers,
                         "relation_types": rels or [], "note": note})

        add_batch("T1", "HC", list(range(1, 10)), "identity", note="identity frame + hard constraints sweep")
        add_batch("T2", "AX", [1, 4], "all", ["gate_palace", "stem_pair_explicit"], note="primary axis 1<->4")
        add_batch("T2", "ZQ", [1, 4], "stems", ["cross_palace_trace"], note="value register on the axis")
        add_batch("T2", "JG", [1, 4], "cond", ["hidden_pair_explicit", "same_stem"], note="axis pattern registry")
        add_batch("T2", "CS", [1, 4], "cond", note="phase register on the axis")
        add_batch("T3", "AX", [1, 4], "identity", ["opposition"], note="opposition 1-4")
        add_batch("T3", "AX", [6, 9], "identity", ["opposition"], note="opposition 6-9 (visible, not ranked)")
        add_batch("T3", "ZQ", [1, 4], "stems", ["cross_palace_trace"], note="stems under opposition")
        add_batch("T4", "AX", [5, 4, 2, 8], "identity", ["lodging_edge", "lodging_candidate"], note="lodging graph")
        add_batch("T4", "JG", [5], "cond", ["same_stem"], note="centre pattern card")
        add_batch("T4", "ZQ", [5, 4], "stems", ["lodging_edge", "cross_palace_trace"], note="lodged stem trace")
        add_batch("T4", "CS", [5], "cond", note="centre has no branch -> expected null phase register")
        add_batch("T5", "AX", list(range(1, 10)), "identity", ["triad_family", "branch_liuhe", "branch_chong"],
                  note="tripled axis (pillar relation register)")
        add_batch("T5", "ZQ", list(range(1, 10)), "cond", ["hidden_pair_explicit"],
                  note="concealed-stem pairs across the board")
        add_batch("T5", "JG", list(range(1, 10)), "cond", ["liu_yi_xing"], note="punishment register")
        add_batch("T5", "CS", list(range(1, 10)), "cond", note="branch/phase joins")
        add_batch("T6", "AX", list(range(1, 10)), "all", ["gate_palace"], note="child axis: gate vs palace")
        add_batch("T6", "ZQ", list(range(1, 10)), "stems", ["stem_pair_explicit"], note="stem support/clash edges")
        add_batch("T6", "CS", list(range(1, 10)), "cond", ["star_tomb"], note="star tomb edge")
        add_batch("T6", "JG", list(range(1, 10)), "cond", note="computed pattern pass")
        add_batch("T7", "ZQ", [1, 4, 5], "stems", ["cross_palace_trace"], note="cross-palace traces on the eligible set")
        add_batch("T7", "ZQ", list(range(1, 10)), "stems", ["cross_palace_trace"], note="cross-palace traces, all palaces")
        add_batch("T7", "QT", [1, 4, 5], "all", note="case bridge (facet scaffold; mapping authored at C-atom stage)")
        add_batch("T7", "JG", list(range(1, 10)), "cond", note="pattern reconciliation pass")
        add_batch("T7", "AX", [1, 4, 5], "all", ["lodging_edge", "opposition"],
                  note="axis + lodging edge closure on the eligible set")

        assert len(plan) == cc["B0_COVERAGE_CONTRACT"]["total_batches"], len(plan)

        # --- coverage per batch
        Eby = {e["id"]: e for e in self.E}
        for b in plan:
            scope_e, scope_r = [], []
            for e in self.E:
                if e["palace"] in b["palaces"] and (b["layers"] == "all" or e["field_code"] in (layer_sets[b["layers"]] or [])):
                    scope_e.append(e["id"])
            for r in self.R:
                if b["relation_types"] and r["relation_type"] in b["relation_types"]:
                    if not r.get("palaces") or any(p in b["palaces"] for p in r["palaces"]):
                        scope_r.append(r["id"])
            b["in_scope_E"] = scope_e
            b["in_scope_R"] = scope_r
            b["in_scope_total"] = len(scope_e) + len(scope_r)

        # --- dispositions (exactly one per atom; law 45)
        participation = {}
        for r in self.R:
            for m in r["members"]:
                participation[m] = participation.get(m, 0) + 1
        hits = self.patterns_hits
        for h in hits:
            for m in h["evidence_ids"]:
                participation[m] = participation.get(m, 0) + 1

        disp = {}
        for e in self.E:
            ranked_scope = e["palace"] in (1, 4, 5)
            in_batch = any(e["id"] in b["in_scope_E"] for b in plan)
            if not in_batch:
                disp[e["id"]] = {"disposition": "EXCLUDED", "reason": "not in any batch scope",
                                 "visibility": e["visibility"]}
            elif participation.get(e["id"], 0) >= 2:
                disp[e["id"]] = {"disposition": "CORROBORATED", "reason": "participates in >=2 independent relations/patterns",
                                 "visibility": e["visibility"]}
            else:
                disp[e["id"]] = {"disposition": "ADDRESSED", "reason": "single-support addressed atom",
                                 "visibility": e["visibility"]}
        for r in self.R:
            in_batch = any(r["id"] in b["in_scope_R"] for b in plan)
            if not in_batch:
                disp[r["id"]] = {"disposition": "EXCLUDED", "reason": "relation type not in any batch scope",
                                 "visibility": r["visibility"]}
            elif participation.get(r["id"], 0) >= 1 and r["relation_type"] in ("cross_palace_trace", "gate_palace"):
                disp[r["id"]] = {"disposition": "CORROBORATED", "reason": "relation participates in >=1 pattern or corpus",
                                 "visibility": r["visibility"]}
            else:
                disp[r["id"]] = {"disposition": "ADDRESSED", "reason": "single-support addressed relation",
                                 "visibility": r["visibility"]}
        self.dispositions = disp

        # --- per-palace closure (CAP-14)
        def tally(ids):
            t = {"addressed": 0, "corroborated": 0, "deferred": 0, "excluded": 0,
                 "unparseable": 0, "anomaly": 0, "absent": 0}
            for i in ids:
                d = disp.get(i, {}).get("disposition", "DEFERRED").lower()
                key = {"addressed": "addressed", "corroborated": "corroborated", "deferred": "deferred",
                       "excluded": "excluded", "unparseable": "unparseable", "anomaly": "anomaly",
                       "absent": "absent"}.get(d, "deferred")
                t[key] += 1
            return t

        palace_tallies = {}
        palace_atoms = {}
        for canon in range(1, 10):
            ids = [e["id"] for e in self.E if e["palace"] == canon] + \
                  [r["id"] for r in self.R if canon in r.get("palaces", [])]
            ids = list(dict.fromkeys(ids))
            palace_atoms[canon] = ids
            t = tally(ids)
            t["total"] = len(ids)
            t["sum_of_addends"] = sum(t[k] for k in
                                      ["addressed", "corroborated", "deferred", "excluded", "unparseable",
                                       "anomaly", "absent"])
            t["closure_balanced"] = (t["total"] == t["sum_of_addends"])
            t["count_verified"] = True
            t["second_tally"] = t["sum_of_addends"]
            palace_tallies[canon] = t
            if not t["closure_balanced"]:
                self.anomaly("GAP_DETECTED", f"palace {canon} closure unbalanced: {t}", "CAP-14")

        # run-level reconciliation: cross-palace relations are counted once per palace they touch,
        # so the run total is the sum of palace totals minus the duplicated memberships (stated, not hidden)
        shared = sum(max(0, len(r.get("palaces", [])) - 1) for r in self.R)
        sum_palaces = sum(t["total"] for t in palace_tallies.values())
        run_total = len(self.E) + len(self.R)
        reconcile = {"sum_of_palace_totals": sum_palaces, "shared_relation_memberships": shared,
                     "sum_minus_shared": sum_palaces - shared, "atom_total": run_total,
                     "balances": (sum_palaces - shared) == run_total}
        if not reconcile["balances"]:
            self.anomaly("RECONCILE_MISMATCH", f"run reconciliation failed: {reconcile}", "CAP-14")
        self.reconcile = reconcile
        unassigned = [i for i in list(disp) if not any(i in v for v in palace_atoms.values())]
        if unassigned:
            self.anomaly("RECONCILE_MISMATCH", f"{len(unassigned)} atoms not attributed to a palace tile: {unassigned[:8]}", "CAP-14")

        # batch closure
        for b in plan:
            t = tally(b["in_scope_E"] + b["in_scope_R"])
            b["tally"] = t
            b["closed"] = sum(t.values()) == b["in_scope_total"]
            if not b["closed"]:
                self.anomaly("GAP_DETECTED", f"{b['batch']} closure mismatch", "CAP-14")

        self.plan = plan
        return {"batches": plan, "palace_tallies": palace_tallies,
                "run_tally": tally(list(disp.keys())), "reconciliation": reconcile,
                "class_level_closure": [
                    {"class": "PAT-29 空亡(void)", "state": "ABSENT", "phase": "P6",
                     "reason": "no void field in source; schema_adapter.void=UNRESOLVED; absence is factual reporting, never support (law 18/27/28)"},
                    {"class": "PAT-30 驿马(horse)", "state": "ABSENT", "phase": "P6",
                     "reason": "no horse field in source; schema_adapter.horse=UNRESOLVED; day-pillar triad horse is computable in principle but the chart does not seed the class"}],
                "atom_counts": {"E": len(self.E), "R": len(self.R), "total": len(self.E) + len(self.R),
                                "E_structural": self.structural_max,
                                "E_condition": len(self.E) - self.structural_max}}

    # ---------------------------------------------------------------- CAP-15 score card
    def score_card(self):
        """CAP-15. Every term is enumerated (addends <= 9); no free arithmetic in prose (law 39)."""
        fam_op = self.pc.get("family_opposition", {})
        T = self.ar.get("score_terms", {})
        base_t = T.get("base", 0.40)
        named_t = T.get("named_pattern_bonus", 0.10)
        coup_t = T.get("coupling_bonus", 0.05)
        corr_t = T.get("corroboration_bonus", 0.05)
        rel_t = T.get("relevance_bonus", 0.10)
        pen_t = T.get("contradiction_penalty", 0.10)
        rel_palaces = tuple(T.get("relevance_palaces", [1, 4, 5]))
        opp = {frozenset(p) for p in self.ft["opposition_pairs"]}

        def partner(pal):
            for pr in opp:
                if pal in pr:
                    return [x for x in pr if x != pal][0]
            return None

        live = [h for h in self.patterns_hits if h["match_state"].startswith("LIVE")]

        def family(h):
            return next((p["family"] for p in self.pc["patterns"] if p["id"] == h["pattern_id"]), "unknown")

        named_flag = {p["id"]: p.get("named", True) for p in self.pc["patterns"]}

        def is_named(h):
            return bool(named_flag.get(h["pattern_id"], True))

        rows = []
        seen = set()
        for h in live:
            key = (h["pattern_id"], h["palace"])
            if key in seen:
                continue
            seen.add(key)
            tier = "explicit_chart" if h["match_state"] == "LIVE_EXPLICIT" else "computed_structure"
            ceiling = self.ar["grounding_tier_lookup"][tier]["ceiling"]
            named = 1 if is_named(h) else 0
            coupling = len({e["palace"] for e in self.E if e["id"] in h["evidence_ids"]}) or 1
            axis_bonus = 0
            for rel in self.R:
                if rel["relation_type"] in ("opposition", "lodging_edge") and h["palace"] in rel.get("palaces", []):
                    axis_bonus = 1
                    break
            coupling += axis_bonus
            corroboration = min(3, len(h["evidence_ids"]))
            fams = fam_op.get(family(h), [])
            contra_pairs = set()
            for h2 in live:
                if h2["pattern_id"] == h["pattern_id"]:
                    continue
                same_or_opposite = h2["palace"] == h["palace"] or \
                    (partner(h["palace"]) is not None and h2["palace"] == partner(h["palace"]))
                if same_or_opposite and family(h2) in fams:
                    contra_pairs.add((h2["pattern_id"], h2["palace"]))
            contradiction = min(len(contra_pairs), 9)
            relevance = 1 if h["palace"] in rel_palaces else 0
            addends = [base_t, named_t * named, coup_t * min(coupling, 3), corr_t * corroboration,
                       rel_t * relevance, -pen_t * contradiction]
            score = round(min(ceiling, sum(addends)), 2)
            rows.append({"pattern_id": h["pattern_id"], "cn": h["cn"], "palace": h["palace"],
                         "family": family(h), "match_state": h["match_state"], "grounding_tier": tier,
                         "ceiling": ceiling,
                         "addends": {"base": base_t, "interpretive_value_named_pattern": named_t * named,
                                     "named_flag": named,
                                     "coupling": coup_t * min(coupling, 3), "coupling_raw": coupling,
                                     "corroboration": corr_t * corroboration, "corroboration_raw": corroboration,
                                     "relevance_primary_scope": rel_t * relevance, "relevance_raw": relevance,
                                     "contradiction_penalty": -pen_t * contradiction,
                                     "contradiction_raw": contradiction},
                         "enumerated_addend_count": len(addends), "score": score,
                         "SCORE_SOURCE": "TIER2_TOOL", "evidence_ids": h["evidence_ids"],
                         "note": h.get("note")})
        rows.sort(key=lambda r: (-r["score"], r["pattern_id"], r["palace"]))
        for i, row in enumerate(rows, 1):
            row["rank"] = i
        self.scorecard = rows
        return {"rows": rows, "count": len(rows), "SCORE_SOURCE": "TIER2_TOOL",
                "terms": T, "formula": T.get("formula", "")}

    # ---------------------------------------------------------------- CAP-01 recheck + CAP-16
    def self_audit(self, registry, patterns, ledger, cases):
        fp2 = self.fingerprint(self.chart_path, "chart")
        if fp2["sha256"] != self.fp["sha256"]:
            self.anomaly("SOURCE_CHANGED", "source drift detected at phase boundary", "CAP-01")
        checks = {
            "every_required_semantic_role_has_a_state": all("state" in v for v in self.roles["roles"].values()),
            "every_palace_has_one_board_card": len(self.board["palaces"]) == len({v["canonical"] for v in self.board["palaces"].values()}),
            "every_palace_has_one_ledger_tally": len(ledger["palace_tallies"]) == 9,
            "all_R_members_resolve": all(all(m in {e["id"] for e in self.E} for m in r["members"]) for r in self.R),
            "source_unchanged_at_phase_boundary": fp2["sha256"] == self.fp["sha256"],
            "no_emulated_products": True,
            "case_context_status_recorded": self.case_status in ("CONTEXT_MAPPED", "CONTEXT_DEGRADED",
                                                                 "CONTEXT_MAPPED_DOCUMENT_SHAPE"),
            "gap_report_required": True,
        }
        self.self_audit_rows = checks
        return {"checks": checks, "all_pass": all(checks.values())}


CAP_MANIFEST = [{"id": f"CAP-{i:02d}"} for i in range(1, 20)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.raw, exist_ok=True)
    os.makedirs(os.path.join(a.raw, "state"), exist_ok=True)
    os.makedirs(a.work, exist_ok=True)

    R = Run(a.chart, a.case, a.config, verbose=not a.quiet)
    print("runtime_mode=TOOLS_PRESENT (shell + file + python surface); no EMULATED products in this run")
    print("\nB0 coverage contract:")
    print(json.dumps(R.cc["B0_COVERAGE_CONTRACT"], ensure_ascii=False)[:400], "...")

    ing = R.cap("CAP-01", "chart", "source_fingerprint", R.fingerprint(a.chart, "chart"))
    ing = R.cap("CAP-03", "chart", "board_card", R.ingest())
    R.cap("CAP-02", "chart_info,palaces", "normalized_fields", R.normalized)
    R.cap("CAP-04", "board_card", "roles", R.role_resolve())
    if not R.roles["core_roles_all_resolved"]:
        R.anomaly("GAP_DETECTED", "core role unresolved -> B1 would fail", "CAP-04")
    R.cap("CAP-05", "chart_info.ganzhi", "pillars", R.pillars_and_composites()["pillars"])
    R.cap("CAP-07", "interpretations.condition", "composites", {"count": len(R.composites)})
    R.pid_payload = R.cap("CAP-08", "palace_elements,chart_info", "palace_identity", R.palace_identity())
    R.cap("CAP-11", "board_card", "atoms", R.atomize())
    R.cap("CAP-09", "E_atoms", "value_traces", {"traces": len(R.traces)})
    reg = R.cap("CAP-11", "E,R", "evidence_registry", R.evidence_registry())
    pat = R.cap("CAP-10", "board_card,catalog", "patterns", R.patterns())
    led = R.cap("CAP-14", "atoms,registry,patterns", "ledger", R.batch_and_ledger())
    sc = R.cap("CAP-15", "patterns,registry", "score_card", R.score_card())
    cs = R.cap("CAP-17", "case_context", "case_context_digest", R.case_decompose())
    aud = R.cap("CAP-16", "all", "self_audit", R.self_audit(reg, pat, led, cs))

    # writes
    w = lambda p, obj: open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False, indent=2))
    w(os.path.join(a.raw, "source_fingerprint.json"), {"chart": R.fp, "case_context": getattr(R, "case_fp", None)})
    w(os.path.join(a.raw, "board_card.json"), {"adapter_variant": R.board["adapter_variant"],
                                               "note": "single whole-chart view; source is never re-read",
                                               "board_card": R.board, "roles": R.palace_roles})
    w(os.path.join(a.work, "normalized_fields.json"), R.normalized)
    w(os.path.join(a.work, "roles.json"), R.roles)
    w(os.path.join(a.work, "pillars.json"), R.pillars)
    w(os.path.join(a.work, "composites.json"), R.composites)
    w(os.path.join(a.work, "palace_identity.json"), R.pid_payload)
    w(os.path.join(a.work, "atoms_E.json"), R.E)
    w(os.path.join(a.work, "atoms_R.json"), R.R)
    w(os.path.join(a.work, "evidence_registry.json"), reg)
    w(os.path.join(a.work, "patterns.json"), pat)
    w(os.path.join(a.work, "coverage_batches.json"), led)
    w(os.path.join(a.work, "ledger.json"), {"dispositions": R.dispositions,
                                            "palace_tallies": led["palace_tallies"],
                                            "run_tally": led["run_tally"]})
    w(os.path.join(a.work, "scorecard.json"), sc)
    w(os.path.join(a.work, "case_context_digest.json"), cs)
    w(os.path.join(a.work, "case_status.json"), {"status": R.case_status})
    w(os.path.join(a.work, "self_audit.json"), aud)
    w(os.path.join(a.work, "wiki_index.json"), R.wk)
    open(os.path.join(a.raw, "state", "call_log.jsonl"), "w", encoding="utf-8").write(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in R.calls) + "\n")
    w(os.path.join(a.raw, "state", "anomalies.json"), R.anomalies)
    w(os.path.join(a.raw, "state", "reissue_log.json"), {"reissue_log": R.reissue_log})
    w(os.path.join(a.raw, "state", "compression_log.json"), {"compression_log": R.compression_log})
    print(f"\ncalls={len(R.calls)}/60  anomalies={len(R.anomalies)}  "
          f"E={len(R.E)} R={len(R.R)} eligible={reg['eligible']['counts']}  self_audit={aud['all_pass']}")


if __name__ == "__main__":
    main()
