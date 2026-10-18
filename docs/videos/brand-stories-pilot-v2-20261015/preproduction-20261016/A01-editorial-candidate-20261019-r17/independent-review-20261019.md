# A01 r17 獨立限縮審查 — HOLD

- 審查日期：2026-10-19。
- 審查對象：`A01-editorial-candidate-20261019-r17/manifest.json`，SHA-256 `F0603AC804089797BDD1C083EE006306618D19D67B58E621058DB026EEE02805`。
- 結果：P0 0、P1 0、P2 3。這是離線編輯候選的審查，不是正式劇本核准或主機安裝授權。

## 已核對

- 逐項比較 r16→r17：第 53 鏡的插畫拿掉未證實的 `late-1980s` 年份；第 56 鏡把清單式回顧改成郵購與 1993 年零售節拍；`n60`、`n64`、`n65`、`n66`、`n67` 從該鏡及主張表移除。其餘鏡頭、台詞 ID、章序、畫面類型與鉤子的 setup/payoff ID 未變。第 53 鏡所引 [2010 年《紐約時報》文章於 RNPA 第 199 期第 48 頁的重印](https://northwestairlineshistory.org/wp-content/uploads/2025/12/Contrails-199-Aug2016.pdf)沒有為旅客目擊空服員的畫面標年份。
- [Judi Dash 1993 年《洛杉磯時報》原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)支持 Travelpro 起初郵購、四家受測品牌，以及主要百貨**或**行李專門店的販售通路；沒有以此推算銷量。
- [Jayne Clark 2012 年刊載的 Plath 回憶](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)記載安檢員回答 OK，沒有獨立可核對的通關結果。
- `node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r17/build.mjs --check` 通過：65 鏡、77 句、73 筆 `PENDING` 主張、18 筆公開引用；場景主張 ID、`source-map.json` 和 `source-alignment.json` 的 73 筆映射一致。`lint` 錯誤 0、可愛插畫檢查錯誤 0；`lint` 仍有 31 項警告。文字估時 434.4 秒（300 字/分）、468.9 秒（275 字/分）、508.4 秒（250 字/分），並非實際配音或成片長度。掃描未見私人主機路徑、金鑰或密碼。

## P2 修正事項

1. 第 56 鏡說「百貨已有四家品牌」比來源的「主要百貨或行李專門店」更窄，且 `n56` 只寫多個品牌，沒有直接寫四家。口播及 `n56` 應與來源一致。
2. 第 43 鏡繼承的「安檢員會讓它過嗎？」由第 48 鏡「好」回收，容易讓聽眾以為已證實通關。史料只支持安檢員的回話；應問他會如何回答。
3. `validation.json` 的 `plan_sources: 25` 及 README 對「25 個企劃來源」的簡寫，可能被誤認為此候選已裝入 25 筆。此候選 `candidate/series.json` 實為 23 筆；另包才有**擬採用**的 25 筆，公開 `candidate/video.json.sources` 為 18 筆。應明列三個集合。

## 未完成與界線

本審查只核對 r17 相對 r16 的改動、上述來源、映射和靜態敘事；沒有重新獨立查證全部 73 筆正式事實。73 筆仍為 `PENDING`。未實測 TTS、配音語速、剪輯長度、圖片聯絡表，也未核對正式機的六章與新主張 ID；沒有 `story/reviews/script-review.json` 正式審稿收據。保持 **HOLD**：不據此解除 STOP、寫正式機、呼叫付費媒體、合成或上傳。
