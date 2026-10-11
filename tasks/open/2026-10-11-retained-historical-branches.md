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
- [ ] 核對待核對組的獨有差異；逐項記錄需整合、已取代或刻意保留的證據。
- [ ] 把尚未進共享看板的工作補成窄範圍任務，連回原始 HEAD。
- [ ] 完成的項目重新檢查與備份後清理，並更新本索引。

## Verification

本票是追蹤索引，scope 只含此檔；實作走既有任務或另外認領窄範圍票。不得藉本票改動其他模型的認領、影片生產或正式站。

## Notes

核對時間：2026-10-11T13:16:41.525938+00:00（UTC）。原始清單固定為 197 個本機歷史分支。

已刪除 109 個（Codex 97、Claude 12）；保留 88 個（Codex 76、Claude 12）。
保留分類：64 個未完成、24 個待核對。

刪除前已保存完整 Git bundle，驗證 SHA-256，並在獨立空白 bare repository 中還原每個 HEAD；沒有借用原始物件庫。每次刪除都比對預期 HEAD，確認分支未被任何 worktree 使用、沒有開啟中的 PR，並驗證 ref 已不存在。

完整核對、清理及還原證據位於 `C:/Users/x8120/.codex/scratch/historical-cleanup-20261011/`。主幹基準 `0c93720e684b4c3995b16f7c2e859fe2bc06ec9f`。

- 備份 `completed-codex.bundle`：93 個分支；SHA-256 `90926263e043158940b0612550a68f12ec79fb2c47e51c9cbfb8b8a95e4c1774`；獨立還原通過。
- 備份 `completed-codex-supplement-2.bundle`：4 個分支；SHA-256 `2b3aeadb1056f3f2369e0c1c7ca25d94a222969a3b7d0118d1dbecf74c2a8072`；獨立還原通過。
- 備份 `completed-claude.bundle`：12 個分支；SHA-256 `b59844447c9b39b03c579137b3f58e1f43a71bc0f672b0acfa0e3bf3a40d1e73`；獨立還原通過。

以下為分支索引，不重複開已存在的任務。所有原認領均保留；同一任務可能由多個歷史分支指向。

### 文章、多語系與發布（19）

- [ ] **Codex `codex/article-localization-030-pair-b` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`d0ec33cc7bfe44ffd6ba61bda4e8eb268a506241`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/app/guides/content/wordpress-host-migration.json, apps/api/app/guides/content/wordpress-migration-aftercare.json
  - 任務：[2026-09-27-batch030-host-diagram-label](../../tasks/done/2026-09-27-batch030-host-diagram-label.md)（主幹 done）。
  - 任務：[2026-09-27-localize-wordpress-migration-batch030-pair-b](../../tasks/done/2026-09-27-localize-wordpress-migration-batch030-pair-b.md)（主幹 done）。
  - 優先核對路徑：`apps/api/app/guides/content/wordpress-host-migration.json`, `apps/api/app/guides/content/wordpress-migration-aftercare.json`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/article-localization-031-pair-b` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`e8fa87d9abb0969a5c9861e5b0b551757cd47ba6`。
  - 原始下一步：2026-09-27-correct-wordpress-user-roles-unrelated-ai remains open
  - 任務：`2026-09-27-localize-wordpress-social-login-and-user`（主幹 absent）。
  - 任務：[2026-09-27-correct-wordpress-user-roles-unrelated-ai](../../tasks/open/2026-09-27-correct-wordpress-user-roles-unrelated-ai.md)（主幹 open）。
  - 優先核對路徑：`apps/api/app/guides/content/wordpress-user-roles.json`, `apps/web/public/guides/wordpress-user-roles/diagram-1-en.svg`, `apps/web/public/guides/wordpress-user-roles/diagram-1-ja.svg`, `apps/web/public/guides/wordpress-user-roles/diagram-1-ko.svg`, `apps/web/public/guides/wordpress-user-roles/diagram-1-zh-cn.svg`, `apps/web/public/guides/wordpress-user-roles/hero-en.jpg`, `apps/web/public/guides/wordpress-user-roles/hero-en.svg`, `apps/web/public/guides/wordpress-user-roles/hero-ja.jpg` 等 13 個路徑。
  - 保留證據：Linked main task remains unfinished: 2026-09-27-correct-wordpress-user-roles-unrelated-ai=open

- [ ] **Codex `codex/article-localization-037-social-a` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`893ff4adaa862d634b74ea746209ad53f4b089c5`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/app/guides/content/social-media-planning.json, docs/article-localization/batch037-pair-a-evidence.md
  - 任務：[2026-09-28-batch037-pair-a-localize-stp-persona](../../tasks/done/2026-09-28-batch037-pair-a-localize-stp-persona.md)（主幹 done）。
  - 優先核對路徑：`apps/api/app/guides/content/social-media-planning.json`, `docs/article-localization/batch037-pair-a-evidence.md`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/article-localization-040-affiliate-a` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`0bbf0d74e55e4a1089009abee8525e025c894f88`。
  - 原始下一步：2026-09-28-review-batch040-pair-a-inherited-editorial remains open
  - 任務：[2026-09-28-batch040-pair-a-artwork-evidence](../../tasks/done/2026-09-28-batch040-pair-a-artwork-evidence.md)（主幹 done）。
  - 任務：[2026-09-28-install-reviewed-batch040-affiliate-and-store](../../tasks/done/2026-09-28-install-reviewed-batch040-affiliate-and-store.md)（主幹 done）。
  - 任務：[2026-09-28-release-reviewed-batch040-affiliate-and-store](../../tasks/done/2026-09-28-release-reviewed-batch040-affiliate-and-store.md)（主幹 done）。
  - 任務：[2026-09-28-review-batch040-pair-a-inherited-editorial](../../tasks/open/2026-09-28-review-batch040-pair-a-inherited-editorial.md)（主幹 open）。
  - 優先核對路徑：`apps/api/app/guides/content/affiliate-marketing-basics.json`, `apps/api/app/guides/content/independent-store-marketplace.json`, `apps/web/public/guides/affiliate-marketing-basics/diagram-1-en.svg`, `apps/web/public/guides/affiliate-marketing-basics/diagram-1-ja.svg`, `apps/web/public/guides/affiliate-marketing-basics/diagram-1-ko.svg`, `apps/web/public/guides/affiliate-marketing-basics/diagram-1-zh-cn.svg`, `apps/web/public/guides/affiliate-marketing-basics/hero-en.jpg`, `apps/web/public/guides/affiliate-marketing-basics/hero-en.svg` 等 27 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 1dbb4ec15657892528f435e29c18903eaca042f6
  - 保留證據：Linked main task remains unfinished: 2026-09-28-review-batch040-pair-a-inherited-editorial=open

- [ ] **Codex `codex/article-localization-040-seo-b` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`6922a5a20d92778863178ddeaab7808962170e6f`。
  - 原始下一步：2026-09-28-review-batch040-pair-b-inherited-editorial remains open
  - 任務：[2026-09-28-batch040-pair-b-ecommerce-zero-click](../../tasks/done/2026-09-28-batch040-pair-b-ecommerce-zero-click.md)（主幹 done）。
  - 任務：[2026-09-28-correct-batch040-b-preview-viewport-evidence](../../tasks/done/2026-09-28-correct-batch040-b-preview-viewport-evidence.md)（主幹 done）。
  - 任務：[2026-09-28-install-batch040-product-seo-and-zero](../../tasks/done/2026-09-28-install-batch040-product-seo-and-zero.md)（主幹 done）。
  - 任務：[2026-09-28-release-reviewed-batch040-product-seo-and](../../tasks/done/2026-09-28-release-reviewed-batch040-product-seo-and.md)（主幹 done）。
  - 任務：[2026-09-28-review-batch040-pair-b-inherited-editorial](../../tasks/open/2026-09-28-review-batch040-pair-b-inherited-editorial.md)（主幹 open）。
  - 優先核對路徑：`apps/api/app/guides/content/ecommerce-product-seo.json`, `apps/api/app/guides/content/zero-click-search-strategy.json`, `apps/web/public/guides/ecommerce-product-seo/diagram-1-en.svg`, `apps/web/public/guides/ecommerce-product-seo/diagram-1-ja.svg`, `apps/web/public/guides/ecommerce-product-seo/diagram-1-ko.svg`, `apps/web/public/guides/ecommerce-product-seo/diagram-1-zh-cn.svg`, `apps/web/public/guides/ecommerce-product-seo/hero-en.jpg`, `apps/web/public/guides/ecommerce-product-seo/hero-en.svg` 等 27 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 49aa683a050df824204166c4f15656c603be2dab
  - 保留證據：Linked main task remains unfinished: 2026-09-28-review-batch040-pair-b-inherited-editorial=open

- [ ] **Codex `codex/article-localization-042-seo-a` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`f06b6b7200b97ff8e1c1046b63f075211385b48c`。
  - 原始下一步：2026-09-28-batch042-pair-a-source-editorial-followup remains open
  - 任務：[2026-09-28-batch042-pair-a-install-reviewed-locales](../../tasks/done/2026-09-28-batch042-pair-a-install-reviewed-locales.md)（主幹 done）。
  - 任務：[2026-09-28-prepare-batch042-search-intent-and-content](../../tasks/done/2026-09-28-prepare-batch042-search-intent-and-content.md)（主幹 done）。
  - 任務：[2026-09-28-batch042-pair-a-release-reviewed-locales](../../tasks/done/2026-09-28-batch042-pair-a-release-reviewed-locales.md)（主幹 done）。
  - 任務：[2026-09-28-batch042-pair-a-source-editorial-followup](../../tasks/open/2026-09-28-batch042-pair-a-source-editorial-followup.md)（主幹 open）。
  - 優先核對路徑：`apps/api/app/guides/content/seo-content-quality.json`, `apps/api/app/guides/content/seo-search-intent.json`, `apps/web/public/guides/seo-content-quality/diagram-1-en.svg`, `apps/web/public/guides/seo-content-quality/diagram-1-ja.svg`, `apps/web/public/guides/seo-content-quality/diagram-1-ko.svg`, `apps/web/public/guides/seo-content-quality/diagram-1-zh-cn.svg`, `apps/web/public/guides/seo-content-quality/hero-en.jpg`, `apps/web/public/guides/seo-content-quality/hero-en.svg` 等 27 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit f0f031c60d9fbb4016a184a1e7e3bf19b751568f
  - 保留證據：Linked main task remains unfinished: 2026-09-28-batch042-pair-a-source-editorial-followup=open

- [ ] **Codex `codex/article-localization-042-seo-b` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`7707fb82a9624cd9cd39c6493c238a1c3bb8472f`。
  - 原始下一步：2026-09-28-batch042-pair-b-source-editorial-followup remains open
  - 任務：[2026-09-28-batch042-pair-b-install-reviewed-locales](../../tasks/done/2026-09-28-batch042-pair-b-install-reviewed-locales.md)（主幹 done）。
  - 任務：[2026-09-28-prepare-batch042-technical-roadmap-art](../../tasks/done/2026-09-28-prepare-batch042-technical-roadmap-art.md)（主幹 done）。
  - 任務：[2026-09-28-batch042-pair-b-release-reviewed-locales](../../tasks/done/2026-09-28-batch042-pair-b-release-reviewed-locales.md)（主幹 done）。
  - 任務：[2026-09-28-batch042-pair-b-source-editorial-followup](../../tasks/open/2026-09-28-batch042-pair-b-source-editorial-followup.md)（主幹 open）。
  - 優先核對路徑：`apps/api/app/guides/content/seo-learning-roadmap.json`, `apps/api/app/guides/content/technical-seo-checklist.json`, `apps/web/public/guides/seo-learning-roadmap/diagram-1-en.svg`, `apps/web/public/guides/seo-learning-roadmap/diagram-1-ja.svg`, `apps/web/public/guides/seo-learning-roadmap/diagram-1-ko.svg`, `apps/web/public/guides/seo-learning-roadmap/diagram-1-zh-cn.svg`, `apps/web/public/guides/seo-learning-roadmap/hero-en.jpg`, `apps/web/public/guides/seo-learning-roadmap/hero-en.svg` 等 27 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 4f282b0f23268e0a89df6b38ac147c81c9819edf
  - 保留證據：Linked main task remains unfinished: 2026-09-28-batch042-pair-b-source-editorial-followup=open

- [ ] **Codex `codex/article-localization-043-search-b` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`fbc82f78ee21937e63f69908a5a57f15b3105dba`。
  - 原始下一步：2026-09-28-review-batch043-inherited-editorial-intake-failures remains open
  - 任務：[2026-09-28-localize-batch043-search-results-and-semrush](../../tasks/done/2026-09-28-localize-batch043-search-results-and-semrush.md)（主幹 done）。
  - 任務：[2026-09-28-release-reviewed-batch043-search-results-and](../../tasks/done/2026-09-28-release-reviewed-batch043-search-results-and.md)（主幹 done）。
  - 任務：[2026-09-28-review-batch043-inherited-editorial-intake-failures](../../tasks/open/2026-09-28-review-batch043-inherited-editorial-intake-failures.md)（主幹 open）。
  - 優先核對路徑：`apps/api/app/guides/content/search-results-clickthrough.json`, `apps/api/app/guides/content/semrush-research-workflow.json`, `apps/web/public/guides/search-results-clickthrough/diagram-1-en.svg`, `apps/web/public/guides/search-results-clickthrough/diagram-1-ja.svg`, `apps/web/public/guides/search-results-clickthrough/diagram-1-ko.svg`, `apps/web/public/guides/search-results-clickthrough/diagram-1-zh-cn.svg`, `apps/web/public/guides/search-results-clickthrough/hero-en.jpg`, `apps/web/public/guides/search-results-clickthrough/hero-en.svg` 等 27 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 086e006cdfd5a982da9f412d28939ebb8eb4b453
  - 保留證據：Linked main task remains unfinished: 2026-09-28-review-batch043-inherited-editorial-intake-failures=open

- [ ] **Codex `codex/article-localization-batch-005` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`40d482aa1d56fa19a16df2bf56e2bc952ed142bf`。
  - 原始下一步：Only task bookkeeping or completion receipts differ; reconcile linked task IDs with current main done records before deleting.
  - 任務：`2026-09-20-article-localization-batch-005`（主幹 absent）。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/article-localization-batch-006` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`56d98e4decce9f760179665119c2821c350b7613`。
  - 原始下一步：Only task bookkeeping or completion receipts differ; reconcile linked task IDs with current main done records before deleting.
  - 任務：[2026-09-20-article-localization-batch-006-three-guides](../../tasks/done/2026-09-20-article-localization-batch-006-three-guides.md)（主幹 done）。
  - 任務：`2026-09-20-article-localization-batch-006`（主幹 absent）。
  - 任務：`2026-09-20-hanoi-old-quarter-vietnam-tourism-source`（主幹 absent）。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/article-localization-batch-011-korea` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`1fbd57ac8845c8d4f465be7a1914669386f26ee7`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/app/guides/content/jeju-car-rental-guide.json, apps/api/app/guides/content/nami-island-petite-france-day-trip.json
  - 任務：`2026-09-21-localize-three-korea-travel-guides-in`（主幹 absent）。
  - 優先核對路徑：`apps/api/app/guides/content/jeju-car-rental-guide.json`, `apps/api/app/guides/content/nami-island-petite-france-day-trip.json`。
  - 保留證據：Uncommitted content exists in checkout; never delete this checked-out branch or worktree.

- [ ] **Codex `codex/article-localization-batch016-llms` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`fd63272eba3b44d2f36f43bac128b0e5c72562de`。
  - 原始下一步：Preserve and reconcile uncommitted checkout files.
  - 任務：[2026-09-22-correct-llms-txt-evaluation-token-link](../../tasks/done/2026-09-22-correct-llms-txt-evaluation-token-link.md)（主幹 done）。
  - 任務：[2026-09-22-localize-llms-txt-evaluation-draft-only](../../tasks/done/2026-09-22-localize-llms-txt-evaluation-draft-only.md)（主幹 done）。
  - 優先核對路徑：`apps/api/app/guides/content/llms-txt-evaluation.json`, `apps/web/public/guides/llms-txt-evaluation/diagram-1-en.svg`, `apps/web/public/guides/llms-txt-evaluation/diagram-1-ja.svg`, `apps/web/public/guides/llms-txt-evaluation/diagram-1-ko.svg`, `apps/web/public/guides/llms-txt-evaluation/diagram-1-zh-cn.svg`, `apps/web/public/guides/llms-txt-evaluation/hero-en.jpg`, `apps/web/public/guides/llms-txt-evaluation/hero-en.svg`, `apps/web/public/guides/llms-txt-evaluation/hero-ja.jpg` 等 13 個路徑。
  - 保留證據：Every non-task changed path blob/deletion has been delivered in origin/main history; no linked task remains open. See per-path landedHistoricallyAt.
  - 保留證據：Uncommitted content exists in checkout; never delete this checked-out branch or worktree.

- [ ] **Codex `codex/article-localization-batch028-release-prep` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`bdd08fd7c92e89c161840e7d478c119f2a4ef3b3`。
  - 原始下一步：Only task bookkeeping or completion receipts differ; reconcile linked task IDs with current main done records before deleting.
  - 任務：`2026-09-27-release-wordpress-presentation-guides-batch028`（主幹 absent）。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/article-localization-source-edit-preservation` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`a80f6b5faef47a17c862e8a981d78f5f3b4cfd06`。
  - 原始下一步：Preserve and reconcile uncommitted checkout files.
  - 任務：[2026-09-21-authorize-reviewed-source-corrections-in-localization](../../tasks/done/2026-09-21-authorize-reviewed-source-corrections-in-localization.md)（主幹 done）。
  - 任務：[2026-09-22-compare-deployed-localization-packs-by-validated](../../tasks/done/2026-09-22-compare-deployed-localization-packs-by-validated.md)（主幹 done）。
  - 任務：[2026-09-22-preserve-reviewed-unselected-repository-locale-edits](../../tasks/done/2026-09-22-preserve-reviewed-unselected-repository-locale-edits.md)（主幹 done）。
  - 優先核對路徑：`docs/article-localization/assemble_bundle.py`, `docs/article-localization/publish_bundle.py`, `docs/article-localization/repository_preservation.py`, `docs/article-localization/test_assemble_bundle.py`, `docs/article-localization/test_publish_bundle.py`。
  - 保留證據：Every non-task changed path blob/deletion has been delivered in origin/main history; no linked task remains open. See per-path landedHistoricallyAt.
  - 保留證據：Uncommitted content exists in checkout; never delete this checked-out branch or worktree.

- [ ] **Codex `codex/batch003-qa-tasks` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`3e072badac7c2a25e2d96ed4656536550cfb6feb`。
  - 原始下一步：2026-09-20-five-language-article-batch-003 remains open
  - 任務：[2026-09-20-five-language-article-batch-003](../../tasks/open/2026-09-20-five-language-article-batch-003.md)（主幹 open）。
  - 保留證據：Linked main task remains unfinished: 2026-09-20-five-language-article-batch-003=open

- [ ] **Codex `codex/batch029-release-prep` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`6bb1d6c701819b5fbd56ca8a1362ede6b7843602`。
  - 原始下一步：Only task bookkeeping or completion receipts differ; reconcile linked task IDs with current main done records before deleting.
  - 任務：`2026-09-27-batch029-wordpress-contact-release-prep`（主幹 absent）。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/localization-release-permissions-task` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`95ffc2fa91b04c53f900489d3fcfa6a14bf8cdfd`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-20-fix-nonroot-source-mount-permissions-in. Keep the branch pending this reconciliation.
  - 任務：[2026-09-20-fix-nonroot-source-mount-permissions-in](../../tasks/open/2026-09-20-fix-nonroot-source-mount-permissions-in.md)（主幹 open）；Fix nonroot source mount permissions in article localization release。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr899-locale-review` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`9b915eed53750e8918fae653efb2831999f91f56`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/guides/content/email-newsletter-planning.json, apps/api/app/guides/content/mailchimp-wordpress-newsletter.json, apps/web/public/guides/email-newsletter-planning/diagram-1-ja.svg, docs/article-localization/batch035-newsletter-pair-a-evidence.md, docs/article-localization/batch035-newsletter-pair-a-merge-review.md. Reconcile current open/missing task IDs: 2026-09-28-correct-email-address-wording-in-newsletter. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-correct-email-address-wording-in-newsletter`（主幹 missing）。
  - 任務：[2026-09-28-localize-newsletter-pair-a-in-five](../../tasks/done/2026-09-28-localize-newsletter-pair-a-in-five.md)（主幹 done）；Localize newsletter pair A in five languages；原認領 codex-batch035-newsletter-pair-a。
  - 優先核對路徑：`apps/api/app/guides/content/email-newsletter-planning.json`, `apps/api/app/guides/content/mailchimp-wordpress-newsletter.json`, `apps/web/public/guides/email-newsletter-planning/diagram-1-ja.svg`, `apps/web/public/guides/mailchimp-wordpress-newsletter/diagram-1-zh-cn.svg`, `docs/article-localization/batch035-newsletter-pair-a-evidence.md`, `docs/article-localization/batch035-newsletter-pair-a-merge-review.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/sothatswhy-season2-batch09` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`aa203808e0729b9c66bea1c3d611a353dc8952ad`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-10-01-sothatswhy-season1-launch-buffer, 2026-10-01-sothatswhy-season3-production-packages. Keep the branch pending this reconciliation.
  - 任務：[2026-10-01-a31-atm-tactile-standard-evidence](../../tasks/done/2026-10-01-a31-atm-tactile-standard-evidence.md)（主幹 done）；修正 A31 舊查核把 ATM 5 鍵觸覺規定誤寫成電梯凸點規定；原認領 codex-a31-evidence。
  - 任務：[2026-10-01-b37-fy2025-evidence-rounding](../../tasks/done/2026-10-01-b37-fy2025-evidence-rounding.md)（主幹 done）；B37 原題查核摘要：修正 FY2025 AWS 億美元約數；原認領 codex-b37-evidence。
  - 任務：[2026-10-01-knowledge-story-backlog](../../tasks/done/2026-10-01-knowledge-story-backlog.md)（主幹 done）；Restore knowledge explainer and short-story planning backlog；原認領 codex-knowledge-story。
  - 任務：[2026-10-01-sothatswhy-season1-launch-buffer](../../tasks/open/2026-10-01-sothatswhy-season1-launch-buffer.md)（主幹 open）；原來如此第一季：試片後建立首批庫存與開播交接。
  - 任務：[2026-10-01-sothatswhy-season2-batch01](../../tasks/done/2026-10-01-sothatswhy-season2-batch01.md)（主幹 done）；原來如此第二季首批：B26 S26 T26 A31 四集製作包與獨立審稿；原認領 codex-sothatswhy-batch01。
  - 任務：[2026-10-01-sothatswhy-season2-batch02](../../tasks/done/2026-10-01-sothatswhy-season2-batch02.md)（主幹 done）；原來如此第二季第二批：B27 S27 T28 A33 製作包與獨立審稿；原認領 codex-sothatswhy-batch02。
  - 任務：[2026-10-01-sothatswhy-season2-batch03](../../tasks/done/2026-10-01-sothatswhy-season2-batch03.md)（主幹 done）；原來如此第二季第三批：B48 S44 T33 A36 製作包與獨立審稿；原認領 codex-sothatswhy-batch03。
  - 任務：[2026-10-01-sothatswhy-season2-batch04](../../tasks/done/2026-10-01-sothatswhy-season2-batch04.md)（主幹 done）；原來如此第二季第四批：B37 S31 T29 A41 製作包與獨立審稿；原認領 codex-sothatswhy-batch04。
  - 任務：[2026-10-01-sothatswhy-season2-batch05](../../tasks/done/2026-10-01-sothatswhy-season2-batch05.md)（主幹 done）；原來如此第二季第五批：B46 S32 T41 A40 製作包與獨立審稿；原認領 codex-sothatswhy-batch05。
  - 任務：[2026-10-01-sothatswhy-season2-batch06](../../tasks/done/2026-10-01-sothatswhy-season2-batch06.md)（主幹 done）；原來如此第二季第六批：B44 S43 T43 A46 製作包與獨立審稿；原認領 codex-sothatswhy-batch06。
  - 任務：[2026-10-01-sothatswhy-season2-batch07](../../tasks/done/2026-10-01-sothatswhy-season2-batch07.md)（主幹 done）；原來如此第二季第七批：B47 S48 T48 A44 製作包與獨立審稿；原認領 codex-sothatswhy-batch07。
  - 任務：[2026-10-01-sothatswhy-season2-batch08](../../tasks/done/2026-10-01-sothatswhy-season2-batch08.md)（主幹 done）；原來如此第二季第八批：B50 S36 T45 A39 製作包與獨立審稿；原認領 codex-sothatswhy-batch08。
  - 任務：[2026-10-01-sothatswhy-season2-batch09](../../tasks/done/2026-10-01-sothatswhy-season2-batch09.md)（主幹 done）；原來如此第二季第九批：B42 S35 T35 A37 製作包與獨立審稿；原認領 codex-sothatswhy-batch09。
  - 任務：[2026-10-01-sothatswhy-season2-production-packages](../../tasks/done/2026-10-01-sothatswhy-season2-production-packages.md)（主幹 done）；原來如此第二季：把已查核候選題整理成製作包；原認領 codex-root。
  - 任務：[2026-10-01-sothatswhy-season3-production-packages](../../tasks/open/2026-10-01-sothatswhy-season3-production-packages.md)（主幹 open）；原來如此第三季：把已查核候選題整理成製作包。
  - 優先核對路徑：`docs/videos/KNOWLEDGE-STORIES.md`, `docs/videos/so-thats-why/season2-topics.json`, `docs/videos/so-thats-why/season2/README.md`, `docs/videos/so-thats-why/season2/validate.mjs`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.


### 影片、配音與漫劇（21）

- [ ] **Claude `backup/dub-retry-local-merge` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`c54a97efe23b71fbaca668642bd54e5ed28eb51f`。
  - 原始下一步：Finish or reconcile the listed task IDs before cleanup.
  - 任務：[2026-10-10-let-the-owner-re-request-a](../../tasks/open/2026-10-10-let-the-owner-re-request-a.md)（主幹 open）；Let the owner re-request a skipped dub from the languages card；原認領 claude-opus-5-5。
  - 任務：[2026-10-11-a-sent-back-newest-languages-batch](../../tasks/open/2026-10-11-a-sent-back-newest-languages-batch.md)（主幹 open）；A sent-back newest languages batch leaves every part unfinished and the worker re-sending it。
  - 任務：[2026-10-11-make-a-dub-again-on-a](../../tasks/open/2026-10-11-make-a-dub-again-on-a.md)（主幹 open）；Make a dub again on a video whose work files were tidied。
  - 優先核對路徑：`apps/api/app/models.py`, `apps/api/app/video_reviews/admin_api.py`, `apps/api/app/video_reviews/admin_service.py`, `apps/api/app/video_reviews/dub_retry.py`, `apps/api/app/video_reviews/producer_state.py`, `apps/api/app/video_reviews/schemas.py`, `apps/api/migrations/versions/0131_video_dub_retries.py`, `apps/api/tests/test_migration_0131_video_dub_retries.py` 等 30 個路徑。
  - 保留證據：Associated task remains open on main

- [ ] **Claude `claude/ai-terminology-video-series-c1754d` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`92e3ae6ba64b75243b6127da2c09d4b96470f0c5`。
  - 原始下一步：Finish or reconcile the listed task IDs before cleanup.
  - 任務：[2026-09-29-ai-terms-video-pilot](../../tasks/open/2026-09-29-ai-terms-video-pilot.md)（主幹 open）；AI 名詞影片系列：前三集試片（token、上下文視窗、RAG）；原認領 claude-opus-5-5。
  - 任務：`2026-10-04-a-four-line-quote-card-loses`（主幹 absent）；A four-line quote card loses the bottom of its last line。
  - 任務：`2026-10-04-a-slides-storyboard-whose-pictures-all`（主幹 absent）；A slides storyboard whose pictures all passed still waits for the owner when any carries a judge note。
  - 任務：`2026-10-04-produce-the-ai-terms-overview-episode`（主幹 absent）；Produce the AI terms overview episode: prompt to graph engineering；原認領 claude-opus-5-5。
  - 任務：`2026-10-04-shot-prompts-put-the-look-first`（主幹 absent）；Shot prompts put the look first for image models that take no style reference。
  - 優先核對路徑：`docs/videos/ai-term-context-window/brief.md`, `docs/videos/ai-term-context-window/claims.md`, `docs/videos/ai-term-context-window/video.json`, `docs/videos/ai-term-retrieval-augmented-generation/brief.md`, `docs/videos/ai-term-retrieval-augmented-generation/claims.md`, `docs/videos/ai-term-retrieval-augmented-generation/video.json`, `docs/videos/ai-term-token/brief.md`, `docs/videos/ai-term-token/claims.md` 等 12 個路徑。
  - 保留證據：Associated task remains open on main

- [ ] **Claude `claude/continue-task-ad1ac7` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`1381413254878c79eb1090fe2ea62d996a6f1dff`。
  - 原始下一步：Keep the draft source and file a reconciliation task comparing it with the accepted plan; preserve the main clip-route pilot task independently.
  - 任務：[2026-10-04-clip-route-pilot-comparison](../../tasks/open/2026-10-04-clip-route-pilot-comparison.md)（主幹 open）；試拍比價：同兩鏡在 Kling CLI、Hailuo 網頁、伺服器 Lite 各生一支，量點數、解析度、速度、PSNR 後定整部的片段路線。
  - 任務：[2026-10-04-no-return-arrow-plan](../../tasks/done/2026-10-04-no-return-arrow-plan.md)（主幹 done）；無歸箭：取材經典布袋戲結構的長篇漫劇企劃包（期一 24 集與全系列路線圖）；原認領 claude。
  - 優先核對路徑：`docs/videos/series-plans/no-return-arrow/README.md`, `docs/videos/series-plans/no-return-arrow/authoring-contract.json`, `docs/videos/series-plans/no-return-arrow/build.mjs`, `docs/videos/series-plans/no-return-arrow/continuity.csv`, `docs/videos/series-plans/no-return-arrow/continuity.md`, `docs/videos/series-plans/no-return-arrow/documents.json`, `docs/videos/series-plans/no-return-arrow/manifest.json`, `docs/videos/series-plans/no-return-arrow/outline.json` 等 19 個路徑。
  - 保留證據：No merged PR head covers 1381413254878c79eb1090fe2ea62d996a6f1dff.
  - 保留證據：Draft source: docs/videos/series-plans/no-return-arrow; includes 24-episode continuity and setting package.
  - 保留證據：Main task 2026-10-04-no-return-arrow-plan is done; the source reconciliation remains unproved.

- [ ] **Claude `claude/ou-de-jianghu-e001-285512` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`38e062ada2c7a315aed644e051cfaa85aeaa596d`。
  - 盤點期間有新提交，目前 HEAD：`22ee6f1338f11ce48c84c28631ff6f2d1cc489b4`，完整保留；續作前重讀此分支。
  - 原始下一步：Keep the active production branch and worktree; continue from current video/media receipts. Do not delete while the episode-one Claude session or production handoff is active.
  - 任務：`2026-10-08-ou-de-jianghu-art-direction`（主幹 absent）；《偶的江湖》角色美術定調：三位主角候選與共同畫風；原認領 codex-ou-de-jianghu-art。
  - 任務：`2026-10-08-ou-de-jianghu-external-look-import`（主幹 absent）；《偶的江湖》角色設定圖外部匯入：採用畫像接入正常look與跨集參照；原認領 codex-ou-import。
  - 任務：`2026-10-08-ou-de-jianghu-visual-preproduction`（主幹 absent）；《偶的江湖》補齊角色美術前期規格與任務鏈；原認領 codex-ou-de-jianghu-art。
  - 任務：`2026-10-08-animatic-title-gap-subtitle-boundary`（主幹 absent）；Animatic skips title spans and crashes subtitle lookup before next shot。
  - 任務：`2026-10-08-integrate-external-look-import-duration-review`（主幹 absent）；Integrate external look import duration review after PR 1387 receipt reconciliation。
  - 任務：`2026-10-08-ou-de-jianghu-animation-reference`（主幹 absent）；《偶的江湖》第一集角色動畫參照：多視圖、表情與動作。
  - 任務：`2026-10-08-ou-de-jianghu-episode1-portraits`（主幹 absent）；《偶的江湖》第一集9位角色畫像與全身定妝。
  - 任務：`2026-10-08-ou-de-jianghu-preflight-plan`（主幹 absent）；《偶的江湖》第1集開拍前置包：文字動態分鏡、路線與美術預算。
  - 任務：`2026-10-08-ou-de-jianghu-scene-prop-design`（主幹 absent）；《偶的江湖》第一集場景與道具美術參照及連戲細節。
  - 任務：`2026-10-08-ou-de-jianghu-supporting-looks`（主幹 absent）；《偶的江湖》後續角色畫像、16種命名造型與隱藏身份清冊。
  - 任務：`2026-10-08-ou-de-jianghu-visual-handoff`（主幹 absent）；《偶的江湖》角色資產鎖定與第一集動畫試播交接；原認領 claude-fable-5.1。
  - 任務：`2026-10-08-validate-windows-stock-path-and-brightness`（主幹 absent）；Validate Windows stock path and brightness fixture regressions。
  - 優先核對路徑：`.agents/skills/animation-production/SKILL.md`, `.agents/skills/animation-production/references/browser-production.md`, `.agents/skills/animation-production/references/in-app-browser-hailuo.md`, `.claude/skills/animation-production/SKILL.md`, `docs/videos/series-plans/ou-de-jianghu/visual-development/README.md`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/README.md`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/build-final-gallery.mjs`, `docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/build-receipt.mjs` 等 111 個路徑。
  - 保留證據：Checked-out worktree is dirty or has a live Claude session; preserve its branch

- [ ] **Claude `claude/video-batch-2` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`85da5f2cbc06572e74fc1c6f0c3062880a9ffd83`。
  - 原始下一步：Finish or reconcile the listed task IDs before cleanup.
  - 任務：[2026-09-24-video-pilot-ai-model-choice](../../tasks/open/2026-09-24-video-pilot-ai-model-choice.md)（主幹 open）；影片產線 T6：試作影片〈AI 模型怎麼挑〉；原認領 claude-opus-5-5。
  - 任務：`2026-09-24-video-speaking-rate`（主幹 absent）；影片長度估計改用聲音的實際語速，不固定每分鐘 250 字。
  - 任務：`2026-09-25-video-ai-agent-permissions`（主幹 absent）；影片：AI 代理人越界事件，和你該先設好的三道權限；原認領 claude-opus-5-5。
  - 任務：`2026-09-25-video-chatgpt-ads-upgrade`（主幹 absent）；影片：ChatGPT 開始有廣告了，免費版、Go、Plus 要不要升級；原認領 claude-opus-5-5。
  - 任務：`2026-09-25-video-gemini-student-offer`（主幹 absent）；影片：Google AI 學生方案免費一年，台灣大學生怎麼領，加上 Gemini Notebook 讀書流程；原認領 claude-opus-5-5。
  - 優先核對路徑：`docs/videos/README.md`, `docs/videos/ai-agent-permissions/brief.md`, `docs/videos/ai-agent-permissions/claims.md`, `docs/videos/ai-agent-permissions/i18n/en.json`, `docs/videos/ai-agent-permissions/i18n/ja.json`, `docs/videos/ai-agent-permissions/i18n/ko.json`, `docs/videos/ai-agent-permissions/i18n/zh-CN.json`, `docs/videos/ai-agent-permissions/verify-1.md` 等 40 個路徑。
  - 保留證據：Associated task remains open on main

- [ ] **Claude `claude/video-dubs-worker` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`841cb719be8a0a3295bd73b46a5a2d2c073f21eb`。
  - 原始下一步：Inspect unmatched changes and remaining acceptance steps.
  - 任務：[2026-09-26-video-dubs-captions-package](../../tasks/done/2026-09-26-video-dubs-captions-package.md)（主幹 done）；Video dubs: captions follow the dub timeline, the upload package carries the tracks, UPLOAD.md gets the Languages steps；原認領 claude-fable-5-1-video-dubs。
  - 任務：[2026-09-26-video-dubs-worker](../../tasks/done/2026-09-26-video-dubs-worker.md)（主幹 done）；Video dubs: the worker synthesizes, shortens, checks and packages the tracks, and qa reports them；原認領 claude-fable-5-1-video-dubs。
  - 任務：`2026-09-27-trip-parser-test-utc-midnight`（主幹 absent）；test_ai_trip_parser_llm fixes TODAY at import and fails when the api job crosses UTC midnight。
  - 優先核對路徑：`.agents/skills/youtube-video/references/automated.md`, `.agents/skills/youtube-video/references/prompts/caption-review.md`, `.agents/skills/youtube-video/references/prompts/caption-translate.md`, `.agents/skills/youtube-video/references/publish.md`, `docs/videos/AUTOMATION.md`, `tools/video/automation/dubs.mjs`, `tools/video/automation/dubs.test.mjs`, `tools/video/automation/flow.mjs` 等 18 個路徑。
  - 保留證據：Unique work needs review before cleanup

- [ ] **Claude `claude/video-pilot` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`d913dcdba5d1b3a33c26044da4cedfff0136f0de`。
  - 原始下一步：Finish or reconcile the listed task IDs before cleanup.
  - 任務：[2026-09-24-video-pilot-ai-model-choice](../../tasks/open/2026-09-24-video-pilot-ai-model-choice.md)（主幹 open）；影片產線 T6：試作影片〈AI 模型怎麼挑〉；原認領 claude-opus-5-5。
  - 任務：`2026-09-24-video-speaking-rate`（主幹 absent）；影片長度估計改用聲音的實際語速，不固定每分鐘 250 字。
  - 優先核對路徑：`docs/videos/README.md`, `docs/videos/ai-model-choice/brief.md`, `docs/videos/ai-model-choice/claims.md`, `docs/videos/ai-model-choice/cost-flows.svg`, `docs/videos/ai-model-choice/verify-1.md`, `docs/videos/ai-model-choice/verify-2.md`, `docs/videos/ai-model-choice/video.json`, `docs/videos/lexicon.json`。
  - 保留證據：Associated task remains open on main

- [ ] **Claude `claude/video-pilot-audio` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`f4ebe05505450e4552505b3fc3d8dd83d5b2144c`。
  - 原始下一步：Finish or reconcile the listed task IDs before cleanup.
  - 任務：[2026-09-24-video-pilot-ai-model-choice](../../tasks/open/2026-09-24-video-pilot-ai-model-choice.md)（主幹 open）；影片產線 T6：試作影片〈AI 模型怎麼挑〉；原認領 claude-opus-5-5。
  - 任務：`2026-09-24-video-speaking-rate`（主幹 absent）；影片長度估計改用聲音的實際語速，不固定每分鐘 250 字。
  - 優先核對路徑：`docs/videos/README.md`, `docs/videos/ai-model-choice/brief.md`, `docs/videos/ai-model-choice/claims.md`, `docs/videos/ai-model-choice/cost-flows.svg`, `docs/videos/ai-model-choice/i18n/en.json`, `docs/videos/ai-model-choice/i18n/ja.json`, `docs/videos/ai-model-choice/i18n/ko.json`, `docs/videos/ai-model-choice/i18n/zh-CN.json` 等 12 個路徑。
  - 保留證據：Associated task remains open on main

- [ ] **Claude `claude/youtube-language-manifest` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`3e61f790e542fda088f650fdf025e4b5522c2399`。
  - 原始下一步：Keep the branch/worktree; file or restore the source-bound producer-manifest follow-up on main, compare against current language-package contracts, then implement/review the required integration.
  - 任務：[2026-09-30-youtube-approved-languages-sync](../../tasks/done/2026-09-30-youtube-approved-languages-sync.md)（主幹 done）；YouTube sync reads stale publish package after approved languages；原認領 claude-opus-5-5-youtube-language-manifest。
  - 任務：`2026-10-06-bind-tidied-language-batches-and-prove`（主幹 absent）；Bind tidied language batches and prove one approved-language upload end to end。
  - 優先核對路徑：`apps/api/tests/fixtures/video_language_manifest_v1.json`, `apps/api/tests/test_video_youtube_language_package.py`, `docs/videos/APPROVED-LANGUAGE-PACKAGE.md`, `tools/video/review/language-source.mjs`, `tools/video/review/language-source.test.mjs`, `tools/video/review/sync.mjs`, `tools/video/review/sync.test.mjs`。
  - 保留證據：Current head 3e61f790e542fda088f650fdf025e4b5522c2399; clean checked-out worktree C:/Users/x8120/mokaair/.claude/worktrees/wf_3eff2890-671-8.
  - 保留證據：No merged PR head in the audited object graph covers this head.
  - 保留證據：Unshared open follow-up: 2026-10-06-bind-tidied-language-batches-and-prove.

- [ ] **Claude `wf-fix-1342` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`d98a1471eaedd070bc94e726b262b7bd65b87adb`。
  - 原始下一步：Keep the dirty worktree; preserve and inspect its 12 uncommitted paths. The historical feature tasks are already done on main, so isolate the remaining local work before any cleanup.
  - 任務：[2026-10-06-a-failing-video-is-deferred](../../tasks/done/2026-10-06-a-failing-video-is-deferred.md)（主幹 done）；A failing video is deferred on its own instead of halting the lane；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-pictures-keep-best-after-prompt-fixes](../../tasks/done/2026-10-06-pictures-keep-best-after-prompt-fixes.md)（主幹 done）；Pictures a model takes no style plate for are judged from the look's text, and a slides shot still failing after its prompt fixes keeps its best picture for the owner's final review；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-an-owner-retry-resets-the-counter](../../tasks/done/2026-10-06-an-owner-retry-resets-the-counter.md)（主幹 done）；An owner retry resets the counter that blocked the video and a new seed replaces an exhausted picture request；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-image-prompts-fit-the-chosen-image](../../tasks/done/2026-10-06-image-prompts-fit-the-chosen-image.md)（主幹 done）；Image prompts fit the chosen image model's limit (MiniMax 1500) instead of being refused；原認領 claude-fable-5-1-video-unstuck。
  - 任務：[2026-10-06-a-stale-writer-receipt-looks-the](../../tasks/done/2026-10-06-a-stale-writer-receipt-looks-the.md)（主幹 done）；A stale writer receipt looks the saved job up and archives it when it is over instead of blocking the video；原認領 claude-fable-5-1-video-unstuck。
  - 優先核對路徑：`apps/api/app/video_automation/schemas.py`, `apps/api/app/video_automation/settings.py`, `apps/api/app/video_media/catalog.py`, `apps/api/tests/test_video_automation_settings.py`, `apps/api/tests/test_video_media_api.py`, `apps/api/tests/test_video_media_catalog.py`, `docs/videos/ILLUSTRATED.md`, `docs/videos/long-form/review.json` 等 30 個路徑。
  - 保留證據：Checked-out worktree is dirty or has a live Claude session; preserve its branch

- [ ] **Codex `codex/ai-developer-videos` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`d9c3e8e7b95810aca014559eb927392d873765e1`。
  - 原始下一步：2026-09-27-developer-ai-bug-fix-pr-review remains open
  - 原始下一步：2026-09-27-developer-ai-coding-tool-comparison-video remains open
  - 任務：[2026-09-27-developer-ai-bug-fix-pr-review](../../tasks/open/2026-09-27-developer-ai-bug-fix-pr-review.md)（主幹 open）。
  - 任務：[2026-09-27-developer-ai-coding-tool-comparison-video](../../tasks/open/2026-09-27-developer-ai-coding-tool-comparison-video.md)（主幹 open）。
  - 優先核對路徑：`docs/videos/ai-bug-fix-pr-review/brief.md`, `docs/videos/ai-bug-fix-pr-review/claims.md`, `docs/videos/ai-bug-fix-pr-review/demo/README.md`, `docs/videos/ai-bug-fix-pr-review/demo/acceptance.test.mjs`, `docs/videos/ai-bug-fix-pr-review/demo/claude-acceptance-output.txt`, `docs/videos/ai-bug-fix-pr-review/demo/claude-acceptance.png`, `docs/videos/ai-bug-fix-pr-review/demo/claude.patch`, `docs/videos/ai-bug-fix-pr-review/demo/fare.mjs` 等 34 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit d61b699290a70c6a108660eb4a2554192141e62a
  - 保留證據：Linked main task remains unfinished: 2026-09-27-developer-ai-bug-fix-pr-review=open, 2026-09-27-developer-ai-coding-tool-comparison-video=open

- [ ] **Codex `codex/ai-general-videos` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`7a2dd684234a59b4d992987753ce24bb96790bee`。
  - 原始下一步：2026-09-27-ai-video-batch-first-week-analytics remains open
  - 原始下一步：2026-09-27-general-audience-ai-agent-versus-chatbot remains open
  - 原始下一步：2026-09-27-general-audience-ai-citation-checking-video remains open
  - 任務：[2026-09-27-ai-video-batch-first-week-analytics](../../tasks/open/2026-09-27-ai-video-batch-first-week-analytics.md)（主幹 open）。
  - 任務：[2026-09-27-general-audience-ai-agent-versus-chatbot](../../tasks/open/2026-09-27-general-audience-ai-agent-versus-chatbot.md)（主幹 open）。
  - 任務：[2026-09-27-general-audience-ai-citation-checking-video](../../tasks/open/2026-09-27-general-audience-ai-citation-checking-video.md)（主幹 open）。
  - 優先核對路徑：`docs/videos/ai-agent-vs-chatbot/brief.md`, `docs/videos/ai-agent-vs-chatbot/claims.md`, `docs/videos/ai-agent-vs-chatbot/demo-log.md`, `docs/videos/ai-agent-vs-chatbot/i18n/en.json`, `docs/videos/ai-agent-vs-chatbot/i18n/ja.json`, `docs/videos/ai-agent-vs-chatbot/i18n/ko.json`, `docs/videos/ai-agent-vs-chatbot/i18n/zh-CN.json`, `docs/videos/ai-agent-vs-chatbot/verify-1.md` 等 18 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit ec383889f6d5ae582d07c350b5755899300aa4e7
  - 保留證據：Linked main task remains unfinished: 2026-09-27-ai-video-batch-first-week-analytics=open, 2026-09-27-general-audience-ai-agent-versus-chatbot=open, 2026-09-27-general-audience-ai-citation-checking-video=open

- [ ] **Codex `codex/ai-video-season-01` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`226f11725803b43782fc2e1ce15c0ec960261ba9`。
  - 原始下一步：2026-09-28-ai-season-one-final-review remains open
  - 任務：[2026-09-28-ai-video-season-one-review-pack](../../tasks/done/2026-09-28-ai-video-season-one-review-pack.md)（主幹 done）。
  - 任務：[2026-09-28-ai-season-one-final-review](../../tasks/open/2026-09-28-ai-season-one-final-review.md)（主幹 open）。
  - 優先核對路徑：`docs/ai-video-season-01/.gitignore`, `docs/ai-video-season-01/README.md`, `docs/ai-video-season-01/analytics.csv`, `docs/ai-video-season-01/assets/01-thumbnail-a.png`, `docs/ai-video-season-01/assets/01-thumbnail-b.png`, `docs/ai-video-season-01/assets/02-thumbnail-a.png`, `docs/ai-video-season-01/assets/02-thumbnail-b.png`, `docs/ai-video-season-01/assets/03-thumbnail-a.png` 等 149 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 9081d0a2b07f46eb6f442d05fc85f1c96134ee14
  - 保留證據：Linked main task remains unfinished: 2026-09-28-ai-season-one-final-review=open

- [ ] **Codex `codex/drama-competition-wedding-20261002` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`fac0cb96ed2014b5c5f9327ca7234511b1ac2f81`。
  - 原始下一步：2026-10-02-run-the-two-wedding-episodes-with remains open
  - 原始下一步：2026-10-02-wedding-competition-pilot-four-languages remains open
  - 任務：[2026-10-02-drama-competition-wedding-final](../../tasks/done/2026-10-02-drama-competition-wedding-final.md)（主幹 done）。
  - 任務：[2026-10-02-honor-veo-lite-negativeprompt-compatibility](../../tasks/done/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md)（主幹 done）。
  - 任務：[2026-10-02-keep-character-look-review-identities-distinct](../../tasks/done/2026-10-02-keep-character-look-review-identities-distinct.md)（主幹 done）。
  - 任務：[2026-10-02-keep-named-look-clip-judge-questions](../../tasks/done/2026-10-02-keep-named-look-clip-judge-questions.md)（主幹 done）。
  - 任務：[2026-10-02-preserve-sanitized-video-provider-rejection-details](../../tasks/done/2026-10-02-preserve-sanitized-video-provider-rejection-details.md)（主幹 done）。
  - 任務：[2026-10-02-run-the-two-wedding-episodes-with](../../tasks/open/2026-10-02-run-the-two-wedding-episodes-with.md)（主幹 open）。
  - 任務：[2026-10-02-wedding-competition-pilot-four-languages](../../tasks/open/2026-10-02-wedding-competition-pilot-four-languages.md)（主幹 open）。
  - 優先核對路徑：`apps/api/tests/test_scoped_drama.py`, `docs/videos/series-plans/competition-20261002/README.md`, `docs/videos/series-plans/competition-20261002/budget-and-launch.md`, `docs/videos/series-plans/competition-20261002/competition.json`, `docs/videos/series-plans/competition-20261002/cost-ledger.csv`, `docs/videos/series-plans/competition-20261002/episodes/audio-check-summary.json`, `docs/videos/series-plans/competition-20261002/episodes/build-audio-preview.py`, `docs/videos/series-plans/competition-20261002/episodes/episode-01-brief.md` 等 55 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 1c7ed24de0e5321ece01a42b4eb4b999e1ec7211
  - 保留證據：Linked main task remains unfinished: 2026-10-02-run-the-two-wedding-episodes-with=open, 2026-10-02-wedding-competition-pilot-four-languages=open

- [ ] **Codex `codex/import-reviewed-drama-plans` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`b8c38832fb36d177b0363f957d6f50ea55377a2a`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-28-verify-imported-review-pages-and-reconcile. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-pr881-drama-plan-admin-import](../../tasks/done/2026-09-28-pr881-drama-plan-admin-import.md)（主幹 done）；Import authored drama and video plans for admin review；原認領 codex-drama-plan-import。
  - 任務：[2026-09-28-verify-imported-review-pages-and-reconcile](../../tasks/open/2026-09-28-verify-imported-review-pages-and-reconcile.md)（主幹 open）；Verify imported review pages and reconcile remaining video previews。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/knowledge-story-backlog` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`55de2dadfda62946276c29e359ae0576c341c6a4`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-10-01-sothatswhy-season1-launch-buffer, 2026-10-01-sothatswhy-season3-production-packages. Keep the branch pending this reconciliation.
  - 任務：[2026-10-01-knowledge-story-backlog](../../tasks/done/2026-10-01-knowledge-story-backlog.md)（主幹 done）；Restore knowledge explainer and short-story planning backlog；原認領 codex-knowledge-story。
  - 任務：[2026-10-01-sothatswhy-season1-launch-buffer](../../tasks/open/2026-10-01-sothatswhy-season1-launch-buffer.md)（主幹 open）；原來如此第一季：試片後建立首批庫存與開播交接。
  - 任務：[2026-10-01-sothatswhy-season2-production-packages](../../tasks/done/2026-10-01-sothatswhy-season2-production-packages.md)（主幹 done）；原來如此第二季：把已查核候選題整理成製作包；原認領 codex-root。
  - 任務：[2026-10-01-sothatswhy-season3-production-packages](../../tasks/open/2026-10-01-sothatswhy-season3-production-packages.md)（主幹 open）；原來如此第三季：把已查核候選題整理成製作包。
  - 優先核對路徑：`docs/videos/KNOWLEDGE-STORIES.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr897-story-conflict` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`5a759a5b24aed881a898d71bf14c7ed97358d59f`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/videos/STORY.md. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-resolve-narrator-story-merge-conflicts](../../tasks/done/2026-09-28-resolve-narrator-story-merge-conflicts.md)（主幹 done）；Resolve narrator story merge conflicts；原認領 codex-pr-merge-watch。
  - 任務：[2026-09-28-video-story-core-narrator-only](../../tasks/done/2026-09-28-video-story-core-narrator-only.md)（主幹 done）；沒有角色的漫劇跳過設定圖，加上故事的 lint 規則；原認領 claude-opus-5-5-video-story-core。
  - 優先核對路徑：`.github/workflows/video-tooling.yml`, `docs/videos/STORY.md`, `tools/video/assemble/smoke.mjs`, `tools/video/core/fixtures/load.mjs`, `tools/video/core/lint.mjs`, `tools/video/core/lint.test.mjs`, `tools/video/core/state.mjs`, `tools/video/core/state.test.mjs` 等 10 個路徑。
  - 保留證據：Merged PR exists but local non-task scope differs, so completion is not proven by the PR alone.

- [ ] **Codex `codex/stalled-video-reviewed-fixes-pre-oct9-rebase` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`8bac279ed87abe38aa7f29379643a05a52960f7a`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/videos/long-form/review.json, docs/videos/long-form/review.md, docs/videos/recovery/2026-10-08-stalled-production.md, tools/video/assemble/branding-smoke.mjs, tools/video/assemble/branding.mjs, tools/video/assemble/branding.test.mjs, tools/video/qa/cli.mjs, tools/video/qa/qa.test.mjs (and 2 more paths listed in pathBlobEvidence). Reconcile current open/missing task IDs: 2026-10-08-make-durable-polling-deadline-regression-deterministic, 2026-10-08-preserve-translator-critique-and-final-when, 2026-10-08-retain-existing-guide-packs-in-imported, 2026-10-08-stalled-production-video-completion, 2026-10-08-use-normal-caption-warnings-and-local, 2026-10-08-video-audio-closing-particle-boundaries, 2026-10-08-video-branding-true-peak, 2026-10-08-video-qa-undecided-languages. Keep the branch pending this reconciliation.
  - 任務：`2026-10-08-make-durable-polling-deadline-regression-deterministic`（主幹 missing）。
  - 任務：`2026-10-08-preserve-translator-critique-and-final-when`（主幹 missing）。
  - 任務：`2026-10-08-retain-existing-guide-packs-in-imported`（主幹 missing）。
  - 任務：`2026-10-08-stalled-production-video-completion`（主幹 missing）。
  - 任務：`2026-10-08-use-normal-caption-warnings-and-local`（主幹 missing）。
  - 任務：`2026-10-08-video-audio-closing-particle-boundaries`（主幹 missing）。
  - 任務：`2026-10-08-video-branding-true-peak`（主幹 missing）。
  - 任務：`2026-10-08-video-qa-undecided-languages`（主幹 missing）。
  - 優先核對路徑：`docs/videos/long-form/review.json`, `docs/videos/long-form/review.md`, `docs/videos/recovery/2026-10-08-stalled-production.md`, `tools/video/assemble/branding-smoke.mjs`, `tools/video/assemble/branding.mjs`, `tools/video/assemble/branding.test.mjs`, `tools/video/qa/cli.mjs`, `tools/video/qa/qa.test.mjs` 等 10 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/stalled-videos-completion-20261008` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`b9940f18c1dfed8b493ceb9778df4c845728d4e2`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/videos/long-form/review.json, docs/videos/long-form/review.md, tools/video/assemble/branding-smoke.mjs, tools/video/assemble/branding.mjs, tools/video/assemble/branding.test.mjs, tools/video/qa/cli.mjs, tools/video/qa/qa.test.mjs, tools/video/tts/check.mjs (and 1 more paths listed in pathBlobEvidence). Reconcile current open/missing task IDs: 2026-10-08-make-durable-polling-deadline-regression-deterministic, 2026-10-08-retain-existing-guide-packs-in-imported, 2026-10-08-stalled-production-video-completion, 2026-10-08-use-normal-caption-warnings-and-local, 2026-10-08-video-audio-closing-particle-boundaries, 2026-10-08-video-branding-true-peak, 2026-10-08-video-qa-undecided-languages, 2026-10-09-video-stage-receipt-site-identity. Preserve dirty checkout C:/Users/x8120/.codex/worktrees/2a98/travel_scanㄐ and its untracked evidence. Keep the branch pending this reconciliation.
  - 任務：`2026-10-08-make-durable-polling-deadline-regression-deterministic`（主幹 missing）。
  - 任務：`2026-10-08-retain-existing-guide-packs-in-imported`（主幹 missing）。
  - 任務：`2026-10-08-stalled-production-video-completion`（主幹 missing）。
  - 任務：`2026-10-08-use-normal-caption-warnings-and-local`（主幹 missing）。
  - 任務：`2026-10-08-video-audio-closing-particle-boundaries`（主幹 missing）。
  - 任務：`2026-10-08-video-branding-true-peak`（主幹 missing）。
  - 任務：`2026-10-08-video-qa-undecided-languages`（主幹 missing）。
  - 任務：`2026-10-09-video-stage-receipt-site-identity`（主幹 missing）。
  - 優先核對路徑：`docs/videos/long-form/review.json`, `docs/videos/long-form/review.md`, `tools/video/assemble/branding-smoke.mjs`, `tools/video/assemble/branding.mjs`, `tools/video/assemble/branding.test.mjs`, `tools/video/qa/cli.mjs`, `tools/video/qa/qa.test.mjs`, `tools/video/tts/check.mjs` 等 9 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.
  - 保留證據：Checked-out worktree has local modifications/untracked evidence; do not remove it.

- [ ] **Codex `codex/ten-drama-backend-sync-20261002` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`ab6192ef4ba2f08e8da96f0064a593c3d49feab7`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/videos/long-form/review.json, docs/videos/long-form/review.md. Keep the branch pending this reconciliation.
  - 任務：[2026-10-02-ten-drama-backend-production-sync](../../tasks/done/2026-10-02-ten-drama-backend-production-sync.md)（主幹 done）；Sync ten drama production plans into backend review revisions；原認領 codex-ten-drama-sync。
  - 任務：[2026-10-02-ten-drama-voice-detail-review](../../tasks/done/2026-10-02-ten-drama-voice-detail-review.md)（主幹 done）；Review ten drama voices and production detail contracts；原認領 codex-ten-drama-voice-review。
  - 優先核對路徑：`docs/videos/long-form/review.json`, `docs/videos/long-form/review.md`, `docs/videos/series-plans/binge-five-20260928/city-owes-a-light/production-design.json`, `docs/videos/series-plans/binge-five-20260928/city-owes-a-light/production-review.md`, `docs/videos/series-plans/claude-binge-five-20260928/reload-first-day/production-design.json`, `docs/videos/series-plans/claude-binge-five-20260928/reload-first-day/production-review.md`, `tools/video/automation/flow.mjs`, `tools/video/automation/series.test.mjs` 等 19 個路徑。
  - 保留證據：Merged PR exists but local non-task scope differs, so completion is not proven by the PR alone.

- [ ] **Codex `codex/ten-drama-production-readiness-20261001` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`371f27d687ac8b8f7f140f444484eaa3abb57dc1`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/video_automation/series.py, apps/api/tests/test_video_media_jobs.py, apps/api/tests/test_video_series.py, docs/videos/LANGUAGES.md, docs/videos/series-plans/binge-five-20260928/seventh-passenger/production-design.json, docs/videos/series-plans/binge-five-20260928/wedding-reckoning/production-design.json, docs/videos/series-plans/claude-binge-five-20260928/before-the-hammer/production-design.json, docs/videos/series-plans/claude-binge-five-20260928/ghost-at-his-side/production-design.json (and 11 more paths listed in pathBlobEvidence). Keep the branch pending this reconciliation.
  - 優先核對路徑：`.agents/skills/youtube-video/SKILL.md`, `.agents/skills/youtube-video/references/animation-production.md`, `.agents/skills/youtube-video/references/drama.md`, `.agents/skills/youtube-video/references/prompts/writer-drama.md`, `.agents/skills/youtube-video/references/prompts/writer-series.md`, `.claude/skills/youtube-video/SKILL.md`, `.claude/skills/youtube-video/references/animation-production.md`, `.claude/skills/youtube-video/references/drama.md` 等 65 個路徑。
  - 保留證據：Merged PR exists but local non-task scope differs, so completion is not proven by the PR alone.


### 新聞、審核與 PR 整合（18）

- [ ] **Claude `claude/news-fetcher-http2` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`c6256fb6ceb3d44b78dbcbbdbbde3a6845a081ca`。
  - 原始下一步：Finish or reconcile the listed task IDs before cleanup.
  - 任務：[2026-10-11-news-fetcher-is-refused-by-cloudflare](../../tasks/open/2026-10-11-news-fetcher-is-refused-by-cloudflare.md)（主幹 open）；News fetcher is refused by Cloudflare where plain curl from the host is not。
  - 優先核對路徑：`apps/api/app/news_automation/fetch.py`, `apps/api/pyproject.toml`, `apps/api/uv.lock`。
  - 保留證據：Associated task remains open on main

- [ ] **Codex `codex/adsense-review-audit-20261004` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`5c44a43612884462aada86f80e6a004f7cdcc9de`。
  - 原始下一步：2026-10-04-address-adsense-low-value-content-before remains open
  - 任務：[2026-10-04-verify-current-adsense-blockers-and-prepare](../../tasks/done/2026-10-04-verify-current-adsense-blockers-and-prepare.md)（主幹 done）。
  - 任務：[2026-10-04-address-adsense-low-value-content-before](../../tasks/open/2026-10-04-address-adsense-low-value-content-before.md)（主幹 open）。
  - 任務：[2026-10-04-keep-article-faq-headings-and-answers](../../tasks/done/2026-10-04-keep-article-faq-headings-and-answers.md)（主幹 done）。
  - 優先核對路徑：`docs/adsense-feasibility.md`, `docs/adsense-review-readiness.md`, `docs/frontend-monetization-plan.md`。
  - 保留證據：Full branch aggregate patch matches origin/main commit 41f2f363b3036b0545497c2cb48d79dea5f0be7e
  - 保留證據：Linked main task remains unfinished: 2026-10-04-address-adsense-low-value-content-before=open

- [ ] **Codex `codex/catalog-review-all-20260908` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`a24472d02174d928358fc5eb8c9dba65f85d6ccd`。
  - 原始下一步：2026-09-08-continue-evidence-backed-remaining-hotspot-candidate remains open
  - 任務：[2026-09-08-resolve-pending-catalog-evidence-with-browser](../../tasks/done/2026-09-08-resolve-pending-catalog-evidence-with-browser.md)（主幹 done）。
  - 任務：[2026-09-08-review-all-pending-travel-catalog-with](../../tasks/done/2026-09-08-review-all-pending-travel-catalog-with.md)（主幹 done）。
  - 任務：[2026-09-08-review-hotspot-candidates-with-exact-browser](../../tasks/done/2026-09-08-review-hotspot-candidates-with-exact-browser.md)（主幹 done）。
  - 任務：[2026-09-08-continue-evidence-backed-remaining-hotspot-candidate](../../tasks/open/2026-09-08-continue-evidence-backed-remaining-hotspot-candidate.md)（主幹 open）。
  - 任務：[2026-09-08-prevent-google-coordinates-being-labelled-durable](../../tasks/done/2026-09-08-prevent-google-coordinates-being-labelled-durable.md)（主幹 done）。
  - 優先核對路徑：`docs/catalog-review-2026-09-08.md`, `docs/catalog-review-followup-2026-09-08.md`, `docs/hotspot-review-2026-09-08.md`, `ops/catalog_review_20260908.py`, `ops/catalog_review_20260908_decisions.json`, `ops/catalog_review_20260908_styles.json`, `ops/catalog_review_followup_20260908.json`, `ops/catalog_review_followup_20260908.py` 等 10 個路徑。
  - 保留證據：Linked main task remains unfinished: 2026-09-08-continue-evidence-backed-remaining-hotspot-candidate=open

- [ ] **Codex `codex/content-review-resolution` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`9cd24e2be787925be58eb55418c4d9b6333fa049`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/tests/test_catalog_content_review_resolution.py, apps/api/tests/test_catalog_remaining_proof_report.py, docs/catalog-content-reviews/2026-09-09-remaining-proof-result.md, docs/catalog-content-reviews/2026-09-09-remaining-proof.json, docs/catalog-content-reviews/2026-09-09-resolution-result.md, docs/catalog-content-reviews/2026-09-09-resolution.json
  - 任務：`2026-09-08-content-review-resolution`（主幹 absent）。
  - 任務：`2026-09-08-remaining-189-catalog-proof`（主幹 absent）。
  - 優先核對路徑：`apps/api/tests/test_catalog_content_review_resolution.py`, `apps/api/tests/test_catalog_remaining_proof_report.py`, `docs/catalog-content-reviews/2026-09-09-remaining-proof-result.md`, `docs/catalog-content-reviews/2026-09-09-remaining-proof.json`, `docs/catalog-content-reviews/2026-09-09-resolution-result.md`, `docs/catalog-content-reviews/2026-09-09-resolution.json`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/news-publication-deploy-receipt` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`380e463ae785ac98b66eb4fc52dd13d9a6166549`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/news-automation-recovery-2026-10-04.md. Reconcile current open/missing task IDs: 2026-10-04-deploy-verifier-freshness-exit, 2026-10-04-news-publication-recovery. Keep the branch pending this reconciliation.
  - 任務：`2026-10-04-deploy-verifier-freshness-exit`（主幹 missing）。
  - 任務：[2026-10-04-news-publication-recovery](../../tasks/open/2026-10-04-news-publication-recovery.md)（主幹 open）；Deploy the news diagram fix and reassess held publication drafts。
  - 優先核對路徑：`docs/news-automation-recovery-2026-10-04.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/news-recovery-20261010` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`1b7be83e6cc65a308e2c21b785c7e37c8ac966f7`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/news-held-cohort-recovery-2026-10-10.md. Reconcile current open/missing task IDs: 2026-10-05-video-held-retry-status, 2026-10-10-add-audited-source-extension-for-held, 2026-10-10-distinguish-reported-and-negated-trading-verbs, 2026-10-10-news-held-cohort-recovery. Preserve dirty checkout C:/Users/x8120/.codex/worktrees/6f71/travel_scanㄐ and its untracked evidence. Keep the branch pending this reconciliation.
  - 任務：`2026-10-05-video-held-retry-status`（主幹 missing）。
  - 任務：[2026-10-10-add-audited-source-extension-for-held](../../tasks/open/2026-10-10-add-audited-source-extension-for-held.md)（主幹 open）；Add audited source extension for held news。
  - 任務：[2026-10-10-distinguish-reported-and-negated-trading-verbs](../../tasks/open/2026-10-10-distinguish-reported-and-negated-trading-verbs.md)（主幹 open）；Distinguish reported and negated trading verbs from crypto recommendations。
  - 任務：[2026-10-10-exclude-system-topic-navigation-from-news](../../tasks/done/2026-10-10-exclude-system-topic-navigation-from-news.md)（主幹 done）；Exclude system topic navigation from news factual verification；原認領 codex-news-recovery-6f71。
  - 任務：[2026-10-10-news-disclaimer-correction-loop](../../tasks/done/2026-10-10-news-disclaimer-correction-loop.md)（主幹 done）；Investigate recurring news disclaimer corrections after locale review；原認領 codex-news-recovery-6f71。
  - 任務：[2026-10-10-news-held-cohort-recovery](../../tasks/open/2026-10-10-news-held-cohort-recovery.md)（主幹 open）；Resolve the 208 held news candidates inspected on October 10；原認領 codex-news-recovery-6f71。
  - 優先核對路徑：`docs/news-held-cohort-recovery-2026-10-10.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.
  - 保留證據：Checked-out worktree has local modifications/untracked evidence; do not remove it.

- [ ] **Codex `codex/pr377-review-fixes-20260909` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`4b05afc47a5424ddfd0db057b1746b7af9a08f08`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/admin/users.py, apps/api/app/community/accounts.py, apps/api/app/community/jobs.py, apps/api/app/database_admin/service.py, apps/api/tests/test_admin_rbac.py, apps/api/tests/test_admin_users_integration.py, apps/api/tests/test_community_foundation.py, apps/api/tests/test_database_admin.py. Keep the branch pending this reconciliation.
  - 任務：[2026-09-09-admin-operations-center](../../tasks/done/2026-09-09-admin-operations-center.md)（主幹 done）；Travel Scanner 後台營運中心升級；原認領 codex-root。
  - 任務：[2026-09-09-ci](../../tasks/done/2026-09-09-ci.md)（主幹 done）；後台營運中心驗收矩陣與 CI；原認領 codex-admin-acceptance。
  - 優先核對路徑：`.env.example`, `.github/workflows/ci.yml`, `README.md`, `apps/api/app/admin/operations_service.py`, `apps/api/app/admin/service.py`, `apps/api/app/admin/user_router.py`, `apps/api/app/admin/users.py`, `apps/api/app/auth/router.py` 等 72 個路徑。
  - 保留證據：Merged PR exists but local non-task scope differs, so completion is not proven by the PR alone.

- [ ] **Codex `codex/pr890-browser-validation` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`8e4110e4e85488fa41e23bd0b100ab25ff2568c4`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-28-vps-youtube-studio-deployment-and-live. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-vps-independent-youtube-upload-service-mode](../../tasks/done/2026-09-28-vps-independent-youtube-upload-service-mode.md)（主幹 done）；VPS independent YouTube upload service mode；原認領 codex-vps-upload。
  - 任務：[2026-09-28-vps-youtube-studio-deployment-and-live](../../tasks/open/2026-09-28-vps-youtube-studio-deployment-and-live.md)（主幹 open）；VPS YouTube Studio deployment and live private upload acceptance。
  - 任務：[2026-09-28-youtube-manual-browser-validation](../../tasks/done/2026-09-28-youtube-manual-browser-validation.md)（主幹 done）；Verify manual YouTube upload guide on desktop and mobile；原認領 codex-pr-merge-watch。
  - 任務：[2026-09-28-youtube-manual-upload](../../tasks/done/2026-09-28-youtube-manual-upload.md)（主幹 done）；YouTube manual upload guide with downloads and copyable fields；原認領 codex-manual-upload。
  - 優先核對路徑：`.github/workflows/ci.yml`, `apps/api/app/video_youtube/admin_api.py`, `apps/api/app/video_youtube/sync.py`, `apps/api/app/video_youtube/vps.py`, `apps/api/tests/test_video_youtube_vps.py`, `apps/web/components/admin-video-vps-upload.test.tsx`, `apps/web/components/admin-video-vps-upload.tsx`, `apps/web/components/admin-video-youtube.tsx` 等 26 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr900-ci-investigation` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`87711b4cf7bb3e03eb17f7419e8054a82ab79f2b`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-28-diagnose-merchant-style-browser-timeout-with. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-diagnose-merchant-style-browser-timeout-with`（主幹 missing）。
  - 任務：[2026-09-28-localize-newsletter-content-guides-batch035-pair](../../tasks/done/2026-09-28-localize-newsletter-content-guides-batch035-pair.md)（主幹 done）；Localize Kit and content marketing guides (batch 035 pair B)；原認領 codex-p1-audit。
  - 優先核對路徑：`apps/api/app/guides/content/content-marketing-calendar.json`, `apps/api/app/guides/content/kit-newsletter-setup.json`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr904-explainer-review` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`b2e42d88a67907737b4eeac0c82fdcd78b615940`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/video_automation/models.py, apps/api/app/video_automation/schemas.py, apps/api/app/video_automation/series.py, apps/api/migrations/versions/0109_video_flat_explainer.py, apps/api/tests/test_migration_0109_video_flat_explainer.py, apps/web/components/admin-video-reviews.test.tsx, apps/web/components/admin-video-series.tsx, apps/web/messages/en/admin.json (and 28 more paths listed in pathBlobEvidence). Reconcile current open/missing task IDs: 2026-09-28-sothatswhy-mascot-setting, 2026-09-28-sothatswhy-pilot-3. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-malformed-episode-shorts-isolation](../../tasks/done/2026-09-28-malformed-episode-shorts-isolation.md)（主幹 done）；Keep malformed episode Shorts from blocking long videos；原認領 codex-pr-merge-watch。
  - 任務：[2026-09-28-so-that-s-why-thumbnail-template](../../tasks/done/2026-09-28-so-that-s-why-thumbnail-template.md)（主幹 done）；So That's Why: thumbnail template gaps (series palette, stamp, pillar accent, brand, headline check)；原認領 claude-opus。
  - 任務：[2026-09-28-sothatswhy-explainer-preset](../../tasks/done/2026-09-28-sothatswhy-explainer-preset.md)（主幹 done）；So That's Why: flat-illustration explainer preset for the drama route (narrator only, all still shots)；原認領 claude-opus。
  - 任務：[2026-09-28-sothatswhy-mascot-setting](../../tasks/open/2026-09-28-sothatswhy-mascot-setting.md)（主幹 open）；So That's Why: series look and the 3-second opener (no mascot)。
  - 任務：[2026-09-28-sothatswhy-pilot-3](../../tasks/open/2026-09-28-sothatswhy-pilot-3.md)（主幹 open）；So That's Why: pilot the first three episodes with Shorts, captions and dubs, and measure。
  - 任務：[2026-09-28-sothatswhy-shorts-from-episode](../../tasks/done/2026-09-28-sothatswhy-shorts-from-episode.md)（主幹 done）；So That's Why: cut two Shorts from each long episode's keyframes and script。
  - 優先核對路徑：`.agents/skills/youtube-video/references/drama.md`, `apps/api/app/video_automation/models.py`, `apps/api/app/video_automation/schemas.py`, `apps/api/app/video_automation/series.py`, `apps/api/migrations/versions/0109_video_flat_explainer.py`, `apps/api/tests/test_migration_0109_video_flat_explainer.py`, `apps/api/tests/test_video_drama_requests.py`, `apps/api/tests/test_video_series.py` 等 50 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr904-main-integration` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`850b35f1ee4b658fa47a9c8ab244ce2a9ae38783`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/video_automation/models.py, apps/api/app/video_automation/series.py, apps/api/migrations/versions/0112_video_flat_explainer.py, apps/api/tests/test_migration_0112_video_flat_explainer.py, docs/videos/ai-shorts/README.md, docs/videos/so-thats-why/README.md, docs/videos/so-thats-why/playlists.md, docs/videos/so-thats-why/thumbnails.md (and 17 more paths listed in pathBlobEvidence). Reconcile current open/missing task IDs: 2026-09-28-pr904-main-integration, 2026-09-28-sothatswhy-mascot-setting, 2026-09-28-sothatswhy-pilot-3. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-guard-story-starts-and-repair-merged](../../tasks/done/2026-09-28-guard-story-starts-and-repair-merged.md)（主幹 done）；Guard story starts and repair merged migration chain；原認領 codex-pr910-followup。
  - 任務：[2026-09-28-malformed-episode-shorts-isolation](../../tasks/done/2026-09-28-malformed-episode-shorts-isolation.md)（主幹 done）；Keep malformed episode Shorts from blocking long videos；原認領 codex-pr-merge-watch。
  - 任務：`2026-09-28-pr904-main-integration`（主幹 missing）。
  - 任務：[2026-09-28-so-that-s-why-thumbnail-template](../../tasks/done/2026-09-28-so-that-s-why-thumbnail-template.md)（主幹 done）；So That's Why: thumbnail template gaps (series palette, stamp, pillar accent, brand, headline check)；原認領 claude-opus。
  - 任務：[2026-09-28-sothatswhy-explainer-preset](../../tasks/done/2026-09-28-sothatswhy-explainer-preset.md)（主幹 done）；So That's Why: flat-illustration explainer preset for the drama route (narrator only, all still shots)；原認領 claude-opus。
  - 任務：[2026-09-28-sothatswhy-mascot-setting](../../tasks/open/2026-09-28-sothatswhy-mascot-setting.md)（主幹 open）；So That's Why: series look and the 3-second opener (no mascot)。
  - 任務：[2026-09-28-sothatswhy-pilot-3](../../tasks/open/2026-09-28-sothatswhy-pilot-3.md)（主幹 open）；So That's Why: pilot the first three episodes with Shorts, captions and dubs, and measure。
  - 任務：[2026-09-28-sothatswhy-shorts-from-episode](../../tasks/done/2026-09-28-sothatswhy-shorts-from-episode.md)（主幹 done）；So That's Why: cut two Shorts from each long episode's keyframes and script。
  - 優先核對路徑：`.agents/skills/youtube-video/references/drama.md`, `apps/api/app/video_automation/models.py`, `apps/api/app/video_automation/schemas.py`, `apps/api/app/video_automation/series.py`, `apps/api/migrations/versions/0112_video_flat_explainer.py`, `apps/api/tests/test_migration_0112_video_flat_explainer.py`, `apps/api/tests/test_video_drama_requests.py`, `apps/api/tests/test_video_series.py` 等 54 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr905-schedule-guard` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`bb60b9615f930c9e6734fcd0197cccfb93aa93e8`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/video_youtube/sync.py, docs/videos/SHORTS.md. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-guard-automatic-shorts-sync-against-changed](../../tasks/done/2026-09-28-guard-automatic-shorts-sync-against-changed.md)（主幹 done）；Guard automatic Shorts sync against changed consent and Studio schedules；原認領 codex-pr905-schedule-guard。
  - 任務：[2026-09-28-video-shorts-api](../../tasks/done/2026-09-28-video-shorts-api.md)（主幹 done）；Video shorts A1: Shorts on the server: projects, slots, metrics, costs, settings and the auto-approval rule；原認領 claude-fable-5-1-shorts。
  - 任務：[2026-09-28-video-shorts-automation-api](../../tasks/done/2026-09-28-video-shorts-automation-api.md)（主幹 done）；Video shorts A3: the topic library, the weekly plan, the next job and the weekly report on the server；原認領 claude-opus-5-5-shorts-a3。
  - 任務：[2026-09-28-video-shorts-tools-push](../../tasks/done/2026-09-28-video-shorts-tools-push.md)（主幹 done）；Video shorts T1: the Shorts tool speaks to the site: server narration, check-audio, qa, package and push；原認領 claude-fable-5-1-shorts。
  - 任務：[2026-09-28-video-shorts-worker-lab](../../tasks/done/2026-09-28-video-shorts-worker-lab.md)（主幹 done）；Video shorts T2: the worker makes experiment Shorts by itself, plans the week and writes the weekly report；原認領 claude-opus-5-5-shorts-t2。
  - 任務：[2026-09-28-video-shorts-youtube-auto](../../tasks/done/2026-09-28-video-shorts-youtube-auto.md)（主幹 done）；Video shorts Y1: the site schedules Shorts on YouTube by itself under the owner's standing consent；原認領 claude-fable-5-1-shorts。
  - 優先核對路徑：`apps/api/app/admin/operations_service.py`, `apps/api/app/main.py`, `apps/api/app/models.py`, `apps/api/app/video_automation/admin_api.py`, `apps/api/app/video_automation/judge.py`, `apps/api/app/video_reviews/admin_api.py`, `apps/api/app/video_reviews/admin_service.py`, `apps/api/app/video_reviews/schemas.py` 等 26 個路徑。
  - 保留證據：Unique local commits have no merged PR provenance; content and receipts require integration or explicit supersession.

- [ ] **Codex `codex/pr906-validator-guard` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`aef6dcfb06949776edd57510f6486c3c7fc17079`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: .github/workflows/video-tooling.yml, tools/video/shorts/cli.mjs, tools/video/shorts/package.mjs, tools/video/shorts/pipeline.test.mjs, tools/video/shorts/push.mjs, tools/video/shorts/qa.mjs. Reconcile current open/missing task IDs: 2026-09-28-pr906-main-integration, 2026-09-28-pr906-shorts-validation-atomic-reports. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-pr906-main-integration`（主幹 missing）。
  - 任務：`2026-09-28-pr906-shorts-validation-atomic-reports`（主幹 missing）。
  - 任務：[2026-09-28-video-shorts-api](../../tasks/done/2026-09-28-video-shorts-api.md)（主幹 done）；Video shorts A1: Shorts on the server: projects, slots, metrics, costs, settings and the auto-approval rule；原認領 claude-fable-5-1-shorts。
  - 任務：[2026-09-28-video-shorts-automation-api](../../tasks/done/2026-09-28-video-shorts-automation-api.md)（主幹 done）；Video shorts A3: the topic library, the weekly plan, the next job and the weekly report on the server；原認領 claude-opus-5-5-shorts-a3。
  - 任務：[2026-09-28-video-shorts-tools-push](../../tasks/done/2026-09-28-video-shorts-tools-push.md)（主幹 done）；Video shorts T1: the Shorts tool speaks to the site: server narration, check-audio, qa, package and push；原認領 claude-fable-5-1-shorts。
  - 任務：[2026-09-28-video-shorts-worker-lab](../../tasks/done/2026-09-28-video-shorts-worker-lab.md)（主幹 done）；Video shorts T2: the worker makes experiment Shorts by itself, plans the week and writes the weekly report；原認領 claude-opus-5-5-shorts-t2。
  - 任務：[2026-09-28-video-shorts-youtube-auto](../../tasks/done/2026-09-28-video-shorts-youtube-auto.md)（主幹 done）；Video shorts Y1: the site schedules Shorts on YouTube by itself under the owner's standing consent；原認領 claude-fable-5-1-shorts。
  - 優先核對路徑：`.github/workflows/video-tooling.yml`, `apps/api/app/admin/operations_service.py`, `apps/api/app/main.py`, `apps/api/app/models.py`, `apps/api/app/video_automation/admin_api.py`, `apps/api/app/video_automation/judge.py`, `apps/api/app/video_reviews/admin_api.py`, `apps/api/app/video_reviews/admin_service.py` 等 38 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr909-source-independence` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`8419f131694493ed9a2517be629dc32df092e034`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/videos/story-plans/brand-stories-100/AUTHORING.md, tools/video/story-plans/plan.mjs, tools/video/story-plans/plan.test.mjs. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-story-source-mirror-independence](../../tasks/done/2026-09-28-story-source-mirror-independence.md)（主幹 done）；Treat encyclopedia mirrors as one story source；原認領 codex-pr909-review。
  - 任務：[2026-09-28-video-story-admin](../../tasks/done/2026-09-28-video-story-admin.md)（主幹 done）；後台的故事清單、匯入表單、每日支數與上架時段；原認領 claude-opus-5-5-video-story-admin。
  - 任務：[2026-09-28-video-story-backlog](../../tasks/done/2026-09-28-video-story-backlog.md)（主幹 done）；100 個品牌故事的完整企劃清單；原認領 claude-fable-5-1-video-story。
  - 任務：[2026-09-28-video-story-worker](../../tasks/done/2026-09-28-video-story-worker.md)（主幹 done）；工人的故事流程：逐章撰稿、查核、審稿與提示詞；原認領 claude-opus-5-5-video-story-worker。
  - 優先核對路徑：`docs/videos/STORY.md`, `docs/videos/story-plans/brand-stories-100/AUTHORING.md`, `tools/video/story-plans/plan.mjs`, `tools/video/story-plans/plan.test.mjs`, `tools/video/story-plans/validate.mjs`。
  - 保留證據：Merged PR exists but local non-task scope differs, so completion is not proven by the PR alone.

- [ ] **Codex `codex/pr917-dedup-order` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`af3a18161792bc3667ace03e513d5ade9b634d8a`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/news_automation/duplicates.py, apps/api/tests/test_news_pipeline.py. Reconcile current open/missing task IDs: 2026-09-28-pr917-dedup-admission-order. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-pr917-dedup-admission-order`（主幹 missing）。
  - 任務：[2026-09-28-run-news-candidates-on-a-pool](../../tasks/done/2026-09-28-run-news-candidates-on-a-pool.md)（主幹 done）；Run news candidates on a pool of news workers instead of one at a time；原認領 claude-opus-5-5。
  - 優先核對路徑：`.agents/skills/prod-host-ops/references/news-ops.md`, `apps/api/app/config.py`, `apps/api/app/news_automation/duplicates.py`, `apps/api/app/news_automation/worker.py`, `apps/api/tests/test_news_pipeline.py`, `docs/news-automation.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr921-tidy-metadata-current` — 未完成**。先保全現有工作目錄並確認原認領者；依現有任務續作，完成驗證與整合後再清理。
  - 核對 HEAD：`a89cfa65ef518198b4b6f641148519431df4f6ae`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: tools/video/automation/tidy.mjs, tools/video/automation/tidy.test.mjs. Reconcile current open/missing task IDs: 2026-09-28-pr906-main-integration, 2026-09-28-pr921-tidy-metadata-guard. Preserve dirty checkout C:/Users/x8120/.codex/worktrees/pr-merge-watch/travel_scanㄐ and its untracked evidence. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-pr906-main-integration`（主幹 missing）。
  - 任務：`2026-09-28-pr921-tidy-metadata-guard`（主幹 missing）。
  - 任務：[2026-09-28-video-story-tidy-finished](../../tasks/done/2026-09-28-video-story-tidy-finished.md)（主幹 done）；影片上架後清掉工人的工作檔；原認領 claude-opus-5-5-video-story-tidy。
  - 任務：[2026-09-28-video-tidied-late-languages](../../tasks/done/2026-09-28-video-tidied-late-languages.md)（主幹 done）；清理過的影片被勾新語言時告訴站主；原認領 claude-opus-5-5-tidied-languages。
  - 優先核對路徑：`docs/videos/AUTOMATION.md`, `tools/video/automation/cli.mjs`, `tools/video/automation/cli.test.mjs`, `tools/video/automation/tidy.mjs`, `tools/video/automation/tidy.test.mjs`, `tools/video/cli.mjs`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.
  - 保留證據：Checked-out worktree has local modifications/untracked evidence; do not remove it.

- [ ] **Codex `codex/pr921-tidy-metadata-guard` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`1c3c08a80ca3e7ba7015d2d0da9510c4adbf913e`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: tools/video/automation/tidy.mjs, tools/video/automation/tidy.test.mjs. Reconcile current open/missing task IDs: 2026-09-28-pr921-tidy-metadata-guard. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-pr921-tidy-metadata-guard`（主幹 missing）。
  - 任務：[2026-09-28-video-story-tidy-finished](../../tasks/done/2026-09-28-video-story-tidy-finished.md)（主幹 done）；影片上架後清掉工人的工作檔；原認領 claude-opus-5-5-video-story-tidy。
  - 任務：[2026-09-28-video-tidied-late-languages](../../tasks/done/2026-09-28-video-tidied-late-languages.md)（主幹 done）；清理過的影片被勾新語言時告訴站主；原認領 claude-opus-5-5-tidied-languages。
  - 優先核對路徑：`docs/videos/AUTOMATION.md`, `tools/video/automation/cli.mjs`, `tools/video/automation/cli.test.mjs`, `tools/video/automation/tidy.mjs`, `tools/video/automation/tidy.test.mjs`, `tools/video/cli.mjs`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr922-main-integration` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`9c3412103ce22c5c2ec9a7182bb8c0078a3f482f`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-28-main-has-two-alembic-heads-0111, 2026-09-28-pr922-main-doc-integration. Keep the branch pending this reconciliation.
  - 任務：`2026-09-28-main-has-two-alembic-heads-0111`（主幹 missing）。
  - 任務：`2026-09-28-pr922-main-doc-integration`（主幹 missing）。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.


### 網站、後台、資料與其他修補（30）

- [ ] **Claude `fix/food-seed-test-drift` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`a103fb3ae11dce9138c76016b7b852c2618f6bef`。
  - 原始下一步：Keep the ref and file a narrow task to decide whether the dynamic reseeding test should be adopted; verify against current seeds/integration tests before integrating or retiring the patch.
  - 優先核對路徑：`apps/api/tests/test_food_integration.py`。
  - 保留證據：Closed #171 comment records replacement by #172, but it does not establish integration of the current branch's remaining fixture enhancement.
  - 保留證據：Only current aggregate changed path: apps/api/tests/test_food_integration.py.
  - 保留證據：Main source and branch diff were read directly; no merged PR head covers this ref.

- [ ] **Codex `codex/ai-shorts-pilot` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`4f01e2b82f7d0ceae51853069545bf9aff1b5d1b`。
  - 原始下一步：2026-09-27-ai-shorts-owner-review-studio-launch remains open
  - 任務：[2026-09-27-ai-shorts-pilot](../../tasks/done/2026-09-27-ai-shorts-pilot.md)（主幹 done）。
  - 任務：[2026-09-27-ai-shorts-owner-review-studio-launch](../../tasks/open/2026-09-27-ai-shorts-owner-review-studio-launch.md)（主幹 open）。
  - 優先核對路徑：`docs/videos/ai-shorts/README.md`, `docs/videos/ai-shorts/campaign/README.md`, `docs/videos/ai-shorts/campaign/briefs/01-shorts-receipt-total.md`, `docs/videos/ai-shorts/campaign/briefs/02-shorts-poster-blind.md`, `docs/videos/ai-shorts/campaign/briefs/03-shorts-prompt-check.md`, `docs/videos/ai-shorts/campaign/briefs/04-shorts-taiwan-location.md`, `docs/videos/ai-shorts/campaign/briefs/05-shorts-boba-game.md`, `docs/videos/ai-shorts/campaign/briefs/06-shorts-self-check.md` 等 41 個路徑。
  - 保留證據：Full branch aggregate patch matches origin/main commit 78a2703d4dbe59c2af20571888175a11a4979795
  - 保留證據：Linked main task remains unfinished: 2026-09-27-ai-shorts-owner-review-studio-launch=open

- [ ] **Codex `codex/codex-learning-complete` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`7c9c6652ccc9c43f21abc832f9da98b80092027b`。
  - 原始下一步：2026-09-14-codex-learning-series remains blocked
  - 任務：[2026-09-14-claude-code-tutorial-center](../../tasks/done/2026-09-14-claude-code-tutorial-center.md)（主幹 done）。
  - 任務：[2026-09-14-codex-upstream-integration](../../tasks/done/2026-09-14-codex-upstream-integration.md)（主幹 done）。
  - 任務：[2026-09-14-codex-depth-content](../../tasks/done/2026-09-14-codex-depth-content.md)（主幹 done）。
  - 任務：[2026-09-14-codex-depth-plan-alignment](../../tasks/done/2026-09-14-codex-depth-plan-alignment.md)（主幹 done）。
  - 任務：[2026-09-14-codex-learning-series](../../tasks/open/2026-09-14-codex-learning-series.md)（主幹 blocked）。
  - 優先核對路徑：`apps/web/app/[locale]/life/page.tsx`, `apps/web/components/guides/article-page.tsx`。
  - 保留證據：Linked main task remains unfinished: 2026-09-14-codex-learning-series=blocked

- [ ] **Codex `codex/complete-food-guide-review` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`20efde68f269999fc1fd60422c76fecdf5d62ae0`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/tests/test_catalog_content_review_all.py, docs/catalog-content-reviews/2026-09-08-all-pending-result.md, docs/catalog-content-reviews/2026-09-08-all-pending.json
  - 任務：`2026-09-08-complete-pending-food-guide-review`（主幹 absent）。
  - 優先核對路徑：`apps/api/tests/test_catalog_content_review_all.py`, `docs/catalog-content-reviews/2026-09-08-all-pending-result.md`, `docs/catalog-content-reviews/2026-09-08-all-pending.json`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/country-foods-map-links` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`a8736021c98f38a71e5f57555766d4cb86cc893e`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/app/models.py, apps/api/app/trips/itinerary.py, apps/api/app/trips/router.py, apps/api/migrations/versions/0020_food_catalog.py, apps/api/tests/test_schema.py
  - 優先核對路徑：`apps/api/app/models.py`, `apps/api/app/trips/itinerary.py`, `apps/api/app/trips/router.py`, `apps/api/migrations/versions/0020_food_catalog.py`, `apps/api/tests/test_schema.py`。
  - 保留證據：Uncommitted content exists in checkout; never delete this checked-out branch or worktree.

- [ ] **Codex `codex/food-and-hotspot-guide-review` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`7d092dd3c068037bb56b3666a52d32c57516a235`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/tests/test_catalog_content_review_batch2.py, apps/api/tests/test_catalog_content_review_evidence.py, docs/catalog-content-reviews/2026-09-08-batch2-result.md, docs/catalog-content-reviews/2026-09-08-batch2.json, docs/catalog-content-reviews/2026-09-08-result.md, docs/catalog-content-reviews/2026-09-08-review.json
  - 任務：`2026-09-08-food-hotspot-content-review`（主幹 absent）。
  - 任務：`2026-09-08-food-hotspot-review-batch-two`（主幹 absent）。
  - 優先核對路徑：`apps/api/tests/test_catalog_content_review_batch2.py`, `apps/api/tests/test_catalog_content_review_evidence.py`, `docs/catalog-content-reviews/2026-09-08-batch2-result.md`, `docs/catalog-content-reviews/2026-09-08-batch2.json`, `docs/catalog-content-reviews/2026-09-08-result.md`, `docs/catalog-content-reviews/2026-09-08-review.json`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/food-reservation-data-followup` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`c7e0e612e4cc35c31181b6a7af8ccf039ff05ea4`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: docs/catalog-content-reviews/2026-09-11-reservation-followup.json, docs/catalog-content-reviews/2026-09-11-reservation-followup.md
  - 任務：`2026-09-11-food-reservation-data-followup`（主幹 absent）。
  - 優先核對路徑：`docs/catalog-content-reviews/2026-09-11-reservation-followup.json`, `docs/catalog-content-reviews/2026-09-11-reservation-followup.md`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/food-reservation-platforms` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`59f4b994533554509ec2dd90d0f7139acf8030a9`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: docs/catalog-content-reviews/2026-09-11-reservation-enrichment.md
  - 任務：[2026-09-11-food-reservation-platforms](../../tasks/done/2026-09-11-food-reservation-platforms.md)（主幹 done）。
  - 任務：`2026-09-11-merchant-reservation-enrichment`（主幹 absent）。
  - 優先核對路徑：`docs/catalog-content-reviews/2026-09-11-reservation-enrichment.md`。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/frontend-flow-release-record-a899437a` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`2cfb1acab8f4f9bad565b54fa194bd5a3cbd90d4`。
  - 原始下一步：Only task bookkeeping or completion receipts differ; reconcile linked task IDs with current main done records before deleting.
  - 任務：[2026-09-09-frontend-flow-integration](../../tasks/done/2026-09-09-frontend-flow-integration.md)（主幹 done）。
  - 任務：[2026-09-09-frontend-flow-discovery-api](../../tasks/done/2026-09-09-frontend-flow-discovery-api.md)（主幹 done）。
  - 任務：[2026-09-09-frontend-flow-discovery-web](../../tasks/done/2026-09-09-frontend-flow-discovery-web.md)（主幹 done）。
  - 任務：`2026-09-09-frontend-flow-post-deploy-polish`（主幹 absent）。
  - 任務：[2026-09-09-frontend-flow-saved-api](../../tasks/done/2026-09-09-frontend-flow-saved-api.md)（主幹 done）。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/gemini-advanced-curriculum` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`a9ec247999535775d3adf288490414522f5542d2`。
  - 原始下一步：2026-09-14-gemini-advanced-api remains open
  - 原始下一步：2026-09-14-gemini-advanced-automation remains open
  - 原始下一步：2026-09-14-gemini-advanced-creative remains open
  - 原始下一步：2026-09-14-gemini-advanced-md remains open
  - 原始下一步：2026-09-14-gemini-advanced-release remains open
  - 原始下一步：2026-09-14-gemini-advanced-research remains open
  - 原始下一步：2026-09-14-gemini-advanced-work remains open
  - 任務：[2026-09-14-gemini-advanced-curriculum](../../tasks/done/2026-09-14-gemini-advanced-curriculum.md)（主幹 done）。
  - 任務：[2026-09-14-gemini-advanced-api](../../tasks/open/2026-09-14-gemini-advanced-api.md)（主幹 open）。
  - 任務：[2026-09-14-gemini-advanced-automation](../../tasks/open/2026-09-14-gemini-advanced-automation.md)（主幹 open）。
  - 任務：[2026-09-14-gemini-advanced-creative](../../tasks/open/2026-09-14-gemini-advanced-creative.md)（主幹 open）。
  - 任務：[2026-09-14-gemini-advanced-md](../../tasks/open/2026-09-14-gemini-advanced-md.md)（主幹 open）。
  - 任務：[2026-09-14-gemini-advanced-platform](../../tasks/done/2026-09-14-gemini-advanced-platform.md)（主幹 done）。
  - 任務：[2026-09-14-gemini-advanced-release](../../tasks/open/2026-09-14-gemini-advanced-release.md)（主幹 open）。
  - 任務：[2026-09-14-gemini-advanced-research](../../tasks/open/2026-09-14-gemini-advanced-research.md)（主幹 open）。
  - 任務：[2026-09-14-gemini-advanced-work](../../tasks/open/2026-09-14-gemini-advanced-work.md)（主幹 open）。
  - 任務：[2026-09-14-tasks-done-retains-open-copy](../../tasks/done/2026-09-14-tasks-done-retains-open-copy.md)（主幹 done）。
  - 優先核對路徑：`docs/gemini-series/README.md`, `docs/gemini-series/advanced/README.md`, `docs/life-ai-series.md`。
  - 保留證據：Linked main task remains unfinished: 2026-09-14-gemini-advanced-api=open, 2026-09-14-gemini-advanced-automation=open, 2026-09-14-gemini-advanced-creative=open, 2026-09-14-gemini-advanced-md=open, 2026-09-14-gemini-advanced-release=open, 2026-09-14-gemini-advanced-research=open, 2026-09-14-gemini-advanced-work=open

- [ ] **Codex `codex/gemini-original-snapshot` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`90bc53f52d8944466ace02b2d18414fa1581c804`。
  - 原始下一步：Compare unmatched paths against current requirements and preserve source: apps/api/app/guides/admin_service.py, apps/api/app/guides/content/gemini-api-ai-studio-first-call.json, apps/api/app/guides/content/gemini-api-cost-errors-guide.json, apps/api/app/guides/content/gemini-api-document-assistant.json, apps/api/app/guides/content/gemini-api-files-structured-output.json, apps/api/app/guides/content/gemini-beginner-guide.json, apps/api/app/guides/content/gemini-canvas-guide.json, apps/api/app/guides/content/gemini-cli-agent-skills.json, apps/api/app/guides/content/gemini-cli-authentication.json, apps/api/app/guides/content/gemini-cli-coding-workflow.json, apps/api/app/guides/content/gemini-cli-command-reference.json, apps/api/app/guides/content/gemini-cli-custom-commands.json, apps/api/app/guides/content/gemini-cli-files-and-shell.json, apps/api/app/guides/content/gemini-cli-gemini-md.json, apps/api/app/guides/content/gemini-cli-getting-started.json, apps/api/app/guides/content/gemini-cli-headless-automation.json, apps/api/app/guides/content/gemini-cli-hooks.json, apps/api/app/guides/content/gemini-cli-mcp-extensions.json, apps/api/app/guides/content/gemini-cli-memory-hierarchy.json, apps/api/app/guides/content/gemini-cli-permissions-sandbox.json, apps/api/app/guides/content/gemini-cli-sessions-context.json, apps/api/app/guides/content/gemini-cli-settings.json, apps/api/app/guides/content/gemini-cli-subagents.json, apps/api/app/guides/content/gemini-cli-troubleshooting.json, apps/api/app/guides/content/gemini-connected-apps-guide.json, apps/api/app/guides/content/gemini-deep-research-guide.json, apps/api/app/guides/content/gemini-file-analysis-guide.json, apps/api/app/guides/content/gemini-for-google-sheets-formulas.json, apps/api/app/guides/content/gemini-for-travel-planning.json, apps/api/app/guides/content/gemini-gems-custom-assistants.json, apps/api/app/guides/content/gemini-guide.json, apps/api/app/guides/content/gemini-in-chrome-guide.json, apps/api/app/guides/content/gemini-in-gmail-docs-sheets.json, apps/api/app/guides/content/gemini-ios-app-guide.json, apps/api/app/guides/content/gemini-live-voice-camera.json, apps/api/app/guides/content/gemini-mac-app-guide.json, apps/api/app/guides/content/gemini-markdown-basics.json, apps/api/app/guides/content/gemini-model-lineup-flash-pro.json, apps/api/app/guides/content/gemini-on-android-assistant.json, apps/api/app/guides/content/gemini-plans-ai-pro-ultra-2026.json, apps/api/app/guides/content/gemini-privacy-activity-settings.json, apps/api/app/guides/content/gemini-prompt-writing-guide.json, apps/api/app/guides/content/gemini-spark-workflows-guide.json, apps/api/app/guides/content/gemini-vs-chatgpt-vs-claude-daily.json, apps/api/app/guides/content/gemini-web-desktop-guide.json, apps/api/app/guides/content/google-ai-mode-search.json, apps/api/app/guides/content/google-ai-overviews-for-site-owners.json, apps/api/app/guides/content/google-workspace-ai-for-small-business.json, apps/api/app/guides/content/nano-banana-image-editing.json, apps/api/app/guides/content/notebooklm-for-study-notes.json, apps/api/app/guides/content/notebooklm-guide.json, apps/api/app/guides/content/veo-video-generation-guide.json, apps/api/app/guides/pack_ingest.py, apps/api/app/guides/schemas.py, apps/api/tests/test_guide_rich_blocks.py, apps/web/app/[locale]/life/page.tsx, apps/web/components/admin-guides-panel.test.tsx, apps/web/components/admin-guides-panel.tsx, apps/web/components/content-blocks.tsx, apps/web/components/guides/article-page.tsx, apps/web/components/guides/article.tsx, apps/web/components/guides/code-block.tsx, apps/web/components/guides/series-index.tsx, apps/web/components/guides/series-navigation.tsx, apps/web/components/guides/series.test.tsx, apps/web/lib/content-blocks.ts, apps/web/lib/guide-series.ts, apps/web/lib/guides.ts, apps/web/messages/en/admin.json, apps/web/messages/en/common.json, apps/web/messages/ja/admin.json, apps/web/messages/ja/common.json, apps/web/messages/ko/admin.json, apps/web/messages/ko/common.json, apps/web/messages/zh-CN/admin.json, apps/web/messages/zh-CN/common.json, apps/web/messages/zh-TW/admin.json, apps/web/messages/zh-TW/common.json, docs/gemini-series/README.md, docs/gemini-series/acceptance.json, docs/gemini-series/build.py, docs/gemini-series/example-verification.json, docs/gemini-series/reviewed-files.json, docs/gemini-series/verify-examples.py, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-desktop-chromium-lesson-18-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-desktop-chromium-lesson-36-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-desktop-chromium-lesson-47-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-desktop-chromium-lesson-50-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-mobile-chromium-lesson-18-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-mobile-chromium-lesson-36-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-mobile-chromium-lesson-47-code.png, docs/gemini-series/visual-review/gemini-series-all-50-real--87cb4-opy-render-without-overflow-mobile-chromium-lesson-50-code.png, docs/gemini-series/visual-review/gemini-series-hub-has-ever-9e0b1-tegories-and-learning-paths-desktop-chromium-hub-search.png, docs/gemini-series/visual-review/gemini-series-hub-has-ever-9e0b1-tegories-and-learning-paths-mobile-chromium-hub-search.png, docs/life-ai-series.md, tools/gemini-series.mjs, tools/gemini-series.test.mjs
  - 任務：[2026-09-13-pin-actions-and-dependency-updates](../../tasks/done/2026-09-13-pin-actions-and-dependency-updates.md)（主幹 done）。
  - 任務：[2026-09-13-thirty-original-travel-and-lifestyle-articles](../../tasks/done/2026-09-13-thirty-original-travel-and-lifestyle-articles.md)（主幹 done）。
  - 任務：[2026-09-13-life-ai-batch-04](../../tasks/done/2026-09-13-life-ai-batch-04.md)（主幹 done）。
  - 任務：[2026-09-13-life-ai-batch-05](../../tasks/done/2026-09-13-life-ai-batch-05.md)（主幹 done）。
  - 任務：[2026-09-14-fix-windows-workflow-pin-test-file](../../tasks/done/2026-09-14-fix-windows-workflow-pin-test-file.md)（主幹 done）。
  - 任務：[2026-09-14-gemini-series-content](../../tasks/done/2026-09-14-gemini-series-content.md)（主幹 done）。
  - 任務：[2026-09-14-gemini-series-platform](../../tasks/done/2026-09-14-gemini-series-platform.md)（主幹 done）。
  - 優先核對路徑：`apps/api/app/guides/admin_service.py`, `apps/api/app/guides/content/gemini-api-ai-studio-first-call.json`, `apps/api/app/guides/content/gemini-api-cost-errors-guide.json`, `apps/api/app/guides/content/gemini-api-document-assistant.json`, `apps/api/app/guides/content/gemini-api-files-structured-output.json`, `apps/api/app/guides/content/gemini-beginner-guide.json`, `apps/api/app/guides/content/gemini-canvas-guide.json`, `apps/api/app/guides/content/gemini-cli-agent-skills.json` 等 97 個路徑。
  - 保留證據：No sufficient content landing proof; do not delete.

- [ ] **Codex `codex/imported-long-languages` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`89d33b74acd16798d580f9f2e27121244cb4901d`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-29-resume-imported-long-video-languages. Keep the branch pending this reconciliation.
  - 任務：[2026-09-29-prevent-lost-long-running-language-stages](../../tasks/done/2026-09-29-prevent-lost-long-running-language-stages.md)（主幹 done）；Prevent lost long-running language stages and duplicate model retries；原認領 claude-opus-5-5-lang-stages。
  - 任務：[2026-09-29-resume-imported-long-video-languages](../../tasks/open/2026-09-29-resume-imported-long-video-languages.md)（主幹 open）；Resume selected languages for six imported long videos。
  - 優先核對路徑：`docs/videos/imported-long-languages/README.md`, `docs/videos/imported-long-languages/package-runtime.mjs`, `docs/videos/imported-long-languages/prepare.test.mjs`, `docs/videos/imported-long-languages/runner.mjs`, `docs/videos/imported-long-languages/runner.test.mjs`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/jev-outcome-uncertain-endpoints-20261005` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`498d3aad47667dbec412169a481bf90cac23b933`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/tests/test_video_automation_judge.py. Keep the branch pending this reconciliation.
  - 任務：[2026-10-05-jev-judge-endpoints-report-an-uncertain](../../tasks/done/2026-10-05-jev-judge-endpoints-report-an-uncertain.md)（主幹 done）；Jev judge endpoints report an uncertain provider outcome apart from a settled failure；原認領 codex-jev-uncertain-endpoints。
  - 優先核對路徑：`apps/api/app/video_automation/admin_api.py`, `apps/api/app/video_speech/admin_api.py`, `apps/api/tests/test_video_automation_judge.py`, `apps/api/tests/test_video_speech_check.py`。
  - 保留證據：Unique local commits have no merged PR provenance; content and receipts require integration or explicit supersession.

- [ ] **Codex `codex/klook-product-integration` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`96a0065520e3a3d284e208b2467a1894fe7e3c74`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-07-merchant-style-discovery. Keep the branch pending this reconciliation.
  - 任務：[2026-09-07-merchant-style-discovery](../../tasks/open/2026-09-07-merchant-style-discovery.md)（主幹 open）；網美與文青店家風格篩選、審核及首批來源資料。
  - 任務：[2026-09-08-admin-catalog-review-filters-and-canonical](../../tasks/done/2026-09-08-admin-catalog-review-filters-and-canonical.md)（主幹 done）；Admin catalog review filters and canonical location editor；原認領 codex-admin-editors。
  - 任務：[2026-09-08-admin-domain-navigation-and-workspaces](../../tasks/done/2026-09-08-admin-domain-navigation-and-workspaces.md)（主幹 done）；Admin domain navigation and workspaces；原認領 codex-admin-root。
  - 任務：[2026-09-08-admin-domain-regression-compatibility-tests](../../tasks/done/2026-09-08-admin-domain-regression-compatibility-tests.md)（主幹 done）；Admin domain regression compatibility tests；原認領 codex-admin-regression。
  - 任務：[2026-09-08-admin-domain-scoped-catalog-ai-review](../../tasks/done/2026-09-08-admin-domain-scoped-catalog-ai-review.md)（主幹 done）；Admin domain scoped catalog AI review；原認領 codex-admin-review。
  - 任務：[2026-09-08-admin-domain-settings-ownership-and-safe](../../tasks/done/2026-09-08-admin-domain-settings-ownership-and-safe.md)（主幹 done）；Admin domain settings ownership and safe saves；原認領 codex-admin-settings。
  - 任務：[2026-09-08-admin-hotel-workspace-isolation](../../tasks/done/2026-09-08-admin-hotel-workspace-isolation.md)（主幹 done）；Admin hotel workspace isolation；原認領 codex-admin-hotel。
  - 任務：[2026-09-08-klook-affiliate-web](../../tasks/done/2026-09-08-klook-affiliate-web.md)（主幹 done）；Klook affiliate frontend channels and contextual discovery；原認領 codex-klook-web。
  - 任務：[2026-09-08-klook-channel-backend](../../tasks/done/2026-09-08-klook-channel-backend.md)（主幹 done）；Klook channel aware affiliate backend and secure clickout；原認領 codex-klook-backend。
  - 任務：[2026-09-08-klook-direct-affiliate-integration](../../tasks/done/2026-09-08-klook-direct-affiliate-integration.md)（主幹 done）；Klook direct affiliate product integration and reviewed rollout；原認領 codex-klook-root。
  - 優先核對路徑：`.env.example`, `apps/api/app/admin/service.py`, `apps/api/app/affiliates/router.py`, `apps/api/app/affiliates/schemas.py`, `apps/api/app/affiliates/service.py`, `apps/api/app/config.py`, `apps/api/app/models.py`, `apps/api/app/travel_services/admin.py` 等 31 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/local-space-cleanup-20261011` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`0663ee01e10a7a5a9f4f315a4ab85192c6d87527`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/cleanup-2026-10-11.md. Reconcile current open/missing task IDs: 2026-10-11-local-space-cleanup. Keep the branch pending this reconciliation.
  - 任務：`2026-10-11-local-space-cleanup`（主幹 missing）。
  - 優先核對路徑：`docs/cleanup-2026-10-11.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/merchant-style-batch-08` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`ebd94ce0610e1f43172800313be07d954bfa9099`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-07-merchant-style-discovery. Keep the branch pending this reconciliation.
  - 任務：[2026-09-07-merchant-style-discovery](../../tasks/open/2026-09-07-merchant-style-discovery.md)（主幹 open）；網美與文青店家風格篩選、審核及首批來源資料。
  - 優先核對路徑：`apps/api/tests/test_merchant_styles.py`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr343-merge-ready-20260909` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`73dd2c21331412de61134ce553ed7eeefaa3c957`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-07-mokaair-community-foundation. Keep the branch pending this reconciliation.
  - 任務：[2026-09-07-mokaair-community-foundation](../../tasks/open/2026-09-07-mokaair-community-foundation.md)（主幹 open）；Mokaair community foundation and account safety。
  - 任務：[2026-09-09-frontend-flow-saved-api](../../tasks/done/2026-09-09-frontend-flow-saved-api.md)（主幹 done）；Unified saved items and private inbox API；原認領 codex-saved-flow。
  - 任務：[2026-09-09-pr343-account-safety-integration](../../tasks/done/2026-09-09-pr343-account-safety-integration.md)（主幹 done）；Integrate PR 343 account safety with current main；原認領 codex-account-safety。
  - 優先核對路徑：`apps/api/app/community/accounts.py`, `apps/api/app/community/jobs.py`, `apps/api/tests/test_community_foundation.py`, `docs/community.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr361-merge-ready-20260909` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`c3af57de73d1d66a63fedc44d8d58932f19abb48`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-07-merchant-style-discovery. Keep the branch pending this reconciliation.
  - 任務：[2026-09-07-merchant-style-discovery](../../tasks/open/2026-09-07-merchant-style-discovery.md)（主幹 open）；網美與文青店家風格篩選、審核及首批來源資料。
  - 優先核對路徑：`apps/api/tests/test_merchant_styles.py`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr365-docs-ready-20260909` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`7054a1d9bcb779a836a18a2245fe0255640515ea`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-08-travelpayouts-live-destination-activation. Keep the branch pending this reconciliation.
  - 任務：[2026-09-08-community-ci-read-retry](../../tasks/done/2026-09-08-community-ci-read-retry.md)（主幹 done）；Revalidate community read resets against production-build CI；原認領 claude-opus-5。
  - 任務：[2026-09-08-travelpayouts-live-destination-activation](../../tasks/open/2026-09-08-travelpayouts-live-destination-activation.md)（主幹 open）；Complete live Travelpayouts brand and destination offer verification。
  - 任務：[2026-09-09-pr365-docs-integration](../../tasks/done/2026-09-09-pr365-docs-integration.md)（主幹 done）；Integrate PR 365 historical deployment and open verification notes；原認領 codex-review-archive。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/pr367-merge-ready-20260909` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`aac58949819347bc6bfe43ef7a011498931ddd1b`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-07-hotel-platform-options-and-quote-readiness. Keep the branch pending this reconciliation.
  - 任務：[2026-09-07-hotel-platform-options-and-quote-readiness](../../tasks/open/2026-09-07-hotel-platform-options-and-quote-readiness.md)（主幹 open）；Hotel platform options and quote readiness。
  - 優先核對路徑：`apps/api/tests/test_hotel_content_package.py`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/preserve-smoke-ci-evidence` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`9e7882da8d28f58ac79dd536c0808072a8184f11`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-28-investigate-chromium-screenshot-capture-failure-in. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-investigate-chromium-screenshot-capture-failure-in](../../tasks/open/2026-09-28-investigate-chromium-screenshot-capture-failure-in.md)（主幹 open）；Investigate Chromium screenshot capture failure in discovery UI。
  - 任務：[2026-09-28-preserve-full-stack-browser-failure-evidence](../../tasks/done/2026-09-28-preserve-full-stack-browser-failure-evidence.md)（主幹 done）；Preserve full-stack browser failure evidence across suites；原認領 codex-pr-merge-watch。
  - 任務：[2026-09-28-use-runner-owned-tracing-in-community](../../tasks/done/2026-09-28-use-runner-owned-tracing-in-community.md)（主幹 done）；Use runner-owned tracing in community smoke tests；原認領 codex-pr-merge-watch。
  - 優先核對路徑：`.github/workflows/ci.yml`, `apps/web/e2e/community.spec.ts`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/redeploy-20260914` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`434fc41292b7530f006d6ff29f93c4655aa5deea`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/deployments/2026-09-14-redeploy.md. Reconcile current open/missing task IDs: 2026-09-14-harden-legacy-host-redeploy-backups-and, 2026-09-14-redeploy-latest-green-main-and-verify. Keep the branch pending this reconciliation.
  - 任務：`2026-09-14-harden-legacy-host-redeploy-backups-and`（主幹 missing）。
  - 任務：`2026-09-14-redeploy-latest-green-main-and-verify`（主幹 missing）。
  - 優先核對路徑：`docs/deployments/2026-09-14-redeploy.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/seoul-day2-transport-ux` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`abdd425422a522f1e80d538025d571054b7c8864`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: docs/seoul-day2-transport-ux.md. Reconcile current open/missing task IDs: 2026-09-10-transit-timing-and-fare-precision. Keep the branch pending this reconciliation.
  - 任務：[2026-09-10-seoul-day2-transport-ux](../../tasks/done/2026-09-10-seoul-day2-transport-ux.md)（主幹 done）；Seoul Day 2 transport settings and readable route details；原認領 codex-seoul-day2-release。
  - 任務：`2026-09-10-transit-timing-and-fare-precision`（主幹 missing）。
  - 優先核對路徑：`docs/seoul-day2-transport-ux.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/stay22-hotel-clickout` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`d5e137b2cf56786758ea9a1753c8c69ee9621187`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-09-include-community-sweeper-in-deployment-agent. Keep the branch pending this reconciliation.
  - 任務：`2026-09-09-include-community-sweeper-in-deployment-agent`（主幹 missing）。
  - 任務：[2026-09-09-stay22-hotel-clickout](../../tasks/done/2026-09-09-stay22-hotel-clickout.md)（主幹 done）；Stay22 exact hotel affiliate clickouts；原認領 codex-stay22。
  - 優先核對路徑：`.github/workflows/ci.yml`, `apps/api/app/travel_services/admin.py`, `apps/api/app/travel_services/errors.py`, `apps/api/app/travel_services/hotel_admin.py`, `apps/api/app/travel_services/hotel_options.py`, `apps/api/app/travel_services/router.py`, `apps/api/app/travel_services/schemas.py`, `apps/api/app/travel_services/service.py` 等 38 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/travel-discovery-community` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`66c3372b7654288682e888e54945620fe09b1391`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-07-merchant-style-discovery. Keep the branch pending this reconciliation.
  - 任務：[2026-09-07-merchant-style-discovery](../../tasks/open/2026-09-07-merchant-style-discovery.md)（主幹 open）；網美與文青店家風格篩選、審核及首批來源資料。
  - 任務：[2026-09-08-planner-premium-app](../../tasks/done/2026-09-08-planner-premium-app.md)（主幹 done）；Premium app-style itinerary planning flow；原認領 codex-planner-premium。
  - 任務：[2026-09-08-travel-discovery-api](../../tasks/done/2026-09-08-travel-discovery-api.md)（主幹 done）；Travel discovery search feed and explicit preferences API；原認領 codex-discovery-api。
  - 任務：[2026-09-08-travel-discovery-community](../../tasks/done/2026-09-08-travel-discovery-community.md)（主幹 done）；Community curated video invitations and collection references；原認領 codex-discovery-community。
  - 任務：[2026-09-08-travel-discovery-integration](../../tasks/done/2026-09-08-travel-discovery-integration.md)（主幹 done）；Travel discovery integration navigation safety and acceptance；原認領 codex-discovery-root。
  - 任務：[2026-09-08-travel-discovery-web](../../tasks/done/2026-09-08-travel-discovery-web.md)（主幹 done）；Travel discovery homepage search collections and media experience；原認領 codex-discovery-web。
  - 優先核對路徑：`.env.example`, `.github/workflows/travel-discovery.yml`, `apps/api/app/analytics/service.py`, `apps/api/app/community/collections.py`, `apps/api/app/community/discovery.py`, `apps/api/app/community/jobs.py`, `apps/api/app/community/models.py`, `apps/api/app/config.py` 等 58 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/vps-uploader-setup-20261001` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`4bc6154d549eff183d5ad70b4f40b81ab691d018`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-10-01-google-sign-in-refusal-blocks-vps, 2026-10-01-provision-vps-studio-uploader-secrets-and, 2026-10-01-vps-uploader-initialization-rejects-numeric-install. Keep the branch pending this reconciliation.
  - 任務：`2026-10-01-google-sign-in-refusal-blocks-vps`（主幹 missing）。
  - 任務：`2026-10-01-provision-vps-studio-uploader-secrets-and`（主幹 missing）。
  - 任務：`2026-10-01-vps-uploader-initialization-rejects-numeric-install`（主幹 missing）。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/wordpress-map-form-token-link-task` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`f61b7436c2d0385b69d3ba5a890ebc0d78e8b4f4`。
  - 原始下一步：Reconcile current open/missing task IDs: 2026-09-27-correct-wordpress-map-embed-marker-ai. Keep the branch pending this reconciliation.
  - 任務：`2026-09-27-correct-wordpress-map-embed-marker-ai`（主幹 missing）。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/youtube-approved-languages-sync-20260930` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`bdfe068b872e4b12996e19b3a248580ca4f23ab5`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/video_youtube/sync.py, apps/api/app/video_youtube/vps.py, apps/api/tests/test_video_youtube_vps.py. Reconcile current open/missing task IDs: 2026-09-30-clarify-first-upload-of-pending-dubbed. Keep the branch pending this reconciliation.
  - 任務：[2026-09-30-clarify-first-upload-of-pending-dubbed](../../tasks/open/2026-09-30-clarify-first-upload-of-pending-dubbed.md)（主幹 open）；Clarify first upload of pending dubbed language reviews。
  - 任務：[2026-09-30-youtube-approved-languages-sync](../../tasks/done/2026-09-30-youtube-approved-languages-sync.md)（主幹 done）；YouTube sync reads stale publish package after approved languages；原認領 claude-happy-carson。
  - 優先核對路徑：`apps/api/app/video_youtube/language_package.py`, `apps/api/app/video_youtube/sync.py`, `apps/api/app/video_youtube/vps.py`, `apps/api/tests/test_video_youtube_language_package.py`, `apps/api/tests/test_video_youtube_sync.py`, `apps/api/tests/test_video_youtube_vps.py`, `docs/videos/APPROVED-LANGUAGE-PACKAGE.md`。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/youtube-vps-uploader` — 未完成**。對照既有任務的完成條件與分支獨有內容，確認認領者後續作；先補入共享看板尚未登記的工作。
  - 核對 HEAD：`4bcd1fef3a55258537799914c613910df7c698d5`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/web/e2e/admin-video-manual-upload.spec.ts, apps/web/messages/en/admin.json, apps/web/messages/ja/admin.json, apps/web/messages/ko/admin.json, apps/web/messages/zh-CN/admin.json, apps/web/messages/zh-TW/admin.json, docs/videos/MANUAL-UPLOAD.md, tools/e2e-runtime-api.mjs. Reconcile current open/missing task IDs: 2026-09-28-vps-youtube-studio-deployment-and-live. Keep the branch pending this reconciliation.
  - 任務：[2026-09-28-vps-independent-youtube-upload-service-mode](../../tasks/done/2026-09-28-vps-independent-youtube-upload-service-mode.md)（主幹 done）；VPS independent YouTube upload service mode；原認領 codex-vps-upload。
  - 任務：[2026-09-28-vps-youtube-studio-deployment-and-live](../../tasks/open/2026-09-28-vps-youtube-studio-deployment-and-live.md)（主幹 open）；VPS YouTube Studio deployment and live private upload acceptance。
  - 任務：[2026-09-28-youtube-manual-browser-validation](../../tasks/done/2026-09-28-youtube-manual-browser-validation.md)（主幹 done）；Verify manual YouTube upload guide on desktop and mobile；原認領 codex-pr-merge-watch。
  - 任務：[2026-09-28-youtube-manual-upload](../../tasks/done/2026-09-28-youtube-manual-upload.md)（主幹 done）；YouTube manual upload guide with downloads and copyable fields；原認領 codex-manual-upload。
  - 優先核對路徑：`.github/workflows/ci.yml`, `apps/api/app/video_youtube/admin_api.py`, `apps/api/app/video_youtube/sync.py`, `apps/api/app/video_youtube/vps.py`, `apps/api/tests/test_video_youtube_vps.py`, `apps/web/components/admin-video-vps-upload.test.tsx`, `apps/web/components/admin-video-vps-upload.tsx`, `apps/web/components/admin-video-youtube.tsx` 等 26 個路徑。
  - 保留證據：At least one branch-associated/touched task is open or absent on main.

- [ ] **Codex `codex/youtube-vps-web-settings-20260930` — 待核對**。逐項核對分支差異與已合併版本；確認仍需整合或已有取代紀錄後再決定清理。
  - 核對 HEAD：`005a6e9e4e09a602873b54f9e1c7d1c2f4749910`。
  - 原始下一步：Inspect/integrate or prove supersession of these exact branch-only versions: apps/api/app/video_reviews/admin_service.py, apps/api/tests/test_video_reviews_integration.py, apps/web/components/admin-video-youtube.test.tsx. Keep the branch pending this reconciliation.
  - 任務：[2026-09-30-youtube-vps-web-settings](../../tasks/done/2026-09-30-youtube-vps-web-settings.md)（主幹 done）；Configure the VPS YouTube uploader from video settings；原認領 codex-vps-web-settings。
  - 任務：[2026-09-30-youtube-vps-web-settings-browser-acceptance](../../tasks/done/2026-09-30-youtube-vps-web-settings-browser-acceptance.md)（主幹 done）；Verify the VPS settings card in desktop and mobile browsers；原認領 claude-opus-5-5-vps-settings-e2e。
  - 優先核對路徑：`apps/api/app/video_reviews/admin_service.py`, `apps/api/app/video_youtube/sync.py`, `apps/api/app/video_youtube/vps.py`, `apps/api/tests/test_video_review_renewal.py`, `apps/api/tests/test_video_reviews_integration.py`, `apps/api/tests/test_video_youtube.py`, `apps/api/tests/test_video_youtube_vps.py`, `apps/web/components/admin-video-vps-settings.test.tsx` 等 11 個路徑。
  - 保留證據：Merged PR exists but local non-task scope differs, so completion is not proven by the PR alone.
