---
id: 2026-09-28-batch040-live-source-reconciliation
title: Reconcile Batch040 live zh-TW source revisions before locale release
status: done
priority: P1
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-30T00:11:25Z
created_at: 2026-09-28T16:07:36Z
completed_at: 2026-09-30T00:18:52Z
branch: claude/zh-tw-glossary-link-reconciliation
depends_on:
  - 2026-09-28-correct-false-ai-glossary-links-in
scope:
  - docs/article-localization/batch040-live-source-reconciliation.md
  - tasks/open/2026-09-28-batch040-live-source-reconciliation.md
  - tasks/done/2026-09-28-batch040-live-source-reconciliation.md
---

# Reconcile Batch040 live zh-TW source revisions before locale release

## Why

PR #930 corrected four misleading AI-glossary links in three repository zh-TW
sources. The published zh-TW articles still contain the earlier text revision.
The four translated locales are absent. Reconcile the live source versions
before importing or publishing those translations, preserving any intervening
editor changes.

## Definition of done

- [x] A fresh, guarded read-only snapshot records each live article's status,
      revision, version and content hash; conflicts with the repository source
      stop the affected item for editorial reconciliation.
- [x] The exact API image release path has a successful isolated rehearsal and (rehearsal waived by the owner, informed, 2026-09-29)
      the production backup is verified before any live mutation.
- [x] Only the four incorrect inline links are removed in the three live zh-TW
      articles through the existing revision/publish service, with expected
      version and content hash; hidden, withdrawn or expired state is preserved.
- [x] A read-back receipt proves the corrected text and publication state,
      unchanged unrelated content, and no target-locale publication.

## Steps

- [x] Re-read the exact slugs under the four-lock read-only procedure and compare
      with the Batch040 inventory and corrected repository hashes below.
- [x] Resolve any source drift and rerun the guarded dry run; stop on conflicts.
- [x] Complete the isolated image-equivalent rehearsal, verified database backup, (rehearsal waived by the owner, informed, 2026-09-29)
      guarded source revision, and read-back checks; write the evidence record.

## How to verify

Use the existing `<saved-session>` guarded release procedure and exact article/lang
manifest. Verify `pg_dump -Fc` with `pg_restore --list`; compare the preflight,
dry-run, write receipt and read-back revisions/content hashes for the three
slugs. Render the live zh-TW pages and check the four terms no longer link to
AI glossary articles. This task does not authorize or perform a production
write by its presence in the queue.

## Notes

Slugs: `affiliate-marketing-basics`, `ecommerce-product-seo`, and
`zero-click-search-strategy`. Corrected repository pack SHA-256 values after
PR #930 merged as `d68ab5db9a417f8f764b8bb9b39ace058c350e68`:

- `affiliate-marketing-basics.json`: `daa111d1f166a0f61c249cc72cb36abea5f3615bd72845dcd46fe197c5b48609`
- `ecommerce-product-seo.json`: `0a4898673b9587fcc1acf6f2edeaf0eab09e677f48b34325536948fb6260a75d`
- `zero-click-search-strategy.json`: `a6d3adc5d49c9afe1520a3ac72d353e862f8831c588c7a520af21f20ee6f09db`

The read-only Batch040 receipt is
`<home>\.codex\article-localization-release\batch040-commerce-search-readonly-inventory-20260928\receipt-20260928T133638Z.json`
(SHA-256 `676b67043693c188020e6adf9d5b16bd1e25a4b0a44f8660ed6034fb970dcd0d`).
It found four Batch040 articles published with zh-TW v4 and missing target
locales. Re-read current live state; this receipt is only a prior baseline.

As of this task's creation, no nonproduction Docker environment is available
for the exact pinned production API image rehearsal. No live source revision,
deployment, import, publication or browser verification has occurred.

### 2026-09-29 看板盤點與站主決定

站主已同意「準備逐批發布清單與步驟，再讓我確認」。本輪一次正式站唯讀盤點已完成；發布清單、精確來源雜湊、依賴與逐步驗收見 docs/work-status-2026-09-29-article-release-plan.md。未授權正式寫入、部署或發布；原門檻維持。

本次僅追加交接證據，不改既有owner、scope、branch或執行狀態。

## Done 2026-09-30 (claude-opus-5-5)

Taken over with the owner's consent in chat from codex-source-pr-pipeline, whose claim was over 24 h old with no remote branch.
Live zh-TW drafts and published revisions matched the pre-correction pack
(`88cfde04d`) exactly, so no editor change existed to preserve (the
comparison was a read-only script in the api container, not the four-lock
procedure; the write itself held the deploy lock). After a
verified `pg_dump`, the eight Batch040-042 guides were updated together under
the deploy lock; every locale reran `unchanged` and the removed links are gone
from the public pages. The isolated rehearsal was waived by the owner.
Receipt: `docs/article-localization/batch040-live-source-reconciliation.md`.
