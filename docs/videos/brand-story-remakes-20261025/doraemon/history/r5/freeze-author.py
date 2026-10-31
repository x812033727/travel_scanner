#!/usr/bin/env python3
"""R5 author deduplication delta and byte-integrity freeze; no independent verdict."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=Path('/workspace/work/brand-story-20261025/doraemon-audit/author-r5')
HISTORY=HERE/'history/r4'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
protected=read(AUDIT/'protected-before-r5.json')
for f in protected['protected213']:assert sha(f['path'])==f['sha256'],f['path']
for name,w in protected['previous_external_files'].items():assert sha(name)==w,name
for rev in ['r1','r2','r3','r4']:
    hist=HERE/'history'/rev;m=read(hist/'history-manifest.json')
    for name,w in m['files_sha256'].items():assert sha(hist/name)==w,f'{rev}/{name}'
assert sha(HISTORY/'history-manifest.json')==protected['r4_history_manifest_sha256']
for p in (HISTORY/'reviews').iterdir():
    if p.is_file():assert sha(HERE/'reviews'/p.name)==sha(p),p.name
assert sha(HISTORY/'reviews/source-r4-independent.json')==protected['r4_source_pass_sha256']
assert sha(HISTORY/'verify-1.md')==protected['r4_verify_sha256']
assert not (HERE/'verify-1.md').exists(),'R4 verify must remain historical, not approve R5.'
merged=read(HISTORY/'reviews/narrative-r3.json')
assert merged['round']==3 and merged['passed'] is False and merged['failed']==['no_recap']
outputs=['video.json','script.md','narration-only.json','claims.json','claims.md','series.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','image-reuse-plan.json']
prior={n:sha(HERE/n) for n in outputs}
subprocess.run(['python',str(HERE/'build-candidate.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['node',str(HERE/'build-image-reuse-plan.mjs')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
assert {n:sha(HERE/n) for n in outputs}==prior,'Author replay drift.'
old=read(HISTORY/'video.json');doc=read(HERE/'video.json');oldn=read(HISTORY/'narration-only.json');n=read(HERE/'narration-only.json');oldc=read(HISTORY/'claims.json');c=read(HERE/'claims.json')
oldtext='今天就沿著這份跨過三十年的哆啦Ａ夢工作，看看一張紙怎麼交到下一雙手。'
newtext='今天就沿著哆啦Ａ夢的創作工作，看看一張紙怎麼交到下一雙手。'
removed_ids={'d1c021','d1c022'}
removed_lines=[l for l in oldn if l['id'] in removed_ids]
old_scenes={s['id']:s for s in old['scenes']}
for s in old['scenes']:
    s['lines']=[l for l in s['lines'] if l['id'] not in removed_ids]
    for l in s['lines']:
        if l['id']=='d1h051':assert l['text']==oldtext;l['text']=newtext
old['scenes']=[s for s in old['scenes'] if s['lines']]
assert old==doc,'Video changes exceed h051 and removal of c021/c022.'
oldn=[l for l in oldn if l['id'] not in removed_ids]
for l in oldn:
    if l['id']=='d1h051':l['text']=newtext
assert oldn==n,'Other132 surviving spoken lines changed.'
retained_scenes={s['id'] for s in doc['scenes']}
oldc['revision']='doraemon-r5';oldc['lines']=[l for l in oldc['lines'] if l['id'] not in removed_ids]
for l in oldc['lines']:
    if l['id']=='d1h051':l['text']=newtext
oldc['written_visuals']=[v for v in oldc['written_visuals'] if v['scene_id'] in retained_scenes]
assert oldc==c,'Claims exceed the same spoken delta and retired visuals, plus revision.'
expected=(HISTORY/'script.md').read_text().replace('Doraemon remake｜R4作者稿','Doraemon remake｜R5作者稿').replace(oldtext,newtext)
for l in removed_lines:expected=expected.replace(f"**{l['id']}** {l['text']}\n\n",'')
assert expected==(HERE/'script.md').read_text()
for name in ['source-anchors-r1.json','series.json','research-original.md','research-original.claims.json','original-preservation.json']:
    assert sha(HERE/name)==sha(HISTORY/name),name
assert doc['loops']==read(HISTORY/'video.json')['loops'],'All23 loop endpoints and descriptions must remain exact.'
flat={l['id']:l for s in doc['scenes'] for l in s['lines']}
assert all(loop['setup'] in flat and loop['payoff'] in flat for loop in doc['loops'])
for lid in ['d1b011','d1b082','d1c011','d1c012']:
    previous=next(l for s in read(HISTORY/'video.json')['scenes'] for l in s['lines'] if l['id']==lid)
    assert flat[lid]==previous,lid
plan=read(HERE/'image-reuse-plan.json');oldplan=read(HISTORY/'image-reuse-plan.json')
assert plan['pairs'][0]['requests']==oldplan['pairs'][0]['requests'] and not plan['actual_same_asset_verified']
core={name:sha(HERE/name) for name in ['video.json','script.md','narration-only.json','claims.json']}
assert plan['core_four_sha256']==core
lint=read(HERE/'native-author-lint-r5.json');checks=read(AUDIT/'free-checks-r5.json');notes=read(HERE/'producer-notes.json')
assert lint['errors']==[] and not [w for w in lint['warnings'] if w.get('kind')=='narrative']
assert checks['lint_exit_code']==checks['planner_exit_code']==0 and checks['network_attempts']==0 and checks['dictionary_initialized'] is False
assert lint['summary']['spoken_units']==notes['counts']['spoken_units_total']
for item in checks['dictionary_copies']:assert sha(item['source'])==sha(item['target'])==item['sha256']
state={'schema_version':1,'revision':'doraemon-r5','actualcount':3,'last_actual_native_round':3,'last_actual_native_result':'HOLD','last_actual_native_shared_required_holds':['no_recap'],'last_actual_native_binding':{'source_video_sha256':sha(HISTORY/'video.json'),'receipt_sha256':sha(HISTORY/'reviews/narrative-r3.json')},'current_candidate_native_state':'NOT_PREPARED_NOT_READ','next_fresh_round_if_root_starts_it':4,'r5_author_prepared_native_payloads':0,'r5_author_native_or_blind_calls':0,'source_r5_delta':'PENDING_OTHER_REVIEWER','r4_published_source_pass_is_historical_only':True,'verify_1_for_r5_exists':False,'owner_approval':False}
dump(HERE/'native-state.json',state)
changes={'schema_version':1,'revision':'doraemon-r5','role':'AUTHOR_DELTA_NOT_INDEPENDENT_REVIEW','published_r4_core_four_sha256':{name:sha(HISTORY/name) for name in core},'current_core_four_sha256':core,'line_changes':[{'id':'d1h051','old':oldtext,'new':newtext}],'removed_lines':removed_lines,'other_surviving_spoken_lines_exact':132,'line_count_before':135,'line_count_after':133,'scene_count_before':115,'scene_count_after':113,'removed_scene_ids':[sid for sid in old_scenes if sid not in retained_scenes],'all113_surviving_scene_non_line_fields_exact':True,'new_line_or_scene_ids':[],
 'no_recap_fix':'h051 keeps one named-topic promise without repeating the thirty-year scope already said in h011. c011/c012 retain the attributed director proposal and participant writing response; c021/c022 synonymous generalizations are deleted instead of adding a fake callback.',
 'loop_integrity':{'all23_entries_and_endpoints_exact':True,'all_endpoints_survive':True,'b10_actual_payoff_c011_proposal_preserved':True,'false_callbacks_added':0},'b082_work_result_and_D14_D15_evidence_exact':True,'r2_movie_release_year_fix_exact':True,'full_three_end_stage_requests_exact':True,'actual_same_asset_verified':False,'not_chased':['chapter-name advisory'],
 'published_r4_source_pass_sha256':protected['r4_source_pass_sha256'],'published_r4_verify_sha256':protected['r4_verify_sha256'],'last_true_native_round':3,'last_true_native_shared_hold':['no_recap'],'all_old_review_tickets_unchanged':True,
 'source_r5_delta':'PENDING_OTHER_REVIEWER','fresh_native4':'PENDING_ROOT_NOT_PREPARED_BY_AUTHOR','actual_native_rounds_total':3,'capacity':{'before_units':3104,'after_units':notes['counts']['spoken_units_total'],'target_minutes':13,'required_measured_body_seconds':[720,840],'pure_arithmetic_seconds_at_4_5':notes['counts']['estimated_speech_seconds_at_4_5'],'actual_measured_seconds':None,'actual_duration_fail_claimed':False,'risk':'Thin-script capacity is reduced by genuine deduplication. No lowering13, slowing, padding, repetition or sliced pictures.'}}
dump(HERE/'changes-r5.json',changes)
protection={'role':'AUTHOR_BYTE_INTEGRITY_ONLY','revision':'doraemon-r5','protected_before_receipt_sha256':sha(AUDIT/'protected-before-r5.json'),'protected_files':protected['protected213'],'all_213_unchanged':True,'raw_downloads_unchanged':42,'research_files_unchanged':3,'old_related_originals_unchanged':9,'old_backend_snapshot_unchanged':True,'all_r1_r2_r3_r4_archived_files_hash_checked':True,'previous_external_files':protected['previous_external_files'],'all_previous_runtime_and_round1_round2_round3_files_unchanged':True,'old_paid_media_readable':False,'old_paid_media_preserved_claim':False,'original_dictionary_versions':1,'original_dictionary_events':1,'dictionary_reinitialized':False,'free_runtime_dictionary_copies':checks['dictionary_copies']}
dump(HERE/'protected-inputs.json',protection)
files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','rows-r5.json','build-candidate.py','build-image-reuse-plan.mjs','free-checks-r5.mjs','freeze-author.py','image-reuse-plan.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','native-author-lint-r5.json','native-state.json','changes-r5.json','protected-inputs.json','README.md','research-original.md','research-original.claims.json','original-preservation.json','history/r4/history-manifest.json']
freeze={'schema_version':1,'revision':'doraemon-r5','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'AUTHOR_FREEZE_NOT_SOURCE_NATIVE_MEDIA_OWNER_OR_ADMISSION_VERDICT','core_four_sha256':core,'file_sha256':{name:sha(HERE/name) for name in files},'counts':notes['counts'],'deduplication_delta_verified':True,'replay':{'exact':True,'outputs':outputs},
 'normal_free_checks':{'ordinary_cli_lint_exit_code':0,'errors':0,'warnings':len(lint['warnings']),'narrative_warnings':0,'full_warning_receipt':'native-author-lint-r5.json','ordinary_tts_dry_run_exit_code':0,'requests':checks['requests'],'speech_hash':checks['speech_hash'],'network_attempts':0,'real_tts_calls':0,'dictionary_initialized':False,'proof_path':str(AUDIT/'free-checks-r5.json'),'proof_sha256':sha(AUDIT/'free-checks-r5.json'),'speech_request_plan_sha256':sha(AUDIT/'speech-request-plan-r5.json')},
 'history':{'published_r4_manifest_sha256':protected['r4_history_manifest_sha256'],'published_r4_source_pass_sha256':protected['r4_source_pass_sha256'],'published_r4_historical_verify_sha256':protected['r4_verify_sha256'],'native3_true_merged_hold_preserved':True,'old_review_tickets_unchanged':True,'r5_not_mixed_into_published_r4_snapshot':True},
 'protection':{'all_213_unchanged':True,'raw42_research3_old9_snapshot_unchanged':True,'all_old_runtime_external_rounds_and_r1_r2_r3_r4_history_unchanged':True,'immutable_dictionary_versions':1,'immutable_dictionary_events':1,'all_dictionary_bytes_unchanged':True},
 'duration':{'target_minutes':13,'required_actual_body_seconds':[720,840],'include':['cold open','voiced CTA'],'exclude_new_bookends_seconds':26,'body_units':notes['counts']['spoken_units_total'],'speech_only_arithmetic_seconds_at_4_5':notes['counts']['estimated_speech_seconds_at_4_5'],'native_estimated_cut_minutes':lint['summary']['minutes'],'actual_audio_seconds':None,'capacity_risk':True,'actual_duration_fail_claimed':False},
 'image_plan':{'three_complete_stage_requests_deep_equal_to_r4':True,'key_1k':'65ad6caf0492dab0','key_2k':'08e0d542886f823b','actual_same_asset_verified':False,'actual_generated_images':0},'native_actualcount':3,'current_candidate_native':'NOT_PREPARED_NOT_READ','next_fresh_round_if_root_runs_it':4,'r5_author_new_native_inputs_or_calls':0,'source_r5_delta':'PENDING_OTHER_REVIEWER','pronunciation_audio_images_owner':'ALL_PENDING','budget':notes['budget'],'paid_calls':0,'backend_calls':0,'owner_approvals':0,'git_mutations':0}
dump(HERE/'author-freeze-r5.json',freeze);dump(AUDIT/'author-freeze-r5.json',freeze)
print(json.dumps({'core_four_sha256':core,'units':notes['counts']['spoken_units_total'],'lines':133,'scenes':113,'loops':23,'changed_spoken_lines':['d1h051'],'removed_spoken_lines':sorted(removed_ids),'other132_lines_and_113_prompt_camera_exact':True,'lint_errors':0,'lint_warnings':len(lint['warnings']),'narrative_warnings':0,'native_actualcount':3,'r5_native_prepared_or_called':0,'all_protected213_unchanged':True},ensure_ascii=False,indent=2))
