---
id: 2026-10-22-c10-oxo-owner-script-approval
title: Record C10 OXO owner script approval
status: review
priority: P1
area: docs
owner: codex-gpt6-owner-decisions
claimed_at: 2026-10-22T16:50:07Z
created_at: 2026-10-22T16:49:43Z
completed_at:
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/owner-script-approval.md
---

# Record C10 OXO owner script approval

## Why

站主已核准 C10 當前逐字稿與逐鏡方向；需留下對應內容雜湊、審查證據及未核准的付費邊界，避免後續改稿沿用舊授權。

## Definition of done

- [x] `reviews/owner-script-approval.md` 綁定 80 句劇本、逐鏡 JSON/MD 與當時草稿 PR head。
- [x] 決定與付費／上傳／發布關卡分開。

## Steps

- [x] 讀回當前三份檔案 SHA 與兩位盲讀／來源收據。
- [x] 記錄站主 2026-10-23 核准原話與邊界。

## How to verify

`Get-FileHash` 核對腳本及逐鏡檔；`git diff --cached --check`，再讀回 `gh pr view 1689` 的 head／draft 狀態。

## Notes

此票只記錄站主已給的稿件決定；不得把它當 C10 整支報價或付費批准。實測正文時長及插圖時間比例仍待辦。
