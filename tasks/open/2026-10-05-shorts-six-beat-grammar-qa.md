---
id: 2026-10-05-shorts-six-beat-grammar-qa
title: Shorts six-beat grammar and a grammar QA item: first frame is the thumbnail, last frame returns to it, no CTA
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:27Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/prompts.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/build.mjs
  - tools/video/shorts/motion.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/shorts/pipeline.test.mjs
  - tools/video/shorts/motion.test.mjs
  - tools/video/shorts/smoke.mjs
  - .agents/skills/youtube-video/references/prompts/shorts-lab.md
  - .agents/skills/youtube-video/references/prompts/shorts-cut.md
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/SHORTS.md
  - .agents/skills/youtube-video/references/shorts.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Shorts six-beat grammar and a grammar QA item: first frame is the thumbnail, last frame returns to it, no CTA

## Why

The Shorts writer prompts say only that the first two seconds are the question or the result.
The faceless-shorts repo (MIT) encodes what keeps a 40-second Short watched to the end: a six
beat grammar (hook → setup → quiz → reveal → twist → loop), frame 0 fully composed as the
thumbnail, the last frame returning to the first so the loop is seamless, and no dated
engagement CTA. None of that is checked today.

## Definition of done

- [ ] Schema v2 scenes take an optional `beat` (`hook | setup | turn | proof | payoff | loop`,
      in order); the writer prompts ask for all six; `validate` checks the order.
- [ ] A 13th QA item `grammar` (appended to `ITEM_IDS` and the server's `SHORTS_QA_ITEMS`
      together, with a `qaItems.grammar` label in five locales): frame 0 is the thumbnail
      (`cover.png` equals frame 0 and the first card carries a ≤ 14-character headline or a
      `big`), the last frame returns to the first (a 12-frame tail dissolving to frame 0,
      PSNR ≥ 30), no CTA (訂閱 / 按讚 / 小鈴鐺 / 點連結 / 追蹤 absent from phrases, headlines,
      body and note).
- [ ] The smoke script carries beats and passes `grammar`.

## Steps

- [ ] `core.mjs` beats + validation; `prompts.mjs`, `shorts-lab.md`, `shorts-cut.md`.
- [ ] `motion.mjs` loop tail (last segment dissolves to the first frame); `build.mjs`.
- [ ] `qa.mjs grammar`; `judge.py SHORTS_QA_ITEMS`; `admin.json` ×5; tests; smoke; docs.
- [ ] Receipt increment by an independent agent (`judge.py`, admin.json ×5).

## How to verify

```bash
node --test tools/video/shorts/*.test.mjs
node tools/video/shorts/smoke.mjs --workdir /tmp/shorts-smoke
cd apps/api && uv run pytest tests/test_video_automation_judge.py -q
node tools/video/long-form/cli.mjs check
```

## Notes

- After `2026-10-05-shorts-karaoke-captions-estimated-timing` (PR #1292) on `build.mjs`,
  `motion.mjs`, `qa.mjs`; add it to `depends_on` once it is in `tasks/done/`.
- Bound: `apps/api/app/video_automation/judge.py`, `apps/web/messages/*/admin.json`.
- YouTube Shorts loop practice; no outside code.
