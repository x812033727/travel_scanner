# 兩站標題盤點與 Mokaair 原創生活分享交付

完成日期：2026-09-14。232 篇原創文章已完成正文、來源查證、配圖及本機驗收，共 504,295 字，單篇 1,801–2,565 字。沿用既有 ArticlePack／GuideDocument，全部為 `kind: life`、`zh-TW`、`destination_id: null`，使用既有生活分享標籤。

本次交付為可審閱、可匯入的內容包。正式站匯入、發布與部署尚未執行；沒有新增 API 或資料庫結構，Git PR 與合併依使用者後續指示處理。

## PR 整合結果

以主分支 `0b120251a0dcd71af50b3db49eca1dc370569ff0` 的 398 篇內容包重新對照後，4 篇同需求文章已由主分支涵蓋。原創稿與圖片完整保留於 [superseded](superseded)，可匯入目錄只新增 **228 篇**。原始 232 篇製作與逐張視覺驗收紀錄仍保留，不能把 4 篇封存稿重複匯入。

| 封存原稿 | 使用的既有文章 |
| --- | --- |
| small-language-models | ai-term-small-language-model |
| rag-retrieval-explained | ai-term-retrieval-augmented-generation |
| generative-ai-basics | ai-term-generative-ai |
| claude-code-plugin-management | claude-code-plugins-guide |

[pr-integration.json](pr-integration.json) 保存整合基底、398 篇主分支標題、逐篇合併理由與站內連結修正。`claude-cowork-evaluation` 的生成式 AI 連結改指向既有文章。

[pr-evidence.json](pr-evidence.json) 保存原始批次雜湊、目前檔案雜湊與可逆轉換；原始批次紀錄沒有改寫。`final_audit.py` 會還原 LF 正規化與該站內連結修正，重新驗證全部 1,624 個原始雜湊。232 篇正文及 SVG 都不含兩個靈感網站的名稱或網址；來源標題僅留在內部研究文件。

## 先看這些檔案

| 交付 | 位置與內容 |
| --- | --- |
| 完整來源標題 | [titles.md](titles.md)：474 筆標題與文章連結 |
| 原始資料 | [titles.json](titles.json)：保留原始標題、清理後 title、來源、網址、查閱日及分頁核對 |
| 選題與處理對照 | [catalogue.md](catalogue.md)：232 篇原創選題、228 篇新增／4 篇封存及每筆來源處理結果 |
| 可讀取的題庫 | [catalogue.json](catalogue.json)：固定配圖需求、相關連結、228 篇 validated_local、4 篇 covered_upstream 狀態 |
| 來源對應 JSON | [mapping.json](mapping.json)：逐筆處理原因與 target_slug |
| 完整交付驗收 | [delivery-audit.json](delivery-audit.json)：232 篇檔案路徑、字數、來源數與驗證結果 |
| 查證紀錄 | [notes](notes)：每篇一份，記錄實際查閱來源、限制、原創情境與圖像來源 |
| 文章內容包 | [apps/api/app/guides/content](../../../apps/api/app/guides/content)：依 catalogue 的 validated_local slug 選取本次新增的 228 份 JSON |
| 圖片 | [apps/web/public/guides](../../../apps/web/public/guides)：每篇資料夾含 hero.jpg、hero.svg、diagram-1.svg |

PR 整合時內容包目錄共 626 篇，包含主分支的 398 篇。匯入本次成果時應依交付清單的 228 個 validated_local slug 選取。原始製作基底為 110 篇，批次紀錄中的 342 篇是當時快照。

## 來源完整性與去重結果

犬哥指定分類 394 筆，核對 40 個分頁；諾特斯公開文章索引 80 筆，核對 14 個分頁。合計 474 筆、54 個分頁。來源僅擷取標題與文章網址，不使用原站正文、推薦排名、優惠碼、實測結論或圖片創作新文。

| 來源處理 | 筆數 |
| --- | ---: |
| 對應一篇新增文章 | 228 |
| 與其他來源合併到同一篇新文章 | 224 |
| 既有文章已涵蓋（含 PR 整合 4 筆） | 11 |
| 原有 AI 規劃題目已涵蓋 | 10 |
| 站務招募公告，保留原因排除 | 1 |
| 總計 | 474 |

21 筆由既有／規劃題目涵蓋；其中 4 篇在本次製作後發現主分支已先合併同需求文章，因此封存原稿；其中 10 筆是原有 AI 規劃，不能視為本次已代為完成那個系列。排除項是諾特斯自身 YouTube 會員招募公告，完整原因保存在對照表。

諾特斯首頁分頁列出 78 篇，另有 2 篇出現在公開文章 API 而未列於首頁分頁，均已納入 80 筆：wordpress-blog-tutorial-cloudways、wordpress-org-recommendation。原始差異保存在 titles.json 的 verification，沒有默默剔除。

去重依主題、讀者問題及操作目的判斷，並與原有 110 篇、220 個 AI 規劃題目及當時 46 個文章任務核對；PR 整合另比對主分支新增的 288 篇。最終沒有新增未對照 slug；同目的來源合併，備份／搬家、商品型錄／完整報價等不同操作保留獨立文章。

## 正文、配圖與驗收

每篇具備原創案例、操作步驟、比較表、提醒、至少兩個相關內容包連結及有查閱日期的一手資料。沒有將示範情境寫成親身實測。產品功能、版本與規則以各篇查證紀錄為準。

232 張 1600×900 封面 JPG、232 份封面 SVG 與 232 張 SVG 圖解均自行繪製；PR 公開圖片目錄保留 228 張 JPG 與 456 份 SVG，其餘 4 張 JPG、8 份 SVG 留在封存目錄。圖像 credit 記為 Mokaair；沒有第三方照片或需另行取得的圖片授權。共 464 張渲染 QA PNG 已逐張檢視，確認無缺字、重疊與裁切。

12 批均通過個別 `guides.pack_cli ingest`、限定 slug lint、圖片渲染與內容包測試。每批內容包測試為 9 passed、5 skipped；5 項 PostgreSQL 整合測試因本機沒有對應測試資料庫略過。本機 ingest 是整理與驗證內容檔案，不能當作正式站已匯入。

最終驗收核對 232 篇的必備區塊、字數、life/null、來源日期、站內連結、圖片尺寸與作者資訊，並以可逆的整合紀錄重驗各批 1,624 項原始雜湊。PR 整合後對全部 626 份本機內容包比較，涉及本次文章的 50 字以上完全相同段落為零；語意去重另依選題表與逐批編輯核對。

站內連結已確認有對應本機內容包；正式發布時仍需讓被引用文章同時可用，這項檢查不代表線上網址已發布。

## 批次證據

| 批次 | 篇次 | 編輯、視覺與查證驗收 | 檔案證據 |
| --- | --- | --- | --- |
| 01 | 1–20 | [review](batch-01-review.md) | [audit](batch-01-audit.json) |
| 02 | 21–40 | [review](batch-02-review.md) | [audit](batch-02-audit.json) |
| 03 | 41–60 | [review](batch-03-review.md) | [audit](batch-03-audit.json) |
| 04 | 61–80 | [review](batch-04-review.md) | [audit](batch-04-audit.json) |
| 05 | 81–100 | [review](batch-05-review.md) | [audit](batch-05-audit.json) |
| 06 | 101–120 | [review](batch-06-review.md) | [audit](batch-06-audit.json) |
| 07 | 121–140 | [review](batch-07-review.md) | [audit](batch-07-audit.json) |
| 08 | 141–160 | [review](batch-08-review.md) | [audit](batch-08-audit.json) |
| 09 | 161–180 | [review](batch-09-review.md) | [audit](batch-09-audit.json) |
| 10 | 181–200 | [review](batch-10-review.md) | [audit](batch-10-audit.json) |
| 11 | 201–220 | [review](batch-11-review.md) | [audit](batch-11-audit.json) |
| 12 | 221–232 | [review](batch-12-review.md) | [audit](batch-12-audit.json) |

PR 整合另通過 228 個 slug 的 lint、內容包測試（9 passed、5 skipped）及任務檢查。整合未改動圖片像素或 SVG 內容；原始逐張視覺驗收仍適用。

相同目錄的 batch-NN-lint.log、batch-NN-tests.log 與任務檢查日誌保留實際輸出。早期批次文件記錄當時的剩餘工作，完整交付狀態以本檔、catalogue.json 與 delivery-audit.json 為準。

在儲存庫根目錄可用既有 API Python 執行 `docs/content-research/two-site-life/final_audit.py` 重查交付；它只讀取內容並寫入驗收報告，不匯入、發布或部署。原始來源與初始比對快照是本次盤點證據，後續重新擷取應另存日期版本。
