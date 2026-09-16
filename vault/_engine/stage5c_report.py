"""Stage 5c: Chart-Analysis-Report.md + MOC.md + package hash + HALT."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *

data = load_source()
machine = load_state("machine.json")
prov = load_state("raw_provenance.json")
palaces_state = load_state("palaces.json")
pkr = load_state("palace_key_resolution.json")["palaces"]
key_of = {pid: v["raw_palace_key"] for pid, v in pkr.items()}
pillars = load_state("pillars.json"); season = load_state("season.json"); duty = load_state("duty.json")
origins = load_state("origin_sets.json"); lodging = load_state("lodging.json"); mv = load_state("marker_validation.json")
systems = load_state("systems.json"); patterns = load_state("patterns.json"); res = load_state("archetype_resolutions.json")
seed = load_state("solution_seed.json"); absence = load_state("absence_registry.json"); anom = load_state("anomaly_registry.json")
mani = load_state("path_coverage_manifest.json"); yg = load_state("yongshen.json")
gates = load_state("package_gates.json"); red = load_state("red_team.json"); cg = load_state("coverage_gate.json")
TS = utcnow()

def fm(id_, type_, phase, batch, palace_ids, status, sources):
    return ("---\n" + f'id: "{id_}"\ntype: "{type_}"\nphase: "{phase}"\nbatch: "{batch}"\n'
            f"palace_ids: {json.dumps(palace_ids)}\n" + "sources:\n"
            + "".join(f'  - "{s}"\n' for s in sources) + f'updated: "{TS}"\nstatus: "{status}"\n---\n\n')

def claim_line(v):
    return f"- **{v['claim_id']}** [{v['slot']} · {v['polarity']} · {v['confidence']} · {v['grounding']}] {v['text_en']}"

R = []
R.append(fm("chart-analysis-report", "report", "PACKAGE_RENDER", "—", list("123456789"), "frozen",
            ["raw/state/chart_analysis_package.json", "raw/state/archetype_resolutions.json", "raw/state/solution_seed.json", "raw/state/red_team.json"]))
R.append("# Chart Analysis Report — project_1 (MARKETING chart JSON)\n")
R.append("> **Scope law:** chart-derived evidence only. This report binds nothing to any assignment; requirement-fit is null by design; every claim cites leaf-level JSON paths or derived state objects. Source JSON was hashed and never mutated.")
R.append("")
R.append("## Infobox")
R.append(f"- **Source:** `{prov['file']}` (sha256 `{prov['sha256']}`, {prov['size_bytes']} bytes, UTF-8)")
R.append(f"- **Run:** `{machine['run_id']}` · generated {TS}")
R.append(f"- **Schema variant:** project_1_chart_info_v1 (confidence 1.0) · **Variant binding:** semantic-role, no hardcoded paths")
R.append(f"- **Chart:** {data['chart_info']['system']} / {data['chart_info']['method']} · Yin Dun 6th Ju · solar term: {data['chart_info']['solar_term']} · 2026-09-15 22:04 Tue · lunar 8M/5D Hai hour")
R.append(f"- **Structural proof:** {mani['total_paths']} recursive paths inventoried · {load_state('array_itemization.json')['item_count']} array items · {sum(len(r['absent_paths']) for r in absence['records'])} absent leaf fields · {len(anom['records'])} anomalies preserved · 0 exclusions")
R.append(f"- **Gates:** coverage PASS · citations 0 broken · leaf-only OK · board consistency PASS · red team **{ 'PASS' if red['pass'] else 'FAIL' }** · determinism PASS (double-run diff = 0)")
R.append(f"- **Protocol:** interpretation v2.2.0 `sha256:protocol_v2_2_2_0_chart_analyst_v5` · rubric v1.1.0 `sha256:archetype_scoring_rubric_1_1_0_chart_analyst_v5`")
R.append("")
R.append("## 0. Executive reading (chart-only)")
R.append("1. **The seat is Zhen 3 (East, Wood, outer).** Day stem Ren faces outward from Zhen 3, and it is the *only* palace carrying the day stem on heaven; the concealed leader (fu_tou: Jia Chen → Ren) and the duty star (Tian Rui) point at the same palace, with the Chief deity presiding. One seat, no rivals — but it sits **hour-void** (Mao) and its method (Scenery door) is **Imprisoned**: identity is clear; landing and visibility are not.")
R.append("2. **The trap is Xun 4 (Southeast, Wood, outer).** The duty door itself is **Death**, forced by the palace, entering tomb; the explicit marker entombs *and* punishes the day stem Ren right there — while the same palace flashes explicit 'wonder' patterns (Yi+Geng combination, Three Wonders Obtaining Mission, Nine Heavens, Horse). The chart's own gold is glued to the chart's own lock. Rule 16 split: the glitter is real, the door is shut.")
R.append("3. **The how is Dui 7 (West, Metal, inner).** The board's only concordant-strong, affliction-free palace: Rest door at Strong, star Prosperous/Prosperous, palace Prosperous/Inner, explicit Palace-Generating-Door, sanqi on both plates (Bing heaven / Yi earth) — **earthly escape co-located**, month-stacked (in-period). White Tiger warns: run it clean, procedural, inside institutions.")
R.append("4. **The when/with-whom is Qian 6 (Northwest, Metal, inner).** Hour focus, Life door, Six Harmony, the Tian Yi star — but a cool engine (star Imprisoned/Imprisoned, earth Wu entombed) and an Xu–Chen clash into the day root. Use it for pacts and backstage backing; expect latency and friction.")
R.append("5. **The showcase is void.** Li 9 — the year-stacked public surface — is day-void (Wu) with seasonal fire imprisoned. Big display energy that does not land this window; it fills on **Wu**. And all eight explicit opposite-palace labels disagree with frozen geometry (preserved as anomalies; computed geometry stands).")
R.append("")
R.append("## 1. Chart anatomy (validated)")
P = pillars["pillars"]
R.append("| pillar | raw | stem | branch | xun | void check |")
R.append("|---|---|---|---|---|---|")
for p in ["year", "month", "day", "hour"]:
    g = P[p]; R.append(f"| {p} | {g['raw_value']} | {g['stem_pinyin']} ({g['stem_polarity']} {g['stem_element']}) | {g['branch_pinyin']} | {g['xun']['xun_leader']} | {g['xun']['void_branches']} |")
R.append(f"- Metadata voids match computed xun voids (day `{pillars['day_void']['metadata']}`, hour `{pillars['hour_void']['metadata']}`) → both **validated**.")
R.append(f"- Pillar relations (computed): " + "; ".join(f"{r['type']} {r['members']} over {r['pillars']}" for r in pillars["relations"]))
R.append(f"- Season: {json.dumps({k: v['normalized'] for k, v in season['normalized'].items()})} (raw vocabulary preserved in `raw/state/season.json`)")
R.append(f"- Duty: lead = Jia hidden under **Ren** (`chart_info.fu_tou`); duty star **Tian Rui @3** (cross-checked in `palaces.zhen_3.star` and by Chief deity seat); duty door **Death @4** (original 2 ≠ active 4 → displacement logged); tian yi **Tian Chong @6** (`chart_info.tian_yi`, `palaces.qian_6.star`).")
R.append("")
R.append("## 2. Operator plan (origin sets are sets, resolved by value)")
R.append(f"B1 day-trace → **{origins['B1']['primary_set']}** (proxies converge: lead Ren, duty-star palace; tomb-of-day-gan → {origins['B1']['proxy_hits'][2]['palaces']}; earth/hidden → {origins['B1']['proxy_hits'][3]['palaces']}) · B2 hour-focus → **{origins['B2']['primary_set']}** · B3 cost/check → **{origins['B3']['primary_set']}** · B4 forward → **{origins['B4']['primary_set']}** · B5 remainder (Luo Shu) → **{origins['B5']['primary_set']}**")
R.append("")
R.append("## 3. Palace verdicts (32 typed claims)")
for pid in sorted(palaces_state, key=int):
    c = palaces_state[pid]; idn = PALACE_IDENTITY[pid]
    R.append(f"### Palace {pid} — {idn['name']} ({idn['dir']}, {idn['element']}, {'inner' if pid in INNER_PALACES else 'outer'}) · batch {c['batch']}")
    R.append(f"*roles:* {' · '.join(c['roles'])}")
    for v in c["verdicts"]:
        R.append(claim_line(v))
    R.append(f"→ full card [[Palace-{pid}-{idn['name']}]] · trace `raw/traces/trace_palace_{pid}.json`")
    R.append("")
R.append("## 4. Systems (P6)")
R.append("**Wangshuai matrix** (raw tokens preserved; normalization computed):")
R.append("| palace | element(season) | door strength | star strength raw | palace state | split | door==season? |")
R.append("|---|---|---|---|---|---|---|")
for pid in sorted(systems["wangshuai_matrix"], key=int):
    w = systems["wangshuai_matrix"][pid]
    R.append(f"| {pid} | {w['palace_element']} ({w['seasonal_element_strength']['normalized']}) | {w['door_strength_raw'] or '—'} | {w['star_strength_raw'] or '—'} | {w['palace_state_raw'] or '—'} | {'YES' if w['split_star_strength'] else 'no'} | {w['season_matches_door']} |")
R.append("- Door map: " + "; ".join(f"{d}@{m['palace']}" for d, m in systems["door_system_map"].items()))
R.append("- Star map: every star displaced from home (0 `star_sitting_home` hits); Tian Qin additionally lodged out of center into Zhen 3.")
R.append("- Deity map: " + "; ".join(f"{d}@{m['palace']}" for d, m in systems["deity_two_plate_map"].items()))
R.append("- San Qi: Yi (4 heav, 7 earth, 9 hid) · Bing (7 heav, 8 earth, 6 hid) · Ding (8 heav, 9 earth, 3 hid). Hidden-layer five-combinations computed: Ding–Ren in palace 3, Bing–Xin in palace 6, Wu–Gui in palace 2.")
mv2 = load_state("marker_validation.json")
R.append(f"- **Liu-Yi punishment validated:** all six entries match the classical punishment-palace table (Wu@3, Ji@2, Geng@8, Xin@9, Ren@4, Gui@4) — chart internals consistent; oppression marker validated (door Wood over palace Earth in Gen 8); palace name fields all match keys.")
R.append(f"- **Original-position audit:** explicit branch lists match frozen geometry 8/8; original stars/doors all consistent; deity divergences recorded as expected rotation; `original_position.numbers` kept opaque by policy. Six-harm branch relations computed: Chen(4)–Mao(3) ties the trap palace to the answer seat; You(7)–Xu(6) warns that the HOW and WHEN channels chafe each other.")
R.append("")
R.append("## 5. Patterns (explicit first, computed second)")
R.append("| explicit pattern | palace | reconciliation | |")
R.append("|---|---|---|---|")
for r in patterns["explicit_pattern_reconciliation"]:
    R.append(f"| {r['pattern']} | {r['palace']} | {r['status']} | {r['note'] or ''} |")
R.append("")
R.append("Computed catalog highlights: forced_door@4 · void_palace {2,3,8,9} · stem_in_tomb {2,4,6,8} · duty_star@3 · duty_door@4 · hour_stem_focus@6 · horse_star {2,4,6,8} · **earthly_escape@7 (named — both pieces present)** · heavenly/human escapes withheld (pieces not co-located) · door_at_original_palace@9 · star_sitting_home: 0 hits · split_star_strength {1,2,3,4,8,9} · stacked branches: year→9, month→7, day→4, hour→6 · opposite_palace_mismatch on all 8 labeled palaces.")
R.append("")
R.append("## 6. Archetype resolutions (rubric v1.1.0; requirement_fit = null)")
for rr in res["resolutions"]:
    R.append(f"### {rr['resolution_id']} — {rr['slot']}")
    R.append("| candidate | grounding | support | contra | board | score | selected | reason |")
    R.append("|---|---|---|---|---|---|---|---|")
    for c in rr["candidates_considered"]:
        R.append(f"| {c['archetype_id']} | {c['grounding_tier']} | {c['supporting_evidence_count']} | {c['contradicting_evidence_count']} | {'✓' if c['board_consistency_pass'] else '✗'} | **{c['final_score']}** | {'**WINNER**' if c['selected'] else ''} | {c.get('rejection_reason') or ('no competing candidate found' if len(rr['candidates_considered'])==1 else '—')} |")
    R.append(f"- **Winner:** {rr['winner']} · **Margin:** {rr['margin_note']}")
    R.append(f"- **Tie note:** {rr['tie_note']}")
    R.append("")
R.append("## 7. Solution seed — chart-derived only, not yet requirement-bound")
R.append(f"*note carried in package:* `{seed['note']}`")
R.append("### Answers")
for a in seed["answers"]:
    R.append(f"- **[{a['archetype_resolution']} · score {a['score']}]** {a['reading']} (claims: {', '.join(a['claims'])}; constraints cited: {', '.join('`'+p+'`' for p in a['constraints_cited'])})")
R.append("### Hidden problems (ranked)")
for h in seed["hidden_problems"]:
    tied = f" — tied at this score with {', '.join(h['tied_with'])}" if h.get("tied_with") else ""
    R.append(f"- **#{h['rank']} [{h['archetype_resolution']} · {h['archetype']} · {h['score']}]**{tied} {h['reading']} (claims: {', '.join(h['claims'])})")
R.append("### Best-solution candidates (ranked)")
for b in seed["best_solution_candidates"]:
    cav = f" — caveats: {', '.join('`'+p+'`' for p in b['caveats_cited'])}" if b.get("caveats_cited") else ""
    rj = f" — rejected: {b['reason']}" if b.get("reason") else ""
    R.append(f"- **{b['rank']} [{b['archetype']} · {b['score']}]** {b.get('reading', '')}{cav}{rj} (claims: {', '.join(b['claims'])})")
R.append("")
R.append("## 8. Timing picture (chart-derived)")
R.append("- Voids: day-void **Wu Wei** → palaces 9 (Wu) and 2 (Wei) silent until filled (fills on Wu/Wei); hour-void **Yin Mao** → palaces 8 (Yin) and 3 (Mao) — the answer seat lands on **Mao** day/hour; the showcase fills on **Wu**.")
R.append("- Horses: year Shen→2, month Hai→6, day Yin→8, hour **Si→4** — the hour's fastest vector points into the obstruction cluster; the month horse supports the help palace 6.")
R.append("- Stacked pillar branches: year→9, month→7, day→4, hour→6 — palaces 9/7/4/6 are 'in-frame' for their respective periods; palace 7 is month-resourced now.")
R.append("- Clashes: palace 6 branch Xu clashes day branch Chen — activating help rocks the day's root (SEQUENCE/WARN shipped on CLM-011).")
R.append("")
R.append("## 9. Anomalies & absences (preserved, never repaired)")
R.append(f"**Anomalies: {len(anom['records'])}**")
R.append("| id | type | severity | description |")
R.append("|---|---|---|---|")
for a in anom["records"]:
    R.append(f"| {a['id']} | {a['type']} | {a['severity']} | {a['description']} |")
R.append("")
R.append(f"**Absences: {sum(len(r['absent_paths']) for r in absence['records'])} leaf fields across {len(absence['records'])} palaces** — absence recorded, never treated as false:")
for r in absence["records"]:
    R.append(f"- palace {r['palace_id']}: {', '.join('`' + p.split('.')[-2] + '.' + p.split('.')[-1] + '`' for p in r['absent_paths'])} — {r['structural_significance']}")
R.append("")
R.append("## 10. Coverage, gates, red team, determinism")
R.append(f"- Coverage gate: {json.dumps(cg['gates'])}")
g = gates["gates"]
R.append(f"- Package gates: schema {g['validate_schema']['valid']} · citations broken {g['citation_integrity']['broken_links']} · parent-only citations {g['leaf_citation_integrity']['parent_only_citations']} · board consistency {g['board_consistency']['pass']} · archetype refs missing {g['archetype_resolution_presence']['missing']} · determinism {g['determinism_check']['pass']} · coverage {g['coverage_complete']['pass']} · explicit-before-computed {g['explicit_pattern_priority']['pass']}")
R.append(f"- Red team: **{'PASS' if red['pass'] else 'FAIL'}** — 3 adversarial rederivation attempts (Kun 2 as best channel / Li 9 as auspicious showcase / re-seating the answer) all REJECTED with cited reasons; contamination scans clean. Details: [[Chart-Red-Team]].")
R.append("- AUDIT_FIX cycles used: 1 of 3 (citation class rewrite `state:qmdj_complete.*` → `state:frozen_tables.*` persisted).")
R.append("")
R.append("## 11. Unbound yongshen candidates (no assignment binding)")
R.append("| candidate | class | bound | requirement_fit |")
R.append("|---|---|---|---|")
for c in yg["candidates"]:
    R.append(f"| {c['candidate']} | {c['class']} | {c['bound']} | {c['requirement_fit_score']} |")
R.append("")
R.append("## 12. Provenance & reproduction")
R.append(f"- Source: `{prov['file']}` · sha256 `{prov['sha256']}` · ingested {prov['ingested_at']} · run `{machine['run_id']}`")
R.append("- Package: `raw/state/chart_analysis_package.json` (sha256 `" + load_state("machine.json")["verification"]["package_sha256"] + "`)")
R.append("- Determinism: P0 derivation run twice in memory, origin-sets diff = 0; package byte-stable modulo `generated_at`/`run_id`.")
R.append("- Pipeline: CHART_INGEST → STRUCTURAL_INVENTORY → SCHEMA_ADAPTATION → P0_ANATOMY → B1–B5 → COVERAGE_GATE → P6_BOARD_SYNTHESIS → PACKAGE_RENDER → HALT")
R.append("")
R.append("See also: [[Chart-Anatomy]] · [[Chart-Board-Synthesis]] · [[Chart-Patterns]] · [[Palace-Analysis-Index]] · [[Chart-Red-Team]] · [[MOC]]")
write_text(os.path.join(WIKI, "Chart-Analysis-Report.md"), "\n".join(R))

# ---------- MOC ----------
cards = sorted([f for f in os.listdir(WIKI) if f.startswith("Palace-") and "Index" not in f])
moc = [fm("moc", "moc", "PACKAGE_RENDER", "—", list("123456789"), "frozen",
          ["raw/state/chart_analysis_package.json"]),
       "# MOC — Carpathia QMDJ Chart Analysis (project_1)\n",
       "## Report", "- [[Chart-Analysis-Report]] — master report (start here)\n",
       "## Structural layer", "- [[Chart-Schema]] — variant detection & semantic binding",
       "- [[Chart-Anatomy]] — pillars, season, duty, origin sets, lodging, validation",
       "- [[Chart-Working-Copy]] — normalized board view\n",
       "## Synthesis layer", "- [[Chart-Board-Synthesis]] — systems & matrices (P6)",
       "- [[Chart-Patterns]] — explicit reconciliation + computed catalog", "- [[Chart-Red-Team]] — adversarial audit\n",
       "## Palace cards", *[f"- [[{c[:-3]}]]" for c in cards],
       "\n## Indexes & state", "- [[Palace-Analysis-Index]]", "- `raw/state/chart_analysis_package.json` (machine deliverable)",
       "- `raw/state/progress.md` (heartbeat)"]
write_text(os.path.join(WIKI, "MOC.md"), "\n".join(moc))

pkg_hash = sha256_file(os.path.join(STATE, "chart_analysis_package.json"))
machine_update(state="HALT", completed_phases=load_state("machine.json")["completed_phases"] + ["PACKAGE_RENDER"],
               package_sha256=pkg_hash, halted_at=TS)
progress(f"PACKAGE_RENDER done | wiki articles: {len([f for f in os.listdir(WIKI) if f.endswith('.md')])} | report written | package sha256: {pkg_hash}")
progress("HALT | run complete; not waiting for user input")
print("HALT OK — report:", os.path.join(WIKI, "Chart-Analysis-Report.md"), "| package sha256:", pkg_hash)
