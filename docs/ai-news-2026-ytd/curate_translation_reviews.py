"""Record human decisions; unknown suggestions remain pending and are never applied."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ACCEPT={
 ('ai-news-2026-january-september-index','zh-CN','/document/blocks/4/text'),
 ('ai-news-chatgpt-work-20260709','ko','/document/blocks/21/text'),
 ('ai-news-claude-opus-46-20260205','ja','/document/blocks/8/rows/0/1'),
 ('ai-news-gemini-31-pro-20260219','en','/document/description'),
 ('ai-news-gemini-31-pro-20260219','ja','/document/blocks/9/rows/2/1'),
 ('ai-news-gemini-31-pro-20260219','ja','/document/blocks/11/text'),
 ('ai-news-gemini-31-pro-20260219','ko','/document/blocks/14/text'),
 ('ai-news-gemini-36-flash-20260721','en','/document/blocks/8/rows/0/0'),
 ('ai-news-gemini-36-flash-20260721','ja','/document/blocks/10/text'),
 ('ai-news-gemini-omni-20260519','ko','/document/blocks/1/text'),
 ('ai-news-gemini-omni-20260519','zh-CN','/document/blocks/11/text'),
 ('ai-news-gemini-omni-20260519','zh-CN','/document/blocks/12/text'),
 ('ai-news-gemini-personal-intelligence-20260114','zh-CN','/document/blocks/12/text'),
 ('ai-news-gpt-56-sol-preview-20260626','en','/document/blocks/15/alt'),
 ('ai-news-gpt-56-sol-preview-20260626','ja','/document/blocks/10/rows/1/1'),
 ('ai-news-lyria-3-pro-20260325','en','/document/blocks/8/caption'),
 ('ai-news-meta-muse-spark-20260408','zh-CN','/document/blocks/6/text'),
 ('ai-news-qwen-35-20260216','ko','/diagram/nodes/3/1'),
}
corrections=[];decisions=[];pending=[]
reviews=[json.loads(f.read_text(encoding='utf8')) for f in (HERE/'renders/reviews').glob('*.json')]
for review in reviews:
    slug=review['slug'];doc=json.loads((ROOT/'apps/api/app/guides/content'/f'{slug}.json').read_text(encoding='utf8'))['locales']['zh-TW']
    for issue in review['issues']:
        key=(slug,issue['locale'],issue['id']);entry={'slug':slug,**issue}
        match=re.fullmatch(r'/document/blocks/(\d+)/text',issue['id'])
        if match and doc['blocks'][int(match[1])]['type']=='link':
            entry.update(decision='resolved-by-assembly',reason='Link title and URL are rebuilt from the target published content pack in the same locale, so provider link text is not used.')
        elif key==('ai-news-nvidia-rubin-20260105','ja','/document/blocks/12/text'):
            entry.update(decision='rejected',reason='The hypothetical local retailer is intentionally presented to Taiwan readers; naming Taiwan preserves the editorial context and asserts no new product availability. The proposed replacement would also omit the remaining source sentences, which the current translation retains.')
        elif key in ACCEPT:
            value=issue['correction']
            if slug=='ai-news-chatgpt-work-20260709':value=value.replace('장부상 몇백 원이 부족하지만','장부상 금액이 몇백 정도 부족하지만')
            if key==('ai-news-lyria-3-pro-20260325','en','/document/blocks/8/caption'):
                value='Community film festival music: compare section roles and checks. Allocate seconds to match on-site flow, then listen section by section to check volume changes and speech clarity.'
            entry.update(decision='accepted',reason='Editor compared source and target meaning; no new product facts or currency were added.')
            corrections.append({'slug':slug,'locale':issue['locale'],'id':issue['id'],'text':value})
        else:
            entry.update(decision='pending');pending.append(entry)
        decisions.append(entry)
corrections.append({'slug':'ai-news-chatgpt-health-20260107','locale':'en','id':'/document/blocks/9/caption','text':'Comparison of boundaries and responsibilities in personal record organization, medical terminology, consultation preparation and clinical decisions.'})
(HERE/'translation-corrections.json').write_text(json.dumps(corrections,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'translation-review.json').write_text(json.dumps({'reviewed_articles':len(reviews),'reviews':reviews,'decisions':decisions,'pending':pending},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'reviews':len(reviews),'corrections':len(corrections),'pending':pending},ensure_ascii=False))
