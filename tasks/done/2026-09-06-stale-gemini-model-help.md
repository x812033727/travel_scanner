---
id: 2026-09-06-stale-gemini-model-help
title: Admin help text tells operators to avoid the model now shipped
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:23:09Z
created_at: 2026-09-06T00:52:20Z
completed_at: 2026-09-06T06:56:51Z
branch: claude/ai-settings-consolidation
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

- [x] The help text describes what the operator should actually do with the field it sits on.
- [x] It does not contradict the shipped default.

## Steps

- [x] Rewrite the help. Done as part of `2026-09-06-ai-settings-web`: the field is now a
      catalog dropdown, its help lives at `providerFields.hotspot_guide_gemini_model.help`
      in `apps/web/messages/*/admin.json` (Flash builds candidate lists, is weaker at
      listing grounded sources; Pro may be closed to new keys; trust the connection test),
      and every Gemini entry in `apps/api/app/ai/catalog.py` carries its own tier note that
      shows under the dropdown.
- [x] The comment above `hotspot_guide_gemini_model` in `apps/api/app/config.py` says the
      same thing and was left as is.

## How to verify

Open `/admin/settings`, AI 服務 → Gemini 多語文章搜尋, and read the model dropdown's help
and the selected option's note against the value in the dropdown. They should agree.

## Notes

Han text in `apps/web/**/*.tsx` is checked by `tools/check-i18n.mjs`, which rejects *new*
Han runs in those files; the old sentence was removed from the tsx rather than edited, and
the replacement went through the message catalogs.
