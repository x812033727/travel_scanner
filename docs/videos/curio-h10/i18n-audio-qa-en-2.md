# H10 English dub: targeted retake and second audio QA

Reviewed 2026-10-16 (Asia/Taipei). This is a read-only triage of the completed paid run; this reviewer did not call TTS, Gemini, or TypeSafe Jev and did not approve the dub.

## Current artifact

- Approved zh-TW `video.json` SHA-256: `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`; revised English `i18n/en.json` SHA-256: `99EF6F2F11DDFC72DDD94072B82C66E86126A2EBDFCB691F1614514C901AD7E3`. The three English wording changes passed [independent review](i18n-review-en-3.md).
- Local media under `<home>/mokaair-work/videos/curio-h10`: `dubs/en/narration.wav` SHA-256 `3E5F492CF89F8E3BF093434B0457B3EE326CB680A43464BE35E3B9E976750553`; exported `dubs/en.m4a` SHA-256 `6382426E07EB5809F63A08C5CC77583DD25D9B6B18BEE9840BE856F4D8508BAD`; `dubs/en/timeline.json` SHA-256 `078F0FFAE6360CB1BCC8D0627ED773AA73CE9DBBF4E9D69B67F623A2D51E45A7`. The exported track measures 614.20 seconds by `ffprobe`.
- Timeline binds translation hash `64b8150108224a77` and speech hash `0a29b510bcc5591c`. Current `review/check.en.json` SHA-256 `2D9AEAD9723698B9F58898E4A0764E95A1FF1E7C23D0C61F7D8E7E94D5B842501A99656`; `review/check-flags.en.json` SHA-256 `99F440A47798E1A4E169EEAF0F878E11D7DD951726FDA5614C25837AC6821374`.
- All 82 lines were checked: 68 exact, 8 Jev-accepted differences, 6 flags. The first check had 8 flags. The three targeted clips are `h5cac1f4` SHA-256 `574184BD7C581EB0B9C7EC9E4AEF55295900E015A0A43935F42AB1169631FB38`, `h72b4789` `47AB0B466CCC0DFE712E1074B3A9603987BED3F260F72D859F3D2FC8D8744C4C`, and `hb624337` `7CAA336E3440D5B6A92DB2B534E18C81849EEFF762BDBB4A8DF65A82EF1EAEFF`.
- The shared spend ledger reconciles this targeted three-clip TTS and cached check-audio as a conservative US$0.04 estimate: 3 TTS requests / 236 billable characters, 3 new Gemini transcriptions, and 1 Jev judgment. The provider invoice is unavailable; this is stop-limit accounting under H10's separately approved US$2 multilingual increment.

The revised `h5cac1f4` and `h72b4789` are exact in the new Gemini check and have matching lexical content in a new offline Whisper small pass. The revised `hb624337` retains one flag because `April 25` was transcribed as `April 25th`; offline Whisper also gives `25th` and writes `Bax` for the homophonous `Back's`. Both transcriptions retain **entry**, **plan**, **Fish River**, and **the next day**. The offline retake transcription is `review/whisper-small-en-retakes-20261016.txt` (SHA-256 `0B3A20B5E773702124CF1ECFDD9CF8258A9A72402CEFA47383D42C151B8CEB36`); the five unchanged flagged clips were checked against `review/whisper-small-en-flags-20261016.txt` from the first dub.

## Six remaining flags

| ID | Gemini/Jev difference | Independent offline evidence | Triage |
| --- | --- | --- | --- |
| `h1dff7cb` | `May 28th` for written `May 28` | Old Whisper renders `May 28`. | Ordinary spoken date / transcription format. No evidence to retake. |
| `h1d74698` | `June 11th` for written `June 11` | Old Whisper also renders `June 11th`. | Ordinary spoken date, same day and year. No evidence to retake. |
| `hb624337` | Revised line gives `April 25th` for written `April 25`. | New Whisper also gives `April 25th`; `Bax` is how `Back's` sounds. | Orthography and name spelling. The recorded **plan** and April 26 implication survived; no evidence to retake. |
| `h3a137ee` | `Inookpoozhejook` for `Inukpujijuq`. | Old Whisper writes `Inuk Pujizhuak`; both are phonetic approximations. | Proper-name pronunciation cannot be confirmed from ASR spelling. Owner should listen to the name. |
| `hcc5d7ed` | Gemini inserts `thought` before the question. | Old Whisper starts at `which features` with no extra word. | Possible Gemini hallucination, but listen to the start of the clip to exclude a real stray word. |
| `h2fd7271` | `descendant sample` for `descendant's sample`. | Old Whisper also omits the possessive mark. | Adjacent /s/ sounds make written possessive uncertain; meaning remains the sample of a living descendant in context. No evidence to retake. |

**Decision:** No further paid retake is justified by the two ASR passes alone. The name `h3a137ee` and possible stray word `hcc5d7ed` need owner listening; the other four flags are pronunciation or orthography differences without a demonstrated semantic error. All six flags still require the normal owner audio gate. The local 82-line English dub listening page at `<home>/mokaair-work/videos/curio-h10/review/dub-en.html` first shows the six flags and the two retakes cleared by QA; its SHA-256 is `13E4CD1A033B576EF31BA252F9F152055BE99870CF1603757053D9AE788E56E0`. It is a local preview, not a backend approval.

## Owner listening follow-up

The owner subsequently replied 「英語旁白可以」 after the listening handoff. This records the human listening result for the six flagged clips, including the proper name and possible leading word. It does not by itself record an `/admin/videos` upload-package approval or publication.
