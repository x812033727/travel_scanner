---
id: 2026-09-30-let-the-compilation-planner-judge-thumbnails
title: Let the compilation planner judge thumbnails instead of re-ranking scores
status: done
priority: P3
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-01T03:15:00Z
created_at: 2026-09-30T09:40:07Z
completed_at: 2026-10-01T03:16:36Z
branch: claude/audit-followups
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

- [x] Both texts say the candidates come best-judged first and ask for the picture that best
  carries the headline's promise.

## Steps

- [x] Wait for #1030 (compilation spoilers), which rewrites the same prompt block, then rebase.
- [x] Edit both texts; keep the output shape unchanged.

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

## Notes

Found by the 2026-09-30 prompt audit (medium confidence, Group 4).

Done 2026-10-01 after #1030 merged. Claimed with `--force`: `2026-09-28-sothatswhy-shorts-from-episode`
holds `prompts.mjs`, but its claim is more than 24 hours old, its branch is gone from origin and its
PRs (#904, #950, #962) are merged. The output shape is unchanged; `compilation.mjs` still falls back
to `candidates[0]`.
