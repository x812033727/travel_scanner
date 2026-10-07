---
id: 2026-10-07-article-missing-locales-completion
title: Complete all missing published travel and life article locales
status: in-progress
priority: P1
area: ops
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T04:49:40Z
created_at: 2026-10-07T04:49:38Z
completed_at:
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - docs/article-localization/coverage-20261007.md
---

# Complete all missing published travel and life article locales

## Why

The owner requested every missing language for the published travel-information,
travel-guide and life-sharing articles. The 2026-10-07 read-only production
snapshot has 862 incomplete public articles and 3,448 missing public documents
(en, ja, ko and zh-CN). Existing translations must be reused rather than rewritten.

## Definition of done

- [ ] Every eligible public article in intel, howto and life has all five public languages.
- [ ] Source text, existing published translations and original images remain preserved.
- [ ] New text and image text have independent hash-bound reviews.
- [ ] Every released wave has guarded publication and public desktop/mobile verification.
- [ ] A fresh production inventory confirms zero missing eligible language documents.

## Steps

- [x] Audit production, repository, old translation work and concurrent task scopes.
- [x] Export a fresh full production snapshot and build a pinned repository-backed baseline.
- [x] Identify 116 existing unpublished locale documents in 29 life article packs.
- [x] Independently review, compile and rehearse the first reusable 2-article/8-locale wave.
- [ ] Translate and review travel articles, then remaining life articles, in waves of at most 20.
- [ ] Open narrow content/release tickets for each wave; merge, deploy and publish with receipts.
- [ ] Refresh production coverage after every release and close only after all eligible gaps are filled.

## How to verify

Use the full `export_snapshot.py` result and effective article visibility to count
published locale gaps. Run the official localization bundle guards, content lint
and applicable CI checks for every wave. Bind independent reviews to document,
asset and artifact hashes. Verify each released locale through public APIs and
the browser, including body, images, canonical, hreflang, links and mobile layout.

## Notes

- Snapshot captured 2026-10-07T04:45:46.904711+00:00. Eligible public cohort: 1,246 articles.
- intel: 21 incomplete articles / 84 locales; howto: 108 / 432; life: 733 / 2,932.
- Missing locales are en, ja, ko and zh-CN for every incomplete article. No missing
  target has a database draft. 116 target documents already exist in repository packs.
- All 96 database-only articles in this cohort already have five public languages;
  the original full export is retained, and the official builder is scoped to
  repository-backed records without excluding any missing target.
- Baseline includes 251 repository/database document differences. Database
  published documents remain authoritative; inspect each affected wave before translation.
- First exact reusable wave: marketing-mix-models and brand-tone-vibe-marketing.
  Current full review and corrections completed; the compiled prospective candidate
  passed 13 isolated same-deployed-image rehearsal cases. Final within-cohort
  related-reading labels were then corrected before the expanded content freeze.
- The fixed first content cohort contains 13 articles / 52 target documents.
  Singapore entry and powerbank final review passed before the Git freeze.
  All 13 packs lint with zero errors after the last two official installs.
  Inherited summary/length advisories remain.
- Release ticket 2026-10-07-release-localized-travel-life-wave-20261007 owns only
  publication evidence. Deployment/publication still require concrete approvals.
- All snapshots, model jobs, logs, review inputs and queue state live in the
  owner's persistent external work directory. Do not commit raw production data.
- Existing active batch-8 and Korea/source-correction scopes, unpublished hubs,
  private/expired articles and publish_holds remain excluded from automatic work.
- This program ticket owns coverage documentation only. Claim separate narrow
  content and release tickets before changing article packs, images or release records.
- No new translation or publication is claimed complete by this inventory.
