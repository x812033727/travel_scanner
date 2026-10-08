---
id: 2026-10-08-airport-english-series-remediation
title: Rebuild airport English series through channel production and review gates
status: blocked
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T11:54:44Z
completed_at:
branch: codex/airport-english-series-pr-20261008
depends_on:
  - 2026-10-08-airport-english-series-pr
scope:
  - docs/videos/airport-english-60-days/production
  - tools/video/airport_english
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/stages.mjs
  - tools/video/core/stages.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

- [x] Create official per-episode brief, video.json, claims and independent reviews;
      preserve the historical source-snapshot unchanged.
- [x] Keep 60 days, final 600 seconds, always-visible English/default English,
      four selected translated CC/coaching voices and English character dialogue.
      Choose English voice style explicitly; don't inherit Mandarin narration.
- [x] Replace heuristic quiz selection with explicit dialogue-turn IDs and review
      all questions, including the separately produced Day01.
- [x] Verify applicable travel/safety advice with dated official sources; label
      fictional practice flight numbers, gates and examples accurately.
- [x] Rewrite episode-specific hooks/outros, shorten individual static states,
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
- [x] Fix offline player cue accumulation, failed-audio routing, speed persistence,
      accessible episode label and mobile CC controls; add meaningful regressions.
- [x] Verify direct-file launch only in an allowed environment; otherwise ship and
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

- Remediation began on 2026-10-08 following the user's explicit instruction to
  finish all 60 episodes. The original audit remains unchanged.
- Current preparation: all 60 five-language lesson sources independently reviewed;
  all 180 quiz evidence sets explicit and checked. Three safety statements fixed.
  Official lint has zero errors; warnings remain visible (57 duration estimates,
  16 fictional-example source notices and 3,540 pairwise quote-template matches).
  Above checked items describe the source/profile and player fixes, not final
  media acceptance. Estimated body lengths are 538.57–623.40 seconds.
- Static preflight: 21 longest/representative current cards rendered with official
  renderer; no overflow, at most three rows, minimum fitting font 60px. All 5,112
  prepared scene states estimate at most 15 seconds. Neither result is a measured
  full-video check. The earlier 95-state Day01 render is superseded preflight only.
- Preview module/browser regressions use old prototype media solely as fixtures.
  Local HTTP launch is supported; file:// is explicitly unsupported. No new full
  series preview or replacement ZIP has been certified.
- Runtime workspace: /workspace/airport_production/{project,media}; no real
  synthesis yet. This environment needs official login pairing, and actual
  installed branding assets are absent locally. Do not copy credentials into
  this task, chat or Git. The latest discovered historical channel record is the
  v2 CC package activation; verify the actual current pin before making media.
- All 60 current source sets now have verify-1.md and review-binding.json backed
  by genuine independent reports; 720 prepared artifacts were independently
  checked. A pre-TTS guard rejects stale repository or staged evidence. All 60
  thumbnail layouts passed after shortening Day12/46 headlines (metadata only).
- Mixed teaching audio and delivery tools have their own explicit manifests and
  require checked original English takes, current source/final hashes, real
  measured media and the official main-package checks. Combined review remains
  pending; these tools never manufacture generic dub or production approvals.
- Next: finish one full five-language Day01, including real translated-speech
  window fitting and purposeful pacing adjustments, before batching 59 episodes.
  Use cached checked takes during retiming; do not hide a language that cannot fit
  or consume the learner's four-second answer pause. Keep intermediates bounded
  after actual per-episode disk measurements; preserve legacy deliverables.
- Saved in draft PR #1389. Checks: test:tools 2,223 pass / 3 skip / 0 fail;
  test:docs-videos 199 pass; final airport regressions 48 pass; check:tasks passes.
  Official Day01 dry-run passed through current source/staged review guards:
  45 synthesis requests, about 2,217 billable characters and 50 exact-take replays.
  It reported no token. No paid synthesis, final QA approval or real new package
  was produced. Resume from PRODUCTION_STATUS.json after pairing and obtaining
  actual current branding assets; the old pairing codes must not be reused.
- Scope extended to core/drama.mjs and its tests after collision checks found no
  active task or open PR touching either implementation scope: slides need the
  existing safe audio_ref replay support, with identical-content/voice validation.
- tools/video/tts/check.mjs is touched by another open PR (#1387); do not compete
  with that work while planning mixed-language coaching/source-audio verification.
- Scope extended to core/stages.mjs and its tests after a collision check found
  no active task or open PR: readLanguages was discarding the selected zh-TW dub
  even for an English source. Preserve that choice and filter the actual source
  language when collecting alternate audio for upload.
- The mandatory long-form duration receipt binds drama.mjs, drama.test.mjs and
  stages.test.mjs. An independent duration-only increment must review those three
  changes and refresh only their bindings, preserving historical review prose.
  Collision check: no active claim; PR #1387 also updates this shared receipt for
  different implementation files. This isolated branch will append its own
  evidence and keep that future receipt merge explicit; it does not modify or
  supersede #1387's implementation/review work.
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
