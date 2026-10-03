---
id: 2026-10-03-drama-craft-spec-check-and-probe
title: Drama craft spec, craft check and shot probe for the youtube-video skill
status: done
priority: P1
area: docs
owner: claude-fable-5-1-video-craft
claimed_at: 2026-10-03T02:52:38Z
created_at: 2026-10-03T02:51:57Z
completed_at: 2026-10-03T06:41:26Z
branch: codex/wedding-visual-revision-20261003
depends_on: []
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/drama-craft.md
  - .agents/skills/youtube-video/references/visual-quality.md
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - .agents/skills/youtube-video/references/animation-production.md
  - .claude/skills/youtube-video/references/animation-production.md
  - .agents/skills/youtube-video/references/prompts/writer-drama.md
  - .claude/skills/youtube-video/references/prompts/writer-drama.md
  - .agents/skills/youtube-video/references/prompts/writer-series.md
  - .claude/skills/youtube-video/references/prompts/writer-series.md
  - .agents/skills/youtube-video/references/prompts/verifier-drama.md
  - .agents/skills/youtube-video/scripts/drama_craft_check.mjs
  - .agents/skills/youtube-video/scripts/yt_shot_probe.js
  - tools/drama-craft-check.test.mjs
  - docs/videos/drama-craft
  - docs/videos/DRAMA.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Drama craft spec, craft check and shot probe for the youtube-video skill

## Why

The owner rated the wedding pilot about 60 out of 100 ("不會想讓人想繼續看下去") and asked
for the production craft to be raised and made repeatable. PR #1161 first added a
visual-quality workflow: how to diagnose a rejected look, run a bounded pilot and keep
evidence. It says how to review, not what to write: there was no number for how fast a drama
cuts, how it opens, how long a line is or how a scene is covered, and nothing that measures a
storyboard before money is spent on it. The owner then asked for a second pass on the same
pull request, with research on the AI dramas currently on YouTube done in the in-app browser.

## Definition of done

- [x] Reference dramas people actually click on are measured, not sampled by eye: shot
      lengths, opening structure, line length, coverage and packaging, with the limits stated
      and what was only seen by eye marked as such.
- [x] The skill tells a writer what to aim for before writing a script and storyboard for a
      drama with a cast, with each target marked as measured or as an editorial rule.
- [x] A script turns a storyboard into pass or miss rows that name the shots at fault, and the
      writer and verifier prompts require it to be run and answered.
- [x] The measuring method is a reusable script with its steps, and an agent that had only
      those steps reproduced a measurement.
- [x] The wedding pilot's own edits are measured with the same check, the check's reading is
      compared with a hand reading of every shot, and the gaps are written down.
- [x] What differs from the channel's current spec and needs the owner (burned subtitles, name
      cards, vertical frame, the channel intro) is listed, not silently adopted.
- [x] Work the tools need is filed as its own task.

## Steps

- [x] Measure five dramas in the in-app browser with an in-page probe; validate the cut
      detector against contact sheets.
- [x] Write `references/drama-craft.md`, the study record and its raw data.
- [x] Write `scripts/drama_craft_check.mjs` with tests, and `scripts/yt_shot_probe.js`.
- [x] Route from `SKILL.md`, `drama.md` and `visual-quality.md`; update the drama writer and
      verifier prompts; keep the `.claude` copies identical.
- [x] Two independent reviews (one reviewer; then five lenses, each finding re-checked by a
      second agent), a forward test by a fresh writer, an independent replication of one
      measurement; fix what they found.
- [x] Merge `main`, and an independent duration-only increment for the two `SKILL.md`
      bindings.

## How to verify

```bash
node --test tools/skills.test.mjs tools/drama-craft-check.test.mjs
node tools/video/long-form/cli.mjs check
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/series-plans/competition-20261002/episodes/episode-01-measured-edit.json
npm run check:tasks
```

The third command prints eight missed rows for episode 1 (`hook.opening`, `hook.opening30`,
`size.insert`, `size.wide`, `size.reestablish`, `size.stall`, `motion.run`, `motion.opening`).

## Notes

- Measured on 2026-10-03, first 240 seconds of each, 0.25-second samples: median shot 1.5 to
  2.25 s across the five (the owner's own reference, 《山海经之万兽图鉴》, is 2.0 s; the design
  document said 5 to 8 and is corrected); four to eight shots start in the first ten seconds;
  no title sequence longer than a quarter second; burned-in lines of one to eleven characters;
  in four of five the first minute's subtitles read as dialogue. Combined views at the time
  were 4,181,443. Numbers and raw shot lengths: `docs/videos/drama-craft/reference-study-20261003.json`.
- Not measured, and said so in the spec: sound (the pane was muted, so "no narrator" is an
  inference from subtitles), retention curves (the watch page carries no most-replayed data),
  movement and camera movement inside a shot. Coverage shares of the references are by eye,
  except the inserts of one video.
- The pilot's episode 1 and 2 edits: 81 of 81 shots have a locked camera; about a third show
  only a look, a breath or a tremor; episode 1 has no wide shot at all and is 46% inserts;
  three shots start in the first ten seconds; episode 1's first three shots are all looks,
  the first of them five seconds of narration over a standing figure. Episode 1's line length
  and narration share were already inside the targets. The pilot's files are not changed here;
  they belong to `2026-10-02-wedding-competition-pilot-four-languages`.
- The first version of the check misread the pilot: "overhead hand shot" as a wide, hand and
  prop close-ups as faces, "a smile leaves his face" as an action, "sets the pen down" as
  nothing happening. Both reviews caught it. The rewritten reading agrees with a hand reading
  of the 81 shots on 80 sizes and 81 motions; the tables in the test file are those real
  lines. The published pilot numbers come from the rewritten script.
- Targets are set between the references and what the pipeline can pay for: median 2.5 to
  3.5 s rather than 2. `lint` still warns under 3 s; the spec tells the writer to keep the
  shots between 2 and 3 and say so. Changing that warning, feeding the rows to the worker,
  shots without lines and reusing one clip for several cuts is
  `2026-10-03-drama-craft-in-video-tools`.
- The share of look-only shots was first set at a quarter, with no evidence. Reaction shots
  are looks and a covered dialogue needs them, so the rule became: at most a third, at most
  two in a row, never all of the first three, whatever the camera does. It is an editorial
  rule and is labelled so.
- A fresh agent given only the skill wrote a 24-shot opening that met 18 of the then 19 rows
  on its first draft, with the conflict at 7.8 s; its storyboard misses the new `pace.spread`
  row (every shot nearly the same length), which is why that row and the "lengths differ"
  rule exist.
- An independent agent re-measured one reference from the probe's written steps and got the
  same 46 cuts; checking frames it found one cut 1.5 s early (a light leak before it) and
  one "cut" that is a person standing up. Both are recorded in the study; the probe's header
  says a run of flagged samples is counted at its first sample.
- How the probe works in the pane: seeking and `drawImage` work while the pane is hidden; a
  fresh watch page refuses `eval` of stored text (Trusted Types), so the script is pasted; a
  scripted click on "skip ad" is ignored, a real click works; a mid-roll advertisement can
  replace the video during a contact sheet, which the probe reports instead of drawing it;
  leaving `measure()`'s promise as the last expression makes the tool wait and time out.
