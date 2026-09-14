# Operator Comments

**Tree:** OPERATOR · Chart terminology permitted. Operator-facing candour.

---

## 1. Run summary

| Item | Value |
|---|---|
| Assignment | `ASSIGNMENTS/ADVERTISING/project_1.md` (Markdown, not PDF) |
| Package | `chart_analysis_package.json`, 9/9 validation checks PASS |
| `QMDJ.json` reads | **0** — enforced by `guard_path` deny-list, not by discipline |
| Requirements extracted | 22 (R01–R22) |
| Deliverables | 10, brief-derived, no `UNGROUNDED_PACK` fallback needed |
| Resolutions | 3, all RESOLVED, 0 `STILL_TIED` |
| Slot bindings | 6/6 bound, 0 unbound |
| Logo policy | `EXCLUDE_ARTWORK` |
| Forbidden-term lint | PASS, 0 violations over 10 SUBMISSION files |
| AUDIT_FIX cycles used | 0 of 3 |

---

## 2. The Markdown-not-PDF deviation

The spec names `Assignment.pdf`. The actual input is `project_1.md`, 64 lines, 2446 bytes, sha256 `96a17883…f9d6`.

**Handling:** no `pdf_extract` was invoked and no page anchors were fabricated. Requirement `page_anchor` values are the Markdown's own heading and line references. This is a faithful substitution, not an approximation — the Markdown is the complete and authoritative brief, and it contains strictly more addressable structure than a PDF page number would.

**Not** logged as an anomaly requiring remediation. Logged here so nobody later reads `page_anchor: "L31"` and assumes a PDF was silently invented.

---

## 3. Anomaly: RUBRIC_HASH_LINEAGE (LOW)

The package carries `sha256:archetype_scoring_rubric_1_0_0_chart_analyst_v4`; this phase applies `sha256:archetype_scoring_rubric_1_0_0_assignment_solver_v4`.

**Assessment: expected and correct.** Prompt 1 stamped the rubric it used; Prompt 2 legitimately applies a different rubric because `requirement_fit_score` goes live here. This is lineage, not staleness.

**Critically:** `interpretation_protocol_v2_version_hash` matched the reference exactly. That is the hash that governs `PACKAGE_STALE`, and it matched, so no halt. Both hashes are recorded in `MANIFEST.md`.

Had the protocol hash differed, the correct action would have been to halt, not to proceed with a note.

---

## 4. Where the brief changed a conclusion — and where it did not

`SUP-001`. Live requirement fit widened the P8/P6 margin from what chart grounding alone produced. **Ordering was unchanged in all three slots.**

This is the result you want. If the brief had reordered a slot, it would mean the assignment was driving the chart reading rather than being informed by it — the exact inversion the method exists to prevent. The brief sharpened confidence; it did not manufacture an answer.

Worth stating plainly: had requirement fit flipped an ordering, the correct response would have been to stop and examine whether the chart reading was being bent to fit the brief, not to accept the new ordering.

---

## 5. Judgement calls a reviewer should interrogate

**5.1 Splitting governance between two routes.** The P8 route governs campaign strategy; the P6 route governs the key creative's execution standard. This is defensible — they win different jobs — but it is a judgement call, not a mechanical output. A stricter reading would let P8 govern everything and produce a more monotonous, arguably more honest campaign. The split is recorded in `PATH_RANK.md` §1 and surfaced user-facing in `06_INTEGRATION_PROOF.md` §4 rather than hidden.

**5.2 Grading weights are inferred.** Research .25 / Strategy .25 / Execution .30 / Presentation .20. The brief does not state weights. The inference is used only to check balance, **never** to justify skipping a requirement. Every one of the 22 requirements has a coverage location regardless of weight.

**5.3 Five hidden problems shipped, one withheld.** The sixth scored 0.1902. The threshold call is defensible but it is a call. Shipping it would have added noise; withholding it is a choice a reviewer may contest.

**5.4 Creative content is invented, and that is the assignment.** The Meghalaya niche, the audience, the campaign — all authored here. What is *not* invented: any claim about the chart, the package, or the brief. The line between "creative work produced to satisfy the brief" and "fabricated input" is held strictly. No brief text was invented; no package field was invented.

---

## 6. Research honesty

The submission repeatedly states that its research is secondary and unvalidated. This is accurate and was not softened.

No visitor figures, no revenue claims, no percentages appear in `SUBMISSION/` — because none could be verified from the inputs available. The temptation to add "Meghalaya saw X lakh visitors in 2024" for credibility was refused. An unverifiable statistic in a student submission is a fabrication with a decimal point on it.

---

## 7. What is genuinely weak

1. **The creative depends on the root-bridge niche being as unique as claimed.** It is, as far as can be established without field research, but no primary verification was possible.
2. **The outdoor execution may not survive procurement.** A twelve-month living installation is a real operational commitment. The mechanical fallback exists precisely because this was foreseeable.
3. **The audience insight is an inference from working conditions.** Labelled as such in three places. It is the campaign's load-bearing assumption and it is untested.
4. **No budget.** The delivery plan gives lead times, not costs. A real pitch would be rejected for this; the brief does not ask for it.

---

## 8. Prior-phase correction carried forward

Chart phase OVR-001 stands: the original AR-BEST-01 verdict claimed a P6/P8 discriminator required assignment information. **That was wrong** — the discriminator was in the chart, in fields that had not been read.

The lesson governs this phase too: **never declare something unresolvable before every field has been read.** This is why 242/242 field coverage was made a hard gate rather than a target, and why this phase inherits a complete package rather than a partial one.

The superseded verdict is preserved, not deleted.
