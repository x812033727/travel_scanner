---
id: 2026-10-03-drama-craft-in-video-tools
title: Drama craft in the tools: cut pace lint, craft rows, worker prompts, several cuts from one clip
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-03T02:52:05Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/schema.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/assemble/drama.mjs
  - tools/drama-craft-check.test.mjs
  - .agents/skills/youtube-video/scripts/drama_craft_check.mjs
  - .agents/skills/youtube-video/references/drama-craft.md
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - docs/videos/DRAMA.md
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

- [ ] `lint` no longer tells a writer to merge shots at a median the references sit above: the
      warning starts under 2 seconds, and its text points at the craft spec.
- [ ] `lint` prints the craft rows for a drama with a cast as warnings (same ids as the skill
      script, one implementation shared by both), and the worker's script verdict sends an
      episode back to the writer when the opening or the coverage rows miss.
- [ ] The worker's drama and series writer and verifier prompts carry the craft rules (opening,
      coverage list, line length, narration share, `camera` starts with the shot size, the
      off-screen line on a reaction shot), and a test keeps them in step with the skill's
      `writer-drama.md`.
- [ ] A shot scene can cut from another shot's clip (`source: { shot, from_s }` or similar):
      `clips` buys nothing for it, `assemble` trims the named clip, the frame-zero check
      compares against the right frame, and the ledger shows the saving. A punch-in (crop to a
      closer size from the same clip, at most 1.5x) is decided with numbers from one pilot
      scene, not assumed.
- [ ] A shot without lines has a stated length (`data.seconds` or similar) and passes lint, or
      the decision not to support it is written into `docs/videos/DRAMA.md`.
- [ ] `motionMove` reads the move from `camera` only, treats locked as no move, and anchors its
      patterns.
- [ ] `docs/videos/DRAMA.md` and the skill's `drama.md` describe the new fields; the craft
      spec's paragraph on what the tools cannot do yet is updated, and the check script stops
      flagging what has become possible (`lines.empty`).

## Steps

- [ ] Lower the median warning and reword it (constant, test, the sentence in `drama.md`).
- [ ] Move the check's pure functions where both `lint` and the skill script can import them,
      or have `lint` import the skill script; keep `tools/drama-craft-check.test.mjs` green.
- [ ] Bring `prompts.mjs` in line (drama writer, series episode writer, both verifiers) and
      add the craft rows to `scriptVerdict`.
- [ ] Design the clip-reuse and silent-shot fields with the frame-zero and hash rules, then
      implement them.
- [ ] Fix `motionMove`.

## How to verify

`npm run test:tools`; `node tools/video/cli.mjs lint` on
`tools/video/core/fixtures/drama/video.json` and on a script written to the craft spec (no
median warning between 2 and 3 seconds, craft rows printed); a dry run of `clips` on a scene
with a reused setup shows fewer paid seconds than shots.

## Notes

- `tools/video/core/drama.mjs`, `lint.mjs`, `schema.mjs` and `prompts.mjs` are bound by the
  duration receipt (`docs/videos/long-form/review.json`); changing them needs an independent
  duration-only increment in the same pull request.
- PR #1166 also edits `drama.mjs` (`pictureVarietyProblems` for illustrated slides) and
  `assemble/drama.mjs`; land after it or rebase onto it.
- Open question for whoever designs the fields: an insert that shows only a hand. Listing the
  character brings the right sleeve and ring from the sheet, but the judge's identity question
  needs a face. The skill does not rule on it yet.
- What the measurements do not cover is listed at the end of the craft spec: sound, retention
  curves and movement inside a shot were not measured, so do not turn those into lint rules.
- If production moves to a subscription video tool whose unlimited models cost nothing per
  clip, item 4's saving matters less and the pace target can move toward the references; the
  import path for clips made outside the pipeline is planned separately.
