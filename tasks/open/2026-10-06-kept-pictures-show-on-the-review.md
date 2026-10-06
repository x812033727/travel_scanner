---
id: 2026-10-06-kept-pictures-show-on-the-review
title: Kept pictures show on the review card, their summary fits the server's limit, and only illustrated videos keep them
status: in-progress
priority: P1
area: web
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T12:27:53Z
created_at: 2026-10-06T12:27:16Z
completed_at:
branch: claude/video-unstuck-kept-pictures-card
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-kept-pictures.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/ILLUSTRATED.md
---

# Kept pictures show on the review card, their summary fits the server's limit, and only illustrated videos keep them

## Why

Since PR #1341 an illustrated slides video whose pictures still fail the judge after two
prompt fixes keeps the best take of each (`keyframes --accept-best`), its storyboard marks
those shots accepted, and its final cut goes up for the owner's own review. The owner
decided on 2026-10-06 that such a cut is never approved automatically and that its review
card lists the kept pictures. Three things were left open:

1. **A stall waiting to happen.** The final review's summary named every kept shot id, and
   the site takes a summary of at most 500 characters (`ReviewIn.summary`,
   `apps/api/app/video_reviews/schemas.py`). With dozens of kept pictures the site answers
   422, `review-push` exits with the lint code, and the worker blocks the video
   (`automation/flow.mjs` `submissionFailure`): the change that was meant to stop videos
   blocking on their pictures would block them one step later.
2. **`--accept-best` kept any video's pictures.** Only an illustrated video's cut is sent for
   the manual review (`sync.mjs` `acceptedPicturesOf` and `flow.mjs` `acceptBestPictures`
   both ask `illustrated(doc)`). Run by hand on a drama, the command took the shot out of
   `needs_review`; its storyboard and cut could then be approved on arrival with nobody
   asked to look at the picture.
3. **The card showed none of it.** The review card listed quality-check items from
   `payload.qa` alone and read neither `manual_review`, `manual_review_reason`,
   `manual_review_qa`, `accepted_pictures` nor `accepted`, so for a cut with kept pictures
   the owner saw one summary line.

## Definition of done

- [x] A final review with any number of kept pictures is accepted by the site: its summary
      names at most five ids and counts the rest, and no review `review-push` sends carries
      a summary longer than 500 characters.
- [x] `keyframes --accept-best` on a video that is not illustrated is a usage error that
      says why, and writes nothing; the worker's own call still works for every video
      `illustrated()` covers.
- [x] The final review card shows why the cut waits for the owner, the quality check
      marked as for reference only, and every kept picture with the judge's remarks; the
      storyboard card marks kept shots apart from shots waiting for a prompt fix.
- [x] A payload missing any of those fields, or carrying them in another shape, shows
      nothing for that part and never breaks the card.

## Steps

- [x] `tools/video/review/sync.mjs`: `namedPictures` (first five ids, then 「等，另 N 張」) in
      the final summary and in `manual_review_reason`; `fitSummary` on every review
      `reviewPush` posts and on the outline review `outlineReview` builds, which the worker
      posts itself (cut at 500 code points, the last an ellipsis); `audioSummary` drops the
      cleared line ids when they would not fit.
- [x] `tools/video/media/keyframes.mjs`: `acceptBest` refuses a video that is not
      `illustrated(doc)`.
- [x] `apps/web/components/admin-video-review-card.tsx`: the manual-review notice, the
      reference-only mark on `CheckItems`, the kept-pictures block, the kept mark on
      storyboard shots; eight strings in the five locales.
- [x] Tests: `sync.test.mjs` (the helpers; eighty kept pictures with long ids through the
      fake site, which answers 422 past 500 characters), `look-keyframes.test.mjs` (a drama
      and an explainer refused; slides and a screencast with stills kept by the worker's
      call), `admin-video-kept-pictures.test.tsx` (36 cases, most of them malformed payloads).
- [x] `docs/videos/ILLUSTRATED.md`: the follow-up under the 2026-10-06 section.

## How to verify

```bash
node --test tools/video/review/sync.test.mjs tools/video/media/look-keyframes.test.mjs
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-kept-pictures.test.tsx components/admin-video-review-card.test.tsx components/admin-video-storyboard-pages.test.tsx components/admin-video-reviews.test.tsx
```

`node tools/video/long-form/cli.mjs check` is red on this branch until an independent
reviewer re-binds the duration receipt: `sync.mjs`, `sync.test.mjs`,
`look-keyframes.test.mjs`, `admin-video-review-card.tsx` and the five `admin.json` are bound
files (`tools/video/long-form/review.mjs` `REVIEW_FILES`), and the author may not re-bind.

After the deploy: a video with kept pictures shows, on its final card, the amber notice with
the reason, 「自動品管」 with a 「僅供參考」 pill, and 「保留的插圖（N 張）」 with one row per
picture; on its storyboard card the kept shots have a blue border and a 「保留」 pill.

## Notes

- **Reverse checks** (the base tree exported with `git archive`, the new tests copied in;
  run again by the agent that finished this from the first one's patch). The new keyframes
  test fails on the base at the first `--accept-best`: an explainer's failing shot is kept,
  exit 0 where 2 is expected. With `namedPictures` and `fitSummary` switched off in a copy
  of `sync.mjs`, the eighty-pictures test fails on `summary：內容太長` with exit 1, which is
  the stall; with only the fitting in `reviewPush` off it fails the same way where five
  206-character ids are past the limit; with only `outlineReview` unfitted the helper test
  reads 926 characters where 500 are expected. On the base card 25 of the 36 new component
  cases fail; the 11 that pass assert that nothing is shown.
- **The wording 「等，另 N 張」.** N is the number of pictures not named. 「a、b 等 80 張」
  reads in Chinese as eighty in all, and the sentence already opens with that total.
- **`manual_review_reason`** is not limited by the server beyond the payload's 256 KB and was
  rendered nowhere; the card renders it now, so it names five ids like the summary. The
  server writes the same field from the owner's own text on a renewal (up to 2000
  characters), which the card shows as typed.
- **Other summaries in `sync.mjs`.** Storyboard, script, look, publish and dubs carry
  counts and a fixed handful of codes (eleven check ids, four locales). The audio summary
  named every line a second transcript cleared, eight characters each, with no bound:
  about fifty would pass the limit. It now falls back to the count. The outline summary
  ends in Jev's choice, which `pickFrom` takes as any text. `fitSummary` is the last line
  of defence for all of them: a scene id has no length limit (`core/schema.mjs`
  `SCENE_ID`). It is applied in two places, which between them cover every review this
  file assembles: in `reviewPush`, after the renewal binding and before the post, and in
  `outlineReview`, because `flow.mjs` `submitOutline` posts that review through the
  automation client and never reaches `reviewPush`. Reviews built outside this file
  (`import/import.mjs`, `shorts/push.mjs`, `review/renewal-handoff.mjs`, and the
  languages batch `flow.mjs` `tidiedLanguages` sends for a tidied video) have summaries of
  a fixed size (four locales at most, a constant reason) and do not pass through it.
- **`illustrated()` covers a screencast with stills too**, not only format `slides`: any
  video that is not a drama and has `shot` scenes. Such a video draws under the drama
  route's switch and model (`stages.mjs` `choiceFor` reads the slides choice for format
  `slides` alone), so its test uses the drama status.
- **What `automation/flow.mjs` writes for kept pictures** (read, not changed: another pull
  request owns the file). Nothing it sends in the project report can pass a server limit:
  the title is cut to 200 where each state is created, the stage is `slice(0, 40)` and
  every stage on this path is a short constant, the checklist is at most twenty rows (one
  blocked row and up to nineteen steps), and the blocked row's label is cut to 120
  (`blockedLabel`). The line `acceptBestPictures` returns carries counts only and goes to
  the log. Its note, `keyframes: N pictures kept … (every id) …`, has no bound: it is kept
  in `auto.json` and sent as `owner_notes` in every later writer payload
  (`StageRunIn.payload` has no size limit, so nothing refuses it; it costs tokens and reads
  as the owner's words). Naming five there too would match this change. One thing there
  is not about kept pictures: `blockedLabel` and the stage are cut with `String.slice`,
  which counts UTF-16 units, so a character outside the basic plane that straddles the
  cut is left as half a pair; the limit itself is never passed.
- **Left for later.** The payload limit of 256 KB is the next thing a refused submission
  could come from, not the summary: a kept picture's remarks travel twice in each review
  (`shots[].judge.problems` and `accepted[].problems` on the storyboard;
  `accepted_pictures[].problems` and the `assemble` item's `warnings` in
  `manual_review_qa` on the final). By a rough count (not measured on a real video) a
  storyboard of sixty kept shots with 1,000-character prompts and three remarks each is
  about 120 KB, so it is not close today. The final card lists kept pictures by shot id
  with no time in the cut; the payload carries chapters but not each shot's start.
- **The claim was forced.** The scope overlaps three sibling tasks of the same owner
  (in review) and `2026-10-01-hand-off-owner-approved-renewed-finals`
  (codex-video-stall-followthrough, claimed 2026-10-04, stale by the 24-hour rule; its
  branch is not on origin), which lists `sync.mjs` and `sync.test.mjs`.
