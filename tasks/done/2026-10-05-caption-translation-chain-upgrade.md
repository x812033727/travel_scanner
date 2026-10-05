---
id: 2026-10-05-caption-translation-chain-upgrade
title: Caption translation chain: split rules, a glossary, and translate then reflect then refine in one call
status: done
priority: P2
area: tools
owner: claude-fable-5-1-captions
claimed_at: 2026-10-05T16:59:49Z
created_at: 2026-10-05T16:08:23Z
completed_at: 2026-10-05T17:23:06Z
branch: claude/caption-translation-chain
depends_on: []
scope:
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
  - tools/video/core/lexicon.mjs
  - tools/video/core/lexicon.test.mjs
  - docs/videos/AUTOMATION.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/i18n/cli.mjs
  - tools/video/i18n/i18n.test.mjs
---

# Caption translation chain: split rules, a glossary, and translate then reflect then refine in one call

## Why

The caption translator (`prompts/caption-translate.md`, `automation/prompts.mjs`) translates
line by line with no glossary and no second look; the reviewer prompt catches some of what a
reflection pass would have fixed. Translate-then-reflect-then-refine with a terminology table
is the chain the strongest open translators use (VideoLingo, Apache-2.0; pyvideotrans, GPL,
idea only). Our en, ja, ko and zh-CN CC and metadata go through this prompt for every video.

## Definition of done

- [x] The translator answers `{draft, critique, final}` in one call; only `final` is used,
      and an answer without a critique is refused and retried.
- [x] The prompt carries a glossary built from the lexicon terms the video uses plus its
      `sources` names, and the zh-TW cue boundaries, so the translator sees where cues split.
      (`i18n-sheet` writes them into the worksheet and the worker sends them beside it; Notes.)
- [x] `splitText` prefers clause ends and never splits a number from its unit.
- [x] `prompts.test.mjs` pins the prompt sections; a fixture shows a glossary term kept the
      same across all four locales.

## Steps

- [x] Rewrite `caption-translate.md` (three passes, glossary table, cue boundaries) and
      `caption-review.md` (review against the glossary).
- [x] `automation/prompts.mjs`: build the glossary and the boundaries into the request, parse
      the three-part answer; `prompts.test.mjs`.
- [x] `core/captions.mjs splitText`: clause-end preference, number+unit tokens; `core/lexicon.mjs`
      exposes the terms a video used.
- [x] `docs/videos/AUTOMATION.md`: the translator stage.
- [ ] Receipt increment by an independent agent for `automation/prompts.mjs` (and
      `automation/automation.test.mjs`, see Notes).

## How to verify

```bash
node --test tools/video/automation/prompts.test.mjs tools/video/core/captions.test.mjs tools/video/core/lexicon.test.mjs
node tools/video/cli.mjs i18n-sheet --slug <video>     # the sheet carries the glossary and the boundaries
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `tools/video/automation/prompts.mjs` → receipt increment. `flow.mjs` is deliberately
  untouched: the three passes are one call.
- `prompts.mjs` is also named by `2026-10-03-illustrated-slides-round-2-a-family`; claim order
  decides who rebases.
- Technique from VideoLingo (Apache-2.0) and pyvideotrans (GPL — idea only); nothing copied.
- 2026-10-05, claude-fable-5-1-captions, branch `claude/caption-translation-chain`:
  - **Where the answer is read.** `flow.mjs` calls `parseAnswer(answer.text)` for every stage
    and reads `translated.worksheet.lines`, so the chain lives in `parseAnswer`: `finalAnswer()`
    returns `final` of a `{draft, critique, final}` answer (the `final` is `{"worksheet": …}`,
    the shape the stage always answered) and throws on a missing or blank critique, or a draft
    with no final object. The throw becomes `OUTPUT_INVALID` in `stage()` (the message reads
    "translator answered something that is not JSON: the answer skipped its critique…"),
    which `move()` turns into `retryLater` (kept answer, one more try, blocked the second time):
    the DoD's "refused and retried" without touching `flow.mjs`. A plain `{worksheet}` answer
    still passes through, since `parseAnswer` does not know the stage; the automation test's
    fake translators answer that shape and keep passing. A stage-aware refusal would need
    `flow.mjs`.
  - **Scope added `tools/video/automation/automation.test.mjs`** (nobody active on it, same as
    `2026-10-01-video-worker-translator-fills-the-thumbnail` did): it pins the zh-TW translator
    and caption reviewer prompts by SHA-256 ("change a hash only when you mean to change what
    every zh-TW video is told"), and this ticket means to. Only the two hashes and a dated
    comment line changed there; the shortening and rewording passes kept their bytes. It is
    receipt-bound too (`REVIEW_FILES`), so the increment covers `prompts.mjs` and it.
  - **How the glossary and the boundaries reach the translator** (scope extended on the
    coordinator's request to `tools/video/automation/flow.mjs`, `tools/video/i18n/cli.mjs` and
    `tools/video/i18n/i18n.test.mjs`, because the worker's payload is assembled in
    `translateLocale` and the worksheet in `buildSheet`, and `instructionsFor()` never sees the
    video, so `prompts.mjs` alone could not carry them). `translationContext(video, lexicon)`
    lives in `i18n/cli.mjs` (the CLI must not import the automation layer; `prompts.mjs`
    re-exports it) and returns `{glossary: {terms, sources}, boundaries}`: `entriesUsed` in
    `core/lexicon.mjs` lists every dictionary entry the texts use (null entries included, with
    the forms they appear in: "GPT" as "GPT-5.5"), `cuePieces` in `core/captions.mjs` the pieces
    a line is cut into. `i18n-sheet` builds it once per run (the narration's, the same for every
    locale) and `buildSheet(…, context)` writes `glossary` into every sheet and `boundaries` into
    one that holds lines, with a note saying what they are; the command's line says how many
    terms, sources and lines. `translateLocale` reads them off the sheet (`sheetContext`) and
    sends them at the top of every translator and caption reviewer request beside a worksheet
    stripped of them (`withoutContext`, so the glossary is not sent twice); a lines unit gets
    only its own lines' boundaries and the metadata unit none (`unitContext` in `flow.mjs`).
    `sheetUnits`/`assembleSheet` keep the keys, `mergeSheet` reads neither (a test shows the
    merge is byte-identical with or without them), and `channelLocale`'s `sheetDone` check
    builds its sheet without a context. A sheet from before this change (no `glossary` key)
    sends nothing extra, and the prompts read both as optional.
  - **`unitKey` still hashes the unit as written**, context included, so a kept unit is bound
    to the glossary it was translated with and a lexicon change mid-translation asks that unit
    again (rare, and the honest choice). Stripping the context from the key would also break
    `docs/videos/imported-long-languages/runner.test.mjs`, which asserts
    `kept[unitKey(f.fresh, null)]` against the sheet exactly as `i18n-sheet` writes it; that
    suite (out of scope) and `runner.mjs`'s strict wrapper, which reads `payload.worksheet`'s
    `slug` and `parts`, both pass as they are (44/44).
  - **Stage-aware refusal of the old `{worksheet}` shape: not done.** It would need
    `finalAnswer` to mark an unwrapped final (a Symbol property) and `translateLocale` to refuse
    an unmarked translator answer; the automation test's fake translators and the out-of-scope
    `runner.test.mjs` fakes answer `{worksheet}` directly and drive `translateLocale`, so the
    change is not cheap. A model that ignores the three-pass shape is therefore merged as before;
    `prompts.test.mjs` pins that the prompt demands the shape.
  - **Output size.** The answer now carries two worksheets (draft and final) plus the critique:
    about twice the output tokens and time of before. A unit is at most 24 lines / 2400 chars
    (`sheet-units.mjs`, 3.2 s a line measured on 2026-09-29 → about 80 s), so a doubled unit
    stays under the web route's 295 s; watch the first real run and lower `UNIT_LINES` if a unit
    comes close.
  - **`splitText`.** Three cut costs now: a sentence end (。！？.!? with closing quotes after)
    costs nothing, a clause end (，、；：,;:—) half the mid-clause cost, mid-clause the old
    `cap²/4`; the evenness term still dominates, so a sentence end wins only when the pieces
    stay about as even. A number keeps its unit in both tokenizers: the CJK regex has a
    number+unit alternative first (currency sign, digits, then %／×／a CJK measure word with or
    without a space, or a Latin unit word after a space; a Latin suffix with no space such as
    "24fps" was one token already), and word-based locales rejoin "300", " ", "GB". Every pinned
    cue and SRT byte in `captions.test.mjs`, `tts.test.mjs`, `renewal*.test.mjs`,
    `runner.test.mjs` and the fixtures stayed the same; a line with a number and a space before
    its unit at a former cut point will cut differently from now on, which `renewal-handoff`
    reports as captions to upload again for an old video.
  - Verified: `node --test tools/video/automation/*.test.mjs tools/video/i18n/*.test.mjs
    tools/video/core/captions.test.mjs tools/video/core/lexicon.test.mjs`,
    `node --test docs/videos/imported-long-languages/runner.test.mjs`, `npm run test:tools`
    (only `review.test.mjs` red, the receipt for `prompts.mjs`, `automation.test.mjs` and
    `flow.mjs`, which the independent increment re-binds), `npm run check:tasks`,
    `node tools/video/long-form/cli.mjs check` (stale on those three files, expected).
