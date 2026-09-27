---
id: 2026-09-27-link-each-published-news-candidate-to
title: Link each published news candidate to its live article from /admin/news
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-27T08:06:09Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/service.py
  - apps/api/tests/test_news_admin.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages
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

- [ ] A `published` candidate's detail panel in `/admin/news` shows one link per locale
      to its public article (`/<locale>/life/<slug>`), opening in a new tab. The link
      label is in all five admin locales.
- [ ] A candidate that is not `published` shows no public link, even if it has a saved
      article: its locales have no public version, so the link would answer 404.
- [ ] The API exposes the slug on the candidate detail (and on the summary if the list
      rows show the link too), with a test.

## Steps

- [ ] Add `article_slug: str | None` to the candidate schema and fill it in
      `service.candidate_detail` from the joined `GuideArticle`.
- [ ] Render the links in `admin-news-workspace.tsx` next to the editor links, only for
      `status == "published"`.
- [ ] Add the label to `apps/web/lib/admin-news-messages/*.json` (five files; the copy
      lives there, not in `.ts`, because `check:i18n` rejects new Han characters in
      staged `.ts` files).
- [ ] Tests: `apps/api/tests/test_news_admin.py` for the slug,
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
