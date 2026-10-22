---
id: 2026-10-22-price-c07-dr-martens-local-pilot
title: Price C07 Dr Martens local pilot
status: done
priority: P2
area: docs
owner: codex-c07-quote
claimed_at: 2026-10-22T15:08:40Z
created_at: 2026-10-22T15:08:33Z
completed_at: 2026-10-22T15:09:41Z
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/production-quote.md
---

# Price C07 Dr Martens local pilot

## Why

C07 script and storyboard direction are owner-approved, but paid local production needs a complete per-film quote and an attributed budget route before any TTS, image, judging, or music call.

## Definition of done

- [x] A SHA-bound whole-film proposal with picture count, maximum attempts, narration/music scope, USD stop, and explicit prerequisite gates.

## Steps

- [x] Count current script/shot rows and optional long-shot states; verify current public provider prices.
- [x] Write the local-pilot quote and preserve the unapproved paid status and missing C07 budget route.

## How to verify

PowerShell table parser counted 73 script rows, 63 shot rows, 10 cards, 23 shot rows with narration longer than 33 characters, and 2,275 body characters. Verified MiniMax and Google official price pages; `rg` confirmed no C07 pilot-slug registration in the current server/media/TTS lists; `git diff --check` for the quote.

## Notes

The 86-image/258-attempt proposal is not an approval or a spending authorization. Actual TTS body time and illustration time share remain unmeasured, and C07 budget attribution support is absent. C03-C06 uncertain historical costs remain separately held.
