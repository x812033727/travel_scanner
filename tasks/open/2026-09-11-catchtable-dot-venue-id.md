---
id: 2026-09-11-catchtable-dot-venue-id
title: Support dotted Catchtable venue IDs safely
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T14:33:26Z
completed_at:
branch: codex/catchtable-dot-venue-id
depends_on: []
scope:
  - apps/api/app/foods/platform_links.py
  - apps/api/tests/test_food_platform_links.py
  - apps/web/lib/reservation-platforms.ts
  - apps/web/lib/reservation-platforms.test.ts
  - apps/web/components/admin-merchant-platform-editor.test.tsx
  - apps/web/components/merchant-external-links.test.tsx
  - apps/web/e2e/food-reservation-platforms.spec.ts
---

# Support dotted Catchtable venue IDs safely

## Why

The reviewed Catchtable original `https://www.catchtable.net/zh-TW/shop/yosukgung.kr` was rejected by both shared validators because the venue ID contains a literal dot. The admin platform-only save stayed disabled and the public component would omit the same otherwise reviewed URL.

## Definition of done

- [x] Exact literal dotted Catchtable IDs can be saved independently and rendered without dropping their identity.
- [x] Host, HTTPS, path traversal, encoding, query and distinct-branch guards remain effective; other providers are not widened.
- [x] API, shared-validator, admin/public component, five-language browser regressions and static/build checks pass.

## Steps

- [x] Reproduce rejected dotted IDs and missing public links in failing-before frontend tests; cover the admin save button with a focused regression.
- [x] Add a Catchtable-specific dot-separated ASCII ID pattern in frontend/backend; reject encoded dots consistently.
- [x] Run focused API, frontend, production-build and browser checks and record actual results.
- [ ] Release through PR/merge/deployment only when separately authorized; do not treat the local fix as live or auto-publish the researched merchant.

## How to verify

Run `uv run pytest tests/test_food_platform_links.py tests/test_reservation_platform_auth.py tests/test_discovery_flow.py` in `apps/api`; `npm run test --workspace @travel-scanner/web -- lib/reservation-platforms.test.ts components/admin-merchant-platform-editor.test.tsx components/merchant-external-links.test.tsx`; i18n, typecheck, lint and build. Run existing `food-reservation-platforms.spec.ts` against the isolated local production build. Fixtures must never submit real reservations or write production data.

## Notes

- Isolated from latest origin/main `94fef42d055678eed0f46efb979ce1a49acd24a7`; unrelated data-enrichment commits and dirty main workspace remain untouched.
- Task claim overlapped historic PR #391/#392 task files still marked review. Both PRs were independently confirmed merged (`28ca9d70`, `19a94294`) and ancestors of this base. Force-claim is only for this isolated successor; other task files were not changed.
- Frontend failing-before run: 14 failures and 224 passes across three affected suites. Thirteen reproduced dotted validator rejection and missing five-language public links; the admin test initially used an unavailable matcher, corrected to the repository's explicit DOM-property assertions before the final run.
- Literal dot-separated IDs only: no leading, trailing or repeated dots. Global shared slug rules stay unchanged for other providers; encoded dots remain rejected to match backend normalization.
- User authorized implementation, not merge/deployment or catalog publication. No migration, production write, automatic approval, platform booking or paid API activation.
- API validation: **241 passed** across food-platform, reservation-auth and discovery-flow suites (SQLite/ASGI fixtures; no external provider calls). Includes dotted platform-only service save with unchanged merchant relations/other platform, reviewed-only public output in five locales, and independent branch identities. Two existing Python boolean-inversion deprecation warnings; no test failure.
- Frontend: **251 passed** across shared URL validator, admin platform editor, public merchant links and merchant-panel suites. Full web lint, typecheck, five-locale/25-namespace translation validation and production build passed.
- Ruff passed both changed API files; Mypy passed `app/foods/platform_links.py`. After the browser evidence adjustment, targeted E2E ESLint and full TypeScript checks passed again.
- Read-only cross-runtime comparison covered **174 Catchtable URL/identity cases** over no locale plus five supported locales, valid dotted IDs, encoded values and malicious forms: **zero frontend/backend differences**.
- Existing Playwright production-build fixture now exercises the dotted save after TableCheck/inline edits, rejects repeated/encoded dots and traversal before writing, and preserves unsaved merchant name/independent platform rows. No synthetic URL is opened on Catchtable or sent to production.
- Browser diagnostics: initial two-worker run had 31 passes and a zh-TW/1280 mobile-emulation timeout; its trace passed every save/identity/preservation/overflow assertion before timing out at the final screenshot. The same case passed twice in isolation (4.2s/4.0s). A full single-worker rerun had 31 passes and the same screenshot-stage timeout on ja/1280 instead. Both traces are retained under ignored `apps/web/test-results/`.
- Evidence capture now uses Playwright `scale: "css"` so high-DPR mobile emulation does not produce oversized desktop-width PNGs. Viewports, device behavior, screenshots, assertions and the default 30-second timeout are preserved; no test is skipped. This is a test-artifact change, not a production UI or viewport change.
- Final production-build Playwright run: **32 passed in 2.6 minutes**, all five locales at 320/390/1280px in desktop and mobile Chromium projects, light/dark theme cases, plus conflict retry. Command: `PLAYWRIGHT_SERVE_BUILD=true PLAYWRIGHT_PORT=3193 npx playwright test e2e/food-reservation-platforms.spec.ts --workers=1 --max-failures=2 --trace=retain-on-failure --output=test-results/catchtable-final` (environment variables set using PowerShell on Windows). `.last-run.json` reports passed with no failed tests. Normal startup warns about Next standalone/next start; no server launch or test failure in the final run.
- Inspected actual 320px zh-TW and 390px ja dark save-result screenshots; verified the final CSS-resolution 320px capture as well. These are isolated fixture screenshots, not production moderation proof. Production build ID: `jT4r4mW4sST6Yys9psEHa`.
- Implementation and local validation complete. Keep release separate: no PR opened, no merge/deployment, no catalog data write. The task is released with this handoff instead of being marked merged.
