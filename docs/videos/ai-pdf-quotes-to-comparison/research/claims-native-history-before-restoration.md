# 事實、原始報價與實作主張

更新日期：2026-10-26（Asia/Taipei）。

（第 4 輪以前的內容全部保留，未修改：證據位置、最終來源綁定、官方來源、逐項主張 c1–c31、八頁原件摘錄、AI 身分、Decimal 三情境、相對命令、21 張拒絕、工具版本，以及第 1–4 輪查核紀錄。第 5、6 輪段落與「新增同一採購的21張範圍驗證」段落也保留未改；本次只在檔尾新增第 7 輪段落。）

## 第 5 輪事實查核（2026-10-26，獨立新工作階段）

### 結果

- c1–c16、c19–c31 CONFIRMED。
- c17、c18、tags、outro CTA 為 OUT OF SCOPE。
- CHANGED 0、NOT FOUND 0，video.json 未修改。

### 官方頁今日重讀（ok=true，status 200）

- **pypdf**（6.21.2 documentation）：https://pypdf.readthedocs.io/en/stable/user/extract-text.html 。以下句子逐字相符：
  - "If a PDF page appears to contain only an image (e.g., a scanned document), the extracted text may be minimal or visually empty."
  - "pypdf is not OCR software."
  - "Typically, tables are just absolutely positioned text."
  - "That makes it hard to tell where columns / rows are."
  - "PDF files don’t contain a semantic layer."
  - 對應 c29 handoff-scan、c30 handoff-table，以及 description 的 OCR 邊界。
- **openpyxl**（3.1.3 documentation）：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html 。"openpyxl never evaluates formula" 逐字相符，對應 c15 與 description。

### 第五次獨立重算

- **10 張原版**：
  - 甲：10×180＝1800，稅 90，運費 200×1.05＝210，合計 2100
  - 乙：10×205＝2050
  - 丙：10×175×1.05＝1837.5，運費 null，總價待確認
- **10 張修訂**：
  - 丙：1837.5＋262.5＝2100，與甲同價
  - 乙 2050 最低
- **20 張修訂**：
  - 甲：3780＋210＝3990（不是 4200）
  - 乙：4100
  - 丙：3675＋262.5＝3937.5，最低
  - 甲乙相對十張時反轉
- **e86a**：丙商品含稅比乙低 212.5，條件句成立。
- **卡片行數**：viewer-prompt 7 行、request-20.json 4 行，與 caption 相符。

### 規則檢查

- 免責語家族與查證用語，在旁白及 description 中都沒有出現。
- 稅率標明為練習假設。
- 沒有站主常設指示，旁白也沒有使用敘事者名字。

### 懷疑但未改（延續）

- aster.pdf、cedar-revised.pdf 第2頁逐字全文仍待摘入。這兩頁是 sxtz 與 quantity-ranges 的依據。
- requirements.txt 全文仍待摘入。
- 本輪 payload 未附八頁原件摘錄、quantity-run 原始 stdout、selected-comparison.json。成片前要對照 lab receipts 做視覺核對。

### 即將過期

- 金額全為原創 fixture，沒有會過期的價格。
- pypdf 6.21.2 與 openpyxl 3.1.3 的行為描述，以 2026-10-26 讀取為準。

## 第 6 輪事實查核（2026-10-26，獨立新工作階段）

### 結果

- c1–c16、c19–c31 CONFIRMED。
- c17、c18、outro CTA、tags 的風格部分為 OUT OF SCOPE。
- CHANGED 0、NOT FOUND 0，video.json 未修改。

### 官方頁今日重讀（ok=true，status 200）

- **pypdf 6.21.2**：https://pypdf.readthedocs.io/en/stable/user/extract-text.html 。以下句子逐字相符，對應 c29、c30：
  - "the extracted text may be minimal or visually empty"
  - "consider using OCR software such as Tesseract OCR"
  - "pypdf is not OCR software."
  - "Typically, tables are just absolutely positioned text."
  - "That makes it hard to tell where columns / rows are."
- **openpyxl 3.1.3**：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html 。"openpyxl never evaluates formula" 逐字相符，對應 c15 ehby 與 description。

### 第六次獨立重算（與第 5 輪一致）

- **10 張原版**：
  - 甲：1800＋90＋210＝2100
  - 乙：2050
  - 丙：商品含稅 1837.5，總價待確認
- **10 張修訂**：
  - 丙：1837.5＋262.5＝2100，與甲同價
  - 乙最低
- **20 張修訂**：
  - 甲：3780＋210＝3990
  - 乙：4100
  - 丙：3675＋262.5＝3937.5，最低
- **甲乙反轉**：10 張時 2100 對 2050，20 張時 3990 對 4100，pruf 成立。
- **e86a**：差額 212.5，條件句成立。
- **單價排序**：175、180、205。
- **卡片行數**：viewer-prompt 7 行、request-20.json 4 行。requirements 卡第 7–8 行與第 8–9 行的重疊行一致。

### 規則檢查

- 免責語家族與查證用語，在旁白及 description 中都沒有出現。
- 沒有站主常設指示。
- 沒有個人資料。
- 第三方頁未被用來佐證任何數字。

### 懷疑但未改

- quantity-run 與 quantity-output 的實跑內容，依據是 lab receipts（selected-comparison.json、stdout）。本輪 payload 仍未附這些原始輸出，無法直接核對。旁白只要求觀眾自行確認，沒有宣稱已觀察到的成功。成片前必須對照 receipts；對不上時，這兩張卡改標為預期輸出。
- aster.pdf、cedar-revised.pdf、cedar.pdf 第 2 頁的逐字全文，以及 requirements.txt 全文，仍待摘入。

### 即將過期

- 沒有會過期的價格。
- 套件行為描述以 2026-10-26 讀取的 pypdf 6.21.2 與 openpyxl 3.1.3 為準。

## 新增同一採購的21張範圍驗證

c36｜數量21超出原文10–20張範圍；同一程式實際exit1並未建立comparison-21｜原創PDF各第2頁及下列真實命令紀錄｜2026-10-26｜range21-request/run/result
c37｜重詢21張條件的文字僅為本次實寫的詢問草稿，未寄送、未取得供應商新報價｜materials/questions-21.txt｜2026-10-26｜range21-question

```json
{
  "executed_at_utc": "2026-10-26T09:16:45.033752+00:00",
  "cwd": "/workspace/work/ai-pdf-01/repro-package/materials",
  "command": [
    "python3",
    "build_comparison.py",
    "--analysis",
    "../research/lab-ai-extraction.json",
    "--extracted",
    "../research/lab-extracted-pages.json",
    "--request",
    "request-21-invalid.json",
    "--out",
    "comparison-21"
  ],
  "exit_code": 1,
  "stdout": "",
  "stderr": "Traceback (most recent call last):\n  File \"/workspace/work/ai-pdf-01/repro-package/materials/build_comparison.py\", line 234, in <module>\n    if __name__ == '__main__': main()\n                               ^^^^^^\n  File \"/workspace/work/ai-pdf-01/repro-package/materials/build_comparison.py\", line 196, in main\n    selected_rows = make_rows(quote_map, originals if selected_request['scenario']=='original' else revised, selected_request['quantity'])\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/workspace/work/ai-pdf-01/repro-package/materials/build_comparison.py\", line 70, in make_rows\n    result = delivered(fields, qty)\n             ^^^^^^^^^^^^^^^^^^^^^^\n  File \"/workspace/work/ai-pdf-01/repro-package/materials/build_comparison.py\", line 46, in delivered\n    raise ValueError('Quantity outside explicitly quoted range')\nValueError: Quantity outside explicitly quoted range\n",
  "displayed_exact_last_line": "ValueError: Quantity outside explicitly quoted range",
  "output_directory_created": false,
  "python_version": "3.12.14",
  "source_code_sha256": "35103b82d83b527b897bbc171e8d71e40431ebc0c4412a9c3ce62b898b160ea1",
  "request_sha256": "0f3f6f5c96284192bfc545f951e9c24f68b3867837f05ec8efa67f213fb99b4e",
  "analysis_sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
  "extracted_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
  "meaning": "Actual negative input validation by the AI-authored comparison program; not a model/provider failure or a fabricated terminal."
}
```

## 第 7 輪事實查核（2026-10-26，獨立新工作階段）

### 結果

- c1–c16、c19–c27、c31、c36、c37 CONFIRMED。
- c17、c18、title、thumbnail、tags、outro CTA 為 OUT OF SCOPE。
- CHANGED 0、NOT FOUND 0，video.json 未修改。

### 官方頁今日重讀（ok=true，status 200）

- **pypdf 6.21.2**：https://pypdf.readthedocs.io/en/stable/user/extract-text.html 。"pypdf is not OCR software." 逐字相符，對應 description 的 OCR 邊界。
- **openpyxl 3.1.3**：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html 。"openpyxl never evaluates formula" 逐字相符，對應 c15 ehby 與 description。

### 第七次獨立重算（與第 5、6 輪一致）

- **10 張原版**：
  - 甲：2100
  - 乙：2050
  - 丙：總價待確認（商品含稅 1837.5）
- **10 張修訂**：
  - 丙：2100，與甲同價
  - 乙 2050 最低
- **20 張修訂**：
  - 甲：3990
  - 乙：4100
  - 丙：3937.5，最低
- **e86a**：差額 212.5。
- **單價排序**：175、180、205。
- **卡片行數**：viewer-prompt 7 行、request-20.json 4 行、request-21-invalid.json 4 行，皆與 caption 相符。

### 21 張段落（range21-request、range21-run、range21-result、range21-question）

- **c36**：對照上方收據逐項相符：
  - 只更換 --request 與 --out，其餘輸入不變（cegb）
  - exit_code 1，最後一行 ValueError 與 quote 卡逐字相同
  - output_directory_created=false，對應 9jiq「也沒有建立新的結果資料夾」
  - 執行時間 2026-10-26，與 caption「實跑 2026-10-26」一致
- **egmv**：超出範圍的依據為 c24 的 10–20 張。
- **c37**：卡片 key 標「詢問草稿｜尚未寄出」，與 c37 一致。

### 規則檢查

- 旁白與 description 都沒有免責語家族用語或查證用語。
- 沒有站主常設指示。
- 沒有個人資料。
- 第三方頁（FableGuide、Kevin Stratvert）只用於選題觀測，未佐證任何上片數字。
- 沒有把預期結果寫成已觀察到的成功。

### 懷疑但未改

- quantity-run 與 quantity-output 的「實跑」標記依賴 c31 lab receipts。本輪 payload 仍未附原始 stdout 與 selected-comparison.json，成片前必須對照。
- 三家第 2 頁的逐字全文，以及 requirements.txt 全文，仍待摘入。
- range21 各行的 emotion 標記相同，屬於風格問題，未處理。

### 即將過期

- 沒有會過期的價格。
- 套件行為描述以 2026-10-26 讀取的 pypdf 6.21.2 與 openpyxl 3.1.3 為準。
