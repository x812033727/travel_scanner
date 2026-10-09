---
id: 2026-10-09-languages-card-says-the-site-cannot
title: Languages card says the site cannot upload dub tracks
status: done
priority: P1
area: web
owner: claude-fable-5.1
claimed_at: 2026-10-09T14:50:00Z
created_at: 2026-10-09T14:49:19Z
completed_at: 2026-10-09T15:04:24Z
branch: claude/youtube-audio-missing-languages-94f59a
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
  - docs/videos/DUBS.md
  - docs/videos/LANGUAGES.md
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
---

# Languages card says the site cannot upload dub tracks

## Why

On 2026-10-09 the owner reported that the published videos have no Japanese, Korean or
English audio. The production database showed sixteen `languages` batches carrying a
ready dub track, every one approved by the owner with the card's button「已在 Studio 上傳配音」,
and YouTube showed no extra audio track on any of them (`_v1vc2s3_MU` and `vxv8KrNual8`
carry five caption tracks and one audio track; a video with real dubs lists
`audioTrack` on its audio formats). The owner's words: 「我以為按了網站會幫我傳」.

The card does say the dub goes up in Studio, but nothing says the site *cannot* do it,
and the button reads like a command rather than a statement. The Data API has no audio
track method (docs/videos/DUBS.md), so until the VPS Studio operator does it
(`2026-10-09-vps-studio-uploader-uploads-the-dub`), the owner is the only path.

## Definition of done

- [x] The Studio box on the languages card says in its first sentence that the site cannot
      upload audio tracks because YouTube has no API for it, and that the button below only
      records what the owner did.
- [x] The approve button of the `languages` gate reads as the owner's statement
      (「我已經在 Studio 傳好這些配音」), in all five locales, and step 3 names the same words.
- [x] The language panel's dub state after approval reads 「你說已上傳」 rather than 「已上傳」,
      so a state the site never verified does not look like one it did.
- [x] The Studio box tells the owner the channel needs「進階功能」before Studio shows the dub
      control, since that was never field-tested (DUBS.md §站主要做的事).

## Steps

- [x] Reword `studioNote`, `approveLanguages`, `studioStep3` and `partStates.uploaded` in
      `apps/web/messages/*/admin.json` (five locales).
- [x] Cover the card's Studio box and the panel label in `admin-video-review-card.test.tsx`.
- [x] `npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web`.

## How to verify

Open `/zh-TW/admin/videos?video=meta-anti-scam-2fa-passkey`: the approved languages card
still lists the three tracks with download links and the Studio steps (the payload keeps
`"dub": "ready"`), the box opens with the sentence that the site cannot upload, and the
panel's dub cells read 「你說已上傳」.

## Notes

- Approving does not hide the files or the steps, so the owner can go back to the sixteen
  cards and upload the tracks now; the list of the eleven videos and their locales is in
  the 2026-10-09 session summary (ten on YouTube, `ai-agent-vs-chatbot` not yet).
- Resetting the sixteen approved batches to pending on production was offered and not
  chosen; the states stay as the owner left them.
- The site cannot verify the track either: `videos.list` does not expose audio tracks.
  The public watch page's `ytInitialPlayerResponse.streamingData.adaptiveFormats[].audioTrack`
  does, which is how this was confirmed, but that is scraping and is not built in.
- `2026-09-30-clarify-first-upload-of-pending-dubbed` covers the server side of the same
  trust problem (`language_states()` turning an approved batch's dub into "uploaded").
