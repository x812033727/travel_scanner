---
id: 2026-10-03-drama-craft-in-video-tools
title: Drama craft in the tools: cut pace lint, craft rows, worker prompts, several cuts from one clip
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1-video-craft
claimed_at: 2026-10-03T06:42:20Z
created_at: 2026-10-03T02:52:05Z
completed_at:
branch: claude/video-production-skills-7d87cc
depends_on: []
scope:
  - tools/video/core/craft.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/ledger.mjs
  - tools/drama-craft-check.test.mjs
  - .agents/skills/youtube-video/scripts/drama_craft_check.mjs
  - .agents/skills/youtube-video/references/drama-craft.md
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - .agents/skills/youtube-video/references/prompts/writer-drama.md
  - .claude/skills/youtube-video/references/prompts/writer-drama.md
  - .agents/skills/youtube-video/references/prompts/verifier-drama.md
  - docs/videos/DRAMA.md
  - docs/videos/AUTOMATION.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Drama craft in the tools: cut pace lint, craft rows, worker prompts, several cuts from one clip

## Why

The owner rated the wedding pilot's look about 60 out of 100 and said nobody would keep
watching. On 2026-10-03 five AI dramas that people do click on were measured in the in-app
browser (`docs/videos/drama-craft/reference-study-20261003.md`): they change picture every
1.5 to 2.25 seconds at the median, open inside an event with four to eight shots in the first
ten seconds, show lines of one to eleven characters, and cover a scene from three or four
camera setups that they cut between. The craft spec and a standalone check now live in the
skill (`.agents/skills/youtube-video/references/drama-craft.md`,
`.agents/skills/youtube-video/scripts/drama_craft_check.mjs`), but the tools still pull the
other way, and the host worker never reads the skill's files:

1. `lint` warns when the median shot is under 3 seconds (`MIN_MEDIAN_SHOT_SECONDS` in
   `tools/video/core/drama.mjs`), "cuts this fast read as a montage, merge some shots". Every
   reference is faster than that.
2. The craft rows (opening shots, wide shots, looks in a row, line length, narration share)
   are printed only by the skill script. The worker's fix loop cannot see them, so a hands-off
   episode is never sent back for them.
3. The worker sends `tools/video/automation/prompts.mjs`, not the skill's prompt files. Its
   drama and series writer text still says a shot carries 3 to 10 seconds, a line is about 25
   characters and the narrator carries the story.
4. One shot scene buys one keyframe and one clip and uses the clip once. The references reuse
   a setup: speaker, listener, back to the speaker from the same camera position. With one
   8-second clip per cut, cutting as densely as they do costs a clip per cut.
5. A scene without lines is a schema error (`tools/video/core/schema.mjs`: "a scene lasts as
   long as its narration"), so a silent action or reaction shot cannot be written in a
   `video.json`; the pilot keeps its silent windows in its own edit plan. The craft spec tells
   writers to hang the off-screen speaker's line on the shot instead.
6. For a `visual: "still"` shot `motionMove` (`tools/video/assemble/drama.mjs`) reads `motion`
   when `camera` names no move, with unanchored patterns: "She pushes the box back" becomes a
   push-in, "rises" (also inside "surprised" and "enterprise") a tilt up. The spec now asks for
   action verbs in `motion`, which is what reaches this.

## Definition of done

- [x] `lint` no longer tells a writer to merge shots at a median the references sit above: the
      warning starts under 2 seconds, and its text points at the craft spec.
- [x] `lint` prints the craft rows for a drama with a cast as warnings (same ids as the skill
      script, one implementation shared by both), and the worker's script verdict sends an
      episode back to the writer when the opening or the coverage rows miss.
- [x] The worker's drama and series writer and verifier prompts carry the craft rules (opening,
      coverage list, line length, narration share, `camera` starts with the shot size, the
      off-screen line on a reaction shot), and a test keeps them in step with the skill's
      `writer-drama.md`.
- [x] A shot scene can cut from another shot's clip (`source: { shot, from_s }`): `clips` buys
      nothing for it, `assemble` trims the named clip, the frame-zero check compares against the
      source clip's frame at `from_s`, and the ledger shows the saving. The punch-in (a crop to a
      closer size from the same clip, at most 1.5x) is **not done**: it needs one pilot scene's
      1080p clip to measure how the crop holds up, and no pilot clip exists locally; the spec and
      `docs/videos/DRAMA.md` say so, and nothing assumes it.
- [x] A shot without lines has a stated length: `action_seconds` (1 to 8) with an empty `lines`
      array is accepted in a drama with a cast that carries no length floor
      (`timesSilentShots`), not only under the long-anime policy; a narrated video, a knowledge
      long-form (a brand story with leads, an explainer) and an anime episode still refuse it,
      since their lengths are measured on their narration or their policy. The reviewer's first
      pass caught the brand-story gap; the regression is in `drama.test.mjs`.
- [x] `motionMove` reads the move from `camera` only, treats locked as no move (`locked`: the
      keyframe held still, PSNR-checked like a push-in), and anchors its patterns.
- [x] `docs/videos/DRAMA.md` and the skill's `drama.md` describe the new fields; the craft
      spec's paragraph on what the tools cannot do yet is updated, and the check script's
      `lines.empty` row counts only shots with neither lines nor `action_seconds`.

## Steps

- [x] Lower the median warning and reword it (constant, test, the sentence in `drama.md`).
- [x] Move the check's pure functions where both `lint` and the skill script can import them:
      `tools/video/core/craft.mjs` (the worker image ships `tools/video` alone); the skill script
      is the command and re-exports; `tools/drama-craft-check.test.mjs` stays green.
- [x] Bring `prompts.mjs` in line (drama writer, series episode writer, both verifiers, the
      discuss variant, the production guide) and add the craft rows to `scriptVerdict`.
- [x] Design the clip-reuse and silent-shot fields with the frame-zero and hash rules, then
      implement them.
- [x] Fix `motionMove`.
- [ ] Independent duration-only review increment for the bound files, then
      `node tools/video/long-form/cli.mjs check`.

## How to verify

```bash
node --test tools/video/core/drama.test.mjs tools/video/core/lint.test.mjs tools/video/core/timeline.test.mjs tools/video/assemble/drama.test.mjs tools/video/automation/prompts.test.mjs tools/video/automation/series.test.mjs tools/video/media/clips.test.mjs tools/drama-craft-check.test.mjs
node tools/video/cli.mjs lint --file tools/video/core/fixtures/drama/video.json   # prints the craft rows as warnings
node tools/video/long-form/cli.mjs check
```

The fixture lint prints eight `craft …` warnings and no error: a four-shot retelling misses the
craft rows by design. A `clips --dry-run` on a script with a `source` shot prints "N cuts from
another shot's clip (nothing to buy, S clip seconds saved)" and prices only the clips.

## Notes

- `tools/video/core/drama.mjs`, `lint.mjs`, `schema.mjs`, `timeline.mjs`, `prompts.mjs`,
  `series.mjs`, `flow.mjs`, `assemble/cli.mjs` and their tests are bound by the duration
  receipt (`docs/videos/long-form/review.json`); this change carries its own independent
  duration-only increment in `docs/videos/long-form/review.md`.
- PR #1166 edited `drama.mjs` and `assemble/drama.mjs` first; this change is on top of it.
- The contract, as implemented (2026-10-03):
  - `tools/video/core/craft.mjs`: `craftChecks(doc, { timeline })` (the skill script's table,
    on lint's own timeline when one is given), `craftProblems(doc, timeline)` (what lint
    warns: `craft <row>: <label> <value>, target <target>; <hint> (<shots>)`), `CRAFT_GATE_ROWS`
    and `craftGateProblems(report)` (what sends a hands-off script back: `hook.*`,
    `motion.opening`, `size.face`, `size.wide`, `size.reestablish`, `size.stall`). A long anime
    keeps to its production policy: no craft rows in lint or the verdict.
  - `MIN_MEDIAN_SHOT_SECONDS` is 2 for a drama with a cast; `MIN_MEDIAN_SHOT_SECONDS_NARRATED`
    keeps 3 for an explainer or illustrated slides.
  - `data.source: { shot, from_s }`: an earlier clip shot with a clip of its own; no
    `start_frame`, `end_frame`, still or thumbnail; `from_s` plus the estimated length within
    10 s (`MAX_SOURCE_CLIP_SECONDS`), within 8 s under a production profile. `keyframes` skips
    it (`drawnShotScenes`); `clips` records `{ source: { shot, from_s, from_frame }, file,
    sha256, frames, seconds, needed_s }` after the bought clips, `needs_review` when the source
    failed or is too short, and books `{ kind: "clip", status: "cut", cost_usd: 0,
    saved_seconds, saved_usd }` in the ledger (`bookReuse`, replaced on rerun; `savedTotals`
    sums them). `assemble` trims with `trim=start_frame`, counts the frames after the start as
    available, and compares the segment's frame 0 with the source clip's frame there
    (`frameArgs`, `sourceFrameProblem`, `metrics.shots[].source_frame_psnr`).
  - `action_seconds` on a cast drama: `schema.mjs` and `timeline.mjs` accept it where the
    long-anime gate stood; `timesSilentShots(doc)` decides (`hasCast`, no `needsMinimumLength`,
    not `isKnowledgeLongform`, which moved to `drama.mjs` and is re-exported by `duration.mjs`,
    and not category anime).
  - `motionMove` / `cameraMove`: `camera` only, whole words; `locked` (locked, static, fixed,
    tripod) holds the picture (`zoompanExpr` z=1), a written `drift` wins over `static`.
- What the measurements do not cover is listed at the end of the craft spec: sound, retention
  curves and movement inside a shot were not measured, so none became a lint rule.
- Open question left for whoever designs it: an insert that shows only a hand. Listing the
  character brings the right sleeve and ring from the sheet, but the judge's identity question
  needs a face. The skill does not rule on it yet.
- Tests on Windows: `tools/video/assemble/assemble.test.mjs` "native auto-fit probes every
  directed clip" and eleven `automation.test.mjs` cases (thumbnails, uploads, lanes, restyle)
  fail on this machine on `origin/main` as well (shebang stand-ins for ffprobe cannot run, the
  font package is not installed); CI on Linux is where they count.
