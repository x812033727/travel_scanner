# ai-term-world-model 查證紀錄

格式：主張｜來源網址｜查證日｜讀取方式

## 定義與強化學習用法

環境模型＝代理用來預測環境如何回應其動作的任何東西；給定狀態與動作，預測下一個狀態與獎勵｜http://incompleteideas.net/book/the-book-2nd.html｜2026-10-03｜curl 書頁 200，再讀同站全文 PDF（RLbook2020.pdf）第 8.1 節
規劃＝以模型為輸入、產生或改進策略的計算｜http://incompleteideas.net/book/the-book-2nd.html｜2026-10-03｜同上，第 8.1 節（"any computational process that takes a model as input and produces or improves a policy"）
Ha 與 Schmidhuber 把代理分成 V（VAE，畫面壓成潛在向量）、M（MDN-RNN，預測下一個潛在向量）、C（單層線性控制器）｜https://arxiv.org/abs/1803.10122｜2026-10-03｜arXiv 摘要頁 200，全文 PDF 以 pdftotext 讀第 2 節
VizDoom Take Cover：控制器完全在世界模型生成的夢境裡訓練，再放回真實環境；連續 100 次測試約 1,100 個時間步，任務要求 750 步｜https://arxiv.org/abs/1803.10122｜2026-10-03｜全文第 4.3、4.4 節（"The score over 100 random consecutive trials is ∼ 1100 time steps, far beyond the required score of 750 time steps"）
控制器學會讓夢裡怪物在某些回合不發射火球的對抗策略；世界模型只是近似，策略會在模型錯的地方得分｜https://arxiv.org/abs/1803.10122｜2026-10-03｜全文第 4.5 節 Cheating the World Model
Dreamer：在學到的世界模型的精簡狀態空間裡想像軌跡，從想像中學習行為（2019）｜https://arxiv.org/abs/1912.01603｜2026-10-03｜arXiv 摘要頁 200
DreamerV3：單一設定在 150 多種任務勝過專門方法；第一個不靠人類資料或課程、從零在 Minecraft 收集鑽石的演算法（2023）｜https://arxiv.org/abs/2301.04104｜2026-10-03｜arXiv 摘要頁 200（v2，2024-04-17）

## LeCun 的路線

立場論文；作者在序言說不是傳統意義的技術或學術論文｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜OpenReview 對本環境回瀏覽器驗證頁（403），改讀 Wayback 快照 web/20230228171808id_/https://openreview.net/pdf?id=BZ5a1r-kVsf（Version 0.9.2, 2022-06-27），pdftotext 讀全文
世界模型是架構中最複雜的模組：補上感知沒提供的狀態、預測可能的未來（含依動作序列的結果）；在抽象表示空間預測、須能表示多種可能，因世界並不完全可預測｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜同上，第 3 節
JEPA 是非生成式架構，兩個編碼分支，預測器從 x 的表示預測 y 的表示；岔路口例子（位置、方向、速度；忽略樹木與人行道紋理；潛在變數決定左或右）｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜同上，第 4.4 節與圖 12
地毯紋理、風中樹葉、水面漣漪無法長期準確預測；JEPA 可選擇忽略不易預測的細節，直接生成 y 的模型則否｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜同上，第 4.5 節
V-JEPA 2（FAIR at Meta，2025）：網路影片預訓練；用不到 62 小時未標註的 Droid 機器人影片後訓練出依動作預測的 V-JEPA 2-AC；在兩個實驗室的 Franka 手臂上以目標影像規劃完成抓取與放置｜https://arxiv.org/abs/2506.09985｜2026-10-03｜arXiv 摘要頁 200，PDF 第 1 頁確認單位

## 生成式互動環境

Genie（Google DeepMind，2024）：用無標註網路影片無監督訓練；可用文字、合成圖片、照片、草圖提示；學出潛在動作，使用者可逐格操作｜https://arxiv.org/abs/2402.15391｜2026-10-03｜arXiv 摘要頁 200，PDF 第 1 頁確認單位與日期
Genie 3 於 2025 年 8 月 5 日發表；依文字提示生成可即時探索的世界，一致性維持數分鐘；視覺記憶可回溯約一分鐘｜https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜curl 200，去標籤讀全文
逐格（自迴歸）生成比生成整段影片更難維持一致，因誤差隨時間累積｜https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜同上，Environmental consistency over a long horizon 段
限制：代理可直接執行的動作有限、多代理互動難模擬、無法精準重現真實地點、文字呈現、連續互動只支援數分鐘｜https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜同上，Limitations 段
官方把世界模型稱為通往 AGI 的重要一步｜https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜同上（"World models are also a key stepping stone on the path to AGI"）
OpenAI 2024 年 2 月 15 日技術報告題為 Video generation models as world simulators；報告寫明模型無法準確模擬許多基本互動的物理，例如玻璃碎裂｜https://openai.com/index/video-generation-models-as-world-simulators/｜2026-10-03｜官網對本環境回 403；改讀 Wayback 快照 web/20260926091256id_/（gzip 解壓後去標籤）

## 大型語言模型有沒有世界模型

Othello-GPT：GPT 變體只用棋局走法訓練，事先不知道規則；非線性探針可讀出棋盤狀態，線性探針效果差；干預內部活化值改變一格後，預測的合法棋步隨之改變（ICLR 2023）｜https://arxiv.org/abs/2210.13382｜2026-10-03｜arXiv 摘要頁 200，全文 v5 PDF 第 3、4 節
Gurnee 與 Tegmark：在 Llama-2 系列（正文寫「開放權重語言模型」，不寫型號）找到空間與時間的線性表示；作者稱具備世界模型的基本成分，仍需進一步研究｜https://arxiv.org/abs/2310.02207｜2026-10-03｜arXiv 摘要頁 200
Vafa 等（NeurIPS 2024）：用紐約計程車逐段轉向序列訓練 transformer；下一步幾乎都合法、常找到最短路線；還原的曼哈頓地圖有方向不可能的街道；加入繞道後表現下滑；棋類與邏輯謎題也有類似落差｜https://arxiv.org/abs/2406.03689｜2026-10-03｜arXiv 摘要頁 200，全文 v3 PDF 第 1、3 節與表 2

## 編輯紀錄

- 圖解上的數字只有 2026（製圖年份），正文第二段有「資料截至 2026 年 10 月」。
- 掃地機器人是自編示例，正文已標「示例（假想情境，未實測）」；圖解沿用同一示例。
- 用語：policy 寫「策略」（Google 機器學習詞彙表繁中版寫「政策」，本系列強化學習篇的指派用「策略」，跟系列一致）；representation 寫「表示」；activation 寫「活化值」；probe 寫「探針」並附英文。
- 正文不寫 Genie 3 的影格率與解析度（官方有公開，但屬產品規格快照），也不寫 Sora 以外的產品名。
- 讀過但沒用的來源：Genie 2 官方文章（https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/，curl 200，為字數刪去）、Nanda 等 arXiv:2309.00941（線性表示，為字數刪去）、MuZero arXiv:1911.08265、I-JEPA arXiv:2301.08243。
- 字數用 app.guides.pack_ingest._body_length 實算：2,598。
