"""Build the R7 recap deletion delta from immutable R6 inputs.

Historical actions, source anchors, stable IDs, visual data and approved main
thread are retained. An author build never grants source or narrative approval.
"""
from pathlib import Path
import copy
import hashlib
import json
import subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
REPO = BASE.parents[3]
R6 = OUT / 'history' / 'r6'
CANONICAL_ROOT = Path('/workspace/work/brand-story-20261025/submission-root')
CANONICAL = CANONICAL_ROOT / 'docs/videos/story-everyday-patagonia-c09-remake-20261025'
SHA = lambda data: hashlib.sha256(data).hexdigest()
FILE_SHA = lambda file: SHA(file.read_bytes())
dump = lambda file, value: file.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
R6_INPUTS = {
    'video.json': 'f12dd1a611783ccbfd94377d5c79b7099d9b14541f49d602e6a8abe9ec228962',
    'script.md': 'be8d0331bb468c9c33ac4cd17670e13503f0594455aceb9504fea1a117edc88f',
    'narration-only.json': '9fb48e140406d089e4555e8a26c47cc7a12b4d4e62477428d915167e35dc23d4',
    'claims.json': 'edc8bbf93db92cb206851f11e92539327d095eb39121f67840e1bc847e10aea1',
}
for name, expected in R6_INPUTS.items():
    assert FILE_SHA(R6 / name) == expected, name

protected_paths = [file for file in BASE.rglob('*') if file.is_file() and OUT not in file.parents]
protected_paths += [file for sub in ['history', 'reviews'] for file in (OUT / sub).rglob('*') if file.is_file()]
protected_paths += [file for file in CANONICAL.rglob('*') if file.is_file()]
protected_before = {str(file): FILE_SHA(file) for file in protected_paths}

old_sections = json.loads((R6 / 'r6-lines.json').read_text())
sections = json.loads((OUT / 'r7-lines.json').read_text())
old_rows = {row[0]: row for section in old_sections for row in section['rows']}
rows = {row[0]: row for section in sections for row in section['rows']}
deleted = ['use_reaction', 'catalog_start', 'climb_reaction', 'outro_answer']
changed = ['use_letter_q', 'use_larger', 'catalog_guides', 'climb_target', 'climb_trust_q']
assert set(old_rows) - set(rows) == set(deleted)
assert not set(rows) - set(old_rows)
assert {key for key in rows if rows[key] != old_rows[key]} == set(changed)
assert [section.get('chapter') for section in sections] == [section.get('chapter') for section in old_sections]
assert all(rows[key][2:] == old_rows[key][2:] for key in rows)

doc = json.loads((R6 / 'video.json').read_text())
series = json.loads((R6 / 'series.json').read_text())
old_claims = json.loads((R6 / 'claims.json').read_text())
old_claim_by_key = {row['key']: row for row in old_claims}
key_to_id = {key: row['id'] for key, row in old_claim_by_key.items()}
id_to_key = {value: key for key, value in key_to_id.items()}
deleted_ids = {key_to_id[key] for key in deleted}
chapter_moves = []
retained_scenes = []
pending_chapter = None
for original in doc['scenes']:
    scene = copy.deepcopy(original)
    if scene.get('lines') and all(line['id'] in deleted_ids for line in scene['lines']):
        if scene.get('chapter'):
            pending_chapter = {'chapter': scene['chapter'], 'from_scene': scene['id']}
        continue
    scene['lines'] = [line for line in scene.get('lines', []) if line['id'] not in deleted_ids]
    for line in scene['lines']:
        line['text'] = rows[id_to_key[line['id']]][1]
    if pending_chapter:
        assert not scene.get('chapter')
        scene['chapter'] = pending_chapter['chapter']
        chapter_moves.append({**pending_chapter, 'to_scene': scene['id']})
        pending_chapter = None
    retained_scenes.append(scene)
assert pending_chapter is None
doc['scenes'] = retained_scenes

loop_changes = []
for loop in doc['loops']:
    if loop['payoff'] == key_to_id['outro_answer']:
        before = copy.deepcopy(loop)
        loop['payoff'] = key_to_id['climb_first']
        loop['what'] = '賣家自己把重量交給楔塊時，第一次實際承重的結果'
        loop_changes.append({'operation': 'rebind', 'before': before, 'after': copy.deepcopy(loop), 'reason': '刪除末尾歸納後，指向5091首次實際承重的直接動作，不以新標籤冒充額外結果。'})
assert len(doc['loops']) == 28
assert {'setup': key_to_id['resistance_viewer'], 'payoff': key_to_id['climb_finish'], 'what': '提出換用楔塊要求的人，能否親自完成一條大岩壁路線'} in doc['loops']
all_ids = {line['id'] for scene in doc['scenes'] for line in scene['lines']}
assert all(loop['setup'] in all_ids and loop['payoff'] in all_ids for loop in doc['loops'])

claims = []
for original in old_claims:
    if original['key'] in deleted:
        continue
    row = copy.deepcopy(original)
    row['text'] = rows[row['key']][1]
    assert row['candidate_evidence'] == original['candidate_evidence']
    claims.append(row)
narration = []
for section in sections:
    chapter = sections[-2]['chapter'] if section.get('outro') else section['chapter']
    narration.extend({'chapter': chapter, 'id': key_to_id[key], 'text': text} for key, text, refs, action in section['rows'])
assert [row['id'] for row in narration] == [line['id'] for scene in doc['scenes'] for line in scene['lines']]
assert len(narration) == 103
series['production_status'] = 'r7_candidate_unapproved_pending_independent_source_delta_and_two_new_isolated_readers'
dump(OUT / 'video.json', doc)
dump(OUT / 'series.json', series)
dump(OUT / 'narration-only.json', narration)
dump(OUT / 'claims.json', claims)

script = ['# C09 R7 作者附來源稿｜器材商的勸告如何承重', '', '狀態：HOLD，待獨立來源／書面配鏡差分及兩位全新隔離讀者；不是owner核准，不沿用R6批准。', '']
last_chapter = None
for row in claims:
    if row['chapter'] != last_chapter:
        script += ['## ' + row['chapter'], '']
        last_chapter = row['chapter']
    script += [f"[{row['id']}] {row['text']}", f"來源：{row['source']}；{row['anchor']}", '']
(OUT / 'script.md').write_text('\n'.join(script).rstrip() + '\n')

old_claims_md = (R6 / 'claims.md').read_text()
source_boundaries = '## 原始輸入與來源界線' + old_claims_md.split('## 原始輸入與來源界線', 1)[1].split('## c09r5001', 1)[0]
md = ['# C09 R7 逐句來源對照', '', '全部狀態為 PENDING_INDEPENDENT_REVIEW。來源引用是可稽核錨點，不是本作者自授PASS。', '', 'R7以R6為基準刪除重述：四句全刪、三句只撤後半歸納、兩個原有問句改為第一人稱反應。歷史動作、來源錨點、來源bytes與留存鏡頭prompt均不改；不新增史實或支線。R6完整輸入與原結果保留於history/r6，R7不沿用核准。', '', source_boundaries.rstrip(), '']
for row in claims:
    md += [f"## {row['id']} · {row['key']}", '', row['text'], '', f"來源：{row['source']}；錨點：{row['anchor']}", '']
    for evidence in row.get('candidate_evidence', []):
        md += [f"- {evidence['source']}:{evidence['paragraph']}，paragraph SHA256 `{evidence['paragraph_sha256']}`；cache SHA256 `{evidence['cache_sha256']}`。", '  > ' + evidence['short_quote']]
    md += ['']
(OUT / 'claims.md').write_text('\n'.join(md).rstrip() + '\n')

brief = (R6 / 'brief.md').read_text()
brief = brief.replace('# C09 R6｜', '# C09 R7｜', 1)
brief = brief.replace('R5完整輸入及原結果保留於history/r5', 'R6完整輸入及原結果保留於history/r6')
brief = brief.split('## 後續', 1)[0] + '''## 後續

BASE、canonical、舊核准、八語譯文、history與reviews不改。R7刪除章首重講型錄要求、末尾重述親自承重，以及兩句只回看前文的旁白歸納；另三句保留首次史實、撤去後半同義總結。原有兩個未解問句用旁白的「我想知道」承接，保留每章對觀眾及個人反應。留存鏡頭的prompt、camera、emotion及來源錨點均不改。開場問題直接回收到5091首次承重的動作；5068到5106的完成結果回收不動。

正文2737個朗讀單位，實聲尚未量測，720–840秒目標可能不足；不灌字、慢播或加停頓。改字與loop端點仍須獨立複核。原生字典context lint只檢查機械條件；未寫verify、未呼叫後台或付費供應商。
'''
(OUT / 'brief.md').write_text(brief)

native_code = r"""
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {loadProject,lintProject} from './tools/video/core/state.mjs';
import {spokenUnits,estimateTimeline,FPS,DEFAULT_CPM} from './tools/video/core/timeline.mjs';
import {spokenText} from './tools/video/core/schema.mjs';
import {hookCadenceProblems,TIGHT_CADENCE} from './tools/video/core/narrative.mjs';
const candidate=process.argv[1],root=process.argv[2],slug='story-everyday-patagonia-c09-remake-20261025';
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const project=loadProject({root,slug});const binding={canonical_video_sha256:sha(project.file),canonical_file:project.file,lexicon_initialized_terms:Object.keys(project.lexicon.terms??{}).length,lexicon_sha256:crypto.createHash('sha256').update(JSON.stringify(project.lexicon)).digest('hex'),preserved_fields:['lexicon','shelfLexicon','translations','others','pack','file','dir']};
project.doc=JSON.parse(fs.readFileSync(path.join(candidate,'video.json')));project.brief=fs.readFileSync(path.join(candidate,'brief.md'),'utf8');project.series=JSON.parse(fs.readFileSync(path.join(candidate,'series.json')));
const doc=project.doc,result=lintProject(project),timeline=estimateTimeline(doc),flat=doc.scenes.flatMap(scene=>scene.lines??[]),sum=lines=>lines.reduce((n,line)=>n+spokenUnits(spokenText(line)),0),first=doc.scenes.findIndex((scene,i)=>i>0&&scene.chapter),opening=sum(doc.scenes.slice(0,first).flatMap(scene=>scene.lines??[])),total=sum(flat),closing=sum(doc.scenes.filter(scene=>scene.template==='outro').flatMap(scene=>scene.lines??[]));
const shots=doc.scenes.filter(scene=>scene.template==='shot'),seconds=Object.fromEntries(timeline.scenes.map(scene=>[scene.id,(scene.end_frame-scene.start_frame)/FPS]));
const previous=JSON.parse(fs.readFileSync(path.join(candidate,'history/r6/video.json'))),oldLines=new Map(previous.scenes.flatMap(scene=>scene.lines??[]).map(line=>[line.id,line])),newLines=new Map(flat.map(line=>[line.id,line]));
const delta=[...oldLines].filter(([id,line])=>!newLines.has(id)||newLines.get(id).text!==line.text).map(([id,line])=>({id,operation:newLines.has(id)?'replace':'delete',before_units:sum([line]),after_units:newLines.has(id)?sum([newLines.get(id)]):0,net_units:(newLines.has(id)?sum([newLines.get(id)]):0)-sum([line])}));
const chapters=doc.scenes.filter(scene=>scene.chapter).map((scene,index,all)=>{const at=doc.scenes.indexOf(scene),next=all[index+1]?doc.scenes.indexOf(all[index+1]):doc.scenes.length,text=doc.scenes.slice(at,next).filter(item=>item.template!=='outro').flatMap(item=>item.lines??[]).map(line=>line.text).join('');return{chapter:scene.chapter,you:(text.match(/你/g)??[]).length,narrator:(text.match(/我/g)??[]).length};});
console.log(JSON.stringify({context_binding:binding,result,units:{total,opening,body_after_opening:total-opening,closing,body_excluding_opening_and_closing:total-opening-closing},line_count:flat.length,scene_count:doc.scenes.length,shot_count:shots.length,chapter_count:chapters.length,chapter_address:chapters,loop_count:doc.loops.length,max_estimated_shot_seconds:Math.max(...shots.map(scene=>seconds[scene.id])),shot_time_share:shots.reduce((n,scene)=>n+seconds[scene.id],0)/(timeline.total_frames/FPS),cadence_problems:hookCadenceProblems(doc,timeline,TIGHT_CADENCE.gap),timeline_estimated_minutes:timeline.total_frames/FPS/60,default_cpm:DEFAULT_CPM,actual_timing_verified:false,delta}));
"""
run = subprocess.run(['node', '--input-type=module', '-e', native_code, str(OUT), str(CANONICAL_ROOT)], cwd=REPO, capture_output=True, text=True, check=True)
native = json.loads(run.stdout)
dump(OUT / 'author-local-lint-r7.json', native)
assert native['units'] == {'total': 2916, 'opening': 179, 'body_after_opening': 2737, 'closing': 56, 'body_excluding_opening_and_closing': 2681}
assert not native['result']['errors'], native['result']['errors']
assert not native['cadence_problems'], native['cadence_problems']
assert native['max_estimated_shot_seconds'] <= 12
assert native['shot_time_share'] >= .7
assert all(chapter['you'] and chapter['narrator'] for chapter in native['chapter_address'])

retained_old_scenes = {scene['id']: scene for scene in json.loads((R6 / 'video.json').read_text())['scenes']}
for scene in doc['scenes']:
    original = copy.deepcopy(retained_old_scenes[scene['id']])
    original['lines'] = [line for line in original['lines'] if line['id'] not in deleted_ids]
    for line in original['lines']:
        line['text'] = rows[id_to_key[line['id']]][1]
    for move in chapter_moves:
        if move['to_scene'] == original['id']:
            original['chapter'] = move['chapter']
    assert scene == original, scene['id']

reasons = {
    'use_reaction': '刪去對剛說過的器材動作與習慣作總結；5038保留原有可被回信回答的問題。',
    'catalog_start': '開場5004已說自家型錄要求克制，章首不再重報。',
    'climb_reaction': '刪去對剛發生的承重與放置困難作信服／用法歸納；5097保留原有下一個真實結果問題。',
    'outro_answer': '5091已第一次交付修納德親自承重的動作，末尾不再概括同一行為。',
    'use_letter_q': '僅將原有未解問題改為旁白反應，不新增事實或另說已知結果。',
    'use_larger': '保留裂縫從小釘改需大釘的首次史實，撤去「尺寸跟著傷痕走」的同義歸納。',
    'catalog_guides': '保留寫進當地指南的首次具體方法，撤去資訊傳給下一人的同義歸納。',
    'climb_target': '保留Nose目標，撤去再說一次「從冊子走到實際攀登」的主題總結。',
    'climb_trust_q': '僅將原有未解問題改為旁白反應，隨後仍由卡森自己的記錄回答。',
}
delta = {
    'revision': 'length-extension-r7',
    'status': 'HOLD_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_DELTA_AND_TWO_NEW_ISOLATED_READERS',
    'baseline': 'history/r6',
    'baseline_input_sha256': R6_INPUTS,
    'retained_ids_and_unmodified_visuals_preserved': True,
    'deleted_lines': [{'id': key_to_id[key], 'key': key, 'text': old_rows[key][1], 'reason': reasons[key]} for key in deleted],
    'modified_lines': [{'id': key_to_id[key], 'key': key, 'before_text': old_rows[key][1], 'after_text': rows[key][1], 'source_anchor': rows[key][2], 'reason': reasons[key]} for key in changed],
    'modified_visuals': [],
    'chapter_moves': chapter_moves,
    'loop_changes': loop_changes,
    'protected_true_payoff': {'setup': 'c09r5068', 'payoff': 'c09r5106', 'unchanged': True},
    'units_by_line': native['delta'],
    'net_spoken_units': sum(row['net_units'] for row in native['delta']),
    'unchanged_retained_narration_lines': len(narration) - len(changed),
    'unchanged_retained_scene_visuals': len(doc['scenes']),
    'source_bytes_changed': False,
    'source_anchors_changed': False,
    'new_historical_claims': False,
    'new_sources': [],
    'actual_audio_measured': False,
    'runtime_risk': 'Body after the cold opening is 2737 spoken units, down from 2918. Natural 4–5 units per second may miss 720–840 seconds. No runtime approval, slowdown, pauses, or padding.',
}
assert delta['net_spoken_units'] == -181
dump(OUT / 'author-delta-r7.json', delta)

after = {str(file): FILE_SHA(file) for file in protected_paths}
assert protected_before == after, [file for file in protected_before if protected_before[file] != after.get(file)]
old_notes = json.loads((R6 / 'author-notes.json').read_text())
notes = {
    'status': delta['status'],
    'revision': 'length-extension-r7',
    'author': '/root/c09_r5_author',
    'author_is_not_source_reviewer': True,
    'r6_input_sha256': R6_INPUTS,
    'current_input_sha256': {name: FILE_SHA(OUT / name) for name in ['video.json', 'script.md', 'narration-only.json', 'claims.json', 'claims.md', 'brief.md', 'series.json', 'r7-lines.json', 'build-r7.py', 'author-delta-r7.json']},
    'editorial_delta': delta,
    'new_primary_source': copy.deepcopy(old_notes['new_primary_source']),
    'r5_r6_source_qa_advisories_retained': copy.deepcopy(old_notes['r5_source_qa_advisories_retained']),
    'native_initialized_context_lint': native,
    'legacy_opening_loop_count_warning': old_notes['legacy_opening_loop_count_warning'],
    'protected_existing_files_count': len(protected_before),
    'protected_existing_files_unchanged': True,
    'protected_manifest_sha256': SHA(json.dumps(protected_before, sort_keys=True).encode()),
    'old_approvals_inherited': False,
    'verify_written_by_author': False,
    'actual_audio_measured': False,
    'media_generated': False,
    'backend_calls': 0,
    'paid_calls': 0,
}
dump(OUT / 'author-notes.json', notes)
print(json.dumps({'input_sha256': notes['current_input_sha256'], 'units': native['units'], 'line_count': native['line_count'], 'scene_count': native['scene_count'], 'shot_count': native['shot_count'], 'chapter_count': native['chapter_count'], 'loop_count': native['loop_count'], 'errors': native['result']['errors'], 'warning_count': len(native['result']['warnings']), 'cadence_problems': native['cadence_problems'], 'max_estimated_shot_seconds': native['max_estimated_shot_seconds'], 'shot_time_share': native['shot_time_share'], 'net_spoken_units': delta['net_spoken_units'], 'protected_files': len(protected_before), 'status': notes['status']}, ensure_ascii=False))
