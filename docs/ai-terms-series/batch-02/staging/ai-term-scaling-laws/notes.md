# 查證與編輯紀錄：ai-term-scaling-laws（縮放定律）

查證日一律 2026-10-03。讀取方式縮寫：
- abs = `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" https://arxiv.org/abs/<id>`，HTTP 200，讀摘要、版本與日期。
- pdf = `curl -sSL` 同一 User-Agent 抓 `https://arxiv.org/pdf/<id>`，HTTP 200，`pdftotext -layout` 轉文字後讀正文、附錄與註腳。
- 兩種都做；`sources` 寫 arXiv abs 網址。沒有用到 Wayback，也沒有 403。

格式：主張｜來源網址｜查證日｜讀取方式

## 冪律與 Kaplan

損失在沒看過的文字上量，是逐 token 的交叉熵，單位 nats｜https://arxiv.org/abs/2001.08361（§1.3 Notation）｜2026-10-03｜abs+pdf
損失與參數量 N、資料量 D、訓練計算量 C 各自近似冪律；有些趨勢跨越七個以上數量級｜https://arxiv.org/abs/2001.08361（摘要、§1.2）｜2026-10-03｜abs+pdf
「參數量加倍，損失變成 2^-0.076 = 0.95 倍」；條件是參數有限、資料足夠、訓練到收斂（公式 1.1），資料集 WebText2，N 不含嵌入層。2^-0.076 = 0.9487，文章寫約 0.95 倍、少約 5%｜https://arxiv.org/abs/2001.08361（§1.2）｜2026-10-03｜pdf
冪律在雙對數圖上是直線；一般座標下報酬遞減｜https://arxiv.org/abs/2001.08361（摘要「diminishing returns」，§8）。「直線」是冪律的數學性質，不是論文逐字說法｜2026-10-03｜pdf
「目前對任何提出的縮放定律都沒有紮實的理論理解……很難判斷在哪些情況下可以信任」｜https://arxiv.org/abs/2001.08361（Appendix C Caveats）｜2026-10-03｜pdf
Kaplan 自己提醒要檢驗損失的進步是否轉成相關語言任務的進步，並說平滑的量變可能掩蓋質變｜https://arxiv.org/abs/2001.08361（§8 Discussion）｜2026-10-03｜pdf
Kaplan 的最佳配置 N ∝ C^0.73、D ∝ C^0.27，新增預算主要花在放大模型｜https://arxiv.org/abs/2001.08361（式 1.7 後、Appendix A 表 6）｜2026-10-03｜pdf
Kaplan 實驗範圍：模型 768 到 1.5B 非嵌入參數、資料 22M 到 23B token。文章刻意不寫這些數字（本篇不寫任何模型的參數或訓練量）｜https://arxiv.org/abs/2001.08361（§3）｜2026-10-03｜pdf

## Chinchilla

「對 10 倍的算力預算，Kaplan 建議模型放大 5.5 倍、訓練 token 只增加 1.8 倍；我們的結論是兩者等比例增加」。這是 Hoffmann 論文對 Kaplan 結論的換算，不是 Kaplan 自己的句子（10^0.73 = 5.37、10^0.27 = 1.86，與 5.5、1.8 只是取整不同）｜https://arxiv.org/abs/2203.15556（§1）｜2026-10-03｜abs+pdf
訓練「超過 400 個」模型；結論是模型大小與訓練 token 數該等比例增加（每次模型加倍，token 也加倍）｜https://arxiv.org/abs/2203.15556（摘要）｜2026-10-03｜abs+pdf
Hoffmann 對差異的說法：Kaplan 對所有模型用固定的訓練 token 數與學習率排程，使較短訓練的中途損失被高估；Kaplan 的多數實驗模型較小（許多小於 100M）。文章只寫「同樣的訓練長度與學習率排程」「模型多半較小」，不寫 100M｜https://arxiv.org/abs/2203.15556（§2 Related Work）｜2026-10-03｜pdf
Chinchilla 公式 L(N,D) = E + A/N^α + B/D^β，第一項對應自然文字的熵（理想生成過程的損失）；Kaplan 的公式沒有這個常數項｜https://arxiv.org/abs/2203.15556（§3.3）；Kaplan 無偏移項見 https://arxiv.org/abs/2406.12907（§1 貢獻第二點）｜2026-10-03｜pdf
Chinchilla 三種估計：方法 1、2 得 N 的指數 0.50、0.49，方法 3 得 0.46（正文未寫這些指數）。文章只寫「Chinchilla 論文用三種方法估計最佳配置」，給下一句 Besiroglu 的「第三種」「前兩種」一個交代｜https://arxiv.org/abs/2203.15556（§3 開頭「We present three different approaches」、Table 2）｜2026-10-03｜pdf

## 兩篇對差異的後續解釋

Pearce 與 Song：很大一部分差異（「much of this discrepancy」，不是「most」）來自 Kaplan 數非嵌入參數而非總參數，加上分析在小規模進行；Kaplan 排除的是詞彙與位置兩種嵌入（§2.1「embedding layers for the vocabulary and position indices」），文章因此寫「嵌入層（把 token 及其位置轉成向量的部分）」；模擬 Chinchilla 研究在這些條件下得到接近 Kaplan 的偏誤係數。TMLR 2024（PDF 頁首「Published in Transactions on Machine Learning Research (11/2024)」）｜https://arxiv.org/abs/2406.12907（摘要、§1、§2.1、§2.2）｜2026-10-03｜abs+pdf
Pearce 與 Song：多個訓練長度與餘弦退火對係數只有邊際影響（Experiment 2「counter to Chinchilla's explanation」；Result 2：換最佳化方案的影響小於把 N_T 換成 N_\E），並認為 Hoffmann 的最佳化方案說法「incomplete」（§1）｜https://arxiv.org/abs/2406.12907（§1、§4）｜2026-10-03｜pdf
嵌入層與輸出層在小模型裡占比較大、模型變大後可忽略，因此漏算加上以小模型為主的實驗，會把 N 的指數估高（Kaplan 0.73 對 Chinchilla 0.50），也就是結論偏向把預算多花在放大模型。文章寫成「這兩部分在小模型裡占比較大，Kaplan 的實驗又以小模型為主，漏算就讓結論偏向把預算多花在放大模型」｜https://arxiv.org/abs/2406.12907（摘要「Kaplan's original overestimation」、§7「At larger values of N_T, the embedding parameter counts become negligible」）；https://arxiv.org/abs/2406.19146（§5.2「with scale, the contribution of the model head becomes negligible」、圖 1 計入最後一層後指數 0.835→0.706）；Kaplan 多數實驗模型較小見 https://arxiv.org/abs/2203.15556（§2）｜2026-10-03｜pdf
Porian 等人：重現 Kaplan 後找出三個因素，分別是最後一層（解碼層、model head，文章寫「輸出層」）的計算成本、暖身期對小模型太長、隨規模調整的最佳化器設定（學習率、批次、AdamW β2）；修正後與 Chinchilla 吻合（「excellent agreement」）。§3.2 推測 Kaplan 因 head 與嵌入共用權重，連帶把 head 的 FLOPs 也扣掉；§5.1 也說 Pearce 與 Song 找到的是同一個最後一層 FLOP 計算問題。NeurIPS 2024｜https://arxiv.org/abs/2406.19146（摘要、§1、§3.2、§5.1）｜2026-10-03｜abs+pdf
Porian 等人：學習率衰減並非 Chinchilla 定律成立的必要條件，與 Hoffmann 論文的推測相反｜https://arxiv.org/abs/2406.19146（摘要、§1、Appendix A）｜2026-10-03｜abs+pdf
來源與簡報之間的衝突（已在文中處理）：Hoffmann 自己的假說是學習率排程；Porian 的重現實驗推翻了「必要」這一點；Pearce 與 Song 則把重點放在非嵌入參數與小規模，兩篇歸因不同。文章寫「Chinchilla 論文的解釋是」（歸給 Hoffmann，不寫成定論）、「兩篇後續研究……都發現學習率排程不是主因」，以及「重疊之處是 Kaplan 計算參數與算力時，沒有算進嵌入層或最後一層」｜（綜合上列三篇）｜2026-10-03｜pdf
Besiroglu 等人重做 Chinchilla 的第三種擬合（用從論文圖表重建的資料，摘要「a reconstruction of data from their plots」）：原報告數值與前兩種方法不一致、信賴區間窄得不合理；重做後與前兩種相容（「compatible」）｜https://arxiv.org/abs/2404.10102（摘要）｜2026-10-03｜abs+pdf
Sardana 等人（ICML 2024，PMLR 235；arXiv v1 2023-12-31、v3 2025-04-14）：Chinchilla 定律「neglect to include the cost of inference」；把推論成本算進去後，預期推論需求夠大（約 10 億次請求）時應「train models smaller and longer than Chinchilla-optimal」。文章寫「預期請求量夠大時，該訓練比 Chinchilla 建議更小、看更多 token 的模型」，不寫 10 億這個門檻｜https://arxiv.org/abs/2401.00448（摘要、§1）｜2026-10-03｜abs+pdf
（已換掉）初稿原用 Roberts 等人 arXiv:2604.01411（2026-04-01，「Preprint. Under review.」，只有 v1，談推論時重複取樣的成本）。第一輪查核改用同行審查過的 Sardana 等人，文章與 sources 都不再引用 2604.01411｜https://arxiv.org/abs/2604.01411｜2026-10-03｜abs

## 湧現能力

Wei 等人定義：能力若在小模型不存在、在大模型存在，即為湧現，因此無法由小模型外推；曲線在某規模前接近隨機、之後明顯高於隨機。TMLR 2022（abs 頁為 v2，2022-10-26）｜https://arxiv.org/abs/2206.07682（§2）｜2026-10-03｜abs+pdf
Wei：不給部分分數的指標「至多是不完整的解釋」，因為分類任務也觀察到湧現｜https://arxiv.org/abs/2206.07682（§5.1）｜2026-10-03｜pdf
Wei：對六項 BIG-Bench 湧現任務，在下游指標近隨機的規模上，交叉熵損失其實已在改善；但這「解釋不了下游指標為何湧現，也無法預測湧現的規模」｜https://arxiv.org/abs/2206.07682（§5.1、Appendix A.1）｜2026-10-03｜pdf
Schaeffer 等人：非線性或不連續指標產生表面上的湧現；連續指標下平滑、可預測；超過 92% 的 BIG-Bench 湧現能力出現在多選題等級（Multiple Choice Grade）或完全字串相符（Exact String Match）兩種指標之下。abs 頁為 v2（2023-05-22），PDF 標示 Preprint, under review｜https://arxiv.org/abs/2304.15004（摘要、§1）｜2026-10-03｜abs+pdf
Schaeffer 的 92% 是對「Jason Wei 手動整理的 BIG-Bench 湧現清單（其文獻 [32]，一篇部落格）」統計（§3「hand-annotated task-metric-model family triplets」），不是 Wei 等人 2022 論文本身的清單。文章因此寫「他們統計一份人工標注的 BIG-Bench 湧現能力清單」，不寫成 Wei 等人的清單｜https://arxiv.org/abs/2304.15004（§1，文獻 [32]）｜2026-10-03｜pdf
Schaeffer：「本文不應被解讀為主張大型語言模型不可能有湧現能力；訊息是先前主張的湧現可能是研究者分析造成的幻象」｜https://arxiv.org/abs/2304.15004（§7）｜2026-10-03｜pdf
Schaeffer：各 token 獨立的假設不成立，但近似的結果在質性上吻合湧現主張（註腳 1）。示例算式採這個近似｜https://arxiv.org/abs/2304.15004（§2）｜2026-10-03｜pdf
示例算術（我們自己算的，非論文數字、未實測）：5 位全對率 = 逐位答對率的 5 次方；0.5^5 = 0.03125 → 3%；0.7^5 = 0.16807 → 17%；0.9^5 = 0.59049 → 59%；0.95^5 = 0.77378 → 77%。圖與正文使用同一組數字｜（Schaeffer 等人 §2 的模型：Accuracy ≈ p^L）｜2026-10-03｜pdf

## 推論時計算

Brown 等人：覆蓋率（至少一個樣本答對的題目比例）隨取樣次數增加，跨越四個數量級，常近似對數線性、可用指數化冪律描述｜https://arxiv.org/abs/2407.21787（摘要）｜2026-10-03｜abs+pdf
Brown 等人，MATH 數學題集、單一開放權重模型（論文用 Llama-3-8B-Instruct，文章不寫模型名）：覆蓋率從 100 次取樣的 82.9% 升到 10,000 次的 98.44%；用多數決或獎勵模型挑答案，同一範圍內進步最多的做法也只從 40.50% 升到 41.41%（原文「the biggest performance increase is only from 40.50% to 41.41%」，不是每種挑法都是這兩個數字）｜https://arxiv.org/abs/2407.21787（§1 引言，Figure 7）｜2026-10-03｜pdf
程式題、形式證明這類能自動驗證答案的領域，覆蓋率上升直接轉成實際表現；沒有自動驗證器的領域，多數決與獎勵模型跟不上取樣次數。文章寫「程式題這類能自動驗證答案的題目，覆蓋率上升就直接轉成實際表現；沒有自動驗證器時，覆蓋率不等於最終答對率」｜https://arxiv.org/abs/2407.21787（摘要「In domains like coding and formal proofs, where answers can be automatically verified, these increases in coverage directly translate into improved performance」）｜2026-10-03｜abs+pdf
Brown 內部不一致：摘要說多數決與獎勵模型「在數百次取樣之後」趨於持平，§1 與 §3 寫「約 100 次取樣」。文章只引兩組具體百分比，不寫持平點｜https://arxiv.org/abs/2407.21787（摘要 vs §1、§3）｜2026-10-03｜abs+pdf
Snell 等人：MATH 題集；用專門微調來做修改與驗證的模型；依題目難度適應性分配推論算力（compute-optimal），效率比 best-of-N 基準提高。數字三處寫法不同：摘要「超過 4 倍」、§1「約 4 倍」、§8「2 到 4 倍」。文章採最保守且涵蓋三者的「約 2 至 4 倍」｜https://arxiv.org/abs/2408.03314（摘要、§1、§8）｜2026-10-03｜abs+pdf
Snell：FLOPs 相同下與約 14 倍參數量的預訓練模型比較；簡單與中等題「或」推論負載小（R << 1）時推論時計算較佳，難題「或」推論負載大（R >> 1）時預訓練較佳（條件是「或」，文章寫成「題目簡單或中等、或推論量少時」「題目很難、或推論量大時」）；「兩者不能一比一互換」。該比較設定為參數放大、資料量固定（刻意不採 Chinchilla 式等比例縮放）｜https://arxiv.org/abs/2408.03314（§7）｜2026-10-03｜pdf

## 「縮放撞牆」

Villalobos 等人：估計公開人類文字的存量並預測訓練資料需求，問的是資料供應。其預測年份區間是預測，不是觀察，且屬於「預測未來」，本文不寫｜https://arxiv.org/abs/2211.04325（摘要、§1）｜2026-10-03｜abs+pdf
冪律「報酬遞減、必然在到達零損失前變平」｜https://arxiv.org/abs/2001.08361（§1.1「performance must flatten out eventually before reaching zero loss」）｜2026-10-03｜pdf
「基準測試分數進步變慢要先分辨是指標飽和還是能力停滯」是編輯建議，不是任何一篇論文的結論；文章用「要先分辨」的口吻，沒有宣稱任一方是對的｜（編輯判斷）｜2026-10-03｜—

## 簡報與來源的出入、以及沒做的事

- 簡報（catalogue.json）建議的五篇一手來源全部讀到並採用。額外加入 Pearce 與 Song、Porian 等人（差異的成因）、Besiroglu 等人（Chinchilla 第三種擬合的重做）、Brown 等人（推論時縮放的另一條證據）、Villalobos 等人（資料供應）、Sardana 等人（把推論成本納入，ICML 2024；第一輪查核時取代了初稿的 2026 預印本 2604.01411）。共 11 筆，皆為論文原文。
- 簡報要求寫「Kaplan 與 Chinchilla 結論差異與原因（各自設定）」。原因的一手來源有兩層：Hoffmann 論文自己的假說，以及 2024 年兩篇後續論文的實證歸因；兩層不一致之處見上。
- 沒有取用：搜尋時另見 2509.23963（Schaeffer 等人，檢驗 Chinchilla 的穩健性）、2603.22339（IsoFLOP 拋物線擬合的偏誤）、2608.07222（Skaling 定律，2026-08），只讀了摘要，沒有用在文章裡，因為正文篇幅已滿，且與必須涵蓋的五點無直接關係。
- 不寫任何模型名、價格、截止日期、排行榜分數。出現的專有名詞只有論文與資料集名稱：Chinchilla（論文通稱）、BIG-Bench、MATH、Transformer。
- 圖與 hero 是原創向量圖（手寫 SVG），不是 AI 產圖；2026 是製圖年份，同時出現在表格圖說「2026 年 10 月」。
- 簡報指定的渲染指令（`render_svg`，視窗 1600x900）在這台機器上只輸出上方約 812 像素，下方約 88 像素是空白。圖的頁尾（y=870）與任何 y>812 的內容在那個 PNG 看不到。已確認的做法：另用 1600x1100 視窗渲染後裁成 1600x900 檢查全圖；hero 的所有內容放在 y<812 以內，避免 ingest 時被裁掉。第二輪查核（2026-10-03）照 brief 用預設 headless shell 跑 `render_svg`，`diagram-1.svg` 輸出完整 1600x900，y=870 的頁尾看得到，沒有疊字或超框。

純段落正文字元數（`app.guides.pack_ingest._body_length` 實算：段落、rich_paragraph、表格格子、callout 標題與內文；不含標題、圖說、來源）：初稿 2497；第一輪查核後 2580；第二輪查核後 2705（其中站內連結文字 24 字，扣除後 2681）。示範數字為說明用，未宣稱實測。查核紀錄見同目錄 `verify-1.md`、`verify-2.md`。
