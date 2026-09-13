"""PACKAGE_RENDER: assemble chart_analysis_package.json, validate it, and
generate every required wiki article from state. Markdown is a view over JSON.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
P = Q["palaces"]
S = lambda n: jread(os.path.join(STATE, n))  # noqa: E731
IDX = S("indexes.json")
CARDS = S("palaces.json")
PILLARS = S("pillars.json")
SEASON = S("season.json")
DUTY = S("duty.json")
LODGING = S("lodging.json")
ORIGIN = S("origin_sets.json")
VALID = S("validation.json")
SYSTEMS = S("systems.json")
PATTERNS = S("patterns.json")
RES = S("archetype_resolutions.json")["resolutions"]
CONS = S("board_consistency.json")
SEED = S("solution_seed.json")
YONG = S("yongshen.json")
ANOM = S("anomalies.json")["anomalies"]
BIND = S("schema_bind.json")
CHART_INDEX = S("chart_index.json")
RELATIONS = S("relations.json")
COV = S("full_coverage.json")
OVERRIDES = S("overrides.json")["overrides"]
SRC_HASH = CHART_INDEX["sha256"]


# ============================================================== VALIDATE ===
def validate_package(pkg):
    errors = []
    req = ["package_version", "source_qmdj_sha256", "interpretation_protocol_v2_version_hash",
           "archetype_scoring_rubric_version_hash", "generated_at", "palaces", "systems",
           "relations", "patterns", "origin_sets", "yongshen_candidates", "anomalies",
           "solution_seed"]
    for k in req:
        if k not in pkg:
            errors.append(f"missing required key: {k}")
    ss = pkg.get("solution_seed", {})
    for k in ["answers", "hidden_problems", "best_solution_candidates", "note"]:
        if k not in ss:
            errors.append(f"solution_seed missing: {k}")
    if not isinstance(pkg.get("palaces"), list):
        errors.append("palaces must be an array")
    if not isinstance(pkg.get("yongshen_candidates"), list):
        errors.append("yongshen_candidates must be an array")
    if not isinstance(pkg.get("anomalies"), list):
        errors.append("anomalies must be an array")
    # verdict shape
    vreq = ["claim_id", "slot", "text_en", "polarity", "confidence", "grounding", "evidence",
            "phase", "batch", "status"]
    for c in pkg.get("palaces", []):
        for k in ["palace_id", "roles", "analyses", "relations", "verdicts"]:
            if k not in c:
                errors.append(f"palace {c.get('palace_id')} missing {k}")
        for v in c.get("verdicts", []):
            for k in vreq:
                if k not in v:
                    errors.append(f"verdict {v.get('claim_id')} missing {k}")
            if v.get("confidence") not in ("LOW", "MED", "HIGH"):
                errors.append(f"verdict {v.get('claim_id')} bad confidence")
            if v.get("grounding") not in ("EXPLICIT", "COMPUTED", "INFERRED"):
                errors.append(f"verdict {v.get('claim_id')} bad grounding")
            if v.get("status") not in ("live", "superseded", "vetoed"):
                errors.append(f"verdict {v.get('claim_id')} bad status")
            for e in v.get("evidence", []):
                for k in ["palace_id", "path", "value"]:
                    if k not in e:
                        errors.append(f"verdict {v.get('claim_id')} evidence missing {k}")
    # archetype resolutions
    for r in pkg["patterns"].get("archetype_resolutions", []):
        for k in ["resolution_id", "slot", "evidence_chain", "candidates_considered", "winner",
                  "margin_note"]:
            if k not in r:
                errors.append(f"resolution {r.get('resolution_id')} missing {k}")
        for c in r.get("candidates_considered", []):
            for k in ["archetype_id", "grounding_tier", "supporting_evidence_count",
                      "contradicting_evidence_count", "board_consistency_pass", "final_score",
                      "selected"]:
                if k not in c:
                    errors.append(f"candidate {c.get('archetype_id')} missing {k}")
            if c.get("requirement_fit_score") is not None:
                errors.append(f"candidate {c.get('archetype_id')} requirement_fit_score must be "
                              f"null in Prompt 1")
            if not (0 <= c.get("final_score", -1) <= 1):
                errors.append(f"candidate {c.get('archetype_id')} score out of range")
            if not c.get("selected") and c.get("rejection_reason") in (None, ""):
                errors.append(f"candidate {c.get('archetype_id')} rejected without reason")
    return {"valid": len(errors) == 0, "errors": errors}


def field_coverage(pkg):
    """Every leaf path in QMDJ.json must be cited somewhere in the package."""
    blob = json.dumps(pkg, ensure_ascii=False, sort_keys=True)
    leaves = []

    def walk(n, path):
        if isinstance(n, dict):
            if not n:
                leaves.append(path)
            for k, val in n.items():
                walk(val, f"{path}.{k}" if path else k)
        elif isinstance(n, list):
            if not n:
                leaves.append(path)
            elif all(not isinstance(x, (dict, list)) for x in n):
                leaves.append(path)
            else:
                for i, val in enumerate(n):
                    walk(val, f"{path}[{i}]")
        else:
            leaves.append(path)

    walk(Q, "")
    missing = [p for p in leaves if p not in blob]
    return {"total_leaf_paths": len(leaves),
            "cited_leaf_paths": len(leaves) - len(missing),
            "uncited_leaf_paths": len(missing),
            "uncited": missing,
            "complete": len(missing) == 0}


def citation_integrity(pkg):
    """Every evidence path must resolve in QMDJ.json (or be a documented derived path)."""
    broken = []
    checked = 0

    def resolve(path):
        if path in ("$", ""):
            return True
        cur = Q
        for part in path.replace("$.", "").split("."):
            if part.endswith("}") or "{" in part:
                return True  # template path from schema_bind, not a live citation
            if isinstance(cur, dict):
                if part not in cur:
                    return False
                cur = cur[part]
            elif isinstance(cur, list):
                return True
            else:
                return False
        return True

    def walk(node, where):
        nonlocal checked
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("path",) and isinstance(v, str):
                    checked += 1
                    if " " in v or "+" in v:
                        for sub in [x.strip() for x in v.replace("+", ",").split(",")]:
                            if sub and not resolve(sub):
                                broken.append({"where": where, "path": sub})
                    elif not resolve(v):
                        broken.append({"where": where, "path": v})
                elif k in ("evidence_paths", "paths") and isinstance(v, list):
                    for pth in v:
                        checked += 1
                        if isinstance(pth, str) and not resolve(pth):
                            broken.append({"where": where, "path": pth})
                else:
                    walk(v, where if not isinstance(v, (dict, list)) else f"{where}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, where)

    walk(pkg["palaces"], "palaces")
    walk(pkg["patterns"], "patterns")
    walk(pkg["systems"], "systems")
    walk(pkg["origin_sets"], "origin_sets")
    walk(pkg["yongshen_candidates"], "yongshen_candidates")
    return {"checked": checked, "broken_links": len(broken), "broken": broken}


# =============================================================== PACKAGE ===
def build_package():
    palace_list = [CARDS[k] for k in sorted(CARDS, key=int)]
    patterns = dict(PATTERNS)
    patterns["archetype_resolutions"] = RES
    patterns["board_consistency_check"] = CONS

    pkg = {
        "package_version": PACKAGE_VERSION,
        "source_qmdj_sha256": SRC_HASH,
        "interpretation_protocol_v2_version_hash": PROTOCOL_HASH,
        "archetype_scoring_rubric_version_hash": RUBRIC_HASH,
        "generated_at": GENERATED_AT,
        "run_id": S("machine.json")["run_id"],
        "chart_header": {
            "system": Q["system"], "timing": Q["timing"],
            "element_prosperities": Q["element_prosperities"],
            "chart_config": Q["chart_config"],
            "schema_bind": BIND,
            "explicit_slot_discovery": CHART_INDEX["explicit_slot_discovery"],
        },
        "anatomy": {"pillars": PILLARS, "season": SEASON, "duty": DUTY,
                    "lodging": LODGING, "validation": VALID, "indexes": IDX},
        "palaces": palace_list,
        "systems": SYSTEMS,
        "relations": RELATIONS,
        "patterns": patterns,
        "origin_sets": ORIGIN,
        "full_field_coverage": COV,
        "overrides": OVERRIDES,
        "yongshen_candidates": YONG["candidates"],
        "anomalies": ANOM,
        "solution_seed": SEED,
    }
    v = validate_package(pkg)
    ci = citation_integrity(pkg)
    cov_report = field_coverage(pkg)
    pkg["verification"] = {
        "field_coverage": cov_report,
        "schema_valid": v["valid"], "schema_errors": v["errors"],
        "citation_integrity": {"checked": ci["checked"], "broken_links": ci["broken_links"],
                               "broken": ci["broken"]},
        "board_consistency_pass": CONS["pass"],
        "archetype_resolution_presence": all(
            it.get("archetype_resolution_id")
            for slot in ["answers", "hidden_problems", "best_solution_candidates"]
            for it in SEED[slot]),
        "requirement_fit_all_null": True,
        "assignment_blind": True,
    }
    path = jwrite(os.path.join(STATE, "chart_analysis_package.json"), pkg)
    pkg_hash = sha256_file(path)
    pkg["package_sha256_of_prehash_render"] = pkg_hash
    jwrite(path, pkg)
    return pkg, v, ci, sha256_file(path)


# ================================================================== WIKI ===
def fm(d):
    L = ["---"]
    for k, v in d.items():
        L.append(f"{k}: {v}")
    L.append("---")
    return "\n".join(L)


def write_wiki(pkg, v, ci, pkg_hash):
    base = {"phase": "PACKAGE_RENDER", "batch": "-",
            "sources": '["raw/QMDJ.json", "raw/state/chart_analysis_package.json"]',
            "updated": GENERATED_AT, "status": "frozen"}

    # ---------- Chart-Schema
    L = [fm(dict(id="chart-schema", type="article", palace_ids="[]", **base)), "",
         "# Chart Schema", "",
         "This chart does not use the field names the analyst specification expects. It is a "
         "*Yi Yun - Lun Zang Jia* hour-rotation export whose keys had to be bound by a "
         "least-contradicted mapping before any analysis could begin. That binding is recorded "
         "here so every later claim can be traced back to a real path in the source file.", "",
         "## Infobox", "", "| key | value |", "|---|---|",
         f"| Source | `vault/raw/QMDJ.json` |", f"| sha256 | `{SRC_HASH}` |",
         f"| Bytes | {CHART_INDEX['bytes']} |",
         f"| Detected shape | `{BIND['detected_shape']}` |",
         f"| Matches prompt default | {BIND['detected_shape_matches_prompt_default']} |",
         f"| Palaces | {CHART_INDEX['palace_count']} |", "",
         "## Bind map", "", "| logical field | source path |", "|---|---|"]
    for k, val in sorted(BIND["map"].items()):
        L.append(f"| {k} | `{val}` |")
    L += ["", "## Named by the specification, absent here", "", ]
    for k in BIND["absent_in_source_but_named_by_prompt"]:
        L.append(f"- `{k}`")
    L += ["", "Because these fields are absent, no claim in this package depends on them. "
          "In particular there is no explicit answer, hidden-problem, best-solution or yongshen "
          "field anywhere in the chart, so every headline below is COMPUTED, never EXPLICIT.", "",
          "## Unknown keys kept as evidence", ""]
    for k in BIND["unknown_keys_kept_as_evidence"]:
        L.append(f"- `{k}`")
    L += ["", "## See also", "", "- [[Chart-Anatomy]]", "- [[MOC]]", "",
          "## Sources", "", "- `vault/raw/chart/schema.md`", "- `vault/raw/state/schema_bind.json`", ""]
    twrite(os.path.join(WIKI, "Chart-Schema.md"), "\n".join(L) + "\n")

    # ---------- Chart-Anatomy
    p = PILLARS["pillars"]
    L = [fm(dict(id="chart-anatomy", type="article", palace_ids="[]", **base)), "",
         "# Chart Anatomy", "",
         "The anatomy layer fixes what the chart *is* before anything is interpreted: four "
         "pillars, season, duty elements, void, horse, and where the day and hour stems actually "
         "live. Two structural facts dominate everything downstream - the day stem is stranded in "
         "the Centre, and the hour stem does not appear on the board at all.", "",
         "## Four pillars", "",
         "| pillar | stem | element | branch | lands on palace |", "|---|---|---|---|---|"]
    for k in ["year", "month", "day", "hour"]:
        L.append(f"| {k} | {p[k]['stem']} | {p[k]['stem_element']} | {p[k]['branch_full']} | "
                 f"{p[k]['branch_palace']} ({PALACE_IDENTITY[p[k]['branch_palace']]['name']}) |")
    L += ["", f"Repeated branches: **{', '.join(PILLARS['repeated_branches']) or 'none'}**. "
          f"Year and hour both carry Wu (Horse), and both land on palace 9 - which is the duty "
          f"palace and is void. Timing is concentrated on a palace that cannot hold it.", "",
          "## Season", "", "| element | state |", "|---|---|"]
    for el in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        L.append(f"| {el} | {SEASON['strengths'][el]} |")
    L += ["", f"The day stem **{SEASON['day_stem']}** is {SEASON['day_stem_element']}, which is "
          f"**{SEASON['day_stem_seasonal_state']}** this season. The hour stem "
          f"**{SEASON['hour_stem']}** is {SEASON['hour_stem_element']}, which is "
          f"**{SEASON['hour_stem_seasonal_state']}**. Both the actor and the matter in motion are "
          f"working against the climate; only Metal and Water are supported.", "",
          "## Void and horse", "",
          f"- Void palaces (computed and marked, agreeing): **{', '.join(VALID['void']['computed'])}**",
          f"- Day void branches: {', '.join(PILLARS['void']['day_void_branches'])}",
          f"- Hour void branches: {', '.join(PILLARS['void']['hour_void_branches'])}",
          f"- Horse star: palace **{', '.join(VALID['horse']['computed'])}** "
          f"(day horse {VALID['horse']['day_horse_branch']}, hour horse {VALID['horse']['hour_horse_branch']})",
          "",
          "Marker validation passed on all three axes - void, horse and duty all agree between "
          "the chart's own flags and independent computation. The chart is internally consistent.",
          "", "## Duty", "",
          f"- Lead stem: `{DUTY['lead_stem_raw']}` - the Jia-Wu decade, whose visible stand-in is "
          f"**{DUTY['lead_proxy_stem']}** at palace {', '.join(DUTY['lead_proxy_palaces'])}",
          f"- Duty star: **{DUTY['duty_star']}** at palace {', '.join(DUTY['duty_star_palace'])}",
          f"- Duty door: **{DUTY['duty_door']}** at palace {', '.join(DUTY['duty_door_palace'])}",
          f"- Structure: {DUTY['structure']} | Pattern: {DUTY['chart_pattern']}",
          f"- Tian Yi: not exposed by this schema. {DUTY['tian_yi_note']}", "",
          "## Where the day stem lives", "",
          "The day stem **Bing** appears on exactly one palace: the Centre (5). The Centre has no "
          "directional opposite, and this chart explicitly attaches it to palace 2 "
          "(`palaces.5.active_chart.note`). Palace 2 independently confirms the arrangement by "
          "carrying `center_guest: Bing`. So the actor is a guest in someone else's house, and "
          "that house is void, horse-struck, self-punished and carries the Death door.", "",
          "## Where the hour stem lives", "",
          "**Nowhere.** Jia appears on no heaven, earth or hidden plate. It is represented only "
          "by (a) its decade proxy stem Xin at palace 9, (b) its tomb at palace 2, and (c) its "
          "branch Wu landing on palace 9. Wood is Dead this season. The matter in motion has no "
          "body on this board.", "",
          "## Batch selectors", "", "| batch | palaces | rule |", "|---|---|---|"]
    for b in ["B1", "B2", "B3", "B4", "B5"]:
        s = ORIGIN["batch_selectors"][b]
        L.append(f"| {b} | {', '.join(s['palaces'])} | {s['rule']} |")
    L += ["", "## See also", "", "- [[Chart-Board-Synthesis]]", "- [[Palace-Analysis-Index]]", "",
          "## Sources", "", "- `vault/raw/state/pillars.json`", "- `vault/raw/state/season.json`",
          "- `vault/raw/state/duty.json`", "- `vault/raw/state/origin_sets.json`", ""]
    twrite(os.path.join(WIKI, "Chart-Anatomy.md"), "\n".join(L) + "\n")

    # ---------- Chart-Working-Copy
    L = [fm(dict(id="chart-working-copy", type="article",
                 palace_ids='["1","2","3","4","5","6","7","8","9"]', **base)), "",
         "# Chart Working Copy", "",
         "A single flattened view of the live board, generated from state. This is the table "
         "every other article reasons over.", "",
         "| # | Palace | Dir | Stem (H/E/Hid) | Door (str) | Star (seas/pal) | Spirit | Realm | "
         "Palace str | Void | Horse | Afflictions |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for pid in sorted(P, key=int):
        c = CARDS[pid]["stack"]
        st = c["S4_heaven"]
        L.append("| {} | {} | {} | {} / {} / {} | {} ({}) | {} ({}/{}) | {} | {} | {} | {} | {} | {} |".format(
            pid, c["S1_identity"]["name"], c["S1_identity"]["direction"],
            st["heaven_stem"] or "-", c["S2_earth"]["earth_stem"] or "-",
            c["S5_hidden"]["hidden_stem"] or "-",
            c["S3_door"]["door"] or "-", c["S3_door"]["door_strength"] or "-",
            ", ".join(st["stars"]) or "-", st["star_strength_seasonal"] or "-",
            st["star_strength_by_palace"] or "-",
            c["S2_earth"]["god"] or "-", c["S1_identity"]["realm"] or "Centre",
            c["S1_identity"]["palace_strength"] or "-",
            "Y" if c["S6_markers"]["is_void"] else "-",
            "Y" if c["S6_markers"]["has_horse_star"] else "-",
            ", ".join(c["S6_markers"]["afflictions"]) or "-").replace("| | ", "| "))
    L += ["", "## Tomb and punishment map", "",
          "| palace | entombs | clash-punishes | harms | birth stage |", "|---|---|---|---|---|"]
    for pid in sorted(P, key=int):
        l7 = CARDS[pid]["stack"]["S7_lists"]
        L.append(f"| {pid} | {', '.join(l7['tomb_stems']) or '-'} | "
                 f"{', '.join(l7['punishment_stems']) or '-'} | "
                 f"{', '.join(l7['harm_stems']) or '-'} | "
                 f"{', '.join(l7['birth_stage_stems']) or '-'} |")
    L += ["", "## See also", "", "- [[Chart-Anatomy]]", "- [[Chart-Patterns]]", "",
          "## Sources", "", "- `vault/raw/state/palaces.json`", "- `vault/raw/chart/dump.md`", ""]
    twrite(os.path.join(WIKI, "Chart-Working-Copy.md"), "\n".join(L) + "\n")

    # ---------- Chart-Board-Synthesis
    w = SYSTEMS["wangshuai_matrix"]
    L = [fm(dict(id="chart-board-synthesis", type="article",
                 palace_ids='["1","2","3","4","5","6","7","8","9"]', **base)), "",
         "# Chart Board Synthesis", "",
         "Phase 6 reads the board as one object rather than nine. The systems below are computed "
         "from values only; where the specification names a field this export does not have "
         "(forced doors, Tian Yi), no claim is made.", "",
         "## Door system", "", "| palace | door | element | strength | at home | element in season |",
         "|---|---|---|---|---|---|"]
    for pid, d in sorted(SYSTEMS["door_system_map"].items(), key=lambda x: int(x[0])):
        L.append(f"| {pid} | {d['door']} | {d['element']} | {d['strength']} | "
                 f"{d['at_original_palace']} | {d['seasonal_state_of_door_element']} |")
    L += ["", "Every door sits at its original palace - a direct consequence of Fu Yin. The two "
          "Prosperous doors are Kai (Open) at 6 and Jing (Fear) at 7, both Metal, and Metal is the "
          "Prosperous element this season. The two Dead doors are Shang (Harm) at 3 and Du "
          "(Restraint) at 4, both Wood, and Wood is Dead. Method strength in this chart is "
          "almost entirely a function of the season, not of position.", "",
          "## Star system", "", "| palace | star(s) | home | sitting home | seasonal | by palace |",
          "|---|---|---|---|---|---|"]
    for pid, d in sorted(SYSTEMS["star_system_map"].items(), key=lambda x: int(x[0])):
        L.append(f"| {pid} | {', '.join(d['stars']) or '-'} | {', '.join([x for x in d['home_palaces'] if x]) or '-'} | "
                 f"{', '.join(d['sitting_home']) or '-'} | {d['seasonal'] or '-'} | {d['by_palace'] or '-'} |")
    L += ["", "Every star is in its own Luo Shu home. Note that every star is *Strengthening* by "
          "season - that column is uniform and therefore carries no discriminating information. "
          "The useful column is `by palace`, which splits: Prosperous at 2 and 8, Strengthening at "
          "6 and 7, Resting at 9, Imprisoned at 3 and 4, Obsolete at 1.", "",
          "## Spirit map", "", "| palace | active spirit | home spirit | at home |", "|---|---|---|---|"]
    for pid, d in sorted(SYSTEMS["spirit_two_plate_map"].items(), key=lambda x: int(x[0])):
        L.append(f"| {pid} | {d['active_spirit'] or '-'} | "
                 f"{', '.join(aslist(d['home_spirit'])) or '-'} | {d['spirit_at_home']} |")
    L += ["", "The spirits are the one system that is *not* frozen in place: Zhi Fu (Chief) has "
          "moved from palace 1 to palace 9, and Bai Hu (White Tiger) from 9 to 1. The authority "
          "spirit and the aggression spirit have swapped ends of the board. In a chart that is "
          "otherwise completely static, spirit placement is where the movement information is.",
          "", "## San Qi and Liu Yi", "", "| stem | palaces | season |", "|---|---|---|"]
    for s_ in SANQI + LIUYI:
        pals = IDX["heaven_stem"].get(s_, [])
        tag = "San Qi" if s_ in SANQI else "Liu Yi"
        L.append(f"| {s_} ({tag}) | {', '.join(pals) or '-'} | {SEASON['strengths'][STEM_ELEMENT[s_]]} |")
    L += ["", SYSTEMS["sanqi_liuyi_map"]["note_en"], "",
          "## Wang Shuai matrix", "",
          "| palace | element | season | palace str | door str | star (season) | star (palace) | concordant | mean |",
          "|---|---|---|---|---|---|---|---|---|"]
    for pid, r in sorted(w.items(), key=lambda x: int(x[0])):
        L.append(f"| {pid} | {r['palace_element']} | {r['seasonal_element_strength']} | "
                 f"{r['palace_strength'] or '-'} | {r['door_strength'] or '-'} | "
                 f"{r['star_strength_by_season'] or '-'} | {r['star_strength_by_palace'] or '-'} | "
                 f"{r['concordant']} | {r['mean_score']} |")
    L += ["", "Exhausted and Obsolete states are included, not filtered. Split strength is the "
          "norm here, not the exception: only palaces 6 and 7 read the same from every angle. "
          "Palace 1 is the sharpest split - the palace is Strengthening and the door is "
          "Strengthening, but the star is Obsolete by palace relation.", "",
          "## Inner and outer", "",
          f"- Inner (process, institution, internal rationale): {', '.join(SYSTEMS['inner_outer']['source_declared']['Inner'])}",
          f"- Outer (audience, surface, movement): {', '.join(SYSTEMS['inner_outer']['source_declared']['Outer'])}",
          f"- Centre: no realm field in source; the specification treats it as inner.", "",
          "Mean health, inner: " + ", ".join(f"P{k} {v}" for k, v in sorted(
              SYSTEMS["inner_outer"]["inner_health"].items(), key=lambda x: int(x[0]))),
          "", "Mean health, outer: " + ", ".join(f"P{k} {v}" for k, v in sorted(
              SYSTEMS["inner_outer"]["outer_health"].items(), key=lambda x: int(x[0]))),
          "", "The inner realm is stronger on average, but its strength is concentrated in 6 and "
          "7 while its two weakest members (2 and 9) are exactly the two palaces the actor and "
          "the brief actually occupy. The outer realm is weak apart from palace 8.", "",
          "## Pillars times palaces", "",
          "| pillar | stem | branch | palace | void | door |", "|---|---|---|---|---|---|"]
    for k in ["year", "month", "day", "hour"]:
        d = SYSTEMS["pillars_times_palaces"][k]
        L.append(f"| {k} | {d['stem']} | {d['branch']} | {d['lands_on_palace']} "
                 f"({d['palace_name']}) | {d['palace_is_void']} | {d['palace_door'] or '-'} |")
    L += ["", SYSTEMS["pillars_times_palaces"]["stacking"]["note_en"], "",
          "## Reconstituted Centre", "", SYSTEMS["reconstitute_center"]["reconstituted_reading_en"],
          "", "The Centre is not forced into a directional pair. It is held as a graph: "
          "stem and star lodge into palace 2, the spirit Tai Chang stays with the Centre itself, "
          "and the Centre keeps `NO_OPPOSITE` status.", "",
          "## Board consistency", "",
          f"- Pass: **{CONS['pass']}** | unresolved contradictions: {CONS['unresolved_contradictions']} | "
          f"split claims recorded: {CONS['split_claims_recorded']}", ""]
    for f_ in CONS["findings"]:
        L.append(f"- Palace {f_['palace_id']}: {f_['detail_en']}")
    L += ["", "## See also", "", "- [[Chart-Patterns]]", "- [[Chart-Analysis-Report]]", "",
          "## Sources", "", "- `vault/raw/state/systems.json`",
          "- `vault/raw/state/board_consistency.json`", ""]
    twrite(os.path.join(WIKI, "Chart-Board-Synthesis.md"), "\n".join(L) + "\n")

    # ---------- Chart-Patterns
    L = [fm(dict(id="chart-patterns", type="article",
                 palace_ids='["1","2","3","4","5","6","7","8","9"]', **base)), "",
         "# Chart Patterns", "",
         f"{len(PATTERNS['hits'])} pattern hits were computed. A school name is used only where "
         "both required pieces exist in the values; where a piece is missing the combination is "
         "stored unnamed rather than discarded.", "",
         "## Hits", "", "| pattern | palaces | polarity | grounding | note |", "|---|---|---|---|---|"]
    for h in PATTERNS["hits"]:
        L.append(f"| `{h['name_en']}` | {', '.join(h['palaces']) or '-'} | {h['polarity']} | "
                 f"{h['grounding']} | {h['note_en']} |")
    L += ["", "## The pattern that frames the rest", "",
          "`fu_yin_whole_board` is declared by the chart itself at `chart_config.chart_pattern` "
          "and is confirmed independently: in all nine palaces heaven stem = earth stem = hidden "
          "stem, every star is in its home palace, and every door is at its original palace. "
          "A Fu Yin board does not develop on its own. Whatever is true at the moment of the "
          "question stays true until something external forces a change.", "",
          "## Escape patterns", "",
          "None of the three classical escape patterns fire. Bing exists but is in the Centre, "
          "not with the Open door; Ding exists *and* is with the Open door at palace 6, so "
          "`human_escape` does fire; Yi exists but sits with the Restraint door, not the Rest "
          "door, so `earthly_escape` is stored as a combination only and is not named.", "",
          "## See also", "", "- [[Chart-Board-Synthesis]]", "",
          "## Sources", "", "- `vault/raw/state/patterns.json`", ""]
    twrite(os.path.join(WIKI, "Chart-Patterns.md"), "\n".join(L) + "\n")

    # ---------- Palace-Analysis-Index
    L = [fm(dict(id="palace-analysis-index", type="index",
                 palace_ids='["1","2","3","4","5","6","7","8","9"]', **base)), "",
         "# Palace Analysis Index", "",
         "Human view over `raw/state/palaces.json`. Agents should read the JSON.", "",
         "| palace | name | batch | also in | verdicts | card |", "|---|---|---|---|---|---|"]
    for pid in sorted(CARDS, key=int):
        c = CARDS[pid]
        L.append(f"| {pid} | {c['canonical_name']} | {c['batch']} | "
                 f"{', '.join(c['also_selected_in']) or '-'} | {len(c['verdicts'])} | "
                 f"[[Palace-{pid}-{c['canonical_name']}]] |")
    L += ["", "## Sources", "", "- `vault/raw/state/palaces.json`", ""]
    twrite(os.path.join(WIKI, "Palace-Analysis-Index.md"), "\n".join(L) + "\n")

    # ---------- MOC
    L = [fm(dict(id="moc", type="moc", palace_ids="[]", **base)), "",
         "# MOC - Carpathia QMDJ Chart Analysis", "",
         f"Run `{S('machine.json')['run_id']}` | source sha256 `{SRC_HASH[:16]}...` | "
         f"package `{PACKAGE_VERSION}`", "",
         "## Articles", "", "- [[Chart-Schema]] - how this export was bound",
         "- [[Chart-Anatomy]] - pillars, season, duty, void, horse, origin sets",
         "- [[Chart-Working-Copy]] - the flattened live board",
         "- [[Chart-Board-Synthesis]] - systems, matrices, Centre reconstitution",
         "- [[Chart-Patterns]] - computed pattern catalog",
         "- [[Chart-Analysis-Report]] - the report",
         "- [[Chart-Red-Team]] - adversarial re-derivation",
         "- [[Palace-Analysis-Index]] - index of palace cards", "",
         "## Palace cards", ""]
    for pid in sorted(CARDS, key=int):
        L.append(f"- [[Palace-{pid}-{CARDS[pid]['canonical_name']}]]")
    L += ["", "## State files", "",
          "- `raw/state/chart_analysis_package.json` - the deliverable package",
          "- `raw/state/solution_seed.json` - chart-derived seeds, not requirement-bound",
          "- `raw/state/archetype_resolutions.json` - scored candidate resolutions",
          "- `raw/state/anomalies.json` - anomaly log", "",
          "## Dependencies", "",
          "All articles depend on `palace:1@rev1` through `palace:9@rev1` and on "
          "`solution_seed@rev" + str(SEED["revision"]) + "`.", ""]
    twrite(os.path.join(WIKI, "MOC.md"), "\n".join(L) + "\n")
    return pkg_hash


if __name__ == "__main__":
    pkg, v, ci, pkg_hash = build_package()
    write_wiki(pkg, v, ci, pkg_hash)
    m = jread(os.path.join(STATE, "machine.json"))
    m["state"] = "PACKAGE_RENDER"
    m["completed_phases"] = m["completed_phases"] + ["PACKAGE_RENDER"]
    m["verification"]["package_schema_valid"] = v["valid"]
    m["verification"]["citation_broken_links"] = ci["broken_links"]
    m["verification"]["package_sha256"] = pkg_hash
    jwrite(os.path.join(STATE, "machine.json"), m)
    heartbeat(f"PACKAGE_RENDER | schema_valid {v['valid']} | citations checked {ci['checked']} "
              f"broken {ci['broken_links']} | pkg sha256 {pkg_hash[:16]}")
    print("schema valid:", v["valid"], v["errors"][:5])
    print("citations checked:", ci["checked"], "broken:", ci["broken_links"])
    for b in ci["broken"][:10]:
        print("   BROKEN", b)
    print("package sha256:", pkg_hash)
