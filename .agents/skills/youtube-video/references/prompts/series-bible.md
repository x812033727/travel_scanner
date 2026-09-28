# Planner prompt: a one-off drama's STORY BIBLE (故事聖經)

The worker runs this as the planner stage with variant `bible` (`tools/video/automation/prompts.mjs`, `SERIES_INSTRUCTIONS["planner:bible"]`) when the site's next series job is a one-off's bible (`GET /api/v1/video/automation/series/next`, `kind: "bible"`); an agent doing it by hand fills the same payload from the one-off on `/admin/videos` (`GET /api/v1/admin/video-automation/series/<slug>`) and files the answer with `POST /api/v1/video/automation/series/<slug>/docs` (`kind: "bible"`). The design is `docs/videos/DRAMA-FLOW.md` §二: a one-off drama is a series of one episode, and the bible is its only document; once the owner approves it, episode 1 is ready and the writer works from it.

## Payload

`series` (slug, kind `one-off`, title, premise, style_preset, target_minutes, note), `series_reference`, `drama`, `drama_settings` (the voice pool the characters may be cast from), and, on a rewrite, `previous` (`body_md`, `body_json`, `owner_note`) or `previous_problem`.

## What to write

The premise in three to five sentences (who wants what, what stands in the way, how it ends; the source and what is invented), 2 to 4 characters with an appearance an image model draws the same way every time and a voice, three acts, ONE outline (no options: the owner approves the bible, not a pick), the source material and music direction, and what the episode leaves out. Original, or from the public-domain source the premise names.

## Answer

`{"body_md": <zh-TW Markdown with the sections 故事前提, 角色, 幕, 大綱, 素材, 不做的事>, "body_json": {"characters": [{"id", "name", "role", "appearance" (English, ≤ 800 chars), "voice": {"provider", "name", "style"}, "personality"}], "acts": [{"number", "title", "summary", "shots"}], "outline": {"title", "logline", "hook", "conflict", "turn", "cliffhanger": {"type", "text"}, "characters", "locations", "theme"}, "music", "not_doing": [...], "lexicon": {"term": "reading"|null}}}`

The worker refuses an answer without `characters`, `acts` or an `outline` object and asks once more with `previous_problem`. When the owner approves, the site makes episode 1 ready with the outline as its beats, and the worker drafts the episode from the bible: the brief's 角色 are the bible's cast, its 大綱 is the one outline, approved locally with the note 「依故事聖經」.
