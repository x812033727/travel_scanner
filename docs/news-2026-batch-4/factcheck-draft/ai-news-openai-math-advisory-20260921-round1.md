# `ai-news-openai-math-advisory-20260921` 查核報告（第一輪）

- 查核者：independent factcheck agent, round 1（沒有參與撰稿）
- 查核日：2026-09-23
- 垂直／順序：AI，`display_order` 171，事件日 2026-09-21
- 內容包：`apps/api/app/guides/content/ai-news-openai-math-advisory-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-math-advisory-20260921.json`
- 結論：**needs_second_round**（依 DELTA-4-7 第 12 條第二輪本來就必做；本輪改了 13 處事實／表述、8 處漏空格，其中標題與「普林斯頓」動到骨幹表述）

## 1. 來源重抓結果（2026-09-23 01:03–01:04 台北）

四條都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒，
任何請求的 UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料。

| # | URL | HTTP | bytes | 抽出正文 | 是否讀到正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://openai.com/index/advisory-group-on-mathematics-and-ai/` | 200 | 370,896 | 4,942 字元 | 是（全篇＋九位成員名單） |
| 2 | `https://agmai.org/` | 200 | 67,830 | 2,508 字元 | 是（Purpose／Independence／Members／Current Task 四節全文） |
| 3 | `https://mathandai.org/` | 200 | 10,873 | 6,290 字元 | 是（宣言全文、發表日、DOI、27 位費爾茲獎得主名單） |
| 4 | `https://openai.com/index/navier-stokes-solution/` | 200 | 457,098 | 11,975 字元 | 是（含 2026-09-10 更新註腳） |

- `openai.com/index/*` 本輪兩次請求都沒有 403，不需要改走替代管道。
- bytes 與研究紀錄寫的略有出入（370,857→370,896、67,957→67,830、457,104→457,098），是 Next.js 每次建置的 chunk 清單與 WordPress.com 的 nonce 不同所致。
  把撰稿代理 00:26–00:28 存下的 `_raw/.../*.txt` 與我 01:03 的版本**正規化空白後逐字比對，四頁完全相同**——這段期間來源沒有改動，
  所有「截至查核當天」的狀態句今天仍然成立。
- 沒有開啟、沒有填寫、沒有送出 agmai.org 的意見表單（`/input`）；沒有開啟 mathandai.org 的 Endorsers 分頁。

## 2. 主張表（101 條）

判定：C＝CONFIRMED、CH＝CHANGED、NF＝NOT FOUND（已改寫）、S＝排版（非事實）。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | 「OpenAI 的」數學顧問小組 | **CH** | agmai：`This group operates independently of any AI company`；OpenAI：`mathematicians who have established an independent…group` |
| 2 | title | 小組是獨立的 | C | `The group will operate independently from OpenAI` |
| 3 | title | 能公開意見 | C | `make its advice public` |
| 4 | title | 不管內部進度 | C | `will not be responsible for advising us on how to pace our internal progress` |
| 5 | desc | 2026-09-21 OpenAI 公告 | C | 頁面印 `September 21, 2026`、分類 Company |
| 6 | desc | 「將與」一群數學家合作 | **CH** | 原文為現在進行式；agmai 的 Current Task 也寫已在進行 |
| 7 | desc | 這群數學家已自行成立獨立顧問小組 | C | `who have established an independent mathematics advisory group` |
| 8 | desc | 起因是未發布內部模型解出超過 100 題 | C | `this model has now resolved more than 100 long-standing open problems` |
| 9 | desc | 小組能建議如何發布、評估結果重要性 | C | `help OpenAI assess their significance, advise on how to coordinate their dissemination` |
| 10 | desc | 不負責建議調整內部進度節奏 | C | `Importantly, the group will not be responsible…` |
| 11 | desc | 也沒有決策權 | C | agmai：`we do not have decision making power at any AI company` |
| 12 | desc | 結尾「（2026 年 9 月查證）」 | C | DELTA-4-7 §14 |
| 13 | desc | 長度 155 字（需 120–200） | C | checker |
| 14 | P1 | 事件日 2026-09-21 = slug 尾碼 = `news_date` | C | 三處一致 |
| 15 | P1 | OpenAI 在官方網站公告 | C | openai.com |
| 16 | P1 | 「將與」 | **CH** | 同 #6 |
| 17 | P1 | 小組全名 Advisory Group on Mathematics and Artificial Intelligence | C | 兩個來源逐字 |
| 18 | P1 | 掛在「普林斯頓」高等研究院 | **NF** | 四條來源全文搜尋 `Princeton` 皆 0 筆；原文只有 `hosted at the Institute for Advanced Study` |
| 19 | P1 | 初始成員九人 | C | 兩個來源各九行，逐行清點一致 |
| 20 | P1 | 模型自 8 月 28 日開始訓練、尚未發布 | C | `On August 28, we began training a new internal model.` |
| 21 | P1 | 解出 Navier–Stokes 千禧年大獎難題 | C | OpenAI 說法，兩頁一致 |
| 22 | P1 | 「不但…還解出超過 100 題」的加總關係 | C | 原文 `In addition to resolving the Navier–Stokes…, this model has now resolved more than 100…`，文章沒有把 N–S 算進 100 題裡 |
| 23 | P1 | 公開信 9 月 11 日發表 | C | `Published 11 September 2026` |
| 24 | P1 | 公開信質疑把解題當成新 AI 系統的評比指標 | C | `negative externalities of solving open problems as a benchmark for new AI systems` |
| 25 | P2 | 查核日 2026-09-23 | C | 與研究紀錄、四條 source、表格 caption 四處一致 |
| 26 | P2 | 「讀的是…」只列三條來源 | **CH** | `sources[]` 四條，且第四條正文有用到（#73） |
| 27 | P2 | 「本站沒有獨立驗證或測試」 | C | 編輯聲明 |
| 28 | S1 | 同 #6、#18（連動） | **CH** | — |
| 29 | S2 | 把 OpenAI 自報成果寫成事實 | **CH** | 研究紀錄標 `is_vendor_claim: true`；已補「OpenAI 表示」 |
| 30 | S3 | 小組三項工作 | C | `The group will advise on the review and communication of emerging results…` |
| 31 | S3 | 引句「不負責建議我們如何調整內部數學進度的節奏」 | C | 逐字對得上 |
| 32 | S4 | 沒有決策權、責任仍在公司 | C | agmai 逐字 |
| 33 | S5 | 承諾把建議公布在網站 | C | `We will publish our recommendations to AI companies on this website.` |
| 34 | S5 | 截至 9/23 尚未刊出任何一份 | C | 今日重抓 agmai.org：全站只有四節，站內連結只有 `/input` 與 `ias.edu`，沒有任何建議頁 |
| 35 | P3 | 「橫跨大多數數學領域」 | C | `across most areas of mathematics` |
| 36 | P3 | 進展速度讓 OpenAI 內部數學家意外 | C | `has surprised the mathematicians within OpenAI` |
| 37 | P3 | 引發內部討論如何讓數學界知道並提早準備 | C | `internal discussions on the best way to inform the community… to prepare and adapt the field` |
| 38 | P4 | 公開信標題與 9/11 | C | mathandai |
| 39 | P4 | 引句「目標嚴重失準」 | C | `The goals of the AI companies and the goals of the mathematical community are severely misaligned.` |
| 40 | P4 | 倉促公布／來不及寫成論文／釐清新方法／引用他人研究 | C | `Often these solutions are announced in a rush…` |
| 41 | P4 | 「需要**更**審慎地往來」 | **CH** | 原文 `the need for thoughtful engagement`，沒有比較級 |
| 42 | P5 | 公告原文「與已經成立獨立數學顧問小組的數學家們合作」 | C | 逐字 |
| 43 | P5 | 小組不是 OpenAI 設立的 | C | 同上＋agmai 的成立經過 |
| 44 | P5 | 「普林斯頓」 | **NF** | 同 #18 |
| 45 | P5 | 成員不由 OpenAI 支薪 | C | `Its members will not be paid by OpenAI` |
| 46 | P5 | 小組可自行決定成員增減 | C | `the group can change its membership as it sees fit` |
| 47 | P6 | 三項工作逐項 | C | 逐字 |
| 48 | P6 | 另就工具如何支援研究與學習給意見 | C | `It will also advise on how our tools can support mathematical research and learning.` |
| 49 | P7 | 獨立運作／可提未經要求的意見／可評論影響／可公開 | C | 四項逐字都在 |
| 50 | P7 | 截至 9/23 沒有刊出建議 | C | 同 #34 |
| 51 | 表格列 1 | 評估重要性、建議如何協調發布｜OpenAI 公告 | C | — |
| 52 | 表格列 2 | 建議學術與專業規範｜OpenAI 公告 | C | — |
| 53 | 表格列 3 | 不負責建議調整內部進度節奏｜OpenAI 公告 | C | — |
| 54 | 表格列 4 | 在任何 AI 公司都沒有決策權｜agmai.org | C | 依據欄位標對來源 |
| 55 | 表格 caption | 查核日 2026-09-23、51 字（≤200） | C | — |
| 56 | P8 | OpenAI 用 `Importantly` 特別標示 | C | 原文確實以 Importantly 開頭 |
| 57 | P8 | 「管不到內部推進速度」 | C | 同句 |
| 58 | P9 | agmai 引句「沒有決策權…責任仍在該公司」 | C | 逐字 |
| 59 | P9 | Current Task：協調 OpenAI「所報告」由內部模型產出的大量成果 | C | `…that they report have been produced by their internal model` |
| 60 | P9 | 小組沒有自己驗證或背書 | C | `they report` 的寫法；兩頁都沒有驗證或背書的敘述 |
| 61 | P10 | 不是監督或審查機關 | C | agmai 的無決策權句 |
| 62 | P10 | 決定權都在 OpenAI | C | `the responsibility for the decisions made by any company will rest with that company` |
| 63 | 圖解 caption | 四個角色／超過 100 題；與研究紀錄 `diagram.caption` 逐字相同 | C | checker 也比對這一項 |
| 64 | P11 | agmai 的成立經過引句 | C | `This group came together after OpenAI approached some of its members…` |
| 65 | P11 | 「改走獨立路線是成員自己的決定」 | C | `they decided to instead create an independent group` |
| 66 | P12 | 九人名單逐字 | C | 兩來源一致；OpenAI 頁的錯字 `Simons Institue` 沒有被抄入（文章只列名字不列單位） |
| 67 | P12 | 「以 2026-09-23 查核到的名單為準」 | C | 滿足研究紀錄 `live_data_warnings` 第 1 條 |
| 68 | P12 | Hairer 同時是公開信連署人、標註 2014 費爾茲獎 | C | `Martin Hairer (Fields Medal 2014)`；另以程式核對，九位成員中**只有** Hairer 在宣言頁名單上，Gowers／Witten／De Lellis／Wood 都不在，所以這句沒有把個案寫成通例 |
| 69 | P12 | 「顯示不是兩個互斥陣營」 | C（保留） | 編輯推論，非來源語句；見第 5 節 |
| 70 | P13 | 宗旨對象是「AI 公司」複數 | C | `to advise AI companies on their interactions…` |
| 71 | P13 | 目前工作對象是 OpenAI 及其原因 | C | Current Task 一節 |
| 72 | P14 | 解題的是未發布內部模型、不是 ChatGPT | C | 兩頁都寫 internal model；ChatGPT 是已發布產品 |
| 73 | P14 | 「比 GPT-6 Astra 強得多」（OpenAI 表示） | C | 只出現在 navier 頁：`an internal model that is significantly more capable than GPT‑6 Astra`；連字號已正規化為 U+002D |
| 74 | P14 | 沒有寫任何發布時程 | C | 兩頁皆無 |
| 75 | P14 | 「**三份**官方頁面都沒有提到台灣、亞洲或任何特定地區」 | **CH** | 四頁 `Taiwan`／`Asia`／`Japan`／`Korea`／`country`／`countries` 命中數全部 0（navier 唯一的 `region` 是 `This central region shrinks` 的流體描述），否定句對四份都成立 |
| 76 | P15 | 能追的官方頁面有兩個 | C | — |
| 77 | P15 | 引句「AI 有潛力增進並加速真正的數學研究與理解」 | C | 逐字 |
| 78 | P15 | 「數學這個專業需要在幾個面向上調整」 | C | `Mathematics as a profession will need to adapt to these changes in several ways.` |
| 79 | P15 | 「不是要求停止開發」 | C | 宣言全文讀畢，沒有停止／暫停的訴求 |
| 80 | P16 | Amodei 是 Anthropic 執行長、9 月稍早發表〈We Must Pace the Frontier〉 | C | 不在 `sources[]`；以站上已發布的 `ai-news-pace-the-frontier-20260912` 內容包核對，其 description 逐字寫「Anthropic 執行長 Dario Amodei 於 2026 年 9 月 12 日發表」 |
| 81 | FAQ A1 | 不是監督機構 | C | — |
| 82 | FAQ A2 | 不是 ChatGPT；官方沒公布名稱、規模、時程 | C | `not_said` |
| 83 | FAQ A3 | 成立經過 | C | agmai |
| 84 | FAQ A4 | 兩份官方頁面都沒寫能否否決、延後或有無拘束力 | C | 兩頁逐字確認 |
| 85 | FAQ A5 | 「這**三個**官方頁面」 | **CH** | 同 #75 |
| 86 | FAQ A5 | 模型還沒對外發布，沒有人能實際用到 | C | — |
| 87 | callout | 只有一個 callout、沒有投資免責段落 | C | AI 垂直規則 |
| 88 | callout | 來源列舉漏第四條 | **CH** | 同 #26 |
| 89 | callout | 「超過 100 題、8 月 28 日」是 OpenAI 自己的說法 | C | 歸因正確 |
| 90 | callout | 「**以下內容**為…查核當天的狀態」 | **CH** | callout 之後只剩兩個結尾連結，「以下」指不到東西；DELTA-4-7 §14 要求用「這一篇」 |
| 91 | 結尾連結 1 | text = 索引 zh-TW title | C | 與 `ai-news-2026-january-september-index.json` 字元級完全相同 |
| 92 | 結尾連結 2 | text = `ai-news-pace-the-frontier-20260912` 的 zh-TW title | C | 字元級完全相同（目標 `news_date` 2026-09-12、`display_order` 147） |
| 93 | sources[0] | 今日 200／370,896 B／讀到正文 | C | — |
| 94 | sources[1] | 今日 200／67,830 B／讀到正文 | C | — |
| 95 | sources[2] | 今日 200／10,873 B／讀到正文 | C | — |
| 96 | sources[3] | 今日 200／457,098 B／讀到正文 | C | — |
| 97 | meta | `topics ["ai","ai-news"]` | C | 通過 checker；站上 13 篇治理／公司類 ai-news（frontier-governance、misalignment-reports、pace-the-frontier、eu-transparency…）同一組 |
| 98 | meta | `display_order` 171、`news_date` 2026-09-21、`locales` 只有 zh-TW | C | 與 DELTA-4-7 第 2、5 條相符 |
| 99 | meta | 讀者優先：0 個「本文」、「官方」共 9 次分散 4 段、description 以查證註記收尾 | C | — |
| 100 | meta | 無 U+2011／NBSP／零寬字元；未抄入 `Simons Institue` 錯字 | C | — |
| 101 | 全篇 | 中英文之間漏空格 8 處 | **S** | 全篇其他地方都有空格，屬撰稿掉字；已修 |

**小計：查核 101 條、CONFIRMED 87、CHANGED 11、NOT FOUND（已改寫）2、排版 1（8 處）。**
事實／表述類的實際編輯是 13 筆（NOT FOUND 那一項散在 3 個位置）。

## 3. 改掉的 13 處（事實／表述）

| # | 位置 | 改前 | 改後 | 來源 |
| --- | --- | --- | --- | --- |
| 1 | title | OpenAI 的數學顧問小組是獨立的：能公開意見，但不管內部進度 | 與 OpenAI 合作的數學顧問小組是獨立的：能公開意見，但不管內部進度 | `agmai.org` |
| 2 | description | OpenAI 公告**將**與一群數學家合作 | OpenAI 公告**正**與一群數學家合作 | 公告頁 |
| 3 | P1 | OpenAI 在官方網站公告，**將**與一群數學家合作 | …**正**與一群數學家合作 | 公告頁 |
| 4 | summary 1 | …**將**與…，初始成員九人，掛在**普林斯頓**高等研究院之下。 | …**正**與…，初始成員九人，掛在**高等研究院（Institute for Advanced Study）**之下。 | 公告頁 |
| 5 | P1 | 掛在**普林斯頓**高等研究院（Institute for Advanced Study）之下 | 掛在高等研究院（Institute for Advanced Study）之下 | 公告頁 |
| 6 | P5 | 小組掛在**普林斯頓**高等研究院之下 | 小組掛在高等研究院之下 | `agmai.org` |
| 7 | summary 2 | 起因是 OpenAI 一個自 8 月 28 日開始訓練、尚未發布的內部模型，除了解出… | 起因是一個自 8 月 28 日開始訓練、尚未發布的內部模型：**OpenAI 表示**它除了解出… | 公告頁 |
| 8 | P2 | 讀的是 OpenAI **公告全文**、顧問小組自己的網站，以及數學家公開信全文 | 讀的是 OpenAI **的兩份公告**、顧問小組自己的網站，以及數學家公開信全文 | navier 頁 |
| 9 | P4 | 凸顯AI 公司需要**更**審慎地與數學社群往來 | 凸顯 AI 公司需要審慎地與數學社群往來 | 公告頁 |
| 10 | P14 | **三份**官方頁面查核到 9 月 23 日為止，都沒有提到台灣… | **四份**官方頁面… | 四頁機械核對 |
| 11 | FAQ A5 | OpenAI 的公告、…這**三個**官方頁面… | OpenAI 的**兩份公告**、…這**四個**官方頁面… | 四頁機械核對 |
| 12 | callout | 內容整理自 OpenAI **公告全文**、顧問小組網站 agmai.org**與**… | 內容整理自 OpenAI **的兩份公告**、顧問小組網站 agmai.org **與**… | navier 頁 |
| 13 | callout | **以下內容為**2026 年 9 月 23 日查核當天的狀態 | **這一篇寫的是** 2026 年 9 月 23 日查核當天的狀態 | DELTA-4-7 §14 |

### 排版修正（非事實，另計 5 處）

`不是OpenAI 設立的`、`決定權都在 OpenAI自己身上`、`不限OpenAI；`、`不是ChatGPT`、`Anthropic 執行長Amodei`
——全部補上中英文之間的空格。另外 3 處（`凸顯AI`、`agmai.org與`、`以下內容為2026`）已併在上表第 9、12、13 筆裡。
修正後全篇 CJK 與拉丁字母之間再無漏空格。

## 4. 查過而且正確的部分（摘要）

- **兩個結尾連結**的 text 與目標內容包的 zh-TW title **字元級完全相同**，不需要動。
- **九位成員名單**與兩個來源逐行一致；OpenAI 頁面上的錯字 `Simons Institue` 沒有被帶進文章。
- **Hairer 那一句**經程式交叉比對：九位成員中只有他出現在宣言頁那份 27 位費爾茲獎得主名單上（Gowers、Witten、De Lellis、Wood 都不在），
  所以「同時也是連署人之一」是準確的，也沒有被寫成通例。文章沒有印連署總人數，也沒有印 27 這個編輯清點數字——符合 `must_not_write`。
- **「尚未刊出任何一份建議」**今天重新確認成立。
- **`checked_on` 2026-09-23** 在四條 source、研究紀錄、第二段、表格 caption 四處一致，且等於我今天重抓的日期，因此**沒有改**。
- **事件日**：slug 尾碼 `20260921` = `news_date` = 第一段「2026 年 9 月 21 日」= 公告頁印的 `September 21, 2026`。
- **界線**：沒有購買建議、沒有比價、沒有投資免責段落（AI 垂直只有一個 callout）、廠商宣稱都有歸因、
  「超過 100 題」沒有被寫成已經過同儕審查或已被數學界接受、沒有任何台灣／地區的推測。
- **`hero.alt`** 依規格未查也未動（主圖由協調者繪製後改寫）。

## 5. 留給協調者的事

1. **標題我改了**。這是研究紀錄自己選的 `title`、也排在 `title_candidates` 第一位，所以這是需要裁定的一項。
   若要保留原標題，**研究紀錄的 `title` 要一起改回去**（`check_article.py` 會比對兩者）。
   紀錄裡的備選第四案是「數學家自己成立顧問小組：不支薪、可公開建議，但沒有決定權」。
2. **「普林斯頓高等研究院」→「高等研究院（Institute for Advanced Study）」**。四條來源全文都沒有 `Princeton`。
   若站主認為這是中文慣用名、可讀性優先，可以改回去，但那就不是來源撐得住的寫法。
3. **P12 結尾「顯示這場討論不是『支持顧問小組』與『連署公開信』兩個互斥的陣營」是編輯推論**，
   任何來源都沒有這樣寫，支撐它的只有 Hairer 一個重疊個案。我沒有刪；第二輪若要收緊，這是最該看的一句。
4. **宣言頁那 27 個名字上方沒有標題**（只在其後有「Add your name」與另一個 Endorsers 分頁），
   文章稱他們「連署人」是合理解讀但不是來源印出的字。要更保守可寫「署名者」。
5. **description 與第一段仍把「解出 Navier–Stokes」「超過 100 題」放在 OpenAI 公告的框架裡而沒有逐句掛「OpenAI 表示」**
   （summary 我已補、callout 也已聲明）。研究紀錄自己的 `summary` 也是這樣寫的，所以我依紀錄保留；
   若要更嚴，`description` 還有 45 字的空間可以加。
6. **繪圖**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug（DELTA-4-7 §15 是刻意的）。
   圖上會用到的數字在定稿後是：**9（初始成員）、100（超過 100 題）、8/28、9/11、9/21**，四個節點文字與 caption 未動。

## 6. 自檢輸出（原樣）

```
OK ai-news-openai-math-advisory-20260921 zh-TW paragraphs 2384
check_article exit=0
```

```
ai-news-openai-math-advisory-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-openai-math-advisory-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-math-advisory-20260921/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

兩個 `image_missing` 與一個 `raw_internal_url` 是 DELTA-4-7 預期的（繪圖與 relink 都還沒做），其餘沒有任何問題。

## 7. 第二輪

**需要**。依 DELTA-4-7 第 12 條第二輪必做；本輪的事實變更是 **13 處**（另加 8 處漏空格），
其中第 1、5、6 筆（標題與「普林斯頓」）動到骨幹表述，第 7、10、11 筆是新寫進去、還沒有人查過的句子，
第二輪要逐句回一手來源重查這些，外加隨機三分之一的 CONFIRMED 條目。
