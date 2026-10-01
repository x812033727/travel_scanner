# Planner prompt: a long series' SETTING BOOK (設定集)

The worker runs this as the planner stage with variant `setting` (`tools/video/automation/prompts.mjs`, `SERIES_INSTRUCTIONS["planner:setting"]`); an agent doing it by hand fills the same payload from the owner's series on `/admin/videos` (`GET /api/v1/admin/video-automation/series/<slug>`) and files the answer with `POST /api/v1/video/automation/series/<slug>/docs` (`kind: "setting"`). The design is `docs/videos/SERIES.md`; the route's reference is `references/series.md`.

## Payload

`series` (slug, title, premise, aspects, tone, style_preset, target_minutes, planned_episodes, episodes_per_chapter, chapters, open_ended, note), `series_reference`, `drama`, `drama_settings` (the voice pool the characters may be cast from), and, on a rewrite, `previous` (`body_md`, `body_json`, `owner_note`) or `previous_problem`.

## What to write

One original world with a conflict engine: sects and clans that want and hide things, cultivation ranks with prices, an orthodox and a demonic path whose line is not where people say. Two leads bound as `tone` says (subtext: never stated, one word or object for what is unsaid), 4–7 supporting characters, 2–3 antagonists with reasons; each with name, standing, want, fear, secret, a verbal habit, and the relationship map. 8–12 long-running mysteries with ids, where they are planted, when they may be revealed, and which are RESERVED for the sequel (at least 3 when the series is open-ended). The register and imagery, the naming rules with examples, and what the series never does. Nothing from any existing work: no borrowed name, sect, artefact or plot.

## Answer

`{"body_md": <zh-TW Markdown with the sections 世界觀, 規則與代價, 人物, 長線謎團, 語氣與畫面, 命名規則, 不做的事>, "body_json": {"characters": [{"id", "name", "role", "appearance" (English, ≤ 800 chars, copied word for word into every episode), "voice": {"provider", "name", "style"}, "personality", "want", "fear", "secret", "speech", "relationships": [{"with", "kind"}], "looks": [{"id", "from", "to"?, "appearance", "sheet_prompt"?, "voice_style"?}] (optional)}], "world": {...}, "rules": [...], "mysteries": [{"id", "question", "planted_chapter", "reveal_chapter"|null, "reserved"}], "tone", "naming": [...], "never": [...], "lexicon": {"term": "reading"|null}}}`

## Looks (換裝與變化)

`appearance` is what the whole series keeps: no episode numbers, time words, occasions or other characters' names. A shot prompt can add a thing but cannot take one off, so a change that lasts a run of episodes (a coat taken off, a cord cut, a wheelchair, a hospital gown, a dress worn only in the first episodes, a voice changed by a stroke) is a look on that character, as `docs/videos/SERIES.md` (換裝與變化) describes:

- `id` lowercase ascii 2–24 characters, unique within the character; `from` and `to` are episode numbers, both included, and no `to` runs to the last episode.
- `appearance` is the whole look in those episodes, under the same rules as the base (English, ≤ 800 characters, no time words): it replaces the base, and the image model reads it alone, so it restates age, build, face and hair rather than adding to the base.
- `sheet_prompt` and `voice_style` are optional and replace the base's in those episodes; `voice_style` needs the character's own Gemini voice.
- one look per episode: two looks of one character never cover the same episode; episodes no look covers use the base.
- a change inside one episode (aged decades within a scene) is not a look but a second character id (for example `lin-old`), cast in that episode beside the first.

The worker checks the shape with `documentProblem` (`looksProblem` in `tools/video/automation/series.mjs`) before filing; a character who never changes has no `looks`.

The leads' ids first; ids never change once the owner approves. The worker refuses an answer without `characters` or `mysteries` and asks once more with `previous_problem`.
