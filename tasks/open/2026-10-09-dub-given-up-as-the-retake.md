---
id: 2026-10-09-dub-given-up-as-the-retake
title: Dub given up as the retake failed when a retake overruns its window
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T14:49:22Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Dub given up as the retake failed when a retake overruns its window

## Why

Four of the 49 dub parts skipped on production (count of 2026-10-09) carry the reason
`the retake failed:   budgets are in <workdir>/dubs/<locale>/fit.json; after i18n-merge,
run dub --locale <locale> again`: `enisa-threat-landscape-2026-denominator` en,
`openai-devday-2026-recap` en, `ai-term-temperature` ja, `cloudflare-ai-attacks-own-waf-49-findings` ja.

The message is the last line of `dub --redo`'s exit-1 output: the re-synthesised take of
a flagged line came out longer than its window. `flow.mjs` only re-enters shortening when
`rounds.shorten < MAX_DUB_SHORTEN_ROUNDS`; once the shortening rounds are spent it reaches
`if (redo.code === 1 || redo.code === 3) return this.giveUpDub(...)` and the locale is
lost, although the previous take of that line fitted and only its wording was in doubt.
The reason the owner reads is a hand-run instruction with a host path in it.

## Definition of done

- [ ] A retake that overruns its window with no shortening round left keeps the previous
      take of that line (or shortens that one line once more), and the batch reports the
      line as "kept the earlier take, heard as …" instead of skipping the locale.
- [ ] The skip reason, when a skip is still right, names the lines and says what the owner
      can do on the card, not a path on the host.
- [ ] `automation.test.mjs` covers a retake exiting 1 after the shortening rounds are spent.

## Steps

- [ ] Reproduce with the fake dub in `automation.test.mjs` (`fakeDub`): a `--redo` run that
      exits 1 with over lines when `rounds.shorten` is already at the cap.
- [ ] Change the branch in the retake loop; keep the exit-3 (needs the owner) path as is.
- [ ] Reword the give-up reason through `giveUpDub` for all three skip reasons so none of
      them carries a host path.

## How to verify

`npm run test:tools`; the four videos above re-run with `dub --locale <l>` on the host
end with a track or a reason that names lines, not a path.

## Notes

- Sibling tickets: `2026-10-09-dub-skipped-because-jev-still-hears` (31 skips) and
  `2026-10-09-dub-skipped-because-lines-do-not` (14 skips).
