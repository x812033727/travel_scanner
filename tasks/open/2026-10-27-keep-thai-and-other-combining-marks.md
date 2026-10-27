---
id: 2026-10-27-keep-thai-and-other-combining-marks
title: Keep Thai and other combining marks in description hashtags (hashtagsFrom drops \p{M})
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-27T16:06:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/metadata.test.mjs
---

# Keep Thai and other combining marks in description hashtags (hashtagsFrom drops \p{M})

## Why

`hashtagsFrom` in `tools/video/core/metadata.mjs` builds the description's hashtags with
`String(tag).replace(/[^\p{L}\p{N}_]/gu, "")`. Thai tone and vowel marks are combining marks
(`\p{M}`), so they are stripped: 「ข่าว AI」 becomes `#ขาวAI` ("white AI") and 「แฮกเกอร์ AI」
becomes `#แฮกเกอรAI`. The same happens to Hindi, Vietnamese decomposed text and any script with
combining marks. Found by the th caption reviewer of `artex-ai-attack-leftover-keys` on 2026-10-27
(confirmed: `hashtagsFrom(['ข่าว AI'])` returns `['#ขาวAI']`).

## Definition of done

- [ ] `hashtagsFrom` keeps combining marks (`[^\p{L}\p{M}\p{N}_]`), and a test covers a Thai tag.
- [ ] Already uploaded th descriptions are listed for the owner if any carry a broken hashtag.

## Steps

- [ ] Change the character class and add the test beside the existing hashtag test.
- [ ] `npm run test:tools`.

## How to verify

`node -e "import('./tools/video/core/metadata.mjs').then(m=>console.log(m.hashtagsFrom(['ข่าว AI'])))"`
prints `[ '#ข่าวAI' ]`.

## Notes

- Not done at filing time: `2026-10-26-97-100-cc-100-blocked` was active on the same file, so the
  claim was refused. For ARTEX the th translator put Latin-only tags first as a workaround.
