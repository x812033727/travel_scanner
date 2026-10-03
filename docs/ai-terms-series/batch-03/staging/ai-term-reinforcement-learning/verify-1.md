# 查核紀錄 verify-1：ai-term-reinforcement-learning

查核者不是撰稿者。查核日 2026-10-03。所有請求用 `curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。
11 筆來源都在今天重新打開（全部 HTTP 200）。Sutton & Barto 的全文 PDF、Christiano、Ouyang、Tulu 3、Amodei 四篇 arXiv PDF 都下載後用 pdftotext 逐節核對；
pdftotext 會吃掉教科書的負號，迷宮例子的 −1 另外把第 75 頁轉成圖片確認。DeepSeek-R1 的 Nature 版是開放取用，讀了 HTML 全文；
Mnih、Silver 兩篇 Nature 是付費文章，只讀得到摘要與編輯摘要。樂詞網要先從首頁取得 session 與 csrf token，再送查詢表單，才會回 10 筆結果。

## 修改

1. 「Ouyang 等人 2022 年把這條路用到語言模型：標註者替回答排序…」→「這套做法先被用在語言模型的續寫與摘要，Ouyang 等人 2022 年沿用它訓練模型遵循指令：標註者替回答排序…」｜原句暗示是 Ouyang 等人把 RLHF 帶進語言模型。論文第 2 節說 RLHF 已被用來微調語言模型做摘要（Ziegler 等 2019、Stiennon 等 2020），第 3.1 節也說方法是沿用 Ziegler 等與 Stiennon 等在風格續寫與摘要上的做法｜https://arxiv.org/abs/2203.02155
2. 「最簡單的折衷是 ε-greedy」→「一個簡單的折衷是 ε-greedy」｜措辭。書中寫的是「a simple alternative」，沒有說它最簡單｜http://incompleteideas.net/book/the-book-2nd.html（全文第 2.2 節）
3. sources「Google 機器學習詞彙表：強化學習（繁體中文版）」`…/glossary/rl?hl=zh-tw` →「Google 機器學習詞彙表（繁體中文版）：「增強學習 (RL)」與「政策」條目」`https://developers.google.com/machine-learning/glossary?hl=zh-tw#reinforcement-learning-rl`｜來源維護，不改正文。原網址今天會 301 轉到整本詞彙表，RL 分類頁已經不存在，所以改成轉址後的網址，並用錨點指到條目。條目內容和正文的說法一致｜https://developers.google.com/machine-learning/glossary?hl=zh-tw
4. sources「…第二版（作者官網全文，第 1、2、3、17 章）」→「…第二版（作者官網全文，第 1–3 章）」｜來源維護。正文沒有引用第 17 章｜http://incompleteideas.net/book/the-book-2nd.html

同步更新了 notes.md 與 research.json：Ouyang 的依據、Google 詞彙表的網址與讀法、書的章節範圍，以及 `running_text_characters`。
字數用 `_body_length` 實算，從 2557 變成 2578。dry-run 通過，只剩 `no_summary` 警告，依 brief 不用處理。

## 查過、沒問題的主要主張

- 譯名：樂詞網用「reinforcement learning」精確查中英文名詞共 10 筆，有強化學習、增強式學習、加強學習、強化性學習。Google 繁中詞彙表的條目標題寫「增強學習 (RL)」，內文寫「強化學習」；policy 譯為「政策」。系列 RLHF 專文的標題是「人類回饋強化學習（RLHF）」，所以正文說採「強化學習」與系列一致是對的。
- Sutton & Barto 第 1.1 節：定義（學習把情況對應到動作，讓數值獎勵最大）；試錯與延遲獎勵是兩個最重要的區別特徵；強化學習是監督式、非監督式之外的第三種範式；探索與利用的取捨只出現在強化學習，只做其中一種都會失敗，研究了幾十年仍未解決；這個名稱同時指問題、解法與研究領域，三者要分開看。
- Sutton & Barto 第 1.3、1.4、3.2、3.3、2.2 節：策略可以是查表、函數或隨機的；獎勵是每步一個數字，定義好與壞；價值是從某狀態起預期能累積的獎勵；狀態是代理能取得的環境資訊；回報是獎勵的加總，常用折扣率打折；迷宮例子每步 −1（看圖片確認）；西洋棋只獎勵贏棋、不獎勵吃子，「告訴代理要達成什麼，不是怎麼達成」；ε-greedy 以小機率 ε 從所有動作中等機率隨機挑。第 2 章開頭說強化學習的回饋是評估式，不是給出正確動作，支持「只說結果好壞，不說哪個動作才對」。
- Mnih 等（Nature 518，2015-02-25）摘要與編輯摘要：deep Q-network 只以像素和遊戲分數為輸入，49 款 Atari 2600 遊戲用同一套演算法、網路架構與超參數；編輯摘要寫要最大化的獎勵「in this case the game score」。
- Silver 等（Nature 529，2016-01-27）摘要：價值網路評估局面，策略網路選棋；以人類高手棋譜的監督式學習加上自我對弈的強化學習訓練；搜尋演算法結合蒙地卡羅模擬與兩種網路。正文沒有寫勝率或比數。
- Christiano 等（arXiv v1 2017-06-12）：讓人比較兩段行為短片，以監督式學習擬合獎勵估計，策略去最大化預測獎勵。
- Ouyang 等第 3.5 節：強化學習的環境是 bandit 環境，給提示詞、收回答、由獎勵模型給分後回合結束；在每個 token 加上相對 SFT 模型的 KL 懲罰，以減輕對獎勵模型的過度最佳化。
- DeepSeek-R1（arXiv v1 2025-01-22；Nature 645:633–638，2025-09-17，開放取用）：規則獎勵分準確度與格式兩種，數學答案寫在指定格式（例如方框裡）再用規則驗證，程式題用編譯器跑預先定義的測試案例，格式獎勵要求推理過程放在 `<think>` 標籤內。R1-Zero 跳過 RL 前的 SFT，直接從基礎模型開始；獎勵只看最後答案，不約束推理過程。訓練集上的平均回答長度上升，反思式推理與嘗試其他解法的情形增加。推理任務不用神經獎勵模型，理由之一是它在大規模 RL 中容易被 reward hacking；限制段承認寫作這類任務很難建立可靠的獎勵模型。
- Lambert 等（Tulu 3，arXiv v1 2024-11-22）第 6 節：提出並命名 RLVR，沿用 RLHF 目標，但把獎勵模型換成驗證函數，正確給 α、否則給 0；用在數學與可驗證的指令遵循。
- Amodei 等（arXiv v1 2016-06-21）第 4 節：清潔機器人如果因「看不到髒亂」得獎勵，可能乾脆閉上眼睛；摘要把 avoiding reward hacking 列為五個問題之一。
- 格子世界示例自己重算過：4 欄 3 列，陷阱在第 3 欄第 2 列。上 2 再右 3 共 5 步，回報 −5＋10＝5；9 步的回報是 1，奇偶性相同，可以靠回頭路走出來；右 2 再上 1 在第 3 步踩到陷阱，回報 −3−10＝−13。圖上的路線、格子位置、desc 和正文一致，圖上每個數字正文都有。
- 系列規矩：topics 含 `ai-terms`。「本文」「這篇」全篇 0 次。沒有查證過程，日期寫成「資料截至 2026 年 10 月」。只用「推理」（reasoning），沒有「推論」。正文沒有模型名、價格或分數，DQN 是論文用的演算法名。示例都有標明，也寫了未實測。沒有保證式說法。用語是台灣用語（最佳化、神經網路、資料、超參數），沒有中國用語。5 個指派連結都在（rlhf、machine-learning、reward-hacking、reasoning-models、總索引），沒有多加連結；6 個 H2、一個 3 欄表、一個 callout。兄弟篇 ai-term-reward-hacking 的標題用「獎勵駭客」，和連結文字一致。

## 我懷疑但沒改的事

- DQN「代理只看畫面像素和遊戲分數」照的是 Nature 摘要的寫法。論文的 Methods 是付費內容，今天讀不到，無法確認有沒有其他輸入（例如剩餘生命數）或分數裁切等細節。
- 表格說明寫「依 Sutton 與 Barto 教科書第 1.1 節整理」，但非監督式那格的「例如分群」是撰稿者補的例子，第 1.1 節沒有。
- callout 的「獎勵給最終目標，不給你以為必經的中間步驟」照的是教科書的西洋棋建議。但 reward shaping 的文獻有證明不會改變最佳策略的中間獎勵設計法，所以寫成通用規則可能太絕對。
- 「提示詞是狀態，整段回答是動作」是依 Ouyang 的 bandit 框架做的簡化。實作上 PPO 是逐 token 計算，同一段也寫了逐 token 的 KL 懲罰，讀者可能覺得兩者有落差。
- 樂詞網的查詢結果要帶 session 與 csrf token 才拿得到，所以 sources 只能放首頁，讀者點進去不能直接重現那 10 筆。

facts_changed: 1
