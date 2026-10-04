---
id: 2026-10-04-anime-silent-action-guidance
title: Align anime silent action guidance with long-anime-v1 policy
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-04T04:06:45Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/references/drama.md
---

# Align anime silent action guidance with long-anime-v1 policy

## Why

The main drama reference still says anime-category silent `action_seconds` is
unsupported. Current schema and `long-anime-v1` production policy support
validated silent action beats under their policy conditions. An author following
the older reference while preparing an existing anime episode could remove a
valid beat or incorrectly change category to work around the advice.

## Definition of done

- [ ] The drama reference describes the actual ordinary-short-drama and valid long-anime-v1 silent-action conditions.
- [ ] Unsupported categories/policies remain clearly distinguished, with links to the current schema/policy authority.
- [ ] The YouTube skill entrypoint hashes and existing independent-review receipt remain unchanged.

## Steps

- [ ] Compare `drama.md` silent-action guidance with `tools/video/core/schema.mjs` and `tools/video/core/anime-policy.mjs`.
- [ ] Correct the reference-only wording without changing runtime behavior or encouraging category/profile removal.
- [ ] Validate existing policy examples and skill links; preserve both YouTube SKILL.md entrypoints.

## How to verify

Run the relevant schema/anime-policy tests under Node 24.19 and
`node --test tools/skills.test.mjs`. Read the corrected reference against a
valid long-anime-v1 silent-action scene and an unsupported-category scene.
Compare both YouTube SKILL.md files with origin/main and the bound receipt.

## Notes

- Found on 2026-10-04 by independent forward use of the optional animation style. The old statement is at `drama.md` around line 95.
- The new animation-camera notes already point to the effective schema/policy. This task corrects the older prerequisite reference separately.
- Do not weaken the external-clip rejection for `series.production.profile`; that is a different production-contract limitation.
