---
id: 2026-10-13-narrated-videos-tell-one-story-with
title: Narrated videos tell one story with hooks and close without naming the next video
status: review
priority: P1
area: tools
owner: claude-fable-5-1-narrative
claimed_at: 2026-10-13T00:50:29Z
created_at: 2026-10-13T00:46:53Z
completed_at:
branch: claude/youtube-narrative-flow-1cadbc
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/fixtures
  - tools/video/core/captions.test.mjs
  - tools/video/cli.mjs
  - tools/video/cli.test.mjs
  - tools/video/automation
  - tools/video/templates/terminal/fixtures/claude-code/video.json
  - tools/video/screencast/fixtures/tutorial/video.json
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/README.md
  - docs/videos/history-curiosity/README.md
  - docs/videos/ai-terms/README.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
  - docs/videos/curio-h01-v2
---

# Narrated videos tell one story with hooks and close without naming the next video

## Why

The owner, 2026-10-13: the remastered videos are finished work, but the content "feels patchwork,
the opening condensation included", a viewer cannot follow it from one chapter to the next, and it
should be told like a story with hooks placed now and then. They scored the content 50 of 100 and
want 85 or more. They also asked for one cut: the close must stop saying what the next video is
about. Their reference channels are 馬臉姐 (@malianjie) and 老高與小茉 (@laogao), for pacing too.

Read against the five delivered 奇聞檔案局 recuts, the rules themselves were the cause:

- script-writing.md §節奏 asked for chapters that stand alone ("a viewer who jumps in still follows"),
  so each one opened on a label (「先講大家聽過的那個版本」「打開檔案的第一頁」「回到清單上」) and
  closed on a 「那…？」 the next chapter did not answer.
- The 奇聞檔案局 profile made the chapters functional sections (流傳的版本 / 紀錄裡有什麼 / 最站得住的解釋).
- CONDENSATION_RULE asked the opening to tease two or three later moments, so h01's opening gave
  away the blood test, the nine empty casks and the ending, and the body then said them again.
- No rule asked for a forward hook or a payoff; 1,701 casks was said five times.
- The 奇聞檔案局 writer never received REGISTER_RULES, where chapter-to-chapter linking lived, and
  lint's warnings never reached the writer at all.

## Definition of done

- [x] One rule text (`register.mjs` NARRATIVE_RULES, script-writing.md §故事主線與鉤子) says how a
      narrated video is one story: a spine, chapters as beats named by what happens, each opening
      on the consequence of the one before, an open loop every 60-90 s, every loop paid off and
      named, a fact told once, sentences joined the way a person tells a story.
- [x] The condensation is ONE scene told in order up to the first fact that makes no sense, ending
      on the video's question: it reveals no later chapter's result (it kept its 30-60 s).
- [x] A script carries a `loops` table (schema: both ids exist, the payoff is after the setup,
      `what` is at most 40 characters); lint counts them (3 per ten minutes, one in the opening).
- [x] lint reads the storytelling of every narrated episode (slides, explainers, brand stories):
      chapter labels, hook cadence, loops and repeated facts are warnings, and a close that names
      the next video is an error. The narrative warnings reach the writer with the next rewrite.
- [x] The storytelling panel: ten yes-or-no questions answered blind by a reader that is given the
      script and nothing else, after the listener's edit; a required "no" sends the script back to
      the writer twice, then the video waits for the owner. The worker asks it itself; the
      owner-driven route runs `cli.mjs narrative --slug`.
- [x] Nothing in the prompts, the skill or the series docs tells a close to name the next video or
      the next file, and no fixture does either.
- [ ] The owner has seen the proof: H01 (瑪麗賽勒斯特號) rewritten under the new rules, against the
      old script, script only (docs/videos/curio-h01-v2).

## Steps

- [x] `tools/video/core/narrative.mjs`: the checks, the panel, the narration renderer.
- [x] `schema.mjs`: the `loops` field; `lint.mjs`: the narrated gate, the tagged problems.
- [x] `register.mjs`, `prompts.mjs`, `explainer-series.mjs`, `story-prompts.mjs`: the rules the
      worker sends, and the outlines that carry 主線 / 轉折 / 開場濃縮 / 鉤子.
- [x] `flow.mjs` + `story.mjs`: the gate, the bare stage (no standing instructions), the rounds.
- [x] `cli.mjs narrative`, the status line, the skill and the series docs.
- [x] Re-pin the prompt digests; fix the fixtures' closes and the hashes that moved with them.
- [x] An independent DURATION_ONLY increment for the receipt-bound files this PR touches.
- [ ] The H01 comparison for the owner, and the owner's decision on the five delivered recuts.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/core/lint.test.mjs tools/video/core/schema.test.mjs
node --test tools/video/automation/automation.test.mjs tools/video/automation/prompts.test.mjs tools/video/automation/explainer-series.test.mjs tools/video/automation/series.test.mjs tools/video/automation/story.test.mjs
node tools/video/cli.mjs lint --slug curio-h01-v2
node tools/video/cli.mjs narrative --slug curio-h01-v2        # the panel, for a blind reader
npm run test:tools && npm run check:tasks
```

## Notes

- **Deploying this re-asks an unfinished explainer stage.** The flat-explainer planner and writer
  texts and all eight profiled-series texts moved, so an episode left unfinished on the host when
  this deploys has that stage asked, and paid for, again (run-receipts.mjs). Deploy with none
  unfinished.
- The panel rides on the `verifier` stage under the variant `narrative`: the API's stage names are
  a closed list (`apps/api/app/video_automation/models.py` STAGES) and "verifier/narrative" fits
  the 32 characters the server keeps. It is sent `bare`, so no standing instruction, stance or
  genre section can colour a blind read.
- Only yes-or-no questions discriminate: the keyframe judge and the tutorial panel both taught
  this (a scale pins at the same number for a good script and a bad one).
- The narrative lint only reads a narrated zh-TW episode of MIN_EPISODE_MINUTES or more, so the
  fixtures that run seconds keep their shape and none of their tests moved for it.
- `docs/videos/so-thats-why/README.md` still says 鉤子 0:00-0:20 in §一集長什麼樣. It is in the
  scope of `2026-10-10-sothatswhy-minimax-images` (active), so it was left alone again; the
  prompt the worker reads (`explainer-series.mjs`) is current.
- Left for the owner to decide: whether the five delivered 奇聞檔案局 recuts are remade under the
  new rules (they chose "leave them, show me H01 first" on 2026-10-13).
- The `loops` table is a warning, not an error, for its first deploy: once a batch of scripts has
  passed with it, raising it to an error is a one-line change in `core/narrative.mjs`.
