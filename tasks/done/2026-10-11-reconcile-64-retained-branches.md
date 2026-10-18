---
id: 2026-10-11-reconcile-64-retained-branches
title: Deeply reconcile the original 64 retained historical branches
status: done
priority: P2
area: meta
owner: codex-gpt6-retained64-audit
claimed_at: 2026-10-11T13:54:28Z
created_at: 2026-10-11T13:54:27Z
completed_at: 2026-10-11T14:25:43Z
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
- [x] 備份與獨立還原驗證後，僅對已完成且fresh guards通過的本機ref清理。
- [x] 更新保留分支索引，補回缺失具体工作而不重開已解舊案或原owner工作。
- [x] 核對全197數量與保存結果、檢查任務與差異，準備更新draft PR1450。

## Verification

每個原64候選都有獨立結論；deleted ref absence、retained ref presence、新HEAD變動與worktree status/index/現存bytes有readback。9個worktree的工作不被重設或接管；未提交缺檔與有內容的修改分別記錄，不能把缺檔冒稱實際翻譯改稿。Shared queue變更限本票scope，所有原active claims與source hold保留。

## Notes

- 固定main：`1f183e4d1f3bb493b5412ca242f2cbb98da4f9bf`；兩clone相同。
- 證據／執行／還原清單：`<home>/.codex/scratch/retained64-followup-20261011/`。
- Fresh status共3254個未提交路徑，3202缺檔、52現存檔案；前兩個locale preservation worktree合計3199都是deleted working paths。9個checkout均保留。
- Claude偶的江湖分支HEAD相對首輪已新增commit；按本輪fresh HEAD核對，後續owner新提交仍保留，不將idle或clean當ownership release。
- 本票只核對與記錄；正式站、生成／付費、其他工作目錄、原票認領與remote舊分支不改動。

## Durable task checkpoint

本輪已恢復23張具體open、未認領票；PR921兩分支共用同票，speaking-rate連回既有pace票。source整合沿用PR1387，不另開同義source PR。原owner/claim/HOLD/STOP保持；新票將先保存至既有draft PR1450，尚未合併main，未執行任何待辦實作。完整來源JSON、正面／反面比對與root逐筆決策在本輪scratch。

## Completion record

原64逐項深核對完成：本輪清理42個、保留22個；其中18個實際未完成、4個原scope完成但checkout/dirty保留。原197累計清理168個、保留29個。前輪7個索引區塊逐字保留。

所有9個checkout、原claims與外部素材保留，《偶的江湖》按站主確認仍在Claude製作，永不納入本輪cleanup。所有42個刪除ref均全歷史bundle、SHA256、空白bare repo獨立逐HEAD還原通過；每筆刪除前重新讀openPR/worktrees，以預期HEAD CAS，事後驗證ref不存在。新票先保存至draft PR1450，再清歷史ref；沒有將新票宣稱main已合。

- 本輪備份`<home>\.codex\scratch\retained64-followup-20261011\completed-codex.bundle`：38heads；SHA256 `6699e2f8fb3a02d9e088cb80140611b3d3d670682dbd91e4545a2e778b140794`；獨立還原與事後雜湊通過。
- 本輪備份`<home>\.codex\scratch\retained64-followup-20261011\completed-claude.bundle`：4heads；SHA256 `45669fde7446eb8548ee5476d3cf40e2988900b938b4cd091a6375a33d5b69a7`；獨立還原與事後雜湊通過。

工作目錄readback：

- `codex/article-localization-batch016-llms`：692未提交路徑（0現存檔、692缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `codex/article-localization-source-edit-preservation`：2507未提交路徑（0現存檔、2507缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `codex/batch003-qa-tasks`：0未提交路徑（0現存檔、0缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `codex/news-recovery-20261010`：13未提交路徑（13現存檔、0缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `codex/pr921-tidy-metadata-current`：17未提交路徑（17現存檔、0缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `codex/stalled-videos-completion-20261008`：13未提交路徑（10現存檔、3缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `claude/ou-de-jianghu-e001-285512`：0未提交路徑（0現存檔、0缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `claude/youtube-language-manifest`：0未提交路徑（0現存檔、0缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。
- `wf-fix-1342`：12未提交路徑（12現存檔、0缺檔）；status/內容SHA256相同=True，index-stage簽章相同=True；branch完整保留。

恢復23張open、未認領的具體票，PR921共用一票，voice/pacing另連回已存在票；三項source修補只跟進現有PR1387及原owner，不重建PR。新票與scope含文章四語／SVG、交通秒數/票價、去重、素材保留、部署對帳、影片producer/parser/runtime/receipt/source修補與必需owner policy決策。沒有實作、生成／付費、正式站或素材清理。

- [2026-10-11-reconcile-wordpress-user-roles-locales](../../tasks/open/2026-10-11-reconcile-wordpress-user-roles-locales.md)。
- [2026-10-11-localize-batch003-zh-tw-diagram-helpers](../../tasks/open/2026-10-11-localize-batch003-zh-tw-diagram-helpers.md)。
- [2026-10-11-reconcile-merchant-style-batch08-acceptance](../../tasks/open/2026-10-11-reconcile-merchant-style-batch08-acceptance.md)。
- [2026-10-11-restore-transit-timing-fare-precision](../../tasks/open/2026-10-11-restore-transit-timing-fare-precision.md)。
- [2026-10-11-reconcile-wordpress-map-source-release](../../tasks/open/2026-10-11-reconcile-wordpress-map-source-release.md)。
- [2026-10-11-restore-deploy-verifier-freshness-exit](../../tasks/open/2026-10-11-restore-deploy-verifier-freshness-exit.md)。
- [2026-10-11-video-held-retry-status](../../tasks/open/2026-10-11-video-held-retry-status.md)。
- [2026-10-11-restore-merchant-style-first-failure-investigation](../../tasks/open/2026-10-11-restore-merchant-style-first-failure-investigation.md)。
- [2026-10-11-restore-news-dedup-admission-order](../../tasks/open/2026-10-11-restore-news-dedup-admission-order.md)。
- [2026-10-11-restore-tidy-capped-list-retention-guard](../../tasks/open/2026-10-11-restore-tidy-capped-list-retention-guard.md)。
- [2026-10-11-reconcile-legacy-host-redeploy-hardening](../../tasks/open/2026-10-11-reconcile-legacy-host-redeploy-hardening.md)。
- [2026-10-11-restore-agent-community-sweeper-services](../../tasks/open/2026-10-11-restore-agent-community-sweeper-services.md)。
- [2026-10-11-preserve-translator-critique-and-final-when](../../tasks/open/2026-10-11-preserve-translator-critique-and-final-when.md)。
- [2026-10-11-stalled-production-video-completion](../../tasks/open/2026-10-11-stalled-production-video-completion.md)。
- [2026-10-11-make-durable-polling-deadline-regression-deterministic](../../tasks/open/2026-10-11-make-durable-polling-deadline-regression-deterministic.md)。
- [2026-10-11-retain-existing-guide-packs-in-imported](../../tasks/open/2026-10-11-retain-existing-guide-packs-in-imported.md)。
- [2026-10-11-use-normal-caption-warnings-and-local](../../tasks/open/2026-10-11-use-normal-caption-warnings-and-local.md)。
- [2026-10-11-video-stage-receipt-site-identity](../../tasks/open/2026-10-11-video-stage-receipt-site-identity.md)。
- [2026-10-11-vps-uploader-initialization-rejects-numeric-install](../../tasks/open/2026-10-11-vps-uploader-initialization-rejects-numeric-install.md)。
- [2026-10-11-a-four-line-quote-card-loses](../../tasks/open/2026-10-11-a-four-line-quote-card-loses.md)。
- [2026-10-11-a-slides-storyboard-whose-pictures-all](../../tasks/open/2026-10-11-a-slides-storyboard-whose-pictures-all.md)。
- [2026-10-11-shot-prompts-put-the-look-first](../../tasks/open/2026-10-11-shot-prompts-put-the-look-first.md)。
- [2026-10-11-integrate-retained-video-source-fixes](../../tasks/open/2026-10-11-integrate-retained-video-source-fixes.md)。

附帶回應站主C:容量排行：59個已登記worktrees，成功讀取邏輯檔案44.47GiB；6個共用Git目錄3.61GiB另列。跳過16reparse項目，OneDrive3個快取folder拒讀；不是NTFS allocated bytes，沒有全C掃描或刪除工作目錄。報表與JSON在本輪scratch `branch-space-ranking.*`；獨立覆核名次/總量/分層通過。

本機audit/cleanup已完成；共享任務與本完成票保存於既有draft [PR1450](https://github.com/x812033727/travel_scanner/pull/1450)，尚未合併。完整197結果、64判定、42執行/還原、工作目錄readback与13份外部空間清理收據的保全manifest均在本輪scratch。`check:tasks`與`git diff --check`通過，最終更新readback保存於delivery.json。
