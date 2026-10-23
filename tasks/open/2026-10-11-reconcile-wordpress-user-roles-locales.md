---
id: 2026-10-11-reconcile-wordpress-user-roles-locales
title: 恢復並重綁 WordPress 權限文章的四語交付
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T14:18:40Z
completed_at:
branch:
depends_on:
  - 2026-09-27-correct-wordpress-user-roles-unrelated-ai
scope:
  - tasks/open/2026-10-11-reconcile-wordpress-user-roles-locales.md
  - apps/api/app/guides/content/wordpress-user-roles.json
  - apps/web/public/guides/wordpress-user-roles
  - docs/article-localization/batch031-user-roles-reconciliation
---

## Why

來源 codex/article-localization-031-pair-b@e8fa87d9abb0969a5c9861e5b0b551757cd47ba6 已有四語全文與12素材；#879只採用social-login，user-roles目前main仍只有zh-TW。#875已修正原文普通「參數」誤連AI名詞，但來源正式發布／重綁仍在既有票。

## Done when

- [ ] 繼承已完成作者材料，保留主線修正原文並綁新來源hash。
- [ ] 精確四語＋12素材独立覆核、可合併內容PR與獨立發布交接齊備。

## Steps

先完成既有來源票的版本查核，再比較舊作者稿與新來源，僅調整受影響欄位及審查綁定。

## Verification

來源／目標／素材hash、schema、pack lint、圖像檢視與相關內容／連結測試；正式import/publication另走release gate。

## Notes

日期2026-10-11；social-login已由#879落地，不重做；不擅自付費、部署、覆寫正式來源或恢復錯誤ArticleInline。

原始保留分支／核對HEAD：
- `codex/article-localization-031-pair-b@e8fa87d9abb0969a5c9861e5b0b551757cd47ba6`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
