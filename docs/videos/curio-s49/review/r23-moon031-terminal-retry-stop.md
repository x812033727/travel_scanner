# S49 R23｜`moon031` 逾時工作終結後單景重試停線

2026-10-22 UTC。R23 [前一輪原生停線](r23-moon030-031-native-stop.md)中，`moon031` 的 MiniMax 工作 `9f0ba914-f619-43b7-b27d-7d3f6445089f` 在本機帳本明確為 `failed`／`video_media_upstream_failed`、費用 US$0；`media/jobs.json` 為空、預約 0、私有 STOP 在位，manifest 該景 `takes: []` 且無 R23 選圖。工具在[服務端終止狀態](../../../../tools/video/media/stages.mjs)才會把這種失敗寫入帳本、清掉待續 job；沒有 `video_media_outcome_uncertain`。R23 創作檔雜湊未變、US$0.9855 + 單圖／judge 約 US$0.0135 低於 US$5.30 整集上限；確認沒有其他 `keyframes` 進程後，才在 EXIT trap 保護下暫移 STOP，**僅執行 `keyframes --slug curio-s49 --shot moon031 --takes 1` 一次**。

CLI exit **0**，同一服務端 job ID `9f0ba914-f619-43b7-b27d-7d3f6445089f` 由先前的零費失敗列改為 `ready` US$0.0035；再做一次 judge US$0.01，沒有第二個 image job。這是同一請求鍵 `ec0b29f821f49b70` 的終態回收，並非雙重計費。完整[帳本、圖單、原圖／裁圖雜湊清單](r23-moon031-terminal-retry-inventory.json) SHA-256 `7be91b6278f97d058ff48c45cbc35ff9d23dfeeb9c0b1aad463652dd876e9434`；私有前後快照在 `/workspace/.video-work/curio-s49/review/r23-moon031-retry-pre/` 與 `r23-moon031-retry-post/`，CLI stdout／stderr／exit 同處保存。

| 景 | 原圖／機器 | 直接開原圖與裁圖的結論 |
| --- | --- | --- |
| `moon031` | 1280×720 未裁 JPEG SHA-256 `6bace6550be430b9e0068b13f226121fd4b284c6910694edb633d1435203588c`；所選裁圖 SHA-256 `1c08ed80e1eb60378322ab5e3806dad5068ebaecc4719f657ba2ec3837451e94`；judge **9.29 PASS**，其 `details` 題已指出符號形狀不符。 | **人工 REJECT**：畫中有成年、舊式衣著的讀者，沒有實體圓筒、密集偽報紙印字或黑邊；但人物旁是似字母的曲線、點和底線，並非指定的空心平面鏡筒輪廓，畫面也未使「文章聲稱鏡筒重三千磅」變得可辨。裁邊後這個無意義近似字形仍在。不能只因機器總分通過而當作合格 `moon031` 圖。 |

帳本由 **US$0.9855／74 image entries／73 judges** 至 **US$0.9990／74 image entries／74 judges**，淨 US$0.0135，0 reservations；失敗 job 原列被同 ID 成功結果取代，故 image entries 數沒有增加。manifest 只有 `moon031` 一景的條目變動，先前 25 張 KEEP 及 R23 `moon030` 的合計 **26 張** manifest 條目與實際所選圖片 SHA 都未變。當前 manifest SHA-256 `0407c0e6ac63aa6e5d394aecbd2ed9963ccf01a33babd1da015f764105e65b48`，ledger SHA-256 `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`；STOP 已恢復，jobs 無待續。CLI 仍因 Playwright Chromium 版本缺口未產生 contact sheet，這不影響逐張原圖檢視。

**下一步：**本輪不再重畫。`moon031` 已有 R22 偽原報／立體道具退件及本次平面符號失形退件；由作者決定只對這景做窄提示詞修訂，或按系列規則評估同章已收圖重用／來源明確的資訊卡，保住全片插圖比例與卡片間距，再交另一人獨立紙審。R23 `video.json` SHA-256 `fb144f9e2af0b6c59b08c477a149b21af6291af8b0b328934d96d87e1c3fe0b8`、`claims.md` `0071e502905c7669a6bfb70c406921d52e82d5fa54a3e4c8ffd75240eb157809`、`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` 未改。首章與全片 storyboard 仍 HOLD；沒有核准語音、音樂、成片或 Studio 連結。
