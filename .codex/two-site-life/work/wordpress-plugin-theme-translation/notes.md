# WordPress 主題外掛中文化：Loco Translate 與 Poedit 工作流：查證與編輯紀錄

正文非空白字數（排除標題、表格）：2139

來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。

## 主張與來源

- 2026-09-14 查閱 Loco manual/msginit：Author/System 更新覆寫風險，Custom 路徑與啟用時優先載入。https://localise.biz/wordpress/plugin/manual/msginit
- 2026-09-14 查閱 Loco custom-translations：自訂檔保留原系統回退，原文字串變更後需人工 Sync/Save。https://localise.biz/wordpress/plugin/custom-translations
- 2026-09-14 查閱 Poedit 現行官方 poedit.com 文件：WordPress 專用流程屬 Pro；伺服器儲存會上傳；可產出 MO、l10n.php、JS JSON，手動搬移須維持產出檔案。未實際連線或購買。https://poedit.com/docs/get-started/wordpress/
- 2026-09-14 WordPress 一手文件核對 POT/PO/MO 及佔位符、複數與上下文。https://developer.wordpress.org/apis/internationalization/localization/ ； https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/
- 原創預約介面校對案例；未宣稱實測外掛相容性。區別於多語系內容翻譯，本文專門處理程式介面字串。

## 配圖

封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。
