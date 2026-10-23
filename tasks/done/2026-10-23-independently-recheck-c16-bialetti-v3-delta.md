---
id: 2026-10-23-independently-recheck-c16-bialetti-v3-delta
title: Independently recheck C16 Bialetti v3 delta
status: done
priority: P1
area: docs
owner: codex-c16-v3-delta-review
claimed_at: 2026-10-23T05:30:28Z
created_at: 2026-10-23T05:30:21Z
completed_at: 2026-10-23T05:32:13Z
branch: codex/c16-bialetti-v3-delta-review
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/c16-v3-delta-review.md
---

# Independently recheck C16 Bialetti v3 delta

## Why

草稿 PR #1704 的 C16 Bialetti 作者稿在舊版 81/81 獨立 PASS 後再改三句與同 ID 配鏡。舊雜湊上的審查不能覆蓋新 bytes；需要非作者核對來源、跨章回收、視聽一致與改動邊界。

## Definition of done

- [x] 以新 head 的四份 Git blob SHA-256 留下可追溯的三處差異 PASS／HOLD 收據。
- [x] 核對 81/81 旁白及視覺 ID、Markdown／JSON 對鏡內容和新舊改動範圍。

## Steps

- [x] 只讀作者工作樹，比對 `b98f47e` 與 `09e24dc` 並重開有關一手來源。
- [x] 逐項評估 `c160212→301`、`c160417→501`、`c160519→601` 及同 ID 圖像。
- [x] 以草稿、`no-auto-merge` 的 stacked PR 交付獨立收據；保留作者及站主後續關卡。

## How to verify

收據 `docs/videos/story-everyday-bialetti-c16/reviews/c16-v3-delta-review.md`。從 `git show 09e24dc:<path>` 的 bytes 以 Python SHA-256 重算四份雜湊、三組 ID 差異及 81/81 Markdown／JSON 欄位一致；`npm run check:tasks` 和 `git diff --check`。

## Notes

新 head `09e24dc11b9d0e3549a7c31f80d33db79d56ec82` 的來源／視覺差異審查為 HOLD：`c160212` 與 `c160417` PASS；`c160601` 的隔日同戶動作在旁白沒有明示概念或條件，M06 只支持可拆合和重複使用的能力。圖像 prompt 有「概念」標示，可保留，但須由作者窄修旁白後用新雜湊再核。兩位新旁白盲讀、站主核稿、TTS 實測與付費媒體均未完成。

`npm run check:tasks` 在 `done` 前 exit 0。`done` 產生完成檔後留下未追蹤的 `tasks/open` 原檔；一次精確路徑的 `Remove-Item` 遭執行政策 `blocked by policy`。停止清理嘗試；PR 只納入本完成檔及收據，不納入 open 副本。提交樹的任務板檢查交 CI 驗證。
