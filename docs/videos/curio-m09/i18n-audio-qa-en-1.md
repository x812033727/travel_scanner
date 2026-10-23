# M09 English dub and audio QA — 2026-10-16

The owner selected English metadata, captions and dubbing in `/admin/videos` and separately approved an M09 multilingual estimate stop limit of US$2.50. The independently reviewed `i18n/en.json` has SHA-256 `9C0AE224FE1D2EFAA85F2928A86C29ADBB513B153695CE395D1CB74B2CF7B643`.

## Dub and recovery

`dub --locale en --dry-run` planned 95 requests, 5,520 billable characters and no unfit time slot. The initial run cached 53 WAVs, then held a 64-character POST after HTTP 502. [The host evidence](i18n-dub-en-502-recovery.md) establishes that Nginx could not connect to the web upstream, so that POST never reached the API or Gemini. Before clearing the exact held request SHA `22c2a8a38039b40008d89a7208f532fc69e949fe11a7355247f121926447036e`, its JSON was copied to `<VIDEO_WORKDIR>/curio-m09/review/speech-journal-held-22c2a8a38039b40008d89a7208f532fc69e949fe11a7355247f121926447036e.json`; original and copy both hashed `BB2DA6BA8413274483C1A2F5CF3C508D5DFD1B672EEB80CFDF2510AD1961A48F`. `speech-journal forget` was used for **that SHA only**, and `speech-journal list` then reported no entries. The owner separately authorized this exact retry, including any possible duplicate charge.

The resumed `dub --locale en` ran without `--force`: 42 new requests and 2,458 characters, 53 cached takes reused. The completed dub therefore has 95/95 WAVs and 5,520 synthesized characters. All 93 windows fit at ordinary speed, with zero sped or overlong windows. `dubs/en.m4a` measures 559.100 seconds and SHA-256 `3500B12D310E73FA4C15B322E937D56D4ABDCE0823BA67DC07DC4F4BC138ADBE`. The shared ledger entry `m09-dub-en-20261016-01` was reserved and then reconciled at a conservative US$0.15 estimate; final vendor billing was unavailable.

## Audio comparison

`check-audio --locale en` transcribed all 95 clips with Gemini and made one TypeSafe Jev difference judgment. It found 89 exact matches, 2 Jev-accepted differences and 4 flags. Exit 1 reflects those quality flags, not an incomplete run. `review/check.en.json` SHA-256 is `A96A53B1D1E658618EE3D1A27BB3088A8B59D39B7379CB4B316FFCFF3CD9DED8`; `review/check-flags.en.json` SHA-256 is `0B2E0294094CFFB543FF360638A0C1C5424567810F9A1A847EA9B770D2AA1C7C`. `speech-journal list` remained empty. Ledger entry `m09-dub-en-qa-20261016-01` was reserved and reconciled at a conservative US$0.50 estimate. M09's cumulative estimated spend became US$4.484 / US$8.50.

An independent offline faster-whisper small pass (CPU int8, English, beam 5, no VAD or previous-text prompt) on the four flagged WAVs is saved at `<VIDEO_WORKDIR>/curio-m09/review/whisper-small-en-flags-20261016.txt`, SHA-256 `9034F7CB241D2871DC551D2B90C29ABD0AE58428BA2BE85185A69FC05CC15E6A`. A four-line listening page at `<home>/mokaair-work/videos/curio-m09/review/dub-en.html` contains the approved wording, both transcripts and each WAV (page SHA-256 `10E1F17824F0C8158FD9DFFC05342EB7B8FF4E2CE04CE4C4CA89715AC265E395`).

| ID | Gemini transcript difference | Offline Whisper result | Triage |
| --- | --- | --- | --- |
| `gi7k` | adds “In” before 1901 | matches approved wording | Recognition disagreement; owner listening needed |
| `35ke` | “match” for approved “met” | “matched” | Both differ from approved verb; prioritize listening |
| `r9ri` | “will” for approved “would” | matches “would” | Recognition disagreement; owner listening needed |
| `gfsv` | “authors stop” for approved “authors stopped” | “author stops” | Both differ in tense; prioritize listening |

No retake or text change was made on the automated evidence alone. The owner subsequently listened to the four flagged clips in the linked page and confirmed **the English narration is acceptable**. This closes the human-listening step for this English track; the approved track SHA remains `3500B12D310E73FA4C15B322E937D56D4ABDCE0823BA67DC07DC4F4BC138ADBE`. English captions and the multilingual upload package remain separate downstream steps.
