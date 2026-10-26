---
id: 2026-10-25-complete-eight-selected-language-packages-for
title: Complete eight selected language packages for OpenAI DNS containment video
status: blocked
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

- [x] en, ja, ko, es, pt, id, vi and th each have current metadata, CC, checked dubbing and localized thumbnails delivered through final/publish and verified by backend stored-file readback.
- [ ] The formal native languages batch is bound to a genuinely approved source final review and submitted successfully; generic final/publish file delivery alone does not satisfy this batch requirement.
- [x] The reusable AI/tech skill records eight foreign languages plus the zh-TW original as the default; both existing skill mirrors match.
- [x] Original QA failures, narration facts and source attribution remain intact; no unperformed YouTube upload is claimed.

## Steps

- [x] Read the owner's saved selection from the backend; retain its actual decision timestamp.
- [x] Translate and independently review all eight languages against the final source and timing budgets.
- [x] Synthesize, fit and check each dub serially; all eight current tracks have actual 80/80 checks (640 lines), with affected takes repaired and prior failures retained.
- [x] Rebuild nine-language CC and the full package, send updated final/publish files, and verify remote sizes/hashes and eight downloadable M4A evidence aliases.
- [ ] Send the formal languages batch after genuine source-final approval; the actual native attempt returned exit 3 while remote final remained pending.
- [x] Record final per-language measurements, localized thumbnail checks, standing eight-language preference and remaining QA warnings.
- [ ] Finish the task in the existing review PR only after the formal batch has a successful native submission and backend readback.

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
- The media-production chain ran serially, with en/ja/pt/id/th/ko/es in the recorded chain; historical native exit codes remain in external language-media-chain.json. No ASR flag was manually cleared.
- Final local verification at 2026-10-25T16:10:53.139Z records all eight ready, each 80/80 checked, 500.6 s, -14.0 LUFS (th -14.1), decoded true peak -2.8/-2.9 dBTP; full hashes remain in language-delivery-verification.json.
- Backend readback at 2026-10-25T16:44:51.430Z matches eight final dub files and eight evidence_{locale}_m4a aliases, nine CC/description files, metadata, eight localized thumbnails and the unchanged original final. The generic final review's original-evidence area provides the eight M4A downloads. This is stored-blob/project readback, not an unperformed admin-only binary download.
- BLOCKED: the task's formal batch requirement remains incomplete. Remote final and publish are pending, all eight language components remain working, and native review-push --gate languages actually stopped with exit 3. Do not forge approval, mark the formal batch submitted, or close the task from file delivery alone.
- An existing bounded watcher runs 2026-10-25T16:44:44.829Z to 2026-10-26T16:44:44.829Z, every 300 s; latest recorded check 16:49:47.685Z still waits for genuine source approval. It only reads while waiting, verifies unchanged source/package/choices/media after real approval, then attempts one normal native languages push. It makes no review decision and stops on changed/rejected inputs or the deadline.
- Latest native QA stays 10/11: policy demo 0.48 is below 0.6; the earlier zh-TW 0.46 remains historical. Captions pass with 35 speed advisories (es 5, pt 1, id 4, vi 25), not zero warnings. Later localized-thumbnail checks all pass; earlier QA thumbnail warnings remain in their original receipt.
- Full delivery and outstanding dependency are documented in docs/videos/openai-dns-containment/languages-result.md. Original final SHA256 remains 32dc8fc9e7de880011ab257dc3e774ddf23e4203dc1138a6d1f1bac88ca50dd6; YouTube video ID remains null. This task has no completed_at until the formal batch requirement is satisfied.
- Public PR evidence is docs/videos/openai-dns-containment/delivery-verification.json: eight checked tracks, 47 stored-file roles, eight thumbnail checks, download aliases, genuine pending source approval, QA 10/11 and 35 caption-speed advisories. Reviewers do not need private scratch access for these delivery facts.

- New-rule qualification remains incomplete: local `branding.json` is absent and checks have no official bookend binding; the shared package is missing. Preserve the delivered files and pending reviews. Recover canonical assets and follow native version protections before any timeline replacement; no arbitrary bookends or blind paid retries. Cross-project asset recovery is recorded as `2026-10-25-local-first-build-without-branding`.
