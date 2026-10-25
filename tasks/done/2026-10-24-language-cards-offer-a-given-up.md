---
id: 2026-10-24-language-cards-offer-a-given-up
title: Language cards offer a given-up dub's current track as an unchecked download
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-24T10:25:56Z
created_at: 2026-10-24T10:25:07Z
completed_at: 2026-10-24T11:03:15Z
branch: claude/unchecked-dub-downloads
depends_on: []
scope:
  - tools/video/core/stages.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/api/app/video_youtube/language_package.py
  - apps/api/tests/test_video_youtube_language_package.py
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
  - docs/videos/DUBS.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Language cards offer a given-up dub's current track as an unchecked download

## Why

On 2026-10-24 the owner looked at the A4 (`story-adapt-a4-paper-size`) language card: only the
Indonesian dub had a download. ja, ko, en, pt, th and vi had current tracks on the host, but the
check had heard a few lines wrong, so the batch only said 「配音跳過（Jev still hears …）」 with no
file. The owner wants every dub downloadable, and the right version, to judge and upload by hand.

## Definition of done

- [x] `dubsForUpload` also returns, for a given-up locale, its track when `currentDub` reads it
  current, with the lines `check-audio` flagged for this take (id, seconds, intended, heard; max 20).
- [x] The language batch attaches it as `dub_unchecked_<locale>` and writes `dub.unchecked`
  (file, format, role, sha256, lines) beside the skip; a stale take is not sent.
- [x] YouTube sync's `compose` accepts it for a skipped dub (audio only) and never sends it.
- [x] The card offers 「下載 <file>（沒過自動檢查）」 and lists the failed lines.
- [x] Duration review increment for the bound files (`claude-pr-review-unchecked-dubs-20261024`, PASS).
- [x] Merged, deployed; A4's language batch sent again and its card checked. Deployed 413a4b3e4; A4's batch of 2026-10-24 11:01Z offers en, ja, ko, pt, vi, th unchecked and id ready, 23 failed lines; downloaded ja/ko hashes match the host.

## How to verify

`node --test tools/video/review/sync.test.mjs tools/video/core/stages.test.mjs tools/video/review/language-contract.test.mjs` (107);
`cd apps/api && uv run pytest tests/test_video_youtube_language_package.py tests/test_video_youtube_language_contract.py tests/test_video_languages_worker.py`;
`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx` (85).

## Notes

- Claimed with --force: `2026-10-19-worker-video-languages-five` also lists `tools/video/core/stages.mjs`,
  but its code merged as #1611/#1614 on 2026-10-20 and it only waits in review.
- The committed language contract cases have no given-up dub with a track, so the contract bytes
  are unchanged.
