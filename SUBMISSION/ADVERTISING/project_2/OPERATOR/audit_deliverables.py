#!/usr/bin/env python3
"""Bounded real-file checks. Does not certify formal charter or empirical results."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from html.parser import HTMLParser
from xml.etree import ElementTree

import fitz
from PIL import Image
from pptx import Presentation

BASE=Path(__file__).resolve().parents[1]
SUB=BASE/'SUBMISSION'
issues=[];checks=[]

for p in sorted(SUB.rglob('*.pdf')):
 d=fitz.open(p)
 for i,page in enumerate(d):
  for b in page.get_text('blocks'):
   if b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1:
    issues.append({'path':str(p.relative_to(BASE)),'page':i+1,'problem':'text_outside_page','sample':b[4][:100]})
 checks.append({'file':str(p.relative_to(BASE)),'pages':len(d),'parseable':True})
assert len(fitz.open(SUB/'CAMPAIGN_PRESENTATION.pdf'))==19
assert len(Presentation(SUB/'CAMPAIGN_PRESENTATION.pptx').slides)==19
for p in SUB.rglob('*.svg'):ElementTree.parse(p)
for p in SUB.rglob('*.png'):
 with Image.open(p) as im:
  im.verify()
with Image.open(SUB/'ARTWORK/social_story_1080x1920.png') as im:assert im.size==(1080,1920)
with fitz.open(SUB/'ARTWORK/seat_card_A6.pdf') as d:
 assert abs(d[0].rect.width-148*72/25.4)<.1
 assert abs(d[0].rect.height-105*72/25.4)<.1
with fitz.open(SUB/'ARTWORK/poster_A3.pdf') as d:
 assert abs(d[0].rect.width-297*72/25.4)<.2
 assert abs(d[0].rect.height-420*72/25.4)<.2

class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v and not v.startswith(('https:','http:','#','data:')):self.refs.append(v)
for p in SUB.glob('*.html'):
 parser=Links();parser.feed(p.read_text())
 for ref in parser.refs:
  if not (p.parent/ref).is_file():issues.append({'file':str(p),'broken_local_link':ref})

terms=['QMDJ','Qimen','Dunjia','奇门','遁甲','天盘','地盘','人盘','神盘','九星','八门','八神','值符','值使','旬空','空亡','马星','入墓','击刑','门迫','反吟','伏吟','天乙','阳遁','阴遁','节气','用神','heaven stem','earth stem','day stem','hour stem','the day palace','the hour palace','chart-reading slang','transliterated technical label','Chinese metaphysical technical term']
for tree in ['SUBMISSION','ANNOTATED']:
 for p in (BASE/tree).rglob('*'):
  if p.suffix in ['.md','.html','.svg']:t=p.read_text()
  elif p.suffix=='.pdf':t='\n'.join(pg.get_text() for pg in fitz.open(p))
  elif p.suffix=='.pptx':t='\n'.join(sh.text for sl in Presentation(p).slides for sh in sl.shapes if sh.has_text_frame)
  else:continue
  for term in terms:
   if term.casefold() in t.casefold():issues.append({'file':str(p.relative_to(BASE)),'forbidden_term':term})
# Narrative check excluding the declared technical appendix.
text=(BASE/'LAYER_A/DECISION_AND_AUDIT.md').read_text().split('### Technical appendix:')[0]
for term in terms:
 if term.casefold() in text.casefold():issues.append({'file':'LAYER_A narrative','forbidden_term':term})

r=json.loads((BASE/'OPERATOR/design_requirement_map.json').read_text())['requirements']
assert len(r)==17 and len({x['id'] for x in r})==17
assert all(re.fullmatch(r'REQ-\d{3}',x['id']) for x in r)
assert all(x['formal_charter_coverage_certified'] is False for x in r)
assert len(list(__import__('csv').reader((SUB/'COMPREHENSION_TEMPLATE.csv').open())))==1
assert len(list(__import__('csv').reader((SUB/'PILOT_TALLY_TEMPLATE.csv').open())))==1
# Validate source JSON syntax without ever opening the raw chart.
for p in (BASE/'OPERATOR').glob('*.json'):json.loads(p.read_text())
assert not issues,issues
result={'status':'passed_for_listed_checks_only','checks':checks,'additional_checks':['19 PDF/PPTX slides','SVG XML parses','PNG integrity and social dimensions','A6/A3 page dimensions','all local HTML links resolve','full declared lexical term list in public and annotated trees','17 unique design-facet records','research instruments contain headers only'],'issues':issues,'not_verified':['real browser playback','full semantic-lint harness','formal charter guards','equipment safety certification','permissions','audience response','campaign effectiveness','exhaustive originality']}
(BASE/'OPERATOR/final_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: PDF bounds, real binary formats, artwork sizes, local links, lexical scopes, unique brief facets and blank research instruments. Formal/empirical limits retained.')
