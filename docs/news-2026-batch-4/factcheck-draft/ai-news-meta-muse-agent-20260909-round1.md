# ai-news-meta-muse-agent-20260909 第一輪查核報告

- 查核代理：獨立第一輪查核代理（Claude Opus 5），未參與撰稿
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/ai-news-meta-muse-agent-20260909.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-meta-muse-agent-20260909.json`
- 工作樹：`C:\Users\x8120\mokaair\.claude\worktrees\news-4-4`（全程沒有執行任何 git 指令）
- 主張數 131：CONFIRMED 117、CHANGED 11、NOT FOUND（已改寫）3；
  另有 2 條判定正確但留了排版／譯詞的註記（撇號、surrogate token），見第 5 節
- 這 14 條被動到的主張合併成 **10 處編輯**（同一處改動涵蓋多條，對照第 3 節）：
  7 處是事實／限定詞／否定句範圍，3 處是讀者優先（歸因密度與查證紀律）
- 結論：**需要第二輪**（第一輪規格本來就要求）

## 1. 重抓結果

四條 `sources[]` 全部在 2026-09-23 台北 09:03 自行重抓，
`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 2 秒。
任何請求的 UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料，沒有填寫或送出任何表單，
沒有註冊 muse.ai，也沒有嘗試任何繞過地區限制的做法。

| # | 來源 | HTTP | bytes（今天／研究紀錄） | 抽出正文字元（今天／研究紀錄） | 是否為正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | about.fb.com Newsroom 發表稿 | 200 | 646,535／646,535 | 12,018／12,018 | 是，Takeaways 到 Looking Ahead 全文 |
| 2 | research.meta.ai 安全長文 | 200 | 189,320／189,321 | 24,938／24,938 | 是，讀到結尾註腳與頁尾模型清單 |
| 3 | research.meta.ai Muse Spark 1.3 | 200 | 189,791／189,877 | 10,558／10,558 | 是，讀到 Availability 與 Looking Forward |
| 4 | introducing.muse.ai 產品設計說明 | 200 | 44,788／44,788 | 9,029／9,029 | 是，讀到 Ready to try Muse? |

抽字配方與研究紀錄相同（移除 `<!-- -->`、`script`／`style`／`noscript`，`html.unescape`，
NBSP 與 U+2011 正規化，去零寬字元）。四頁的抽出字元數與研究紀錄**逐一相同**，
bytes 的個位數差異出在頁尾隨建置變動的資產清單，正文沒有差異。
研究紀錄列的每一條 `verbatim_quote` 都用程式對抽出的正文做連續子字串比對，**全部命中**；
研究紀錄 `sourcing_notes` 第 4 條警告的兩條（bug bounty 與 1Password 那句在原始 HTML 被行內標籤切開）
確認只在抽出的正文中連續，直接 grep HTML 會誤判。

事件日獨立驗證：`muse.html` 裡 `"datePublished":"2026-09-08T19:00:51+00:00"` 出現 2 次、
`article:published_time content="2026-09-08T19:00:51+00:00"` 1 次、`dateModified` 出現 **0** 次；
頁面標題下印的是「September 8, 2026 September 8, 2026」（發布日與更新日相同），
可證這一頁到查核當天為止沒有被改寫。換算台北為 2026-09-09T03:00:51+08:00，
與 slug 尾碼、`news_date`、DELTA-4-4 第 3 條表列一致。

價格獨立驗證：四頁全文搜尋 `$`、`USD`、`per month`、`/month`、`pricing`，
**只有安全長文的 bug bounty 兩筆金額**，其餘三頁 0 筆，四頁都沒有任何與 Muse 訂閱有關的金額。

## 2. 主張表

`✓` = CONFIRMED，`△` = CHANGED，`✗` = NOT FOUND（已改寫），`—` = OUT OF SCOPE（語氣／排版）。

### A. 中介資料與日期（1–10）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 1 | slug 尾碼 20260909 = `news_date` 2026-09-09 = DELTA-4-4 第 3 條 | ✓ | 內容包與指派表 |
| 2 | 官方頁 `datePublished` 2026-09-08T19:00:51+00:00，2 筆、無 `dateModified` | ✓ | 自行 grep 今天的 HTML |
| 3 | og `article:published_time` 同值 | ✓ | 同上 |
| 4 | 換算台北 2026-09-09T03:00:51+08:00 | ✓ | 換算 |
| 5 | 頁面印「September 8, 2026 September 8, 2026」＝未被改寫 | ✓ | 今天的抽出正文第 234 行 |
| 6 | 第一段同時寫出 9 月 9 日（台北）與 9 月 8 日（美國） | △ | 見改動 1（兩個日期都保留） |
| 7 | `display_order` 178 | ✓ | `check_article.py` RELATED |
| 8 | `kind: life`、`topics` 以 ai 起首含 software／ai-news、`locales` 只有 zh-TW | ✓ | 內容包 |
| 9 | `checked_on` 2026-09-23：研究紀錄、四條 source、第二段、表格 caption 四處一致 | ✓ | 內容包與研究紀錄 |
| 10 | 研究紀錄 `title` 與內容包 zh-TW `title` 逐字相同 | ✓ | 程式比對 |

### B. 標題與描述（11–18）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 11 | Meta 推出個人 AI 代理 Muse | ✓ | 「Today, Meta is introducing Muse, a secure, private personal AI agent…」 |
| 12 | 只在美國上線 | ✓ | 「Muse is rolling out in the US…」 |
| 13 | 連外都要 Sentinel 核可 | ✓ | 「Nothing Muse does reaches the internet unless the Sentinel approves it」 |
| 14 | 標題 45 字 ≤ 60；標題無篇數 | ✓ | 程式量測 |
| 15 | description：2026 年 9 月 9 日（台北時間）Meta 發表 Muse | ✓ | 同 2–4 |
| 16 | description：能自己瀏覽網頁、寄送電子郵件與結帳 | ✓ | 「It can open a browser, fill out forms…」「sending an email or booking travel」 |
| 17 | description：官方說對外連線都要先經過另一個 Sentinel 代理核可 | ✓ | 同 13 |
| 18 | description 129 字（120–200）、句尾「（2026 年 9 月查證）」、無查證流水帳、無篇數 | ✓ | 程式量測 |

### C. summary 四點（19–26）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 19 | 2026 年 9 月 9 日（台北時間）Meta 發表個人 AI 代理 Muse | ✓ | 同 2–4 |
| 20 | 會自己瀏覽網頁、填表單、寄信與結帳 | ✓ | Newsroom「open a browser, fill out forms」＋設計頁「fill out forms, and complete transactions」 |
| 21 | 寄信、付款這類動作會先問過使用者 | ✓ | 「Muse checks with the person before sensitive actions like sending an email or making a purchase.」 |
| 22 | Muse Spark 是模型、Muse 是產品 | ✓ | Spark 1.3 頁「available today in Muse Code and in Meta Model API」對比 Newsroom 的消費者代理 |
| 23 | 9 月 2 日發布的 1.3 版驅動 Muse | ✓ | Spark 1.3 頁「September 2, 2026」；安全長文「Muse Spark 1.3 is close to SOTA on this capability.」「Driving the web browser … is something the Muse Spark 1.3 model is particularly good at.」 |
| 24 | 每個人的 Muse 跑在專屬虛擬機，連網前要先經過 Sentinel 核可（已歸因） | ✓ | 同 13、「a dedicated, virtual machine (VM) that houses both the agent and a person's data」 |
| 25 | 官方自己寫 Muse 不是攻不破、提示詞注入在業界仍未解 | ✓ | 「Muse isn't immune to attack. Prompt injection remains an open problem in the industry」 |
| 26 | 只在美國上線、沒有公布任何價格 | ✓ | 同 12；四頁金額搜尋 |
| — | summary 四點沒有任何選錄篇數，且每個數字（1.3、9 月 2 日、2026）都出現在正文 | ✓ | 程式比對 |

### D. 正文（27–102）

**第一段（27–34）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 27 | 事件日兩個日期並陳 | △ | 改動 1：刪掉「Meta 官方頁面印的是」這個歸因詞，兩個日期原樣保留 |
| 28 | Meta 在 Newsroom 發表 Muse | ✓ | 來源 1 |
| 29 | 能自己瀏覽網頁、寄信與結帳 | ✓ | 同 16 |
| 30 | 逐字引「Muse is rolling out in the US」 | ✓ | 連續子字串命中 |
| 31 | 入口 iOS、Android、muse.ai | ✓ | JSON-LD articleBody 的完整句 |
| 32 | AI 眼鏡是 coming soon | ✓ | 同上 |
| 33 | 台灣讀者現階段還用不到 | ✓ | 直接來自「rolling out in the US」；研究紀錄 editorial_brief 也是這個定調 |
| 34 | 「四份官方頁面也都沒有提到台灣、亞洲或其他任何地區」 | △ | 改動 1／2：頁面明白寫了美國，「其他任何地區」讀起來會把美國也包進去；改成「沒有提到台灣、亞洲或美國以外的任何國家」並移到第二段 |

**第二段（35–37）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 35 | 「這一則在發布當時沒有排進本站的頭條批次，這一篇補上。」 | ✓ | DELTA-4-4 第 2 條唯一允許的句子，逐字相符 |
| 36 | 查核日 2026 年 9 月 23 日 | ✓ | 與研究紀錄、四條 source、表格 caption 一致 |
| 37 | 「讀的是……共四份官方文件；本站沒有註冊、沒有實測」 | △ | 改動 2：DELTA-4-7 第 14 條——查證紀律不是內容；callout 已經寫了「本站沒有實測或稽核」 |

**「Muse 不是 Muse Spark」一節（38–47）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 38 | Muse Spark 是模型、Muse 是建立在模型之上的產品 | ✓ | 同 22 |
| 39 | Meta 表示 Muse 由 Muse Spark 驅動 | ✓ | 「powered by Muse Spark, Meta's most capable model to date」 |
| 40 | 驅動的版本是 9 月 2 日另外發表的 1.3 版，是獨立的模型更新 | ✓ | 同 23；Spark 1.3 頁只講 Muse Code／Meta Model API，不是 Muse 產品發表 |
| 41 | inline `article` 指向 `ai-news-meta-muse-spark-20260408` | ✓ | 目標內容包存在，`news_date` 2026-04-08 |
| 42 | Muse 不只回答問題，會實際把工作做掉 | ✓ | 「It doesn't just answer questions, it actually does the work.」 |
| 43 | 包括寄電子郵件、訂行程，也包括比較大的目標 | ✓ | 「It can handle tasks, like sending an email or booking travel, and it can take on big audacious goals.」 |
| 44 | 耗時較久的工作會在關掉 App 後繼續做，有變化或需要核可時回來找人 | ✓ | 「For tasks that take more time, Muse keeps working after people close the app…」 |
| 45 | 標題自稱 The World's First Personal AI Agent Built for Everyone（歸因為 Meta 自稱） | ✓ | 頁面標題 |
| 46 | 也寫 Muse 為全世界數十億人打造、沒有學習門檻 | ✓ | 「Unlike other agents, Muse was built to work for billions of people worldwide, so there's no learning curve.」 |
| 47 | 「這是官方自己的用詞，這一篇不會照抄成本站的事實敘述」 | △ | 改動 3：編務自述，「自稱」已足以歸因 |

**「Muse 能做什麼」一節（48–60）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 48 | 可在 Muse App 或直接在 WhatsApp 裡像傳訊息一樣對話 | ✓ | 「…in the Muse app or directly in WhatsApp.」（未寫成 Muse 會讀 WhatsApp 訊息，符合 must_not_write） |
| 49 | 能處理寄信、訂行程，也能接手比較大的目標 | ✓ | 同 43 |
| 50 | 結帳可用 Stripe 打造的 Link 產生一次性卡號 | ✓ | 「Muse can checkout with Link built by Stripe」「Link's wallet for agents generates a one-time-use card」 |
| 51 | 「不會把使用者真正的信用卡號交給店家」 | △ | 改動 4：這是 Meta 對自家機制的描述，且原文是「送到商家網站的是那組一次性卡號」；已歸因並照原文改寫 |
| 52 | Shop Pay 是 coming soon | ✓ | 「Shop Pay is coming soon as another way to pay」 |
| 53 | 「1Password 的登入代填也是 coming soon」 | ✗ | 改動 5：官方只寫「1Password support so Muse can use logins a person already has」，沒有說代填表單 |
| 54 | 連接器官方只舉例、沒有完整清單 | ✓ | 安全長文「We've built an initial set of connectors … to other Meta apps like Instagram and Facebook」，日曆出現在讀寫權限與 worker 的例子裡 |
| 55 | 使用者自己選 Muse 連哪些 App、給多少存取權 | ✓ | 「People choose which apps Muse connects to and exactly how much access it gets.」 |
| 56 | 電子郵件可以只讀信，也可以代為寄信 | ✓ | 「whether it reads their mail or can also send on their behalf」 |
| 57 | 預設放行一般網頁瀏覽，遇到難以復原的動作才停下來問 | ✓ | 設計頁「So the default allows for standard browsing of the web and stops for anything hard to undo.」 |
| 58 | 這個預設使用者可以調鬆調緊 | ✓ | 「And we have controls built in for you to change those defaults to be more or less cautious.」 |
| 59 | 寄信、付款前先問過使用者 | ✓ | 同 21 |
| 60 | 提供完整稽核紀錄，列出做過什麼、打算做什麼 | ✓ | 「Muse shows people a complete audit trail of everything it has done and plans to do.」 |

**表格（61–68）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 61 | 自動瀏覽器操作／已上線／可搜尋、瀏覽網站、填表單、完成訂位與購買 | ✓ | 設計頁「search, navigate sites, fill out forms, and complete transactions, like booking and purchasing」 |
| 62 | 結帳付款／已上線／用 Stripe 打造的 Link 產生一次性卡號 | ✓ | 同 50 |
| 63 | Shop Pay／尚未上線／coming soon | ✓ | 同 52 |
| 64 | 1Password 登入代填／尚未上線／coming soon | ✗ | 改動 5：欄名改「1Password 登入支援」 |
| 65 | AI 眼鏡入口／尚未上線／coming soon | ✓ | 「coming soon to AI glasses」 |
| 66 | 第三欄標「官方用字」 | △ | 改動 6：五格裡只有三格是英文原字，其餘是中文轉述，改標「官方說法」 |
| 67 | caption 只寫「整理自 Newsroom 發表稿與安全長文」 | △ | 改動 6：第一列的用字出自產品設計說明，caption 補上 |
| 68 | caption 帶查核日 2026 年 9 月 23 日、長度 ≤ 200 | ✓ | 程式量測 |

**「Meta 怎麼管住它」一節（69–80）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 69 | 專屬雲端虛擬機，官方稱為 Muse Secure VM | ✓ | 「Muse runs on Muse Secure VM」「a dedicated, virtual machine (VM)」 |
| 70 | 代理本身與使用者資料都在同一台機器裡 | ✓ | 「houses both the agent and a person's data」 |
| 71 | 不會被別人的代理碰到 | ✓ | 「contained so no one else's agent can reach it」 |
| 72 | 連接服務的資料與憑證也存在那一台 | ✓ | 「where the data and credentials for any service a person connects are securely stored」 |
| 73 | Sentinel 在同一台機器上、在系統層與 Muse 隔開 | ✓ | 「A separate Sentinel agent runs on that same machine, kept apart from Muse at the system level.」 |
| 74 | 引句「Muse 做的任何事，沒有經過 Sentinel 核可就無法連上網際網路」 | ✓ | 同 13，翻譯忠實 |
| 75 | 「必要時它會徵求使用者同意」（原文主詞同樣模糊，譯文用「它」保留） | ✓ | 「and it asks the person for permission when needed」 |
| 76 | Muse 只能提出動作，連外與動第三方服務的決定權在 Sentinel | ✓ | 安全長文「It is the sole permission authority … Muse proposes actions, but only Sentinel can grant permission to perform action.」 |
| 77 | 密碼與付款方式進入 Muse 看不到的安全儲存區 | ✓ | 「Muse has no visibility into people's passwords or payment methods. Any credentials a person shares go into secure storage…」 |
| 78 | 連使用者自己在瀏覽器輸入的密碼也看不到 | ✓ | 「including passwords a person types into the browser themselves」 |
| 79 | 代理端拿到的是替身憑證，真正的憑證由 Sentinel 在網路邊界換上 | ✓ | 「only ever sees a "surrogate" token … Sentinel will replace any surrogate tokens with the real credential … at the network boundary」（譯「替身憑證」，原文是 surrogate token，語意不差，未改） |
| 80 | 圖解 caption 四句（專屬虛擬機／Muse 只能提出動作／Sentinel 決定連外／寄信付款再問一次） | ✓ | 同 69–76；與研究紀錄 `diagram.caption` 逐字相同 |

**「界線在哪裡」一節（81–96）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 81 | 「Muse isn't immune to attack」 | ✓ | 安全長文原句（頁面用 U+2019 撇號，內容包用半形，見未決事項） |
| 82 | 提示詞注入在整個業界仍是未解問題 | ✓ | 「Prompt injection remains an open problem in the industry」 |
| 83 | 「Bug 懸賞從發表當天起對所有人開放」 | △ | 改動 7：原文是 to anyone **to responsibly disclose issues**，限定詞補回 |
| 84 | 上限 300,000 美元 | ✓ | 「The program awards up to $300,000 for valid reports」 |
| 85 | 影響單一使用者的成功提示詞注入上限 130,000 美元 | ✓ | 「including up to $130,000 for successful prompt injection attempts that affect one user」 |
| 86 | 兩個數字都寫成上限、不是已付出的金額 | ✓ | 改動 7 只刪掉重覆的歸因詞，「上限」框架完整保留；全篇沒有把它寫成行情或已付金額 |
| 87 | 發表稿寫不會把對話或 VM 資料分享給 Meta 廣告系統 | ✓ | 「Muse doesn't share a person's conversations or the data in their VM with Meta's ad systems.」 |
| 88 | 安全長文同時寫 Muse 上網會被視為使用者自己的活動 | ✓ | 「When Muse browses the internet, it will appear as your activity」 |
| 89 | 因此請它買東西、訂餐廳仍可能間接影響看到的廣告；兩句同段 | ✓ | 「…that designer might use your visit to show you an ad on Instagram … may also indirectly influence the ads you see.」 |
| 90 | 對話與操作紀錄預設會用來訓練模型 | ✓ | 「these trajectories are sanitized … before being used in training」＋「We think this is a good default」 |
| 91 | 會先做去識別化處理再使用（已歸因） | ✓ | 同上 |
| 92 | 不想被訓練的人可在設定裡用一個開關關掉 | ✓ | 「If you do not want your data to be used in model training at all, you can opt-out via a simple switch in Muse settings.」 |
| 93 | 現在的架構只用作業政策限制 Meta 員工存取 | ✓ | 「It restricts access to your data by Meta personnel through operational policies.」 |
| 94 | 並不阻止 Meta 在支援、維安或營運需要時存取資料 | ✓ | 「It does not prevent Meta from accessing data when necessary to support, secure or operate the service.」 |
| 95 | Muse Confidential VM 官方寫今年稍晚推出，查核當天還沒上線 | ✓ | Newsroom「Later this year, Meta will introduce…」；安全長文「plan to deliver this capability later this year」、章節標題 Coming Soon |
| 96 | 還沒有任何稽核結果可以參考 | ✓ | 「we've begun making our design and the source code … available to external auditors … once launched, will have a continuous audit」——查核當天沒有可讀結果 |
| — | 90–96 原本擠在同一段、掛三個歸因詞 | △ | 改動 8：拆成兩段，每個限定詞保住自己的歸因 |

**「台灣讀者現在能怎麼追」一節（97–102）**

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 97 | 逐字引「Muse is rolling out in the US on iOS, Android, and muse.ai, and coming soon to AI glasses.」 | ✓ | 完整不帶多餘空白的版本在頁面 JSON-LD articleBody，今天自行比對命中 1 筆 |
| 98 | 「入口只有這幾個」 | △ | 改動 9：這是封閉清單斷言；被排除的 muse.ai 首頁另外提到 Mac 版，改寫成「發表稿列出的入口只有這幾個」 |
| 99 | 官方只表示大部分需求免費、想做更多有訂閱方案 | ✓ | 「It's free for most of what people need, with subscription plans for people who want to do more.」 |
| 100 | 整頁沒有印出任何金額、幣別或方案名稱 | ✓ | 今天對四頁搜尋金額，只有安全長文的 bug bounty 兩筆 |
| 101 | 「台灣讀者現階段也沒有管道可以申請或排隊等候」 | ✗ | 改動 9：研究紀錄 `unverified_or_excluded` 第 5 條明文排除這類操作結論；改成「四頁也都沒有寫美國以外的開放時程、等候名單或申請方式」 |
| 102 | 結尾的七問對照表（跑在哪裡、誰決定連外、看不看得到密碼、哪些動作先問、有沒有紀錄、會不會拿去訓練、廠商看不看得到） | ✓ | 七項逐一對回 69–96，沒有新增事實 |

### E. FAQ、callout、連結、來源（103–124）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 103 | FAQ1 Muse Spark 是驅動 Muse 的模型、4 月已介紹過 | ✓ | 同 22、39 |
| 104 | FAQ1 這次發表的是會動手的代理產品 | ✓ | 同 42 |
| 105 | FAQ2 原文 rolling out in the US，只在美國的 iOS、Android、muse.ai | ✓ | 同 97 |
| 106 | FAQ2 AI 眼鏡 coming soon | ✓ | 同 65 |
| 107 | FAQ2 四份官方頁面都沒有提到台灣、亞洲或其他地區，也沒有寫開放時程 | ✓ | 已用「四份官方頁面」界定範圍，與研究紀錄 `not_said` 第 2 條相符 |
| 108 | FAQ3 沒有公布任何價格、幣別或方案內容 | ✓ | 同 100 |
| 109 | FAQ4 憑證進入 Muse 看不到的安全儲存區、瀏覽器裡輸入的密碼也一樣 | ✓ | 同 77、78 |
| 110 | FAQ5 只用作業政策限制員工存取，不阻止 Meta 在支援、維安或營運需要時存取 | ✓ | 同 93、94 |
| 111 | FAQ5 Muse Confidential VM 今年稍晚推出、查核當天還沒上線 | ✓ | 同 95 |
| 112 | FAQ6 Meta 自己寫 Muse 不是攻不破、提示詞注入業界未解 | ✓ | 同 81、82 |
| 113 | FAQ6 沒有寫這套機制的失敗率 | ✓ | 四頁皆無，與 `not_said` 第 9 條相符 |
| 114 | FAQ6 沒有寫出錯時的責任歸屬 | ✓ | 同上 |
| 115 | callout：安全設計整理自 Newsroom 與安全長文 | ✓ | 兩頁都在 `sources[]` |
| 116 | callout：Secure VM、Sentinel、一次性卡號都是官方自己的說明，本站沒有實測或稽核 | ✓ | 事實正確；AI 篇只有這一個 callout，沒有投資免責 callout |
| 117 | callout：只在美國上線、沒有公布任何價格 | ✓ | 同 12、100 |
| 118 | callout：寫的是 2026 年 9 月 23 日查核當天的狀態 | ✓ | 與 `checked_on` 一致；沒有出現「本文」 |
| 119 | 結尾連結 1 文字＝索引 zh-TW title | ✓ | 逐字比對 `ai-news-2026-january-september-index.json` → 相同 |
| 120 | 結尾連結 2 文字＝`ai-news-meta-muse-spark-20260408` zh-TW title | ✓ | 逐字比對 → 相同（39 字），與 `check_article.py` RELATED 第 168 行相符 |
| 121–124 | 四條 `sources[]` 的 title、URL、`checked_on` | ✓ | 四條今天全部 200 且讀到正文，`checked_on` 皆 2026-09-23 |

### F. 研究紀錄的 hero_label 與 diagram（125–131）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 125 | `hero_label`「美國先上線的個人代理」 | △ | 改動 10：「先上線」暗示其他地區排在後面，四頁都沒有寫任何美國以外的時程 |
| 126 | `diagram.title`「Muse 想連外，要先過誰」 | ✓ | 同 76 |
| 127 | 節點 1 專屬虛擬機／代理與資料都在裡面 | ✓ | 同 69、70 |
| 128 | 節點 2 Muse／提出動作，不能自己連外 | ✓ | 同 76 |
| 129 | 節點 3 Sentinel／唯一核可者，可問使用者 | ✓ | 同 76、75 |
| 130 | 節點 4 使用者／寄信、付款前先問過 | ✓ | 同 21 |
| 131 | `diagram.caption` 與內容包 image caption 逐字相同 | ✓ | 程式比對 |

## 3. 改掉的 10 處

| # | 位置 | 原文 → 改成 | 來源原文 | 為什麼 |
| --- | --- | --- | --- | --- |
| 1 | 第一段 | 「（台北時間；Meta 官方頁面印的是美國時間 9 月 8 日）」→「（台北時間，美國時間 9 月 8 日）」 | 頁面印 September 8, 2026；`datePublished` 2026-09-08T19:00:51+00:00 | 兩個日期都留著，只刪掉多餘的歸因詞（開頭段至多一個歸因） |
| 2 | 第一段→第二段 | 「四份官方頁面也都沒有提到台灣、亞洲或其他任何地區」→ 移到第二段並改成「這四頁沒有提到台灣、亞洲或美國以外的任何國家」；第二段刪掉四份文件的清單與「本站沒有註冊、沒有實測」 | 頁面明寫 rolling out in the US | 頁面本來就寫了美國，「其他任何地區」讀起來連美國都否定掉；查證紀律不是正文內容（DELTA-4-7 第 14 條） |
| 3 | 第四段 | 刪「這是官方自己的用詞，這一篇不會照抄成本站的事實敘述」 | — | 「自稱」已完成歸因；剩下的是編務自述 |
| 4 | 「Muse 能做什麼」第一段 | 「不會把使用者真正的信用卡號交給店家」→「Meta 說送到商家網站的是一組一次性卡號，不是使用者平常那張信用卡」 | 「a single-use card number is issued, and that's what gets passed through to the merchant's website, rather than your regular credit card」 | 廠商對自家機制的說法要歸因；原文講的是「送過去的是什麼」 |
| 5 | 「Muse 能做什麼」第二段＋表格第 4 列 | 「1Password 的登入代填」→「讓 Muse 沿用使用者既有登入資訊的 1Password 支援」；表格欄名改「1Password 登入支援」 | 「1Password support so Muse can use logins a person already has」 | 官方沒有寫「代填」；coming soon 照原樣保留 |
| 6 | 表格 header 與 caption | 「官方用字」→「官方說法」；caption 補上「Muse 產品設計說明」 | 第一列的用字出自 introducing.muse.ai | 五格裡只有三格是英文原字；caption 漏列實際來源 |
| 7 | 「界線在哪裡」第一段 | 「對所有人開放……這兩個數字都是官方訂的上限」→「開放給任何循負責任揭露程序回報問題的人……這兩個數字都是上限」 | 「we're opening the Muse bug bounty program to anyone to responsibly disclose issues」 | 限定詞被刪；同段歸因詞從 3 個降到 2 個，上限框架不動 |
| 8 | 「界線在哪裡」訓練／存取段 | 拆成兩段，第一段講訓練預設與關閉開關（保留「官方寫的是會先做去識別化處理再使用」），第二段講 Meta 仍可存取與 Confidential VM 時程 | 同 90–96 | 原本一段掛三個歸因詞；拆段後每個限定詞都保住自己的歸因，一個都沒刪 |
| 9 | 「台灣讀者現在能怎麼追」第一段 | 「入口只有這幾個」→「發表稿列出的入口只有這幾個」；「台灣讀者現階段也沒有管道可以申請或排隊等候」→「四頁也都沒有寫美國以外的開放時程、等候名單或申請方式」 | 「Muse is rolling out in the US on iOS, Android, and muse.ai, and coming soon to AI glasses.」 | 封閉清單斷言與未經驗證的操作結論（研究紀錄 `unverified_or_excluded` 第 5 條明文排除） |
| 10 | 研究紀錄 `hero_label` | 「美國先上線的個人代理」→「只在美國上線的個人代理」 | 四頁都沒有寫美國以外的時程 | 「先」暗示其他地區已排定，屬 `must_not_write` 第 3 條 |

## 4. 查過而且正確的部分（重點）

- **跨日事件日**：`datePublished`／`article:published_time` 兩處各 1 筆、值相同、無 `dateModified`，
  頁面自印的發布日與更新日都是 September 8, 2026。台北 9 月 9 日與美國 9 月 8 日兩個日期都在第一段，
  且與 slug 尾碼、`news_date`、DELTA-4-4 第 3 條表列一致。
- **只在美國**：標題、description、第一段、表格、FAQ2、callout、summary 第 4 點七處都寫到，
  沒有任何一處寫或暗示台灣可用、可下載、可註冊、可排隊，也沒有任何「預計何時來台灣」的推測。
- **價格**：內容包全篇沒有任何價格、幣別、方案名稱或免費層用量上限；四頁重查後也確認一個都沒有。
  唯二的金額是 bug bounty 上限，位置與性質都正確。
- **Muse vs Muse Spark**：與已發布的 `ai-news-meta-muse-spark-20260408` 的實質重疊只有
  「Muse Spark 是模型」一句加那個 inline 連結，沒有重講該篇的社群使用情境、裝備辨識或私訊範圍；
  也沒有把 Muse 寫成 Muse Image／Muse Code／Muse Glimmer／Meta AI。
- **安全敘述**：Sentinel 是「連接器動作與所有對外流量的唯一許可權威」、Muse 只能提出動作、
  必要時再問使用者——三句都在來源裡，沒有被寫成「Sentinel 保證安全」或防火牆／防毒。
  「Muse isn't immune to attack」與「提示詞注入業界未解」有寫進正文與 FAQ，沒有被省略。
- **Meta 仍可存取**：「只用作業政策限制員工存取、不阻止 Meta 在支援／維安／營運需要時存取」有寫，
  而且和「Muse Confidential VM 是今年稍晚的計畫、查核當天尚未推出、還沒有稽核結果」放在一起，
  沒有寫成「Meta 看不到你的資料」。
- **訓練預設**：寫成預設會用、先去識別化、要自己去設定關掉；沒有寫「不會被拿去訓練」，
  也沒有寫成「Meta 直接拿原始對話訓練」。
- **廣告的兩句同段**：「不分享給廣告系統」與「上網會被視為你自己的活動」確實在同一段。
- **coming soon／up to 等限定詞**：Shop Pay、1Password、AI 眼鏡三處都寫 coming soon；
  bug bounty 兩個金額都寫成上限；Confidential VM 寫「今年稍晚」。
- **邊界**：沒有購買建議、沒有推薦式比價、沒有 benchmark 名稱或分數、沒有 `~20% fewer tool calls` 那組數字、
  沒有把訂閱方案連到 Meta One、沒有引用 muse.ai 首頁獨有的說法（Mac 版、該頁對 Link 保障的措辭）、
  沒有描述 Link 保障條款細節、沒有引用 ElevenLabs 朗讀字串、沒有把頁尾地區選單當上線地區證據、
  沒有寫攻擊手法或可操作的注入範例、沒有繞過地區限制的方法。
- **讀者優先**：全篇 0 個「本文」、0 個「最近／本週／日前／這幾天／近日」；
  description 129 字、句尾「（2026 年 9 月查證）」；標題、description、summary 都沒有選錄篇數。
  改後每一段的歸因詞都在上限內（開頭段 1 個，其餘每段 ≤ 2 個）。
- **兩個結尾連結**：文字逐字等於目標內容包現行的 zh-TW `title`（程式比對，非目視）。

## 5. 留給協調者的事

1. **英文引句的撇號**：正文寫 `Muse isn't immune to attack`（半形），頁面是 `isn’t`（U+2019）。
   repo 兩種寫法都有，多數內容包用半形，判為排版正規化，未改；若要統一請整批一起處理。
2. **「模型 vs 產品」出現在四個地方**（H2 標題、summary 第 2 點、內文一段兩句、FAQ 第 1 題）。
   與已發布那篇的實質重疊確實只有一句加連結，研究紀錄 `overlaps` 也允許「1.3 版在 9 月 2 日發布」這一點，
   所以沒有動結構；若「一句帶過」的裁示涵蓋 summary 與 FAQ，請指定要刪哪一處。
3. **「Meta 把安全架構寫得比一般發表稿詳細很多」**是本站對其他發表稿的比較，無來源可查，
   但也不是關於 Muse 的事實主張，判為語氣、未改。
4. **surrogate token 譯成「替身憑證」**（原文是 token，由 Sentinel 在網路邊界換成 real credential），
   語意不差，未改。
5. 圖檔尚未產生：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug，
   所以 `pack_cli lint` 的 `image_missing` 與 `raw_internal_url` 都還在（預期內）。

## 6. 自檢輸出（原樣）

```
check_article exit=0
OK ai-news-meta-muse-agent-20260909 zh-TW paragraphs 2531
```

```
pack_cli lint exit=1
ai-news-meta-muse-agent-20260909
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-meta-muse-agent-20260909/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-meta-muse-agent-20260909/diagram-1.svg
1 entries checked
```

退出碼寫在 `C:\Users\x8120\mokaair-work\news44\_tools\ai-news-meta-muse-agent-20260909-r1\check.exit`
與 `lint.exit`；輔助腳本（重抓、抽字、機械檢查、改稿、寫入 `factcheck`）在同一個目錄。

## 7. 結論

`needs_second_round`（第一輪一律要）。本輪改了 10 處：7 處是事實／限定詞／否定句範圍，
3 處是讀者優先的歸因密度與查證紀律。沒有動到骨幹論述，也沒有改任何一個日期、金額或機制名稱。
第二輪要特別回查第一輪**新寫進去**的句子：改動 2 的第二段、改動 4 的信用卡句、
改動 5 的 1Password 句與表格欄名、改動 7 的 bug bounty 句、改動 8 拆出來的兩段、改動 9 的兩處改寫。
