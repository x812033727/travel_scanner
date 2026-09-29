# Listener register prompt: an existing video's narration retold in the storytelling register

Fill the placeholders before dispatch: `<VIDEO_WORKDIR>`, `<SLUG>`, `<VIDEO_DOCS>`. Use it for a video written before the storytelling register (`docs/videos/ILLUSTRATED.md` §說書式旁白, `script-writing.md` §說書式旁白) whose narration should sound told rather than read out, without a new script: the outline approval on `brief.md` holds, the line ids stay so the translations still match, only the wording, the rhythm and the pause beats change. On the worker's route `node tools/video/cli.mjs restyle --slug <SLUG>` sends the same rules as the listener stage's variant `register` (`tools/video/automation/prompts.mjs` `LISTENER_REGISTER`) with every line in the payload, applies the answer line by line through the check in `tools/video/automation/rewrite.mjs` (a line that changes a number, a Latin-script word or a dictionary term is refused and keeps its text), runs `lint` (a script it refuses goes back as it was), writes `review/restyle.json`, and marks the video for another fact-check, a new recording and a new audio review; `restyle --slug <SLUG> --dry-run` only measures the script (turns, chapters closing on a question, pause beats). On the recorded route the coordinator pastes the lines and applies the answer the same way. Everything below the rule is the prompt.

---

You retell the narration of ONE finished zh-TW (Traditional Chinese, Taiwan) Mokaair video in the storytelling register, for a synthesized Taiwanese-Mandarin voice. The video was written as a tutorial and sounds read out; make it sound told.

READ: `<VIDEO_DOCS>/video.json` (the script; every narration line, its scene and its chapter), `<VIDEO_DOCS>/../lexicon.json` (the dictionary's terms). Write nothing.

## The register

- The first sentence is a counter-intuitive claim or the viewer's own question; the hook has landed within 20 seconds. No greeting, no 「今天要來跟大家分享」, no table of contents.
- The first chapter turns at least once on 「你以為…其實…」: what the viewer believes, then what is so, with the fact that shows it. Later chapters may turn the same way when they have a real reversal; never fake one.
- Every chapter's LAST sentence is the question the next chapter answers; the last chapter's last sentence answers the opening question instead. Never 「接下來我們來看」.
- Every chapter has at least one concrete scene or comparison a viewer can picture.
- Sentences alternate long and short; a reveal is a short sentence. Numbers arrive one at a time, each with what it means in the viewer's day.
- Beats as `pause_after_ms`: 900 after the cold open's first sentence, 600 on the sentence before 「其實」, 1200 on a chapter's closing question. Nowhere else, never over 5000.
- Facts stay facts: wording, order and rhythm change, never a number, a name, a version or who said what.

## What you may and may not do

- May: reword any line, reorder the words inside it, shorten or lengthen it (about 25 characters, at most 40), set `pause_after_ms` on the beats above, turn a chapter's last line into the next chapter's question, open the first chapter on 「你以為…其實…」 when the facts give a turn.
- May not: add, drop, merge, split or move a line; change a line's id or scene; change any number, price, date, version, Latin-script word, product or proper name (the check refuses the line); add a fact, an opinion or an owner's experience the script does not have; touch the cards, the shots or the thumbnail. The dictionary's terms appear exactly as written.
- When `previous_problems` lists lines the check refused last round, do not repeat them. Nobody's personal data anywhere.

## Output

ONE JSON object and nothing else (no Markdown fence): `{"lines": [{"id": "<line id>", "text": "<the retold line>", "pause_after_ms"?: <integer>}]}`, with only the lines you changed, or `{"lines": []}` when the script already tells its story.
