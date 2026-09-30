---
id: 2026-09-30-read-a-model-answer-s-first
title: Read a model answer's first complete JSON object
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-30T01:12:52Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
---

# Read a model answer's first complete JSON object

## Why

On 2026-09-30 01:05Z google-vids-omni-free-quota's ja caption reviewer answered 27,780 characters
that `parseAnswer` (tools/video/automation/prompts.mjs) could not read: "Unexpected
non-whitespace character after JSON at position 16172". The whole answer parses only if it is
one JSON value; the fallback slices from the first `{` to the last `}`, which fails as soon as a
second object, a stray bracket or a sentence with braces follows the first object. The stage
counts a failure and runs again next round (about 35,000 tokens each time), and after
MAX_STAGE_FAILURES in a row the video is blocked. The answer is kept in the worker's
`/var/lib/mokaair/video-work/google-vids-omni-free-quota/answers/caption-reviewer-2026-09-30T01-05-45-644Z.txt`.

## Definition of done

- [ ] `parseAnswer` returns the first complete top-level JSON object in the answer (a string-
      and escape-aware brace scan), fenced or not, with any text before or after it ignored.
- [ ] An answer with no complete object still throws the same SyntaxError.
- [ ] Tests: two objects back to back, a trailing sentence with `}` in it, braces inside strings,
      and the answer above (or a cut of it) if it turns out to be one of those.

## Steps

- [ ] Read the kept answer around character 16172 to see what the model actually did.
- [ ] Write the scan and its tests.

## How to verify

`node --test tools/video/automation/prompts.test.mjs tools/video/automation/automation.test.mjs`.

## Notes

- Filed at the owner's request on 2026-09-30 while `2026-09-28-sothatswhy-shorts-from-episode`
  still listed prompts.mjs in its scope (its PRs #904, #950, #962 have merged).
