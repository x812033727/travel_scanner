# 交接：新聞批次 4（2026-09-18：三個垂直都已發布）

這份文件給接手的人或模型。它記的是**批次 4 三個垂直現在各做到哪裡、還缺什麼、怎麼接著做**。
規格在 [`BRIEF.md`](BRIEF.md)、[`crypto.md`](crypto.md)、[`tech.md`](tech.md)、
[`ai.md`](ai.md)；工具的取捨在 [`PORT-NOTES.md`](PORT-NOTES.md)。

站主的指示是「幣圈和科技的先全部寫，AI 挑補漏那幾則」，並指定**先交幣圈這批驗收**。
2026-09-17 兩個 session 都只做幣圈（批次 4.1）：第一個寫完十一篇並查核、翻好十篇；第二個補齊缺的語系、
做完逐語審稿、出圖、互連與驗證。**站主當天指示合併並匯入發布，幣圈十二個內容包已在正式站上線**（部署、匯入與驗證紀錄在 4.1 那張票）。
站主接著說「好 開始」，同一個 session 在 2026-09-17 晚到 09-18 把**科技垂直（批次 4.2）十三篇加索引做到五語、已逐語審稿、圖檔齊全**，
PR #546；**站主 2026-09-18 明確指示「合併並發布」，十四個內容包已在正式站上線**（見第 1b 節；部署、匯入與驗證紀錄在 4.2 那張票）。
AI 12 篇（4.3）在同一個 session 於 2026-09-18 做到**五語、兩輪查核、逐語審稿、圖檔齊全，並把既有索引原地改版**（第 1c 節），
PR #548；**站主 2026-09-18 明確指示「合併並發布」，12 篇加改版索引與 30 個既有包已在正式站上線**（見第 1c 節；部署、匯入與驗證紀錄在 4.3 那張票）。

## 1. 幣圈十一篇加索引的現況

「查核」欄是獨立查核代理核對的主張數與改動處數；兩個數字的是做了第二輪。
十二個內容包都是五語（zh-TW、en、ja、ko、zh-CN）、五語圖檔齊全、都經過逐語審稿。

| 代號 | slug | 查核 | 逐語審稿採用的修正（en／ja／ko／zh-CN） |
| --- | --- | --- | --- |
| C1 | `crypto-news-taiwan-vasp-act-20260630` | 87 條／改 7 | 16／26／15／8 |
| C2 | `crypto-news-mica-transition-ends-20260701` | 86／18 | 17／4／5／5 |
| C3 | `crypto-news-sec-crypto-interpretation-20260323` | 107／9 | 5／11／19／16 |
| C4 | `crypto-news-sec-regulation-crypto-assets-20260821` | 108／20，第二輪再改 9 件 | 11／5／7／31 |
| C5 | `crypto-news-eba-psd2-mica-20260212` | 96／9 | 8／4／43／0 |
| C6 | `crypto-news-genius-act-occ-20260302` | 98／12 | 6／11／15／28 |
| C7 | `crypto-news-stablecoin-aml-20260410` | 96／13，第二輪 41／12 | 16／6／8／8 |
| C8 | `crypto-news-fdic-genius-act-20260410` | 96／6 | 9／20／20／21 |
| C9 | `crypto-news-ncua-genius-act-20260518` | 92／13，第二輪 58／10 | 8／10／4／39 |
| C10 | `crypto-news-jfsa-working-group-20260216` | 111／10，逐語審稿後再訂正 1 處事實（見第 4 節） | 12／34／14／45 |
| C11 | `crypto-news-jfsa-cybersecurity-20260723` | 104／12 | 11／29／10／14 |
| 索引 | `crypto-news-2026-index` | 約 160 條／14 條發現已全數套用 | 30／8／8／6 |

每篇的查核報告在 [`factcheck-draft/`](factcheck-draft)，研究紀錄（含 `factcheck` 欄位、每條事實的逐字引文）
在 [`../crypto-news-2026/research/`](../crypto-news-2026/research)。逐語審稿採用的 706 筆修正全文在
[`translation-corrections.json`](translation-corrections.json)，退回的 1 筆在
[`translation-corrections-rejected.json`](translation-corrections-rejected.json)，協調者自己的 54 筆在
[`coordinator-corrections.json`](coordinator-corrections.json)。
十一篇都過 `check_article.py --full --assets`，索引五語過 schema 與 lint；**十二篇已於 2026-09-17 以 `guides-import --slug` ×12 匯入發布**（60 個語系全數 created＋published、`failed: null`）。

## 1b. 科技十三篇加索引的現況（批次 4.2）

PR #546（squash 為 `88e4cd1a`）。十四個內容包都是五語、五語圖檔齊全、都經過**兩輪**獨立查核與逐語審稿；
十三篇都過 `check_article.py --full --assets`，索引五語過 schema 與 lint，`pack_cli lint --kind life` 0 error。
**2026-09-17T22:10Z 部署、`guides-import --slug` ×14 匯入發布**（70 個語系 create＋published、`failed: null`），正式站 70 個網址全數 200、可索引、都在 sitemap。
「查核」欄是第一輪核對的主張數／改動處數，與第二輪再改的處數。

| 代號 | slug | 查核（第一輪；第二輪） | 逐語審稿採用的修正（en／ja／ko／zh-CN） |
| --- | --- | --- | --- |
| T1 | `tech-news-iphone-duo-20260909` | 98／13；再改 9 | 1／14／25／16 |
| T2 | `tech-news-apple-september-hardware-20260909` | 96／20；再改 10 | 5／8／13／13 |
| T3 | `tech-news-eu-cra-reporting-20260911` | 96／16；再改 14 | 7／8／10／34 |
| T4a | `tech-news-taiwan-sovereign-ai-corpus-20260915` | 97／17；再改 10 | 5／16／25／4 |
| T4b | `tech-news-taiwan-6g-spectrum-20260910` | 94／15；再改 10 | 9／27／17／27 |
| T4c | `tech-news-taiwan-matsu-cable-20260623` | 92／11；再改 8 | 5／32／7／3（ja 另做第二次審稿，見第 4 節） |
| T5 | `tech-news-apple-eu-business-terms-20260818` | 96／14；再改 14 | 2／34／4／14 |
| T6 | `tech-news-windows-project-zenith-20260904` | 96／16；再改 9 | 1／57／66／52（大宗是公司名改回 Microsoft） |
| T7 | `tech-news-pixel-drop-20260915` | 96／17；再改 16 | 1／3／30／2 |
| T8 | `tech-news-apple-m6-m5-ultra-20260825` | 144／21；再改 9 | 4／11／15／5 |
| T9 | `tech-news-nvidia-cuda-q-20260914` | 123／30；再改 15 | 2／6／3／9 |
| T10 | `tech-news-nvidia-mediatek-20260831` | 96／22；再改 17 | 4／11／17／1 |
| T11 | `tech-news-nvidia-vera-rubin-20260915` | 92／19；再改 18 | 5／11／7／8 |
| 索引 | `tech-news-2026-index` | 協調者撰寫，只重述十三篇已查核的事實 | 9／35／25／14 |

查核報告在 [`factcheck-draft/`](factcheck-draft)（`tech-news-*.md`，每份都有「第二輪」一節），研究紀錄在
[`../tech-news-2026/research/`](../tech-news-2026/research)。逐語審稿採用的 799 筆與幣圈的 706 筆同在
[`translation-corrections.json`](translation-corrections.json)；協調者自己的修訂（標題、公司名、用語統一、`hero.alt`、圖上文字、
騰字數的刪減）在 [`coordinator-corrections.json`](coordinator-corrections.json)。實際發給代理的四份規格在 [`agents/tech/`](agents/tech)。

### 留給站主決定的事（發布後仍可修訂）

- **會變動的活資料（日後更新文章時重查）**：ENISA 常見問答是活文件（第 9 題 09-17 標 `[UPDATED]`）；
  Pixel Drop 的 11 地區／8 語言清單與機型對照表、數發部「最新海纜狀況」頁、Apple 台灣售價都是 09-17 的快照。
  歐盟 CRA 那篇的法條來源換成了 EUR-Lex 的 ELI 網址（原本的 CELLAR 網址在中文瀏覽器會回錯誤頁）：**發布前已確認**——
  2026-09-17T21:56Z `curl` 200／974,702 bytes，讀到 Article 14 與「11 September 2026」；帶 `Accept-Language: zh-TW` 同樣 200 HTML，舊網址同條件回 404。
- **NVIDIA 投資聯發科那篇照申報書寫了轉換價 NT$4,513.75 與 8/31 收盤價 NT$3,925**。科技垂直沒有禁止，文章也沒有任何投資語氣；
  站主若想比照幣圈「不寫行情數字」，刪這兩個數字即可（五語）。暫定發行日 9/8 已過，要寫最新狀態得換 `sources[]`。
- **Apple 九月硬體那篇的 29／30 小時**（續航）兩個數字都沒寫：來源名額放不下美國版新聞稿。
- **馬祖海纜那篇**要不要把數發部新聞稿 16356 換進 `sources[]` 以寫「原定 115 年 6 月完工」的對照；**語料庫那篇**要不要寫即時規模
  （需另指定來源）、taic 網站仍自稱 Beta、授權條款的官方英文版把「停止提供使用」寫得比中文版窄（文章已註明只依中文版陳述）。
- **zh-TW 的「微軟」保留**（站上已有 11 篇繁中文章這樣寫）；四個譯文語言的公司名一律用拉丁原名。

## 1c. AI 十二篇加索引改版的現況（批次 4.3）

PR #548（squash 為 `d5a97c6f`）。十二個新內容包都是五語、五語圖檔齊全、都經過**兩輪**獨立查核與逐語審稿；
十二篇都過 `check_article.py --full --assets`，`pack_cli lint --kind life` 0 error（只有 en 超過 6,000 字元的既有警告），內容測試 164 passed。
**2026-09-18T03:19Z 部署、`guides-import --slug` ×43 同一次匯入發布**（12 篇 60 個語系 create、索引與 30 個既有包 147 個語系 update、`failed: null`），
正式站 65 個網址（12 篇＋索引 × 5 語）全數 200、可索引、都在 sitemap，既有文章指向索引的連結文字已換新。「查核」欄是第一輪核對的主張數／改動處數，與第二輪再改的處數。

| 代號 | slug | 查核（第一輪；第二輪） | 逐語審稿採用的修正（en／ja／ko／zh-CN） |
| --- | --- | --- | --- |
| B1 | `ai-news-openai-astral-20260319` | 96／20；再改 21 | 5／11／3／23 |
| B2 | `ai-news-openai-funding-20260331` | 110／30；再改 9 | 3／4／5／2 |
| B3 | `ai-news-gpt-55-instant-20260505` | 96／18；再改 6 | 2／4／4／3 |
| B4 | `ai-news-chatgpt-ads-20260505` | 138／24；再改 12 | 8／23／6／1 |
| B5 | `ai-news-frontier-governance-20260528` | 96／19；再改 14 | 10／11／77／3（ko 69 筆是 한다체→합니다體） |
| B6 | `ai-news-openai-s1-20260608` | 108／19；再改 9 | 6／12／18／21 |
| B7 | `ai-news-openai-broadcom-chip-20260624` | 106／18；再改 11 | 3／31／1／5（ja 30 筆是だ・である→です・ます） |
| B8 | `ai-news-chatgpt-financial-services-20260910` | 128／17；再改 25 | 2／7／13／18 |
| B9 | `ai-news-gpt-live-1-api-20260910` | 96／15；再改 13 | 5／5／7／7 |
| B10 | `ai-news-chatgpt-storage-scale-20260911` | 87／20；再改 14 | 2／9／15／0 |
| A1 | `ai-news-gemini-38-live-20260915` | 96／29；再改 9 | 4／4／5／10 |
| A3 | `ai-news-nvidia-hugging-face-20260903` | 118／19；再改 9 | 1／2／6／2 |

查核報告在 [`factcheck-draft/`](factcheck-draft)（`ai-news-*.md`，每份都有「第二輪」一節），研究紀錄在
[`../ai-news-2026-09-late/research/`](../ai-news-2026-09-late/research)。逐語審稿採用的 429 筆與前兩個垂直的 1,510 筆同在
[`translation-corrections.json`](translation-corrections.json)（zh-CN 審稿另交的 40 筆「查核→核实／核查」沒有套，見第 3 節）；
協調者自己的修訂在 [`coordinator-corrections.json`](coordinator-corrections.json)。實際發給代理的六份規格在 [`agents/ai/`](agents/ai)。
另有一位文體修正代理把 B7 的 ko 全篇、B5 的 ja 半篇改回本站規定的敬體，並把 B3／B8 ko 約 17 處「공식이／공식은」當主詞的句子改成「OpenAI가／OpenAI는」（不動內容）。

**既有索引 `ai-news-2026-january-september-index` 原地改版**（`update_index.py ai`）：五語標題去掉日期（「1 月至 9 月」）、
description 與正文拿掉所有篇數、月份表拿掉「本輯新聞篇數」整欄並把「9 月 1–14 日」改成「9 月」、加 12 個連結（依事件日插進各月）、
多引 4 條來源（共 13 條）；因為改了標題，**30 個既有內容包**裡指向索引的連結文字一併改掉——發布時這 30 個 slug 要和索引一起 `--slug` 重新匯入
（清單在第 2.4 節）。索引的 hero 圖上仍印著「2026-09-14」（批次 3 的圖），這次沒有重畫。

### 留給站主決定的事（發布後仍可修訂）

- **`openai.com/index/*` 的可及性不穩**：前期研究時 403，撰稿與兩輪查核當天（09-18）都讀得到 200 全文，多篇因此改用官方公告頁當 `sources[]`
  （B1 交易狀態的骨幹只掛這一頁）。發布當天用瀏覽器重開一次；讀不到也不影響文章正確性，只影響讀者點得開與否。
- **B1 揭露本站後端用 uv 與 Ruff**（正文與 FAQ 各一處，查核者對過 `pyproject.toml`／`uv.lock`）：屬實、也是誠實揭露，但等於公開站方工具鏈，站主可刪。
- **B2** 沒寫約 47 億美元循環信貸額度與 SoftBank 3/27 過渡融資（兩輪查核都判「不寫不會誤導」）；10 月 1 日 SoftBank 第三批與 Amazon 剩餘 350 億到位後要重查。
- **B6** 的 `sources[1]` 是 EDGAR 全文檢索 **API 端點**（讀者點開是 JSON）；換成 `www.sec.gov/edgar/search/` 介面要同步改研究紀錄的 fact url，而那頁是 JS 應用、curl 讀不到。四條來源都沒解釋 Form D，要解釋得換一條來源（例如 17 CFR 239.500）。
- **B3** Figure 2 的六個百分比只存在 PNG（第二輪代理實際開圖核對過）；「現在還是不是預設模型」官方沒有句點。
- **B4** 指派要求的 8/11、8/18 兩則更新因 `sources` 上限 4 條被移出，正文完全不提；要補得換掉一份開發者文件。
- **B7** `investors.broadcom.com` 拒絕 `Mokaair-editorial` UA（五次重現），查核用 curl 預設 UA；段落 2,984／3,000。
- **B8** OfficeQA Pro 那張圖官方沒註明誰做的；21.6% 圖說與圖表矛盾（只採 55.6%）；`sources[]` 只剩 2 條（下限）。
- **A1** 發表文自帶 `Updated September 17, 2026`，是活文件；定價頁頁尾 `Last updated 2026-09-16`。
- **zh-CN 的「查核」**：這批四篇（B1、B9、B10、A1）用「查核」、其餘用「核查」（normalize 統一）或「核实」（B5、B6、B8、A3）；每篇內部一致、跨篇不一致。
  審稿者建議全批統一「核实」；本站 tech 批次 131 處用「查核」、crypto 用「核查」——三批各異，要不要統一請站主定。
- **ko 的「本文」**分「본 기사」與「이 글」兩種，**ja 的「本文」**同樣有兩種寫法，各篇內部一致，沒有統一。

## 1d. 9 月 16 日起的十三篇（批次 4.5）：AI 六篇、科技四篇、幣圈三篇，三個索引原地增補

PR #550（squash 為 `f5cf4950`）。**2026-09-18T08:41Z 部署（`deploy_20260918_083808`，無 migration）、`guides-import --slug` ×16 同一次匯入發布**（13 篇 65 個語系 create、三個索引 15 個語系 update、`taxonomy_updated` 13、`failed: null`；腳本先核對 dry-run 計畫才 `--publish`），正式站 80 個網址（13 篇＋3 索引 × 5 語）全數 200、都在 sitemap、hero 圖 200；AI 索引本來就沒有 summary／FAQ 區塊，驗證腳本對它的三個提示是既有狀態。這一批只寫 2026-09-16 之後的新消息（站主決定不做 4.4 那 15 則 8/1–9/15 的次要新聞）：三位探索代理掃官方 feed 後由站主圈選 13 篇，
每篇五語、**兩輪**獨立查核（一律第二輪）、逐語審稿（一語兩組、八位）；13 篇都過 `check_article.py --full --assets`，`pack_cli lint --kind life` 0 error。
與 4.1–4.3 的差異寫在 [`agents/DELTA-4-5.md`](agents/DELTA-4-5.md)：沒有前期 corrections 段落、研究紀錄直接寫在各垂直工作區、
`display_order` 由 `check_article.py` 的 `RELATED` 決定（AI 161–166、科技 313–316、幣圈 211–213）、第二個結尾連結指向既有文章（兩篇指向同批）。

| slug | order | 查核（第一輪；第二輪） | 逐語審稿採用（en／ja／ko／zh-CN） |
| --- | --- | --- | --- |
| `ai-news-chatgpt-sponsored-agents-20260916` | 161 | 95／22；再改 3 | 0／6／1／6 |
| `ai-news-firefox-smart-window-mistral-20260916` | 162 | 94／15；再改 6 | 4／1／5／3 |
| `ai-news-openai-misalignment-reports-20260917` | 163 | 118／31；再改 11 | 5／7／1／1 |
| `ai-news-anthropic-pace-metrics-20260917` | 164 | 101／23；再改 5 | 0／7／7／2 |
| `ai-news-astra-for-law-20260917` | 165 | 146／28；再改 12 | 0／2／5／0 |
| `ai-news-google-cc-family-agent-20260918` | 166 | 139／16；再改 19 | 8／6／7／1 |
| `tech-news-apple-att-eu-20260916` | 313 | 84／26；再改 6 | 0／3／3／0 |
| `tech-news-app-store-bundles-multiseat-20260916` | 314 | 95／16；再改 12 | 4／29／6／1 |
| `tech-news-eu-kids-act-20260917` | 315 | 124／16；再改 5 | 4／4／10／1 |
| `tech-news-taiwan-matsu-cable-tm4-20260918` | 316 | 96／12；再改 5 | 3／5／5／0 |
| `crypto-news-fca-perimeter-guidance-20260916` | 211 | 96／18；再改 8 | 1／1／32／0（ko 主要是 암호자산→가상자산） |
| `crypto-news-cftc-passive-software-20260917` | 212 | 95／20；再改 13 | 0／6／22／1（ko 主要是 노액션레터→비조치의견서） |
| `crypto-news-fca-p2p-crypto-crackdown-20260917` | 213 | 109／17；再改 8 | 0／5／16／1 |

查核報告在 [`factcheck-draft/`](factcheck-draft)（每份都有「第二輪」一節），研究紀錄在各垂直工作區的 `research/`
（[`../ai-news-2026-09-late/research/`](../ai-news-2026-09-late/research)、[`../tech-news-2026/research/`](../tech-news-2026/research)、
[`../crypto-news-2026/research/`](../crypto-news-2026/research)）；候選清單在 `candidates-since-0916-{ai,tech,crypto}.md`，前期研究紀錄在 [`research/`](research)
（兩個沒選的候選 `tech-news-moda-mydata-student-loan-20260917`、`tech-news-taiwan-gsn-idc-20260916` 留著）。
審稿採用的 248 筆（八位：ja／ko 用 opus、en／zh-CN 用 sonnet，AI 六篇一組、科技四篇加幣圈三篇一組）同在 [`translation-corrections.json`](translation-corrections.json)，協調者自己的修訂在 [`coordinator-corrections.json`](coordinator-corrections.json)（含 ko 三篇 74 處「공식은／공식이」主語改成公司名、四個譯文標題的用語統一）。

**三個索引都原地增補**（`update_index.py`，不重跑 `build_*_index.py`——那兩支會整份重寫 zh-TW、蓋掉 relink 與譯文）：
AI 索引把「2026-09-15 與 2026-09-18 兩度增補」改成「之後多次增補（最近一次 2026-09-18）」——下次只換 `EXPANDED_ON` 這個常數——第二段加一句點名六篇、
9 月組尾端加六個連結、多引六條來源；科技索引在平台、台灣、歐盟三組各插一段新敘述（`INSERT` 表，五語）、四個連結進所屬組、查核句加增補日；
幣圈索引新開「英國」組（散文一節＋連結列一節）、CFTC 職員函併進「美國：證券法的解釋、提案與 CFTC 職員函」、開頭的月份範圍與地區數改掉、description 加英國。
`update_index.py` 這次多了 `INSERT` 表（`link:`／`heading:`／`paragraph:` 三種 anchor）與 `NEW` 的逐語系 heading anchor；`COUNT_RULE` 只守 AI 索引
（科技、幣圈索引的「那一篇」「兩篇微軟公告」會被篇數規則假命中）。

### 留給站主決定的事（發布後仍可修訂）

- **活頁面，發布當天要重讀**：sponsored（`testing-ads-in-chatgpt` 是持續疊加更新的頁，市場清單與「台灣不在清單」最可能先過期）、google-cc（`gemini.google` 產品頁無日期、頁尾細則會無預警改）、
  astra（外掛目錄）、kids（四頁 `Last update` 2026-09-17）、fca-p2p（9 月新聞稿沒有修訂紀錄區塊，4 月那篇是發布後 26 天才補關鍵但書）、perimeter（法規資料庫頁尾「整編資料截止日」每週五更新；
  9/30 申請窗口開放後 FAQ 第一題與第 5 節要改；10 月諮詢一開第 4 節過期）。
- **misalignment** 的發布時刻（UTC 9/16 17:00＝台北 9/17 01:00）只印在 OpenAI 官方新聞 feed，feed 不在 `sources[]`（規格禁止 feed 進 sources、四條已滿）；正文三處都點名「官方新聞 feed」。
  `GPT‑5.6 Sol`／`5.6-sol`／`5.6-Sol` 三種官方寫法並存，文中是本站排版。段落 2,995／3,000。
- **pace-metrics** 的「2026 年 7 月 13 日至 20 日」年份是依同頁其他處 `July 2026` 補的（原文那句沒印年份）；8 月風險報告 PDF 三輪都沒讀；三步驟計畫是本站 9/12 那篇的內容，正文已改成「出自本站另一篇整理」。
- **astra**：公告點名的 Harvey／Legora 等 API 客戶與「法律科技公司」對象因字數沒寫進去（研究紀錄有），日後擴寫不可反寫成只有事務所能用；24% 參考判例數字未寫。
- **firefox**：`sources[0].title` 用的是 mistral.ai 的 `<title>`，另外兩條用 `<h1>`（三條裡二比一）；Mistral 兩度自稱觸及 Firefox 使用者 `worldwide` 與四國市場句不一致，字數已滿沒進文章。
- **bundles**：「組合方案／套組／群組購買」是本站自譯（Apple 繁中頁只有「多名額購買／名額／群組購買者／大量採購／Apple 商務／Apple 校務管理」）；繁中說明頁自己前後矛盾（家人共享能否與多名額購買並存），本文以英文版為準、不判斷哪版正確；
  繁中頁另寫 Apple「會」自動關閉已開啟家人共享的既有訂閱的多名額購買，查證屬實但字數沒放。zh-CN 用 Apple 簡中公告那套（套装／套件／多席位购买／席位／批量购买／群组购买），與說明頁的「多名额购买／名额」不同，第二段有說明。
- **att-eu**：RSS `pubDate` 是台北 9/17 01:00，文章採 Apple 印的 9/16；「允許 App 要求追蹤」這類中文設定名是本站翻譯（兩頁都只有英文）。
- **kids**：factsheet FS/26/1891 仍 404；提案本體、Communication、SWD 三份未讀，全篇不引條號；第五個官方頁 `/en/policies/kids-act` 多寫了「也適用應用程式商店與作業系統」與「部分服務擬豁免」，`sources[]` 已四條沒換。
- **matsu**：標題的「完工」是編輯用語（中華電信寫「完成建置、登陸、測通」），callout 已劃界；數發部兩個海纜子頁未開；數發部若補發新聞稿，第 5 節末段與 summary 第 4 句要更新。
- **perimeter**：PS26/18 第 5 章列的三項新 SI 排除刻意未寫（`legislation.gov.uk` 不在白名單）；第一輪把台灣對照改成直接引全國法規資料庫（第四條來源），查核日統一 2026-09-18。
- **cftc**：第 5 節講 3/23 聯名解釋令那句的依據是本站既有文章、不在本篇 `sources[]`；26-09 由律師代提且含補充往來，「Phantom 提出的申請」顆粒度較粗；來源自身兩處不一致（`Inc` 無句點、Re: 行印成 `Section 4(k)`）未代為訂正。
- **fca-p2p**：第 4 節第 3 段「規範範圍還在擴大中」是編輯過場句（來源只印 `until October 2027`）。
- **ko 的「가상자산／암호자산」**：perimeter 譯者用了「암호자산」，審稿統一成站上的「가상자산」；**ja 的「莒」**（西莒／莒光）與「虛擬資產服務法」的繁體字會被 `translation_checks.py` 的 cp932 檢查標出，是假陽性。

## 2. 還沒做完的事

### 2.1 上線後仍可修訂的原稿用詞（都不是事實錯誤）

站主已指示發布；下面是審稿代理回報、日後修訂時可以一併處理的原稿（zh-TW）疑點。要改就改內容包、跑 `check_article.py`，再 `guides-import --slug <那一篇>` 更新：

- **FDIC 篇的「清理程序」**：來源原文是 `insolvency proceedings`（GENIUS Act 第 11 條）。en、ja、ko、zh-CN 四個譯文已改用各語言的
  無力清償／倒產用語（insolvency proceedings、倒産手続、도산 절차、破产程序）；zh-TW 的「清理程序」可解作債務清理程序，沒有動，
  要不要改成「破產（無力清償）程序」請站主決定。
- **美國四篇有幾段整段沒有「擬議」字樣**（FDIC 第 4 節的 10% 門檻那句、OCC 第 2 節的 30 天／120 天那句、AML 第 2 節末段、NCUA 第 3 節第 2 段）。
  每篇開頭都有「下面每一項要求都是草案擬議」的總聲明，所以不算錯；四個譯文在這些句子上已補回提案語氣（would／提案／제안），比原稿保守。
- **日本審議會那篇依英文暫譯本寫的三個地方與日文原文有出入**：「逾八成」「超過 350 件」（日文是「以上」）、「犯則調查權限」（日文是「調査権限」）；
  資安那篇的「CSSA…或視需要對話」（日文是「含め…必要な対話」）。zh-TW 照它引的英文來源沒有動，ja 版改依日文原文。
- **兩篇 SEC 文章的繁中用詞不一致**：「Howey 判準」對「Howey 測試」、「必要管理努力」對「重要經營努力」（來源同為 essential managerial efforts）、
  「支付穩定幣」對其他篇的「支付型穩定幣」；permitted payment stablecoin issuer 在美國四篇有「經核准／已許可／獲准／核照」四種寫法；
  outstanding issuance value 三篇三種寫法。要統一得從 zh-TW 起五語一起改。
- **MiCA 篇 callout 標題寫「四個日期」，內文列了五個日曆日期**；同篇 block5 的「該日」最近的先行詞是 2024-12-30（四個譯文已寫明 7 月 1 日）。
- 歐盟兩篇對 CASP（加密資產服務商／服務提供者）與 MiCA 第 63 條 authorisation（許可／核准／執照／授權）的繁中寫法不一致。

### 2.2 會變動的活資料（發布日 2026-09-17 即查核日；日後更新文章時重查）

- C1：金管會證期局名單（10／1／18 家，中文頁標 2026-09-03 更新；**英文版是另一頁**，只列一類、名單標 22 September 2025，
  en 譯文已寫明三類名單與更新日出自中文頁）；全國法規資料庫的「最後生效日期：未定」。
- C2：ESMA 各國過渡期對照表（PDF 內部修改時間 2026-05-19，文章逐列清點 27 列）。
- C7：`sources[3]` 是聯邦公報依案號的官方查詢（2026-09-17 回 1 筆、Proposed Rule）。
- C8：FDIC 刊登清單頁上 RIN 3064–AG19 只有 2026-04-10 那一列（該頁用 en dash）。
- C3：Federal Register API 的 `corrections` 仍為空。
- C5：EBA 不行動函 PDF 是活檔（`Last-Modified` 2026-02-17）。
- C10：金融廳「国会提出法案等」頁第 221 回國會那一區；01.pdf 的 bytes。
- 美國五份草案若出現定案規則或展延公告，文中「未見／草案」的句子要一起改。

### 2.3 匯入與發布（幣圈已完成；科技與 AI 兩個垂直照做）

- 一律 `guides-import --slug …`；先 `--dry-run --publish` 核對計畫只有自己的 slug、動作符合預期，再 `--publish`；部署前查分段發布狀態與 hold 檔。
- **sitemap 不再是阻礙**：上一版交接寫的「1,000 列上限」在 2026-09-16 就由 `2026-09-14-sitemap-split-before-1000-rows`（PR #531）解掉了，
  `/sitemap.xml` 現在是 sitemap index。這批是 12 個內容包 × 5 語系 = 60 列。
- 同一群文章的互連用內容包的 `related`（延伸閱讀）：`guides-import` 會在該次匯入的文章都存在後第二輪套用，所以十二篇要同一次匯入。

### 2.4 科技的匯入發布，與 AI 12 篇

**科技（4.2）**：已發布（2026-09-18）。十四篇同一次匯入，`related` 在第二輪套上（`taxonomy_updated` 13 篇；
`tech-news-nvidia-vera-rubin-20260915` 的延伸閱讀另外連到已發布的 `ai-news-nvidia-rubin-20260105`，正式站已看得到）。

**AI（4.3）**：已發布（2026-09-18T03:2xZ）。匯入的 `--slug` 清單比前兩個垂直長，日後重新匯入索引時同樣要帶上這 30 個既有包：
12 個新 slug ＋ 改版的索引 `ai-news-2026-january-september-index` ＋ **30 個只改了連結文字的既有包**（不重新匯入的話，
既有文章頁面上指向索引的連結會顯示舊標題「1 月 1 日至 9 月 14 日」）：
`ai-model-release-timeline-2026`、`ai-news-anthropic-threat-report-20260910`、`ai-news-chatgpt-health-20260107`、`ai-news-chatgpt-images-20-20260421`、
`ai-news-chatgpt-work-20260709`、`ai-news-claude-fable-5-access-20260609`、`ai-news-claude-interactive-visuals-20260312`、`ai-news-claude-opus-46-20260205`、
`ai-news-claude-sonnet-5-20260630`、`ai-news-deepseek-v41-flash-20260910`、`ai-news-gemini-31-pro-20260219`、`ai-news-gemini-36-flash-20260721`、
`ai-news-gemini-omni-20260519`、`ai-news-gemini-personal-intelligence-20260114`、`ai-news-gemini-spark-20260519`、`ai-news-google-assistant-gemini-20260904`、
`ai-news-gpt-53-codex-20260205`、`ai-news-gpt-54-20260305`、`ai-news-gpt-55-20260423`、`ai-news-gpt-56-sol-preview-20260626`、`ai-news-gpt-live-voice-20260708`、
`ai-news-lyria-3-pro-20260325`、`ai-news-meta-muse-spark-20260408`、`ai-news-nvidia-rubin-20260105`、`ai-news-openai-agents-api-20260910`、
`ai-news-pace-the-frontier-20260912`、`ai-news-project-glasswing-20260407`、`ai-news-qwen-35-20260216`、`ai-news-siri-ai-ios-27-20260914`、`ai-news-sources-to-follow`。
這 31 個既有包本來就是「已發布」狀態，`guides-import --slug` 對它們是更新不是新建；這次的 dry-run 計畫是 43 篇、create 60（12 × 5 語）、update 147，核對後才 `--publish`。`related` 在第二輪套上（含連到已發布的 `ai-news-gpt-live-voice-20260708`、
`ai-news-gpt-55-20260423`、`ai-news-gpt-6-astra-20260903`）。發布當天先重開第 1c 節列的活頁面。

## 3. 定下來、接手的人不要再翻案的決定

第一個 session 定的：

- **`checked_on`**：`corrections-crypto.md` 寫「一律填 2026-09-16」，`BRIEF.md` 寫「實際查證當天」。
  依「BRIEF > 修正清單」：C2–C11 的撰稿代理當天重抓每一條 `sources[]` 並讀到 body，所以是 **2026-09-17**；
  C1 維持 09-16（那是它真正的查核日）。
- **美國聯邦規則的事件日＝聯邦公報刊登日**（slug 尾碼與 `news_date`），作成／通過／署名日另外明寫在文章裡。
  `corrections-crypto.md` 對 FDIC 傾向 04-07，站主圈選的 slug 清單是 04-10；照 slug 清單。
- **生效日：照來源印的寫。** FDIC 的聯邦公報文件自己印了 `January 18, 2027, or 120 days after … if earlier`，
  照印並歸因；NCUA 全文沒印日期，只寫公式。不可自己換算。
- **來源自己的矛盾照印不訂正**：FinCEN/OFAC 草案的 1022.220 對 1020.220、EBA 兩份文件的日期、
  OCC 的 PART 15 標題、EBA PDF 的 `andthe`。`corrections-crypto.md` 有兩處要求訂正，與 `BRIEF.md` 型態 7 衝突，照 BRIEF。
- **否定句必須指得到 `sources[]`**：「未見定案規則」這類句子，要嘛把能承載它的官方頁放進 `sources[]`
  （C7 用聯邦公報依案號的官方查詢、C8 用 FDIC 的刊登清單頁），要嘛限縮成現有來源撐得住的說法（C9、C6）。
- **C1 的第二個連結改指 MiCA 那篇**：原本指向的〈電子支付與電子票證〉只有 zh-TW，四個譯文沒有標題可連。
- **C11 不點名個案**：報告的十個個案（交易所、協議）整串拿掉；報告自己聲明個案不代表責任歸屬，一串名字會被讀成黑名單。
- **用語**：日本法的「暗号資産」在繁中一律譯「加密資產」（首次出現附日文），「虛擬資產」留給台灣的法律；
  OCC 的中文名統一為「通貨監理局」、NCUA 為「全國信用合作社管理局」。
- **標題、摘要、圖上不放來源沒印的清點數字**（「27 國四種緩衝」「四層申報」都拿掉了）；
  來源自己編號的（條文的 (1)–(10)、`five key elements`）可以寫。
- **主管機關文件裡的行情數字一律不寫**（市場規模、市值、交易量、轉引 CoinMarketCap／TRM 的數字）；
  開戶數、帳戶分布、罰鍰、資本額門檻這類不是行情，可以寫。

第二個 session 定的：

- **全批統一用語**（審稿代理照這張表改，表在 [`agents/REVIEW.md`](agents/REVIEW.md)）：payment stablecoin＝決済用ステーブルコイン／
  지급결제용 스테이블코인／支付型稳定币；NCUA share insurance＝出資金保険／출자금보험／股金保险；IDI＝付保預金取扱機関／부보예금취급기관／受保存款机构；
  final rule＝最終規則／최종 규칙／最终规则；洗錢的日文用金融庁的「マネー・ローンダリング」；no-action letter 的韓文是金融委員會的「비조치의견서」；
  日本法律在 zh-CN 用通行譯名《资金结算法》《金融商品交易法》並在首次出現附日文原名。
- **「本站沒有實測」**：ja「当サイトは実地の検証を行っておらず」（「実機検証」會被讀成在講機器）；
  ko「본 사이트는 직접 시험해 보지 않았고」——**不要用「검증」**，它會被讀成「本站沒有查證」，與文章自己的「확인일」打架；查核一律「확인」。
- **免責 callout 的「當期公告」**：ja「その時点の」（「当期」是會計用語）、ko「그때그때의 공고」（「당시」是過去那時、「당기」是會計期間）。
- **日本兩篇的日文版以金融庁日文原文為準**：機關名、會議名、報告用語（情報提供、事務ガイドライン、一定の熟慮期間、お墨付き、記述子…）
  都對回日文報告與取組方針別紙１，不從英文或中文回譯；數量限定詞也照日文原文（「以上」）。
- **同群文章的互連用 `related`，不用 autolink**：`pack_cli autolink` 對這批只找到一條——台灣那篇法條引文裡的「澳門」連到澳門一日遊——不套用。
  GENIUS Act 四篇互連，SEC 兩篇、歐盟兩篇、日本兩篇各自互連；台灣那篇與索引不設。
- **標題可以改，改完跑 `align_links.py --apply`**；只有索引的五個標題不動。這一輪依審稿建議改了 11 個譯文標題（清單在 `coordinator-corrections.json`）。
- **譯文不新增原稿沒有的句子**：退回的那 1 筆就是這個原因；但把一句原稿拆開後掉了提案標記的，補回「would／提案条文では／제안된」是該做的。

科技那一輪（第三個 session）定的：

- **科技沒有免責 callout**，每篇只有一個一般的 callout（查核日、取材範圍、本站沒有實測、不提供購買建議）；索引同樣只有一個。
- **`display_order`**：十三篇 300–312（`check_article.RELATED` 的順序），索引 299。
- **台灣讀者視角帶進每個語言**：台幣售價不換算、不換成當地售價；台灣的預訂／供貨日、「台灣不會一開始推出」照譯；
  譯文不自己補上日本、韓國或美國的上市資訊（Pixel Drop 那篇日本在名單上、韓國不在，譯文都沒有加註）。
- **公司與產品名在四個譯文語言一律用拉丁原名**（Apple、Google、NVIDIA、Microsoft…），功能名以廠商自己的該語言 newsroom 為準、查不到就留英文；
  zh-TW 保留「微軟」。人名可以用該語言表記；台灣人名在 ko 照華語發音（예닝(葉寧)），不用漢字音讀。
- **引文**：來源是英文的，en 一律用研究紀錄 `verbatim_quote` 的原文，不從中文回譯；文章在比較「繁中版新聞稿」與「英文版」用字的地方，
  被引用的繁中原文保留中文、附該語言的意思。
- **全批統一用語**（表在 [`agents/tech/REVIEW.md`](agents/tech/REVIEW.md)，收件後再補的）：查核日＝ja「確認日」（**「査読」是論文同儕審查，不能用**）、ko「확인일」、zh-CN「查核日」；
  「本文」＝ja「本記事」、ko「본 기사」；法規「上路」＝zh-CN「开始适用」（「上线」是系統上線、「生效」是另一個法律概念）；
  AI factory＝ja「AIファクトリー」、ko「AI 팩토리」、zh-CN「AI 工厂」，首次出現交代是 NVIDIA 對 AI 機房的稱呼；NVIDIA 的 projections＝ja「予測」、ko「추정」；
  unified memory＝ユニファイドメモリ／통합 메모리／统一内存；百萬瓦＝MW、十億瓦＝GW（zh-CN 兆瓦／吉瓦，「兩兆參數」寫「两万亿」）。
- **標題不寫來源撐不住的動詞**：CUDA-Q 那篇原標題「NVIDIA 開源 CUDA-Q Logical」在逐語審稿時被指出來源只說「為開源的 CUDA-Q 平台新增」，五語標題都改了；
  Apple 歐盟條款的 en／zh-CN 標題被譯者加上「Cut to／降至 5%」，原稿沒有方向（文章還明寫無法判斷升降），也改掉。
- **圖上的數字不能比正文強**：Vera Rubin 那張圖的「40%」原本少了「最高」，五語都補回。
- **排版**：zh-TW 與 zh-CN 的中文與英數之間留半形空格（`space_cjk` 類腳本，「」內的引文不動）；zh-CN 引號用“ ”；ja 相鄰日文的括號、冒號用全形（`Regulation (EU)`、`第14条第2項(a)` 保留半形）。

第三個 session（AI 4.3）定的：

- **zh-CN 的「查核」不再整批改字**：`normalize_locales.py` 只把「核查→查核」（沿用 4.2），審稿交的「查核→核实」40 筆沒有套；
  「事实核查」是 fact-checking 的通行譯法，不受這條規則影響（B3 一處保留）。三批 zh-CN 的用字本來就不同（4.1 核查、4.2 查核、4.3 混），要統一是站上另一件事。
- **既有 AI 索引不再顯示篇數**（`ai.md` 第 2 點、站主 2026-09-16 的決定）：月份表整欄拿掉而不是把 38 改成 50，`update_index.py` 的 COUNT 規則會擋住任何殘留的篇數。
- **AI 篇的 `topics`** 只有 `["ai","ai-news"]` 或再加 `software`／`gadgets`；B8 不掛 `finance`（`ai.md`）。
- **標題改了兩篇**：B7 原「做模型的公司為什麼也要做晶片？」問了正文沒回答的問題、B4 原「怎麼買」讀起來像投放教學，都改成描述公告內容；研究紀錄的 `title` 已同步。

## 4. 學到的（寫給下一個協調者）

科技那一輪（2026-09-17／18）新增的：

- **撰稿與翻譯換成 sonnet、查核與審稿用 opus、協調者只做協調，是划算的，但兩輪查核變成必要。** 十三篇第一輪每篇改 11–30 處，
  **第二輪每一篇又再改 8–18 處**，而且抓到的不只是限定詞：一條用刪節號把兩句拼起來的假引文（Apple 硬體篇，連帶正文「測試版軟體」是錯的）、
  黃仁勳的「一座十億瓦…一座二十億瓦」被寫成兩座十億瓦、第一輪自己新寫的全稱否定句被同一份來源推翻（CUDA-Q、馬祖、6G 各一）。
  第一輪「新寫進去的每一句」沒有人查過，第二輪的規格要明寫逐句回來源；`verbatim_quote` 要用程式做連續字串比對，含 `...`／`|` 的引文逐片段另外看。
- **sonnet 譯的 CJK 會有成片的錯字**，不是文風問題：馬祖海纜的日文把「北竿／南竿／莒光」打成「北竹／南竹／莠光」、日期漏數字，
  英文與韓文裡引用的中文原文出現「海翆」「搖通」「阿聯酫」，韓文有「겑자기」這種不存在的音節。逐語審稿抓到了，但收件後值得再跑三個機械檢查：
  ja 用 Shift_JIS 編不出來的漢字、ko 用 EUC-KR 編不出來的音節、en／ko 裡引用的中文字串是否出現在 zh-TW 原稿；錯得多的那一篇再派一次審稿。
- **審稿也會錯**：en 審稿依研究紀錄回報 iPhone Duo 原稿把「低光源表現」掛錯相機，協調者重抓 Apple 英文稿核對，**原稿對、錯的是研究紀錄那條拼接引文**。
  審稿回報的「原稿疑似有誤」要回一手來源查，不要直接照改。
- **譯者會自作主張**：把 NVIDIA 的 AI factory 全部在地化成 data center、自己回英文稿把轉述補成直接引語（多出原稿沒有的字）、
  替標題加方向性動詞、漏掉清單的最後一項（CUDA-Q 四語都漏了 Sandia，譯者還回報成「原稿漏了」）。翻譯規格要寫「不增刪、不加方向、清單逐項對」。
- **給讀者的來源連結要用讀者的瀏覽器開一次**：`publications.europa.eu/resource/celex/…` 對 curl 正常，對語言偏好是 zh／ja／ko 的瀏覽器回純文字錯誤。
- **字數上限含空格**：兩篇沒留中英文間空格的原稿補上空格後超過 3,000，是刪重複敘述（不是但書）騰出來的，刪了什麼記在 `coordinator-corrections.json`。
- **修正超過欄位上限時 `apply_corrections.py` 會整筆跳過**（alt 200、description 500）：看 `SKIPPED` 行，協調者改短後自己套。
- **用量（Max 方案）**：十三位 sonnet 撰稿約 5 點、十三篇兩輪 opus 查核約 60 點、十四位 sonnet 翻譯約 25 點——一個 5 小時窗剛好用完（94%）；
  十二位 opus 審稿平行跑約 35 點，要排到下一個窗。週額度一整個垂直約用掉全模型 20 點、協調者自己（Fable）約 6 點。
  協調者的脈絡看圖很貴（一張 contact sheet 約 2–3 千 tokens），先用小腳本出預覽、只看必要的語言。

幣圈那兩輪學到的：

- **第二輪查核不是形式。** NCUA 第二輪推翻的，正是第一輪自己新寫進去、沒人查過的那一句；
  SEC 提案第二輪抓到三個「第一輪報告寫對、套進內容包時沒套滿」的限定詞。
- **翻譯是第三道查核，逐語審稿是第四道。** 審稿這一關抓到一個**兩輪查核都放過的原稿事實錯誤**：日本審議會那篇把揭露三種情形的義務主體
  照參考資料的表逐欄對應，寫成「發行人未募資時由業者公表發行人編製的資訊」；日文審稿代理對照日文報告提出異議，協調者回英文版第 18、57 頁查證屬實
  （那種情形是業者自行編製並公表），五語一起改、研究紀錄加註。**PDF 表格抽出來的文字順序不等於欄位對應，要回正文找同一件事的句子。**
- **審稿代理要讀逐段對照檔，不要讀內容包 JSON。** [`review_dumps.py`](review_dumps.py) 把每一格印成「ZH／譯文」一組，`old` 可以直接複製；
  一個語言分三組（一組四篇，約 9–10 萬 tokens 的閱讀量），比一位代理讀十二篇穩，也比較便宜。跨組一致靠事先發下去的統一用語表，
  收件後用 `term_grep` 類的腳本掃一次殘留（這輪掃出 ko 的 15 處站方語氣、5 處免責句、FDIC 的 insolvency 用語）。
- **審稿建議不要照單全收地統一站方語氣**：協調者發下去的 ko「직접 검증하지 않았고」被一位審稿代理指出會讀成「沒有查證」，最後全批改掉。
- **`check_article.py` 看不到的兩件事**：摘要裡的中文數字（「一成」躲過數字比對）；摘要的事實有沒有出現在正文（只比對阿拉伯數字）。
- **撰稿者系統性地壓掉但書來湊字數**（每篇都卡在 2,9xx／3,000）。查核規格要明寫「字數爆了就精簡敘述，不可刪但書」，
  第二輪專門回頭掃 `except`／`unless`／`or`／`may`／`in its discretion`。
- **環境**：`pypdf` 在系統 Python（`python`），不在 `apps/api/.venv`；多個代理同時跑不要用 `uv run`（搶鎖），直接用 venv 的 python；
  Windows 上 `CHROMIUM_BIN` 要指到 Playwright 的 headless shell 或 Edge；聯邦公報正規頁回 `Request Access` 擋阻頁，
  全文用 `federalregister.gov/documents/full_text/text/…txt` 或 govinfo 的 PDF；`sec.gov` 對 curl 回 403。
  重跑 `build_assets.py` 不會動到沒改字的 JPG（位元組相同）；`git status` 裡一整排 SVG「修改」只是工作樹的 CRLF，`git add` 後就消失。
- **用量**：一篇走完撰稿、查核、翻譯約 90–130 萬 subagent tokens（第二輪另加 25–30 萬）。逐語審稿 12 位代理每位 29–39 萬 tokens、各跑約 25 分鐘，
  **平行跑會在 25 分鐘內吃掉 Max 方案 5 小時額度的七成**（7% → 74%）。開工前用 `get_usage` 看額度；一次開 4–6 位、分兩波比較安全；
  額度逼近時先叫所有代理「現在就把已確認的寫檔、照實回報沒看完的地方」，比被切斷後續跑划算。被切斷的代理用 `SendMessage` 對原 id 續跑。
- **代理遇到「Output blocked by content filtering policy」**（兩次，都在大段逐字貼來源原文的時候）：
  檔案通常已經寫好，重派或續跑時要求它用「位置＋前後十來個字」描述，不要整段貼。
