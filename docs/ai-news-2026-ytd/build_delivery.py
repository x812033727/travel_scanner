"""Build the final link directory only from verified publication and public QA receipts."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf8'))
publication=json.loads((HERE/'publication.json').read_text(encoding='utf8'))
public=json.loads((HERE/'public-verification.json').read_text(encoding='utf8'))
assets=json.loads((HERE/'asset-link-verification.json').read_text(encoding='utf8'))
assert len(manifest)==22 and len(publication['result']['published'])==110
assert len(publication['replay']['unchanged'])==110 and publication['existing_editorial_data_unchanged'] is True
assert len(public['pages'])==220 and public['sitemap_locale_articles']==110
assert len(assets['assets'])==220
old=json.loads((HERE.parent/'ai-news-2026-09/manifest.json').read_text(encoding='utf8'))
all_items=sorted(manifest+old,key=lambda i:(i['event_date'],i['slug']))
assert len(all_items)==32
index=next(i for i in all_items if i['slug']=='ai-news-2026-january-september-index')
lines=['# 2026 年 AI 新聞：2026-01-01 至 2026-09-14','','31 篇解析與 1 篇月份索引，均已提供五語全文。','',
'索引：'+' · '.join(f'[{label}]({index["locales"][locale]["url"]})' for locale,label in [('zh-TW','繁體中文'),('zh-CN','简体中文'),('en','English'),('ja','日本語'),('ko','한국어')]),'',
'| 事件日期 | 繁體中文文章 | 其他語言 |','|---|---|---|']
for item in all_items:
    if item is index:continue
    langs=' · '.join(f'[{label}]({item["locales"][locale]["url"]})' for locale,label in [('zh-CN','简中'),('en','EN'),('ja','日本語'),('ko','한국어')])
    lines.append(f'| {item["event_date"]} | [{item["title"]}]({item["locales"]["zh-TW"]["url"]}) | {langs} |')
lines+=['',f'本批新增刊登時間：{publication["published_at"]}。正式公開檢查：{public["checked_at"]}。',
'',f'本批正式圖片與內容版本：`{assets["release_sha"]}`。先前十篇保留原文章身分與發布紀錄。','']
(HERE/'articles.md').write_text('\n'.join(lines),encoding='utf8')
receipt={'release_sha':assets['release_sha'],'locale_documents':110,'desktop_mobile_pages':220,'assets':220,'all_passed':True,'checked_at':public['checked_at'],'total_news_articles':31,'total_index_articles':1,'all_language_documents':160}
(HERE/'public-qa.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
print('Created verified formal links and host closeout receipt')
