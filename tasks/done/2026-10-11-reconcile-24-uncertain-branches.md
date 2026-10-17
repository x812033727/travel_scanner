---
id: 2026-10-11-reconcile-24-uncertain-branches
title: Reconcile the 24 uncertain historical branches and clean completed refs
status: done
priority: P2
area: meta
owner: codex-gpt6-uncertain-followup
claimed_at: 2026-10-11T13:33:52Z
created_at: 2026-10-11T13:33:49Z
completed_at: 2026-10-11T13:46:58Z
branch: codex/historical-branches-cleanup-20261011
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-24-uncertain-branches.md
  - tasks/done/2026-10-11-reconcile-24-uncertain-branches.md
  - tasks/open/2026-10-11-retained-historical-branches.md
  - tasks/open/2026-10-11-reconcile-hanoi-localization.md
  - tasks/open/2026-10-11-reconcile-nami-seoul-localization.md
  - tasks/open/2026-10-11-restore-frontend-flow-polish.md
  - tasks/open/2026-10-11-reconcile-retained-catalog-proof.md
  - tasks/open/2026-10-11-reconcile-reservation-review-residuals.md
  - tasks/open/2026-10-11-preserve-country-foods-formatting.md
---

## Why

站主要求繼續核對前次清理後的 24 個待核對分支。完成且沒有未提交修改的分支應備份後清理；未完成內容保留並補入待辦索引。

## Done when

24 個分支都有具體內容、PR、主幹歷史與任務證據。已完成且可清理的 ref 有完整備份與獨立還原證據；其餘分支有明確下一步，既有修改與認領完整保留。

## Steps

- [x] 固定 24 個原始待核對候選，更新兩 clone 的主幹與 all-state PR snapshot。
- [x] 逐一對照獨有 commit/patch、取代 PR、語系／產品版本、完整收據與任務身份。
- [x] 覆核未提交修改與使用狀態，核准可清理清單。
- [x] 備份、獨立還原驗證並比對預期 HEAD 後清理完成 ref。
- [x] 更新待辦索引與可搜尋報告、驗證完整數量，準備更新現有草稿 PR #1450 的任務檔案。

## Verification

- 每個原始候選都出現在本次 audit 與最終決策。
- 被刪 ref 不存在，保留 ref 與未提交修改仍存在。
- 任務檢查及 git diff --check。

## Notes

- 證據與收據：C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/。
- 凍結主幹：73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b；24 個候選 HEAD 相對前次未變。
- batch011-korea 與 country-foods-map-links 各有 17 個未提交路徑，完整保留。
- 只處理這 24 個候選與本票 scope；不改其他模型的認領或遠端分支。

## Completion record

24 個原候選全部完成深核對：17 個完成（8 個內容整合完成、9 個操作／替代版本完成需保存原完整 HEAD）已清理；7 個實際未完成保留。Codex 本輪刪除14、Claude3；原始197總計刪除126（Codex111、Claude15）、保留71（Codex62、Claude9）。原來其他64個待辦區塊逐字保留，不擴大本輪處置範圍。

刪除前重新核對 HEAD、worktree 與 open PR，保存完整 bundle 並在獨立空白 bare repository 逐 HEAD fetch/readback。每次使用 git update-ref 預期 HEAD 比對，執行後 show-ref --quiet 確認不存在。另對原始197候選逐 ref核對現在存在／不存在狀態。沒有清理工作目錄或 outside-Git素材、改遠端舊分支、接管其他任務或執行正式站／付費操作。

- 本輪備份：`C:\Users\x8120\.codex\scratch\uncertain-branches-followup-20261011\completed-codex.bundle`；14 heads；SHA-256 `5b58f4e1673c6a7064a8916cb123d950cb733a4e635fb1a43b1d4ed13f427a39`；獨立還原與事後雜湊驗證通過。
- 本輪備份：`C:\Users\x8120\.codex\scratch\uncertain-branches-followup-20261011\completed-claude.bundle`；3 heads；SHA-256 `a29f0d7f00f5ddbe1967d591e7f2195c531b99075c117a6c0a76c72db1f2568e`；獨立還原與事後雜湊驗證通過。

3 個使用中的 worktree 仍在原 branch；Batch005 clean0、Batch011 dirty17、country foods dirty17。後兩者共34個路徑的 git status、內容 SHA-256、bytes與分支均對照 before快照確認未變。

7 個保留分支已連至現有／新 open票，未認領或釋出原作者工作。新增6票均 open、owner空白：

- [2026-10-11-reconcile-hanoi-localization](../../tasks/open/2026-10-11-reconcile-hanoi-localization.md)：`codex/article-localization-batch-006`。
- [2026-10-11-reconcile-nami-seoul-localization](../../tasks/open/2026-10-11-reconcile-nami-seoul-localization.md)：`codex/article-localization-batch-011-korea`。
- [2026-10-11-restore-frontend-flow-polish](../../tasks/open/2026-10-11-restore-frontend-flow-polish.md)：`codex/frontend-flow-release-record-a899437a`。
- [2026-10-11-reconcile-retained-catalog-proof](../../tasks/open/2026-10-11-reconcile-retained-catalog-proof.md)：`codex/content-review-resolution`。
- [2026-10-11-reconcile-reservation-review-residuals](../../tasks/open/2026-10-11-reconcile-reservation-review-residuals.md)：`codex/food-reservation-platforms`。
- [2026-10-11-preserve-country-foods-formatting](../../tasks/open/2026-10-11-preserve-country-foods-formatting.md)：`codex/country-foods-map-links`。

Batch005 沿用現有 main open `2026-10-06-batch-005-nikko-kyoto-translations-refresh`。各票區分歷史cohort、當前未核對、作者／審稿／發布，排除已完成Jeju、KL/Singapore、Escape #493、#408全目錄訂位查核等舊項。

可搜尋報告：`C:/Users/x8120/.codex/scratch/historical-cleanup-20261011/cleanup-report.html` 已更新197項總清單；本輪24項資料、執行收據及工作目錄保存證據分別為新scratch的 `reviewed-audit.json`、`cleanup-receipt.json`、`post-cleanup-verification.json`。既有草稿 [PR #1450](https://github.com/x812033727/travel_scanner/pull/1450)承載共享任務檔；本次cleanup本機操作已完成，沒有宣稱草稿PR已合併或其他工作已驗收。

## 24 branch decisions

以下17個 unused ref 已完整備份、独立還原驗證後刪除；scope外的未完成任務維持原狀。整合完成與收據／取代版本封存依據皆詳見 `reviewed-audit.json`；後者保留原始草稿與操作證據，不把被取代的bytes聲稱成逐字merged。

- `codex/article-localization-030-pair-b` — 內容整合完成；HEAD `d0ec33cc7bfe44ffd6ba61bda4e8eb268a506241`；相關PR [#859](https://github.com/x812033727/travel_scanner/pull/859), [#855](https://github.com/x812033727/travel_scanner/pull/855), [#874](https://github.com/x812033727/travel_scanner/pull/874), [#877](https://github.com/x812033727/travel_scanner/pull/877)。
- `codex/article-localization-037-social-a` — 內容整合完成；HEAD `893ff4adaa862d634b74ea746209ad53f4b089c5`；相關PR [#911](https://github.com/x812033727/travel_scanner/pull/911), [#932](https://github.com/x812033727/travel_scanner/pull/932), [#1104](https://github.com/x812033727/travel_scanner/pull/1104)。
- `codex/article-localization-batch028-release-prep` — 操作完成／取代版本封存；HEAD `bdd08fd7c92e89c161840e7d478c119f2a4ef3b3`；相關PR [#863](https://github.com/x812033727/travel_scanner/pull/863), [#869](https://github.com/x812033727/travel_scanner/pull/869), [#872](https://github.com/x812033727/travel_scanner/pull/872)。
- `codex/batch029-release-prep` — 操作完成／取代版本封存；HEAD `6bb1d6c701819b5fbd56ca8a1362ede6b7843602`；相關PR [#857](https://github.com/x812033727/travel_scanner/pull/857), [#873](https://github.com/x812033727/travel_scanner/pull/873)。
- `codex/complete-food-guide-review` — 操作完成／取代版本封存；HEAD `20efde68f269999fc1fd60422c76fecdf5d62ae0`；依獨立操作manifest／postflight與done收據核對。
- `codex/food-and-hotspot-guide-review` — 操作完成／取代版本封存；HEAD `7d092dd3c068037bb56b3666a52d32c57516a235`；依獨立操作manifest／postflight與done收據核對。
- `codex/food-reservation-data-followup` — 操作完成／取代版本封存；HEAD `c7e0e612e4cc35c31181b6a7af8ccf039ff05ea4`；相關PR [#392](https://github.com/x812033727/travel_scanner/pull/392), [#408](https://github.com/x812033727/travel_scanner/pull/408), [#397](https://github.com/x812033727/travel_scanner/pull/397), [#428](https://github.com/x812033727/travel_scanner/pull/428), [#434](https://github.com/x812033727/travel_scanner/pull/434)。
- `codex/gemini-original-snapshot` — 操作完成／取代版本封存；HEAD `90bc53f52d8944466ace02b2d18414fa1581c804`；相關PR [#490](https://github.com/x812033727/travel_scanner/pull/490), [#492](https://github.com/x812033727/travel_scanner/pull/492)。
- `codex/pr377-review-fixes-20260909` — 內容整合完成；HEAD `4b05afc47a5424ddfd0db057b1746b7af9a08f08`；相關PR [#377](https://github.com/x812033727/travel_scanner/pull/377)。
- `codex/pr897-story-conflict` — 內容整合完成；HEAD `5a759a5b24aed881a898d71bf14c7ed97358d59f`；相關PR [#897](https://github.com/x812033727/travel_scanner/pull/897), [#1413](https://github.com/x812033727/travel_scanner/pull/1413), [#909](https://github.com/x812033727/travel_scanner/pull/909)。
- `codex/pr909-source-independence` — 內容整合完成；HEAD `8419f131694493ed9a2517be629dc32df092e034`；相關PR [#909](https://github.com/x812033727/travel_scanner/pull/909), [#1382](https://github.com/x812033727/travel_scanner/pull/1382)。
- `codex/ten-drama-backend-sync-20261002` — 內容整合完成；HEAD `ab6192ef4ba2f08e8da96f0064a593c3d49feab7`；相關PR [#1122](https://github.com/x812033727/travel_scanner/pull/1122), [#1124](https://github.com/x812033727/travel_scanner/pull/1124), [#1125](https://github.com/x812033727/travel_scanner/pull/1125)。
- `codex/ten-drama-production-readiness-20261001` — 內容整合完成；HEAD `371f27d687ac8b8f7f140f444484eaa3abb57dc1`；相關PR [#1094](https://github.com/x812033727/travel_scanner/pull/1094), [#1122](https://github.com/x812033727/travel_scanner/pull/1122)。
- `codex/youtube-vps-web-settings-20260930` — 內容整合完成；HEAD `005a6e9e4e09a602873b54f9e1c7d1c2f4749910`；相關PR [#1046](https://github.com/x812033727/travel_scanner/pull/1046)。
- `claude/continue-task-ad1ac7` — 操作完成／取代版本封存；HEAD `1381413254878c79eb1090fe2ea62d996a6f1dff`；相關PR [#1213](https://github.com/x812033727/travel_scanner/pull/1213), [#1276](https://github.com/x812033727/travel_scanner/pull/1276)。
- `claude/video-dubs-worker` — 操作完成／取代版本封存；HEAD `841cb719be8a0a3295bd73b46a5a2d2c073f21eb`；相關PR [#834](https://github.com/x812033727/travel_scanner/pull/834), [#870](https://github.com/x812033727/travel_scanner/pull/870), [#983](https://github.com/x812033727/travel_scanner/pull/983), [#839](https://github.com/x812033727/travel_scanner/pull/839)。
- `fix/food-seed-test-drift` — 操作完成／取代版本封存；HEAD `a103fb3ae11dce9138c76016b7b852c2618f6bef`；相關PR [#171](https://github.com/x812033727/travel_scanner/pull/171), [#172](https://github.com/x812033727/travel_scanner/pull/172)。

以下7個保留並以現有／新待辦續作：

- `codex/article-localization-batch-005`；HEAD `40d482aa1d56fa19a16df2bf56e2bc952ed142bf`；[2026-10-06-batch-005-nikko-kyoto-translations-refresh](../../tasks/open/2026-10-06-batch-005-nikko-kyoto-translations-refresh.md), [2026-10-06-publish-onsen-kyoto-bus-zh-tw](../../tasks/open/2026-10-06-publish-onsen-kyoto-bus-zh-tw.md)。
- `codex/article-localization-batch-006`；HEAD `56d98e4decce9f760179665119c2821c350b7613`；[2026-10-11-reconcile-hanoi-localization](../../tasks/open/2026-10-11-reconcile-hanoi-localization.md)。
- `codex/article-localization-batch-011-korea`；HEAD `1fbd57ac8845c8d4f465be7a1914669386f26ee7`；[2026-10-11-reconcile-nami-seoul-localization](../../tasks/open/2026-10-11-reconcile-nami-seoul-localization.md)。
- `codex/frontend-flow-release-record-a899437a`；HEAD `2cfb1acab8f4f9bad565b54fa194bd5a3cbd90d4`；[2026-10-11-restore-frontend-flow-polish](../../tasks/open/2026-10-11-restore-frontend-flow-polish.md)。
- `codex/content-review-resolution`；HEAD `9cd24e2be787925be58eb55418c4d9b6333fa049`；[2026-10-11-reconcile-retained-catalog-proof](../../tasks/open/2026-10-11-reconcile-retained-catalog-proof.md)。
- `codex/country-foods-map-links`；HEAD `a8736021c98f38a71e5f57555766d4cb86cc893e`；[2026-10-11-preserve-country-foods-formatting](../../tasks/open/2026-10-11-preserve-country-foods-formatting.md)。
- `codex/food-reservation-platforms`；HEAD `59f4b994533554509ec2dd90d0f7139acf8030a9`；[2026-10-11-reconcile-reservation-review-residuals](../../tasks/open/2026-10-11-reconcile-reservation-review-residuals.md)。

另外保留原本主幹的 Wave3 發布、VPS live驗收、偶的江湖pilot／路線決策以及實際音軌／影片製作關卡；它們不是本輪舊分支完成所涵蓋的交付。只有本機cleanup對帳票結案，沒有關閉這些原票。
