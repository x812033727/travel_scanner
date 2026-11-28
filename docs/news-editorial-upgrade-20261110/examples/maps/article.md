# Google Maps 接進 AI Studio：免綁卡做門市地圖原型，上線前先看這張表

想替網站加上門市查找或路線規劃，Google 11 月 9 日宣布，開發者可直接在 AI Studio 描述需求，製作結合 Google Maps Platform 的網頁原型。使用 Maps Demo Key 的地圖原型額度不必先綁信用卡，但有呼叫額度與功能限制；正式上線仍須啟用 Cloud 計費。[官方公告](https://blog.google/innovation-and-ai/technology/developers-tools/build-google-maps-platform-ai-studio/)

## 先做「找到門市」這個小功能

對網站經營者來說，可以先把需求縮成一條操作：訪客搜尋地點、看到門市標記，再點開地址。這比一開始要求完整旅遊平台，更容易判斷原型是否有用。

Google 說明的流程是：在 AI Studio 輸入構想，讓平台設定 Maps 連線與 API 金鑰，接著在預覽區操作互動地圖；官方也提供門市查找範例。以下是依公告整理的流程，未經本機實測。[完整開發者公告](https://developers.googleblog.com/from-prompt-to-app-build-with-google-maps-in-ai-studio/)

- 輸入明確任務。編輯示例：「做一個門市查找網頁，顯示地圖與門市清單，點選標記後顯示地址；找不到結果時給出提示。」
- 選擇免費 Maps Demo Key（示範用 API 金鑰）或既有已啟用計費的 Cloud 專案，確認自己走哪條路徑。
- 在預覽區檢查標記、地址、搜尋無結果和手機操作。示例提示詞尚未測試，產生結果仍須逐項驗證。

## 免費試用和正式上線，差在哪裡？

| 項目 | 免費原型 | 正式上線 |
| --- | --- | --- |
| 帳務 | Demo Key 不需信用卡或 Cloud 計費帳戶 | 連結 Cloud 計費帳戶或既有已計費專案 |
| 額度 | 每個 API 每日 100 次呼叫，每 24 小時重設 | 適用標準配額，依 API 與專案核對 |
| 功能 | 依新／既有 Cloud 使用者路徑而異 | 可使用完整 Maps Platform 產品，仍須依功能設定 |
| 費用 | 在 Demo 額度內免費試作 | 適用標準價格及各項每月免費用量 |

表中限制依 11 月 10 日讀取的官方文件整理；100 次指 API 呼叫，不能直接當成每日可服務 100 位訪客。[AI Studio 專用文件](https://developers.google.com/maps/ai/ai-studio)、[正式專案入門文件](https://developers.google.com/maps/get-started)

已有 Cloud 專案、選免費 Demo Key 的人要特別留意：專用文件列明，這條路徑的 Places 地點資料服務不含使用者照片與評論。若設計靠照片選店，先確認可用功能，再承諾要做的畫面。公司 Workspace 帳號也應先核對資格：通用 Demo Key 文件列為不適用，AI Studio 專頁未說明例外。[功能與路徑](https://developers.google.com/maps/ai/ai-studio)、[Demo Key 資格](https://developers.google.com/maps/demo-key?hl=en)

## 下一步：驗證功能，再決定是否上線

先用少量已知門市核對位置與地址，確認訪客能順利找到目標。這一步通過後，再列出實際呼叫的 API、估算用量，並設定適合網站或伺服器的金鑰限制；Google 建議同時限制可用應用與 API，避免金鑰被挪用。[金鑰安全指引](https://developers.google.com/maps/api-security-best-practices)

今天要試，先從官方門市範例或一個搜尋任務開始。能在預覽區跑起來，只代表原型可檢查；資料是否正確、費用是否可接受，才是下一步上線的依據。
