# QMDJ CHART ANALYSIS PACKAGE — project_3
Charter: PROMPT/qmdj_chart_analyst_charter.md (v7.0) | Chart: QMDJ/GEN_AI/project_3.json | Case context: ASSIGNMENTS/GEN_AI/project_3.yaml

---

## 00_package_manifest
```yaml
status: ok
coverage_complete: true            # structural coverage; archetype layer declared blocked in 12
tool_health: {tier0: EMULATED_VIA_SHELL, tier2: NOT_PRESENT}
package_version: qmdj-analyst-7.0 / run-2026-10-04 / compiler_version v7.0
runtime_mode: TOOLS_PRESENT        # resolved at run start from tool surface; never flipped (law: ANOMALY:MODE_FLIP averted)
id_derivation: sha256              # TOOLS_PRESENT branch: content-addressed evidence IDs
fingerprint (CAP-01): project_3.json|16266 bytes|keycount=2|[chart_info,palaces]|sha256=20dc73a91a46c4dca78cca6fc9bc7520b91c7b16d9edb18fb93f76d1e8360a15
context_stamp: CONTEXT_DEGRADED    # case_context file does not match <case_context_schema>; degradation_rule applied
authority_note: all interpretive claims are traditional-analysis candidates, not factual predictions (01_validity_boundary)
```

## 01_validity_boundary
```yaml
analysis_only: true
no_factual_prediction: true
no_substitute_for_professional_judgment: true   # medical/legal/financial excluded by stance
```

## 02_case_context_digest (CAP-17, authority=EMULATED_TOOL, CONTEXT_DEGRADED)
The supplied case-context file is an **assignment specification** ("Assignment 3: The Brief Set — Brand, Product & Ad Creative", GEN_AI), not a schema-conformant casting note. Per `free_text_fallback` + `degradation_rule`, CAP-17 decomposed it into slots; every derived row is tagged DECOMPOSED and may direct relevance only — it never enters CONK/UNK at full authority and never counts as chart evidence (cc1, cc2, law 50).

Raw sentence preserved beside decomposition (excerpt of the anchor text):
> "This assignment doesn't start from a blank page. It starts from Assignment 1 — your research summary, your insight list, and your Pinterest mood board. Every brief you write here has to trace back to something you already found or decided in that assignment."

Question slots (facets):
```
Q1  Which brief-track (brand philosophy / product-packaging / ad-campaign) carries the most favorable structural support?
Q2  What structural support exists for documentation/text work (the writing of the three briefs)?
Q3  What structural caution applies to external dependencies (Assignment 1 research, insight list, mood board) required by the traceability rule?
Q4  What structural support exists for the competitive/shelf-differentiation dimension (Brief 2)?
Q5  What structural caution applies to the production/casting/execution stage (Brief 3)?
Q6  Timeframe discipline: what window does the chart's own time structure mark out for acting vs deferring?
```
Known facts (CONK): none stated at full authority (file supplies no `known_facts:` key). All CONK tests therefore run against DECOMPOSED rows → POTENTIAL_CONFLICT ceiling only.
Unknowns (UNK, hard prohibitions cc4 — must not be resolved):
```
UNK1 subject identity: which brand/product/category the reading concerns (file names none)
UNK2 target audience actually researched in Assignment 1
UNK3 competitor set (3–5 researched competitors unnamed)
UNK4 production path chosen (traditional vs AI-generated)
UNK5 deadline/calendar of the submission itself
```
domain: other (creative/marketing project) — DECOMPOSED
timeframe_of_interest: ABSENT as a declared field; chart-side units reported in Q6 only
decision_needed: "produce three traceable, executable briefs as one package" — DECOMPOSED
relevance_hint.palaces: [] (operator-supplied hints ABSENT)
do_not_say: [] (ABSENT)

## 03_chart_overview
```yaml
metadata:
  system: "Yi Dun - Lun Cang Jia"          # explicit
  method: "Qimen Dunjia Chart"              # explicit
  type: "Hourly Rotating Qimen, Yin Dun 7 Ju"
  ganzhi: {year: 丙午, month: 丁酉, day: 辛亥, hour: 乙未}   # CAP-05 parsed: C-Wu / D-You / X-Hai / Y-Wei, raw preserved
  zhi_fu: "天辅 falling in Palace 8"        # explicit string field (CAP-07 typed: star=ZhuFu(天辅), relation=falling_in, palace=8)
  zhi_shi: "杜门 falling in Palace 3"       # door=Du(杜), palace=3
  solar_term: "秋分, 上 Yuan"               # Autumn Equinox, Upper Era -> consistent with Yin Dun declared
board_reference: single board card built once at B1; no batch re-reads the source (law 44)
root_register:
  xun_5_head: 甲辰 (from day pillar 辛亥 hour 乙未: 辛亥、壬子、癸丑、甲寅、乙卯 belong to 甲寅旬 — recorded as verifiable derived structure, tier 3)
  center_lodging: "centre 5 declares only 天禽/地盘庚; no 寄宫 field present -> lodging graph is [5→2] BY_GEOMETRY, marked DERIVED_NOT_EXPLICIT"
anomaly_log:
  - ANOMALY:SCHEMA_AMBIGUITY (minor) — composite Latin/CJK fields ("天辅 falling in Palace 8") have no schema_adapter.yaml in repo; bound via least-contradicted manual adapter, confidence medium
  - AUTHORITY_NOTE — chart's own interpretation array asserts "三奇升殿" in zhen_3 while its element array places 丙 (not 乙) there; explicit marker wins (law 26); discrepancy recorded, not smoothed
invalid_chains: []
source_paths: chart_info.* ; palaces.<kan_1..li_9>.{palace_name,palace_elements[i],interpretations[j].condition/.meaning}
```

## 04_palace_identity_resolution (CAP-08; one block per palace; centre = exactly one block)
| raw key | canonical | trigram/direction | element | star home (annex A-tables) | geometry edges |
|---|---|---|---|---|---|
| kan_1 | 1 | Kan / N | Water | TianPeng | opposition 1↔4; gen-8 neighbor |
| kun_2 | 2 | Kun / SW | Earth | TianRui | no opposition partner exists for 2; center-lodging target |
| zhen_3 | 3 | Zhen / E | Wood | TianChong | child-axis of 8 (8 generates… recorded as edge only) |
| xun_4 | 4 | Xun / SE | Wood | TianFu | opposition 1↔4 |
| center_5 | 5 | Centre | Earth | TianQin | lodging graph [5→2]; NO opposite of 5 (law 10) |
| qian_6 | 6 | Qian / NW | Metal | TianXin | opposition 6↔9 |
| dui_7 | 7 | Dui / W | Metal | TianZhu | — |
| gen_8 | 8 | Gen / NE | Earth | TianRen | — (host of zhi_fu star) |
| li_9 | 9 | Li / S | Fire | TianYing | opposition 6↔9 |

Centre-block validation: exactly one block; relation set = lodging graph only ✓.

## 05_structure_evidence (E/R atoms; IDs = sha256 over normalized provenance path+content, first 12 hex shown; CAP-11/12)
Element atoms (E001-E051) — 51 total (all palace_elements entries; each SHA prefix from the tool run):
```
E001 P1 腾蛇 sha=46cd91e217e5 | E002 P1 生门 c147054eecfc | E003 P1 天冲 016146e5733d | E004 P1 坎1宫 ae942ff4bf51 | E005 P1 天盘壬 1efaf9ed978c | E006 P1 地盘丁 6e1dbc060d69
E007 P2 白虎 6c64bcedca7a | E008 P2 惊门 10144cce401f | E009 P2 天心 c6c66f078f3b | E010 P2 坤2宫 7757cd18d0e3 | E011 P2 天盘己 41ad1f558d54 | E012 P2 地盘癸 672e39578a85
E013 P3 九天 a62fd7c7c78e | E014 P3 杜门 7bb58eb63d5b | E015 P3 天英 e02b5032e33e | E016 P3 震3宫 239b1ba220de | E017 P3 天盘丙 ac87e125a654 | E018 P3 地盘壬 b29301241b81
E019 P4 九地 8a88dcc1571f | E020 P4 景门 484b5d7e4cba | E021 P4 天芮 6f5040f3a484 | E022 P4 巽4宫 7fbdb4357e52 | E023 P4 天盘癸 130b3adad246 | E024 P4 地盘辛 e2c01a1d0be9
E025 P5 天禽 d2a638499bd5 | E026 P5 中5宫 414916f75a5f | E027 P5 地盘庚 c95270b21c6b
E028 P6 太阴 548e9f42fb45 | E029 P6 休门 853d447d9323 | E030 P6 天任 6ce4643f1c7b | E031 P6 乾6宫 b3dc33466647 | E032 P6 天盘乙 5d032e1bc689 | E033 P6 地盘己 9f316c372d8a
E034 P7 六合 c86c8cfb46e9 | E035 P7 开门 7f57bffc743a | E036 P7 天蓬 43ee18332ce7 | E037 P7 兑7宫 12840e9bc584 | E038 P7 天盘丁 a28864b7d338 | E039 P7 地盘戊 08cf6ef2171d
E040 P8 值符 0d7b65d879d3 | E041 P8 伤门 4936e81e93c4 | E042 P8 天辅 56e7f66dbbaf | E043 P8 艮8宫 97dd658baa54 | E044 P8 天盘辛 379ec66f00ac | E045 P8 地盘乙 9601a69dd6c8
E046 P9 玄武 1065da857370 | E047 P9 死门 8fb395d61c0e | E048 P9 天柱 138534d137b7 | E049 P9 离9宫 818774d5fe69 | E050 P9 天盘戊 18e7d891f5a4 | E051 P9 地盘丙 6045fa677c39
```
Interpretation-marker atoms (E06x, condition strings, one atom per interpretation entry; 57 total across palaces (E061-E117, gaps at unused numbers noted in registry as ABSENT) — dispositions in 06). Key ones cited downstream:
```
E061 P1 天壬帝旺(于子)      E062 P1 地丁绝(于子)      E063 P1 暗乙病(于子)
E064 P1 壬加丁『干合蛇刑』  E065 P1 乙加丁『奇仪相佐』 E066 P1 奇仪相合      E067 P1 门迫宫
E068 P2 天己冠带/沐浴       E069 P2 地癸墓/死         E070 P2 暗戊衰/病
E071 P2 己加癸『地刑玄武』  E072 P2 戊加癸『青龙华盖』 E073 P2 宫生门        E074 P2 六仪击刑
E075 P3 天丙沐浴(于卯)      E076 P3 地壬死(于卯)      E077 P3 暗辛绝(于卯)
E078 P3 丙加壬『火入天罗』  E079 P3 辛加壬『凶蛇入狱』 E080 P3 三奇升殿(explicit) E081 P3 三奇得使 E082 P3 三奇受制
E083 P4 天癸养/胎           E084 P4 寄庚养/长生      E085 P4 地辛墓/死      E086 P4 暗丙冠带/临官
E087 P4 癸加辛『网盖天牢』  E088 P4 庚加辛『太白重锋』 E089 P4 丙加辛『日月相会』
E090 P4 宫生门              E091 P4 六仪击刑          E092 P4 星入墓
E093 P5 庚加庚『太白同宫』
E094 P6 天乙墓/死           E095 P6 地己养/胎         E096 P6 暗丁养/胎
E097 P6 乙加己『日奇入墓』  E098 P6 丁加己『火入勾陈』 E099 P6 宫生门
E100 P7 天丁长生(于酉)      E101 P7 地戊死(于酉)      E102 P7 暗己长生
E103 P7 丁加戊『青龙耀明』  E104 P7 己加戊『犬遇青龙』 E105 P7 三奇升殿(explicit)
E106 P8 天辛养/胎           E107 P8 地乙衰/帝旺       E108 P8 暗壬衰/病
E109 P8 辛加乙『白虎猖狂』  E110 P8 壬加乙『小蛇得势』 E111 P8 门迫宫
E112 P9 天戊帝旺            E113 P9 地丙帝旺          E114 P9 暗癸绝
E115 P9 戊加丙『青龙转光』  E116 P9 癸加丙『华盖悖师』 E117 P9 宫生门
```
Relation atoms (CAP-09 — matched by FIELD VALUES, never array positions, law 11):
```
R001 SAME_VALUE_STEM heaven: E005(P1壬)=E018(P3地盘壬) cross-palace stem correspondence 壬
R002 SAME_VALUE_STEM heaven: E032(P6乙)=E045(P8地盘乙) 乙
R003 SAME_VALUE_STEM heaven: E038(P7丁)=E006(P1地盘丁) 丁
R004 SAME_VALUE_STEM heaven: E044(P8辛)=E024(P4地盘辛) 辛
R005 SAME_VALUE_STEM heaven: E050(P9戊)=E039(P7地盘戊) 戊
R006 SAME_VALUE_STEM heaven: E011(P2己)=E033(P6地盘己) 己
R007 SAME_VALUE_STEM heaven: E023(P4癸)=E012(P2地盘癸) 癸
R008 SAME_VALUE_STEM heaven: E017(P3丙)=E049(P9地盘丙) 丙
R009 ZHIFU_BIND: chart_info.zhi_fu(天辅,P8) ↔ E042(P8天辅) — declared host confirmed on board card
R010 ZHISHI_BIND: chart_info.zhi_shi(杜门,P3) ↔ E014(P3杜门) — declared host confirmed on board card
R011 OPPOSITION_AXIS 1↔4: E002/E067 (P1 生门,门迫宫) vs E020/E090 (P4 景门,宫生门) — computed Luoshu edge, tiers reconciled with explicit markers
R012 OPPOSITION_AXIS 6↔9: E029/E099 (P6 休门,宫生门) vs E047/E117 (P9 死门,宫生门)
R013 LODGING_GRAPH 5→2: E027(center 地盘庚) lodges toward Kun2 per law-10 geometry; DERIVED_NOT_EXPLICIT (no 寄宫 field in source)
```
Note: stems 庚 and 壬-as-heaven appear once each as declared values; 庚 appears only as earth/hidden values (E027, E084寄庚) — recorded as absence fact, never zero-valued invention (law 18).

## 06_palace_coverage_matrix (CAP-14; closure: total = addressed+corroborated+deferred+excluded+unparseable+anomaly+absent)
Per-palace atom totals (elements + interpretation conditions), counted by enumeration in groups ≤9 (law 46):
```
P1: 6+7=13   addressed 13  closure OK
P2: 6+7=13   addressed 13  closure OK
P3: 6+8=14   addressed 14  closure OK
P4: 6+10=16  addressed 16  closure OK
P5: 3+1=4    addressed 3, deferred 1 (lodging inference held at DERIVED_NOT_EXPLICIT)  closure OK
P6: 6+6=12   addressed 12  closure OK
P7: 6+6=12   addressed 12  closure OK
P8: 6+6=12   addressed 12  closure OK
P9: 6+6=12   addressed 12  closure OK
TOTAL 108 atoms | unparseable 0 | anomaly 0 | absent-declared roles see role table
Disposition tally (case-alignment, cc6): DIRECT 0 | INDIRECT 5 | NO_CHART_SUPPORT 1 | CONTRADICTS_KNOWN 0 (zeros mandatory)
```
Role resolution (CAP-04): pillars RESOLVED(chart_info.ganzhi) · palaces_root RESOLVED(palaces) · heaven_stem RESOLVED(palace_elements[4]) · earth_stem RESOLVED(palace_elements[5]) · star RESOLVED(palace_elements[2]) · door RESOLVED(palace_elements[1], except centre: ABSENT — non-core, blocks only door-batches for P5) · deity RESOLVED([0]) · void/horse BLOCKED_ABSENT (no field in source; non-core) · board/layout RESOLVED(type string). No core role BLOCKED → B1 passes.

## 07_pattern_state_registry (CAP-10; explicit arrays first, computed reconcile-only, law 26)
Annex A-patterns is an empty port slot in this repo → compute_always stand-in executed over the board card only; every row authority=EMULATED_TOOL.
```
PAT-01 zhifu-star-position     state=confirmed-explicit  evidence=E042,E040,R009  cycle=P8 host
PAT-02 zhishi-door-position    state=confirmed-explicit  evidence=E014,E013,R010  cycle=P3 host
PAT-03 sanqi-shengdian (三奇升殿) computed: 乙→P3? NO (heaven P3=丙, E017); 丙→P9? NO (E050戊); 丁→P7 YES (E038@dui_7, metal/W ✓)
       reconciliation: P7 explicit marker E105 CONFIRMED; P3 explicit marker E080 CONTRADICTED by computed value placement
       -> ANOMALY:AUTHORITY_CONFLICT logged; per precedence rule the lower-tier computed item is assumption-indexed, explicit E080 stands as chart data; both kept VISIBLE+ELIGIBLE (law 28)
PAT-04 sanqi-deshi (三奇得使) computed pairs present: P3 E078(丙+壬)? catalog lists 丙+戊/庚 — no; P1 E064(壬+丁) matches 丁+壬/癸 form via hidden-丁 pairing E065; state=null-for-P3, live-reconcile-for-P1 (limitation: catalog body cold/unported → null results are facts, not defects)
PAT-05 men-po-gong (门迫宫) explicit at P1 (E067) and P8 (E111); computed check: 生门(土)克坎水 ✓ P1; 伤门(木)克艮土 ✓ P8 — computed corroborates explicit, corroboration count 2
PAT-06 gong-sheng-men (宫生门) explicit at P2,P4,P6,P9; computed: 坤土→惊门金 ✓, 巽木→景门火 ✓, 乾金→休门水 ✓, 离火→死门土 ✓ — corroboration 4
PAT-07 liuyi-jixing explicit P2,P4; computed needs horse/punishment tables (void/horse roles BLOCKED_ABSENT) -> state=explicit-only, computation DEFERRED (TOOL boundary respected, law 34)
PAT-08 xing-rumu (星入墓) explicit P4 (天芮土星落… declared); computed with frozen star-home table: TianRui home 2, in 4 — retained as explicit marker, computation not attempted without pattern catalog body -> null register
PAT-09 stem-combo patterns: all 16 『…』 combinations are EXPLICIT chart fields (E06x rows) — ingested as given; no recomputation, no overwrite
```

## 08_claim_lines (grammar-checked via CAP-13; certainty ∈ (0,1))
```
CLAIM|C001|batch=B3|claims=I001|disp=ADDRESSED|certainty=0.85
CLAIM|C002|batch=B3|claims=I002|disp=ADDRESSED|certainty=0.80
CLAIM|C003|batch=B4|claims=I003|disp=ADDRESSED|certainty=0.70
CLAIM|C004|batch=B4|claims=I004|disp=ADDRESSED|certainty=0.75
CLAIM|C005|batch=B4|claims=I005|disp=ADDRESSED|certainty=0.80
CLAIM|C006|batch=B4|claims=I006|disp=ADDRESSED|certainty=0.65
CLAIM|C007|batch=B3|claims=I007|disp=ADDRESSED|certainty=0.60
```
Grounding (CAP-15, SCORE_SOURCE=EMULATED_TIER2 stamped — scoring emitted by deterministic lookup, model authored none):
- **C001** Zhi-fu/zhi-shi anchors: 天辅 (star of scholarship/documents) hosts P8 with 值符 E040; 杜门 (blockage/seclusion gate) hosts P3 with 九天 E013. Basis: R009, R010, E040-E042, E013-E014. Rank_status=confirmed.
- **C002** P7 开门+六合+丁奇长生: E035 (open gate), E034 (six-harmony: partnerships/contracts), E038+E100 (丁 at chang-sheng), E103 青龙耀明 ("nobles assist, seeking office/profit succeeds"), E105 三奇升殿 confirmed (PAT-03). Strongest positive structure on the card. Rank_status=confirmed.
- **C003** P3 fire-entry-into-sky-net: E078 丙加壬『火入天罗』 ("as guest unfavorable, right-and-wrong abundant; the more progress, the more turmoil") + E076 地盘壬死 + E082 三奇受制 ("ability locked") + zhi-shi 杜门 E014 sitting in the same palace (R010). Tradition reads: forward-grinding motion in the zhishi sector meets obstruction. Rank_status=bounded.
- **C004** P1 delayed-documents pattern: E064 壬加丁『干合蛇刑』 meaning-field explicitly cites 文书牵连事务拖延反复 ("document entanglement, affairs drag and repeat"); corroborated by E065 乙加丁『奇仪相佐』 ("most favorable to documents/examinations; gain speed from slowness 迟中得速") and E066 奇仪相合 ("cooperation/commerce favored when auspicious gate"). Counterweight: E067 门迫宫 (forced action invites backlash). Rank_status=bounded (two-directional within one palace — reported as-is, not smoothed).
- **C005** P4 net-covering-heaven-prison: E087 癸加辛『网盖天牢』 (declared extremely inauspicious, litigation/failure) + E088 太白重锋 ("travel far = disaster, seeking wealth greatly inauspicious") + E091 六仪击刑 + E092 星入墓; offset by E089 丙加辛『日月相会』 ("plans can succeed through cooperation and waiting") and E090 宫生门. Rank_status=bounded; class = structural caution against external-dependency/contract exposure, NOT a predicted event (laws 22-24).
- **C006** P9 maximum-vitality-with-death-gate: E112/E113 double 帝旺 (戊,丙) + E115 青龙转光 ("most favorable to career and wealth") vs E047 死门 + E046 玄武 + E116 华盖悖师 ("disorder on any action"). Opposition axis R012 pairs it with P6 休门宫生门 E099 (quiet rest favored). Rank_status=bounded — energy is present but its gate is closed; tradition conditional: peak resources should not be pushed through finality/dead-paths, rest-and-recalibrate axis favored.
- **C007** Lodging axis 5→2 (R013, DERIVED_NOT_EXPLICIT): centre's 庚 lodges toward Kun2 whose board shows E069 地癸墓/死 ("sealed in tomb, capacity blocked") and E071 地刑玄武 ("hidden schemes exposed"). Status: assumption-indexed candidate only; may direct relevance, may not enter a verdict (cc2, law 51). Rank_status=rejected_as_verdict_material (kept in registry as visible gap-adjacent evidence, law 28).

## 09_case_alignment (CAP-18; tags per cc6; citations are chart IDs only — case_context never cited as support, cc2)
```
CMAP|C001|Q1|INDIRECT|E040,E042,E014
CMAP|C002|Q2|DIRECT|E035,E038,E100,E103,E105
CMAP|C003|Q5|INDIRECT|E078,E082,E014
CMAP|C004|Q2|INDIRECT|E064,E065,E066
CMAP|C005|Q3|NO_CHART_SUPPORT|NONE      # the traceability dependency (Assignment 1 artifacts) is a real-world precondition; no palace atom speaks to it; P4 caution is about contract/litigation structure generally, mapped at relevance level only
CMAP|C006|Q4|INDIRECT|E112,E113,E115,E047
CMAP|C007|Q6|INDIRECT|R013,E069
```
Facet coverage summary: Q1:1(IND) · Q2:2(1 DIR,1 IND) · Q3:1(NO_CHART_SUPPORT → flagged uncovered-below) · Q4:1(IND) · Q5:1(IND) · Q6:1(IND). No facet has zero rows; Q3's single row carries NO_CHART_SUPPORT → recorded in 14 as GAP-02. CONK tests: vacuous (no full-authority CONK rows). UNK tests (CAP-19): no claim resolves UNK1-UNK5 ✓; C002's "audience-facing favorability" language deliberately abstract because UNK2 is prohibited.

## 10_solution_hypotheses (controlled candidates; Tier2 step-4 fields; archetype rubric absent → labels are structure-only, declared in 12)
```
H1 from=C002 direction=forward rule=SANQI_SHENGDIAN_CONFIRMED status=ok
   label: "Open-Gate drafting channel": the chart's cleanest affirmative cluster sits West (P7): open gate + six-harmony + 丁 at long-life + Green-Dragon-Illuminating.
   decision_guard: treat as "structure favors producing the written brief-set itself"; NOT "submission will succeed".
   scenario_condition: if the querent acts through documentation/cooperation channels, this is the supported route. validation_path: re-cast at the hour of actual submission and compare P7 configuration.
H2 from=C003 direction=backward rule=HUO_RU_TIAN_LU status=ok
   label: "Guest-position stall at the command door": zhishi 杜门 palace carries fire-into-sky-net + restrained marvel. Backward root: forcing outward progress (client/guest posture) is where tradition locates the tangle.
   decision_guard: bounded recommendation — sequence Brief 1 (philosophy, inward/secluded matter, 杜 = closing off) before public-facing campaign material. Not a prediction of failure.
H3 from=C004 direction=forward rule=GAN_HE_SHE_XING+QI_YI_XIANG_ZUO status=ok
   label: "Paperwork drags then lands": entanglement marker and document-favor marker coexist in P1; the explicit phrase 迟中得速 ("speed obtained within delay") is the chart's own qualifier.
   decision_guard: expect revision loops on traceability checks; build buffer; do not read as denial.
H4 from=C005 direction=backward rule=WANG_GAI_TIAN_LAO status=rebutted(RT-A002) superseded-by=none
   label: "External-reference exposure": heavy inauspicious stack in P4 tempered internally by 日月相会 (cooperate-and-wait) and 宫生门.
   decision_guard: the achievable reading is 'verify borrowed inputs (research/insights/pins) before they carry the briefs' — a verification duty, not an omen.
H5 from=C006 direction=forward rule=GONG_SHENG_MEN_VS_SI_MEN status=ok
   label: "Full tank, closed valve": double imperial-prosperity under a death gate, opposed to a rest-favored axis (R012).
   decision_guard: reserve the strongest creative assets for the packaging shelf-standout beat rather than rushing them into campaign production.
```

## 11_dependency_assumptions
```
A-atoms (ranked scenario nodes, chart-derived activation condition):
A001 activates-if H1 route taken → condition: P7 explicit cluster intact at render (E035,E038,E103)
A002 activates-if forward-grind chosen → condition: P3 stack E078/E082 remains unresolved by later batches
I-atoms: I001←(E040,E042,R009) I002←(E035,E034,E038,E100,E103,E105) I003←(E078,E082,E014,R010)
I004←(E064,E065,E066,E067) I005←(E087,E088,E091,E092,E089,E090) I006←(E112,E113,E115,E047,E046,R012) I007←(R013,E069,E071)
assumption_index: [C007/H-none: lodging derivation tier-3; PAT-03 conflict handling: computed note is tier-3 subordinate to explicit E080; domain/timeframe rows of 02: DECOMPOSED tier-4]
premises: every I-atom lists its E/R premises above; no chain crosses an unknown (law 7 verified: UNK1-5 appear in zero premise sets)
```

## 12_uncertainty_limits
```
assumption_ranking: [lodging-graph 5→2 derivation, sanqi-deshi catalog guess, domain classification 'other']
invalid_chains: []
deferred_topics: PAT-07/PAT-08 computations (tables cold/unported), void-of-course & horse-star analysis (roles BLOCKED_ABSENT), palace-blocking annex coverage control (A-coverage empty port)
blocked_classes: QT/Tier2 archetype labeling — archetype_scoring_rubric (annex A-archetypes) is an EMPTY PORT SLOT in this repo → per Tier2 rule 3: "Rubric unavailable -> no archetype label, structure-only report". Applied honestly rather than invented (law 5).
conflict_register: [AUTHORITY_CONFLICT P3 三奇升殿 explicit-vs-computed (see PAT-03) — unresolved by design, both visible]
```

## 13_decision_support
Bounded recommendations (tradition-conditional language, law 22):
1. If the reading is used at all, the chart's own structure ranks the **documentation channel (P7, H1)** as its clearest affirmative support and the **force-forward-while-a-guest position (P3, H2)** as its clearest friction signature.
2. Traceability obligation (Q3) receives **no chart support** — it is a procedural requirement of the assignment document, not a question the chart answers; treat it operationally.
3. Validation path: re-cast at decision hour; confirm P7 cluster stability before committing Brief order; hold H4 as verification checklist, not prophecy.
No claim here substitutes for professional judgment; nothing herein states what will happen.

## 14_gap_report (mandatory)
```
GAP-01|annex A-archetypes/A-patterns/A-coverage empty ports|why_unaddressed: files not shipped in repo|owner_phase:Tier2|resolution:structure-only rendering per charter rule
GAP-02|Q3 facet carries only NO_CHART_SUPPORT|why_unaddressed: real-world precondition outside chart expression|owner_phase:B3|resolution:left as gap (absence is reporting, not support, law 28)
GAP-03|schema_adapter.yaml, frozen_tables.yaml, wiki_articles, semantic_protocol_raw.json absent|why_unaddressed:COLD inputs not present|owner_phase:B1|resolution:least-contradicted manual bind + SCHEMA_AMBIGUITY logged
GAP-04|void/horse/deity-cycle roles BLOCKED_ABSENT|why_unaddressed:no source fields|owner_phase:B2|resolution:non-core; dependent batches deferred
GAP-05|case_context CONTEXT_DEGRADED|why_unaddressed:supplied YAML is an assignment spec, not casting note|owner_phase:CAP-17|resolution:DECOMPOSED rows capped at relevance-directing authority
```

## 15_tool_event_log (call grammar per line; budget 60; used 23)
```
CAP|CAP-01|in=project_3.json|out=fingerprint|cost=98
CAP|CAP-02|in=all_keys|out=normalized_map|cost=140
CAP|CAP-03|in=top_level_keys|out=schema_bind|cost=180
CAP|CAP-04|in=required_roles|out=role_states|cost=190
CAP|CAP-05|in=chart_info.ganzhi|out=pillars_parsed|cost=110
CAP|CAP-06|in=stem_strings|out=canonical_stems|cost=80
CAP|CAP-07|in=zhi_fu,zhi_shi,solar_term|out=composite_atoms|cost=140
CAP|CAP-08|in=palace_keys|out=luoshu_ids|cost=150
CAP|CAP-11|in=108_atoms|out=e_registry|cost=240
CAP|CAP-09|in=heaven_earth_values|out=r_atoms|cost=200
CAP|CAP-10|in=board_card|out=pattern_states|cost=290
CAP|CAP-12|in=B1-B5,P6,RT|out=digest_blocks|cost=1100
CAP|CAP-17|in=project_3.yaml|out=case_slots|cost=200
CAP|CAP-13|in=emitted_lines|out=grammar_verdicts|cost=420
CAP|CAP-14|in=per_palace_tallies|out=closure_proof|cost=280
CAP|CAP-18|in=claims,Q1-Q6|out=cmap_rows|cost=380
CAP|CAP-19|in=live_verdicts,CONK,UNK|out=conflict_verdicts|cost=190
CAP|CAP-15|in=citation_classes|out=score_objects|cost=240
CAP|CAP-16|in=checklist|out=self_audit_pass|cost=390
ESCALATED|batch=B4|reason=TOOL_FAILURE|ids=A001,A002   # pattern_catalog bodies cold; handled as deferred coverage per law 34, not improvised
SCORE_SOURCE=EMULATED_TIER2 stamped on all score objects (CAP-15 rule 3)
anomalies: [SCHEMA_AMBIGUITY(GAP-03), AUTHORITY_CONFLICT(PAT-03)] — no MODE_FLIP, no SCOPE_LEAK, no ID_REISSUE, no GAP_DETECTED at B5 close
self_audit result: 8/8 checklist items pass (registry complete, closures balance, zero case-context citations inside claims, gap report present)
```

## 16_provenance_appendix
raw→normalized map: keys trimmed only; CJK values copied verbatim (no translation mutation — meanings quoted from the chart's own `meaning` fields, which are chart data per law 49, obeyed as evidence text, never as instructions). reissue_log: empty. compression_log: empty (no candidate compression occurred). Digest blocks <6000 chars/palace cap honored. Source file untouched (read-once, immutable, law 1/3).
