# Curio S43 R9 — independent blind story read A

## Scope and freeze

- Read only `docs/videos/curio-s43/script.md`, `docs/videos/curio-s43/video.json`, and the official `narrative --slug curio-s43 --json` output.
- Verified before reading: script SHA256 `d064b7eaa757cf6f3889e87bfccd43a9c958c0adacc603320e41f117a251792b`; video SHA256 `c6a0f334f13aea045b669eb0c3bf4112472dd8ae3cdb636dffa5209ef47d618d`.
- Timing below is the official narrative's **speech-only** clock, not rendered audio. Opening chapter: **00:00–00:56 (0:56)**. Main body: **00:56–11:06 (10:10)**. Outro begins **11:06**; its last spoken line starts **11:18**, and the output gives no final end timestamp. The speech therefore runs past 11:18, above the video's 8–10 minute target. This length observation is separate from the 13 story questions.

## Official 13-question verdict: 13 Yes, 0 No

| # / ID | Answer | Exact speech and scene evidence |
| --- | --- | --- |
| 1 `scene_first` | **Yes** | `dn001` (00:00) starts in late August 1831 with Darwin returning from a north Wales geology trip to Henslow's waiting letter; `dn002` (00:09) says the letter invites him aboard the Beagle. The opening is a specific action, place/time and document. |
| 2 `no_spoiler` | **Yes** | Opening `dn005` (00:23) asks whether Darwin accepted; `dn006` (00:29) asks whether his uncle changed his father's mind; `dn007` (00:35) asks whether Wood's captain letter brought good news; `dn008` (00:43) asks what the captain saw in the nose. None gives its later answer. |
| 3 `one_line` | **Yes** | After the opening preview, `dn010–dn023` follows Henslow's recommendation, `dn024–dn035` the first refusal, `dn037–dn050` the uncle's intervention, `dn054–dn062` the captain's letter and vacancy, `dn066–dn077b` the meeting and decision, and `dn079–dn088` the later nose recollection and sailing. `dn078` explicitly places the nose story as something Darwin learned after knowing the captain, so the later recollection advances the same discovery. |
| 4 `no_toc` | **Yes** | The chapter transitions are story questions and replies: `dn009` asks whether Henslow could decide the berth, and `dn010` replies “不能”; `dn023` asks how Darwin replied, and `dn024–dn032` show the letter and refusal. No spoken line declares an upcoming section or lists the video's structure. |
| 5 `chapters_link` | **Yes** | All six transitions answer the prior chapter's concrete prompt: `dn009→dn010` (authority); `dn023→dn024` (reply); `dn036→dn037` (which adviser: uncle Josiah Wedgwood); `dn053→dn054` (whether he can commit now: wait); `dn065→dn066` (shared cabin difficulty); `dn078→dn079` (other hesitation: nose). |
| 6 `open_loops` | **Yes** | New unresolved questions are frequent: `dn005–dn008` at 00:23–00:43; `dn014` 01:23, `dn019` 01:56, `dn023` 02:22; `dn029` 03:03; `dn036` 04:00; `dn049` 05:01; `dn060` 06:14; `dn069` 07:13; `dn074b` 08:02; `dn077a` 09:18; `dn086` 10:28. There is no 90-second body interval without a new unresolved question. |
| 7 `payoffs` | **Yes** | Long loops get concrete named returns: `dn008` asks what the nose meant, answered by `dn082` (10:08): “從鼻形懷疑他缺少毅力”; `dn029` worries about living with the captain, answered by `dn074` (07:44): “先前擔心…見面後…覺得兩人能相處”; `dn071` raises the South Pacific route, returned to by `dn087a–dn087b` (10:42–10:49), naming Tahiti and the 1835 sighting. Other prompts resolve directly: `dn005→dn032` refusal, `dn006→dn050` father changes mind, `dn007→dn057` he writes that he will not go, `dn060→dn062` Chester's vacancy, `dn074b/dn074f→dn077b` his decision to go, `dn086→dn087` December 27 departure. |
| 8 `no_recap` | **Yes** | Revisited facts change state or explicitly return to a hook. `dn025` establishes the father's objection and `dn032` gives its new consequence (Darwin actually refuses); `dn074d` says he buys nothing while undecided and `dn077c` contrasts this with new equipment orders; `dn071` raises the route and `dn087a` explicitly calls back to “他九月掛心的航路” before reporting Tahiti. No passage simply repeats a number or conclusion to fill time. |
| 9 `chapters_are_events` | **Yes** | Chapter names identify happenings or revelations: “一封邀請信來到什魯斯伯里”, “亨斯洛把達爾文推薦出去”, “父親的顧慮使他先拒絕”, “舅舅帶著顧慮去見父親”, “伍德收到船長回信”, “兩人在倫敦談明白狹窄的船”, “鼻子的說法，出現在多年後”. |
| 10 `outro_no_next` | **Yes** | `dn999a–dn999c` (11:06 onward) answers the nose question, asks the viewer whether they would go, and points to source links; no next video, episode, or file is mentioned. |
| 11 `opening_hooks` | **Yes** | Beyond the initial letter scene, `dn005` (reply), `dn006` (father's change), `dn007` (Wood's captain letter), and `dn008` (the nose judgment) present **four** concrete later moments without their outcomes. |
| 12 `one_thread` | **Yes** | Darwin's Beagle berth remains the problem: nomination (`dn012`), refusal (`dn032`), reversal (`dn050`), seeming loss and vacancy (`dn057–dn062`), captain meeting and personal decision (`dn074–dn077b`), nose recollection (`dn079–dn083`), actual departure (`dn087`). |
| 13 `no_detour` | **Yes** | Apparent side details feed that berth decision: crew retention at `dn076b` is Darwin's evidence that the captain is reliable before `dn077b`; the Tahiti landing at `dn087a–dn087b` closes his earlier South Pacific uncertainty from `dn071/dn074f`. There is no detached list or unrelated section. |

## Blind-reader note

The story questions pass on the speech as written. The material practical issue outside those questions is duration: the body alone is 10:10, and the outro starts at 11:06, so the current spoken cut exceeds the `video.json` target of 8–10 minutes.
