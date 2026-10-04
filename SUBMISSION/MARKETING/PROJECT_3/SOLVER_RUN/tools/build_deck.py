#!/usr/bin/env python3
"""build_deck.py: renders the Assignment 2 presentation in two formats.

  SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pptx   (Python-pptx, 16:9)
  SUBMISSION/Off_Hours_Assignment_2_Content_Strategy.pdf    (ReportLab, same content)

Both are generated from the SLIDES structure below so the two formats cannot drift.
Lint-safe: no chart terminology, no metaphysical framing (checked by CAP-11).
"""
import io, os

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, "SUBMISSION")
ASSETS = os.path.join(OUT, "assets")
PPTX = os.path.join(OUT, "Off_Hours_Assignment_2_Content_Strategy.pptx")
PDF = os.path.join(OUT, "Off_Hours_Assignment_2_Content_Strategy.pdf")

BG = (0xEF, 0xE9, 0xE1)          # warm paper
INK = (0x1C, 0x1A, 0x17)
ACCENT = (0xC2, 0x54, 0x2A)
MUTED = (0x6B, 0x62, 0x59)
H_FONT = "Georgia"
B_FONT = "Helvetica"

# --------------------------------------------------------------------------- content
SLIDES = [
 ("title", "OFF HOURS", "Assignment 2. Content and Social Media Strategy",
  ["What begins when work ends.", "A continuation of the Assignment 1 deck",
   "Mumbai and Bengaluru · 10-sachet night drink · melatonin-free"]),

 ("bullets", "Where we stand, inherited from Assignment 1", None, [
   ("Retention before reach. The 10-night trial is the decision window, not an acquisition vanity metric.", None),
   ("An understated, proof-led launch. The audience is an evidence-seeking wellness sceptic, not a hype audience.", None),
   ("We compete with the habit of not switching off, not with pharmacies.", None),
   ("Deliberately delayed: celebrity blitzes, mass display, TV and print, marketplace-ad dependence, and partnership pushes.", None),
   ("Persona: Meera Nair, 32, Product Manager, Koramangala. Trials first, reads ingredients, cancels in one click.", None),
 ]),

 ("bullets", "1 · Content Marketing Objective", "Make Off Hours the brand people turn to when the evening will not switch off.",
  [("Primary. Build awareness of the moment, not of a claim.", "Recognition of the 10 pm problem comes before any product belief."),
   ("Primary. Educate consumers and own the ingredient question.", "The trust gate for an ingested product is the label. Answering the question earns the right to sell."),
   ("Secondary. Engagement, community, traffic, conversion support.", "Each is a means here, never a headline goal."),
   ("Why not more? Awareness gives recognition. Education gives permission. Everything else is downstream of those two.", None),
  ]),

 ("bullets", "2 · Brand Story and Communication", "The core idea: a landing, not a pill.",
  [("Calm. Never urgent, never a countdown. The evening is not a sale to close.", None),
   ("Plain-spoken. Ingredient answers in ordinary words. No clinical jargon, no wellness poetry.", None),
   ("Evidence-led. Show the label, the quantity, the reason. Facts, never feelings.", None),
   ("Quietly warm. Written to one tired person, not to a market.", None),
   ("Sample line: \u201cYou don't have a sleep problem. You have a landing problem.\u201d", None),
   ("Never: preachy, alarmist, medical-sounding, countdowns, streaks, competitive sneering.", None),
  ]),

 ("table", "3 · Content Pillars", "Five pillars, each with a function.",
  ([["Pillar", "Function", "Example", "Why Meera cares"],
    ["Plain Labels", "Education and trust", "What magnesium glycinate does, in 40 seconds", "She reads labels anyway"],
    ["The Landing", "Awareness", "10 pm, laptop closed, brain still on", "The moment matches her night"],
    ["Quiet Proof", "Credibility", "Unedited testimonials, including lukewarm ones", "Evidence beats promises"],
    ["After Hours", "Depth and loyalty", "The sleep-journal letter", "She wants the long version"],
    ["We Won't", "Differentiation", "Six claims we refuse to make", "Refusals are believable"]]),
  "Rotation rule: every piece belongs to exactly one pillar. A piece which fits no pillar does not go out."),

 ("table", "4 · Platform Strategy", "Three surfaces, chosen on audience behaviour.",
  ([["Platform", "Behaviour", "Role", "Formats"],
    ["Instagram", "Scrolls Reels at 10 pm", "Awareness: name the moment", "Reels, carousels, Stories Q&A"],
    ["YouTube", "Watches to research", "Education: own the ingredient answer", "6 to 8 min long-form and Shorts"],
    ["WhatsApp and e-mail", "Consented, private, read-later", "Retention: hold the 10-night window", "Plain-text notes, letters"]]),
  "Deliberately not in the plan: TV and print · mass display · celebrity blitzes · marketplace-ad dependence · alarm and outrage formats."),

 ("bullets", "5 · One Idea, Different Platforms", "Night 1 of 10, the first landing.",
  [("The idea never changes. Only the behaviour does.", None),
   ("Instagram. 25-second landing film: the kitchen at night, laptop closed, no voiceover, one line at the end.", "She sees the landing."),
   ("YouTube. 6 to 8 minute explainer plus a 45-second cut: what sits in the sachet, plainly, including what it does not do.", "She understands the landing."),
   ("WhatsApp and e-mail. One plain-text note per night for ten nights. Night one asks one question.", "She lives the landing."),
   ("Every piece points to the next surface. The referral link closes the loop back to discovery.", None),
  ]),

 ("image", "6 · Content Concepts", "Six concepts, each specified as idea, pillar, platform, format, objective.",
  os.path.join(ASSETS, "mockup_1_carousel_cover.png"),
  ["Concept 3, \u201cSix things we refuse to say\u201d, carousel slide 2 of 6.",
   "Design direction: warm off-white ground, one burnt-orange accent, editorial serif headline. No badge, no arrow, no urgency device."],
  [("1 · What magnesium glycinate does", "Plain Labels · Instagram carousel · education and saves"),
   ("2 · We read our own label out loud", "Plain Labels · YouTube long-form · education and trust"),
   ("3 · Six things we refuse to say about our own product", "We Won't · Instagram carousel · differentiation and shares"),
   ("4 · Night 1 of 10, the landing film", "The Landing · Instagram Reel · awareness"),
   ("5 · The shelf, customers' own notes, unranked", "Quiet Proof · Instagram and private channel · trust"),
   ("6 · Ask us about the label", "Plain Labels · Stories Q&A to video · engagement and education")]),

 ("image2", "6 · Content Concepts (continued)", "Concept 4, the Reel key frame with timing margin.",
  os.path.join(ASSETS, "mockup_2_reel_storyboard.png"),
  ["Shot discipline: one continuous take in a dim kitchen, single lamp source, hands and objects only, no faces. Music only in the middle beat."],
  [("The landing film, storyboard beats", "25 seconds, one continuous shot"),
   ("0 to 5s. A laptop is closed and pushed aside. Room tone only. No music.", None),
   ("5 to 15s. A hand sets down one sachet and a glass of warm water. Slow, unhurried.", None),
   ("15 to 25s. The sachet opens, pours, stirs once. The camera holds. The only text is the last line.", None),
   ("On-screen text at 20 to 25s: NIGHT 1 OF 10.", None),
   ("Why 25 seconds: the audience is scrolling at the exact hour the film shows. The idea must land in three seconds and stay saveable for tonight.", None)]),

 ("bullets", "7 · Hero Content / Campaign", "The 10-Night Landing. The trial window becomes the campaign.",
  [("Insight. The problem for Meera is not sleep. The problem is the twenty minutes between closing the laptop and reaching bed.", None),
   ("Big idea. Ten nights, ten small pieces, one per night, each a landing rather than a lesson.", None),
   ("Key message. \u201cWe are not asking you to sleep earlier. We are asking you to land better.\u201d", None),
   ("Arc. Name the moment, answer the question, hold the ten nights, let the proof speak.", None),
   ("Why this hero: the campaign turns the brand's hardest metric, the trial-to-subscription window, into content.", None),
  ]),

 ("bullets", "8 · Community and Engagement", "Followers become participants by answering a question they already answer elsewhere.",
  [("Ask-the-coach, answered in public. No question too basic, including the awkward ingredient questions.", None),
   ("The Shelf. Customers' own night notes, unranked and unedited. Inclusion, never competition.", None),
   ("Quiet Testimony. Reviews in the customer's own words. Any edit visibly marked.", None),
   ("The 10-Night Check-in. One private question a night. No scoreboard, no streak to lose.", None),
   ("Refused: competitive challenges and duets · alarm-driven live formats · announcements broadcast through community channels.", None),
  ]),

 ("table", "9 · Influencer / Creator Strategy", "Fit is a teaching-and-trust test, not a reach test.",
  ([["", "Creator A", "Creator B"],
    ["Who", "Shabbir Ahmed, Sleep Psychologist, Navi Mumbai", "Shruti Maheshwari, co-founder, Sleep Gurukul, Mumbai"],
    ["Credibility", "CBT-I practice. Author, The Sleep Foundations. MA Psychology. Doctoral research.", "Sleep and wellbeing coach, breath-work. Practice recognised at the BW Wellbeing Festival, Mumbai."],
    ["Audience", "Adults seeking behavioural answers, not chemical ones", "Indian professionals, metro, breath-work and routine-led"],
    ["Why fit", "Purest carrier of Plain Labels: method-led, positioned against hacks and unfounded claims", "Carries The Landing: teaches the ritual a product will never show. India-native practice."],
    ["Role", "Flagship educator: one explainer, one label review, one Q&A", "Ritual partner: guided ten-night wind-down series. Phase 2 corporate bridge."]]),
  "Filters first, names second: teaching ratio · private-engagement ratio · reply tone · disclosure comfort. Open checks: category conflicts, disclosure line, Mumbai and Bengaluru audience share."),

 ("table", "10 · Two-Week Content Calendar", "Ten pieces, four deliberate quiet days.",
  ([["Day", "Platform", "Content", "Format", "Pillar"],
    ["1 · Mon", "YouTube", "We read our own label out loud (anchor)", "Long-form 7 min", "Plain Labels"],
    ["2 · Tue", "None", "Quiet day", "None", "None"],
    ["3 · Wed", "Instagram", "What magnesium glycinate does, in 40 seconds", "Carousel (5)", "Plain Labels"],
    ["4 · Thu", "Instagram", "Night 1 of 10, the landing film", "Reel 25s", "The Landing"],
    ["5 · Fri", "Instagram", "Ask us about the label, weekly answers", "Stories Q&A", "Plain Labels"],
    ["6 · Sat", "WhatsApp and e-mail", "Night 5 check-in: what time did your evening end?", "Plain-text note", "After Hours"],
    ["7 · Sun", "None", "Quiet day", "None", "None"],
    ["8 · Mon", "YouTube", "Why this is not a sleeping pill (anchor)", "Long-form 6 min", "Plain Labels"],
    ["9 · Tue", "Instagram", "Six things we refuse to say about our product", "Carousel (6)", "We Won't"],
    ["10 · Wed", "None", "Quiet day", "None", "None"],
    ["11 · Thu", "Instagram", "The shelf, customers' own night notes", "Carousel (6)", "Quiet Proof"],
    ["12 · Fri", "Instagram", "Short cut of the Monday anchor", "Short 45s", "Plain Labels"],
    ["13 · Sat", "WhatsApp and e-mail", "Night 10: one thing which changed, one which did not", "Note and referral link", "Quiet Proof"],
    ["14 · Sun", "None", "Quiet day", "None", "None"]]),
  "Cadence rationale: the brand's job is a habit, not a feed. Four quiet days are a decision, not a gap. One anchor and one visual piece per week. Paid amplifies only messages already proven organically."),

 ("table", "11 · Measurement and Success", "Seven metrics, each tied to an objective, and one of them negative.",
  ([["#", "Objective", "KPI", "Healthy signal", "Cadence"],
    ["1", "Awareness", "Reach: Reels against search arrivals", "Search arrivals grow faster than Reels reach", "Monthly"],
    ["2", "Education", "Saves and returns on label explainers", "Explainers lead the month for saves", "Monthly"],
    ["3", "Consideration", "Completion rate on long-form", "The \u201cnot a pill\u201d film completes best", "Monthly"],
    ["4", "Trust", "Private interactions: saves, DM questions, replies", "Private at least equals public", "Monthly"],
    ["5", "Conversion support", "Trial starts from discovery and search", "Rising, with a healthy source mix", "Monthly"],
    ["6", "Retention", "Night-5 and night-10 check-in participation", "A meaningful share reply or stay", "Every 10 nights"],
    ["7", "Health (stop signal)", "Argument threads and complaint mentions", "Flat or falling", "Monthly"]]),
  "Month one, working when saves lead, private responses match public ones, check-ins receive answers and argument threads stay flat. Not working when reach rises while saves stall."),

 ("bullets", "Continuity, risks and what would change our mind", "Every choice here traces back to Assignment 1, and every risk is named.",
  [("Viable alternative on record: an education-first, newsletter-led plan. Fully compliant, and it leaves the display surface idle. The margin is narrow (0.84 against 0.82) and stated.", None),
   ("Risk 1. The quiet channel is favourable but slow. Judge the channel across a full cycle, not a month.", None),
   ("Risk 2. Restraint becomes inaudibility. Display content carries reach, and we track reach.", None),
   ("Risk 3. Partnership announcements under-deliver in alliance channels. Those channels stay two-way.", None),
   ("Risk 4. Creator conflicts and audience geography are unverified. Three checks run before contracting.", None),
   ("Strategy first. Design second. Every creative decision has a reason, and the reason is always the same: this brand exists to end the day, not to win the feed.", None),
  ]),
]

# --------------------------------------------------------------------------- PPTX
def build_pptx():
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

    W, H = Inches(13.333), Inches(7.5)
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    blank = prs.slide_layouts[6]

    def bg(slide):
        r = slide.shapes.add_shape(1, 0, 0, W, H)
        r.fill.solid(); r.fill.fore_color.rgb = RGBColor(*BG); r.line.fill.background()
        r.shadow.inherit = False
        return r

    def tb(slide, x, y, w, h):
        box = slide.shapes.add_textbox(x, y, w, h)
        tf = box.text_frame; tf.word_wrap = True
        return tf

    def para(tf, text, size, color, font, bold=False, first=False, space=6, italic=False):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        p.text = text
        for run in p.runs:
            run.font.size = Pt(size); run.font.bold = bold; run.font.italic = italic
            run.font.color.rgb = RGBColor(*color); run.font.name = font
        p.space_after = Pt(space)
        return p

    def accent_rule(slide, x, y, w):
        bar = slide.shapes.add_shape(1, x, y, w, Pt(3))
        bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor(*ACCENT); bar.line.fill.background()
        bar.shadow.inherit = False

    def table_shape(slide, data, x, y, w, h, widths=None):
        rows, cols = len(data), len(data[0])
        shp = slide.shapes.add_table(rows, cols, x, y, w, h)
        tbl = shp.table
        if widths:
            total = sum(widths)
            for i, ww in enumerate(widths):
                tbl.columns[i].width = int(w * ww / total)
        for ri, row in enumerate(data):
            for ci, val in enumerate(row):
                cell = tbl.cell(ri, ci)
                cell.text = str(val)
                cell.margin_left = Pt(6); cell.margin_right = Pt(4)
                cell.margin_top = Pt(2); cell.margin_bottom = Pt(2)
                cell.vertical_anchor = MSO_ANCHOR.TOP
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(*(0xE4, 0xDC, 0xD1) if ri == 0 else
                                                   (0xF6, 0xF2, 0xEC) if ri % 2 else (0xEF,0xE9,0xE1))
                for p in cell.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(11 if len(data) > 8 else 12)
                        r.font.name = B_FONT
                        r.font.bold = (ri == 0)
                        r.font.color.rgb = RGBColor(*(INK if ri == 0 else (0x33, 0x2F, 0x2B)))
        return tbl

    for slide_spec in SLIDES:
        kind, title, subtitle = slide_spec[0], slide_spec[1], slide_spec[2]
        body = slide_spec[3]
        if kind == "title":
            s = prs.slides.add_slide(blank); bg(s)
            tf = tb(s, Inches(0.9), Inches(2.1), Inches(11.5), Inches(3.2))
            para(tf, title, 54, INK, H_FONT, bold=True, first=True, space=10)
            para(tf, subtitle, 22, ACCENT, B_FONT, space=18)
            for i, line in enumerate(body if isinstance(body, list) else []):
                para(tf, line, 14, MUTED, B_FONT, space=4)
            accent_rule(s, Inches(0.9), Inches(5.6), Inches(3.4))
            tf2 = tb(s, Inches(0.9), Inches(5.9), Inches(11.5), Inches(0.8))
            para(tf2, "Assignment 2 · Content & Social Media Strategy · submission 5 October 2026",
                 12, MUTED, B_FONT, first=True)
            continue

        s = prs.slides.add_slide(blank); bg(s)
        tf = tb(s, Inches(0.7), Inches(0.45), Inches(12), Inches(1.2))
        para(tf, title, 26, INK, H_FONT, bold=True, first=True, space=4)
        if subtitle:
            para(tf, subtitle, 15, ACCENT, B_FONT, italic=False, space=0)
        accent_rule(s, Inches(0.7), Inches(1.62), Inches(2.6))

        if kind == "bullets":
            tf = tb(s, Inches(0.75), Inches(2.0), Inches(11.9), Inches(5.0))
            for i, item in enumerate(body):
                main, note = item if isinstance(item, tuple) else (item, None)
                para(tf, "-  " + main, 15, (0x2A, 0x26, 0x22), B_FONT, first=(i == 0), space=3)
                if note:
                    para(tf, "         " + note, 12, MUTED, B_FONT, space=9)
        elif kind in ("table",):
            data, footnote = body, slide_spec[4]
            table_shape(s, data, Inches(0.7), Inches(1.9), Inches(12.0), Inches(4.4),
                        widths=[1.0] * len(data[0]))
            tf = tb(s, Inches(0.75), Inches(6.5), Inches(11.9), Inches(0.9))
            para(tf, footnote, 12, MUTED, B_FONT, first=True, italic=True)
        elif kind in ("image", "image2"):
            img, captions = body, slide_spec[4]
            extras = slide_spec[5] if len(slide_spec) > 5 else []
            if kind == "image":
                s.shapes.add_picture(img, Inches(0.75), Inches(1.85), height=Inches(4.5))
                tf = tb(s, Inches(5.35), Inches(1.9), Inches(7.4), Inches(4.9))
            else:
                s.shapes.add_picture(img, Inches(0.75), Inches(1.8), height=Inches(4.7))
                tf = tb(s, Inches(5.8), Inches(1.9), Inches(6.9), Inches(4.9))
            for i, c in enumerate(captions):
                para(tf, c, 12.5 if i == 0 else 11, INK if i == 0 else MUTED, B_FONT,
                     bold=(i == 0), first=(i == 0), space=8)
            for i, item in enumerate(extras):
                main, sub = item if isinstance(item, tuple) else (item, None)
                para(tf, main, 11.5, (0x2A, 0x26, 0x22), B_FONT, bold=(i == 0), space=2)
                if sub:
                    para(tf, "       " + sub, 10, MUTED, B_FONT, space=7)

    prs.save(PPTX)
    return PPTX

# --------------------------------------------------------------------------- PDF
def build_pdf():
    from reportlab.lib.pagesizes import landscape
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                    Table, TableStyle, Image as RLImage, KeepTogether)

    page = landscape((11 * inch, 8.27 * inch))
    ink = colors.Color(*[c / 255 for c in INK])
    accent = colors.Color(*[c / 255 for c in ACCENT])
    muted = colors.Color(*[c / 255 for c in MUTED])
    paper = colors.Color(*[c / 255 for c in BG])
    tint = colors.Color(*[c / 255 for c in (0xE4, 0xDC, 0xD1)])
    rowt = colors.Color(*[c / 255 for c in (0xF6, 0xF2, 0xEC)])

    doc = BaseDocTemplate(PDF, pagesize=page, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
                          topMargin=0.55 * inch, bottomMargin=0.5 * inch,
                          title="Off Hours. Assignment 2 Content and Social Media Strategy",
                          author="Off Hours")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def canvas_bg(canv, d):
        canv.saveState()
        canv.setFillColor(paper); canv.rect(0, 0, page[0], page[1], stroke=0, fill=1)
        canv.setFillColor(accent)
        canv.rect(doc.leftMargin, page[1] - 0.42 * inch, 2.2 * inch, 1.6, stroke=0, fill=1)
        canv.setFillColor(muted); canv.setFont("Helvetica", 8)
        canv.drawString(doc.leftMargin, 0.33 * inch,
                        "Off Hours · Assignment 2 · Content & Social Media Strategy · 5 October 2026")
        canv.drawRightString(page[0] - doc.rightMargin, 0.33 * inch, "%d" % d.page)
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=canvas_bg)])

    h1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=30, leading=34, textColor=ink)
    h2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=19, leading=23, textColor=ink,
                        spaceAfter=2)
    h3 = ParagraphStyle("h3", fontName="Times-Italic", fontSize=12.5, leading=15, textColor=accent,
                        spaceAfter=10)
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=12.6, textColor=ink,
                          spaceAfter=3.5)
    note = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8.2, leading=10.4,
                          textColor=muted, spaceBefore=6)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=10, bulletIndent=0)
    tcell = ParagraphStyle("tcell", fontName="Helvetica", fontSize=7.6, leading=9.4, textColor=ink)
    thead = ParagraphStyle("thead", fontName="Helvetica-Bold", fontSize=7.6, leading=9.4,
                           textColor=ink)

    def esc(x):
        """reportlab Paragraph text needs XML escaping, or '&' corrupts on render."""
        return (str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

    flow = []
    for spec in SLIDES:
        kind, title, subtitle, bodydata = spec[0], spec[1], spec[2], spec[3]
        if kind == "title":
            flow.append(Spacer(1, 1.9 * inch))
            flow.append(Paragraph(esc(title), h1))
            flow.append(Spacer(1, 6))
            flow.append(Paragraph(esc(subtitle), ParagraphStyle("st", fontName="Helvetica", fontSize=14,
                                                           textColor=accent, spaceAfter=12)))
            for line in bodydata:
                flow.append(Paragraph(esc(line), body))
            flow.append(Spacer(1, 26))
            flow.append(Paragraph("Assignment 2 · Content & Social Media Strategy · "
                                  "submission 5 October 2026", note))
            from reportlab.platypus import PageBreak
            flow.append(PageBreak())
            continue

        flow.append(Paragraph(esc(title), h2))
        if subtitle:
            flow.append(Paragraph(esc(subtitle), h3))
        if kind == "bullets":
            for item in bodydata:
                main, sub = item if isinstance(item, tuple) else (item, None)
                flow.append(Paragraph(esc(main), bullet, bulletText="-"))
                if sub:
                    flow.append(Paragraph(esc(sub), ParagraphStyle("sn", parent=note, leftIndent=10,
                                                              spaceBefore=1, spaceAfter=6)))
        elif kind == "table":
            data, footnote = bodydata, spec[4]
            rows = [[Paragraph(esc(c), thead if ri == 0 else tcell) for c in row]
                    for ri, row in enumerate(data)]
            t = Table(rows, repeatRows=1)
            style = [("GRID", (0, 0), (-1, -1), 0.4, tint),
                     ("BACKGROUND", (0, 0), (-1, 0), tint),
                     ("VALIGN", (0, 0), (-1, -1), "TOP"),
                     ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                     ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
            for ri in range(1, len(rows)):
                if ri % 2 == 0:
                    style.append(("BACKGROUND", (0, ri), (-1, ri), rowt))
            t.setStyle(TableStyle(style))
            flow.append(Spacer(1, 3)); flow.append(t)
            flow.append(Paragraph(esc(footnote), note))
        elif kind in ("image", "image2"):
            img, captions = bodydata, spec[4]
            extras = spec[5] if len(spec) > 5 else []
            from PIL import Image as PILImage
            iw, ih = PILImage.open(img).size
            avail_h = 4.3 * inch
            render_h = avail_h
            render_w = avail_h * iw / float(ih)
            if render_w > 4.2 * inch:
                render_w = 4.2 * inch
                render_h = render_w * ih / float(iw)
            right = [Paragraph(esc(captions[0]), body)] + [Paragraph(esc(c), note) for c in captions[1:]]
            for i, item in enumerate(extras):
                main, sub = item if isinstance(item, tuple) else (item, None)
                right.append(Paragraph(esc(main), ParagraphStyle("ex", parent=tcell, fontName="Helvetica-Bold"
                                                            if i == 0 else "Helvetica", fontSize=8.4,
                                                            leading=10.6, spaceBefore=5)))
                if sub:
                    right.append(Paragraph(esc(sub), ParagraphStyle("exs", parent=note, fontSize=7.6,
                                                               leftIndent=8, spaceBefore=1,
                                                               spaceAfter=0)))
            tbl = Table([[RLImage(img, width=render_w, height=render_h), right]],
                        colWidths=[render_w + 0.18 * inch, None])
            tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                     ("LEFTPADDING", (0, 0), (0, 0), 0)]))
            flow.append(Spacer(1, 4)); flow.append(tbl)

        from reportlab.platypus import PageBreak
        flow.append(PageBreak())

    doc.build(flow)
    return PDF


if __name__ == "__main__":
    print("pptx:", build_pptx())
    print("pdf :", build_pdf())
