# S61 R7｜作者窄幅敘事與引文修訂交接

2026-10-22 UTC。**R7 是作者候選，尚未經本版獨立史料／書面畫面覆核或全新正式雙盲放行；本收據不是審核票。** R6 [獨立史料／畫面覆核](r6-independent-source-visual.md) PASS；兩名正式隔離盲讀各 11／13， [OR 合併](r6-formal-merge-audit.md) 12／13 HOLD，共同 No 僅 `no_recap`。本次沒有 TTS、圖片、音樂、成片、上傳或付費評審。

## R6→R7 修訂

- `s61028` 保留瓦礫阻路，`s61031` 改為消防員在首爆後很快回應全城警報、隊伍一度仍有組織，直連 Prince L1963–1968；`s61034` 接著交代教堂、學校與工廠被北區火勢捲入，直連 L924–937，不再重講消防指揮空缺。
- `s61054` 說另有整支隊伍志願處理火藥庫，`s61055` 才依 Prince L1832–1834 指出他稱之為砲兵隊且未記軍種或下令者，`s61057` 只交代灌水動作；`s61061` 仍保留消防員面對第二次警報卻留守的後續。自願隊伍不冠海軍身分，海軍造船廠只修飾火藥庫所在地。
- `s61059` 的重述卡片改為 Prince L931–937 所記消防員知道傷者受困瓦礫，形成 `s61060–61` 市政官員接手指揮、消防員留守的直接理由。卡片只寫北區火場與待救者，不畫可識別傷者。
- 開場 `s61005` 留下傷者能否等到搜救的問題，不先洩露救援工具放下及消防員留守；`s61113` 把「公地之後何處避寒」交給 `s61081` 白帳回收，避免已抵公地後再問同一停靠處。`loops` 的砲兵隊身份回收點同步改到 `s61055`。
- `claims.md` 為 `s61008` 增補 Prince 自述參與救援的 L766–773 直連，為 `s61026` 增補破木板在 L1363–1370 的直連；旁白未藉此增加無根據內容。`s61130` 仍是「有人跑向店鋪；店裡的人則趕回家」，維持兩群人分開。

## 固定檔案與可逆差異

| 檔案 | R7 SHA-256 |
| --- | --- |
| `brief.md` | `ef67f56b4d384015edc9eeaea3640946ff0c4c9b778a2a587adb190c43004a65` |
| `research.md` | `3da127b6e386cfc1e67808688102124931715e75d3f5db18b38cdfda4fcc3203` |
| `video.json` | `1916964aeb68e2586c697eff5cedd61999a9c3088890f4f0ba78c1c1d694fb8e` |
| `script.md` | `9ac6972f9c3e27dd67ba11e3eb7f621da71a2c72d58b81d3c9f4dddbaa9ee4d5` |
| `claims.md` | `33283abb5ac43f98947deed544e41c730d5cbe1a1f717390a761cdcd38c65d8d` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `9e9ce88e15db56d4fadb8ec25df08a8b4f40d7d419e98a66ed0fbf943c8c7404` |
| [r7-author-delta.json](r7-author-delta.json) | `da5b1897f118184d4664fdc92b98d9d6c179a0bff1e89ea9f53a15f72e6abffd` |

[r7-author-delta.json](r7-author-delta.json) 保存六檔 R6 PR 固定版到 R7 的逐塊舊／新行、零起算座標與 SHA，已驗證正向重放及反向還原。基準六檔在 `/tmp/s61-r6-pr-frozen/`；其中任務票為根工作者已補記 R6 獨立與正式雙盲結果的 PR 版，SHA `207841138653d82bc4381b6ffd20b2cd88944cec0e22aa9ce22bd718a1bc56bf`。固定史料仍是 GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`，原文 SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。

## 作者機械檢查

重新產生 `script.md` 後，`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json` 為 **0 errors、0 warnings**；106 句（含 3 句品牌片尾）、六章、20 組 `loops`、96 幅插圖鏡頭與 7 張資訊卡。逐字比對 103／103 個非片尾鏡頭的 `video.json` 與 `claims.md` 旁白，96／96 幅提示詞及 7／7 卡片文字對齊。以 325 字／分鐘，濃縮開場 **48.23 秒**，開場後到品牌片尾前的正文 **486.57 秒（8 分 6.57 秒）**；以 250 字／分鐘，開場 59.53 秒、正文 604.00 秒。`npm run check:tasks` 驗證 2,094 份任務檔；跨任務範圍和舊認領警告屬既有項目。

**下一步：**請全新獨立工作者在上述固定 SHA 上覆核全部史料與書面畫面；另由兩名未看舊票的隔離讀者先取得正式 13 題，再獨立盲讀並合併。R6 PASS 不自動移轉到 R7，媒體與站主實聽仍待核准。
