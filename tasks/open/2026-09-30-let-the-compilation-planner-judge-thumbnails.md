---
id: 2026-09-30-let-the-compilation-planner-judge-thumbnails
title: Let the compilation planner judge thumbnails instead of re-ranking scores
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-30T09:40:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - .agents/skills/youtube-video/references/prompts/planner-compilation.md
---

# Let the compilation planner judge thumbnails instead of re-ranking scores

## Why

The compilation planner prompt (`tools/video/automation/prompts.mjs`, the compilation block, and
`.agents/skills/youtube-video/references/prompts/planner-compilation.md`) tells the model to pick
"the candidate with a character's face and the highest judge score". `compilation.mjs`
`thumbnailCandidates` already keeps only shots with a character and sorts them by judge score,
so the instruction's answer is always `candidates[0]`, which is also the code's fallback. The model
is doing a lookup and not the judgment it is there for: which picture carries the headline.

## Definition of done

- [ ] Both texts say the candidates come best-judged first and ask for the picture that best
  carries the headline's promise.

## Steps

- [ ] Wait for #1030 (compilation spoilers), which rewrites the same prompt block, then rebase.
- [ ] Edit both texts; keep the output shape unchanged.

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

## Notes

Found by the 2026-09-30 prompt audit (medium confidence, Group 4).
