# 查證記錄：ai-term-neural-network

格式：主張｜來源網址｜查證日｜讀取方式。查證日皆為實際開啟日 2026-10-03。抓頁一律 `curl -sSL`，User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，未帶任何個資。

## 定義與單元

神經元做兩步：輸入乘權重加總，再交給激活函數｜https://developers.google.com/machine-learning/glossary（neuron 條目）｜2026-10-03｜curl 200，擷取條目文字
神經網路＝至少含一個隱藏層的模型；隱藏層多於一層稱深度模型（deep model）｜https://developers.google.com/machine-learning/glossary（neural network、deep model、hidden layer 條目）｜2026-10-03｜curl 200
術語表寫「A neuron in a neural network mimics the behavior of neurons in brains」，文中以「Google 術語表說」限定歸屬，不作無條件陳述｜https://developers.google.com/machine-learning/glossary（neuron 條目）｜2026-10-03｜curl 200
隱藏層的單元稱為神經元、每個單元＝上一層輸出的加權和加偏差｜https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers｜2026-10-03｜curl 200
參數＝訓練中學到的權重與偏差；學習率為人給的超參數｜https://developers.google.com/machine-learning/glossary（parameter 條目）｜2026-10-03｜curl 200
參數計數方法（每個神經元的權重數加一個偏差，再加輸出單元）與 Google 練習的 3-4-1 網路共 21 個參數的算法一致；本文改用自己的 2-2-1 網路｜https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers｜2026-10-03｜curl 200
訓練是決定權重，推論是用學好的權重做預測｜https://developers.google.com/machine-learning/glossary（weight 條目）｜2026-10-03｜curl 200

## 感知器與反向傳播的歷史

Rosenblatt 把感知器稱為「hypothetical nervous system, or machine」；目的是說明智慧系統的基本性質，不深陷特定生物體常屬未知的條件｜https://doi.org/10.1037/h0042519｜2026-10-03｜DOI 對 curl 回 403（APA PsycNet）；改讀 Wayback 快照 20260307062446 的 https://www.ling.upenn.edu/courses/cogs501/Rosenblatt1958.pdf（id_ 原始檔，23 頁，頁首為 Psychological Review Vol. 65 No. 6, 1958，頁 386–408），pdftotext 全文閱讀
感知器有感測單元（S）、聯想單元（A）、反應單元（R）三群；學習靠正負強化改變聯想單元的「值」｜同上｜2026-10-03｜同上
Rosenblatt 自述的限制：要辨認刺激之間的關係時，問題對感知器「excessively difficult」｜同上（Conclusions 前一節）｜2026-10-03｜同上
感知器輸入與輸出之間的「特徵分析器」連線由人預先固定，不是真正的隱藏單元，不學表示；反向傳播讓隱藏單元學出任務的重要特徵，這是與感知器收斂程序的差別｜https://www.nature.com/articles/323533a0｜2026-10-03｜nature.com 頁面 200，只有摘要；全文讀作者網站的掃描 PDF https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf（無文字層，轉成 PNG 逐頁目視）
損失 E = ½ ΣΣ (y − d)²，前向傳遞再反向傳遞，連鎖律｜同上（式 3 至式 6，第 534 頁）｜2026-10-03｜同上
反向傳播的想法在 1970 至 1980 年代被多組人各自發現｜https://www.nature.com/articles/nature14539（Backpropagation 一節）｜2026-10-03｜nature.com 頁面 200 只有摘要與參考文獻；全文讀作者網站 PDF https://www.cs.toronto.edu/~hinton/absps/NatureDeepReview.pdf，pdftotext

## 非線性

加了隱藏層但只有線性運算，網路仍是線性的（練習 2）；多層疊非線性才能學複雜關係｜https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers 與 https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions｜2026-10-03｜curl 200
ReLU 定義為 max(0, x)；教材「still recommend starting with ReLU」｜https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions｜2026-10-03｜curl 200
ReLU 在多層網路通常學得快很多（2015 年的敘述）｜https://www.nature.com/articles/nature14539｜2026-10-03｜作者網站 PDF，pdftotext
單層線性分類器只能用超平面切出半空間（1960 年代已知）｜https://www.nature.com/articles/nature14539｜2026-10-03｜同上；此句在最終文稿已刪，保留於記錄
單一隱藏層、連續 sigmoid 型非線性的前饋網路可把單位超立方體上的連續函數逼近到任意精度｜https://link.springer.com/article/10.1007/BF02551274｜2026-10-03｜curl 200，只讀摘要與引用中繼資料（Math. Control Signals Systems 2, 303–314, 1989）；文中「是能表示的結果、不談訓練找不找得到」為編輯對存在性結果的說明，非引自該文

## 訓練與推論

隨機梯度下降：每次用一小批樣本估計梯度、重複至目標不再下降｜https://www.nature.com/articles/nature14539｜2026-10-03｜作者網站 PDF
測試集用於量泛化能力（對沒見過的輸入給出合理答案）｜同上｜2026-10-03｜同上
反向傳播是兩趟循環中的後向那趟；學習率控制每次增減的幅度｜https://developers.google.com/machine-learning/glossary（backpropagation 條目）與 https://developers.google.com/machine-learning/crash-course/neural-networks/backpropagation｜2026-10-03｜curl 200

## 與深度學習、Transformer

深度學習＝由多個簡單非線性模組疊成、各層表示由資料學出的表示學習｜https://www.nature.com/articles/nature14539｜2026-10-03｜作者網站 PDF
Transformer 是「完全建立在注意力機制上的網路架構」｜https://arxiv.org/abs/1706.03762｜2026-10-03｜curl 200，摘要
Transformer 每層含自注意力子層與位置別的全連接前饋網路，由兩個線性轉換夾一個 ReLU；原論文實驗為機器翻譯與英語句法分析｜https://arxiv.org/abs/1706.03762（PDF https://arxiv.org/pdf/1706.03762 第 3.1、3.3 節與摘要）｜2026-10-03｜curl 200，pdftotext

## 手算（不引來源，已用程式驗算）

雙開關網路 2-2-1：隱藏一 ReLU(a+b)、隱藏二 ReLU(a+b−1)、輸出 h1−2·h2，四種輸入輸出 0、1、1、0；參數 2×3+3＝9｜無｜2026-10-03｜以 python3 逐項計算
單一單元（加權和加門檻）不能解雙開關：兩個該亮組合相加與兩個該滅組合相加互相矛盾；另以 −6 至 6、間隔 0.5 的權重與偏差暴力搜尋，無解｜無｜2026-10-03｜python3
一步更新：輸出權重 1、−1.2、偏差 0，輸入 (1,1) 時 h＝(2,1)，輸出 0.8、目標 0，損失 0.32，梯度 1.6、0.8、0.8，學習率 0.1 後權重 0.84、−1.28、偏差 −0.08，輸出 0.32；(0,1) 的輸出由 1 變 0.76｜無｜2026-10-03｜python3
100 個隱藏神經元、2 輸入、1 輸出：100×(2+1)+(100+1)＝401 個參數（假設的網路，不是任何模型的規格）｜無｜2026-10-03｜python3

## 編輯記錄

- 正文字數（_body_length 算法，含連結文字）：2,500；不含 3 個文內連結的連結文字：2,479。
- 示例一律標「示例」與「手算」，沒有任何實測輸出或模型輸出；沒有模型名、價格、截止日期、排行榜分數與任何模型的參數量。
- 原先寫了 Rumelhart 等人鏡像對稱網路「掃過 64 種輸入共 1,425 遍」（圖 1 說明，已目視確認），為壓縮字數與減少數字而刪除，來源仍在 sources。
- 來源間的分歧：Google 術語表要求「至少一個隱藏層」，Rosenblatt 與 Rumelhart 等人的感知器中間層連線固定，文中並列並提醒讀者先確認對方定義。Google 術語表說神經元「模仿」腦中神經元，Rosenblatt 說類比一看即知但設計不糾纏於生物條件；文中兩邊都標明歸屬，結論是運作定義只是運算。
- SVG 為原創向量圖，不是 AI 產圖；diagram-1.svg 上的數字（2、2、1、9）皆在正文出現，另有製圖年份 2026。
- 渲染檢查：brief 指定的 `chromium-1194/chrome-linux/chrome` 在這台機器會把截圖視窗高度吃掉約 88 px（圖底部被切掉、露出白底）；改用 `chromium_headless_shell-1194/chrome-linux/headless_shell` 才完整輸出 1600×900，兩張 SVG 都以後者看過，無疊字、無超框。
