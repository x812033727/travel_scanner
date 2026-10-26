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
