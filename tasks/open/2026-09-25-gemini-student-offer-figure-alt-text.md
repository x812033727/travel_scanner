---
id: 2026-09-25-gemini-student-offer-figure-alt-text
title: Gemini 學生方案文章的圖一替代文字與圖不符
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-25T06:01:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-gemini-student-offer-20260820.json
---

# Gemini 學生方案文章的圖一替代文字與圖不符

## Why

2026-09-25 查核影片〈Google AI 學生方案免費一年〉時發現：`ai-news-gemini-student-offer-20260820` 的圖一是 2×2 四格、沒有箭頭的「四道關卡」圖，每格裡有一行說明；替代文字卻描述成別的樣子（見 `docs/videos/gemini-student-offer/verify-1.md`，分支 `claude/video-batch-2`）。替代文字是讀螢幕的人唯一看得到的內容。

## Definition of done

- [ ] 五語系的圖一替代文字都照實描述：四格、各格標題與一行說明、沒有箭頭。

## Steps

- [ ] 對照 `apps/web/public/guides/ai-news-gemini-student-offer-20260820/` 的 SVG 改寫 alt。

## How to verify

`content-pipeline` 的機械檢查過；正式站圖一的 alt 與圖一致。

## Notes

- 只改替代文字，圖本身不動。
