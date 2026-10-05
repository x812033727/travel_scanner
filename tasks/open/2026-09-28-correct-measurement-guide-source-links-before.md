---
id: 2026-09-28-correct-measurement-guide-source-links-before
title: Correct measurement guide source links before localization
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T09:39:32Z
completed_at:
branch: codex/article-localization-036-measurement-source
depends_on: []
scope:
  - apps/api/app/guides/content/ga4-site-measurement.json
  - apps/api/app/guides/content/ga4-sessions-engagement.json
  - apps/api/app/guides/content/google-search-console-workflow.json
  - apps/api/app/guides/content/utm-link-conventions.json
  - docs/article-localization/batch036-measurement-source-links.md
---

# Correct measurement guide source links before localization

## Why

Four published GA4, Search Console and UTM guides contain seven links from
ordinary analytics words ("參數" and "標記") to unrelated AI model-parameter and
token terminology articles. The 2026-09-28 read-only inventory confirmed their
repository zh-TW documents match published v4; correct this source before
translating the four missing locales.

## Definition of done

- [x] All seven misleading links become plain text while every visible word,
      metadata field, source and remaining article link stays unchanged.
- [x] Four source packs pass scoped lint and structural comparison against main.
- [ ] A reviewed PR is merged; the published zh-TW revisions are rebound before
      the missing-language import. Production publication is separate.

## Steps

- [x] Pin the seven findings and published-source baseline.
- [x] Replace only the seven incorrect inline link nodes.
- [x] Validate pack structure and exact JSON difference.
- [x] Open PR and record its URL.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug <slug>` for each of the
four slugs from `apps/api`. The source comparison uses `git show origin/main`
and asserts each resulting JSON equals the baseline after precisely seven
specified `ArticleInline` to `TextInline` substitutions. Run focused content
pack/link tests and `npm run check:tasks`.

## Notes

Original read-only findings:
`C:\Users\x8120\.codex\article-localization-release\batch036-measurement-readonly-inventory-20260928\source-link-findings.json`
(SHA-256 `8275fb90b6f812c519d90f30fd80d2920b33c10a432a2548fe9dd441f800ed75`).
Both AI articles are unrelated to the surrounding GA4/UTM/Search Console use
of these words, so removing the link is more accurate than substituting an
unverified destination. See the scoped evidence document for exact hashes.
Draft PR: https://github.com/x812033727/travel_scanner/pull/902 .
CI, merge, source-version rebind and publication remain separate checks.

### 2026-09-29 看板盤點與站主決定

站主已同意「準備逐批發布清單與步驟，再讓我確認」。本輪一次正式站唯讀盤點已完成；發布清單、精確來源雜湊、依賴與逐步驗收見 docs/work-status-2026-09-29-article-release-plan.md。未授權正式寫入、部署或發布；原門檻維持。

本次僅追加交接證據，不改既有owner、scope、branch或執行狀態。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-root (since 2026-09-28T09:40:32Z) was stale and is released so it stops locking its scope. Landed: #902. Still open: Reviewed PR merged; published zh-TW revisions rebound before missing-language import (production publication s.
