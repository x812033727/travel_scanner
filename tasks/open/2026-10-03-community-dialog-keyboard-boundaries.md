---
id: 2026-10-03-community-dialog-keyboard-boundaries
title: Keep community dialog keyboard focus within the active layer
status: review
priority: P2
area: web
owner: codex-community-dialog-keyboard-20261003
claimed_at: 2026-10-03T13:56:07Z
created_at: 2026-10-03T13:55:56Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/web/components/community/ui.tsx
  - apps/web/components/community/ui.test.tsx
---

# Keep community dialog keyboard focus within the active layer

## Why

The community report dialog does not explicitly wrap Tab at its first and last usable controls. In PR #1175 run 37126555983, all five locales on both browser projects failed the existing assertion that Shift+Tab from the Close button focuses the enabled Submit button. The trace did not record the resulting active element, so this evidence does not identify where focus moved. The shared native Dialog needs a narrow boundary guard that preserves its existing dismissal, nested-layer ownership, and focus restoration behavior.

## Definition of done

- [x] Tab from the last usable control focuses the first, and Shift+Tab from the first focuses the last.
- [x] Disabled and hidden trailing controls are excluded; ordinary intermediate Tab movement stays native.
- [x] Only the topmost dialog handles a boundary event; already-consumed and composing events are preserved.
- [x] The existing six regression cases remain unchanged and pass, including native cancel/close, backdrop behavior, nested dismissal, scrolling, and opener focus restoration.
- [x] New assertions fail against the original implementation and pass after the minimal fix; scoped lint passes.
- [ ] Evaluate the unchanged real-browser keyboard assertions on the new CI head.

## Steps

- [x] Verify the two source paths are free of active work and claim this new ticket normally.
- [x] Add focused regressions and record the original implementation's failure.
- [x] Reuse the existing modal focus-target and top-layer helpers for boundary-only handling.
- [x] Record focused tests, lint, exact runtime and source hashes; obtain independent review before integrating.

## How to verify

From `apps/web`, use the selected bundled Node to run `../../node_modules/vitest/vitest.mjs run components/community/ui.test.tsx --reporter=verbose`, followed by `../../node_modules/eslint/bin/eslint.js components/community/ui.tsx components/community/ui.test.tsx --max-warnings=0`.

The full-stack community browser matrix is the separate real-browser check: the report dialog must wrap both keyboard boundaries without weakening its current assertions. Parent coordinates the full web typecheck/build and CI run.

## Notes

- Normal claim succeeded; no force was used. Existing shared modal helper behavior is reused without changing that helper or the browser expectations.
- Preserve the native Escape/cancel handler, close handler, backdrop detection, scroll lock, trigger restoration, and their six original test blocks byte-for-byte.
- Private preparation and command receipts: `<home>/.codex/tmp/community-dialog-keyboard-20261003/`. Source, test results, and browser acceptance are recorded separately; the first CI's 18 browser failures also include eight unrelated admin-locale fixture failures handled in the original community-web ticket.
- Local validation used the actual bundled primary-runtime `node.exe` v24.19.0 (`win32/arm64`) and this worktree's Vitest 5.0.2. The original source produced 3 failed / 10 passed: both boundary directions and the nested child failed the exact focus assertion. The corrected source produced 13 passed / 0 failed / 0 skipped. Scoped ESLint and `git diff --check` returned 0. These are unit-level results; jsdom does not perform native intermediate Tab navigation.
- `implementation-receipt.json` SHA-256 `99a85264c41a61cdac45641e036346da69e872f718de00a7df942fbaff449670` binds the exact argv/runtime, red/green/lint logs and receipts, source SHA-256 `edd54a41e8ff13d9be2231d26758c022cbe6736ca9e6307fa4d06407dd2cc77b`, and test SHA-256 `d7fb81c9e25a201e9dc3ec77796a304805eec196e8c50eddb89cfa927f74070f`. Mechanical comparison confirms the original six test blocks are byte-identical and reversing only the helper import/new handler restores the original source bytes.
- Independent source review passed for keyboard boundaries and the isolated admin-locale fixture. Receipt SHA-256 `95b4bd9244e120eeffc5e7a7f9390ce4b700dde44ad5edd444de6ece09a92646`; the four-path collision gate SHA-256 is `f5612ac20302de81b7e0c9414f4f9ae7c9744cf164e4e460033748fb3fd060d5`. This review does not replace real-browser execution.
- The complete web TypeScript check passed on 2026-10-03, 14:01:29–14:02:37 UTC (exit 0). Its owned compiler process used bundled primary Node v24.19.0; npm was invoked through the installed npm shim. All three UI/test/spec hashes were unchanged. Private receipt: `task-continuation-20261003/ui-locale-typecheck-20261003T140129996Z.json`. Exact-head CI remains pending.
- At PR head `70174ca194dc386ead9c02a1e70cc1d0aed7645a`, actual checkout `a52226de3d79d89e817cecd10ed05f237ecd1916`, the unchanged keyboard assertions now ran past both boundaries and focus restoration in all five locales and both browser projects. The broader matrix had 28 passes and two later Japanese message-locator failures at line 225; the full-stack job failed overall. The UI and unit-test hashes matched this ticket's frozen hashes in both the PR and actual checkout. Private canonical receipt SHA-256 `90073327ab7d271fa4cba80f01f65bf89ca160abe70a18a4d8b48c5001535a60`. Keep review until the coordinated corrected matrix and CI complete.
