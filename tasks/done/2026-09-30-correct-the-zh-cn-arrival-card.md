---
id: 2026-09-30-correct-the-zh-cn-arrival-card
title: Correct the zh-CN arrival-card guide's outdated 47-city mainland tourism claim
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T09:46:12Z
created_at: 2026-09-30T01:29:06Z
completed_at: 2026-09-30T09:51:42Z
branch: claude/arrival-card-zhcn
depends_on:
  - 2026-09-21-91-ci
scope:
  - apps/api/app/guides/content/taiwan-entry-2026-arrival-card.json
---

# Correct the zh-CN arrival-card guide's outdated 47-city mainland tourism claim

## Why

`taiwan-entry-2026-arrival-card` zh-CN block 2 still says mainland individual
tourism is limited to residents of 47 designated cities with 15-day stays. The
zh-TW source says the current eligibility depends on residence, status and the
open category, and explicitly warns not to use the old "47 cities" description.
Found while fixing the content checker in `2026-09-21-91-ci`, which only added
the other nationalities' visa-free days to this block.

## Definition of done

- [x] zh-CN block 2 and the block 3 table match the zh-TW wording on mainland
      and Hong Kong/Macau entry, checked against the NIA page on the day of the edit.
- [x] Independent review; lint 0 errors; after deploy, import and publish zh-CN only.

## How to verify

Read zh-TW block 2 next to zh-CN blocks 2-3; no "47" city claim remains.

## Notes

- 2026-09-30 (claude-opus-5-5): re-read the NIA pages. The individual-tourism
  notice (36078) is dated 2022-05-17 and still lists 47 cities and 15 days, but it
  is a procedure page and says nothing about whether the category is open now;
  the category page and the living-abroad/HK-Macau notices (36084, 146295) and
  the HK-Macau permit notice (30159) are also live. zh-CN now follows the zh-TW
  wording: eligibility depends on residence, status and the currently open
  category, and the old "47 cities" description is not a current eligibility
  test. Changed: description, block 2 (mainland and HK-Macau paragraphs; the
  Singapore/Malaysia and other-nationality lines kept), block 3 rows 1–2 and
  caption. Sources: dropped 36078 and the HK-Macau Q&A (no longer relied on),
  added the NIA category page, updated 36084 and 30159 to 2026-09-30.
- "網簽" still appears in blocks 4 and 6 as a permit type in the TWAC and
  e-Gate context, which is correct. Lint 0 errors; content pack tests green.
  Production import of zh-CN after merge and deploy.
