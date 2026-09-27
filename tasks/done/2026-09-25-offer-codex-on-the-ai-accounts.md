---
id: 2026-09-25-offer-codex-on-the-ai-accounts
title: Offer Codex on the AI accounts agent's prompt runs once a shell-free run is proven
status: done
priority: P2
area: ops
owner: codex-codex-subscription
claimed_at: 2026-09-27T11:48:09Z
created_at: 2026-09-25T13:07:39Z
completed_at: 2026-09-27T12:21:08Z
branch: codex/codex-subscription-settings
depends_on:
  - 2026-09-25-run-the-site-s-claude-features
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/app/ai/subscription.py
  - apps/api/app/admin_ai_accounts/agent.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_ai_subscription.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/subscription.py
  - apps/api/app/video_automation/usage.py
  - apps/api/tests/test_video_automation_subscription.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-model-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/components/admin-ai-model-overview.tsx
  - apps/web/components/admin-ai-model-overview.test.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - ops/ai-accounts/README.md
  - .agents/skills/prod-host-ops/references/ai-accounts.md
---

# Offer Codex on the AI accounts agent's prompt runs once a shell-free run is proven

## Why

On 2026-09-25 the owner asked for both Claude and Codex to run on their subscription
accounts instead of API keys. Only Claude could be done. `POST /v1/runs` refuses Codex
because `codex exec` keeps a shell, and its read-only sandbox still reads the site's `.env`
and every account's credentials. The prompt carries untrusted web pages, so a model that can
run a command is an injection path to those secrets, which would come back out in a news
draft.

Codex 0.156.1 on the host lists features that `--disable` can turn off: `shell_tool`,
`unified_exec`, `shell_snapshot`, `apps`, `plugins`, `browser_use`, `browser_use_external`,
`computer_use`, `in_app_browser`, `image_generation`, `multi_agent` and `hooks`. With the
first two off, the model may have no shell at all. That could not be tried on 2026-09-25:
every Codex account was at 100% of its weekly window until 9/27–9/30.

## Definition of done

- [x] On the host, a `codex exec` run with the flags below cannot read `/etc/hostname` or run
      `id` when the prompt asks it to, and still returns the schema's JSON.
- [x] `POST /v1/runs` accepts `tool: "codex"` with exactly those flags, picks among signed-in
      Codex accounts the way `pick_slot` does for Claude, and reads the answer and token
      usage from the JSONL.
- [x] The AI vendors card gets `openai_connection` (API key / Codex subscription), owner only,
      and `research_provider("openai")` routes through it with the MiniMax fallback.
- [x] The video writing stages also offer Codex subscription accounts beside Claude Code,
      and record their plan usage separately from API-billed tokens.

## Steps

- [x] Try on the host (it spends a little Codex quota):
      `codex exec - --json --ephemeral --skip-git-repo-check --ignore-user-config --ignore-rules -s read-only -C <empty dir> -m gpt-6-sol --output-schema <file> --color never --disable shell_tool --disable unified_exec --disable shell_snapshot --disable apps --disable plugins --disable browser_use --disable browser_use_external --disable computer_use --disable in_app_browser --disable image_generation --disable multi_agent --disable hooks`,
      plus whichever `-c` key turns web search off in this version (`web_search="disabled"`
      or `tools.web_search=false`; check `codex exec --help` and the config reference). Web
      search runs on OpenAI's side and could send page text out in a query.
- [x] Look at the JSONL tool list or `turn.completed` events and confirm no shell,
      `apply_patch`, `view_image` or `read_file`-style tool was offered.
- [x] Only then write the agent code and its fake-CLI tests, as for Claude.

## How to verify

The injection prompt fails on the host, and `/admin/settings` → AI vendors → 測試連線 lists
a Codex account as usable.

## Notes

- The Codex models in the host's models_cache on 2026-09-24: gpt-6-astra, gpt-6-sol,
  gpt-6-luna, gpt-5.6-sol/terra/luna, gpt-5.5.
- Defence in depth that helps both tools: `InaccessiblePaths=-/root/travel_scanner
  -/etc/travel-scanner -/root/.ssh` on the agent's systemd unit. The agent reads its env file
  before start and needs none of those paths. That is a host change, so the owner approves it.
- 2026-09-27: owner explicitly approved one isolated production-host Codex test using a small
  amount of subscription quota, without changing live settings. On host Codex CLI 0.156.1,
  slot A had room. `codex exec` with the flags in Steps plus `--strict-config` and
  `-c 'web_search="disabled"' -c 'tools.web_search=false'` exited 0 and returned schema JSON
  `{ "command_result": "UNAVAILABLE", "file_result": "UNAVAILABLE" }` when asked to run `id`
  and read `/etc/hostname`. Its JSONL held only two `agent_message` items and no tool-call
  items. The summary wrapper printed this evidence, then hit a here-doc terminator error; the
  CLI result and parsed events were already complete. Temporary probe directory was removed.
- The agent checks for the verified `codex-cli 0.156.1` before every Codex run. A later CLI
  version must repeat the isolated shell/file test before the pin is changed.
- Local checks: 159 focused API tests passed; 41 video/agent tests passed with 1 skipped;
  75 admin web tests passed; API ruff and app mypy, web lint and typecheck, five-locale i18n,
  and task-board validation passed. Windows `mypy tests` still reports the existing
  `socketserver.UnixStreamServer` typing error in `tests/support/e2e_deploy_agent.py`;
  five touched test files pass mypy separately. The full Windows `test:tools` command had
  17 video tool files fail to start without assertion output, outside this scope.
- The production `/admin/settings` connection card and real video stages have not been
  exercised because the owner approved only the isolated CLI test, not a deployment.
