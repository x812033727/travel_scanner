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

## With the retention rules, a visual tier, or compilation mode (docs/videos/BINGE.md)

The genre section at the end of the prompt (`genreBlock`) adds, when the series has them:

- Retention (`genre_spec.retention`): the first line of the first shot is the hook itself (no title card, no greeting; about 5 seconds, one line of about 25 characters); the conflict is stated or shown by about 10 seconds; the `beats.satisfaction` moments are played as lines and pictures the viewer can point at, the first inside 30 seconds; an emotional beat every 20 to 30 seconds; the last line of the last shot is the cliffhanger and nothing follows it. The checker names the hook, satisfaction and cliffhanger lines and the tool measures them (hook inside 8 s, first satisfaction inside 30 s, at least 2, cliffhanger last), so a hook buried in the second shot is sent back.
- Visual tier (`series.visual_tier`): mark each shot's `visual` as the tier says (`hybrid`: at most 40% `"clip"`, the climax of each beat; `stills`: at most 10%; `clips`: every shot a clip, `visual` may be left out) and give every `"still"` shot a `camera` move the tool renders (push in, pull out, pan left, pan right, tilt up, tilt down; anything else drifts). Lint refuses more clips than the tier allows.
- Compilation mode (`series.compilation`): no title card and no outro card; the episode opens cold on its hook and ends on its cliffhanger, and never recaps earlier episodes. Lint refuses a `title` card as the first scene.

FIX mode with `fix.kind = "script"` may also come from the checker on a hands-off series: `owner_note` is then the list of problems `scriptVerdict` found (a missing beat, a hook that ends too late, a satisfaction beat only mentioned, a summary after the cliffhanger), at most `MAX_PROMPT_FIX_ROUNDS` times before the script goes up as it is.
