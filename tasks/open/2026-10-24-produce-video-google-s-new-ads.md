---
id: 2026-10-24-produce-video-google-s-new-ads
title: Produce video: Google's new ads exception for Gmail, Drive and Photos connected to AI search (google-ai-search-ads-exception)
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-news-video
claimed_at: 2026-10-24T11:27:35Z
created_at: 2026-10-24T11:26:58Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/google-ai-search-ads-exception
---

# Produce video: Google's new ads exception for Gmail, Drive and Photos connected to AI search (google-ai-search-ads-exception)

## Why

The owner asked on 2026-10-24 to keep producing AI/tech current-events videos (after ai-shopping-agents-blocked and claude-duet-proactive-agent, PR #1700). Picked Google's privacy-policy change effective 2026-10-16: the "Drive, Gmail, or Photos" no-ads promise gained an exception for users who connect those apps to Search's Personal Intelligence / AI Mode. Reported by The Verge 2026-10-23; the site's hourly news has `ai-news-google-personal-intelligence-ads-20261023` (DB only, so it goes in `sources`, not `source_guide`). Every fact rests on Google's own pages: the current policy, the 2026-10-01 archived version, and four Search Help pages.

Route: teaching-card short (teaching-flow §十 one concept, §十二 picture rules, PAPER.md paper look), `category: "ai-news"`, 8-minute floor. **On-screen text in English** (owner 2026-10-24: the video is multilingual, so the single picture track should not depend on Traditional Chinese; narration stays zh-TW, zh-TW is CC). Locale thumbnails and every other rule stay as they are.

## Definition of done

- [ ] `docs/videos/google-ai-search-ads-exception/` holds brief.md, video.json, claims.md and verify-*.md; lint has zero errors and the storytelling panel passes (or its misses are fixed and recorded).
- [ ] Outline recorded (owner's standing word: take the recommended option), narration, final and publish gates pushed to /admin/videos (hand-pushed: every gate waits for the owner).
- [ ] final.mp4, captions and the upload package exist in the local workdir and qa passes 11/11 (policy and narration items are the owner's call at the final gate).
- [ ] Eight languages (en, ja, ko, es, pt, id, vi, th; owner 2026-10-24 「不只三語了現在是八語」) titles/descriptions, CC, locale thumbnails and dubs made once the owner ticks them on the video page; `review-push --gate languages` accepted.

## Steps

- [x] Sources saved to `<home>/mokaair-work/videos/google-ai-search-ads-exception/_tools/sources/` (policy current + 2026-10-01 archive, help 16859283 / 17212611 / 17025248 / 17026260 / 17265703); brief.md written with 3 outlines (A recommended).
- [x] Writer: video.json (English cards, 44 scenes / 64 states, est. 9.0 min) + claims.md + 19 lexicon terms (all null), lint clean; outline recorded as A on the owner's standing word.
- [x] Verifier rounds 1–2 (opus, 5 + 3 fact edits; verify-1.md 50 claims, verify-2.md 47; blog.google 2026-01-22 proves Connected Content Apps predates Oct 16).
- [x] Listener pass (19 lines). Blind reads: round 1 three readers (6/13, 6/13, 8/13) → 16 lines reworded (recaps became named callbacks, step ordinals and group counts dropped, product list cut, two forward hooks added); round 2 two readers (11/13, 9/13) → 5 more lines; final reader recorded with `narrative --answers` (9/13, verdict in `review/narrative.json`). The three standing misses (scene_first, no_spoiler, no_toc) are the teaching-flow §一 five-sentence opening by design (the answer and the promise sentence are in the opening); no_recap is the chapter-7 「my call」 restating the recipe as the one-sentence answer. Left for the owner's final-gate judgement, not reworked further.
- [ ] tts (8:30 on the first synthesis, 2,748 characters), pace (63 states, longest 14.2 s, under the 15 s cap), check-audio round 1: 8 flagged → all reworded (連了→接上去, 推薦→優惠, 片段→摘錄, 兩版都有→新舊兩個版本都在, 連接→Connect 那一步, 點三層→第三層) and re-recorded (8:34); round 2 running; then review-push audio.
- [ ] render, assemble, captions, qa, review-push final.
- [ ] package, review-push publish; note what the owner still has to do.
- [ ] Languages after the owner's tick: i18n-sheet → translate → merge → review → render (locale thumbnails) → dub → check-audio → captions → package → review-push languages.

## How to verify

`node tools/video/cli.mjs status --slug google-ai-search-ads-exception --workdir <home>/mokaair-work/videos`; `lint` zero errors; `qa` writes review/qa.json; the cards appear on /admin/videos.

## Notes

- The Verge cannot be fetched from this machine (host refuses); the site article and Google's pages carry everything needed.
- `KEY_MAX_CHARS` is 24 characters, so English keys are about four short words; the lint length estimate counts a Latin word as two units, a CJK character as one.
- Paper `quote` cards hold three lines of 100px type; longer quotes ran their last line under the source pill (render did not flag it): keep the clause that carries the fact. A one-line `big` with an icon still clipped descenders, so the only bigs that keep an icon are the numeral one and `ad-center`.
- First render: a paper `big` card with an icon and two lines of text runs its second line under the key band and render does not flag it (the exemplars only ever use one line with an icon); fixed by one-lining short texts and dropping the icon on long ones (`_tools/fix-layout.mjs`). `steps`/`compare` cards with a band lose their card title. `**` must not span `
`.
- The channel has no Google account session: account settings pages are described on `steps` cards from the help pages; `screencast` only of the public policy and help pages.
