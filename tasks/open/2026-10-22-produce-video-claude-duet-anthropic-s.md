---
id: 2026-10-22-produce-video-claude-duet-anthropic-s
title: Produce video: Claude Duet, Anthropic's proactive agent that calls you first (claude-duet-proactive-agent)
status: blocked
priority: P2
area: docs
owner: claude-fable-5-1-news-video
claimed_at: 2026-10-22T17:13:12Z
created_at: 2026-10-22T17:12:37Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-duet-proactive-agent
---

# Produce video: Claude Duet, Anthropic's proactive agent that calls you first (claude-duet-proactive-agent)

## Why

The owner asked on 2026-10-23 for a second AI/tech current-events video from the hot topics of the day (after ai-shopping-agents-blocked). Picked Anthropic's Claude Duet (announced 2026-10-21, research preview, US Pro/Max waitlist): the official announcement and product page carry a full demo (Maya, the Marlo café chain) and three quoted testers, enough for one protagonist and 8+ minutes. Illustrated storytelling route, category ai-news, site article ai-news-claude-duet-20261022 (auto-news, DB only, so it goes in sources, not source_guide).

## Definition of done

- [ ] `docs/videos/claude-duet-proactive-agent/` holds brief.md, video.json, claims.md, verify-*.md and shorts.json; lint has zero errors and the storytelling panel passes (or its misses are fixed and recorded).
- [ ] Outline approved (owner said 2026-10-23: take the recommended option), narration, storyboard, final and publish gates pushed to /admin/videos (hand-pushed: every gate waits for the owner).
- [ ] final.mp4, captions and the upload package exist in the local workdir and qa passes 11/11.

## Steps

- [x] Sources fetched into the workdir (_tools/sources), brief.md written with 3 outlines (A recommended).
- [x] Writer: video.json + claims.md + shorts.json + lexicon terms, lint clean.
- [x] Verifier rounds 1–2 (10 + 3 fact edits), listener pass, three blind reads (63 → 70 → 72; misses fixed afterwards, no fourth read).
- [x] tts (8:39 on the first synthesis), pace, check-audio twice (5 → 3 flagged, all reworded), review-push audio (pending the owner; re-pushed after the rewording).
- [x] keyframes (round 1: 42 shots, 5 needing review; round 2 with simpler prompts: all passed, nothing to accept-best), storyboard pushed (pending), render, assemble (8:36 + branding), captions, review-push final: qa 8/11 — narration unapproved (owner), pace (thumb-approve 8.8 s; fixed by the rewording round that followed), policy (Jev 符合立場 0.47, 業配 0.24: the owner decides at the final gate).
- [x] Rewording round (iuiv, tiyx, 2cae shortened under 8 s; tv2w reworded): check-audio 0 flagged, audio re-pushed, assemble (8:27 body), final re-pushed: qa 9/11 — narration unapproved (owner) and policy (Jev 符合立場 0.53, 業配 0.22) are the owner's call at the final gate.
- [ ] package, review-push publish: blocked until the owner approves the final cut on /admin/videos.
- [ ] package, review-push publish; note what the owner still has to do.

## How to verify

`node tools/video/cli.mjs status --slug claude-duet-proactive-agent`; `lint` zero errors; `qa` writes review/qa.json with all 11 passing; the cards appear on /admin/videos.

## Notes

- The outro state must be split for qa pace (answer and comment question each on a shot, the outro keeps the subscribe line only).
- Same pitfalls as the sister ticket 2026-10-22-produce-video-ai-shopping-agents-blocked (source_guide, lexicon scope, panel evidence format, pace after tts). Both videos share the lexicon (append only) and the same local tool token.
- 2026-10-23 owner: 「之前我有修改過規則，這個應該要用新規則做」 → remake under the 2026-10-21 rules (teaching-flow §十 one-concept short, §十二 picture rules, PAPER.md paper look; model = `claude-md-house-rules`). brief.md gained a 「新規則版」 section (outline re-approved locally on the owner's standing word); the illustrated video.json is kept at `<workdir>/_tools/v1-illustrated/video.json`; the 53/47 keyframes stay in the workdir but are unused. Facts and claim ids are reused; narration, cards and pictures are rewritten (no `shot`), then tts, render, assemble, qa and the three gates are redone.
- Paper remake done 2026-10-23: 47 scenes / 66 states, no shots, one screencast of the product page (also the thumbnail), verify rounds 3–4 (9 + 0 fact edits), narration 7:45 body (final with branding over 8:00), check-audio 0 flagged after one rewording, qa 9/11 (narration unapproved; policy 符合立場 0.57／有示範 0.46), audio and final gates re-pushed. The illustrated version is kept at `_tools/v1-illustrated/video.json`.

