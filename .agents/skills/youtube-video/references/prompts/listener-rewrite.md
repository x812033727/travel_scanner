# Listener rewrite prompt: the lines Jev still hears wrong after the retakes

Fill the placeholders before dispatch: `<VIDEO_WORKDIR>`, `<SLUG>`, `<VIDEO_DOCS>`. Dispatch only after `tts --redo` has been tried the allowed number of times and `check-audio` still flags lines (`docs/videos/HANDS-OFF.md` §旁白). The worker sends the same rules as the listener stage's variant `rewrite` (`tools/video/automation/prompts.mjs`), with the flagged lines in the payload; on the recorded route the coordinator pastes them. The agent changes no file: the coordinator applies the answer, runs `lint`, then `tts --redo` with exactly those ids and `check-audio` again, at most two rounds, and the owner decides what is still flagged. A rewrite that changes a number, a Latin-script word or a term of the pronunciation dictionary is dropped (`tools/video/automation/rewrite.mjs`); the line keeps its text. Everything below the rule is the prompt.

---

You rewrite a few narration lines of ONE zh-TW (Traditional Chinese, Taiwan) Mokaair video for a synthesized Taiwanese-Mandarin voice. Each line below was retaken and Jev still heard it wrong: `text` is what the script says, `heard` is what the transcriber understood.

READ: `<VIDEO_DOCS>/video.json` (the script, for the line's neighbours), `<VIDEO_WORKDIR>/<SLUG>/review/check-flags.json` and `review/check.json` (the flagged ids and what was heard), `<VIDEO_DOCS>/../lexicon.json` (the dictionary's terms). Write nothing.

## Rules

- Rewrite ONLY these sentences' wording so the voice reads them unambiguously: swap the word that gets misheard for a plainer one with the same meaning (for example 「和」→「跟」, a sentence-final 「答」→「回答」, 「旗艦」→「旗艦模型」), split a run of same-sound characters, keep the sentence about as long.
- Keep every number, price, date and version exactly as written; keep every Latin-script word and every product or proper name spelled exactly the same, the dictionary's terms included; keep the meaning. Add no fact and no filler.
- Leave a line alone when `heard` already says the same thing in other characters.
- When `previous_problems` lists rewrites of yours the check refused last round, do not repeat them.
- Nobody's personal data anywhere.

## Output

ONE JSON object and nothing else (no Markdown fence): `{"lines": [{"id": "<line id>", "text": "<the rewritten line>"}]}`, with only the lines you changed, or `{"lines": []}` when none should change.
