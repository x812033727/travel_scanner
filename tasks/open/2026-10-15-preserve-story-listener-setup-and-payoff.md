---
id: 2026-10-15-preserve-story-listener-setup-and-payoff
title: Preserve story listener setup and payoff context
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-15T18:38:20Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story-prompts.mjs
  - tools/video/automation/story.test.mjs
---

# Preserve story listener setup and payoff context

## Why

The A01 story listener twice removed a previously reviewed explicit long-distance callback from line `83ew` (dropping the opening reference), and its latest idea pass removed the opening-pitch reference from `j9sw`. The subsequent genuine narrative panel still failed. The listener sees one chapter and short neighboring context, not the full setup/payoff map. The supplied house-style document already requires callbacks, but the short LISTENER instruction emphasizes trimming repeated phrases and only explicitly protects facts, figures, years, names and attribution. Numeric/Latin/lexicon rewrite guards cannot identify this narrative regression.

## Definition of done

- [ ] A chapter listener receives the actual relevant cross-chapter setup/payoff context and preserves earned callbacks while retaining freedom to improve wording and remove genuine adjacent repetition.
- [ ] Request hashing and durable journals bind the added context; a changed request cannot reuse an old result or discard a pending request.
- [ ] Tests cover the observed regression and ordinary edits without granting any narrative or pilot PASS from a structural check.

## Steps

- [ ] Check current production/source state and task/worktree ownership before changing the shared story producer.
- [ ] Use current chapter loop metadata to give the listener concise, accurate context; keep original fact/attribution and output constraints.
- [ ] Add focused request/rewrite regression coverage. Document that final narrative review still judges the actual resulting full script.

## How to verify

Run the focused story automation tests and inspect one captured request: the intended setup and payoff IDs/text must be present, current and part of the normalized request hash. A model's returned wording remains subject to actual whole-film narrative and independent pilot review; an instruction alone is not proof that the regression is fixed.

## Notes

Evidence: A01 stopped snapshot `actual-20261016-022930`, archive SHA `9ce10e09123f1c22174d6552929e0232e62efd3b31da89e592c7e7c4699a28f9`, 57 continuous audits. Actual source `b343e84a33b2933854377b8f50c57f33dfa99ba191e7dfe0b35fd87c9f14422d`; genuine narrative round 7 remains FAIL. Relevant deployed source: `story-prompts.mjs` LISTENER, `story.mjs` listener payload, and `core/rewrite.mjs` guards. This task does not authorize deployment, media, reinterpreting the failed panel, resetting counters or resubmitting an unchanged panel. A narrowly reviewed operational request appendix, if used for A01, must preserve its original instructions and record the real new request/audit rather than modifying historical responses.
