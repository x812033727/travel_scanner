# S55 R8｜隔離雙盲正式合併

2026-10-20 UTC。兩位讀者各自先凍結相同 R8 劇本 SHA-256 `50b59af8177a054e5049c1b94f31cef5838deef3837aec9d7d7c916514be0269` 的 13 題答卷，再依任一讀者答是即算是的規則合併；原卷不改。

| 答卷 | SHA-256 | 是／否 |
| --- | --- | --- |
| A `r8-isolated-blind-a.json` | `b59a0abcf337a4518847605dfbab1ed25e2c3f9aa90c80c8486e958f2514550d` | 12／1 |
| B `r8-isolated-blind-b.json` | `75ec3e9a09f25e2cee79aee3a39ad09cea82d5f6b3c2770c4c95c01825b18a00` | 12／1 |
| 正式 OR `r8-isolated-merged-answers.json` | `bb5d05585c1216057792c369e3296363ec028908da2bec5a404b07fddf7c977c` | **12／1，FAIL** |

兩人都判 `no_recap` 否。A 指 `s55097`／`s55099` 重提進火口目的、`s55090`／`s55091` 重複轉場和 `s55045`／`s55100` 重提加熱原理；B 指 `s55062`／`s55089` 重複繩索距離、`s55131`／`s55133` 重複乘員平安。各自原卷保留具體依據。其他 12 題按正式規則均是。

實跑 `VIDEO_WORKDIR=/tmp/curio-s55-r8-official NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s55 --answers /workspace/travel_scanner/docs/videos/curio-s55/review/r8-isolated-merged-answers.json --json`，退出碼 1；原始 `r8-isolated-cli-receipt.json` SHA-256 `9aa1d9fb0c6a4190a5dfb1a9f928c9f3ed76ba64b09dd7ba0c3d46e6383fe56d`，`passed:false`、唯一 `failed` 是 `no_recap`、`advisory:[]`。

R8 獨立史料與書面畫面另已 PASS；敘事仍 **HOLD**。作者應窄幅刪除重複句與重述，重凍結後再由新讀者及獨立史料覆核。尚未進入 TTS、圖片或成片。
