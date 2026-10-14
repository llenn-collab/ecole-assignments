#!/usr/bin/env python3
"""Build design deliverables from authored campaign state; not a charter CAP harness.
Run from project_2: .venv/bin/python OPERATOR/build_deliverables.py
Reads only campaign_spec.json and the authored campaign report in this project folder.
"""
import csv
import hashlib
import html
import io
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase.pdfmetrics import stringWidth
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pypdf import PdfReader
import fitz

BASE = Path(__file__).resolve().parents[1]
SUB = BASE / 'SUBMISSION'
ART = SUB / 'ARTWORK'
ART.mkdir(parents=True, exist_ok=True)
SPEC = json.loads((BASE / 'OPERATOR/campaign_spec.json').read_text())
INK, PAPER, SIGNAL, MUTED = '#172C28', '#F2F0E5', '#DEEF54', '#587167'


def norm(s):
    # PDF base fonts do not contain a rupee glyph; retain meaning explicitly.
    return s.replace('₹', 'INR ').replace('→', ' / ').replace('–', '-').replace('—', ' - ').replace('’', "'").replace('“', '"').replace('”', '"').replace('•', ' / ')


class Draw:
    """A small shared vector drawing surface for matched editable SVG and PDF."""
    def __init__(self, c, w, h):
        self.c, self.w, self.h = c, w, h
        self.svg = []

    def rect(self, x, y, w, h, fill, radius=0):
        self.c.setFillColor(colors.HexColor(fill))
        self.c.setStrokeColor(colors.HexColor(fill))
        self.c.roundRect(x, y, w, h, radius, fill=1, stroke=0)
        self.svg.append(f'<rect x="{x}" y="{self.h-y-h}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"/>')

    def line(self, x1, y1, x2, y2, stroke, width=1):
        self.c.setStrokeColor(colors.HexColor(stroke)); self.c.setLineWidth(width)
        self.c.line(x1, y1, x2, y2)
        self.svg.append(f'<line x1="{x1}" y1="{self.h-y1}" x2="{x2}" y2="{self.h-y2}" stroke="{stroke}" stroke-width="{width}"/>')

    def text(self, x, y, t, size, fill, bold=False, maxw=None):
        font = 'Helvetica-Bold' if bold else 'Helvetica'
        t = norm(t)
        if maxw:
            while stringWidth(t, font, size) > maxw:
                size -= .25
        self.c.setFillColor(colors.HexColor(fill)); self.c.setFont(font, size)
        self.c.drawString(x, y, t)
        self.svg.append(f'<text x="{x}" y="{self.h-y}" fill="{fill}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}">{escape(t)}</text>')

    def helmet(self, x, y, s, fill):
        # Stylized helmet symbol, not equipment artwork or a certification mark.
        self.c.setFillColor(colors.HexColor(fill))
        p = self.c.beginPath()
        p.moveTo(x, y+s*.25); p.curveTo(x-s*.03, y+s*.93, x+s*.85, y+s*1.04, x+s, y+s*.43)
        p.lineTo(x+s*.72, y+s*.43); p.lineTo(x+s*.72, y+s*.22)
        p.lineTo(x+s*.40, y+s*.12); p.lineTo(x+s*.12, y+s*.16); p.close()
        self.c.drawPath(p, fill=1, stroke=0)
        self.svg.append(f'<path d="M {x} {self.h-y-s*.25} C {x-s*.03} {self.h-y-s*.93} {x+s*.85} {self.h-y-s*1.04} {x+s} {self.h-y-s*.43} L {x+s*.72} {self.h-y-s*.43} L {x+s*.72} {self.h-y-s*.22} L {x+s*.40} {self.h-y-s*.12} L {x+s*.12} {self.h-y-s*.16} Z" fill="{fill}"/>')
        # Chinstrap drawn visibly closed.
        self.line(x+s*.30, y+s*.17, x+s*.34, y+s*.03, fill, max(1, s*.035))
        self.line(x+s*.34, y+s*.03, x+s*.65, y+s*.12, fill, max(1, s*.035))

    def save_svg(self, path, width_attr, height_attr, title, desc):
        s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_attr}" height="{height_attr}" viewBox="0 0 {self.w} {self.h}" role="img"><title>{escape(title)}</title><desc>{escape(desc)}</desc>' + ''.join(self.svg) + '</svg>\n'
        path.write_text(s)


def make_art(kind, name, size):
    w,h=size
    c=canvas.Canvas(str(ART/f'{name}.pdf'), pagesize=size, invariant=1)
    c.setTitle(SPEC['title']+' / '+kind)
    d=Draw(c,w,h)
    if kind=='seat':
        d.rect(0,0,w,h,INK)
        d.text(22,h-32,'BEFORE YOU SIT',10,SIGNAL,True)
        d.text(22,h-82,'THIS SEAT',36,PAPER,True,maxw=w-44)
        d.text(22,h-124,'HAS A HEAD.',36,PAPER,True,maxw=w-44)
        d.text(22,h-172,'YOURS.',43,SIGNAL,True)
        d.helmet(w-91,h-172,58,SIGNAL)
        d.line(22,93,w-22,93,MUTED)
        d.text(22,73,'Pillion passengers need a helmet too.',12,PAPER,True,maxw=w-44)
        d.text(22,51,'Put on and fasten your helmet before you ride.',10,PAPER,maxw=w-44)
        d.text(22,18,'STUDENT PROTOTYPE / REMOVE BEFORE MOUNTING',6.7,SIGNAL,True,maxw=w-44)
        d.save_svg(ART/f'{name}.svg','148mm','105mm',SPEC['title'],'A temporary stationary-seat campaign card. Pillion passengers need a helmet too. Put on and fasten your helmet before you ride. Remove before mounting.')
    elif kind=='poster':
        # Normalized A3 coordinates retain generous print margins.
        c.saveState(); c.scale(w/595,h/842)
        d=Draw(c,595,842)
        d.rect(0,0,595,842,PAPER)
        d.rect(32,789,531,3,INK)
        d.text(32,758,'A REMINDER FOR BOTH OF YOU',11,MUTED,True)
        d.text(32,674,'TWO',79,INK,True)
        d.text(32,589,'SEATS.',79,INK,True)
        d.rect(32,370,531,169,SIGNAL,12)
        d.helmet(88,398,121,INK); d.helmet(356,398,121,INK)
        d.text(32,310,'TWO HELMETS.',53,INK,True,maxw=531)
        d.text(32,252,'BOTH FASTENED.',49,INK,True,maxw=531)
        d.line(32,218,563,218,INK)
        d.text(32,180,'Riding together?',22,INK,True)
        d.text(32,149,'Check each other before you leave.',18,INK,maxw=531)
        d.text(32,87,'Use a well-fitting BIS-certified motorcycle helmet.',12,MUTED,maxw=531)
        d.text(32,38,'THIS SEAT HAS A HEAD. / STUDENT CAMPAIGN PROTOTYPE',8,MUTED,True,maxw=531)
        c.restoreState()
        d.save_svg(ART/f'{name}.svg','297mm','420mm','Two seats. Two helmets. Both fastened.','Riding together? Check each other before you leave. Use a well-fitting BIS-certified motorcycle helmet.')
    else:
        d.rect(0,0,w,h,INK)
        d.text(28,h-47,'BEFORE THE NEXT SHARED RIDE',10,SIGNAL,True)
        for y,t in [(h-120,"WHO'S ON"),(h-179,'YOUR SECOND'),(h-238,'SEAT?')]:
            d.text(28,y,t,44,PAPER,True,maxw=w-56)
        d.helmet(44,287,112,PAPER); d.helmet(245,287,112,SIGNAL)
        d.line(28,245,w-28,245,MUTED)
        d.text(28,206,'Riding together?',19,PAPER,True)
        d.text(28,169,'Both helmets on.',23,SIGNAL,True)
        d.text(28,137,'Both straps fastened.',23,SIGNAL,True,maxw=w-56)
        d.text(28,77,'Check before you ride. Never while riding.',11,PAPER,maxw=w-56)
        d.text(28,29,'THIS SEAT HAS A HEAD. / STUDENT PROTOTYPE',7.7,MUTED,True,maxw=w-56)
        d.save_svg(ART/f'{name}.svg','1080','1920',"Who's on your second seat?",'Both helmets on. Both straps fastened. Check before you ride, never while riding.')
    c.showPage(); c.save()
    doc=fitz.open(ART/f'{name}.pdf')
    doc[0].get_pixmap(matrix=fitz.Matrix(1080/w,1080/w),alpha=False).save(ART/f'{name}.png')


make_art('seat','seat_card_A6',(148*72/25.4,105*72/25.4))
make_art('poster','poster_A3',A3)
make_art('story','social_story_1080x1920',(405,720))


def report_pdf():
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CampaignTitle',fontName='Helvetica-Bold',fontSize=32,leading=36,textColor=colors.HexColor(INK),spaceAfter=22))
    styles['Heading1'].textColor=colors.HexColor(INK)
    styles['Heading2'].textColor=colors.HexColor(INK)
    styles['BodyText'].fontName='Helvetica'; styles['BodyText'].fontSize=9.8; styles['BodyText'].leading=14
    styles['BodyText'].spaceAfter=8
    story=[]
    text=(SUB/'CAMPAIGN_REPORT.md').read_text()
    for block in text.split('\n\n'):
        block=block.strip()
        if not block: continue
        style=styles['BodyText']
        if block.startswith('# '): style=styles['CampaignTitle']; block=block[2:]
        elif block.startswith('## '): style=styles['Heading1']; block=block[3:]
        elif block.startswith('### '): style=styles['Heading2']; block=block[4:]
        block=norm(block)
        block=escape(block)
        block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block)
        # Keep readable linked labels while clickable targets remain in the PDF.
        block=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#587167">[\1]</link>',block)
        block=block.replace('\n','<br/>').replace('`','')
        story.append(Paragraph(block,style))
    def footer(c,doc):
        c.setStrokeColor(colors.HexColor(MUTED)); c.line(42,35,A4[0]-42,35)
        c.setFont('Helvetica',7); c.setFillColor(colors.HexColor(MUTED))
        c.drawString(42,23,'THIS SEAT HAS A HEAD. / DESIGN SUBMISSION / NOT DEPLOYED')
        c.drawRightString(A4[0]-42,23,str(doc.page))
    SimpleDocTemplate(str(SUB/'CAMPAIGN_REPORT.pdf'),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=40,bottomMargin=48,title=SPEC['title'],author='Student campaign submission').build(story,onFirstPage=footer,onLaterPages=footer)


report_pdf()

# Authored presentation content. Factual notes are attached to the relevant slide,
# not hidden solely in a final bibliography.
slides=[
 {'kicker':'ADVERTISING 2 / CRAFTING FOR A SOCIAL CAUSE','title':'THIS SEAT\nHAS A HEAD.','body':'The overlooked second rider.\nA campaign on the seat they are about to occupy.','note':'DESIGN PROPOSAL / NOT DEPLOYED','art':'seat_card_A6'},
 {'kicker':'01 / NARROW THE CAUSE','title':'The person\non the second seat.','body':'Cause: pillion helmet use on everyday shared journeys.\nFocus: adult driver-pillion pairs, stationary before departure.\nNot a new product, app, rental scheme or service.','note':'Age 18-30 and private-parking setting are strategic choices, not measured local prevalence.'},
 {'kicker':'02 / NATIONAL CONTEXT','title':'14,652','body':'Passenger fatalities recorded in the non-wearing-of-helmet category in India, 2024.\n54,122 total fatalities in that category.','note':'MoRTH data via inspected OpenCity table records and Hindustan Times, 12 June 2026. Same underlying dataset; original ministry table cells not directly inspected. Not proof nonuse caused every crash.'},
 {'kicker':'03 / THE BEHAVIOURAL OPPORTUNITY','title':'Knowing is not\nalways doing.','body':'346 adult crash patients in one eastern-India hospital sample.\n96.6% agreed helmets were essential; 35.7% had used one.\nShort-distance travel and forgetfulness were associated with nonuse.','note':'Mishra et al., 2025; data March-December 2021. Hospital sample, not national/Mumbai prevalence. Association, not causation. PMC12020946 / DOI 10.4103/ijciis.ijciis_85_24.'},
 {'kicker':'04 / AUDIENCE AND INSIGHT','title':'Make the second\nperson present.','body':'Audience: adult student / early-career driver-pillion pairs.\nHypothesis: on an ordinary shared ride, the second seat can become an afterthought.\nPut the reminder where the second person is about to sit.','note':'Creative hypothesis, not a participant quote. Local reasons for nonuse remain to be tested.'},
 {'kicker':'05 / SINGLE-MINDED STRATEGY','title':'Their own helmet.\nBefore the ride.','body':'Proposition: the second person needs their own helmet too.\nAction: both helmets on; both chinstraps fastened.\nTone: direct, considerate, no blame or simulated enforcement.','note':'Correct helmet use reduces risk, not all risk. WHO road-traffic fact sheet, 20 July 2026; PIB helmet guidance, 12 July 2025.'},
 {'kicker':'06 / THREE MEDIA CONCEPTS','title':'Three routes.\nOne campaign.','body':'01 SECOND-SEAT MESSAGE - selected: seat is the placement.\n02 TWO-PERSON PARKING SLIP - rejected: close receipt precedent.\n03 PLUS-ONE RIDE INVITE - reserve: before-ride social message.','note':'Receipt precedent: HDFC Bank / STUDDS, The Helmet Receipt, reported February 2026. No claim of exhaustive originality clearance.'},
 {'kicker':'07 / THE SELECTED MEDIA INNOVATION','title':'The seat supplies\nthe meaning.','body':'An A6 card rests on the stationary pillion seat.\nIt addresses the passenger at the mounting decision.\nNo scan. No sign-up. No new service.\nFacilitator removes it before anyone mounts.','note':'Opt-in, permissioned, supervised placement only. No adhesive or vehicle alteration. Stop if safe collection cannot be assured.'},
 {'kicker':'08 / HERO EXECUTION','title':'THIS SEAT\nHAS A HEAD.','body':'YOURS.\nPillion passengers need a helmet too.\nPut on and fasten your helmet before you ride.','note':'Finished A6 artwork supplied as PDF, SVG and PNG. Supervised prototype; remove before mounting.','art':'seat_card_A6'},
 {'kicker':'09 / CONTEXT DEMONSTRATION','title':'Where the second\nperson is about to sit.','body':'A parked vehicle. Engine off. Adult participants opt in.\nMessage placed briefly on the rear seat.\nCard collected and accounted for before mounting.','note':'Illustrated placement mockup, not a photograph or evidence of deployment.','context':True},
 {'kicker':'10 / ONE VISUAL SYSTEM','title':'Two seats.\nTwo helmets.','body':'Equal-scale helmet symbols. One clear instruction.\nDeep green + warm ivory + signal yellow-green.\nSupporting poster reinforces the pre-ride check.','note':'No certification marks, police styling, sponsor logo, crash imagery or claim of guaranteed protection.','art':'poster_A3'},
 {'kicker':'11 / DIGITAL EXTENSION','title':"Who's on your\nsecond seat?",'body':'A captioned 15-second illustrated sequence.\nOne bike / two people / two helmets / both fastened.\nCheck before the ride, never while riding.','note':'HTML motion prototype and vertical artwork supplied. Not live-action footage or a claimed platform deployment.','art':'social_story_1080x1920'},
 {'kicker':'12 / EXECUTION','title':'Small enough\nto demonstrate safely.','body':'12 reusable A6 cards + 2 A3 posters.\nPermissioned stationary encounter; no unattended placement.\nNo helmet or vehicle attachments.\nNo permission? Use the illustrated demonstration only.','note':'No partner, venue access, participant consent or filming is claimed to have been secured.'},
 {'kicker':'13 / FEASIBILITY','title':'INR 700','body':'Cards 180 / Posters 160 / Proofs 160\nConsent and tally sheets 50 / Contingency 150\nUses existing print media and a supervised setting.','note':'Planning assumptions, not vendor quotes. Excludes labour, travel, permissions, tax changes and helmet purchase.'},
 {'kicker':'14 / VALIDATION, NOT INVENTED RESULTS','title':'Did the message\nactually arrive?','body':'Proposed comprehension test: 12 consenting adults.\nProposed revision gate: 10 identify passenger helmet use + fastening before departure.\nAsk openly about meaning, tone, timing and confusion.','note':'No tests conducted. Threshold is an operational design gate, not a validated benchmark. Any safety concern triggers revision.'},
 {'kicker':'15 / EVALUATION AND LIMITS','title':'Measure the check.\nDo not promise lives saved.','body':'Optional pilot: aggregate observations of paired departures.\nRecord both helmets, visible straps and unknown observations.\nNo plates, faces, names or equipment-certification claims.\nAn uncontrolled small pilot cannot establish causality.','note':'Plan only. Do not report invented lifts, audience quotes, crash reductions or long-term effectiveness.'},
 {'kicker':'16 / PROJECT PROGRESSION','title':'From evidence\nto one clear action.','body':'14 OCT - cause, research / insight, three concepts.\n21 OCT - design WIP and feasible comprehension work.\n27 OCT - campaign submission.\n28 OCT - presentation and final review.','note':'Dates as supplied in the assignment brief; brief specifies no year. Actual fieldwork, permissions and outcomes remain unclaimed.'},
 {'kicker':'17 / RESEARCH AND PRECEDENT','title':'Traceable facts.\nHonest limitations.','body':'Mishra et al., 2025 / PMC12020946 / primary hospital study.\nMoRTH 2024 data / reproduced OpenCity table + HT reporting.\nWHO, Road traffic injuries / updated 20 July 2026.\nPIB, Helmet - More Than Just a Shell / 12 July 2025.\nMediaNews4u / The Helmet Receipt / 7 February 2026.','note':'Complete URLs and claim limits in CAMPAIGN_REPORT and the research ledger. Sources accessed 14 October 2026.'},
 {'kicker':'THE TAKEAWAY','title':'Two seats.\nTwo helmets.\nBoth fastened.','body':'The second person is not an afterthought.','note':'THIS SEAT HAS A HEAD. / STUDENT DESIGN SUBMISSION'}
]
(BASE/'OPERATOR/presentation_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')


def wrap(t,font,size,width):
    lines=[]
    for para in norm(t).split('\n'):
        line=''
        for word in para.split():
            candidate=(line+' '+word).strip()
            if stringWidth(candidate,font,size)>width and line:
                lines.append(line);line=word
            else: line=candidate
        lines.append(line)
    return lines


def draw_context(c,x,y,w,h):
    # Abstract parked scooter silhouette, deliberately not a technical equipment diagram.
    c.setFillColor(colors.HexColor(PAPER));c.roundRect(x,y,w,h,14,fill=1,stroke=0)
    c.setFillColor(colors.HexColor(INK))
    c.roundRect(x+w*.15,y+h*.27,w*.65,h*.15,14,fill=1,stroke=0)
    c.circle(x+w*.26,y+h*.24,w*.09,fill=1,stroke=0);c.circle(x+w*.75,y+h*.24,w*.09,fill=1,stroke=0)
    c.roundRect(x+w*.22,y+h*.45,w*.48,h*.09,8,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor(INK));c.setLineWidth(9)
    c.line(x+w*.75,y+h*.35,x+w*.80,y+h*.68);c.line(x+w*.75,y+h*.68,x+w*.9,y+h*.68)
    c.setFillColor(colors.HexColor(SIGNAL));c.roundRect(x+w*.24,y+h*.48,w*.21,h*.06,2,fill=1,stroke=0)
    c.setFillColor(colors.HexColor(INK))
    c.setFont('Helvetica-Bold',9);c.drawString(x+16,y+h-24,'ILLUSTRATED STATIONARY PLACEMENT')
    c.setFont('Helvetica',9);c.drawString(x+16,y+18,'Rear-seat card removed before anyone mounts.')


# Standalone illustrated mockup: final artwork shown on the stationary seat.
ctx=canvas.Canvas(str(ART/'stationary_context_mockup.pdf'),pagesize=(960,600),invariant=1)
ctx.setFillColor(colors.HexColor(INK));ctx.rect(0,0,960,600,fill=1,stroke=0)
ctx.setFillColor(colors.HexColor(PAPER));ctx.setFont('Helvetica-Bold',30)
ctx.drawString(40,544,'THE SECOND SEAT BECOMES THE MEDIUM.')
draw_context(ctx,40,122,550,360)
ctx.drawImage(str(ART/'seat_card_A6.png'),176,292,width=107,height=76,preserveAspectRatio=True,mask='auto')
ctx.setStrokeColor(colors.HexColor(SIGNAL));ctx.setLineWidth(2)
ctx.line(286,346,636,398)
ctx.drawImage(str(ART/'seat_card_A6.png'),628,273,width=292,height=208,preserveAspectRatio=True,mask='auto')
ctx.setFillColor(colors.HexColor(PAPER));ctx.setFont('Helvetica-Bold',15)
ctx.drawString(628,235,'On the rear seat, before the ride.')
ctx.setFont('Helvetica',11)
ctx.drawString(628,209,'Owner opt-in. Engine off. Supervised.')
ctx.drawString(628,189,'No adhesive or vehicle alteration.')
ctx.drawString(628,169,'Collect the card before anyone mounts.')
ctx.setFont('Helvetica',10);ctx.drawString(40,62,'ILLUSTRATED CONCEPT MOCKUP / NOT A DEPLOYMENT PHOTOGRAPH / NO REAL SITE OR PARTNER CLAIMED')
ctx.showPage();ctx.save()
ctxdoc=fitz.open(ART/'stationary_context_mockup.pdf')
ctxdoc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(ART/'stationary_context_mockup.png')

W,H=960,540
c=canvas.Canvas(str(SUB/'CAMPAIGN_PRESENTATION.pdf'),pagesize=(W,H),invariant=1)
c.setTitle(SPEC['title']+' / Presentation')
prs=Presentation();prs.slide_width=Inches(13.333333);prs.slide_height=Inches(7.5)


def ppt_text(sl,x,y,w,h,text,size,color,bold=False):
    tb=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=tb.text_frame;tf.word_wrap=True
    tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
    for i,line in enumerate(norm(text).split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line
        p.font.name='Arial';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color[1:])
        p.space_after=Pt(7 if size<25 else 1)
    return tb


for i,s in enumerate(slides):
    dark=(i in [0,8,18]);bg=INK if dark else PAPER;fg=PAPER if dark else INK
    c.setFillColor(colors.HexColor(bg));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(colors.HexColor(SIGNAL if dark else MUTED));c.setFont('Helvetica-Bold',10);c.drawString(40,H-36,norm(s['kicker']))
    has_art='art' in s or s.get('context');leftw=510 if has_art else 865
    title_size=43 if has_art else 49
    y=H-103
    for line in s['title'].split('\n'):
        c.setFillColor(colors.HexColor(fg));c.setFont('Helvetica-Bold',title_size);c.drawString(40,y,norm(line));y-=title_size*1.05
    y-=22
    for line in wrap(s['body'],'Helvetica',17,leftw):
        c.setFillColor(colors.HexColor(SIGNAL if dark else INK));c.setFont('Helvetica',17);c.drawString(40,y,line);y-=25
    if 'art' in s:
        image=ART/(s['art']+'.png')
        c.drawImage(str(image),590,115,width=326,height=330,preserveAspectRatio=True,anchor='c',mask='auto')
    if s.get('context'):draw_context(c,590,142,326,255)
    c.setStrokeColor(colors.HexColor(MUTED));c.line(40,77,W-40,77)
    for n,line in enumerate(wrap(s['note'],'Helvetica',8.5,W-95)):
        c.setFillColor(colors.HexColor(MUTED if not dark else PAPER));c.setFont('Helvetica',8.5);c.drawString(40,61-n*12,line)
    c.setFont('Helvetica-Bold',9);c.drawRightString(W-40,22,f'{i+1:02d} / {len(slides):02d}')
    c.showPage()
    sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=RGBColor.from_string(bg[1:])
    ppt_text(sl,.56,.32,12.2,.3,s['kicker'],10,SIGNAL if dark else MUTED,True)
    title_lines=s['title'].count('\n')+1
    ppt_text(sl,.56,1.0,7.3 if has_art else 12.2,title_lines*.66+.1,s['title'],title_size,fg,True)
    by=1.0+title_lines*.66+.4
    ppt_text(sl,.56,by,7.0 if has_art else 12.1,3.3,s['body'],17,SIGNAL if dark else INK)
    if 'art' in s:
        im=ART/(s['art']+'.png')
        doc=fitz.open(ART/(s['art']+'.pdf'));ratio=doc[0].rect.width/doc[0].rect.height
        maxw,maxh=4.4,4.5;ih=min(maxh,maxw/ratio);iw=ih*ratio
        sl.shapes.add_picture(str(im),Inches(8.2+(4.4-iw)/2),Inches(1.1+(4.5-ih)/2),width=Inches(iw),height=Inches(ih))
    if s.get('context'):
        buf=io.BytesIO();cc=canvas.Canvas(buf,pagesize=(326,255));draw_context(cc,0,0,326,255);cc.showPage();cc.save()
        img=fitz.open(stream=buf.getvalue(),filetype='pdf')[0].get_pixmap(matrix=fitz.Matrix(2,2)).tobytes('png')
        sl.shapes.add_picture(io.BytesIO(img), Inches(8.2), Inches(2), width=Inches(4.4))
    ppt_text(sl,.56,6.65,12.1,.65,s['note'],8.5,fg if dark else MUTED)
    sl.notes_slide.notes_text_frame.text=norm(s['note'])
c.save();prs.save(SUB/'CAMPAIGN_PRESENTATION.pptx')

# Deck preview: entirely self-contained apart from the local, supplied SVG assets.
sections=[]
for i,s in enumerate(slides):
    a=f'<img src="ARTWORK/{s["art"]}.svg" alt="{html.escape(s["title"])}">' if 'art' in s else ''
    sections.append(f'<section class="slide {"dark" if i in [0,8,18] else ""}"><div class="kicker">{html.escape(s["kicker"])}</div><div class="cols"><div><h1>{html.escape(s["title"]).replace(chr(10),"<br>")}</h1><p>{html.escape(s["body"]).replace(chr(10),"<br>")}</p></div>{a}</div><footer>{html.escape(s["note"])}<b>{i+1:02d} / {len(slides):02d}</b></footer></section>')
(SUB/'PRESENTATION.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>THIS SEAT HAS A HEAD. / Presentation</title><style>*{box-sizing:border-box}body{margin:0;background:#172C28;font-family:Arial,sans-serif;color:#172C28}.slide{background:#F2F0E5;min-height:100vh;padding:4vw;display:flex;flex-direction:column;scroll-snap-align:start;border-bottom:8px solid #172C28}.dark{background:#172C28;color:#F2F0E5}.kicker{font-size:13px;letter-spacing:.12em;color:#587167;font-weight:bold}.dark .kicker{color:#DEEF54}.cols{display:flex;align-items:center;gap:4vw;flex:1}.cols>div{flex:1}h1{font-size:clamp(32px,5vw,70px);line-height:1.02;letter-spacing:-.045em;margin:.5em 0}p{font-size:clamp(16px,1.65vw,24px);line-height:1.6}.cols img{width:32%;max-height:62vh;object-fit:contain}footer{font-size:12px;line-height:1.4;border-top:1px solid #587167;padding-top:12px;position:relative;padding-right:70px}footer b{position:absolute;right:0;top:12px}@media(max-width:650px){.cols{display:block}.cols img{width:70%;max-height:40vh}.slide{padding:6vw}footer{margin-top:25px}}@media print{.slide{height:100vh;break-after:page;border:0}}a{color:inherit}</style>'''+''.join(sections)+'</html>\n')

# A motion storyboard, not a claim of filmed or deployed creative.
(SUB/'MOTION_PROTOTYPE.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>This seat has a head / 15-second motion prototype</title><style>body{margin:0;background:#172C28;color:#F2F0E5;font:18px Arial;display:grid;place-items:center;min-height:100vh}.wrap{width:min(90vw,440px)}.frame{aspect-ratio:9/16;max-height:78vh;background:#F2F0E5;color:#172C28;padding:8%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center}h1{font-size:clamp(32px,7vw,56px);line-height:1.04}p{line-height:1.5}.badge{font-size:11px;letter-spacing:.1em}button{padding:12px 20px;background:#DEEF54;border:0;border-radius:4px;font-weight:bold;cursor:pointer;margin:14px 6px 0 0}.symbol{font-size:60px;font-weight:bold;color:#587167}small{display:block;font-size:12px;line-height:1.5;margin:10px 0}progress{width:100%;accent-color:#DEEF54}.card{background:#172C28;color:#F2F0E5;padding:20px;font-size:30px;font-weight:bold}.hidden{display:none}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}</style><div class="wrap"><div class="frame" aria-live="polite"><div class="badge">ILLUSTRATED STUDENT PROTOTYPE / NOT DEPLOYED</div><div class="symbol" id="symbol">01</div><h1 id="title">One bike.</h1><p id="caption">A parked two-wheeler. Engine off. No one has mounted.</p><div class="card hidden" id="card">THIS SEAT<br>HAS A HEAD.<br><span style="color:#DEEF54">YOURS.</span></div></div><progress id="progress" max="15" value="0" aria-label="Sequence progress"></progress><button id="play">Play 15 seconds</button><button id="pause">Pause</button><button id="next">Next frame</button><small>No sound. All meaning is captioned. No flashing or hearing/crash simulation. Manual frame navigation is available.</small></div><script>const scenes=[{at:0,title:'One bike.',caption:'A parked two-wheeler. Engine off. No one has mounted.',symbol:'01'},{at:3,title:'Two people.',caption:'The message rests on the second seat, with consent and supervision.',symbol:'02',card:true},{at:6,title:'Two helmets. Both fastened.',caption:'Each person needs their own suitable helmet, chinstrap fastened.',symbol:'02 / 02'},{at:10,title:'Check each other before you ride.',caption:'Facilitator collects the card before anyone mounts. Both helmets on. Both straps fastened.',symbol:'BEFORE'}];let timer=null,time=0;const show=()=>{let s=scenes.filter(s=>s.at<=time).at(-1);document.getElementById('title').textContent=s.title;document.getElementById('caption').textContent=s.caption;document.getElementById('symbol').textContent=s.symbol;document.getElementById('card').classList.toggle('hidden',!s.card);document.getElementById('progress').value=time};document.getElementById('pause').onclick=()=>{clearInterval(timer);timer=null};document.getElementById('play').onclick=()=>{clearInterval(timer);time=0;show();timer=setInterval(()=>{time=Math.min(15,time+.1);show();if(time>=15){clearInterval(timer);timer=null}},100)};document.getElementById('next').onclick=()=>{clearInterval(timer);timer=null;time=(scenes.find(s=>s.at>time)||scenes[0]).at;show()};show();</script></html>\n''')

# Blank instruments are honest planned fieldwork, not manufactured findings.
with (SUB/'PILOT_TALLY_TEMPLATE.csv').open('w',newline='') as f:
    csv.writer(f, lineterminator="\n").writerow(['window_baseline_or_campaign','aggregate_session_id','adult_paired_departures','both_helmets_and_visible_fastened_straps','one_or_more_helmets_absent','strap_or_helmet_observation_unknown','card_present_at_mounting_safety_incidents','notes_no_personal_data'])
with (SUB/'COMPREHENSION_TEMPLATE.csv').open('w',newline='') as f:
    csv.writer(f, lineterminator="\n").writerow(['anonymous_code','message_understood_verbatim','addressee_understood_verbatim','action_timing_understood_verbatim','discomfort_or_confusion_verbatim','unprompted_correct_message_yes_no_unknown','revision_needed'])

(SUB/'PRINT_AND_ACCESSIBILITY_NOTES.md').write_text('''# Print and accessibility notes

Tree: SUBMISSION | Status: design complete, not deployed | Fallback: false

- Seat card: 148 x 105 mm (A6 landscape), trim-size PDF and editable SVG. Print at 100%, no fit-to-page. Use 180-250 gsm matte card for the supervised reusable prototype. No attachment to vehicle or helmet. Collect before mounting. The PDF is a finished trim-size prototype, not a vendor-specific imposed/bleed-certified press file.
- Poster: 297 x 420 mm (A3 portrait). Print at 100%. Place only on a permissioned wall in the stationary preparation area, not on road signs or driving sightlines.
- Social: 1080 x 1920 PNG and SVG; PDF supplied for review. Use before riding. No live platform integration is claimed.
- SVGs contain editable vector shapes and live Arial/Helvetica/system text. Fonts may substitute; inspect before final vendor output. PDF fonts use standard Helvetica. No external artwork or font download is required.
- Text and paired symbols carry meaning without colour. Captioned prototype has no sound, flashing, automatic playback or required scan. Manual frame navigation is available. Alternative text is embedded in SVG title/description.
- Main palette: deep green #172C28; ivory #F2F0E5; signal #DEEF54. Small secondary text is for production labels, not the action instruction. Ask local participants whether additional-language executions are needed; only the English master is claimed here.
- Source citations and research qualifications are in the report and presentation, not compressed into the immediate-action card.
- All contextual images are illustrations, not deployment photographs. Nothing certifies equipment, guarantees protection, or implies government or brand sponsorship.
''')

# Machine checks: real binary formats, page counts, dimensions, copy and lexical scope.
checks=[]
for f in [SUB/'CAMPAIGN_REPORT.pdf',SUB/'CAMPAIGN_PRESENTATION.pdf']+list(ART.glob('*.pdf')):
    reader=PdfReader(f)
    checks.append({'file':str(f.relative_to(BASE)),'pages':len(reader.pages),'readable':True})
assert len(PdfReader(SUB/'CAMPAIGN_PRESENTATION.pdf').pages)==len(slides)
assert len(Presentation(SUB/'CAMPAIGN_PRESENTATION.pptx').slides)==len(slides)
for name in ['seat_card_A6','poster_A3','social_story_1080x1920']:
    assert all((ART/(name+ext)).is_file() for ext in ['.pdf','.png','.svg'])
for f in [ART/'seat_card_A6.pdf',ART/'poster_A3.pdf']:
    assert 'HELMET' in ''.join(p.extract_text() or '' for p in PdfReader(f).pages).upper()
forbidden=['QMDJ','Qimen','Dunjia','heaven stem','earth stem','day stem','hour stem','destiny','fortune-telling']
violations=[]
for f in SUB.rglob('*'):
    if f.suffix in ['.md','.html','.svg']:
        t=f.read_text().lower()
    elif f.suffix=='.pdf':
        t='\n'.join(p.extract_text() or '' for p in PdfReader(f).pages).lower()
    elif f.suffix=='.pptx':
        deck=Presentation(f);t='\n'.join(sh.text for sl in deck.slides for sh in sl.shapes if sh.has_text_frame).lower()
    else:continue
    for term in forbidden:
        if term.lower() in t:violations.append({'path':str(f.relative_to(BASE)),'term':term})
assert not violations,violations
budget=sum(x['amount'] for x in SPEC['budget_inr_estimates'])
assert budget==700
checks.append({'budget_total_inr':budget,'status':'arithmetic_verified_not_quotes'})
(BASE/'OPERATOR/build_checks.json').write_text(json.dumps({'status':'passed_for_listed_checks_only','checks':checks,'lexical_violations':violations,'cap_execution_claimed':False,'fieldwork_verified':False},indent=2)+'\n')
# One preview is sufficient for inspecting typography without generating large datasets.
doc=fitz.open(SUB/'CAMPAIGN_PRESENTATION.pdf')
doc[8].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(BASE/'OPERATOR/hero_slide_preview.png')
print(f'Built report, {len(slides)}-slide PDF/PPTX/HTML presentation, three PDF/SVG/PNG artworks, motion prototype and blank research instruments. Budget INR {budget}. Listed binary and lexical checks passed.')
