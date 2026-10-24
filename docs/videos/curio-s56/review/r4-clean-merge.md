# S56 R4｜無歷史脈絡雙盲正式合併

2026-10-20 UTC。兩名讀者用 `fork_turns:none` 各自從空白對話讀同一份 R4 劇本與官方 13 題，不在投票前讀先前審核或對方答卷。劇本 SHA-256 `b76995caa74f0a1f65b068d9e115659d7c48678600b80e9ff502e641a6505152` 前後未變。先前繼承上層對話的 R4 雙人答卷保留作歷史參考，不列入這次正式判斷。

| 答卷 | SHA-256 | 是／否 |
| --- | --- | --- |
| 無背景 A `r4-clean-blind-a.json` | `8d131dda4e220469370b0054b7ae892a4a189d5638b42a6f9dd0303f1b14da09` | 10／3 |
| 無背景 B `r4-clean-blind-b.json` | `6ca44fe6039d5c722c872ea17fe01f34a7f7d78fe2e7b8977ea10eac2d74b667` | 11／2 |
| 正式 OR `r4-clean-merged-answers.json` | `20e68ba688274e6f1c107a62ab9cc7177745de7ec3b3658b2f0b4fdfc431930e` | **12／1，FAIL** |

B 的原卷採 `{answers:{id:boolean},evidence:{id:string}}` 結構，合併時只將其兩欄配成 CLI 所需的 `{id,yes,evidence}`；原卷未改。兩人共同判 `no_recap` 否：A 指 `s56166–s56167` 再說下雨以及 `s56058–s56059` 重複教堂屋頂，B 的原卷另列其他重述。A 的 `no_spoiler`、`no_detour` 否票及 B 的 `payoffs` 否票依 OR 規則通過，但仍留在原卷供修稿參考。

實跑 `VIDEO_WORKDIR=/tmp/curio-s56-r4-clean-official NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s56 --answers /workspace/travel_scanner/docs/videos/curio-s56/review/r4-clean-merged-answers.json --json`，退出碼 1；原始 `r4-clean-cli-receipt.json` SHA-256 `6c2381d575198914bb08cb96a5c4863cd55040211976676bcdb6844d0b5f36a7`，`passed:false`，唯一 `failed` 為 `no_recap`，`advisory:[]`。

R4 史料／書面畫面與 Jev 政策原先通過，首輪 TTS 與定點重配的音訊也已保存，但敘事正式 **HOLD**；音訊複查仍屬 R4 草稿。作者修正重述後須重做來源及兩名無背景讀者審核，新稿通過才處理舊稿音訊的沿用或重錄。
