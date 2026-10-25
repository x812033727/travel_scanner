---
id: 2026-10-25-complete-eight-selected-language-packages-for
title: Complete eight selected language packages for OpenAI DNS containment video
status: in-progress
priority: P2
area: docs
owner: codex-ai-tech-news
claimed_at: 2026-10-25T11:28:48Z
created_at: 2026-10-25T11:28:38Z
completed_at:
branch: codex/ai-tech-dns-20261025
depends_on: []
scope:
  - docs/videos/openai-dns-containment
  - .agents/skills/ai-tech-news-video
  - .claude/skills/ai-tech-news-video
---

# Complete eight selected language packages for OpenAI DNS containment video

## Why

The owner saved all eight foreign languages in the backend and now expects all
eight in future AI/tech video deliveries. The already delivered zh-TW episode
needs the selected metadata, CC and dubbing, with actual checks and a complete
language batch sent to the backend.

## Definition of done

- [ ] en, ja, ko, es, pt, id, vi and th each have current metadata, CC and checked dubbing delivered to the backend.
- [ ] The reusable AI/tech skill records eight foreign languages plus the zh-TW original as the default.
- [ ] Original QA failures, narration facts and source attribution remain intact; no unperformed YouTube upload is claimed.

## Steps

- [x] Read the owner's saved selection from the backend; retain its actual decision timestamp.
- [x] Translate and independently review all eight languages against the final source and timing budgets.
- [ ] Synthesize, fit and check each dub serially; correct only affected takes and report any unresolved exception.
- [ ] Rebuild CC and the full upload package, send the languages batch and updated package, then verify remote files.
- [ ] Record final measurements and standing eight-language preference; finish the task in the existing review PR.

## How to verify

Native `i18n-merge`, `dub`, `check-audio --locale`, `captions`, `package` and
`review-push --gate languages`, followed by backend readback. Run shared skill
mirror tests, native lint and task checks before pushing the documentation.

## Notes

- Backend readback at 2026-10-25T11:28:25Z confirms all three parts true for all eight locales; owner saved at 2026-10-25T11:26:16.864834Z.
- These are eight foreign language tracks in addition to the zh-TW original (nine audio/caption languages total), not eight replacement videos.
- Do not rerun the already passed zh-TW render/assembly/TTS. The original overall QA 10/11 and delegated adoption remain recorded.
- Media stays outside the public repo in /workspace/work/videos/openai-dns-containment. Native dubbing and audio checking share the project lease and must run serially.
- All eight translations have 80 current lines and 7 chapters. Independent review corrections were merged and exact deltas checked before audio; reports remain under the external work directory's i18n folder.
- VI's first track fits all 78 windows at 1x and measures 500.6 s, -14 LUFS, -2.8 dBFS decoded peak. Its first check flags 11 lines; the secondary transcriber initially failed on PyAV 19.0.2's removed metadata_errors parameter. Private runtime pinned to PyAV 16.1.0 for actual clip validation; no failed secondary run counts as evidence.
- Formal remaining-language chain is serialized, starts en/ja/pt/id/th/ko/es, and records every native exit code in the external language-media-chain.json. No ASR flag is manually cleared.
