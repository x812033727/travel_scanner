---
id: 2026-10-20-produce-claude-code-beginner-guide-for
title: Produce Claude Code beginner guide for non-technical users: four basics and a real event folder
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-10-20T17:40:44Z
created_at: 2026-10-20T17:40:24Z
completed_at: 2026-10-21T13:49:18Z
branch: claude/ai-video-production-520ea2
depends_on: []
scope:
  - docs/videos/claude-code-beginner-event-folder
---

# Produce Claude Code beginner guide for non-technical users: four basics and a real event folder

## Why

The owner (2026-10-21) set Gary Chen's Codex beginner guide (479,000 views) as the structure to
match or beat: an agent that lives in your computer, the four basics (project folder, permission
modes, context, AGENTS.md), one running example, hands-on, Skills/connectors/automation, "it is
also your tutor". This video is the Claude Code version for people who do not write code, made
under the tutorial flow rules written from that study (`teaching-flow.md`), with every number
from real headless runs on an invented event folder. Slug `claude-code-beginner-event-folder`.

## Definition of done

- [x] Brief with outline options, four outcomes and a mechanical 要先實作 list; Jev picked A.
- [x] 18 headless Claude Code 2.1.295 sessions recorded in `runlog.txt` and `demo/` (seed, prompts,
      replies, output files); outcomes 1, 3, 4 hold, outcome 2 downgraded to 「有幫助，但不是每一項」.
- [x] Script (`video.json`, `claims.md`), three fact-check rounds (7, 6, 0 corrections), listener
      pass, four revisions after the blind panel (tutorial wording), lint clean, `category: "tutorial"`.
- [x] Narration synthesized and cleared by the audio check (4 rounds; 26 + 7 + 3 lines reworded).
- [x] Frames, thumbnail, final.mp4, zh-TW captions; QA 10 of 11 (the 11th is the owner's
      narration approval). After the owner called the 19:26 cut 「無聊、沒內容」 the narration was
      rewritten to teach moves (teaching-flow §九): 13:20, 128 lines, 10 chapters, one move or more
      per chapter named by the blind reader; fact-check round 4 (3 corrections), audio check clean.
- [ ] Owner approvals on /admin/videos: outline, narration, final cut, then upload package and
      publish gate (hand-pushed video: the owner decides at every gate).
- [ ] On YouTube (the owner uploads; `UPLOAD.md` after `package`).

## Steps

- [x] Plan, run, write, verify, listen, panel, voice, render, assemble, captions, QA, review-push
      (outline, audio, final all pending the owner).
- [ ] After the owner approves final: `package`, `review-push --gate publish`.

## How to verify

```bash
node tools/video/cli.mjs status --slug claude-code-beginner-event-folder
node tools/video/cli.mjs lint --slug claude-code-beginner-event-folder
node tools/video/cli.mjs qa --slug claude-code-beginner-event-folder
```

## Notes

- Blind panel (tutorial wording) ended at 10 of 13 after four readers; the three "no"s moved
  between readers (one_line / no_recap / no_detour on the hands-on chapter and the CLAUDE.md score
  comparison). Two readers independently stopped at the hands-on chapter's replay of earlier
  steps; that block was cut in revision 4. Verdicts in the work directory `review/narrative*.json`.
- Length 19:26 is over the brief's 12–16 target; the rule since 2026-10-04 is that the upper end is
  an aim, and the connector walkthrough (about 2 min, CITED only) was the one chapter cut.
- The four 「建議」 lines (read other people's Skills first, connect only what you use, keep a copy
  of originals, press send/delete yourself) are not among the brief's four proposed stance points;
  the owner decides whether to adopt them into the channel stance.
- Audio check lesson: 確認信名單 is heard as 確認姓名單 every time; 要寄信的那份名單 passes.
  Attendee names in narration (宋柏均, 劉思妤, 王志明) are misheard; the cards keep the names and
  the narration says the role instead.

## Outcome (2026-10-21, owner review)

The owner watched the 13:20 cut and the Skill pair and said the content was still dull and hard to
follow, possibly the topic, and the pictures weak; the target is the two reference videos' view
counts. Decided: this video is **not uploaded**. It stays as material (the event folder, the 18
`claude -p` runs, g1's self-written CLAUDE.md with the wrong rule 3, the n1/v1/s1 comparison) for
the short "one concept" tutorials that replace it, starting with 「CLAUDE.md 就是員工守則」.
Second-round findings (topic crowded by 400k+ presenter videos, every chapter narrating run-log
detail, 102 states all text cards) are in `docs/videos/reference-study-20261021/README.md`
§第二輪 and the rules in `teaching-flow.md` §十–§十二. The site project `claude-code-beginner-event-folder`
should be marked stopped in `/admin/videos` (owner action).
