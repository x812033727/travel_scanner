import pathlib,json,hashlib,shutil,datetime
repo=pathlib.Path('/workspace/work/brand-remakes-source');out=repo/'docs/videos/brand-story-remakes-20261025/dyson';audit=pathlib.Path('/workspace/work/brand-story-20261025/dyson-audit/author-r4');cap=pathlib.Path('/workspace/work/brand-story-20261025/dyson-audit/capacity-r4');hist=out/'history/r3';sha=lambda b:hashlib.sha256(b).hexdigest()
f=json.loads((out/'author-freeze-r3.json').read_text());assert sha((out/'author-freeze-r3.json').read_bytes())=='ff99e793929fd513c40e6e08d19e29bf66a5b5b304469970a22210a57c6bec99';assert sha((out/'video.json').read_bytes())=='f28f3feb6ea49867acd60157688f9ae675a5d0eddfa711de0cb983f991555969'
for n,h in f['file_sha256'].items():assert sha((out/n).read_bytes())==h,n
assert not hist.exists()
base=json.loads((cap/'protected-before.json').read_text());assert len(base['files'])==316
for path,v in base['files'].items():assert sha(pathlib.Path(path).read_bytes())==v['sha256'],path
# Existing R4 capacity report is research input, not a fictional R3 source artifact.
files=[p for p in sorted(out.rglob('*')) if p.is_file() and 'history' not in p.relative_to(out).parts and p.name not in {'capacity-primary-research-r4.md','capacity-primary-research-r4.json'}]
for p in files:
 q=hist/p.relative_to(out);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert q.read_bytes()==p.read_bytes()
runtime=pathlib.Path('/workspace/work/brand-story-20261025/dyson-audit/author-r3/runtime');sdir=runtime/'docs/videos/story-dyson-japan-first-20261021-remake-20261025';assert (sdir/'video.json').read_bytes()==(out/'video.json').read_bytes()
shutil.copytree(sdir,hist/'runtime-project-snapshot');shutil.copyfile(runtime/'runtime-manifest.json',hist/'runtime-manifest.json');shutil.copyfile(runtime/'docs/videos/lexicon.json',hist/'runtime-shared-lexicon.json')
state={'schema_version':1,'revision':'dyson-r3','source_state':'NOT_REVIEWED_NO_SOURCE_PASS','native_state':'R3_NOT_PREPARED_NOT_READ','actual_native_round_count':1,'last_actual_native_round':'R2_SOURCE_ACTUAL_NATIVE1_MERGED_HOLD','next_fresh_round':2,'no_r3_native_round_invented':True,'no_r3_verify':True,'planning_capacity':'HOLD','owner_approval_created':False,'paid_calls':0}
(hist/'native-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
items=[{'path':str(p.relative_to(hist)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(hist.rglob('*')) if p.is_file()]
(hist/'history-manifest.json').write_text(json.dumps({'schema_version':1,'role':'HASH_BOUND_R3_UNREVIEWED_AUTHOR_SOURCE_ARCHIVE_NOT_APPROVAL','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_files_copied':len(files),'all_archived_files':items,'actual_native_round_count':1,'source_state':'R3_UNREVIEWED','fresh_native2':'NOT_PREPARED_NOT_READ','prior_r3_freeze_sha256':'ff99e793929fd513c40e6e08d19e29bf66a5b5b304469970a22210a57c6bec99'},ensure_ascii=False,indent=2)+'\n')
research=json.loads((out/'capacity-primary-research-r4.json').read_text());actualclaims=sha((out/'claims.json').read_bytes());reportedclaims=research['baseline']['claims_sha256']
notice={'field':'baseline.claims_sha256','reported':reportedclaims,'actual_frozen_R3_bytes':actualclaims,'r3_author_freeze_and_protected316_manifest_agree_with_actual':True,'research_input_edited':False,'use_for_R3_binding':'Actual bytes/author-freeze-r3/protected316, not this mistyped baseline field.'}
assert reportedclaims!=actualclaims
# Preserve every316 pre-R4 byte. Mutable R3 author inputs are archived before R4 replacement;
# original evidence, histories, dictionaries and external R3 runtime stay at their original locations.
protected={}
immutable_names={'research-original.md','research-original.claims.json','original-preservation.json','capacity-primary-research-r4.md','capacity-primary-research-r4.json'}
mapped=[]
for path,v in base['files'].items():
 p=pathlib.Path(path);q=p
 if p.is_relative_to(out):
  rel=p.relative_to(out)
  if 'history' not in rel.parts and p.name not in immutable_names:
   q=hist/rel;assert q.exists();mapped.append({'original_path':str(p),'archive_path':str(q),'sha256':v['sha256']})
 assert sha(q.read_bytes())==v['sha256'];protected[str(q)]={'path':str(q),'original_path':str(p),'bytes':q.stat().st_size,'sha256':v['sha256'],'preservation':'R3-author-bytes-archived' if q!=p else 'original-location-immutable'}
for parent in [hist,cap]:
 for p in parent.rglob('*'):
  if p.is_file():protected[str(p)]={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'preservation':'archived-or-new-primary-immutable'}
for n in immutable_names:
 p=out/n;protected[str(p)]={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'preservation':'original-location-immutable'}
manifest={'schema_version':1,'role':'R4_PRESERVATION_BEFORE_AUTHOR_NOT_APPROVAL','source_original316_manifest_sha256':sha((cap/'protected-before.json').read_bytes()),'original316_count':316,'mutable_R3_author_inputs_preserved_by_archive':mapped,'files':list(protected.values()),'r4_research_files_sha256':{n:sha((out/n).read_bytes()) for n in ['capacity-primary-research-r4.md','capacity-primary-research-r4.json']},'baseline_discrepancy_notice':notice,'actual_native_round_count':1,'fresh_native2':'NOT_PREPARED_NOT_READ'}
(audit/'protected-before-r4.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(audit/'r4-research-baseline-field-notice.json').write_text(json.dumps(notice,ensure_ascii=False,indent=2)+'\n')
for p in hist.rglob('*'):
 if p.is_file():p.chmod(0o444)
print(json.dumps({'r3_source_files_archived':len(files),'r3_archive_total':len(items),'original316_all_bytes_preserved':True,'author_inputs_mapped_to_history':len(mapped),'protected_entries':len(protected),'research_baseline_discrepancy':notice},ensure_ascii=False,indent=2))
