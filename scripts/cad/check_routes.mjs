import fs from 'node:fs';
const origin=process.argv[2]||'http://localhost:3000';
const products=JSON.parse(fs.readFileSync('website/app/products-data.json','utf8'));
let checked=0;
for(const p of products){
 const url=`${origin}/products/${p.slug}`;const page=await fetch(url);if(!page.ok)throw Error(`${url}: ${page.status}`);const html=await page.text();if(!html.includes(p.code)||!html.includes('Assembly navigator'))throw Error(`Missing product content ${p.slug}`);
 for(const file of [p.downloads.step,p.downloads.pdf,p.downloads.zip,'bom.csv','mesh.json','preview.svg',...p.parts.flatMap(x=>[`parts/${x.id}/${x.id}.step`,`parts/${x.id}/${x.id}.svg`])]){
  const r=await fetch(`${url}/${file}`);if(!r.ok)throw Error(`${p.code}/${file}: ${r.status}`);const b=new Uint8Array(await r.arrayBuffer());const text=new TextDecoder().decode(b.slice(0,120));if(file.endsWith('.step')&&!text.startsWith('ISO-10303-21'))throw Error(`Not STEP: ${file}`);if(file.endsWith('.pdf')&&!text.startsWith('%PDF-'))throw Error(`Not PDF: ${file}`);if(file.endsWith('.zip')&&!(b[0]===80&&b[1]===75))throw Error(`Not ZIP: ${file}`);checked++;
 }
 console.log(`${p.code}: route and downloads OK`);
}
const missing=await fetch(origin+'/products/not-a-product');if(missing.status!==404)throw Error('Missing product did not return 404');
console.log(`${products.length} routes, ${checked} downloads and 404 verified. Browser/WebGL interaction not tested.`);
