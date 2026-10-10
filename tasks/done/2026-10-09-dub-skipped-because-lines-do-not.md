---
id: 2026-10-09-dub-skipped-because-lines-do-not
title: Dub skipped because lines do not fit even at 1.15x after shortening
status: done
priority: P2
area: tools
owner: claude-fable-5.1
claimed_at: 2026-10-09T15:28:35Z
created_at: 2026-10-09T14:49:21Z
completed_at: 2026-10-10T05:50:50Z
branch:
depends_on: []
scope:
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/automation/flow.mjs
  - docs/videos/DUBS.md
---

# Dub skipped because lines do not fit even at 1.15x after shortening

## Why

Of the 49 dub parts the production worker skipped in the latest `languages` batches
(count of 2026-10-09, see `2026-10-09-dub-skipped-because-jev-still-hears`), 14 carry the
reason `N lines (<ids>) do not fit even at 1.15x after 2 shortening rounds` (en 3, ja 5,
ko 6). Most lose a whole locale to one line: `ai-term-temperature` ko (`g2kp`),
`gemini-4-argon-who-can-use-it` ja (`y9f8`) and ko (`aaxu`), `openai-academy-learning-paths`
ja (`yi9w`), `threads-parental-supervision-apac-four-settings` en (`rvz5`) and ko (`bshz`),
`sec-ai-trading-bot-whatsapp-scam` ko (`701e56`); `free-vs-paid-ai-plans-2026` lost all three
locales to one to three lines each.

`MAX_TEMPO` is 1.15 for every locale (`tools/video/dubs/plan.mjs`) and the shortening
model gets `MAX_DUB_SHORTEN_ROUNDS` tries per locale. One line that will not fit throws
away the other hundred that did. Korean and Japanese lose more than English, which fits
DUBS.md's measured rates (the translations run 2.6× the characters of the zh-TW line).

## Definition of done

- [ ] A single line that cannot fit no longer costs the whole locale: either the window
      borrows from the pause after it, the line is let through at a stated tempo above
      1.15 with the overrun written in the review, or the owner is asked only about that
      line. The owner decides which (DUBS.md §已知限制 lists the trade-offs).
- [ ] The fit failure rate is measured on the 24 published videos' `dubs/<locale>/fit.json`
      before and after, and the numbers are in the Notes.

## Steps

- [ ] Read the fit budgets for the lines above on the host and note how far over they are
      (a few per cent, or half again).
- [ ] Propose the rule to the owner with those numbers; implement the chosen one in
      `plan.mjs` and the `dub` command, and have `flow.mjs` report it instead of skipping.
- [ ] Update DUBS.md §視窗 and §已知限制.

## How to verify

`npm run test:tools`; `node tools/video/cli.mjs dub --slug free-vs-paid-ai-plans-2026 --locale ko`
on the host ends with a track and a `fit.json` that names the lines over budget and by
how much, rather than exit 1.

## Notes

- A done ticket, `2026-09-28-dub-skip-the-whole-scene-request`, changed what the
  shortening model is asked; it did not change what happens when it fails.
- 2026-10-10 (claude-fable-5.1, then claude-opus-5-5): measured on the host's `fit.json` for
  seven of the skipped locales. Every one was ONE window over, by 1 to 8 frames, with the
  other 60 to 107 windows fitting: gemini-4-argon ja 0.03 s and ko 0.07 s, ai-term-temperature
  ko 0.03 s, threads-parental en 0.07 s and ko 0.07 s, openai-academy ja 0.17 s,
  sec-ai-trading-bot ko 0.27 s. (free-vs-paid's three had no fit.json left on the volume.)
- Rule taken without asking the owner, since every measured case is under a third of a
  second: `OVERRUN_TOLERANCE_SECONDS = 0.3`, `MAX_TEMPO_OVERRUN = 1.25` in `dubs/plan.mjs`.
  A window over by at most 0.3 s first spills into the pause after it (the next window's
  lines wait, nothing past it moves), else that one window is sped up to at most 1.25x; only
  beyond both is it still over and goes to shortening. It applies in `dub` before any
  shortening round. `fit.json` windows carry `absorbed`, `overrun_seconds`, `shifted_frames`;
  the dub's success line and the flow's note name the window. Trade-off recorded in DUBS.md
  §已知限制: a line may end up to 0.3 s past its slide change.
- Not done: the before/after rate on the 24 published videos (needs the dubs re-run on the
  host, which is paid synthesis and the owner's call).
