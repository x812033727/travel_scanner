---
id: 2026-09-19-ai-news-batch-4-6-since
title: AI 新聞批次 4.6：2026-09-18 的兩則（Anthropic 內嵌式評估、Google Flow 與時裝週）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T11:57:24Z
completed_at:
branch: claude/ai-teaching-news-expansion-wa6kur
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-anthropic-accenture-evaluation-20260918.json
  - apps/api/app/guides/content/ai-news-google-flow-fashion-20260918.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/news-2026-batch-4
  - docs/ai-news-2026-09-late
  - apps/web/public/guides/ai-news-anthropic-accenture-evaluation-20260918
  - apps/web/public/guides/ai-news-google-flow-fashion-20260918
---

# AI 新聞批次 4.6：2026-09-18 的兩則（Anthropic 內嵌式評估、Google Flow 與時裝週）

## Why

站主 2026-09-19 要求「新增 AI 相關新聞」。批次 4.5 收到 9 月 18 日的 Google CC 家庭版為止
（`display_order` 166）。這一批補上同一天另外兩則有一手來源可寫的公告，接在 167、168。

## Definition of done

- [x] 兩個五語內容包通過 `check_article.py <slug> --full --assets`。
- [x] 兩篇的研究紀錄（含四個語言的 `translations`）寫在 `docs/ai-news-2026-09-late/research/`。
- [x] 十組圖檔（五語各一張 hero.jpg／hero.svg 與一張 diagram-1.svg）建好，都在位元組上限內。
- [x] 既有索引 `ai-news-2026-january-september-index` 原地增補：五語各加兩個連結、日期句改成 9 月 19 日。
- [x] `pack_cli lint --kind life` 0 errors；四個 guides 測試檔全綠；`npm run check:tasks` 綠。
- [ ] 站主決定要不要發布；發布後照批次 4.5 的做法先部署再 `guides-import --slug` 兩篇＋索引同一趟。

## Steps

- [x] 找消息：官方 feed 三個（openai.com/news/rss.xml、blog.google/rss/、anthropic.com/news），
      挑出 9 月 18 日有一手頁面可讀的兩則。
- [x] 撰稿 zh-TW，逐條事實對照抓下來的頁面；四個語言各自寫一份，用 `merge_locale.py` 併入。
- [x] `check_article.py` 的 `RELATED` 加兩行（位置即 `display_order`，所以是 167、168）。
- [x] `build_assets.py` 加兩個 hero 構圖，`--slug` 只建這兩篇。
- [x] `update_index.py` 改寫成批次 4.6 的設定後跑 `ai`。
- [x] `pack_cli relink --slug` ×2 → `autolink --slug` ×2 → 用 ai-workflow 系列的 `prune_autolinks.py`
      把兩篇正文裡單獨一個「AI」的連結還原成文字（兩篇各剪 1 條）。
- [ ] 人眼看過十張圖（這一輪沒有重建 contact sheet，見下方「留給下一位」）。

## How to verify

```bash
cd apps/api
for s in ai-news-anthropic-accenture-evaluation-20260918 ai-news-google-flow-fashion-20260918; do
  ./.venv/bin/python3 ../../docs/news-2026-batch-4/check_article.py "$s" --full --assets
done
./.venv/bin/python3 -m app.guides.pack_cli lint --kind life | grep -c "error:"   # 0
./.venv/bin/python3 -m pytest tests/test_guide_series.py tests/test_guides_content_pack.py \
  tests/test_guides_pack_ingest.py tests/test_guides_content_links.py -q
```

## Notes

- **OpenAI 9 月 18 日那則沒有寫**：`Introducing the Australian Youth Safety Blueprint`。
  `openai.com/index/...` 對 curl 回 403（BRIEF 已經記過這件事），官方 RSS 只有一行描述，
  湊不出一篇有依據的文章。依 BRIEF「查到的事實如果只存在於被擋的頁面後面，那就不寫」略過。
  想補的人要先解決 403，不要拿媒體報導充數。
- **索引的來源已經到上限**：`GuideDocument` 的 sources 上限是 20，索引原本 19 條。
  所以 `CITED` 只放了 Anthropic 那一篇的第一個來源，Google 那篇的來源留在它自己的文章裡。
  下一批要再引用索引來源，得先決定拿掉哪一條舊的。
- **`update_index.py` 是一次性腳本**：它的句子替換必須剛好命中一次，所以批次 4.5 的
  `NEW`／`CITED`／`EDITS`／`INSERT` 不能留著重跑。這一輪把那四張表改寫成 4.6 的內容
  （crypto 與 tech 清空），日期常數 `EXPANDED_ON` 改成 2026-09-19。
  改寫時一度把 `_QUANTITY` 等 regex 常數與 `TABLE`／`DROP_COLUMN` 一起刪掉，
  下一位改這個檔案時，只動 `EXPANDED_ON` 到 `EDITS` 這一段，不要碰後面的工具常數。
- **索引的事件日沒有動**：兩篇都是 9 月 18 日的事件，所以 callout 的「事件到 2026-09-18 為止」
  維持原樣，只改「最後增補於」。加進第二段的那一句刻意不寫篇數，因為 `COUNT_RULE["ai"]`
  會擋掉索引裡任何「幾篇」的說法。
- **兩篇都沒有獨立查核**：批次 4.3 與 4.5 是「一篇一個撰稿代理，另一個代理獨立查核」。
  這一輪由同一個模型撰稿並自檢，`docs/news-2026-batch-4/factcheck/` 沒有這兩篇的報告。
  每一條事實都在研究紀錄裡附了出處與原文片段，但「查核不能由撰稿者自己做」這條沒有滿足，
  發布前值得補一輪。

### 留給下一位

- 沒有重建 contact sheet（那是全量建置，會重畫本工作區其他十八篇的圖）。要人眼審圖時，
  跑不帶 `--slug` 的 `build_assets.py ai`，再看 `docs/ai-news-2026-09-late/` 下的 sheet。
- 兩篇都寫明本站沒有實際使用、沒有參與、沒有取得當事人說法，發布前不要把這些句子拿掉。
- Google 那篇的頁面上有一段官方標為「由 Google AI 產生、實驗性質」的摘要，
  研究紀錄已經寫明沒有拿它當依據；之後要補寫這篇時，一樣不要引用那一段。
