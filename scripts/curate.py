#!/usr/bin/env python3
"""Source-checked seed facts. These are catalogue facts, not validated AI Braking ratings."""
import json,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=[]
def rec(m,model,field,value,unit,conditions,selector,page=None,revision=None):
 records=json.loads((R/f'research/normalized/{m}-collection.json').read_text())['records']
 s=next(x for x in records if selector in x.get('url','') or selector in x.get('sha256',''))
 rows.append(dict(id=f'SPEC-{len(rows)+1:03}',manufacturer=m,model=model,property=field,value=value,unit=unit,conditions=conditions,source_url=s['url'],source_sha256=s['sha256'],pdf_page=page,document_revision=revision,checked_at='2026-09-07',verification='source-checked by AI; not independently tested',review_method='rendered PDF page and extracted text' if page else 'archived official product-page text',engineering_approval='not approved as design input'))
rec('galvi','N(NV)…HYD','calculation friction coefficient',0.42,'1','Published lining calculation assumption, not measured coefficient across all conditions','schedatecnica/1')
rec('galvi','PD / PL','PD material option','EN-GJL-250','grade','Published cast-iron option; select actual version and duty before comparison','schedatecnica/12')
rec('galvi','PD / PL','alternative material option','EN-GJS-500-7','grade','Published ductile-iron option; not interchangeable without engineering review','schedatecnica/12')
rec('dellner-bubenzer','CMB-3 for SF','ambient temperature range','-20 to +70','deg C','Monitoring unit rating; not brake friction-surface temperature','/products/cmb-3-for-sf-brakes')
rec('dellner-bubenzer','CMB-3 for SF','enclosure protection','IP65','rating','Published standard unit enclosure rating','/products/cmb-3-for-sf-brakes')
rec('dellner-bubenzer','CMB-3 for SF','fieldbus options','Profibus / Profinet','interface','Options described on product page; confirm selected configuration','/products/cmb-3-for-sf-brakes')
rec('sibre','SHI 75-1','clamping force',18.3,'kN','Air gap c = 1 mm; FA in manufacturer table','87cfb89',1,'M 1501 306 E-DE-2017-01')
rec('sibre','SHI 75-1','release pressure',45,'bar','Type 75-1; distinguish release pressure from maximum pressure','87cfb89',1,'M 1501 306 E-DE-2017-01')
rec('sibre','SHI 75-1','maximum pressure',85,'bar','Type 75-1; manufacturer hydraulic limit','87cfb89',1,'M 1501 306 E-DE-2017-01')
rec('stromag','SH32','maximum braking torque',458000,'N m','Overview maximum specifically at disc diameter 3000 mm; not every SH configuration','d0320fa',61,'MCC-P-8518-SG-EN-A4 04/25')
rec('stromag','SH / SHV','overview disc diameter range','300 to 3000','mm','Family overview; individual model selection still required','d0320fa',61,'MCC-P-8518-SG-EN-A4 04/25')
rec('stromag','TH / THC','overview disc diameter range','1000 to 2000','mm','Family overview; individual model selection still required','d0320fa',61,'MCC-P-8518-SG-EN-A4 04/25')
rec('twiflex','MU3','maximum braking force',2.75,'kN','At 5 bar; conditioned pads; nominal friction coefficient 0.4','644a8ed',8,'P-1648-TF 3/21; printed page 6')
rec('twiflex','MU3','maximum pressure',5,'bar','Pneumatic applied / spring released variant','644a8ed',8,'P-1648-TF 3/21; printed page 6')
rec('twiflex','MU series','minimum disc diameter',150,'mm','Series guidance; mounting and specific variant require review','644a8ed',8,'P-1648-TF 3/21; printed page 6')
rec('svendborg','BSFI 100 MONOspring','maximum operating pressure',23.0,'MPa','Catalogue specification; do not generalize to other BSFI models','e8078a',5,'P-7575-SV 7/20; printed page 4')
rec('svendborg','BSFI 100 MONOspring','general operating temperature','-20 to +70','deg C','Manufacturer requests consultation outside range; not friction-surface limit','e8078a',5,'P-7575-SV 7/20; printed page 4')
rec('svendborg','BSFI 100 MONOspring','actuating time guide',0.4,'s','Guide value for calculation, not a guaranteed response in every installation','e8078a',5,'P-7575-SV 7/20; printed page 4')
rec('mondel','Angled brake wheel; OD 8 in','maximum speed',5000,'rpm','8-inch OD row, angled wheel table; shaft/interface suitability separately required','7e6d04',2,'MH638 Brake Accessories 2/16')
rec('mondel','Angled brake wheel; OD 8 in','weight',32,'lb','8-inch OD row; do not treat as finished custom bore mass','7e6d04',2,'MH638 Brake Accessories 2/16')
rec('mondel','Angled brake wheel; OD 8 in','heat dissipation',1800000,'ft lbf/h','Published table figure; thermal boundary conditions not specified on this page','7e6d04',2,'MH638 Brake Accessories 2/16')
rec('emg','ELHY','ambient temperature range','-45 to +80','deg C','Family-level product-page claim; configuration and fluid must be confirmed','/solutions/safety-components/emg-elhy')
rec('emg','ELHY','available enclosure protection','up to IP68','rating','Configuration-dependent claim, not standard rating of every unit','/solutions/safety-components/emg-elhy')
rec('emg','ELHY','factory testing claim','100% function and endurance run','manufacturer claim','Claim describes production testing; not independent validation or lifetime certification','/solutions/safety-components/emg-elhy')
(R/'research/normalized/reviewed-specifications.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False))
with (R/'research/normalized/reviewed-specifications.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(len(rows),'source-checked seed facts')
