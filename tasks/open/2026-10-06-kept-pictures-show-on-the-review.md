---
id: 2026-10-06-kept-pictures-show-on-the-review
title: Kept pictures show on the review card, their summary fits the server's limit, and only illustrated videos keep them
status: review
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
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
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

A review of this pull request found a fourth, the same stall one field over:

4. **The payload has a limit too.** The server refuses a review whose payload is larger than
   262,144 bytes (`ReviewIn._small`), with the same 422. What the judge said of a kept
   picture is the remarks of every take, and each review carried them twice: the final in
   `accepted_pictures` and again as a warning of the `assemble` item inside
   `manual_review_qa`, the storyboard in `accepted` and again in each shot's own verdict.
   Two hundred kept pictures with nine remarks of 300 characters each are over a megabyte.

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
- [x] A final review and a storyboard review with any number of kept pictures stay within
      the server's payload limit: every kept picture keeps its id, what the judge said is
      cut until the payload fits, and a review that still cannot fit is refused by
      `review-push` with its size, never by the server.
- [x] A storyboard whose every shot was kept shows no automatic-check label with nothing
      after it, and the Japanese pill on a kept shot does not read 「保留」 (on hold).

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
- [x] `tools/video/qa/cli.mjs`: the `assemble` item carries one warning for the kept
      pictures, their number and at most five ids (`keptPicturesWarning`), where it carried
      a line of remarks for each.
- [x] `tools/video/review/sync.mjs`: `keptRemarks` (six lines of 300 characters, then a
      line counting the rest), `payloadBytes` (the server's measure) and `fitPayload`, which
      `reviewPush` passes every review through before the post: two lines a picture, then
      none, while the payload is past 240,000 bytes, and a refusal with the size when it is
      still past the server's limit.
- [x] `apps/web/components/admin-video-review-card.tsx`: the storyboard's automatic-check
      line only when the board has a score. `apps/web/messages/ja/admin.json`: `shotKept`
      is 「採用」, and the kept pictures are 「イラスト」 as on the settings page.
- [x] Tests: `sync.test.mjs` (the fake site answers 422 past 262,144 bytes as the server
      counts them; two hundred kept pictures with nine remarks of 300 characters go up as a
      storyboard and as a cut; a storyboard that cannot fit is not sent), `qa.test.mjs` (the
      one warning), `admin-video-kept-pictures.test.tsx` (seven cases for the line).

## How to verify

```bash
node --test tools/video/review/sync.test.mjs tools/video/qa/qa.test.mjs tools/video/media/look-keyframes.test.mjs
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-kept-pictures.test.tsx components/admin-video-review-card.test.tsx components/admin-video-storyboard-pages.test.tsx components/admin-video-reviews.test.tsx
```

`node tools/video/long-form/cli.mjs check` is red on this branch until an independent
reviewer re-binds the duration receipt: `sync.mjs`, `sync.test.mjs`,
`look-keyframes.test.mjs`, `qa/cli.mjs`, `qa/qa.test.mjs`, `admin-video-review-card.tsx` and
the five `admin.json` are bound files (`tools/video/long-form/review.mjs` `REVIEW_FILES`),
eleven in all, and the author may not re-bind.

After the deploy: a video with kept pictures shows, on its final card, the amber notice with
the reason, 「自動品管」 with a 「僅供參考」 pill, and 「保留的插圖（N 張）」 with one row per
picture; on its storyboard card the kept shots have a blue border and a 「保留」 pill. A
video with many kept pictures logs `the judge's remarks on the kept pictures were cut to 2
lines a picture` (or `were left out`) when it sends a review, and the review is there.

## Notes

- **Pull request.** #1344, a draft against main on `claude/video-unstuck-kept-pictures-card`,
  opened on 2026-10-06. It waits for the independent re-binding of the duration receipt
  (above) before it can be green.
- **What verification found on 2026-10-06 (head `3127e6e3e`): the receipt, and nothing
  else.** The stale receipt reddens more than `cli.mjs check`. On the pull request CI's
  `web-checks` (`npm run test:tools`, 1 failure in 1,897 tests) and Video tooling's `smoke`
  (1 in 1,605) both fail in `tools/video/long-form/review.test.mjs`, 「the shipped
  independent duration review binds the current plans and implementation」; `web` fails
  only as the roll-up of `web-checks`, and every other check is green.
  `checkDurationReview()` returns nine `stale duration review binding` problems: one for
  each bound file named under How to verify, and for no other. Checked for the reviewer:
  that test file passes 2 of 2 on an export of the base `a435f0672`; each of the nine
  hashes `review.json` holds equals the base's file, so the baseline holds; and main up to
  `fdc0ce920` (#1345) changed none of the 108 bound files, so the increment is these nine
  files against that base and needs no merge first. The pass that repaired what
  verification found changed no code and left `review.md` and `review.json` as they were.
  It works on the author's side (`author_agent` is this task's owner),
  `durationReviewProblems` refuses a receipt whose reviewer is its author, and
  `.agents/skills/dev-and-ci/references/duration-receipt.md` gives the re-binding to the
  review agent alone. One step is left, and it comes last because any later edit to one of
  the nine files stales the receipt again: an independent reviewer (`claude-pr-review-1344`)
  reads the nine diffs, adds a `## PR #1344 … increment: 9 files (2026-10-06)` section to
  `review.md` and binds the nine hashes in both files.
  A second verification, on head `f74b00490`, handed back that one problem again and no
  other, and the pass that answered it changed nothing but this note. On that head CI
  fails in the same two jobs on the same one test (1 of 1,897 and 1 of 1,605, every other
  check green), `checkDurationReview()` names the same nine files, each of the nine hashes
  `review.json` holds still equals the file at the base `a435f0672`, the other 99 bound
  files match their bindings, and main has not moved past `fdc0ce920`. The nine files are
  as final as verification can make them, so the re-binding can start from the branch as
  it is; another pass on the author's side has nothing it may change.
- **The payload limit and two card details (2026-10-06, after head `cee129f71`): the
  receipt's increment is eleven files now.** The pass that made these three fixes changed
  six bound files: `sync.mjs`, `sync.test.mjs`, `admin-video-review-card.tsx` and
  `ja/admin.json` again, and `tools/video/qa/cli.mjs` and `tools/video/qa/qa.test.mjs` for
  the first time. `checkDurationReview()` names eleven stale bindings on the result, the
  nine above and those two, and no other problem; what the two notes above say of nine
  files, and of the branch being ready for the re-binding as it was, is superseded by this
  one. Nothing here touches a duration rule: the qa change is the text of one warning on
  the `assemble` item, whose verdict and detail are as they were. The pass merged main
  (`fdc0ce920`, #1345) first, which changed none of the bound files, and left `review.md`
  and `review.json` alone as before.
- **How a payload is measured.** `ReviewIn._small` takes
  `len(json.dumps(value, ensure_ascii=False).encode())`: Python's default separators put a
  space after every comma and colon, and text outside ASCII stays as it is, three bytes a
  Chinese character. `payloadBytes` writes the same (on the JSON the request carries), so
  it agrees with the server to the byte except for a very small number such as `1e-7`,
  which Python writes `1e-07`. That is what the gap between the budget (240,000) and the
  limit (262,144) is for. The fake site in `sync.test.mjs` counts apart from it: the
  compact JSON plus one for each separator.
- **What is cut, and what is not.** Only what the judge said of kept pictures: on a final
  `accepted_pictures[].problems`, on a storyboard `accepted[].problems` and the
  `judge.problems` of the shots sent with `accepted: true`. The server reads none of the
  three (`storyboard_check_passed` skips an accepted shot's verdict), and the worker reads
  `shots[].judge.problems` only of shots with `needs_review` (`flow.mjs` `storyboardGate`,
  for the prompt fix), so those and the board's own `judge.problems` go up whole. The
  builders still assemble the whole remarks; `fitPayload` cuts them in one place, where
  `reviewPush` posts, so the line that counts the rest always counts from the whole list.
  With no line left the list's entry says so (「意見因審核資料的大小上限略去…」) and the kept
  shot's own verdict is empty: the card reads the list first and the shot's verdict only
  when the list has nothing, so the note shows once.
- **A review that still does not fit is refused before the post, with the lint code.**
  `fitPayload` throws a `ReviewError` with code `payload_too_large`, and `fail` answers it as
  it answers the server's 413 and 422: the worker blocks the video with the message as the
  reason (`submissionFailure`), which names the gate, the size and the limit. The server's
  own answer to such a payload names none of them: 「payload：格式或內容不正確」
  (`apps/api/app/problems.py` `_localized_issue`), which is what the fake site answers too.
  Between the budget and the limit a review is sent as it is: a screenplay of 250 KB went
  up before this change and still does. The limit follows the server's rule, 1 MB for the
  screenplay of a long-anime series episode (`payloadLimit`, with `validateAnimeRuntime`
  standing for `AnimeRuntimeSpec`).
- **Not bounded here.** A storyboard's `shots[].prompt`, up to 1,000 characters a shot by
  the writer's budget: two hundred shots with prompts of that length come to about the
  limit by themselves, kept or not, and a board past it is now refused with its size,
  where it was a bare 422 before. Sending it in pages is another change. The outline
  review the worker posts itself (`flow.mjs` `submitOutline`) does not pass through
  `fitPayload`; its payload is the brief and its options.
- **Reverse checks of this pass.** With the fitting switched off in `reviewPush` the
  two-hundred-pictures test fails at its first push: the storyboard is answered
  「payload：格式或內容不正確」 and `review-push` exits 1 where 0 is expected, which is the
  stall; the twelve-pictures test fails on remarks that went up whole. With the
  storyboard's line rendered whatever the score, the seven new component cases fail.
- **The Japanese strings.** 「保留」 is the Chinese word; in Japanese it reads "on hold",
  which is the opposite of a picture that was taken. The other new strings were read again
  in Japanese and Korean and none carries a Chinese word over (the Korean pill is 「유지」,
  not 「보류」). One was changed for another reason: the kept pictures were 「挿絵」, and the
  settings page and the rest of the admin call the same pictures 「イラスト」.
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
- **Left for later.** The final card lists kept pictures by shot id with no time in the
  cut; the payload carries chapters but not each shot's start. (The payload limit, which
  stood here as left for later, is done: see above.)
- **The claim was forced.** The scope overlaps three sibling tasks of the same owner
  (in review) and `2026-10-01-hand-off-owner-approved-renewed-finals`
  (codex-video-stall-followthrough, claimed 2026-10-04, stale by the 24-hour rule; its
  branch is not on origin), which lists `sync.mjs` and `sync.test.mjs`. The two qa files
  added to the scope later are also in the scope of
  `2026-10-06-pictures-keep-best-after-prompt-fixes` (the same owner, in review; its change
  is on main as #1341).
- **Verified at `4d296e304` (2026-10-07, independent read-only reader).** Worst case
  through `review-push` and the fake site: 200 kept pictures, 165-character ids, nine
  remarks of 300 characters each, measured as `ReviewIn._small` does
  (`len(json.dumps(payload, ensure_ascii=False).encode())`, equal to `payloadBytes` to the
  byte). The final review is 56,691 bytes (CJK or astral remarks, which are left out) or
  173,691 bytes (ASCII, cut to two lines); the storyboard is 241,737 bytes. Every summary
  is at most 500 characters. Every field the card reads is still there. The tests in
  "How to verify" are green. One limit is left: a kept shot still costs about 300 bytes
  after its remarks are left out, because its id is repeated in `payload.accepted` with
  the "left out" line. So a board of 200 shots with long ids and long prompts, all kept,
  is refused at 270,537 bytes, while the same board with nothing kept goes up at 210,720.
  That is beyond any brand story's 85–100 shots; it is filed as
  `2026-10-06-a-storyboard-with-many-kept-pictures`. Also on the storyboard, a kept
  shot's remarks travel twice (`shots[].judge.problems` and `payload.accepted[].problems`)
  until the last step empties the shot's copy. "Remarks sent once" holds for the final
  review only.
