---
id: 2026-10-21-render-layout-check-misses-a-big
title: Render layout check misses a big card whose second text line is covered by its sub (icon + two lines + sub)
status: done
priority: P2
area: tools
owner: codex-open-tasks-tools
claimed_at: 2026-10-24T13:50:58Z
created_at: 2026-10-22T00:40:00Z
completed_at: 2026-10-24T14:31:39Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/video/render/browser.mjs
  - tools/video/render/render.test.mjs
---

# Render layout check misses a big card whose second text line is covered by its sub (icon + two lines + sub)

## Why

The owner watched the first paper-look tutorial (`claude-md-house-rules`, 2026-10-22) and saw text
cut off at 4:10. The card was a `big` scene with `icon: "checklist"`, a two-line `text`
(「寫得出「怎麼算做對」\n的才寫」) and a `sub`: with the key band's `--safe-bottom:274px` the icon
(150 px) plus two 150 px lines plus the sub no longer fit, and the second text line was drawn
under the sub line. `render` reported no layout problem for that state: its checks catch content
taller than the area and text that does not fit at 60 %, but not one element overlapping another
inside the content box. Three cards had the shape (`verifiable`, `draft-keep`, `answer`); the fix
in the video was to drop their icons.

## Definition of done

- [x] `render` reports a layout problem when two elements of a `big` card (icon, word, sub,
      kicker) overlap, or when the `.word` block is taller than the room the icon and sub leave it.
- [x] A `big` card with icon + two-line text + sub either fits (the icon shrinks or the word wraps
      smaller) or is refused before any frame is drawn.
- [x] templates.test.mjs / render.test.mjs cover the case.

## Steps

- [x] In `tools/video/render/browser.mjs` layout checks, compare bounding boxes of `.t-big .ic`,
      `.t-big .word`, `.t-big .sub` (and the numeral row) and report overlaps.
- [ ] Or in NUMERAL/ICON CSS give `.t-big .word` a max-height that accounts for the icon and the
      sub, and let `.fit` shrink it.

## How to verify

Render `tools/video/templates/fixtures/paper/video.json` with an added big card of that shape and
see the problem reported; render `claude-md-house-rules` and see none.

## Notes

- 2026-10-24: The coordinator narrowed the claim to `browser.mjs` and `render.test.mjs`
  after fresh open-PR/exact-path checks found no current matching implementation owner.
  The two stale overlapping credited-image/brand-thumbnail task scopes keep their owners
  and remaining work. No template, theme, source video or production asset was changed.
- Reproduced the exact `verifiable` card in native Edge by restoring only its removed
  checklist icon. The old renderer reported no problems, while its second line visibly
  clipped the bottom of 寫. The word's box was 272.84375 px tall, its natural two-line
  height 302.4 px, and scrollHeight 327 px; the generic 0.4-em overflow allowance missed it.
- New big-card admission measures a hidden off-flow clone at the same width/font with
  unconstrained height, then immediately removes it. It also compares sibling slots;
  a numeral row is one slot so its contained word is not a false overlap. The settled
  check runs before any still or entrance screenshot and refuses with a clear UsageError.
- Complete render regressions passed 42/42 with zero skips on bundled Node 24.19.0.
  New cases cover the measured clipping, sibling overlap, touching edges, hidden slots,
  numeral containment, zero screenshots on refusal and normal 18-frame entrance output.
- Real native Edge readback: the exact bad card now refuses with `screenshots: 0`;
  the current corrected card renders with no problems and `screenshots: 1`. Both before
  and corrected PNGs were visually inspected. Evidence stays outside Git in the
  operator's temporary directory: `big-card-before-20261024.png`,
  `big-card-after-good-20261024.png`, `big-card-geometry-20261024.jsonl`,
  `big-card-after-bad-20261024.jsonl`, `big-card-after-good-20261024.jsonl`,
  and `big-card-render-full-20261024.log`.
- Existing cached states retain their original pixels and cache policy. To apply the
  new browser check to retained cached states, use an explicit `render --force` run;
  this fix does not invalidate approvals or automatically rewrite older frames.
  No paid call, host operation, new source capture or media approval occurred.
- The coordinator accepted the current tutorial's 20 big cards as the native cohort;
  other scene types and source recapture stay outside this layout fix. The initial
  20-second-per-card run rendered 18 cards, including all three originally affected
  scenes; `g1-rule` and `stakes` hit capture timeouts during startup. That run has
  actual exit 1 and is retained as `big-card-tutorial-big-only-20261024.jsonl`.
  Only those two cards receive one bounded retry (60 seconds per card, 150 overall);
  the failed first receipt is preserved.
- The single two-card retry completed with actual exit 0: `g1-rule` and `stakes`
  both rendered with `problems: []`. Its independent receipt is
  `big-card-tutorial-two-retry-20261024.jsonl`. The unchanged current-source cohort
  therefore has 18 first-run passes plus two bounded-retry passes, covering all 20
  distinct big cards. This does not relabel the initial exit-1 run as a success.
- Independent review by `/root/final_checks` found no code blocker and verified the
  before/after PNGs, zero-screenshot refusal, valid readback and complete 42-test log.
  Direct inspection of `tools/video/long-form/review.mjs` confirms neither changed
  product/test path is in `REVIEW_FILES`, so this layout fix needs no duration
  binding change. Renderer admission implements the chosen path;
  the alternative CSS step is not required.

Found on 2026-10-22 from the owner's first viewing; the render's "content is N px taller than its
area" check did fire for the eight numeral cards (icon + numeral + sub) earlier the same day, so
the gap is specifically overlap without overflow.


### 2026-10-24 narrow owner-requested execution

Parent coordinated only the exact listed source/test paths after fresh branch/worktree/open-PR checks found no active exact-file implementation. Historical broader stale scope is not taken over; its remaining producer/media/acceptance work stays untouched. The preceding related fixes on this parent branch are retained. Scope is narrowed before product editing. No provider calls, paid regeneration, production settings change or deployment is part of this code task.


### 2026-10-24 coordinator acceptance

Renderer refuses clipped/overlapping big cards before any screenshot;42/42 regressions passed. Independent code+PNG review by codex-final-checks accepted. Native exact bad card zero screenshots; corrected card valid. Current20-card cohort18 first-run passes plus2 bounded retry passes; initial2 startup-timeout failures retained. browser.mjs/render.test.mjs excluded from108 duration REVIEW_FILES; no new binding needed. Existing cached states require explicit render --force to revalidate.

Implementation is local on `codex/open-tasks-reconcile-20261024`; merge/deployment and any paid media actions remain separate. No vendor POST, media deletion, upload or approval was performed by this fix.
