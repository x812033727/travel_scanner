# AI 名詞系列第二批：文章清單

2026-10-03 撰稿與查核，14 篇全部新增，依票 `2026-10-03-ai-terms-series-batch-02`。
撰稿指令見 [`brief.md`](brief.md)，指派見 [`catalogue.json`](catalogue.json)，查核規則見 [`VERIFY.md`](VERIFY.md)。
每篇的查證紀錄在 `staging/<slug>/`：`notes.md`（主張｜來源｜查證日｜讀法）、`research.json`、`verify-1.md`、`verify-2.md`。

「查核改動」是每輪查核者記下的事實性修改數（只算事實，不算措辭）。第一輪超過三處就換人做第二輪。

| 分組 | 名詞 | 標題 | 正文字數 | 來源數 | 查核改動（第一輪 → 第二輪） | slug |
| --- | --- | --- | ---: | ---: | --- | --- |
| 模型與 AI 基礎 | 神經網路 / Neural Network | 神經網路（Neural Network）是什麼：由層與權重組成、能從資料學習的函數 | 2,707 | 10 | 3 | `ai-term-neural-network` |
| 模型與 AI 基礎 | 注意力機制 / Attention Mechanism | 注意力機制（Attention）是什麼：模型怎麼決定要參考哪些 token | 2,866 | 9 | 5 → 4 | `ai-term-attention-mechanism` |
| 模型與 AI 基礎 | 推論 / Inference | 推論（Inference）是什麼：模型訓練完之後，每次回答都在做的計算 | 2,583 | 10 | 3 | `ai-term-inference` |
| 提示、token 與上下文 | 溫度 / Temperature | 溫度（Temperature）是什麼：AI 回答變化程度的取樣參數 | 2,737 | 11 | 6 → 2 | `ai-term-temperature` |
| 提示、token 與上下文 | 知識截止日 / Knowledge Cutoff | 知識截止日（Knowledge Cutoff）是什麼：模型知道到哪一天，又為什麼不準 | 2,718 | 13 | 6 → 3 | `ai-term-knowledge-cutoff` |
| 訓練、調整與推論資源 | 思維鏈 / Chain-of-Thought | 思維鏈（Chain-of-Thought）是什麼：讓模型寫出步驟，以及步驟能信多少 | 2,635 | 10 | 3 | `ai-term-chain-of-thought` |
| 提示、token 與上下文 | 結構化輸出 / Structured Outputs | 結構化輸出（Structured Outputs）是什麼：讓 AI 照固定格式交資料 | 2,552 | 7 | 7 → 0 | `ai-term-structured-outputs` |
| 搜尋、文件與知識 | 接地 / Grounding | 接地（Grounding）是什麼：讓 AI 的回答有可以對回去的依據 | 2,597 | 13 | 5 → 0 | `ai-term-grounding` |
| 評測、安全與人工介入 | AI 對齊 / AI Alignment | AI 對齊（Alignment）是什麼：對齊到誰的什麼，先問清楚 | 2,768 | 11 | 5 → 2 | `ai-term-ai-alignment` |
| 訓練、調整與推論資源 | 合成資料 / Synthetic Data | 合成資料（Synthetic Data）是什麼：兩種用途、品質控管與模型崩潰 | 2,729 | 9 | 4 → 0 | `ai-term-synthetic-data` |
| 模型與 AI 基礎 | 縮放定律 / Scaling Laws | 縮放定律（Scaling Laws）是什麼：規模變大，損失與能力怎麼變 | 2,704 | 11 | 5 → 0 | `ai-term-scaling-laws` |
| 評測、安全與人工介入 | 迎合 / Sycophancy | 迎合（Sycophancy）是什麼：AI 為什麼順著你說，怎麼問才不被帶著走 | 2,574 | 7 | 7 → 2 | `ai-term-sycophancy` |
| 模型與 AI 基礎 | 通用人工智慧 / Artificial General Intelligence | 通用人工智慧（AGI）是什麼：各家定義為什麼不一樣 | 2,656 | 10 | 6 → 3 | `ai-term-agi` |
| 代理、工具與互通協定 | 電腦操作 / Computer Use | 電腦操作（Computer Use）是什麼：讓 AI 看畫面、點滑鼠、打鍵盤 | 2,738 | 9 | 4 → 4 | `ai-term-computer-use` |

## 協調者在收件時另改的地方

- 「本文／這篇」每篇壓到一次（讀者優先規則，`intake_check.py` 的 self-reference 上限）。
- 正文不寫查證過程：「查證日為⋯⋯」「查證時讀到的頁面⋯⋯」改成「資料截至 2026 年 10 月」或直接陳述。
- `ai-term-neural-network`：activation function 用台灣慣用的「活化函數」（Google 繁中機器學習詞彙表的譯法），首次出現附「也常譯作激勵函數」。
- `ai-term-chain-of-thought`：Chen 等人 2025 的限制段，寫明作者推測非靠步驟不可的任務可能較忠實但沒測，且這次較難的 GPQA 反而較低。
- `ai-term-computer-use`：圖解標題不再說迴圈「從一張截圖開始」。
- `ai-term-structured-outputs`：H2 拿掉「今天」；拒答一句改成官方文件的「可能不符合 schema」。
- `ai-term-scaling-laws`：表格「答對率」改「表現」（Brown 量的是覆蓋率，不是答對率）。
- `ai-term-grounding`：符號接地問題改寫成「最常被引用的是 Harnad 1990 年的同名論文」，不主張詞源。
- `ai-term-agi`：圖說的自主性改成論文的說法（設計者與使用者選擇怎麼互動），不是「由部署方式決定」。
- `ai-term-ai-alignment`：Sharma 等人只說 "in part"，改成「迎合有一部分來自這種偏好判斷」。

## 總索引與速查

- `ai-terms-index`：14 篇分進既有六組，各組導言補一句，問題表加一列「AI 一直附和我，或同一題每次答得不同」。
  **正文 5,910 字，離 life 類 6,000 字上限只剩 90 字。** 下一批再加詞前要先改結構（例如各組只留導言、把連結改成清單，或拆成分組子索引）。
- `ai-glossary-50-terms`：temperature 與知識截止日兩條所在的「模型與訓練」組、電腦操作所在的「推理與代理」組，各加連到新專文的連結。
- 兩者都由 [`../integrate.py`](../integrate.py) 寫入，可重跑（已連過的不會重複加）。

## 發布順序（部署後，站主同意才做）

先 14 篇 `--dry-run`、再 `--publish`；確認公開後，最後才帶 `ai-terms-index` 與 `ai-glossary-50-terms` 發布。
