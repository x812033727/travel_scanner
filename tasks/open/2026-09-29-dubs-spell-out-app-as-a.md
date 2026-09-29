---
id: 2026-09-29-dubs-spell-out-app-as-a
title: Dubs spell out App as A P P: drop letter-spelling aliases of mixed-case words outside Chinese
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-29T03:28:43Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/plan.test.mjs
---

# Dubs spell out App as A P P: drop letter-spelling aliases of mixed-case words outside Chinese

## Why

`docs/videos/lexicon.json` has `"App": "A P P"`, because the zh-TW voice reads the word as
letters, which is how Taiwan says it. Both main's #891 (with `null`) and the RTX Spark video
(with `"A P P"`) added the entry. The merge of main into claude/ai-video-planning-l43qas on
2026-09-29 kept `"A P P"`, since the Sora video's approved narration was recorded with it.

`dubLexicon` in `tools/video/dubs/plan.mjs` drops only aliases that contain CJK characters.
`"A P P"` has none, so an en, ja or ko dub line that says `App` would be read letter by letter:
"App Store" would become "A P P Store". Term matching is case-sensitive, and no translation
in docs/videos has a capitalised `App` today, so nothing recorded is wrong yet. English copy
that starts a sentence with "App", or names the App Store, would hit it.

Main's two videos that use `App` (free-vs-paid-ai-plans-2026, 3 lines;
siri-ai-ios-27-how-to-get-it, 8 lines; owner claude-opus-4-8) are not recorded yet. Their
zh-TW narration will now say "A P P" where #891 had left the word to the voice.

## Definition of done

- [ ] An en, ja or ko dub of a line containing `App` sends the word itself, not "A P P".
- [ ] zh-TW and zh-CN narration still say "A P P".
- [ ] Other letter-spelled aliases (`CBS` → `C B S` and the like) keep working in dubs where
      the letters are how every language says them. Only an alias that spells out a
      mixed-case word is dropped.

## Steps

- [ ] In `dubLexicon`, set an alias to null when it is the term's own letters separated by
      spaces and the term is not all capitals (`App` → `A P P` is dropped, `CBS` → `C B S` stays).
- [ ] Test in `tools/video/dubs/plan.test.mjs`.
- [ ] Tell the #891 videos' owner that the zh-TW voice now says "A P P" for `App`.

## How to verify

`node --test tools/video/dubs/plan.test.mjs`. Then `dub --slug <video> --locale en --dry-run`
on a video whose en translation says "App Store", and read the planned request text.

## Notes

- Scope overlaps `2026-09-26-video-dubs-worker` (review) on `tools/video/dubs`. That one is
  about the worker, not the lexicon, so either order works.
