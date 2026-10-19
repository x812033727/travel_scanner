---
id: 2026-10-11-reconcile-wordpress-map-source-release
title: 對帳 WordPress 地圖來源發布與語系來源重綁
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T14:18:53Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-wordpress-map-source-release.md
  - docs/article-localization/releases/wordpress-map-source-reconciliation
---

## Why

原票codex/wordpress-map-form-token-link-task@f61b7436c2d0385b69d3ba5a890ebc0d78e8b4f4未入main。#887與done alias完成repository block3 inline1普通「標記」修正，但正式source publish/publicversion與Batch034 rebind沒有完成證據；current pack只有zhTW。

## Done when

- [ ] fresh readonly確認public source與corrected repository是否同revision/hash，已完成者有精確receipt。
- [ ] 若仍欠source publish，受控release後rebind Batch034並交獨立四語發布票。

## Steps

先核對live identity／visibility／draft／published version與hash，保全歷史captures；所有write另按release coordination/backups/authorization gate。

## Verification

publicblock3普通標記无AI token連結；其餘正文與sourceversion差異清楚，freshsourcehash與bundlemanifest一致。

## Notes

日期2026-10-11；source-only #887 dd1d517已完成不重開。本次草稿不授權正式write/deploy/paidcall，舊v2/v4非currentproof。

原始保留分支／核對HEAD：
- `codex/wordpress-map-form-token-link-task@f61b7436c2d0385b69d3ba5a890ebc0d78e8b4f4`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
