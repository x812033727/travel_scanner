---
id: 2026-09-25-choose-every-ai-model-from-the
title: Choose every AI model from the AI settings page
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-25T13:34:12Z
created_at: 2026-09-25T13:33:49Z
completed_at: 2026-09-25T14:42:54Z
branch: claude/ai-models-in-ai-settings
depends_on: []
scope:
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/checking.py
  - apps/api/tests/test_news_automation_settings_models.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/web/app/[locale]/admin/settings/page.tsx
  - apps/web/components/admin-ai-model-overview.tsx
  - apps/web/components/admin-ai-model-overview.test.tsx
  - apps/web/components/admin-ai-settings.tsx
  - apps/web/components/admin-ai-settings.test.tsx
  - apps/web/components/admin-catalog-review-panel.tsx
  - apps/web/components/admin-catalog-review-panel.test.tsx
  - apps/web/components/admin-news-model-settings.tsx
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/components/admin-video-model-settings.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/e2e/admin-domains.spec.ts
  - apps/web/lib/admin-news-messages/en.json
  - apps/web/lib/admin-news-messages/ja.json
  - apps/web/lib/admin-news-messages/ko.json
  - apps/web/lib/admin-news-messages/zh-CN.json
  - apps/web/lib/admin-news-messages/zh-TW.json
  - apps/web/lib/admin-settings-copy.ts
  - apps/web/lib/admin-settings-ownership.ts
  - apps/web/lib/admin-settings-ownership.test.ts
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/hotspotAdmin.json
  - apps/web/messages/zh-CN/hotspotAdmin.json
  - apps/web/messages/en/hotspotAdmin.json
  - apps/web/messages/ja/hotspotAdmin.json
  - apps/web/messages/ko/hotspotAdmin.json
---

# Choose every AI model from the AI settings page

## Why

On 2026-09-25, after GPT-6 Sol became the default (#758), the owner found the planner still
ran GPT-5.6 Terra: the planner card had it saved. The model choices were spread over four
pages (AI settings for the planner and Gemini search, the hotspot settings tab for guide
search and introductions, `/admin/news` for the writer and verifier, `/admin/videos` for six
stages), so nobody could see at a glance what runs where. The owner asked for every model
choice in the AI settings page, each linked to its feature, each feature page linking back,
and for the features that can only run on an API key (not the subscription accounts) to be
marked.

## Definition of done

- [x] `/admin/ai-accounts` has a third tab, 「各功能模型」: a table of every feature's vendor
      and model (an empty choice resolved to the model it inherits), how it is paid for now,
      whether it can run on a subscription at all, and links to change it and to the feature.
- [x] Below the table, the planner, guide search, introduction and Gemini cards, then the news
      and video model editors. The 「API 金鑰」 tab keeps only the vendor keys and speech.
- [x] `/admin/news` and `/admin/videos` show their models read-only with a link to the new tab;
      the hotspot settings tab lists the guide search and introduction models read-only.
- [x] News and video models save through their own routes, and a settings save from the
      feature page cannot put back models it loaded earlier.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation_settings_models.py tests/test_video_automation_settings.py -q
npx vitest run components/admin-ai-model-overview.test.tsx components/admin-ai-settings.test.tsx   # in apps/web
```

After deploying: `/admin/ai-accounts?tab=models` lists twelve rows; changing the news writer
there shows up on `/admin/news?tab=settings` and in the table at once.

## Notes

- New routes: `PUT /admin/news/settings/models` (content.manage) and
  `PUT /admin/video-automation/settings/models` (settings.manage). The old `PUT /settings`
  routes keep a stored model when the payload leaves it out (news: `model_fields_set`; video:
  `SettingsSave` with an optional `stage_models`). A news model change is still a major change
  and returns every vertical to shadow mode; the editor says so.
- The subscription column reads `ai_vendors.config.anthropic_connection`, which PR #761 adds.
  Before #761 lands the column says every site feature is API-key only (true on main); after,
  it shows guide search, introductions and news as Claude-capable. The planner stays API-key
  only either way; video runs on the subscription only with Claude Code.
- `AdminSettingsPanel` gained `providers` (narrow the cards beyond `categories`) and
  `focusFirst` (do not scroll to the first card when nothing was linked; the models tab has the
  table above it).
- Same-page links must go through `adminNavigate`: a Next `<Link>` to the same route changes
  the URL without the admin location event, so the settings panel never switched cards.
- The in-app browser pane was hidden, so `requestAnimationFrame` never ran there and the card
  switch could not be seen; `admin-ai-settings.test.tsx` covers it in jsdom instead.
- Local Playwright could not run: `npm ci` moved Playwright past the installed browser build.
  CI runs `admin-domains.spec.ts`, whose redirect URL now names `tab=models`.
- Gemini and subscriptions: on 2026-09-25 the owner asked whether Gemini could use the
  Antigravity subscriptions (#760/#762) as well, and after the ban risk was laid out
  (Antigravity terms §6; Google banned paid accounts for routing its OAuth into other tools)
  chose to keep them for manual use on the host. Every row that runs on Gemini therefore says
  `geminiApiKeyOnly`. Do not wire the site's Gemini calls to `agy` without asking again.
- Open PR #763 adds a third news model (`editor_provider`/`editor_model`, the final editor) in
  the same news files. Whichever lands second must move it here too: add it to `ModelsWrite`,
  `SettingsWrite`'s kept-when-omitted keys, `AdminNewsModelSettings` and `overviewRows`.
- Production today (read 2026-09-25): the planner card has `openai_model = gpt-5.6-terra`
  saved, so it overrides the new GPT-6 Sol default until the owner changes it on the new tab.
