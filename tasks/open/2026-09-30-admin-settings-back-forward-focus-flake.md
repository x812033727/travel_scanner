---
id: 2026-09-30-admin-settings-back-forward-focus-flake
title: Stabilize admin settings Back/Forward focus under load
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-30T11:01:19Z
completed_at:
branch:
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

- [ ] Identify and repair the focus/history synchronization race, preserving the
      Back/Forward acceptance assertions and the existing timeout budget.
- [ ] The settings test passes in isolation and as part of the full web suite.

## Steps

- [ ] Audit active worktrees, claims and open PRs for this test before claiming it.
- [ ] Reproduce the full-suite failure and capture the exact focus assertion.
- [ ] Fix the missing React synchronization or cleanup without weakening checks.

## How to verify

Run `npm run test:web -- components/admin-settings-panel.test.tsx` and then
`npm run test:web`, preserving the normal Vitest configuration. If isolating one
test, invoke Vitest directly or forward the test-name option through both npm
layers; an outer `-t` may be consumed by npm and actually run the entire file.

## Notes

- Observed while validating `2026-09-30-reject-icu-escaped-parameters-in-admin`, on
  main 422b3f68. The ICU change does not edit this test, its component or Vitest
  configuration; the directly declared FormatJS version was already installed.
- Full run: 59 settings tests / one Back/Forward failure (3,074 ms), then stalled
  before another file completed. CPU was 100% and free physical memory fell to
  roughly 540 MB. The owning full-run process was stopped; this is not a completed
  full-suite result. Isolated settings file: 59 passed in 22.55 seconds.
- No test retry loop, timeout increase or skipped acceptance assertion was added.
  This ticket remains unclaimed; no settings files were changed for the ICU fix.
