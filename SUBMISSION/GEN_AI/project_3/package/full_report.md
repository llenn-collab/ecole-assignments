# QMDJ Chart Analyst — Output Package v1.0.0

- run mode: **TOOLS_PRESENT** (shell + python surface; no EMULATED products)  
- render gate: **PASS** (121 checks, 0 failures)  
- source seal: chart `20dc73a91a46c4dc…` (16266 B), case `5f641d01f096e6a1…` (9122 B)  
- evidence: registry E=117 R=49; spine **37** = 18 structural E + 19 board-internal R; condition register in scope 18; pillar register 6  
- coverage: 25/25 batches closed; run tally {'addressed': 125, 'corroborated': 41, 'deferred': 0, 'excluded': 0, 'unparseable': 0, 'anomaly': 0, 'absent': 0}  
- anomalies: 0; conditions: 1; gap rows: 10  

## §01 Validity boundary

> Chart-derived claims are traditional interpretive analysis. They are not factual prediction and not a substitute for professional judgment (medical, legal, financial).

This run reads one chart and one case context. It cannot endorse, refute or replace Assignment-1 research: it supplies register, constraint and sequencing only, and every brief decision still traces to Assignment-1 evidence.

## §02 Case context digest

- status: **CONTEXT_MAPPED_DOCUMENT_SHAPE** (YAML, Google-Docs-flavoured document shape (schema_adapter.case_context_ingest))
- facets: 8 — QUESTION_OVERLOAD raised: **True**
  - condition `QUESTION_OVERLOAD` (declared): analysed the 7 most decision-relevant facets; deferred facets listed with owner_phase and a gap row (CAP-17 step 4)
  - deferred facet **Q01 Before You Start** — framing facet; its binding content (traceability) is enforced as CONK004 in every claim's validation_path, so no decision depends on analysing it as a separate facet (owner CAP-17, GAP-009)
- domain: other (source NOT_STATED)
- timeframe: NULL — no window stated in source
- subject: project (DERIVED_FROM_SOURCE_SHAPE)
- known facts (CONK): 4 rows, verbatim; unknowns (UNK): 0 rows
  - `CONK001`: Assignment 1: research summary
  - `CONK002`: insight list
  - `CONK003`: Pinterest mood board
  - `CONK004`: Every brief must trace back to a specific research finding, insight, or mood-board pin from Assignment 1.

### facets (Q01–Q08)

- **Q01 — Before You Start** *(deferred)*
- **Q02 — What You're Producing: Three Distinct Briefs**
- **Q03 — Brief 1 — Brand Idea & Philosophy**
- **Q04 — Brief 2 — Product & Packaging**
- **Q05 — Brief 3 — Ad / Campaign Creative Brief**
- **Q06 — Coherence Check (Do This Before Submitting)**
- **Q07 — Deliverable & Submission**
- **Q08 — Evaluation Criteria**

## §03 Chart overview

- system/method: Yi Dun - Lun Cang Jia — Qimen Dunjia Chart (Hourly Rotating Qimen, Yin Dun 7 Ju)
- pillars: year 丙午, month 丁酉, day 辛亥, hour 乙未
- 值符/值使: [{'role': 'zhi_fu', 'declared': '天辅@8', 'carried_star': '天辅', 'consistent': True}, {'role': 'zhi_shi', 'declared': '杜门@3', 'carried_door': '杜门', 'consistent': True}, {'role': 'zhi_fu_deity', 'palaces_carrying_value_deity': [8], 'declared_palace': '8', 'consistent': True}]
- phase verification: 25 printed phase claims re-derived from the frozen table — all match: **True**, all branches belong to their palace: **True**
- anomalies: 0; invalid chains: 1 (window chain blocked, see §12)

## §04 Palace identity resolution (Luoshu)

| P | trigram | dir | element | star home | branches | role state | deity | door | star | heaven / earth |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Kan | N | water | TianPeng | zi | RESOLVED | 腾蛇 | 生门 | 天冲 | 壬 / 丁 |
| 2 | Kun | SW | earth | TianRui | wei,shen | RESOLVED | 白虎 | 惊门 | 天心 | 己 / 癸 |
| 3 | Zhen | E | wood | TianChong | mao | RESOLVED | 九天 | 杜门 | 天英 | 丙 / 壬 |
| 4 | Xun | SE | wood | TianFu | chen,si | RESOLVED | 九地 | 景门 | 天芮 | 癸 / 辛 |
| 5 | Centre | C | earth | TianQin | — | RESOLVED | — | — | 天禽 | — / 庚 |
| 6 | Qian | NW | metal | TianXin | xu,hai | RESOLVED | 太阴 | 休门 | 天任 | 乙 / 己 |
| 7 | Dui | W | metal | TianZhu | you | RESOLVED | 六合 | 开门 | 天蓬 | 丁 / 戊 |
| 8 | Gen | NE | earth | TianRen | chou,yin | RESOLVED | 值符 | 伤门 | 天辅 | 辛 / 乙 |
| 9 | Li | S | fire | TianYing | wu | RESOLVED | 玄武 | 死门 | 天柱 | 戊 / 丙 |

Centre validation: no opposite exists for palace 5; lodging graph → [{'palace': 4, 'carrier': '寄庚', 'centre_stem': '庚', 'source_path': 'palaces.xun_4.interpretations[寄庚]'}]

## §05 Structure evidence

Spine (37 atoms) — structural E in palaces 1/4/5 and every board-internal relation touching them.

| id | type | value | rule |
|---|---|---|---|
| R001 | gate_palace | 门迫宫 | frozen_tables.gate_palace_rules |
| R004 | gate_palace | 宫生门 | frozen_tables.gate_palace_rules |
| R009 | stem_pair_explicit | 壬丁 | explicit_field_pair |
| R010 | hidden_pair_explicit | 乙加丁 | explicit_marker_atom |
| R015 | stem_pair_explicit | 癸辛 | explicit_field_pair |
| R016 | hidden_pair_explicit | 庚加辛 | explicit_marker_atom |
| R017 | hidden_pair_explicit | 丙加辛 | explicit_marker_atom |
| R018 | hidden_pair_explicit | 庚加庚 | explicit_marker_atom |
| R028 | liu_yi_xing | 癸 | frozen_tables.liu_yi_xing |
| R029 | star_tomb | None | frozen_tables.element_tomb |
| R036 | cross_palace_trace | 乙 | CAP-09 value_trace (field values, never array positions) |
| R037 | cross_palace_trace | 丙 | CAP-09 value_trace (field values, never array positions) |
| R038 | cross_palace_trace | 丁 | CAP-09 value_trace (field values, never array positions) |
| R041 | cross_palace_trace | 庚 | CAP-09 value_trace (field values, never array positions) |
| R042 | cross_palace_trace | 辛 | CAP-09 value_trace (field values, never array positions) |
| R043 | cross_palace_trace | 壬 | CAP-09 value_trace (field values, never array positions) |
| R044 | cross_palace_trace | 癸 | CAP-09 value_trace (field values, never array positions) |
| R045 | opposition | [1, 4] | frozen_tables.opposition_pairs |
| R047 | lodging_edge | 庚 | centre stem re-appears as 寄X in the host palace |

Condition register in scope (the chart's own 判断 lines, kept in their own register):

- `E061` P1 — 天壬 phase=帝旺 branch=子 [verified]
- `E062` P1 — 地丁 phase=绝 branch=子 [verified]
- `E063` P1 — 暗乙 phase=病 branch=子 [verified]
- `E064` P1 — 天盘干:壬加丁『干合蛇刑』
- `E065` P1 — 暗干干:乙加丁『奇仪相佐』
- `E066` P1 — 奇仪相合
- `E067` P1 — 门迫宫
- `E083` P4 — 天癸 phase=养/胎 branch=辰 [verified]
- `E084` P4 — 寄庚 phase=养/长生 branch=辰 [verified]
- `E085` P4 — 地辛 phase=墓/死 branch=辰 [verified]
- `E086` P4 — 暗丙 phase=冠带/临官 branch=辰 [verified]
- `E087` P4 — 天盘干:癸加辛『网盖天牢』
- `E088` P4 — 寄宫干:庚加辛『太白重锋』
- `E089` P4 — 暗干干:丙加辛『日月相会』
- `E090` P4 — 宫生门
- `E091` P4 — 六仪击刑
- `E092` P4 — 星入墓
- `E093` P5 — 暗干干:庚加庚『太白同宫』

Pillar register (reported, never absorbed into the spine count):

- `R030` triad_family P[2] hai_mao_wei
- `R031` triad_family P[3] hai_mao_wei
- `R032` branch_chong P[4] 巳
- `R033` branch_liuhe P[6] 亥
- `R034` triad_family P[6] hai_mao_wei
- `R035` branch_liuhe P[8] 寅

## §06 Palace coverage matrix

| P | total | addressed | corroborated | deferred | excluded | unparseable | anomaly | absent | closes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 21 | 17 | 4 | 0 | 0 | 0 | 0 | 0 | True |
| 2 | 23 | 18 | 5 | 0 | 0 | 0 | 0 | 0 | True |
| 3 | 22 | 18 | 4 | 0 | 0 | 0 | 0 | 0 | True |
| 4 | 31 | 22 | 9 | 0 | 0 | 0 | 0 | 0 | True |
| 5 | 7 | 5 | 2 | 0 | 0 | 0 | 0 | 0 | True |
| 6 | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | True |
| 7 | 19 | 16 | 3 | 0 | 0 | 0 | 0 | 0 | True |
| 8 | 21 | 16 | 5 | 0 | 0 | 0 | 0 | 0 | True |
| 9 | 20 | 16 | 4 | 0 | 0 | 0 | 0 | 0 | True |

Run tally: {'addressed': 125, 'corroborated': 41, 'deferred': 0, 'excluded': 0, 'unparseable': 0, 'anomaly': 0, 'absent': 0}
Reconciliation: {'sum_of_palace_totals': 186, 'shared_relation_memberships': 20, 'sum_minus_shared': 166, 'atom_total': 166, 'balances': True}

Class-level closure (declared absences):
- PAT-29 空亡(void): **ABSENT** (P6) — no void field in source; schema_adapter.void=UNRESOLVED; absence is factual reporting, never support (law 18/27/28)
- PAT-30 驿马(horse): **ABSENT** (P6) — no horse field in source; schema_adapter.horse=UNRESOLVED; day-pillar triad horse is computable in principle but the chart does not seed the class

## §07 Pattern state registry

catalog 32 classes · 65 live instances · 2 declared null classes · SCORE_SOURCE=TIER2_TOOL

| pattern | palace | state | evidence | tier | score | rank |
|---|---|---|---|---|---|---|
| PAT-01 门迫宫 | 1 | LIVE_COMPUTED+LIVE_EXPLICIT | E002,E067 | explicit_chart | 0.65 | 3 |
| PAT-05 奇仪相合 | 1 | LIVE_COMPUTED+LIVE_EXPLICIT | E005,E006,E066 | explicit_chart | 0.55 | 18 |
| PAT-06 干合蛇刑 | 1 | LIVE_EXPLICIT | E064 | explicit_chart | 0.55 | 19 |
| PAT-07 奇仪相佐 | 1 | LIVE_EXPLICIT | E065 | explicit_chart | 0.55 | 20 |
| PAT-13 三奇得使 | 1 | LIVE_COMPUTED | E006 | computed_structure | 0.45 | 33 |
| PAT-14 三奇受制 | 1 | LIVE_COMPUTED | E006 | computed_structure | 0.45 | 37 |
| PAT-27 干相克 | 1 | LIVE_COMPUTED | E005,E006 | computed_structure | 0.3 | 50 |
| PAT-02 宫生门 | 2 | LIVE_COMPUTED+LIVE_EXPLICIT | E009,E073 | explicit_chart | 0.6 | 9 |
| PAT-03 六仪击刑 | 2 | LIVE_COMPUTED+LIVE_EXPLICIT | E012,E074 | explicit_chart | 0.5 | 27 |
| PAT-08 地刑玄武 | 2 | LIVE_EXPLICIT | E071 | explicit_chart | 0.5 | 28 |
| PAT-09 青龙华盖 | 2 | LIVE_EXPLICIT | E072 | explicit_chart | 0.4 | 41 |
| PAT-27 干相克 | 2 | LIVE_COMPUTED | E012,E013 | computed_structure | 0.55 | 23 |
| PAT-31 支合冲刑 | 2 | LIVE_COMPUTED | E011 | computed_structure | 0.5 | 29 |
| PAT-10 火入天罗 | 3 | LIVE_EXPLICIT | E078 | explicit_chart | 0.3 | 48 |
| PAT-11 凶蛇入狱 | 3 | LIVE_EXPLICIT | E079 | explicit_chart | 0.3 | 49 |
| PAT-12 三奇升殿 | 3 | LIVE_EXPLICIT | E080 | explicit_chart | 0.4 | 42 |
| PAT-13 三奇得使 | 3 | LIVE_EXPLICIT | E081 | explicit_chart | 0.4 | 43 |
| PAT-14 三奇受制 | 3 | LIVE_COMPUTED+LIVE_EXPLICIT | E019,E082 | explicit_chart | 0.4 | 44 |
| PAT-31 支合冲刑 | 3 | LIVE_COMPUTED | E018 | computed_structure | 0.5 | 30 |
| PAT-02 宫生门 | 4 | LIVE_COMPUTED+LIVE_EXPLICIT | E023,E090 | explicit_chart | 0.65 | 4 |
| PAT-03 六仪击刑 | 4 | LIVE_COMPUTED+LIVE_EXPLICIT | E026,E091 | explicit_chart | 0.35 | 45 |
| PAT-04 星入墓 | 4 | LIVE_COMPUTED+LIVE_EXPLICIT | E024,E092 | explicit_chart | 0.35 | 46 |
| PAT-13 三奇得使 | 4 | LIVE_COMPUTED | E028 | computed_structure | 0.45 | 34 |
| PAT-14 三奇受制 | 4 | LIVE_COMPUTED | E028 | computed_structure | 0.45 | 38 |
| PAT-15 网盖天牢 | 4 | LIVE_EXPLICIT | E087 | explicit_chart | 0.35 | 47 |
| PAT-16 太白重锋 | 4 | LIVE_EXPLICIT | E088 | explicit_chart | 0.75 | 1 |
| PAT-17 日月相会 | 4 | LIVE_EXPLICIT | E089 | explicit_chart | 0.55 | 21 |
| PAT-31 支合冲刑 | 4 | LIVE_COMPUTED | E025 | computed_structure | 0.65 | 7 |
| PAT-18 太白同宫 | 5 | LIVE_EXPLICIT | E093 | explicit_chart | 0.75 | 2 |
| PAT-02 宫生门 | 6 | LIVE_COMPUTED+LIVE_EXPLICIT | E034,E099 | explicit_chart | 0.65 | 5 |
| PAT-13 三奇得使 | 6 | LIVE_COMPUTED | E037 | computed_structure | 0.45 | 35 |
| PAT-19 日奇入墓 | 6 | LIVE_EXPLICIT | E097 | explicit_chart | 0.25 | 51 |
| PAT-20 火入勾陈 | 6 | LIVE_EXPLICIT | E098 | explicit_chart | 0.15 | 52 |
| PAT-27 干相克 | 6 | LIVE_COMPUTED | E037,E038 | computed_structure | 0.6 | 17 |
| PAT-31 支合冲刑 | 6 | LIVE_COMPUTED | E036 | computed_structure | 0.55 | 26 |
| PAT-12 三奇升殿 | 7 | LIVE_COMPUTED+LIVE_EXPLICIT | E044,E105 | explicit_chart | 0.6 | 10 |
| PAT-21 青龙耀明 | 7 | LIVE_EXPLICIT | E103 | explicit_chart | 0.6 | 13 |
| PAT-22 犬遇青龙 | 7 | LIVE_EXPLICIT | E104 | explicit_chart | 0.6 | 14 |
| PAT-28 干相生 | 7 | LIVE_COMPUTED | E044,E045 | computed_structure | 0.55 | 25 |
| PAT-01 门迫宫 | 8 | LIVE_COMPUTED+LIVE_EXPLICIT | E048,E111 | explicit_chart | 0.6 | 8 |
| PAT-13 三奇得使 | 8 | LIVE_COMPUTED | E052 | computed_structure | 0.6 | 11 |
| PAT-14 三奇受制 | 8 | LIVE_COMPUTED | E052 | computed_structure | 0.6 | 12 |
| PAT-23 白虎猖狂 | 8 | LIVE_EXPLICIT | E109 | explicit_chart | 0.6 | 15 |
| PAT-24 小蛇得势 | 8 | LIVE_EXPLICIT | E110 | explicit_chart | 0.6 | 16 |
| PAT-27 干相克 | 8 | LIVE_COMPUTED | E051,E052 | computed_structure | 0.55 | 24 |
| PAT-31 支合冲刑 | 8 | LIVE_COMPUTED | E050 | computed_structure | 0.5 | 31 |
| PAT-32 值符值使 | 8 | LIVE_COMPUTED | E049 | computed_structure | 0.5 | 32 |
| PAT-02 宫生门 | 9 | LIVE_COMPUTED+LIVE_EXPLICIT | E055,E117 | explicit_chart | 0.65 | 6 |
| PAT-13 三奇得使 | 9 | LIVE_COMPUTED | E059 | computed_structure | 0.45 | 36 |
| PAT-14 三奇受制 | 9 | LIVE_COMPUTED | E059 | computed_structure | 0.45 | 39 |
| PAT-25 青龙转光 | 9 | LIVE_EXPLICIT | E115 | explicit_chart | 0.45 | 40 |
| PAT-26 华盖悖师 | 9 | LIVE_EXPLICIT | E116 | explicit_chart | 0.55 | 22 |

Score formula (tool-owned): `min(ceiling(tier), base + named + coupling + corroboration + relevance - contradiction)`

### explicit vs computed reconciliation (law 26)

| pattern | palace | explicit marker kept | computed rule confirms |
|---|---|---|---|
| PAT-06 干合蛇刑 | 1 | yes (rank 1) | CONFIRMED |
| PAT-07 奇仪相佐 | 1 | yes (rank 1) | CONFIRMED |
| PAT-05 奇仪相合 | 1 | yes (rank 1) | CONFIRMED |
| PAT-01 门迫宫 | 1 | yes (rank 1) | CONFIRMED |
| PAT-08 地刑玄武 | 2 | yes (rank 1) | CONFIRMED |
| PAT-09 青龙华盖 | 2 | yes (rank 1) | CONFIRMED |
| PAT-02 宫生门 | 2 | yes (rank 1) | CONFIRMED |
| PAT-03 六仪击刑 | 2 | yes (rank 1) | CONFIRMED |
| PAT-10 火入天罗 | 3 | yes (rank 1) | CONFIRMED |
| PAT-11 凶蛇入狱 | 3 | yes (rank 1) | CONFIRMED |
| PAT-12 三奇升殿 | 3 | yes (rank 1) | EXPLICIT_UNCONFIRMED |
| PAT-13 三奇得使 | 3 | yes (rank 1) | EXPLICIT_UNCONFIRMED |
| PAT-14 三奇受制 | 3 | yes (rank 1) | CONFIRMED |
| PAT-15 网盖天牢 | 4 | yes (rank 1) | CONFIRMED |
| PAT-16 太白重锋 | 4 | yes (rank 1) | CONFIRMED |
| PAT-17 日月相会 | 4 | yes (rank 1) | CONFIRMED |
| PAT-02 宫生门 | 4 | yes (rank 1) | CONFIRMED |
| PAT-03 六仪击刑 | 4 | yes (rank 1) | CONFIRMED |
| PAT-04 星入墓 | 4 | yes (rank 1) | CONFIRMED |
| PAT-18 太白同宫 | 5 | yes (rank 1) | CONFIRMED |
| PAT-19 日奇入墓 | 6 | yes (rank 1) | CONFIRMED |
| PAT-20 火入勾陈 | 6 | yes (rank 1) | CONFIRMED |
| PAT-02 宫生门 | 6 | yes (rank 1) | CONFIRMED |
| PAT-21 青龙耀明 | 7 | yes (rank 1) | CONFIRMED |
| PAT-22 犬遇青龙 | 7 | yes (rank 1) | CONFIRMED |
| PAT-12 三奇升殿 | 7 | yes (rank 1) | CONFIRMED |
| PAT-23 白虎猖狂 | 8 | yes (rank 1) | CONFIRMED |
| PAT-24 小蛇得势 | 8 | yes (rank 1) | CONFIRMED |
| PAT-01 门迫宫 | 8 | yes (rank 1) | CONFIRMED |
| PAT-25 青龙转光 | 9 | yes (rank 1) | CONFIRMED |
| PAT-26 华盖悖师 | 9 | yes (rank 1) | CONFIRMED |
| PAT-02 宫生门 | 9 | yes (rank 1) | CONFIRMED |

### null register
- PAT-29 空亡: **NULL_CLASS_ABSENT** — void class not in source; ABSENT is factual reporting, not support
- PAT-30 驿马: **NULL_CLASS_ABSENT** — horse class not in source; ABSENT is factual reporting, not support

## §08 Claim lines

```
CLAIM|C001|batch=B5|claims=I001,I003|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C002|batch=B5|claims=I004|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C003|batch=B5|claims=I008|disp=ADDRESSED|certainty=0.55   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C004|batch=B5|claims=I002,I004|disp=ADDRESSED|certainty=0.65   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C005|batch=B5|claims=I002|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C006|batch=B5|claims=I003|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C007|batch=B5|claims=I001,I003,I004|disp=ADDRESSED|certainty=0.65   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C008|batch=B5|claims=I002|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C009|batch=B5|claims=I002,I004|disp=ADDRESSED|certainty=0.65   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C010|batch=B5|claims=I003|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C011|batch=B5|claims=I005|disp=ADDRESSED|certainty=0.65   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C012|batch=B5|claims=I006,I007|disp=ADDRESSED|certainty=0.60   | rank=bounded | tier=explicit_chart | ceiling=0.9
CLAIM|C013|batch=B5|claims=I001|disp=EXCLUDED|certainty=NA   | rank=rejected | tier=no_chart_support | ceiling=0.75
```

| claim | archetype | label | certainty | addends | rank |
|---|---|---|---|---|---|
| C001 | ARC-01 | guarded_alliance | 0.6 | 0.45 + 0.20 + 0.10 - 0.15 | bounded |
| C002 | ARC-02 | precise_watchful | 0.6 | 0.45 + 0.20 + 0.05 - 0.10 | bounded |
| C003 | ARC-03 | ritual_mark | 0.55 | 0.45 + 0.20 + 0.05 - 0.15 | bounded |
| C004 | ARC-04 | sustained_care | 0.65 | 0.45 + 0.20 + 0.10 - 0.10 | bounded |
| C005 | ARC-05 | layered_reveal | 0.6 | 0.45 + 0.20 + 0.05 - 0.10 | bounded |
| C006 | ARC-06 | opposition_led | 0.6 | 0.45 + 0.20 + 0.05 - 0.10 | bounded |
| C007 | ARC-07 | pressure_into_poise | 0.65 | 0.45 + 0.20 + 0.15 - 0.15 | bounded |
| C008 | ARC-08 | single_subject_soft_light | 0.6 | 0.45 + 0.20 + 0.05 - 0.10 | bounded |
| C009 | ARC-09 | enclosed_studio | 0.65 | 0.45 + 0.20 + 0.10 - 0.10 | bounded |
| C010 | ARC-10 | hands_only | 0.6 | 0.45 + 0.20 + 0.05 - 0.10 | bounded |
| C011 | ARC-11 | core_first_then_context | 0.65 | 0.45 + 0.20 + 0.05 - 0.05 | bounded |
| C012 | ARC-12 | hybrid_staged | 0.6 | 0.45 + 0.20 + 0.10 - 0.15 | bounded |
| C013 | ARC-03 | chart_selected_name | None | NA | rejected |

## §09 Case alignment

```
CMAP|C001|Q03|DIRECT|E064,E065,E066,R009
CMAP|C001|Q02|INDIRECT|E064,E065,E066,R009
CMAP|C002|Q03|DIRECT|E001,E002,E003,R001
CMAP|C003|Q03|DIRECT|E023,E022,R009,E066
CMAP|C003|Q06|INDIRECT|E023,E022,R009,E066
CMAP|C004|Q04|DIRECT|E002,E022,E024,R029
CMAP|C004|Q04|NO_CHART_SUPPORT|NONE
CMAP|C004|Q04|NO_CHART_SUPPORT|NONE
CMAP|C005|Q04|DIRECT|E022,E023,R004,E090
CMAP|C006|Q04|DIRECT|R045,R001,E067,R004
CMAP|C006|Q03|INDIRECT|R045,R001,E067,R004
CMAP|C007|Q05|DIRECT|R001,E067,R004,E090
CMAP|C007|Q06|INDIRECT|R001,E067,R004,E090
CMAP|C007|Q08|INDIRECT|R001,E067,R004,E090
CMAP|C008|Q05|DIRECT|E023,E022,E024,R029
CMAP|C009|Q05|DIRECT|E022,E023,R004,E025
CMAP|C010|Q05|DIRECT|E022,E092,E023,E001
CMAP|C010|Q08|INDIRECT|E022,E092,E023,E001
CMAP|C011|Q05|DIRECT|E083,E084,E086,E061
CMAP|C011|Q07|INDIRECT|E083,E084,E086,E061
CMAP|C012|Q05|DIRECT|R028,E091,R029,E092
CMAP|C012|Q08|INDIRECT|R028,E091,R029,E092
CMAP|C013|Q03|CONTRADICTS_KNOWN|NONE
CMAP|C013|Q06|CONTRADICTS_KNOWN|NONE
```

| facet | claims | DIRECT | INDIRECT | NO_CHART_SUPPORT | CONTRADICTS_KNOWN |
|---|---|---|---|---|---|
| Q01 (deferred) | — | 0 | 0 | 0 | 0 |
| Q02 | C001 | 0 | 1 | 0 | 0 |
| Q03 | C001,C002,C003,C006,C013 | 3 | 1 | 0 | 1 |
| Q04 | C004,C005,C006 | 3 | 0 | 2 | 0 |
| Q05 | C007,C008,C009,C010,C011,C012 | 6 | 0 | 0 | 0 |
| Q06 | C003,C007,C013 | 0 | 2 | 0 | 1 |
| Q07 | C011 | 0 | 1 | 0 | 0 |
| Q08 | C007,C010,C012 | 0 | 3 | 0 | 0 |

Tag tally (all four present, including zeros): {'DIRECT': 12, 'INDIRECT': 8, 'NO_CHART_SUPPORT': 2, 'CONTRADICTS_KNOWN': 2}

## §10 Solution hypotheses (controlled candidates)

### C001 · ARC-01 · guarded_alliance

- **basis**: The source pole forms a he-combination under a coiled-spirit marker while the life-gate presses against its own palace; the display pole is fed by its environment but keeps its nourishing star in tomb. Read together: the brand's core idea is a deliberate pact that stays guarded about its generosity.
- **chart support**: E064, E065, E066, R009, R001, E067, E002, E001, E022, R029, E092, R045
- **case alignment**: Q03:DIRECT, Q02:INDIRECT
- **limiting**: interpretation is structural; no factual prediction is made; the he-combination's traditional gloss is register-level, not outcome-level
- **counterevidence**: E093, R028, E090
- **guard**: State as tradition-conditional direction only. Do not phrase as a promise about market response (law 22).
- **scope**: primary axis {1,4} plus centre 5 lodging edge · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the brand's public voice remains narrower than its internal generosity
- **validation path**: re-check against the Assignment-1 insight list: if a researched insight already claims 'generous' positioning, this claim is CONTRADICTS_KNOWN and must be reworked
- **competing candidates**: quiet_craft_discipline [not_rejected]; corrective_awakening [rejected]

### C002 · ARC-02 · precise_watchful

- **basis**: Coiled spirit and life-gate sit under gate pressure at the source pole; depth and display sit together at the display pole with the centre's stem lodged into it. The voice register is exact and observant, warm only where the structure allows it.
- **chart support**: E001, E002, E003, R001, E022, E023, R047, E032, E029
- **case alignment**: Q03:DIRECT
- **limiting**: tone register is the least fact-bound layer of the board; treat as creative direction
- **counterevidence**: R004, R018
- **guard**: Voice adjectives must trace to a deity/gate/star atom in the shipped package, never to mood (no free invention).
- **scope**: primary axis {1,4} · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds where the brand speaks about its process rather than its effect
- **validation path**: one line of voice copy drafted against C002; if the line promises an outcome, the line fails the guard, not the claim
- **competing candidates**: warm_directive [not_rejected]; cool_withholding [not_rejected]

### C003 · ARC-03 · ritual_mark

- **basis**: Display gate with a deep-earth deity, a union combination, and a stored core: the name and mark should behave like a made object used in a repeated act, not like an announcement of authority.
- **chart support**: E023, E022, R009, E066, R017, E089, R004
- **case alignment**: Q03:DIRECT, Q06:INDIRECT
- **limiting**: no literal object, place, or figure may be read off the chart (laws 23-24)
- **counterevidence**: E105, E080, R028
- **guard**: A name or mark must never be 'selected by the chart'. The chart supplies register and constraint only; the choice traces to Assignment-1 (see C013, rejected).
- **scope**: primary axis {1,4} with contrast from {3,7} · **confidence**: 0.55 · **rank**: bounded · **uncertainty**: medium-high
- **scenario condition**: holds while the mark is used in a repeated act rather than as a burst of signalling
- **validation path**: logo direction must name 2-3 mood-board styles and one explicit avoid-line (brief requirement), each traced to Assignment 1
- **competing candidates**: visible_authority [not_rejected]; engineered_softness [rejected]

### C004 · ARC-04 · sustained_care

- **basis**: The life-gate stands at the source pole, the display pole carries the slow-earth star and keeps it in tomb, and the centre's stem is lodged into that same display palace. Structurally the product behaves as something kept and applied over time.
- **chart support**: E002, E022, E024, R029, E092, R041, R047, E023, R004
- **case alignment**: Q04:DIRECT, Q04:NO_CHART_SUPPORT(format), Q04:NO_CHART_SUPPORT(price)
- **limiting**: product category is supplied by the case as scope only; the chart never names a product
- **counterevidence**: E028, R037
- **guard**: No medical, therapeutic or bodily claim may be derived (law 23). The star is used strictly as a registry term for a slow earth process.
- **scope**: primary axis {1,4} plus centre lodging · **confidence**: 0.65 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the product's value is expressed in repeated use rather than in a single effect
- **validation path**: product definition (format, variants, size, price) is NOT chart-derivable: those rows carry NO_CHART_SUPPORT and must come from Assignment 1
- **competing candidates**: contained_remedy [not_rejected]; restorative_rebuild [rejected]

### C005 · ARC-05 · layered_reveal

- **basis**: A concealing earth deity holds a display gate; the environment feeds that gate; the nourishing core is stored; the hidden brightness sits inside the same palace. The package should be composed in two states — a muted closed state and a warmer opened state.
- **chart support**: E022, E023, R004, E090, R029, R017, E089, E028, E026
- **case alignment**: Q04:DIRECT
- **limiting**: the chart cannot specify colour; colour must come from the mood board and Assignment-1 insight
- **counterevidence**: R028, E087
- **guard**: Material statements are creative direction only. No physical fact (substrate, finish, mechanism) may be asserted from the chart (laws 23-24).
- **scope**: primary axis {1,4} · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the first read is quiet and the second read rewards attention
- **validation path**: shelf-standout element must be describable in one sentence from three feet away (brief requirement); tie it to one mood-board pin
- **competing candidates**: muted_shell_over_active_core [not_rejected]; overt_signal_low_noise [rejected]

### C006 · ARC-06 · opposition_led

- **basis**: The two poles are a generative pair (water feeds wood) but their local conditions invert: agency presses on the environment at the source pole while the environment feeds agency at the display pole. The difference to lead with is that inversion, not a feature list.
- **chart support**: R045, R001, E067, R004, E090, E004, E025, R032
- **case alignment**: Q04:DIRECT, Q03:INDIRECT
- **limiting**: pillar-register relations are tallied separately and never absorbed into the spine count
- **counterevidence**: E022, R029
- **guard**: The difference must be stated as a describable direction, never as 'better' (brief requirement).
- **scope**: primary axis {1,4} with the day-branch chong noted from the pillar register · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the category leads with performance claims that push against the environment
- **validation path**: place the package beside the 3-5 researched competitors and state the inversion in one sentence
- **competing candidates**: layer_led [not_rejected]; sequence_led [rejected]

### C007 · ARC-07 · pressure_into_poise

- **basis**: A pressed gate at the source pole, a fed gate at the display pole, a generative opposition between them, and a stored core in the display palace: the campaign idea is pressure resolved into composure.
- **chart support**: R001, E067, R004, E090, R045, E064, E065, R029, R047, R017
- **case alignment**: Q05:DIRECT, Q06:INDIRECT, Q08:INDIRECT(internal_consistency)
- **limiting**: no calendar or venue claim is made anywhere in this campaign direction
- **counterevidence**: R028, R018, E111
- **guard**: The big idea must not promise an outcome or a result (law 22).
- **scope**: primary axis {1,4} plus centre lodging and the visible command-axis contrast · **confidence**: 0.65 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the campaign shows the act rather than the result
- **validation path**: hero image briefed from C008 and stage from C009 must both be derivable from this idea without a fourth, unrelated claim
- **competing candidates**: return_to_the_source [not_rejected]; the_quiet_instrument [not_rejected]

### C008 · ARC-08 · single_subject_soft_light

- **basis**: A display gate under a concealing earth deity, with the slow-earth star in tomb: one subject, low and even light, focal weight on what is withheld rather than on what is displayed.
- **chart support**: E023, E022, E024, R029, E092, R004, R017, E089
- **case alignment**: Q05:DIRECT
- **limiting**: no claims about the photographed person, body, or condition (law 23)
- **counterevidence**: E003, R001
- **guard**: Composition language is creative direction. Nothing in this claim describes the world.
- **scope**: primary axis {1,4} · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium-high
- **scenario condition**: holds while the hero image is readable at thumbnail scale without any text
- **validation path**: generate or shoot two frames (single subject; object-only) and test which one survives the 'no text' rule
- **competing candidates**: object_only_ritual_frame [not_rejected]; figure_in_pressure [not_rejected]

### C009 · ARC-09 · enclosed_studio

- **basis**: Depth deity, display gate fed by its palace, slow-earth star stored: an enclosed, low-ceilinged stage with a directional light source, rather than an open location.
- **chart support**: E022, E023, R004, E025, E024, R029, R047
- **case alignment**: Q05:DIRECT
- **limiting**: the chart supplies register, not architecture
- **counterevidence**: E003, E067
- **guard**: Palace direction is contextual only; never state a real location (law 5).
- **scope**: primary axis {1,4} · **confidence**: 0.65 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the set can be built in one controlled space with one motivated light
- **validation path**: location scouting brief or AI prompt must contain: enclosure, single motivated light, one reserved negative space
- **competing candidates**: threshold_interior [not_rejected]; open_field [rejected]

### C010 · ARC-10 · hands_only

- **basis**: The concealing deity and stored star put the human register behind the object register; the impulse star keeps movement in frame. Hands and gesture carry the act without a face.
- **chart support**: E022, E092, E023, E001, E003, R045
- **case alignment**: Q05:DIRECT, Q08:INDIRECT(specificity)
- **limiting**: audience fit is a case-side judgement; the chart cannot confirm it
- **counterevidence**: E003, E002
- **guard**: No inference about any person, body, or condition is permitted; casting here is a stated creative choice (law 23).
- **scope**: primary axis {1,4} · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while the campaign can be cast from hands and gesture alone
- **validation path**: state the choice explicitly in the brief as a deliberate avoidance of faces, and give the reason
- **competing candidates**: product_only [not_rejected]; one_calm_figure [not_rejected]

### C011 · ARC-11 · core_first_then_context

- **basis**: The display pole holds the gestating and growing phases while the source pole holds peak-then-cut phases. Build the supported, growing assets first; add the pressed life-register assets afterwards as the closing beat.
- **chart support**: E083, E084, E086, E061, E062, E063, R004, R001
- **case alignment**: Q05:DIRECT, Q07:INDIRECT
- **limiting**: the chart's own time units are not a delivery schedule
- **counterevidence**: E061
- **guard**: Sequence claims cite phase atoms, not preference.
- **scope**: primary axis {1,4} · **confidence**: 0.65 · **rank**: bounded · **uncertainty**: medium-high
- **scenario condition**: holds while the production run can hold the pressed-register assets to the end
- **validation path**: asset list ordered: hero, then 2-3 supporting, then detail, then any motion — with the phase citation beside each block
- **competing candidates**: context_first_then_core [not_rejected]; parallel_build [rejected]

### C012 · ARC-12 · hybrid_staged

- **basis**: The defect points sit on the concealed/instrument layer; the command axis is off the spine and pressed; the display pole is the supported one. Proposal: stage the work in passes with a human gate at the instrument/punishment point, rather than committing a single automated chain.
- **chart support**: R028, E091, R029, E092, R001, R004, R047
- **case alignment**: Q05:DIRECT, Q08:INDIRECT(production_realism)
- **limiting**: the chart cannot select tools or vendors
- **counterevidence**: E049, E109, E111
- **guard**: No budget, vendor, or schedule claim is made; the case states none and none may be inferred.
- **scope**: primary axis {1,4} with the visible command-axis contrast from {8} · **confidence**: 0.6 · **rank**: bounded · **uncertainty**: medium
- **scenario condition**: holds while each pass has one named human approval point and a rollback
- **validation path**: write the pass list with the approval gate marked at the pass that touches the concealed/instrument layer
- **competing candidates**: ai_led_human_gated [not_rejected]; human_led_ai_assisted [not_rejected]

### C013 · ARC-03 · chart_selected_name

- **basis**: Draft claim (retained for the record): the chart's union marker and rise-to-throne markers 'select' a brand name.
- **chart support**: (none — rejected before support was admissible)
- **case alignment**: Q03:CONTRADICTS_KNOWN, Q06:CONTRADICTS_KNOWN
- **limiting**: kept in the package deliberately: a rejection that is visible is stronger than a rejection that is silent
- **counterevidence**: CONK004
- **guard**: Rejected. The chart supplies register and constraint; selection belongs to Assignment-1 evidence.
- **scope**: name selection · **confidence**: None · **rank**: rejected · **uncertainty**: NA
- **scenario condition**: n/a
- **validation path**: if a name candidate appears, it must be traced to a named insight or pin, then checked against C003's register, never the reverse
- **conflict**: {'against': 'CONK004', 'type': 'CONFLICT_WITH_KNOWN', 'action': 'downgraded to rejected; the verdict was not rewritten to fit (law 52/cc3)', 'resolver': 'C003 (direction only)', 'note': 'CONK004 = document.metadata.traceability_requirement (verbatim)'}

Blocked class: ARC-13 — requires timeframe_of_interest; the case context declares no window and none may be inferred (law 40, cc5)

## §11 Dependency assumptions

Implications (I-atoms):
- **I001** (backward, named-pattern composition (PAT-06 + PAT-05 + PAT-01 in one palace); premises E064, E066, R009, R001, E067, E001, E002) — At the source pole an alliance is formed and immediately taxed: the he-combination is entangled by the coiled spirit, and the life-gate presses on its own environment.
- **I002** (forward, PAT-02 + PAT-04 in one palace with a concealing deity; premises E090, R004, E092, R029, E022, E023) — At the display pole the surface is fed by its environment while the nourishing core is stored: support arrives, but not from the visible layer.
- **I003** (backward, frozen_tables.element_cycle.generates + law 10 opposition geometry; premises R045, E004, E025) — The opposition pair 1-4 is generational, not antagonistic: the palace elements are water and wood, and water generates wood, so the two poles stand in a parent-child relation.
- **I004** (forward, lodging graph (centre builds a lodging GRAPH; law 10); premises E032, E029, R047, R041) — The centre's only stem is deposited into the display palace as a lodged stem, so the unexpressed core lands in the work that is shown rather than in the work that is argued.
- **I005** (forward, frozen_tables.twelve_phases, verified against palace branches; premises E061, E062, E063, E083, E084, E086, E090, R001) — The phase register is split by pole: the source pole holds peak-then-cut phases, the display pole holds gestating and growing phases.
- **I006** (backward, PAT-03 + PAT-04 + PAT-01 convergence (three independent computations); premises R028, R029, R001, E091, E092, E067) — Defect points concentrate on the hidden/instrument register: punishment marker, star tomb and gate pressure all sit on the concealed or stored layer.
- **I007** (backward, PAT-32 (值符/值使 anchor) + PAT-01 + PAT-23 as visible contrast (law 28); premises E047, E049, E048, E111, E109, E050) — The command axis of the board sits off the primary axis and is itself pressed: the leading star is the tool/learning star, and its palace carries both gate pressure and a metal-on-wood breakage marker.
- **I008** (forward, CAP-09 stem value traces across palaces; premises R037, R038, R043, R042, R036, E028, E007) — The three wonders circulate off-axis through the board's stem traces while the axis itself holds the receiving end, so the axis reads as a place where value arrives rather than originates.

Assumptions (A-atoms, ranked):
- **A001** idx=1 (jurisdiction) — The slow-earth star is used strictly as a registry term for a slow earth process; no health, medical or bodily reading is derived from it. *(activates when: any claim that names a symptom, condition or treatment invalidates the reading and must be reworked)*
- **A002** idx=2 (scope) — The three briefs are executed for a brand whose category can carry a restraint-led register. *(activates when: if Assignment-1 research shows the category is saturated with restraint, this assumption fails and the register must be re-argued)*
- **A003** idx=2 (boundary) — The palace 3 rise-to-throne / service / restraint markers are treated as visible contrast only, never as ranked support. *(activates when: if the operator re-earmarks the eligibility scope, those markers must be re-run through CAP-14 before any ranking)*
- **A004** idx=1 (boundary) — Pillar-register relations (day-branch chong / liuhe / triad) are reported and cited but never absorbed into the 37-atom spine tally. *(activates when: if a claim's support would depend only on pillar-register atoms, the claim is NO_CHART_SUPPORT for the spine and must be downgraded)*
- **A005** idx=1 (production) — The production path is a creative-direction proposal, not a vendor, budget or schedule decision. *(activates when: any cost, timeline or tool-selection statement requires a case-side input that does not exist in this run)*

## §12 Uncertainty & limits

- assumption indices in use: [1, 2]
- invalid chains: 1 — the window chain is blocked rather than resolved (INVALID_INTO_UNKNOWN)
- deferred topics: campaign window (ARC-13), case facet Q01
- blocked classes: Tier2 QT for ARC-13 (required field absent)
- conflict register: [{'claim_id': 'C013', 'against': 'CONK004', 'type': 'CONFLICT_WITH_KNOWN', 'action': 'verdict downgraded to rejected', 'why': "the case's traceability requirement: every major decision must trace to a specific Assignment-1 research finding, insight, or mood-board pin — a chart-selected name can never do that"}]
- null classes:
  - PAT-29 空亡: NULL_CLASS_ABSENT
  - PAT-30 驿马: NULL_CLASS_ABSENT

## §13 Decision support

**Bounded recommendation** — Build the three briefs on one shared register: a displayed surface that is supported, over a stored core that is withheld; pressure belongs in the frame, not in the promise.

*Guard*: All directives are tradition-conditional creative direction. Nothing here selects a name, a price, a material, a vendor or a window.

### Directive sheets

| id | brief | section | directive | strength | chart basis | guard | trace slot |
|---|---|---|---|---|---|---|---|
| D001 | Brand Idea & Philosophy | Core Idea | Write the core idea as a pact with a withheld interior: what the brand commits to, and what it deliberately keeps back. | bounded | C001 | no outcome promise | Assignment-1 research finding (category gap) |
| D002 | Brand Idea & Philosophy | Philosophy / POV | Anchor the POV in the inversion on the axis: the category presses against its environment; this brand lets its environment feed the display. | bounded | C006, R001, R004 | state as direction, never as superiority | Assignment-1 insight (category behaviour) |
| D003 | Brand Idea & Philosophy | Positioning Statement | Audience and differentiator must be pulled from Assignment 1. The chart supplies only the register of the 'because' clause: supported display over pressed agency. | conditional | C006 | audience is never chart-derived | Assignment-1 audience research + insight |
| D004 | Brand Idea & Philosophy | Personality & Tone | 3-5 adjectives from the voice claim: exact, observant, unhurried, self-possessed, warm only where supported. | bounded | C002 | each adjective maps to a cited atom | mood-board pin (tone) |
| D005 | Brand Idea & Philosophy | Name Rationale | Name choice is not chart-derived (C013 is rejected). Argue it from Assignment-1 evidence, then check it against the register in C003. | conditional | C003 | no chart-selected name | Assignment-1 insight + pin |
| D006 | Brand Idea & Philosophy | Logo Direction | Brief a mark that behaves as a made object used in a repeated act; reference 2-3 mood-board styles and one explicit avoid-line. | bounded | C003, E023, E022 | no literal object or figure from the chart | 2-3 mood-board pins + 1 avoid reference |
| D007 | Product & Packaging | Product Definition | Define format, variants, size and price from Assignment 1. The chart's contribution is the use-register only: value expressed over repeated use. | conditional | C004 | NO_CHART_SUPPORT rows must be filled from Assignment-1 research | Assignment-1 competitor scan (size/price band) |
| D008 | Product & Packaging | Packaging Direction | Design a two-state package: a muted closed read, a warmer opened read, with the focal weight on the stored element. | bounded | C005, E022, E092, R017 | no material or colour asserted from the chart | mood-board pins (surface / colour) |
| D009 | Product & Packaging | Shelf Standout | The standout element is the reserved negative space that makes the second read discoverable at three feet. | bounded | C005, C006, R045 | one sentence, describable at shelf distance | Assignment-1 insight (category shelf/feed sameness) |
| D010 | Product & Packaging | Functional-to-Emotional Bridge | Connect one functional choice to the withheld-interior philosophy: the choice that slows the first read is the same choice that pays on the second. | bounded | C001, C005 | no efficacy claim | Assignment-1 insight |
| D011 | Ad / Campaign | Big Idea | Show pressure resolving into composure. Show the act, not the result. | bounded | C007 | no outcome promise (law 22) | Assignment-1 insight (audience tension) |
| D012 | Ad / Campaign | Hero Shot | One subject, low even light, focal weight on the withheld element; the frame must read without text. | bounded | C008 | no claim about any person | mood-board pin (light / framing) |
| D013 | Ad / Campaign | Stage / Environment | Enclosed stage, one motivated light, one reserved negative space. Not an open field. | bounded | C009 | register only; no real location named | mood-board pin (set / texture) |
| D014 | Ad / Campaign | Models / Casting | Cast hands and gesture; state explicitly that faces are avoided and why. | bounded | C010 | casting is a creative choice, never an inference about people | Assignment-1 audience research |
| D015 | Ad / Campaign | Plan of Action | Order: hero (display pole, growing phases) -> 2-3 supporting -> detail -> motion; pressed-register assets close the set. | bounded | C011 | each block carries its phase citation; this is a preference, not a finding | mood-board pins per asset |
| D016 | Ad / Campaign | Production Requirements | Propose a staged hybrid path: passes with one named human approval gate at the concealed/instrument layer. | bounded | C012, I006 | no budget, vendor or schedule claim | course workflow (standardized image/video path) |
| D017 | Ad / Campaign | Window (blocked) | Do not state a campaign window. ARC-13 is BLOCKED: the case declares no window and none may be inferred. | blocked | GAP-003 | silence is the correct output here | operator-supplied window if one exists |

### Coherence check (the assignment's one-line answers)

- **Brand Idea & Philosophy** — The core idea (D001/D002) traces to the axis inversion C006 plus the guarded-alliance claim C001; the research finding it must cite is the category gap identified in Assignment 1.
  - chart basis: C001, C006 · trace slot: Assignment-1 research finding (category gap) + insight list
- **Product & Packaging** — The two-state package (D008/D009) traces to the stored-core structure C005 with the caveat that all product facts (D007) are NO_CHART_SUPPORT and come from Assignment 1.
  - chart basis: C004, C005 · trace slot: Assignment-1 competitor scan + mood-board pins (surface/colour)
- **Ad / Campaign** — The campaign (D011-D016) traces to the pressure-into-poise claim C007 with hero, stage, casting and sequence each carrying its own chart citation and guard.
  - chart basis: C007, C008, C009, C010, C011, C012 · trace slot: Assignment-1 insight (audience tension) + pins per asset

## §14 Gap report

| id | path | why unaddressed | owner phase | resolution |
|---|---|---|---|---|
| GAP-001 | PAT-29 空亡 (void) | the source declares no void field; the class cannot be computed from this adapter | P6 | declared null class; ABSENT, not a defect (law 27) |
| GAP-002 | PAT-30 驿马 (horse) | the source declares no horse marker; the day-pillar triad horse is computable in principle but the chart does not seed the class | P6 | declared null class; ABSENT |
| GAP-003 | ARC-13 campaign window | case context declares no timeframe_of_interest, and none may be inferred (law 40/cc5) | Tier2 step 1 | class BLOCKED; directive D017 tells the writer to leave the window blank |
| GAP-004 | explicit marker 三奇升殿 at palace 3 | the chart's own definition places 丙 at palace 9; palace 3 carries 丙 with 壬, so the computed rule does not confirm the printed marker | P6 reconciliation | marker retained at authority rank 1 and tagged EXPLICIT_UNCONFIRMED; it is outside the ranked spine so it cannot move a claim |
| GAP-005 | case_context shape | the case ships as a document, not the flat case_context schema | CAP-17 | CONTEXT_MAPPED_DOCUMENT_SHAPE; derived rows tagged DECOMPOSED; CONK rows are verbatim strings only |
| GAP-006 | domain | the case states no domain and it may not be inferred | CAP-17 | domain=other with source NOT_STATED |
| GAP-007 | board arrangement re-derivation | the run reads the printed board; it does not re-derive the hourly rotation from the hour pillar | Tier-0 (out of contract) | declared verification gap, not an assertion of error; every downstream claim inherits it |
| GAP-008 | product facts (format, variants, size, price) | not chart-derivable at all | CAP-18 | NO_CHART_SUPPORT rows on Q04; Assignment-1 evidence is the only admissible source |
| GAP-009 | case facet Q01 (Before You Start) | the case decomposes into 8 facets, over the threshold of 7, so CAP-17 step 4 requires a deferral | CAP-17 | deferred by declared facet_handling; its binding content is enforced as CONK004 in every claim's validation_path |
| GAP-010 | palace 3 explicit markers (升殿/得使) | two of the 32 explicit markers are not confirmed by their computed rules | P6 reconciliation | kept visible in the explicit-vs-computed table; no claim depends on them |

## §15 Tool event log

- CAP calls: 15 (toolchain) + 5 (render gate) + 7 (render) = 27 of 60
- SCORE_SOURCE stamps: TIER2_TOOL (no EMULATED products in this run)
- anomalies: 0; conditions: 1
- render gate: PASS — 121 checks
- tool registry declared vs used:
  - `compute_evidence_registry` (Tier-0) → CAP-11 (tools/tier0.py:atomize/evidence_registry)
  - `build_board_digest` (Tier-0) → CAP-12 (tools/render_package.py:build_digests)
  - `expand_claim_lines` (Tier-0) → CAP-13/CAP-15 (tools/validate_package.py)
  - `compute_path_rank` (Tier-0) → CAP-15 (tools/tier0.py:score_card)
  - `validate_coverage` (Tier-0) → CAP-14 (tools/tier0.py:batch_and_ledger)
  - `luoshu_cycle_mapper` (Tier-2) → CAP-08 (tools/tier0.py:palace_identity)
  - `ganzhi_to_luoshu_mapper` (Tier-2) → CAP-05/CAP-09 (tools/tier0.py:pillars_and_composites, value traces)
  - `five_state_classifier` (Tier-2) → CAP-10 (tools/tier0.py:patterns, element relations)
  - `archetype_compressor` (Tier-2) → not used — no candidate compression was needed (compression_log empty)
  - `pattern_coverage_detector` (Tier-2) → CAP-10 + P6 (tools/tier0.py:patterns, score_card)

## §16 Provenance appendix

- raw→normalized: trim + absence-code separation; raw retained
- absence codes: {'chart_void': 'ABSENT', 'chart_horse': 'ABSENT', 'chart_board_array': 'ABSENT', 'case_timeframe': 'NULL', 'case_domain': 'ABSENT', 'case_unknowns': 'FALSE (empty list is a stated emptiness, not an absent key)'}
- id derivation: path-derived fallback + fixed-width numeric suffix (examples {'E001': 'E.1.deity', 'R001': 'R.gate_palace.E002'})
- reissue log: {'reissue_log': []}
- compression log: {'compression_log': []}
- source fingerprints: chart `20dc73a91a46c4dca78cca6fc9bc7520b91c7b16d9edb18fb93f76d1e8360a15` · case `5f641d01f096e6a1de5b2654da30bc6048085999214ce203fcb93388bae39cc0`

### reproduce

```
python3 tools/tier0.py --chart ../../../../QMDJ/GEN_AI/project_3.json --case raw/case_context.case.yaml --config config --raw raw --work work
python3 tools/validate_package.py
python3 tools/render_package.py
```

## Appendix A — pattern for reuse

- 1 ANCHOR — ingest once, fingerprint, and write a board card that every later phase reads instead of the source.
- 2 REGISTRY — atomise the source into typed atoms with fixed-width ids, and keep registers separate (structural / condition / relation / pillar).
- 3 COVER — run the full coverage protocol, tally every atom exactly once, and reconcile at run level, not only per container.
- 4 RECONCILE — let explicit markers and computed rules meet in a table; neither overwrites the other, and unconfirmed markers stay visible.
- 5 GATE — compute every score and every claim line in a validator, never in prose; the gate must be able to fail.
- 6 SEAL — hash the shipped artifacts with the source fingerprints so a reviewer can re-run and compare.
- 7 REPORT THE GAPS — a gap report ships even on a clean run: null classes, blocked classes, deferred facets and verification gaps are output, not omissions.
