# Discussion prompts: the planner and the writer answer the owner's line (討論串)

The worker runs these as the planner stage with variant `discuss` on a document's thread and as the writer stage with variant `discuss` on a screenplay's thread (`tools/video/automation/prompts.mjs`, `VARIANT_INSTRUCTIONS["planner:discuss"]` and `["writer:discuss"]`; `tools/video/automation/discuss.mjs` runs one line per round, before any series work). An agent doing it by hand reads the line with `GET /api/v1/video/automation/series/messages/next` and answers with `POST /api/v1/video/automation/series/messages/<id>/answer`. The design is `docs/videos/DRAMA-FLOW.md` §三.

## Payload

A document's thread: `subject` (`setting`, `outline`, `chapter:<n>`, or a one-off's `bible`), `message` (the owner's line), `thread` (every line so far: `author` owner／planner／writer, `body_md`, `refers_to` the version it was said about), `document` (the latest version: `kind`, `version`, `status`, `body_md`, `body_json`; null before the first version), `series`, `series_reference`, `drama`, `drama_settings`, and the approved documents above this one (`setting`, and for a chapter `outline`, `chapter_number`, `chapter_range`).

A screenplay's thread: `subject` (`script:<集數>`), `message`, `thread`, `video` (video.json as it stands), `screenplay` (script.md), `brief`, `line_ids` (fresh ids for new lines), plus what the writer normally gets for the video (`cast`, `setting_md`, `beats`, `recaps`, `series` for an episode of a series).

## Rules

- Reply in Traditional Chinese (Taiwan), within 300 characters, unless the owner asked for text (a passage, a line three ways): then give exactly that.
- A question gets an answer only: `revised` is null.
- A request for a change gets a new version, and the reply lists what changed, briefly. A document's `revised` is the whole document (`body_md` and `body_json` in the document's shape, every id kept); a screenplay's `revised.video` is the whole corrected video.json, every other scene, line and id kept exactly, the cast word for word, within lint's rules.
- Change only what the owner asked. Never change a document above the one discussed: suggest it in the reply, the owner takes it to that thread.
- When no usable answer is possible (the request contradicts an approved document or the cast, or needs something not in the payload), say why in the reply and leave `revised` null. The thread then waits for the owner; nothing is retried.

## Answer

Planner: `{"reply": <zh-TW>, "revised": null | {"body_md": <the whole document>, "body_json": <the whole structured document>}}`.

Writer: `{"reply": <zh-TW>, "revised": null | {"video": <the whole corrected video.json>}}`.

## What the worker does with it

A document's revision goes up with the reply: the site files it as a new version that waits for the owner and closes the one it replaces with the note 「討論後出了新版本」, which does not count against `series_doc_rewrites`. A screenplay's revision is written into `video.json` here, passed through lint (fixed by the writer up to three times, else put back as it was and the reply says so), and the video is checked, heard and sent to the script gate again on the following rounds. An answer that is not JSON, or has no reply, is answered for with a reply that says so.
