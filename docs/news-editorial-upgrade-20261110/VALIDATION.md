# 本輪驗證

- 三篇來源查核由非作者完成：Apple／Instagram 由 layout_review 覆核，Maps 由 article_layout 覆核。皆 PASS，沒有待修事實。官方來源與未知條件見各篇紀錄。
- 12 個稿件／來源／查核檔與研究工作區逐位元比較，除 Maps JSON 的 CRLF→LF 之外完全相同；雙份 SHA-256 在 REVIEW-MANIFEST.json。三份 JSON 可解析，標題、導讀、小標、正文與列點均與 Markdown 一致；表格由獨立查核逐項確認。
- 預覽 18 種組合通過：三篇文章 × 原標題導讀／完整改稿 × 1024、390、320 寬度。無水平溢出或頁面 JavaScript 錯誤；鍵盤可切換版本。
- 捲到 Maps 比較表後另取得 390、320 淺色與 1024 深色截圖，表頭及四列均在可視範圍。root 與獨立覆核者親看後通過，320 最後一列靠下緣但文字完整。
- 原先外層 fullPage 擷取有 iframe 畫面外的空白區，只列為不完整擷取，不用來宣稱已驗完整文章；後續用實際捲動畫面補齊比較表。
- 預覽曾在外觀事件重繪時遇到表格 DOM 被替換；已改為只在選擇狀態真正變化時恢復狀態，18 組與整表檢查重新通過。
- README、INTEGRATION 與本輪三票由 layout_review 獨立覆核通過；合併範圍與費用授權措辭已精確化。沒有修改已活躍的其他任務。
- 任務格式驗證 2,391 檔通過（既有其他任務的過期／重疊認領警告仍在）；repo hygiene 3/3 通過、退出碼 0；git diff --check 通過。

證據在 `<home>/.codex/tmp/mokaair-editorial-upgrade-20261110/`：`preview-check.json`、`table-check.json`、三篇 `review-1.md`、`package-review.md` 與截圖。來源快照與瀏覽器操作證據保留在本機，未把整頁外部原文提交到 repo。

這些驗證僅支持內容示範與預覽可讀性，不支持正式站已更新、App 功能已實測、模型產出已改善、SEO／點閱／收入已提升等結論。
