# 查核第一輪：ai-term-token

查核 2026-09-30（verifier: claude-fable-5-1，獨立於撰稿者；第一輪）。方法照 `.agents/skills/youtube-video/references/prompts/verifier-video.md`：先把 `video.json` 的每句旁白、每張卡的資料、縮圖、標題、說明欄、標籤、來源抽成 236 個字串（`SCRATCH/ai-term-token/verify/claims-extracted.txt`），再逐條對官方頁與示範輸出；`claims.md` 只當撰稿者的線索，不當證據。

- 示範重跑：`SCRATCH/ai-term-token/verify/demo_token_rerun.py`（`demo_token.py` 逐字複本）於 2026-09-30 重跑，輸出除 `date` 外與 `SCRATCH/demo/demo-token.json` 逐位相同；本機 `tiktoken.__version__` 0.14.0。
- 官方頁今天重抓（`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同主機間隔 1 秒，0 次網路搜尋）：Google tokens 頁 200（頁尾 Last updated 2026-09-23 UTC）、Hugging Face tokenizer_summary 200（main 版）、PyPI JSON 端點 200（`info.version` 0.14.0；0.14.0 檔案 2026-08-17T19:48 上傳）、PyPI HTML 頁 200 但內容仍是「Client Challenge」驗證頁、站內文章 ai-term-token 200、ai-terms-index 200、ai-context-window-explained 200。
- 改動只在 `video.json` 與 `claims.md`；沒有 `say` 欄位，所以沒有 `say_for` 要改；brief.md、demo-log.md、shorts.json、lexicon.json 沒動；沒碰 git。

## 主張表

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 「週六臺北見，帶雨傘」9 個字：o200k_base 10、cl100k_base 16 | hook/tk3zo、hook.data.subtitle、nine-vs.data.text、count-table.rows[0]、thumbnail.sub、youtube.title／description、tkpa6、tk8gm、tkvk1 | demo-token.json `sentence`（重跑相同） | — | CONFIRMED | — |
| 2 | 「傘」在其中一種編碼被拆成兩個位元組片段 | byte-umbrella/tk0is | demo `sentence.o200k_base.pieces`：…雨、`<e582>`、`<98>` | — | CONFIRMED | — |
| 3 | 另一種編碼連週、六、臺都拆開，所以是十六個 | torn-slips/tkvdx | demo `sentence.cl100k_base.pieces`：週六臺帶雨各 2 片、傘 3 片、北見逗號各 1 ＝ 16 | — | CONFIRMED | — |
| 4 | 拆開的片段會再拼回來，數的時候一片算一片 | rejoin/tkfmu | 自算 `decode(encode(句子)) == 句子` 兩種編碼皆 true | — | CONFIRMED | —（拼回的是分詞器的 decode，旁白說「模型」是通俗說法；見懷疑 2） |
| 5 | 模型以 token 為單位處理輸入與輸出；AI 數的不是字 | cutter/tk31b、in-out/tk7rj、wrap/tkmad、youtube.title | https://ai.google.dev/gemini-api/docs/tokens 「process input and output at a granularity called a token」 | 200 | CONFIRMED | — |
| 6 | 用量紀錄寫的是 token，不是字數 | receipt/tklcz、tklg8 | 同上「Use the usage on the interaction response. Returns token counts…」 | 200 | CONFIRMED | — |
| 7 | 一個 token 可能是半個字、一個字或一個詞，大小不固定 | pieces/tkl8w、tkeyu | Google「Tokens can be single characters like z or whole words like cat. Long words are broken up into several tokens.」；文章「中文字的一部分」；demo 位元組片段 | 200 | CONFIRMED | — |
| 8 | 常用的詞整塊、少見的字拆片；郵局分揀；中文也一樣 | word-block/tkezc、sorting/tkevx、chinese-pieces/tkyyy | https://huggingface.co/docs/transformers/main/tokenizer_summary 「Common words stay intact as single tokens, and rare or unknown words decompose into subwords.」 | 200 | CONFIRMED | — |
| 9 | Hugging Face 原句、譯文與出處標示 | hf-quote.data.quote／translation／source、tkacn、tk6cf | 同上，逐字相符；頁面標題「Tokenization algorithms」，Transformers documentation，main 版 | 200 | CONFIRMED | — |
| 10 | 全部片段的集合叫詞彙表；每個模型各有一本 | ch3-card/tkvqv、tklei、drawers/tkxq1 | Google「The set of all tokens used by the model is called the vocabulary, and the process of splitting text into tokens is called tokenization.」 | 200 | CONFIRMED | — |
| 11 | 詞彙表是做模型時定下來的，所以每種編碼切法不同 | vocab-made/tkxs6 | HF「BPE continues learning merge rules until it reaches the target vocabulary size」；demo 兩種編碼結果不同 | 200 | CONFIRMED | — |
| 12 | 文字 → 分詞器 → 片段與編號 → 模型；完整請求含規則與歷史；模型看到的是號碼 | how-diagram.data.caption、tk3ru、lockers/tk4c9 | apps/web/public/guides/ai-term-token/diagram-1.svg（節點：文字／分詞器／token 序列 片段與編號／完整請求也可能含規則、歷史與工具）；文章圖說 | 200（站頁） | CONFIRMED | —（「→ 模型」來自圖的 desc 與文章圖說，SVG 沒畫模型方框；見懷疑 5） |
| 13 | 四步：查詞彙表／少見的字拆到位元組／轉成編號／交給模型 | four-steps.data.steps、tktqf、tkcsk、tkrz0、tkccr | HF「Byte-level BPE uses 256 byte values as the base vocabulary instead, ensuring every word can be tokenized」＋ Google 定義 | 200 | CONFIRMED | — |
| 14 | Google 對自家模型的估法：一個 token 約 4 字元 | google-estimate.data.stats[0]、tkhqe | Google「For Gemini models, a token is equivalent to about 4 characters.」——原句沒限定語言 | 200 | CHANGED | tkhqe「一個 token，大約四個英文字元。」→「一個 token，大約四個字元。」；stats[0].note「英文」→「Google 自家模型」 |
| 15 | 一百個 token 約 60–80 個英文字 | google-estimate.data.stats[1]、tk48k | Google「100 tokens is equal to about 60-80 English words.」 | 200 | CONFIRMED | — |
| 16 | 那是英文的估法，中文、程式碼、表情符號不能直接套 | google-estimate.data.title／stats[2]、tkx87 | 文章「不要把英文估算比例直接套在中文、程式碼、表情符號或混合語言訊息上」；demo 同文換編碼 142 → 200 | 200 | CONFIRMED | — |
| 17 | 要知道數量就用該服務自己的計數功能 | count-tool/tkmzh、compare-card.right | Google「Call count_tokens with the input of the request」；文章 | 200 | CONFIRMED | — |
| 18 | 完整公告 172 字元：142／200 | count-table.rows[1]、request.data.messages[0]、tk09v | demo `full`：chars 172（不含空白 149）、142、200 | — | CONFIRMED | — |
| 19 | 同一份公告換一種編碼多了四成 | forty-percent/tk8lj | 200 ÷ 142 ＝ 1.408 | — | CONFIRMED | — |
| 20 | 精簡版 107 字元：86／115 | count-table.rows[2]、tkp01 | demo `trim` | — | CONFIRMED | — |
| 21 | 精簡版刪掉的是什麼 | tkp01、youtube.description、tkhe4 | demo-log 兩段輸入文字比對：刪了三行客套話（含裝飾）、【】（）、並把「集合地點」「攜帶物品」縮成「集合」「攜帶」；只刪三行客套話而留【】（）與原標籤的版本自算是 93／124（請求 111／155） | — | CHANGED | tkp01「精簡版，只刪客套話和裝飾，變成八十六個…」→「精簡版，刪掉客套話、裝飾和幾個贅字，變成八十六個…」；說明欄「只刪掉客套話和表情符號之後 104 個」→「只刪掉客套話、裝飾符號和幾個贅字之後 104 個」（tkhe4 原本就寫對） |
| 22 | 那句要求 23 字元：18／31；chat 卡照這句寫 | count-table.rows[3]、request.data.messages[0]、tkplh、tkvdf | demo `instruction` | — | CONFIRMED | — |
| 23 | 完整請求 160／231、精簡請求 104／146；「加起來」 | count-table.rows[4–5]、tk277、tkb31、deco-stats.stats[1]、tkwkz、description | demo `full_request`、`trim_request`；18＋142＝160、18＋86＝104、31＋200＝231、31＋115＝146 | — | CONFIRMED | — |
| 24 | 省 56 個，大約三分之一；「教你省下三分之一」 | deco-stats.stats[2]、tk72m、tkt60、tk6x6、description | 160 − 104 ＝ 56；56 ÷ 160 ＝ 35% | — | CONFIRMED | — |
| 25 | 精簡版仍含下雨取消、報名截止、費用；數字和條件全留 | deco-stats labels、tkhe4、trim-steps.data、failed-trim/tkyko | demo `keeps` 三項皆 true；TRIM 文字含時間、集合、費用 150 元 | — | CONFIRMED | — |
| 26 | 裝飾「！！！🌟🌟🌟～～～💖💖💖」12 字元 → 15 個 token（另一種 20） | deco-stats.stats[0]、tka4x | demo `decorations` | — | CONFIRMED | —（量的是獨立拼出的 12 字元字串；見懷疑 1） |
| 27 | 56 × 100 ＝ 5,600，標明是假設 | hundred-big.data.kicker／text、tk04t | 算式；kicker「如果每封都像剛才那份公告」、旁白「如果每封都像剛才那份」 | — | CONFIRMED | — |
| 28 | 客服每天一百封、每封省三分之一 | support-desk/tkuhg | 假設句（「如果你是客服」），下一句再標「如果每封都像剛才那份」 | — | CONFIRMED | —（見懷疑 4） |
| 29 | 輸入含規則、之前的對話、附件；輸出另算；量整份請求 | bundle/tk7kx、hidden-input/tkjd4、tkd03、measure-all/tki54、helper/tkgtl | Google「System instructions are counted as part of the input tokens」「Usage includes tokens from both turns」「All input to the Gemini API is tokenized, including images, video, and audio」「Tools (functions, code execution, Google Search) are also counted」 | 200 | CONFIRMED | — |
| 30 | 輸入輸出分開算；快取另外算；有的服務分推理、快取、工具；欄位以服務為準 | three-cases.data.items[2]、tkay1、report/tk736、fields/tkw7h | Google usage 欄位 input／output／thinking（total_thought_tokens）／cached／tool use；文章「有些服務另列推理、快取或工具相關用量，欄位定義需依提供者文件判讀」 | 200 | CONFIRMED | — |
| 31 | 用量不等於帳單；別拿字數乘一個常數；換一種編碼常數失效 | bill/tkn8k、constant/tk8kr | 文章「用量也不完全等於帳單」「不能拿字數乘上網路流傳的常數」；demo 142 vs 200 | 200 | CONFIRMED | — |
| 32 | token 數決定塞不塞得下與帳單上的用量 | two-things/tkc58 | Google「The context window defines the combined limit of input and output tokens.」「the cost of a call… is determined in part by the number of input and output tokens」 | 200 | CONFIRMED | — |
| 33 | 上下文視窗是容器多大，token 是刻度 | jar-ruler/tktzo、jar-teaser | Google 同上；文章「容器大小與容量刻度的關係」 | 200 | CONFIRMED | — |
| 34 | 塞得下不代表每一條都被讀懂 | full-jar/tkq56 | 文章「容量充足也不代表內容都會被正確使用」 | 200 | CONFIRMED | — |
| 35 | 存取權杖英文也叫 token，是登入用的憑證，要保密；貼 token 前先看是哪一種 | key/tkn8b、paste-key/tkuk0、three-things/tk9oz、ch6-card | 文章「軟體文件中的 token 也可能指存取權杖，例如用來證明登入身分的 access token…前者可能是需要保密的憑證…看到教學叫你「貼上 token」時，先讀清楚上下文」；brief 站主觀點「那是鑰匙，要保密」 | 200 | CONFIRMED | —（沒超出文章的定義；「要保密」比文章「可能是需要保密」強，見懷疑 3） |
| 36 | 字數 vs 文字 token：字元數／編輯器算／篇幅；分詞器切出／服務計數功能／輸入輸出資源 | compare-card.data、tk0md、tklhg、two-rulers/tkw90 | 文章表格「字數｜人可讀的字元或文字規則｜編輯篇幅」「文字 token｜指定分詞器產生的單位｜輸入與輸出資源」 | 200 | CONFIRMED | — |
| 37 | 叫模型剛好寫一千個 token 不會剛好一千字 | thousand-words/tkwtz | 文章「要求模型輸出一定數量的 token，通常不能保證剛好達到編輯規格」 | 200 | CONFIRMED | — |
| 38 | 平常聊天不用算；三種情況：長文件、重複流程、看用量帳單 | ch5-card/tkzrj、tktak、casual-chat/tkoh6、three-cases | 文章「平常使用 AI，不必每段文字都精算。當你處理長文件、設計重複工作或解讀用量時，再用正確工具測量」 | 200 | CONFIRMED | — |
| 39 | 超限先縮小這一輪需要的資料，不是硬塞 | overflow/tkn7g | 文章「遇到超限訊息時，先縮小本輪需要的資料範圍」 | 200 | CONFIRMED | — |
| 40 | 先做一份核對過的精簡版，之後每次都用；重複流程值得先量那份辦法 | fixed-template/tkbwu、hundred/tk081、attach-once/tk0mq、trim-steps | 文章「保留必要條件、固定比較方法、核對輸出內容」與社團助理的例子 | 200 | CONFIRMED | — |
| 41 | 站主觀點「我的看法是，量對東西比追求短重要」「先保住日期和否定條件，整理完對原文，再談省」 | ask-owner.data.messages、tk544、tk5gl | brief.md §站主觀點逐字 | — | CONFIRMED | —（有標「我的看法是」） |
| 42 | 示範工具 tiktoken 0.14.0、2026-09-30 自行計算、不是產品介面 | deco-stats.data.source、youtube.description、sources[2]、claims.md 前言 | https://pypi.org/pypi/tiktoken/json `info.version` 0.14.0，0.14.0 檔案 2026-08-17 上傳；demo JSON `tiktoken` 0.14.0；本機模組 0.14.0。https://pypi.org/project/tiktoken/ 今天仍回 Client Challenge | 200／200 | CHANGED | sources[2].url https://pypi.org/project/tiktoken/ → https://pypi.org/pypi/tiktoken/json；title 加「JSON 端點」 |
| 43 | 編碼名稱 o200k_base、cl100k_base；旁白不說哪個較新、不說模型名稱 | count-table.data.columns、全部 104 句旁白、全部字卡 | demo 腳本 `get_encoding` 的名稱；旁白掃描：無「新」字、無模型名稱；字卡與說明欄無 Gemini | — | CONFIRMED | — |
| 44 | 公告是編的範例，不含個資 | ch4-card/tk7si | demo-log「公告是編的範例，不含任何人的個資」；FULL 內無姓名、電話 | — | CONFIRMED | — |
| 45 | 公告內容：時間、地點、費用、下雨取消、報名截止；前排驚嘆號星星、後排波浪愛心 | bulletin/tk5lx、stickers/tk5ck | demo-log FULL 十行逐行對 | — | CONFIRMED | — |
| 46 | 回覆是示意的，不冒充產品 | request.data.messages[1].name「示意回覆」、tkwe6 | 自製對話卡 | — | CONFIRMED | — |
| 47 | 說明欄末行總索引網址；片尾「下一個名詞：上下文視窗（先讀文章）」 | youtube.description、wrap.data.lines、next-article/tkwg2 | https://mokaair.com/zh-TW/life/ai-terms-index ；https://mokaair.com/zh-TW/life/ai-context-window-explained （那一集未上架） | 200／200 | CONFIRMED | — |
| 48 | sources[0] Google、sources[1] Hugging Face，checked_on 2026-09-30 | sources | 今天重抓皆 200 | 200 | CONFIRMED | — |
| 49 | 圖解 diagram-1.svg，Mokaair 自有，© Mokaair | assets[0] | 檔案存在；SVG 內「© Mokaair 製圖 2026」 | — | CONFIRMED | — |
| 50 | 標題「Token 是什麼？AI 算的不是字數，是它自己的單位」、縮圖「九個字，十六個單位」 | youtube.title、thumbnail.data | 同 #1、#5；符合系列標題格式（名詞在前、無集數） | — | CONFIRMED | — |
| 51 | shorts.json 的數字（9 字 ＝ 10 或 16；142 → 200 多四成；省三分之一）與 video.json 一致 | shorts.json（唯讀） | demo 同上 | — | CONFIRMED | —（只報告，沒動） |

## 摘要

- 查了 51 條主張（抽出的字串 236 個）：確認 48、改了 3（#14 c5 估法的語言限定、#21 c7 精簡版刪了什麼、#42 c13 來源網址）、找不到 0、範圍外 0。改動後 `claims.md` 的 c5、c7、c13 與「懷疑但沒動」的 PyPI 一條同步更新。
- 會過期的事實：Google tokens 頁（估法原句、用量欄位、視窗定義）頁尾 Last updated 2026-09-23 UTC；Hugging Face 是 main 版文件，措辭會改；tiktoken 最新版 0.14.0（PyPI 2026-08-17 上傳），換版本或編碼檔同一段文字的數量可能變；站內文章「查證於 2026 年 9 月」；「下一個名詞」上架後要改指影片。
- 意見不符：無。兩句站主觀點逐字同 brief，且有「我的看法是」。另外 brief §站主觀點寫「刪掉客套話和表情符號真的省下三分之一」，示範實際還刪了【】（）與兩個標籤縮短（只刪三行客套話的版本自算是 93／124、請求 111／155）；brief 唯讀，請站主知悉。
- 聽眾檢查：最長句 37 字（tkhqe，改後 35），沒有超過 40；旁白無「本影片」「經查證」「根據官方文件」；拉丁詞 AI、Google、token、Hugging、Face 都在 lexicon.json（Hugging、Face 為 null 照原字唸，第一次連唸「Hugging Face」沒試聽過）；旁白無括號、無網址；每張卡的 reveal 數等於項目數，沒有 reveal 先於介紹它的句子。
- lint（`node tools/video/cli.mjs lint --slug ai-term-token`，改後）：0 errors、1 warning（平均 6.5 秒換一次畫面，撰稿時已有，最終關卡只警告）；估 9.9 分、104 句、2,104 單位。
- 懷疑但沒動：
  1. tka4x「光是那一串驚嘆號、星星、波浪、愛心，十二個字元，就要十五個 token」：量的是獨立拼出的 12 字元字串，不是公告裡的連續一段；公告裡實際 18 個裝飾字元在上下文中佔 17（o200k_base）／25（cl100k_base）個 token，o200k_base 下反而不到一字元一個。數字對得上示範，deco-stats 的 source 也寫明自算，所以沒改；站主可以決定要不要改成在上下文中的數字（要重跑並改 demo-log）。
  2. tkfmu「拆開的片段，模型會再拼回來」：自算 decode 還原成功，但拼回的是分詞器的 decode，不是模型本身；通俗說法，沒改。
  3. tkn8b「那是登入用的憑證，要保密」：文章寫「可能是需要保密的憑證」，「要保密」是 brief 站主觀點的說法，沒標「我的看法」；沒改。
  4. tkuhg「每封省三分之一」是把示範比例套到假設情境，靠「如果你是客服」與下一句「如果每封都像剛才那份」撐；hundred-big 的 kicker 也標了假設；沒改。
  5. how-diagram caption 的「→ 模型」在 SVG 裡不是一個方框（SVG 節點止於「完整請求」），來自圖的 desc 與文章圖說；沒改。
  6. sources[2] 改成 JSON 端點後，如果 `package` 把 sources 印進說明欄，觀眾點到的是 JSON 而不是專案頁；要給觀眾看的話可另列 https://github.com/openai/tiktoken （PyPI JSON 的 project_urls.homepage），今天沒抓那頁，沒加。
  7. c14–c18（存取權杖、字數 vs token、何時該在意、超限、常數）的來源仍是站內文章；RFC 6749 沒加進 `sources`。
- 第二輪：這一輪改了 3 個事實（c5、c7、c13），沒有超過 3，依規則不需要第二輪；但 c5 與 c7 都動到旁白措辭，建議站主過目 tkhqe 與 tkp01 兩句。
