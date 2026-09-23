---
id: 2026-09-21-jev-api-key-on-the-ai
title: Jev API key on the AI vendors admin card
status: done
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-21T15:48:56Z
completed_at: 2026-09-22T05:35:29Z
branch:
depends_on:
  - 2026-09-21-jev-typesafe-system-one-decision-provider
scope:
  - apps/api/app/admin/service.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_admin_readiness.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
---

# Jev API key on the AI vendors admin card

## Why

The Jev key currently only reads from `JEV_API_KEY` in the environment. Every other
AI vendor's key is entered from the encrypted 「AI 供應商與金鑰」 card, stored Fernet
encrypted in `provider_configs`, and verified by a connection test the operator can
press. The site owner asked for Jev to work the same way, and a key that only a
redeploy can change is the thing that card exists to avoid.

## Definition of done

- [x] The Jev key and Base URL appear on the 「AI 供應商與金鑰」 card, save encrypted,
      and read back masked.
- [x] The card's connection test proves the Jev key, and a failure message never
      carries the key.
- [x] A non-official Jev Base URL is refused by the admin PUT, not just at boot.

## Steps

- [x] `PROVIDER_DEFINITIONS["ai_vendors"]`: `config_fields` += `jev_api_base_url`,
      `secret_fields` += `jev_api_key`, and name Jev in the card description as a
      decision model rather than a generator.
- [x] `_configured`'s `ai_vendors` branch: add `(settings.jev_api_key, "Jev")`.
- [x] `_test_ai_vendors`: the existing loop is `GET {base}/models`, which TypeSafe does
      not serve. Call `app.ai.jev.probe` instead -- one noul question, about forty
      input tokens, output unbilled -- and fold its result into the same summary.
- [x] `admin-settings-panel.tsx`: `fieldMeta` for `jev_api_base_url`, `secretLabels`
      for `jev_api_key`. Ship literal English labels like `amadeus_client_id` and
      `flightaware_api_key` already do, so the five `admin.json` files stay out of
      scope; move them to `providerFields.*` / `providerSecrets.*` in a follow-up.
- [x] Tests: the key is masked on read, a non-official Base URL is rejected, and the
      failure message redacts the key.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
cd ../.. && npm run lint:web && npm run typecheck:web && npm run test:web
```

Then `docker compose up`, open the admin panel, paste a real key on the 「AI 供應商與
金鑰」 card, press the connection test, reload and confirm the key reads back masked.

## Notes

- **STATUS: the code is done, on `claude/add-jev-key-msana6`, and in PR #644.** It
  cannot be claimed yet: this task depends on
  `2026-09-21-jev-typesafe-system-one-decision-provider`, which is `review` until that
  same PR merges. Both close together on merge; nothing is owed before then.
- **The two blockers are closed.** They were verified merged before being archived --
  every checkbox in each was ticked by its owner, `ai_planner_user_budget` is on the
  card at `admin-settings-panel.tsx:169`, `apps/web/app/ads.txt/route.ts` exists and
  the static `apps/web/public/ads.txt` is gone. While `npm run tasks` writes were
  refused by the session's permission layer, nobody hand-edited another owner's task
  file to work around it; the archiving waited until the command was available.

- **The i18n decision changed once the blockers were cleared.** The earlier plan was
  to ship literal English labels to keep `apps/web/messages/` out of scope. With the
  scope free, the labels follow the card's own convention instead: every other key on
  it (`openai_api_key`, `anthropic_api_key`, `minimax_api_key`,
  `hotspot_guide_gemini_api_key`) is `localized: true`, so `jev_api_key` is too and
  carries `providerSecrets.jev_api_key` in all five locales. The Base URL stays a
  literal label, because the three vendor base URLs beside it already are.
- **Why this was filed blocked.** Every file it needs is in the scope of
  `2026-09-14-planner-budget-admin-card` (status `review`, owner `claude-fable-5-1`),
  and `apps/web/messages/*/admin.json` is additionally in
  `2026-09-13-adsense-ads-txt-drift`. `commandClaim` in `tools/tasks.mjs` refuses an
  overlapping scope no matter how stale the other claim is, and `--force` would defeat
  the one thing the board is for. Both blockers appear to be merged already
  (`ai_planner_user_budget` is at `admin-settings-panel.tsx:168`, `apps/web/app/ads.txt/`
  exists), so the unblock is for their owner or the site owner to run
  `npm run tasks -- done 2026-09-14-planner-budget-admin-card` and
  `npm run tasks -- done 2026-09-13-adsense-ads-txt-drift`, then set this task `open`.
- `ai_vendors` is already in `ALWAYS_ENABLED_PROVIDERS` and `CONNECTION_TESTED_PROVIDERS`,
  so this adds fields to an existing card rather than a new one: no `enabled_field`, and
  `test_admin_readiness.py`'s every-card-is-classified test is not affected.
- Watch the two silent fall-throughs if a separate `jev_decisions` card is ever added:
  `_configured` has no default branch and would report NAVITIME's readiness, and
  `_test_provider` would return `success` from its final line without calling anything.
