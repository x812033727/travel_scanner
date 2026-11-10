---
id: 2026-11-10-tai-nainai-handoff-back-up-e001
title: tai-nainai handoff: back up e001-e005 production files to Drive, then shoot episode 6
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-10T06:56:17Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/session-tools
---

# tai-nainai handoff: back up e001-e005 production files to Drive, then shoot episode 6

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Context
The session that made 《恁祖媽今年18》 episodes 1–5 ended on 2026-11-10. Read
`docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/session-tools/README.md` first.

- Episodes 1–5 are imported and wait for the owner at /admin/videos.
- Their production files were never copied to Google Drive (the old session could not read the rclone variables).
  Their latest copies are on the retired backup branches in `drama-backup-tn`; the host is moving those branches to Drive.
  Branches `transfer/tn-e001`, `tn-e004`, `tn-e005`, `tn-shared` match the final local files (independently checked).
  `transfer/tn-e002` and `transfer/tn-e003` are older than the final local files (e002: about 34 files — the new c15 take,
  the v3 cut and the import folder; e003 not checked). Whatever the old session decided about those is recorded below.
- Episode 6 is storyboarded and reviewed (37 shots) and nothing has been spent; the prepared manifests are in `session-tools/e006/`.
- Cap from episode 6: 40 CU (owner 2026-11-10).

- [ ] confirm the host migration put `transfer/tn-e00N` and `tn-shared` under `AI劇/恁祖媽今年18/` on Drive
- [ ] episode 6: pictures → stills → clips → pick → fix → refine → cut → review → import → todrive.sh
