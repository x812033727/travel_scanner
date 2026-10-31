# S49 R23｜兩景首試：moon030 保留、moon031 服務逾時停畫

2026-10-22 UTC。[R23 獨立書審](r23-moon030-031-prompt-independent.md)以精確檔 PASS 後，只執行 `keyframes --slug curio-s49 --shot moon030,moon031 --takes 1` 一次；`STOP` 由 EXIT trap 暫移並已恢復。MiniMax 回來一張新原圖，第二景工作逾時失敗，CLI exit **1**。沒有重試、沒有開下一批，也沒有把舊 `moon031` 圖冒充新版。

| 景 | 1280×720 新原圖／機器 | 原圖直接判斷 |
| --- | --- | --- |
| `moon030` | SHA-256 `5a5862db7308…`；judge **10/10 PASS**；manifest 直接選原圖，沒有裁切。 | **KEEP**：成年舊式學者在無字紙上畫分開的兩個圓；沒有真望遠鏡或三腳架，也沒有上下黑邊。紙有中間折線，略像攤開的兩頁，但仍是泛用空白紙的卡通示意，不冒充可核原設計；不因這一點重畫。 |
| `moon031` | MiniMax job `9f0ba914-f619-43b7-b27d-7d3f6445089f` 回 `video_media_upstream_failed`／`ReadTimeout`；**未得到 R23 圖，也未進評審**。 | **HOLD**：新 manifest 記 `takes: []`、`needs_review: true`、無選圖。舊 R22 圖和預備副本仍在磁碟，不能因其檔案存在而當新稿可用。待服務穩定後，按同一 R23 提示詞只補這一景的一張；原圖須再驗有無偽文字／立體器材。 |

[完整新舊 SHA、judge、帳本與圖單清單](r23-moon030-031-native-inventory.json)已保存。付費前私有備份在 `/workspace/.video-work/curio-s49/review/r23-moon030-031-pre/`，含 manifest、ledger、兩張 R22 原圖／裁圖及此前 **25 張 KEEP** 的圖單項目與檔案 SHA。批後逐一重算，這 25 項與選圖檔 **全部不變**。圖單 SHA-256 `29fd2d89…` → `735fcfca…`，帳本 SHA-256 `de005bd1…` → `d79d5a39…`，`STOP` 仍存在。

帳本由 **US$0.9720／72 image entries／72 judge** 到 **US$0.9855／74 image entries／73 judge**，淨 US$0.0135：`moon030` 一張 US$0.0035 加一評審 US$0.01；`moon031` 失敗 job 作一筆 image entry，費用 **US$0**，沒有評審、預約或額外收費。仍低於整集 US$5.30 上限。CLI 因瀏覽器版本缺口另報未產生 contact sheet；這不影響已保存的原生 JPEG 或本次直接原圖判斷，但 contact sheet 在分鏡前仍須補。

劇本未動。首章仍有 `moon031` 未通過，全片 121 張插圖亦未完成；不能送全片 storyboard 或宣告影片完成。網站 outline／script／audio 卡及人耳審查等後續關卡仍待完成。
