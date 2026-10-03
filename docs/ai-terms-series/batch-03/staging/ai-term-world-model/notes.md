# ai-term-world-model 查證紀錄

格式：主張｜來源網址｜查證日｜讀取方式

## 定義與強化學習用法

環境模型＝代理用來預測環境如何回應其動作的任何東西；給定狀態與動作，預測下一個狀態與獎勵｜http://incompleteideas.net/book/the-book-2nd.html｜2026-10-03｜curl 書頁 200，再讀同站全文 PDF（RLbook2020.pdf）第 8.1 節
規劃＝以模型為輸入、產生或改進策略的計算｜http://incompleteideas.net/book/the-book-2nd.html｜2026-10-03｜同上，第 8.1 節（"any computational process that takes a model as input and produces or improves a policy"）
Ha 與 Schmidhuber 把代理分成 V（VAE，畫面壓成潛在向量）、M（MDN-RNN，預測下一個潛在向量）、C（單層線性控制器）｜https://arxiv.org/abs/1803.10122｜2026-10-03｜arXiv 摘要頁 200，全文 PDF 以 pdftotext 讀第 2 節
VizDoom Take Cover：控制器完全在世界模型生成的夢境裡訓練，再放回真實環境；連續 100 次測試約 1,100 個時間步，任務要求 750 步｜https://arxiv.org/abs/1803.10122｜2026-10-03｜全文第 4.3、4.4 節（"The score over 100 random consecutive trials is ∼ 1100 time steps, far beyond the required score of 750 time steps"）
控制器學會讓夢裡怪物在某些回合不發射火球的對抗策略；世界模型只是近似，策略會在模型錯的地方得分｜https://arxiv.org/abs/1803.10122｜2026-10-03｜全文第 4.5 節 Cheating the World Model
Dreamer：在學到的世界模型的精簡狀態空間裡想像軌跡，從想像中學習行為（2019）｜https://arxiv.org/abs/1912.01603｜2026-10-03｜arXiv 摘要頁 200
DreamerV3：單一設定在 150 多種任務勝過專門方法（2023 年 v1 的 Results 段已寫 "over 150 tasks"，比較對象是針對各基準設計的方法）；第一個不靠人類資料或課程（curricula）、從零在 Minecraft 收集鑽石的演算法，正文保留「也不靠由易到難的課程安排」這個限定｜https://arxiv.org/abs/2301.04104｜2026-10-03｜arXiv 摘要頁 200（v2，2024-04-17）；查核時另讀 v1、v2 全文 PDF

## LeCun 的路線

立場論文；作者在序言說不是傳統意義的技術或學術論文｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜OpenReview 對本環境回瀏覽器驗證頁（403），改讀 Wayback 快照 web/20230228171808id_/https://openreview.net/pdf?id=BZ5a1r-kVsf（Version 0.9.2, 2022-06-27），pdftotext 讀全文；verify-2 時 Wayback 連線全被重設，改讀 Internet Archive 項目 archive.org/details/a-path-towards-autonomous-machine-intelligence 的 PDF（SHA-1 775f42ed458b8c5b0f2094ea4ff5b64c557b1a34，與 Semantic Scholar 這篇的 paper ID 相同；首頁 Version 0.9.2, 2022-06-27）
世界模型是架構中最複雜的模組：補上感知沒提供的狀態、預測可能的未來（含依動作序列的結果）；在抽象表示空間預測、須能表示多種可能，因世界並不完全可預測｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜同上，第 3 節
JEPA 是非生成式架構，兩個編碼分支，預測器從 x 的表示預測 y 的表示；岔路口例子（位置、方向、速度等特徵，原文是 "position, orientation, velocity and other characteristics"，所以正文不寫「只記」；忽略樹木與人行道紋理；潛在變數決定左或右）｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜同上，第 4.4 節與圖 12
地毯紋理、風中樹葉、水面漣漪無法長期準確預測；JEPA 可選擇忽略不易預測的細節，直接生成 y 的模型則否｜https://openreview.net/forum?id=BZ5a1r-kVsf｜2026-10-03｜同上，第 4.5 節
V-JEPA 2（FAIR at Meta，2025）：網路影片預訓練；用不到 62 小時未標註的 Droid 機器人影片後訓練出依動作預測的 V-JEPA 2-AC；在兩個實驗室的 Franka 手臂上以目標影像規劃完成抓取與放置｜https://arxiv.org/abs/2506.09985｜2026-10-03｜arXiv 摘要頁 200，PDF 第 1 頁確認單位

## 生成式互動環境

Genie（Google DeepMind，2024）：用無標註網路影片無監督訓練；以一張圖片當第一格提示，可以是照片、手繪草圖或文字生圖模型產生的圖片（摘要寫 "described through text"，但第 4 節與圖 10 的做法是先用文字生圖模型產生圖片，所以正文不寫「提示可以是文字」）；學出潛在動作，使用者可逐格操作｜https://arxiv.org/abs/2402.15391｜2026-10-03｜arXiv 摘要頁 200，PDF 第 1 頁確認單位與日期，第 4 節與圖 10 確認提示方式
Genie 3 於 2025 年 8 月 5 日發表；依文字提示生成可即時探索的世界，一致性維持數分鐘；視覺記憶最多回溯約一分鐘（"visual memory extending as far back as one minute ago"，正文不寫「記得細節」）｜https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜curl 200，去標籤讀全文
逐格（自迴歸）生成比生成整段影片更難維持一致，因誤差隨時間累積｜https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜同上，Environmental consistency over a long horizon 段
限制：代理可直接執行的動作有限、多代理互動難模擬、無法精準重現真實地點、文字呈現、連續互動只支援數分鐘｜https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜同上，Limitations 段
官方把世界模型稱為通往 AGI 的重要一步｜https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/｜2026-10-03｜同上（"World models are also a key stepping stone on the path to AGI"）
（已刪除，verify-2）OpenAI 2024 年 2 月 15 日技術報告 Video generation models as world simulators 的玻璃碎裂一句：官網對 curl 與 WebFetch 都回 403，web.archive.org 今天每次連線都被重設，讀不到任何一手副本，正文與來源都拿掉｜https://openai.com/index/video-generation-models-as-world-simulators/｜2026-10-03｜verify-1 讀過 Wayback web/20260926091256id_/；verify-2 只能從 archive.org 的 wayback/available API 確認該快照存在（狀態 200），內容無法再讀

## 大型語言模型有沒有世界模型

Othello-GPT：GPT 變體只用黑白棋走法訓練，事先不知道規則；以黑／白／空三類去讀時，非線性探針可讀出棋盤狀態，線性探針錯誤率都在 20% 以上（表 1、表 2）；干預內部活化值改變一格後，預測的合法棋步隨之改變（ICLR 2023）｜https://arxiv.org/abs/2210.13382｜2026-10-03｜arXiv 摘要頁 200，全文 v5 PDF 第 3、4 節與圖 2
Nanda、Lee、Wattenberg：改用「我方／對方」（my colour vs opponent's colour）來讀，Othello-GPT 的棋盤狀態可由線性探針讀出｜https://arxiv.org/abs/2309.00941｜2026-10-03｜arXiv 摘要頁 200，全文 v2 PDF 摘要、第 1 與第 3 節
Gurnee 與 Tegmark（ICLR 2024）：在 Llama-2 與 Pythia（正文寫「開放權重語言模型」，不寫型號）找到空間與時間的線性表示；空間是世界、美國、紐約地名的經緯度，時間是歷史人物卒年、藝術與娛樂作品發表日期、新聞標題日期（正文寫「人物、作品、新聞年代」）；作者稱具備世界模型的基本成分，也說這種時空表示本身不構成動態因果的世界模型、仍需進一步研究｜https://arxiv.org/abs/2310.02207｜2026-10-03｜arXiv 摘要頁 200，全文 v3 PDF 摘要與第 1 節
Vafa 等（NeurIPS 2024）：用紐約計程車逐段轉向序列訓練 transformer；下一步幾乎都合法、常找到最短路線；還原的曼哈頓地圖和真實街道相去甚遠，有方向不可能的街道與高架跨越；加入繞道後表現下滑；邏輯謎題與用冠軍賽棋譜訓練的黑白棋模型也有同樣落差，用合成棋局訓練的黑白棋模型則兩項指標都好、繞道下仍近乎完美｜https://arxiv.org/abs/2406.03689｜2026-10-03｜arXiv 摘要頁 200，全文 v3 PDF 第 1、3、4 節與表 2

## 編輯紀錄

- 圖解上的數字只有 2026（製圖年份），正文第二段有「資料截至 2026 年 10 月」。
- 掃地機器人是自編示例，正文已標「示例（假想情境，未實測）」；圖解沿用同一示例。
- 用語：policy 寫「策略」（Google 機器學習詞彙表繁中版寫「政策」，本系列強化學習篇的指派用「策略」，跟系列一致）；representation 寫「表示」；activation 寫「活化值」；probe 寫「探針」並附英文。
- 正文不寫 Genie 3 的影格率與解析度（官方有公開，但屬產品規格快照），也不寫產品名。
- 讀過但沒用的來源：Genie 2 官方文章（https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/，curl 200，為字數刪去）、MuZero arXiv:1911.08265、I-JEPA arXiv:2301.08243。Nanda 等 arXiv:2309.00941 在 verify-2 補回正文。
- 字數用 app.guides.pack_ingest._body_length 實算：2,600（verify-2 後；verify-1 後為 2,624，原為 2,598）。

## 查核（verify-1，2026-10-03）

查核者今天重新打開全部 12 個來源，讀法：arXiv 摘要頁與全文 PDF（pdftotext）都是 200；Sutton 與 Barto 書頁 200，RLbook2020.pdf 第 8.1 節；OpenReview 對本環境回瀏覽器驗證頁（200 的空殼），改讀 Wayback web/20230228171808id_/https://openreview.net/pdf?id=BZ5a1r-kVsf（Version 0.9.2）；OpenAI 報告直連 403，改讀 Wayback web/20260926091256id_/；Genie 3 官方文章舊網址 301 轉到 https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/，來源改用新網址（直連 200，無轉址）。

- Dreamer 句原寫「改在學到的精簡狀態空間裡想像未來」，但 Ha 與 Schmidhuber 的 VizDoom 控制器也完全在潛在空間的夢境裡訓練（1803.10122 第 4.3 節 "train entirely in a latent space environment"；verify-1 原記為 4.2 節，verify-2 更正），改成「同樣⋯⋯並直接從想像出的軌跡學習行為」（1912.01603 摘要）。
- DreamerV3 的 Minecraft「第一個」原文限定是 "without human data or curricula"，正文補上課程安排的限定。
- LeCun 岔路口例子原文是位置、方向、速度「與其他特徵」，刪掉「只」。
- Sutton 與 Barto 的來源標題原寫「第 8 章 Models and Planning」；第 8 章是 Planning and Learning with Tabular Methods，Models and Planning 是 8.1 節，已改。
- 「開發者常把世界模型說成通往 AGI 的一步」只有 Genie 3 官方文章一個來源（OpenAI 報告與 LeCun 論文都沒有用 AGI 這個詞），收斂成「有開發者」。

## 查核（verify-2，2026-10-03）

第二位獨立查核者。arXiv 9 篇（含新加的 2309.00941）摘要頁與全文 PDF 都是 200，以 pdftotext 讀；DreamerV3 另讀 v1 PDF；Sutton 與 Barto 書頁 200，RLbook2020.pdf 第 8.1 節；Genie 3 官方文章直連 200、無轉址。OpenReview 的 forum、pdf 與 api／api2 端點都回瀏覽器驗證（403 ChallengeRequiredError），web.archive.org 今天每次連線都被重設（代理紀錄 ws_closed_mid_exchange），所以 LeCun 改讀 Internet Archive 項目的 PDF（雜湊見上）。OpenAI 報告對 curl 與 WebFetch 都回 403，又讀不到 Wayback，沒有任何一手副本可讀。

- Genie 的提示：摘要寫 "described through text"，但第 4 節與圖 10 的做法是拿一張圖片當第一格（照片、手繪草圖或 Imagen2 等文字生圖模型的輸出）。正文改成「示範時從一張圖片起步，可以是照片、手繪草圖或文字生成的圖片」；Genie 3 才「直接依文字提示」。
- Othello-GPT：「非線性探針比線性探針準得多」只在黑／白／空編碼下成立。正文改成按黑白子讀時只有非線性探針讀得準，並補 Nanda 等改按「我方／對方」讀、線性探針也讀得出來（2309.00941 摘要與第 3 節）。
- Gurnee 與 Tegmark：「事件年代」改成「人物、作品、新聞年代」；「並說仍需研究」改用作者自己的限定：時空表示本身不構成動態因果的世界模型（第 1 節）。
- Vafa 等：「棋類與邏輯謎題也有同樣落差」只對用冠軍賽棋譜訓練的黑白棋模型成立；用合成棋局訓練的那個兩項指標都好、繞道下仍近乎完美（第 4 節）。正文改寫。
- Genie 3：「回到一分鐘前看過的地方仍記得細節」超出原文，改成「畫面記憶最多回溯約一分鐘」。
- OpenAI 報告的玻璃碎裂一句與來源刪除（今天讀不到任何一手副本）。
- 精簡論文設定：VizDoom 的「連續 100 次測試」「在論文的設定下」、V-JEPA 2 的「未標註」等；字數 2,624 → 2,600。
