# ai-server-supply-chain-layers 查核第二輪（2026-10-05）

格式：主張｜結果（ok / fixed / softened / kept-unresolved）｜來源網址（怎麼讀到的）。
我自己重抓了每個來源（curl -sSL，UA 為規定字串，檢查 HTTP 狀態；PDF 用 pdftotext -layout；HTML 去掉註解、script、style 後讀），檔案在 `_tools/ai-server-supply-chain-layers/v2/`。改稿前的 pack.json 存在同一個資料夾，檔名 `pack.before-r2.json`。

讀取狀態（今天）：
- IEA 報告頁 `www.iea.org/reports/key-questions-on-energy-and-ai` 和 `/energy-and-ai` 用 curl 和 WebFetch 讀都回 403。改讀 IEA 資產主機上的 PDF，兩份都回 200：Key Questions on Energy and AI（作者 International Energy Agency，PDF 建立於 2026-04-16，138 頁），以及 Energy and AI（2025）。sources 保留報告頁網址。
- JEDEC 新聞稿、jesd270-4 文件頁、站內搜尋頁都回 403（curl 和 WebFetch 都一樣）。Wayback CDX 經代理時連線被重置（curl 35）。`jedec.org/rss.xml` 回 200。
- IEEE HIR ch02_hpc.pdf 回 200（PDF 標題是 Heterogeneous Integration Roadmap, 2021 Version）。四份 ASHRAE `tpc.ashrae.org/FileDownload` PDF 都回 200。UALink FAQ 和 ultraethernet.org 也都回 200。

## A1. 第一輪改過的項目（逐條重查）

- HBM4 數字（2025 年 4 月、2048 位元、2 TB/s、4 到 16 層、64GB）已刪除，改寫「以官方公告為準」｜ok，維持刪除｜JEDEC 新聞稿今天仍是 403，Wayback 也連不上。我另外查了 IEA 兩份 PDF，裡面沒有任何 HBM 世代的數字，所以今天在官方頁上找不到依據。
- JEDEC 寫成「微電子產業標準組織 JEDEC（固態技術協會）」｜ok｜https://www.jedec.org/rss.xml（200）：「Solid State Technology Association, the global leader in the development of standards for the microelectronics industry」
- JEDEC 制定 HBM 標準｜ok｜https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf 第 3 頁：「A JEDEC standard has been defined and recently updated for five successive generations of HBMs … JEDEC has also recently published a standard for HBM 3」
- JEDEC 新聞稿已從 sources 移除｜ok｜同上，今天仍是 403。
- description 改列 IEEE，不再列 JEDEC｜ok｜IEEE HIR 有用在正文的封裝段。
- 「電壓從常見的 400 伏特提高到 800 伏特，並從交流改為直流」｜ok｜KQ PDF 第 41 頁原文：「increasing the voltage from the standard 400 volts to 800 volts … and by shifting from alternating current (AC) to direct current (DC)」。補充一點：第 43 頁另有「transitional architectures centred around the delivery of 400-volt AC power」，所以第一輪之前的寫法其實也有依據。不過現在的寫法比較貼近第 41 頁，不改。
- diagram-1 供電框寫「配電／400 V 提高到 800 V／交流改為直流」｜ok｜同上。渲染圖看過，框內文字沒有溢出。
- 縱向擴展「同一個運算叢集（pod）」、UALink 補中文全名｜ok｜https://ualinkconsortium.org/faq/（200）：「200G per lane scale-up connection for up to 1,024 accelerators within an AI computing pod」「direct load, store, and atomic operations between AI Accelerators」「based on copper … a few meters without the addition of a repeater」「UEC primarily addressing scale-out」
- diagram-1 網路框寫「叢集內縱向擴展、叢集之間橫向擴展」｜ok｜同上
- 表格「高密度機櫃逐漸超出氣冷能力」｜ok｜ASHRAE Snapshot（Issued June 2026）：「GPC High Density–kW/Rack exceeding the cooling capability of air toward the end of the decade」「HPC undoubtedly will demand liquid cooling」；KQ 第 43 頁：「High-density AI racks increasingly require liquid cooling」
- 併網等待「可能長達五到十年」｜ok｜KQ 第 21 頁：「can be as long as five to ten years in many jurisdictions」
- callout 寫 TWh 是「一段時間累積的用電量（這裡指一年）」｜ok｜單位定義
- HBM 定義補上「資料傳輸率遠高於一般記憶體模組」｜ok｜KQ 詞彙表：「vertically stacks multiple memory dies and connects them via wide internal interfaces, achieving significantly higher data transfer rates than conventional memory modules」
- kW、MW 補上中文｜ok｜用詞
- sources 標題補年份：HIR 2021、ASHRAE 2021 和 2019、Bulletin 2026 年 5 月｜ok｜對過 PDF：HIR 的 PDF metadata 是「2021 Version」；兩份白皮書分別印「© 2021 ASHRAE」「© 2019 ASHRAE」；Bulletin 標題是「TCS Coolant Integrity and System Readiness Best Practices」，頁尾印「Issued: May 2026」。
- 「規格」改成「標準」｜ok｜用詞

## A2. 第一輪無法確認的項目

- HBM4 數字｜kept-unresolved（維持「以官方公告為準」）｜見上。協調者如果之後能讀到 jedec.org，可以補回數字。
- IEA 報告頁 403｜kept｜PDF 內容與報告同名、同作者，sources 保留報告頁網址。
- 「一家 GPU 廠商／目前的架構／已宣布的下一代」｜ok（法遵見 B）｜KQ 第 40 頁原文有點名廠商和架構，正文都沒有寫出來。
- UALink、超乙太網路聯盟｜ok（法遵見 B）｜兩者都是制定開放標準的產業聯盟，不是公司。
- 沒有 JEDEC、OCP 來源｜ok｜JEDEC 只用到它「制定 HBM 標準」這件事，依據是 IEEE HIR。OCP 沒有被引用。
- 字數｜工具計 2,655 字（第一輪是 2,653）｜在 1,800–3,000 之內，比 2,600 的目標上限多 55 字。我評估過能刪的地方：封裝產能那句和表格重複，但它是正文唯一標明 IEA 為出處的地方，所以沒有刪。
- intake 的 hero title 警告｜info｜結果 PASS。

## A3. 隨機三分之一（verify-1.md 中第一輪判 ok 的項目，從第 2 條起每隔三條取一條）

- 2030 年約 950 TWh、約占 3%｜ok｜KQ 第 10 頁：「roughly doubling from 485 TWh in 2025 to 950 TWh in 2030, accounting for around 3%」
- 以 AI 為主的資料中心到 2030 年三倍以上｜ok｜KQ 第 25 頁：「increases by more than threefold to 2030」
- 冷卻占比約 7% 到超過 30%｜ok｜EAI 第 53 頁
- 機櫃例子：32 顆約 13 kW；每顆 1,000 W、每櫃 72 顆約 130 kW；下一代約 600 kW｜ok｜KQ 第 40 頁
- 單顆晶片功率越來越高｜ok｜KQ 第 40 頁「growing power rating of chips」
- 2023 年不到 150 GB，2027 年超過 1,000 GB｜ok｜KQ 第 21 頁
- HBM 短缺至少到 2027 年底｜ok｜KQ 第 10 頁「persist through at least the end of 2027」
- 2.5D／3D｜ok，但同一段改了措辭｜HIR 第 3 頁：「placed adjacent to the processor on an interposer or stacked onto the processor」。原文寫「Adjacent placement appears to be an attractive solution」，理由是 3D 要克服散熱和大量導通孔；正文原本寫「較實際的做法」，比原文說得重，改成「較容易做到」（見 C）。
- 加速器包括 GPU 與 ASIC｜ok｜KQ 第 25、30 頁
- 橫向擴展由 UEC 以乙太網路為基礎制定｜ok｜ultraethernet.org：「Deliver an Ethernet based open, interoperable, high performance, full-communications stack architecture … AI & HPC at scale」
- 風扇用電 10% 到 20%、50 kW 機櫃至少 5 kW｜fixed｜ASHRAE 2021 白皮書第 10 頁原文是「not uncommon for some of the denser servers」，而 5 kW 是用 10% 到 20% 這個比例推算出來的。正文原本寫成泛稱，也沒有年份；現在改成「ASHRAE 2021 年的白皮書指出，部分高密度伺服器……照這個比例，50 kW 的機櫃……」。
- 浸沒式冷卻泡進冷卻液槽｜ok｜ASHRAE 2021 第 19 頁「Immersion」「For tank applications」
- 不到一秒擺動數十 MW、約額定容量一半｜ok｜KQ 第 42 頁
- diagram-1 上的數字 400、800、2026 都出現在正文｜ok｜intake_check 結果是「every number on the diagram is in the text」
- IEA Energy and AI 報告頁｜ok（403，內容讀 PDF）
- ultraethernet.org｜ok（200）

另外順帶重讀到的：PUE 原文是「Best-in-class hyperscale facilities … 1.1 to 1.2」，正文原本只寫「頂尖的」，改成「頂尖的超大型資料中心」｜fixed｜KQ 第 30 頁。

## B. 法遵

- 公司名：pack.json 的正文、表格、callout、description、alt 和 sources 都沒有公司名。我掃過 Nvidia、輝達、台積、TSMC、Hynix、三星、Samsung、Micron、美光、AMD、Intel、Google、鴻海、廣達、緯創、Blackwell、Rubin、CoWoS，都是 0 筆。KQ 原文點名的廠商和架構一律寫成「一家 GPU 廠商／目前的架構／已宣布的下一代」，這個寫法可以接受，因為讀者無法從字面上認出是哪一家。IEA、IEEE、ASHRAE、JEDEC、UALink 聯盟、超乙太網路聯盟都是國際組織、學會或標準聯盟，不是公司，保留。
- 投資語言：「受惠」「概念股」「營收」「股價」「題材」「投資」都是 0 筆。全文沒有市場規模、價格或產值的預測。KQ 提到的記憶體價格漲幅，正文沒有寫。
- 預測類數字：2030 年用電、2027 年記憶體容量、HBM 短缺至少到 2027 年底，三項都標明出自 IEA，屬於能源與技術面的估計，不是市場預測，保留。HBM 短缺這一項放在表格的「目前的限制」欄，算是邊界情況，提醒協調者再看一次。
- 數字來源：功率、容量、用電的數字都出自 IEA（2025、2026 年的報告），ASHRAE 2026 Snapshot 有寫明「2026 年」，風扇比例現在標了「2021 年」，UALink 1.0 版有版本號，三者都有出處和時間點。
- 技術名詞第一次出現就附中文：accelerator、GPU、ASIC、CPU、HBM、advanced packaging、interposer、chiplet、scale-up／pod、UALink、scale-out、Ultra Ethernet Consortium、co-packaged optics、direct-to-chip、cold plate、CDU、PUE、UPS、kW、MW、TWh 都有。GB 和「200G」沒有附中文，沿用常見寫法。

## C. 讀者優先與文風（compliance_fixes）

- 導言第一段原本是「AI 伺服器不是一張顯示卡插進機殼……」，沒有用一句話回答標題。現在改成「一台 AI 伺服器由內而外分成七層：……」，一句話講完七層和各自的作用。第二段刪掉重複的「由內而外拆成七層」。
- 封裝段刪掉「電機電子工程師學會（IEEE）的異質整合路線圖指出」，不在句子裡敘述出處，出處留在 sources。IEEE 的中文名改放進 sources 標題。
- 「本文」「這篇」出現 0 次。全文沒有驚嘆號、沒有「總結來說」。沒有描述查證過程的句子；表格 caption 的「查證於 2026 年 10 月」是 brief §6 規定的寫法，也讓圖上的 2026 在正文裡找得到。用語都是台灣用法。
- 圖：diagram-1 和 hero 重新渲染後都看過。diagram 沒有文字壓到線、溢出或互相重疊，構圖置中。hero 的機櫃是八層等高托盤，沒有遞增長條，只有一行 56 px 的字，alt 和畫面一致。

## 機械關卡

- `pack_cli ingest --dry-run`：dry run: nothing written（通過）
- `intake_check.py`：RESULT PASS（0 failures），body_length=2655
