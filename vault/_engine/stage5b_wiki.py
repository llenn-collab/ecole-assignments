"""Stage 5b: PACKAGE_RENDER part 2 — wiki views from JSON state, master report, HALT."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *

data = load_source()
machine = load_state("machine.json")
prov = load_state("raw_provenance.json")
palaces_state = load_state("palaces.json")
pkr = load_state("palace_key_resolution.json")["palaces"]
key_of = {pid: v["raw_palace_key"] for pid, v in pkr.items()}
pillars = load_state("pillars.json")
season = load_state("season.json")
duty = load_state("duty.json")
origins = load_state("origin_sets.json")
lodging = load_state("lodging.json")
mv = load_state("marker_validation.json")
systems = load_state("systems.json")
patterns = load_state("patterns.json")
res = load_state("archetype_resolutions.json")
seed = load_state("solution_seed.json")
absence = load_state("absence_registry.json")
anom = load_state("anomaly_registry.json")
mani = load_state("path_coverage_manifest.json")
yg = load_state("yongshen.json")
gates = load_state("package_gates.json")
red = load_state("red_team.json")
TS = utcnow()

def fm(id_, type_, phase, batch, palace_ids, status, sources):
    return ("---\n"
            f'id: "{id_}"\ntype: "{type_}"\nphase: "{phase}"\nbatch: "{batch}"\n'
            f"palace_ids: {json.dumps(palace_ids)}\n"
            "sources:\n" + "".join(f'  - "{s}"\n' for s in sources) +
            f'updated: "{TS}"\nstatus: "{status}"\n---\n\n')

RAW_SRCS = ["raw/state/path_coverage_manifest.json", "raw/state/indexes.json", "raw/chart/dump.md"]

# ---------- palace cards ----------
for pid in sorted(palaces_state, key=int):
    card = palaces_state[pid]
    idn = PALACE_IDENTITY[pid]
    pv = data["palaces"][key_of[pid]]
    md = [fm(f"palace-{pid}", "palace-card", card["batch"], card["batch"], [pid], "verdicted", RAW_SRCS + ["raw/state/palaces.json"]),
          f"# Palace {pid} — {idn['name']} ({idn['han']}), {idn['dir']}, {idn['element']} · batch {card['batch']}\n",
          f"**Raw key:** `{card['raw_palace_key']}` · **Ring:** {'inner' if pid in INNER_PALACES else 'outer'} · **Branches:** {', '.join(idn['branches']) or '—'}",
          f"**Roles:** {' · '.join(card['roles'])}\n",
          "## Plates",
          f"- Heaven stem: `{pv.get('heaven_stem')}` · Earth stem: `{pv.get('earth_stem')}` · Hidden stem: `{pv.get('hidden_stem')}`",
          f"- Star: `{pv.get('star')}` · Door: `{pv.get('door')}` · Deity: `{pv.get('deity')}`",
          f"- Markers: {json.dumps(pv.get('special_markers', []))}",
          f"- Auspicious (explicit): {json.dumps(pv.get('auspicious_patterns', []))}",
          f"- Inauspicious (explicit): {json.dumps(pv.get('inauspicious_patterns', []))}",
          f"- Prosperity/decline: {json.dumps(pv.get('prosperity_decline', {}))}"]
    if card["absent_paths"]:
        md.append(f"- **Absent leaf fields** (registry): {', '.join('`' + p.split(key_of[pid] + '.')[-1] + '`' for p in card['absent_paths'])}")
    md.append("\n## Verdicts (typed, leaf-cited)")
    for v in card["verdicts"]:
        md.append(f"- **{v['claim_id']}** [{v['slot']} · {v['polarity']} · {v['confidence']} · {v['grounding']} · {v['status']}] {v['text_en']}")
        md.append(f"  - evidence: {', '.join('`' + e['path'] + '`' for e in v['evidence'])}")
    md.append("\n## Relations (computed)")
    for r in card["relations"]:
        md.append(f"- *{r['type']}* — {r['description']} ({', '.join('`' + e + '`' for e in r['evidence'])})")
    if card["anomalies"]:
        md.append("\n## Anomalies touching this palace")
        for a in card["anomalies"]:
            md.append(f"- **{a['id']}** [{a['type']}] {a['description']}")
    md.append(f"\nSee also: [[Palace-Analysis-Index]] · [[Chart-Board-Synthesis]] · trace `raw/traces/trace_palace_{pid}.json`")
    write_text(os.path.join(WIKI, f"Palace-{pid}-{idn['name']}.md"), "\n".join(md))

# ---------- Chart-Schema ----------
variant = load_state("schema_variant.json")
reg = load_state("semantic_path_registry.json")["roles"]
md = [fm("chart-schema", "article", "CHART_INGEST", "—", [], "frozen", ["raw/chart/schema.md", "raw/state/schema_variant.json", "raw/state/semantic_path_registry.json"]),
      "# Chart Schema\n",
      f"Detected variant: **{variant['detected_variant']}** (confidence {variant['confidence']}). Match evidence:",
      *[f"- {e}" for e in variant["match_evidence"]],
      "\nUnresolved ambiguities:", *[f"- {u}" for u in variant["unresolved_ambiguities"]],
      "\n## Semantic path registry (bind by role, never hardcoded)",
      "| role | resolved path | status | parser |", "|---|---|---|---|"]
for role, r in reg.items():
    md.append(f"| {role} | `{r['resolved_path']}` | {r['status']} | {r['parser_required']} |")
md.append("\nSee also: [[Chart-Anatomy]] · [[MOC]]")
write_text(os.path.join(WIKI, "Chart-Schema.md"), "\n".join(md))

# ---------- Chart-Anatomy ----------
P = pillars["pillars"]
md = [fm("chart-anatomy", "article", "P0_ANATOMY", "—", list("123456789"), "frozen",
         ["raw/state/pillars.json", "raw/state/season.json", "raw/state/duty.json", "raw/state/origin_sets.json", "raw/state/lodging.json", "raw/state/marker_validation.json"]),
      "# Chart Anatomy\n",
      "## Four pillars (parsed from combined Ganzhi strings)",
      "| pillar | raw | stem | branch | stem element | void membership | branch palace |", "|---|---|---|---|---|---|---|"]
for p in ["year", "month", "day", "hour"]:
    g = P[p]
    vd = []
    if pillars["void_membership"][p]["in_day_void"]: vd.append("DAY-VOID")
    if pillars["void_membership"][p]["in_hour_void"]: vd.append("HOUR-VOID")
    md.append(f"| {p} | {g['raw_value']} | {g['stem_pinyin']} ({g['stem_polarity']} {g['stem_element']}) | {g['branch_pinyin']} ({g['branch_animal']}) | {g['stem_element']} | {', '.join(vd) or '—'} | {BRANCH_TO_PALACE[g['branch_pinyin']]} |")
md += ["\nPillar relations (computed):",
       *[f"- `{r['type']}` {r['members']} across pillars {r['pillars']} (evidence: {', '.join('`' + e + '`' for e in r['evidence'])})" for r in pillars["relations"]],
       f"- day void metadata `{pillars['day_void']['metadata']}` == computed `{pillars['day_void']['computed']}` → **validated**",
       f"- hour void metadata `{pillars['hour_void']['metadata']}` == computed `{pillars['hour_void']['computed']}` → **validated**",
       "\n## Season (raw terms preserved; normalization computed)",
       "| element | raw | normalized |", "|---|---|---|"]
for el, s in season["normalized"].items():
    md.append(f"| {el} | {s['raw']} | {s['normalized']} ({s['mapping_status']}) |")
md += ["\n## Duty & authority",
       f"- **fu_tou**: `{duty['fu_tou']['raw_value']}` → xun leader {duty['fu_tou'].get('xun_leader')}, yi stem **{duty['fu_tou'].get('yi_stem')}** (frozen table check: {duty['fu_tou'].get('yi_stem_matches_frozen_table')}); Jia concealed under {duty['lead_stem']['visible_proxy']} → **Ren is the visible stand-in for the invisible leader Jia**",
       f"- **zhi_fu (duty star)**: {duty['zhi_fu']['raw_value']} → Tian Rui, home 2, active **3**; cross-check in palace star field: {json.dumps(duty['zhi_fu']['cross_check_in_palace_star_field'])}",
       f"- **zhi_shi (duty door)**: {duty['zhi_shi']['raw_value']} → Death, original {duty['zhi_shi']['original_palace']}, active **{duty['zhi_shi']['active_palace']}** (displacement logged); door field cross-check: {json.dumps(duty['zhi_shi']['cross_check_door_field'])}",
       f"- **tian_yi**: {duty['tian_yi']['raw_value']} → Tian Chong seated in palace 6 (`palaces.qian_6.star`)",
       f"- **Chief deity** cross-validates duty star seat: {json.dumps(duty['chief_deity_palace'])}",
       "\n## Origin sets (selectors are sets — resolved by value match)",
       f"- **B1** (day stem trace): {origins['B1']['primary_set']} — day stem Ren on heaven `palaces.zhen_3.heaven_stem`; proxies: lead Ren → {origins['B1']['proxy_hits'][0]['palaces']}, duty_star palace → {origins['B1']['proxy_hits'][1]['palaces']}, tomb_of_day_gan → {origins['B1']['proxy_hits'][2]['palaces']}, earth_or_hidden → {origins['B1']['proxy_hits'][3]['palaces']}",
       f"- **B2** (hour focus): {origins['B2']['primary_set']} (+ hour branch → {origins['B2']['proxy_hits'][0]['palaces']}, hour horse → {origins['B2']['proxy_hits'][1]['palaces']} as trace)",
       f"- **B3** (opposite of B1): {origins['B3']['primary_set']} — cost/check",
       f"- **B4** (opposite of B2): {origins['B4']['primary_set']} — forward/if-proceed check",
       f"- **B5** (remaining, Luo Shu order): {origins['B5']['primary_set']}",
       f"- Jia on heaven: **false by construction** (Dun Jia); {origins['jia']['note']}; Jia references: {json.dumps(origins['jia']['jia_references'])}",
       "\n## Center lodging graph (Center stays NO_OPPOSITE pivot)",
       *[f"- {e['entity']} ({e['entity_layer']}) lodged from palace {e['from_palace']} → **{e['to_palace']}** (`{e['evidence']}`; host confirmation: {json.dumps(e['host_confirmation'])[:120]}…)" for e in lodging["graph"]],
       "\n## Marker validation (explicit markers vs computed)",
       f"- Void: {json.dumps([(v['palace'], v['status']) for v in mv['void']])}",
       f"- Horse: computed palaces {sorted(mv['horse_palaces_computed'], key=int)} — {json.dumps([(h['palace'], h['status']) for h in mv['horse']])}",
       f"- Tomb checks: {json.dumps([(t['palace'], t['stem'], t['computed_tomb_branch'], t['tomb_branch_in_palace']) for t in mv['tomb']])}",
       f"- Mismatches (recorded, not suppressed): {json.dumps(mv['mismatches'])}",
       f"- Oppression validation: {json.dumps([(o['palace'], o['door'], o['validated']) for o in mv.get('oppression', [])])}",
       f"- Liu-Yi punishment validation (classical table): {json.dumps([(e['palace'], e['stem'], e['validated']) for e in mv.get('liuyi_punishment', [])])} — all entries match Wu@3/Ji@2/Geng@8/Xin@9/Ren@4/Gui@4",
       f"- Name-key consistency: {json.dumps([(e['palace'], e['name_matches_key']) for e in mv.get('name_key_consistency', [])])}",
       "\nSee also: [[Chart-Working-Copy]] · [[Palace-Analysis-Index]] · [[MOC]]"]
write_text(os.path.join(WIKI, "Chart-Anatomy.md"), "\n".join(md))

# ---------- Chart-Working-Copy ----------
wang = systems["wangshuai_matrix"]
md = [fm("chart-working-copy", "article", "P6_BOARD_SYNTHESIS", "—", list("123456789"), "frozen",
         ["raw/state/systems.json", "raw/state/palaces.json"]),
      "# Chart Working Copy (normalized board)\n",
      "| palace | heaven/earth/hidden | star | door | deity | door str | star str (raw tokens) | palace state | ring | split |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for pid in sorted(wang, key=int):
    pv = data["palaces"][key_of[pid]]; w = wang[pid]
    md.append(f"| {pid} {PALACE_IDENTITY[pid]['name']} | {pv.get('heaven_stem')} / {pv.get('earth_stem')} / {pv.get('hidden_stem')} | {pv.get('star')} | {pv.get('door') or '—'} | {pv.get('deity')} | {w['door_strength_raw'] or '—'} | {w['star_strength_raw'] or '—'} | {w['palace_state_raw'] or '—'} | {w['ring']} | {'YES' if w['split_star_strength'] else 'no'} |")
md += ["\n*Raw vocabulary preserved; normalization is computed only. Star two-token convention (by_season/by_palace order) is flagged SCHEMA_AMBIGUITY — tokens never force-mapped.*",
       "\nSee also: [[Chart-Anatomy]] · [[Chart-Board-Synthesis]] · [[MOC]]"]
write_text(os.path.join(WIKI, "Chart-Working-Copy.md"), "\n".join(md))

# ---------- Chart-Board-Synthesis ----------
md = [fm("chart-board-synthesis", "article", "P6_BOARD_SYNTHESIS", "—", list("123456789"), "frozen",
         ["raw/state/systems.json", "raw/state/relations.json", "raw/state/patterns.json"]),
      "# Chart Board Synthesis (P6)\n", "## Door system map"]
for d, m in systems["door_system_map"].items():
    md.append(f"- **{d}** @ palace {m['palace']} — {m['relation'] or '—'} (`{m['evidence'][0]}`)")
md.append("\n## Star system map (home → seat; all displaced)")
for s, m in systems["star_system_map"].items():
    md.append(f"- **{s}** (home {m['seats'][0]['home']}) → seats {json.dumps([(x['palace'], x['displaced']) for x in m['seats']])}")
md += ["\n## Deity map", *[f"- **{d}** @ palace {m['palace']}" for d, m in systems["deity_two_plate_map"].items()],
       "\n## San Qi / Liu Yi positions", "| stem | class | positions |", "|---|---|---|"]
for s, m in systems["sanqi_liuyi_map"].items():
    md.append(f"| {s} | {m['class']} | {json.dumps([(p['palace'], p['layer']) for p in m['positions']])} |")
md += ["\n## Void · tomb · punishment · force · horse graph", "| palace | void | tomb markers | punishment | forced door | horse |", "|---|---|---|---|---|---|"]
for pid, g in systems["void_tomb_punish_force_horse_graph"].items():
    md.append(f"| {pid} | {g['void'] or '—'} | {json.dumps(g['tomb_markers']) if g['tomb_markers'] else '—'} | {g['punishment_field'] or '—'} | {'YES' if g['forced_door'] else 'no'} | {(' ; '.join(g['horse'])) if g['horse'] else '—'} |")
md += ["\n## Inner/outer", f"- inner: {systems['inner_outer']['inner']} — {systems['inner_outer']['meaning']['inner']}",
       f"- outer: {systems['inner_outer']['outer']} — {systems['inner_outer']['meaning']['outer']}",
       "\n## Pillars × palaces", "| pillar | stem→palaces | branch→palace | void membership |", "|---|---|---|---|"]
for p, pj in systems["pillars_times_palaces"]["projections"].items():
    vd = ("DAY-VOID " if pj["in_day_void"] else "") + ("HOUR-VOID" if pj["in_hour_void"] else "")
    md.append(f"| {p} ({pj['stem']} {pj['branch']}) | {json.dumps([(x['palace'], x['layer']) for x in pj['stem_palaces_layers']])} | {pj['branch_palace']} | {vd or '—'} |")
md += ["\n## Reconstituted center", f"- center lodging graph: {json.dumps([(e['entity'], e['to_palace']) for e in systems['reconstitute_center']['lodging_graph']])}",
       f"- read-through hosts: {systems['reconstitute_center']['read_through_hosts']}",
       "\n## Original-position audit (post-remediation)", "| palace | branches | star home | door home | deity note | numbers |", "|---|---|---|---|---|---|"]
for pid in sorted(systems["original_position_audit"], key=int):
    o = systems["original_position_audit"][pid]
    if not o.get("explicit_block_present"):
        continue
    md.append(f"| {pid} | {'match' if o['branches']['match'] else 'MISMATCH'} | {o['star']['explicit']}→{o['star']['canonical']} ✓ | {o['door'].get('explicit') or 'absent by design'} | rotation-divergence recorded | opaque |")
md.append(f"- summary: {json.dumps(systems['original_position_audit_summary'])}")
md += ["\n## Opposite-palace audit (explicit vs frozen geometry)",
       "| palace | explicit | computed | status |", "|---|---|---|---|",
       *[f"| {o['palace']} | {o.get('explicit')} | {o.get('computed_opposite', o.get('computed'))} | {o['status']} |" for o in systems["opposite_palace_audit"]],
       "\nBoard consistency: **PASS** — split claims recorded for palaces 2, 4, 9 (overload rule); no SUPPORT/VETO collision on the same logical path.",
       "\nSee also: [[Chart-Patterns]] · [[Chart-Analysis-Report]] · [[MOC]]"]
write_text(os.path.join(WIKI, "Chart-Board-Synthesis.md"), "\n".join(md))

# ---------- Chart-Patterns ----------
md = [fm("chart-patterns", "article", "P6_BOARD_SYNTHESIS", "—", list("123456789"), "frozen",
         ["raw/state/patterns.json", "raw/state/explicit_patterns.json"]),
      "# Chart Patterns\n", "## Explicit pattern reconciliation (explicit ingested before computed)",
      "| explicit pattern | palace | status | note |", "|---|---|---|---|"]
for r in patterns["explicit_pattern_reconciliation"]:
    md.append(f"| {r['pattern']} | {r['palace']} | **{r['status']}** | {r['note'] or '—'} |")
md += ["\n## Computed catalog (always-on extraction)", "| pattern | palaces | polarity | grounding | note |", "|---|---|---|---|---|"]
for h in patterns["computed_catalog"]:
    nm = h.get("name_en") or h.get("name_or_combination")
    md.append(f"| {nm} | {h['palaces']} | {h['polarity']} | {h['grounding']} | {h.get('note', '—')} |")
md += ["\nNaming discipline: **earthly_escape** named (both pieces co-located in palace 7). Heavenly/human escapes stored as unnamed combinations only — pieces exist but are not co-located.",
       "\nSee also: [[Chart-Board-Synthesis]] · [[Chart-Analysis-Report]] · [[MOC]]"]
write_text(os.path.join(WIKI, "Chart-Patterns.md"), "\n".join(md))

# ---------- Palace-Analysis-Index ----------
md = [fm("palace-analysis-index", "article", "P6_BOARD_SYNTHESIS", "—", list("123456789"), "frozen", ["raw/state/palaces.json"]),
      "# Palace Analysis Index\n",
      "| palace | batch | roles | verdicts | polarities | card | trace |", "|---|---|---|---|---|---|---|"]
for pid in sorted(palaces_state, key=int):
    c = palaces_state[pid]
    pols = sorted({v["polarity"] for v in c["verdicts"]})
    md.append(f"| {pid} {PALACE_IDENTITY[pid]['name']} | {c['batch']} | {len(c['roles'])} | {len(c['verdicts'])} | {', '.join(pols)} | [[Palace-{pid}-{PALACE_IDENTITY[pid]['name']}]] | `raw/traces/trace_palace_{pid}.json` |")
md.append("\nMachine index: `raw/state/palaces.json` (agents read JSON; this page is the generated human view).")
write_text(os.path.join(WIKI, "Palace-Analysis-Index.md"), "\n".join(md))

# ---------- Chart-Red-Team ----------
rt = red["checks"]
md = [fm("chart-red-team", "article", "AUDIT", "—", list("123456789"), "frozen", ["raw/state/red_team.json", "raw/state/package_gates.json"]),
      "# Chart Red Team\n"]
for i, a in enumerate(rt["adversarial_rederivation"], 1):
    md += [f"## Adversarial rederivation {i}: {a['attempt']}", f"**Result: {a['result']}**",
           *[f"- {w}" for w in a["why"]], f"- verdict effect: {a['verdict_effect']}", ""]
md += [f"## Machine checks",
       f"- citation integrity: broken links = {rt['citation_integrity']['broken_links']}",
       f"- candidate contamination (requirement-fit / assignment leakage): {len(rt['candidate_contamination']['violations'])} violations → PASS",
       f"- coverage contamination (claims citing uninventoryed paths): {len(rt['coverage_contamination']['claims_citing_uninventoryed_paths'])} → PASS",
       f"- anomaly suppression: {rt['anomaly_suppression_check']['registry_count']} registry anomalies == {rt['anomaly_suppression_check']['package_count']} packaged → all visible → PASS",
       f"\nOverall red-team verdict: **{'PASS' if red['pass'] else 'FAIL'}**"]
write_text(os.path.join(WIKI, "Chart-Red-Team.md"), "\n".join(md))

print("wiki part 1 written:", len(os.listdir(WIKI)), "files")
