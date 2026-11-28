#!/usr/bin/env python3
"""R3 author integrity freeze. No SOURCE, native reader, media, owner or budget verdict."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=Path('/workspace/work/brand-story-20261025/doraemon-audit/author-r3')
HISTORY=HERE/'history/r2'
SLUG='story-adapt-doraemon-after-fujiko-remake-20261025'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

protected=read(AUDIT/'protected-before-r3.json')
for f in protected['protected213']:assert sha(f['path'])==f['sha256'],f['path']
for collection in ['external_runtime_files','old_native_round1_files']:
    for name,want in protected[collection].items():assert sha(name)==want,name
for rev in ['r1','r2']:
    hist=HERE/'history'/rev;manifest=read(hist/'history-manifest.json')
    for name,want in manifest['files_sha256'].items():assert sha(hist/name)==want,f'{rev}/{name}'
assert sha(HISTORY/'history-manifest.json')==protected['r2_history_manifest_sha256']
assert sha(HERE/'history/r1/history-manifest.json')==protected['r1_history_manifest_sha256']
for name in ['reviews/source-r1-independent.json','reviews/source-r2-independent.json','reviews/narrative-r1-a.raw.json','reviews/narrative-r1-b.raw.json','reviews/narrative-r1-input.json','reviews/narrative-r1-binding.json','reviews/narrative-r1.json']:
    assert sha(HERE/name)==sha(HISTORY/name),name
assert sha(HISTORY/'reviews/source-r2-independent.json')=='8ff2cb3e90dc7d7d97773f712e071c414c132b00c2898f8f252c3cc0259348ab'
assert sha(HISTORY/'verify-1.md')=='c3d2069b92de5d0891b38cfc23bfe7355a6391d85386492672b150c544e2c483'
assert not (HERE/'verify-1.md').exists(),'Historical R2 verify cannot approve R3.'
oldnative=read(HISTORY/'reviews/narrative-r1.json')
assert oldnative['round']==1 and not oldnative['passed'] and oldnative['failed']==['payoffs','no_recap','no_detour']

outputs=['video.json','script.md','narration-only.json','claims.json','claims.md','series.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','image-reuse-plan.json']
before={n:sha(HERE/n) for n in outputs}
subprocess.run(['python',str(HERE/'build-candidate.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['node',str(HERE/'build-image-reuse-plan.mjs')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
assert {n:sha(HERE/n) for n in outputs}==before,'Deterministic author replay changed bytes.'
doc=read(HERE/'video.json');old=read(HISTORY/'video.json');narration=read(HERE/'narration-only.json');claims=read(HERE/'claims.json');edits=read(HERE/'edits-r3.json');notes=read(HERE/'producer-notes.json')
old_lines={l['id']:l for s in old['scenes'] for l in s['lines']}
new_lines={l['id']:l for s in doc['scenes'] for l in s['lines']}
removed=[lid for lid in old_lines if lid not in new_lines]
assert set(removed)==set(edits['removed_ids'])
changed=[lid for lid in new_lines if new_lines[lid]['text']!=old_lines[lid]['text']]
assert set(changed)==set(edits['patches'])
for lid in changed:assert new_lines[lid]['text']==edits['patches'][lid]
assert set(new_lines).issubset(old_lines),'No new or renumbered line IDs.'
for lid in new_lines:
    expect=dict(old_lines[lid]);expect['text']=new_lines[lid]['text'];assert expect==new_lines[lid],lid
assert new_lines['d1b011']==old_lines['d1b011'] and new_lines['d1b012']==old_lines['d1b012'],'Do not lose the R2 release-year fix.'
old_scenes={s['id']:s for s in old['scenes']}
for scene in doc['scenes']:
    previous=old_scenes[scene['id']]
    assert {k:v for k,v in previous.items() if k!='lines'}=={k:v for k,v in scene.items() if k!='lines'},scene['id']
assert [s['id'] for s in doc['scenes']]==[s['id'] for s in old['scenes'] if any(l['id'] in new_lines for l in s['lines'])]
for key in old:
    if key not in ['loops','scenes']:assert doc[key]==old[key],key
assert [(l['id'],l['text']) for s in doc['scenes'] for l in s['lines']]==[(l['id'],l['text']) for l in narration]==[(l['id'],l['text']) for l in claims['lines']]
assert len(doc['loops'])==23 and all(loop['setup'] in new_lines and loop['payoff'] in new_lines for loop in doc['loops'])
assert sha(HERE/'research-original.md')==sha(HISTORY/'research-original.md') and sha(HERE/'research-original.claims.json')==sha(HISTORY/'research-original.claims.json') and sha(HERE/'original-preservation.json')==sha(HISTORY/'original-preservation.json')
assert sha(HERE/'source-anchors-r1.json')==sha(HISTORY/'source-anchors-r1.json'),'Original author anchors unchanged.'
oldplan=read(HISTORY/'image-reuse-plan.json');plan=read(HERE/'image-reuse-plan.json')
assert oldplan['pairs'][0]['requests']==plan['pairs'][0]['requests'],'Full three-end native Stage requests changed.'
assert plan['actual_same_asset_verified'] is False
lint=read(HERE/'native-author-lint-r3.json');checks=read(AUDIT/'free-checks-r3.json')
assert lint['errors']==[] and not [w for w in lint['warnings'] if w.get('kind')=='narrative']
assert checks['lint_exit_code']==checks['planner_exit_code']==0 and checks['network_attempts']==0 and checks['dictionary_initialized'] is False
assert lint['summary']['spoken_units']==notes['counts']['spoken_units_total']
for copy in checks['dictionary_copies']:assert sha(copy['source'])==sha(copy['target'])==copy['sha256']
state={'schema_version':1,'revision':'doraemon-r3','actualcount':1,'last_actual_native_round':1,'last_actual_native_result':'HOLD','last_actual_native_shared_required_holds':oldnative['failed'],'last_actual_native_binding':{'source_video_sha256':sha(HISTORY/'video.json'),'receipt_sha256':sha(HISTORY/'reviews/narrative-r1.json')},'current_candidate_native_state':'NOT_PREPARED_NOT_READ','next_fresh_round_if_root_starts_it':2,'r3_author_prepared_native_payloads':0,'r3_author_native_or_blind_calls':0,'source_r3_delta':'PENDING_OTHER_REVIEWER','r2_source_pass_is_historical_only':True,'verify_1_for_r3_exists':False,'owner_approval':False}
dump(HERE/'native-state.json',state)
core={name:sha(HERE/name) for name in ['video.json','script.md','narration-only.json','claims.json']}
assert core==plan['core_four_sha256']
changes={'schema_version':1,'revision':'doraemon-r3','role':'AUTHOR_CHANGES_NOT_INDEPENDENT_VERDICT','previous_core_four_sha256':{name:sha(HISTORY/name) for name in core},'current_core_four_sha256':core,
 'previous_source_pass_sha256':sha(HISTORY/'reviews/source-r2-independent.json'),'previous_verify_sha256':sha(HISTORY/'verify-1.md'),'previous_true_native_round':1,'previous_true_native_shared_holds':oldnative['failed'],'existing_review_tickets_unchanged':True,
 'line_changes':[{'id':lid,'old':old_lines[lid]['text'],'new':new_lines[lid]['text']} for lid in changed],'removed_lines':[{'id':lid,'text':old_lines[lid]['text']} for lid in removed],'unchanged_surviving_lines':len(new_lines)-len(changed),
 'removed_scene_ids':[s['id'] for s in old['scenes'] if s['id'] not in {x['id'] for x in doc['scenes']}],'surviving_scene_prompt_camera_all_other_non_line_fields_exact':True,'new_scene_ids':[],
 'payoffs_fix':'c05 asks about the director creative-work requirement. c06 attributes that requirement; c07 gives the participant admission and actual reconsideration stated in MW2019A2 L16. No question about fictional friendship is left hanging, no film plot/answer was invented.',
 'no_recap_fix':'b042 removes repeated screenwriter credit. d04/d05 already-answered question/answer restatement is deleted; d023 now asks a new work question answered by the existing d03 director feedback.',
 'no_detour_fix':'a04b pen-name/separation history is removed from narration and retained in claims.unvoiced_background with the unchanged A05 source anchor.',
 'not_chased':['chapters_are_events advisory','B-only scene_first HOLD'],'r2_release_year_fix_exactly_preserved':True,
 'source_for_work_rewrite':{'source_id':'MW2019A2','text_line_1based':16,'quote_fragments':['最初はただ','関係性を考えていきました'],'original_raw_and_anchors_unchanged':True},
 'loops':doc['loops'],'complete_three_end_stage_requests_unchanged':True,'actual_same_asset_verified':False,'source_r3_delta':'PENDING','fresh_native2':'PENDING_ROOT_NOT_PREPARED_BY_AUTHOR','actual_native_rounds_total':1,
 'capacity':{'before_units':read(HISTORY/'producer-notes.json')['counts']['spoken_units_total'],'after_units':notes['counts']['spoken_units_total'],'target_minutes':13,'required_measured_body_seconds':[720,840],'speech_only_seconds_at_4_5':notes['counts']['estimated_speech_seconds_at_4_5'],'actual_measured_seconds':None,'actual_duration_fail_claimed':False,'risk':'Deletions reduce content capacity below approximate3500 units. Arithmetic and default native estimate are not measured audio. No lowering13, slowed voice, added pauses, repeated facts or sliced pictures to fill time.'}}
dump(HERE/'changes-r3.json',changes)
protection={'role':'AUTHOR_BYTE_INTEGRITY_ONLY','revision':'doraemon-r3','protected_before_receipt_sha256':sha(AUDIT/'protected-before-r3.json'),'protected_files':protected['protected213'],'all_213_unchanged':True,'raw_downloads_unchanged':42,'research_files_unchanged':3,'old_related_originals_unchanged':9,'old_backend_snapshot_unchanged':True,'old_paid_media_readable':False,'old_paid_media_preserved_claim':False,'r1_and_r2_histories_hash_checked':True,'original_runtime_all_files_unchanged':True,'actual_native1_external_and_repo_receipts_unchanged':True,'original_dictionary_versions':1,'original_dictionary_events':1,'dictionary_reinitialized':False,'free_runtime_dictionary_copies':checks['dictionary_copies']}
dump(HERE/'protected-inputs.json',protection)
files=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','rows-r3.json','edits-r3.json','build-candidate.py','build-image-reuse-plan.mjs','free-checks-r3.mjs','freeze-author.py','image-reuse-plan.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','native-author-lint-r3.json','native-state.json','changes-r3.json','protected-inputs.json','README.md','research-original.md','research-original.claims.json','original-preservation.json','history/r2/history-manifest.json']
freeze={'schema_version':1,'revision':'doraemon-r3','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'AUTHOR_FREEZE_NOT_SOURCE_NATIVE_MEDIA_OWNER_OR_ADMISSION_VERDICT','slug':SLUG,'core_four_sha256':core,'file_sha256':{name:sha(HERE/name) for name in files},'counts':notes['counts'],
 'replay':{'exact':True,'outputs':outputs},'normal_free_checks':{'ordinary_cli_lint_exit_code':0,'errors':0,'warnings':len(lint['warnings']),'narrative_warnings':0,'full_warning_receipt':'native-author-lint-r3.json','ordinary_tts_dry_run_exit_code':0,'requests':checks['requests'],'speech_hash':checks['speech_hash'],'network_attempts':0,'real_tts_calls':0,'dictionary_initialized':False,'proof_path':str(AUDIT/'free-checks-r3.json'),'proof_sha256':sha(AUDIT/'free-checks-r3.json'),'speech_request_plan_sha256':sha(AUDIT/'speech-request-plan-r3.json')},
 'history':{'r1_manifest_sha256':protected['r1_history_manifest_sha256'],'r2_manifest_sha256':protected['r2_history_manifest_sha256'],'r2_source_and_verify_historical_only':True,'r2_native1_true_merged_hold_preserved':True,'old_review_tickets_unchanged':True},
 'protection':{'all_213_unchanged':True,'raw42_research3_old9_snapshot_unchanged':True,'old_original_runtime_unchanged':True,'immutable_dictionary_versions':1,'immutable_dictionary_events':1,'all_dictionary_bytes_unchanged':True},
 'duration':{'target_minutes':13,'required_actual_body_seconds':[720,840],'include':['cold open','voiced CTA'],'exclude_new_bookends_seconds':26,'body_units':notes['counts']['spoken_units_total'],'speech_only_arithmetic_seconds_at_4_5':notes['counts']['estimated_speech_seconds_at_4_5'],'native_estimated_cut_minutes':lint['summary']['minutes'],'actual_audio_seconds':None,'capacity_risk':True,'actual_duration_fail_claimed':False},
 'image_plan':{'three_complete_stage_requests_deep_equal_to_r2':True,'key_1k':'65ad6caf0492dab0','key_2k':'08e0d542886f823b','actual_same_asset_verified':False,'actual_generated_images':0},
 'native_actualcount':1,'current_candidate_native':'NOT_PREPARED_NOT_READ','next_fresh_round_if_root_runs_it':2,'r3_author_new_native_inputs_or_calls':0,'source_r3_delta':'PENDING_OTHER_REVIEWER','pronunciation_audio_images_owner':'ALL_PENDING','budget':notes['budget'],'paid_calls':0,'backend_calls':0,'owner_approvals':0,'git_mutations':0}
dump(HERE/'author-freeze-r3.json',freeze);dump(AUDIT/'author-freeze-r3.json',freeze)
print(json.dumps({'core_four_sha256':core,'units':notes['counts']['spoken_units_total'],'lines':len(new_lines),'scenes':len(doc['scenes']),'loops':len(doc['loops']),'changed_lines':len(changed),'removed_lines':len(removed),'surviving_prompt_camera_exact':True,'lint_errors':0,'lint_warnings':len(lint['warnings']),'narrative_warnings':0,'native_actualcount':1,'r3_native_prepared_or_called':0,'all_protected213_unchanged':True},ensure_ascii=False,indent=2))
