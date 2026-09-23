# 查核報告（第一輪）：`ai-news-openai-zero-data-retention-20260820`

- 垂直：AI（批次 4.4）、`display_order` 181、`news_date` 2026-08-20、只做 zh-TW
- 查核者：獨立查核代理（沒有參與撰稿），查核日 **2026-09-23**
- 內容包：`apps/api/app/guides/content/ai-news-openai-zero-data-retention-20260820.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-zero-data-retention-20260820.json`
- 結論：**主張 107 條／確認 93／改 14／查無 0**；改的 12 條是事實或限定詞，2 條是讀者優先規則。**需要第二輪。**

## 1. 今天重抓的來源

全部用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同主機間隔 ≥2 秒，
請求的 UA、標頭、查詢字串裡沒有任何人的姓名、email 或個人資料。抓取時間 2026-09-23 09:11–09:12（台北）。

| # | 來源 | 狀態 | bytes | 讀到正文？ |
| --- | --- | --- | --- | --- |
| 1 | `https://openai.com/index/offering-zero-data-retention-for-frontier-models/` | 200 | 423,817 | 是。抽出 8,344 字元正文，含 `OpenAI August 19, 2026`、`Company Safety`、副標、三個小節、2026-09-22 更新區塊、四家客戶標記、CSAM 註腳、Glean 推薦語。與研究紀錄記的 8,344 字元一致。 |
| 2 | `https://developers.openai.com/api/docs/guides/your-data` | 200 | 615,506 | 是。HTML 抽出 61,826 字元；另抓 `.md` 版 79,683 bytes（與研究紀錄記的 bytes 完全相同），含 27 列端點資格表、資料落地表、CSAM 一節、兩個收回條款。 |
| 3 | `https://developers.openai.com/api/docs/guides/private-safety-processing` | 200 | 460,634 | 是。HTML 抽出 29,850 字元；`.md` 版 24,849 bytes（與紀錄相同），含三項原則、兩個流程、雙層加密、AWS／Azure 設定、五條客戶責任。 |
| 4 | `https://openai.com/news/rss.xml` | 200 | 744,049 | 是。1,219 個 item；本篇那一筆逐字 `<pubDate>Wed, 19 Aug 2026 19:00:00 GMT</pubDate>`。 |

公告頁的 bytes 與研究紀錄記的 423,863 差 46（Next.js RSC payload／導覽外殼），正文與 09-22 更新區塊逐字比對都在，
不是頁面被改。`openai.com/index/*` 的 403 今天沒有發生。四條 `checked_on` 都是 2026-09-23，與研究紀錄、第二段、
表格 caption、圖說一致，**沒有因為我今天重查而改動**。

## 2. 主張表

「確認」＝今天在上表某一條來源的正文裡找到支撐句；「改」＝下一節有逐條說明。

### 標題、描述、hero

| # | 主張 | 判定 |
| --- | --- | --- |
| 1 | 標題：「把零資料保留**延伸到**前沿模型」 | **改**（C1） |
| 2 | 標題後半：內容留在客戶自己的雲端、只回傳訊號 | 確認（來源 3：客戶控制的儲存＋bounded safety signals） |
| 3 | 描述：2026-08-20（台北）／頁面印 8 月 19 日 | 確認（來源 4 pubDate、來源 1 頁首） |
| 4 | 描述：發布 PSP 預覽，作為 ZDR 的延伸 | 確認（`Previewing Private Safety Processing…remaining compatible with ZDR`、`extends those protections across related interactions`） |
| 5 | 描述：受審查的紀錄加密後留在客戶自己的雲端 | 確認 |
| 6 | 描述：OpenAI 只留索引 | 確認（`keeps an index with operational metadata and a storage reference, not a copy of the content`） |
| 7 | 描述：官方表示「人員」拿不到內容 | 確認（`without giving OpenAI personnel access to the underlying content`） |
| 8 | 描述：是 API 客戶的資料控制功能，不是 ChatGPT 的功能 | 確認 |
| 9 | 描述長度 193 字、句尾「（2026 年 9 月查證）」、沒有選件數字 | 確認（合規） |
| 10 | `hero_label`「私密安全處理預覽」 | 確認 |

`hero.alt` 依規格不查、不改。

### 第一段、第二段

| # | 主張 | 判定 |
| --- | --- | --- |
| 11 | 台北 2026-08-20 凌晨發布 | 確認（19:00Z＋8＝03:00，跨日） |
| 12 | 公告標題逐字 | 確認 |
| 13 | 預覽 PSP | 確認 |
| 14 | 頁面印的發布日期是 8 月 19 日 | 確認（歸因語改寫，見 C13） |
| 15 | 換算後在台北跨午夜到凌晨 3 點 | 確認 |
| 16 | 這是 API 客戶才會碰到的設定，台灣個人 ChatGPT 使用者不用做任何事 | 確認 |
| 17 | ZDR 承諾請求處理完就不留存提示與回覆 | 確認（逐字定義句） |
| 18 | 「有些嚴重風險**只有**把多次互動放在一起看才看得出來」 | **改**（C2，`may`） |
| 19 | 查核日 2026-09-23 | 確認 |
| 20 | 第二段列出讀了哪些來源 | **改**（C14，讀者優先） |
| 21 | 「發布當時沒有排進本站的頭條批次，這一篇補上」 | 確認（`must_not_write` 指定的唯一寫法，逐字） |
| 22 | 「本站沒有獨立驗證或測試**文中**提到的任何數字」 | **改**（C14） |

### Summary 五條

| # | 主張 | 判定 |
| --- | --- | --- |
| 23 | 日期＋PSP 預覽＋ZDR 的延伸機制 | 確認 |
| 24 | ZDR 是 API 客戶層級控制、要先經核准 | 確認（`subject to prior approval by OpenAI…for their API Organization or project`） |
| 25 | 資格逐端點列、不是逐模型 | 確認（27 列端點表；四份來源沒有任何按模型列的 ZDR 資格表） |
| 26 | 「公告**全篇**沒有提到 ChatGPT 的任何方案」 | **改**（C4） |
| 27 | 加密後寫進客戶自己的雲端（AWS S3 或 Azure Blob） | 確認 |
| 28 | OpenAI 只留索引與中繼資料 | 確認 |
| 29 | 在關閉人員存取的安全執行環境裡自動審查 | 確認（`hardware-attested safety runtime that disables human access`） |
| 30 | 只回傳範圍受限的安全訊號 | 確認（`Only bounded safety signals and operational metadata leave the PSP protected review in plaintext`） |
| 31 | 加密紀錄至少留 30 天 | 確認（`Retain encrypted records for at least 30 days`） |
| 32 | 「**金鑰授權**分兩層」 | **改**（C9） |
| 33 | 外層 EKM 是建議啟用、不是強制 | 確認（`We recommend enabling EKM for this additional control.`） |
| 34 | 撤銷授權擋住之後解密、不刪紀錄 | 確認 |
| 35 | 公告當時只與早期客戶測試 | 確認 |
| 36 | 09-22 追加更新：已開始分階段推給 API 客戶 | 確認（逐字更新區塊） |
| 37 | 官方沒有寫完成時程 | 確認（更新只寫 `with access expanding in phases`） |

### 第一節「為什麼要多一層私密安全處理」

| # | 主張 | 判定 |
| --- | --- | --- |
| 38 | 現有相容 ZDR 的安全系統是逐次互動分開評估 | 確認 |
| 39 | 任務越長越複雜、風險要合看才看得出來 | **改**（C2，`may`） |
| 40 | 近期前沿模型部署要求保留敏感內容，與組織的安全義務衝突 | 確認 |
| 41 | PSP 設計目的逐字英文引文＋中譯 | 確認（連續字串比對命中，一字不差） |
| 42 | 公告當時仍在與早期客戶測試 | 確認 |
| 43 | 計畫 9 月「推出」並發布技術白皮書 | **改**（C3，`start`） |
| 44 | 09-22 是後來追加的更新、不是發布日 | 確認 |

### 第二節「零資料保留現在管到什麼」

| # | 主張 | 判定 |
| --- | --- | --- |
| 45 | ZDR 定義逐字引文＋中譯 | 確認（連續字串比對命中） |
| 46 | 「公告**全篇**沒有出現 ChatGPT 方案」 | **改**（C4） |
| 47 | 申請管道只有聯絡業務團隊詢問資格 | 確認 |
| 48 | 文件沒有公開申請表或門檻數字 | 確認（今天全文查無） |
| 49 | 核准後才會看到 Settings → Organization → Data controls 的 Data Retention 分頁 | 確認 |
| 50 | 可在組織與專案層級分別設 ZDR 或 MAM | 確認 |
| 51 | 資格逐個 API 端點列出、不是逐個模型 | 確認 |
| 52 | 聊天、回應、嵌入、影像生成列為「符合 ZDR 資格」 | **改**（C7，漏了 `see below for limitations`） |
| 53 | 對話、討論串、向量庫、檔案、批次列為不符合 | 確認（`/v1/conversations`、`/v1/conversations/items`、`/v1/chatkit/threads`、`/v1/threads*`、`/v1/vector_stores`、`/v1/files`、`/v1/batches` 全部 No） |
| 54 | 濫用監控紀錄預設最多 30 天，除非法律要求或為保護服務與第三方 | 確認（`up to 30 days` 與兩個但書都在） |
| 55 | 與 PSP 的 30 天是兩回事 | 確認（一個是 OpenAI 的紀錄保存期，一個是客戶儲存的 TTL） |

### 表格（4 列 × 3 格＋caption）

| # | 主張 | 判定 |
| --- | --- | --- |
| 56 | MAM｜把客戶內容排除在濫用監控紀錄外｜要先經核准 | 確認（原文另有「圖片與檔案輸入在少數情況例外」，由第 4 列的 CSAM 承接） |
| 57 | ZDR｜同上＋部分端點 store 視為 false｜逐端點列 | 確認（`/v1/responses` 與 `/v1/chat/completions`） |
| 58 | ZDR＋PSP｜加密寫進客戶雲端、離線自動審查｜自備 S3／Blob、紀錄留 30 天 | 確認 |
| 59 | CSAM｜「**三種設定**都一樣」｜不受上述控制影響 | **改**（C10） |
| 60 | caption：整理自兩份文件、查核日 2026-09-23、50 字 | 確認 |

### 第三節「私密安全處理怎麼運作」與圖說

| # | 主張 | 判定 |
| --- | --- | --- |
| 61 | 開發者指南把做法整理成三項原則 | 確認 |
| 62 | 原則一：客戶內容存在客戶控制的儲存空間 | 確認 |
| 63 | 先經核准 → 接 S3／Blob 到專案 → 註冊並完成驗證 | 確認（`Ask your OpenAI contact to approve your organization.`） |
| 64 | Validated 只代表某次檢查通過、Refresh 不會重跑 | 確認（逐字） |
| 65 | 原則二：安全審查不得成為人員閱讀受保護內容的新管道 | 確認 |
| 66 | 加密內容「**只**在」硬體證明環境裡解密 | **改**（C8） |
| 67 | 離開審查流程的明文只有安全訊號與操作中繼資料 | 確認 |
| 68 | 被挑出來送審不代表已違規 | 確認（`A referral does not establish a policy violation.`） |
| 69 | 原則三：不得訓練、不得給 OpenAI 其他團隊或夥伴 | 確認 |
| 70 | OpenAI 留的是索引不是副本；加密與寫入非同步、不卡推論 | 確認 |
| 71 | 圖說第四環節「金鑰授權由客戶掌握」 | **改**（C11） |

### 第四節「客戶要付出的代價與界線」

| # | 主張 | 判定 |
| --- | --- | --- |
| 72 | 加密紀錄寫進客戶自己的區域雲端，TTL 30 天 | 確認（逐字） |
| 73 | 客戶端生命週期規則不能提早刪 | 確認（`Configure storage lifecycle rules so they do not delete PSP records earlier.`） |
| 74 | 「**金鑰授權**分兩層」 | **改**（C9） |
| 75 | 內層是 OpenAI 管理的 HPKE，把解密限制在授權的安全審查執行環境 | 確認（逐字） |
| 76 | 外層是客戶自管的 EKM，官方寫「建議」、非強制 | 確認 |
| 77 | 撤銷授權擋住之後解密，但不刪紀錄、不推翻已完成的處理 | 確認（逐字） |
| 78 | 兩個收回條款：Private Retention with PSP、Safety Retention | 確認（`(fka Eyes Off)`；公告頁完全沒提） |
| 79 | 保留取消特定客戶特定模型 ZDR 資格的權利、事先書面通知 | **改**（C12：補上兩個條款寫明的後果） |
| 80 | 「人員拿不到內容」是官方自己的敘述，四份來源沒有第三方稽核 | 確認（今天四份都查無稽核或認證） |

### 第五節「這件事跟一般讀者的關係」、`rich_paragraph`、FAQ、callout、結尾連結

| # | 主張 | 判定 |
| --- | --- | --- |
| 81 | 整件事都在 API 這一側 | 確認 |
| 82 | 「四份官方來源都沒有提到台灣、**亞洲或任何特定地區**」 | **改**（C6，與來源相反） |
| 83 | 官方沒寫收費、儲存成本由誰負擔；四份來源沒有價格 | 確認 |
| 84 | 09-22 更新只寫分階段開放、沒有完成時程 | 確認 |
| 85 | Glean、Databricks、Abridge、Microsoft 是 OpenAI 自己列的合作客戶 | 確認（頁面上逐字四家；未引述 Glean 的推薦語） |
| 86 | 端點資格表是活文件、兩份開發者頁面都沒印最後更新日 | 確認（今天兩份全文查無 `Last updated`／`Updated on`） |
| 87 | 以上是查核當天的狀態；要確認請查官方文件、聯絡業務團隊 | 確認 |
| 88 | `/v1/agents` 的 ZDR 欄位仍是 No，PSP 沒有改變這一格 | 確認（今天表上該列逐字 `No 30 days Until deleted No No`） |
| 89 | 第二個結尾連結文字＝目標內容包 zh-TW 標題 | 確認（程式逐字比對，相同） |
| 90 | FAQ1：「公告頁與資料控制文件**完全沒有出現** Plus／Business／Enterprise／Edu」 | **改**（C5） |
| 91 | FAQ2：限定在「人員」；仍有安全訊號與中繼資料；紀錄留 30 天 | 確認 |
| 92 | FAQ3：申請方式、沒公布門檻與時間、預覽且分階段 | 確認 |
| 93 | FAQ4：兩層加密、EKM 建議非強制 | 確認 |
| 94 | FAQ5：「四份官方來源都沒有提到台灣、亞洲或任何特定地區」 | **改**（C6） |
| 95 | callout：來源是公告頁與兩份開發者文件 | 確認 |
| 96 | callout：08-19 公告當時是預覽、只與早期客戶測試 | 確認 |
| 97 | callout：09-22 更新為分階段推給 API 客戶、沒有全面開放時間表 | 確認 |
| 98 | callout：說法都是 OpenAI 自己的敘述、沒有第三方稽核或認證 | 確認 |
| 99 | callout：端點資格是查核當天的快照 | 確認 |
| 100 | 索引連結文字逐字＝索引現行 zh-TW 標題 | 確認（程式比對，相同） |
| 101 | 沒有第二個（投資免責）callout | 確認（AI 垂直只有一個 callout） |

### 來源與日期一致性

| # | 主張 | 判定 |
| --- | --- | --- |
| 102–105 | 四條 `sources[]` 的標題、網址、`checked_on` 2026-09-23 | 確認（今天四條全部 200 且讀到正文） |
| 106 | slug 尾碼 `20260820` ＝ `news_date` 2026-08-20 ＝ 第一段 ＝ DELTA-4-4 第 3 條裁定 | 確認 |
| 107 | `display_order` 181、`topics` ai／software／ai-news、`kind` life | 確認 |

## 3. 改掉的 14 處（before → after）

**C1 標題**
`OpenAI 把零資料保留延伸到前沿模型：…` → `OpenAI 為前沿模型提供零資料保留：…`
公告頁的標題是 `Offering Zero Data Retention for frontier models`，內文寫的是
`Private Safety Processing is designed so we can continue to offer ZDR`（為了**繼續**提供）。
四份來源沒有任何一份按模型列 ZDR 資格，「延伸到前沿模型」會讀成模型層級的資格變動——
正是研究紀錄 `not_said` 第 1 條與 `must_not_write` 第 8 條禁止的推論。研究紀錄的 `title` 已同步。
來源：<https://openai.com/index/offering-zero-data-retention-for-frontier-models/>

**C2 `may` 被刪（兩處：第一段、第一節第一段）**
`有些嚴重風險只有把多次互動放在一起看才看得出來` → `有些嚴重風險可能只有…`
原文 `some serious risks **may** only become visible across multiple interactions`。
來源：同上。

**C3 `start` 被刪**
`OpenAI 表示計畫 9 月推出並發布技術白皮書` → `…計畫 9 月開始推出並發布技術白皮書`
原文 `We plan to **start** rolling out Private Safety Processing, and share a technical white paper, in September.`
來源：同上。

**C4 「公告全篇」（兩處：summary 第 2 條、第二節第一段）**
`公告全篇沒有提到 ChatGPT 的任何方案` → `公告內文沒有提到 ChatGPT 的任何方案`
公告頁的**頁尾導覽**逐字列有 `ChatGPT Business`、`ChatGPT Enterprise`、`ChatGPT for Education` 三個連結
（頁面外殼，不是公告內文）。否定句要限縮在內文才站得住。
來源：同上。

**C5 FAQ 第一題的否定句**
`四份官方來源都只談 API 客戶，公告頁與資料控制文件完全沒有出現 Plus、Business、Enterprise 或 Edu…`
→ `公告內文與兩份開發者文件都只談 API 客戶，沒有出現 Plus、Business、Enterprise 或 Edu…`
兩份開發者文件今天全文 grep `ChatGPT` 是 0 筆（這一半是對的），公告頁則有頁尾那三個連結。
來源：<https://developers.openai.com/api/docs/guides/your-data>

**C6 「沒有提到台灣、亞洲或任何特定地區」（兩處：第五節第一段、FAQ 第五題）**
`四份官方來源都沒有提到 ChatGPT 的任何方案，也沒有提到台灣、亞洲或任何特定地區。`
→ `公告與兩份開發者文件從頭到尾只談 API 客戶，沒有出現任何 ChatGPT 方案，也沒有出現台灣。`
FAQ5：`四份官方來源都沒有提到台灣、亞洲或任何特定地區，` → `公告與兩份開發者文件都沒有提到台灣，`
**這是與來源直接相反的一條。** 資料控制文件的 `Data residency controls` 一節逐列印出
United States、Europe (EEA + Switzerland)、Australia、Canada、Japan、India、Singapore、South Korea、
United Kingdom、United Arab Emirates 十個區域與各自的網域前綴（`jp.api.openai.com`、`sg.api.openai.com`…），
PSP 指南也寫 `Choose an approved US or EU storage region`。台灣則是三份文件都查無（各 0 筆），
所以改成只講台灣。依研究紀錄 `not_said` 第 5 條「資料落地是另一份文件的另一組規則，不要混為一談」，
正文沒有把資料落地的清單搬進來。
來源：<https://developers.openai.com/api/docs/guides/your-data>

**C7 端點資格「符合」那幾格漏了但書**
`聊天、回應、嵌入與影像生成等端點列為符合 ZDR 資格，` → `…列為符合 ZDR 資格（多數還註明另有限制），`
表上 `/v1/chat/completions`、`/v1/responses`、`/v1/images/generations`、`/v1/images/edits` 四格印的是
`Yes, see below for limitations`，只有 `/v1/embeddings` 是單獨的 `Yes`。
來源：同上。

**C8 「只在」硬體證明環境解密**
`加密內容只在一個經核准、關閉人員存取的硬體證明安全執行環境裡解密` → 刪掉「只」
原句 `Encrypted customer content is decrypted in an approved, hardware-attested safety runtime that disables human access.` 沒有 only；
指南講唯一性時用的是 `is designed to be the only workload that can decrypt customer content`，是設計目標不是斷言。
來源：<https://developers.openai.com/api/docs/guides/private-safety-processing>

**C9 「金鑰授權分兩層」（兩處：summary 第 4 條、第四節第二段）**
`金鑰授權分兩層，不是客戶完全獨力掌握` → `加密分兩層，不是客戶完全獨力掌握`
指南寫的是 `Each stored record is **doubly encrypted**`（內層 OpenAI-managed HPKE、外層客戶自管 EKM）。
EKM 沒開時只有一層，說成「金鑰授權分兩層」也與同篇 FAQ 第四題的「加密分兩層」不一致。
來源：同上。

**C10 表格 CSAM 列的「三種設定」**
`三種設定都一樣：疑似兒少性剝削素材的圖片仍保留供人工審查` → `不論哪一種設定：…`
資料控制文件列舉的三種是 `Zero Data Retention, Modified Abuse Monitoring, or **Private Retention with PSP**`，
不是這張表自己的三列（MAM、ZDR、ZDR 搭配 PSP）；公告頁的註腳寫的是 `even in Zero Data Retention deployments`。
改成「不論哪一種設定」兩份來源都撐得住。
來源：<https://developers.openai.com/api/docs/guides/your-data>

**C11 圖說第四環節**
`…只回傳範圍受限的安全訊號、金鑰授權由客戶掌握。` → `…、金鑰授權由客戶掌握（要另外開啟 EKM）。`
外層的客戶自管金鑰就是 EKM，而指南寫的是 `We recommend enabling EKM for this additional control.`（建議、非強制）；
沒開 EKM 時只剩 OpenAI 管理的 HPKE 內層。研究紀錄的 `diagram.caption` 與第四格節點
（`["客戶掌握金鑰", "授權可撤銷"]` → `["客戶掌握金鑰", "要另開 EKM，授權可撤銷"]`）已同步。**圖還沒畫，構圖請照這一格。**
來源：<https://developers.openai.com/api/docs/guides/private-safety-processing>

**C12 兩個收回條款只寫了「取消資格」，沒寫後果**
`…會事先書面通知。` → `…會事先書面通知；真的走到那一步，內容會改留在 OpenAI 的加密紀錄裡，後者還可能對疑似違規的內容做人工審閱。`
`Private Retention with PSP` 一節：`customer content will be retained in encrypted abuse monitoring logs in OpenAI-managed infrastructure`；
`Safety Retention` 一節：`we **may** retain and **human review** customer content when using these models that our classifiers detect as potentially violating…`。
這是全篇「人員拿不到內容」在官方文件上**唯一寫明的例外**，原稿漏掉。
來源：<https://developers.openai.com/api/docs/guides/your-data>

**C13 第一段歸因密度（讀者優先）**
`官方頁面印的發布日期是美國時間 2026 年 8 月 19 日` → `這一頁印的發布日期是美國時間 2026 年 8 月 19 日`
第一段原本有「官方頁面印的」與「OpenAI 表示」兩個歸因語，超過「開頭段最多一個」。
頁面印了什麼是可驗證的事實、不需要歸因語；「OpenAI 表示」留著（廠商宣稱必須歸因）。

**C14 第二段的查證流水帳與「文中」（讀者優先）**
`這一篇的資料在 2026 年 9 月 23 日查核，讀的是 OpenAI 這則公告、兩份開發者文件與官方新聞 RSS；…本站沒有獨立驗證或測試文中提到的任何數字，也不是安全稽核報告。`
→ `這一篇的資料在 2026 年 9 月 23 日查核；這一則在發布當時沒有排進本站的頭條批次，這一篇補上。機制的說法一律以 OpenAI 的官方原文為準，沒有獨立驗證或測試，也不是安全稽核報告。`
DELTA-4-7 第 14 條：查證紀律不要寫進正文，來源清單讀者在 `sources` 就看得到；「文中」是指涉自己的寫法，
規格要求用「這一篇」。查核日留著（自檢要求出現在前兩段）。補寫理由那一句逐字沒動。

## 4. 讀者優先與界線檢查

- 「本文」：0 筆（「文中」1 筆已改）。「最近」「本週」「日前」「近日」：各 0 筆。
- 歸因密度：改完後開頭段 1 個歸因語；正文每一段最多 2 個（第一節第一段、第二節第三段、第三節第一段、
  第四節第三段、第五節第二段各 2 個，都在限內）。
- 描述 193 字，句尾「（2026 年 9 月查證）」，沒有查證流水帳、沒有選件數字；標題與 summary 也沒有。
- 沒有購買建議、沒有推薦式比價、沒有估值或投資語氣；AI 垂直只有一個 callout，沒有自己加免責段。
- 廠商宣稱都有歸因；「預覽／分階段開放」的狀態在 summary、第一節、FAQ3、callout 四處都寫到。
- 「業界首創」「唯一」「最安全」「從未」：0 筆。沒有描述商標圖示或介面截圖；後台路徑只用文字。
- 沒有抄任何 ARN、應用程式 ID、bucket 名稱或 curl 指令（指南裡有，正文一個都沒有）。
- 沒有引述 Glean 資安長的推薦語（頁面上有，正文沒有）；四家客戶寫明是 OpenAI 自己列的。
- 兩個結尾連結的文字與目標內容包的 zh-TW 標題逐字相同（程式比對）。

## 5. 留給協調者的事

1. **與〈OpenAI Agents API 公開 beta〉的重疊。** `must_not_write` 第 14 條把「ZDR 的基本定義、濫用監控預設 30 天」
   劃給那一篇，但本篇第二節仍逐字引了 ZDR 的定義句、也寫了濫用監控預設最多 30 天。查核者判斷這兩句在本篇有獨立
   用途（定義句是這則公告的核心引文；30 天是為了與 PSP 的 30 天 TTL 做區隔，正文也明講「是兩回事」），所以沒有刪。
   Agents API 在正文只被提到一次（`/v1/agents` 仍是 No）並連過去，第二個結尾連結是規格要求的結構，不算重述。
   要不要再壓縮，請協調者決定。
2. **PSP 技術白皮書。** 研究紀錄把它放在 `unverified_or_excluded`（`sources[]` 四條已滿），所以正文一個字都沒寫。
   公告頁承諾的「9 月發布白皮書」已經兌現（09-22）。若要寫，依研究紀錄的規定必須把白皮書換進 `sources[]`
   （建議換掉 RSS 那條，並把事件時刻的依據寫進 `event_date_basis`）。
3. **「美國時間 8 月 19 日」。** 頁面只印 `August 19, 2026`、沒有印時區；「美國時間」是從 RSS 的 19:00 GMT 推出來的
   （當下美東 15:00、美西 12:00，確實還是 8 月 19 日）。推論成立但不是頁面逐字，要不要改成不帶時區的寫法請裁示。
4. **`/v1/videos`。** 表上 ZDR 資格是 No，而且文件另寫 `v1/videos is currently blocked for MAM or ZDR requests`。
   正文的不符合清單用「等端點」收尾、沒列到影片；不是錯，但如果想讓清單更貼近表格，影片是最值得補的一格
   （字數還有 17 字的空間）。
5. **圖還沒畫。** `build_assets.py` 的 `_DRAWINGS` 沒有本 slug。第四格的文字已經改成「要另開 EKM，授權可撤銷」，
   構圖與 alt 請照這一格，不要畫成「金鑰完全由客戶掌握」。

## 6. 自檢輸出（原樣）

```
OK ai-news-openai-zero-data-retention-20260820 zh-TW paragraphs 2983
check_article exit=0
```

```
ai-news-openai-zero-data-retention-20260820
  error: image_missing: zh-TW: /guides/ai-news-openai-zero-data-retention-20260820/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-zero-data-retention-20260820/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

`image_missing` 兩條是預期內（圖還沒畫）；沒有 `raw_internal_url`。
正文 2,983 字，距離 3,000 的上限剩 17 字——**第二輪要加字的話要先量。**

## 7. 需不需要第二輪

**需要。** 改了 14 處（12 處事實或限定詞、2 處讀者優先），其中 C1 動到標題、C6 改掉一條與來源相反的否定句、
C12 在第四節新增一整句。第二輪要逐句回一手來源重查 C1–C12 這 12 條，加上第一輪新寫進去的那一句
（「真的走到那一步，內容會改留在 OpenAI 的加密紀錄裡，後者還可能對疑似違規的內容做人工審閱。」），
以及確認過的 93 條裡隨機三分之一。
