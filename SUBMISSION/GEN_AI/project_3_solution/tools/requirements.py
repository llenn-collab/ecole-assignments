#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
requirements.py — CAP-15 pdf_decompose / CAP-04 requirement_resolve.

Splits the assignment brief (non-PDF source: anchors degrade from page anchors to SECTION
anchors, per the charter's pdf_edge_cases rule) into requirement facets REQ-###:
  quote + anchor + artefact_type + must_level + except_logo + slug
and indexes the Assignment-1 research pack (RS-###) so every creative decision can cite a
specific finding by location, not by vibe.

Mechanical only. No interpretation of the brief text happens here.
"""
from __future__ import annotations

import os
import re
import yaml

import guarded as g

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slug(text):
    s = text.lower().replace("—", "-").replace("–", "-")
    return SLUG_RE.sub("_", s).strip("_")


BRIEF_ASSET = {"Brand Idea & Philosophy": "brief_1_brand_idea_and_philosophy",
               "Product & Packaging": "brief_2_product_and_packaging",
               "Ad / Campaign Creative Brief": "brief_3_ad_campaign_creative"}

MUST_DEFAULTS = {
    "Before You Start": "must",
    "What You're Producing: Three Distinct Briefs": "must",
    "Coherence Check (Do This Before Submitting)": "must",
    "Deliverable & Submission": "must",
    "Evaluation Criteria": "should",
}


def decompose(path):
    doc = yaml.safe_load(g.read_text(path))["document"]
    rows = []
    n = 0

    def add(quoted, anchor, artefact_type, must_level, except_logo, slug_src, extra=None):
        nonlocal n
        n += 1
        row = {"id": f"REQ-{n:03d}", "quoted_text": " ".join(str(quoted).split()),
               "page_anchor": f"section:{anchor}", "section_anchor": anchor,
               "artefact_type": artefact_type, "must_level": must_level, "except_logo": except_logo,
               "slug": slug(slug_src) or f"req_{n:03d}", "coverage_status": "UNCOVERED",
               "terminal_state": "OPEN", "satisfaction": "unsupported", "bindings": [], "gap_row": None}
        if extra:
            row.update(extra)
        rows.append(row)
        return row

    # ---- prerequisites + traceability (metadata block)
    meta = doc.get("metadata", {}) or {}
    for p in meta.get("prerequisites", []) or []:
        add(p, "metadata.prerequisites", "evidence_input", "must", False,
            f"input_{p}", {"evidence_available": None, "source_class": "assignment_1_artifact"})
    if meta.get("traceability_requirement"):
        add(meta["traceability_requirement"], "metadata.traceability_requirement", "constraint",
            "must", False, "traceability_requirement")

    # ---- sections
    for sec in doc.get("sections", []):
        head = sec.get("heading", "")
        lvl = sec.get("level", 2)
        must = MUST_DEFAULTS.get(head, "should")
        # a level-2 section that is one of the three briefs -> its subsections are the requirements
        subs = sec.get("subsections") or []
        if subs:
            for sub in subs:
                bits = [sub.get("content") or ""]
                for it in sub.get("items") or []:
                    bits.append(f"- {it}" if isinstance(it, str) else f"- {it}")
                if sub.get("note"):
                    bits.append(f"Note: {sub['note']}")
                add(" ".join(b for b in bits if b), f"{head} > {sub['heading']}", "deliverable_section",
                    "must", False, f"{head}_{sub['heading']}",
                    {"brief_asset": BRIEF_ASSET.get(head), "subsection": sub["heading"]})
            if sec.get("content"):
                add(sec["content"], head, "deliverable", "must" if must == "must" else "should", False,
                    f"{head}_umbrella", {"brief_asset": BRIEF_ASSET.get(head)})
            continue
        # table-driven section (Evaluation Criteria)
        if sec.get("table"):
            for row in sec["table"]["rows"]:
                label, desc = (row + ["", ""])[:2]
                add(f"{label}: {desc}", f"{head} > {label}", "quality_criterion", must, False,
                    f"{head}_{label}", {"criterion": label})
            if sec.get("content"):
                add(sec["content"], head, "deliverable", must, False, f"{head}_umbrella")
            continue
        # prose / item sections
        bits = [sec.get("content") or ""]
        for it in sec.get("items") or []:
            bits.append(f"- {it}" if isinstance(it, str) else f"- {it}")
        if sec.get("note"):
            bits.append(f"Note: {sec['note']}")
        add(" ".join(b for b in bits if b), head, "deliverable" if must == "must" else "quality_criterion",
            must, False, f"{head}_umbrella")

    # ---- must_not obligations the brief states as exclusions/prohibitions (verbatim quotes)
    must_nots = [
        ("Logo Direction (not the logo itself — a brief for it)", "Brief 1 — Brand Idea & Philosophy > Logo Direction",
         "exclusion_logo_artwork", True,
         "No logo artwork is produced, generated or attached; written design direction only."),
        ("Pull the audience and differentiator directly from your research — don't invent a new audience here.",
         "Brief 1 — Brand Idea & Philosophy > Positioning Statement", "prohibition_new_audience", False,
         "The audience and differentiator must come from Assignment-1 research; no new audience may be introduced."),
        ("avoid the clinical, all-lowercase sans-serif look most competitors use",
         "Brief 1 — Brand Idea & Philosophy > Logo Direction", "prohibition_logo_style", False,
         "The logo direction must explicitly avoid the category-default clinical lowercase sans-serif look."),
        ("If a choice in this assignment can't be justified by a specific research finding, a specific insight, or "
         "a specific pin on your board, it's a guess dressed up as a decision — and it should be reworked until it isn't.",
         "Before You Start", "prohibition_untraced_decisions", False,
         "Every major decision must carry a named trace source; untraced choices must be reworked."),
    ]
    for quote, anchor, sslug, except_logo, note in must_nots:
        row = add(quote, anchor, "prohibition", "must_not", except_logo, sslug,
                  {"satisfied_by_absence": True, "proof_required": True, "obligation_note": note})
    # ---- logo boundary (brief states it explicitly inside a brief-1 subsection)
    for r in rows:
        if r["slug"].startswith("brief_1_brand_idea_and_philosophy_logo_direction"):
            r["except_logo"] = True
            r["logo_boundary_note"] = ("the brief demands written design direction and explicitly "
                                       "excludes the artwork itself")
    return {"source_format": "YAML (Assignment 3 brief; non-PDF source, anchors degraded to sections)",
            "source_path": g.rel(path), "requirement_count": len(rows), "requirements": rows}


# --------------------------------------------------------------------------- research index
def index_research(path):
    doc = yaml.safe_load(g.read_text(path))["document"]
    rows = []
    n = 0

    def add(locator, heading, kind, content=None, table=None, items=None):
        nonlocal n
        n += 1
        rows.append({"id": f"RS-{n:03d}", "locator": locator, "heading": heading, "kind": kind,
                     "excerpt": " ".join(str(content or "").split())[:220],
                     "table_caption": (table or {}).get("caption"),
                     "table_headers": (table or {}).get("headers"),
                     "item_headings": [i.get("heading") for i in (items or []) if isinstance(i, dict)]})

    for part in doc.get("parts", []) or []:
        pl = f"Part {part['part']}"
        for sec in part.get("sections", []) or []:
            add(f"{pl} · {sec['heading']}", sec["heading"], "section",
                content=sec.get("content"), table=sec.get("table"), items=sec.get("items"))
            for it in sec.get("items") or []:
                if isinstance(it, dict) and it.get("heading"):
                    add(f"{pl} · {sec['heading']} · {it['heading']}", it["heading"], "item",
                        content=it.get("content"))
        if part.get("competitive_matrix"):
            add(f"{pl} · Competitive matrix", "Competitive matrix", "table", table=part["competitive_matrix"])
        for bp in part.get("brand_profiles", []) or []:
            add(f"{pl} · Brand profile · {bp['brand']}", bp["brand"], "brand_profile", content=bp.get("content"))
        for q in part.get("questions", []) or []:
            ans = q.get("answer", {}) or {}
            add(f"{pl} · Q{q['question_number']} · {ans.get('heading') or q['question']}",
                ans.get("heading") or q["question"], "question_answer",
                content=ans.get("content") or q["question"], table=ans.get("table"), items=ans.get("items"))
            if ans.get("brand_concept"):
                bc = ans["brand_concept"]
                add(f"{pl} · Q{q['question_number']} · brand concept: {bc.get('name')}",
                    f"brand concept: {bc.get('name')}", "brand_concept", table=bc.get("table"))
            for it in ans.get("items") or []:
                if isinstance(it, dict) and it.get("heading"):
                    add(f"{pl} · Q{q['question_number']} · {it['heading']}", it["heading"], "item",
                        content=it.get("content"))
    return {"source_format": doc.get("type"), "source_path": g.rel(path), "index_count": len(rows),
            "rows": rows}


if __name__ == "__main__":
    out = os.path.join(g.SOLUTION, "work")
    req = decompose(g.BRIEF)
    g.write_json(os.path.join(out, "requirements.json"), req)
    rs = index_research(g.RESEARCH)
    g.write_json(os.path.join(out, "research_index.json"), rs)
    print(f"requirements: {req['requirement_count']}")
    for r in req["requirements"]:
        print(f"  {r['id']:8s} {r['must_level']:8s} {r['slug'][:58]:58s} {r['page_anchor']}")
    print(f"\nresearch index rows: {rs['index_count']}")
    for r in rs["rows"][:8]:
        print(f"  {r['id']} {r['kind']:14s} {r['locator'][:70]}")

g.flush_log(os.path.join(g.SOLUTION, "OPERATOR", "STATE", "logs", "INGEST"),
            note="written at the end of requirements.py; the log is this phase's own accounting")
