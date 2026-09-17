# 獨立查核：tech-news-nvidia-cuda-q-20260914

查核代理：未參與撰稿。來源重抓於 **2026-09-17 深夜**，報告寫於 **2026-09-18**
（文章的 `checked_on` 維持撰稿者實際讀到來源的 **2026-09-17**，四處一致，不改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body
（任何請求都沒有帶入 email、姓名或其他個人資料），HTML 去標籤後逐句比對，
24 條 `verbatim_quote` 另外用程式做「原樣搜尋得得到嗎」的檢查。
**沒有使用任何 `sources[]` 以外的新網址**，也沒有猜任何識別碼。

檢查的主張：**123 條**（正文 36 句、摘要 5 句、FAQ 6 題共 14 句答句、callout、
表格 13 格與 caption、圖解 caption 與 alt、title 與 description，
以及研究紀錄的 24 條引文、8 條 `not_said`、4 條 `live_data_warnings`、圖解四格與 `hero_label`）。
**改了 30 處**（內容包 26 處、研究紀錄 4 處），另有 5 件留給站主。

## 重抓結果（四條 sources 都還在、內容沒變）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| nvidianews 新聞稿 | 200 | 81,400 | 是（無轉址） | 刊頭 September 14, 2026；Costa／Grassellino／Proctor 三段引言；六個機構名單與漏掉的逗號；1,000／150,000／10x；Availability 一句；前瞻性聲明第一項 |
| cuda-quantum 0.16.0 logical/index.html | 200 | 50,833 | 是 | 「Preview release」提示框；In this preview 那一句；`pip install cudaq`；範例程式碼檔頭的 Apache License 2.0 |
| cuda-quantum 0.16.0 …/reference/capabilities.html | 200 | 37,029 | 是 | resource-estimation toolkit 定義句；不送硬體／不執行物理模擬／沒有偵測器與解碼語意三句；未測試功能清單 |
| cuda-quantum latest/releases.html | 200 | 144,916 | 是 | 0.16.0 條目下的 This release integrates CUDA-Q Logical version 0.1.1 |

四條的位元組數與撰稿紀錄完全相同，版本鎖定的 `/0.16.0/` 兩頁今天仍與紀錄一致。

**引文可搜尋性**：24 條 `verbatim_quote` 裡 23 條在頁面呈現文字中是連續字串，
其中 F01、F05、F13、F14 四條中間夾著 `<a>`／`<sup>` 標籤，**對原始 HTML 搜尋會找不到**，
翻譯階段要從呈現文字複製。只有 Apache 授權那條不是連續字串（見下方第 17 點）。

## 改掉的 30 處

**推翻的事實（5 處）**

1. **表格第 3 列「不是它的估算對象」**（物理量子位元欄）→「估算要用掉多少顆、多少時間」。
   新聞稿寫 Fermilab 用它 `evaluate physical qubits, runtimes and other resource requirements`，
   Iceberg 的例子估的正是 150,000 個物理量子位元——**物理量子位元就是這套工具的估算對象**，
   原本的寫法和同一篇文章自己的數字互相矛盾。同列邏輯量子位元欄改成「固定住程式再比較不同方案」
   （文件：`keeps the workload fixed while these system choices change`）。
2. **「Iceberg Quantum ⋯替 Diraq 的量子位元架構建模」→「針對 Diraq 的量子位元替自家容錯架構建模」**
   （摘要第 3 句、第 3 節第 1 段、FAQ 第 3 題三處）。原文是
   `Iceberg Quantum modeled its fault-tolerant architecture for Diraq's qubits`：
   被建模的是 **Iceberg 自己的**容錯架構，Diraq 提供的是量子位元。原本的寫法把功勞與標的都換了家。
3. **「依兩者的連結分開列出」**→「原文中 Quantum Motion 是連往該公司網站的超連結，本文因此分開列出」。
   原始 HTML 裡只有 `Quantum Motion` 帶 `quantummotion.com` 的錨點，**`QCDesign` 是純文字**，
   「兩者的連結」不存在。分開列出的判斷本身正確，理由寫錯了。
4. **刪掉 Iceberg Quantum 的「新創公司」**。新聞稿沒有給它任何公司規模或階段的描述。
5. **「本身帶有雜訊」→「本身帶有固有的錯誤」**（表格、圖解 alt、研究紀錄圖解節點）。
   來源的用語是 `the errors inherent in physical qubits`；`noise` 在新聞稿 0 次，
   在 capabilities 頁唯一一次是 `that is a parameter surface, not a noise model`，語意相反。

**被刪掉或放寬的限定詞（4 處）**

6. **「都會改變同一個運算需要多少顆量子位元」→「都可能改變」**。文件原文是 `can all change`。
   同段歸屬也從「NVIDIA 表示」改成「技術文件說明」——解碼與「多少量子位元與多少執行時間」
   出自說明頁的 co-design 段，不在新聞稿裡。
7. **補回 `useful`**：「協助開發適用於容錯量子電腦的**有用**應用程式」（`developing useful applications`）。
8. **補回 `for performance with logical qubits`**：「找出**在邏輯量子位元上**效能最佳的系統組合」。
9. **補回 `in upcoming versions`**：「API、行為與文件都可能**在之後的版本**大幅變動」。

**收窄或放大來源範圍（7 處）**

10. **「CUDA-Q Logical 目前的版本號是 0.1.1」→ 綁回版本紀錄頁的說法**：
    該頁寫的是 **CUDA-Q 0.16.0 這一版**整合 CUDA-Q Logical 0.1.1；頁面上方另有 `latest`
    （main 分支的每夜建置），所以不能寫成「目前的版本號」。摘要、第 5 節、FAQ 第 5 題、callout 四處同步。
11. **「NVIDIA 只提供 CUDA-Q 裡的參考實作」→「公告只寫到『NVIDIA CUDA-Q 裡可以取得 QUOPS 的參考實作』」**。
    內文原句是 `A QUOPS reference implementation is available in NVIDIA CUDA-Q`，
    沒有說 NVIDIA 的角色僅止於此。摘要第 4 句與 FAQ 第 4 題同步。
12. **「量子效能基準 QUOPS」→「跨平台基準 QUOPS」**（description 與第一段）。
    來源自稱 `a new, independent cross-platform benchmark`；「效能」是桑迪亞那個實驗室的名字，
    不是 QUOPS 的定義。第 4 節引文另補回「一個**新的**、獨立的跨平台基準」。
13. **「新聞稿形容可用性只有一句」→「新聞稿描述可用性的只有一句」**，並把
    「也沒出現『預覽』兩個字」改成「全文也沒有出現 preview（預覽）這個字」。
    Availability 段其實有三句（另兩句講 QUOPS 倉庫與論文），只有講 CUDA-Q Logical 可用性的是一句；
    `preview` 在新聞稿頁逐詞查核 0 次。
14. **Grassellino 的「只花三週」補回它的對象**：原文是
    `explored combinations of these resources in just three weeks`，
    已改成「團隊用 CUDA-Q Logical 探索這些資源的組合『只花三週』，相較之下自行建置專屬基礎設施
    『通常大約需要五個月』」；她第一句引言的前提也改成「**要走到**容錯量子運算」
    （`but getting there will require…`）。對照估計、不是計時測量的但書保留。
15. **Proctor 的主詞**：「業界需要能追蹤與預測⋯」→「他們與其他量子運算相關方必須能追蹤並預測⋯」
    （`we, and other quantum computing stakeholders`）。同段改成「初步 QUOPS 結果」。
16. **表格第 2 列「目前多數運算依賴的基礎單位」沒有來源**→「過去衡量進展主要看它」
    （`Historically, progress … measured primarily through advances in physical qubits`）；
    邏輯量子位元欄改成「用錯誤更正克服物理位元的錯誤」。

**研究紀錄（4 處）**

17. **F17 的 `verbatim_quote` 不是連續字串**。它寫成
    `This source code and the accompanying materials are made available under the terms of the Apache License 2.0 which accompanies this distribution.`，
    但頁面上那是內嵌範例程式的註解框，**每一行前後各有一個 `#`、行尾補滿空白，而且分成兩行**，
    這個句子在頁面上搜尋不到。已改成單行可搜尋的
    `the terms of the Apache License 2.0 which accompanies this distribution.`，
    並在 `fact` 裡寫明它印在 `examples/02_surface_code_resource_estimate.py` 的註解框裡。
18. **`not_said` 的「沒有任何來源提到台灣、台積電、聯發科」被新聞稿頁自己推翻**：
    該頁右側「More News」區塊有一則 2026-08-31 的其他公告標題含 `MediaTek`。
    Taiwan／Taipei／TSMC 四頁確實各 0 次，已把這條限縮成「新聞稿正文成立、整頁不成立」。
19. F7 的 `fact` 同步改成「針對 Diraq 的量子位元為自家的容錯架構建模」並附原文。
20. 圖解節點「本身帶有雜訊、容易出錯」→「本身帶有固有的錯誤」。

**其他補正與精簡（10 處）**

21. 第 3 節第 3 段補回文件列出的另一個入口與正確的元件名：「或直接撰寫可攜的邏輯程式」、
    「設定錯誤更正碼、元件與擺放方式、蒸餾（distillation）協定」，
    並把「估算完的程式」改成「展開後的程式」（`emit realized programs`）。
22. 第 3 節第 2 段補上費米實驗室評估的具體項目：「需要多少物理量子位元、執行時間等資源」。
23. 第 5 節第 2 段三句引文重譯得更貼原文：「它仍然是編譯與估算的產物：CUDA-Q Logical 不會把實體排程
    送上硬體，也不為它提供執行期服務」、「套件裡沒有任何東西會**取用**或執行物理模擬」
    （`consumes or executes`），並把「留到 Stim 這類下游工具」改成文件自己的界線
    「這些要在輸出的 Stim 文字之後、於 Stim 生態系裡才開始」，補上文件明列的四件事
    （標註偵測器與可觀測量、產生偵測器錯誤模型、取樣、解碼）。
24. 前瞻性聲明的結論改成照原文說：「NVIDIA 自己把這類陳述歸為非歷史事實，不保證日後的結果」。
25. 第一段與摘要第 1 句補上「設計」這個用途（`researchers can now design and orchestrate…`），
    並把「不是推出新的量子電腦」改成可查證的寫法「公告裡沒有出現新的量子電腦或硬體產品」。
26. 「廠商與實驗室」→「QPU 製造商與實驗室」（`QPU makers and labs`），
    並補上「NVIDIA 沒有說總共有幾家」。
27.–30. 為了讓補回的限定詞放得進 1,800–3,000 字，精簡了九處贅語
    （重複的機構全名、「資料來源是⋯官方新聞稿全文」、「這一點在下一節說明」等），
    **沒有刪掉任何但書、限定詞或條件**。最終 zh-TW 段落字數 **2,999**。

## 查過而且正確的部分（沒有動）

- **事件日沒有混用**：2026-09-14 是新聞稿頁面自己印的刊頭日期，`news_date`、slug 尾碼與第一句一致；
  文章沒有引用 RSS 的 `pubDate`／`modDate`，也沒有寫「發布後修訂過」這個推論。
- **沒有自算的數字**：1,000、150,000、「大約 10 倍」逐字對回新聞稿；
  文章與紀錄都沒有出現 150,000÷1,000＝150，也沒有使用摘要條列句的 `7x speedup`。
- **`including` 清單處理正確**：寫成「包括⋯在內」，沒有寫成「共六家」或「名單為」。
- **QUOPS 的歸屬正確**：桑迪亞開發、NVIDIA 側只有參考實作、公告沒有任何分數或排名
  （逐頁確認新聞稿沒有任何 QUOPS 數值）；也沒有寫進 arXiv 預印本裡物理／邏輯量子位元的區分
  （該頁不在 `sources[]`，紀錄已說明為何迴避）。
- **技術文件三句明文否定逐字命中** capabilities 頁；「資源估算工具」定義句命中。
- **負面句都限縮到具體文件**：`preview`、`Apache`、`price`／`pricing` 在新聞稿頁逐詞 0 次；
  `Taiwan`／`Taipei`／`TSMC` 四頁各 0 次；2027 年以後的年份四頁各 0 次——
  所以「沒有時間表」「沒有提到台灣」成立。
- **`checked_on` 2026-09-17 四處一致**（四條 source、研究紀錄、第二段、表格與圖解 caption），
  本輪沒有因為重查而改動它。
- **界線**：全文沒有購買、升級或機型比較建議，沒有把官方定價做成推薦（來源根本沒有價格），
  **沒有投資免責 callout**，callout 只有一個；所有能力、效能與時程敘述都掛在
  「NVIDIA 表示／技術文件說明／Costa 表示／Grassellino 表示／Proctor 表示」之下。
- **預覽狀態沒有被寫成已上市**：摘要、第 5 節、FAQ、callout 四處都寫出預覽版與 0.1.1，
  並標明是查核當天的技術文件狀態。
- **`sources[]` 之外的事實沒有外溢**：quickstart 的 `cu13`／`cu12` 安裝路徑、PyPI 上傳時間、
  GitHub 分支命名、arXiv 預印本細節、IEEE 官網的參加人數，一句都沒有進文章或紀錄。

## 留給站主的 5 件事

1. **`check_article.py` 仍是 FAIL，只剩兩條，都不是本文造成的**：
   tech 垂直索引內容包 `tech-news-2026-index` 還不存在；第二個連結的 `text` 要等
   `tech-news-nvidia-vera-rubin-20260915` 定稿後換成它的正式 title。兩者都在協調者的階段處理，
   查核前後完全相同。
2. **zh-TW 段落字數 2,999／3,000，只剩 1 個字的餘裕。** 之後任何補字都必須同時刪掉等量的字。
3. **兩段值得考慮補、但現在沒有位置的內容**：新聞稿內文那句
   `accelerating fault-tolerant algorithm development from five months to three weeks, a 7x speedup`
   （NVIDIA 自己的敘述，比 Grassellino 的引言更強），以及 QUOPS 預印本裡「跨平台結果量的是物理
   量子位元」這個區分（佐證頁不在 `sources[]`，要補就得換一條 source）。兩件都是編輯取捨。
4. **新聞稿的 News Summary 條列與內文有兩處不一致**：`architecture` 對 `algorithm`、
   `QUOPS is now available in NVIDIA CUDA-Q` 對 `A QUOPS reference implementation is available in NVIDIA CUDA-Q`。
   本文一律採內文寫法，但沒有在文章裡點出這個矛盾。
5. **`sources[4]` 的 `releases.html` 仍指 `/latest/`**，是會一直往上長的活頁面；
   0.17.0 一出，0.16.0 那一則仍在，但頁面描述的最新版會變。出刊前值得再抓一次。

## 結論

`needs_second_round`：123 條主張逐條核對後，**骨幹論述成立且沒有更動**——
這是估算工具不是量子電腦、新聞稿與技術文件用詞有落差、QUOPS 不是 NVIDIA 的基準，三件事都查得過。
但被改掉的事實超過十處（5 條推翻、4 個被刪的限定詞、7 處範圍收窄或放大），依規格要再過一輪。
第二輪的範圍很窄：**只需覆核本報告列出的 30 處改寫，不必再抓新來源**——四條 `sources` 今天重抓後
位元組數與內容都與撰稿紀錄一致。

---

## 第二輪

查核代理：未參與撰稿，也**未參與第一輪**。來源重抓於 **2026-09-18**。

四條 `sources[]` 全部再次以 `curl -sL -A "Mokaair-editorial"` 重抓（任何請求都沒有帶入
email、姓名或其他個人資料），並用本輪自己寫的去標籤程式重新產生呈現文字，**沒有沿用第一輪的抽取結果**。

| source | HTTP | bytes | 轉址 | body 是正文嗎 | 與第一輪／撰稿紀錄 |
| --- | --- | --- | --- | --- | --- |
| nvidianews 新聞稿 | 200 | 81,400 | 無 | 是 | 完全相同 |
| logical/index.html（0.16.0） | 200 | 50,833 | 無 | 是 | 完全相同 |
| …/reference/capabilities.html（0.16.0） | 200 | 37,029 | 無 | 是 | 完全相同 |
| latest/releases.html | 200 | 144,916 | 無 | 是 | 完全相同 |

檢查範圍依指派收窄：第一輪改動過的 30 處段落與**新寫進去的每一句**（逐句回原文）、
24 條 `verbatim_quote` 的字串比對、全篇否定句的範圍、`summary` ⊆ 正文與 FAQ ⊆ 正文、
預覽狀態與「估算工具不是量子電腦」兩條骨幹的全文一致性、第一輪有沒有為了字數刪掉但書。
合計覆核 **68 條**，**又改了 15 處**（內容包 13 處、研究紀錄 2 處），
歸納成下面 10 個問題——同一個毛病在摘要、正文、FAQ 重複出現時算多處，但只記一條。

### 引文比對（本項第一輪已做過，本輪重做且加嚴）

24 條 `verbatim_quote` 在本輪自建的呈現文字裡**全部是連續字串，沒有一條是拼湊的**，
24 條的 `url` 也全部在 `sources[]` 內。本輪另加一項第一輪沒做的嚴格測試：
**「這條引文是否落在同一個可見行？」**——因為 `<pre>` 區塊裡的換行是真的看得見的換行，
把兩行接起來才成立的引文就是拼湊。結果：第一輪改過的 Apache 授權那條，
確認**就印在說明頁內嵌範例 `examples/02_surface_code_resource_estimate.py` 註解框的同一行**，
第一輪的修法正確。其餘 23 條不是落在單一可見行、就是同一段 HTML 散文（瀏覽器會併成一行），
沒有任何一條跨可見換行。

### 改掉的 10 個問題（15 處文字）

**否定句的範圍太寬（5 個問題、9 處文字，其中 3 處被新聞稿自己推翻）**

1. **第 1 段「公告裡沒有出現新的量子電腦或硬體產品」→ 刪掉「或硬體產品」。**
   同一份新聞稿寫了 `NVIDIA NVQLink™, the open system architecture for tightly coupling
   quantum processors with GPU supercomputers` 與 `NVIDIA Ising`，
   「沒有硬體產品」這個範圍**會被自己引用的來源推翻**。
   第一輪為了把「不是推出新的量子電腦」改成「可查證的寫法」，反而把否定範圍擴大了。
   第 1 節第 1 段的對應句「新的量子電腦或硬體產品線」同樣收窄（同一個問題的第二處）。
2. **「公告只寫到『NVIDIA CUDA-Q 裡可以取得 QUOPS 的參考實作』」→「公告內文寫的是…」**
   （第 4 節第 2 段、摘要第 4 句、FAQ 第 4 題三處）。
   **同一頁的 News Summary 條列寫著** `Developed by Sandia National Laboratories, QUOPS is
   now available in NVIDIA CUDA-Q`——所以「只寫到」在整份公告的層次不成立。
   第一輪把這個矛盾記進了「留給站主的事」，卻在正文與摘要寫成了「只」。
3. **「新聞稿描述可用性的只有一句」→「新聞稿描述這套工具可用性的只有一句」。**
   Availability 段有三句（另兩句講 QUOPS 倉庫與論文），News Summary 還有一句 QUOPS 的可用性；
   限縮到 CUDA-Q Logical 才成立。順帶一提，FAQ 第 5 題本來就寫成「新聞稿只說**它**現已透過
   GitHub 提供」，是對的——正文那句才是唯一漏掉限縮的。
4. **「NVIDIA 沒有說總共有幾家」→「新聞稿沒有說總共有幾家」**（第 1 節第 3 段），
   以及**「NVIDIA 沒有說這些量子位元已做成硬體」→「新聞稿沒有說…」**（第 3 節第 1 段）。
   兩句都是第一輪新寫進去的**無界否定**，依規格限縮到本文引用的文件。
5. **FAQ 第 6 題「新聞稿與技術文件都沒有提到…，只說明可以透過 GitHub 取得」
   →「…；新聞稿只說可以透過 GitHub 取得」。** 技術文件的 Installation 段寫的是
   `pip install cudaq`，不是 GitHub；把兩份文件綁在同一個「只」底下並不成立。

**未經查證的推論與用詞（3 個問題、4 處文字）**

6. **刪掉第 2 節第 2 段的「不必真的換一台機器來試」。** 四條來源都沒有這個對照——
   說明頁只寫 `keeps the workload fixed while these system choices change, so you can compare
   results directly and inspect the assumptions behind each one`。這是第一輪新寫的推論。
   刪的是未經查證的敘述，**不是但書**。
7. **「固定住要跑的應用程式」→「固定住同一個運算」。** 說明頁同一段把 `the application`
   列為「會改變」的選項之一（`Choices in the application, QEC code, … can all change the qubits
   and runtime required for the same computation`），再說 `keeps the workload fixed`；
   寫成「應用程式」會和來源自己的句子打架。表格第 3 列邏輯欄「固定住**程式**」同步改成
   「固定住**運算**」（同一個問題的第二處）。
8. **第 5 節第 2 段句末補「這些界線新聞稿都沒有寫。」** 摘要第 2 句結尾是
   「但這些說明都沒有出現在新聞稿裡」，原本**在正文找不到對應的說法**（`summary` ⊆ 正文）。
   已逐詞確認新聞稿頁沒有 `resource-estimation` 定義句，也沒有那三句明文否定。

**研究紀錄（2 處）**

9. **Proctor 那條 `fact` 仍寫「業界需要能追蹤與預測…」**——這是第一輪已經在正文改掉
   （改成「他們與其他量子運算相關方」）、**卻沒有同步到研究紀錄**的舊說法。
   已改成原文主詞 `we, and other quantum computing stakeholders`，
   並註明該引文是從句子中段擷取的連續字串（前面還有 `Our mission right now is… To do that,`）。
10. **「F01、F05、F13、F14 四條引文在原始 HTML 搜尋不到」的數目不對。**
    本輪程式比對出**12 條**在原始 HTML 中被行內標籤或原始碼換行打斷，不是 4 條。已更正。

### 覆核過而且正確的部分（第一輪的改寫站得住）

- **Iceberg 與 Diraq 的關係三處一致且正確**。原文 `Iceberg Quantum modeled its fault-tolerant
  architecture for Diraq's qubits`，下一句 `…rapidly assess potential implementations of
  **Iceberg's** architecture` 再次確認 `its` 指向 Iceberg。摘要第 3 句、第 3 節第 1 段、
  FAQ 第 3 題三處寫法一致，都是「針對 Diraq 的量子位元替自家容錯架構建模」。
- **150,000 這個數字的三個要素都寫齊了**：估的人是 Iceberg Quantum（用 CUDA-Q Logical 建模）、
  估的是要幾個物理量子位元才能做出 1,000 個邏輯量子位元、前提是**模型估算而非已建成的硬體**
  且比較對象是 Diraq 自己先前的估計。新聞稿正文只出現 `1,000`、`150,000`、`10x`、`7x`、
  `14`、`2026` 六組數字，文章沒有做任何來源沒印的換算。
- **表格第 3 列兩格都撐得住**：物理欄「估算要用掉多少顆、多少時間」對應
  `evaluate physical qubits, runtimes and other resource requirements` 與
  `can all change the qubits and runtime required`；邏輯欄對應 `keeps the workload fixed…
  so you can compare results directly`，並由新聞稿的
  `identify optimal system configurations for performance with logical qubits` 支撐它放在邏輯欄。
- **第一輪補回的四個限定詞逐一回原文，沒有變強也沒有變弱**：
  `can all change` →「都**可能**改變」；`developing useful applications` →「**有用**應用程式」；
  `optimal system configurations for performance with logical qubits`
  →「**在邏輯量子位元上**效能最佳的系統組合」；
  `may change substantially in upcoming versions` →「都**可能在之後的版本**大幅變動」。
- **合作夥伴名單那一句的理由正確**。原始 HTML 確認
  `QCDesign <a href="https://quantummotion.com/…">Quantum Motion</a>`——QCDesign 是純文字、
  Quantum Motion 帶錨點。Infleqtion 也是超連結，但文章並沒有宣稱 Quantum Motion 是唯一的連結，
  所以寫法成立。
- **預覽骨幹四處一致**：摘要第 5 句、第 5 節第 1 段、FAQ 第 5 題、callout 都寫
  「預覽版＋API 可能在之後的版本大幅變動＋CUDA-Q 0.16.0 這一版整合 CUDA-Q Logical 0.1.1」，
  沒有一處寫成「目前的版本號」。今天確認版本紀錄頁 0.16.0 條目**上方仍有 `latest`**
  （main 分支每夜建置）條目，所以這個寫法是必要的。
- **「估算工具、不是量子電腦、不執行也不模擬」骨幹八處一致**：title、description、摘要第 2 句、
  第 3 節第 3 段、第 5 節第 2 段、FAQ 第 1 題、圖解四格、`hero_label`，沒有互相矛盾。
- **否定句逐詞重驗**：`preview` 在新聞稿**整頁** 0 次（不只正文）、`Apache` 0 次、
  `price`／`pricing` 0 次、任何 `x.y` 版本號 0 次；`Taiwan`／`Taipei`／`TSMC` 四頁各 0 次；
  `MediaTek` 只在新聞稿頁右側 More News 的另一則 2026-08-31 標題出現 1 次
  （第一輪對 `not_said` 的限縮正確）。新聞稿內文 9 次 `QUOPS` 附近沒有任何分數或排名。
- **第一輪沒有為了字數刪掉但書**。逐一確認五處但書都還在：Costa「沒有附上具體年份或期程」、
  三個應用領域「不代表用途只限這三項」、Grassellino「這是她形容的對照估計，不是一次計時測量」、
  Iceberg「這是模型估算的結果」、「文件列出的動作停在產生估算與輸出程式，沒有包含執行」。
  **本輪也沒有刪任何但書**——騰出的字數來自一句未經查證的推論與五處收窄後變短的否定句。
- **界線**：沒有購買或升級建議、沒有推薦式比價（來源根本沒有價格）、沒有投資免責 callout、
  callout 仍只有一個；所有能力與時程敘述都掛在具名歸屬之下。
- **`checked_on` 2026-09-17 四處仍一致**，本輪沒有因為重查而改動它；兩個結尾連結未動。

### 留給站主的 3 件事

1. **`hero.alt` 仍寫「邊緣帶著**雜訊**紋理的小圓點」**，而第一輪已把表格、圖解與研究紀錄裡的
   「雜訊」全部改成來源用語「固有的錯誤」（`noise` 在新聞稿 0 次，在能力頁唯一一次是
   `that is a parameter surface, not a noise model`，語意相反）。依規格 `hero.alt` 由協調者
   依實際畫面改寫，本輪沒有動它——**請協調者改寫時避開「雜訊」**。
2. **zh-TW 段落字數 2,999 → 2,984**，多出 16 字的餘裕。第一輪列的兩項「值得補但沒有位置」的
   內容（新聞稿內文的 `7x speedup` 那句、QUOPS 預印本量測對象的物理／邏輯區分）**仍然放不下**，
   且後者的佐證頁不在 `sources[]` 內，要補就得換一條 source。這是編輯取捨，查核代理不代決定。
3. **`sources[4]` 的 `releases.html` 仍指 `/latest/`**，今天 0.16.0 條目上方的 `latest` 區塊仍在；
   出刊前值得再抓一次，確認 0.17.0 有沒有出。

### 自檢

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
 - zh-TW link text must be the title of tech-news-nvidia-vera-rubin-20260915
```

只剩規格允許的那兩條，查核前後完全相同，都不是本文造成的。

### 結論

`ok`。**兩條骨幹論述都成立且全文一致，本輪沒有更動**——這是估算工具不是量子電腦、
新聞稿與技術文件用詞有落差，兩件事在八處與四處說法上都對得起來。
第一輪的 30 處改寫覆核下來 24 處無誤；**又改的 15 處全部落在第一輪新寫進去、沒有人查過的句子上**，
而且集中在同一個毛病：**否定句的範圍寫得比來源撐得住的還寬**，其中三處被新聞稿自己的
News Summary 條列推翻。事實骨幹沒有再被推翻，不需要第三輪。
