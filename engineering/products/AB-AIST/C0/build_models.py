#!/usr/bin/env python3
"""Reproducible original C0 layout solids, drawings and web meshes. Units: mm.
Geometry validity is not engineering validation. Never use C0 files to manufacture.
"""
import cadquery as cq
import json, math, csv, hashlib, shutil, zipfile, sys, io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from types import SimpleNamespace
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.utils import simpleSplit
from product_briefs import BRIEFS
R=Path(__file__).resolve().parents[2]; OUT=R/'engineering/products'; PUB=R/'website/public/products'
REV='C0'; DATE='2026-09-07'; PARTS=[]; CODE=''
STEEL='S355J2+N candidate; condition and design properties unapproved'
PIN='42CrMo4 candidate; heat treatment / fit unapproved'
BUY='Supplier-controlled; illustrative reserved envelope'
COLORS=['#5e91b7','#a2b6c7','#38a5d0','#415a77','#76c6dc','#d3dde5']
def box(x,y,z):return cq.Workplane('XY').box(x,y,z)
def ring(od,id,h):return cq.Workplane('XY').circle(od/2).circle(id/2).extrude(h).translate((0,0,-h/2))
def cyl(d,h):return cq.Workplane('XY').circle(d/2).extrude(h).translate((0,0,-h/2))
def plate(x,y,z,holes=(),d=13):
 s=box(x,y,z)
 for a,b in holes:s=s.cut(cyl(d,z+2).translate((a,b,0)))
 return s
def flange(od,bore,t,pcd,n,d):
 s=ring(od,bore,t)
 for i in range(n):s=s.cut(cyl(d,t+2).translate((pcd/2*math.cos(i*2*math.pi/n),pcd/2*math.sin(i*2*math.pi/n),0)))
 return s
def add(name,shape,pos=(0,0,0),material=STEEL,process='Saw/laser blank; CNC critical faces and bores',notes=None,role='make-concept',explode=None):
 idx=len(PARTS)+1;pid=f'{CODE}-{idx:03d}'
 sh=shape.val() if isinstance(shape,cq.Workplane) else shape
 assert sh.isValid() and sh.Volume()>0,(pid,name)
 PARTS.append(dict(id=pid,item=idx,name=name,shape=sh,pos=pos,material=material,process=process,notes=notes or ['All dimensions nominal. Fits, GD&T and edge details awaiting engineer release.'],role=role,color=COLORS[(idx-1)%len(COLORS)],explode=explode or [0,0,idx*15]))
 return pid

def rotor():
 add('Disc 400',flange(400,110,20,150,6,13),notes=['OD 400; bore 110; thickness 20 mm.','6 x diameter 13 THRU on PCD 150; first hole on +X.','Candidate M12 through-bolts; preload and friction joint unresolved.'],material='C45 normalized candidate; friction pair unqualified',explode=[0,0,70])
 hub=flange(170,50,12,150,6,13).translate((0,0,-16)).union(ring(110,50,20)).union(ring(85,50,55).translate((0,0,-49.5)))
 add('Detachable flanged hub',hub,material=PIN,notes=['Shaft bore 50; spigot OD 110; flange OD 170 mm.','Flange 12 mm; 6 x diameter 13 THRU on PCD 150.','No shaft locking, keyway, fit or retention released.'],explode=[0,0,-70])
 for i in range(6):
  a=i*math.pi/3
  add(f'M12 interface fastener envelope {i+1}',cyl(12,44).union(cyl(20,8).translate((0,0,26))),(75*math.cos(a),75*math.sin(a),-8),material=BUY,process='Buy certified bolt/nut/washer set after joint calculation',notes=['Smooth nominal shank only; threads, washer and nut omitted.','Fastener length, grade and preload not released.'],role='bought-envelope',explode=[0,0,100])

def drum(d=315):
 r=d/2; zc=r+100
 add('Four-hole base',plate(520,240,20,[(-230,-90),(230,-90),(-230,90),(230,90)],18),(0,0,10),notes=['520 x 240 x 20; 4 x diameter 18 THRU.','Hole centres X +/-230, Y +/-90 from part origin.','Machine base datum; mounting preload unassigned.'],explode=[0,0,-80])
 dr=ring(d,d-36,110).union(flange(d-36,90,14,125,6,13))
 add('Study brake drum',dr.rotate((0,0,0),(1,0,0),90),(0,0,zc),material='C45 prototype candidate; friction/thermal qualification required',notes=[f'OD {d}; friction width 100 within 110 mm axial envelope.','Web bore 90; 6 x diameter 13 on PCD 125.','Shaft hub and retention not detailed.'],explode=[0,-150,20])
 for side in [-1,1]:
  x=side*(r+42)
  # Clevis base and two bored ears, with a real open slot for lever.
  clevis=plate(65,100,12,[(-20,-35),(20,-35),(-20,35),(20,35)],9).translate((0,0,-26))
  for y in [-36,36]:
   ear=box(60,16,65).translate((0,y,0)).cut(cyl(20,100).rotate((0,0,0),(1,0,0),90))
   clevis=clevis.union(ear)
  add(f'Pivot clevis {side}',clevis,(x,0,52.5),notes=['Clevis pin bore 20; nominal ear gap 56 mm.','Foot 4 x diameter 9 at (+/-20,+/-35); base mating holes pending.'],explode=[side*60,0,-20])
  lev=box(32,24,290).translate((0,0,130))
  for z in [0,205,260]:lev=lev.cut(cyl(20,30).rotate((0,0,0),(1,0,0),90).translate((0,0,z)))
  add(f'Lever {side}',lev,(x,0,52.5),notes=['32 x 24 section; pin centres Z 0, 205, 260 in local coordinates.','Nominal pin bore 20; bush fit not detailed.'],explode=[side*110,0,0])
  add(f'Lower pivot pin {side}',cyl(19.8,105).rotate((0,0,0),(1,0,0),90),(x,0,52.5),material=PIN,process='Turn/grind; specify retention after review',notes=['Diameter 19.8 study clearance in nominal 20 bore.','No final fit, hardness or axial retainer design.'],explode=[side*70,100,0])
  for inner,outer,name,mat in [(r+1,r+9,'Lining',BUY),(r+9,r+23,'Shoe carrier',STEEL)]:
   sh=ring(outer*2,inner*2,100).rotate((0,0,0),(1,0,0),90).intersect(box(90,110,180).translate((side*(r+10),0,0)))
   add(f'{name} {side}',sh,(0,0,zc),material=mat,process='Buy friction lining / machine carrier to approved retention drawing',notes=['1 mm radial study gap at drum; not a release-clearance specification.','Carrier pivots and lining retention remain to be designed.'],role='bought-envelope' if name=='Lining' else 'make-concept',explode=[side*90,0,30])
 add('Thruster reserved space',cyl(100,190),(r+145,0,140),material=BUY,process='Buy selected thruster; replace with vendor STEP',notes=['Nonfunctional body envelope; linkage not included.'],role='bought-envelope',explode=[160,0,40])
 add('Spring/equalizer reserved space',box(160,50,45),(0,0,zc+r+60),material=BUY,process='Engineer spring/linkage after kinematics',notes=['Reserved volume only; no spring, force path or release motion solved.'],role='interface-envelope',explode=[0,0,110])

def disc(positive=False):
 # XY rotor, Z shaft axis; bridge above rotor rim in +Y.
 add('Common disc reference',flange(400,110,20,150,6,13),material='C45 candidate',notes=['Common AB-ROT disc geometry; see rotor package for hub.'],role='shared-concept',explode=[0,-100,0])
 add('Bridge beam',plate(150,45,60,[(-55,0),(55,0)],13),(0,247.5,0),notes=['Bridge width 150; depth 45; axial span 60.','Tie interface bores are concept only; structural joint not released.'],explode=[0,90,0])
 for side in [-1,1]:
  add(f'Cheek plate {side}',plate(150,160,20,[(-55,52.5),(55,52.5)],13),(0,195,side*40),notes=['150 x 160 x 20; mounting holes local X +/-55, Y 52.5.','Faces mate bridge at Z +/-30; preload/fastener detail pending.'],explode=[0,0,side*110])
  add(f'Pad backing {side}',plate(70,60,8,[(-25,0),(25,0)],8.5),(0,155,side*23),material='C45 candidate',notes=['70 x 60 x 8; two diameter 8.5 retainer holes.','Retention detail must avoid lining damage.'],explode=[0,-30,side*70])
  add(f'Friction pad {side}',box(70,60,8),(0,155,side*15),material=BUY,process='Purchase matched compound and approved bonding/retention',notes=['Pad inner face Z +/-11; 1 mm cold study clearance to disc.','Uniform pressure effective radius approximated at 155 mm.'],role='bought-envelope',explode=[0,-35,side*40])
  add(f'{"Direct" if positive else "Spring-release"} cartridge {side}',cyl(65,70),(0,155,side*85),material=BUY,process='Purchase cartridge; mounting interface unassigned',notes=['Diameter 65 x 70 envelope only.','No pressure port, piston, seals or spring mechanism modelled.'],role='bought-envelope',explode=[0,0,side*160])

def service():
 for i,x in enumerate([-55,55]):
  add(f'Backing plate {i+1}',plate(70,60,8,[(-25,0),(25,0)],8.5),(x,0,0),material='C45 candidate',notes=['70 x 60 x 8; 2 x diameter 8.5 on 50 mm pitch.','Common nominal planform with AB-DC.'],explode=[x,0,-30])
  add(f'Lining block {i+1}',box(70,60,8),(x,0,8),material=BUY,process='Specialist friction supplier',notes=['8 mm concept thickness; compound and retention unresolved.'],role='bought-envelope',explode=[x,0,55])
  add(f'Retainer pin {i+1}',cyl(8,85),(x,65,0),material=PIN,process='Turn/grind; retention detail pending',notes=['Diameter 8 x 85 smooth envelope; no final retaining feature.'],explode=[x,40,35])
  add(f'Bush {i+1}',ring(28,20,24),(x,-65,0),material='Purchased bronze bearing candidate',process='Buy or turn to approved fit',notes=['OD 28; bore 20; length 24; fit not assigned.'],explode=[x,-40,20])

def thruster():
 add('Integration base',plate(200,180,16,[(-75,-60),(75,-60),(-75,60),(75,60)],13),notes=['200 x 180 x 16; 4 x diameter 13 at (+/-75,+/-60).'],explode=[0,0,-70])
 add('Thruster body envelope',cyl(120,240),(0,0,140),material=BUY,process='Buy selected electrohydraulic thruster',role='bought-envelope',explode=[0,0,30])
 add('Rod travel envelope',cyl(30,100),(0,0,310),material=BUY,process='Supplier model required',notes=['Includes 60 mm assumed stroke; no seal or bearing design.'],role='interface-envelope',explode=[0,0,100])
 add('Top clevis envelope',box(65,35,50).cut(box(28,40,28).translate((0,0,12))).cut(cyl(16,40).rotate((0,0,0),(1,0,0),90)),(0,0,385),material=BUY,process='Supplier interface',role='interface-envelope',explode=[0,0,150])

def hpu():
 tank=box(400,260,220).cut(box(394,254,220).translate((0,0,3)))
 add('Reservoir shell',tank,(0,0,110),notes=['Outer 400 x 260 x 220; nominal wall and floor 3 mm.','No baffles, drains or weld details released; open top.'],process='Fabricate welded sheet; clean and leak-test after approval',explode=[0,0,-80])
 add('Removable deck',plate(420,280,6,[(-190,-120),(190,-120),(-190,120),(190,120)],9),(0,0,223),notes=['420 x 280 x 6; four diameter 9 holes at (+/-190,+/-120).','Tank mating flange/fasteners and gasket pending.'],explode=[0,0,60])
 add('Motor-pump envelope',cyl(125,180),(-95,0,316),material=BUY,process='Buy selected motor-pump',role='bought-envelope',explode=[-80,0,150])
 add('Qualified valve block envelope',box(130,100,75),(95,0,263.5),material=BUY,process='Buy manifold; no custom pressure channels',role='bought-envelope',explode=[80,0,110])
 add('Filter envelope',cyl(55,130),(90,90,291),material=BUY,process='Buy selected filter',role='bought-envelope',explode=[80,70,130])

def coupling():
 for side in [-1,1]:
  s=flange(160,50,16,120,6,11).union(ring(90,50,55).translate((0,0,side*35.5)))
  add(f'Hub {side}',s,(0,0,side*38),material=PIN,notes=['Flange OD 160; bore 50; six diameter 11 on PCD 120.','No shaft key/locking or torque-transmitting flexible interface.'],explode=[0,0,side*100])
 add('Flexible-element reserved envelope',ring(145,70,60),material=BUY,process='Buy complete coupling or engineered flexible element',notes=['Reserved space, not a functioning elastic or gear mechanism.'],role='interface-envelope',explode=[0,80,0])

def buffer():
 add('Mounting plate',plate(240,240,25,[(-90,-90),(90,-90),(-90,90),(90,90)],22),notes=['240 x 240 x 25; 4 x diameter 22 on 180 square.','Foundation bolts must be sized for supplier peak force.'],explode=[0,0,-70])
 add('Absorber body envelope',cyl(130,250),(0,0,137.5),material=BUY,process='Buy rated absorber',role='bought-envelope',explode=[0,0,30])
 add('Rod envelope',cyl(55,150),(0,0,337.5),material=BUY,process='Vendor stroke model required',role='bought-envelope',explode=[0,0,100])
 add('Impact face envelope',cyl(180,35),(0,0,430),material=BUY,process='Buy supplier face/bumper',role='bought-envelope',explode=[0,0,150])

def rail():
 rail=box(70,350,30).translate((0,0,85)).union(box(20,350,70).translate((0,0,35))).union(box(140,350,20).translate((0,0,-10)))
 add('Rail reference envelope',rail,material='Customer rail specification required',process='Reference only; not supplied',role='interface-envelope',explode=[0,-100,-40])
 add('Clamp crosshead',plate(260,140,30,[(-100,-45),(100,-45),(-100,45),(100,45)],18),(0,0,170),notes=['Original package interface only; not a structural sizing.'],explode=[0,0,100])
 for side in [-1,1]:
  add(f'Jaw carrier {side}',box(35,100,100),(side*65,0,105),notes=['Carrier concept; mechanism, pins and adjustment omitted.'],explode=[side*90,0,40])
  add(f'Rail shoe {side}',box(10,100,28),(side*41,0,85),material=BUY,process='Specialist rail-contact material',notes=['1 mm lateral rail clearance study.','No wedge/latch or contact force mechanism.'],role='bought-envelope',explode=[side*60,0,0])
 add('Actuation reserved volume',cyl(95,110),(0,0,240),material=BUY,process='Specialist spring/wedge mechanism required',role='interface-envelope',explode=[0,0,150])

def fixture():
 add('Inspection base',plate(650,350,25,[(-290,-140),(290,-140),(-290,140),(290,140)],13),notes=['650 x 350 x 25; 4 x diameter 13 at (+/-290,+/-140).','Flatness datum and levelling scheme not released.'],explode=[0,0,-80])
 for side in [-1,1]:
  add(f'Centre support envelope {side}',box(90,120,250).cut(cyl(51,100).rotate((0,0,0),(0,1,0),90).translate((0,0,102.5))),(side*250,0,137.5),material=BUY,process='Buy precision centre/support',notes=['Reserved supports; spindle axis Z 240.'],role='bought-envelope',explode=[side*80,0,0])
 add('Study mandrel',cyl(50,490).rotate((0,0,0),(0,1,0),90),(0,0,240),material=PIN,process='Turn/grind after datum and mounting design',notes=['Diameter 50 nominal; no centre holes, bearing seats or expanding feature.'],explode=[0,0,100])
 add('Reference disc',ring(400,50,20).rotate((0,0,0),(0,1,0),90),(0,0,240),material='Reference test piece; not AB-ROT interface',process='Reference only',role='interface-envelope',explode=[0,0,40])
 add('Indicator column',cyl(25,350),(160,120,187.5),material='6082-T6 aluminium candidate',process='Machine adjustable metrology support',explode=[80,80,0])
 add('Probe arm envelope',box(140,20,20).cut(cyl(25.5,24).translate((65,0,0))),(95,120,350),material=BUY,process='Buy articulated holder and calibrated indicator',role='bought-envelope',explode=[50,80,80])

BUILDERS={'AB-ROT':rotor,'AB-DR':drum,'AB-DC':disc,'AB-SP':service,'AB-AIST':lambda:drum(304.8),'AB-ACT':thruster,'AB-HPU':hpu,'AB-COUP':coupling,'AB-POS':lambda:disc(True),'AB-BUF':buffer,'AB-SPEC':rail,'AB-MON':fixture}

def edges(shape):
 lines=[]
 for e in shape.Edges():
  try:
   pts,_=e.sample(2 if e.geomType()=='LINE' else 72)
   pts.append(e.endPoint())
   lines.append([list(v.toTuple()) for v in pts])
  except Exception:pass
 return lines

def projection(lines,axes,rect):
 x,y,w,h=rect;pts=[p for line in lines for p in line];a,b=axes
 lo=[min(p[a] for p in pts),min(p[b] for p in pts)];hi=[max(p[a] for p in pts),max(p[b] for p in pts)]
 scale=min((w-48)/max(hi[0]-lo[0],1),(h-56)/max(hi[1]-lo[1],1));ox=x+w/2-(hi[0]+lo[0])/2*scale;oy=y+h/2-(hi[1]+lo[1])/2*scale
 return [[(ox+p[a]*scale,oy+p[b]*scale) for p in line] for line in lines],(ox+lo[0]*scale,oy+lo[1]*scale,ox+hi[0]*scale,oy+hi[1]*scale),[hi[0]-lo[0],hi[1]-lo[1]]

def exact_bounds(shape):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(shape.wrapped,b,False,False)
 xmin,ymin,zmin,xmax,ymax,zmax=b.Get()
 return SimpleNamespace(xmin=xmin,ymin=ymin,zmin=zmin,xmax=xmax,ymax=ymax,zmax=zmax,xlen=xmax-xmin,ylen=ymax-ymin,zlen=zmax-zmin)

def view_svg(shape,direction,width=490,height=240):
 if direction==(0,-1,0):shape=shape.rotate((0,0,0),(1,0,0),-90)
 elif direction==(1,0,0):shape=shape.rotate((0,0,0),(0,0,1),-90).rotate((0,0,0),(1,0,0),-90)
 direction=(0,0,1)
 return cq.exporters.getSVG(shape,opts={'width':width,'height':height,'marginLeft':25,'marginTop':25,'showAxes':False,'projectionDir':direction,'strokeWidth':.8,'strokeColor':(37,76,110),'showHidden':True,'hiddenColor':(165,188,205)})

def drawing_svg(p,lines):
 from html import escape
 out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 820">','<rect width="1200" height="820" fill="#fff"/>']
 for direction,x,y,label in [((0,0,1),35,50,'TOP X-Y'),((0,-1,0),35,415,'FRONT X-Z'),((1,0,0),630,415,'SIDE Y-Z')]:
  svg=view_svg(p['shape'],direction);svg=svg[svg.index('<svg'):]
  out += [f'<g transform="translate({x},{y})">',svg,'</g>',f'<text x="{x}" y="{y-10}" fill="#254c6e" font-size="13">{label}</text>']
 out += [f'<text x="625" y="85" fill="#19334f" font-size="24">{escape(p["id"])} / C0</text>',f'<text x="625" y="118" fill="#19334f" font-size="19">{escape(p["name"])}</text>']
 bb=exact_bounds(p['shape']);notes=[f'Overall X / Y / Z bounds: {bb.xlen:.2f} / {bb.ylen:.2f} / {bb.zlen:.2f} mm',*p['notes']]
 y=155
 for n in notes:
  for t in simpleSplit(n,'Helvetica',12,450):out.append(f'<text x="625" y="{y}" fill="#365774" font-size="12">{escape(t)}</text>');y+=18
  y+=10
 out+=['<rect x="20" y="748" width="1160" height="53" fill="#eaf3fa"/>','<text x="36" y="771" fill="#1b4e80" font-size="15">C0 CONCEPT / NOT FOR MANUFACTURE / NOMINAL mm / THIRD-ANGLE VIEW POSITIONS</text>','<text x="36" y="791" fill="#365774" font-size="12">CAD hidden-line projections; bounds and features are reference only. No tolerance, fit, finish or strength approval.</text>','</svg>']
 return '\n'.join(out)

def pack_pdf(code,brief,parts,dest):
 W,H=landscape(A3);c=canvas.Canvas(str(dest),pagesize=(W,H));c.setTitle(f'{code} C0 engineering review pack')
 def page(title):
  c.setFillColor(colors.HexColor('#0d233b'));c.rect(0,H-85,W,85,fill=1,stroke=0);c.setFillColor(colors.white);c.setFont('Helvetica-Bold',22);c.drawString(35,H-43,title);c.setFont('Helvetica',10);c.drawString(35,H-64,f'AI BRAKING  /  {code}  /  C0  /  {DATE}')
  c.setFillColor(colors.HexColor('#eaf3fa'));c.rect(25,20,W-50,39,fill=1,stroke=0);c.setFillColor(colors.HexColor('#1b4e80'));c.setFont('Helvetica-Bold',10);c.drawString(37,43,'ENGINEER REVIEW ONLY - NOT FOR MANUFACTURE - NO VALIDATED RATINGS');c.setFont('Helvetica',8);c.drawString(37,29,'Original concept geometry. Nominal mm. No tolerances, GD&T, finish, preload, material approval or certification.');c.drawRightString(W-38,29,str(c.getPageNumber()))
 def textblock(text,y,width=W-80,size=11):
  c.setFont('Helvetica',size);c.setFillColor(colors.HexColor('#243e57'))
  for ln in simpleSplit(text,'Helvetica',size,width):c.drawString(38,y,ln);y-=size*1.5
  return y-9
 page(brief['short']+' - design brief');y=H-118
 y=textblock(brief['description'],y)
 for head,items in [('TARGETS (not validated)',[f'{a}: {b}. {d}' for a,b,d in brief['targets']]),('DESIGN DECISIONS',brief['decisions']),('CANDIDATE MATERIALS',brief['materials'])]:
  c.setFont('Helvetica-Bold',12);c.drawString(38,y,head);y-=24
  for t in items:y=textblock(t,y)
 c.showPage();page('Assembly and engineering gates');y=H-118
 for head,items in [('ASSEMBLY INTENT',brief['steps']),('OPEN DESIGN RISKS',brief['risks']),('VALIDATION REQUIRED',brief['validation']),('ELECTRICAL / SENSOR REQUIREMENTS ONLY',brief['sensors'])]:
  c.setFont('Helvetica-Bold',12);c.drawString(38,y,head);y-=22
  for i,t in enumerate(items):y=textblock(f'{i+1}. {t}',y,size=10)
  if y<190:c.showPage();page('Engineering gates continued');y=H-118
 c.showPage();page('Assembly reference / numbered components')
 lines=[];anchors=[]
 for part in parts:
  world=part['shape'].translate(cq.Vector(*part['pos']))
  def iso(v):return [(v[0]-v[1])*.7071,(v[0]+v[1])*.4082+v[2]*.8165,0]
  lines.extend([[iso(v) for v in line] for line in edges(world)])
  anchors.append(iso(list(world.Center().toTuple())))
 pls,b,d=projection(lines,(0,1),(215,100,720,570))
 pts=[v for line in lines for v in line];lo=[min(p[i] for p in pts) for i in [0,1]];hi=[max(p[i] for p in pts) for i in [0,1]]
 scale=min((720-48)/max(hi[0]-lo[0],1),(570-56)/max(hi[1]-lo[1],1));ox=215+360-(hi[0]+lo[0])/2*scale;oy=100+285-(hi[1]+lo[1])/2*scale
 c.setStrokeColor(colors.HexColor('#457798'));c.setLineWidth(.4)
 for line in pls:
  path=c.beginPath();path.moveTo(*line[0])
  for pt in line[1:]:path.lineTo(*pt)
  c.drawPath(path)
 for i,(part,anchor) in enumerate(zip(parts,anchors)):
  left=i%2==0;xx=72 if left else W-95;yy=H-135-(i//2)*67
  ax,ay=ox+anchor[0]*scale,oy+anchor[1]*scale
  c.setStrokeColor(colors.HexColor('#4da8d0'));c.line(xx,yy,ax,ay);c.setFillColor(colors.white);c.circle(xx,yy,12,fill=1,stroke=1);c.setFillColor(colors.HexColor('#20577d'));c.setFont('Helvetica-Bold',9);c.drawCentredString(xx,yy-3,str(part['item']));c.setFont('Helvetica',7);c.drawCentredString(xx,yy-24,part['id'])
 c.setFont('Helvetica',10);c.drawString(38,76,'Static isometric reference with item marks. Exploded geometry and part selection are available in the web workspace.')
 c.showPage();page('Parts and interfaces');y=H-115
 for p in parts:
  y=textblock(f'{p["id"]} | {p["name"]} | {p["role"]}',y,size=11)
  y=textblock(p['material']+'; '+p['process'],y,size=9)
  if y<115:c.showPage();page('Parts continued');y=H-115
 c.showPage()
 for p in parts:
  page(p['id']+' / '+p['name']);ls=edges(p['shape'])
  for direction,x,y,label in [((0,0,1),35,405,'TOP X-Y'),((0,-1,0),35,95,'FRONT X-Z'),((1,0,0),625,95,'SIDE Y-Z')]:
   svg=view_svg(p['shape'],direction);drawing=svg2rlg(io.BytesIO(svg.encode()))
   drawing.scale(1.3,1.3);renderPDF.draw(drawing,c,x,y)
   c.setFillColor(colors.HexColor('#254c6e'));c.setFont('Helvetica',9);c.drawString(x,y+250,label)
  y=690
  for t in [p['material'],p['process'],f'Overall X/Y/Z bounds: {exact_bounds(p["shape"]).xlen:.2f} / {exact_bounds(p["shape"]).ylen:.2f} / {exact_bounds(p["shape"]).zlen:.2f} mm',*p['notes'],'CAD hidden-line reference projections. Bounds and selected features are nominal; see STEP for solid geometry.','Datum proposal: choose primary mounting face A, functional bore/axis B and clocking feature C during review.','Part marking: item ID + C0 + material lot on a non-friction/non-fit surface; exact location unresolved.']:
   c.setFont('Helvetica',10);c.setFillColor(colors.HexColor('#243e57'))
   for ln in simpleSplit(t,'Helvetica',10,480):c.drawString(625,y,ln);y-=15
   y-=8
  c.showPage()
 c.save()

def build(code):
 global CODE,PARTS
 CODE=code;PARTS=[];BUILDERS[code]();brief=BRIEFS[code];root=OUT/code/REV;root.mkdir(parents=True,exist_ok=True);ass=cq.Assembly(name=code);mesh=[];bom=[];checks=[]
 for p in PARTS:
  folder=root/'parts'/p['id'];folder.mkdir(parents=True,exist_ok=True);sh=p['shape'];cq.exporters.export(sh,str(folder/(p['id']+'.step')))
  imported=cq.importers.importStep(str(folder/(p['id']+'.step'))).val();err=abs(imported.Volume()-sh.Volume())/sh.Volume();assert imported.isValid() and err<1e-6
  ls=edges(sh);(folder/(p['id']+'.svg')).write_text(drawing_svg(p,ls))
  bb=exact_bounds(sh);dims=[round(bb.xlen,3),round(bb.ylen,3),round(bb.zlen,3)]
  verts,tris=sh.tessellate(.65,.3);v=[round(z,4) for pt in verts for z in pt.toTuple()];t=[i for tri in tris for i in tri]
  row={k:p[k] for k in ['id','item','name','pos','material','process','notes','role','color','explode']};row.update(dimensions=dims,volume_mm3=round(sh.Volume(),3),quantity=1)
  mesh.append(dict(id=p['id'],vertices=v,triangles=t,pos=p['pos'],color=p['color'],explode=p['explode']))
  bom.append(row);checks.append(dict(part=p['id'],valid_solid=True,solid_count=len(sh.Solids()),step_volume_relative_error=err))
  ass.add(sh,name=p['id'],loc=cq.Location(cq.Vector(*p['pos'])),color=cq.Color(*[int(p['color'][i:i+2],16)/255 for i in (1,3,5)]))
 ass.save(str(root/(code+'-assembly.step')))
 intersections=[]
 for i,p in enumerate(PARTS):
  a=p['shape'].translate(cq.Vector(*p['pos']))
  for q in PARTS[i+1:]:
   b=q['shape'].translate(cq.Vector(*q['pos']))
   if not a.BoundingBox().isInside(b.BoundingBox()) and not b.BoundingBox().isInside(a.BoundingBox()):
    ba,bb=a.BoundingBox(),b.BoundingBox()
    if any(getattr(ba,x+'max')<getattr(bb,x+'min') or getattr(bb,x+'max')<getattr(ba,x+'min') for x in 'xyz'):continue
   vol=a.intersect(b).Volume()
   if vol>1:intersections.append(dict(a=p['id'],b=q['id'],volume_mm3=round(vol,2),status='open: review contact/envelope interference; not approved fit'))
 (root/'geometry-checks.json').write_text(json.dumps(dict(parts=checks,intersections=intersections,scope='B-rep validity and STEP round-trip only; intersections are unresolved review items, not contact analysis.'),indent=2))
 (root/'bom.json').write_text(json.dumps(bom,indent=2))
 with (root/'bom.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=['id','item','name','quantity','role','material','process','dimensions']);w.writeheader();w.writerows({k:p[k] for k in w.fieldnames} for p in bom)
 (root/'design-brief.json').write_text(json.dumps(brief,indent=2))
 shutil.copyfile(__file__,root/'build_models.py');shutil.copyfile(Path(__file__).with_name('product_briefs.py'),root/'product_briefs.py')
 (root/'README.md').write_text(f'# {code} / C0 / engineer review\n\n{brief["description"]}\n\nNOT FOR MANUFACTURE. All dimensions are nominal mm. Drawings are orthographic reference projections, not complete production drawings. Hardware, fits, tolerances, GD&T, welds, material condition, shaft attachment, retention and performance remain to be approved. Envelope parts are not manufacturable internals.\n\nOpen `geometry-checks.json` before reviewing assembly. Intersections are recorded, not silently accepted. Models are static; no solved motion, FEA, CFD, thermal or physical qualification is included.\n\nSTEP: solid geometry. SVG: viewable nominal reference drawing. PDF: review drawing pack. BOM: part identity and make/buy status. These are original models, not copied competitor CAD.\n\nRebuild from repository: `uv venv --python 3.11 .cad-venv`, `uv pip install --python .cad-venv/bin/python -r engineering/cad/requirements.txt`, `.cad-venv/bin/python scripts/cad/build_models.py {code}`. Packaged scripts are source references; run them in the documented repository layout.\n')
 pdf=root/(code+'-review-pack.pdf');pack_pdf(code,brief,PARTS,pdf)
 hashes=[dict(path=str(p.relative_to(root)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in root.rglob('*') if p.is_file() and p.name not in ['manifest.json','web-record.json']];(root/'manifest.json').write_text(json.dumps(hashes,indent=2))
 public=PUB/brief['slug'];public.mkdir(parents=True,exist_ok=True)
 for p in [root/(code+'-assembly.step'),pdf,root/'bom.csv',root/'geometry-checks.json',root/'README.md']:shutil.copyfile(p,public/p.name)
 with zipfile.ZipFile(public/(code+'-C0-review.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(root.rglob('*')):
   if p.is_file() and p.name!='web-record.json':z.write(p,str(p.relative_to(root)))
 (public/'mesh.json').write_text(json.dumps(mesh,separators=(',',':')))
 # Individual part files remain directly downloadable, avoiding a forced full archive.
 shutil.copytree(root/'parts',public/'parts',dirs_exist_ok=True)
 # Clean orthographic CAD-derived card thumbnail.
 compound=ass.toCompound();thumb=cq.exporters.getSVG(compound,opts={'width':700,'height':500,'showAxes':False,'projectionDir':(1,-1,.8),'strokeWidth':1,'strokeColor':(48,103,148),'showHidden':False})
 (public/'preview.svg').write_text(thumb)
 result=dict(code=code,revision=REV,date=DATE,**brief,parts=bom,intersections=intersections,part_count=len(bom),downloads=dict(step=code+'-assembly.step',pdf=code+'-review-pack.pdf',zip=code+'-C0-review.zip'))
 (root/'web-record.json').write_text(json.dumps(result,indent=2));print(code,len(bom),'parts',len(intersections),'open intersections',flush=True)
 return result
if __name__=='__main__':
 for code in (sys.argv[1:] or BUILDERS):build(code)
 records=[json.loads(p.read_text()) for p in OUT.glob('*/C0/web-record.json')];records.sort(key=lambda p:p['priority'])
 (R/'website/app/products-data.json').write_text(json.dumps(records,separators=(',',':')))
 print('Total:',len(records),'product pages')
