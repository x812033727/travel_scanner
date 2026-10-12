# H02 selected language delivery

The English, Japanese and Korean supplements for [H02](https://youtu.be/6hswTvAftUA) are delivered: all three audio tracks, CC tracks and metadata translations are published in Studio. Each dub passes 134/134 formal audio checks with zero flags. Final media, captions and the approved backend package pass independent readback.

The existing video was uploaded privately. Public visibility, complete player/listening verification and owner playback acceptance are not established by these checks.

## Current delivery status

| Component | English | Japanese | Korean |
| --- | --- | --- | --- |
| Formal audio check | PASS, 134/134 | PASS, 134/134 | PASS, 134/134 |
| Current audio | MP3 | PCM WAV | MP3 |
| Local CC | PASS, 134 cues | PASS, 138 cues | PASS, 142 cues |
| Studio audio | Published | Published, PCM WAV | Published |
| Studio CC | Published; 134/134 DOM texts match | Published; 138/138 DOM texts match | Published; 142/142 DOM texts match |
| Studio title/description | Published | Published | Published |

Fresh Studio reload at `2026-10-12T04:38:18.309Z` confirms all nine published components ([DOM and screenshot][studio-published]). Backend language review `db892505-45d9-401a-8c94-408c54ef9927` is approved, bound to manifest SHA `d3721be9c03d4af1e1a51201beead27b729d72e11d2434473ea43ce1e7a873b3`. The [read-only consumer audit][backend-approved] at `04:38:47.949657Z` reports `APPROVED_CONSUMER_PASS`: all 11 language attachments match their bytes/hashes, the original five files remain unchanged, and native `read_approved_package(verify_files=True)` accepts all three dubs and four caption locales.

## Frozen source and final files

The owner selected only en/ja/ko CC and audio; the backend also selects their metadata. The native language writer preserved the original decision timestamp. The approved Traditional Chinese source remains unchanged:

| Source | SHA-256 |
| --- | --- |
| [video.json](video.json) | `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e` |
| 680.500-second final cut | `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6` |
| Source timeline | `4c9de49bf9536d6d645b6aa3cd40a7301a809bd1149365223910922cbb8ff4c3` |
| Traditional Chinese SRT, 134 cues | `c8d49f959b2c898384a25f8fa0dc47251805e27b421e212df432c42d5aa22112` |

Original approved final review: `a3f6b386-f6ec-41ce-a5e2-9ded114a605b`; original approved publish review: `fb4ff837-1f5b-4a32-8f7e-baa27a251f9d`. H03 and the separate pilot-language production remain outside this scope. Initial ownership checks found no competing H02 worker or lease.

All final audio tracks are 680.5 seconds, 48 kHz and two-channel; every measured window fits. Japanese WAV has 32,664,000 PCM sample frames.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `dubs/en.mp3` | 27,222,764 | `a2c8d440f553e81ee339fdc366d5cff464274169391b2fee6a2af9a010524725` |
| `dubs/ja.wav` | 130,656,078 | `7422c5778eaab2d6fc8fda5fd01babb3917e107bb5eaf87c48c4fe0122d1f906` |
| `dubs/ko.mp3` | 27,222,764 | `11df3ff938ba7f13f84562d3f24f06d63499e510924f10dd3617e821cb3ffbc2` |
| `captions/en.srt` | 12,021 | `95e8f4c048f3818d94397c535bf0323553017cda6030d5744f7654bee369a35c` |
| `captions/ja.srt` | 14,608 | `9ae22ae7be03f5f22ed977ee8f6e860f2a57c71d75e9cd4c3a64dc5f2b1807f7` |
| `captions/ko.srt` | 13,808 | `9c35624a046934414b216bbc74e1bba53242d9882347a3fadb421a14caa9a71f` |

Final translation SHAs: en `03b91fd71f093018aef5758d3b43108a5de1f7b5d0fcd4183a903c0749036d8a`; ja `d7b87f08c2af55125c7af4d5cd9db61e35f5cdcf258408f647a6a087bfe723d2`; ko `2841b584e6508134080d247b5e4b70d5fda70932c7995319e46eff91c4793675`.

## Validation and publication evidence

- All 134 narration lines, seven chapters and selected metadata per language passed independent semantic review. Audio fixes also have independent review and exact canonical readback. Japanese rewrites covered 34 then eight lines, followed by two same-text single-line retakes. Korean rewrites covered 20 lines/543 characters then three lines/102 characters, followed by two same-text 37-character retakes. Unchanged lines and metadata were verified; dictionaries and acceptance thresholds were not relaxed. Evidence: workdir `i18n/*.review.md` and audit `ja-audio-fixes-r*.review.md/.readback.json`, `ko-audio-fixes-r*.review.md/.readback.json`.
- Final native formal checks: EN `01:50:21.986Z`, JA `03:35:21.992Z`, KO `04:23:19.556Z`, all exit 0 and 134/134 without flags. JA cleared 100 exact + 28 Jev + six second-transcript lines; KO cleared 108 exact + 12 Jev + 14 second-transcript lines. The latest KO retake `dub-2026-10-12T04-20-32-926Z` exited 0. Full [audio readback][audio-proof] verifies source/translation/voice/fit bindings, every raw clip's checked hash and final media properties for all three languages.
- [Strict full-file decoding][decode-proof] of the three exact upload tracks passed without errors; all 439 source/clip/input hashes match before and after. Proof SHA: `4aebf13d664879504035b9343c5c9ca409d743d5591738d4532cfb52882a722a`. This check made no paid/network calls or canonical writes.
- Native `captions` at `04:23:49.735Z` and `package` at `04:24:14.193Z` exited 0. [Final caption readback][caption-proof] verifies all 134 source IDs per language, exact native text/timing bytes, one 5-second intro, no overlaps or readability warnings and identical package copies. TC remains 134 cues. Earlier provisional JA/KO captions are superseded.
- English's failed M4A and Japanese's failed MP3 were deleted only after explicit owner authorization. Replacement EN MP3 is published. JA WAV reused all 120 synthesis requests with zero new requests/characters; the [Studio main-table readback][ja-published] at `04:25:57.178Z` confirms Japanese audio, CC and metadata published. The failed-upload receipts and replacement receipts remain in the audit directory.
- Studio editor text readbacks match EN 134/134, JA 138/138 and KO 142/142 cues in order (`studio-en-caption-readback.json`, `studio-ja-caption-readback.json`, `studio-ko-caption-readback.json`). The fresh three-language main table confirms all published states. EN's first 12 UI timestamps are within two nominal 30-fps frames. These checks do not establish full Studio timing, downloaded SRT byte equality or successful playback/listening.
- Native `review-pull` at `04:38:45.919Z` exited 0 and recorded the approved language batch after Studio publication. Its older audio/publish-version warnings concern historical approvals; the pinned original publish/final reviews and current source-bound consumer both pass. No old review was resubmitted and no full YouTube synchronization was triggered.
- Final content validation: 199/199 docs-video tests, zero failed/skipped; task check validated 1,854 files. Both exited 0; logs are `docs-video-tests-final.log` and `task-check-final.log`. Only unrelated existing stale-claim warnings remain.

## Recovery evidence and remaining boundaries

Confirmed speech/transcription journal responses were recovered after Windows rename failures without repeating paid requests: native before/after proofs made zero network calls and reused the saved answer. Receipts remain under audit `prepared-recovery-*/run-*/receipt.json` (JA `2fd6dd61`; KO `f8b3918c`, `c7f96412`, `e27465ff`, `644e077b`, `b6dbac6e`, and the [04:05:11 recovery of 440b10d6][recovery-440b]). The general fix remains in the [Windows journal repair task](../../../tasks/open/2026-10-09-windows-speech-journal-rename-failures.md).

The [KO HTTP 502 evidence][ko-502] is consistent with native status preflight failing before synthesis; no persistent unknown request attributable to that failed stage was observed. Provider billing was not independently reconciled. Subsequent actual 37-character retakes have their own successful receipts. The [redo dry-run estimate follow-up](../../../tasks/open/2026-10-12-dub-redo-dry-run-budget-estimates.md) remains open: its zero estimate must not be treated as actual retake cost.

Media and private receipts stay outside Git: media `C:/Users/x8120/mokaair-work/videos/curio-h02`; audit `C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA`. The requested supplements and backend verification are complete. The original video remains private; public publication, complete player/listening verification and owner playback acceptance are outside the evidence established here.

[audio-proof]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/dub-final-readback.json
[caption-proof]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/captions-final-readback.json
[ja-published]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/studio-ja-wav-published.json
[studio-published]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/studio-three-languages-published.json
[backend-approved]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/language-store-approved-readback.json
[decode-proof]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/final-dub-decode-readback.json
[recovery-440b]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/prepared-recovery-440b10d6-f8bf8ae5-009c-42c9-902b-0343a207e809/run-ab885ca4-0f91-481b-b773-65cf026aced1/receipt.json
[ko-502]: C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/ko-pure-retake1-502-evidence.md
