#!/usr/bin/env python3
"""Replay the Doraemon R6 author candidate. No network, provider, approval or backend call."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'story-adapt-doraemon-after-fujiko-remake-20261025'
DATE = '2026-10-26'
EXTERNAL = Path('/workspace/work/brand-story-20261025/doraemon-audit/author-r6')
RUNTIME = EXTERNAL / 'free-runtime'
MEDIA = EXTERNAL / 'media'
RESEARCH = json.loads((HERE/'research-original.claims.json').read_text())
SOURCES = {s['id']: s for s in RESEARCH['sources']}
BASE = {c['id']: c for c in RESEARCH['claims']}
ROWS = json.loads((HERE/'rows-r6.json').read_text())
CHAPTERS = {'h':'開場濃縮','a':'另取一張紙，留下原件','b':'一封郵件，把作者帶到月球前','c':'舊設定接上新朋友','d':'把說話交給畫面，再重新寫成書','e':'找到這一版真正做工作的人'}
TITLE = '哆啦Ａ夢：作者走了30年，誰還在寫新故事？｜品牌故事'
VOICE_STYLE = subprocess.check_output(['node','--input-type=module','-e',"import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs'; console.log(STORY_VOICE_STYLE);"],cwd=ROOT,text=True).strip()
LOOPS = [
    ('h03','a01','為什麼接續大長篇卻不在原紙落筆'),
    ('h04','b08','科學資料被帶進哪個寫作步驟'),
    ('a05','a06','2017究竟是接手年還是回憶出版年'),
    ('a02','a03','能否從保存動作判定接續到哪回'),
    ('a06b','a07','2016究竟是哪個發行版本的日期'),
    ('a09','b01','下一份新冒險交到哪位寫作者手上'),
    ('b05','b06','新舞台怎麼跟觀眾原有生活接上'),
    ('b10','c01','月球舞台與原作世界的入口'),
    ('c02b','c02c','複雜設定要怎麼讓孩子跟上'),
    ('c02d','c03','新寫作者如何判斷角色該怎麼說話'),
    ('c05','c06','導演如何要求編劇處理冒險動機'),
    ('c09','d01','電影腳本是否能像小說一直加長'),
    ('d02','d03','小說家的長台詞如何適應電影'),
    ('d06','d07','文字交出後電影是否已經完成'),
    ('d09','d10','同一故事小說化能帶來什麼新表現'),
    ('d12b','d12c','寫給孩子如何處理詞彙與讀音'),
    ('d11','d12','有既有畫面是否就能寫得比較快'),
    ('d13','d14b','小說是否總在電影上映後發售'),
    ('d15','e01','電影漫畫是否重新手繪同一故事'),
    ('e04','e05','近年腳本是否一直由同一人寫'),
    ('e06b','e07','新寫腳本是否一定是全新原案'),
    ('e07c','e08','公司列名與腳本作者欄如何分清'),
    ('h06','e10','新故事寫作者與原作署名如何並存'),
]
EXTRA = {
    'A01': ('MW2019A',23,26,'昨日までと違う身近さ','2019 participant account: choosing a familiar destination and the desired viewer response.'),
    'A02': ('MW2019',26,26,'先生だったらどうするか','Writer explicitly separates imagining the original author from reasoning through established characters.'),
    'A03': ('TSUJINTERVIEW',8,11,'映画とは違うアプローチ','Novel versus screenplay: first sentence, narration, staging and the animation team making an unspecified colour concrete.'),
    'A04': ('TSUJINTERVIEW',12,12,'映画にはないシーン','Writer recalls internal feelings and scenes absent from the movie; no new screenplay draft or film viewing claimed.'),
    'A05': ('PROFILE',10,12,'1987年のコンビ解消後','Fujimoto Hiroshi and Abiko Motoo are separate people; official biography states shared pen name and later separation.'),
    'A06': ('MW2019',32,33,'わずか数ページ','Participants describe economical visual explanations already present in the original short manga; source pages, not manga pages personally examined.'),
    'A07': ('TSUJINTERVIEW',13,14,'漢字のフリガナもすべてつく','Participant account: age, unfamiliar vocabulary, contextual reading and junior edition reading aids. Not a reader learning test.'),
}

def sha(file): return hashlib.sha256(Path(file).read_bytes()).hexdigest()
def dump(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def units(text):
    return sum(1 if re.match(r'[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]',t) else 2 for t in re.findall(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]",text))
def split(text):
    # Preserve all words and punctuation. No silence or delivery-rate instruction is added.
    clauses=re.findall(r'.+?[，；。？！：]|.+$',text)
    out=[];current=''
    for clause in clauses:
        if current and units(current+clause)>36: out.append(current);current=''
        current+=clause
        if current.endswith(('？','?','。','！')): out.append(current);current=''
    if current:out.append(current)
    assert ''.join(out)==text
    return out

def make_anchors():
    anchors={}
    for key,claim in BASE.items():
        evidence=[]
        for e in claim.get('evidence',[]):
            source=SOURCES[e['source_id']]
            text=Path(source['text_path']).read_text().splitlines()
            excerpt='\n'.join(text[e['text_line_1based']-1:e['text_line_end_1based']])
            assert e['quote_exact_short'] in excerpt,(key,e['quote_exact_short'])
            evidence.append({**e,'url':source.get('requested_url',source.get('url')),'raw_path':source.get('raw_path',source.get('tool_result_path')),'text_path':source['text_path'],'http_status_observed':source.get('http_status_observed',source.get('origin_http_status_observed')),'retrieval_method':source.get('retrieval_method','downloaded origin response; see frozen source receipt'),'full_located_excerpt':excerpt})
        anchors[key]={'id':key,'claim':claim['claim_zh'],'classification':claim['classification'],'limits':claim['limits'],'evidence':evidence,'independent_review':'PENDING'}
    for key,(sid,a,b,quote,scope) in EXTRA.items():
        s=SOURCES[sid];text=Path(s['text_path']).read_text().splitlines();excerpt='\n'.join(text[a-1:b]);assert quote in excerpt
        assert sha(s['raw_path'])==s['raw_sha256'] and sha(s['text_path'])==s['text_sha256']
        anchors[key]={'id':key,'classification':'AUTHOR_ADDITIONAL_ANCHOR_FROM_EXISTING_FROZEN_RAW','limits':scope,'evidence':[{'source_id':sid,'url':s['requested_url'],'raw_path':s['raw_path'],'source_raw_sha256':s['raw_sha256'],'text_path':s['text_path'],'source_text_sha256':s['text_sha256'],'text_line_1based':a,'text_line_end_1based':b,'quote_exact_short':quote,'full_located_excerpt':excerpt,'http_status_observed':s['http_status_observed'],'retrieval_method':'existing downloaded origin raw; no new network retrieval'}],'independent_review':'PENDING'}
    return anchors

def main():
    for name,want in {
        'research-original.md':'79728c6932d9b6305899a0ffafdcf7f21094b9f4b994101382932bcf3bf2e218',
        'research-original.claims.json':'47b0eb3803241e3ec057eed11a62dd02a1a1d04bf45c0a62575198f294f5c39c',
        'original-preservation.json':'ec235af1f086d9bc3fb1e49e67d6c93a335725aaba8d46e3141207d1ba4ca730',
    }.items():
        assert sha(HERE/name)==want, f'Protected research drift: {name}; stop.'
    anchors=make_anchors();narration=[];claims=[];scenes=[];visual=[];index={};sceneindex={}
    baseline=json.loads((HERE/'history/r5/video.json').read_text())
    base_scenes={s['id']:s for s in baseline['scenes']}
    cameras=['push in','pan left','pull out','tilt down','pan right','tilt up']
    framings=['Close-up','Overhead view','Medium close-up','Medium shot']
    lights=['soft window light','warm lamp light','gentle overhead light','diffuse daylight']
    places={'h':'at an anonymous illustration worktable','a':'at a small paper archive workbench','b':'in a plain research reading corner','c':'at an anonymous storyboard planning surface','d':'at a quiet writing workspace','e':'in a simple publication archive corner'}
    for rownum,row in enumerate(ROWS):
        assert all(k in anchors for k in row['refs'])
        key=row['key'];lines=[l['text'] for l in row['lines']];ids=[l['id'] for l in row['lines']];index[key]=ids;sceneindex[key]=[]
        current={l['id']:l['text'] for l in row['lines']}
        groups=[]
        for old_scene in baseline['scenes']:
            group=[(l['id'],current[l['id']]) for l in old_scene['lines'] if l['id'] in current]
            if group:groups.append((old_scene['id'],group))
        for part_id,group in groups:
            sid=part_id;j=int(sid.rsplit('-p',1)[1])-1;sceneindex[key].append(sid)
            prompt=f"{framings[(rownum+j)%4]} {places[row['ch']]}, anonymous hands {row['action']}, {lights[(rownum+j)%4]}, entirely blank paper surfaces."
            # The single forward event teaser and its payoff share the full request, not just wording.
            if key in ['h04','b08']:
                prompt='Close-up at a plain research table, anonymous hands opening several unmarked research magazines beside entirely blank grid paper, soft window light.'
                camera='push in'
            else:camera=cameras[(rownum+j)%6]
            scene=json.loads(json.dumps(base_scenes[sid],ensure_ascii=False))
            scene['lines']=[dict(next(l for l in base_scenes[sid]['lines'] if l['id']==lid),text=t) for lid,t in group]
            scenes.append(scene)
            visual.append({'scene_id':sid,'row_key':key,'source_anchors':row['refs'],'kind':'ANONYMOUS_CONCEPT_ILLUSTRATION_NOT_HISTORICAL_RECONSTRUCTION','written_visual_review':'PENDING_OTHER_REVIEWER','description':'Only anonymous hands/back views, blank paper/panels, generic tools and unmarked books. No character, silhouette, signature prop, brand/name/logo/readable wording or real likeness. No original art/page/email/film still reproduced.','actual_image_generated':False})
            for lid,t in group:
                narration.append({'id':lid,'text':t,'chapter':CHAPTERS[row['ch']]})
                line_refs=next(l for l in row['lines'] if l['id']==lid).get('refs',row['refs'])
                claims.append({'id':lid,'scene_id':sid,'row_key':key,'text':t,'kind':row['kind'],'source_anchors':line_refs,'evidence':[e for ref in line_refs for e in anchors[ref]['evidence']],'limits':[anchors[ref]['limits'] for ref in line_refs],'status':'AUTHOR_MAPPING_PENDING_INDEPENDENT_SOURCE_REVIEW'})
    names=['哆啦Ａ夢','哆啦A夢','Doraemon','ドラえもん','藤子・Ｆ・不二雄','藤子・F・不二雄','藤本弘','安孫子素雄','藤子不二雄','むぎわらしんたろう','辻村深月','八鍬新之介','路卡','大雄','寺本幸代','伊藤公志','矢嶋哲生','村山功','川村元氣','藤子プロ','小学館','月球探測記','發條都市冒險記','繪畫世界物語','海底鬼岩城','新恐龍']
    used={e['source_id'] for c in claims for e in c['evidence']}
    sources=[{'title':s['title'],'url':s.get('requested_url',s.get('url')),'checked_on':DATE} for s in SOURCES.values() if s['id'] in used]
    video={'schema_version':1,'slug':SLUG,'format':'drama','category':'story','narration_locale':'zh-TW','target_minutes':[12,14],
           'voice':{'provider':'gemini','name':'Sulafat','style':VOICE_STYLE},'subtitles':{'burn_in':True},'look':{'preset':'cute-mystery'},'characters':[],
           'music':{'prompt':'light curious instrumental, gentle paper workshop mood, no vocals','gain_db':-20,'duck_db':-10},
           'loops':[{'setup':index[a][0 if a=='d12b' else -1],
                     'payoff':index[b][{'a03':2,'a07':1,'c03':1,'c06':0,'d12':2,'d12c':1}.get(b,0)],'what':what} for a,b,what in LOOPS],
           'youtube':{'category_id':27,'made_for_kids':False,'default_language':'zh-TW','title':TITLE,'description':'一張原稿留下來，新故事卻仍需要別人動筆。從むぎわらしんたろう另紙接續的回顧，追到2019年辻村深月與八鍬新之介處理月球資料、友情動機、台詞和小說化的工作，再讀2025、2026的版本署名。角色是虛構的，這份製作故事依當事人訪談與官方書目撰寫；匿名插圖不是歷史重建。\n\n來源（查閱2026-10-26）\n'+'\n'.join(s['title']+'\n'+s['url'] for s in sources),'tags':['哆啦A夢','品牌故事','藤子F不二雄','辻村深月','腳本','漫畫','電影改編'],'video_id':None},
           'thumbnail':{'template':'thumb','data':{'layout':'d','headline':'誰還在寫？','sub':'作者走了30年','brand':'哆啦Ａ夢','tag':'品牌故事','shot':sceneindex['h02'][0]}},'sources':sources,'assets':[],'scenes':scenes}
    dump('video.json',video);dump('narration-only.json',narration)
    dump('claims.json',{'schema_version':1,'role':'AUTHOR_MAPPING_NOT_INDEPENDENT_VERDICT','revision':'doraemon-r6','slug':SLUG,'lines':claims,'written_visuals':visual,'anchor_file':'source-anchors-r1.json','research_original_unchanged':True,'research_original_claims_sha256':sha(HERE/'research-original.claims.json'),'independent_source_review':'PENDING','unvoiced_background':json.loads((HERE/'edits-r3.json').read_text())['retired_unvoiced_background'],'cached_source_notice':'D03 uses the retained official interview SEARCH EXTRACTION, origin HTTP503; no origin HTML200 or 1996 serial pages claimed.'})
    dump('source-anchors-r1.json',{'schema_version':1,'role':'AUTHOR_ANCHORS_PENDING_INDEPENDENT_CHECK','anchors':list(anchors.values()),'research_original_claims_sha256':sha(HERE/'research-original.claims.json'),'new_raw_downloads':0,'old_raw_modified':False})
    dump('series.json',{'kind':'story','slug':'brand-stories-adapt-20261017','episode':26,'chapter':1,'title':TITLE,'logline':'保存原紙與寫出新稿是不同工作；沿接稿、2019編劇實作及2025/2026署名看同一世界如何繼續。','names':names,'characters':[],'visual_tier':'stills','compilation':False,'target_minutes':13,'image_model':'image-01','look':{'preset':'cute-mystery'}})
    script=['# Doraemon remake｜R6作者稿','',f'新slug：{SLUG}。作者候選；所有獨立、實聲、影像與站主關卡待審。','']
    for ch,title in CHAPTERS.items():
        script+=['## '+title,'']
        for n in narration:
            if n['chapter']==title:script += [f"**{n['id']}** {n['text']}",'']
    (HERE/'script.md').write_text('\n'.join(script)+'\n')
    md=['# Doraemon R6逐句來源與書面配鏡','','作者建立的待審映射，沒有CONFIRMED/PASS或獨立查核效力。完整原語短引、LF定位、raw/text精確SHA及HTTP層級在source-anchors-r1.json；claims.json將它們逐句展開。','','| 旁白ID | 錨點 | 性質 |','| --- | --- | --- |']
    md += [f"| {c['id']} | {', '.join(c['source_anchors']) or '無新增史實'} | {c['kind']} |" for c in claims]
    md += ['','## 來源邊界','','D03僅取得CoroCoro官方對談的搜尋工具快取，origin本輪HTTP503；不能寫成取得原HTML200，亦不是已讀1996逐頁原件。D04/D05為2017回憶書特設頁的第一人稱留言，不是同期臨終紀錄。D06–D09分清回憶出版、劇場、單行本與電子配信；沒有讀完整130頁回憶書。D29只引用官方附件介紹，沒有讀160頁縮印腳本。角色雖為fiction，本片的製作經歷按非虛構處理。沒有臨終命令、逐頁上墨/ネーム邊界、AI/欺詐代筆或單一總接班人的推斷。','','A05身份／筆名沿革只留不口播的背景錨點；原作者已由a03辨認。R3 c05–c07只交代導演工作要求與當事人實際回應，不承諾解答電影友情或補寫電影情節。','','A01–A07是本輪作者從已保全原語raw新增的精確定位，未改研究三檔，也不是新增獨立來源判定。所有意見、假設與敘事連接都按kind明列；旁白不冒充當事人未公開心理。','','## 書面配鏡','','所有scene都是合法shot模板的匿名概念插圖；空白紙、空白格、無字書與一般工具只示意工作，無品牌/產品/真人名、logo、可讀字、真人長相。不得畫出任何可識別角色、剪影、部位或招牌道具；不得將來源漫畫、照片、電影或email當製片素材。實際圖尚未生成，書面配鏡與實圖judge均待。','','## 預告共圖','','唯一前向事件預告h04的所有拆分scene，必與b08回收的所有拆分scene共用同一完整原生request。image-reuse-plan.json由Stage.imageKey純本機重算；先回收景takes1、驗收，預告前live cache命中及實檔SHA必須吻合，miss即停。兩端各自judge，裁切後選定實檔與組片引用也必須相同；目前actual_same_asset_verified=false。開場h02/h03為原紙的起始場景，不是另一個未來事件預告。']
    (HERE/'claims.md').write_text('\n'.join(md)+'\n')
    counts={'method':'native spokenUnits-compatible author count; exact native count follows in lint receipt','spoken_units_total':sum(units(n['text']) for n in narration),'spoken_units_cold_open':sum(units(n['text']) for n in narration if n['chapter']==CHAPTERS['h']),'spoken_units_voiced_cta':sum(units(r['text']) for r in ROWS if r['kind']=='cta'),'chapters':{title:sum(units(n['text']) for n in narration if n['chapter']==title) for title in CHAPTERS.values()},'lines':len(narration),'scenes':len(scenes),'shots':len(scenes),'cards':0,'loops':len(LOOPS)}
    counts['speech_body_includes_cold_open_and_voiced_cta']=counts['spoken_units_total'];counts['estimated_speech_seconds_at_4_5']=round(counts['spoken_units_total']/4.5,2)
    dump('producer-notes.json',{'schema_version':1,'revision':'doraemon-r6','role':'AUTHOR_PRODUCTION_PLAN_NOT_ADMISSION_OR_APPROVAL','slug':SLUG,'original_slug':'story-adapt-doraemon-after-fujiko','fresh_production':True,'counts':counts,
      'runtime':{'target_minutes':13,'speech_body_seconds_required':[720,840],'body_includes':['cold open','all spoken narration','voiced CTA'],'body_excludes':['new 5-second intro after cold open','new 21-second v4 outro'],'new_bookends_seconds':26,'actual_speech_seconds':None,'actual_bookend_assets_verified':False,'capacity_risk':'About3500 units at4.5/s is a planning calculation only. No measured voice; do not lower13minutes, slow delivery, insert pauses, repeat facts or count bookends to make duration.'},
      'media':{'provider':'minimax','model':'image-01','look':{'preset':'cute-mystery'},'shot_share_by_scene_count':1,'shot_share_by_spoken_units':1,'max_consecutive_cards':0,'runtime_root':str(RUNTIME),'media_base':str(MEDIA),'media_outside_runtime_and_repository':True,'actual_generated_media':0,'actual_same_asset_verified':False},
      'delivery':{'primary_locale':'zh-TW','burn_in':True,'cc':True,'default_later_locales':['en','ja','ko','es','pt','id','vi','th'],'language_media_status':'PENDING_AFTER_CHINESE_FINAL','retain':['clean master without burned captions','original image sources','dry voices','music/effects stems','source-bound text and CC']},
      'budget':{'usd_cap':25,'exact_new_slug_account_created':False,'all_film_quote':None,'protected_admission':'PENDING','original_account_or_approval_reused':False,'paid_calls':0,'policy':'This nonC remake needs its own exact-slug US$25 account, current all-film quote and protected admission before any paid step.'},
      'pending':['independent source and written visual review','two fresh native narrative readers','independent pronunciation review','owner outline and script approval','exact-account all-film quote/protected admission','real TTS and sentence listening','measured speech body720–840s','images and both-end judge / same-file SHA','music and bookends','captions and eight language media','assemble/final QA','owner final approval'],'backend_calls':0,'approvals_created':0,'git_mutations':0})
    dump('row-index-r1.json',{'lines_by_row':index,'scenes_by_row':sceneindex})
    print(json.dumps(counts,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
