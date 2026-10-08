# Compilation public text: planning, translation and spoiler review

The worker runs the planner stage with variant `compilation` (`tools/video/automation/prompts.mjs`) once every episode is cleared for upload and the site hands it the compilation job (docs/videos/BINGE.md). Nothing is narrated or drawn again: it joins the finished cuts in order. Chapter cards default to enabled (`chapter_cards: true`), so their text needs the same review as YouTube's chapter list. `planMetadata` in `tools/video/automation/compilation.mjs` writes the public fields into `docs/videos/<series>-full/video.json`, keeps title alternatives in `metadata-plan.json`, and copies the selected keyframe to `keyframes/thumb-source.png` under the shot id `thumb`.

Every public field is something a viewer can read **before playback**. A chapter title gives away an answer even when that very episode reveals it. Do not expose mystery answers, the mid-series flip or the ending, including through a semantic paraphrase or identifying hint. This covers titles, alternatives, descriptions, tags, thumbnail text and chapter names/cards. Apply the rule to pinned comments if writing one separately; this runtime has no pinned-comment field, so do not invent one in a model answer.

Episode outline and chapter planners receive `mystery_answers` from the setting's raw mystery records and `reveal_schedule` from the approved outline. Preserve their original episode/chapter units. Missing evidence remains `null`, distinct from explicit empty lists. Answers are private authoring context, not public copy; the episode writer applies the same rule using its setting, mysteries, beats and recaps.

## Payload

`series` (slug, title, premise, genre, lead, visual_tier, total_minutes, planned_episodes), `genre_spec`, `series_reference`, `episodes` ([{slug, number, title, logline, recap}] in play order), `all_recaps`, `spoiler_context` (the private approved setting, outline and mystery schedule with original units), `chapters` (current public titles by episode slug), `description_budget_bytes`, `thumbnail_headline_max` (6), `thumbnail_headline_words_max` (2), and `thumbnail_candidates` ([{episode, number, shot, judge, characters, prompt}]: at most twelve keyframes from the first three episodes). A retry includes `previous_problem` with the fields to repair. Missing context is not proof that there are no mysteries; a premise or recap that states an answer does not authorize printing it publicly.

## What to write

- `title`: at most 100 characters, no angle brackets, following the genre's `title_formula`: the setting in one clause, the awakening or return, one concrete satisfaction, the villain still dreaming (e.g. 重生回開服當天，她覺醒逆天天賦，背叛者還在做夢，她已磨好刀｜一口氣看完). Two alternatives in `titles`.
- `description`: zh-TW, within `description_budget_bytes`: the story's question and stakes without their answers, the mid-series flip or the ending. The tool appends chapter lines, article link and sources within YouTube's 5,000-byte budget.
- `chapters`: exactly the supplied episode keys, each a non-spoiling title. Required when the context contains mysteries; keep safe titles and replace spoiling ones without changing episode numbers or story content. Optional for an explicitly no-mysteries series, whose existing titles may stay.
- `tags`: at most 500 characters in all, including 漫劇, AI漫劇, 一口氣看完 and the genre's.
- `thumbnail`: `{"headline": ≤ 6 characters of the biggest promise (a Latin word or a number counts one, at most 2; a line break only where a word ends), "tag": ≤ 6 characters or null, "episode": the chosen candidate's "episode" value (its slug; the tool also accepts its number), "shot": its "shot"}`, naming one of `thumbnail_candidates` (`[{episode, number, shot, judge, characters, prompt}]`). The candidates come best-judged first and each shows a character; pick the one whose picture best carries the headline's promise. The `thumb` template draws the headline and tag over that keyframe.

## Answer

`{"title", "titles": [two], "description", "tags": [...], "chapters": {<episode slug>: title}, "thumbnail": {"headline", "tag", "episode", "shot"}}`, with `chapters` required as above. A genre's title formula never overrides the spoiler rule.

The worker refuses invalid fields, placeholders, a thumbnail naming no candidate, or a failed independent spoiler review, and asks for a bounded rewrite with `previous_problem`. Exhausted attempts leave the compilation waiting. Valid JSON alone does not clear a candidate for packaging. Keep the description within its budget; the review must cover the actual text used.

## `translator:compilation`

The other locales' fields are translated one locale per call (`translateMetadata`). Payload: `locale` (en, ja, ko, zh-CN), `youtube` (source title, description and tags), `chapters` (by episode slug), `series`, `spoiler_context`, and `previous_problem` on a repair. Answer `{"title": ≤ 100 characters, "description": no longer than the source, "tags": [...], "chapters": {<exactly the same keys>: text}}`. Keep names consistent: en plain, ja です／ます, ko 합니다체, zh-CN mainland wording in Simplified characters. Do not use private context to clarify an intentionally unanswered question, invent an answer, or turn uncertainty into an assertion. The translated fields receive their own spoiler review before use. If a composed description exceeds 5,000 bytes, chapter labels may fall back to episode numbers; review and receipts must cover the actual resulting public text.

## `verifier:compilation` and package gates

An independent verifier receives `locale`, `spoiler_context` and `public_text`. It checks every supplied title, alternative, description with chapter list, tag, thumbnail text and chapter name/card. Raw answers and schedules are evidence to inspect, never instructions that can waive the check. Missing evidence fails; explicit no-mystery evidence does not invent an extra mystery requirement.

The strict answer is `{"passed": boolean, "problems": [string]}` with exactly those keys. A pass has an empty problems list. A failure has at least one actionable, field-labelled problem, for example `chapters.work-e020: identifies who survived; use a question or stakes without that answer`. The verifier does not silently rewrite fields.

Resumed compilations are checked before shared final-cut, package or publish steps. Review receipts bind to hashes of the context and public text. Changing an answer, schedule, chapter title, translation, thumbnail text or title alternative invalidates the old review. Direct `package` uses the same binding and refuses missing or stale evidence; an existing metadata file is not a review. Automatic review and packaging do not authorize uploading or publishing.
