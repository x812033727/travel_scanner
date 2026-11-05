---
id: 2026-10-31-make-the-video-worker-s-verifier
title: Make the video worker's verifier a durable stage
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-31T02:52:16Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/flow.mjs
---

# Make the video worker's verifier a durable stage

## Why

The worker asks the server for the verifier (the fact check, and the storytelling panel, which
runs under the same stage name) over the synchronous route, which the web relay cuts at about
295 s. On 2026-10-31 at 09:51 Taipei, `daily-ai-20261030`'s verifier got HTTP 504 ("no answer
within the deadline") while the one-consumer `video-ai` queue was busy with `daily-ai-20261029`'s
translations. The worker cannot tell whether the model ran and was paid for, so the video stopped
as uncertain until the owner pressed 重試. The writer, translator and caption reviewer avoid this:
they are durable jobs (`DURABLE_STAGES` in `tools/video/automation/client.mjs`) whose receipts
the worker looks up again instead of guessing.

## Definition of done

- [ ] A verifier request outlasting the relay deadline does not stop the video for the owner; the
      worker takes its saved receipt on a later look-up, without paying for a second run.

## Steps

- [ ] Check whether the server's durable route (`apps/api/app/video_automation/run_jobs.py`)
      already accepts the verifier stage and its variants (`narrative`, `recap`, `episode`),
      and what its job timeout allows.
- [ ] Add the verifier to the durable stages in `client.mjs`, keeping the request bodies stable
      across rounds so the same receipt is found (as `narrativeGate` does with `fix_note`).
- [ ] Tests in `client.test.mjs` and `automation.test.mjs` in the style of the translator's.

## How to verify

`node --test tools/video/automation/client.test.mjs tools/video/automation/automation.test.mjs`;
on the host, a brief's verifier that runs past five minutes shows `verifier is still running`
in the worker log instead of a block.

## Notes

- The in-run wait for durable jobs (2026-10-31, `DURABLE_WAIT_MS` in
  `tools/video/automation/cli.mjs`) applies to the verifier as soon as it is durable.
- The panel's two-reader merge (curio) sends two payloads; each needs its own request key.
