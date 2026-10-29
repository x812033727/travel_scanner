# 你跟 AI 說的話，誰看得到？關掉訓練，還有兩個開關開著

企劃日期 2026-10-29。工具教學，**教學卡片**（`format: "slides"`、`category: "tutorial"`、`theme: "paper"`；teaching-flow §一–§九、§十二），
目標 10–12 分鐘（啟動訊息指定；8 分鐘是下限）。字卡主語言 zh-TW，產品名、設定名稱、選單字樣照各家官方頁的寫法（中文介面有官方中文名稱的用中文，
其餘保留英文）。站上沒有對應文章，沒有 `source_guide`。

一句話：「拿去訓練」「記住你」「有人審查」是三個不同的開關，關掉其中一個，另外兩個不會跟著關；每家把開關接在不同的地方。
跟前幾支的分界：`artex-ai-attack-leftover-keys`、`frontend-keys-ai-reverse-engineering` 講金鑰，`muse-allow-always-agent-permission` 講代理的權限按鈕；
這支講**你自己打進聊天框的字**，不碰金鑰、不碰代理權限。旁白最多一句回指前面那幾支。

事實來源（2026-10-29 用頻道 UA 開過，HTTP 200，原始 HTML 與抽出的文字存在 `<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/_tools/sources/`）：
Google〈Gemini Apps Privacy Hub〉（頁面 Last updated: October 26, 2026；英文與繁中版）、〈Manage & delete your Gemini Apps activity〉（英、繁中）、
〈Get personalization with memory of your past Gemini chats〉（英、繁中）、〈Start a temporary chat〉所在的 Gemini 使用說明（英、繁中）；
Anthropic Privacy Center〈Is my data used for model training?〉（March 16, 2026）、〈How long do you store my data?〉（July 1, 2026）、
〈How do I change my model improvement privacy settings?〉（August 3, 2026）、〈How does Anthropic protect the personal data of Claude users?〉（March 16, 2026）；
Claude Help Center〈Use incognito chats〉、〈Use Claude's chat search and memory to build on previous context〉；Anthropic〈Consumer Terms of Service〉（Effective Oct 8, 2025）、
〈Updates to Consumer Terms and Privacy Policy〉（Aug 28, 2025）；OpenAI〈Personalize ChatGPT〉與〈Memories〉（learn.chatgpt.com，markdown 版）。

**ChatGPT 的缺口（撰稿前一定要補）**：OpenAI 說明中心（help.openai.com 的 Data Controls FAQ、Temporary Chat FAQ、Memory FAQ、
How your data is used to improve model performance）與 openai.com 的隱私政策，用頻道 UA 抓一律回 **403**（Cloudflare 的機器人檢查頁），
跟 `frontend-keys-ai-reverse-engineering` 那次一樣。所以這份企劃裡 **ChatGPT 那一欄沒有任何天數**，只有 learn.chatgpt.com 證實的一件事：記憶在
**Settings > Personalization** 管理。訓練開關的名稱、Temporary Chat 的保留天數、人工審查的寫法，要由協調者或站主在撰稿當天**用瀏覽器打開**上面那四頁、
把原句與網址記進 `claims.md`；打不開就把 ChatGPT 降成「片中不給天數、只給選單位置」，第 5 章的實算表只放 Gemini 與 Claude。

企劃先驗（**不算執行紀錄**，協調者照「要先實作」再跑一次寫進 `runlog.txt`）：2026-10-29 在本容器用 Node v22.22.0 跑了 `_tools/lifespan.mjs`
（官方頁的期限加到起算日上），輸出與第 5 章那張表相同。

## 觀眾

每天用 ChatGPT、Gemini 或 Claude 的一般人：拿 AI 改履歷、回客戶的信、整理會議紀錄、問家裡的事；有人已經照網路教學「把訓練關掉」，以為從此沒人看得到。
他們搜的是「ChatGPT 隱私 設定」「AI 會不會拿我的對話去訓練」「Gemini 關閉活動記錄」「臨時對話 安全嗎」「Claude 隱私設定」。
他們不知道的是：訓練、記憶、人工審查是三件事，各家的開關接法不一樣（Gemini 把訓練跟記憶接在同一個開關上，Claude 是分開的）；
而「有人可能讀到」這件事，三家都沒有一個開關能完全關掉。

### 先搜（teaching-flow §十一；YouTube 搜尋，2026-10-29，原始結果存在 `_tools/search/q1–q4.json`；訂閱數本機沒抓）

啟動訊息點名的兩支參考片（q1、q2）：

| 題目 | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| ¡¡NO DES ESTA INFORMACIÓN A CHATGPT!! - Experto alerta | The Wild Project | 7:29 | 439,402 | 4 天前 |
| Your Local AI Is Not as Private as You Think | Kai | 26:01 | 481,343 | 7 天前 |

第一支用英文片名搜，唯一的結果是這支西語片；「DON'T GIVE CHATGPT THIS INFORMATION」應該是 YouTube 自動翻譯的片名，**同一支片是推定、未確認**。
第二支片名與頻道都對得上，已確認。兩支都是「不要給 AI 什麼」與「本機 AI 也不私密」的警告型，沒有一支逐家對照設定。

繁中關鍵字「ChatGPT 隱私 設定 訓練」（q3）與「AI 聊天 隱私 記憶 Gemini」（q4），節錄：

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| AI 知道你多少秘密？Claude、ChatGPT、Gemini，3 大 AI 隱私設定一次學會！ | 可波 AI 白話 | 12:43 | 8,746 | 1 個月前 |
| 【Gemini抵港】小心鬼祟私隱陷阱！更有效使用Google Gemini AI 廣東話教學！ | JP電腦教學 | 18:20 | 115,775 | 7 個月前 |
| Gemini設定 教學！…記憶匯入＋個人背景… | 旅攝Henry Lo | 14:10 | 9,078 | 6 個月前 |
| 小白AI攻略，我的數據我做主！一影片看懂 ChatGPT & Gemini 隱私設定差異 | 嘿~科技 | 3:46 | 76 | 4 個月前 |
| How to Stop ChatGPT, Claude & Gemini From Training on Your Data | Tom Nassr | XRAY | 4:58 | 296 | 3 週前 |
| How To Prevent Gemini From Using Your Chat History To Train It's AI Models | Full Speed Mac & PC | 1:07 | 9,970 | 1 年前 |

讀法：繁中有一支同題（可波 AI 白話，三家隱私設定，12:43、8,746 次），英文多是一兩分鐘的「怎麼關訓練」。沒有一支講**關掉一個開關之後還開著什麼**，
也沒有一支把保留期限算成日期。這支不做「三家設定總覽」，切一個概念：三個開關是分開的，收在觀眾自己做得到的三個動作。
標題可借熱門片的字眼（「誰看得到」「一次講清」），不用「偷看」「監視」這類字。

## 觀眾看完能做到的事

- 在自己用的那一家，把訓練、記憶、人工審查三個開關各自找到並設成想要的狀態，說得出關掉訓練之後**還開著的是哪兩個**；
  例外也說得出來：Gemini 關掉「保留活動記錄」，「個人化記憶」與 Google Workspace 這類連結的應用程式會一起停掉。
  怎麼知道做對了：官方頁寫的畫面標記——Gemini 活動記錄頁頂端的開關顯示「關閉」、臨時對話時畫面上方有臨時對話圖示；Claude 的 Incognito 有黑框與「Incognito chat」標籤，
  關掉記憶的單一對話在標題旁有劃掉的記憶圖示（第 2–3 章，`table`、`steps`×3、`screencast`；**引用**：Gemini、Claude 官方頁 2026-10-29；ChatGPT 待撰稿日補，見上）。
- 用一句「金絲雀」驗證記憶有沒有在用：在一般對話裡留一個假的、獨一無二的事實，再到臨時對話／Incognito／關掉記憶的對話裡問它記不記得，
  並用官方給的問句檢查（Gemini 頁：“Did you use any info from past chats?”、“What do you know about me?”；Claude 頁：搜過去的對話時會出現工具呼叫）。
  怎麼知道做對了：臨時模式裡答不出那個假事實，一般對話答得出來（第 4 章，`chat`×3、`compare`；**引用**；**要先實作**見下：站主自己的帳號才能升到「看過」）。
- 算出今天打的一句話，在自己的設定下**最晚可能留到哪一天**，並分出哪幾個期限是自己的開關管得到、哪幾個管不到（審查過、被安全系統標記、按了回饋鍵）
  （第 5 章，`table`×2、`big`；**引用**：官方頁的期限＋實算，`_tools/lifespan.mjs`，**跑過（待第 1 項）**）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，所以這一段是提案，站主選大綱時確認或改寫。語氣接站主確認過的兩句：Muse 那支「規則的範圍是你按出來的」、
前端金鑰那支「我照樣用 AI 寫前端，但哪些字送到瀏覽器是我決定的」；這支不重複那句的字面。）

我的看法是：三個開關要分開按。訓練我關掉；記憶我留著，但每個月自己打開來看一次它記了什麼；人工審查沒有一家能完全關，所以別人的電話地址、
公司還沒公開的東西、我不想三年後還存在某台伺服器上的事，我不貼進任何一個聊天框，臨時模式也一樣。回饋鍵我在有個資的對話裡不按，因為按下去整段對話會留得比我關掉的任何開關都久。
我每天都用 AI，這個頻道的影片也是用 Claude 做的，所以 Claude 那一欄我照樣查、照樣關，不替它說好話。
我查不到的事：Gemini 說審查過的對話「最多保留 3 年」，從哪一天起算頁面沒寫；ChatGPT 現在的保留天數，要等撰稿當天打開它的說明中心才知道。

## 示範或實算

製作路線：教學卡片（`theme: "paper"`，紙底、米白、墨黑、一個紅色強調；沒有 `shot`）。

**一個例子撐全片**：一份假的履歷，觀眾要請 AI 改得更適合投遞。內容全部是編的、一眼看得出是假的：
姓名「林測試」、電話「0900-000-000」、Email「test@example.com」、地址「某市某路 0 號」，外加一句金絲雀：「我最喜歡的顏色是薄荷綠，代號 MINT-42」。
同一段文字依序貼進三家、三種狀態（一般對話／關掉訓練／臨時模式），每一章問同一個問題：這段字會不會被拿去訓練、下週開新對話時 AI 還記不記得我在找工作、
有沒有人可能讀到、最晚留到哪一天。四個問題就是卡片上固定的四列，每章多填幾格。

**不用這個方法**（觀眾今天的做法，產品最接近的內建功能）：照網路教學把「訓練」那個開關關掉（Gemini 的「保留活動記錄」、Claude 的 Help improve 開關、ChatGPT 的資料控管開關），
就以為這段履歷沒人看得到。主例的差別是在**同一段履歷**上，那個做法只管了四列裡的一列：
① Claude 關掉訓練，記憶照樣開著（記憶對 Free、Pro、Max 預設開啟，在另一個設定頁）；
② Gemini 反過來：關掉「保留活動記錄」，「個人化記憶」也用不了（官方頁：「如關閉此設定，就無法使用這項功能」），Workspace 這類連結的應用程式一起停；
③ 三家都留著一條關不掉的：Gemini 即使關閉或用臨時對話，對話仍可能經人工審查用來「保護 Google、使用者和一般大眾」；Claude 被安全系統標記的對話由 Trust & Safety 的指定成員查看；
④ 期限差很多：Gemini 關閉後與臨時對話留 72 小時，Claude 的 Incognito 與刪掉的對話留 30 天；Gemini 審查過的對話刪了活動記錄也不會刪，最多 3 年；
Claude 被標記的對話輸入輸出最多 2 年、分類分數最多 7 年；按了讚／倒讚，Claude 把整段對話存 5 年。
兩邊都**跑不了**（容器不能登入任何一家的帳號，頻道也不登入、不截任何人的帳號畫面），所以兩邊都是**引用**，卡片標明出處與日期。

**觀眾猜不到的結果**（主例自己的，全部來自官方原句）：
- Gemini 的訓練開關跟記憶是**同一個**：想要它記得你，就得同時讓它把對話拿去改良服務（含人工審查）。Claude 剛好相反，兩個開關分開。
- 「最私密」的模式反而留得比較久：Claude 的 Incognito 30 天，比 Gemini 一般對話關掉紀錄後的 72 小時長十倍。
- Claude 的 Incognito 裡，它**仍然讀得到你的個人偏好**（官方 FAQ：custom styles、personal preferences 在 Incognito 裡可以讀）。
- 最長的那個期限不是訓練開關決定的：Gemini 是審查（3 年）、Claude 是安全標記（7 年）與回饋鍵（5 年）。

**實算**（第 5 章；`_tools/lifespan.mjs`，起算 2026-10-29 00:00 UTC；期限出處見〈會過期的事實〉）：

| 產品與狀態 | 期限 | 最晚 |
| --- | --- | --- |
| Gemini：關閉「保留活動記錄」／臨時對話 | 72 小時 | 2026-11-01 |
| Gemini：開著，自動刪除改成 3 個月 | 3 個月 | 2027-01-29 |
| Gemini：開著，預設自動刪除 | 18 個月 | 2028-04-29 |
| Gemini：被審查員讀過（假設當天審查） | 最多 3 年 | 2029-10-29 |
| Claude：刪掉的對話／Incognito | 30 天 | 2026-11-28 |
| Claude：被標記，輸入與輸出 | 最多 2 年 | 2028-10-29 |
| Claude：開著 Help improve（去識別化） | 最多 5 年 | 2031-10-29 |
| Claude：按了讚／倒讚 | 5 年 | 2031-10-29 |
| Claude：被標記，分類分數 | 最多 7 年 | 2033-10-29 |

前四列與後五列分兩張卡（一張卡一家）；Claude 沒刪的一般對話，官方頁沒有寫固定天數（「as long as reasonably necessary」），卡片照寫，不編數字。
ChatGPT 的列在撰稿日從 help.openai.com 補；補不到就不放。

**要先實作**（協調者在選大綱之前照順序做，每一項把指令或動作、完整輸出、日期與工具版本寫進
`<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/runlog.txt`；做不出「預期」的那一項，對應的成果拿掉或維持引用）：

1. **實算（RUN，計算本身）**。`node _tools/lifespan.mjs 2026-10-29`（檔案在工作區，24 行，期限寫死在檔內、每一列一個官方頁的數字），記 `node --version`。
   預期輸出 9 列，日期與上表相同。認法：72 小時落在 2026-11-01、7 年落在 2033-10-29。撰稿日若官方頁的數字變了，改檔、重跑、重記。
2. **ChatGPT 的四頁（CITED，人工開）**。用瀏覽器開 help.openai.com 的 Data Controls FAQ、Temporary Chat FAQ、Memory FAQ、How your data is used to improve model performance，
   記下：訓練開關的確切名稱與位置、Temporary Chat 的保留天數與是否用於訓練、記憶的兩個開關名稱、有沒有人工審查的原句、頁面日期。
   預期能填滿 ChatGPT 那一欄的三列。打不開就照開頭那段降級。**不登入 ChatGPT。**
3. **金絲雀測試（要升到「看過」才需要；SEEN，只有站主能做）**。站主在**自己的**帳號、自己的電腦上錄螢幕（三家各一次）：
   一般對話貼上假履歷 → 開新的一般對話問「我最喜歡的顏色代號是什麼？」→ 預期答 `MINT-42`（記憶開著時）；
   開臨時對話／Incognito 問同一句 → 預期答不出；Gemini 另外問 “Did you use any info from past chats?”。結束後刪掉那段對話與記憶。
   錄影只截對話區，不露帳號名稱、頭像、其他對話標題。**這一項站主不做，第二件成果維持「引用」，卡片標「依官方說明的預期結果」**，旁白不提錄沒錄。
   站主要不要做，是選大綱時的決定（見報告）：它跟頻道「不登入、不截帳號」的規格衝突，只有站主能開這個例外。
4. **畫面截圖（`screencast`，公開官方頁，不登入）**：Gemini Privacy Hub 的 “Even if your Keep Activity setting is off…human reviewers” 一段與 “retained for up to three years” 一段（繁中版同段）；
   〈管理及刪除 Gemini 系列應用程式活動記錄〉的「關閉『保留活動記錄』設定」步驟；〈個人化記憶〉頁的「開啟保留活動記錄。如關閉此設定，就無法使用這項功能」；
   Anthropic〈How long do you store my data?〉的 Usage Policy Violations 一段；〈How do I change my model improvement privacy settings?〉的四個步驟；
   Claude〈Use incognito chats〉的 FAQ（個人偏好那一題）；learn.chatgpt.com〈Memories〉的 “Manage ChatGPT memory from Settings > Personalization”。
   help.openai.com 若 `screencast` 的瀏覽器也被擋，ChatGPT 不截圖，用 `steps` 卡。

沒有更高一級可以列的：第 1 項本身就是一行指令和它的輸出。三家的開關步驟（設定、關掉、刪除）**不是成果**，是「留下來／關掉」那一步，靠官方頁的步驟（`steps`），卡片標「引用」。

示範的位置：第 2 章 `table`（四列×三家，同一段履歷）、第 3 章 `steps`×3、第 4 章 `chat`×3（金絲雀）、第 5 章 `table`×2（實算）＋ `terminal`（`node lifespan.mjs` 的輸出，逐字取自 `runlog.txt`）。

## 大綱

三個選項的共同點：主例都是那份假履歷，章序都照觀眾的問題（我會得到什麼 → 跟我現在的做法差在哪 → 怎麼做 → 怎麼知道做對了 → 怎麼留下來或收回）。
差在主角是哪一個開關、從哪個意外開場、章節沿著什麼排。「我」的句子三個選項都取自：上面提案的立場（「訓練我關掉，記憶我每個月看一次」「有個資的對話我不按回饋鍵」
「這個頻道也是用 Claude 做的」）、執行紀錄（實算那一行）、查不到的事（3 年從哪天起算、ChatGPT 的天數）。
頻道用 Claude 做影片的揭露**整支片只講一次**，放在第一次講到 Claude 的地方。

### 選項 A（推薦）：關掉訓練，還剩兩個——從「我已經關了」走到四列都填滿

角度：故事線「實測型」，主角是那份履歷。從觀眾**現在的做法失靈**開場（關了訓練＝安全），一章填一列。跟 B 差在主角是開關、不是臨時模式；跟 C 差在不照時間軸排。

開場（teaching-flow §一，五句，前 20 秒說出 Gemini、「保留活動記錄」、3 年）：
「你在 Gemini 把『保留活動記錄』關掉，再把紀錄全部刪光；可是其中如果有一段被審查員讀過，它不會跟著刪，還會再留三年。」（結果）／
「你可能會想：我不是已經把訓練關掉了嗎？」（用觀眾的話問）／
「關掉的是訓練；你打進去的字，還會被記住、被人讀到、被留下來，這是另外兩個開關。」（動詞清單：訓練、記住、讀到、留下來）／
「你貼進去的履歷、客戶的信、家裡的事，都走同一條路。」（利害）／
「三個開關、一句驗證、一張保留期限表，十分鐘內把三家一起設好。」（承諾句）

案例與結果：「假履歷貼進三家：關掉訓練只填了四列裡的一列；Gemini 關掉訓練連記憶一起關、Claude 關掉訓練記憶照開；三家都有一條人工審查關不掉；
今天打的字最晚 2026-11-01 到 2033-10-29；證據 引用（Gemini、Claude 官方頁 2026-10-29；ChatGPT 待第 2 項）＋實算 跑過（待第 1 項）。」

旁白先講出來再答的疑問（§三，每次緊接答案）：「我不是關了訓練嗎？」（第 1 章）、「那我都用臨時模式不就好了？」（第 2 章）、
「關了記憶，它會不會變笨？」（第 3 章）、「我怎麼知道它真的沒記住？」（第 4 章）、「刪掉了，總該不在了吧？」（第 5 章）。
對照已在用的（§三）：觀眾現在的做法＝照教學關訓練開關（第 1 章）；選擇規則一句：「不想被拿去訓練，關訓練；不想被記住，關記憶或開臨時模式；不想被任何人讀到，就別貼。」

例子在每章開頭的狀態（§四）與畫面：

0. 開場（50 秒）狀態：履歷還沒貼。`title`（標題）→ `screencast`（Gemini Privacy Hub「審查過的對話…最多保留 3 年」那段，框起來）→ `big`（你可能會想：我不是關了訓練嗎？）→
   `bullets`（承諾：三個開關、一句驗證、一張表，`icon`：gear、chat、clock）。
1. 三個開關是什麼（100 秒）狀態：履歷貼進一般對話。`table`（四列：訓練／記憶／人工審查／保留，三家欄位先空白）→ `big`（`numeral` 3：三個開關，不是一個）→
   `steps`（一句話送出之後：回答你 → 可能被記住 → 可能被拿去改良 → 可能被審查員讀）→ `quote`（Gemini："Even if your Keep Activity setting is off…including with help from human reviewers"＋譯文）→
   `quote`（Claude："By default, Anthropic employees cannot access your conversations unless…"＋譯文；同一句帶出「這個頻道也用 Claude 做影片」的揭露）。
   收尾問題：「那我關掉的那一個，到底關了哪一格？」
2. 我已經關了訓練（110 秒）狀態：三家都關了訓練。`compare`（左「網路教學說的」：關訓練＝沒人看得到／右「實際上還開著的」：記憶、審查、保留）→
   `table`（三家各一欄，只填「關掉訓練之後」：Claude 記憶照開、Gemini 記憶跟著關、ChatGPT 待補）→ `screencast`（Gemini〈個人化記憶〉頁：「如關閉此設定，就無法使用這項功能」）→
   `big`（Gemini：想被記得，就得讓它拿去改良）→ `compare`（臨時對話 vs Incognito：72 小時 vs 30 天；Incognito 仍讀得到個人偏好）。收尾問題：「那三個開關各在哪？」
3. 三家怎麼設（150 秒）狀態：知道要動哪三格。`steps`（Gemini：設定與說明 → 活動記錄 → 開啟 → 關閉／關閉並刪除活動記錄；自動刪除改成 3 個月）→
   `screencast`（Gemini 活動記錄說明頁的步驟）→ `steps`（Claude：Settings → Privacy → Help improve 開關；Settings → Your Claude → Memory from chats：Pause 或 Reset；
   單一對話用「+」選單關 Memory）→ `screencast`（Anthropic〈model improvement settings〉的四步）→ `steps`（ChatGPT：Settings > Personalization 管記憶；資料控管的訓練開關與 Temporary Chat 待第 2 項補）→
   `bullets`（我的設法，三條，`icon`：lock、clock、chat）。收尾問題：「設完了，怎麼知道它真的沒記住？」
4. 怎麼知道做對了（100 秒）狀態：三家都設好。`chat`（一般對話：貼履歷，最後一句是金絲雀 `MINT-42`）→ `chat`（新的一般對話：「我最喜歡的顏色代號是什麼？」→ 預期答得出；卡片標「依官方說明的預期結果」或站主實錄）→
   `chat`（臨時對話／Incognito 問同一句 → 預期答不出）→ `quote`（Gemini："Did you use any info from past chats?"）→ `bullets`（畫面標記：活動記錄頁顯示關閉、臨時對話圖示、Incognito 黑框、劃掉的記憶圖示）→
   `compare`（記憶的兩種刪法：Gemini 刪掉那段對話／Claude Reset memory，無法復原）。收尾問題：「它不記得了，那份履歷就不在了嗎？」
5. 一句話留多久（100 秒）狀態：記憶乾淨了，回頭看伺服器。`terminal`（`node lifespan.mjs 2026-10-29` 的輸出，逐字自 `runlog.txt`）→ `table`（Gemini 四列）→ `table`（Claude 五列）→
   `big`（最長的那個，不是你關得掉的：7 年）→ `quote`（Claude："we will store the entire related conversation…for up to 5 years"，回饋鍵）→ `big`（有個資的對話，不按讚也不按倒讚）。
   收尾問題：「所以現在先做哪三件？」
6. 行動清單＋收尾（50 秒）：`steps`（三件，照先後：關訓練、看一次記憶並刪掉不該在的、自動刪除改短）→ `big`（答案：關一個開關只關一格，三格要各自按；別人的個資不貼）→
   `outro`（留言題：「你用的那一家，記憶是開著還是關著？你上次看它記了什麼是什麼時候？」＋訂閱邀請）。

總長約 660 秒（11 分鐘），旁白約 2,750 字。

### 選項 B：「不留紀錄」的三種模式——Temporary Chat、臨時對話、Incognito 比一比

角度：故事線「疑問型」，主角是**臨時模式這顆按鈕**。觀眾以為臨時模式＝什麼都不留；全片回答「它少了什麼、沒少什麼、什麼時候用它、什麼時候不夠」。
跟 A 差在從一顆按鈕切入、三個開關當成它的拆解；跟 C 差在不排時間軸。風險：ChatGPT 的 Temporary Chat 是三家裡用的人最多的，第 2 項補不到時，B 少掉最重要的一欄。

開場：「同樣叫『不留紀錄』：Gemini 的臨時對話留 72 小時，Claude 的 Incognito 留 30 天。」／「你可能會想：反正都不會被拿去訓練，差幾天有什麼關係？」／
「差在有沒有人讀得到：兩邊的臨時模式，都還保留著安全審查。」／「你貼進去的履歷，在這段時間裡跟一般對話走同一條安全檢查。」／「三種臨時模式、三個開關、一句驗證。」

案例與結果：「假履歷貼進三家的臨時模式：不訓練、不記憶，但 72 小時／30 天內仍在安全審查的範圍；Incognito 仍讀得到個人偏好；證據 引用＋實算 跑過（待第 1 項）。」

0. 開場（45 秒）`title` → `compare`（72 小時 vs 30 天）→ `big`（你可能會想）→ `bullets`（承諾）。
1. 臨時模式關了哪幾格（110 秒）`table`（四列×三家，只填臨時模式）→ `screencast`（Claude〈Use incognito chats〉）→ `quote`（Gemini：臨時對話不用於訓練，但仍保護…含人工審查）→ `big`（關了兩格，留了兩格）。
2. 每次都開臨時模式行不行（110 秒）`bullets`（Gemini 臨時對話不能用 Gem、連結的應用程式、個人化、不能回饋）→ `compare`（Claude：Incognito vs 單一對話關記憶）→ `big`（常駐設定才是主力）。
3. 不想每次開：三家的常駐設定（150 秒）同 A 第 3 章的三張 `steps` 與兩張 `screencast`。
4. 怎麼知道做對了（100 秒）同 A 第 4 章的金絲雀。
5. 留多久與回饋鍵（90 秒）`terminal`＋兩張 `table`＋`big`（回饋鍵）。
6. 收尾（45 秒）。總長約 650 秒。

### 選項 C：一句話的壽命——從送出那一秒到七年後

角度：故事線「實測型」，主角是**履歷裡那一句金絲雀**，章節沿著時間走：0 秒、72 小時、30 天、18 個月、3–7 年；每到一個時間點，看哪一個開關決定它還在不在。
跟 A、B 差在用實算當主幹，開關是沿途碰到的；最貼「誰看得到」的題目，但**最依賴天數**：ChatGPT 那一欄補不到時，C 只剩兩家的時間軸。記憶不在時間軸上（直到你刪），放倒數第二章。

開場：「今天打進 Claude 的一句話，最短 30 天，最長可以留到 2033 年。」／「你可能會想：我把訓練關了啊？」／「決定它活多久的，大多不是那個開關。」／
「你的履歷、你朋友的電話，也在同一條時間軸上。」／「五個時間點、三個開關、一張你自己的表。」

案例與結果：「金絲雀 `MINT-42` 在兩家（ChatGPT 待補）的時間軸：72 小時、30 天、18 個月、3 年、5 年、7 年各由哪個開關或事件決定；證據 實算 跑過（待第 1 項）＋引用。」

0. 開場（50 秒）`title` → `big`（`numeral` 7：年）→ `big`（你可能會想）→ `bullets`（承諾）。
1. 第 0 秒：送出（90 秒）`steps`（回答 → 安全檢查 → 可能記憶 → 可能訓練）→ `quote`（Claude 員工預設看不到，除非…）→ 揭露頻道用 Claude。
2. 第 72 小時（100 秒）`screencast`（Gemini 關閉後仍保留 72 小時）→ `compare`（關閉 vs 臨時對話：一樣 72 小時，差在記憶與 Gem）→ `big`（關訓練＝連記憶一起關）。
3. 第 30 天（90 秒）`quote`（Claude 刪除後 30 天內從後端刪除）→ `compare`（Incognito vs 關記憶的單一對話）。
4. 第 18 個月（80 秒）`steps`（Gemini 自動刪除改 3 個月）→ `table`（三家常駐設定）。
5. 第 3 到 7 年（100 秒）`terminal`（實算）→ `table`×2 → `quote`（回饋鍵 5 年）→ `big`（管不到的那幾格）。
6. 不在時間軸上的：記憶（100 秒）金絲雀 `chat`×3 → `bullets`（畫面標記）。
7. 收尾（45 秒）。總長約 655 秒。

**推薦 A**：開場打在觀眾現在那個做法上（「我已經關了訓練」），四列表從第 1 章一路填到第 5 章，觀眾一直知道自己在哪一格；
ChatGPT 那一欄補不到時，A 只要把第 2、3 章的 ChatGPT 欄改成「只有選單位置」，結構不動。B 押在 ChatGPT 的 Temporary Chat 上，C 押在天數上，兩者都比 A 更怕那個缺口。

## 會過期的事實

- Gemini：關閉「保留活動記錄」（Keep Activity）後，未來的對話仍以帳戶保存最多 72 小時；不用於訓練，除非你送出回饋；仍會用來保護 Google、使用者與大眾，過程可能有人工審查：
  https://support.google.com/gemini/answer/13594961?hl=zh-Hant （英文版 `?hl=en`；Privacy Hub Last updated: October 26, 2026；2026-10-29 開過）
- Gemini：臨時對話保留 72 小時、不用於訓練、不會為改良服務送人工審查，但仍可能為保護目的借助人工審查；臨時對話不能用 Gem、需要「保留活動記錄」的連結應用程式、個人化回覆、回饋：
  同上一頁，及 https://support.google.com/gemini/answer/13275745?hl=en （Start a temporary chat 一節）
- Gemini：審查員審查過的對話與相關資料，刪除活動記錄時不會刪除，與帳戶斷開，最多保留 3 年；送出的回饋最多 3 年：https://support.google.com/gemini/answer/13594961?hl=en
- Gemini：「保留活動記錄」18 歲以上預設開啟；路徑「設定與說明」→「活動記錄」→「開啟」→「關閉」或「關閉並刪除活動記錄」；預設自動刪除 18 個月，可改 3、36 個月或不自動刪除；
  關閉時只有 Device assistance、Gemini Notebook、Messages、Phone、WhatsApp 可用：https://support.google.com/gemini/answer/13278892?hl=zh-Hant （英文版 `?hl=en`）
- Gemini：「個人化記憶」（past chats）需要開啟「保留活動記錄」，關閉就無法使用；路徑「設定與說明」→「個人化智慧服務」→「個人化記憶」；可問 “Did you use any info from past chats?”；
  記憶摘要可用 “What do you know about me?” 查看：https://support.google.com/gemini/answer/16598469?hl=zh-Hant 、Privacy Hub 同上
- Gemini：從其他 AI 平台匯入的記憶與對話存進活動記錄，照活動記錄的方式使用（含訓練）：Privacy Hub 同上（片中不展開，見〈不做的事〉）
- Claude：消費者方案（Free、Pro、Max，含這些帳號用的 Claude Code）在三種情況使用對話改良模型：你允許、對話被標記做安全審查、你另外加入訓練（例如 Trusted Tester）：
  https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training （March 16, 2026）
- Claude：設定路徑 Settings → Privacy → “Help Improve our AI models” 開關（頁面用語；中文介面的字樣撰稿日在頁面繁中版核對）；關掉後新對話不用於之後的訓練，已開始的訓練與已訓練好的模型不受影響；被安全分類器標記的對話仍可能用於內部安全模型：
  https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings （August 3, 2026）
- Claude：刪掉的對話立刻從歷史移除、30 天內從後端刪除；允許改良時去識別化資料最多 5 年；被標記違反 Usage Policy 的輸入輸出最多 2 年、分類分數最多 7 年；回饋 5 年：
  https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data （July 1, 2026）
- Claude：讚／倒讚會儲存整段相關對話最多 5 年，使用前與使用者 ID 去連結：https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
- Claude：員工預設不能存取對話，除非你送回饋，或為執行 Usage Policy 需要審查（只有 Trust & Safety 的指定成員）：https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users
- Claude：Consumer Terms 原句「…including training our models, unless you opt out of training through your account settings. Even if you opt out, we will use Materials for model training when: (1) you provide Feedback…, or (2) your Materials are flagged for safety review…」：
  https://www.anthropic.com/legal/consumer-terms （Effective Oct 8, 2025）；背景：2025-08-28 的更新公告（五年保留、2025-10-08 前要選）：https://www.anthropic.com/news/updates-to-our-consumer-terms
- Claude：Incognito 不存進對話歷史與記憶、不用於訓練、保留 30 天（預設）；Incognito 裡仍讀得到個人資料設定（custom styles、personal preferences）；只能在專案外開；開法是右上角的幽靈圖示：
  https://support.claude.com/en/articles/12260368-use-incognito-chats
- Claude：記憶對 Free、Pro、Max 預設開啟；Settings → Your Claude → “Memory from chats”；關閉時選 Pause memory 或 Reset memory（無法復原）；單一對話在送出第一則訊息前用「+」選單關 “Memory”；
  搜尋過去對話是付費方案功能（“Search and reference chats” 開關）；預設不存健康等敏感主題：https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- ChatGPT：記憶在 Settings > Personalization 管理：https://learn.chatgpt.com/docs/customization/memories.md 、https://learn.chatgpt.com/docs/personalize.md （2026-10-29 開過）
- ChatGPT：訓練開關名稱與位置、Temporary Chat 的保留天數與用途、記憶的開關名稱、人工審查原句——**2026-10-29 用頻道 UA 抓回 403，未確認**，撰稿日用瀏覽器開：
  https://help.openai.com/en/articles/7730893-data-controls-faq 、https://help.openai.com/en/articles/8914046-temporary-chat-faq 、https://help.openai.com/en/articles/8590148-memory-faq 、
  https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance
- 參考片與同題片的觀看數：YouTube 搜尋頁，撰稿當天重抓 `_tools/search/`（2026-10-29 的數字見〈觀眾〉兩張表）

## 素材

- `screencast`（公開官方頁，不登入）：見〈示範或實算〉第 4 項的七段；Gemini 頁面用繁中版（`?hl=zh-Hant`）截，選單字樣跟觀眾看到的一致。help.openai.com 若被擋就不截。
- `terminal`：`node lifespan.mjs 2026-10-29` 的輸出，逐字取自協調者的 `runlog.txt`；檔案在 `<VIDEO_WORKDIR>/ai-chat-privacy-three-switches/_tools/lifespan.mjs`（企劃先驗用）。
- `chat`：假履歷與金絲雀句由撰稿寫；回覆是「依官方說明的預期結果」，除非站主做了第 3 項，那時逐字取自錄影。
- 原始頁面 HTML 與文字：`_tools/sources/`（g-privacyhub、g-activity、g-memory、g-tempchat 各英繁兩版；a-training、a-retention、a-setting、a-protect、a-incognito、a-memory、a-consumer-terms、a-terms-news；
  lc-personalize、lc-memories、lc-settings；oai-* 是 403 的擋頁，留著當證據）。
- YouTube 搜尋結果：`_tools/search/q1–q4.json`（2026-10-29）。
- 縮圖：米白底，大字「還剩兩個開關」（6 字），右側 Gemini Privacy Hub「最多保留 3 年」那段的截圖；不畫眼睛、監視器、駭客。
- 說明欄：三家設定的完整路徑、各官方頁連結、`lifespan.mjs` 全文、揭露一句「本頻道使用 Claude 協助製作影片」。

## 不做的事

- 不登入任何一家的帳號、不截任何人的設定畫面或對話（第 3 項是站主自己決定的例外，不是預設）。
- 不講 API、企業版（ChatGPT Business／Enterprise、Claude Team／Enterprise、Google Workspace 的 Gemini）的資料政策；只講個人帳號。Incognito 在 Team／Enterprise 會進組織匯出，一句帶過或不講。
- 不講本機模型（Ollama 之類）：第二支參考片的題目，例子不同，另做。
- 不講 Gemini 的「匯入其他 AI 平台的記憶與對話」、Gemini Live 的音訊與螢幕分享設定、Computer History、Claude 的 Cowork／Duet 記憶：同一個道理，例子不同。
- 不給法律意見，不評論各家政策合不合法，不講各國法規（GDPR 等）；不講任何訴訟或法院命令，除非撰稿日 ChatGPT 的官方頁自己寫了，那時照原句放卡片。
- 不談健康、財務、法律問題「能不能問 AI」：片中只講「別人的個資與未公開的資料不貼」，不列敏感主題清單。
- 不比較哪一家「最安全」、不推薦換用哪一家；不推薦付費隱私工具或去識別化服務。
- 不重講金鑰、`.env`、代理權限按鈕（前三支講過）；旁白最多一句回指。
