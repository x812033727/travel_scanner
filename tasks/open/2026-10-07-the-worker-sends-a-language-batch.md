---
id: 2026-10-07-the-worker-sends-a-language-batch
title: The worker sends a language batch before the upload confirmation it must follow
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T08:03:28Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# The worker sends a language batch before the upload confirmation it must follow

## Why

YouTube sync reads a language batch only beside the upload confirmation it was sent after:
`apps/api/app/video_youtube/language_package.py` `compose()` ignores any `languages` review
created at or before the newest approved `publish`, and reads the confirmation's own package
instead.

The worker sends the batch as soon as every chosen part is made, once the final is approved,
whether the confirmation is approved yet or not (`tools/video/automation/flow.mjs`
`languages()`). It runs `package` first, so `upload/metadata.json` changes, and while the video
is not done the next round sends a new confirmation for that package (`advance()`, "on
YouTube"). That confirmation is newer than the batch, so the batch is never read:

- titles, descriptions and captions still reach YouTube, because the new confirmation's
  package carries them (the fallback branch of `compose()`);
- a ready dub does not: a confirmation never attaches `dub_*` tracks, so the fallback refuses
  "已選取的 <locale> 配音尚未核准，請先完成語言包" and the video cannot be synced.

The worker also sends nothing when the owner changes the choice after a batch went up and
every part still chosen was already made: narrowing it ({en, ja} to {en}), or going back to an
earlier choice. `pendingLanguages()` reads the site's merged part states, which still say every
remaining part is ready, and past the confirmation `repackage` is false, so `languages()` returns
null. `compose()` reads only the newest batch, whose `choice.locales` is no longer the site's, and
refuses every sync with "語言選擇已變更，請依目前勾選內容重新送審" until someone runs `package`
and `review-push --gate languages` by hand (the producer then binds it, `follows` included).

Since 2026-10-07 every batch names the confirmation it was sent after
(`2026-09-30-youtube-approved-languages-sync`, docs/videos/APPROVED-LANGUAGE-PACKAGE.md), so a
batch sent after the confirmation is approved is read as intended. Only these two orderings are
left.

## Definition of done

- [ ] A video whose languages were chosen before its confirmation was approved reaches YouTube
      sync with a language batch newer than that confirmation, ready dubs included.
- [ ] A choice narrowed or changed back after a batch went up is followed by a batch of the
      current choice (when it is not empty: `compose()` reads no batch for an empty choice).
- [ ] Videos already on YouTube are not sent new batches unless the owner decided how (a new
      batch with a ready dub waits for the owner's approval again, and `compose()` then refuses
      every sync of that video until it is approved).

## Steps

- [ ] Ask the owner: send the batch only after the confirmation is approved (the panel shows the
      parts as in the making until then), or send it again after the confirmation (one more
      batch, and one more owner approval when it has a dub); and whether a changed choice is
      sent again the same way (compare the site's choice with `review/languages.json`'s
      `choice.locales`).
- [ ] Implement the chosen order in `flow.mjs` and cover both orders in `automation.test.mjs`
      (its fake site keeps `created_at`; the consumer compares it).
- [ ] Rebind the duration receipt independently (both files are bound).

## How to verify

`node --test tools/video/automation/automation.test.mjs`, with a test where the owner chooses a
dubbed language before approving the confirmation and the newest batch is created after the
approved confirmation; and the API contract test with such a fixture
(`apps/api/tests/test_video_youtube_language_contract.py`).

## Notes

- Found while binding normal batches to their source (claude-happy-carson, PR #1361).
- The first-upload policy for a pending dub is `2026-09-30-clarify-first-upload-of-pending-dubbed`;
  decide this ticket's order together with it.
