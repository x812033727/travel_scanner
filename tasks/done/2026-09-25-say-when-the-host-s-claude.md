---
id: 2026-09-25-say-when-the-host-s-claude
title: Say when the host's Claude Code is too old for the model a video stage names
status: done
priority: P2
area: api
owner: codex-gpt6-cli
claimed_at: 2026-09-30T02:30:27Z
created_at: 2026-09-25T12:50:45Z
completed_at: 2026-09-30T02:39:14Z
branch: codex/claude-cli-outdated
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/app/video_automation/subscription.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_video_automation_subscription.py
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
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

- [x] A run refused because the CLI is too old returns its own code (for example
      `subscription_cli_outdated`, 409). The code carries the installed and the required version.
- [x] The video pipeline treats that code as the owner's to fix. It shows the message and does
      not retry: the message says to run `claude update` on the host.
- [ ] Optional: the model dropdowns on /admin/videos show which Claude Code version is installed.

## Steps

- [x] Match the CLI's message in `runs.py` (next to `LIMIT_MESSAGE`) and raise `RunRefused`.
- [x] Map the new code in `app/video_automation/subscription.py` to an owner error, and add it
      to `OWNER_CODES` in `tools/video/automation/client.mjs`. That means adding
      `tools/video/automation/client.mjs` to this ticket's scope.

## How to verify

Put a fake CLI in `tests` that prints the 2.1.259 message. The agent should answer 409 with
the new code, and `auto` should exit with the owner's code after one call.

## Notes

- 2026-09-30 collision audit: no open PR touches the implementation or chosen
  test paths. The old withdrawal review claim overlaps the subscription directory,
  but its PR #870 (79e26fcd) is already on main and its branch is absent. Used
  claim --force only for that stale overlap; left the other owner's record alone.
- Add a separate client test file rather than editing automation.test.mjs, which
  currently belongs to PR #999/#1000. Match version refusal text only when the
  CLI reports failure, so a successful model answer quoting the notice stays valid.
- Implemented agent HTTP 409 `subscription_cli_outdated` with structured installed
  and required versions and fixed `claude update` guidance. Recognizes failed JSON
  result, stderr, and non-JSON stdout; does not echo surrounding CLI output.
- The API maps this to `video_ai_subscription_cli_outdated`; `auto` exits 3 after
  one stage request without backoff or account rotation. A failed zero-token run
  remains visible in the stage history. Updating the executable permits the same
  agent/account to run again without restarting the agent.
- Optional admin dropdown version display is deferred: it is not needed to make
  this refusal actionable, and no admin UI paths are part of this ticket's scope.
- Validation: 56 focused Python tests passed, including executable-update
  recovery. Eight worker/client CLI tests passed,
  including red/green coverage for the owner exit and a generic-failure retry
  regression. Full tool suite: 880 passed, 2 platform skips. Full API Ruff,
  mypy app (444 files), mypy tests (333 files), focused agent mypy, and
  check:tasks passed. Full service integration remains CI validation. No host
  CLI or live settings were changed and no real model requests were made.
- Repeated pre-PR collision audit at main bf41ae84: 15 open PRs and 177
  accessible worktrees have no overlapping changes outside this worktree.
- Rebased onto main 444d52af after PR creation; all 56 focused Python tests and
  the full tool suite passed again on the updated base.

The worker logged "claude run failed: API Error: 400 Claude Code 2.1.259 does not support this
model; …", so the message went through the `CliError` branch at the end of `run_claude`. It is
not known whether it arrived in the JSON result text or on stderr, so match both.
