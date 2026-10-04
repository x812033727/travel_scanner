---
id: 2026-10-04-anime-silent-action-guidance
title: Align anime silent action guidance with long-anime-v1 policy
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-drama-docs-truth
claimed_at: 2026-10-04T14:51:06Z
created_at: 2026-10-04T04:06:45Z
completed_at:
branch: claude/drama-docs-say-what-code-does
depends_on: []
scope:
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - .agents/skills/youtube-video/references/drama-craft.md
  - docs/videos/DRAMA.md
---

# Align anime silent action guidance with long-anime-v1 policy

## Why

The main drama reference still says anime-category silent `action_seconds` is
unsupported. Current schema and `long-anime-v1` production policy support
validated silent action beats under their policy conditions. An author following
the older reference while preparing an existing anime episode could remove a
valid beat or incorrectly change category to work around the advice.

## Definition of done

- [x] The drama reference describes the actual ordinary-short-drama and valid long-anime-v1 silent-action conditions.
- [x] Unsupported categories/policies remain clearly distinguished, with links to the current schema/policy authority.
- [x] The YouTube skill entrypoint hashes and existing independent-review receipt remain unchanged.

## Steps

- [x] Compare `drama.md` silent-action guidance with `tools/video/core/schema.mjs` and `tools/video/core/anime-policy.mjs`.
- [x] Correct the reference-only wording without changing runtime behavior or encouraging category/profile removal.
- [x] Validate existing policy examples and skill links; preserve both YouTube SKILL.md entrypoints.

## How to verify

Run the relevant schema/anime-policy tests under Node 24.19 and
`node --test tools/skills.test.mjs`. Read the corrected reference against a
valid long-anime-v1 silent-action scene and an unsupported-category scene.
Compare both YouTube SKILL.md files with origin/main and the bound receipt.

## Notes

- Found on 2026-10-04 by independent forward use of the optional animation style. The old statement is at `drama.md` around line 95.
- The new animation-camera notes already point to the effective schema/policy. This task corrects the older prerequisite reference separately.
- Do not weaken the external-clip rejection for `series.production.profile`; that is a different production-contract limitation.
- 2026-10-04, claude-opus-5-5-drama-docs-truth. Claimed with `--force`: the overlap was
  `2026-10-03-illustrated-slides-round-2-a-family` (status review, scope
  `.agents/skills/youtube-video/references`), whose work landed on origin/main as #1172; its
  open steps (receipt rebind, post-deploy look) do not touch this file.
- What the code does (`tools/video/core/schema.mjs` `validateScenes`): a scene with
  `action_seconds` is accepted when `validAnime || timesSilentShots(doc)`; `validAnime` is
  `isLongAnime(doc) && validateAnimePolicy(doc).length === 0` (`anime-policy.mjs`), and
  `timesSilentShots` (`drama.mjs`) is a cast, no length floor, not a knowledge long-form and
  `category !== "anime"`. The scene must be `template: "shot"` with non-empty `data.prompt` and
  `data.motion`, `lines: []` and an integer 1–8; `timeline.mjs` refuses the same at timing.
  `drama.md` now says this, names what is refused (narrated, knowledge long-forms with the
  480 s floor, `category: "anime"` without a valid policy), links
  `docs/videos/LONG-ANIME-PRODUCTION.md`, and says not to change `category` or drop
  `production_policy`/`series.production.profile` to get a beat through. The `clips import`
  refusal for a profile (line 85) is unchanged.
- The same old sentence was in `drama-craft.md` §四 and in `DRAMA.md` (the 鏡頭場景 row and
  「沒有人說話的鏡頭」); corrected here too, so those two files are added to scope (both are also
  in the sibling ticket `2026-10-03-drama-design-documents-say-what-the`, same PR).
- `.claude/skills/youtube-video/references/drama.md` was not byte-identical before this change:
  #1174 updated line 93 (the `accent.mjs` voice note) in `.agents` only. The copy is now
  `cp` of the canonical file, so it also picks up that line. `tools/skills.test.mjs` compares
  only SKILL.md, so nothing caught it.
- One more stale cell fixed while in the file: the still-move table said `drift` drifts
  "slightly right"; since #1166 the direction alternates by shot id (`driftDirection`,
  `tools/video/assemble/drama.mjs`).
- Read against real validation (a scratch script calling `validateVideo` on the fixtures):
  ordinary cast drama accepted; valid long-anime-v1 accepted; short `category: "anime"` drama
  without a policy refused (`action_seconds` and `lines`); long-anime-v1 with `lead: male`
  refused (policy error plus `action_seconds`); narrated drama refused.
- Checks (Node v24.13.0 on this machine, not 24.19): `node --test tools/video/core/schema.test.mjs
  tools/video/core/anime-policy.test.mjs tools/video/core/drama.test.mjs
  tools/video/core/timeline.test.mjs tools/video/core/screenplay.test.mjs` 67/67;
  `node --test tools/skills.test.mjs` 6/6; both `youtube-video/SKILL.md` have no diff against
  origin/main and hash `e64e9588…` as in `docs/videos/long-form/review.json`;
  `node tools/video/long-form/cli.mjs check` PASS.
