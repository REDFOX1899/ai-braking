"""GALVI-referenced interface study; NOT vendor CAD or production design."""
import sys,json,math,hashlib,shutil,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import build_models as m
R=m.R;code='AB-G315'
source='https://drfmxgbd0lt74.cloudfront.net/PDF/Cataloghi/GALVI_Shoe%20Brakes.pdf'
dims=[('A','Drum diameter',315,4),('B','Brake axis height above mounting plane',230,4),('D','Brake base length',722,4),('E','Left base edge to drum axis',240,4),('F','Drum axis to right base edge',482,4),('H','Mounting-hole half-pitch from drum axis',220,4),('I','Mounting-hole transverse pitch',80,4),('M','Four brake mounting holes',18,4),('Cmax','Brake maximum height',595,4),('Gmax','Brake maximum length',784,4),('T','Standard shoe width',110,4),('PD-A','PD.315 outer diameter',315,15),('PD-B','PD.315 dimension B',133,15),('PD-B1','PD.315 friction-band width B1',118,15),('PD-C','PD.315 overall axial length',153,15),('PD-D','PD.315 hub outside diameter',130,15),('PD-E','PD.315 coupling-hole pitch circle',200,15),('PD-F','PD.315 machined coupling-hole diameter',50,15),('PD-X','PD.315 coupling-hole count',6,15),('PD-Rmax','PD.315 maximum finished shaft bore',80,15)]
brief=dict(slug='galvi-315-reference',short='GALVI 315 interface study',subtitle='A defined basis for the partnership conversation',level='Published-interface study',priority=0,description='Original integration geometry referencing GALVI N.315.HYD.030/05 and PD.315 catalogue dimensions. This is not a GALVI manufacturing model or verified replacement. Purchased brake internals, load paths and shaft locking are not released.',targets=[['Drum outside diameter','315 mm','GALVI PD.315; PDF page 15'],['Brake axis height','230 mm','GALVI N.315; PDF page 4'],['Four mounting holes','Ø18; 440 × 80 mm pitch','GALVI N.315; PDF page 4'],['Drum band width','118 mm','GALVI PD.315 B1; PDF page 15'],['Finished bore selected','50 mm nominal','Our selection within published R max 80; shaft requirement pending']],decisions=['Buy or partner for the complete brake and actuator; focus our first integration effort on the mounting and drum/shaft interface.','Use published dimensions for external interfaces only. Keep proposed section thickness and shaft selection visibly separate.','Request a current GALVI drawing before establishing compatibility or manufacturing release.'],materials=['GALVI publishes EN-GJL-250 and EN-GJS-500-7 drum variants; neither is selected for production here.','Our adapter plate: S355J2+N candidate, 20 mm illustrative thickness; no strength or bolt-joint approval.'],risks=['Catalogue revision February 2016; current availability and dimensions unconfirmed.','Drum wall/web geometry is an original simplification, not published manufacturing geometry.','Brake envelope contains no levers, shoes, springs or actuation mechanism; do not manufacture it.','No verified shaft connection, preload, tolerances, thermal capacity or operating rating.'],steps=['Confirm source revision and purchased brake option with supplier.','Inspect 440 x 80 four-hole pattern and datum plane on proposed adapter.','Place the brake so its drum axis is 230 mm above its mounting plane.','Confirm PD.315 axial position and shaft attachment from machine and supplier drawings.','Approve detailed joints, load paths and guarded test plan before prototype manufacture.'],validation=['Check supplier CAD and physical first article against the published interface.','Size adapter, foundation, shaft connection and drum for approved duty.','Perform independent dimensional, torque, thermal and endurance validation.'],hypotheses=[['First-build scope','Partner for the brake mechanism','Validate purchasing and integration economics with supplier quotations.'],['Traceability','Every key interface has a source','Confirm against current controlled vendor drawings before release.']],sensors=['Request thruster supply/duty, position-switch options, wear sensing, connector and machine-safe-state requirements.'])
def model():
 # Mounting origin X=drum axis, Y=shaft axis, Z=adapter top.
 m.add('Our mounting adapter concept',m.plate(762,220,20,[(-341,-40),(99,-40),(-341,40),(99,40)],18),(121,0,-10),notes=['4 x Ø18 THRU. Assembly X +/-220, Y +/-40; part-local X -341/+99, Y +/-40. Full pitch 440 x 80.','Plate 762 x 220 x 20 is our proposal; foundation holes, strength and flatness unapproved.'],explode=[0,0,-90])
 # Transparent envelope rendered separately, not a claimed mechanism.
 m.add('Purchased brake installation envelope',m.box(784,200,595), (148,0,297.5),material=m.BUY,process='Buy complete brake; replace this envelope with current vendor STEP',notes=['Published maximum extents O/P: X -244 / +540; height C=595.','200 mm transverse envelope is our assumed display width; actual full width requires vendor CAD.','Volume is reserved space, not a physical solid to manufacture.'],role='interface-envelope',explode=[250,0,100])
 # Separate integral drum concept. Internal wall & web explicitly assumed.
 drum=m.ring(315,275,118).translate((0,0,74)).union(m.ring(315,50,15).translate((0,0,7.5))).union(m.ring(130,50,153).translate((0,0,76.5)))
 for i in range(6):drum=drum.cut(m.cyl(50,19).translate((100*math.cos(i*math.pi/3),100*math.sin(i*math.pi/3),7.5)))
 m.add('PD.315-referenced drum concept',drum.rotate((0,0,0),(1,0,0),90),(0,76.5,230),material='GALVI material options: EN-GJL-250 / EN-GJS-500-7; selection pending',process='Supplier-controlled drum preferred; our simplified CAD for interface review only',notes=['Published: OD 315, band 118, overall length 153, hub OD 130, 6 x Ø50 on PCD200.','Our choices: shaft bore 50, rim inner diameter 275, 15 mm flat web. Internal section is NOT GALVI geometry.','Coupling holes are pin interfaces, not six mounting-bolt holes. No speed or torque rating transferred.'],role='reference-concept',explode=[0,-190,0])
 for x in [-220,220]:
  for y in [-40,40]:m.add('M16 mounting hardware envelope',m.cyl(16,60).union(m.cq.Workplane('XY').polygon(6,27.7).extrude(10).translate((0,0,30))),(x,y,0),material=m.BUY,process='Buy after joint/preload calculation',notes=['M16 is our candidate for Ø18 clearance holes, not a GALVI specified bolt.','Nut, washer stack, grip, grade and preload unresolved; envelope only.'],role='bought-envelope',explode=[0,0,75])
m.BRIEFS[code]=brief;m.BUILDERS[code]=model
p=m.build(code)
# Do not append this study to the original twelve-family catalogue.
p['source']=dict(url=source,sha256='08b6d7d0f37c2e4973c8cc67c7c8325d25c32cd6ee42d56403ce615c3b5e5675',revision='February 2016',pdf_pages=[4,15],printed_pages=['4–5','26–27'],verified_on='2026-09-07',current_supplier_confirmation=False)
p['dimensions']=[dict(symbol=s,label=l,value=v,unit='count' if s=='PD-X' else 'mm',page=page,status='published; current revision unconfirmed') for s,l,v,page in dims]
p['annotations']=[dict(label='Ø315 mm · GALVI PD.315',a=[-157.5,-100,230],b=[157.5,-100,230],status='published'),dict(label='230 mm axis height · GALVI B',a=[-210,-100,0],b=[-210,-100,230],status='published'),dict(label='440 mm full pitch · 2 × GALVI H',a=[-220,-65,-20],b=[220,-65,-20],status='published'),dict(label='153 mm axial length · GALVI PD.C',a=[190,-76.5,230],b=[190,76.5,230],status='published')]
(R/'website/app/galvi-study.json').write_text(json.dumps(p,indent=2))
root=R/'website/public/products'/brief['slug']
(root/'dimension-register.json').write_text(json.dumps(dict(source=p['source'],dimensions=p['dimensions']),indent=2))
print('GALVI study:',len(p['parts']),'components;',len(dims),'sourced dimensions')

# Classify nonphysical envelope intersections rather than accepting them as fits.
checkpath=R/'engineering/products'/code/'C0/geometry-checks.json'
checks=json.loads(checkpath.read_text());roles={x['id']:x['role'] for x in p['parts']}
for item in checks['intersections']:
 item['status']='nonphysical reserved-volume overlap' if 'interface-envelope' in [roles[item['a']],roles[item['b']]] else 'physical overlap: unresolved'
checkpath.write_text(json.dumps(checks,indent=2));shutil.copyfile(checkpath,root/'geometry-checks.json')
# Include the specialized generator and sourced register in the review archive.
studyroot=R/'engineering/products'/code/'C0'
shutil.copyfile(__file__,studyroot/'galvi_study.py')
shutil.copyfile(root/'dimension-register.json',studyroot/'dimension-register.json')
manifest=[dict(path=str(f.relative_to(studyroot)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size) for f in studyroot.rglob('*') if f.is_file() and f.name not in ['manifest.json','web-record.json']]
(studyroot/'manifest.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(root/(code+'-C0-review.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for f in studyroot.rglob('*'):
  if f.is_file() and f.name!='web-record.json':z.write(f,str(f.relative_to(studyroot)))
