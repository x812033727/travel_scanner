---
id: 2026-09-26-rotate-subscription-accounts-only-when-full
title: Rotate subscription accounts only when full, with no usage cap setting
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-26T05:23:29Z
created_at: 2026-09-26T05:20:00Z
completed_at: 2026-09-26T05:23:32Z
branch: claude/subscription-rotate-when-full
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/app/ai/subscription.py
  - apps/api/app/config.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_ai_subscription.py
  - apps/api/tests/test_video_automation_subscription.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - docs/news-automation.md
  - docs/videos/AUTOMATION.md
  - ops/ai-accounts/README.md
---

# Rotate subscription accounts only when full, with no usage cap setting

## Why

On 2026-09-26 the owner asked why their Claude quota never dropped. The site was using the
subscription accounts (news had made 100+ Claude calls since 03:50 UTC), but on B and C:
`current-claude` was C and A sat at 0%. The owner then asked to drop the usage cap settings and
simply use each account until it is full, in turn A -> B -> C -> ... -> A.

Two caps existed: 「訂閱帳號用量上限（%）」 on the AI vendors card
(`ai_subscription_max_usage_percent`, default 80, production had 100) and 「訂閱帳號用到幾 %
就先停」 on the video settings (`subscription_max_usage_percent`, default 80).

## Definition of done

- [x] Neither cap appears in the admin; the site always asks the host agent for runs up to
      100%, so an account keeps the runs until its 5-hour or weekly window is full.
- [x] The rotation is the agent's existing slot order (A, B, C, D, E, back to A), described
      that way in the card help, the video settings help and the docs.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_subscription.py tests/test_video_automation_subscription.py tests/test_admin_provider_settings.py -q
```

After deploying: the AI vendors card on `/admin/ai-accounts?tab=api` shows 「Claude 連線方式」
without a cap field, and the video settings budget section has no percentage field.

## Notes

- The host agent is unchanged (another session is working in `ai_accounts_agent/`): its
  `pick_slot` already walks `rotation(current)` in slot order and passes over an account whose
  peak is at or above the caller's cap, or that a run just reported as limited. The site now
  sends `FULL_PERCENT = 100` (`app/ai/subscription.py`) from news and video.
- Stored values are ignored, not migrated: `apply_runtime_overrides` reads only a card's
  `config_fields`, so the `ai_subscription_max_usage_percent` saved on production's
  `ai_vendors` row is inert; the video column `subscription_max_usage_percent` stays (no
  migration) and is no longer read.
- The turn does not reset to A: the account whose turn it is keeps the runs until it is full.
  On 2026-09-26 that was C, so the order from there is C -> D/E if signed in -> A -> B.
