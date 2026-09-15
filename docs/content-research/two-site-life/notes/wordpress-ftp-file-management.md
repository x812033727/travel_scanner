# WordPress 檔案傳輸：用 SFTP 管理網站檔案：查證與編輯紀錄

正文非空白字數（排除標題、表格）：1985

來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。

## 主張與來源

- 2026-09-14 查閱 FileZilla 官方連線文件：站台管理員、協定、帳號與密碼或私鑰登入。未實際登入遠端主機；不指定讀者通訊埠。https://filezillapro.com/docs/v3/basic-usage-instructions/connecting-to-a-server/
- WinSCP 官方核對主機金鑰文件說明首次信任、後續變更警告，以及主機金鑰與使用者驗證金鑰不同。協定頁支持 SFTP 使用 SSH、FTPS 使用 TLS 的區別。https://winscp.net/eng/docs/ssh_verifying_the_host_key https://winscp.net/eng/docs/protocols
- WordPress Hardening 支持優先 SFTP、最小檔案寫入權限與常見 755/644；避免採用舊 File Permissions 文件中逐步放寬到 777 的範例，本文依主機擁有者模型個別處理。https://developer.wordpress.org/advanced-administration/security/hardening/
- WordPress 編輯檔案文件要求修改前備份並於錯誤時恢復原始檔。WordPress.com 權限文件說明直接 SFTP 上傳媒體可能需要另外登錄媒體庫，託管檔案也可能不可更改。本文不將平台預設權限套用全體主機。https://developer.wordpress.org/advanced-administration/wordpress/edit-files/ https://developer.wordpress.com/docs/guides/manage-permissions/
- 工作室案例、變更紀錄欄位與回復驗證順序為原創建議；不提供可直接執行的遞迴權限或刪除指令。查證日均為 2026-09-14。

## 配圖

封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。
