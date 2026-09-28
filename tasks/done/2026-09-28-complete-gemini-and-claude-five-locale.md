---
id: 2026-09-28-complete-gemini-and-claude-five-locale
title: Complete Gemini and Claude five-locale series catalogues
status: done
priority: P2
area: api
owner: codex-series-five-locale
claimed_at: 2026-09-28T15:10:41Z
created_at: 2026-09-28T15:10:36Z
completed_at: 2026-09-28T17:22:57Z
branch: codex/article-series-five-language-completion
depends_on: []
scope:
  - apps/api/app/guides/series.py
  - apps/api/app/guides/series_data/gemini.json
  - apps/api/app/guides/series_data/locales
  - apps/api/tests/test_guide_series.py
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/gemini-page.test.tsx
  - apps/web/components/guides/series-hub.tsx
  - apps/web/components/guides/series.test.tsx
  - apps/web/lib/guide-series-copy.ts
  - apps/web/lib/gemini-series-projection.ts
  - apps/web/lib/gemini-series-projection.test.ts
  - docs/article-localization/series-five-locale-evidence.md
---

# Complete Gemini and Claude five-locale series catalogues

## Why

Claude Code has a 96-lesson zh-TW catalogue, but the other four locales have no
catalogue. Gemini has a zh-TW-only web directory, while the API series loader
has no Gemini catalogue. As new language articles publish, the directory and
previous/next navigation must use that locale's published lessons and copy.

## Definition of done

- [x] Claude Code and Gemini groups, learning paths and search aliases are
      localized in zh-TW, zh-CN, en, ja and ko.
- [x] The API selects the matching locale and only exposes published lessons,
      keeping withdrawn lessons and unpublished hubs out of directories and
      previous/next navigation.
- [x] Gemini keeps its existing zh-TW advanced-series projection without a
      duplicate directory/navigation; newly published other locales use the
      publication-aware generic series UI.
- [x] The zh-TW Gemini projection also intersects live published lessons so a
      withdrawn lesson cannot remain in the directory or previous/next links.
- [x] Gemini has language-specific directory and search labels, including an
      accurate zh-CN beginner level.
- [x] Focused API/web tests and CI pass before merge. Production import and
      public browser verification remain separate.

## Steps

- [x] Rechecked main: sitemap pagination is already merged; the series locale
      gap remains. Confirmed Gemini's 50 base slugs match the current web source.
- [x] Added locale overlays for Gemini and all 96 Claude Code lessons, including
      the later six groups, seven paths and 63 new search aliases.
- [x] Added locale-aware API catalogue loading and publication-boundary tests.
- [x] Added web duplication and withdrawal guard tests, kept the existing
      zh-TW Gemini renderer and let the other locales use API navigation.
- [x] Focused API and Web tests passed, plus Web lint, typecheck, i18n and task checks.
- [x] Updated the existing Gemini page integration fixture to return a published API
      series, matching the new release boundary; its old null mock caused Web CI
      to hide the directory even when the fixture expected published lessons.
- [x] Opened focused draft PR #947.
- [x] Complete implementation review and full CI at the verified implementation head.

## How to verify

Run `uv run pytest tests/test_guide_series.py -q`, `uv run ruff check
app/guides/series.py tests/test_guide_series.py`, and `uv run mypy
app/guides/series.py` from `apps/api`. Run focused article tests, Web lint,
typecheck, i18n and task checks from the root. CI and later production/browser
receipts are independent acceptance gates.

## Notes

Independent review found that the former zh-TW Gemini static directory could
retain a withdrawn lesson, and the generic non-zh-TW directory spoke of Claude.
Both are corrected in this task. The older uncommitted c5d9 series overlay covered only Claude's original 60
lessons and used the old Gemini web architecture. Current main has 96 Claude
lessons and Gemini's server-only projection, so the old diff must not be copied
wholesale. The new overlays retain stable slugs and use published article
documents for public titles/descriptions; API series links remain locale- and
publication-aware. No production write occurred.

Draft PR: https://github.com/x812033727/travel_scanner/pull/947
The first Web CI run failed in `gemini-page.test.tsx` because its API series
mock still returned null. The updated fixture keeps the publication guard in
place and locally passes all seven integration cases.

All nine checks passed at `f8ca81dc9f10b158ff89538d8940bd395ebce2bc`, including
API, Web and article-localization release-safety. This closes implementation work;
the task-only closure commit must pass its own CI before the authorized ordinary
merge. Deployment, imports and public browser acceptance remain in the guarded
localization release work and are not claimed complete here.
