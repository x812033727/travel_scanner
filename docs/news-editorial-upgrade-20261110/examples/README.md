# 三篇實際改稿

狀態：繁中離線樣稿，三篇均經非作者獨立查核；尚未匯入、翻譯或發布。原稿為 2026-11-10 直接從公開 API 取得的動態文章，並非本 worktree 內的靜態內容包。

| 篇目 | 文稿 | 增加的實用資訊 | 查核 |
| --- | --- | --- | --- |
| Apple 用量包 | [閱讀樣稿](apple/article.md) | 台灣訂閱與加購範圍分開、必要方案／裝置條件、扣除順序、共享及到期規則 | [獨立覆核](apple/review-1.md) |
| Instagram Effect Builder | [閱讀樣稿](instagram/article.md) | 製作資格、照片預覽、審查與分享階段、作者連結；不承諾收益或台灣已開放 | [獨立覆核](instagram/review-1.md) |
| Google Maps × AI Studio | [閱讀樣稿](maps/article.md) | 地圖原型任務、每 API 配額、帳號路徑差異、試用與正式上線條件 | [獨立覆核](maps/review-1.md) |

各目錄的 `draft.json` 用於閱讀預覽，**不是正式 content-pack schema**。`article.md` 與 JSON 對應；review 固定原研究檔的 SHA-256。repo 複本只統一 CRLF 為 LF，原始與 repo 雜湊對照在 [REVIEW-MANIFEST.json](../REVIEW-MANIFEST.json)；沒有改寫正文。Maps 的單句精確化保留 v1 與 v2 紀錄，現行版本為 v2。

`sources.md` 和 review 是離線研究紀錄的複本。裡面 `evidence/`、`review-evidence-1/`、原稿 JSON 等相對名稱均指原研究工作區：`<home>/.codex/tmp/mokaair-editorial-upgrade-20261110/drafts/<apple|instagram|maps>/`；它們不是此文件目錄內的檔案。為避免把外部原文整頁複製進 repo，原始 HTML 與完整公共文章快照保留在該工作區。來源 URL、日期及文稿雜湊可在此交叉檢視。

互動預覽可切換三篇樣稿，以及原標題／導讀快照；原稿全文以連結開啟，不重製全部正文。新版展示完整小樣。預覽不是正式網站頁面或功能實測證據。

後續正式發布前仍須按 content-pipeline 轉為內容包、補齊圖像／語言處理，重新核對會變動的價格與適用條件，並走匯入與公開頁驗收。
