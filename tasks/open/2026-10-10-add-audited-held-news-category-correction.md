---
id: 2026-10-10-add-audited-held-news-category-correction
title: Add audited correction of held news candidate categories
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T06:16:18Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/tests/test_news_automation.py
---

# Add audited correction of held news candidate categories

## Why

Gemini and Manus AI stories inherited `crypto` from the fixed Decrypt feed.
The scanner classifies individual content only for mixed feeds. Existing
candidate actions cannot correct a held candidate's category, while changing
the source affects the whole feed and does not backfill existing candidates.
The resulting crypto framing and financial warnings can obstruct review of
an AI article even after other corrections.

Exact affected candidates are Gemini `31ddc338-8cff-4e5c-b647-38de7c7423a7`
and Manus `0f23dbf9-a6d0-4938-9fbf-825b4e582313`. Both currently lack a guide
and have partial cached drafts. Their latest checked-document fingerprints
differ from the cached zh-TW documents; category correction is not a claim
that those drafts have been fixed or approved.

## Definition of done

- [ ] A permitted editor can correct one explicitly selected unpublished,
  held, partial candidate's category with a genuine actor-attributed audit.
- [ ] The operation verifies the expected old category, candidate state/time,
  evidence hash and absence of active work under a fresh row lock.
- [ ] It preserves hold, retry count, all cache/claims/evidence/history and
  lifetime judge rewrites, with no implicit queue, approval or publication.
- [ ] Subsequent normal review uses the new category without treating old
  crypto assessments as approval of the AI article.

## Steps

- [ ] Add a narrow content.manage schema/service/route for candidate category
  correction with an explicit category, reason and expected prior identity.
- [ ] Reject published candidates, unknown categories, stale source/evidence
  or candidate state, active DB/RQ work and conflicting article ownership.
- [ ] Preserve all original rows and cap counts; record only the legitimate
  category transition and its normal audit.
- [ ] Keep source qualification and later draft ingestion/review independent.

## How to verify

Use focused API tests for a fixed-crypto feed's AI article, stale category or
evidence, concurrent work, an existing capped rewrite history and repeated
requests. Assert the real actor audit, exact preservation of all other state,
and zero queue/publication calls. Verify the selected candidate's persisted
row and audit after a separately bounded production operation.

## Notes

- External root: `C:\Users\x8120\.codex\news-review\20261010-6f71\`.
- Actual selected-25 capture `processed-held25-actual-0563.json`, SHA256
  `985b829eac27cee719cc335d52318c4c224cb9614ad37f7a725f6a0e42e304cb`.
- Bound source/category research
  `gemini-manus-category-source-native-gap-readonly-v1.json`, SHA256
  `11eeb929862a376b107f5e3bd81c4faced07dc6691e419fbdf54de678ed69dac`,
  contains exact candidate/source/assessment pointers and native entry points.
- The cause is fixed feed inheritance in scanner.py, not a claim that BTC
  page noise caused the persisted classification. Pure local classification
  of the stored article bodies returned AI but did not update any data.
- Gemini retains two actual judge rewrites; Manus retains one. Neither
  counter was reset, and no new category or draft was saved at filing.
- Manus has a separate single non-first-party source qualification hold.
  Changing its category cannot satisfy that gate. Do not make Decrypt first
  party or grant whole-feed single-source publication to resolve this case.
- The native global SourcePatch remains a separate source configuration
  decision and cannot substitute for an audited candidate correction.
