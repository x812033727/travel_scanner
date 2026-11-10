# Curio S59 R8 blind reader A

Script SHA-256 before review: `f0fd2a6069844fe99e994367f3fa8d27b36928231dc0695fd816762c18faf07b`.

This ballot was frozen before the official narrative CLI. I read only `script.md`, the fixed `NARRATIVE_PANEL`, and the narrative rules in `script-writing.md` for editorial assessment. The raw ballot is in `r8-blind-a/answers.json`.

Verdict: **fail**. Eleven of the twelve required questions are yes; `payoffs` is no. The advisory chapter-title question is yes.

| Question | Vote | One quoted spoken line |
| --- | --- | --- |
| `scene_first` | Yes | [s59001] 一八七八年三月十一日，巴黎科學院裡，普斯卡斯準備轉動一台圓筒機。 |
| `no_spoiler` | Yes | [s59008] 幾位院士走進秘書室，請普斯卡斯重試；在那裡又會怎樣？ |
| `one_line` | Yes | [s59070] 開場那天，杜蒙塞爾代表愛迪生將這台機器呈給科學院。 |
| `no_toc` | Yes | [s59009] 這隻手轉出的人聲，要怎麼證明不是那張嘴偷偷發出來的？ |
| `chapters_link` | Yes | [s59080] 他真的試了，卻沒做出剛才那個效果。 |
| `open_loops` | Yes | [s59077] 難題其實變得更窄：人聲究竟留在錫箔上，還是有人趁著搖柄替喇叭口補聲？ |
| `payoffs` | **No** | [s59059] 杜蒙塞爾說，錫箔反覆播放後壓痕會漸淺，聲音也逐漸模糊；這會不會妨礙旁人重聽？ |
| `no_recap` | Yes | [s59030] 還記得開場那張十八美元的草圖嗎？愛迪生就在這時把小機器畫了下來。 |
| `chapters_are_events` | Yes (advisory) | [s59090] 秘書室裡，普斯卡斯照要求重新讓機器發聲。 |
| `outro_no_next` | Yes | [s59110] 原始資料和頻道連結都在說明欄；喜歡歷史謎題，訂閱奇聞檔案局。 |
| `opening_hooks` | Yes | [s59007] 愛迪生後來提到一張十八美元的草圖；它究竟做出了什麼？ |
| `one_thread` | Yes | [s59108] 那個說話者的嘴，終於能和喇叭裡的聲音分開看：箔上的壓痕自己推動薄片。 |
| `no_detour` | Yes | [s59064] 杜蒙塞爾另記，規律的鐘錶機構讓二重唱重播得較好；可巴黎院士要查的，仍是那台手搖機。 |

`payoffs` reason: s59059 introduces a fresh question about whether the degrading foil prevents other people from hearing a replay. The later material moves to playback speed, a different drive, and public testing. It never returns to that listening consequence with a new answer. The opening's other previews receive identifiable answers.

The opening previews three later moments without revealing their outcomes: Du Moncel's own trial, the eighteen-dollar sketch, and the secretary-room retest. The return to the Paris event is explicitly introduced as the opening day, so I treated it as the promised callback rather than an unrelated second story.

Official CLI: `node tools/video/cli.mjs narrative --slug curio-s59 --answers docs/videos/curio-s59/review/r8-blind-a/answers.json --workdir <isolated /tmp directory> --json`. It recorded round 1, `passed: false`, `failed: ["payoffs"]`; exit code 1 is the expected failed-panel result, with empty stderr. The exact workdir and the CLI stdout, stderr, exit code, and official record are preserved in `r8-blind-a/`.

Script SHA-256 after the official CLI: `f0fd2a6069844fe99e994367f3fa8d27b36928231dc0695fd816762c18faf07b`. The frozen raw ballot's SHA-256 is `3d6f382a8fa806337f03044da5b6f34d6abac1810c29826e45b1fb9b6a863f74`.
