# X13 Spotify｜兩支 Shorts 9:16 逐拍構圖計畫 v12

這是**尚未生成畫面**的原生直式重構規格，不是裁切或手機 QA 通過收據。每拍 `shot` 均須是長片真正的 `shot` 影格；兩張長片 `stats` 不送入 Shorts 影格管線。數字由 Shorts `big` 欄位在 1080×1920 直式卡原生排字，場景底圖另取有效的匿名插畫。編譯器直接呼叫 `episodeShortsProblems(shorts, video)` 防止再引用 `stats`。

每拍有效插畫先從 1920×1080 取 x=656–1264 的 608×1080 中央窗，再重排為 1080×1920。Short 1 關閉音訊格與開放影片格以兩個不同中央架位呈現，不畫成同一檔節目轉型；Short 2 廣告與會員帳本上下堆疊，先後鏡頭保持同一色序。Shorts 卡片工具原生文字內容區 x=80–900、y=258–1378；可關閉繁中字幕區 x=80–900、y=1430–1595；片尾控制區 y≥1640 不放關鍵字。每拍在 360px 寬手機畫面檢查臉、手、主物、字與控制列不互相遮擋。

兩張原生數字卡：Short 1 第 1 拍以 `x130401` 的有效匿名內容架插畫作背景，`headline` 為「部分內容沖銷」、`big` 為 **€30m**，47px `body` 放「2023 Q2｜部分播客內容資產」，`note` 放 S3 SEC 及非全體範圍；先留下是否全面退出的問題。Short 2 第 1 拍以 `x130611` 的有效服務帳插畫作背景，`headline` 為「廣告欄播客成本」、`big` 為 **−€21m**，47px `body` 放「2025 Q2 同比｜Ad-Supported」，`note` 放 S7 SEC 與非全平台總支出範圍；第一句旁白說明廣告欄同比變動，不提前回答『真省』或 Premium 搬移。`big` 用 Shorts 工具的 168px 字級、`headline` 88px；`note` 28px 只輔助來源，關鍵口徑另由頭條與旁白交代。原生排字後仍須以 360px 畫面實測可讀性。

| Short／拍 | 長片有效 shot | 焦點／內容（直接取自來源鏡頭提示） | 橫版 x 起點 | 直式原生頭條／大數字 |
| --- | --- | --- | ---: | --- |
| 1/1 | `x13-b04-s01` | Overhead shot, tilt down along a content-catalog aisle, a broad anonymous content-portfolio shelf opens in the central frame, with separate blank audio tiles and no identifiable program | 656 | 部分內容沖銷／**€30m** |
| 1/2 | `x13-b04-s05` | Close-up, pull out along a content-catalog aisle, several generic unmarked audio slots close in the central frame, with no show name or cover art | 656 | 若干節目關閉 |
| 1/3 | `x13-b04-s06` | Wide shot, gentle pan left along a content-catalog aisle, a public notice with no readable lettering faces anonymous closed audio slots, all in the central crop | 656 | 全面退場？ |
| 1/4 | `x13-b04-s08` | Medium close-up, pan right along a content-catalog aisle, closed audio slots and open video catalog tiles stack vertically, never implying they are the same program | 656 | 影片供給仍在 |
| 1/5 | `x13-b04-s13` | Overhead shot, tilt down along a content-catalog aisle, an illustrative listener sets a generic closed-audio notice next to a distinct open-video catalog card, without identifying a show | 656 | 不同內容 |
| 1/6 | `x13-b06-s01` | Low-angle shot, lift gently inside a quiet video studio facing a living area, the previously blank video-entry tile from the opening meets a new generic creator-program doorway, with no identifiable show | 656 | 新方案啟動 |
| 1/7 | `x13-b06-s03` | Close-up, pull out inside a quiet video studio facing a living area, an eligible anonymous video creator receives an unmarked view-based payment token in the center | 656 | 合格創作者 |
| 1/8 | `x13-b06-s06` | Medium close-up, pan right inside a quiet video studio facing a living area, a Premium member watches an unbranded blank video tile without an ad interruption symbol, centered | 656 | 會員觀看 |
| 1/9 | `x13-b06-s18` | Medium close-up, pan right inside a quiet video studio facing a living area, a new anonymous creator records video while a different member presses play, both inside a central vertical composition | 656 | 並未全面退出 |
| 2/1 | `x13-b06-s11` | Overhead shot, tilt down inside a quiet video studio facing a living area, a lighter green advertising podcast-cost card sits over an unopened orange member card in the central frame | 656 | 廣告欄播客成本／**−€21m** |
| 2/2 | `x13-b06-s08` | Medium shot, push in inside a quiet video studio facing a living area, an unassigned new video cost token waits between vertically stacked green and orange service lanes | 656 | 真省多少？ |
| 2/3 | `x13-b06-s03` | Close-up, pull out inside a quiet video studio facing a living area, an eligible anonymous video creator receives an unmarked view-based payment token in the center | 656 | 合格影片 |
| 2/4 | `x13-b06-s06` | Medium close-up, pan right inside a quiet video studio facing a living area, a Premium member watches an unbranded blank video tile without an ad interruption symbol, centered | 656 | Premium 會員 |
| 2/5 | `x13-b06-s12` | Medium close-up, pan right inside a quiet video studio facing a living area, only a limited new video experience cost token moves into the orange member lane, both lanes vertically stacked | 656 | 成本換欄 |
| 2/6 | `x13-b06-s14` | Medium shot, push in inside a quiet video studio facing a living area, a blank unknown-transfer cell rests between vertically stacked green and orange cost lanes | 656 | 拆分未知 |
| 2/7 | `x13-b06-s15` | Close-up, pull out inside a quiet video studio facing a living area, an analyst removes an unsupported all-service savings sticker from a smaller green account | 656 | 不能全算省下 |

Short 1 的九拍從部分內容縮編追到新影片合作，Short 2 的七拍解釋費用分類和不能全算節省。兩支各需正式 TTS 實測 25–55 秒、重新排版文字／CC、核 9:16 真圖與音樂授權；不得以這份紙面規格冒稱成片。
