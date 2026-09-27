# Writer prompt: one automated video, video.json and claims.md

Fill the placeholders before dispatch: `<ROOT>` (absolute path of the repo or worktree), `<VIDEO_WORKDIR>` (the video working directory, outside the repo), `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`, the video's folder in the repo), `<TODAY>` (YYYY-MM-DD). The launch message adds an IDENTITY block: the outline option the owner chose, the owner's own words for 站主觀點 if they changed it, the source article slug, and the channel voice. Commands are written for a POSIX shell; translate them for your shell if needed. Everything below the rule is the prompt.

---

You are writing ONE zh-TW (Traditional Chinese, Taiwan) YouTube tutorial for the Mokaair channel as `video.json`: every slide and every sentence of narration. A speech engine reads the narration aloud and the same text becomes the zh-TW captions, so you are writing for the ear. This is a DRAFT: a different agent re-checks every fact afterwards, so record your evidence.

REPO (read-only except the paths below; never run git): `<ROOT>`
WRITE HERE ONLY: `<VIDEO_DOCS>/video.json`, `<VIDEO_DOCS>/claims.md`, and new entries in the shared pronunciation dictionary `lexicon.json` in `<ROOT>/docs/videos/` (add terms; never change or remove an existing one). Helper scripts go in `<VIDEO_WORKDIR>/<SLUG>/_tools/`. Never edit `brief.md`: the owner's approval is bound to its hash.

## Read, in this order

1. `<VIDEO_DOCS>/brief.md` and the chosen outline in the launch message. The owner's version of 站主觀點 overrides the brief's; the brief overrides everything below except official sources.
2. `<ROOT>/.agents/skills/youtube-video/references/script-writing.md`, all of it, including the section for synthesized narration.
3. `<ROOT>/.agents/skills/youtube-video/references/automated.md` §video.json 的重點 and §發音與試聽.
4. The format: `<ROOT>/tools/video/core/schema.mjs` (fields and their limits), `TEMPLATE_SPECS` in `<ROOT>/tools/video/templates/templates.mjs` (what each template's `data` holds, how many items it can reveal), and the examples `<ROOT>/tools/video/core/fixtures/minimal/video.json` and `<ROOT>/tools/video/templates/fixtures/showcase/video.json` (shape only; do not copy text).
5. The channel spec `<ROOT>/docs/videos/README.md`: voice, intro and outro, description template.
6. The source article, if any: `<ROOT>/apps/api/app/guides/content/<SOURCE>.json`.

## Hard rules

- `video.json` FIRST as a skeleton that passes the schema (all scenes from the outline, one placeholder line each), then fill scene by scene and save after each; a cut-off session keeps files, not chat.
- Line ids: get fresh ones with `node <ROOT>/tools/video/cli.mjs ids --count 40 --slug <SLUG>`; never renumber when inserting a line.
- One `lines[]` entry is one spoken sentence, about 25 characters, at most 40. The opening scene states the viewer's question within its first sentence and what they will get within 30 seconds.
- `reveal` on the sentence that introduces a bullet, step or card, never ahead of it. A scene's reveal count equals the items it shows.
- Every Latin-letter term in `text` or `say` must be in the dictionary. Add a new term with its spoken form (`"RAG": "R A G"`) or with `null` if a Mandarin voice reads it correctly as written, and list every term you added in your report so the owner listens for them.
- `say` only where the spoken form must differ from the caption; lint's error message gives the `say_for` value.
- No parentheses, URLs, emoji or symbols the voice cannot read in `text`. Numbers as a listener hears them; exact figures go on the slide.
- Slides hold keywords, not sentences: a title of at most about 16 characters, bullet items of at most about 20. `**文字**` marks the accent colour; `\n` breaks a line by hand.
- Pace: no slide state should stay up much longer than about 15 seconds. Split a long explanation into several scenes, reveal one item per sentence, and show concrete things with `chat` (a question and its answer, a customer's message), `quote` (an official sentence, its translation, where it is from) and `stats` (two to four big numbers). If the video has a source article, put one `cta` scene near the middle, after the main example, with one sentence pointing to the article in the description's first line.
- Chapters: at least 3, the first scene has one, each at least 10 seconds. Chapter names are what a viewer would search for (a question or a noun), never 「第一部分」, and the first and last are named for their content too, not 「開場」 or 「結論」.
- `youtube.title` at most 100 characters, no angle brackets; `youtube.description` is the body only (two opening lines that say what the video answers and for whom, then the substance). The article link (first line), chapters, references and hashtags (from the first three `tags`) are added by the tool; do not write them. Put the most searched terms first in `tags`. `tags` total at most 500 characters. `video_id` stays null.
- `sources`: every official page a fact rests on, `{ title, url, checked_on: "<TODAY>" }`, the final URL after redirects.
- `assets`: only files under `<ROOT>/apps/web/public/` or `<ROOT>/docs/videos/`, each with its source and licence. No logos, no screenshots of other people's accounts.
- Fetching: `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`, at least 1 s between requests to one host, NO personal name, email or other personal data of anyone anywhere. Check the HTTP status; strip `<!-- -->` before reading. Web search at most 5 calls.
- Every price, limit, version and date is re-opened on the official page TODAY. Not found → say it without the number, or 「以官網為準」 on the slide; never a third-party number.
- Verification belongs in `claims.md`, never in the narration: no 「經查證」「根據官方文件」「截至查證」, no 「本影片」.
- Opinions are marked as the owner's (「我的看法是」「以我的用法」) and must follow 站主觀點; never invent a usage experience the owner did not have.
- Write helper scripts as files and run them; do not paste non-ASCII text into shell heredocs, Windows mangles it.

## claims.md

One line per checkable claim, numbered, and each scene lists the ids it uses in `claims`:

    c1｜主張（as narrated or shown）｜官方網址｜<TODAY>｜scene id

End the file with `## 與企劃不同的地方`, `## 我懷疑但沒動的事`, and `## 進度` (which scenes are done; keep it updated).

## Self-checks before reporting

    node <ROOT>/tools/video/cli.mjs lint --slug <SLUG>
    node <ROOT>/tools/video/cli.mjs status --slug <SLUG>

Lint must show zero errors. Read every warning and fix it or say in the report why it stays. The estimated length must sit inside the target.

## Report (at most 40 lines, pasted back)

status; estimated minutes and narration characters; scenes and chapters with their estimated start times; the worked example and where it sits; dictionary terms you added and how you expect them to be read; lint warnings that remain and why; claims written without a number and why; differences from the chosen outline; things you suspected but did not change.
