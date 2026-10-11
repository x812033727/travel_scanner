# C: Codex 工作目錄核對與待辦（2026-10-11）

> 本文保留初次 59 筆／36 個 Codex 目錄的歷史盤點。最新收尾、已刪項目與後續保留理由，以 [本輪收尾紀錄](worktree-closeout-20261011.md) 為準；下列 0 刪除／36 保留是初次盤點結果。

最新指示只處理 Codex：原 59 筆清單中本輪涵蓋 36 個 Codex 工作目錄；18 個 Claude 與 5 個其他專案不在清理範圍。

結果：**刪除 0，保留 36，回收 0 bytes**。沒有目錄同時符合已完成、無未提交修改及不再使用。六個共用 Git 儲存庫亦未刪除。

以下按主要保留原因互斥分類：

| 主要原因 | 數量 |
|---|---:|
| 未提交修改 | 22 |
| 未完成交付／續作 | 4 |
| 未合併 PR | 6 |
| 保護／使用中 | 3 |
| 主倉庫 | 1 |

未提交修改、已合併產品、內容已發布、PR 已合併與整個目錄已完成分開記錄。Claude 的《偶的江湖》、Codex 1b93 前期交接與外部製作素材均保護。沒有移動他人的任務、釋出認領、變更 production 或付費工作。

共享後續票：`tasks/open/2026-10-11-follow-up-retained-c-drive-worktrees.md`（open，未認領）。

核對證據：`C:/Users/x8120/.codex/scratch/worktree59-cleanup-20261011/`，互動報告 `codex-worktree-report.html`，完整清單 `codex-worktree-report.json`。

容量沿用 2026-10-11 22:04 台北的檔案邏輯長度快照；本輪重新核對 Git、PR、工作用途及檔案保存，未重測 NTFS 配置容量。

## 1. codex/codex-practical-series-20261011

- 工作目錄：`C:/Users/x8120/.codex/worktrees/afd6/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：1；前次容量：1.284 GiB。
- HEAD：`10cc468b71ba57fc823a2df498cc9bf6e0dff707`
- 原因：#1429 OPEN，PRhead與snapshot10cc468b不同；dirty1 environment.toml；Codex實作系列原owner對話未封存，包含source/策畫/價值/視覺規格的3個獨有commit。

具體待辦：

- [ ] 保存目前HEAD/environment及規劃素材；對照#1429較新head與owner規劃稿，切勿reset/刪除以追遠端。
- [ ] 繼續沿系列原票確認可跟做材料、示範成效與review/production門檻，不能把策劃commit當成影片交付。

PR 證據：[1429](https://github.com/x812033727/travel_scanner/pull/1429) OPEN。

沿用任務：`2026-10-10-bind-final-codex-practical-packages-and`、`2026-10-10-codex-practical-01-production`、`2026-10-10-codex-practical-02-production`、`2026-10-10-codex-practical-03-production`、`2026-10-10-codex-practical-04-production`、`2026-10-10-codex-practical-05-production`、`2026-10-10-codex-practical-06-production`、`2026-10-10-codex-practical-07-production`、`2026-10-10-codex-practical-08-production`、`2026-10-10-codex-practical-09-production`、`2026-10-10-codex-practical-10-production`、`2026-10-10-codex-practical-11-production`、`2026-10-10-codex-practical-12-production`、`2026-10-10-codex-practical-13-production`、`2026-10-10-codex-practical-14-production`、`2026-10-10-codex-practical-15-production`、`2026-10-10-codex-practical-16-production`、`2026-10-10-codex-practical-17-production`、`2026-10-10-codex-practical-18-production`、`2026-10-10-codex-practical-curriculum`、`2026-10-10-codex-practical-final-test-locator`、`2026-10-10-codex-practical-material-guide-paths`、`2026-10-10-codex-practical-public-host-locators`、`2026-10-10-codex-practical-zip-root-followalong`、`2026-10-10-windows-automation-fixture-import`、`2026-10-10-windows-ffmpeg-empty-reference-range`、`2026-10-11-codex-practical-03-05-recording-inputs`、`2026-10-11-correct-codex-03-05-brief-source`。

證據：
- #1429 OPEN，PRhead與snapshot10cc468b不同；dirty1 environment.toml；Codex實作系列原owner對話未封存，包含source/策畫/價值/視覺規格的3個獨有commit。

## 2. codex/article-locales-release-20261007

- 工作目錄：`C:/Users/x8120/.codex/worktrees/4e16/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：2；前次容量：1.263 GiB。
- HEAD：`08a280298f41670476f71cf3e2ebf87f663dfd67`
- 原因：32篇已發布的收據與四張release結案記錄仍在OPEN PR #1373；checkout另有2個未追蹤檔，整體多語補齊工作仍未完成。

具體待辦：

- [ ] 保留release收據、4張done票及原始staging；由原owner核對#1373當前CI/review並完成窄收據整合，不重譯或重發已驗證32篇。
- [ ] 將news-decrypt-topic-disclaimer-loop原稿與共享新聞票對帳，保存environment設定；更廣的article-missing-locales-completion由其既有owner續作。

PR 證據：[1373](https://github.com/x812033727/travel_scanner/pull/1373) OPEN。

沿用任務：`2026-10-07-release-business-analysis-missing-locales`、`2026-10-07-release-localized-travel-life-wave-20261007`、`2026-10-07-release-reviewed-japan-refund-source-and`、`2026-10-07-release-wave3-travel-and-life-article`、`2026-10-07-article-missing-locales-completion`。

證據：
- exact HEAD 08a280298f41670476f71cf3e2ebf87f663dfd67; mainAncestor=false; main...HEAD behind/ahead=63/2; HEAD未較排行快照變動。
- PR #1373 OPEN，headRefOid精確等於08a280298f41670476f71cf3e2ebf87f663dfd67；main仍缺本支9個release/coverage文件版本，不能把已發布收據尚未整合說成需要重發32篇。
- 兩個未追蹤路徑是.codex/environments/environment.toml與news-decrypt-topic-disclaimer-loop任務原稿；ignored含localization-staging的baseline、bundle、jobs與工作資料，需保存。

## 3. codex/stalled-videos-completion-20261008

- 工作目錄：`C:/Users/x8120/.codex/worktrees/2a98/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：13；前次容量：1.262 GiB。
- HEAD：`b9940f18c1dfed8b493ceb9778df4c845728d4e2`
- 原因：dirty13包括三張open票刪除＋對應done未追蹤、最新recovery document與多張補充未共享原稿；commit HEAD b9940f18不是main祖先。

具體待辦：

- [ ] 保全13dirty與原stage/檔案hash；對照stalled-video-reviewed-fixes的#1387，已替代source不要重播，缺少共享票先查該PR是否包含。
- [ ] 沿原owner/固定影片cohort核對caption粒子、true-peak、locale決定、guide-pack retention及receipt-site identity；保留STOP和uncertain paid results，交付/發布需各自收據。

沿用任務：`2026-10-08-make-durable-polling-deadline-regression-deterministic`、`2026-10-08-retain-existing-guide-packs-in-imported`、`2026-10-08-stalled-production-video-completion`、`2026-10-08-use-normal-caption-warnings-and-local`、`2026-10-08-video-audio-closing-particle-boundaries`、`2026-10-08-video-branding-true-peak`、`2026-10-08-video-qa-undecided-languages`、`2026-10-09-video-stage-receipt-site-identity`。

證據：
- dirty13包括三張open票刪除＋對應done未追蹤、最新recovery document與多張補充未共享原稿；commit HEAD b9940f18不是main祖先。
- 原生產線續作、retained provider/STOP/review/lease需依主owner收據；同source的reviewed-fixes successor仍有#1387 OPEN，原本地done搬檔不能被當成merged。

## 4. codex/news-recovery-followup-20261011

- 工作目錄：`C:/Users/x8120/.codex/worktrees/news-held-bundle-ingestion/travel_scanㄐ`
- 決定：保留；主要原因：未完成交付／續作；未提交路徑：0；前次容量：1.100 GiB。
- HEAD：`c3d7a76961088bbcbf54e1bf0a7fbc5648a017d4`
- 原因：PR #1444完整合併，但原新聞聊天仍用此worktree接續208篇恢復流程，ownership未釋放。

具體待辦：

- [ ] 保留聊天附件與worktree；由原owner依news-held-cohort-recovery的固定208 IDs、sealed ledger與原外部workspace續作。
- [ ] 追Sanders/Glasses historical-claim修正、rotating widgets、upstreamHTTP、AI-agent/Verge held stories等既有窄票；不重開已done navigation/i18n節點，不把dated133 published census當本輪正式站現況。

PR 證據：[1444](https://github.com/x812033727/travel_scanner/pull/1444) MERGED。

沿用任務：`2026-10-10-add-audited-repair-for-legacy-navigation`、`2026-10-11-localize-audited-navigation-repair-errors-required`、`2026-10-10-news-held-cohort-recovery`、`2026-10-11-add-audited-correction-for-obsolete-held`、`2026-10-11-exclude-rotating-source-widgets-from-news`、`2026-10-11-expose-upstream-http-status-and-recover`、`2026-10-11-recover-ai-agent-control-story-after`、`2026-10-11-recover-two-verge-held-stories-after`。

證據：
- exact HEAD c3d7a76961088bbcbf54e1bf0a7fbc5648a017d4; mainAncestor=false; main...HEAD behind/ahead=5/4; HEAD未較排行快照變動。
- PR #1444 MERGED且exact HEAD；mergeCommit 0c93720e684b4c3995b16f7c2e859fe2bc06ec9f是frozen main祖先，5個變動的程式/測試/receipt路徑目前與main精確同blob。
- navigation-repair與55條錯誤多語文案兩張窄票main已done；canonical news-held-cohort-recovery仍in-progress，owner codex-news-recovery-6f71。
- root讀取聊天01a1233b…確認為非archived附件且長turn尚無收尾final；目前0 dirty，但clean不代表owner已釋放。ignored僅venv、Python caches與generated BOARD。

## 5. codex/news-recovery-20261010

- 工作目錄：`C:/Users/x8120/.codex/worktrees/6f71/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：13；前次容量：1.099 GiB。
- HEAD：`1b7be83e6cc65a308e2c21b785c7e37c8ac966f7`
- 原因：原程式修復已合併，原208 cohort仍未收尾，且6f71有13個未提交路徑。

具體待辦：

- [ ] 保存13檔diff與所有saved bundles/receipts；把舊recovery checkpoint與main #1444後續receipt逐段對帳，保留日期及source/history hashes。
- [ ] 沿既有208-cohort操作票續處理未完source/editorial/redraft/failure/duplicate gates；scope外video-held-retry-status原稿移交原影片owner對帳，不擴大新聞執行scope。

PR 證據：[1411](https://github.com/x812033727/travel_scanner/pull/1411) MERGED。

沿用任務：`2026-10-10-exclude-system-topic-navigation-from-news`、`2026-10-10-news-disclaimer-correction-loop`、`2026-10-10-add-audited-source-extension-for-held`、`2026-10-10-distinguish-reported-and-negated-trading-verbs`、`2026-10-10-news-held-cohort-recovery`、`2026-10-05-video-held-retry-status`、`2026-10-06-news-judge-translations-only-rerun`、`2026-10-07-resolve-current-news-review-and-redraft`、`2026-10-10-add-audited-held-news-bundle-ingestion`、`2026-10-10-add-audited-held-news-category-correction`、`2026-10-10-add-audited-repair-for-legacy-navigation`、`2026-10-10-correct-published-bitmine-sole-outlet-attribution`、`2026-10-10-preserve-and-recover-translated-news-before`、`2026-10-10-track-ledger-duplicate-coverage-gap`、`2026-10-11-add-audited-minor-corrections-for-published`、`2026-10-11-show-final-judge-holds-on-news`、`2026-10-11-translate-held-news-ingestion-error-messages`。

證據：
- exact HEAD 1b7be83e6cc65a308e2c21b785c7e37c8ac966f7; mainAncestor=false; main...HEAD behind/ahead=38/6; HEAD未較排行快照變動。
- #1411 MERGED head50a2c502…與現在HEAD不同，但五個程式/測試路徑目前同main；其merge commit仍main祖先。HEAD新增的FAQ/恢復receipt及working notes需與後續#1444對帳。
- canonical recovery票與6f71 owner仍保留；13 dirty包括2 tracked docs/task修改及11 untracked tasks/environment。其中bundle-ingestion/error-copy/navigation已有done successor，不需重做。

## 6. codex/pr921-tidy-metadata-current

- 工作目錄：`C:/Users/x8120/.codex/worktrees/pr-merge-watch/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：17；前次容量：0.897 GiB。
- HEAD：`a89cfa65ef518198b4b6f641148519431df4f6ae`
- 原因：clean不能成立：dirty17，含Shorts來源14路徑、done rename/原task及未追蹤pr906 integration；HEADa89cfa65的missing-site-entry tidy guard未入main。

具體待辦：

- [ ] 保全17 dirty/index簽名及原草稿，不reset/abort/replay舊PR906衝突。
- [ ] 連回root #1450恢复的單一capped-video-list素材保留票，僅整合missing entry hold與相容回歸；不執行正式tidy或移除media。

沿用任務：`2026-09-28-guard-automatic-shorts-sync-against-changed`、`2026-09-28-pr906-main-integration`、`2026-09-28-pr921-tidy-metadata-guard`、`2026-09-28-video-shorts-youtube-auto`、`2026-09-28-video-story-tidy-finished`、`2026-09-28-video-tidied-late-languages`。

證據：
- clean不能成立：dirty17，含Shorts來源14路徑、done rename/原task及未追蹤pr906 integration；HEADa89cfa65的missing-site-entry tidy guard未入main。
- 先前retained64 deep audit已確認：current main latest200列表漏列仍可使用舊local approval；兩PR921 branch同缺口僅共用一張恢復追蹤，#916/#925已承接其他舊source。

## 7. codex/article-locales-wave6-release-20261010

- 工作目錄：`C:/Users/x8120/.codex/worktrees/article-locales-wave5-20261008/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：2；前次容量：0.893 GiB。
- HEAD：`d4f074c4da1473fac04b46aa9e70d7a733bcc560`
- 原因：17篇/68語系內容PR #1409已進main，但這個release checkout仍有未提交author票搬移；正式發布票與驗收證據未完成。

具體待辦：

- [ ] 保存2檔任務搬移與wave6全部baseline/jobs/artifacts，核對author票CI與#1409後再完成窄記帳。
- [ ] 沿既有release-localized-web-design-wave6票核對實際發布證據；若尚無，依原owner的授權/gates續作。不得由內容已merge推論68語系已正式發布。

沿用任務：`2026-10-09-localize-reviewed-web-design-wave6`、`2026-10-09-release-localized-web-design-wave6`。

證據：
- exact HEAD d4f074c4da1473fac04b46aa9e70d7a733bcc560; mainAncestor=true; main...HEAD behind/ahead=39/0; HEAD未較排行快照變動。
- HEAD d4f074c4da1473fac04b46aa9e70d7a733bcc560為#1409 squash merge commit且main祖先，unique=0；17篇authoring內容不需重做。
- main tasks/open/2026-10-09-release-localized-web-design-wave6.md仍open，明確要求fresh cohort authorization、deploy、backup/restore、68 target及13 source corrections發布、public QA與ledger CAS。
- dirty2是author票open刪除與done新檔；本機done正文仍留歷史CI未勾，需用#1409已合併事實對帳。ignored .codex/l10n含wave5/wave6 baseline、jobs、bundle與install證據。

## 8. codex/article-locales-wave4-release-20261008

- 工作目錄：`C:/Users/x8120/.codex/worktrees/article-locales-wave4/travel_scanㄐ`
- 決定：保留；主要原因：未合併 PR；未提交路徑：0；前次容量：0.858 GiB。
- HEAD：`79758f18cf39652a9f4d08dd764f0242f0735ece`
- 原因：13篇/52目標語系實際發布收據已有，但收據PR #1401仍OPEN，需完成交接整合。

具體待辦：

- [ ] 保留clean checkout、ignored wave4-review staging及外部raw receipts；由原owner完成#1401當前CI/review與窄收據整合、兩張release票記帳。
- [ ] 完整留存既有public QA和original failure記錄；不重發13篇、不以更廣805篇剩餘工作阻止窄交付驗收。

PR 證據：[1401](https://github.com/x812033727/travel_scanner/pull/1401) OPEN。

沿用任務：`2026-10-07-release-independently-reviewed-wave4-web-and`、`2026-10-07-release-reviewed-japan-entry-article-source`。

證據：
- exact HEAD 79758f18cf39652a9f4d08dd764f0242f0735ece; mainAncestor=false; main...HEAD behind/ahead=57/1; HEAD未較排行快照變動。
- #1401 OPEN且headRefOid精確匹配79758f18cf39652a9f4d08dd764f0242f0735ece；branch clean0但4個release README/evidence路徑尚未進main。
- 完整README含Japan zhTW v8、12篇life五語、原素材guards、independent postpublication preservation與57篇/228語系ledger；歷史805缺篇/3220語系為2026-10-08觀測，不是本輪production census。
- 9個每語系related-target findings已有未公開語系對應，frontend顯示純文字；全域missing-locales/link backlog是其他票scope，不能據此要求重做這13篇發布。

## 9. codex/video-approved-final-languages-20261004

- 工作目錄：`C:/Users/x8120/.codex/worktrees/e82d/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：13；前次容量：0.742 GiB。
- HEAD：`7132cd7d5e6bb4f85c7bb9b2627991ea83aa783c`
- 原因：#1210 MERGED但local7132cd7d不等PRhead，仍2 unique commits、13dirty；main bounded-video-media-followthrough in-progress、imported languages/renewed-finals open。

具體待辦：

- [ ] 保全13dirty並逐source patch對#1210/new main及本地收據，不重播已完成guard。
- [ ] 在已有bounded-followthrough/imported-languages/renewed-finals票分別確認原生review、uncertain request、owner預覽/上架gate；不得按本地approved或exit0直接結案。

PR 證據：[1210](https://github.com/x812033727/travel_scanner/pull/1210) MERGED。

沿用任務：`2026-09-29-resume-imported-long-video-languages`、`2026-09-29-video-language-progress-state`、`2026-10-01-hand-off-owner-approved-renewed-finals`、`2026-10-04-audit-llm-language-resubmission-request`、`2026-10-04-bounded-video-media-followthrough`、`2026-10-04-minimax-image-prompt-preflight`、`2026-10-04-native-language-durable-units-and-progress`、`2026-10-04-native-video-project-stop-and-producer-exclusion`、`2026-10-04-prepare-grok-language-source-resubmission`、`2026-10-04-preserve-normal-speech-results-before-retrying`、`2026-10-04-repair-three-fit-held-japanese-lines`、`2026-10-04-resubmit-registrar-language-source-manifest`、`2026-10-04-resubmit-waf-language-source-manifest`、`2026-10-04-retain-video-policy-holds-without-new`。

證據：
- #1210 MERGED但local7132cd7d不等PRhead，仍2 unique commits、13dirty；main bounded-video-media-followthrough in-progress、imported languages/renewed-finals open。
- MiniMax prompt-preflight/preserve speech等source guard主票done，但本目錄還保存語言/正常模型答卷/媒體恢復工作；原owner未封存。

## 10. codex/news-backlog-review-20261007

- 工作目錄：`C:/Users/x8120/.codex/worktrees/fe41/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：8；前次容量：0.739 GiB。
- HEAD：`bcc073b8db64c5b8955c4b49ddc2aabd7fe83e7b`
- 原因：原520候選隊列尚未完成，且checkout有8個未提交路徑；#1371窄程式合併不等於整個新聞流程完成。

具體待辦：

- [ ] 保留8檔diff及520-ID baseline/driver receipts，將新source-attribution、deterministic selection、navigation/mutable evidence、deployment race、fingerprint票原稿與main successor逐項對帳。
- [ ] 原owner接續520固定cohort與technical holds，使用persisted state驗證；不重做已merged disclaimer節點、不釋放claim或重播unknown provider requests。

PR 證據：[1371](https://github.com/x812033727/travel_scanner/pull/1371) MERGED。

沿用任務：`2026-10-07-recognize-translated-news-disclaimer-notices-and`、`2026-10-07-resolve-current-news-review-and-redraft`。

證據：
- exact HEAD bcc073b8db64c5b8955c4b49ddc2aabd7fe83e7b; mainAncestor=false; main...HEAD behind/ahead=64/2; HEAD未較排行快照變動。
- #1371 MERGED exact HEAD bcc073b8db64c5b8955c4b49ddc2aabd7fe83e7b；mergeCommit為main祖先，translated-disclaimer-recognition票main done。
- canonical resolve-current-news-review-and-redraft仍in-progress，owner codex-news-backlog-review；正文要求固定520 IDs最終outcome對帳、technical holds/failures與bounded batches。511 remains為當時checkpoint，沒有本轮查production。
- dirty8含docs與原操作票修改、5個新窄票原稿及environment設定；原外部workspace是.codex/news-review/20261007-fe41。

## 11. codex/historical-branches-cleanup-20261011

- 工作目錄：`C:/Users/x8120/.codex/worktrees/historical-branch-cleanup/travel_scanㄐ`
- 決定：保留；主要原因：保護／使用中；未提交路徑：1；前次容量：0.711 GiB。
- HEAD：`4907bb8df7575938eef17419d612ae24323009e0`
- 原因：本次正在使用的審核工作目錄；PR #1450 為草稿，本輪任務與報告仍在此編輯。

具體待辦：

- [ ] 保留盤點/新票PR的工作區及原claim；不得在自己的runner裡清掉它。

PR 證據：[1450](https://github.com/x812033727/travel_scanner/pull/1450) OPEN。

沿用任務：`2026-10-11-a-four-line-quote-card-loses`、`2026-10-11-a-slides-storyboard-whose-pictures-all`、`2026-10-11-audit-clean-59-c-drive-worktrees`、`2026-10-11-historical-branch-cleanup-audit`、`2026-10-11-integrate-retained-video-source-fixes`、`2026-10-11-localize-batch003-zh-tw-diagram-helpers`、`2026-10-11-make-durable-polling-deadline-regression-deterministic`、`2026-10-11-preserve-country-foods-formatting`、`2026-10-11-preserve-translator-critique-and-final-when`、`2026-10-11-reconcile-24-uncertain-branches`、`2026-10-11-reconcile-64-retained-branches`、`2026-10-11-reconcile-hanoi-localization`、`2026-10-11-reconcile-legacy-host-redeploy-hardening`、`2026-10-11-reconcile-merchant-style-batch08-acceptance`、`2026-10-11-reconcile-nami-seoul-localization`、`2026-10-11-reconcile-reservation-review-residuals`、`2026-10-11-reconcile-retained-catalog-proof`、`2026-10-11-reconcile-wordpress-map-source-release`、`2026-10-11-reconcile-wordpress-user-roles-locales`、`2026-10-11-restore-agent-community-sweeper-services`、`2026-10-11-restore-deploy-verifier-freshness-exit`、`2026-10-11-restore-frontend-flow-polish`、`2026-10-11-restore-merchant-style-first-failure-investigation`、`2026-10-11-restore-news-dedup-admission-order`、`2026-10-11-restore-tidy-capped-list-retention-guard`、`2026-10-11-restore-transit-timing-fare-precision`、`2026-10-11-retain-existing-guide-packs-in-imported`、`2026-10-11-retained-historical-branches`、`2026-10-11-shot-prompts-put-the-look-first`、`2026-10-11-stalled-production-video-completion`、`2026-10-11-use-normal-caption-warnings-and-local`、`2026-10-11-video-held-retry-status`、`2026-10-11-video-stage-receipt-site-identity`、`2026-10-11-vps-uploader-initialization-rejects-numeric-install`。

證據：
- 本次正在使用的審核工作目錄；PR #1450 為草稿，本輪任務與報告仍在此編輯。

## 12. detached b12ae9f6d6

- 工作目錄：`C:/Users/x8120/.codex/worktrees/2792/travel_scanㄐ`
- 決定：保留；主要原因：保護／使用中；未提交路徑：1；前次容量：0.710 GiB。
- HEAD：`b12ae9f6d689b5275906899278c06f3c46ead7b9`
- 原因：本次盤點對話cwd，detached b12ae9f6為main祖先；environment.toml untracked；使用者/本次root明確保護。

具體待辦：

- [ ] 保留當前盤點工作區，不納入worktree移除。

證據：
- 本次盤點對話cwd，detached b12ae9f6為main祖先；environment.toml untracked；使用者/本次root明確保護。

## 13. codex/stalled-production-resume-20261010

- 工作目錄：`C:/Users/x8120/.codex/worktrees/3603/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：4；前次容量：0.706 GiB。
- HEAD：`1bd1d47ceab109b1425af01f1571173e95004c8e`
- 原因：HEAD1bd1d47c是fresh main祖先，沒有unique commit；但有4未追蹤路徑，包含10/10 production-resume收據與deterministic-blockers、whisper-pyav19兩張原票。

具體待辦：

- [ ] 保全4untracked檔，恢復/連結deterministic production blocker與Whisper PyAV19兼容性窄票，不能只刪已merged baseline工作區。
- [ ] 依原owner的原生production/review/STOP receipts確認哪些影片仍需階段修復，不重啟paid/生成工作。

沿用任務：`2026-10-10-resume-deterministic-video-production-blockers`、`2026-10-10-whisper-pyav19-second-opinion`。

證據：
- HEAD1bd1d47c是fresh main祖先，沒有unique commit；但有4未追蹤路徑，包含10/10 production-resume收據與deterministic-blockers、whisper-pyav19兩張原票。
- 原對話仍未封存；只有committed baseline在main，整個working tree交付未完成。

## 14. codex/ou-de-jianghu-visual-preproduction-20261008

- 工作目錄：`C:/Users/x8120/.codex/worktrees/1b93/travel_scanㄐ`
- 決定：保留；主要原因：保護／使用中；未提交路徑：3；前次容量：0.700 GiB。
- HEAD：`9607a9001aa40851dd07e4c5f4f1e6246d6568e1`
- 原因：偶的江湖全案hard-protected；本地dirty3包含visual-handoff及CLAUDE-HANDOFF-20261009，HEAD仍有10獨有commit，#1388 OPEN且PRhead較此snapshot不同。

具體待辦：

- [ ] 保留完整目錄、branch、三項dirty、outside-Git media/STOP/paid ledger；只讀對照Claude目前successor與原handoff，不接管lease、重送provider或撤銷原claim。

PR 證據：[1388](https://github.com/x812033727/travel_scanner/pull/1388) OPEN。

沿用任務：`2026-10-08-animatic-title-gap-subtitle-boundary`、`2026-10-08-integrate-external-look-import-duration-review`、`2026-10-08-ou-de-jianghu-animation-reference`、`2026-10-08-ou-de-jianghu-art-direction`、`2026-10-08-ou-de-jianghu-episode1-portraits`、`2026-10-08-ou-de-jianghu-external-look-import`、`2026-10-08-ou-de-jianghu-preflight-plan`、`2026-10-08-ou-de-jianghu-scene-prop-design`、`2026-10-08-ou-de-jianghu-supporting-looks`、`2026-10-08-ou-de-jianghu-visual-handoff`、`2026-10-08-ou-de-jianghu-visual-preproduction`、`2026-10-08-validate-windows-stock-path-and-brightness`。

證據：
- 偶的江湖全案hard-protected；本地dirty3包含visual-handoff及CLAUDE-HANDOFF-20261009，HEAD仍有10獨有commit，#1388 OPEN且PRhead較此snapshot不同。
- 預製作、已買provider request/原take、停止/Claude移交、完整影片交付是不同狀態；不能因部分art/工具local done刪除此目錄。

## 15. codex/gemini-advanced-platform

- 工作目錄：`C:/Users/x8120/.codex/worktrees/3281/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：2；前次容量：0.696 GiB。
- HEAD：`57308fe8f86149449181bc48af2346bffa4b111f`
- 原因：可見性/平台節點已完成，但這個聚合author checkout尚有2個未追蹤檔及36篇進階內容/實測交接待對帳。

具體待辦：

- [ ] 保留聚合checkout及2個untracked檔；對36篇手稿/素材/實測receipts與main及後續#947等release逐項對帳，標出確實缺真實驗收的篇目與原owner。
- [ ] 沿既有advanced author/release票補其原本要求的實測/版本凍結證據；本輪不觸發Google付費或正式站操作，也不重做已done platform/projection/UI。

PR 證據：[520](https://github.com/x812033727/travel_scanner/pull/520) MERGED。

沿用任務：`2026-09-14-claude-code-tutorial-center`、`2026-09-14-gemini-advanced-content-tooling`、`2026-09-14-gemini-advanced-curriculum`、`2026-09-14-gemini-content-compiler-lf`、`2026-09-14-gemini-advanced-api`、`2026-09-14-gemini-advanced-automation`、`2026-09-14-gemini-advanced-creative`、`2026-09-14-gemini-advanced-md`、`2026-09-14-gemini-advanced-platform`、`2026-09-14-gemini-advanced-release`、`2026-09-14-gemini-advanced-research`、`2026-09-14-gemini-advanced-visible-projection`、`2026-09-14-gemini-advanced-visible-ui`、`2026-09-14-gemini-advanced-work`、`2026-09-14-tasks-done-retains-open-copy`。

證據：
- exact HEAD 57308fe8f86149449181bc48af2346bffa4b111f; mainAncestor=false; main...HEAD behind/ahead=869/24; HEAD未較排行快照變動。
- #520 MERGED head45994ab3…與目前HEAD不同；其mergeCommit a06afe2291ff734165945d2906f4827d26d5755a為main祖先。main platform、visible-projection、visible-ui及content-tooling原票全部done；不得重開這些平台節點。
- 本支24 unique commits含六批教材、真實帳號實驗與release handoff；1550個非task變動路徑1485 current-main同blob、65已不同，需要按後續release/內容版本對帳，不能將不同blob全當未落地code。
- main advanced api/automation/creative/md/research/work/release仍open，正文區分真實Google帳號/模型/裝置結果、成本上限與本機fixture；它們是內容驗收續作，不是舊平台code未完的證据。
- dirty2為environment設定與sales-audit.xlsx.inspect.ndjson，後者是workbook檢查輸出；須保存後辨認原owner用途。

## 16. codex/stalled-video-reviewed-fixes-20261008

- 工作目錄：`C:/Users/x8120/.codex/worktrees/stalled-video-reviewed-fixes/travel_scanㄐ`
- 決定：保留；主要原因：未合併 PR；未提交路徑：0；前次容量：0.693 GiB。
- HEAD：`382f26428786500a8e59d87ed04d8ccdf5c7e300`
- 原因：clean但#1387 OPEN exactHead382f2642，25 unique commits包括Mandarin粒子、true-peak/locale、guarded recovery、完整語言/交付收據與durable task修補。

具體待辦：

- [ ] 保留工作目錄與所有25 commit/CI/source duration/production收據；沿#1387核對當前CI及獨立review。
- [ ] 僅依原owner原生route及source-bound receipts處理留下的production/metadata/journal gate；原未確認provider不得重送，package完成與public交付分開。

PR 證據：[1387](https://github.com/x812033727/travel_scanner/pull/1387) OPEN。

沿用任務：`2026-10-08-make-durable-polling-deadline-regression-deterministic`、`2026-10-08-preserve-translator-critique-and-final-when`、`2026-10-08-retain-existing-guide-packs-in-imported`、`2026-10-08-stalled-production-video-completion`、`2026-10-08-use-normal-caption-warnings-and-local`、`2026-10-08-video-audio-closing-particle-boundaries`、`2026-10-08-video-branding-true-peak`、`2026-10-08-video-qa-undecided-languages`、`2026-10-09-carry-rejected-reword-length-feedback-into`、`2026-10-09-duration-review-stalled-fixes-rebase`、`2026-10-09-recover-own-complete-speech-answers-after`、`2026-10-09-video-numeric-prefix-lexicon-validation`、`2026-10-09-video-skipped-dub-caption-timing`、`2026-10-09-video-speech-pretransport-admission`、`2026-10-09-video-stage-receipt-site-identity`、`2026-10-09-video-translator-owned-control-fields`、`2026-10-09-windows-process-birth-closure`、`2026-10-09-windows-rename-confirmed-answer-backoff`。

證據：
- clean但#1387 OPEN exactHead382f2642，25 unique commits包括Mandarin粒子、true-peak/locale、guarded recovery、完整語言/交付收據與durable task修補。
- owner是仍未封存2a98主對話，其保留recovery/paid hold與工作treeattachments；沒有merged producer證目前HEAD已完成共享整合。

## 17. codex/windows-video-validation-20261009

- 工作目錄：`C:/Users/x8120/.codex/worktrees/windows-video-validation/travel_scanㄐ`
- 決定：保留；主要原因：未合併 PR；未提交路徑：0；前次容量：0.692 GiB。
- HEAD：`b0537d31fc90de057727cc685631e2e5bcd70231`
- 原因：clean但fresh #1391 OPEN，head b0537d31精確等目前branch。原owner對話archived=1，仍不能把尚未merged的PR/11 commits當作已完成共享source。

具體待辦：

- [ ] 保留checkout與#1391 source/duration/Windows native lock收據；owner封存後由現有PR讀取CI/review確認是否可merge或有明確replacement，不能直接清工作目錄。
- [ ] fixture修正local done與剩餘native journal replacement safety分開核對；保持Unix fsync/atomicity，無證據不可採會丟receipt的Windows替換方案。

PR 證據：[1391](https://github.com/x812033727/travel_scanner/pull/1391) OPEN。

沿用任務：`2026-10-07-accept-windows-separators-in-stock-fetch`、`2026-10-07-make-project-lease-test-children-use`、`2026-10-07-preserve-speech-journal-writes-through-windows`、`2026-10-07-windows-reference-comparison-ffmpeg`、`2026-10-07-windows-video-test-imports`、`2026-10-08-windows-video-path-assertions`。

證據：
- clean但fresh #1391 OPEN，head b0537d31精確等目前branch。原owner對話archived=1，仍不能把尚未merged的PR/11 commits當作已完成共享source。
- 五個fixture/platform票local done，main仍有make-project-lease-test-children-use/windows-reference-comparison-ffmpeg/windows-video-test-imports open；另preserve-speech-journal-writes-through-windows仍local open與後續native replacement evidence。

## 18. detached c7ff1f5c59

- 工作目錄：`C:/Users/x8120/.codex/worktrees/windows-atomic-write-retry-20261008/travel_scanㄐ`
- 決定：保留；主要原因：未合併 PR；未提交路徑：0；前次容量：0.682 GiB。
- HEAD：`c7ff1f5c599d2b36684f91ad466c49baab320cd1`
- 原因：clean detached c7ff1f5c，但fresh #1379 OPEN且head精確等此detached HEAD。四unique commits是保留完整speech answers、promotion recovery、journal list consumer契約與收據。

具體待辦：

- [ ] 保留detached HEAD及該checkout，沿#1379 current-head CI/review/Windows sharing-lock+list consumer contract整合；不要當無branch可刪的孤立目錄。
- [ ] 保全原已知provider answer及recovery receipts，不重送paid speech；只有PR真正merged/被具體replacement取代且owner不再依賴時再核对清理。

PR 證據：[1379](https://github.com/x812033727/travel_scanner/pull/1379) OPEN。

沿用任務：`2026-10-07-preserve-full-speech-answers-when-windows`。

證據：
- clean detached c7ff1f5c，但fresh #1379 OPEN且head精確等此detached HEAD。四unique commits是保留完整speech answers、promotion recovery、journal list consumer契約與收據。
- 四封存子代理與一未封存23a9主owner attachment並存；本地done preserved-speech task是已寫/測試收據，不等於merged。

## 19. codex/ai-agent-continuation-20261007

- 工作目錄：`C:/Users/x8120/.codex/worktrees/ai-agent-continuation-20261007/travel_scanㄐ`
- 決定：保留；主要原因：未合併 PR；未提交路徑：0；前次容量：0.682 GiB。
- HEAD：`bffe323af4e27f93795b795e3eb5571389ed118f`
- 原因：clean但#1372 OPEN且head bffe323a精確相同；main general-audience-ai-agent-versus-chatbot仍open。

具體待辦：

- [ ] 保留此managed worktree，沿#1372取得當前CI與內容/source/語言consumer review。
- [ ] 按現有AI agent票驗收原example/語言與影片包、owner播放/上傳/公開證據；PR未merged前不清checkout。

PR 證據：[1372](https://github.com/x812033727/travel_scanner/pull/1372) OPEN。

沿用任務：`2026-09-27-general-audience-ai-agent-versus-chatbot`、`2026-10-07-recover-confirmed-speech-answers-when-windows`。

證據：
- clean但#1372 OPEN且head bffe323a精確相同；main general-audience-ai-agent-versus-chatbot仍open。
- 主owner是23a9語言重審對話，未封存；9封存子代理不代表owner/影片交付已完成。

## 20. codex/ai-citation-completion-20261007

- 工作目錄：`C:/Users/x8120/.codex/worktrees/ai-citation-completion-20261007/travel_scanㄐ`
- 決定：保留；主要原因：未合併 PR；未提交路徑：0；前次容量：0.682 GiB。
- HEAD：`934a563ce4c48da6ed963dc2d14fea8fb98bb2a3`
- 原因：clean但#1369 OPEN且head934a563c精確相同；main general-audience-ai-citation-checking-video仍open。

具體待辦：

- [ ] 保留此managed worktree，沿#1369核對current-head CI與原citation tutorial/follow-along evidence。
- [ ] 用原語言票/source manifest完成獨立review與consumer readback；owner playback/upload/publication分開列證據，不釋放原claim。

PR 證據：[1369](https://github.com/x812033727/travel_scanner/pull/1369) OPEN。

沿用任務：`2026-09-27-general-audience-ai-citation-checking-video`、`2026-10-07-audio-review-distinguishes-transcripts-awaiting-a`、`2026-10-07-make-citation-video-evidence-portable-in`、`2026-10-07-make-tools-tests-portable-on-windows`。

證據：
- clean但#1369 OPEN且head934a563c精確相同；main general-audience-ai-citation-checking-video仍open。
- 主owner仍是23a9未封存語言重審對話；caption/source/metadata與包審核接受不等於影片上架/公開。

## 21. codex/llm-selected-language-completion-20261007

- 工作目錄：`C:/Users/x8120/.codex/worktrees/23a9/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：1；前次容量：0.681 GiB。
- HEAD：`7e26c83956ab5d6488f47bdd344276692ffd6b3b`
- 原因：#1368 OPEN且head與7e26c839精確相同；本地有environment.toml untracked，影片selected-language/submission/metadata舊package重審工作仍由未封存owner持有。

具體待辦：

- [ ] 保留environment.toml及selected-language/source-manifest逐項收據；沿#1368核對當前四必需CI/獨立review。
- [ ] 原selected-language票及主owner確認新manifest/consumer readback與原route接受；owner播放、upload/publication分開驗收，不以ready flag當完成。

PR 證據：[1368](https://github.com/x812033727/travel_scanner/pull/1368) OPEN。

沿用任務：`2026-10-07-complete-selected-languages-for-the-published`、`2026-10-07-count-targeted-dub-retakes-in-dry`、`2026-10-07-make-whisper-second-opinion-stdout-utf`、`2026-10-07-preserve-full-speech-answers-when-windows`。

證據：
- #1368 OPEN且head與7e26c839精確相同；本地有environment.toml untracked，影片selected-language/submission/metadata舊package重審工作仍由未封存owner持有。
- 完整source清單/metadata、caption review及audio/配音approved package不等於owner playback、YouTube upload/publication；不能以已封存子代理刪除主交付工作區。

## 22. codex/renewed-finals-host-handoff-20261007

- 工作目錄：`C:/Users/x8120/.codex/worktrees/7392/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：2；前次容量：0.681 GiB。
- HEAD：`d03c624b56953bb9116325a876b7ac4fc2d18d83`
- 原因：#1359 OPEN且head d03c624b精確相同，10 unique commits保存renewed-final與Temperature source resubmission、本地dirty2。

具體待辦：

- [ ] 保全untracked ({file 與environment.toml，確認({file實際用途後由owner處置。
- [ ] 沿#1359及existing renewed-finals票保留語言答卷/journal與native project證據，核對當前CI/review及source-bound新審稿；公開交付不得從已提交package推論。

PR 證據：[1359](https://github.com/x812033727/travel_scanner/pull/1359) OPEN。

沿用任務：`2026-10-01-hand-off-owner-approved-renewed-finals`、`2026-10-07-accept-windows-separators-in-stock-fetch`、`2026-10-07-continue-imported-language-units-before-requiring`、`2026-10-07-handle-a-no-cut-range-in`、`2026-10-07-imported-language-runner-hides-native-speech`、`2026-10-07-keep-executable-language-runtime-current`、`2026-10-07-keep-renewed-final-evidence-notes-portable`、`2026-10-07-preserve-speech-journal-writes-through-windows`、`2026-10-07-support-proven-thumbnail-encoding-in-renewal`、`2026-10-08-resubmit-temperature-language-source-manifest`。

證據：
- #1359 OPEN且head d03c624b精確相同，10 unique commits保存renewed-final與Temperature source resubmission、本地dirty2。
- main hand-off-owner-approved-renewed-finals仍open；各語言恢復/原答卷保全、source hash與approval/upload/publication是獨立門檻。

## 23. codex/mobile-planner-app-ui

- 工作目錄：`C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanㄐ`
- 決定：保留；主要原因：主倉庫；未提交路徑：1179；前次容量：0.678 GiB。
- HEAD：`75bb195badf0f26127b8cdf78c49ae71bde9a0e8`
- 原因：HEAD已main祖先且mobile舊產品已合併，但primary checkout的1179檔未提交來源/用途未逐檔確定。

具體待辦：

- [ ] 保護primary checkout與共用Git；用root全hash/index快照將1179檔分成已在main的同步內容、其他session改動與真正未整合內容，逐組核對原owner。
- [ ] 在隔離窄scope中記錄需要復原/保留/交接的路徑與receipt；不reset、不以branch名清整個primary目錄。

PR 證據：[28](https://github.com/x812033727/travel_scanner/pull/28) MERGED。

沿用任務：`2026-09-29-prevent-lost-long-running-language-stages`。

證據：
- exact HEAD 75bb195badf0f26127b8cdf78c49ae71bde9a0e8; mainAncestor=true; main...HEAD behind/ahead=1806/0; HEAD未較排行快照變動。
- HEAD 75bb195badf0f26127b8cdf78c49ae71bde9a0e8 mainAncestor=true、unique=0；#28 MERGED mergeCommit為main祖先。
- 這是Codex Travel共用Git所在的primary working copy，1179 dirty跨API/web/content/docs/tasks；不能從舊branch名認定全是mobile未完成改動，也不能由HEAD落地推論local bytes可丟。
- ignored包含歷史其他nested/checkouts、測試cache與可能私有工作材料；root已另做hash/index/ownership盤點。

## 24. codex/ai-term-embedding-20261004

- 工作目錄：`C:/Users/x8120/.codex/worktrees/ai-series-next-20261004/travel_scanㄐ`
- 決定：保留；主要原因：未完成交付／續作；未提交路徑：0；前次容量：0.660 GiB。
- HEAD：`545ce140d0cf46644a7b7ac1310b99e7105a1157`
- 原因：#1211 MERGED且merge是fresh main祖先，但PRhead並非local545ce140；local仍3 unique commits，不可用舊merged PR名稱證目前全部HEAD已落地。

具體待辦：

- [ ] 保留HEAD545ce140與完整source/語言/配音/STOP/receipt；逐3 unique commits對原Embedding生產門檻及successor資料，未證退役前不清。
- [ ] 沿canonical Embedding票與b136 owner核對恢復/hold/uncertain paid request及owner播放交付，不能盲重試或將#1211 merge當整部完成。

PR 證據：[1211](https://github.com/x812033727/travel_scanner/pull/1211) MERGED。

沿用任務：`2026-10-04-ai-term-embedding`。

證據：
- #1211 MERGED且merge是fresh main祖先，但PRhead並非local545ce140；local仍3 unique commits，不可用舊merged PR名稱證目前全部HEAD已落地。
- main 2026-10-04-ai-term-embedding仍in-progress；主owner是未封存b136對話，本工作區也有該owner attachment。clean只代表無未提交內容。

## 25. codex/ai-series-continuation-20261004

- 工作目錄：`C:/Users/x8120/.codex/worktrees/b136/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：1；前次容量：0.660 GiB。
- HEAD：`3b870bc37286f6e8accdaf30a27de3cbd3a7cb9e`
- 原因：#1207 MERGED但local3b870bc3不等PRhead，仍18獨有commit與1dirty；若干付費重試/publish-locale/QA修復在main已done。

具體待辦：

- [ ] 保全dirty與所有retained operation/source/journal receipts，原已merged safety guards不要重播。
- [ ] 沿LLM/Embedding既有票及原owner的固定cohort收據确认current hold/known provider requests，再判哪些原流程允許續作；備份G槽與移除media需原hash/還原/同步gate，不由此次Git cleanup代替。

PR 證據：[1207](https://github.com/x812033727/travel_scanner/pull/1207) MERGED。

沿用任務：`2026-10-04-ai-term-large-language-model`、`2026-10-04-audio-stage-incomplete-exits`、`2026-10-04-avoid-claiming-owner-youtube-upload-when`、`2026-10-04-jev-provider-uncertain-retries`、`2026-10-04-keyframes-crashes-when-every-image-take`、`2026-10-04-prevent-automatic-retries-of-paid-video`、`2026-10-04-prevent-paid-speech-retries-after-ambiguous`、`2026-10-04-reject-unselected-locales-in-video-publish`。

證據：
- #1207 MERGED但local3b870bc3不等PRhead，仍18獨有commit與1dirty；若干付費重試/publish-locale/QA修復在main已done。
- main ai-term-large-language-model仍open，持有者對話/Embedding successor attachments未封存，產品局部done並不使續作工作目錄完成。

## 26. codex/codex-learning-publication-receipt

- 工作目錄：`C:/Users/x8120/.codex/worktrees/fc2e/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：34；前次容量：0.623 GiB。
- HEAD：`a9e2b2afa4e158adc0974be5510e4d6d92189c34`
- 原因：#585 MERGED且head a9e2b2af與local精確相同，merge是fresh main祖先；Codex depth/content/finalize-release/hub-query-ads主線票done。

具體待辦：

- [ ] 保全34dirty與ignored收據logs，逐變更對main最新版和owner內容修改意圖；舊publication receipt封存不能丟掉新draft。
- [ ] 沿blocked Codex-learning-series確認具體blocked條件與內容/公開驗收；只有原scope完成、不再使用且dirty/ignored全部正式保存後才重新判可清。

PR 證據：[585](https://github.com/x812033727/travel_scanner/pull/585) MERGED。

沿用任務：`2026-09-14-codex-depth-content`、`2026-09-14-codex-depth-plan-alignment`、`2026-09-14-codex-learning-series`、`2026-09-20-codex-learning-finalize-release`、`2026-09-20-tutorial-hub-query-ads`。

證據：
- #585 MERGED且head a9e2b2af與local精確相同，merge是fresh main祖先；Codex depth/content/finalize-release/hub-query-ads主線票done。
- 仍34dirty，main Codex-learning-series blocked；原owner/pinned對話未封存，ignored包含獨有frontend regression/build/evidence logs。

## 27. codex/batch034-source-task-close

- 工作目錄：`C:/Users/x8120/.codex/worktrees/batch006-final-close/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：2；前次容量：0.546 GiB。
- HEAD：`dd1d51730c0c46698325fb357bb90ac0303d7b8c`
- 原因：兩處WordPress來源inline修正已合併；本機task結案副本尚需保全對帳。

具體待辦：

- [ ] 保存2個task版本、與main原票/後續source-publication票對帳，保留原#887與body hashes後完成窄記帳。
- [ ] 發布/rebinding沿既有wordpress-map來源待辦，由原owner處理；不要將scope外發布票併回這個已完成code節點。

沿用任務：`2026-09-28-correct-unrelated-ai-term-links-in`。

證據：
- exact HEAD dd1d51730c0c46698325fb357bb90ac0303d7b8c; mainAncestor=true; main...HEAD behind/ahead=468/0; HEAD未較排行快照變動。
- HEAD dd1d51730c0c46698325fb357bb90ac0303d7b8c是#887 merge commit，為main祖先，unique=0。
- 本機done票全文只結案repository source correction：wordpress-map-form-embeds及wordpress-multilingual-site各一處AI token link改純text；production來源發布/rebinding由另外窄票處理。
- dirty2是原open task修改與done新副本，不含新增source implementation；不能因此重做已完成兩處來源修正。

## 28. codex/korea-source-fact-corrections

- 工作目錄：`C:/Users/x8120/.codex/worktrees/korea-source-fact-corrections/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：6；前次容量：0.496 GiB。
- HEAD：`f34bb245691e7f32f97d1c9373394e87650591af`
- 原因：HEAD來源修正已main，但另有6個本機source/diagram/task變更尚未整合驗收。

具體待辦：

- [ ] 保存6檔patch、source hashes與圖稿；與batch011現有Nami/Seoul HOLD及shared source票核對重疊owner，不合併或覆蓋未核准來源。
- [ ] 獨立覆核Nami星期三holiday例外及圖文精確版本；把仍有效窄缺件放回已有同scope票，已main的Jeju完工部分不重做。

證據：
- exact HEAD f34bb245691e7f32f97d1c9373394e87650591af; mainAncestor=true; main...HEAD behind/ahead=781/0; HEAD未較排行快照變動。
- HEAD f34bb245691e7f32f97d1c9373394e87650591af mainAncestor=true、unique=0；Jeju已完成來源及四語工作不需重開。
- dirty6包含Jeju/Nami兩JSON、兩diagram，以及batch008/qualify-Nami-Wednesday-holiday任務原稿；它們是實際保留的本機bytes，不是純ref殘留。

## 29. codex/batch003-qa-tasks

- 工作目錄：`C:/Users/x8120/.codex/worktrees/batch003-qa-tasks/travel_scanㄐ`
- 決定：保留；主要原因：未完成交付／續作；未提交路徑：0；前次容量：0.487 GiB。
- HEAD：`3e072badac7c2a25e2d96ed4656536550cfb6feb`
- 原因：clean checkout但唯一QA註記尚未main；四繁中SVG仍有英文helper，onsen四語另有既有待辦。

具體待辦：

- [ ] 保留唯一QA註記与40-browser/80-screenshot歷史材料；接續窄票修四繁中SVG的英文helper並驗桌機/手機，不重發已公開四篇。
- [ ] onsen四語/SVG沿原Batch003票處理fresh source/review/release；先對帳既有已公開正文與舊未勾發布記錄。

沿用任務：`2026-09-20-five-language-article-batch-003`。

證據：
- exact HEAD 3e072badac7c2a25e2d96ed4656536550cfb6feb; mainAncestor=false; main...HEAD behind/ahead=794/1; HEAD未較排行快照變動。
- 唯一unique提交3e072badac7c2a25e2d96ed4656536550cfb6feb只改原Batch003票，追加實際公開圖稿QA缺件，沒有新的translation code或pack；clean checkout不等於此QA已處理。
- main原Batch003票OPEN，9/29正文已明載四非onsen篇五語公開且bodyhash與repo相符；onsen zhTW v8來源已修正，四target locales／SVG尚未落地。10/4清單仍有舊發布未完文字，與9/29已公開證據需分項對帳，不重發四篇也不重做onsen繁中修正。
- 本支新增的繁中圖稿QA註記未進main。直接讀frozen main四原文diagram-1.svg，仍有「A practical sequence」「Editorial diagram」以及Same party、Check receiver、Official booking、Choose station等英文輔助文字，正面證明此窄缺件尚在產品。
- 40 browser QA／80 screenshots的歷史引用在本支註記，是既有驗收材料，應保全再接續。onsen剩四語已在主票，與新的四繁中source SVG標籤修正分scope。

## 30. codex/article-localization-batch-005

- 工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-batch-005/travel_scanㄐ`
- 決定：保留；主要原因：未完成交付／續作；未提交路徑：0；前次容量：0.487 GiB。
- HEAD：`40d482aa1d56fa19a16df2bf56e2bc952ed142bf`
- 原因：clean checkout只保留作者/來源review記帳，Nikko/Kyoto8份四語refresh仍未完成。

具體待辦：

- [ ] 沿2026-10-06-batch-005-nikko-kyoto-translations-refresh尋找/核對舊external staging與備份；既有指定external path已不存在的歷史結果需保存，不假裝找回譯文。
- [ ] 待京都既有zhTW來源發布後重新pin來源；補Nikko同行日本國籍資格、Kyoto刷卡/一日券啟用/線型，重綁8份翻譯與圖稿、取得獨立完整review後再走內容PR。

沿用任務：`2026-09-20-article-localization-batch-005`、`2026-10-06-batch-005-nikko-kyoto-translations-refresh`、`2026-10-06-publish-onsen-kyoto-bus-zh-tw`。

證據：
- exact HEAD 40d482aa1d56fa19a16df2bf56e2bc952ed142bf; mainAncestor=false; main...HEAD behind/ahead=797/2; HEAD未較排行快照變動。
- 兩個 unique commits 只有 tasks/open 的作者/來源review紀錄，沒有 content pack、翻譯 asset 或 review approval 寫入 Git。完整末次 task 明示8 unsigned jobs、editorial/glyph review未簽、Kyoto/Nikko source-fact holds、summary/FAQ/render tooling仍待整合，不能列已完成收據。
- frozen main Kyoto/Nikko packs 仍只有 zh-TW；main open 2026-10-06-batch-005-nikko-kyoto-translations-refresh 已直接承接這批工作，記錄 corrected live v8與8 target locales unpublished、重新source pin及獨立審稿缺件。Kyoto source後續 #1001/#1028 修改另由publish-onsen-kyoto-bus-zh-tw追蹤。
- fresh frozen及唯讀再查 checkout 為 clean，無一般untracked files；ignored清單只有20個Python .pyc與generated tasks/BOARD.md，沒有藏在checkout的未完翻譯/媒體。歷史指定 external staging C:/Users/x8120/.codex/article-localization-batch-005 現在不存在；缺件仍需復原或重新翻譯。

## 31. codex/article-five-language-completion

- 工作目錄：`C:/Users/x8120/.codex/worktrees/c5d9/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：1099；前次容量：0.315 GiB。
- HEAD：`8c83e90ab401f05044f614e5843c00d26aaed3dd`
- 原因：HEAD已main祖先，但1099檔本機變更涵蓋多個產品與資料/文稿，其精確未完scope仍需原owner逐組對帳。

具體待辦：

- [ ] 保留1099檔working bytes與index/hash快照，按source/API/UI/material/task分組比較frozen main，找出已被後續PR替代與真正需續作的部分。
- [ ] 與原聊天/session對帳本機改動來源與claim；只為具體仍未完成scope補窄票，不重開已落地舊HEAD全部產品。

證據：
- exact HEAD 8c83e90ab401f05044f614e5843c00d26aaed3dd; mainAncestor=true; main...HEAD behind/ahead=890/0; HEAD未較排行快照變動。
- HEAD 8c83e90ab401f05044f614e5843c00d26aaed3dd mainAncestor=true、unique=0，不能把舊HEAD稱未合併。
- dirty1099跨guides API/series、web/life/article UI、Gemini導覽、內容/assets/docs/tasks；branch名不能證明全部屬同一five-language任務或可丟棄。

## 32. codex/country-foods-map-links

- 工作目錄：`C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-foods-maps`
- 決定：保留；主要原因：未提交修改；未提交路徑：17；前次容量：0.072 GiB。
- HEAD：`a8736021c98f38a71e5f57555766d4cb86cc893e`
- 原因：country foods產品已由replacement #56整合，保留的是17檔formatting-only本機patch待處置。

具體待辦：

- [ ] 保存17檔exact bytes/diff與既有AST-equivalence證據；沿preserve-country-foods-formatting窄票核對原owner意圖後決定保留或整合，不reset。
- [ ] 不重做已合併food catalog/map-link產品；舊0020與#56替代0022migration的chain改名證據一併保留。

沿用任務：`2026-10-11-preserve-country-foods-formatting`。

證據：
- exact HEAD a8736021c98f38a71e5f57555766d4cb86cc893e; mainAncestor=false; main...HEAD behind/ahead=1729/1; HEAD未較排行快照變動。
- Producer PR #56 on replacement branch codex/country-foods-map-links-pr merged as 803b84601340d024fcdfe4fb326e086aa2a4e9c3, confirmed ancestor of frozen fresh main 73c84ca7. Of 63 product paths, 57 are exact branch blobs at that merge; foods/service.py has a positive main-history match and equivalent create-only initialization after upstream integration.
- Unmatched old migration 0020_food_catalog.py is positively replaced by PR #56 migration 0022_food_catalog.py. Python AST comparison proves both entire upgrade/downgrade bodies exactly equal; only revision/down_revision chain metadata changed to follow itinerary system slots and hotspot AI search. test_schema.py explicitly moves expected head to0022 and checks0020/0021 are no longer heads.
- The models and itinerary/router differences against PR #56 are upstream system-slot/schedule/AI additions rather than missing food changes; food catalog, map-link UI, API and focused food tests are already present in the merged producer scope.
- Cleanup remains protected: checkout C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-foods-maps has17 uncommitted Python paths. Full dirty diff was read; AST comparison of HEAD versus working bytes proves all17 are formatting-only, but the user/root explicitly require these bytes be preserved and disposition tracked.

## 33. codex/article-localization-batch-011-korea

- 工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-batch-011-korea/travel_scanㄐ`
- 決定：保留；主要原因：未提交修改；未提交路徑：17；前次容量：0.050 GiB。
- HEAD：`1fbd57ac8845c8d4f465be7a1914669386f26ee7`
- 原因：Jeju已完成；Nami/Seoul8份候選+8圖與來源修正仍HOLD，17檔dirty必須保存。

具體待辦：

- [ ] 保留5 tracked＋12 untracked全部bytes，沿reconcile-nami-seoul-localization補對帳；Jeju與main相同，不重開Jeju。
- [ ] Nami核对13:30、取消50%、under36條件及交通source；Seoul核對T-Luggage服務站/尺寸/terminal。保留原policy拒絕，不換工具重試receipt。
- [ ] 經允許的獨立SOURCE PASS後再重綁8份翻譯/8圖與main新楓葉互連，完成獨立文字/視覺review後交內容PR。

沿用任務：`2026-09-21-localize-three-korea-travel-guides-in`、`2026-10-11-reconcile-nami-seoul-localization`、`2026-09-22-localize-jeju-car-rental-guide-in`。

證據：
- exact HEAD 1fbd57ac8845c8d4f465be7a1914669386f26ee7; mainAncestor=false; main...HEAD behind/ahead=754/1; HEAD未較排行快照變動。
- 唯一commit 1fbd57ac 的Jeju source correction已精確被 #643整合：branch zh-TW與main一致；目前本機Jeju5語pack及4份untracked SVG在CRLF正規化後全與frozen main相同，Jeju不是剩餘localization缺件。main done Jeju-only task與2026-09-22 release receipts記錄獨立review與發布。
- 同commit的Nami rail-bike source correction尚未落地：branch /locales/zh-TW/blocks/24 提13:30及當日取消扣50%；main仍13:00及舊退款敘述。main後續 #1272只插楓葉文章互連，未取代該更正。
- 完整working-tree task已讀，scope縮為Nami/Seoul並明示HOLD：Nami under36month parental/proof/ferry條件新修正待獨立review；Seoul T-Luggage service-center/size/terminal proposal未獨立核准。歷史receipt write遭policy拒绝不重試／繞過；本次只有唯讀盤點。
- frozen及再查共有17變更（5 tracked+12 untracked）。本機Nami與Seoul各有四語documents及各4SVG，frozen main各仍zh-TW-only。Nami還有本機來源diagram變更，並缺main新插入楓葉互連；候選需重新對main source對齊並審稿。不能刪checkout或任何素材。

## 34. codex/security-hardening

- 工作目錄：`C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-security`
- 決定：保留；主要原因：未提交修改；未提交路徑：1；前次容量：0.037 GiB。
- HEAD：`0c139a27b48f204e42edc39d777b25161924a7e1`
- 原因：security HEAD已完整合併，但一份CI workflow本機修改尚未保存處置。

具體待辦：

- [ ] 保存ci.yml exact patch與hash，對照main及原owner目的，確認是否後續CI已替代或需另開窄CI票整合。
- [ ] 安全產品不重做；待原owner確認local patch保存/整合及ownership釋放後另行決定checkout清理。

PR 證據：[23](https://github.com/x812033727/travel_scanner/pull/23) MERGED。

證據：
- exact HEAD 0c139a27b48f204e42edc39d777b25161924a7e1; mainAncestor=true; main...HEAD behind/ahead=1788/0; HEAD未較排行快照變動。
- #23 MERGED exact HEAD 0c139a27b48f204e42edc39d777b25161924a7e1；HEAD及mergeCommit皆main祖先，unique=0。
- 唯一dirty路徑.github/workflows/ci.yml，不能由安全產品完工推論這份CI修改可丟。

## 35. codex/article-localization-batch016-llms

- 工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-batch016-llms`
- 決定：保留；主要原因：未提交修改；未提交路徑：692；前次容量：0.001 GiB。
- HEAD：`fd63272eba3b44d2f36f43bac128b0e5c72562de`
- 原因：LLMS私有draft五語產品已由#654替代整合；692個tracked task缺檔/index狀態尚需保存對帳。

具體待辦：

- [ ] 保留HEAD、index簽章與缺檔清單；核對原session/缺檔來源後只從已保全HEAD復原需要tasks/，或維持隔離。
- [ ] 13產品檔與#654完整同blob、兩原票main done的證據已足夠；私有draft/WITHHOLD是原驗收要求，不補不必要公開發布。

PR 證據：[655](https://github.com/x812033727/travel_scanner/pull/655) CLOSED。

沿用任務：`2026-09-22-correct-llms-txt-evaluation-token-link`、`2026-09-22-localize-llms-txt-evaluation-draft-only`。

證據：
- exact HEAD fd63272eba3b44d2f36f43bac128b0e5c72562de; mainAncestor=false; main...HEAD behind/ahead=733/2; HEAD未較排行快照變動。
- PR #655 是 CLOSED，而不是個別 MERGED；完成證據是 #654 d5f03e679bef2102e843426c42f045aef4ae08c0 的替代整合。逐一比較本支13個產品檔（1完整五語pack＋12素材）與#654 snapshot，13/13精確同blob；不是只看closed狀態或git ancestry。
- main author票 DONE 的完整收據明載 #655 unchanged integrated into #654，五語33 blocks/7 sources各v1只匯入私有draft，未有published hash/version/time，五語預覽及signed-out browser/API/sitemap隱私驗收已完成。與另一已公開llms文章重複，因此不得把私有草稿不公開算欠發布。
- main token-link票亦DONE；目前pack的15個parsed差異全是五語普通「標記」inline由AI glossary ArticleInline轉text，visible word不變，原來源及duplicate-topic exclusion保留。沒有缺四語內容或未落地素材。
- fresh checkout dirty692全部為工作目錄 D 缺檔、無現存bytes，路徑全部tasks/（舊共享任務記錄），不是692譯文變更。提交完成與缺檔checkout保護分開；本輪不可reset/release/archive/remove。
- 完成的歷史branch HEAD／原task版本與外部WITHHOLD/PASS／delivery收據需保全為archive；status只表示交付已被接替且可保全，不授權清除dirty/active checkout。

## 36. codex/article-localization-source-edit-preservation

- 工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-source-edit-preservation`
- 決定：保留；主要原因：未提交修改；未提交路徑：2507；前次容量：0.001 GiB。
- HEAD：`a80f6b5faef47a17c862e8a981d78f5f3b4cfd06`
- 原因：preservation實作由#654完整整合、三原票done；2507個tracked缺檔/index狀態需保存對帳。

具體待辦：

- [ ] 保留HEAD、index與缺檔清單及WITHHOLD/PASS/delivery receipts，核對原session/缺檔來源後在隔離scope決定需要復原的path。
- [ ] 2507全為工作目錄D且沒有現存bytes，不能說成2507次翻譯改動；不reset、不釋出claim、不重做已合併preservation implementation。

PR 證據：[652](https://github.com/x812033727/travel_scanner/pull/652) CLOSED。

沿用任務：`2026-09-21-authorize-reviewed-source-corrections-in-localization`、`2026-09-22-compare-deployed-localization-packs-by-validated`、`2026-09-22-preserve-reviewed-unselected-repository-locale-edits`。

證據：
- exact HEAD a80f6b5faef47a17c862e8a981d78f5f3b4cfd06; mainAncestor=false; main...HEAD behind/ahead=733/8; HEAD未較排行快照變動。
- 原PR #652 CLOSED，但其工作 unchanged integrated into merged #654 d5f03e679bef2102e843426c42f045aef4ae08c0。逐一比較5個scoped程式／測試檔在#654 snapshot皆精確同blob；current main repository_preservation.py同blob，assembler/publisher/tests後來演進亦有歷史同blob。
- main三原票全部DONE，完整preservation票保留舊WITHHOLD與修復：current HEAD必須等於baseline.repo_commit，tempGit A成功／emptyB拒絕回歸已做；126 passed/59 skipped、Ruff/check tasks記錄，並有#6549/9CI與guarded batch015保留repository edit而published zhTW v8未改、四missinglocaleimport/publish驗收。
- fresh dirty2507是apps/api（含guides content與tests）、docs及舊任務／工具等tracked路徑全部工作目錄缺檔，exists=false且沒有現存檔案bytes；其中1473 apps/api/app、257 apps/api/tests。這不是2507未提交翻譯或程式差異，也不能憑缺檔猜此前誰清掉。
- 原baseline/source/locale published bytes仍是當時live值，reviewreceipt與staleHEAD防護必須保留。完成交付的正面證據不解除dirty checkout或原owner防護。
- 完成的歷史branch HEAD／原task版本與外部WITHHOLD/PASS／delivery收據需保全為archive；status只表示交付已被接替且可保全，不授權清除dirty/active checkout。

## 保存核對

除本輪自己的審核工作目錄以外，原盤點的工作目錄 HEAD、status、index 與已存在的未提交檔案 SHA-256 均通過前後一致核對。本輪移除指令執行次數為 0。

下次須重新取得 live HEAD、status、PR、程序與所有權；本報告不是未來刪除許可。
