# S46 R12 fresh blind narrative panel A

Script SHA-256: `d5e6f84c7fe1259e870472d7983c09784223cdea4c8d5337c70382126181584c`

Isolation: I read only the current `docs/videos/curio-s46/script.md` for episode content and `tools/video/core/narrative.mjs` lines 266–303 for the 13 criteria. I did not read the S46 brief, research, claims, earlier reviews, source materials, or other agents' findings. I read repository `AGENTS.md` and the `curio-episode` skill for workspace instructions; neither supplied episode evidence for this review.

| Criterion | Answer | Direct script evidence |
| --- | --- | --- |
| `scene_first` | Yes | `[bkw001]` 「一八四七年十月二十日，院長寫了一封回信。」 |
| `no_spoiler` | Yes | `[bkw004]` 「就算學生答應，這張票真能讓她讀完醫學嗎？」 |
| `one_line` | Yes | `[bkw042]` 「回到開場那封信：教授們前一晚才開本學期第一次會。」 |
| `no_toc` | **No** | `[bkw086]` 「她在教室裡能學了；接下來，她還想補哪一段醫學訓練？」 |
| `chapters_link` | Yes | `[bkw041]` 「終於，紐約州日內瓦的一封信到了。」 |
| `open_loops` | Yes | `[bkw097]` 「真正進病房後，臨床資訊還拿得到嗎？」 |
| `payoffs` | Yes | `[bkw103]` 「她看不到前人留下的判斷，只能靠自己逐項整理臨床所見。」 |
| `no_recap` | Yes | `[bkw102]` 「回到開場那張卡：她入院後，住院醫師真的停填診斷與治療欄。」 |
| `chapters_are_events` | Yes | `[script.md:171]` 「全班表決後，院長寄出回信」 |
| `outro_no_next` | Yes | `[outro; script.md:493]` 「原著固定版連結放在說明欄，方便核對她的記述。」 |
| `opening_hooks` | Yes | `[bkw005]` 「她還向北方一批學校遞交申請；究竟有幾所？」 |
| `one_thread` | Yes | `[bkw087]` 「一八四八年，第一段課程後，她仍缺病房臨床經驗；入學決議管得到那扇門嗎？」 |
| `no_detour` | **No** | `[bkw025]` 「她把這一場談話記在五月的日記裡。」 |

The opening also leaves concrete questions at `[bkw006]` (returning to class), `[bkw007]` (learning after bedside records stop), and `[bkw009]` (finding a formal route). The chapter break from `[bkw040]` waiting for a letter to `[bkw041]` its arrival is a particularly clean handoff. `[bkw103]` pays off the bedside-card question; `[bkw083]` pays off the classroom question. The same protagonist and goal run through admission, classes, hospital practice, and the diploma.

`no_toc` fails because `[bkw086]` says 「接下來」 and asks which training segment comes next, announcing the next content area before `[bkw087]` names the actual clinical obstacle. `no_detour` fails because `[bkw025]` only says that a conversation was recorded in a diary; it supplies no new action, obstacle, or answer in the diploma journey. `[bkw058]` also pauses for the friend's memento on her wall.

**Effect of `[bkw044]`:** 「院長回信寫著，她的申請信日期是十月三日。」 It dates the application letter. Together with `[bkw001]`'s October 20 reply, it lets a listener infer a 17-day wait after `[bkw039]` asks how long she can wait. Its placement between `[bkw043]`'s two student resolutions and `[bkw045–048]`'s answer briefly stalls that vote's reveal. `[bkw112]` also says October 3, but that is the **following year** and a different event (her return to Geneva), so I did not count the date as a repeated fact for `no_recap`. The line's chronology value kept it from being my decisive `no_detour` evidence.
