---
id: 2026-10-08-video-qa-undecided-languages
title: QA requires only narration captions before language selection
status: in-progress
priority: P1
area: tools
owner: codex-stalled-video-completion
claimed_at: 2026-10-08T06:43:25Z
created_at: 2026-10-08T06:43:24Z
completed_at:
branch: codex/stalled-videos-completion-20261008
depends_on: []
scope:
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# QA requires only narration captions before language selection

## Why

Final QA required four untranslated caption tracks before the owner could open
the language selection panel, which itself requires final approval. A real
Cloudflare Workers export had current zh-TW captions and no language choice,
but its captions item failed for en/ja/ko/zh-CN.

## Definition of done

- [x] Undecided final QA checks narration and mandatory zh-TW only.
- [x] Explicit selected metadata/caption parts remain enforced separately.
- [x] QA makes no owner choice and retains all other quality and duration gates.
- [ ] Independent duration review bindings cover the two changed QA files.

## Steps

- [x] Collision-check and claim the two QA files.
- [x] Add real CLI regression for no choice, metadata-only English, and selected CC.
- [x] Run all15 QA CLI tests, zero failures/skips; independent source review passes.
- [ ] Rebind duration review through a different reviewer, not the author.

## How to verify

`node --test tools/video/qa/qa.test.mjs`; `node tools/video/long-form/cli.mjs check`;
`node tools/tasks.mjs check`. The regression removes untranslated caption files,
checks that no choice file is created, then chooses English captions and requires
their absence to fail without requiring unchosen languages.

## Notes

- Narrow change affects ordinary final QA; legacy caption generation and compilation
  language rules remain unchanged. English narration still requires en plus zh-TW.
- Private verified runtime SHA514539d4f6a9f4df285567791957d0aa9c66318bbbced3d8800d6193f3383267.
- Actual focused15 tests pass. A broad Windows tools run observed2060passed,
  8failed and13skipped; it is not reported as green. Existing Windows c: ESM
  hang was verified and only its owned test child stopped after40minutes.
  Other observed failures are preserved in the private raw log and tracked separately.
