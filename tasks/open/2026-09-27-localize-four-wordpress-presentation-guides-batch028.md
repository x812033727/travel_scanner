---
id: 2026-09-27-localize-four-wordpress-presentation-guides-batch028
title: Localize four WordPress presentation guides batch028
status: review
priority: P2
area: api
owner: codex-batch028
claimed_at: 2026-09-27T08:24:29Z
created_at: 2026-09-27T08:24:22Z
completed_at:
branch: codex/article-localization-batch028-wordpress-design
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-theme-selection.json
  - apps/api/app/guides/content/wordpress-page-builder-choice.json
  - apps/api/app/guides/content/wordpress-fonts-self-hosting.json
  - apps/api/app/guides/content/wordpress-table-of-contents.json
  - apps/web/public/guides/wordpress-theme-selection
  - apps/web/public/guides/wordpress-page-builder-choice
  - apps/web/public/guides/wordpress-fonts-self-hosting
  - apps/web/public/guides/wordpress-table-of-contents
---

# Localize four WordPress presentation guides batch028

## Why

The four published WordPress presentation guides currently have only zh-TW content. Readers selecting en, ja, ko, or zh-CN cannot read the corresponding full guides or localized diagram text. This task prepares the missing content and image variants as a reviewable repository batch; live publication is a separate release task.

## Definition of done

- [x] `wordpress-theme-selection`, `wordpress-page-builder-choice`, `wordpress-fonts-self-hosting`, and `wordpress-table-of-contents` each have complete en, ja, ko, and zh-CN documents and localized text-bearing image variants (16 documents, 48 image files).
- [x] Titles, summaries, headings, body, tables, cautions, links, captions, alt text, and source titles retain the full source meaning; numbers, dates, URLs, code, eligibility, and product names remain accurate.
- [x] Published zh-TW documents and original assets are byte-preserved; categories, ordering, and visibility are unchanged. Internal links are language-correct and only clickable when the destination is published.
- [x] Independent language, structural, source-version, link, and rendered-image review passes; relevant pack, frontend, API, task, i18n, lint, type, and build checks pass before a content PR.

## Steps

- [x] Claim exact-path scope and verify the full live source against the current repository pack and assets.
- [x] Translate and render the four guides in batches no larger than 20 articles.
- [x] Independently review every language document and image, repair findings, and save a hash-bound receipt.
- [x] Create a content PR from the latest main and keep the production release gated on merge and fresh evidence.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug <slug>` for each guide from `apps/api`; run `npm run check:i18n`, `npm run check:tasks`, `npm run lint:web`, `npm run typecheck:web`, `npm run test:tools`, `npm run test:web`, and `npm run build:web` where touched. Run API ruff, mypy, and focused guide tests. Compare each target document and rendered diagram against the frozen source and inspect links. A production release uses a separate guarded dry run and public QA.

## Notes

Fresh read-only REPEATABLE READ production snapshot at 2026-09-27T08:26:16Z: host checkout `243b0f2f84359456ebf68c6f0b450d9ef19c344f`; each article published, active, unexpired, article v2 with zh-TW published v4. Full live zh-TW documents match main `d6a35d9e1d515716941ee92396baabd254e68e69`; target locale rows are absent. Snapshot SHA-256 `189b8d42d57146b1ed4605bdaf23dd7e01284f338b755a49f98071d567c13629`; comparison receipt SHA-256 `4aa72919f84eedc72986018441f54abc43042f02550430baa9938a51cc5d51b9` in `C:\Users\x8120\.codex\article-localization-release\next-queue-20260927\fresh-live`. Recheck versions immediately before any eventual release.

Some source article links point to `wordpress-themes-plugins-install` and `wordpress-widgets-sidebar` in Batch027. Preserve those as conditional article links; publish Batch027's target locales before Batch028 where possible, and verify unavailable destinations are never clickable. Source text explicitly addresses Taiwan readers, which remains the audience in every translated locale.

2026-09-27 content handoff: Pair A author receipt SHA-256 `aebd871cf54ba6be37454381e62a84c6de65eedf4606ccc207bac511e6f42c20`; Pair B author receipt SHA-256 `351b0ac7150932c7bd16382fe2db9e9a30de0f47f4a47d4be72091b79926e992`. Reciprocal review receipts SHA-256 `53776bfd33c081f0d951d0b148cda5b2ddc5bbfcab7198fffa18264f44c1bd35` (Pair A reviewed by B) and `040e80f4b9580ab068647a87e0d4d177254dce7a7adaab3a859226b497246a5c` (Pair B reviewed by A) both PASS after simplifying regional zh-CN wording and avoiding an over-specific Japanese 404 claim. Independent 52-path integration review SHA-256 `452687b92ca30f2456f58adb219b9f29470371247bca129d91aa359795abcfe6` passed source/metadata preservation, 16 full documents, 48 images, 32 conditional links and rendered visual checks. Staged-Git blob review SHA-256 `2a7682e3b6879d3e2b283475b44c01101db88a1db9edb424fa32b4c7569fdef1` found 32 exact content bytes and 20 CRLF-to-LF-only text normalizations. Six numeric differences were reviewed as equivalent Han-word-to-digit renderings. Root structural verifier, four focused pack lints, `check:i18n`, `check:tasks`, API ruff/mypy, frontend lint/typecheck and production build all passed. Focused API tests: 208 passed, 122 skipped where Windows lacks isolated PostgreSQL; full web tests: 316 files and 3,402 tests passed. `test:tools` passed 411 with one skip on a rerun using an isolated Windows temp directory after an unrelated first-run `EPERM` rename failure in a video automation test. No production write yet.

Content PR #852 opened from reviewed content commit `a58cb22d859d11c8f58ce1d05828de95341476ce` on main `e97172c297f537170f19fbe6e4813c505a22893a`; CI is pending and squash auto-merge is configured. A task-status-only follow-up commit leaves the 52 reviewed content blobs unchanged. Rebase receipt SHA-256 `c4cb25eb2c8e854f82fbcc25422c2901cef23972a074dbf57677bc2e84dea1c5` proves the initial 52 content blobs remained identical after rebasing. The task is in review; merging the PR will not publish any database locale rows.
