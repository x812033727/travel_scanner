from pathlib import Path
import copy, datetime, hashlib, json, subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
REPO = BASE.parents[3]
R4 = OUT / 'history' / 'r4'
WORK = Path('/workspace/work/brand-story-20261025/c09-audit')
CANONICAL_ROOT = Path('/workspace/work/brand-story-20261025/submission-root')
CANONICAL = CANONICAL_ROOT / 'docs/videos/story-everyday-patagonia-c09-remake-20261025'
SHA = lambda b: hashlib.sha256(b).hexdigest()
FILE_SHA = lambda f: SHA(f.read_bytes())
R4_INPUTS = {
    'video.json': '8fc4ada68f086f68532f3c317606018273f9d291885e2833795bfc14efab1aad',
    'script.md': 'f9cae91c7b169ef557eefcf7f9568414a175f4b440d05d193f5e5be70a36e533',
    'narration-only.json': 'f13a4111a9c320ac3670e3acc0f11498babe514bafc00cab60c22b29013dba31',
    'claims.json': '181c1a6440b2c65fe7b5bcd54ccca0870c4d5341b0df7566cb4eba3802b5b999',
}
for name, expected in R4_INPUTS.items():
    assert FILE_SHA(R4 / name) == expected, name

protected_paths = [f for f in BASE.rglob('*') if f.is_file() and OUT not in f.parents]
protected_paths += [f for sub in ['history', 'reviews'] for f in (OUT / sub).rglob('*') if f.is_file()]
protected_paths += [f for f in CANONICAL.rglob('*') if f.is_file()]
protected_before = {str(f): FILE_SHA(f) for f in protected_paths}

sections = json.loads((OUT / 'r5-lines.json').read_text())
doc = json.loads((R4 / 'video.json').read_text())
series = json.loads((R4 / 'series.json').read_text())

source_files = {sid: WORK / 'source-cache' / (sid + '.paragraphs.txt') for sid in ['S1', 'S2', 'S3', 'S4']}
source_files['S8'] = WORK / 'r5-source/S8.paragraphs.txt'
paragraphs = {}
for sid, f in source_files.items():
    paragraphs[sid] = {line[:3]: line[4:] for line in f.read_text().splitlines() if line[:3].isdigit() and line[3:4] == ' '}

S8_PDF = WORK / 'r5-source/S8.pdf'
assert FILE_SHA(S8_PDF) == '8cbc2bba3bf9a39035dc9167bb9a303acce4ac9bdb45b5810d8380648ad2bfdc'
assert FILE_SHA(WORK / 'r5-source/S8.html') == 'd250cd07512be13f66ae7f8219f5b1024574846f20d555dfec9e0f2ea9aa2b28'

settings = [
    ('a plain reading desk', 'soft side light from the left'),
    ('a compact metalworking bench', 'gentle overhead light'),
    ('a generic stone practice area', 'mild overcast daylight'),
    ('a quiet climbing camp', 'warm late afternoon light'),
    ('an unmarked equipment room', 'soft doorway light'),
    ('a generic rocky ledge', 'diffuse morning light'),
]
camera = ['push in', 'pan left', 'pull back', 'tilt down', 'pan right', 'tilt up']
sizes = ['Close-up', 'Medium shot', 'Medium close-up', 'Wide shot', 'Close-up', 'Medium shot']
chapter_places = [
    'a plain reading desk', 'a compact workbench', 'a generic practice wall',
    'a camp workbench', 'a quiet camp beside a plain rock wall',
    'a plain granite ledge',
]

doc['scenes'] = []
narration = []
claims = []
keys = {}
scene_keys = {}
serial = 0
for chapter_index, section in enumerate(sections):
    if section.get('outro'):
        closing_lines = []
        for key, text, refs, action in section['rows']:
            serial += 1
            line_id = f'c09r5{serial:03}'
            keys[key] = line_id
            closing_lines.append({'id': line_id, 'text': text})
            narration.append({'chapter': sections[-2]['chapter'], 'id': line_id, 'text': text})
            claims.append({'id': line_id, 'chapter': 'outro', 'key': key, 'text': text, 'source': refs, 'claim_type': 'editorial closing/question', 'anchor': '結尾答案或觀眾問題；所依據攀登過程見原始第一人稱記錄，非額外史實。', 'status': 'PENDING_INDEPENDENT_REVIEW'})
        doc['scenes'].append({'id': 'c09r5-outro', 'template': 'outro', 'data': {'title': '那一錘，自己先停下', 'cta': '你會更相信公開不順利的賣家嗎？'}, 'lines': closing_lines})
        continue
    for row_index, (key, text, refs, action) in enumerate(section['rows']):
        serial += 1
        line_id, scene_id = f'c09r5{serial:03}', f'c09r5-shot-{serial:03}'
        assert key not in keys
        keys[key], scene_keys[key] = line_id, scene_id
        line = {'id': line_id, 'text': text}
        if '?' in text or '？' in text:
            line['emotion'] = '帶著好奇，問句自然上揚，不拖慢。'
        elif serial % 3 == 0:
            line['emotion'] = '像對朋友說出具體的新發現，句尾俐落。'
        place = chapter_places[chapter_index]
        light = settings[(serial + chapter_index) % len(settings)][1]
        actor = ['one anonymous adult', 'one unidentified person', 'one unnamed climber', 'one anonymous craftsperson'][(serial-1) % 4]
        action = action.replace('generic ', 'plain ')
        place = place.replace('generic ', 'plain ')
        prompt = f'{sizes[(serial-1) % len(sizes)]} at {place}, {actor} {action}, {light}.'
        scene = {'id': scene_id, 'template': 'shot', 'data': {'prompt': prompt, 'camera': camera[(serial-1) % len(camera)], 'visual': 'still'}, 'lines': [line]}
        if row_index == 0:
            scene['chapter'] = section['chapter']
        doc['scenes'].append(scene)
        narration.append({'chapter': section['chapter'], 'id': line_id, 'text': text})
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
        editorial = any(k in key for k in ['_q', 'reaction', 'question', 'promise', 'viewer', 'callback', 'transition', 'end'])
        claims.append({'id': line_id, 'chapter': section['chapter'], 'key': key, 'text': text, 'source': '、'.join(dict.fromkeys(e['source'] for e in evidence)), 'claim_type': 'sourced event with editorial/question framing' if editorial else 'sourced factual narration', 'anchor': refs, 'candidate_evidence': evidence, 'paragraph_hash_rule': 'SHA256 of UTF-8 paragraph body, excluding the three-digit index and one following space', 'status': 'PENDING_INDEPENDENT_REVIEW'})

loops = [
    ('open_question', 'outro_answer', '賣家怎樣讓少敲的勸告承受真實重量'),
    ('open_bag', 'climb_bag', '賣家實際攀登那次，器材袋裡帶了什麼'),
    ('origin_forge_q', 'origin_forge', '買不到合用釘子時，採取哪種行動'),
    ('origin_output_q', 'origin_output', '便攜手工爐每小時產量'),
    ('origin_price_q', 'origin_price', '手工岩釘售價和原有價格差距'),
    ('origin_order_q', 'origin_mail', '郵購單怎樣處理攀岩季的交貨'),
    ('origin_machine_q', 'origin_machine', '手工供不應求後的製造改變'),
    ('origin_transition', 'use_sequence', '新商品面對的是一套已練熟的身體動作'),
    ('use_holding_q', 'use_rotation', '多敲不是唯一固定力來源，裂縫配合如何作用'),
    ('use_extra_q', 'use_removal', '額外一錘把回收時間交給誰'),
    ('use_letter_q', 'use_letter', '賣家在1970年的回信是否願意換工具'),
    ('use_rock_q', 'use_rockscar', '重複敲拔在岩壁留下的實際痕跡'),
    ('use_larger_q', 'use_larger', '擴大裂縫讓下一枚工具發生什麼改變'),
    ('use_end', 'catalog_teach', '型錄如何把要求變成可學的使用方法'),
    ('catalog_how_q', 'catalog_anchors', '楔塊和多支點搭配的實際要求'),
    ('catalog_every_q', 'catalog_cleanroutes', '前言依路線條件給出的使用次序'),
    ('catalog_fixed_q', 'catalog_guides', '必要固定岩釘如何讓後來者取得資訊'),
    ('catalog_evidence_q', 'catalog_britain', '不同使用動作留下怎樣的岩縫對照'),
    ('catalog_end', 'resistance_fair', '顧客怎樣質疑賣家替自己決定攀登方式'),
    ('resistance_money_q', 'resistance_hypocrisy', '商業身分面對的具體批評'),
    ('trial_question', 'trial_hammer', '不帶錘子在現場改變哪個順手動作'),
    ('trial_callback', 'trial_opposed', '教學的組合支點在卡森早期嘗試中的新做法'),
    ('resistance_end', 'climb_first', '賣家到大岩壁時第一步的實際結果'),
    ('climb_first_q', 'climb_first', '第一個楔塊承重後的移動'),
    ('climb_partner_q', 'climb_partner', '頭兩次移動讓夥伴作何打算'),
    ('climb_trust_q', 'climb_trust', '夥伴的獨攀念頭後來如何改變'),
    ('climb_higher_q', 'climb_faster', '早期慢段之後，更高岩壁的放置速度'),
    ('climb_water_q', 'climb_water', '開始不順是否拖垮補給，原記錄的結果'),
    ('climb_repeat_q', 'climb_repeat', '同年另一次攀登能否重複這條路線'),
]
doc['loops'] = [{'setup': keys[a], 'payoff': keys[b], 'what': what} for a, b, what in loops]
doc['youtube']['title'] = 'Patagonia勸少敲，1973年自己敢嗎？｜品牌故事'
doc['youtube']['description'] = '一個賣岩釘的人，怎麼讓攀登者相信這一錘可以少敲？從修納德親手鍛造的商品、1970年的回信與1972年型錄，走到1973年他和Bruce Carson攀登酋長岩鼻子路線的第一步。新增原始第一人稱記錄，保留楔塊移動、搭檔疑慮及後續推進的實際細節。\n\n1974年是Carson文章刊出年，文中事件發生於1973年。1977年僅為另一採訪文章的刊出年，非已確認的到訪日。歷史畫面為匿名概念插畫，不重建真人長相、真實攀登路線或提供操作教學。\n\n參考資料\n' + '\n'.join([
    'https://publications.americanalpineclub.org/articles/12196733400/On-New-Rock-Climbing-Equipment-and-Its-Use',
    'https://www.patagonia.com/stories/sports/climbing/a-word/story-116598.html',
    'https://publications.americanalpineclub.org/articles/12197352200/Chouinard-Equipment',
    'https://www.newyorker.com/magazine/1977/01/31/ascending',
    'https://publications.americanalpineclub.org/articles/12197405800/Some-Clean-Wall-Climbs-in-Yosemite',
    'https://aac-publications.s3.amazonaws.com/documents/aaj/1974/PDF/AAJ_1974_19_1_058.pdf',
])
doc['thumbnail']['data'].update({'headline': '他自己\n敢爬嗎？', 'sub': '1973年拿掉岩釘', 'shot': scene_keys['climb_first'], 'layout': 'd', 'brand': 'PATAGONIA'})
doc['sources'] = [s for s in doc['sources'] if '2012' not in s['title']]
doc['sources'].append({'title': 'Carson，1974年刊出、敘述1973年攀登的第一人稱原文與原刊PDF', 'url': 'https://publications.americanalpineclub.org/articles/12197405800/Some-Clean-Wall-Climbs-in-Yosemite', 'checked_on': '2026-10-25'})
series.update({'title': 'Patagonia：賣岩釘的人，自己敢把錘子留下嗎？', 'logline': '跟著修納德賣出岩釘、改變使用次序、面對顧客的公平質疑，最後和卡森把楔塊帶上1973年的鼻子路線，讓勸告承受實際重量。', 'production_status': 'r5_candidate_unapproved_pending_independent_source_and_new_blind_readers'})
series['names'] = list(dict.fromkeys(series['names'] + ['Bruce Carson', 'Carson', '卡森']))

# The three editorial closing lines keep the same auditable original-source binding.
for row in claims:
    if 'candidate_evidence' not in row:
        evidence = []
        for ref in row['anchor'].split(';') if ':' in row['anchor'] else row['source'].split(';'):
            sid, para = ref.split(':')
            original = paragraphs[sid][para]
            evidence.append({'source': sid, 'cache_path': str(source_files[sid]), 'cache_sha256': FILE_SHA(source_files[sid]), 'paragraph': para, 'paragraph_sha256': SHA(original.encode()), 'short_quote': original[:220], 'quote_is_exact_prefix': True, 'original_pdf': str(S8_PDF), 'original_pdf_sha256': FILE_SHA(S8_PDF)})
        row['candidate_evidence'] = evidence
        row['source'] = '、'.join(dict.fromkeys(e['source'] for e in evidence))
        row['paragraph_hash_rule'] = 'SHA256 of UTF-8 paragraph body, excluding the three-digit index and one following space'

dump = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
dump(OUT / 'video.json', doc)
dump(OUT / 'series.json', series)
dump(OUT / 'narration-only.json', narration)
dump(OUT / 'claims.json', claims)

script = ['# C09 R5 作者附來源稿｜器材商的勸告如何承重', '', '狀態：HOLD，待獨立來源／書面配鏡及兩位全新隔離讀者；不是owner核准。', '']
last_chapter = None
for row in claims:
    chapter = row['chapter']
    if chapter != last_chapter:
        script += ['## ' + chapter, '']
        last_chapter = chapter
    script += [f"[{row['id']}] {row['text']}", f"來源：{row['source']}；{row['anchor']}", '']
(OUT / 'script.md').write_text('\n'.join(script).rstrip() + '\n')
md = ['# C09 R5 逐句來源對照', '', '全部狀態為 PENDING_INDEPENDENT_REVIEW。來源引用是可稽核錨點，不是本作者自授PASS。', '', 'S8為Bruce Carson的原始第一人稱報告，1974年出版，內文1973年；原刊PDF第59–60頁已目視核對，不能把其回憶改成全知敘事。', '', '## 原始輸入與來源界線', '', '- S1：1967年器材文章，描述當時作者提出的用法，不當現代攀登教學。', '- S2：只把重刊頁027–036當1972年前言；043的創辦人身分是現代編輯人物介紹。', '- S3：1973書評，私人批評、不同讀者立場及觀察均保留歸屬；東岸限定文字流傳，不限定作者籍貫。', '- S4：1977刊出採訪，1957/1964/1970等過去年份是文中明示回述；不把1977當到訪日。', '- S8：五月信、夏末約定、兩週後攀登依原文先後；1973年並由S4:009交叉對時。原文one of these不擴成他從未用過任何楔塊，未寫入旁白。', '- 四分之一英吋換算六公釐是近似換算，不當精密量測值；楔塊下沉不改成脫落、墜落或事故。', '- 早期卡森嘗試清楚說仍用既有螺栓；Nose的器材選擇只排除攜帶岩釘，沒有排除繩索或其他攀登裝備。', '- 字數、估秒與書面配鏡均不是實際TTS或媒體驗收。', '']
for row in claims:
    md += [f"## {row['id']} · {row['key']}", '', row['text'], '', f"來源：{row['source']}；錨點：{row['anchor']}", '']
    for e in row.get('candidate_evidence', []):
        md += [f"- {e['source']}:{e['paragraph']}，paragraph SHA256 `{e['paragraph_sha256']}`；cache SHA256 `{e['cache_sha256']}`。", '  > ' + e['short_quote']]
    md += ['']
(OUT / 'claims.md').write_text('\n'.join(md).rstrip() + '\n')

brief = '''# C09 R5｜讓一個賣家的勸告真正承重

狀態：作者候選HOLD，待新的獨立來源、書面配鏡與兩位全新隔離讀者。R4來源PASS與敘事HOLD保留於history/r4；本版沒有沿用舊批准。

## 本次建議

### 選項 A：他自己敢爬嗎？

故事線：抉擇。主角：修納德面對自己熟悉的岩釘，以及顧客要求他同樣承擔的新選擇。開場在1972型錄旁，只回溯一次商品與動作如何形成；之後按1967、1970、1972、1973往前，終點是同一次Nose攀登的真實試行。

## 問題

賣岩釘的人，怎麼讓顧客相信，這一錘可以少敲？

## 一句答案

他需要給出可學的做法，面對既有使用者的公平質疑，還得自己把重量交給替代工具；夥伴留下的原始記錄，也保留了不順利的第一步。

## 站主觀點

賣家的主張要走到使用現場才有分量。這次沿一個器材替換問題，讓觀眾看見手上動作、顧客信任與一次具體攀登如何相連，不把品牌寫成一句環保口號。

## 故事如何往前

手工做出的可回收岩釘讓人學會相信舊工具；熟練動作的另一個結果是岩縫傷痕。1970年的回信顯示賣家自己也不願普遍換用楔塊。1972型錄把優先次序與十四頁使用教學印出來，1973讀者直接質疑他為何替後來者決定難度。這個問題交到實際攀登：卡森先前的試行提供具體組合支點，接著成為修納德在Nose的搭檔；第一、第二個楔塊移動，兩人重新取得配合，再推進到完成及同年另一隊的重複。

卡森春季的場景不是品牌造成的成功案例；沒有證據說是讀型錄後才去爬。本版只用它交代這位後來搭檔已有的嘗試，以及同一種替換工具在現場的問題。原書評的判斷不再重讀一次，工廠扣環、冰斧、尺寸清單、服裝與模具財務全部刪離正文。

## 新增原始來源

S8：Bruce Carson，Some Clean Wall Climbs in Yosemite，American Alpine Journal 1974，第58–61頁。完整原刊PDF及網頁bytes保存在work/c09-audit/r5-source，原刊第59–60頁已目視，逐句錨點和hash見claims.json。1973事件與1974出版不混同；作者的心理只以其自己文字為歸屬。

## 視聽與長度

目標13分鐘，實際自然語速正文720–840秒待TTS量測；不加停頓或慢播湊長。look只用cute-mystery preset、image-01；匿名英文概念提示詞不畫真人或真實路線。正文插畫比例在原生估算裡檢查，仍不等於生成圖驗收。繁中燒錄與CC、開場後5秒片頭與21秒正式v4片尾、bold layout d縮圖均是待執行規格，不虛構素材身分。

## 後續

原current、canonical、舊核准、八語譯文、history與reviews不改。本版所有新ID、改字、配鏡與source anchors均須獨立複核；原生字典context lint只檢查機械條件。未寫verify、未呼叫後台或付費供應商。
'''
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
console.log(JSON.stringify({context_binding:binding,result,units:{total,opening,body_after_opening:total-opening,closing,body_excluding_opening_and_closing:total-opening-closing},line_count:flat.length,scene_count:doc.scenes.length,shot_count:shots.length,chapter_count:doc.scenes.filter(s=>s.chapter).length,max_estimated_shot_seconds:Math.max(...shots.map(s=>seconds[s.id])),shot_time_share:shots.reduce((n,s)=>n+seconds[s.id],0)/(timeline.total_frames/FPS),cadence_problems:hookCadenceProblems(doc,timeline,TIGHT_CADENCE.gap),timeline_estimated_minutes:timeline.total_frames/FPS/60,default_cpm:DEFAULT_CPM,actual_timing_verified:false}));
"""
run = subprocess.run(['node', '--input-type=module', '-e', native_code, str(OUT), str(CANONICAL_ROOT)], cwd=REPO, capture_output=True, text=True, check=True)
native = json.loads(run.stdout)
dump(OUT / 'author-local-lint-r5.json', native)

after = {str(f): FILE_SHA(f) for f in protected_paths}
assert protected_before == after, [f for f in protected_before if protected_before[f] != after.get(f)]
notes = {
    'status': 'HOLD_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_NEW_ISOLATED_READERS',
    'revision': 'length-extension-r5',
    'author': '/root/c09_r5_author',
    'author_is_not_source_reviewer': True,
    'r4_input_sha256': R4_INPUTS,
    'current_input_sha256': {f: FILE_SHA(OUT/f) for f in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','r5-lines.json','build-r5.py']},
    'substantive_rewrite': 'one equipment-replacement decision and its field trial; all narration receives new c09r5 IDs; no resampling of unchanged text',
    'removed_branches': ['hardware-racking directions','carabiner and ice-axe manufacture','catalog size inventories','repeated review-author rebuttal','later factory tour','clothing label and financial mold discussion'],
    'new_primary_source': {
        'id': 'S8', 'title': 'Some Clean Wall Climbs in Yosemite', 'author': 'Bruce Carson',
        'url': 'https://publications.americanalpineclub.org/articles/12197405800/Some-Clean-Wall-Climbs-in-Yosemite',
        'publication_year': 1974, 'event_year': 1973, 'printed_pages': '58–61',
        'html_sha256': FILE_SHA(WORK/'r5-source/S8.html'), 'pdf_sha256': FILE_SHA(S8_PDF),
        'paragraph_cache_sha256': FILE_SHA(source_files['S8']), 'pdf_pages_visually_read': [2,3],
        'pdf_actual_bytes_local_only': True, 'search_result_is_not_evidence': True,
        'limits': ['one of these not expanded into never used any chocks','a sinking placement is not rewritten as a fall','spring trial uses existing bolts as explicitly stated','no claim the catalog caused Carson to attempt these routes','Nose carry choice excludes pitons, not rope or other gear','same-year follow-up team is reported by Carson, not population-wide adoption']
    },
    'native_initialized_context_lint': native,
    'legacy_opening_loop_count_warning': 'Native generic loop lint asks for three opening loops, but current owner series rule permits at most two future teaser moments. The actual opening is kept concise instead of adding a third teaser to silence that legacy warning.',
    'protected_existing_files_count': len(protected_before),
    'protected_existing_files_unchanged': True,
    'protected_manifest_sha256': SHA(json.dumps(protected_before,sort_keys=True).encode()),
    'old_approvals_inherited': False,
    'verify_written_by_author': False,
    'actual_audio_measured': False,
    'media_generated': False,
    'backend_calls': 0,
    'paid_calls': 0,
}
dump(OUT/'author-notes.json', notes)
print(json.dumps({'input_sha256':notes['current_input_sha256'],'native':native,'protected_files':len(protected_before)},ensure_ascii=False))
if native['result']['errors']:
    raise SystemExit('Native full-context errors remain; do not freeze or submit')
