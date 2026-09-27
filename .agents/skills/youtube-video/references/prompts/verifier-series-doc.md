# Verifier prompt: the VERDICT on a planned series document (設定集、總綱、篇章細綱)

The worker runs this as the verifier stage with variant `series-doc` (`tools/video/automation/prompts.mjs`, `SERIES_INSTRUCTIONS["verifier:series-doc"]`), in a fresh session, right after the planner wrote a document of a hands-off series (`series.hands_off`, docs/videos/BINGE.md). The verdict travels with the document to `POST /api/v1/video/automation/series/<slug>/docs` as `judge`, and the site decides on arrival: approved, sent back for a rewrite, or, once the rewrites are spent, left for the owner with the problems on the card. An agent doing it by hand fills the same payload and files the same `judge`. The rules the site applies are `series_doc_passed` in `apps/api/app/video_automation/judge.py`; the worker mirrors them in `tools/video/automation/series.mjs` (`verdictPasses`).

## Payload

`kind` (`setting | outline | chapter`), `series` (slug, title, premise, aspects, tone, style_preset, genre, lead, visual_tier, compilation, hands_off, planned_episodes, episodes_per_chapter, chapters, open_ended, note), `genre_spec` (the genre preset: premise seed, conflict engine, satisfaction types, tropes, title and thumbnail formulas, what it never does, whether the retention rules apply), `series_reference` (this route's reference), `document` (`{body_md, body_json}` the planner just wrote), `setting` and `outline` (the approved documents before it, when any), `chapter_number` (for a chapter); on a second attempt `previous_problem` (why the last verdict could not be filed, e.g. a missing key).

## What to judge

You did not write the document, and nobody else will read it before the site acts on your word. Judge in the vocabulary 有 (delivered), 弱 (there but flat, generic or late) or 無 (missing), exactly these keys:

| kind | verdicts |
| --- | --- |
| `setting` | `originality` (no name, sect, system, place, artefact or plot a reader would recognise from an existing work), `conflict_engine` (the world makes trouble by itself; every faction wants and hides something), `genre_fit` (it delivers what this genre's audience came for, and the premise seed when the premise was blank), `cast_playable` (each character has a want, a fear, a secret, a speech habit and an English appearance an image model draws the same way every time) |
| `outline` | `originality`, `escalation` (stakes rise chapter by chapter), `midpoint_reveal` (one reveal around the middle turns the world on its head), `chapter_turns` (every chapter ends on a turn that changes the situation), `satisfaction_schedule` (satisfaction beats spread over the run; no chapter is dry) |
| `chapter` | `originality`, `tension_rules` (hook, turn and cliffhanger per episode, cliffhanger types vary between neighbours, tension curves not flat and ending high), `hooks` (each hook is a line or a picture, not a mood), `satisfaction` (at least two per episode, the first in the first half, of the genre's types), `alternation` (satisfaction and trouble alternate; the lead never only suffers two episodes in a row), `escalation` (the chapter ends higher than it began) |

## Answer

`{"verdicts": {<key>: "有"|"弱"|"無"}, "similar_works": [text, empty when none], "problems": [zh-TW sentences the planner can act on, one for every 弱 or 無, empty when everything is 有], "notes": one zh-TW line}`

The site approves when every required key is there, none is 無, at most one is 弱 (`MAX_WEAK_VERDICTS = 1`), and both lists are empty; anything else sends the document back with your `problems` as the note (prefixed 「[auto]」), so write problems the planner can fix in one rewrite. A verdict missing a key, or with a value outside the three words, cannot be filed; the worker asks once more with `previous_problem`, then files the document without a verdict and it waits for the owner.
