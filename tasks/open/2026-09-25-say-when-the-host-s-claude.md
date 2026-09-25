---
id: 2026-09-25-say-when-the-host-s-claude
title: Say when the host's Claude Code is too old for the model a video stage names
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-25T12:50:45Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/app/video_automation/subscription.py
---

# Say when the host's Claude Code is too old for the model a video stage names

## Why

On 2026-09-25 the owner set every video stage to Claude Opus 5.5. The first automatic run then
failed four times in 40 seconds. The host still had Claude Code 2.1.259, installed on 2026-09-02,
and the CLI answered:
"API Error: 400 Claude Code 2.1.259 does not support this model; version 2.1.280 or newer is
required."

`ai_accounts_agent.runs.run_claude` turns any failed run into `subscription_run_failed` (502).
The API maps that to `video_ai_upstream_failed`, which the worker retries as if the vendor were
busy. In the end the owner learns about it only from the worker's log. `claude update` fixed it
(2.1.282), and it will happen again with the next new model.

## Definition of done

- [ ] A run refused because the CLI is too old returns its own code (for example
      `subscription_cli_outdated`, 409). The code carries the installed and the required version.
- [ ] The video pipeline treats that code as the owner's to fix. It shows the message and does
      not retry: the message says to run `claude update` on the host.
- [ ] Optional: the model dropdowns on /admin/videos show which Claude Code version is installed.

## Steps

- [ ] Match the CLI's message in `runs.py` (next to `LIMIT_MESSAGE`) and raise `RunRefused`.
- [ ] Map the new code in `app/video_automation/subscription.py` to an owner error, and add it
      to `OWNER_CODES` in `tools/video/automation/client.mjs`. That means adding
      `tools/video/automation/client.mjs` to this ticket's scope.

## How to verify

Put a fake CLI in `tests` that prints the 2.1.259 message. The agent should answer 409 with
the new code, and `auto` should exit with the owner's code after one call.

## Notes

The worker logged "claude run failed: API Error: 400 Claude Code 2.1.259 does not support this
model; …", so the message went through the `CliError` branch at the end of `run_claude`. It is
not known whether it arrived in the JSON result text or on stderr, so match both.
