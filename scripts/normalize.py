#!/usr/bin/env python3
"""Extract page-addressable text, catalogue inventory and unreviewed numeric leads."""
import csv, hashlib, json, re
from pathlib import Path
from urllib.parse import urlsplit, unquote
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
def save(name,data): (ROOT/'research/normalized'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
def csvsave(name,rows,fields):
 with (ROOT/'research/normalized'/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def run():
 assets=[]; candidates=[]; products=[];seen=set()
 for manifest in sorted((ROOT/'research/normalized').glob('*-collection.json')):
  d=json.loads(manifest.read_text())
  for r in d['records']:
   if r.get('status')!=200 or not r.get('local_path'): continue
   r=dict(r);r['source_url']=r['url'];r['revision']=None
   r['redistribution']='private-reference-only'
   if r.get('format')=='html' and r.get('title'):
    products.append(dict(manufacturer=r['manufacturer'],title=r['title'],source_url=r['url'],sha256=r['sha256'],record_type='discovered page; product classification pending'))
   assets.append(r)
 for r in json.loads((ROOT/'research/normalized/galvi-import.json').read_text()):
  assets.append(dict(r,format=Path(r['local_path']).suffix[1:],revision=None,redistribution='private-reference-only'))
 for r in assets:
  if r.get('format')!='pdf' or r['sha256'] in seen:continue
  seen.add(r['sha256']);path=ROOT/r['local_path']
  target=ROOT/'sources/extracted'/r['manufacturer']/(r['sha256']+'.pages.json');target.parent.mkdir(parents=True,exist_ok=True)
  try:
   if target.exists():pages=json.loads(target.read_text())
   else:
    reader=PdfReader(path)
    pages=[{'pdf_page':i+1,'text':p.extract_text(extraction_mode='layout')} for i,p in enumerate(reader.pages)]
    target.write_text(json.dumps(pages,ensure_ascii=False,indent=2))
   r['page_count']=len(pages);r['page_text_path']=str(target.relative_to(ROOT));r['pdf_validation']='parsed'
   joined='\n'.join(p['text'] for p in pages[:3]+pages[-2:])
   rev=re.search(r'(?:Rev(?:ision)?[ .:]*)[A-Z0-9./-]+',joined,re.I)
   r['revision_candidate']=rev.group(0) if rev else None
   r['revision_status']='unreviewed candidate' if rev else 'not identified'
   for p in pages:
    lines=p['text'].splitlines()
    for i,line in enumerate(lines):
     if re.search(r'\b(?:torque|force|stroke|speed|pressure|temperature|diameter|moment|kraft|hub)\b',line,re.I) and re.search(r'\d',line) and re.search(r'N\s*m|kN|Nm|mm|bar|rpm|°|MPa|kW|daN|min.?1',line):
      candidates.append(dict(manufacturer=r['manufacturer'],asset_sha256=r['sha256'],source_url=r.get('source_url'),pdf_page=p['pdf_page'],raw_text=line.strip(),context='\n'.join(lines[max(0,i-2):i+3]),verification='unreviewed extraction; not a design input'))
  except Exception as e:r['pdf_validation']='error';r['extraction_error']=str(e)
 save('assets.json',assets);save('specification-candidates.json',candidates);save('discovered-pages.json',products)
 csvsave('asset-index.csv',assets,['manufacturer','source_url','format','filename','sha256','local_path','retrieved_at','revision','revision_candidate','revision_status','page_count','pdf_validation','redistribution'])
 csvsave('specification-candidates.csv',candidates,['manufacturer','asset_sha256','source_url','pdf_page','raw_text','context','verification'])
 csvsave('discovered-pages.csv',products,['manufacturer','title','source_url','sha256','record_type'])
 print(f'{len(assets)} asset references; {len(seen)} unique PDFs; {len(candidates)} unreviewed specification leads; {len(products)} page records')
if __name__=='__main__':run()
