---
id: 2026-10-09-send-a-final-cut-back-to
title: Send a final cut back to the writer when its demonstration score fails, instead of to the owner
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T02:41:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - tools/video/automation/flow.mjs
  - tools/video/qa
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

- [ ] A script whose demonstration score is under the threshold goes back to the writer with
  the judge's reason, before narration and pictures are paid for.
- [ ] The owner is asked only when the writer's revisions are used up, and the card says so.
- [ ] A video already at the final gate is not sent back by this change.

## Steps

- [ ] Find where the script could be scored between `lint` and `tts` (the outline judge and the
  final policy judge are both in `apps/api/app/video_automation/judge.py`).
- [ ] Decide with the owner how many revisions before it becomes theirs.
- [ ] Tests for both paths, and the duration receipt if a bound file changes.

## How to verify

A fixture script with no demonstration is returned to the writer once and reaches the owner
with the reason on the card after the last revision; a script that passes is untouched.

## Notes

- Found while writing the content-value rules (`2026-10-09-hold-every-slides-video-to-content`,
  PR 1392). Those rules are prompt text: this task is the gate that makes them hold.
- Changing who decides at a gate is the owner's call (`docs/videos/HANDS-OFF.md`); ask before
  building.
