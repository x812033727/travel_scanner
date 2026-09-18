---
id: 2026-09-16-news-batch-4-4-the-8
title: News batch 4.4: the 8/1 onward secondary news for the three verticals
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-16T14:16:20Z
completed_at:
branch:
depends_on: []
scope:
  - docs/news-2026-batch-4/candidates-secondary.md
---

# News batch 4.4: the 8/1 onward secondary news for the three verticals

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 2026-09-18：站主決定**先不做**這 15 則 8/1–9/15 的次要新聞，改做「9/16 起真正最新的消息」（批次 4.5，另一張票 `2026-09-18-news-batch-4-5-since-0916`）。
  本票的候選清單、幣圈 0 則的查證結果與 scope 都沒動；要做時號段接在 4.5 之後。

## Why

站主最初的要求是「1/1 到現在的**重要新聞**、8/1 到現在的**次要新聞**」，而且
「次要新聞每則各一篇完整文章，不做月份彙整」。重要新聞那 36 篇由 4.1／4.2／4.3 處理，
**這一格是剩下的另一半**，從 `2026-09-16-news-batch-4-the-shared-authoring` 結案時
唯一沒勾掉的那一項接手。

## 現況

候選題目已經列在
[`docs/news-2026-batch-4/candidates-tech-and-ai.md`](../../docs/news-2026-batch-4/candidates-tech-and-ai.md)
最後一節「次要新聞（8/1 → 9/16）」：

| 垂直 | 已列候選 | 狀態 |
| --- | --- | --- |
| AI | 8 則 | 日期與標題來自 OpenAI 官方 feed，**內容都還沒讀原文**（而且 `openai.com/index/*` 在容器裡 403） |
| 科技 | 8 則 | Apple Developer 四則、Windows 一則、NVIDIA 兩則、Pixel Drop 一則；日期已驗、內容未讀 |
| 幣圈 | **0 則** | 見下 |

## 幣圈那 0 則是查證結果，不是偷懶

在站主定的界線內（只寫法規／技術／產業，不碰行情），8/1–9/16 幾乎沒有東西：

- **Federal Register**（涵蓋 SEC／CFTC／FinCEN／OCC／FDIC／NCUA）在這個窗口扣掉例行
  SRO 申報後**只有 3 筆**，其中一筆已列為重要新聞 C4。另一筆是 2026-09-04 的
  Transfer Agent Rules（SEC 提案，評論截止 2026-11-03），**要先確認它是否真的涉及
  代幣化證券**才能用。第三筆是統一議程的例行公告，沒有新聞價值。
- **台灣金管會**：`fsc.gov.tw` 限定搜尋回來的都是 2025 年的，最新一筆是 2025-09-22 的
  VASP 洗錢防制登記名單，**沒有找到 2026 年 8–9 月的項目**。這是「沒查到」不是
  「沒發生」——金管會的站內搜尋在這個環境不好用，要換管道（公報、法規查詢系統）再確認。

**建議做法**：把幣圈的次要新聞窗口放寬到 2026 全年，挑份量較輕的項目
（例如 C10 日本 FSA 的工作小組報告就偏次要），而不是為了湊 4–6 則去寫行情或整合站的內容。

## 開工前提

**4.1／4.2／4.3 先做完。** 理由不是排程，是分工：重要新聞寫完才知道哪些題目已經被涵蓋，
否則次要新聞會跟重要新聞重複（例如 ChatGPT 廣告那條線在 B4 已經有一篇）。

scope 目前只掛一個還不存在的候選檔。**逐篇題目定下來之後**要改成每篇兩行
（`apps/api/app/guides/content/<slug>.json` 與 `apps/web/public/guides/<slug>`），
**不要用整個 `content/` 目錄**。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life    # 0 error
npm run check:tasks
```
