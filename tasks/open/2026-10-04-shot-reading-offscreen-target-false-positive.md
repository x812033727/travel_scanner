---
id: 2026-10-04-shot-reading-offscreen-target-false-positive
title: Avoid offscreen target co-mention false positives in shot reading
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-animation-preproduction
claimed_at: 2026-10-04T14:40:09Z
created_at: 2026-10-04T04:03:32Z
completed_at:
branch: claude/hailuoai-kling-animation-optimize-208bc1
depends_on: []
scope:
  - .agents/skills/animation-camera/scripts/shot_reading.mjs
  - tools/animation-camera.test.mjs
---

# Avoid offscreen target co-mention false positives in shot reading

## Why

The shot-reading offscreen heuristic treats every named character in a clause
containing `off screen` as the offscreen subject. For a correctly visible actor
whose action targets an offscreen opponent, this can tell the author to delete
the visible actor from `characters`, breaking the keyframe binding.

An independent forward-use review reproduced this with a medium close-up:
`One cyan arc leaves Yan's sword toward Wei off screen right.` Yan is visible and
must remain in `characters`; Wei is the offscreen target. Splitting the sentence
into a visible-actor clause and an explicit offscreen-target clause avoids the
current false positive, but the original sentence is semantically valid.

## Definition of done

- [x] A visible actor aiming at a named offscreen target does not receive `cast.offscreen` or advice to remove the visible actor.
- [x] Truly offscreen characters still receive the existing useful cast-binding diagnostic.
- [x] Regression coverage includes the co-mention example, an explicit offscreen subject and an ambiguous clause.

## Steps

- [x] Inspect the name/offscreen co-mention heuristic and distinguish actor from target where the wording supports it.
- [x] Keep ambiguous clauses reviewable; do not solve this by disabling offscreen checks.
- [x] Add regression cases and update any diagnostic guidance that could remove a correctly visible character.

## How to verify

Run `node --test tools/animation-camera.test.mjs` under Node 24.19. Run
`shot_reading.mjs --strict` on a temporary three-shot pilot using the example
above and confirm that the visible actor remains bound. Also exercise a true
offscreen speaker to show the guard still works.

## Notes

- Found on 2026-10-04 in the independent Budaimiao-style skill trial; the relevant heuristic is in `shot_reading.mjs` around lines 218-226.
- The current documentation warns against deleting a visible actor merely to clear this heuristic. Runtime behavior is unchanged by the skill-only task.
- No paid media, browser operations or runtime fix were performed for this discovery.
- Fixed 2026-10-04 in the animation-preproduction branch: `offScreenSubjects()` reads who
  the off-screen phrase is about. The name the phrase is attached to (right before it, or joined
  by a verb such as speaks or waits) is the off-screen one. A name before a look or pointing verb
  ("Yan looks off screen at Wei") stays bound, and the name after the phrase is the off-screen
  one. A name cut off from the phrase by toward, at or into ("leaves Yan's sword toward ...") is
  the actor and stays bound. A clause that names nobody falls back to the speakers, and an unclear clause is
  reported as a question whose fix keeps the visible actor in `characters`. "watches" and
  "listens" no longer bridge a name to off screen. `--route server|hailuo|kling` was added so
  the `source.bought` advice only appears on the server route.
