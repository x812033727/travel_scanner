# Writer prompt: one EPISODE of a long series (on top of `writer-drama.md`)

Writer stage, variant `episode` (`SERIES_INSTRUCTIONS["writer:episode"]` = the drama writer's text plus the rules below). By hand: read `docs/videos/<slug>/series.json` (the worker writes it when it starts the episode) and `brief.md`, then write `video.json` as `writer-drama.md` says.

## What the episode adds to the payload

`cast` (the setting book's characters in video.json's shape), `setting_md`, `chapter_md`, `beats` (this episode's row of the approved chapter outline), `recaps` (the last few in full, earlier ones in a line), `earlier_episodes`, `next_logline`, `mysteries`, `series` (title, premise, tone, aspects, note), `series_reference`; when a source-bound directing design is attached, `production` (profile, this episode's hero shot/risk controls, opening timing for E1, cast look/voice plans, props and audio rules).

## Rules on top of the drama writer's

- Copy each character you use from `cast` into `characters` word for word (id, name, appearance, voice, sheet_prompt, approved shot_looks), by id in order; invent nobody. Lint refuses any difference: the character sheets are reused across episodes.
- `beats` is the contract: the hook is spoken or shown within the first shot or two (about 20 seconds); the turn sits near the middle; the last scene is the cliffhanger and nothing follows it, no summary, no moral. Plant `beats.setups`, pay `beats.payoffs`, touch no RESERVED mystery.
- Continue from `recaps`; set up `next_logline` without telling it.
- The leads' bond follows `series.tone`: for subtext nothing is said; an act, a look, an object.
- Spell every name and term as the setting book does; new terms go to `lexicon_additions`.

FIX mode with `fix.kind = "script"` is the owner's script-gate note (`owner_note`): rewrite what the note asks, keep every id you can, and the whole video.json comes back.


## Source-bound animation production

When the launch/payload has `production`, read its `profile`, `episode`, `opening_30s` (E1 only), `visual_direction`, `characters`, `prop_rules`, `audio_plan` and `acceptance_checks` before drawing shots. `production.episode.hero_shot`, its `risk_controls` and source references are concrete directing constraints; turn them into visible actions, never speak the production notes as dialogue or invent an extra story event. The approved story still governs who is present, what they know and when props change hands.

- Finish the zh-TW Taiwan-accent cut first. Set `subtitles.burn_in: false`; all dialogue/narration captions are switchable CC. ja/ko/en cast audio and independently timed CC follow approval of the Chinese master; multi-character drama dubbing is planned, not an already implemented automatic stage. Keep line and speaker ids stable for that later work.
- Keep the cast's base appearance and approved `shot_looks: [{id, appearance}]` unchanged. For each shot choose `data.character_looks: {characterId: lookId}` from that character's catalog; the visible character must be in `data.characters`. A change of clothes, injury or prop handoff within an episode changes the selected look at the exact shot, not the actor's id, face or voice. Do not invent look ids. The catalog's episode lists are candidates, not automatic whole-episode overrides.
- This profile is clips-only: one clear action and one camera intention per shot. Veo Lite 1080p produces exactly eight seconds at 24fps; plan useful cuts inside that source, normally 3–6 seconds, never a shot over 8 seconds, a static portrait called animation, or freeze padding. Split a reach, handoff and reaction into separate shots. Use anticipation, contact, weight, eye focus and follow-through appropriate to the action.
- `veo-3.1-lite-generate-preview` supports a first-frame keyframe, but no referenceImages or extension. Do not instruct unsupported multi-reference video generation. The existing tool may convert 24fps source to its 30fps edit grid; do not claim extra captured motion.
- Important labels/numbers are verified graphics composited onto a moving prop insert; never trust generated lettering. This is diegetic evidence, not burned-in dialogue. CC closed must still leave the spoken/visual causal chain understandable.
- Use independent cast TTS, narrator, room tone, effects and music; discard native clip speech. Mouth close-ups need separate synchronization acceptance: lip-sync is not implemented by declaring it in a prompt. Reaction, over-shoulder and object inserts can carry dialogue honestly. Names in the pronunciation plan remain proposed until native listening.
- No title/thumbnail/trailer may reveal a scheduled answer. A million views is a goal, not a prediction or acceptance criterion. Render/audio/CC acceptance cannot be inferred from a source or storyboard check.

## With the retention rules, a visual tier, or compilation mode (docs/videos/BINGE.md)

The genre section at the end of the prompt (`genreBlock`) adds, when the series has them:

- Retention (`genre_spec.retention`): the first line of the first shot is the hook itself (no title card, no greeting; about 5 seconds, so at most about 28 characters: the tool measures it at 250 characters a minute and refuses a hook whose words end after 8 s); the conflict is stated or shown by about 10 seconds; the `beats.satisfaction` moments are played as lines and pictures the viewer can point at, the first inside 30 seconds; an emotional beat every 20 to 30 seconds; the last line of the last shot is the cliffhanger and nothing follows it. The checker names the hook, satisfaction and cliffhanger lines and the tool measures them (hook inside 8 s, first satisfaction inside 30 s, at least 2, cliffhanger last), so a hook buried in the second shot is sent back.
- Visual tier (`series.visual_tier`): mark each shot's `visual` as the tier says (`hybrid`: at most 40% `"clip"`, the climax of each beat; `stills`: at most 10%; `clips`: every shot a clip, `visual` may be left out) and give every `"still"` shot a `camera` move the tool renders (push in, pull out, pan left, pan right, tilt up, tilt down; anything else drifts). Lint refuses more clips than the tier allows.
- Compilation mode (`series.compilation`): no title card and no outro card; the episode opens cold on its hook and ends on its cliffhanger, and never recaps earlier episodes. Lint refuses a `title` card as the first scene.

FIX mode with `fix.kind = "script"` may also come from the checker on a hands-off series: `owner_note` is then the list of problems `scriptVerdict` found (a missing beat, a hook that ends too late, a satisfaction beat only mentioned, a summary after the cliffhanger), at most `MAX_PROMPT_FIX_ROUNDS` times before the script goes up as it is.
