# S56 R9｜乾淨雙讀者正式敘事合併（HOLD）

2026-10-20 UTC。這次合併只適用於 [R9 作者凍結](r9-author-fix.md)：`script.md` SHA-256 `2679f45e2c775e3554ff55896d852f1ae95d9dba9489fd319d2bc15f72c0f0ed`、`video.json` SHA-256 `645c8c505f840393b3401c4746896a015da081a4ca6027d25ed1378f9ca4834d`。正式命令前五檔 SHA-256 都與作者表相同。[R9 獨立史料及書面畫面覆核](r9-source-independent.md)在同一組雜湊上判 **HOLD**；其檔案 SHA-256 是 `42a504abe79d0511195848bbeddebdccb4b0a87974497392bee42c363d8d61cc`。

| 獨立讀者答卷 | SHA-256 | 是／否 | 否票 |
| --- | --- | ---: | --- |
| [A 答卷](r9-clean-blind-a/ballot.json) | `471f07d68e53058762e224400020ae4136e45a02387a9ece1047080c9b782a3e` | 11／2 | `no_recap`、`no_detour` |
| [B 答卷](r9-clean-blind-b/ballot.json) | `b0fa159576ae941e901ab74f205fec15d49589577b7f581e2e70b1f25c06b648` | 9／4 | `one_line`、`no_toc`、`no_recap`、`no_detour` |
| [逐題 OR 合併答卷](r9-clean-merged-answers.json) | `6831e3bb4ae07aaed0aead844c383a307bfe6d2d1ea27c53e27711434b28b8a1` | **11／2** | **`no_recap`、`no_detour`** |

兩讀者的個別 [A 收據](r9-clean-blind-a/receipt.md)與[B 收據](r9-clean-blind-b/receipt.md)均記載同一 R9 劇本雜湊及各自 CLI 退出碼 1。A 的 yes 使 `one_line` 和 `no_toc` 按 OR 通過；兩人都對必答 `no_recap`、`no_detour` 投 no。A 指向片尾 `s56174` 重述既有事實，以及草地避難段與開場問題的距離；B 指向 `s56027–s56028` 重提北側住處，以及草地避難的多個動作。這些是獨立敘事判斷，不代替史料覆核。

逐一比對兩卷的 **34** 個 `[ID]` 引句與凍結 `video.json`：**33 個精確相同**。A 的 `open_loops` 把「前面的商業區能擋住火嗎？」標成 `[s56091]`，該句實際是 `s56092`；原卷保留不改。正式合併 `open_loops` 的 yes 使用 B 的精確 `s56165` 引句；其餘合併答覆各取一個原卷中的精確口說引句，**13／13** 均可對回凍結劇本。此引句 ID 錯誤沒有讓任何 OR 否票變成是票。選句及異常見 [機器稽核](r9-clean-merge.json)。

正式執行 `VIDEO_WORKDIR=/tmp/s56-r9-official-merge NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r9-clean-merged-answers.json --json`，出口碼 **1**。[原樣 CLI 回條](r9-clean-cli-receipt.json) SHA-256 `01ff76d812a7a2e3015e6c1d201a3770e0d5d06e651e146c28a20fe134f46df6`：`passed:false`、`failed:[no_recap,no_detour]`、`advisory:[]`。隔離目錄的正式紀錄 `/tmp/s56-r9-official-merge/curio-s56/review/narrative.json` SHA-256 `4d08fd9ee57d07c49a0d24a13a4d233280e63908d1e54c7fd4befecdae815c63`，`round=1`、`narrative_hash=22460011c9b90017`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

來源 HOLD 另指出 `s56155` 的西南方位未獲原文支持、`s56061` 的人物撤出動作未見於家書，以及 `s56173`、`s56174`、`s56176` 畫面提示的時間或位置線索不符記錄。**R9 來源與敘事關卡均 HOLD**；[政策停點](r9-policy.md)記錄未送 Jev。R10 若修稿，必須使用新凍結雜湊及新獨立關卡，不能沿用這次答卷。
