# S38 R4 audio check and R5 line repair

2026-10-20. R4 source and independent narrative review are in [verify-4.md](verify-4.md), bound to R4 script SHA-256 `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411`. This file records measured speech and the later four-line R5 change; **R5 still needs a fresh independent script and source/prompt review before further paid media**.

## Measured R4 audio

R4 synthesized 112/112 Gemini Sulafat lines. The first `timeline.json` had 17,902 frames at 30 fps, 596.733 seconds total. Story body from `pf006` to the start of `pf112` measured 561.133 seconds (9:21.13), above the 8-minute requirement.

The first `check-audio` reached 74/112 cached transcripts, then its `speech/transcribe` request SHA-256 `60ffa6a6e03f4a439758f04d4dc8cf51ed24b6dc06da44cfd51b793ccd68da7f` received HTTP 502 without a usable answer and was held in the speech journal. Rerunning the same native command did not resend it. The non-pilot website status API has no per-transcription billing receipt, so whether that request was charged remains unknown. Under the site owner's standing instruction to keep producing with my recommended decisions, the coordinating agent explicitly cleared **that one** hold and accepted possible duplicate transcription cost. The retry completed; no other hold was cleared.

Full first pass: 112/112 checked, 85 exact, 8 same-sound/filler, 5 Jev accepted, 14 flagged: `pf007,pf021,pf033,pf040,pf042,pf061,pf069,pf070,pf073,pf074,pf077,pf081,pf082,pf085`. Targeted `tts --redo` synthesized only those 14 lines (291 billable characters; 98 reused). Second check: 112/112 checked, 93 exact, 10 same-sound/filler, 5 Jev accepted, **4 flagged**: `pf040,pf069,pf077,pf085`. The first two check logs are `/tmp/curio-s38-r4-check-audio-retry1.log` and `/tmp/curio-s38-r4-check-audio-redo1.log`; machine-readable cached transcripts and current flags remain in `<VIDEO_WORKDIR>/curio-s38/review/`.

## R5 wording, frozen for fresh review

Four persistent or badly transcribed lines were simplified without changing the diary event:

| ID | R4 issue | R5 narration |
| --- | --- | --- |
| `pf040` | ASR returned a garbled phrase for the riverboat's view of the fire. The pinned diary says it had spread farther above and below the bridge, without naming a particular burned street. | 他再從船上看，橋的上游、下游，火都燒得更遠了。 |
| `pf069` | ASR consistently said `土坑` for `同坑`. | 佩皮斯趁機，把辦公文件也放進這個土坑。 |
| `pf077` | ASR consistently said `回應` for `回音`. | 佩皮斯另寫信請求拆屋許可，卻沒有等到答覆；街上會有人先動手嗎？ |
| `pf085` | The place-name `伍利奇` was repeatedly transcribed phonetically as `烏利齊`. | 這次他立刻帶著妻子和金錢，乘船往泰晤士河下游走。 |

R5 script SHA-256 `e7eca53fdb4d6fbae4c4454fc652bb33bd00ca1156f5e30e9fada26413a63cd5`, video SHA-256 `cafb69b501d7f0d41d09d90c8650a2f7198ffb5388c57beacf15a5a88f2994ec`, claims SHA-256 `2c0041720122040c94782054024e82f6dcf6da352e10986d1cdc71c93c594bb1`. `script` regenerated from `video.json`; `lint --json` returned 0 errors, 0 warnings, 112 lines and approximately 10.007 minutes. Claim IDs/text and 111 still prompts require independent R5 confirmation. No R5 TTS, audio approval, keyframes or storyboard approval has yet occurred.
