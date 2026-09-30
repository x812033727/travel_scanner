# Claims：ai-term-token

撰稿 2026-09-30（writer: claude-fable-5-1；草稿，交給另一位代理查核）。大綱選項 A（配方 A 先誤解）。格式：`id｜主張（照旁白或字卡的寫法）與證據｜官方網址｜查核日｜scene id`。官方頁的純文字在撰稿 scratchpad 的 `sources/`（2026-09-30 用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 抓）；示範數字全部來自 `demo-log.md`（2026-09-30 自行執行的計算，tiktoken 0.14.0，編碼 o200k_base 與 cl100k_base），不是任何產品介面。

c1｜「週六臺北見，帶雨傘」9 個字：o200k_base 10 個 token（「傘」切成兩個位元組片段 e582、98，其餘一字一個），cl100k_base 16 個（週、六、臺、帶、雨、傘各拆成位元組片段，北、見、逗號各一個）。口播「一種編碼算十個，另一種算十六個」「傘被拆成了兩個位元組片段」「連週、六、臺都被拆開，所以才變成十六個」；字卡「9 個字 ＝ 10 或 16 個 token」與表格第一列｜自行計算（demo-log.md）；工具 https://pypi.org/project/tiktoken/ ｜2026-09-30｜hook, nine-vs, two-machines, same-text, byte-umbrella, torn-slips, rejoin, count-table
c2｜模型以 token 為單位處理輸入與輸出：「Gemini and other generative AI models process input and output at a granularity called a token.」「All input to and output from the Gemini API is tokenized」。口播「它先把文字切成自己的單位，叫 token」「你貼進去的每一句，跟它回你的每一句，都是用這把尺在算」「服務回給你的用量紀錄，寫的也是 token」「AI 數的不是字，是它自己的單位」｜https://ai.google.dev/gemini-api/docs/tokens （200，頁尾 Last updated 2026-09-23 UTC）｜2026-09-30｜cutter, in-out, receipt, wrap
c3｜token 可以是單一字元或整個詞，長詞拆成多個 token；全部 token 的集合叫詞彙表，切分叫 tokenization：「Tokens can be single characters like z or whole words like cat. Long words are broken up into several tokens. The set of all tokens used by the model is called the vocabulary, and the process of splitting text into tokens is called tokenization.」口播「半個字、一個字，或一個詞」「大小不固定」「每個抽屜裝一個片段，這就是詞彙表」「變成一串片段和編號，模型拿到的是這串編號」「每個片段換成一個編號」（編號＝token id，文章圖解的「片段與編號」）｜https://ai.google.dev/gemini-api/docs/tokens ；圖解 apps/web/public/guides/ai-term-token/diagram-1.svg｜2026-09-30｜pieces, word-block, drawers, vocab-made, how-diagram, lockers, four-steps
c4｜子詞分詞：「They split text into units between words and characters… Common words stay intact as single tokens, and rare or unknown words decompose into subwords.」（quote 卡原句與譯文）；拆到位元組：「Byte-level BPE uses 256 byte values as the base vocabulary instead, ensuring every word can be tokenized」；詞彙表由訓練資料學出：「BPE continues learning merge rules until it reaches the target vocabulary size」。口播「常用的詞一整個就是一塊；少見的字反而被切成好幾片」「整包能直接投的先投，剩下的才拆開來分」「少見的字拆開，拆到詞彙表裡有的為止」「詞彙表是做模型的時候定下來的，所以每種編碼，切法都不一樣」「拆開的片段，模型會再拼回來」（demo 的 decode 把位元組片段拼回「傘」）。旁白不講 BPE、Unigram、WordPiece 的名字｜https://huggingface.co/docs/transformers/main/tokenizer_summary （200，main 版）｜2026-09-30｜word-block, vocab-made, four-steps, sorting, hf-quote, chinese-pieces, rejoin
c5｜Google 對自家模型的估法：「For Gemini models, a token is equivalent to about 4 characters. 100 tokens is equal to about 60-80 English words.」字卡「≈ 4 字元」標「Google 自家模型」、「60–80 個字」標「英文單字」與「以官網為準」；口播「一個 token，大約四個字元」「大約六十到八十個英文字」（查核第一輪：原句的 4 characters 沒限定語言，「英文」只在 60–80 words 那句，口播與字卡照原句）；口播「Google 對自家模型給過一個估法」不說模型名稱。「但那是英文的估法，中文、程式碼、表情符號，都不能直接套」：原句限定 English words，加上 c6（同一段中文換編碼多四成）與 c10（12 個字元的表情符號要 15 個）｜https://ai.google.dev/gemini-api/docs/tokens ｜2026-09-30｜google-estimate, count-tool
c6｜完整公告 172 字元（不含空白 149）：o200k_base 142、cl100k_base 200；200 ÷ 142 ＝ 1.41，口播「多了四成」；口播「時間、地點、費用、下雨取消、報名截止」是公告的內容｜自行計算（demo-log.md）｜2026-09-30｜bulletin, request, count-table, forty-percent
c7｜精簡版 107 字元（87）：86／115。刪掉的是兩行客套話、裝飾符號（！！！🌟🌟🌟～～～💖💖💖）、【】與（）、「集合地點→集合」「攜帶物品→攜帶」兩個標籤縮短；腳本檢查精簡版仍含「下雨取消」「報名截止」「150 元」為 true。口播「刪掉客套話、裝飾和幾個贅字，變成八十六個」「刪掉的是客套話、裝飾符號和幾個贅字，數字和條件全留著」「該留的一條都沒少」（查核第一輪：table 那句與說明欄原本寫「只刪客套話和裝飾／表情符號」，改成與 demo-log 一致；只刪兩行客套話而留【】（）與標籤的版本自算是 93／124）；「token 少了，卻漏掉下雨取消，這次精簡就是失敗的」與三步（留原文當基準、只刪客套話與裝飾、整理完對原文）照文章「用一份公告做可重複的檢查」一節｜自行計算（demo-log.md）；https://mokaair.com/zh-TW/life/ai-term-token ｜2026-09-30｜count-table, torn, deco-stats, trim-steps, failed-trim, ask-owner
c8｜那句要求「請整理成繁體中文公告，保留所有日期與否定條件。」23 字元：o200k_base 18、cl100k_base 31；chat 卡右邊照這句寫｜自行計算（demo-log.md）｜2026-09-30｜request, count-table
c9｜完整請求（要求＋換行＋完整公告）160／231；精簡請求（要求＋換行＋精簡版）104／146；160 − 104 ＝ 56，56 ÷ 160 ＝ 35%，口播「大約三分之一」；56 × 100 ＝ 5,600，big 卡標「如果每封都像剛才那份公告」，是假設的算式，不是量過一百封｜自行計算（demo-log.md）｜2026-09-30｜tape-cut, count-table, deco-stats, scale, support-desk, hundred-big, hundred
c10｜裝飾「！！！🌟🌟🌟～～～💖💖💖」12 個字元：o200k_base 15、cl100k_base 20；15 > 12，所以口播「有的符號一個就佔好幾個」是算術推論；口播「三組驚嘆號、星星、波浪、愛心」照原文｜自行計算（demo-log.md）｜2026-09-30｜stickers, deco-stats
c11｜輸入不只你打的那句：「System instructions are counted as part of the input tokens」「Usage includes tokens from both turns」（多輪）「Tools (functions, code execution, Google Search) are also counted」「All input to the Gemini API is tokenized, including images, video, and audio」（附件）；用量欄位分輸入、輸出、思考、快取、工具：「token counts for input (total_input_tokens), output (total_output_tokens), thinking (total_thought_tokens), cached content (total_cached_tokens), tool use (total_tool_use_tokens)」。口播「規則、之前的對話、附件，都會一起算進輸入；它回你的字，另外算輸出」「輸入和輸出是分開算的」「快取另外算」「有的服務還分推理、快取、工具」「欄位以服務為準」（「推理」對應這頁的 thinking；別家欄位名不同，所以旁白說看它自己的說明）｜https://ai.google.dev/gemini-api/docs/tokens ｜2026-09-30｜receipt, how-diagram, count-tool, hidden-input, bundle, three-cases, helper, measure-all, report, fields, bill
c12｜上下文視窗是輸入與輸出 token 的合併上限，token 是量它的刻度：「Each Gemini model has a maximum number of tokens it can handle. The context window defines the combined limit of input and output tokens.」；「容器塞得下，不代表每一條都被讀懂」是文章「空間限制與回覆長度為何要一起看」一節（「容量充足也不代表內容都會被正確使用」），本集只點一句，指向下一個名詞；不講任何視窗大小的數字｜https://ai.google.dev/gemini-api/docs/tokens ；https://mokaair.com/zh-TW/life/ai-term-token ｜2026-09-30｜two-things, jar-teaser, three-things, jar-ruler, full-jar
c13｜示範工具 tiktoken 0.14.0 是 PyPI 上的最新版（releases 含 0.14.0，2026-08-17 上傳）；示範 JSON 的 `tiktoken` 欄位也是 0.14.0。HTML 頁對抓取工具回 200 但內容是「Client Challenge」驗證頁（查核第一輪同日重抓仍是驗證頁），版本以 JSON 端點為證，`sources` 已改列 JSON 端點。口播只說「公開的計數工具」；名稱、版本與編碼名稱只在字卡（table 欄名、stats 的 source）｜https://pypi.org/pypi/tiktoken/json （200，info.version 0.14.0，0.14.0 檔案 2026-08-17T19:48 上傳）；https://pypi.org/project/tiktoken/ （200，驗證頁，不列入 sources）｜2026-09-30｜counter, count-table, deco-stats
c14｜存取權杖（access token）與文字 token 同名不同物：前者是證明登入身分或授權的憑證、可能要保密；口播「那是登入用的憑證，要保密」「先看清楚是哪一種，別把鑰匙當成字數」｜站內文章「token 不等於字數，也不是登入憑證」一節 https://mokaair.com/zh-TW/life/ai-term-token （定義性說法，今天沒另抓外部官方頁；見下）｜2026-09-30｜three-things, key, paste-key
c15｜字數與 token 是兩套尺度：字數是人可讀的字元數、管篇幅、用文字編輯器算；token 管輸入與輸出的資源；要求模型輸出固定 token 數不保證剛好達到篇幅（「不同標點、空格和分詞方式都會影響結果」）；compare 卡與 verdict「篇幅看字數，資源看 token」照文章的表｜站內文章同一節與表格；token 的定義依 c2、c3｜2026-09-30｜two-rulers, three-things, compare-card, thousand-words
c16｜平常不必精算；處理長文件、重複的工作、解讀用量時才量；先做一份核對過的精簡版之後重複用（「保留必要條件、固定比較方法、核對輸出內容」）；口播「平常聊天問問題，根本不用算」「三種情況才值得量一次」「先做一份核對過的精簡版，之後每次都用它」｜站內文章末段 https://mokaair.com/zh-TW/life/ai-term-token ｜2026-09-30｜trim-steps, ch5-card, casual-chat, three-cases, helper, attach-once, hundred, fixed-template
c17｜遇到超限訊息，先縮小本輪需要的資料範圍，而不是硬塞；口播「碰到超限的訊息，先縮小這一輪真的需要的資料」｜站內文章「遇到超限訊息時，先縮小本輪需要的資料範圍」｜2026-09-30｜overflow
c18｜網路流傳的字數換算常數不能套：Google 的估法限定自家模型與英文（c5）、同一段中文換編碼多四成（c6）；文章「不能拿字數乘上網路流傳的常數」；口播「換一種編碼就失效了」「別拿字數乘一個常數去猜」｜https://ai.google.dev/gemini-api/docs/tokens ；https://mokaair.com/zh-TW/life/ai-term-token ｜2026-09-30｜constant, bill

## 與企劃不同的地方

- 鉤子第二句改成問句：「十分鐘，教你省下三分之一，但先問一句：AI 數的到底是什麼？」（企劃：「十分鐘，你會知道 AI 到底在數什麼，還有怎麼替自己省下三分之一」）。理由：每章最後一句要是下一章的問題，而 title 卡只能帶一句才不會超過 8 秒；「會得到什麼」仍在 16 秒內說完。
- 加了 5 張章節卡（第 2 到 6 章）。「你以為」那句放在第 2 章的章節卡上（停 600），「其實」在硬切後的第一個 shot；每張章節卡後的第一個 shot 都設 `transition: cut`。
- 配方 A 之外多了幾張卡：`quote`（Hugging Face 原句與譯文）、`stats` 兩張（Google 的估法；省下的三分之一）、第二張 `steps`（觀眾照做的三步）、第二張 `big`（56 × 100）、第二張 `chat`（觀眾問、站主答）。配方的相對順序 title → big → diagram → steps → chat → table → bullets → compare → outro 沒變；`cta` 在示範之後、第 4 章的結尾問題之前。
- 站主觀點用第 6 章的 `chat` 卡三個泡泡帶出（「我的看法是…」那句照 brief），不是一句旁白配插圖。
- `table` 六列：企劃的四列之外，多了「週六臺北見，帶雨傘」一列（呼應開場）和「那句要求」一列（要求本身也算 token）。
- 精簡版刪掉的不只客套話和表情符號：還有【】（）和「集合地點→集合」「攜帶物品→攜帶」兩個標籤縮短。口播說「客套話、裝飾符號和幾個贅字」，不照企劃說「只有客套話和表情符號」。
- 第 3 章多了「詞彙表是做模型的時候定下來的，所以每種編碼切法都不一樣」（回答鉤子為什麼兩種結果）和「拆開的片段模型會再拼回來，只是一片算一片」兩個 shot；Google 估法的 `stats` 多一格「不能套」，把「英文估法中文不能套」放進同一張卡。
- 第 5 章每個條件 2–4 個 shot（多了：先量一次那份辦法、量整份請求、超限先縮資料、做一份核對過的精簡版、推理／快取／工具欄位、用量不等於帳單）。
- 第 4 章的 shot「計數器」旁白說「我們拿公開的計數工具，兩種編碼各算一次」；「示意回覆」寫在 chat 卡的名字欄，旁白另說「回覆是示意的」。
- shot 50 個（企劃 38–45）、卡片 21 張（含 5 張章節卡）：一個狀態 ≤ 8 秒、插圖 ≥ 一半，估計 590 秒的影片至少要 44 個 shot；多出的 5 個是第 3、5 章補的場景。
- 章節秒數（估）：15／88／128／155／115／89（企劃 20／90／120／150／120／90）。第 3、4 章比企劃長，第 5 章短。

## 我懷疑但沒動的事

- lint 剩一個警告：平均 6.5 秒換一次畫面（目標 6）。24–28 單位是自然句長；壓到 6 秒要把 7 個 shot 再切成 14 個短鏡（shot 會到 57 個，接近 montage）。實際合成語速約 300 字／分，真實時間軸會比估計短兩成；最終 QA 對平均只警告，對超過 8 秒才擋。
- c14、c15、c16、c17 的來源是站內文章（Mokaair 自有），不是外部官方頁；存取權杖的定義可以補 OAuth 2.0 的 RFC 6749 §1.4，今天沒抓，查核者可以決定要不要加進 `sources`。
- PyPI 的 HTML 頁抓到的是 Client Challenge；版本以 JSON 端點與示範 JSON 的 `tiktoken.__version__` 為準。查核第一輪（2026-09-30）已把 `sources` 改成 JSON 端點 https://pypi.org/pypi/tiktoken/json 。
- 哪種編碼較新：GitHub 的 tiktoken 說明頁對我們的 UA 回 403，沒讀到；旁白只說「兩種編碼」「第一種編碼」，字卡列名稱。
- 「多了四成」是 200 ÷ 142 ＝ 1.41；「大約三分之一」是 56 ÷ 160 ＝ 35%；「一封省五十六個，一百封五千六百個」把示範比例套到假設情境，big 卡標「如果每封都像剛才那份公告」。
- 「有的服務還分推理、快取、工具」：「推理」對應 Google 頁的 thinking（total_thought_tokens）；別家的欄位名稱與分法不同，旁白已說「看它自己的說明」。
- 字典：`Hugging`、`Face` 在 lexicon.json 都是 null（照原字唸），這集是第一次連著唸「Hugging Face」，沒試聽過；`Google` 唸「估狗」、`token` 唸「投肯」、`AI` 唸「A I」是既有條目。沒有新增任何條目。
- chat 卡「示意回覆」的文字是編的，不是任何模型的輸出；「你」那格寫「＋整份公告，172 字元」是為了在 44 字內表示公告也貼上去了。
- 第 6 章 `chat` 卡三個泡泡沒有名字（三個泡泡的版型限制），「站主」身分靠旁白「我的看法是」；查核者若覺得要標名字，可改回兩個有名字的泡泡並合併後兩句。
- `outro` 的 `lines` 寫「下一個名詞：上下文視窗（先讀文章）」：那一集還沒上架，上架後改指影片。

## 進度

- 已完成：brief.md、spec.json → video.json（71 景、50 個 shot、104 句）、claims.md、demo-log.md、shorts.json。
- lint（2026-09-30）：0 錯誤、1 警告（平均換畫面 6.5 秒）；Estimate 9.9 分、2,102 單位；章節 00:00／00:15／01:43／03:52／06:28／08:23。
- 沒做：tts、keyframes、i18n、verify（另一位代理查核）；lexicon.json 沒動。
