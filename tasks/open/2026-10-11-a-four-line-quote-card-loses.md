---
id: 2026-10-11-a-four-line-quote-card-loses
title: A four-line quote card loses the bottom of its last line
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:18:59Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-a-four-line-quote-card-loses.md
  - tools/video/templates/theme.css
  - tools/video/render
---

## Why

frozen main .t-quote blockquote仍max-height370px，舊episode用縮成3行直接引文繞過；4行英文descenders被裁（實際cut row649/1080）問題未修，main同ID缺。

## Done when

- [ ] 4行引用完整呈現或render報明確layout error
- [ ] 1920x1080英文g/p括號fixture、獨立duration-bound review

## Steps

- [ ] 持久化舊票；用原兩段引用sanitize fixture重現
- [ ] 修fitted height/縮字或layout檢測；不改原已通過media/不發paidrequest

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-04-a-four-line-quote-card-loses`。

原始保留分支／核對HEAD：
- `claude/ai-terminology-video-series-c1754d@92e3ae6ba64b75243b6127da2c09d4b96470f0c5`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
