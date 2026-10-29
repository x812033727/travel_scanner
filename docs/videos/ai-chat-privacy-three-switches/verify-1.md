# verify-1：ai-chat-privacy-three-switches

查核第 1 輪，2026-10-29，獨立查核代理（沒有參與撰稿）。每一頁都在今天用頻道 UA
`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新抓過，同一主機間隔至少 1.5 秒，去掉 `<!-- -->` 後讀全文；
原始 HTML 與文字檔在 `<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/_tools/v1/pages/`，主張清單（每句 `text`、每張卡的 `data`）在 `_tools/v1/dump.txt`。
網路搜尋用了 1 次（Claude 的 Incognito 能不能搜尋過去的對話；沒有官方答案）。沒有用任何封存或鏡像頁。

## 網址代號與今天的狀態

| 代號 | 網址 | HTTP | 頁面日期 |
| --- | --- | --- | --- |
| GH | https://support.google.com/gemini/answer/13594961?hl=en | 200 | Last updated October 26, 2026 |
| GH-tw | https://support.google.com/gemini/answer/13594961?hl=zh-Hant | 200 | — |
| GA-tw / GA | https://support.google.com/gemini/answer/13278892?hl=zh-Hant ／ ?hl=en | 200 / 200 | 繁中頁自標「可能含有使用 AI 技術翻譯的內容」 |
| GM-tw / GM | https://support.google.com/gemini/answer/16598469?hl=zh-Hant ／ ?hl=en（另抓 `&co=GENIE.Platform%3DDesktop` 兩版） | 200 ×4 | 繁中頁自標 AI 翻譯 |
| GT / GT-tw | https://support.google.com/gemini/answer/13275745?hl=en ／ ?hl=zh-Hant（另抓繁中桌機版） | 200 ×3 | 繁中版沒有「臨時對話」那一段 |
| AT | https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training | 200 | March 16, 2026 |
| AR | https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data | 200 | July 1, 2026 |
| AS | https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings | 200 | August 3, 2026 |
| AP | https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users | 200 | March 16, 2026 |
| AI | https://support.claude.com/en/articles/12260368-use-incognito-chats | 200 | Updated over a month ago |
| AM | https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context | 200 | Updated this week |
| AX | https://support.claude.com/en/articles/8325621-i-would-like-to-input-sensitive-data-into-my-chats-with-claude-who-can-view-my-conversations（只為旁證） | 200 | May 22, 2026 |
| LC | https://learn.chatgpt.com/docs/customization/memories.md | 200 | — |
| OAI | https://help.openai.com/en/articles/7730893-data-controls-faq | **403** | 照指示不繞路 |
| RUN | `<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/runlog.txt` run 1 | — | 2026-10-29 |

## 主張表

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Gemini 關掉保留活動記錄、刪光紀錄，被審查員讀過的那段不會跟著刪，最多留三年 | open-hub hw9f、5fhw；key；縮圖 capture | GH（“past chats already reviewed by service providers aren't deleted … retained for up to 3 years”）、GH-tw 截圖段 | 200 | CONFIRMED | — |
| 2 | 關掉的只是訓練；還可能被記住、讀到、留下來 | open-answer r8j6 | GH、AP、AM、AR | 200 | CONFIRMED（都有「可能」） | — |
| 3 | 三個開關、一次測試、一張表 | open-promise | — | — | OUT OF SCOPE | — |
| 4 | 假履歷內容全是編的 | ch1-resume | — | — | OUT OF SCOPE | — |
| 5 | 送出去第一件事是回答你，三家都一樣 | ch1-flow 2uzy | GH（“to respond to you”）；Claude、ChatGPT 自明 | 200 | CONFIRMED | — |
| 6 | 記憶開著可能被記下帶到下次；訓練開著可能拿去改良；可能被審查員或安全團隊讀到 | ch1-flow bnp3、cdi4、suyd、steps | GH、AT、AP、AM | 200 | CONFIRMED | — |
| 7 | Gemini 保留活動記錄滿 18 歲預設開啟 | ch1-defaults 6quk | GA-tw「如果你年滿 18 歲，「保留活動記錄」會預設為開啟」；GA | 200 | CONFIRMED | — |
| 8 | Claude 記憶 Free、Pro、Max 預設開啟 | ch1-defaults 8ya3 | AM “Memory is on by default for Free, Pro, and Max plans” | 200 | CONFIRMED | — |
| 9 | Claude 搜尋過去對話是付費方案、推出後預設開啟 | ch1-defaults ntiw | AM “available to users on paid plans”；“it will be enabled by default” | 200 | CONFIRMED | — |
| 10 | Gemini 關紀錄或臨時對話，仍用對話保護 Google、使用者、大眾，可能有人工審查（引言） | ch1-gemini-quote ihcc、jjhj、quote | GH-tw 第 235 行同句；GH | 200 | CONFIRMED | — |
| 11 | Claude 員工預設看不到；例外是回饋或安全審查，只有 Trust & Safety 指定成員 | ch1-claude-quote w3tx、agxq、9pw6、quote | AP | 200 | CONFIRMED | — |
| 12 | 頻道影片用 Claude 做 | ch1-disclose | brief〈站主觀點〉 | — | CONFIRMED（站主陳述） | — |
| 13 | 關掉訓練只回答四題中的一題；記憶、審查、保留都還沒動 | ch2-compare haan | GH、AM、AR | 200 | CONFIRMED | — |
| 14 | 關掉訓練後 Gemini 記憶跟著停、Claude 記憶照樣開著 | ch2-table 記憶列；aj4i | GM-tw「如關閉此設定，就無法使用這項功能」；AM、AS（兩個設定頁） | 200 | CONFIRMED | — |
| 15 | 人工審查：Gemini 仍可能 | ch2-table；yvka 前半 | GH | 200 | CONFIRMED | — |
| 16 | 人工審查：Claude「被標記才看」／「要被安全系統標記，才會有人看」 | ch2-table rows[1][2]；yvka | AP：例外是「送回饋」或「為執行 Usage Policy 需要審查」 | 200 | **CHANGED**（「才會」是唯一條件，漏了回饋這個例外，且關掉訓練後仍可送回饋） | 「被標記才看」→「回饋或被標記才看」；yvka「Claude 要被安全系統標記，才會有人看。」→「Claude 要你送回饋或被安全系統標記，才會有人看。」 |
| 17 | 保留：Gemini 關掉紀錄後 72 小時 | ch2-table；2gun | GH “Future chats are still saved for 72 hours”；GA-tw | 200 | CONFIRMED | — |
| 18 | Claude 刪掉的對話 30 天內從後端刪除 | ch2-table；gsps | AR “Deleted from our back-end storage systems within 30 days” | 200 | CONFIRMED | — |
| 19 | ChatGPT 保留天數沒查到；記憶在 Settings > Personalization | ch2-table ChatGPT 欄；sdjw | LC “Manage ChatGPT memory from Settings > Personalization”；OAI 403 | 200 / 403 | CONFIRMED（沒查到是實情） | — |
| 20 | Gemini 個人化記憶要先開著保留活動記錄，一關就不能用 | ch2-memory-page 6neu、截圖 | GM-tw、GM | 200 | CONFIRMED | — |
| 21 | 在 Gemini 想被記得，保留活動記錄就得開著，對話也會被拿去改良服務、包括訓練模型 | ch2-tied hxei、p5hz | GH “Google uses your activity to provide, develop, and improve its services (including training generative AI models)” | 200 | CONFIRMED | — |
| 22 | Claude 訓練和記憶是兩個分開的開關 | ch2-claude-separate | AS（Privacy）、AM（Your Claude） | 200 | CONFIRMED | — |
| 23 | Gemini 臨時對話留 72 小時、不訓練；不能用 Gem、沒有個人化回覆 | ch2-temp-compare；c9sx、pvzn | GH “Temporary chats … retained with your account for 72 hours”、“not used to train”；GT “you can't: Use Gems … Get personalized responses” | 200 | CONFIRMED | — |
| 24 | Claude Incognito 不訓練、不進記憶，留 30 天，是十倍 | ch2-temp-compare；m999 | AI “retained for either 30 days (default)”；30 天 ÷ 72 小時 = 10 | 200 | CONFIRMED | — |
| 25 | Incognito 裡仍讀得到個人偏好 | ch2-temp-compare；v4nx | AI FAQ “Yes, Claude can access this information within an incognito chat.” | 200 | CONFIRMED | — |
| 26 | 選法表：不想被訓練關訓練；不想被記住關記憶或開臨時模式；不想被讀到別貼；兩家都沒有開關能完全關掉人工讀到 | ch2-rule rnju–p89k | GH（關了仍可能人工審查）、AP（Usage Policy 審查） | 200 | CONFIRMED（「別貼」是建議） | — |
| 27 | Gemini：電腦版 設定與說明 → 活動記錄 → 畫面上方「開啟」→「關閉」或「關閉並刪除活動記錄」 | ch3-gemini-steps hsbb、dpty、gpm4；steps；說明欄 | GA-tw 原句；GA “Click Settings & help Activity … Near the top, click On Turn off or Turn off and delete activity” | 200 | CONFIRMED（字樣見下〈第 4 項〉） | — |
| 28 | 自動刪除預設 18 個月，可改 3、36 個月或不自動刪除 | ch3-gemini-steps imd7、steps；說明欄 | GA-tw、GA、GH | 200 | CONFIRMED | — |
| 29 | 一關掉，Workspace 這類連結的應用程式一起停用 | hb6y | GH “other Connected Apps like Google Workspace are unavailable if you turn off Keep Activity”；GA 只剩 Device assistance、Notebook、Messages、Phone、WhatsApp | 200 | CONFIRMED | — |
| 30 | 關掉後新對話不再出現在活動記錄 | ch3-gemini-page mbuz、截圖 | GH、GA-tw | 200 | CONFIRMED | — |
| 31 | Claude 訓練開關：Settings → Privacy → Help Improve our AI models | ch3-claude-steps jym8、f9n8、steps；說明欄 | AS “Under Help Improve our AI models, click the button to toggle it off/on” | 200 | CONFIRMED | — |
| 32 | 關掉後新舊對話都不再用於之後的訓練；已開始的訓練、訓練好的模型收不回 | ch3-claude-past xkc5–fj5x | AS、AR | 200 | CONFIRMED | — |
| 33 | 手機：名字、Settings、Privacy，同一個開關 | ch3-claude-page k7h3、截圖 | AS 手機四步 | 200 | CONFIRMED | — |
| 34 | 記憶：Settings → Your Claude → Memory from chats；Pause 暫停、舊的留著；Reset 全刪無法復原 | ch3-claude-memory 33zp、b4rg；說明欄 | AM | 200 | CONFIRMED | — |
| 35 | 單次不進記憶：送出第一句前，「+」選單關 Memory | ch3-claude-single vwvq；說明欄 | AM “Click "+" in the message box. Click "Memory" to turn it off for this chat.” | 200 | CONFIRMED | — |
| 36 | Incognito：右上角幽靈圖示，只在專案外 | z4x7；說明欄 | AI、AM | 200 | CONFIRMED | — |
| 37 | 不翻舊對話：Your Claude 同一頁的 Search and reference chats 關掉 | ghcz | AM “Settings > Your Claude … Search and reference chats off” | 200 | CONFIRMED | — |
| 38 | ChatGPT 記憶：Settings → Personalization；訓練與臨時對話請自己對 | ch3-chatgpt-steps mak3、wz26、npzc；說明欄 | LC；OAI 403 | 200 / 403 | CONFIRMED | — |
| 39 | 「我的設法」：訓練關、記憶留著每月看；Gemini 兩件綁在一起，只能二選一 | ch3-my-way qhms–8qxa | brief〈站主觀點〉；GM-tw＋GH（記憶要開保留活動記錄，開著就用於訓練） | 200 | CONFIRMED（看法標了「我的看法是」；「只能二選一」見〈第 5 項〉） | — |
| 40 | 金絲雀：一般對話貼履歷，新的一般對話問代號 | ch4-canary-chat gpgn、v676、ezcu | 指示，非結果 | — | OUT OF SCOPE | — |
| 41 | 記憶開著可能答得出來 | ch4-expect 8yh7、左欄 | AM、GM（預期結果，有「可能」） | 200 | CONFIRMED | — |
| 42 | 臨時對話「或 Incognito」裡問，不用既有記憶，應該答不出來 | ch4-expect 3nbs、右欄標題 | GT（臨時對話不能個人化）；AI 只寫 Incognito 不用既有記憶，**沒寫 Incognito 能不能搜尋過去的對話**；AM：付費方案搜尋預設開著，單次關記憶的對話 “doesn't search your past chats from it” | 200 | **CHANGED**（Incognito 那一半沒有官方根據；改用官方明寫不用記憶、也不搜舊對話的單次關記憶對話，brief 的金絲雀本來就列了這個模式，第 3 章已介紹過） | 標題「臨時對話・Incognito」→「臨時對話・單次關記憶」；3nbs「同一句改到臨時對話或 Incognito 裡問，它不用既有的記憶，應該答不出來。」→「同一句改到臨時對話，或 Claude 單次關掉記憶的對話裡問，應該答不出來。」；claims c29 → c20 |
| 43 | Gemini 可問「你是否使用過往對話中的任何資訊？」「你知道我哪些事？」 | ch4-ask mhre、3ieu、卡片 | GM-tw、GH-tw 第 281 行 | 200 | CONFIRMED | — |
| 44 | Gemini 臨時對話上方有臨時對話圖示 | ch4-marks 8h3j | GT | 200 | CONFIRMED | — |
| 45 | Claude Incognito 黑色外框、左上角 Incognito chat | 66ii | AI | 200 | CONFIRMED | — |
| 46 | 單次關記憶，送出第一句後標題旁有劃掉的記憶圖示 | t6g7 | AM（網頁與桌面版；手機版是鎖住的開關，卡片未提） | 200 | CONFIRMED | — |
| 47 | Claude 付費方案翻舊對話時出現工具呼叫 | mu6r | AM “will appear as tool calls” | 200 | CONFIRMED | — |
| 48 | Gemini 要刪掉含那句的每一段對話，會有一小段延遲 | ch4-delete y6nv、左欄 | GM-tw | 200 | CONFIRMED | — |
| 49 | Claude 刪對話，記憶不跟著刪；Your Claude 按 Manage 刪那一條 | 7ixk、98am、右欄 | AM | 200 | CONFIRMED | — |
| 50 | 兩家刪法剛好相反 | ny5m | 同上 | 200 | CONFIRMED（概括） | — |
| 51 | 兩張 terminal 卡逐字取自 runlog 第 1–5、6–10 行；指令、Node 版本 | ch5-term1、ch5-term2 | RUN；`_tools/v1/term.py` 10/10 行逐字相符；lifespan.mjs 期限與官方頁一致 | — | CONFIRMED | — |
| 52 | 起算 2026-10-29；Gemini 關紀錄／臨時對話 11 月 1 日清掉 | m9se、rq75 | RUN；GH 72 小時 | 200 | CONFIRMED | — |
| 53 | 開著不動到 2028 年 4 月 | uevg、pskv | RUN；GA 18 個月 | 200 | CONFIRMED | — |
| 54 | 自動刪除改三個月，是明年一月底 | 8qtx、key | RUN 2027-01-29；GA “activity older than 3 months is auto-deleted” | 200 | CONFIRMED（見〈第 6 項〉） | — |
| 55 | 審查過的對話先跟帳戶斷開，刪活動記錄刪不到；假設今天讀到，最晚 2029 年 10 月 | ch5-reviewed 7kgs、j56c、卡片 | GH “Chats are disconnected from your account before being sent to service providers”、“retained for up to three years”；RUN | 200 | CONFIRMED（假設已標明） | — |
| 56 | 三年從哪一天算起，我查不到 | ch5-unknown xpvk | GH、GH-tw 都沒寫起算日 | 200 | CONFIRMED | — |
| 57 | Claude 刪掉的對話和 Incognito，11 月 28 日清掉 | x3b4 | AR 30 天內、AI 30 天；RUN | 200 | CONFIRMED | — |
| 58 | Claude 沒刪的一般對話沒有固定保留天數 | 7zax；說明欄 | AR “as long as reasonably necessary” | 200 | CONFIRMED | — |
| 59 | 開著改良：去識別化資料最多到 2031 年 | 9nng、6qvm | AR “de-identified format for up to 5 years … only applies to new or resumed chats after the model training setting has been enabled”；RUN | 200 | CONFIRMED（今天的新對話適用） | — |
| 60 | 被標記：內容最多到 2028 年；分類分數到 2033 年 | p3y5、6jde | AR “inputs and outputs for up to 2 years and trust and safety classification scores for up to 7 years” | 200 | CONFIRMED | — |
| 61 | 按讚／倒讚的整段對話留到 2031 年 | d6ys | AT “for up to 5 years”；AR “for 5 years” | 200 | CONFIRMED | — |
| 62 | 誰決定表：72 小時、30 天／3、18、36 個月／5 年按之前管得到／3 年審查員讀過管不到／2、7 年安全系統標記管不到 | ch5-who 全表與 a8jv–6f2b | GH、GA、AR、AT | 200 | CONFIRMED | — |
| 63 | 最長的那一格是七年，跟訓練開關無關 | ch5-big7 zad2 | AR（標記不看設定）；AS “If our safety classifiers flag your conversations, they may still be used…” | 200 | CONFIRMED（「那一格」指表內；Gemini「不自動刪除」比它長，但那是你選的） | — |
| 64 | 刪掉管的是自己那份紀錄；按過回饋的那一段另外存了一份 | ch5-deleted-q tqwm | AR 把 Feedback Data 列為獨立類別、“retain data associated with that submission for 5 years”（刪對話是 30 天）；AT “store the entire related conversation … for up to 5 years”；GH 審查過的回饋刪了也留 | 200 | CONFIRMED（見〈第 1 項〉） | — |
| 65 | 按讚倒讚：整段對話連同風格、偏好存最多五年；使用前拿掉帳號識別 | ch5-feedback-quote ezqj、83s7、引言 | AT | 200 | CONFIRMED | — |
| 66 | Gemini 審查過的回饋和相關對話最多三年 | th6g | GH “Reviewed feedback, associated conversations, and related data are retained for up to 3 years” | 200 | CONFIRMED | — |
| 67 | 有個資的對話不按讚也不按倒讚；按下去留得比任何關掉的開關都久 | ch5-my-feedback | brief〈站主觀點〉；AT 5 年 | 200 | CONFIRMED（看法，標「我的做法」） | — |
| 68 | 今天三件事：關訓練；Gemini 想留記憶就別關、改自動刪除三個月；記憶打開看一次；別人的個資不貼，臨時模式也一樣 | ch6-actions emfq–5irf | brief〈站主觀點〉；GA | 200 | CONFIRMED（事實部分）；看法見摘要 | — |
| 69 | 收尾：關掉訓練只填了四格裡的一格 | closing 5hcs | 同 #13 | — | CONFIRMED | — |
| 70 | 標題「關掉訓練，還有兩個開關開著」；縮圖「還剩兩個開關」 | youtube.title、thumbnail | GH、AM、AP | 200 | CONFIRMED（概括；Gemini 關掉後記憶也停，見摘要） | — |
| 71 | 說明欄：Gemini 個人化記憶 設定與說明 → 個人化智慧服務 → 個人化記憶 | youtube.description | GM-tw 桌機版「依序點按畫面底部的「設定與說明」圖示「個人化智慧服務」」；GM 桌機版 | 200 | CONFIRMED | — |
| 72 | 說明欄：臨時對話是「新對話」旁邊的「臨時對話」 | youtube.description | GT “Next to New chat, click Temporary chat”；GT-tw 把 New chat 寫成「新的對話」 | 200 | **CHANGED**（按鈕字樣） | 「新對話」→「新的對話」 |
| 73 | 說明欄：OpenAI 說明中心 403，所以沒有 ChatGPT 的訓練、臨時對話天數、人工審查 | youtube.description | OAI 今天 403 | 403 | CONFIRMED | — |
| 74 | 說明欄：實算方法、假設、未實測、不談企業版 | youtube.description | RUN；claims D1–D3 | — | CONFIRMED | — |
| 75 | tags | youtube.tags | — | — | OUT OF SCOPE | — |

## 撰稿人請查核判斷的八件事

1. 「按過回饋的那一段，另外存了一份」：保留。AR 把回饋資料列成獨立類別、固定保留 5 年（刪對話是 30 天內）；AT 寫按讚倒讚時把整段對話存在後端。「另外存一份」有原句支撐。不改成「另外存最多五年」，因為這句同時講 Gemini（下一張卡說三年）。
2. 「Claude 被標記才看」：改了。AP 的例外是「回饋」或「為執行 Usage Policy 需要審查」；「才會」說成唯一條件就錯了，而且關掉訓練以後仍然可以送回饋。改成表格「回饋或被標記才看」、旁白「Claude 要你送回饋或被安全系統標記，才會有人看。」
3. Claude Incognito 能不能搜尋過去的對話：官方頁沒寫。AI 只寫 Incognito 不用既有記憶，以及 Incognito 對話不會被搜尋到；AM 明寫單次關記憶的對話既不用記憶也不搜舊對話。付費方案搜尋預設開著，金絲雀又在一般對話裡，所以「Incognito 裡應該答不出來」沒有根據。ch4-expect 改成單次關記憶的對話（brief 的金絲雀本來就列了它）。
4. Gemini 選單字樣：英文頁是 Settings & help → Activity → On → Turn off／Turn off and delete activity；Settings & help → Personal Intelligence → Memory；Next to New chat → Temporary chat。繁中頁對應「設定與說明」「活動記錄」「開啟」「關閉」「關閉並刪除活動記錄」「個人化智慧服務」「個人化記憶」。沒有頁面寫出台灣介面實際顯示的字（活動記錄頁與記憶頁都自標 AI 翻譯），所以只能用繁中說明頁的字。唯一不一致的是說明欄的「新對話」：繁中說明頁寫「新的對話」，已改。繁中頁沒有「臨時對話」按鈕那一段，「臨時對話」這個字取自繁中隱私權專區。
5. 「只能二選一」（Gemini 訓練或記憶）：成立。GM／GM-tw 寫個人化記憶要開著保留活動記錄；GH 寫保留活動記錄開著時，活動會用於改良服務，包括訓練生成式 AI 模型。GH 沒有另外的訓練開關，Gemini 設定也管不到匿名化處理。所以「訓練關、記憶開」的組合不存在。
6. 「明年一月底」：成立。2026-10-29 加 3 個月是 2027-01-29，GA 原句是 “activity older than 3 months is auto-deleted”。GA 也寫刪除會「立刻開始」，再跑一套從儲存系統刪除的程序，所以那天是開始刪的日子，不保證當天從儲存系統完全消失。旁白沒改，最晚 72 小時、30 天兩處也是同樣的讀法。
7. Gemini 審查過的「最多三年」：GH 和 GH-tw 都沒寫從哪一天起算。只寫 “Reviewed chats are retained for up to three years”，以及 “Data reviewed by service providers is disconnected from your account and saved for 3 years”。稿子已經說「我查不到」，卡片也標了「假設當天就被審查」，不用改。
8. Claude 的保留期限：AR（July 1, 2026）原句，全部成立：開著改良，去識別化資料最多 5 年，只算開啟之後的新對話或續聊的對話；刪掉的對話 30 天內從後端刪除；Incognito 30 天（AI）；被自動 trust and safety 系統標記的對話，輸入輸出最多 2 年、分類分數最多 7 年；回饋資料 5 年。開關名稱是 **Help Improve our AI models**（AS 兩段步驟都這麼寫）；AR、AS 內文另稱它 “model training setting”／“model improvement setting”，旁白用「改良模型的開關」，沒有問題。

## 摘要

- 查核主張：75；CONFIRMED 68、CHANGED 3（全是事實：#16、#42、#72）、NOT FOUND 0（#42 的 Incognito 部分查不到，用改寫解決）、OUT OF SCOPE 4（#3、#4、#40、#75）。
- 會過期的事實：Gemini 隱私權專區 Last updated 2026-10-26；Anthropic 保留頁 2026-07-01、改良設定頁 2026-08-03、訓練頁與保護頁 2026-03-16；Claude 記憶頁 “Updated this week”，這頁變動頻繁，上片前再對一次。全部期限都是從 2026-10-29 起算，上片日期晚了，日期要重跑。
- 公司歸屬：每個主張都對到正確的公司；Gemini 的三年與 Claude 的五年、七年沒有混用。ChatGPT 只給選單位置，旁白明說沒查到。
- 看法：ch3-my-way、ch5-my-feedback、ch6、closing 都標了「我的看法是／我的做法」，也跟 brief 一致。有一處不一致只報告不改：ch6 的 dtxb「在 Gemini，想留記憶就別關，改成自動刪除三個月」等於替站主選了 Gemini 留記憶、訓練照開。brief 寫「訓練我關掉」，沒有處理 Gemini 綁在一起的情況，請站主確認。
- 實測：旁白沒有說、也沒有暗示用真實帳號測過。第 4 章只放觀眾要打的字，結果用「可能／應該」，卡片標「依官方說明的預期結果」。有兩句措辭像示範：bhtz「這份假履歷，現在要貼進…」與 emfq「假履歷測完了，回到你自己的帳號」。它們沒有宣稱任何結果，所以沒改；站主如果想更保險，可以改成教學口吻。
- 聽眾檢查：
  - 新的 yvka 約 43 字（含英文），略超過 40，lint 沒有警告；
  - 沒有「經查證／根據官方文件／本影片」這類字，沒有括號或網址；
  - 拉丁字的發音交給撰稿時加的發音字典（17 個詞都是 `null`，還沒試聽），這部分沒查；
  - 揭曉順序沒問題：3nbs 用的「單次關掉記憶」在第 3 章 vwvq 已經介紹過。
- lint（`VIDEO_WORKDIR=<VIDEO_WORKDIR> node tools/video/cli.mjs lint --slug ai-chat-privacy-three-switches`）：修改後 0 errors、0 warnings，估計 12.3 分鐘、140 句。
- 懷疑但沒改：
  - AX（May 22, 2026）寫開著改良模型時，“a small number of personnel involved in model training” 會在去連結後審查資料。這是 AP「例外有兩個」以外的第三種人讀到的情況，只在訓練開著時成立；稿子主軸是關掉訓練之後，所以沒改。
  - 說明欄第一句「帶你在 Gemini、Claude、ChatGPT 找到訓練、記憶、人工審查三個開關」：ChatGPT 實際只給了記憶位置，Claude 也沒有人工審查的開關，算概括。
  - 標題「還有兩個開關開著」在 Gemini 不完全成立：關掉保留活動記錄後記憶也停了。
  - ch4-marks t6g7 的「劃掉的記憶圖示」只適用網頁與桌面版。
  - ch4-expect 改寫後 claims 不再引用 c29（Incognito 不用既有記憶），c29 還留在 claims.md。
- 第二輪：不需要。本輪 3 個事實改動，沒有超過三個。但 #42 改了第 4 章測試的說法，建議站主看一眼。
