---
id: 2026-10-13-correct-published-2026-10-07-openai
title: Correct published 2026-10-07 OpenAI math Guide formalization count
status: done
priority: P1
area: docs
owner: codex-second-math-guide
claimed_at: 2026-10-13T09:07:01Z
created_at: 2026-10-13T08:55:53Z
completed_at: 2026-10-13T09:29:53Z
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - docs/openai-math-manuscripts-20261007-guide-correction.md
---

# Correct published 2026-10-07 OpenAI math Guide formalization count

## Why

2026-10-13 在正式站 `/zh-TW/admin/guides` 搜尋 `math-manuscripts`，發現除了 10/06 既刊 Guide，另有五語已刊 `ai-news-openai-math-manuscripts-20261007`，Guide ID `e31a32b6-2f93-4a7a-ba45-ecc729e138b6`。它的繁中描述、摘要、驗證段、表格與 FAQ 仍說 722 份中只有 162 份主結果經 Lean 檢查（約 22%），但 [OpenAI 10/07 官方修訂紀錄](https://github.com/openai/math/blob/main/history.md) 將主要結果形式化覆蓋率更新為 300／719（約 42%）。10/06 原始 README 722 份與 10/07 後現存 719 份也需區分。此篇的「加密貨幣與區塊鏈」標籤、加密資產免責聲明及加密貨幣主題連結亦與數學主題不符，應確認是否內容分類誤植。這是與 `0fe56758-5ac9-468e-b86e-71dabc7e0cd4` 不同的已刊 Guide；不要誤編另一篇。

## Definition of done

- [x] 五語已刊稿逐一核對 722 首發、719 現存、300／719 約 42% **已形式化**，並明確區分形式化與整批成果獨立驗證。
- [x] 清除或修正過時的 162／722 約 22% 舊數字、來源歸因和不符主題的分類／免責／連結，保持合理新聞脈絡。
- [x] 每語經獨立覆核、版本化草稿保存與管理員發布，讀回五語公開頁、已發版本和修訂稽核。

## Steps

- [x] 讀取五語原稿及版本，查 OpenAI 官方 README、10/07 history 與原始公告；準備逐欄更正文案。
- [x] 使用 Guide 編輯器分語保存、審閱、發布；不用新聞候選 AI judge 取代 Guide 人工審稿。

## How to verify

後台搜 `math-manuscripts` 並以完整 slug 與 Guide ID 確認目標；公開 API `/api/travel/guides/life/ai-news-openai-math-manuscripts-20261007?locale=<locale>` 及五個 `/{locale}/life/...` 公開頁逐語讀回。Guide 版本及稽核在編輯器內核對。來源：[OpenAI 現行 README](https://github.com/openai/math/blob/main/README.md)、[10/07 history](https://github.com/openai/math/blob/main/history.md)。

## Notes

2026-10-13 由 `codex-second-math-guide` 認領，針對 Guide ID `e31a32b6-2f93-4a7a-ba45-ecc729e138b6` 完成五語精確草稿、獨立覆核 PASS、版本化保存與管理員發布。已刊版本 zh-TW v6、其餘四語 v4；五語公開頁及稽核 `guide_article_published` 事件均已讀回成功。分類逐語確認為 AI 新聞已勾選／加密貨幣未勾選，錯置投資免責與 crypto 連結已去除。逐欄正文、來源與執行紀錄見 `docs/openai-math-manuscripts-20261007-guide-correction.md`。另票 `2026-10-13-update-published-openai-math-manuscripts-guide` 處理 10/06 文章，兩篇保持分開。
