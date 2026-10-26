# 事實、原始報價與實作主張

更新日期：2026-10-26（Asia/Taipei）。

（第 1 輪以前的內容全部保留，未修改，包括：證據位置、最終來源綁定、官方來源、逐項主張 c1–c31、八頁原件摘錄、AI 身分、Decimal 三情境、相對命令、21 張拒絕、工具版本、第 1 輪查核、原生 verifier 後的逐字核對。）

## 第 2 輪事實查核（2026-10-26，獨立新工作階段）

### 結果

- c1–c17、c19–c31 全數 CONFIRMED。
- c18（教學建議）與 tags／CTA 為 OUT OF SCOPE。
- CHANGED 0、NOT FOUND 0，video.json 未修改。

### 官方頁今日讀取（ok=true）

- **pypdf Extract Text**：https://pypdf.readthedocs.io/en/stable/user/extract-text.html（頁面 pypdf 6.21.2 documentation）。逐字句：
  - "If a PDF page appears to contain only an image (e.g., a scanned document), the extracted text may be minimal or visually empty."
  - "pypdf is not OCR software."
  - "Typically, tables are just absolutely positioned text."
  - "PDF files don’t contain a semantic layer."
- **openpyxl**：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html（頁面 openpyxl 3.1.3 documentation）。逐字句："openpyxl never evaluates formula"。

### 獨立重算（與 lab-comparison 及 stdout winners 一致）

- **10 張原版**：甲 10×180=1800、稅 90、運費 200×1.05=210，合計 2100；乙 10×205=2050，運費 0；丙商品含稅 1837.50，運費 null，總價待確認。
- **10 張修訂**：丙 1837.50＋250×1.05=262.50，合計 2100.00，與甲同價；乙 2050 最低。
- **20 張修訂**：甲 20×180×1.05=3780＋210=3990；乙 4100；丙 20×175×1.05=3675＋262.50=3937.50，最低。
- **request-20.json**：逐字元重算為 46 bytes（含結尾換行），與紀錄相符。

### 卡片原句核對

- extract-aster-quote、extract-missing-quote、revision-identity 三句與 PDF 摘錄逐字相符。
- 頁碼標示一致：aster 第2頁、cedar 第2頁、cedar-revised 第1頁。

### 第三方來源

Kevin Stratvert 兩頁與 FableGuide 只用於企劃參考，沒有拿來確認任何數字，影片也沒有引用。

### 懷疑但未改

- **sxtz「三份報價都寫明，單價在範圍內保持相同」**：只有 birch 第2頁摘錄有逐字句。aster 與 cedar-revised 的摘錄只有 "Quantity range: 10 to 20 pieces inclusive"，且摘錄註明省略其他段落。程式依此範圍重算，21 張被拒絕，語意成立。待補：把 aster.pdf 與 cedar-revised.pdf 第2頁全文摘入本檔。
- **requirements.txt 第1–10行全文**：仍未摘入本檔。need-spec 與 need-delivery 的程式碼卡目前依 root exact string equality 紀錄（research/verifier-followup-exact-text.json）採信。

### 即將過期

無。片中金額都是原創 fixture。pypdf 與 openpyxl 的行為描述以 2026-10-26 的頁面版本為準，未來版本若有變動要重查。
