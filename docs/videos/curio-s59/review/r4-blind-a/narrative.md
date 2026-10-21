# S59 R4 independent blind narrative reader A

This score was fixed before reading any S59 author receipt, previous review, other reader ballot, or earlier verdict. I read the frozen `script.md`, `video.json`, and the fixed 13-question narrative panel. The `curio-episode` skill and its linked narrative rubric supplied the series gate. No creative material or paid media was changed.

## Frozen inputs and result

| Input | SHA-256 |
| --- | --- |
| `script.md` | `5b18eb40b5c3434599abbd939d3231fc30837e360bfaff0ea00d23cdca89cf48` |
| `video.json` | `108db5d8ae5b540e396b1e9add3490c7ac8761e1aaa7dfd76b172edbadaba226` |

**Independent score: 13 yes, 0 no.** All 12 required questions pass; the advisory chapter-name question passes. Raw answers are in [narrative-answers.json](narrative-answers.json). The isolated official CLI produced [official-narrative-record.json](official-narrative-record.json) and [cli-verdict.json](cli-verdict.json): `passed: true`, round 1, `failed: []`, `advisory: []`, exit 0. The CLI work directory was `/tmp/curio-s59-r4-blind-a-work/curio-s59`, separate from prior receipts.

## Fixed panel

| # | ID | Yes? | Script evidence and reason |
| --- | --- | --- | --- |
| 1 | `scene_first` | Yes | `[s59001]` dates and places Puskas at the Paris Academy, about to turn the cylinder; `[s59002]` makes him act. |
| 2 | `no_spoiler` | Yes | `[s59006]` asks whether the inexperienced Dumoncel can succeed. The opening leaves his result and the secretary-room result unresolved. |
| 3 | `one_line` | Yes | `[s59070]` explicitly returns to the opening Academy scene after the machine's origin and first demonstrations; its ventriloquism test remains the same thread. |
| 4 | `no_toc` | Yes | `[s59077]` narrows the factual problem to foil versus operator. The chapter changes use concrete questions and actions, without listing the video's sections. |
| 5 | `chapters_link` | Yes | `[s59080]` answers the preceding chapter's question about Dumoncel's attempt. The other joins carry forward the cylinder/voice question (`s59009→s59010`), sketch (`s59032→s59033`), editorial visit (`s59066→s59067`), and secretary-room test (`s59089→s59090`). |
| 6 | `open_loops` | Yes | `[s59029]` holds the practical recording medium unresolved. Further questions keep the story moving through recording, replay, unfamiliar operators, and independent retests. |
| 7 | `payoffs` | Yes | `[s59096]` gives the new physical reason for Dumoncel's initial failure. Other distant openings resolve at `s59006→s59080`, `s59007→s59033`, `s59008→s59090–s59091`, and `s59009→s59108`; the script calls the opening scene back when it returns. |
| 8 | `no_recap` | Yes | `[s59070]` names the opening day before adding the previously withheld test details. Later mechanical reminders acquire a new consequence: Dumoncel's distance at `s59096–s59099` and the final separation of mouth from playback at `s59108`. |
| 9 | `chapters_are_events` | Yes | `[s59090]` opens “秘書室重試，疑問落在話筒邊” with Puskas actually making the machine sound again. The chapter headings name actions or revelations. |
| 10 | `outro_no_next` | Yes | `[s59110]` offers sources and a channel subscription; it names no subsequent episode. |
| 11 | `opening_hooks` | Yes | `[s59008]` teases the still unknown secretary-room result. The first scene is followed by four unresolved future moments/questions at `s59006–s59009`. |
| 12 | `one_thread` | Yes | `[s59055]` keeps the concrete problem of foil playback versus an operator's voice at the center. The origin, mechanics, public demos, failed try, and repeat test all advance that object and question. |
| 13 | `no_detour` | Yes | `[s59106]` introduces the telephone as a proposed way to test the same ventriloquism suspicion. The telegraph and foil mechanics establish how a voice can be stored and replayed; speed and technique explain why demonstrations differed. |

The score concerns story structure only. It does not independently certify the source claims, historical accuracy, audio, visuals, or production readiness.
