---
id: 2026-11-04-narration-lint-warns-known-mishearings
title: Narration lint warns on words the transcriber is known to mishear, before any TTS is paid for
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-tts-retakes
claimed_at: 2026-11-04T16:50:58Z
created_at: 2026-11-04T16:48:18Z
completed_at:
branch: claude/tender-einstein-ss8r5w
depends_on: []
scope:
  - tools/video/core/mishearings.mjs
  - tools/video/core/mishearings.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/automation/register.mjs
  - tools/video/templates/fixtures/paper/video.json
  - tools/video/templates/terminal/fixtures/claude-code/video.json
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

- [x] `node tools/video/cli.mjs lint --slug <slug>` on a zh-TW script that contains a phrase
      from the table prints a **warning** (never an error) on that line, naming the phrase, what
      the transcriber writes for it and the wording to use instead.
- [x] The phrases live in one module (`tools/video/core/mishearings.mjs`); the table in
      `script-writing.md` is kept in step with it by a test, so adding a row in one place and
      not the other fails `npm run test:tools`.
- [x] A phrase that is part of its own fix or of an unrelated word does not warn
      (沒有量到 for 沒有量, 日本機場 for 本機).
- [x] English narration (`narration_locale: "en"`) and dub translations are not checked.

## Steps

- [x] `core/mishearings.mjs`: the existing `MISHEARD_WORDS` moved here from
      `automation/register.mjs` (which imports and re-exports it), plus `UNLESS`, `phrasesOf`
      and `mishearingsIn(text)`.
- [x] `core/lint.mjs`: one `warn(label, …)` per hit in the per-line loop, zh only.
- [x] `mishearings.test.mjs`: hits, the exceptions, and the table-vs-module parity.
- [x] `script-writing.md`: say the table is enforced as a lint warning and where to add rows.

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
- 2026-11-04 (claude-opus-5.5-tts-retakes, claimed with `--force` on the owner's go-ahead):
  done on branch `claude/tender-einstein-ss8r5w`.
  - The list already existed: `MISHEARD_WORDS` in `automation/register.mjs`, sent to the slides
    writer and listener in `HEARD_RULES` and checked against the guide's table by
    `prompts.test.mjs`. lint cannot import register.mjs (register imports lint), so the list
    moved to `core/mishearings.mjs`; `HEARD_RULES`' text is byte-for-byte the same, so the
    hash-pinned prompts do not change and no host stage reruns.
  - `mishearings.test.mjs` asserts every row's own fix never warns; that found three more
    exceptions beyond the obvious ones (含糊的那一份, 尺取十一, 延後的到底是什麼).
  - Lint reads `spokenText` (the `say` form when there is one), zh narration only.
  - Two template fixtures said 「印出」 and their tests require zero warnings; their text now
    says 「顯示」 (paper `pl14`, claude-code `tc04`, `tc08`).
  - `lint.mjs` is bound by the long-form duration receipt; it is rebound by an independent
    reviewer agent (`.agents/skills/dev-and-ci/references/duration-receipt.md`).
  - `npm run test:tools`: the only failures left are the 15 that also fail on `origin/main`
    in this container (the native-log exit classifier tests 124–142).
- 2026-11-04 feasibility check on all 203 zh `docs/videos/*/video.json` (21,336 lines): 151
  warnings in 50 videos at first, mostly true positives in tutorials (印出, 放行, 讀檔, 本機).
  False positives fixed with `UNLESS`: 行程 as an itinerary (排行程, 這份行程, 天的行程) and
  inside 執行程式, 四項 inside 二十四項 and 第四項, 讀檔 inside 讀檔案; 137 left.
- **The host worker never sees these warnings**: flow.mjs `lintWarnings` passes only
  `kind: "narrative"` warnings to the writer, and only alongside a rewrite errors already asked
  for. So this helps an agent or person who runs `lint` by hand; the host's slides writer keeps
  getting the same list through `HEARD_RULES`. Giving the warning `kind: "narrative"` would put
  it in front of the worker's writer, but only on drafts that already fail lint; left as is.
