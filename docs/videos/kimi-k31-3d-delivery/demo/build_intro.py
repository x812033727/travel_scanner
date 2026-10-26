#!/usr/bin/env python3
"""Build one neutral, spoiler-free source frame from the actual original STLs."""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent
inputs = {
    'ring': (BASE / 'ring.stl').read_text(),
    'filled': (BASE / 'filled.stl').read_text(),
    'spec': json.loads((BASE / 'spec.json').read_text()),
}
page = r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>先看外觀｜原創 STL 教具</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f6efe3;color:#1f2a44;font-family:"Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif}.page{max-width:1920px;margin:auto;padding:42px 48px 28px}header{display:flex;justify-content:space-between;align-items:flex-start;gap:40px}.eyebrow{color:#d8452f;font-size:20px;font-weight:800;letter-spacing:.12em}h1{margin:8px 0 8px;font-size:43px;line-height:1.3}header p{margin:0;color:#626b7b;font-size:21px}.disclosure{background:#1f2a44;color:white;border-radius:10px;padding:19px 24px;font-size:23px;line-height:1.55;font-weight:750}.disclosure small{font-weight:400;font-size:16px;display:block;color:#dce0e7}.spec{display:flex;gap:50px;align-items:center;border-top:1px solid #d9d2c5;border-bottom:1px solid #d9d2c5;margin:26px 0 24px;padding:18px 0}.spec span{font-size:18px;color:#626b7b}.spec strong{display:block;font-size:30px;color:#1f2a44}.unit{margin-left:auto;font-size:19px;line-height:1.5}.unit b{color:#d8452f}.cards{display:grid;grid-template-columns:1fr 1fr;gap:24px}.card{border:1px solid #d9d2c5;border-radius:13px;background:#fffdf8}.card-head{padding:21px 26px 0;display:flex;justify-content:space-between;align-items:center}.card h2{margin:0;font-size:31px}.card-head span{font-size:20px;color:#626b7b}.mesh{display:block;width:100%;height:430px}.caption{border-top:1px solid #e3ddcf;margin:0 26px;padding:16px 0 21px;font-size:22px;color:#626b7b}.promise{margin-top:22px;padding:17px 22px;border-left:5px solid #d8452f;background:#e9e3d7;font-size:27px;line-height:1.5}.promise strong{color:#d8452f}footer{margin-top:16px;color:#626b7b;font-size:17px;line-height:1.6}@media(max-width:1000px){.page{padding:25px}.cards{grid-template-columns:1fr}header{flex-direction:column}.spec{flex-wrap:wrap;gap:25px}.unit{margin-left:0}.mesh{height:300px}h1{font-size:34px}.disclosure{font-size:21px}.promise{font-size:23px}}
</style></head><body><main class="page">
<header><div><div class="eyebrow">先看外觀，先別下結論</div><h1>同樣的外形，兩份都能交嗎？</h1><p>先打開檔案，再沿著同一份規格看下去。</p></div><div class="disclosure">原創教具，非 Kimi 生成結果<small>這兩份檔案由編輯製作；未測 Kimi 匯出、未實際列印。</small></div></header>
<section class="spec" aria-label="外部名義規格"><div><span>名義外徑</span><strong>40 mm</strong></div><div><span>名義貫穿孔徑</span><strong>16 mm</strong></div><div><span>厚度</span><strong>5 mm</strong></div><div class="unit"><b>STL 本身沒有單位。</b><br>本教具依外部規格假設為 mm。</div></section>
<section class="cards" aria-label="兩份實際 STL 的中性側視"><article class="card"><div class="card-head"><h2>檔案 A</h2><span>第一份檔案</span></div><canvas class="mesh" id="intro-ring" width="898" height="430" aria-label="第一份實際 STL 側視"></canvas><div class="caption">側視・先看外形與厚度</div></article><article class="card"><div class="card-head"><h2>檔案 B</h2><span>第二份檔案</span></div><canvas class="mesh" id="intro-filled" width="898" height="430" aria-label="第二份實際 STL 側視"></canvas><div class="caption">側視・先看外形與厚度</div></article></section>
<aside class="promise"><strong>檢查結果尚未展開。</strong> 接著把檔案轉過來，再逐項核對用途與規格。</aside>
<footer>這裡只呈現兩份真實網格的側視外觀；圖上數字是外部規格，不能當作孔或製造品質的結論。</footer>
</main><script type="application/json" id="intro-inputs">__ACTUAL_INPUTS__</script><script>
'use strict';const source=JSON.parse(document.querySelector('#intro-inputs').textContent);const evidence={view:'side',external_spec:source.spec,original_teaching_fixture_not_Kimi_output:true,results_not_displayed:true,models:{}};
function triangles(text){const vertices=[];for(const row of text.split(/\r?\n/)){const f=row.trim().split(/\s+/);if(f[0]==='vertex'){if(f.length!==4)throw Error('Invalid vertex');const v=f.slice(1).map(Number);if(v.some(x=>!Number.isFinite(x)))throw Error('Non-finite vertex');vertices.push(v)}}if(!vertices.length||vertices.length%3)throw Error('Incomplete triangles');const out=[];for(let i=0;i<vertices.length;i+=3)out.push(vertices.slice(i,i+3));return out}
function draw(name){const tris=triangles(source[name]),c=document.querySelector('#intro-'+name),r=c.getBoundingClientRect(),ratio=window.devicePixelRatio||1;c.width=r.width*ratio;c.height=r.height*ratio;const ctx=c.getContext('2d');ctx.scale(ratio,ratio);const w=r.width,h=r.height,scale=Math.min((w-100)/40,(h-100)/5),cx=w/2,cy=h/2;ctx.fillStyle='#fffdf8';ctx.fillRect(0,0,w,h);ctx.strokeStyle='#eee9df';ctx.lineWidth=1;for(let x=45;x<w-40;x+=45){ctx.beginPath();ctx.moveTo(x,50);ctx.lineTo(x,h-50);ctx.stroke()}for(let y=55;y<h-45;y+=45){ctx.beginPath();ctx.moveTo(35,y);ctx.lineTo(w-35,y);ctx.stroke()}const faces=tris.map(t=>({t,depth:t.reduce((s,v)=>s+v[1],0)/3})).sort((a,b)=>a.depth-b.depth);for(const{t,depth}of faces){ctx.beginPath();t.forEach((v,i)=>ctx[i?'lineTo':'moveTo'](cx+v[0]*scale,cy-(v[2]-2.5)*scale));ctx.closePath();const light=.72+.16*(depth+20)/40;ctx.fillStyle=`rgb(${Math.round(35*light)},${Math.round(123*light)},${Math.round(120*light)})`;ctx.fill();ctx.strokeStyle='rgba(255,253,248,.28)';ctx.lineWidth=.6;ctx.stroke()}c.dataset.renderedTriangles=String(tris.length);evidence.models[name]={actual_triangle_count:tris.length};window.introEvidence=evidence;document.documentElement.dataset.ready='true'}
draw('ring');draw('filled');window.addEventListener('resize',()=>{draw('ring');draw('filled')});
</script></body></html>'''
assert page.count('__ACTUAL_INPUTS__') == 1
(BASE / 'intro.html').write_text(page.replace('__ACTUAL_INPUTS__', json.dumps(inputs, ensure_ascii=False).replace('<', '\\u003c')))
print('Built the neutral side-view page from the two actual original STL files.')
