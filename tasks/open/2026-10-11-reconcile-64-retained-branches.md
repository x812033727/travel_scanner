---
id: 2026-10-11-reconcile-64-retained-branches
title: Deeply reconcile the original 64 retained historical branches
status: in-progress
priority: P2
area: meta
owner: codex-gpt6-retained64-audit
claimed_at: 2026-10-11T13:54:28Z
created_at: 2026-10-11T13:54:27Z
completed_at:
branch: codex/historical-branches-cleanup-20261011
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-64-retained-branches.md
  - tasks/done/2026-10-11-reconcile-64-retained-branches.md
  - tasks/open/2026-10-11-retained-historical-branches.md
  - tasks/open/2026-10-11-reconcile-wordpress-user-roles-locales.md
  - tasks/open/2026-10-11-localize-batch003-zh-tw-diagram-helpers.md
  - tasks/open/2026-10-11-reconcile-merchant-style-batch08-acceptance.md
  - tasks/open/2026-10-11-restore-transit-timing-fare-precision.md
  - tasks/open/2026-10-11-reconcile-wordpress-map-source-release.md
  - tasks/open/2026-10-11-restore-deploy-verifier-freshness-exit.md
  - tasks/open/2026-10-11-video-held-retry-status.md
  - tasks/open/2026-10-11-restore-merchant-style-first-failure-investigation.md
  - tasks/open/2026-10-11-restore-news-dedup-admission-order.md
  - tasks/open/2026-10-11-restore-tidy-capped-list-retention-guard.md
  - tasks/open/2026-10-11-reconcile-legacy-host-redeploy-hardening.md
  - tasks/open/2026-10-11-restore-agent-community-sweeper-services.md
  - tasks/open/2026-10-11-preserve-translator-critique-and-final-when.md
  - tasks/open/2026-10-11-stalled-production-video-completion.md
  - tasks/open/2026-10-11-make-durable-polling-deadline-regression-deterministic.md
  - tasks/open/2026-10-11-retain-existing-guide-packs-in-imported.md
  - tasks/open/2026-10-11-use-normal-caption-warnings-and-local.md
  - tasks/open/2026-10-11-video-stage-receipt-site-identity.md
  - tasks/open/2026-10-11-vps-uploader-initialization-rejects-numeric-install.md
  - tasks/open/2026-10-11-a-four-line-quote-card-loses.md
  - tasks/open/2026-10-11-a-slides-storyboard-whose-pictures-all.md
  - tasks/open/2026-10-11-shot-prompts-put-the-look-first.md
  - tasks/open/2026-10-11-integrate-retained-video-source-fixes.md
---

## Why

站主要求深入核對原197清理候選中，首輪保留的64個未完成分支。這64個不含前一輪已深入核對的24個；前輪已清理17、保留7與其6張新票保持原紀錄。本票追查實際差異與後續替代證據，將可清理的完成ref完整備份後清理，為真正未完成的內容補上具體待辦。

## Done when

- 原64分支逐一有完整task/patch/PR/替代版本與收據對照；完成scope與後續發布／製作／owner gate分開記錄。
- 可清理ref完整bundle、SHA-256與空白bare repo独立逐HEAD還原通過；执行比對預期HEAD、checkout/openPR，事後核對不存在。
- 所有未完成／使用中／dirty工作保留，具體下一步與已有或恢復的窄scope票列入共享索引，原認領與HOLD不變。
- 原197帳面總數與實際ref/readback一致；tasks check及diff check通過，更新既有draft PR1450。

## Steps

- [x] 從首輪audit固定原64分支，重新fetch兩clone、盤點PR/HEAD/worktree及正在使用的session。
- [x] 記錄9個工作目錄的status、現存修改檔案SHA-256／bytes、缺檔狀態與完整index-stage signature。
- [x] 深入讀64個unique patch、task全文、替代PR、合併差異、source/receipt與後續scope。
- [x] Root覆核完成與保留清單；需要保存的原始草稿／操作收據記錄完整HEAD。
- [ ] 備份與獨立還原驗證後，僅對已完成且fresh guards通過的本機ref清理。
- [ ] 更新保留分支索引，補回缺失具体工作而不重開已解舊案或原owner工作。
- [ ] 核對全197數量與保存結果、檢查任務與差異，準備更新draft PR1450。

## Verification

每個原64候選都有獨立結論；deleted ref absence、retained ref presence、新HEAD變動與worktree status/index/現存bytes有readback。9個worktree的工作不被重設或接管；未提交缺檔與有內容的修改分別記錄，不能把缺檔冒稱實際翻譯改稿。Shared queue變更限本票scope，所有原active claims與source hold保留。

## Notes

- 固定main：`1f183e4d1f3bb493b5412ca242f2cbb98da4f9bf`；兩clone相同。
- 證據／執行／還原清單：`C:/Users/x8120/.codex/scratch/retained64-followup-20261011/`。
- Fresh status共3254個未提交路徑，3202缺檔、52現存檔案；前兩個locale preservation worktree合計3199都是deleted working paths。9個checkout均保留。
- Claude偶的江湖分支HEAD相對首輪已新增commit；按本輪fresh HEAD核對，後續owner新提交仍保留，不將idle或clean當ownership release。
- 本票只核對與記錄；正式站、生成／付費、其他工作目錄、原票認領與remote舊分支不改動。

## Durable task checkpoint

本輪已恢復23張具體open、未認領票；PR921兩分支共用同票，speaking-rate連回既有pace票。source整合沿用PR1387，不另開同義source PR。原owner/claim/HOLD/STOP保持；新票將先保存至既有draft PR1450，尚未合併main，未執行任何待辦實作。完整來源JSON、正面／反面比對與root逐筆決策在本輪scratch。
