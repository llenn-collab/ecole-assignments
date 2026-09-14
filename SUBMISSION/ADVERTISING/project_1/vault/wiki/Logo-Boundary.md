---
id: logo-boundary
type: policy
palace_ids: []
phase: PDF_INGEST
batch: S1
sources: ["raw/state/logo_boundary.json"]
status: live
---

# Logo-Boundary

**Policy: `EXCLUDE_ARTWORK`**

## Determination

The brief was scanned for any term that would require a produced identity artefact.

| Term | Present in brief? |
|---|---|
| logo | No |
| identity | No |
| wordmark | No |
| logotype | No |
| brand mark | No |
| visual identity | No |

**None present.** The brief asks for a campaign deck and for creatives specified across media types. It never asks for a designed mark.

## Consequence

No finished artwork of any kind is produced. Every visual in `SUBMISSION/` ships as **written art direction precise enough for a designer or director to execute without further briefing**.

This applies beyond logos:

| Would-be artefact | Shipped instead as |
|---|---|
| Logo / wordmark | Not produced, not required |
| Key visual | Written art direction (`03_KEY_CREATIVE.md` §5) |
| Storyboard frames | Shot list with framing, light, grade, prohibitions |
| Print layout | Compositional description with the gutter mechanic specified |
| Outdoor mock-up | Build specification plus twelve-month growth sequence |
| Microsite UI | Interaction sequence with timings and copy |

## Why this is a boundary and not a shortfall

The distinction the policy protects is between **specifying** and **producing**. A campaign deck's job is to specify precisely enough that production is unambiguous. Producing artwork that the brief did not request would add unverifiable craft claims to a submission whose honesty about its own limits is one of its strengths.

This is stated plainly to the assessor up front in `00_README.md` §"Two things stated plainly" and again in `01_CAMPAIGN_DECK.md` §10, so the reader is never misled about what is being submitted.

## Escape condition

The policy would flip to producing an artefact only if the brief explicitly required a non-excluded artefact. It does not. No exception was taken.

## Linked

[[Constraints-And-Deliverables]] · [[Assignment-Brief]] · [[Solution-Live]]
