# 事實、原始報價與實作主張：完整證據 ledger

更新日期：2026-10-26（Asia/Taipei）。本次僅復原／補齊提供查核者的真實文字證據；沒有呼叫模型或外部 API，沒有改影片、原生 auto、核准、音訊或付費收據，也沒有把本 ledger 當成新的查核通過。

本片只教同一件事：把三家原創虛構報價整理成有逐欄來源、能依共同需求比較的表，依修訂版、數量20及超出範圍的21張追蹤結果。供應商、交易條件及5%稅率皆為明示練習假設，不對應真實採購或稅法判斷。


## 復原來源與現行綁定

- 原始完整 ledger 確實存在於 git `a2c088e49e93f1a6c0ccea8730a23da43bde74ee` 的本片 `claims.md`：29857 bytes，SHA-256 `91e1de197b7f157603dc989dd8ff56a195599469cc71211c6802c9c75bec3e3f`。下方 c1–c31 的證據列保留這份真實版本；只在 c15、c29 的既有 URL 後補一個分隔空白，避免原生網址抽取把相鄰全形日期括號黏入網址造成假404，未更動任何事實或來源。內容不從記憶補寫。
- 被原生後續回答替換成「以前內容全部保留」佔位文字的目前檔案，已逐字保存在 `research/claims-native-history-before-restoration.md`，SHA-256 `8250adb0157038ac0e68175fe352c7f9e31d5e4a167f3eb1204e97f715526249`。該檔只作原生歷史紀錄，佔位句不能證明遺失的內容仍在。
- 第8輪實際查核輸入 `video.json` SHA-256 `d990cd49715dcfdc6992e34c1ceff281f12a893d3481e55080fb693c9874c069`；55 scenes／101 narration lines。沒有把舊ledger的場景或句數冒稱成現在的版本。
- 實際本地教材 `research/lab-ai-extraction.json` SHA-256 `f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8`；八頁抽文 SHA-256 `586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c`。全文直接放在下方，使只收到本 ledger 的查核者也能核對，不能再以未提供本機檔案作為已讀證據。


## 逐項主張 c1–c37 與現版使用範圍

c1–c31 為原始完整 ledger 的真實編號；c36–c37 是後來同一採購的21張練習。c32–c35 沒有在可找回的原始 ledger 或現行 video 中定義，不為了連號捏造四項新主張。c16、c28–c30 保留作既有背景證據，但現版沒有 scene 直接引用；c29／c30 仍只說明本地文字抽取路線的限制。

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
| c15 | 試算表匯出已算值與逐欄來源，改需求後需重新產生 | 實際 `results/comparison.xlsx` 已以 openpyxl 讀回各表；「使用說明」明示固定值；官方 https://openpyxl.readthedocs.io/en/stable/simple_formulae.html （2026-10-26檢查） | 沒有宣稱活公式、自動重算、已在 Excel UI 開啟或互動操作 |
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
| c29 | 本次 pypdf 文字流程不做掃描影像OCR，文字抽不到要換能辨識的流程並核原圖 | 官方 https://pypdf.readthedocs.io/en/stable/user/extract-text.html （2026-10-26）；本次輸入為真正可選取文字 PDF | 不是「所有AI都不能讀掃描PDF」；本次沒有處理影像掃描，因此不宣稱OCR準確率 |
| c30 | PDF文字可選仍可能因表格換行、多欄位置而失去語義，需要核對原頁 | 同一 pypdf 官方抽取文件；本次逐欄 literal evidence 核對 | 一般路線限制，不假造本次真的抽錯或模型失誤 |
| c31 | 在教材materials目錄執行畫面上的完整相對命令，可依request-20.json輸出20張修訂情境及仍只有3家供應商 | 真正 `research/lab-relative-command-execution.json`：cwd `/workspace/work/ai-pdf-01/repro-package/materials`，argv逐字對應code卡，exit0；analysis與extracted雜湊對應上述最終輸入；actual selected_result 數量20、Aster／Birch／Cedar修訂版共3列 | 命令以shell續行分為5行，沒有改參數或簡寫；輸出 comparison-output 在repo外，未把此計算命令說成AI模型呼叫或商用UI操作 |

| c32 | 未定義、現版未引用 | 原始完整 ledger 及現行 `video.json` 均無此 ID | 不補造主張 |
| c33 | 未定義、現版未引用 | 原始完整 ledger 及現行 `video.json` 均無此 ID | 不補造主張 |
| c34 | 未定義、現版未引用 | 原始完整 ledger 及現行 `video.json` 均無此 ID | 不補造主張 |
| c35 | 未定義、現版未引用 | 原始完整 ledger 及現行 `video.json` 均無此 ID | 不補造主張 |
| c36 | 同一份程式使用數量21的實際需求時拒絕計算，exit1，沒有建立 comparison-21 | 四份 PDF 第2頁的10–20範圍；`materials/request-21-invalid.json`；`research/quantity-21-relative-execution.json` 的完整 argv/stdout/stderr 與 output_directory_created=false，全文如下 | 真實程式的負面輸入驗證；不是AI供應商服務失敗，也沒有新報價或新總價 |
| c37 | 重詢21張同規格單價、運費、交期的字句是本次實寫詢問草稿 | `materials/questions-21.txt` 全文如下；現版 range21-question 卡片逐字相符 | 未寄出、未下單、未取得供應商回覆；不假稱已同意或已報新價格 |

### 現版逐 scene 的實際 claim 引用

| ID | 現版 scene IDs |
| --- | --- |
| c1 | `opening-unit` |
| c2 | `need-start`、`need-spec`、`need-delivery` |
| c3 | `need-labels` |
| c4 | `need-fiction` |
| c5 | `need-route`、`extract-start` |
| c6 | `need-proof`、`extract-start`、`extract-aster`、`extract-aster-quote` |
| c7 | `extract-core`、`extract-fields` |
| c8 | `extract-birch`、`extract-review` |
| c9 | `extract-missing-quote`、`extract-null`、`extract-review`、`missing-start`、`missing-known` |
| c10 | `cost-start`、`cost-unit-baseline` |
| c11 | `cost-aster-formula`、`cost-initial-result` |
| c12 | `cost-birch-formula`、`cost-initial-result` |
| c13 | `cost-initial-result`、`missing-start` |
| c14 | `cost-rounding`、`cost-workbook` |
| c15 | `cost-workbook` |
| c16 | 沒有現版 scene 引用；保留原始背景證據 |
| c17 | `missing-question`、`missing-no-send` |
| c18 | `missing-status` |
| c19 | `revision-start`、`revision-identity`、`revision-diff`、`revision-links` |
| c20 | `revision-diff`、`revision-total`、`revision-ranking` |
| c21 | `revision-ranking` |
| c22 | `revision-links` |
| c23 | `quantity-start`、`quantity-edit`、`quantity-prompt`、`quantity-run`、`quantity-output` |
| c24 | `quantity-ranges` |
| c25 | `quantity-aster`、`quantity-ranking` |
| c26 | `quantity-birch`、`quantity-ranking` |
| c27 | `quantity-cedar`、`quantity-ranking` |
| c28 | 沒有現版 scene 引用；保留原始背景證據 |
| c29 | 沒有現版 scene 引用；保留原始背景證據 |
| c30 | 沒有現版 scene 引用；保留原始背景證據 |
| c31 | `quantity-run`、`quantity-output` |
| c32 | 沒有現版 scene 引用；未曾定義 |
| c33 | 沒有現版 scene 引用；未曾定義 |
| c34 | 沒有現版 scene 引用；未曾定義 |
| c35 | 沒有現版 scene 引用；未曾定義 |
| c36 | `range21-request`、`range21-run`、`range21-result` |
| c37 | `range21-question` |

## 實際 AI 身分、原始提示與工具版本

本次實際欄位分析者是 OpenAI Codex 代理 `/root/pdf_ai_extract`。它經 Codex multi-agent execution 讀逐頁文字；分析代理介面沒有揭露具體 model identifier，不能補填 GPT、Claude 或其他模型版本。它沒有讀 PDF 二進位／頁面圖、fixture truth、生成器、repo、其他代理答案或網路；不能把這次實作說成 Claude Cowork、Claude Artifacts、ChatGPT PDF-upload UI 或 OCR 的安裝／操作／實測。影片查核／撰稿階段的其他供應商模型也不能取代這份實際抽取者身分。

以下身份與時序直接取自 `research/lab-ai-analysis-execution.json`，不是本次補寫的假執行收據：

```json
{
  "executed_at_utc": "2026-10-26T06:58:52.874972+00:00",
  "actual_identity": {
    "provider": "OpenAI",
    "agent": "OpenAI Codex agent",
    "agent_task": "/root/pdf_ai_extract",
    "interface": "Codex multi-agent execution",
    "specific_model_identifier": "Not exposed to this agent; no unsupported model name claimed."
  },
  "inputs": [
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
  "scope_executed": [
    "Initial extraction and later viewer-prompt application remain recorded in prior_run_provenance and exact original prompt fields.",
    "Actually reread the four refreshed inputs, reviewed all eight page texts, and reconstructed every extracted field from the current source text.",
    "Validated literal evidence for all fields, supporting scope mappings, revision differences, scenario notes, questions, and the quantity-20 analysis against current pages.",
    "Actually read request-20.json as the fifth input, selected the revised scenario with three suppliers, confirmed quantity and shipping applicability, and preserved original Cedar missing values.",
    "Actually ran Python decimal.Decimal to calculate selected suppliers at 10 and 20 for quantity-change comparison and ranking; no spreadsheet execution was claimed.",
    "Wrote normalized-quotes.json, quantity-20-analysis.json, and this updated execution record; independent lab calculations and editable table creation remain downstream."
  ],
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
  "independence": "Source analysis used only the five explicitly authorized input files plus task instructions. Own previous artifacts were used solely for provenance/comparison. No archive, fixture truth, results, generators, repository content, other agents' outputs, PDFs, network resource, or OCR was accessed.",
  "outputs": [
    {
      "path": "/workspace/work/ai-pdf-01/lab/normalized-quotes.json",
      "sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
      "bytes": 22847
    },
    {
      "path": "/workspace/work/ai-pdf-01/lab/quantity-20-analysis.json",
      "sha256": "e25cbe467150f9f3c28509c5fef97b808f9371e41fa0bc6679cc020b7de3305c",
      "bytes": 19007
    }
  ],
  "updated_at_utc": "2026-10-26T07:06:40.290951+00:00",
  "font_correction_rerun": {
    "parent_reported_change": "Embedded existing DejaVuSans in regenerated PDFs to repair text spacing; business meaning unchanged.",
    "archive_location_reported_by_parent": "/workspace/work/ai-pdf-01/lab/versions/before-embedded-fonts",
    "archive_opened": false,
    "current_extracted_pages_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
    "all_eight_pages_actually_reread": true,
    "fields_rebuilt_from_current_text": true,
    "semantic_field_changes": [],
    "literal_evidence_triples_validated": 128,
    "page_checks": [
      {
        "source_file": "aster.pdf",
        "page": 1,
        "current_page_text_sha256": "49b85cdcf5fe25a11795d562f2673f6c026a4cc74695611c59d790fa3fcea663",
        "literal_evidence_matches": 13,
        "reviewed_content": "Goods specifications, original quoted quantity, currency, unit price and goods tax."
      },
      {
        "source_file": "aster.pdf",
        "page": 2,
        "current_page_text_sha256": "d64eb9e1801ebbc59a8aaf9534d9e8fb6204d29e5552b809f393681c7b74ea3e",
        "literal_evidence_matches": 17,
        "reviewed_content": "Quantity range, stable unit price, destination shipping and shipping tax or missing terms, shipping scope, and lead time."
      },
      {
        "source_file": "birch.pdf",
        "page": 1,
        "current_page_text_sha256": "1cc5dad170395ca2513ddc76871f9d769534648db8260566e7b23a5d389f8b97",
        "literal_evidence_matches": 13,
        "reviewed_content": "Goods specifications, original quoted quantity, currency, unit price and goods tax."
      },
      {
        "source_file": "birch.pdf",
        "page": 2,
        "current_page_text_sha256": "3027612a139fcd109845baf3ab9c5384d43ae11b60f8f1128fd051b21503c314",
        "literal_evidence_matches": 17,
        "reviewed_content": "Quantity range, stable unit price, destination shipping and shipping tax or missing terms, shipping scope, and lead time."
      },
      {
        "source_file": "cedar.pdf",
        "page": 1,
        "current_page_text_sha256": "6f1d3979ce33f60c0128e77f91a8115ba2cbf91e3c996c806618de9bcc5155fa",
        "literal_evidence_matches": 6,
        "reviewed_content": "Goods specifications, original quoted quantity, currency, unit price and goods tax."
      },
      {
        "source_file": "cedar.pdf",
        "page": 2,
        "current_page_text_sha256": "79c9db4c6687893e032f520bdd3e0b248ff95e1484e12902ddbfb2ade03914b5",
        "literal_evidence_matches": 25,
        "reviewed_content": "Quantity range, stable unit price, destination shipping and shipping tax or missing terms, shipping scope, and lead time."
      },
      {
        "source_file": "cedar-revised.pdf",
        "page": 1,
        "current_page_text_sha256": "506a41872e581b309d7fce543fd4275555d716e31a7f2319e2207290bc0b0120",
        "literal_evidence_matches": 15,
        "reviewed_content": "Goods specifications, original quoted quantity, currency, unit price and goods tax."
      },
      {
        "source_file": "cedar-revised.pdf",
        "page": 2,
        "current_page_text_sha256": "62336c07e11bde354e83dd7ff0abc107d6cc8f5cb496bfba50a026a3458849c6",
        "literal_evidence_matches": 22,
        "reviewed_content": "Quantity range, stable unit price, destination shipping and shipping tax or missing terms, shipping scope, and lead time."
      }
    ]
  }
}
```

初次給分析者的是 requirements、較長的 analysis-prompt 與八頁抽文；七行 viewer-prompt 是完成初次分析後才真實追加並讀取。嵌入字型修正後，代理確實重讀目前八頁與前四個輸入，再讀第5份 request-20.json。不能把長技術schema、後補提示、人工核對或第5輸入隱去，聲稱一開始只有七行提示便自動完成全部工作。

### 實際安裝版本與官方頁標示分開

```json
{
  "actual_generation_receipt": "research/lab-generation-receipt.json",
  "actual_tools": {
    "reportlab": "4.4.9",
    "pypdf": "6.10.0",
    "openpyxl": "3.1.5",
    "Pillow": "12.3.0"
  },
  "python_version_from_real_quantity21_receipt": "3.12.14",
  "generation_method": "Original ReportLab PDFs, extracted with actual installed pypdf; actual Poppler preview rendering",
  "generator_ai_extraction_executed_flag": false,
  "generator_flag_meaning": "生成器本身不呼叫或假造AI抽取；另一次真正獨立AI執行由上述analysis-execution記錄，兩者不是矛盾的完成聲明。"
}
```

實測用的是 pypdf 6.10.0、openpyxl 3.1.5；官方 stable 網頁當時頁首顯示的 pypdf 6.21.2／openpyxl 3.1.3 只是所讀文件標籤，不是本機安裝版本，不得把兩組號碼混成同一次安裝實測。


## 官方文件來源與本地實作的界線

下列內容取自既存 `research/sources-20261026.json` 的2026-10-26官方頁查閱紀錄；本次 ledger 復原沒有再次連網，不追加或捏造新的HTTP狀態。官方頁的存在／閱讀只支持功能說明，不等於本片安裝或實測了該服務。

```json
[
  {
    "id": "pypdf-text-extraction",
    "title": "Extract Text from a PDF",
    "url": "https://pypdf.readthedocs.io/en/stable/user/extract-text.html",
    "checked_on": "2026-10-26",
    "page_label_observed": "pypdf 6.21.2 documentation",
    "supports": [
      "PdfReader exposes pages and page.extract_text(), including a layout extraction mode.",
      "PDF text extraction and table reconstruction can be ambiguous; page appearance alone is not a semantic table."
    ],
    "limits": "This library is not OCR. Image-only scans can yield little or no text and need an appropriate OCR workflow. This is a limitation of our selected local extraction route, not a claim about all multimodal AI products.",
    "production_requirement": "Record the actually installed library version separately. Extract and inspect every source page before scripting any successful result."
  },
  {
    "id": "openpyxl-formulas",
    "title": "Using formulae",
    "url": "https://openpyxl.readthedocs.io/en/stable/simple_formulae.html",
    "checked_on": "2026-10-26",
    "page_label_observed": "openpyxl 3.1.3 documentation",
    "supports": "A workbook can contain Excel formula strings written by openpyxl.",
    "limits": "openpyxl does not evaluate those formulas. Do not label blank cached values as calculated spreadsheet results.",
    "production_requirement": "Verify numeric values independently, and either supply explicit calculated-value columns alongside formulas or use a real spreadsheet engine and record that actual recalculation."
  },
  {
    "id": "claude-academy-file-creation",
    "title": "Create and edit files with Claude to eliminate hours of busy work",
    "url": "https://academy.claude.com/tutorials/create-and-edit-files-with-claude-to-eliminate-hours-of-busy-work",
    "checked_on": "2026-10-26",
    "supports": "Official examples connect multiple input files with coordinated editable document and spreadsheet outputs.",
    "limits": "Capability and teaching reference only. Reading this page does not establish that this production ran Claude or its UI."
  },
  {
    "id": "claude-pdf-support",
    "title": "PDF support",
    "url": "https://platform.claude.com/docs/en/build-with-claude/pdf-support",
    "checked_on": "2026-10-26",
    "supports": "The official API route describes processing extracted PDF text together with rendered page images, subject to platform/model/request requirements.",
    "limits": "API PDF processing is a different path from the local pypdf text extraction demonstrated here. Do not transpose its limits to a chat UI or imply it was exercised."
  },
  {
    "id": "claude-upload-help",
    "title": "Upload files to Claude",
    "url": "https://support.claude.com/en/articles/8241126-upload-files-to-claude",
    "checked_on": "2026-10-26",
    "supports": "The help page distinguishes PDF visual analysis from text-only processing and recommends PDF-viewer page numbers for references.",
    "limits": "Do not promise that an arbitrary screenshot or scanned document will work through our local text route. No chat-plan limits are needed in this tutorial; recheck official documentation if adding any numeric limits."
  }
]
```

pypdf 的原意是此文字抽取路線不做 OCR，PDF 表格／多欄也不自帶可靠語義；不能擴張成所有多模態AI都不能讀掃描PDF。openpyxl 官方的短句 `openpyxl never evaluates formula` 說明它不計算公式。本教材使用 Decimal 真正計算，再寫值到 XLSX；沒有假稱 Excel UI 重新計算、已操作商用試算表或提供活公式計算器。

Kevin Stratvert／FableGuide 等公開頁只作選題與呈現研究；其日期、第三方點閱觀測不是本教材金額的證據，也不是即時YouTube分析或對本片成效保證。完整研究限制保存在同一 sources JSON，未把外國案例的資料或對話搬成本次實測。


## 四份原創 PDF 的八頁實際抽文全文

以下是 `research/lab-extracted-pages.json` 的各 page.text 原字串全文，沒有省略跨頁運費、數量有效範圍、交期或練習註記。這是 pypdf 實際抽出的文字，不是重新拼排成供應商的另一份報價。

### aster.pdf 第1頁

PDF SHA-256：`bce9caf069869382befd06316469df97993648e0163a00cbd71f2f73cacc3b5b`；此 page.text UTF-8 SHA-256：`49b85cdcf5fe25a11795d562f2673f6c026a4cc74695611c59d790fa3fcea663`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
ASTER PRINT / PRICE SHEET
aster.pdf    |    Page 1 of 2
Quote AST-1026 / Original / 2026-10-26
Currency: TWD
Item: A6 postcard (105 x 148 mm)
Paper: 350 gsm matte white card
Print: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 180.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,800.00
The delivered total also includes page 2 terms.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Aster / original / fictional exercise only
1 / 2
```

### aster.pdf 第2頁

PDF SHA-256：`bce9caf069869382befd06316469df97993648e0163a00cbd71f2f73cacc3b5b`；此 page.text UTF-8 SHA-256：`d64eb9e1801ebbc59a8aaf9534d9e8fb6204d29e5552b809f393681c7b74ea3e`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
ASTER / DELIVERY AND SCOPE
aster.pdf    |    Page 2 of 2
Quote AST-1026 / Terms belonging to page 1
Quantity range: 10 to 20 pieces inclusive
Unit price stays TWD 180.00 excluding tax throughout this range.
Shipping: TWD 200.00 excluding tax to the specified address
Shipping tax: 5% of shipping net amount
Shipping remains TWD 200.00 net for 10 to 20 pieces.
Lead time: 7 business days
Payment: one payment after acceptance
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Aster / original / fictional exercise only
2 / 2
```

### birch.pdf 第1頁

PDF SHA-256：`03fd30a530d9c2b0f6930e745f75180dac97c47e1b6a5b64dc1f23f7e2bac173`；此 page.text UTF-8 SHA-256：`1cc5dad170395ca2513ddc76871f9d769534648db8260566e7b23a5d389f8b97`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
BIRCH / SIMPLE ALL-IN OFFER
birch.pdf    |    Page 1 of 2
Offer BIR-20261026 / Original / 2026-10-26
For: one A6 postcard design, printed identically
Size: A6 postcard (105 x 148 mm)
Stock: 350 gsm matte white card
Printing: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Currency: TWD
Unit price: TWD 205.00 including 5% goods tax
No second goods tax is added to this inclusive unit price.
Read page 2 for shipping and quantity range.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Birch / original / fictional exercise only
1 / 2
```

### birch.pdf 第2頁

PDF SHA-256：`03fd30a530d9c2b0f6930e745f75180dac97c47e1b6a5b64dc1f23f7e2bac173`；此 page.text UTF-8 SHA-256：`3027612a139fcd109845baf3ab9c5384d43ae11b60f8f1128fd051b21503c314`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
BIRCH / INCLUDED IN YOUR OFFER
birch.pdf    |    Page 2 of 2
Offer BIR-20261026 / Included terms
Quantity range: 10 to 20 pieces inclusive
The TWD 205.00 tax-inclusive unit price stays the same in this range.
Shipping: TWD 0.00; delivery to the specified address is free
Shipping tax: TWD 0.00; no separate shipping charge or shipping tax
Shipping tax mode: inclusive; shipping tax rate: 0%
Lead time: 5 business days
Payment: one payment after acceptance
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Birch / original / fictional exercise only
2 / 2
```

### cedar.pdf 第1頁

PDF SHA-256：`bb17821765e31fa26e3b6a82cfdfc63403f56740de4719d67d48fc25850e61f9`；此 page.text UTF-8 SHA-256：`6f1d3979ce33f60c0128e77f91a8115ba2cbf91e3c996c806618de9bcc5155fa`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR PRINT / GOODS QUOTATION
cedar.pdf    |    Page 1 of 2
Quotation CED-1026-v1 / Original / 2026-10-26
Currency: TWD
Product: A6 postcard (105 x 148 mm)
Material: 350 gsm matte white card
Print specification: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 175.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,750.00
This is a goods quotation; see page 2 before comparing delivery.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / original / fictional exercise only
1 / 2
```

### cedar.pdf 第2頁

PDF SHA-256：`bb17821765e31fa26e3b6a82cfdfc63403f56740de4719d67d48fc25850e61f9`；此 page.text UTF-8 SHA-256：`79c9db4c6687893e032f520bdd3e0b248ff95e1484e12902ddbfb2ade03914b5`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR / TERMS REQUIRING CLARIFICATION
cedar.pdf    |    Page 2 of 2
Quotation CED-1026-v1 / Original delivery terms
Quantity range: 10 to 20 pieces inclusive
Unit price stays TWD 175.00 excluding tax throughout this range.
Shipping: not quoted
Shipping tax: not quoted
Lead time: 7 business days
Payment: one payment after acceptance
Do not assume shipping is free; ask for a written delivery quote.
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / original / fictional exercise only
2 / 2
```

### cedar-revised.pdf 第1頁

PDF SHA-256：`54e8b2bc9943e0707d424e860a10de5cb76d4dc2199c0ea1bfc7d8899401f414`；此 page.text UTF-8 SHA-256：`506a41872e581b309d7fce543fd4275555d716e31a7f2319e2207290bc0b0120`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR PRINT / REVISED QUOTATION
cedar-revised.pdf    |    Page 1 of 2
Quotation CED-1026-v2 / Revised / 2026-10-26
Replaces CED-1026-v1; not an additional supplier.
Currency: TWD
Product: A6 postcard (105 x 148 mm)
Material: 350 gsm matte white card
Print specification: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 175.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,750.00
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / revised / fictional exercise only
1 / 2
```

### cedar-revised.pdf 第2頁

PDF SHA-256：`54e8b2bc9943e0707d424e860a10de5cb76d4dc2199c0ea1bfc7d8899401f414`；此 page.text UTF-8 SHA-256：`62336c07e11bde354e83dd7ff0abc107d6cc8f5cb496bfba50a026a3458849c6`。

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR / WRITTEN DELIVERY CLARIFICATION
cedar-revised.pdf    |    Page 2 of 2
Quotation CED-1026-v2 / Revised delivery terms
Quantity range: 10 to 20 pieces inclusive
Unit price stays TWD 175.00 excluding tax throughout this range.
Shipping: TWD 250.00 excluding tax to the specified address
Shipping tax: 5% of shipping net amount
Shipping remains TWD 250.00 net for 10 to 20 pieces.
Lead time: 7 business days
Payment: one payment after acceptance
Only delivery terms changed; all goods specifications and prices remain.
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / revised / fictional exercise only
2 / 2
```


## 需求、觀眾提示與可改需求檔全文

### `materials/requirements.txt` 全文

實際檔案 SHA-256：`c3c38e75c01b15a10b8fe8540e367fad8eeebbf0a0dcc7f8fcd4d00100759fa3`；1131 bytes。以下逐字複製，不重寫。

```text
練習案例：比較三家虛構供應商的明信片印刷報價

本教材完全原創，所有供應商與交易條件均屬虛構。
金額單位為練習用新臺幣 TWD。5% 是本練習指定的計算假設，
不是對任何真實交易稅法、稅率或會計處理的判斷。

原始需求：10 張 A6 明信片（105 × 148 mm），350 gsm 霧面白卡紙，
雙面全彩，所有稿件相同；送到同一個指定地址，7 個工作天內交貨。
比的是符合需求、送達且含明示稅額的總價，不是單價。
規格或費用沒寫就列待確認，不能把缺漏視為 0，也不能自行補稅。

後續練習一：Cedar 補寄 cedar-revised.pdf。保留原檔，使用修訂版替代
Cedar 原報價重做 10 張比較，列出改了哪些欄位。
後續練習二：數量改成 20 張，其餘條件相同。先確認各報價的數量
適用範圍與運費，再重算；不可假設原來的最低總價仍然最低。

所有來源 PDF 都是可選取文字的 PDF。本流程不示範掃描影像 OCR。
原件只讀；輸出放另一個資料夾。重要欄位都保留檔名和頁碼。
```

### `materials/viewer-prompt.txt` 全文

實際檔案 SHA-256：`6b491f229d7f5e12f53c2f56de3c812614f4ec7ac96e9042127aa45bb6d3a5c4`；442 bytes。以下逐字複製，不重寫。

```text
請比較 requirements.txt 與三家報價的逐頁原文。
先列規格、適用數量、幣別、單價、稅、運費、交期。
每個欄位附檔名、頁碼及支持它的原句。
沒寫的填待確認，不能當作零或自行補價格。
Cedar 修訂版取代原版參與比價，原檔保留。
確認規格和數量可比，再按已知稅與運費計算總價。
交付可編輯比價表、待問問題及修訂前後差異。
```

### `materials/request.json` 全文

實際檔案 SHA-256：`7c1d5d568212a5c6e31042f1e7f8fc542950956814ce044b1f3a05868e8a9b30`；46 bytes。以下逐字複製，不重寫。

```json
{
  "scenario": "revised",
  "quantity": 10
}
```

### `materials/request-20.json` 全文

實際檔案 SHA-256：`53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62`；46 bytes。以下逐字複製，不重寫。

```json
{
  "scenario": "revised",
  "quantity": 20
}
```

### `materials/request-21-invalid.json` 全文

實際檔案 SHA-256：`0f3f6f5c96284192bfc545f951e9c24f68b3867837f05ec8efa67f213fb99b4e`；46 bytes。以下逐字複製，不重寫。

```json
{
  "scenario": "revised",
  "quantity": 21
}
```

### `materials/questions-21.txt` 全文

實際檔案 SHA-256：`dbbc86c25a90002c3538dd34d58eb3da14a86f273f5bce2e55a53da9137d26fe`；66 bytes。以下逐字複製，不重寫。

```text
想改成21張，請重報同規格的單價、運費和交期。
```

較長的初始技術提示也逐字提供，避免只展示後補七行提示而隱去原始schema：

### `materials/analysis-prompt.txt` 全文

實際檔案 SHA-256：`dc159f0d4ad8713e3c7d28cc9a43df823ec20fe2bd25687105f1001c7d29921f`；2387 bytes。以下逐字複製，不重寫。

```text
你是本次實際執行的 AI 文件分析者。請讀 requirements.txt 與 extracted-pages.json
（原創可選文字 PDF 的逐頁 pypdf 抽文）。不要讀 generator、quote-source.json、
fixture-truth.json 或其他答案。這不是任一特定商用 AI 介面或 PDF 視覺 OCR 的測試。

請只依提供的逐頁原文抽出 Aster、Birch、Cedar、Cedar 修訂版的下列資料。
每一個值都附 source_file、page（1 開始）、evidence（原文短句）。
沒寫的值一律 null，unknown 不等於 0。請分清單價已含稅／未稅與運費是否已含稅；
不得替原本的 Cedar 編造總價，也不要把舊、新 Cedar 當成兩家不同供應商。

交付 JSON：
{
  "analyst": "實際使用的模型/代理身分；不要冒稱另一模型",
  "input_files": ["檔名"],
  "quotes": [{
    "supplier": "Aster|Birch|Cedar",
    "source_file": "檔名",
    "revision": "original|revised",
    "fields": {
      "specification": {"value":"完整規格字串", "page":1, "evidence":"原句"},
      "quoted_quantity": {"value":10, "page":1, "evidence":"原句"},
      "quantity_min": {"value":數字或null, "page":頁碼, "evidence":"原句"},
      "quantity_max": {"value":數字或null, "page":頁碼, "evidence":"原句"},
      "currency": {"value":"TWD", "page":頁碼, "evidence":"原句"},
      "unit_price": {"value":"精確金額字串", "page":頁碼, "evidence":"原句"},
      "unit_tax_mode": {"value":"exclusive|inclusive|unknown", "page":頁碼, "evidence":"原句"},
      "goods_tax_rate": {"value":"0.05"或null, "page":頁碼, "evidence":"原句"},
      "shipping_amount": {"value":"精確金額字串"或null, "page":頁碼, "evidence":"原句"},
      "shipping_tax_mode": {"value":"exclusive|inclusive|unknown", "page":頁碼, "evidence":"原句"},
      "shipping_tax_rate": {"value":"0.05"或null, "page":頁碼, "evidence":"原句"},
      "lead_business_days": {"value":數字或null, "page":頁碼, "evidence":"原句"}
    },
    "questions": [{"field":"欄位", "question":"真正待問問題", "page":頁碼}]
  }],
  "limitations": ["本次 pypdf 文字抽取不做 OCR；原文缺漏仍需詢問。"]
}

請先抽欄位，勿用自行心算的總價取代原文欄位。比價表另由 Decimal 計算，
再由不讀你推理的獨立檢查器對照 fixture truth；試算表內會寫明值的計算方法。
```


## 三個情境的真實計算結果與獨立核對

### `research/lab-comparison.json` 全文

實際檔案 SHA-256：`c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab`；4304 bytes。以下逐字複製，不重寫。

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

### `research/lab-baseline-and-normalized-order.json` 全文

實際檔案 SHA-256：`9de1c612ae82e3c4dbdf00abe1aaf2c509a7925cb2e00eecf888f629588eaa2c`；601 bytes。以下逐字複製，不重寫。

```json
{
  "method": "Actual arithmetic unit-price sort of the three original quotes, without tax/delivery normalization",
  "not_a_claimed_model_failure": true,
  "unit_price_order": [
    "Cedar",
    "Aster",
    "Birch"
  ],
  "unit_prices": [
    "175.00",
    "180.00",
    "205.00"
  ],
  "normalized_original_10_order": [
    "Birch",
    "Aster"
  ],
  "original_Cedar": "not comparable: delivery cost and delivery tax are unknown",
  "revised_10_groups": [
    [
      "Birch"
    ],
    [
      "Aster",
      "Cedar"
    ]
  ],
  "revised_20_order": [
    "Cedar",
    "Aster",
    "Birch"
  ]
}
```

`research/lab-verification-request-10.json` 與 `lab-verification-request-20.json` 是實際核對，不是本次重新執行。20張核對的所有來源綁定與checks逐字如下：

### `research/lab-verification-request-20.json` 全文

實際檔案 SHA-256：`580591e663d330e16e07d28a9f98ee4dee720f8093f46fb90d2c83d1e8b1b4c9`；5350 bytes。以下逐字複製，不重寫。

```json
{
  "checked_at_utc": "2026-10-26T07:07:35.310302+00:00",
  "actual_ai_analyst": "OpenAI Codex agent (sub-agent /root/pdf_ai_extract)",
  "analysis_sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
  "selected_request": {
    "scenario": "revised",
    "quantity": 20
  },
  "request_sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
  "extracted_pages_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
  "truth_sha256": "ba02380452061fe58abc6a4187566b9d101dce26f9c9242efcf85cda87ad37ee",
  "verification": "Independent fixture field assertions, exact page-evidence substring checks, Decimal totals, actual xlsx data_only readback, unknown shipping kept blank, revision replacement and out-of-range rejection",
  "checks": [
    {
      "check": "independent_total",
      "file": "aster.pdf",
      "quantity": 10,
      "actual": "2100.00",
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "aster.pdf",
      "quantity": 20,
      "actual": "3990.00",
      "pass": true
    },
    {
      "check": "reject_out_of_range_quantity_21",
      "file": "aster.pdf",
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "birch.pdf",
      "quantity": 10,
      "actual": "2050.00",
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "birch.pdf",
      "quantity": 20,
      "actual": "4100.00",
      "pass": true
    },
    {
      "check": "reject_out_of_range_quantity_21",
      "file": "birch.pdf",
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "cedar.pdf",
      "quantity": 10,
      "actual": null,
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "cedar.pdf",
      "quantity": 20,
      "actual": null,
      "pass": true
    },
    {
      "check": "reject_out_of_range_quantity_21",
      "file": "cedar.pdf",
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "cedar-revised.pdf",
      "quantity": 10,
      "actual": "2100.00",
      "pass": true
    },
    {
      "check": "independent_total",
      "file": "cedar-revised.pdf",
      "quantity": 20,
      "actual": "3937.50",
      "pass": true
    },
    {
      "check": "reject_out_of_range_quantity_21",
      "file": "cedar-revised.pdf",
      "pass": true
    },
    {
      "check": "winner_and_no_duplicate_revision",
      "scenario": "original-10",
      "winners": [
        "Birch"
      ],
      "pass": true
    },
    {
      "check": "winner_and_no_duplicate_revision",
      "scenario": "revised-10",
      "winners": [
        "Birch"
      ],
      "pass": true
    },
    {
      "check": "winner_and_no_duplicate_revision",
      "scenario": "revised-20",
      "winners": [
        "Cedar"
      ],
      "pass": true
    },
    {
      "check": "actual_headline_sort_is_Cedar_Aster_Birch_not_model_failure",
      "pass": true
    },
    {
      "check": "actual_request_file_drives_selected_table",
      "request_file": "/workspace/work/ai-pdf-01/lab/requests/request-20.json",
      "request_sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
      "quantity": 20,
      "scenario": "revised",
      "totals": {
        "Aster": "3990.00",
        "Birch": "4100.00",
        "Cedar": "3937.50"
      },
      "pass": true
    }
  ],
  "all_passed": true,
  "formula_evaluation_claimed": false,
  "output_files": [
    {
      "name": "baseline-and-normalized-order.json",
      "bytes": 601,
      "sha256": "9de1c612ae82e3c4dbdf00abe1aaf2c509a7925cb2e00eecf888f629588eaa2c"
    },
    {
      "name": "change-log.json",
      "bytes": 573,
      "sha256": "5eece163997905a316890f7acf8e84bf82e57a3218105b5ddae1c59b716558b9"
    },
    {
      "name": "comparison.json",
      "bytes": 4304,
      "sha256": "c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab"
    },
    {
      "name": "comparison.md",
      "bytes": 1319,
      "sha256": "403eb971cacecc3cb83f7c44af857306d72c36a19c8e27c7712abaf348c72800"
    },
    {
      "name": "comparison.xlsx",
      "bytes": 13524,
      "sha256": "e88467448f4b837723bb66cb0a5f92cc2d1a7e8737743dd00f3b90b7b0d55736"
    },
    {
      "name": "headline-unit-sort-baseline.csv",
      "bytes": 448,
      "sha256": "4672e1eba5c482d194c250de197e18b4e57a7703be9eb2c5e5185875067edf6a"
    },
    {
      "name": "original-10.csv",
      "bytes": 531,
      "sha256": "ce6b009a07c14160dc8c6f632815e9d06cb856018fdc8c129e9dd98d529e8435"
    },
    {
      "name": "questions.txt",
      "bytes": 504,
      "sha256": "fa572e87cedfce6246f78cc4f6f773da35ffde32f99a45c4c55cf97a0ef5bab2"
    },
    {
      "name": "revised-10.csv",
      "bytes": 540,
      "sha256": "93c64f00c828eb4c8cd168ebdc749f742a9d33a8e2e4ef653072081321d0d6aa"
    },
    {
      "name": "revised-20.csv",
      "bytes": 540,
      "sha256": "1161a12d8e5f8a55d3465624bb941dd98c45b4a1d8a97b4891c0ccd5e78916b6"
    },
    {
      "name": "selected-comparison.csv",
      "bytes": 540,
      "sha256": "1161a12d8e5f8a55d3465624bb941dd98c45b4a1d8a97b4891c0ccd5e78916b6"
    },
    {
      "name": "selected-comparison.json",
      "bytes": 1586,
      "sha256": "aafb2cefc8d163c2631ec55d7d60d95ad3fa195457781a255ddf17d940064a64"
    }
  ]
}
```

工作簿是含已計算數值的可編輯交付檔；更改數量或條件應重跑程式。本次真實 openpyxl data_only 回讀、公式格檢查與二進位所在路徑，見 `research/lab-execution-20261026.json`；以下摘錄該實際執行報告的數值／工作簿範圍，沒有追加新的執行宣稱。

```json
{
  "checked_at_utc": "2026-10-26T07:10:23.014410+00:00",
  "actual_execution": "Original ReportLab PDF creation; actual pypdf extraction; separate input-limited OpenAI Codex AI extraction and later quantity instruction; independent Decimal fixture verification; actual openpyxl value-only export/readback; actual relative command replay; actual preview rendering and visual inspection",
  "paid_calls_in_lab_agent": 0,
  "field_page_evidence_checks_per_run": 48,
  "standard_scenarios_passed": 16,
  "request_10_checks_passed": 17,
  "request_20_checks_passed": 17,
  "invalid_request_21_exit_code": 1,
  "invalid_request_output_created": false,
  "independent_quantity20_AI_analysis_matches_actual_recomputed_selected_table": true,
  "primary_tables": {
    "original-10": {
      "Aster": "2100.00",
      "Birch": "2050.00",
      "Cedar": null
    },
    "revised-10": {
      "Aster": "2100.00",
      "Birch": "2050.00",
      "Cedar": "2100.00"
    },
    "revised-20": {
      "Aster": "3990.00",
      "Birch": "4100.00",
      "Cedar": "3937.50"
    }
  },
  "baseline": "Actual raw unit-price sort Cedar 175, Aster 180, Birch 205. This is an arithmetic baseline, not a fabricated failed AI response.",
  "xlsx": "Actual openpyxl XLSX contains editable computed values and sources. It is NOT a live formula calculator; change request and rerun. No formula evaluation by openpyxl is claimed.",
  "pdf_scope": "Text PDFs only, no OCR; no general claim about other AI PDF vision products."
}
```


## 20張畫面相對命令的實跑原始輸出與 selected_result

以下直接取自真實 `research/lab-relative-command-execution.json`。其 cwd、argv、exit0、stdout 與 selected_result 都內嵌給查核者；不要求其假裝已開過本機路徑。這次重播是程式讀「已保存的AI抽取」重算，不是再次呼叫AI。

### 原始 cwd 與 argv

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
  "stderr": ""
}
```

### 原始 stdout（逐字）

```text
{"output": "comparison-output", "checks": 17, "all_passed": true, "winners": {"original-10": ["Birch"], "revised-10": ["Birch"], "revised-20": ["Cedar"]}}
```

### 實際 selected_result（逐欄保留）

```json
{
  "request": {
    "scenario": "revised",
    "quantity": 20
  },
  "request_sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
  "rows": [
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

### 此次實跑來源與輸出 hash

```json
{
  "code_sha256": "35103b82d83b527b897bbc171e8d71e40431ebc0c4412a9c3ce62b898b160ea1",
  "analysis_sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
  "extracted_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
  "request_sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
  "selected_output_sha256": "aafb2cefc8d163c2631ec55d7d60d95ad3fa195457781a255ddf17d940064a64",
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


## 21張範圍拒絕的完整真實收據

這是同一採購／同一程式的真負面輸入驗證，不是AI模型讀錯或供應商服務失敗。四份第2頁只授權10–20張；21張沒有新總價，也沒有建立 comparison-21。以下直接複製目前收據，保留原始Traceback與最後一行，不把預期輸出冒充實跑。

### `research/quantity-21-relative-execution.json` 全文

實際檔案 SHA-256：`67baa2c706b7a4c77992a6880e7ac9f038465760a8fe6bdc78305e4a86bb5fec`；2099 bytes。以下逐字複製，不重寫。

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

`materials/questions-21.txt` 是真實寫下的詢問草稿，文字已在上方逐字給出；沒有寄信、聊天傳送、下單或新的供應商報價。


## 教材封裝與現行可重播證據

教材ZIP／解壓重播是另一次真實執行，不能拿 ZIP 存在充當主影片完成。以下來源報告明列當時實際產物與重播結果；本次ledger復原沒有再次執行其命令。

### `research/lab-materials-archive-replay-20261026.json` 全文

實際檔案 SHA-256：`2a11ffbba4f022c2daa39a339cd97a2e9b56b3b9a442d6c0bd46d6824a8bda0b`；7443 bytes。以下逐字複製，不重寫。

```json
{
  "schema_version": 1,
  "performed_by": "OpenAI Codex /root/pdf_materials_refresh",
  "checked_at_utc": "2026-10-26T09:24:56.392817+00:00",
  "archive": "/workspace/work/ai-pdf-01/lab/ai-pdf-comparison-materials.zip",
  "archive_sha256": "541234b6bc0f26725e4670339568eb92c122d89caf1b43ea7e2a25ec70fbb1e7",
  "archive_bytes": 1011175,
  "fresh_extraction_root": "/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked",
  "manifest_sha256": "fcb88351134ed6da5301d36d6cf141f5ed13547f7eec896105dc1269497a6894",
  "manifest_entries_verified": 54,
  "archive_members": 55,
  "crc_check_passed": true,
  "all_manifest_names_bytes_hashes_matched": true,
  "bundled_output_moved_before_replay": "/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/bundled-comparison-output",
  "python_version": "Python 3.12.14",
  "installed_versions": {
    "openpyxl": "3.1.5",
    "pypdf": "6.10.0",
    "reportlab": "4.4.9",
    "Pillow": "12.3.0"
  },
  "input_files": [
    {
      "path": "materials/build_comparison.py",
      "sha256": "35103b82d83b527b897bbc171e8d71e40431ebc0c4412a9c3ce62b898b160ea1",
      "bytes": 18205
    },
    {
      "path": "materials/fixture-truth.json",
      "sha256": "ba02380452061fe58abc6a4187566b9d101dce26f9c9242efcf85cda87ad37ee",
      "bytes": 1648
    },
    {
      "path": "materials/request-20.json",
      "sha256": "53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62",
      "bytes": 46
    },
    {
      "path": "materials/request-21-invalid.json",
      "sha256": "0f3f6f5c96284192bfc545f951e9c24f68b3867837f05ec8efa67f213fb99b4e",
      "bytes": 46
    },
    {
      "path": "research/lab-ai-extraction.json",
      "sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
      "bytes": 22847
    },
    {
      "path": "research/lab-extracted-pages.json",
      "sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
      "bytes": 6693
    }
  ],
  "commands": [
    {
      "executed_at_utc": "2026-10-26T09:24:56.058918+00:00",
      "cwd": "/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked/materials",
      "argv": [
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
      "output_directory_existed_before": false,
      "output_directory_created": true,
      "totals": {
        "Aster": "3990.00",
        "Birch": "4100.00",
        "Cedar": "3937.50"
      },
      "checks": 17,
      "all_checks_passed": true,
      "selected_json_matches_bundled_result": true,
      "outputs": [
        {
          "name": "baseline-and-normalized-order.json",
          "bytes": 601,
          "sha256": "9de1c612ae82e3c4dbdf00abe1aaf2c509a7925cb2e00eecf888f629588eaa2c"
        },
        {
          "name": "change-log.json",
          "bytes": 573,
          "sha256": "5eece163997905a316890f7acf8e84bf82e57a3218105b5ddae1c59b716558b9"
        },
        {
          "name": "comparison.json",
          "bytes": 4304,
          "sha256": "c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab"
        },
        {
          "name": "comparison.md",
          "bytes": 1319,
          "sha256": "403eb971cacecc3cb83f7c44af857306d72c36a19c8e27c7712abaf348c72800"
        },
        {
          "name": "comparison.xlsx",
          "bytes": 13525,
          "sha256": "e9afd9cd419f195b78bd06070ced41923dacadfd32f430a44030ec30d28fa996"
        },
        {
          "name": "headline-unit-sort-baseline.csv",
          "bytes": 448,
          "sha256": "4672e1eba5c482d194c250de197e18b4e57a7703be9eb2c5e5185875067edf6a"
        },
        {
          "name": "original-10.csv",
          "bytes": 531,
          "sha256": "ce6b009a07c14160dc8c6f632815e9d06cb856018fdc8c129e9dd98d529e8435"
        },
        {
          "name": "questions.txt",
          "bytes": 504,
          "sha256": "fa572e87cedfce6246f78cc4f6f773da35ffde32f99a45c4c55cf97a0ef5bab2"
        },
        {
          "name": "revised-10.csv",
          "bytes": 540,
          "sha256": "93c64f00c828eb4c8cd168ebdc749f742a9d33a8e2e4ef653072081321d0d6aa"
        },
        {
          "name": "revised-20.csv",
          "bytes": 540,
          "sha256": "1161a12d8e5f8a55d3465624bb941dd98c45b4a1d8a97b4891c0ccd5e78916b6"
        },
        {
          "name": "selected-comparison.csv",
          "bytes": 540,
          "sha256": "1161a12d8e5f8a55d3465624bb941dd98c45b4a1d8a97b4891c0ccd5e78916b6"
        },
        {
          "name": "selected-comparison.json",
          "bytes": 1586,
          "sha256": "aafb2cefc8d163c2631ec55d7d60d95ad3fa195457781a255ddf17d940064a64"
        },
        {
          "name": "verification.json",
          "bytes": 5311,
          "sha256": "1f8b6b5f54b6fa169c8b7b6662d3dab9b8341f2d9ef505c5d5c7eefea01231f1"
        }
      ]
    },
    {
      "executed_at_utc": "2026-10-26T09:24:56.234822+00:00",
      "cwd": "/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked/materials",
      "argv": [
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
      "stderr": "Traceback (most recent call last):\n  File \"/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked/materials/build_comparison.py\", line 234, in <module>\n    if __name__ == '__main__': main()\n                               ^^^^^^\n  File \"/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked/materials/build_comparison.py\", line 196, in main\n    selected_rows = make_rows(quote_map, originals if selected_request['scenario']=='original' else revised, selected_request['quantity'])\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked/materials/build_comparison.py\", line 70, in make_rows\n    result = delivered(fields, qty)\n             ^^^^^^^^^^^^^^^^^^^^^^\n  File \"/workspace/work/ai-pdf-01/materials-replay-20261026T092456Z/unpacked/materials/build_comparison.py\", line 46, in delivered\n    raise ValueError('Quantity outside explicitly quoted range')\nValueError: Quantity outside explicitly quoted range\n",
      "output_directory_existed_before": false,
      "output_directory_created": false,
      "expected_last_stderr_line": "ValueError: Quantity outside explicitly quoted range",
      "expected_rejection_observed": true
    }
  ],
  "passed": true,
  "scope": "Real local replay from the final refreshed ZIP using already-saved actual AI extraction; no API or paid request, no new extraction/OCR/model invocation, no authenticated download verification. Source code and README unchanged during replay."
}
```


## 本次只補回證據，未代填品質或核准

c17、c18、c37 的詢問／比較狀態是教學建議與已寫草稿；它們不是供應商已回覆的事實。c29、c30 是所選文字路線的一般限制，不是假造本次模型出錯。所有金額都只能在這份虛構需求、同一規格與明示範圍中比較；不得變成真實供應商推薦。

原生 verifier 回答中「CONFIRMED／0 changed」只代表該次回答及其實際收到的資料；若它曾收到佔位ledger，不能追溯聲稱讀到未提供的八頁或stdout。本次把這些證據真正放回來後，仍須以現行source跑真正的獨立查核。原生歷史全文另存於前述 history檔，沒有被刪除，也沒有修改成看似先前已查到全部資料。

本次復原沒有安裝、執行PDF產生／計算、呼叫AI／TTS／Jev、取得站主核准、上傳或發布，也沒有變更影片旁白、auto、付費收據、原始claims canonical。這份候選只讓下一輪查核有完整、可核對的真實文字證據。

## 真正作者批次修訂：新的比較差額與操作

這次移除近義重述並增加核對動作，非新的供應商回覆或模型測試。原生事實查核與聽眾審稿需要重新進行；不沿用先前關卡冒稱新稿已通過。

| ID | 主張 | 實際證據 |
| --- | --- | --- |
| c38 | 修訂十張丙2100.00比乙2050.00多50.00；修訂二十張乙4100.00比甲3990.00多110.00，丙3937.50比甲3990.00少52.50 | research/lab-comparison.json 真值的實際 Python Decimal 差額，以下附完整新計算紀錄 |

### revised-ten-price-difference.json

```json
{
  "calculated_at_utc": "2026-10-26T09:39:08.624608+00:00",
  "method": "Actual Python Decimal subtraction of saved real lab output; no model or supplier request",
  "input": "research/lab-comparison.json",
  "input_sha256": "c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab",
  "scenario": "revised-10",
  "cedar_delivered_total": "2100.00",
  "birch_delivered_total": "2050.00",
  "cedar_minus_birch": "50.00",
  "meaning": "Revised Cedar remains fifty TWD above Birch for ten cards; fictional exercise currency and conditions only."
}
```

### revised-twenty-price-difference.json

```json
{
  "calculated_at_utc": "2026-10-26T09:42:58.217461+00:00",
  "method": "Actual Python Decimal subtraction of saved real lab output; no model or supplier request",
  "input": "research/lab-comparison.json",
  "input_sha256": "c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab",
  "scenario": "revised-20",
  "aster_delivered_total": "3990.00",
  "birch_delivered_total": "4100.00",
  "birch_minus_aster": "110.00",
  "meaning": "For twenty cards Birch is 110 TWD above Aster; fictional exercise only."
}
```

### revised-twenty-cedar-gap.json

```json
{
  "calculated_at_utc": "2026-10-26T09:45:49.134871+00:00",
  "method": "Actual Python Decimal subtraction of saved real lab output; no model or supplier request",
  "input": "research/lab-comparison.json",
  "input_sha256": "c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab",
  "scenario": "revised-20",
  "aster_delivered_total": "3990.00",
  "cedar_delivered_total": "3937.50",
  "aster_minus_cedar": "52.50"
}
```

修訂後 source SHA256 e4d3825137fde933e6976e9a8c2236ce93e3eaa68f851665e7a4f2b5337b5fc5；55scenes／93lines。

## 實際第10輪來源查核與聽眾用字

原生聽眾審稿只修改7dp4，清楚說先另存新檔名再改數量；實際第10輪查核報告 verify-10.md 為42CONFIRMED、0CHANGED、0NOT_FOUND。查核輸入videoSHA 648ddf2634f2412e7163fd23d5d0f721ba0c6d1f82616ff0396877e43783aee3。所有原生返回claims另存 research/claims-native-round-10-return.md，完整原始證據仍保留。


## 正文實測不足後新增的相鄰數量實算（c39–c41）

本片第一版真正錄音正文14024frames/30fps=467.466667秒，未滿480秒；此時才加入同一虛構採購的有用新操作，沒有以片頭片尾、慢播、重述或靜音補時。實際原88個語音請求的快取保留，原始正文與時間軸在repo外 before-threshold 保存。新實算不是AI模型/供應商服務呼叫；用相同已保存的AI抽取結果、同一套原文與實際比較程式執行。

| ID | 精確主張 | 真證據與限制 |
| --- | --- | --- |
| c39 | 真正另存request-12.json及request-13.json，各為revised情境，只改數量，完整兩條畫面命令實跑exit0，仍僅三家 | materials兩檔全文＋下方quantity-threshold-12-13-execution actual_runs/stdout/selected_result；都在四份PDF第2頁明示10–20範圍，不是新供應商報價 |
| c40 | 12張：甲2478.00、乙2460.00、丙2467.50，乙最低；13張：甲2667.00、乙2665.00、丙2651.25，丙最低 | 真正新輸出各selected_result及獨立Decimal公式；12張丙比乙貴7.50，13張丙比乙便宜13.75 |
| c41 | 丙減乙的送達差額由+7.50變成-13.75；同一固定運費下，乙每多一張商品含稅增加205.00，丙增加183.75，相對每張追回21.25 | 同一實際兩份selected_result goods_gross及delivered_total，用Decimal獨立相減；正負號只是此算式方向，不擴張為真實供應商推薦 |

需求兩檔逐字：

### request-12.json
```json
{
  "scenario": "revised",
  "quantity": 12
}
```

### request-13.json
```json
{
  "scenario": "revised",
  "quantity": 13
}
```

真實兩次執行及獨立核對全文（原始stdout與selected_result皆完整保留）：
```json
{
  "schema_version": 1,
  "method": "Actual existing comparison program, two changed request files, exact saved AI extraction and eight-page sources; separate Decimal formulas independently check selected outputs; no new AI/provider/supplier call",
  "reason": "First actual narrated body was measured467.466667seconds, below480; add a new useful threshold-finding operation instead of silence/repetition/slow speech",
  "input_code_sha256": "35103b82d83b527b897bbc171e8d71e40431ebc0c4412a9c3ce62b898b160ea1",
  "analysis_sha256": "f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8",
  "extracted_pages_sha256": "586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c",
  "actual_runs": [
    {
      "executed_at_utc": "2026-10-26T11:09:38.768031+00:00",
      "cwd": "/workspace/work/ai-pdf-01/repro-package/materials",
      "command": [
        "python3",
        "build_comparison.py",
        "--analysis",
        "../research/lab-ai-extraction.json",
        "--extracted",
        "../research/lab-extracted-pages.json",
        "--request",
        "request-12.json",
        "--out",
        "comparison-12"
      ],
      "exit_code": 0,
      "stdout": "{\"output\": \"comparison-12\", \"checks\": 17, \"all_passed\": true, \"winners\": {\"original-10\": [\"Birch\"], \"revised-10\": [\"Birch\"], \"revised-20\": [\"Cedar\"]}}\n",
      "stderr": "",
      "request_file": "materials/request-12.json",
      "request_sha256": "470f32f0126f80a526165455dabf16195c4895a5f0f46f68638208f401b53dab",
      "selected_result": {
        "request": {
          "scenario": "revised",
          "quantity": 12
        },
        "request_sha256": "470f32f0126f80a526165455dabf16195c4895a5f0f46f68638208f401b53dab",
        "rows": [
          {
            "supplier": "Aster",
            "source_file": "aster.pdf",
            "quantity": 12,
            "unit_price": "180.00",
            "unit_tax_mode": "exclusive",
            "goods_gross": "2268.00",
            "shipping_gross": "210.00",
            "delivered_total": "2478.00",
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
            "quantity": 12,
            "unit_price": "205.00",
            "unit_tax_mode": "inclusive",
            "goods_gross": "2460.00",
            "shipping_gross": "0.00",
            "delivered_total": "2460.00",
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
            "quantity": 12,
            "unit_price": "175.00",
            "unit_tax_mode": "exclusive",
            "goods_gross": "2205.00",
            "shipping_gross": "262.50",
            "delivered_total": "2467.50",
            "status": "可比較",
            "comparable": true,
            "lead_business_days": 7,
            "price_source": "cedar-revised.pdf p.1",
            "shipping_source": "cedar-revised.pdf p.2",
            "lowest_comparable": false
          }
        ]
      },
      "selected_result_sha256": "69c124266f2d43caf09b60cf1a096e3eb9523bd38e74d742f6dc2611349b3a62",
      "independent_decimal_totals": {
        "Aster": "2478.00",
        "Birch": "2460.00",
        "Cedar": "2467.50"
      },
      "independent_check_passed": true,
      "winner": "Birch"
    },
    {
      "executed_at_utc": "2026-10-26T11:09:38.941935+00:00",
      "cwd": "/workspace/work/ai-pdf-01/repro-package/materials",
      "command": [
        "python3",
        "build_comparison.py",
        "--analysis",
        "../research/lab-ai-extraction.json",
        "--extracted",
        "../research/lab-extracted-pages.json",
        "--request",
        "request-13.json",
        "--out",
        "comparison-13"
      ],
      "exit_code": 0,
      "stdout": "{\"output\": \"comparison-13\", \"checks\": 17, \"all_passed\": true, \"winners\": {\"original-10\": [\"Birch\"], \"revised-10\": [\"Birch\"], \"revised-20\": [\"Cedar\"]}}\n",
      "stderr": "",
      "request_file": "materials/request-13.json",
      "request_sha256": "08ebad425a955e34cffc984a7ae131dd9401887cc013a9fa7423f46058c434c1",
      "selected_result": {
        "request": {
          "scenario": "revised",
          "quantity": 13
        },
        "request_sha256": "08ebad425a955e34cffc984a7ae131dd9401887cc013a9fa7423f46058c434c1",
        "rows": [
          {
            "supplier": "Aster",
            "source_file": "aster.pdf",
            "quantity": 13,
            "unit_price": "180.00",
            "unit_tax_mode": "exclusive",
            "goods_gross": "2457.00",
            "shipping_gross": "210.00",
            "delivered_total": "2667.00",
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
            "quantity": 13,
            "unit_price": "205.00",
            "unit_tax_mode": "inclusive",
            "goods_gross": "2665.00",
            "shipping_gross": "0.00",
            "delivered_total": "2665.00",
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
            "quantity": 13,
            "unit_price": "175.00",
            "unit_tax_mode": "exclusive",
            "goods_gross": "2388.75",
            "shipping_gross": "262.50",
            "delivered_total": "2651.25",
            "status": "可比較",
            "comparable": true,
            "lead_business_days": 7,
            "price_source": "cedar-revised.pdf p.1",
            "shipping_source": "cedar-revised.pdf p.2",
            "lowest_comparable": true
          }
        ]
      },
      "selected_result_sha256": "67681c31721565460b7c72a5e4adcd632887ef363dd6dba66da4770f80838dd1",
      "independent_decimal_totals": {
        "Aster": "2667.00",
        "Birch": "2665.00",
        "Cedar": "2651.25"
      },
      "independent_check_passed": true,
      "winner": "Cedar"
    }
  ],
  "margin_calculation": {
    "at_12_cedar_minus_birch": "7.50",
    "at_13_birch_minus_cedar": "13.75",
    "one_extra_cedar_goods_gross": "183.75",
    "one_extra_birch_goods_gross": "205.00",
    "relative_gain_per_extra_piece": "21.25"
  },
  "scope": "All quantities stay within the original explicit10–20 range; only same fictional procurement, source versions and shipping conditions. No real supplier recommendation.",
  "additional_actual_decimal_derivation": {
    "calculated_at_utc": "2026-10-26T11:13:14.850233+00:00",
    "method": "Actual Python decimal.Decimal subtraction of both actual selected_result goods_gross/delivered_total strings; fixed shipping unchanged in both outputs",
    "cedar_goods_increase": "183.75",
    "birch_goods_increase": "205.00",
    "relative_gain": "21.25",
    "cedar_minus_birch_at_12": "7.50",
    "cedar_minus_birch_at_13": "-13.75"
  }
}
```
