---
id: 2026-10-10-official-pages-the-news-writer-declined
title: Official pages the news writer declined become video topic candidates
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T07:35:26Z
completed_at:
branch:
depends_on:
  - 2026-10-10-add-official-changelog-and-developer-update
scope:
  - apps/api/app/video_automation/topics.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_automation_topics.py
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - docs/videos/AUTOMATION.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
  - apps/api/app/news_automation/sources.json
---

# Official pages the news writer declined become video topic candidates

## Why

The owner wants official updates and official how-to posts to become tutorial videos
(2026-10-10). The scheduled draft picks its topic from two places only
(`apps/api/app/video_automation/topics.py`): the site's own articles of the last 14 days
and a Brave search. A news story the site published reaches the planner as a site
article. An official how-to post does not: the news writer declines it as not
newsworthy, no article is written, and the planner never sees it.

## Definition of done

- [ ] `GET /video/automation/topics` returns recent first-party pages the news writer
      declined, from the sources that opt in, as topics with `source: "official"`.
- [ ] With no source opted in, the endpoint answers exactly as it does today.
- [ ] The planner prompt says how to treat an official topic.
- [ ] A first set of sources is opted in in `sources.json`.
- [ ] `docs/videos/AUTOMATION.md` describes the third source and its two limits.
- [ ] The duration receipt is re-bound by an independent reviewer.

## Steps

- [ ] `schemas.py`: `TopicView.source` gains `"official"`.
- [ ] `topics.py`: `official_topics(session, now=None)` returning topics and notes.
      Sources are enabled, first-party `NewsSource` rows whose
      `config_json.get("video_topics") is True` (filter in Python; the column is JSON).
      Skip a source that uses its feed summary as evidence, with a note. Candidates use
      the predicate of `backfill_cli.refetch_pool`: `status == "rejected"`,
      `error_code == "news_not_eligible"`, `human_decision IS NULL`; from those sources,
      created in the last 14 days, newest first, at most 20; outer-join `NewsEvidence` on
      the candidate's own page for the excerpt. Title `"<source name>｜<source title>"`,
      summary the first 500 characters of the excerpt, url the canonical URL, no slug.
- [ ] `gather_topics`: site, then official, then search; drop a search result whose URL
      is an official one; add a note when no source is opted in.
- [ ] `tools/video/automation/prompts.mjs`, planner: name the three kinds of topic; an
      `"official"` topic is a company's own page the site has no article for, preferred
      to a web result, returned with `"source_guide": null` and its URL first in
      `"source_urls"`, and an update is told in the four moves of the content-value rules.
- [ ] `sources.json`: `video_topics: true` on "Claude blog", "Claude developer blog",
      "Anthropic engineering", "Cursor changelog" and "GitHub Changelog" (the names the
      previous task gives them).
- [ ] Tests: a new `apps/api/tests/test_video_automation_topics.py` (in-memory sqlite as
      `test_news_automation.py` does) for the pool, the field mapping, every exclusion,
      and the order, de-duplication and notes of `gather_topics`;
      `tools/video/automation/prompts.test.mjs` for the planner text.
- [ ] Receipt: `tools/video/long-form/review.mjs` binds `schemas.py` and `prompts.mjs`.
      An agent other than the author reviews the two diffs for DURATION_ONLY, appends an
      increment to `docs/videos/long-form/review.md` and updates `review.json`. Rebase
      late and recompute after every rebase; these two files change often.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
cd apps/api && uv run pytest tests/test_video_automation_topics.py tests/test_video_automation_ai.py -q
node --test tools/video/automation/prompts.test.mjs tools/video/long-form/review.test.mjs
node tools/video/long-form/cli.mjs check
npm run check:tasks
```

## Notes

- Decided with the plan the owner approved on 2026-10-10: the switch is the per-source
  config key, not a checkbox on `/admin/videos`. A setting would need a migration and
  changes to six receipt-bound files; the key needs neither, and turning it on is the
  same owner-approved host load every `sources.json` change needs.
- The worker needs no change beyond the prompt: `flow.mjs` and `client.mjs` pass topics
  through without reading `source`.
- Two limits to write into `AUTOMATION.md`:
  - Only pages the writer declined become official topics. A page that became a news
    story arrives as a site article; one held for review is not offered.
  - The automated route cannot operate a tool yet
    (`2026-10-09-give-the-automated-route-a-way`), so an official topic becomes a
    "what changed and what to do now" video resting on cited evidence. A hands-on
    tutorial still goes through the manual route.
- A summary-evidence source is skipped because the worker's page reader refuses pages
  over 3 MB, and such entries all point at one shared page.
- Follow-ups to file with this work: the worker reads one entry of a shared changelog
  page; the owner pastes an official URL on `/admin/videos` to ask for a video; a
  checkbox for this source, if the owner wants one-click control.
