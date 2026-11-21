from pathlib import Path
import ast,copy,hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE/'history/r6'
REPO=HERE.parents[3]
AUDIT=Path('/workspace/work/brand-story-20261025/c10-audit')
ROOT=Path('/workspace/work/brand-story-20261025/c10-submission-root')
MEDIA=AUDIT/'r7-prepared-media'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
jread=lambda p:json.loads(Path(p).read_text())
def writej(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
protection=jread(AUDIT/'r7-protected-before.json')
for p,h in protection['protected_files'].items():assert sha(p)==h,p
old=jread(BASE/'video.json');oldn=jread(BASE/'narration-only.json');oldclaims=jread(BASE/'claims.json')
changes={
'c10v5s04':('削皮器用鏈條拴在碗上，讓走進店裡的人直接試。','開場預告的黑柄試用，就在這裡：削皮器用鏈條拴在胡蘿蔔碗上，讓進店的人伸手試。'),
'c10l20':('如果是你，會替家裡哪件小工具換掉握的地方？留言告訴我，卡住的是哪個動作。','也請你留言分享，想替家裡哪件小工具換個握柄，以及最卡手的那個動作。')}
newemotion='自然邀請觀眾分享，不上揚追問，不拉長停頓'
doc=copy.deepcopy(old)
for sc in doc['scenes']:
 for line in sc.get('lines',[]):
  if line['id'] in changes:
   before,after=changes[line['id']];assert line['text']==before;line['text']=after
   if line['id']=='c10l20':line['emotion']=newemotion
writej('video.json',doc)
assert doc['scenes'][:9]==old['scenes'][:9]
assert doc['loops']==old['loops']
for before,after in zip(old['scenes'],doc['scenes']):
 expected=copy.deepcopy(before)
 for line in expected.get('lines',[]):
  if line['id'] in changes:
   line['text']=changes[line['id']][1]
   if line['id']=='c10l20':line['emotion']=newemotion
 assert after==expected
narration=copy.deepcopy(oldn)
for line in narration:
 if line['id'] in changes:assert line['text']==changes[line['id']][0];line['text']=changes[line['id']][1]
writej('narration-only.json',narration)
claims=copy.deepcopy(oldclaims)
for row in claims['claims']:
 if row['line_id'] in changes:
  assert row['text']==changes[row['line_id']][0];row['text']=changes[row['line_id']][1]
  row['limits']+=['開場回叫同一次店內試用，不宣稱黏土原型、展會樣品與零售工具為同一實體；不增添精確日期／店址、逐人結果或量化銷售。' if row['line_id']=='c10v5s04' else '明確邀請觀眾分享工具與卡手動作，不是要求故事另交答案的事實懸念。']
for before,after in zip(oldclaims['claims'],claims['claims']):
 if before['line_id'] not in changes:assert before==after
script=(BASE/'script.md').read_text().replace('# C10 OXO｜R6 作者附來源稿','# C10 OXO｜R7 作者附來源稿',1)
md=(BASE/'claims.md').read_text().replace('# C10 OXO｜R6 作者逐句來源錨點','# C10 OXO｜R7 作者逐句來源錨點',1)
for lid,(before,after) in changes.items():
 row=next(r for r in claims['claims'] if r['line_id']==lid)
 oldrow=next(l for l in script.splitlines() if l.startswith('| '+lid+' | '));newrow='| '+lid+' | '+after+' | '+', '.join(row['material_refs'])+'；'+row['kind']+' |';script=script.replace(oldrow,newrow,1)
 oldrow=next(l for l in md.splitlines() if l.startswith('| '+lid+' | '));newrow='| '+lid+' | '+row['kind']+' | '+', '.join(row['material_refs'])+' | '+'；'.join(dict.fromkeys(row['limits']))+' |';md=md.replace(oldrow,newrow,1)
(HERE/'script.md').write_text(script);(HERE/'claims.md').write_text(md)
claims.update(revision='r7',scope='R7 author two-line callback/CTA correction only; new independent source/written-visual and actual native panel6 pending',input_sha256={n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json']},r6_input_sha256=protection['r6_input_sha256'],source_qa=False,visual_qa=False)
writej('claims.json',claims)
assert (HERE/'series.json').read_bytes()==(BASE/'series.json').read_bytes()
brief=(BASE/'brief.md').read_text().replace('# C10 OXO｜R6 修訂作者候選','# C10 OXO｜R7 修訂作者候選',1).replace('保留R5開場九句及主體，僅將c10o11窄成原型先交給哪些人試用的問題。','保留R6開場九句、c10o11原型試用群體問題及主體，僅明確回叫開場黑柄預告，並將觀眾結尾改成直接分享邀請。',1)
marker='本版R6只修c10o11';assert marker in brief
brief=brief[:brief.index(marker)]+'''本版R7只改c10v5s04的開場黑柄回叫及c10l20的觀眾分享邀請。待新的獨立來源／書面配鏡與actual native panel6（round-6-r7）。R6來源／書面配鏡PASS與actual panel5的payoffs HOLD已完整封存history/r6，只綁R6，不批准R7。R4僅prepared-only，未冒充actual panel。無verify或owner批准；無provider、backend、Git、付費、音訊、圖片、影片與翻譯。

## R6 → R7 定點修正

Lechters試用段沿用同一次零售故事，在c10v5s04直接回叫開場預告的黑柄試用，再交出鏈條拴胡蘿蔔碗、進店者伸手試的新動作。不把黏土原型、展會樣品、零售削皮器說成同一實體，不另造第二次試用。保留Stowell晚近回憶歸屬、慢銷與試用後結果的原有界線。

結尾c10l20直接邀請你分享想換握柄的工具及卡手動作，不懸置應由本故事回答的新問題。其他116句、開場九句、R6的c10o11及其公眾試原型答案、章序、27組loop、全部115景prompt和camera不變；只有該CTA情緒改為自然邀請，不靠問句上揚。單人no_recap保留，不為rough3500填長。實聲時長未知。
'''
(HERE/'brief.md').write_text(brief)
assert not (HERE/'verify-1.md').exists()
row=next(r for r in claims['claims'] if r['line_id']=='c10v5s04');records={r['id']:r for r in claims['source_records']}
for ev in row['evidence']:
 assert sha(records[ev['source']]['path'])==ev['source_bytes_sha256']
 assert sha(ev['readable_cache_path'])==ev['readable_cache_sha256']
 assert ev['short_excerpt'] in Path(ev['readable_cache_path']).read_text()
target=ROOT/'docs/videos'/doc['slug'];assert not (target/'verify-1.md').exists()
prep=subprocess.run(['node',str(HERE.parent/'prepare-runtime.mjs'),str(ROOT),str(MEDIA),'c10'],cwd=REPO,capture_output=True,text=True)
if prep.returncode:raise RuntimeError(prep.stderr)
(AUDIT/'r7-prepare-runtime.txt').write_text(prep.stdout+prep.stderr)
tree=ast.parse((HERE/'history/r5/build-candidate.py').read_text());code=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='code' for t in n.targets));code=code.replace('R5 author native mechanical preflight only','R7 author native mechanical preflight only')
run=subprocess.run(['node','--input-type=module','-e',code,str(HERE),str(ROOT)],cwd=REPO,capture_output=True,text=True)
if run.returncode:raise RuntimeError(run.stderr)
result=json.loads(run.stdout);writej('native-author-lint-r7.json',result)
assert not result['lint']['errors'],result['lint']['errors']
assert result['cadence_warning_count']==0,result['lint']['warnings']
assert result['maximum_estimated_shot_seconds']<=12
assert all(c['you'] and c['i'] for c in result['chapter_viewer_counts'])
assert result['lines']==118 and result['scenes']==116 and result['illustration_scenes']==115
for p,h in protection['protected_files'].items():assert sha(p)==h,p
notes={'status':'HOLD_PENDING_NEW_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_ACTUAL_NATIVE_PANEL6','revision':'r7','author':'/root/c10_r7_author','scope':'two-line explicit opening callback and direct viewer-share invitation only; other facts/order, all visuals and loops unchanged','input_sha256':{n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json','claims.json']},'r6_input_sha256':protection['r6_input_sha256'],'delta_from_r6':{'changed_narration':[{'id':lid,'before':v[0],'after':v[1]} for lid,v in changes.items()],'added_narration':[],'deleted_narration':[],'changed_emotion':[{'id':'c10l20','before':'好奇上揚，不拉長停頓','after':newemotion}],'other_116_narration_and_claim_objects_unchanged':True,'opening_nine_scenes_unchanged':True,'r6_o11_and_its_answer_unchanged':True,'scene_order_and_chapter_markers_unchanged':True,'all_prompts_cameras_and_other_scene_data_unchanged':True,'all_27_loops_unchanged':True,'series_context_byte_identical':True,'net_whole_units_planning':result['native_units']['total']-2658},'narration_plan':result['native_units'],'duration_body_definition':'Whole unbranded narration includes cold open and voiced CTA; only added formal 5s intro / 21s outro excluded. after-opening/strict are auxiliary planning breakdowns.','planning_note':'rough3500不填長；實聲720–840秒及需補多少未知，原生估時不能當時長PASS或已知不足。','actual_narration_seconds':None,'actual_required_extra_units':None,'native_mechanical':{k:v for k,v in result.items() if k!='shot_times'},'native_lint_receipt_sha256':sha(HERE/'native-author-lint-r7.json'),'protected_files':{'count':len(protection['protected_files']),'all_unchanged':True,'manifest_path':str(AUDIT/'r7-protected-before.json'),'manifest_sha256':sha(AUDIT/'r7-protected-before.json')},'runtime':{'c10_only_offline_preparation':True,'source_equals_runtime':True,'immutable_dictionary_changed':False,'current_verify_absent':not (target/'verify-1.md').exists(),'approvals_created':0},'independent_source_pass':False,'independent_visual_pass':False,'native_narrative_pass':False,'verify_written':False,'owner_approval':False,'actual_panel_round_next':6,'actual_panel_audit_name':'round-6-r7','last_actual_panel':'R6 actual panel5, archived history/r6','source_or_media_eligibility':False,'translations_created':False,'provider_calls':0,'backend_writes':0,'generated_media':0,'git_actions':0}
writej('author-notes.json',notes)
freeze={'kind':'R7_AUTHOR_FREEZE_ONLY_NO_APPROVAL','four_sha256':notes['input_sha256'],'all_current_author_outputs_sha256':{n:sha(HERE/n) for n in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','author-notes.json','build-candidate.py','native-author-lint-r7.json']},'r6_input_sha256':protection['r6_input_sha256'],'delta':notes['delta_from_r6'],'whole_body_spoken_units_planning':result['native_units']['total'],'native_mechanical':{'errors':len(result['lint']['errors']),'cadence_warnings':result['cadence_warning_count'],'max_estimated_shot_seconds':result['maximum_estimated_shot_seconds'],'other_warnings':result['lint']['warnings']},'runtime_official_script_sha256':sha(target/'script.md'),'runtime_manifest_sha256':sha(ROOT/'runtime-manifest.json'),'protected_count':len(protection['protected_files']),'protected_all_unchanged':True,'actual_audio_duration_seconds':None,'actual_next_panel_round':6,'actual_next_panel_audit_name':'round-6-r7','independent_approval':False,'provider_calls':0,'backend_writes':0,'git_actions':0,'status':notes['status']}
(AUDIT/'r7-author-freeze.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':notes['status'],'four_sha256':notes['input_sha256'],'units':result['native_units'],'changes':notes['delta_from_r6']['changed_narration'],'errors':result['lint']['errors'],'cadence_warnings':result['cadence_warning_count'],'max_shot':result['maximum_estimated_shot_seconds'],'other_warnings':result['lint']['warnings'],'protected_unchanged':len(protection['protected_files'])},ensure_ascii=False,indent=2))
