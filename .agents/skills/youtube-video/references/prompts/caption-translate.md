# Caption translator prompt: one video, one locale

Fill the placeholders before dispatch: `<ROOT>`, `<VIDEO_WORKDIR>`, `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`), `<LOCALE>` (en, ja, ko or zh-CN). Run `node <ROOT>/tools/video/cli.mjs i18n-sheet --slug <SLUG> --locale <LOCALE> [--parts metadata,captions]` first; it writes the worksheet this prompt names. Everything below the rule is the prompt.

**Which parts, and the dub budget** (`docs/videos/LANGUAGES.md`, `docs/videos/DUBS.md`). A language is made of three parts the owner ticks per video on `/admin/videos` after the final cut: the title, description, tags and chapter names (`metadata`), the captions (`captions`), and a dub track (`dub`, which reads the captions' translation aloud). `--parts` narrows the sheet to what was ticked: `--parts metadata` writes a sheet with no lines, `--parts captions` one with no title, description, tags or chapters (those fields are `null`); `i18n-merge` leaves a part the sheet does not hold exactly as it was. The sheet says which parts it holds in `parts`. When the owner also ticked a dub, and the narration is timed, every line carries `max_chars`: the same voice reads the translation in the time the zh-TW line takes, so a translation over its budget has to be shortened later; stay under it from the start. The worker (`tools/video/automation`) dispatches the same prompt with `parts` and the worksheet in the payload; a hand run passes the flags.

---

You are translating ONE zh-TW (Traditional Chinese, Taiwan) YouTube tutorial into `<LOCALE>`: its closed captions, chapter names, title, description and tags. Viewers read the captions while the narration plays, so write captions, not a transcript: natural in `<LOCALE>`, faithful in meaning, short enough to read at speaking pace.

REPO (read-only; never run git): `<ROOT>`
WRITE HERE ONLY: `<VIDEO_WORKDIR>/<SLUG>/i18n/<LOCALE>.todo.json`, the worksheet. Fill in `text` fields; never change `id`, `scene`, `source` or `todo`. Never edit `video.json` or anything in the repo, and never write a hash: `i18n-merge` computes them.

## Read first

1. `<VIDEO_DOCS>/video.json`: the slides (`data`) show what the viewer sees while a line plays; use them for context and keep the terms consistent with what is on screen.
2. The worksheet. Every entry with `todo: true` needs a translation: lines, chapters, the title, the description and the tags. Its `text` is empty because it is missing, or because its zh-TW source changed since the last merge (a renamed chapter, a new paragraph, reordered tags). The others already have a current one, which you may improve only if it is wrong.
3. `<ROOT>/apps/api/app/guides/content/<SOURCE>.json` when `video.json` names a `source_guide`: its `<LOCALE>` version, if any, is the site's own wording for the same terms.

## Rules

- One entry is one spoken sentence. Translate its meaning, not its words; keep every number, price, date, version and product name exactly as in the source (product names in their official spelling for `<LOCALE>`).
- Length: about the time the sentence takes to say. English at most about 80 characters per line entry, Japanese and Korean at most about 40, Simplified Chinese about as long as the source. The tool splits long entries into caption cues; you do not.
- `max_chars` on a line (present when the owner chose a dub for this locale) is a hard budget: the dub must fit the zh-TW line's slot even sped up 1.15×. Stay under it; cut the words around numbers and names, never the numbers and names.
- Fill only the parts the sheet holds (`parts`): a sheet without lines wants the title, description, tags and chapter names alone; one without those wants the lines alone.
- Register: en plain and direct; ja です／ます; ko 합니다체; zh-CN mainland wording and Simplified characters (视频, 软件, 默认), never a character-by-character conversion.
- Do not add explanations, greetings or anything the narration does not say; do not drop a clause.
- Opinions stay the owner's first person ("I", 「私は」, "저는", 「我」).
- Chapter names: what a viewer searching in `<LOCALE>` would type, at most about 30 characters.
- `title`: at most 100 characters, no angle brackets, searchable in `<LOCALE>`; not a word-for-word copy if a natural title reads better.
- `description`: the body only, same structure as the source; the tool appends chapters, the article link and the references. No angle brackets.
- `tags`: the product names plus the terms `<LOCALE>` viewers search for; the whole list at most 500 characters.
- Write helper scripts as files and run them; do not paste non-ASCII text into shell heredocs, Windows mangles it.

## Check before reporting

    node <ROOT>/tools/video/cli.mjs i18n-merge --slug <SLUG> --locale <LOCALE>

It writes `<VIDEO_DOCS>/i18n/<LOCALE>.json` and lists anything not translated or not mergeable; fix the worksheet until it lists nothing.

## Report (the coordinator scans it, one line per item)

Lines translated, the title you chose, terms you kept in English or transliterated and why, lines you were unsure of (id and why).

## Shortening pass (the worker's `translator:shorten`)

When `dub --locale <LOCALE>` ends with exit code 1, a slide window's lines do not fit even at 1.15× and `<VIDEO_WORKDIR>/<SLUG>/dubs/<LOCALE>/fit.json` lists them under `over`: for each line its `id`, `chars` (the translation's length now), `max_chars` (the most it may keep), `seconds` (how long the voice took) and `window_over_seconds`. Only those lines change. Cut words, not meaning: every number, price, date, version, product and proper name, and what the sentence claims, stay exactly; drop a hedge, a repeated subject, a connective, a filler; keep the register. Numbers and currency codes read slowly for their length, so cut the words around them. The captions show the shortened line too, so it must still read as a caption. Put the new text into a captions-only sheet (`i18n-sheet --slug <SLUG> --locale <LOCALE> --parts captions`, then edit those lines' `text`), run `i18n-merge`, then `dub --locale <LOCALE>` again; only the changed lines are synthesized again. The worker does this at most two rounds (`MAX_DUB_SHORTEN_ROUNDS` in `tools/video/automation/flow.mjs`) and then gives the locale's dub up with the reason, which the language card shows; a shortened line that is not shorter, or changes a digit, is dropped. Its payload is `{"locale", "lines": [{id, source, text, chars, max_chars, seconds, window_over_seconds}], "video"}` and it expects `{"lines": [{"id", "text"}]}`.

## Rewording pass (the worker's `translator:reword`)

When `check-audio --locale <LOCALE>` still flags lines after the two retakes, the voice usually said them right and the transcriber heard a homophone or near-homophone every time (for example ja 定価 heard as 低下, en "bill" as "build" and "Two: developers" as "to developers", ko 두 표를 as 투표를). No retake changes that; the words must. For each flagged line in `review/check-flags.<LOCALE>.json`, read what was heard in `review/check.<LOCALE>.json` (`lines.<id>.heard`) and change only the misheard words to ones no listener could take for what was heard: a synonym, a longer form, a particle, an explicit ordinal such as "Second,". Every number, price, date, version, product and proper name, and the claim, stay exactly; keep the register; stay within the line's `max_chars` from a captions sheet (or its current length when the sheet has none). Put the text in through a captions-only sheet and `i18n-merge` as above, then `dub --locale <LOCALE>` and `check-audio --locale <LOCALE>` again. The worker does this at most two rounds (`MAX_DUB_REWORD_ROUNDS`) before giving the locale up; a reworded line that is unchanged, over its budget or changes a digit is dropped. Its payload is `{"locale", "lines": [{id, source, text, heard, max_chars}], "video"}` and it expects `{"lines": [{"id", "text"}]}`.
