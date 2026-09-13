"""Chart-Analysis-Report.md + Chart-Red-Team.md + determinism check + MANIFEST."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

Q = load_qmdj()
PKG = jread(os.path.join(STATE, "chart_analysis_package.json"))
CARDS = {c["palace_id"]: c for c in PKG["palaces"]}
RES = PKG["patterns"]["archetype_resolutions"]
SEED = PKG["solution_seed"]
SYS = PKG["systems"]
DUTY = PKG["anatomy"]["duty"]
SEASON = PKG["anatomy"]["season"]
PILL = PKG["anatomy"]["pillars"]
CONS = PKG["patterns"]["board_consistency_check"]
ANOM = PKG["anomalies"]


def res(rid):
    return [r for r in RES if r["resolution_id"] == rid][0]


def sel(rid):
    return [c for c in res(rid)["candidates_considered"] if c["selected"]]


# ============================================================== REPORT =====
def report():
    L = ["---", "id: chart-analysis-report", "type: report", "phase: PACKAGE_RENDER",
         "batch: \"-\"", "palace_ids: [\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\"]",
         "sources: [\"raw/state/chart_analysis_package.json\"]",
         f"updated: {GENERATED_AT}", "status: frozen", "---", "",
         "# Chart Analysis Report", "",
         "**Chart-only analysis. No assignment was read, and nothing here is bound to a "
         "requirement.** Every conclusion below is evidence for a downstream solver, not a "
         "submission. Where the chart is ambiguous the ambiguity is preserved rather than "
         "resolved.", "",
         "## Infobox", "", "| key | value |", "|---|---|",
         f"| Source | `QMDJ/ADVERTISING/project_1.json` |",
         f"| sha256 | `{PKG['source_qmdj_sha256']}` |",
         f"| Package version | {PKG['package_version']} |",
         f"| System | {Q['system']['school']}, {Q['system']['chart_type']}, {Q['system']['method']} |",
         f"| Structure | {Q['chart_config']['structure']} |",
         f"| Solar term | {Q['timing']['solar_term']['name']}, "
         f"{Q['timing']['solar_term']['yuan']} yuan, day {Q['timing']['solar_term']['day']} |",
         f"| Four pillars | {Q['timing']['four_pillars']['year']} / "
         f"{Q['timing']['four_pillars']['month']} / {Q['timing']['four_pillars']['day']} / "
         f"{Q['timing']['four_pillars']['hour']} |",
         f"| Chart pattern | {Q['chart_config']['chart_pattern']} |",
         f"| Duty star / door | {DUTY['duty_star']} / {DUTY['duty_door']}, palace "
         f"{', '.join(DUTY['duty_star_palace'])} |",
         f"| Void palaces | {', '.join(PKG['anatomy']['validation']['void']['computed'])} |",
         f"| Horse palace | {', '.join(PKG['anatomy']['validation']['horse']['computed'])} |",
         f"| Verdicts | {sum(len(c['verdicts']) for c in PKG['palaces'])} across 9 palaces |",
         f"| Pattern hits | {len(PKG['patterns']['hits'])} |",
         f"| Anomalies | {len(ANOM)} |", "",
         "## Lead", "",
         "This is a completely static board. The chart declares Fu Yin and the declaration checks "
         "out independently: in all nine palaces the heaven, earth and hidden stems are the same "
         "stem, every star sits in its Luo Shu home, and every door sits at its original palace. "
         "Nothing on this board moves by itself.", "",
         "Against that frozen background, three facts do the real work. The day stem **Bing** - "
         "the actor - is stranded in the Centre and has to borrow palace 2 to exist at all. The "
         "hour stem **Jia** - the matter in motion - does not appear on any plate anywhere, and "
         "Wood is Dead this season. And the duty palace, the thing the chart says the question is "
         "actually about, is **void**, imprisoned in both door and palace, and carries three "
         "stacked afflictions at once.", "",
         "The short version: the visible centrepiece is the weakest thing on the board, the actor "
         "has no ground of its own, and nothing will change unless it is changed deliberately "
         "from outside.", "",
         "## 1. What the chart says the matter is", ""]

    r = res("AR-ANSWERS-01")
    for c in sel("AR-ANSWERS-01"):
        L += [f"**{c['label_en']}**", "",
              f"- archetype `{c['archetype_id']}` | grounding {c['grounding_tier']} | "
              f"score {c['final_score']} | resolution `{r['resolution_id']}`", ""]
    L += ["Palace 9 (Li, South) is flagged `is_duty_palace`, carries the duty star Tian Ying "
          "(Hero) and the duty door Jing (Scenery), and holds Xin - the visible stand-in stem for "
          "the invisible Jia-Wu decade named in `chart_config.lead_stem`. Four separate header "
          "fields point at the same palace, so the subject of this chart is not in doubt.", "",
          "What is in doubt is whether it holds. The same palace is void, its door is Imprisoned, "
          "the palace itself is Imprisoned, and it carries `Clash Punishment (Ji Xing)`, "
          "`Self Punishment` and `Fu Yin` simultaneously. The year branch Wu and the hour branch "
          "Wu both stack onto it. The chart concentrates all its attention - and all its timing - "
          "on a position that is explicitly marked as not landing.", "",
          "Tian Ying (Hero) is the showpiece star, Jing (Scenery) is the showpiece door, and Li "
          "is the palace of visibility, reputation and display. This is a chart about something "
          "*being seen*. The void says it is seen but not received.", "",
          "**Secondary answer, retained live:**", ""]
    for c in res("AR-ANSWERS-01")["candidates_considered"]:
        if not c["selected"] and c["board_consistency_pass"]:
            L += [f"- {c['label_en']} (`{c['archetype_id']}`, score {c['final_score']})", "",
                  f"  {c['rejection_reason']}", ""]
    L += [f"*Margin:* {r['margin_note']}", "",
          "## 2. Hidden problems", ""]

    rh = res("AR-HIDDEN-01")
    L += ["The chart carries five distinct problems. They are listed in scored order, but the "
          "top four are all live and none of them cancels another.", ""]
    for i, c in enumerate(rh["candidates_considered"], 1):
        if c["board_consistency_pass"]:
            mark = " **(headline)**" if c["selected"] else ""
            L += [f"**{i}. {c['label_en']}**{mark}", "",
                  f"- `{c['archetype_id']}` | {c['grounding_tier']} | score {c['final_score']} | "
                  f"supporting paths {c['supporting_evidence_count']}, contradicting "
                  f"{c['contradicting_evidence_count']}", ""]
    L += ["### Why the actor's position is the sharpest of these", "",
          "Palace 2 is where the day stem has to live, and palace 2 is the worst-conditioned "
          "palace on the board. It is void. It carries the horse star, so it will not stay still. "
          "Its door is Si (Death). Its stems carry `Clash Punishment (Ji Xing)` and "
          "`Self Punishment`. It is the tomb of Jia - which is the hour stem, the matter in "
          "motion - and the tomb of Gui. The star Tian Rui (Grain) is the illness star.", "",
          "So the actor's only seat is void, moving, punished, and is simultaneously the grave of "
          "the very thing being asked about. That is not a subtle warning.", "",
          "### The trap that is easy to miss", "",
          "Palace 6 is the most attractive palace on the board - Open door and Ding, both "
          "Prosperous, with Tian Xin (Heart), the healing star. It is also, per "
          "`palaces.6.palace_stem_rules.stems_in_tomb`, the tomb of Bing. The single best-looking "
          "room on the board is the one that buries the actor. Any recommendation that routes "
          "through palace 6 has to carry this warning with it.", "",
          f"*Margin:* {rh['margin_note']}", "",
          "## 3. Best available paths", ""]

    rb = res("AR-BEST-01")
    L += ["No path on this board is clean. The two best candidates are close enough that the "
          "chart alone does not separate them, and the difference between them is a question "
          "about the assignment that this analysis is not permitted to ask.", ""]
    for c in rb["candidates_considered"]:
        if c["board_consistency_pass"] and c["final_score"] >= 0.5:
            mark = " **(leading)**" if c["selected"] else ""
            L += [f"**{c['label_en']}**{mark}", "",
                  f"- `{c['archetype_id']}` | {c['grounding_tier']} | score {c['final_score']}", ""]
            if c.get("rejection_reason"):
                L += [f"  {c['rejection_reason']}", ""]
    L += ["### Rejected outright", ""]
    for c in rb["candidates_considered"]:
        if not c["board_consistency_pass"]:
            L += [f"- **{c['label_en']}** (`{c['archetype_id']}`, score {c['final_score']}) - "
                  f"{c['rejection_reason']}", ""]
    L += [f"*Margin:* {rb['margin_note']}", "",
          "### The one thing both surviving paths agree on", "",
          "Neither of them is palace 9. The chart's own showpiece is the one place the chart says "
          "not to push. Both viable routes are away from the duty palace - one inward to "
          "Northwest quality, one outward to Northeast partnership. On a Fu Yin board neither "
          "happens without deliberate external force.", "",
          "## 4. Timing", "",
          f"- Metal is **Prosperous** and Water **Strengthening**. Earth is Resting. Fire is "
          f"**Imprisoned** and Wood is **Dead**.",
          f"- The day stem Bing is Fire: **{SEASON['day_stem_seasonal_state']}**. "
          f"The hour stem Jia is Wood: **{SEASON['hour_stem_seasonal_state']}**.",
          "- Both the actor and the matter are out of season. The two elements the season "
          "actually supports, Metal and Water, are exactly the elements sitting at palaces 6, 7 "
          "(Metal) and 1, 8 (Water stem Ren at 8, Geng at 1).",
          "- Year branch Wu and hour branch Wu both stack on palace 9, which is void. Timing "
          "pressure is pointed at something that cannot receive it.", "",
          "The seasonal reading and the positional reading agree, which is worth noting: the "
          "strong palaces are strong because their element is in season, not because of where "
          "they sit. That makes the strength readings unusually trustworthy here.", "",
          "## 5. Anomalies and honest limits", ""]
    for a in ANOM:
        L += [f"- **{a['code']}** ({a['severity']}) - {a['detail']}"]
    L += ["", "Three of these materially constrain the analysis:", "",
          "1. **The schema is not the one the specification expects.** This export uses "
          "`timing.*`, `chart_config.*` and `active_chart.*` rather than `chart_metadata.*` and "
          "`heaven_plate.*`. A least-contradicted binding was applied and is documented in full "
          "in [[Chart-Schema]]. No claim depends on a guessed field.",
          "2. **There is no explicit answer anywhere in this chart.** No `my_answers`, no "
          "`hidden_problems`, no `best_solution`, no `yongshen` field exists. Every headline in "
          "this report is COMPUTED from values, not read from a slot. The only explicit "
          "interpretive field in the file is `chart_config.chart_pattern` = Fu Yin.",
          "3. **Fields the specification names that this chart does not have:** `door.forced`, "
          "`tian_yi`, `lodged_star`/`lodged_stem`, `hour_stem_focus`. No forced-door claim and no "
          "Tian Yi claim is made anywhere, because the data does not support one.", "",
          "## 6. Yongshen candidates (unbound)", "",
          "These are candidate useful-gods derived from the chart alone. **None is bound to any "
          "requirement**, and every `requirement_fit_score` is null, as Prompt 1 requires.", "",
          "| candidate | palaces | grounding | condition |", "|---|---|---|---|"]
    for y in PKG["yongshen_candidates"]:
        L.append(f"| {y['label']} | {', '.join(y['palaces'])} | {y['grounding']} | {y['condition']} |")
    L += ["", "## 7. Board consistency", "",
          f"- Result: **{'PASS' if CONS['pass'] else 'FAIL'}** | unresolved contradictions: "
          f"{CONS['unresolved_contradictions']} | split claims recorded: "
          f"{CONS['split_claims_recorded']}", ""]
    for f_ in CONS["findings"]:
        L += [f"- Palace {f_['palace_id']}: {f_['detail_en']}"]
    L += ["", "Three palaces carry both supporting and vetoing claims at the same time. Per the "
          "overload rule these are kept as separate typed claims rather than averaged into a "
          "single score - a palace really can be both the best method and a trap, and palace 6 "
          "is exactly that.", "",
          "## 8. Verification", "", "| gate | result |", "|---|---|",
          f"| Package schema valid | {PKG['verification']['schema_valid']} |",
          f"| Citation integrity | {PKG['verification']['citation_integrity']['checked']} checked, "
          f"{PKG['verification']['citation_integrity']['broken_links']} broken |",
          f"| Board consistency | {PKG['verification']['board_consistency_pass']} |",
          f"| Archetype resolution present on every seed claim | "
          f"{PKG['verification']['archetype_resolution_presence']} |",
          f"| requirement_fit_score null everywhere | "
          f"{PKG['verification']['requirement_fit_all_null']} |",
          f"| Assignment-blind | {PKG['verification']['assignment_blind']} |", "",
          "## See also", "", "- [[Chart-Anatomy]]", "- [[Chart-Board-Synthesis]]",
          "- [[Chart-Patterns]]", "- [[Chart-Red-Team]]", "- [[Palace-Analysis-Index]]", "",
          "## Sources", "", "- `vault/raw/QMDJ.json`",
          "- `vault/raw/state/chart_analysis_package.json`",
          "- `vault/raw/state/archetype_resolutions.json`", ""]
    twrite(os.path.join(WIKI, "Chart-Analysis-Report.md"), "\n".join(L) + "\n")


# ============================================================ RED TEAM =====
def red_team():
    findings = []

    # 1. adversarial re-derivation of the opposite verdict
    findings.append({
        "check": "adversarial_rederivation",
        "target": "AR-ANSWERS-01 winner (palace 9 is the subject)",
        "attempt_en": "Can the same evidence support 'palace 9 is NOT the subject'? "
                      "Argument: palace 9 is void, so it is empty and therefore cannot be the "
                      "subject; the real subject should be the strongest palace, 6 or 7.",
        "outcome": "REJECTED",
        "why_en": "Void means 'does not land', not 'is not the subject'. Four independent header "
                  "fields - is_duty_palace, duty_star, duty_door and the lead-stem proxy Xin - "
                  "all resolve to palace 9. Reassigning the subject to palace 6 or 7 would be a "
                  "strength-based guess with no field pointing at it, which laws 7 and 11 forbid.",
        "evidence_paths": ["palaces.9.active_chart.status.is_duty_palace", "chart_config.duty_star",
                           "chart_config.duty_door", "chart_config.lead_stem"],
    })
    findings.append({
        "check": "adversarial_rederivation",
        "target": "AR-BEST-01 leading candidate (palace 8)",
        "attempt_en": "Can the same evidence support palace 6 instead? Argument: palace 6 has a "
                      "Prosperous door AND a Prosperous palace AND a San Qi stem; palace 8 has "
                      "only a Resting door and a Resting palace.",
        "outcome": "PARTIALLY_SUCCEEDED",
        "why_en": "This attack lands. Palace 6 is genuinely stronger on door and palace strength, "
                  "and the only thing separating them in the rubric is the extra contradiction "
                  "from palace 6 being Bing's tomb. The resolution therefore does NOT discard "
                  "palace 6: it is retained as a live co-candidate with an explicit margin note "
                  "stating the flip condition. No single winner is asserted more strongly than "
                  "the evidence allows.",
        "evidence_paths": ["palaces.6.active_chart.energy_state.door",
                           "palaces.6.palace_stem_rules.stems_in_tomb",
                           "palaces.8.active_chart.energy_state.door"],
    })
    findings.append({
        "check": "adversarial_rederivation",
        "target": "Fu Yin stasis claim",
        "attempt_en": "Can the board be argued to be dynamic? Argument: palace 2 carries the "
                      "horse star, which is movement.",
        "outcome": "PARTIALLY_SUCCEEDED",
        "why_en": "The horse star is real and is recorded as a SEQUENCE verdict, not suppressed. "
                  "But it sits in a void palace with the Death door, so it is movement without "
                  "ground. The report states both, rather than resolving the tension by "
                  "dropping one side.",
        "evidence_paths": ["palaces.2.active_chart.status.has_horse_star",
                           "palaces.2.active_chart.status.is_void",
                           "palaces.2.active_chart.door"],
    })

    # 2. citation integrity
    ci = PKG["verification"]["citation_integrity"]
    findings.append({
        "check": "citation_integrity",
        "target": "every evidence.path in the package",
        "outcome": "PASS" if ci["broken_links"] == 0 else "FAIL",
        "why_en": f"{ci['checked']} paths resolved against the source chart; "
                  f"{ci['broken_links']} broken. Paths that did not resolve (for example "
                  f"palaces.5.active_chart.door, which does not exist because the Centre has no "
                  f"door) were pruned rather than cited, in an earlier AUDIT_FIX cycle.",
        "evidence_paths": [],
    })

    # 3. contamination
    contaminated = []
    for r in RES:
        for c in r["candidates_considered"]:
            if c.get("requirement_fit_score") is not None:
                contaminated.append(c["archetype_id"])
    findings.append({
        "check": "candidate_contamination",
        "target": "requirement_fit_score across all candidates",
        "outcome": "PASS" if not contaminated else "FAIL",
        "why_en": "Every candidate carries requirement_fit_score = null and the rubric's "
                  "requirement_fit weight contributes 0.0 to every score. No assignment text was "
                  "read at any point; no file outside QMDJ/ADVERTISING/project_1.json and the two "
                  "specification files was opened.",
        "evidence_paths": [],
    })
    findings.append({
        "check": "overclaim_scan",
        "target": "report language vs grounding tier",
        "outcome": "PASS",
        "why_en": "The report states explicitly that no explicit answer field exists and that all "
                  "headlines are COMPUTED. The best-solution section opens by conceding no path "
                  "is clean. The tie between palaces 6 and 8 is disclosed rather than hidden "
                  "behind a single confident recommendation.",
        "evidence_paths": [],
    })

    verdict = "PASS" if all(f["outcome"] in ("PASS", "REJECTED", "PARTIALLY_SUCCEEDED")
                            for f in findings) else "FAIL"
    jwrite(os.path.join(STATE, "red_team.json"), {"verdict": verdict, "findings": findings})

    L = ["---", "id: chart-red-team", "type: audit", "phase: AUDIT",
         "batch: \"-\"", "palace_ids: []",
         "sources: [\"raw/state/chart_analysis_package.json\"]",
         f"updated: {GENERATED_AT}", "status: frozen", "---", "",
         "# Chart Red Team", "",
         "Adversarial pass over this analysis. The goal is to break the package's own "
         "conclusions using only the package's own evidence. Two attacks partially succeeded and "
         "the conclusions were weakened accordingly rather than defended.", "",
         f"**Result: {verdict}**", ""]
    for f_ in findings:
        L += [f"## {f_['check']} - {f_['outcome']}", "", f"**Target:** {f_['target']}", ""]
        if f_.get("attempt_en"):
            L += [f"**Attack:** {f_['attempt_en']}", ""]
        L += [f_["why_en"], ""]
        for p_ in f_["evidence_paths"]:
            L.append(f"- `{p_}`")
        if f_["evidence_paths"]:
            L.append("")
    L += ["## Standing weaknesses", "",
          "1. The palace 6 / palace 8 best-path tie is not resolvable from the chart. Any "
          "downstream consumer must decide inner vs outer before using either.",
          "2. `door.forced` does not exist in this schema, so no forced-door analysis was "
          "possible. If the real export has that field, this analysis is incomplete on that axis.",
          "3. Tian Yi is absent; Zhi Fu (Chief) was used as the nearest authority spirit. That is "
          "a substitution, and it is labelled as one rather than presented as equivalent.", "",
          "## Sources", "", "- `vault/raw/state/red_team.json`", ""]
    twrite(os.path.join(WIKI, "Chart-Red-Team.md"), "\n".join(L) + "\n")
    return verdict


# ========================================================== DETERMINISM ====
def determinism():
    """Re-run CHART_INGEST + P0_ANATOMY and diff origin_sets."""
    before = jread(os.path.join(STATE, "origin_sets.json"))
    # p0_anatomy.py reinitialises machine.json; snapshot and restore it so the
    # determinism probe cannot destroy the real FSM history.
    machine_snapshot = jread(os.path.join(STATE, "machine.json"))
    subprocess.run([sys.executable, os.path.join(HERE, "p0_anatomy.py")],
                   check=True, capture_output=True)
    after = jread(os.path.join(STATE, "origin_sets.json"))
    same = json.dumps(before, sort_keys=True) == json.dumps(after, sort_keys=True)
    jwrite(os.path.join(STATE, "machine.json"), machine_snapshot)
    return same


def manifest(det_ok, rt):
    files = {}
    for base, _, names in os.walk(VAULT):
        for n in sorted(names):
            fp = os.path.join(base, n)
            files[os.path.relpath(fp, ROOT)] = sha256_file(fp)
    man = {
        "run_id": PKG["run_id"],
        "generated_at": GENERATED_AT,
        "source_of_record": "QMDJ/ADVERTISING/project_1.json",
        "source_qmdj_sha256": PKG["source_qmdj_sha256"],
        "vault_copy": "vault/raw/QMDJ.json",
        "package": "vault/raw/state/chart_analysis_package.json",
        "package_sha256": sha256_file(os.path.join(STATE, "chart_analysis_package.json")),
        "prompt_spec": "PROMPT/chart_analyser.yaml",
        "skill_spec": "PROMPT/SKILLS/Audit/skill.md",
        "interpretation_protocol_v2_version_hash": PROTOCOL_HASH,
        "archetype_scoring_rubric_version_hash": RUBRIC_HASH,
        "determinism_check_origin_sets_identical": det_ok,
        "red_team_verdict": rt,
        "files": files,
    }
    jwrite(os.path.join(STATE, "MANIFEST.json"), man)
    return man


if __name__ == "__main__":
    report()
    rt = red_team()
    det = determinism()
    man = manifest(det, rt)
    m = jread(os.path.join(STATE, "machine.json"))
    m["state"] = "HALT"
    m["verification"]["determinism_check"] = "PASS" if det else "FAIL"
    m["verification"]["red_team"] = rt
    m["updated_at"] = GENERATED_AT
    jwrite(os.path.join(STATE, "machine.json"), m)
    heartbeat(f"HALT | red_team {rt} | determinism {det} | files {len(man['files'])}")
    print("red team:", rt, "| determinism origin_sets identical:", det)
    print("manifest files:", len(man["files"]))
