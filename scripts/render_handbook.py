#!/usr/bin/env python3
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
R=Path(__file__).resolve().parents[1];out=R/'output/pdf/ai-braking-engineering-handbook.pdf';out.parent.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=10,leading=15,spaceAfter=9,textColor=colors.HexColor('#273d3b')))
styles.add(ParagraphStyle(name='CellCustom',fontName='Helvetica',fontSize=8,leading=11,spaceAfter=2))
styles['Heading1'].textColor=colors.HexColor('#164d49');styles['Heading1'].spaceBefore=18;styles['Heading1'].keepWithNext=True;styles['Heading1'].allowOrphans=0
styles['Title'].textColor=colors.HexColor('#164d49');styles['Title'].fontSize=27;styles['Title'].leading=32

def markup(t):
 t=escape(t)
 t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{m[2]}" color="#16685c">{m[1]}</link>',t)
 t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
 return t.replace('→',' / ').replace('…','...').replace('–','-').replace('—','-')
lines=(R/'engineering/ENGINEERING-HANDBOOK.md').read_text().splitlines();flow=[];i=0
while i<len(lines):
 line=lines[i]
 if line.startswith('|'):
  table=[]
  while i<len(lines) and lines[i].startswith('|'):
   vals=[v.strip() for v in lines[i].strip('|').split('|')]
   if not all(re.fullmatch(r'[-: ]+',v) for v in vals):table.append([Paragraph(markup(v),styles['CellCustom']) for v in vals])
   i+=1
  widths=[110,155,230] if len(table[0])==3 else [495/len(table[0])]*len(table[0])
  tb=Table(table,colWidths=widths,repeatRows=1,hAlign='LEFT')
  tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e4efea')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#cbd8d3')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
  flow.extend([tb,Spacer(1,12)]);continue
 if line.startswith('# '):flow.append(Paragraph(markup(line[2:]),styles['Title']))
 elif line.startswith('## '):flow.append(Paragraph(markup(line[3:]),styles['Heading1']))
 elif line.strip():flow.append(Paragraph(markup(line),styles['BodyCustom']))
 i+=1

def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#cbd8d3'));c.line(50, forty:=40,545,forty)
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#536463'));c.drawString(50,28,'AI BRAKING  /  CONCEPT - ENGINEER REVIEW REQUIRED  /  REV 0.1');c.drawRightString(545,28,str(doc.page))
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=50,rightMargin=50,topMargin=45,bottomMargin=55,title='AI Braking Engineering Handbook',author='AI Braking').build(flow,onFirstPage=footer,onLaterPages=footer)
print(out)
