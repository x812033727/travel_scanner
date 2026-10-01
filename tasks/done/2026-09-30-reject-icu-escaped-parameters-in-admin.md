---
id: 2026-09-30-reject-icu-escaped-parameters-in-admin
title: Reject ICU-escaped parameters in admin UI text overrides
status: done
priority: P2
area: web
owner: codex-gpt6-ui-text-icu
claimed_at: 2026-09-30T10:24:55Z
created_at: 2026-09-30T02:08:56Z
completed_at: 2026-09-30T11:03:32Z
branch: codex/ui-text-icu-overrides
depends_on: []
scope:
  - apps/web/lib/ui-text.ts
  - apps/web/lib/ui-text.test.ts
  - apps/web/components/admin-ui-text-panel.test.tsx
  - apps/web/package.json
  - package-lock.json
  - apps/api/app/ui_text/service.py
  - apps/api/app/ui_text/icu.py
  - apps/api/tests/test_ui_text.py
  - apps/api/tests/test_ui_text_integration.py
  - docs/ui-text-overrides.md
  - docs/ui-text-icu-cases.json
---

# Reject ICU-escaped parameters in admin UI text overrides

## Why

The catalog checker now catches quoted ICU arguments, but administrator overrides
still use lexical brace matching in both the API and web merge/editor helpers.
With default `Hello {name}`, override `Hello '{name}'` passes validation and
`applyUiTextOverrides` reports one applied row. IntlMessageFormat then renders
`Hello {name}` literally even when given `name: "Ada"`.

This was reproduced locally while completing
`2026-09-27-korean-placeholders-escaped-by-apostrophes` (PR #1005). That ticket
repairs the bundled catalogs and their CI check; it does not change saved overrides.

## Definition of done

- [x] The editor, API write path and web merge reject an override that quotes away
      a runtime argument, with an actionable validation message.
- [x] Existing saved invalid overrides fall back to the valid default when read.
- [x] Valid curly-quoted or doubled-apostrophe arguments still work, and deliberate
      literal URL-template tokens remain preserved, including Travelpayouts help.
- [x] Cover nested plural/select branches and syntax errors consistently across
      API and web validation. Avoid silently accepting incompatible semantics.

## Steps

- [x] Audit `normalize_value`, `icu_parameters`, `overrideProblem` and
      `applyUiTextOverrides`; choose compatible parsing/validation semantics.
- [x] Add behavioral API/web regressions and update override documentation.
      Keep the separate lexical-token guard for literal template tokens.

## How to verify

Run `npm run test:web -- lib/ui-text.test.ts`, the affected editor tests,
`npm run check:i18n`, and from apps/api `uv run pytest tests/test_ui_text.py
tests/test_ui_text_integration.py -q`. PostgreSQL integration cases run in CI.
Verify actual IntlMessageFormat output, not only placeholder-name regex results.

## Notes

- Implemented syntax-aware contracts with the actual web IntlMessageFormat parser
  and a pure Python API parser. Preserve argument roles in each branch, selector sets,
  plural kind/offset and pound references; separately preserve parsed literal template
  tokens. Invalid persisted/cached overrides are skipped by the web merge. API batch
  validation still precedes all row, audit and cache mutations.
- Shared corpus: 43 acceptance/rejection cases, including actual formatted output.
  Independent differential checks found zero mismatches in 145 targeted syntax cases
  and 2,125 deterministic mutations; all 33,200 bundled catalog strings parsed.
- Local verification: 77 focused web tests passed, including the real editor Save
  state. API tests: 84 passed / one PostgreSQL-only skip; the final human-readable
  diagnostic change passed its three focused tests. Full API Ruff and mypy app
  (445 files) / tests (335 files), web lint and typecheck passed. Staged i18n validation
  passed for five locales / 25 namespaces; task checks passed for 1,196 files with
  existing unrelated stale-claim warnings. The existing locked
  IntlMessageFormat 11.2.15 is now a direct dependency; npm ci dry-run passed.
- On the final d7787f51 base, all 64 helper tests passed. A threads worker failed
  to start before running the editor file; its 13 tests then passed with the CLI
  `--pool=forks` environment workaround. No Vitest configuration or timeout changed.
- Full web run was stopped after a long stall under CPU/memory load. Before the
  stall it reported one unchanged admin-settings Back/Forward focus failure; the
  isolated complete 59-test settings suite passed. Earlier recurrence is recorded in
  tasks/done/2026-09-09-discovery-card-details.md; current follow-up is
  2026-09-30-admin-settings-back-forward-focus-flake. Do not count the full suite as green.
- Final pre-PR audit: 26 open PRs and 175 other accessible worktrees remain clear of
  this scope. Updated base through main d7787f51; the two added main commits only
  change an unrelated done task record and video worker docs synchronization, with
  no overlap in this scope. PostgreSQL/Redis integration and the full suite remain CI acceptance.
  Draft PR only; no merge, deployment, production data access or saved-row cleanup.

- 2026-09-30 claim on main `adee8da0`: six existing scope files plus the new pure API
  parser and shared API/web case corpus are clear across 25 open PRs, 57 remote heads
  and 175 other accessible worktrees. Three old P: checkouts have whole-repository
  deletion states with no competing UI implementation; they were untouched.
  Preserve lexical URL-template tokens separately from runtime ICU arguments. Runtime
  comparison retains argument types, plural offsets and branch scope, so quoting a
  reference away in one branch cannot be hidden by another branch using the same name.
  The direct dependency declaration and actual editor regression paths were separately
  checked against the same live PR/worktree inventory before being added to scope.

- The API already tests that `icu_parameters("'{destination}' is quoted")`
  contains `destination`. Replacing only the web helper with an ICU argument set
  would break API/editor parity and lose protection for literal template tokens.
- No production override rows have been inspected or modified. This is a code
  follow-up; any live cleanup needs its own review and authorization.
