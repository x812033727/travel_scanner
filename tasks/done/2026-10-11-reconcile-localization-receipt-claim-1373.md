---
id: 2026-10-11-reconcile-localization-receipt-claim-1373
title: Reconcile PR 1373 localization coverage claim
status: done
priority: P2
area: meta
owner: codex-localization-1373-closeout
claimed_at: 2026-10-11T15:34:43Z
created_at: 2026-10-11T15:34:07Z
completed_at: 2026-10-11T15:36:30Z
branch: codex/localization-receipts-closeout-20261011
depends_on: []
scope:
  - tasks/open/2026-10-07-article-missing-locales-completion.md
  - tasks/open/2026-10-11-reconcile-localization-receipt-claim-1373.md
  - tasks/done/2026-10-11-reconcile-localization-receipt-claim-1373.md
---

# Reconcile PR 1373 localization coverage claim

## Why

PR #1373 的 32 篇已發布收據會把全域補語系總票的過期 4e16 claim 帶回主線。最新 main 657d34790d1446d4f4b2784b4cf5261a22f2c5f6 已將此總票保持 open、未認領；合併收據應保留這個當前狀態。此票只修總票 frontmatter 與自己的收尾紀錄，不接手全域翻譯或發布。

## Definition of done

- [x] 總票 status、owner、claimed_at、branch 與核對時 origin/main 一致：open、未認領，coverage 工作仍未完成。
- [x] 總票正文 bytes 不變，保留 32 篇／128 語系／2 原文修正、160 公開頁／320 截圖的真實發布紀錄與歷史 830／3320 缺口觀察。
- [x] PR 原有九份 docs 與四張完成 release 票保持原有 blob；不重发、部署或聲稱新一波已完成。
- [x] 修正前任務格式與 diff 檢查通過，只有此窄 scope 的 metadata 改動；提交樹驗證由集中收尾 PR 完成。

## Steps

- [x] 查 local worktree branch、遠端 PR head 與開著的 PR；由站主授權協調 PR #1373，原 4e16 工作區不變。
- [x] 在隔離工作區建 codex/localization-receipts-closeout-20261011，透過 task tool claim 此窄票。
- [x] 只取最新 main 的四個認領 frontmatter 欄位，保存原總票、main 對照與正文 SHA。
- [x] 运行 task/check 與 diff --check；核對 receipt blobs 與前後正文，保留被政策保護的 local open duplicate，不納入提交樹。

## How to verify

對原 head 08a280298f41670476f71cf3e2ebf87f663dfd67 比對 changed paths，總票正文 SHA 必須一致；九份 docs／四張 done release 票 blob 與原 head 不變。依站主最新「收在同一個 PR」指示，只建立本機 metadata commit，交由既有 PR #1450 納入全部合法收據與完成票，驗其實際提交樹的 task/check、diff --check 與 required CI。原 #1373 不推新 head、不合併；待 #1450 真正合併且涵蓋全部原 scope 後由站主關成 superseded。

## Notes

- 站主 2026-10-11 授權只修 stale claim 與收尾票；不修改原 owner checkout，不解除其他 claim/HOLD，不做正式站或 provider 呼叫。
- 原 32 篇產品發布已完成；全域 862 篇 queue 與後续 staged cohort仍保留，總票保持 open，不以收據合併當整個補語系計畫完成。
- Decrypt 原始未共享票另有精確快照保全與去重草稿，交由站主新建共享 open/unclaimed；不在本票 scope。
- #1373 原 green HEAD 08a280298f41670476f71cf3e2ebf87f663dfd67 不更新；#1450 須依集中整合後自己的新 HEAD 取得 CI，不沿用舊綠燈。
- 原 body SHA-256：7a262bafb7d8a5faffd293e1d8e1fce404e15fd9cdb3e61f105706eec91aebae；before/readback 及對照存於 <home>/.codex/scratch/codex-closeout-20261011/pr1373-metadata-fix-proof.json。

- 驗證：產生 duplicate 前 node tools/tasks.mjs check 已通過 1,634 票；git diff --check 通過；既有 stale claims 只出 warning。總票 tracked diff 僅 4/4 行 frontmatter，正文 SHA 一致，所有原收據 blobs 保持不變。
- 本票 done 工具已寫完整完成版本，但 Windows 留下同 ID 未追蹤 open copy；精確單檔刪除被 automatic approval policy 拒絕（僅回 blocked by policy）。遵站主指示原檔保持原位，不刪除、移動或改用其他工具；它不納入任何提交，無未追蹤 duplicate 的 #1450 共享提交樹再跑完整驗證。
