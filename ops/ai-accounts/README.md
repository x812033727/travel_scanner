# AI accounts agent

The owner runs Claude Code and the Codex CLI as root over SSH on the production host, billed
to their subscriptions rather than API keys. This agent lets `/admin/ai-accounts` sign those
CLIs in to up to five accounts per tool, pick the default one, and show each account's email,
plan and remaining quota. No CLI, token or credential file ever enters a container.

Like the deployment agent (`ops/deployer/`), it is a host-only systemd service that answers a
fixed set of HMAC-signed requests on a Unix socket, `/run/mokaair-ai-accounts/agent.sock`,
which the API container can open through the `travel-api` group. Requests name a tool
(`claude`, `codex`) and a slot (`a`–`e`); the only free text it accepts is the sign-in code
the owner pastes for Claude, limited to base64url characters and `#`.

## Where things live

| Path | What |
| --- | --- |
| `/var/lib/mokaair-ai-accounts/claude-a` … `claude-e` | One `CLAUDE_CONFIG_DIR` per account |
| `/var/lib/mokaair-ai-accounts/codex-a` … `codex-e` | One `CODEX_HOME` per account |
| `/var/lib/mokaair-ai-accounts/default-claude`, `default-codex` | The default slot letter |
| `/root/.claude`, `/root/.claude.json`, `/root/.codex` | Links to account A |
| `/opt/mokaair-ai-accounts/ai_accounts_agent` | The agent (copied from `apps/api`) |
| `/etc/travel-scanner/ai-accounts.env` | `AI_ACCOUNTS_AGENT_HMAC_KEY`, `AI_ACCOUNTS_ALLOWED_EMAILS` |
| `/usr/local/bin/claude-a` … `codex-e` | Run the CLI on one named account |
| `/etc/profile.d/mokaair-ai-accounts.sh` | `claude` and `codex` shell functions that use the default |

Accounts B–E link to A's `CLAUDE.md`, agents, commands, skills, plugins and `projects/`
(Claude) and `AGENTS.md`, prompts, skills and `sessions/` (Codex), so a new account behaves
the same and `--resume` finds every session. Each starts from a copy of A's `settings.json`
or `config.toml` and A's MCP servers.

## Using the accounts over SSH

- `claude` and `codex` in an interactive root shell use the default account. The account is
  chosen when the command starts, so a running session keeps its account when the default
  changes.
- `claude-b`, `codex-c` and so on always use that account, from any shell or script.
- Anything that runs `/root/.local/bin/claude` or `/usr/local/bin/codex` directly without
  the functions, such as cron, `nohup` or a non-interactive `ssh host cmd`, gets account A
  through the `/root` links.
- If the page cannot complete a login, for example after a CLI update changes its login
  screen, sign in on the host instead: `claude-b auth login` or `codex-b login --device-auth`.

## Quota

- **Codex:** read live from `codex app-server` (`account/rateLimits/read`) and cached for
  five minutes. Reading limits can refresh tokens, and doing that every minute next to an
  interactive session risks "refresh token already used". The page has a refresh button
  for a fresh read.
- **Claude:** Claude Code has no documented way to read plan usage outside a session. Its
  status line input carries `rate_limits.five_hour` and `seven_day` for Pro and Max
  accounts, so each account's status line runs `statusline-record claude-<slot>`. That
  records the latest numbers in `mokaair-usage.json` and prints a short line, or the
  owner's own status line command if one was configured before; that command is kept in
  `mokaair-statusline-chain.json`. The agent re-points the status line at the recorder
  whenever it starts, and after every login. A `statusLine` in a project's
  `.claude/settings.json` still overrides it for that project.
- **Claude, read automatically:** sessions over SSH keep the numbers current, and the agent
  fills the gaps itself. When the page is opened and an account's snapshot is missing or
  older than 30 minutes, when the refresh button is pressed (at most once a minute per
  account), and right after a login, it opens Claude Code once in a pseudo-terminal in
  `/var/lib/mokaair-ai-accounts/home/usage-probe`:
  - `--restricted` loads none of the owner's settings, so no hooks, push notifications or
    Remote Control session, and no tool that runs code. The recorder comes in through
    `--settings`, and `--model haiku` keeps the fallback cheap.
  - It answers the first-run screens it knows: the theme picker (Enter), notice pages
    (Enter) and the folder trust prompt (Down, Enter; the default is "No, exit"). It gives
    up at the login picker rather than start a sign-in.
  - Usage usually arrives within about 2 seconds, before any message. If nothing has
    arrived after 15 seconds, it sends one one-word message and waits up to 40 more.
  - An account signed in with `claude auth login` never finished onboarding, and the TUI
    then shows the login picker. The agent sets `hasCompletedOnboarding` (and
    `lastOnboardingVersion`) in that account's `.claude.json` after a login and before a
    probe, and changes nothing else in the file.
  - Accounts on API billing are never probed.

## Install

Before anything else, get the owner's approval: this changes root's CLI setup on the
production host.

1. Close every `claude` and `codex` session on the host. The installer refuses to move the
   logins while one is running.
2. Deploy a release that contains this directory, then run it from that checkout:

   ```bash
   bash ops/ai-accounts/install.sh --runtime-env /root/travel_scanner/.env
   ```

   `--runtime-env` writes the shared key and `AI_ACCOUNTS_ENABLED=true` into the app's
   runtime environment without printing them. Leave it out to copy the key by hand.
3. Put the owner's account emails in `AI_ACCOUNTS_ALLOWED_EMAILS` in
   `/etc/travel-scanner/ai-accounts.env`, comma-separated. If a login ends on any other
   account, it is signed out again at once. An empty list allows any account and the page
   warns about it.
4. `systemctl enable --now mokaair-ai-accounts`, then recreate the API container so it
   picks up the environment: `docker compose -f docker-compose.prod.yml up -d api` from
   `/root/travel_scanner`, or the next deploy.

## Check it

```bash
systemctl status mokaair-ai-accounts
# Unsigned requests are refused:
curl -s --unix-socket /run/mokaair-ai-accounts/agent.sock http://agent/v1/accounts
# A signed request lists every slot (emails masked):
set -a; . /etc/travel-scanner/ai-accounts.env; set +a
cd /opt/mokaair-ai-accounts && python3 -m ai_accounts_agent.client GET /v1/accounts
```

Then open `/admin/ai-accounts`. Account A should show the existing Claude and Codex logins.
Claude's quota appears after the next Claude session on the host has made its first request.

## Trust boundary

- The agent runs as root with an empty capability set, `ProtectSystem=strict`, and write
  access only to its state and socket directories. It starts nothing but the two CLIs,
  with fixed arguments and an environment built from scratch, so the HMAC key never
  reaches them.
- Anyone holding `AI_ACCOUNTS_AGENT_HMAC_KEY` and the `travel-api` group can start and
  cancel logins, sign accounts out and change the default. They cannot sign root's CLIs
  in to an account of their own while `AI_ACCOUNTS_ALLOWED_EMAILS` is set. Treat the key
  like the deployment agent's.
- The page never receives a token. It sees emails, plans, quota percentages, the sign-in
  URL and the Codex device code, and the last two only while a login is open.

## Undo

```bash
systemctl disable --now mokaair-ai-accounts
rm /root/.claude /root/.claude.json /root/.codex   # the links, not the accounts
mv /var/lib/mokaair-ai-accounts/claude-a/.claude.json /root/.claude.json
mv /var/lib/mokaair-ai-accounts/claude-a /root/.claude
mv /var/lib/mokaair-ai-accounts/codex-a /root/.codex
rm /etc/profile.d/mokaair-ai-accounts.sh /usr/local/bin/claude-? /usr/local/bin/codex-?
```

Remove the `# mokaair-ai-accounts` line from `/root/.bashrc`, and `statusLine` from
`/root/.claude/settings.json`, if the recorder is no longer wanted.
