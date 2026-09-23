# ai-news-meta-muse-agent-20260909 第二輪查核報告

- 查核代理：獨立第二輪查核代理（Claude Opus 5），未參與撰稿、也未參與第一輪
- 查核日：2026-09-23（台北），重抓時間 09:25–09:26
- 內容包：`apps/api/app/guides/content/ai-news-meta-muse-agent-20260909.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-meta-muse-agent-20260909.json`
- 工作樹：`C:\Users\x8120\mokaair\.claude\worktrees\news-4-4`（全程沒有執行任何 git 指令）
- 第一輪報告：`C:\Users\x8120\mokaair-work\news44\factcheck\ai-news-meta-muse-agent-20260909-round1.md`
- 本輪查 **63 條**：第一輪改過的 10 處、第一輪新寫進去的 14 句、從 117 條 CONFIRMED 中
  以 seed 20260923 抽出的 39 條（隨機三分之一）；另做 54 條 `verbatim_quote` 的程式比對與四條來源重抓。
- 判定：CONFIRMED 52、CHANGED 11、NOT FOUND 0。11 條合併成 **9 處精確字串取代**（同一處取代涵蓋多條）。
- 結論：**ok**（沒有動到骨幹論述，沒有改任何日期、金額或機制名稱；自檢 `check_article.py` exit 0）

## 1. 重抓結果（我自己抓的，不是沿用第一輪）

`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 2 秒。
任何請求的 UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料；沒有填寫或送出任何表單，
沒有註冊 muse.ai，沒有嘗試任何繞過地區限制的做法。

| # | 來源 | HTTP | bytes（本輪／第一輪） | 抽出正文字元（本輪／第一輪／研究紀錄） | 是否為正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | about.fb.com Newsroom 發表稿 | 200 | 646,535／646,535 | 12,018／12,018／12,018 | 是，讀到 Categories／Tags |
| 2 | research.meta.ai 安全長文 | 200 | 189,405／189,320 | 24,938／24,938／24,938 | 是，讀到結尾註腳與頁尾模型清單 |
| 3 | research.meta.ai Muse Spark 1.3 | 200 | 189,790／189,791 | 10,558／10,558／10,558 | 是，讀到 Availability 與 Looking Forward |
| 4 | introducing.muse.ai 產品設計說明 | 200 | 44,788／44,788 | 9,029／9,029／9,029 | 是，讀到 Ready to try Muse? |

四頁抽出的正文字元數與第一輪、與研究紀錄**逐一相同**；bytes 的差異只在頁尾隨建置變動的資產清單。
研究紀錄 54 條 `verbatim_quote` 以程式對**我自己抽出的正文**做連續子字串比對，**54 條全數命中**，
而且沒有任何一條帶 `...`／`…`／`|` 的拼接引文（不存在把兩段拼成一句的風險）。

事件日獨立複核：今天自己抓的 `muse.html` 裡 `"datePublished":"2026-09-08T19:00:51+00:00"` 出現 2 次、
`article:published_time content="2026-09-08T19:00:51+00:00"` 1 次、`dateModified` **0** 次，
頁面自印「September 8, 2026 September 8, 2026」（第 235 行）。換算台北 2026-09-09T03:00:51+08:00。
另外兩頁的 JSON-LD：安全長文 `datePublished` **2026-09-08**（與發表稿同一天，所以「Bug 懸賞從發表當天起」成立）、
Spark 1.3 頁 **2026-09-02**（支持正文與 summary 的「9 月 2 日」）。第一輪沒有查這兩個日期，本輪補上。

## 2. A 組：第一輪改過的 10 處，逐處覆核

| # | 第一輪改動 | 本輪判定 | 依據 |
| --- | --- | --- | --- |
| A1 | 第一段「（台北時間，美國時間 9 月 8 日）」 | ✓ 維持 | `datePublished` 2026-09-08T19:00:51Z、頁面自印 September 8, 2026 |
| A2 | 否定句移到第二段並改寫 | △ 再改 | 見改動 R1（頁尾地區選單實際列出 7 個國家） |
| A3 | 刪掉「這是官方自己的用詞……」 | ✓ 維持 | 刪除，未新增任何事實；`自稱` 仍完成歸因 |
| A4 | 一次性卡號改寫並歸因 | ✓ 維持 | 安全長文第 93 行「a single-use card number is issued, and that's what gets passed through to the merchant's website, rather than your regular credit card」，逐字對回 |
| A5 | 1Password 由「登入代填」改「登入支援」 | ✓ 維持 | 發表稿第 249 行「Shop Pay is coming soon as another way to pay, along with 1Password support so Muse can use logins a person already has」——`coming soon` 涵蓋兩者，官方確實沒有寫「代填」 |
| A6 | 表格 header 改「官方說法」、caption 補產品設計說明 | ✓ 維持 | 第一列用字確實出自設計說明第 19 行「search, navigate sites, fill out forms, and complete transactions, like booking and purchasing」 |
| A7 | bug bounty 補回限定詞、刪一個歸因詞 | △ 再改 | 見改動 R4（限定詞補得比原文強）與 R6（同段仍有四個歸因詞） |
| A8 | 訓練／存取拆成兩段 | △ 再改 | 拆段本身正確（限定詞一個都沒少），但「去識別化」比原文強，見改動 R3 |
| A9 | 「發表稿列出的入口只有這幾個」＋改寫台灣管道那句 | △ 再改 | 封閉清單改寫正確；新寫的否定句沒有限定對象，見改動 R5 |
| A10 | `hero_label`「只在美國上線的個人代理」 | ✓ 維持 | 發表稿只寫 rolling out in the US，四頁無任何其他地區時程 |

## 3. B 組：第一輪**新寫進去**的句子，逐句回原文

| # | 新句 | 判定 | 依據 |
| --- | --- | --- | --- |
| B1 | 「以下寫的是 2026 年 9 月 23 日查核當天的狀態」 | ✓ | 與 `checked_on`、四條 source、表格 caption、callout 一致 |
| B2 | 「依據是 Meta 的四份官方頁面」 | ✓ | `sources[]` 四條今天全部 200 且讀到正文 |
| B3 | 「這四頁沒有提到台灣、亞洲或美國以外的任何國家」 | △ | **改動 R1**：Newsroom 頁尾地區選單實際印出 Canada／Japan／Korea／India／Brazil／Germany／France（第 428–437 行），語系列另有 Japanese／Korean |
| B4 | 「Meta 說送到商家網站的是一組一次性卡號，不是使用者平常那張信用卡」 | ✓ | 安全長文第 93 行原句；歸因給 Meta 正確 |
| B5 | 「讓 Muse 沿用使用者既有登入資訊的 1Password 支援也是 coming soon」 | ✓ | 發表稿第 249 行 |
| B6 | 表格欄名「1Password 登入支援」 | ✓ | 同上 |
| B7 | 表格 caption 加「Muse 產品設計說明」 | ✓ | 設計說明第 19 行 |
| B8 | 「開放給任何循負責任揭露程序回報問題的人」 | △ | **改動 R4**：原文是 `to anyone to responsibly disclose issues`（副詞），不是一套「程序」 |
| B9 | 「有效回報最高上限是 300,000 美元」 | ✓ | 「The program awards up to $300,000 for valid reports」 |
| B10 | 「這兩個數字都是上限，不是已經付出的金額」 | ✓ | `awards up to`；全篇沒有寫成行情或已付金額 |
| B11 | 訓練段：「官方寫的是會先做去識別化處理再使用」 | △ | **改動 R3**：原文是 `sanitized to remove key personally identifiable information`，`key` 這個限定詞被丟掉 |
| B12 | 存取段：「只用作業政策限制員工存取，並不阻止 Meta 在支援、維安或營運需要時存取資料」 | ✓ | 安全長文第 97 行兩句原文 |
| B13 | 「發表稿列出的入口只有這幾個，而且只在美國」 | ✓ | 發表稿第 268 行；已從封閉清單斷言降為「發表稿列出的」 |
| B14 | 「四頁也都沒有寫美國以外的開放時程、等候名單或申請方式」 | △ | **改動 R5**：Spark 1.3 頁有「Sign up and start building」（Muse Code／Meta Model API 的開發者入口），否定句要限定對象是 Muse |

## 4. C 組：117 條 CONFIRMED 的隨機三分之一（39 條，seed 20260923）

抽中的編號（沿用第一輪報告的編號）：
1, 4, 5, 9, 12, 26, 29, 31, 35, 42, 48, 49, 50, 55, 57, 61, 73, 74, 77, 78, 82, 84, 86, 92, 93, 94, 96, 100,
103, 106, 112, 114, 116, 117, 120, 121, 122, 128, 130。

| 群 | 抽中的編號 | 判定 | 本輪的獨立依據 |
| --- | --- | --- | --- |
| 中介資料 | 1, 4, 5, 9 | ✓ | slug 尾碼＝`news_date` 2026-09-09＝DELTA-4-4 第 3 條表列（第 28 行）；台北換算；頁面第 235 行雙日期；`checked_on` 四處程式比對一致 |
| 標題／描述 | 12, 26 | ✓ | 發表稿第 268 行 `rolling out in the US`；四頁金額重掃只有 bug bounty 兩筆 |
| 第一段 | 29, 31, 35 | ✓ | 第 247–248 行；完整入口句在 JSON-LD articleBody 命中 1 筆；DELTA-4-4 第 2 條那句逐字相符 |
| Muse 做什麼 | 42, 48, 49, 50, 55, 57, 61 | ✓ | 第 239 行 `It doesn't just answer questions, it actually does the work.`；第 244 行 `in the Muse app or directly in WhatsApp`；第 260 行連接器授權；設計說明第 34 行預設放行與可調整；第 19 行瀏覽器能力；發表稿第 249 行 Link |
| 安全架構 | 73, 74, 77, 78 | ✓ | 第 257 行 Sentinel 兩句；第 258 行 `no visibility into people's passwords`＋`including passwords a person types into the browser themselves` |
| 界線 | 82, 84, 86, 92, 93, 94, 96 | ✓ | 安全長文第 105 行提示詞注入未解；第 12 行兩筆上限；第 103 行 opt-out 開關；第 97 行作業政策兩句；第 99 行外部稽核仍在進行、查核當天無結果可讀 |
| 價格 | 100 | ✓ | 四頁重掃 `$`／USD／price／pricing／subscription／per month，只有 bug bounty 兩筆與「free for most of what people need」一句 |
| FAQ | 103, 106, 112, 114 | ✓ | 分別對回 22／39、65、81／82、`not_said` 第 9 條（四頁皆無失敗率與責任歸屬） |
| callout | 116, 117 | ✓ | 兩份來源都在 `sources[]`；只有一個一般 callout，沒有投資免責 callout |
| 連結／來源 | 120, 121, 122 | ✓ | 兩個結尾連結文字**逐字等於**目標內容包現行 zh-TW `title`（程式比對，索引篇也已存在）；四條 source 今天皆 200 |
| 圖解 | 128, 130 | ✓ | 安全長文第 42 行 `Muse proposes actions, but only Sentinel can grant permission`；發表稿第 259 行寄信／付款前確認 |

抽樣 39 條全部 CONFIRMED。**抽樣之外另有兩條被連帶查到而改掉**（第一輪編號 91、107），
因為它們分別落在第一輪改過的段落（A8）與同一個否定句的 FAQ 版本，屬於 A 組的相依檢查。

## 5. 改掉的 11 條（9 處精確字串取代）

| # | 位置 | 原文 → 改成 | 來源原文 | 為什麼 | URL |
| --- | --- | --- | --- | --- | --- |
| R1 | 第二段 | 「這四頁沒有提到台灣、亞洲或美國以外的任何國家。」→「這四頁的內文沒有提到台灣，也沒有寫美國以外的任何上線地區。」 | Newsroom 第 428–437 行頁尾地區選單：Brazil／Germany／France／Japan／Korea／Canada／India | 頁面上確實印著這些國名（其中三個在亞洲），否定句得限縮到「內文」與「上線地區」；`must_not_write` 第 17 條本來就說頁尾選單不是上線地區的證據 | about.fb.com |
| R2 | FAQ 2 | 「四份官方頁面都沒有提到台灣、亞洲或其他地區，也沒有寫任何開放時程。」→「四份官方頁面的內文都沒有提到台灣，也沒有寫美國以外的上線地區或開放時程。」 | 同上 | 同一個過寬的否定句，FAQ 版本第一輪判為 CONFIRMED | about.fb.com |
| R3 | 訓練段 | 「官方寫的是會先做去識別化處理再使用」→「官方寫的是會先移除主要的個人識別資訊再使用」 | 「these trajectories are sanitized to remove **key** personally identifiable information before being used in training」 | `key` 是限定詞，被丟掉就變成「完整去識別化」，比廠商自己寫的還強 | research.meta.ai 安全長文 |
| R4 | 界線第一段 | 「開放給任何循負責任揭露程序回報問題的人」→「開放給任何願意負責任揭露問題的人」 | 「Today, we're opening the Muse bug bounty program to anyone **to responsibly disclose issues**」 | 原文是副詞，不是一套既定「程序」；第一輪補限定詞時補得比原文具體 | research.meta.ai 安全長文 |
| R5 | 台灣讀者段 | 「四頁也都沒有寫美國以外的開放時程、等候名單或申請方式。」→「四頁也都沒有寫 Muse 在美國以外的開放時程、等候名單或申請方式。」 | Spark 1.3 頁 Availability 區有「Sign up and start building」（Muse Code／Meta Model API） | 那是模型的開發者入口、不是 Muse 的申請管道；否定句要限定對象 | research.meta.ai Spark 1.3 |
| R6 | 界線第一段 | 四個歸因詞（安全長文自己劃出界線／文中寫／並且說／同一篇文章也提到）→ 兩個（安全長文自己劃出界線／同一篇文章寫） | — | FACTCHECK-44「任一正文段落至多兩個歸因詞」；**一個限定詞都沒有刪**，只把重覆的「文中寫」「並且說」還原成直述 | — |
| R7 | 憑證段 | 「技術長文另外補充」→「安全長文另外補充」 | 同一份 `sources[2]` 在別處都叫「安全長文」 | 正文自己說「四份官方頁面」，多出一個「技術長文」會被讀成第五份文件 | research.meta.ai 安全長文 |
| R8 | 界線第一段 | `Muse isn't immune to attack` → `Muse isn’t immune to attack` | 安全長文第 105 行原字元為 U+2019 | **協調者裁示 1** | research.meta.ai 安全長文 |
| R9 | `sources[0].title` | `The World's First…` → `The World’s First…` | 頁面 `<title>` 與正文均為 U+2019 | **協調者裁示 1** | about.fb.com |
| R10 | H2 標題 | 「Muse 不是 Muse Spark：代理與模型的差別」→「Meta 這次發表的 Muse 是什麼」 | — | **協調者裁示 2**：模型／產品的區別退出標題 | — |
| R11 | summary 第 2 點 | 「驅動 Muse 的是 4 月已經介紹過的模型 Muse Spark，9 月 2 日發布的 1.3 版是目前這一版，兩者是模型與產品的關係。」→「Meta 表示 Muse 由 Muse Spark 驅動，目前這一版是 9 月 2 日另外發表的 1.3，那是一次獨立的模型更新。」 | Spark 1.3 頁 `datePublished` 2026-09-02、正文「available today in Muse Code and in Meta Model API」 | **協調者裁示 2**：區別退出 summary | research.meta.ai Spark 1.3 |

改完以程式複核裁示 2：模型／產品的區別只剩 `block[4]`（帶 `article` inline 的那一句內文）與 `block[26]`（FAQ 第 1 題）兩處；
`summary` 裡的 9、2、1.3 仍全部出現在正文（`check_article.py` 的數字規則）。
改完以程式複核裁示 1：全文 ASCII 撇號 0 個、U+2019 2 個。

## 6. 讀者優先與界線（本輪重掃）

- 全篇 **0 個「本文」**、0 個「最近／本週／日前／這幾天／近日」。
- `title` 45 字、`description` 129 字且句尾「（2026 年 9 月查證）」、沒有查證流水帳；標題／描述／summary 都沒有選錄篇數。
- 歸因密度：開頭段 1 個（「官方原文寫的是」；「Meta 在 Newsroom 發表」是事件主詞不是歸因），
  改後每一個正文段落 ≤ 2 個。改動前「界線在哪裡」第一段有 4 個，是本輪唯一超標處。
- 段落總字數 2,531 → **2,537**（規格 1,800–3,000）；每節 2–4 段不變。
- 界線：不帶 `finance` 主題、只有一個一般 callout、沒有投資免責 callout；沒有購買／訂閱／升級建議；
  沒有推定台灣可用；沒有繞過地區限制的方法；沒有 benchmark 名稱或分數、沒有 `~20% fewer tool calls` 那組數字；
  沒有 Meta One 的關聯；沒有引用 muse.ai 首頁獨有的說法（Mac 版、該頁對 Link 保障的措辭）；
  沒有 Link 保障條款細節；沒有引用 ElevenLabs 朗讀字串；沒有把頁尾地區選單當成上線地區證據；
  廠商宣稱（Secure VM、Sentinel、一次性卡號、`The World’s First`、`most capable model to date`）全部有歸因。
- `must_not_write` 第 8、9、10 條的三個必寫點都在：廣告兩句同段、訓練預設與開關、
  `Muse isn’t immune to attack` 與提示詞注入未解。

## 7. 留給協調者的事

1. **「Meta 把安全架構寫得比一般發表稿詳細很多」**（第 14 段）是本站對「一般發表稿」的比較，四頁都沒有來源可查。
   第一輪已提出、協調者未裁示，本輪同樣不自行更動。若要拿掉，建議改成「Meta 另寫了一篇安全長文講架構」這種可查證的寫法。
2. **bug bounty 的兩段原文不同**：安全長文開頭摘要那段寫 `up to $300,000`、其中 `up to $130,000` 對「影響單一使用者」的提示詞注入；
   正文那段只寫 `up to $300,000`、`based on demonstrated impact`，**沒有 130,000**。文章用的是摘要那一段，正確；
   是否要補上 `based on demonstrated impact` 這個條件，請協調者決定。
3. **`surrogate token` 譯「替身憑證」**（研究紀錄 `overlaps` 第 5 條用的是「替身權杖」）。同一句裡 real credential 也譯「憑證」，
   對應關係與原文一致，語意不差，未改；若要全批統一譯詞請一次處理。
4. **研究紀錄 `not_said` 第 2 條的措辭**寫「唯一出現的 Canada／United States 字串是頁尾選單」，
   實際上頁尾還有 Japan、Korea、India、Brazil、Germany、France。正文已按 R1／R2 限縮，但研究紀錄那條建議一併修正。
5. 圖檔尚未產生：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug，`pack_cli lint` 的 `image_missing`×2 與
   `raw_internal_url`×1 都還在（預期內）。

## 8. 自檢輸出（原樣）

```
check_article exit=0
OK ai-news-meta-muse-agent-20260909 zh-TW paragraphs 2537
```

```
pack_cli lint exit=1
ai-news-meta-muse-agent-20260909
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-meta-muse-agent-20260909/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-meta-muse-agent-20260909/diagram-1.svg
1 entries checked
```

退出碼寫在 `C:\Users\x8120\mokaair-work\news44\_tools\ai-news-meta-muse-agent-20260909-r2\check.exit`
與 `lint.exit`；輔助腳本（重抓、抽字、引句比對、機械檢查、改稿與寫入 `factcheck.second_round`）在同一個目錄。

## 9. 結論

**ok**。本輪查 63 條、改 11 條（9 處取代）：4 條是協調者的兩項裁示，5 條是限定詞與否定句範圍（R1–R5），
2 條是歸因密度與來源名稱（R6、R7）。沒有動任何日期、金額、機制名稱或骨幹論述，
兩個結尾連結、表格數值、圖解四格與 `hero_label` 均未更動。只動了內容包與研究紀錄兩個檔，沒有執行任何 git 指令。

（第 7 節的四個未決事項已由協調者裁示並於同日套用，見下方「追加」一節；第 8 節的自檢輸出以追加一節的為準。）

## 追加：協調者對第 7 節四個未決事項的裁示（同日套用）

協調者在第二輪交件後對第 7 節第 1–4 項逐一裁示，本節記錄套用結果：內容包 3 處精確取代、研究紀錄 1 處改寫，
四條裁示都已寫進研究紀錄 `factcheck.second_round.coordinator_rulings`（該陣列現有 10 條）。

| # | 裁示 | 原文 → 改成 | 依據 |
| --- | --- | --- | --- |
| S1 | 「Meta 把安全架構寫得比一般發表稿詳細很多」沒有來源，改成「Meta 另外發表了一篇安全長文說明架構」這個可查證的事實陳述，歸因、不做比較 | 第 14 段開頭「Meta 把安全架構寫得比一般發表稿詳細很多：」→「Meta 另外發表了一篇安全長文說明這套架構：」 | 發表稿正文的 How We Built Safety Into Muse 超連結轉到 research.meta.ai 那一頁，其 JSON-LD `datePublished` 為 2026-09-08、與發表稿同一天（今日自行重抓核對）。段落其餘文字與「官方稱為 Muse Secure VM」的歸因不動，字數恰好相同 |
| S2 | bug bounty 補上正文那段的條件「依實際影響而定」，兩個數字仍寫成上限 | 「開放給任何願意負責任揭露問題的人，有效回報最高上限是 300,000 美元」→「……的人，金額依實際影響而定，有效回報最高上限是 300,000 美元」 | 安全長文正文段「The program awards up to $300,000 for valid reports, based on demonstrated impact, including successful prompt injection attempts.」；`awards up to` 的上限框架與「不是已經付出的金額」原樣保留，該段歸因詞仍為兩個 |
| S3 | `surrogate token` 內容包一律譯「替身權杖」，與研究紀錄一致 | 第 16 段「代理端拿到的其實是替身憑證」→「……替身權杖」 | 研究紀錄 `overlaps_existing_article` 第 5 條用的就是「替身權杖」；同句裡 real credential 仍譯「憑證」，正好對回原文 `surrogate token` → `real credential` 的區別。改後內容包「替身憑證」0 個 |
| S4 | 研究紀錄 `not_said` 第 2 條改寫：否定句限定在「四頁的文章內文」，頁尾地區選單列齊 | 原「唯一出現的 Canada／United States 字串是……頁尾的地區與語系選單」→ 列出頁尾**十一個**項目並說明正文裡唯一的地區字串是 rolling out in the US | 2026-09-23 對抽出正文第 427–437 行清點：United States (English)、Brazil (Português)、Germany (Deutsch)、France (Français)、Japan (日本語)、Korea (한국어)、Latin America (Español)、Spain (Español)、Canada (English)、EMEA (English)、India (English)；頁首語系列另有 Japanese、Korean。原條目只寫了 Canada／United States 兩個 |

套用後複核：段落總字數 2,537 → **2,547**（規格 1,800–3,000）；第 14 段與第 19 段的歸因詞各 2 個，
仍在「任一正文段落至多兩個」之內；內容包 ASCII 撇號仍為 0、U+2019 仍為 2；「比一般發表稿」字串 0 個；
標題、description、summary、表格、圖解四格、`hero_label` 與兩個結尾連結都沒有再動。

```
check_article exit=0
OK ai-news-meta-muse-agent-20260909 zh-TW paragraphs 2547
```

```
pack_cli lint exit=1
ai-news-meta-muse-agent-20260909
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-meta-muse-agent-20260909/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-meta-muse-agent-20260909/diagram-1.svg
1 entries checked
```

第 7 節第 1–4 項全部結案，沒有新的未決事項（只剩第 5 項的圖檔，等 `_DRAWINGS` 登記）；結論維持 **ok**。
