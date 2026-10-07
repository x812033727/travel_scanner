---
id: 2026-10-07-article-missing-locales-completion
title: Complete all missing published travel and life article locales
status: in-progress
priority: P1
area: ops
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T07:17:24Z
created_at: 2026-10-07T04:49:38Z
completed_at:
branch: codex/article-locales-wave3-20261007
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

### 2026-10-07 authoring checkpoint and owner gate

First content PR #1365 is a draft at exact head
`3812fe2c9ae8c58d1eb0373d22529e76a27349c7`; all 21 check runs completed with
success, including full-stack smoke and release safety. It contains 13 articles /
52 independently reviewed target documents. No merge or deployment was performed.

The next content cohort contains Japan refund source correction + four missing
languages and four business-analysis articles / sixteen existing unpublished
targets: 5 articles / 20 independently reviewed targets. All five packs passed
scoped lint; the official refund install/replay was byte-identical. Publication
has separate refund and business-analysis release tickets. The fixed first13
cohort and its reviewed candidate were not expanded.

Cumulative local review readiness is 18 articles / 72 target documents. This is
not live publication. The latest full production inventory remains the retained
04:45 UTC snapshot: 862 incomplete eligible articles / 3,448 missing public
language documents. Completed production publications in this program: zero.
The full 862-article external queue preserves original pins, reviews, source
holds, attempts and the remaining work; source corrections and already active
scopes must not be blindly translated or overwritten.

The owner has been asked to choose whether to merge/deploy PR #1365, merge only,
or retain the draft. Until a choice arrives, keep production unchanged. Release
this coverage-only claim while waiting; resume by reclaiming it and reading the
persistent program state, exact current PR heads and fresh production guards.
This overall task stays open until a fresh production count is zero.

### Continued preparation after owner follow-up

The owner requested continuation. Reclaimed this coverage-only task on
`codex/article-locales-wave3-20261007`, starting from the exact second content
head. Both draft PRs now have all21 successful checks at their unchanged heads.
No merge/deploy/publication choice was selected; preparation continues within
the authorized translation/review scope while those concrete choices remain
pending.

Twelve existing life packs / 48 targets are undergoing current source, ownership
and full independent text/image review. Separate six-pack content tasks will
own any resulting corrections. Hong Kong entry and Taiwan holiday sources are
being rechecked in parallel before new travel jobs. The original862-article
queue and latest production gap counts are unchanged; preparation is not
publication and this overall task is not done.

Continuation checkpoint: the12 life/48 target final independent reviews are now
aggregated verbatim (reviewSHA adbd51543953e233f37f32f3da5090037b998ecff963090bd14425677ad1aeb3;
evidenceSHA4a2f4883988c3f93c4c33abff7cf1b2110666f8c5c10d35f26679898af451f3b).
Official prospective compile is pending, so the prior18/72 completed local
readiness checkpoint remains unchanged. Taiwan/HK8 new targets remain under
final review;15 genuine Taiwan findings have been applied and rerendered with
original/failing artifacts preserved. Wave4 read-only audits filed explicit
Japan source-correction and Sapporo-route follow-ups without expanding wave3.
Global original production deficit3448 and completed_publications=[] remain
unchanged; no production content write, merge or deployment occurred.
