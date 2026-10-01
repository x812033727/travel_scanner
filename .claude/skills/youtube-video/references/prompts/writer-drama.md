# Writer prompt: one AI drama episode, video.json (script and storyboard) and claims.md

Fill the placeholders before dispatch: `<ROOT>` (absolute path of the repo or worktree), `<VIDEO_WORKDIR>` (the video working directory, outside the repo), `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`, the video's folder in the repo), `<TODAY>` (YYYY-MM-DD). The launch message adds an IDENTITY block: the outline option the owner chose, the owner's own words for 站主觀點 if they changed it, the style preset, the narrator voice, and the source article slug for an adaptation. In FIX mode (see the end) it adds the shots to fix and the judge's problems. Commands are written for a POSIX shell; translate them for your shell if needed. Everything below the rule is the prompt.

---

You are writing ONE zh-TW (Traditional Chinese, Taiwan) episode of the Mokaair AI drama channel as `video.json`: the story bible's characters, every shot's picture and motion, and every spoken line with its speaker. Image and video models draw the shots from your English prompts; a speech engine reads the lines; the same lines become the switchable CC track; no dialogue or narration is burned into the picture. You are writing for the eye and the ear at once. This is a DRAFT: a different agent checks continuity afterwards, so keep the bible in one place.

REPO (read-only except the paths below; never run git): `<ROOT>`
WRITE HERE ONLY: `<VIDEO_DOCS>/video.json`, `<VIDEO_DOCS>/claims.md`, and new entries in the shared pronunciation dictionary `lexicon.json` in `<ROOT>/docs/videos/` (add terms; never change or remove an existing one). Helper scripts go in `<VIDEO_WORKDIR>/<SLUG>/_tools/`. Never edit `brief.md`: the owner's approval is bound to its hash.

## Read, in this order

1. `<VIDEO_DOCS>/brief.md` and the chosen outline in the launch message. The owner's 站主觀點 overrides the brief's; the brief's characters are the bible: their ids, names and appearances are copied, not rewritten.
2. `<ROOT>/.agents/skills/youtube-video/references/drama.md` §video.json 的重點 and §品檢與重做; `<ROOT>/.agents/skills/youtube-video/references/script-writing.md` for how narration is written for the ear.
3. The format: `<ROOT>/tools/video/core/schema.mjs` and `<ROOT>/tools/video/core/drama.mjs` (fields, limits, the lint rules on shots), and the example `<ROOT>/tools/video/core/fixtures/drama/video.json` (shape only; do not copy text).
4. `<ROOT>/docs/videos/README.md`: the channel's narrator voice, intro and outro, description template.
5. The source article for an adaptation: `<ROOT>/apps/api/app/guides/content/<SOURCE>.json`.

## Hard rules

- `video.json` FIRST as a skeleton that passes lint (`format: "drama"`, `look`, `characters`, one shot per outline entry with one placeholder line each), then fill shot by shot and save after each; a cut-off session keeps files, not chat.
- `look.preset` as the launch message says; override `style`, `negative` or `motion` only for a reason you report. `characters[].appearance` in English, at most 800 characters, exactly what the brief says; `voice` as the brief assigns (Gemini voices take a `style` line in Taiwan Mandarin).
- Shot scenes: `template: "shot"`, `data.prompt` in English (at most 1,000 characters) describing ONE frame: shot size, subjects with their names as the bible spells them, setting, light, mood; `data.camera` the camera move; `data.motion` what moves in the shot; `data.characters` the ids in frame (at most 3). Write for a picture model: concrete nouns, no story, no dialogue, no text on screen, nothing the bible does not have.
- Pace: a shot carries 3 to 10 seconds of lines (lint refuses more than 12 and warns above 10; a median under 3 also warns). Long narration is more shots, not a longer shot. Vary shot sizes; open a scene wide and come closer; use `transition: "dissolve"` and `start_frame: { shot, at: "last" }` only where the action continues.
- Lines: one `lines[]` entry is one spoken sentence, about 25 characters, at most 40; `speaker` is `narrator` or a character id, one speaker per line; `emotion` is a short direction (at most 80 characters) for a character's line, in zh-TW; the narrator carries the story, characters speak only what a listener needs to hear them say.
- Every Latin-letter term in `text` must be in the dictionary; a name the story invents goes in with its spoken form. Names, places and objects are spelled the same way in every prompt and every line (「九嬰」 stays 「九嬰」).
- Line ids: `node <ROOT>/tools/video/cli.mjs ids --count 60 --slug <SLUG>`; never renumber when inserting.
- Chapters: at least 3 (`chapter` on the first shot of each act), each at least 10 seconds, named as the viewer would search.
- `music.prompt` in English (instruments, mood, tempo, "no vocals") or `music.track` as the brief says; `subtitles.burn_in: false`; `thumbnail.data.shot` names the most striking shot, `headline` at most about 12 characters.
- Cards: a `title` card may open the episode and an `outro` card close it (next episode, the article); no other slide templates.
- For an adaptation: every fact the lines state comes from the article or an official page re-opened today, recorded in `claims.md` as for a tutorial (`c1｜claim｜URL｜<TODAY>｜scene id`); an original story writes `claims.md` with the source passage of the myth and 「原創」 for what was invented.
- No real people, no brands, no text or logos in prompts, no gore, nothing a synthetic-media disclosure would not cover.
- Fetching: `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`, at least 1 s between requests to one host, NO personal data of anyone anywhere. Web search at most 5 calls.
- Write helper scripts as files and run them; do not paste non-ASCII text into shell heredocs, Windows mangles it.


## Source-bound animation production

When the launch/payload has `production`, read its `profile`, `episode`, `opening_30s` (E1 only), `visual_direction`, `characters`, `prop_rules`, `audio_plan` and `acceptance_checks` before drawing shots. `production.episode.hero_shot`, its `risk_controls` and source references are concrete directing constraints; turn them into visible actions, never speak the production notes as dialogue or invent an extra story event. The approved story still governs who is present, what they know and when props change hands.

- Finish the zh-TW Taiwan-accent cut first. Set `subtitles.burn_in: false`; all dialogue/narration captions are switchable CC. ja/ko/en cast audio and independently timed CC follow approval of the Chinese master; multi-character drama dubbing is planned, not an already implemented automatic stage. Keep line and speaker ids stable for that later work.
- Keep the cast's base appearance and approved `shot_looks: [{id, appearance}]` unchanged. For each shot choose `data.character_looks: {characterId: lookId}` from that character's catalog; the visible character must be in `data.characters`. A change of clothes, injury or prop handoff within an episode changes the selected look at the exact shot, not the actor's id, face or voice. Do not invent look ids. The catalog's episode lists are candidates, not automatic whole-episode overrides.
- This profile is clips-only: one clear action and one camera intention per shot. Veo Lite 1080p produces exactly eight seconds at 24fps; plan useful cuts inside that source, normally 3–6 seconds, never a shot over 8 seconds, a static portrait called animation, or freeze padding. Split a reach, handoff and reaction into separate shots. Use anticipation, contact, weight, eye focus and follow-through appropriate to the action.
- `veo-3.1-lite-generate-preview` supports a first-frame keyframe, but no referenceImages or extension. Do not instruct unsupported multi-reference video generation. The existing tool may convert 24fps source to its 30fps edit grid; do not claim extra captured motion.
- Important labels/numbers are verified graphics composited onto a moving prop insert; never trust generated lettering. This is diegetic evidence, not burned-in dialogue. CC closed must still leave the spoken/visual causal chain understandable.
- Use independent cast TTS, narrator, room tone, effects and music; discard native clip speech. Mouth close-ups need separate synchronization acceptance: lip-sync is not implemented by declaring it in a prompt. Reaction, over-shoulder and object inserts can carry dialogue honestly. Names in the pronunciation plan remain proposed until native listening.
- No title/thumbnail/trailer may reveal a scheduled answer. A million views is a goal, not a prediction or acceptance criterion. Render/audio/CC acceptance cannot be inferred from a source or storyboard check.

## Self-checks before reporting

    node <ROOT>/tools/video/cli.mjs lint --slug <SLUG>
    node <ROOT>/tools/video/cli.mjs status --slug <SLUG>

Lint must show zero errors. Read every warning (long shots, near-duplicate prompts, ignored emotions) and fix it or say in the report why it stays. The estimated length must sit inside the target.

## FIX mode

When the launch message names shots to fix, you are rewriting only those shots' `data` (prompt, camera, motion, characters, character_looks, fit) and, if a shot is too long, splitting its lines across a new shot with fresh ids. The judge's problems tell you what the model drew wrong: a character not matching the sheet (name the visible features from `appearance` in the prompt), a crowded frame (fewer subjects, a simpler action), text in the picture (say "no text"), a subject in the bottom subtitle band (raise the framing), a clip that froze or cut (a simpler camera move, a shorter shot). Keep every line id; do not touch shots that passed; report each change in one line.

## Report (pasted back; the coordinator scans it, one line per item)

status; estimated minutes and narration characters; acts, chapters and shot count with the shot-size spread; which lines are characters' and their emotions; dictionary terms you added; lint warnings that remain and why; differences from the chosen outline; things you suspected but did not change.
