---
id: 2026-10-03-ai-term-system-one-model-video
title: Produce the AI terms episode on System One models (ai-term-system-one-model)
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-03T17:48:48Z
completed_at:
branch:
depends_on:
  - 2026-10-03-ai-term-system-one-model-article
  - 2026-10-03-ai-terms-episode-system-one-plan
scope:
  - docs/videos/ai-term-system-one-model
  - docs/videos/ai-terms/terms.json
  - docs/videos/ai-terms/README.md
  - docs/videos/long-form/plans.json
  - tools/video/long-form/plans.mjs
  - docs/videos/lexicon.json
  - docs/videos/ILLUSTRATED.md
---

# Produce the AI terms episode on System One models (ai-term-system-one-model)

## Why

The brief for the System One model episode of 「AI 名詞十分鐘」 is written
(`docs/videos/ai-term-system-one-model/brief.md`). This task takes it from the outline gate to
an upload package and registers the term in the series catalogue.

It is also the pilot that fills `docs/videos/ILLUSTRATED.md` 「試片的數字表」: the owner merged
`2026-09-29-video-pilot-jev-decision-model` into it on 2026-10-03 (see that task, now in
`tasks/done/`). Every number in `docs/videos/ILLUSTRATED.md` (cost, pace, judge first-pass
rate, the owner's review minutes) is still an estimate, and this episode measures them.

## Definition of done

- [ ] The owner has answered `docs/videos/ai-term-system-one-model/notes.md` §站主要決定的事,
      at least items 3, 5, 6 and 7 (items 1 and 2 were decided on 2026-10-03), before anything
      is generated.
- [ ] `docs/videos/ai-terms/terms.json` has the row in `notes.md`, `counts` updated,
      `CATALOG_COUNTS["ai-terms"]` raised in `tools/video/long-form/plans.mjs`, and
      `node tools/video/long-form/cli.mjs build` then `check` pass. The duration review and the
      admin catalog are hash-bound to these files: widen this scope to whatever `check` names.
- [ ] The writing-day run in `demo-log.md` is done and its output pasted there.
- [ ] The episode goes through the automated route from `review-push --gate outline` to
      `package`, with `video.json`, `claims.md`, `verify-*.md`, `shorts.json` and `i18n/`.
- [ ] `lexicon.json` has the words the brief lists under 素材.
- [ ] Acceptance, carried from the pilot and brought up to today's rules: hook ≤ 20 s; at least
      two 「你以為…其實…」, the first inside chapter 1 as `REGISTER_RULES` requires (the brief has
      one in chapter 1 and one in chapter 3); every chapter except the last ends on the question
      the next one answers, and the last answers the hook; no state longer than 8 s, average
      ≤ 6 s, shot share ≥ 0.5 (as `qa`'s pace check counts them); shots cut, and dissolve only
      after a pause beat of at least 600 ms (`DISSOLVE_BEAT_MS`, `tools/video/assemble/drama.mjs`;
      do not write `transition` by hand), chapter cards hard-cut, single-state cards drift;
      music bed ≤ −24 LUFS, final −14 LUFS; sound effects never cover the narration; no
      burned-in text; media spend ≤ US$15 (`ILLUSTRATED.md` §成本 expects about US$9–12; the
      server cap `slides_max_usd_per_video` defaults to US$20, so a run between 15 and 20 is
      recorded as failing this line, not hidden).
- [ ] `docs/videos/ILLUSTRATED.md` 「試片的數字表」 filled from this run: illustrations,
      retakes, judge first-pass rate, media spend, minutes from launch to final, the owner's
      minutes reviewing the final, longest state / average / shot share, and an observation
      beside Gary Chen's `2mtn-Qp59y4` (same subject, different angle; not a point-by-point
      comparison). Also update the two rows that still name the pilot (「第一支試片」 and
      「9 試片〈Jev〉」) to point at this episode, and the 「並排的觀察」 label in the table.
      Decide with the owner whether the first-deployed-video checks in `ILLUSTRATED.md`
      §第二輪 (first 2K image, the judge's craft-score distribution, the style plate) are also
      measured here or by the slide videos already queued.
- [ ] With the numbers in hand, the owner decides whether the 10 older slide videos are redone
      or published as they are; record the decision here. Measure each first with
      `node tools/video/cli.mjs restyle --slug <slug> --dry-run`. A new voice is `restyle`;
      adding illustrations means rewriting each script with `shot` scenes, filed as separate
      tasks because those folders are in other tasks' scope.

## Steps

- [ ] Wait for the article task, and for the tasks holding this scope today
      (`npm run tasks -- claim` refuses until they release it, stale or not):
      `2026-09-29-ai-terms-video-pilot` (review: `docs/videos/ai-terms`, `lexicon.json`),
      `2026-09-27-developer-ai-coding-tool-comparison-video` and
      `2026-09-28-en-video-01-openai-agents-broke` (in progress: `lexicon.json`),
      `2026-10-03-illustrated-slides-round-2-a-family` (review: `ILLUSTRATED.md`).
      `lexicon.json` only gains lines, which is why the ai-terms pilot was claimed with `--force`
      over the same overlap; do the same only if the owner agrees.
- [ ] Turn off Jev's outline pick and final auto-approval for this one video, or approve both
      gates by hand (`notes.md` item 6).
- [ ] The owner's phase-0 setup from the pilot, if not already done: in `/admin/videos`
      settings, tutorial (教學) tab: the Gemini voice `style` from `STORY_VOICE_STYLE`
      (`tools/video/automation/register.mjs`; new installs already default to it, existing rows
      need pasting); 「投影片影片的插畫」 switched on (gemini-3.1-flash-image, per-video cap
      `slides_max_usd_per_video` in US$, storyboard auto-approval on); a licensed music file
      name (e.g. `bed.mp3`; mp3, m4a, wav or flac) and a sound-effect set (e.g. `studio-a`, with
      `stamp`, `whoosh` and `pop`). `REGISTER_RULES` is already in the prompts; paste nothing
      else unless the channel has its own catchphrases. On the worker host
      `<VIDEO_WORKDIR>/_music/<file>` and `<VIDEO_WORKDIR>/_sfx/<set>/` with `manifest.json`
      (format in `docs/videos/ILLUSTRATED.md` §`video.json` 多了什麼).
- [ ] Record every step's numbers as it runs, for the table above.
- [ ] `docs/videos/ILLUSTRATED.md` is held by `2026-10-03-illustrated-slides-round-2-a-family`
      (review) today; claim this task after that one lands.

## How to verify

```bash
node tools/video/long-form/cli.mjs check
npm run test:tools
node tools/video/cli.mjs status --slug ai-term-system-one-model
node tools/video/cli.mjs qa --slug ai-term-system-one-model
node tools/video/cli.mjs media-status
```

`status` lists, in order: keyframes drawn, storyboard approved, frames rendered, music
generated, video assembled, final video approved. `qa`'s pace line prints the longest state,
the average and the shot share; `media-status` prints the spending ledger. Those two are the
source of the acceptance numbers and of the `ILLUSTRATED.md` table.
