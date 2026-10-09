---
id: 2026-10-09-produce-the-headless-and-claude-md
title: Produce the headless-mode and CLAUDE.md hands-on tutorials under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T13:27:32Z
created_at: 2026-10-09T13:27:00Z
completed_at:
branch: claude/headless-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-headless-hands-on
  - docs/videos/claude-code-claude-md-hands-on
  - docs/videos/lexicon.json
---

# Produce the headless-mode and CLAUDE.md hands-on tutorials under the content-value rules

## Why

The owner asked for more AI tutorials made by hand under the content-value rules, in the same
order as the settings-hooks one (plan, run, write): first `claude -p`, Claude Code without its
interactive screen, then how to write a CLAUDE.md. Each goes as far as the publish gate on
`/admin/videos`; uploading stays the owner's.

## Definition of done

Headless mode (`claude-code-headless-hands-on`):

- [x] A brief by a planner with the rules and no run evidence; outline A, as the owner delegated.
- [x] The listed runs made and logged: ten headless sessions and the model-free checks.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`), their findings applied.
- [x] Narration synthesized and checked against the script until no line was flagged.
- [x] The cut, and the final and publish gates: final 11 of 11 with the judge's demonstration
  score at 0.92, publish 4 of 4, both approved by the server.

CLAUDE.md (`claude-code-claude-md-hands-on`):

- [x] Brief, eleven sessions, script, two fact checks.
- [x] Narration synthesized and checked until no line was flagged; the audio gate approved it.
- [x] Its files in the repository.
- [ ] The cut, and the final and publish gates.

- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Headless: plan, run, write, verify twice, narrate.
- [x] Headless: `render`, `assemble`, `captions`, `review-push --gate final`, `package`,
  `review-push --gate publish`; languages: zh-TW only (the owner, in chat).
- [ ] CLAUDE.md: the same, after its narration passes the audio check.

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-headless-hands-on
node tools/video/cli.mjs status --slug claude-code-headless-hands-on
```

`docs/videos/claude-code-headless-hands-on/runlog.txt` holds every run a card quotes, and `demo/`
the practice project as it was used.

## Notes

- Both produced on 2026-10-09 with Claude Code 2.1.295 on Windows, Git Bash.
- The headless video's files go in first, before its cut is approved: the description links to
  its `demo/` folder on GitHub (the owner asked for the link), and the final gate's link check
  needs that address to open.
- Headless, what only the runs showed and the video now teaches: the stream's last line is not
  the result on this version (a `task_summary` line follows it); a refused tool call still exits
  0 with `is_error` false; `--max-turns 1` reports two turns; a project `permissions.allow` is
  ignored in an untrusted folder; a second category table did not move the invoice report.
- Headless, never observed and not told as seen: any scheduler, GitHub Actions or Routines run,
  an API key or `--bare`, macOS or Linux, a PowerShell session, the default permission mode.
- Headless narration: 11 of 110 lines flagged on the first audio check, 3 on the second, none on
  the third (`narration-rewrites-1.json`, `-2.json`). New mishearings: 本機 as 本期, 旗標 as 指標,
  「我沒有給」 as 「我們有給」, which reverses the meaning.
- The first final submission passed 9 of 11: one card state ran 15.2 s (two lines shortened; a
  compare card has two reveal steps, so the verdict cannot take its own), and the demo link did
  not open before this change was merged.
- CLAUDE.md, what only the runs showed: the CHANGELOG line made no difference (3 of 3 with and
  without the file), so it is told as a line this project does not need; in the conflict arm the
  path alone proves nothing, because the runs without any file landed on the same path; with
  loading disabled the model opened the file itself and followed all three lines.
- CLAUDE.md: one run's raw files (b1) were lost to a `--dry` that rebuilt the project before
  checking its flag; its record survives as a captured excerpt and no card uses it. The next
  video's runner script refuses to overwrite a named run.
- CLAUDE.md narration: 15 lines flagged on the first check, then 2, then none; later edits for a
  card that did not fit (three official example pairs became two) and for two card states over
  15 s were each re-recorded and re-checked. 「有檔」 and 「有檔案」 at the start of a clause were
  misheard four times; naming the file passed (PR 1403 adds both to the list).
- Both videos now check the longest card state from `timeline.json` before assembling, which
  takes seconds; finding it at the final gate costs a 25-minute re-encode.
