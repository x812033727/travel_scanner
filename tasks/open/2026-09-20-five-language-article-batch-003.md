---
id: 2026-09-20-five-language-article-batch-003
title: Five-language article batch 003
status: in-progress
priority: P1
area: docs
owner: codex-article-localization
claimed_at: 2026-09-20T08:59:50Z
created_at: 2026-09-20T07:26:10Z
completed_at:
branch: codex/article-localization-batch-003
depends_on: []
scope:
  - apps/api/app/guides/content/japan-hotel-room-plan-guide.json
  - apps/api/app/guides/content/japan-luggage-forwarding-guide.json
  - apps/api/app/guides/content/japan-onsen-ryokan-guide.json
  - apps/api/app/guides/content/japan-restaurant-reservation-etiquette.json
  - apps/api/app/guides/content/japan-station-locker-guide.json
  - apps/web/public/guides/japan-hotel-room-plan-guide
  - apps/web/public/guides/japan-luggage-forwarding-guide
  - apps/web/public/guides/japan-onsen-ryokan-guide
  - apps/web/public/guides/japan-restaurant-reservation-etiquette
  - apps/web/public/guides/japan-station-locker-guide
---

# Five-language article batch 003

## Why

Five published Japan travel guides have only their complete Traditional Chinese
document. English, Japanese, Korean and Simplified Chinese are absent. Each guide
also has an editable SVG with visible Traditional Chinese labels. These five pack
and asset paths do not overlap an active task. The originally considered Bangkok
and Busan guides overlap two existing review tasks, so they are excluded.

## Definition of done

- [ ] Each article has complete, independently reviewed documents in all five locales.
- [ ] Every text-bearing SVG has reviewed localized variants without overflow or missing glyphs.
- [ ] The exact reviewed bundle installs idempotently without changing zh-TW prose.
- [ ] A content PR is merged, deployed, and only the twenty missing locales are published.
- [ ] All twenty public pages pass desktop/mobile content, image, canonical, hreflang and link review.

## Steps

- [x] Claim five non-overlapping paths and capture a fresh read-only production snapshot.
- [x] Translate twenty missing locale documents with strict schema/token checks.
- [x] Render twenty localized SVGs and pass automated bounds/overlap checks.
- [ ] Independently review all translated text, SVG glyphs and raster captions at full size.
- [ ] Assemble, install and validate a hash-bound explicit release bundle.
- [ ] Open/merge the content PR, deploy, dry-run, publish and browser verify.

## How to verify

Run the localization pipeline status and progress report against the pinned
baseline and per-locale review hashes; assemble and install twice to prove
idempotence. Run focused guide content/link tests and required CI checks. At
publication, compare the durable journal with a direct database snapshot and
inspect each new locale on desktop and mobile, including links and metadata.

## Notes

Fresh production snapshot was captured read-only on 2026-09-20 while deployed
repository HEAD remained `6532eaa6e7e9d5a34b94cfe8f8a62ed2e0fba9a1` before
and after. Snapshot SHA-256:
`7194a070c25ee443c32d3f7870320d8323c58421ff5d2b1dd1e433532a417b87`.
The working branch began at `80ad55c6a85b7a5635f9763c5837094aa5dbc513`;
the full combined baseline SHA-256 is
`6717c88cbf7ad46df11628a594d65e9b7f03b75179bcb5b228be28ebd4ab3543`.
The five selected source documents exactly match the published database documents.
All five articles are active/published, each has only zh-TW and lacks exactly
en, ja, ko and zh-CN. The source SVGs are editable. Four covers are disclosed
AI conceptual illustrations, while the onsen guide has three photographs with
their original authors and licenses; all seven rasters have no designed text
overlay. Baseline and work evidence live outside the repository at
`C:\Users\x8120\.codex\article-localization-batch-003`; no article pack or public
asset is changed until review and assembly finish.

Twenty jobs are `rendered`, with GuideDocument/schema and protected-token checks
passed, one 1600x900 SVG each, and no automated SVG bounds/overlap issues.
The progress report has 20 translated, 20 rendered, 0 independently reviewed,
0 assembled, 0 published and 0 browser-verified, with zero article/locale
issues. Pre-review evidence SHA-256:
`bede7c02cde6a26b54efb63fac2ac45066db3820d15624811cc1a857c0be8832`.
It binds twenty document, source, artwork and render hashes and verifies source
credits, source URLs and checked dates. The twenty-eight field-level corrections
are recorded outside the repository with before/after text; their file SHA-256 is
`559bc67e131fedc5b6bf7afef472e4a0b89b795f270f1be5188914afe4aa8cc7`.
Corrections cover three already-Japanese citation titles, Korean word-form
numbers, AI illustration alt text, and narrow SVG labels. The localization
pipeline's 27 Python tests, 17 Node artifact/layout tests, and `check:tasks`
passed. Independent line-by-line editorial and visual sign-off remains pending;
do not assemble or publish from the rendered state alone. Re-export the live
snapshot before assembly because the deployed revision may have advanced.

Four non-onsen articles now have all sixteen target locale documents independently
reviewed, including each localized SVG at full size. The exact four-article
manifest SHA-256 is
`099aec1b983a418f288998840c1548b51c90ab3f8e496c5ba702dac281d8186b`.
Its original four pack hashes still matched the branch and current main; the
twenty pinned bundle assets (sixteen new diagrams plus four unchanged covers)
matched their recorded hashes. The installer completed twice with the same
24-file result; the durable journal SHA-256 is
`1cfc2b50e6fee21d567f0f383385571144dc451a5c13df2a55ce55e6ed9e81ec`.
Reviewed inputs and installation evidence are preserved outside the repository
under `C:\Users\x8120\.codex\article-localization-batch-003`.
`japan-onsen-ryokan-guide` is deliberately excluded pending a separate source
correction, fresh live baseline, regenerated translations and independent review.
Focused content-pack/link tests gave 11 passed and 5 skipped; one existing,
unrelated link test still fails because `taipei-4-day-itinerary` points four
locales to `taiwan-entry-2026-arrival-card` under the `howto` kind although the
target article kind is `intel`. Neither article belongs to this batch. Task
validation and `git diff --check` passed. Installer inputs remain untracked
locally after the native cleanup command was blocked by automatic policy; the
PR contains only the scoped article packs, diagrams and this task record.
