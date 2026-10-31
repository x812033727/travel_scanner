#!/usr/bin/env python3
"""R4 single-line author delta and byte-integrity freeze; no review or production verdict."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=Path('/workspace/work/brand-story-20261025/doraemon-audit/author-r4')
HISTORY=HERE/'history/r3'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
protected=read(AUDIT/'protected-before-r4.json')
for f in protected['protected213']:assert sha(f['path'])==f['sha256'],f['path']
for name,w in protected['previous_external_files'].items():assert sha(name)==w,name
for rev in ['r1','r2','r3']:
    hist=HERE/'history'/rev;m=read(hist/'history-manifest.json')
    for name,w in m['files_sha256'].items():assert sha(hist/name)==w,f'{rev}/{name}'
assert sha(HISTORY/'history-manifest.json')==protected['r3_history_manifest_sha256']
for name in ['source-r1-independent.json','source-r2-independent.json','source-r3-independent.json','narrative-r1-a.raw.json','narrative-r1-b.raw.json','narrative-r1-input.json','narrative-r1-binding.json','narrative-r1.json','narrative-r2-a.raw.json','narrative-r2-b.raw.json','narrative-r2-input.json','narrative-r2-binding.json','narrative-r2.json']:
    assert sha(HERE/'reviews'/name)==sha(HISTORY/'reviews'/name),name
assert sha(HISTORY/'reviews/source-r3-independent.json')==protected['r3_source_pass_sha256']
assert sha(HISTORY/'verify-1.md')==protected['r3_verify_sha256']
assert not (HERE/'verify-1.md').exists(),'R3 verify must remain historical, not approve R4.'
merged=read(HISTORY/'reviews/narrative-r2.json')
assert merged['round']==2 and merged['passed'] is False and merged['failed']==['payoffs']
outputs=['video.json','script.md','narration-only.json','claims.json','claims.md','series.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','image-reuse-plan.json']
prior={n:sha(HERE/n) for n in outputs}
subprocess.run(['python',str(HERE/'build-candidate.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['node',str(HERE/'build-image-reuse-plan.mjs')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
assert {n:sha(HERE/n) for n in outputs}==prior,'Author replay drift.'
old=read(HISTORY/'video.json');doc=read(HERE/'video.json');oldn=read(HISTORY/'narration-only.json');n=read(HERE/'narration-only.json');oldc=read(HISTORY/'claims.json');c=read(HERE/'claims.json')
oldtext='辻村記得，大家要一起找：月球上哪裡還有生命能介入的餘地？'
newtext='辻村回顧，那次會議用科學資料討論設定；結果，寫腳本還是遇到困難。'
oldwhat='五、六本科學雜誌帶來的寫作問題'
newwhat='科學資料被帶進哪個寫作步驟'
changed=[]
for s in old['scenes']:
    for l in s['lines']:
        if l['id']=='d1b082':assert l['text']==oldtext;l['text']=newtext;changed.append(l['id'])
for loop in old['loops']:
    if loop['setup']=='d1h042':assert loop['what']==oldwhat;loop['what']=newwhat
assert changed==['d1b082'] and old==doc,'Video changes exceed one text leaf and one loop description.'
for l in oldn:
    if l['id']=='d1b082':l['text']=newtext
assert oldn==n,'Other134 spoken lines changed.'
oldcm={l['id']:l for l in oldc['lines']}
for line in c['lines']:
    if line['id']!='d1b082':assert line==oldcm[line['id']],line['id']
assert c['written_visuals']==oldc['written_visuals'] and c['unvoiced_background']==oldc['unvoiced_background']
newclaim=next(l for l in c['lines'] if l['id']=='d1b082')
assert newclaim['text']==newtext and newclaim['source_anchors']==['D14','D15']
expected=(HISTORY/'script.md').read_text().replace('Doraemon remake｜R3作者稿','Doraemon remake｜R4作者稿').replace(oldtext,newtext)
assert expected==(HERE/'script.md').read_text()
for name in ['source-anchors-r1.json','series.json','row-index-r1.json','research-original.md','research-original.claims.json','original-preservation.json']:
    assert sha(HERE/name)==sha(HISTORY/name),name
plan=read(HERE/'image-reuse-plan.json');oldplan=read(HISTORY/'image-reuse-plan.json')
assert plan['pairs'][0]['requests']==oldplan['pairs'][0]['requests'] and not plan['actual_same_asset_verified']
core={name:sha(HERE/name) for name in ['video.json','script.md','narration-only.json','claims.json']}
assert plan['core_four_sha256']==core
lint=read(HERE/'native-author-lint-r4.json');checks=read(AUDIT/'free-checks-r4.json');notes=read(HERE/'producer-notes.json')
assert lint['errors']==[] and not [w for w in lint['warnings'] if w.get('kind')=='narrative']
assert checks['lint_exit_code']==checks['planner_exit_code']==0 and checks['network_attempts']==0 and checks['dictionary_initialized'] is False
assert lint['summary']['spoken_units']==notes['counts']['spoken_units_total']
for item in checks['dictionary_copies']:assert sha(item['source'])==sha(item['target'])==item['sha256']
state={'schema_version':1,'revision':'doraemon-r4','actualcount':2,'last_actual_native_round':2,'last_actual_native_result':'HOLD','last_actual_native_shared_required_holds':['payoffs'],'last_actual_native_binding':{'source_video_sha256':sha(HISTORY/'video.json'),'receipt_sha256':sha(HISTORY/'reviews/narrative-r2.json')},'current_candidate_native_state':'NOT_PREPARED_NOT_READ','next_fresh_round_if_root_starts_it':3,'r4_author_prepared_native_payloads':0,'r4_author_native_or_blind_calls':0,'source_r4_delta':'PENDING_OTHER_REVIEWER','r3_source_pass_is_historical_only':True,'verify_1_for_r4_exists':False,'owner_approval':False}
dump(HERE/'native-state.json',state)
changes={'schema_version':1,'revision':'doraemon-r4','role':'AUTHOR_DELTA_NOT_INDEPENDENT_REVIEW','previous_core_four_sha256':{name:sha(HISTORY/name) for name in core},'current_core_four_sha256':core,'line_changes':[{'id':'d1b082','old':oldtext,'new':newtext}],'other_spoken_lines_exact':134,'spoken_line_ids_order_and_count_exact':135,'all_115_scene_non_line_fields_exact':True,'removed_or_added_lines_or_scenes':[],
 'loop_delta':{'one_description_changed':{'setup':'d1h042','payoff':'d1b081','old':oldwhat,'new':newwhat},'all23_endpoints_and_other22_entries_exact':True},
 'claim_delta':'Only d1b082 text and its existing D15 evidence/limits mapping are updated, plus revision metadata. Other134 claim entries, written visuals and unvoiced background are exact.',
 'source_for_work_result':{'source_id':'MW2019A','text_lines_1based':[32,33],'quote_exact_short':'案の定、脚本づくりは難航したんですが','reading_scope':'Existing frozen raw participant interview only; no new download or film/science inspection.'},
 'payoff_scope':'The science books enter the first setting discussion; the participant then reports screenplay difficulty. The remaining b10 work question asks how to connect the original world to the new stage; c01 supplies the director existing-manga-device proposal and the participant stated writing response. No question about a lunar location/life remains in spoken text.',
 'not_chased':['A-only scene_first','B-only no_recap','chapter-name advisory'],'full_three_end_stage_requests_exact':True,'actual_same_asset_verified':False,
 'previous_source_pass_sha256':protected['r3_source_pass_sha256'],'previous_verify_sha256':protected['r3_verify_sha256'],'previous_true_native_round':2,'previous_true_native_shared_hold':['payoffs'],'all_old_review_tickets_unchanged':True,
 'source_r4_delta':'PENDING_OTHER_REVIEWER','fresh_native3':'PENDING_ROOT_NOT_PREPARED_BY_AUTHOR','actual_native_rounds_total':2,'capacity':{'before_units':3101,'after_units':notes['counts']['spoken_units_total'],'target_minutes':13,'required_measured_body_seconds':[720,840],'pure_arithmetic_seconds_at_4_5':notes['counts']['estimated_speech_seconds_at_4_5'],'actual_measured_seconds':None,'actual_duration_fail_claimed':False,'risk':'Thin-script capacity risk persists. No slowing, added silence, repeated facts or sliced pictures to fill duration.'}}
dump(HERE/'changes-r4.json',changes)
protection={'role':'AUTHOR_BYTE_INTEGRITY_ONLY','revision':'doraemon-r4','protected_before_receipt_sha256':sha(AUDIT/'protected-before-r4.json'),'protected_files':protected['protected213'],'all_213_unchanged':True,'raw_downloads_unchanged':42,'research_files_unchanged':3,'old_related_originals_unchanged':9,'old_backend_snapshot_unchanged':True,'all_r1_r2_r3_archived_files_hash_checked':True,'previous_external_files':protected['previous_external_files'],'all_previous_runtime_and_round1_round2_files_unchanged':True,'old_paid_media_readable':False,'old_paid_media_preserved_claim':False,'original_dictionary_versions':1,'original_dictionary_events':1,'dictionary_reinitialized':False,'free_runtime_dictionary_copies':checks['dictionary_copies']}
dump(HERE/'protected-inputs.json',protection)
files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','rows-r4.json','build-candidate.py','build-image-reuse-plan.mjs','free-checks-r4.mjs','freeze-author.py','image-reuse-plan.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','native-author-lint-r4.json','native-state.json','changes-r4.json','protected-inputs.json','README.md','research-original.md','research-original.claims.json','original-preservation.json','history/r3/history-manifest.json']
freeze={'schema_version':1,'revision':'doraemon-r4','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'AUTHOR_FREEZE_NOT_SOURCE_NATIVE_MEDIA_OWNER_OR_ADMISSION_VERDICT','core_four_sha256':core,'file_sha256':{name:sha(HERE/name) for name in files},'counts':notes['counts'],'single_line_and_loop_description_delta_verified':True,'replay':{'exact':True,'outputs':outputs},
 'normal_free_checks':{'ordinary_cli_lint_exit_code':0,'errors':0,'warnings':len(lint['warnings']),'narrative_warnings':0,'full_warning_receipt':'native-author-lint-r4.json','ordinary_tts_dry_run_exit_code':0,'requests':checks['requests'],'speech_hash':checks['speech_hash'],'network_attempts':0,'real_tts_calls':0,'dictionary_initialized':False,'proof_path':str(AUDIT/'free-checks-r4.json'),'proof_sha256':sha(AUDIT/'free-checks-r4.json'),'speech_request_plan_sha256':sha(AUDIT/'speech-request-plan-r4.json')},
 'history':{'r3_manifest_sha256':protected['r3_history_manifest_sha256'],'r3_source_pass_sha256':protected['r3_source_pass_sha256'],'r3_historical_verify_sha256':protected['r3_verify_sha256'],'native2_true_merged_hold_preserved':True,'old_review_tickets_unchanged':True},
 'protection':{'all_213_unchanged':True,'raw42_research3_old9_snapshot_unchanged':True,'all_old_runtime_external_rounds_and_r1_r2_r3_history_unchanged':True,'immutable_dictionary_versions':1,'immutable_dictionary_events':1,'all_dictionary_bytes_unchanged':True},
 'duration':{'target_minutes':13,'required_actual_body_seconds':[720,840],'include':['cold open','voiced CTA'],'exclude_new_bookends_seconds':26,'body_units':notes['counts']['spoken_units_total'],'speech_only_arithmetic_seconds_at_4_5':notes['counts']['estimated_speech_seconds_at_4_5'],'native_estimated_cut_minutes':lint['summary']['minutes'],'actual_audio_seconds':None,'capacity_risk':True,'actual_duration_fail_claimed':False},
 'image_plan':{'three_complete_stage_requests_deep_equal_to_r3':True,'key_1k':'65ad6caf0492dab0','key_2k':'08e0d542886f823b','actual_same_asset_verified':False,'actual_generated_images':0},'native_actualcount':2,'current_candidate_native':'NOT_PREPARED_NOT_READ','next_fresh_round_if_root_runs_it':3,'r4_author_new_native_inputs_or_calls':0,'source_r4_delta':'PENDING_OTHER_REVIEWER','pronunciation_audio_images_owner':'ALL_PENDING','budget':notes['budget'],'paid_calls':0,'backend_calls':0,'owner_approvals':0,'git_mutations':0}
dump(HERE/'author-freeze-r4.json',freeze);dump(AUDIT/'author-freeze-r4.json',freeze)
print(json.dumps({'core_four_sha256':core,'units':notes['counts']['spoken_units_total'],'lines':135,'scenes':115,'loops':23,'only_spoken_line_changed':'d1b082','other134_lines_and_115_prompt_camera_exact':True,'lint_errors':0,'lint_warnings':len(lint['warnings']),'narrative_warnings':0,'native_actualcount':2,'r4_native_prepared_or_called':0,'all_protected213_unchanged':True},ensure_ascii=False,indent=2))
