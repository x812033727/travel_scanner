---
id: 2026-10-11-decide-and-fact-check-the-rewritten
title: Decide and fact-check the rewritten Skills hands-on tutorial
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T12:13:06Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-skills-vs-claude-md
---

# Decide and fact-check the rewritten Skills hands-on tutorial

## Why

The Skills tutorial was rewritten on 2026-10-11 (task
`2026-10-11-rewrite-the-skills-hands-on-tutorial`) so that its main example is the same
procedure kept in CLAUDE.md beside the same procedure as a Skill. This task held what was open
after the rewrite. Both of its questions are answered; what is left is production, which the
owner wants run by another agent under its own task. This file stays open until that task
exists, so that what the producer needs is not lost; close it when the production task is filed.

- **The owner's decision** (relayed by the coordinating session on 2026-10-11, the owner's
  words): on the rewritten script, 「先查核與重讀，過了再出片」; on how it goes to the site,
  「用新代號，舊專案標停止」. The film is now `claude-code-skills-vs-claude-md`; the old project
  `claude-code-skills-hands-on` was stopped on the site at 13:21 UTC by the coordinating session.
- **The fact-check** is `docs/videos/claude-code-skills-vs-claude-md/verify-3.md`: an
  independent check (188 claims, pass after fixes), the fixes, a second independent reading of
  the fixes (206 claims, pass), and what was changed after it.

## Definition of done

- [x] The owner's decision on the rewritten script is recorded (brief.md, first paragraphs).
- [x] An independent fact-check of the rewritten script: `verify-3.md`, 2026-10-11.
- [x] A second reading of what changed after the fact-check: appended to `verify-3.md`.
- [ ] A production task exists and names what is listed under Notes.

## Steps

- [ ] File the production task (speech and everything after it), then close this one.

## How to verify

`node tools/video/cli.mjs lint --slug claude-code-skills-vs-claude-md` ends with 0 errors, and
`docs/videos/claude-code-skills-vs-claude-md/verify-3.md` has both readings and both change lists.

## Notes

What the producer starts from, as of 2026-10-11 13:30 UTC:

- Nothing has been made or sent for the new slug: no outline push, no speech request, no work
  folder. One `tts --dry-run` was made on the old slug at 13:18 UTC (103 requests, about 3,790
  billable characters; it synthesized nothing and wrote nothing into the old work folder).
- The outline gate has not been pushed and no approval is recorded. The brief offers two
  options the tool sends in full, D (recommended, the one `video.json` follows) and E; if the
  judge picks E, the script does not match the pick.
- Languages: zh-TW only. Write the languages file for the new slug before captions and QA.
- All 125 narration lines need speech (47 new ids, 78 kept, most reworded). A line the audio
  check mishears is reworded, not just recorded again, and each rewording is recorded.
- Three cards may not fit the frame and are judged at render: `look-call` (a one-line JSON
  quote), `slash-score` (four columns) and `rule` row 3 (a long cell). What overflows is cut or
  split, and no real output is edited.
- `video.json` has the same `source_guide` as the old film (`claude-code-skills-skill-md`).
- The old cut's work folder stays where it is and is not touched.
- Left because each needs a new run: a measured break-even on a larger project; a control run
  without `--setting-sources`; the CLAUDE.md arm with the `# vX.Y.Z` title line written in
  (`claims.md`, c60).
