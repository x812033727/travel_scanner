"""Deterministic visual-only author rebuild from the preserved adopted narrative.
No runtime, media, backend, approval, dictionary or Git operation is performed.
"""
from pathlib import Path
import copy,hashlib,json
HERE=Path(__file__).resolve().parent
BASE=HERE/'history/before-teaser-image-plan'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
spec=read(HERE/'teaser-visual-spec.json')
manifest=read(BASE/'snapshot-manifest.json')
for name,h in manifest['files_sha256'].items():assert sha(BASE/name)==h,name
assert sha(BASE/'video.json')==spec['baseline_video_sha256']
assert not (HERE/'verify-1.md').exists(),'Current independent verification exists; reconcile before rebuilding author input.'
old=read(BASE/'video.json');doc=copy.deepcopy(old)
by_scene={s['id']:s for s in doc['scenes']}
by_line={l['id']:s for s in doc['scenes'] for l in s.get('lines',[])}
for pair in spec['pairs']:
 for side in ['setup','payoff']:
  sid=pair[side+'_scene_id'];lid=pair[side+'_line_id'];sc=by_scene[sid]
  assert by_line[lid]['id']==sid
  assert sc['template']=='shot' and sc['data'].get('visual')=='still'
  sc['data']['prompt']=pair['prompt'];sc['data']['camera']=pair['camera']
compare=copy.deepcopy(doc)
for pair in spec['pairs']:
 for sid in [pair['setup_scene_id'],pair['payoff_scene_id']]:
  before=next(s for s in old['scenes'] if s['id']==sid);now=next(s for s in compare['scenes'] if s['id']==sid)
  now['data']['prompt']=before['data']['prompt'];now['data']['camera']=before['data']['camera']
assert compare==old
(HERE/'video.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
# The existing narration projection is copied byte-for-byte, not reconstructed.
(HERE/'narration-only.json').write_bytes((BASE/'narration-only.json').read_bytes())
append=['','## 開場共圖製作註解（非旁白、非實圖驗收）','',
'本段只記錄素材規劃，不加入有聲劇本。所有旁白、scene／line IDs、章序、情緒、loops與metadata均不變。現有來源PASS只屬封存輸入，新圖像prompt／camera須由獨立來源與書面分鏡查核。','']
for pair in spec['pairs']:
 append += [f"- `{pair['setup_scene_id']}` ↔ `{pair['payoff_scene_id']}`：同一張已驗still，兩端同prompt與camera。",f"  - English prompt: {pair['prompt']}",f"  - Camera: {pair['camera']}",f"  - Boundaries: {pair['source_scope']}",f"  - Opening: {pair['no_result_drawn_in_teaser']}"]
append += ['','實檔尚不存在；詳見 `image-reuse-plan.json`。正式操作前先核既有payoff快取與實檔SHA，快取缺失就停，不能用第二次派送當快取探測。兩端仍各需judge，任何retake／裁切後須再核最終manifest與實檔SHA完全相同。不得以兩張近似圖代替同一資產。','']
append='\n'.join(append)
for name in ['script.md','claims.md']:(HERE/name).write_text((BASE/name).read_text()+append)
claims=copy.deepcopy(read(BASE/'claims.json'))
rows=claims if isinstance(claims,list) else claims[spec.get('claims_collection_key','claims')]
for pair in spec['pairs']:
 for side in ['setup','payoff']:
  lid=pair[side+'_line_id'];row=next(r for r in rows if r.get('line_id',r.get('id'))==lid)
  w=row.setdefault('written_visual',{})
  w.update(conceptual=True,not_historical_reconstruction=True,prompt=pair['prompt'],camera=pair['camera'],narration_binding=lid,teaser_same_asset_plan={'file':'image-reuse-plan.json','pair_id':pair['pair_id'],'setup_scene_id':pair['setup_scene_id'],'payoff_scene_id':pair['payoff_scene_id'],'actual_same_asset_verified':False})
if isinstance(claims,dict) and spec.get('claims_collection_key')!='narration_claims':
 claims['revision']=spec['revision']
 claims['scope']='Visual-only teaser/shared-still plan. Existing facts and every narrative field are unchanged; independent source/written-visual review pending, not an actual asset manifest or approval.'
 claims['input_sha256']={n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json']}
 claims['source_qa']=False;claims['visual_qa']=False
(HERE/'claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'VISUAL_ONLY_AUTHOR_OUTPUTS_PENDING_INDEPENDENT_REVIEW','core_four_sha256':{n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json','claims.json']},'runtime_writes':0,'provider_calls':0,'backend_calls':0,'git_actions':0},ensure_ascii=False))
