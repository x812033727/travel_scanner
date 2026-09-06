---
id: 2026-09-06-ai-settings-web
title: AI settings in the admin panel: vendor card, model dropdowns, per-feature models (web)
status: in-progress
priority: P1
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:23:38Z
created_at: 2026-09-06T06:23:05Z
completed_at:
branch: claude/ai-settings-consolidation
depends_on: []
scope:
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/components/admin-hotspot-guides-panel.tsx
  - apps/web/components/admin-hotspot-guides-panel.test.tsx
  - apps/web/messages
---

# AI settings in the admin panel: vendor card, model dropdowns, per-feature models (web)

## Why

On `/admin/settings` the AI keys were split between the「AI 行程規劃」card and the
「Gemini 多語文章搜尋」card under a different category, every model was a free-text box,
and nothing showed which vendor and model a feature would actually call. The owner asked
for one place for keys, dropdowns for models, and a clear "which vendor, which model" per
feature.

## Definition of done

- [x] The AI 服務 category holds four cards: AI 供應商與金鑰 (no enable switch), AI 行程規劃,
      AI 景點介紹搜尋, Gemini 多語文章搜尋.
- [x] Model fields render as dropdowns from the server's `field_options`, with 自訂… for an
      unlisted id; a stored id outside the catalog shows as custom instead of snapping to
      the first option.
- [x] Each feature card shows the vendor dropdown and only the model dropdown(s) that
      vendor choice needs (auto → all three in priority order).
- [x] The hotspot AI-search dialog shows "供應商 · 模型" per option.

## Steps

- [x] `admin-settings-panel.tsx`: `field_options` type, `customFields` in the draft,
      `visibleConfigFields`/`selectedAiVendors`, `hasEnableToggle`, diff-only save for
      `ai_vendors`, custom-id input, localized labels via `providerFields.*`, fix of the
      text-branch label bug.
- [x] `messages/*/admin.json`: `providerFields` namespace in all five locales;
      `messages/*/hotspotAdmin.json`: `aiProviderModel`, `aiProviderHelp`.
- [x] `admin-hotspot-guides-panel.tsx`: read `coverage.ai_search.models`.
- [x] Tests: eight new panel cases, guides dialog fixture and assertion.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
git add -A && node tools/check-i18n.mjs     # staged mode runs the Han-run gate
```

Then open `/admin/settings` → AI 服務 and walk the four cards; change 行程來源 between
自動備援 and a single vendor and watch the model dropdowns follow.

## Notes

- New visible text went through the catalogs on purpose: `tools/check-i18n.mjs` rejects
  any new Han run in `apps/web/**/*.tsx`, even a second copy of an existing one.
- The custom-id input sits outside the `<label>` (as a sibling) so
  `getByLabelText(/^OpenAI 模型/)` keeps resolving to the select alone; it carries its own
  `aria-label` (`providerFields.customInputLabel`).
- `ai_vendors` saves config diff-only (like `runtime`/`layout`) so pasting a key does not
  turn the four environment-default Base URLs into database overrides.
- The rest of the panel's hardcoded zh-TW copy is still `2026-09-06-admin-panels-i18n`.
