# 查證與編輯紀錄：ai-term-synthetic-data

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律是實際打開該頁的 2026-10-03。User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL`，狀態碼皆 200。

## 定義與兩種用法

合成資料＝由演算法、生成模型或模擬產生、模仿真實資料特徵的資料，而不是直接由人產生｜https://arxiv.org/abs/2404.07503｜2026-10-03｜abs 頁與 PDF（arxiv.org/pdf/2404.07503，pdftotext）第 1 頁導言；COLM 2024 論文，Google DeepMind 等
部分合成＝只替換部分欄位或加雜訊；完全合成＝用原始資料建模再由模型產生、與原始記錄沒有一對一對應｜https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf｜2026-10-03｜PDF 全文（pdftotext），第 4.4 節與表 3，2023 年 9 月版；csrc.nist.gov/pubs/sp/800/188/final 也開過（200）
合成資料產生自真實資料、有部分合成與完全合成兩種｜https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/｜2026-10-03｜網頁 HTML 轉純文字
用較強模型輸出教較小模型常歸入蒸餾、以教師輸出做 SFT 是一條蒸餾路徑｜站內 ai-term-knowledge-distillation 的既有正文（apps/api/app/guides/content/）｜2026-10-03｜讀站內檔案，用來對齊用語，不是外部來源

## Self-Instruct（原論文設定）

175 個種子任務，每個 1 條指令加 1 個實例｜https://arxiv.org/abs/2212.10560｜2026-10-03｜PDF 第 2.2 節 Instruction Generation
每步抽 8 條指令當示範，6 條人工寫、2 條來自先前模型產出｜同上｜2026-10-03｜PDF 第 2.2 節
先判斷是否為分類任務（用 12 條分類、19 條非分類種子指令的少樣本提示）；分類任務用 output-first（先產生標籤再產生輸入），其他用 input-first，原因是 input-first 對分類任務會產生偏向單一標籤的輸入｜同上｜2026-10-03｜PDF 第 2.2 節
過濾：新指令與任務池中任何現有指令的 ROUGE-L 相似度小於 0.7 才加入；排除含 image、picture、graph 等關鍵字的指令（正文未寫）；剔除完全相同或同輸入不同輸出的實例，以及過長過短、輸出重複輸入等啟發式異常｜同上｜2026-10-03｜PDF 第 2.2 節 Filtering and Postprocessing
最後用產生的資料以監督式方式微調原本的模型（論文用 GPT-3 davinci，2 個 epoch；正文不寫模型名）｜同上｜2026-10-03｜PDF 第 2.3、4.2 節
產生 52,445 條指令、82,439 個實例｜同上｜2026-10-03｜PDF 表 1
抽樣品質：隨機抽 200 條指令各取 1 個實例，由一位專家標註者（作者之一）判斷；指令有效 92%、輸入合適 79%、輸出正確可接受 58%、所有欄位皆有效 54%｜同上｜2026-10-03｜PDF 第 3.3 節與表 2
零樣本評測 Super-NaturalInstructions（119 個任務），ROUGE-L 由原模型 6.8 到微調後 39.9，即 +33.1；比較對象是以人類標註與私有使用者資料訓練的指令微調模型（正文不寫其名）｜同上｜2026-10-03｜PDF 第 4.3 節與表 3
限制：增益可能偏向預訓練語料中常見的任務（論文用「不意外」的推測語氣）；擔心迭代演算法放大社會偏見｜同上｜2026-10-03｜PDF 第 8 節 Limitations（正文照推測語氣寫成「可能」「擔心」）

## 模型崩潰

Shumailov 等人，Nature 631，2024-07-24 上線；「不加區分地使用模型生成內容」造成不可逆缺陷，原始分佈的尾端消失，稱為 model collapse｜https://www.nature.com/articles/s41586-024-07566-y｜2026-10-03｜網頁 HTML（nature.com 直連 200）抽出摘要與全文
LLM 實驗：微調 OPT-125m（1.25 億參數）於 wikitext2，五路 beam search，每代用上一代產生的資料；設定一：五個 epoch、不保留原始資料，困惑度上升；設定二：十個 epoch、每代隨機保留 10% 原始資料，只有輕微退化｜同上｜2026-10-03｜網頁全文「Fine-tuning language models」一節；正文不寫模型名與資料集名，也不寫論文中「20 到 28 點」那句（原文語意不明，不引）
Gerstgrasser 等人：replace 與 accumulate 兩種設定；9M GPT-2、12M／42M／125M Llama2 在 TinyStories（470M token、由 GPT-3.5/4 產生的短篇故事）預訓練，每代新初始化模型，replace 時測試交叉熵上升，accumulate 時持平或更低；VAE 與擴散模型有類似結果；線性模型證明 accumulate 時測試誤差有與迭代次數無關的上界｜https://arxiv.org/abs/2404.01413｜2026-10-03｜abs 頁與 PDF（pdftotext）第 2.1 節、摘要、討論
Gerstgrasser 等人自己指出「model collapse」被不同研究者用在不同現象，至少四種｜同上｜2026-10-03｜PDF Discussion 最後一段
Barzilai、Shamir 2025：最大概似估計的理論，標準假設下即使真實資料占比趨近於零也能避免崩潰；缺少額外假設時，即使原始資料還在，崩潰可任意快發生｜https://arxiv.org/abs/2505.19046｜2026-10-03｜只讀 abs 頁摘要（v3，2026-03-26 修訂），正文僅寫摘要明講的內容
Schaeffer 等人 2025 立場論文：模型崩潰研究含八種不同且有時互相衝突的定義｜https://arxiv.org/abs/2503.03150｜2026-10-03｜只讀 abs 頁摘要；是立場論文，正文以「立場論文」稱之，不當成實證結果
Feng 等人：矩陣特徵值（transformer）與新聞摘要（LLM）兩個任務，用驗證器（即使不完美）可避免崩潰｜https://arxiv.org/abs/2406.07515｜2026-10-03｜只讀 abs 頁摘要（v2）；正文只寫「該研究兩個任務」

## 隱私用途

完全合成資料不是零揭露風險，因為仍含源自非公開個人資訊的內容（第 4.4.6 節）｜https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf｜2026-10-03｜PDF 全文
模型與由模型產生的合成資料都可能洩漏可再識別資訊；深度學習模型是否記住訓練資料難以量化（第 4.4.4 節）｜同上｜2026-10-03｜PDF 全文
建議在資料本身標示合成，例如 SYNTHETIC PERSON；分析者應能用原始資料驗證發現（第 4.4.4 節）｜同上｜2026-10-03｜PDF 全文
差分隱私可控制洩漏量（第 4.4.4、4.4.7 節）｜同上｜2026-10-03｜PDF 全文
合成資料是否匿名取決於能否從中推回原本的個人資訊；擬真度愈高效用愈大也愈可能揭露；部分生成方法易受模型反演、成員推論、屬性揭露攻擊；差分隱私與離群值抑制是緩解方式但可能降低效用；原始資料偏誤會被帶進合成資料｜https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/｜2026-10-03｜網頁 HTML 轉純文字
ICO 頁面頂端註明「Due to changes made by the Data (Use and Access) Act, this guidance is under review」｜同上｜2026-10-03｜網頁；正文以一句話交代
台灣法規：本文不引，正文明寫「引用的是美國與英國文件，不是台灣法規」｜無｜2026-10-03｜未查台灣法規，因此不下任何台灣法規結論

## 示例與數字

客服問答示例（民宿、300 組問答、抽查 30 組）｜無外部來源｜2026-10-03｜原創教學情境，標明「假設流程，沒有實際執行，數字都是舉例」；沒有任何想像的模型輸出被寫成觀察結果
圖解數字 1、2、3（第幾代）與 SVG 標籤｜正文「第 1 代…第 2 代、第 3 代」一句｜2026-10-03｜示意圖，不是量測值

## 讀了但未使用

Kazdan 等人，arXiv:2410.16713（Collapse or Thrive?）：替換崩潰、累積穩定、固定大小子集時緩慢退化，與 Gerstgrasser 等人同方向，與本文已寫的兩邊對照重複，未引｜https://arxiv.org/abs/2410.16713｜2026-10-03｜只讀摘要
Yi 等人，arXiv:2510.16657（驗證器重訓）：理論上驗證器不完美時早期增益會持平甚至反轉；與 Feng 等人重複，未引｜https://arxiv.org/abs/2510.16657｜2026-10-03｜只讀摘要

## 編輯與工具備註

純段落正文（段落、rich_paragraph、清單項、表格格子、callout 標題與內文；不含標題、圖說、連結文字、來源）：2541 字元（`_body_length` 算法，去空白）。
標題 38 字，description 127 字，5 個 H2，1 個表格，1 個 callout，連結 ai-term-knowledge-distillation、ai-term-supervised-fine-tuning、ai-term-pretraining、ai-terms-index 各 1 次。
SVG 皆為原創向量圖，沒有 logo、截圖或人臉；2026 為製圖年份。
brief 與來源的差異：catalogue 寫 Shumailov 的設定是「遞迴只用生成資料」，Nature 論文的語言模型實驗另有每代保留 10% 原始資料的設定（只輕微退化），正文兩個設定都寫；以來源為準。
渲染備註：brief 的渲染指令用完整版 chrome，視窗高度被瀏覽器外框吃掉約 88 px，PNG 下緣約 88 px 會變白，圖看起來被截斷；自查改用 chromium_headless_shell（`render_svg` 在未設 CHROMIUM_BIN 時預設選的那個）才看到完整 1600×900。
