from pathlib import Path
import json,copy,hashlib,subprocess,re,ast
HERE=Path(__file__).resolve().parent
BASE=HERE/'history/r5'
REPO=HERE.parents[3]
AUDIT=Path('/workspace/work/brand-story-20261025/c10-audit')
ROOT=Path('/workspace/work/brand-story-20261025/c10-submission-root')
MEDIA=AUDIT/'r6-prepared-media'
SLUG='story-everyday-oxo-c10-remake-20261025'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
jread=lambda p:json.loads(Path(p).read_text())
def writej(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
protection=jread(AUDIT/'r6-protected-before.json')
for p,h in protection['protected_files'].items():assert sha(p)==h,p
assert {n:sha(BASE/n) for n in protection['r5_input_sha256']}==protection['r5_input_sha256']
old=jread(BASE/'video.json');oldclaims=jread(BASE/'claims.json');oldn=jread(BASE/'narration-only.json')
oldtext='我會想把它交給第二個人：同一個捏好的形狀，換隻手還合嗎？'
newtext='我想知道，原型先交到哪些人的手裡試？'
newprompt='Medium shot of several unmarked handle prototypes on a shared workbench, with anonymous hands approaching them for a trial.'
lid='c10o11'
doc=copy.deepcopy(old)
scene=next(s for s in doc['scenes'] if any(l['id']==lid for l in s['lines']))
assert len(scene['lines'])==1 and scene['lines'][0]['text']==oldtext
oldprompt=scene['data']['prompt']
scene['lines'][0]['text']=newtext;scene['data']['prompt']=newprompt
loop=next(l for l in doc['loops'] if l['setup']==lid)
oldloop=copy.deepcopy(loop)
assert loop['payoff']=='c10o14'
loop.update(payoff='c10v5o01',what='原型先交到哪些使用者手裡試用')
writej('video.json',doc)
# Every other scene, line, position, chapter, camera, prompt and the 39 R5 source facts stay unchanged.
for before,after in zip(old['scenes'],doc['scenes']):
 if before['id']!=scene['id']:assert before==after
 else:
  expected=copy.deepcopy(before);expected['lines'][0]['text']=newtext;expected['data']['prompt']=newprompt
  assert after==expected
assert doc['scenes'][:9]==old['scenes'][:9]
assert [s['id'] for s in doc['scenes']]==[s['id'] for s in old['scenes']]
assert [{**l,'payoff':oldloop['payoff'],'what':oldloop['what']} if l['setup']==lid else l for l in doc['loops']]==old['loops']
narration=copy.deepcopy(oldn)
for n in narration:
 if n['id']==lid:assert n['text']==oldtext;n['text']=newtext
writej('narration-only.json',narration)
claims=copy.deepcopy(oldclaims)
row=next(r for r in claims['claims'] if r['line_id']==lid)
answer=next(r for r in oldclaims['claims'] if r['line_id']=='c10v5o01')
row['text']=newtext;row['material_refs']=copy.deepcopy(answer['material_refs']);row['evidence']=copy.deepcopy(answer['evidence']);row['limits']=copy.deepcopy(answer['limits'])+['本句只問原型曾交給哪些群體試用；不宣稱同一塊黏土適合所有手，不承諾試用成效或精確受試者／模型數。']
row['evidence'][0]['short_excerpt']='including chefs, cooks, general kitchen utensil users, New York arthritis groups'
row['written_visual']['prompt']=newprompt
assert row['kind']=='opinion' and row['independent_verdict']=='NOT_REVIEWED'
for before,after in zip(oldclaims['claims'],claims['claims']):
 if before['line_id']!=lid:assert before==after
assert all(before==after for before,after in zip(oldclaims['claims'],claims['claims']) if before['line_id'].startswith('c10v5'))
script=(BASE/'script.md').read_text().replace('# C10 OXO｜R5 作者附來源稿','# C10 OXO｜R6 作者附來源稿',1)
oldrow=next(l for l in script.splitlines() if l.startswith('| '+lid+' | '))
newrow='| '+lid+' | '+newtext+' | '+', '.join(row['material_refs'])+'；'+row['kind']+' |'
script=script.replace(oldrow,newrow,1)
(HERE/'script.md').write_text(script)
claims.update(revision='r6',scope='R6 author single-question and matching visual/loop/anchor correction only; new independent source/written-visual and actual native panel5 pending',input_sha256={n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json']},r5_input_sha256=protection['r5_input_sha256'],source_qa=False,visual_qa=False)
writej('claims.json',claims)
md=(BASE/'claims.md').read_text().replace('# C10 OXO｜R5 作者逐句來源錨點','# C10 OXO｜R6 作者逐句來源錨點',1)
oldmd=next(l for l in md.splitlines() if l.startswith('| '+lid+' | '))
newmd='| '+lid+' | '+row['kind']+' | '+', '.join(row['material_refs'])+' | '+'；'.join(dict.fromkeys(row['limits']))+' |'
(HERE/'claims.md').write_text(md.replace(oldmd,newmd,1))
# Keep planning context byte-identical; do not bind an original episode in the video document.
assert (HERE/'series.json').read_bytes()==(BASE/'series.json').read_bytes()
brief=(BASE/'brief.md').read_text().replace('# C10 OXO｜R5 修訂作者候選','# C10 OXO｜R6 修訂作者候選',1)
brief=brief.replace('保留R4已合併開場九句及去重核心。','保留R5開場九句及主體，僅將c10o11窄成原型先交給哪些人試用的問題。',1)
marker='本版HOLD待新的獨立來源／書面配鏡、actual native panel4'
assert marker in brief
brief=brief[:brief.index(marker)]+'''本版R6只修c10o11及對應loop／prompt／anchor，HOLD待新的獨立來源／書面配鏡與actual native panel5（round-5-r6）。R5來源／書面配鏡收據與actual native panel4保留history/r5，只綁R5輸入，不自動批准R6。R4僅prepared-only，未冒充actual panel。沒有verify、SOURCE／敘事／visual PASS或owner批准。無provider、backend、Git、付費、音訊、圖片、影片與翻譯。

## R5 → R6 定點修正

刪去同一個捏好形狀換手是否仍合的承諾，改問原型先交到哪些人的手裡試。保持原敘述順序，將loop payoff由c10o14的訪談群體改綁c10v5o01的真試用群體列舉；該答案位於c10o20之後，並非緊接c10o11。只把c10o11概念圖改成多個未標示原型等待匿名使用者試，不再畫同一塊黏土在兩隻不同大小的手間傳遞。來源綁教師包原件的公眾試原型段，不聲稱普適性、臨床效果或精確測試人數。其他117句、39項R5新增句、開場九句、所有其他景及章序不變；c10a03 lone no_recap不追，不為rough3500填長。實聲時長未知。
'''
(HERE/'brief.md').write_text(brief)
assert not (HERE/'verify-1.md').exists()
# Actual bytes and quote selfcheck only, not an independent source verdict.
records={x['id']:x for x in claims['source_records']}
for ev in row['evidence']:
 assert sha(ev['readable_cache_path'])==ev['readable_cache_sha256']
 assert sha(records[ev['source']]['path'])==ev['source_bytes_sha256']
 normal=lambda s:re.sub(r'\s','',s).lower()
 assert normal(ev['short_excerpt']) in normal(Path(ev['readable_cache_path']).read_text())
# Preserve existing runtime bytes before ordinary c10-only offline preparation.
target=ROOT/'docs/videos'/SLUG
archive=AUDIT/'r6-runtime-before';archive.mkdir(exist_ok=True)
snapshot=AUDIT/'r6-runtime-before.json'
if snapshot.exists():
 runtime_before=jread(snapshot)
 for p,h in runtime_before.items():assert sha(archive/Path(p).relative_to(target))==h
else:
 runtime_before={}
 for p in target.rglob('*'):
  if p.is_file():
   runtime_before[str(p)]=sha(p);dest=archive/p.relative_to(target);dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();dest.write_bytes(p.read_bytes())
 snapshot.write_text(json.dumps(runtime_before,indent=2)+'\n')
oldverify=target/'verify-1.md'
if oldverify.exists():
 assert (archive/'verify-1.md').read_bytes()==oldverify.read_bytes();oldverify.unlink()
prep=subprocess.run(['node',str(HERE.parent/'prepare-runtime.mjs'),str(ROOT),str(MEDIA),'c10'],cwd=REPO,capture_output=True,text=True)
if prep.returncode:raise RuntimeError(prep.stderr)
(AUDIT/'r6-prepare-runtime.txt').write_text(prep.stdout+prep.stderr)
# Reuse the exact native mechanical adapter, not the old author's build or any reader verdict.
tree=ast.parse((BASE/'build-candidate.py').read_text())
code=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='code' for t in n.targets))
code=code.replace('R5 author native mechanical preflight only','R6 author native mechanical preflight only')
run=subprocess.run(['node','--input-type=module','-e',code,str(HERE),str(ROOT)],cwd=REPO,capture_output=True,text=True)
if run.returncode:raise RuntimeError(run.stderr)
result=json.loads(run.stdout)
writej('native-author-lint-r6.json',result)
assert not result['lint']['errors'],result['lint']['errors']
assert result['cadence_warning_count']==0,result['lint']['warnings']
assert result['maximum_estimated_shot_seconds']<=12
assert all(c['you'] and c['i'] for c in result['chapter_viewer_counts'])
assert result['lines']==118 and result['scenes']==116
for p,h in protection['protected_files'].items():assert sha(p)==h,p
new_byid={n['id']:n for n in narration}
assert {n['id'] for n in oldn if n!=new_byid[n['id']]}=={lid}
notes={'status':'HOLD_PENDING_NEW_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_ACTUAL_NATIVE_PANEL5','revision':'r6','author':'/root/c06_translate_en_ja','scope':'one question plus matching source anchor, conceptual prompt and declared loop target; all other story facts and ordering unchanged','input_sha256':{n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json','claims.json']},'r5_input_sha256':protection['r5_input_sha256'],'r5_history_receipts_sha256':protection['r5_history_receipts_sha256'],'delta_from_r5':{'changed_narration':[{'id':lid,'before':oldtext,'after':newtext,'reason':'將同一捏好形狀能否普適的未回答承諾，窄成原型交給哪些人試用，後者有教師包原件及現有v5o01列舉。'}],'added_narration':[],'deleted_narration':[],'changed_scene_data':[{'scene':scene['id'],'field':'prompt','before':oldprompt,'after':newprompt,'reason':'移除同一黏土握柄傳給不同大小手的暗示，改為原型與待試匿名手。'}],'changed_loop':{'before':oldloop,'after':loop,'reason':'c10o14描述問使用者，v5o01才實述原型交給公眾試用。'},'changed_claim_targets':[lid],'other_117_line_and_claim_objects_unchanged':True,'r5_new_39_line_and_claim_objects_unchanged':True,'opening_nine_scenes_unchanged':True,'scene_order_and_chapter_markers_unchanged':True,'other_prompts_cameras_and_scene_data_unchanged':True,'series_context_byte_identical':True,'lone_no_recap_c10a03_not_changed':True,'net_whole_units_planning':result['native_units']['total']-2667},'narration_plan':result['native_units'],'duration_body_definition':'Whole unbranded narration includes cold open and voiced CTA; only added formal 5s intro / 21s outro excluded. after-opening/strict are auxiliary planning breakdowns.','planning_note':'rough3500不填長；本次只窄承諾，實聲720–840秒及需補多少未知，原生估時不能當時長PASS或已知不足。','actual_narration_seconds':None,'actual_required_extra_units':None,'native_mechanical':{k:v for k,v in result.items() if k!='shot_times'},'native_lint_receipt_sha256':sha(HERE/'native-author-lint-r6.json'),'protected_files':{'count':len(protection['protected_files']),'all_unchanged':True,'manifest_path':str(AUDIT/'r6-protected-before.json'),'manifest_sha256':sha(AUDIT/'r6-protected-before.json')},'runtime':{'c10_only_offline_preparation':True,'source_equals_runtime':True,'immutable_dictionary_changed':False,'current_verify_absent':not (target/'verify-1.md').exists(),'approvals_created':0},'independent_source_pass':False,'independent_visual_pass':False,'native_narrative_pass':False,'verify_written':False,'owner_approval':False,'actual_panel_round_next':5,'actual_panel_audit_name':'round-5-r6','last_actual_panel':'R5 actual panel4, archived history/r5','source_or_media_eligibility':False,'translations_created':False,'provider_calls':0,'backend_writes':0,'generated_media':0,'git_actions':0}
writej('author-notes.json',notes)
freeze={'kind':'R6_AUTHOR_FREEZE_ONLY_NO_APPROVAL','four_sha256':notes['input_sha256'],'all_current_author_outputs_sha256':{n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','author-notes.json','build-candidate.py','native-author-lint-r6.json']},'r5_input_sha256':protection['r5_input_sha256'],'delta':notes['delta_from_r5'],'whole_body_spoken_units_planning':result['native_units']['total'],'native_mechanical':{'errors':len(result['lint']['errors']),'cadence_warnings':result['cadence_warning_count'],'max_estimated_shot_seconds':result['maximum_estimated_shot_seconds'],'other_warnings':result['lint']['warnings']},'runtime_official_script_sha256':sha(target/'script.md'),'immutable_dictionary_sha256':{str(p.relative_to(target)):sha(p) for p in (target/'story-lexicon').rglob('*') if p.is_file()},'runtime_manifest_sha256':sha(ROOT/'runtime-manifest.json'),'protected_count':len(protection['protected_files']),'protected_all_unchanged':True,'actual_audio_duration_seconds':None,'actual_next_panel_round':5,'actual_next_panel_audit_name':'round-5-r6','independent_approval':False,'provider_calls':0,'backend_writes':0,'git_actions':0,'status':notes['status']}
(AUDIT/'r6-author-freeze.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':notes['status'],'four_sha256':notes['input_sha256'],'units':result['native_units'],'changed_line':{'id':lid,'before':oldtext,'after':newtext},'changed_loop':loop,'errors':result['lint']['errors'],'cadence_warnings':result['cadence_warning_count'],'max_shot':result['maximum_estimated_shot_seconds'],'other_warnings':result['lint']['warnings'],'protected_unchanged':len(protection['protected_files'])},ensure_ascii=False,indent=2))
