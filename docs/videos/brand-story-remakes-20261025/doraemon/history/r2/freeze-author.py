#!/usr/bin/env python3
"""Author integrity and exact-SHA freeze; never a source, reader, media or owner verdict."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=Path('/workspace/work/brand-story-20261025/doraemon-audit')
RUNTIME=Path('/workspace/work/brand-story-20261025/doraemon-submission-root')
SLUG='story-adapt-doraemon-after-fujiko-remake-20261025'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def read(p):return json.loads(Path(p).read_text())

before=read(AUDIT/'author-protected-before.json')['files']
changed=[]
for f in before:
    if sha(f['path'])!=f['sha256']:changed.append(f['path'])
assert not changed,changed
invpath=AUDIT/'source-cache/raw-inventory.json';inv=read(invpath);binds=0
for item in inv['items']+inv['cached_extractions']+inv['supplemental_extractions']:
    for pk,hk in [('raw_path','raw_sha256'),('decoded_path','decoded_sha256'),('text_path','text_sha256'),('receipt_path','receipt_sha256'),('tool_result_path','tool_result_sha256')]:
        if item.get(pk) and item.get(hk):assert sha(item[pk])==item[hk],item[pk];binds+=1
pres=read(HERE/'original-preservation.json')
for old in pres['related_git_material']:
    assert Path(old['readonly_snapshot_path']).stat().st_mode & 0o777==0o400
assert Path(pres['original_worker']['readonly_snapshot_path']).stat().st_mode & 0o777==0o400
dictionary=RUNTIME/'docs/videos'/SLUG/'story-lexicon'
versions=list((dictionary/'versions').glob('*.json'));events=list((dictionary/'events').glob('*.json'))
assert len(versions)==1 and len(events)==1,'Do not rebuild or self-approve the dictionary.'
protected={'schema_version':1,'role':'AUTHOR_BYTE_INTEGRITY_ONLY_NOT_INDEPENDENT_SOURCE_VERDICT','slug':SLUG,
 'before_receipt':str(AUDIT/'author-protected-before.json'),'before_receipt_sha256':sha(AUDIT/'author-protected-before.json'),'protected_files':before,
 'all_existing_protected_bytes_unchanged':True,'protected_file_count':len(before),'frozen_research_files':3,'old_related_originals_unchanged':9,'old_backend_snapshot_unchanged':True,
 'download_inventory':str(invpath),'download_inventory_sha256':sha(invpath),'raw_download_inventory_items':len(inv['items']),'cached_extractions':len(inv['cached_extractions']),'recorded_inventory_hash_bindings_checked':binds,
 'old_readonly_snapshot_modes_0400':True,'old_paid_media_locally_readable':False,'old_paid_media_preserved_claim':False,
 'dictionary':{'root':str(dictionary),'version_count':len(versions),'event_count':len(events),'version_files_sha256':{str(p):sha(p) for p in versions},'current_sha256':sha(dictionary/'current.json'),'normal_initialize_helper':'../prepare-runtime.mjs','independent_pronunciation_approval':'PENDING'},
 'new_network_raw_downloads':0,'old_raw_rewritten':False,'approvals_created':0,'backend_calls':0,'paid_calls':0,'git_mutations':0}
dump(HERE/'protected-inputs.json',protected)

# A second deterministic replay must leave every generated author output byte-identical.
generated=['video.json','script.md','narration-only.json','claims.json','claims.md','series.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','image-reuse-plan.json']
oldhash={n:sha(HERE/n) for n in generated}
subprocess.run(['python',str(HERE/'build-candidate.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['node',str(HERE/'build-image-reuse-plan.mjs')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
assert {n:sha(HERE/n) for n in generated}==oldhash,'Replay drift; stop before freeze.'
doc=read(HERE/'video.json');n=read(HERE/'narration-only.json');claims=read(HERE/'claims.json');lint=read(HERE/'native-author-lint-r2.json');notes=read(HERE/'producer-notes.json')
assert lint['errors']==[]
assert not [w for w in lint['warnings'] if w.get('kind')=='narrative'],'Cadence is not cleared mechanically.'
flat=[{'id':l['id'],'text':l['text'],'chapter':s.get('chapter')} for s in doc['scenes'] for l in s['lines']]
assert [(l['id'],l['text']) for l in flat]==[(l['id'],l['text']) for l in n]==[(l['id'],l['text']) for l in claims['lines']]
assert len({l['id'] for l in n})==len(n) and all(re.fullmatch('[a-z0-9]{4,8}',l['id']) for l in n)
core={name:sha(HERE/name) for name in ['video.json','script.md','narration-only.json','claims.json']}
assert read(HERE/'image-reuse-plan.json')['core_four_sha256']==core
runtime_dir=RUNTIME/'docs/videos'/SLUG
assert sha(runtime_dir/'video.json')==core['video.json']
assert sha(runtime_dir/'brief.md')==sha(HERE/'brief.md')
nativecount=lint['summary']['spoken_units'];assert nativecount==notes['counts']['spoken_units_total']
history=HERE/'history/r1'
history_manifest=read(history/'history-manifest.json')
for name,want in history_manifest['files_sha256'].items():assert sha(history/name)==want, f'R1 archive drift: {name}'
assert sha(HERE/'reviews/source-r1-independent.json')==sha(history/'reviews/source-r1-independent.json')=='af898fce98bc61e139a08157da755f0af5b87798b1a4fc0b14e57c9b904c8999'
assert sha(HERE/'author-freeze-r1.json')==sha(history/'author-freeze-r1.json')
dict_before=read(AUDIT/'r2-dictionary-before.json')
assert {str(p):sha(p) for p in dictionary.rglob('*') if p.is_file()}==dict_before, 'Immutable dictionary bytes changed.'
oldtext='二〇一九年，接下《大雄的月球探測記》腳本的辻村深月，收到むぎわら的鼓勵。'
newtext='替二〇一九年上映的《大雄的月球探測記》寫腳本時，辻村深月收到むぎわら的鼓勵。'
oldvideo=read(history/'video.json');oldn=read(history/'narration-only.json');oldclaims=read(history/'claims.json')
oldcore={name:sha(history/name) for name in core}
changed=[]
for scene in oldvideo['scenes']:
    for line in scene['lines']:
        if line['id']=='d1b011':assert line['text']==oldtext;line['text']=newtext;changed.append(line['id'])
assert changed==['d1b011'] and oldvideo==doc, 'Video delta exceeds the one authorized text leaf.'
for line in oldn:
    if line['id']=='d1b011':line['text']=newtext
assert oldn==n, 'Other narration changed.'
oldclaims['revision']='doraemon-r2'
for line in oldclaims['lines']:
    if line['id']=='d1b011':line['text']=newtext
assert oldclaims==claims, 'Claim delta exceeds revision metadata and one text leaf.'
expected_script=(history/'script.md').read_text().replace('Doraemon remake｜R1作者稿','Doraemon remake｜R2作者稿').replace(oldtext,newtext)
assert expected_script==(HERE/'script.md').read_text(), 'Script delta exceeds heading metadata and one text leaf.'
oldplan=read(history/'image-reuse-plan.json');newplan=read(HERE/'image-reuse-plan.json')
oldplan['revision']='doraemon-r2';oldplan['core_four_sha256']=core
assert oldplan==newplan, 'Complete Stage request/key plan changed.'
for unchanged in ['series.json','source-anchors-r1.json','row-index-r1.json','rows-r1.json','research-original.md','research-original.claims.json','original-preservation.json']:
    assert sha(HERE/unchanged)==sha(history/unchanged), unchanged
assert not (HERE/'verify-1.md').exists() and not (runtime_dir/'verify-1.md').exists() and not (history/'verify-1.md').exists()
state=read(HERE/'native-state.json');assert state['fresh_native_state']=='NOT_PREPARED_NOT_READ' and state['actualcount']==0 and not state['native_1_hold_exists']
delta={'schema_version':1,'revision':'doraemon-r2','role':'AUTHOR_DELTA_INTEGRITY_NOT_INDEPENDENT_SOURCE_OR_NATIVE_VERDICT',
 'source_hold_r1_sha256':sha(history/'reviews/source-r1-independent.json'),'source_delta_review':'PENDING_OTHER_REVIEWER',
 'core_four_before_sha256':oldcore,'core_four_after_sha256':core,'authorized_changed_line_id':'d1b011','old_text':oldtext,'new_text':newtext,
 'year_scope':'2019 explicitly modifies the movie release; the email receipt/sent year remains unasserted.','email_event_year_asserted':None,
 'adjacent_lines_re_read':[l for l in n if l['id'] in ['d1b011','d1b012','d1b021','d1b022']],
 'other_spoken_lines_unchanged':148,'all_149_line_ids_and_order_unchanged':True,'all_124_scene_ids_order_prompt_camera_and_other_fields_unchanged':True,
 'all_23_loops_deep_equal':True,'all_three_stage_request_endpoints_deep_equal_to_r1':True,'actual_same_asset_verified':False,
 'nonspoken_metadata_delta':['R2 revision labels and author-script heading','current exact counts/estimates and current SHA bindings'],
 'r1_archive_manifest_sha256':sha(history/'history-manifest.json'),'all_r1_archived_files_unchanged':True,'research3_raw42_protected213_old9_and_snapshot_unchanged':True,
 'dictionary_all_existing_file_bytes_unchanged':True,'dictionary_versions':1,'dictionary_events':1,
 'fresh_native_state':'NOT_PREPARED_NOT_READ','fresh_native_actualcount':0,'native_1_hold_exists':False,'ordinary_free_lint_is_not_fresh_native_review':True,
 'verify_1_written':False,'owner_approvals':0,'backend_calls':0,'paid_calls':0,'git_mutations':0}
dump(HERE/'author-delta-r2.json',delta)
corefiles=['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','rows-r2.json','build-candidate.py','build-image-reuse-plan.mjs','image-reuse-plan.json','source-anchors-r1.json','row-index-r1.json','producer-notes.json','protected-inputs.json','native-author-lint-r2.json','README.md','freeze-author.py','research-original.md','research-original.claims.json','original-preservation.json','author-delta-r2.json','native-state.json','history/r1/history-manifest.json']
freeze={'schema_version':1,'revision':'doraemon-r2','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'AUTHOR_SUBMISSION_FREEZE_NOT_INDEPENDENT_VERDICT','slug':SLUG,
 'core_four_sha256':core,'file_sha256':{name:sha(HERE/name) for name in corefiles},'counts':notes['counts'],
 'native_author_lint':{'errors':0,'warnings':len(lint['warnings']),'narrative_warnings':0,'summary':lint['summary'],'receipt':'native-author-lint-r2.json','command':['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',str(RUNTIME),'lint','--slug',SLUG,'--json'],'schema_preflight_failures_external_only':['free-lint-attempt-01.json','free-lint-attempt-02.json'],'author_cadence_working_receipts_external':['free-lint-attempt-03.json','free-lint-attempt-04.json','free-lint-attempt-05.json','free-lint-attempt-06.json'],'fresh_native_reader_rounds_run':0,'warning_policy':'Complete native warnings preserved; no suppression. Repetitive blank-surface concepts, intentional same-asset adjacent payoff, long-shot estimates and overall length still need production assessment.'},
 'replay':{'generated_files':generated,'all_exactly_reproduced':True},'protection':{'protected_files':len(before),'changed':[],'research3_unchanged':True,'raw_index_and_all_old_cache_unchanged':True,'old_backend_and9_related_originals_unchanged':True,'old_paid_media_locally_readable':False,'old_paid_media_preserved_claim':False},
 'runtime':{'root':str(RUNTIME),'media_base':str(AUDIT/'media'),'runtime_outside_repo':True,'media_outside_runtime_and_repo':True,'manifest_sha256':sha(RUNTIME/'runtime-manifest.json'),'canonical_runtime_script_sha256':sha(runtime_dir/'script.md'),'author_script_is_not_canonical_runtime_script':True,'immutable_dictionary_version_count':len(versions),'immutable_dictionary_sha256':versions[0].stem},
 'duration':{'target_minutes':13,'required_actual_speech_body_seconds':[720,840],'speech_body_includes_cold_open_and_voiced_cta':True,'new_bookends_excluded_seconds':26,'native_estimated_cut_minutes':lint['summary']['minutes'],'speech_only_arithmetic_seconds_at_4_5':round(nativecount/4.5,2),'actual_speech_body_seconds':None,'risk':'3371 units is below the approximate3500 capacity target. Native estimate includes normal pauses/scene gaps and remains about15.7min; the4.5units/s speech-only arithmetic is not actual duration. Measure real voice/cut before any duration decision; do not lower13, slow delivery, pad silence or repeat facts.'},
 'image_reuse':{'declared_complete_native_key_equal':True,'endpoints':3,'actual_same_asset_verified':False,'real_selected_file_sha256':None,'actual_generated_media':0},
 'budget':notes['budget'],'pending':notes['pending'],'source_review':'PENDING_OTHER_REVIEWER_R2_DELTA','previous_source_review':'R1_HOLD','previous_source_receipt_sha256':'af898fce98bc61e139a08157da755f0af5b87798b1a4fc0b14e57c9b904c8999','fresh_native_state':'NOT_PREPARED_NOT_READ','fresh_native_actualcount':0,'native_1_hold_exists':False,'fresh_native_readers':'PENDING_TWO_FRESH_READERS','pronunciation':'PENDING_OTHER_REVIEWER','audio_and_visuals':'PENDING','owner':'ALL_PENDING','paid_calls':0,'backend_calls':0,'approvals_created':0,'git_mutations':0}
dump(HERE/'author-freeze-r2.json',freeze)
dump(AUDIT/'author-freeze-r2.json',freeze)
print(json.dumps({'core_four_sha256':core,'native_units':nativecount,'lines':len(n),'scenes':len(doc['scenes']),'loops':len(doc['loops']),'lint_errors':0,'lint_warnings':len(lint['warnings']),'native_narrative_warnings':0,'protected_files_unchanged':len(before),'raw_downloads_checked':len(inv['items']),'replay_exact':True},ensure_ascii=False,indent=2))
