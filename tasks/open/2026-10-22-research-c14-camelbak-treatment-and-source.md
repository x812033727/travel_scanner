---
id: 2026-10-22-research-c14-camelbak-treatment-and-source
title: Research C14 CamelBak treatment and source matrix
status: in-progress
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-22T16:00:03Z
created_at: 2026-10-22T15:59:10Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14
---

# Research C14 CamelBak treatment and source matrix

## Why

C14 in the approved 20-episode order needs an independently checkable CamelBak treatment before a script. Brand retellings disagree about the race year (1988 versus 1989), while contemporaneous trademark records and later patent text carry their own date scopes. Keep prototype, company founding, product, patent, and distribution distinct; preserve the Curio-style story and its owner gates.

## Definition of done

- [ ] A six-chapter, hook-led Treatment names the exact unresolved dates and scopes.
- [ ] A source matrix uses directly readable brand, SEC, patent and trademark records for every proposed causal claim.
- [ ] An independent reviewer signs PASS or HOLD on fixed file hashes before owner Treatment adoption is requested.

## Steps

- [x] Identify official company history, original patents, SEC 2014 filing and trademark record; separate claims they actually support.
- [x] Draft Treatment and source matrix within the exact C14 folder.
- [ ] Request independent source and story review, then address any HOLD.
- [ ] Present the reviewed Treatment for owner adoption before script writing.

## How to verify

`git diff --check`, SHA-256 of both new files, source URL readback and `npm run check:tasks`. Review receipt must bind those hashes.

## Notes

Company site and 2014 parent 10-K date founding to 1989; a 2017 USPTO opposition record reports a CamelBak first-use claim of 1988-12-16, while a Fawcett patent retrospectively says 1988 for pack-and-bottle combination. Current CamelBak NZ brand history says the race idea arose in 1989; original year should not be stated as settled in narration. The 1990-filed, 1992-granted Fawcett bite-valve patent describes technical operation, but cannot alone prove every early ThermoBak used that exact valve or that founder Michael Eidson invented it. 2014 parent 10-K dates mountain-biker following to early 1990s and bottle-category expansion to 2006. No paid calls are part of this ticket.

2026-10-23: Draft Treatment SHA-256 `32AF5F0744DF5961E3B92FD2D0E33F305C07DCEED5B2F4D33F6E09C28B39E437`; source matrix SHA-256 `E1C9766A4432F56CA84E7EC9886EF5DAB95895DF7B008096E973FD369A1B5B17`. Independent source review and owner adoption pending.
