---
id: 2026-09-25-offer-codex-on-the-ai-accounts
title: Offer Codex on the AI accounts agent's prompt runs once a shell-free run is proven
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-25T13:07:39Z
completed_at:
branch:
depends_on:
  - 2026-09-25-run-the-site-s-claude-features
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/app/ai/subscription.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_ai_subscription.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - ops/ai-accounts/README.md
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

- [ ] On the host, a `codex exec` run with the flags below cannot read `/etc/hostname` or run
      `id` when the prompt asks it to, and still returns the schema's JSON.
- [ ] `POST /v1/runs` accepts `tool: "codex"` with exactly those flags, picks among signed-in
      Codex accounts the way `pick_slot` does for Claude, and reads the answer and token
      usage from the JSONL.
- [ ] The AI vendors card gets `openai_connection` (API key / Codex subscription), owner only,
      and `research_provider("openai")` routes through it with the MiniMax fallback.

## Steps

- [ ] Try on the host (it spends a little Codex quota):
      `codex exec - --json --ephemeral --skip-git-repo-check --ignore-user-config --ignore-rules -s read-only -C <empty dir> -m gpt-6-sol --output-schema <file> --color never --disable shell_tool --disable unified_exec --disable shell_snapshot --disable apps --disable plugins --disable browser_use --disable browser_use_external --disable computer_use --disable in_app_browser --disable image_generation --disable multi_agent --disable hooks`,
      plus whichever `-c` key turns web search off in this version (`web_search="disabled"`
      or `tools.web_search=false`; check `codex exec --help` and the config reference). Web
      search runs on OpenAI's side and could send page text out in a query.
- [ ] Look at the JSONL tool list or `turn.completed` events and confirm no shell,
      `apply_patch`, `view_image` or `read_file`-style tool was offered.
- [ ] Only then write the agent code and its fake-CLI tests, as for Claude.

## How to verify

The injection prompt fails on the host, and `/admin/settings` → AI vendors → 測試連線 lists
a Codex account as usable.

## Notes

- The Codex models in the host's models_cache on 2026-09-24: gpt-6-astra, gpt-6-sol,
  gpt-6-luna, gpt-5.6-sol/terra/luna, gpt-5.5.
- Defence in depth that helps both tools: `InaccessiblePaths=-/root/travel_scanner
  -/etc/travel-scanner -/root/.ssh` on the agent's systemd unit. The agent reads its env file
  before start and needs none of those paths. That is a host change, so the owner approves it.
