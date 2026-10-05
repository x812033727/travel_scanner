---
id: 2026-10-05-clips-a-shot-every-seed-is
title: Clips: a shot every seed is refused for loses the provider's refusal
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T00:37:01Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
---

# Clips: a shot every seed is refused for loses the provider's refusal

## Why

When the clip provider refuses every seed of a shot (a failed job with a retakeable code such as
`video_media_rejected` or `video_media_upstream_invalid`), `tools/video/media/clips.mjs` saves the
shot as `{ ...entry, needs_review: true, problems: ["no take could be generated"] }`. The provider's
words are printed once per seed on stdout and then lost: the `ERROR <id>: no take passed:` line and
the manifest say only "no take could be generated", and `automation/flow.mjs` `failedTargets` hands
that bare phrase to the writer's prompt fix, which then has nothing to go on (a prompt too long for
the model, a content filter). `keyframes` had the same gap and now keeps the refusal
(2026-10-04-keyframes-crashes-when-every-image-take); clips does not crash, it only loses the reason.

## Definition of done

- [ ] A clip shot every seed is refused for is saved with one problem per distinct refusal
      (`no take could be generated: <provider detail>`), and its `ERROR <id>:` line shows that text
      rather than "no take passed".
- [ ] The record of such a shot carries no field from an earlier record whose clip is gone (today
      `{ ...entry }` spreads `current` into it).
- [ ] Failed-job ledger rows (zero cost) and `media/jobs.json` stay as `Stage.generate` leaves them, and
      a rerun once the provider takes the prompt draws only that shot.

## Steps

- [ ] In the take loop of `clips.mjs`, keep each retakeable error's message (without the
      `<shot id>: ` prefix `Stage.generate` adds) and build the all-refused record from them, as
      `keyframes.mjs` does.
- [ ] A test in `clips.test.mjs` with a fake server whose clip job fails with a retakeable code for every
      seed of one shot and not for another.

## How to verify

```bash
node --test tools/video/media/clips.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Found while fixing 2026-10-04-keyframes-crashes-when-every-image-take (PR on branch
  `claude/keyframes-all-rejected`); see that ticket's Notes for the keyframes side of the same change.
- `tools/video/media/clips.test.mjs` is bound by `docs/videos/long-form/review.json`: editing it needs an
  independent DURATION_ONLY receipt increment, so open the PR as a draft and report the stale list.
- The open ticket 2026-10-04-profile-works-external-clip-route also lists both files; check it is not
  claimed before claiming this one.
