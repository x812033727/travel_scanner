# Till the Verdict Do Us Part 第一季台詞表

`extract.py` 讀 `docs/videos/till-the-verdict-eNNN/script.md` 每一集現有的分鏡表
（`| 鏡 | 景別、運鏡 | 畫面裡有誰 | 動作 | 台詞 | 秒數 |`），把每一句說出口的台詞寫成
`lines-s1.csv` 的一列，並印出每集的數字與給編劇的警告。只用 Python 標準函式庫，只讀劇本、不改劇本。

```bash
python3 -I docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western/production/lines/extract.py
# --quiet 只印數字；--out 另存 CSV；--root 指定 repo 根目錄
```

劇本改了就重跑一次；`lines-s1.csv` 是產出，不要手改。

## 欄位

| 欄 | 內容 |
| --- | --- |
| `episode`、`shot` | `e001`、`c07` |
| `speaker` | 冒號前的名字，照劇本原樣（含中文角色名） |
| `voice` | `model`（標「原聲」）或 `gemini`（標「Gemini」，含 `Gemini Leda` 這類指定聲音）；兩個都沒標時當 `model` 並警告 |
| `kind` | `inner`（心裡話）、`tv`（電視、廣告）、`phone`（電話、電話裡、電話那頭、電話濾波、語音）、`shout`（短喊；「不是短喊」不算）、`off-screen`（畫外）、其餘 `on-screen`；同一句有好幾個標記時照這個順序取第一個 |
| `english` | 冒號後到第一個全形括號或箭頭之前的英文 |
| `words` | 英文以空白切開、含英數字的字數 |
| `tone` | 說話人括號裡去掉聲音與種類標記後剩下的語氣說明 |
| `answer_to`、`because_of` | 「→ 答在 cNN」「← 因為 cNN」的鏡號，多個用 `;` 隔開；答在的不是鏡號時照寫（如「同一句」） |
| `shot_seconds` | 秒數欄的第一個「約 N 秒」；寫成範圍時取上限 |

一格裡有好幾句（用 `<br>` 隔開，或同一格接著第二個「名字（標記）：」）會拆成好幾列；
台詞欄是「—」開頭的鏡（沒有台詞、只有哭聲或懸念註記）不出列。

## 警告

1. 台詞超過 14 個字。
2. 模型原聲只有 6 個字以內。
3. Gemini 的台詞，但那一鏡的動作寫「嘴在說話」。
4. 同一場（同一個「###」標題底下）同一個角色既有原聲又有 Gemini（心裡話也算進來，看到時自己判斷）。
5. 鏡長短於「這一鏡台詞的總字數 ÷ 2.5 ＋ 0.5」秒。

另外會報表格本身的問題：欄數不對、秒數讀不出來、認不出說話的人、讀不到英文。
