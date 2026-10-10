---
id: 2026-10-10-official-pages-the-news-writer-declined
title: Official pages the news writer declined become video topic candidates
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-official-accounts
claimed_at: 2026-10-10T08:58:33Z
created_at: 2026-10-10T07:35:26Z
completed_at:
branch: claude/official-video-topics
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

- [x] `GET /video/automation/topics` returns recent first-party pages the news writer
      declined, from the sources that opt in, as topics with `source: "official"`.
- [x] With no source opted in, the endpoint answers exactly as it does today (no topic,
      no note).
- [x] The planner prompt says how to treat an official topic.
- [x] A first set of sources is opted in in `sources.json`.
- [x] `docs/videos/AUTOMATION.md` describes the third source and its two limits.
- [ ] The duration receipt is re-bound by an independent reviewer.

## Steps

- [x] `schemas.py`: `TopicView.source` gains `"official"`.
- [x] `topics.py`: `official_topics(session, now=None)` returning topics and notes.
      Sources are enabled, first-party `NewsSource` rows whose
      `config_json.get("video_topics") is True`. A source that uses its feed summary as
      evidence is skipped with a note. Candidates use the predicate of
      `backfill_cli.refetch_pool`: `status == "rejected"`,
      `error_code == "news_not_eligible"`, `human_decision IS NULL`; from those sources,
      created in the last 14 days, newest first, at most 20; `NewsEvidence` of the
      candidate's own page gives the excerpt.
- [x] `gather_topics`: site, then official, then search; a search result whose URL is an
      official one is dropped.
- [x] `tools/video/automation/prompts.mjs`, planner.
- [x] `sources.json`: `video_topics: true` on "Claude blog", "Claude developer blog",
      "Anthropic engineering", "GitHub Changelog" and "Cursor changelog".
- [x] Tests: `apps/api/tests/test_video_automation_topics.py` and
      `tools/video/automation/prompts.test.mjs`.
- [ ] Receipt: `tools/video/long-form/review.mjs` binds `schemas.py` and `prompts.mjs`.
      An agent other than the author reviews the two diffs for DURATION_ONLY, appends an
      increment to `docs/videos/long-form/review.md` and updates `review.json`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
cd apps/api && uv run pytest tests/test_video_automation_topics.py tests/test_news_sources_cli.py tests/test_news_automation.py -q
node --test tools/video/automation/prompts.test.mjs tools/video/long-form/review.test.mjs
node tools/video/long-form/cli.mjs check
npm run check:tasks
```

## Notes

- Decided with the plan the owner approved on 2026-10-10: the switch is the per-source
  config key, not a checkbox on `/admin/videos`. A setting would need a migration and
  changes to six receipt-bound files; the key needs neither, and turning it on is the
  same owner-approved host load every `sources.json` change needs
  (`2026-10-10-load-the-changelog-and-developer-news`).
- One change from the plan: no note is added when no source opts in. The plan had one;
  with it the endpoint's answer would have changed on every deployment the moment this
  merged, and "nothing changes until a source is loaded" is the safer promise. The note
  for a skipped summary-evidence source stays, because it only appears once the owner has
  opted such a source in.
- The worker needs no change beyond the prompt: `flow.mjs` and `client.mjs` pass topics
  through without reading `source`.
- The exclusion test was checked by breaking the code: with the `human_decision` filter
  removed and the key read as truthy instead of `is True`, it failed on the
  owner-rejected row and on the row whose key is the string "true".
- Two limits, written into `AUTOMATION.md`:
  - Only pages the writer declined become official topics. A page that became a news
    story arrives as a site article; one held for review is not offered.
  - The automated route cannot operate a tool yet
    (`2026-10-09-give-the-automated-route-a-way`), so an official topic becomes a
    "what changed and what to do now" video resting on cited evidence. A hands-on
    tutorial still goes through the manual route.
- A summary-evidence source is skipped because the worker's page reader refuses pages
  over 3 MB (`tools/video/automation/fetch.mjs`), and such entries all point at one
  shared page. That leaves the Claude Code changelog out for now.
- OpenAI and Gemini are not in the first set: their update pages cannot be read by the
  scanner yet (`docs/official-ai-accounts.md`).
- Follow-ups filed with this work: the worker reads one entry of a shared changelog page;
  the owner pastes an official URL on `/admin/videos` to ask for a video; a checkbox for
  this source, if the owner wants one-click control.
