---
id: 2026-09-15-life-hub-redesign-web
title: 生活分享 hub 重設計：與旅遊 hub 同構，三段手寫 aside 改由系列列取代
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T01:39:47Z
created_at: 2026-09-15T13:57:49Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guides-hub-redesign-web
scope:
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# 生活分享 hub 重設計：與旅遊 hub 同構，三段手寫 aside 改由系列列取代

## Why

`/life` 用三段手寫 aside 連 Codex／Gemini／Claude Code hub；財經 hub 上線後又要再加一段。

## Definition of done

- [x] `/life` 用 `HubHero`／`TopicTiles`／`SeriesRow`；保留 `filterGeminiArticleLinks` 投影；精選排序。

## Steps

- [x] 重組頁面與測試。

## How to verify

```bash
cd apps/web && npx vitest run "app/[locale]/life/page.test.tsx"
```

## Notes

見 `docs/article-architecture.md`。

2026-09-16 落地（claude-fable-5-1）：`/life` 用 `HubHero`／`TopicTiles`（`?topic=` 仍標示 `aria-current`）／`SeriesRow`；
三段手寫 aside（Codex 學習中心、Gemini、Claude Code）由登錄檔列取代，之後財經 hub 進登錄檔就自動出現。
Gemini 投影保留：hub 是否發布改由登錄檔有無 `web-gemini` 列判斷（等價於原本的 `getGuideArticle` 讀取，少一次 API），
`filterGeminiArticleLinks` 照舊過濾列表；Gemini 卡的說明用 `geminiSeries.entry`（e2e 數 `a[href=hub]` 恰一個並找「N 篇完整教學」）。
列表標題「全部文章」、curated 排序、看更多沿用。
