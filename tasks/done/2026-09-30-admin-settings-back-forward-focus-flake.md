---
id: 2026-09-30-admin-settings-back-forward-focus-flake
title: Stabilize admin settings Back/Forward focus under load
status: done
priority: P3
area: web
owner: codex-b10e-settings-focus
claimed_at: 2026-10-01T00:51:31Z
created_at: 2026-09-30T11:01:19Z
completed_at: 2026-10-01T01:14:54Z
branch: codex/admin-settings-focus-20261001
depends_on: []
scope:
  - apps/web/components/admin-settings-panel.test.tsx
---

# Stabilize admin settings Back/Forward focus under load

## Why

The unchanged `AdminSettingsPanel` test named `restores provider, field focus and
audit panel from Back/Forward URL state` failed its focus wait during a full web
run on 2026-09-30 under heavy local CPU/memory load. React also reported updates
outside `act`. The complete 59-test settings suite passed when run separately.
This makes unrelated changes fail validation intermittently.

The same symptom was recorded in `tasks/done/2026-09-09-discovery-card-details.md`:
the unchanged suite failed under concurrent build load and passed in isolation.
That task delivered discovery cards; it did not repair this test's synchronization.

## Definition of done

- [x] Identify and repair the focus/history synchronization race, preserving the
      Back/Forward acceptance assertions and the existing timeout budget.
- [x] The settings test passes in isolation and as part of the full web suite.

## Steps

- [x] Audit active worktrees, claims and open PRs for this test before claiming it.
- [ ] Reproduce the full-suite failure and capture the exact focus assertion.
- [x] Fix the missing React synchronization or cleanup without weakening checks.

## How to verify

Run `npm run test:web -- components/admin-settings-panel.test.tsx` and then
`npm run test:web`, preserving the normal Vitest configuration. If isolating one
test, invoke Vitest directly or forward the test-name option through both npm
layers; an outer `-t` may be consumed by npm and actually run the entire file.

## Notes

- 2026-10-01: normal claim after 14 open PRs, 46 remote heads and local/worktree scope checks found no active collision. The OneDrive dirty test additions were compared byte-for-byte with their merged versions and current main; they are historical residue. No other worktree was modified.
- The existing Back/Forward case now owns a local animation-frame queue, flushes actual callbacks frame by frame inside async `act`, honors cancellations and defers newly queued callbacks to the next frame. All three history/popstate transitions use `act`. A ten-frame cap fails explicitly if effects do not settle; `finally` unmounts before restoring globals. Product code, Vitest configuration, the original assertions and timeout budgets are unchanged.
- Controlled RED: with data rendered and one frame pending, the unchanged focus wait failed because `document.activeElement` remained `body`. GREEN: the repaired case passed. Removing only its frame flushes while retaining `act` failed at the same precise focus assertion. Both temporary mutations were restored byte-for-byte and hash-checked.
- These negatives prove the test's dependency on real jsdom frame scheduling; they do not establish the historical heavy-load failure's unique cause. The fresh full-suite failure reproduction step remains unchecked for that reason; its original evidence above is preserved.
- Settings file: 59/59 PASS. Scoped ESLint and TypeScript using the existing web configuration passed; independent review passed. The one default full web run on base `01c04f6e` passed all 335 files / 3670 tests (803.82 s), with the normal configuration and no retries, timeout increases or skipped assertions.
- Observed while validating `2026-09-30-reject-icu-escaped-parameters-in-admin`, on
  main 422b3f68. The ICU change does not edit this test, its component or Vitest
  configuration; the directly declared FormatJS version was already installed.
- Full run: 59 settings tests / one Back/Forward failure (3,074 ms), then stalled
  before another file completed. CPU was 100% and free physical memory fell to
  roughly 540 MB. The owning full-run process was stopped; this is not a completed
  full-suite result. Isolated settings file: 59 passed in 22.55 seconds.
- No test retry loop, timeout increase or skipped acceptance assertion was added.
  This ticket remains unclaimed; no settings files were changed for the ICU fix.
