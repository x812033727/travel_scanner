---
id: 2026-09-13-life-ai-series-catalogue
title: 生活分享 AI 系列：220 篇總表 docs/life-ai-series.md
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T11:56:01Z
created_at: 2026-09-13T11:55:58Z
completed_at:
branch: claude/festive-brown-6nsxfm
depends_on: []
scope:
  - docs/life-ai-series.md
---

# 生活分享 AI 系列：220 篇總表 docs/life-ai-series.md

## Why

站主要在生活分享放至少 200 篇 Claude、Codex、ChatGPT、Gemini、MiniMax 等 AI 工具的介紹與教學。
分十一批、多個 session 產出，slug 與標題要先定死，批次票的 scope 才能精確到檔案、彼此不互卡。

## Definition of done

- [ ] `docs/life-ai-series.md`：目的與讀者、語系（zh-TW）、配圖與合作連結政策、十一個批次與任務票、
      220 篇的 slug／標題／topics／圖／合作／易變、產製流程、經驗記錄區。
- [ ] 所有 slug 符合 `SLUG_PATTERN`、與現有 50 個旅遊 slug 不重複、topics 只用 life 詞彙。

## Steps

- [ ] 寫總表。
- [ ] 用 `guides-pack lint --catalogue` 對一次（工具票完成後）。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
```

## Notes

- 總表不記錄狀態；內容包檔案存在就是寫了。批次完成後不改總表，只在「經驗記錄」加一兩行。
