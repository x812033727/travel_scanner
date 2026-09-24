---
id: 2026-09-24-refresh-claude-plan-usage-automatically-from
title: Refresh Claude plan usage automatically and put all AI settings on one page
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-24T11:57:31Z
created_at: 2026-09-24T11:57:21Z
completed_at: 2026-09-24T15:43:02Z
branch: claude/ai-accounts-claude-usage-probe
depends_on: []
scope:
  - apps/api/ai_accounts_agent
  - apps/api/tests/test_ai_accounts_agent.py
  - apps/api/app/admin_ai_accounts/schemas.py
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_admin_operations.py
  - apps/web/app/[locale]/admin/ai-accounts
  - apps/web/app/[locale]/admin/settings/page.tsx
  - apps/web/components/admin-ai-accounts-panel.tsx
  - apps/web/components/admin-ai-accounts-panel.test.tsx
  - apps/web/components/admin-ai-settings.tsx
  - apps/web/components/admin-ai-settings.test.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/lib/admin-settings-ownership.ts
  - apps/web/lib/admin-settings-ownership.test.ts
  - apps/web/lib/admin-operations.ts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - tools/e2e-runtime-api.mjs
  - apps/web/e2e/admin-operations.spec.ts
  - apps/web/e2e/admin-operations-full-stack.spec.ts
  - ops/ai-accounts/README.md
---

# Refresh Claude plan usage automatically and put all AI settings on one page

## Why

After the rollout, the Claude cards said "use Claude once over SSH and the quota shows up". The
owner asked for that to happen on its own. They also found the AI settings scattered: the
subscription accounts on /admin/ai-accounts, and the site's AI keys and models in the AI category of
/admin/settings. They asked for one place. They also wanted to drop the API keys, but those power
the site's own AI features. Moving those features onto personal subscriptions breaks Anthropic's
and OpenAI's consumer terms, and fails whenever a window runs out; that day all three Codex accounts
were at 100 % weekly. So the keys stay, on the same page under their own tab.

Probed on the host on 2026-09-24 before writing any code:

- `claude -p ... --output-format stream-json` carries no rate-limit data. It only reports
  "You've hit your weekly limit" once the account is exhausted.
- An interactive session started with `--restricted --strict-mcp-config --model haiku --settings
  '{"statusLine":...}'` in a fixed folder gives the status line `rate_limits` about 2 s after start,
  with no message sent, for an account that has been used before. `--restricted` loads none of the
  owner's settings: no hooks, no push notifications, no Remote Control session.
- Accounts signed in with `claude auth login` never finished onboarding. Their first TUI start
  shows the theme picker and then the login picker, as if nobody were signed in. Setting
  `hasCompletedOnboarding` (plus `lastOnboardingVersion`) in their `.claude.json` fixes it.
- The folder trust prompt defaults to "No, exit", so it needs Down and then Enter.
- For those two fresh accounts, `rate_limits` only arrived after one short message. The numbers
  then matched the TUI's own "You've used 86% of your weekly limit".

## Definition of done

- [x] Opening the page, or pressing refresh, reads the usage of every signed-in Claude
      subscription account whose snapshot is missing or stale. The card shows "正在更新額度…" and
      the numbers appear without anyone using SSH.
- [x] Probes never load the owner's settings, never start a sign-in, and never touch API-billed
      accounts. They run at most once a minute per account on the button, and on page views only
      when the snapshot is older than 30 minutes.
- [x] /admin/ai-accounts is "AI 設定". Its "訂閱帳號" tab is for the owner only; its "API 金鑰與模型"
      tab holds the six AI-category provider cards. /admin/settings shows every other category plus
      a pointer, and old /admin/settings?provider=<AI card> links land on the new tab.
- [x] Anyone with settings.read reaches the page (the sidebar item moved from roles.manage to
      settings.read). The subscription routes stay owner only.

## Steps

- [x] Agent: `ClaudeAccounts.refresh_usage` (PTY, first-run screens, login-picker guard,
      one-message fallback), `mark_onboarding_done`, and background probes in `AgentApplication`
      with max-age, min-interval and retry rules. The status line recorder now prefers
      `CLAUDE_CONFIG_DIR` when it names the slot.
- [x] API: `usage_refreshing` in the slot schema. Registry capability is now settings.read.
- [x] Web: `AdminAiSettings` tabs, a `categories` filter on `AdminSettingsPanel`,
      `settingsHref` routing for AI providers, a redirect plus a notice on /admin/settings, the
      refreshing state and polling on the accounts panel, and messages in five languages.
- [x] Tests: probe flows with a fake interactive CLI (Linux), probe scheduling rules,
      onboarding marker, category filter and AI provider list parity, tabs by capability,
      ownership links, and refreshing UI.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_ai_accounts_agent.py tests/test_ai_accounts_admin.py tests/test_admin_operations.py
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-ai-accounts-panel.test.tsx components/admin-ai-settings.test.tsx components/admin-settings-panel.test.tsx lib/admin-settings-ownership.test.ts
```

After deploying, reinstall the agent on the host from the merged `main` (bundle, then
`install.sh`, which restarts the running service). Then open AI 設定 and watch the Claude cards
fill in.

## Notes

- Local runs: API 111 passed; the agent file passed 35 in WSL, including the three PTY probe
  tests; web 105 passed. The page was driven in the in-app browser against a mock.
- In a hidden Browser pane `requestAnimationFrame` never fires. The settings panel's deep-link
  selection runs in rAF, so a hidden pane always shows the first card. This happens on `main` too
  and is not a bug.
- Claude B and C on the host (s812, z812) had their onboarding marked and their usage read by hand
  during the probe work: B at 87 % weekly, C at 15 % weekly.
