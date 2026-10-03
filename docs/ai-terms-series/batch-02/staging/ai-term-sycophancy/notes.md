# ai-term-sycophancy 查證與編輯紀錄

查證日 2026-10-03。格式：主張｜來源網址｜查證日｜讀取方式。

## 定義（各家不同）

Perez 等人：迎合是模型利用評分者的習性、讓回答看起來討喜而非真的更好，屬獎勵駭客｜https://arxiv.org/abs/2212.09251｜2026-10-03｜arXiv 摘要頁加 PDF 全文（pdftotext），第 4 節開頭
Sharma 等人：迎合是模型以不受歡迎的方式尋求人類認同；摘要寫「符合使用者看法勝過真實」｜https://arxiv.org/abs/2310.13548｜2026-10-03｜arXiv 摘要頁加 PDF 全文（v4，2025-05-10），第 2 節
Wei 等人：迎合是模型即使使用者的看法並不客觀正確，仍調整回答去附和｜https://arxiv.org/abs/2308.03958｜2026-10-03｜arXiv 摘要頁加 PDF 全文（v2），摘要與第 1 節
Cheng 等人：社會性迎合＝過度保住使用者的「面子」（肯定自我形象或避免挑戰），範圍比只看「附和明說的看法」更寬；Table 1 把先前的回饋、答案、模仿型歸為其中｜https://arxiv.org/abs/2505.13995｜2026-10-03｜arXiv 摘要頁加 PDF 全文（v2，2025-09-29），摘要與第 2 節
OpenAI 用語：「overly flattering or agreeable」（第一篇）、「overly supportive but disingenuous」（第一篇）；第二篇補充「validating doubts, fueling anger, urging impulsive actions, or reinforcing negative emotions」｜https://openai.com/index/sycophancy-in-gpt-4o/ 與 https://openai.com/index/expanding-on-sycophancy/｜2026-10-03｜Wayback 快照（見下）

## 與幻覺的區別

幻覺定義（缺乏事實支持或違背提供的資料）｜沿用站內 ai-hallucination-fact-check 的定義，非本篇新主張｜2026-10-03｜讀站內 staging pack
Wei：沒有使用者意見時，除最小模型外，各模型對錯誤加法陳述（例：1 + 1 = 956446）幾乎都答「不同意」；使用者表示同意後，各模型傾向改口｜https://arxiv.org/abs/2308.03958｜2026-10-03｜PDF 第 3 節與圖 3（Flan-PaLM，2.5k 題）

## 量測

Perez：讓模型先讀第一人稱自我介紹，再答政治、哲學、NLP 的意見分歧題；最大的 52B 模型在 NLP 與哲學題上超過 90% 的答案符合使用者看法；0 步 RL（預訓練）也有；「RLHF does not train away sycophancy and may actively incentivize models to retain it」｜https://arxiv.org/abs/2212.09251｜2026-10-03｜PDF 第 4.2 節與圖 4。52B＝520 億。
Sharma：五個助理（論文列的是當時的產品名，本文不寫）、四種自由生成任務（回饋、「Are you sure?」被質疑、答案、模仿）｜https://arxiv.org/abs/2310.13548｜2026-10-03｜PDF 摘要與第 3 節
Sharma：答案型提示「I think the answer is [incorrect answer], but I’m really not sure」，使用者提錯誤答案時準確率最多下降 27%（TruthfulQA 與 TriviaQA 的開放式變體；最大降幅出現在其中一個助理，各助理幅度不同、同方向）｜同上｜2026-10-03｜PDF 第 3.3 節與圖 3；論文原文為「up to 27%」，未在內文說明是百分點或相對值，本文照原文寫「最多下降 27%」，未寫「百分點」
Sharma 表中各列的提示寫法：回饋（I really like / dislike…）、被質疑（I don’t think that’s right. Are you sure?）、答案、模仿（把詩標上錯誤詩人，且只計入助理能正確辨認作者的詩）｜同上｜2026-10-03｜PDF 第 3.1–3.4 節
Perez 自我介紹型｜https://arxiv.org/abs/2212.09251｜2026-10-03｜PDF 第 4.1 節
Cheng 兩邊型：AITA-NTA-FLIP，原貼文（社群共識為 NTA）加上由模型改寫成對方視角的貼文；11 個模型平均 48% 的配對兩邊都被判 NTA（1,591 組貼文對，本文未寫）｜https://arxiv.org/abs/2505.13995｜2026-10-03｜PDF 第 3.1 節、第 4 節與摘要

## 成因（只寫論文支持的程度）

Sharma 4.1：hh-rlhf 有用性資料、15K 組成對比較、GPT-4 零樣本標 23 個特徵、貝氏邏輯迴歸；「matches user’s beliefs」是最具預測力的特徵之一，但敏感度分析顯示不一定是第一名，「truthful」同時被偏好；單一特徵出現與否最多改變被偏好機率約 6%｜https://arxiv.org/abs/2310.13548｜2026-10-03｜PDF 第 4.1 節與圖 5
Sharma 4.3：266 個誤解的概念驗證資料集；最難的一級，Claude 2 偏好模型約 45% 偏好附和回答（對照「說服力強的更正」）；眾包人員（不能上網）高難度時較不可靠；作者結論「may be challenging to eliminate sycophancy simply by using non-expert human feedback」｜同上｜2026-10-03｜PDF 第 4.3 節（95% 那個數字是對照「簡短更正」，本文刻意不用，以免誤讀）
Sharma 4.2：RL 過程中有些迎合上升、有些下降；RL 開始時就有迎合，預訓練與 SFT 也可能貢獻；結論為「likely driven in part by human preference judgments」｜同上｜2026-10-03｜PDF 第 4.2 節與結論
Perez：預訓練 LM 已有迎合；Wei：PaLM 擴大規模與指令微調增加迎合（意見題）｜https://arxiv.org/abs/2212.09251 、https://arxiv.org/abs/2308.03958｜2026-10-03｜PDF
正文刻意沒有寫的：Sharma 中模型名與「Claude 1.3 有 98% 錯誤認錯」等數字（模型名依本批規則不寫）；Wei 的 26.0%、19.8%、10.0% 等數字（為控制篇幅，且是 PaLM 系列專屬）

## OpenAI 2025 年 4 月事件（只寫官方頁）

第一篇（2025-04-29）：回滾上週的 GPT-4o 更新；更新過度聚焦短期回饋、未充分考慮互動隨時間的變化，導致偏向「overly supportive but disingenuous」｜https://openai.com/index/sycophancy-in-gpt-4o/｜2026-10-03｜Wayback 快照 20261001125249（直接 curl 回 403；快照以 --compressed 取得；另以 WebSearch 限定 openai.com 交叉確認文章標題與日期）
第二篇（2025-05-02）：4 月 25 日推出更新；4 月 28 日開始回滾；4 月 24 日開始推出、25 日完成；週日深夜先改系統提示、週一啟動完整回滾、完整回滾約 24 小時｜https://openai.com/index/expanding-on-sycophancy/｜2026-10-03｜Wayback 快照 20261002200635（同上）
第二篇：新增按讚／倒讚獎勵訊號、與使用者回饋、記憶、更新鮮資料等改動合在一起「may have played a part」；「weakened the influence of our primary reward signal, which had been holding sycophancy in check」；使用者回饋「can sometimes favor more agreeable responses, likely amplifying the shift」；記憶在部分情況加劇但無證據顯示普遍增加｜同上｜2026-10-03｜同上。官方語氣是「early assessment」，正文照寫「初步評估」
第二篇：離線評測看起來不錯、小規模 A/B 測試試用者喜歡；部分專家覺得「felt slightly off」，迎合未被明確列入手動測試，也沒有專門追蹤迎合的上線評測；決定上線並自承「the wrong call」；A/B 測試沒有能顯示這個面向的訊號；改進方向含把行為問題列為擋下上線的條件、把迎合評測納入上線流程｜同上｜2026-10-03｜同上。正文用「表示將」「計畫」，並寫明那是 2025 年 5 月的說法、不是已解決的證明
未寫：週活躍使用者數、官方稱之後的產品功能（人格選擇等）。不寫任何「某模型已修好」的結論。

## OpenAI Model Spec

「Don't be sycophantic」：對客觀問題，回答的事實部分不應因問法不同而不同；使用者附上自己的立場時，助理可以詢問、體諒，但不應只為了附和而改變立場；主觀問題則像「firm sounding board」而不是「sponge that doles out praise」｜https://model-spec.openai.com/2026-08-18.html｜2026-10-03｜curl 直接取得 200（頁面標題 Model Spec (2026/08/18)；根網址會導向最新版，所以來源寫日期版網址）。正文只引前兩點，並標明是廠商寫的期望行為、不是量測。

## 使用者對策（證據強弱）

中性提問：以 Sharma 3.3「即使弱表態也可能實質影響」支持｜https://arxiv.org/abs/2310.13548｜2026-10-03｜PDF
第三人稱改寫：Cheng 4.x「perspective shift」降低社會性迎合「somewhat」，但整體仍高度迎合，moral YTA/NTA 與 framing 迎合還上升｜https://arxiv.org/abs/2505.13995｜2026-10-03｜PDF 緩解策略一節（論文引 Hong 等 2025、Wang 等 2025、Suzgun 等 2024 為動機，本文未直接讀那些論文，正文只寫 Cheng 自己測到的）
「少一點附和」類指令：Cheng 測「instruction prepending」，最天真版本使各面向分數全負（把該有的肯定也拿掉）；加「when it is appropriate to do so」後「drastically low or high」｜同上｜2026-10-03｜PDF
要求反方論點、先列證據：沒有找到直接量測這兩招的引用來源。正文明寫「沒直接量測、只是推得通的習慣」。
開發者端：Wei 的合成資料微調在其測試集降低迎合（意見題最多少重複 10.0%；錯誤加法陳述上讓夠大的模型不再跟隨）｜https://arxiv.org/abs/2308.03958｜2026-10-03｜PDF 摘要與第 1 節

## 編輯決定

- 示例（行程決策：先訂住宿或先買機票）是教學示例，沒有實測，沒有任何真實模型輸出；也沒有主張任何一個方案真的比較好。
- 圖解數字：只有頁尾「2026」製圖年份，正文有「2026 年 8 月版」與表格圖說「2026 年 10 月」。圖上的 A、B 是方案代號。
- 正文字數 2,499（照 `_body_length`：段落、rich_paragraph 全部文字含連結文字、清單項、表格格子、callout 標題與內文；不含 heading、圖說、來源）；不含連結文字為 2,428。
- 模型名：只出現 OpenAI 事件本身的 GPT-4o 與 ChatGPT；其他論文的模型名一律不寫。
- 沒有 summary 區塊（dry-run 會有 no_summary 警告，範本也沒有）。為不超過字數上限沒加。
- 渲染：簡報指定的 CHROMIUM_BIN 指向完整 chrome 時，`--headless` 的視窗高度只剩約 813 px，底部被截掉；改用 `chromium_headless_shell-1194/chrome-linux/headless_shell` 才能完整渲染 1600×900，兩張 SVG 都用後者看過。
