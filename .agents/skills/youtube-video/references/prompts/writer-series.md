# Writer prompt: one EPISODE of a long series (on top of `writer-drama.md`)

Writer stage, variant `episode` (`SERIES_INSTRUCTIONS["writer:episode"]` = the drama writer's text plus the rules below). By hand: read `docs/videos/<slug>/series.json` (the worker writes it when it starts the episode) and `brief.md`, then write `video.json` as `writer-drama.md` says.

## What the episode adds to the payload

`cast` (the setting book's characters in video.json's shape), `setting_md`, `chapter_md`, `beats` (this episode's row of the approved chapter outline), `recaps` (the last few in full, earlier ones in a line), `earlier_episodes`, `next_logline`, `mysteries`, `series` (title, premise, tone, aspects, note), `series_reference`.

## Rules on top of the drama writer's

- Copy each character you use from `cast` into `characters` word for word (id, name, appearance, voice, sheet_prompt), by id in order; invent nobody. Lint refuses any difference: the character sheets are reused across episodes.
- `beats` is the contract: the hook is spoken or shown within the first shot or two (about 20 seconds); the turn sits near the middle; the last scene is the cliffhanger and nothing follows it, no summary, no moral. Plant `beats.setups`, pay `beats.payoffs`, touch no RESERVED mystery.
- Continue from `recaps`; set up `next_logline` without telling it.
- The leads' bond follows `series.tone`: for subtext nothing is said; an act, a look, an object.
- Spell every name and term as the setting book does; new terms go to `lexicon_additions`.

FIX mode with `fix.kind = "script"` is the owner's script-gate note (`owner_note`): rewrite what the note asks, keep every id you can, and the whole video.json comes back.
