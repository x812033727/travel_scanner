---
id: 2026-10-26-persist-keyframe-take-verdicts-before-network
title: Persist keyframe take verdicts before network recovery
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-26T16:13:33Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/keyframes.test.mjs
---

# Persist keyframe take verdicts before network recovery

## Why

During Curio S31 v2 production on 2026-10-27 Taipei time, an ECONNRESET while reading the second image result terminated the CLI after take1's judge had returned a failed verdict and corrective wording. That verdict was not durable at the scene boundary. A normal same-command resume judged take1 again, obtained different corrective wording, and generated a different take2 request key while the already-submitted original take2 remained in media/jobs.json. This can strand a paid reservation and buy another image even though the original result exists.

## Definition of done

- [ ] Every completed take, its exact judge verdict/stamp and corrective wording survive a subsequent download or transport failure.
- [ ] Resuming the same source reuses that evidence and the existing in-flight job; no extra judge call or replacement generation is sent merely because the process stopped.
- [ ] A regression covers a connection reset between take1 judgment and take2 download with a deliberately different second judge response.

## Steps

- [ ] Check existing ownership and main/PR fixes before claiming the narrow tooling scope.
- [ ] Persist resumable per-take evidence atomically while retaining script/context binding and uncertain-job safeguards.
- [ ] Verify partial scene state cannot approve a storyboard before all selected images are valid.

## How to verify

Use mocked media/transport calls: fail take1 with fixA, submit take2, reset its download, and resume with a mock judge that would return fixB. Assert the resumed run never asks that judge again for the same bound take and never submits an image using fixB. The original job must be polled/downloaded and its existing reservation reconciled. Run the targeted keyframes tests and check:tasks; no paid or production requests are needed for the regression.

## Notes

The current video task does not claim or modify this tooling scope. Evidence is retained outside the repo in `~/mokaair-work/curio-s31-v2-preflight/`: `keyframes-production-r6.txt`, `keyframes-resume-r6.txt`, and `connection-reset-r6/{jobs,ledger,reconciled-job}.json`.

Original stranded key `f468efef0fa55ae3` / job `b9b0803a-1be7-4d27-b6b6-f6c44c4c4c70` was separately reconciled without any generation submission: status ready, US$0.0035, image SHA-256 `81511ca76f23c802da4c4acc6652b9ffa200d69230a1af8af40284981c28dff2`. Its bytes were downloaded and hash-verified into the recovery receipt directory. Do not erase a pending job or replay its submission to reproduce this issue.
