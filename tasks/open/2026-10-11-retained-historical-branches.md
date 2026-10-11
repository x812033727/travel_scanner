---
id: 2026-10-11-retained-historical-branches
title: Reconcile retained historical branches after the 197-branch cleanup
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T13:17:06Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-retained-historical-branches.md
---

## Why

2026-10-11 依站主要求核對 Claude 與 Codex 的 197 個本機歷史分支。確認完成、沒有工作目錄使用或未提交修改的 ref 已備份後清理；本票保存仍需續作或核對的分支與下一步。

## Done when

- 每個保留分支的獨有工作已有明確對應任務，或有內容整合／取代的可核對紀錄。
- 依既有票續作；未共享的工作先補窄範圍任務。既有認領、製作 STOP 與外部核准仍有效。
- 後續只有在完成條件、未提交修改與使用狀態重新核對後，才清理分支。

## Steps

- [ ] 核對認領者與現有工作目錄，依下列分支索引續作；不因 chat idle 判定釋出。
- [x] 深入核對原 24 個待核對分支的獨有差異，逐項記錄已取代內容、完成收據或實際尚未完成工作。
- [x] 深入核對原先其餘64個，補回缺失的具體待辦並連回原HEAD；既有未完成票與認領保留。
- [ ] 完成的項目重新檢查與備份後清理，並更新本索引。

## Verification

本票是追蹤索引，scope 只含此檔；實作走既有任務或另外認領窄範圍票。不得藉本票改動其他模型的認領、影片生產或正式站。

## Notes

覆核時間：2026-10-11T14:25:30.963423+00:00（UTC）。原始197個本機歷史分支全部已有深入核對；本輪處理原先其餘64個。

已刪除 168 個（Codex 149、Claude 19）；保留 29 個（Codex 24、Claude 5）。
前轮24個已清理17、保留7，其索引紀錄不改寫。原先其餘64個保留分支已深入核對：本輪清理42個、保留22個（未完成18個；原scope完成但保存工作4個）。累計197個清理168個、保留29個。

刪除前已保存完整 Git bundle，驗證 SHA-256，並在獨立空白 bare repository 中還原每個 HEAD；沒有借用原始物件庫。每次刪除都比對預期 HEAD，確認分支未被任何 worktree 使用、沒有開啟中的 PR，並驗證 ref 已不存在。

完整核對、清理及還原證據位於 `C:/Users/x8120/.codex/scratch/historical-cleanup-20261011/`。主幹基準 `0c93720e684b4c3995b16f7c2e859fe2bc06ec9f`。

- 備份 `completed-codex.bundle`：93 個分支；SHA-256 `90926263e043158940b0612550a68f12ec79fb2c47e51c9cbfb8b8a95e4c1774`；獨立還原通過。
- 備份 `completed-codex-supplement-2.bundle`：4 個分支；SHA-256 `2b3aeadb1056f3f2369e0c1c7ca25d94a222969a3b7d0118d1dbecf74c2a8072`；獨立還原通過。
- 備份 `completed-claude.bundle`：12 個分支；SHA-256 `b59844447c9b39b03c579137b3f58e1f43a71bc0f672b0acfa0e3bf3a40d1e73`；獨立還原通過。

本輪詳細證據：`C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/`；新主幹基準 `73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b`。完整執行收據為 `cleanup-receipt.json`，保留修改驗證為 `post-cleanup-verification.json`。

- 本輪備份 `completed-codex.bundle`：14 個分支；SHA-256 `5b58f4e1673c6a7064a8916cb123d950cb733a4e635fb1a43b1d4ed13f427a39`；獨立空白 bare repository 還原通過。
- 本輪備份 `completed-claude.bundle`：3 個分支；SHA-256 `a29f0d7f00f5ddbe1967d591e7f2195c531b99075c117a6c0a76c72db1f2568e`；獨立空白 bare repository 還原通過。

本輪64項證據：`C:/Users/x8120/.codex/scratch/retained64-followup-20261011/`；新main基準`1f183e4d1f3bb493b5412ca242f2cbb98da4f9bf`。本輪所有9個checkout完整保留；《偶的江湖》仍在Claude製作，不接管、不清理。

- 本輪64項備份 `completed-codex.bundle`：38個分支；SHA-256 `6699e2f8fb3a02d9e088cb80140611b3d3d670682dbd91e4545a2e778b140794`；獨立空白bare repository逐HEAD還原通過。
- 本輪64項備份 `completed-claude.bundle`：4個分支；SHA-256 `45669fde7446eb8548ee5476d3cf40e2988900b938b4cd091a6375a33d5b69a7`；獨立空白bare repository逐HEAD還原通過。

以下為分支索引，不重複開已存在的任務。所有原認領均保留；同一任務可能由多個歷史分支指向。

### 文章、多語系與發布（7）

- [ ] **Codex `codex/article-localization-031-pair-b` — 未完成**。沿用 existing source ticket 2026-09-27-correct-wordpress-user-roles-unrelated-ai，先核對／完成修正後繁中公開版本與來源 hash 重捕捉；本輪不進正式站或發布。
  - 核對 HEAD：`e8fa87d9abb0969a5c9861e5b0b551757cd47ba6`。
  - 待辦：在窄 scope 對帳 user-roles 本支四語與12素材，依新的 zh-TW hash 重綁並補獨立差異審查，再補主線內容 PR 與獨立 release 票；social-login 與其他已落地三篇不重開。
  - 任務：[2026-10-11-reconcile-wordpress-user-roles-locales](../../tasks/open/2026-10-11-reconcile-wordpress-user-roles-locales.md)（主幹 本 PR open）。
  - 任務：`2026-09-27-localize-wordpress-social-login-and-user`（主幹 absent）。
  - 任務：[2026-09-27-correct-wordpress-user-roles-unrelated-ai](../../tasks/open/2026-09-27-correct-wordpress-user-roles-unrelated-ai.md)（主幹 open）。
  - 核對證據：唯一提交 e8fa87d9abb0969a5c9861e5b0b551757cd47ba6 是 social-login 與 user-roles 各四語全文及 24 素材；原本作者票 localize-wordpress-social-login-and-user 在分支 done，但 frozen main 找不到該 ID。不能由本地 done 推論兩篇都已交付主線。
  - 核對證據：wordpress-social-login 的五語 parsed pack 與 main 完全相同，12 個新素材有精確歷史／main blob；main 完成票 batch031-three-wordpress-target-locales 明載採用本支 SHA，PR #879 2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1 已 merged，這半邊不重做。
  - 核對證據：wordpress-user-roles 目前 main 只有 zh-TW；本支 en/ja/ko/zh-CN 全文與 diagram/hero 共12素材皆沒有 main 歷史同 blob，也沒有後續導入的四語產品。比較只剩四個 locale 節點以及 zh-TW block20 inline1 的已修正 AI 連結三欄。
  - 核對證據：PR #875 4b6c5cd99fa9eab3b658d5b6cf639cb001f8fc3e 已將 zh-TW「參數」改純文字，但 main 原來源票仍 open，明確只完成 repository 修正、正式來源發布與重綁未完成。保留 reviewed 翻譯，不可把舊 pack 直接回寫以還原錯誤 ArticleInline。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-reconcile-wordpress-user-roles-locales。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'path': 'apps/api/app/guides/content/wordpress-social-login.json', 'status': 'M', 'baseBlob': '72513515ea98e2c8d035581b8af124ba40eb7178', 'branchBlob': '8cf029a4eee5bfd78672dd19c595f2f7e52f0bf1', 'mainBlob': '8cf029a4eee5bfd78672dd19c595f2f7e52f0bf1', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': '2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1', 'ownMergeBlob': None}`, `{'path': 'apps/api/app/guides/content/wordpress-user-roles.json', 'status': 'M', 'baseBlob': '20e54c0bbc6f70330d8aa58566b5cb13a6c89326', 'branchBlob': '4cc690d0745c0a39133ab0f034cff7d720f68e6d', 'mainBlob': '8013c4135137583e375a4ecc2c1138723326340a', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': None, 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/diagram-1-en.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'f42b30c0defa95472b9364a426b82335a80fdf0f', 'mainBlob': 'bc136da72a630b76a21766fa198ae88680d1110b', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '77a58c85a4912daad9a1d117364e5260d92a9cc6', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/diagram-1-ja.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'bac45479893acecbb22568be3b5e4fbbfcb37e27', 'mainBlob': 'aff4de42587385396e59903dadcbe13b89c4829e', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '77a58c85a4912daad9a1d117364e5260d92a9cc6', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/diagram-1-ko.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'abd4e182e4563d9286c92ec0819dc0ed3c418e02', 'mainBlob': 'c4c969b3adbfca3c4978703c7d470a0b04b84be3', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '77a58c85a4912daad9a1d117364e5260d92a9cc6', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/diagram-1-zh-cn.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '6b64d63616220c4d18859c5f0dff6805c125e908', 'mainBlob': '6b64d63616220c4d18859c5f0dff6805c125e908', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': '2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/hero-en.jpg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '8f2316f57e436248a5de04a81c1e26f158b61d95', 'mainBlob': '8f2316f57e436248a5de04a81c1e26f158b61d95', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': '2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/hero-en.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '20d12b1ec6a0251bd7c4ca2a3c9282579476ffce', 'mainBlob': '20d12b1ec6a0251bd7c4ca2a3c9282579476ffce', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': '2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/hero-ja.jpg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '3b8a13982c43aa888b7e85243424d17b9a0d39ae', 'mainBlob': '3b8a13982c43aa888b7e85243424d17b9a0d39ae', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': '2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/wordpress-social-login/hero-ja.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'c08b0aba0bfcc23aceebcbe463af4a32dc30fa09', 'mainBlob': 'c08b0aba0bfcc23aceebcbe463af4a32dc30fa09', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': '2fa7bf1e567079e06bfc1149faa8929bcfe9b7b1', 'ownMergeBlob': None}`。

- [ ] **Codex `codex/article-localization-batch-005` — 未完成**。沿用 main 2026-10-06-batch-005-nikko-kyoto-translations-refresh：先查原 staging 是否已搬走／備份；記錄找到的實際路徑與hash，若確認不存在再以既有產線重建8份翻譯。
  - 核對 HEAD：`40d482aa1d56fa19a16df2bf56e2bc952ed142bf`。
  - 待辦：等京都既有 zh-TW 發布待辦處理後重新擷取來源hash；Nikko補日本國籍陪同者資格，Kyoto補均一票價下車刷卡／一日券首次下車啟用及線型，同步四語diagram。
  - 待辦：逐份取得獨立文字、數字、glyph、photo/SVG與連結覆核，確認目前工具已含必要 summary/FAQ處理；再開內容PR，正式發布與桌機／手機readback走後續guarded gate。
  - 任務：`2026-09-20-article-localization-batch-005`（主幹 absent）。
  - 任務：[2026-10-06-batch-005-nikko-kyoto-translations-refresh](../../tasks/open/2026-10-06-batch-005-nikko-kyoto-translations-refresh.md)（主幹 open）。
  - 任務：[2026-10-06-publish-onsen-kyoto-bus-zh-tw](../../tasks/open/2026-10-06-publish-onsen-kyoto-bus-zh-tw.md)（主幹 open）。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-batch-005/travel_scanㄐ`；未提交路徑 0 個，狀態及檔案 SHA-256 已比對確認未變。
  - 核對證據：兩個 unique commits 只有 tasks/open 的作者/來源review紀錄，沒有 content pack、翻譯 asset 或 review approval 寫入 Git。完整末次 task 明示8 unsigned jobs、editorial/glyph review未簽、Kyoto/Nikko source-fact holds、summary/FAQ/render tooling仍待整合，不能列已完成收據。
  - 核對證據：frozen main Kyoto/Nikko packs 仍只有 zh-TW；main open 2026-10-06-batch-005-nikko-kyoto-translations-refresh 已直接承接這批工作，記錄 corrected live v8與8 target locales unpublished、重新source pin及獨立審稿缺件。Kyoto source後續 #1001/#1028 修改另由publish-onsen-kyoto-bus-zh-tw追蹤。
  - 核對證據：fresh frozen及唯讀再查 checkout 為 clean，無一般untracked files；ignored清單只有20個Python .pyc與generated tasks/BOARD.md，沒有藏在checkout的未完翻譯/媒體。歷史指定 external staging C:/Users/x8120/.codex/article-localization-batch-005 現在不存在；缺件仍需復原或重新翻譯。
  - 續作路徑：`tasks/open/2026-09-20-article-localization-batch-005.md`。

- [ ] **Codex `codex/article-localization-batch-006` — 未完成**。依新待辦 `2026-10-11-reconcile-hanoi-localization` 續作，原始分支与既有修改完整保留。
  - 核對 HEAD：`56d98e4decce9f760179665119c2821c350b7613`。
  - 待辦：將原Hanoi authoring及Vietnam Tourism來源修復待辦補回共享tasks/open（若root合併為一票需保留兩個缺件），避免重複新增已完成的KL／Singapore工作。
  - 待辦：查找原四語 unsigned jobs的保留/備份；重新驗證官方來源URL與Hoan Kiem claim coverage，提出最小來源修復並取得獨立覆核。
  - 待辦：讀目前正式站zh-TW版本／hash確認#599句子是否已發布；在來源修正正式發布後rebind四語jobs、受控同站locale links与SVG，獨立審稿、內容PR、後續發布及readback。
  - 任務：[2026-10-11-reconcile-hanoi-localization](../../tasks/open/2026-10-11-reconcile-hanoi-localization.md)（主幹 本 PR open）。
  - 任務：`2026-09-20-article-localization-batch-006`（主幹 absent）。
  - 任務：`2026-09-20-hanoi-old-quarter-vietnam-tourism-source`（主幹 absent）。
  - 任務：[2026-09-20-article-localization-batch-006-three-guides](../../tasks/done/2026-09-20-article-localization-batch-006-three-guides.md)（主幹 done）；原認領 codex-batch006-three。
  - 任務：[2026-09-20-correct-hanoi-old-quarter-source-sentence](../../tasks/done/2026-09-20-correct-hanoi-old-quarter-source-sentence.md)（主幹 done）；原認領 codex-source-ticket-cleanup-20261003。
  - 核對證據：兩個 unique commits 是claim與scope split，只修改3張task。完整local task把KL/Singapore交給three-guides，保留Hanoi authoring；其四語jobs unsigned，來源sentence correction部署／source version rebind及獨立review尚未完成。
  - 核對證據：KL與Singapore portion 已由 #602/#605/#607及#617取代：main done three-guides task完整final closeout記錄15 public routes、31 browser cases、source/QA驗證及hold clear。這部分從本branch待辦移除。
  - 核對證據：#599 source-only correction MERGED e8ad6c1d；main done source task明示其結案不包含Hanoi publication、四語rebind或失效來源維護。frozen Hanoi pack仍只有zh-TW，整個path history最新產品變更仍是 #599；main retains Vietnam Tourism舊URL /places-to-go/northern-vietnam/ha-noi；無替代翻譯PR/pack落地或citation更換證據。
  - 核對證據：原Hanoi localization與source-link兩task均未在frozen main保留，unique branch正保存這兩個具體未完handoff；不能因three-guides已done刪掉Hanoi。未對production或官方URL作新現況HTTP判斷。
  - 續作路徑：`tasks/open/2026-09-20-article-localization-batch-006-three-guides.md`, `tasks/open/2026-09-20-article-localization-batch-006.md`, `tasks/open/2026-09-20-hanoi-old-quarter-vietnam-tourism-source.md`。

- [ ] **Codex `codex/article-localization-batch-011-korea` — 未完成**。依新待辦 `2026-10-11-reconcile-nami-seoul-localization` 續作，原始分支与既有修改完整保留。
  - 核對 HEAD：`1fbd57ac8845c8d4f465be7a1914669386f26ee7`。
  - 待辦：保留整個dirty worktree及12 SVG；把已縮為Nami／Seoul的local任務補到共享tasks/open，帶上17檔清單與hash；Jeju已完成且候選等同main，勿重開Jeju翻譯。
  - 待辦：Nami：重新查證rail-bike13:30、當日取消扣50%、未滿36個月陪同／證明／渡輪條件與Gapyeong官方公車時刻圖；由獨立覆核者核准精確來源patch並保留新main楓葉互連。
  - 待辦：Seoul：核對T-Luggage服務站、尺寸與機場terminal來源提案，先取得允許的獨立覆核；原policy拒絕的receipt不得用換工具或路徑繞過。
  - 待辦：來源完成後重綁Nami/Seoul8份候選翻譯與8圖、核對每份來源及artifact hash、完整獨立文字／視覺review、正式內容PR；發布與public QA後續處理。
  - 任務：[2026-10-11-reconcile-nami-seoul-localization](../../tasks/open/2026-10-11-reconcile-nami-seoul-localization.md)（主幹 本 PR open）。
  - 任務：`2026-09-21-localize-three-korea-travel-guides-in`（主幹 absent）。
  - 任務：[2026-09-22-localize-jeju-car-rental-guide-in](../../tasks/done/2026-09-22-localize-jeju-car-rental-guide-in.md)（主幹 done）；原認領 codex-p1-audit。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-batch-011-korea/travel_scanㄐ`；未提交路徑 17 個，狀態及檔案 SHA-256 已比對確認未變。
  - 核對證據：唯一commit 1fbd57ac 的Jeju source correction已精確被 #643整合：branch zh-TW與main一致；目前本機Jeju5語pack及4份untracked SVG在CRLF正規化後全與frozen main相同，Jeju不是剩餘localization缺件。main done Jeju-only task與2026-09-22 release receipts記錄獨立review與發布。
  - 核對證據：同commit的Nami rail-bike source correction尚未落地：branch /locales/zh-TW/blocks/24 提13:30及當日取消扣50%；main仍13:00及舊退款敘述。main後續 #1272只插楓葉文章互連，未取代該更正。
  - 核對證據：完整working-tree task已讀，scope縮為Nami/Seoul並明示HOLD：Nami under36month parental/proof/ferry條件新修正待獨立review；Seoul T-Luggage service-center/size/terminal proposal未獨立核准。歷史receipt write遭policy拒绝不重試／繞過；本次只有唯讀盤點。
  - 核對證據：frozen及再查共有17變更（5 tracked+12 untracked）。本機Nami與Seoul各有四語documents及各4SVG，frozen main各仍zh-TW-only。Nami還有本機來源diagram變更，並缺main新插入楓葉互連；候選需重新對main source對齊並審稿。不能刪checkout或任何素材。
  - 續作路徑：`apps/api/app/guides/content/jeju-car-rental-guide.json`, `apps/api/app/guides/content/nami-island-petite-france-day-trip.json`, `apps/web/public/guides/jeju-car-rental-guide/diagram-1.svg`, `tasks/open/2026-09-21-localize-three-korea-travel-guides-in.md`。

- [ ] **Codex `codex/article-localization-batch016-llms` — 原scope完成，保留工作**。保留缺檔checkout與其index／HEAD／session證據；在另行核對原owner與索引簽章後決定僅從已保全HEAD復原tasks/或維持隔離。本輪不釋出claims、不清工作目錄。
  - 核對 HEAD：`fd63272eba3b44d2f36f43bac128b0e5c72562de`。
  - 任務：[2026-09-22-correct-llms-txt-evaluation-token-link](../../tasks/done/2026-09-22-correct-llms-txt-evaluation-token-link.md)（主幹 done）；原認領 claude-opus-5-5。
  - 任務：[2026-09-22-localize-llms-txt-evaluation-draft-only](../../tasks/done/2026-09-22-localize-llms-txt-evaluation-draft-only.md)（主幹 done）；原認領 codex-batch016-en-zhcn。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-batch016-llms`；未提交路徑692個；現存內容／缺檔與index signature分別保存。
  - 核對證據：PR #655 是 CLOSED，而不是個別 MERGED；完成證據是 #654 d5f03e679bef2102e843426c42f045aef4ae08c0 的替代整合。逐一比較本支13個產品檔（1完整五語pack＋12素材）與#654 snapshot，13/13精確同blob；不是只看closed狀態或git ancestry。
  - 核對證據：main author票 DONE 的完整收據明載 #655 unchanged integrated into #654，五語33 blocks/7 sources各v1只匯入私有draft，未有published hash/version/time，五語預覽及signed-out browser/API/sitemap隱私驗收已完成。與另一已公開llms文章重複，因此不得把私有草稿不公開算欠發布。
  - 核對證據：main token-link票亦DONE；目前pack的15個parsed差異全是五語普通「標記」inline由AI glossary ArticleInline轉text，visible word不變，原來源及duplicate-topic exclusion保留。沒有缺四語內容或未落地素材。
  - 核對證據：fresh checkout dirty692全部為工作目錄 D 缺檔、無現存bytes，路徑全部tasks/（舊共享任務記錄），不是692譯文變更。提交完成與缺檔checkout保護分開；本輪不可reset/release/archive/remove。
  - 核對證據：完成的歷史branch HEAD／原task版本與外部WITHHOLD/PASS／delivery收據需保全為archive；status只表示交付已被接替且可保全，不授權清除dirty/active checkout。
  - 續作路徑：`{'path': 'apps/api/app/guides/content/llms-txt-evaluation.json', 'status': 'M', 'baseBlob': '9f935d820f6e02d08c0272a2fed2ab86e19b8e07', 'branchBlob': '551be9901a9e9f915aae372be48a2ffa24799a57', 'mainBlob': '304469585a03a0f424a7b18b16acabf7db6343b8', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '1e1dc7ff49cdaa420c9e6c12e32e3993f7cdfec3', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/diagram-1-en.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '6e45a78dcb2e93265952b5d9d87f5ba980ed79b4', 'mainBlob': '6e45a78dcb2e93265952b5d9d87f5ba980ed79b4', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/diagram-1-ja.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '80a7f1124f4e0370752036db51d065ed99c07a39', 'mainBlob': '80a7f1124f4e0370752036db51d065ed99c07a39', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/diagram-1-ko.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '81fed3f47168fe6f090fd55a4a569d962050ba30', 'mainBlob': '81fed3f47168fe6f090fd55a4a569d962050ba30', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/diagram-1-zh-cn.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '6633185722790de617e832bb77b209c4d844cd3e', 'mainBlob': '6633185722790de617e832bb77b209c4d844cd3e', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/hero-en.jpg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '7f826a83e9b6bf5ea4e91f584cd60bd960431938', 'mainBlob': '7f826a83e9b6bf5ea4e91f584cd60bd960431938', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/hero-en.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '89e45e85e7bf93857da2c7b496ca69ac63b2ea9e', 'mainBlob': '89e45e85e7bf93857da2c7b496ca69ac63b2ea9e', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/hero-ja.jpg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'a8b12ab406afe4e928730e5ada8f827b2490bf9b', 'mainBlob': 'a8b12ab406afe4e928730e5ada8f827b2490bf9b', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/hero-ja.svg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'da640d30d527ff550698f0e28e971b0c243448d6', 'mainBlob': 'da640d30d527ff550698f0e28e971b0c243448d6', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'apps/web/public/guides/llms-txt-evaluation/hero-ko.jpg', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'ff5e09ab38617efe69a1f3d5ccf92046b856dd2f', 'mainBlob': 'ff5e09ab38617efe69a1f3d5ccf92046b856dd2f', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`。

- [ ] **Codex `codex/article-localization-source-edit-preservation` — 原scope完成，保留工作**。保留缺檔checkout、index signature、HEAD及歷史WITHHOLD/PASS收據；另行核對原session與缺檔來源，從已保全HEAD對帳需要復原的程式/文稿路徑。本輪不reset、不清目錄或釋出claims。
  - 核對 HEAD：`a80f6b5faef47a17c862e8a981d78f5f3b4cfd06`。
  - 任務：[2026-09-21-authorize-reviewed-source-corrections-in-localization](../../tasks/done/2026-09-21-authorize-reviewed-source-corrections-in-localization.md)（主幹 done）；原認領 codex-source-correction。
  - 任務：[2026-09-22-compare-deployed-localization-packs-by-validated](../../tasks/done/2026-09-22-compare-deployed-localization-packs-by-validated.md)（主幹 done）；原認領 codex-deployed-pack-guard。
  - 任務：[2026-09-22-preserve-reviewed-unselected-repository-locale-edits](../../tasks/done/2026-09-22-preserve-reviewed-unselected-repository-locale-edits.md)（主幹 done）；原認領 codex-source-preservation。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/article-localization-source-edit-preservation`；未提交路徑2507個；現存內容／缺檔與index signature分別保存。
  - 核對證據：原PR #652 CLOSED，但其工作 unchanged integrated into merged #654 d5f03e679bef2102e843426c42f045aef4ae08c0。逐一比較5個scoped程式／測試檔在#654 snapshot皆精確同blob；current main repository_preservation.py同blob，assembler/publisher/tests後來演進亦有歷史同blob。
  - 核對證據：main三原票全部DONE，完整preservation票保留舊WITHHOLD與修復：current HEAD必須等於baseline.repo_commit，tempGit A成功／emptyB拒絕回歸已做；126 passed/59 skipped、Ruff/check tasks記錄，並有#6549/9CI與guarded batch015保留repository edit而published zhTW v8未改、四missinglocaleimport/publish驗收。
  - 核對證據：fresh dirty2507是apps/api（含guides content與tests）、docs及舊任務／工具等tracked路徑全部工作目錄缺檔，exists=false且沒有現存檔案bytes；其中1473 apps/api/app、257 apps/api/tests。這不是2507未提交翻譯或程式差異，也不能憑缺檔猜此前誰清掉。
  - 核對證據：原baseline/source/locale published bytes仍是當時live值，reviewreceipt與staleHEAD防護必須保留。完成交付的正面證據不解除dirty checkout或原owner防護。
  - 核對證據：完成的歷史branch HEAD／原task版本與外部WITHHOLD/PASS／delivery收據需保全為archive；status只表示交付已被接替且可保全，不授權清除dirty/active checkout。
  - 續作路徑：`{'path': 'docs/article-localization/assemble_bundle.py', 'status': 'M', 'baseBlob': 'dab4a2589f398274d38b157ce9b6ae2cead7cf4d', 'branchBlob': '7f3d328edae609f6a5250ea6b1bfc8c3bd181a18', 'mainBlob': '19cef7894581ebf864bdb9d1383462d54d8cb2d9', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '6630449054e5ae0972c3208db0827057d335d495', 'ownMergeBlob': None}`, `{'path': 'docs/article-localization/publish_bundle.py', 'status': 'M', 'baseBlob': '1fdc212f9004a7d767e732f3a136af2636d41f43', 'branchBlob': '598c66a688e6ac8e872086443341b411692b9059', 'mainBlob': '4d2dd733e20be3902882f3d6c997cdd2f5d2a518', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '716bd5dc81cb2ebef51e338be5a2e6a201314226', 'ownMergeBlob': None}`, `{'path': 'docs/article-localization/repository_preservation.py', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '58aa0b18c294360717d6391d33c4ee5731bb74fd', 'mainBlob': '58aa0b18c294360717d6391d33c4ee5731bb74fd', 'matchesMain': True, 'exactAtOwnMerge': None, 'historicalMainCommit': 'd5f03e679bef2102e843426c42f045aef4ae08c0', 'ownMergeBlob': None}`, `{'path': 'docs/article-localization/test_assemble_bundle.py', 'status': 'M', 'baseBlob': '6ec3bab5c836a12afcfacdd62ab23cfdaabfd61b', 'branchBlob': '1a2542e9e2fcafb42d6a031ee0472a5f81359014', 'mainBlob': '45687efe5f802f5cf7a991d6bf79ac5253ff5a20', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '6630449054e5ae0972c3208db0827057d335d495', 'ownMergeBlob': None}`, `{'path': 'docs/article-localization/test_publish_bundle.py', 'status': 'M', 'baseBlob': 'b2e72eaf874a7c5debb77c45a0dee1659ff67360', 'branchBlob': '093ab8da16140cf2a8fb04763a0b3202f9fd877f', 'mainBlob': 'aa0cfd0feeddb54cc60a17315427ba2f4165ef2c', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '716bd5dc81cb2ebef51e338be5a2e6a201314226', 'ownMergeBlob': None}`, `{'path': 'tasks/done/2026-09-21-authorize-reviewed-source-corrections-in-localization.md', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '7e06a7d687b67f25d9d1244b2e5ff9f5367155a4', 'mainBlob': '544cdd9d95d42c091d83c0c232ec8516f794315a', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': 'cc019d260f82d31a706d5c95cad89c84cf10bca6', 'ownMergeBlob': None}`, `{'path': 'tasks/done/2026-09-22-compare-deployed-localization-packs-by-validated.md', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '8581260d39899186fa8c7c80237b56f13e6cbf99', 'mainBlob': '38ab574f30ba2301131a00f6584046372830eda1', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': 'cc019d260f82d31a706d5c95cad89c84cf10bca6', 'ownMergeBlob': None}`, `{'path': 'tasks/open/2026-09-21-authorize-reviewed-source-corrections-in-localization.md', 'status': 'D', 'baseBlob': 'fc0955f22f7ee7d8c3c3c0225073a0dbecba70ea', 'branchBlob': '0000000000000000000000000000000000000000', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': None, 'ownMergeBlob': None}`, `{'path': 'tasks/open/2026-09-22-compare-deployed-localization-packs-by-validated.md', 'status': 'D', 'baseBlob': '82b060b0b38fd4d546a80f92427635ffdfa87c58', 'branchBlob': '0000000000000000000000000000000000000000', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': None, 'ownMergeBlob': None}`, `{'path': 'tasks/open/2026-09-22-preserve-reviewed-unselected-repository-locale-edits.md', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'f80c71dfcde59d1afbb81f24735a78b35ab2074c', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': '9fafd4293506a264dfe54c3722cb2c2eac86b516', 'ownMergeBlob': None}`。

- [ ] **Codex `codex/batch003-qa-tasks` — 未完成**。保留clean batch003-qa-tasks工作目錄與原QA註記；把四繁中SVG英文helper缺件補成窄票，逐圖換繁中helper並驗桌機／手機，不改四語素材、不重發已公開全文。
  - 核對 HEAD：`3e072badac7c2a25e2d96ed4656536550cfb6feb`。
  - 待辦：原Batch003票只接續onsen四語＋SVG的fresh source/review/install/release與公開驗收；先消除其四篇已公開／舊發布未勾的記帳衝突。
  - 任務：[2026-10-11-localize-batch003-zh-tw-diagram-helpers](../../tasks/open/2026-10-11-localize-batch003-zh-tw-diagram-helpers.md)（主幹 本 PR open）。
  - 任務：[2026-09-20-five-language-article-batch-003](../../tasks/open/2026-09-20-five-language-article-batch-003.md)（主幹 open）。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/batch003-qa-tasks/travel_scanㄐ`；未提交路徑0個；現存內容／缺檔與index signature分別保存。
  - 核對證據：唯一unique提交3e072badac7c2a25e2d96ed4656536550cfb6feb只改原Batch003票，追加實際公開圖稿QA缺件，沒有新的translation code或pack；clean checkout不等於此QA已處理。
  - 核對證據：main原Batch003票OPEN，9/29正文已明載四非onsen篇五語公開且bodyhash與repo相符；onsen zhTW v8來源已修正，四target locales／SVG尚未落地。10/4清單仍有舊發布未完文字，與9/29已公開證據需分項對帳，不重發四篇也不重做onsen繁中修正。
  - 核對證據：本支新增的繁中圖稿QA註記未進main。直接讀frozen main四原文diagram-1.svg，仍有「A practical sequence」「Editorial diagram」以及Same party、Check receiver、Official booking、Choose station等英文輔助文字，正面證明此窄缺件尚在產品。
  - 核對證據：40 browser QA／80 screenshots的歷史引用在本支註記，是既有驗收材料，應保全再接續。onsen剩四語已在主票，與新的四繁中source SVG標籤修正分scope。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-localize-batch003-zh-tw-diagram-helpers。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'path': 'tasks/open/2026-09-20-five-language-article-batch-003.md', 'status': 'M', 'baseBlob': 'd60129077711aa6aa94f470aa57c6c0286283137', 'branchBlob': 'addb13640aea9022b2d7cb6e1748ec7b56fa6e73', 'mainBlob': '4f0ca26e9e15c30bf7f7152a4d70c8a23d9e2430', 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': None, 'ownMergeBlob': None}`。

### 影片、配音與漫劇（6）

- [ ] **Claude `claude/ai-terminology-video-series-c1754d` — 未完成**。保留92e3ae6完整四集來源；與實際final/media/owner approvals hash對帳
  - 核對 HEAD：`92e3ae6ba64b75243b6127da2c09d4b96470f0c5`。
  - 待辦：把12個source改動透過現在的rewrite母票逐集整合/再審，禁止直接重買已通過素材
  - 待辦：將3個main欠缺具體缺陷票持久化；season2 A26/A30引用hash另按shareddisposition票對帳
  - 任務：[2026-10-11-a-four-line-quote-card-loses](../../tasks/open/2026-10-11-a-four-line-quote-card-loses.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-a-slides-storyboard-whose-pictures-all](../../tasks/open/2026-10-11-a-slides-storyboard-whose-pictures-all.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-shot-prompts-put-the-look-first](../../tasks/open/2026-10-11-shot-prompts-put-the-look-first.md)（主幹 本 PR open）。
  - 任務：[2026-09-29-ai-terms-video-pilot](../../tasks/open/2026-09-29-ai-terms-video-pilot.md)（主幹 open）。
  - 任務：`2026-10-04-a-four-line-quote-card-loses`（主幹 absent）。
  - 任務：`2026-10-04-a-slides-storyboard-whose-pictures-all`（主幹 absent）。
  - 任務：`2026-10-04-produce-the-ai-terms-overview-episode`（主幹 absent）。
  - 任務：`2026-10-04-shot-prompts-put-the-look-first`（主幹 absent）。
  - 核對證據：三pilot文稿的原文字階段 #1006、overview #1188已main，但本ref的4個後續commits改12個source路徑（四集brief/claims/video）：style-first單subject/action prompts、實測tempo拆shot、語音修詞、quote3行、當日重新查來源。12個blob在main现況/歷史皆無，不是後续main改稿假未完成。
  - 核對證據：原task Notes實錄：四集12:48–13:31、11–20個過8秒shot拆到0，大綱/旁白自動核准，image-01 custompositive style/negative空白、owner全彩細描。這些code/source進度需入新稿並和實際media/sourcehash對帳；不是恢復舊paid生成。
  - 核對證據：main現有rewrite-ai-term-token / context-window / overview票指定保留來源；原overview製作與3個缺陷票只此ref，quote-height/nonblocking-storyboard/style-order經main source讀取確認仍有缺口，會持久化，不把其in-progress字樣當live session。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-a-four-line-quote-card-loses, 2026-10-11-a-slides-storyboard-whose-pictures-all, 2026-10-11-shot-prompts-put-the-look-first。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`docs/videos/ai-term-context-window/brief.md`, `docs/videos/ai-term-context-window/claims.md`, `docs/videos/ai-term-context-window/video.json`, `docs/videos/ai-term-retrieval-augmented-generation/brief.md`, `docs/videos/ai-term-retrieval-augmented-generation/claims.md`, `docs/videos/ai-term-retrieval-augmented-generation/video.json`, `docs/videos/ai-term-token/brief.md`, `docs/videos/ai-term-token/claims.md`, `docs/videos/ai-term-token/video.json`, `docs/videos/ai-terms-prompt-to-graph-engineering/brief.md`。

- [ ] **Claude `claude/ou-de-jianghu-e001-285512` — 未完成**。保持Claude生產會話/ref/worktree/media/claims原狀；root不接管、不STOP、不restart
  - 核對 HEAD：`22ee6f1338f11ce48c84c28631ff6f2d1cc489b4`。
  - 待辦：由既有Claude producer照最新封包/ledger/lease續A/B期仍未產鏡；本audit只保留124+11+3及7reference缺件證據
  - 待辦：補齊reference上傳管道與有限候選decision，不能重送a04-s021；對D溢出/鄰鏡接點與ASR疑字實聽後剪輯
  - 待辦：待全集cut/聲音/actualownerfinalQA與delivery收據，現在不結案
  - 任務：`2026-10-08-ou-de-jianghu-art-direction`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-external-look-import`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-visual-preproduction`（主幹 absent）。
  - 任務：`2026-10-08-animatic-title-gap-subtitle-boundary`（主幹 absent）。
  - 任務：`2026-10-08-integrate-external-look-import-duration-review`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-animation-reference`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-episode1-portraits`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-preflight-plan`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-scene-prop-design`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-supporting-looks`（主幹 absent）。
  - 任務：`2026-10-08-ou-de-jianghu-visual-handoff`（主幹 absent）。
  - 任務：`2026-10-08-validate-windows-stock-path-and-brightness`（主幹 absent）。
  - 保留工作目錄：`C:/Users/x8120/mokaair/.claude/worktrees/ou-de-jianghu-e001-285512`；未提交路徑0個；現存內容／缺檔與index signature分別保存。
  - 核對證據：使用者此輪明確「偶的江湖在claude還在製作」：硬userProtected，無刪除資格。clean checked-out不代表完工，現head22ee6f133已由38e062ada再進1commit，本輪 frozen最新20:53:57記packet10。
  - 核對證據：最新packet10真24firstframes+24影片及D tracks：22候選/2有限（a03-s067動作角色反了、a03-s069幾乎不動），paid1872點，B期3545，全域new_spent20040/26980；snapshot餘額41555。這是生成receipt，不是全集cut/ownerfinalacceptance。
  - 核對證據：A期剩7缺reference（a01-s001/002/003/004/006/007/008）；B期此次後124reference齊鏡未產、11鏡缺reference、3active鏡a03-s070/086/088無動作。a04-s021 generating84點仍無provider端取消入口，佔12-slot佇列一格，不得重送。
  - 核對證據：D轨仍provisional/needs listening與跨鏡overflow：a03-s089可用s090無台詞吸收，a05-s015用s016吸收；s067→s068、s069→s070、s024→s025等需現在cut對帳；畫面有限候選須原owner/take gate決定。123scope路徑/34authoredcommits尚未main，PR1388只是preproduction繼承內容open，不等于Claude最新生產已合。
  - 續作路徑：`.agents/skills/animation-production/SKILL.md`, `.agents/skills/animation-production/references/browser-production.md`, `.agents/skills/animation-production/references/in-app-browser-hailuo.md`, `.claude/skills/animation-production/SKILL.md`, `docs/videos/series-plans/ou-de-jianghu/visual-development/README.md`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/README.md`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/build-final-gallery.mjs`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/build-receipt.mjs`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/fan-independent-final-review.json`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/finalization-20261009.json`。

- [ ] **Claude `claude/video-batch-2` — 未完成**。保留85da5f2完整source/ref及外部media
  - 核對 HEAD：`85da5f2cbc06572e74fc1c6f0c3062880a9ffd83`。
  - 待辦：依main rewrite-ai-model-choice / rewrite-ai-agent-permissions / rewrite-gemini-student-offer等精確票作新版，不重開母製作scope
  - 待辦：對chatgpt-ads brief/claim時間與已產cut來源做對帳，source改動與舊owner approvals分清
  - 待辦：speech-rate欠缺票先對現有main pacing ticket，避免兩票互鎖
  - 任務：[2026-09-24-video-pilot-ai-model-choice](../../tasks/open/2026-09-24-video-pilot-ai-model-choice.md)（主幹 open）。
  - 任務：`2026-09-24-video-speaking-rate`（主幹 absent）。
  - 任務：`2026-09-25-video-ai-agent-permissions`（主幹 absent）。
  - 任務：`2026-09-25-video-chatgpt-ads-upgrade`（主幹 absent）。
  - 任務：`2026-09-25-video-gemini-student-offer`（主幹 absent）。
  - 任務：[2026-10-11-cute-explainer-prompts-pace-and-lint](../../tasks/open/2026-10-11-cute-explainer-prompts-pace-and-lint.md)（主幹 open）。
  - 核對證據：40個產品source blob無一在frozen main現況/歷史，且45 aggregate scope有4支 authored film scripts、4語i18n、實測聽寫、lexicon和5原票；確有未整合來源，不是只沒PR。
  - 核對證據：main最新blind-reading rewrite票明確Where its script is指origin/claude/video-batch-2。ai-model-choice未uploaded且核心需真實cascade/p95/錯答率實測；ai-agent-permissions/gemini-student-offer source已有YouTube cut記錄，rewrite仍與發布decision分開。chatgpt-ads有過期pricing/brief被官方推翻的舊校正。
  - 核對證據：來源票進度09/25僅代表當時旁白/CC產線，不能當live或全部film current done；下一步用保留source作新版rewrite基準，先核對實際已產cut/hash，不能直接合併舊未經現在教學規則審核的稿。
  - 續作路徑：`docs/videos/README.md`, `docs/videos/ai-agent-permissions/brief.md`, `docs/videos/ai-agent-permissions/claims.md`, `docs/videos/ai-agent-permissions/i18n/en.json`, `docs/videos/ai-agent-permissions/i18n/ja.json`, `docs/videos/ai-agent-permissions/i18n/ko.json`, `docs/videos/ai-agent-permissions/i18n/zh-CN.json`, `docs/videos/ai-agent-permissions/verify-1.md`, `docs/videos/ai-agent-permissions/verify-2.md`, `docs/videos/ai-agent-permissions/video.json`。

- [ ] **Claude `claude/youtube-language-manifest` — 原scope完成，保留工作**。保留 checked-out worktree/ref，待持有者收尾
  - 核對 HEAD：`3e61f790e542fda088f650fdf025e4b5522c2399`。
  - 待辦：向既有tidied-source票補原fixture/真實private-sync待驗證範圍，不再整包合舊splitmodule
  - 待辦：完整HEAD初稿可archive；不要因此稱 Studio已看見新語言
  - 任務：[2026-09-30-youtube-approved-languages-sync](../../tasks/done/2026-09-30-youtube-approved-languages-sync.md)（主幹 done）；原認領 claude-happy-carson。
  - 任務：`2026-10-06-bind-tidied-language-batches-and-prove`（主幹 absent）。
  - 保留工作目錄：`C:/Users/x8120/mokaair/.claude/worktrees/wf_3eff2890-671-8`；未提交路徑0個；現存內容／缺檔與index signature分別保存。
  - 核對證據：兩獨有commits原拆分language-source.mjs/fixture路徑確實不在main；但源功能被 #1361在 sync.mjs重新實作。逐讀當前bindLanguageSource：metadata+manifest綁 publish/final/script/branding/choice/files，拒絕改源/改choice/改byte，普通batch的 review/languages.json/hash/file上传一致，還新增narration一致、follows重送、ready dub附件與brand story兼容。
  - 核對證據：main原任務done及26-case真正producer→API pinned language-contract fixture寫明改寫替代，非只因done猜測。舊split module無需再merge；完整HEAD保留初稿。
  - 核對證據：原 bind-tidied-language-batches-and-prove 缺main，但其 deterministic tidied缺source proof已另main open 2026-10-07-a-tidied-video-s-skipped-language，普通producer後續實際deploy/resubmit/owner-approved private-sync仍須由發布/ownerscope驗收。
  - 核對證據：此ref是checked-out clean wf_3eff2890-671-8，按root guard保留worktree/ref，即使implementation scope已完成亦不刪。
  - 續作路徑：`apps/api/tests/fixtures/video_language_manifest_v1.json`, `apps/api/tests/test_video_youtube_language_package.py`, `docs/videos/APPROVED-LANGUAGE-PACKAGE.md`, `tasks/open/2026-09-30-youtube-approved-languages-sync.md`, `tasks/open/2026-10-06-bind-tidied-language-batches-and-prove.md`, `tools/video/review/language-source.mjs`, `tools/video/review/language-source.test.mjs`, `tools/video/review/sync.mjs`, `tools/video/review/sync.test.mjs`。

- [ ] **Claude `wf-fix-1342` — 原scope完成，保留工作**。保存完整HEAD與12份原工作diff，保持index/ownership
  - 核對 HEAD：`d98a1471eaedd070bc94e726b262b7bd65b87adb`。
  - 待辦：由持有者確認本地review patch對#1342/main的覆盖後收尾worktree；若發現新的差異再精確開票
  - 待辦：現階段root不刪ref/worktree、不把已完成review再次當新bug
  - 任務：[2026-10-06-a-failing-video-is-deferred](../../tasks/done/2026-10-06-a-failing-video-is-deferred.md)（主幹 done）；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-pictures-keep-best-after-prompt-fixes](../../tasks/done/2026-10-06-pictures-keep-best-after-prompt-fixes.md)（主幹 done）；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-an-owner-retry-resets-the-counter](../../tasks/done/2026-10-06-an-owner-retry-resets-the-counter.md)（主幹 done）；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-image-prompts-fit-the-chosen-image](../../tasks/done/2026-10-06-image-prompts-fit-the-chosen-image.md)（主幹 done）；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-a-stale-writer-receipt-looks-the](../../tasks/done/2026-10-06-a-stale-writer-receipt-looks-the.md)（主幹 done）；原認領 claude-fable-5-1-video-unstuck。
  - 保留工作目錄：`C:/Users/x8120/mokaair/.claude/worktrees/wf_42860dcf-e1a-1`；未提交路徑12個；現存內容／缺檔與index signature分別保存。
  - 核對證據：committed15 unique authored commits的original fixes已經 #1337/#1339/#1340/#1341/#1342 landed；5個原任務全main done。
  - 核對證據：dirty12是#1342第一輪review修補：defer limit6、unrecorded limit3、second-deferral報卡、Retry-After floor、STOP不算次數、job_gone保留journal、retry acknowledgment占busy、script-discussion resting gate。逐case對main：新增19個test，18個title字節一致，另1個同case已被第二輪增強加入跨回合deferred_until。
  - 核對證據：main相同源實作+第二輪更強busy/freshauto.json/shared-budget保護都在，並非只因oldtaskdone假完成；未發現dirty patch獨有尚未整合產品feature。不能重新merge此舊baseline覆蓋後续強化。
  - 核對證據：checked-out wf_42860dcf-e1a-1 dirty12，root硬保留；工作copy未整理仍須持有者協調，不能因上述完工結論刪dirty工作。
  - 續作路徑：`apps/api/app/video_automation/schemas.py`, `apps/api/app/video_automation/settings.py`, `apps/api/app/video_media/catalog.py`, `apps/api/tests/test_video_automation_settings.py`, `apps/api/tests/test_video_media_api.py`, `apps/api/tests/test_video_media_catalog.py`, `docs/videos/ILLUSTRATED.md`, `docs/videos/long-form/review.json`, `docs/videos/long-form/review.md`, `tasks/open/2026-10-06-a-failing-video-is-deferred.md`。

- [ ] **Codex `codex/stalled-videos-completion-20261008` — 未完成**。硬保留HEAD/dirty13/media/原票claims與STOP/UNKNOWN
  - 核對 HEAD：`b9940f18c1dfed8b493ceb9778df4c845728d4e2`。
  - 待辦：將3個localdone source修補與独立duration receipts作currentmain窄review；不拿oldfullfile覆蓋main後续paidguard
  - 待辦：先持久化5個缺main open follow-ups（以及pre-rebase parser票），避免paid保全只留chat
  - 待辦：剩餘影片用原目前producer收據、source/key/caps續作；audit不生成/付費/上傳/部署
  - 任務：[2026-10-11-stalled-production-video-completion](../../tasks/open/2026-10-11-stalled-production-video-completion.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-make-durable-polling-deadline-regression-deterministic](../../tasks/open/2026-10-11-make-durable-polling-deadline-regression-deterministic.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-retain-existing-guide-packs-in-imported](../../tasks/open/2026-10-11-retain-existing-guide-packs-in-imported.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-use-normal-caption-warnings-and-local](../../tasks/open/2026-10-11-use-normal-caption-warnings-and-local.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-video-stage-receipt-site-identity](../../tasks/open/2026-10-11-video-stage-receipt-site-identity.md)（主幹 本 PR open）。
  - 任務：[2026-10-11-integrate-retained-video-source-fixes](../../tasks/open/2026-10-11-integrate-retained-video-source-fixes.md)（主幹 本 PR open）。
  - 任務：`2026-10-08-make-durable-polling-deadline-regression-deterministic`（主幹 absent）。
  - 任務：`2026-10-08-retain-existing-guide-packs-in-imported`（主幹 absent）。
  - 任務：`2026-10-08-stalled-production-video-completion`（主幹 absent）。
  - 任務：`2026-10-08-use-normal-caption-warnings-and-local`（主幹 absent）。
  - 任務：`2026-10-08-video-audio-closing-particle-boundaries`（主幹 absent）。
  - 任務：`2026-10-08-video-branding-true-peak`（主幹 absent）。
  - 任務：`2026-10-08-video-qa-undecided-languages`（主幹 absent）。
  - 任務：`2026-10-09-video-stage-receipt-site-identity`（主幹 absent）。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/2a98/travel_scanㄐ`；未提交路徑13個；現存內容／缺檔與index signature分別保存。
  - 核對證據：checked-out2a98 HEAD b9940f18…未advance，但dirty13：3個tracked open票刪除、3個done票與recovery文/5個open票及environment目錄未tracked。完整snapshot不含secret配置值。noPR，7個產品文件blob無main/history命中。
  - 核對證據：actualcode包含4xoversampling/latencycompensated-2dB limiter、owner未選語言時QA只要求narration+zhTW、Mandarin punctuation前heard-only closing particle；main branding仍直接concat無limiter、QA仍readLanguages走舊要求、tts仍只有line末候選，三源修補確未整合。source任務已localdone≠main已landed。
  - 核對證據：local recovery最新2026-10-10：Travel EN/JA96check tracks/languageconsumer29附件合格，backend另記ID Ztg1vzKfLBM+LANG4cdb approved；這不獨立證明public visibility/ownerplayback。Embedding V6已closed3 canonicalrenameEPERM，197speech(124synthesis/10596chars+73ASR)、158EN WAV/72checkedlines保留；privateknown-answer恢復/15fault tests不是三語terminal。
  - 核對證據：root目前更晚thread證據為23/54音軌已published、31未完且Mods hold verified；此audit未查正式站，不把localOct10 checkpoint當currentliveness。原Mods STOP SHA f5bbf969d413bc7e8ef4419162459d3ea26d88a311493fd1eef9294e9d1cbea3保持。
  - 核對證據：5個補票又逐讀frozen main source：package-runtime僅copy tools/skill/4runner檔，未帶guides pack；localAdditions仍用caption problems.length==0拒warnings；最終caller仍submitSnapshot(api, remote,…); runReceiptStore仍record.site===site。poll regression已從40ms拉到25秒但仍用真實setTimeout，歷史224ms失敗不是已確認現況，應先核對是否只剩可選deterministic測試改進。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-stalled-production-video-completion, 2026-10-11-make-durable-polling-deadline-regression-deterministic, 2026-10-11-retain-existing-guide-packs-in-imported, 2026-10-11-use-normal-caption-warnings-and-local, 2026-10-11-video-stage-receipt-site-identity, 2026-10-11-integrate-retained-video-source-fixes。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`docs/videos/long-form/review.json`, `docs/videos/long-form/review.md`, `tasks/open/2026-10-08-video-audio-closing-particle-boundaries.md`, `tasks/open/2026-10-08-video-branding-true-peak.md`, `tasks/open/2026-10-08-video-qa-undecided-languages.md`, `tools/video/assemble/branding-smoke.mjs`, `tools/video/assemble/branding.mjs`, `tools/video/assemble/branding.test.mjs`, `tools/video/qa/cli.mjs`, `tools/video/qa/qa.test.mjs`。

### 新聞、審核與 PR 整合（7）

- [ ] **Codex `codex/content-review-resolution` — 未完成**。依新待辦 `2026-10-11-reconcile-retained-catalog-proof` 續作，原始分支与既有修改完整保留。
  - 核對 HEAD：`9cd24e2be787925be58eb55418c4d9b6333fa049`。
  - 待辦：Restore/consolidate task 2026-09-08-remaining-189-catalog-proof into the shared queue with the exact 181 keep_pending IDs from 2026-09-09-remaining-proof.json. First perform a fresh read-only per-ID status/audit reconciliation so already completed records are excluded; do not claim all 181 are still currently pending.
  - 待辦：For remaining IDs obtain only their recorded missing evidence: article original body/language or material transport/context facts; video actual narration/locale/place proof; merchant exact branch source, precise map identity and qualified durable-coordinate provenance. Retain genuine unavailable evidence as a recorded hold.
  - 待辦：Use a new dated finite manifest and normal authorized review path for newly supported decisions; preserve original applied manifests/audit history and integrate or archive the historical evidence tests separately. Keep this branch until the unique follow-up record and evidence package are durably reconciled.
  - 任務：[2026-10-11-reconcile-retained-catalog-proof](../../tasks/open/2026-10-11-reconcile-retained-catalog-proof.md)（主幹 本 PR open）。
  - 任務：`2026-09-08-content-review-resolution`（主幹 absent）。
  - 任務：`2026-09-08-remaining-189-catalog-proof`（主幹 absent）。
  - 核對證據：Commit 7c4a93e8 completed the bounded 255-item resolution operation: 36 approvals, 30 rejections, 189 holds; done task and detailed independent postflight are retained. Commit 9cd24e2b then researched all 189 and applied only eight new supported status decisions.
  - 核對證據：Full remaining-proof manifest explicitly has status applied_and_independently_verified and declares publication adjudication incomplete: 181 held records comprise 154 merchants, 22 articles and 5 videos. Its separate read-only verification at 2026-09-09T00:32:02Z records 189 receipts, 6 guide and 2 merchant normal audits, unchanged 154 held merchants/27 held guides and preserved 817 older audits; runtime f752ce43/schema0064.
  - 核對證據：Local tasks/open/2026-09-08-remaining-189-catalog-proof.md still has an explicit unchecked final proof-resolution item; neither original task ID has a matching open/done main ticket. The later PR #408 public reservation review is a different cohort and does not adjudicate these original article/video bodies, locale, transport or exact merchant durable-coordinate evidence.
  - 核對證據：181 is the historical sealed held set, not a verified current pending count. No exact per-ID successor adjudication/completion receipt for this set was found in fresh main. Preserving the unique manifest/tests and restoring a shared follow-up is still required.
  - 續作路徑：`{'path': 'apps/api/tests/test_catalog_content_review_resolution.py', 'status': 'A', 'branchBlob': '07e132aa19d442dec6c72a01fdfa6be460dda25e', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'apps/api/tests/test_catalog_remaining_proof_report.py', 'status': 'A', 'branchBlob': '1cd294c9116242c20dbcf66d31571888798ec71c', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'docs/catalog-content-reviews/2026-09-09-remaining-proof-result.md', 'status': 'A', 'branchBlob': '59958cedaded02fc0593c26a6e83761f7d8a388b', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'docs/catalog-content-reviews/2026-09-09-remaining-proof.json', 'status': 'A', 'branchBlob': '78708b045afd52f3eb7d53c83b3b133219ea3594', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'docs/catalog-content-reviews/2026-09-09-resolution-result.md', 'status': 'A', 'branchBlob': 'ae9681313e2376439b830bc5b7452f95bcc35509', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'docs/catalog-content-reviews/2026-09-09-resolution.json', 'status': 'A', 'branchBlob': 'bb47281dc63d7f1bf37e92a372bfc703292d088b', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'tasks/BOARD.md', 'status': 'M', 'branchBlob': '6525bfe07d75dd988451843bce194c94186db21f', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'tasks/done/2026-09-08-content-review-resolution.md', 'status': 'A', 'branchBlob': '119c724b44112caf004f870302130461c86d2189', 'historicalMainCommit': None, 'producerPR': None}`, `{'path': 'tasks/open/2026-09-08-remaining-189-catalog-proof.md', 'status': 'A', 'branchBlob': '6b1a669a93b035b172dd6e281ffeb639a25e720f', 'historicalMainCommit': None, 'producerPR': None}`。

- [ ] **Codex `codex/news-publication-deploy-receipt` — 未完成**。恢復並縮窄missing verifier追蹤票，先離線重現兩契約問題；歷史部署receipt封存、publication只沿現有共享票讀新收據。
  - 核對 HEAD：`380e463ae785ac98b66eb4fc52dd13d9a6166549`。
  - 任務：[2026-10-11-restore-deploy-verifier-freshness-exit](../../tasks/open/2026-10-11-restore-deploy-verifier-freshness-exit.md)（主幹 本 PR open）。
  - 任務：`2026-10-04-deploy-verifier-freshness-exit`（主幹 absent）。
  - 任務：[2026-10-04-news-publication-recovery](../../tasks/open/2026-10-04-news-publication-recovery.md)（主幹 open）。
  - 任務：[2026-10-04-news-publish-retired-diagram](../../tasks/done/2026-10-04-news-publish-retired-diagram.md)（主幹 done）；原認領 codex-gpt-6-news-recovery。
  - 核對證據：只有兩個獨有commit、三條文件/任務路徑；#1201 e9942相關Oct4 forced-redeploy/13服務與新聞恢復是已完成日期收據。後續main Notes已記錄Oct6三故事五語發布，不應把旧39 cohort機械稱current pending。
  - 核對證據：真正未共享的是2026-10-04-deploy-verifier-freshness-exit。fresh main host-verify.sh:279仍StartedAt>=head_ct，而不是與其餘check統一已驗證重建cutoff；335–336只有TOTAL及echo，不以FAIL_N退出非零。#1245後續修正沒有完成此契約。
  - 核對證據：新聞publication recovery現有main open票保存真實剩餘owner/內容gate；本branch未實作verifier修正。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-deploy-verifier-freshness-exit。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'A', 'path': 'docs/news-automation-recovery-2026-10-04.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-10-04-deploy-verifier-freshness-exit.md', 'oldPath': None}`, `{'status': 'M', 'path': 'tasks/open/2026-10-04-news-publication-recovery.md', 'oldPath': None}`。

- [ ] **Codex `codex/news-recovery-20261010` — 未完成**。保全6f71的13dirty路徑、stage簽名/未追蹤原稿/最新收據，核對原owner後移交successor recovery分支。
  - 核對 HEAD：`1b7be83e6cc65a308e2c21b785c7e37c8ac966f7`。
  - 待辦：只沿canonical主票及現有audited category/source/claim/duplicate/UI票確認當前原route與final judge；不要以舊cohort數量當current pending。
  - 待辦：STOP/retry顯示原稿先查同義票/影片分支後恢復缺失共享追蹤。
  - 任務：[2026-10-11-video-held-retry-status](../../tasks/open/2026-10-11-video-held-retry-status.md)（主幹 本 PR open）。
  - 任務：`2026-10-05-video-held-retry-status`（主幹 absent）。
  - 任務：[2026-10-06-news-judge-translations-only-rerun](../../tasks/open/2026-10-06-news-judge-translations-only-rerun.md)（主幹 open）。
  - 任務：[2026-10-07-resolve-current-news-review-and-redraft](../../tasks/open/2026-10-07-resolve-current-news-review-and-redraft.md)（主幹 open）；原認領 codex-news-backlog-review。
  - 任務：[2026-10-10-add-audited-held-news-bundle-ingestion](../../tasks/done/2026-10-10-add-audited-held-news-bundle-ingestion.md)（主幹 done）；原認領 codex-news-held-bundle-ingestion。
  - 任務：[2026-10-10-add-audited-held-news-category-correction](../../tasks/open/2026-10-10-add-audited-held-news-category-correction.md)（主幹 open）。
  - 任務：[2026-10-10-add-audited-repair-for-legacy-navigation](../../tasks/done/2026-10-10-add-audited-repair-for-legacy-navigation.md)（主幹 done）；原認領 codex-news-recovery-6f71。
  - 任務：[2026-10-10-add-audited-source-extension-for-held](../../tasks/open/2026-10-10-add-audited-source-extension-for-held.md)（主幹 open）。
  - 任務：[2026-10-10-correct-published-bitmine-sole-outlet-attribution](../../tasks/open/2026-10-10-correct-published-bitmine-sole-outlet-attribution.md)（主幹 open）。
  - 任務：[2026-10-10-distinguish-reported-and-negated-trading-verbs](../../tasks/open/2026-10-10-distinguish-reported-and-negated-trading-verbs.md)（主幹 open）。
  - 任務：[2026-10-10-exclude-system-topic-navigation-from-news](../../tasks/done/2026-10-10-exclude-system-topic-navigation-from-news.md)（主幹 done）；原認領 codex-news-recovery-6f71。
  - 任務：[2026-10-10-news-disclaimer-correction-loop](../../tasks/done/2026-10-10-news-disclaimer-correction-loop.md)（主幹 done）；原認領 codex-news-recovery-6f71。
  - 任務：[2026-10-10-news-held-cohort-recovery](../../tasks/open/2026-10-10-news-held-cohort-recovery.md)（主幹 open）；原認領 codex-news-recovery-6f71。
  - 任務：[2026-10-10-preserve-and-recover-translated-news-before](../../tasks/open/2026-10-10-preserve-and-recover-translated-news-before.md)（主幹 open）。
  - 任務：[2026-10-10-track-ledger-duplicate-coverage-gap](../../tasks/open/2026-10-10-track-ledger-duplicate-coverage-gap.md)（主幹 open）。
  - 任務：[2026-10-11-add-audited-minor-corrections-for-published](../../tasks/open/2026-10-11-add-audited-minor-corrections-for-published.md)（主幹 open）。
  - 任務：[2026-10-11-show-final-judge-holds-on-news](../../tasks/open/2026-10-11-show-final-judge-holds-on-news.md)（主幹 open）。
  - 任務：[2026-10-11-translate-held-news-ingestion-error-messages](../../tasks/done/2026-10-11-translate-held-news-ingestion-error-messages.md)（主幹 done）；原認領 codex-news-held-error-copy。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/6f71/travel_scanㄐ`；未提交路徑13個；現存內容／缺檔與index signature分別保存。
  - 核對證據：#1411已merged的五個程式/測試路徑與原branch blob精確相同；舊程式工作包括disclaimer迴圈及system navigation排除已done，不能再當未整合。
  - 核對證據：canonical recovery主票main仍in-progress、owner codex-news-recovery-6f71，branch已更新為codex/news-recovery-followup-20261011。main後續收據含原208 cohort 2026-10-11T11:32:38Z 133published/46manual/19redraft/1failed/6duplicate/3rejected，只是該時刻固定cohort，不是這次production census。
  - 核對證據：原checkout 6f71有13未提交路徑；其中bundle-ingestion與error-copy done、legacy-navigation task在main已有done successor，其他新聞同ID現有open票。保留source/history/claims及draft/producer-gate分別證據，不重播原cohort或釋放claim。
  - 核對證據：另有scope外untracked video-held-retry-status原稿main absent，需要保存並與影片owner/audit對帳；不是擴大news recovery執行範圍。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-video-held-retry-status。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'M', 'path': 'apps/api/app/news_automation/ai.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/news_automation/policy.py', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/api/tests/test_news_ai.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/tests/test_news_pipeline.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/tests/test_news_policy.py', 'oldPath': None}`, `{'status': 'A', 'path': 'docs/news-held-cohort-recovery-2026-10-10.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-10-10-exclude-system-topic-navigation-from-news.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-10-10-news-disclaimer-correction-loop.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-10-10-add-audited-source-extension-for-held.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-10-10-distinguish-reported-and-negated-trading-verbs.md', 'oldPath': None}`。

- [ ] **Codex `codex/pr900-ci-investigation` — 未完成**。恢復原merchant-style診斷共享追蹤，把已merged tracing步驟標成完成，只保留具體case根因與desktop/mobile驗證；先確認現在fixture是否仍適用。
  - 核對 HEAD：`87711b4cf7bb3e03eb17f7419e8054a82ab79f2b`。
  - 任務：[2026-10-11-restore-merchant-style-first-failure-investigation](../../tasks/open/2026-10-11-restore-merchant-style-first-failure-investigation.md)（主幹 本 PR open）。
  - 任務：`2026-09-28-diagnose-merchant-style-browser-timeout-with`（主幹 absent）。
  - 任務：[2026-09-28-localize-newsletter-content-guides-batch035-pair](../../tasks/done/2026-09-28-localize-newsletter-content-guides-batch035-pair.md)（主幹 done）；原認領 codex-p1-audit。
  - 核對證據：#900 merged的27非task產品路徑全部精確匹配branch；newsletter pairB主票main done，不存在內容未整合。
  - 核對證據：局部未共享診斷票記錄required job108879586343在Japanese dark merchant-style filter merchant-styles.spec.ts:54空URL與30秒timeout，原archive無trace/DOM，600MiB local build未完成，passing rerun不證明cause。
  - 核對證據：#884 first-failure retain-on-failure/unique artifact設施已main landed，這張票最初capture設施步驟可對帳已滿足；仍沒有此merchant-style失敗根因/修正的結案證據。現有discovery screenshot票是另一失敗，不同義。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-merchant-style-first-failure-investigation。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'M', 'path': 'apps/api/app/guides/content/content-marketing-calendar.json', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/guides/content/kit-newsletter-setup.json', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/diagram-1-en.svg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/diagram-1-ja.svg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/diagram-1-ko.svg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/diagram-1-zh-cn.svg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/hero-en.jpg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/hero-en.svg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/hero-ja.jpg', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/web/public/guides/content-marketing-calendar/hero-ja.svg', 'oldPath': None}`。

- [ ] **Codex `codex/pr917-dedup-order` — 未完成**。恢復單一窄shared admission-order票，只移植當前主線仍缺的duplicates.py與對應四回歸；fake judge/SQLite驗證，不重播舊cohort/付費router。
  - 核對 HEAD：`af3a18161792bc3667ace03e513d5ade9b634d8a`。
  - 任務：[2026-10-11-restore-news-dedup-admission-order](../../tasks/open/2026-10-11-restore-news-dedup-admission-order.md)（主幹 本 PR open）。
  - 任務：`2026-09-28-pr917-dedup-admission-order`（主幹 absent）。
  - 任務：[2026-09-28-run-news-candidates-on-a-pool](../../tasks/done/2026-09-28-run-news-candidates-on-a-pool.md)（主幹 done）；原認領 claude-opus-5-5。
  - 核對證據：#917 worker-pool feature已merged，但最後af3a181的admission-order局部防護與四回歸没有merged producer/history正面匹配。
  - 核對證據：fresh main duplicates.py:65–75仍查所有同vertical in-flight KNOWN_STATUSES，按created_at降序limit30；不存在processing_started_at/created_at入場比較/UUID平手與先活躍後裁切。test_overlapping_same_story_checks_leave_one_candidate_to_draft亦不在fresh main。
  - 核對證據：原done receipt標明修前兩worker互相duplicate或都draft、修後0/31歷史×claim平手四回歸通過；本機done只是準備完成，不等於上主線。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-news-dedup-admission-order。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'M', 'path': '.agents/skills/prod-host-ops/references/news-ops.md', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/config.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/news_automation/duplicates.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/news_automation/worker.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/tests/test_news_pipeline.py', 'oldPath': None}`, `{'status': 'M', 'path': 'docs/news-automation.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-09-28-pr917-dedup-admission-order.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-09-28-run-news-candidates-on-a-pool.md', 'oldPath': None}`。

- [ ] **Codex `codex/pr921-tidy-metadata-current` — 未完成**。與pr921-tidy-metadata-guard共用同一新追蹤票；保留pr-merge-watch全部17dirty與stage签名/未追蹤原稿。
  - 核對 HEAD：`a89cfa65ef518198b4b6f641148519431df4f6ae`。
  - 待辦：對當前main套最小missing-entry hold回歸，避免拿本地done標誌當merged；不執行實際素材清理。
  - 任務：[2026-10-11-restore-tidy-capped-list-retention-guard](../../tasks/open/2026-10-11-restore-tidy-capped-list-retention-guard.md)（主幹 本 PR open）。
  - 任務：[2026-09-24-video-youtube-sync](../../tasks/done/2026-09-24-video-youtube-sync.md)（主幹 done）；原認領 claude-opus-5-5-youtube-link。
  - 任務：[2026-09-25-video-auto-orchestrator-one-command-that](../../tasks/done/2026-09-25-video-auto-orchestrator-one-command-that.md)（主幹 done）；原認領 claude-opus-5-5。
  - 任務：[2026-09-26-video-drama-look-keyframes](../../tasks/done/2026-09-26-video-drama-look-keyframes.md)（主幹 done）；原認領 claude-fable-5-1-video-drama。
  - 任務：[2026-09-26-video-dubs-worker](../../tasks/done/2026-09-26-video-dubs-worker.md)（主幹 done）；原認領 claude-fable-5-1-video-languages。
  - 任務：[2026-09-26-video-hands-off-qa](../../tasks/done/2026-09-26-video-hands-off-qa.md)（主幹 done）；原認領 claude-fable-5-1-video-qa。
  - 任務：[2026-09-27-video-drama-room-skill-docs](../../tasks/done/2026-09-27-video-drama-room-skill-docs.md)（主幹 done）；原認領 claude-fable-5-1-video-languages。
  - 任務：[2026-09-27-video-drama-room-worker](../../tasks/done/2026-09-27-video-drama-room-worker.md)（主幹 done）；原認領 codex-p1-audit。
  - 任務：[2026-09-27-video-split-settings-worker](../../tasks/done/2026-09-27-video-split-settings-worker.md)（主幹 done）；原認領 codex-p1-audit。
  - 任務：[2026-09-28-guard-automatic-shorts-sync-against-changed](../../tasks/done/2026-09-28-guard-automatic-shorts-sync-against-changed.md)（主幹 done）；原認領 codex-pr905-schedule-guard。
  - 任務：`2026-09-28-pr906-main-integration`（主幹 absent）。
  - 任務：`2026-09-28-pr921-tidy-metadata-guard`（主幹 absent）。
  - 任務：[2026-09-28-video-shorts-youtube-auto](../../tasks/done/2026-09-28-video-shorts-youtube-auto.md)（主幹 done）；原認領 claude-fable-5-1-shorts。
  - 任務：[2026-09-28-video-story-tidy-finished](../../tasks/done/2026-09-28-video-story-tidy-finished.md)（主幹 done）；原認領 claude-opus-5-5-video-story-tidy。
  - 任務：[2026-09-28-video-story-worker](../../tasks/done/2026-09-28-video-story-worker.md)（主幹 done）；原認領 claude-opus-5-5-video-story-worker。
  - 任務：[2026-09-28-video-tidied-late-languages](../../tasks/done/2026-09-28-video-tidied-late-languages.md)（主幹 done）；原認領 claude-opus-5-5-tidied-languages。
  - 保留工作目錄：`C:/Users/x8120/.codex/worktrees/pr-merge-watch/travel_scanㄐ`；未提交路徑17個；現存內容／缺檔與index signature分別保存。
  - 核對證據：#921原tidy feature merged，四個非taskpath精確producer相同；最後a89cfa65包含局部missing-site-entry guard，但fresh main tidy.mjs:238–241仍latest200漏列就site=null並使用本地舊approval。
  - 核對證據：fresh main新pending/language/retry holds只能處理有site-entry者，沒有解決列表漏列時語系/排程未知仍可清理。local done guard receipt absentmain，不宣称已landed。
  - 核對證據：checkout pr-merge-watch有17dirty路徑，14個source/docs staged/2個done-task staged及rename、另untracked pr906 integration；主要是舊#905 source/guard準備稿，#916 replacement已承接功能，#925已解決pr906衝突。仍須完整保存stage/working bytes後由owner決定處置，不能reset/abort。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-tidy-capped-list-retention-guard。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'M', 'path': 'docs/videos/AUTOMATION.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-09-28-pr921-tidy-metadata-guard.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-09-28-video-story-tidy-finished.md', 'oldPath': None}`, `{'status': 'D', 'path': 'tasks/open/2026-09-28-video-story-tidy-finished.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-09-28-video-tidied-late-languages.md', 'oldPath': None}`, `{'status': 'M', 'path': 'tools/video/automation/cli.mjs', 'oldPath': None}`, `{'status': 'A', 'path': 'tools/video/automation/cli.test.mjs', 'oldPath': None}`, `{'status': 'A', 'path': 'tools/video/automation/tidy.mjs', 'oldPath': None}`, `{'status': 'A', 'path': 'tools/video/automation/tidy.test.mjs', 'oldPath': None}`, `{'status': 'M', 'path': 'tools/video/cli.mjs', 'oldPath': None}`。

- [ ] **Codex `codex/pr921-tidy-metadata-guard` — 未完成**。連到同一restore-tidy-capped-list-retention-guard票，保存此較早guard與當前branch差異；只整合缺失hold與必要回歸。
  - 核對 HEAD：`1c3c08a80ca3e7ba7015d2d0da9510c4adbf913e`。
  - 任務：[2026-10-11-restore-tidy-capped-list-retention-guard](../../tasks/open/2026-10-11-restore-tidy-capped-list-retention-guard.md)（主幹 本 PR open）。
  - 任務：[2026-09-24-video-youtube-sync](../../tasks/done/2026-09-24-video-youtube-sync.md)（主幹 done）；原認領 claude-opus-5-5-youtube-link。
  - 任務：[2026-09-25-video-auto-orchestrator-one-command-that](../../tasks/done/2026-09-25-video-auto-orchestrator-one-command-that.md)（主幹 done）；原認領 claude-opus-5-5。
  - 任務：[2026-09-26-video-drama-look-keyframes](../../tasks/done/2026-09-26-video-drama-look-keyframes.md)（主幹 done）；原認領 claude-fable-5-1-video-drama。
  - 任務：[2026-09-26-video-dubs-worker](../../tasks/done/2026-09-26-video-dubs-worker.md)（主幹 done）；原認領 claude-fable-5-1-video-languages。
  - 任務：[2026-09-26-video-hands-off-qa](../../tasks/done/2026-09-26-video-hands-off-qa.md)（主幹 done）；原認領 claude-fable-5-1-video-qa。
  - 任務：[2026-09-27-video-drama-room-skill-docs](../../tasks/done/2026-09-27-video-drama-room-skill-docs.md)（主幹 done）；原認領 claude-fable-5-1-video-languages。
  - 任務：[2026-09-27-video-drama-room-worker](../../tasks/done/2026-09-27-video-drama-room-worker.md)（主幹 done）；原認領 codex-p1-audit。
  - 任務：[2026-09-27-video-split-settings-worker](../../tasks/done/2026-09-27-video-split-settings-worker.md)（主幹 done）；原認領 codex-p1-audit。
  - 任務：`2026-09-28-pr921-tidy-metadata-guard`（主幹 absent）。
  - 任務：[2026-09-28-video-story-tidy-finished](../../tasks/done/2026-09-28-video-story-tidy-finished.md)（主幹 done）；原認領 claude-opus-5-5-video-story-tidy。
  - 任務：[2026-09-28-video-story-worker](../../tasks/done/2026-09-28-video-story-worker.md)（主幹 done）；原認領 claude-opus-5-5-video-story-worker。
  - 任務：[2026-09-28-video-tidied-late-languages](../../tasks/done/2026-09-28-video-tidied-late-languages.md)（主幹 done）；原認領 claude-opus-5-5-tidied-languages。
  - 核對證據：同一#921 merged feature與current branch同一未落地缺口；唯一局部guard要求listed.get(slug)不存在時hold，與fresh main site=null/舊approval fallback不同。
  - 核對證據：原回歸涵蓋capped200 missing entry、working dubs、future publish且保留media；own local done receipt未共享，內容尚需選與current main相容版本，不能與current branch各開一張票。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-tidy-capped-list-retention-guard。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'M', 'path': 'docs/videos/AUTOMATION.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-09-28-pr921-tidy-metadata-guard.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-09-28-video-story-tidy-finished.md', 'oldPath': None}`, `{'status': 'D', 'path': 'tasks/open/2026-09-28-video-story-tidy-finished.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-09-28-video-tidied-late-languages.md', 'oldPath': None}`, `{'status': 'M', 'path': 'tools/video/automation/cli.mjs', 'oldPath': None}`, `{'status': 'A', 'path': 'tools/video/automation/cli.test.mjs', 'oldPath': None}`, `{'status': 'A', 'path': 'tools/video/automation/tidy.mjs', 'oldPath': None}`, `{'status': 'A', 'path': 'tools/video/automation/tidy.test.mjs', 'oldPath': None}`, `{'status': 'M', 'path': 'tools/video/cli.mjs', 'oldPath': None}`。

### 網站、後台、資料與其他修補（9）

- [ ] **Codex `codex/codex-learning-complete` — 未完成**。接 existing 2026-09-14-codex-learning-series 唯一未勾項，逐03/10/04/11/23核對已有產品UI材料，列出缺少的具體操作／平台／版本，再於具備owner帳號／裝置條件時補證據及五語圖文review；保留不適用／未測標示與歷史拒絕。
  - 核對 HEAD：`7c9c6652ccc9c43f21abc832f9da98b80092027b`。
  - 待辦：不重跑已保存全文終審、305語言發布／部署，不重新claim已結案depth票；本輪不操作產品帳號或繞過既有policy拒絕。
  - 任務：[2026-09-14-claude-code-tutorial-center](../../tasks/done/2026-09-14-claude-code-tutorial-center.md)（主幹 done）；原認領 codex-claude-tutorials。
  - 任務：[2026-09-14-codex-upstream-integration](../../tasks/done/2026-09-14-codex-upstream-integration.md)（主幹 done）；原認領 codex-upstream-integration-fc2e。
  - 任務：[2026-09-14-codex-depth-content](../../tasks/done/2026-09-14-codex-depth-content.md)（主幹 done）。
  - 任務：[2026-09-14-codex-depth-plan-alignment](../../tasks/done/2026-09-14-codex-depth-plan-alignment.md)（主幹 done）；原認領 gpt-6。
  - 任務：[2026-09-14-codex-learning-series](../../tasks/open/2026-09-14-codex-learning-series.md)（主幹 open）。
  - 核對證據：所有779個產品檔：777與自身merged PR #525 ecf6fbc50c0f94cb73365b4b588412dbf09c9da7 精確同blob。剩life/page與article-page已逐patch讀取：差異為PR整合保留新版Gemini可見投影與guideArticle structured-data，舊分支是較早共用程式；不是Codex文稿尚未落地。61pack在#525 parsed diff皆0。
  - 核對證據：main originalseries最新9/20更新明確取代歷史0/60、policy預覽限制、未PR/未發布文字：#578 26583af5681b19b963c0a5e701d4600f61151ed7＋#583 b0dfcf128646c90fe5e5af66da5f3ae9c10b5bf7 已merged，60篇五語全文終審＋總目錄305文件公開，6532eaa部署及公開browser驗收。文章、練習包、全文終審與發布不重開。
  - 核對證據：depth-content已done是重複票closure，正文精確將唯一真正欠項移交回原codex-learning-series：五篇代表教學的Codex產品介面實際操作證據及圖文終審／平台版本日期／未測範圍。這是原series同scope的驗收欠項，非其他scope偶然open；目前本輪未找到完成此UI證據的替代receipt。
  - 核對證據：保留原policy拒絕診斷／未實測裝置界線；原始拒絕來源未確認的記錄不能改成已驗。下一步應從current main既有系列票與已發布版本補UI證據，不能重新生成60篇或回寫兩份舊共用元件。
  - 續作路徑：`{'path': 'apps/api/app/guides/content/codex-account-usage.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'a698d744c621c127021a94f85ed09f7679e8351b', 'mainBlob': 'a2308aca03421f183aa5be80767e1c04387fc9f4', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': 'a698d744c621c127021a94f85ed09f7679e8351b'}`, `{'path': 'apps/api/app/guides/content/codex-agents-md-scopes.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'f6941078fb121da0b816024ee402d3c2baf69e81', 'mainBlob': '45d5f1c59d3d4fe80b23afd0b77b6b34ae3320d5', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': 'f6941078fb121da0b816024ee402d3c2baf69e81'}`, `{'path': 'apps/api/app/guides/content/codex-agents-md.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '6155fc2826782a94330df84318459d881d4fb8e9', 'mainBlob': 'db84887410a687bd409c0f5250ab8821919eff0e', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': '6155fc2826782a94330df84318459d881d4fb8e9'}`, `{'path': 'apps/api/app/guides/content/codex-automation-recovery.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '3e1c50d59276297ec7301e0cc314b1cd8b2e2a7e', 'mainBlob': '56ce91754cb25e43f0af4f92c52605285300f431', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': '3e1c50d59276297ec7301e0cc314b1cd8b2e2a7e'}`, `{'path': 'apps/api/app/guides/content/codex-automations.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '867ad1402f1c33b1df20ad3764e41ef58ab43cf2', 'mainBlob': '9cb1cbf3fca5e9c97b3acf5b66046aa38b846aa5', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': '867ad1402f1c33b1df20ad3764e41ef58ab43cf2'}`, `{'path': 'apps/api/app/guides/content/codex-beginner-guide.json', 'status': 'M', 'baseBlob': 'ec30de94c03aad2017059bf265d93cbb9cc7be01', 'branchBlob': 'f30aa374fe8cce51b2022d6c6b9309a205647a28', 'mainBlob': 'e766ee300ab6fe6d3bf5513fc1cdc3a8df380239', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': 'f30aa374fe8cce51b2022d6c6b9309a205647a28'}`, `{'path': 'apps/api/app/guides/content/codex-browser-images.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '4a909eabf7bf62452cbb94d527b908d32fce118d', 'mainBlob': 'd53f26dec2772449acb641fc424eeb36a8d21309', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': '4a909eabf7bf62452cbb94d527b908d32fce118d'}`, `{'path': 'apps/api/app/guides/content/codex-ci-workflows.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'ec6e66f5a6da22475275dc73db2f8e75c145f206', 'mainBlob': '40675df44dbd8ee77106875164b42e85ca18550d', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': 'ec6e66f5a6da22475275dc73db2f8e75c145f206'}`, `{'path': 'apps/api/app/guides/content/codex-cli-getting-started.json', 'status': 'M', 'baseBlob': 'c70377cb80e4d64461c9943cbb27e64d5b1c8864', 'branchBlob': '2c060ad3c447d7e23b72f5f4f37a58fbe9ac2f63', 'mainBlob': 'bdb5a2e711a129c7a32c2c9f6e9946e14c13d3ea', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': '2c060ad3c447d7e23b72f5f4f37a58fbe9ac2f63'}`, `{'path': 'apps/api/app/guides/content/codex-cli-linux-wsl.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '75dfd845baca50ab9e08ffe30569fe68312b57b1', 'mainBlob': '0c0d638d51b9aff114f482dd3d955e8da1aa43b7', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '930100f3a9a81f76971126b4f755370b1d81dac7', 'ownMergeBlob': '75dfd845baca50ab9e08ffe30569fe68312b57b1'}`。

- [ ] **Codex `codex/country-foods-map-links` — 未完成**。依新待辦 `2026-10-11-preserve-country-foods-formatting` 續作，原始分支与既有修改完整保留。
  - 核對 HEAD：`a8736021c98f38a71e5f57555766d4cb86cc893e`。
  - 待辦：Keep the checked-out branch/worktree. Preserve the exact17-file uncommitted patch and bytes; record it as formatting-only using catalog-semantic-proofs.json workingASTEquivalent. Reconcile owner intent before deciding whether to retain or deliberately integrate these formatting edits. Do not reset, delete or treat product completion as worktree ownership release.
  - 任務：[2026-10-11-preserve-country-foods-formatting](../../tasks/open/2026-10-11-preserve-country-foods-formatting.md)（主幹 本 PR open）。
  - 保留工作目錄：`C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-foods-maps`；未提交路徑 17 個，狀態及檔案 SHA-256 已比對確認未變。
  - 核對證據：Producer PR #56 on replacement branch codex/country-foods-map-links-pr merged as 803b84601340d024fcdfe4fb326e086aa2a4e9c3, confirmed ancestor of frozen fresh main 73c84ca7. Of 63 product paths, 57 are exact branch blobs at that merge; foods/service.py has a positive main-history match and equivalent create-only initialization after upstream integration.
  - 核對證據：Unmatched old migration 0020_food_catalog.py is positively replaced by PR #56 migration 0022_food_catalog.py. Python AST comparison proves both entire upgrade/downgrade bodies exactly equal; only revision/down_revision chain metadata changed to follow itinerary system slots and hotspot AI search. test_schema.py explicitly moves expected head to0022 and checks0020/0021 are no longer heads.
  - 核對證據：The models and itinerary/router differences against PR #56 are upstream system-slot/schedule/AI additions rather than missing food changes; food catalog, map-link UI, API and focused food tests are already present in the merged producer scope.
  - 核對證據：Cleanup remains protected: checkout C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-foods-maps has17 uncommitted Python paths. Full dirty diff was read; AST comparison of HEAD versus working bytes proves all17 are formatting-only, but the user/root explicitly require these bytes be preserved and disposition tracked.
  - 續作路徑：`{'path': 'apps/api/app/foods/__init__.py', 'status': 'A', 'branchBlob': 'a96f5d9bb885ad0906edb07a048e98542d3070b6', 'historicalMainCommit': '8ce43a66dd34dc07e08ec27e7b4a9909b936c757', 'producerPR': None}`, `{'path': 'apps/api/app/foods/admin_router.py', 'status': 'A', 'branchBlob': '316c302c47639d26653ece96ff6b0f149127404e', 'historicalMainCommit': '36aac03b303bf2d5db2d7d3ef838697eb6bf5889', 'producerPR': 62}`, `{'path': 'apps/api/app/foods/catalog.py', 'status': 'A', 'branchBlob': 'a24e9c8ec599d637f4a80f4ab3f73afb47617ef4', 'historicalMainCommit': '86b716ee75c3ba242cee79248133fac44cbf3a84', 'producerPR': 154}`, `{'path': 'apps/api/app/foods/router.py', 'status': 'A', 'branchBlob': '07c1f7b1ff90f309d6e73083ae78d286c0cea33b', 'historicalMainCommit': '1a7456e473a2a9141723ca3068f8c49916fb6a5a', 'producerPR': 65}`, `{'path': 'apps/api/app/foods/service.py', 'status': 'A', 'branchBlob': '7c4590a00d048ced777754f8ee203b4bff6ea4c2', 'historicalMainCommit': '8ce43a66dd34dc07e08ec27e7b4a9909b936c757', 'producerPR': None}`, `{'path': 'apps/api/app/hotspots/catalog.py', 'status': 'M', 'branchBlob': '112174b1567c09d3d7d357fdd7d1cc5e1e101c28', 'historicalMainCommit': '4ac1208f08ee3060748b789f22e3f56d38ed0f8f', 'producerPR': 108}`, `{'path': 'apps/api/app/hotspots/food_area_bootstrap.json', 'status': 'A', 'branchBlob': '39645f72aeb153ee9435605537b7becf89b1fb48', 'historicalMainCommit': 'b75ae15f97956c26bb8e94a2a7fefd81b0545777', 'producerPR': 214}`, `{'path': 'apps/api/app/hotspots/maps.py', 'status': 'A', 'branchBlob': '169461610d40e7b379f8a9d31f9ef1331912881d', 'historicalMainCommit': '36aac03b303bf2d5db2d7d3ef838697eb6bf5889', 'producerPR': 62}`, `{'path': 'apps/api/app/hotspots/router.py', 'status': 'M', 'branchBlob': '0416f515f144184e1744452e26bed354598756b8', 'historicalMainCommit': 'bdc9d08628f9f5749c3b6ba41ac6bf05de30dd83', 'producerPR': 61}`, `{'path': 'apps/api/app/hotspots/service.py', 'status': 'M', 'branchBlob': '412418bbe742cff2524b59daa4287c410a4c0c33', 'historicalMainCommit': 'bdc9d08628f9f5749c3b6ba41ac6bf05de30dd83', 'producerPR': 61}`。

- [ ] **Codex `codex/food-reservation-platforms` — 未完成**。依新待辦 `2026-10-11-reconcile-reservation-review-residuals` 續作，原始分支与既有修改完整保留。
  - 核對 HEAD：`59f4b994533554509ec2dd90d0f7139acf8030a9`。
  - 待辦：Reconcile/restore task2026-09-11-merchant-reservation-enrichment with only residual concrete issues: reproduce the Maisen-search→Thipsamai-dialog mismatch on current editor with an identity-checked no-write fixture; locate an existing fix receipt or file the focused bug if reproducible.
  - 待辦：Freshly compare the exact TABLES original closure notice with current official branch/operating-status sources, and reconcile Qin Yuan Chun founding-store temporary129→137 move with current merchant/source records under a separate factual-review scope. Record a finite source-backed conclusion before closing those old unchecked items.
  - 待辦：Preserve/integrate the full dated enrichment report and historical applied URLs/receipts; mark full-catalog research and verified canonical-link former holds superseded by#408/#397 rather than repeating them. Keep this branch until those unique residual tracking items have a durable disposition.
  - 任務：[2026-10-11-reconcile-reservation-review-residuals](../../tasks/open/2026-10-11-reconcile-reservation-review-residuals.md)（主幹 本 PR open）。
  - 任務：[2026-09-11-food-reservation-platforms](../../tasks/done/2026-09-11-food-reservation-platforms.md)（主幹 done）；原認領 codex-food-reservation-platforms。
  - 任務：`2026-09-11-merchant-reservation-enrichment`（主幹 absent）。
  - 核對證據：PR #392 merged the source/CI/browser editor changes at19a94294;25 of26 non-task product/evidence paths are exact at that producer tree, and the only different path is the later enrichment operation report. Main has the done platform implementation task. The14 unique commits comprise5 integrated product/test/CI commits and9 later deployment/enrichment receipts.
  - 核對證據：The old research completion item is superseded: PR #408/done backfill covers all296 then-unlinked merchants and311 reviews, preserves manually reviewed rows and records production application. Do not create a296/309-unresearched backlog.
  - 核對證據：Concrete former holds now have exact replacement proof: GU:UM/Nómada/FRANCIS query-free SevenRooms routes were independently opened with matching branch/address and booking widget in main review manifest; Druggists has separately observed canonical inline branch ID. yosukgung.kr is supported via#397 and verified in main. Haeundaegalbi is disabled and Chunshim ambiguous per full review; Qin Yuan Chun has a separately opened matching founding-store widget plus relocation notice.
  - 核對證據：Residual unique local task asks for suspected rapid-search/editor identity mismatch reproduction (Maisen row opened Thipsamai, caught before save), TABLES operating-status review after a dated closure notice, and Qin Yuan Chun merchant/source treatment for temporary129→137 move. Subsequent reservation manifest gives booking data outcomes but does not supply an explicit reproduction/fix receipt for that race or adjudication of the conflicting business/source facts. The unique report/task must be consolidated so these specific issues are not silently lost.
  - 核對證據：Generic support for raw SevenRooms venues queries/inline custom paths is not needed to claim the existing exact canonical merchant links complete; those former data blockers have positive independent alternate-route evidence. No current merge gap in the#392 feature is claimed.
  - 續作路徑：`{'path': '.github/workflows/food-map-reservations.yml', 'status': 'M', 'branchBlob': '628a78aec417cfad383657e30d0592ead7d08ced', 'historicalMainCommit': 'a4ee0f50770334051c7e2618a2138617875a1b40', 'producerPR': 468}`, `{'path': 'apps/api/app/foods/admin_router.py', 'status': 'M', 'branchBlob': '7481e5fa7b4670cbb17c4f703f038443eb9fd060', 'historicalMainCommit': '93933b2771ac8a994c55f0ec6e64138ad05503df', 'producerPR': 555}`, `{'path': 'apps/api/app/foods/platform_links.py', 'status': 'M', 'branchBlob': 'a004fcfe37ce1687d1168191585bfe6c6432fe24', 'historicalMainCommit': '80dfaa535b27f3b816ff44ad5fc2ce9090761959', 'producerPR': 399}`, `{'path': 'apps/api/app/foods/service.py', 'status': 'M', 'branchBlob': 'bf5a34357dc6995118d3f4f03d7c5a722e68f84f', 'historicalMainCommit': '6caa1e7906cd10991ada1be039dc93e2f3672103', 'producerPR': 1220}`, `{'path': 'apps/api/app/i18n.py', 'status': 'M', 'branchBlob': '087db8ea496091f6184f6215184066c484451f03', 'historicalMainCommit': '94fef42d055678eed0f46efb979ce1a49acd24a7', 'producerPR': 396}`, `{'path': 'apps/api/tests/test_discovery_flow.py', 'status': 'M', 'branchBlob': '5689765d19c622ac43d871368d48102a9e4395e1', 'historicalMainCommit': '02317cf5ad32d2a36647313a1f1aca5585189596', 'producerPR': 408}`, `{'path': 'apps/api/tests/test_food_integration.py', 'status': 'M', 'branchBlob': '809317732c66a6d7ded6eb67ae8a653cb0962eb0', 'historicalMainCommit': '6c6346e4407337b9803b40b48a3735dbc7429755', 'producerPR': 562}`, `{'path': 'apps/api/tests/test_food_platform_links.py', 'status': 'M', 'branchBlob': '555c83723d61666c9b07533831a6460b8f0ec70d', 'historicalMainCommit': '80dfaa535b27f3b816ff44ad5fc2ce9090761959', 'producerPR': 399}`, `{'path': 'apps/api/tests/test_reservation_platform_auth.py', 'status': 'A', 'branchBlob': '3f0957d60e6bbbbcd60230417ff288733298ab48', 'historicalMainCommit': '6c6346e4407337b9803b40b48a3735dbc7429755', 'producerPR': 562}`, `{'path': 'apps/web/components/admin-food-merchants-panel.test.tsx', 'status': 'M', 'branchBlob': '6feebdc1f68debdde11a9229c87f97c8453b4893', 'historicalMainCommit': '19a94294c71503cfba29d1cb1f1f57776fd3ce46', 'producerPR': 392}`。

- [ ] **Codex `codex/frontend-flow-release-record-a899437a` — 未完成**。依新待辦 `2026-10-11-restore-frontend-flow-polish` 續作，原始分支与既有修改完整保留。
  - 核對 HEAD：`2cfb1acab8f4f9bad565b54fa194bd5a3cbd90d4`。
  - 待辦：恢复／归并2026-09-09-frontend-flow-post-deploy-polish的两项真实UX待办：在390px My trips保留可见且可触达的继续入口，更新五语copy／布局及相应回归。
  - 待辦：Collections的merchant与restaurant筛选项使用不同、准确的五语label，不改变服务端筛选枚举；验证URL filter、五语文案与keyboard选择。
  - 待辦：附本次frozenmain行号和现有scope证据，保留原release／CI handoff供追溯；Escape由#493已完成，不再列generic未解决flake。
  - 任務：[2026-10-11-restore-frontend-flow-polish](../../tasks/open/2026-10-11-restore-frontend-flow-polish.md)（主幹 本 PR open）。
  - 任務：`2026-09-09-frontend-flow-post-deploy-polish`（主幹 absent）。
  - 任務：[2026-09-09-frontend-flow-integration](../../tasks/done/2026-09-09-frontend-flow-integration.md)（主幹 done）；原認領 codex-frontend-flow。
  - 任務：[2026-09-11-modal-escape-flake-under-load](../../tasks/done/2026-09-11-modal-escape-flake-under-load.md)（主幹 done）；原認領 claude-opus-5。
  - 任務：[2026-09-09-discovery-card-details](../../tasks/done/2026-09-09-discovery-card-details.md)（主幹 done）；原認領 codex-discovery-card-details。
  - 核對證據：4 unique commits只修改task closure/scope/handoff與generatedBOARD。完整原integrationrecord已读：#374 a899437a发布完成，postdeploypolish另开；main4个frontendflow原tasks均done，discovery-card handoff已由 #378與maindone task取代。這些完成收據不是剩餘code。
  - 核對證據：原Escape失效handoff已由真正rootcause取代：完整mainmodal-escape task的2026-09-13／14收尾读完，default-lane DOMcommit与passiveeffect的间隔得到5个确定性回归，#493 (46298e28)改为layout effects且4轮CI／本机fullsuite通过，未放宽Escape断言。将该调查从剩餘工作移除。
  - 核對證據：另外两个实际UXtodo仍见于frozen代码：account-list.tsx:436 的 flowCopy.continue 仍class="hidden text-sm font-semibold text-[var(--teal)] sm:inline"，mobile隐藏；discovery/collections.tsx:109 同时列merchant/restaurant但restaurant强制c.kinds.merchant，discovery-copy.ts:17 zh-TW名称仍「特色店家」。因此该分支不只是可丢弃完工收据。
  - 核對證據：原2026-09-09-frontend-flow-post-deploy-polish只存在branch，frozen main无此task，也未找到补足该两项的后续产品commit。需把具体未完UX票补回共享看板；无需重新调查已修Escape或重做已完成发布。
  - 續作路徑：`tasks/BOARD.md`, `tasks/done/2026-09-09-frontend-flow-integration.md`, `tasks/open/2026-09-09-frontend-flow-discovery-api.md`, `tasks/open/2026-09-09-frontend-flow-discovery-web.md`, `tasks/open/2026-09-09-frontend-flow-integration.md`, `tasks/open/2026-09-09-frontend-flow-post-deploy-polish.md`, `tasks/open/2026-09-09-frontend-flow-saved-api.md`。

- [ ] **Codex `codex/merchant-style-batch-08` — 未完成**。保留原票／owner與9/29 HOLD；在未來授權輪先對精確4店+4提案做唯讀逐欄snapshot，確認哪些仍缺map identity／獨立耐久座標／風格review，再按真正欠項補窄子票；不重新匯入候選。
  - 核對 HEAD：`ebd94ce0610e1f43172800313be07d954bfa9099`。
  - 待辦：本輪不核准／退回／補正式欄位／發布或付費map/model；source材料與早期handoff收據保留，不改回已移交的trips／metadata scopes。
  - 任務：[2026-10-11-reconcile-merchant-style-batch08-acceptance](../../tasks/open/2026-10-11-reconcile-merchant-style-batch08-acceptance.md)（主幹 本 PR open）。
  - 任務：[2026-09-07-merchant-style-discovery](../../tasks/open/2026-09-07-merchant-style-discovery.md)（主幹 open）。
  - 核對證據：第八批實作／資料交付已merged #361 a8adec5e4132e4392f20568708d043ac2292e7ea，3產品檔（資料/匯入設定/merchant-styles文檔）與merge精確同blob；9unique commits中後續多為範圍窄幅handoff metadata，不是新未合API改動。
  - 核對證據：完整當輪receipt明記華山青鳥、bibliothèque福岡天神、오설록北村、Merci Marcel Orchard，4店/4提案已guarded preview/apply/replay0/0匯入，privatebackup/fieldaudit/publichidden驗證；pending/inactive/unverified是刻意保護狀態，不能重做import或當公開店家。
  - 核對證據：main原同票2026-09-07-merchant-style-discovery明確認第八批＋#361已完成，但逐家精準地圖、獨立耐久座標、管理員風格核准再發布仍未勾。這是原同scope實際未完成要求，而非scope外另一open票。9/29 owner已決定保留待辦、這輪不改正式資料。
  - 核對證據：本輪没有逐店新正式snapshot，20全站pending商戶總數不是四店逐筆結案證據。保留同scope最後驗收與原ownership，不由資料PR合併推論已公開。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-reconcile-merchant-style-batch08-acceptance。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'path': 'apps/api/app/foods/data/style_merchants_2026_09_batch_08.json', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'e446b902670f8bf3235f47154c31c6c698b70e39', 'mainBlob': 'e446b902670f8bf3235f47154c31c6c698b70e39', 'matchesMain': True, 'exactAtOwnMerge': True, 'historicalMainCommit': 'a8adec5e4132e4392f20568708d043ac2292e7ea', 'ownMergeBlob': 'e446b902670f8bf3235f47154c31c6c698b70e39'}`, `{'path': 'apps/api/tests/test_merchant_styles.py', 'status': 'M', 'baseBlob': '56c40415bfb7755a2d01231c6b8a4ceab0a9fbec', 'branchBlob': 'cf4db971f9f3473ed21a84db3d2fcb1dea577a79', 'mainBlob': 'c8a7e36289f562c73593d0a2b56c5d579e53082f', 'matchesMain': False, 'exactAtOwnMerge': True, 'historicalMainCommit': '6c6346e4407337b9803b40b48a3735dbc7429755', 'ownMergeBlob': 'cf4db971f9f3473ed21a84db3d2fcb1dea577a79'}`, `{'path': 'docs/merchant-styles.md', 'status': 'M', 'baseBlob': '2779bce555db465d324a6f4b36aa709a11b14361', 'branchBlob': '1d997208ccb99aac331f9ec781fef2eedfc43660', 'mainBlob': '1d997208ccb99aac331f9ec781fef2eedfc43660', 'matchesMain': True, 'exactAtOwnMerge': True, 'historicalMainCommit': 'a8adec5e4132e4392f20568708d043ac2292e7ea', 'ownMergeBlob': '1d997208ccb99aac331f9ec781fef2eedfc43660'}`, `{'path': 'tasks/BOARD.md', 'status': 'M', 'baseBlob': 'ea1d9700921a6706286ad71ed4b9ee8c945b0b4b', 'branchBlob': 'a3d7ca2402274e0ddb9fdbb7d69f8ce84980f7b7', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': '27686699b661f8b923b51676832925eb921a1252'}`, `{'path': 'tasks/open/2026-09-07-merchant-style-discovery.md', 'status': 'M', 'baseBlob': 'f787c80c8ec785582113f24cce8c8e58dfb3b7be', 'branchBlob': 'b069dbab86bef60e93ba75d3e89c636e469b5ab3', 'mainBlob': '9d264211690027d74230844b48c54ebafb0f6b84', 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': '38f0a5323b03bd8a9fa9f0da66a834c33a569041'}`。

- [ ] **Codex `codex/redeploy-20260914` — 未完成**。恢復窄read-only對帳票，先辨識目前host入口與source/version；已替代項目用具體程式結案，仍缺項目再窄scope/claim修復。
  - 核對 HEAD：`434fc41292b7530f006d6ff29f93c4655aa5deea`。
  - 待辦：封存完成操作receipt，保留原backup檔/restore證據；不把pg_restore --list當full還原驗證。
  - 任務：[2026-10-11-reconcile-legacy-host-redeploy-hardening](../../tasks/open/2026-10-11-reconcile-legacy-host-redeploy-hardening.md)（主幹 本 PR open）。
  - 任務：`2026-09-14-harden-legacy-host-redeploy-backups-and`（主幹 absent）。
  - 任務：`2026-09-14-redeploy-latest-green-main-and-verify`（主幹 absent）。
  - 核對證據：單一commit三個文件/task路徑，Sep14部署a4ee0f507、8 app服務health、backup27,298,580 bytes SHA2d096及pg_restore --list已完成，沒有guide-import/30新內容發布，不能擴大收據scope。
  - 核對證據：真正missing local open票為harden-legacy-host-redeploy-backups-and；它指出舊host manual脚本source/backup/rollback契約，沒有對應implementation patch或main共享票。
  - 核對證據：fresh repo ops/deployer/manual-deploy.sh已不存在，只有README入口說明；本輪未讀實際installed host driver，歷史缺口要先定位replacement/installed version，不能直接宣稱目前正式主機仍有Sep14缺陷。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-reconcile-legacy-host-redeploy-hardening。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'A', 'path': 'docs/deployments/2026-09-14-redeploy.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/done/2026-09-14-redeploy-latest-green-main-and-verify.md', 'oldPath': None}`, `{'status': 'A', 'path': 'tasks/open/2026-09-14-harden-legacy-host-redeploy-backups-and.md', 'oldPath': None}`。

- [ ] **Codex `codex/seoul-day2-transport-ux` — 未完成**。先補回原precision/fare缺件票（或等价窄票），保全release receipt；原#387已完成功能及部署不重開。
  - 核對 HEAD：`abdd425422a522f1e80d538025d571054b7c8864`。
  - 待辦：以synthetic 20s-step fixtures保留source seconds後合計再round/rank，並明確區分missing/invalid money、verified0+currency；更新backend/types/UI五語與回歸，毋須付費providerprobe。
  - 任務：[2026-10-11-restore-transit-timing-fare-precision](../../tasks/open/2026-10-11-restore-transit-timing-fare-precision.md)（主幹 本 PR open）。
  - 任務：[2026-09-10-seoul-day2-transport-ux](../../tasks/done/2026-09-10-seoul-day2-transport-ux.md)（主幹 done）；原認領 codex-seoul-day2-release。
  - 任務：`2026-09-10-transit-timing-and-fare-precision`（主幹 absent）。
  - 任務：[2026-09-11-seoul-day2-live-requery](../../tasks/open/2026-09-11-seoul-day2-live-requery.md)（主幹 open）。
  - 核對證據：原Seoul可查詢/可讀details產品已merged #387 a044e4cc04f27107b68f7a198482ea000ca5e982，原票 main DONE。unique HEAD abdd425422a522f1e80d538025d571054b7c8864只有實際release收據＋新precision/fare缺件票，無待合原產品code。
  - 核對證據：完整新增收據明載已部署8應用、verifiedbackup/health、Chrome普通query3 previews、noapplytrip v8/33items/0routes不變；不是宣稱全韓國coverage或futuretimetime已驗。
  - 核對證據：真正缺件票2026-09-10-transit-timing-and-fare-precision main ABSENT，亦未找到重命名同scope票。已直接讀frozen main routing.py：duration_minutes仍max(1,round(seconds/60))、RouteStep最低1、LESS_WALKING仍加rounded per-step minutes、_money({})仍Decimal0/null currency；panel/card仍用空currency拼fare，types没有seconds。
  - 核對證據：正面current-code證據符合原缺件：24×20s應8min卻24min、未知fare被當裸0，兩個產品欠項尚存在。另2026-09-11-seoul-day2-live-requery為live查詢票，不修deterministic時間／money規格，不可當alias已完成。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-transit-timing-fare-precision。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'path': 'docs/seoul-day2-transport-ux.md', 'status': 'M', 'baseBlob': '5c2a1ce50c192d17d7e49a064317392867ce4ed0', 'branchBlob': '16e3bade834f1136fc15271d49e5efbb1289fdea', 'mainBlob': '5c2a1ce50c192d17d7e49a064317392867ce4ed0', 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': '5c2a1ce50c192d17d7e49a064317392867ce4ed0'}`, `{'path': 'tasks/BOARD.md', 'status': 'M', 'baseBlob': 'cf35749ce1723e9cece0bff35f9554faea77cc75', 'branchBlob': 'd87c20a36224fcb78fe2fc1d1954da6b8b0be127', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': 'cf35749ce1723e9cece0bff35f9554faea77cc75'}`, `{'path': 'tasks/done/2026-09-10-seoul-day2-transport-ux.md', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'b4585123fa8f703c555329b522ff6431a5bb9248', 'mainBlob': '97d873b5480fe55462db4df9840b8ffc02c3c864', 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': None}`, `{'path': 'tasks/open/2026-09-10-seoul-day2-transport-ux.md', 'status': 'D', 'baseBlob': 'e9029399393d516fcbb2bb752de6e93da3696f88', 'branchBlob': '0000000000000000000000000000000000000000', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': 'e9029399393d516fcbb2bb752de6e93da3696f88'}`, `{'path': 'tasks/open/2026-09-10-transit-timing-and-fare-precision.md', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': 'da3b6d8369b1115c415a0d7bb60c559f087d4f35', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': False, 'historicalMainCommit': None, 'ownMergeBlob': None}`。

- [ ] **Codex `codex/stay22-hotel-clickout` — 未完成**。把缺服務shared跟踪恢復為一張窄票，對現compose/mandatory服務集與fake runner契約；Stay22 feature done保持，不重开整個clickout。
  - 核對 HEAD：`d5e137b2cf56786758ea9a1753c8c69ee9621187`。
  - 任務：[2026-10-11-restore-agent-community-sweeper-services](../../tasks/open/2026-10-11-restore-agent-community-sweeper-services.md)（主幹 本 PR open）。
  - 任務：[2026-09-06-area-circles-electronics-districts](../../tasks/done/2026-09-06-area-circles-electronics-districts.md)（主幹 done）；原認領 codex-gpt6-electronics-areas。
  - 任務：[2026-09-06-oka-amerikamura-wrong-qid](../../tasks/done/2026-09-06-oka-amerikamura-wrong-qid.md)（主幹 done）；原認領 claude-opus-5-5-oka-qid。
  - 任務：[2026-09-06-shopping-seeds-second-batch](../../tasks/open/2026-09-06-shopping-seeds-second-batch.md)（主幹 open）。
  - 任務：[2026-09-07-enrich-new-shopping-place-ids](../../tasks/open/2026-09-07-enrich-new-shopping-place-ids.md)（主幹 open）。
  - 任務：[2026-09-07-jsonb-3-42](../../tasks/done/2026-09-07-jsonb-3-42.md)（主幹 done）；原認領 claude-fable-5-1。
  - 任務：[2026-09-08-continue-evidence-backed-remaining-hotspot-candidate](../../tasks/open/2026-09-08-continue-evidence-backed-remaining-hotspot-candidate.md)（主幹 open）。
  - 任務：[2026-09-08-travel-discovery-api](../../tasks/done/2026-09-08-travel-discovery-api.md)（主幹 done）；原認領 codex-discovery-api。
  - 任務：[2026-09-08-travel-discovery-community](../../tasks/done/2026-09-08-travel-discovery-community.md)（主幹 done）；原認領 codex-discovery-community。
  - 任務：[2026-09-08-travel-discovery-integration](../../tasks/done/2026-09-08-travel-discovery-integration.md)（主幹 done）；原認領 codex-discovery-root。
  - 任務：[2026-09-08-travel-discovery-web](../../tasks/done/2026-09-08-travel-discovery-web.md)（主幹 done）；原認領 codex-discovery-web。
  - 任務：[2026-09-09-admin-operations-center](../../tasks/done/2026-09-09-admin-operations-center.md)（主幹 done）；原認領 codex-root。
  - 任務：`2026-09-09-include-community-sweeper-in-deployment-agent`（主幹 absent）。
  - 任務：[2026-09-09-pr335-funnel-merge-integration](../../tasks/done/2026-09-09-pr335-funnel-merge-integration.md)（主幹 done）；原認領 codex-pr335-delivery。
  - 任務：[2026-09-09-pr365-docs-integration](../../tasks/done/2026-09-09-pr365-docs-integration.md)（主幹 done）；原認領 codex-review-archive。
  - 任務：[2026-09-09-stay22-hotel-clickout](../../tasks/done/2026-09-09-stay22-hotel-clickout.md)（主幹 done）；原認領 codex-stay22。
  - 核對證據：#379 merged的38非task產品路徑全部精確producer匹配，Stay22 clickout與own整合task main done，歷史deploy收據已完成。
  - 核對證據：未共享的local open票include-community-sweeper-in-deployment-agent不是Stay22實作缺口；fresh main executor.py:27–37 APPLICATION_SERVICES仍缺community-sweeper，forward/rollback沿用tuple，contract tests無sweeper。
  - 核對證據：代理是否目前enabled/installed不能憑舊收據判斷；即使另一路正常deploy能啟sweeper，代理程式契約缺口也沒有被其替代。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-restore-agent-community-sweeper-services。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'status': 'M', 'path': '.github/workflows/ci.yml', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/admin.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/errors.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/hotel_admin.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/hotel_options.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/router.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/schemas.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/travel_services/service.py', 'oldPath': None}`, `{'status': 'A', 'path': 'apps/api/app/travel_services/stay22.py', 'oldPath': None}`, `{'status': 'M', 'path': 'apps/api/app/trips/stay_router.py', 'oldPath': None}`。

- [ ] **Codex `codex/wordpress-map-form-token-link-task` — 未完成**。補回獨立 source-publication/rebind 窄票，連#887與done alias；先唯讀核對map guide當前published revision／block3／hash，若已另行發布則引用精確receipt結案，否則依原release gate處理。
  - 核對 HEAD：`f61b7436c2d0385b69d3ba5a890ebc0d78e8b4f4`。
  - 待辦：對修正後live source做fresh capture與Batch034四語bundle重綁；不得覆寫後來source edits、直接拿舊v2/v4或舊#887pack當正式baseline，不重做已落地inline修正。
  - 任務：[2026-10-11-reconcile-wordpress-map-source-release](../../tasks/open/2026-10-11-reconcile-wordpress-map-source-release.md)（主幹 本 PR open）。
  - 任務：`2026-09-27-correct-wordpress-map-embed-marker-ai`（主幹 absent）。
  - 任務：[2026-09-28-correct-unrelated-ai-term-links-in](../../tasks/done/2026-09-28-correct-unrelated-ai-term-links-in.md)（主幹 done）；原認領 codex-source-ticket-cleanup-20261003。
  - 核對證據：唯一commit f61b7436c2d0385b69d3ba5a890ebc0d78e8b4f4只是來源修正／guardedpublish/rebind原票；該exact ID目前main ABSENT，無自身PR。
  - 核對證據：已找到部分接替：#887 dd1d51730c0c46698325fb357bb90ac0303d7b8c和main DONE的correct-unrelated-ai-term-links-in只涵蓋兩pack repository source-only。直接讀current map-form-embeds zhTW block3 inline1已是 {type:text,text:標記}，普通map marker錯連AI glossary實作已完成，不應重做。
  - 核對證據：但原票明列「依guarded procedure發布source、驗public revision、recapture/rebind後才翻譯」。新done票2026-10-03完整正文明說沒有freshproduction／import／publication，guarded source publication與Batch034 source rebind仍是separatework。main的兩篇packs目前仍只有zhTW，release receipts搜尋未有這兩slug的正式來源完成收據；不能從#887merge就宣告原完整票done。
  - 核對證據：目前需要保全的真未完項是缺失的來源發布／版本重綁記帳，不是JSON修正。無新正式站核對，本報告把具體待驗前提列待辦，不能把舊v2/v4讀取當current live state。
  - 核對證據：本輪恢復待辦保存於既有draft PR1450（open、未認領，尚未合併main）：2026-10-11-reconcile-wordpress-map-source-release。歷史ref依完整bundle保全，不把建票當實作完成。
  - 續作路徑：`{'path': 'tasks/open/2026-09-27-correct-wordpress-map-embed-marker-ai.md', 'status': 'A', 'baseBlob': '0000000000000000000000000000000000000000', 'branchBlob': '2fc0dd5ad9ae2189f0bffc749189f4b24073ca6f', 'mainBlob': None, 'matchesMain': False, 'exactAtOwnMerge': None, 'historicalMainCommit': None, 'ownMergeBlob': None}`。
