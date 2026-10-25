---
id: 2026-10-24-c03-moleskine-finish-to-upload-package
title: C03 Moleskine: re-record c031202 and finish to the upload package once the C-series paid hold is lifted
status: review
priority: P1
area: docs
owner: claude-fable-5-1-c03-upload
claimed_at: 2026-10-24T16:00:00Z
created_at: 2026-10-24T14:19:06Z
completed_at:
branch: claude/c03-upload-package-20261025
depends_on: []
scope:
  - docs/videos/story-everyday-moleskine-c03/reviews/upload-readiness-20261024.md
  - docs/videos/story-everyday-moleskine-c03/reviews/upload-package-20261025.md
---

# C03 Moleskine: re-record c031202 and finish to the upload package once the C-series paid hold is lifted

## Why

The owner asked on 2026-10-24 for the brand story that is closest to publishable to be
completed with every rule, the 5 s channel intro and the 21 s v4 outro. In the local work
base (`<home>/mokaair-work/videos`) that is C03 Moleskine. The 2026-10-24 readiness readback
found one gap: line `c031202` was recorded as 「七十八家」 and the approved script says
「七十九家」, and every paid request for `story-everyday-*` was held at four layers. The owner
then decided (2026-10-24): lift the hold for C03 only, deploy, close C03's pre-ledger exposure
at the full USD 25, re-record the line and finish to the upload package.

## Definition of done

- [x] The C-series hold is lifted for C03 by a reviewed change (PR #1832, deployed
      `11e23a876`, verified 13/13), the host settled C03's `pre-ledger-history` at USD 25 with
      receipt `owner-decision-20261024-c03-full-ceiling`, and the workspace `STOP` was set aside
      with a note of who and why.
- [x] `c031202` re-recorded; `check-audio` run twice (six old flags retaken once, five cleared;
      `c031101` kept as an ASR near-homophone with its MP3 left for the owner); chapters 2–20 pure
      speech 481.02 s; audio and storyboard gates recorded with notes.
- [x] `final.mp4` assembled with the v4 package (intro at 37.87 s after chapter 1, 630-frame
      outro, 19,006 frames, −14 LUFS), zh-TW CC written, `qa` 10/11 (policy: Jev observation
      0.59 against 0.6, not re-askable), final gate recorded with that note.
- [x] `package` written (4/4).
- [ ] The owner watches `review/final.html`, uploads privately, imports the end screen from
      `oxEtlA8GWas` in Studio and verifies the three elements, then picks languages.

## Steps

- [x] Lift, deploy, settle, set `STOP` aside.
- [x] `tts` → `check-audio` → `tts --redo` → `check-audio` → gates.
- [x] `clips` → `music --loop` → `assemble` → `captions` → `qa` → final gate → `package`.
- [ ] Owner upload and Studio end screen; `youtube-sync --dry-run`; languages later.

## How to verify

```sh
node tools/video/cli.mjs status --slug story-everyday-moleskine-c03 --workdir <home>/mokaair-work/videos
```

Every step through `upload package` is ticked; `upload/final.mp4` sha256
`915830a0969b480225c5e4d655794489de29bcfd02cc15ad61a8de24187dc75b`; `branding.json` pins
`intro_at: after_first_chapter`, `intro_at_frame 1136`. Host:
`python -m app.video_budget.reconcile_cli --slug story-everyday-moleskine-c03` reads
`historical_closed_usd 25.000000`, settled 0.017682.

## Notes

2026-10-25 (claude-fable-5-1): everything through the upload package is done and read back in
`reviews/upload-package-20261025.md`. Post-activation spend USD 0.017682 (7 TTS, 7 transcriptions,
2 judges, 1 policy). Two things the owner should know before uploading: `c031101`「開場那天」 is
heard as 「開展」/「開產」 by both transcribers on two takes (MP3 in `review/c031101-take2.mp3`),
and the policy judge scored "leaves an observation" 0.59 against a 0.6 threshold and cannot be
re-asked for the same narration. The music loop plays the 174 s track 4 times; seams at about
174, 348 and 522 s should be listened to in the final cut. The task stays in review until the
owner's upload; close it then.
