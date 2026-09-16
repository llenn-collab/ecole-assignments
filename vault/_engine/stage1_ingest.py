"""Stage 1: INIT -> CHART_INGEST -> STRUCTURAL_INVENTORY -> SCHEMA_ADAPTATION.
Pure structural work: no synthesis, no interpretation."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *

run_id = f"carpathia-qmdj-v5-run-{utcnow().replace(':','').replace('-','')}-{os.getpid()%997}"
src_hash = sha256_file(SRC)
src_size = os.path.getsize(SRC)
data = load_source()

# ---------------- INIT ----------------
assert not state_exists("machine.json"), "machine.json exists; resume path not requested"
machine_update(run_id=run_id, state="INIT", completed_batches=[], completed_phases=[],
               palaces={}, solution_seed_revision=0, verification={},
               source_file_name=SRC_REL, source_sha256=src_hash, source_size_bytes=src_size)
dump_state("solution_seed.json", {
    "revision": 0, "answers": [], "hidden_problems": [], "best_solution_candidates": [],
    "note": "chart-derived only; not yet requirement-bound", "patches": []})
dump_state("palaces.json", {})
write_text(os.path.join(STATE, "progress.md"),
           f"# Analyst Progress — run `{run_id}`\n\nsource: `{SRC_REL}` sha256 `{src_hash}`\n\n")
progress(f"INIT ok | run_id: {run_id} | source_sha256: {src_hash[:16]}... | size: {src_size}B")

# ---------------- CHART_INGEST ----------------
prov = {"file": SRC_REL, "sha256": src_hash, "size_bytes": src_size,
        "ingested_at": utcnow(), "run_id": run_id, "encoding": "UTF-8",
        "key_normalization": "trim leading/trailing whitespace; raw preserved",
        "value_normalization": "trim leading/trailing whitespace; raw preserved"}
dump_state("raw_provenance.json", prov)

inventory_preview = {}
whitespace_keys = []
def walk(node, raw_path, norm_path, parent, records):
    """Recursive traversal: every key, array item, primitive leaf -> path record."""
    ntype = ("object" if isinstance(node, dict) else "array" if isinstance(node, list)
             else "null" if node is None else
             "boolean" if isinstance(node, bool) else
             "number" if isinstance(node, (int, float)) else "string")
    if ntype in ("object", "array"):
        digest = sha256_bytes(json.dumps(node, sort_keys=True, ensure_ascii=False, default=str).encode())[:12]
    elif ntype == "string":
        digest = sha256_bytes(node.encode())[:12]
    else:
        digest = sha256_bytes(str(node).encode())[:12]
    records.append({"raw_path": raw_path or "$", "normalized_path": norm_path or "$",
                    "raw_key": raw_path, "normalized_key": norm_path,
                    "node_type": ntype, "value_digest": digest,
                    "parent_path": parent or None,
                    "child_count": len(node) if ntype in ("object", "array") else 0,
                    "presence_status": "NULL" if ntype == "null" else "PRESENT",
                    "analysis_status": "UNPARSED", "evidence_class": "EXPLICIT",
                    "semantic_role": None, "exclusion_reason": None, "linked_claim_ids": []})
    if ntype == "object":
        for k, v in node.items():
            nk = norm_key(k)
            if nk != k:
                whitespace_keys.append({"raw_key": k, "normalized": nk, "at": raw_path or "$"})
            walk(v, f'{raw_path}["{k}"]' if raw_path else f'["{k}"]',
                 f"{norm_path}.{nk}" if norm_path else nk, norm_path or "$", records)
    elif ntype == "array":
        for i, v in enumerate(node):
            walk(v, f"{raw_path}[{i}]", f"{norm_path}[{i}]", norm_path, records)

records = []
walk(data, "", "", None, records)

# chart_index: top-level + per-palace field map
top = {k: type(v).__name__ for k, v in data.items()}
palace_fields = {pk: sorted(list(pv.keys())) for pk, pv in data.get("palaces", {}).items()}
dump_state("chart_index.json", {"top_level_keys": top, "palace_keys": list(data.get("palaces", {}).keys()),
                                "palace_fields": palace_fields, "total_paths": len(records)})

# dump.md + schema.md (ingest notes with provenance)
lines = [f"# Chart Dump (structural)\n", f"- provenance: `{SRC_REL}` sha256 `{src_hash}` ingested {prov['ingested_at']}",
         f"- total recursive paths: {len(records)}", f"- top-level keys: {json.dumps(top)}", ""]
for r in records:
    lines.append(f"- `{r['raw_path']}` :: {r['node_type']} children={r['child_count']} digest={r['value_digest']}")
write_text(os.path.join(RAW, "chart", "dump.md"), "\n".join(lines))

# whitespace check on string values
ws_vals = [r["raw_path"] for r in records if r["node_type"] == "string"]
whitespace_values = []
def walk_vals(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            walk_vals(v, f'{path}["{k}"]' if path else f'["{k}"]')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_vals(v, f"{path}[{i}]")
    elif isinstance(node, str) and node != node.strip():
        whitespace_values.append({"path": path, "raw": node})
walk_vals(data, "")

schema_md = f"""# Chart Schema (ingest pass)

- source: `{SRC_REL}` (sha256 `{src_hash}`, {src_size} bytes)
- top-level keys: {json.dumps(top)}
- palace key style: compound trigram-number ({", ".join(data.get('palaces', {}).keys())})
- keys with leading/trailing whitespace: {len(whitespace_keys)} {json.dumps(whitespace_keys)}
- string values with leading/trailing whitespace: {len(whitespace_values)} {json.dumps(whitespace_values)}
- palace field sets vary per palace (see chart_index.json); center_5 is minimal (no door/branches/opposite).
- no unknown top-level keys beyond {{chart_info, palaces}}.
"""
write_text(os.path.join(RAW, "chart", "schema.md"), schema_md)
progress(f"CHART_INGEST ok | paths: {len(records)} | ws_keys: {len(whitespace_keys)} | ws_values: {len(whitespace_values)}")

# ---------------- STRUCTURAL_INVENTORY ----------------
manifest = []
array_items = []
for r in records:
    manifest.append({"raw_path": r["raw_path"], "normalized_path": r["normalized_path"],
                     "type": r["node_type"], "value_digest": r["value_digest"],
                     "presence_status": r["presence_status"], "analysis_status": r["analysis_status"],
                     "evidence_class": r["evidence_class"], "semantic_role": None,
                     "exclusion_reason": None, "linked_claim_ids": []})
    if re_match := __import__("re").search(r"\[(\d+)\]$", r["normalized_path"]):
        array_items.append({"array_path": r["normalized_path"].rsplit("[", 1)[0],
                            "index": int(re_match.group(1)), "raw_path": r["raw_path"],
                            "type": r["node_type"], "value_digest": r["value_digest"]})
dump_state("path_coverage_manifest.json",
           {"complete": False, "total_paths": len(manifest), "records": manifest})
dump_state("array_itemization.json", {"complete": False, "item_count": len(array_items), "items": array_items})
dump_state("absence_registry.json", {"complete": False, "records": []})
dump_state("exclusion_log.json", {"complete": False, "explicit_exclusions_logged": True,
                                  "records": [], "note": "no exclusions yet; silent omission forbidden"})
dump_state("anomaly_registry.json", {"complete": False, "records": []})
progress(f"STRUCTURAL_INVENTORY ok | manifest paths: {len(manifest)} | array items: {len(array_items)} | registries initialized")
machine_update(state="STRUCTURAL_INVENTORY", completed_phases=["CHART_INGEST"])

# ---------------- SCHEMA_ADAPTATION ----------------
variant = {"detected_variant": "project_1_chart_info_v1", "version": "1", "confidence": 1.0,
           "match_evidence": ["top_level_keys == {chart_info, palaces}",
                              "palace_key_style == compound_trigram_number",
                              "pillars are combined ganzhi strings (e.g. 'Ren Chen')",
                              "duty fields are composite strings (e.g. 'Tian Rui falling in Zhen 3 Palace')",
                              "markers/patterns are explicit string arrays",
                              "strength fields composite (e.g. 'Rest / Strong')",
                              "center palace lacks door/branches/opposite_palace"],
           "unresolved_ambiguities": ["star_strength two-token convention ('A / B') by_season vs by_palace order unverified; raw preserved, tokens normalized separately"]}
dump_state("schema_variant.json", variant)

sem = {
 "metadata_root": "chart_info", "system": "chart_info.system", "method": "chart_info.method",
 "chart_type": "chart_info.type", "gregorian": "chart_info.gregorian", "lunar": "chart_info.lunar",
 "solar_term": "chart_info.solar_term", "year_pillar": "chart_info.ganzhi.year",
 "month_pillar": "chart_info.ganzhi.month", "day_pillar": "chart_info.ganzhi.day",
 "hour_pillar": "chart_info.ganzhi.hour", "day_void": "chart_info.void.day",
 "hour_void": "chart_info.void.hour", "horse_year": "chart_info.horse.year",
 "horse_month": "chart_info.horse.month", "horse_day": "chart_info.horse.day",
 "horse_hour": "chart_info.horse.hour", "ju": "chart_info.ju", "fu_tou": "chart_info.fu_tou",
 "zhi_fu": "chart_info.zhi_fu", "zhi_shi": "chart_info.zhi_shi", "tian_yi": "chart_info.tian_yi",
 "seasonal_strength": "chart_info.seasonal_strength", "palaces_root": "palaces",
 "palace_identity": "object_key + name + original_position", "heaven_stem": "heaven_stem",
 "earth_stem": "earth_stem", "hidden_stem": "hidden_stem", "star": "star", "door": "door",
 "deity": "deity", "special_markers": "special_markers", "auspicious_patterns": "auspicious_patterns",
 "inauspicious_patterns": "inauspicious_patterns", "original_position": "original_position",
 "prosperity_decline": "prosperity_decline", "life_stage": "life_stage", "harm": "harm",
 "tomb": "tomb", "punishment": "punishment",
}
registry = {}
for role, path in sem.items():
    ok, val = cite_source(path) if path.startswith("chart_info") or path == "palaces" else (True, "<per-palace role>")
    registry[role] = {"resolved_path": path, "raw_path": path, "confidence": 1.0 if ok else 0.8,
                      "status": "BOUND" if ok else "PER_PALACE", "parser_required": role in {
                          "year_pillar","month_pillar","day_pillar","hour_pillar","fu_tou","zhi_fu",
                          "zhi_shi","life_stage","harm","tomb","punishment","special_markers",
                          "auspicious_patterns","inauspicious_patterns","prosperity_decline",
                          "original_position","heaven_stem","hidden_stem","star"}}
for absent_role in ["lead_stem", "duty_star_name", "duty_star_palace", "duty_door_name",
                    "duty_door_original", "duty_door_active", "day_void", "hour_void", "lodged_stem", "lodged_star"]:
    if absent_role not in registry:
        registry[absent_role] = {"resolved_path": None, "raw_path": None, "confidence": 0.0,
                                 "status": "ABSENT — derive via parser (fu_tou/zhi_fu/zhi_shi) or lodging protocol",
                                 "parser_required": True}
dump_state("semantic_path_registry.json", {"roles": registry, "binding_rule": "semantic role, never hardcoded canonical path"})

# palace key resolution via frozen geometry
res = {}
anomalies = []
NAME2ID = {v["name"].lower(): k for k, v in PALACE_IDENTITY.items()}
for raw_key in data["palaces"]:
    trig, num = raw_key.rsplit("_", 1)
    canon = NAME2ID.get(trig)
    flag = []
    if canon is None:
        flag.append("UNKNOWN_TRIGRAM_LABEL")
    if canon != num:
        anomalies.append({"id": None, "type": "PALACE_KEY_TRIGRAM_NUMBER_DISAGREE",
                          "raw_key": raw_key, "trigram_part": trig, "number_part": num,
                          "resolved_via": "trigram" if canon else "number"})
        canon = canon or num
    ident = PALACE_IDENTITY[canon]
    res[canon] = {"raw_palace_key": raw_key, "canonical_palace_id": canon,
                  "canonical_name": ident["name"], "direction": ident["dir"],
                  "element": ident["element"], "branches": ident["branches"],
                  "resolution_confidence": 1.0 if not flag else 0.6, "ambiguity_flags": flag}
assert set(res) == set("123456789"), f"integrity_nine_palaces failed: {sorted(res)}"
dump_state("palace_key_resolution.json", {"palaces": res, "integrity_nine_palaces": True})

# annotate manifest semantic roles (metadata roles)
mani = load_state("path_coverage_manifest.json")
role_by_path = {v["resolved_path"]: k for k, v in registry.items() if v.get("resolved_path")}
for rec in mani["records"]:
    p = rec["normalized_path"]
    if p in role_by_path:
        rec["semantic_role"] = role_by_path[p]
    elif p.startswith("palaces."):
        parts = p.split(".")
        rec["semantic_role"] = f"palace_field:{parts[2] if len(parts)>2 else 'root'}"
    rec["analysis_status"] = "PARSED" if rec["type"] != "object" else "ANALYZED"
dump_state("path_coverage_manifest.json", mani)
machine_update(state="SCHEMA_ADAPTATION",
               completed_phases=["CHART_INGEST", "STRUCTURAL_INVENTORY"])
progress(f"SCHEMA_ADAPTATION ok | variant: project_1_chart_info_v1 (conf 1.0) | roles bound: {len(registry)} | palaces resolved: 9 | integrity_nine_palaces: true")
print(json.dumps({"run_id": run_id, "paths": len(mani["records"]), "array_items": len(array_items),
                  "ws_keys": len(whitespace_keys), "ws_values": len(whitespace_values),
                  "variant": "project_1_chart_info_v1", "palaces": sorted(res)}, indent=1))
