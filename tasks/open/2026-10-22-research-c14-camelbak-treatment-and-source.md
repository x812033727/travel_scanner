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
  - docs/videos/story-everyday-camelbak-c14/treatment.md
  - docs/videos/story-everyday-camelbak-c14/source-matrix.md
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

Draft PR: https://github.com/x812033727/travel_scanner/pull/1695 (review and owner gates pending).

2026-10-23: First independent review at PR head `fb7806301` held M11's implied post-ThermoBak valve sequence and the proposed nine-minute chapter density. Revised the valve to a parallel engineering thread and added the 2006 bottle category and 2014 product/channel/gross-sales mix from the SEC 10-K as later-phase evidence. New Treatment SHA-256 `DDEF7ECB1CE58CB6E32A227CAFC1EC0B5A5A1AA6241DBBBAB2E9312A0FE5D70D`; matrix SHA-256 `557B31C3FD8A7192E7B276BC90A6BAA0C0D9A6B98E8AD24F713C11BB8C6B076F`. Fresh independent delta and owner adoption pending; no script or paid work.

The independent delta reviewer caught two wording inferences before signing that revision: “重新做起水瓶” implied an earlier CamelBak bottle product, and the 2014 SEC channel list did not assign specific channels to bottle entry. Narrowed both, added three withheld cold-open moments, and clarified 8:15 planned spoken time within the 8:20 timeline. Current Treatment SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E`; matrix SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E`. Awaiting fresh review of these exact files.
