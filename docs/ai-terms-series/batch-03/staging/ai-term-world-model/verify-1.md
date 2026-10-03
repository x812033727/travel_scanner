# ai-term-world-model 查核紀錄（verify-1）

查核日：2026-10-03。查核者不是撰稿者。12 個來源都在今天重新打開，User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。

讀法：arXiv 的 8 篇都讀了摘要頁（200）與全文 PDF（pdftotext）。Sutton 與 Barto 的書頁回 200，再讀 RLbook2020.pdf 第 8.1 節。OpenReview 只回瀏覽器驗證頁（200 的空殼），所以改讀 Wayback 的 `web/20230228171808id_/https://openreview.net/pdf?id=BZ5a1r-kVsf`（Version 0.9.2）。OpenAI 報告直連回 403，改讀 Wayback 的 `web/20260926091256id_/`。Genie 3 官方文章直連可讀（200）。

## 修改

### 事實性修改（計入 facts_changed）

- 「Hafner 等人 2019 年的 Dreamer 改在學到的精簡狀態空間裡想像未來、從想像中學習行為」→「Hafner 等人 2019 年的 Dreamer 同樣在學到的精簡狀態空間裡想像未來，並直接從想像出的軌跡學習行為」｜「改」暗示 Dreamer 和 Ha 與 Schmidhuber 的差別在於潛在空間想像，其實不是。Ha 與 Schmidhuber 的 VizDoom 控制器本來就「train entirely in a latent space environment」（第 4.2 節）。Dreamer 的摘要說的是從想像軌跡學習行為｜https://arxiv.org/abs/1803.10122 ；https://arxiv.org/abs/1912.01603
- 「也是第一個不靠人類資料、從零在 Minecraft 收集到鑽石的演算法」→「也是第一個不靠人類資料、也不靠由易到難的課程安排，從零在 Minecraft 收集到鑽石的演算法」｜論文的「第一個」帶兩個限定：「without human data or curricula」。v1 也寫前人「resorted to human expert data and manually-crafted curricula」。少了課程這個限定，主張就比論文說的大｜https://arxiv.org/abs/2301.04104
- 「表示只記位置、方向與速度」→「表示記下車子的位置、方向、速度等特徵」｜原文是「position, orientation, velocity and other characteristics of the car」（第 4.4 節、圖 12 說明），沒有說「只」｜https://openreview.net/forum?id=BZ5a1r-kVsf
- 來源標題「（作者官網全文，第 8 章 Models and Planning）」→「（作者官網全文，第 8.1 節 Models and Planning）」｜第 8 章的標題是 Planning and Learning with Tabular Methods，Models and Planning 是 8.1 節｜http://incompleteideas.net/book/the-book-2nd.html

### 措辭與來源維護（不計入）

- 「開發者常把世界模型說成通往 AGI 的一步」→「有開發者把世界模型說成通往 AGI 的一步」｜「常」是頻率主張，但只有 Genie 3 官方文章一個來源（"World models are also a key stepping stone on the path to AGI"）。OpenAI 報告和 LeCun 論文都沒有用 AGI 這個詞，所以收斂成「有開發者」｜https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
- 「沿這條路的實驗之一是Meta 研究團隊」→「⋯⋯是 Meta 研究團隊」｜中英文之間補空格｜—
- Genie 3 來源網址 `https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/` → `https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/`｜舊網址現在 301 轉址，新網址直連 200、不轉址。內容不變｜https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/

改完以 `_body_length` 實算為 2,624 字（原為 2,598）。dry-run 通過，只有 `no_summary` 警告，brief 說這個警告不用處理。`notes.md` 與 `research.json` 已同步：網址、主張描述，以及 `running_text_characters` 改成 2624。

## 查過、沒問題的主要主張

- Sutton 與 Barto 對環境模型的定義（給定狀態與動作，預測下一狀態與獎勵）與對規劃的定義（以模型為輸入、產生或改進策略）：RLbook2020.pdf 第 8.1 節原文相符。
- Ha 與 Schmidhuber 的部分都相符。三個組件是 VAE、MDN-RNN 與 single layer linear 控制器。VizDoom Take Cover 完全在夢境中訓練。結果是「100 random consecutive trials ∼1100 time steps」，門檻是「greater than 750 time steps」（第 4.1、4.3、4.4 節）。第 4.5 節記載控制器讓怪物不發射火球的 adversarial policy，並指出它會專挑模型錯的地方。
- DreamerV3 的「同一組設定在 150 多種任務勝過專門方法」：v2 摘要有這句，2023 年 v1 的 Results 段也已寫「over 150 tasks」，比較對象是「specifically designed to the benchmark」的方法，所以標成 2023 年沒錯。
- LeCun 的部分在 Version 0.9.2 裡找到依據：序言說這是立場論文，「not a technical nor scholarly paper in the traditional sense」；世界模型是「most complex piece」；它補感知缺的資訊、預測依動作序列的未來；預測在抽象表示空間進行；「natural world is not completely predictable」；JEPA 是非生成式的，從 s_x 預測 s_y；地毯紋理、樹葉、漣漪無法長期準確預測，JEPA 可以忽略。
- V-JEPA 2：作者單位是 FAIR at Meta，2025 年 6 月發表。先以網路影片預訓練，再用「less than 62 hours of unlabeled robot videos」後訓練出 V-JEPA 2-AC。它在兩個實驗室的 Franka 手臂上以目標影像規劃，完成抓取與放置。
- Genie 論文：Google DeepMind，2024-02-23。用無標註網路影片訓練，學出潛在動作，可以用文字、合成圖片、照片、草圖當提示。
- Genie 3 官方文章：發表日是 August 5, 2025。依文字提示即時生成可探索的環境。「largely consistent for several minutes, with visual memory extending as far back as one minute ago」。自迴歸生成「harder ... than generating an entire video, since inaccuracies tend to accumulate」。Limitations 段列了代理可做的動作有限、多代理互動、真實地點、只能互動幾分鐘。正文沒寫影格率與解析度，符合指派。
- OpenAI 報告：日期是 February 15, 2024，標題是 Video generation models as world simulators。報告寫「does not accurately model the physics of many basic interactions, like glass shattering」。
- Othello-GPT（ICLR 2023，v5）：模型「no a priori knowledge of the game or its rules」。線性探針錯誤率都在 20% 以上（表 1），非線性探針最低約 1.7%（表 2）。第 4 節的干預只改一格棋盤狀態，預測的合法棋步跟著變。
- Gurnee 與 Tegmark：用 Llama-2 與 Pythia，兩者都是開放權重模型。找到經緯度與時間的線性表示，作者寫「basic ingredients of a world model」與「further investigation is needed」。
- Vafa 等（NeurIPS 2024，見 PDF 第一頁頁腳）：資料是紐約計程車的轉向序列。模型的下一步「valid turn nearly 100%」，也「usually find the shortest path」。還原的地圖有「impossible physical orientations and flyovers」。「detours erode performance」。Othello 與邏輯謎題也有同樣的落差。
- 本系列的規矩：topics 是 `["ai","tutorial","ai-terms"]`。全篇「本文／這篇」0 次。正文沒有查證過程。沒有推論、推理兩個詞。沒有價格、截止日期或排行榜分數，也沒有產品型號（Genie、Dreamer、V-JEPA 2 是指派或論文裡的研究系統名）。掃地機器人標了「示例（假想情境，未實測）」。沒有保證式說法。用台灣用語（活化值、探針、演算法、影片）。圖上唯一的數字 2026，正文有「2026 年 10 月」。結構是 6 個 H2、恰好一個表、一個 callout，5 個指派連結都在。diagram-1.svg 渲染後沒有壓線、超框或疊字。

## 我懷疑但沒改的事

- Genie 論文摘要說可以用文字提示，但全文的實際做法是先用文字生圖模型產生第一格，再拿這張圖當提示（圖 10）。正文照摘要寫「提示可以是文字」，沒有改。
- Othello-GPT 的「非線性探針比線性探針準得多」只適用 Li 等人的設定（黑／白編碼）。之後 Nanda 等（arXiv:2309.00941）改用「我方／對方」編碼，找到了線性表示。正文沒有提，讀者可能誤以為這個表示本質上是非線性的。
- LeCun 論文與 OpenAI 報告今天都讀不到原站，只讀到 Wayback 快照（2023-02-28 與 2026-09-26），無法確認原站今天的內容是否有變。
- Gurnee 與 Tegmark 的「事件年代」其實是三種資料：歷史人物的卒年、作品的發表日期、新聞標題的日期。正文寫法稍嫌籠統，但不算錯。
- 字數 2,624，超過第三批 brief 的目標上限 2,600，但仍在 3,000 的硬上限內。為了不重寫，沒有刪減。

facts_changed: 4
