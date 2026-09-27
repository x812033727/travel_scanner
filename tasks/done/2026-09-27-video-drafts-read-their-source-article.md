---
id: 2026-09-27-video-drafts-read-their-source-article
title: Video drafts read their source article at a URL that answers 404
status: done
priority: P1
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-27T07:10:55Z
created_at: 2026-09-27T07:10:50Z
completed_at: 2026-09-27T07:21:23Z
branch: claude/video-source-article-url
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/api/app/video_automation/topics.py
  - apps/api/tests/test_video_automation_ai.py
---

# Video drafts read their source article at a URL that answers 404

## Why

On 2026-09-27 the host worker blocked `gpt-6-sol-luna-where-to-use`: its writer answered
`{"video": null, …}` twice, and its `claims.md` explained why. The only source in the payload,
`https://mokaair.com/zh-TW/guides/ai-news-gpt-6-sol-luna-20260923`, answered 404 with an empty
page, so the writer would not state any GPT-6 fact without a source. The article is live at
`https://mokaair.com/zh-TW/life/ai-news-gpt-6-sol-luna-20260923` (200).

Since the article restructure in #531 (2026-09-16), the site serves life articles at
`/<locale>/life/<slug>` and every other kind at `/<locale>/guides/<kind>/<slug>` (routes in
`apps/web/app/(ads-public)/[locale]`). `/<locale>/guides/<slug>` is a kind's list page and
answers 404 for an article. Three places still built the old address:

- `apps/api/app/video_automation/topics.py`: `SITE_URL = "https://mokaair.com/zh-TW/guides"`, with
  a comment saying life articles are read there. The planner copies these topic URLs into a
  draft's `source_urls`.
- `tools/video/automation/flow.mjs`: the writer (`write`) and the drama planner (`draftDrama`)
  read `https://mokaair.com/zh-TW/guides/${source_guide}`.
- `tools/video/review/sync.mjs` `GUIDE_URL` only recognised that shape, so `guideSlugs` would not
  find an article in a correct address.

Every automatic draft since the topics list went live (#754) has been written without its
site article. `openai-academy-learning-paths` has the same stale address in its `source_urls`
but had academy.openai.com as a second source, so it got further. `core/metadata.mjs`
`articleUrl`, which builds the YouTube description link, already had the right shapes.

## Definition of done

- [x] The topics endpoint lists each site article at `https://mokaair.com/zh-TW/life/<slug>`.
- [x] The writer, the fact-checker and the drama planner read a site article at the address
      its content pack's kind gives. A slug with no pack is read as a life article.
- [x] A draft that saved `/<locale>/guides/<slug>` for an article with a pack, or for its own
      article, reads the served address instead. A kind's list page stays as it is.
- [x] `guideSlugs` finds an article in `/life/<slug>` and `/guides/<kind>/<slug>` addresses and
      still in the old one, so earlier videos keep their topic.
- [ ] After the deploy, `gpt-6-sol-luna-where-to-use` is unblocked and its writer produces a
      script.

## Steps

- [x] `core/metadata.mjs`: `articlePath(pack)` holds the URL shapes; `articleUrl` uses it.
- [x] `automation/flow.mjs`: `siteArticleUrl(slug, root)` and `siteSources(sourceGuide, urls, root)`,
      used by `write`, `verify` and `draftDrama`.
- [x] `review/sync.mjs`: `GUIDE_URL` accepts `/life/<slug>`, `/guides/<kind>/<slug>` and the old
      `/guides/<slug>`.
- [x] `topics.py`: `SITE_URL` ends in `/zh-TW/life`, and a unit test pins the address.
- [x] Tests: `metadata.test.mjs`, `sync.test.mjs`, and a new test in `automation.test.mjs` for
      the stale addresses.
- [ ] Deploy, then unblock `gpt-6-sol-luna-where-to-use`. In the worker's
      `/var/lib/mokaair/video-work/<slug>/auto.json`, set `status` to `active` and remove `blocked`
      and `failures.writer`. The owner agreed on 2026-09-27, and the session that wrote this
      ticket does it after the deploy.

## How to verify

```bash
node --test tools/video/core/metadata.test.mjs tools/video/review/sync.test.mjs tools/video/automation/automation.test.mjs
cd apps/api && uv run pytest tests/test_video_automation_ai.py -q
# the addresses the worker now reads
curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/zh-TW/life/ai-news-gpt-6-sol-luna-20260923   # 200
curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/zh-TW/guides/ai-news-gpt-6-sol-luna-20260923 # 404, the old one
```

After the deploy, the worker log for `gpt-6-sol-luna-where-to-use` should show
`script drafted and passes lint` instead of `writer gave nothing usable`.

## Notes

- The unchecked item and step are the deploy and the unblock. They can only happen after this
  PR merges, so the ticket closes with the code and the session follows up on the host.
- The worker has no command to unblock a video. `block()` sets `status: "blocked"` in
  `auto.json`, and `step()` only advances `active` videos, so a person edits the file. An
  unblock action on `/admin/videos` would be a separate ticket.
- The writer's refusal was correct behaviour, not a model fault. Its `claims.md` also doubts
  whether "ChatGPT Work" exists and questions the "50% off the GPT-5.6 promotional price"
  wording. Once it can read the article, those points go to the fact-check.
