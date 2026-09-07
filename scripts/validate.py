#!/usr/bin/env python3
"""Integrity and publication-boundary checks. Does not validate brake engineering."""
import hashlib,json,zipfile,csv
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];N=R/'research/normalized';errors=[];warnings=[]
assets=json.loads((N/'assets.json').read_text());seen=set()
for a in assets:
 p=R/a['local_path'];digest=a['sha256']
 if digest in seen:continue
 seen.add(digest)
 if not p.is_file():errors.append('missing '+str(p));continue
 b=p.read_bytes()
 if hashlib.sha256(b).hexdigest()!=digest:errors.append('hash mismatch '+str(p))
 if a.get('format')=='pdf' and not b.startswith(b'%PDF-'):
  if a.get('valid_signature') is False:warnings.append('Known invalid supplied PDF retained for provenance: '+str(p))
  else:errors.append('invalid PDF signature '+str(p))
for p in (R/'galvi_all_products').glob('*.zip'):
 with zipfile.ZipFile(p) as z:
  if z.testzip():errors.append('ZIP CRC failure '+p.name)
specs=json.loads((N/'reviewed-specifications.json').read_text());m=json.loads((N/'manufacturers.json').read_text())
if len(m)!=8 or len(specs)!=24:errors.append('Unexpected manufacturer/specification count')
for s in specs:
 if not s['conditions'] or not s['unit'] or not s['source_url']:errors.append('Missing reviewed fact provenance '+s['id'])
 if s['source_sha256'] not in seen:errors.append('Fact source missing '+s['id'])
 if s['engineering_approval']!='not approved as design input':errors.append('Unexpected engineering approval')
 if s['pdf_page']:
  paths=list((R/'sources/extracted'/s['manufacturer']).glob(s['source_sha256']+'.pages.json'))
  if not paths or s['pdf_page']>len(json.loads(paths[0].read_text())):errors.append('Invalid source page '+s['id'])
public=json.loads((R/'website/public/research.json').read_text())
if len(public['portfolio'])!=12 or any(p['maturity']!='concept' for p in public['portfolio']):errors.append('Invalid portfolio maturity')
manifest=json.loads((R/'reports/public-export-manifest.json').read_text());allowed={x['path']:x['sha256'] for x in manifest}
for p in (R/'website/public').rglob('*'):
 if not p.is_file():continue
 rel=str(p.relative_to(R/'website/public'))
 if rel not in allowed or hashlib.sha256(p.read_bytes()).hexdigest()!=allowed.get(rel):errors.append('Unexpected public bytes '+rel)
 if any(x in rel.lower() for x in ['sources/','session-transcript','galvi_all_products','.env','supplier-confidential']):errors.append('Private path published '+rel)
 if p.suffix=='.pdf' and p.name!='engineering-handbook.pdf':errors.append('Unapproved PDF publication '+rel)
 if p.suffix not in ['.pdf','.png','.jpg']:
  txt=p.read_text(errors='replace')
  if any(x in txt for x in ['ghp_','github_pat_','BEGIN PRIVATE KEY','braking.fd.guru']):errors.append('Sensitive/stale content '+rel)
for path in ['engineering-handbook.pdf','product-portfolio.md','programme-and-budget.md','supplier-requirements.csv','requirements-template.csv','research-method.md','reviewed-specifications.csv','domain-handoff.md','build-log-2026-09-07.md']:
 if not (R/'website/public/downloads'/path).is_file():errors.append('Missing download '+path)
counts=dict(unique_archived_files=len(seen),valid_unique_pdfs=public['counts']['unique_pdfs'],manufacturers=len(m),source_checked_facts=len(specs),unreviewed_leads=public['counts']['unreviewed_leads'])
report=dict(checks='Archive hashes, ZIP CRC, PDF signatures, fact provenance/page bounds, publication allowlist and required downloads',counts=counts,errors=errors,warnings=warnings,engineering_validation='not performed',webmcp_validation='No supported WebMCP validation context available; tool contract not runtime-verified',browser_visual_testing='not requested; not performed')
(R/'reports/validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
