# OpenAI 為什麼收掉 Sora？今天 AI 影片一秒多少錢

slug：`why-openai-killed-sora`｜旁白繁體中文（台灣）；CC 五語（zh-TW、zh-CN、ja、ko、en），配音音軌 en、ja、ko｜企劃日 2026-09-28｜目標 8–10 分鐘｜季企劃第 6 支：`docs/ai-video-en-season-01/briefs/06-why-openai-killed-sora.md`（建議上架 2026-11-10）

## 觀眾

台灣與其他華語觀眾優先，三種人：

- 看過 Sora 影片、知道它收掉了，想弄清楚「為什麼」的人。
- 用 AI 做短影音、廣告素材或社群影片的創作者、行銷與小團隊。他們知道 AI 能用文字生影片，但沒算過一秒要多少錢，也分不清各家是用秒、token、點數還是「單位」計價。
- 把影片 API 接進產品的開發者：Sora 的 API 已經關了，正在找下一家。

英語、日語、韓語觀眾透過 CC 字幕與配音音軌收看，簡中觀眾看簡中 CC。中文搜尋：「Sora 關閉」「OpenAI 為什麼收掉 Sora」「Sora 停止服務 替代」「AI 影片 價格」「AI 生成影片 一秒多少錢」「Veo 3.1 價格」「Kling 3.0 價格」；英文搜尋：「why did openai shut down sora」「sora shut down」「ai video generator cost per second」「veo 3.1 vs kling 3.0 vs seedance 2.0 price」。

## 觀眾看完能做到的事

- 拿任何一家 AI 影片工具的官方價目表，五分鐘內換算成「一秒多少美元、一支 8 秒多少美元」，旁邊寫下這個價錢假設的解析度、有沒有聲音、一支最長幾秒，再用同一個數字比較各家。
- 付錢或把工作流程接上某一家之前，打開它的棄用頁（開發者）或說明中心的停止服務與匯出說明（App 使用者），記下「最短給多久通知、有沒有指定替代」，並在行事曆設一個每季匯出一次素材的提醒。

## 站主觀點

套用立場：1、2、5

我看 AI 影片工具，先看一秒多少錢，再看 demo。OpenAI 收掉 Sora，它自己公開說過的理由只有兩句：Sora App 停止公告裡的「經過內部仔細討論更廣的研究優先順序」，和發言人給 CBS News 的「隨著我們聚焦、算力需求成長」。其他說法，像是 Sora 很吃算力、使用人數下滑，都是媒體報導，我會在畫面上標出是哪一家報的；OpenAI 沒公布的成本與營收，我一個數字都不引用。

我的讀法是（這是我的讀法，不是 OpenAI 說的）：影片是每生成一秒都要付算力的生意，價錢又一路往下。今天官方價目表上，720p 一秒已經有 0.05 美元的選擇（Veo 3.1 Lite）；Sora 2 關門前標的是 720p 一秒 0.10 美元，和 Veo 3.1 Fast 一樣，並不貴。它輸的不是標價，而是在一家說自己算力需求一直成長的公司裡，排不到前面。

所以我付錢給 AI 影片工具之前只做兩件事：一，把價目表換成「一秒多少、一支 8 秒多少」，旁邊寫上解析度、聲音、秒數；二，打開那一家的棄用頁和匯出說明。Sora 的 API 從通知到關閉是六個月，App 只有 33 天，棄用表上的建議替代欄是空的。新出的、demo 最驚豔的那一個，不是付錢的理由；用得到、付得起、哪天被收掉時搬得走，才是。價錢要登入或由程式載入、我讀不到的，我就說「以官網為準」，不猜。

數字出處：Veo 3.1 Lite 與 Veo 3.1 Fast 的每秒價見 https://ai.google.dev/gemini-api/docs/pricing ；Sora 2 的 0.10 美元見 OpenAI 價目頁 2026-08-02 的存檔 https://web.archive.org/web/20260802044220/https://developers.openai.com/api/docs/pricing ；六個月與空白的替代欄見 https://developers.openai.com/api/docs/deprecations ；33 天是 2026-03-24 通知到 2026-04-26 App 停止（OpenAI 說明中心，網址在「會過期的事實」）。

## 示範或實算

主軸是「一秒影片多少錢」。每一家都從企劃日（2026-09-28）打開的官方價目表，換成「每秒美元」和「一支 8 秒美元」，每一格都寫這個價錢假設的解析度、聲音與秒數。這和 `gpt6-vs-opus55-worth-paying` 的 token 月帳單不是同一種算法：單位是秒與支，要先把四種計價方式（直接標每秒、token、點數、單位）換成同一個數字，再比規格條件一樣的價錢。

**實算一：換成每秒、每支 8 秒**（選項 A 第 4 章的 `code`、兩張 `table`、`stats`；選項 B 第 2–3 章；選項 C 第 4 章）

| 模型（賣家） | 價目表的寫法 | 每秒 | 這個價錢假設的條件 | 一支 8 秒 | 官方頁 |
| --- | --- | --- | --- | --- | --- |
| Sora 2（OpenAI，已停） | $0.10／秒 | $0.10 | 720p，Standard；最長 20 秒 | $0.80 | 價目頁 2026-08-02 存檔 https://web.archive.org/web/20260802044220/https://developers.openai.com/api/docs/pricing （今天的 https://developers.openai.com/api/docs/pricing 已經沒有 Sora） |
| Sora 2 Pro（OpenAI，已停） | $0.30／$0.50／$0.70 每秒 | 同左 | 720p／1024p／1080p | $2.40／$4.00／$5.60 | 同上 |
| Veo 3.1（Google） | $0.40／秒 | $0.40 | 720p 或 1080p，有聲（預設）；4k $0.60；可選 4、6、8 秒，1080p 與 4k 只能 8 秒 | $3.20 | https://ai.google.dev/gemini-api/docs/pricing ；秒數規則 https://ai.google.dev/gemini-api/docs/veo |
| Veo 3.1 Fast（Google） | $0.10／秒 | $0.10 | 720p 有聲；1080p $0.12、4k $0.30 | $0.80 | 同上 |
| Veo 3.1 Lite（Google） | $0.05／秒 | $0.05 | 720p 有聲；1080p $0.08；不支援 4k | $0.40 | 同上 |
| Gemini Omni Flash（Google） | 影片輸出每百萬 token $17.50；720p 每秒 5,792 token | ≈ $0.10 | 720p；1080p 每秒 8,688 token，約 $0.15 | ≈ $0.81 | https://ai.google.dev/gemini-api/docs/pricing ；各解析度 token 數 https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing |
| Kling 3.0（Kling AI） | 每秒 0.9 單位，1 單位 $0.14（定價） | $0.126 | 720p、原生音訊（不含聲音控制）；無聲 $0.084；1080p 有聲 $0.168 | ≈ $1.01 | https://kling.ai/dev/pricing |
| Dreamina Seedance 2.0（BytePlus） | 每百萬 token 7.0 美元；官方範例 5 秒 $0.76 | ≈ $0.15 | 720p、16:9、輸入不含影片；token 數和秒數成正比 | ≈ $1.22 | https://docs.byteplus.com/en/docs/ModelArk/1544106 |
| Grok Imagine Video 1.5（xAI） | $0.14／秒 | $0.14 | 720p；480p $0.08、1080p $0.25；可選 1–15 秒 | $1.12 | https://docs.x.ai/developers/pricing ；秒數 https://docs.x.ai/developers/model-capabilities/video/generation |
| MiniMax-H3（MiniMax） | $0.08／秒 | $0.08 | 768P；2K $0.13 | $0.64 | https://platform.minimax.io/docs/guides/pricing-paygo |
| Gen-4.5（Runway） | 每秒 12 點，1 點 $0.01 | $0.12 | 1280:720 等畫面比例（約 720p）；可選 2–10 秒 | $0.96 | https://docs.dev.runwayml.com/guides/pricing/ ；秒數 https://docs.dev.runwayml.com/api/ |
| Higgsfield | 價目頁的數字由程式載入，讀不到 | 以官網為準 | — | — | https://higgsfield.ai/pricing |

畫面上的重點：表上最便宜 $0.05／秒（Veo 3.1 Lite，720p 有聲），最貴 $0.40／秒（Veo 3.1，720p 或 1080p 有聲），相差 8 倍；Sora 2 當年的 $0.10 落在中間。「一支 8 秒」只是比較用的長度：Veo 3.1、Grok Imagine Video 1.5、Gen-4.5 的官方文件都允許 8 秒；Kling 3.0、Dreamina Seedance 2.0、MiniMax-H3、Gemini Omni Flash 的原廠頁沒讀到可選秒數，只在 Runway 的 API 文件讀到它們在 Runway 上的範圍（Seedance 2.0 4–15 秒、MiniMax-H3 5–15 秒、Omni Flash 3–10 秒），寫稿日以原廠官網為準。

**實算二：同一個模型，原廠和轉售的價差**（選項 A 第 4 章的 `compare`；選項 B 第 3 章；選項 C 第 4、5 章）

| 模型 | 原廠 | Runway API（1 點 $0.01） |
| --- | --- | --- |
| Dreamina Seedance 2.0 | 約 $0.15／秒（720p） | 36 點＝$0.36／秒（480p／720p） |
| Veo 3.1 Fast，有聲 | $0.10／秒（720p） | 15 點＝$0.15／秒（頁面沒寫解析度） |
| MiniMax-H3 | $0.08／秒（768P） | hailuo3 10 點＝$0.10／秒（768P） |
| Grok Imagine Video 1.5 | $0.14／秒（720p） | 16 點＝$0.16／秒（720p） |
| Veo 3.1 有聲、Gemini Omni Flash | $0.40、約 $0.10 | 40 點＝$0.40、10 點＝$0.10（一樣） |

轉售平台多了一個帳號接很多家的方便；影片只比標價，不評好壞。

**實算三：一支 60 秒短片的素材費**（選項 A 第 5 章的 `steps`、`table`、`stats`；選項 B 第 1–2 章）

60 秒 ÷ 8 秒＝7.5，所以要 8 支素材；**假設三支留一支**（畫面上寫明是假設，請觀眾換成自己的比例），要生成 24 次。官方寫的是成功生成才收費（Gemini API 價目頁：「You will only be charged if your video is successfully generated.」；BytePlus 與 Kling 的價目頁也寫生成失敗不扣），所以生成成功、但你不想用的那兩支照樣算錢。

| 模型 | 一支 8 秒 | × 24 次 | 每「能用的一秒」 |
| --- | --- | --- | --- |
| Veo 3.1 Lite（720p 有聲） | $0.40 | $9.60 | $0.15 |
| Veo 3.1 Fast（720p 有聲） | $0.80 | $19.20 | $0.30 |
| Kling 3.0（720p 原生音訊） | 約 $1.01 | 約 $24.19 | 約 $0.38 |
| Veo 3.1（720p 或 1080p 有聲） | $3.20 | $76.80 | $1.20 |

口播只唸約數（「不到十美元」「將近七十七美元」），精確數字留在表上：英日韓配音唸數字比中文長，句子短才塞得進同一個畫面的時間。

## 大綱

### 選項 A：官方一句話，對上一張每秒價目表（推薦）
一行說明：先用 OpenAI 自己的兩句話和四個日期回答「為什麼」（報導標出處、站主的讀法標明是讀法），再用今天的官方價目表算出一秒、一支 8 秒、一支 60 秒短片，最後給付錢前要查的兩個頁面；和先算帳的 B、給開發者的 C 相比，最直接回答標題的問題。
開場鉤子（口播）：「九月二十四號，OpenAI 把 Sora 的 API 也關了。官方公告給的理由只有一句：研究的優先順序。可是 Sora 關門前，一秒影片只標零點一美元；今天 Google 的 Veo 3.1 Lite，一秒只要零點零五。這集把 OpenAI 的原話、各家一秒的價錢，和付錢前該查的兩個頁面，一次攤開給你看。」

鉤子數字：Sora 2 720p $0.10／秒（OpenAI 價目頁 2026-08-02 存檔，網址見實算一）；Veo 3.1 Lite 720p 有聲 $0.05／秒（https://ai.google.dev/gemini-api/docs/pricing ）；API 關閉日見 https://developers.openai.com/api/docs/deprecations 。

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是這張逐條出現的次數） |
| --- | --- | --- | --- |
| 1 | OpenAI 為什麼收掉 Sora？官方公告只給一句理由 | 30 | `title`：問題當標題，副標「官方公告只給一句理由，價目表說了其他的」；`quote`：Sora App 停止公告的英文原句，譯文隨第二句出現（1）；`stats`：Sora 2 關門前 $0.10／秒（720p）→ Veo 3.1 Lite 今天 $0.05／秒（720p 有聲）（2）；`big`：「一秒 $0.05 到 $0.40」，小字是這集的三件事。30 秒內換 6 次畫面，不用前幾支共用的「這集要講的三件事」那張 `steps` |
| 2 | Sora 的最後六個月：四個日期 | 55 | `steps`：3/24 宣布停止（App 與 API 一起）→ 4/26 網頁與 App 停止 → 匯出期限過後資料永久刪除 → 9/24 API 停止（4）；`table`：OpenAI 棄用頁原樣三列：Videos API、sora-2、sora-2-pro，關閉日 2026-09-24，建議替代欄「—」（3） |
| 3 | OpenAI 說了什麼，媒體報了什麼 | 90 | `quote`：發言人給 CBS News 的聲明原句與譯文（1）；`compare`：左「OpenAI 自己說的」（研究優先順序；聚焦、算力需求成長；研究團隊繼續做世界模擬、推進機器人；買過的點數可以改用在 Codex），右「媒體報導」（很吃算力、別的團隊分得少：Reuters，經 The Verge 轉述；算力不夠、有些事先不做：財務長受訪，Business Insider；使用人數從高峰大幅下滑：WSJ，經 TechCrunch 轉述）（2）；`bullets`：官方沒回答的三個問題（一秒影片成本多少、多少人還在用、為什麼不指定替代）（3）；`chat`：觀眾「所以 Sora 是因為太貴才收掉的？」→ 站主「官方沒這樣說；官方說的是優先順序和算力。」（2）；`big`：小標「我的讀法，不是 OpenAI 說的」，大字「影片每一秒都在燒算力」 |
| 4 | 今天 AI 影片一秒多少錢 | 150 | `code`：四種計價換成「每秒美元」，最後一行「一支 8 秒＝每秒 × 8」（實算一的算式）；`table`：Sora 2（已停）、Veo 3.1、Veo 3.1 Fast、Veo 3.1 Lite、Gemini Omni Flash，欄位「模型／條件／每秒／一支 8 秒」（5）；`table`：Kling 3.0、Dreamina Seedance 2.0、Grok Imagine Video 1.5、MiniMax-H3、Gen-4.5、Higgsfield「以官網為準」（6）；`stats`：表上最便宜 $0.05、最貴 $0.40、相差 8 倍（3）；`compare`：同一個模型，原廠 vs Runway 轉售（實算二的前兩列）（2）；`cta`：〈AI 影片工具比較〉看訂閱方案每月能生幾秒，連結在說明欄第一行 |
| 5 | 一支 60 秒短片，素材要花多少 | 90 | `steps`：60 秒 → 8 支 8 秒 → 三支留一支（假設）→ 生成 24 次（4）；`quote`：Gemini API 價目頁「You will only be charged if your video is successfully generated.」與譯文（1）；`table`：Veo 3.1 Lite $9.60、Veo 3.1 Fast $19.20、Kling 3.0 約 $24、Veo 3.1 $76.80（4）；`stats`：每「能用的一秒」Veo 3.1 Lite $0.15、Veo 3.1 $1.20，小字「三支留一支，換成你自己的比例」（2） |
| 6 | 付錢前，先查兩個頁面 | 75 | `steps`：價目表（換成每秒與一支 8 秒，寫下解析度、聲音、秒數）→ 棄用頁（最短通知期、有沒有替代）→ 匯出（存在自己的硬碟，行事曆設每季提醒）（3）；`table`：三筆官方棄用紀錄：Sora 2 與 Videos API 2026-09-24、替代「—」；Veo 3.0 2026-06-30、替代 Veo 3.1；Gemini Omni Flash 預覽版 2026-06-30 上線、2026-09-30 關閉、替代 Gemini Omni 1.1 Flash（3）；`stats`：API 從通知到關閉 184 天、App 從宣布到關閉 33 天（2） |
| 7 | 所以，OpenAI 為什麼收掉 Sora？ | 40 | `chat`：觀眾「一句話，到底為什麼？」→ 站主「官方說優先順序和算力；我的讀法是，一秒影片的帳排不到前面。」（2）；`bullets`：付錢前的三行（一秒與一支 8 秒；解析度、聲音、秒數；棄用頁與匯出提醒）（3）；`outro`：標題「先算一秒，再看 demo」，一個下一步 |

實算在第 4、5 章，第 6 章的棄用紀錄是第二個觀眾動作的示範。結尾的下一步（只有一個）：「留言告訴我：你做一支能用的 8 秒素材，平均要生成幾次？」（回到第 5 章的三支留一支假設）。總長約 530 秒，中文旁白約 2,200 字（每分鐘 250 字）；27 個場景、約 67 個畫面狀態，平均約 8 秒一個，每個狀態 1–2 句。

### 選項 B：先算你的帳：一支 60 秒 AI 短片
一行說明：從觀眾自己的一支 60 秒短片算起（秒、支、次），價目表攤開之後才點出「最有名的 Sora 不在上面」，再講 OpenAI 怎麼說；多一個做影片的人才需要的檢查（YouTube 的 AI 揭露），順序和先講新聞的 A 相反，比 C 更貼近創作者。
開場鉤子（口播）：「同樣一支 60 秒的 AI 短片，三支素材留一支的話，照今天的官方價目表，素材費從不到 10 美元到將近 77 美元都有，差在你選哪一家、幾 p。可是這張價目表上，少了一個曾經最有名的名字：Sora。這集先把帳算給你看，再看 OpenAI 自己怎麼說。」

鉤子數字：$9.60＝Veo 3.1 Lite 一支 8 秒 $0.40 × 24 次；$76.80＝Veo 3.1 一支 8 秒 $3.20 × 24 次（https://ai.google.dev/gemini-api/docs/pricing ；算法見實算三）。

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） |
| --- | --- | --- | --- |
| 1 | 一支 60 秒 AI 短片要花多少錢 | 30 | `title`；`chat`：觀眾「我想做一支 60 秒的 AI 廣告，要多少錢？」→ 站主「看你選哪一家、幾 p、三支留幾支。」（2）；`stats`：不到 $10 → 將近 $77（2）；`big`：「價目表上少了 Sora」。30 秒內換 6 次畫面 |
| 2 | 帳怎麼算：秒、支、次 | 90 | `steps`：60 秒 → 8 支 8 秒 → 三支留一支 → 24 次（4）；`code`：四種計價換成每秒（實算一的算式）；`quote`：「成功生成才收費」原句與譯文（1）；`stats`：每「能用的一秒」Veo 3.1 Lite $0.15、Veo 3.1 $1.20（2） |
| 3 | 今天各家一秒多少錢 | 130 | `table`：Google 家與 Sora 當年（5）；`table`：其他家與 Higgsfield「以官網為準」（6）；`compare`：原廠 vs Runway 轉售（2）；`cta`：〈AI 影片工具比較〉 |
| 4 | 價目表上少了 Sora：OpenAI 怎麼說 | 110 | `steps`：四個日期（4）；`quote`：App 停止公告原句與譯文（1）；`quote`：發言人聲明原句與譯文（1）；`compare`：OpenAI 原話 vs 媒體報導（標出處）（2）；`big`：站主的讀法（標明是讀法） |
| 5 | 做影片的人，付錢前查三件事 | 110 | `steps`：價目表 → 棄用頁與匯出 → YouTube Studio 的「AI 使用」揭露（3）；`quote`：YouTube 說明中心「Generates a realistic scene that didn't actually occur.」與譯文（1）；`bullets`：要揭露的三種（讓真人說或做沒做過的事、改動真實事件或地點的畫面、生成沒發生過的逼真場景）（3）；`chat`：觀眾「用 AI 做的動畫也要勾嗎？」→ 站主「不寫實的內容，官方說不用揭露。」（2）；`big`：「揭露不會限制觀眾，也不影響營利」（YouTube 說明中心的說法） |
| 6 | 所以，Sora 為什麼不在價目表上？ | 30 | `bullets`：官方說的（優先順序、算力）／價目表說的（一秒 $0.05 起）／你要做的（查兩個頁面、設一個提醒）（3）；`outro` |

實算在第 1–3 章。結尾的下一步（只有一個）：說明欄第一行的〈AI 影片工具比較〉，看訂閱方案每月能生幾秒。總長約 500 秒，中文旁白約 2,080 字；24 個場景、約 55 個畫面狀態，平均約 9 秒一個。風險：鉤子的金額建立在「三支留一支」的假設上，觀眾要到第 2 章才聽到假設怎麼來；標題問的「為什麼」到第 4 章（約 4 分鐘）才回答。

### 選項 C：給接 API 的人：六個月通知、替代欄空白
一行說明：從把影片 API 接進產品的人看 Sora：通知期、建議替代、預覽版與正式版、轉售平台的價差，「為什麼」只佔一章；最實用，但觀眾比 A、B 窄（開發者與小團隊）。
開場鉤子（口播）：「如果你的產品接的是 Sora 的 API，三月二十四號收到通知，九月二十四號就得搬完家；OpenAI 的棄用表上，建議替代那一欄是空的。今天還在賣影片 API 的幾家，一秒的價錢差到八倍。這集教你搬家前先看三個欄位，再算給你看搬到哪裡要多少錢。」

鉤子數字：通知日與關閉日見 https://developers.openai.com/api/docs/deprecations ；8 倍＝Veo 3.1 $0.40 ÷ Veo 3.1 Lite $0.05（https://ai.google.dev/gemini-api/docs/pricing ）。

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） |
| --- | --- | --- | --- |
| 1 | Sora API：六個月通知，替代欄空白 | 30 | `title`；`table`：OpenAI 棄用頁原樣三列（3）；`big`：「184 天」，小字「從通知到關閉」。30 秒內換 5 次畫面 |
| 2 | Sora 的 API 怎麼收掉的 | 70 | `steps`：3/24 通知 → 六個模型與版本一起列入 → 9/24 關閉 → 價目頁不再列 Sora（4）；`quote`：發言人聲明原句與譯文（1）；`stats`：API 184 天、App 33 天（2） |
| 3 | 別家的棄用頁怎麼寫 | 100 | `table`：Google 三筆（Veo 3.0 2026-06-30 關閉、替代 Veo 3.1；Gemini Omni Flash 預覽版上線三個月就關、替代 Gemini Omni 1.1 Flash；Veo 3.1 三個預覽版尚未公布關閉日）（3）；`compare`：Gemini API 上的預覽版 vs Gemini Enterprise Agent Platform 上的正式版（2）；`quote`：Google 棄用頁的替代寫法「or the GA models on the Gemini Enterprise Agent Platform」與譯文（1）；`chat`：開發者「預覽版可以直接上線嗎？」→ 站主「可以用，但 Omni Flash 預覽版三個月就換了。」（2）；`big`：「先看替代欄，再看價錢」；`cta`：〈Sora 影片生成教學：官方已停止服務〉 |
| 4 | 搬家候選：一秒多少錢 | 140 | `code`：四種計價換成每秒；`table`：Google 家（5）；`table`：其他家（6）；`compare`：原廠 vs Runway 轉售（2）；`stats`：最便宜、最貴、8 倍（3） |
| 5 | 接影片 API 前的三個欄位 | 120 | `steps`：最短通知期 → 建議替代 → 匯出與備援（3）；`table`：Sora 2、Veo 3.0、Gemini Omni Flash 預覽版、Veo 3.1 各自的「通知或關閉日／建議替代」，讀不到的寫「以官網為準」（4）；`chat`：開發者「用轉售平台一次接很多家不就好了？」→ 站主「方便，但同一個模型可能比原廠貴兩倍多。」（2）；`bullets`：這週就做的三件事（3） |
| 6 | 所以 Sora 教了開發者什麼？ | 40 | `big`：「替代欄空白，就自己準備替代」；`bullets`：官方說的理由／媒體報導／我的讀法（3）；`outro` |

實算在第 4 章，第 5 章把它變成清單。結尾的下一步（只有一個）：「留言告訴我：你接的影片 API，棄用頁寫的通知期是多久？」總長約 500 秒，中文旁白約 2,080 字；24 個場景、約 58 個畫面狀態，平均約 8.6 秒一個。

三個選項的場景順序和前四支（`openai-agents-broke-in`、`gpt6-vs-opus55-worth-paying`、`ai-real-jobs-chart`、`always-on-agent-explained`）的相似度，用 lint 的同一個算法估是 37%–54%，都在警告線 80% 以下。

## 會過期的事實

| 事實 | 企劃日（2026-09-28）讀到的 | 寫稿日到這裡重新確認 |
| --- | --- | --- |
| Sora API 的通知日、關閉日與建議替代 | 2026-03-24 通知；2026-09-24 關閉 Videos API、sora-2、sora-2-pro 與 sora-2-2025-10-06、sora-2-2025-12-08、sora-2-pro-2025-10-06；六列的建議替代都是「—」 | https://developers.openai.com/api/docs/deprecations （platform.openai.com/docs/deprecations 會轉到這裡） |
| Sora 網頁與 App 的停止日、匯出、刪除、點數 | 網頁與 App 2026-04-26 停止；匯出期限過後永久刪除；買過的 ChatGPT／Sora 點數可以改用在 Codex；說明裡沒有寫理由 | https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation （對抓取工具回 403；內容讀自 Wayback 2026-06-30 的存檔 https://web.archive.org/web/20260630192218/https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation ，寫稿日由真人用瀏覽器開正本）；The Decoder 2026-03-28 的報導寫的是同樣兩個日期：https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/ |
| OpenAI 有沒有補充其他理由 | 企劃日只找到兩句（見「素材」）；TechCrunch 與 The Verge 都寫 OpenAI 沒有另外解釋 | 上面的說明中心頁；OpenAI 新聞頁 https://openai.com/news/ （openai.com 對抓取工具回 403，要真人開） |
| Sora 2 當年的每秒價與單支長度 | sora-2 720p $0.10；sora-2-pro 720p $0.30、1024p $0.50、1080p $0.70（Standard）；最長 20 秒；今天的價目頁已經沒有 Sora | 存檔 https://web.archive.org/web/20260802044220/https://developers.openai.com/api/docs/pricing 、https://web.archive.org/web/20260727175148/https://developers.openai.com/api/docs/guides/video-generation ；現行 https://developers.openai.com/api/docs/pricing |
| Veo 3.1／Fast／Lite 的每秒價 | 有聲（預設）：Veo 3.1 720p 與 1080p $0.40、4k $0.60；Fast 720p $0.10、1080p $0.12、4k $0.30；Lite 720p $0.05、1080p $0.08；成功生成才收費 | https://ai.google.dev/gemini-api/docs/pricing （頁尾 Last updated 2026-09-24） |
| Veo 3.1 的秒數與解析度 | 4、6、8 秒；1080p 與 4k 只能 8 秒；Lite 不支援 4k；Gemini API 上三個 Veo 3.1 都是預覽版 | https://ai.google.dev/gemini-api/docs/veo （Last updated 2026-09-17） |
| Gemini Omni Flash 的價格 | 影片輸出每百萬 token $17.50；720p 每秒 5,792 token，頁面寫約 $0.10／秒；1080p 每秒 8,688 token | https://ai.google.dev/gemini-api/docs/pricing ；各解析度 token 數 https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing （舊的 Vertex AI 價目頁網址會轉到這裡；這頁的 Veo 價格單位寫「1 count」，沒寫每秒，所以 Veo 一律用 Gemini API 價目頁） |
| Google 的棄用紀錄 | Veo 3.0（veo-3.0-generate-001）2026-06-30 關閉，替代 Veo 3.1；Gemini Omni Flash 預覽版 2026-06-30 上線、2026-09-30 關閉，替代 gemini-omni-1.1-flash；Veo 3.1 三個預覽版「No shutdown date announced」 | https://ai.google.dev/gemini-api/docs/deprecations （Last updated 2026-09-24） |
| Kling 3.0 | 1 單位 $0.14（定價）；720p 無聲 0.6 單位、原生音訊 0.9 單位；1080p 0.8／1.2；4K 3.0；Kling 3.0 Turbo 720p 有聲 0.8；以預付資源包購買，包的價格與到期規則、可選秒數以官網為準 | https://kling.ai/dev/pricing （頁面由程式載入，數字讀自頁面原始碼裡的價目資料；寫稿日用瀏覽器看一次） |
| Dreamina Seedance 2.0 | 720p 輸入不含影片每百萬 token 7.0 美元；官方範例 720p、16:9、5 秒 $0.76；Fast $0.60、Mini $0.38（同條件）；企業用戶的限時折扣到 2026-10-07 14:00（UTC+8），表上用定價 | https://docs.byteplus.com/en/docs/ModelArk/1544106 （會轉到 model-pricing 頁；同樣由程式載入） |
| Grok Imagine Video 1.5 | 480p $0.08、720p $0.14、1080p $0.25 每秒；可選 1–15 秒 | https://docs.x.ai/developers/pricing （Last updated: September 21, 2026）；https://docs.x.ai/developers/model-capabilities/video/generation |
| MiniMax-H3 | 768P $0.08、2K $0.13 每秒（定價） | https://platform.minimax.io/docs/guides/pricing-paygo |
| Runway | 1 點 $0.01；Gen-4.5 每秒 12 點、2–10 秒、1280:720 等畫面比例；轉售：seedance2（480p／720p）36 點、veo3.1_fast 有聲 15 點、veo3.1 有聲 40 點、hailuo3（768P）10 點、grok_imagine_1_5（720p）16 點、gemini_omni_flash 10 點 | https://docs.dev.runwayml.com/guides/pricing/ ；秒數 https://docs.dev.runwayml.com/api/ |
| Higgsfield | 價目頁的數字由程式載入，讀不到，以官網為準 | https://higgsfield.ai/pricing |
| YouTube 的 AI 揭露（選項 B） | Studio 的「AI 使用」設定；讓真人說或做沒做過的事、改動真實事件或地點的畫面、生成沒發生過的逼真場景都要揭露；不寫實的內容不用；揭露不會限制觀眾或影響營利 | https://support.google.com/youtube/answer/14328491 |
| 站內文章 | 〈AI 影片工具比較〉與〈Sora 影片生成教學〉都在線上，更新日 2026-09-19（資料日 2026-09-14） | https://mokaair.com/zh-TW/life/ai-video-tools-compared 、https://mokaair.com/zh-TW/life/sora-video-guide |

## 素材

| 素材 | 路徑或網址 | 來源 | 授權與用法 |
| --- | --- | --- | --- |
| 表格、算式、數據卡 | 本片的 `table`、`code`、`stats` | Mokaair 自製，數字出自上面各官方頁 | © Mokaair |
| Sora App 停止公告（英文原句） | https://www.theverge.com/ai-artificial-intelligence/899850/openai-sora-ai-chatgpt （2026-03-24，03-25 補上公告全文） | OpenAI，經 The Verge 引述 | 短句引述，`quote` 版型標出處與日期 |
| 發言人聲明（英文原句） | https://www.cbsnews.com/news/sora-ai-openai-discontinues/ （2026-03-24） | OpenAI 發言人，經 CBS News 引述 | 同上 |
| 棄用表、價目頁 | https://developers.openai.com/api/docs/deprecations 、https://developers.openai.com/api/docs/pricing 與上面的存檔 | OpenAI 官方頁 | 頁面沒有標授權，只做短句引述與數字 |
| 「成功生成才收費」與 Veo 價格 | https://ai.google.dev/gemini-api/docs/pricing | Google 官方頁 | 頁尾寫明內容採 CC BY 4.0，引用時標出處 |
| YouTube 揭露規則（選項 B） | https://support.google.com/youtube/answer/14328491 | YouTube 說明中心 | 短句引述加出處 |
| 標明出處的報導（只做一句轉述，不放截圖） | The Verge（同上，轉述 Reuters 與 WSJ）；TechCrunch 2026-03-24 https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/ ；TechCrunch 2026-03-29 https://techcrunch.com/2026/03/29/why-openai-really-shut-down-sora/ ；Business Insider 2026-04-02 https://www.businessinsider.com/openai-cfo-says-compute-crunch-is-forcing-tough-trade-offs-2026-4 | 各媒體 | Reuters 原文 https://www.reuters.com/technology/openai-set-discontinue-sora-video-platform-app-wsj-reports-2026-03-24/ 對抓取工具回 401，只用 The Verge 的轉述 |
| 站上既有圖解（選用） | `apps/web/public/guides/ai-video-tools-compared/diagram-1.svg`、`apps/web/public/guides/sora-video-guide/diagram-1.svg` | Mokaair 自己的文章 | © Mokaair；圖裡是 2026-09-14 的方案與規格，用前要對今天的官網；全自動路線預設不用 `diagram` 版型，要不要用由站主決定 |
| 不用 | Sora 或任何模型生成的影片片段、各家 Logo、價目頁與新聞網站截圖、任何人的照片 | — | — |

## 不做的事

- 不替 OpenAI 編內部理由：官方原話放 `quote`，報導一律標媒體名與日期，站主的讀法一律標「我的讀法」。
- 不引用報導或第三方估算的營運成本、營收、下載數、使用人數、募資或投資金額；不談股票、估值、上市，也不評論任何公司的財務。
- 不用季企劃裡 Exploding Topics 的 Higgsfield 搜尋成長數字（第三方資料，不是官方頁）。
- 不排名誰的畫質最好，也不宣稱實測過：唯一的量測是把官方標價換成每秒。沒有聯盟或推薦連結。
- 不說 Sora 2 現在還能在 ChatGPT 裡用：企劃日沒有官方頁可以確認。
- 不談著作權官司、深偽爭議或授權合作的細節；不放任何生成影片的畫面。
- 不做成前四支的翻版：開場不放「這集要講的三件事」，結尾不放連續兩張 `big`。
