# R11 fresh blind B — curio-s49

**Verdict: FAIL.** Official questions `payoffs` and `no_recap` fail. This review used only the CLI `narration` string and its 13 official questions; `script.md` was hashed as raw bytes, not read as prose.

- Script file: `docs/videos/curio-s49/script.md`
- Script file SHA256: `a9fb4bcc6e271609d79e34d2f4278cdb2c797d0fc8af32b52d4f68b3b1629259`
- Narration UTF-8 SHA256: `9811b993b5264414fec15d02ad36101985cfc856706afd9447baba8168dc9b5c`
- CLI: `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s49 --json`

| Official question | Result | Narration evidence and judgment |
| --- | --- | --- |
| `scene_first` | PASS | `[moon001 00:00]`–`[moon004 00:18]`: 1835 年紐約讀者拿到《太陽報》，報紙宣稱好望角天文學家有發現，接著問助手來信。具體時地、人、動作都在前四句。 |
| `no_spoiler` | PASS | `[moon001 00:00]`–`[moon008 00:44]`: 開場留下來信、光學、第二份觀測、其他編輯的問題，沒有公布後段查核結果。 |
| `one_line` | PASS | `[moon009 00:50]`、`[moon032 03:03]`、`[moon056 05:32]`、`[moon079 07:49]`、`[moon100 09:57]`、`[moon112 11:11]`: 順著報紙造出月球觀測的過程走到後來的反應。重印本在前後兩處用途不同，沒有完整重講同一事件。 |
| `no_toc` | PASS | `[moon008 00:44]`、`[moon030 02:49]`、`[moon059 05:50]`: 提問與「故事先安排」都講報導裡的事，不宣告影片章節或後續清單。 |
| `chapters_link` | PASS | `[moon008 00:44]`→`[moon009 00:50]`、`[moon031 02:57]`→`[moon032 03:03]`、`[moon055 05:26]`→`[moon056 05:32]`、`[moon078 07:43]`→`[moon079 07:49]`、`[moon099 09:53]`→`[moon100 09:57]`、`[moon111 11:04]`→`[moon112 11:11]`: 章首承接具體名字、物件或疑問。 |
| `open_loops` | PASS | `[moon015 01:30]`、`[moon028 02:39]`、`[moon038 03:40]`、`[moon050 04:54]`、`[moon061 06:01]`、`[moon076 07:32]`、`[moon083 08:13]`、`[moon098 09:46]`、`[moon107 10:40]`、`[moon116 11:37]`、`[moon126 12:39]`: 各段在 90 秒內有尚待後句或後段回答的問題。 |
| `payoffs` | **FAIL** | `[moon104 10:23]` 問月面觀測何時能補；`[moon105 10:28]`–`[moon106 10:34]` 只說修好後當月不宜看，`[moon108 10:45]` 已轉土星，沒有給新觀測日期或明說不再有續報。`[moon121 12:08]` 再問反諷能否算支持；`[moon122 12:13]` 只重說 `[moon119 11:55]`–`[moon120 12:01]` 的判斷。開場 `[moon006 00:31]` 問能否拿出第二份觀測，`[moon118 11:48]` 僅說選錄中沒有，範圍也較窄。 |
| `no_recap` | **FAIL** | `[moon019 01:52]` 和 `[moon112 11:11]` 都說 1859 年重印本；`[moon119 11:55]`–`[moon122 12:13]` 又連續重述《晚郵報》是反諷、不能算支持的判斷。 |
| `chapters_are_events` | PASS | `[moon001 00:00]`、`[moon009 00:50]`、`[moon032 03:03]`、`[moon056 05:32]`、`[moon079 07:49]`、`[moon100 09:57]`、`[moon112 11:11]`: 七個章名都表示事件或揭曉。 |
| `outro_no_next` | PASS | `[moon999a 13:33]`–`[moon999c 13:43]`: 片尾邀請查細節、看連結、訂閱，沒有預告下一集。 |
| `opening_hooks` | PASS | `[moon004 00:18]`、`[moon005 00:24]`、`[moon006 00:31]`、`[moon007 00:38]`: 場景後有四個具體、留待後段處理的疑問。 |
| `one_thread` | PASS | `[moon008 00:44]`、`[moon019 01:52]`、`[moon041 04:00]`、`[moon091 08:59]`、`[moon118 11:48]`、`[moon132 13:18]`: 始終查報紙怎樣把虛構寫成看似可核的天文觀測。 |
| `no_detour` | PASS | `[moon103 10:16]`、`[moon108 10:45]`、`[moon112 11:11]`、`[moon123 12:20]`、`[moon130 13:04]`: 火災、土星與重印本反應都推進報導的可信度問題，沒有整段岔出。 |

The strongest repair targets are the unresolved date implied by `[moon104 10:23]`, the repeated satire verdict at `[moon119 11:55]`–`[moon122 12:13]`, and the repeated 1859 reprint setup at `[moon019 01:52]`/`[moon112 11:11]`.
