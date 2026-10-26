import pathlib,json
out=pathlib.Path('/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/dyson');audit=pathlib.Path('/workspace/work/brand-story-20261025/dyson-audit/author-r4');p=out/'author-rows.json';r=json.loads(p.read_text());idmap=json.loads((out/'native-id-map.json').read_text())
# Native story schema permits5–7chapters; one connected origin chapter covers factory and household tests.
for x in r:
 if x['chapter'] in {'工廠的布濾先堵住了','袋子倒空，仍然吸不動'}:x['chapter']='布濾堵住，家裡的空袋也吸不動'
x=next(x for x in r if x['text']=='所以日本之前，已經有商品和跨國製造，不能說所有人都不肯接。');x['text']='日本之前已經有商品；Apex這次，又是怎麼找到戴森的？';x['kind']='question';x['research_claim_ids']=['D01','D02','D07']
i=next(i for i,x in enumerate(r) if x['text'].startswith('那份訪談研究也指出'))
ids=(audit/'native-fresh-ids.txt').read_text().split();newid=next(x for x in ids if x not in {r['id'] for r in r});struct='dyr4qlicense';idmap[struct]=newid
r.insert(i+1,{'id':newid,'chapter':r[i]['chapter'],'text':'真的有人接下授權，把後面的生產做出來了嗎？','kind':'question','research_claim_ids':['D01','N05'],'visual':'cyclon','author_structural_reference':struct})
x=next(x for x in r if x['text'].startswith('你會以為能上架'));x['text']='你會以為能上架就會大賣嗎？我想問，這回究竟是多大一門生意？'
x=next(x for x in r if x['text'].startswith('公司另有一張標作'));x['text']='公司另有一張標作一九九三年的產線照，留下的是哪個現場？';x['kind']='question'
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(out/'native-id-map.json').write_text(json.dumps(idmap,indent=2)+'\n')
b=out/'build-candidate.mjs';s=b.read_text().replace('chapters:8,loops:',"chapters:[...new Set(rows.map(r=>r.chapter))].length,loops:")
s=s.replace("const loopDefs=[", "const loopDefs=[\n[findText('真的有人接下'),findText('後來，英國一家'),'英國獲授權廠商做出Cyclon'],[findText('日本之前已經有商品'),'kget','Apex社長看到設計照片而聯絡'],[findText('公司另有一張標作'),'i6fq','另一份1993產線圖說指向BumpersFarm'],")
b.write_text(s)
