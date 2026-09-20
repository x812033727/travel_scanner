---
id: 2026-09-14-article-sitemap-pagination
title: Paginate article sitemap for all five languages
status: in-progress
priority: P1
area: api
owner: codex-sitemap-pagination
claimed_at: 2026-09-20T10:35:54Z
created_at: 2026-09-14T13:56:19Z
completed_at:
branch: codex/article-sitemap-pagination
depends_on: []
scope:
  - apps/api/app/guides/sitemap.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guides_sitemap_pagination.py
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
---

# Paginate article sitemap for all five languages

## Why

The API and web loader silently kept only 1,000 published translations. Completing
five languages exceeds that bound, omitting article URLs and sibling hreflang links.

## Definition of done

- [x] Enumerate every published translation through bounded API pages and keep one sitemap.xml.
- [x] Include reciprocal language alternates even when an article spans a page boundary.
- [x] Treat a failed, malformed, repeated-cursor or legacy capped answer as incomplete.
- [x] Focused API/web tests and static checks pass.

## Steps

- [x] Add stable slug/locale keyset pagination, cursor validation, limit <= 1,000 and next_cursor.
- [x] Drain every page before deriving alternates; deduplicate and remove the total-list cap.
- [x] Add coverage for exactly/over 1,000 rows, cross-page locales and publication exclusions.
- [x] Record final verification results.

## How to verify

From apps/api:

```powershell
.venv/Scripts/python.exe -m pytest tests/test_guides_sitemap_pagination.py tests/test_guides.py -q
.venv/Scripts/python.exe -m ruff check app/guides/service.py app/guides/router.py app/guides/schemas.py tests/test_guides_sitemap_pagination.py
.venv/Scripts/python.exe -m mypy app/guides/service.py app/guides/router.py app/guides/schemas.py
```

From the repository root:

```powershell
npm run test --workspace @travel-scanner/web -- lib/guides.server.test.ts app/sitemap.test.ts --pool=threads --maxWorkers=1
npm run typecheck:web
npm run check:tasks
```

## Notes

- Cursor ordering is (slug, locale), independent of publication timestamps. Slugs are unique
  across kinds; changing a timestamp or withdrawing an earlier row does not shift the cursor.
- Explicit next_cursor=null proves a terminal page, including exactly 1,000 rows. A legacy
  response without next_cursor is supported only on page one below 1,000 raw rows.
- A partial enumeration returns no article rows and complete=false, preserving the static
  sitemap and hub fallback without presenting incomplete hreflang as a complete language set.
- An unreadable optional modified_at retains the existing published_at fallback.
- The PR uses a dedicated sitemap query module because active review tasks claim
  `service.py` and `test_guides.py`; this keeps their scopes separate.
- No migrations, article content changes or deployment are part of this subtask.
- Verification on 2026-09-14: API pagination plus existing guide tests **87 passed, 83 skipped**
  (PostgreSQL integration service was not enabled); web loader/sitemap tests **147 passed**.
  Scoped Ruff, scoped ESLint, mypy on the three API modules, full web typecheck,
  git diff --check and check:tasks passed. Task check reports only existing aged claims
  and unrelated overlap warnings. npm's root test wrapper consumed worker flags, but both
  requested files ran successfully; the direct workspace command above preserves those flags.
- Task remains in progress until the parent integration work accepts it. No commit or deployment.
- 2026-09-20 handoff: the former owner released this task and `codex-sitemap-pagination`
  claimed it on `codex/article-sitemap-pagination` from `ac860f38`. The mainline now has
  a sitemap index and section/locale children, so this PR preserves that structure. Its
  route uses a dedicated query module to avoid two other active task scopes on
  `service.py` and `test_guides.py`; a separate pet-friendly task owns the child file.
- Local validation after adapting to current main: API guide and pagination tests
  113 passed / 106 skipped (PostgreSQL not configured); focused web tests 176 passed;
  web typecheck, scoped Ruff, scoped ESLint, i18n and task checks passed. Scoped mypy
  has no errors in changed files but reports five existing errors in `app/infra.py`
  and `app/hotspots/guides.py`. CI must run the PostgreSQL integration cases.
