# S49 R24｜`moon031` 字卡的私人圖單離線重綁

2026-10-22 UTC。**首章既收圖綁定 PASS；全片 storyboard 仍 HOLD。**R24 的[來源字卡獨立紙審](r24-moon031-source-card-independent.md)已通過；本回只清除私人圖單對 R23 退件圖的引用，沒有生圖、judge、音樂或其他付費呼叫。

## 綁定依據與操作

R24 `video.json` SHA-256 `98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c`。以[可逆差分](r24-moon031-source-card-structured-diff.json)逐字還原的 R23 檔案 SHA 為 `fb144f9e2af0b6c59b08c477a149b21af6291af8b0b328934d96d87e1c3fe0b8`；除 `moon031` 的 `shot → big` 外，其他場景物件逐項相等。工具的 `visualHash` 對還原 R23 計得 `30fd88199d433154`，恰等於舊圖單的 `visual_hash`。**S49 是 `format: drama`，此 manifest 使用 `visual_hash`，不是 `pictures_hash`。**R24 新值是 `30ca7d69acc3fc9a`；現行 `look_hash` `98a370ae40badbaf` 未變。

`STOP` 在位時，CLI `keyframes --slug curio-s49 --shot moon030 --takes 1` 以 exit 6 在寫入前停止。故以離線、原子方式保存舊圖單備份 `/workspace/.video-work/curio-s49/rebind-backups/r23-manifest-before-r24-card.json`（SHA-256 `0407c0e6ac63aa6e5d394aecbd2ed9963ccf01a33babd1da015f764105e65b48`），只將 manifest 的 `visual_hash` 換為 R24 值並刪除 `shots.moon031`。新 manifest SHA-256 `4f40a7ad117ed6393b4fea39e4cfbd206ee0312b1c6c9b25ba8e3bc48e72c611`，權限維持 `600`。其餘 **26 個 shot 條目與備份逐項 JSON 相等**；縮圖來源仍是已收的 `moon006`。舊圖單的 contact sheet 原本就是 `null`／空清單，沒有需要刪除的展示引用；原退件 JPEG 留在私人工作區作證據，但新 manifest 內沒有 `moon031` 或其路徑。

## 輸出與費用驗證

`shotScenes(R24)` 為 120 景且不含 `moon031`；全場景 128 景中該景現在是 `template: big`。以工具 `renderPlan` 的只讀結果核對，`moon031` 輸出為一張 `stills` 字卡，畫面文字包含「1835 年虛構報導／鏡筒重三千磅／1859 重印本所載，非器材紀錄」，HTML 不引用退件的 `moon031-1-trim.jpg`。對 26 張留存景執行 `keyframeProblems` 得 **0 問題**，每張被選檔案的實際 SHA 均符合 manifest；對完整 R24 執行同一檢查仍有 **94 張未畫景**，沒有 `moon031` 缺圖或退圖錯誤。`lint --slug curio-s49 --json` exit 0、0 errors／0 warnings、131 lines。

私人 ledger SHA-256 仍為 `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，即 **US$0.9990／74 image／74 judge／0 reservations**，小於整集 US$5.30 上限；jobs 空、`STOP` 仍在位。後續可逐章紙審與限額畫其餘景；完整 storyboard、網站卡、人耳旁白、長短片與 Studio 連結均尚待完成。
