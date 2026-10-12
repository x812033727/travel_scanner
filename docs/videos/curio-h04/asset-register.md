# H04 真實文件素材登錄

2026-10-12。供已選定的 A 案整合使用。本輪只準備真實來源掃描與裁切，沒有修改 `video.json`、呼叫付費生成或核准分鏡。

三張原件與三張原生 `screenshot` 預覽均已實看；原生模板／素材存在檢查及三張預覽 layout 均無錯誤。完整機讀記錄與可直接採用的 `nativeAsset`、`nativeScene` 建議位於 `C:/Users/x8120/mokaair-work/videos/curio-h04/_audit/source-assets.json`。其中示範 `lines` 僅供模板驗證，不應覆寫作家旁白。

## 來源與權利依據

文件為 1959-05-28 結案決定書，作者是 **Лев Никитич Иванов（Lev Nikitich Ivanov）**。Commons 檔案頁標示 **PD-RU-exempt**，依據為俄羅斯官方文件的著作權豁免。這個依據不擴張到隊員照片、搜救照片或同案其他圖片。

| 頁 | Commons 檔案頁 | 原圖 URL | 原件 SHA-256 |
| --- | --- | --- | --- |
| 385 | [檔案頁](https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_385.jpg) | [原圖](https://upload.wikimedia.org/wikipedia/commons/6/6b/Dyatlov.Volume_1.Page_385.jpg) | `2f4b75198c72e72da599d671f9bb29f05f501c1f4acdb99f3dfbacd92d7cf461` |
| 386 | [檔案頁](https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_386.jpg) | [原圖](https://upload.wikimedia.org/wikipedia/commons/6/65/Dyatlov.Volume_1.Page_386.jpg) | `69a0a1057bea0eba1a1d258eadb9315e6bbba4e14788e7dc62069cc2762a519b` |
| 387 | [檔案頁](https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_387.jpg) | [原圖](https://upload.wikimedia.org/wikipedia/commons/a/ab/Dyatlov.Volume_1.Page_387.jpg) | `c4f82ff9bd2803d254ba065a913d49543be6a68b9f212d89f5069dff20a82b18` |

385／386 沿用已下載、SHA 相同的原件。387 先前 GET 429；本輪於 **2026-10-12 05:22:42 UTC** 只作一次有界 GET，得到 HTTP 200，1,017,510 bytes，並已核對實際像素。收據為 `_audit/1959-sources/page-387-fetch-receipt.json`。先前 `research-history.md` 的「387 尚未實看」是較早狀態，由本次登錄補足。

原件保存於外部 `_audit/1959-sources/case-385.jpg`、`case-386.jpg`、`case-387.jpg`。Commons 原始來源欄指向民間論壇 `http://taina.li/forum/index.php?topic=7124.msg478824#msg478824`；不得標成官方檔案館直接供圖。

## 選用區域與成片檔案

座標均以**原件左上角為 (0, 0)**，順序為 `x, y, width, height`。先解碼 JPEG，矩形裁切，存無損 PNG，再加入透明留邊。沒有 AI 重畫、換字、調色、轉正或重新取樣。已比較裁切區解碼後 RGBA，三張內容與原件對應區域相同。

| 用途 | 原件尺寸 | 裁切區域 | 透明畫布尺寸 | 原生 `data.image`（相對 workdir） |
| --- | --- | --- | --- | --- |
| 鞋子／內側切口 | 2299×3796 | `65, 2775, 2120, 465` | 2120×964 | `stock/bf338fb136401d2bb9358a7bceeb46abe20a9ee55b7bdcf263d483eb67d1963f.png` |
| 足跡 | 2290×3796 | `40, 650, 2080, 428` | 2080×946 | `stock/1c31a7da3de0851b0645f7636df4a6bc07a8252447a8ad74f98e2f9dca709b40.png` |
| 自然力量 | 2325×3796 | `484, 1475, 447, 75` | 800×364 | `stock/f90b4c557783827cfde143fb4ddfd59ae08e93b9b97a05026a9cb3e288ddf25d.png` |

`stock` 實體目錄是 `C:/Users/x8120/mokaair-work/videos/curio-h04/stock`。檔名即各輸出檔 SHA-256。未留邊的原始裁切、三張原生預覽及其 SHA 都在 `source-assets.json`，像素檔位於 `_audit/1959-sources/`。

- **385**：保留所需完整段落。多數鞋子留帳內；「突然、同時離開」是調查文件的推論。該頁提到兩處開口，與鑑定三條切口口徑不同；旁白不報切口確數。
- **386**：只保留最上方足跡段，完整排除後續遺體與傷勢段。原文八至九組，不是九組確數；不同鞋襪印不能呈現成九人全赤腳。原文約 500 公尺不與證人約 50 公尺合成一條完整足跡。
- **387**：只保留 **стихийная сила** 原文關鍵詞，繁中 caption 為「自然力量」。這不是完整段落；沒有展示上方傷勢及驗屍前提。原件行距窄、略斜，頂邊有極少相鄰行墨跡，保留真實像素，不補字或抹字。這句未指明雪板機制。

## 原生整合方式

文件頁應用 **`screenshot`**，不是 `photo`。依 `tools/video/templates/templates.mjs`，`photo` 專用於真實照片，頁面截圖用 `screenshot`。原生 screenshot 沒有 crop 欄位，所以採已登錄矩形的外部裁切檔；透明留邊使橫向段落能以原生固定高度完整放入畫面。

每張須把 `source-assets.json` 的 `nativeAsset` 加進 `assets[]`，再把 `nativeScene.data` 配入對應景。必須保留 `path/source/license/author/url`。原生說明欄 `creditLine` 讀 `source`，不單獨輸出 `author`，因此建議 `source` 已包括作者、頁碼、日期、Commons 及裁切／透明留邊。`url` 連 Commons 對應頁，原圖 URL 留在來源登錄。

建議 `data.caption` 已備妥繁中摘要，`data.credit` 為「1959 結案書 · PD-RU-exempt · 裁切」。示範不設定 highlight，所以所有示範 line 的 reveal 為 0；正式旁白由主稿管理。三張 native asset／scene 檢查均通過，真實檔案可由 `render/plan.mjs` 的 `assetFile` 解析到 workdir，不需要圖庫供應商呼叫或後台素材匯入。

## 排除項與驗收界線

不使用帳篷照 `Dyatlov_Pass_incident_02.jpg`（Commons 標記 possible wrong license），不使用未清權的 `case-304-back.jpg`／`case-312.jpg`，不展示 386／387 全頁傷勢段，也不生成任何仿原件文件。這次 PASS 是素材像素、版型與來源整合準備；不是全片聲音／字幕播放驗證或站主成片核准。
