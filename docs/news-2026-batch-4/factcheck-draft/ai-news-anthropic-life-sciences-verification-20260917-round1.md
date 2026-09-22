# 查核報告（第一輪）ai-news-anthropic-life-sciences-verification-20260917

- 查核代理：獨立查核代理（第一輪），未參與撰稿
- 查核日：2026-09-23（台北）
- 垂直／順序：AI／`display_order` 173；事件日 2026-09-17；`kind` life
- 內容包：`apps/api/app/guides/content/ai-news-anthropic-life-sciences-verification-20260917.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-anthropic-life-sciences-verification-20260917.json`
- 依據：`FACTCHECK-47.md`、`DELTA-4-7.md`（優先）、`agents/ai/FACTCHECK.md`、`ASSIGNMENTS.md` A3 列

## 1. 來源重抓結果（2026-09-23 台北 01:03–01:04）

全部用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒；
UA、標頭、查詢字串都沒有帶任何姓名或 email；沒有填寫或送出任何表單（只做 GET）。

| # | 來源 | 狀態 | bytes | 是否讀到正文 | 與撰稿代理 00:27–00:30 抓到的差異 |
| --- | --- | --- | --- | --- | --- |
| S1 | `https://www.anthropic.com/news/life-sciences-verification-program` | 200 | 173,459 | 是。六個小節（Verification and access types／Enabling trusted access through shared responsibility／How monitoring works in LSVP／What researchers are saying／Applications and availability／What comes next）全部讀到 | 173,464 → 173,459，差 5 bytes，出在頁尾 Related content 動態卡片；正文一字未變 |
| S2 | `https://www.anthropic.com/news` | 200 | 460,541 | 是。列表仍把本篇標 `Sep 17, 2026` + `Announcements` | 462,392 → 460,541；精選卡片改成 2026-09-22 的 Introducing Claude Opus 5.5（活頁面，見 `live_data_warnings` 第 1 條） |
| S3 | `https://www.anthropic.com/threat-intelligence-report-september-2026` | 200 | 1,221,782 | 是。讀到 `seven harm areas` 那一段與生物誤用整節 | 1,221,761 → 1,221,782，正文未變 |
| S4 | `https://claude.com/form/life-sciences-verification-program` | 200 | 441,344 | 是。方案說明與資格說明都讀到 | **正文改字**：441,311 → 441,344（差 33 bytes 就是那一句），見第 4 節 |

`verbatim_quote` 逐條連續字串比對：`verified_facts` 43 條，41 條在抽出的純文字命中、第 37 條依紀錄所載在 `.html` 的 RSC payload 命中、第 40 條因 S4 當天改字而失效（不是捏造，兩個時點的 HTML 都在）。
`sources[]` 四條的 `verbatim_quote` 三條命中、第四條同上。

## 2. 主張逐條核對

Verdict：C＝CONFIRMED，**CH＝CHANGED**，NF＝NOT FOUND，OOS＝OUT OF SCOPE（風格）。
「來源」欄 S1–S4 對應第 1 節。

### 2.1 title／description

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 1 | 方案名稱「生命科學驗證方案（LSVP）」 | S1 `Life Sciences Verification Program (LSVP)` | C |
| 2 | 「上線」＝當天開放申請、以 beta 起步 | S1 `are now opening applications…launching in beta` | C |
| 3 | 「通過驗證的團隊才鬆綁生物類限制」 | S1 驗證三項＋grant 綁定 | C |
| 4 | title 與研究紀錄 `title` 逐字相同 | 程式比對 True | C |
| 5 | description：2026-09-17、Anthropic 推出 LSVP | S1／S2 | C |
| 6 | description：通過驗證的團隊與機構、較寬鬆防護、Mythos／Opus／Sonnet | S1 第一段 | C |
| 7 | description：原本被擋下的生物相關工作 | S1 `currently blocked in our generally available Fable models` | C |
| 8 | description：分標準用途與高風險用途，鬆綁範圍／續約週期／適用型號不同 | S1 兩節 | C |
| 9 | description：個人方案與第三方平台目前都沒有支援 | S1 `We do not yet support individual plans…not yet available on third-party platforms` | C |
| 10 | description 長度 168 字（120–200）、句尾只帶「（2026 年 9 月查證）」、無清點數字 | DELTA-4-7 §14 | C |

### 2.2 前言兩段

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 11 | 第一段日期 2026-09-17＝`news_date`＝slug 後綴 | 三者一致 | C |
| 12 | LSVP 英文全名與縮寫 | S1 | C |
| 13 | 對象是「生命科學專業人員」 | S1 `life science professionals` | C |
| 14 | 一組對生物相關工作較寬鬆的防護 | S1 `refined set of safeguards more permissive for biology-related work` | C |
| 15 | 這些工作在一般開放的 Fable 模型上被擋住 | S1 | C |
| 16 | 給組織申請的 beta、只開放團隊與機構 | S1 `launching in beta, initially for teams and institutions` | C |
| 17 | 「不是一般 Claude 使用者會遇到的變化」 | S1＋S4 資格句；`must_not_write` 第 2 條要求這樣寫 | C |
| 18 | 「前一輪名額已滿，留到這一輪才補上」 | DELTA-4-7 §1 要求交代，研究紀錄 `editorial_brief` 指定用「名額已滿」 | C |
| 19 | 「日期仍照事件發生的 9 月 17 日寫」 | 同上；但屬編務說明，見第 5 節 | OOS |
| 20 | 第二段查核日 2026-09-23，與四條 `sources.checked_on`、研究紀錄 `checked_on`、表格 caption 四處一致 | 程式比對 | C |
| 21 | 第二段列出的三類依據（公告頁、申請頁、威脅情報報告） | S1／S4／S3 | C |
| 22 | 「本站沒有實測、不提供訂閱或申請建議」 | AI 垂直界線 | C |

### 2.3 summary 五句

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 23 | S1 句：9/17、LSVP、團隊與機構、三個型號、beta、Pro／Max 還不能用 | S1＋S4 | C |
| 24 | S2 句：研究資格、資安標準、研究倫理監督三項審查 | S1 `research credentials, security standards, and ethical research oversight` | C |
| 25 | S2 句：通過後才能申請兩種授權 | S1 `Once verified, teams may apply for two types` | C |
| 26 | S3 句：標準用途整個團隊、一年續約、Mythos 5.1／Opus 5／Sonnet 5 | S1 | C |
| 27 | S3 句：高風險單一研究專案、六個月續約、移除阻擋生命科學請求的防護、資安分類器不受影響 | S1 兩句連寫 | C |
| 28 | S4 句：即時阻擋改離線監測、LSVP 流量保留 30 天、組織自訂安全用途、管理員限時處置 | S1 | C |
| 29 | S5 句：查核日公告頁與申請頁都沒說開放地區、沒提台灣 | 對 S1／S4 純文字 grep `taiwan`／`台灣` 各 0 筆；全頁唯一的 `available in` 是 `available in our first-party console` | C |
| 30 | summary 每一句都能在正文找到對應（checker 強制） | `check_article.py` OK | C |

### 2.4 第一節「9 月 17 日發生了什麼」

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 31 | 跨過一般開放模型對生物相關工作的門檻 | S1 | C |
| 32 | 例子：藥物開發、研究生物學、臨床開發與製造，且原文用「像」帶出 | S1 `like drug discovery, research biology, clinical development, and manufacturing` | C（譯法見第 4 節開放問題） |
| 33 | 服務對象從學術實驗室到新創、藥廠「等等」 | S1 `from academic labs to startups, pharma companies, and more` | C |
| 34 | 驗證審三個項目 | S1 | C |
| 35 | 通過後才能申請兩種授權、兩者可以並存 | S1 `add-on grant`＋`one Standard Use grant…and one or more High-risk Use grants` | C |
| 36 | 「已有數十個組織透過早期存取**用過**這個方案」 | S1 `We have already onboarded dozens of organizations` | **CH**（改「加入」） |
| 37 | 9 月 17 日才對外開放申請 | S1 `are now opening applications to the broader life science community` | C |
| 38 | 「公司預期第一週**再增**數百個組織」 | S1 `We expect to enroll hundreds of organizations within the first week` | **CH**（改「納入」） |
| 39 | 之後幾週擴大到涵蓋多數生命科學社群 | S1 | C |
| 40 | 「這是當天寫下的預期，查核當天沒看到後續公布的實際數字」 | S2 列表到 9/22 為止沒有後續數字；否定句已限縮在「查核當天沒看到」 | C |
| 41 | 威脅報告顯示平台上有愈來愈精密的濫用嘗試，含可能支援生物武器開發的嘗試 | S1 `As we've shown in our recent threat report…` | C |
| 42 | 「因此近期模型上線時**都**帶了較嚴格的防護」 | S3 `we have launched recent models (most notably Claude Fable 5) with stronger safeguards` | **CH**（刪「都」） |
| 43 | 限制大量兩用生物研究查詢 | S3 `restrict access to a wide range of dual-use biological research queries` | C |
| 44 | LSVP 要鬆綁的正是這一層 | S1＋S3 因果 | C |
| 45 | 生物領域常無法只憑一個請求判斷善惡意；最擔心的是合法存取被挪用或奪走 | S1 `the most concerning threat models are ones where valid access has been diverted or overtaken` | C |

### 2.5 第二節「兩種授權」

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 46 | 標準用途可擴及整個團隊的日常多樣工作（保留「可」） | S1 `can be extended to entire teams for diverse, daily workloads` | C |
| 47 | 一年續約一次 | S1 `renewed once a year` | C |
| 48 | 「**今天**適用 Mythos 5.1、Opus 5 與 Sonnet 5」 | S1 `apply to Mythos 5.1, Opus 5, and Sonnet 5 today`，today＝公告當天 | **CH**（改「9 月 17 日當天」） |
| 49 | 未來推出的新模型也會納入 | S1 `and to future models as they launch` | C |
| 50 | 涵蓋範圍八項清單，以「等等」收尾、不是完整清單 | S1 `basic science, R&D, supply chain and manufacturing, clinical development, quality assurance, regulatory affairs, investing and diligence, and more` | C |
| 51 | 公司預期標準用途應能滿足大多數需求（有歸因） | S1 `Although we expect Standard Use to cover the majority of access needs` | C |
| 52 | 部分工作誤用風險較高、需要額外審查 | S1 `some work carries a higher potential for misuse and therefore requires additional vetting` | C |
| 53 | 高風險是標準用途之外的附加授權 | S1 `add-on grant` | C |
| 54 | 只適用單一研究專案、不是整個團隊 | S1 `applies to a single research project as opposed to a full team` | C |
| 55 | 每六個月要續約一次 | S1 `must be renewed every six months` | C |
| 56 | 移除所有阻擋生命科學請求的防護，但資安分類器等其他防護不鬆動（兩句一起寫） | S1 `It removes all safeguards that block life sciences requests`＋`All other safeguards, such as cyber classifiers, will remain in place` | C |
| 57 | 兩用研究者的典型情境：一個標準＋一或多個綁專案的高風險 | S1 | C |
| 58 | 病毒載體的例子（只轉述一次，未延伸生物學細節） | S1；`must_not_write` 第 11 條 | C |
| 59 | 高風險目前可用在 Claude Opus 5 與 Claude Sonnet 5 | S1 `High-risk grants for Claude Opus 5 and Claude Sonnet 5 are available today` | C |
| 60 | Claude Mythos 高風險在這次發布時仍只開放少數經額外審查的機構 | S1 `at the time of this launch they will remain limited to a small set of entities with additional vetting` | C |
| 61 | Anthropic 說正與美國政府合作、希望之後擴大（歸因完整、未寫成已開放） | S1 `We are working with the US government` | C |
| 62 | 產品介面清單是舉例（Claude Science、Claude.ai、Claude Code、API） | S1 `including` | C |

### 2.6 表格（表頭 3＋4 列 12 格＋caption）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 63 | 表頭「授權類型」 | — | C |
| 64 | 表頭「涵蓋範圍與續約週期」 | — | C |
| 65 | 表頭「適用模型／方案（**查核日資訊**）」 | 四列內容全部出自 9/17 公告；查核日的 S4 寫的是 Opus 5.5 | **CH**（改「依 9 月 17 日公告」） |
| 66–68 | 第 1 列：標準用途 Standard Use／整個團隊，一年續約一次／Mythos 5.1、Opus 5、Sonnet 5 | S1 | C |
| 69–71 | 第 2 列：高風險用途 High-risk Use／單一研究專案，六個月續約一次／Opus 5、Sonnet 5 可用；Mythos 限少數機構 | S1 | C |
| 72–74 | 第 3 列：個人 Pro／Max 方案／beta 階段不符資格／Anthropic 說之後才會擴大 | S1 `launching in beta, initially for teams and institutions`＋`expand access to individual Pro and Max plans over time`；S4 `Free, Pro, and Max plans are not eligible at this time` | C |
| 75–77 | 第 4 列：第三方平台／尚未提供／僅第一方 console／Enterprise／Team | S1 `Today, LSVP is available in our first-party console for API usage, as well as in Claude for Enterprise and Team plans. …not yet available on third-party platforms.` | C |
| 78 | caption 含查核日 2026-09-23、長度 47 字（≤200） | — | C |

### 2.7 第三節「還沒放寬的部分」

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 79 | 目前只給團隊與機構，個人 Pro／Max 還用不到 | S1＋S4 | C |
| 80 | 之後會逐步擴大到個人方案、沒有時間表 | S1 `over time`；`not_said` 第 11 條 | C |
| 81 | API 與 Claude Science 可原生切換授權 | S1 `users can switch between grants natively` | C |
| 82 | Claude.ai 與 Claude Code 一開始只套用一個預選的預設授權 | S1 `initially only a preselected default grant applies` | C |
| 83 | 「**唯一的**例外是用 API 驗證方式登入 Claude Code」 | S1 只寫一個括號例外，沒寫那是唯一 | **CH**（刪「唯一的」） |
| 84 | beta 階段不支援已簽 BAA 的組織 | S1 `LSVP is not available for BAA-enabled orgs` | C |
| 85 | 有「**病患**健康資訊（PHI）」的客戶要另用非 BAA、非 HIPAA 的組織 | S1 `customers with PHI data should use separate non-BAA orgs with non-HIPAA`；PHI＝Protected Health Information | **CH**（改「受保護健康資訊」） |
| 86 | 發布當下：第一方 console 的 API 存取＋Enterprise 與 Team；未開放第三方平台 | S1 | C |
| 87 | 9/17 公告寫標準用途適用 Mythos 5.1、Opus 5、Sonnet 5 | S1 | C |
| 88 | 申請頁在 2026-09-23 查核時寫 Mythos 5.1 用於生物與藥物開發、Opus 5.5 與 Sonnet 5 搭配調整過的生物安全分類器 | S4（今日重抓仍逐字相同） | C |
| 89 | 申請頁沒印日期、看不出何時寫上去 | S4 全頁無日期；頁尾版權寫 `© [year]` 未填 | C |
| 90 | 兩個時間點要分開看、未寫成「Anthropic 更新了公告」 | `must_not_write` 第 8 條 | C |

### 2.8 圖解

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 91 | alt 的四格內容＝研究紀錄 `diagram.nodes` 四格 | 逐項比對 | C |
| 92 | caption 與研究紀錄 `diagram.caption` 逐字相同，且數字（一年／半年／整個團隊／單一專案）都在正文出現 | 程式比對 True | C |

### 2.9 第四節「從即時擋下改成事後監看」

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 93 | 一般情況是每次請求即時判斷要不要擋 | S1 `real-time blocking, where we reject potentially harmful access at the time of each request` | C |
| 94 | 嚴重濫用常分散在多次請求、多個工作階段以避開偵測 | S1 `Serious misuse is often spread across many requests and sessions to look disconnected and evade detection` | C |
| 95 | LSVP 改成離線監測＝事後比對使用模式 | S1 `offline monitoring…across patterns of behavior` | C |
| 96 | 要求 LSVP 流量保留 30 天資料（限於 LSVP 流量，不是全體使用者） | S1 `For LSVP traffic, we are requiring data retention for 30 days` | C |
| 97 | 資料嚴格區隔、不能用於訓練、生命科學研究團隊成員不能存取 | S1 | C |
| 98 | 責任共擔：已審查過組織的可信度與監督機制，才由組織自訂安全用途 | S1 `Because we vet the LSVP organizations…we can empower them to specify for themselves` | C |
| 99 | 存取權綁定申請書寫的用途 | S1 `Each entity's access is tied to the use cases it has specified` | C |
| 100 | 申請書寫像職缺公告那樣的高層次說明，不放敏感資訊或 IP | S1 | C |
| 101 | Anthropic 持續監測 LSVP 流量、找出超出範圍的使用或模式 | S1 `we continuously monitor LSVP traffic` | C |
| 102 | 「一旦發現未經授權的活動，**會通知**組織的管理員」 | S1 `we **can** flag these cases to organization admins` | **CH**（改「可以把案例交給」） |
| 103 | 由管理員在事先講好的時限內處理，而不是系統自動擋下 | S1 `to take action within pre-agreed timeframes` | C |

### 2.10 第五節「讀者自己查得到什麼」

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 104 | 查核日公告頁與申請頁都沒說任何國家或地區的開放條件、沒提台灣 | S1／S4 grep 0 筆 | C |
| 105 | 台灣的生技公司、醫院、大學實驗室能不能申請，兩頁都沒寫 | 同上 | C |
| 106 | 「不能用『Team 與 Enterprise 方案在台灣買得到』去推論」 | 研究紀錄 `unverified_or_excluded` 第 1 條原句；但這個前提本身沒有來源，見第 4 節 | C（留給協調者） |
| 107 | 沒交代審查要多久、通過率、能不能申訴 | `not_said` 第 3 條；今日重讀兩頁確認 | C |
| 108 | 沒寫高風險六個月到期續約要不要重審、專案結束怎麼收回 | `not_said` 第 6 條 | C |
| 109 | 只承諾未來幾個月再說明新產品、研究合作與方案改進，沒給時間 | S1 `in the coming months` | C |
| 110 | 要由管理員在申請頁填表登記意願、Anthropic 再評估資格、不保證取得存取權 | S4 兩句 | C |
| 111 | 兩用生物研究風險正是 9 月稍早威脅情報報告點出的隱憂之一 | S3；S2 列表標該報告 `Sep 10, 2026`（早於 9/17） | C |
| 112 | 「報告寫了哪**七**類濫用」 | S3 `seven harm areas: cyber operations, influence operations, surveillance, scams and fraud, biological misuse, conventional weapons development, and distillation` | C |
| 113 | 「哪些 API 金鑰被盯上」 | S3 竊得／外洩 API 金鑰的案例段落 | C |
| 114 | 未重述第二連結那篇的七類內容與自保清單，只做導流 | `must_not_write` 第 18 條 | C |

### 2.11 FAQ 五題

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 115 | Q1「不會」＋只給通過驗證的團隊與機構、在登記用途範圍內 | S1 | C |
| 116 | Q1「一般開放的 Fable 模型與其他一般帳號的防護沒有任何改變」 | S1 的設計前提；`must_not_write` 第 2 條要求這樣寫 | C |
| 117 | Q2 台灣：兩頁都沒寫、無法判斷，只能等說明或直接確認 | S1／S4 grep 0 筆 | C |
| 118 | Q3「一年續約一次，能滿足大多數日常工作」（無歸因） | S1 `Standard Use grants are suitable for most life science work`／`we expect Standard Use to cover…` 都是 Anthropic 自己的說法 | **CH**（補「Anthropic 說」） |
| 119 | Q3 其餘：高風險只綁單一專案、半年續約、只移除生命科學相關防護 | S1 | C |
| 120 | Q4「即時阻擋改離線監測、換來 30 天資料保留」 | S1 | C |
| 121 | Q4「一旦超出申請書範圍，Anthropic **會通知**管理員」 | S1 `we can flag` | **CH**（改「可以把案例交給」） |
| 122 | Q5 9/17 公告 vs 申請頁 9/23 的型號差異、申請頁沒印日期 | S1／S4 | C |

### 2.12 callout、結尾連結、sources

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 123 | callout：只開放通過驗證的團隊與機構，在 Team 與 Enterprise 方案申請 | S1／S4 | C |
| 124 | callout：Free、Pro、Max 與第三方平台都還沒有這個選項 | S4／S1 | C |
| 125 | callout：放寬範圍綁定申請書登記用途、資安分類器等其他防護不受影響 | S1 | C |
| 126 | callout：查核日兩頁都沒說開放地區、沒提台灣 | S1／S4 | C |
| 127 | callout：規格數字都是 Anthropic 的說法、本站沒有實測；全篇只有這一個 callout、沒有免責 callout | AI 垂直界線 | C |
| 128 | 第一個連結 text＝`ai-news-2026-january-september-index` 的 zh-TW title，逐字相同 | 程式比對 True | C |
| 129 | 第二個連結 text＝`ai-news-anthropic-threat-report-20260910` 的 zh-TW title，逐字相同；且公告內文的 `recent threat report` href 正是那份報告 | 程式比對 True；S1 HTML href 查證 | C |
| 130 | `sources[]` 四條的 title 描述與 `checked_on` 2026-09-23 | 第 1 節重抓 | C |

**統計：核對 130 條主張——CONFIRMED 119、CHANGED 10、NOT FOUND 0、OUT OF SCOPE 1。沒有任何一句因為查不到來源而需要刪除。**

## 3. 改掉的 10 處（before → after）

全部出自 `https://www.anthropic.com/news/life-sciences-verification-program`（第 3 處出自
`https://www.anthropic.com/threat-intelligence-report-september-2026`）。

| # | 位置 | before | after | 來源原文怎麼寫／為什麼 |
| --- | --- | --- | --- | --- |
| 1 | 正文第 4 段 | 已有數十個組織透過早期存取**用過**這個方案 | 已有數十個組織透過早期存取**加入**這個方案 | `We have already onboarded dozens of organizations through an early-access program`。onboarded 是已納入、仍在用的狀態；「用過」讀起來像已經結束 |
| 2 | 正文第 4 段 | 公司預期第一週**再增**數百個組織 | 公司預期第一週**納入**數百個組織 | `We expect to enroll hundreds of organizations within the first week`。原文沒有寫這是相對於「數十個」的增量，「再增」是自己算出來的關係 |
| 3 | 正文第 5 段 | 因此近期模型上線時**都**帶了較嚴格的防護 | 因此近期模型上線時帶了較嚴格的防護 | `we have launched recent models (most notably Claude Fable 5) with stronger safeguards`。原文沒有全稱語氣，「都」是被加上去的絕對詞 |
| 4 | 正文第 6 段 | 一年續約一次；**今天**適用 Mythos 5.1、Opus 5 與 Sonnet 5 | 一年續約一次；**9 月 17 日當天**適用 Mythos 5.1、Opus 5 與 Sonnet 5 | `Standard Use grants apply to Mythos 5.1, Opus 5, and Sonnet 5 today`，today＝公告當天。文章後段自己寫申請頁在 9/23 是 Opus 5.5，留著「今天」會被讀成閱讀當天，正是 `must_not_write` 第 8 條要避免的日期混用 |
| 5 | 表格表頭第 3 欄 | 適用模型／方案（**查核日資訊**） | 適用模型／方案（**依 9 月 17 日公告**） | 四列內容全部出自 9/17 公告；查核日的申請頁寫的是 Opus 5.5，標成「查核日資訊」會與正文第 11 段、FAQ 第 5 題自相矛盾 |
| 6 | 正文第 9 段 | **唯一的**例外是用 API 驗證方式登入 Claude Code 的情況 | 例外是用 API 驗證方式登入 Claude Code 的情況 | `(except while using Claude Code with API authentication)`。原文只寫一個括號例外，沒有寫那是唯一的例外 |
| 7 | 正文第 10 段 | 手上有**病患**健康資訊（PHI）的客戶 | 手上有**受保護**健康資訊（PHI）的客戶 | 原文只寫 `customers with PHI data`；PHI＝Protected Health Information，「病患健康資訊」把 Protected 讀成 Patient |
| 8 | 正文第 14 段 | 一旦發現未經授權的活動，**會通知**組織的管理員 | 一旦發現未經授權的活動，**可以把案例交給**組織的管理員 | `Should unauthorized activity occur, we **can** flag these cases to organization admins`。can 是能力不是承諾，寫成「會通知」是安靜強化來源（BRIEF 的錯誤型態第 1 類） |
| 9 | FAQ 第 4 題 | 一旦發現用途超出申請書登記的範圍，Anthropic **會通知**組織的管理員 | 一旦發現用途超出申請書登記的範圍，Anthropic **可以把案例交給**組織的管理員 | 同第 8 處，一併改以維持全篇一致 |
| 10 | FAQ 第 3 題 | 一年續約一次，**能滿足**大多數日常工作 | 一年續約一次，**Anthropic 說這能滿足**大多數日常工作 | `Standard Use grants are suitable for most life science work`／`we expect Standard Use to cover the majority of access needs` 都是廠商自己的說法；正文第 6 段有歸因，FAQ 漏掉了 |

字數影響：正文 2,860 → 2,869 字（上限 3,000）。表格與 FAQ 不計入正文字數。

## 4. 留給協調者的事（開放問題）

1. **申請頁在查核當天改字。** 撰稿代理 00:30 抓到的是
   `LSVP is currently available to verified organizations on Team and Enterprise plans only.`；
   查核代理 01:03 重抓變成
   `LSVP is currently available to verified organizations on Claude Enterprise and Team plans, and the Claude Platform (API).`
   （441,311 → 441,344 bytes，差的 33 bytes 剛好就是這一句）。因此研究紀錄 `sources[3]` 與 `verified_facts` 第 40 條的
   `verbatim_quote` 在現行頁面上搜尋不到——**兩個時點的 HTML 都留著，不是捏造**。
   語意沒有被推翻：正文第 10 段、表格第 4 列與 callout 寫的「第一方 console 提供 API 存取／Enterprise 與 Team」本來就涵蓋
   Claude Platform (API)，所以正文沒有改。**要不要把那兩處 `verbatim_quote` 更新成新句子請協調者裁定**；
   第二輪重跑逐字比對時會再撞到一次，這裡先講清楚免得被當成撰稿代理造假。
2. **`drug discovery` 的譯法。** 公告同一個清單裡有 `drug discovery` 與 `clinical development`，
   研究紀錄 `verified_facts` 第 4 條與正文（第 3 段、第 11 段各一處）都譯成「藥物開發」與「臨床開發」，兩個「開發」容易混
   （`drug discovery` 一般譯「新藥探索」）。研究紀錄是拘束性文件而且自己就是這樣寫，查核代理不自行偏離，是否統一請協調者決定。
3. **正文第 15 段引用了一個沒有來源的前提。** 「不能用『Team 與 Enterprise 方案在台灣買得到』去推論這個方案在台灣是否開放」——
   四條來源沒有一條寫台灣的方案供應情況。這句是照研究紀錄 `unverified_or_excluded` 第 1 條原樣搬來的，所以保留；
   若不希望正文帶入未查證的前提，可改成「不能從別處的方案供應情況去推論」。
4. **Opus 5.5 有自己的發布日了。** 新聞總覽頁今天的精選卡片是 2026-09-22 的 `Introducing Claude Opus 5.5`。
   正文「申請頁沒印日期，看不出何時寫上去的」仍然成立；若要讓讀者知道 Opus 5.5 已有發布日，需要新增一條來源
   （本輪沒有抓那一頁，所以沒寫）。順帶一提，這也表示 `claude-model-lineup-2026` 的型號清單（查核日 2026-09-13）已經落後，
   照研究紀錄 `live_data_warnings` 第 6 條，那屬於另開維護票的範圍。

## 5. 讀者優先（DELTA-4-7 §14）檢查

- **「本文」0 次**，指涉自己一律用「這一篇」。✔
- **`description` 沒有查證流水帳**，句尾只有「（2026 年 9 月查證）」。✔
- **title／description／summary 都沒有清點數字。** ✔
- **正文只有 1 個「官方」**（第 4 段「這是官方當天寫下的預期」），沒有韓國美食特輯那種密度。✔
- **第一段就講清楚跟讀者的關係**（給組織申請的 beta、不是一般帳號的改變）。✔
- **歸因密度偏高**：第 3、4、6、8、16 段各有兩個以上的歸因詞（`Anthropic 表示`／`Anthropic 說明`／`公司預期`／`公告舉`／`公告列`／`官方`），
  嚴格看超過「每段至多一次歸因」。這不是事實錯誤，而且查核規格明令 `never restyle`，所以**沒有動**，留給協調者或第二輪。
- **第一段末句「日期仍照事件發生的 9 月 17 日寫」是編務說明不是內容**（列為 OOS 第 19 條）。DELTA-4-7 §1 要求交代「為什麼現在才整理」，
  前半句「這則消息在前一輪整理時名額已滿，留到這一輪才補上」已經滿足；末句可刪 15 字而不損任何事實，同樣留給協調者裁定。
- **AI 垂直界線**：無購買建議、無推薦式比價、無金額、無「首創／唯一／最嚴格」比較級；廠商宣稱皆有歸因；
  beta／預期／尚未支援三種狀態都保留；只有一個 callout，沒有免責 callout。✔
- **補寫件規則**：「最近」「近日」「本週」「日前」逐字 grep 各 0 次；slug 後綴＝`news_date`＝第一段日期＝2026-09-17。✔

## 6. 自檢輸出（原樣）

```
check_article exit=0
OK ai-news-anthropic-life-sciences-verification-20260917 zh-TW paragraphs 2869
```

```
pack_cli lint exit=1
ai-news-anthropic-life-sciences-verification-20260917
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-anthropic-life-sciences-verification-20260917/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-anthropic-life-sciences-verification-20260917/diagram-1.svg
1 entries checked
```

兩項都符合 `FACTCHECK-47.md` 的預期：`check_article.py` 印 OK；`pack_cli lint` 只剩 `image_missing`（圖還沒畫）
與 `raw_internal_url`（還沒 relink），exit code 1 由這兩個 error 造成。

## 7. 結論

- 骨幹敘述全部站得住：兩種授權的條件、資安分類器不鬆動、Mythos 高風險仍限少數機構、BAA／PHI 的限制、
  即時阻擋改離線監測與 30 天保留、以及「官方頁沒有寫開放地區、沒有提到台灣」這個對台灣讀者最重要的結論，
  都能回到今天重抓的一手頁面原文。
- 10 處修正全部屬於限定詞（`can`、`唯一`、`都`）、日期歸屬（`today`、表頭時點）、名詞精確度（PHI）與漏掉的歸因，
  沒有一處動到骨幹論述，也沒有任何一句因查不到來源而刪除。
- **需要第二輪**（DELTA-4-7 §12 規定第一輪一律要第二輪）。本輪 **10 處事實修正**，第二輪請特別看：
  第 3 節 10 處全部、隨機三分之一的 CONFIRMED 條目，以及第 4 節第 1 點（申請頁改字，逐字比對會再失敗一次）。
