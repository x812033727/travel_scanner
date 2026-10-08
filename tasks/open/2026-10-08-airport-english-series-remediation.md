---
id: 2026-10-08-airport-english-series-remediation
title: Rebuild airport English series through channel production and review gates
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T11:54:44Z
completed_at:
branch:
depends_on:
  - 2026-10-08-airport-english-series-pr
scope:
  - docs/videos/airport-english-60-days/production
  - tools/video/airport_english
---

# Rebuild airport English series through channel production and review gates

## Why

The 60-day airport listening prototype was delivered as complete after basic
decode/duration checks. The full audit found all masters below channel video
specification, all audio below channel format/loudness, incorrect quiz replay
selection, oversized CC lines, player state bugs and missing formal review gates.
See `docs/videos/airport-english-60-days/AUDIT.md` and its evidence. This task is
the unfinished production work; completion of the audit task does not close it.

## Definition of done

- [ ] All 60 episodes satisfy an explicit English-teaching profile and channel
      quality requirements, with every remaining exception stated and evidenced.
- [ ] Every quiz replay supports its answer; each selected language's CC is
      readable and timed to its actual speech, with English dialogue preserved.
- [ ] Current audio/final/package hashes have genuine required QA/review evidence.
- [ ] Preview episode switching and audio failures are correct; no unsupported
      offline/YouTube availability claim is made.

## Steps

- [ ] Create official per-episode brief, video.json, claims and independent reviews;
      preserve the historical source-snapshot unchanged.
- [ ] Keep 60 days, final 600 seconds, always-visible English/default English,
      four selected translated CC/coaching voices and English character dialogue.
      Choose English voice style explicitly; don't inherit Mandarin narration.
- [ ] Replace heuristic quiz selection with explicit dialogue-turn IDs and review
      all questions, including the separately produced Day01.
- [ ] Verify applicable travel/safety advice with dated official sources; label
      fictional practice flight numbers, gates and examples accurately.
- [ ] Rewrite episode-specific hooks/outros, shorten individual static states,
      improve quiz typography and retain purposeful listening/response practice.
- [ ] Produce a compliant Day01 using official server voice/TTS dry-run,
      check-audio and current review workflow, then apply the validated workflow
      to the remaining episodes. Never invent approvals or expose credentials.
- [ ] Render 1080p30, CRF18, 2 B frames, 2-second closed GOP, BT.709 and faststart;
      encode AAC-LC48k stereo at384k target with two-pass -14LUFS/-1dBTP loudnorm.
- [ ] Apply actual installed branding within the authorized 600-second total;
      regenerate synchronized CC/audio/chapter offsets and preserve media hashes.
- [ ] Segment per locale using repository caption rules and measured speech timing;
      review line widths, word boundaries, reading-speed warnings and mobile safety.
- [ ] Rebuild JPEG thumbnails using channel layout, prepare English/TC metadata,
      per-episode hooks/audience/tags and owner upload-decision fields; record
      selection scope for any additional localized metadata.
- [ ] Fix offline player cue accumulation, failed-audio routing, speed persistence,
      accessible episode label and mobile CC controls; add meaningful regressions.
- [ ] Verify direct-file launch only in an allowed environment; otherwise ship and
      document a supported local HTTP launch rather than claim untested double-click.
- [ ] Re-run all-media format/loudness/hash checks and full content/caption review,
      formal 11-item final QA and 4-item package QA. Review current hashes only.
- [ ] Supersede old bundles and completion claims only with validated replacements;
      provide a usable preview and clearly identify remaining limitations.

## How to verify

Follow `.agents/skills/youtube-video/references/automated.md` for the current
`lint`, `tts --dry-run`, `check-audio`, render/assemble/captions, `qa`, package and
review commands. Keep approvals/media in VIDEO_WORKDIR outside the public repo.
Measure every final MP4/M4A, verify all selected CC with core/captions.mjs, review
all replay IDs against actual rendered sequences, and test player switch/error
paths. Run applicable AGENTS.md checks for any code changes. Audit data and its
rule baseline are preserved under the series `evidence/` directory.

## Notes

- No production rebuild has happened in the audit PR; all checkboxes remain open.
- Do not port Edge TTS, the fixed A/B heuristic, stale PID polling or hard-coded
  `/workspace` prototype paths into a new production tool.
- Day01 used a separate generator; its old encode.py targets earlier translated
  burned-in variants, not the final YouTube master. Source preservation is not a
  claim of a complete reproducible final encoder.
- The custom preview is not proof of YouTube multi-language-audio eligibility.
  User has not requested upload/publication; keep it outside this task.
- Original 600-second timing/hash/decode checks still hold. Closed GOP structure,
  true peak and faststart passed; don't fix imaginary failures.
- A user instruction to produce the series already authorizes ordinary work.
  Do not re-ask for languages or invent an approval gate for reversible preparation;
  use actual configured automatic reviews, and disclose any real unmet gate.
