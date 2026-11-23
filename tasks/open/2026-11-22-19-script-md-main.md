---
id: 2026-11-22-19-script-md-main
title: 種田第 19 集 script.md 的真人版兩節帶上 main
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-22T11:06:59Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e019-r2/script.md
---

# 種田第 19 集 script.md 的真人版兩節帶上 main

## Why

種田娶妻打天下（真人版）第 19 集的成片是照 `docs/videos/zhong-tian-qu-qi-e019-r2/script.md` 裡〈真人版的改動〉〈審稿後的修改〉兩節拍的。這兩節目前只在分支 `claude/inspiring-lovelace-luesgx` 上，main 的 script.md 還是 2026-11-06 的 CG 稿。之後有人拿 main 的稿子審第 19 集，會照舊稿判錯（2026-11-21 審片報告第 8 條，站主 2026-11-22 照建議開票）。

## Definition of done

- [ ] main 的 `docs/videos/zhong-tian-qu-qi-e019-r2/script.md` 有這兩節，內容跟分支上的一致。

## Steps

- [ ] 比對分支與 main 的這份檔，只帶上這兩節，不動其他段落。
- [ ] 若分支整個合併進 main 時已經帶上，直接結案。

## How to verify

`git diff origin/main -- docs/videos/zhong-tian-qu-qi-e019-r2/script.md` 在合併後只剩無關的差異或沒有差異。

## Notes

- 審片報告在雲端 `AI劇/種田娶妻打天下（真人版）/_共用/製作檔/review-e001-e030-20261121/`（e019 第 5–7 行與第 169 行）。
