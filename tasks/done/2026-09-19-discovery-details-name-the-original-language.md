---
id: 2026-09-19-discovery-details-name-the-original-language
title: Discovery details name the original language instead of printing its locale code
status: done
priority: P3
area: web
owner: gpt-6-codex-d99a
claimed_at: 2026-09-30T15:59:06Z
created_at: 2026-09-19T11:19:36Z
completed_at: 2026-10-01T00:00:21Z
branch: codex/discovery-language-names
depends_on: []
scope:
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/card-details.test.tsx
---

# Discovery details name the original language instead of printing its locale code

## Why

The discovery detail drawer's sources section prints the raw locale code after the
"original language" label: `原文語言: ja`, `Original language: zh-TW`. Every other word on
that line is in the reader's language. `2026-09-11-discovery-card-language-badge` gave the
feed card a proper name through `contentLanguageName` in `card.tsx`, but that helper returns
null when reader and content locales match, because the card must add nothing then; the
detail line always shows the language, so it needs the name in both cases.

## Definition of done

- [x] The sources line of `DiscoveryDetails` names the original language in the reader's
      language (a zh-TW reader sees 日文, an en reader sees Japanese), also when it equals the
      reader's own language.
- [x] A locale the platform cannot name, or an empty one, falls back to what shows today (the
      code) rather than an empty label, and never throws.

## Steps

- [x] Give `contentLanguageName` in `card.tsx` a way to name the language regardless of
      equality (a second export or an option), keeping the card's "same locale, no badge" rule
      and its `card.test.tsx` intact.
- [x] Use it at the `{c.originalLanguage}: {item.locale}` line in `DiscoveryDetails`.
- [x] Cover both the named and the fallback case in `card-details.test.tsx`.

## How to verify

```bash
cd apps/web && npx vitest run components/discovery/card-details.test.tsx components/discovery/card.test.tsx
cd ../.. && npm run check:i18n && npm run typecheck:web && npm run lint:web
```

## Notes

- 2026-10-01: claimed after checking 29 open PRs, remote/local branches and 175
  other accessible worktrees. Both component/test paths and this ticket's records
  are free of active collisions. `claim --force` bypassed the old badge claim;
  its work already merged in #565 (`d11178863d1a2a35ddfff17be65bcc2a63514194`).
  No other holder's task or worktree was modified.
- `contentLanguageName` keeps its default badge behavior and offers
  `includeSameLocale: true` to the detail sources line. CLDR names the language;
  an unnameable, malformed or empty value retains the original code. No message
  keys or translations were changed.
- Added 17 rendered-detail regressions: zh-TW/en readers of Japanese, English
  reading English, all five matching reader/content locales (case-normalized),
  and nine unknown/malformed/empty/null/undefined values. Before the fix, eight
  named-language cases failed at the actual source line. After the fix, all 71
  detail/card tests pass; the original badge tests are unchanged.
- Validation: `lint:web`, `typecheck:web` and `check:i18n` pass (five locales,
  25 namespaces). Final scope audit found no open-PR overlap and no changes in
  these paths across 171 other accessible worktrees (excluding the known P:
  deletion snapshot). Full web suite and CI status are recorded in the PR.

- Filed while finishing `2026-09-11-discovery-card-language-badge`, which holds `card.tsx`
  until its pull request lands; claim this one after that.
- `Intl.DisplayNames` with `fallback: "none"` returns undefined for a tag it cannot name and
  throws on one it cannot parse; the existing helper already turns both into null.
- No new message key is needed: `getDiscoveryCopy(locale).originalLanguage` is the label.
