# 查核第二輪（輕量版）：ai-term-token

查核 2026-09-30（verifier: claude-fable-5-1，第二個代理；沒寫過這份稿子，也不是第一輪的查核者）。第一輪只改了 3 個事實，依規則不需要完整第二輪；這一輪只查第一輪之後「加長＋聽眾審稿」動到的部分：`claims.md`「加長新增的句子」列的 25 句與 5 個拆句、兩張新的 `bullets` 卡（why-fewer、decisions）、12 個新 shot 的提示、新增的 c19–c23、聽眾審稿改的 10 處、`sources[2]` 改回專案頁，最後全稿 grep 一次。方法照 `.agents/skills/youtube-video/references/prompts/verifier-video.md`；`claims.md` 只當撰稿者的線索。

- 抽稿：`SCRATCH/ai-term-token/verify2/dump_scenes.py` 把 85 景、132 句、141 個字卡字串、26 個中繼字串抽成 `scenes-dump.txt`；`scan.py` 對 `lengthen/video.before.json` 做差異（新 shot 12 個、新卡 2 張、新句 30 個 ＝ 25 句＋5 個拆句、刪 2 句、改 8 句，與 `claims.md` 兩節逐一相符），並掃模型名稱、價格、新舊、查證用語、括號、網址、句長、字典、reveal。
- 示範重跑：`verify2/demo_token_rerun.py`（`demo_token.py` 逐字複本）2026-09-30 重跑，輸出除 `date` 外與 `SCRATCH/demo/demo-token.json` 逐位相同；`tiktoken.__version__` 0.14.0。另寫 `verify2/tiktoken_checks.py`：用位元組偏移把每個片段對回原字（o200k_base 每字 1 片、傘 2 片；cl100k_base 週六臺帶雨各 2 片、北見逗號各 1 片、傘 3 片）、`decode(encode(句子)) == 句子` 兩種編碼皆 true、傘單獨 2／3 個編號也拼回傘、單一符號的片數（🌟 2／3、💖 2／2、！1／1、～1／1；「！！！」在 o200k_base 合成 1 片）、英文例（cat 1 片、annoyingly 2–3 片）、省下比例 35.0%／36.8%。
- 官方頁：PyPI JSON 端點 200（`info.version` 0.14.0；0.14.0 檔案 2026-08-17T19:48:31Z 上傳），PyPI 專案頁 200 但仍是「Client Challenge」驗證頁（3,038 位元組），站內文章 ai-term-token 200（c19–c23 引的每一句都在頁上）；Google tokens 頁與 Hugging Face 用今天 00:06 抓在 `SCRATCH/sources/` 的純文字（Google 頁尾 Last updated 2026-09-23 UTC；HF main 版）。同主機兩次抓取隔開，0 次網路搜尋。
- 改動只在 `claims.md`（c1、c4、c10、c13 補第二輪證據與現行口播措辭、進度；兩處「133 句」更正為 132，lint 與抽稿都是 132）；`video.json` 沒有事實要改，所以沒動；沒有 `say` 欄位；brief.md、demo-log.md、shorts.json、verify-1.md、lexicon.json 沒動；沒碰 git。

## 主張表

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 常用的詞一整個是一塊，少見的字拆成好幾片，字少不等於片少 | why-fewer/0yfm、why-fewer.data.items[0] | hf-tokenizer-summary.txt「Common words stay intact as single tokens, and rare or unknown words decompose into subwords.」；demo `sentence` 9 字 → 10／16 | 200（今日純文字） | CONFIRMED | — |
| 2 | 表情符號和裝飾符號看起來一個字，佔的位子可能不只一片 | why-fewer/2d6g、items[1] | demo `decorations` 12 字元 → 15／20；第二輪自算 🌟 2／3 片、💖 2／2 片 | — | CONFIRMED | —（「不只一片」的證據是表情符號；！、～ 單獨各 1 片，見懷疑 2） |
| 3 | 換一種編碼切法就不一樣，同一句話片數也不一樣 | why-fewer/3z5qc、items[2] | demo `sentence` 10 對 16，片段序列不同 | — | CONFIRMED | — |
| 4 | 連標點都算：那句話中間的逗號在兩種編碼裡都自己佔一片 | why-fewer/are2、items[3] | demo `sentence.*.pieces` 的「，」（efbc8c）在兩種編碼都是單一片段；文章「常見文字、空白、標點…可能用不同方式表示」 | 200 | CONFIRMED | — |
| 5 | why-fewer 卡標題「字數少，token 為什麼不一定少」 | why-fewer.data.title | 章名的問題；demo 9 字 → 10／16 | — | CONFIRMED | — |
| 6 | token 不是字裡本來就有的邊界，而是每個系統自己選的切法 | chalk-lines/n8599 | 文章「token 並不是藏在字裡的自然邊界，而是特定系統選定的表示方式」（今日 200 頁上有） | 200 | CONFIRMED | —（「切法」是「表示方式」的口語版，文章同段也說分詞器「依自己的詞彙表與規則切出片段」） |
| 7 | 北、見、逗號一查就有（詞彙表裡整個有） | four-steps/bc059ux | demo：北 e58c97、見 e8a68b、，efbc8c 在兩種編碼都是單一片段 | — | CONFIRMED | — |
| 8 | 傘就是這樣被拆開的（拆到詞彙表裡有的為止） | four-steps/crqureq | demo：傘 → e582＋98（o200k_base）、e5＋82＋98（cl100k_base） | — | CONFIRMED | — |
| 9 | 十個片段就是十個號碼，一片一個 | four-steps/rl2ww | demo `sentence.o200k_base` count 10；重跑 10 個編號、10 個都不同 | — | CONFIRMED | —（十個是第一種編碼；另一種是 16 片 16 號，規則一樣成立，見懷疑 3） |
| 10 | 數的時候一個號碼算一個 token | four-steps/smc2i | demo 的 `count` ＝ 編號個數；Google「process input and output at a granularity called a token」 | 200 | CONFIRMED | — |
| 11 | 積木比喻：常用的形狀整塊，少見的拿小顆粒拼 | bricks/o2hs7 | 同 #1 的 HF 原句；「Byte-level BPE uses 256 byte values as the base vocabulary」 | 200 | CONFIRMED | —（c4 的第二個比喻，沒有新事實） |
| 12 | 英文最明顯：常見的單字往往一整個是一片，長的字才會被拆開 | long-bead/p6b8z | google-tokens.txt「Tokens can be single characters like z or whole words like cat. Long words are broken up into several tokens.」；自算 cat 1 片、annoyingly 2–3 片 | 200 | CONFIRMED | —（「最明顯」是措辭，見懷疑 1） |
| 13 | 那種編碼裡傘被拆成三片，北、見和逗號都還是一片 | umbrella-three/pv2ey | demo `sentence.cl100k_base.pieces`；重跑按位元組偏移對回每字：傘 3、北 1、見 1、，1 | — | CONFIRMED | — |
| 14 | 另一種編碼 231 變 146，省的也是三分之一多 | ribbon-rolls/vrgpj、count-table.rows[4–5] | demo `full_request.cl100k_base` 231、`trim_request.cl100k_base` 146；85 ÷ 231 ＝ 36.8% | — | CONFIRMED | — |
| 15 | 量完兩份差不多？計數器沒壞，可能能刪的本來就不多 | even-pins/w0o5、xi5j | 文章「若兩份 token 數差異很小，也不表示計數器壞了，可能刪除的文字本來就不多」 | 200 | CONFIRMED | — |
| 16 | 來回聊一下午，前面每一輪的字可能每次都再送一次 | bubble-train/zg4x | 文章「若應用程式把歷史對話重送，前幾輪產生的文字也可能成為下一輪的輸入」；Google「Usage includes tokens from both turns」 | 200 | CONFIRMED | —（有「可能」） |
| 17 | 要它讀完一整本手冊再寫一頁摘要？ | handbook/dkskl8 | 情境問句，沒有事實主張；場景依文章「處理長文件…再用正確工具測量」 | — | OUT OF SCOPE | — |
| 18 | 先問那本手冊塞不塞得下 | handbook/igvbqc | Google「The context window defines the combined limit of input and output tokens.」；文章「檢查一份文件能否放進上下文」 | 200 | CONFIRMED | — |
| 19 | 答案也要佔位子：別把整個上限全拿來貼文件，要留空間給回覆 | answer-room/jwxded | 文章「要為答案保留餘裕」「不能只看一個最大數字便假設所有空間都能用來貼文件」；Google 合併上限與 input／output token limit 分列 | 200 | CONFIRMED | — |
| 20 | 比較前後兩個月，用同一家服務回傳的欄位對照，不要換尺 | two-ledgers/lk06h8 | 文章「評估工作流程時，應先記錄同一服務回傳的實際欄位，再對照當時方案規則」 | 200 | CONFIRMED | —（「前後兩個月」是情境，文章說「評估工作流程」） |
| 21 | 編輯交稿看字數，付錢的人看 token | two-desks/wypays | 文章表格「字數｜編輯篇幅」「文字 token｜輸入與輸出資源」；Google「the cost of a call… is determined in part by the number of input and output tokens」 | 200 | CONFIRMED | —（見懷疑 4） |
| 22 | 第一個決定花不花錢：用量分開讀，別拿字數乘常數猜 | decisions/41dbma、decisions.data.items[0] | brief §站主觀點「第一，花不花錢：…先把輸入、輸出、快取分開讀…不拿字數乘網路流傳的常數估帳」；事實依 Google 用量欄位與 demo 142 對 200 | — | CONFIRMED | —（有「以我的用法」） |
| 23 | 第二個信不信答案：省了 token 卻漏掉下雨取消就不能信 | decisions/4fitri3、items[1] | brief「第二，信不信答案：…漏掉「下雨取消」，這次精簡就是失敗的」；文章「若 token 數下降但漏掉「下雨取消」，這次精簡就不成功」 | 200 | CONFIRMED | — |
| 24 | 第三個給不給權限：鑰匙也叫 token，別因為同名貼進聊天視窗 | decisions/hrtqbf9、items[2] | brief「第三，給不給權限：存取權杖也叫 token，那是鑰匙，要保密，別因為同名就把它貼進聊天視窗」；文章 access token 一段 | 200 | CONFIRMED | — |
| 25 | decisions 卡標題「以我的用法，它改變三個決定」 | decisions.data.title | brief「token 這個名詞會改變我的三個決定」 | — | CONFIRMED | — |
| 26 | 簡單講：AI 數的是片段，要省就先量整份請求，平常不用算 | takeaways/jtxi0r | Google 定義句；文章 callout「先量完整請求」、末段「不必每段文字都精算」 | 200 | CONFIRMED | — |
| 27 | 五個拆句（afysv、e7png、ikky、ktsuo、mu7he）的文字 | lockers、helper、measure-all、support-desk、key | 與 `claims.md`「聽眾審稿改動」列的後半句逐字相同；沒有數字改變 | — | CONFIRMED | — |
| 28 | tk7g0 拿掉「真的」 | ch4-card/tk7g0 | demo-log「公告是編的範例」；下一句 tk7si「是編的範例」 | — | CONFIRMED | —（改得對：原句自相矛盾） |
| 29 | tk0is「傘」被拆成兩個更小的位元組片段 | byte-umbrella/tk0is | demo o200k_base 傘 → 2 片；「兩個」沒變 | — | CONFIRMED | — |
| 30 | tkfmu 拆開的片段最後會再拼回來，數的時候一片算一片 | rejoin/tkfmu | 自算 `decode(encode(句子)) == 句子` 兩種編碼皆 true；傘單獨的 2／3 個編號 decode 回傘 | — | CONFIRMED | —（拼回的是分詞器的 decode，「最後會」比原本的「模型會」準；見懷疑 6） |
| 31 | tkimq「量的東西不一樣」、tklg8「看的是這個數」已刪 | — | `video.json` 無此兩句；`claims.md` 沒有任何證據依賴它們 | — | CONFIRMED | — |
| 32 | tk4c9、tkgtl、tki54、tkuhg、tkn8b 拆成兩句 | lockers、helper、measure-all、support-desk、key | 前後半合起來與改前逐字相同（scan.py 差異表）；一百封、三分之一、存取權杖等數字與名稱沒動 | — | CONFIRMED | — |
| 33 | sources[2] 改回 https://pypi.org/project/tiktoken/ ；c13 註明版本以 JSON 端點確認 | sources[2]、claims.md c13 | 專案頁今天 200 但仍是 Client Challenge；JSON 端點 200，`info.version` 0.14.0，0.14.0 檔案 2026-08-17T19:48:31Z | 200／200 | CONFIRMED | —（c13 補「第二輪同日重抓仍是驗證頁」） |
| 34 | c19–c23 引的文章句子 | claims.md c19–c23 | 今日抓的文章純文字 `verify2/article.txt`：保留餘裕、不能只看一個最大數字、計數器壞了、前幾輪產生的文字、同一服務回傳的實際欄位、自然邊界，全部在頁上 | 200 | CONFIRMED | — |
| 35 | 12 個新 shot 的提示不畫字、logo、真人、產品畫面 | chalk-lines … takeaways 的 data.prompt | scan.py 對 text／logo／person／screen／UI／品牌字掃描：0 個命中 | — | CONFIRMED | —（風格項，順手確認） |
| 36 | 標題、說明欄、縮圖、shorts.json 在加長後沒變 | youtube、thumbnail、shorts.json | 與 `lengthen/video.before.json` 相同；shorts 的 9 → 10／16、142 → 200、三分之一與 demo 一致 | — | CONFIRMED | —（第一輪已查） |
| 37 | claims.md 記的句數「133 句」 | claims.md「與企劃不同的地方」末條、「進度」 | lint「132 lines」；dump_scenes.py 132 句（104 ＋ 30 − 2） | — | CHANGED | 133 句 → 132 句（兩處；只是 claims.md 的記錄，影片裡沒有這個數字） |

## 摘要

- 查了 37 條（新句 25、拆句 5、兩張新卡的標題與 7 條項目、聽眾審稿 10 處、sources[2]／c13、c19–c23、新 shot 提示、中繼資料、claims.md 的句數）：確認 35、改了 1（只是 claims.md 記錄的句數 133 → 132，影片裡沒有這個數字）、找不到 0、範圍外 1（dkskl8 情境問句）。`video.json` 一個字沒動；`claims.md` 補證據、把 c1、c4 引的口播改成聽眾審稿後的現行措辭、句數改成 132。
- 會過期的事實：tiktoken 最新版 0.14.0（PyPI JSON 今天，2026-08-17 上傳），換版本或編碼檔同一段文字的片數可能變；Google tokens 頁 Last updated 2026-09-23 UTC；Hugging Face 是 main 版；站內文章「查證於 2026 年 9 月」；片尾「下一個名詞」上架後要改指影片。
- 意見不符：無。新增的三個「決定」與 decisions 卡逐條對得上 brief §站主觀點，且有「以我的用法」；brief 寫的仍是「提案，待站主確認」。
- 聽眾檢查（全稿 grep，report only）：模型名稱 0（只有 `sources[0].url` 裡的 gemini 字串）；價格、方案、便宜、排行 0（「費用」是公告內容，「帳單」是讀帳單的動作，「元」全是字元／位元組）；「新」「舊」0，沒有哪種編碼較新的比較；旁白無「本影片」「經查證」「根據官方文件」「官方」「官網」；旁白無括號、無網址（`wrap` 卡的「（文章）」「（先讀文章）」是字卡，第一輪已報）；最長句 31 單位（41dbma），其次 29（0yfm），沒有超過 40；拉丁詞 AI、Google、token、Hugging、Face 都在 `lexicon.json`（Hugging、Face 為 null，第一次連唸沒試聽過）；12 張有 reveal 的卡，reveal 數都等於項目數，four-steps 的四句示範例子沒有 reveal、各跟在自己那一步之後；新 shot 12 個、插圖比例照 `claims.md` 約 59%。
- lint（`node tools/video/cli.mjs lint --slug ai-term-token`，改後）：0 errors、2 warnings（平均 6.7 秒換一次畫面；約 12.4 分，目標 9–11），兩個都是加長輪已知、封包說明過的；估 12.4 分、132 句、2,653 單位。
- 懷疑但沒動：
  1. p6b8z「英文最明顯」：官方頁用英文舉例（cat、annoyingly），示範裡中文常見字是一字一片、沒有整個詞一片的例子，所以「英文最明顯」說得通，但「最」是措辭不是量過的比較；不是數字，沒改。
  2. 2d6g「表情符號和裝飾符號…可能不只一片」：不只一片的證據是表情符號（🌟 2／3 片、💖 2／2 片）；「！」「～」單獨各 1 片，「！！！」在 o200k_base 反而合成 1 片。句子有「可能」且把兩者連著講，沒改；若要更準可只說表情符號。
  3. rl2ww「十個片段，就是十個號碼」：十個是第一種編碼的結果，旁白沒說是哪一種；「一片一個」兩種編碼都成立。
  4. wypays「付錢的人，看的就是 token」：Google 說費用「部分」由輸入輸出 token 決定，tkn8k 也說用量不等於帳單；情境句，沒改。
  5. mu7he「那是登入用的憑證，要保密」：文章寫「可能是需要保密的憑證」，「要保密」是 brief 站主觀點的說法（第一輪懷疑 3）；沒改。
  6. tkfmu「最後會再拼回來」：自算還原成功，但拼回的是分詞器 decode 的往返，模型回覆是另外生成再解碼；口語簡化，比原本「模型會再拼回來」準，沒改。
  7. 第一輪懷疑 1（tka4x 量的是獨立拼出的 12 字元）、5（how-diagram 的「→ 模型」）、7（c14–c18 只靠站內文章）仍在，這一輪沒動。
- 第三輪：這一輪影片事實改了 0 個（只有 claims.md 的句數記錄 1 處），不需要。
