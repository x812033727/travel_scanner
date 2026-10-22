---
id: 2026-10-17-warn-brand-stories-at-45-second
title: Warn brand stories at 45-second hook gaps and fewer than eight loops
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-17T19:44:38Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/story-hook-cadence.mjs
  - tools/video/core/story-hook-cadence.test.mjs
---

# Warn brand stories at 45-second hook gaps and fewer than eight loops

## Why

The owner wants brand stories to hold a viewer's attention with source-backed questions and
turns throughout the narration, not only in the cold open. PR #1557, merged on `origin/main` as
`3dabd06be`, added brand-story-only `STORY_HOOK_RULES` to the writer prompt: roughly one hook
every 30–45 seconds, no gap above 45 seconds, at least eight setup/payoff loops for a ten-minute
story, and three later-moment previews in the opening. The shared explainer rules did not change.

The measurable lint still uses the general narrated-video thresholds in
`tools/video/core/narrative.mjs`: `HOOK_GAP_SECONDS = 90` and
`LOOPS_PER_10_MINUTES = 3`; the blind panel's `open_loops` question also asks about 90 seconds.
The lint findings are warnings, and a story with a long dry passage or
only three recorded loops can pass that mechanical check. This ticket adds a story-specific
warning without tightening the rules for tutorials or Curio videos. A warning identifies a
passage to read and listen to; punctuation, a chapter boundary, or a loop row by itself cannot
prove a real unresolved question or a satisfying payoff.

One isolated A01 editorial candidate has a 119-second gap on its **text-estimated** timeline.
It has no measured TTS, and it was not produced by the deployed #1557 writer prompt. That
estimate motivates a targeted check; it is not evidence that the new prompt failed in production.

## Definition of done

- [ ] `lint` warns for a `kind: story` video when an estimated narration stretch exceeds 45
      seconds without a candidate open question, escalation, held-back cause or turn, and gives
      the time window. It does not call every question mark or chapter cut a successful hook.
- [ ] For a ten-minute story with fewer than eight ID-valid setup/payoff rows, `lint` warns with the
      observed and required counts. The threshold scales to other story targets (for example,
      ten rows near 13 minutes); opening previews must map to later payoffs, not to the same
      opening scene.
- [ ] General narrated videos retain their current 90-second/three-loop warning behavior.
      The existing story source, listener, blind narrative review and measured-audio gates remain
      separate; this check never labels an actual script or completed film as approved.

## Steps

- [ ] Recheck current task claims, worktrees and open PRs for the four scoped paths before a
      future assignee claims this ticket. Do not release another owner's active claim.
- [ ] Add a story-only cadence/count helper and call it only when `isStory(context.series)` is
      true, without changing the shared constants or panel questions in `narrative.mjs`.
- [ ] Cover long gaps, real cross-chapter setup/payoff rows, short immediately answered
      questions, an opening-scene row wrongly counted as a later preview, and a non-story
      control. Keep the warning grounded in the available timeline; actual TTS can move cuts.
- [ ] Run focused lint tests and the affected video tool checks; have an independent reader
      review any semantic edge cases before treating the warnings as editorial decisions.

## How to verify

Run `node --test tools/video/core/story-hook-cadence.test.mjs
tools/video/core/lint.test.mjs` and `npm run test:tools`. Compare the same synthetic story and
non-story timelines before and after the change: a 46-second story gap and seven loops warn,
while a general narrated video still follows the 90-second/three-loop thresholds. Inspect the
time-window text and setup/payoff IDs, then review a real complete story with its actual audio
timeline before claiming the cadence is achieved in a film.

## Notes

Filed from current `origin/main`; ticket only, unclaimed. PR #1557's prompt test proves the
instruction reaches `writer:story`, not that a generated or offline script obeys it. The older
`2026-10-13-raise-the-loops-table-from-a` and `2026-10-13-lint-reads-the-whole-video-for`
tickets target the shared `narrative.mjs`, so this scope deliberately uses a separate helper
and its narrow `lint.mjs` integration. A stale in-progress Curio claim still lists `lint.mjs`
although its PR #1500 is merged; a future assignee must reconcile ownership under the
task-board rules before editing code. This task does not authorize host writes, paid media,
deployment, or reinterpretation of A01's existing HOLD reviews.
- 2026-10-19（票 `2026-10-19-curio-keeps-the-brand-stories-hook`）：`lint` 對 `kind: story` 與 curio- slug 改用
  `narrative.mjs` 的 `TIGHT_CADENCE`（45 秒、十分鐘 8 個伏筆，依長度縮放），沿用既有的 `hookCadenceProblems` 偵測器。
  這張票還剩的是更嚴的偵測：不把每個問號或章節切點都當成鉤子、開場預告要對到後面的回收。
