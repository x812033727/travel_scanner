# S56 R8｜乾淨雙讀者正式敘事合併（HOLD）

2026-10-20 UTC。這次合併只適用於 [R8 作者凍結](r8-author-fix.md)：`script.md` SHA-256 `4ffefbfd2310bdca453a331001c2c61c385f4ef43d7ca85316079a17d8924b00`、`video.json` SHA-256 `543054261039a1ecb8c38bccc93b3a48cd77a02a361a2f1f57084ef772470690`。正式合併前五檔 SHA-256 均與作者表及 [R8 獨立史料、主張與書面畫面 PASS](r8-source-independent.md)一致；來源覆核檔 SHA-256 `949dfb27a308c278f32e14eb1d754facd73a3b824353d0752ebd720d88b50d95`。

| 獨立讀者答卷 | SHA-256 | 是／否 | 否票 |
| --- | --- | ---: | --- |
| [A 答卷](r8-clean-blind-a/narrative-answers.json) | `9541d94233e062b0ad6c4c3ec3e8e19153cbcb94f7c99fa3e482bddb7c2ff113` | 10／3 | `payoffs`、`no_recap`、`no_detour` |
| [B 答卷](r8-clean-blind-b/narrative-answers.json) | `2923df8a73555c52afc61e933968a724c464e4bde1519feb124ab5afbc410354` | 12／1 | `no_detour` |
| [逐題 OR 合併答卷](r8-clean-merged-answers.json) | `4501d5d23941bc64772572a604e9bb9d47493cc3644929bc256a1ad73f2c3d44` | **12／1** | **`no_detour`** |

兩讀者各自凍結 R8 劇本票，並留下個別正式紀錄：[A](r8-clean-blind-a/narrative-cli-receipt.json)、[B](r8-clean-blind-b/narrative-cli-receipt.json)。B 對 `payoffs` 和 `no_recap` 的 yes 使這兩題依 OR 通過；兩人都在必答 `no_detour` 投 no。A 指出草地避難準備段偏離開場問題；B 指出 `[s56175] 兩份私人記錄都沒找出十月八日最初點火者。` 將片尾帶向起火者，與追蹤河道及避難界線的主線不連續。

答卷引句稽核是 **25／26** 句與當時凍結 `video.json` 完全一致。A 的 `no_detour` 答卷把「洛許自己也被分去拔籬柱，手都磨傷了。」標成 `[s56163]`；該口說實際是 `s56162`，`s56163` 是井水與浸衣備案。保留 A 原卷及其否票，沒有暗改。正式合併的 `no_detour` 引句採 B 的精確 `s56175`；合併答卷 **13／13 引句**均與凍結口說一致。這個 A 引句 ID 錯誤不改變雙讀者的 `no_detour=no` 或 OR 結果。

正式執行 `VIDEO_WORKDIR=/tmp/s56-r8-official-merge NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r8-clean-merged-answers.json --json`，出口碼 **1**。[原樣 CLI 回條](r8-clean-cli-receipt.json) SHA-256 `a25d76793a6d5e1a89c741741b75edeb439c9842b1c34d58dc4f21610b023ca8`：`passed:false`、`failed:[no_detour]`、`advisory:[]`。正式紀錄 `/tmp/s56-r8-official-merge/curio-s56/review/narrative.json` SHA-256 `f34de845d3d64664f63af83cefa2967abc8924be1ff9038ff1333893b02b16e0`，`round=1`、`narrative_hash=442f1009de84b004`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。完整輸入、答卷與命令稽核在 [機器回條](r8-clean-merge.json)。

**R8 敘事關卡 HOLD。** [政策停點](r8-policy.md)記錄本任務未送 Jev。R9 若刪改 `s56175`，須以新的凍結劇本重過獨立史料、乾淨盲評與正式合併；本票不涵蓋 R9。
