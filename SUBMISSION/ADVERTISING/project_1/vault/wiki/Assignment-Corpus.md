---
id: assignment-corpus
type: source
palace_ids: []
phase: PDF_INGEST
batch: S1
sources: ["raw/assignment/Assignment.md"]
status: live
---

# Assignment-Corpus

The addressable text of the brief, and the anchor scheme used to cite it.

## Anchor scheme

Because the input is Markdown rather than PDF, anchors take the form:

| Anchor form | Meaning |
|---|---|
| `L<n>` | Line number in `Assignment.md` |
| `H:<heading>` | A Markdown heading in the brief |
| `L<a>-L<b>` | A line span |

**No `page_anchor` value in this run refers to a PDF page.** Nothing was invented to make the anchors resemble the spec's expected shape. A fabricated page number would be a fabricated input, which law forbids outright.

## Corpus properties

| Property | Value |
|---|---|
| Lines | 64 |
| Bytes | 2433 |
| sha256 | `96a17883…f9d6` |
| Headings | Brief sections covering task, purpose, exclusions, timeline, deliverable, grading |
| Immutable | Yes — verified by hash at ingest and again at audit |

## Extraction result

| Artefact | Count | Stored at |
|---|---|---|
| Requirements | 22 (R01–R22) | `vault/raw/state/requirements.json` |
| Deliverables | 10 (D01–D10) | `vault/raw/state/deliverable_registry.json` |
| Hard constraints | 3 (R01, R05, R10) | Flagged `must_not` / `must` |
| Logo boundary | `EXCLUDE_ARTWORK` | `vault/raw/state/logo_boundary.json` |

## Fidelity statement

Every requirement in [[Requirements-Matrix]] traces to a span of this corpus. No requirement was invented to justify a deliverable, and no brief sentence was paraphrased into a stronger claim than it makes. Where the brief is silent — notably on grading weights and on budget — that silence is recorded as silence, not filled in.

## Linked

[[Assignment-Brief]] · [[Requirements-Matrix]] · [[Constraints-And-Deliverables]]
