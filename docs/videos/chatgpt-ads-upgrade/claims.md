# claims.md — chatgpt-ads-upgrade

One line per checkable claim. Every URL was fetched today (2026-09-25) with
`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`.

c1｜官方公告日期 2026-09-23（"Starting today, ChatGPT Ads will begin rolling out across Indonesia, Malaysia, the Philippines, Singapore, Thailand, Vietnam, and Taiwan."），台灣與東南亞六個市場（印尼、馬來西亞、菲律賓、新加坡、泰國、越南）同一篇公告開始陸續上線。**官方頁沒有寫台灣當地的上線時刻**：官方 RSS 的發布時間是 2026-09-23 02:00 GMT（台灣 9/23 10:00），sitemap 的最後修改是 2026-09-24 02:01 GMT（台灣 9/24 10:01）；「9/24 上午 10 點」只出現在台灣媒體報導，第三方不能證實數字，所以片中改成「官方 9 月 23 日公告」、不講時刻（查核第 1 輪）。查核第 2 輪重抓：官方頁日期仍是 September 23, 2026、RSS pubDate 仍是 Wed, 23 Sep 2026 02:00:00 GMT；sitemap lastmod 2026-09-24T02:01:30Z 與 Inside 報導的 datePublished 2026-09-24T10:01+08:00 同一分鐘，所以台灣媒體的「24 日上午 10 點」很可能是頁面實際上線的台灣時間，但官方文字只給 9 月 23 日，片中維持不變｜https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ ＋ https://openai.com/news/rss.xml｜2026-09-25｜ads-launch-big, ads-launch-bullets

c1a｜時間軸：2026-02-09 在美國開始測試（對象是美國已登入的成年 Free 與 Go 用戶）；2026-08-11 的官方更新寫廣告「已經在英國、墨西哥、巴西、日本、南韓上線」（官方沒寫確切上線日，只知道這則更新的日期是 8 月）；8 月 18 日宣布下週擴大到歐洲 31 國；官方表示今年會繼續擴大到更多市場。查核第 2 輪補充：3/26 更新說先到加拿大、澳洲、紐西蘭，5/7 更新說「接下來幾週」在英國等五國擴大試行，8/18 歐洲公告說半年內已擴大到 8 個市場；所以片中「8 月擴大到英國、日本、南韓」的「8 月」是官方宣布已上線的月份，不是確切上線日｜https://openai.com/index/testing-ads-in-chatgpt/ ＋ https://openai.com/index/chatgpt-ads-expands-across-europe/｜2026-09-25｜ads-launch-bullets

c1b｜廣告出現在回答下方，官方原文是 "clearly labeled as sponsored and visually separated from ChatGPT's response"；官方從沒寫「用一條線隔開」，片中三處「一條線」已改成「標明是贊助、和回答分開」（查核第 1 輪）｜https://help.openai.com/en/articles/20001047-ads-in-chatgpt｜2026-09-25｜ads-launch-big, approach-bullets

c2｜廣告只可能出現在 Free 與 Go 方案；Plus、Pro、Business、Enterprise、Edu 帳號不會看到廣告（所以「只有 Plus」不對，是「Plus 以上」）｜https://help.openai.com/en/articles/20001047-ads-in-chatgpt｜2026-09-25｜hook, myth-compare, q1-bullets, approach-bullets

c3｜Free 方案有免費的 Ads-Free 切換，換掉廣告但降低訊息額度；Go 沒有這個免費開關，需切回 Free 或升級到 Plus/Pro 才能保證沒有廣告｜https://help.openai.com/en/articles/20001047-ads-in-chatgpt｜2026-09-25｜myth-compare, q2-compare, settings-steps, approach-bullets

c4｜Ads-Free 不會改變 ChatGPT 給的回答內容；切過去是「沒有廣告」（No ads，不是「少看到」），代價是訊息額度變低、部分工具不能用（原文 "no access to some tools like image generation or deep research"），官方沒公布降多少｜https://help.openai.com/en/articles/20001047-ads-in-chatgpt｜2026-09-25｜q1-bullets, q2-compare

c5｜官方不對「經判定」未滿 18 歲的帳號顯示廣告（依帳號年齡資訊與年齡預測）；未登入的畫面也可能有廣告，但只放適合所有人的｜https://help.openai.com/en/articles/20001047-ads-in-chatgpt｜2026-09-25｜q1-bullets

c6｜Go 方案卡片英文原文 "This plan may include ads."，台灣看到的中文版是「此方案可能包含廣告。」（Plus 卡片沒有這句）｜https://chatgpt.com/pricing/（openai.com/chatgpt/pricing/ 轉址過去）｜2026-09-25｜myth-big

c7｜廣告設定路徑：個人頭像 → Settings（中文介面「設定」）→ Ad Controls（中文介面「廣告控制功能」）；免費版可以在裡面切到 Ads-Free（中文介面「無廣告」），切之前會跳出說明取捨的提示；Go 要用 Ads-Free 得先切回 Free。廣告控制頁除了個人化開關，還有廣告紀錄、刪除廣告資料、過往對話與記憶開關｜https://help.openai.com/en/articles/20001047-ads-in-chatgpt ＋ https://help.openai.com/zh-hant/articles/20001047-ads-in-chatgpt ＋ https://help.openai.com/en/articles/8357869-how-to-change-your-language-setting-in-chatgpt｜2026-09-25｜settings-steps

c8｜ChatGPT Go 美國定價每月 8 美元（官方原文 "In the US, Go is available for $8 per month."；定價頁今天載入的美國價格設定也是 8.0 美元、未稅）｜https://openai.com/index/introducing-chatgpt-go/ ＋ https://chatgpt.com/backend-anon/checkout_pricing_config/configs/US｜2026-09-25｜q3-table, q3-code

c9｜ChatGPT Plus 每月 20 美元（Help Center 原文 "Price: $20/month (billed monthly)."；定價頁今天載入的美國價格設定也是 20.0 美元）｜https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus ＋ https://chatgpt.com/backend-anon/checkout_pricing_config/configs/US｜2026-09-25｜q3-table

c10｜台灣銀行 2026-09-25 13:25 牌告，美元即期賣出 31.855（現金賣出 32.05）；片中只拿來做「美元換算對照」｜https://rate.bot.com.tw/xrt/flcsv/0/day｜2026-09-25｜q3-code

c11｜台灣客戶沒提供統一編號，要付 5% 營業稅（2025-05-01 起）；台灣官網的台幣價已經是含稅價，所以不是在 270／690 上面再加 5%｜https://help.openai.com/en/articles/11173733-taiwan-vat-and-egui ＋ https://chatgpt.com/backend-anon/checkout_pricing_config/configs/TW｜2026-09-25｜q3-code

c12｜**ChatGPT 官網已經對台灣直接標台幣價**：未登入、從台灣打開 chatgpt.com/pricing，畫面顯示 Go「$270 /每月」、Plus「$690 /每月」、Pro「From $3,300 /每月」；頁面載入的官方價格設定 configs/TW 寫 symbol "NT$"、symbol_code "TWD"、go.month 270.0、plus.month 690.0，兩者 "tax": "inclusive"、tax_percent 5.0。一年＝月費 × 12：Go NT$3,240、Plus NT$8,280（Go、Plus 沒有年繳）。Multi-currency billing 說明頁也寫具體價格看定價頁。撰稿時寫的「只有登入結帳頁才看得到」不成立（查核第 1 輪）。查核第 2 輪在內建瀏覽器未登入重看：畫面仍是 $0、$270、$690、From $3,300 /每月，頁尾地區「台灣」，網路請求確實是 configs/TW；**畫面上只有「$」符號，沒有 NT$、TWD 或「含稅」字樣**，台幣與含稅這兩件事只來自 configs/TW（symbol_code TWD、tax inclusive、tax_percent 5.0，另有 pricing_rollout_gate "is_pricing_enabled_for_twd"，表示台幣價是逐步開放的設定）。configs/TW 裡另有 plus.year 575.0，但 Plus 說明頁寫 "Currently, we do not support annual billing ... for ChatGPT Plus subscriptions"，定價頁常見問題也寫「我們提供 Go、Plus 和 Business 的月繳方案，以及 Business 和 Enterprise 的年繳方案」，所以一年仍是月費 × 12｜https://chatgpt.com/pricing/ ＋ https://chatgpt.com/backend-anon/checkout_pricing_config/configs/TW ＋ https://help.openai.com/en/articles/10421635-multicurrency-billing｜2026-09-25｜q3-table, q3-code, youtube.description

補充查證（未逐句編號，但支撐敘事）：
- Go 的對照算式（8 × 31.855 = 254.84；254.84 × 1.05 ≈ 268）是站上自己的算術，用來說明台灣官網的 270 元大約就是美元價換匯再加 5% 稅；一年的金額用官方台幣月費算（270 × 12 = 3,240）。撰稿版的「268 × 12 = 3,211」算錯（268 × 12 = 3,216；3,211 是 267.58 × 12），已隨官方台幣價一起改掉（查核第 1 輪）。
- 「9 月 24 日上午 10 點台灣時間、酒類與真錢博弈禁止刊登、金融廣告在台灣尚未開放」等細節與 c1、c8 同一篇 inside.com.tw 報導，本片只用了時間點與八美元這兩個數字，酒類／博弈細節未使用（見「不做的事」）。

## 與企劃不同的地方

- **第 7 節（動手做）把 `steps` 和 `screenshot` 兩個場景合併成一個 `steps` 場景。** 原企劃是「`steps`：設定廣告怎麼找（3 步）」加上「`screenshot`：Ad Controls 頁面（待站主截圖）」。因為 `docs/videos/chatgpt-ads-upgrade/screenshot-ad-controls.png` 目前不存在，lint 會拒絕缺檔的資產，所以照 launch 指示把整節改寫成一個 4 步的 `steps` 場景（`settings-steps`）：前兩步是原本的「打開 Settings」「點進 Ad Controls」，第三、四步把原本screenshot 要呈現的「Free 才看得到切換」「Go 只能管理個人化」內容改成文字步驟。**等站主補上截圖之後，建議把第三、四步拆回一個獨立的 `screenshot` 場景**（`highlight` 框在 Ads-Free 切換或 Ad Controls 選單的位置），恢復企劃原本兩個場景的安排。
- **narration 沒有逐字唸出英文引句 "may include ads"。** `myth-big` 場景的字卡（`data.text`）保留官方英文原句，但口播只講中文翻譯與意涵，沒有把整句英文讀出來，避免中文語音唸一整句英文顯得生硬；這句英文因此不需要另外加 "may"、"include"、"ads" 三個詞到發音字典。
- **敘事中沒有直接講出「OpenAI」這個公司名稱**，全片用「官方」代替，是文字風格選擇，不影響事實。
- 表格與算式的欄位文字做了精簡（例如「Free（預設，看廣告）」精簡成「Free 預設」），內容與企劃的四條路徑、四個數字完全一致，只是字數配合 `table`/`code` 版型的欄寬需求微調用詞。
- 每個章節的口播長度和企劃草案中列出的秒數不會逐節精確對齊（企劃的秒數是規劃輔助，不是驗收標準），但九個小節的總長度、頻道實測語速下的總長（約 8.9 分鐘）落在企劃「8–12 分鐘」的框架內，也落在 schema 的 `target_minutes: [8, 12]`。

## 我懷疑但沒動的事

- ~~**Plus 每月 20 美元這個數字**~~：查核第 1 輪已用 Help Center「What is ChatGPT Plus?」與定價頁載入的美國價格設定確認（見 c9）；同時發現定價頁對台灣直接標台幣價（見 c12），表格與算式已改用官方台幣價。
- **"Ads controls" 在官方頁面上出現兩種大小寫**（操作步驟寫 "Select Ads controls"，另一段寫 "Settings > Ad Controls"），影片統一用「Ad Controls」，這只是引用哪一段的差異，不影響設定路徑本身。
- **發音字典裡新加的詞全部先標 `null`**（ChatGPT、Go、Plus、Free、Settings、Ad、Controls、App），因為撰稿階段沒有試聽環境。這些詞多數是常見英文單字，猜測唸起來風險不高，但「Settings」「Controls」这類較長的字，實際聽感如何無法在這個階段確認，需要 `review` 階段站主實際聽過。
- **本片沒有處理「金融廣告在台灣尚未開放」「酒類與真錢博弈禁止刊登」這兩個細節**（inside.com.tw 報導裡有提到），因為和判斷升不升級的主線無關，故意沒有寫進口播或字卡；如果之後要做「廣告主視角」的影片，這兩點可以用上。
- **9/24 之後如果官方又調整了廣告地區、Ads-Free 規則，或台灣定價頁的台幣金額變動**（台幣金額第 1 輪已經看到並採用），本片會過期，需要在正式上架前重新核一次「會過期的事實」表列出的每一條連結。

## 進度

全部 17 個場景、180 句台詞已經寫完，`lint` 0 錯誤、2 個警告（都是已知的 250 字/分鐘估速高估，見報告）。尚待：
- [x] verify-1.md（另一位代理的事實查核；2026-09-25 完成，事實修改超過三處，需要第 2 輪）
- [x] verify-2.md（換一位代理；2026-09-25 完成，第 1 輪的修改全部成立，這一輪沒有事實修改）
- [ ] 站主決定：方案階梯圖（approach-diagram）上的「台灣網頁刷卡以美元計價」「只有免費版標廣告」已和本片內容衝突，見 verify-1.md
- [ ] 聽眾優先審稿（口語、句長、術語唸法、開場鉤子）
- [ ] `tts --dry-run`（先看字數與額度）
- [ ] 站主聽 `review/audio.html`，確認新加的發音字典詞唸得對不對
- [ ] `render` / `assemble` / `captions`
- [ ] 站主補 `docs/videos/chatgpt-ads-upgrade/screenshot-ad-controls.png` 之後，把 `settings-steps` 場景的第三、四步拆回一個 `screenshot` 場景
