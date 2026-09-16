# 查核紀錄：ai-news-siri-ai-ios-27-20260914

- 查核日：2026-09-15
- 對象：`apps/api/app/guides/content/ai-news-siri-ai-ios-27-20260914.json`（zh-TW）與研究紀錄
- 做法：以 `curl -A "Mokaair-editorial"` 抓官方頁原始 HTML，轉純文字後逐句比對（沒有帶任何個人資料）。
- 自檢：`check_article.py` 輸出 `OK … zh-TW paragraphs 2977`

## 對照的一手來源

| 代號 | URL | 狀態 |
|---|---|---|
| NR-US | https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/ | 200，稿日 2026-09-14 |
| SUP | https://support.apple.com/en-us/127893 | 200，Published 2026-09-14 |
| SUP-TW | https://support.apple.com/zh-tw/127893 | 200，內容與 en-us 相同的英文原文 |
| FA-TW | https://www.apple.com/tw/ios/feature-availability/ | 200 |
| NR-TW-18P | https://www.apple.com/tw/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/ | 200，稿日 2026-09-09 |
| NR-TW-AI | https://www.apple.com/tw/newsroom/2026/09/next-generation-of-apple-intelligence-available-today/ | 200，交叉確認用，不在 sources |
| NR-SW | https://www.apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/ 與台灣版 | 200，交叉確認用，不在 sources |
| SUP-AI | https://support.apple.com/en-us/121115 | 200，交叉確認用；zh-tw/121115 仍是 iOS 26 舊版 |
| — | https://www.apple.com/tw/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/ | 404（台灣沒有 Siri AI 專稿） |

## 結果統計

共拆出 **95 條**主張（title 1、description 2、開頭兩段 15、五節正文 63、表格 5 列、圖解 1、callout 4、sources 4）。

- 正確：80
- 需要改寫：12（過度肯定、把繁中或台灣條件講得太寬、缺地區條件、機型不一致沒寫明、將來式寫成確定）
- 錯誤：0
- 查無出處：3（beta 定義、「以設定畫面為準」誤掛成 Apple 說法、「兩家處理方式不同」的比較）

文章改了 16 處（含 3 處為了控制字數刪掉的重複句），研究紀錄改了 5 處。

## 逐條改動

### 需要改寫

1. **10 月新增語言寫成已定**
   - 原文：法文、日文、韓文、葡萄牙文與西班牙文於 10 月加入
   - 改後：…預計 10 月加入
   - 依據：NR-TW-18P「法文、日文、韓文、葡萄牙文、西班牙文支援將於 10 月推出」；NR-US「is coming next month」

2. **第三方 App 的推論**
   - 原文：Microsoft Outlook、Notability、Tripsy 的操作「即將」支援，可見不是每個 App 第一天都已接上。
   - 改後：…「即將」支援，代表推出當天還不能用。
   - 依據：NR-US 只說 Outlook、Notability、Tripsy 這三項是 soon，沒有講「每個 App」。

3. **繁體中文可用範圍講得太寬（沒提機型與 Siri 語言）**
   - 原文：用繁體中文的 iPhone 更新後，拿到的是新一代 Apple Intelligence 的部分功能，Siri AI 則不在繁體中文的清單上。
   - 改後：支援 Apple Intelligence 的 iPhone 把裝置與 Siri 語言設為繁體中文，更新後能用到新一代 Apple Intelligence 的部分功能；Siri AI 則目前只支援英文。
   - 依據：NR-TW-18P 註腳「Apple Intelligence 適用於 Siri 和裝置語言均設為…繁體中文…的裝置」；FA-TW 頁尾機型清單

4. **「台灣沒被排除」推成台灣可用**
   - 原文：也就是說，台灣沒有被列為排除地區，但 Siri AI 本身只標英文。
   - 改後：台灣沒有被列為排除地區，但這不等於 Apple 確認台灣帳號可用，地區條件見下一節。
   - 依據：FA-TW 只寫「適用於英文 - 不適用於中國大陸或歐盟地區」；SUP 另寫「your Apple Account is in an eligible region」和「Availability varies by region and platform」，沒有地區清單。

5. **支援機型不一致沒有寫明**
   - 原文：…iPhone 16 系列或後續機型，以及 iPhone Air。（沒提新聞稿寫法不同）
   - 改後：…以及 iPhone Air；9 月 14 日新聞稿的機型清單沒有單獨寫出 iPhone Air，兩處不一致，本文以支援文件為準。
   - 依據：SUP「iPhone 15 Pro, iPhone 15 Pro Max, iPhone 16 models or later, and iPhone Air」；NR-US Pricing and Availability「iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max」

6. **地區條件寫得不完整**
   - 原文：Apple 帳號也要位於符合資格的地區，但支援文件沒有逐一列出是哪些地區。
   - 改後：Apple 帳號也要位於「符合資格的地區」，支援文件沒有列出清單，也沒有說明台灣是否在內。
   - 依據：SUP

7. **改成英文後的影響**
   - 原文：上一節表格裡在繁體中文下列出的功能，也會跟著改在英文設定下運作。主要用中文收發訊息的人，可以先想清楚這個代價再決定。
   - 改後：上一節表格裡的功能也會改在英文設定下運作。Apple 沒有說明英文設定的 Siri AI 能否處理中文訊息與郵件，主要用中文溝通的人可以先想清楚再決定。
   - 依據：SUP、NR-US 都沒有提到跨語言內容，所以只寫「沒有說明」。

8. **Siri AI 的伺服器端說法**
   - 原文：Siri AI 屬於有每日用量限制的伺服器端功能。
   - 改後：Apple 把 Siri AI 列在仰賴伺服器端模型、有每日使用限制的功能之中。
   - 依據：NR-US「Certain Apple Intelligence features that rely on server-side models are subject to daily usage limits, including but not limited to Siri AI」

9. **情境少了地區前提**
   - 原文：假設你已把 iPhone 設成英文並等到 Siri AI 下載完成
   - 改後：假設你的帳號地區符合資格、已把 iPhone 設成英文並等到 Siri AI 下載完成
   - 依據：SUP

10. **通話情境「不必改英文」少了機型條件、歸因不清**
    - 原文：Apple 說明它會在「電話」App 顯示確認碼或預約編號這類資訊，且繁體中文欄位有列出，不必改成英文。
    - 改後：至於撥電話給飯店時會顯示預約編號這類資訊的「通話情境」，適用範圍頁的繁體中文欄位有列出，在支援機型上不必為它改成英文。
    - 依據：FA-TW「Apple Intelligence：電話：通話情境」列中文（繁體）；NR-US Call Context 原文

11. **callout 少了機型與地區**
    - 原文：維持繁體中文設定，更新 iOS 27 可以用到…；Siri AI 目前只標英文…Apple 未列出繁體中文的 Siri AI 時程。
    - 改後：在支援機型上維持繁體中文設定，更新 iOS 27 可以用到…。Siri AI 目前只支援英文…Apple 未列出繁體中文的時程，也沒有說明台灣帳號是否屬於符合資格的地區。
    - 依據：SUP、FA-TW

12. **description 與圖解缺地區條件**
    - description：「需要的機型與語言設定」→「需要的機型、語言與地區條件」
    - 圖解第 3 格：「語言設定／裝置與 Siri 同為英文」→「語言與地區／英文，帳號地區須合格」；image alt 與 caption（內容包與研究紀錄）同步。圖上數字仍只有正文出現過的「27」。
    - 依據：SUP

### 查無出處

13. **beta 的意思寫得像 Apple 的說明**
    - 原文：beta 代表功能還在調整，回答可能出錯，介面與規則也可能改變。
    - 改後：Apple 在上述頁面沒有定義 beta 的範圍；一般來說 beta 是仍在測試的版本，回答可能出錯，功能與規則也可能改變。
    - 依據：NR-US、SUP、FA-TW 都只有「beta／Beta 版」字樣，沒有定義。

14. **「實際以更新後的設定畫面為準」接在 Apple 提醒後面，看起來像 Apple 說的**
    - 原文：Apple 也提醒部分功能可能未在所有地區提供，或未適用於所有語言，實際以更新後的設定畫面為準。
    - 改後：Apple 也提醒部分功能可能未在所有地區提供，或未適用於所有語言。（刪掉後半句）
    - 依據：FA-TW 頁首「部分 iOS 和 iPadOS 功能目前並未在所有地區提供，或適用於所有語言」，沒有後半句。

15. **和 Google 的比較沒有來源**
    - 原文：兩家說明的處理方式不同，建議分別閱讀官方文件。
    - 改後：兩家的隱私說明不宜互相套用，請各自對照官方文件。
    - 依據：本篇 sources 沒有 Google 文件，不做比較。

### 為了控制字數刪掉的重複句（內容正確）

16. 第一段刪掉能力列舉（第一節已寫）；第一節第三段刪掉「這些都是 Apple 的產品說明。」（第二段已說明）；第四節第二段刪掉「Siri App 的對話紀錄則透過 iCloud 同步。」（第一節已寫）。

### 研究紀錄同步

- verified_facts：支援文件那條加上「Availability varies by region and platform」；新增「機型寫法不一致」一條與「Apple Intelligence 須 Siri 與裝置語言都設成支援語言、限支援機型」一條；FA-TW 那條加上頁首的地區語言提醒。
- unverified_or_excluded：台灣 eligible region 那條寫明文章現在的寫法；機型不一致那條補上 iPhone Air 已寫明、iPhone Duo 不提的原因；新增「英文 Siri AI 能否處理中文內容」「beta 定義」「通話情境裝置端處理（來源不在 sources）」三條。
- diagram 的 caption 與第 3 格同步更新。

## 核對過沒問題的重點

- 9/14：NR-US 稿日與「begins rolling out today in beta in English」；NR-TW-18P「iOS 27 將於 9 月 14 日 (星期一) 以免額外付費軟體更新的形式提供」「Siri AI 將於 9 月 14 日 (星期一) 隨 iOS 27 推出 Beta 版，適用於設定為英文的支援裝置」。
- 台灣 iPhone 18 Pro：NR-TW-18P 把台灣列在 65 個以上國家和地區中，「台灣時間 9 月 12 日 (星期六) 晚上 8 點開始預訂…9 月 18 日 (星期五) 開始供貨」；A20 Pro 正確。
- 等候名單：SUP「This will add you to a waitlist, and wait times can vary. Siri AI will begin to download automatically when your wait is complete.」
- 隱私：NR-US「Apple Intelligence uses on-device processing and Private Cloud Compute…personal data is not stored nor made accessible to Apple or anyone else. Outside experts can continue to verify this privacy promise at any time.」；台灣官方譯名「私密雲端運算」見 NR-TW-AI 與 NR-TW-18P。Spotlight index、App Toolbox「work entirely on device」與 Google／Gemini 合作的說法都與 NR-US 相符。
- 16 種語言與繁中：NR-TW-18P 註腳逐一核對，共 16 種。
- FA-TW 繁中欄位：照片空間重構、延伸、Safari 標籤頁依主題分類、通知我、行事曆描述行程、捷徑描述捷徑、電話通話情境都列「中文 (繁體)」；郵件建議只列英文；Siri AI 生動聲音只列英文（英國）、英文（美國）。
- 未滿 13 歲、每日使用限制與未來付費、歐盟與中國大陸條件、旅行到其他地區仍可使用：都有原文。
- 讀者角度：文章沒有暗示本站實測，沒有建議更改帳號地區，也和 `ai-news-gemini-personal-intelligence-20260114` 不重複（那篇講 Google 的授權連結與訓練政策，本篇只留一句連結）。

## 仍不確定的點

1. **台灣帳號是否屬於 Siri AI 的「eligible region」**：支援文件沒有清單，FA-TW 只排除中國大陸與歐盟。文章寫成「Apple 沒有說明」，要等 Apple 公布清單或更新支援頁。
2. **Siri 語言的對應**：Apple Intelligence 要求 Siri 語言設為「繁體中文」，但 FA-TW 的 Siri 語言欄位寫的是「國語 (台灣)」。這兩個是不是同一個設定，Apple 沒有明說，文章沿用 Apple 的「繁體中文」寫法。
3. **iPhone Duo**：〈Apple 軟體平台重大更新〉稿（美國與台灣版）把它列進 Apple Intelligence 與 Siri AI 機型，支援文件 127893 沒有單獨列出，「iPhone 16 models or later」算不算包含它無法判斷。文章不提。
4. **10 月新增語言**：還是不是 beta、地區條件是否一樣，Apple 沒有說明。
5. **英文設定的 Siri AI 能否讀懂中文訊息、郵件**：官方沒有說明。
6. **通話情境打給海外商家（例如情境中的大阪飯店）是否適用**：官方沒有說明，文章只當作編輯設計的情境。
7. **生動聲音的機型**：NR-US 註腳比支援文件多列 iPhone Duo、iPhone 18 Pro 系列，文章只寫語言限制、不寫機型。
8. support.apple.com/zh-tw/121115 在 9/15 仍是 iOS 26 舊版內容，zh-tw/127893 是英文原文，繁中讀者點過去會看到不一致的內容。
