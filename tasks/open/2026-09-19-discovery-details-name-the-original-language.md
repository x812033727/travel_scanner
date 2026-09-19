---
id: 2026-09-19-discovery-details-name-the-original-language
title: Discovery details name the original language instead of printing its locale code
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-19T11:19:36Z
completed_at:
branch:
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

- [ ] The sources line of `DiscoveryDetails` names the original language in the reader's
      language (a zh-TW reader sees 日文, an en reader sees Japanese), also when it equals the
      reader's own language.
- [ ] A locale the platform cannot name, or an empty one, falls back to what shows today (the
      code) rather than an empty label, and never throws.

## Steps

- [ ] Give `contentLanguageName` in `card.tsx` a way to name the language regardless of
      equality (a second export or an option), keeping the card's "same locale, no badge" rule
      and its `card.test.tsx` intact.
- [ ] Use it at the `{c.originalLanguage}: {item.locale}` line in `DiscoveryDetails`.
- [ ] Cover both the named and the fallback case in `card-details.test.tsx`.

## How to verify

```bash
cd apps/web && npx vitest run components/discovery/card-details.test.tsx components/discovery/card.test.tsx
cd ../.. && npm run check:i18n && npm run typecheck:web && npm run lint:web
```

## Notes

- Filed while finishing `2026-09-11-discovery-card-language-badge`, which holds `card.tsx`
  until its pull request lands; claim this one after that.
- `Intl.DisplayNames` with `fallback: "none"` returns undefined for a tag it cannot name and
  throws on one it cannot parse; the existing helper already turns both into null.
- No new message key is needed: `getDiscoveryCopy(locale).originalLanguage` is the label.
