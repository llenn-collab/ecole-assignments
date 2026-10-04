# OPERATOR / PATH_RANK — candidate ranking

Produced by CAP-10 (`state/score_card.json`). Rubric v2.1.0: grounding 0.30, corroboration 0.20,
contradiction penalty 0.15, board consistency 0.05, requirement fit 0.30. Hard-constraint compliance is a
multiplier, never an average.

| Rank | Candidate | Final | Requirement fit | Coverage | Hard | Grounding | Contradictions |
|---|---|---|---|---|---|---|---|
| 1 | **S-01 Quiet Authority** | 0.8407 | 0.9800 | 1.000 | 1.0 | COMPUTED | 2 (E077, E078) |
| 2 | S-04 Education-First, Newsletter-Led | 0.8163 | 0.8691 | 0.773 | 1.0 | EXPLICIT | 2 (E085, E086) |
| 3 | S-03 Advocacy Blitz | 0.4278 | 0.0000 | 0.250 | **0.0** | EXPLICIT | 4 |
| 4 | S-02 Broadcast Reach Sprint | 0.3778 | 0.0000 | 0.375 | **0.0** | EXPLICIT | 7 |

**Margin note.** S-01 wins on requirement coverage and on carrying both engines; S-04 is fully compliant but
leaves the display capacity idle (coverage 0.773 against 1.000). The margin is 0.024 — narrow enough to
record that S-04 is a legitimate alternative if the brand decides depth alone should carry the cycle.

**Tie policy.** No tie: `tie_state = RESOLVED`. Rows 3 and 4 are not tied candidates but vetoed ones — their
zero scores come from the compliance multiplier, not from ranking.
