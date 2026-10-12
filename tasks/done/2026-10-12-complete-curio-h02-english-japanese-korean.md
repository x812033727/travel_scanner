---
id: 2026-10-12-complete-curio-h02-english-japanese-korean
title: Complete Curio H02 English Japanese Korean captions and dubs
status: done
priority: P2
area: docs
owner: codex-gpt6-h02-languages-3a3c
claimed_at: 2026-10-12T00:54:04Z
created_at: 2026-10-12T00:53:04Z
completed_at: 2026-10-12T04:40:18Z
branch: codex/curio-h02-en-ja-ko-20261012
depends_on: []
scope:
  - docs/videos/curio-h02/i18n
  - docs/videos/curio-h02/language-delivery.md
---

# Complete Curio H02 English Japanese Korean captions and dubs

## Why

The owner requested missing English, Japanese and Korean CC and audio for H02, YouTube video `6hswTvAftUA`. The backend selects metadata, captions and dubs for exactly those languages. The approved 680.5-second Traditional Chinese source remains unchanged.

## Definition of done

- [x] All 134 lines and selected metadata in en/ja/ko pass independent semantic review.
- [x] Three current dub tracks fit the original cut and pass formal audio checks; any remaining defect is explicitly recorded.
- [x] Matching CC, audio and source-bound language manifests are delivered, with backend attachments read back and Studio upload status accurately distinguished.

## Steps

- [x] Verify video identity, original media hashes and ownership; claim isolated H02 language scope.
- [x] Copy the current backend language decision, generate worksheets, translate and independently review.
- [x] Dry-run budgets, synthesize, resolve fit and audio flags, generate matching CC.
- [x] Package and submit the language batch, verify consumer files and record remaining owner actions.

## How to verify

Use native `i18n-sheet`, `i18n-merge`, `dub --dry-run`, `dub`, `check-audio --locale`, `captions`, `package` and `review-push --gate languages`. Verify source/media hashes, measured fit, native caption bytes and upload copies, backend attachment/consumer hashes and actual Studio state. Final content tests already pass; local QA is separate from Studio publication and playback acceptance.

## Current outcome

All three dubs pass formal 134/134 checking with zero flags, and all final audio/caption readbacks pass. Native captions produced TC 134 / EN 134 / JA 138 / KO 142 cues; package exited 0. Fresh Studio reload at `04:38:18.309Z` confirms all three audio tracks, CC tracks and metadata translations published. The approved language package passes read-only verification of all 11 attachments, the five unchanged original files and native consumer output. Requested supplement delivery is complete.

The original video was uploaded privately. No public visibility, full player/listening verification or owner playback acceptance is claimed. Full final hashes and evidence links are in [language-delivery.md](../../docs/videos/curio-h02/language-delivery.md).

## Evidence and scope

- Branch starts from `codex/curio-h02-production-20261012` (draft PR #1453). H03 in a18a, its inherited untracked files and the separate bb7a pilot-language task remain outside scope. Initial local/host checks found no competing H02 production lease.
- Frozen final SHA `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`; source timeline SHA `4c9de49bf9536d6d645b6aa3cd40a7301a809bd1149365223910922cbb8ff4c3`; TC SRT SHA `c8d49f959b2c898384a25f8fa0dc47251805e27b421e212df432c42d5aa22112`. Original final review `a3f6b386-f6ec-41ce-a5e2-9ded114a605b` and publish review `fb4ff837-1f5b-4a32-8f7e-baa27a251f9d` remain the binding source.
- Independent text review covers 134 lines, seven chapters and selected metadata per language. Audio fixes also passed independent semantic review and exact canonical readback. JA used two wording rounds (34 then eight lines) and two same-text single-line retakes. KO used 20 lines/543 characters, then three lines/102 characters and two same-text 37-character retakes. Final KO canonical SHA `2841b584e6508134080d247b5e4b70d5fda70932c7995319e46eff91c4793675`; dictionaries/thresholds unchanged.
- Final formal check receipts: EN `01:50:21.986Z`; JA `03:35:21.992Z`; KO `04:23:19.556Z`, all exit 0. KO final breakdown is 108 exact + 12 Jev + 14 second-transcript passes. Latest KO retake `dub-2026-10-12T04-20-32-926Z` exited 0. Audit `dub-final-readback.json` and `captions-final-readback.json` both PASS with current media, raw-clip, source and translation bindings.
- Failed EN M4A and JA MP3 deletions/replacements were explicitly owner-authorized and fulfilled. JA WAV reused 120 requests with zero synthesis, SHA `7422c5778eaab2d6fc8fda5fd01babb3917e107bb5eaf87c48c4fe0122d1f906`. Final publication evidence is `studio-three-languages-published.json/.jpg`; all nine components are published. EN 134/134, JA 138/138 and KO 142/142 Studio caption DOM texts match. Full server timing/downloaded-file/playback checks are not claimed.
- Language review `db892505-45d9-401a-8c94-408c54ef9927` is approved with manifest SHA `d3721be9c03d4af1e1a51201beead27b729d72e11d2434473ea43ce1e7a873b3`. Audit `language-store-approved-readback.json` at `04:38:47.949657Z` reports `APPROVED_CONSUMER_PASS`: 11 language files, five original files and native `read_approved_package(verify_files=True)` pass, including mixed MP3/WAV and all four caption locales. `review-pull` at `04:38:45.919Z` exited 0 and recorded the language batch. Historical audio/publish-version warnings did not invalidate the pinned source-bound consumer; no old review resubmission or full YouTube synchronization was triggered.
- `final-dub-decode-readback.json` reports strict decoding PASS for the exact three upload tracks, with all 439 source/clip/input hashes unchanged. Proof SHA `4aebf13d664879504035b9343c5c9ca409d743d5591738d4532cfb52882a722a`; no paid/network calls or canonical writes.
- Confirmed journal responses, including KO transcription `440b10d6` at `04:05:11.047Z`, were recovered with zero paid/network calls and native reuse before/after. Audit `prepared-recovery-*/run-*/receipt.json` preserves evidence. The [Windows journal repair task](../open/2026-10-09-windows-speech-journal-rename-failures.md) remains separate.
- `ko-pure-retake1-502-evidence.md/.json` records a failure consistent with status preflight, with no persistent unknown request attributable to that failed stage observed; provider billing is not independently reconciled. Subsequent successful retakes have separate receipts. The [redo dry-run estimate task](../open/2026-10-12-dub-redo-dry-run-budget-estimates.md) remains open; dry-run zero is not actual retake accounting.
- Final checks: 199/199 docs-video tests, zero failed/skipped, exit 0; task check validated 1,854 files, exit 0, only unrelated existing stale-claim warnings. Logs: `docs-video-tests-final.log`, `task-check-final.log`.
- Media: `C:/Users/x8120/mokaair-work/videos/curio-h02`. Private audit/receipts: `C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA`. No media or recovery backups belong in Git.
