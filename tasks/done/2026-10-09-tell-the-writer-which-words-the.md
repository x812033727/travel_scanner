---
id: 2026-10-09-tell-the-writer-which-words-the
title: Tell the writer which words the audio check mishears
status: done
priority: P2
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T10:15:40Z
created_at: 2026-10-09T10:15:35Z
completed_at: 2026-10-09T10:16:00Z
branch: claude/video-misheard-words
depends_on: []
scope:
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
---

# Tell the writer which words the audio check mishears

## Why

The two tutorials made on 2026-10-09 had 13 and 19 of their 151 lines flagged by the first audio
check, nearly all because the transcription heard a homophone (實跑 as 食譜, 餵 as 為, 印出 as
引出, 放行 as 方形). Re-recording the same words did not help: the three lines that were only
re-recorded in the first video were flagged again. Each video took three rounds and reworded 12
and 22 lines. The second writer had been told the first video's words and still met a new batch,
because the list lived in a launch message and not in the guide.

## Definition of done

- [x] `script-writing.md` §給 TTS 唸的稿子 lists each misheard word, what it was heard as and
  what to say instead, and says a flagged line is reworded, not only re-recorded.
- [x] `writer-video.md` points at the list.

## Steps

- [x] Write the list from the two videos' rewrite records.

## How to verify

`node --test tools/skills.test.mjs`. The records the list comes from are
`docs/videos/claude-code-mods-hands-on/narration-rewrites-1.json` and `-2.json`, and the same
two files under `docs/videos/claude-code-hooks-hands-on/` once PR 1398 has merged.

## Notes

- This reaches agents that write by the prompt docs. The host worker's writer prompt
  (`tools/video/automation/prompts.mjs`) does not carry the list; its own loop re-records and
  then rewords flagged lines. Putting the list there is a separate change, with a receipt
  increment and a deploy.
