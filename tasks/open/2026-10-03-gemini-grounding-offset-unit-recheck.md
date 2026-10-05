---
id: 2026-10-03-gemini-grounding-offset-unit-recheck
title: gemini-api-search-grounding-citations 說引用位移是 UTF-8 位元組，現行文件不支持
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-ai-article-rechecks
claimed_at: 2026-10-05T06:14:20Z
created_at: 2026-10-03T12:04:02Z
completed_at:
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

- [ ] 文章對位移單位的說法與當天官方文件一致；文件沒寫的就照實寫「文件未說明，範例做法不一」。
- [ ] 範例程式（若有）處理中文時不會切錯。

## Steps

- [ ] 讀官方 API 參考與指南現行版，必要時用中文樣本實測一次並記錄。

## How to verify

`pack_cli lint --slug gemini-api-search-grounding-citations --warnings`；查證紀錄寫進票。

## Notes

- 來源：`docs/ai-terms-series/batch-02/staging/ai-term-grounding/verify-1.md`。
