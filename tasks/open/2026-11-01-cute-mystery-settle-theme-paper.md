---
id: 2026-11-01-cute-mystery-settle-theme-paper
title: 主機 cute-mystery 單集 settle 預設 theme paper（奇聞檔案局小卡紙底）
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T04:56:42Z
completed_at:
branch:
depends_on:
  - 2026-11-01-theme-paper-skill-lint-settle
scope:
  - tools/video/automation/flow.mjs
---

# 主機 cute-mystery 單集 settle 預設 theme paper（奇聞檔案局小卡紙底）

## Why

站主 2026-11-01：「奇聞檔案局之後如果有用到的小卡也都用成這樣」（紙白底，同 AI 科技片的 `theme: "paper"`）。
本機路線由 skill 與 lint 警告管（票 2026-11-01-theme-paper-skill-lint-settle）；新集預設走主機 cute-mystery 單集，要在 `settle()` 預設。

## Definition of done

- [ ] `settle()`（`tools/video/automation/flow.mjs`）在 preset 為 cute-mystery 且 writer 沒寫 theme 時設 `settled.theme = "paper"`，
      就放在 `settled.subtitles = … burn_in: preset === "cute-mystery"` 那行旁；附 automation.test.mjs 斷言（cute-cartoon 不受影響）
- [ ] 縮圖照舊（thumb 不套紙底）；關鍵句帶不加（字幕燒錄同區）

## Steps

- [ ] 等 2026-10-24-manga-sticker-drama-pace-visible-camera、2026-10-25-fixprompts-look-blocked-sheet-prompt 釋出或完成（它們認領 flow.mjs）
- [ ] 改 settle、加測試、`npm run test:tools`
- [ ] 部署時機：提示詞 digest 不變；settle 只對新寫好的稿子生效，進行中的集數不受影響

## How to verify

`node --test tools/video/automation/automation.test.mjs`

## Notes

2026-11-01 由 claude-opus-5-5-curio-paper 開票，未認領（scope 被上述兩張票占用）。
