---
id: 2026-10-22-reconcile-legacy-generated-music-manifests-in
title: Reconcile legacy generated music manifests in status
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-22T03:09:57Z
completed_at:
branch:
depends_on:
  - 2026-10-16-bind-story-audits-and-narration-to
scope:
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
---

# Reconcile legacy generated music manifests in status

## Why

Before the generated-music duration guard, `music/manifest.json` stored the requested
`seconds` as if it were the delivered length. The C03 Moleskine manifest requests
600 s although the retained MP3 fully decodes to 174.0016 s. The new guard makes
the assembly and dub paths refuse an unmeasured generated track and can remeasure the cached file
on a manual `music` rerun, but `pipelineStatus` in `state.mjs` still marks an old
manifest's `music generated` step done solely from `mix_hash`. Automated runners
can therefore advance to assembly and hit a hold without offering the remeasurement
step. `state.mjs` is in an already claimed A01 lexicon task, so this follow-up
depends on that task rather than editing its files concurrently.

## Definition of done

- [ ] For generated music, status only marks `music generated` done after actual
      duration and hash evidence for the current cut are present and sufficient;
      legacy request-only manifests remain pending without discarding paid files.
- [ ] Owner-supplied `music.track` and existing unrelated routes retain their
      current status semantics.
- [ ] Tests cover a legacy manifest, a measured short hold, a measured long track,
      and a changed timeline.

## Steps

- [ ] Reconcile the A01 changes to `state.mjs`, then add the narrow generated-music
      evidence check after that scope is released.
- [ ] Ensure status tells the operator to rerun `music` for cached measurement,
      without a new vendor purchase.

## How to verify

Run `node --test tools/video/core/state.test.mjs` with the repo's supported Node
runtime, then `npm run check:tasks`. Confirm a retained legacy C03 manifest is
pending while its MP3 and media ledger remain untouched.

## Notes

Raised from the duration guard branch (`codex/lyria-duration-guard`, stacked on
the C03 draft PR). The manual `music` path measures a cached MP3 and writes
`requested_seconds`, `actual_seconds`, `duration_measurement` and `duration_hold`;
the shared music input guard already rejects request-only generated manifests. Do not resubmit the
provider job merely to update status.
