---
id: 2026-10-09-dub-skipped-because-jev-still-hears
title: Dub skipped because Jev still hears lines wrong is the top skip reason
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-09T14:49:20Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - docs/videos/DUBS.md
---

# Dub skipped because Jev still hears lines wrong is the top skip reason

## Why

The owner ticks English, Japanese and Korean dubs on every video, and on 2026-10-09 the
latest `languages` batch of each of the forty videos on production showed, per locale:

| locale | dub ready | dub skipped |
| --- | --- | --- |
| en | 10 | 14 |
| ja | 5 | 19 |
| ko | 6 | 16 |

Of the 49 skips, 31 carry the reason `Jev still hears lines wrong after 2 retakes and N
rewording rounds` (en 9, ja 12, ko 10): `gpt-6-sol-luna-where-to-use` and
`openai-cursor-wind-down-nov-12` lost all three locales to it, `sec-ai-trading-bot-whatsapp-scam`,
`mcdonalds-ai-pricing-engine-who-said-what` and `cloudflare-workers-per-worker-permissions-ai-agent`
two each. The worker gives up after `MAX_DUB_RETAKE_ROUNDS` retakes and
`MAX_DUB_REWORD_ROUNDS` rewordings (`flow.mjs`, the `Jev still hears lines wrong` branch)
and leaves `review/check-flags.<locale>.json` behind for a hand-run `dub --redo`, which
nobody runs. A dub that reaches the owner is the exception, not the rule.

DUBS.md §聲音會唸錯的地方 already records that most of Gemini's flags on its own are it
"correcting" version numbers and brands it does not know, and that `check-audio
--second-opinion` (local Whisper) clears those. Whether the production worker runs with a
second opinion, and what the 31 flags actually are, has not been measured.

## Definition of done

- [ ] The flags behind at least ten of the 31 skips are classified (real misreading,
      transcriber "correction" of a name or number, number or unit read wrong per
      DUBS.md's list) and the counts are in the Notes.
- [ ] The dominant class has a fix in the pipeline, not a hand-run instruction: a second
      opinion on by default on the host if it is off, dictionary entries fed back from the
      flags, or a bounded extra round, whichever the measurement supports.
- [ ] The skip rate on the next ten videos' first `languages` batch is reported against
      this baseline (31 of 49 skips, 20 of 70 ticked dubs ready).

## Steps

- [ ] On the host, read `review/check-flags.<locale>.json` under
      `/var/lib/mokaair/video-work/<slug>/` for the five videos above and classify each flag.
- [ ] Check whether `VIDEO_SECOND_OPINION` (or the `--second-opinion` argument) is set for
      the production video worker; if not, cost it and propose turning it on.
- [ ] Pick the fix from the measurement; add the regression to `automation.test.mjs`.
- [ ] Record the before/after counts here and in DUBS.md.

## How to verify

`npm run test:tools`; then one video through the automated route on the host with all
three dubs ticked, and its `languages` card showing dubs ready rather than skipped.

## Notes

- Sibling tickets from the same count: `2026-10-09-dub-skipped-because-lines-do-not`
  (14 skips, windows that do not fit at 1.15x) and `2026-10-09-dub-given-up-as-the-retake`
  (4 skips, a retake that overran its window).
- The ready tracks were never uploaded either; see
  `2026-10-09-languages-card-says-the-site-cannot`.
