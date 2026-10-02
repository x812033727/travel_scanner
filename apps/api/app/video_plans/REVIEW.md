# Independent review: read-only long-form planning catalog

Reviewer: /root/review_longform. Checked source bytes on 2026-10-02T05:49:56.611Z. Reviewed HEAD checkpoint: 73c0a750444f7b26eca747f3482a27ec9dc862de. This report covers the new 24-file admin catalog feature. It does not replace the existing 70-file duration review, rerun factual review, prove generated media, or assert current database import, approval, publication or deployment.

Status: PASS for reviewed source semantics, generator, API contract/authorization, UI code and local desktop/mobile browser acceptance. No live-production, imported-data or media acceptance is claimed.

## Findings and resolved fixes

The five counts remain 100 / 92 / 100 / 100 / 81 (473 total). All reviewed source bindings match current raw bytes; the 24 reviewed feature files remain unchanged after integrating main. The current 70 duration files match the newer inherited upstream receipt; nine of those bindings were updated upstream. Season two displays production_title, including the corrected B28 Saks angle; eight rejected duplicates are excluded. Third-season records remain checked candidates with no invented outline package. Brand story titles, six chapter points, claims/source attribution, caveats, images, proposed publishing order, plus original subject/category/region/sensitivity/related_guide/number/source.kind/cast.id/core flags are preserved. In particular, 23 care flags and 19 related articles remain visible in authored details. AI titles use zh term names while article_title is explicitly labelled as the source article title. 77 backlog, three planned terms and the single covered ai-agent keep their original stages; all three existing-video references and the no-remake note survive.

I identified missing brand metadata and a stale search draft when navigating back to an earlier URL query. Both were fixed and reread: sourceText now renders the original fields; keyed PlanSearch resets draft text on URL-query changes. I also verified the completed covered-row fix: no production target is displayed for COVERED_DO_NOT_REMAKE. New browser assertions explicitly require all three references and zero 10-minute target on that row.

## Implementation review

The deterministic generator confines reads to bound docs/videos paths, checks every source/file/record/package hash and reproduces effective ten-minute season-one/two inputs and six chapter budgets totaling 600 seconds. It refuses drift, traversal and escaping symlinks. Only its explicit build operation writes the new packaged JSON; the check command is read-only. Candidate and other catalogs receive no fabricated backend input.

The API image copies app/video_plans/data/catalog.json; runtime reads this fixed data path with a 16 MiB cap and strict typed validation. The registered endpoint requires content.read, matching the existing videos admin navigation capability. It has only GET, with no import service, provider request, database business write or queue enqueue. Independent API review verifies 401/403 authorization failures, 422 invalid filters/pagination and 405 mutation methods, exact counts, typed detail labels and covered references. A bad bundle fails 503 instead of reusing stale data. Standard authentication/session behavior is inherited; this is a no-business-write planning view.

The frontend uses the existing same-origin /api/travel BFF and retains locale/unrelated query parameters. Catalog, search and page are URL-backed; narrowing resets the page, out-of-range pages normalize, aborts prevent stale filtered responses and errors provide a read retry. Plan articles and long source strings use min-w-0/wrapping; existing Tabs supplies desktop keyboard tabs and the mobile select. All five copy catalogs have aligned keys and interpolation parameters. Original authored prose is retained rather than automatically translated; these new lib copy catalogs are not database-overridable text namespaces.

The bundle is 7,897,635 bytes. Actual Python API JSON serialization over all unfiltered/catalog-filtered pages gives maxima 986,846 bytes at 25 items and 3,226,105 bytes at 100 items, below the existing 10,485,760-byte BFF response cap. The 16 MiB bundle cap is a separate runtime-file limit.

## Verification and boundary

Independent generator tests: 13/13 PASS; reproducibility CLI: all 473 PASS; existing duration CLI: all 473 PASS; scoped frontend tests (plans, copy, existing Shorts tabs): 24/24 PASS. Independent delegated final targeted API/i18n tests: 63/63 PASS (50 video_plans, 10 i18n, 3 error-localization guards), plus actual ASGI response/GET-only probes. The earlier 42-case result is historical. Original 308 source/policy bindings still match. All current 70 duration files match the inherited updated receipt, whose raw report hash also matches; this is mechanical receipt validation. CI adds the dedicated desktop/mobile Playwright spec, and the spec uses actual packaged entries with local-only GET/HEAD/OPTIONS traffic, checks reload/filter state, count/targets/stages, three covered references, no covered target, browser errors and horizontal overflow.

Full-suite and production acceptance remain the parent's separate gates. The earlier full API run exposed missing localization coverage; this report validates its fix with targeted tests and does not label a full API rerun green.

Evidence: 20261002-admin-long-form-plans-independent-review.json. API delegated evidence: 20261002-admin-catalog-api-probe.json; final SHA256 a6b3a969bef10833cc2255a6c029c72000c217b94e635850c6cf4f6e1b6fc786. Targeted log SHA256 3e0f80d2aa7ff0df0145460b3f8b2802e6719b599156684a14e105f9cf1f8c53.

## Final incremental review: browser, locale errors and operational README

I actually viewed all four saved PNGs using view_image at original resolution. Desktop filters stay in one row; mobile filters and clear action reflow within the screen. The corrected B28 title and ten-minute target are readable, and the covered AI Agent article shows its reference-only stage with no production target. Expanded source sections remain readable. These are scrolled viewport screenshots: they do not independently capture every below-fold claim or top-level tab, which are covered by the browser assertions and source review.

The final build browser log records 4/4 PASS, two cases in each of desktop-chromium and mobile-chromium. Its automatic guards passed for local-only traffic, no writes, no first-party failures/browser errors and no horizontal overflow. The test uses packaged catalog data served through local browser fixtures: it validates UI behavior, not a live production deployment or database import.

I reviewed the added README against implementation: authorized source regeneration commands, image packaging, content.read, fixed data path, no import/apply needed for visibility, 503 fail-closed behavior, title/ID/slug search, pagination and 600/780 targets are accurate. The locale increment adds only video_plans_unavailable to four non-zh-TW ERROR_DETAILS maps; the original zh-TW raw detail path is unchanged. Runtime old-HEAD/current map comparison confirms zero removed or overwritten messages across all five locales. Five new ASGI cases check specific non-generic 503 text in every locale. The API test file is the only changed path from the original 22-file review; other 21 source hashes remain identical. Existing schema guards were reread and retained; they are not new schema edits in this increment.

| Viewed screenshot | Pixel size | SHA256 |
| --- | --- | --- |
| 20261002-admin-catalog-browser/admin-video-plans-all-473--80fc4--and-catalog-survive-reload-desktop-chromium/long-form-plans.png | 1280 x 720 | 59419e90af83f263f704f3f0d3c3dbf1cb250b32f58932140474a3cfbc726170 |
| 20261002-admin-catalog-browser/admin-video-plans-all-473--80fc4--and-catalog-survive-reload-mobile-chromium/long-form-plans.png | 1082 x 2202 | 6e95d85614d9423bf9ba4d2d499c9a4016bfb5f2fb9baaab7027c6ab17d75d17 |
| 20261002-admin-catalog-browser/admin-video-plans-candidat-d4a2d-retain-the-13-minute-target-desktop-chromium/long-form-plans.png | 1280 x 720 | 9b21a814de08b3740ac31fb82acf621f0a7c823d73998c53e1be1042f0d1d3f7 |
| 20261002-admin-catalog-browser/admin-video-plans-candidat-d4a2d-retain-the-13-minute-target-mobile-chromium/long-form-plans.png | 1082 x 2202 | febafde5860049f1636e6e33f14b687fd293e768691821f298efc18c049cca50 |

Browser log SHA256: 2ebe851a7a4557e17315c099644975b5c7b5c1795a451cc5e46a0e7456aa525f. Last-run state SHA256: 91d1c43004802cd49950d78eb11c8fa7d05da8ffffe219a8b13b2f561bc00903. Final build log SHA256: 6b26fb6870f2e24d6dc7efe0bc9dcce8791867e9670712a6c65e8f9410cc36f5. Original scoped report and JSON evidence are preserved as before-browser history artifacts.

## Integration with main 73c0a7504

Integrated HEAD and observed origin/main are 73c0a750444f7b26eca747f3482a27ec9dc862de, following anime category PR #1110 and language-thumbnail worker PR #1112. All 24 feature file SHA256 values below remain identical to the prior independently reviewed/browser-tested snapshot; the catalog bundle, plans SHA and 308 original source/policy bindings also remain unchanged.

I independently reran the 13 catalog tests plus two current-duration-receipt tests: 15/15 PASS, exit 0. The admin-catalog reproducibility check and existing duration CLI each passed all 473 records, exit 0. Current duration receipt validation covers 70 files with zero byte mismatches and exact raw report SHA c33b7aed0cec2c3d8c792217eaca07b202781ab120c9dca6d7a37f12cda4b0d7; receipt SHA is 5b22b33c1291aa3f2f358b5f508cf37d2bc70500f98923cd0ab42367be62693c. The inherited receipt identifies author claude-opus-5-5-worker-thumbs and reviewer claude-pr-review-1112, with DURATION_ONLY/PASS. Compared with the earlier b11e01eb checkpoint, nine bindings changed upstream:

- apps/web/components/admin-video-reviews.test.tsx
- apps/web/messages/en/admin.json
- apps/web/messages/ja/admin.json
- apps/web/messages/ko/admin.json
- apps/web/messages/zh-CN/admin.json
- apps/web/messages/zh-TW/admin.json
- tools/video/automation/automation.test.mjs
- tools/video/automation/flow.mjs
- tools/video/core/schema.mjs

This confirms the current inherited receipt is internally consistent; it does not claim I independently rereviewed every new upstream worker behavior. No duration implementation, source catalog, duration report or receipt was edited by this feature review. Independent API increment review confirms User/auth/content.read are unchanged, PlanCatalog remains separate from VideoCategory.anime, and migration 0119's video_projects constraint and language worker changes do not add a database import, business write or job path to the packaged catalog GET.

Broader validation history supplied by the parent is preserved accurately: the full web run had 3749 passes and two timing failures, followed by two passing runs of the affected 18-case group; remaining investigation is recorded in tasks/open/2026-10-02-investigate-loading-query-timeouts-under-windows.md. The original full API run had one missing-translation coverage failure; the parent validated its fix with 53 targeted passes and the independent API/i18n review with 63 targeted passes. These focused results are not a claim of a successful full API or full web rerun. Existing four-case local browser acceptance and its frozen screenshots/logs remain valid because all 24 feature bytes are unchanged. Final PR CI and production acceptance remain separate gates.

The prior genuine report (SHA b948ad557b92752ac4c21f51aeb00d76fa9b039e88ba5d7ec3c52b4bea7349b7) and its JSON evidence are preserved as before-main73 artifacts.

## Reviewed working-byte SHA256 (24 files)

| File | SHA256 |
| --- | --- |
| .github/workflows/ci.yml | e56ab22e6275613e932fdedaa32aeac9ae6f3d8f2ef73c4f27515605594939af |
| apps/api/app/i18n.py | aac1d6feb5d06d7caf4b2568a60807922ac8d2c366439a691382af03d6e54002 |
| apps/api/app/main.py | 224ece58a7dfb10735480a10d0cbdc992506b03cd361a2c63a6e650808b521c6 |
| apps/api/app/video_plans/README.md | 63d08bc573a6c3b2c2d0fd01866ec7725c1f0d632215c14444c7036309f56506 |
| apps/api/app/video_plans/__init__.py | 12c89ecdd40954c7566ffc3d12799c9528033c966ffdd3ecb29503cd16bbfdc5 |
| apps/api/app/video_plans/catalog.py | 2608712000de9684eb1e06fcc3410bdbd76ef611a724b83868c5cdfc6ea471de |
| apps/api/app/video_plans/data/catalog.json | f3ca37c80345e1542a85cb5caba926ed45073fbda21845a7b8d2b521b14e2da9 |
| apps/api/app/video_plans/router.py | 9d6223a978fb510b5920a0afee0882c289c3fb132eca2a791e1db55e7aff315b |
| apps/api/app/video_plans/schemas.py | db00e092be1c07613154384f2b2cb1040dc27f4e3d495298f2353dec9cb18d2c |
| apps/api/tests/test_video_plans.py | 182dc5ce8d4f76f46ca03268aead5130d39910377c7258ef8f99725cf80a88b8 |
| apps/web/components/admin-video-plans.test.tsx | b7cb41a2f6b8d33363a998b0da33230ca81a40389300c0d6660009c4d8784a74 |
| apps/web/components/admin-video-plans.tsx | b0df02688fcd5db746f90dcff5136b59f06e4983a2d3f67ff3d0ec01ac944eb4 |
| apps/web/components/admin-video-reviews.tsx | 531e8592fc89fdf3aaaa6686a6f7aad270a4db6acbf91fd34bb5762c6ffb6dff |
| apps/web/components/admin-video-shorts.test.tsx | a031686cb8d2411d3b6e7d90982faccc2d8e97f4da16edd321520a49c082f60f |
| apps/web/e2e/admin-video-plans.spec.ts | c9b103a4959c6f3d9262a2bfe6f49b0688dfb6645f214c3ab3cd7199d348e679 |
| apps/web/lib/video-plans-copy.test.ts | c98f2043067a27d9ed9f904004c6af412ecafc56bb7f76daab6b1642a21bb6a7 |
| apps/web/lib/video-plans-copy.ts | 50cbe7900cc2cf00647c2c6e36f248de941d4f8f9eb8e18996567096b2e3065e |
| apps/web/lib/video-plans-messages/en.json | d80ee52baa3c586df5a372a5f616ee0867b2321738e75ac7abe1a2249781a05d |
| apps/web/lib/video-plans-messages/ja.json | ae6ae1ee52cd81a8a40d145a8a6deef7d5c1b924b5686937b972d850f43f047d |
| apps/web/lib/video-plans-messages/ko.json | f96e3230e999028a96194469787471f67e06d03d15b1b60e068292d42f6a67ad |
| apps/web/lib/video-plans-messages/zh-CN.json | 0172207c765168f6251d768561f503721f71f1fbc4bea8ccfad04150001deb3f |
| apps/web/lib/video-plans-messages/zh-TW.json | 71131149f7dd241fce9834c4c0b5207ddec485bdf135efb60ba6cf5f27dd0384 |
| tools/video/long-form/admin-catalog.mjs | 274e80a807f637b16c444574153931e532c2e46ee0ca07ca55fa774be0038553 |
| tools/video/long-form/admin-catalog.test.mjs | 4236cc25444516e09b5a9a2f5798eed946302befe2a016b4e9311ca89f9206bf |
