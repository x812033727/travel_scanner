# claims：ai-chat-privacy-three-switches

撰稿 2026-10-29。選項 A（站主 2026-10-29 核准，`approvals.json` 綁 brief.md 的 sha256 71f1613e…）。每一頁都在 2026-10-29 用頻道 UA
（`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓過，HTTP 200、最終網址同下；原始 HTML 在
`<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/_tools/recheck/`，逐字比對用 `_tools/verify.py`（第一輪 74 個、補查 16 個原句片段都找到；
兩處只是字樣不同：英文版 Gemini 活動記錄頁的按鈕是 “Turn off and delete activity”，Anthropic 那句是 “previously stored chats and coding sessions”）。

格式：`id｜主張（旁白或卡片上的說法）｜官方網址（原句）｜查證日｜場景`

## 示範紀錄（輸入、動作、預期、實際、證據）

| 項目 | 輸入 | 動作 | 預期 | 實際 | 證據等級 |
| --- | --- | --- | --- | --- | --- |
| D1 實算 | `_tools/lifespan.mjs`（期限寫死在檔內，每列一個官方頁的數字），起算 2026-10-29 | `node _tools/lifespan.mjs`，Node v22.22.0，2026-10-29T00:51:51Z | 9 列日期，72 小時落在 2026-11-01、7 年落在 2033-10-29 | runlog run 1：10 行輸出（起算行＋9 列），exit 0，日期與企劃表相同 | 跑過（RUN）：`runlog.txt` run 1 |
| D2 ChatGPT 說明中心 | https://help.openai.com/en/articles/7730893-data-controls-faq | 撰稿當天用頻道 UA 試一次（`_tools/recheck.sh`） | 填 ChatGPT 的訓練開關、Temporary Chat 天數、人工審查 | HTTP 403（Cloudflare 擋頁，存為 `recheck/oai-datacontrols.html`）；照站主指示不繞路，ChatGPT 只給記憶的選單位置 | 引用（只有 learn.chatgpt.com 一頁） |
| D3 金絲雀測試 | 假履歷最後一行「我最喜歡的顏色是薄荷綠，代號 MINT-42」 | 一般對話貼上 → 新的一般對話問「我最喜歡的顏色代號是什麼？」→ Gemini 臨時對話／Claude 單次關記憶的對話問同一句（查核第 1 輪由 Incognito 改）；Gemini 另問「你是否使用過往對話中的任何資訊？」 | 記憶開著：可能答得出；臨時對話／Incognito：不用既有記憶、應該答不出 | **未實測**：站主決定不錄自己的帳號（2026-10-29），沒有人跑過 | 引用（預期結果，卡片標「依官方說明的預期結果」） |
| D4 公開頁截圖 | 4 個 `screencast` 場景的步驟 | 撰稿時在 scratch 工作區（不是正式工作區）用 `tools/video/screencast/capture.mjs` 的 `ensureCaptures` 對真頁面跑一次 | 每景一張，焦點框到指定段落 | 4 景都成功：隱私權專區的「「保留活動記錄」設定控管哪些項目？」摺疊段點開後框到「刪除活動記錄並不會刪除…最多會保留 3 年」；其餘三頁直接框到目標段 | 看過公開頁（不登入） |

設定步驟（關訓練、關記憶、開臨時模式、刪記憶）不是成果，是「關掉／留下來」那一步，全部引用官方說明頁，卡片標頁面與日期。

## 主張

c1｜Gemini：被審查員（服務供應商）審查過的對話與相關資料，刪除活動記錄時不會刪除，因為已跟 Google 帳戶斷開，最多保留三年｜https://support.google.com/gemini/answer/13594961?hl=en（“Chats reviewed by human reviewers … are not deleted when you delete your activity. Instead, they are retained for up to three years.”；“If you delete your activity, past chats already reviewed by service providers aren't deleted because they aren't connected to your Google Account. Instead, they're retained for up to 3 years.”）；繁中 https://support.google.com/gemini/answer/13594961?hl=zh-Hant（「刪除活動記錄並不會刪除服務供應商審查過的對話…這些資料最多會保留 3 年」「系統會先解除對話與帳戶之間的連結」）｜2026-10-29｜open-hub, ch5-term1, ch5-reviewed, ch5-who
c2｜Gemini：即使關閉「保留活動記錄」或使用臨時對話，Google 仍用對話回覆你，並保護 Google、使用者和一般大眾，過程可能有人工審查｜https://support.google.com/gemini/answer/13594961?hl=en（“Even if your Keep Activity setting is off or you use temporary chats, Google still uses your chats to respond to you and help protect Google, our users, and the public, including with help from human reviewers.”；卡片引繁中版同段）｜2026-10-29｜open-answer, ch1-flow, ch1-gemini-quote, ch2-compare, ch2-table, ch2-rule
c3｜Gemini：關閉「保留活動記錄」後，之後的對話不出現在活動記錄、不用於訓練（除非送回饋），仍保存 72 小時｜https://support.google.com/gemini/answer/13594961?hl=en（“Your future chats won't appear in your Activity, and won't be used to train our AI models, unless you choose to send Google feedback. Future chats are still saved for 72 hours …”）；https://support.google.com/gemini/answer/13278892?hl=zh-Hant（「最多保留 72 小時…這項活動不會出現在 Gemini 系列應用程式活動記錄裡」）｜2026-10-29｜ch2-table, ch3-gemini-page, ch5-term1, ch5-who
c4｜Gemini：臨時對話以帳戶保存 72 小時、不用於訓練；臨時對話不能用 Gem、需要保留活動記錄的連結應用程式、個人化回覆、回饋｜https://support.google.com/gemini/answer/13594961?hl=en（“Temporary chats and chats you have when Keep Activity is off are retained with your account for 72 hours”；“Temporary chats are not used to train Google's AI models.”）；https://support.google.com/gemini/answer/13275745?hl=en（“When using a temporary chat you can't: Use Gems. … Get personalized responses. … Give feedback about the response.”）｜2026-10-29｜ch2-temp-compare, ch4-expect, ch5-term1
c5｜Gemini：「個人化記憶」需要開啟「保留活動記錄」，關閉就無法使用｜https://support.google.com/gemini/answer/16598469?hl=zh-Hant（「開啟保留活動記錄。如關閉此設定，就無法使用這項功能。」；英文 “Have Keep Activity on. This feature isn't available when this setting is off.”）｜2026-10-29｜ch2-table, ch2-memory-page, ch3-my-way
c6｜Gemini：保留活動記錄開著時，活動用於提供、開發、改良服務（包括訓練生成式 AI 模型），並有人工審查｜https://support.google.com/gemini/answer/13594961?hl=en（“Google uses your activity to provide, develop, and improve its services (including training generative AI models), as well as to protect Google, its users, and the public with the help of human reviewers.”）｜2026-10-29｜ch1-flow, ch2-tied
c7｜Gemini：「保留活動記錄」年滿 18 歲預設開啟｜https://support.google.com/gemini/answer/13278892?hl=zh-Hant（「如果你年滿 18 歲，「保留活動記錄」會預設為開啟。」）｜2026-10-29｜ch1-defaults
c8｜Gemini：關閉路徑：電腦版 gemini.google.com →「設定與說明」→「活動記錄」→ 畫面上方「開啟」→「關閉」或「關閉並刪除活動記錄」｜https://support.google.com/gemini/answer/13278892?hl=zh-Hant（「依序點按「設定與說明」圖示「活動記錄」圖示」「在畫面上方，依序點按「開啟」「關閉」或「關閉並刪除活動記錄」」）｜2026-10-29｜ch3-gemini-steps, ch3-gemini-page
c9｜Gemini：活動記錄預設 18 個月自動刪除，可改 3、36 個月或不自動刪除｜https://support.google.com/gemini/answer/13278892?hl=zh-Hant（「根據預設，系統會自動刪除 18 個月前的…可以停用自動刪除功能，或是將保留期限調整為 3 或 36 個月」）；Privacy Hub（“from the default of 18 months to 3 months, 36 months, or indefinite”）｜2026-10-29｜ch3-gemini-steps, ch5-term1, ch5-who
c10｜Gemini：關閉保留活動記錄時，Google Workspace 這類連結的應用程式無法使用｜https://support.google.com/gemini/answer/13594961?hl=en（“other Connected Apps like Google Workspace are unavailable if you turn off Keep Activity”）｜2026-10-29｜ch3-gemini-steps
c11｜Gemini：可問「你是否使用過往對話中的任何資訊？」確認是否用了過往對話；記憶摘要可問「你知道我哪些事？」｜https://support.google.com/gemini/answer/16598469?hl=zh-Hant（「只要詢問 Gemini「你是否使用過往對話中的任何資訊？」」；英文 “Did you use any info from past chats?”）；https://support.google.com/gemini/answer/13594961?hl=zh-Hant（「輸入提示詞：你知道我哪些事？」；英文 “What do you know about me?”）｜2026-10-29｜ch4-ask
c12｜Gemini：臨時對話時，畫面上方有臨時對話圖示；開法是「新的對話」旁的「臨時對話」（查核第 1 輪：繁中說明頁 13275745?hl=zh-Hant 把 New chat 寫成「新的對話」；繁中頁沒有臨時對話那一段）｜https://support.google.com/gemini/answer/13275745?hl=en（“When you're in a temporary chat, the temporary chat icon will be at the top of the screen.”；“Next to New chat, click Temporary chat.”）｜2026-10-29｜ch4-marks
c13｜Gemini：要刪掉 Gemini 記住的事，刪除含那項資訊的所有對話；刪除後可能有一小段延遲才停止拿來個人化｜https://support.google.com/gemini/answer/16598469?hl=zh-Hant（「刪除含有個人資訊的所有對話」「可能需要經過一小段時間，Gemini 才會停止使用該對話記錄提供個人化回覆」）｜2026-10-29｜ch4-delete
c14｜Gemini：審查過的回饋、相關對話與資料，與帳戶斷開，最多保留 3 年｜https://support.google.com/gemini/answer/13594961?hl=en（“Reviewed feedback, associated conversations, and related data are retained for up to 3 years, disconnected from your Google Account.”）｜2026-10-29｜ch5-feedback-quote
c15｜Claude：員工預設不能存取你的對話，除非你送回饋，或為執行 Usage Policy 需要審查，這時只有 Trust & Safety 團隊的指定成員能看｜https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users（March 16, 2026；“By default, Anthropic employees cannot access your conversations unless: … feedback … Review is needed to enforce our Usage Policy … only designated members of our Trust & Safety team may access this data”）｜2026-10-29｜open-answer, ch1-flow, ch1-claude-quote, ch2-table, ch2-rule（查核第 1 輪：ch2-table 那一格與 yvka 原本只寫「被標記才看」，漏了回饋這個例外，改成「回饋或被標記才看」）
c16｜Claude：消費者方案（Free、Pro、Max）在你允許、對話被標記做安全審查、或另外加入訓練（如 Trusted Tester）時使用對話改良模型｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training（March 16, 2026）｜2026-10-29｜ch1-flow
c17｜Claude：訓練開關在 Settings → Privacy →「Help Improve our AI models」；手機同樣是名字選單 → Settings → Privacy → 同一個開關；與記憶是不同的設定頁｜https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings（August 3, 2026；“Under Help Improve our AI models, click the button to toggle it off/on”）｜2026-10-29｜ch2-claude-separate, ch3-claude-steps, ch3-claude-page
c18｜Claude：關掉後，新的與已存的對話都不再用於之後的訓練；已開始的訓練與已訓練好的模型不受影響｜https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings（“we will not use any new chats and coding sessions … Your data will still be included in model training that has already started and in models that have already been trained, but we will stop using your previously stored chats and coding sessions in future model training runs”）｜2026-10-29｜ch3-claude-past
c19｜Claude：記憶對 Free、Pro、Max 預設開啟；Settings → Your Claude →「Memory from chats」；關閉時 Pause memory（保留舊的、不用也不新增）或 Reset memory（永久刪除，無法復原）｜https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context（“Memory is on by default for Free, Pro, and Max plans”；“Reset memory: Permanently deletes all memories … this cannot be undone”）｜2026-10-29｜open-answer, ch1-defaults, ch2-compare, ch2-table, ch2-tied, ch2-claude-separate, ch3-claude-memory
c20｜Claude：只有這一次不用記憶：送出第一則訊息前，在「+」選單關掉 Memory；送出後標題旁出現劃掉的記憶圖示｜同上（“Click "+" in the message box. Click "Memory" to turn it off for this chat.”；“a crossed-out memory icon appears next to the chat title”；“If you turn off memory in the “+” menu when you start a new chat, Claude doesn't use memory in that chat, doesn’t search your past chats from it”）｜2026-10-29｜ch3-claude-single, ch4-marks, ch4-expect
c21｜Claude：Incognito 不存進對話歷史與記憶、不用於訓練、預設保留 30 天；Incognito 裡仍讀得到個人資料設定（custom styles、personal preferences）；只在專案外、右上角幽靈圖示；畫面黑框、左上角「Incognito chat」標籤｜https://support.claude.com/en/articles/12260368-use-incognito-chats（“retained for either 30 days (default)”；“Can Claude access my profile information (custom styles, personal preferences, etc.) in incognito chats? Yes”；“black border and “Incognito chat” label in the upper left corner”）｜2026-10-29｜ch2-temp-compare, ch2-rule, ch3-claude-single, ch4-marks, ch5-term2
c22｜Claude：刪掉的對話立刻從歷史移除、30 天內從後端刪除｜https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data（July 1, 2026；“Deleted from our back-end storage systems within 30 days”）｜2026-10-29｜ch2-compare, ch2-table, ch5-term2, ch5-who
c23｜Claude：允許改良時，去識別化資料最多保留 5 年（只套用在開啟後的新對話或續聊的對話）｜同上（“we may retain your data in a de-identified format for up to 5 years … only applies to new or resumed chats after the model training setting has been enabled”）｜2026-10-29｜ch5-term2
c24｜Claude：被自動安全系統標記違反 Usage Policy：輸入輸出最多 2 年、信任與安全分類分數最多 7 年｜同上（“We retain inputs and outputs for up to 2 years and trust and safety classification scores for up to 7 years if your chat or session is flagged”）｜2026-10-29｜ch5-term2, ch5-who, ch5-big7
c25｜Claude：按讚／倒讚會把整段相關對話（含 custom styles、偏好）存在後端最多 5 年；使用前與使用者 ID 去連結，不與其他對話合併｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training（“we will store the entire related conversation, including any content, custom styles or conversation preferences, in our secured back-end for up to 5 years”；“We de-link your feedback from your user ID … We do not combine your feedback with your other conversations”）；保留頁 “we retain data associated with that submission for 5 years”｜2026-10-29｜ch5-term2, ch5-who, ch5-deleted-q, ch5-feedback-quote
c26｜Claude：沒刪的一般對話沒有固定保留天數（as long as reasonably necessary）｜https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data（“Anthropic retains your personal data for as long as reasonably necessary”）｜2026-10-29｜ch5-term2
c27｜Claude：刪除對話時，由它產生的記憶不會被刪；要在 Settings → Your Claude、Your memory 旁的「Manage」刪掉那一條｜https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context（“When a conversation is deleted … memory entries generated from it aren't removed, but you can delete individual memories while memory is on.”；“selecting "Manage" next to Your memory”）｜2026-10-29｜ch4-delete
c28｜Claude：搜尋過去對話是付費方案功能，推出後預設開啟，開關是 Your Claude 的「Search and reference chats」；搜尋時在對話中以工具呼叫出現｜同上（“Once the ability to search past chats is rolled out to your account, it will be enabled by default.”；“These searches … will appear as tool calls”）｜2026-10-29｜ch1-defaults, ch3-claude-single, ch4-marks
c29｜Claude：Incognito 不會使用既有的記憶｜https://support.claude.com/en/articles/12260368-use-incognito-chats（“Starting an incognito chat won't use Claude's existing memory.”）｜2026-10-29｜（查核第 1 輪起不再用於 ch4-expect：Incognito 能不能搜尋過去的對話，官方頁沒寫；付費方案搜尋預設開著，金絲雀在一般對話裡搜得到，所以「應該答不出」對 Incognito 沒有根據。ch4-expect 改用 c20 的單次關記憶對話，官方頁明寫它不用記憶、也不搜尋過去的對話）
c30｜ChatGPT：記憶在 Settings > Personalization 管理｜https://learn.chatgpt.com/docs/customization/memories.md（“Manage ChatGPT memory from **Settings > Personalization**.”）｜2026-10-29｜ch2-table, ch3-chatgpt-steps
c31｜ChatGPT：說明中心 2026-10-29 無法讀取，所以片中沒有 ChatGPT 的訓練開關名稱、臨時對話天數與人工審查（卡片標明，旁白只說「我沒查到」）｜https://help.openai.com/en/articles/7730893-data-controls-faq（頻道 UA 回 403，`recheck/oai-datacontrols.html`）｜2026-10-29｜ch2-table, ch3-chatgpt-steps
r1｜實算：`node _tools/lifespan.mjs`（Node v22.22.0，2026-10-29）的 10 行輸出；兩張 `terminal` 卡逐字取自 runlog 第 1–5 行與第 6–10 行（欄寬 71，沒有修剪）；「2029 年 10 月」「明年一月底」「十一月一日」「十一月二十八日」「二〇二八、二〇三一、二〇三三年」都是這次執行的結果｜`<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/runlog.txt` run 1｜2026-10-29｜ch5-term1, ch5-reviewed, ch5-term2, ch5-who
s1｜站主觀點（企劃提案，站主 2026-10-29 選選項 A 時採用）：三個開關分開按；訓練關、記憶留著每月看一次；有個資的對話不按回饋；別人的個資不貼，臨時模式也一樣；頻道用 Claude 做影片，Claude 照樣查、照樣關｜brief.md〈站主觀點〉｜2026-10-29｜ch1-disclose, ch3-my-way, ch5-my-feedback, ch6-actions, closing
s2｜不確定（旁白說「我查不到」）：Gemini 審查過的對話「最多三年」從哪天起算，頁面沒寫；ChatGPT 現在的保留天數沒有查到｜brief.md〈站主觀點〉最後一句；Privacy Hub 無起算日｜2026-10-29｜ch2-table, ch5-unknown
e1｜金絲雀測試的預期結果（見示範紀錄 D3，未實測；Claude 那一側用單次關記憶的對話，不用 Incognito）｜c4、c11、c19、c20、c21 的頁面｜2026-10-29｜ch4-canary-chat, ch4-expect

## 與企劃不同的地方

- 開場沒有 `title` 卡：第一張就是隱私權專區的 `screencast`（「刪除活動記錄並不會刪除…最多會保留 3 年」），縮圖的 `capture` 也用它。
- 開場第三句企劃寫「還會被記住」；Gemini 關掉保留活動記錄時記憶也跟著停，所以改成「還可能被記住」。
- 第 4 章（怎麼知道做對了）的 `chat` 卡只放觀眾要打的字，不放 AI 的回答：沒有人跑過（站主不錄帳號），預期結果放在 `compare` 卡，來源標「依官方說明的預期結果」。企劃的「`chat`×3 含回覆」沒照做。
- ChatGPT：help.openai.com 撰稿當天試一次仍是 403，照站主指示降級，只給 Settings > Personalization；卡片寫「說明中心 2026-10-29 無法讀取」，旁白只有一句「我沒查到，先別拿另外兩家的數字去套」。
- 第 5 章：runlog 有 10 行輸出，`terminal` 一張最多 8 行，所以拆成兩張「節錄第 1–5 行」「同一次執行：第 6–10 行」（整行、照順序、沒改字）；企劃的兩張分家 `table` 換成一張「誰決定、你管得到嗎」的表，另加「審查過的：最晚 2029 年 10 月」與「三年從哪一天算起，我查不到」兩張 `big`。
- 多加的內容（都在今天的官方頁上）：第 1 章「什麼都不做時大多開著」的預設值表；第 2 章「選法」表（企劃是一句話）；第 3 章 Claude 的「以前聊過的那些呢？」、記憶的獨立步驟卡、「這一次不進記憶／不留歷史／不翻舊對話」表（含 Search and reference chats）；第 4 章「翻舊對話會出現工具呼叫」；第 5 章 Gemini 審查過的回饋最多三年。
- 企劃第 1 章 Gemini 的 “Even if your Keep Activity setting is off…” 是 `quote`（引繁中官方版同段），不是截圖；Claude〈Use incognito chats〉與 learn.chatgpt.com〈Memories〉沒有做截圖，改用卡片。Claude 的截圖是〈model improvement settings〉的桌機四步。
- 企劃第 3 章的疑問「關了記憶，它會不會變笨？」拿掉（官方頁沒有能回答它的句子）；換成「為什麼 Gemini 的記憶會跟著停？」與「那以前聊過的那些呢？」。
- 章節 7 → 9：第 1 章在「誰讀得到你的 AI 對話？」、第 5 章在「刪掉的對話、按過的讚，還留著什麼？」各切一刀（原本各超過兩分鐘）。
- 說明欄沒有放 `lifespan.mjs` 全文：檔內的 `=>` 含角括號，說明欄不收；改寫成一句它做什麼（加期限到起算日，UTC）。

## 我懷疑但沒動的事

- ch5-deleted-q「按過回饋的那一段，另外存了一份」是從 “store the entire related conversation … in our secured back-end for up to 5 years” 與 “We do not combine your feedback with your other conversations” 推的；頁面沒有直接寫「刪掉原本的對話，回饋那份還在」。查核請判斷這句要不要收成「另外存最多五年」。
- ch2-table「Claude 被標記才看」：保護頁的例外是「送回饋」或「為執行 Usage Policy 需要審查」，「自動安全系統標記」出自保留頁；表格那一格沒寫回饋（第 1 章旁白講過）。
- ch4-expect「Incognito 裡應該答不出來」：頁面寫 Incognito 不用既有記憶；Incognito 裡能不能搜尋過去的對話，頁面沒寫。用了「應該」，沒有更強的說法。
- Gemini 的中文選單字樣（設定與說明、活動記錄、關閉並刪除活動記錄、個人化智慧服務、個人化記憶、臨時對話）取自 zh-Hant 說明頁；活動記錄頁自己標「可能含有使用 AI 技術翻譯的內容」，介面實際字樣可能略有不同。英文頁是 Settings & help、Activity、Turn off and delete activity、Personal Intelligence、Memory、Temporary chat。
- 站主觀點「訓練關掉、記憶留著」在 Gemini 做不到（兩件綁在一起）；稿子寫成「在 Gemini 只能二選一」，沒有替站主決定他在 Gemini 選哪一邊。站主要講自己的選擇，請補一句。
- `lifespan.mjs` 把 Gemini「自動刪除 3 個月」算成今天加三個月；實際是「刪除保存超過 3 個月的活動」，刪除流程還要時間，所以「明年一月底」是最早可能被刪的日子，不是保證的日子。旁白說「是明年一月底」，沒加但書。
- Claude「開著改良最多五年」只套用在開啟後的新對話或續聊的對話；旁白沒講這個但書。
- 第 4 章 Claude「劃掉的記憶圖示」在手機版是鎖住的開關，不是圖示；卡片只講網頁版的說法。

## 進度

- [x] 骨架（schema 通過）
- [x] 全部 45 個場景、140 句旁白（open-hub … closing）
- [x] loops 12 組（3 組埋在開場）
- [x] 發音字典新增 17 個詞（全部 `null`，待試聽）
- [x] 官方頁 2026-10-29 重抓、逐字核對；help.openai.com 403
- [x] `lint`：0 errors、0 warnings，估計 12.3 分鐘
- [x] 撰稿自查：密集卡片 67 個狀態用 `render/repeat.mjs` 畫兩次（兩次相同、沒有溢出；兩張英文引文改短以免下伸字母被切），4 個 `screencast` 在 scratch 工作區對真頁面跑過一次
- [x] 查核第 1 輪（另一個代理，verify-1.md，2026-10-29）：3 處事實改動（ch2-table/yvka 補回饋例外；ch4-expect/3nbs 由 Incognito 改單次關記憶；說明欄「新的對話」）
