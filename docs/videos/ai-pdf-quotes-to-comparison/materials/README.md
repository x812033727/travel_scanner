# 原創 PDF 報價比對練習

四份 PDF 是本教材自行撰寫的虛構文件：Aster、Birch、Cedar 原版與 Cedar 修訂版。
供應商、價格、日期與條件均不對應真實交易；5% 僅為明示練習假設。
每份兩頁，第一頁寫規格與價格，第二頁寫數量範圍與運費。

這次實測為目前的 OpenAI Codex 代理分析逐頁文字，再以 Python Decimal 計算。
不是 Claude、Gemini 或某產品上傳 PDF 介面的測試；本流程也沒有執行 OCR。
原始單價排序是算術對照，不是捏造某個普通提示詞失敗。

`quote-source.json` 是自行撰寫的 PDF 原文來源；`fixture-truth.json` 是獨立檢查答案。
**實際 AI 抽取時不要提供這兩個檔案或程式碼**，只提供實際 PDF 抽文、需求與提示詞。
AI 原始輸出完整保留，檢查器不把答案改寫成看似模型已答對的輸出。

## 重現

以下使用已安裝的 `requirements-lab.txt` 版本。PDF/PNG/XLSX 一律輸出 repo 外。
PDF 預覽需要 Poppler 的 `pdftoppm`；本次 Linux 字型為系統已有的 DejaVu Sans TTF
與 Noto Sans CJK。PDF 實際嵌入 DejaVu 字型，避免用替代字型造成字距錯亂。
程式目前以這個 Linux 環境的絕對字型路徑為準。

```bash
python3 docs/videos/ai-pdf-quotes-to-comparison/materials/generate_lab.py \
  --out /workspace/work/ai-pdf-01/lab
```

讓 AI 實際讀輸出資料夾中的 `requirements.txt`、`analysis-prompt.txt` 和
`extracted-pages.json`，產生 `normalized-quotes.json`。本次另實際採用了更適合
觀眾複製的 `viewer-prompt.txt`，執行時序及輸入雜湊記在 AI 代理自己的
`ai-analysis-execution.json`；不能由產檔程式冒造 AI 執行收據。

`request.json` 只有本次情境與數量。先用 10 張重做，再把副本的 quantity 改成 20。
原報價與修訂報價都明示單價、運費在 10–20 張內適用，所以這個變更有原文依據。
超出書面範圍（例如 21）會拒絕，不會猜測新單價或運費。

```bash
python3 docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py \
  --analysis /workspace/work/ai-pdf-01/lab/normalized-quotes.json \
  --extracted /workspace/work/ai-pdf-01/lab/extracted-pages.json \
  --request /workspace/work/ai-pdf-01/lab/requests/request-10.json \
  --out /workspace/work/ai-pdf-01/lab/results-request-10

python3 docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py \
  --analysis /workspace/work/ai-pdf-01/lab/normalized-quotes.json \
  --extracted /workspace/work/ai-pdf-01/lab/extracted-pages.json \
  --request /workspace/work/ai-pdf-01/lab/requests/request-20.json \
  --out /workspace/work/ai-pdf-01/lab/results-request-20
```

檢查器會先核對實際 AI 抽出的欄位、各原文短句及頁碼，再獨立驗算。
`selected-comparison.csv/json` 是讀本次 request 重新計算的結果；`comparison.xlsx`
另包含三個教學情境與「本次請求」工作表。CSV、XLSX、Markdown 使用同一份 Decimal 結果。

`comparison.xlsx` 寫入的是**已算數值**，儲存格可編輯，並不是即時公式計算器。
變更數量或條件後請重跑產檔；openpyxl 本身不計算 Excel 公式。本次確實用
`load_workbook(data_only=True)` 讀回金額與空白，也確認沒有假裝已算的公式格。

```bash
python3 docs/videos/ai-pdf-quotes-to-comparison/materials/render_results.py \
  --results /workspace/work/ai-pdf-01/lab/results-request-10 \
  --out /workspace/work/ai-pdf-01/lab/result-previews
```

結果 PNG/PDF 是實際計算資料的獨立可讀預覽，不是偽裝成 Excel 或 AI 對話介面的截圖。

## 這個案例要看什麼

- 原始單價：Cedar 175、Aster 180、Birch 205。
- 原版 10 張：Aster 2100、Birch 2050；Cedar 只知道商品含稅 1837.50，運費及其稅額未報，總價空白且不排序。
- Cedar 修訂版補運費後：Cedar 送達總價 2100，與 Aster 同價；Birch 仍最低。
- request 改成 20 張重跑：Aster 3990、Birch 4100、Cedar 修訂版 3937.50，最低改成 Cedar。
- Cedar 修訂版替代原版，不是第四家廠商；舊檔保留供追溯。

所有排序都只是**符合這份虛構需求、明示條件完整的候選中**比較總價；
不能把它擴張成真實供應商推薦、稅法判斷或 AI 對任何 PDF 都可靠的承諾。

## 已解壓教材的簡短重跑指令

教材解壓目錄把 `materials/` 與 `research/` 放在同一層。以下相對指令已在
本次 `/workspace/work/ai-pdf-01/repro-package/materials` 真正執行成功，輸出只在 repo 外。
先進入 `materials`，`request-20.json` 已是 `{ "scenario": "revised", "quantity": 20 }`。

```bash
python3 build_comparison.py \
  --analysis ../research/lab-ai-extraction.json \
  --extracted ../research/lab-extracted-pages.json \
  --request request-20.json \
  --out comparison-output
```

這個指令重現**本次已保存的 AI 抽取結果**如何產生 20 張比價表；不是重新呼叫 AI。
換成自己的 PDF 時，須先實際重做抽取與來源檢查，不能沿用這份虛構資料的 AI JSON。

## 相鄰數量的轉換點：12 張與 13 張

把修訂情境分別另存為 `request-12.json`、`request-13.json`，只改 `quantity`，
保留 `"scenario": "revised"` 及其他條件。這兩個數量都在三家原文明示的
10–20 張範圍內；Cedar 使用修訂版，甲與丙的固定運費各只計一次。
教材已附兩份可修改的需求檔。在解壓教材的 `materials` 資料夾分別執行：

```bash
python3 build_comparison.py \
  --analysis ../research/lab-ai-extraction.json \
  --extracted ../research/lab-extracted-pages.json \
  --request request-12.json \
  --out comparison-12

python3 build_comparison.py \
  --analysis ../research/lab-ai-extraction.json \
  --extracted ../research/lab-extracted-pages.json \
  --request request-13.json \
  --out comparison-13
```

兩份結果保存在不同資料夾。先看各自的 `selected-comparison.json`：確認需求為
12／13 張、情境為 `revised`，三家來源仍只有甲、乙、丙修訂版，再核對金額。
這是使用已保存 AI 抽取資料的本機重算，沒有再次呼叫模型。

| 需求數量 | 甲送達含稅總價 | 乙送達含稅總價 | 丙修訂版送達含稅總價 | 最低候選 |
| --- | ---: | ---: | ---: | --- |
| 12 張 | 2,478.00 | 2,460.00 | 2,467.50 | 乙 |
| 13 張 | 2,667.00 | 2,665.00 | 2,651.25 | 丙修訂版 |

上表金額單位為本練習的 TWD。差額固定用「丙減乙」：12 張為 `+7.50`，
表示丙較貴；13 張為 `-13.75`，表示丙較便宜。其他條件不變時，每多一張，
乙的含稅商品金額增加 `205.00`，丙增加 `175.00 × 1.05 = 183.75`；
丙相對乙每張追回 `21.25`，所以在這兩個相鄰數量之間跨過零。
這個轉換點只適用於本教材明示條件，不能外推至未報價的數量或真實供應商。

程式 stdout 的 `winners` 是固定三個教學情境（原版10／修訂10／修訂20）的
回歸檢查摘要，不是本次12／13張的名次。新數量的名次以各自
`selected-comparison.json` 的 `request`、`delivered_total` 與
`lowest_comparable` 為準。`research/quantity-threshold-12-13-execution.json`
保留兩次真實命令、退出碼、完整 stdout、選定結果及獨立 Decimal 核對。


## 數量超出報價範圍的負例練習

沿用同一份抽取結果，`request-21-invalid.json` 已把需求改成 21 張。
在解壓教材的 `materials` 資料夾執行：

```bash
python3 build_comparison.py \
  --analysis ../research/lab-ai-extraction.json \
  --extracted ../research/lab-extracted-pages.json \
  --request request-21-invalid.json \
  --out comparison-21
```

這是**預期失敗**的練習：退出碼為 1，最後一行是
`ValueError: Quantity outside explicitly quoted range`，不會建立新的 `comparison-21/`。
請先確認該輸出資料夾不存在，才能觀察「沒有建立」的結果；程式不會刪除你原本已有的資料夾。
原因是 21 張超出三份報價明示的 10–20 張適用範圍，不能直接沿用單價或運費條件。
`questions-21.txt` 是可編輯的重新詢價草稿，尚未寄出；供應商重報後才可更新原文與抽取資料。

`research/quantity-21-relative-execution.json` 保留本次已實跑的命令、輸入雜湊、
退出碼與 stderr；它是這個本機負例的執行證據，不是 AI 服務失敗或新一輪模型呼叫。
