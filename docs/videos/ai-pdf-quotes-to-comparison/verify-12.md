# verify-12.md — ai-pdf-quotes-to-comparison（第12輪獨立查核，2026-10-26）

查核輸入：payload 內 video.json（55 scenes）、claims.md 證據 ledger（含八頁 pypdf 抽文全文、requirements／viewer-prompt／request 檔全文、comparison／selected_result／stdout／stderr 收據）、brief、sources（pypdf、openpyxl 官方頁皆 status 200，本日讀取）。

本片所有金額、稅率、張數、範圍與交期都是原創虛構練習資料。它們的依據是 ledger 內逐字附上的 PDF 抽文與實跑收據，不是官網數字，所以卡片不需要「官網 YYYY-MM-DD」標示。真正引用官方頁的只有兩項功能性主張：openpyxl 不計算公式、pypdf 不做 OCR。兩項都只出現在描述欄，且都能在官方頁原文找到。所有算式都已用 Decimal 邏輯逐一手算複核。

| # ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after |
|---|---|---|---|---|
| 1 ｜ 開場：最低單價還不能直接排第一 ｜ opening/6vwc ｜ ledger c10、c13 ｜ CONFIRMED ｜ — |
| 2 ｜ 單價：甲180未稅、乙205含稅、丙175未稅 ｜ opening-unit ｜ aster/birch/cedar.pdf p1 抽文 ｜ CONFIRMED ｜ — |
| 3 ｜ 需求：10張 A6 105×148、350gsm 霧面白卡、雙面全彩、同稿、同地址、7工作天內 ｜ need-spec code、need-start/ddpd ｜ requirements.txt 全文（第7–8行） ｜ CONFIRMED（行號正確） ｜ — |
| 4 ｜ 比的是送達含明示稅額總價（第8–9行） ｜ need-delivery code ｜ requirements.txt 第8–9行 ｜ CONFIRMED ｜ — |
| 5 ｜ 三家原檔 aster/birch/cedar.pdf，原件保留、輸出另存 ｜ need-labels ｜ ledger c3 ｜ CONFIRMED ｜ — |
| 6 ｜ 供應商、條件、稅率為虛構練習 ｜ need-fiction、description ｜ 每頁「Fictional training quote…」、requirements 第3–5行 ｜ CONFIRMED ｜ — |
| 7 ｜ 文字 PDF 抽文 → AI 讀逐頁原文 → 精確小數計算 ｜ need-route、extract-start ｜ ledger c5、analysis-execution 收據 ｜ CONFIRMED ｜ — |
| 8 ｜ 甲單價在第1頁、送貨條件在第2頁 ｜ need-proof/m57n、extract-aster ｜ aster.pdf p1、p2 ｜ CONFIRMED ｜ — |
| 9 ｜ 甲：單價180未稅 p1、商品稅5% p1、運費200未稅 p2 ｜ extract-aster ｜ aster.pdf p1–2 ｜ CONFIRMED ｜ — |
| 10 ｜ 引文「Shipping: TWD 200.00 excluding tax to the specified address」 ｜ extract-aster-quote ｜ aster.pdf p2 逐字 ｜ CONFIRMED ｜ — |
| 11 ｜ 七行提示詞全文（第1–7行） ｜ extract-core ｜ viewer-prompt.txt 全文逐字 ｜ CONFIRMED ｜ — |
| 12 ｜ 欄位定義：規格與數量、單價與稅、送貨條件 ｜ extract-fields ｜ viewer-prompt 第2行、analysis-prompt ｜ CONFIRMED ｜ — |
| 13 ｜ 乙：205含稅 p1、運費0免運 p2、交期5工作天 p2 ｜ extract-birch/q7x8 ｜ birch.pdf p1–2 ｜ CONFIRMED ｜ — |
| 14 ｜ 引文「Shipping: not quoted」（丙第2頁） ｜ extract-missing-quote ｜ cedar.pdf p2 逐字 ｜ CONFIRMED ｜ — |
| 15 ｜ shipping_amount 值為 null、page 2、附 evidence ｜ extract-null ｜ analysis-prompt JSON 契約；comparison.json 丙 null ｜ CONFIRMED（卡片標為「示意」） ｜ — |
| 16 ｜ 單價排序：丙→甲→乙 ｜ cost-start、cost-unit-baseline ｜ baseline-and-normalized-order.json ｜ CONFIRMED ｜ — |
| 17 ｜ 甲10張：1,800＋90＋210＝2,100 ｜ cost-aster-formula ｜ comparison.json original-10；手算 ｜ CONFIRMED ｜ — |
| 18 ｜ 乙10張：10×205＝2,050，免運，不重複加稅 ｜ cost-birch-formula ｜ birch.pdf p1「No second goods tax…」；comparison.json ｜ CONFIRMED ｜ — |
| 19 ｜ 十張結果：甲2,100.00、乙2,050.00、丙待確認 ｜ cost-initial-result、asset 註記 ｜ original-10 ｜ CONFIRMED ｜ — |
| 20 ｜ 值以計算工具算出，試算表不是活公式，需求改了要重產 ｜ cost-rounding、cost-workbook/ehby ｜ ledger c14、c15；lab-execution xlsx 說明 ｜ CONFIRMED ｜ — |
| 21 ｜ 丙商品比乙便宜，運費不夠高時名次會翻（1,837.50 對 2,050） ｜ missing-start/e86a ｜ comparison.json goods_gross ｜ CONFIRMED ｜ — |
| 22 ｜ 丙已知：175未稅、商品稅5%、數量10–20；未知：運費、含稅狀態、稅額 ｜ missing-known ｜ cedar.pdf p1–2 ｜ CONFIRMED ｜ — |
| 23 ｜ 詢問草稿，尚未寄出 ｜ missing-question、missing-no-send ｜ ledger c17 ｜ CONFIRMED（未宣稱已寄出） ｜ — |
| 24 ｜ 狀態欄規則（規格不同為條件式示例） ｜ missing-status ｜ ledger c18 ｜ CONFIRMED ｜ — |
| 25 ｜ 引文「Replaces CED-1026-v1; not an additional supplier.」 ｜ revision-identity ｜ cedar-revised.pdf p1 逐字 ｜ CONFIRMED ｜ — |
| 26 ｜ 修訂版：運費250未稅、運費稅5%，單價175不變 ｜ revision-diff/hiqk ｜ cedar-revised.pdf p2「Only delivery terms changed」 ｜ CONFIRMED ｜ — |
| 27 ｜ 丙修訂10張：1,837.50＋262.50＝2,100.00，與甲同價 ｜ revision-total/ambg ｜ revised-10；手算 ｜ CONFIRMED ｜ — |
| 28 ｜ 修訂十張：乙2,050最低，丙比乙多50 ｜ revision-ranking/dyun、loop ｜ revised-ten-price-difference.json ｜ CONFIRMED ｜ — |
| 29 ｜ 來源欄改指修訂版 ｜ revision-links ｜ revised-10 的 price_source／shipping_source ｜ CONFIRMED ｜ — |
| 30 ｜ request-20.json 內容為 revised、20 ｜ quantity-edit、quantity-start/7dp4 ｜ request-20.json 全文 ｜ CONFIRMED ｜ — |
| 31 ｜ 20張命令實跑：argv 逐字相符、exit 0 ｜ quantity-run ｜ lab-relative-command-execution.json ｜ CONFIRMED（有實跑證據） ｜ — |
| 32 ｜ 輸出：數量20、修訂版、甲乙丙修訂版共3列 ｜ quantity-output ｜ selected_result ｜ CONFIRMED ｜ — |
| 33 ｜ 三家都明示10–20張；甲200、丙250範圍內固定；乙免運 ｜ quantity-ranges/sxtz ｜ 三份 p2 抽文 ｜ CONFIRMED ｜ — |
| 34 ｜ 甲20張：3,780＋210＝3,990 ｜ quantity-aster ｜ revised-20 ｜ CONFIRMED ｜ — |
| 35 ｜ 乙20張：4,100，比甲多110 ｜ quantity-birch/m8sb ｜ revised-twenty-price-difference.json ｜ CONFIRMED ｜ — |
| 36 ｜ 丙20張：3,675＋262.50＝3,937.50，比甲少52.50 ｜ quantity-cedar/gy4i ｜ revised-twenty-cedar-gap.json ｜ CONFIRMED ｜ — |
| 37 ｜ 二十張排名：丙3,937.50＜甲3,990＜乙4,100 ｜ quantity-ranking/cbe9 ｜ revised-20 winners Cedar ｜ CONFIRMED ｜ — |
| 38 ｜ request-12／13 全文與兩條命令實跑 exit 0 ｜ threshold-request12/run12/request13/run13 ｜ quantity-threshold actual_runs ｜ CONFIRMED（有實跑證據） ｜ — |
| 39 ｜ 12張：甲2,478、乙2,460、丙2,467.50，乙最低；13張：甲2,667、乙2,665、丙2,651.25，丙最低 ｜ threshold-results ｜ selected_result 12/13；手算 ｜ CONFIRMED ｜ — |
| 40 ｜ 12張丙比乙多7.50；13張丙領先乙13.75 ｜ 6nxr、7jrk ｜ margin_calculation ｜ CONFIRMED ｜ — |
| 41 ｜ 每加一張：205.00−183.75＝21.25 ｜ threshold-margin/petb ｜ additional_actual_decimal_derivation ｜ CONFIRMED ｜ — |
| 42 ｜ request-21-invalid.json 全文與命令 ｜ range21-request、range21-run ｜ quantity-21-relative-execution.json ｜ CONFIRMED ｜ — |
| 43 ｜ 「ValueError: Quantity outside explicitly quoted range」，exit 1，未建立資料夾 ｜ range21-result/9jiq ｜ 同上，output_directory_created=false ｜ CONFIRMED（實際觀察到的失敗） ｜ — |
| 44 ｜ 21張重報詢問句 ｜ range21-question ｜ questions-21.txt 逐字 ｜ CONFIRMED ｜ — |
| 45 ｜ openpyxl 只寫檔，不計算公式 ｜ description ｜ https://openpyxl.readthedocs.io/en/stable/simple_formulae.html 「openpyxl never evaluates formula」 ｜ CONFIRMED ｜ — |
| 46 ｜ 本流程不做掃描影像 OCR ｜ description ｜ https://pypdf.readthedocs.io/en/stable/user/extract-text.html 「pypdf is not OCR software.」 ｜ CONFIRMED ｜ — |
| 47 ｜ 使用 Codex AI 文件分析，未實測商用 AI 上傳介面；AI 也讀了 analysis-prompt 契約 ｜ description ｜ analysis-execution 收據 ｜ CONFIRMED ｜ — |
| 48 ｜ 標題、縮圖（先算總價／稅與運費別漏算）、tags ｜ youtube、thumbnail ｜ 同上述計算 ｜ CONFIRMED ｜ — |
| 49 ｜ asset 註記「A2100/B2050/C未知」 ｜ assets ｜ original-10 ｜ CONFIRMED ｜ — |
| 50 ｜ 語氣、節奏、loop 鋪陳 ｜ 全片 ｜ — ｜ OUT OF SCOPE ｜ — |

## 計數
CONFIRMED 49；CHANGED 0；NOT FOUND 0；OUT OF SCOPE 1。changed_facts = 0，video 不需修改（回傳 null）。

## 教學卡片：示範與實跑證據
- 有實跑證據的觀察結果：20張命令（exit 0）、12／13張命令（exit 0）、21張命令（exit 1、ValueError 逐字相符、未建立資料夾）。卡片上的 argv 與收據逐字一致。
- 只作為操作指示、沒有被說成已觀察到成功的：qrv8「打開試算表核對」、326u／m5sn「打開輸出確認」。這些對應的輸出內容都有收據支持，且沒有宣稱操作過 Excel 介面。
- 沒有發現把預期結果寫成已觀察成功的地方。

## 即將過期的事實
- 練習報價寫有「Valid … through 2026-11-30」，但旁白與畫面都沒說這個日期，影響僅限教材本身。
- 官方文件頁首版本會變動（pypdf 頁面 6.21.2、openpyxl 頁面 3.1.3），影片沒有提到版本號。實際安裝版本 pypdf 6.10.0、openpyxl 3.1.5 也沒有出現在影片中。

## 觀點不符
無。全片沒有站主觀點句，也沒有假裝成站主親身經驗或習慣的句子。內容與站主觀點立場 1、3、4、6、7 一致：先算實際成本、回原文核對、只報真正執行的結果。

## 懷疑但未修改
1. threshold-results 的 source「實際comparison-12/13｜原報價第1–2頁」：丙其實取自 cedar-revised.pdf，「原報價」可能被誤讀為原版。數字本身正確，所以只建議下一輪措辭改為「三家報價第1–2頁（丙修訂版）」。
2. 7jrk「丙就領先十三元七角五分」：比較對象是乙（丙對甲領先15.75）。上一句6nxr與threshold-margin都明確是丙對乙，語境足夠清楚，不改。
3. extract-null 的 JSON 標為「示意」。ledger 沒有逐字附 normalized-quotes.json 的丙欄位全文，但 null、page 2 與 evidence 字串都和 cedar.pdf p2、comparison.json 一致。
4. 描述欄只提到修訂版與十改二十張，沒提12／13／21張段落。這屬於取捨範圍，不是事實錯誤。
5. 要求「7個工作天內」、乙交期5天：沒有影響比較結果，旁白也沒有誤述。
