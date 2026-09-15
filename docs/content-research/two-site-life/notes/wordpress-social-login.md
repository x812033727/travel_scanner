# WordPress 社群登入：LINE、Google 與 Facebook 的串接檢查：查證與編輯紀錄

正文非空白字數（排除標題、表格）：2199

來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。

## 主張與來源

- 2026-09-14 核對 Nextend 官方外掛頁：Google/Facebook 免費、LINE Pro、會員表單整合、個人頁連結解除功能。https://wordpress.org/plugins/nextend-facebook-connect/
- 2026-09-14 核對 LINE 官方回呼及電子郵件權限，再核對 Nextend 欄位；未沿用 Nextend 舊的 Messaging API 建立官方帳號說明。https://developers.line.biz/en/docs/line-login/integrate-line-login/ https://social-login.nextendweb.com/documentation/providers/line/
- 2026-09-14 Google 官方確認 redirect_uri 精確匹配，Nextend 文件用於外掛操作；未泛稱所有 Google 登入都需相同審查。https://developers.google.com/identity/protocols/oauth2/web-server https://social-login.nextendweb.com/documentation/providers/google/
- 2026-09-14 Nextend Facebook 現行設定章節要求驗證/審查/發布，但同頁舊 FAQ 相衝突；正文明確歸屬 Nextend 現行章節並要求核對 Meta 實際狀態。Meta 官方 Advanced Access、App Review 與連結聲明嘗試開啟均 Internal Error，未宣稱完成直接查證，也未承諾個人帳號一定可公開使用。https://social-login.nextendweb.com/documentation/providers/facebook/
- 2026-09-14 核對不支援 WebView 的按鈕設定，不沿用舊平台瀏覽器支援斷言。https://social-login.nextendweb.com/documentation/settings/general-settings/
- 收藏清單與連結驗收為原創情境；未建立應用程式、取得密鑰或實際登入。

## 配圖

封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。
