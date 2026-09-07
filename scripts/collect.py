#!/usr/bin/env python3
"""Bounded, resumable collection from official product sites. No logins or form submissions."""
import concurrent.futures, hashlib, json, re, time, zipfile
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urldefrag, unquote
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).isoformat()
UA = 'AI-Braking-Research/1.0 (public engineering reference collection)'
CONFIG = {
 'galvi': ['http://www.galvi.com/index'] + [f'http://www.galvi.com/moduli/catalogo/schedatecnica/{i}' for i in range(1,38)],
 'dellner-bubenzer': ['https://www.dellnerbubenzer.com/products','https://www.dellnerbubenzer.com/downloads'],
 'sibre': ['https://www.sibre.de/en/','https://www.sibre.de/downloads/'],
 'stromag': ['https://www.stromag.com/en/products/brake-solutions-category','https://www.stromag.com/-/media/Project/Altramotion/shared/files/Literature/brand/stromag/catalogs/mcc-p-8518-sg-en-a4-web.pdf?rev=d1104cc1554a466487df155561b85270'],
 'twiflex': ['https://www.twiflex.com/products','https://www.twiflex.com/literature','https://www.twiflex.com/-/media/project/altramotion/shared/files/literature/brand/twiflex-limited/catalogs/p-1648-tf.pdf?rev=920b53b1879149a08c1962382d264058'],
 'svendborg': ['https://www.svendborg-brakes.com/products/','https://svendborg-brakes.com/media/enuo1zu4/product-catalogue.pdf','https://www.svendborg-brakes.com/media/jihl2vom/superior-braking-solutions_svendborg-brakes.pdf'],
 'mondel': ['https://www.cmco.com/en-us/products/power-and-motion-technology/brakes/brake-accessories/mondel-brake-wheels/','https://www.cmco.com/globalassets/industries/marine-terminal--port/mh1156_marine-terminal-brochure.pdf'],
 'emg': ['https://www.emg.elexis.group/solutions/safety-components','https://www.emg.elexis.group/fileadmin/user_upload/emg/Sicherheitskomponenten/EMG-ELDRO/EMG-ELDRO-Neue-Generation/20250314_ELDRO_Uebersicht_A-Baureihe_EN.pdf']
}
ASSET = re.compile(r'\.(pdf|step|stp|iges|igs|dwg|dxf|zip)(?:$|\?)',re.I)
RELEVANT = re.compile(r'product|brak|brems|catalog|literature|download|thruster|eldro|elhy|safety-component|sicherheitskomponent|coupling|buffer|hydraulic',re.I)
EXCLUDE = re.compile(r'login|register|cart|checkout|contact|privacy|imprint|career|news|search|distributor|youtube|linkedin',re.I)

def sha(data): return hashlib.sha256(data).hexdigest()
def write_json(path, data):
 path.parent.mkdir(parents=True,exist_ok=True)
 temp=path.with_suffix('.tmp'); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)); temp.replace(path)

def audit_galvi():
 records=[]
 for archive in sorted((ROOT/'galvi_all_products').glob('*.zip')):
  with zipfile.ZipFile(archive) as z:
   bad=z.testzip()
   info=next((z.read(n).decode('utf-8',errors='replace') for n in z.namelist() if n.endswith('INFO.txt')),'')
   match=re.search(r'Source:\s*(\S+)',info)
   source=match.group(1) if match else None
   for n in z.namelist():
    if n.endswith('/'): continue
    data=z.read(n); digest=sha(data)
    suffix=Path(n).suffix.lower()
    valid=not (suffix=='.pdf' and not data.startswith(b'%PDF-'))
    dest=ROOT/'sources/raw/galvi-import'/f'{digest}{suffix}'
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(data)
    records.append(dict(manufacturer='galvi',product=archive.stem,filename=n,archive=str(archive.relative_to(ROOT)),source_url=source,asset_url=None,retrieved_at=None,imported_at=NOW,sha256=digest,bytes=len(data),local_path=str(dest.relative_to(ROOT)),valid_signature=valid,zip_crc_valid=bad is None,provenance='user-provided archive; original retrieval date and individual asset URLs unverified'))
 write_json(ROOT/'research/normalized/galvi-import.json',records)
 print('GALVI archive audit:',len(records),'members',flush=True)

def collect(name,seeds):
 out=ROOT/'research/normalized'/f'{name}-collection.json'
 previous=json.loads(out.read_text()) if out.exists() else {}
 records=previous.get('records',[])
 seen={r['url'] for r in records}
 queue=deque((u,0,'seed') for u in seeds)
 domains={urlsplit(u).hostname.removeprefix('www.') for u in seeds}
 s=requests.Session(); s.headers['User-Agent']=UA
 robots={}; discovered={}; page_count=0; asset_count=0
 def allowed(u):
  p=urlsplit(u); origin=f'{p.scheme}://{p.netloc}'
  if origin not in robots:
   try:
    r=s.get(origin+'/robots.txt',timeout=15)
    parser=RobotFileParser(); parser.parse(r.text.splitlines() if r.status_code==200 else [])
    robots[origin]=(parser,r.status_code)
   except requests.RequestException: robots[origin]=(None,'unavailable')
  parser,status=robots[origin]
  return parser is None or parser.can_fetch(UA,u)
 while queue:
  u,depth,parent=queue.popleft(); u=urldefrag(u)[0]
  if u in seen: continue
  is_asset=bool(ASSET.search(u))
  if (is_asset and asset_count>=120) or (not is_asset and page_count>=75):
   discovered[u]={'url':u,'parent':parent,'reason':'collection batch limit'}; continue
  seen.add(u)
  rec=dict(manufacturer=name,url=u,parent_url=parent,retrieved_at=datetime.now(timezone.utc).isoformat(),depth=depth)
  try:
   if not allowed(u):
    rec['status']='robots_disallowed'; records.append(rec); continue
   time.sleep(.15)
   r=s.get(u,timeout=(10,25),stream=True)
   rec.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('content-type',''))
   if r.status_code!=200:
    r.close(); records.append(rec); continue
   buf=bytearray()
   for chunk in r.iter_content(65536):
    buf.extend(chunk)
    if len(buf)>35*1024*1024: raise ValueError('asset exceeds 35 MiB limit')
   data=bytes(buf); r.close()
   if data.startswith(b'%PDF-'): suffix='.pdf'; asset_count+=1
   elif data.startswith(b'PK\x03\x04'): suffix='.zip';asset_count+=1
   elif 'html' in rec['content_type'] or b'<html' in data[:2000].lower():suffix='.html';page_count+=1
   else:suffix=Path(urlsplit(u).path).suffix.lower() or '.bin';asset_count+=1
   rec['expected_asset_valid']=not is_asset or suffix!='.html'
   rec.update(sha256=sha(data),bytes=len(data),format=suffix[1:])
   dest=ROOT/'sources/raw'/name/(rec['sha256']+suffix)
   dest.parent.mkdir(parents=True,exist_ok=True)
   if not dest.exists():dest.write_bytes(data)
   rec['local_path']=str(dest.relative_to(ROOT))
   if suffix=='.html':
    soup=BeautifulSoup(data,'html.parser')
    rec['title']=soup.title.get_text(' ',strip=True) if soup.title else ''
    main=soup.find('main') or soup.find('div',class_='corpo-princ') or soup.body or soup
    links=[]
    for a in soup.select('a[href]'):
     link=urljoin(r.url,a['href'].strip()); lp=urlsplit(link)
     if lp.scheme not in ('http','https'):continue
     label=a.get_text(' ',strip=True)
     asset=bool(ASSET.search(link))
     same=(lp.hostname or '').removeprefix('www.') in domains
     if 'altraliterature.com' in (lp.hostname or '') and not asset:
      same = same and ('/brand/'+('twiflex-limited' if name=='twiflex' else name)+'/') in link
     if name=='mondel' and not asset: same = same and ('/brake' in link or 'mondel' in link)
     # External documents are accepted only when directly linked from an official page.
     if asset or (same and RELEVANT.search(link+' '+label) and not EXCLUDE.search(link)):
      links.append({'url':link,'label':label,'kind':'asset' if asset else 'page'})
      if asset or depth<3:queue.append((link,depth+1,r.url))
      else:discovered[link]={'url':link,'parent':r.url,'reason':'depth limit'}
    rec['links']=links
    for tag in main(['script','style','nav','footer','header']):tag.decompose()
    txt=main.get_text('\n',strip=True)
    target=ROOT/'sources/extracted'/name/(rec['sha256']+'.txt');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(txt)
    rec['text_path']=str(target.relative_to(ROOT))
   records.append(rec)
  except Exception as e:
   rec.update(status='error',error=str(e));records.append(rec)
  write_json(out,dict(manufacturer=name,started_at=NOW,limits={'html_pages':75,'assets':120,'depth':3,'max_asset_mib':35},records=records,unfetched=list(discovered.values()),robots={k:v[1] for k,v in robots.items()}))
  if len(records)%15==0:print(name,len(records),'requests',flush=True)
 write_json(out,dict(manufacturer=name,started_at=NOW,limits={'html_pages':75,'assets':120,'depth':3,'max_asset_mib':35},records=records,unfetched=[v for k,v in discovered.items() if k not in seen],robots={k:v[1] for k,v in robots.items()}))
 print(name,'finished',len(records),'records',flush=True)

if __name__=='__main__':
 audit_galvi()
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  list(pool.map(lambda p:collect(*p),CONFIG.items()))
