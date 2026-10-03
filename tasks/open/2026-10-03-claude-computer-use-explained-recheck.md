---
id: 2026-10-03-claude-computer-use-explained-recheck
title: claude-computer-use-explained 的工具版本與 beta 字樣可能落後一版
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-03T12:04:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/claude-computer-use-explained.json
---

# claude-computer-use-explained 的工具版本與 beta 字樣可能落後一版

## Why

AI 名詞第二批寫電腦操作（Computer Use）時讀到：Anthropic 開發者文件現在是分版本的 computer use 工具組，較早版本仍標 beta。
`claude-computer-use-explained`（2026-09-14）的工具名稱與 beta 字樣可能落後一版。方案與平台的說法沒有查。

## Definition of done

- [ ] 文中工具名稱、版本、beta 狀態與當天官方文件一致；方案與平台說法逐條複查。

## Steps

- [ ] 讀 Anthropic computer use tool 文件與 Claude 說明中心現行頁。

## How to verify

`pack_cli lint --slug claude-computer-use-explained --warnings`；查證紀錄寫進票。

## Notes

- 來源：`docs/ai-terms-series/batch-02/staging/ai-term-computer-use/` 撰稿者回報。
