---
id: 2026-10-17-narrative-panel-rejects-evidence-quoted-with
title: Narrative panel rejects evidence quoted with its timestamp
status: done
priority: P2
area: tools
owner: claude-opus-5-5-narrative-fix
claimed_at: 2026-10-17T02:17:31Z
created_at: 2026-10-17T02:16:17Z
completed_at: 2026-10-17T02:20:21Z
branch: claude/narrative-panel-timestamp-evidence
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
---

# Narrative panel rejects evidence quoted with its timestamp

## Why

The storytelling blind panel (`tools/video/core/narrative.mjs`) is sent the script with every
spoken line printed as `[<line id> <mm:ss>] sentence` (`narrationText`), and each "yes" must quote
a line by its id. `panelVerdict` only recognised a bare `[id]`, so a reader that copied a line
exactly as it was shown, with its start time, was ruled "no line id quoted". On 2026-10-17 the
production host's story-adapt-seiko-quartz-astron round 9 had all 13 answers quote
`[48m5 00:00] 1969 年 12 月 25 日…` and the whole video stalled for a reason unrelated to its script.

## Definition of done

- [x] Evidence quoted as `[id]`, `[id mm:ss]` or `[id h:mm:ss]` counts as a cited line.
- [x] Any other text after the id inside the brackets (`[a1 很好]`, `[是 整支片]`) still does not.

## Steps

- [x] Widen `EVIDENCE_LINE_ID` to an optional ` (h:)mm:ss` after the id, matching `formatClock`.
- [x] Add pass and fail cases beside the "A chapter name carries no line id" cases.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs
```

## Notes

- `formatClock` prints `mm:ss`, or `h:mm:ss` from one hour; the pattern accepts exactly that
  shape (`(?:\d+:)?\d{2}:\d{2}`) and nothing else, so `[a1 1:2]` and `[a1 12:34 很好]` are refused.
- Claimed with `--force`: the scope overlapped `2026-10-14-ai-and-tech-videos-tell-one`, whose PR
  #1504 merged on 2026-10-14 but whose task file was never closed. That file is outside this
  task's scope and was left as it is.
