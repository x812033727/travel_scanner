# M09 Korean dub and audio QA — 2026-10-16

The owner selected Korean metadata, captions and dubbing in `/admin/videos` and separately approved an M09 multilingual estimate stop limit of US$2.50. The independently reviewed `i18n/ko.json` has SHA-256 `45572C2D51D182CFCBCD7CEEB4A476698E3C3170C6E52064540270BFFBFD02B7`; source `video.json` has SHA-256 `9F52ECF207849E0892F5F75DAF0C42DF9078E78D8899297ED5E464D0D9814363`. The translated text has not been edited for this QA round.

## Dub and accounting

`dub --locale ko --dry-run` planned 95 requests and 2,586 billable characters, with no window beyond the 1.15x fit limit. The actual run synthesized 95/95 clips, reusing none; none of 93 windows was sped up or exceeded its slot. `dubs/ko.m4a` measures 559.100 seconds and SHA-256 `7A264D836D28247CB63F5C0E44AD9C5C59899D92334F4189870EC94B9C155336`. `dubs/ko/audio/cache.json` contains 95 takes. The shared speech-journal directory has no held requests after the completed run. Shared ledger entry `m09-dub-ko-20261016-01` was reserved and reconciled at a conservative US$0.15 estimate; final vendor billing was unavailable.

## Audio comparison

The post-`aa36ce02d` `check-audio --locale ko` transcribed all 95 clips with Gemini and made one TypeSafe Jev judgment. It found 64 exact matches, 12 Jev-accepted differences and 19 flags. Exit 1 reflects those quality flags, not an incomplete run. `review/check.ko.json` SHA-256 is `72CF66DAB8B3433665009CCC4C1C0BCF9EE09D98D93E482C0A674C15BEBF6224`; `review/check-flags.ko.json` SHA-256 is `71354A3AFAFB3B9613AE3821CAE387E58B8A454D5A7D7E7882844E56ED08B249`. Ledger entry `m09-dub-ko-qa-20261016-01` was reserved and reconciled at a conservative US$0.50 estimate, making M09 estimated spend US$5.784 / US$8.50 after Korean QA. The ledger was independently read back after the atomic update (SHA-256 `F5EEC5A81E87ABFAC8E1FA2DD942CB88902F8D79AA296F7E48257BF8FED68626` at that moment).

An independent offline faster-whisper small pass (CPU int8, Korean, beam 5, no VAD or previous-text prompt) covered all 19 flagged WAVs. Its TSV is `review/whisper-small-ko-flags-20261016.txt`, SHA-256 `E108E9511E63FA6D25701CA4E47B311687264236F400C3D2E6D58905460BE52B`. The listening page at `<home>/mokaair-work/videos/curio-m09/review/dub-ko.html`, SHA-256 `679A9B3E49AAAB97FD36F8D80A2D5CCD630EED09E185E839338A4B0DA8D72CFD`, puts eight uncertain clips first and provides all 19. All linked WAV files exist.

| Priority ID | Approved Korean | Gemini / offline finding | Triage |
| --- | --- | --- | --- |
| `riwp`, `32we` | `제한` (restrict) | Both hear `제안` (suggest) in both lines | Hear the intended evidence boundary before deciding on retakes |
| `n8f4` | `이듬해` (the next year) | Gemini hears `이 때문에`; Whisper hears `이때면` | Listen for the temporal transition |
| `u5ar` | `셀까요` (count) | Both hear `쓸까요` (write/use) | Listen for the verb |
| `ydxy` | `식의 주기` (eclipse period) | Both hear `시계 주기` (clock period) | Listen for the astronomical term |
| `5tiw` | `위 작은 판` (upper small dial) | Both hear `이 작은 판` (this small dial) | Listen for the location |
| `tsq6` | `관축을 겹쳐 씁니다` (nested tubular shafts) | Gemini hears `광축을 겹쳤습니다`; Whisper supports `관축` but also hears past tense | Listen for the technical noun and tense |
| `fyct` | `배치해도` (even if arranged) | Both hear `배치에도` | Listen for the conditional evidence boundary |

The other 11 flags are `x9jb`, `w2cm`, `hwfk`, `pdjs`, `pk3b`, `vrwn`, `bauw`, `xzqu`, `vsnk`, `w3c9`, `6pzf`. The second recognizer supports the approved noun or a same-sound rendering in most of these; the listening page retains each original clip and both transcripts for audit. This is a triage conclusion, not a claim that either automated transcript proves the actual spoken word.

Owner listening is pending for the eight priority clips. No Korean translation, WAV, or track was changed based on these recognizer results; no targeted retake or new paid call was made.
