---
id: 2026-11-04-narration-lint-warns-known-mishearings
title: Narration lint warns on words the transcriber is known to mishear, before any TTS is paid for
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-04T16:48:18Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/mishearings.mjs
  - tools/video/core/mishearings.test.mjs
  - tools/video/core/lint.mjs
  - .agents/skills/youtube-video/references/script-writing.md
---

# Narration lint warns on words the transcriber is known to mishear, before any TTS is paid for

## Why

Most lines `check-audio` flags are not misread by the voice: Gemini's transcriber writes a
commoner word that sounds alike (實跑→食譜, 本機→本期, 背景→北京), and a retake of the same text
is heard the same way again (`.agents/skills/youtube-video/references/script-writing.md`
§給 TTS 唸的稿子). Each flagged line costs a retake round, Jev calls from the shared daily
quota, a listener rewrite and, when it still fails, the owner's manual audio approval.

The fix is already known for 36 phrases: the table in `script-writing.md` (two tutorials on
2026-10-09, 302 lines, 13 and 19 flagged on the first round). But it is prose for the writer
agent only; nothing checks a draft against it, so the same words come back and are paid for
again. The owner asked (2026-11-04) to keep the Gemini Flash TTS voice and cut the retakes
instead.

## Definition of done

- [ ] `node tools/video/cli.mjs lint --slug <slug>` on a zh-TW script that contains a phrase
      from the table prints a **warning** (never an error) on that line, naming the phrase, what
      the transcriber writes for it and the wording to use instead.
- [ ] The phrases live in one module (`tools/video/core/mishearings.mjs`); the table in
      `script-writing.md` is kept in step with it by a test, so adding a row in one place and
      not the other fails `npm run test:tools`.
- [ ] A phrase that is part of its own fix or of an unrelated word does not warn
      (沒有量到 for 沒有量, 日本機場 for 本機).
- [ ] English narration (`narration_locale: "en"`) and dub translations are not checked.

## Steps

- [ ] `core/mishearings.mjs`: `MISHEARINGS = [{ said, heard: [...], instead, unless? }]`
      and `mishearingsIn(text)`.
- [ ] `core/lint.mjs`: one `warn(label, …)` per hit in the per-line loop, zh only.
- [ ] `mishearings.test.mjs`: hits, the exceptions, and the table-vs-module parity.
- [ ] `script-writing.md`: say the table is enforced as a lint warning and where to add rows.

## How to verify

```bash
node --test tools/video/core/mishearings.test.mjs tools/video/core/lint.test.mjs
npm run test:tools
```

## Notes

- Filed from the 2026-11-04 cost conversation (Colab → Flash-Lite → "keep the voice, cut the
  retakes"). Sister task: `2026-11-04-worker-rewords-near-homophone-flags-first`.
- Warnings, not errors: some rows are ordinary words (界線, 放行) that read fine in another
  sentence, and the worker's `lintErrors` must not start blocking existing videos.
- Claim was refused on 2026-11-04 because `tools/video/core/lint.mjs` and `script-writing.md`
  are in the scope of five in-progress tasks; every one of those claims is older than 24 hours
  (stale). Taking it needs `claim --force`, which the session's permission mode did not allow
  without the owner's go-ahead.
