# verify-2：上下文視窗（Context Window）是什麼（輕量第二輪）

- 查核日：2026-09-30。第二輪、輕量版，獨立查核者（Claude；沒寫過這份稿，也不是第一輪的查核者）。第一輪只改了 1 個事實，所以這一輪不重查全稿，只查第一輪之後「加長＋聽眾審稿」動到的部分：加長新增的 26 句與 1 張 `steps` 卡（claims.md「加長新增的句子」）、聽眾審稿改過的 6 句（claims.md「聽眾審稿改動」），外加全稿 grep 一次。
- 先不信 claims.md 的清單：用 `SCRATCH/ai-term-context-window/lengthen/video.before.json`（加長前的稿）和現在的 `video.json` 自己 diff（`verify2/diff_before.py`）：新句 26、新場景 22（21 個 shot 加 `workset-steps`）、改過的既有句 6、沒有刪句、標題／說明欄／標籤／縮圖／sources／assets 都沒動，跟 claims.md 列的完全一樣。
- 依據只用封包指定的本地材料：`SCRATCH/demo/demo-context.json`（在自己的資料夾重跑 `demo_context.py`，Python 3.11.15、tiktoken 0.14.0、`o200k_base`，輸出與撰稿封包逐位元相同）、`demo-log.md`、文章純文字 `SCRATCH/article-ai-context-window-explained.md`（另對照 repo 的 `apps/api/app/guides/content/ai-context-window-explained.json` 與第一輪今天抓的正式站頁 `verify/live-mokaair-article.html`，三處同句）、官方頁純文字 `SCRATCH/sources/*.txt`（arXiv、Anthropic、Google 三頁，第一輪今天重開都是 200，見 `verify/http-results.json`）、brief §站主觀點。這一輪沒有新的網路請求（curl 0 次、搜尋 0 次）。
- 輔助腳本與輸出在 `SCRATCH/ai-term-context-window/verify2/`：`dump.py`（全稿逐句）、`diff_before.py`、`demo_context.py` 重跑、`listen_pass2.py`（聽眾檢查與全稿 grep）、`check_numbers.py`（沿用第一輪的 63 項數字檢查，改後仍全過）、`patch_round2.py`（兩處修改，逐字取代、不重新序列化）、`video.before-r2.json`／`claims.before-r2.md`（改前快照）。

## 主張表

# ｜ 主張 ｜ 位置 ｜ 網址或示範檔 ｜ HTTP ｜ 判定 ｜ 改前 → 改後

### 一、加長新增的句子與 steps 卡

1 ｜ 如果你把一批合約丟給它整理，先問一句：它這一次拿到了哪幾份？ ｜ cw0fm（contracts-to-sort） ｜ 情境句；前提是 c3（文章 §視窗裡放的是當次可用的資料「不一定等於你所有上傳檔案或全部聊天紀錄」）；「一批合約」出自 brief §觀眾 ｜ — ｜ OUT OF SCOPE（情境／建議句，沒有數字與名稱） ｜ —
2 ｜ 哪一種，看你用的工具怎麼做。 ｜ cw0gl（summary-note 第二句） ｜ 文章同節「具體行為由產品實作決定」 ｜ 200（live 頁同句） ｜ CONFIRMED ｜ —
3 ｜ 最長的一份，兩百一十七個字元。 ｜ cw3si（longest-record-lifted） ｜ demo-context.json `records[1].chars` = 217，是 198／217／189 之最 ｜ 重跑相同 ｜ CONFIRMED ｜ —
4 ｜ 算出來一百八十八個 token。 ｜ cwof9（document-on-scale） ｜ `records[1].tokens` = 188（同一份；也是三份裡最多的） ｜ 重跑相同 ｜ CONFIRMED ｜ —
5 ｜ 你自己的文件也能算：視窗大小除以每份的 token 數，就是放得下幾份。 ｜ cw4k9（your-own-stack-ruler） ｜ demo `fits` 的算式 `int(window // (535 / 3))`；brief §觀眾看完能做到的事 3「視窗大小除以每份的 token 數」 ｜ 重跑相同 ｜ CONFIRMED（粗估，見懷疑 1） ｜ —
6 ｜ 他們測的是多份文件一起放進去的問答。 ｜ cw5mv（many-folders-one-marked） ｜ arXiv 2307.03172 摘要「multi-document question answering and key-value retrieval」（sources/lost-in-the-middle.txt） ｜ 200 ｜ CONFIRMED（論文還有第二個任務，旁白沒說「只」，見懷疑 2） ｜ —
7 ｜ 看相關的那一份放在哪裡。 ｜ cwotj（bookmark-in-stack） ｜ 摘要「changing the position of relevant information」 ｜ 200 ｜ CONFIRMED ｜ —
8 ｜ 換成你的長桌，撤回單在最後面還好。 ｜ cw6fn（withdrawal-at-end） ｜ 摘要「performance is often highest when relevant information occurs at the beginning or end of the input context」；「撤回單在最後面」承接 cwa0h 與文章例子「後面才正式撤回」 ｜ 200 ｜ CONFIRMED ｜ —
9 ｜ 要是被夾在中間，它就容易漏看。 ｜ cwprg（withdrawal-in-middle） ｜ 摘要「significantly degrades when models must access relevant information in the middle of long contexts」 ｜ 200 ｜ CONFIRMED ｜ —
10 ｜ 如果你是管委會的幹部，先把每份紀錄貼上標籤。 ｜ cw8rl（tabs-few-minutes） ｜ 情境句；做法是 c12（文章「明確標出提案、決議、撤回與待查證項目」） ｜ — ｜ OUT OF SCOPE（情境／建議句） ｜ —
11 ｜ 比換一個更大的視窗有用。 ｜ cwptq（movers-with-giant-desk） ｜ 文章 §容量上限與有效使用能力分開看「這時只把容量加大，沒有修正版本關係。更有幫助的是明確標出…」 ｜ 200 ｜ CONFIRMED ｜ —
12 ｜ 像是一口氣把一整櫃的報告全丟進去，門太小；最直接的做法，是分批。 ｜ cw9ec（cabinet-into-bundles） ｜ 文章 §超限、摘要漏失與理解錯誤「最直接的處理是縮小本輪工作集，保留相關章節與原文位置，必要時分批抽取」（純文字、repo JSON、live 頁三處同句）；c9 Anthropic「prompt is too long」 ｜ 200 ｜ CHANGED ｜ 「…門太小；最直接的做法，是分批。」→「…門太小；那就分批。」文章的「最直接」是給「縮小本輪工作集」整套的，分批是「必要時」的一種做法；旁白把分批升成「最直接」，跟第一輪拿掉的「最常見」同一類、來源撐不住的最高級。畫面、id、後兩句「分批之後，還要合併檢查」不動；沒有 `say`。
13 ｜ 壞的那句什麼都記得：報價、燈具、旅遊。 ｜ cwaua（summary-three-icons） ｜ demo `summary.text`「三家廠商報價 18 至 22 萬元；中庭燈具已更換完成；年度旅遊 6 月 14 日去宜蘭」三個詞逐字都在 ｜ 重跑相同 ｜ CONFIRMED（「什麼都記得」是反話鋪陳，下一句就翻） ｜ —
14 ｜ 就是沒說維修案還沒核准。 ｜ cwsjq（unused-stamp） ｜ `summary.keeps_not_approved` = false；摘要全文連「核准」兩個字都沒有 ｜ 重跑相同 ｜ CONFIRMED ｜ —
15 ｜ 好的那句留的是狀態：尚未核准、流會延期、不得發包，還有待辦。 ｜ cwchh（handoff-status-strip） ｜ `good_handoff.text`「維修案狀態：尚未核准，區權會流會延期，不得發包；待辦是臨時防水方案報價」；「尚未核准」「流會延期」「不得發包」「待辦」四個詞逐字都在 ｜ 重跑相同 ｜ CONFIRMED ｜ —
16 ｜ steps 卡：標題「把紀錄整理成可查核的工作集」；三步「列欄位，建索引／提案、狀態、負責人、缺什麼、原文位置」「抽成工作表／找不到就留空；保留可回查的位置」「只帶核對過的表／加必要原文，再請它草擬議程」 ｜ workset-steps.data ｜ 文章 §把會議紀錄整理成可查核的工作集 三段：「提案名稱、目前狀態、負責人、尚缺資料與原始段落。再依日期建立索引」「要求找不到就留空，並保留可回查的位置」「只帶入已核對的工作表與必要原文，請模型草擬議程」 ｜ 200 ｜ CONFIRMED ｜ —
17 ｜ 第一步，先列欄位：提案、狀態、負責人、缺什麼、原文在哪；再按日期建索引。 ｜ cwcp2（workset-steps，reveal 1） ｜ 同上第一段 ｜ 200 ｜ CONFIRMED ｜ —
18 ｜ 第二步，請它把每份紀錄抽成工作表；找不到就留空，位置要查得回去。 ｜ cwcxa（workset-steps，reveal 2） ｜ 文章第二段「第二步先請模型針對相關紀錄抽取欄位，要求找不到就留空，並保留可回查的位置」；「每份紀錄」文章沒有，三處都是「相關紀錄」 ｜ 200 ｜ CHANGED ｜ 「請它把每份紀錄抽成工作表」→「請它把相關紀錄抽成工作表」。第一步的索引就是拿來挑相關紀錄的（文章：「避免把所有附件一次丟入」），「每份」跟這一步的意思相反。單位數 28 不變，reveal 不動。
19 ｜ 第三步，只帶核對過的工作表和必要原文，請它草擬議程。 ｜ cwdzl（workset-steps，reveal 3） ｜ 文章第三段 ｜ 200 ｜ CONFIRMED ｜ —
20 ｜ 要的是一張工作表，不是一篇看起來很完整的摘要。 ｜ cwex2（worksheet-vs-summary） ｜ 文章第二段「預期產物是工作表，而不是先寫一篇看似完整的摘要」 ｜ 200 ｜ CONFIRMED ｜ —
21 ｜ 寫錯了，回頭查三件事。 ｜ cwflo（pen-paused-looking-back） ｜ 文章第三段「就回頭檢查工作表是否有錯、原文是否真的在本輪上下文，以及指示是否要求區分狀態」，正好三件 ｜ 200 ｜ CONFIRMED ｜ —
22 ｜ 表對不對、原文在不在、有沒有要它分狀態。 ｜ cwslc（three-things-to-recheck） ｜ 同上 ｜ 200 ｜ CONFIRMED ｜ —
23 ｜ 以我的用法，上下文視窗這個名詞，改變我兩個決定。 ｜ cwk4g（two-decisions-fork） ｜ brief §站主觀點「這個名詞改變的決定有兩個」；已標成意見 ｜ — ｜ CONFIRMED（brief 這節仍標「提案，待站主確認」） ｜ —
24 ｜ 第一，換不換更大的視窗，先分清是哪一種忘記。 ｜ cwka0（bigger-desk-or-not） ｜ brief「要不要為更大的視窗付錢或換工具（先分清楚是沒送進去、摘要漏掉還是看了卻答錯，再說）」；旁白不提付錢，合系列規則 ｜ — ｜ CONFIRMED ｜ —
25 ｜ 第二，信不信一句看起來很完整的摘要：先對原文，再信。 ｜ cwkop（trust-after-checking） ｜ brief「信不信一句看起來很完整的摘要（先對原文再信）」 ｜ — ｜ CONFIRMED ｜ —
26 ｜ 帶走三件事。 ｜ cwmw3（three-takeaways 第一句） ｜ 引導句 ｜ — ｜ OUT OF SCOPE ｜ —
27 ｜ 先看桌上有什麼；摘要對原文；分清是哪一種，再動手。 ｜ cwnro（three-takeaways 第二句） ｜ outro 卡三行「先看這一輪桌上有什麼／摘要一定拿去對原文／分清楚是哪一種忘記，再動手」；brief §站主觀點 ｜ — ｜ CONFIRMED ｜ —

### 二、聽眾審稿改過的 6 句

28 ｜ 「token 是模型自己的單位，不是字數；我拿三份會議紀錄算過一次」→「…；拿三份會議紀錄實際算一次」 ｜ cwr09（ruler-by-desk） ｜ 數字「三份」、名稱 token 都沒動；第一人稱拿掉；「實際算」對得上 demo-log「自行執行的計算」 ｜ 重跑相同 ｜ CONFIRMED ｜ —
29 ｜ 「我把三次會議壓成一句話，六十二個字元，看起來很完整」→「把三次會議壓成一句話試試看：六十二個字元，看起來很完整」 ｜ cwpzq（one-line-summary） ｜ 62 = `summary.chars`；第一人稱拿掉 ｜ 重跑相同 ｜ CONFIRMED ｜ —
30 ｜ 「它要是把維修案寫成即將施工，錯的不是模型，是交接」→「我的看法是，它要是寫成即將施工，錯的不是模型，是交接」 ｜ cw9er（crane-question） ｜ brief §不做的事「寫錯了錯的是交接」與 §站主觀點；仍是條件句、沒說成實測（demo-log：沒把任何文字送進任何模型）；「維修案」由前一句 cwio4「這個案子」承接 ｜ — ｜ CONFIRMED（意見已標） ｜ —
31 ｜ 「你貼的附件、它查到的資料，也都攤在這張桌上」→「你貼的附件，還有它查到的資料，也都攤在這張桌上」 ｜ cwb3u（clipped-attachments） ｜ 只改連接詞；c2（Anthropic「including tool results, images, and documents」，第一輪 #20） ｜ 200 ｜ CONFIRMED ｜ —
32 ｜ 「反正全都在桌上，它自己會翻」→「反正都在桌上，它自己會翻、會找」 ｜ cwftv（pages-turn-themselves） ｜ 「你可能覺得」開頭，沒有主張 ｜ — ｜ OUT OF SCOPE ｜ —
33 ｜ 「沒有超限，全部都放上桌了，模型還是可能搞混哪一版才有效」→「沒有超限，全都上桌了，它還是可能搞混哪一版才有效」 ｜ cw5l9（reader-two-questions） ｜ c12 文章「即使整份資料沒有超限，模型仍可能混淆哪一版有效」 ｜ 200 ｜ CONFIRMED ｜ —

### 三、全稿 grep（127 句旁白、14 張卡、標題、說明欄、標籤、縮圖；`listen_pass2.py`）

34 ｜ 沒有模型或廠商名稱（Claude／Gemini／GPT／Sonnet／Opus／Haiku／Llama／Mistral／OpenAI／Anthropic／Google／Copilot／Grok／DeepSeek／Qwen…） ｜ 全稿 ｜ listen_pass2.py B1–B3 ｜ — ｜ CONFIRMED（0 命中；`sources[]` 的來源標題有 Google／Anthropic，那是來源表，不是旁白或字卡） ｜ —
35 ｜ 沒有價格、方案、付費、訂閱、美元、台幣 ｜ 全稿 ｜ listen_pass2.py C1–C3 ｜ — ｜ CONFIRMED（命中只有「字元」的「元」、「一塊空位」、會議的「舊方案」「臨時防水方案」，以及 code 卡示範資料裡廠商報價「18 至 22 萬元」；沒有任何 AI 的價格或方案） ｜ —
36 ｜ 沒有「哪個編碼比較新」之類的比較 ｜ 全稿 ｜ listen_pass2.py D1–D2 ｜ — ｜ CONFIRMED（「編碼」只出現在 cwo6s「同一種編碼」與 stats、code 兩張卡的「o200k_base 編碼」） ｜ —
37 ｜ 旁白沒有「本影片」「經查證」「根據官方文件」 ｜ 旁白 ｜ listen_pass2.py E1 ｜ — ｜ CONFIRMED（0 命中；最接近的是既有的 cwaf3「有官方文件把它比作短期記憶」（引述用語，第一輪已報）和 cwyee 的標籤名「待查證」；卡片上的「可查核的工作集」是文章的節名） ｜ —
38 ｜ 旁白沒有括號、網址、阿拉伯數字 ｜ 旁白 ｜ listen_pass2.py F ｜ — ｜ CONFIRMED（0；括號只在 title 卡副標「（Context Window）」與 code 卡 caption「（o200k_base 編碼）」，網址只在說明欄末行） ｜ —
39 ｜ 沒有超過 40 單位的句子 ｜ 旁白 ｜ listen_pass2.py A（同 `tools/video/core/timeline.mjs` 的 spokenUnits 算法） ｜ — ｜ CONFIRMED（0；最長 cwicb 31，新句最長 cwcp2、cwcxa 各 28；改後全稿 2,565 單位） ｜ —
40 ｜ 旁白的拉丁字母詞都在字典 ｜ 旁白 ｜ docs/videos/lexicon.json ｜ — ｜ CONFIRMED（只有 token → 投肯，11 句，新句 cwof9、cw4k9 也用它） ｜ —
41 ｜ 沒有 reveal 先於介紹它的句子 ｜ desk-stats、lost-middle-quote、three-fixes、handoff-items、workset-steps、desk-table ｜ listen_pass2.py H ｜ — ｜ CONFIRMED（新 steps 卡三個 reveal 各跟「第一步／第二步／第三步」同句出現；其餘與第一輪相同） ｜ —
42 ｜ 第一人稱都有意見標記 ｜ cw9er、cw4rn、cw0y7、cwk4g ｜ brief §站主觀點 ｜ — ｜ CONFIRMED（cw0y7「我不靠…」緊接 cw4rn「我的看法是」，同一段意見；cwr09、cwpzq 已不是第一人稱） ｜ —
43 ｜ shorts.json 與 video.json 一致（唯讀） ｜ shorts.json ｜ check_numbers.py（沿用第一輪） ｜ — ｜ CONFIRMED（引用的 10 個 shot 都還在；短片旁白是自己的短句，沒有沿用被改掉的第一人稱句；short-2 的「最常見的誤解」是 README §Shorts 規定的短片類型，不是事實主張） ｜ —
44 ｜ 21 個新插圖 prompt 不畫字、logo、真人、產品畫面 ｜ 新 shot 的 data.prompt ｜ 腳本掃描 ｜ — ｜ CONFIRMED（命中只有「no lettering」與橡皮印章的「face」） ｜ —

## 摘要

- **查了 44 條**（加長新增 27 含 steps 卡、聽眾審稿 6、全稿 grep 11）：確認 38、改了 2（#12 cw9ec、#18 cwcxa）、找不到 0、OUT OF SCOPE 4（#1、#10 情境句，#26 引導句，#32 「你可能覺得」）。引到示範的數字逐字對 JSON：217 字元、188 token 是第 42 次紀錄（`records[1]`），也是三份之最；壞摘要的「報價、燈具、旅遊」與好交接的「尚未核准、流會延期、不得發包、待辦」都是 `summary.text`／`good_handoff.text` 的逐字子字串；`demo_context.py` 在我的資料夾重跑，輸出與撰稿封包逐位元相同。
- **改了什麼**：（1）cw9ec「最直接的做法，是分批」→「那就分批」：文章的「最直接」是給「縮小本輪工作集」整套的，分批是「必要時」；（2）cwcxa「每份紀錄」→「相關紀錄」：文章第二步是「針對相關紀錄」，第一步的索引就是為了挑出相關紀錄。兩句都沒有 `say`，畫面與 reveal 不動；claims.md 的兩條依據、c13、c14 與進度各加一筆「查核第二輪」。
- **聽眾審稿的 6 句**：數字（三份、六十二）與名稱（token）都沒動；cwr09、cwpzq 不再是第一人稱，示範回到「拿三份紀錄實際算一次」「壓成一句話試試看」，對得上 demo-log「自行執行的計算」；cw9er 加了「我的看法是」，仍是條件句。
- **會過期的事實**：新句子沒有引進任何官方頁的數字，只用示範（tiktoken 0.14.0、`o200k_base`，2026-09-30）、文章（正式站頁第一輪今天 200）、arXiv v3（2023-11-20，不會過期）與 brief；第一輪列的級距「二十萬」「一百萬」、超限措辭、定義句沒有被加長輪動到。
- **意見不符**：沒有。新加的三句意見（cwk4g、cwka0、cwkop）與 cwnro 逐句對得上 brief §站主觀點；但那一節仍標「提案，待站主確認」，站主確認前這集不算定稿（第一輪同樣提醒）。
- **聽眾檢查**：沒有超過 40 單位的句子（最長 31）；沒有「本影片」「經查證」「根據官方文件」；旁白沒有括號、網址、阿拉伯數字；拉丁字母詞只有 token（字典：投肯）；六張有 reveal 的卡每個 reveal 都跟介紹它的句子同時出現；五個章末問題各停 1,200，最後一章回答開場。只報告不動的：summary-note、three-takeaways 兩個 shot 各帶兩句，README 寫「一個 shot 只帶一句」，lint 沒擋，屬節奏。
- **lint**：`node tools/video/cli.mjs lint --slug ai-term-context-window` → 0 errors, 1 warning（「about 12.3 minutes; the target is 9-11」，已知的估計值警告）；Estimate 12.3 min、127 lines、2,565 spoken units（改前 2,570）。第一輪的 63 項數字檢查改後仍全過（唯一的 FAIL 是第一輪就知道的誤判：「舊方案」是會議的方案）。
- **懷疑但沒動**：（1）cw4k9 與 stats 卡的算式「視窗 ÷ 每份 token」是粗估：桌上還有問題、規則、回答的位子（c2），實際放得下的份數會少一些；brief 與 stats 卡就是這樣定義，旁白說的也是量級，沒動。（2）cw5mv「他們測的是多份文件一起放進去的問答」：論文測了兩個任務（多文件問答與鍵值檢索），旁白只講一個、沒說「只」；文章也只說「特定長文問答與資訊查找任務」，沒動。（3）改後第四章的順序是「分批 → 合併檢查 → 縮小工作集」，文章是「縮小工作集，必要時分批 → 合併檢查」；兩邊每句都對、只是次序，cw4f0 第一輪已確認，規則不改順序。（4）`spec.json` 在我查核期間從資料夾消失了：01:03 前的列表還有它（48,121 位元組，00:42 寫的），01:43 的列表已經沒有，三集試片的資料夾現在都沒有 spec.json，應該是別的 session 清掉的（加長輪已經不用它）。不是我刪的：我沒跑任何 rm，patch 腳本只寫 video.json 與 claims.md。第一輪說它還留著 cwdgg 的舊句，現在無從比對。（5）cwpzq「試試看」是邀請觀眾，但 code 卡放的是撰稿自己寫的那句摘要；不算把示範說成站主做的，沒動。（6）cw2pd「第三種最難察覺」與 cwpmk「服務直接告訴你，輸入太長」維持第一輪的判定，這一輪沒重查。
- **要不要第三輪**：這一輪改了 2 個事實（規則：超過 3 個才要），**不需要**；站主確認 brief 的觀點提案之前，仍不能說這集已定稿。
