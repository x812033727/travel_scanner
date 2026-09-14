# WordPress 寄信失敗怎麼辦：SMTP、網域驗證與記錄：查證與編輯紀錄

正文非空白字數（排除標題、表格）：2176

來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。

## 主張與來源

- 2026-09-14 官方 WP Mail SMTP Brevo 流程：API v3 金鑰、From 同驗證網域、Force From 與測試；未引用可靠度行銷文案或固定免費額度。https://wpmailsmtp.com/docs/how-to-set-up-the-sendinblue-mailer-in-wp-mail-smtp/
- 2026-09-14 Brevo 官方新舊流程交叉核對：逐步推出、DKIM 類型依帳號、DMARC 已有紀錄勿盲目替換。優先採 Brevo 最新帳號流程，不套用外掛文件較舊的固定兩 TXT 說法。https://help.brevo.com/hc/en-us/articles/12163873383186-Authenticate-your-domain-with-Brevo-Brevo-code-DKIM-DMARC ； https://help.brevo.com/hc/en-us/articles/35337929909778-Set-up-your-domain-in-Brevo
- 2026-09-14 官方 Email Test、Debug Events 及 Setup Wizard 文件查閱；區分付費完整 Email Log 與基本錯誤追蹤。https://wpmailsmtp.com/docs/how-to-send-a-test-email-in-wp-mail-smtp/ ； https://wpmailsmtp.com/docs/how-to-debug-email-sending-issues-in-wp-mail-smtp/ ； https://wpmailsmtp.com/docs/how-to-use-the-wp-mail-smtp-setup-wizard/
- 2026-09-14 Brevo Transactional Logs 官方核對事件及查詢欄位。https://help.brevo.com/hc/en-us/articles/360021533839-Manage-your-transactional-logs-and-email-previews
- 原創逐段排查與測試案例；沒有申請帳號、修改 DNS、發出實測郵件或宣稱送達率。

## 配圖

封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。
