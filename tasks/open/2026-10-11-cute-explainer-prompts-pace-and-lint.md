---
id: 2026-10-11-cute-explainer-prompts-pace-and-lint
title: Cute explainer prompts: the pace they state is not the pace lint measures with
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T12:19:53Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/long-form/review.mjs
---

# Cute explainer prompts: the pace they state is not the pace lint measures with

## Why

The duration reviewer of the pull request that added the cute explainers' own prompts
(`tools/video/automation/explainer-series.mjs`) passed it and recorded seven observations. Two
are statements in the writer texts that do not match the tools, and one is a gap in what the
receipt watches:

1. **Pace.** The writer text says the voice reads 3.4 characters a second. Lint estimates a
   script at `DEFAULT_CPM = 250` (4.17 units a second) plus 300 ms a line and 700 ms a scene,
   and the bible text uses 250 a minute. An 8-minute request sized as exactly 8 minutes of
   speech at 3.4 a second estimates at 7.94 minutes with 20-unit lines and 7.68 with 24-unit
   lines, so lint refuses it and the video pays for one fix round. At 9 minutes the same sizing
   passes (8.91 and 8.70). The default request is 10 minutes, so this bites only at the floor.
2. **"40 is where lint refuses the line."** Lint only warns above 40 (`core/lint.mjs`, about
   lines 413-414). Harmless while the cute rule is "about 20, at most 24", but it is not true.
3. **The file is not bound by the duration receipt.** `explainer-series.mjs` is not in
   `REVIEW_FILES`, so a later change to the cute texts' length wording will not make the
   receipt stale, unlike `prompts.mjs`.

Also recorded, not acted on: at the low end of every range the episode shape gives 580 seconds
for a 10-minute target and 472 when scaled to 8 (the sentence after it and lint settle it);
12 line ids a minute is exact for a card-heavy script (106% of the target with four 20-unit
lines a scene); nothing but QA's 15-second pace item bounds the lines spoken over one card
state; the "4 to 7 seconds" cadence is not enforced for a drama-format explainer.

## Definition of done

- [ ] The two cute writer texts state the pace the way lint measures it (or tell the writer to
      size an episode with a margin above the 8-minute floor), and no longer say lint refuses a
      line at 40. The ten digests pinned in `explainer-series.test.mjs` are recomputed.
- [ ] A decision, written here, on whether `explainer-series.mjs` joins `REVIEW_FILES`; if it
      does, an independent reviewer issues the increment.
- [ ] flat-explainer's texts and every pinned digest of an existing variant are unchanged.

## Steps

- [ ] Deploy only with no cute explainer run in flight: a wording change within one variant
      does stop an unfinished run with `video_ai_receipt_input_changed`.

## How to verify

`node --test tools/video/automation/explainer-series.test.mjs tools/video/automation/prompts.test.mjs`;
an 8-minute cute request's first draft estimates at or above 8 minutes in a run with a fake
model that follows the text literally.

## Notes

- 2026-10-11 filed from the duration receipt of the cute explainers' prompts
  (reviewer `claude-opus-receipt-explainer-pr3`; the numbers above are that reviewer's).
