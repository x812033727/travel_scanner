---
id: 2026-10-04-video-keyframe-storyboard-completeness
title: Require every expected keyframe before storyboard approval
status: in-progress
priority: P1
area: tools
owner: codex-video-recovery-20261004
claimed_at: 2026-10-04T06:01:51Z
created_at: 2026-10-04T05:49:29Z
completed_at:
branch: codex/video-pipeline-recovery-20261004
depends_on: []
scope:
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_reviews_integration.py
  - tools/video/automation/automation.test.mjs
---

# Require every expected keyframe before storyboard approval

## Why

Three illustrated slide videos reached automatic storyboard approval and rendered their
cards while their current keyframe manifests still lacked required pictures. Assembly was
the first stage to reject the incomplete set. The read-only production audit on
2026-10-04 found the following sequence in the worker log:

1. Keyframe production stopped at the US$20 per-video cap: Grok had spent US$25.21,
   SEC US$20.03 and Cloudflare Registrar US$20.17; another picture was estimated at US$0.10.
2. After later retries, the worker submitted their storyboards and the backend automatically
   approved the supplied shots under the configured judge rule.
3. The worker printed `frames rendered`.
4. Assembly refused `keyframes/manifest.json has no picture for ...; run keyframes first`:
   `grok-4-7-bedrock-output-doubles` lacked 16 pictures,
   `sec-ai-trading-bot-whatsapp-scam` lacked 18, and
   `cloudflare-registrar-renewal-price-ai-agent` lacked 12.

This is an integrity gap between pipeline status, storyboard submission and assembly,
not evidence that complete pictures failed their judge. Matching manifest hashes and
passing verdicts on the pictures already present do not prove every expected shot exists.
The resulting retry changes the reported failure from a generation cap to missing
assembly inputs without finishing the missing media.

## Definition of done

- [ ] A current partial keyframe manifest never counts as `keyframes drawn`: every expected
      shot must have its required selected picture, no incomplete/needs-review entry, and
      the required file/evidence must still exist. Cover applicable end-frame requirements.
- [ ] Storyboard submission reports or refuses missing expected shot IDs instead of silently
      dropping them from the review. A previously approved partial manifest cannot bypass
      the completeness requirement on resume.
- [ ] Automatic storyboard approval requires a complete expected set as well as passing
      quality checks; tests reject omitted, duplicate, missing-file and incomplete entries.
      Preserve existing hash binding and do not invent evidence for legacy submissions.
- [ ] An interrupted or capped keyframe generation preserves reusable completed pictures
      while visibly remaining incomplete. A resumed worker returns to missing keyframes
      before storyboard, rendering or assembly, and does not re-buy unchanged accepted takes.
- [ ] Disabled media settings and the owner's spending cap remain enforced. In particular,
      `drama_enabled=false` and `slides_media_enabled=false` must not generate or pay for
      replacement media; stop with the actual settings/cap reason, retaining partial work.
- [ ] A genuinely complete storyboard still advances; ordinary slides, dramas, still shots,
      contact-sheet pagination and externally imported media retain their intended contracts.

## Steps

- [x] Read-only audit: compare backend project state, persisted worker state and worker logs.
- [x] Trace coverage checks and search open/done tasks for an existing exact issue.
- [ ] Add focused regressions for a matching-hash partial manifest and its approved review.
- [ ] Enforce the expected keyframe set consistently at status and storyboard boundaries.
- [ ] Verify interrupted/capped resume and disabled-media behavior without paid requests.
- [ ] Run focused checks and the required repository validation before a PR.

## How to verify

Implemented full expected-picture/start/end coverage with current disk hashes at
status, submission and pull boundaries. Backend auto-approval requires coverage
evidence; old payloads without it remain manual review. A cap during end-frame
generation now saves the reusable start picture before stopping, and a resume
does not rebuy an accepted take. Focused state/sync regression tests: 15 passed;
full look-keyframes: 29 passed; API settings/review collection: 46 passed,
11 PostgreSQL-only skipped. Existing drama/illustrated Automation fixtures now
write real selected-picture bytes and matching hashes rather than fake hashes.
Independent review completed; no paid production recovery or setting change.

Use offline fixtures based on the three missing-picture cases: a manifest whose look and
pictures hashes match the document, whose present entries all passed the judge, and whose
remaining expected shot IDs have no picture. Assert `keyframes drawn` is false, submission
cannot auto-approve the subset, and assembly is never the first place the worker learns that
the set is incomplete. Repeat with an existing approved partial-manifest receipt, a missing
disk file, an incomplete end frame, duplicate IDs, a cap interruption and both media
switches disabled. Network stubs must prove no unauthorized generation request is sent.

```bash
node --test tools/video/core/state.test.mjs tools/video/review/sync.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/automation/automation.test.mjs
cd apps/api && uv run pytest tests/test_video_automation_settings.py
npm run test:tools && npm run check:tasks
```

After a separately authorized deploy and owner decision about the media settings/cap,
compare current document shot IDs to manifest IDs/files and the resulting storyboard.
Local regressions are not proof that any of the three production videos has recovered.

## Notes

- Diagnosis-only ticket: leave open and unclaimed. No source fix, production mutation,
  generation, retry, spending-limit change or publication was performed in this audit.
- At the live snapshot, the main worker was enabled, STOP was absent, production used two
  lanes, and both drama/media switches were off. Slides image model was `image-01`;
  settings were updated at 2026-10-04 05:23 UTC (13:23 Asia/Taipei). That snapshot does not
  establish which settings applied during each earlier generation. Do not re-enable them
  or raise caps as part of this implementation task.
- Source pointers in the audited checkout:
  - `tools/video/core/state.mjs:274,425,470`: `needsReview` checks present entries only;
    `keyframesDone` checks hashes/verdicts but not full expected-shot/file coverage.
  - `tools/video/media/keyframes.mjs:267,378-389,474-475`: manifests carry current bindings,
    preserve valid existing shots and persist each completed shot while production continues.
  - `tools/video/review/sync.mjs:783-837`, especially line 791: storyboard `drawn` silently
    filters out expected shots without a manifest file; judge summary covers this subset.
  - `apps/api/app/video_automation/settings.py:433-450,470-497`: automatic approval checks
    the supplied nonempty shot list and aggregate verdict, without an expected coverage set.
  - `tools/video/render/plan.mjs:97` and `tools/video/render/cli.mjs:241-252`: shot scenes
    have no rendered card states; render checks thumbnail backgrounds, so successful card
    rendering is not complete picture coverage.
  - `tools/video/assemble/cli.mjs:102-109`: assembly correctly checks every current shot
    and reports the missing IDs. Keep this final defense.
- Live evidence was captured outside git at
  `%TEMP%/mokaair-video-diagnosis-20261004/host-output.txt` (PROJECT/AUTO rows and worker log
  lines 208-234 in this audit). Do not commit host credentials, raw model requests or media.
- The coordinator verified SHA-256 equality between the live worker/API and this checkout
  for `core/state.mjs`, `review/sync.mjs`, `automation/flow.mjs`, `render/plan.mjs` and
  `apps/api/app/video_automation/settings.py`; the live BFF automation-run route also
  matched. Local HEAD was `7f2744a`, live repository HEAD `d038b035`. Despite the different
  repository commits, these relevant deployed source files were byte-identical, so the
  coverage gap is present in the audited live code rather than inferred from stale source.
- Related but different tickets: `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`
  covers model selection/2K/heuristics; `2026-10-03-video-worker-narration-takes-made-stale`
  covers narration evidence. Neither covers expected keyframe completeness.
- Separately observed stale backend reports for two writer-timeout videos are outside this
  ticket. Timeout recovery, UI reconciliation and imported-language runner recovery need
  their own work; do not expand this scope into them.
- Filing validation: `npm run check:tasks` passed (1390 task files, exit 0) before the
  separate blocked-report reconciliation ticket was filed; existing scope/stale-claim
  warnings were retained. No implementation tests were run because only this ticket changed.
