---
id: 2026-11-19-opening-300s-independent-review
title: Strict first-300-seconds review by three independent readers before any voice
status: done
priority: P1
area: tools
owner: claude-opus-elegant-hypatia
claimed_at: 2026-11-19T02:55:32Z
created_at: 2026-11-19T03:00:00Z
completed_at: 2026-11-19T02:55:33Z
branch: claude/elegant-hypatia-07i3yx
depends_on: []
scope:
  - tools/video/core/opening-review.mjs
  - tools/video/core/opening-review.test.mjs
  - tools/video/cli.mjs
  - tools/video/tts/cli.mjs
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - .agents/skills/youtube-video/references/script-writing.md
  - docs/videos/lessons/sothatswhy.md
  - docs/videos/lessons/curio.md
  - tools/video/automation/flow.mjs
  - tools/video/automation/opening-gate.test.mjs
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - docs/videos/BRANDING.md
  - docs/videos/STORY.md
  - docs/videos/so-thats-why/README.md
  - .agents/skills/youtube-video/references/automated.md
  - .agents/skills/curio-episode/references/w03-lessons.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Strict first-300-seconds review by three independent readers before any voice

## Why

Owner 2026-11-19: 「應該要前300秒都不會滑走比較好，嚴格審核」「多一點獨立代理來看」. The new opening
rules were only warnings, and hand-made 原來如此 / 奇聞 / brand-story episodes never pass the script
gate (they go straight to storyboard and final), so nothing held a weak opening before paid voice.

## Definition of done

- [x] `opening-review --slug S` writes the packet (thumbnail, title, first 300 s timed); `--record F --author A`
      records three readers' verdicts bound to the script.
- [x] Pass only when three distinct readers (not the author), one per persona (newcomer, scroller,
      stickler), each score >= 8.5, would stay 300 s, swipe_at null and problems empty; any edit invalidates.
- [x] `tts` refuses a hand-made episode of the three series until it passes (not a dry run, not a host
      worker video with auto.json, not a cut with a final approval).
- [x] Skills, the sothatswhy template, script-writing.md and lessons describe the step.

- [x] After an independent review: the record binds to `openingHash` (title, thumbnail headline,
      lines under 300 s with speaker names) and every reader echoes it; edits after 300 s, a `say`
      fix and retakes (`--redo`, `--refresh-evidence`) or a voice already made for this script are
      not asked again; the old "any final approval" exemption is gone (a recut in the same workdir is
      gated); `problems` must be a list; names compare without case or spaces; the packet shows
      character names (所長, 小問), not ids.

- [x] Owner 2026-11-19 「都修一修吧」: the readers are asked by the tool itself (`opening-review --ask`,
      three verifier requests on the site's model, variant `opening-review`), each verdict records
      `via: "site"` and the model, and the gate takes no verdict typed in by hand (`--record` removed).
      `tts --dry-run` and `opening-review --check` show where the review stands. Residual: the record
      is still a local file, so a deliberate hand edit could forge `via`; the site keeps each prompt.

- [x] Owner 2026-11-19 「用每個跑的AI?」: both sources count. By default the AI making the episode
      asks three fresh subagents and records them with `--record F --author A` (via "session"; no site
      quota; the author is never a reader); `--ask` stays for the site's model (via "site").
- [x] End-to-end review fixes: the host's script gate sends a bad opening back to the writer
      (`fixScript(..., "opening")`) instead of parking on the review-push refusal; `--ask` binds the
      hash itself, keeps answers when a later request fails, reads 無/空字串 as no swipe, 8,000 output
      tokens; `--redo` on a never-voiced script is still gated; the hash ignores pauses; the ten-step
      series need 2 opening loops, not 3; the 原來如此 prompt uses one opening range (40–90 s) and
      maps the ten steps to a why-question; stale docs marked.

## How to verify

```bash
node --test tools/video/core/opening-review.test.mjs && npm run test:tools
```
