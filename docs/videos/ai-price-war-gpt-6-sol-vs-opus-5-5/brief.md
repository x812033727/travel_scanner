# GPT-6 Sol、Luna 和 Claude Opus 5.5 同一天降價：你的 AI 帳單其實會少多少？

<!-- 百萬點閱批次第 1 支（docs/videos/MILLION-VIEWS.md）。企劃日 2026-09-28；「套用立場」條號依 docs/videos/HANDS-OFF.md §頻道立場的草稿編號。 -->

## 觀眾

用 API 付費、或訂 ChatGPT／Claude 的人，看到「便宜 50%」「成本少 40%」「牌價降 20%」三個數字同一天出現，卻不知道哪一個跟自己的帳單有關。搜尋「GPT-6 Sol price」「Claude Opus 5.5 pricing」「cheapest AI API 2026」「OpenAI price cut」。英文市場是主要對象：這支要勾英文配音，縮圖與標題以英文為主。

## 觀眾看完能做到的事

1. 拿自己每月的三種 token 數（輸入、輸出、快取讀取），套進影片的算式，算出換模型後每月差幾美元；不知道自己的用量，就用影片的三種典型情境對號入座。
2. 下次看到「便宜 X%」的新聞，先問一句「跟什麼比」：促銷價、牌價、還是廠商自己估的成本。

## 站主觀點

套用立場：1、2、6
降價不是換工具的理由，帳要自己算。我的做法是只拿當天官方價目表的數字：OpenAI 的「便宜 50%」比的是 GPT-5.6 的促銷價，Anthropic 的「少 40%」是它自己在預設設定下估的成本，只有「20%」是輸入輸出牌價的降幅；三個數字比的不是同一件事。算完會發現：聊天型的小用量本來就便宜到不值得為了降價換工具，代理型的帳單大頭是輸出 token，而不是新聞裡強調的快取讀取。先看自己是哪一種用量，再談要不要換。

## 示範或實算

第 4 章的 `table` 用 2026-09-28 開啟的官方價目表，算三種每月用量在五個模型上的帳單（美元，短脈絡、標準處理，不含快取寫入）：

| 每月用量 | 情境 A 聊天型：500 萬輸入、100 萬輸出 | 情境 B 代理型：1,200 萬新輸入、4,800 萬快取讀取、400 萬輸出 | 情境 C 批次整理型：2 億輸入、1,000 萬輸出 |
| --- | --- | --- | --- |
| GPT-6 Sol（2／0.20／10） | 20 | 73.6 | 500 |
| GPT-6 Luna（0.10／0.01／0.50） | 1.0 | 3.68 | 25 |
| Claude Opus 5.5（4／0.20／20） | 40 | 137.6 | 1,000 |
| Claude Sonnet 5（2／0.20／10） | 20 | 73.6 | 500 |
| Gemini 3.8 Flash（0.75／0.075／3.75，促銷價至 2026-12-31） | 7.5 | 27.6 | 187.5 |

括號是每百萬 token 的輸入／快取讀取／輸出價。兩個對照組放同章的 `stats`：GPT-5.6 Sol 促銷價（4／20，至少維持到 2026-11-21）在情境 A 是 40 美元，GPT-6 Sol 是 20 美元，剛好一半；Claude Opus 5（5／0.50／25）在情境 B 是 184 美元，Opus 5.5 是 137.6 美元，少 25%，不是 40%，因為 40% 還包含 Anthropic 說的「每個任務用的 token 變少」。情境 B 裡輸出 token 佔 GPT-6 Sol 帳單的 54%（40 ÷ 73.6），快取讀取只佔 13%：代理型工作要省錢，先看輸出價。

## 大綱

### 選項 A：先看自己是哪一種用量（推薦）
一行說明：從觀眾的帳單出發，把三個百分比拆開，再用三種典型用量實算；和 B 的差別是不逐格讀價目表，和 C 的差別是以 API 使用者為主、訂閱只帶一段。
開場鉤子：「OpenAI 說便宜 50%，Anthropic 說便宜 40%，同一天。但這兩個數字比的不是同一件事，而且對你的帳單，可能一毛錢都沒差。」
章節（估計秒數，合計約 555 秒）：
1. 同一天兩張降價單（60 秒）
   - title: 觀眾的問題「你的 AI 帳單會少多少？」，副標「三個百分比，三種比法」
   - stats: GPT-6 Sol 2／10、GPT-6 Luna 0.10／0.50、Claude Opus 5.5 4／20（每百萬 token 美元）
   - quote: OpenAI 原文「reducing API prices for Sol and Luna by 50% compared with their GPT-5.6 promotional pricing」與翻譯
2. 三個百分比各自在比什麼（90 秒）
   - compare: 左「50%：跟 GPT-5.6 促銷價比」「40%：Anthropic 自估的執行成本」，右「20%：輸入輸出牌價」「60%：快取讀取牌價」
   - big: 「牌價降 20%」，kicker「只有這個是價目表上的數字」
   - bullets: 促銷價、牌價、成本估計三個詞的差別
3. 帳單的三種 token（80 秒）
   - steps: 輸入 → 輸出 → 快取讀取，各一句話說明什麼時候會產生
   - bullets: 快取讀取兩家都是 0.20；輸出價才是三家差最多的地方
4. 三種用量實算（170 秒）
   - table: 上面的 5 列 × 3 情境，逐列出現，標出 GPT-6 Luna 那一列
   - stats: 兩個對照組（GPT-5.6 Sol 促銷價 40 對 20；Opus 5 184 對 137.6）
   - big: 「54%」，sub「代理型帳單裡輸出 token 的占比」
   - cta: 說明欄第一行的站內文章
5. 什麼時候該換、什麼時候不用動（110 秒）
   - compare: 左「值得算一次」（每月帳單超過 50 美元、輸出多、已在用 GPT-5.6 Sol 或 Opus 5）；右「不用動」（聊天型小用量、訂閱制、還沒量過自己的 token）
   - chat: 觀眾問「我每月 API 帳單 30 美元，要換嗎？」，回答用情境 A 的數字算給他看
   - bullets: 換模型前要做的兩件事：看自己用量頁的三種 token 數、跑一次自己的測試集
6. 一句話答案（45 秒）
   - outro: 「先算帳，再換模型」；下一步：說明欄第一行的站內文章
實算放第 4 章。結尾的下一步：站內文章〈GPT-6 Sol 與 Luna 推出：API 降價、Codex 可用，ChatGPT 對話裡還沒有〉。

### 選項 B：跟著價目表逐格讀
一行說明：以 OpenAI 價目表為主線，教觀眾讀懂同一個模型的八個價格（短脈絡、長脈絡、快取讀取、快取寫入、批次），再對照 Anthropic 與 Gemini；和 A 的差別是先教讀表、後算帳。
開場鉤子：「價目表上，同一個 GPT-6 Sol 有八個價格。哪一個才是你會付的那個？」
章節（估計秒數，合計約 560 秒）：
1. 一個模型八個價格（70 秒）：title；table 列出 gpt-6-sol 短脈絡與長脈絡各四格
2. 輸入、快取讀取、快取寫入（100 秒）：steps 三種 token 什麼時候產生；bullets Sol 的快取寫入 2.50 比一般輸入 2 貴
3. 批次五折與促銷價（80 秒）：compare 批次與即時；quote GPT-5.6 Sol 促銷價至少到 2026-11-21
4. 同一筆工作算三家（170 秒）：table 五個模型 × 三種情境（同 A 的表）；stats 對照組
5. Anthropic 的三個數字（80 秒）：compare 40%、20%、60%；big「20%」
6. 答案（60 秒）：outro
實算放第 4 章。結尾的下一步：站內文章〈API 價格比較：每百萬 token 各家多少〉。

### 選項 C：訂閱使用者版：API 降價和你的月費無關？
一行說明：以 ChatGPT Plus、Claude Pro 的訂閱者為主要觀眾，講清楚 API 降價不等於月費降價、誰能在 ChatGPT 裡用到新模型、什麼情況下從訂閱換成 API 反而省錢；和 A、B 的差別是觀眾不是開發者。
開場鉤子：「API 便宜一半，ChatGPT Plus 還是 20 美元。那這次降價到底跟你有什麼關係？」
章節（估計秒數，合計約 545 秒）：
1. 降的是 API，不是月費（60 秒）：title；quote OpenAI 公告沒有提到訂閱月費
2. 誰在 ChatGPT 裡用得到 Sol 與 Luna（110 秒）：table 方案 × ChatGPT Work、Codex、Chat（Chat 還沒有；Free 與 Go 在桌面 App 用 Luna）
3. Claude 這邊：付費方案五小時上限提高，但沒寫多少（80 秒）：bullets；quote
4. 訂閱換 API 划不划算（170 秒）：table 情境 A 的五個模型帳單對 20 美元月費；chat 一個每月 5,000 則訊息的使用者算給他看
5. 換之前先知道的三件事（80 秒）：steps 用量頁、模型選單、帳單上限
6. 答案（45 秒）：outro
實算放第 4 章。結尾的下一步：站內文章〈免費版夠不夠用：ChatGPT、Claude、Gemini 付費方案比較（2026）〉。

## 會過期的事實

| 事實 | 撰稿日重查的官方頁 |
| --- | --- |
| GPT-6 Sol 每百萬 token：輸入 2、快取讀取 0.20、快取寫入 2.50、輸出 10（短脈絡）；長脈絡 4／0.40／5／15；批次五折 | https://developers.openai.com/api/docs/pricing |
| GPT-6 Luna：0.10／0.01／0.125／0.50；GPT-6 Astra：10／1／12.50／50 | 同上 |
| GPT-5.6 Sol 促銷價 4／20，「至少維持到 2026 年 11 月 21 日」 | 同上 |
| 「50%」比的是 GPT-5.6 促銷價；快取讀取 90% 折扣；Sol 與 Luna 在 ChatGPT Work 與 Codex 對 Plus、Pro、Business、Enterprise、Edu 開放；Free 與 Go 在桌面 App 用 Luna；「not yet available in Chat」 | https://openai.com/index/introducing-gpt-6-sol-and-luna/ （撰稿日用瀏覽器重查；站內文章 2026-09-26 查核過） |
| Claude Opus 5.5：輸入 4、輸出 20、快取讀取 0.20、快取寫入 5；Sonnet 5：2／10；Haiku 4.5：1／5；Fable 5.1：10／50；批次五折；Fast mode 兩倍價 | https://www.anthropic.com/pricing |
| 「40% less to run than Opus 5」是 Anthropic 在預設設定、一般工作負載下的估計；20% 與 60% 是牌價降幅；Sonnet 5.5 與 Haiku 5.5「未來幾週」 | https://www.anthropic.com/claude-opus-5-5 |
| Claude Opus 5（對照組）：輸入 5、輸出 25、快取讀取 0.50 | https://www.anthropic.com/pricing （撰稿日確認 Opus 5 是否仍列在價目表；下架就用公告降幅反推並註明） |
| Gemini 3.8 Flash：輸入 0.75、輸出 3.75、快取 0.075，「through December 31, 2026」，2027-01-01 起 1.50／7.50／0.15 | https://ai.google.dev/gemini-api/docs/pricing |
| Claude Pro 年繳折合每月 17 美元（一次付 200）、月繳 20；Max 100 美元起 | https://www.anthropic.com/pricing |

## 素材

- 站內文章（`source_guide`）：`ai-news-gpt-6-sol-luna-20260923`；引用：`ai-news-claude-opus-55-20260922`、`ai-api-pricing-comparison-2026`。
- 官方頁：上表的每一個網址。
- 圖片與圖解：不用；全部用 `stats`、`table`、`compare`、`big` 版型。

## 不做的事

- 不判斷哪個模型比較聰明：公告裡的評測都是廠商自己選、自己報的分數，影片只提一句「以官方公告為準」。
- 不談 IPO、募資、股價，不給任何採購或投資建議。
- 不算長脈絡價格、不算快取寫入、不算 Fast mode；各講一句「另有價格」。
- 不猜台灣或任何地區的開放時程。
- 不宣稱本站測過任何模型。

## 英文市場的包裝

- 英文標題（三案，撰稿代理挑一個放進 `i18n/en.json` 的 title）：
  1. OpenAI and Anthropic cut prices on the same day. Here's what your AI bill actually looks like now
  2. GPT-6 Sol vs Claude Opus 5.5: the 3 numbers behind "50% cheaper", worked out
  3. The AI price war is here: what $1 buys you on GPT-6 Sol, Luna and Claude Opus 5.5
- 縮圖（`thumb` 版型，英文為主）：tag「PRICE WAR」、headline「50% off?\n**Read the fine print**」、sub「GPT-6 Sol · Luna · Opus 5.5」；zh-TW 縮圖等本地化縮圖的票做好再分開。
- 英文標籤：GPT-6 Sol, GPT-6 Luna, Claude Opus 5.5, OpenAI pricing, Anthropic pricing, AI API cost, Gemini 3.8 Flash, AI price war。
- 投影片文字盡量用產品名、數字、美元符號，少用整句中文。
- 配音：在 `/admin/videos` 勾 en（ja、ko、zh-CN 可一併勾）。
- 上架時機：新聞在 9 月 22 日，越早越好；標題用「帳單怎麼算」的常青角度，熱度過了還有搜尋量。
