"""Build the targeted R6 author revision from the immutable R5 archive.

Retained IDs, emotions, cameras, and prompts stay stable. This is an editorial
delta, not a new all-scene rewrite or an approval of any production stage.
"""
from pathlib import Path
import copy
import hashlib
import json
import subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
REPO = BASE.parents[3]
R5 = OUT / 'history' / 'r5'
WORK = Path('/workspace/work/brand-story-20261025/c09-audit')
CANONICAL_ROOT = Path('/workspace/work/brand-story-20261025/submission-root')
CANONICAL = CANONICAL_ROOT / 'docs/videos/story-everyday-patagonia-c09-remake-20261025'
SHA = lambda b: hashlib.sha256(b).hexdigest()
FILE_SHA = lambda f: SHA(f.read_bytes())
dump = lambda p, value: p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

R5_INPUTS = {
    'video.json': '22029a19ce8643fc7694ee78b186f68db93acbde9ce7ae70cd3d5928dfee1ff1',
    'script.md': '0ddbec18d204ecc22fe210c915f618636c224ebb823a86d81d22bccfa503d64a',
    'narration-only.json': 'ace0923859bd9ecf2d85a0feb225cadbcee7eda1475b4beb6d519bc0041c56a6',
    'claims.json': '9d22c84c69a70d31fceec4bc6a986081fe8a335211c7baa867dea37e169fd12d',
}
for name, expected in R5_INPUTS.items():
    assert FILE_SHA(R5 / name) == expected, name

protected_paths = [f for f in BASE.rglob('*') if f.is_file() and OUT not in f.parents]
protected_paths += [f for sub in ['history', 'reviews'] for f in (OUT / sub).rglob('*') if f.is_file()]
protected_paths += [f for f in CANONICAL.rglob('*') if f.is_file()]
protected_before = {str(f): FILE_SHA(f) for f in protected_paths}

old_sections = json.loads((R5 / 'r5-lines.json').read_text())
sections = json.loads((OUT / 'r6-lines.json').read_text())
old_rows = {r[0]: r for section in old_sections for r in section['rows']}
rows = {r[0]: r for section in sections for r in section['rows']}
deleted = ['use_rockscar', 'resistance_money_q', 'resistance_hypocrisy', 'resistance_reaction', 'resistance_end']
changed = ['use_rockhard', 'resistance_viewer']
assert set(old_rows) - set(rows) == set(deleted)
assert not set(rows) - set(old_rows)
assert {key for key in rows if rows[key] != old_rows[key]} == set(changed)
assert [s.get('chapter') for s in sections] == [s.get('chapter') for s in old_sections]

doc = json.loads((R5 / 'video.json').read_text())
series = json.loads((R5 / 'series.json').read_text())
old_claims = json.loads((R5 / 'claims.json').read_text())
old_claim_by_key = {r['key']: r for r in old_claims}
key_to_id = {key: row['id'] for key, row in old_claim_by_key.items()}
id_to_key = {value: key for key, value in key_to_id.items()}
deleted_ids = {key_to_id[key] for key in deleted}

retained_scenes = []
for original in doc['scenes']:
    if any(line['id'] in deleted_ids for line in original.get('lines', [])):
        assert len(original['lines']) == 1 and 'chapter' not in original
        continue
    scene = copy.deepcopy(original)
    for line in scene.get('lines', []):
        line['text'] = rows[id_to_key[line['id']]][1]
    if any(line['id'] == key_to_id['resistance_viewer'] for line in scene.get('lines', [])):
        scene['data']['prompt'] = 'Medium shot at a plain granite practice area, one unidentified person examining a small unmarked metal wedge below a tall rock surface, soft overcast light.'
    retained_scenes.append(scene)
doc['scenes'] = retained_scenes

loops = []
loop_changes = []
for original in doc['loops']:
    loop = copy.deepcopy(original)
    if loop['setup'] == key_to_id['resistance_money_q']:
        replacement = {'setup': key_to_id['resistance_viewer'], 'payoff': key_to_id['climb_finish'], 'what': '提出換用楔塊要求的人，能否親自完成一條大岩壁路線'}
        loops.append(replacement)
        loop_changes.append({'operation': 'replace', 'before': original, 'after': replacement})
        continue
    if loop['setup'] == key_to_id['resistance_end']:
        loop_changes.append({'operation': 'delete', 'before': original})
        continue
    if loop['setup'] == key_to_id['use_rock_q']:
        loop['payoff'] = key_to_id['use_rockhard']
        loop['what'] = '花崗岩與鋼釘的材質差異，怎樣使薄岩片鬆落'
        loop_changes.append({'operation': 'rebind', 'before': original, 'after': loop})
    loops.append(loop)
doc['loops'] = loops
assert len(loops) == 28
all_ids = {line['id'] for scene in doc['scenes'] for line in scene.get('lines', [])}
assert all(loop['setup'] in all_ids and loop['payoff'] in all_ids for loop in loops)

source_files = {sid: WORK / 'source-cache' / (sid + '.paragraphs.txt') for sid in ['S1', 'S2', 'S3', 'S4']}
source_files['S8'] = WORK / 'r5-source/S8.paragraphs.txt'
paragraphs = {}
for sid, f in source_files.items():
    paragraphs[sid] = {line[:3]: line[4:] for line in f.read_text().splitlines() if line[:3].isdigit() and line[3:4] == ' '}
S8_PDF = WORK / 'r5-source/S8.pdf'
assert FILE_SHA(S8_PDF) == '8cbc2bba3bf9a39035dc9167bb9a303acce4ac9bdb45b5810d8380648ad2bfdc'
assert FILE_SHA(WORK / 'r5-source/S8.html') == 'd250cd07512be13f66ae7f8219f5b1024574846f20d555dfec9e0f2ea9aa2b28'

def evidence_for(refs):
    evidence = []
    for ref in refs.split(';'):
        sid, para = ref.split(':')
        original = paragraphs[sid][para]
        item = {'source': sid, 'cache_path': str(source_files[sid]), 'cache_sha256': FILE_SHA(source_files[sid]), 'paragraph': para, 'paragraph_sha256': SHA(original.encode()), 'short_quote': original[:220], 'quote_is_exact_prefix': True}
        if sid == 'S8':
            p = int(para)
            item['original_pdf'] = str(S8_PDF)
            item['original_pdf_sha256'] = FILE_SHA(S8_PDF)
            item['original_pdf_pages'] = [1] if p < 10 else [2, 3] if p == 19 else [2] if p < 19 else [3]
            item['publication_year'] = 1974
            item['event_year'] = 1973
        evidence.append(item)
    return evidence

claims = []
for old in old_claims:
    key = old['key']
    if key in deleted:
        continue
    claim = copy.deepcopy(old)
    if key in changed:
        claim['text'] = rows[key][1]
        claim['anchor'] = rows[key][2]
        claim['candidate_evidence'] = evidence_for(rows[key][2])
        claim['source'] = '、'.join(dict.fromkeys(e['source'] for e in claim['candidate_evidence']))
    claims.append(claim)

narration = []
for section in sections:
    chapter = sections[-2]['chapter'] if section.get('outro') else section['chapter']
    narration.extend({'chapter': chapter, 'id': key_to_id[key], 'text': text} for key, text, refs, action in section['rows'])
assert [row['id'] for row in narration] == [line['id'] for scene in doc['scenes'] for line in scene.get('lines', [])]
assert len(narration) == 107

# Keep the already-reviewed story, packaging, source list, and all other scene data.
series['production_status'] = 'r6_candidate_unapproved_pending_independent_source_delta_and_two_new_isolated_readers'
dump(OUT / 'video.json', doc)
dump(OUT / 'series.json', series)
dump(OUT / 'narration-only.json', narration)
dump(OUT / 'claims.json', claims)

script = ['# C09 R6 作者附來源稿｜器材商的勸告如何承重', '', '狀態：HOLD，待獨立來源／書面配鏡差分及兩位全新隔離讀者；不是owner核准，不沿用R5批准。', '']
last_chapter = None
for row in claims:
    chapter = row['chapter']
    if chapter != last_chapter:
        script += ['## ' + chapter, '']
        last_chapter = chapter
    script += [f"[{row['id']}] {row['text']}", f"來源：{row['source']}；{row['anchor']}", '']
(OUT / 'script.md').write_text('\n'.join(script).rstrip() + '\n')

md = ['# C09 R6 逐句來源對照', '', '全部狀態為 PENDING_INDEPENDENT_REVIEW。來源引用是可稽核錨點，不是本作者自授PASS。', '', 'R6保留R5未改句子與場景ID，只撤五句、改兩句及一景prompt；來源bytes不變。R5完整輸入與原結果保留於history/r5，R6不沿用核准。', '', '## 原始輸入與來源界線', '', '- S1：1967年器材文章，描述當時作者提出的用法，不當現代攀登教學。5030的「希望」是流程概述，並非忽略原文外傾地形例外的操作法。', '- S2：只把重刊頁027–036當1972年前言；043的創辦人身分是現代編輯人物介紹。', '- S3：1973書評，私人批評、不同讀者立場及觀察均保留歸屬；東岸限定文字流傳，不限定作者籍貫。', '- S4：1977刊出採訪，1957/1964/1970等過去年份是文中明示回述；不把1977當到訪日。', '- S8：Bruce Carson原始第一人稱報告，1974年出版，敘述1973年。五月信、夏末約定、兩週後攀登依原文先後；1973年並由S4:009交叉對時。原文one of these不擴成他從未用過任何楔塊。', '- 四分之一英吋換算六公釐是近似換算，不當精密量測值；楔塊下沉不改成脫落、墜落或事故。', '- 早期卡森嘗試清楚說仍用既有螺栓；Nose的器材選擇只排除攜帶岩釘，沒有排除繩索或其他攀登裝備。', '- 5111及CTA是向觀眾提出的假設性問題，不是修納德曾主動出版、授權或有意披露不順利的史實。', '- 字數、估秒與書面配鏡均不是實際TTS或媒體驗收。', '']
for row in claims:
    md += [f"## {row['id']} · {row['key']}", '', row['text'], '', f"來源：{row['source']}；錨點：{row['anchor']}", '']
    for evidence in row.get('candidate_evidence', []):
        md += [f"- {evidence['source']}:{evidence['paragraph']}，paragraph SHA256 `{evidence['paragraph_sha256']}`；cache SHA256 `{evidence['cache_sha256']}`。", '  > ' + evidence['short_quote']]
    md += ['']
(OUT / 'claims.md').write_text('\n'.join(md).rstrip() + '\n')

brief = (R5 / 'brief.md').read_text()
brief = brief.replace('# C09 R5｜', '# C09 R6｜', 1)
brief = brief.replace('狀態：作者候選HOLD，待新的獨立來源、書面配鏡與兩位全新隔離讀者。R4來源PASS與敘事HOLD保留於history/r4；本版沒有沿用舊批准。', '狀態：作者候選HOLD，待新的獨立來源／書面配鏡差分與兩位全新隔離讀者。R5完整輸入及原結果保留於history/r5；本版沒有沿用舊批准。')
brief = brief.replace('## 新增原始來源', '## 沿用原始來源')
brief = brief.replace('原刊第59–60頁已目視，逐句錨點和hash見claims.json。', '原始bytes不變，逐句錨點和hash見claims.json。')
brief = brief.replace('原current、canonical、舊核准、八語譯文、history與reviews不改。本版所有新ID、改字、配鏡與source anchors均須獨立複核；原生字典context lint只檢查機械條件。未寫verify、未呼叫後台或付費供應商。', 'BASE、canonical、舊核准、八語譯文、history與reviews不改。本版保留未改句子與場景ID，撤五句、改兩句，讓公平質疑對到能被一次真實攀登回答的選擇；刪去口袋／動機問句、岩壁受損重報及第三次器材袋預告。改字、配鏡與source anchors仍須獨立複核。原生字典context lint只檢查機械條件；未寫verify、未呼叫後台或付費供應商。正文預計2918個朗讀單位，實聲尚未量測，720–840秒目標可能不足；不灌字、慢播或加停頓。')
(OUT / 'brief.md').write_text(brief)

native_code = r"""
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {loadProject,lintProject} from './tools/video/core/state.mjs';
import {spokenUnits,estimateTimeline,FPS,DEFAULT_CPM} from './tools/video/core/timeline.mjs';
import {spokenText} from './tools/video/core/schema.mjs';
import {hookCadenceProblems,TIGHT_CADENCE} from './tools/video/core/narrative.mjs';
const candidate=process.argv[1],root=process.argv[2],slug='story-everyday-patagonia-c09-remake-20261025';
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const project=loadProject({root,slug});const binding={canonical_video_sha256:sha(project.file),canonical_file:project.file,lexicon_initialized_terms:Object.keys(project.lexicon.terms??{}).length,lexicon_sha256:crypto.createHash('sha256').update(JSON.stringify(project.lexicon)).digest('hex'),preserved_fields:['lexicon','shelfLexicon','translations','others','pack','file','dir']};
project.doc=JSON.parse(fs.readFileSync(path.join(candidate,'video.json')));project.brief=fs.readFileSync(path.join(candidate,'brief.md'),'utf8');project.series=JSON.parse(fs.readFileSync(path.join(candidate,'series.json')));
const doc=project.doc,result=lintProject(project),timeline=estimateTimeline(doc),flat=doc.scenes.flatMap(s=>s.lines??[]),sum=ls=>ls.reduce((n,l)=>n+spokenUnits(spokenText(l)),0),first=doc.scenes.findIndex((s,i)=>i>0&&s.chapter),opening=sum(doc.scenes.slice(0,first).flatMap(s=>s.lines??[])),total=sum(flat),closing=sum(doc.scenes.filter(s=>s.template==='outro').flatMap(s=>s.lines??[]));
const shots=doc.scenes.filter(s=>s.template==='shot'),seconds=Object.fromEntries(timeline.scenes.map(s=>[s.id,(s.end_frame-s.start_frame)/FPS]));
const previous=JSON.parse(fs.readFileSync(path.join(candidate,'history/r5/video.json'))),oldLines=new Map(previous.scenes.flatMap(s=>s.lines??[]).map(l=>[l.id,l])),newLines=new Map(flat.map(l=>[l.id,l]));
const delta=[...oldLines].filter(([id,l])=>!newLines.has(id)||newLines.get(id).text!==l.text).map(([id,l])=>({id,operation:newLines.has(id)?'replace':'delete',before_units:sum([l]),after_units:newLines.has(id)?sum([newLines.get(id)]):0,net_units:(newLines.has(id)?sum([newLines.get(id)]):0)-sum([l])}));
console.log(JSON.stringify({context_binding:binding,result,units:{total,opening,body_after_opening:total-opening,closing,body_excluding_opening_and_closing:total-opening-closing},line_count:flat.length,scene_count:doc.scenes.length,shot_count:shots.length,chapter_count:doc.scenes.filter(s=>s.chapter).length,loop_count:doc.loops.length,max_estimated_shot_seconds:Math.max(...shots.map(s=>seconds[s.id])),shot_time_share:shots.reduce((n,s)=>n+seconds[s.id],0)/(timeline.total_frames/FPS),cadence_problems:hookCadenceProblems(doc,timeline,TIGHT_CADENCE.gap),timeline_estimated_minutes:timeline.total_frames/FPS/60,default_cpm:DEFAULT_CPM,actual_timing_verified:false,delta}));
"""
run = subprocess.run(['node', '--input-type=module', '-e', native_code, str(OUT), str(CANONICAL_ROOT)], cwd=REPO, capture_output=True, text=True, check=True)
native = json.loads(run.stdout)
dump(OUT / 'author-local-lint-r6.json', native)
assert native['units'] == {'total': 3097, 'opening': 179, 'body_after_opening': 2918, 'closing': 88, 'body_excluding_opening_and_closing': 2830}
assert not native['result']['errors'], native['result']['errors']
assert not native['cadence_problems'], native['cadence_problems']
assert native['max_estimated_shot_seconds'] <= 12
assert native['shot_time_share'] >= .7

retained_old_scenes = {s['id']: s for s in json.loads((R5 / 'video.json').read_text())['scenes']}
for scene in doc['scenes']:
    original = copy.deepcopy(retained_old_scenes[scene['id']])
    for line in original.get('lines', []):
        line['text'] = rows[id_to_key[line['id']]][1]
    if scene['id'] == 'c09r5-shot-068':
        original['data']['prompt'] = scene['data']['prompt']
    assert scene == original, scene['id']

delta = {
    'revision': 'length-extension-r6',
    'status': 'HOLD_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_DELTA_AND_TWO_NEW_ISOLATED_READERS',
    'baseline': 'history/r5',
    'baseline_input_sha256': R5_INPUTS,
    'retained_ids_and_unmodified_visuals_preserved': True,
    'deleted_ids': [key_to_id[key] for key in deleted],
    'modified_lines': [{'id': key_to_id[key], 'key': key, 'before_text': old_rows[key][1], 'after_text': rows[key][1], 'before_anchor': old_claim_by_key[key]['anchor'], 'after_anchor': rows[key][2]} for key in changed],
    'modified_visuals': [{'scene_id': 'c09r5-shot-068', 'field': 'data.prompt', 'before': retained_old_scenes['c09r5-shot-068']['data']['prompt'], 'after': next(s for s in doc['scenes'] if s['id'] == 'c09r5-shot-068')['data']['prompt']}],
    'loop_changes': loop_changes,
    'units_by_line': native['delta'],
    'net_spoken_units': sum(row['net_units'] for row in native['delta']),
    'unchanged_retained_narration_lines': len(narration) - len(changed),
    'unchanged_retained_scene_visuals': len(doc['scenes']) - 1,
    'source_bytes_changed': False,
    'new_sources': [],
    'actual_audio_measured': False,
    'runtime_risk': 'Body after the cold opening is 2918 spoken units; natural 4–5 units per second may miss 720–840 seconds. No runtime approval, slowdown, pauses, or inventory padding.',
}
assert delta['net_spoken_units'] == -149
dump(OUT / 'author-delta-r6.json', delta)

after = {str(f): FILE_SHA(f) for f in protected_paths}
assert protected_before == after, [f for f in protected_before if protected_before[f] != after.get(f)]
old_notes = json.loads((R5 / 'author-notes.json').read_text())
notes = {
    'status': delta['status'],
    'revision': 'length-extension-r6',
    'author': '/root/c09_r5_author',
    'author_is_not_source_reviewer': True,
    'r5_input_sha256': R5_INPUTS,
    'current_input_sha256': {f: FILE_SHA(OUT / f) for f in ['video.json', 'script.md', 'narration-only.json', 'claims.json', 'claims.md', 'brief.md', 'series.json', 'r6-lines.json', 'build-r6.py', 'author-delta-r6.json']},
    'editorial_delta': delta,
    'new_primary_source': copy.deepcopy(old_notes['new_primary_source']),
    'r5_source_qa_advisories_retained': [
        {'id': 'c09r5030', 'limit': '「希望」是原文流程概述，不把它當成忽略外傾地形例外的操作法。'},
        {'ids': ['c09r5111', 'c09r5-outro.data.cta'], 'limit': '假設性觀眾問題，非修納德曾出版、授權或有意披露不順利的史實。'},
    ],
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
