---
id: 2026-09-24-video-terminal-template
title: 影片產線 T10：模擬終端機版型
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:18Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-pilot-ai-model-choice
scope:
  - tools/video/templates/terminal
---

# 影片產線 T10：模擬終端機版型

## Why

Claude Code、Codex 這類終端機工具的教學需要「模擬終端機」版型：逐字打出指令、再顯示輸出。輸出必須來自真的執行（附日期與工具版本），查核代理才能核對，不能憑空寫。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `terminal` 版型：提示字元不露使用者名稱與主機名、逐字打字動畫、輸出分段出現。
- [ ] 輸出檔記錄執行日期與版本，lint 檢查有這兩欄。
- [ ] 用一段 Claude Code 教學跑通。

## Steps

- [ ] 版型與打字動畫（Web Animations 固定時間點截影格）。
- [ ] 輸出記錄格式。

## How to verify

```bash
node --test tools/video/templates/terminal/*.test.mjs
```

## Notes
