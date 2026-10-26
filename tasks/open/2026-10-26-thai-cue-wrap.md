---
id: 2026-10-26-thai-cue-wrap
title: 泰文字幕換行會撕開音譯名與 เขา|วัว 這類複合詞
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-26T23:57:10Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/captions.mjs
---

# 泰文字幕換行會撕開音譯名與 เขา|วัว 這類複合詞

## Why

`tools/video/core/captions.mjs` 的 `wrapCue` 折泰文字幕時，任何斷詞點都能斷，扣分只有 2，所以會把音譯名和複合詞從中間撕開。2026-10-26 審 `curio-s27-v2` 泰文時看到：ไวกิ้|ง、ไบรอย|ท์、ทาซิ|ทัส、นอร์|ดิก，還有「เขา|วัว」被拆成「他／母牛」。`checkCues` 抓不到這種錯。審稿是靠在詞後加空格繞過去的，其他泰文影片很可能也有同樣情況。

## Definition of done

- [ ] 泰文 cue 內折行不再撕開音譯名或 เขา+วัว 這類複合詞（偏好空格、標點，再來才是一般斷詞點），仍守行寬上限。
- [ ] 其他語言的折行結果不變。

## Steps

- [ ] 在 `wrapCue` 的泰文路徑提高「非空格斷點」的成本，或對連續泰文字母段落只在空格斷。
- [ ] 補單元測試：ไวกิ้ง、เขาวัว 不被切開。

## How to verify

`node --test tools/video/core/captions.test.mjs`；對 `curio-s27-v2` 跑 `captions`，看 th.srt 的 vk408、vk906、vk812。

## Notes

- 同類的日文問題在 `2026-10-26-cue`（日文在詞中間折行）。
- S27 泰文審稿已在譯文加空格避開，修好工具後那些空格不用拿掉。
