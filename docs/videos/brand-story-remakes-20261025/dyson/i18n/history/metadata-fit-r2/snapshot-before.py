from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
w=Path('/workspace/work/brand-story-20261025/dyson-audit/text-r5');a=w/'metadata-fit-r2';c=json.loads((w/'text-current.json').read_text());b=Path('/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/dyson');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
assert not (a/'before-inventory.json').exists()
for loc in ['es','pt','id','vi','th']:
 sheet=Path(c['media'])/c['slug']/'i18n'/f'{loc}.todo.json';native=Path(c['root'])/'docs/videos'/c['slug']/'i18n'/f'{loc}.json';target=a/'before'/loc;target.mkdir(parents=True)
 for original,name in [(sheet,'worksheet.todo.json'),(native,'native.json')]:
  shutil.copyfile(original,target/name);assert original.read_bytes()==(target/name).read_bytes()
 rows.append({'locale':loc,'worksheet':str(sheet),'worksheet_sha256':h(sheet),'worksheet_snapshot':str(target/'worksheet.todo.json'),'native':str(native),'native_sha256':h(native),'native_snapshot':str(target/'native.json')})
files=list(w.glob('*.json'))+list((w/'translation-source-sheets').glob('*.json'))+[b/x for x in ['video.json','script.md','claims.json','claims.md','series.json','brief.md','image-reuse-plan.json','author-freeze-r5.json','operator-freeze-r5.json']]
files+=list((Path(c['root'])/'docs/videos'/c['slug']/'i18n').glob('*.json'))
protected={str(p):h(p) for p in files}
out={'schema_version':1,'captured_at':datetime.now(timezone.utc).isoformat(),'scope':'Actual current root-reviewed worksheet and native bytes before five metadata-only author changes; not the original author submission.','source_video_sha256':c['source_video_sha256'],'locales':rows,'protected_files_sha256':protected}
(a/'before-inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'snapshots':len(rows)*2,'protected_files':len(protected),'inventory_sha256':h(a/'before-inventory.json')}))
