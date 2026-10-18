---
id: 2026-10-14-recognize-the-video-monthly-draft-cap
title: Recognize the video monthly draft cap in deploy verification
status: review
priority: P2
area: tools
owner: claude-opus-5-5-draft-cap
claimed_at: 2026-10-17T16:41:28Z
created_at: 2026-10-14T17:33:16Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-verify.sh
  - .agents/skills/deploy/references/post-deploy.md
  - tools/deploy-host-verify.test.mjs
  - tasks/open/2026-10-14-recognize-the-video-monthly-draft-cap.md
---

# Recognize the video monthly draft cap in deploy verification

## Why

The 2026-10-14 deployment of #1498 passed 11 host-verification checks, but the
video-worker-started check failed because the worker logged "本月已產生 40 支草稿，達到上限
40 支" followed by "video-worker: auto exited with 3". The container was running,
had zero restarts, and started after the deployed commit. This exit is the
owner-configured monthly draft cap, not a deployment regression: the video API
returns video_ai_budget_exhausted before a model call and the worker loop sleeps
before its next round. The verifier currently recognizes only the separate
AI-drama-disabled exit 4, so it labels this expected policy stop as a deployment
failure.

## Definition of done

- [x] The verifier reports the exact monthly-draft-cap message paired with the
      following auto exit 3 as an expected policy stop, while still showing it in
      the output.
- [x] An unpaired exit 3, any other nonzero auto exit, a stopped worker, or a
      restart remains a failed deploy check.
- [ ] The next applicable deployment verification can distinguish a healthy
      worker at its monthly limit from a broken worker without changing the cap.

## Steps

- [x] Confirm the current exit mapping and worker loop in video automation code.
- [x] Narrow the host verifier's log classification to the exact cap message
      and adjacent exit 3; retain all container and restart gates.
- [x] Add focused verification for the paired-cap case and negative cases.
      Widen scope to the actual test path before writing a test.

## How to verify

Run bash syntax validation and focused log-classification tests with paired and
unpaired exit 3 fixtures, then run npm run test:tools. On a host already at the
monthly cap, a read-only host verification should pass the worker-health gate
while visibly reporting the cap; it must still fail for an unrelated exit 3.

## Notes

The #1498 deploy reached live SHA e8d8a8fa18fc2974bab5aa4ada426eadb709fd8d,
returned DEPLOY_EXIT=0 and health 3/3, and loaded the new API code. The generic
host verifier returned TOTAL pass=11 fail=1 solely for video-worker-started.
Source scan recovery was independently verified. See
apps/api/app/video_automation/usage.py, tools/video/automation/client.mjs,
tools/video/automation/flow.mjs, tools/video/cli.mjs, and ops/video/worker.sh.

An unclaimed open task, 2026-10-07-autodeploy-rollout-and-skill-docs, has a broad
.agents/skills/deploy scope. Recheck task claims, worktrees, and open PRs before
claiming this ticket; its remaining work was host rollout at filing time.

### 2026-10-17 done in repo (claude-opus-5-5-draft-cap)

- Exit mapping confirmed: the cap is `video_ai_budget_exhausted` (an owner code in
  `tools/video/automation/client.mjs`), the CLI prints its message to stderr and returns
  `EXIT.owner` (3); `ops/video/worker.sh` then logs `video-worker: auto exited with 3`.
- `host-verify.sh` counts an exit 3 whose previous line (Shorts lines aside) carries
  「支草稿，達到上限」 apart as `auto_exit3_draft_cap`, prints a `NOTE` line when any, and keeps
  every other gate (state, restarts, start time, knock, pairing, every other exit). The token cap
  (「本月模型 token 已用…」) is a different message and still fails, as the ticket asked for the
  exact draft-cap message only.
- `tools/deploy-host-verify.test.mjs` reads the awk program out of the script and runs it on
  paired, unpaired, wrong-code, token-cap and mixed logs, and checks the octal strings spell the
  two messages. Removing the new branch makes two of its four tests fail.
- `post-deploy.md` explains the new field next to `auto_exit4_drama_off`.
- Left: the next deployment on a host at its cap shows the check passing with the `NOTE`.
