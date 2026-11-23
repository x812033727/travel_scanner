---
id: 2026-11-20-gemini-key-pool-per-slot-save
title: Gemini key pool per-slot save (A/B/C/D...), circular turn rotation and manual start slot
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-20T08:25:42Z
created_at: 2026-11-20T08:25:05Z
completed_at: 2026-11-20T08:33:31Z
branch: antigravity/gemini-pool-slots-and-rotation
depends_on: []
scope:
  - apps/api/app/admin/router.py
  - apps/api/app/ai/gemini_pool.py
  - apps/api/tests/test_gemini_pool.py
  - apps/web/components/admin-gemini-pool.test.tsx
  - apps/web/components/admin-gemini-pool.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/lib/gemini-pool-messages/en.json
  - apps/web/lib/gemini-pool-messages/ja.json
  - apps/web/lib/gemini-pool-messages/ko.json
  - apps/web/lib/gemini-pool-messages/zh-CN.json
  - apps/web/lib/gemini-pool-messages/zh-TW.json
---

# Gemini key pool per-slot save (A/B/C/D...), circular turn rotation and manual start slot

## Why

Previously, extra Google AI Ultra Gemini keys (`hotspot_guide_gemini_api_keys_extra`) and their monthly budgets (`hotspot_guide_gemini_key_budgets_usd`) were entered as a single comma-separated string, making it error-prone to add, replace or clear a single account slot. In addition, the pool always restarted from index 0 whenever an earlier key's cooldown expired instead of keeping a circular turn pointer (`A → B → C → … → A`), and the owner had no button to pick which account slot (`A`, `B`, `C`…) the pool should start running from.

## Definition of done

- [x] Extra Gemini keys can be entered, saved and cleared individually per named slot (`A`, `B`, `C`, `D`… expandable up to `Z` via a "+ 新增帳號槽" button) in the `AdminGeminiPool` panel on the `ai_vendors` card, while preserving full backward compatibility with legacy comma-separated strings.
- [x] `gemini_pool` maintains a persistent circular turn pointer (`gmpool:turn:<month>`): when slot `A` runs out of credit/quota or hits its limit/budget, the turn moves to `B`, then `C`, and wraps from the last configured Ultra slot back to `A`.
- [x] The admin panel displays which slot (`A`, `B`, `C`…) is currently active/in turn, and lets the owner click "從此開始" on any configured Ultra slot to immediately switch the turn pointer to that slot (clearing any temporary rest on it).

## Steps

- [x] Extend `apps/api/app/ai/gemini_pool.py` with slot parsing/serialization (`A`–`Z`, backward-compatible with comma-separated strings), circular turn pointer (`current_turn`, `set_turn`, sticky rotation in `choose`), and unit tests in `apps/api/tests/test_gemini_pool.py`.
- [x] Add `PUT /admin/provider-settings/ai_vendors/gemini-pool/slots/{slot}` and `POST /admin/provider-settings/ai_vendors/gemini-pool/turn` to `apps/api/app/admin/router.py`, and include `slot`, `configured`, `is_turn` and `current_turn_slot` in `GeminiPoolSnapshot`.
- [x] Update `apps/web/components/admin-gemini-pool.tsx`, `apps/web/components/admin-settings-panel.tsx`, the 5 locale files under `apps/web/lib/gemini-pool-messages/` and `apps/web/components/admin-gemini-pool.test.tsx`.

## How to verify

```bash
cd apps/api && uv run ruff check app/ai/gemini_pool.py app/admin/router.py tests/test_gemini_pool.py && uv run mypy app/ai/gemini_pool.py app/admin/router.py tests/test_gemini_pool.py && uv run pytest tests/test_gemini_pool.py -q
cd apps/web && npx vitest run components/admin-gemini-pool.test.tsx
```

## Notes

- Claimed with `--force` over `2026-11-17-gemini-pool-ordinary-rate-limit-429`, which was already merged in #2140 (`efa37ae6a`).
