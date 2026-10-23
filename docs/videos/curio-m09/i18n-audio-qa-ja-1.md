# M09 Japanese dub and audio QA — 2026-10-16

The owner selected Japanese metadata, captions and dubbing in `/admin/videos` and separately approved an M09 multilingual estimate stop limit of US$2.50. The independently reviewed `i18n/ja.json` has SHA-256 `E3F0379F280457DD0986BEAE735CF21A595108D72B2016A5E8F59E07743D9695`; source `video.json` has SHA-256 `9F52ECF207849E0892F5F75DAF0C42DF9078E78D8899297ED5E464D0D9814363`. The translated text has not been edited for this QA round.

## Dub and accounting

`dub --locale ja --dry-run` planned 95 requests and 2,134 billable characters, with no window beyond the 1.15x fit limit. The actual run synthesized 95/95 clips, reusing none; 3 of 93 windows sped up, at most 1.1x, and no window exceeded its slot. `dubs/ja.m4a` measures 559.100 seconds and SHA-256 `7D02E468699D2CFB71910D7C3ABCD41EAC92E1E9D1CBB9DF938739A40FA2A145`. `dubs/ja/audio/cache.json` contains 95 takes and the speech journal had no uncertain request. Shared ledger entry `m09-dub-ja-20261016-01` was reserved and reconciled at a conservative US$0.15 estimate; final vendor billing was unavailable.

## Audio comparison

`check-audio --locale ja` transcribed all 95 clips with Gemini and made two TypeSafe Jev judgments. It found 51 exact matches, 20 Jev-accepted differences and 24 flags. Exit 1 reflects those quality flags, not an incomplete run. `review/check.ja.json` SHA-256 is `61CD22BACE7673923728162FBA0677DA71EE934A388590E345EE6DCFD8FF5C54`; `review/check-flags.ja.json` SHA-256 is `F2D580551D81614C779D0F8AFE7E51F2FF48366E52CBF72191885CA8F390EEA6`. Ledger entry `m09-dub-ja-qa-20261016-01` was reserved and reconciled at a conservative US$0.50 estimate, making M09 estimated spend US$5.134 / US$8.50 after Japanese QA.

After main commit `aa36ce02d` added leaked-word detection, a cache preflight found all 95 WAV hashes matched their transcription entries and every nonmatch already had a Jev verdict. A guarded rerun blocked network access and observed **0 network attempts, 0 new transcriptions and 0 Jev calls**. It produced the same 24 flags and no leaked-word flag; both QA file hashes remained unchanged. Exact previous copies are retained under `review/*ja.pre-leak-rule-20261016.json`.

An independent offline faster-whisper small pass (CPU int8, Japanese, beam 5, no VAD or previous-text prompt) covered all 24 flagged WAVs. Its TSV is `review/whisper-small-ja-flags-20261016.txt`, SHA-256 `AD66BE7ED731A3D8476F2DCED26D7FF37BECDA9B67BD70F91A7B3E0C3BE67B73`. The listening page at `<home>/mokaair-work/videos/curio-m09/review/dub-ja.html`, SHA-256 `1A58C469589A7B6C8C62E9A44F19DA7D740CF5EB62AB2D2F54E91601D4A2CE82`, puts eight uncertain clips first and provides all 24.

| Priority ID | Approved Japanese | Gemini / offline finding | Triage |
| --- | --- | --- | --- |
| `gi7k` | `…島沖です` | Gemini ends `…島沖で`; Whisper corrupts the place phrase but ends `です` | Listen for the final syllable |
| `5cah` | `…見えました` | Both hear `…見えたんです` | Likely changed wording; listen before a targeted retake |
| `rwa9`, `5tiw` | `小盤` | Both produce `小判` or `個番` | Listen for a coin-like `こばん` reading; the term itself may need an unambiguous translation |
| `35ke` | `天の時間` | Both hear `雨の時間` | Listen for the sky/rain ambiguity |
| `b3gv` | `結果ごと` | Both hear `経過ごと` | Listen for a changed noun |
| `avua` | `管軸` | Both hear `各軸` | Listen for the mechanical term |
| `32we` | `選択が要ります` | Gemini hears `選択があります`; Whisper hears `選択が入ります` | Two recognizers disagree; listen for the verb |

The other 16 flags are `nk25`, `hwfk`, `c6qp`, `4ci3`, `vrwn`, `ydxy`, `i5mw`, `7wfi`, `n6ri`, `vsnk`, `r9ri`, `tsq6`, `gfsv`, `8k59`, `wnbq`, `mmyi`. Whisper supports the approved wording or a same-sound rendering for these; the listening page retains each original clip and both transcripts for audit. This is a triage conclusion, not a claim that an automated transcript proves the actual spoken word.

The [National Astronomical Observatory of Japan's Antikythera explanation](https://eco2.mtk.nao.ac.jp/koyomi/exhibition/060/) calls the smaller auxiliary dials `副文字盤`, a possible clearer term for `rwa9` and `5tiw` if owner listening confirms ambiguity. No Japanese translation, WAV, or track was changed based on this finding. Owner listening and any independent review of targeted translation wording remain open.
