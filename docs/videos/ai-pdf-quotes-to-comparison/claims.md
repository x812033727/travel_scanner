# 事實、原始報價與實作主張

更新日期：2026-10-26（Asia/Taipei）。本片只教一件事：把三份報價整理成有來源、可依同一需求比較的表，再依修訂版與新數量重做。所有供應商與交易條件均為本次原創教材。百分之五稅率是練習明示假設，不判斷真實交易適用的法規或稅務處理。

實際 AI 分析者是 OpenAI Codex 代理 `/root/pdf_ai_extract`，它讀取 pypdf 的逐頁抽文及需求，留下欄位、原文、頁碼與待問問題。不是 Claude Cowork、Claude Artifacts、ChatGPT 上傳介面或掃描 OCR 的實測。精確金額由本次 Python Decimal 程式計算；openpyxl 寫入已算值，不宣稱它執行 Excel 公式。具體模型版本未由代理介面揭露，不能自行補寫。

## 證據位置與適用範圍

- 文字教材與可重做程式：本資料夾的 `materials/`。`quote-source.json` 與 `fixture-truth.json` 是出題資料與獨立核對答案，不是交給 AI 抽取者的輸入。
- 實際 PDF、逐頁抽文、AI 分析及結果：repo 外 `/workspace/work/ai-pdf-01/lab/`。
- 原始 AI 輸入：`requirements.txt`、`analysis-prompt.txt`、`extracted-pages.json`。分析者先讀這三份並產出結果，後來才實際讀取追加的七行 `viewer-prompt.txt` 並依它更新工作；不追溯聲稱短提示詞一開始就存在。時序見 `ai-analysis-execution.json`。
- 金額與比較：`results/comparison.json`、`results/verification.json`、`results/baseline-and-normalized-order.json`；可編輯交付檔為 `results/comparison.xlsx`，其實際工作表含「使用說明」「原報價10張」「修訂報價10張」「修訂報價20張」「逐欄來源」。
- 需求可改欄位與實際重做：`materials/request.json`、`materials/request-20.json` 與實際 `lab/requests/` 對應檔，`research/lab-request-runs.json` 記錄真正程式呼叫。`request-21-invalid.json` 的實際 exit 1 是超出明示適用範圍，不是 AI 失敗。

最終源綁定已實際核對：`research/lab-ai-extraction.json` SHA-256 為 `f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8`，`research/lab-extracted-pages.json` 為 `586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c`。`research/lab-verification-request-10.json` 與 `lab-verification-request-20.json` 真實綁定這兩個目前檔案，各17項實際核對全通過，並非沿用較早 `256b…`／`24cc…` 的歷史結果。PDF 內嵌字型修正後，AI 分析者實際重讀新版8頁文字、四份原輸入及追加的第5份 request-20.json，再重新判讀；完整時序保留於 `research/lab-ai-analysis-execution.json`。

公開來源快照對應：`research/lab-generation-receipt.json`（生成與版本）、`lab-extracted-pages.json`（實際8頁）、`lab-ai-extraction.json`（實際AI欄位）、`lab-ai-analysis-execution.json`（真實身分及輸入時序）、`lab-comparison.json`（三個情境）、`lab-verification-request-10.json`／`lab-verification-request-20.json`（獨立核對）、`lab-request-runs.json`（真正10／20／21程式執行）、`lab-relative-command-execution.json`（畫面相對命令的真正執行）、`lab-visual-review.json`（實際PDF與結果預覽）。本表引用的外部lab檔案均有這些可讀文字證據，不要求觀眾取得製作機器。

## 逐項主張

| ID | 主張／對應畫面 | 可核對證據 | 性質與限制 |
| --- | --- | --- | --- |
| c1 | 三家原報單價為甲 180 未稅、乙 205 含稅、丙 175 未稅 | 實際 `extracted-pages.json` 的 `aster.pdf`、`birch.pdf`、`cedar.pdf` 各第1頁；原創 `materials/quote-source.json` | 報價原文，不把不同稅基的單價直接當成總價 |
| c2 | 需求為10張同稿 A6、350 gsm 霧面白卡、雙面全彩、同一地址、7個工作天內送達 | `materials/requirements.txt` 第7–10行；實際三份 PDF 的規格及交期原文 | 三份教材都能對齊這組要求；不把報價自身的數量代替使用者需求 |
| c3 | 原始三家 PDF 保留，修訂版另存；輸出不修改原件 | 實際 `lab/pdfs/` 四檔；`materials/generate_lab.py`、`build_comparison.py`；`generation-receipt.json` | 沒有聲稱寄出詢問、下單或修改真實供應商檔案 |
| c4 | 供應商、價格與稅率全是原創虛構練習 | `materials/requirements.txt` 第1–5行及每份 PDF 的 fictional training quote 註記 | 5% 不是真實稅務建議，也不代表任何真實交易必須如此計稅 |
| c5 | 本次實際使用逐頁文字抽取、獨立 Codex AI 欄位判讀、Decimal 計算與 openpyxl 匯出 | `generation-receipt.json`、`extracted-pages.json`、`ai-analysis-execution.json`、`normalized-quotes.json`；`materials/build_comparison.py` | AI 沒有讀 fixture truth；特定商用 AI 的 UI、PDF 視覺理解及 OCR 未測試 |
| c6 | 甲商品單價與商品稅在第1頁，運費200未稅及運費稅5%在第2頁 | `aster.pdf` 第1–2頁的實際抽文；AI normalized 欄位的 verbatim evidence | `extract-aster-quote` 的英文為逐字原句；卡片引用不冒充產品截圖 |
| c7 | 七行 viewer-prompt 明確要求欄位、來源、缺漏、新舊版及交付內容 | `materials/viewer-prompt.txt` 全文；`ai-analysis-execution.json` 的追加提示詞與實際讀取時序 | 畫面顯示全文第1–7行；技術 analysis-prompt 另附較長 JSON schema，不隱稱只靠短提示詞就完成所有工作 |
| c8 | 乙單價205已含5%商品稅、送達免運，交期5工作天 | `birch.pdf` 第1–2頁；原文明說 no second goods tax；實際 normalized 值與來源 | 運費0有原文依據，與未報價不同 |
| c9 | 丙原版運費與其稅未報，shipping amount 保留 null，送達總價未知 | `cedar.pdf` 第2頁；AI `normalized-quotes.json`；實際 comparison 中該總價為 null／工作簿空格 | 已知商品金額不能替代完整送達總價；不擅填0或猜運費 |
| c10 | 真正執行原報單價排序得到丙→甲→乙 | `results/headline-unit-sort-baseline.csv`、`baseline-and-normalized-order.json`；實際 Decimal 程式 | 這是刻意只排原報單價的算術對照，不是冒稱簡單 AI 提示詞失敗，也不代表手工比價必然錯誤 |
| c11 | 甲10張：商品1800+商品稅90+運費含稅210，送達2100 | `aster.pdf` 第1–2頁；實際 `results/comparison.json`、獨立 `verification.json`；程式 Decimal | 只按此練習明示的兩種稅基計算 |
| c12 | 乙10張：205×10=2050，免運，不再加一次商品稅 | `birch.pdf` 第1–2頁；實際 comparison 與獨立核對 | 含稅單價已包含商品稅，不二次加稅 |
| c13 | 原始10張只有甲乙具有已知完整送達總價，乙比甲便宜；丙待確認 | `results/original-10.csv`、comparison 的 unknown 值與原文證據 | 「乙」只是在已知可比報價中最低，不宣稱未知丙的真實總價已被排除 |
| c14 | 算術使用 Decimal，而非先讓模型心算或提前四捨五入單價 | `materials/build_comparison.py` 的 Decimal 與金額量化；實際 verification | 不是測試所有模型的算術能力；也不是實際會計計價規範 |
| c15 | 試算表匯出已算值與逐欄來源，改需求後需重新產生 | 實際 `results/comparison.xlsx` 已以 openpyxl 讀回各表；「使用說明」明示固定值；官方 https://openpyxl.readthedocs.io/en/stable/simple_formulae.html（2026-10-26檢查） | 沒有宣稱活公式、自動重算、已在 Excel UI 開啟或互動操作 |
| c16 | 已包含於單價或小計的稅不能重複加入總額 | 乙原文 `No second goods tax is added to this inclusive unit price.`；本次程式 inclusive 分支 | 這是計算基準的條件判斷，不假造另一份錯誤 AI 結果 |
| c17 | 缺運費、稅基或稅額時可產生具體待問清單 | 實際 `results/questions.txt`；`missing-question` 為依缺漏撰寫的可修改詢問草稿 | 草稿未寄出、沒有供應商真的回覆或同意；數量範圍亦需核對運費是否適用 |
| c18 | 比價狀態可分條件完整、費用缺漏、規格不同；規格不同應先問不能編升級價 | 原創教學建議；本次實際規格全部相同，只有丙運費缺漏 | 「規格不同」是使用規則的條件式示例，不說成這次真有一份不合規格 |
| c19 | Cedar修訂版明示取代原版，仍為同一家；商品內容保持，送貨條件更新 | `cedar-revised.pdf` 第1–2頁；實際 `results/change-log.json`；revision scenario 只3家 | 不把舊版、新版當成兩家，來源欄同步換成新檔 |
| c20 | 丙修訂10張：商品含稅1837.50+運費含稅262.50=2100.00 | 實際 revised-10 CSV、comparison、verification；修訂 PDF 的250未稅運費與5%運費稅 | 與甲同價；不是同一稅額被算兩次 |
| c21 | 補件後10張乙2050最低，甲丙2100同價 | 實際 `results/revised-10.csv` 及 baseline-and-normalized-order 的同價分組 | 不為了產生唯一名次捏造評分，也不把交期差異私自折算成金額 |
| c22 | 改運費時，證據也應改指向修訂版來源 | 實際 revised-10／revised-20 的來源欄及工作簿逐欄來源；change-log | 操作建議與真實結果相符；不宣稱原版包含後來新增的費用 |
| c23 | 改 request.json 的 quantity=20 可重新選取修訂情境下20張的比較 | `requests/request-10.json`、`requests/request-20.json`；實際 `actual-request-runs.json`，`results-request-20/selected-comparison.json`；AI追加需求處理收據 | 畫面顯示教材 `request-20.json` 第1–4行全文；AI已實際讀此第5輸入重判數量適用；程式另有真正20張重算，不假造 requirements20 文字檔 |
| c24 | 三家皆明示單價適用10–20；甲200未稅及丙修訂250未稅運費在範圍內固定，乙免運 | 三家相對應 PDF 第2頁原文；實際 normalized range evidence | 只有此範圍能依原文重算；21的實際要求被程式拒絕，不能擴張成任何數量都可用 |
| c25 | 甲20張送達含稅總價3990 | 實際 `results/revised-20.csv`、comparison 與獨立 Decimal 核對 | (20×180+200)×1.05=3990 |
| c26 | 乙20張送達含稅總價4100 | 實際 revised-20 與獨立核對 | 20×205=4100；免運、單價已含稅 |
| c27 | 丙修訂20張送達含稅總價3937.50，於此情境最低 | 實際 revised-20 與獨立核對 | (20×175+250)×1.05=3937.50；固定運費分攤比例改變，不是供應商臨時降價 |
| c28 | 真正輸出可編輯比價XLSX、CSV、待問問題與版本變動 | 實際 `results/comparison.xlsx`、三份 CSV、questions.txt、change-log.json、comparison.md；實際 data_only 讀回 | 本片不宣稱已在商用試算表UI打開、修改或實測自動公式重算 |
| c29 | 本次 pypdf 文字流程不做掃描影像OCR，文字抽不到要換能辨識的流程並核原圖 | 官方 https://pypdf.readthedocs.io/en/stable/user/extract-text.html（2026-10-26）；本次輸入為真正可選取文字 PDF | 不是「所有AI都不能讀掃描PDF」；本次沒有處理影像掃描，因此不宣稱OCR準確率 |
| c30 | PDF文字可選仍可能因表格換行、多欄位置而失去語義，需要核對原頁 | 同一 pypdf 官方抽取文件；本次逐欄 literal evidence 核對 | 一般路線限制，不假造本次真的抽錯或模型失誤 |
| c31 | 在教材materials目錄執行畫面上的完整相對命令，可依request-20.json輸出20張修訂情境及仍只有3家供應商 | 真正 `research/lab-relative-command-execution.json`：cwd `/workspace/work/ai-pdf-01/repro-package/materials`，argv逐字對應code卡，exit0；analysis與extracted雜湊對應上述最終輸入；actual selected_result 數量20、Aster／Birch／Cedar修訂版共3列 | 命令以shell續行分為5行，沒有改參數或簡寫；輸出 comparison-output 在repo外，未把此計算命令說成AI模型呼叫或商用UI操作 |

## 與企劃不同的地方

本次三份報價的商品規格全部相同，困難來自含稅基準、跨頁運費與缺漏條件；沒有另造一份不合規格的報價來戲劇化。實際單價排序被清楚標成算術對照，未把刻意少算的對照冒稱某款 AI 的真實失敗。數量更新的可改檔是 JSON request，而不是假造已操作的商用介面。

## 我懷疑但沒動的事

短提示詞屬分析完成後的真實追加要求；片中雖逐字顯示它，說明欄與本表保留完整分析要求及時序，不能把長技術要求與實際人工核對隱去。報價視覺與xlsx能否閱讀仍須用真正預覽驗收；檔案生成成功、稿子估算9.9分鐘，都不是成片已通過的證據。

## 進度

腳本已寫56場景、107句，原始103句的line IDs保留，新增命令與結果4句使用先前未用ID。新字型PDF／8頁抽文／獨立AI重新判讀／10與20實際重算／21拒絕／相對命令／結果視覺的真實來源均已保存；這些是範例驗收，不是主影片音訊或成片QA。字幕、音檔及八語要分別完成後才可聲稱完成。此檔不代填任何尚未執行的AI judge或站主核准。

## 直接提供查核者的實作證據摘錄

下面的內容直接取自本片現行真實收據與輸出，放進 claims 全文，讓只收到本檔、而無法讀製作機器或 repo 路徑的查核者仍能逐項評估。它們是本次原創資料的直接摘錄，與一般外網功能文件分開；不聲稱查核者曾打開未交給它的本機檔案。

### 八頁原件的關鍵原句

以下每個區塊標明實際檔名與頁碼。原文大小寫、金額與標點保留；省略其他段落，不重新拼成另一句。全體抽文 SHA-256：`586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c`。


**aster.pdf 第1頁**

```text
Currency: TWD
Item: A6 postcard (105 x 148 mm)
Paper: 350 gsm matte white card
Print: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 180.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,800.00
```


**aster.pdf 第2頁**

```text
Quantity range: 10 to 20 pieces inclusive
Shipping: TWD 200.00 excluding tax to the specified address
Shipping tax: 5% of shipping net amount
Shipping remains TWD 200.00 net for 10 to 20 pieces.
Lead time: 7 business days
```


**birch.pdf 第1頁**

```text
Size: A6 postcard (105 x 148 mm)
Stock: 350 gsm matte white card
Printing: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Currency: TWD
Unit price: TWD 205.00 including 5% goods tax
No second goods tax is added to this inclusive unit price.
```


**birch.pdf 第2頁**

```text
Quantity range: 10 to 20 pieces inclusive
The TWD 205.00 tax-inclusive unit price stays the same in this range.
Shipping: TWD 0.00; delivery to the specified address is free
Shipping tax: TWD 0.00; no separate shipping charge or shipping tax
Shipping tax mode: inclusive; shipping tax rate: 0%
Lead time: 5 business days
```


**cedar.pdf 第1頁**

```text
Currency: TWD
Product: A6 postcard (105 x 148 mm)
Material: 350 gsm matte white card
Print specification: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 175.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,750.00
```


**cedar.pdf 第2頁**

```text
Quantity range: 10 to 20 pieces inclusive
Shipping: not quoted
Shipping tax: not quoted
Lead time: 7 business days
Do not assume shipping is free; ask for a written delivery quote.
```


**cedar-revised.pdf 第1頁**

```text
Replaces CED-1026-v1; not an additional supplier.
Currency: TWD
Product: A6 postcard (105 x 148 mm)
Material: 350 gsm matte white card
Print specification: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 175.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,750.00
```


**cedar-revised.pdf 第2頁**

```text
Quantity range: 10 to 20 pieces inclusive
Shipping: TWD 250.00 excluding tax to the specified address
Shipping tax: 5% of shipping net amount
Shipping remains TWD 250.00 net for 10 to 20 pieces.
Lead time: 7 business days
Only delivery terms changed; all goods specifications and prices remain.
```


### 真實AI分析身分、輸入與沒有做的事

技術 analysis-prompt 與七行 viewer-prompt 都實際讀取。修字型後又真實重讀新8頁及 request-20.json。下面是分析者自己的實際紀錄子集，不把生成程式或 fixture truth 說成模型見過的資料。

```json
{
  "actual_identity": {
    "provider": "OpenAI",
    "agent": "OpenAI Codex agent",
    "agent_task": "/root/pdf_ai_extract",
    "interface": "Codex multi-agent execution",
    "specific_model_identifier": "Not exposed to this agent; no unsupported model name claimed."
  },
  "actual_rerun_inputs": [
    {
      "path": "/workspace/work/ai-pdf-01/lab/requirements.txt",
      "sha256": "c3c38e75c01b15a10b8fe8540e367fad8eeebbf0a0dcc7f8fcd4d00100759fa3",
      "bytes": 1131,
      "input_order_in_rerun": 1,
      "first_received_history": "Initial input in the first three-input task."
    },
    {
      "path": "/workspace/work/ai-pdf-01/lab/analysis-prompt.txt",
      "sha256": "dc159f0d4ad8713e3c7d28cc9a43df823ec20fe2bd25687105f1001c7d29921f",
      "bytes": 2387,
      "input_order_in_rerun": 2,
      "first_received_history": "Initial input in the first three-input task."
    },
    {
      "path": "/workspace/work/ai-pdf-01/lab/extracted-pages.json",
      "sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
      "bytes": 6693,
      "input_order_in_rerun": 3,
      "first_received_history": "Initial input in the first three-input task."
    },
    {
      "path": "/workspace/work/ai-pdf-01/lab/viewer-prompt.txt",
      "sha256": "6b491f229d7f5e12f53c2f56de3c812614f4ec7ac96e9042127aa45bb6d3a5c4",
      "bytes": 442,
      "input_order_in_rerun": 4,
      "first_received_history": "Added after initial extraction as viewer prompt."
    },
    {
      "path": "/workspace/work/ai-pdf-01/lab/requests/request-20.json",
      "sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
      "bytes": 46,
      "input_order_in_rerun": 5,
      "first_received_history": "New fifth input supplied with the quantity-20 follow-up task."
    }
  ],
  "output": {
    "path": "research/lab-ai-extraction.json",
    "sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8"
  },
  "not_read_or_used": [
    "Repository content and source code",
    "Generators",
    "quote-source.json",
    "fixture-truth.json",
    "Other source fixtures or answer files",
    "Other agents' outputs",
    "Source PDF binaries",
    "Network resources or paid APIs",
    "Commercial AI product interfaces",
    "OCR or PDF image interpretation"
  ],
  "font_correction_rerun": {
    "current_extracted_pages_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
    "all_eight_pages_actually_reread": true,
    "fields_rebuilt_from_current_text": true,
    "semantic_field_changes": [],
    "literal_evidence_triples_validated": 128
  }
}
```


### Decimal 實際輸出的三個情境

下列為 `research/lab-comparison.json` 的真實內容，保留 null 與新舊來源檔名，沒有把不知道的運費補0。`lab-verification-request-10.json`、`lab-verification-request-20.json` 各17個真正檢查全部通過，且都綁定上方同一組最終分析與抽文雜湊。

```json
{
  "original-10": [
    {
      "supplier": "Aster",
      "source_file": "aster.pdf",
      "quantity": 10,
      "unit_price": "180.00",
      "unit_tax_mode": "exclusive",
      "goods_gross": "1890.00",
      "shipping_gross": "210.00",
      "delivered_total": "2100.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 7,
      "price_source": "aster.pdf p.1",
      "shipping_source": "aster.pdf p.2",
      "lowest_comparable": false
    },
    {
      "supplier": "Birch",
      "source_file": "birch.pdf",
      "quantity": 10,
      "unit_price": "205.00",
      "unit_tax_mode": "inclusive",
      "goods_gross": "2050.00",
      "shipping_gross": "0.00",
      "delivered_total": "2050.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 5,
      "price_source": "birch.pdf p.1",
      "shipping_source": "birch.pdf p.2",
      "lowest_comparable": true
    },
    {
      "supplier": "Cedar",
      "source_file": "cedar.pdf",
      "quantity": 10,
      "unit_price": "175.00",
      "unit_tax_mode": "exclusive",
      "goods_gross": "1837.50",
      "shipping_gross": null,
      "delivered_total": null,
      "status": "待確認：運費及其稅額未報",
      "comparable": false,
      "lead_business_days": 7,
      "price_source": "cedar.pdf p.1",
      "shipping_source": "cedar.pdf p.2",
      "lowest_comparable": false
    }
  ],
  "revised-10": [
    {
      "supplier": "Aster",
      "source_file": "aster.pdf",
      "quantity": 10,
      "unit_price": "180.00",
      "unit_tax_mode": "exclusive",
      "goods_gross": "1890.00",
      "shipping_gross": "210.00",
      "delivered_total": "2100.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 7,
      "price_source": "aster.pdf p.1",
      "shipping_source": "aster.pdf p.2",
      "lowest_comparable": false
    },
    {
      "supplier": "Birch",
      "source_file": "birch.pdf",
      "quantity": 10,
      "unit_price": "205.00",
      "unit_tax_mode": "inclusive",
      "goods_gross": "2050.00",
      "shipping_gross": "0.00",
      "delivered_total": "2050.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 5,
      "price_source": "birch.pdf p.1",
      "shipping_source": "birch.pdf p.2",
      "lowest_comparable": true
    },
    {
      "supplier": "Cedar",
      "source_file": "cedar-revised.pdf",
      "quantity": 10,
      "unit_price": "175.00",
      "unit_tax_mode": "exclusive",
      "goods_gross": "1837.50",
      "shipping_gross": "262.50",
      "delivered_total": "2100.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 7,
      "price_source": "cedar-revised.pdf p.1",
      "shipping_source": "cedar-revised.pdf p.2",
      "lowest_comparable": false
    }
  ],
  "revised-20": [
    {
      "supplier": "Aster",
      "source_file": "aster.pdf",
      "quantity": 20,
      "unit_price": "180.00",
      "unit_tax_mode": "exclusive",
      "goods_gross": "3780.00",
      "shipping_gross": "210.00",
      "delivered_total": "3990.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 7,
      "price_source": "aster.pdf p.1",
      "shipping_source": "aster.pdf p.2",
      "lowest_comparable": false
    },
    {
      "supplier": "Birch",
      "source_file": "birch.pdf",
      "quantity": 20,
      "unit_price": "205.00",
      "unit_tax_mode": "inclusive",
      "goods_gross": "4100.00",
      "shipping_gross": "0.00",
      "delivered_total": "4100.00",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 5,
      "price_source": "birch.pdf p.1",
      "shipping_source": "birch.pdf p.2",
      "lowest_comparable": false
    },
    {
      "supplier": "Cedar",
      "source_file": "cedar-revised.pdf",
      "quantity": 20,
      "unit_price": "175.00",
      "unit_tax_mode": "exclusive",
      "goods_gross": "3675.00",
      "shipping_gross": "262.50",
      "delivered_total": "3937.50",
      "status": "可比較",
      "comparable": true,
      "lead_business_days": 7,
      "price_source": "cedar-revised.pdf p.1",
      "shipping_source": "cedar-revised.pdf p.2",
      "lowest_comparable": true
    }
  ]
}
```


### 畫面上的相對命令確實執行過

命令卡的5行以 shell 續行表達，下列 argv 是同一條真正執行的命令，實際解壓教材目錄包含兄弟 `materials`／`research`，輸出留 repo 外。`selected-comparison.json` 中 request.quantity 為20、scenario為revised、三列來源為 aster.pdf、birch.pdf、cedar-revised.pdf；不是說成執行這條程式就又呼叫了一次 AI。

```json
{
  "cwd": "/workspace/work/ai-pdf-01/repro-package/materials",
  "command": [
    "python3",
    "build_comparison.py",
    "--analysis",
    "../research/lab-ai-extraction.json",
    "--extracted",
    "../research/lab-extracted-pages.json",
    "--request",
    "request-20.json",
    "--out",
    "comparison-output"
  ],
  "exit_code": 0,
  "stdout": "{\"output\": \"comparison-output\", \"checks\": 17, \"all_passed\": true, \"winners\": {\"original-10\": [\"Birch\"], \"revised-10\": [\"Birch\"], \"revised-20\": [\"Cedar\"]}}\n",
  "stderr": "",
  "all_generated_files_outside_repo": true,
  "code_sha256": "35103b82d83b527b897bbc171e8d71e40431ebc0c4412a9c3ce62b898b160ea1",
  "analysis_sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
  "extracted_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
  "request_sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
  "output_files": [
    {
      "path": "comparison-output/baseline-and-normalized-order.json",
      "bytes": 601,
      "sha256": "9de1c612ae82e3c4dbdf00abe1aaf2c509a7925cb2e00eecf888f629588eaa2c"
    },
    {
      "path": "comparison-output/change-log.json",
      "bytes": 573,
      "sha256": "5eece163997905a316890f7acf8e84bf82e57a3218105b5ddae1c59b716558b9"
    },
    {
      "path": "comparison-output/comparison.json",
      "bytes": 4304,
      "sha256": "c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab"
    },
    {
      "path": "comparison-output/comparison.md",
      "bytes": 1319,
      "sha256": "403eb971cacecc3cb83f7c44af857306d72c36a19c8e27c7712abaf348c72800"
    },
    {
      "path": "comparison-output/comparison.xlsx",
      "bytes": 13525,
      "sha256": "f6ab1291ca9b17934ade3826087ad0890efbf7ea7fe154172ac0bd66f2d94fc1"
    },
    {
      "path": "comparison-output/headline-unit-sort-baseline.csv",
      "bytes": 448,
      "sha256": "4672e1eba5c482d194c250de197e18b4e57a7703be9eb2c5e5185875067edf6a"
    },
    {
      "path": "comparison-output/original-10.csv",
      "bytes": 531,
      "sha256": "ce6b009a07c14160dc8c6f632815e9d06cb856018fdc8c129e9dd98d529e8435"
    },
    {
      "path": "comparison-output/questions.txt",
      "bytes": 504,
      "sha256": "fa572e87cedfce6246f78cc4f6f773da35ffde32f99a45c4c55cf97a0ef5bab2"
    },
    {
      "path": "comparison-output/revised-10.csv",
      "bytes": 540,
      "sha256": "93c64f00c828eb4c8cd168ebdc749f742a9d33a8e2e4ef653072081321d0d6aa"
    },
    {
      "path": "comparison-output/revised-20.csv",
      "bytes": 540,
      "sha256": "1161a12d8e5f8a55d3465624bb941dd98c45b4a1d8a97b4891c0ccd5e78916b6"
    },
    {
      "path": "comparison-output/selected-comparison.csv",
      "bytes": 540,
      "sha256": "1161a12d8e5f8a55d3465624bb941dd98c45b4a1d8a97b4891c0ccd5e78916b6"
    },
    {
      "path": "comparison-output/selected-comparison.json",
      "bytes": 1586,
      "sha256": "aafb2cefc8d163c2631ec55d7d60d95ad3fa195457781a255ddf17d940064a64"
    },
    {
      "path": "comparison-output/verification.json",
      "bytes": 5311,
      "sha256": "574839210e8d327f108099a985aef71248ddaae090d474583ac4f2d17e2c4827"
    }
  ]
}
```


### 超出原報價範圍的實際拒絕

這筆反例只有21張超出明示10–20範圍，並不是AI亂答。實際紀錄保留 exit1、錯誤文字與沒有產生輸出：

```json
{
  "command": [
    "python3",
    "docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py",
    "--analysis",
    "/workspace/work/ai-pdf-01/lab/normalized-quotes.json",
    "--extracted",
    "/workspace/work/ai-pdf-01/lab/extracted-pages.json",
    "--out",
    "/workspace/work/ai-pdf-01/lab/results-request-21-invalid",
    "--request",
    "/workspace/work/ai-pdf-01/lab/requests/request-21-invalid.json"
  ],
  "exit_code": 1,
  "stdout": "",
  "stderr": "Traceback (most recent call last):\n  File \"/workspace/travel_scanner_pdf/docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py\", line 234, in <module>\n    if __name__ == '__main__': main()\n                               ^^^^^^\n  File \"/workspace/travel_scanner_pdf/docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py\", line 196, in main\n    selected_rows = make_rows(quote_map, originals if selected_request['scenario']=='original' else revised, selected_request['quantity'])\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/workspace/travel_scanner_pdf/docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py\", line 70, in make_rows\n    result = delivered(fields, qty)\n             ^^^^^^^^^^^^^^^^^^^^^^\n  File \"/workspace/travel_scanner_pdf/docs/videos/ai-pdf-quotes-to-comparison/materials/build_comparison.py\", line 46, in delivered\n    raise ValueError('Quantity outside explicitly quoted range')\nValueError: Quantity outside explicitly quoted range\n",
  "output_created": false
}
```


### 真正使用的工具版本與視覺限度

```json
{
  "Python": "Python 3.12.14",
  "reportlab": "4.4.9",
  "pypdf": "6.10.0",
  "openpyxl": "3.1.5",
  "Pillow": "12.3.0"
}
```

上述版本是本機實際版本，不稱最新版。`research/lab-visual-review.json` 記錄實際4份8頁PDF和結果預覽已查看、字型修正後可讀且無裁切；結果預覽是我們根據真實計算輸出另行排版的文件，不是 Excel 或 AI 產品 UI 截圖。圖文預覽可讀、欄位與算術通過，也不能單獨證明主影片音訊或成片已通過。
