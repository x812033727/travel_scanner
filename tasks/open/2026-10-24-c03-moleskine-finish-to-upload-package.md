---
id: 2026-10-24-c03-moleskine-finish-to-upload-package
title: C03 Moleskine: re-record c031202 and finish to the upload package once the C-series paid hold is lifted
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-24T14:19:06Z
completed_at:
branch:
depends_on:
  - 2026-10-23-reconcile-c-series-prior-charges-and
scope:
  - docs/videos/story-everyday-moleskine-c03/reviews/upload-readiness-20261024.md
---

# C03 Moleskine: re-record c031202 and finish to the upload package once the C-series paid hold is lifted

## Why

The owner asked on 2026-10-24 for the brand story that is closest to publishable to be
completed with every rule, the 5 s channel intro and the 21 s v4 outro. In the local work
base (`<home>/mokaair-work/videos`) that is C03 Moleskine: 94 narration lines, 73 judged
illustrations, 21 rendered cards, music, thumbnail with the big brand name, outline and
script approved. The 2026-10-24 readiness readback
(`docs/videos/story-everyday-moleskine-c03/reviews/upload-readiness-20261024.md`) checks
every brand-story rule and the installed v4 bookends and finds one gap: line `c031202`
was recorded as 「七十八家」 and the approved script says 「七十九家」 (annual-report
correction, `reviews/factual-correction.md`). That one re-record (28 billable
characters) is a paid request, and every paid request for `story-everyday-*` is held
at four layers: the workspace `STOP`, `isPreproductionHeld` in the three local clients,
`PREPRODUCTION_HOLD_SLUGS` in the deployed API (#1782 in `c9cbf0022`), and the
activation process in `apps/api/app/video_budget/PENDING_EVERYDAY.md`. Nothing after
the re-record can run, because `clips`, `assemble`, `captions`, `qa` and `package` all
bind to the new speech hash.

## Definition of done

- [ ] The C-series hold is lifted for C03 by the reviewed activation change the
      dependency task describes (or the owner records a decision that settles C03's
      historical exposure), and the workspace `STOP` is removed with a note of who and why.
- [ ] `c031202` is re-recorded; `check-audio` passes; a human listens to the six old
      flags, `c031202` and `c031301`; chapters 2–20 pure speech measures at least 480 s;
      the owner approves narration and storyboard.
- [ ] `final.mp4` is assembled with the installed v4 package (intro at chapter 2,
      `intro_at: after_first_chapter`, 630-frame outro), zh-TW CC written, `qa` green
      including the three music loop seams, the owner approves the final.
- [ ] `package` written; the owner uploads privately, imports the end screen from
      `oxEtlA8GWas` in Studio, verifies the three elements by clicking, then picks languages.

## Steps

- [ ] Wait for (or do under) `2026-10-23-reconcile-c-series-prior-charges-and`: no
      unattributed request, no local edit of the hold lists outside a reviewed PR.
- [ ] Run the twelve-step chain in the readback's 「到『可以上架』還缺的每一步」 in order,
      each with `--workdir <home>/mokaair-work/videos`; keep every receipt under
      `docs/videos/story-everyday-moleskine-c03/reviews/`.
- [ ] Re-measure pure speech after the re-record; the old timeline had 481.25 s for
      chapters 2–20, only 1.25 s above the floor. Do not pad with pauses or bookends.
- [ ] Music: the cached Lyria track is 174 s against a 600 s manifest; record the
      checked loop before `assemble` (#1825) and listen to the seams at about 174, 348
      and 522 s in the final mix.

## How to verify

```sh
node tools/video/cli.mjs status --slug story-everyday-moleskine-c03 --workdir <home>/mokaair-work/videos
node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03
node tools/video/cli.mjs tts --slug story-everyday-moleskine-c03 --workdir <home>/mokaair-work/videos --dry-run
node tools/video/cli.mjs branding --workdir <home>/mokaair-work/videos --json
```

Before the hold is lifted the dry run says `1 to synthesize; about 28 billable characters`
and branding reports the v4 package (intro 150 frames, outro 630 frames). After the chain,
`status` shows every step ticked through `upload package`, and `checks.json` carries
`branding.intro_at_frame` at the chapter-2 start.

## Notes

2026-10-24 (claude-fable-5-1): readback written, lint 0/0, tts dry run 1 line / 28 chars,
server voice ready (Gemini 6,937,825 characters left this month), v4 bookends verified by
SHA-256 and `ffprobe -count_frames`. No paid call, no `STOP` removal, no upload. C04–C06 in
the same work base are further back (no images; C04 also no narration) and sit under the
same hold.
