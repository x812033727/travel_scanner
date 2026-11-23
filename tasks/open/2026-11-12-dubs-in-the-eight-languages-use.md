---
id: 2026-11-12-dubs-in-the-eight-languages-use
title: Dubs in the eight languages use MiniMax voices; zh-TW narration stays Gemini
status: review
priority: P2
area: tools
owner: claude-opus-5.5-minimax-dubs
claimed_at: 2026-11-12T10:29:43Z
created_at: 2026-11-12T10:28:56Z
completed_at:
branch: claude/fervent-dijkstra-vqykpz
depends_on: []
scope:
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/minimax.test.mjs
  - docs/videos/DUBS.md
---

# Dubs in the eight languages use MiniMax voices; zh-TW narration stays Gemini

## Why

The owner listened to the 2026-11-12 trials and chose MiniMax for the eight foreign dub tracks
(en, ja, ko, es, pt, id, vi, th) while the zh-TW narration keeps its Gemini voice: the Mandarin
MiniMax voices have no Taiwan accent, but the foreign ones read correctly and close to Gemini's
length once `language_boost` followed the voice (#2084).

## Definition of done

- [x] `dub` reads every foreign locale in MiniMax voices when the site has a MiniMax key, and in
  Gemini otherwise or with `--provider gemini`.
- [x] Each distinct speaker keeps a voice of its own (narrator, slides cohost, dialogue explainer
  characters); a speaker past a locale's MiniMax list keeps its Gemini dub voice.
- [x] A dub record keeps `voice_provider`, and status and upload judge it by the voices it was
  made with; records from before stay current as Gemini's.
- [x] Docs (`docs/videos/DUBS.md` §聲音).
- [ ] Merged, deployed, and one real episode dubbed by the worker in MiniMax and listened to.

## Steps

- [x] `tools/video/dubs/plan.mjs`: `DUB_MINIMAX_VOICES`, `DUB_PROVIDERS`, voice order, provider
  through `dubScript`, `dubRequests`, `dubFingerprint`, `speechCurrent` (`recordProvider`).
- [x] `tools/video/dubs/cli.mjs`: `--provider`, `dubProvider` (status `minimax_configured`), the
  plan made after the status call, per-provider key and budget checks, `voice_provider` recorded.
- [x] Tests in `tools/video/dubs/minimax.test.mjs` (the bound dub tests are untouched).

## How to verify

```bash
node --test tools/video/dubs/*.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Trials on 原來如此 P14 (three host lines per language), measured by transcription and length
  against the Gemini dub, after #2084: en CalmWoman 104 %, expressive_narrator 112 %; ja CalmLady
  95 % (0 errors), KindLady 103 %; ko GentleWoman 108 %, CaringWoman 118 %; es SereneWoman 109 %,
  ThoughtfulLady 116 %; pt SereneWoman 100 %, LovelyLady 105 %; id ConfidentWoman 100 %,
  SweetGirl 97 %; vi kindhearted_girl 132 %, 110 % at +15 % with no error; th female_2 87 %,
  female_1 100 %. Korean sped up 40 % started misreading, so no rate is set there.
- MiniMax takes no style text and no pronunciation hints: `--style` only reaches Gemini voices,
  and `pronunciation_hints` (zh-TW readings) are dropped from MiniMax dub scripts.
- The eight tracks are now eight different people, not one host; the owner accepted that.
- Claimed with `--force` over stale claims on `tools/video/dubs` (latest 2026-11-04; the two
  branches still on origin, codex/story-lexicon-core-20261016 and codex/whisper-pyav-compat-20261026,
  last moved in October).
- Not done: the admin language panel shows no provider; the worker uses whatever `dub` picks.
