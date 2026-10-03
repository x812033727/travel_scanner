---
id: 2026-09-27-link-each-published-news-candidate-to
title: Link each published news candidate to its live article from /admin/news
status: done
priority: P3
area: web
owner: claude-opus-5-5-news-live-link
claimed_at: 2026-10-02T15:17:24Z
created_at: 2026-09-27T08:06:09Z
completed_at: 2026-10-02T15:59:17Z
branch: claude/news-candidate-live-link
depends_on: []
scope:
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/service.py
  - apps/api/tests/test_news_admin.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages
  - apps/web/lib/admin-news.ts
---

# Link each published news candidate to its live article from /admin/news

## Why

On 2026-09-27 the site owner reported the hourly AI news as "published but not visible on
the front end". All nine `published` candidates were in fact live in five locales and
listed on `/life`. The owner had no quick way to check that from `/admin/news`: a
candidate's detail panel links only to the guide editor (`copy.openEditor`, one link per
locale, `apps/web/components/admin-news-workspace.tsx`, the `detail.guide_article_id`
block). Nothing on the page names the public URL. The news lists sort by the day the news
happened, and stories are published 1 to 6 days after the event, so the newest publication
sat 18th of 20 on `/life`, easy to miss by scrolling.

`CandidateSummary` and `CandidateDetail` (`apps/api/app/news_automation/schemas.py`)
carry `guide_article_id` but not the article's slug, so the web cannot build the link
today. Every news article is `kind="life"` (`_save_guide_bundle` in `pipeline.py`), so
the public path is `/<locale>/life/<slug>`.

## Definition of done

- [x] A `published` candidate's detail panel in `/admin/news` shows one link per locale
      to its public article (`/<locale>/life/<slug>`), opening in a new tab. The link
      label is in all five admin locales.
- [x] A candidate that is not `published` shows no public link, even if it has a saved
      article: its locales have no public version, so the link would answer 404.
- [x] The API exposes the slug on the candidate detail (and on the summary if the list
      rows show the link too), with a test.

## Steps

- [x] Add `article_slug: str | None` to the candidate schema and fill it in
      `service.candidate_detail` from the joined `GuideArticle`.
- [x] Render the links in `admin-news-workspace.tsx` next to the editor links, only for
      `status == "published"`.
- [x] Add the label to `apps/web/lib/admin-news-messages/*.json` (five files; the copy
      lives there, not in `.ts`, because `check:i18n` rejects new Han characters in
      staged `.ts` files).
- [x] Tests: `apps/api/tests/test_news_admin.py` for the slug,
      `admin-news-workspace.test.tsx` for the link and its absence.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_admin.py -q
cd apps/web && npx vitest run components/admin-news-workspace.test.tsx
```

After a deploy, open `/admin/news?queue=published`, open one candidate and follow each
locale's link: each answers 200 with the article.

## Notes

- Filed while fixing `2026-09-27-news-images-under-guides-news-assets` (the other half of
  the same report: every generated hero and diagram answered 500).
- The owner chose on 2026-09-27 to keep the news lists in event-date order, so this link
  is the way to find a just-published story; do not change the list order here.
- 2026-10-02, claude-opus-5-5-news-live-link: claimed with `--force` over two stale claims
  by claude-opus-5-5-news-4-9 (`2026-09-24-attach-a-second-evidence-source-to` and
  `2026-09-30-alert-in-admin-news-when-a`, branch `claude/gifted-rubin-umw5s4`): their PR
  #1041 merged on 2026-09-30 and no open PR uses that branch.
- Decided: the API sends `article_slug` and `article_kind` on the detail only. The list rows
  carry no link, so the summary (and its query) stay as they were. The kind comes from the
  saved `GuideArticle` rather than a hard-coded `life`, so the web builds the address with
  the public site's own helpers: `localeUrl(locale, guideHref(kind, slug))`
  (`apps/web/lib/seo.ts`, `apps/web/lib/guides.ts`), the same absolute URL the feed, the
  sitemap and the canonical tag use. `NEXT_PUBLIC_SITE_URL` is a required build argument of
  the web image, so the client bundle carries the real domain.
- The web decides visibility from `status == "published"` alone, as the Definition of done
  says; the API sends the slug whenever an article is saved (the editor already has it).
- Added `apps/web/lib/admin-news.ts` to the scope: the `NewsCandidate` type lives there, and
  no active task or open PR touched it.
- The label `openLive` is in `apps/web/lib/admin-news-messages/*.json`, which
  `docs/videos/long-form/review.json` does not bind.
- Verified: the new component test fails when the status gate is removed (the
  `manual_review` and `rejected` cases show five links); the API test reads the slug and
  kind through a real SQLite session.
