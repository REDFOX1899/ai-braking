import json,hashlib,zipfile,math
from pathlib import Path
import cadquery as cq
R=Path(__file__).resolve().parents[2];p=json.loads((R/'website/app/galvi-study.json').read_text());web=R/'website/public/products'/p['slug'];root=R/'engineering/products/AB-G315/C0'
assert len(p['dimensions'])==20
assert hashlib.sha256((R/'sources/raw/galvi'/ (p['source']['sha256']+'.pdf')).read_bytes()).hexdigest()==p['source']['sha256']
a=cq.importers.importStep(str(root/'parts/AB-G315-001/AB-G315-001.step')).val()
assert abs(a.Volume()-(762*220*20-4*math.pi*9**2*20))<.01
for x in [-341,99]:
 for y in [-40,40]:assert not a.isInside(cq.Vector(x,y,0))
assert a.isInside(cq.Vector(0,0,0))
assert 2*next(d['value'] for d in p['dimensions'] if d['symbol']=='H')==440
checks=json.loads((web/'geometry-checks.json').read_text());assert all(i['status']=='nonphysical reserved-volume overlap' for i in checks['intersections'])
assert all(x['valid_solid'] and x['step_volume_relative_error']<1e-6 for x in checks['parts'])
with zipfile.ZipFile(web/p['downloads']['zip']) as z:
 assert z.testzip() is None
 for f in json.loads(z.read('manifest.json')):assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256']
 assert 'galvi_study.py' in z.namelist()
assert (web/p['downloads']['pdf']).read_bytes().startswith(b'%PDF-')
print('PASS: source hash, 20 references, doubled H pitch, four physical bores, solid round-trips, classified envelope overlaps, ZIP checksums, PDF signature.')
