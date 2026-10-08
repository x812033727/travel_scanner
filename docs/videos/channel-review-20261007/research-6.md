# 搜尋需求與競品占位：Mokaair 18 個題目在 YouTube 台灣有沒有人搜、誰已經占住、Mokaair 的角度差在哪

> **事實查核後的修正（2026-10-07 下午）**
> - Google 2025 台灣「快速竄升 AI 工具」官方前十依序是 Gemini、DeepSeek、Grok、NotebookLM、ChatGPT、Google AI Studio、Nano Banana、Sora、Manus、Cursor（blog.google 台灣官方文 2025-12-04）；本文漏了 DeepSeek、Grok、ChatGPT，techbang 不是榜單來源。「Google 免費工具是最熱入口」只能說「Gemini 第一、前六名三個是 Google 工具」。
> - 今天比昨天厲害 bj07f9II6NQ 實際上架 2026-08-17（非 09-07），Mokaair 晚 41 天；整體「晚 4 天到 5 週」改「晚 5 天到 6 週」（Opus 5–6 天、Cursor 32 天、學生方案 38 天、Hugging Face 41 天）。
> - channels/*.dated.json 的日期是頻道頁相對時間換算，近期 ±1 天、超過一個月差數週：Whoops Opus 09-24、可波 Opus 09-25、黃敬峰 09-28、可波 GPT-6 Astra 09-05、Whoops GPT-6 Sol 09-24。
> - 「拆解式角度停在百次、該不該換角度拿 21,000」要弱化：可波 09-25 幾乎與 Whoops 同日且比其他三支都早，可波其他片常態 10 萬–35.7 萬次，21,000 主要反映頻道觸及；GPT-6 那組比的是不同子題。
> - Google Vids 前 12 名的中文競品還有 SaKai's Channel 2,620、AI 生活筆記 1,594／1,783、度白視界 189,212（綜合片）；知川 0ROKOt71q3o 是 10-04 上架、比 Mokaair 晚 4 天卻已 1,237 次。
> - Auto Router 搜尋回 12 筆，只有 2 筆是 Auto Router 主題，Mokaair 排第 3；Mokaair 排第 1 的是 WAF、資安百分比、Cursor、Connected Apps 四題。
> - 建議詞每日變動（「chatgpt 方案」「Grok 4.7」兩天內已不同），引用請標 2026-10-07；「AI 代理」的建議其實含「ai 代理人」。ytsearch12 與建議詞只能看競爭與需求訊號，量不到搜尋量。
> - Whoops SEO 是否「全自動、無真人、無人聲」沒有依據，改「同為極小頻道（18 訂閱）的 2–7 分鐘新聞解說」；Mokaair 中位數 24（資料包）／25（10-07 重抓）。
> - 「yt-dlp 抓回全英文標題」只適用頻道列表與搜尋結果；單支 --dump-json 回的是中文標題，暗示原始標題是中文、英文只是在地化；仍建議站主在 Studio 確認。


# Mokaair 18 支影片的搜尋需求與競品占位診斷

抓取日期 2026-10-07。工具：`yt-dlp` 的 `ytsearch12:`（前 12 名）、`suggestqueries.google.com`（`ds=yt&hl=zh-TW&gl=TW`，即台灣 YouTube 搜尋框建議）、各競品頻道最近 12–15 支（含 `approximate_date`）。原始檔都在 `<分析暫存區>/work/seo/`（`results/`＝搜尋、`sugg/`＝建議、`channels/`＝頻道列表）。

兩個限制先說：
- ytsearch 的排序受 yt-dlp 預設語系影響，不是 100% 等於台灣使用者看到的順序；但「有沒有人做、做多大」的判斷不受影響。
- 影片單頁 metadata（上架日、留言）在抓到一半時被 YouTube 擋（「Sign in to confirm you're not a bot」），所以競品上架日只對有列出頻道頁的那幾個頻道有（用 `approximate_date`），其餘用標題或說明欄裡的日期。

## 0. 先看一個對照組

| 頻道 | 做法 | 09-23～10-07 的觀看 |
|---|---|---|
| **Mokaair**（3 訂閱） | 新聞＋深色投影片／插圖＋合成旁白，8 分鐘 | 18 支：0–252，中位數約 20 |
| **Whoops SEO**（17 訂閱） | 新聞＋投影片，「X 是什麼｜N 分鐘看懂」，2–5 分鐘 | 12 支：0、2、41、27、3、172、432、771、200、232、486、62 |
| **AI 好友實驗室**（2,450 訂閱） | 系列解說「認識 AI 素養 01–06」「認識開源 AI 01–05」 | 12 支：9–317 |
| **黃敬峰**（2,090 訂閱） | 新聞評論，「每個台灣 CEO 必知的 3 個…」 | 12 支：9–311 |
| **可波 AI 白話**（6,590 訂閱） | 同樣的新聞，標題是「該換嗎／懶人包／台灣開通一次看完」 | 12 支：1,100–357,000 |

同一週、同一批新聞，無人聲投影片路線的天花板目前就是幾百次；差距不在畫面精緻度，在題目與標題角度（下面逐題證明）。

## 1. 18 支分三組

### A 組：有搜尋需求，而且 Mokaair 的角度能贏（4 支）

| # | 影片 | 證據：需求 | 證據：競爭 | Mokaair 現況 |
|---|---|---|---|---|
| 8 | Google Vids 免費做 AI 影片 | 建議詞「google vids」為空（量不大），但「ai 影片生成 免費」「免費 ai 影片」在「AI 免費」建議裡 | 搜尋「Google Vids 免費 普通帳號」中文最高只有知川 Kinta 1,196（0ROKOt71q3o）、DMP 1,320；英文 Paul J Lipsky 139K | **S88lbAsLz2E 251 次＝頻道最高，排第 2**。這是全頻道唯一「搜尋位置」已經拿到的題目 |
| 9 | 臉書、IG 帳號防盜 | 建議：「ig 帳號被盜」「fb 雙重驗證」「passkey 是什麼／教學／iphone／google」 | 科技狗 14.5K、小董（救帳號）85K、Nic（破解驗證碼）197K；都是真人，但沒有一支專講 passkey＋2FA 怎麼開 | _v1vc2s3_MU 32 次。標題寫「通行金鑰」，而「通行金鑰」的建議是「隨身碟無法讀取」——台灣人打的是 **passkey** |
| 17 | ChatGPT 開始有廣告，免費版／Go／Plus 該不該升級 | 「ChatGPT Go」建議第 2 個就是 **「chatgpt go vs plus」**；「ChatGPT Plus」→ plus vs free、plus vs pro；「chatgpt 廣告 關閉」→「chatgpt要付費嗎」 | 蘋果爹「免費版 vs Plus 怎麼選」142K、科技兔「Go/Plus/Pro 怎麼選」20.5K、知識流氓「Go 在台灣上線」4.3K；同一則廣告新聞：黃敬峰 311（10-02）、Whoops 199（09-27） | eSg90eCfqOI 71 次。角度「該不該升級」是對的，但標題把「廣告」放最前面，而「廣告」的建議只回自己一筆 |
| 2 | Gemini 推出 skills、Gems 要退場 | 建議「gemini gems 教學」「gemini gems opal」「gemini gems vs gpts」；中文 Gems 教學有 183K（職能小真）、76K（T客邦）、61K（七七）觀眾等著要搬家 | 「Gems 退場怎麼搬」中文搜尋前 12 名 **沒有任何一支**；英文 Futurepedia 55K、Skill Leap 71K | xSrFAMk_udE 今天上架 7 次。標題已含「Gems」「skills」兩個建議詞，是 18 支裡標題關鍵字最對的一支 |

### B 組：有需求，但角度太偏或太晚（7 支）

| # | 影片 | 需求證據 | 誰占住、差多少 | 角度差在哪 |
|---|---|---|---|---|
| 16 | Google AI 學生方案台灣符不符合 | 「Gemini 免費」建議：免費一年、pro 免費一年、免費1年；「google ai pro」→ 免費、教學、學生、家庭 | 零度解说 218K、Seven 168K、Porter 90K（簡中「白嫖」教學）；台灣：數位時代 1.4K（**08/20 當天**）、爆點議題 9.8K、點哥 952 | 公告 08-20，Mokaair 09-27 才上（晚 38 天）。「真的符合資格嗎」是台灣獨有的好角度，但繁中競爭者少，應該做成常青「怎麼申請＋到期怎麼不被扣款」 |
| 10 | Claude Opus 5.5 便宜了？三個數字 | 建議「claude opus 5.5」排第 1 | 可波「ChatGPT 該換 Claude 嗎？」21K（09-26）；**同角度**：Whoops「省 40% 帳單真相」232（09-25）、AI 好友「便宜 50% 就一定比較省？」209（09-30）、黃敬峰「別看跑分」136（09-29） | Mokaair 142（09-30）。拆數字角度 4 個頻道擠在 100–250 次；決策角度一支 21K |
| 14 | GPT-6 出了，對話裡卻沒有 | 建議「gpt-6」有（但混 gta 6） | 可波「GPT-6 Astra 懶人包…台灣開通」260K（09-07）、泛科 97K；Sol/Luna：Whoops「半價真的省？」486（09-25） | Mokaair 39（09-28）。「找不到是正常的」是好的使用者切入，但晚了、也沒用「台灣能不能用」這種建議詞 |
| 3 | Gemini 4 Argon 找不到 | 建議「gemini 4 argon」第 2 | 英文 WorldofAI 264K、Caleb 219K；中文 商業本質 17.5K、為什麼叫QQ 4K、數位時代「實際效果被質疑」2.9K | 今天上架 1 次，還看不出來；但「為什麼你的 Gemini 裡找不到」比競品都貼近使用者，值得在 48 小時內推 |
| 4 | 大型語言模型是什麼｜AI 名詞十分鐘 | 建議「llm 是什麼」「大型語言模型」「李宏毅 大型語言模型」是常青需求 | 今天比昨天厲害「什麼是大型語言模型?」32K、鬍子Jack 11.6K、泛科「20 件 AI 新手必知」28K、貝背包 566K、jasonmel 593K | 21 次。常青但競爭重；「會接話≠查到資料」的角度獨特，但標題沒有「LLM 是什麼」這個原詞（只有「大型語言模型是什麼」），且「AI 名詞」這個系列名在建議裡不存在（→ ai發音／ai用法） |
| 5 | 網域第一年便宜，第五年呢 | 建議「網域申請教學」「cloudflare 網域」「買網域」→ 購物網站架設 | 犬哥 NameCheap 7.6K、麥克斯「買網域去哪買」3.3K、零度「免費域名」180K | 2 次。「註冊價 vs 續約價」沒人搜，但「去哪買、怎麼申請」有；AI 代理代買那段更是沒人搜 |
| 15 | OpenAI Academy 要錢嗎 | 建議「openai academy」有，但後綴是 india／hindi／certificate；台灣打的是「ai 證照」「google ai 證照」「ai 課程推薦」 | 林易璁「OpenAI 官方證書 4 小時入手」1.2K、優米「10 門免費 AI 課程」550 | 11 次。角度「徽章不算證照」是在潑冷水，而搜尋者想要的是「哪裡拿證書」 |

### C 組：幾乎沒人搜（7 支）

| # | 影片 | 證據 | Mokaair |
|---|---|---|---|
| 1 | Cloudflare Auto Router 省錢數字誰測的 | 搜尋只有 TechJonesAi 11 次與 Mokaair；建議「AI 省錢」→ ai生活／ai 收入 | 2 次（排第 3） |
| 6 | Grok 4.7 上 Bedrock | 前 12 名全英文；建議「Grok 4.7」只回自己，「Amazon Bedrock」全是英文開發者詞 | 3 次 |
| 7 | Cloudflare 請 AI 打自家 WAF | 整個搜尋只回 **2 筆**；建議「WAF」→ waffle、waferlock | 34 次（排第 1） |
| 11 | Gemini Connected Apps | 建議「Gemini 連結」→ gemini 直播；英文 Thoughts Brewing 4K | 13 次（排第 1） |
| 12 | OpenAI 停供 Cursor | 建議「cursor 斷供」→ cursor python；前 12 名除 Mokaair 全簡中（最高 3.8K），台灣 David Tseng 12 次 | 27 次（排第 1） |
| 13 | 資安新聞的百分比 | 前 12 名第 2 起全是台股、RBI、流感；建議「資安新聞」→ 資訊安全工程師 | 6 次（排第 1） |
| 18 | AI 代理人越界三起事件 | 今天比昨天厲害（5.7 萬訂閱）做同事件 612 次（09-07）、AIDive 92；建議「ai agent」→ 是什麼／教學／n8n，沒有事件詞 | 36 次 |

排第 1 名仍只有 6–34 次，證明不是排名問題，是題目本身沒有台灣觀眾在找。

## 2. 最可能站得住的 3 個利基

### 利基 1：「AI 月費算盤」——方案、額度、台幣價、到期扣款
- 需求：「chatgpt go vs plus」「plus vs free」「chatgpt 方案／收費／要付費嗎」「gemini 免費一年」「google ai pro 學生／家庭／方案」「claude 額度」（建議）；泛科學院「一個月 600 塊訂閱哪家 AI 最香」**399K**、「AI 訂閱好貴只能選一個」146K、孔老師 123K、蘋果爹 143K、AgentCrew「Claude 額度一下就爆」47K、贊贊小屋「先看懂 Usage 再升級 Max」2.8K（小頻道也有）。
- Mokaair 的優勢：#17、#10、#16、#14、#6、#1 的素材本來就是這條線，而且「分清三個數字」「先算一年帳」在這裡是加分，不是潑冷水。
- 前 5 支：
  1. ChatGPT Go vs Plus 怎麼選？台灣台幣價一年差多少（2026 版）
  2. Google AI Pro 學生免費一年：台灣申請四個資格、到期怎麼不被自動扣款
  3. Claude Pro 額度一下就用完？用量上限怎麼算、Opus／Sonnet 什麼時候切
  4. ChatGPT、Gemini、Claude 免費版 2026 能做什麼、什麼時候才該付錢
  5. AI API 帳單怎麼算：輸入、輸出、快取三個價格，一張表看懂（用 Opus 5.5／GPT-6 Sol 當例子）

### 利基 2：「帳號守門員」——一般人與長輩的 AI 時代帳號／權限安全
- 需求：「ig 帳號被盜」「fb 雙重驗證」「passkey 是什麼／教學／iphone／google」「ai 詐騙 視訊／聲音／變臉」（建議）；科技狗 14.5K、小董 85K、Nic 197K、可波「3 大 AI 隱私設定一次學會」7.5K。「passkey 教學」在中文搜尋裡沒有專門的一支。
- Mokaair 的優勢：#9、#11、#18 已經是這條線；「連結之前先看你給了什麼權限」「允許清單／Sandbox／金鑰」是這條線裡少有的扎實內容，只是標題用錯詞、掛在沒人搜的新聞上。
- 前 5 支：
  1. passkey 是什麼？FB、IG、Google 帳號被盜前先開這兩個設定（手機畫面逐步）
  2. ChatGPT、Gemini、Claude 隱私設定：對話會不會拿去訓練、怎麼關
  3. 讓 AI 連你的 Gmail、雲端、Adobe 之前：授權畫面要看的三件事、怎麼斷
  4. 幫爸媽手機設防詐：驗證碼永遠不給人、三個設定一次開
  5. 給 AI 代理人權限之前：允許清單、Sandbox、API 金鑰三道防線（給用 Claude Code／Codex 的人）

### 利基 3：「Google 免費 AI 工具箱」——Vids、Gems→skills、NotebookLM、AI Studio
- 需求：Google 2025 台灣年度「快速竄升 AI 工具」榜是 Gemini、NotebookLM、Nano Banana、Sora、Manus、Google AI Studio、Cursor（techbang 2025-12-07）；建議「gemini gems 教學」「notebooklm gemini 教學」「google ai pro 教學」「gemini 免費版」。
- Mokaair 的優勢：Google Vids 是全頻道唯一已拿到搜尋位置的題目（251 次、第 2 名、中文競品最高 1.3K）；#2 Gems 搬家中文無人做；#16 學生方案是這條線的入口。
- 前 5 支：
  1. Google Vids 免費版實作：額度怎麼不浪費、浮水印、中文提示（接 #8，前 12 名競品的賣點就是這三個）
  2. Gems 要退場：把你的 Gem 搬到 Gemini skills 的完整步驟（#2 的常青版）
  3. Gemini 免費版 10/9 起縮水：Flash-Lite／Flash／Pro 差在哪、現在該做的三件事（3cTim 19K、數碼講呢D 已做，台灣繁中缺一支完整版）
  4. NotebookLM 免費額度與學生方案怎麼搭：讀論文、做筆記、查引用
  5. Google AI Studio 免費能做什麼：跟 Gemini App 差在哪、額度在哪裡看

三條線共通的證據：建議詞裡「ai 工具推薦／教學／比較」「ai 免費課程／工具」都在，而「ai 新聞」的建議是「ai 新聞主播」「新聞女王」——台灣人在 YouTube 上搜的是「工具怎麼用、要不要花錢」，不是「AI 新聞」。

## 3. 新聞題改寫成常青題（5 例）

| 原標題 | 改法 | 依據 |
|---|---|---|
| ChatGPT 開始有廣告了，免費版、Go、Plus 到底該不該升級？ | **ChatGPT Go vs Plus 怎麼選？台灣台幣價一年差多少（2026）** ——廣告變成片中一個章節「免費版現在有廣告，但設定裡可以關」 | 建議「chatgpt go vs plus」「plus vs free」；蘋果爹 143K、科技兔 20.5K |
| Google AI 學生方案免費一年，台灣大學生真的符合資格嗎？四道關卡全解析 | **Google AI Pro 學生免費一年：台灣怎麼申請、四個資格、到期怎麼不被扣款** | 建議「gemini 免費一年」「google ai pro 學生」；台灣繁中競品只有 952–9.8K |
| 臉書、IG 帳號防盜：雙重驗證和通行金鑰怎麼開｜Meta 防詐騙活動在推什麼 | **passkey 是什麼？FB、IG 帳號被盜前先開這兩個設定（手機示範）** ——Meta 活動整段拿掉 | 建議「passkey 是什麼／教學」「ig 帳號被盜」「fb 雙重驗證」；「通行金鑰」建議無關 |
| Claude Opus 5.5 便宜了？其實是三個不同的數字 | **Claude 額度一下就用完？Pro／Max 用量上限怎麼算、Opus 跟 Sonnet 什麼時候切** ——「三個數字」變成片中的方法 | AgentCrew 47K、贊贊小屋 2.8K；同角度拆數字 4 個頻道都在 100–250 |
| 掛了防火牆，外掛就不用更新？Cloudflare 請 AI 打自家 WAF：1,107 次嘗試、49 筆發現怎麼讀 | **WordPress 外掛要不要更新？掛了 Cloudflare 還是要，三步把待更新清到零** ——Cloudflare 實驗當一個論據 | 建議「wordpress 外掛」存在、「WAF」→ waffle；原搜尋只有 2 筆結果 |

同一個原則也適用 #5（→「買網域去哪買？Cloudflare／Namecheap／GoDaddy 註冊價 vs 續約價，五年總帳」）、#4（→「LLM 是什麼？大型語言模型 10 分鐘看懂」）、#12（→「Cursor 裡的 OpenAI 模型怎麼換、API key 怎麼接」，建議「cursor openai api key」）。

## 4. 對產線的具體落差（摘要，細項見 mokaair_gaps）
1. 選題沒有「有沒有人搜」的自動關卡——7 支題目連一個建議詞都沒有。
2. 標題不用使用者打的原詞（passkey、go vs plus、google ai pro、買網域）。
3. 新聞題晚 4 天到 5 週，前 12 名早被占。
4. 「拆數字」角度要留在片中當方法，標題改用決策句（該不該換、怎麼選、台灣能不能用、一年差多少）。
5. 沒有系列與播放清單；同量級頻道全部有固定系列格式。
6. 唯一贏的題目（Google Vids）沒有延伸。
7. 請站主確認每支影片的預設標題語言是中文（台灣）——yt-dlp 抓回的全是英文在地化標題，無法從外部判斷哪個是預設。

## 來源
- YouTube 搜尋與頻道列表原始 JSON：`<分析暫存區>/work/seo/results/`、`channels/`
- YouTube 搜尋建議原始 JSON：`<分析暫存區>/work/seo/sugg/`
- Google 台灣 2025 年度搜尋排行：https://www.techbang.com/posts/126799-google-taiwan-search-2025-gemini-notebooklm-hot-topics 、https://technews.tw/?p=1478485
- Google 學生方案公告日（2026-08-20）：https://technews.tw/2026/08/20/google-offers-free-student-plans-for-one-year-and-launches-new-study-tools/
- 頻道資料包：`<分析暫存區>/data/channel_pack.md`