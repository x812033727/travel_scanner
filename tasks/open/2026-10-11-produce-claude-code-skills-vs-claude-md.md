---
id: 2026-10-11-produce-claude-code-skills-vs-claude-md
title: Produce the rewritten Skills tutorial from its outline gate to the upload package
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-11T13:40:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-skills-vs-claude-md
---

# Produce the rewritten Skills tutorial from its outline gate to the upload package

## Why

On 2026-10-11 the owner had every tutorial the blind reading did not pass sent back to be
rewritten (`tasks/done/2026-10-11-tutorial-worth-rules.md`), and asked that the speech stage
and everything after it be run under its own task, by another AI than the one that wrote the
script. This is that task for the first rewritten film.

The script is finished and checked. Nothing has been synthesized, rendered or sent to the
site for it.

## What is ready

- The film: `docs/videos/claude-code-skills-vs-claude-md/` (pull request 1446). It was first
  made as `claude-code-skills-hands-on` on 2026-10-10 and rewritten on 2026-10-11 around a
  question its first version never answered: the same release procedure in CLAUDE.md and in
  a Skill, the same request three times on each side. Both sides did all five steps every
  time; the difference is cost.
- Its evidence: 23 headless sessions recorded in `runlog.txt`, with their files under `demo/`.
- Its checks: three blind readers said "publish" (two failed 2 of 16 questions, the third
  1 of 16); an independent fact-check of 188 claims and a second reading of 206, both in
  `verify-3.md`, the second with nothing left to change before recording.
- Lint: 0 errors, 0 warnings; 57 scenes, 125 narration lines, about 11.7 minutes by the
  lint's estimate.
- The writer's notes for whoever produces it are in
  `tasks/open/2026-10-11-decide-and-fact-check-the-rewritten.md`; read them, then close
  that task.

## Where it starts from

- A new slug. The owner decided on 2026-10-11 that a rewritten film is produced under a new
  slug and the old project is stopped (「用新代號，舊專案標停止」). The old project
  `claude-code-skills-hands-on` was stopped on the site that day at 13:21 UTC, with the reason
  in its note. Its local work folder still holds the old cut: leave it alone.
- No project, no review and no work folder exist yet for `claude-code-skills-vs-claude-md`.
- The brief offers two outline options, D (recommended; the one `video.json` follows) and E.
  The owner's decision on the script is option D: on 2026-10-11 the owner was shown the
  rewritten script's result and chose 「先查核與重讀，過了再出片」, and both checks then passed.
  If the outline judge picks E, stop: the script does not follow E.
- Speech: a dry run on the same narration gave 103 requests and about 3,790 billable
  characters; the site reported more than nine million Gemini characters left for the month.
  The voice is the channel's (gemini:Sulafat).
- Languages: zh-TW only. Write the languages file that says so before the captions and QA
  stages; an earlier film failed its captions item for lack of it.
- `video.json` carries the same `source_guide` as the stopped film
  (`claude-code-skills-skill-md`). Nobody has checked whether the site accepts a second
  project resting on that article now that the first is stopped.

## Definition of done

- [ ] The outline gate is approved for option D, by the site's judge or on the owner's word
      as recorded above, whichever the skill prescribes.
- [ ] Narration is synthesized, the pace check is run on the real timeline, and the audio
      check ends with no line flagged. A line the checker mishears is reworded to a form it
      hears right (`HEARD_RULES` in `tools/video/automation/register.mjs`), not just recorded
      again; a rewording changes no fact and is recorded as the earlier films'
      `narration-rewrites-*.json` do.
- [ ] The film is rendered and assembled. Three cards were flagged as possibly too full:
      `look-call`, `slash-score` and row 3 of `rule`. What the render reports as overflowing
      is cut or split, not shrunk, and no real output is edited: whole lines are excerpted.
- [ ] Final QA passes all its items, and the policy scores are written down (the
      demonstration score in particular).
- [ ] The upload package passes its checks, and the audio, final and publish gates are
      approved on the site.
- [ ] Nothing is uploaded to YouTube and the publish button is not pressed: the owner does that.
- [ ] The measured length, the billable characters used, every reworded line and each gate's
      decision with its time are written in this task's Notes.

## Steps

- [ ] Read `.agents/skills/youtube-video/SKILL.md` and what it points to for producing a
      slides film on the owner's machine; follow it.
- [ ] Wait until pull request 1446 is on main, or work from its branch
      `claude/skills-hands-on-rewrite`.
- [ ] Outline gate, speech, pace, audio check, render, assemble, captions, QA, package, the
      gates.
- [ ] Commit what production changes in the film's folder (reworded lines and their record).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-skills-vs-claude-md
node tools/video/cli.mjs status --slug claude-code-skills-vs-claude-md
```

and the site's page for the video shows its gates approved and an upload package waiting.

## Notes

- This is the first film produced this way. The route itself (new slug, old project stopped)
  is not yet in the skill or in `docs/videos/`:
  `tasks/open/2026-10-11-write-down-how-an-approved-film.md`. How the old project was
  stopped: the site's own stop action (`POST /admin/videos/{slug}/drop`, the 停止 button on
  `/admin/videos`), with a note giving the reason and the new slug.
- The description is within a few bytes of YouTube's 5,000-byte limit; adding to it needs a
  cut elsewhere.
- The script that generated `video.json` was not kept in the repository. Editing
  `video.json` by hand is fine; a code, terminal or quote card that changes is checked
  against `demo/` and `runlog.txt`.
- Five other tutorials' briefs still name the old slug's folder as a path. They refer to the
  first version of this film and are outside this task.
- The narration must not talk about the film's own making, so a line reworded in the audio
  check does not gain a phrase about what was or was not run.
