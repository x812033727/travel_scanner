---
id: 2026-10-02-ten-drama-audio-handoff-audit
title: Preserve drama voice acceptance and future localization sources
status: done
priority: P1
area: tools
owner: codex-ten-drama-handoff
claimed_at: 2026-10-02T13:50:03Z
created_at: 2026-10-02T13:49:15Z
completed_at: 2026-10-02T14:56:22Z
branch: codex/ten-drama-audio-handoff-20261002
depends_on: []
scope:
  - tools/video/core/audio-evidence.mjs
  - tools/video/core/audio-evidence.test.mjs
  - tools/video/core/approvals.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/fixtures/load.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/narration-locale.test.mjs
  - tools/video/qa/qa.test.mjs
  - tools/video/qa/duration.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/package/cli.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
  - tools/video/assemble/synthetic.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/package/variants.test.mjs
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - tools/video/production/retention.mjs
  - tools/video/production/retention.test.mjs
  - docs/videos/series-plans/binge-five-20260928/city-owes-a-light/production-design.json
  - docs/videos/series-plans/binge-five-20260928/city-owes-a-light/production-review.md
  - docs/videos/series-plans/claude-binge-five-20260928/reload-first-day/production-design.json
  - docs/videos/series-plans/claude-binge-five-20260928/reload-first-day/production-review.md
  - docs/videos/series-plans/production-20261002-handoff-review
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/youtube-video/references/animation-production.md
  - .claude/skills/youtube-video/references/animation-production.md
  - docs/videos/AUTOMATION.md
---

# Preserve drama voice acceptance and future localization sources

## Why

An independent offline reproduction shows an equal-duration retake changes the
actual narration but leaves timeline.json and its audio approval unchanged.
Chinese-first productions also risk losing later localization sources to tidy
when the current website language selection is empty. Source review found three
wrong or ambiguous speaker/recording clues in City E13 and Reload E23/E25.

## Definition of done

- [x] Bind voice acceptance and downstream readiness to actual take and mix hashes.
- [x] Reject missing or changed audio evidence without buying replacement media.
- [x] Correct three source-bound sound cues and synchronize only fresh pending revisions.
- [x] Preserve Chinese-first production assets needed for planned later language delivery.
- [x] Independently review the changes and record honest audio/localization limits.

## Steps

- [x] Check ten source/design and runtime voice handoffs.
- [x] Fix confirmed defects and test with local mock speech only.
- [x] Run source/design/tools checks and independently renew affected duration bindings.
- [x] Verify live preconditions, preserve history, and submit a draft PR.

## How to verify

Mock two different WAVs with identical duration: retaking an original or its
audio_ref repeat must invalidate old listening approval. Tampering or deleting
any bound WAV must stop downstream work. Source, director and backend bodies
must match without changing story hashes, approvals or generation settings.

## Notes

- This follows the user's continuing instruction to check and fix confirmed
  defects, and the earlier authorization for independent-branch backend repairs.
- Base origin/main 129c07729 includes the already merged PR #1122. No competing
  open PR was returned by the fresh GitHub check. Other worktrees are preserved.
- Narrow scopes overlap the stale earlier claims from this same chat and the
  stale video-worker claim. --force applies only to this follow-up claim; no
  other task, branch or owner claim is released or closed.
- No paid synthesis, generation, approval, upload or publication is performed.
- Author audio/automation integration: 267 passed, zero failures/skips, with
  deterministic local WAVs and mock speech. Independent reviewers checked the
  final full-SHA cache delta and kept every original duration boundary assertion.
- Backend readback: City/Reload latest v4 review, eight other works v3 review;
  all 180 historical rows retained and 12 new review rows matched the normal
  admin serializer. Both read-only replays were unchanged. The updater changed
  only its two expected updated_at timestamps; no decisions, settings or media.
- Fresh collision check also found no overlap with open PRs #1130/#1131. Main
  advanced to acb935fb4 through unrelated branding work; this draft preserves its
  tested runtime base rather than editing that other task's changes.
- Independent LF publication-byte continuation renewed six line-ending-only
  duration bindings. The eleven substantive updates and 59 original bindings
  retain their semantic review; both original receipt archives are untouched.
- Full tools initial run: 1,248 passed, seven old fixture failures, three skips
  out of 1,258 cases. The two affected fixture files then passed all 22 cases;
  every original assertion remained. Combined distinct coverage is 1,255 passes
  and three skips, with no unresolved failure; this is not a second full run.
- Root verified all 95 duration/independent bindings against both actual files
  and staged Git bytes. Source hashes are unchanged; mirrored skill refs are LF.
- Submitted draft PR https://github.com/x812033727/travel_scanner/pull/1132 on
  codex/ten-drama-audio-handoff-20261002. GitHub reports it mergeable but behind
  unrelated main changes; checks are pending. This completed audit does not
  authorize or claim merge, runtime deployment or real media acceptance.
