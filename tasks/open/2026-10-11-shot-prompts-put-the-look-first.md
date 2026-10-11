---
id: 2026-10-11-shot-prompts-put-the-look-first
title: Shot prompts put the look first for image models that take no style reference
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:19:00Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-shot-prompts-put-the-look-first.md
  - tools/video/media/keyframes.mjs
  - tools/video/media/prompt-budget.mjs
  - tools/video/core/drama.mjs
  - tools/video/media/look-keyframes.test.mjs
---

## Why

main composeShotPrompt仍scene→Style→Camera→Characters，no-style-reference image-01仍無look.lead。四稿手工lead+positive customlook繞過，原票main缺；stage key更改會影響已付費pictures。

## Done when

- [ ] 只對catalog no-style-reference型號採style lead，motif lint兼容
- [ ] negative prompt能力明確處理，scene/source cache unchanged媒體不無故重買
- [ ] dry-run/timing source-bound regressions和独立duration receipt

## Steps

- [ ] 持久化原票；盤composeShotPrompt/capability/imageKey
- [ ] scope review後保守model-gated composition和cache transition，不當場重畫已過pictures

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-04-shot-prompts-put-the-look-first`。

原始保留分支／核對HEAD：
- `claude/ai-terminology-video-series-c1754d@92e3ae6ba64b75243b6127da2c09d4b96470f0c5`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
