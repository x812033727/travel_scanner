# Verifier prompt: one AI drama episode, continuity and the story bible, never the writer

Fill the placeholders before dispatch: `<ROOT>`, `<VIDEO_WORKDIR>`, `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`, the video's folder in the repo), `<TODAY>`, `<ROUND>` (1 or 2). Round 2 goes to a different agent than round 1. Everything below the rule is the prompt.

---

You are the independent checker of ONE unverified zh-TW drama script. You did not write it. A picture model will draw every shot from its prompt and a speech engine will read every line, so what you are checking is whether the episode holds together: the same characters, the same names, a story that does not contradict itself or its source, and prompts a model can draw without inventing. For an adaptation you are also the fact-checker, with the tutorial verifier's rules.

REPO (read-only except the paths below; never run git): `<ROOT>`
DRAFT: `<VIDEO_DOCS>/` (`video.json`, `claims.md`, `brief.md`, and `verify-1.md` when you are round 2). You may edit `video.json` and `claims.md`, and write `verify-<ROUND>.md`; never `brief.md`, never anything else in the repo. Helper scripts go in `<VIDEO_WORKDIR>/<SLUG>/_tools/`.

## Method

1. Build the bible table from `brief.md` §角色 and `video.json` `characters[]`: id, name, appearance, voice. They must agree; the brief wins.
2. Walk every shot in order and write a continuity table to your helper folder: shot id, characters in `data.characters`, every name or character mentioned in `data.prompt`, setting, time of day, props. Flag: a character in the prompt but not in `characters` (the sheet will not be referenced and the face will drift); a character in `characters` the prompt never shows; a name spelled two ways; a prop, wound, garment or weather that appears without cause or vanishes; a setting that changes between consecutive shots without a cut being implied; more than 3 characters; text, logos, real people or brands in a prompt.
3. Walk every line: `speaker` must be a bible id or `narrator`; a character speaks only when in the shot (or is heard off-screen and the prompt says so); `emotion` fits the moment; names in the lines match the prompts and the dictionary; the story's cause and effect holds from the premise to the end; nothing the source contradicts (for a retelling: the passage in `claims.md`; for an adaptation: the article and official pages, opened today with `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`, at least 1 s apart per host, NO personal data of anyone anywhere).
4. Verdict per finding: FIX (apply it) / REPORT (a judgement call the owner or the writer makes). Fix spelling, ids, `characters` lists, a prompt's missing or contradictory detail, an emotion that fights the line. Do not rewrite style, order or pacing; do not add or remove shots or lines; keep every id.
5. Listener pass (report only): lines over 40 characters, verification narration, Latin terms not in the dictionary, two consecutive shots whose prompts are near duplicates (lint warns), shots over 10 seconds.
6. Re-run the checks after your edits: `node <ROOT>/tools/video/cli.mjs lint --slug <SLUG>` must show zero errors.
7. Write helper scripts as files and run them; do not paste non-ASCII text into shell heredocs.

## Output

Write `<VIDEO_DOCS>/verify-<ROUND>.md` with the bible table, the continuity table (shot ｜ characters ｜ names in prompt ｜ setting ｜ finding ｜ verdict ｜ before → after) and, for an adaptation, the claim table of the tutorial verifier; then a summary: findings fixed and reported, names unified, prompts changed, facts confirmed or changed, listener findings, the lint result, and whether a SECOND ROUND is required (rule: more than three continuity or fact changes → yes). Paste the summary (at most 40 lines) as your reply.

Round 2 (when told so): re-check every shot and line round 1 changed plus a random third of the rest; write `verify-2.md`.
