---
id: 2026-10-09-send-a-final-cut-back-to
title: Send a final cut back to the writer when its demonstration score fails, instead of to the owner
status: done
priority: P2
area: tools
owner: claude-opus-5-5-demo-gate
claimed_at: 2026-10-17T04:53:40Z
created_at: 2026-10-09T02:41:25Z
completed_at: 2026-10-17T05:08:20Z
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - tools/video/automation/flow.mjs
  - tools/video/qa
  - tools/video/automation/automation.test.mjs
  - docs/videos/HANDS-OFF.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Send a final cut back to the writer when its demonstration score fails, instead of to the owner

## Why

`claude-code-mods-no-sandbox-before-install` reached the final gate with
`policy: Jev：符合立場 0.79、有示範 0.45、建議 0.01、業配 0.04；沒過（有示範低於 0.6）`
in its `review/qa.json`. The flow's answer to a failed policy item is to hand the cut to the
owner, who approved it on `/admin/videos` on 2026-10-08 and the next day said the video teaches
nothing. The judge had seen it; nothing acted on what it saw. By then the narration was
recorded and 55 illustrations were paid for.

The same script had passed the outline gate with 有示範 0.91 (`approvals.json`), so the score
fell between the outline and the finished script, and the first place it was read again was
after every paid stage.

## Definition of done

- [x] A script whose demonstration score is under the threshold goes back to the writer with
  the judge's reason, before narration and pictures are paid for.
- [x] The owner is asked only when the writer's revisions are used up, and the card says so.
- [x] A video already at the final gate is not sent back by this change.

## Steps

- [x] Find where the script could be scored between `lint` and `tts` (the outline judge and the
  final policy judge are both in `apps/api/app/video_automation/judge.py`).
- [x] Decide with the owner how many revisions before it becomes theirs.
- [x] Tests for both paths, and the duration receipt if a bound file changes.

## How to verify

A fixture script with no demonstration is returned to the writer once and reaches the owner
with the reason on the card after the last revision; a script that passes is untouched.

## Notes

- Found while writing the content-value rules (`2026-10-09-hold-every-slides-video-to-content`,
  PR 1392). Those rules are prompt text: this task is the gate that makes them hold.
- Changing who decides at a gate is the owner's call (`docs/videos/HANDS-OFF.md`); ask before
  building.
- 2026-10-17 (claude-opus-5-5-demo-gate): the owner answered 「退回兩次」. Built as `demoGate` in
  flow.mjs, right after the storytelling panel and before `script approved` and every paid stage:
  the narration goes to the existing `POST /video/automation/judge/policy` (no server change; the
  site still picks the question set, so explainers and stories answer `demo: null`), a demo under
  `SCRIPT_MIN_DEMO` (0.6) goes back through `fixScript(..., "Jev", "demo")`, whose
  `MAX_PROMPT_FIX_ROUNDS` (2) gives the two revisions and then blocks with the note
  (`prompt_fixes:demo`; the owner's retry resets it). The verdict is kept in
  `review/demo-check.json`, bound to the narration's SHA-256, so an unchanged rewrite is not
  asked again. Skipped once `narration synthesized` is done, for drama, stories and
  compilations, and when the site answers 409 (no stance) or 404. Tests in
  automation.test.mjs; the receipt is re-issued by an independent reviewer.
- Review round 1 (claude-pr-review-demo-gate) found that the skip read whether the narration was
  *current*: a line edited after the audio was sent back, or a lexicon reading changed at the
  final cut, made a paid narration stale and let the gate send the script back. The gate now skips
  any video whose `timeline.json` exists (narration ever recorded); a regression test edits a line
  of a narrated video and asserts no Jev call and no writer fix.
