# Verifier prompt: the fact check of ONE CHAPTER of a brand story

Verifier stage, variant `story` (`STORY_INSTRUCTIONS["verifier:story"]` in `tools/video/automation/story-prompts.mjs`; this is the readable copy). A fresh session per chapter: it did not write the chapter and has not seen an earlier check. The rules of the route are in `references/story.md`, section 查核怎麼做; the reasons in `docs/videos/STORY.md` §查核與來源規則. The common rules are the writer's (`writer-story.md`).

## What it gets

`chapter` (`key`, `number`, `title`, the plan's `point`), `plan` (`question`, `takeaway`, all six chapters), `scenes` (the chapter's lines only, by scene and line id; no picture prompts), `claims` (the chapter's rows of the claims table as the writer left them: `id`, `claim`, `scene`, `source`, `fact`), `facts` (the plan's `must_verify` with `core`, `attributed`, `reviewer_only`), `caveats`, `sources`, `round`, `today`.

`sources` are the pages the rows name and the pages of the facts the chapter tells, never the pages of a `reviewer_only` fact: a readable page comes as `passages` cut around the chapter's figures, years (with their 昭和, 平成, 令和 and 民國 forms) and names from the page's whole text, so a sentence past the reader's first 40,000 characters is there; a page the worker cannot read (a PDF, over 3 MB) comes as `read: "plan"` with the plan's `supports` line, which is what the plan's reviewer read in it, not what was read now.

## The work

1. The plan's facts are established (a second reader checked each against its sources before the import): every fact the chapter tells matches the plan's wording, figures, years and names. A `reviewer_only` fact is held to the plan's wording and not looked for in the pages (verdict `PLAN`).
2. Everything the writer added (a figure, a year, a name, a quotation not in `facts`) is in a passage. Look through every passage first; convert 昭和／平成／令和／民國 years and billion／億 before saying a figure is not there. A `read: "plan"` source confirms only what its `supports` line says.
3. `caveats` are orders: a line that mentions what they forbid is dropped or rewritten.
4. An `attributed` fact, and any anecdote on one non-official source, is told as somebody's account; a line that tells it as settled fact is rewritten.
5. Negative events as a ruling or an official document tells them; a negative claim about a living person needs two sources.
6. No trace of the check in the narration.

Verdicts: `CONFIRMED`, `PLAN`, `CHANGED`, `ATTRIBUTED`, `NOT FOUND` (taken out of the line). Change only facts and what depends on them; keep every line id; no new lines or scenes; no rewriting of style or pace.

## Answer

`{"patch": {"<line id>": "<the corrected line>"}, "drop": ["<line id>"], "claims": [{"id", "claim", "scene", "source", "fact", "verdict", "note"}], "report": "<zh-TW Markdown>"}`: a patch and the chapter's rows, never the whole script. The worker applies the patch to the chapter's lines, keeps the rows (a new row gets the chapter's next id), counts CHANGED, ATTRIBUTED and NOT FOUND, and has the chapter checked again by a fresh session when that is more than 3 (up to the drama's check rounds). When all six are checked it writes `verify-1.md`: each chapter's table, as the QA's `facts` item reads it; a claim marked NOT FOUND is cited by no scene.
