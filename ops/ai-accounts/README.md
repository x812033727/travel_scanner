# AI accounts agent

The owner runs Claude Code, the Codex CLI and Google's Antigravity CLI (`agy`) as root over
SSH on the production host, billed to their subscriptions rather than API keys. This agent lets `/admin/ai-accounts` sign those
CLIs in to up to five accounts per tool, pick the default one, and show each account's email,
plan and remaining quota. No CLI, token or credential file ever enters a container.

Like the deployment agent (`ops/deployer/`), it is a host-only systemd service that answers a
fixed set of HMAC-signed requests on a Unix socket, `/run/mokaair-ai-accounts/agent.sock`,
which the API container can open through the `travel-api` group. Requests name a tool
(`claude`, `codex`, `agy`) and a slot (`a`–`e`); the only free text it accepts is the sign-in
code the owner pastes for Claude or Antigravity, limited to base64url characters, `#` (Claude)
and `/` (Google).

## Where things live

| Path | What |
| --- | --- |
| `/var/lib/mokaair-ai-accounts/claude-a` … `claude-e` | One `CLAUDE_CONFIG_DIR` per account |
| `/var/lib/mokaair-ai-accounts/codex-a` … `codex-e` | One `CODEX_HOME` per account |
| `/var/lib/mokaair-ai-accounts/agy-a` … `agy-e` | One `HOME` per Antigravity account |
| `/var/lib/mokaair-ai-accounts/default-claude`, `default-codex`, `default-agy` | The default slot letter |
| `/root/.claude`, `/root/.claude.json`, `/root/.codex`, `/root/.gemini/antigravity-cli` | Links to account A |
| `/opt/mokaair-ai-accounts/ai_accounts_agent` | The agent (copied from `apps/api`) |
| `/etc/travel-scanner/ai-accounts.env` | `AI_ACCOUNTS_AGENT_HMAC_KEY`, `AI_ACCOUNTS_ALLOWED_EMAILS` |
| `/usr/local/bin/claude-a` … `agy-e` | Run the CLI on one named account |
| `/etc/profile.d/mokaair-ai-accounts.sh` | `claude`, `codex` and `agy` shell functions that use the default |

Accounts B–E link to A's `CLAUDE.md`, agents, commands, skills, plugins and `projects/`
(Claude) and `AGENTS.md`, prompts, skills and `sessions/` (Codex), so a new account behaves
the same and `--resume` finds every session. Each starts from a copy of A's `settings.json`
or `config.toml` and A's MCP servers.

Antigravity is different because `agy` has no switch for its data folder: it always uses
`~/.gemini/antigravity-cli`. So each account is a home of its own, and `agy-b` runs with
`HOME=/var/lib/mokaair-ai-accounts/agy-b`. Inside agy, `~` is that folder, not `/root`:
`.gitconfig`, `.git-credentials`, `.npmrc` and `.config/gh` are linked back to `/root`, ssh
finds `/root/.ssh` by itself, and accounts B–E share A's `.gemini/config` (MCP servers).
The session bus points at nothing (`DBUS_SESSION_BUS_ADDRESS=unix:path=/dev/null/…`): a
keyring would hold one login for every account, and without one agy keeps each login in
`~/.gemini/antigravity-cli/jetski-standalone-oauth-token`.

## Using the accounts over SSH

- `claude`, `codex` and `agy` in an interactive root shell use the default account. The account is
  chosen when the command starts, so a running session keeps its account when the default
  changes.
- `claude-b`, `codex-c`, `agy-d` and so on always use that account, from any shell or script.
- Anything that runs `/root/.local/bin/claude`, `/usr/local/bin/codex` or
  `/root/.local/bin/agy` directly without the functions, such as cron, `nohup` or a
  non-interactive `ssh host cmd`, gets account A through the `/root` links.
- If the page cannot complete a login, for example after a CLI update changes its login
  screen, sign in on the host instead: `claude-b auth login`, `codex-b login --device-auth`,
  or `agy-b` and pick Google OAuth.
- The first time an Antigravity account starts, agy may show first-run pages (terms, colour
  scheme). The agent never answers those for the owner; run `agy-<slot>` once over SSH.

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
- **Antigravity:** agy shows quota only on its TUI's "Models & Quota" page (`/usage`), which
  asks Google and draws groups of buckets with the share left and when each refreshes.
  (`agy -p /usage` was reported to send the text to the model as a prompt.) On the same
  schedule as Claude (page view when older than 30 minutes, the refresh button, after a
  login), the agent opens `agy` once in `/var/lib/mokaair-ai-accounts/home/agy-usage-probe`,
  waits for the TUI to settle, types `/usage`, reads the page through a small terminal
  emulator (`screen.py`) and records the windows in the account's `mokaair-usage.json`.
  `/usage` calls no model. The probe gives up, and says why on the page, at the login
  picker (`signed_out`), at a first-run page (`setup_needed`), or when it finds no quota
  rows (`unreadable`); in the last case it writes the page it saw, emails masked, to the
  journal (`journalctl -u mokaair-ai-accounts`) so the parser can follow a layout change.
- **Antigravity sign-in and email:** the TUI opens on "Select login method"; the agent
  picks Google OAuth, hands the `accounts.google.com` URL to the page, types the code the
  owner pastes, and takes the saved token file as success. agy has no status command, so
  the email comes from its log line "OAuth: authenticated successfully as …" and the plan
  from the TUI header. With an allowlist set, a login whose email cannot be read is signed
  out again.
- **Antigravity terms:** they forbid using the service with products Google does not
  provide, and Google suspended paid accounts in 2026-02 and 2026-09 for routing its OAuth
  into other tools. The agent only drives the official binary and never reads the token or
  calls Google with it; `/v1/runs` does not offer Antigravity.

## Install

Before anything else, get the owner's approval: this changes root's CLI setup on the
production host.

1. Close every `claude`, `codex` and `agy` session on the host. The installer refuses to
   move the logins while one is running. agy itself is installed separately, as a single
   verified binary at `/root/.local/bin/agy` (see the rollout ticket); its installer's
   `agy install` step, which edits shell rc files, is not needed.
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

## Prompt runs

`POST /v1/runs` (`ai_accounts_agent/runs.py`) runs one prompt through `claude -p` with every
tool turned off, on the signed-in Claude subscription account with the most room below the
caller's usage cap. The video pipeline uses it (#756). Since 2026-09-25, when the owner sets
「Claude 連線方式」 on the AI vendors card to 訂閱帳號, every other site feature that calls
Claude uses it too (`apps/api/app/ai/subscription.py`): guide search, introductions,
introduction review, Simplified names and the news stages. The trip planner and the trip
text parser do not; a reader cannot wait for a CLI.

- Each account runs one prompt at a time. Runs on different accounts go side by side, and
  a request waits up to its `queue_seconds` for a busy account before it is refused as
  `subscription_busy`.
- A run that hits a usage limit rests that account for 30 minutes and moves on to the next
  one. When every account is at the cap, the answer is `subscription_quota_paused`, and the
  site falls back to MiniMax if it has the key.
- Codex is not offered. `codex exec` has no switch that removes its shell, and its read-only
  sandbox still reads the site's `.env`.

## Trust boundary

- The agent runs as root with an empty capability set, `ProtectSystem=strict`, and write
  access only to its state and socket directories. It starts nothing but the three CLIs,
  with fixed arguments and an environment built from scratch, so the HMAC key never
  reaches them.
- Anyone holding `AI_ACCOUNTS_AGENT_HMAC_KEY` and the `travel-api` group can start and
  cancel logins, sign accounts out and change the default. They cannot sign root's CLIs
  in to an account of their own while `AI_ACCOUNTS_ALLOWED_EMAILS` is set. Treat the key
  like the deployment agent's.
- The API, worker and news-worker containers mount the socket, because all three run
  prompts. A prompt can spend quota on the owner's accounts but can do nothing on the host:
  Claude Code runs with no tools, in an empty folder, with a fresh environment.
- The page never receives a token. It sees emails, plans, quota percentages, the sign-in
  URL and the Codex device code, and the last two only while a login is open.

## Undo

```bash
systemctl disable --now mokaair-ai-accounts
rm /root/.claude /root/.claude.json /root/.codex /root/.gemini/antigravity-cli   # links
mv /var/lib/mokaair-ai-accounts/claude-a/.claude.json /root/.claude.json
mv /var/lib/mokaair-ai-accounts/claude-a /root/.claude
mv /var/lib/mokaair-ai-accounts/codex-a /root/.codex
mv /var/lib/mokaair-ai-accounts/agy-a/.gemini/antigravity-cli /root/.gemini/antigravity-cli
rm /etc/profile.d/mokaair-ai-accounts.sh /usr/local/bin/claude-? /usr/local/bin/codex-? \
  /usr/local/bin/agy-?
```

Remove the `# mokaair-ai-accounts` line from `/root/.bashrc`, and `statusLine` from
`/root/.claude/settings.json`, if the recorder is no longer wanted.
