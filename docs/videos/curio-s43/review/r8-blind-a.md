# curio-s43 — independent blind narrative read A

## Scope and integrity

Read only `docs/videos/curio-s43/script.md`, `docs/videos/curio-s43/video.json`, and the official output of `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s43 --json`. No research, brief, claims, verification, prior review, or task notes were consulted. No repository edits or paid calls.

| Allowed file | SHA-256 | Check |
|---|---|---|
| `script.md` | `0b255d4c8af07a85a5fcab56f7f748105e15a3e25d3e55ff1d3739991a60b29e` | Matches expected |
| `video.json` | `e812da7a3f9e40cd32d03daa177729faa296fe473c44bd744d58b592ccefd002` | Matches expected |

## Official 13 questions

| ID | Yes/No | Scene evidence and reason |
|---|---|---|
| `scene_first` | **Yes** | dn001 opens with “一八三一年八月底，達爾文從北威爾斯的地質旅行回家” and the waiting Henslow letter. dn002–dn003 give the letter's offer and his earlier Tenerife plan. The first four sentences place a person and document in a specific arrival, rather than introducing the topic. |
| `no_spoiler` | **Yes** | The opening stops before each result: dn005 “這封信是答應，還是拒絕？”, dn006 “舅舅能讓父親改口嗎？”, dn007 “寫給姊姊的是好消息嗎？”, and dn008 “船長從中看出什麼？” It names later moments without giving their answers. |
| `one_line` | **Yes** | After the opening preview, dn010–dn023 trace the recommendation; dn024–dn036 the refusal; dn037–dn053 the uncle's intervention; dn054–dn065 the captain's letter and vacancy; dn066–dn078 the meeting and decision; dn079–dn088 the later nose account and departure. The explanation of the Wood letter at dn076 adds its motive, rather than replaying the episode. |
| `no_toc` | **Yes** | dn009 asks “寄出邀請的亨斯洛，能自己決定誰上船嗎？” and dn010 answers “不能”; transitions are questions and consequences, with no announced chapter list or “接下來要講” line. dn039's “接下來兩年” refers to Darwin's next two years, not the video's structure. |
| `chapters_link` | **Yes** | Each chapter begins from its preceding concrete question: dn009→dn010 (“能自己決定”→“不能”); dn023→dn024 (his reply); dn036→dn037 (the uncle); dn053→dn054 (can he accept yet?); dn065→dn066 (the captain's difficulties); dn078→dn079 (the other reservation, his nose). |
| `open_loops` | **Yes** | Questions or withheld outcomes keep recurring: dn014 “船長另要什麼？”; dn023 “怎麼回答？”; dn041 “真有證據嗎？”; dn060 “哪位原定旅伴的缺席”; dn069 “花錢是最後障礙嗎？”; dn077a “他的想法變了嗎？” In the official timeline, the gaps between these and neighboring hooks remain well under 90 seconds. |
| `payoffs` | **No** | dn071 opens “船究竟會不會駛向南太平洋群島.” dn074f says the route is still uncertain, and dn077b1 says “這封信沒說最後怎麼定案.” The latter names the same route but gives no new resolution to whether the ship would go there. The decision to board (dn077b) resolves a different question. Other major hooks do pay off, for example dn007→dn057 and dn008→dn082. |
| `no_recap` | **Yes** | Recurrences add a changed state or an explicit callback. dn074d says he buys nothing while undecided; dn077c recalls “幾天前” and now says he orders a telescope and compass. dn057 reports the discouraging captain's letter; dn076 later supplies its motive. Repeated names and the South Pacific route serve the same developing decision, without a repeated block of facts. |
| `chapters_are_events` | **Yes** | Titles name occurrences or revelations: “一封邀請信來到什魯斯伯里,” “亨斯洛把達爾文推薦出去,” “父親的顧慮使他先拒絕,” “伍德收到船長回信,” and “鼻子的說法，出現在多年後.” |
| `outro_no_next` | **Yes** | The outro (dn999a–c) answers the nose claim, asks the viewer whether they would sail, and points to source links. It does not mention another video or file. |
| `opening_hooks` | **Yes** | After dn001–dn003 establish the arrival and invitation, the opener offers at least four specific later moments before their results: the reply (dn005), the uncle's appeal (dn006), Wood receiving the captain's letter (dn007), and the captain judging the nose (dn008). |
| `one_thread` | **Yes** | Darwin's possible place on the Beagle is the continuous difficulty. dn032 refuses, dn050 says his father changes his mind, dn057 says he thinks he is out again, dn077b says he expects to go, and dn087 confirms he sails. The late nose account resolves the title's version of the same question. |
| `no_detour` | **Yes** | The apparently ancillary detail at dn076b (“原有軍官都留任；前次三分之二的船員與八名陸戰隊員，也願再上船”) is presented as Darwin's evidence that the captain is reliable (dn076a), directly relevant to his decision. The salary, cabin, food, route, and equipment details similarly affect whether he can go. No separate subplot or sustained inventory interrupts the line. |

**Verdict:** 12 Yes, 1 No. The unresolved South Pacific route is the one substantive payoff failure under the official questions.

## Timing estimate

The first three scenes contain the opening's first four sentences: 87 Han characters. At an assumed speech-only rate of 240–270 Han characters per minute, they take roughly **19–22 seconds**; the tool timeline places dn005 at **00:23**. Thus the first four sentences are somewhat longer than the question's “約 15 秒” cue, though they meet its scene requirement.

The full opener (dn001–dn009) contains **202 Han characters**: about **45–51 seconds** of speech at that rate; the official tool timeline runs **00:00–00:56**. The body (dn010–dn088) contains **2,179 Han characters**: about **8:04–9:05** of speech; the tool timeline runs **00:56–10:50** (**9:54**). The outro begins at **10:50** and its final line starts at **11:02**, so the tool's implied finished runtime exceeds **11:02**, above `video.json`'s 8–10 minute target. Speech-only figures are pace estimates, not measured audio duration.
