---
id: 2026-09-19-mobilenav-search-button-fires-twice-in
title: Isolate MobileNav search mock calls between discovery cases
status: done
priority: P2
area: web
owner: codex-test-isolation
claimed_at: 2026-09-29T06:41:18Z
created_at: 2026-09-19T14:14:09Z
completed_at: 2026-09-29T06:51:41Z
branch: codex/test-isolation-fixes
depends_on: []
scope:
  - apps/web/components/mobile-nav.test.tsx
---

# Isolate MobileNav search mock calls between discovery cases

## Why

The original 2026-09-19 report observed `discovery: true` failing with
`expected vi.fn() to be called 1 times, but got 2 times`. Its assertion counted
calls left over from the preceding `discovery: false` case. Both parameterized
cases share the hoisted `search.open` mock, and the fixture reset only discovery
flags. There is no evidence of a duplicated product click handler.

## Definition of done

- [x] All 13 MobileNav cases pass with the repository runner and with automatic
      mock clearing disabled.
- [x] The cause is demonstrated by changing only mock clearing, while a single
      discovery case still invokes the handler once.
- [x] Each case clears the shared mock's call history explicitly; the assertion
      still detects two calls caused by one click within that case.

## Steps

- [x] Inspect component bindings, runner versions and the original report.
- [x] Reproduce the exact failure using the same sources with `clearMocks: false`.
- [x] Clear `search.open` in `beforeEach`; leave component behavior unchanged.
- [x] Verify both configurations and record final results.

## How to verify

From `apps/web`, run `npx vitest run components/mobile-nav.test.tsx`.
Also run the same file with a scratch config importing `vitest.config.ts` and
overriding only `test.clearMocks` to `false`. This option is not a Vitest CLI flag.

## Notes

- Diagnosis on 2026-09-29: normal Vitest 5.0.1 configuration passed 13/13;
  disabling mock clearing yielded 12 passed / 1 failed with the exact original
  assertion; running only `discovery: true` with clearing disabled passed.
- The repository runner defaults to clearing mocks. The shared install named
  in the original report currently contains Vitest 4.1.11, whose default is
  false; this is not proof of the exact version installed on 2026-09-19.
  The explicit reset avoids depending on runner defaults.
- The component, setup and configuration did not change between the original
  report and this diagnosis. No merged product fix is claimed.
- After the explicit reset, both configurations pass all 13 tests. A scratch
  Vite transform that invokes the handler twice for each click fails both
  discovery cases (11 passed / 2 failed), so the single-click assertion still
  detects a real duplicated handler. Component source stays unchanged.
- ESLint for the changed test passes with zero warnings.
- The original `qrcode` resolution error was a shared-install gap. The worktree
  now has its own dependencies. Before this isolated test edit, the full web
  suite on PR #972 passed 334 files / 3,580 tests with no `qrcode` failure.
  That is prior validation, not a full-suite run of this new branch.
- Controlled red-run reports and source hashes are retained privately at
  `<home>/.codex/tmp/mobile-nav-obsolete-review-20260929/`.
  Receipt SHA-256:
  `8b597afc8d4c1eaaddc89997d1078b3057be3c057796d6691d996ce9d67b54af`.
- The green and deliberately duplicated-handler runs use base `49aa683a` with
  Vitest 5.0.1. Their `green-receipt.json` SHA-256 is
  `883abfa95a3e9ac665cc51eebcdccb4c05ca1990d4229497b83a86b73ab5c3c8`.
- After rebasing onto main `c1fe22fc` and reinstalling its dependencies,
  bundled Node 24.21.0 / Vitest 5.0.2 also passed all 13 cases with each
  configuration. ESLint passed again. These newer reports are retained at
  `<home>/.codex/tmp/test-isolation-fixes-20260929/` as
  `mobile-current-5.0.2.json` and `mobile-no-clear-5.0.2.json`.
