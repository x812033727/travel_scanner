---
id: 2026-09-29-dubs-spell-out-app-as-a
title: Dubs spell out App as A P P: drop letter-spelling aliases of mixed-case words outside Chinese
status: done
priority: P3
area: tools
owner: codex-gpt6-dub-lexicon
claimed_at: 2026-09-30T04:20:35Z
created_at: 2026-09-29T03:28:43Z
completed_at: 2026-09-30T04:29:09Z
branch: codex/dub-word-aliases
depends_on: []
scope:
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/plan.test.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/tts/check.mjs
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

- [x] An en, ja or ko dub of a line containing `App` sends the word itself, not "A P P".
- [x] zh-TW and zh-CN narration still say "A P P".
- [x] Other letter-spelled aliases (`CBS` → `C B S` and the like) keep working in dubs where
      the letters are how every language says them. Only an alias that spells out a
      mixed-case word is dropped.

## Steps

- [x] In `dubLexicon`, set an alias to null when it is the term's own letters separated by
      spaces and the term is not all capitals (`App` → `A P P` is dropped, `CBS` → `C B S` stays).
- [x] Test in `tools/video/dubs/plan.test.mjs`.
- [ ] Tell the #891 videos' owner that the zh-TW voice now says "A P P" for `App`.

## How to verify

`node --test tools/video/dubs/plan.test.mjs`. The CLI regressions create a fixture whose
translation says "App Store", run `dub --dry-run`, then capture the real request bodies
through a mocked speech service. Dry-run output itself reports billing, not request text.
They also verify Chinese dubs of an English source via `--file`, cache invalidation/reuse,
and the checker's expected spoken forms without contacting real services.

## Notes

- 2026-09-30 preclaim audit: main `72069973`, 26 open PRs, remote/local branches,
  active claims and 176 accessible worktrees have no competing work in these four files.
  The old `2026-09-26-video-dubs-worker` overlap is obsolete: that ticket is done on main.
- Expanded the scope to the dub CLI and audio checker: both must select the same dictionary
  by the target language. `loadProject` filters its dictionary for the source narration, so
  target-language selection must start from the raw shelf dictionary (also for `--file`).
- The ticket's complete-letter rule also applies to `iOS` → `i O S` outside Chinese.
  Partial names such as `OpenAI` → `Open A I` and all-capital acronyms stay unchanged.
- Validation on bundled Node 24.19.0: 10 new regressions passed; 38 existing dub/check/locale
  tests passed. The full existing tool suite passed 924 tests with 2 skips (926 total);
  the new file was added after that run started and was tested separately.
- Independent review found no blocking request-generation issue. The existing gap where
  a finished dub can remain `current` after its target pronunciation changes is tracked in
  `2026-09-30-invalidate-dubs-when-target-pronunciation-changes`; direct `dub` reruns already
  regenerate affected clips through their changed request keys.
- Owner handoff for #891: `free-vs-paid-ai-plans-2026` and
  `siri-ai-ios-27-how-to-get-it` still receive `App` → `A P P` in zh-TW/zh-CN. This change
  leaves the shared lexicon unchanged. Their current recording status was not inspected.
  This note is included in the PR/user handoff; the unchecked notification step records
  that no separate message was sent to the other author's chat.
