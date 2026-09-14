# 搜尋爬蟲與 AI 爬蟲：網站管理者該怎麼辨識與管理：查證與編輯紀錄

正文非空白字數（排除標題、表格）：2240

來源網站只提供選題標題，未以來源文章正文作為撰稿依據。以下官方來源由撰稿者實際查閱；案例與檢查方法為原創建議。

## 主張與來源

- 2026-09-14 Google 官方說明確認抓取／索引分界、robots.txt 不強制存取保護、noindex 需能抓取才能發現，以及 Google-Extended 無獨立 HTTP UA 且不控制 Google 搜尋收錄。
- 2026-09-14 使用 OpenAI Docs，直接開啟 platform.openai.com/docs/bots 轉址的 developers.openai.com/api/docs/bots 正文。確認 OAI-SearchBot／GPTBot 獨立用途、ChatGPT-User 使用者觸發且 robots.txt 可能不適用。Markdown 入口工具不支援，改用 HTML 實際正文，不依搜尋片段判斷。
- 2026-09-14 Google 來源驗證文件確認反向後正向 DNS 與公開 IP 清單。本文不固定寫死供應商 IP，供實際設定時查詢。
- 修繕網站政策、CDN 對照、登入驗收與紀錄清單為原創建議。未更動本專案 robots、防火牆、正式站或使用者服務；本篇為可匯入教學文章。

## 配圖

封面與圖解均為 Mokaair 原創 SVG，無外部素材或外部參照。
