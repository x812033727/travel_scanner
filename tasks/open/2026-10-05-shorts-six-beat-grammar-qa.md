---
id: 2026-10-05-shorts-six-beat-grammar-qa
title: Shorts six-beat grammar and a grammar QA item: first frame is the thumbnail, last frame returns to it, no CTA
status: in-progress
priority: P2
area: tools
owner: claude-fable-5-1-sixbeat
claimed_at: 2026-10-05T18:00:54Z
created_at: 2026-10-05T16:08:27Z
completed_at:
branch: claude/shorts-six-beat
depends_on:
  - 2026-10-05-shorts-karaoke-captions-estimated-timing
scope:
  - tools/video/shorts/prompts.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/build.mjs
  - tools/video/shorts/motion.mjs
  - tools/video/shorts/lab.mjs
  - tools/video/shorts/cut.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/shorts/pipeline.test.mjs
  - tools/video/shorts/motion.test.mjs
  - tools/video/shorts/lab.test.mjs
  - tools/video/shorts/cut.test.mjs
  - tools/video/shorts/bindings.test.mjs
  - tools/video/shorts/smoke.mjs
  - .agents/skills/youtube-video/references/prompts/shorts-lab.md
  - .agents/skills/youtube-video/references/prompts/shorts-cut.md
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/tests/test_video_shorts.py
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

- [x] Schema v2 scenes take an optional `beat` (`hook | setup | turn | proof | payoff | loop`,
      in order); the writer prompts ask for all six; `validate` checks the order.
- [x] A 13th QA item `grammar` (appended to `ITEM_IDS` and the server's `SHORTS_QA_ITEMS`
      together, with a `qaItems.grammar` label in five locales): frame 0 is the thumbnail
      (`cover.png` equals frame 0 and the first card carries a ≤ 14-character headline or a
      `big`), the last frame returns to the first (a 12-frame tail dissolving to frame 0,
      PSNR ≥ 30), no CTA (訂閱 / 按讚 / 小鈴鐺 / 點連結 / 追蹤 absent from phrases, headlines,
      body and note).
- [x] The smoke script carries beats and passes `grammar`.

## Steps

- [x] `core.mjs` beats + validation; `prompts.mjs`, `shorts-lab.md`, `shorts-cut.md`.
- [x] `motion.mjs` loop tail (last segment dissolves to the first frame); `build.mjs`.
- [x] `qa.mjs grammar`; `judge.py SHORTS_QA_ITEMS`; `admin.json` ×5; tests; smoke; docs.
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

### 2026-10-05 done (claude-fable-5-1-sixbeat, branch `claude/shorts-six-beat` on top of #1305)

- **Scope widened before the claim**, each for a reason the ticket could not see: `cut.mjs` and
  `cut.test.mjs` (the `shorts-cut.md` prompt's original moved to `cut.mjs` on 10-04 and its test
  pins the copy byte for byte); `lab.mjs` and `cut.mjs` (their `SCENE_FIELDS` whitelists would
  have dropped the writer's `beat` silently, so the prompt change would have been hollow for the
  worker); `lab.test.mjs`, `cut.test.mjs`, `bindings.test.mjs` (their stand-in measurements of
  the final must now carry `grammar`, or the new item fails and `passingBuild` asserts all pass);
  `apps/api/tests/test_video_shorts.py` (hardcoded the 12-item auto-approval note; now reads
  `SHORTS_QA_AUTO_APPROVED_NOTE`). No active ticket held any of them (`claim` did not refuse).
- **Beats**: `BEATS` in `core.mjs`; `validate` holds the order (repeat allowed, never backwards,
  optional, schema 2 only). Both writer prompts (`prompts.mjs` `writer:shorts-lab`, `cut.mjs`
  `writer:shorts-cut`, skill copies regenerated from the originals) ask for all six, a ≤ 14
  character first headline or a `big`, and no call to action; the cut's lead-back is now "完整影片在說明欄",
  never 點連結.
- **Loop tail** (`motion.mjs`, `MOTION_VERSION` v3): the last segment takes the first segment's
  frame 0 (`build/scene-000.png`, the cover) as one more input, `fade=t=in:s=0:n=12:alpha=1`
  by frame count, `setpts` to the segment's end, `overlay=eof_action=repeat` over cards and
  captions; measured with ffmpeg 6.1 that frames before the tail pass through untouched and the
  last frame is the still whatever image2 rounds the input length to. `measureFinal` takes
  `{ cover, frames }` and returns `grammar { cover_psnr, loop_psnr }` (`framePsnrArgs`, RGB, one
  clock); `build` fails on `loopProblems` like it does on profile and loudness, and writes
  `checks.json.grammar` (inf capped to 100, `PSNR_CAP`).
- **`grammar` item** (`qa.mjs`, 13th, appended): `loopProblems` (cover ≥ 40 dB, loop ≥ 30 dB)
  plus `scriptGrammarProblems` (first headline / `big`, `callsToAction` over headline, kicker,
  big, body, note and narration). The same text rules run in the lab and cut lints so the writer
  fixes them before narration is paid for, and `grammar` is in the worker's `QA_FIXES`.
- **CTA words are patterns, not substrings**: 按讚/點讚, 小鈴鐺, 點(擊|下)連結 always; 訂閱 and
  追蹤 only as asks (記得訂閱, 訂閱我們, 追蹤頻道 …), so "訂閱制方案" and "追蹤包裹" pass; English:
  subscribe, hit/smash that like, like and subscribe, ring/hit the bell, link in bio, click the
  link, follow us. Add words to `CALLS_TO_ACTION` as they show up.
- **Measured on the smoke** (six scenes with the six beats, a sixth `loop` scene added in
  memory, 1152 frames): cover PSNR inf (identical), loop 38.4 dB (a flat synthetic picture scores
  52.9 dB; the drifting backdrop and the cards under the dissolve lower it), `grammar` passes
  offline, 8 of 13 items without the site. Frames 0 / 1139 / 1145 / 1151 looked at: hook card,
  loop card, mid-dissolve, hook card again.
- **Checks run**: 172 Shorts tests, `npm run test:tools` (1715 pass, the one failure is the
  stale duration receipt), judge/shorts/renewal/integration pytest (106 pass), ruff, mypy app
  and tests, `check:i18n`, `lint:web`, `typecheck:web`, `check:tasks`.
- **Receipt**: `node tools/video/long-form/cli.mjs check` names the six bound files this
  changed — `apps/api/app/video_automation/judge.py` and the five `apps/web/messages/*/admin.json`
  — for the independent reviewer's increment; `review.md`/`review.json` untouched here.
- **Noticed, not fixed** (filed as `2026-10-05-shorts-thirteen-items-wording`): the
  youtube-video `SKILL.md` (both copies, receipt-bound) still says 12 項自動品管; comments in
  `apps/api/app/video_shorts/models.py` and `video_reviews/admin_service.py` say "twelve"; the
  web fixtures in `admin-video-shorts.test.tsx` carry 12-item summaries as data (harmless).
- **Not done, by design**: an imported cut (`import`) passes `grammar` only if its maker did the
  same three things; the vertical drama line should carry the loop tail when it exists. The
  loop tail overlaps the last phrase's final 0.22 s of speech (the timeline pads 0.18 s).
- Environment: `/opt/pw-browsers` now ships Chromium 1243, which Playwright 1.63 wants, so the
  symlink workaround of the karaoke ticket was not needed.
