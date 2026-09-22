# ai-news-openai-academy-paths-20260921 查核報告（第二輪）

- 查核者：獨立查核代理（第二輪，未參與撰稿、未參與第一輪），2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-openai-academy-paths-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-academy-paths-20260921.json`
- 第一輪報告：`factcheck/ai-news-openai-academy-paths-20260921-round1.md`（改 14 處／15 次字串替換）
- 重查 72 條：第一輪改過的 14 處全部、第一輪新寫進去的每一句、另加 58 條原判 CONFIRMED 的（占 78 條的 74%）
- 結果：CONFIRMED 66、CHANGED 6、NOT FOUND 0
- 事件日 2026-09-21 ＝ slug 後綴 ＝ `news_date` ＝正文第一段；`checked_on` 2026-09-23 四處一致，未改

## 1. 第二輪自己重抓（2026-09-23）

`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同主機間隔 ≥1.2 秒；
任何請求的 UA、標頭、查詢字串都沒有帶入姓名或 email。

| # | URL | 狀態 | bytes | 是否讀到正文 |
| --- | --- | --- | --- | --- |
| S1 | `https://openai.com/index/expanding-openai-academy-with-new-learning-paths/` | 200 | 420,322 | 是。剝標籤後 7,841 字，八段正文與五個角色小標全部可讀；署名區只印 `September 21, 2026`。本輪沒有 403 |
| S2 | `https://help.openai.com/en/articles/20001270-openai-academy-courses` | 200 | 110,051 | 是。14,303 字，含 14 列課程表、測驗規則、徽章、路徑證書、組織報表與 FAQ |
| S3 | `https://help.openai.com/en/articles/7947663-chatgpt-supported-countries` | 200 | 70,121 | 是。`Taiwan` 在第 194 行，前後為 `Svalbard and Jan Mayen` 與 `Tajikistan` |
| S4 | `https://academy.openai.com/public/courses/ai-for-college-students-gxgmr` | 200 | 296,427 | 是，但要從 `<script id="__NEXT_DATA__">` 的 `props.pageProps.data.course.course` 取；`description` 是 Slate 節點，另外攤平成純文字 |

把第一輪留在 `_raw\<slug>\` 的抓取結果與本輪逐行比對，**四頁的內容今天沒有變動**，兩邊的差異全部是剝標籤方式不同造成的空白差。

工具：`C:\Users\x8120\mokaair-work\news47\_tools\ai-news-openai-academy-paths-20260921-r2\`
（`fetch_r2.py`、`course_extract_r2.py`、`course_plaintext_r2.py`、`verify_quotes_r2.py`、`recheck_misses_r2.py`、
`mech_checks_r2.py`、`apply_edits_r2.py`、`append_second_round.py`）；抓下來的正文在
`C:\Users\x8120\mokaair-work\news47\_r2raw\ai-news-openai-academy-paths-20260921\`。

## 2. 第一輪改過的 14 處：逐句回一手來源

代號：C＝維持（第一輪的改法正確）、X＝第二輪再改。

| # | 第一輪改後的句子（節錄） | 判定 | 今天讀到的原文 |
| --- | --- | --- | --- |
| R1-1 | 「這次新增的課程是加在它旁邊」 | C | `These join Apply AI at Work, which helps people build foundational skills, create repeatable workflows, and direct work with agents.` 公告沒有任何一句說它未改版 |
| R1-2 | AI Leadership 的對象與商業價值改掛回公告 | C | `The AI Leadership course, part of Lead AI Adoption, helps people responsible for strategy, adoption, and change management assess where AI could create business value.` ＋`Learners connect an initiative to business priorities, define ownership and governance, and develop an initial AI strategy and roadmap for adoption.`；課程表只有 `180 min`／`Business priorities, governance, roadmaps, and adoption.`／`No single product; AI strategy and adoption` |
| R1-3 | 「給學生、教學助理與同事的溝通內容」 | C | `adapt communications for students, teaching assistants, or colleagues` |
| R1-4 | 「課程頁沒有列先修課程，講 AI 基礎與提示詞的入門課是 Apply AI at Work 路徑裡的 AI Foundations」（正文＋FAQ Q3） | C | S4 的 `prerequisiteCourses` 是空陣列、整頁 `AI Foundations` 出現 **0** 次；S2 課程表 `Apply AI at work｜AI Foundations｜60–75 min｜AI basics, prompting, context, and responsible use.` |
| R1-5 | 「要在 10 月 31 日前領取（頁面沒有印年份）」 | C | `Claim the student offer by October 31; your subscription renews at $20/month after the free period unless you cancel.` ——`by October 31` 是領取期限；頁面文字確實沒有年份 |
| R1-6 | 企業搭配路徑的方向與補回「開發者」 | C | `A company might use Apply AI at Work in employee onboarding, offer Build with AI courses to developers and technical teams, and include AI Leadership in an executive, Champion, or transformation program.` |
| R1-7 | 「徽章……代表的是完成課程並通過測驗這兩件事」 | C | `Each badge recognizes that you completed a course and passed the assessment.`；`credit`／`degree` 在四條來源全文各 **0** 次 |
| R1-8 | 「可以用個人身分修，也可以透過所屬的組織修」 | C | `Learners can access courses as individuals or through an organization.` |
| R1-9 | 「選錯帳號，課程紀錄與徽章就會掛在那個 email 上」 | C | `If you use the wrong account, your course activity and OpenAI Academy badges will be associated with the email address for that account.` ＋`Academy accounts cannot currently be linked or merged after you begin a course.` |
| R1-10 | 「公告、說明中心的課程表與課程頁讀到的內容都是英文」（正文＋FAQ Q5） | C | 三個來源都在 `sources[]`；今天讀到的三頁全部是英文 |
| R1-11 | summary 第五句「頁面沒有寫台灣有對應方案」 | C | S4 只寫 `Eligible U.S. college students`，全頁沒有其他地區的方案 |
| R1-12 | 第二段「課程時間、測驗規則與學生優惠的價格都是 OpenAI 自己頁面上寫的」 | C | 時間與測驗規則在 S2、價格在 S4，三者都是 OpenAI 自己的頁面；不再有無法查證的否定句 |
| R1-13 | callout 刪掉寫給撰稿者的指示 | C | 留下的「課程時間與價格數字一律是 OpenAI 自己的說法。」有來源、對讀者有意義 |
| R1-14 | 第 9 點同段的標點 | C | 體例，未再動 |
| — | FAQ Q2 仍留著第一輪從正文刪掉的「不是學分或學位」 | **X** | 見 §3-3、§3-4 ——**第一輪只改了正文，沒有跟到 FAQ** |

## 3. 第二輪再改的 6 處（6 次字串替換）

1. **「出題」不是 `activities`**（表格第 3 列內容欄＋正文第 6 段，同一字串兩處）
   `備課、出題、評量與溝通內容` → `備課、課堂活動、評量與溝通內容`。
   S2 課程表寫的是 `Lesson planning, activities, assessments, and communications.`——`activities` 是課堂活動，
   `assessments` 已經譯成「評量」，把 `activities` 譯成「出題」等於憑空多一項、又漏掉活動。
   公告同一節也寫 `create an activity or assessment`。
   來源：`https://help.openai.com/en/articles/20001270-openai-academy-courses`

2. **補考次數被寫成只有一次**
   `沒通過可以再考一次，題目會重新隨機抽。` → `沒通過可以重考，題目會重新隨機抽。`
   S2：`If you do not pass, you can try again with a newly randomized selection of questions.`——沒有任何次數上限。
   來源：`https://help.openai.com/en/articles/20001270-openai-academy-courses`

3. **FAQ Q1 末句是不設限的否定句、而且語意不清**
   `官方沒有另外說明台灣以外還有沒有其他限制。` → `查核當天讀到的這幾頁，沒有再寫台灣還有什麼其他限制。`
   本篇只讀了四頁，「官方沒有」超出可查證範圍（本批錯誤型態第 6 種）；「台灣以外」讀起來像在講別的國家。
   來源：`https://help.openai.com/en/articles/7947663-chatgpt-supported-countries`

4. **FAQ Q2 的題目還在問學分**
   `課程徽章等於證照或學分嗎？` → `課程徽章等於證照嗎？`
   第一輪已認定「學分／學位」無來源並從正文刪掉，FAQ 的題目與答句卻原封不動。
   `credit` 與 `degree` 在四條來源全文各出現 0 次。
   來源：`https://help.openai.com/en/articles/20001270-openai-academy-courses`

5. **FAQ Q2 答句的學分／學位**
   `它們代表完成課程並通過測驗，不是學分或學位。` → `它們代表的是完成課程並通過測驗這兩件事。`
   改成與正文同一句話（`Each badge recognizes that you completed a course and passed the assessment.`），
   FAQ 的答案回到正文的子集。
   來源：`https://help.openai.com/en/articles/20001270-openai-academy-courses`

6. **FAQ Q5 首句是不設限的否定句**
   `官方頁面沒有說明課程使用哪些語言。` → `公告與說明中心都沒有說明課程使用哪些語言。`
   正文寫的是「公告與說明中心都沒有寫」，FAQ 卻擴大成「官方頁面」。`language` 在 S1 與 S2 全文各 0 次
   （S1 只有頁尾語系選單的 `English United States`）。
   來源：`https://openai.com/index/expanding-openai-academy-with-new-learning-paths/`

## 4. 抽查的 58 條 CONFIRMED（重點）

- **事件日鏈**：公告署名區今天仍只印 `September 21, 2026`；slug 後綴 `20260921` ＝ `news_date` ＝ 正文第一段一致。
- **「台灣也能免費修」三段鏈**（站主特別要求的那條）今天重抓全部命中：
  公告全文 `countr`／`region`／`global`／`Taiwan` 各 **0** 次（只有頁尾語系選單印 `English United States`）；
  說明中心 `OpenAI Academy courses are available globally to anyone with a ChatGPT account.` ＋ `Courses are free…`；
  支援地區頁第 194 行 `Taiwan`。免費與全球都出自說明中心、不是公告，正文的歸屬正確。
- **表格 16 格**逐格對 S2 課程表：AI Foundations 60–75 min、AI Leadership 180 min、
  AI for Educators 45 min、AI for College Students 45 min 與四個 `What's covered` 欄全部相符
  （內容欄的「出題」已於 §3-1 改掉）；caption 84 字 ≤200，`Actual completion time may vary…` 支撐「實際依練習多寡而定」。
- **徽章與證書**：完成課程＋測驗 80% 以上、10–20 題、題庫 50 題、Accredible 發放與管理、
  `eligible pathway` 才有完課證書、`AI Leadership, AI for Educators, and AI for College Students are standalone
  courses and do not form a pathway.`——S2 與 S4 兩處一致。
- **課程頁**：`Level: Intermediate`、`designed for higher education students who already have some experience using
  ChatGPT and writing prompts`、`No prior experience with Projects or Work is required`、
  `four months of ChatGPT Work for free`、`$20/month after the free period unless you cancel`——全部逐字命中。
- **三段英文引文**（`The educator decides what belongs in their teaching.`、
  `These badges and certificates of completion are not certifications and do not guarantee eligibility for a future
  certification.`、`Eligible U.S. college students`）程式比對逐字命中。
- **兩個結尾連結**的 text 與目標內容包的 zh-TW title 用程式逐字比對，`ai-news-2026-january-september-index`
  與 `ai-news-chatgpt-work-20260709` 兩條都相同。
- **`sources[]` 四條**的 title／url／`checked_on` 與研究紀錄一致；`checked_on` 2026-09-23 與表格 caption、
  圖解 caption 同日；圖解 caption 與研究紀錄 `diagram.caption` 逐字相同，四組 node 的字串都在正文裡。
- **活資料仍未進正文**：課程頁 `enrollCount` 今天讀到 **824**（第一輪 823、研究時 815）；
  說明中心頁首 `Updated: 2 days ago`、支援地區頁 `Updated: last month` 都沒有被換算。

## 5. `verbatim_quote` 連續字串比對

研究紀錄 44 條 `verified_facts` ＋ `sources[]` 4 條，**48 條全部命中**。
其中 6 條（`Sign in with your ChatGPT account…Gradual, which manages…`、四列課程表、課程頁的 `Duration: 45 minutes`）
在「標籤之間補空白」的剝法下對不上，追查後確認是**剝法差異**：那 6 條取自「標籤直接刪掉、不補分隔」的渲染，
把空白全部去掉後 6 條都命中。四列課程表各自是**同一列的儲存格依序相接**，不是把不同段落拼在一起，
`Duration: 45 minutes` 則是課程頁把粗體 `Duration` 與 `: 45 minutes` 兩個文字節點連著顯示的結果。
都不是拼接造假，維持原狀，做法寫進研究紀錄的 `second_round.quote_continuity_notes`。

## 6. 讀者優先與界線檢查

- 全篇 **0 個「本文」**；指涉自己用「這裡整理的是……」。通過。
- `description` 199 字（120–200），句尾只有「（2026 年 9 月查證）」，沒有查證流水帳。通過。
- title／description／summary 沒有任何清點數字；「四條路徑」是公告四個角色小標與課程表四個 Category 的內容事實。通過。
- **歸因密度**：第一段只有一個歸因詞（「OpenAI 說明中心另外指出」，另兩處是事件本身與文件名稱）；
  16 段正文裡最多的兩段各兩個，其餘 ≤1。符合 FACTCHECK-47 的上限。
- 正文合計 **2,734 字**（1,800–3,000），每節 2–4 段；第二輪的改動淨值為 0 字。
- 沒有購買建議、沒有推薦式比價、沒有「划算／值得／推薦」；每月 20 美元只以「優惠期滿後的續訂價」出現。
- 廠商宣稱（課程效果、「用 AI 學 AI」、從試用走到可靠系統、路徑怎麼搭配）都歸因給 OpenAI；
  企業搭配那段保留了公告的 `might`（「當成一個範例做法而不是規定」）。
- 沒有把公告寫成已上市／已生效；沒有推定台灣有學生優惠；沒有 `finance` 主題、沒有投資免責 callout，只有一個一般 callout。
- 否定句全部限縮到「讀到的這幾頁、查核日」——本輪把最後三個沒限縮的（FAQ Q1、Q5）補上。

## 7. 留給協調者／站主

1. **每月 20 美元出現兩次**（summary 第五句＋正文最後一段）。`must_not_write` 第 10 條寫「可以照官方原文寫一次」，
   但 summary 依規定必須是正文的子集，兩處都是純事實、沒有評語，所以沒有動。要嚴格照「一次」解，
   刪掉 summary 那一句的價格即可。
2. **學生優惠的年份**（第一輪留下的問題，維持原樣）：課程頁文字只有 `October 31`，
   「Claim the student offer」的超連結指向 `https://chatgpt.com/students/2026/`。依裁定年份不進正文；
   要寫年份得先把 `chatgpt.com/students` 那一頁抓下來當來源，並換掉現有四條 `sources[]` 其中一條。
3. **summary 第四句的「60 到 75 分鐘」只出現在表格**、沒有出現在任何一段正文。
   `check_article.py` 的 `body_without_summary` 把表格算進正文，所以自檢通過（OK）；
   若之後把這條規則收緊成「只看段落」，要把這個時間補進正文。
4. 圖檔尚未產出（`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug），`--assets` 未跑；`raw_internal_url` 待 `relink`。
5. 課程語言仍只有「查核當天讀到的都是英文」：課程頁原始碼裡的 `"supportedLocales":["en","ja","ko","fr"]`
   依研究紀錄仍不採用（那是平台介面設定，不是課程語言），本輪重抓確認該字串今天還在，維持不寫。

## 8. 自檢輸出（原樣）

```
OK ai-news-openai-academy-paths-20260921 zh-TW paragraphs 2734
check_exit=0
```

```
ai-news-openai-academy-paths-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-openai-academy-paths-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-academy-paths-20260921/diagram-1.svg
1 entries checked
lint_exit=1
```

log 檔：`C:\Users\x8120\mokaair-work\news47\_out\fc2_check_ai-news-openai-academy-paths-20260921.log`、
`…\_out\fc2_lint_ai-news-openai-academy-paths-20260921.log`；
exit code 另存 `C:\Users\x8120\mokaair-work\news47\factcheck\ai-news-openai-academy-paths-20260921-round2.exitcodes.txt`。

## 9. 結論

`ok`。第二輪重查 72 條、又改 6 處，沒有 NOT FOUND。
第一輪的 14 處改動**全部站得住**，但它只改了正文、沒有跟到 FAQ——「不是學分或學位」在 FAQ 存活下來，
是本輪最重的一處。另外兩處（`activities` 誤譯成「出題」、補考次數被寫死成一次）都會影響讀者對課程的實際判斷。
骨幹論述（台灣可修、免費、徽章不是證照、四條路徑、學生優惠只給美國）本輪全部回到一手來源重驗，沒有動。
**不需要第三輪**；剩下的三件事（§7 第 1–3 點）是協調者的裁量，不是事實問題。
