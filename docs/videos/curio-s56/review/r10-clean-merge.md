# S56 R10｜乾淨雙讀者正式敘事合併（HOLD）

2026-10-20 UTC。這次合併只適用於 [R10 作者凍結](r10-author-fix.md)的五檔：`brief.md` `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52`、`research.md` `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7`、`claims.md` `4fc2b9887afe5805340c553d7c099658ce5231d8f27b836c621842477f14a172`、`video.json` `e54a6dfde678a536e81eac36c13360782e5e1efad6c2c30c694cefc5e01098f8`、`script.md` `286b7d50bc21ee8c8c5f61d99a3744f988ca1cbdac2c80bef05237a74f585153`。正式命令前五檔 SHA-256 均與作者表相同。[R10 獨立史料及書面畫面覆核](r10-source-independent.md)對同組雜湊判 **HOLD**；報告 SHA-256 `31d6f128b8c4ee62ba13aee71a1a8180133cf10fbdc0be9144cbfaee664bded1`。

| 獨立讀者答卷 | SHA-256 | 是／否 | 否票 |
| --- | --- | ---: | --- |
| [A 答卷](r10-clean-blind-a/ballot.json) | `5d1db05ae8ae82f65915710545ff543cde0b3cf09fbe6aab5d59a9d3b3c8ada2` | 12／1 | `no_recap` |
| [B 答卷](r10-clean-blind-b/narrative-answers.json) | `df04c534fbf5462f96ba559c97280e86343d8e028d9ee7b1a29b36530c80a812` | 12／1 | `no_recap` |
| [逐題 OR 合併答卷](r10-clean-merged-answers.json) | `3b5cb9ef75c0b6ae97a0754d27b35b0cb75844246774693b36c2f03a364e1815` | **12／1** | **`no_recap`** |

兩讀者各自的官方 CLI 收據在 [A](r10-clean-blind-a/cli.stdout.json) 與 [B](r10-clean-blind-b/narrative-cli.stdout.json) 目錄，退出碼均為 1；兩份獨立敘事紀錄與正式合併紀錄的 R10 敘事雜湊、劇本綁定、panel 規則及口說雜湊相同。兩人都指出 `[s56174] 西岸大火隨後越河，與東岸新火連成一片。` 重複正文 `[s56079] 他寫，西岸大火後來過河，與東岸新起的火連成一片。`，故必答 `no_recap` 仍是 no。

逐一比對兩卷的 **26** 個 `[ID]` 引句與凍結 `video.json`：**25 個精確相同**。A 的 `scene_first` 將「他才從西側走過橋，想把烈火留在身後。」標成 `[s56002]`，實際 ID 是 `s56003`；原卷保留不改。合併答卷的 `scene_first` 使用 B 的精確 `s56001` 引句，共同 no 票也用 B 的精確引句；其他 11 個 yes 答覆取 A 的精確引句。合併答卷 **13／13** 引句均對回凍結口說，沒有改動任何票。選句與異常詳見 [機器稽核](r10-clean-merge.json)。

正式執行 `VIDEO_WORKDIR=/tmp/s56-r10-official-merge NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r10-clean-merged-answers.json --json`，出口碼 **1**。[原樣 CLI 回條](r10-clean-cli-receipt.json) SHA-256 `86eaefda354aad670e9bc7ac14e391a2736772061dccb70d97edcc1e84eebe6c`：`passed:false`、`failed:[no_recap]`、`advisory:[]`。隔離目錄正式紀錄 `/tmp/s56-r10-official-merge/curio-s56/review/narrative.json` SHA-256 `2fbbfa5d9fd64487a5e7d0238acec9bf8ec915732a9c01f710a1a7d1d40491d3`，`round=1`、`narrative_hash=1f5f1f43a62d7609`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

來源 HOLD 另指出 `s56112` 的「催車」動作未見於 Foster 信，開場 `s56011`、`s56013` 畫面過早出現後來才打包的小箱。**R10 來源與敘事關卡均 HOLD**；[政策停點](r10-policy.md)記錄未送 Jev。後續修稿須用新凍結雜湊和新獨立關卡，不能沿用本輪票。
