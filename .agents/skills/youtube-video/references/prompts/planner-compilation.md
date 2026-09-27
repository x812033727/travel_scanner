# Planner prompt: a COMPILATION's upload fields (合集的標題、說明、標籤、縮圖), and its translations

The worker runs this as the planner stage with variant `compilation` (`tools/video/automation/prompts.mjs`, `SERIES_INSTRUCTIONS["planner:compilation"]`) once every episode of a binge series is cleared for upload and the site handed it the compilation job (docs/videos/BINGE.md). Nothing is narrated or drawn again: the compilation is the episodes' finished cuts joined in order, a chapter card before each and an outro after the last, and this prompt writes only what YouTube shows. The worker (`tools/video/automation/compilation.mjs`, `planMetadata`) writes the answer into `docs/videos/<series>-full/video.json` (`youtube`, `thumbnail`), copies the chosen keyframe to the work directory as `keyframes/thumb-source.png` under the shot id `thumb`, and keeps the three title options in `metadata-plan.json`. An agent doing it by hand edits the same fields and copies the same file.

## Payload

`series` (as the site summarises it: slug, title, premise, genre, lead, visual_tier, total_minutes, planned_episodes), `genre_spec` (the genre preset, with its `title_formula` and `thumbnail_formula`), `series_reference`, `episodes` ([{slug, number, title, logline, recap}] in play order), `all_recaps`, `description_budget_bytes` (how many bytes the description body may take: YouTube allows 5,000, the tool appends one chapter line of about 150 bytes per episode and keeps 400 for its own lines, never less than 500), `thumbnail_headline_max` (12), `thumbnail_candidates` ([{episode, number, shot, judge, characters, prompt}]: keyframes of the first three episodes with a character in frame, best judged first, at most twelve); on a second attempt `previous_problem`.

## What to write

- `title`: at most 100 characters, no angle brackets, following the genre's `title_formula`: the setting in one clause, the awakening or return, one concrete satisfaction, the villain still dreaming (e.g. 重生回開服當天，她覺醒逆天天賦，背叛者還在做夢，她已磨好刀｜一口氣看完). Two alternatives in `titles`.
- `description`: zh-TW, within `description_budget_bytes` (with forty episodes that is 500 bytes, about 166 characters): the first two lines say what the story is and who it is for, then what happens without spoiling the end. The chapters, the article link and the sources are appended by the tool.
- `tags`: at most 500 characters in all, including 漫劇, AI漫劇, 一口氣看完 and the genre's.
- `thumbnail`: `{"headline": ≤ 12 characters of the biggest promise, "tag": ≤ 6 characters or null, "episode": n, "shot": id}`, naming one of `thumbnail_candidates` with a character's face and the highest judge score. The `thumb` template draws the headline and tag over that keyframe.

## Answer

`{"title", "titles": [two], "description", "tags": [...], "thumbnail": {"headline", "tag", "episode", "shot"}}`

The worker refuses a title over the limit or still the placeholder 「（合集標題待企劃）」, a headline over 12 characters or still 「（待企劃）」, tags over 500 characters, or a thumbnail that names no candidate, and asks once more with `previous_problem`; then the compilation waits for the next run. A description over the budget is cut, so write inside it.

## `translator:compilation`

The other four locales' fields, one locale a call (`SERIES_INSTRUCTIONS["translator:compilation"]`, `translateMetadata`). Payload: `locale` (en, ja, ko, zh-CN), `youtube` (the zh-TW title, description and tags), `chapters` (the episode titles keyed by episode slug), `series`. Answer `{"title": ≤ 100 characters, "description": no longer than the source, "tags": [...], "chapters": {<the same keys>: text}}`, every name spelled the same way throughout, en plain, ja です／ます, ko 합니다체, zh-CN mainland wording in Simplified characters. The worker writes `docs/videos/<series>-full/i18n/<locale>.json`; a locale missing a chapter title is refused. When the composed description would pass 5,000 bytes, the tool falls back to 「第 N 集」 (Episode N, 第N話, N화) for every chapter and warns.
