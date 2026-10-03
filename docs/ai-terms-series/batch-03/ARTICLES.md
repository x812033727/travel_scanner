# AI 名詞系列第三批：文章清單

2026-10-03 撰稿、查核與收件，10 篇全部新增，依票 `2026-10-03-ai-terms-series-batch-03`。
指派見 [`catalogue.json`](catalogue.json)，撰稿指令見 [`brief.md`](brief.md)，查核規則見 [`VERIFY.md`](VERIFY.md)。
產線是一份 workflow 腳本，每篇依序：撰稿 → 第一輪查核 → 第一輪改超過三處事實才換人做第二輪 → 寫摘要 → 另一位逐句核對摘要。
每篇的查證紀錄在 `staging/<slug>/`（`notes.md`、`research.json`、`verify-1.md`、`verify-2.md`），workflow 的原始回傳在 `result-*.json`。

10 篇第一輪共改 33 處事實，6 篇進第二輪，第二輪又改 27 處。

| 分組 | 名詞 | 標題 | 來源數 | 查核改動（第一輪 → 第二輪） | slug |
| --- | --- | --- | ---: | --- | --- |
| 訓練、調整與推論資源 | 強化學習 / Reinforcement Learning | 強化學習（Reinforcement Learning）是什麼：靠獎勵一步步試出做法 | 11 | 1 | `ai-term-reinforcement-learning` |
| 訓練、調整與推論資源 | KV 快取 / KV Cache | KV 快取（KV Cache）是什麼：為什麼對話越長越吃記憶體 | 15 | 4 → 3 | `ai-term-kv-cache` |
| 模型與 AI 基礎 | 過擬合 / Overfitting | 過度擬合（過擬合，Overfitting）是什麼：考古題全對、新題卻答錯 | 16 | 2 | `ai-term-overfitting` |
| 評測、安全與人工介入 | 可解釋性 / Interpretability | 可解釋性（Interpretability）是什麼：看懂模型為什麼這樣回答 | 16 | 2 | `ai-term-interpretability` |
| 評測、安全與人工介入 | 資料投毒 / Data Poisoning | 資料投毒（Data Poisoning）是什麼：在訓練資料裡埋下後門 | 9 | 4 → 6 | `ai-term-data-poisoning` |
| 模型與 AI 基礎 | 世界模型 / World Model | 世界模型（World Model）是什麼：讓 AI 預測「接下來會怎樣」 | 12 | 4 → 6 | `ai-term-world-model` |
| 影像、語音、開放模型與來源 | 視覺語言模型 / Vision-Language Model | 視覺語言模型（VLM）是什麼：讓 AI 讀圖片、再用文字回答 | 12 | 4 → 5 | `ai-term-vision-language-model` |
| 評測、安全與人工介入 | 獎勵駭客 / Reward Hacking | 獎勵駭客（Reward Hacking）是什麼：AI 拿到高分，卻沒做到你要的事 | 11 | 6 → 4 | `ai-term-reward-hacking` |
| 訓練、調整與推論資源 | 本機推論 / Local Inference | 本機推論（Local Inference）是什麼：在自己的裝置上跑模型 | 12 | 2 | `ai-term-local-inference` |
| 訓練、調整與推論資源 | 速率限制 / Rate Limit | 速率限制（Rate Limit）是什麼：API 為什麼回你 429 | 17 | 4 → 3 | `ai-term-rate-limit` |

## 協調者收件時另改的地方

- `ai-term-interpretability`：NIST 的用法和機制可解釋性「正好相反」改成「用詞方向不同」；表格補上「天生就忠實」的說法也有人質疑（Jacovi 與 Goldberg）。
- `ai-term-rate-limit`：批次 API 那句改成「三家文件都把批次的限制和即時呼叫分開列」，不把三家寫法說成一樣。
- `ai-term-world-model`：Vafa 等人的邏輯謎題結果是直接下提示詞測大型語言模型，不是訓練出來的序列模型，句子分開寫。
- `ai-term-reinforcement-learning`：callout 與摘要的「獎勵給最終目標」寫明是 Sutton 與 Barto 的建議，不寫成通則。
- `ai-term-reward-hacking`：圖解拿掉「較多資料」讓下降較緩（Gao 等人只對獎勵模型大小這樣說）。指派要求說明的「獎勵投機」查不到 AI 語境的用例，正文不收。
- `ai-term-overfitting`：撰稿者依國教院樂詞網與站上既有文章用「過度擬合」，標題並列「過擬合」。

## 別名

`docs/ai-terms-series/aliases.json` 加了 10 個詞的別名，來自各篇 `research.json`；`interpretability` 拿掉 `XAI`（那是 explainable AI 的縮寫，日後若另寫專文會撞）。
