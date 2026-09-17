# 獨立查核：tech-news-windows-project-zenith-20260904

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 維持 **2026-09-17**，不改——
那是撰稿者實際讀到來源的那一天，而且內容包四條 source、研究紀錄、第二段與表格 caption 四處一致）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body（請求裡沒有任何
email、姓名或個人資料），再用純 Python 抽正文與 meta 逐條比對；預先安裝工具那張圖另外重新下載、
放大三倍重新判讀。**沒有使用任何 `sources[]` 以外的新網址替文章補事實**；為了反駁而讀的只有那張圖片，
它本來就記在研究紀錄裡。全部 29 條 `verbatim_quote` 以程式對原始 HTML 與抽出的正文各比對一次。

檢查的主張：**96 條**（正文 16 段的每一句、summary 四句、FAQ 六題的答句、callout、表格四列與欄位標題
與 caption、圖解 caption、研究紀錄 `diagram` 四格與 `hero_label`、title、description）。
**改了 16 處，其中 5 處是被推翻的事實**，另有 4 件留給站主。

## 重抓結果（四條都在，都讀到正文）

| source | HTTP | bytes | 驗到的東西 |
| --- | --- | --- | --- |
| Zenith 公告 9/4（windowsdeveloper） | 200 | 121,061 | `published_time 2026-09-04T10:00:29+00:00`／`modified_time …13:17:30`；`64 GB+ unified memory and 250+ GB/s memory bandwidth`；`30B+ parameter models locally and unmetered`；`Project Zenith will first become available with`；`The hardware may vary…`；圖片 `Preinstalled-tools-2-1024x625.png`、alt `Chart showing pre-installed tools` |
| IFA 報導 9/14（devices） | 200 | 140,491 | `published_time 2026-09-14T17:00:39+00:00`；`64GB+ unified memory and 250gbps memory bandwidth`；`…that includes Visual Studio Code, WSL, GitHub Copilot CLI, and PowerShell`；`price` ×3；`October 2026`；`Berlin` |
| Build 2026 文章 6/2 | 200 | 158,245 | `published 2026-06-02T16:31:36`／`modified 2026-06-05T14:18:38`；`available in experimental preview`；`now generally available`（Coreutils、Windows Development Skills、Windows Developer Configurations）；`Windows 365 comes pre-configured…available in public preview`；註腳 [ii] 全句 |
| AMD 部落格 5/20 | 200 | 183,399 | `May 20, 2026`；`capably runs models of up to 200 billion parameters`；`available exclusively at Micro Center`；`up to 192GB of unified memory and 160GB of VRAM`；`GRHP-01 … 300 billion+ parameters at 4-bit quantization`；規格表 `Ryzen™ AI Max+ PRO 495` 對註腳 `Ryzen™ AI Max+ 495 PRO` |

AMD 那頁本輪 183,399 bytes（撰稿記 183,162，更早兩輪 183,253／183,411）——已知的動態相關文章欄漂移，
正文相同，**位元組數不可當版本識別**。圖表圖檔本輪 200、140,734 bytes、1024×625，與前兩輪相同。

## 改掉的 16 處

**被推翻的（5 處）**

1. **表格「Windows 裝置部落格 9/14」那一列寫「30B 以上」，但那篇根本沒有這個數字。**
   IFA 那篇全文子字串搜尋 `30B` **0 次命中**，它寫的是 `run capable coding models locally and unmetered`。
   已改成「未提參數」。同一列的來源名依 `og:site_name`（`Microsoft Devices Blog`）改成「微軟裝置部落格」，
   備註改成「頻寬寫成 250gbps」。
2. **「兩篇公告全文，沒有價格、幣別或 price、pricing 字樣」不成立。** IFA 那篇 `price` 出現 **3 次**
   （`every person, purpose, and price point`／`the right device at the right price for them`／`at different price points`）。
   已限縮成「兩篇公告全文都沒有 Zenith 的價格、出貨日、預覽日或正式推出日」。
3. **「唯一的未來時間『未來幾個月內』」不成立。** IFA 那篇寫了
   `NVIDIA RTX Spark Windows PCs will arrive in October 2026`。已限縮成「9 月 4 日公告裡唯一的未來時間」。
4. **「兩篇公告都沒提到台灣、亞洲或任何地區」不成立**——IFA 那篇提到 `Berlin`。
   已改成「兩篇公告都沒有提到台灣，也沒說 Zenith 會在哪些國家或市場推出」（Taiwan 兩篇各 0 次命中，成立）。
5. **「18 項裡標版本號的共 5 項：前四項加 PowerShell 7」自相矛盾。** 照字面，「前四項」是剛剛列出的
   Python 3.14+、**uv**、**NVM**、Node 24+，而同一句後半就說「uv 與 NVM 沒有標版本」。
   **我重新下載頁面實際引用的那張圖（`Preinstalled-tools-2-1024x625.png`，200、140,734 bytes）放大三倍逐項重數，
   數到的結果和撰稿者相同：帶版本的是 Python 3.14+、Node 24+、WSL 2+ Ubuntu、.NET 10 加 PowerShell 7 共 5 項，
   uv 與 NVM 是裸名稱**，所以計數留著，改掉的是敘述：「語言欄除 uv 與 NVM 外的四項，加上 PowerShell 7」。
   三欄標題與 18 個工具名也逐項核對無誤。

**收窄／放大來源的（4 處）**

6. **AMD 開箱清單「列出四項工具……範圍比圖表 18 項小得多」。** 微軟原文是
   `a ready-to-code Windows experience that **includes** Visual Studio Code, WSL, GitHub Copilot CLI, and PowerShell`——
   `includes` 引出的是舉例，撐不起「範圍比 18 項小得多」這個比較。
   已改成「並舉出……原文用的是『包含』，不是完整清單，也不是圖表那 18 項」。
7. **「微軟另列四項預先套用的介面預設」，接著列了九項設定。** 來源印的「四」是
   `across File Explorer, Search, Start, and the Taskbar` 四個**區域**，不是四項設定；
   而且同一句的 `with long-path support enabled` 被漏掉。計數已拿掉，長路徑支援已補回。
8. **「圖表其餘工具在那篇 6 月文章各有不同狀態」。** 6 月那篇只交代了圖表 18 項裡的少數幾項；
   Git、GitHub CLI、Azure CLI、Oh My Posh、uv、NVM、Node、.NET 完全沒提。
   已改成具體的「圖表上的 Core Utils 與 Windows Dev Skills 在那篇標的是正式推出」。
9. **「公告內文只點名兩項工具」。** 同一篇內文另外提到 WSL（`Windows Subsystem for Linux (WSL) has become foundational…`）
   與 Intelligent Terminal（`From WSL and Windows Developer Configurations to Intelligent Terminal…`）。
   已改成「只點名工作列預設固定的兩項工具」——這一點來源是明寫的（`pinned to the Taskbar by default`）。

**歸因與但書（4 處）**

10. **「美國的 Micro Center」還在文章裡。** 修正清單 must_fix 4 早就指出這個定性不在 AMD 頁面上，
    研究紀錄也把它列進了排除清單，**但交稿的文章仍在 FAQ 第一題、第四題與 callout 寫了三次**。
    我重測 AMD 全文：`U.S.`、`United States`、`America`、`retailer` 各 **0 次命中**。
    三處已改成「通路僅限 Micro Center，AMD 沒有提到任何地區」。
11. **「不必計量計費」被加了引號，像是微軟的原話；「藉此降低雲端 token 花費」刪掉了對沖詞。**
    原文兩處都是 `helping`（`helping reduce reliance on metered cloud tokens`／`helping lower token costs`）。
    已改成「而且是『不計量』（unmetered）的——微軟拿它和『按量計費的雲端 token』對照，說**有助於**降低 token 成本」，
    FAQ 第六題同步，並明說「這不是在說微軟另外提供免費的服務」（見下方「unmetered」那一節）。
12. **Surface RTX Spark Dev Box 被寫成「既有裝置」。** 它在 2026-06-02 當天是
    `available later this year`、註腳 [ii] 明寫 `pre-release products`，不是既有裝置。
    已改成「同一篇 6 月文章還提到一款微軟自家裝置」，並把「當時說今年稍晚在美國僅透過 Microsoft.com 銷售」
    與先行釋出但書綁在同一句。
13. **「全球第一款 x86 用戶端處理器」→「全球第一批」**：AMD 原文是
    `Ryzen AI Max PRO 400 Series are the world's first x86 client **processors**`，講的是整個系列。

**推論被寫成事實（3 處）**

14. **「因此 Zenith 不是單一機型，而是一套 OEM 夥伴共同遵守的設定標準」。** 來源沒有任何「標準」或
    「共同遵守」的說法，而且這句和文章自己「微軟沒說 Zenith 技術上是什麼」互相打架。
    已改成「可見 Zenith 涵蓋的是多款裝置與效能等級，不是單一機型」（`choice across devices and performance tiers`）。
15. **「微軟在意的是機器能不能把大模型整個放進去運作」→「看的是……」**（正文與 FAQ 第三題）：不替微軟講動機。
    FAQ 第三題另補上「微軟沒有說這兩個數字是認證或強制規範，也沒有說低於這個數字的機器會怎樣」。
16. **「不設硬體門檻」與「第一款支援裝置採用 AMD 的 Ryzen AI Halo」**：前者來源沒說，已拿掉，
    FAQ 第二題改寫成微軟自己的說法（`on any Windows 11 device`／`from any device`）；
    後者原文是 `will first become available with`，已改成「Zenith 會先隨 AMD 的 Ryzen AI Halo 推出」，
    summary 第二句與 H4 標題同步。另外 `dev-config.winget` 的工具清單補上「等工具」（原文結尾是 `Python and more`），
    summary 第四句與 description 末句的「微軟沒有公布」限縮成「這兩篇公告都沒有寫」。

**研究紀錄**：兩條讀自圖片的 `verbatim_quote`（`Preinstalled tools`、`Python 3.14+`）**在頁面文字裡搜尋不到**，
已改成圖片的 alt 文字與空字串並註明是讀自圖片；IFA 那條 `AMD announced that Ryzen AI Halo systems will support`
**跨過一個 `<a>` 連結**、Build 那條 `pre-release products` 的兩個字之間是 **U+202F 窄式不斷行空格**，
兩條都換成頁面上真正連續的字串。另補三條新事實（IFA 沒有 30B、IFA 有 price 與 October 2026 與 Berlin、
Zenith 公告後段的 `250 GB/s+` 變體）並加上 `factcheck` 欄位。

## 撰稿者點名要重查的四件事

- **圖表的版本號計數**：我自己重抓、放大三倍重數，**得到同一個答案（5 項）**，圖表在 1024×625 放大後完全清晰，
  所以計數保留；改掉的是「前四項」這個把 uv、NVM 也算進去的寫法。18／5／7／6 全部是清點出來的數字，
  圖上沒有印任何總數，正文已明寫「本站清點共 18 項」。
- **AMD 的 2,000 億／3,000 億與 4 位元量化**：正文 H4 第三段本來就把「3,000 億參數以上」與「但須 4 位元量化才成立」
  寫在同一句，**沒有拆開**，維持不動；**表格原本把它們拆在兩格**，已合併成「3,000 億以上（4 位元量化）」。
  兩個數字都帶「AMD 表示」。註腳 GRHP-01 自己還標了 `As of 5/11/2026`，見「留給站主」第 2 點。
- **表格會不會被讀成跨廠商規格比較**：第三欄原標題「本機模型規模**上限**」是真正的問題——
  微軟的 `30B+` 是下限、AMD 的 `up to 200 billion` 才是上限，同一欄兩種意義都叫「上限」就是比較。
  已改成「本機模型規模的**說法**」，caption 加上「四列是各文件各自的說法……也不是效能排名」。
  四列八格逐格回查：微軟兩列的 `64GB+` 在兩篇各自的原文裡，AMD 兩列的 128GB／200B、192GB／300B／4-bit
  全在 AMD 那一頁，**沒有一格跨文件**。
- **PRO 495／495 PRO 命名衝突**：今天重抓確認兩種拼法都還在（規格表 `Ryzen™ AI Max+ PRO 495`，
  註腳 `AMD Ryzen™ AI Max+ 495 PRO`）。**文章正文兩種拼法一個字都沒有出現**，用的是頁面上乾淨出現的
  系列名「Ryzen AI Max PRO 400 系列」（AMD 頁面自己就這樣寫），**沒有因為迴避而發明來源沒有的系列名**。
- **`unmetered` 的 must_add 沒寫進正文，會不會誤導**：會，而且已經處理。
  微軟這個詞出自 Build 2026 的一節標題 `Unmetered intelligence on Windows powered by on-device AI`，
  底下宣布的是裝置端小模型 Aion 1.0（`available in the coming months`），
  同節還寫 `all running without cloud dependency or per-token cost`。
  原文的「不必計量計費」加了引號、又沒有對照組，讀者很可能讀成「微軟送你一份不計費的 AI 服務」。
  正文與 FAQ 已改成把它和「按量計費的雲端 token」對照，FAQ 第六題並直接寫「這不是在說微軟另外提供免費的服務」。
  **仍然沒有點名 Aion 1.0**——那是 AI 垂直的範圍，也是本篇 `editorial_brief` 明訂的排除範圍。
- **上市時程／支援機種／地區**：全篇沒有一句能讀成台灣已經買得到或已經推送。
  FAQ 第四題結尾另外加了一句「讀者不能從本文推論台灣已經買得到或已經推送」。

## 查過而且正確的部分（沒有動）

- **日期沒有混用**：事件日 2026-09-04 就是 `published_time`；同日 13:17 的 `modified_time` 沒有被當成另一個事件；
  IFA 是 09-14、Build 是 06-02（且 06-05 被編輯過，研究紀錄有記）、AMD 是 05-20。
  文章把「6 月的狀態」與「9 月的公告」分開寫，並明講 9/4 公告沒有重新交代那些狀態。
- **詞界比對重測 9/4 公告**：Acer、ASUS、Dell、HP、Lenovo、MSI、Intel、NVIDIA、Qualcomm 各 0 次，AMD 1 次；
  `preview`、`generally available`、`general availability`、`Taiwan` 各 0 次。
  **文章沒有把任何一個 grep 次數寫進正文**，只寫「公告未提其他 OEM 或晶片廠商」——這是修正清單 must_fix 2 要的做法。
- **AMD 那頁的缺項重測**：`Zenith`、`bandwidth`、`GB/s`、`price`、`$` 各 0 次命中，
  所以「全文未提 Project Zenith」「未提地區，也沒有頻寬數字」成立。
- **界線**：全文沒有購買或升級建議、沒有推薦式比價、沒有排名、沒有「值不值得」；
  每一句能力與規格敘述都帶「微軟表示／AMD 表示／公告說」；**只有一個 callout，沒有投資免責段落**；
  沒有簡體字；FAQ 六題的答案都是純文字、沒有網址。
- **`sources[]` 結構**：四條全是一手（三個微軟部落格、一個 AMD 部落格），沒有加也沒有減，
  feed 網址與圖片網址依修正清單都不放進 `sources[]`；文章沒有任何事實掛在表外網址。
- **圖解與 summary**：圖解四格的每個數字（5、7、6）與標題的 18 都出現在正文；summary 四句的每個數字也都在正文；
  圖解 caption 與研究紀錄 `diagram.caption` 仍然逐字相同；`hero.alt` 依規格沒有查也沒有動。

## 留給站主的 4 件事

1. **`check_article.py` 仍是 FAIL，只剩協調者要處理的兩條**：tech 索引內容包還不存在，
   以及第二個連結的 `text` 要換成 `tech-news-pixel-drop-20260915` 的正式 title。
   這兩條在查核前後完全相同，不是本次編輯造成的，兩個結尾連結我沒有動。
2. **AMD 註腳 GRHP-01 自己標了 `As of 5/11/2026`**，文章沒有寫進去。
   zh-TW 段落字數現在是 **2,988／3,000**，補這一句就得從別處刪等量的字——這是編輯取捨，查核代理不代決定。
3. **「門檻」是本文的框架用詞**：微軟只是把裝置描述成具備 `64 GB+` 與 `250+ GB/s`，
   沒有說那是認證或強制規範（FAQ 第三題已經寫出這一點，但 title 與正文仍用「門檻」）。要不要換詞由站主決定。
4. **圖表是一張 PNG 快照**，微軟換圖就過時；18／5／7／6 四個數字與 18 個工具名都綁在 2026-09-18 讀到的
   那一版 `Preinstalled-tools-2-1024x625.png` 上。出刊前若要保險，再抓一次那張圖比對。

## 結論

`needs_owner`：96 條主張逐條核對後文章可刊，16 處已改（5 處是被推翻的事實，其餘是限縮、歸因與但書）；
骨幹論述（門檻兩個數字、18 項工具、AMD 是唯一具名夥伴、微軟沒公布價格時程地區）經重查全部成立，沒有被動到。
唯一擋住 gate 的是 tech 索引內容包還不存在與第二個連結的 title，那兩件不在查核代理可動的兩個檔案裡。

---

## 第二輪

第二輪查核代理：同樣未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 仍維持
**2026-09-17** 不動——那是撰稿者實際讀到來源的那一天，四處一致）。

第一輪改了 16 處、其中 5 處是被推翻的事實，超過十處，所以要第二輪。第二輪**不是整篇重做**，
範圍是：第一輪改動過的每一個段落、第一輪**新寫進去**的每一句（那些句子沒有人查過）、
表格八格的來源歸屬、圖表計數、台灣與購買建議的界線、全部 `verbatim_quote` 的連續性，
以及第一輪有沒有為了湊字數刪掉但書。

檢查的主張：**104 條**（正文 16 段的 40 個句子、圖表 18 個工具名與 3 個欄位標題、summary 四句、
FAQ 六題答句、callout 三項、表格 16 格加 4 個欄位標題加 caption、圖解 caption 與四格 nodes 與
`hero_label`、title 與 description 兩句），另外獨立跑了 **34 條 `verbatim_quote`** 的連續性比對與
約 60 組關鍵字／詞界計數。**又改了 9 處**（沿用第一輪的數法，一個發現算一處；這 9 處共動到 13 個文字位置），
其中 3 處是被推翻或被放大的事實。

### 重抓結果（四條都在，都讀到正文）

| source | HTTP | bytes | 本輪新驗到的東西 |
| --- | --- | --- | --- |
| Zenith 公告 9/4 | 200 | 121,061 | `coming months` 1 次，而 `later this year`／`soon`／`quarter`／`launch` 各 0 次——「唯一的未來時間」成立；`Project Zenith devices enable developers to run capable coding models locally and unmetered, helping lower token costs` |
| IFA 報導 9/14 | 200 | 140,491 | `30B` 與 `parameter` 各 0 次（表格「未提參數」成立）；`price` 3 次、`October 2026` 1 次、`Berlin` 1 次 |
| Build 2026 文章 6/2 | 200 | 158,245 | `Core Utils` 0 次、`Windows Dev Skills` 0 次，印的是 `Announcing general availability of Coreutils for Windows`／`…of Windows Development Skills`；`all running without cloud dependency`、`per-token cost` 各 1 次（第一輪報告引述的那兩句確實存在） |
| AMD 部落格 5/20 | 200 | 183,163 | `Ryzen AI Max PRO 400 Series are the world's first x86 client processors capable of running 300 billion parameter models locally`（**正文沒有加號**）；`retail`／`region`／`country`／`store`／`distributor`／`channel` 亦各 0 次 |

AMD 那頁本輪 183,163 bytes——四輪四個數字（183,253／183,411／183,162／183,163），
再次確認**位元組數不可當版本識別**，正文相同。圖表圖檔本輪 200、140,734 bytes、1024×625，與前兩輪相同。

四條請求的 UA 一律 `Mokaair-editorial`，**標頭、查詢字串裡沒有任何 email、姓名或個人資料**。

### 又改掉的 9 處

**被推翻或被放大的（3 處）**

1. **「3,000 億參數**以上**」放大了 AMD 的「全球第一」宣稱。** AMD **正文**印的是
   `capable of running 300 billion parameter models locally`——**沒有加號**。
   加號出自註腳 GRHP-01，而那個註腳的主詞是**單一 SKU**（「該系列最高階的那顆處理器……支援最高
   160 GB 專屬圖形記憶體」），不是整個系列。第一輪把註腳的加號併進正文的系列宣稱。
   正文與**表格第四列**都已改回 AMD 正文的寫法（表格：`3,000 億以上（4 位元量化）` → `3,000 億（4 位元量化）`）。
2. **「AMD 那篇部落格唯一提到的通路是 Micro Center」不成立，而且和文章自己打架。**
   同一頁另寫了 `will be available from leading OEM partners including HP and Lenovo in the third quarter of 2026`——
   那也是一條供貨路徑，**而文章 H4 第三段自己就寫了這一句**。`exclusively at Micro Center` 的獨家
   只屬於 Ryzen AI Halo 這一個產品。callout 與 FAQ 第四題已改成
   「AMD 那篇部落格只說 Ryzen AI Halo 的通路僅限 Micro Center」。
   （`U.S.`／`United States`／`America`／`retailer`／`retail`／`region`／`country`／`store`／`distributor`／`channel`
   今天重測仍各 0 次，「沒有提到任何地區」本身成立。）
3. **「圖表上的 Core Utils 與 Windows Dev Skills 在那篇標的是正式推出」是第一輪新寫的句子，但 6 月那篇
   沒有這兩個名字。** 全文 `Core Utils` **0 次**、`Windows Dev Skills` **0 次**；那篇印的是
   `Coreutils for Windows` 與 `Windows Development Skills`。這是圖表自己的寫法，微軟從未說兩邊是同一件事——
   **而同一段才剛拒絕替微軟調和 Windows Terminal／Intelligent Terminal**，這裡要用同一個標準。
   已改成「那篇把名稱相近的 Coreutils for Windows 與 Windows Development Skills 標為正式推出」。

**主詞被放大（2 處）**

4. **「符合門檻的裝置上開發者可在本機執行 30B 參數以上模型」把產品宣稱擴大成硬體規格通則。**
   微軟兩處的主詞都是 Project Zenith 裝置：`On these devices`（指前一句的 Project Zenith devices）、
   `With 64 GB+ of unified memory and 250 GB/s+ of memory bandwidth, **Project Zenith devices** enable developers to…`。
   一台自行組裝、記憶體達標但不是 Zenith 的機器，微軟並沒有對它承諾任何事。
   正文 H2 第二段與 FAQ 第六題已改回「Zenith 裝置」。
5. **「微軟用記憶體規格而非處理器規格當門檻，看的是機器能不能把大模型整個放進去運作」仍在替微軟講理由。**
   第一輪已把「在意的」改成「看的是」，但主詞還是微軟，而公告只是把這兩個數字和「本機執行模型」**並列**，
   沒有說為什麼挑記憶體規格。已改成「公告把這兩個數字和『在本機執行模型』綁在一起」（正文與 FAQ 第三題同步）。

**補回但書／補回來源印的時點（3 處）**

6. **第一輪為了字數把註腳 [ii] 的兩個條件壓成一個。** 原文是
   `Products and features are subject to regulatory certification/approval; **actual sale and delivery is contingent on
   compliance with applicable requirements.**`——兩個條件。文章只寫了「要視法規核准而定」，
   等於少寫一個但書（研究紀錄裡本來就是完整的兩句）。已改成「要視法規核准**與相關要求**而定」。
7. **AMD 註腳自己標的 `As of 5/11/2026` 補進正文。** 這是第一輪列給站主的第 2 件事（當時段落 2,988／3,000 補不下）。
   第二輪先刪掉一句重複敘述清出空間，已寫成「但須 4 位元量化才成立，**註腳標的是 2026 年 5 月 11 日的狀態**」。
   **站主不必再決定這一件。**
8. **H1 第一段「這套設定建立在……改善之上」來源沒說。** 來源只有
   `Project Zenith devices will benefit from all these improvements`，沒有「建立在……之上」這個因果；
   而且同一句後半已經寫了「會從這些既有改善中受惠」，前半是多出來的。
   已改成「公告說微軟從年初以來持續改善 Windows 11 的搜尋、檔案總管與日常記憶體使用」。

**換出字數的刪節（1 處）**

9. **H5 第一段句尾「只說 Zenith 裝置會受惠於 Windows 11 今年以來的改善」與 H1 第一段末句重複**，
   且該段是「微軟沒講什麼」的清單。刪掉的是重複敘述，**不是但書**——它換回的字數正好用在第 6、7 兩處補但書。

（以上 9 處中，第 1、2、4、5 各動到兩個文字位置——正文加表格、callout 加 FAQ、正文加 FAQ——
合計動到 **13 個文字位置**。）

### 第一輪指定要覆核的六件事，逐件結果

- **表格八格的來源歸屬**：逐格回查，第一、二列的數字只出自微軟各自的那一篇（9/4 的 `64 GB+` 與 `30B+`；
  9/14 的 `64GB+` 與 `250gbps`），第三、四列的 128GB／200B、192GB／160GB／300B／4-bit 只出自 AMD 那一頁，
  **沒有一格跨文件**。「30B 以上」只掛在 9/4 那一列；IFA 那篇今天再測 `30B`、`parameter` 仍各 0 次，
  第二列「未提參數」成立。唯一要改的是第四列的加號（見第 1 處）。
- **被限縮到「9/4 那篇」的三句否定句**：範圍**剛好**。9/4 公告 `price`／`pricing`／`$`／`preview`／
  `generally available`／`general availability`／`Taiwan`／`Berlin`／`October` 各 0 次，未來時間字樣只有
  `coming months` 1 次，所以「9 月 4 日公告裡唯一的未來時間」成立。IFA 那篇的 `price` 3 次、
  `October 2026`、`Berlin` 各 1 次都確認存在，但**正文寫的是「兩篇公告全文都沒有 _Zenith 的_ 價格、出貨日、
  預覽日或正式推出日」與「沒說 Zenith 會在哪些國家或市場推出」——兩句都仍然成立**；
  而且正文一個字都沒有提到 IFA 那篇的 price／October 2026／Berlin，**所以不需要另外帶它自己的條件**。
- **Surface RTX Spark Dev Box 的狀態**：三件事全部對上——`available later this year`、
  `in the U.S. exclusively on Microsoft.com`、註腳 [ii] 的 `pre-release` 與法規但書；文章寫的是「當時說」，
  沒有寫成既有裝置或已上市。要補的是但書的第二個條件（見第 6 處）。
  四條來源今天再測都沒有把這款裝置和 Zenith 畫上等號（6 月那篇 `Zenith` 0 次命中）。
- **`unmetered` 改寫後的那一段與 FAQ**：對沖詞**都還在**——微軟原文兩處都是 `helping`
  （`helping reduce reliance on metered cloud tokens`／`helping lower token costs`），
  正文寫「說有助於降低 token 成本」、FAQ 第六題明寫「這不是在說微軟另外提供免費的服務」。
  讀者不會讀成微軟送一份免費服務。**仍然沒有點名 Aion 1.0**（AI 垂直的範圍）。
  順帶確認第一輪報告引述的 `all running without cloud dependency or per-token cost` 確實在 6 月那篇裡。
- **AMD 那一頁**：2,000 億／3,000 億與 4 位元量化**都在同一句、都帶「AMD 表示」**（表格第三、四列亦然）；
  IFA 開箱那四項仍寫成「包含」（`includes`）的舉例，**沒有**被寫成全清單，也沒有「範圍比 18 項小得多」那種比較。
  對整個 zh-TW 內容包做字串搜尋：**`PRO 495`、`495 PRO`、`Max+ PRO` 各 0 次**；
  文章用的三個名字 `Ryzen AI Halo`、`Ryzen AI Max+ 395`、`Ryzen AI Max PRO 400 系列`
  **都在 AMD 頁面上乾淨出現**，沒有發明來源沒有的系列名。零售通路那一句見第 2 處。
- **圖表計數**：**我自己重抓、自己放大三倍、不看第一輪結論重數一次**，
  得到生產力與編輯 5 項（Visual Studio Code、GitHub Copilot、PowerToys、WinAppCLI、Windows Dev Skills）、
  終端機與原始碼控制 7 項（Intelligent Terminal、PowerShell 7、Git、GitHub CLI、Azure CLI、Core Utils、Oh My Posh）、
  語言與執行環境 6 項（Python 3.14+、uv、NVM、Node 24+、WSL 2+ Ubuntu、.NET 10），合計 **18**；
  帶版本號的**正好 5 項**（Python 3.14+、Node 24+、WSL 2+ Ubuntu、.NET 10、PowerShell 7），
  uv 與 NVM 是裸名稱。圖上沒有印任何總數，正文已標「本站清點」。
  **圖解 nodes 的 5／7／6 與標題的 18 等於我重數的結果，四個數字都出現在正文。**

### 其他查過而且正確的部分（沒有動）

- **34 條 `verbatim_quote` 全部重驗**：非空的每一條都以正規化後（引號、破折號、U+00A0／U+202F、連續空白）的
  字串出現在**原始 HTML**裡，**沒有一條是靠補空白才連得起來的**；每一條的 `url` 都在 `sources[]` 內。
  第一輪修掉的三類問題（IFA 跨 `<a>`、Build 的 U+202F、兩條讀自圖片的）**今天全部通過**。
- **台灣**：全文出現「台灣」四次，**四次都是否定句**；沒有一句能讀成台灣已上市、已推送或有台灣售價，
  FAQ 第四題並明寫「讀者不能從本文推論台灣已經買得到或已經推送」。
- **購買建議**：推薦／值得／划算／最好／最佳／CP值 各 **0 次**；該買、升級、建議、排名的出現處
  **全部是否定用法**（不做該不該升級、該買哪一台的建議／不提供購買或升級建議／不是效能排名）。
  只有一個 callout，沒有投資免責段落。
- **summary ⊆ 正文、FAQ ⊆ 正文**：逐句回比，沒有任何一句帶入正文沒有的事實；
  FAQ 多出來的只有**更嚴的但書**（微軟沒有說這兩個數字是認證或強制規範／讀者不能推論台灣已上市）。
  summary 的每個數字仍都在正文裡。
- **`checked_on` 2026-09-17 沒有動**，內容包四條 source、研究紀錄、第二段、表格 caption 與圖解 caption 一致。

### 留給站主的 4 件事（第一輪的第 2 件已由本輪處理掉）

1. **`check_article.py` 仍是 FAIL，且只剩協調者要處理的那兩條**：tech 索引內容包還不存在，
   以及第二個連結的 `text` 要換成 `tech-news-pixel-drop-20260915` 的正式 title。
   **兩輪查核前後完全相同**，兩個結尾連結都沒有動過。
2. **zh-TW 段落字數現在是 2,996／3,000，只剩 4 個字的空間。** 第二輪是先刪掉一句重複敘述、
   再把 AMD 註腳時點與法規但書補回去才擠進來的；之後若還要加字，得從別處刪等量，**而且不能刪但書**。
3. **「門檻」仍是本文的框架用詞**（title 與正文都用）：微軟只是把裝置描述成具備 `64 GB+` 與 `250+ GB/s`，
   沒有說那是認證或強制規範——FAQ 第三題已寫出這一點。要不要改詞仍由站主決定；**第一輪就留下的同一件事，本輪沒有改。**
4. **圖表是一張 PNG 快照**，微軟換圖就過時；18／5／7／6 與 18 個工具名綁在 2026-09-18 讀到的那一版
   `Preinstalled-tools-2-1024x625.png`（**兩輪各自獨立重數，結果相同**）。出刊前若隔了一段時間，再抓一次比對。

### 第二輪結論

`ok`：104 條主張逐條核對後，**9 處已改（動到 13 個文字位置）**——3 處是被推翻或被放大的事實（AMD 的「3,000 億以上」、
「唯一的通路」、6 月那篇沒有的兩個工具名），2 處是主詞被放大，3 處是補回但書與來源印的時點，
1 處是刪掉重複敘述換字數。**骨幹論述全部重查成立，沒有被動到**：門檻那兩個數字、18 項工具與 5／7／6、
AMD 是唯一具名的晶片夥伴、微軟沒有公布 Zenith 的價格時程地區。
擋住 gate 的仍然只有 tech 索引內容包與第二個連結的 title，那兩件不在查核代理可動的檔案裡。
自檢最後輸出：

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
 - zh-TW link text must be the title of tech-news-pixel-drop-20260915
```
