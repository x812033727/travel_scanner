# Listener prompt: ONE CHAPTER of a brand story, for the ear

Listener stage, variant `story` (`STORY_INSTRUCTIONS["listener:story"]` in `tools/video/automation/story-prompts.mjs`; this is the readable copy). One chapter a call, after its fact check. The common rules are the writer's (`writer-story.md`).

## What it gets

`chapter` (`key`, `number`, `title`), `scenes` (the chapter's lines by scene and line id), `previous_lines` (the last sentences of the chapter before), `next_lines` (the first of the chapter after), `script_writing` (the house style), and `owner_note` when the owner sent the narration back.

## The work

The viewer hears the story once, from a synthesized Taiwanese Mandarin voice, over still pictures. Rewrite lines that are too long, ambiguous when heard, stiff or written-sounding, or that repeat the line before; let the chapter's first line lead on from `previous_lines`. Keep every fact, figure, year, name and attribution exactly (「照某某的說法」 stays) and every line id. A line may be dropped only when it repeats the one before and holds no figure and no name. With `owner_note`, do what the owner asks, within the facts.

## Answer

`{"patch": {"<line id>": "<the new line>"}, "drop": ["<line id>"], "edits": ["<id>: <before> → <after>"]}`, only what changes. The worker checks every patched line against the one it replaces (`tools/video/automation/rewrite.mjs`): a line whose numbers, Latin words or dictionary terms changed keeps its old text, and a line with a figure or a Latin word is never dropped; the refusals go to the video's notes.
