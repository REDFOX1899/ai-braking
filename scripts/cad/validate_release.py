"""Checks release consistency; never claims engineering approval."""
from pathlib import Path
import json,zipfile,hashlib,math
R=Path(__file__).resolve().parents[2];data=json.loads((R/'website/app/products-data.json').read_text());errors=[];count=0
assert len(data)==12
for p in data:
 root=R/'engineering/products'/p['code']/'C0';web=R/'website/public/products'/p['slug'];checks=json.loads((root/'geometry-checks.json').read_text());mesh=json.loads((web/'mesh.json').read_text())
 assert len(mesh)==len(p['parts'])==len(checks['parts'])
 assert {x['id'] for x in mesh}=={x['id'] for x in p['parts']}
 for m in mesh:
  assert len(m['vertices'])%3==0 and len(m['triangles'])%3==0
  assert all(math.isfinite(x) for x in m['vertices']) and max(m['triangles'])<len(m['vertices'])//3
 for a in checks['parts']:assert a['valid_solid'] and a['step_volume_relative_error']<1e-6
 for part in p['parts']:
  count+=1;d=web/'parts'/part['id'];assert (d/(part['id']+'.step')).read_bytes().startswith(b'ISO-10303-21');assert '<svg' in (d/(part['id']+'.svg')).read_text()
 assert (web/p['downloads']['pdf']).read_bytes().startswith(b'%PDF-')
 assert (web/p['downloads']['step']).read_bytes().startswith(b'ISO-10303-21')
 with zipfile.ZipFile(web/p['downloads']['zip']) as z:
  assert z.testzip() is None
  manifest=json.loads(z.read('manifest.json'))
  for f in manifest:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256']
 for f in web.rglob('*'):
  if f.is_file():assert f.stat().st_size<25*1024*1024
 assert 'not' in (web/'README.md').read_text().lower()
# Independent numerical sanity checks of the study formula outputs.
assert abs(500/(.3*.1575)/1000-10.582010582)<1e-6
assert abs(1000/(2*.3*.155)/1000-10.752688172)<1e-6
report={'products':len(data),'component_instances':count,'positive_volume_intersections':sum(len(p['intersections']) for p in data),'checks':['BOM/mesh/part identity','Finite indexed triangle meshes','CAD validity and STEP round-trip evidence','STEP/PDF signatures','ZIP CRC and SHA256 manifests','Per-asset hosting size','Study arithmetic'],'engineering_validation':'NOT performed: no FEA, solved motion, physical tests or production release','errors':errors}
(R/'reports/C0-release-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
