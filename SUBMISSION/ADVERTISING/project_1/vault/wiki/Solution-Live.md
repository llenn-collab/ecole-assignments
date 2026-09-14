---
id: solution-live
type: live
palace_ids: [2, 6, 8, 9]
phase: SOLUTION_ENGINE
batch: S2
sources: ["raw/state/solution_live.json"]
status: live
---

# Solution-Live

The live claim set, revision 1. **8 live claims, 8 citing a resolution, 0 uncited, 0 split, 0 vetoed.**

## Claim register

| Claim | Slot | Text (abbreviated) | Conf | Resolution | Requirements |
|---|---|---|---|---|---|
| ANS-01 | my_answers | One idea must survive six media | HIGH | SR-ANSWERS-01 | R06, R01, R12 |
| ANS-02 | my_answers | The traveller who doesn't recognise themselves in tourism advertising | MED | SR-ANSWERS-01 | R03, R19 |
| HID-01 | hidden_problems | The visible part is the weakest | HIGH | SR-HIDDEN-01 | R01, R10, R22 |
| HID-02 | hidden_problems | No natural home for the work | HIGH | SR-HIDDEN-01 | R03, R19 |
| HID-03 | hidden_problems | Nothing moves by itself | HIGH | SR-HIDDEN-01 | R14, R15 |
| HID-04 | hidden_problems | The craft route is seductive and buries the idea | MED | SR-HIDDEN-01 | R20, R07 |
| HID-05 | hidden_problems | The connecting idea is invisible until late | MED | SR-HIDDEN-01 | R22, R13 |
| BEST-01 | best_solution | Participation over spectacle | HIGH | SR-BEST-01 | R01, R03, R06, R08, R09, R10, R20, R22 |

## BEST-01 in full

> Lead with participation, not spectacle. The campaign should be built as an invitation the audience can accept and pass on, with every medium doing one job the other five cannot do. Craft and finish govern the key creative, but they do not lead the campaign.

Winner: `BEST-LIFE-DOOR-NE-P8-WITH-LIUHE`. Score 0.8200. Requirement fit **1.00**.
Runner-up retained: `BEST-OPEN-DOOR-NW-P6-WITH-DING`, role — *governs the key creative standard only: craft, finish, authority.*
Hard-eliminated: `BEST-RIDE-THE-HORSE-AT-P2`, `BEST-PUSH-THE-SHOWPIECE-AT-P9`.

## Split and veto status

| Property | Value |
|---|---|
| `STILL_TIED` split claims | **0** |
| Vetoed claims shipped | **0** |
| Silent tie-breaks | **0** — every margin is published in [[Path-Rank]] |
| AUDIT_FIX cycles used | **0 of 3** |

## Plain-English translation boundary

Every live claim crosses into `SUBMISSION/` and `ANNOTATED/` in ordinary English only. The translation table is authoritative:

| Technical | Plain English |
|---|---|
| Whole-board stasis | "Nothing moves by itself; each execution must be pushed" |
| Void showpiece at duty palace | "The most visible part is the weakest" |
| Displaced actor, no seat | "No natural home for the work" |
| P8 Life door with Liu He | "An invitation the audience accepts and passes on" |
| P6 Open door with Ding | "Craft, finish and authority" |
| Jing door Imprisoned | "Announced but does not land" |

No term in the left column appears anywhere in `SUBMISSION/`. Verified by lint gate 2 — 0 violations across 10 files.

## Linked

[[Recommended-Answers]] · [[Hidden-Problems]] · [[Solution-Architecture]] · [[Path-Rank]] · [[Risk-And-Audit-Log]]
