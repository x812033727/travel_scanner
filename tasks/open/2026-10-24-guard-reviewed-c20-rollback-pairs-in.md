---
id: 2026-10-24-guard-reviewed-c20-rollback-pairs-in
title: Guard reviewed C20 rollback pairs in host verification
status: blocked
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-24T05:47:47Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
  - tasks/open/2026-10-24-guard-reviewed-c20-rollback-pairs-in.md
---

# Guard reviewed C20 rollback pairs in host verification

## Why

The deploy verifier's `alembic-head` section invokes the correct read-only
`app.migration_guard --status` but then accepts `rollback-compatible` only
for 0132 image / 0133 database. The 0137 / 0138 pair already reviewed by the
API and the staged 0138 / 0139 C20 pair would therefore fail host verification
even after the guard checked the exact account/hold state.

## Definition of done

- [ ] After scope release, host verification accepts only exact 0132→0133,
      0137→0138, and 0138→0139 pairs when exactly one image head exists,
      guard exit is zero, the guard's expected head equals that image head,
      and its state is `rollback-compatible`.
- [ ] Unknown, reversed, multiple-head, missing readback and guard-error states
      still fail; the existing exact-head path remains unchanged.

## Steps

- [x] Read current script and other verification paths; prepare narrow patch
      and tests without editing the occupied file.
- [ ] Release the two exact scope paths through task-board coordination.
- [ ] Add a small exact-pair predicate to `host-verify.sh`; test its positive
      and negative matrix in `tools/deploy-host-verify.test.mjs` and run `bash -n`.
- [ ] Rerun CI and review before declaring C20 compatibility release-ready.

## How to verify

Run `node --test tools/deploy-host-verify.test.mjs`, `bash -n
.agents/skills/deploy/scripts/host-verify.sh`, the focused API rollback tests,
and all four required PR checks. After an authorized deployment, run the host
verifier itself and require `TOTAL fail=0` plus its `SCHEMA_STATUS` readback.

## Notes

2026-10-24: `host-verify.sh:215-224` parses `SCHEMA_STATUS`, requires exactly
one image head, guard exit 0 and expected=image head, but hardcodes only
`0132_video_pilot_budget` + `0133_story_followon_budget` in the compatible
branch. Exact needed alternatives are `0137_video_manga_tier` +
`0138_story_everyday_budget`, and `0138_story_everyday_budget` +
`0139_c20_zippo_pilot_budget`. A `case "$alembic_head:$current"` helper
inside that guarded branch can cover precisely the three pairs; tests should
exercise all three plus reversed, same-head, unknown future, and wrong-current
pairs. `docker-compose.prod.yml:37` already runs the migration guard before
API startup. API `/ready` and admin overview inspect revision only; they do
not recheck account/hold contents during runtime. Host verification must keep
the guard's full `--status` readback. `host-preflight.sh` and
`host-deploy.sh` contain no separate Alembic compatibility condition.
`post-deploy.md:8,33` still describes equality with image head only and will
need a later documentation correction when its scope is available.

Normal claim without `--force` refused: `2026-10-24-guard-reviewed-c20-rollback-pairs-in
covers files already being changed by 2026-10-14-recognize-the-video-monthly-draft-cap
(claude-opus-5-5-video-cloud-backup); run 'next' for a task that is free,
or pass --force`. That old ticket is status=in-progress, claimed at
2026-10-22T02:15:08Z; its branch/PR is absent according to the parent audit.
This ticket is blocked pending the owner's narrow release. No occupied file
has been edited.
