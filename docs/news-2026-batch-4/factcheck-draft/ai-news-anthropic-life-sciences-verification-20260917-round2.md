# 第二輪（獨立查核）ai-news-anthropic-life-sciences-verification-20260917

> 協調者可整段貼進 `docs/news-2026-batch-4/factcheck-draft/<slug>.md` 的第二節，標題已寫「第二輪」。

- 查核代理：獨立查核代理（第二輪），未參與撰稿、未參與第一輪
- 查核日：2026-09-23（台北），重抓時刻 01:21
- 垂直／順序：AI／`display_order` 173；事件日 2026-09-17；`kind` life
- 第一輪報告：`ai-news-anthropic-life-sciences-verification-20260917-round1.md`（130 條主張、10 處修正）
- 依據：`FACTCHECK-47.md`、`agents/ai/SECOND-ROUND.md`、`agents/ai/FACTCHECK.md`、`DELTA-4-7.md`、指派訊息的四條協調者裁定
- 輔助腳本：`C:\Users\x8120\mokaair-work\news47\_tools\ai-news-anthropic-life-sciences-verification-20260917-r2\`
  （`extract.py`、`verify_quotes.py`、`check37.py`、`paras.py`、`sample.py`、`mech.py`、`apply_edits.py`、`fix_p15.py`、`append_second_round.py`）

## 1. 來源重抓（2026-09-23 台北 01:21）

全部用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒；
UA、標頭、查詢字串都沒有帶任何人的姓名或 email；沒有填寫或送出任何表單（只做 GET）。

| # | 來源 | 狀態 | bytes | 讀到正文 | 與第一輪 01:03 的差異 |
| --- | --- | --- | --- | --- | --- |
| S1 | `https://www.anthropic.com/news/life-sciences-verification-program` | 200 | 173,459 | 是，六個小節全部 | 純文字逐行 diff 與撰稿代理 00:28 抓到的只差一個行尾空白 |
| S2 | `https://www.anthropic.com/news` | 200 | 460,541 | 是，本篇仍標 `Sep 17, 2026` + `Announcements` | 與第一輪相同（活頁面，精選卡片仍是 9/22 的 Opus 5.5） |
| S3 | `https://www.anthropic.com/threat-intelligence-report-september-2026` | 200 | 1,221,782 | 是，`seven harm areas` 與生物誤用整節 | 與第一輪相同 |
| S4 | `https://claude.com/form/life-sciences-verification-program` | 200 | 441,344 | 是，方案說明與資格說明 | 與第一輪相同；與撰稿代理 00:30 的 441,311 只差資格句那一行（見裁定 1） |

**逐行 diff 的結論（`_raw` 的撰稿版 vs 本輪 01:21）：S4 全頁只有第 199 行變了，就是資格句；S1 一字未變。**
所以第一輪報的「申請頁當天改字」屬實，不是撰稿代理捏造。

`verbatim_quote` 連續字串比對（`verify_quotes.py`，47 條）：**改完之後 46 條命中**。
唯一沒命中的 `verified_facts[37]` 是比對腳本的假陽性——那條引文在 `news-index.html` 的 RSC payload 裡是反斜線跳脫的原樣，
`check37.py` 用原樣比對確認 `True`；研究紀錄自己已經寫明「比對要對 .html」。

## 2. 覆核第一輪改過的 10 處（全部成立）

| # | 位置 | 第一輪改成 | 一手來源原文 | 第二輪判定 |
| --- | --- | --- | --- | --- |
| 1 | 第 4 段 | 已有數十個組織透過早期存取**加入** | S1 `We have already onboarded dozens of organizations through an early-access program` | 成立 |
| 2 | 第 4 段 | 公司預期第一週**納入**數百個組織 | S1 `We expect to enroll hundreds of organizations within the first week` | 成立（`enroll`＝納入，且未寫成增量） |
| 3 | 第 5 段 | 刪掉「都」 | S3 `we have launched recent models (most notably Claude Fable 5) with stronger safeguards` | 成立（原文無全稱語氣） |
| 4 | 第 6 段 | **9 月 17 日當天**適用 Mythos 5.1、Opus 5 與 Sonnet 5 | S1 `Standard Use grants apply to Mythos 5.1, Opus 5, and Sonnet 5 today`；頁面自印 `Sep 17, 2026` | 成立 |
| 5 | 表頭第 3 欄 | 適用模型／方案（**依 9 月 17 日公告**） | 四列內容逐格回 S1 均命中 | 成立 |
| 6 | 第 9 段 | 刪掉「唯一的」 | S1 `(except while using Claude Code with API authentication)` | 成立 |
| 7 | 第 10 段 | **受保護**健康資訊（PHI） | S1 `customers with PHI data should use separate non-BAA orgs with non-HIPAA` | 成立（PHI＝Protected Health Information；S1 未自行展開，但同句的 HIPAA 語境支持此展開） |
| 8 | 第 14 段 | **可以把案例交給**組織的管理員 | S1 `we **can** flag these cases to organization admins to take action within pre-agreed timeframes` | 成立（`can` 的能力語氣保住） |
| 9 | FAQ 4 | 同上 | 同上 | 成立 |
| 10 | FAQ 3 | **Anthropic 說**這能滿足大多數日常工作 | S1 `Standard Use grants are suitable for most life science work`＋`we expect Standard Use to cover the majority of access needs` | 成立（新增的歸因子句可回原文；`daily` 出自 `diverse, daily workloads`） |

**第一輪新寫進去的句子只有兩處**（第 10 處的歸因子句、第 5 處的表頭字串），兩處都逐字回到 S1，見上表。
其餘 8 處是刪字或換詞，沒有新增未查證的內容。

## 3. 隨機抽查的 CONFIRMED（`random.seed(20260923)`，119 取 39）

抽到的號碼（沿用第一輪編號）：
1, 4, 5, 8, 11, 26, 28, 30, 33, 41, 47, 49, 50, 53, 55, 59, 69, 70, 73, 74, 78, 79, 81, 89, 90, 91, 93, 96, 100, 104, 110, 112, 115, 119, 120, 122, 126, 127, 129。

| # | 主張 | 覆核依據 | 判定 |
| --- | --- | --- | --- |
| 1 | LSVP 的名稱與定位 | S1 第一句 | C |
| 4 | title 與研究紀錄 `title` 逐字相同 | 程式比對 True | C |
| 5 | description 的日期與主體 | S1＋S2 的 `Sep 17, 2026` | C |
| 8 | 兩種授權的三項差異 | S1 兩節 | C |
| 11 | slug 後綴＝`news_date`＝第一段日期 | 程式比對 True | C |
| 26 | summary：標準用途整個團隊／一年／三個型號 | S1 | C |
| 28 | summary：離線監測、30 天、組織自訂、管理員限時 | S1 四句 | C |
| 30 | summary ⊆ 正文 | `check_article.py` OK | C |
| 33 | 學術實驗室到新創、藥廠「等等」 | S1 `from academic labs to startups, pharma companies, and more` | C |
| 41 | 威脅報告顯示濫用嘗試含生物武器 | S1 `As we've shown in our recent threat report…` | C |
| 47 | 一年續約一次 | S1 `renewed once a year` | C |
| 49 | 未來新模型也納入 | S1 `and to future models as they launch` | C |
| 50 | 涵蓋範圍清單以「等等」收尾 | S1 `basic science, R&D, … investing and diligence, and more`，順序一致 | C |
| 53 | 高風險是附加授權 | S1 `add-on grant` | C |
| 55 | 六個月續約 | S1 `must be renewed every six months` | C |
| **59** | 高風險「**目前**可以用在 Opus 5 與 Sonnet 5」 | S1 `High-risk grants for Claude Opus 5 and Claude Sonnet 5 are available **today**`，today＝9/17 | **CH**（見第 4 節第 7 處） |
| 69–70 | 表格第 2 列 | S1 | C |
| 73–74 | 表格第 3 列（個人方案不符資格） | S1＋S4（今日仍寫 `Free, Pro, and Max plans are not eligible at this time`） | C |
| 78 | caption 含查核日、56 字（≤200） | 程式比對 | C |
| 79 | 只給團隊與機構 | S1＋S4 | C |
| 81 | API 與 Claude Science 可原生切換 | S1 | C |
| 89 | 申請頁沒印日期 | S4 全頁無日期，頁尾 `© [year] Anthropic PBC` | C |
| 90 | 兩個時點分開寫，未寫成「更新了公告」 | `must_not_write` 第 8 條 | C |
| 91 | alt 四格＝研究紀錄 `diagram.nodes` | 逐項比對 | C |
| 93 | 即時阻擋的定義 | S1 `real-time blocking, where we reject … at the time of each request` | C |
| 96 | 30 天保留只限 LSVP 流量 | S1 `For LSVP traffic, we are requiring data retention for 30 days` | C |
| 100 | 申請書像職缺公告、不放敏感資訊或 IP | S1 | C |
| 104 | 兩頁未提開放地區與台灣 | `taiwan`／`台灣` grep 各 0；`region` 命中只有頁尾導覽的 `Regional compliance` | C |
| 110 | 管理員填表、Anthropic 評估、不保證 | S4 兩句（今日仍在） | C |
| 112 | 威脅報告的七類濫用 | S3 `seven harm areas: cyber operations, … and distillation` | C |
| 115 | FAQ 1 的「不會」 | S1 | C |
| 119 | FAQ 3 的高風險條件 | S1 | C |
| 120 | FAQ 4 的交換條件 | S1 | C |
| 122 | FAQ 5 的兩個時點 | S1／S4 | C |
| 126 | callout 的台灣否定句 | S1／S4 grep | C |
| 127 | 只有一個 callout、無免責 callout | 程式計數 1 | C |
| 129 | 第二個連結 text 逐字＝目標包 zh-TW title | 程式比對 True | C |

**抽查 39 條：38 條維持 CONFIRMED，1 條（第 59 條）改為 CHANGED。**

兩個結尾連結 text 都與目標內容包的 zh-TW `title` **逐字相同**（程式比對，兩條皆 True）。

## 4. 第二輪改掉的 8 處（before → after）

| # | 依據 | 位置 | before | after | 來源 |
| --- | --- | --- | --- | --- | --- |
| 1 | 裁定 1 | 正文第 10 段（新增一句） | （只寫到 9/17 公告當下的第一方 console／Enterprise／Team） | 申請頁 9 月 23 日寫的資格是 Claude Enterprise 與 Team 方案，以及 Claude Platform（API），Free、Pro、Max 方案不符資格。 | S4 |
| 2 | 裁定 1 | callout | 生命科學驗證方案**目前只開放通過驗證的團隊與機構，在 Team 與 Enterprise 方案申請**；一般的 Free、Pro、Max 方案與第三方平台都還沒有這個選項。 | 生命科學驗證方案只開放通過驗證的團隊與機構；**申請頁 9 月 23 日寫的資格是 Claude Enterprise 與 Team 方案，以及 Claude Platform（API）**，一般的 Free、Pro、Max 方案不符資格，第三方平台也還沒有這個選項。 | S4 |
| 3 | 裁定 2 | 正文第 3 段 | 公告舉的例子有**藥物開發**、研究生物學、臨床開發與製造 | 公告舉的例子有**藥物發現（drug discovery）**、研究生物學、臨床開發與製造 | S1 `like drug discovery, research biology, clinical development, and manufacturing` |
| 4 | 裁定 2 | 正文第 11 段 | Mythos 5.1 用在生物與**藥物開發** | Mythos 5.1 用在生物與**藥物發現** | S4 `Mythos 5.1 for biology and drug discovery` |
| 5 | 裁定 2 | FAQ 第 5 題 | 同上 | 同上 | S4 |
| 6 | 裁定 3 | 正文第 15 段 | 以 2026 年 9 月 23 日查核，公告頁與申請頁都沒有說明任何國家或地區的開放條件，也沒有提到台灣；……兩頁都沒有寫，**不能用「Team 與 Enterprise 方案在台灣買得到」去推論這個方案在台灣是否開放**。 | 以 2026 年 9 月 23 日查核，公告頁與申請頁都**沒有交代哪些地區的組織可以申請**，也沒有提到台灣；……這兩頁都沒有寫。 | S1／S4（兩頁 `taiwan`／`台灣` grep 皆 0） |
| 7 | 第二輪自己找到 | 正文第 8 段 | 高風險用途**目前**可以用在 Claude Opus 5 與 Claude Sonnet 5 上 | 高風險用途**在 9 月 17 日當天**可以用在 Claude Opus 5 與 Claude Sonnet 5 上 | S1 `High-risk grants for Claude Opus 5 and Claude Sonnet 5 are available today` |
| 8 | 裁定 4 | 正文第 4 段 | 之後幾週擴大到涵蓋多數生命科學社群，但這是**官方**當天寫下的預期 | 之後幾週擴大到涵蓋多數生命科學社群，但那是 **9 月 17 日**當天寫下的預期 | S1（同段仍有「Anthropic 說明」「公司預期」兩個歸因） |

第 7 處是**第一輪漏掉的同型錯誤**：第一輪已經把標準用途的 `today` 改成「9 月 17 日當天」（其第 4 處），
但高風險授權那一句的 `today` 留成了「目前」。文章後段自己寫申請頁在 9/23 列的是 Opus 5.5，
留著「目前」就會落回 `must_not_write` 第 8 條要避免的日期混用。

**研究紀錄同步改了 7 處**（都寫進 `factcheck.second_round.record_edits`）：
`sources[3]` 的 `verbatim_quote`／`fetched_at`／`bytes` 換成 01:21 的版本、`sourcing_notes` 補記第二輪四個 bytes 與這一句的改動、
`verified_facts[40]` 的 `fact` 與引文、`live_data_warnings[3]` 的資格句現況、`verified_facts[4]`／`[43]` 的譯名、
`unverified_or_excluded[1]` 刪掉台灣方案供應的前提。

## 5. 四條協調者裁定的落實

1. **申請頁 9/23 改字**：已重抓確認（逐行 diff 只有那一行變）。研究紀錄 `sources[3]` 的 `verbatim_quote` 換成
   `LSVP is currently available to verified organizations on Claude Enterprise and Team plans, and the Claude Platform (API). Free, Pro, and Max plans are not eligible at this time.`，
   `fetched_at` 改 `2026-09-23T01:21:00+08:00`、`bytes` 改 `441344`（引文與它出自的那次抓取必須一致），
   `sourcing_notes` 補一句說明；`verified_facts[40]` 同步，並寫明 00:30 的舊句與兩份 HTML 都留著。
   正文第 10 段與 callout 都改成含 **Claude Platform（API）** 並標「申請頁 9 月 23 日」。
   **表格第三欄與正文「發布當下」那一句仍屬 9/17 公告的說法，維持不動**——那是另一個時點，不是同一句話。
2. **`藥物發現（drug discovery）`**：正文第 3 段（第一次出現，帶英文）、正文第 11 段、FAQ 第 5 題三處都改；
   研究紀錄 `verified_facts[4]`、`[43]` 同步。與 `clinical development`＝「臨床開發」已經分得開。
   英文只在第一次出現時帶一次，若站主要三處都帶，再加 28 字，字數仍在上限內。
3. **刪掉台灣方案供應的前提**：正文第 15 段改寫成「公告頁與申請頁都沒有交代哪些地區的組織可以申請」，
   不再引用「Team 與 Enterprise 方案在台灣買得到」。研究紀錄 `unverified_or_excluded[1]` 一併改掉，
   免得下一輪又從那裡搬回正文。
4. **歸因密度**：逐段盤點 17 段（人工判讀，不只靠字串）：

   | 段 | 歸因詞 | 數 |
   | --- | --- | --- |
   | P01（前言首段） | — | **0**（≤1 合格） |
   | P02 | 依據 Anthropic 的公告頁／都是 Anthropic 自己的說法 | 2 |
   | P03 | Anthropic 表示／公告舉 | 2 |
   | **P04** | Anthropic 說明／公司預期／~~官方~~ | **3 → 2（已改）** |
   | P05 | 報告顯示／Anthropic 也提到 | 2 |
   | P06 | Anthropic 說／公司預期 | 2 |
   | P07 | 公告給的情境 | 1 |
   | P08 | Anthropic 說／公告列出 | 2 |
   | P09 | Anthropic 說 | 1 |
   | P10 | 申請頁 9 月 23 日寫的 | 1（本輪新增那一句帶來的） |
   | P11 | 公告寫／申請頁寫的是 | 2 |
   | P12 | Anthropic 說明 | 1 |
   | P13–P17 | — | 0 |

   只有 P04 超過「每段至多兩個」，已把第三個（「官方」）改寫成日期直述。其餘各段 0–2，全部合格，因此沒有再動。
   **廠商宣稱的歸因一個都沒有刪**（`公司預期`、`Anthropic 說`、`公告列出` 全部保留），
   限定詞與但書（`can`、`beta`、`over time`、`不是完整清單`、`資安分類器等其他防護不受影響`）也全部原地不動。

## 6. 讀者優先與垂直界線（改完後重掃）

- 正文「本文」**0 次**；「最近」「近日」「本週」「日前」各 **0 次**；「買得到」**0 次**；「藥物開發」**0 次**。
- 正文「官方」**0 次**（第一輪那 1 次已隨裁定 4 改掉）；全篇只有 `sources[]` 兩條標題裡各有一個「官方」，屬來源描述。
- `description` 168 字，句尾只有「（2026 年 9 月查證）」；title／description／summary 無清點數字。
- 否定句全部限縮在「這兩頁、2026-09-23」：第 15 段、第 16 段、summary 第 5 句、FAQ 第 2 題、callout 五處都是。
- AI 垂直界線：不帶 `finance` 主題（`topics` 為 `ai`／`software`／`ai-news`）、只有 1 個 callout、沒有免責 callout、
  沒有購買或升級建議、沒有金額、沒有「首創／唯一／業界第一」，beta／預期／尚未支援三種狀態都在。
- 段落字數 2,869 → **2,946**（上限 3,000，餘 54 字）。每節 2–4 段不變。

## 7. 留給協調者的事

1. **字數只剩 54 字餘裕。** 之後若要再補句子（例如裁定 2 的英文要三處都帶），建議先精簡第 3 段
   「原文用「像」帶出例子，不是完整清單」與第 8 段「同樣是舉例，不是完整清單」其中一處的重複敘述，**不要動但書或限定詞**。
2. **`verified_facts[37]` 會讓通用比對腳本永遠報一次假陽性**（RSC payload 的反斜線跳脫引文，只能對 `.html` 原樣比對）。
   研究紀錄自己已註明；若之後要跑第三輪，比對腳本要對這一條做例外。
3. **Opus 5.5 已有自己的發布日**（新聞總覽頁的 2026-09-22 卡片）。這一篇沒有引用那張卡片，
   「申請頁沒印日期」的說法不受影響；`claude-model-lineup-2026` 的時效問題照 `live_data_warnings` 第 6 條另開維護票。
4. **申請頁是活頁面，而且本篇查核當天就改過一次。** 正式站上線前若還會再查一次，請特別重抓 S4 的資格句與型號句。
5. 圖還沒畫、`relink` 還沒跑（`_DRAWINGS` 依 DELTA-4-7 第 15 條要等定稿），`pack_cli lint` 的 exit 1 由這兩項造成。

## 8. 自檢輸出（原樣）

```
OK ai-news-anthropic-life-sciences-verification-20260917 zh-TW paragraphs 2946
check_article exit=0
```

```
ai-news-anthropic-life-sciences-verification-20260917
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-anthropic-life-sciences-verification-20260917/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-anthropic-life-sciences-verification-20260917/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

```
verify_quotes: checked 47 quotes, 1 problems
  （唯一那 1 條是 verified_facts[37] 的比對假陽性，check37.py 原樣比對 True）
```

exit code 檔：`_tools/ai-news-anthropic-life-sciences-verification-20260917-r2/check_article.log`、`pack_lint.log`、`quotes.log`。

## 9. 結論

- **統計：第二輪重查 49 條主張（第一輪改的 10 條全部＋隨機三分之一的 CONFIRMED 39 條）——維持 CONFIRMED 48、CHANGED 1（第 59 條）、NOT FOUND 0。**
  另外執行 47 條 `verbatim_quote` 連續字串比對與 17 段歸因密度盤點。
- **內容包改 8 處、研究紀錄改 7 處**：6 處落實協調者裁定、1 處是第二輪自己找到的日期歸屬錯誤、1 處是裁定 4 的風格調整。
- 第一輪那 10 處修正**全部經重抓原文覆核成立，沒有一處被推翻**；第一輪新寫進去的兩處字句也都能逐字回到 S1。
- 骨幹敘述（兩種授權的條件、資安分類器不鬆動、Mythos 高風險仍限少數機構、BAA／PHI、離線監測與 30 天保留、
  官方頁沒有交代開放地區）全部未動。
- 結論：**`ok`**。不需要第三輪；剩下的是繪圖、`relink` 與第 7 節那五件協調者事項。
