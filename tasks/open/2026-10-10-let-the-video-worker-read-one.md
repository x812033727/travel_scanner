---
id: 2026-10-10-let-the-video-worker-read-one
title: Let the video worker read one entry of a shared changelog page
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-10T09:02:25Z
completed_at:
branch:
depends_on:
  - 2026-10-10-official-pages-the-news-writer-declined
scope:
  - tools/video/automation/fetch.mjs
  - tools/video/automation/automation.test.mjs
  - apps/api/app/video_automation/topics.py
  - apps/api/tests/test_video_automation_topics.py
  - docs/videos/AUTOMATION.md
---

# Let the video worker read one entry of a shared changelog page

## Why

Official pages the news writer declined are offered to the video planner as topics
(`official_topics` in `apps/api/app/video_automation/topics.py`), except those of a source
read from its feed summary: the Claude Code changelog and the Claude Platform release
notes. Every entry of such a source is an anchor on one shared page. The worker's page
reader gives up above 3 MB (`MAX_PAGE_BYTES` in `tools/video/automation/fetch.mjs`) and the
Claude Code changelog page was 4.8 MB on 2026-10-10, so the writer and the fact-checker
could not read the entry a topic would name.

Claude Code releases are what the channel's tutorials are mostly about, so this is the
gap that matters most among official sources.

## Definition of done

- [ ] A topic of a summary-evidence source reaches the writer and the fact-checker with
      the text of that one entry, not the shared page.
- [ ] `official_topics` stops skipping such a source once that works.
- [ ] `docs/videos/AUTOMATION.md` drops the "skipped for now" paragraph.

## Steps

- [ ] Choose the route: the API hands the entry's stored evidence (the feed summary, in
      `news_evidence.excerpt`) to the worker with the topic; or the worker reads the
      source's feed and takes the entry by its anchor. The first needs no fetch at all.
- [ ] Decide how the fact-checker re-reads it later, when the feed has rolled on (the feed
      lists about fifteen entries).
- [ ] Implement, with tests on both sides.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_automation_topics.py -q
node --test tools/video/automation/automation.test.mjs
```

## Notes

- `tools/video/automation/prompts.mjs`, `flow.mjs` and `automation.test.mjs` may be bound by the duration receipt
  (`tools/video/long-form/review.mjs`): touching them needs an independent DURATION_ONLY
  increment.
- Titles of the Claude Code changelog are bare version numbers ("2.1.296"); a topic title
  made from one tells the planner nothing. The first lines of the entry would have to
  stand in.
