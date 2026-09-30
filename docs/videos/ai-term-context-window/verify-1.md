# verify-1：上下文視窗（Context Window）是什麼

- 查核日：2026-09-30。第一輪，獨立查核者（Claude，沒有寫過這份稿子；撰稿者的 claims.md 只當線索，不當證據）。
- 方法：從 `video.json` 自己抽出 94 條可查主張（清單在 `SCRATCH/ai-term-context-window/verify/claims-list.md`），每條今天重開官方頁（`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同主機間隔 ≥ 1.2 秒，網路搜尋 0 次），或在自己的資料夾重跑示範腳本（`python3 demo_context.py`，Python 3.11.15、tiktoken 0.14.0、`o200k_base`）：輸出與撰稿封包的 `demo/demo-context.json` 逐位元相同。輔助腳本與今天抓下的頁面在 `SCRATCH/ai-term-context-window/verify/`（`check_numbers.py`、`listen_pass.py`、`http_check.py`、`live-*.html`、`http-results.json`）。
- 今天看到的頁面日期：Google Long context「Last updated 2026-06-22 UTC」；Google Understand and count tokens「2026-09-23」；Google Models「2026-09-24」；Anthropic Context windows 沒有頁面日期（原網址 docs.anthropic.com 今天仍轉址到 platform.claude.com，200）；arXiv 2307.03172 v3 2023-11-20；PyPI JSON：tiktoken 最新版 0.14.0（2026-08-17 上傳，MIT）。

## 主張表

# ｜ 主張 ｜ 位置 ｜ 網址或示範檔 ｜ HTTP ｜ 判定 ｜ 改前 → 改後

1 ｜ 標題「上下文視窗（Context Window）是什麼？塞得進去，不等於讀得懂｜AI 名詞十分鐘」 ｜ youtube.title ｜ ai-terms/README §標題（名詞在前、帶英文、後綴、無集數） ｜ — ｜ CONFIRMED ｜ —
2 ｜ 縮圖 headline「上下文視窗」、tag「AI 名詞十分鐘」、sub「留著，不等於讀到」 ｜ thumbnail.data ｜ brief §素材；README §縮圖 ｜ — ｜ CONFIRMED ｜ —
3 ｜ 說明欄：桌上有本輪問題、規則、部分歷史、附件、工具結果，還要留位子給回答；桌面多大就是視窗，用 token 算 ｜ youtube.description ｜ https://platform.claude.com/docs/en/build-with-claude/context-windows（「Everything in the request counts…system prompt, every message…tool results, images, and documents…The output…counts too」）；https://ai.google.dev/gemini-api/docs/tokens（「combined limit of input and output tokens」） ｜ 200／200 ｜ CONFIRMED ｜ —
4 ｜ 說明欄：2023 年的研究 Lost in the Middle 發現關鍵資訊放在長上下文中間時表現明顯下降 ｜ youtube.description ｜ https://arxiv.org/abs/2307.03172（摘要；v1 2023-07-06） ｜ 200 ｜ CONFIRMED ｜ —
5 ｜ 說明欄：三種忘記與各自處理（縮小工作集／補上核對過的原文／重組比對、要求指出依據） ｜ youtube.description ｜ 站內文章文末比較表（repo JSON；https://mokaair.com/zh-TW/life/ai-context-window-explained） ｜ 200 ｜ CONFIRMED ｜ —
6 ｜ 說明欄：604 字元、535 個 token；62 字元摘要壓掉「尚未核准」，同樣 62 字元的交接單留住；tiktoken 是開源工具、自行計算 ｜ youtube.description ｜ 重跑 demo_context.py；https://pypi.org/pypi/tiktoken/json（MIT License、0.14.0） ｜ 重跑相同／200 ｜ CONFIRMED ｜ —
7 ｜ 說明欄：交接單五格；先由人核對數字、日期與決議狀態 ｜ youtube.description ｜ 文章 §一般使用者如何保留工作連續性 ｜ 200 ｜ CONFIRMED ｜ —
8 ｜ 說明欄末行總索引網址，utm_campaign=ai-term-context-window ｜ youtube.description ｜ https://mokaair.com/zh-TW/life/ai-terms-index ｜ 200 ｜ CONFIRMED ｜ —
9 ｜ 標籤（上下文視窗、Context Window、Lost in the Middle…） ｜ youtube.tags ｜ 無事實 ｜ — ｜ OUT OF SCOPE ｜ —
10 ｜ sources 五筆今天都開得到，checked_on 2026-09-30 ｜ sources[] ｜ 五個網址（見上） ｜ 全部 200（PyPI 專案頁對 curl 回 3 KB 的機器人驗證頁，版本改由 JSON API 確認） ｜ CONFIRMED ｜ —
11 ｜ assets：diagram-1.svg 存在、Mokaair 自有 ｜ assets[0] ｜ apps/web/public/guides/ai-context-window-explained/diagram-1.svg（內含「© Mokaair 製圖 2026」） ｜ — ｜ CONFIRMED ｜ —
12 ｜ 上個月的對話還在畫面裡，模型這一次卻可能一個字都沒看到 ｜ cw293 ｜ 文章首段「聊天畫面裡看得到一段舊對話，不代表模型這一次也收到那段原文」；Anthropic 頁註 1「rolling "first in, first out"」 ｜ 200 ｜ CONFIRMED ｜ —
13 ｜ 十分鐘，你會分得出沒收到、被摘掉、看了卻答錯 ｜ cw26m ｜ 承諾句 ｜ — ｜ OUT OF SCOPE ｜ —
14 ｜ 模型每一次只拿到應用程式放上桌面的東西 ｜ cwtjf ｜ 文章 §視窗裡放的是當次可用的資料「桌上的東西由應用程式準備」 ｜ 200 ｜ CONFIRMED ｜ —
15 ｜ 放什麼上桌是應用程式準備的，不一定是你貼過的全部 ｜ cw8cz ｜ 文章同節「不一定等於你所有上傳檔案或全部聊天紀錄」 ｜ 200 ｜ CONFIRMED ｜ —
16 ｜ 有的放全文，有的先搜尋相關段落 ｜ cw2ka ｜ 文章同節；Google Long context「using RAG with vector databases」 ｜ 200 ｜ CONFIRMED ｜ —
17 ｜ 有的把舊對話換成一段摘要 ｜ cwiz3 ｜ 文章同節「保留摘要」；Google Long context「summarizing content」 ｜ 200 ｜ CONFIRMED ｜ —
18 ｜ 桌上有本輪的問題，還有應用程式先放好的規則 ｜ cw7ed ｜ Anthropic「the system prompt, every message in messages」 ｜ 200 ｜ CONFIRMED ｜ —
19 ｜ 一部分的歷史訊息，可能是全部，也可能只是最近幾段 ｜ cwcmp ｜ Anthropic「previous turns are preserved completely」（API）＋頁註 1（聊天介面 FIFO） ｜ 200 ｜ CONFIRMED ｜ —
20 ｜ 你貼的附件、它查到的資料也在桌上 ｜ cwb3u ｜ Anthropic「including tool results, images, and documents」 ｜ 200 ｜ CONFIRMED ｜ —
21 ｜ 還要留一塊空位給回答 ｜ cw2m7 ｜ Anthropic「The output Claude generates for the turn…counts too」；Google tokens「combined limit of input and output tokens」 ｜ 200 ｜ CONFIRMED ｜ —
22 ｜ big 卡：桌面多大就是上下文視窗；用 token 算；輸入和輸出都佔位子 ｜ desk-is-window.data ｜ Google tokens「Each Gemini model has a maximum number of tokens it can handle. The context window defines the combined limit of input and output tokens.」；文章首段定義句 ｜ 200 ｜ CONFIRMED ｜ —
23 ｜ 這張桌面有多大，就是上下文視窗，單位是 token ｜ cwos5 ｜ 同 22 ｜ 200 ｜ CONFIRMED ｜ —
24 ｜ 有官方文件把它比作短期記憶：人一次記得住的有限，模型也是 ｜ cwaf3 ｜ Google Long context「An analogy for the context window is short term memory. There is a limited amount of information that can be stored in someone's short term memory, and the same is true for generative models.」 ｜ 200 ｜ CONFIRMED ｜ —
25 ｜ token 是模型自己的單位，不是字數；三份會議紀錄算過一次 ｜ cwr09 ｜ Google tokens「a token is equivalent to about 4 characters」「Tokens can be single characters…or whole words」；demo 重跑 ｜ 200／重跑相同 ｜ CONFIRMED ｜ —
26 ｜ 三份紀錄加起來六百零四個字元 ｜ cwfqu ｜ demo all_three.chars = 604（198+217+189） ｜ 重跑相同 ｜ CONFIRMED ｜ —
27 ｜ stats：535 token／三份紀錄 604 字元 ｜ desk-stats.stats[0] ｜ demo all_three.tokens = 535（三份各自 180+188+167 也是 535） ｜ 重跑相同 ｜ CONFIRMED ｜ —
28 ｜ stats：178 平均每份 token（535 ÷ 3） ｜ desk-stats.stats[1] ｜ 535/3 = 178.33 ｜ 重跑相同 ｜ CONFIRMED ｜ —
29 ｜ stats：1,121 份／二十萬 token 的桌面／每月開會約 93 年 ｜ desk-stats.stats[2] ｜ demo fits.200000 = 1121；1121/12 = 93.4（demo 用未取整的份數算出 93.5，兩者都是「約 93 年」） ｜ 重跑相同 ｜ CONFIRMED ｜ —
30 ｜ stats：5,607 份／一百萬 token 的桌面／約 467 年 ｜ desk-stats.stats[3] ｜ demo fits.1000000 = 5607；5607/12 = 467.25（demo 467.3） ｜ 重跑相同 ｜ CONFIRMED ｜ —
31 ｜ stats source：o200k_base 自行計算；二十萬與一百萬是官方文件的兩個級距，以官網為準 ｜ desk-stats.source ｜ demo encoding；Anthropic「Context window sizes by model」：多個模型 1M，「Other Claude models, including Claude Sonnet 4.5, have a 200k-token context window」；Google Long context「1 million or more tokens」；Google Models「1M token context window」 ｜ 200／200／200 ｜ CONFIRMED ｜ —
32 ｜ 同一種編碼算下來，三份一共五百三十五個 token ｜ cwo6s ｜ demo all_three.tokens ｜ 重跑相同 ｜ CONFIRMED ｜ —
33 ｜ 平均一份大約一百七十八個 ｜ cwbeg ｜ 178.33 ｜ 重跑相同 ｜ CONFIRMED ｜ —
34 ｜ 二十萬 token 的桌面能放一千一百多份，每個月開一次會要開九十三年 ｜ cwzgs ｜ 1121 份；1121/12 = 93.4 ｜ 重跑相同 ｜ CONFIRMED ｜ —
35 ｜ 一百萬 token 的桌面放得下五千六百多份，四百多年的會議 ｜ cwyeb ｜ 5607 份；467 年 ｜ 重跑相同 ｜ CONFIRMED ｜ —
36 ｜ 旁白不唸模型名稱、不講價格與方案 ｜ 全部 101 句 ｜ 腳本 grep：無 Claude／Gemini／GPT／Sonnet／Opus／價格字眼（「舊方案」是會議的方案，不是付費方案） ｜ — ｜ CONFIRMED ｜ —
37 ｜ 沒有超限、全部放上桌，模型還是可能搞混哪一版有效 ｜ cw5l9 ｜ 文章 §容量上限與有效使用能力分開看「即使整份資料沒有超限，模型仍可能混淆哪一版有效」 ｜ 200 ｜ CONFIRMED ｜ —
38 ｜ diagram caption：紀錄經選取才進入本輪工作集；容量與事實狀態分開驗證 ｜ flow-diagram.data ｜ SVG `<desc>`「外部紀錄經選取後進入當次上下文…容量檢查與決議狀態核對是兩個分開的檢查」 ｜ — ｜ CONFIRMED ｜ —
39 ｜ 紀錄先被選進工作集模型才看得到；容量和事實是兩個檢查 ｜ cwad3 ｜ 同 38 ｜ — ｜ CONFIRMED ｜ —
40 ｜ 二零二三年一篇研究，把答案放在長文的不同位置，看它找不找得到 ｜ cwm26 ｜ arXiv 摘要「performance can degrade significantly when changing the position of relevant information」；v1 2023-07-06 ｜ 200 ｜ CONFIRMED ｜ —
41 ｜ 同一份關鍵文件從開頭移到中間再到結尾 ｜ cwmi0 ｜ arXiv 摘要「beginning or end of the input context…in the middle」「multi-document question answering」 ｜ 200 ｜ CONFIRMED ｜ —
42 ｜ quote 卡英文原句逐字 ｜ lost-middle-quote.quote ｜ arXiv 摘要：腳本比對為逐字子字串 ｜ 200 ｜ CONFIRMED ｜ —
43 ｜ quote 卡翻譯 ｜ lost-middle-quote.translation ｜ 對原句逐段：often highest→通常最高；significantly degrades→明顯下降；must access…in the middle of long contexts→必須從長上下文的中間取用 ｜ 200 ｜ CONFIRMED ｜ —
44 ｜ kicker「二〇二三年的研究原句」；source「Liu 等，Lost in the Middle，arXiv:2307.03172，2023」 ｜ lost-middle-quote.data ｜ arXiv：第一作者 Nelson F. Liu；v1 2023-07-06、v3 2023-11-20；TACL 2023 ｜ 200 ｜ CONFIRMED ｜ —
45 ｜ 答案放在開頭或結尾表現最好；放在中間明顯變差 ｜ cw0na ｜ 同 42 ｜ 200 ｜ CONFIRMED ｜ —
46 ｜ 就算是專門做長上下文的模型，也一樣會在中間迷路 ｜ cwrtb ｜ arXiv 摘要「even for explicitly long-context models」 ｜ 200 ｜ CONFIRMED ｜ —
47 ｜ 這不是每個模型、每個問題都會這樣的鐵律 ｜ cwnlz ｜ 文章「這不是所有模型在所有問題上的固定規則」 ｜ 200 ｜ CONFIRMED ｜ —
48 ｜ 容量是資源檢查，理解是另一場考試；資源檢查過了考試不一定過 ｜ cwgcj、cwn2q ｜ 文章「『放得下』與『答得準』需要不同驗證」；brief §觀眾看完能做到的事 3 ｜ 200 ｜ CONFIRMED ｜ —
49 ｜ 把桌子換大一張，舊方案和撤回單還是各在一頭 ｜ cwavs ｜ 文章「這時只把容量加大，沒有修正版本關係」 ｜ 200 ｜ CONFIRMED ｜ —
50 ｜ 把提案、決議、撤回、待查證一項一項標清楚 ｜ cwyee、cwfnp ｜ 文章「明確標出提案、決議、撤回與待查證項目」 ｜ 200 ｜ CONFIRMED ｜ —
51 ｜ 三份紀錄裡維修案三次都尚未核准 ｜ cw3i4 ｜ demo R1「本案尚未核准」、R2「目前仍未核准」、R3「仍未核准」 ｜ 重跑相同 ｜ CONFIRMED ｜ —
52 ｜ 「這四個字」＝尚未核准 ｜ cwiyl ｜ 4 個字 ｜ — ｜ CONFIRMED ｜ —
53 ｜ 第一次同意研究，第二次列入區權會，第三次區權會流會、延期 ｜ cwjto ｜ demo R1「決議『同意研究』」、R2「列入 5 月區分所有權人會議討論」、R3「因人數不足流會，本案延至下次會議」 ｜ 重跑相同 ｜ CONFIRMED ｜ —
54 ｜ 第一種沒送進去：服務直接告訴你輸入太長 ｜ cwpmk ｜ Anthropic「If the input alone already exceeds the model's context window, the API returns a 400 invalid_request_error ("prompt is too long") on every model.」；文章「若服務明確回報輸入過長」 ｜ 200 ｜ CONFIRMED（只確認到 API；見「懷疑但沒動」2） ｜ —
55 ｜ 分批之後還要合併檢查；某一次的決議可能改了另一份紀錄 ｜ cw9my、cwmbr ｜ 文章 §超限、摘要漏失與理解錯誤「分批後仍需要合併檢查，因為某個決議可能修改另一份紀錄」 ｜ 200 ｜ CONFIRMED ｜ —
56 ｜ 縮小這一輪的工作集，只留相關章節，記下原文在哪 ｜ cw4f0 ｜ 文章同節「縮小本輪工作集，保留相關章節與原文位置」 ｜ 200 ｜ CONFIRMED ｜ —
57 ｜ 第二種「最常見」，摘要漏掉 ｜ cwdgg ｜ 「最常見」在文章、brief.md、封包 outline、官方頁都找不到；沒有任何來源說哪一種忘記最常發生 ｜ — ｜ NOT FOUND（刪掉限定詞） ｜ 「第二種最常見，摘要漏掉：對話太長，被壓成一段摘要。」→「第二種，摘要漏掉：對話太長，被壓成一段摘要。」
58 ｜ 摘要留得住主題，留不住狀態，尤其是否定條件 ｜ cwc6q ｜ 文章「摘要常容易保留主題卻丟掉細微狀態」「『不得視為已核准』這種否定條件」 ｜ 200 ｜ CONFIRMED（文章寫「常容易」，旁白說成通則；見「懷疑但沒動」3） ｜ —
59 ｜ 三次會議壓成一句話，六十二個字元 ｜ cwpzq ｜ demo summary.chars = 62 ｜ 重跑相同 ｜ CONFIRMED ｜ —
60 ｜ code 卡兩段文字逐字、62／55 與 62／60、highlight 第 7 行 ｜ two-texts.data ｜ 腳本：去掉排版換行後與 demo 的 SUMMARY／GOOD_HANDOFF 逐字相同；templates.mjs 的 highlight 是 1 起算的行號，第 7 行是「維修案狀態：尚未核准…」 ｜ 重跑相同 ｜ CONFIRMED ｜ —
61 ｜ code caption：自己寫、自己算（o200k_base）；字元數一樣，差別在「尚未核准」 ｜ two-texts.caption ｜ demo ｜ 重跑相同 ｜ CONFIRMED ｜ —
62 ｜ 上面的摘要「尚未核准」不見了；下面的交接留住了 ｜ cw05s ｜ demo keeps_not_approved false／true ｜ 重跑相同 ｜ CONFIRMED ｜ —
63 ｜ 字元數一模一樣，token 數只差五個 ｜ cw7le ｜ 62＝62；60−55＝5 ｜ 重跑相同 ｜ CONFIRMED ｜ —
64 ｜ 只帶這句摘要開新對話，桌上就沒有一個字說這個案子不能發包 ｜ cwio4 ｜ SUMMARY 全文不含「尚未核准」「未核准」「不得發包」「不得」 ｜ 重跑相同 ｜ CONFIRMED ｜ —
65 ｜ 它要是把維修案寫成即將施工，錯的不是模型，是交接（條件句） ｜ cw9er ｜ brief §示範「不宣稱…是實測結果」；demo-log「沒有把任何文字送進任何模型」；旁白是條件句，沒把模型的回答說成事實 ｜ — ｜ CONFIRMED ｜ —
66 ｜ 摘要漏掉的要用已核對的原文補回去 ｜ cwnnb ｜ 文章「必要處以原文補強，避免摘要成為唯一依據」 ｜ 200 ｜ CONFIRMED ｜ —
67 ｜ 重開對話要帶未解的問題、取消的方向、驗收要求 ｜ cwer0 ｜ 文章「不只帶結論，也要帶未解問題、已取消方向、驗收要求」 ｜ 200 ｜ CONFIRMED ｜ —
68 ｜ 第三種「最難察覺」：原文在桌上它還是答錯 ｜ cw2pd ｜ 文章「若原文確實在輸入裡，模型仍回答錯誤」；「最難察覺」無出處，但第一種有服務回報、第二種摘要看得出、第三種沒有任何訊號，屬描述而非可查數字 ｜ 200 ｜ CONFIRMED（描述；見「懷疑但沒動」1） ｜ —
69 ｜ 舊方案、撤回、報價草稿混在一起會抓錯版本 ｜ cwcls ｜ 文章 §容量上限與有效使用能力分開看 ｜ 200 ｜ CONFIRMED ｜ —
70 ｜ 把相關段落拉到一起；直接問哪一版有效並要求指出依據 ｜ cwx7i、cwpjd ｜ 文章「把相關段落拉到一起、明確提出比對問題，並要求指出依據」 ｜ 200 ｜ CONFIRMED ｜ —
71 ｜ 重問答對是改善訊號，不是永久可靠的證明 ｜ cwfxi ｜ 文章同句 ｜ 200 ｜ CONFIRMED ｜ —
72 ｜ 留幾個容易混淆的例子確認方法對別的文件也管用 ｜ cw2v7 ｜ 文章「留下幾個容易混淆的例子，確認整理方法對其他文件也有幫助」 ｜ 200 ｜ CONFIRMED ｜ —
73 ｜ compare 卡三列（先查什麼／怎麼處理） ｜ three-fixes.data ｜ 文章文末表（完整請求與服務限制／交接摘要是否保留條件／版本關係與回答依據；縮小資料集／補上已核對原文／重組比對並驗證） ｜ 200 ｜ CONFIRMED ｜ —
74 ｜ 先查是哪一種，再對症處理 ｜ cwicb、cw4wt ｜ 同 73 ｜ 200 ｜ CONFIRMED ｜ —
75 ｜ cta：完整整理步驟與檢查表在說明欄第一行的文章 ｜ article-cta.data、cwcbe ｜ 文章 §把會議紀錄整理成可查核的工作集（三步）＋文末表；文章頁今天 200；package 會把 source_guide 的文章接到說明欄 ｜ 200 ｜ CONFIRMED ｜ —
76 ｜ 交接單不是把前面聊過的縮短，而是讓下一輪知道怎麼接手 ｜ cwe28、cwxci ｜ 文章「它的價值是讓下一輪知道如何接手，而不是單純縮短前面聊過的內容」 ｜ 200 ｜ CONFIRMED ｜ —
77 ｜ bullets 五格：目標／已確認的事實／原文位置／不能違反的限制／下一步 ｜ handoff-items.data、cwvwf–cweff ｜ 文章「目標、目前已確認的事實、原文位置、不能違反的限制，以及接下來要做的事」 ｜ 200 ｜ CONFIRMED ｜ —
78 ｜ 交接單先由人核對，尤其數字、日期、決議狀態 ｜ cwhq0 ｜ 文章「交接稿先由人核對，尤其是數字、日期和決議狀態」 ｜ 200 ｜ CONFIRMED ｜ —
79 ｜ 「同意研究」跟「正式通過」摘要很容易合併成同一種 ｜ cwvy3 ｜ 文章「留意『建議』『同意研究』與『正式通過』是否被合併成相同狀態」 ｜ 200 ｜ CONFIRMED ｜ —
80 ｜ 「正在討論」不能在交接單上變成「已經決定」 ｜ cw238 ｜ 文章 callout「『正在討論』不能在摘要裡變成『已決定』」 ｜ 200 ｜ CONFIRMED ｜ —
81 ｜ 很多人把專案、附件或記憶功能當成無限大的空間 ｜ cwf76 ｜ 文章「不要把專案、附件或記憶功能當成無限空間」 ｜ 200 ｜ CONFIRMED ｜ —
82 ｜ 記憶功能是倉庫不是桌面；取回來放上桌才佔這一輪的空間 ｜ cwbtf、cw4bo ｜ 文章 §視窗裡放的是當次可用的資料 第三段；https://docs.langchain.com/oss/python/concepts/memory（「Long-term memory stores…across sessions…can be recalled at any time」「A full history may not fit inside an LLM's context window」）；Anthropic「Everything in the request counts toward the context window」 ｜ 200／200 ｜ CONFIRMED ｜ —
83 ｜ 別假設倉庫會逐字留下你給過的每一份文件 ｜ cwh55 ｜ 文章「不能假設記憶功能會逐字保留你給過的所有文件」 ｜ 200 ｜ CONFIRMED ｜ —
84 ｜ 長資料待在有整理的地方按問題取用；留一條查回原文的路 ｜ cwqax、cwh2g ｜ 文章「讓長資料待在有組織的來源裡，按問題取用，並保留查回原文的途徑」 ｜ 200 ｜ CONFIRMED ｜ —
85 ｜ 要比對全文就逐段處理再總體校對 ｜ cwtjm ｜ 文章「明確安排逐段處理與總體校對」 ｜ 200 ｜ CONFIRMED ｜ —
86 ｜ table 卡四列：token 刻度／上下文視窗 桌面／記憶 倉庫／模型參數 訓練來的本事、不在桌上 ｜ desk-table.data ｜ Google tokens（token 是計量單位）；文章 §視窗裡放的是當次可用的資料（參數、記憶）；Anthropic「different from the large corpus of data the language model was trained on…a "working memory"」 ｜ 200／200 ｜ CONFIRMED ｜ —
87 ｜ token 是刻度；上下文視窗是容器；記憶是倉庫；訓練得到的知識在參數裡 ｜ cwuzq、cwm1m、cwnyo、cwuni ｜ 同 86 ｜ 200 ｜ CONFIRMED ｜ —
88 ｜ 算 token 是在量長度；看視窗是在問這一輪放不放得下 ｜ cwi5w ｜ 同 22 ｜ 200 ｜ CONFIRMED ｜ —
89 ｜ 今天貼進去的決議它可以照著答，但不會因此變成它的知識 ｜ cwcer、cw8xe ｜ 文章「你今天貼入會議決議，模型可以依它作答，但不代表這些內容立刻成為模型權重的一部分」 ｜ 200 ｜ CONFIRMED ｜ —
90 ｜ 開新對話桌面重來；決議會不會跟過來看應用程式怎麼做 ｜ cwkh2 ｜ 文章「或所有新對話從此都能讀到」「具體行為由產品實作決定」 ｜ 200 ｜ CONFIRMED ｜ —
91 ｜ 站主觀點：先看桌上有什麼再決定要補什麼；不靠換更大的視窗；摘要一定拿去對原文；先問是沒放上去還是放了沒讀到 ｜ cw4rn、cw0y7、cw5u2 ｜ brief §站主觀點（逐句對得上；該節標「提案，待站主確認」） ｜ — ｜ CONFIRMED ｜ —
92 ｜ 真正要看的是這一輪收到什麼、限制留住了沒、結果追不追得到證據 ｜ cwuec ｜ 文章「本輪收到哪些資訊、關鍵限制有沒有保留、結果能否追溯到證據」 ｜ 200 ｜ CONFIRMED ｜ —
93 ｜ 下一步：說明欄第一行的文章，照三個步驟整理 ｜ cwrcr、closing.cta ｜ 文章 §把會議紀錄整理成可查核的工作集 有三步；brief：token 那集未上架，片尾只指文章 ｜ 200 ｜ CONFIRMED ｜ —
94 ｜ outro 三行與收尾句「留在畫面裡的訊息，模型不一定讀到；先看桌上有什麼」 ｜ closing.data.lines、cwwtb ｜ brief §大綱 最後一句、§站主觀點 ｜ — ｜ CONFIRMED ｜ —

## 摘要

- **查了 94 條**：確認 91、改了 1（#57，NOT FOUND，刪掉「最常見」）、找不到 1（同一條）、OUT OF SCOPE 2（#9 標籤、#13 承諾句）。示範的每個數字（604／535／178／1,121／5,607／93／467／62／55／60／差 5）都對到我自己重跑的 `demo-context.json`（與撰稿封包的輸出逐位元相同）；quote 卡的英文原句是 arXiv 摘要的逐字子字串；code 卡兩段文字去掉排版換行後與腳本裡的字串逐字相同，highlight 第 7 行（1 起算）正是「尚未核准」那行。
- **會過期的事實（今天看到的日期）**：「二十萬」「一百萬」兩個級距：Anthropic Context windows（2026-09-30 開啟，頁面無日期）寫多個模型 1M、「Other Claude models, including Claude Sonnet 4.5, have a 200k-token context window」；Google Long context（Last updated 2026-06-22）「1 million or more tokens」；Google Models（2026-09-24）「1M token context window」。字卡已標「以官網為準」，旁白不唸模型名。定義句：Google tokens（2026-09-23）「combined limit of input and output tokens」。超限回報的措辭「400 invalid_request_error ("prompt is too long")」（Anthropic，2026-09-30），影片只說「服務直接告訴你，輸入太長」。tiktoken 0.14.0 是今天 PyPI 的最新版（2026-08-17 上傳）；出新版或換編碼要重算。arXiv v3 2023-11-20，不會過期。
- **意見不符**：沒有。三句站主觀點（cw4rn、cw0y7、cw5u2）與 outro 三行逐句對得上 brief，但 brief 的站主觀點仍標「提案，待站主確認」，站主未確認前這集不算定稿。cw9er「錯的不是模型，是交接」是 brief 的立場但沒有「我」的標記；cwr09「我拿三份會議紀錄算過一次」、cwpzq「我把三次會議壓成一句話」把示範說成站主親自做的（示範是撰稿代理 2026-09-30 執行，我今天重跑過），是否用第一人稱由站主決定。
- **聽眾檢查**：沒有超過 40 單位的句子（最長 cwicb 31 單位）；沒有「本影片」「經查證」「根據官方文件」；cwaf3「有官方文件把它比作短期記憶」是引述用語，最接近那一類，留給站主判斷；旁白的拉丁字母詞只有 token（字典：投肯）；旁白沒有括號、網址、阿拉伯數字；五張有 reveal 的卡（stats、quote、compare、bullets、table）每個 reveal 都跟介紹它的那句同時出現；停頓（開場 900、你以為 600、五個章末問題 1200）與每章末尾是問題、最後一章回答開場，都合規則。
- **lint**：`node tools/video/cli.mjs lint --slug ai-term-context-window` → 0 errors, 0 warnings；Estimate 10.1 min、101 lines、2,096 spoken units（改前 2,099）。
- **懷疑但沒動**：（1）cw2pd「第三種最難察覺」也是沒出處的最高級，但它由三種忘記的定義推得（第一種有服務回報、第二種摘要本身看得出、第三種沒有訊號），當描述留著。（2）cwpmk「服務直接告訴你，輸入太長」只在 API 文件確認（Anthropic：每個模型都回 400）；聊天介面可能默默捨棄舊訊息（同頁頁註 1），那種「沒送進去」不會有回報；旁白沿用文章的三分法，沒改。（3）cwc6q「摘要留得住主題，留不住狀態」是通則語氣，文章寫「常容易」；意思沒錯，沒改。（4）`spec.json` 還留著 cwdgg 的舊句「第二種最常見」，不在我可改的檔案內。（5）`sources[]` 的 PyPI 專案頁對 curl 只回機器人驗證頁（瀏覽器開得到），版本與授權改由 JSON API 確認，網址沒換。（6）stats 卡「約 93 年」由 1,121 ÷ 12 = 93.4 來，demo JSON 的 93.5 是用未取整的份數算的，兩者都是「約 93 年」。
- **要不要第二輪**：這一輪只改了 1 個事實（規則：超過 3 個才要），**不需要**；但站主確認 brief 的觀點提案之前，不能說這集已定稿。
