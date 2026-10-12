---
id: 2026-10-11-produce-curio-h03-tunguska-traditional-chinese
title: Produce Curio H03 Tunguska Traditional Chinese episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h03
claimed_at: 2026-10-11T23:02:28Z
created_at: 2026-10-11T23:02:26Z
completed_at:
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
- [ ] Current, source-bound outline, audio and storyboard decisions are recorded; no inherited H02 approvals are reused.
- [ ] Narration and finished video each meet the eight-minute minimum; generated images and contact sheets have been inspected.
- [ ] Traditional Chinese CC, thumbnail, metadata, source list and upload package pass applicable checks; current backend decisions and hashes are read back.
- [ ] Delivery records distinguish automated checks, owner review, upload and publication; no YouTube upload or publication is performed.

## Steps

- [x] Check shared work, remote branches and open PRs; claim the episode-only scope.
- [x] Refresh primary research, write three outline choices and submit the outline.
- [x] Write and independently verify the script, including listener review.
- [x] Run dry-runs, synthesize/check narration, create and inspect illustrated shots.
- [ ] Render, assemble, produce zh-TW CC, run QA and prepare the upload package.
- [ ] Persist delivery evidence and open a draft PR for the episode documents.

## How to verify

Use the bundled Node runtime with `tools/video/cli.mjs`, slug `curio-h03`, and workdir base `C:/Users/x8120/mokaair-work/videos`. Record native lint, dry-run, stage exit receipts, review-pull results, media durations, content hashes and package checks. Inspect rendered media rather than treating a launched process or judge score as final acceptance.

## Notes

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
- Render exit 0: 56 states, no layout errors, 376 seconds. Final source documentation tests: 199 passed, 0 failed; task check: 1,849 valid files with unrelated stale-claim warnings. Assembly is in progress; final video/QA/owner acceptance are not yet complete.
