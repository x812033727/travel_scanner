# Google Maps × AI Studio 改稿小樣：來源與查核紀錄

本次為離線內容示範，未匯入、未發布。查核日期：2026-11-10（Asia/Taipei）。原文輸入為 `../../ai-news-google-maps-ai-studio-20261109.json`。

## 本次實際做了什麼

- 透過瀏覽工具讀取下列官方正文；再以公開 UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 直接 HTTP 取得同頁，六頁均回傳 200。
- 原始 HTML、去除 script/style 的文字抽取與 URL／時間／SHA-256 收據保存在 `evidence/`；收據為 `evidence/http-receipts.json`。直接 HTTP 時間為 2026-11-10 12:16 UTC（台灣 20:16）。`checked_on` 表示當日確實讀到文件，不代表當日功能實測。
- 完整閱讀兩份公告、AI Studio 專用文件與通用 Demo Key 文件；正式入門文件讀取設定與計費正文；安全指引核對 API／應用限制及網站／伺服器差異。

## 逐來源觀察

### 1. Google The Keyword 簡版公告

- 標題：[Developers can now build with Google Maps Platform in AI Studio.](https://blog.google/innovation-and-ai/technology/developers-tools/build-google-maps-platform-ai-studio/)
- 發布：2026-11-09；checked_on：2026-11-10。
- 觀察：對象是開發者在 AI Studio 製作應用；列出描述構想、接上 Maps、互動預覽流程，試用與正式計費分開。
- 使用處：兩句導讀的事件、對象與免費／上線分界。沒有把它改寫成 Google Maps 消費 App 的更新。
- 原文只有這份短公告；本次跟進其完整開發者公告與文件，未沿用舊 checked_on。

### 2. 完整 Google Developers 公告

- 標題：[From prompt to app: Build with Google Maps in AI Studio](https://developers.googleblog.com/from-prompt-to-app-build-with-google-maps-in-ai-studio/)
- 發布：2026-11-09；作者 Abinaya Selvam、Mike Taylor-Cai；checked_on：2026-11-10。
- 觀察：官方流程是輸入構想、啟用 Maps、預覽互動地圖；列門市、路線、3D 等範例。每日每 API 100 次呼叫、每 24 小時重設；正式使用需連結計費，適用標準價格。
- 使用處：第一節的官方流程與門市切角。未複製其提示詞，未宣稱「幾分鐘一定做好」。
- 範例入口是官方提供，不等於本次已打開範例、產生程式或驗證地圖資料。

### 3. AI Studio 專用文件（本次核心依據）

- 標題：[Google Maps Platform in AI Studio](https://developers.google.com/maps/ai/ai-studio)
- 頁面更新：2026-11-09 UTC；checked_on：2026-11-10。
- 觀察：新 Cloud 使用者、既有使用者免費原型、既有已計費專案是不同路徑。新使用者 Demo Key 功能範圍較廣；既有使用者免費原型欄的 Places 排除使用者照片與評論。Demo 路徑都列 100 次／日／API；正式專案列標準配額。
- 使用處：路徑選擇、比較表、照片／評論限制。本文沒有將特定欄位限制套用全部使用者。
- 文件部分敘述寫移除配額限制，但同頁表格與 troubleshooting 寫標準／production 配額；小樣採後者，不寫成付費無上限。

### 4. 通用 Demo Key 文件

- 標題：[Get a Maps Demo Key and use it with Google Maps Platform](https://developers.google.com/maps/demo-key?hl=en)
- 頁面更新：2026-10-22 UTC；checked_on：2026-11-10。
- 觀察：文件列個人 Google 帳號，排除 Workspace；申請資格也與 IP、帳號所在地有關。Demo 僅供測試原型，不供正式產品。正文功能清單比 AI Studio 新版文件簡略。
- 使用處：Workspace 需先查資格的提醒。未聲稱全部台灣帳號必能啟用。
- 文件差異：較舊通用頁把 Demo Key 功能寫成單一範圍，較新專用頁依新／既有 Cloud 使用者區分。無法從這些文件完全釐清各帳號的實際開通結果；寫稿以本次專用頁為主要依據，資格問題不自行推定例外。

### 5. 正式專案入門文件

- 標題：[Getting started with Google Maps Platform](https://developers.google.com/maps/get-started)
- 頁面更新：2026-11-09 UTC；checked_on：2026-11-10。
- 觀察：正式專案需啟用計費、需要的 API／SDK、建立或設定 API 金鑰。正文 Billing Account Credits 按各 SKU 提供每月免費用量，並連至價目表。
- 使用處：上線設定與按項目的每月免費用量。不填未核對的價格、成本試算或免費可服務訪客數。
- 差異：頁首自動摘要仍提舊式每月 credit，與正文按 SKU 敘述不同；小樣採正文，不引用摘要的金額，也未查價目表完整費率。

### 6. API 安全指引

- 標題：[Google Maps Platform security guidance](https://developers.google.com/maps/api-security-best-practices)
- 頁面更新：2026-11-09 UTC；checked_on：2026-11-10。
- 觀察：建議同時設定一類應用限制及一個以上 API 限制；網站與伺服器的限制種類不同。需按所用 API／平台配置。
- 使用處：下一步中的金鑰限制，不提供適用所有 Maps API 的單一配置。
- 未把「金鑰完全不會在前端出現」寫成通則；瀏覽器 SDK 與伺服器 web service 的使用方式不同。

## 編輯建議與推論，不是官方實測結果

- 「先完成搜尋→標記→地址」是編輯建議；提示詞為本次自撰，未實跑。
- 核對少量已知門市、無結果、手機操作，是建議的原型驗證清單，未暗示已執行或已通過。
- API 次數不能直接換算人次是單位上的區分；未估計每位訪客實際會呼叫幾次。
- 未開啟帳號、領取金鑰、連結帳務、呼叫 Maps API、部署或量測效能。未驗證台灣實際開通、額度重設時間點、資料準確性、每次互動呼叫數、生成程式安全性、整體 AI Studio／Gemini 成本。
- 「免費」僅指已核對的 Maps Demo Key 原型路徑，不代表 Gemini、代管或其他服務皆免費。

## 給獨立查核者

優先核對專用文件的三欄表格、既有使用者照片／評論限制、Workspace 資格差異與每 API／日單位。若來源後續修改，更新當日查核並保留現有快照，不能把本次的文件確認寫成功能實測。
