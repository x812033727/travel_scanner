# DNS 設定怎麼查：從 A、CNAME 到郵件紀錄：查證與編輯紀錄

正文非空白字數（排除標題、表格）：1977

來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。

## 主張與來源

A、AAAA、CNAME、MX、TXT、NS 用途｜https://www.cloudflare.com/learning/dns/dns-records/｜2026-09-14。
欄位及代理、別名展平為服務特定功能｜https://developers.cloudflare.com/dns/manage-dns-records/｜2026-09-14。
舊快取依先前 TTL；代理可能回傳平台 IP｜https://developers.cloudflare.com/dns/faq/｜2026-09-14。
nslookup 支援指定查詢類型；本文以 example.com 示範語法，未捏造執行結果｜https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup｜2026-09-14。
四層排查、資料保存與服務驗收為原創操作建議，沒有保證固定生效時間。

## 配圖

封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。
