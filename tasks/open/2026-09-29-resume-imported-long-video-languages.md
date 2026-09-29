---
id: 2026-09-29-resume-imported-long-video-languages
title: Resume selected languages for six imported long videos
status: in-progress
priority: P1
area: tools
owner: codex-imported-languages
claimed_at: 2026-09-29T11:14:08Z
created_at: 2026-09-29T11:13:51Z
completed_at:
branch: codex/imported-long-languages
depends_on: []
scope:
  - docs/videos/imported-long-languages
---

# Resume selected languages for six imported long videos

## Why

Six approved `ai-real-world-*` long videos were imported through `video import`,
which sends a final review but creates no automation project or narration timeline.
The owner selected en/ja/ko metadata, captions and dubs plus zh-CN metadata/captions,
then explicitly asked this chat to continue after PR #964 was merged and deployed.
The standard worker cannot adopt these external cuts automatically.

## Definition of done

- [x] The six local final hashes match the currently approved backend reviews.
- [x] Original source timing is faithfully adapted with provenance that separates
  the original Hanhan narration from the Gemini target dub voice.
- [ ] An isolated, resumable runner makes only the six projects' selected languages,
  preserving the approved cuts and the owner's language and publication choices.
- [ ] Completed metadata/captions and checked dub tracks are submitted cumulatively;
  failures retain actual reasons and partial progress survives a restart.
- [ ] Record real backend review state and remaining work without claiming human
  audio acceptance, Studio upload or publication.

## Steps

- [x] Read the video workflow and inspect competing work; keep Shorts out of scope.
- [x] Read-only preflight verifies all six exact approved hashes and language choices.
- [x] Build and independently check the adapter, runner and focused regression tests.
- [ ] Start the authorized language work and verify persisted progress in the backend.
- [ ] Record the final receipt or the concrete continuation state.

## How to verify

Run the adapter and runner's Node tests, a read-only dry run against the paired
site, and compare the source/final hashes before and after. Verify each cumulative
review's locale payload and attached file hashes by reading the persisted project.
The job must not call the general auto loop, assemble, tidy or youtube-sync.

## Notes

- Preflight at 2026-09-29T11:17:06Z: six final hashes match approved reviews, no
  existing language review, Gemini configured and channel voice Sulafat.
- Source imports: `C:/Users/x8120/mokaair-work/videos/season1-import/`.
  Isolated output: `C:/Users/x8120/mokaair-work/imported-long-languages-20260929/`.
- Episode 01 uses the currently approved original cut. The separately merged
  image-trust opening revision is not substituted into that approval.
- Do not fabricate standard-render checks or previous approvals. Pull actual
  hash-bound approval, preserve external-render provenance, submit language files
  through the existing review API, and leave Studio confirmation to the owner.
- PR #981 owns production acceptance of #964; do not duplicate its task or report.
- Adapter/runner: 22 focused tests passed on bundled Node 24.19.0; task check passed.
  All 554 source SRT cues match the source timing within 0.5 ms. Independent review
  covered approval drift, immutable inputs, complete audio checks and cumulative
  submission preservation.
