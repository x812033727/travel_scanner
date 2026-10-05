---
id: 2026-10-03-gemini-grounding-offset-unit-recheck
title: gemini-api-search-grounding-citations 說引用位移是 UTF-8 位元組，現行文件不支持
status: done
priority: P2
area: docs
owner: claude-opus-5-5-ai-article-rechecks
claimed_at: 2026-10-05T06:14:20Z
created_at: 2026-10-03T12:04:02Z
completed_at: 2026-10-05T06:48:54Z
branch: claude/ai-article-rechecks
depends_on: []
scope:
  - apps/api/app/guides/content/gemini-api-search-grounding-citations.json
---

# gemini-api-search-grounding-citations 說引用位移是 UTF-8 位元組，現行文件不支持

## Why

AI 名詞第二批查核接地（Grounding）時順帶看到：`gemini-api-search-grounding-citations` 寫引用位移以「UTF-8 位元組」計。
2026-10-03 的 Gemini 文件：Interactions API 參考（2026-10-02 更新）說 UrlCitation 的 `start_index` 是 "measured in bytes"，
但沒有一頁寫 UTF-8；Grounding with Google Search 指南沒寫單位，範例 Go 切位元組、Python／JS／Java 切字元。

## Definition of done

- [x] 文章對位移單位的說法與當天官方文件一致；文件沒寫的就照實寫「文件未說明，範例做法不一」。
- [x] 範例程式（若有）處理中文時不會切錯。

## Steps

- [x] 讀官方 API 參考與指南現行版，必要時用中文樣本實測一次並記錄。

## How to verify

`pack_cli lint --slug gemini-api-search-grounding-citations --warnings`；查證紀錄寫進票。

## Notes

- 來源：`docs/ai-terms-series/batch-02/staging/ai-term-grounding/verify-1.md`。

### 查證紀錄（2026-10-05，claude-opus-5-5-ai-article-rechecks）

三頁都用 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重抓，200，轉純文字對照：

- Interactions API 參考 https://ai.google.dev/api/interactions-api （頁尾 Last updated 2026-10-02 UTC）：UrlCitation 的
  `start_index` 寫「Index indicates the start of the segment, measured in bytes.」，`end_index` 只寫「End of the attributed
  segment, exclusive.」；全頁沒有「UTF」字樣。
- Grounding with Google Search 指南 https://ai.google.dev/gemini-api/docs/google-search （Last updated 2026-09-23 UTC）：
  只說每個 url_citation 有 start_index 與 end_index，沒寫單位；全頁沒有 byte、UTF、character。範例：Python
  `content_block.text[start:end]`、JavaScript `text.slice(...)`、Java `text.substring(...)` 依字串索引切，Go `text[start:end]`
  依位元組切。範例模型仍是 gemini-3.8-flash，回應欄位 google_search_call／search_suggestions／url_citation 與正文表格一致。
- Python SDK 參考 https://googleapis.github.io/python-genai/genai.html ：`Segment.start_index`／`end_index` 寫「Start/End index
  in the given Part, measured in bytes」，沒指明編碼（這頁的 UTF-8 只出現在 tuned model 名稱的說明）。

改了：

- 正文「此版本 SDK 的引用欄位說明以 UTF-8 位元組計算位置……」一段改寫成：Interactions API 參考與 Python SDK 的引用片段欄位都寫
  以位元組計算、沒指明編碼；搜尋教學沒寫單位，範例做法不一（Go 按位元組，Python／JavaScript／Java 按字串索引）；下載包以
  UTF-8 編碼並核對字元邊界，切到半個字的引用會被拒絕。FAQ「可能把位元組位置當成字元位置」與上述一致，沒改。
- 來源：新增 Interactions API 參考與 Python SDK `genai.html` 兩筆（2026-10-05）；指南的 `checked_on` 改 2026-10-05。
  SDK 首頁那筆維持 2026-09-14：正文「genai 2.23.0」的版本號這次沒有複查，首頁也不顯示版本。使用條款這次沒重讀，日期不動。

範例程式：下載包 `lesson-82.zip` 與 `api-verification.zip` 的 `lablib/citations.py` 裡 `byte_segment` 先 `encode("utf-8")`，
範圍不合或切到多位元組字元中間就丟 `ValueError`，`extract_urls` 把它列進 `rejected`；兩個 zip 都不用改。
本機用中文與表情符號樣本跑過這個函式（沒有呼叫 Gemini API；官方參考頁已足以判定單位，不需付費實測）：
`[0:57]` 得到整句「颱風警報資訊請查看中央氣象署官方網站。」、`[0:6]` 得「颱風」、`[1:57]`／`[0:5]`／`[57:59]`（切進表情符號）
都丟 `citation_splits_utf8_character`、超出長度丟 `invalid_citation_range`；同樣的 `[0:6]` 若當字元索引會切出「颱風警報資訊」。

看到但沒改（在本票範圍外的句子）：測試段落「wrong-byte-offset.json 測中文字元被切開時能否報错」的「错」是簡體字，
另開票 `2026-10-05-gemini-grounding-citations-simplified-typo`。

驗證：`PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug gemini-api-search-grounding-citations` 0 errors；
加 `--warnings` 只有既有的 `no_summary`。
