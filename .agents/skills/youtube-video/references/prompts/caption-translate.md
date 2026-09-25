# Caption translator prompt: one video, one locale

Fill the placeholders before dispatch: `<ROOT>`, `<VIDEO_WORKDIR>`, `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`), `<LOCALE>` (en, ja, ko or zh-CN). Run `node <ROOT>/tools/video/cli.mjs i18n-sheet --slug <SLUG> --locale <LOCALE>` first; it writes the worksheet this prompt names. Everything below the rule is the prompt.

---

You are translating ONE zh-TW (Traditional Chinese, Taiwan) YouTube tutorial into `<LOCALE>`: its closed captions, chapter names, title, description and tags. Viewers read the captions while the narration plays, so write captions, not a transcript: natural in `<LOCALE>`, faithful in meaning, short enough to read at speaking pace.

REPO (read-only; never run git): `<ROOT>`
WRITE HERE ONLY: `<VIDEO_WORKDIR>/<SLUG>/i18n/<LOCALE>.todo.json`, the worksheet. Fill in `text` fields; never change `id`, `scene`, `source` or `todo`. Never edit `video.json` or anything in the repo, and never write a hash: `i18n-merge` computes them.

## Read first

1. `<VIDEO_DOCS>/video.json`: the slides (`data`) show what the viewer sees while a line plays; use them for context and keep the terms consistent with what is on screen.
2. The worksheet. Lines with `todo: true` need a translation; the others already have a current one, which you may improve only if it is wrong.
3. `<ROOT>/apps/api/app/guides/content/<SOURCE>.json` when `video.json` names a `source_guide`: its `<LOCALE>` version, if any, is the site's own wording for the same terms.

## Rules

- One entry is one spoken sentence. Translate its meaning, not its words; keep every number, price, date, version and product name exactly as in the source (product names in their official spelling for `<LOCALE>`).
- Length: about the time the sentence takes to say. English at most about 80 characters per line entry, Japanese and Korean at most about 40, Simplified Chinese about as long as the source. The tool splits long entries into caption cues; you do not.
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

## Report (at most 20 lines)

Lines translated, the title you chose, terms you kept in English or transliterated and why, lines you were unsure of (id and why).
