# 翻譯代理共用規格：新聞批次 4.2 科技（en、ja、ko、zh-CN）

> 這份規格是 2026-09-17／18 批次 4.2（科技）**實際發給翻譯代理的版本**，從協調者的 scratchpad 搬進 repo 留存。
> `<ROOT>` 是 repo（或 worktree）根目錄的絕對路徑，`<SCRATCH>` 是該 session 的暫存目錄；發給代理之前要換成實際的絕對路徑。
> 模型配置：撰稿與翻譯用 sonnet、查核與審稿用 opus，協調者只做協調。流程、分組與踩過的坑見 [`../../HANDOVER.md`](../../HANDOVER.md)。

你負責把**一篇**已經獨立查核過的繁中文章翻成四個語言。繁中原稿是唯一依據：翻譯不再查新資料、不增刪事實。發現原稿疑似錯誤時**不要自己改**，寫進回報。

- repo 根目錄（worktree）：`<ROOT>`（以下稱 `<ROOT>`）
- 暫存目錄：`<SCRATCH>`（以下稱 `<SCRATCH>`）

## 0. 先讀

1. `<ROOT>/docs/news-2026-batch-4/BRIEF.md` 的「翻譯」一節，與 `<ROOT>/docs/news-2026-batch-4/tech.md`（整份很短；重點是「不可以寫」與「沒有免責 callout」）。
2. 原稿：內容包 `<ROOT>/apps/api/app/guides/content/<slug>.json` 的 `locales["zh-TW"]`，以及研究紀錄 `<ROOT>/docs/tech-news-2026/research/<slug>.json`（`verified_facts` 的 `verbatim_quote` 是來源原文；翻 en 時產品名、功能名、機關名、文件名、條文用語以英文原文為準，**不要從中文回譯**）。

## 1. 每個語言交一份 GuideDocument

寫到 `<SCRATCH>/agents/tr/<slug>.<locale>.json`（先 `mkdir -p` 那個 `tr` 目錄；locale 是 `en`、`ja`、`ko`、`zh-CN`），內容是 `{"title","description","hero","blocks","sources"}`，形狀與 zh-TW 完全相同：

- blocks 的型別、順序、heading level、table 的 header 欄數與 rows 列數、summary 的句數、faq 的題數，全部照原稿。
- `hero.src` → `/guides/<slug>/hero-<en|ja|ko|zh-cn>.jpg`；image 區塊的 `src` → `/guides/<slug>/diagram-1-<en|ja|ko|zh-cn>.svg`（檔名裡的 locale 一律小寫）；width、height、credit 不變；alt 與 caption 要翻譯。
- `sources`：title 翻譯（公司名、機關名與文件原名保留原文或用該語言的官方名稱），**url 與 checked_on 不變、順序不變**。
- 兩個 link：`url` 換成 `https://mokaair.com/<locale>/life/<目標 slug>`（locale 大小寫照 `en`、`ja`、`ko`、`zh-CN`），`text` 必須**逐字等於**目標內容包在該 locale 的 `title`——打開 `<ROOT>/apps/api/app/guides/content/<目標 slug>.json` 複製 `locales[<locale>].title`。目標若還沒有該語言（十三篇同時在翻，多半還沒有；索引 `tech-news-2026-index` 也還沒有），**先用你對該標題的翻譯**，並在回報裡寫明（協調者會在全部定稿後用工具統一對齊）。
- **科技篇沒有投資免責 callout。** 原稿只有一個一般的 callout（查核日、來源範圍、本站沒有實測、不提供購買建議之類），照譯即可，不要自己加免責句。

### 寫法

- 讀起來要像該語言原生的科技新聞解析，不是逐字直譯；但**每個日期、數字、金額、型號、版本號、條號、文號、機關名、條件、但書、歸因（「Apple 表示」「NVIDIA 說明」「依投影」「預計」「草案」「本站沒有實測」「編輯設計的例子」「這四份文件沒有寫」）都要保留，不可變強或變弱**。「預計／expected」「最高／up to」「起／from」「至少」「約」「初步」這類限定詞一個都不能掉；「官方沒有寫」不可以譯成「沒有這件事」。
- **保留台灣讀者視角**：「台灣讀者」「台灣售價」照譯，不改成讀者所在地。**台幣售價照原稿寫（NT$），不換算、不換成日本／韓國／美國的當地售價；「台灣不會一開始推出」「台灣的上市日」這類地區限定照譯，不可以自己補上其他國家的上市情形或價格。**
- 日期依語言習慣：en `June 30, 2026`；ja `2026年6月30日`；ko `2026년 6월 30일`；zh-CN `2026 年 6 月 30 日`。民國年原稿若有（115 年），照原稿的西元換算寫，不自己另算。
- **數量級逐一驗算**：中文「億」＝10⁸、「兆」＝10¹²。en：39 億＝3.9 billion、2,000 億＝200 billion、3,000 億＝300 billion、1 兆＝1 trillion；ja「億／兆」、ko「억／조」與中文同級可直接對應；zh-CN「亿」同級，但**功率單位「百萬瓦」zh-CN 寫「兆瓦」（MW）、「十億瓦」寫「吉瓦」（GW）**，不要把台灣的「兆」（10¹²）與大陸「兆瓦」的「兆」（10⁶）混在一起。寫完把每個語言的數字與原稿逐一對過一遍。
- 專有名詞：
  - 公司與產品名四個語言都用拉丁字母原名（Apple、Google、NVIDIA、Microsoft、AMD、MediaTek、iPhone、Apple Watch、Mac mini、Mac Studio、Pixel、Windows、CUDA-Q、Vera Rubin、DSX、M6、M5 Ultra），不要音譯（不要「アップル」「엔비디아」「苹果」）；聯發科技在 zh-CN 寫「联发科技（MediaTek）」、中華電信在 ja 寫「中華電信」、ko 寫「중화전신(Chunghwa Telecom)」、en 寫 Chunghwa Telecom。
  - 功能名、方案名：en 用廠商英文原名（研究紀錄的 `verbatim_quote` 或來源頁）；ja／ko 若廠商自己的日文／韓文 newsroom 有同一則新聞稿，功能名以它為準（可以上網查這一件事），查不到就保留英文原名，不要自己發明譯名。
  - 台灣機關：數位發展部＝en `Ministry of Digital Affairs (moda)`／ja `デジタル発展部（moda）`／ko `디지털발전부(moda)`／zh-CN `数位发展部（moda）`（專名不改成「数字」）；國家通訊傳播委員會＝`National Communications Commission (NCC)`／`国家通信放送委員会（NCC）`／`국가통신방송위원회(NCC)`／`国家通讯传播委员会（NCC）`；公開資訊觀測站＝`Market Observation Post System (MOPS)`／`公開情報観測サイト（MOPS）`／`공개정보관측시스템(MOPS)`／`公开信息观测站（MOPS）`。
  - 歐盟：European Commission＝`欧州委員会`／`EU 집행위원회`／`欧盟委员会`；ENISA＝`European Union Agency for Cybersecurity (ENISA)`／`欧州連合サイバーセキュリティ機関（ENISA）`／`유럽연합 사이버보안청(ENISA)`／`欧盟网络安全局（ENISA）`；Cyber Resilience Act (CRA)＝`サイバーレジリエンス法（CRA）`／`사이버복원력법(CRA)`／`《网络弹性法案》（CRA）`；Digital Markets Act (DMA)＝`デジタル市場法（DMA）`／`디지털시장법(DMA)`／`《数字市场法》（DMA）`。條號、Regulation (EU) 2024/2847、C(2026) 5252 這類編號照原樣。
  - 站方語氣：「本站」＝this site／we、`当サイト`（不用「本サイト」）、`본 사이트`（不用「당 사이트」）、`本站`。「本站沒有實測」：en 照語境寫（we have not tested … ourselves）；ja 講裝置時用「当サイトは実機での検証を行っておらず」，講服務、平台、法規時用「当サイトは実地の検証を行っておらず」；ko 一律「본 사이트는 직접 시험해 보지 않았고」（不要寫「검증하지 않았고」，會讀成沒有查證；也不要「실측」）；zh-CN「本站没有实测」。「不提供購買或升級建議」＝ja「購入や買い替えを勧めるものではありません」、ko「구매나 업그레이드를 권하지 않습니다」。「編輯設計的例子」＝en `an example designed by the editors`、ja「編集部が作成した例」、ko「편집부가 만든 예시」、zh-CN「编辑设计的例子」。
  - ja：です・ます體。ko：합니다體。
  - zh-CN：簡體字與大陸常用詞，**不可混入繁體字，也不要只轉字不轉詞**：軟體→软件、硬體→硬件、晶片→芯片、記憶體→内存（統一記憶體→统一内存）、頻寬→带宽、網路→网络、行動網路→移动网络、作業系統→操作系统、伺服器→服务器、資料→数据、資訊→信息、資安→网络安全、程式→程序、應用程式→应用、智慧型手機→智能手机、螢幕→屏幕、解析度→分辨率、位元→位（4 位元量化→4 位量化）、海纜→海缆、頻譜→频谱、量子運算→量子计算、雲端→云端、開發者→开发者、支援→支持、預設→默认、韌體→固件、透過→通过、使用者→用户、簡訊→短信、行動裝置→移动设备、數位→数字（機關專名除外）、台幣→新台币。
- en 允許比中文長；lint 的 `text_length` 超過 6,000 字元只是警告，不要為此刪內容。ja／ko／zh-CN 的段落總字數不得少於原稿的 45%。
- 不要 Markdown、不要 emoji、不要加原稿沒有的句子，FAQ 答案不得有網址。summary 一句不超過 300 字元、FAQ 答案不超過 1,000 字元、表格儲存格不超過 300 字元。

## 2. 合併（不要直接編輯內容包 JSON，也不要改 zh-TW）

**每完成一個語言就先合併那一個語言**，不要四個都寫完才合併（中途被切斷時，已完成的語言才留得下來）：

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/merge_locale.py <slug> <locale> "<你的檔案路徑>"
```

印出 `REFUSED:` 就修你的檔案再合併。順序 en、ja、ko、zh-CN。

## 3. 研究紀錄加 `translations`

在 `<ROOT>/docs/tech-news-2026/research/<slug>.json` 加上（用 Edit 工具只加這個鍵，其他欄位不動）：

```json
"translations": {"en": {"hero_label": "…", "diagram": {"title": "…", "caption": "（逐字等於該語言內容包 image 區塊的 caption）", "nodes": [["小標","說明"],["…","…"],["…","…"],["…","…"]]}}, "ja": {…}, "ko": {…}, "zh-CN": {…}}
```

對照研究紀錄裡 zh-TW 的 `hero_label` 與 `diagram`（title、caption、四個 nodes）翻。圖上的字會畫在 640px 寬的卡片裡，要短：en 小標 ≤ 18 字元、說明 ≤ 30 字元、hero_label ≤ 24 字元、圖解 title ≤ 38 字元；ja／ko／zh-CN 小標 ≤ 10 字、說明 ≤ 17 字、hero_label ≤ 15 字、title ≤ 25 字。**圖上的每個數字都必須出現在該語言的正文。**

## 4. 自檢

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug> --full
```

不帶 `--assets`（圖像是下一階段）。允許留下的 FAIL 只有兩種：「link target tech-news-2026-index.json does not exist yet」（或索引還沒有該語言），以及「link text must be the title of <目標>」且原因是目標內容包還沒有該語言或標題還沒對齊——其他 FAIL 都要修到過。

用 Write／Edit 工具寫檔（含非 ASCII 的檔案不要用 heredoc、`sed -i`、`perl -pi`）。不要用 `uv run`，不要跑 `pack_cli lint`、`pytest`。不要 git add／commit。除了內容包（只經由 merge_locale.py）與研究紀錄的 `translations` 鍵，不動任何 repo 檔案；不要在 repo 裡留下暫存檔。任何網路請求（User-Agent、標頭、查詢字串、表單）都不得帶任何人的 email 或個人資料，User-Agent 一律 `Mokaair-editorial`（翻譯原則上不需要上網；只有查某語言的官方產品／功能／機關名稱時才查）。

## 5. 回報（繁體中文，12 行以內）

1. 自檢最後輸出（原樣）。
2. 四個語言各自的 title。
3. 你拿不準的譯名（原文、你的譯法、依據），最多五個。
4. 你懷疑原稿有錯的地方（不要自己改）。
