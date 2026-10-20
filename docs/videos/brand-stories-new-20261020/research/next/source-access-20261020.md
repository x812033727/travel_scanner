# 下一批三題來源連線查核（待重查）

2026-10-20 15:40 UTC，替下一批候選 A28 Levi’s、B13 養樂多、B19 寶礦力水得重新開啟官方來源時，三個 HTTPS 請求均遭本雲端環境代理在 CONNECT 階段回覆 `403 Forbidden`（`curl: (56) CONNECT tunnel failed`），未收到來源網站的正文，不能視為當日來源查核。

| 題目 | 嘗試開啟的原始官方來源 | 結果 |
| --- | --- | --- |
| A28 | https://www.levistrauss.com/2025/03/24/evolution-of-riveted-denim/ | CONNECT 403；正文未取得 |
| B13 | https://www.yakult.co.jp/company/about/history/ | CONNECT 403；正文未取得 |
| B19 | https://www.otsuka.com/jp/company/history/detaile/story_02.html | CONNECT 403；正文未取得 |

本機 `/etc/codex/network-policy.json` 的套用中 HTTP 政策為 `restricted`，僅列平台套件／程式碼來源，未列以上三個品牌網站。雲端設定草稿或舊題庫記錄不能代替當日重開原始來源。舊 `docs/videos/story-plans/brand-stories-100/stories/{A28,B13,B19}.json` 將各來源的上次檢查日記為 2026-09-28；此頁不重新背書其支持範圍。

連線政策生效後，先重開上述官方來源，再核每一敘事主張及其他來源，最後才撰寫新的六章企劃與獨立雜湊查核；在此之前這三題只是候選，沒有新一批可匯入檔或待製作影片。
