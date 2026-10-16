---
id: 2026-10-16-align-story-writer-and-listener-guidance
title: Align story writer and listener guidance with narrative panel semantics
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-16T03:35:05Z
completed_at:
branch:
depends_on:
  - 2026-10-15-clarify-narrative-review-rules-for-adjacent
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/story-prompts.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/automation/register.test.mjs
---

# Align story writer and listener guidance with narrative panel semantics

## Why

PR #1517 clarifies the blind narrative panel: an immediately adjacent answer does not need a
named callback; a distant callback does; a product history may follow one concrete use problem
across historical participants; and the origin may return to an earlier point after a cold-open
preview. The brand-story writer still receives `NARRATIVE_RULES` from
`tools/video/automation/register.mjs` through `story-prompts.mjs`. That text says to pick one
protagonist present in the opening and close, make every new scene enter through that protagonist,
and explicitly name every payoff. The story writer also requires every next chapter to say what
"happened next" and tells it to name loops with 「還記得那…」. The listener is told to make the first
line lead on from the previous chapter. These can pull A01's hook → 1928 origin transition and
adjacent answer back toward the wording that the clarified panel was meant to assess fairly.
This is a prompt alignment issue, not evidence that A01's genuine round 9 FAIL changed.

## Definition of done

- [ ] Brand-story writer and listener instructions agree with the current `chapters_link`,
  `payoffs`, and `one_thread` panel questions, including the cold-open → earlier origin seam,
  adjacent answers, distant callbacks, and a sourced product-use thread across participants.
- [ ] Missing answers, unrelated same-category example montages, and unsupported historical
  causation still fail. Preserve the other narrated-video rules or assess their impact explicitly
  before changing shared `NARRATIVE_RULES`.
- [ ] Prompt tests cover the actual composed `writer:story` and `listener:story` instructions;
  hash/prompt changes are recorded, and old receipts are never reinterpreted as new PASS.

## Steps

- [ ] Check task/worktree/PR ownership for the scoped files; the older
  `2026-10-14-ai-and-tech-videos-tell-one` task still says in-progress but its PR #1504 was
  previously merged, so recheck current state rather than force claiming from this note.
- [ ] Compare the composed writer/listener text with the final #1517 panel questions and the
  approved A01 source-bound candidate. Choose a story-specific override or a carefully scoped
  shared-rule correction; update tests for the chosen contract.
- [ ] Run focused prompt/narrative tests and task validation; separately re-review A01's actual
  script through the real panel only after authorized deployment and a source/hash-bound edit.

## How to verify

Run `node --test tools/video/automation/story.test.mjs
tools/video/automation/register.test.mjs tools/video/core/narrative.test.mjs` with this worktree's
dependencies, then `npm run check:tasks`. Inspect the actual composed stage instructions and
compare prompt hashes. Test both allowed cases and explicit counterexamples; a fixture test is
not a real model verdict.

## Notes

Filed as a separate follow-up while #1517 remains draft, no-auto-merge. No writer/listener
prompt, A01 host artifact, review receipt, paid stage, or production state was changed by filing
this task. Current A01 round 9 panel remains FAIL on `chapters_link`, `payoffs`, and `one_thread`.
