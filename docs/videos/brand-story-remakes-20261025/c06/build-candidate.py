#!/usr/bin/env python3
"""Author's deterministic C06 candidate; never calls providers or creates approvals."""
import hashlib
import json
import re
import subprocess
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = 'story-everyday-play-doh-c06-remake-20261025'
DATE = '2026-10-25'
RESEARCH = json.loads((HERE / 'research-original.claims.json').read_text())
SOURCES = {s['id']: s for s in RESEARCH['sources']}
ROOT = HERE.parents[3]
STORY_VOICE_STYLE = subprocess.check_output(['node','--input-type=module','-e',"import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs'; console.log(STORY_VOICE_STYLE);"],cwd=ROOT,text=True).strip()
CHAPTERS = [
    ('h','一罐材料等著再被打開'),
    ('o','煤灰變少，清潔工作縮小'),
    ('k','孩子把材料捏成作品'),
    ('t','手指的工作交給一個出口'),
    ('b','作者把蓋子寫進了專利'),
    ('n','花束留在了桌上'),
]
DATA = runpy.run_path(str(HERE / 'rows-r2.py'))
REVISION = 'r3'
REMOVED_ROWS = {'o12', 'b17a'}
ROW_RECORDS = [row for row in DATA['ROWS'] if row['key'] not in REMOVED_ROWS]
LOOPS = DATA['LOOPS']
ANCHORS = json.loads((HERE/'anchors-r2.json').read_text())
CITED = {ANCHORS[ref]['source'] for row in ROW_RECORDS for ref in row['refs']}

def dump(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def units(text):
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]", text)
    return sum(1 if re.match(r'[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]', t) else 2 for t in tokens)

def split_for_speech(text):
    if units(text)<=36 and '？' not in text and '?' not in text: return [text]
    parts=re.findall(r'.+?[，；。？！：]|.+$',text)
    result=[]; current=''
    for part in parts:
        if current and units(current+part)>36:
            result.append(current); current=''
        current+=part
        if part.endswith(('？','?')):
            result.append(current); current=''
    if current: result.append(current)
    assert ''.join(result)==text
    return result

def evidence_for(anchor_id,short=None):
    anchor=ANCHORS[anchor_id]; source_id=anchor['source']; source=SOURCES[source_id]
    return {'anchor_id':anchor_id,'source_id':source_id,'url':source['url'],
        'locator':anchor['locator'],'scope':anchor.get('scope',source['limits']),
        'research_raw_sha256':source['raw_sha256']}

def main():
    counters={k:0 for k,_ in CHAPTERS}
    scenes=[]; narration=[]; claims=[]; index={}; visual=[]
    cameras=['push in','pan left','pull out','tilt down','pan right','tilt up']
    lights=['soft window light from the left','mild overcast window light','gentle desk lamp light from the right','soft doorway light']
    sizes=['Close-up','Medium shot','Medium close-up','Wide shot']
    for i,row in enumerate(ROW_RECORDS):
        ch=row['chapter']; refs=','.join(row['refs']); kind=row['kind']; action=row['action']
        lines=[segment for text in row['lines'] for segment in split_for_speech(text)]
        counters[ch]+=1; short=row['key']; sid=f'c06r2-{short}'
        lids=[f'c6s{short}{j+1}' for j in range(len(lines))]; index[short]=lids
        locations={'h':'at a kitchen table','o':'inside a small cleaning-supply shop','k':'inside a classroom craft corner','t':'inside a playroom','b':'at a small product display','n':'at a home crafting corner'}
        place=locations[ch]
        for needles,location in [(['wallpaper'],'beside a freestanding wallpaper panel'),(['soap','washroom'],'beside a washroom sink'),(['television'],'in a living room'),(['exhibition'],'at a small exhibition stand'),(['patent','folder'],'at a document reading desk'),(['extruder','rail'],'inside a playroom'),(['flower','vase','petal'],'at a home crafting corner')]:
            if any(n in action for n in needles): place=location
        groups=[]; current=[]
        for pair in zip(lids,lines):
            if current and sum(units(x[1]) for x in current)+units(pair[1])>38:
                groups.append(current); current=[]
            current.append(pair)
        if current: groups.append(current)
        for j,group in enumerate(groups):
            part_id=sid if j==0 else sid+f'-p{j+1}'
            k=len(scenes)
            person=['one anonymous adult facing the viewer','one curious person looking toward the viewer','one focused hobbyist with a thoughtful expression','one unidentified craftsperson with a puzzled expression'][k%4]
            if 'firm clay' in action:
                person='one anonymous adult with a frustrated expression'
                action=action.replace(' with a frustrated expression','')
            prompt=f'{sizes[k%len(sizes)]} {place}, {person} while {action}, {lights[k%len(lights)]}.'
            scene={'id':part_id,'template':'shot','data':{'prompt':prompt,'visual':'still','camera':cameras[k%len(cameras)]},'lines':[{'id':lid,'text':text,'emotion':'自然親近，問句上揚' if '？' in text else '說書語氣，自然有起伏'} for lid,text in group]}
            if counters[ch]==1 and j==0: scene['chapter']=dict(CHAPTERS)[ch]
            scenes.append(scene)
            visual.append({'scene_id':part_id,'source_anchors':refs.split(','),'kind':'anonymous_concept_illustration','actual_historical_reconstruction':False,'scope':'動作示意，無品牌字樣、歷史人物肖像、可讀文件；非已生成或已驗收圖片。'})
        for lid,text in zip(lids,lines):
            narration.append({'chapter':dict(CHAPTERS)[ch],'id':lid,'text':text})
            scene_id=next(s['id'] for s in scenes if any(l['id']==lid for l in s['lines']))
            claims.append({'id':lid,'scene_id':scene_id,'text':text,'source_anchors':refs.split(','),'evidence':[evidence_for(ref,short) for ref in refs.split(',')],'kind':kind,'status':'PENDING_INDEPENDENT_REVIEW','boundary': '匿名概念插圖；假設動作或旁白觀點不主張為歷史現場。' if kind in ['hypothetical','opinion','question','mixed'] else '保留來源層級、年代與產品範圍；未經獨立新稿查核。'})
    out=[
        ('c6snct1','如果是你，會把一團材料反覆揉回去玩，還是留下一件完成的作品？留言告訴我，你最想做什麼。'),
        ('c6snct2','想繼續看熟悉的日用品，如何被使用者推著換工作，歡迎訂閱這個頻道。'),
    ]
    scenes.append({'id':'c06r2-outro','template':'outro','data':{'title':'換一雙手，就換一種工作','cta':'你想反覆重做，還是留下成品？'},'lines':[{'id':lid,'text':text,'emotion':'溫暖收束，對一位觀眾說話'} for lid,text in out]})
    for lid,text in out:
        narration.append({'chapter':CHAPTERS[-1][1],'id':lid,'text':text})
        claims.append({'id':lid,'scene_id':'c06r2-outro','text':text,'source_anchors':[],'kind':'editorial_cta','status':'PENDING_INDEPENDENT_REVIEW','boundary':'通用觀眾提問和有理由的訂閱邀請，未增加史實。'})
    video={
        'schema_version':1,'slug':SLUG,'format':'drama','category':'explainer','narration_locale':'zh-TW','target_minutes':[12,14],
        'voice':{'provider':'gemini','name':'Sulafat','style':STORY_VOICE_STYLE,'performance':'對一個人說材料怎麼換工作；企業與館方回顧自然保留歸屬。假設動作不演成歷史現場。'},
        'subtitles':{'burn_in':True},'look':{'preset':'cute-mystery'},'characters':[],
        'music':{'prompt':'light, curious, a little mysterious, no vocals','gain_db':-20,'duck_db':-10},
        'loops':[{'setup':index[a][-1],'payoff':index[b][0],'what':w} for a,b,w in LOOPS],
        'youtube':{'category_id':27,'made_for_kids':False,'default_language':'zh-TW','title':'Play-Doh：擦牆膏怎麼變成玩具？｜品牌故事','description':'一團原本擦壁紙的材料，怎麼換成孩子手上的玩具，又走向成人花藝？循著Kutol的公司史、The Strong的歷史回顧、美國專利，以及孩之寶的產品公告，看使用者如何改變顏色、工具與保存要求。1956是公司回顧的品牌生日；後來專利與現代套件各有自己的年代和產品範圍。匿名概念插圖不重建歷史現場。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(s['title']+'\n'+s['url'] for s in SOURCES.values() if s['id'] in CITED),'tags':['Play-Doh','培樂多','Kutol','品牌故事','黏土','日用品的意外轉身','玩具','商業故事'],'video_id':None},
        'thumbnail':{'template':'thumb','data':{'layout':'d','headline':'擦牆膏變玩具','sub':'2024稱逾5億罐','brand':'PLAY-DOH','tag':'品牌故事','shot':'c06r2-h01'}},
        'sources':[{'title':s['title'],'url':s['url'],'checked_on':DATE} for s in SOURCES.values() if s['id'] in CITED],
        'assets':[],'scenes':scenes,
    }
    # R3 deletes two redundant rows only. Preserve every retained R2 scene object,
    # including its original prompt/camera/light, rather than rotating by new index.
    baseline_video=json.loads((HERE/'history/r2/video.json').read_text())
    removed_scenes={scene['id'] for scene in baseline_video['scenes']
        if any(scene['id']==f'c06r2-{key}' or scene['id'].startswith(f'c06r2-{key}-p') for key in REMOVED_ROWS)}
    retained=[scene for scene in baseline_video['scenes'] if scene['id'] not in removed_scenes]
    assert [scene['id'] for scene in scenes]==[scene['id'] for scene in retained]
    for new,old in zip(scenes,retained):
        assert new['lines']==old['lines']
        assert new['template']==old['template'] and new.get('chapter')==old.get('chapter')
    assert {k:v for k,v in video.items() if k!='scenes'}=={k:v for k,v in baseline_video.items() if k!='scenes'}
    video=baseline_video
    video['scenes']=retained
    # STORY_CATEGORY_METADATA_CORRECTION: preserve the frozen narrative while reporting this source as a brand story.
    video['category']='story'

    # Prompt/camera-only teaser image plan; narrative and all scene IDs remain frozen.
    TEASER_IMAGE_OVERRIDES = {'c06r2-h05': {'prompt': "Close-up at a classroom craft table, one child's small hands pressing a firm plain lump of modeling clay, soft window light.", 'camera': 'push in'}, 'c06r2-k02-p2': {'prompt': "Close-up at a classroom craft table, one child's small hands pressing a firm plain lump of modeling clay, soft window light.", 'camera': 'push in'}, 'c06r2-h06': {'prompt': 'Medium shot at a home crafting table, one anonymous adult examining a small bouquet of modeled flowers beside a plain empty vase, soft window light.', 'camera': 'pan left'}, 'c06r2-n06': {'prompt': 'Medium shot at a home crafting table, one anonymous adult examining a small bouquet of modeled flowers beside a plain empty vase, soft window light.', 'camera': 'pan left'}}
    for _scene in video['scenes']:
        if _scene['id'] in TEASER_IMAGE_OVERRIDES:
            _scene['data'].update(TEASER_IMAGE_OVERRIDES[_scene['id']])
    dump('video.json',video); dump('narration-only.json',narration)
    dump('claims.json',{'schema_version':1,'status':'AUTHOR_CANDIDATE_NOT_INDEPENDENTLY_REVIEWED','lines':claims,'written_visuals':visual,'source_catalog':'source-catalog.json','research_original':'research-original.claims.json'})
    dump('source-catalog.json',{'schema_version':1,'sources':list(SOURCES.values()),'original_sha256':hashlib.sha256((HERE/'research-original.claims.json').read_bytes()).hexdigest(),'status':'RESEARCH_RECORD_NOT_NEW_SCRIPT_APPROVAL'})
    dump('source-anchors.json',{'schema_version':1,'anchors':[{'id':key,'source_id':a['source'],'url':SOURCES[a['source']]['url'],'locator':a['locator'],'raw_document_sha256':SOURCES[a['source']]['raw_sha256'],'published_on':SOURCES[a['source']].get('published_on'),'limits':a['scope']} for key,a in ANCHORS.items()],'lines':{c['id']:c['source_anchors'] for c in claims},'line_evidence':{c['id']:c.get('evidence',[]) for c in claims},'written_visuals':visual})
    dump('series.json',{'kind':'story','slug':'brand-stories-everyday-reversals','episode':6,'chapter':1,'title':video['youtube']['title'],'logline':'跟著一團能塑形的材料，從擦壁紙到教室、工具與成人花藝，看使用者如何改變材料的工作。','names':['Play-Doh','PLAY-DOH','培樂多','Kutol','Hasbro','孩之寶','Rainbow Crafts','Fun Factory','Blooms','凱・祖法爾','約瑟夫・麥克維克','諾亞・麥克維克','克里奧・麥克維克','The Strong','克羅格','Kroger','路易維爾','Louisville','辛辛那提','Cincinnati','袋鼠船長','Captain Kangaroo'],'characters':[],'visual_tier':'stills','compilation':False,'target_minutes':13,'image_model':'image-01','look':{'preset':'cute-mystery'}})
    script=['# C06 Play-Doh｜r3 作者精修候選','',f'新 slug：{SLUG}。此為作者逐字稿；不是原生canonical screenplay，也不是核准收據。','']
    for ch,title in CHAPTERS:
        script+=['## '+title,'']
        for n in narration:
            if n['chapter']==title: script += [f"**{n['id']}** {n['text']}",'']
    (HERE/'script.md').write_text('\n'.join(script)+'\n')
    md=['# C06 逐句來源與書面配鏡（作者待審表）','','這份表由作者建立。各句尚待不同代理核對原件，圖片尚未生成；不得當成獨立來源、敘事或媒體通過收據。','','| 旁白ID | 來源錨點 | 類別 | 限定 |','| --- | --- | --- | --- |']
    md += [f"| {c['id']} | {', '.join(c['source_anchors']) or '無新增史實'} | {c['kind']} | {c['boundary']} |" for c in claims]
    md += ['','## 原件與範圍','']
    for s in SOURCES.values(): md += [f"### {s['id']} — {s['title']}",f"{s['url']}\n\n定位：{s['locator']}。出版：{s.get('published_on') or '頁面未列初次出版日'}；查閱：{DATE}。\n\n範圍：{s['limits']}\n"]
    md += ['## 書面配鏡','', '所有 shot 均是匿名概念插圖，英文提示詞不放品牌、人名、標誌或可讀文字；不是歷史照片或專利原圖。1960 Fun Factory用匿名通用槓桿與出口示意，不畫現代兩軌特定外形；專利組成不配成1933配方，成人花藝不配成所有經典黏土的保存性能。實際出圖、視覺QA尚未成立。']
    md += ['','## 新稿使用的原件補充定位','', 'P1的顆粒薄膜／濕熱糊化段在PDF1印刷欄2，保留「專利作者認為」的解釋層級；原件claim9另寫可塑性與保留形狀。後半特性段的密閉容器、玩後放回、充分乾硬不可重塑及可上色，對應Google Patents description498–500；是文件對其組成的描述，沒有獨立性能測試。逐句的細定位及範圍另列claims.json的evidence及source-anchors.json的line_evidence。']
    md += ['', '## 開場預告共圖（作者製片規劃，待獨立覆核）', '', '此節只規劃兩端共用同一張已驗收實圖。旁白、ID、scene順序、loops及原件主張未改；尚無實圖、實際共用SHA、來源新PASS或媒體驗收。具體request/key與停止條件見 `image-reuse-plan.json`。', '', '| 配對 | 預告scene／line | 回收章共圖scene／line | 未提前揭示結果的中性內容 |', '| --- | --- | --- | --- |', '| small-hands-firm-clay | c06r2-h05／c6sh051 | c06r2-k02-p2／c6sk022 | Anonymous small hands face the firm-clay problem, without showing a successful classroom test or identifying a historical child or teacher. |', '| modeled-bouquet-before-finishing | c06r2-h06／c6sh061 | c06r2-n06／c6sn061, c6sn062 | The bouquet is awaiting its final step; no spray bottle, spraying action or durability result is pictured. The actual finishing-spray answer scene is unchanged. |', '', '同prompt/camera只是可執行的快取規劃。正式製片仍需有效全片帳戶與各既有關卡，先生成並驗收回收景單一take；預告指令前查live cache及實檔SHA，cache miss不得直接派送另一張圖。兩端仍各自通過judge；retake、修圖或裁切改了任一實檔則停止配對共同重查。最終manifest、實檔與組片引用SHA相同後才可記實際共圖通過。', '']
    (HERE/'claims.md').write_text('\n'.join(md)+'\n')
    ch_units={title:sum(units(n['text']) for n in narration if n['chapter']==title) for _,title in CHAPTERS}
    counts={'count_method':'native spokenUnits-compatible estimate, not measured audio','spoken_units_total':sum(ch_units.values()),'spoken_units_cold_open':ch_units[CHAPTERS[0][1]],'spoken_units_body':sum(ch_units.values())-ch_units[CHAPTERS[0][1]],'chapters':ch_units,'lines':len(narration),'scenes':len(scenes),'shot_scenes':len(visual),'outro_scenes':1,'loops_authored':len(video['loops']),'body_estimated_seconds_at_4_5_units_per_second':round((sum(ch_units.values())-ch_units[CHAPTERS[0][1]])/4.5,1)}
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['video.json','script.md','narration-only.json','claims.json','source-catalog.json','source-anchors.json','research-original.md','research-original.claims.json']}
    dump('author-notes.json',{'schema_version':1,'author':'/root/find_rules','date':DATE,'status':'AUTHOR_CANDIDATE_PENDING_ALL_INDEPENDENT_GATES','slug':SLUG,'counts':counts,'input_hashes':hashes,'revision':REVISION,'scope':'R3 deletes only o12 and b17a after reading actual r2 no_recap HOLD evidence. Retained R2 scene objects and all non-scenes video fields remain exactly equal. Not an independent approval.','fact_limits':['1956 is attributed brand birthday, not independently established first invoice.','2017 scent application declares first use at least as early as1955-09-12; omitted from narration, not treated as independently verified first sale.','1933 cleaner formula and contemporary classroom records not obtained; later patent cannot prove their contents.','Kutol and museum history are attributed retrospectives, not contemporary classroom/business records.','Patent filing1960-05-17 and grant1965-01-26 distinct; goals are not independent performance tests, current formula or safety approval.','2024 annual cans are corporate shipments claim, not children, retail sales or revenue.','R2 omits licensing and Kutol soap/skin-care branch; G2 is background only and was not independently reopened by r1 source reviewer.','2026adult-line and months-of-structure statements are company/product claims; no efficacy or sales-success claim.','New r2 mixing and up-to-three-years storage statements are attributed patent text claims, not independent manufacturing observations or current-product expiry guarantees.'],'production_plan':{'image_model':'image-01','look':{'preset':'cute-mystery'},'planned_shot_time_share_by_spoken_units':round(sum(units(c['text']) for c in claims if c['scene_id']!='c06r2-outro')/sum(ch_units.values()),4),'consecutive_cards_max':1,'main_subtitles_burn_in':True,'cc_planned':True,'intro_after_cold_open_seconds':5,'outro_v4_seconds':21,'actual_branding_assets_verified':False,'fresh_production':True,'old_media_retrieval_prerequisite':False,'actual_paid_calls':0},'pending':{'independent_source_and_written_visual_review':True,'two_fresh_blind_narrative_readers':True,'independent_pronunciation_review':True,'owner_outline_approval':True,'owner_script_approval':True,'canonical_script_generation':True,'account_budget_admission':True,'tts_and_sentence_listening':True,'actual_body_runtime_12_to_14_minutes':True,'generated_images_and_visual_qa':True,'music':True,'assemble_and_final_qa':True,'owner_final_approval':True,'language_media':True},'no_approval_claim':'This author file confers no source/narrative/owner/audio/media/QA/budget approval.'})
    print(json.dumps(counts,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
