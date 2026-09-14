---
id: path-rank
type: ranking
palace_ids: [2, 6, 8, 9]
phase: SOLUTION_ENGINE
batch: S2
sources: ["raw/state/solver_resolutions.json"]
status: live
---

# Path-Rank

Full candidate rankings with published margins. Mirrors `OPERATOR/PATH_RANK.md`.

## Scoring function

```
final_score     = 0.35·tier + 0.25·support + 0.20·(1−contra)
                + 0.10·consistency + 0.10·requirement_fit

requirement_fit = 0.40·requirement_coverage
                + 0.40·hard_constraint_compliance
                + 0.20·audience_and_tone_fit
```

Hard-constraint elimination runs **before** scoring. Eliminated candidates carry no score.

## SR-BEST-01 — governing strategy

| Rank | Candidate | Score | rfit | Outcome |
|---|---|---|---|---|
| 1 | `BEST-LIFE-DOOR-NE-P8-WITH-LIUHE` | **0.8200** | 1.00 | **SELECTED** |
| 2 | `BEST-OPEN-DOOR-NW-P6-WITH-DING` | 0.7170 | 0.77 | Retained — key creative standard |
| 3 | `BEST-JING-DOOR-S-P9` | 0.5670 | — | Not selected |
| — | `BEST-RIDE-THE-HORSE-AT-P2` | eliminated | — | R05, pre-scoring |
| — | `BEST-PUSH-THE-SHOWPIECE-AT-P9` | eliminated | — | R05 + R01, pre-scoring |

**Margin 0.1030.** Comfortably resolved.

## SR-ANSWERS-01

| Rank | Candidate | Score | rfit | Outcome |
|---|---|---|---|---|
| 1 | `ANS-DUTY-PALACE-9-VOID-SHOWPIECE` | **0.9500** | 0.90 | **SELECTED** |
| 2 | `ANS-ACTOR-DISPLACED-TO-CENTRE` | 0.8815 | 0.84 | Ships live — different question |
| 3 | `ANS-ACTOR-AT-PALACE-1` | 0.2602 | 0.84 | Rejected — consistency FAIL, 4 contradictions |

**Margin 0.0685.** Ranks 1 and 2 are not in competition.

## SR-HIDDEN-01

| Rank | Candidate | Score | Ships |
|---|---|---|---|
| 1 | `HID-VOID-SHOWPIECE-UNDER-PUNISHMENT` | **0.9600** | Yes |
| 2 | `HID-ACTORS-ONLY-SEAT-IS-A-DEATH-DOOR` | 0.9228 | Yes |
| 3 | `HID-WHOLE-BOARD-STASIS` | 0.8515 | Yes |
| 4 | `HID-CRAFT-ROUTE-SEDUCTION` | 0.6803 | Yes |
| 5 | `HID-LATE-VISIBLE-CONNECTOR` | 0.6490 | Yes |
| 6 | (sixth candidate) | 0.1902 | No — below threshold |

## Tie status

**No ties in this run.** All three resolutions returned RESOLVED with margins above threshold. No `STILL_TIED` split candidates were required, and no silent tie-breaking occurred.

## Elimination integrity

A hard-constraint violation disqualifies regardless of how well a candidate would otherwise have scored. Both eliminations happened before scoring; neither candidate has a score recorded anywhere in this run.

## Linked

[[Solution-Architecture]] · [[Recommended-Answers]] · [[Hidden-Problems]] · [[Red-Team]]
