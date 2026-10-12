---
id: 2026-10-12-complete-curio-h03-english-japanese-korean
title: Complete Curio H03 English Japanese Korean languages
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-h03-languages
claimed_at: 2026-10-12T05:23:05Z
created_at: 2026-10-12T05:22:27Z
completed_at:
branch: codex/curio-h03-en-ja-ko-20261012
depends_on: []
scope:
  - docs/videos/curio-h03/i18n
  - docs/videos/curio-h03/language-upload.md
  - docs/videos/curio-h03/video.json
---

# Complete Curio H03 English Japanese Korean languages

## Why

The owner requested English, Japanese and Korean CC and dubbed audio for the existing Tunguska episode, continuing the three-language supplementation workflow. The persisted choice includes metadata, captions and dub for all three on video b98IdS1MB78.

## Definition of done

- [x] Source-bound translations and independent reviews cover all 139 lines and seven chapters in each locale.
- [x] Three dubbed tracks fit the approved 694.3-second cut and pass the native audio and package checks.
- [x] The obsolete Traditional-Chinese-only sentence is removed from the description, with a new native publish confirmation for that metadata change and a language batch bound to the same approved final.
- [x] EN/JA/KO audio, CC and metadata are uploaded to the existing video and Studio shows Published; original visibility is retained.
- [x] Final evidence distinguishes automated QA, actual Studio status, exact readback, and playback/listening limits.

## Steps

- [x] Inventory fixed production handoff, original approvals, live owner choice and absence of another active H03 producer.
- [x] Create an isolated worktree at PR 1456 head; preserve stale untracked 3a3c source files.
- [x] Translate and independently review all three locales; preserve source hashes and unchanged metadata through native merge.
- [x] Finish targeted retakes and obtain current configured full audio checks for all three locales.
- [x] Generate final native captions/package and verify the approved language manifest through the native consumer.
- [x] Complete YouTube sync for four metadata locales, EN/JA/KO CC and thumbnail with private visibility; retain existing Traditional Chinese CC.
- [x] Confirm final audio Published rows and six exact Studio caption/metadata captures.
- [x] Save final local/backend/Studio delivery evidence and explicit verification limits.
- [ ] Open a draft PR and complete the repository task handoff.

## How to verify

Use bundled Node 24.19 with tools/video/cli.mjs and work base C:/Users/x8120/mokaair-work/videos. Preserve stage exits, request journals, native review IDs, source-bound manifests and consumer readback. Verify Studio rows and exact uploaded caption/metadata texts; do not infer player listening or publication from automated checks.

## Evidence and boundaries

- Original production: completed PR 1456 commit 2c921b1be0381c4a003bc7fadd08b1952f273346. Final SHA-256 e786669f5a392fde7f281c617c28f885d25df8b13535b4a37f9e2ae6eaea304e; original TC caption SHA-256 4cf72b2f0d02fe8ff88ff777cc8777e2d2a3f4864ea742949a699fde6e521c59, both preserved.
- The only source change removes the obsolete youtube.description sentence. Current source SHA-256 e73f4c2de44b178c391c59a9c9c603823b5b34f175a55313f8995c04ac765def; speech, visuals, cut and final bytes are unchanged. Refreshed publish approval is now consumer-bound.
- External audit: C:/Users/x8120/mokaair-work/video-language-curio-h03. Native work: C:/Users/x8120/mokaair-work/videos/curio-h03. Current translation/review/media hashes and approval details are in [language-upload.md](../../docs/videos/curio-h03/language-upload.md).

## Notes

Delivery completed: local/backend PASS at 08:02:18.655Z, private YouTube sync at 16:02 Asia/Taipei, exact Studio text PASS at 08:13:23.952Z and all nine Published components observed at 08:13:32.505Z. Only draft PR/task handoff remains:

- All three configured formal checks pass 139/139 lines, zero flags/unchecked lines. Each current M4A is 694.3 seconds, AAC48k stereo and fully decodes with exit 0/empty stderr. Native fit replay has 137 windows per locale and zero overruns; 500 media input pins are stable.
- Native caption counts are EN 139, JA 147 and KO 145, each covering all 139 source IDs in order. Recomputed SRT bytes match packaged copies with no native/readability/overlap defects. Native package passes 4/4 items.
- Approved publish review c367dccd-74a4-4723-aa1f-609d45402a6e has content SHA-256 935f56ea391e9d39ed062d2db7460c945d5eec44e9e7dc3b1f70f0b1b058fbfe. Approved language review 376730d3-8a8b-4155-be40-55903354fe4c has manifest SHA-256 c1764ab94fb295a3c561a78dcdd348b610d5232f337ec4f2c09ed6e4cc2d6b95, decided_at 2026-10-12T08:00:26.077356+00:00. Saved evidence does not identify the approver; the UI already-decided rejection is not a fresh approval or a Studio success receipt.
- approved-delivery-20261012T080112779Z.stdout.json SHA-256 07662ba3c414cea5b619844ba5a3a336a6225af6056e6c2b7e919d33c26cb1e9 and matching receipt establish actual exit 0, 3,361 passing checks/546 stable aggregate pins, 11 verified attachments and native read_approved_package(verify_files=True) acceptance with four CC/three dubs. Remote transaction was read-only and rolled back; no provider call or canonical mutation.
- youtube-sync-complete.json (captured 08:02:50.458Z, SHA-256 59ed9aca385bb7d2bd9154918b5a96319f65ea00f17cd61aea0e96c19a476a40) reports sync complete at 16:02 Asia/Taipei: four metadata locales, EN/JA/KO CC uploaded, existing zh-TW CC retained, thumbnail set and private visibility. The reviewed form's Chinese description exactly equals approved metadata and omits the old TC-only sentence (youtube-sync-reviewed-form.json SHA-256 e19ced25697ef6c6e16fb84bb2c2f1b06939a697d3947a138a1c497e324f1d01).
- studio-final-all-published.json SHA-256 4b3818f9329e6ef6e1c0d47f7179ee345ff56147ded48f39e56c72a7ab0b6623 and studio-final-published.png SHA-256 a92426469d09c864c1a2a6eb442c7153196a9d203ab91d7c77e8e60677073de3 directly show EN/JA/KO audio, CC and title/description all Published on b98IdS1MB78. Language publication does not make the private video public.
- studio-captioned-exact-readback-20261012T081323507Z.stdout.json SHA-256 f5414eb334774b53719a013ad8d3a0f0f0dcc09c7d288afe1495d0de357bfef1 passes 70 guards for six saved captures: 431 exact raw CC texts, three unchanged descriptions and three titles matching the pinned live-native caption-label policy. Matching receipt SHA-256 e8aa8458eb4b7df1aca7c41a4b60cd5586b85a41f7113bbe49569526598842f2 records actual exit 0/empty stderr. Spaces, line breaks and order remain exact; the AX-only LF mapping does not relax raw comparison.
- No full player playback, human listening, full Studio timing or downloaded Studio SRT byte comparison was performed. Local native timing/source coverage and actual Studio publication have separate evidence. Keep this task in progress pending the draft PR; do not move/close it in this documentation update.
- Confirmed-answer Windows recoveries and bounded JA/KO 502 resolutions are preserved in audit receipts. They do not establish a platform fix or provider billing outcome; no check verdict was manually edited. Inspect current receipts before any further production action.
