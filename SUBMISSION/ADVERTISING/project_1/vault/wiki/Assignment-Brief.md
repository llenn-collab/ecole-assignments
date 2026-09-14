---
id: assignment-brief
type: source
palace_ids: []
phase: PDF_INGEST
batch: S1
sources: ["raw/assignment/Assignment.md"]
status: live
---

# Assignment-Brief

Source: `ASSIGNMENTS/ADVERTISING/project_1.md`
sha256: `96a178833dfe2d82ab620cacfd1989c57f977ee97d2bdc7360ee93a87821f9d6`
Size: 64 lines, 2433 bytes. Format: **Markdown, not PDF**.

## Format note

The solver spec names `Assignment.pdf`. The real input is Markdown. No PDF extractor was invoked and **no page anchors were fabricated**. Requirement anchors are the Markdown's own headings and line numbers. See [[Assignment-Corpus]] for the anchor scheme and `OPERATOR/COMMENTS.md` §2 for the disclosure.

## What the brief asks for

An **integrated advertising campaign for a state tourism board**, built on a niche rather than on general destination appeal.

### Stated purpose

> Learning the difference between a truly integrated campaign and an adapt campaign.

This single line is the most important sentence in the brief. It is the grading intent, and it is why [[Solution-Architecture]] treats divisibility of the idea as the primary selection criterion.

### Core tasks

1. Choose a state and a niche within it
2. Find the USP
3. Define the target group
4. Build a creative strategy
5. Produce a key creative
6. Craft the idea across **six media types** — three traditional, three digital

### Hard exclusion

> Not sight-seeing / shopping / common spots.

Recorded as **R05**, a `must_not` constraint. Two candidate solutions were hard-eliminated against it — see [[Path-Rank]] and [[Hidden-Problems]].

### Timeline

- **Week 01** — minimum three creative routes
- **Week 02** — chosen route built into a full campaign

### Deliverable

A campaign deck.

### Grading criteria

Research, Strategy, Execution, Presentation. **Weights are not stated in the brief.** Inferred weights are recorded in [[Rubric-Guess]] and used only for balance checking, never to justify skipping a requirement.

## Linked

[[Assignment-Corpus]] · [[Requirements-Matrix]] · [[Constraints-And-Deliverables]] · [[Rubric-Guess]] · [[Logo-Boundary]]
