# Apple 樣稿來源與編輯紀錄

狀態：作者完成，待獨立查核；未發布、未匯入 repo。

查核日期：2026-11-10（台灣）。所有 curl 請求使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，跟隨轉址，保留原始 HTML。HTML 文字讀取先移除註解、script 與 style；HTTP 200 之外也確認實際標題與正文，不以空殼頁通過。原文與雜湊保存在 `evidence/`；`receipts.json` 記錄各檔大小與 SHA-256。

## 實際讀取

| 來源 | 結果／用途 |
| --- | --- |
| https://www.theverge.com/tech/1030084/apple-intelligence-usage-packs-ai-features-creator-studio-logic-pro | curl 200、390543 bytes；web open 失敗後改用固定 UA。讀到正文並循其超連結取得 Apple 127888、127901。它的 49.99 美元不是本稿的官方價格證據，未寫進樣稿 |
| https://support.apple.com/en-us/127888 | 200、168585 bytes；標題 About the intelligence features in Apple Creator Studio，頁面發布日 November 05, 2026。本文主要產品條件、用量包、地區、期限、帳號與 Logic Pro 路徑證據 |
| https://support.apple.com/en-us/127901 | 200、157567 bytes；標題 Learn about Apple Intelligence usage limits，發布日 September 09, 2026。包含未來軟體的說明；未把那段未來規劃混成目前 Logic Pro 已上線狀態。循其中連結讀 148587 |
| https://support.apple.com/en-us/148587 | 200、160096 bytes；標題 Apple Intelligence Usage Terms，發布日 September 09, 2026。本文最後一節的個別功能額度與重置、其他功能可繼續用的依據 |
| https://support.apple.com/en-us/118205 | 200、439434 bytes；標題 Availability of Apple Media Services。循 127888 的服務可用地區連結讀取，Taiwan 區塊確實列出 Apple Creator Studio；只證明訂閱服務，不能用來推論用量包已開放 |

## 主張核對表

- 第 1–3 節：127888 的 Intelligence features、Logic Pro assistant requirements、Usage limits 段。訂閱條件、部分功能上限、對話複雜度、查看用量與 History、Mac 與語言條件、用量包先後扣除、個人帳號與家人共享限制、逐月保留及 12 個月到期皆在正文內。
- 第 4 節：127888 的購買國家清單只有巴西、加拿大、法國、德國、印度、墨西哥、英國、美國。表述限於「目前官方名單沒有台灣」，不擴大成台灣不能用任何智慧功能。118205 的 Taiwan 區塊另外證明訂閱服務有提供。
- 第 5 節：148587 第 1 節 Usage Limits。某項功能達限後可能受限或暫停到重置，期間其他裝置功能可繼續使用。
- 文中的「先查額度」與區分兩張名單是依上述資料給讀者的閱讀方法，不是採購推薦。

## 相對現稿的實質調整

1. 移除未在官方頁找到的 49.99 美元，不換算台幣、不填台灣售價。
2. 補上官方購買地區不含台灣、需有效 Creator Studio 訂閱；原公開稿只用 The Verge，未帶入這個範圍。
3. 補上「當月原有額度先用，才消耗加購額度」及查看 History 的實用資訊。
4. 移除其他 App 本月將上線的預測，也不聲稱所有 Apple AI 開始收費。
5. 不寫本站實測，不推算每包可問幾次，不把一次性購買說成新的月費。

## 未證實與未採用

- 官方目前這些頁面沒有列出台灣用量包售價或開放日期；樣稿不補猜。
- 沒有實際以任何帳號登入 App 購買或測試，不能保證特定帳號會看見按鈕。
- 127888 提到銷售原則上不退款（法律要求除外）；本稿沒有詳談退款或給法律解釋。
- 文章仍需另一位代理逐項核對保存原文與必要的新讀取。本稿不是最終 fact-check receipt。

## 格式

`draft.json`：title、description、5 個 sections、3 個實際用於文章的官方 sources。

正文含 description、段落、小標與表格共 841 個 CJK 字元（不含來源連結）；不是機械湊字數的長稿。`article.md` 與 JSON 內容一致，段後附對應官方頁。依獨立查核者的初步意見，已補上官方腳註的 Logic Pro 助理 beta 測試版條件；等待定稿雜湊查核。
