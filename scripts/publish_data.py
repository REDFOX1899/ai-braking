#!/usr/bin/env python3
"""Explicit public allowlist: metadata and original work only; never raw competitor files."""
import csv,json,shutil,re,hashlib
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
R=Path(__file__).resolve().parents[1];N=R/'research/normalized';P=R/'website/public';P.mkdir(exist_ok=True)
INFO={
'galvi':('GALVI','https://www.galvi.com/','Shoe brakes, calipers, thrusters, hydraulics, rotating parts and buffers.','The supplied catalogue forms the initial family map. The live site adds accessible catalogues, but authenticated CAD and unavailable links remain gaps. Compare interface families and actuation options without assuming interchangeability.','NEWCOMEN / GALVI; company identity recorded in the supplied catalogue.'),
'dellner-bubenzer':('Dellner Bubenzer','https://www.dellnerbubenzer.com/products','Disc and drum brakes, hydraulics, couplings, monitoring and storm systems.','Use this range to benchmark system breadth and monitoring integration. CMB-3 provides a concrete fieldbus-monitoring reference; telemetry alone is not a unique proposition.','DELLNER BUBENZER is the current source brand; historical PINTSCH BUBENZER references should retain their original names.'),
'sibre':('SIBRE','https://www.sibre.de/downloads/','Drum and disc brakes, rail brakes, buffers, hydraulics and monitoring.','The download centre provides many dimensioned technical sheets. Keep model suffixes, air gaps and release-pressure conditions attached to each extracted value.','Siegerland-Bremsen GmbH, identified on the technical sheets.'),
'stromag':('Stromag','https://www.stromag.com/en/products/brake-solutions-category','Industrial service and emergency brakes, hydraulic/electromagnetic variants and monitoring.','The 200-page SIME industrial braking catalogue is a substantial reference despite direct product-page restrictions. Family overview maxima must not be assigned to every model.','Stromag / SIME product identity; official literature links to Regal Rexnord.'),
 'twiflex':('Twiflex','https://www.twiflex.com/products','Direct-acting and spring-applied disc calipers, couplings, hydraulics and locking systems.','The industrial disc-brake catalogue supports comparisons of actuation and force versus pressure. Check diagrams visually: at least one unit conversion is inconsistent in the source.','Twiflex official catalogue identifies Regal Rexnord; historical Altra labels remain in legacy documents.'),
'svendborg':('Svendborg Brakes','https://www.svendborg-brakes.com/products/','Hydraulic brakes, HPUs, controlled braking, friction parts, connectivity and storm systems.','This is a useful system-level benchmark for conveyors and heavy industry. Published controls and connectivity mean our advantage must be demonstrated through usability, service and measured outcomes.','Official catalogue identifies Svendborg Brakes as a Regal Rexnord brand.'),
'mondel':('Mondel','https://www.cmco.com/en-ae/products/power-and-motion-technology/brakes/brake-products/300m-mill-duty-brakes/','200S and 300M shoe brakes, brake wheels, controllers and service accessories.','Useful for AISE/AIST-oriented industrial and mill-duty research. Imperial dimensions and accessory tables need explicit units; some regional web routes are unavailable.','Mondel is presented within Magnetek products on Columbus McKinnon official sources.'),
'emg':('EMG','https://www.emg.elexis.group/solutions/safety-components','ELDRO and ELHY electrohydraulic thrusters, variants and brake controls.','Benchmark actuation performance, serviceability and factory testing. The vendor is also a potential buy-versus-build reference for early prototypes; family-level ratings need configuration confirmation.','EMG Automation GmbH on the elexis group official domain.')}
allassets=json.loads((N/'assets.json').read_text());specs=json.loads((N/'reviewed-specifications.json').read_text())
manufacturers=[];documents=[];allgaps=[]
for slug,(name,url,families,analysis,identity) in INFO.items():
 c=json.loads((N/f'{slug}-collection.json').read_text());rs=c['records'];fail=[r for r in rs if r.get('status')!=200]
 labels={a['url']:a['label'] for r in rs for a in r.get('links',[]) if a.get('label') and len(a['label'])>5}
 docs=[];seen=set()
 for a in allassets:
  if a['manufacturer']!=slug or a.get('format')!='pdf' or a['sha256'] in seen or a.get('bytes',0)==0 or a.get('valid_signature') is False:continue
  seen.add(a['sha256']);u=a.get('source_url') or a.get('url')
  if not u:continue
  title=labels.get(u) or unquote(Path(urlsplit(u).path).name) or a.get('filename','Catalogue')
  # Corporate/peripheral EMG downloads are not promoted as brake references.
  context_only=slug=='emg' and not re.search('eldro|elhy|sicherheits|brak',u,re.I)
  doc=dict(id=a['sha256'][:16],manufacturer=slug,title=title,source_url=u,format='PDF',page_count=a.get('page_count'),revision=a.get('revision'),source_sha256=a['sha256'],scope='corporate context' if context_only else 'catalogue reference',retrieved_at=a.get('retrieved_at'),verification='archived; specifications require review')
  docs.append(doc)
 documents+=docs
 gaps=[{'url':r['url'],'reason':str(r.get('status'))+(' '+r['error'] if r.get('error') else '')} for r in fail]+c.get('unfetched',[])
 allgaps.extend([dict(x,manufacturer=slug) for x in gaps])
 entry=dict(id=slug,name=name,url=url,families=families,analysis=analysis,identity=identity,pages=sum(r.get('format')=='html' for r in rs),pdfs=len(docs),gaps=len(gaps),reviewed_facts=sum(s['manufacturer']==slug for s in specs),coverage='First collection; gaps recorded')
 manufacturers.append(entry)
 lines=[f'# {name} collection report','',f"Official entry: [{name}]({url})",'',identity,'',f'## Product families\n\n{families}','',f'## Our interpretation\n\n{analysis}','',f"## Collection coverage\n\n{entry['pages']} HTML responses; {entry['pdfs']} distinct PDF hashes; {len(gaps)} failed or deferred URLs. These are collection counts, not products or market shares.",'','Document revisions are only confirmed in reviewed specification records where identified. Other revisions remain unknown or unreviewed candidates. Public availability does not establish current orderability.','', '## Retrieved documents','']
 lines += [f"- [{x['title']}]({x['source_url']}) — SHA-256 `{x['source_sha256']}`, {x['page_count'] or 'unknown'} pages; {x['scope']}." for x in docs]
 lines += ['','## Gaps and deferred collection','']+[f"- {x['url']} — {x.get('reason','not fetched')}" for x in gaps]
 lines += ['','## Next review','', 'Reconcile the downloaded catalogues against current product pages; confirm revisions and missing CAD through legitimate manufacturer access. Validate every configuration-specific value before engineering use.']
 (R/f'research/reports/{slug}.md').write_text('\n'.join(lines))
(N/'manufacturers.json').write_text(json.dumps(manufacturers,indent=2));(N/'documents.json').write_text(json.dumps(documents,indent=2));(N/'collection-gaps.json').write_text(json.dumps(allgaps,indent=2))
portfolio=json.loads((R/'engineering/portfolio.json').read_text())
public=dict(release='2026-09-07',domain='braking.fde.guru',manufacturers=manufacturers,documents=[d for d in documents if d['scope']=='catalogue reference'],specifications=specs,portfolio=portfolio,counts=dict(manufacturers=8,unique_pdfs=len({a['sha256'] for a in allassets if a.get('format')=='pdf' and a.get('bytes',0)>0 and a.get('valid_signature') is not False}),reviewed_facts=len(specs),unreviewed_leads=len(json.loads((N/'specification-candidates.json').read_text())),gaps=len(allgaps)))
(P/'research.json').write_text(json.dumps(public,ensure_ascii=False))
(R/'website/app/research-data.json').write_text(json.dumps(public,ensure_ascii=False))
# Only named original reports and selected factual exports are published.
exports={'engineering-handbook.md':'engineering/ENGINEERING-HANDBOOK.md','supplier-requirements.csv':'engineering/SUPPLIER-REQUIREMENTS.csv','requirements-template.csv':'engineering/REQUIREMENTS-TEMPLATE.csv','product-portfolio.md':'reports/PRODUCT-PORTFOLIO.md','programme-and-budget.md':'reports/PROGRAMME-AND-BUDGET.md','research-method.md':'reports/RESEARCH-METHOD.md','domain-handoff.md':'reports/PUBLICATION-AND-DOMAIN.md','reviewed-specifications.csv':'research/normalized/reviewed-specifications.csv','portfolio.csv':'engineering/portfolio.csv'}
(P/'downloads').mkdir(exist_ok=True)
for target,source in exports.items():shutil.copyfile(R/source,P/'downloads'/target)
shutil.copyfile(R/'output/pdf/ai-braking-engineering-handbook.pdf',P/'downloads/engineering-handbook.pdf')
shutil.copyfile(R/'build-logs/2026-09-07.md',P/'downloads/build-log-2026-09-07.md')
for m in manufacturers:shutil.copyfile(R/f"research/reports/{m['id']}.md",P/'downloads'/f"collection-{m['id']}.md")
# Artifact allowlist records all approved output bytes, not entire repository directories.
expected=['favicon.svg','research.json']+['downloads/'+k for k in exports]+['downloads/engineering-handbook.pdf','downloads/build-log-2026-09-07.md']+['downloads/collection-'+m['id']+'.md' for m in manufacturers]
allowed=[dict(path=rel,sha256=hashlib.sha256((P/rel).read_bytes()).hexdigest()) for rel in expected]
(R/'reports/public-export-manifest.json').write_text(json.dumps(allowed,indent=2))
print(json.dumps(public['counts']))
