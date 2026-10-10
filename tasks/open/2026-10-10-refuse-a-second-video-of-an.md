---
id: 2026-10-10-refuse-a-second-video-of-an
title: Refuse a second video of an official page and reset the article on a re-plan
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-10T14:10:30Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/AUTOMATION.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Refuse a second video of an official page and reset the article on a re-plan

## Why

Official pages the news writer declined are now offered to the video planner
(`official_topics` in `apps/api/app/video_automation/topics.py`), and the planner is told
to prefer one to a web result and to answer `"source_guide": null` with the page first in
`"source_urls"`. Two paths in the worker were written for site articles and do not cover
that answer. Both existed for web results before; an official page makes them matter,
because the same page stays in the candidates for 14 days and is listed ahead of every
search result.

1. **No code check stops a second video of the same official page.** The repeat guard in
   `tools/video/automation/flow.mjs` is `planProblem`: it refuses a plan whose main guide
   is in `usedGuides`, and `mainGuide()` only yields a site article's slug. A plan with no
   guide and an external first URL passes. `earlierVideos()` sends the planner each
   video's slug, title and `source_guide`, never a URL, and `official_topics` does not
   know which pages became videos. So an official page already made into a video, or one
   whose video the owner dropped, is kept out only by the planner matching an English page
   title against an earlier zh-TW video title. With a 72-hour draft interval one page is
   offered on four or more later drafts.
2. **A re-plan that moves to an official page keeps the previous article.** `replan()`
   sets `state.source_guide = requested?.source_guide ?? answer.source_guide ??
   state.source_guide`, so the `null` the prompt asks for falls through to the old slug.
   `draft()` and `planUnplanned()` use `plan.source_guide || null` instead. After such a
   re-plan the writer is handed the old article as the first source and told it is the
   source guide, the site records the video as retelling it, and the article sits in
   `used_guides` although no video of it exists.

Found by the review of the official-topics change on 2026-10-10. Neither was fixed there:
`flow.mjs` is bound by the duration receipt and was outside that task's scope.

## Definition of done

- [ ] A scheduled draft is not offered, and cannot plan, an official page (or any page
      without a site article) that an earlier automated video already rests on, dropped
      videos included. A refused plan gets the same second attempt a used site article
      gets.
- [ ] A scheduled draft's re-plan takes the planner's `source_guide` as given, `null`
      included. A drama adaptation and an owner's slides request keep their article.
- [ ] Tests for both in `tools/video/automation/automation.test.mjs`.
- [ ] `docs/videos/AUTOMATION.md` moves the third limit of 官方頁面當題目 into 不重複選題 as
      a rule the code enforces.
- [ ] The duration receipt is re-bound for `flow.mjs` by an independent reviewer.

## Steps

- [ ] Build the set of used pages from `automatedVideos(this.workBase)`, leaving out the
      video's own slug: each state's first `source_urls` entry where `source_guide` is
      null. Compare the first URL only; later URLs may be shared between videos.
- [ ] In `draft()`, the draft branch of `planUnplanned()` and `replan()`, drop topics whose
      `url` is in that set before the planner payload is built, and have `planProblem`
      refuse a plan with no guide whose first URL is in it.
- [ ] `replan()`: `requested?.source_guide ?? (drama ? answer.source_guide ??
      state.source_guide : answer.source_guide || null)`, or the equivalent that leaves the
      drama and the slides request as they are.
- [ ] The two tests; the document; the receipt increment.

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs
node --test tools/video/long-form/review.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- The 2026-09-25 repeat that led to the site-article guard happened because the worker
  did not know the earlier video at all (#759), not because the planner ignored a listed
  one. There is no recorded case of the prompt-only protection failing; this task closes
  the gap before one.
- A duplicate costs one production run and a waiting-draft slot. Nothing is published
  without the owner, who still sets the upload.
- The server stores only `source_guide` for a video (`video_projects`), so filtering on
  the API side would need the worker to report the page as well; the worker already has
  every earlier state on disk.
