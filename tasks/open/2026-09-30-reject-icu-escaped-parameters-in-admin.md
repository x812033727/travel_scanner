---
id: 2026-09-30-reject-icu-escaped-parameters-in-admin
title: Reject ICU-escaped parameters in admin UI text overrides
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-30T02:08:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/ui-text.ts
  - apps/web/lib/ui-text.test.ts
  - apps/api/app/ui_text/service.py
  - apps/api/tests/test_ui_text.py
  - apps/api/tests/test_ui_text_integration.py
  - docs/ui-text-overrides.md
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

- [ ] The editor, API write path and web merge reject an override that quotes away
      a runtime argument, with an actionable validation message.
- [ ] Existing saved invalid overrides fall back to the valid default when read.
- [ ] Valid curly-quoted or doubled-apostrophe arguments still work, and deliberate
      literal URL-template tokens remain preserved, including Travelpayouts help.
- [ ] Cover nested plural/select branches and syntax errors consistently across
      API and web validation. Avoid silently accepting incompatible semantics.

## Steps

- [ ] Audit `normalize_value`, `icu_parameters`, `overrideProblem` and
      `applyUiTextOverrides`; choose compatible parsing/validation semantics.
- [ ] Add behavioral API/web regressions and update override documentation.
      Keep the separate lexical-token guard for literal template tokens.

## How to verify

Run `npm run test:web -- lib/ui-text.test.ts`, the affected editor tests,
`npm run check:i18n`, and from apps/api `uv run pytest tests/test_ui_text.py
tests/test_ui_text_integration.py -q`. PostgreSQL integration cases run in CI.
Verify actual IntlMessageFormat output, not only placeholder-name regex results.

## Notes

- The API already tests that `icu_parameters("'{destination}' is quoted")`
  contains `destination`. Replacing only the web helper with an ICU argument set
  would break API/editor parity and lose protection for literal template tokens.
- No production override rows have been inspected or modified. This is a code
  follow-up; any live cleanup needs its own review and authorization.
