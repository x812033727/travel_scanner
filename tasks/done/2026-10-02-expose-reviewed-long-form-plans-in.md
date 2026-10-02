---
id: 2026-10-02-expose-reviewed-long-form-plans-in
title: Show the long-form planning catalog in video admin
status: done
priority: P2
area: tools
owner: codex-admin-plans
claimed_at: 2026-10-02T04:39:25Z
created_at: 2026-10-02T01:43:32Z
completed_at: 2026-10-02T05:52:16Z
branch: codex/admin-long-form-plans
depends_on: []
scope:
  - apps/api/app/video_plans
  - apps/api/app/main.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_video_plans.py
  - tools/video/long-form/admin-catalog.mjs
  - tools/video/long-form/admin-catalog.test.mjs
  - apps/web/components/admin-video-plans.tsx
  - apps/web/components/admin-video-plans.test.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/lib/video-plans-copy.ts
  - apps/web/lib/video-plans-copy.test.ts
  - apps/web/lib/video-plans-messages
  - apps/web/e2e/admin-video-plans.spec.ts
  - .github/workflows/ci.yml
---

# Show the long-form planning catalog in video admin

## Why

After redeploying, the owner expected the authored knowledge and small-story plans to appear in the video admin. The latest 2026-10-02 read-only audit found production a775b7535e0c9bd5dac443feb69a23a69e251889, API 0118_video_min_8_minutes. PR #1098 had merged as 6d60a1ef and the plan/disposition files were present on the host, but the existing admin only displayed database production records.

Exact matching against all 473 local plan slugs found zero matching video_projects, video_drama_requests or video_drama_episodes in every catalog; there were no related catalog/story series either. Deployment copies code/files, while admin reads database rows. No pending-review import was delivered for this batch. Existing brand story --apply creates active/ready production work, so it cannot be used blindly to make plans visible.

## Definition of done

- [x] A reproducible source-bound catalog includes all 473 long-form plans and original titles, with source stages and covered AI references preserved.
- [x] A read-only API with content.read authorization serves the catalog packaged inside the API image. It cannot create database rows or enqueue generation.
- [x] The video admin includes a URL-persistent Plans tab with search, catalog filters, plan details, eight-minute minimum and original 10/13-minute targets in all five locales.
- [x] The screen distinguishes textual planning stages from production, import, approval and publication; no historical planning flags are presented as live database state.
- [x] Unit and browser tests verify counts, filtering, authorization and GET-only viewing. Independently review source fidelity and rendering before opening a draft PR.

## Steps

- [x] Recheck deployed revision, matching rows, merged PRs and scope collisions.
- [x] Build and check the reproducible API catalog against the current source plans.
- [x] Implement the authorized read-only API and five-locale admin view.
- [x] Run focused/full relevant checks, independent review and browser acceptance; close this ticket in the same PR.

## How to verify

Run the catalog generator check against current source bytes, API authorization/filter tests and ruff/mypy, frontend lint/typecheck/i18n/tests, tools/tasks checks and the dedicated Playwright spec. Browser acceptance must show 473 plans and preserve filters after reload without issuing any mutation requests. Deployment will expose the packaged catalog without a database import; production generation and publication remain separate owner-controlled workflows.

## Notes

Audit catalog counts: season1 100, season2 92 adopted, season3 100 checked candidates, brand-stories 100, ai-terms 81 including one covered reference. All three matching row counts were zero per catalog at the audit; these counts are historical evidence, not current production state.

Initial audit history: before that redeploy, production ba4dc160 / 0117 did not contain the final plans, and PR #1098 was still open. The subsequent deployment resolved file availability, but not the missing display surface. This implementation adds /zh-TW/admin/videos?tab=plans without a database import.

tools/video/long-form/admin-catalog.mjs build writes only the new packaged API catalog; check enforces exact reproduction and all 308 source/policy bindings. The catalog preserves 192 outline plans, 100 third-season candidates, 100 story plans, 80 term plans and one covered reference. Second-season production titles replace historical original angles; eight rejected duplicate topics stay excluded. Original brand sensitivity/related-guide/attribution/caveats remain visible. Covered ai-agent retains its three existing-video references and the UI hides a new production target for it.

GET /api/v1/admin/video-plans requires content.read. The runtime reads its immutable image file, has no business database dependency, mutation route, provider request or queue side effect, and refuses invalid data with a localized 503. Existing production workflows and mutable worker directories are not used by this view.

Final catalog SHA256 f3ca37c80345e1542a85cb5caba926ed45073fbda21845a7b8d2b521b14e2da9 (7,897,635 bytes). Default 25-item and maximum 100-item API responses were measured below the existing BFF cap (maxima 986,846 / 3,226,105 bytes versus 10 MiB). No production mutation, import, media generation, approval or publication occurred in this task.

Independent reviewer /root/review_longform: PASS_SCOPED_SOURCE_API_UI_LOCAL_BROWSER, final 24-file report SHA 165659e51f67e6c1e8a0617878abd606e3117052514b5112dad3ddab75e1f396, copied unchanged into apps/api/app/video_plans/REVIEW.md. Integrated main checkpoint 73c0a750444f7b26eca747f3482a27ec9dc862de preserves all 24 feature and 308 source/policy hashes. Nine duration bindings changed upstream; the current 70 files match the inherited updated receipt and its report hash. The reviewer independently reran 15 generator/receipt tests and both 473-record CLI checks. The reviewer actually inspected four desktop/mobile screenshots; synthetic local acceptance is not a production-site acceptance.

Validation: 13 generator tests; 24 focused frontend tests, extended to 55/55 including existing review-panel coverage after integrating main 73c0a7504; 53 API/localization regressions (independent broader API increment 63); web lint, TypeScript/build and 5-locale i18n checks; 4 Playwright cases across desktop/mobile; tools 1168 passed / 2 existing platform skips. Full API exercised 5583 passing / 428 skipped cases with one missing-error-translation failure, corrected and explicitly rechecked with the 53-test focused run. Full frontend returned 3749 pass / 2 failures in unchanged account-panel and itinerary-place-browser loading queries; both full files passed unchanged twice afterward (18/18). These observed load-related failures remain recorded, without relabelling the full run as passing, in follow-up 2026-10-02-investigate-loading-query-timeouts-under-windows. CI at the eventual PR head is separate evidence.

Final post-main API run: uv run pytest tests/test_error_localization.py tests/test_video_plans.py -q, 53 passed in 30.50s, exit 0; log 20261002-admin-catalog-api-post-main-focused.log SHA 3a1b2979827170ddeb278245f7f4b684d50fd105b1c2da6f5981fda8767225c8. Final task validation: 1284 valid, exit 0. All 24 reviewed staged Git blobs match the independent report's raw SHA256 bytes.
