---
id: red-team
type: adversarial
palace_ids: []
phase: SYNTHESIZE
batch: S3
sources: ["raw/state/solver_resolutions.json", "raw/state/solution_live.json"]
status: live
---

# Red-Team

Adversarial review of this run. The question asked throughout: **what would a hostile reviewer attack, and does it survive?**

## Attack 1 — "The brief was reverse-engineered to fit the chart"

The strongest available attack. If requirement fit had reordered any slot, the chart reading would have been bent to the assignment.

**Survives.** `SUP-001` records that live requirement fit widened the P8/P6 margin from 0.72→0.82 but **reordered nothing in any slot**. Ordering is driven by chart grounding; the brief only sharpened confidence.

Had an ordering flipped, the correct response would have been to stop and examine whether the reading was being bent — not to accept the new ordering. This is stated in `OPERATOR/COMMENTS.md` §4 *before* anyone asks.

## Attack 2 — "The creative content is invented, so the whole output is fabrication"

**Survives, with a distinction that must be held precisely.**

| Invented | Not invented |
|---|---|
| The Meghalaya niche | Any brief text |
| The audience definition | Any package field |
| The campaign, idea, executions | Any chart claim |
| All art direction | Any evidence path |

Producing creative work is the assignment. Fabricating an *input* is forbidden. The line was held: zero brief sentences invented, zero package fields invented, zero page anchors invented.

**Sharpest form of this attack:** the submission contains no statistics. That is deliberate — no visitor figures could be verified from available inputs, and an unverifiable statistic in a student submission is a fabrication with a decimal point on it. A reviewer may call the absence of numbers a weakness; inventing them would have been a violation.

## Attack 3 — "Splitting governance between two routes is having it both ways"

**Partially lands.** This is the run's most contestable judgement.

P8 governs campaign strategy; P6 governs the key creative's execution standard. A stricter reading would let P8 govern everything, producing a more monotonous but arguably more honest campaign.

**Defence:** the two routes win different jobs on stated criteria. P8 wins on transmission (rfit 1.00), which six-media integration requires. P6 wins on finish, which the one passive execution requires. Both are scored, published, and the split is surfaced user-facing in `06_INTEGRATION_PROOF.md` §4 rather than hidden in operator notes.

**Concession:** this is a judgement call, not a mechanical output, and it is labelled as such in `OPERATOR/COMMENTS.md` §5.1. A reviewer who rejects it is not misreading the evidence.

## Attack 4 — "The audience insight is unvalidated and load-bearing"

**Lands, and is conceded.** ANS-02 is MED confidence on a single evidence path. The claim that this group has never made anything lasting is an inference from working conditions, not a finding.

It is disclosed in three separate SUBMISSION locations and carried into the risk register as S2. The honest position: if this insight is wrong, the campaign's emotional premise weakens considerably. Primary validation is the first item in `09_RISK_REGISTER.md` §4.

## Attack 5 — "The outdoor execution is undeliverable"

**Partially lands.** A twelve-month living billboard requires horticultural contracts and municipal permission for a living installation. It may not survive procurement.

**Defence:** foreseen, with a mechanical fallback specified in `04_TRADITIONAL_MEDIA.md` — a painted root extended by hand monthly. The mechanic survives without the plant. Risk C5.

## Attack 6 — "Five hidden problems is convenient; where is the sixth?"

**Survives.** The sixth scored 0.1902, far below the shipped set's floor of 0.6490. It is named as withheld in [[Hidden-Problems]] and flagged as a threshold judgement in `OPERATOR/COMMENTS.md` §5.3, rather than quietly dropped.

## Attack 7 — "Gate results are self-reported by gates you wrote"

**Lands as a structural limitation, mitigated in practice.**

The gates are self-authored, so they cannot be treated as independent verification. What raises their credibility: the first run **failed 5/8**, the second **failed 7/8**, and in both cases the failures were fixed at source rather than by loosening the gate. One failure (missing `MANIFEST.md`) was a genuine omission the gate caught.

Most significantly, gate 0a was rewritten to test *import reachability* rather than to exclude a file by name — the harder, sounder test, adopted when the easier one was available. A gate suite designed to pass would not have been made stricter mid-run.

**Residual:** an external auditor should re-run `tools/s3_audit.py` and independently verify the denylist in `vault/wiki/_meta/forbidden_terms.txt` is not narrower than it should be.

## Attack 8 — "The campaign could damage the thing it advertises"

**Lands, and is the most serious substantive risk.** Root bridges are living, load-limited structures in small villages.

It is answered structurally rather than with a disclaimer: hard visitor caps, booking routed through village councils, revenue share, and volume explicitly **refused as a success metric** in `08_DELIVERY_PLAN.md` §5. Risk C1 states plainly that this is the one risk that cannot be mitigated after the fact.

## Summary

| Attack | Verdict |
|---|---|
| 1. Brief reverse-engineered | Survives |
| 2. Fabrication | Survives with distinction held |
| 3. Split governance | Partially lands — conceded as judgement |
| 4. Unvalidated insight | Lands — conceded and disclosed |
| 5. Undeliverable outdoor | Partially lands — fallback exists |
| 6. Missing sixth problem | Survives |
| 7. Self-authored gates | Lands as structural limit — mitigated |
| 8. Over-tourism | Lands — answered structurally |

Nothing found in red-teaming required an `AUDIT_FIX` cycle or the withdrawal of a live claim. Four attacks land partially or fully; **all four were already disclosed in the submission before this review**, which is the outcome the process is designed to produce.

## Linked

[[Risk-And-Audit-Log]] · [[Solution-Live]] · [[Path-Rank]] · [[Hidden-Problems]]
