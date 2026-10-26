# verify-1.md — ai-pdf-quotes-to-comparison（第 1 輪事實查核，2026-10-26）

查核範圍：video.json 全部 56 個場景、107 句的 text／say、每張卡片 data、thumbnail、youtube.title、description、tags。數字依據有三種：

- 官方頁面（今日抓取成功者）。
- 本片原創練習資料的實跑證據，也就是 claims.md 內嵌的 PDF 逐頁原句、Codex 分析紀錄、Decimal 三情境輸出、相對命令 argv／exit 0／stdout，以及 21 張拒絕紀錄。
- 逐項重算。

本片的價格、稅率、數量都是原創虛構教材，不是官方產品數字，所以沒有任何卡片需要寫「官網 YYYY-MM-DD」。本片也沒有可依賴的 mokaair.com 查證文章。

## 逐項判定

| # | claim | where | URL | verdict | before → after |
| --- | --- | --- | --- | --- | --- |
| 1 | 三家原報單價：甲 180 未稅、乙 205 含稅、丙 175 未稅 | opening-unit、cost-unit-baseline、missing-known、revision-diff | 原創 aster/birch/cedar.pdf 第1頁（claims 原句摘錄） | CONFIRMED | — |
| 2 | 需求：10 張 A6（105×148 mm）、350 gsm 霧面白卡、雙面全彩同稿、同一地址、7 個工作天內 | need-start、need-spec、need-delivery、d2m5 | materials/requirements.txt（未附全文）；PDF 規格原句對得上 | CONFIRMED（規格與 PDF 一致；requirements.txt 逐字內容見「懷疑未改」） | — |
| 3 | 原檔保留、輸出另存、不改原件 | need-labels、74dc | generation-receipt／相對命令紀錄 all_generated_files_outside_repo:true | CONFIRMED | — |
| 4 | 供應商、金額、5% 稅率皆為虛構練習設定 | need-fiction、description | claims c4；PDF fictional training quote 註記 | CONFIRMED | — |
| 5 | 逐頁文字抽取 → Codex AI 判讀 → Decimal 計算 → openpyxl 寫檔 | need-route、extract-start、description | claims 實際身分紀錄；https://openpyxl.readthedocs.io/en/stable/simple_formulae.html | CONFIRMED（官方頁：openpyxl never evaluates formula） | — |
| 6 | 甲的單價與商品稅在第1頁；運費 200 未稅、運費稅 5% 在第2頁 | need-proof、extract-aster、extract-aster-quote、cost-aster-formula | aster.pdf 第1–2頁原句 | CONFIRMED（引文 "Shipping: TWD 200.00 excluding tax to the specified address" 逐字相符） | — |
| 7 | 七行 viewer-prompt 全文；要求欄位、原句、頁碼、待確認、修訂版取代、交付物 | extract-core、extract-fields、description | ai-analysis-execution（viewer-prompt.txt 為第4輸入，442 bytes） | CONFIRMED（時序與讀取有紀錄；逐字內容見「懷疑未改」） | — |
| 8 | 乙 205 含 5% 商品稅、送達免運、交期 5 個工作天 | extract-birch、extract-review、cost-birch-formula | birch.pdf 第1–2頁原句 | CONFIRMED | — |
| 9 | 丙原版運費與其稅未報，shipping 保留 null，送達總價未知 | extract-missing-quote、extract-null、missing-start、missing-known | cedar.pdf 第2頁 "Shipping: not quoted"；lab-comparison original-10 Cedar delivered_total:null | CONFIRMED | — |
| 10 | 單價排序 丙→甲→乙 | cost-start、cost-unit-baseline | 175<180<205 重算 | CONFIRMED | — |
| 11 | 甲 10 張：1,800＋90＋210＝2,100 | cost-aster-formula、cost-initial-result | lab-comparison original-10 Aster delivered_total 2100.00；重算 | CONFIRMED | — |
| 12 | 乙 10 張：10×205＝2,050，運費 0，不二次加稅 | cost-birch-formula、cost-initial-result | birch.pdf "No second goods tax…"；lab-comparison 2050.00 | CONFIRMED | — |
| 13 | 原始 10 張：乙低於甲，丙待確認、不排名 | cost-initial-result、bcr5、tnrc | lab-comparison original-10（Birch lowest_comparable:true、Cedar comparable:false） | CONFIRMED | — |
| 14 | 算術交給計算工具（Decimal），不先四捨五入單價 | cost-rounding、cost-workbook | claims c14；verification 17 項通過 | CONFIRMED | — |
| 15 | 試算表存已算好的固定值；改需求要重新產生 | cost-workbook、description | https://openpyxl.readthedocs.io/en/stable/simple_formulae.html | CONFIRMED | — |
| 16 | 已含稅的小計不能再加一次稅 | cost-total-check | birch.pdf 第1頁原句 | CONFIRMED（條件式說明） | — |
| 17 | 具體待問草稿；未寄出 | missing-question、missing-no-send | claims c17（questions.txt） | CONFIRMED（畫面標為草稿，未說成已寄出或對方已回覆） | — |
| 18 | 狀態欄分三類，規格不同時先問 | missing-status | 卡片自標「原創教學建議」 | OUT OF SCOPE（教學建議，非實測結果） | — |
| 19 | 修訂版明示取代原版，仍是三家；來源欄改指向修訂版 | revision-start、revision-identity、revision-links | cedar-revised.pdf 第1頁 "Replaces CED-1026-v1; not an additional supplier."；revised-10 source_file 為 cedar-revised.pdf | CONFIRMED | — |
| 20 | 修訂版只改運費（250 未稅、5% 稅），商品單價 175 未變 | revision-diff | cedar-revised.pdf 第2頁 "Only delivery terms changed…" | CONFIRMED | — |
| 21 | 丙修訂 10 張：1,837.50＋262.50＝2,100.00 | revision-total | lab-comparison revised-10 Cedar；重算 10×175×1.05、250×1.05 | CONFIRMED | — |
| 22 | 補件後 10 張：乙 2,050 最低，甲丙 2,100 同價 | revision-ranking、dyun、u9p4 | lab-comparison revised-10；stdout winners revised-10:[Birch] | CONFIRMED | — |
| 23 | request-20.json 第1–4行全文：scenario revised、quantity 20 | quantity-edit | 輸入紀錄 46 bytes（與 4 行加結尾換行的位元組數吻合） | CONFIRMED | — |
| 24 | 命令在 materials 資料夾實跑，結果另存 | quantity-run | 相對命令紀錄：cwd .../materials、argv 與卡片逐字相同、exit 0 | CONFIRMED（有實跑證據，非預期結果） | — |
| 25 | 輸出內容：需求數量 20、採用修訂版、三列為甲／乙／丙修訂版 | quantity-output | selected-comparison 描述；revised-20 三列 | CONFIRMED | — |
| 26 | 三家單價都適用 10–20 張；甲 200、丙修訂 250 運費在範圍內固定；乙免運 | quantity-ranges | 三份 PDF 第2頁原句 | CONFIRMED | — |
| 27 | 甲 20 張：3,780＋210＝3,990 | quantity-aster、quantity-ranking | lab-comparison revised-20 Aster 3990.00 | CONFIRMED | — |
| 28 | 乙 20 張：20×205＝4,100 | quantity-birch、quantity-ranking | lab-comparison revised-20 Birch 4100.00 | CONFIRMED | — |
| 29 | 丙修訂 20 張：3,675＋262.50＝3,937.50，最低；甲乙差距反轉 | quantity-cedar、quantity-ranking、pruf、cbe9、thumbnail「換人贏了」 | lab-comparison revised-20 Cedar lowest_comparable:true；stdout winners revised-20:[Cedar] | CONFIRMED | — |
| 30 | 交付可編輯表、待問清單、版本變動清單 | handoff-start、handoff-output | 相對命令輸出檔清單（comparison.xlsx、questions.txt、change-log.json） | CONFIRMED | — |
| 31 | 掃描圖片的抽文可能是空的；需改用有辨識能力的流程 | handoff-scan、description | https://pypdf.readthedocs.io/en/stable/user/extract-text.html | CONFIRMED（"the extracted text may be minimal or visually empty… consider using OCR software"；"pypdf is not OCR software"） | — |
| 32 | 表格與多欄排版可能讓數字接錯位置 | handoff-table | 同上 pypdf 頁："Tables are just absolutely positioned text… hard to tell where columns / rows are"、Missing Semantic Layer | CONFIRMED | — |
| 33 | youtube.title「最低單價，真的最便宜？」 | youtube.title | 依上方各項計算 | CONFIRMED | — |
| 34 | description：資料與實作日期 2026-10-26、Codex、pypdf、Decimal、openpyxl 不計算公式、不做 OCR、七行提示詞與 JSON 契約並存 | description | claims、兩份官方頁 | CONFIRMED | — |
| 35 | tags | youtube.tags | — | OUT OF SCOPE | — |

## 計數

- CONFIRMED 33
- CHANGED 0
- NOT FOUND 0
- OUT OF SCOPE 2

changed_facts＝0，video 不改，回傳 null。

## 規則檢查

- **免責語**：旁白與 description 都沒有出現 以官網為準、公告沒寫、我不唸、不在這裡唸、不替你填 這一族用語。e86a「不表示」是在說明計算關係，不是「沒寫」型的免責語。
- **查證詞**：旁白沒有「經查證」「根據官方文件」「截至查證」「本影片」。
- **教學卡片實跑**：每個示範都有輸入、動作與實跑證據。命令卡有 argv、cwd 與 exit 0；輸出卡有 selected 結果；21 張拒絕例有 exit 1 紀錄，片中沒有使用。沒有把預期結果講成已觀察到的成功。

## 即將過期的事實

- 本片數字全是原創固定教材，不會過期。
- 官方文件的版本號不在片中。今日讀到 pypdf 文件是 6.21.2、openpyxl 文件是 3.1.3，本機實跑是 pypdf 6.10.0、openpyxl 3.1.5。片中描述的行為（pypdf 非 OCR、openpyxl 不計算公式）兩邊一致。若之後版本改變這兩項行為，要回頭重查 handoff-scan、cost-workbook 與 description。

## 觀點不符

- 片中沒有以站主口吻表述的個人觀點。outro 只邀請觀眾留言，沒有虛構站主經驗或習慣。
- 整體立場（先算清實際成本、AI 整理後回原文核對、只報真正執行的成果）與 brief 站主觀點 1、3、4、6、7 一致。
- 沒有發現未標記的觀點。

## 懷疑但未改

1. **requirements.txt 的逐字內容**：need-spec、need-delivery 兩張程式碼卡顯示 requirements.txt 第7–8行、第8–9行的逐字節錄，但 claims 沒有附這個檔案的全文。我只能確認規格與三份 PDF 一致，無法逐字比對。建議下一輪把該檔第1–10行摘進 claims。
2. **viewer-prompt.txt 的位元組數**：extract-core 七行全文我按 UTF-8 估算約 435–436 bytes，與紀錄的 lab 檔 442 bytes 差 6–7 bytes。可能原因包括 CRLF 換行、BOM，或 materials 與 lab 兩份檔案略有差異。沒有證據顯示文字錯誤，因此不改。建議以 sha256 6b491f22… 對照 materials/viewer-prompt.txt，確認卡片逐字等同。
3. **抓取失敗的網址**：sources 裡兩筆 404 是抓取器把 claims.md 中「URL（2026-10-26檢查」整段當成網址造成的。正確網址當天都抓取成功，不影響任何判定。已在 claims.md 把網址與日期分開寫，避免下次再誤抓。
4. **來源欄頁碼範圍**：quantity-ranges 的來源欄寫「三家 PDF 第2頁」，丙那一列實際出自 cedar-revised.pdf 第2頁，屬於同一套四份檔案。因為不是事實錯誤，沒有更動。
