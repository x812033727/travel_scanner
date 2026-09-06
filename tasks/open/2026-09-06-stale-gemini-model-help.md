---
id: 2026-09-06-stale-gemini-model-help
title: Admin help text tells operators to avoid the model now shipped
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:52:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-settings-panel.tsx
---

# Admin help text tells operators to avoid the model now shipped

## Why

The Gemini model field on `/admin/settings` reads:

> Gemini 模型 — Flash 級模型會拒絕列出來源，請改用 Pro 級模型。

The shipped default is `gemini-3.5-flash`, a Flash-tier model. An operator reading the field
is told the configured value is the wrong one.

The sentence is not simply wrong, which is what makes it confusing. Flash-tier models do
refuse the grounded "list these sources" prompt that the guide search uses. But the same
model handles the schema-bound candidate-generation prompt fine, and `gemini-2.5-pro` returns
404 for new API keys, so Pro is not available to advise. The field help states one half of
that as unconditional advice.

## Definition of done

- [ ] The help text describes what the operator should actually do with the field it sits on.
- [ ] It does not contradict the shipped default.

## Steps

- [ ] Rewrite `fieldMeta.hotspot_guide_gemini_model.help` in
      `apps/web/components/admin-settings-panel.tsx`. It should say which task each tier
      suits, rather than issuing a blanket instruction — Flash is fine for the schema-bound
      path, weaker on the grounded source-listing path, and Pro is closed to new keys.
- [ ] Check the comment above `hotspot_guide_gemini_model` in `apps/api/app/config.py` says
      the same thing; it was updated when the default changed and is the accurate version.

## How to verify

Open `/admin/settings`, find the Gemini 多語文章搜尋 card, and read the model field's help
against the value in the field next to it. They should agree.

## Notes

Han text in `apps/web/**/*.tsx` is checked by `tools/check-i18n.mjs`, which rejects *new*
Han runs in those files — but this string already exists, so editing it in place is fine.
That check only runs with `CI=1` (or something staged): a plain local `npm run check:i18n`
prints "Validated 5 locales" and tells you nothing. Verify with `CI=1 npm run check:i18n`
after committing.
