---
id: 2026-10-11-preserve-translator-critique-and-final-when
title: Preserve translator critique and final when repairing malformed outer JSON braces
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:18:56Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-preserve-translator-critique-and-final-when.md
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
---

## Why

原付費Japanese answer因兩個額外外層右大括號，parseObject取第一個有效draft而丟棄critique/final；frozen main仍只有單次早閉brace修補，沒有此完整envelope恢復。此票只在pre-rebase ref，2a98現worktree與main均缺。

## Done when

- [ ] 保守修復明確可復原的外層brace時保留完整draft/critique/final，交正常finalAnswer
- [ ] 歧義、內容更改、缺critique/破字串仍拒絕；原provider text/journal immutable

## Steps

- [ ] 把原票持久化到 main共享看板，交保留的 codex/stalled-videos-completion-20261008 successor對帳
- [ ] 用sanitized fixture重現原SHA df3c9eb4…；只測parser，不dispatch模型
- [ ] 驗actual final25條critique/24captions來源字節，拒絕歧義

## Verification

對當前主線及原source/hash做可查核回歸；實作只在未與active scope衝突時另claim本票。先對帳歷史缺件與目前替代，不將舊失敗當成現在仍未修。

## Notes

原始任務 ID：`2026-10-08-preserve-translator-critique-and-final-when`。
- 舊私有raw SHA df3c9eb43f3b6a0195b75a1ce7d59736c7a3d79db067a5b4abc7346168c58370；structural-view d9828dd78d3998ebbe515ac72a3bb628d71e3585c527e5f36604660fb9836b47
- 保留sourceTaskId與 successor pointer，不接管 paid/STOP 工作

原始保留分支／核對HEAD：
- `codex/stalled-video-reviewed-fixes-pre-oct9-rebase@8bac279ed87abe38aa7f29379643a05a52960f7a`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
