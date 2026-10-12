---
id: 2026-10-11-produce-curio-h03-tunguska-traditional-chinese
title: Produce Curio H03 Tunguska Traditional Chinese episode
status: done
priority: P2
area: docs
owner: codex-gpt6-curio-h03
claimed_at: 2026-10-12T04:02:08Z
created_at: 2026-10-11T23:02:26Z
completed_at: 2026-10-12T04:33:05Z
branch: codex/curio-h03-production-20261012
depends_on: []
scope:
  - docs/videos/curio-h03
---

# Produce Curio H03 Tunguska Traditional Chinese episode

## Why

Continue 奇聞檔案局 after the approved H02 delivery with the next checked topic, H03 Tunguska. Explain why a blast flattened roughly 2,000 square kilometres of forest without a confirmed main impact crater, while distinguishing observations, models and unresolved details. The owner requested the next episode and explicitly selected Traditional Chinese only on 2026-10-12 (Asia/Taipei).

## Definition of done

- [x] A source-checked brief and independently reviewed Traditional Chinese script answer one central question and pass native lint.
- [x] Current, source-bound outline, audio and storyboard decisions are recorded; no inherited H02 approvals are reused.
- [x] Narration and finished video each meet the eight-minute minimum; generated images and contact sheets have been inspected.
- [x] Traditional Chinese CC, thumbnail, metadata, source list and upload package pass applicable checks; current backend decisions and hashes are read back.
- [x] Delivery records distinguish automated checks, owner review, upload and publication; no YouTube upload or publication is performed.

## Steps

- [x] Check shared work, remote branches and open PRs; claim the episode-only scope.
- [x] Refresh primary research, write three outline choices and submit the outline.
- [x] Write and independently verify the script, including listener review.
- [x] Run dry-runs, synthesize/check narration, create and inspect illustrated shots.
- [x] Render, assemble, produce zh-TW CC, run QA and submit the final for owner review.
- [x] After owner storyboard/final approval, record the existing zh-TW-only choice and prepare/check the upload package.
- [x] Persist delivery evidence and open a draft PR for the episode documents.

## How to verify

Use the bundled Node runtime with `tools/video/cli.mjs`, slug `curio-h03`, and workdir base `C:/Users/x8120/mokaair-work/videos`. Record native lint, dry-run, stage exit receipts, review-pull results, media durations, content hashes and package checks. Inspect rendered media rather than treating a launched process or judge score as final acceptance.

## Notes

The following notes are chronological snapshots; the final entries and PRODUCTION.md describe the current state.

- Base: freshly fetched `origin/main` at `6b5370b6f`; no H03 production documents, media, branch or open PR existed at claim time. Existing topic-bank and pilot work is outside this scope.
- External media and receipts: `C:/Users/x8120/mokaair-work/videos/curio-h03`; binary media must remain outside git.
- Language: zh-TW narration, metadata and CC only. Owner wording:「繼續製作奇聞檔案局下一支影片，一樣只出繁體中文。」No language reconfirmation is needed.
- Research refresh must account for the 2025 critique of the 80-million-tree estimate, possible surviving fragments, differing airburst models and continuing Lake Cheko disagreement; do not repeat older dossier conclusions as settled facts.
- Existing H02 production and unrelated `.codex/environments/` are preserved.
- Outline A approved by the owner; backend review `8c9554c5-ceb3-48b7-ab66-fd713e681f45` read back approved at `2026-10-11T23:08:38.855460Z`. Brief SHA `98e2a3a28c529714bef64d4c42bd76aca5e08ab1cb9318df5c897d7f8cb0bdfc` is frozen.
- Draft: 115 scenes, 82 illustrated shots, two licensed original photos, 139 narration lines. Independent fact and listener reviews run before synthesis. Native preflight confirms Sulafat ready; image-01 estimated US$1.11 for one take each, US$3.32 for three each, under effective US$80 cap.
- Final source SHA `08b8fc80c9b9720ee30cf1ccf73f8f0d540a03e8b3ec6ef77166dde43237dca2`; first full fact review, second independent check and listener review passed. Native lint: 0 errors, 3 prompt-frequency warnings retained for visual inspection. `_audit/preproduction-manifest.json` seals the files and approved outline. Final TTS dry-run: 139 requests, 2,735 billable characters; synthesis started with native request journaling.
- Narration completed: 139 checked lines, zero outstanding flags; two bounded retakes, 137 WAVs unchanged. Body 686.3 seconds; cadence longest 7.9 seconds, zero problems. Audio review `4d67cd87-0db6-49b4-ade2-60b1b2b12cc8` approved and read back. One Windows journal EPERM was recovered from the exact confirmed record with zero resend; existing platform task tracks that issue.
- Three-image pilot is usable after actual-image review and narrow repairs. Bulk generation continues with independent visual checks; snow/night drift in three June scenes was rejected despite judge passing and locally repaired. Current production/revision lineage is in `PRODUCTION.md` and `visual-review.md`; audio hash unchanged. No final video or owner final approval yet.
- Current production: 115 scenes, 81 illustrated shots, two photos and 139 lines; 81/81 selected images have exact-SHA viewing evidence. Five native accept-best pictures retain all original scores/takes and owner review remains pending. Metadata-only final source SHA `c7be5e8032fbf0775976a642bc558f408e1453f0b6b36a688decbfe0e7b8790b`; speech/look/pictures/visual hashes unchanged by that edit.
- Current audio review `d91b4953-eb3f-4329-ae68-5f1dea60c8c0` approved and read back against timeline SHA `d256ebfe5e46cafadf85fc48f136a6c8ef725aafa4a87a5973db39bd9eb6ec12`. Storyboard review `da0651b4-5904-4232-81ec-d71928e3e551` pending; passing ordinary shots retain remarks rejected by the backend predicate. Follow-up is filed as `2026-10-12-reconcile-passing-storyboard-verdicts-with-nonempty`; no scores or approvals were changed.
- Render exit 0: 56 states, no layout errors, 376 seconds; all 56 states visually inspected. Final source documentation tests: 199 passed, 0 failed; task check: 1,849 valid files with unrelated stale-claim warnings.
- Assemble exit 0 at 2026-10-12T03:26:35.756Z: 115 scenes, 20,829 frames / 694.3 seconds, -14 LUFS / -1 dBFS, checks.ok=true. Captions exit 0: 139 zh-TW cues. Final review 385728b4-7bc8-4798-89fb-a5ea16102df8 is pending and binds final SHA e786669f5a392fde7f281c617c28f885d25df8b13535b4a37f9e2ae6eaea304e; GET readback confirmed.
- Draft PR #1456: https://github.com/x812033727/travel_scanner/pull/1456; episode documents and follow-up task committed at cfd313a31. Media and private receipts remain outside git.
- Final QA 10/11: only JPL native HTTP 403 remains; independent official-page read succeeded. Encoding the Commons asset URL parentheses fixed the parser's false 404 without changing media. Current source SHA a7e17af3914bedfbf1327219ef646a59a1625a26ac537914e1ea6d2a509afed6. Shared URL and review-player CC gaps have separate open tasks.
- Independent 139-cue/branding review passed. Official preview playback reached 67.22 seconds; full owner playback/listening is not recorded. The preview has no CC track; local CC server startup was rejected by execution policy, with no alternative startup attempted. Player CC rendering remains NOT_RUN; SRT/VTT files are complete.
- Await H03 owner storyboard/final approval, including five retained images; Traditional Chinese-only authorization already exists and must not be requested again. No upload package, YouTube upload, publication, merge or deployment is complete.
- Final sampling complete: two reviewers actually viewed all 45 start/middle/end frames across 15 scenes, with zero new blockers. Text/credits and selected-picture hashes match; decorative-line crops and narrowed outro whitespace are minor. Native 51 PSNR / 98 motion records and independent ffprobe match the final.
- Owner approval question sent; latest backend readback at 2026-10-12T03:48:18Z still has storyboard and final pending. Release this task while awaiting that decision; resume from the exact final and existing language authorization, without regenerating approved media.

- Owner explicitly approved the current storyboard and 11:34.3 final, including five retained pictures. Both backend reviews were recorded approved; language choice {} was persisted at 2026-10-12T04:03:36.920100Z. No paid/media regeneration occurred.
- Native package and publish review completed; current metadata SHA 3a87c11795acfc0973521593b9930979173dc2a6bfd9d64731f4e81b6fcdc982. Independent package inventory/hash/content review passed. Backend ready_to_upload=true and native read_approved_package(...,verify_files=True) accepted the H03-only package in a READ ONLY transaction. Native languages submission exits 3 because TC-only has no extra language batch; no manifest is required or fabricated.
- The interrupted 193 MB review transfer reused 27 SHA-verified parts and completed the remaining 20 through the existing API, with final full-hash confirmation. Follow-up: 2026-10-12-resume-review-file-transfers-from-server. A language choice change was reverted to the explicitly authorized TC-only setting and reverified; no added-language production persisted.
- Handoff-only corrections: Education (27) display label and unsupported licensed-music wording; shared template follow-up 2026-10-12-derive-video-upload-guide-category-and. Source/media/title/description are unchanged. User approval does not invent full playback/listening/CC evidence. No YouTube upload, publication, PR merge or deployment.
- Production scope is complete; documents remain in draft PR #1456 for owner-controlled merge. Final proof and upload steps are under the existing external H03 directory.
