---
id: 2026-10-27-thai-captions-time-pieces-by-thai
title: Thai captions: time pieces by Thai letters, not by Latin words alone
status: review
priority: P2
area: tools
owner: claude-opus-5-5-happy-brahmagupta
claimed_at: 2026-10-27T00:49:34Z
created_at: 2026-10-27T00:49:33Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/captions.test.mjs
---

# Thai captions: time pieces by Thai letters, not by Latin words alone

## Why

`timePieces`（`tools/video/core/captions.mjs`）沒有逐字時間可用時，照每段的 `weight()` 分這一句的時間，而 `weight()` 用的 `spokenUnits` 只數拉丁單字（每個 2）、數字與中日韓字。泰文不在裡面，一整段泰文的權重是 1。所以一句泰文裡夾著 `UCC Milk Coffee` 或 `1969` 的話，時間幾乎都被拉丁那段拿走。

實例是 2026-10-27 的 C11 UCC remake 泰文字幕：`c11r1h02` 的長段只分到 0.88 秒（每秒 70.5 字），`c11r1w11` 每秒 41.8 字，短的英文段卻掛了 7 秒；整支片有 10 個 cue 讀太快。

## Definition of done

- [x] 泰文按基本字母計權（約 5 個字母等於一個拉丁單字，組合的母音與聲調符號不計），其他語言的權重不變。
- [x] 回歸測試用那一句真的泰文：長段拿到較長的時間，兩段都不超過 `maxCps`；拿掉修正後這個測試會失敗。

## Notes

- C11 重跑 `captions`：泰文需要看的 cue 從 10 降到 1。
- `node --test` 跑 `tools/video` 全部：2423 pass、0 fail。
- 不在 `docs/videos/long-form/review.json` 綁定的檔案裡。
