# ai-news-openai-academy-paths-20260921 查核報告（第一輪）

- 查核者：獨立查核代理（第一輪），2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-openai-academy-paths-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-academy-paths-20260921.json`
- 主張數 96：CONFIRMED 78、CHANGED 14、NOT FOUND 0（兩條原本 NOT FOUND 的併入 CHANGED 改寫）、OUT OF SCOPE 4
- 事件日 2026-09-21 = slug 後綴 = `news_date` = 正文第一段；`checked_on` 2026-09-23（重抓當天，四處一致，未改）

## 1. 來源重抓（2026-09-23，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同主機間隔 ≥1 秒）

| # | URL | 狀態 | bytes | 是否讀到正文 |
| --- | --- | --- | --- | --- |
| S1 | `https://openai.com/index/expanding-openai-academy-with-new-learning-paths/` | 200 | 420,321 | 是。剝標籤後 7,563 字，八段正文加五個小標全部可讀；署名區只印 `September 21, 2026`，無時刻、無 JSON-LD 日期。本輪沒有 403 |
| S2 | `https://help.openai.com/en/articles/20001270-openai-academy-courses` | 200 | 110,050 | 是。13,919 字，含 14 列課程表、測驗規則、徽章、路徑證書、組織報表與 FAQ |
| S3 | `https://help.openai.com/en/articles/7947663-chatgpt-supported-countries` | 200 | 70,122 | 是。221 行，`Taiwan` 在第 194 行，前後為 `Svalbard and Jan Mayen` 與 `Tajikistan` |
| S4 | `https://academy.openai.com/public/courses/ai-for-college-students-gxgmr` | 200 | 296,459 | 是，但要從 `<script id="__NEXT_DATA__">` 的 `props.pageProps.data.course.course` 取；剝標籤只剩 425 字的導覽殼 |

四條都讀到正文，`checked_on` 維持 2026-09-23。所有英文引文以連續字串比對確認今天仍在來源正文裡（26 條，全部命中）。
工具：`C:\Users\x8120\mokaair-work\news47\_tools\ai-news-openai-academy-paths-20260921\`（`fetch.py`、`course_extract.py`、`verify.py`、`apply_edits.py`、`append_factcheck.py`）。

## 2. 主張表

代號：C＝CONFIRMED、X＝CHANGED、O＝OUT OF SCOPE（體例、非事實）。

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 1 | slug 後綴 20260921＝`news_date` 2026-09-21＝第一段「2026 年 9 月 21 日」 | C | S1 署名 `September 21, 2026` |
| 2 | `display_order` 175 | O | 由 DELTA-4-7 第 5 條定，`check_article.py` 已驗 |
| 3 | `topics` ai／software／ai-news、`kind` life、`featured` false | O | 體例 |
| 4 | title「OpenAI Academy 新增開發者、主管與師生課程：台灣也能免費修」 | C | S1＋S2＋S3 三段鏈，見 §4 |
| 5 | title 與研究紀錄 `title` 一致 | C | 逐字相同，未改 |
| 6 | description 199 字、句尾「（2026 年 9 月查證）」、無查證流水帳 | C | DELTA-4-7 第 14 條 |
| 7 | description：9/21 擴充 OpenAI Academy，新增四類對象課程 | C | S1 |
| 8 | description：加上既有 Apply AI at Work＝四條路徑 | C | S1 四個角色小標；S2 課程表四個 Category |
| 9 | description：說明中心指出全球皆可修、只要有 ChatGPT 帳號，台灣在支援地區清單上 | C | S2、S3 |
| 10 | description：可拿徽章、但徽章與完課證書都不是證照 | C | S2 |
| 11 | 公告標題〈Expanding OpenAI Academy with new learning paths〉 | C | S1 `<title>`／H1 |
| 12 | OpenAI Academy 是「免費線上學習平台」 | C | S2「OpenAI Academy offers free, self-paced courses」。公告本身沒有寫免費，草稿沒有把免費歸給公告，符合研究紀錄 not_said 第 3 條 |
| 13 | 新增對象：開發者、主管、教師與大學生 | C | S1「new courses for developers, leaders, educators, and college students」 |
| 14 | 「公告全篇沒有提到任何開放地區」 | C | S1 全文 `countr`／`region`／`globally`／`Taiwan` 命中 0；只有頁尾語系選單印 `EnglishUnited States` |
| 15 | 「台灣就在 ChatGPT 支援地區清單上，所以台灣讀者現在就能註冊上課」 | C | S2＋S3，見 §4 |
| 16 | 「把學習當成部署的一部分」 | C | S1「At OpenAI, we treat learning as part of deployment.」 |
| 17 | 「用 AI 來學 AI，在真實任務裡練習下指令、補充背景與檢查結果」 | C | S1 |
| 18 | 第二段「以下整理……」的導覽句 | O | 體例；未改（見 §5） |
| 19 | 「規格、時程與價格數字都是 OpenAI 自己的說法，沒有第三方測試可以對照」 | X | 見 §3-12 |
| 20 | summary 1：9/21 擴充、四類新課程、加既有 Apply AI at Work＝四條路徑 | C | S1 |
| 21 | summary 2：公告沒寫開放地區、說明中心寫全球皆可修、台灣在清單上 | C | S1／S2／S3 |
| 22 | summary 3：10–20 題、題庫 50 題、80% 以上、Accredible 發徽章、徽章與完課證書都不是證照 | C | S2 |
| 23 | summary 4：AI Leadership 180 分鐘、教師與學生兩門課各 45 分鐘、AI Foundations 60–75 分鐘 | C | S2 課程表四列 |
| 24 | summary 5：四個月免費 ChatGPT Work 只給美國合格大學生、每月 20 美元續訂、「台灣沒有對應方案」 | X | 見 §3-11 |
| 25 | 「Apply AI at Work 是原本就有的路徑」 | C | S1「These join Apply AI at Work」 |
| 26 | 「這次沒有變動」 | X | 見 §3-1 |
| 27 | Apply AI at Work：建立基礎技能、可重複的工作流程、指揮代理人 | C | S1 |
| 28 | Apply AI at Work 後段：指揮更大塊的工作、決定哪些交出去、加檢查點與人工覆核 | C | S1 |
| 29 | Build with AI 為使用 Codex 或以 OpenAI API 開發產品的開發者與技術團隊設計 | C | S1 |
| 30 | Build with AI 目標：從試用走到可靠、堪用的 AI 系統 | C | S1 |
| 31 | Lead AI Adoption 底下是 AI Leadership 這一門課 | C | S1「The AI Leadership course, part of Lead AI Adoption」 |
| 32 | AI Leadership 預估 180 分鐘 | C | S2 課程表 |
| 33 | AI Leadership 內容：商業優先順序、治理、路線圖與導入 | C | S2 課程表 What's covered |
| 34 | AI Leadership「不對應單一產品」 | C | S2「No single product; AI strategy and adoption」 |
| 35 | AI Leadership 的對象與商業價值段落被歸給「說明中心的課程表」 | X | 見 §3-2 |
| 36 | 公告把教師與大學生放在同一條路徑 Teach and Learn with AI、底下兩門課 | C | S1 小標「Educators and students: Teach and Learn with AI」；S2 課程表同 Category 兩列 |
| 37 | AI for Educators 預估 45 分鐘 | C | S2 |
| 38 | AI for Educators 內容：備課、出題、評量與溝通內容 | C | S2 |
| 39 | 教師用「自己有權使用的材料」規劃課程、設計活動或評量 | C | S1 |
| 40 | 改寫「給學生與同事」的溝通內容 | X | 見 §3-3（原文三類：students, teaching assistants, or colleagues） |
| 41 | 引文「The educator decides what belongs in their teaching.」與中譯 | C | S1 逐字命中 |
| 42 | AI for College Students 預估 45 分鐘 | C | S2、S4 皆印 45 |
| 43 | 大學生課練習：讀書計畫、小組角色、照作業要求檢查草稿、準備申請與面試 | C | S1、S2 |
| 44 | 課程頁把難度標為中階（Intermediate） | C | S4「Level: Intermediate」 |
| 45 | 對象是已有一些 ChatGPT 與提示詞經驗的大專學生，不需要用過 Projects 或 Work | C | S4 |
| 46 | 「官方建議完全沒用過 ChatGPT 的初學者先修 AI Foundations」 | X | 見 §3-4（S4 全文 `AI Foundations` 命中 0、`prerequisiteCourses` 為空） |
| 47–62 | 表格 16 格（四列 × 課程／所屬路徑／預估時間／內容重點） | C | S2 課程表逐格比對；路徑名用公告的大小寫（Apply AI at Work／Lead AI Adoption／Teach and Learn with AI），課程表印小寫 w 是同一件事 |
| 63 | 表格 caption：依說明中心課程表整理、時間為官方預估值、實際依練習多寡而定、查核日 9/23 | C | S2「Actual completion time may vary…」；84 字 ≤200 |
| 64 | 「OpenAI 建議企業把幾條路徑搭起來用，是範例不是規定」 | C | S1「A company might use…」的 might |
| 65 | 「新人訓練安排 Apply AI at Work」 | C | S1 |
| 66 | 「技術團隊上 Build with AI」（漏了開發者） | X | 併入 §3-6 |
| 67 | 「主管訓練則放進 AI Leadership 所在的 Lead AI Adoption」 | X | 見 §3-6，方向寫反 |
| 68 | 課程由 OpenAI 內部各團隊共同製作、隨模型／產品／指引更新 | C | S1 |
| 69 | 課程自訂進度、免費、登入 ChatGPT 帳號就能開始、不必加入工作區 | C | S2、S4 |
| 70 | 圖解 caption 與研究紀錄 `diagram.caption` 逐字一致 | C | `check_article.py` 驗過 |
| 71 | 徽章門檻：完成課程且測驗至少 80% | C | S2、S4 兩處一致 |
| 72 | Accredible 是發放與管理數位徽章的第三方平台 | C | S2「OpenAI partners with Accredible, a digital credentialing platform」 |
| 73 | 每份測驗 10–20 題、題庫 50 題、沒過可重考且重新隨機抽 | C | S2 |
| 74 | 修完一條 eligible pathway 的每門課與測驗可另拿完課證書 | C | S2 |
| 75 | AI Leadership／AI for Educators／AI for College Students 是獨立課程，不構成可拿完課證書的路徑 | C | S2「…are standalone courses and do not form a pathway.」，緊接在 Foundations／Codex／API 三條證書路徑之後 |
| 76 | 引文「These badges and certificates of completion are not certifications and do not guarantee eligibility for a future certification.」與中譯 | C | S2 逐字命中 |
| 77 | 「徽章……不是學分、學位或任何正式資格的替代」 | X | 見 §3-7 |
| 78 | 要登入才能開始上課與保存進度，不登入可先瀏覽 | C | S2 |
| 79 | 課程免費、不需要工作區帳號 | C | S2 |
| 80 | 「學校或公司的員工也是用個人身分報名」 | X | 見 §3-8（原文是 individuals **or through an organization**） |
| 81 | 徽章與進度綁在註冊 Academy 或 Sign in with ChatGPT 的那個 email | C | S2 |
| 82 | 開始上課後目前無法合併或連結帳號 | C | S2 |
| 83 | 「選錯 email 就得從頭來過」 | X | 見 §3-9 |
| 84 | 「公告與說明中心都沒有寫課程使用哪些語言」 | C | S1、S2 全文皆無語言說明 |
| 85 | 「公告、課程目錄與課程頁讀到的內容都是英文」（正文與 FAQ 各一次） | X | 見 §3-10，「課程目錄」指的頁不在 `sources[]` |
| 86 | 學生優惠寫明只給「Eligible U.S. college students」 | C | S4 逐字命中 |
| 87 | 四個月免費 ChatGPT Work、每月 20 美元續訂、可取消 | C | S4 |
| 88 | 「期限寫到 10 月 31 日（頁面沒有印年份）」 | X | 見 §3-5，原文是領取期限 |
| 89 | 「頁面沒有寫台灣或其他地區的對應方案」 | C | S4 全文無其他地區方案 |
| 90 | 「登入 academy.openai.com，在側欄點 Courses」 | C | S2「Go to academy.openai.com and sign in…Select **Courses** in the sidebar.」 |
| 91 | FAQ 六題的答句 | C／X | Q1 C、Q2 C、Q3 X（§3-4）、Q4 C、Q5 X（§3-10）、Q6 C |
| 92 | callout：課程會更新、沒有實際註冊或修課 | C | S1；揭露句照 DELTA-4-7 第 14 條寫「這裡整理的是……」，全篇無「本文」 |
| 93 | callout 末段「續訂價可以照官方原文引用，但不做划算與否的評語」 | X | 見 §3-13，寫給撰稿者的指示漏進正文 |
| 94 | 第一個結尾連結文字＝索引 zh-TW title | C | 與 `ai-news-2026-january-september-index.json` 逐字相同 |
| 95 | 第二個結尾連結文字＝`ai-news-chatgpt-work-20260709` 的 zh-TW title | C | 逐字相同（DELTA-4-7 第 7 條） |
| 96 | `sources[]` 四條的 title／url／`checked_on` 與研究紀錄一致 | C | `check_article.py` 驗過；四條今天都 200 且讀到正文 |

## 3. 改掉的 14 處

1. **Apply AI at Work「這次沒有變動」**（正文第 1 節）
   改成「這次新增的課程是加在它旁邊」。S1 只寫 `These join Apply AI at Work, which helps people build foundational skills…`，
   沒有任何一句說它未改版；「沒有變動」是推論。
2. **AI Leadership 的對象與商業價值被掛在「說明中心的課程表」名下**（正文第 2 節）
   原句把「目標是幫助負責策略、導入與變革管理的人評估 AI 能在哪裡創造商業價值」也算成課程表的內容；
   那句在 S1（`helps people responsible for strategy, adoption, and change management assess where AI could create business value.`），
   課程表只有 180 min／內容欄／`No single product`。改成對象與商業價值照公告寫（並補上公告的
   `connect an initiative to business priorities, define ownership and governance, and develop an initial AI strategy and roadmap`），
   課程表只承擔時間與內容欄，段落仍只有一個歸因詞。
3. **「改寫給學生與同事的溝通內容」→「給學生、教學助理與同事」**
   S1：`adapt communications for students, teaching assistants, or colleagues`。清單被縮短是本批列管的錯誤型態第 2 種。
4. **「官方建議先修 AI Foundations」（正文第 2 節與 FAQ Q3 各一次）**
   S4 全文 `AI Foundations` 出現 0 次，`prerequisiteCourses` 是空陣列；S1 只有
   `Education institutions can combine AI Foundations with AI for Educators and AI for College Students`（給學校搭配用，不是先修建議）。
   研究紀錄 `unverified_or_excluded` 第 2 條已寫明「建議先修 AI Foundations」來自不在 `sources[]` 的 AI for Educators 課程頁，
   正文不得使用。改成「課程頁沒有列先修課程，講 AI 基礎與提示詞的入門課是 Apply AI at Work 路徑裡的 AI Foundations」
   （FAQ 同義改寫），只用 S2 課程表撐得住的說法。
5. **「期限寫到 10 月 31 日」→「要在 10 月 31 日前領取」**
   S4：`Claim the student offer by October 31`——那是領取期限，不是四個月免費期的結束日。「（頁面沒有印年份）」保留。
6. **企業搭配路徑的方向寫反**
   S1：`A company might use Apply AI at Work in employee onboarding, offer Build with AI courses to developers and technical teams,
   and include AI Leadership in an executive, Champion, or transformation program.`
   草稿寫成「主管訓練則放進 AI Leadership 所在的 Lead AI Adoption」——把「把 AI Leadership 放進主管／Champion／轉型計畫」
   反過來寫成「把主管訓練放進 Lead AI Adoption」。同時補回被省略的「開發者」。
7. **「徽章……不是學分、學位或任何正式資格的替代」**
   沒有任何來源提到學分或學位。改成 S2 自己的說法：「代表的是完成課程並通過測驗這兩件事」
   （`Each badge recognizes that you completed a course and passed the assessment.`）。
8. **「個人身分就能修，學校或公司的員工也是用個人身分報名」**
   S2：`Learners can access courses as individuals or through an organization.` 原文給的是兩條路，草稿刪掉了組織那一條。
   改成「可以用個人身分修，也可以透過所屬的組織修」。
9. **「選錯 email 就得從頭來過」**
   S2 寫的是 `If you use the wrong account, your course activity and OpenAI Academy badges will be associated with the email address
   for that account.` 加上 `Academy accounts cannot currently be linked or merged after you begin a course.`——沒有「得從頭來過」。
   改成「選錯帳號，課程紀錄與徽章就會掛在那個 email 上」。
10. **「公告、課程目錄與課程頁讀到的內容都是英文」（正文＋FAQ Q5）**
    「課程目錄」指的是 `academy.openai.com/pages/courses`，不在 `sources[]`（研究紀錄把它列在 `sourcing_notes` 的參考頁）。
    改成「說明中心的課程表」，三個來源都在 `sources[]` 裡。
11. **summary 第五句「台灣沒有對應方案」**
    S4 只能支持「這一頁沒有寫」，不能支持「台灣沒有」。改成「頁面沒有寫台灣有對應方案」，與正文第 5 節的寫法一致
    （研究紀錄 `must_not_write` 第 9 條也只准寫「這個優惠寫明只給美國的合格大學生」）。
12. **第二段「沒有第三方測試可以對照」**
    無法查證的否定句（本批錯誤型態第 6 種），而且課程沒有「規格」可言。改成
    「課程時間、測驗規則與學生優惠的價格都是 OpenAI 自己頁面上寫的」。
13. **callout 末段的撰稿指示**
    「四個月免費 ChatGPT Work 學生優惠期滿後的續訂價可以照官方原文引用，但不做划算與否的評語」是寫給撰稿代理看的規格句，
    對讀者沒有意義（DELTA-4-7 第 14 條：查證紀律不要寫進正文）。刪掉，保留「課程時間與價格數字一律是 OpenAI 自己的說法。」
14. **（連動）第 9 點同段的標點**：把連續三個逗號改成分號，句意未動。

## 4. 「台灣也能免費修」這條鏈（站主特別要求核實）

1. 公告（S1）**完全沒有**開放地區：全文 `countr` 0 次、`region` 0 次、`globally` 0 次、`Taiwan` 0 次；
   只有頁尾語系選單印 `EnglishUnited States`。所以標題與第一段不可能從公告推出台灣。
2. 說明中心（S2）「Availability」節逐字寫：`OpenAI Academy courses are available globally to anyone with a ChatGPT account.`
   下一句 `Courses are free and do not require a workspace membership.`——「免費」與「全球」都在這裡，不在公告。
3. 支援地區頁（S3）的「Supported countries & regions on web and mobile」清單第 194 行是 `Taiwan`
   （前後 `Svalbard and Jan Mayen`、`Tajikistan`）。
4. 因此「有 ChatGPT 帳號 → 可修課」＋「台灣可以有 ChatGPT 帳號」＝台灣可以修，**且免費**。
   三段鏈今天全部重抓確認。正文寫的是官方說明怎麼寫、沒有寫「本站實測可註冊」，符合研究紀錄 `unverified_or_excluded` 第 7 條。
5. 徽章不是證照：S2 在 Availability 與 FAQ 兩處各說一次（`Neither is a certification.`），草稿引的是 Availability 那一句，逐字無誤。
6. 四個月 ChatGPT Work 只給美國：S4 逐字 `Eligible U.S. college students can get four months of ChatGPT Work for free…
   Claim the student offer by October 31; your subscription renews at $20/month after the free period unless you cancel.`
   **頁面文字確實沒有年份**（但「Claim the student offer」的超連結指向 `https://chatgpt.com/students/2026/`，網址帶 2026——見 §6）。

## 5. 讀者優先檢查

- 全篇沒有「本文」；指涉自己用「這裡整理的是……」。**通過**。
- `description` 199 字，句尾只帶「（2026 年 9 月查證）」，沒有查證流水帳。**通過**。
- title／description／summary 沒有任何「本站選了 N 則」式的清點數字；「四條路徑」是公告四個角色小標與課程表四個 Category 欄的內容事實，
  研究紀錄 `must_not_write` 第 1 條已裁定照四條寫。**通過**。
- 每段歸因詞：第 1、2、9（教師段）、22（語言段）四段有兩個以上的來源指示詞。
  第 1 段與第 22 段是承重的（公告沉默、說明中心才寫全球可修／語言），拿掉會讓句子失去意義，**未改**；
  第 2 段的「規格……沒有第三方測試」已在 §3-12 精簡。其餘每段最多一個。
- 兩個結尾連結文字與目標內容包的 zh-TW title **逐字相同**（程式比對，非目視）。
- 無購買建議、無推薦式比價；每月 20 美元只出現在「優惠期滿後續訂價」的事實敘述裡，沒有划算與否的評語。
- 廠商宣稱（課程效果、「用 AI 學 AI」、從試用走到可靠系統）都有歸因給 OpenAI。
- 沒有把公告寫成已上市／已生效；「四條路徑」是現況、不是預告。

## 6. 留給協調者／站主

1. **學生優惠的年份**：課程頁文字只有 `October 31`，但「Claim the student offer」連到 `https://chatgpt.com/students/2026/`。
   依研究紀錄 `must_not_write` 第 9 條沒有把 2026 補進正文。若站主要寫年份，得先把 `chatgpt.com/students` 那一頁抓下來當來源、
   並加進 `sources[]`（現在四條已滿，得換掉一條）。
2. **課程語言**：官方四頁都沒有說明課程語言，正文只寫「查核當天讀到的都是英文」。
   課程頁原始碼裡的 `"supportedLocales":["en","ja","ko","fr"]` 依研究紀錄仍不採用（那是平台介面設定，不是課程語言）。
3. **`enrollCount` 是活資料**（今天 AI for College Students 讀到 823，上一輪研究是 815），正文與圖上都沒有出現，維持這樣。
4. **說明中心頁首「Updated: 2 days ago」、支援地區頁「Updated: last month」**是相對時間，兩處都沒有被換算進正文，維持。
5. 圖檔尚未產出（`_DRAWINGS` 還沒有這個 slug），`--assets` 未跑；`raw_internal_url` 待 relink。

## 7. 自檢輸出（原樣）

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

（只剩 `image_missing` 與 `raw_internal_url`，符合 FACTCHECK-47 對出圖與 relink 前的預期。log 檔：
`C:\Users\x8120\mokaair-work\news47\_out\check_ai-news-openai-academy-paths-20260921.log`、
`…\lint_ai-news-openai-academy-paths-20260921.log`。）

## 8. 結論

`needs_second_round`（DELTA-4-7 第 12 條本來就要求第二輪）。第一輪改了 **14 處事實**，其中三處會影響讀者的行動判斷：
「官方建議先修 AI Foundations」（無來源）、「個人 vs 透過組織報名」（刪掉了官方給的另一條路）、
企業搭配路徑的方向寫反。第二輪要逐句回一手來源重驗這 14 處，以及第一輪新寫進去的每一句
（§3 的 1、2、3、4、5、6、7、8、9、10、11、12、13 各自的 after 文字），另加三分之一已確認的主張。
