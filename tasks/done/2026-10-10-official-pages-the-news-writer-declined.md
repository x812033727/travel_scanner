---
id: 2026-10-10-official-pages-the-news-writer-declined
title: Official pages the news writer declined become video topic candidates
status: done
priority: P2
area: api
owner: claude-opus-5-5-official-accounts
claimed_at: 2026-10-10T08:58:33Z
created_at: 2026-10-10T07:35:26Z
completed_at: 2026-10-10T09:23:47Z
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
  - apps/web/app/api/video/automation/topics/route.ts
  - docs/videos/ai-terms/README.md
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
- [x] `docs/videos/AUTOMATION.md` describes the third source and its limits.
- [x] The duration receipt is re-bound by an independent reviewer.

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
- [x] Receipt: `tools/video/long-form/review.mjs` binds `schemas.py` and `prompts.mjs`.
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

- Receipt: reviewer `claude-pr-review-official-topics` (a separate agent that wrote none of
  the change) reviewed commit `30544d813` for DURATION_ONLY and passed it; the increment is
  "Official pages as video topics increment" in `docs/videos/long-form/review.md`. It binds
  the bytes of that commit: if a rebase or a merge with main changes `schemas.py` or
  `prompts.mjs` again, the two hashes have to be reviewed and bound again.
- Decided with the plan the owner approved on 2026-10-10: the switch is the per-source
  config key, not a checkbox on `/admin/videos`. A setting would need a migration and
  changes to ten receipt-bound files; the key needs neither, and turning it on is the
  same owner-approved host load every `sources.json` change needs
  (`2026-10-10-load-the-changelog-and-developer-news`).
- One change from the plan: no note is added when no source opts in. The plan had one;
  with it the endpoint's answer would have changed on every deployment the moment this
  merged, and "nothing changes until a source is loaded" is the safer promise. The note
  for a skipped summary-evidence source stays, because it only appears once the owner has
  opted such a source in.
- The worker passes topics through without reading `source` (`flow.mjs`, `client.mjs`),
  so only the prompt changed here. Two of its paths do not cover a topic without a site
  article, though: nothing in code refuses a second video of the same official page, and
  a re-plan that moves to an official page keeps the previous article as `source_guide`.
  Both are `2026-10-10-refuse-a-second-video-of-an`; `flow.mjs` is receipt-bound and was
  outside this task.
- Reviewed from six angles on 2026-10-10 after the merge with main, each finding checked
  by a second agent. Fixed here: a topic from a source without dates no longer carries
  the scan day as its date; the tests now pin the status filter (a `needs_redraft` row),
  the ordering (oldest inserted first) and the note's way into the endpoint's answer;
  the reason a summary-evidence source is skipped is stated correctly (a shared page,
  and only the Claude Code changelog is also past 3 MB); the host-load ticket says that
  it switches this on.
- The exclusion test was checked by breaking the code: with the `human_decision` filter
  removed and the key read as truthy instead of `is True`, it failed on the
  owner-rejected row and on the row whose key is the string "true".
- Three limits, written into `AUTOMATION.md`. The third came from the review: no code
  check refuses a second video of an official page, and a re-plan keeps the previous
  article (`2026-10-10-refuse-a-second-video-of-an`). The first two:
  - Only pages the writer declined become official topics. A page that became a news
    story arrives as a site article; one held for review is not offered.
  - The automated route cannot operate a tool yet
    (`2026-10-09-give-the-automated-route-a-way`), so an official topic becomes a
    "what changed and what to do now" video resting on cited evidence. A hands-on
    tutorial still goes through the manual route.
- A summary-evidence source is skipped because its entries all point at anchors on one
  shared page: the worker would read the top of that page (the first 40,000 characters,
  `tools/video/automation/fetch.mjs`), not the entry. The Claude Code changelog page is
  also 4.8 MB, past the reader's 3 MB limit, so it cannot be read at all. That leaves
  the Claude Code changelog and the Claude Platform release notes out for now.
- OpenAI and Gemini are not in the first set: their update pages cannot be read by the
  scanner yet (`docs/official-ai-accounts.md`).
- Follow-ups filed with this work: the worker reads one entry of a shared changelog page;
  the owner pastes an official URL on `/admin/videos` to ask for a video; a checkbox for
  this source, if the owner wants one-click control.
